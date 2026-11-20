"""Stage V3-8 tests D1 to D6 (architecture.md 6.2): hand cases to 1e-12 on small arrays, the pack decile table, and the reconciliation with revenue."""
from pathlib import Path
from types import SimpleNamespace as NS

import numpy as np
import pytest

from model_v3.core import base as bs, burden as bd, pack as pk, revenue as rv, schedule as sc

ROOT = Path(__file__).parents[2]
BANDS = ['D4-5', 'D10']


def flows(net, w0, wt, band, death=None, **kw):
    net, w0 = np.asarray(net, float), np.asarray(w0, float)
    return dict(net=net, w0=w0, wt=np.asarray(wt, float), band=band, death=np.zeros_like(net) if death is None else np.asarray(death, float), **kw)


@pytest.fixture(scope='module')
def pack():
    return pk.load_pack(ROOT / 'model_v3' / 'pack' / 'GBR')


@pytest.fixture(scope='module')
def reg():
    return pk.load_register(ROOT / 'registry' / 'inputs.json')


# ---- D1: M2 revenue-weighted --------------------------------------------------------------------------------------------------------------------------
def test_d1_m2_is_revenue_weighted_on_a_hand_case():
    fl = flows([[[1.0], [4.0], [-2.0]]], [[[10.0], [20.0], [5.0]]], [0.5, 0.5, 0.2], ['D4-5', 'D10', 'D10'])
    out = bd.m2(fl, 1, 1)
    assert abs(out['overall'][0] - 18.0) < 1e-12                     # (.5 x 1 x .1 + .5 x 4 x .2) / (.5 x 1 + .5 x 4); the refund line is not a payer
    assert abs(out['D4_5'][0] - 10.0) < 1e-12 and abs(out['D10'][0] - 20.0) < 1e-12 and np.isnan(out['D6_7'][0])
    assert abs(out['overall'][0] - 12.5) > 1                          # not the payer-weighted mean (12.5)


def test_d1_m2_window_and_the_death_flows():
    fl = flows([[[1.0]], [[3.0]]], [[[10.0]], [[10.0]]], [1.0], ['D10'], death=[[[0.0]], [[2.0]]])
    assert abs(bd.m2(fl, 1, 1)['overall'][0] - 10.0) < 1e-12
    assert abs(bd.m2(fl, 1, 2)['overall'][0] - 100 * (0.1 + 0.9) / 4) < 1e-12   # (1 x .1 + 3 x .3) / 4
    assert abs(bd.m2(fl, 1, 2, inlife=True)['overall'][0] - 100 * (0.1 + 0.1) / 2) < 1e-12   # year 2 in life: net 1 over 10


def test_d1_m2b_and_m2c_hand_cases():
    fl = flows([[[2.0], [1.0]]], [[[10.0], [10.0]]], [0.5, 0.5], ['D10', 'D10'], income=np.array([10.0, 4.0]), idx=np.array([[1.0]]), liq_share=np.array([0.5, 0.08]))
    b = bd.m2b(fl, 1, 1)['D10']
    assert abs(b['mean'][0] - 22.5) < 1e-12 and b['share_5'][0] == 100 and b['share_20'][0] == 50 and b['share_10'][0] == 100
    c = bd.m2c(fl, 1, 1)['D10']
    assert abs(c['mean'][0] - 82.5) < 1e-12 and c['share_50'][0] == 50 and c['share_100'][0] == 50 and c['share_25'][0] == 100
    nanl = flows([[[2.0], [1.0]]], [[[10.0], [10.0]]], [0.5, 0.5], ['D10', 'D10'], income=np.array([10.0, np.nan]), idx=np.array([[1.0]]))
    assert abs(bd.m2b(nanl, 1, 1)['D10']['mean'][0] - 20.0) < 1e-12   # a line with no income source is left out, never filled


# ---- D2: M3 gain-weighted -----------------------------------------------------------------------------------------------------------------------------
def test_d2_m3_gain_weighted_hand_case():
    fl = flows([[[1.0], [0.0]], [[0.0], [0.0]]], [[[1.0], [1.0]]] * 2, [0.5, 0.5], ['D10', 'D10'], delta=np.array([[[0.0], [0.0]], [[1.0], [-5.0]]]),
               payer0=np.array([True, True]))
    assert abs(bd.m3(fl, (3.0, 2.5, 2.25), G=2)[0] - 103.0) < 1e-12                       # PV(1 in year 1) / PV(1 in year 2) = 1.03; a loss is not a gain
    fl['payer0'] = np.array([True, False])
    assert abs(bd.m3(fl, (3.0, 2.5, 2.25), G=2)[0] - 103.0) < 1e-12                       # a non-payer is out of both sides (ratio unchanged here)
    fl['payer0'] = np.array([False, False])
    assert np.isnan(bd.m3(fl, (3.0, 2.5, 2.25), G=2)[0])


