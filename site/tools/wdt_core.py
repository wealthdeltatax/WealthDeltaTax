"""
wdt_core.py — WDT Shared Core Mechanics
========================================
Single source of truth for parameters, the rate function, and the Route C
simulation engine used across all VAL and RATES scripts.

PARAMETER LOADING
-----------------
All parameters come from the TOML file. Call load_params() to get a
fully-populated dict.  p['N'] is the LRR fill year from the SSM.

RECORD FIELD GUARANTEE
-----------------------
simulate() records always contain:
  t, V, W, f, cum, L, rate, delta, q

simulate_sell() return dict always contains:
  t, V_sell, W_sell, f_N, delta_sell, rate_sell, L_sell, TW, cum_after

run_sim() return dict always contains:
  TW, TTP, Refunds, Net, records, sell, g_use

TW_settled and Net_settled
--------------------------
run_sim() now returns two additional keys:

  TW_settled  — the economically correct terminal net worth, accounting for
                the post-sale tax/refund oscillation that the mechanism
                produces when the taxpayer holds cash after sale.

                After the sell event the taxpayer holds cash = W_sell - L_sell.
                That cash becomes their declared wealth; the delta each period
                is the negative of the prior period's L, producing a damped
                oscillation that converges to a fixed point.  This is normal,
                designed mechanism behaviour: an overstater who receives a
                large sell-year refund will pay additional tax in subsequent
                periods as that refund produces a positive delta; an
                understater who pays a large sell-year tax will receive small
                refunds as that payment produces negative deltas.

                TW (the naive sell-year figure) is retained for backward
                compatibility but should not be used in analysis.
                TW_settled is the primary output metric.

  Net_settled — Net lifetime tax including post-sale settlement taxes/refunds.
                Identity: TW_settled = W_sell_net - Net_settled, where
                W_sell_net is the gross terminal value before any sell-year
                settlement.  Net (holding-period only) is retained for
                backward compatibility.

SETTLEMENT METHODOLOGY
----------------------
settle_tw() iterates the post-sale cash-holding sequence to convergence.
Each period: delta = cash - prior_basis; L = tau(cash) * delta (subject to
lifetime cap); cash -= L; basis = cash.  The series converges because
|tau| < 1 everywhere, giving a geometric decay in the oscillation amplitude.

Convergence is rapid in policy-relevant cases (typically 10-20 iterations at
canonical parameters).  Extreme cases (alpha=0.1 at very high V0 and g) may
need up to ~500 iterations as the rate ceiling tau_m approaches 1.  The
default max_iter=2000 is sufficient for all tested parameter combinations.

BETA FORMULA
------------
Additive form: g_eff = g + beta * ln(alpha)
VAL.A §B.3 states the multiplicative form incorrectly.
"""

import math
import os
import functools
import tomllib
from pathlib import Path

# ─────────────────────────────────────────────────────────────
# TOML PATH
# ─────────────────────────────────────────────────────────────

_DEFAULT_TOML = Path(__file__).parent / '260812_WDT_Params.toml'


# ─────────────────────────────────────────────────────────────
# RATE FUNCTION
# ─────────────────────────────────────────────────────────────

def tau(W_m, p):
    """
    Marginal WDT rate on declared wealth W_m (£m).

    tau(W) = tau_m / (1 + ((tau_m - tau_0) / tau_0) * exp(-k * (W - W_min)))
    tau(W) = 0  if W < W_min

    Reads tau_0, tau_m, k, W_min from dict p.
    """
    if W_m < p['W_min']:
        return 0.0
    return p['tau_m'] / (
        1.0 + ((p['tau_m'] - p['tau_0']) / p['tau_0'])
        * math.exp(-p['k'] * (W_m - p['W_min']))
    )


# ─────────────────────────────────────────────────────────────
# EFFECTIVE GROWTH RATE
# ─────────────────────────────────────────────────────────────

