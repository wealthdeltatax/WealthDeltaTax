"""V3-4 kernel tests K1 to K10 (architecture.md 6.2). Self-contained: no conftest needed.
Money is pounds m; "to the pound" is 1e-6."""
import ast
import itertools
import pathlib
import sys

import numpy as np
import pytest

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2]))
from model_v3.core import kernel as K  # noqa: E402
from model_v3.core import schedule as S  # noqa: E402

FLAT = lambda x: np.full(np.shape(x), 0.1)
LOGI = S.rate_function(k=0.001, tau_0=0.15, tau_m=0.70, W_min=2.0)   # VAL figure 5 canonical schedule
POUND = 1e-6


def year(book, g, rate_fn=FLAT, cons=0.0, **kw):
    ops = K.step_year(book, rate_fn, 1.0, g, cons, **kw)
    return dict(ops)['tax']


def test_K1_one_line_hand_case_each_route():
    # V0 = 100, g = +50%, flat 10%: delta 50, tax 5 on every route
    for route, mode in (('A', 'sale'), ('B', 'sale')):
        b = K.Book(1, {route: 100.0}, b_mode=mode)
        fl = year(b, 0.5)
        assert fl.L[0] == pytest.approx(5.0, abs=1e-12)
        assert b.R[route]['s'][0] == pytest.approx(5.0 / 150.0, abs=1e-15)      # units sold at the true price
        assert b.E_cash[0] == pytest.approx(5.0) and b.state_true()[0] == pytest.approx(5.0)
        assert b.family_true()[0] == pytest.approx(145.0)
    # C: alpha 1.2 -> declared 120 -> 180; delta 60, tax 6 paid in kind at the declared price 180 per 150
    b = K.Book(1, {'C': 100.0}, alpha0={'C': 1.2})
    fl = year(b, 0.5, alpha_C=1.2)
    assert fl.L[0] == pytest.approx(6.0) and fl.credited['C'][0] == pytest.approx(6.0)
    assert b.R['C']['s'][0] == pytest.approx(6.0 / 180.0)                       # units = tax / declared price
    assert fl.value['C'][0] == pytest.approx(5.0) and b.EC[0] == pytest.approx(5.0)   # worth 5 at the true price
    # D: liability accrues, no unit moves until settlement
    b = K.Book(1, {'D': 100.0})
    year(b, 0.5)
    assert b.A_D[0] == pytest.approx(5.0) and b.R['D']['s'][0] == 0.0
    fl = K.settle_D(b)
    assert fl.value['D'][0] == pytest.approx(5.0) and b.A_D[0] == 0.0 and b.E_cash[0] == pytest.approx(5.0)


def test_K2_loss_is_refunded_at_tau_times_loss():
    b = K.Book(1, {'A': 100.0})
    year(b, 0.5)                          # tax 5
    fl = year(b, -0.2)                    # family holds 145 after paying 5; 145 -> 116: loss 29 (v2 would refund 2.32)
    assert fl.delta[0] == pytest.approx(-29.0)
    assert fl.L[0] == pytest.approx(-2.9, abs=1e-12)
    assert fl.credited['A'][0] == pytest.approx(-2.9) and b.refunded[0] == pytest.approx(2.9)
    assert b.E_cash[0] == pytest.approx(2.1) and b.lost_refund[0] == 0.0


def test_K3_cap_refund_equals_cumulative_tax_paid_and_a_pound_over_is_held_back():
    def run(loss_value):
        b = K.Book(1, {'A': 100.0})
        year(b, 0.5)                      # paid 5.0 at V = 150
        year(b, 0.0, cons=loss_value / 145.0)   # consuming units is a fall in declared wealth at constant V
        return b
    b = run(50.0)                         # refund 0.1 x 50 = 5 = everything paid
    assert b.paid[0] == pytest.approx(5.0, abs=POUND) and b.refunded[0] == pytest.approx(5.0, abs=POUND)
    assert b.lost_refund[0] == pytest.approx(0.0, abs=POUND) and b.E_cash[0] == pytest.approx(0.0, abs=POUND)
    over = 10.0 * POUND                   # a loss worth one pound more of refund: 1e-6 / 0.1
    b = run(50.0 + over)
    assert b.refunded[0] == pytest.approx(b.paid[0], abs=1e-9)                  # still capped at what was paid
    assert b.lost_refund[0] == pytest.approx(POUND, abs=1e-9)                   # the extra pound is held back