def test_d2_discount_schedule():
    d = bd.discount((3.0, 2.5, 2.25), 80)
    assert abs(d[0] - 1 / 1.03) < 1e-15 and abs(d[29] - 1.03 ** -30) < 1e-12 and abs(d[30] - 1.03 ** -30 / 1.025) < 1e-12 and abs(d[75] - d[74] / 1.0225) < 1e-12


def tiny_base(band='D10', w=1.0):
    return NS(adults_k=np.array([2.0]), wealth=np.array([w]), w_min=0.15, band=(band,), labels=('x',))


def test_d2_m3_today_hand_case(reg):
    rows = {**reg, 'I-M6i': NS(central=0.2, high=0.2), 'I-M6b': NS(central=0.15, high=0.15)}
    out = bd.m3_today(tiny_base(), np.full((2, 1), 0.1), 0.0, rows, (3.0, 3.0, 3.0), G=2)
    d1, d2, r = 1 / 1.03, 1 / 1.03 ** 2, 0.0035
    assert abs(out['D10'][0] - 100 * r * (d1 * 1.1 + d2 * 1.21) / (d1 * 0.1 + d2 * 0.11)) < 1e-12 and np.isnan(out['D6_7'][0])


def test_d2_m12_hand_case(pack, reg):
    rows = {**reg, 'I-T5f': NS(central=0.0, high=0.0), 'I-T5e': NS(central=0.0, high=0.0), 'I-T6m': NS(central=0.0, high=0.0)}
    out = bd.m12(tiny_base(), np.full((2, 1), 0.1), 0.0, rows, pack, (3.0, 3.0, 3.0), G=2)['D10']
    ex = next(r['value'] for r in pk.lookup(pack, 'wealth_distribution', variable='pension_share', band='D10')) / 100
    d1, d2 = 1 / 1.03, 1 / 1.03 ** 2
    acc = d1 * 0.1 + d2 * 0.11
    assert abs(out['exempt_law'][0] - 100 * ex) < 1e-9
    assert abs(out['deferral_uplift'][0] - 100 * (1 - ex) * d2 * 0.21 / acc) < 1e-9                  # nothing realised: the whole stock is forgiven at death
    full = bd.m12(tiny_base(), np.full((2, 1), 0.1), 0.0, {**rows, 'I-T5f': NS(central=1e6, high=1e6)}, pack, (3.0, 3.0, 3.0), G=2)['D10']
    assert abs(full['deferral_uplift'][0]) < 1e-12                                                   # everything realised each year (the cap binds)


# ---- D3: M4a by income decile --------------------------------------------------------------------------------------------------------------------------
def test_d3_m4_by_income_decile_hand_case():
    inc = np.array([np.full(10, 100.0), np.arange(1.0, 11.0)])
    out = bd.m4(np.array([[1, 0], [3, 2], [2, 2]]), np.array([2, 2, 2]), inc, np.full(10, 1000.0), np.full(10, 10000.0))   # path 0: the first tax; 1: the second; 2: both
    assert np.allclose(out['M4a']['D1'], [10.0, 0.1, 10.1], atol=1e-12, rtol=0) and np.allclose(out['M4a']['D10'], [10.0, 1.0, 11.0], atol=1e-12, rtol=0)
    assert np.allclose(out['M4b']['D3'], [1.0, 0.03, 1.03], atol=1e-12, rtol=0) and np.allclose(out['M4a']['overall'], [10.0, 0.55, 10.55], atol=1e-12, rtol=0)
    assert np.allclose(out['M4b']['overall'], [1.0, 0.055, 1.055], atol=1e-12, rtol=0) and np.allclose(out['saving_gbp'][2], inc.sum(0))


def test_d3_m4c_is_the_decile_saving_per_month():
    m4b = {d: np.array([float(i)]) for i, d in enumerate(bd.DECILES)}
    income = np.arange(1.0, 11.0) * 1200.0
    out = bd.m4c(m4b, income)
    assert abs(out['p25'][0] - 2 / 100 * income[2] / 12) < 1e-12 and abs(out['p90'][0] - 8 / 100 * income[8] / 12) < 1e-12


