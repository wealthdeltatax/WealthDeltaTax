"""
wdt_core.py — WDT Shared Core Mechanics
========================================
Single source of truth for parameters, the rate function, and the Route C
simulation engine used across all VAL and RATES scripts.

PUBLIC API
----------
  tau(W_m, p)                         marginal WDT rate
  g_eff(g, alpha, beta)               effective growth rate with signalling
  simulate(V0_m, g_series, alpha, p)  holding-period simulation
  simulate_sell(sim, g_next, p)       terminal sell-year event
  settle_tw(sell_result, p)           post-sale oscillation to convergence
  run_sim(p_in, ...)                  constant-g convenience runner
  run_sim_hist(p_in, ...)             historical-series convenience runner
  decompose_tw_advantage(p, alpha, g) TW advantage decomposition (C.11)
  npv_tax(records, sell, rho)         PV of all tax cash flows for one run
  npv_tax_advantage(p, alpha, g, rho) C.12 NPV tax difference vs honest
  load_params(toml_path)              load and validate all parameters

RECORD FIELD GUARANTEE
-----------------------
simulate() records always contain:
  t, V, W, f, cum, L, rate, delta, q

simulate_sell() return dict always contains:
  t, V_sell, W_sell, f_N, delta_sell, rate_sell, L_sell, TW, cum_after

run_sim() / run_sim_hist() return dict always contains:
  TW, TW_settled, TTP, Refunds, Net, Net_settled,
  records, sell, g_use, settle_iters
  (run_sim_hist also returns g_mean; g_use is None)

PRIMARY OUTPUT METRICS
----------------------
TW_settled  -- economically correct terminal net worth, after post-sale
               tax/refund oscillation converges. TW (naive sell-year figure)
               is retained for backward compatibility only.

Net_settled -- net lifetime tax including post-sale settlement.

DECOMPOSITION IDENTITY (C.11)
------------------------------
decompose_tw_advantage() splits TW_settled(alpha) - TW_settled(1) into
three terms that sum EXACTLY to tw_advantage:

  tw_advantage = W_sell_delta - refund_delta - settle_delta

  W_sell_delta = W_sell(alpha) - W_sell(1)       [<= 0 for alpha>1]
  refund_delta = L_sell(alpha) - L_sell(1)        [<= 0 for alpha>1 at mod g]
  settle_delta = net_settle(alpha) - net_settle(1) [>= 0]

excess_periodic (holding-period net tax diff) is NOT additive in this
identity. It is returned as an informational field only. The incorrect
identity -excess_periodic - refund_delta - settle_delta was used in
Fig 08 v1 and has been corrected.

BETA FORMULA
------------
Additive: g_eff = g + beta * ln(alpha).
VAL.A section B.3 states the multiplicative form incorrectly.
"""

import math
import tomllib
from pathlib import Path

_DEFAULT_TOML = Path(__file__).parent / 'WDT_Params.toml'


# ─────────────────────────────────────────────────────────────
# RATE FUNCTION
# ─────────────────────────────────────────────────────────────

def tau(W_m, p):
    """
    Marginal WDT rate on declared wealth W_m (pounds m).

    tau(W) = tau_m / (1 + ((tau_m - tau_0) / tau_0) * exp(-k * (W - W_min)))
    tau(W) = 0  if W < W_min
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
    Effective growth rate after signalling adjustment (additive form).

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
    Iteratively settle the post-sale tax/refund oscillation to convergence.

    Starting state after sale:
      cash  = sell_result['TW']       (W_sell - L_sell)
      basis = sell_result['W_sell']   (carry sell-year declared value forward)
      cum   = sell_result['cum_after']

    Each iteration:
      delta = cash - basis
      L = tau(cash) * delta  if delta > 0 or cum > 0, else 0
          (floored at -cum by lifetime cap)
      cash -= L;  basis = cash;  cum += L

    Returns
    -------
    TW_settled     float  settled terminal net worth
    net_settle_tax float  sum of post-sale L (+ = net tax, - = net refund)
    n_iter         int    iterations to convergence
    """
    sim_p = {k: p[k] for k in ('k', 'tau_0', 'tau_m', 'W_min')}
    cash  = sell_result['TW']
    basis = sell_result['W_sell']
    cum   = sell_result['cum_after']
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
# HOLDING-PERIOD SIMULATION
# ─────────────────────────────────────────────────────────────

