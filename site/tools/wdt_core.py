"""
wdt_core.py — WDT Shared Core Mechanics
========================================
Single source of truth for parameters, the rate function, and the Route C
simulation engine used across:

  3.4.1  generate_appc_full.py        VAL.A Appendix C tables
  3.4.2  generate_illustrative.py     VAL main body citation figures
  3.4.3  generate_worked_examples.py  VAL.B worked example figures
  3.4.4  generate_figures.py          VAL PNG figures
  7.3    WDT_Rates_and_Revenue_Python_Model.py  SSM / TCM / sweep

PARAMETER LOADING — single source of truth
-------------------------------------------
All parameters come from the TOML file (7.4_…_Params.toml). Call
load_params() to get a fully-populated dict.

  p['N']  is the LRR fill year produced by running the SSM at load time,
  not a hardcoded constant. This means N is always consistent with the
  active scenario in the TOML. The fallback is p['tcm_N'] (61) if the
  SSM never fills within the modelling window, with a printed warning.

  p['V0_m'] is read from [val] V0_m in the TOML. All parameters are
  now derived from the TOML; there are no hardcoded values in this file.

RECORD FIELD GUARANTEE
-----------------------
simulate() records always contain:
  t, V, W, f, cum, L, rate, delta, q

simulate_sell() return dict always contains:
  t, V_sell, W_sell, f_N, delta_sell, rate_sell, L_sell, TW, cum_after

run_sim() return dict always contains:
  TW, TTP, Refunds, Net, records, sell, g_use

simulate_sell_year is an alias for simulate_sell, for compatibility with
7.3 which uses that name throughout.

BETA FORMULA
------------
Additive form confirmed from Excel cell: g_eff = g + β·ln(α)
VAL.A §B.3 states the multiplicative form incorrectly.
"""

import math
import tomllib
from pathlib import Path

# ─────────────────────────────────────────────────────────────
# TOML PATH — resolved relative to this file
# ─────────────────────────────────────────────────────────────

_DEFAULT_TOML = Path(__file__).parent / '260812_WDT_Params.toml'

# ─────────────────────────────────────────────────────────────
# RATE FUNCTION
# ─────────────────────────────────────────────────────────────

def tau(W_m, p):
    """
    Marginal WDT rate on declared wealth W_m (£m).

    $\tau$(W) = $\tau_m$ / (1 + (($\tau_m$ − $\tau_0$) / $\tau_0$) × exp(−k × (W − W_min)))
    $\tau$(W) = 0  if W < W_min

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

    g_eff = g + β·ln(α)

    Confirmed from Excel cell (additive form).
    VAL.A §B.3 states the multiplicative form incorrectly.
    Returns g unchanged when β=0, α=1, or α≤0.
    """
    if beta == 0.0 or alpha == 1.0 or alpha <= 0.0:
        return g
    return g + beta * math.log(alpha)


# ─────────────────────────────────────────────────────────────
# PERIOD SIMULATION
# ─────────────────────────────────────────────────────────────

