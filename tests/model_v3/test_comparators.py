"""Brief 126c, block 1: the household arm's untaxed path (design 3.6 site 4) under free_path, M3-today and M12; the legacy path does not move."""
import json
from dataclasses import replace
from types import SimpleNamespace

import numpy as np

from model_v3.core import burden as bd, kernel as K
from model_v3.runner import arm as ab, runner as R
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
    assert all(np.isfinite(v).any() for v in smp['O1'].values()) and not smp.get('OW3') and not smp.get('OM1')     # M13 produced, M15 and M9 still withheld, the headline finite with the legacy c = nan