def simulate(V0_m, g_series, alpha, p):
    """
    Simulate one Route C taxpayer over N holding periods.

    At each period t the declared wealth is W = f * alpha * V.
    Tax L = tau(W) * delta is paid as fraction q = L/W of declared
    wealth, reducing the retained equity fraction: f' = f * (1 - q).

    Parameters
    ----------
    V0_m     initial true asset value (pounds m)
    g_series list of N growth rates (one per period)
    alpha    declaration ratio (1.0 = honest)
    p        parameter dict (k, tau_0, tau_m, W_min)

    Returns
    -------
    list of N+1 record dicts (t=0 through t=N), each with keys:
      t, V, W, f, cum, L, rate, delta, q
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
        V     = V * (1.0 + g_series[t - 1])
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

    At sale, alpha drops out entirely: W_sell = f_N * V_sell (not
    f_N * alpha * V_sell). The taxpayer receives their retained fraction
    of true sale proceeds. For overstaters, the prior declared basis
    (f_N * alpha * V_N) typically exceeds W_sell when alpha > (1+g),
    generating a negative delta_sell and a sell-year refund.

    Parameters
    ----------
    sim    record list from simulate()
    g_next growth rate for the sell year
    p      parameter dict (k, tau_0, tau_m, W_min)

    Returns
    -------
    dict with keys:
      t, V_sell, W_sell, f_N, delta_sell, rate_sell, L_sell, TW, cum_after
    """
    last       = sim[-1]
    f_N        = last['f']
    W_N        = last['W']
    cum_N      = last['cum']
    V_N        = last['V']

    V_sell     = V_N * (1.0 + g_next)
    W_sell     = f_N * V_sell            # alpha drops out at liquidation
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


# Alias retained for backward compatibility
simulate_sell_year = simulate_sell


# ─────────────────────────────────────────────────────────────
# INTERNAL HELPER
# ─────────────────────────────────────────────────────────────

def _holding_totals(recs):
    """
    Sum holding-period (t=1..N) L values into gross tax, gross refunds,
    and net. Sell year is excluded; callers add it separately.
    """
    gross_tax = sum(r['L'] for r in recs[1:] if r['L'] > 0)
    gross_ref = sum(r['L'] for r in recs[1:] if r['L'] < 0)
    return gross_tax, gross_ref, gross_tax + gross_ref


# ─────────────────────────────────────────────────────────────
# CONVENIENCE RUNNER — constant g
# ─────────────────────────────────────────────────────────────

def run_sim(p_in, alpha=None, beta=None, N=None, g=None):
    """
    Run a complete constant-g simulation then settle post-sale oscillation.

    All keyword arguments override the corresponding value in p_in.

    Returns dict with keys:
      TW           naive sell-year TW (backward compat; do not use)
      TW_settled   settled TW -- PRIMARY METRIC
      TTP          gross holding-period tax (pounds m, positive)
      Refunds      gross holding-period refunds (pounds m, negative)
      Net          TTP + Refunds, holding period only (backward compat)
      Net_settled  net lifetime tax including post-sale settlement -- PRIMARY
      records      simulate() list
      sell         simulate_sell() dict
      g_use        effective growth rate used
      settle_iters iterations to convergence
    """
    alpha  = alpha  if alpha  is not None else p_in.get('alpha', 1.0)
    beta   = beta   if beta   is not None else p_in.get('beta',  0.0)
    N      = N      if N      is not None else p_in['N']
    g_base = g      if g      is not None else p_in['g']

    g_use = g_eff(g_base, alpha, beta)
    sim_p = {k: p_in[k] for k in ('k', 'tau_0', 'tau_m', 'W_min')}

    recs = simulate(p_in['V0_m'], [g_use] * N, alpha, sim_p)
    sell = simulate_sell(recs, g_use, sim_p)

    gross_tax, gross_ref, _ = _holding_totals(recs)
    if sell['L_sell'] > 0:
        gross_tax += sell['L_sell']
    else:
        gross_ref += sell['L_sell']

    tw_settled, net_settle_tax, n_iter = settle_tw(sell, sim_p)
    net_settled = gross_tax + gross_ref + net_settle_tax

    return {
        'TW':          sell['TW'],
        'TW_settled':  tw_settled,
        'TTP':         gross_tax,
        'Refunds':     gross_ref,
        'Net':         gross_tax + gross_ref,
        'Net_settled': net_settled,
        'records':     recs,
        'sell':        sell,
        'g_use':       g_use,
        'settle_iters': n_iter,
    }


# ─────────────────────────────────────────────────────────────
# CONVENIENCE RUNNER — historical return series
# ─────────────────────────────────────────────────────────────