def simulate(V0_m, g_series, alpha, p):
    """
    Simulate one Route C taxpayer over N regular periods.

    Entry t=0: V=V0_m, f=1, W=alpha×V0_m, cum=0, no tax event.
    Each period t=1..N uses g_series[t-1].

    Returns a list of N+1 record dicts (t=0 through t=N), each with:
        t       period index
        V       true asset value (£m)
        W       declared wealth = f × alpha × V (£m)
        f       retained fraction (1.0 at entry)
        cum     cumulative tax paid to date (£m)
        L       tax / refund this period (£m; positive=tax, negative=refund)
        rate    $\tau$(W) this period
        delta   W − W_prev (0.0 at t=0)
        q       equity fraction transferred this period (0.0 at t=0)

    Reads k, tau_0, tau_m, W_min from dict p.
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

    sim    record list from simulate()
    g_next growth rate for the sell year
    p      parameter dict (k, tau_0, tau_m, W_min)

    Returns a dict with:
        t           period index (last sim period + 1)
        V_sell      true value at sale (£m)
        W_sell      declared wealth at sale = f_N × V_sell (£m)
        f_N         retained fraction from period N
        delta_sell  W_sell − W_N (£m)
        rate_sell   $\tau$(W_sell)
        L_sell      tax / refund at sale (£m)
        TW          terminal net worth = W_sell − L_sell (£m)
        cum_after   cumulative tax after sell settlement (£m)
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


# Alias: 7.3 uses simulate_sell_year throughout.
simulate_sell_year = simulate_sell


# ─────────────────────────────────────────────────────────────
# CONVENIENCE RUNNER — constant g
# ─────────────────────────────────────────────────────────────

def run_sim(p_in, alpha=None, beta=None, N=None, g=None):
    """
    Run a complete constant-g simulation (N holding periods + sell year).

    All keyword arguments override the corresponding value in p_in.

    Returns:
        TW       terminal net worth (£m)
        TTP      gross taxes paid (£m, positive)
        Refunds  gross refunds received (£m, negative)
        Net      TTP + Refunds — net lifetime tax (£m)
        records  simulate() record list
        sell     simulate_sell() return dict
        g_use    effective growth rate used (after beta adjustment)
    """
    alpha  = alpha if alpha is not None else p_in.get('alpha', 1.0)
    beta   = beta  if beta  is not None else p_in.get('beta',  0.0)
    N      = N     if N     is not None else p_in['N']
    g_base = g     if g     is not None else p_in['g']

    g_use  = g_eff(g_base, alpha, beta)
    sim_p  = {k: p_in[k] for k in ('k', 'tau_0', 'tau_m', 'W_min')}

    recs   = simulate(p_in['V0_m'], [g_use] * N, alpha, sim_p)
    sell   = simulate_sell(recs, g_use, sim_p)

    gross_tax = sum(r['L'] for r in recs[1:] if r['L'] > 0)
    gross_ref = sum(r['L'] for r in recs[1:] if r['L'] < 0)
    if sell['L_sell'] > 0:
        gross_tax += sell['L_sell']
    else:
        gross_ref += sell['L_sell']

    return {
        'TW':      sell['TW'],
        'TTP':     gross_tax,
        'Refunds': gross_ref,
        'Net':     gross_tax + gross_ref,
        'records': recs,
        'sell':    sell,
        'g_use':   g_use,
    }


# ─────────────────────────────────────────────────────────────
# CONVENIENCE RUNNER — historical return series
# ─────────────────────────────────────────────────────────────

def run_sim_hist(p_in, alpha=None, N=None):
    """
    Run a complete simulation using the actual historical return series
    from p_in['returns'] (N holding periods + sell year).

    p_in['returns'] must already be rotated to the active scenario's
    start year (load_params() does this automatically).  The first N
    values are used as the holding-period g_series; index N is used as
    the sell-year growth rate.

    No beta / signalling adjustment is applied — historical-series runs
    model honest-declaration mechanics, not signalling effects.

    Returns the same dict shape as run_sim():
        TW       terminal net worth (£m)
        TTP      gross taxes paid (£m, positive)
        Refunds  gross refunds received (£m, negative)
        Net      TTP + Refunds — net lifetime tax (£m)
        records  simulate() record list
        sell     simulate_sell() return dict
        g_use    None  (no single rate — series-based)
        g_mean   arithmetic mean of the N holding-period returns
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

    return {
        'TW':      sell['TW'],
        'TTP':     gross_tax,
        'Refunds': gross_ref,
        'Net':     gross_tax + gross_ref,
        'records': recs,
        'sell':    sell,
        'g_use':   None,
        'g_mean':  sum(g_series) / len(g_series) if g_series else 0.0,
    }


# ─────────────────────────────────────────────────────────────
# MINIMAL SSM — LRR FILL YEAR ONLY
# ─────────────────────────────────────────────────────────────

def _ssm_lrr_fill_year(p, max_N=71):
    """
    Run the minimal SSM needed to find the LRR fill year for the active
    scenario. Uses the same mechanics as 7.3's run_ssm() but returns
    only the fill year rather than the full row-by-row result set.

    This keeps the core independent of 7.3's full reporting machinery
    while sharing the identical arithmetic.

    Returns the integer LRR fill year, or None if LRR never fills
    within max_N periods.
    """
    returns       = p['returns']
    brackets      = p['brackets']
    srr_ratio     = p['srr_ratio']
    lrr_years     = p['lrr_years']
    budget_base   = p['budget_base']
    budget_growth = p['budget_growth']
    alpha         = 1.0  # SSM always uses honest declaration

    # ── Marginal pass ────────────────────────────────────────
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

    # ── SRR / LRR accumulation pass ──────────────────────────
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
                return N   # ← LRR fill year found

    return None  # LRR did not fill within max_N


