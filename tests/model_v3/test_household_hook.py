"""Brief 117c (W5a): the household arm's line state and its debt rule (block 1), the hook and its equivalence with cells.run_cell (blocks 2 and 3)."""
from pathlib import Path

import numpy as np
import pytest

from model_v3.core import base as bs, cells as ce, kernel as K, pack as pk, revenue as rv, schedule as S
from model_v3.runner import arm

ROOT = Path(__file__).resolve().parents[2]
PACK, REG = pk.load_pack(ROOT / 'model_v3' / 'pack' / 'GBR'), pk.load_register(ROOT / 'registry' / 'inputs.json')
BASE = bs.build_base(PACK, REG, 1.0)
COMP = PACK.tables['decile_composition']
ST = arm.line_state(BASE, COMP, REG, 0.0101)
GAIN = dict(property=0.016455, net_financial=0.0094, physical=0.0, pension=0.0094)


def test_class_balances_sum_to_line_wealth_and_d1_keeps_its_negative_shares():
    assert all(a.shape == (14,) for a in (*ST['pos'].values(), ST['income'], ST['sav'], ST['acc']))
    assert np.allclose(sum(ST['pos'].values()), BASE.wealth, rtol=1e-12, atol=0)
    assert ST['pos']['property'][0] == pytest.approx(-0.0472 * BASE.wealth[0], rel=1e-3) and ST['pos']['net_financial'][0] == pytest.approx(-1.0492 * BASE.wealth[0], rel=1e-3)


def test_tail_lines_carry_the_d10_mix_and_the_incomes_are_the_band_means():
    sh = {k: v / BASE.wealth for k, v in ST['pos'].items()}
    assert all(np.allclose(sh[k][9:], sh[k][9]) for k in sh) and sh['pension'][9] == pytest.approx(0.364, rel=1e-3) and sh['pension'][3] == pytest.approx(0.3614, rel=1e-3)
    per = REG['I-D4h'].central * 1e6
    assert ST['income'][0] == pytest.approx(REG['I-D9a'].low / per) and ST['income'][3] == pytest.approx(REG['I-D9a'].central / per) and ST['income'][13] == pytest.approx(REG['I-D9d'].central / per)
    assert np.allclose(arm.line_state(BASE, COMP, REG, 0.0101, scale=1.3733)['income'], 1.3733 * ST['income']) and ST['acc'][0] == REG['I-D1k'].central / 100 and (ST['sav'] == 0.0101).all()


def test_the_debt_rule_gives_a_negative_property_or_net_financial_balance_no_return():
    g = arm.returns(ST['pos'], GAIN)
    assert g['net_financial'][0] == 0.0 and g['property'][0] == 0.0 and (g['physical'] == 0.0).all()
    assert (g['net_financial'][ST['pos']['net_financial'] >= 0] == GAIN['net_financial']).all() and (g['pension'] == GAIN['pension']).all() and (g['property'][5:] == GAIN['property']).all()


CELLS = ce.scaled(ce.cell_table(PACK, REG, 0.44), 1.8014e12)[0]
CST = dict(pos={k: np.array([c['pos'][k] for c in CELLS]) for k in arm.CLASSES}, income=np.array([c['income'] for c in CELLS]), sav=np.full(10, 0.0101), acc=np.full(10, 0.0483))
RETS = dict(g=GAIN, y=dict(property=0.03758, net_financial=0.0426, physical=0.0, pension=0.0426))
ZERO = lambda w: np.zeros_like(w)


def drive(hook, st, years, paths=1, rate=ZERO, g=None):
    """The kernel's year with no tax under `hook` on lines carrying `st`: yields (t, book) with the classes' total in the book's routes."""
    n, tot = paths * len(st['income']), np.tile(sum(st['pos'].values()), paths)
    book = K.Book(n, {'A': 0.6 * tot, 'B': 0.4 * tot})
    for t in range(1, years + 1):
        K.step_year(book, rate, 1.0, np.zeros(n) if g is None else g[t - 1], 0.0, hook=hook, t=t)
        yield t, book