def run_sim_hist(p_in, alpha=None, N=None):
    """
    Run a simulation using p_in['returns'] then settle post-sale oscillation.
    No beta/signalling adjustment. g_use is None.

    Returns same dict as run_sim() plus g_mean (arithmetic mean of
    the N holding-period returns).
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

    gross_tax, gross_ref, _ = _holding_totals(recs)
    if sell['L_sell'] > 0:
        gross_tax += sell['L_sell']
    else:
        gross_ref += sell['L_sell']

    tw_settled, net_settle_tax, n_iter = settle_tw(sell, sim_p)
    net_settled = gross_tax + gross_ref + net_settle_tax

    return {
        'TW':          sell['TW'],
        'TW_settled':  tw_settled,
        'TTP':         gross_tax,
        'Refunds':     gross_ref,
        'Net':         gross_tax + gross_ref,
        'Net_settled': net_settled,
        'records':     recs,
        'sell':        sell,
        'g_use':       None,
        'g_mean':      sum(g_series) / len(g_series) if g_series else 0.0,
        'settle_iters': n_iter,
    }


# ─────────────────────────────────────────────────────────────
# TW ADVANTAGE DECOMPOSITION (C.11)
# ─────────────────────────────────────────────────────────────

def decompose_tw_advantage(p, alpha, g):
    """
    Split TW_settled(alpha) - TW_settled(1) into three additive terms.

    Correct identity (verified to machine precision):

      tw_advantage = W_sell_delta - refund_delta - settle_delta

    W_sell_delta = W_sell(alpha) - W_sell(1)
        Always <= 0 for alpha > 1. f_N is depleted faster by higher
        periodic tax, reducing the sell-year declared value W_sell = f_N * V_sell.

    refund_delta = L_sell(alpha) - L_sell(1)
        Always <= 0 for alpha > 1 when alpha > (1+g). The prior declared
        basis (f_N * alpha * V_N) exceeds sell proceeds (f_N * V_sell),
        producing a larger sell-year refund (more negative L_sell).

    settle_delta = net_settle_tax(alpha) - net_settle_tax(1)
        Always >= 0. A larger sell-year refund creates a larger positive
        delta in the next post-sale period, which is taxed back.

    excess_periodic = holding_net(alpha) - holding_net(1)
        Informational only. NOT additive in the identity. The excess
        periodic tax feeds into tw_advantage indirectly through f_N
        erosion, but excess_periodic >> -W_sell_delta (approximately 6x
        at canonical parameters) because most of the excess is returned
        via the sell-year refund.

    Parameters
    ----------
    p     parameter dict from load_params()
    alpha declaration ratio
    g     constant growth rate for holding period and sell year

    Returns
    -------
    dict with keys:
      W_sell_delta    pounds m  additive term 1 (f_N erosion effect)
      refund_delta    pounds m  additive term 2 (sell-year refund difference)
      settle_delta    pounds m  additive term 3 (post-sale damping difference)
      tw_advantage    pounds m  TW_settled(alpha) - TW_settled(1)
      excess_periodic pounds m  informational only
      f_ratio         float     f_N(alpha) / f_N(1)
      tw_honest       pounds m  TW_settled(1); denominator for pct tables
      identity_error  pounds m  should be ~0; non-zero indicates a bug
    """
    sim_p = {k: p[k] for k in ('k', 'tau_0', 'tau_m', 'W_min')}
    N     = p['N']
    g_ser = [g] * N

    # honest
    recs_h = simulate(p['V0_m'], g_ser, 1.0, sim_p)
    sell_h = simulate_sell(recs_h, g, sim_p)
    tw_h, net_settle_h, _ = settle_tw(sell_h, sim_p)
    _, _, holding_net_h = _holding_totals(recs_h)

    # declared
    recs_a = simulate(p['V0_m'], g_ser, alpha, sim_p)
    sell_a = simulate_sell(recs_a, g, sim_p)
    tw_a, net_settle_a, _ = settle_tw(sell_a, sim_p)
    _, _, holding_net_a = _holding_totals(recs_a)

    W_sell_delta    = sell_a['W_sell']    - sell_h['W_sell']
    refund_delta    = sell_a['L_sell']    - sell_h['L_sell']
    settle_delta    = net_settle_a        - net_settle_h
    tw_advantage    = tw_a               - tw_h
    excess_periodic = holding_net_a      - holding_net_h
    f_ratio         = (recs_a[-1]['f'] / recs_h[-1]['f']
                       if abs(recs_h[-1]['f']) > 1e-12 else 0.0)
    identity_error  = (W_sell_delta - refund_delta - settle_delta) - tw_advantage

    return {
        'W_sell_delta':    W_sell_delta,
        'refund_delta':    refund_delta,
        'settle_delta':    settle_delta,
        'tw_advantage':    tw_advantage,
        'excess_periodic': excess_periodic,
        'f_ratio':         f_ratio,
        'tw_honest':       tw_h,
        'identity_error':  identity_error,
    }

# ─────────────────────────────────────────────────────────────
# NPV TAX CALCULATION (C.12)
# ─────────────────────────────────────────────────────────────

def npv_tax(records, sell, rho):
    """
    Compute the present value of all tax cash flows for one simulation run.

    Discounts each holding-period payment L_t at period t and the sell-year
    payment L_sell at period N+1, all to t=0 using discount rate rho.

    Sign convention matches the rest of the model: positive L = tax paid,
    negative L = refund received. NPV_tax > 0 means a net tax position in
    PV terms.

    Parameters
    ----------
    records  list of N+1 record dicts from simulate() (t=0..N)
    sell     result dict from simulate_sell() (contains L_sell and t)
    rho      annual discount rate (fraction, e.g. 0.05)

    Returns
    -------
    float  NPV of all tax cash flows (£m, t=0 present value)
    """
    pv = 0.0
    for rec in records[1:]:          # t=1..N, skip t=0 (no payment)
        t   = rec['t']
        pv += rec['L'] / (1.0 + rho) ** t
    t_sell = sell['t']               # always N+1
    pv    += sell['L_sell'] / (1.0 + rho) ** t_sell
    return pv


def npv_tax_advantage(p, alpha, g, rho):
    """
    NPV tax difference: NPV_tax(alpha) - NPV_tax(1), as fraction of
    honest TW_settled (the C.12 metric).

    Positive = alpha pays MORE in PV terms than honest (disadvantage).
    Negative = alpha pays LESS in PV terms than honest (advantage).

    Sign convention is consistent with C.1: positive = understater pays more;
    negative = overstater pays less.

    Parameters
    ----------
    p     parameter dict from load_params()
    alpha declaration ratio
    g     constant growth rate for holding period and sell year
    rho   annual discount rate (fraction)

    Returns
    -------
    dict with keys:
      npv_alpha     float  NPV_tax(alpha) in £m
      npv_honest    float  NPV_tax(1) in £m
      npv_diff      float  npv_alpha - npv_honest in £m
      npv_diff_pct  float  npv_diff / TW_settled(1)  — the C.12 metric
      tw_honest     float  TW_settled(1) for the denominator
    """
    sim_p = {k: p[k] for k in ('k', 'tau_0', 'tau_m', 'W_min')}
    N     = p['N']
    g_ser = [g] * N

    recs_h = simulate(p['V0_m'], g_ser, 1.0, sim_p)
    sell_h = simulate_sell(recs_h, g, sim_p)
    tw_h, _, _ = settle_tw(sell_h, sim_p)

    recs_a = simulate(p['V0_m'], g_ser, alpha, sim_p)
    sell_a = simulate_sell(recs_a, g, sim_p)

    npv_h = npv_tax(recs_h, sell_h, rho)
    npv_a = npv_tax(recs_a, sell_a, rho)
    npv_diff = npv_a - npv_h
    denom    = tw_h if abs(tw_h) > 1e-12 else 1.0

    return {
        'npv_alpha':    npv_a,
        'npv_honest':   npv_h,
        'npv_diff':     npv_diff,
        'npv_diff_pct': npv_diff / denom,
        'tw_honest':    tw_h,
    }

# ─────────────────────────────────────────────────────────────
# MINIMAL SSM — LRR FILL YEAR
# ─────────────────────────────────────────────────────────────

def _ssm_lrr_fill_year(p, max_N=71):
    """
    Minimal Sovereign Wealth Fund Sizing Model to find the LRR fill year.
    Returns the integer fill year or None if LRR never fills within max_N.
    """
    returns       = p['returns']
    brackets      = p['brackets']
    srr_ratio     = p['srr_ratio']
    lrr_years     = p['lrr_years']
    budget_base   = p['budget_base']
    budget_growth = p['budget_growth']

    prev_agg_ttp = 0.0
    prev_agg_ref = 0.0
    marginals    = []

    for n in range(0, max_N):
        g_series = [returns[t] for t in range(1, n + 1)]
        g_sell   = returns[n + 1]
        agg_ttp  = 0.0
        agg_ref  = 0.0

        for b in brackets:
            sim = simulate(b['V0_m'], g_series, 1.0, p)
            for r in sim[1:]:
                x = r['L'] * b['N'] / 1000.0
                (agg_ttp if x > 0 else agg_ref).__add__  # just branch
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

        delta_ttp = agg_ttp - prev_agg_ttp
        delta_ref = agg_ref - prev_agg_ref
        marginals.append({'N': n + 1, 'net': delta_ttp + delta_ref})
        prev_agg_ttp = agg_ttp
        prev_agg_ref = agg_ref

    srr_bal    = 0.0
    lrr_bal    = 0.0
    lrr_filled = False
    cum_net    = 0.0

    for m in marginals:
        N   = m['N']
        net = m['net']
        cum_net += net

        srr_target = srr_ratio * (cum_net / N)
        new_srr    = srr_bal + net
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
                return N

    return None


# ─────────────────────────────────────────────────────────────
# PARAMETER LOADING
# ─────────────────────────────────────────────────────────────

def load_params(toml_path=None):
    """
    Load all model parameters from the TOML file and return a single dict.

    p['N'] is derived from the SSM LRR fill year. Falls back to
    p['tcm_N'] with a warning if the SSM does not fill within 71 periods.

    All monetary values in pounds m. All rates as decimals.
    """
    path = Path(toml_path) if toml_path else _DEFAULT_TOML
    with open(path, 'rb') as fh:
        raw = tomllib.load(fh)

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
    p['rho']   = float(raw['val']['rho'])
    p['g']     = p['hist_mean']
    p['alpha'] = 1.0
    p['beta']  = 0.0

    lrr_N = _ssm_lrr_fill_year(p)
    if lrr_N is None:
        print(f"WARNING: wdt_core.load_params() -- LRR did not fill within "
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
        'tzone_threshold':   float(sw.get('tzone_threshold', 0.02)),
        'g_vals':            [float(v) for v in sw.get('g_vals',        [])],
        'alpha_vals':        [float(v) for v in sw.get('alpha_vals',    [])],
        'over_alphas':       [float(v) for v in sw.get('over_alphas',   [])],
        'under_alphas':      [float(v) for v in sw.get('under_alphas',  [])],
        'n_sweep':           (_range_grid([int(v) for v in sw['n_sweep']])
                              if 'n_sweep' in sw else list(range(5, 66))),
        'n_panel_vals':      [int(v)   for v in sw.get('n_panel_vals',  [])],
        'n_actual_vals':     [int(v)   for v in sw.get('n_actual_vals', [])],
        'v0_sweep_vals':     [float(v) for v in sw.get('v0_sweep_vals', [])],
        'tau0_panel_vals':   [float(v) for v in sw.get('tau0_panel_vals', [])],
        'taum_panel_vals':   [float(v) for v in sw.get('taum_panel_vals', [])],
        'k_panel_vals':      [float(v) for v in sw.get('k_panel_vals',    [])],
        'wmin_panel_vals':   [float(v) for v in sw.get('wmin_panel_vals', [])],
        'tau0_n_surface_tau0':  ([t / 100 for t in
                                  _range_grid([int(v) for v in sw['tau0_n_surface_tau0']])]
                                 if 'tau0_n_surface_tau0' in sw else []),
        'tau0_n_surface_nceil': (_range_grid([int(v) for v in sw['tau0_n_surface_nceil']])
                                 if 'tau0_n_surface_nceil' in sw else []),
        'k_v0_surface_k':    [float(v) for v in sw.get('k_v0_surface_k',  [])],
        'k_v0_surface_v0':   [float(v) for v in sw.get('k_v0_surface_v0', [])],
        'appc_k_vals':       [float(v) for v in sw.get('appc_k_vals',    [])],
        'appc_v0_vals':      [int(v)   for v in sw.get('appc_v0_vals',   [])],
        'appc_over_vals':    [float(v) for v in sw.get('appc_over_vals', [])],
        'rates_tau_0_sweep': [float(v) for v in sw.get('rates_tau_0_sweep', [])],
        'rates_tau_m_sweep': [float(v) for v in sw.get('rates_tau_m_sweep', [])],
        'rates_k_sweep':     [float(v) for v in sw.get('rates_k_sweep',     [])],
        'rates_wmin_sweep':  [float(v) for v in sw.get('rates_wmin_sweep',  [])],
        'rates_srr_ratio_sweep': [float(v) for v in sw.get('rates_srr_ratio_sweep', [])],
        'rates_lrr_years_sweep': [float(v) for v in sw.get('rates_lrr_years_sweep', [])],
    }

    return p