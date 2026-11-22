"""
revenue.py -- revenue lines, the fund and the horizon windows (model v3, stage V3-7)
===================================================================================
Layer L3 (architecture.md 5.1). Imports numpy, core/pack.py and core/kernel.py. No file is read and nothing runs at import (R8). No country
or tax is named here (R11): the pack, the base, the rate function and the retirement lines arrive as arguments.

CONVENTIONS (R6, and the sign of revenue, stage-c-decisions.md item 2)
---------------------------------------------------------------------
Flows are billions of pounds in real prices, arrays (T, P): year 1 to T down, path across. Shares are percent of GDP of the same year.
Every line is positive when it is a receipt to the state; M1c can be negative; M1 = M1a + M1b + M1c - M1d is never floored or clipped.
A line is a representative adult of the base; each is run in `n_phase` death phases (first deaths at ceil(i G / n_phase), then every G
years), as v2's `run_cohorts`; phases and paths are folded into the kernel's line axis, so one call runs all paths.
GDP in year t is the pack's GDP times the cumulated real GDP-per-head growth (population fixed). Wealth is real money; the threshold is
indexed by `index`: 'gdp_pc' (W_min moves with GDP per head) or 'none'.

THE FUND (rewritten from rates_core.run_fund 1109-1193, not ported)
-------------------------------------------------------------------
S_pre = S (1 + r) + net. A = trailing mean of max(net, 0) over `a_window` years, short target ms A, total target (ms + ml) A. Relief is zero until
S_pre reaches the total target (the fill year f). After: upkeep = max(0, total - S (1 + r)); R* = max(0, mean of net - upkeep over the last
ml post-fill years); R = min(R*, max(0, S_pre - ms A)); S = S_pre - R. Relief R = M1a + M1b + M1c, so M1c = S(-1) r - (S - S(-1)): fund
income less the growth the reserves keep. A path with no fill by year `unfilled_after` is unfilled (P1 = T, left out of short-window statistics).

M1d, P3, P5: the retired taxes. Taxes are retired in ascending order of receipts; one is retired in the first year after the fill in which relief
net of the receipts already retired covers its receipts (several may be, in one year). P3 sums, over years, the excess of retired receipts over
relief: staged retirement keeps it zero at each retirement, and a later fall in relief shows as a positive P3, reported, not hidden.
"""

from __future__ import annotations

import numpy as np

from model_v3.core import kernel as K
from model_v3.core import pack as pk



def gdp_growth(pack, years):
    """Real GDP-per-head growth of each calendar year in `years` (any shape), from the pack's returns table."""
    ys, v = pk.series(pack, 'gdp_pc')
    g = np.r_[np.nan, v[1:] / v[:-1] - 1]
    years = np.asarray(years)
    out = g[years - ys[0]]
    if (years < ys[1]).any() or (years > ys[-1]).any() or np.isnan(out).any():
        raise ValueError('gdp_pc: a year is outside the pack or has no previous year')
    return out


_CLASSES = ('property', 'net_financial', 'physical')                                  # the ledger's household classes (the safe asset is added in revenue()); the pension is not one


def _value(fl, n):
    """True value moved family -> state by one operation, per line (units at the true price plus income cash)."""
    return sum(fl.value.values()) + fl.income if fl.value else fl.income + np.zeros(n)


