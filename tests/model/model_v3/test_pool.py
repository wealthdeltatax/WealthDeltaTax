"""Brief 150c: pool.pmap and the sweeps that take `workers`. Serial and parallel give byte-identical results (same units, same seeds)."""
import json
from pathlib import Path

import numpy as np
import pytest
import yaml

from model_v3.core import pack as pk
from model_v3.runner import out_sweeps, pool, runner as R, sweeps as S

ROOT = Path(__file__).parents[3]
SPEC = dict(tau_0=0.04, tau_m=0.9, k_ln=1.0, ratio=0.5)
ROW = lambda lo, c, hi: pk.Row('x', lo, c, hi, '%', False)


def raw(x):
    """The bytes of a nested result: floats by hex, arrays by dtype, shape and buffer. (Not pickle: its bytes differ with how objects are shared, not with their values.)"""
    if isinstance(x, dict):
        return b'{' + b','.join(raw(k) + b':' + raw(v) for k, v in x.items()) + b'}'
    if isinstance(x, (list, tuple)):
        return b'[' + b','.join(raw(v) for v in x) + b']'
    if isinstance(x, np.ndarray):
        return x.dtype.str.encode() + repr(x.shape).encode() + x.tobytes()
    return float(x).hex().encode() if isinstance(x, (float, np.floating)) else repr(x).encode()


same = lambda a, b: raw(a) == raw(b)


def noisy(spec, over=None, g=None):
    """A cheap evaluator whose arrays depend on every input and carry noise seeded by them, so a unit run in the wrong place or order would show."""
    o = over or {}
    r = np.random.default_rng(int(1e6 * (sum(o.values()) + spec['tau_m'] + 7 * spec['k_ln']))).standard_normal(8)
    v = lambda x: x + 0.01 * r
    return dict(M1={h: v(o.get('m', 0.0) - 3.55 + o.get('a', 0.0)) for h in R.HORIZONS}, M2={h: {'overall': v(1.0)} for h in R.HORIZONS}, M4a={h: {'overall': v(2.0)} for h in R.HORIZONS},
                M3=v(3.0), P3h={h: np.where(r > 0, 0.0, 1.0) for h in R.HORIZONS},
                sweeps={'of1': {(m, h): dict(p3=np.where(r > 0, 0.0, 1.0 + m), M2=v(1.0), M4a=v(2.0)) for m in out_sweeps.MARGINS for h in ('transition', 'short')}})


def test_pmap_keeps_the_order_and_the_serial_default():
    f = lambda x: x * x
    assert pool.pmap(f, range(9)) == pool.pmap(f, range(9), 3) == [x * x for x in range(9)] and pool.pmap(f, [], 4) == []
    assert (pool.n_workers(None), pool.n_workers(1), pool.n_workers(3)) == (1, 1, 3) and pool.n_workers(0) >= 1


def test_a_unit_that_raises_raises_in_the_caller():
    def f(x):
        if x == 2:
            raise ValueError('unit 2')
        return x
    for w in (1, 2):
        with pytest.raises(ValueError, match='unit 2'):
            pool.pmap(f, range(4), w)


def test_roots_tornado_and_map_are_byte_identical_serial_and_parallel():
    rows, sp = {'a': ROW(0, 5, 10), 'b': ROW(0, 5, 10), 'c': ROW(0, 5, 10)}, {'S_low': SPEC, 'S_high': dict(SPEC, tau_m=0.5)}
    draws = {'z': np.array([1.0, 2.0, 3.0, 4.0]), 'a': np.array([0.5, 1.0, 1.5, 2.0])}
    be = lambda w: S.breakeven_return(noisy, sp, 'm', draws=draws, tol=1e-3, workers=w)
    to = lambda w: S.tornado(noisy, sp, rows, {'a', 'b'}, workers=w)
    fe = lambda w: S.feasibility(noisy, S.grid(json.loads((ROOT / 'model' / 'model_v3' / 'levers.json').read_text()))[:5], workers=w)
    for f in (be, to, fe):
        assert same(f(1), f(2)) and same(f(2), f(3))
    assert all(len(r[1]) == 4 for r in be(2).values()) and any(np.isfinite(r[0]) for r in be(2).values())


def test_the_model_tornado_is_byte_identical_serial_and_parallel():
    lv, out = json.loads((ROOT / 'model' / 'model_v3' / 'levers.json').read_text()), yaml.safe_load((ROOT / 'model-specs' / 'outputs.yml').read_text())
    tier1 = next(o for o in out['outputs'] if o['id'] == 'OT1')['by']['input']
    ctx = R.context(pk.load_pack(ROOT / 'data' / 'country-packs' / 'GBR'), pk.load_register(ROOT / 'data' / 'input-register' / 'inputs.json'), lv, tier1, [o['id'] for o in out['outputs']])
    ev, rows = R.make_ev(ctx, np.random.default_rng(5).standard_normal((100, 3))), {i: ctx.reg[i] for i in ('I-D1a',)}
    one, two = (S.tornado(ev, {'S': SPEC}, rows, {'I-D1a'}, workers=w) for w in (1, 2))
    assert same(one, two) and any(r['low'] != 0.0 for r in one)


