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
