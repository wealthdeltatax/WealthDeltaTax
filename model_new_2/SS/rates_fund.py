"""
rates_fund.py — RATES rebuild, L4 fund layer and headline metric
=================================================================
The fund is the state's accumulated in-kind stake.  It holds the asset, earns
the asset return, receives net WDT receipts (taxes less refunds, which are paid
in units out of the stake), and pays labour-tax relief once the reserves are full.

DEFINITIONS
-----------
A_t         trailing mean (default 5 years, incl. t) of max(net_t, 0): the income
            that the reserves are sized against.
SRR target  ms * A_t   ring-fenced; its job is to honour refunds.
LRR target  ml * A_t   a REACTION-TIME buffer: m years of the outlay that WDT
            income is funding, so the Governing Council has time to respond to
            a revenue collapse without failing a commitment already made.
            (Replaces "3 years of ALL government expenditure": the exact multiple
            is a parameter; its function is the buffer.)
Fill        S_pre >= (ms + ml) * A_t, where S_pre = S_{t-1}(1 + r_t) + net_t.
            LRR fill year = first such t.  Relief is zero until fill.

RELIEF AS A COMMITMENT (what gives the LRR a job)
-------------------------------------------------
After fill, each year:
    upkeep_t = max(0, T_total_t - S_{t-1}(1 + r_t))     growth the targets need
                                                       that returns do not supply
    Z_t      = net_t - upkeep_t                         surplus available for relief
    R*_t     = max(0, mean(Z over the last W post-fill years))     COMMITTED relief
    avail_t  = max(0, S_pre - SRR target)               what can be paid without
                                                       touching the ring-fence
    R_t      = min(R*_t, avail_t)                       relief actually paid
    S_t      = S_pre - R_t
W (default = ml) is the reaction time: a revenue fall lowers the commitment only
as the trailing average catches up, and the LRR carries the gap.

FAILURE EVENTS (first year each occurs, post-fill)
--------------------------------------------------
  unmet      R*_t > avail_t   a committed relief payment could not be made
                              without breaching the SRR ring-fence
  ring       S_pre < SRR target   ring-fence breached
  insolvent  S_pre < 0            the state cannot return the units it owes

Reserve return is (1 - safe_share) * r + safe_share * safe, with r the asset
return (the stake is held in kind, so safe_share = 0 is the default).

HEADLINE
--------
coverage = sum of relief paid over the H years after fill (default 10)
           / sum of government expenditure over the same years     (ratio of sums)
Censored (reported, not dropped) when fill + H exceeds the window.
The companion `cov_receipts` (net receipts / expenditure over the same years)
is an upper bound that ignores reserve upkeep.

All series are LEVELS in engine units; coverage ratios are scale-free.
"""

import numpy as np


def trailing_mean(x, window):
    """Trailing mean including the current element, over the available history."""
    x = np.asarray(x, float)
    c = np.cumsum(np.insert(x, 0, 0.0))
    idx = np.arange(1, len(x) + 1)
    lo = np.maximum(0, idx - window)
    return (c[idx] - c[lo]) / (idx - lo)


def run_fund(net, E, r, refund=None, safe=None, ms=3.0, ml=3.0, a_window=5,
             w_relief=None, safe_share=0.0, horizon=10):
    """
    net     (T,) net WDT receipts, level
    E       (T,) government expenditure, level (same units)
    r       (T,) asset return
    refund  (T,) refunds paid (negative or positive magnitude), level; optional,
            used only for the SRR-need diagnostic
    safe    (T,) safe-asset return; required if safe_share > 0
    """
    net = np.asarray(net, float)
    E = np.asarray(E, float)
    r = np.asarray(r, float)
    T = len(net)
    w_relief = max(1, int(round(ml if w_relief is None else w_relief)))
    a_window = max(1, int(a_window))
    if safe_share > 0.0:
        if safe is None:
            raise ValueError('safe returns required when safe_share > 0')
        rr = (1.0 - safe_share) * r + safe_share * np.asarray(safe, float)
    else:
        rr = r
    A = trailing_mean(np.maximum(net, 0.0), a_window)

    S = 0.0
    S_path = np.zeros(T); R = np.zeros(T); Rstar = np.zeros(T)
    filled = False
    fill_t = srr_fill = None
    unmet = ring = insolvent = None
    Z_hist = []
    buffer = np.full(T, np.nan)

    for t in range(T):
        Tsrr, Ttot = ms * A[t], (ms + ml) * A[t]
        S_pre = S * (1.0 + rr[t]) + net[t]
        if srr_fill is None and A[t] > 0.0 and S_pre >= Tsrr:
            srr_fill = t + 1
        if not filled:
            if A[t] > 0.0 and S_pre >= Ttot:
                filled, fill_t = True, t + 1
            S = S_pre
        else:
            upkeep = max(0.0, Ttot - S * (1.0 + rr[t]))
            Z_hist.append(net[t] - upkeep)
            Rstar[t] = max(0.0, float(np.mean(Z_hist[-w_relief:])))
            avail = max(0.0, S_pre - Tsrr)
            if Rstar[t] > avail + 1e-12 and unmet is None:
                unmet = t + 1
            if S_pre < Tsrr - 1e-12 and ring is None:
                ring = t + 1
            if S_pre < -1e-12 and insolvent is None:
                insolvent = t + 1
            R[t] = min(Rstar[t], avail)
            S = S_pre - R[t]
            buffer[t] = (S - Tsrr) / A[t] if A[t] > 0.0 else np.nan
        S_path[t] = S

    out = {'S': S_path, 'R': R, 'Rstar': Rstar, 'A': A, 'fill_year': fill_t,
           'srr_fill_year': srr_fill, 'unmet_year': unmet, 'ring_year': ring,
           'insolvent_year': insolvent, 'horizon': horizon, 'T': T}

    if fill_t is None or fill_t + horizon > T:
        out.update({'censored': True, 'coverage': np.nan, 'cov_receipts': np.nan,
                    'fail_in_window': None, 'min_buffer': np.nan})
    else:
        a, b = fill_t, fill_t + horizon          # python slice = years fill+1..fill+H
        sl = slice(a, b)
        win_years = range(a + 1, b + 1)
        out.update({
            'censored': False,
            'coverage': float(R[sl].sum() / E[sl].sum()),
            'cov_receipts': float(net[sl].sum() / E[sl].sum()),
            'fail_in_window': any(y is not None and y in win_years
                                  for y in (unmet, ring, insolvent)),
            'min_buffer': float(np.nanmin(buffer[sl])),
        })
    if refund is not None:
        ref = np.abs(np.asarray(refund, float))
        out['srr_need_mult'] = float((ref / np.where(A > 0, A, np.nan)).max()
                                     if np.isfinite(A).any() else np.nan)
    return out