def test_level_1_is_byte_identical_for_workers_1_2_and_3():
    """Brief 154c: the chunks' paths are drawn in order and the evaluations go through pmap: the Samples and the info do not depend on the worker count."""
    lv, out = json.loads((ROOT / 'model' / 'model_v3' / 'levers.json').read_text()), yaml.safe_load((ROOT / 'model-specs' / 'outputs.yml').read_text())
    tier1 = next(o for o in out['outputs'] if o['id'] == 'OT1')['by']['input']
    ctx = R.context(pk.load_pack(ROOT / 'data' / 'country-packs' / 'GBR'), pk.load_register(ROOT / 'data' / 'input-register' / 'inputs.json'), lv, tier1, [o['id'] for o in out['outputs']])
    specs = {'S_low': dict(SPEC, tau_m=0.5), 'S_high': SPEC}
    run = lambda w: R.level1(ctx, specs, np.random.default_rng(7), n=30, chunk=10, workers=w)
    one = run(1)
    assert same(one, run(2)) and same(one, run(3)) and one[1]['paths'] == 30


def test_a_shortfall_met_in_a_unit_reaches_the_callers_store_first_chunk_first(monkeypatch):
    """The cap store is module state: a forked unit records into its own copy, so the record must travel back and merge in chunk order (the first record stands)."""
    from types import SimpleNamespace
    from model_v3.core import support as U
    ctx = SimpleNamespace(centre={R.RET['mean']: 0.05, R.RET['sd']: 0.1, R.RET['phi']: 0.0}, gdp_g=0.01, ids=(), once=())
    def fake(ctx, th, spec, g, gdp_g, seq=None, key=()):
        if key[0] >= 1 and U._CAP is not None: U._CAP.setdefault('gains', (key[0], g.shape[1]))
        return dict(unfilled=np.zeros(g.shape[1]))
    monkeypatch.setattr(R, 'evaluate', fake); monkeypatch.setattr(R, 'cat', lambda parts: {'unfilled': np.concatenate([p['unfilled'] for p in parts])})
    monkeypatch.setattr(R, 'samples', lambda *a: {}); monkeypatch.setattr(R, 'statics', lambda *a: 0)
    for w in (1, 2, 3):
        store = {}
        with U.capping(store):
            R.level1(ctx, {'S': SPEC}, np.random.default_rng(1), n=30, chunk=10, workers=w, cap=store)
        assert store == {'gains': (1, 10)}, (w, store)           # chunk 1 is the first that met a shortfall, whatever the worker count
    R.level1(ctx, {'S': SPEC}, np.random.default_rng(1), n=30, chunk=10, workers=2)   # no store: nothing is recorded, nothing breaks


def test_illinois_roots_are_byte_identical_serial_and_parallel_and_keep_the_flag():
    """153c: the fewer-evaluations root method is a pure function of its unit, like bisection: the same bytes at any worker count, the same no-sign-change cells."""
    sp = {'S_low': SPEC, 'S_high': dict(SPEC, tau_m=0.5)}
    draws = {'z': np.array([1.0, 2.0, 3.0, 4.0]), 'a': np.array([0.5, 1.0, 1.5, 2.0])}
    be = lambda w, m: S.breakeven_return(noisy, sp, 'm', draws=draws, tol=1e-2, workers=w, method=m)
    assert same(be(1, 'illinois'), be(2, 'illinois')) and same(be(2, 'illinois'), be(3, 'illinois'))
    old, new = be(1, 'bisect'), be(1, 'illinois')
    for s in sp:   # flags cell by cell, and each root within 2 x tol of the bisection root (the author's rule, 2026-11-28)
        assert [np.isfinite(r) for r in [old[s][0], *old[s][1]]] == [np.isfinite(r) for r in [new[s][0], *new[s][1]]]
        assert all(abs(a - b) <= 2e-2 for a, b in zip([old[s][0], *old[s][1]], [new[s][0], *new[s][1]]) if np.isfinite(a))


def test_illinois_stops_in_a_bracket_around_a_sign_change_on_awkward_functions():
    """153c: a plateau then a jump at the root (the shape of M1 at the model's root), a hump, a flat triple root, a jump at the end, a nan in the middle: the bracket guarantee holds and the
    evaluations never exceed bisection's by more than the secant allowance; a smooth function takes far fewer."""
    tol, jump = 1e-2, lambda x: (0.002 if x < 11.217 else -0.03) + (0.001 * (x - 11.2) if x < 11.217 else 0.0)
    cases = {'smooth': lambda x: x - 3.55, 'jump': jump, 'hump': lambda x: 0.27 + 0.03 * x * (15 - x) / 8 - 0.04 * x * (x > 7.5), 'flat': lambda x: (x - 0.3) ** 3,
             'end': lambda x: np.tanh(3 * (x - 14.3)), 'nan': lambda x: float('nan') if 5.0 < x < 6.0 else x - 5.9}
    for name, g in cases.items():
        n = {'bisect': 0, 'illinois': 0}; root = {}
        for m in n:
            def f(x, m=m):
                n[m] += 1; return g(x)
            root[m] = S.breakeven(f, 0.0, 15.0, tol, method=m)
        assert np.isfinite(root['bisect']) == np.isfinite(root['illinois']), name
        if np.isfinite(root['illinois']):
            r = root['illinois']   # a bracket narrower than tol around r holds a sign change (jumps and zero crossings alike), or the function is nan in it
            a, b = g(r - tol / 2), g(r + tol / 2)
            assert a * b <= 0 or not np.isfinite(a * b), name
            assert abs(r - root['bisect']) <= 2 * tol or name in ('hump', 'nan'), (name, root)   # on a function with two sign changes the two methods may find different ones: reported, not accepted
        assert n['illinois'] <= n['bisect'] + 6, (name, n)
    assert n['illinois'] > 0
    c = {'bisect': 0, 'illinois': 0}
    for m in c:
        def f(x, m=m):
            c[m] += 1; return x - 3.55
        S.breakeven(f, 0.0, 15.0, tol, method=m)
    assert c['illinois'] * 2 <= c['bisect']
    assert np.isnan(S.breakeven(lambda x: x + 1, 0.0, 15.0, tol, method='illinois'))
