"""V3-9 supporting-metric tests U1 to U6 (architecture.md 6.2) and the pieces behind them. Money is pounds m unless a name says _bn."""
import ast
import pathlib

import numpy as np
import pytest

from model_v3.core import kernel as K
from model_v3.core import schedule as S
from model_v3.core import support as U

FLAT = lambda x: np.full(np.shape(x), 0.1)
RATE = S.rate_function(k=1.0, tau_0=0.04, tau_m=0.5, W_min=0.5, form='logistic_ln')


def test_U1_c1_uses_tw_at_alpha_one_as_the_denominator():
    alphas = np.array([0.5, 1.0, 2.0])
    runs = {'net': np.array([[8.0], [5.0], [2.0]]), 'refunds': np.array([[0.0], [1.0], [4.0]]), 'tw': np.array([[90.0], [100.0], [50.0]])}
    c1, lost = U.declaration_curve(runs, alphas)
    assert c1[:, 0].tolist() == pytest.approx([3.0, 0.0, -3.0])          # TW(0.5) = 90 and TW(2) = 50 play no part
    assert lost[:, 0].tolist() == pytest.approx([1.0, 0.0, -3.0])
    with pytest.raises(ValueError):
        U.declaration_curve(runs, np.array([0.5, 1.5, 2.0]))


def test_U1_hand_case_on_the_kernel_path():
    # V0 = 100, flat 10%, one holding year at +50%, a sale year at 0%. alpha 1.2: pays 6, the sale refunds 2.9 -> net 3.1.
    # alpha 1: pays 5 and nothing after -> net 5, TW(1) = 145.
    g = np.array([[0.5], [0.0]])
    alphas = np.array([1.0, 1.2])
    runs = U.declaration_runs(FLAT, g, 100.0, alphas)
    assert runs['net'][:, 0].tolist() == pytest.approx([5.0, 3.1], abs=1e-12) and runs['tw'][0, 0] == pytest.approx(145.0)
    c1, lost = U.declaration_curve(runs, alphas)
    assert c1[0, 0] == 0.0 and c1[1, 0] == pytest.approx(100 * (3.1 - 5.0) / 145.0, abs=1e-12)
    assert lost[1, 0] == pytest.approx(-100 * 2.9 / 145.0, abs=1e-12)


def test_tolerant_zone_and_modal_alpha():
    al = np.array([0.5, 0.8, 1.0, 1.5, 2.0])
    c1 = np.array([[-5.0], [-1.0], [0.0], [1.0], [3.0]])
    lo, hi = U.tolerant_zone(al, c1)
    assert lo[0] == pytest.approx(0.725) and hi[0] == pytest.approx(1.75)
    lo, hi = U.tolerant_zone(al, np.zeros((5, 1)))                       # never leaves the zone: the edges are the grid's
    assert (lo[0], hi[0]) == (0.5, 2.0)
    assert U.modal_alpha(al, [0.1, 0.4, 0.4, 0.05, 0.05]) == 0.8          # a tie goes to the lower alpha
    assert U.modal_alpha(al, np.array([[0, 1], [0, 0], [0, 0], [1, 0], [0, 0]]))[:].tolist() == [1.5, 0.5]


def test_U2_crra_certainty_equivalent_hand_case():
    assert U.crra_ce([50.0, 200.0], 2.0) == pytest.approx(80.0)          # 1 / mean(1 / w)
    assert U.crra_ce([50.0, 200.0], 1.0) == pytest.approx(100.0)         # exp(mean(ln w)): log utility
    assert U.cew_bp([[50.0, 200.0]], [[100.0, 400.0]], 2.0)[0] == pytest.approx(-5000.0)
    assert U.cew_bp([[50.0, 200.0]], [[50.0, 200.0]], 1.5)[0] == 0.0
    with pytest.raises(ValueError):
        U.crra_ce([1.0, -1.0], 2.0)


