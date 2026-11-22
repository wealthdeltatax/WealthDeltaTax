"""
support.py -- supporting metrics (model v3, stage V3-9)
=======================================================
Layer L3 (architecture.md 5.1). Imports numpy and core/kernel.py only; it does not import burden (same layer). No file is read and nothing
runs at import (R8). No country or tax line is named (R11): every rate, share and series arrives as an argument, as a fraction (0.06, not 6).

Ids: O7 and OD1 (M7, M7c to M7e), OM1 (M9), OW1 (M13), OW2 (M14), OW3 (M15a, M15b), OS1 (S1).

CONVENTIONS (R6)
----------------
Arithmetic basis: g is the arithmetic real return of one year, V -> V (1 + g). Money is millions of pounds per adult unless a name ends in _bn
(billions of pounds a year) or _k (thousands of adults). Percentage points and basis points are returned as such, never as fractions.
Refund = tau x loss and the envelope resets at death are the kernel's (kernel.py docstring); this module reads its cumulative record.
Welfare is a certainty equivalent over a set of paths, so a function returns one value per call (per line), not one per path: the runner calls
it once per block of paths (a level 2 draw) and summarises across blocks.

M7 is read on a Route C line over N holding years, then a sale year in which alpha drops out (the declared value falls to the true value). The
kernel's post-surrender basis leaves nothing to settle after the sale (the declared value equals the new basis), so there is no settlement loop.
Net is credited tax paid minus credited refunds over the whole run, in pounds; TW(1) is the terminal wealth of the honest line (alpha = 1).
M13 compares four systems on the same paths and payers: each comparator's rate is solved so that its mean lifetime revenue per adult equals the
kernel's net tax; a comparator taxes the payers (lines at or above the threshold at the start) only, and revenue and weights count those lines only. The behavioural response is applied to the
base before this module, equally to every system, so it is not repeated here.
"""

from __future__ import annotations

import numpy as np

from model_v3.core import kernel as K

SYSTEMS = ('income_tax_gains', 'stock_wealth_tax', 'consumption_tax')   # the comparators of M13; the manifest's tax_system labels


# ─────────────────────────────────────────────────────────────
# M7, M7c to M7e: the declaration curve
# ─────────────────────────────────────────────────────────────

def declaration_runs(rate_fn, g, V0, alphas):
    """One Route C line per (alpha, path). g is (N + 1, P): N holding years then the sale year. Returns arrays (A, P): net, refunds, tw."""
    g, alphas = np.asarray(g, float), np.asarray(alphas, float)
    N, P, A = g.shape[0] - 1, g.shape[1], len(alphas)
    gm = np.tile(g, (1, A))                                       # line a * P + p
    book = K.run_lines(rate_fn, gm[:N], {'C': V0}, alpha_C=np.repeat(alphas, P), n=A * P)
    K.step_year(book, rate_fn, 1.0, gm[N], 0.0, alpha_C=1.0)      # the sale: alpha drops out
    shape = lambda x: x.reshape(A, P)
    return {'net': shape(book.paid - book.refunded), 'refunds': shape(book.refunded), 'tw': shape(book.family_true())}


def declaration_curve(runs, alphas):
    """C.1(alpha) = 100 (Net(alpha) - Net(1)) / TW(1) and the lost refund protection 100 (Refunds(1) - Refunds(alpha)) / TW(1): (A, P) each."""
    i = np.flatnonzero(np.isclose(alphas, 1.0))
    if len(i) != 1:
        raise ValueError('the alpha grid must hold 1.0 exactly once: TW(1) is the denominator of C.1')
    tw1 = runs['tw'][i[0]]
    return 100.0 * (runs['net'] - runs['net'][i[0]]) / tw1, 100.0 * (runs['refunds'][i[0]] - runs['refunds']) / tw1


