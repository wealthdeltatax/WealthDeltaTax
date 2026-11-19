"""
returns.py -- the return generator (level 1) and the parameter draw (level 2)
===========================================================================
Layer L1 (architecture.md 5.1). Imports numpy and the Row type of core/pack.py only. No file is read and nothing runs at import
(R8). No country appears here (R11): the pack and the register rows arrive as arguments.

CONVENTIONS (R6)
----------------
Parameters and sample statistics are in percent a year, as the register prints them. Paths are real annual ARITHMETIC returns as
fractions (0.05 is 5%), shape (T, paths): V -> V (1 + g), the kernel's input. The real return is (1 + capital_tr) / (1 + CPI
inflation) - 1 from the pack's returns table, for each year whose own return and own and previous CPI are present (so 1940 to
1946, absent in JST, are not observations; 117 of 1896 to 2019). The lag-1 autocorrelation is the sample one over the series in
order, as model v2 computed it; it pairs 1939 with 1947 and the bootstrap does not (it wraps inside each contiguous segment).
Level 1: AR(1) with normal innovations, arithmetic mean m, marginal SD s, lag-1 phi, innovation SD s sqrt(1 - phi^2), stationary
start. Level 2: mean, SD and phi are independent, normal about the register central with the standard error that makes the
register's low and high the 10th and 90th percentiles; a Latin hypercube sample. No draw is clipped: a return at or below -100%,
an SD at or below 0 or |phi| >= 1 raises (R7).
"""

from __future__ import annotations

import numpy as np

SEED = 20261118
STREAMS = ('level1_paths', 'level2_draws', 'bootstrap_check', 'welfare_risk', 'tornado_crn')   # appended to, never reordered


def streams(seed=SEED):
    """The five named generators of architecture.md 3.1: SeedSequence(seed).spawn(5), in the fixed order."""
    return {k: np.random.default_rng(s) for k, s in zip(STREAMS, np.random.SeedSequence(seed).spawn(len(STREAMS)))}


def real_series(pack):
    """(years, real returns in percent) of the pack's returns table, usable years only."""
    cap, cpi = (np.array([np.nan if r[c] is None else r[c] for r in pack.tables['returns']]) for c in ('capital_tr', 'cpi'))
    years = np.array([r['year'] for r in pack.tables['returns']])
    ok = np.isfinite(cap[1:]) & np.isfinite(cpi[1:]) & np.isfinite(cpi[:-1]) & (np.diff(years) == 1)
    return years[1:][ok], 100 * ((1 + cap[1:][ok] / 100) / (cpi[1:][ok] / cpi[:-1][ok]) - 1)


def sample_stats(r):
    """n, arithmetic and geometric mean, SD (n - 1), lag-1 autocorrelation and effective sample of a series in percent."""
    d = r - r.mean()
    rho = float((d[:-1] * d[1:]).sum() / (d * d).sum())
    return {'n': len(r), 'arithmetic': float(r.mean()), 'geometric': float(100 * np.expm1(np.log1p(r / 100).mean())),
            'sd': float(r.std(ddof=1)), 'lag1': rho, 'n_eff': len(r) * (1 - rho) / (1 + rho)}


def _checked(g):
    if (g <= -1).any():
        raise ValueError(f'a generated return of {100 * g.min():.1f}% is at or below -100%: not clipped, the parameters are wrong')
    return g


def ar1_paths(rng, mean, sd, phi, T, paths):
    """Level 1: (T, paths) real arithmetic returns (fractions) from an AR(1) with normal innovations, stationary start."""
    if sd <= 0 or abs(phi) >= 1:
        raise ValueError(f'sd {sd} must be positive and |phi| {phi} below 1')
    x = np.empty((T, paths))
    x[0] = rng.standard_normal(paths)
    for t in range(1, T):
        x[t] = phi * x[t - 1] + np.sqrt(1 - phi * phi) * rng.standard_normal(paths)
    return _checked((mean + sd * x) / 100)


def block_bootstrap(rng, years, r, T, paths, mean_block=3.0):
    """Check: stationary block bootstrap of the sample r (percent) as (T, paths) fractions; a block runs on to the next year and
    wraps to the first year of its own contiguous segment, and ends with probability 1 / mean_block."""
    brk = np.flatnonzero(np.diff(years) != 1)
    first = np.repeat(np.r_[0, brk + 1], np.diff(np.r_[0, brk + 1, len(r)]))
    last = np.repeat(np.r_[brk, len(r) - 1], np.diff(np.r_[0, brk + 1, len(r)]))
    pos, out = rng.integers(0, len(r), paths), np.empty((T, paths))
    for t in range(T):
        out[t] = r[pos]
        new = rng.random(paths) < 1 / mean_block
        pos = np.where(new, rng.integers(0, len(r), paths), np.where(pos == last[pos], first[pos], pos + 1))
    return out / 100


def _ppf(u):
    """Inverse of the standard normal distribution function (Acklam's rational approximation, relative error 1e-9)."""
    a = (-39.69683028665376, 220.9460984245205, -275.9285104469687, 138.3577518672690, -30.66479806614716, 2.506628277459239)
    b = (-54.47609879822406, 161.5858368580409, -155.6989798598866, 66.80131188771972, -13.28068155288572)
    c = (-0.007784894002430293, -0.3223964580411365, -2.400758277161838, -2.549732539343734, 4.374664141464968, 2.938163982698783)
    d = (0.007784695709041462, 0.3224671290700398, 2.445134137142996, 3.754408661907416)
    u = np.asarray(u, float)
    q = np.where(u < 0.5, u, 1 - u)
    lo = np.sqrt(-2 * np.log(np.minimum(q, 0.02425)))
    tail = np.polyval(c, lo) / np.polyval(d + (1,), lo)
    m = q - 0.5
    mid = np.polyval(a, m * m) * m / np.polyval(b + (1,), m * m)
    z = np.where(q < 0.02425, tail, mid)   # the lower-half value, negative
    return np.where(u < 0.5, z, -z)


def level2_draw(rng, rows, n):
    """Level 2: n Latin hypercube draws (mean, sd, phi) as {'mean', 'sd', 'phi'} arrays; `rows` maps each of the three names to a
    register Row whose low and central and high are the 10th, 50th and 90th percentiles."""
    z90 = float(_ppf(0.9))
    out = {}
    for k, row in rows.items():
        u = (rng.permutation(n) + rng.random(n)) / n
        out[k] = row.central + (row.high - row.low) / (2 * z90) * _ppf(u)
    if (out['sd'] <= 0).any() or (np.abs(out['phi']) >= 1).any():
        raise ValueError('a level 2 draw left the admissible region (sd > 0, |phi| < 1): not clipped')
    return out


def loop_windows(years, T, wrap=True):
    """Windows of length T over the usable years (ascending): with wrap every start is valid and a window that runs past the
    end continues from the first year; without it only windows that fit. Each: start, years, wraps, repeat, contiguous."""
    n, T = len(years), int(T)
    if n == 0 or T < 1:
        return []
    out = []
    for i in (range(n) if wrap else range(n - T + 1)):
        ys = [years[(i + k) % n] for k in range(T)]
        seam = i + T > n
        out.append({'start': years[i], 'years': ys, 'wraps': seam, 'repeat': T > n,
                    'contiguous': not seam and all(ys[k + 1] - ys[k] == 1 for k in range(T - 1))})
    return out
