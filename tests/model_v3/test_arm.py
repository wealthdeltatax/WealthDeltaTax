"""Brief 114c (W2): the kernel hook and the legacy hook. step_year(hook=None) and a hook that returns (g, -c) give equal books to 0.0 (not a tolerance); a
negative `sold` (a buy) keeps f + s + sold = tot."""
import itertools

import numpy as np

from model_v3.core import kernel as K
from model_v3.core import schedule as S

RATE = S.rate_function(k=0.001, tau_0=0.15, tau_m=0.70, W_min=2.0)
V0 = {'A': np.array([40.0, 90.0, 400.0]), 'B': np.array([30.0, 50.0, 100.0]), 'C': np.array([30.0, 60.0, 200.0]), 'D': np.array([20.0, 40.0, 100.0])}


class Hook:
    """What LegacyHook(c) must do: the growth rate unchanged, the share -c, nothing after settlement."""
    def __init__(self, c):
        self.c = c

    def pre(self, book, t, g):
        return g, -self.c

    def post(self, book, fl):
        pass


def snap(book, ops):
    """Every array the year leaves: the routes, the state's and the family's value, the payer record, and the flows of each op."""
    out = [x[k] for r, x in sorted(book.R.items()) for k in sorted(x)]
    out += [book.family_true(), book.state_true(), book.paid, book.refunded, book.E_cash, book.LB]
    out += [np.asarray(v) for _, fl in ops for k, v in sorted(vars(fl).items()) if not isinstance(v, dict)]
    out += [np.asarray(v) for _, fl in ops for k, d in sorted(vars(fl).items()) if isinstance(d, dict) for _, v in sorted(d.items())]
    return out


def test_hook_none_equals_the_legacy_hook_to_zero_on_a_grid_of_c_and_g():
    for c, g in itertools.product((0.0, 0.015, 0.035, 0.2), (-0.3, 0.0, 0.04, 0.5)):
        books = [K.Book(3, V0, alpha0={'C': 1.1, 'D': 1.2}) for _ in range(2)]
        ops = [K.step_year(books[0], RATE, 1.0, np.full(3, g), c, 1.1, 1.2),
               K.step_year(books[1], RATE, 1.0, np.full(3, g), 99.0, 1.1, 1.2, hook=Hook(c), t=1)]      # `consumption` is ignored under a hook
        assert all(np.array_equal(a, b) for a, b in zip(snap(books[0], ops[0]), snap(books[1], ops[1]))), (c, g)


def test_a_driver_run_with_the_hook_equals_the_run_without_to_zero():
    g, books = np.tile(np.array([0.05, -0.1, 0.03, 0.08, 0.0, 0.02] * 5)[:, None], (1, 3)), []
    for kw in ({'consumption': 0.03}, {'consumption': 0.0, 'hook': Hook(0.03)}):
        books.append(K.run_lines(RATE, g, V0, G=10, alpha_C=1.1, alpha_D=1.2, lam_C=0.05, **kw))
    assert all(np.array_equal(books[0].R[r][k], books[1].R[r][k]) for r in books[0].R for k in books[0].R[r]) and np.array_equal(books[0].paid, books[1].paid)


def test_a_negative_sold_keeps_the_unit_invariant_and_a_buy_raises_the_family_value():
    b = K.Book(2, {'A': np.array([100.0, 50.0])})
    fl = K.grow_and_consume(b, 0.1, 0.0, share=np.array([0.2, -0.1]))        # line 0 buys 20% of its units, line 1 sells 10%
    x = b.R['A']
    assert x['sold'][0] < 0 < x['sold'][1] and b.check()['units'] < 1e-12
    assert np.allclose(x['f'], [1.2, 0.9]) and np.allclose(fl.consumed['A'], [-22.0, 5.5])      # true values: -0.2 x 110, 0.1 x 55
