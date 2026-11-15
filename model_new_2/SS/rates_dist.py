"""
rates_dist.py — RATES rebuild, L1 wealth distribution
======================================================
Replaces the 15-bracket household table.  Builds a distribution of ADULT net
worth on a fine cell grid: a survey body, a piecewise-Pareto tail anchored to
published top shares, and a named top tier from the Sunday Times Rich List.

WHY
---
The old table (RATES §5.1) was (a) a per-household shape applied to
individuals, and (b) survey-based, so it inherited the survey's undercount of the
very rich: its top 0.1% share was 3.9% against about 9% in WID-style estimates,
its top 1% was 14.2% against 20-25% from estate-based estimates, and its
top 692 people held roughly £33bn (rescaled) against £773bn for the Rich List's
top 350.  The WDT's payers are concentrated exactly where the survey is weakest.

CONSTRUCTION (all wealth in £bn, per-adult means in £m)
-------------------------------------------------------
Survey anchors (old table shares, RATES §5.1; consistent with the IEA/WAS table:
top 10% 43.9, top 1% 12.6, top 0.1% 3.1-4.4):
    top fraction q : 0.10    0.05    0.01    0.001   1e-4    1e-5
    top share      : 45.77%  32.65%  14.23%  3.88%   1.00%   0.22%
Body (below the top 10%): decile sums from the table, scaled to the ONS total.

scenario 'survey'    survey anchors throughout; total = ONS aggregate.
scenario 'adjusted'  body and the 90-99th percentiles as in 'survey' (the survey
                     measures these acceptably), top 1% rebuilt:
                       top-1% share   s1  = 22.5%  estate-based: "between one fifth
                                                   and one quarter"
                       top-0.1% share s01 = 9%     WID-style estimate
                       top-350 wealth = Rich List £772.8bn (2025); entry £350m
                     'add' mode (default): body is held at survey levels and the
                     extra top wealth is ADDED, so the aggregate exceeds the ONS
                     total (the survey's coverage gap).  'reallocate' mode holds
                     the total at the ONS figure and shrinks the body instead.
Survey anchors are interpolated log-log linear (piecewise Pareto).  The adjusted tail below
the named tier is a SMOOTH density, ln w(q) quadratic in ln q, fitted to three facts: the
top-1% and top-0.1% shares and the £350m list entry (a plain log-log interpolation
between the anchors made cell means non-monotone at the 0.1% boundary).  Needs scipy.  The named
tier is split into three cells (top 10, ranks 11-100, 101-350) by a Pareto with
alpha 1.5 (top 10 hold 31% of the list: stylised, not sourced).

LIMITS
------
* Anchors are 2016-18 (survey) and 2025 (Rich List); no time adjustment.
* The shape of the body is still the household-derived decile profile.
* Pareto interpolation between anchors is smooth by construction; it cannot
  reveal lumpiness between them.
* Trusts, offshore and unlisted-business wealth below the Rich List's reach are
  covered only through the s1 and s01 anchors.

API
---
  build(scenario, n_adults, ...) -> dict   scenario 'advani' (evidence-based, recommended; mode =
                                            'central' | 'upper'), 'adjusted', 'survey'(labels, share, mean_gbp_m, wealth_bn, ...)
  shares_check(d)                -> dict of realised top shares
  wealth_at_top_fraction(d, q)   -> wealth (£m) at top-fraction q (for threshold by percentile)
"""

import numpy as np

ONS_TOTAL_BN = 14_600.0              # GB household net wealth 2016-18 (WAS)
RICH_LIST_BN = 772.8                 # Sunday Times Rich List 2025, top 350
RICH_LIST_N = 350

# survey anchors from the old table (RATES §5.1): (top fraction, top share)
_TABLE_TOTAL = 42_945.4
_SURVEY_ANCHORS = [
    (0.10,  19_658.2 / _TABLE_TOTAL),
    (0.05,  14_021.2 / _TABLE_TOTAL),
    (0.01,   6_109.3 / _TABLE_TOTAL),
    (1e-3,   1_665.6 / _TABLE_TOTAL),
    (1e-4,     429.1 / _TABLE_TOTAL),
    (1e-5,      96.6 / _TABLE_TOTAL),
]
# decile sums below the 90th percentile (£bn, old table), deciles 0-10 .. 80-90
_BODY_DECILES_BN = [24.0, 159.7, 474.1, 1017.4, 1806.9, 2780.4, 3941.2,
                    5412.4, 7671.1]

# cell edges, as top fractions
_EDGES_90_99 = [0.10, 0.08, 0.06, 0.04, 0.02, 0.01]
_EDGES_TOP1  = [0.01, 0.005, 0.002, 0.001, 5e-4, 2e-4, 1e-4, 3e-5, 1e-5]
_TIER_ALPHA = 1.5