def _edge(al, c, tol):
    """First stretch along axis 0 where |c| reaches tol, the edge interpolated linearly; al[-1] when |c| stays under tol."""
    bad = np.abs(c) >= tol
    j = np.where(bad.any(0), bad.argmax(0), len(al) - 1)
    jp = np.maximum(j - 1, 0)
    cj, cp = np.take_along_axis(c, j[None], 0)[0], np.take_along_axis(c, jp[None], 0)[0]
    w = np.where(cj != cp, (np.sign(cj) * tol - cp) / np.where(cj != cp, cj - cp, 1.0), 0.0)
    return np.where(bad.any(0), al[jp] + w * (al[j] - al[jp]), al[-1])


def tolerant_zone(alphas, c1, tol=2.0):
    """Lower and upper alpha of the stretch around alpha = 1 where |C.1| < tol points (O7). alphas ascending, c1 (A, P). An edge on the
    grid's end means the zone reaches past the grid."""
    alphas, c1 = np.asarray(alphas, float), np.asarray(c1, float)
    i = int(np.flatnonzero(np.isclose(alphas, 1.0))[0])
    return _edge(alphas[:i + 1][::-1], c1[:i + 1][::-1], tol), _edge(alphas[i:], c1[i:], tol)


def modal_alpha(alphas, weights):
    """M7e: the alpha held by the largest share of payers. weights (A,) or (A, P) are payer shares at each alpha; the lowest alpha wins a tie.
    The distribution of declared alpha is an input the register does not hold (supporting.md M-3): the caller supplies it."""
    return np.asarray(alphas)[np.argmax(np.asarray(weights, float), axis=0)]


# ─────────────────────────────────────────────────────────────
# M9: net fiscal effect after migration
# ─────────────────────────────────────────────────────────────

def migration_effect(m1_pct, payers_k, gdp_bn, gdp_index, leave, income, rate_income, spend=0.0, rate_spend=0.0):
    """M9 = M1 - X. X is what the state loses each year from the payers who leave: leave (fraction) x payers (thousands of adults, (T, P)) x
    (income x rate_income + spend x rate_spend), per leaver and year in base-year pounds, grown with gdp_index (GDP over its base-year value).
    m1_pct, payers_k, gdp_bn, gdp_index are (T, P); X and M9 are percent of GDP. Returns {'M1', 'X', 'M9'}."""
    x_bn = leave * payers_k * 1e3 * gdp_index * (income * rate_income + spend * rate_spend) / 1e9
    x = 100.0 * x_bn / gdp_bn
    return {'M1': np.asarray(m1_pct, float), 'X': x, 'M9': np.asarray(m1_pct, float) - x}


# ─────────────────────────────────────────────────────────────
# M13: certainty-equivalent welfare of the tax systems at equal revenue
# ─────────────────────────────────────────────────────────────

def crra_ce(w, gamma, axis=-1):
    """Certainty equivalent U^-1(E[U(w)]) of CRRA utility over `axis`; gamma = 1 is log utility."""
    w = np.asarray(w, float)
    if np.any(w <= 0.0):
        raise ValueError('CRRA utility needs positive terminal wealth')
    if abs(gamma - 1.0) < 1e-9:
        return np.exp(np.log(w).mean(axis))
    return np.mean(w ** (1.0 - gamma), axis) ** (1.0 / (1.0 - gamma))


def cew_bp(w, w_none, gamma):
    """CEW = CE(w) / CE(w_none) - 1 in basis points, per line: paths on the last axis. Negative is a welfare cost."""
    return 1e4 * (crra_ce(w, gamma) / crra_ce(w_none, gamma) - 1.0)


def wmean(x, w):
    """Weighted mean over axis 0 (lines); a band is the same call on the band's lines."""
    w = np.asarray(w, float)
    return (w * x).sum(0) / w.sum()


