"""Brief 108c: the household step. The identity closes, the worked household of 104r gives 54 on both sides, a double count is caught, legacy equals the kernel, pension is never sold."""
import numpy as np
import pytest

from model_v3.core import household as hh, kernel as kn

POS = dict(property=600.0, equity=200.0, cash=100.0, pension=400.0, debt=200.0)
FLOWS = dict(Y_L=60.0, Y_P=38.0, I_D=8.0, T_C=12.0, C=58.0, pen_in=20.0)
G = dict(property=0.02, equity=0.02, cash=-0.02, pension=0.05)
Y = dict(property=0.03, equity=0.03, pension=0.03)
DEFL = dict(cpi=0.02, hfce=0.025)
STEP = lambda mode, **kw: hh.household_step('D4-5', POS, FLOWS, dict(g=G, y=Y), DEFL, mode, **{**dict(T_WDT=5.0, source_weights={'equity': 1.0}, sink='cash', fin=('equity', 'cash')), **kw})
close = lambda a, b: np.allclose(a, b, rtol=0, atol=1e-9)


def test_the_worked_household_gives_54_in_a_and_in_b():
    q, a = STEP('A')
    assert close([q[k] for k in ('property', 'equity', 'cash', 'pension', 'debt')], [612, 199, 98, 440, 195])
    assert close([a['dNW'], a['S'], a['CG'], a['CG_wedge'], a['T_WDT'], a['TR'], a['O']], [54, 20, 39, 1.0, 5, 0, 0])
    assert close(STEP('B')[1]['dNW'], 54) and close(sum(q[k] for k in q if k != 'debt') - q['debt'] - 1100, 54)


def test_counting_the_yield_twice_is_caught_by_an_independent_stock_calculation():
    S = FLOWS['Y_L'] + FLOWS['Y_P'] - FLOWS['I_D'] - FLOWS['T_C'] - FLOWS['C']
    wrong = sum((POS[k] * (1 + G[k] + Y.get(k, 0.0))) for k in G) - (POS['debt'] * (1 - DEFL['hfce'])) + S - FLOWS['pen_in'] + FLOWS['pen_in'] - 5.0 - 1100
    _, a = STEP('A')
    assert close(wrong, 90) and abs(wrong - (a['S'] + a['CG'] - a['T_WDT'])) == pytest.approx(36)    # total return credited and the yield left in S: 36 too much


def test_the_identity_holds_and_a_equals_b_on_a_grid():
    rng = np.random.default_rng(3)
    for _ in range(50):
        pos = {k: rng.uniform(1, 500, 4) for k in POS}
        fl = {k: rng.uniform(0, 60, 4) for k in ('Y_L', 'Y_P', 'I_D', 'T_C', 'C', 'pen_in', 'pen_out')}
        rets = dict(g={k: rng.uniform(-.05, .08) for k in G}, y={k: rng.uniform(0, .05) for k in Y})
        T, O = rng.uniform(0, 20, 4), rng.uniform(-5, 5, 4)
        out = [hh.household_step('x', pos, fl, rets, DEFL, m, T_WDT=T, O=O, sink='cash')[1] for m in ('A', 'B')]
        assert close(out[0]['dNW'], out[1]['dNW']) and close(out[0]['dNW'], out[0]['S'] + out[0]['CG'] + out[0]['O'] - out[0]['T_WDT'])


def test_legacy_is_bit_equal_to_the_kernels_growth_and_consumption():
    rng = np.random.default_rng(5)
    for g, c in ((0.0474, 0.035), (0.0, 0.0), (-0.1, 0.5), (0.3, 0.01)):
        W = rng.uniform(0.1, 1e4, 6)
        book = kn.Book(6, {'A': W})
        kn.grow_and_consume(book, g, c)
        q, a = hh.household_step('x', dict(financial=W), dict(c=c), dict(r=g), DEFL, 'legacy', T_WDT=0.0)
        assert np.array_equal(q['financial'], book.family_true()) and close(a['dNW'], a['S'] + a['CG'])


def test_pension_is_not_available_until_withdrawn_and_the_payment_falls_pro_rata():
    pos = dict(property=600.0, financial=300.0, physical=100.0, pension=1000.0, debt=0.0)
    q, a = hh.household_step('x', pos, {}, dict(g={}), DEFL, 'A', T_WDT=100.0)
    assert q['pension'] == 1000.0 and close([q['property'], q['financial'], q['physical']], [540, 270, 90]) and close([a['shares'][k] for k in ('property', 'financial', 'physical')], [.6, .3, .1])
    assert close(a['dNW'], -100) and close(a['T_WDT'], 100) and close(a['S'] + a['CG'] + a['O'] - a['T_WDT'], -100)
    q, a = hh.household_step('x', pos, dict(pen_out=10.0), dict(g={}), DEFL, 'A')
    assert close([q['pension'], q['financial'], a['dNW']], [990, 310, 0])
    for kw in (dict(T_WDT=1001.0), dict(T_WDT=5.0, source_weights={'pension': 1.0})):
        with pytest.raises(ValueError):
            hh.household_step('x', pos, {}, dict(g={}), DEFL, 'A', **kw)


def test_the_liquidity_diagnostic_reports_payment_over_financial_and_over_non_pension_wealth():
    pos = dict(property=600.0, financial=50.0, physical=50.0, pension=1000.0, debt=0.0)
    for T, flag in ((20.0, False), (80.0, True)):
        a = hh.household_step('x', pos, {}, dict(g={}), DEFL, 'A', T_WDT=T)[1]
        assert close([a['pay_over_fin'], a['pay_over_nonpension']], [T / 50, T / 700]) and bool(a['pay_exceeds_fin']) is flag


def test_bad_arguments_are_refused():
    for kw in (dict(convention='C'), dict(convention='A', TR=1.0), dict(convention='A', sink='pension')):
        with pytest.raises(ValueError):
            hh.household_step('x', POS, FLOWS, dict(g=G), DEFL, **kw)


def test_a_cell_with_negative_non_pension_wealth_steps_when_nothing_is_paid():   # 110c
    pos = dict(property=5.0, financial=-8.0, physical=1.0, pension=50.0, debt=0.0)
    q, a = hh.household_step('x', pos, dict(Y_L=10.0, C=12.0), dict(g={}), DEFL, 'A')
    assert close([q['financial'], a['dNW'], a['pay_over_nonpension']], [-10.0, -2.0, np.inf]) and np.isfinite(sum(q.values()))