def _loglog(anchors):
    """Return S(q) interpolating (q, S) anchors log-log linearly; anchors sorted by q desc."""
    q = np.array([a[0] for a in anchors], float)
    s = np.array([a[1] for a in anchors], float)
    lq, ls = np.log(q[::-1]), np.log(s[::-1])      # ascending q for np.interp
    def S(x):
        x = np.asarray(x, float)
        lx = np.log(x)
        out = np.interp(lx, lq, ls)
        # extrapolate with the end slopes
        lo = lx < lq[0]
        hi = lx > lq[-1]
        if np.any(lo):
            b = (ls[1] - ls[0]) / (lq[1] - lq[0])
            out = np.where(lo, ls[0] + b * (lx - lq[0]), out)
        if np.any(hi):
            b = (ls[-1] - ls[-2]) / (lq[-1] - lq[-2])
            out = np.where(hi, ls[-1] + b * (lx - lq[-1]), out)
        return np.exp(out)
    return S


def _fit_tail(total_bn, s1, s01, rich_list_bn, p_list, n_adults, entry_gbp_m):
    """
    Smooth tail below the named tier.  ln w(q) is quadratic in ln q (w = wealth at top
    fraction q, in £bn per unit fraction).  Three constraints pin it down:
      wealth of ranks below the list up to the top 0.1%  = s01*total - RL
      wealth held between the top 0.1% and the top 1%    = (s1 - s01)*total
      wealth at the list entry (rank 350)                = entry_gbp_m per adult
    Returns a function cell_wealth_bn(q_a, q_b).
    """
    from scipy.optimize import fsolve
    from scipy.integrate import quad
    x0, x1, x2 = np.log(p_list), np.log(1e-3), np.log(1e-2)
    G_a = s01 * total_bn - rich_list_bn
    G_b = (s1 - s01) * total_bn
    w_entry = entry_gbp_m * 1e6 * n_adults / 1e9
    lw = lambda x, a, b, c: a + b * (x - x1) + c * (x - x1) ** 2
    integ = lambda lo, hi, a, b, c: quad(lambda x: np.exp(lw(x, a, b, c) + x), lo, hi, limit=200)[0]
    eqs = lambda p: [integ(x0, x1, *p) / G_a - 1, integ(x1, x2, *p) / G_b - 1,
                     lw(x0, *p) - np.log(w_entry)]
    sol = None
    for a0 in (np.log(1e5), np.log(1e6), np.log(5e6)):
        for b0 in (-0.5, -1.0, -1.5):
            for c0 in (0.0, 0.05, -0.05):
                r, info, ier, _ = fsolve(eqs, [a0, b0, c0], full_output=True)
                if ier == 1 and max(abs(np.array(eqs(r)))) < 1e-8:
                    sol = r
                    break
            if sol is not None:
                break
        if sol is not None:
            break
    if sol is None:
        raise RuntimeError('tail fit failed: anchors inconsistent')
    return (lambda qa, qb: integ(np.log(qb), np.log(qa), *sol)), sol


def _pav(mean, weight):
    """Pool adjacent violators: make `mean` non-decreasing by pooling blocks, preserving
    each block's total (mean * weight).  Returns (new_mean, n_pooled_cells)."""
    blocks = [[m * w, w, 1] for m, w in zip(mean, weight)]       # [total, weight, count]
    out = []
    for b in blocks:
        out.append(b)
        while len(out) > 1 and out[-2][0] / out[-2][1] >= out[-1][0] / out[-1][1]:
            t, w, c = out.pop()
            out[-1][0] += t; out[-1][1] += w; out[-1][2] += c
    new = np.concatenate([[b[0] / b[1]] * b[2] for b in out])
    return new, int(sum(b[2] for b in out if b[2] > 1))


# ── Advani, Bangham & Leslie (2021), "The UK's wealth distribution and characteristics of
#    high-wealth households" (Wealth Tax Commission Evidence Paper 1), GB 2016-18, wealth incl.
#    pensions, business assets, physical wealth at ~25% of replacement cost ──
ADVANI = {
    'survey_total_bn': 14_400.0,   # WAS, their definition (ONS official £14.6tn uses another)
    's10_survey': 0.51,            # top-10% share, survey
    's1_survey': 0.18,             # top-1% share, survey
    's1_upper': 0.23,              # top-1% share after Rich List + (upper) Pareto adjustment
    'extra_central_bn': 0.05 * 14_400.0,   # central estimate: total wealth 5% higher (£15.1tn)
    'strl_n': 1000,                # Sunday Times Rich List entries (2017/18 editions)
    'strl_bn': 700.0,              # their total value
    'strl_entry_m': 100.0,         # ~£103m entry, 2016 list (Wikipedia, STRL 2016)
}