def g_eff(g, alpha, beta):
    """
    Additive effective growth rate after signalling adjustment.
    g_eff = g + beta * ln(alpha)
    Returns g unchanged when beta=0, alpha=1, or alpha<=0.
    """
    if beta == 0.0 or alpha == 1.0 or alpha <= 0.0:
        return g
    return g + beta * math.log(alpha)


# ─────────────────────────────────────────────────────────────
# POST-SALE SETTLEMENT
# ─────────────────────────────────────────────────────────────

def settle_tw(sell_result, p, max_iter=2000, tol=1e-10):
    """
    Iteratively settle the post-sale tax/refund oscillation.

    After the sell event, the taxpayer holds cash = W_sell - L_sell.
    Modelling the simplifying assumption that they hold this cash with
    no further growth, each period produces:
      delta = cash - prior_basis  (the negative of the prior period's L)
      L     = tau(cash) * delta   (subject to lifetime cap)
      cash -= L; basis = cash

    The oscillation is damped because |tau| < 1, converging geometrically.
    The series models real mechanism behaviour: a large sell-year refund
    creates a positive delta next period (taxed); a large sell-year tax
    creates a negative delta next period (refunded). This continues until
    the residual is negligible.

    Parameters
    ----------
    sell_result : dict from simulate_sell()
    p           : parameter dict with keys k, tau_0, tau_m, W_min
    max_iter    : maximum iterations (2000 is sufficient for all tested cases)
    tol         : convergence threshold on |L| and |cum|

    Returns
    -------
    TW_settled     : float — settled terminal net worth
    net_settle_tax : float — sum of all post-sale L values
                     (positive = additional net tax; negative = additional net refund)
    n_iter         : int — iterations to convergence
    """
    sim_p  = {k: p[k] for k in ('k', 'tau_0', 'tau_m', 'W_min')}
    cash   = sell_result['TW']          # W_sell - L_sell
    basis  = sell_result['W_sell']      # carry the sell-year declared value as basis
    cum    = sell_result['cum_after']   # residual lifetime balance after sell
    net_settle_tax = 0.0

    for i in range(max_iter):
        delta = cash - basis
        if abs(delta) < tol and abs(cum) < tol:
            return cash, net_settle_tax, i
        rate = tau(cash, sim_p)
        L    = max(-cum, rate * delta) if (delta > 0.0 or cum > 0.0) else 0.0
        if abs(L) < tol:
            return cash, net_settle_tax, i
        net_settle_tax += L
        basis = cash
        cash  = cash - L
        cum  += L

    return cash, net_settle_tax, max_iter


# ─────────────────────────────────────────────────────────────
# PERIOD SIMULATION
# ─────────────────────────────────────────────────────────────

def simulate(V0_m, g_series, alpha, p):
    """
    Simulate one Route C taxpayer over N regular periods.

    Entry t=0: V=V0_m, f=1, W=alpha*V0_m, cum=0, no tax event.
    Each period t=1..N uses g_series[t-1].

    Returns a list of N+1 record dicts (t=0 through t=N), each with:
        t       period index
        V       true asset value (£m)
        W       declared wealth = f * alpha * V (£m)
        f       retained fraction (1.0 at entry)
        cum     cumulative net tax paid to date (£m)
        L       tax / refund this period (£m; positive=tax, negative=refund)
        rate    tau(W) this period
        delta   W - W_prev (0.0 at t=0)
        q       equity fraction transferred this period (0.0 at t=0)
    """
    N   = len(g_series)
    V   = V0_m
    f   = 1.0
    W   = alpha * V
    cum = 0.0

    records = [{
        't': 0, 'V': V, 'W': W, 'f': f, 'cum': cum,
        'L': 0.0, 'rate': tau(W, p), 'delta': 0.0, 'q': 0.0,
    }]

    for t in range(1, N + 1):
        g_t   = g_series[t - 1]
        V     = V * (1.0 + g_t)
        W_new = f * alpha * V
        rate  = tau(W_new, p)
        delta = W_new - W
        L     = max(-cum, rate * delta) if (delta > 0.0 or cum > 0.0) else 0.0
        q     = (L / W_new) if W_new != 0.0 else 0.0
        f     = f * (1.0 - q)
        cum  += L
        W     = W_new
        records.append({
            't': t, 'V': V, 'W': W_new, 'f': f, 'cum': cum,
            'L': L, 'rate': rate, 'delta': delta, 'q': q,
        })

    return records