def test_the_untaxed_hook_reproduces_run_cell_year_by_year_and_i1_holds_in_every_year():
    rows = [ce.run_cell(c, 40, 0.0101, 0.0483, 0.0157, RETS) for c in CELLS]
    h = arm.HouseholdHook(CST, GAIN, 0.0157)
    for t, book in drive(h, CST, 40):
        assert all(np.abs(h.q[k] - [r[t - 1][1][k] for r in rows]).max() < 1e-9 for k in arm.CLASSES)                       # the account of every cell, class by class
        assert np.abs(book.family_true() + book.pen - sum(h.q[k] for k in arm.CLASSES)).max() < 1e-9 and np.abs(book.family_true() - sum(h.q[k] for k in arm.CLASSES[:3])).max() < 1e-9


def test_every_line_gets_route_units_and_a_line_without_non_pension_wealth_raises():
    h = arm.HouseholdHook(ST, GAIN)
    for _, book in drive(h, ST, 1):
        assert all((x['f'] > 0).all() and (x['V'] > 0).all() for x in book.R.values()) and (book.pen > 0).all()
    bad = dict(ST, pos={**ST['pos'], 'property': -1.0 - ST['pos']['net_financial'] - ST['pos']['physical']})       # N = -1, pension positive
    with pytest.raises(ValueError, match='no route units'):
        next(drive(arm.HouseholdHook(bad, GAIN), bad, 1))


def test_a_negative_net_financial_balance_earns_nothing():
    lo = dict(CST, sav=np.full(10, -0.026), acc=np.full(10, 0.0041))
    plain = [ce.run_cell(c, 3, -0.026, 0.0041, 0.0157, RETS) for c in CELLS]
    h = arm.HouseholdHook(lo, GAIN, 0.0157)
    for t, _ in drive(h, lo, 3):
        pass
    assert (h.q['net_financial'][0] < 0) and abs(h.q['net_financial'][0] - plain[0][2][1]['net_financial']) > 1e-6        # D1-3 net financial: gain on a negative balance dropped


def test_the_state_folds_with_paths_as_the_book_does_and_each_path_equals_a_single_run():
    one, three = arm.HouseholdHook(ST, GAIN, 0.0157), arm.HouseholdHook(ST, GAIN, 0.0157)
    list(drive(one, ST, 8))
    list(drive(three, ST, 8, paths=3))
    assert all(np.array_equal(three.q[k].reshape(3, 14), np.tile(one.q[k], (3, 1))) for k in arm.CLASSES)


def test_the_untaxed_hook_reproduces_the_stored_111c_baseline_wealth():
    cells = ce.scaled(ce.cell_table(PACK, REG, 0.4385526696023258), 1801414000000.0)[0]               # the constants of docs/model-v3/cell-baseline/inputs_used.json (mid return, median saving, accrual observed)
    st = dict(pos={k: np.array([c['pos'][k] for c in cells]) for k in arm.CLASSES}, income=np.array([c['income'] for c in cells]), sav=np.full(10, 0.0100626), acc=np.full(10, 0.0483))
    n, h = np.array([c['households'] for c in cells]), arm.HouseholdHook(st, dict(GAIN, net_financial=0.052 - 0.0426115, pension=0.052 - 0.0426115), 0.01570385404020596)
    stored = {1: 13827087740420, 10: 16372370305364, 50: 34185897638460, 100: 83136904645147}
    for t, _ in drive(h, st, 100):
        if t in stored:
            assert (n * sum(h.q[k] for k in arm.CLASSES)).sum() * ce.UNIT == pytest.approx(stored[t], rel=1e-9)


def test_the_legacy_mode_reproduces_the_legacy_hook_path_to_zero_and_keeps_the_classes_at_the_book():
    g, c, rate = np.random.default_rng(4).uniform(-0.2, 0.3, (20, 14)), 0.035, ZERO
    a, b = (list(drive(hk, ST, 20, rate=rate, g=g))[-1][1] for hk in (arm.LegacyHook(c), arm.HouseholdHook(ST, GAIN, c=c)))
    assert all(np.array_equal(a.R[r][k], b.R[r][k]) for r in a.R for k in a.R[r]) and np.array_equal(a.paid, b.paid) and np.array_equal(a.family_true(), b.family_true())