def test_comparator_systems_hand_cases():
    g, w0 = np.array([[0.1], [0.1]]), [10.0]
    w, paid = U.system_run('stock_wealth_tax', 0.01, g, w0, 1.0)
    assert (w[0, 0], paid[0, 0]) == pytest.approx((10.9 * 1.1 - 0.109, 0.209))
    w, paid = U.system_run('income_tax_gains', 0.5, g, w0, 1.0)
    assert (w[0, 0], paid[0, 0]) == pytest.approx((11.025, 1.025))
    w, paid = U.system_run('consumption_tax', 0.5, g[:1], w0, 1.0, c=0.1)
    assert (w[0, 0], paid[0, 0]) == pytest.approx((9.35, 0.55))
    assert U.system_run('stock_wealth_tax', 0.5, g, [0.5], 1.0)[1][0, 0] == 0.0     # under the threshold: no tax
    with pytest.raises(ValueError):
        U.system_run('poll_tax', 0.1, g, w0, 1.0)


def test_welfare_at_equal_revenue():
    rng = np.random.default_rng(3)
    g = rng.normal(0.045, 0.1, size=(30, 400))
    V0 = {'A': np.array([0.02, 2.0, 20.0]), 'C': np.array([0.0, 1.0, 5.0])}
    w, gamma, w_min, c = np.array([0.5, 0.3, 0.2]), 1.5, 0.5, 0.02
    out, rates = U.welfare(RATE, g, V0, w, gamma, w_min, c)
    assert set(out) == {'wdt', *U.SYSTEMS} and set(rates) == set(U.SYSTEMS)
    for k, v in out.items():
        assert v[0] == pytest.approx(0.0, abs=1e-6) and np.all(v[1:] < 0.0), k   # the line under w_min pays nothing; payers lose
    w0 = V0['A'] + V0['C']
    pw = w * (w0 >= w_min)
    target = float((pw[:, None] * U.wdt_run(RATE, g, V0, c)[1]).sum(0).mean())
    for kind, r in rates.items():
        got = float((pw[:, None] * U.system_run(kind, r, g, w0, w_min, c)[1]).sum(0).mean())
        assert got == pytest.approx(target, rel=1e-9), kind                     # revenue equivalence
    assert U.solve_rate('stock_wealth_tax', float((pw[:, None] * U.system_run('stock_wealth_tax', 0.02, g, w0, w_min)[1]).sum(0).mean()),
                        g, w0, pw, w_min) == pytest.approx(0.02, abs=1e-9)
    with pytest.raises(ValueError):
        U.solve_rate('stock_wealth_tax', 1e9, g, w0, pw, w_min)
    assert U.wmean(out['wdt'][1:], w[1:]) == pytest.approx((out['wdt'][1] * 0.3 + out['wdt'][2] * 0.2) / 0.5)


def test_U3_envelope_binding_agrees_with_the_kernels_lost_refund():
    g = np.array([[0.5, 0.5, 0.0], [-0.5, -0.1, -0.1]])
    b, Ls, lost = K.Book(3, {'A': 100.0}), [], []
    for gt in g:
        Ls.append(dict(K.step_year(b, FLAT, 1.0, gt, 0.0))['tax'].L)
        lost.append(b.lost_refund.copy())
    e = U.envelope(np.array(Ls), np.array(lost), weights=[1.0, 1.0, 2.0])
    assert e['forgone'] == pytest.approx(b.lost_refund, abs=1e-12)
    assert e['binds'].tolist() == [True, False, True] and e['first'][[0, 2]].tolist() == [2.0, 2.0] and np.isnan(e['first'][1])
    assert e['forgone_t'][0].tolist() == [0.0, 0.0, 0.0] and e['share_binding'] == pytest.approx(3.0 / 4.0)
    assert e['forgone'][2] == pytest.approx(1.0)               # line 2 paid nothing, so its whole refund of 0.1 x 10 is held back
    assert e['forgone_share'] == pytest.approx((e['forgone'] * [1, 1, 2]).sum() / (e['due'] * [1, 1, 2]).sum())
    # line 0 by hand: paid 5 at V = 150, then V = 75 and the state's stake is worth 2.5; the due refund is 0.1 x 72.5 = 7.25
    assert b.lost_refund[0] == pytest.approx(7.25 - 2.5, abs=1e-12) and e['due'][0] == pytest.approx(7.25, abs=1e-12)
    never = U.envelope(np.array([[1.0], [-1.0]]), np.zeros((2, 1)))
    assert not never['binds'][0] and np.isnan(never['first'][0]) and never['share_binding'] == 0.0


def test_liquidity_timing_of_the_cap():
    assert U.liquidity_timing([[1.0], [3.0], [9.0]], [[100.0], [100.0], [100.0]], 2)[0] == pytest.approx(2.0)