# ---- D4: DH1c equals the pack decile table ------------------------------------------------------------------------------------------------------------
ORDER, PARTS, PAYERS = ['iht', 'stamp_duties', 'cgt', 'business_rates', 'council_tax', 'corporation_tax'], {'stamp_duties': ['stamp_property', 'stamp_shares']}, ('cgt', 'iht')


def test_d4_dh1c_equals_the_pack_decile_table(pack):
    d = bd.dh1c(pack, ORDER, PARTS, PAYERS)
    for i, g in enumerate(bd.DECILES):
        row = lambda v: pk.lookup(pack, 'household_incidence', variable=v, group=g, tax=None)[0]['value']
        assert d['bill_gbp'][i] == row('total_tax') and d['income_gbp'][i] == row('gross_income')
    assert np.allclose(d['bill_pct_income'], 100 * d['bill_gbp'] / d['income_gbp'], atol=1e-12, rtol=0)


def test_d4_incidence_spreads_each_tax_to_its_pack_total_and_shares(pack):
    inc = bd.incidence(pack, ORDER, PARTS, PAYERS)
    gdp, hh = (pk.lookup(pack, 'wealth_distribution', variable=v, band='all')[0]['value'] for v in ('gdp', 'households'))
    pounds = lambda ls: sum(pk.lookup(pack, 'receipts', line=m)[0]['pct_gdp'] for m in ls) / 100 * gdp * 1e9 / (hh * 1e3)
    assert not inc[0].any() and not inc[2].any()                                                 # payers' taxes give the non-payers nothing
    for k, ls in ((1, PARTS['stamp_duties']), (3, ['business_rates']), (4, ['council_tax']), (5, ['corporation_tax'])):
        assert abs(inc[k].mean() - pounds(ls)) < 1e-6
    s10 = pk.lookup(pack, 'household_incidence', variable='tax_share_top_decile', group='D10', tax='council_tax')[0]['value'] / 100
    assert abs(inc[4][9] / inc[4].sum() - s10) < 1e-12


# ---- D5: M8 at the same revenue and the same people -----------------------------------------------------------------------------------------------------
def test_d5_m8_equals_the_revenue_at_the_same_people():
    w, a, band = np.array([0.1, 2.0, 4.0]), np.array([5.0, 1.0, 1.0]), ('D4-5', 'D6-7', 'D8-9')
    sh = {'flat': {'D4-5': 1.0, 'D6-7': 1.0, 'D8-9': 1.0}, 'half': {'D4-5': 0.1, 'D6-7': 0.5, 'D8-9': 0.25}}
    out = bd.m8(w, a, band, 0.15, np.array([0.6, 1.2]), sh)
    assert np.allclose(out['flat']['revenue_bn'], [0.6, 1.2], atol=1e-12, rtol=0)                  # the revenue of M1 exactly; the line below W_min pays nothing
    assert np.allclose(out['flat']['burden'], [10.0, 20.0], atol=1e-12, rtol=0)                    # tax is 10% (20%) of wealth on both payers
    assert np.allclose(out['half']['revenue_bn'], [0.6, 1.2], atol=1e-12, rtol=0)
    t = 0.6 * np.array([0.0, 1.0, 1.0]) / 2.0                                                        # shares x wealth: 1.0 and 1.0
    assert np.allclose(out['half']['burden'][0], 100 * ((t ** 2)[1:] / w[1:]).sum() / 0.6, atol=1e-12)
    with pytest.raises(bd.BurdenError):
        bd.m8(w, a, band, 0.15, 1.0, {'p': {'D4-5': np.nan, 'D6-7': 1.0, 'D8-9': 1.0}} | {'q': {'D4-5': 1.0}})


def test_d5_m8_shares_come_from_the_pack(pack):
    s = bd.reform_shares(pack)
    assert abs(s['property']['D10'] - 0.383) < 1e-12 and np.isnan(s['property']['D4-5'])
    assert abs(s['gains']['D10'] - 3181.0 / pk.lookup(pack, 'wealth_distribution', variable='wealth_total', band='D10')[0]['value']) < 1e-12


# ---- D6: the comparators read only the pack and the register --------------------------------------------------------------------------------------------
def rows(**kw):
    return {i: NS(central=v[0], low=v[0], high=v[-1]) for i, v in kw.items()}