def test_K4_envelope_resets_at_death_and_the_heir_is_taxed_from_zero():
    b = K.Book(1, {'A': 100.0, 'C': 100.0}, has_cv=True)
    for g in (0.3, 0.2):
        year(b, g)
    assert b.E_cash[0] > 0 and b.EC[0] > 0 and b.uo['C'][0] > 0
    paid_before = b.paid[0]
    ops = dict(K.step_death(b, FLAT, 1.0, death_verify=True))
    heir = ops['tax_heir']                # the heir's own first tax is the only thing in the new envelopes
    assert b.E_cash[0] == pytest.approx(heir.credited['A'][0]) and b.EC[0] == pytest.approx(heir.value['Cv'][0])
    assert b.uo['C'][0] == pytest.approx(0.0) and b.uo['Cv'][0] == pytest.approx(heir.units['Cv'][0])
    assert b.inc_paid[0] == 0.0
    assert b.paid[0] > paid_before                                              # lifetime record is kept
    assert heir.L[0] == pytest.approx(0.1 * heir.delta[0])
    assert heir.delta[0] == pytest.approx(b.family_true()[0] + heir.L[0])         # all of it is new to the heir
    with pytest.raises(TypeError):
        K.step_death(b, FLAT, 1.0, heir_influx='fresh_entrant')                 # the rule is dropped
    assert not hasattr(K, 'HEIR_RULES')


def test_K5_lien_recursion():
    b = K.Book(1, {'B': 100.0}, b_mode='lien', r_def=0.02)
    year(b, 0.5)
    assert b.LB[0] == pytest.approx(5.0) and b.R['B']['s'][0] == 0.0            # no unit moves under a lien
    year(b, 0.0)                          # LB accrues to 5.1; net-of-lien wealth falls 0.1; refund 0.01 cancels debt
    assert b.LB[0] == pytest.approx(5.09, abs=1e-12)
    year(b, 0.0)                          # LB = 5.09 x 1.02 = 5.1918; net wealth falls 0.1018; refund 0.01018
    assert b.LB[0] == pytest.approx(5.1918 - 0.01018, abs=1e-12)
    for LB_prev, LB_now in ((5.0, 5.09), (5.09, 5.1918 - 0.01018)):             # LB_t = LB_{t-1}(1+r) + L_t
        assert LB_now == pytest.approx(LB_prev * 1.02 - 0.1 * (LB_prev * 1.02 - LB_prev), abs=1e-12)
    fl = K.settle_B(b)                                                          # sale at the horizon
    assert b.LB[0] == 0.0 and fl.credited['B'][0] == pytest.approx(5.18162, abs=1e-9)


def mixed_lines(n, T, seed, b_mode='sale', **kw):
    """A heterogeneous batch: every route, per-line shares and declaration ratios, per-line growth and consumption."""
    rng = np.random.default_rng(seed)
    sh = rng.dirichlet([2, 2, 2, 2], size=n) + 0.05
    V0 = {r: 50.0 * sh[:, i] for i, r in enumerate('ABCD')}
    g = rng.normal(0.045, 0.12, size=(T, n))
    args = dict(V0=V0, g_mat=g, G=11, alpha_C=rng.uniform(0.6, 1.8, n), alpha_D=rng.uniform(0.6, 1.8, n),
                lam_C=0.08, lam_D=0.05, death_verify=True, reset_years=(7, 19), consumption=rng.uniform(0, 0.02, n),
                index_rate=0.01, b_mode=b_mode, c_cap='units_and_value', r_def=0.02,
                inc_allow=rng.uniform(0, 0.5, n), verify_down='reset')
    args.update(kw)
    return args


def one_line(args, i):
    """The same run for line i alone (n = 1)."""
    a = dict(args)
    a['V0'] = {r: np.atleast_1d(v)[i:i + 1] for r, v in args['V0'].items()}
    a['g_mat'] = args['g_mat'][:, i:i + 1]
    for key in ('alpha_C', 'alpha_D', 'consumption', 'inc_allow'):
        a[key] = np.atleast_1d(args[key])[i:i + 1]
    return a


