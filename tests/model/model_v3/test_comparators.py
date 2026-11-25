"""Brief 126c, block 1: the household arm's untaxed path (design 3.6 site 4) under free_path, M3-today and M12; the legacy path does not move."""
import json
from dataclasses import replace
from types import SimpleNamespace

import numpy as np

from model_v3.core import burden as bd, kernel as K
from model_v3.runner import arm as ab, out_support as osup, runner as R
from test_runner import ROOT, ctx, lv, out, tier1  # noqa: F401  (the fixtures)

INP = json.loads((ROOT / 'docs' / 'model-v3' / 'cell-baseline' / 'inputs_used.json').read_text())
TOY = dict(pos=dict(property=np.array([1.0]), net_financial=np.array([0.5]), physical=np.array([0.0]), pension=np.array([0.5])), income=np.array([0.1]), sav=np.array([0.1]), acc=np.array([0.05]))
GAIN = dict(property=0.02, net_financial=0.01, physical=0.0, pension=0.01)


def test_the_household_free_path_is_the_account_with_no_tax_by_hand_and_by_the_kernel():
    h, g = ab.HouseholdHook(TOY, GAIN, 0.0), np.zeros((3, 2))
    f = h.free(g)
    assert f.shape == (3, 1, 2) and np.allclose(f[0], (2.0 + 0.015 + 0.03) / 2.0, atol=1e-15)     # W0 2, saving 0.1 x (0.05 + 0.1), gains 0.02 + 0.005 + 0.005
    book, hk, W0 = K.Book(1, {'A': np.array([1.5]), 'B': np.array([0.0]), 'D': np.array([0.0])}), ab.HouseholdHook(TOY, GAIN, 0.0), 2.0
    for t in range(1, 4):                                                                          # the same years through the kernel at a zero rate
        K.step_year(book, lambda w: 0.0 * w, 1.0, np.zeros(1), 0.0, hook=hk, t=t)
        assert np.allclose(np.cumprod(f[:, 0, 0])[t - 1] * 2.0, hk.W_after[0], atol=1e-12)


def test_the_burden_on_the_household_path_is_the_toy_rate_by_hand_and_the_legacy_path_is_bit_equal():
    base = SimpleNamespace(wealth=np.array([2.0]), w_min=0.0, adults_k=np.array([1.0]), band=np.array(['D10']))
    W = bd.free_path(base, np.zeros((2, 1)), None, G=2, hook=ab.HouseholdHook(TOY, GAIN, 0.0))
    d1 = 2.0 * 0.0225
    assert W.shape == (3, 1, 1) and np.isclose(W[1, 0, 0] - W[0, 0, 0], d1, atol=1e-12)
    out = bd._pooled(base, W, 2, (0.0, 0.0, 0.0), lambda x: 0.01 * x)                              # a tax of 1% of wealth on the path, no discounting
    assert np.isclose(out['D10'][0], 100 * 0.01 * (W[1, 0, 0] + W[2, 0, 0]) / (W[2, 0, 0] - W[0, 0, 0]), atol=1e-9) if 'D10' in out else True
    g, c = np.array([[0.02], [0.03]]), 0.1
    old = np.concatenate([np.ones((1, 1, 1)), np.cumprod((1.0 + g) * (1.0 - c), axis=0)[:, None, :]]) * base.wealth[None, :, None]
    assert np.array_equal(bd.free_path(base, g, c), old) and np.array_equal(bd.free_path(base, g, c, hook=ab.LegacyHook(c)), old)


def test_m3_and_m12_come_back_under_the_household_arm_without_reading_the_legacy_c(ctx):
    c2 = replace(ctx, arm=dict(arm='household', inputs=INP, saving='median'), once=frozenset({'OH1b', 'OH1c'}))
    th = {**c2.centre, 'I-D14c': np.nan}                                                           # a read of the legacy c would give nan
    st = R.statics(c2, th)['burden']
    assert set(st) == {'OH1b', 'OH1c'}
    vals = [np.asarray(v, float) for cells in st.values() for v in cells.values()]
    assert vals and sum(np.isfinite(v).any() for v in vals) > len(vals) // 2                        # most cells hold numbers (a band with no payer is nan)
    legacy = R.statics(replace(ctx, once=c2.once), th)['burden']
    assert not any(np.isfinite(np.asarray(v, float)).any() for cells in legacy.values() for v in cells.values())   # the legacy arm does read it: the same nan gives nan


# ── block 2: the comparators on the account (M13) ─────────────────────────────────────────────────────────────────────────────────────
from model_v3.core import support as U  # noqa: E402

G1, ONE = np.zeros((1, 2)), np.array([2.0])


