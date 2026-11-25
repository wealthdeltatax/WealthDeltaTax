"""Brief 118c (W5b): the taxed household hook. The value the kernel moves to the state is paid from the non-pension classes (block 1); deaths and the horizon (block 2)."""
from pathlib import Path

import numpy as np
import pytest

from model_v3.core import base as bs, kernel as K, pack as pk, revenue as rv, schedule as S
from model_v3.runner import arm

ROOT = Path(__file__).resolve().parents[3]
PACK, REG = pk.load_pack(ROOT / 'data' / 'country-packs' / 'GBR'), pk.load_register(ROOT / 'data' / 'input-register' / 'inputs.json')
BASE = bs.build_base(PACK, REG, 1.0)
ST = arm.line_state(BASE, PACK.tables['decile_composition'], REG, 0.0101)
NEG = arm.line_state(BASE, PACK.tables['decile_composition'], REG, -0.3)                           # a negative saving: a zero-unit line cannot restart (137c)
GAIN = dict(property=0.016455, net_financial=0.0094, physical=0.0, pension=0.0094)
RATE = S.rate_function(k=0.01, tau_0=0.05, tau_m=0.50, W_min=BASE.w_min)


def book_for(st, paths=1, **kw):
    tot = np.tile(sum(st['pos'].values()), paths)
    return K.Book(paths * 14, {'A': 0.4 * tot, 'B': 0.3 * tot, 'D': 0.3 * tot}, **kw)


def run(hook, years, paths=1, G=0, **kw):
    """The kernel's taxed years, deaths every G years, the horizon settled: yields (t, kind, book, account) after each step, hook.reconcile applied after every settlement."""
    book, n = book_for(hook.st, paths, **kw), paths * 14
    for t in range(1, years + 1):
        K.step_year(book, RATE, 1.0, np.zeros(n), 0.0, hook=hook, t=t)
        yield t, 'year', book, hook.account()
        if G and t % G == 0 and t < years:
            K.step_death(book, RATE, 1.0)
            hook.reconcile(book)
            yield t, 'death', book, hook.account()
    K.settle_terminal(book)
    hook.reconcile(book)
    yield years, 'end', book, hook.account()


def test_the_account_closes_in_every_line_and_year_with_tax_on_and_i1_holds():
    h, paid = arm.HouseholdHook(ST, GAIN, 0.0157), 0.0
    for t, kind, book, a in run(h, 12):
        assert np.abs(a['residual']).max() < 1e-9 and (a['unpaid'] == 0).all() and K.shortfall_lines(book) == 0
        assert np.abs(book.family_true() - sum(h.q[k] for k in arm.CLASSES[:3])).max() < 1e-9 and (book.pen == h.q['pension']).all()
        paid += a['T_WDT'].sum()
    assert paid > 0


def test_the_payment_follows_the_class_weights_and_never_touches_pension():
    h = arm.HouseholdHook(ST, GAIN, 0.0157)
    for t, kind, book, a in run(h, 3):
        T, w = a['T_WDT'], {k: np.maximum(h.q1[k], 0.0) for k in arm.CLASSES[:3]}
        for k in arm.CLASSES[:3]:
            assert np.abs((h.q1[k] - h.q[k]) - T * w[k] / sum(w.values())).max() < 1e-9
        assert (h.q['pension'] == h.q1['pension']).all()
    assert T.max() > 0


def test_the_payment_ratios_are_over_the_pre_payment_balances_and_zero_when_nothing_is_paid():
    h = arm.HouseholdHook(ST, GAIN, 0.0157)
    for t, kind, book, a in run(h, 4):
        T, nonpen = a['T_WDT'], sum(h.q1[k] for k in arm.CLASSES[:3])
        assert np.allclose(a['pay_over_nonpension'][T > 0], (T / nonpen)[T > 0]) and np.allclose(a['pay_over_fin'][T > 0], (T / h.q1['net_financial'])[T > 0]) and (a['pay_over_fin'][T == 0] == 0).all()


def test_i3_closes_over_several_taxed_years():
    g, gg = np.zeros((6, 3)), np.full((6, 3), 0.0157)
    h = arm.HouseholdHook(ST, GAIN, 0.0157)
    out = rv.run_lines(BASE, RATE, g, gg, 0.0, hook=h, n_phase=1)
    assert out['assessed'].min() > 0 and rv.identity(out, g, 0.0, h)['assessed'].max() < 1e-9