# ─────────────────────────────────────────────────────────────
# TERMINAL SELL-YEAR EVENT
# ─────────────────────────────────────────────────────────────

def simulate_sell(sim, g_next, p):
    """
    Compute the terminal Route C sell event (period N+1).

    sim    : record list from simulate()
    g_next : growth rate for the sell year
    p      : parameter dict (k, tau_0, tau_m, W_min)

    Returns a dict with:
        t           period index (last sim period + 1)
        V_sell      true value at sale (£m)
        W_sell      declared wealth at sale = f_N * V_sell (£m)
        f_N         retained fraction from period N
        delta_sell  W_sell - W_N (£m)
        rate_sell   tau(W_sell)
        L_sell      tax / refund at sale (£m)
        TW          naive terminal net worth = W_sell - L_sell (£m)
                    NOTE: use TW_settled from run_sim() for analysis
        cum_after   cumulative net tax after sell settlement (£m)
    """
    last       = sim[-1]
    f_N        = last['f']
    W_N        = last['W']
    cum_N      = last['cum']
    V_N        = last['V']

    V_sell     = V_N * (1.0 + g_next)
    W_sell     = f_N * V_sell
    rate_sell  = tau(W_sell, p)
    delta_sell = W_sell - W_N
    L_sell     = (max(-cum_N, rate_sell * delta_sell)
                  if (delta_sell > 0.0 or cum_N > 0.0) else 0.0)

    return {
        't':          last['t'] + 1,
        'V_sell':     V_sell,
        'W_sell':     W_sell,
        'f_N':        f_N,
        'delta_sell': delta_sell,
        'rate_sell':  rate_sell,
        'L_sell':     L_sell,
        'TW':         W_sell - L_sell,
        'cum_after':  cum_N + L_sell,
    }


# Alias: used in some scripts
simulate_sell_year = simulate_sell


# ─────────────────────────────────────────────────────────────
# CONVENIENCE RUNNER — constant g
# ─────────────────────────────────────────────────────────────

def run_sim(p_in, alpha=None, beta=None, N=None, g=None):
    """
    Run a complete constant-g simulation (N holding periods + sell year),
    then settle the post-sale oscillation to convergence.

    All keyword arguments override the corresponding value in p_in.

    Returns
    -------
    TW          : naive terminal net worth at sell year (retained for
                  backward compatibility; do not use in analysis)
    TW_settled  : economically correct terminal net worth after post-sale
                  oscillation converges — PRIMARY OUTPUT METRIC
    TTP         : gross taxes paid during holding period (£m, positive)
    Refunds     : gross refunds received during holding period (£m, negative)
    Net         : TTP + Refunds — net holding-period tax (retained for
                  backward compatibility)
    Net_settled : net lifetime tax including post-sale settlement (£m)
                  Identity: TW_settled = W_sell_gross - Net_settled
    records     : simulate() record list
    sell        : simulate_sell() return dict
    g_use       : effective growth rate used (after beta adjustment)
    settle_iters: iterations to post-sale convergence
    """
    alpha  = alpha if alpha is not None else p_in.get('alpha', 1.0)
    beta   = beta  if beta  is not None else p_in.get('beta',  0.0)
    N      = N     if N     is not None else p_in['N']
    g_base = g     if g     is not None else p_in['g']

    g_use  = g_eff(g_base, alpha, beta)
    sim_p  = {k: p_in[k] for k in ('k', 'tau_0', 'tau_m', 'W_min')}

    recs = simulate(p_in['V0_m'], [g_use] * N, alpha, sim_p)
    sell = simulate_sell(recs, g_use, sim_p)

    gross_tax = sum(r['L'] for r in recs[1:] if r['L'] > 0)
    gross_ref = sum(r['L'] for r in recs[1:] if r['L'] < 0)
    if sell['L_sell'] > 0:
        gross_tax += sell['L_sell']
    else:
        gross_ref += sell['L_sell']

    # Post-sale settlement
    tw_settled, net_settle_tax, n_iter = settle_tw(sell, sim_p)
    net_settled = gross_tax + gross_ref + net_settle_tax

    return {
        'TW':           sell['TW'],         # naive; retained for compatibility
        'TW_settled':   tw_settled,         # PRIMARY: use this in analysis
        'TTP':          gross_tax,
        'Refunds':      gross_ref,
        'Net':          gross_tax + gross_ref,   # holding-period only; retained
        'Net_settled':  net_settled,             # PRIMARY: full lifetime net tax
        'records':      recs,
        'sell':         sell,
        'g_use':        g_use,
        'settle_iters': n_iter,
    }