def run_lines(base, rate_fn, g, gdp_g, c, lam_C=0.0, lam_D=0.0, G=30, n_phase=6, index='gdp_pc', routes=None, death_verify=False, hook=None, **book_kw):
    """The kernel over every path and phase. g and gdp_g are (T, P) real returns and GDP-per-head growth; c is the consumption share of
    wealth (read when `hook` is None; otherwise the hook of runner/arm.py carries the year, kernel.step_year); routes overrides the base's V0 by route (a dict of arrays). Returns billions-of-pounds flows (T, P): tax and refund (the year's
    assessments, split by sign per line; assessed is the tax assessed on gains before the routes settle it), death_tax (the assessments a death triggers: Route C verified, Route D auctioned), heir, death_B (a deferred balance
    settled), death_D, and the payer record: payers, entries, exits
    (thousands of adults), fall_through (refunds to those who left the base), wbase (start-of-year wealth of the lines taxed this year, those at or
    above W_min after growth) and wtau (the same weighted by the marginal rate at the new wealth). `gdp_index` is GDP over its base-year value and `adults_k` the thousands of adults."""
    g, gdp_g = np.asarray(g, float), np.asarray(gdp_g, float)
    T, P = g.shape
    L = len(base.labels)
    n = P * L
    A = base.adults_k.sum()                       # thousands of adults x millions of pounds per adult = billions of pounds
    w = base.weights / n_phase
    yy = np.cumprod(1.0 + gdp_g, axis=0)
    idx = yy if index == 'gdp_pc' else np.ones_like(yy)
    V0 = {r: np.tile(v, P) for r, v in (routes or base.V0).items()}
    hh = hook is not None and hook.household                                           # the household arm keeps the public ledger (120c)
    keys = ('assessed', 'tax', 'refund', 'death_tax', 'heir', 'death_B', 'death_D', 'payers', 'entries', 'exits', 'fall_through', 'wbase', 'wtau') + (('wgain',) if hook is not None else ()) + (tuple('rc_' + k for k in _CLASSES) if hh else ())
    out = {k: np.zeros((T, P)) for k in keys}
    agg = lambda x, ww=w: (ww[None, :] * x.reshape(P, L)).sum(axis=1) * A
    cnt = lambda m: (base.adults_k[None, :] * m.reshape(P, L)).sum(axis=1) / n_phase
    wmin = base.w_min
    has_cv = (lam_C > 0.0 or death_verify) and 'C' in V0 and np.any(V0['C'] > 0.0)
    for i in range(n_phase):
        ph = int(np.ceil((i + 1) * G / n_phase))
        book = K.Book(n, V0, alpha0={'C': 1.0, 'D': 1.0}, has_cv=has_cv, **book_kw)
        book.ledger = {k: np.zeros(n) for k in _CLASSES} if hh else None                 # per line, the state's stake by class: state_true and the refund cap read it
        prev = np.ones(n, bool) & (np.tile(base.wealth, P) >= wmin)
        for t in range(1, T + 1):
            il = np.repeat(idx[t - 1], L)
            W0 = book.family_true() + book.pen                                          # the assessed base: units plus the pension balance (zero in the legacy arm)
            pay = W0 >= wmin * il
            gr = np.repeat(g[t - 1], L)
            pt, xv, hv, lv, dv, ass = (np.zeros(n) for _ in range(6))
            for kind, fl in K.step_year(book, rate_fn, il, gr, c, 1.0, 1.0, lam_C, lam_D, False, hook, t):
                if kind == 'tax':
                    pt += _value(fl, n)
                    ass = np.where(fl.L > 0, fl.L, 0.0)                                   # assessed, before routes: Route D accrues, C pays in kind
            if t < T and t >= ph and (t - ph) % G == 0:
                for kind, fl in K.step_death(book, rate_fn, il, death_verify):
                    v = _value(fl, n)
                    if kind in ('tax_death_C', 'tax_death'):
                        xv += v
                    elif kind == 'tax_heir':
                        hv += v
                    elif kind == 'death_B':
                        lv += v
                    elif kind == 'death_D':
                        dv += v
                if hook is not None:
                    hook.reconcile(book)                                                    # a death's payments are made in the year they occur (120c), not at the next year's opening
            if t == T and hh:                               # the household arm settles Route D and B at the horizon, in its last year (120c); the legacy arm and its hook do not
                for kind, fl in K.settle_terminal(book):
                    if kind == 'terminal_D':
                        dv += _value(fl, n)
                    else:
                        lv += _value(fl, n)
                hook.reconcile(book)
            W1 = W0 * (1.0 + gr) * (1.0 - c) if hook is None else hook.grown(W0, gr)   # wealth after growth and flow, before tax (read after the year: the household hook sets it in the step)
            pay1 = W1 >= wmin * il
            rate1 = np.asarray(rate_fn(W1 / il), float)                                    # the kernel reads the rate at the new wealth
            pt = np.where(np.abs(pt) < 1e-12, 0.0, pt)
            tt = t - 1
            out['assessed'][tt] += agg(ass)
            out['tax'][tt] += agg(np.where(pt > 0, pt, 0.0))
            out['refund'][tt] += agg(np.where(pt < 0, pt, 0.0))
            out['death_tax'][tt] += agg(xv)
            out['heir'][tt] += agg(hv)
            out['death_B'][tt] += agg(lv)
            out['death_D'][tt] += agg(dv)
            out['payers'][tt] += cnt(pay)
            out['entries'][tt] += cnt(pay & ~prev)
            out['exits'][tt] += cnt(prev & ~pay)
            out['fall_through'][tt] += agg(np.where((pt < 0) & prev & ~pay, -pt, 0.0))
            out['wbase'][tt] += agg(np.where(pay1, W0, 0.0))
            out['wtau'][tt] += agg(np.where(pay1, W0 * rate1, 0.0))
            if hook is not None:                                                           # the pre-tax gain the rate applies to, by line (the identity's I3 reads it under the household hook)
                out['wgain'][tt] += agg(np.where(pay1 & (W0 > 0), rate1 * np.maximum(W1 - W0, 0.0), 0.0))
            if hh:
                rc, rk = hook.receipts(), hook.class_returns()
                for k in _CLASSES:
                    book.ledger[k] = book.ledger[k] * (1.0 + rk[k]) + rc[k]
                    out['rc_' + k][tt] += agg(rc[k])
            prev = pay
    led = dict(rc={k: out.pop('rc_' + k) for k in _CLASSES}, rk={k: np.full((T, P), r) for k, r in hook.class_returns().items()}) if hh else None
    return {**out, 'gdp_index': yy, 'adults_k': A, **({'ledger': led} if hh else {})}