def _build_advani(n_adults, variant='central', wealth_scale=1.0, tail_alpha=None,
                  tier_alpha=_TIER_ALPHA):
    """
    Evidence-based distribution on the Advani-Bangham-Leslie basis.

    survey Lorenz:  bottom 90% = 49% of £14.4tn (decile shape from the RATES table),
                    90th-99th pct log-log between top-10% 51% and top-1% 18%.
    adjustment:     X £bn added within the top 1% (central: 5% of the survey total;
                    'upper': X chosen so the top-1% share is 23%).
    top 0.1%:       share = s1_adj * 0.1**(1 - 1/alpha), alpha taken from the adjusted
                    top-10% -> top-1% slope unless tail_alpha is given.
    named tier:     the 1,000 Rich List families (£700bn), three cells, Pareto alpha 1.5 inside.
    wealth_scale:   multiplies all £ (shares unchanged) -- e.g. 0.66 gives the national-accounts
                    aggregate (£10.0tn) on the same shape.
    """
    A = ADVANI
    base = A['survey_total_bn']
    if variant == 'central':
        X = A['extra_central_bn']
    elif variant == 'upper':
        X = (A['s1_upper'] - A['s1_survey']) * base / (1.0 - A['s1_upper'])
    else:
        raise ValueError("variant must be 'central' or 'upper'")
    T = base + X
    top10 = A['s10_survey'] * base + X
    top1 = A['s1_survey'] * base + X
    s10a, s1a = top10 / T, top1 / T
    beta = np.log(s1a / s10a) / np.log(0.1)
    alpha = tail_alpha or 1.0 / (1.0 - beta)
    s01 = s1a * 0.1 ** (1.0 - 1.0 / alpha)

    cells = []
    f = (1.0 - A['s10_survey']) * base / sum(_BODY_DECILES_BN)
    for i, w in enumerate(_BODY_DECILES_BN):
        cells.append((f'{10*i}-{10*(i+1)}', 0.10, w * f))
    S_surv = _loglog([(0.10, A['s10_survey'] * base), (0.01, A['s1_survey'] * base)])
    for qa, qb in zip(_EDGES_90_99[:-1], _EDGES_90_99[1:]):
        cells.append((f'top{100*qa:g}-{100*qb:g}%', qa - qb, float(S_surv(qa) - S_surv(qb))))

    p_list = A['strl_n'] / n_adults
    cell_w, _ = _fit_tail(T, s1a, s01, A['strl_bn'], p_list, n_adults, A['strl_entry_m'])
    edges = _EDGES_TOP1[:-1] + [p_list]
    for qa, qb in zip(edges[:-1], edges[1:]):
        cells.append((f'top{100*qa:g}-{100*qb:g}%', qa - qb, float(cell_w(qa, qb))))
    b = 1.0 - 1.0 / tier_alpha
    n = A['strl_n']
    for lo, hi in ((n // 10, n), (n // 100, n // 10), (0, n // 100)):
        frac = (hi / n) ** b - (lo / n) ** b
        cells.append((f'RichList {lo+1}-{hi}', (hi - lo) / n_adults, A['strl_bn'] * frac))

    labels = [c[0] for c in cells]
    share = np.array([c[1] for c in cells], float)
    wealth = np.array([c[2] for c in cells], float) * wealth_scale
    share = share / share.sum()
    mean = wealth * 1e9 / (share * n_adults) / 1e6
    repaired = 0
    if np.any(np.diff(mean) <= 0):
        mean, repaired = _pav(mean, share)
        wealth = mean * share * n_adults * 1e6 / 1e9
    return {'labels': labels, 'share': share, 'wealth_bn': wealth, 'mean_gbp_m': mean,
            'total_bn': float(wealth.sum()), 'n_adults': n_adults, 'scenario': 'advani',
            'mode': variant, 'repaired_cells': repaired,
            'params': {'X_bn': X, 'alpha_tail': alpha, 's10_adj': s10a, 's1_adj': s1a,
                       's01': s01, 'wealth_scale': wealth_scale}}


def build(scenario='adjusted', n_adults=52.0e6, mode='add', s1=0.225, s01=0.09,
          rich_list_bn=RICH_LIST_BN, ons_total_bn=ONS_TOTAL_BN, list_entry_gbp_m=350.0,
          wealth_scale=1.0, tail_alpha=None):
    """
    Returns dict with arrays over cells, ordered from the bottom:
      labels, share (adult fraction), wealth_bn, mean_gbp_m (per adult),
      total_bn, n_adults, scenario, notes
    """
    if scenario == 'advani':
        return _build_advani(n_adults, variant=mode, **{k: v for k, v in
                             dict(wealth_scale=wealth_scale, tail_alpha=tail_alpha).items()})
    if scenario not in ('survey', 'adjusted'):
        raise ValueError("scenario must be 'survey', 'adjusted' or 'advani'")
    scale = ons_total_bn / _TABLE_TOTAL
    S_surv = _loglog(_SURVEY_ANCHORS)

    cells = []   # (label, adult_share, wealth_bn)

    # --- body: nine deciles, survey levels ---
    for i, w in enumerate(_BODY_DECILES_BN):
        cells.append((f'{10*i}-{10*(i+1)}', 0.10, w * scale))

    # --- 90th-99th percentile: survey Lorenz, fine cells ---
    for qa, qb in zip(_EDGES_90_99[:-1], _EDGES_90_99[1:]):
        w = (S_surv(qa) - S_surv(qb)) * _TABLE_TOTAL * scale
        cells.append((f'top{100*qa:g}-{100*qb:g}%', qa - qb, w))

    p350 = RICH_LIST_N / n_adults
    if scenario == 'survey':
        edges = _EDGES_TOP1
        for qa, qb in zip(edges[:-1], edges[1:]):
            w = (S_surv(qa) - S_surv(qb)) * _TABLE_TOTAL * scale
            cells.append((f'top{100*qa:g}-{100*qb:g}%', qa - qb, w))
        cells.append(('top0.001%', edges[-1], S_surv(edges[-1]) * _TABLE_TOTAL * scale))
        total = sum(c[2] for c in cells)
    else:
        body_bn = sum(c[2] for c in cells)                       # below the top 1%
        if mode == 'add':
            total = body_bn / (1.0 - s1)
        elif mode == 'reallocate':
            total = ons_total_bn
            body_bn_target = (1.0 - s1) * total
            f = body_bn_target / body_bn
            cells = [(l, a, w * f) for (l, a, w) in cells]
        else:
            raise ValueError("mode must be 'add' or 'reallocate'")
        cell_w, tail_par = _fit_tail(total, s1, s01, rich_list_bn, p350, n_adults,
                                     list_entry_gbp_m)
        edges = _EDGES_TOP1[:-1] + [p350]
        for qa, qb in zip(edges[:-1], edges[1:]):
            cells.append((f'top{100*qa:g}-{100*qb:g}%', qa - qb, float(cell_w(qa, qb))))
        # named tier: three cells splitting the Rich List
        b = 1.0 - 1.0 / _TIER_ALPHA
        cuts = [(100, RICH_LIST_N), (10, 100), (0, 10)]      # ascending wealth, like every other cell
        for lo, hi in cuts:
            frac = (hi / RICH_LIST_N) ** b - (lo / RICH_LIST_N) ** b
            cells.append((f'RichList {lo+1}-{hi}', (hi - lo) / n_adults, rich_list_bn * frac))

    labels = [c[0] for c in cells]
    share = np.array([c[1] for c in cells], float)
    wealth = np.array([c[2] for c in cells], float) * wealth_scale
    # normalise population shares to sum to 1 (cells tile the population)
    share = share / share.sum()
    # wealth_bn*1e9 £ / (share*n_adults persons) / 1e6 = £m per adult
    mean = wealth * 1e9 / (share * n_adults) / 1e6
    repaired = 0
    if np.any(np.diff(mean) <= 0):
        mean, repaired = _pav(mean, share)
        wealth = mean * share * n_adults * 1e6 / 1e9       # totals preserved per pooled block
    return {'labels': labels, 'share': share, 'wealth_bn': wealth, 'mean_gbp_m': mean,
            'total_bn': float(wealth.sum()), 'n_adults': n_adults,
            'scenario': scenario, 'mode': mode, 'repaired_cells': repaired,
            'params': {'s1': s1, 's01': s01, 'rich_list_bn': rich_list_bn}}


def top_shares(d):
    """Realised share of total wealth held by the top q of adults, for standard q."""
    share, w = d['share'], d['wealth_bn']
    tot = w.sum()
    cum_p = np.cumsum(share[::-1])          # from the top
    cum_w = np.cumsum(w[::-1]) / tot
    out = {}
    for q in (0.10, 0.05, 0.01, 1e-3, 1e-4, 1e-5):
        out[q] = float(np.interp(q, np.concatenate([[0], cum_p]),
                                 np.concatenate([[0], cum_w])))
    return out


def wealth_at_top_fraction(d, q):
    """Approximate wealth (£m per adult) at top-fraction q, by log-log interpolation
    of cell means against cell mid-fractions (from the top)."""
    share = d['share'][::-1]
    mean = d['mean_gbp_m'][::-1]
    edges = np.concatenate([[0.0], np.cumsum(share)])
    mid = np.sqrt(np.maximum(edges[:-1], 1e-12) * edges[1:])
    return float(np.exp(np.interp(np.log(q), np.log(mid), np.log(mean))))
