"""Brief 133c, block 1: the tax a route cannot pay is carried as a lien (the kernel's cap callback, default off) and settled."""
import numpy as np

from model_v3.core import kernel as K
from model_v3.runner import arm

POS = dict(property=np.array([0.04]), net_financial=np.array([0.01]), physical=np.array([0.0]), pension=np.array([5.0]))
ST = dict(pos=POS, income=np.array([0.0]), sav=np.array([0.0]), acc=np.array([0.0]))
GAIN = dict(property=0.0, net_financial=0.0, physical=0.0, pension=0.2)            # the pension gains 1.0 a year, the units hold 0.05


def test_the_cap_records_in_unpaid_b_by_default_and_hands_the_excess_to_a_callback_when_one_is_set():
    book, seen = K.Book(1, {'A': np.array([1.0])}), []
    assert np.array_equal(K._cap(book, np.array([3.0]), np.array([1.0])), [1.0]) and np.array_equal(book.unpaid_B, [2.0]) and K.shortfall_lines(book) == 1
    book = K.Book(1, {'A': np.array([1.0])})
    book.cap_cb = lambda b, ex: seen.append(ex.copy())
    assert np.array_equal(K._cap(book, np.array([3.0]), np.array([1.0])), [1.0]) and np.array_equal(seen[0], [2.0]) and K.shortfall_lines(book) == 0
    assert np.array_equal(K._cap(book, np.array([0.5]), np.array([1.0])), [0.5]) and np.array_equal(seen[1], [0.0])


def run(years, rates, r_def=0.0):
    h = arm.HouseholdHook(ST, GAIN, 0.0)
    book = K.Book(1, {'A': np.array([0.05])}, r_def=r_def)
    for t in range(1, years + 1):
        K.step_year(book, lambda w, r=rates[t - 1]: r + 0.0 * w, 1.0, np.zeros(1), 0.0, hook=h, t=t)
    return h, book


def test_the_excess_is_carried_accrues_and_settles_from_the_pension_with_the_account_closed():
    h, book = run(1, [0.5])
    ex = h.PL[0]
    assert ex > 0.4 and np.isclose(ex, 0.5 * 1.0 - 0.05, atol=1e-9) and h.PK[0] == ex and K.shortfall_lines(book) == 0 and book.unpaid_B[0] == 0
    a = h.account()
    assert abs(a['residual'][0]) < 1e-9 and np.isclose(a['T_WDT'][0], 0.05, atol=1e-12) and np.isclose(book.pen[0], 5.0 + 1.0 - ex, atol=1e-12)    # the kernel's pension is net of the lien
    assert np.isclose(h.lien()['new'][0], ex) and h.lien()['bal'][0] == ex
    h.settle(book)                                                                                  # the horizon: no class holds anything, the one-off draw takes it from the pension
    assert h.PL[0] == 0 and np.isclose(h.set_p[0], ex) and np.isclose(h.q['pension'][0], 6.0 - ex) and np.isclose(book.pen[0], 6.0 - ex) and h.unpaid[0] == 0


def test_the_lien_accrues_at_r_def_and_the_ledger_ties():
    h, book = run(2, [0.5, 0.0], r_def=0.1)                                                         # year 2 assesses nothing; the units are gone, so the 127c floor stands (reported separately)
    ex = 0.5 * 1.0 - 0.05
    assert np.isclose(h.PL[0], ex * 1.1, atol=1e-9) and np.isclose(h.lien()['accr'][0], 0.1 * ex, atol=1e-9)
    h.settle(book)
    assert np.isclose(h.set_p[0], ex * 1.1, atol=1e-9) and h.PL[0] == 0