def fund(net, E, r, ms=3.0, ml=3.0, a_window=5, safe=None, safe_share=0.0, unfilled_after=90, led=None):
    """The reserves, paths across (T, P): net receipts into the fund, expenditure E, asset return r (fractions). Returns S, R, A, the target of the
    short reserve `srr`, the fill year (1-based, 0 = never, or later than `unfilled_after`: unfilled), the short fill year, and the first year of each
    failure event (0 = none): unmet (R* above what is available), ring (the short reserve breached), insolvent (S_pre below zero).
    `led` (120c, the public ledger of the household arm): {'rc': receipts by class, 'rk': returns by class}, each (T, P); the balance is the class balances, the return their weighted return (`r` is not read),
    the payout comes out of the classes pro rata, and S, rr and the class balances, returns and payouts are read from it."""
    net = np.asarray(net, float)
    T, P = net.shape
    if led is None:
        r = np.asarray(r, float)
    if led is None and safe_share > 0.0:
        if safe is None:
            raise ValueError('safe returns are needed when safe_share > 0')
        r = (1.0 - safe_share) * r + safe_share * np.asarray(safe, float)
    w = max(1, int(round(ml)))
    c = np.vstack([np.zeros((1, P)), np.cumsum(np.maximum(net, 0.0), axis=0)])
    i = np.arange(1, T + 1)[:, None]
    lo = np.maximum(0, i - max(1, int(a_window)))
    A = (c[i, np.arange(P)] - c[lo, np.arange(P)]) / (i - lo)
    S, Sp = np.zeros((T, P)), np.zeros(P)
    R, Z = np.zeros((T, P)), np.zeros((T, P))
    fill, srr_fill = np.zeros(P, int), np.zeros(P, int)
    ev = {k: np.zeros(P, int) for k in ('unmet', 'ring', 'insolvent')}
    if led is not None:
        Lk, cl, ret, pay, r = {k: np.zeros(P) for k in led['rc']}, {}, {}, {}, np.zeros((T, P))
        for d in (cl, ret, pay):
            d.update({k: np.zeros((T, P)) for k in Lk})
    for t in range(T):
        tsrr, ttot = ms * A[t], (ms + ml) * A[t]
        gro = Sp * (1.0 + r[t]) if led is None else sum(Lk[k] * (1.0 + led['rk'][k][t]) for k in Lk)
        pre = gro + net[t]
        srr_fill = np.where((srr_fill == 0) & (A[t] > 0) & (pre >= tsrr), t + 1, srr_fill)
        done = fill > 0
        newly = ~done & (A[t] > 0) & (pre >= ttot)
        Z[t] = np.where(done, net[t] - np.maximum(0.0, ttot - gro), 0.0)
        lo_t = np.maximum(fill, t - w + 1)                                       # post-fill years are fill .. t (0-based)
        cz = np.cumsum(np.vstack([np.zeros((1, P)), Z[:t + 1]]), axis=0)
        k = np.maximum(t + 1 - lo_t, 1)
        rstar = np.where(done, np.maximum(0.0, (cz[t + 1, np.arange(P)] - cz[lo_t, np.arange(P)]) / k), 0.0)
        avail = np.maximum(0.0, pre - tsrr)
        for name, m in (('unmet', rstar > avail + 1e-12), ('ring', pre < tsrr - 1e-12), ('insolvent', pre < -1e-12)):
            ev[name] = np.where(done & (ev[name] == 0) & m, t + 1, ev[name])
        R[t] = np.where(done, np.minimum(rstar, avail), 0.0)
        if led is None:
            Sp = pre - R[t]
        else:
            r[t] = np.where(Sp > 0, sum(Lk[k] * led['rk'][k][t] for k in Lk) / np.where(Sp > 0, Sp, 1.0), 0.0)
            for k in Lk:
                ret[k][t], lp = Lk[k] * led['rk'][k][t], Lk[k] * (1.0 + led['rk'][k][t]) + led['rc'][k][t]
                pay[k][t] = np.where(pre > 0, R[t] * lp / np.where(pre > 0, pre, 1.0), 0.0)
                Lk[k], cl[k][t] = lp - pay[k][t], lp - pay[k][t]
            Sp = sum(Lk.values())
        S[t] = Sp
        fill = np.where(newly, t + 1, fill)
    unfilled = (fill == 0) | (fill > unfilled_after)
    return {'S': S, 'R': R, 'A': A, 'rr': r, 'srr': ms * A, 'fill': fill, 'srr_fill': srr_fill, 'unfilled': unfilled, **{k + '_year': v for k, v in ev.items()}, **({} if led is None else {'L': cl, 'ret': ret, 'pay': pay, 'rc': led['rc']})}