@pytest.mark.parametrize('mode', ['sale', 'lien'])
def test_deaths_and_the_horizon_settle_and_the_account_closes(mode):
    h, last = arm.HouseholdHook(ST, GAIN, 0.0157), None
    for t, kind, book, a in run(h, 9, G=4, b_mode=mode):
        assert np.abs(a['residual']).max() < 1e-9 and (a['unpaid'] == 0).all() and K.shortfall_lines(book) == 0 and np.abs(book.family_true() - sum(h.q[k] for k in arm.CLASSES[:3])).max() < 1e-9
        last = a
    assert (book.LB == 0).all() and (book.A_D == 0).all() and (h.q['pension'] == book.pen).all()


class Spy(arm.HouseholdHook):
    """Records the gap between the books' family value and the class total at every reconcile (the year it is called in) and at the entry of every year."""

    def __init__(self, *a, **k):
        super().__init__(*a, **k)
        self.pre_gaps, self.rec, self.t = [], [], 0

    def pre(self, book, t, g):
        self.t = t
        if book is self.book:
            self.pre_gaps.append(np.abs(self._n(self.q) - book.family_true()).max())
        return super().pre(book, t, g)

    def reconcile(self, book):
        self.rec.append((self.t, np.abs(self._n(self.q) - book.family_true()).max()))
        super().reconcile(book)


@pytest.mark.parametrize('years, G, n_phase', [(9, 4, 1), (13, 6, 6)])
def test_deaths_and_the_horizon_are_paid_in_the_year_in_the_production_path(monkeypatch, years, G, n_phase):
    books, orig = [], K.Book
    monkeypatch.setattr(K, 'Book', lambda *a, **k: books.append(orig(*a, **k)) or books[-1])
    h = Spy(ST, GAIN, 0.0157)
    out = rv.run_lines(BASE, RATE, np.zeros((years, 2)), np.full((years, 2), 0.0157), 0.0, G=G, n_phase=n_phase, hook=h)
    assert len(books) == n_phase and max(h.pre_gaps) < 1e-9                                  # nothing is left for the next year's opening to catch up
    assert any(t < years and gap > 1e-6 for t, gap in h.rec) and h.rec[-1][0] == years and h.rec[-1][1] > 1e-6    # a death's value is moved and paid in its year; the horizon's in the last year
    assert all(K.shortfall_lines(b) == 0 and (b.unpaid_B == 0).all() and (b.LB == 0).all() and (b.A_D == 0).all() for b in books)
    assert out['death_D'].sum() > 0 and np.isfinite(out['death_D']).all() and (h.rec[-1][0] == years)


def test_a_death_in_the_last_but_one_year_and_the_horizon_leave_the_books_and_classes_equal():
    books, h = [], Spy(ST, GAIN, 0.0157)
    rv.run_lines(BASE, RATE, np.zeros((5, 1)), np.full((5, 1), 0.0157), 0.0, G=4, n_phase=1, hook=h)
    assert [t for t, g in h.rec if g > 1e-6] == [4, 5] and max(h.pre_gaps) < 1e-9


def test_a_tax_the_classes_cannot_pay_becomes_a_lien_on_the_pension_not_a_debt_or_an_alarm():
    """132c (replaces the 127c finding that the book took it as net financial debt and raised unpaid_B): the unpaid part is carried as PL, the kernel's family value stays net of it, no alarm."""
    h = arm.HouseholdHook(ST, GAIN, 0.0157)
    book = book_for(ST)
    K.step_year(book, RATE, 1.0, np.zeros(14), 0.0, hook=h, t=1)
    h.q = {**h.q, 'property': np.full(14, 0.1), 'net_financial': np.full(14, -0.3), 'physical': np.zeros(14)}
    h.T, h.new, h.PL, b0, n0 = 0.0, 0.0, np.zeros(14), book.unpaid_B.copy(), sum(h.q[k] for k in arm.CLASSES[:3])
    q1 = h._pay(h.q, np.full(14, 0.01))
    assert np.allclose(h.new, 0.01) and np.allclose(h.PL, 0.01) and np.allclose(h.T, 0.0) and (book.unpaid_B == b0).all()
    assert np.allclose(sum(q1[k] for k in arm.CLASSES[:3]), n0)                       # the classes are untouched: the lien, not a debt in net financial


