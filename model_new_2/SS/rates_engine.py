"""
rates_engine.py — RATES rebuild, L2 engine + L3 aggregation
============================================================
Honest-declaration WDT mechanics (alpha = 1), vectorised across "lines": a line
is one representative family of one (bracket, tier, death-phase).

MECHANICS (identical to valgen_core.run_family with refund_rule='ratio_mirror',
heir_influx='delta', envelope_unit='real'; checked in test_engine.py)
----------------------------------------------------------------------
Each year t, per line, in units:
  1. asset grows:            V *= 1 + g_t
  2. consumption:            f *= 1 - c                 (units sold, D16/D17)
  3. declared holdings:      W_new = f * V
  4. rate:                   tau(W_new / idx_t)          (W_min and k indexed)
  5. delta = W_new - W_prev
       delta > 0: tax in kind, q = tau * delta / W_new
       delta < 0: refund in units, q = -tau (1 - W_new/W_prev),
                  floored at -u_out/f  (never more units than this individual paid)
  6. f -= f*q; state units s += f*q; u_out += f*q
  7. death (first at t = phase, then every G years, t < T): heir cap cleared
     (u_out = 0); heir taxed in kind on the declared value received as a
     delta from zero: q = tau(W_new / idx_t).

Honest declaration is justified by valgen's result that no tested strategy
gains more than about 1% over honest at lambda >= 5% (VAL handoff).  A four-route
honest mix equals the single-asset run (valgen check p3_honest_ABC_equals_single_asset).

AGGREGATION
-----------
Lines are weighted by bracket population share x tier weight x phase weight
(uniform death phases give a steady inflow of inheritance events from year 1).
All money is per adult in units of y0 (GDP per capita at window start).
Outputs are converted to shares of GDP in run_cohorts().

NOT IN THIS LAYER
-----------------
Reserves, SRR/LRR, relief outlays: see the fund layer (L4).  The engine
reports the state's accumulated unit stake so the fund layer can hold it.
"""

import itertools

import numpy as np


def _tau(x, tau_0, tau_m, k, wmin):
    """Vectorised logistic rate; 0 below wmin.  x is wealth / index."""
    a = (tau_m - tau_0) / tau_0
    out = np.zeros_like(x, dtype=float)
    m = x >= wmin
    out[m] = tau_m / (1.0 + a * np.exp(-k * (x[m] - wmin)))
    return out