def system_run(kind, rate, g, w0, w_min, c=0.0):
    """Terminal wealth and lifetime tax, both (L, P), of payer lines with start wealth w0 (L,) under one system. g is (N, P). Each year wealth
    grows, a share c is consumed, then the tax is paid: 'none'; 'stock_wealth_tax' on start-of-year wealth; 'income_tax_gains' on the gain of
    the year when positive (losses unrelieved); 'consumption_tax' on the value consumed. Lines under w_min pay nothing."""
    if kind not in ('none',) + SYSTEMS:
        raise ValueError(f'unknown system {kind!r}')
    w = np.repeat(np.asarray(w0, float)[:, None], g.shape[1], axis=1)
    payer, paid = (np.asarray(w0) >= w_min)[:, None], np.zeros_like(w)
    for gt in g:
        grown = w * (1.0 + gt)
        tax = {'none': 0.0 * w, 'stock_wealth_tax': rate * w, 'income_tax_gains': rate * np.maximum(grown - w, 0.0),
               'consumption_tax': rate * c * grown}[kind] * payer
        w = grown * (1.0 - c) - tax
        paid += tax
    return w, paid


def solve_rate(kind, target, g, w0, weights, w_min, c=0.0, hi=1.0, iters=80):
    """The rate at which the mean lifetime tax per adult (weighted over lines, averaged over paths) equals target; bisection, since tax rises
    with the rate. Raises when even a rate of `hi` does not raise the target."""
    rev = lambda r: float((np.asarray(weights)[:, None] * system_run(kind, r, g, w0, w_min, c)[1]).sum(0).mean())
    if rev(hi) < target:
        raise ValueError(f'{kind}: a rate of {hi} raises {rev(hi):.6g}, less than the target {target:.6g}')
    lo = 0.0
    for _ in range(iters):
        mid = 0.5 * (lo + hi)
        lo, hi = (mid, hi) if rev(mid) < target else (lo, mid)
    return 0.5 * (lo + hi)


def wdt_run(rate_fn, g, V0, c=0.0, hook=None, **book_kw):
    """Terminal wealth and net tax paid, (L, P), of each line under the kernel over g (N, P). V0 maps routes to (L,) arrays; book_kw reaches
    run_lines (index_rate, lam_C, b_mode, ...). Lines and paths are folded into the line axis, line l and path p at l * P + p."""
    L, P = len(next(iter(V0.values()))), g.shape[1]
    book = K.run_lines(rate_fn, np.tile(g, (1, L)), {r: np.repeat(np.asarray(v, float), P) for r, v in V0.items()}, consumption=c, n=L * P, hook=hook, **book_kw)
    return book.family_true().reshape(L, P), (book.paid - book.refunded).reshape(L, P)


def welfare(rate_fn, g, V0, weights, gamma, w_min, c=0.0, **book_kw):
    """M13 per line, basis points: {'wdt', 'income_tax_gains', 'stock_wealth_tax', 'consumption_tax'} -> (L,), and the solved comparator rates.
    weights (L,) are shares of adults; lines under w_min get none. The comparators raise the same mean lifetime tax per adult as the kernel."""
    w0 = np.sum([np.asarray(v, float) for v in V0.values()], axis=0)
    pw = np.asarray(weights, float) * (w0 >= w_min)
    w_wdt, tax_wdt = wdt_run(rate_fn, g, V0, c, **book_kw)
    target = float((pw[:, None] * tax_wdt).sum(0).mean())
    w_none, _ = system_run('none', 0.0, g, w0, w_min, c)
    out, rates = {'wdt': cew_bp(w_wdt, w_none, gamma)}, {}
    for kind in SYSTEMS:
        rates[kind] = solve_rate(kind, target, g, w0, pw, w_min, c)
        out[kind] = cew_bp(system_run(kind, rates[kind], g, w0, w_min, c)[0], w_none, gamma)
    return out, rates


# ─────────────────────────────────────────────────────────────
# M14: lock-in cost of a gains tax realised on switching
# ─────────────────────────────────────────────────────────────