def load_params(toml_path=None):
    """
    Load all model parameters from the TOML file and return a single
    dict p usable by every domain script and by the simulation engine.

    p['N'] is set to the LRR fill year produced by running the SSM on
    the active scenario. This is the correct VAL reference horizon — not
    a hardcoded constant, and not tcm_N (which is the full SSM window).

    If the SSM does not fill within 71 periods (should not happen at
    Balanced parameters), p['N'] falls back to p['tcm_N'] and a warning
    is printed.

    All keys are read directly from the TOML:
      k, tau_0, tau_m, W_min       — [rate]
      srr_ratio, lrr_years         — [swf]
      budget_base, budget_growth   — [budget]
      hist_mean, tcm_N             — [tcm]
      returns, canonical_returns,
        series_base_year,
        scenario_start_year        — [returns] + [tcm]
      tiers                        — [[tiers]]
      brackets                     — [[brackets]]
      meta, generate_charts        — [meta], [output]
      V0_m                         — [val]

    Additional convenience keys derived at load time:
      g        = hist_mean  (alias for VAL scripts that use p['g'])
      alpha    = 1.0        (default declaration ratio)
      beta     = 0.0        (default signalling multiplier)
      N        = LRR fill year from SSM (not tcm_N)
    """
    path = Path(toml_path) if toml_path else _DEFAULT_TOML
    with open(path, 'rb') as f:
        raw = tomllib.load(f)

    p = {}

    # ── Rate function ──────────────────────────────────────────
    p['tau_0'] = float(raw['rate']['tau_0'])
    p['tau_m'] = float(raw['rate']['tau_m'])
    p['k']     = float(raw['rate']['k'])
    p['W_min'] = float(raw['rate']['W_min'])

    # ── SWF sizing ────────────────────────────────────────────
    p['srr_ratio'] = float(raw['swf']['srr_ratio'])
    p['lrr_years'] = float(raw['swf']['lrr_years'])

    # ── Government expenditure ────────────────────────────────
    p['budget_base']   = float(raw['budget']['budget_base'])
    p['budget_growth'] = float(raw['budget']['budget_growth'])

    # ── Returns series ────────────────────────────────────────
    canonical              = [float(v) for v in raw['returns']['values']]
    p['series_base_year']  = int(raw['returns']['series_base_year'])
    p['canonical_returns'] = canonical

    scenario_start           = int(raw['tcm'].get('scenario_start_year',
                                                   p['series_base_year']))
    p['scenario_start_year'] = scenario_start
    offset                   = (scenario_start - p['series_base_year']) % len(canonical)
    p['returns']             = canonical[offset:] + canonical[:offset]

    # ── TCM / SSM settings ────────────────────────────────────
    p['tcm_N']     = int(raw['tcm']['snapshot_N'])   # 61 — full SSM window
    p['hist_mean'] = float(raw['tcm']['hist_mean'])  # 0.1045

    # ── Tiers ─────────────────────────────────────────────────
    p['tiers'] = [
        {'label':        t['label'],
         'weight':       float(t['weight']),
         'differential': float(t['differential'])}
        for t in raw['tiers']
    ]

    # ── Brackets ──────────────────────────────────────────────
    p['brackets'] = [
        {'label': b['label'],
         'N':     float(b['N_pop']),
         'V0_m':  float(b['V0_m'])}
        for b in raw['brackets']
    ]

    # ── Meta / output ─────────────────────────────────────────
    p['meta']            = raw.get('meta', {})
    p['generate_charts'] = bool(raw.get('output', {}).get('generate_charts', False))

    # ── VAL convenience keys ──────────────────────────────────
    p['V0_m']  = float(raw['val']['V0_m'])  # from [val] section in TOML
    p['g']     = p['hist_mean']  # alias: VAL scripts use p['g']
    p['alpha'] = 1.0
    p['beta']  = 0.0

    # ── N: LRR fill year from SSM ────────────────────────────
    # Run the minimal SSM on the active scenario to find the fill year.
    # This is what 7.3's main() does at runtime; we do it here so all
    # scripts get a consistent N without any hardcoding.
    lrr_N = _ssm_lrr_fill_year(p)
    if lrr_N is None:
        print(f"WARNING: wdt_core.load_params() — LRR did not fill within "
              f"71 periods for scenario starting {scenario_start}. "
              f"Falling back to tcm_N={p['tcm_N']}.")
        lrr_N = p['tcm_N']
    p['N'] = lrr_N

    # ── Sweep grids and canonical reference values ────────────
    # The [sweep] section is the single source of truth for all
    # hardcoded analytical grids and canonical baseline values used
    # by VAL.S and RATES.S scripts.  Exposed as p['sweep'] so every
    # script reads the same values after a single load_params() call.
    sw = raw.get('sweep', {})

    # Reconstruct range-encoded grids from [min, max, step] triples.
    def _range_grid(triple):
        mn, mx, st = triple
        return list(range(mn, mx + 1, st))

    p['sweep'] = {
        # Canonical baseline
        'tau_0_canon':  float(sw.get('tau_0_canon',  p['tau_0'])),
        'tau_m_canon':  float(sw.get('tau_m_canon',  p['tau_m'])),
        'k_canon':      float(sw.get('k_canon',      p['k'])),
        'W_min_canon':  float(sw.get('W_min_canon',  p['W_min'])),
        'N_canon':      int(  sw.get('N_canon',      p['N'])),
        'V0_canon':     float(sw.get('V0_canon',     p['V0_m'])),
        'g_canon':      float(sw.get('g_canon',      p['hist_mean'])),
        # Analysis constant
        'tzone_threshold': float(sw.get('tzone_threshold', 0.02)),
        # Shared analytical grids
        'g_vals':          [float(v) for v in sw.get('g_vals', [])],
        'alpha_vals':      [float(v) for v in sw.get('alpha_vals', [])],
        'over_alphas':     [float(v) for v in sw.get('over_alphas', [])],
        'under_alphas':    [float(v) for v in sw.get('under_alphas', [])],
        'n_sweep':         _range_grid([int(v) for v in sw['n_sweep']])
                           if 'n_sweep' in sw else list(range(5, 66)),
        'n_panel_vals':    [int(v)   for v in sw.get('n_panel_vals',  [])],
        'n_actual_vals':   [int(v)   for v in sw.get('n_actual_vals', [])],
        'v0_sweep_vals':   [float(v) for v in sw.get('v0_sweep_vals', [])],
        # VAL.S parameter sweep panels
        'tau0_panel_vals': [float(v) for v in sw.get('tau0_panel_vals', [])],
        'taum_panel_vals': [float(v) for v in sw.get('taum_panel_vals', [])],
        'k_panel_vals':    [float(v) for v in sw.get('k_panel_vals',    [])],
        'wmin_panel_vals': [float(v) for v in sw.get('wmin_panel_vals', [])],
        # VAL.S interaction surface grids
        'tau0_n_surface_tau0':  [t / 100 for t in
                                 _range_grid([int(v) for v in sw['tau0_n_surface_tau0']])]
                                 if 'tau0_n_surface_tau0' in sw else [],
        'tau0_n_surface_nceil': _range_grid([int(v) for v in sw['tau0_n_surface_nceil']])
                                 if 'tau0_n_surface_nceil' in sw else [],
        'k_v0_surface_k':  [float(v) for v in sw.get('k_v0_surface_k',  [])],
        'k_v0_surface_v0': [float(v) for v in sw.get('k_v0_surface_v0', [])],
        # VAL.A Appendix C table grids
        'appc_k_vals':    [float(v) for v in sw.get('appc_k_vals',    [])],
        'appc_v0_vals':   [int(v)   for v in sw.get('appc_v0_vals',   [])],
        'appc_over_vals': [float(v) for v in sw.get('appc_over_vals', [])],
        # RATES.S sweep grids — rate parameters
        'rates_tau_0_sweep': [float(v) for v in sw.get('rates_tau_0_sweep', [])],
        'rates_tau_m_sweep': [float(v) for v in sw.get('rates_tau_m_sweep', [])],
        'rates_k_sweep':     [float(v) for v in sw.get('rates_k_sweep',     [])],
        'rates_wmin_sweep':  [float(v) for v in sw.get('rates_wmin_sweep',  [])],
        # RATES.S sweep grids — SWF sizing parameters
        'rates_srr_ratio_sweep': [float(v) for v in sw.get('rates_srr_ratio_sweep', [])],
        'rates_lrr_years_sweep': [float(v) for v in sw.get('rates_lrr_years_sweep', [])],
    }

    return p