def run_lines(g, idx, V0, w, group, nb, ph, G, c, rp, heir_rule='delta'):
    """
    g      (T, n) or (T,)  asset growth per year per line
    idx    (T,)            threshold index factor for years 1..T
    V0     (n,)            initial holding value per line
    w      (n,)            weights (sum to 1)
    group  (n,) int        bracket id of each line, for the by-bracket output
    nb     int             number of brackets
    ph     (n,) int | None first-death year per line (None = no deaths)
    G      int             generation gap
    c      float           consumption share per year
    rp     dict            tau_0, tau_m, k, wmin  (already in engine units)
    heir_rule 'delta'      BASELINE.  Heir's net worth rises by the receipt: taxed in kind as a
                           delta from zero (valgen D6)
           'fresh'         ablation only: no tax on the receipt; heir's basis = declared value
                           received (valgen 'fresh_entrant')

    Returns dict of length-T arrays (weighted, money units per adult):
      tax        gross tax paid in holding-year assessments
      refund     refunds (negative)
      heir       tax paid on inheritance receipts
      stake      value of the state's accumulated in-kind stake at year end
      share_paying  adult share paying positive tax in the holding assessment
      by_bracket (T, nb) net receipts by bracket (holding + heir)
    """
    T = len(idx)
    n = len(V0)
    g = np.asarray(g, float)
    if g.ndim == 1:
        g = np.repeat(g[:, None], n, axis=1)
    V = np.asarray(V0, float).copy()
    f = np.ones(n)
    s = np.zeros(n)
    u = np.zeros(n)
    Wp = V.copy()
    tax = np.zeros(T); ref = np.zeros(T); heir = np.zeros(T)
    stake = np.zeros(T); npay = np.zeros(T); wealth = np.zeros(T)
    by_b = np.zeros((T, nb)); wealth_b = np.zeros((T, nb))
    wealth0_b = np.bincount(group, weights=w * np.asarray(V0, float), minlength=nb)
    t0, t_m, kk, wm = rp['tau_0'], rp['tau_m'], rp['k'], rp['wmin']

    for t in range(1, T + 1):
        V = V * (1.0 + g[t - 1])
        if np.any(c > 0.0):
            f = f * (1.0 - c)
        Wn = f * V
        rate = _tau(Wn / idx[t - 1], t0, t_m, kk, wm)
        delta = Wn - Wp
        q = np.zeros(n)
        pos = delta > 0.0
        q[pos] = rate[pos] * delta[pos] / Wn[pos]
        neg = (delta < 0.0) & (u > 0.0) & (f > 0.0) & (Wp > 0.0)
        if neg.any():
            q[neg] = np.maximum(-rate[neg] * (1.0 - Wn[neg] / Wp[neg]),
                                -u[neg] / f[neg])
        units = f * q
        paid = units * V
        f = f - units
        s = s + units
        u = u + units
        Wp = Wn
        wp = w * paid
        tax[t - 1] = wp[paid > 0.0].sum()
        ref[t - 1] = wp[paid < 0.0].sum()
        npay[t - 1] = w[paid > 0.0].sum()
        by_b[t - 1] = np.bincount(group, weights=wp, minlength=nb)

        if ph is not None and t < T:
            d = (t >= ph) & (((t - ph) % G) == 0)
            if d.any() and heir_rule == 'fresh':
                u[d] = 0.0
                Wp[d] = f[d] * V[d]
            elif d.any():
                u[d] = 0.0
                Wd = f[d] * V[d]
                rate_d = _tau(Wd / idx[t - 1], t0, t_m, kk, wm)
                qd = np.where(Wd > 0.0, rate_d, 0.0)
                ud = f[d] * qd
                pd_ = ud * V[d]
                f[d] = f[d] - ud
                s[d] = s[d] + ud
                u[d] = u[d] + ud
                Wp[d] = Wd
                heir[t - 1] = (w[d] * pd_).sum()
                by_b[t - 1] += np.bincount(group[d], weights=w[d] * pd_,
                                           minlength=nb)
        stake[t - 1] = (w * s * V).sum()
        wealth[t - 1] = (w * f * V).sum()
        wealth_b[t - 1] = np.bincount(group, weights=w * f * V, minlength=nb)

    return {'tax': tax, 'refund': ref, 'heir': heir, 'stake': stake,
            'share_paying': npay, 'by_bracket': by_b, 'wealth': wealth,
            'wealth_by_bracket': wealth_b, 'wealth0_by_bracket': wealth0_b}


def _phases(n_phase, G):
    """n_phase equally spaced first-death years in 1..G (G itself = unphased)."""
    return [int(np.ceil((i + 1) * G / n_phase)) for i in range(n_phase)]