def taxes(pack, lines, parts):
    """Retired taxes from the pack: {tax: receipts as percent of GDP}. A line that is a member of a part is merged into the part's tax; sorted ascending."""
    parent = {m: p for p, ms in parts.items() for m in ms}
    rec = {}
    for ln in lines:
        rows = pk.lookup(pack, 'receipts', line=ln)
        if len(rows) != 1:
            raise ValueError(f'receipts: line {ln!r} has {len(rows)} rows, one expected')
        rec[parent.get(ln, ln)] = rec.get(parent.get(ln, ln), 0.0) + rows[0]['pct_gdp']
    return dict(sorted(rec.items(), key=lambda kv: kv[1]))


def retire(relief, fill, rec):
    """Staged retirement. relief (T, P) percent of GDP, fill the fund's fill years (1-based, 0 = never), rec the receipts in ascending order.
    Returns M1d (T, P) and the retirement year of each tax (P, K), 0 = never."""
    T, P = relief.shape
    r = np.array(list(rec.values()), float)
    done, yr, m1d = np.zeros((P, len(r)), bool), np.zeros((P, len(r)), int), np.zeros((T, P))
    for t in range(T):
        live = (fill > 0) & (t + 1 > fill)
        for k in range(len(r)):
            cover = relief[t] - (done * r).sum(axis=1) >= r[k]
            go = live & ~done[:, k] & cover & (done[:, :k].all(axis=1) if k else True)
            done[:, k] |= go
            yr[go, k] = t + 1
        m1d[t] = (done * r).sum(axis=1)
    return m1d, yr


def window_mean(x, gdp, lo, hi):
    """Ratio of sums of a share x over years lo..hi (1-based, per path arrays), weighted by GDP; nan where the window is empty or beyond T."""
    T, P = x.shape
    t = np.arange(1, T + 1)[:, None]
    m = (t >= lo[None, :]) & (t <= hi[None, :]) & (hi[None, :] <= T) & (lo[None, :] >= 1)
    den = (gdp * m).sum(axis=0)
    return np.where(den > 0, (x * gdp * m).sum(axis=0) / np.where(den > 0, den, 1.0), np.nan)


