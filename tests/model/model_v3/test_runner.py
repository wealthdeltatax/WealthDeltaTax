"""Tests N1 to N7 (architecture.md 6.2) and the R3 and R10 checks of acceptance.md for runner/runner.py and runner/sweeps.py (brief 055c)."""
import json
from pathlib import Path

import numpy as np
import pytest
import yaml

from model_v3.core import base as bs, pack as pk, returns as rt, schedule as sc
from model_v3.runner import runner as R, sweeps as S

ROOT = Path(__file__).parents[3]
SPEC = dict(tau_0=0.04, tau_m=0.9, k_ln=1.0, ratio=0.5)
ROW = lambda lo, c, hi: pk.Row('x', lo, c, hi, '%', False)


@pytest.fixture(scope='module')
def lv():
    return json.loads((ROOT / 'model' / 'model_v3' / 'levers.json').read_text())


@pytest.fixture(scope='module')
def out():
    return yaml.safe_load((ROOT / 'model-specs' / 'outputs.yml').read_text())


@pytest.fixture(scope='module')
def tier1(out):
    return next(o for o in out['outputs'] if o['id'] == 'OT1')['by']['input']


@pytest.fixture(scope='module')
def ctx(lv, tier1, out):
    return R.context(pk.load_pack(ROOT / 'data' / 'country-packs' / 'GBR'), pk.load_register(ROOT / 'data' / 'input-register' / 'inputs.json'), lv, tier1, [o['id'] for o in out['outputs']])


def level1(ctx, seed, n=40):
    return R.level1(ctx, {'S': SPEC}, rt.streams(seed)['level1_paths'], n=n, chunk=20)


def fake(m1=lambda o: 0.0):
    """An evaluator with one path: M1 is m1(over), every other headline constant."""
    def ev(spec, over=None, g=None):
        v = lambda x: np.array([x])
        return dict(M1={h: v(m1(over or {})) for h in R.HORIZONS}, M2={h: {'overall': v(1.0)} for h in R.HORIZONS}, M4a={h: {'overall': v(2.0)} for h in R.HORIZONS}, M3=v(3.0))
    return ev


def test_n1_same_seed_gives_byte_identical_samples(ctx):
    a, b, c = level1(ctx, 7)[0], level1(ctx, 7)[0], level1(ctx, 8)[0]
    assert R.digest(a) == R.digest(b) and R.digest(a) != R.digest(c)
    assert a['O1']['S', 'short', (), 'M1'].shape == (40,) and level1(ctx, 7)[1]['paths'] == 40


def test_n2_levels_are_separate_objects_and_r3_draws_the_tier1_list(ctx, tier1, out):
    s1, _ = level1(ctx, 7)
    l2 = R.level2(ctx, {'S': SPEC}, rt.streams()['level2_draws'], n=3, n_paths=20)
    assert isinstance(l2, R.Level2) and isinstance(s1, dict) and l2.samples is not s1
    assert l2.samples['O1']['S', 'short', (), 'M1'].shape == (3,) and set(l2.samples) == set(s1) <= {o['id'] for o in out['outputs']}
    assert set(l2.inputs) == set(tier1) and all(len(v) == 3 for v in l2.inputs.values())      # R3: the drawn ids are the tier 1 list


def test_level2_draws_have_the_registers_percentiles_and_are_never_clipped(ctx):
    d = R.draw_theta(np.random.default_rng(1), ctx, ['I-D5a', 'I-D4a', 'I-D9h'], 4000)
    for i, v in d.items():
        r = ctx.reg[i]
        assert np.allclose(np.percentile(v, [10, 50, 90]), [r.low, r.central, r.high], atol=0.06 * (r.high - r.low))
    bad = R.Ctx(**{**ctx.__dict__, 'reg': {**ctx.reg, 'I-D5a': ROW(0.1, 5.0, 6.0)}})
    with pytest.raises(R.RunnerError):
        R.draw_theta(np.random.default_rng(1), bad, ['I-D5a'], 400)


def test_r10_every_grid_cell_is_progressive(lv, ctx, out):
    g, by = S.grid(lv), next(o for o in out['outputs'] if o['id'] == 'OF1')['by']
    assert len(g) == 27 and {S.labels(s) for s in g} == {(a, b) for a in by['schedule_grid'] for b in by['w_min']}
    for s in g:
        sc.rate_function(s['k_ln'], s['tau_0'], s['tau_m'], bs.w_min(ctx.pack, s['ratio']), 'logistic_ln')


def test_the_burden_run_gives_the_same_receipts_as_run_lines(ctx):
    g = R.paths(np.random.default_rng(3).standard_normal((100, 12)), 4.742, 8.219, 0.3)
    a, b = (R.evaluate(ctx, ctx.centre, SPEC, g, np.full(g.shape, 0.015), full=f) for f in (False, True))
    assert all(np.allclose(a[x][h], b[x][h], atol=1e-9, equal_nan=True) for x in ('M1', 'M1a', 'M1c', 'M1d') for h in R.HORIZONS)