def test_each_comparator_on_the_toy_account_equals_the_hand_calculation():
    h = ab.HouseholdHook(TOY, GAIN, 0.0)
    run = lambda kind, r, payer=True: [np.asarray(x)[0, 0] for x in U.system_run(kind, r, G1, ONE, 0.0, hook=h) ] if payer else [np.asarray(x)[0, 0] for x in U.system_run(kind, r, G1, ONE, 5.0, hook=h)]
    # year 1: opening 2.0 (property 1, net financial 0.5, pension 0.5), saving 0.015 (0.01 outside the pension), gains 0.03, consumption 0.09; wealth with no tax 2.045
    assert np.allclose(run('none', 0.0), (2.045, 0.0), atol=1e-12)
    assert np.allclose(run('stock_wealth_tax', 0.1), (2.045 - 0.2, 0.2), atol=1e-12)                # 10% of the opening stock, pension included
    assert np.allclose(run('income_tax_gains', 0.5), (2.045 - 0.015, 0.015), atol=1e-12)           # 50% of the holding gain
    assert np.allclose(run('consumption_tax', 0.5), (2.045 - 0.045, 0.045), atol=1e-12)            # 50% of consumption
    assert np.allclose(run('stock_wealth_tax', 0.1, payer=False), (2.045, 0.0), atol=1e-12)        # a line under the threshold pays nothing
    assert np.allclose(run('stock_wealth_tax', 1.0), (0.51, 1.535), atol=1e-12)                    # 2.0 owed, 1.535 outside the pension: the pension is never sold and the rest is not paid


def test_the_comparators_raise_the_same_revenue_as_the_wdt_line_on_the_account():
    h, rate = ab.HouseholdHook(TOY, GAIN, 0.0), (lambda w: 0.05 + 0.0 * w)
    V0 = {'A': ONE}
    cew, rates = U.welfare(rate, G1, V0, [1.0], 2.0, 0.0, 0.0, hook=ab.HouseholdHook(TOY, GAIN, 0.0))
    w, tax = U.wdt_run(rate, G1, V0, 0.0, ab.HouseholdHook(TOY, GAIN, 0.0))
    assert tax[0, 0] > 0 and np.isclose(w[0, 0], 2.045 - tax[0, 0], atol=1e-12)                    # the WDT line: terminal wealth is units plus pension
    for kind in U.SYSTEMS:
        assert np.isclose(U.system_run(kind, rates[kind], G1, ONE, 0.0, hook=h)[1][0, 0], tax[0, 0], atol=1e-9) and np.isfinite(cew[kind]).all()
    assert np.isclose(rates['income_tax_gains'], tax[0, 0] / 0.03, atol=1e-9)


def test_welfare_and_the_legacy_systems_are_bit_equal_without_a_hook():
    g, w0 = np.array([[0.02, 0.03], [0.01, -0.02]]), np.array([1.0, 2.0])
    new, old = U.system_run('income_tax_gains', 0.3, g, w0, 0.0, 0.1), U.system_run('income_tax_gains', 0.3, g, w0, 0.0, c=0.1, hook=None)
    assert all(np.array_equal(a, b) for a, b in zip(new, old))


def test_the_household_arm_produces_m13_without_reading_the_legacy_c(ctx):
    c2 = replace(ctx, arm=dict(arm='household', inputs=INP, saving='median'))
    th = {**c2.centre, 'I-D14c': np.nan}
    ev = {'S': R.evaluate(c2, th, dict(tau_0=0.04, tau_m=0.7, k_ln=1, ratio=0.5), np.full((100, 2), 0.01), np.full((100, 2), 0.0157))}
    smp = R.samples(ev, c2.ids, c2.once, R.statics(c2, th))
    assert smp['OW1'] and all(np.isfinite(v).all() for k, v in smp['OW1'].items() if ('wealth_band', 'overall') in k[2]) and {k[2] for k in smp['OW1']} >= {(('tax_system', 'wdt'), ('wealth_band', 'overall'))}     # a band with no payer is nan
    assert all(np.isfinite(v).any() for v in smp['O1'].values())                                          # M13 produced, the headline finite with the legacy c = nan


# ── block 3: M15 (the envelope) and M9 (the migration's spend) on the account ───────────────────────────────────────────────