def run_cohorts(scn, cal, tiers=None, n_phase=6, G=30, deaths=True,
                heir_rule='delta', c_cell=None):
    """
    Aggregate honest WDT receipts for one scenario and calibration.

    scn    from rates_scenario.build_scenario
    cal    from rates_scenario.calibrate
    c_cell    optional per-cell consumption shares (length = number of cells); overrides scn['c']
    heir_rule 'delta' (BASELINE, valgen D6) | 'fresh' (see run_lines).
           'delta' is the mechanism as designed: an heir's net worth rises by
           the receipt, so it is a delta like any other.  It is not an estate
           tax and 'fresh' is not a conservative case.  'fresh' is retained
           only as a validated ablation, to decompose revenue into
           holding-year and receipt-year timing.
    tiers  list of (weight, differential) or None for a homogeneous population.
           Differentials are additive to the return in the scenario's basis and
           persist across generations (a stylisation; see the design notes).

    Returns dict of length-T arrays as shares of GDP, plus diagnostics:
      tax, refund, heir, net (all / GDP), coverage (= net / expenditure_gdp),
      stake (state in-kind holding / GDP), wealth_gdp (family-held wealth / GDP),
      share_paying,
      by_bracket (T, nb) net / GDP
    """
    tiers = tiers or [(1.0, 0.0)]
    tw = np.array([t[0] for t in tiers], float)
    td = np.array([t[1] for t in tiers], float)
    if abs(tw.sum() - 1.0) > 1e-9:
        raise ValueError('tier weights must sum to 1')
    nb = len(cal['V0'])
    phs = _phases(n_phase, G) if deaths else [None]
    lines = list(itertools.product(range(nb), range(len(tiers)), phs))
    b_id = np.array([l[0] for l in lines])
    t_id = np.array([l[1] for l in lines])
    p_id = [l[2] for l in lines]
    w = cal['share'][b_id] * tw[t_id] / len(phs)
    V0 = cal['V0'][b_id]
    g = scn['r'][:, None] + td[t_id][None, :]
    ph = np.array(p_id, int) if deaths else None
    c_line = scn['c'] if c_cell is None else np.asarray(c_cell, float)[b_id]
    raw = run_lines(g, scn['idx'], V0, w, b_id, nb, ph, G, c_line, cal['rate'],
                    heir_rule=heir_rule)

    norm = 1.0 / (scn['yy'] * cal['pop_per_adult'])
    out = {k: raw[k] * norm for k in ('tax', 'refund', 'heir', 'stake', 'wealth')}
    out['wealth_gdp'] = out.pop('wealth')   # family-held net worth / GDP: stationarity diagnostic
    out['net'] = out['tax'] + out['refund'] + out['heir']
    out['coverage'] = out['net'] / scn['exp_gdp']
    out['share_paying'] = raw['share_paying']
    out['by_bracket'] = raw['by_bracket'] * norm[:, None]
    # level series (engine units) for effective-rate calculations
    prev_w = np.vstack([raw['wealth0_by_bracket'][None, :], raw['wealth_by_bracket'][:-1]])
    out['lvl'] = {'net_b': raw['by_bracket'], 'wealth_b': raw['wealth_by_bracket'],
                  'gain_b': scn['r'][:, None] * prev_w}
    out['exp_gdp'] = scn['exp_gdp']
    out['years'] = scn['years']
    return out


def effective_rates(out, cal, groups=(0.10, 0.06, 0.02, 0.01, 1e-3)):
    """
    Wealth-weighted effective rates over the window, for comparison with benchmarks.

      stock rate  = sum_t net WDT / sum_t wealth       (per year)
                    comparator: a stock wealth tax, % of wealth per year (proposals ~1-2%)
      gain rate   = sum_t net WDT / sum_t (r_t * W_{t-1})   tax as a share of accrued return
                    comparator: income / capital-gains tax rates (20-45%)

    Both are ratios of window sums, so each cell is weighted by its wealth (or gain):
    a wealth-weighted average of cell-level rates.  `net` includes inheritance receipts.
    Computed for: all adults, 'payers' (cells whose window net tax is positive), and the
    top-q cells (q in `groups`, by adult share, cells aligned to grid edges).
    """
    L = out['lvl']
    net = L['net_b'].sum(axis=0)
    W = L['wealth_b'].sum(axis=0)
    G = L['gain_b'].sum(axis=0)
    share = np.asarray(cal['share'])
    cum_top = np.cumsum(share[::-1])[::-1]

    def rates(mask):
        w, g, n = W[mask].sum(), G[mask].sum(), net[mask].sum()
        return (n / w if w > 0 else np.nan, n / g if g > 0 else np.nan)

    res = {}
    res['stock_all'], res['gain_all'] = rates(np.ones(len(share), bool))
    pay = net > 0
    res['stock_payers'], res['gain_payers'] = rates(pay)
    res['payer_adult_share'] = float(share[pay].sum())
    res['payer_wealth_share'] = float(W[pay].sum() / W.sum())
    for q in groups:
        m = cum_top <= q * (1 + 1e-6)
        key = f'top{100*q:g}'
        res[f'stock_{key}'], res[f'gain_{key}'] = rates(m) if m.any() else (np.nan, np.nan)
    return res