def compare(batch, alone, i):
    def walk(x, y, path):
        if isinstance(x, dict):
            for key in x:
                walk(x[key], y[key], path + (key,))
        elif isinstance(x, np.ndarray):
            assert x[i] == pytest.approx(y[0], abs=1e-12, rel=1e-12), path
    for name in ('E_cash', 'A_D', 'EC', 'LB', 'LBp', 'inc_left', 'inc_paid', 'inc_total', 'state_cash', 'lost_refund',
                 'unpaid_D', 'unpaid_B', 'paid', 'refunded', 'vD', 'uo', 'R'):
        walk(getattr(batch, name), getattr(alone, name), (name,))


@pytest.mark.parametrize('b_mode', ['sale', 'lien', 'income'])
def test_K6_a_line_alone_equals_the_same_line_in_a_batch_of_1000(b_mode):
    args = mixed_lines(1000, 30, 6, b_mode)
    batch = K.run_lines(LOGI, **args)
    assert batch.n == 1000 and batch.paid.min() > 0
    for i in (0, 1, 499, 998, 999):
        compare(batch, K.run_lines(LOGI, **one_line(args, i)), i)


def test_K7_cumulative_paid_and_refunded_equal_the_sum_of_the_flows():
    for b_mode in K.B_MODES:
        args = mixed_lines(40, 30, 7, b_mode)
        book, log = K.run_lines(LOGI, collect=True, **args)
        paid, ref = np.zeros(40), np.zeros(40)
        for _, kind, fl in log:
            for c in fl.credited.values():
                paid += np.maximum(c, 0.0)
                ref += np.maximum(-c, 0.0)
            paid += np.maximum(fl.income, 0.0)
            ref += np.maximum(-fl.income, 0.0)
        assert np.abs(paid - book.paid).max() < 1e-12 and np.abs(ref - book.refunded).max() < 1e-12
        assert book.paid.min() > 0 and book.refunded.max() > 0
        assert np.all(book.lost_refund >= -1e-12)


def sell_and_settle(alpha, g, N, stale_basis=False, V0=20.0):
    """Route C line on the kernel path: N holding years at alpha, a sell year where alpha drops out (declared
    value falls to f x V), then post-sale years at g = 0 until the tax is quiet. Returns the three terms and TW."""
    b = K.run_lines(LOGI, np.full(N, g), {'C': V0}, alpha_C=alpha)
    sell = dict(K.step_year(b, LOGI, 1.0, g, 0.0, alpha_C=1.0))['tax']      # sell year, alpha = 1
    sold = b.R['C']
    L_sell = float(sell.credited.get('C', [0.0])[0])
    W_sell = float(sold['f'][0] * sold['V'][0] + L_sell)       # declared value before the tax was paid
    if stale_basis:
        sold['Wp'] = np.array([W_sell])                                       # v1 convention: basis stays at W_sell
    settle = 0.0
    for _ in range(50):
        fl = dict(K.step_year(b, LOGI, 1.0, 0.0, 0.0, alpha_C=1.0))['tax']
        settle += float(fl.credited.get('C', [0.0])[0])
        if abs(fl.L[0]) < 1e-13:
            break
    return dict(W_sell=W_sell, L_sell=L_sell, settle=settle, TW=float(b.family_true()[0]))


def decomposition(alpha, g, N, stale_basis=False):
    a, h = sell_and_settle(alpha, g, N, stale_basis), sell_and_settle(1.0, g, N, stale_basis)
    W_sell_delta, refund_delta, settle_delta = a['W_sell'] - h['W_sell'], a['L_sell'] - h['L_sell'], a['settle'] - h['settle']
    tw_adv = a['TW'] - h['TW']                                                # read off the book, not the flows
    return tw_adv, W_sell_delta - refund_delta - settle_delta, settle_delta


def test_K8_decomposition_identity_on_the_70_point_grid():
    alphas = (0.5, 0.75, 1.0, 1.5, 2.0, 3.0, 5.0)                             # alpha 0.5 to 5
    gs = (-0.03, 0.0, 0.0745, 0.1045, 0.20)                                    # g -3% to 20%
    grid = list(itertools.product(alphas, gs, (10, 30)))
    assert len(grid) == 70
    worst = 0.0
    for alpha, g, N in grid:
        lhs, rhs, _ = decomposition(alpha, g, N)
        worst = max(worst, abs(lhs - rhs))
    assert worst < 1e-12, worst