def _envelope_case(gain, years=4):
    """One taxed line of 15 non-pension wealth (+1 pension), no income, no saving, a flat 5% rate on the change, 0 paid before: the kernel rerun under the household hook (`out_support._record`)."""
    toy = dict(pos=dict(property=np.array([10.0]), net_financial=np.array([5.0]), physical=np.array([0.0]), pension=np.array([1.0])), income=np.array([0.0]), sav=np.array([0.0]), acc=np.array([0.0]))
    g = dict(property=gain, net_financial=gain, physical=0.0, pension=0.0)
    base = SimpleNamespace(V0={r: np.array([v]) for r, v in dict(A=15.0, B=0.0, C=0.0, D=0.0).items()}, labels=['x'], G=30)
    raw = SimpleNamespace(base=base, g=np.zeros((years, 1)), gdp_g=np.zeros((years, 1)), rate=lambda w: 0.05 * np.ones_like(np.asarray(w, float)), c=np.nan, arm=dict(arm='household'))
    env = SimpleNamespace(lam=dict(lam_C=0.0, lam_D=0.0), arm=lambda b: SimpleNamespace(make=lambda: ab.HouseholdHook(toy, g, 0.0)))
    return osup._record(raw, env).reshape(years)


def test_the_envelope_on_the_account_equals_the_refund_the_cap_holds_back_by_hand():
    # wealth 15 falls 20% a year (the pension is outside the base): refunds due are 5% of 3.0, 2.4, 1.92, 1.536 and nothing was paid, so the cap holds back all of each
    assert np.allclose(_envelope_case(-0.2), [0.15, 0.12, 0.096, 0.0768], rtol=1e-12, atol=0)
    assert not _envelope_case(0.1).any()                                                              # a rising line is owed no refund: the envelope never binds
    assert np.isnan(_envelope_case(-0.2)).sum() == 0                                                  # the legacy c (nan here) is not read


def test_the_migration_spend_is_the_accounts_consumption_by_hand_and_the_legacy_one_is_the_share_of_wealth():
    toy = dict(TOY, income=np.array([0.1]), sav=np.array([0.1]))
    assert np.allclose(ab.HouseholdHook(toy, GAIN, 0.0).consumption(), [0.09])                      # C = (1 - saving) x income = 0.09 million a year
    base = SimpleNamespace(wealth=np.array([2.0]), weights=np.array([1.0]), w_min=0.0)
    ones = np.ones((3, 1))
    raw = lambda arm: SimpleNamespace(base=base, r=dict(M1=0.5 * ones, gdp=100.0 * ones), arm=dict(arm=arm), c=0.035 if arm == 'legacy' else np.nan, ok=np.array([True]), lo=dict.fromkeys(('transition', 'short', 'long'), np.array([1])), hi=dict.fromkeys(('transition', 'short', 'long'), np.array([3])))
    env = SimpleNamespace(ctx=None, theta={'I-D5c': 10.0, 'I-D9d': 50000.0, 'I-M6l': 20.0, 'I-T3q': 20.0}, arm=lambda b: SimpleNamespace(make=lambda: ab.HouseholdHook(toy, GAIN, 0.0)))
    again = lambda o, full: SimpleNamespace(run=dict(payers=1000.0 * ones, gdp_index=ones))
    # 10% of 1000 thousand payers = 100,000 leavers; each loses 20% of 50,000 income plus 20% of the spend; X is a percent of 100bn GDP
    acct = osup._migration(raw('household'), env, again)
    assert np.allclose(acct['X']['long'], 100.0 * 1e5 * (50000 * 0.2 + 90000 * 0.2) / 1e9 / 100.0) and np.allclose(acct['M9']['long'], 0.5 - acct['X']['long'])
    old = osup._migration(raw('legacy'), env, again)                                                  # legacy: the spend is 3.5% of the payers' mean wealth of 2.0 million = 70,000
    assert np.allclose(old['X']['long'], 100.0 * 1e5 * (50000 * 0.2 + 70000 * 0.2) / 1e9 / 100.0)


def test_the_household_arm_produces_m15_and_m9_without_reading_the_legacy_c(ctx):
    c2 = replace(ctx, arm=dict(arm='household', inputs=INP, saving='median'))
    th = {**c2.centre, 'I-D14c': np.nan}
    ev = {'S': R.evaluate(c2, th, dict(tau_0=0.04, tau_m=0.7, k_ln=1, ratio=0.5), np.full((100, 2), 0.01), np.full((100, 2), 0.0157))}
    smp = R.samples(ev, c2.ids, c2.once, R.statics(c2, th))
    assert smp['OW3'] and smp['OM1'] and {k[3] for k in smp['OM1']} == {'M1', 'X', 'M9'} and {k[3] for k in smp['OW3']} == {'M15a', 'M15b'}
    assert all(np.isfinite(v).any() for k, v in smp['OM1'].items() if k[3] == 'X') and all(np.isfinite(np.asarray(v, float)).any() for k, v in smp['OW3'].items() if k[3] == 'M15b' and ('wealth_band', 'overall') in k[2])