def test_U4_migration_m9_equals_m1_minus_x():
    m1, payers, gdp = np.full((2, 1), 1.5), np.full((2, 1), 1000.0), np.full((2, 1), 1000.0)
    r = U.migration_effect(m1, payers, gdp, np.array([[1.0], [2.0]]), 0.1, 100000.0, 0.4)
    assert r['X'][:, 0].tolist() == pytest.approx([0.4, 0.8])             # 100,000 leavers x 100,000 x 0.4 = 4bn on 1,000bn
    assert np.array_equal(r['M9'], r['M1'] - r['X']) and r['M1'][0, 0] == 1.5
    r2 = U.migration_effect(m1, payers, gdp, np.ones((2, 1)), 0.1, 100000.0, 0.4, spend=50000.0, rate_spend=0.2)
    assert r2['X'][0, 0] == pytest.approx(0.4 + 0.1)
    assert U.migration_effect(m1, payers, gdp, np.ones((2, 1)), 0.0, 1.0, 1.0)['M9'].tolist() == m1.tolist()   # nobody leaves


def test_lockin_hand_cases():
    gA, gB = [[1.0]], [[1.05]]                    # GA = 2, GB = 2.05; rate 0.2, half the value is gain
    cost, locked = U.lockin(gA, gB, 0.2, 0.5, 1, 1.5)
    assert locked == 1.0 and cost == pytest.approx(1e4 * (1.7 - 1.74) / 2.05)   # stay 1.7, taxed switch 1.656, neutral switch 1.74
    cost, locked = U.lockin([[0.0]], [[0.5]], 0.2, 0.5, 1, 1.5)               # both switch: the taxed one still loses what it paid
    assert locked == 0.0 and cost == pytest.approx(1e4 * (1.26 - 1.3) / 1.5)


def test_U6_lockin_is_zero_when_the_gains_tax_is_neutral():
    rng = np.random.default_rng(6)
    gA, gB = rng.normal(0.05, 0.12, (20, 500)), rng.normal(0.05, 0.12, (20, 500))
    assert U.lockin(gA, gB, 0.0, 0.5, 20, 2.0) == (0.0, 0.0)                  # no tax
    assert U.lockin(gA, gB, 0.3, 0.0, 20, 2.0) == (0.0, 0.0)                  # no embedded gain: switching realises nothing
    cost, locked = U.lockin(gA, gB, 0.3, 0.75, 20, 2.0)
    assert cost < 0.0 and 0.0 < locked < 1.0                                  # and it is not zero otherwise


def test_U5_s1_off_equals_s1_absent():
    wealth, share, adults = np.array([1.0, 2.0, 3.0]), np.array([0.5, 0.5, 0.5]), np.array([10.0, 20.0, 30.0])
    off = U.capitalise(wealth, share, 0.2, on=False)
    assert np.array_equal(off, wealth) and off is not wealth
    assert U.payer_count(off, adults, 2.1) == U.payer_count(wealth, adults, 2.1) == 30.0
    on = U.capitalise(wealth, share, 0.2, on=True)
    assert on.tolist() == pytest.approx([1.1, 2.2, 3.3]) and U.payer_count(on, adults, 2.1) == 50.0
    eff = U.s1_effect({'m1': 1.7, 'payer_count': U.payer_count(on, adults, 2.1)}, {'m1': 1.5, 'payer_count': 30.0})
    assert eff['m1'] == pytest.approx(0.2) and eff['payer_count'] == 20.0
    assert all(np.all(v == 0.0) for v in U.s1_effect({'m1': 1.5}, {'m1': 1.5}).values())
    assert U.payer_count(np.array([[1.0, 3.0], [3.0, 3.0]]), [10.0, 20.0], 2.0).tolist() == [20.0, 30.0]


def test_support_imports_numpy_and_kernel_only():
    tree = ast.parse(pathlib.Path(U.__file__).read_text())
    mods = {a.name for n in ast.walk(tree) if isinstance(n, ast.Import) for a in n.names}
    mods |= {n.module for n in ast.walk(tree) if isinstance(n, ast.ImportFrom)}
    assert mods <= {'numpy', '__future__', 'model_v3.core'} and 'burden' not in pathlib.Path(U.__file__).read_text().split('"""')[2]