def test_d6_comparators_read_only_register_values():
    r = rows(**{'I-M5a': (2,), 'I-M5b': (1,), 'I-M5g': (0.2,), 'I-M5d': (100,), 'I-M5h': (2,), 'I-M5i': (10,), 'I-M5k': (1, 2), 'I-M5l': (10, 1000), 'I-M5o': (5,), 'I-M5p': (500,)})
    out = bd.m5(np.array([0.3, 20.0, 50.0, 2000.0]), np.array([9.0, 1.0, 1.0, 1.0]), r, m2_wdt=0.5)
    assert abs(out['zucman'] - 1.8) < 1e-12 and abs(out['uk_minimum'] - 1.8) < 1e-12 and abs(out['once'] - 1.0) < 1e-12 and abs(out['zucman_diff'] - 1.3) < 1e-12
    t = np.array([0.0, 0.2, 0.8, 0.02 * 1990.0])                                                    # the marginal tax above 10 million (the largest line passes the second band)
    green = np.array([0.0, 0.01 * 10, 0.01 * 40, 0.01 * 990 + 0.02 * 1000])
    union = 0.02 * np.maximum(np.array([0.3, 20.0, 50.0, 2000.0]) - 10, 0)
    w = np.array([0.3, 20.0, 50.0, 2000.0])
    assert abs(out['union'] - 100 * (union ** 2 / w).sum() / union.sum()) < 1e-12 and abs(out['green'] - 100 * (green ** 2 / w).sum() / green.sum()) < 1e-12
    with pytest.raises(bd.BurdenError):
        bd.m5(w, np.ones(4), {})


def test_d6_m6_and_m11_are_register_rows(reg):
    m = bd.m6(reg)
    assert abs(m['D10']['total'] - (reg['I-M6i'].central + reg['I-M6b'].central)) < 1e-15 and m['overall']['gains'] == reg['I-M6h'].central
    assert bd.m11(reg) == reg['I-T1d'].central
    with pytest.raises(bd.BurdenError):
        bd.m11({})


# ---- the kernel run, reconciled with revenue --------------------------------------------------------------------------------------------------------------
@pytest.fixture(scope='module')
def run(pack, reg):
    b = bs.build_base(pack, reg, 0.5)
    rate = sc.rate_function(1.0, 0.04, 0.9, b.w_min, 'logistic_ln')
    rng = np.random.default_rng(7)
    g, gg, c = rng.normal(0.047, 0.08, (40, 6)), rng.normal(0.015, 0.02, (40, 6)), reg['I-D14c'].central / 100
    return b, rv.run_lines(b, rate, g, gg, c, n_phase=3), bd.line_flows(b, rate, g, gg, c, n_phase=3), g, c


def test_line_flows_reconcile_with_the_revenue_aggregate(run):
    b, agg, fl, g, c = run
    total = (fl['net'] * fl['wt'][None, :, None]).sum(1) * fl['adults_k']
    ref = agg['tax'] + agg['refund'] + agg['death_tax'] + agg['heir'] + agg['death_B'] + agg['death_D']
    assert np.abs(total - ref).max() < 1e-9 and fl['net'].shape == (40, 14 * 3, 6) and abs(fl['wt'].sum() - 1) < 1e-12 and (fl['death'] != 0).any()


def test_burden_metrics_on_a_run_are_finite_and_ordered(run, reg, pack):
    b, _, fl, g, c = run
    m = bd.m2(fl, 1, 20)
    assert np.isfinite(m['overall']).all() and (m['overall'] > 0).all() and (m['D10'] >= m['D6_7']).all()
    assert (bd.m2(fl, 1, 20, inlife=True)['overall'] <= m['overall'] + 1e-12).all()
    assert np.isfinite(bd.m2b(fl, 1, 20)['overall']['mean']).all() and np.isfinite(bd.m2c(fl, 1, 20)['D10']['share_25']).all()
    rates = [reg[i].central for i in bd.IDS['disc']]
    assert np.isfinite(bd.m3(fl, rates)).all() and (bd.m3(fl, rates) > 0).all()
    e = bd.m12(b, g, c, reg, pack, rates)
    assert all(0 < e[k]['exempt_law'][0] < 100 and e[k]['deferral_uplift'][0] >= 0 for k in ('overall', 'D10'))
    assert np.isfinite(bd.m3_today(b, g, c, reg, rates)['overall']).all()