# ─────────────────────────────────────────────────────────────
# CONVENIENCE RUNNER — historical return series
# ─────────────────────────────────────────────────────────────

def run_sim_hist(p_in, alpha=None, N=None):
    """
    Run a complete simulation using the actual historical return series
    from p_in['returns'], then settle the post-sale oscillation.

    No beta / signalling adjustment is applied.

    Returns the same dict shape as run_sim() with the addition of:
        g_mean : arithmetic mean of the N holding-period returns
        g_use  : None (series-based, no single rate)
    """
    alpha = alpha if alpha is not None else p_in.get('alpha', 1.0)
    N     = N     if N     is not None else p_in['N']

    if len(p_in['returns']) < N + 1:
        raise ValueError(
            f"run_sim_hist: need at least N+1={N+1} return values, "
            f"got {len(p_in['returns'])}."
        )

    g_series = p_in['returns'][:N]
    g_sell   = p_in['returns'][N]
    sim_p    = {k: p_in[k] for k in ('k', 'tau_0', 'tau_m', 'W_min')}

    recs = simulate(p_in['V0_m'], g_series, alpha, sim_p)
    sell = simulate_sell(recs, g_sell, sim_p)

    gross_tax = sum(r['L'] for r in recs[1:] if r['L'] > 0)
    gross_ref = sum(r['L'] for r in recs[1:] if r['L'] < 0)
    if sell['L_sell'] > 0:
        gross_tax += sell['L_sell']
    else:
        gross_ref += sell['L_sell']

    # Post-sale settlement
    tw_settled, net_settle_tax, n_iter = settle_tw(sell, sim_p)
    net_settled = gross_tax + gross_ref + net_settle_tax

    return {
        'TW':           sell['TW'],
        'TW_settled':   tw_settled,
        'TTP':          gross_tax,
        'Refunds':      gross_ref,
        'Net':          gross_tax + gross_ref,
        'Net_settled':  net_settled,
        'records':      recs,
        'sell':         sell,
        'g_use':        None,
        'g_mean':       sum(g_series) / len(g_series) if g_series else 0.0,
        'settle_iters': n_iter,
    }


# ─────────────────────────────────────────────────────────────
# MINIMAL SSM — LRR FILL YEAR ONLY
# ─────────────────────────────────────────────────────────────