def lockin(gA, gB, rate, emb, T, gamma):
    """A payer holds asset A (per unit of value, embedded gain share emb) for T more years and may switch to B. gA, gB are (>= T, P) real
    returns of the two assets. The gains tax at `rate` falls on the gain at the end; switching realises the embedded gain first. The payer
    chooses the better terminal wealth on each path (hindsight), with the switch taxed and with it tax-neutral (the gain rolled over).
    Returns (cost_bp, p_locked): the certainty-equivalent cost of the taxed switch against the neutral one, as a share of the no-tax
    certainty equivalent (<= 0), and the share of paths where the tax alone blocks a switch the neutral payer makes."""
    GA, GB = np.prod(1.0 + np.asarray(gA, float)[:T], axis=0), np.prod(1.0 + np.asarray(gB, float)[:T], axis=0)
    end = lambda value, basis: value - rate * (value - basis)
    stay = end(GA, 1.0 - emb)
    x = 1.0 - rate * emb                                           # what is left to invest after the tax on the realised gain
    switch_tax, switch_neutral = end(x * GB, x), end(GB, 1.0 - emb)
    w_tax, w_neutral = np.maximum(stay, switch_tax), np.maximum(stay, switch_neutral)
    locked = (switch_neutral > stay) & (switch_tax <= stay)
    return 1e4 * (crra_ce(w_tax, gamma) - crra_ce(w_neutral, gamma)) / crra_ce(np.maximum(GA, GB), gamma), float(locked.mean())


# ─────────────────────────────────────────────────────────────
# M15a, M15b: the contribution envelope
# ─────────────────────────────────────────────────────────────

def envelope(L, lost_cum, weights=None, tol=1e-12):
    """M15a from the kernel's record. L (T, n) is the tax (+) or refund (-) assessed per line and year (Flows.L); lost_cum (T, n) the cumulative
    book.lost_refund after each year. The envelope binds in a year when the cap holds back a refund. Returns per line: binds, first (year, 1-based,
    nan if never), due and forgone (totals), forgone_t (T, n); and with the weights (n,): share_binding and forgone_share (of refunds due)."""
    L, lost_cum = np.asarray(L, float), np.asarray(lost_cum, float)
    w = np.ones(L.shape[1]) if weights is None else np.asarray(weights, float)
    due, forgone_t = np.maximum(-L, 0.0), np.diff(lost_cum, axis=0, prepend=0.0)
    hit = forgone_t > tol
    return {'binds': hit.any(0), 'first': np.where(hit.any(0), hit.argmax(0) + 1.0, np.nan), 'due': due.sum(0), 'forgone': forgone_t.sum(0),
            'forgone_t': forgone_t, 'share_binding': float((w * hit.any(0)).sum() / w.sum()),
            'forgone_share': float((w * forgone_t.sum(0)).sum() / max((w * due.sum(0)).sum(), 1e-300))}


def liquidity_timing(forgone_bn, gdp_bn, years):
    """M15b: refunds the short reserve would owe in the first `years` years without the cap, less with it, as the mean annual percent of GDP.
    forgone_bn and gdp_bn are (T, P), billions of pounds."""
    return 100.0 * (np.asarray(forgone_bn)[:years] / np.asarray(gdp_bn)[:years]).mean(0)


# ─────────────────────────────────────────────────────────────
# S1: capitalisation of retired property taxes (a switch, off in every headline cell)
# ─────────────────────────────────────────────────────────────

def capitalise(wealth, property_share, uplift, on=False):
    """Wealth with property worth (1 + uplift) more when the switch is on; off returns the wealth unchanged. The threshold is not touched."""
    wealth = np.asarray(wealth, float)
    return wealth * (1.0 + np.asarray(property_share, float) * uplift) if on else wealth.copy()


def payer_count(wealth, adults_k, w_min):
    """Thousands of adults in lines at or above w_min; wealth is (L,) or (L, P)."""
    a = np.asarray(adults_k, float).reshape((-1,) + (1,) * (np.ndim(wealth) - 1))
    return (a * (np.asarray(wealth) >= w_min)).sum(0)


def s1_effect(on, off):
    """OS1: the switch on minus off, for each quantity the two dicts share (m1, m2, payer_count)."""
    return {k: np.asarray(on[k], float) - np.asarray(off[k], float) for k in off}
