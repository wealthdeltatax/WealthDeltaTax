"""Brief 180c: the compiled household functions (core/kernel_jit.py) against the numpy ones. Skipped when numba is absent. The spike tolerance is 1e-9 relative; these functions have no exp, log or pow, so the test asks for bit equality."""
import numpy as np
import pytest

from model_v3.core import household as hh, kernel_jit as kj

pytestmark = pytest.mark.skipif(not kj.AVAILABLE, reason='numba not installed')
KEYS = ('property', 'net_financial', 'physical', 'pension', 'debt')


def pos(rng, n):
    return {k: (rng.normal(1.0, 1.5, n) if k != 'debt' else np.zeros(n)) for k in KEYS}      # negative balances included


def same(a, b):
    return np.array_equal(np.asarray(a), np.asarray(b)) and np.signbit(a).tolist() == np.signbit(b).tolist()


def test_year_matches_household_step():
    rng = np.random.default_rng(5)
    for _ in range(20):
        n = 37
        q = pos(rng, n)
        fl = dict(Y_L=rng.uniform(0, 2, n), C=rng.uniform(0, 1, n), pen_in=rng.uniform(0, .2, n))
        g = {k: rng.normal(0.02, .1, n) for k in KEYS[:4]}
        kw = dict(sink='net_financial', source_weights=dict(property=1.0))
        a, acct = hh.household_step('t', q, fl, dict(g=g), dict(cpi=0.0, hfce=0.0), 'A', **kw)
        d = kj._year_A(*(np.ascontiguousarray(x) for x in (q['property'], q['net_financial'], q['physical'], q['pension'], fl['Y_L'], fl['C'], fl['pen_in'], g['property'], g['net_financial'], g['physical'], g['pension'])))
        for k, x in zip(KEYS[:4], d[:4]):
            assert same(a[k], x), k
        assert same(acct['S'], d[4]) and same(acct['CG'], d[5]) and d[6] <= 1e-9


def test_pay_matches_apply_payment():
    rng = np.random.default_rng(6)
    for _ in range(20):
        n = 41
        q = pos(rng, n)
        T = rng.normal(0.2, 0.8, n)
        w = {k: np.maximum(q[k], 0.0) for k in KEYS[:3]}
        a, _, un = hh.apply_payment(q, T, w)
        o = kj._pay(q['property'], q['net_financial'], q['physical'], T, *w.values())
        for k, x in zip(KEYS[:3], o[:3]):
            assert same(a[k], x), k
        assert same(un, o[3])