def _ssm_lrr_fill_year(p, max_N=71):
    """
    Run the minimal SSM needed to find the LRR fill year.
    Returns the integer LRR fill year, or None if LRR never fills.
    """
    returns       = p['returns']
    brackets      = p['brackets']
    srr_ratio     = p['srr_ratio']
    lrr_years     = p['lrr_years']
    budget_base   = p['budget_base']
    budget_growth = p['budget_growth']
    alpha         = 1.0

    prev_agg_ttp = 0.0
    prev_agg_ref = 0.0
    marginals    = []

    for n in range(0, max_N):
        g_series = [returns[t] for t in range(1, n + 1)]
        g_sell   = returns[n + 1]
        agg_ttp  = 0.0
        agg_ref  = 0.0

        for b in brackets:
            sim = simulate(b['V0_m'], g_series, alpha, p)
            for r in sim[1:]:
                x = r['L'] * b['N'] / 1000.0
                if x > 0:
                    agg_ttp += x
                else:
                    agg_ref += x
            sy = simulate_sell(sim, g_sell, p)
            x  = sy['L_sell'] * b['N'] / 1000.0
            if x > 0:
                agg_ttp += x
            else:
                agg_ref += x

        delta_ttp     = agg_ttp - prev_agg_ttp
        delta_ref     = agg_ref - prev_agg_ref
        marginals.append({'N': n + 1, 'net': delta_ttp + delta_ref})
        prev_agg_ttp  = agg_ttp
        prev_agg_ref  = agg_ref

    srr_bal    = 0.0
    lrr_bal    = 0.0
    lrr_filled = False
    cum_net    = 0.0

    for m in marginals:
        N   = m['N']
        net = m['net']
        cum_net += net

        srr_target  = srr_ratio * (cum_net / N)
        new_srr     = srr_bal + net
        if new_srr >= srr_target:
            srr_surplus = new_srr - srr_target
            srr_bal     = srr_target
        else:
            srr_surplus = 0.0
            srr_bal     = new_srr

        budget_t   = budget_base * (1.0 + budget_growth) ** (N - 1)
        lrr_target = lrr_years * budget_t

        if not lrr_filled:
            lrr_bal += srr_surplus
            if lrr_bal >= lrr_target:
                lrr_filled = True
                return N

    return None


# ─────────────────────────────────────────────────────────────
# PARAMETER LOADING
# ─────────────────────────────────────────────────────────────