class Free(arm.HouseholdHook):
    """A taxed year with the payment half left out (W5b): the classes roll forward untaxed, so only the first year of a run is consistent."""
    def post(self, book, fl):
        self.q = self.q1


def test_sites_2_and_3_read_the_hook_wealth_and_the_recorded_gain_and_i3_closes():
    rate, g, gg = S.rate_function(k=0.01, tau_0=0.15, tau_m=0.70, W_min=BASE.w_min), np.zeros((1, 3)), np.full((1, 3), 0.0157)
    h = Free(ST, GAIN, 0.0157)
    run = rv.run_lines(BASE, rate, g, gg, 0.0, hook=h, n_phase=1)
    w0, w1 = np.tile(BASE.wealth, 3), h.W_after
    assert np.allclose(run['wbase'][0], run['adults_k'] * (np.tile(BASE.weights, 3) * np.where(w1 >= BASE.w_min, w0, 0.0)).reshape(3, 14).sum(1), rtol=1e-12)    # the base is units plus pension
    assert run['assessed'].min() > 0 and rv.identity(run, g, 0.0, h)['assessed'].max() < 1e-9
    zero = rv.run_lines(BASE, ZERO, np.zeros((6, 3)), np.full((6, 3), 0.0157), 0.0, hook=arm.HouseholdHook(ST, GAIN, 0.0157))        # six untaxed years in six phases: I1 is checked in every year
    assert zero['tax'].max() == 0.0


def test_convention_b_gives_the_same_first_year_account_so_nothing_is_counted_twice():
    h = arm.HouseholdHook(CST, GAIN, 0.0157)
    list(drive(h, CST, 1))
    b = [ce.run_cell(c, 1, 0.0101, 0.0483, 0.0157, RETS, 'B')[0][2]['dNW'] for c in CELLS]
    assert np.abs(sum(h.q[k] for k in arm.CLASSES) - sum(CST['pos'][k] for k in arm.CLASSES) - b).max() < 1e-9


def test_the_tail_pension_is_capped_at_the_d10_mean_and_wealth_per_line_is_unchanged():
    cap = arm.d10_pension(BASE, COMP, PACK.tables['wealth_distribution'])
    st = arm.line_state(BASE, COMP, REG, 0.0101, cap=cap)
    tail = [i for i, x in enumerate(BASE.labels) if x in arm.TAKES_D10]
    assert cap == pytest.approx(0.3859, rel=1e-3) and np.allclose(st['pos']['pension'][tail], np.minimum(ST['pos']['pension'][tail], cap), rtol=1e-12, atol=0)
    assert np.allclose(st['pos']['pension'][[11, 12, 13]], cap) and st['pos']['pension'][9] == ST['pos']['pension'][9] < cap < ST['pos']['pension'][10]
    assert np.allclose(sum(st['pos'].values()), BASE.wealth, rtol=1e-12, atol=0) and np.allclose(sum(v[tail] for v in st['pos'].values()), BASE.wealth[tail], rtol=1e-12, atol=0)
    assert all(np.array_equal(st['pos'][k][:9], ST['pos'][k][:9]) for k in arm.CLASSES) and arm.line_state(BASE, COMP, REG, 0.0101, cap=None)['pos']['pension'].tolist() == ST['pos']['pension'].tolist()
    mix = [st['pos'][k][13] - ST['pos'][k][13] for k in arm.CLASSES[:3]]
    d10 = np.array([arm.comp_share(COMP, 'D10', k) for k in arm.CLASSES[:3]])
    assert np.allclose(np.array(mix) / sum(mix), d10 / d10.sum(), rtol=1e-9) and sum(mix) == pytest.approx(ST['pos']['pension'][13] - cap, rel=1e-12)


def test_the_register_value_of_the_cap_is_the_d10_mean_pension_so_replacing_it_is_one_value():
    row = REG['I-D1l']
    assert row.central == 0.386 and row.central == pytest.approx(arm.d10_pension(BASE, COMP, PACK.tables['wealth_distribution']), abs=5e-4)
    assert arm.line_state(BASE, COMP, REG, 0.0101, cap=row.central)['pos']['pension'][13] == 0.386
