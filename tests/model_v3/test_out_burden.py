"""Brief 086c: the burden group fills the twelve ids: O2d, O2b, O2c, O4b, OL1, OH1b2, DH1c, O5, O6, O8, OH1b and OH1c."""
import numpy as np
import pytest

from model_v3.core import base as bs, burden as bd, returns as rt, revenue as rv
from model_v3.runner import out_burden as B, runner as R
from test_runner import SPEC, ctx, lv, out, tier1  # noqa: F401  (the fixtures)

KEY = lambda *by: tuple(sorted(by))


@pytest.fixture(scope='module')
def s1(ctx):
    return R.level1(ctx, {'S': SPEC}, rt.streams(7)['level1_paths'], n=60, chunk=30)[0]


def test_empty_input_gives_empty_output():
    assert B.per_path(None, None, None) == {} and B.cells({}) == {}


def test_each_built_id_has_one_cell_per_horizon_and_by_value(s1):
    n = {'O2d': 15, 'O2b': 45, 'O2c': 45, 'O4b': 33, 'OL1': 12, 'OH1b2': 1, 'DH1c': 33, 'O5': 30, 'O6': 45, 'O8': 4, 'OH1b': 5, 'OH1c': 10}
    assert {i: len(s1[i]) for i in B.IDS} == n and B.IDS == tuple(n)
    assert s1['O4b']['S', 'long', (('income_decile', 'D10'),), None].shape == (60,)
    assert ('S', 'short', KEY(('wealth_band', 'D10'), ('cutoff_pct_of_income', 20)), None) in s1['O2b']
    assert ('S', 'transition', (('reference_worker', 'p25'),), None) in s1['OL1']


def test_early_check_death_flows_are_the_larger_part_of_m2(s1):
    a, d = (np.nanmean(s1[i]['S', 'short', (('wealth_band', 'overall'),), None]) for i in ('O2', 'O2d'))
    assert d > 5 * a and abs(a - 2.8) < 0.28 and abs(d - 22.2) < 2.22        # 053c's central run: 2.8 in life, 22.2 with death


def test_o2d_exceeds_o2_on_average_and_shares_are_percentages(s1):
    for h in R.HORIZONS:
        a, d = (s1[i]['S', h, (('wealth_band', 'overall'),), None] for i in ('O2', 'O2d'))
        assert np.nanmean(d) > np.nanmean(a) > 0
    for k, v in s1['O2c'].items():
        assert np.nanmax(v) <= 100 + 1e-9
    assert np.nanmax(s1['O2b']['S', 'short', KEY(('wealth_band', 'D10'), ('cutoff_pct_of_income', 5)), None]) <= 100 + 1e-9


def test_ol1_is_positive_by_reference_worker(s1):
    v = [np.nanmean(s1['OL1']['S', 'long', (('reference_worker', p),), None]) for p in ('p25', 'p50', 'p75', 'p90')]
    assert all(x > 0 for x in v) 


def test_oh1b2_is_the_register_point_and_dh1c_the_pack_bill_share_on_every_path(s1, ctx):
    assert set(s1['OH1b2']['S', 'single', (), None]) == {ctx.reg['I-T1d'].central}
    v = s1['DH1c']['S', 'short', (('income_decile', 'D1'),), None]
    bill, inc = bd.pack_deciles(ctx.pack)
    assert v.shape == (60,) and np.allclose(v, 100 * bill[0] / inc[0]) and np.allclose(s1['DH1c']['S', 'long', (('income_decile', 'overall'),), None], 100 * bill.sum() / inc.sum())


def test_o5_o6_are_register_values_and_diff_is_against_m2_in_life(s1, ctx):
    m = lambda i, *by, h='short', ln=None: np.nanmean(s1[i]['S', h, tuple(sorted(by)), ln])
    for c in B.COMPARATORS:
        assert 0.5 < m('O5', ('comparator', c), ln='burden') < 3 and abs(m('O5', ('comparator', c), ln='burden') - m('O5', ('comparator', c), ln='diff') - m('O2', ('wealth_band', 'overall'))) < 1e-9
    assert m('O6', ('wealth_band', 'D10'), ln='total', h='long') == pytest.approx(ctx.reg['I-M6i'].central + ctx.reg['I-M6b'].central)


def test_o8_is_short_only_with_revenue_equal_to_the_m1_headline_and_diff_is_against_m2(s1, ctx):
    assert {k[1] for k in s1['O8']} == {'short'}
    raw = R.core_run(ctx, ctx.centre, SPEC, R.paths(np.random.default_rng(3).standard_normal((100, 8)), 4.7, 8.2, 0.3), np.full((100, 8), ctx.gdp_g))
    lo, hi, gdp = raw.lo['short'], raw.hi['short'], raw.r['gdp']
    rev = rv.window_mean(raw.r['M1'] * gdp, np.ones_like(gdp), lo, hi)
    assert np.allclose(rev / rv.window_mean(gdp, np.ones_like(gdp), lo, hi), rv.window_mean(raw.r['M1'], gdp, lo, hi), equal_nan=True)      # M1 headline: share of GDP
    e = B.per_path(raw, R.env_of(ctx, ctx.centre), None)['O8']['gains']
    ok = np.isfinite(e['burden'])
    assert ok.any() and np.allclose((e['burden'] - e['diff'])[ok], bd.m2(raw.fl, lo, hi)['overall'][ok]) and np.nanmean(e['burden']) > 0


def test_oh1b_and_oh1c_are_static_once_single_horizon_cells_over_1000_paths(ctx):
    a, b = (B.static(R.env_of(ctx, ctx.centre, rt.streams(7)['level1_paths'].bit_generator.seed_seq)) for _ in range(2))
    assert {k: v.shape for k, v in a['OH1b'].items()}[('single', (('wealth_band', 'D10'),), None)] == (1000,) and len(a['OH1b']) == 5 and len(a['OH1c']) == 10
    assert all(np.array_equal(a[i][k], b[i][k], equal_nan=True) for i in a for k in a[i])
    assert 0 < np.nanmean(a['OH1b'][('single', (('wealth_band', 'overall'),), None)]) < 30
    g, c, th = rt.ar1_paths(np.random.default_rng(1), *[ctx.centre[i] for i in ('I-D1a', 'I-D1b', 'I-D1b2')], 30, 50), ctx.centre['I-D14c'] / 100, ctx.centre
    f = lambda b: np.nanmean(bd.m3_today(b, g, c, ctx.reg, tuple(th[i] for i in ('I-D11a', 'I-D11b', 'I-D11c')))['overall'])
    assert abs(f(R.shaped(ctx, ctx.centre, 0.5)) / f(bs.build_base(ctx.pack, ctx.reg, 0.5)) - 1) < 0.05       # unshaped is a fair stand-in: shaping scales payer wealth and M3 is a ratio