def revenue(run, gdp0, levy, rec, g, E_pct, c, a_window=5, ms=3.0, ml=3.0, horizon=10, safe=None, safe_share=0.0, unfilled_after=90):
    """All the lines of one run. `run` is run_lines' result, gdp0 the base-year GDP (billions), levy the corporate levy (percent of GDP, constant),
    rec the retired taxes' receipts (taxes()), g the (T, P) real returns, E_pct reference expenditure over GDP (percent), c consumption. Percent of GDP unless
    named otherwise: M1a, M1b, M1c, M1d, M1 (= M1a + M1b + M1c - M1d), B1a to B1d, the fund (S, R, fill), P1, P3 to P7b, and the short and long windows."""
    T, P = g.shape
    gdp = run['gdp_index'] * gdp0
    wdt = run['tax'] + run['refund'] + run['death_tax'] + run['heir'] + run['death_B'] + run['death_D']
    lev = levy / 100.0 * gdp
    led = run.get('ledger')
    if led is not None:                                                                  # the public ledger (120c): the levy enters as cash, safe_share of it in the safe asset and the rest as net financial
        if safe_share > 0.0 and safe is None:
            raise ValueError('safe returns are needed when safe_share > 0')
        led = dict(rc={**led['rc'], 'net_financial': led['rc']['net_financial'] + (1.0 - safe_share) * lev, 'safe': safe_share * lev}, rk={**led['rk'], 'safe': np.zeros((T, P)) if safe is None else np.asarray(safe, float)})
    f = fund(wdt + lev, E_pct / 100.0 * gdp, g, ms, ml, a_window, safe, safe_share, unfilled_after, led)
    S, Sp = f['S'], np.vstack([np.zeros((1, P)), f['S'][:-1]])
    m1a, m1b, m1c = 100 * wdt / gdp, np.full((T, P), float(levy)), 100 * (Sp * f['rr'] - (S - Sp)) / gdp
    relief = m1a + m1b + m1c
    m1d, years = retire(relief, f['fill'], rec)
    m1 = m1a + m1b + m1c - m1d
    t = np.arange(1, T + 1)[:, None]
    fl, ok = f['fill'], ~f['unfilled']
    short = window_mean(m1, gdp, fl + 1, fl + horizon)
    short = np.where(ok, short, np.nan)
    ones = np.ones(P, int)
    long_ = window_mean(m1, gdp, 51 * ones, T * ones)
    after = (t > fl[None, :]) & (fl[None, :] > 0)
    below = after & (m1 < 0)
    lres = (S - f['srr']) / (ml * np.where(f['A'] > 0, f['A'], np.nan))
    out = {'M1a': m1a, 'M1b': m1b, 'M1c': m1c, 'M1d': m1d, 'M1': m1, 'relief': relief, 'wdt_bn': wdt, 'gdp': gdp,
           'B1a': 100 * run['payers'] / run['adults_k'], 'B1b': run['entries'], 'B1c': run['exits'], 'B1d': 100 * run['fall_through'] / gdp,
           'S_gdp': 100 * S / gdp, 'fill': fl, 'unfilled': f['unfilled'], 'srr_fill': f['srr_fill'],
           'P1': np.where(ok, fl, T), 'P3': np.maximum(0.0, m1d - relief).sum(axis=0), 'P5': years,
           'P4_ratio': long_ / short, 'P4_first_negative': np.where(below.any(axis=0), below.argmax(axis=0) + 1, 0),
           'P6': {y: 100 * S[y - 1] / gdp[y - 1] for y in (10, 25, 50, 100) if y <= T},
           'P7a': (after & (lres <= 1e-12)).any(axis=0), 'P7b': np.where(after, lres, np.inf).min(axis=0),
           'short': short, 'long': long_, 'long_year_T': m1[-1], 'wdt_short': np.where(ok, window_mean(m1a, gdp, fl + 1, fl + horizon), np.nan),
           'fund': f, 'negative_share': {'short': np.nanmean(short < 0) if np.isfinite(short).any() else np.nan, 'long': float(np.mean(long_ < 0))}}
    out['M1e'] = {k: np.where(years[:, i][None, :] > 0, (t >= years[:, i][None, :]) * v, 0.0) for i, (k, v) in enumerate(rec.items())}
    return out


def identity(run, g, c, hook=None):
    """I3, the epsilon check, per path. `assessed` (tax assessed on gains, summed over the years, billions) against sum of eps x g x omega, with g the accrued
    gain rate (1 + r)(1 - c) - 1 where positive, omega the start-of-year wealth of the lines taxed and eps its wealth-weighted marginal rate at the new
    wealth: the gap `assessed` is an accounting error (zero up to rounding). `total` is the gap of eps x g x omega + refunds against M1a, which carries what the
    routes defer (Route D) and the death flows no gain rate explains; both are relative to |M1a|. Returns those, eps, g and omega averaged over the years."""
    gacc = np.maximum((1.0 + g) * (1.0 - c) - 1.0, 0.0) if hook is None else hook.gain(g, run)
    eps = run['wtau'] / np.where(run['wbase'] > 0, run['wbase'], np.nan)
    pred = np.nansum(eps * gacc * run['wbase'], axis=0)
    m1a = sum(run[k].sum(axis=0) for k in ('tax', 'refund', 'death_tax', 'heir', 'death_B', 'death_D'))
    return {'assessed': np.abs(run['assessed'].sum(axis=0) - pred) / np.abs(pred), 'total': np.abs(m1a - pred - run['refund'].sum(axis=0)) / np.abs(m1a),
            'eps': np.nanmean(eps, axis=0), 'g': gacc.mean(axis=0), 'omega': run['wbase'].mean(axis=0)}