def test_K8_identity_with_a_non_zero_settle_delta():
    lhs, rhs, settle_delta = decomposition(1.5, 0.1045, 30, stale_basis=True)
    assert abs(settle_delta) > 1e-3                                           # the third term is exercised
    assert abs(lhs - rhs) < 1e-12


def test_K9_a_T_by_n_growth_matrix_equals_n_separate_runs():
    n, T = 7, 25
    args = mixed_lines(n, T, 9, 'income')
    batch = K.run_lines(LOGI, **args)
    for i in range(n):
        a = one_line(args, i)
        a['g_mat'] = args['g_mat'][:, i]                                      # a (T,) series for one line
        compare(batch, K.run_lines(LOGI, **a), i)
    with pytest.raises(ValueError):
        K.run_lines(LOGI, np.zeros((T, 3)), {'A': np.ones(n)})                # columns must be 1 or n


def test_K10_hand_cases_from_the_docstring():
    # Mixed routes: the tax splits by positive-delta shares. A gains 30, C gains 10 (declared) -> shares 3/4, 1/4.
    b = K.Book(1, {'A': 100.0, 'C': 100.0})
    b.R['C']['Wp'] = np.array([100.0]); b.R['C']['dd'] = np.array([110.0])
    b.R['A']['dd'] = np.array([130.0]); b.R['A']['V'] = np.array([130.0])
    fl = K.assess(b, FLAT, 1.0)
    assert fl.L[0] == pytest.approx(4.0) and fl.credited['A'][0] == pytest.approx(3.0) and fl.credited['C'][0] == pytest.approx(1.0)
    # Route C refund is capped by units paid: pay 6 (units 6/180), then a loss of 1,000 refunds only what was paid
    b = K.Book(1, {'C': 100.0}, alpha0={'C': 1.2})
    year(b, 0.5, alpha_C=1.2)
    fl = year(b, -0.9, alpha_C=1.2)
    assert b.uo['C'][0] == pytest.approx(0.0, abs=1e-15) and b.lost_refund[0] > 0 and b.R['C']['s'][0] == pytest.approx(0.0, abs=1e-15)
    # c_cap = units_and_value: the refund in units is also capped by the value paid (EC / V)
    b = K.Book(1, {'C': 100.0}, alpha0={'C': 1.2}, c_cap='units_and_value')
    year(b, 0.5, alpha_C=1.2)
    year(b, 0.5, alpha_C=1.2)
    assert b.EC[0] >= 0.0 and b.check()['min_EC'] >= -1e-12
    # Route D: a refund first cancels accrued liability, with no cash moved
    b = K.Book(1, {'D': 100.0})
    year(b, 0.5)
    fl = year(b, -0.2)
    assert b.A_D[0] == pytest.approx(2.0) and b.E_cash[0] == 0.0 and b.refunded[0] == 0.0
    # Income mode: pay from income up to the allowance, the rest by sale; a refund returns income first
    b = K.Book(1, {'B': 100.0}, b_mode='income', inc_allow=2.0)
    fl = year(b, 0.5)
    assert fl.income[0] == pytest.approx(2.0) and b.R['B']['s'][0] == pytest.approx(3.0 / 150.0) and b.paid[0] == pytest.approx(5.0)
    fl = year(b, -0.2)
    assert fl.income[0] == pytest.approx(-2.0) and b.refunded[0] == pytest.approx(2.94) and b.state_cash[0] == pytest.approx(0.0)
    # Verification moves a share of C units to Cv and verified_share reads it back
    b = K.Book(1, {'C': 100.0}, has_cv=True)
    year(b, 0.5, lam_C=0.25)
    assert K.verified_share(b)[0] == pytest.approx(0.25)
    assert b.check()['units'] < 1e-12


def test_kernel_has_no_project_import_and_no_ladder_or_heir_rule():
    tree = ast.parse(pathlib.Path(K.__file__).read_text())
    mods = {a.name.split('.')[0] for n in ast.walk(tree) if isinstance(n, ast.Import) for a in n.names}
    mods |= {n.module.split('.')[0] for n in ast.walk(tree) if isinstance(n, ast.ImportFrom)}
    assert mods <= {'numpy', 'dataclasses', '__future__'}
