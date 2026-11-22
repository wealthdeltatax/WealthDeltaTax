"""Brief 118c (W5b): the taxed household hook. The value the kernel moves to the state is paid from the non-pension classes (block 1); deaths and the horizon (block 2)."""
from pathlib import Path

import numpy as np
import pytest

from model_v3.core import base as bs, kernel as K, pack as pk, revenue as rv, schedule as S
from model_v3.runner import arm

ROOT = Path(__file__).resolve().parents[2]
PACK, REG = pk.load_pack(ROOT / 'model_v3' / 'pack' / 'GBR'), pk.load_register(ROOT / 'registry' / 'inputs.json')
BASE = bs.build_base(PACK, REG, 1.0)
ST = arm.line_state(BASE, PACK.tables['decile_composition'], REG, 0.0101)
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