def test_a_line_with_no_units_stays_at_the_floor_and_the_flow_that_cannot_enter_is_the_alarm():
    """127c: a line whose units are all 0 (the tax took everything) cannot carry the year's flow; it stays at 0, I1 holds, the floor amount is recorded (and in unpaid_B). Since 137c this holds for a negative saving (NEG): a positive one restarts the line."""
    h = arm.HouseholdHook(NEG, GAIN, 0.0157)
    book = book_for(NEG)
    K.step_year(book, RATE, 1.0, np.zeros(14), 0.0, hook=h, t=1)
    for k in arm.CLASSES[:3]:
        h.q[k] = h.q[k] * 0.0
    for x in book.R.values():
        x.update({k: x[k] * 0.0 for k in ('V', 'dd', 'Wp', 'ppu')})
    b0 = book.unpaid_B.copy()
    K.step_year(book, RATE, 1.0, np.zeros(14), 0.0, hook=h, t=2)
    a = h.account()
    assert np.abs(book.family_true()).max() < 1e-12 and sum(h.q[k] for k in arm.CLASSES[:3]).max() < 1e-12
    assert (a['floor'] != 0).all() and np.abs(a['residual']).max() < 1e-9 and (book.unpaid_B > b0).all()


def test_a_line_that_never_reaches_the_floor_records_no_floor():
    h = arm.HouseholdHook(ST, GAIN, 0.0157)
    for t, kind, book, a in run(h, 12):
        assert (a['floor'] == 0).all() and K.shortfall_lines(book) == 0


def _dead_year(st, paths=1):
    """Year 1 as normal, then every line's units and non-pension classes are gone (as a tax that took all of them leaves it: f = 0, last assessment's declared value 0, price kept); year 2 is run. Returns (hook, book, account, unpaid_B before)."""
    h, book = arm.HouseholdHook(st, GAIN, 0.0157), book_for(st, paths)
    K.step_year(book, RATE, 1.0, np.zeros(14 * paths), 0.0, hook=h, t=1)
    for k in arm.CLASSES[:3]:
        h.q[k] = h.q[k] * 0.0
    for x in book.R.values():
        x['sold'], x['f'], x['Wp'] = x['sold'] + x['f'], x['f'] * 0.0, x['Wp'] * 0.0
    b0 = book.unpaid_B.copy()
    K.step_year(book, RATE, 1.0, np.zeros(14 * paths), 0.0, hook=h, t=2)
    return h, book, h.account(), b0


def test_a_line_with_no_units_and_a_positive_saving_restarts_from_it_and_the_floor_does_not_fire():
    """137c: units = saving / price; the closing class total equals the family value, I1 holds (post checks it), the units identity holds, no floor entry and no shortfall."""
    h, book, a, b0 = _dead_year(ST)
    assert (a['floor'] == 0).all() and (book.unpaid_B == b0).all() and K.shortfall_lines(book) == 0 and np.abs(a['residual']).max() < 1e-9
    assert (book.family_true() > 0).all() and np.abs(book.family_true() - sum(h.q[k] for k in arm.CLASSES[:3])).max() < 1e-9
    assert all((x['f'] >= 0).all() for x in book.R.values()) and book.check()['units'] < 1e-12                  # a route can be emptied by the year's own tax; the family value above is what restarted


def test_a_dead_line_with_no_saving_stays_at_zero_and_one_with_a_negative_saving_is_still_the_alarm():
    z = {**ST, 'income': ST['income'] * 0.0, 'acc': ST['acc'] * 0.0}
    h, book, a, b0 = _dead_year(z)
    assert np.abs(book.family_true()).max() < 1e-12 and (a['floor'] == 0).all() and all((x['f'] == 0).all() for x in book.R.values()) and np.abs(a['residual']).max() < 1e-9
    h, book, a, b0 = _dead_year(NEG)
    assert np.abs(book.family_true()).max() < 1e-12 and (a['floor'] > 0).all() and (book.unpaid_B > b0).all() and np.abs(a['residual']).max() < 1e-9