def load_params(toml_path=None):
    """
    Load all model parameters from the TOML file and return a single dict.

    p['N'] is set to the LRR fill year from the SSM on the active scenario.
    If the SSM does not fill within 71 periods, p['N'] falls back to
    p['tcm_N'] with a warning.
    """
    path = Path(toml_path) if toml_path else _DEFAULT_TOML
    with open(path, 'rb') as f:
        raw = tomllib.load(f)

    p = {}

    p['tau_0'] = float(raw['rate']['tau_0'])
    p['tau_m'] = float(raw['rate']['tau_m'])
    p['k']     = float(raw['rate']['k'])
    p['W_min'] = float(raw['rate']['W_min'])

    p['srr_ratio'] = float(raw['swf']['srr_ratio'])
    p['lrr_years'] = float(raw['swf']['lrr_years'])

    p['budget_base']   = float(raw['budget']['budget_base'])
    p['budget_growth'] = float(raw['budget']['budget_growth'])

    canonical              = [float(v) for v in raw['returns']['values']]
    p['series_base_year']  = int(raw['returns']['series_base_year'])
    p['canonical_returns'] = canonical

    scenario_start           = int(raw['tcm'].get('scenario_start_year',
                                                   p['series_base_year']))
    p['scenario_start_year'] = scenario_start
    offset                   = (scenario_start - p['series_base_year']) % len(canonical)
    p['returns']             = canonical[offset:] + canonical[:offset]

    p['tcm_N']     = int(raw['tcm']['snapshot_N'])
    p['hist_mean'] = float(raw['tcm']['hist_mean'])

    p['tiers'] = [
        {'label':        t['label'],
         'weight':       float(t['weight']),
         'differential': float(t['differential'])}
        for t in raw['tiers']
    ]

    p['brackets'] = [
        {'label': b['label'],
         'N':     float(b['N_pop']),
         'V0_m':  float(b['V0_m'])}
        for b in raw['brackets']
    ]

    p['meta']            = raw.get('meta', {})
    p['generate_charts'] = bool(raw.get('output', {}).get('generate_charts', False))

    p['V0_m']  = float(raw['val']['V0_m'])
    p['g']     = p['hist_mean']
    p['alpha'] = 1.0
    p['beta']  = 0.0

    lrr_N = _ssm_lrr_fill_year(p)
    if lrr_N is None:
        print(f"WARNING: wdt_core.load_params() — LRR did not fill within "
              f"71 periods for scenario starting {scenario_start}. "
              f"Falling back to tcm_N={p['tcm_N']}.")
        lrr_N = p['tcm_N']
    p['N'] = lrr_N

    sw = raw.get('sweep', {})

    def _range_grid(triple):
        mn, mx, st = triple
        return list(range(mn, mx + 1, st))

    p['sweep'] = {
        'tau_0_canon':  float(sw.get('tau_0_canon',  p['tau_0'])),
        'tau_m_canon':  float(sw.get('tau_m_canon',  p['tau_m'])),
        'k_canon':      float(sw.get('k_canon',      p['k'])),
        'W_min_canon':  float(sw.get('W_min_canon',  p['W_min'])),
        'N_canon':      int(  sw.get('N_canon',      p['N'])),
        'V0_canon':     float(sw.get('V0_canon',     p['V0_m'])),
        'g_canon':      float(sw.get('g_canon',      p['hist_mean'])),
        'tzone_threshold': float(sw.get('tzone_threshold', 0.02)),
        'g_vals':          [float(v) for v in sw.get('g_vals', [])],
        'alpha_vals':      [float(v) for v in sw.get('alpha_vals', [])],
        'over_alphas':     [float(v) for v in sw.get('over_alphas', [])],
        'under_alphas':    [float(v) for v in sw.get('under_alphas', [])],
        'n_sweep':         _range_grid([int(v) for v in sw['n_sweep']])
                           if 'n_sweep' in sw else list(range(5, 66)),
        'n_panel_vals':    [int(v)   for v in sw.get('n_panel_vals',  [])],
        'n_actual_vals':   [int(v)   for v in sw.get('n_actual_vals', [])],
        'v0_sweep_vals':   [float(v) for v in sw.get('v0_sweep_vals', [])],
        'tau0_panel_vals': [float(v) for v in sw.get('tau0_panel_vals', [])],
        'taum_panel_vals': [float(v) for v in sw.get('taum_panel_vals', [])],
        'k_panel_vals':    [float(v) for v in sw.get('k_panel_vals',    [])],
        'wmin_panel_vals': [float(v) for v in sw.get('wmin_panel_vals', [])],
        'tau0_n_surface_tau0':  [t / 100 for t in
                                 _range_grid([int(v) for v in sw['tau0_n_surface_tau0']])]
                                 if 'tau0_n_surface_tau0' in sw else [],
        'tau0_n_surface_nceil': _range_grid([int(v) for v in sw['tau0_n_surface_nceil']])
                                 if 'tau0_n_surface_nceil' in sw else [],
        'k_v0_surface_k':  [float(v) for v in sw.get('k_v0_surface_k',  [])],
        'k_v0_surface_v0': [float(v) for v in sw.get('k_v0_surface_v0', [])],
        'appc_k_vals':    [float(v) for v in sw.get('appc_k_vals',    [])],
        'appc_v0_vals':   [int(v)   for v in sw.get('appc_v0_vals',   [])],
        'appc_over_vals': [float(v) for v in sw.get('appc_over_vals', [])],
        'rates_tau_0_sweep': [float(v) for v in sw.get('rates_tau_0_sweep', [])],
        'rates_tau_m_sweep': [float(v) for v in sw.get('rates_tau_m_sweep', [])],
        'rates_k_sweep':     [float(v) for v in sw.get('rates_k_sweep',     [])],
        'rates_wmin_sweep':  [float(v) for v in sw.get('rates_wmin_sweep',  [])],
        'rates_srr_ratio_sweep': [float(v) for v in sw.get('rates_srr_ratio_sweep', [])],
        'rates_lrr_years_sweep': [float(v) for v in sw.get('rates_lrr_years_sweep', [])],
    }

    return p
