#!/usr/bin/env python3
"""array_pass_micro.py -- the three micro-tests of brief 189c (no model code changed): builtin sum vs a left-to-right add, _div as np.where vs np.divide(where=), and burden.m2's masks with the association changed.
    python -I model/studies/run-cost/array_pass_micro.py
Sizes: 280 and 14,000 elements (20 and 1,000 paths); best of 5 repeats; `identical` is a byte comparison of the results."""
import os
os.environ.setdefault('NPY_DISABLE_CPU_FEATURES', 'X86_V4')
import timeit
import numpy as np

rng = np.random.default_rng(1)
t = lambda f, n: min(timeit.repeat(f, number=n, repeat=5)) / n * 1e6


def asum(xs):
    t_ = xs[0] + xs[1]
    for x in xs[2:]:
        t_ = t_ + x
    return t_


def d0(a, b):
    return np.where(b > 0.0, a / np.where(b > 0.0, b, 1.0), 0.0)


def d1(a, b):
    return np.divide(a, b, out=np.zeros(np.broadcast(a, b).shape), where=b > 0.0)


for n in (280, 14000):
    xs = [rng.random(n) for _ in range(4)]
    a, b = rng.normal(size=n), rng.normal(size=n); b[::5] = 0.0
    print(f'{n:6d} sum {t(lambda: sum(xs), 2000):7.2f} us  asum {t(lambda: asum(xs), 2000):7.2f} us  identical {sum(xs).tobytes() == asum(xs).tobytes()}')
    print(f'{n:6d} _div where {t(lambda: d0(a, b), 2000):7.2f} us  divide(where=) {t(lambda: d1(a, b), 2000):7.2f} us  identical {d0(a, b).tobytes() == d1(a, b).tobytes()}')

Y, P, L = 100, 1000, 12
net, w0 = rng.normal(size=(Y, P, L)), rng.random((Y, P, L)); w0[w0 < .1] = 0
wt, win = rng.random(P)[None, :, None], rng.random((Y, 1, L)) > .3
def m_a():
    m = win & (net > 0) & (w0 > 0)
    return np.where(m, wt * net ** 2 / np.where(w0 > 0, w0, 1.0), 0.0)
def m_b():
    pos = w0 > 0; m = win & (net > 0) & pos
    return np.where(m, (net * wt) * net / np.where(pos, w0, 1.0), 0.0)
print(f'm2 numerator (shape {Y}x{P}x{L}): as written {t(m_a, 5) / 1e3:.1f} ms  fewer passes {t(m_b, 5) / 1e3:.1f} ms  identical {m_a().tobytes() == m_b().tobytes()}')