@pytest.mark.parametrize('mult', [0.0, -1.0])
def test_a_dead_line_whose_route_price_was_zeroed_or_turned_negative_restarts_at_the_opening_mix(mult):
    """137c: a rescale at N <= 0 leaves a route price at 0 or below (f may still be 1); the restart restores it to the line's opening route mix, so the family value is the closing class total again and I1 holds."""
    h = arm.HouseholdHook(ST, GAIN, 0.0157)
    book = book_for(ST)
    K.step_year(book, RATE, 1.0, np.zeros(14), 0.0, hook=h, t=1)
    for k in arm.CLASSES[:3]:
        h.q[k] = h.q[k] * 0.0
    for x in book.R.values():
        x.update({k: x[k] * mult for k in ('V', 'dd', 'Wp', 'ppu')})
        x['Wp'] = x['Wp'] * 0.0
        if mult < 0:                                                                                  # a negative price comes with the units gone (family value 0, I1)
            x['sold'], x['f'] = x['sold'] + x['f'], x['f'] * 0.0
    K.step_year(book, RATE, 1.0, np.zeros(14), 0.0, hook=h, t=2)
    a = h.account()
    assert (a['floor'] == 0).all() and np.abs(a['residual']).max() < 1e-9 and book.check()['units'] < 1e-12
    assert (book.family_true() > 0).all() and np.abs(book.family_true() - sum(h.q[k] for k in arm.CLASSES[:3])).max() < 1e-9
    assert all(x['V'].min() > 0 for x in book.R.values()) and np.allclose(book.R['A']['V'] / sum(x['V'] for x in book.R.values()), h.mix['A'])


def test_a_dead_line_with_huge_units_restarts_exactly_and_i1_holds():
    """135c: a rescale at a near-zero family value can leave the units at 1e18; f + u then lost the restart in rounding (family 0.5 for 1). A wiped line's restart sets f to the target and sold to the identity's remainder."""
    h = arm.HouseholdHook(ST, GAIN, 0.0157)
    book = book_for(ST)
    K.step_year(book, RATE, 1.0, np.zeros(14), 0.0, hook=h, t=1)
    for k in arm.CLASSES[:3]:
        h.q[k] = h.q[k] * 0.0
    for x in book.R.values():
        x.update({k: x[k] * 0.0 for k in ('V', 'dd', 'Wp', 'ppu')})
        x['sold'], x['f'] = x['sold'] + x['f'] - 2.5e18, x['f'] * 0.0 + 2.5e18 * (1.0 if x is book.R['A'] else -1.0)
        x['f'] = x['f'] if x is book.R['A'] else x['f'] * 0.0
    K.step_year(book, RATE, 1.0, np.zeros(14), 0.0, hook=h, t=2)
    a = h.account()
    assert (a['floor'] == 0).all() and np.abs(book.family_true() - sum(h.q[k] for k in arm.CLASSES[:3])).max() < 1e-9 and (book.family_true() > 0).all()


def test_a_restart_with_the_verified_tranche_keeps_i1_over_the_following_years():
    """137c: the production book has route C and its verified tranche Cv (priced at C's). A restart restores both prices, so units that later move from C to Cv keep the family value equal to the class total (post raises otherwise)."""
    st = {**ST, 'pos': {**ST['pos'], 'pension': ST['pos']['pension'] * 1e-3}}                          # a small pension: the year's tax stays inside the units (the I1 pension check is absolute, 1e-12)
    tot, h = sum(st['pos'].values()), arm.HouseholdHook(st, GAIN, 0.0157)
    book = K.Book(14, {'A': 0.5 * tot, 'B': 0.25 * tot, 'C': 0.08 * tot, 'D': 0.17 * tot}, has_cv=True)
    step = lambda t: K.step_year(book, RATE, 1.0, np.zeros(14), 0.0, lam_C=0.3, hook=h, t=t)
    step(1)
    for k in arm.CLASSES[:3]:
        h.q[k] = h.q[k] * 0.0
    for x in book.R.values():
        x.update({k: x[k] * 0.0 for k in ('V', 'dd', 'Wp', 'ppu')})
    for t in range(2, 6):
        step(t)
        assert (h.account()['floor'] == 0).all() and np.abs(book.family_true() - sum(h.q[k] for k in arm.CLASSES[:3])).max() < 1e-9
    assert (book.R['Cv']['f'] > 0).any() and book.check()['units'] < 1e-12


def test_the_i1_check_accepts_the_kernel_caps_residual_and_rejects_a_larger_one():
    """138c: a gap of up to 1e-7 (the cap's own tolerance, the lien's unit part on a line the floor holds at 0) passes; 1e-6 raises."""
    import pytest
    h = arm.HouseholdHook(ST, GAIN, 0.0157)
    book = book_for(ST)
    K.step_year(book, RATE, 1.0, np.zeros(14), 0.0, hook=h, t=1)
    h.q = {**h.q, 'net_financial': h.q['net_financial'] + 5e-8}
    h._check(book)
    h.q = {**h.q, 'net_financial': h.q['net_financial'] + 1e-6}
    with pytest.raises(ValueError):
        h._check(book)