def test_core_run_applies_a_tweak_to_the_shaped_base_and_none_changes_nothing(ctx):
    g = R.paths(np.random.default_rng(3).standard_normal((100, 6)), 4.742, 8.219, 0.3)
    run = lambda **k: R.core_run(ctx, ctx.centre, SPEC, g, np.full(g.shape, 0.015), **k)
    a, b, c = run(), run(tweak=None), run(tweak=lambda x: x.__class__(**{**x.__dict__, 'w_min': 2 * x.w_min}))
    assert np.array_equal(a.r['M1'], b.r['M1'], equal_nan=True) and c.base.w_min == 2 * a.base.w_min and not np.array_equal(a.r['M1'], c.r['M1'], equal_nan=True)


def test_n3_tornado_rows_descend_and_unread_inputs_swing_zero():
    rows = {'a': ROW(0, 5, 10), 'b': ROW(0, 5, 10), 'c': ROW(0, 5, 10)}
    ev = fake(lambda o: 2.0 * o.get('a', 5) - 1.0 * o.get('b', 5))
    t = [r for r in S.tornado(ev, {'S': SPEC}, rows, {'a', 'b'}) if r['headline'] == 'M1' and r['horizon'] == 'short']
    assert [r['input'] for r in t] == ['a', 'b', 'c'] and (t[0]['low'], t[0]['high']) == (-10.0, 10.0) and (t[1]['low'], t[1]['high']) == (5.0, -5.0) and t[2]['high'] == 0.0
    assert {r['horizon'] for r in S.tornado(ev, {'S': SPEC}, rows, set()) if r['headline'] == 'M3'} == {'single'}


def test_n4_break_even_root_on_a_toy_case():
    assert abs(S.breakeven(lambda x: x - 3.55, 0, 15, 1e-4) - 3.55) < 1e-3 and np.isnan(S.breakeven(lambda x: x + 1, 0, 15))
    r = S.breakeven_return(fake(lambda o: o['m'] - 3.55), {'S': SPEC}, 'm', draws={'z': np.array([1.0, 2.0])})
    assert abs(r['S'][0] - 3.55) < 0.02 and len(r['S'][1]) == 2


def test_n5_named_schedules_follow_the_choice_rule_on_a_toy_map():
    pt = lambda n, f1, m2, m4: dict(spec=n, F1={'short': f1}, M2={'short': m2}, M4a={'short': m4})
    rule = dict(closure_share_pct=75, m2_cap_pct_per_year=2.0, m4a_floor_pct=0)
    pts = [pt('a', 80, 0.5, 5), pt('b', 95, 1.5, 5), pt('c', 90, 1.9, 5), pt('d', 99, 2.5, 5), pt('e', 99, 0.2, -1), pt('f', 70, 1.0, 5)]
    assert S.choose(pts, rule) == {'S_low': 'a', 'S_central': 'b', 'S_high': 'c'}                  # d breaks the cap, e the floor, f the closure share
    assert S.choose([pt('f', 70, 1.0, 5)], rule) is None


def test_n6_the_stress_path_closes_up_to_a_stated_amplitude(ctx):
    amps = (0, 2, 4, 8, 12)
    res, top = S.stress(R.make_ev(ctx, np.zeros((100, 1))), SPEC, 4.42, amps, 100)
    assert set(res) == set(amps) and all(np.isfinite(v['P3']) and v['P1'] >= 1 for v in res.values())
    assert top is None or all(res[a]['P3'] <= S.CLOSED for a in amps if a <= top)
    print('CK1 P3 by amplitude', {a: round(v['P3'], 2) for a, v in res.items()}, 'zero up to', top)


def test_n7_one_chunk_is_timed_and_a_schedule_of_10000_paths_fits_the_hour(ctx):
    (_, meta), sec = R.timed(R.level1, ctx, {'S': SPEC}, rt.streams()['level1_paths'], n=R.CHUNK)
    print(f'N7: {R.CHUNK} paths, one schedule, {sec:.1f} s; 10,000 paths about {10 * sec:.0f} s')
    assert meta['paths'] == R.CHUNK and 0 < 10 * sec < 3600


def test_the_tornado_runs_on_the_model_and_the_sweep_reports_the_map(ctx, lv):
    ev = R.make_ev(ctx, np.random.default_rng(5).standard_normal((100, 30)))
    rows = {i: ctx.reg[i] for i in ('I-D1a', 'I-D5a', 'I-D9a')}
    t = {r['input']: r for r in S.tornado(ev, {'S': SPEC}, rows, R.reads(ctx)) if r['headline'] == 'M1' and r['horizon'] == 'long'}
    assert t['I-D1a']['high'] > 0 > t['I-D1a']['low'] and t['I-D5a']['low'] > 0 > t['I-D5a']['high'] and t['I-D9a']['low'] == t['I-D9a']['high'] == 0.0
    pts, of1 = S.feasibility(ev, S.grid(lv)[:2])
    assert len(pts) == 2 and set(k[3] for k in of1) == {'F1', 'M2', 'M4a'} and set(np.unique(of1[next(iter(of1))])) <= {0.0, 100.0}


def test_the_bootstrap_check_and_the_30_year_spread(ctx):
    ev, (yrs, r) = R.make_ev(ctx, np.zeros((100, 1))), rt.real_series(ctx.pack)
    b = S.robustness(ev, SPEC, rt.streams()['bootstrap_check'], yrs, r, 100, 20)
    p = S.spread30(R.paths(np.random.default_rng(2).standard_normal((100, 400)), 4.742, 8.219, 0.3))
    assert b['M1']['short'].shape == (20,) and p[0] < p[1] < p[2]
