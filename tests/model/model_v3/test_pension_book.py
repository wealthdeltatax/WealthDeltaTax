"""Brief 116c (W4): the pension as a balance beside the book's units: in the assessed base, never a unit; the route-share fallback of `assess`."""
import pathlib
import sys

import numpy as np
import pytest

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[3]))
from model_v3.core import kernel as K  # noqa: E402

FLAT = lambda x: np.full(np.shape(x), 0.1)


def assess_with(book, Wn, Wp, monkeypatch):
    """K.assess with Wn and Wp given; returns (Flows, {route: Lr}) where Lr is what each route was asked to settle."""
    got, real = {}, K._route_tax
    monkeypatch.setattr(K, '_route_tax', lambda b, fl, r, Lr: (got.__setitem__(r, np.array(Lr)), real(b, fl, r, Lr))[1])
    return K.assess(book, FLAT, 1.0, Wn=Wn, Wp=Wp), got


def test_default_pension_is_zero_and_changes_nothing(monkeypatch):
    a, b = K.Book(2, {'A': 100.0, 'C': 50.0}), K.Book(2, {'A': 100.0, 'C': 50.0})
    assert not a.pen.any() and not a.penp.any() and a.pen.shape == (2,)
    b.pen, b.penp = np.zeros(2), np.zeros(2)
    Wn, Wp = {'A': np.full(2, 120.0), 'C': np.full(2, 40.0)}, {'A': np.full(2, 100.0), 'C': np.full(2, 50.0)}
    (fa, ga), (fb, gb) = assess_with(a, Wn, Wp, monkeypatch), assess_with(b, Wn, Wp, monkeypatch)
    assert np.array_equal(fa.L, fb.L) and all(np.array_equal(ga[r], gb[r]) for r in ga) and np.array_equal(a.paid, b.paid)


def test_a_pension_delta_enters_the_base_and_the_tax_follows_route_value_when_no_route_grew(monkeypatch):
    b = K.Book(1, {'A': 100.0, 'C': 100.0})
    b.pen = np.array([80.0])                                               # pension up 80; routes down 10 and 20: every route delta is non-positive
    fl, Lr = assess_with(b, {'A': np.array([90.0]), 'C': np.array([80.0])}, {'A': np.array([100.0]), 'C': np.array([100.0])}, monkeypatch)
    assert fl.delta[0] == pytest.approx(50.0) and fl.L[0] == pytest.approx(5.0)               # W_new 250, W_prev 200
    assert sum(Lr.values())[0] == pytest.approx(fl.L[0], rel=1e-12) and Lr['A'][0] / Lr['C'][0] == pytest.approx(90 / 80)   # by route value (declared), not lost
    assert b.R['A']['f'][0] < 1.0 and b.R['C']['f'][0] < 1.0 and b.pen[0] == 80.0          # the routes paid; the pension was not sold


def test_with_a_route_delta_positive_the_weights_are_the_route_deltas_as_before(monkeypatch):
    b = K.Book(1, {'A': 100.0, 'C': 100.0})
    b.pen, b.penp = np.array([30.0]), np.array([10.0])
    fl, Lr = assess_with(b, {'A': np.array([120.0]), 'C': np.array([90.0])}, {'A': np.array([100.0]), 'C': np.array([100.0])}, monkeypatch)
    assert sum(Lr.values())[0] == pytest.approx(fl.L[0], rel=1e-12) and 'C' not in Lr     # only the route that grew carries the tax


def test_a_pension_fall_is_refunded_as_a_loss_at_the_rate(monkeypatch):
    b = K.Book(1, {'A': 100.0})
    b.pen, b.penp = np.array([0.0]), np.array([50.0])                      # pension down 50, route unchanged
    fl, Lr = assess_with(b, {'A': np.array([100.0])}, {'A': np.array([100.0])}, monkeypatch)
    assert fl.delta[0] == -50.0 and fl.L[0] == pytest.approx(-5.0) and Lr['A'][0] == pytest.approx(-5.0)    # allocated as a loss (the cap on what was paid is _route_tax's)


def test_rebase_sets_the_pension_basis_and_the_pension_alone_is_assessed_without_a_route():
    b = K.Book(2, {'A': 100.0})
    b.pen = np.array([10.0, 0.0])
    K.rebase(b)
    assert np.array_equal(b.penp, [10.0, 0.0]) and b.penp is not b.pen
    b.pen = np.array([30.0, 0.0])
    L = K.assess(b, FLAT, 1.0).L
    assert L[0] == pytest.approx(2.0) and L[1] == 0.0        # 0.1 x 20 on the line whose pension grew; none on the other


@pytest.mark.parametrize('route', ['A', 'B', 'C'])
def test_a_payment_above_what_the_line_holds_is_capped_and_reported_never_raised(route):
    b = K.Book(2, {route: 100.0})
    b.pen = np.array([300.0, 20.0])                                        # line 0: the pension grew by 3x its units, tax 150 > 100 held; line 1: 10 < 100 held
    K.assess(b, lambda x: np.full(np.shape(x), 0.5), 1.0)
    f = b.R[route]['f']
    assert f[0] == pytest.approx(0.0) and f[1] == pytest.approx(0.9) and (f >= 0).all()            # the first pays all it holds, not more
    assert b.unpaid_B[0] == pytest.approx(50.0) and b.unpaid_B[1] == 0.0 and K.shortfall_lines(b) == 1
    assert b.pen[0] == 300.0 and b.check()['units'] < 1e-9                 # the pension is not sold


def test_no_shortfall_without_a_pension_over_several_years():
    b = K.Book(3, {'A': 100.0, 'C': 60.0, 'D': 40.0}, has_cv=True)
    for g in (0.3, -0.2, 0.5, 0.1):
        K.step_year(b, lambda x: np.full(np.shape(x), 0.9), 1.0, g, 0.02)
    assert K.shortfall_lines(b) == 0 and not b.unpaid_B.any()
