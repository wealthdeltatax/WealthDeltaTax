"""
WDT Rates and Revenue — Model Module
======================================
Extracted from 7_3_260807_WDT_Rates_and_Revenue_Python_Model.py (v6).
Updated to v8 mechanics per Model_Updates.md.

This file contains only computational logic: parameter loading,
the SSM, the TCM, the start-year sweep, extremal profiles, and
the statistical pass. It has no file I/O, no matplotlib dependency,
and no Excel checker.

Output generation (Markdown report and charts) lives in rates_output.py,
which imports this module.

PUBLIC API
----------
  load_params(toml_path=None)              -> dict
  validate_params(p)                       -> None  (raises on error)
  run_ssm(p, max_N=71)                    -> list[dict]
  run_tcm(p, N=None, N_fill=None)         -> dict[float, list[dict]]
  run_start_year_sweep(p)                 -> list[dict]
  run_scenario_profiles(extremals, p)     -> list[dict]
  compute_statistics(sweep_results)       -> dict

  report_start_year_sweep(sweep, p)       -> dict   (also prints to stdout)
  report_scenario_profiles(prof, p)       -> None   (prints to stdout)
  report_statistics(stats, p)            -> None   (prints to stdout)

ARCHITECTURE
------------
  Inputs:     TOML parameters file via wdt_core.load_params().
  SSM:        cohort marginal model, N=1..max_N.
  SRR target: srr_ratio × (cumulative net income / N).
  LRR:        accumulates SRR surplus until floor target met,
              then funds government expenditure via 5-step priority.
  Rate fn:    tau_m / (1 + ((tau_m-tau_0)/tau_0) * exp(-k*(W-W_min))),
              0 if W < W_min.
  Route C:    equity transfer, delta on declared wealth.
  Sweep:      returns series rotated per calendar start year; 73 years.

POST-FILL MECHANICS (v8)
------------------------
Each year t after lrr_fill_year, in strict priority order:

  Step 1 — SRR from income:
    srr_contrib = min(max(net_t, 0), max(0, srr_target_t - srr_bal))
    srr_bal += srr_contrib;  remainder = net_t - srr_contrib

  Step 2 — LRR floor maintenance from remainder:
    lrr_contrib = min(max(remainder, 0), max(0, lrr_target_t - lrr_bal))
    lrr_bal += lrr_contrib;  remainder -= lrr_contrib

  Step 3 — LRR covers remaining SRR deficit:
    srr_still_short = max(0, srr_target_t - srr_bal)
    lrr_to_srr = min(lrr_bal, srr_still_short)
    lrr_bal -= lrr_to_srr;  srr_bal += lrr_to_srr
    → record lrr_failure_year when lrr_bal hits 0
    → record srr_failure_year when srr_bal hits 0

  Step 4 — Surplus above SRR target tops up LRR toward floor:
    if srr_bal >= srr_target_t and remainder > 0:
        lrr_topup = min(remainder, max(0, lrr_target_t - lrr_bal))
        lrr_bal += lrr_topup;  remainder -= lrr_topup

  Step 5 — Labour tax relief:
    cov_frac_t = max(0, remainder) / budget_t
    → set to 0 if either failure condition already reached in a prior year

FAILURE CONDITIONS
------------------
  lrr_failure_year: first t where lrr_bal reaches 0 (buffer exhausted).
                    Ordering always lrr_failure → srr_failure.
  srr_failure_year: first t where srr_bal reaches 0 (refund guarantee broken).

COVERAGE WINDOWS
----------------
  For W in {5, 10, 20, 50}: average cov_frac_t over post-fill years 1..W,
  wrapping the return series cyclically. Zero in failure years drags the average.
  Metrics: ssm_cov_W, tcm_cov_W, zero_cov_years_W, min_lrr_bal_W,
           lrr_below_floor_years_W.

METRICS RETIRED (v8)
---------------------
  lrr_breach_year, years_fill_to_breach, max_lrr_breach,
  srr_breach_covered, ssm_post_fill_coverage (old), tcm_post_fill_coverage (old).

METRICS ADDED (v8)
-------------------
Per start year:
  lrr_failure_year, srr_failure_year, lrr_srr_failure_gap
  For W in {5,10,20,50}: ssm_cov_W, tcm_cov_W, zero_cov_years_W,
                          min_lrr_bal_W, lrr_below_floor_years_W

EXTREMAL DIMENSIONS (v8)
-------------------------
  Speed:       fastest / slowest LRR fill year (unchanged)
  Margin:      thinnest / largest LRR surplus at fill (unchanged)
  Durability:  highest / lowest 50yr average SSM coverage fraction (replaces breach lag)
  Resilience:  latest / earliest LRR failure year (None = no failure = best case)
"""

import math
from pathlib import Path

from wdt_core import (load_params as _core_load_params,
                      tau, simulate, simulate_sell_year)

DEFAULT_PARAMS = Path(__file__).parent / 'WDT_Params.toml'

# Coverage windows (years) — order matters for reporting
COVERAGE_WINDOWS = [5, 10, 20, 50]


# ─────────────────────────────────────────────────────────────
# SECTION 1 — PARAMETER LOADING
# ─────────────────────────────────────────────────────────────

def load_params(toml_path=None):
    """
    Load and assemble all model parameters from the TOML file.

    Thin wrapper around wdt_core.load_params(); all TOML reading,
    series rotation, and parameter assembly live there.
    Returns a dict used by all model functions.
    """
    path = str(Path(toml_path) if toml_path else DEFAULT_PARAMS)
    return _core_load_params(path)


def validate_params(p):
    """
    Structural sanity checks on loaded parameters.
    Raises ValueError / AssertionError on hard errors;
    prints warnings for soft issues.
    """
    assert len(p['returns']) == 73, \
        f"Expected 73 return values, got {len(p['returns'])}"
    assert len(p['tiers']) >= 1,    "No tier definitions found"
    assert len(p['brackets']) >= 1, "No bracket definitions found"

    w_sum = sum(t['weight'] for t in p['tiers'])
    if abs(w_sum - 1.0) > 1e-6:
        print(f"  WARNING: tier weights sum to {w_sum:.6f}, expected 1.0")

    wm_diff = sum(t['weight'] * t['differential'] for t in p['tiers'])
    if abs(wm_diff) > 1e-6:
        print(f"  WARNING: weighted-mean tier differential = {wm_diff:.2e}, expected ~0")

    if p['tau_0'] <= 0 or p['tau_0'] >= p['tau_m']:
        raise ValueError(f"tau_0={p['tau_0']} must be in (0, tau_m={p['tau_m']})")
    if p['tau_m'] > 1.0:
        raise ValueError(f"tau_m={p['tau_m']} > 1.0")
    if p['W_min'] < 0:
        raise ValueError(f"W_min={p['W_min']} must be non-negative")

    print("  Parameter validation: OK")


# ─────────────────────────────────────────────────────────────
# SECTION 2 — CORE MECHANICS (re-exported from wdt_core)
# ─────────────────────────────────────────────────────────────

# tau(), simulate(), simulate_sell_year() imported above.


# ─────────────────────────────────────────────────────────────
# SECTION 3 — SSM
# ─────────────────────────────────────────────────────────────

def _post_fill_step(net_t, srr_bal, lrr_bal, srr_target_t, lrr_target_t,
                    budget_t, lrr_failed, srr_failed):
    """
    Apply one year of the 5-step post-fill priority mechanic.

    Parameters
    ----------
    net_t        : float   marginal net revenue this year (£b)
    srr_bal      : float   SRR balance entering this year
    lrr_bal      : float   LRR balance entering this year
    srr_target_t : float   SRR target this year
    lrr_target_t : float   LRR target (floor) this year
    budget_t     : float   government expenditure this year (£b)
    lrr_failed   : bool    LRR already failed in a prior year
    srr_failed   : bool    SRR already failed in a prior year

    Returns
    -------
    dict with keys:
      srr_bal, lrr_bal, cov_frac,
      lrr_newly_failed (bool), srr_newly_failed (bool)
    """
    # Step 1 — SRR from income
    srr_gap    = max(0.0, srr_target_t - srr_bal)
    srr_contrib = min(max(net_t, 0.0), srr_gap)
    srr_bal    += srr_contrib
    remainder   = net_t - srr_contrib

    # Step 2 — LRR floor maintenance from remainder
    lrr_gap    = max(0.0, lrr_target_t - lrr_bal)
    lrr_contrib = min(max(remainder, 0.0), lrr_gap)
    lrr_bal    += lrr_contrib
    remainder  -= lrr_contrib

    # Step 3 — LRR covers remaining SRR deficit
    srr_still_short = max(0.0, srr_target_t - srr_bal)
    lrr_to_srr      = min(lrr_bal, srr_still_short)
    lrr_bal        -= lrr_to_srr
    srr_bal        += lrr_to_srr

    lrr_newly_failed = (not lrr_failed) and lrr_bal <= 0.0
    srr_newly_failed = (not srr_failed) and srr_bal <= 0.0

    # Step 4 — Surplus tops up LRR toward floor
    if srr_bal >= srr_target_t and remainder > 0.0:
        lrr_headroom = max(0.0, lrr_target_t - lrr_bal)
        lrr_topup    = min(remainder, lrr_headroom)
        lrr_bal     += lrr_topup
        remainder   -= lrr_topup

    # Step 5 — Labour tax relief coverage fraction
    # Zero if either failure condition has been reached (including this year)
    if lrr_failed or srr_failed or lrr_newly_failed or srr_newly_failed:
        cov_frac = 0.0
    else:
        cov_frac = max(0.0, remainder) / budget_t if budget_t > 0.0 else 0.0

    return {
        'srr_bal':          srr_bal,
        'lrr_bal':          lrr_bal,
        'cov_frac':         cov_frac,
        'lrr_newly_failed': lrr_newly_failed,
        'srr_newly_failed': srr_newly_failed,
    }


def _compute_coverage_windows(post_fill_cov_fracs, post_fill_lrr_bals,
                               post_fill_lrr_targets, returns_rotated,
                               lrr_fill_year, max_N, budget_base,
                               budget_growth, prefix='ssm'):
    """
    Compute per-window coverage metrics from a list of post-fill annual values.

    post_fill_cov_fracs  : list of cov_frac_t for t = lrr_fill_year+1 .. max_N
    post_fill_lrr_bals   : matching LRR balances
    post_fill_lrr_targets: matching LRR targets
    returns_rotated      : full rotated returns series (for cyclic extension)
    lrr_fill_year        : the year LRR filled (1-indexed)
    max_N                : largest year computed (71 normally)
    budget_base, budget_growth: for computing budget in extended years

    Returns a dict keyed by f'{prefix}_cov_{W}' etc.
    """
    out = {}
    n_available = len(post_fill_cov_fracs)
    n_ret       = len(returns_rotated)

    for W in COVERAGE_WINDOWS:
        cov_vals       = []
        lrr_bal_vals   = []
        below_floor    = 0

        for i in range(W):
            if i < n_available:
                cov_vals.append(post_fill_cov_fracs[i])
                lrr_bal_vals.append(post_fill_lrr_bals[i])
                below_floor += (1 if post_fill_lrr_bals[i] < post_fill_lrr_targets[i]
                                else 0)
            else:
                # Cyclic extension: repeat the return series beyond max_N
                # using whatever cov_frac the model last produced.
                # Conservative: carry forward the last known cov_frac (0 if failed).
                last_cov = post_fill_cov_fracs[-1] if post_fill_cov_fracs else 0.0
                cov_vals.append(last_cov)
                # LRR balance: carry forward last known
                last_lrr = post_fill_lrr_bals[-1] if post_fill_lrr_bals else 0.0
                lrr_bal_vals.append(last_lrr)
                # LRR target grows with budget
                t_abs = lrr_fill_year + i   # 0-indexed post-fill offset → year
                lrr_tgt_ext = (3.0 * budget_base *
                               (1.0 + budget_growth) ** t_abs)
                below_floor += (1 if last_lrr < lrr_tgt_ext else 0)

        out[f'{prefix}_cov_{W}']                    = sum(cov_vals) / W
        out[f'{prefix}_zero_cov_years_{W}']         = sum(1 for v in cov_vals if v == 0.0)
        out[f'{prefix}_min_lrr_bal_{W}']            = min(lrr_bal_vals) if lrr_bal_vals else None
        out[f'{prefix}_lrr_below_floor_years_{W}']  = below_floor

    return out


def run_ssm(p, max_N=71):
    """
    SWF Solvency Model — cohort marginal approach, N=1..max_N.

    Capitalisation phase (up to lrr_fill_year): same as v7.
    Post-fill phase: 5-step priority mechanic per Model_Updates.md.

    Returns a list of dicts, one per year (N=1..max_N).

    Each year dict contains:
      year, g, ttp, refunds, net,
      srr_target, srr_balance, srr_surplus, (srr_surplus retained for compat)
      budget, lrr_target, lrr_balance, lrr_filled,
      cov_frac (0.0 during capitalisation; post-fill Step 5 value after)

    Final dict also carries window metrics:
      lrr_fill_year, srr_fill_year,
      lrr_surplus_at_fill, srr_balance_at_lrr_fill,
      lrr_failure_year, srr_failure_year, lrr_srr_failure_gap,
      ssm_cov_{W}, zero_cov_years_{W}, min_lrr_bal_{W},
      lrr_below_floor_years_{W}  for W in COVERAGE_WINDOWS
    """
    returns       = p['returns']
    brackets      = p['brackets']
    alpha         = 1.0
    srr_ratio     = p['srr_ratio']
    lrr_years     = p['lrr_years']
    budget_base   = p['budget_base']
    budget_growth = p['budget_growth']

    # ── marginal revenue pass ──────────────────────────────────
    prev_agg_ttp = 0.0
    prev_agg_ref = 0.0
    marginal = []

    for N in range(0, max_N):
        g_series = [returns[t] for t in range(1, N + 1)]
        g_sell   = returns[N + 1]
        agg_ttp = 0.0; agg_ref = 0.0
        for b in brackets:
            sim = simulate(b['V0_m'], g_series, alpha, p)
            for r in sim[1:]:
                x = r['L'] * b['N'] / 1000.0
                if x > 0: agg_ttp += x
                else:      agg_ref += x
            sy = simulate_sell_year(sim, g_sell, p)
            x  = sy['L_sell'] * b['N'] / 1000.0
            if x > 0: agg_ttp += x
            else:      agg_ref += x
        delta_ttp = agg_ttp - prev_agg_ttp
        delta_ref = agg_ref - prev_agg_ref
        marginal.append({'N': N + 1, 'ttp': delta_ttp, 'ref': delta_ref,
                         'net': delta_ttp + delta_ref,
                         'g':   returns[N + 1]})
        prev_agg_ttp = agg_ttp
        prev_agg_ref = agg_ref

    # ── balance tracking ──────────────────────────────────────
    srr_bal    = 0.0
    lrr_bal    = 0.0
    lrr_filled = False
    cum_net    = 0.0
    results    = []

    srr_fill_year           = None
    lrr_fill_year           = None
    lrr_surplus_at_fill     = 0.0
    srr_balance_at_lrr_fill = 0.0
    lrr_failure_year        = None
    srr_failure_year        = None
    lrr_failed              = False
    srr_failed              = False

    post_fill_cov_fracs   = []
    post_fill_lrr_bals    = []
    post_fill_lrr_targets = []

    for m in marginal:
        N   = m['N']
        net = m['net']
        cum_net += net
        budget_t   = budget_base * (1.0 + budget_growth) ** (N - 1)
        srr_target = srr_ratio * (cum_net / N)
        lrr_target = lrr_years * budget_t

        if not lrr_filled:
            # ── capitalisation phase ──────────────────────────
            new_srr = srr_bal + net
            if new_srr >= srr_target:
                srr_surplus = new_srr - srr_target
                srr_bal     = srr_target
            else:
                srr_surplus = 0.0
                srr_bal     = new_srr

            if srr_fill_year is None and srr_target > 0 and srr_bal >= srr_target * 0.9999:
                srr_fill_year = N

            lrr_bal += srr_surplus
            cov_frac = 0.0

            if lrr_bal >= lrr_target:
                lrr_filled              = True
                lrr_fill_year           = N
                lrr_surplus_at_fill     = lrr_bal - lrr_target
                srr_balance_at_lrr_fill = srr_bal

        else:
            # ── post-fill phase: 5-step priority ─────────────
            step = _post_fill_step(
                net, srr_bal, lrr_bal, srr_target, lrr_target,
                budget_t, lrr_failed, srr_failed,
            )
            srr_bal  = step['srr_bal']
            lrr_bal  = step['lrr_bal']
            cov_frac = step['cov_frac']
            srr_surplus = 0.0   # not meaningful in post-fill; kept for compat

            if step['lrr_newly_failed']:
                lrr_failure_year = N
                lrr_failed       = True
            if step['srr_newly_failed']:
                srr_failure_year = N
                srr_failed       = True

            post_fill_cov_fracs.append(cov_frac)
            post_fill_lrr_bals.append(lrr_bal)
            post_fill_lrr_targets.append(lrr_target)

        results.append({
            'year':        N,
            'g':           m['g'],
            'ttp':         m['ttp'],
            'refunds':     m['ref'],
            'net':         net,
            'srr_target':  srr_target,
            'srr_balance': srr_bal,
            'srr_surplus': srr_surplus if not lrr_filled else 0.0,
            'budget':      budget_t,
            'lrr_target':  lrr_target,
            'lrr_balance': lrr_bal,
            'lrr_filled':  lrr_filled,
            'cov_frac':    cov_frac,
        })

    # ── attach summary metrics to the final result ────────────
    if results:
        last = results[-1]
        last['lrr_fill_year']           = lrr_fill_year
        last['srr_fill_year']           = srr_fill_year
        last['lrr_surplus_at_fill']     = lrr_surplus_at_fill
        last['srr_balance_at_lrr_fill'] = srr_balance_at_lrr_fill
        last['lrr_failure_year']        = lrr_failure_year
        last['srr_failure_year']        = srr_failure_year
        last['lrr_srr_failure_gap']     = (
            (srr_failure_year - lrr_failure_year)
            if (lrr_failure_year is not None and srr_failure_year is not None)
            else None
        )

        if lrr_fill_year is not None:
            win = _compute_coverage_windows(
                post_fill_cov_fracs, post_fill_lrr_bals,
                post_fill_lrr_targets, returns, lrr_fill_year,
                max_N, budget_base, budget_growth, prefix='ssm',
            )
            last.update(win)
        else:
            for W in COVERAGE_WINDOWS:
                last[f'ssm_cov_{W}']                   = None
                last[f'ssm_zero_cov_years_{W}']         = None
                last[f'ssm_min_lrr_bal_{W}']            = None
                last[f'ssm_lrr_below_floor_years_{W}']  = None

    return results


# ─────────────────────────────────────────────────────────────
# SECTION 3b — START-YEAR SWEEP
# ─────────────────────────────────────────────────────────────

def _rotate_returns(returns, calendar_start_year, series_base_year):
    """Rotate the canonical returns list so index 0 = calendar_start_year."""
    offset = (calendar_start_year - series_base_year) % len(returns)
    return returns[offset:] + returns[:offset]


def _ssm_stripped(rotated_returns, p):
    """
    Stripped SSM on a pre-rotated returns series.

    Applies the full v8 post-fill mechanics and coverage window
    calculations. Returns a dict of all per-start-year metrics.
    """
    alpha         = 1.0
    srr_ratio     = p['srr_ratio']
    lrr_years     = p['lrr_years']
    budget_base   = p['budget_base']
    budget_growth = p['budget_growth']
    brackets      = p['brackets']
    max_N         = 71

    # Marginal revenue pass
    prev_agg_ttp = 0.0
    prev_agg_ref = 0.0
    marginals = []
    for N in range(0, max_N):
        g_series = [rotated_returns[t] for t in range(1, N + 1)]
        g_sell   = rotated_returns[N + 1]
        agg_ttp = 0.0; agg_ref = 0.0
        for b in brackets:
            sim = simulate(b['V0_m'], g_series, alpha, p)
            for r in sim[1:]:
                x = r['L'] * b['N'] / 1000.0
                if x > 0: agg_ttp += x
                else:      agg_ref += x
            sy = simulate_sell_year(sim, g_sell, p)
            x  = sy['L_sell'] * b['N'] / 1000.0
            if x > 0: agg_ttp += x
            else:      agg_ref += x
        delta_ttp = agg_ttp - prev_agg_ttp
        delta_ref = agg_ref - prev_agg_ref
        marginals.append({'N': N + 1, 'net': delta_ttp + delta_ref})
        prev_agg_ttp = agg_ttp
        prev_agg_ref = agg_ref

    # Balance tracking
    srr_bal    = 0.0
    lrr_bal    = 0.0
    lrr_filled = False
    cum_net    = 0.0

    srr_fill_year           = None
    lrr_fill_year           = None
    lrr_surplus_at_fill     = 0.0
    srr_balance_at_lrr_fill = 0.0
    lrr_failure_year        = None
    srr_failure_year        = None
    lrr_failed              = False
    srr_failed              = False

    post_fill_cov_fracs   = []
    post_fill_lrr_bals    = []
    post_fill_lrr_targets = []

    for m in marginals:
        N   = m['N']
        net = m['net']
        cum_net += net
        budget_t   = budget_base * (1.0 + budget_growth) ** (N - 1)
        srr_target = srr_ratio * (cum_net / N)
        lrr_target = lrr_years * budget_t

        if not lrr_filled:
            new_srr = srr_bal + net
            if new_srr >= srr_target:
                srr_surplus = new_srr - srr_target
                srr_bal     = srr_target
            else:
                srr_surplus = 0.0
                srr_bal     = new_srr

            if srr_fill_year is None and srr_target > 0 and srr_bal >= srr_target * 0.9999:
                srr_fill_year = N

            lrr_bal += srr_surplus
            if lrr_bal >= lrr_target:
                lrr_filled              = True
                lrr_fill_year           = N
                lrr_surplus_at_fill     = lrr_bal - lrr_target
                srr_balance_at_lrr_fill = srr_bal
        else:
            step = _post_fill_step(
                net, srr_bal, lrr_bal, srr_target, lrr_target,
                budget_t, lrr_failed, srr_failed,
            )
            srr_bal = step['srr_bal']
            lrr_bal = step['lrr_bal']

            if step['lrr_newly_failed']:
                lrr_failure_year = N
                lrr_failed       = True
            if step['srr_newly_failed']:
                srr_failure_year = N
                srr_failed       = True

            post_fill_cov_fracs.append(step['cov_frac'])
            post_fill_lrr_bals.append(lrr_bal)
            post_fill_lrr_targets.append(lrr_target)

    lrr_srr_failure_gap = (
        (srr_failure_year - lrr_failure_year)
        if (lrr_failure_year is not None and srr_failure_year is not None)
        else None
    )

    result = {
        'srr_fill_year':           srr_fill_year,
        'lrr_fill_year':           lrr_fill_year,
        'lrr_surplus_at_fill':     lrr_surplus_at_fill,
        'srr_balance_at_lrr_fill': srr_balance_at_lrr_fill,
        'lrr_failure_year':        lrr_failure_year,
        'srr_failure_year':        srr_failure_year,
        'lrr_srr_failure_gap':     lrr_srr_failure_gap,
    }

    if lrr_fill_year is not None:
        win = _compute_coverage_windows(
            post_fill_cov_fracs, post_fill_lrr_bals,
            post_fill_lrr_targets, rotated_returns,
            lrr_fill_year, max_N, budget_base, budget_growth, prefix='ssm',
        )
        result.update(win)
    else:
        for W in COVERAGE_WINDOWS:
            result[f'ssm_cov_{W}']                   = None
            result[f'ssm_zero_cov_years_{W}']         = None
            result[f'ssm_min_lrr_bal_{W}']            = None
            result[f'ssm_lrr_below_floor_years_{W}']  = None

    return result


def run_start_year_sweep(p):
    """
    Run the stripped SSM and TCM coverage windows across all 73 calendar start years.

    Returns a list of dicts (one per start year) containing all SSM solvency
    metrics plus tcm_cov_{W} for each coverage window.
    """
    base  = p['series_base_year']
    raw   = p.get('canonical_returns', p['returns'])
    years = list(range(base, base + len(raw)))
    results = []

    for cal_year in years:
        rotated = _rotate_returns(raw, cal_year, base)
        metrics = _ssm_stripped(rotated, p)
        metrics['calendar_year'] = cal_year

        lrr_N = metrics.get('lrr_fill_year')
        srr_N = metrics.get('srr_fill_year')

        # TCM coverage windows
        if lrr_N is not None:
            p_rot = dict(p)
            p_rot['returns'] = rotated
            tcm_win = _tcm_coverage_windows(p_rot, lrr_N, srr_N or 1)
            metrics.update(tcm_win)
        else:
            for W in COVERAGE_WINDOWS:
                metrics[f'tcm_cov_{W}'] = None

        results.append(metrics)

    return results


# ─────────────────────────────────────────────────────────────
# SECTION 3c — EXTREMAL SCENARIO PROFILES
# ─────────────────────────────────────────────────────────────

def run_scenario_profiles(sweep_extremals, p):
    """
    Run the full SSM at each of the extremal start years identified
    by report_start_year_sweep().

    Returns a list of profile dicts, each containing:
      calendar_year, dimension_labels, ssm (full year-by-year list), metrics.
    """
    base = p['series_base_year']
    raw  = p.get('canonical_returns', p['returns'])

    label_map = {}
    for dim_label, key in [
        ('Worst speed',       'worst_speed'),
        ('Best speed',        'best_speed'),
        ('Worst margin',      'worst_margin'),
        ('Best margin',       'best_margin'),
        ('Worst durability',  'worst_durable'),
        ('Best durability',   'best_durable'),
        ('Worst resilience',  'worst_resilient'),
        ('Best resilience',   'best_resilient'),
    ]:
        r = sweep_extremals.get(key)
        if r is None:
            continue
        cy = r['calendar_year']
        label_map.setdefault(cy, []).append(dim_label)

    profiles = []
    for cy, labels in sorted(label_map.items()):
        rotated = _rotate_returns(raw, cy, base)
        p_rot   = dict(p)
        p_rot['returns'] = rotated
        ssm_result = run_ssm(p_rot, max_N=71)

        last = ssm_result[-1]
        metrics = {
            'srr_fill_year':           last.get('srr_fill_year'),
            'lrr_fill_year':           last.get('lrr_fill_year'),
            'lrr_surplus_at_fill':     last.get('lrr_surplus_at_fill', 0.0),
            'srr_balance_at_lrr_fill': last.get('srr_balance_at_lrr_fill', 0.0),
            'lrr_failure_year':        last.get('lrr_failure_year'),
            'srr_failure_year':        last.get('srr_failure_year'),
            'lrr_srr_failure_gap':     last.get('lrr_srr_failure_gap'),
        }
        for W in COVERAGE_WINDOWS:
            metrics[f'ssm_cov_{W}'] = last.get(f'ssm_cov_{W}')

        profiles.append({
            'calendar_year':    cy,
            'dimension_labels': labels,
            'ssm':              ssm_result,
            'metrics':          metrics,
        })

    return profiles


def report_scenario_profiles(profiles, p):
    """Print a structured comparison table for all extremal scenario profiles."""
    if not profiles:
        print("  No extremal profiles to report.")
        return

    W = 140
    print()
    print('=' * W)
    print('EXTREMAL SCENARIO PROFILES — full SSM at each extremal start year')
    print('=' * W)
    print(f"{'Start':>5}  {'Dimensions':<30}  {'SRRfill':>7}  {'LRRfill':>7}  "
          f"{'LRRsurp£b':>10}  {'LRRfail':>7}  {'SRRfail':>7}  {'gap':>5}  "
          f"{'cov10%':>7}  {'cov50%':>7}")
    print('-' * W)

    for prof in profiles:
        m   = prof['metrics']
        cy  = prof['calendar_year']
        dim = ', '.join(prof['dimension_labels'])

        def _c(v, w=7): return f"{v:>{w}}" if v is not None else f"{'—':>{w}}"
        lrr_s    = f"{m['lrr_surplus_at_fill']:>10.0f}" if m['lrr_fill_year'] else f"{'—':>10}"
        cov10    = (f"{m['ssm_cov_10']:>6.1%}"  if m.get('ssm_cov_10') is not None else f"{'—':>7}")
        cov50    = (f"{m['ssm_cov_50']:>6.1%}"  if m.get('ssm_cov_50') is not None else f"{'—':>7}")

        print(f"{cy:>5}  {dim:<30}  {_c(m['srr_fill_year'])}  {_c(m['lrr_fill_year'])}  "
              f"{lrr_s}  {_c(m['lrr_failure_year'])}  {_c(m['srr_failure_year'])}  "
              f"{_c(m['lrr_srr_failure_gap'], 5)}  {cov10}  {cov50}")

    print()
    print('  cov10/cov50: average SSM Step-5 coverage fraction over 10/50 post-fill years')
    print('  LRRfail/SRRfail: year LRR/SRR balance hits zero (None = no failure within window)')


# ─────────────────────────────────────────────────────────────
# SECTION 3d — STATISTICAL PASS
# ─────────────────────────────────────────────────────────────

CYCLE_BUCKETS = [
    ('Post-war growth  1947–59', 1947, 1959),
    ('Long boom        1960–79', 1960, 1979),
    ('Liberalisation   1980–99', 1980, 1999),
    ('Crisis decade    2000–19', 2000, 2019),
]


def _success(r):
    """Success = LRR fills within window AND LRR never fails."""
    return (r.get('lrr_fill_year') is not None and
            r.get('lrr_failure_year') is None)


def _median(vals):
    s = sorted(v for v in vals if v is not None)
    if not s:
        return None
    n = len(s)
    return s[n // 2] if n % 2 else (s[n // 2 - 1] + s[n // 2]) / 2


def _mean(vals):
    v = [x for x in vals if x is not None]
    return sum(v) / len(v) if v else None


def _pct(num, den):
    return 100.0 * num / den if den else 0.0


def compute_statistics(sweep_results):
    """
    Compute summary statistics over the full start-year sweep.

    Returns a dict with keys: overall, by_bucket, distributions.

    Success definition (v8): LRR fills within 71-year window AND
    LRR never fails (i.e. lrr_failure_year is None).
    """
    n_total       = len(sweep_results)
    n_success     = sum(1 for r in sweep_results if _success(r))
    n_lrr_fills   = sum(1 for r in sweep_results if r.get('lrr_fill_year') is not None)
    n_lrr_failure = sum(1 for r in sweep_results if r.get('lrr_failure_year') is not None)
    n_srr_failure = sum(1 for r in sweep_results if r.get('srr_failure_year') is not None)

    overall = {
        'n_total':        n_total,
        'n_success':      n_success,
        'success_rate':   _pct(n_success, n_total),
        'n_lrr_fills':    n_lrr_fills,
        'lrr_fill_rate':  _pct(n_lrr_fills, n_total),
        'n_lrr_failure':  n_lrr_failure,
        'lrr_failure_rate': _pct(n_lrr_failure, n_total),
        'n_srr_failure':  n_srr_failure,
        'srr_failure_rate': _pct(n_srr_failure, n_total),
    }

    by_bucket = []
    for label, yr_from, yr_to in CYCLE_BUCKETS:
        bucket = [r for r in sweep_results
                  if yr_from <= r['calendar_year'] <= yr_to]
        if not bucket:
            continue
        nb = len(bucket)
        ns = sum(1 for r in bucket if _success(r))
        nf = sum(1 for r in bucket if r.get('lrr_fill_year') is not None)
        by_bucket.append({
            'label':        label,
            'n':            nb,
            'n_success':    ns,
            'success_rate': _pct(ns, nb),
            'n_lrr_fills':  nf,
            'lrr_fill_rate':_pct(nf, nb),
        })

    def _dist(key):
        vals = [r[key] for r in sweep_results if r.get(key) is not None]
        return {
            'median': _median(vals),
            'mean':   _mean(vals),
            'min':    min(vals) if vals else None,
            'max':    max(vals) if vals else None,
            'n':      len(vals),
        }

    distributions = {
        'lrr_fill_year':      _dist('lrr_fill_year'),
        'srr_fill_year':      _dist('srr_fill_year'),
        'lrr_surplus_at_fill':_dist('lrr_surplus_at_fill'),
        'lrr_failure_year':   _dist('lrr_failure_year'),
        'srr_failure_year':   _dist('srr_failure_year'),
        'lrr_srr_failure_gap':_dist('lrr_srr_failure_gap'),
    }
    for W in COVERAGE_WINDOWS:
        distributions[f'ssm_cov_{W}'] = _dist(f'ssm_cov_{W}')
        distributions[f'tcm_cov_{W}'] = _dist(f'tcm_cov_{W}')

    return {
        'overall':      overall,
        'by_bucket':    by_bucket,
        'distributions':distributions,
    }


def report_statistics(stats, p):
    """Print the statistical pass summary to stdout."""
    W = 90
    print()
    print('=' * W)
    print('STATISTICAL PASS — success rates across all economic cycles')
    print(f"  Parameters: tau_0={p['tau_0']:.0%}  tau_m={p['tau_m']:.0%}  "
          f"k={p['k']}  W_min=£{p['W_min']}m  "
          f"SRR={p['srr_ratio']}×  LRR={p['lrr_years']}yrs")
    print('  Success = LRR fills within window AND LRR never fails')
    print('=' * W)

    ov = stats['overall']
    print()
    print('OVERALL (all 73 start years):')
    print(f"  Success rate:     {ov['success_rate']:>6.1f}%  "
          f"({ov['n_success']}/{ov['n_total']} start years)")
    print(f"  LRR fills:        {ov['lrr_fill_rate']:>6.1f}%  "
          f"({ov['n_lrr_fills']}/{ov['n_total']})")
    print(f"  LRR failures:     {ov['lrr_failure_rate']:>6.1f}%  "
          f"({ov['n_lrr_failure']}/{ov['n_total']})")
    print(f"  SRR failures:     {ov['srr_failure_rate']:>6.1f}%  "
          f"({ov['n_srr_failure']}/{ov['n_total']})")

    print()
    print('BY ECONOMIC CYCLE BUCKET:')
    print(f"  {'Bucket':<32}  {'N':>3}  {'Success%':>9}  {'LRRfill%':>9}")
    print('  ' + '-' * 58)
    for b in stats['by_bucket']:
        print(f"  {b['label']:<32}  {b['n']:>3}  "
              f"{b['success_rate']:>8.1f}%  {b['lrr_fill_rate']:>8.1f}%")

    print()
    print('KEY METRIC DISTRIBUTIONS (across all start years):')
    dist_rows = [
        ('lrr_fill_year',       'LRR breakeven year',          '{:.0f}'),
        ('srr_fill_year',       'SRR fill year',               '{:.0f}'),
        ('lrr_surplus_at_fill', 'LRR surplus at breakeven (£b)','{:.0f}'),
        ('lrr_failure_year',    'LRR failure year',            '{:.0f}'),
        ('srr_failure_year',    'SRR failure year',            '{:.0f}'),
        ('lrr_srr_failure_gap', 'LRR→SRR failure gap (yrs)',   '{:.0f}'),
    ]
    for W in COVERAGE_WINDOWS:
        dist_rows.append((f'ssm_cov_{W}', f'SSM coverage {W}yr avg', '{:.1%}'))
        dist_rows.append((f'tcm_cov_{W}', f'TCM coverage {W}yr avg', '{:.1%}'))

    print(f"  {'Metric':<32}  {'N':>3}  {'Min':>10}  "
          f"{'Median':>10}  {'Mean':>10}  {'Max':>10}")
    print('  ' + '-' * 82)
    for key, label, fmt in dist_rows:
        d = stats['distributions'].get(key, {})
        def _f(v, f=fmt): return f.format(v) if v is not None else '—'
        print(f"  {label:<32}  {d.get('n', 0):>3}  "
              f"{_f(d.get('min')):>10}  {_f(d.get('median')):>10}  "
              f"{_f(d.get('mean')):>10}  {_f(d.get('max')):>10}")


# ─────────────────────────────────────────────────────────────
# SECTION 4 — TCM
# ─────────────────────────────────────────────────────────────

def _tcm_marginal_net(p, N, rotated_returns=None):
    """
    Compute the aggregate marginal net revenue (£b) at year N from the TCM.

    This is the difference in cumulative aggregate net revenue between
    simulations run to year N and year N-1, summed across all tier×bracket
    cells with population weights.

    Uses the rotated return series in p['returns'] unless rotated_returns
    is provided explicitly.
    """
    returns  = rotated_returns if rotated_returns is not None else p['returns']
    brackets = p['brackets']
    alpha    = 1.0

    def _agg_net(n):
        total = 0.0
        for tier in p['tiers']:
            diff     = tier['differential']
            weight   = tier['weight']
            g_series = [returns[t] + diff for t in range(1, n + 1)]
            g_sell   = returns[n + 1] + diff
            for b in brackets:
                sim   = simulate(b['V0_m'], g_series, alpha, p)
                net_h = sum(r['L'] for r in sim[1:])
                sy    = simulate_sell_year(sim, g_sell, p)
                net_h += sy['L_sell']
                total += net_h * b['N'] * weight / 1000.0
        return total

    if N == 0:
        return 0.0
    return _agg_net(N) - _agg_net(N - 1)


def _tcm_coverage_windows(p, lrr_N, srr_N):
    """
    Run the TCM's own post-fill priority loop and compute coverage windows.

    The TCM has completely independent SRR/LRR balance trackers from the
    SSM. It runs year-by-year from 1..71, using marginal TCM revenue at
    each step. Coverage fractions are computed under the same 5-step
    priority as the SSM.

    Returns a dict keyed by 'tcm_cov_{W}' for W in COVERAGE_WINDOWS,
    plus 'tcm_lrr_failure_year', 'tcm_srr_failure_year'.
    """
    returns       = p['returns']
    srr_ratio     = p['srr_ratio']
    lrr_years     = p['lrr_years']
    budget_base   = p['budget_base']
    budget_growth = p['budget_growth']
    max_N         = 71

    srr_bal    = 0.0
    lrr_bal    = 0.0
    lrr_filled = False
    cum_net    = 0.0
    lrr_failed = False
    srr_failed = False
    tcm_lrr_failure_year = None
    tcm_srr_failure_year = None

    post_fill_cov_fracs   = []
    post_fill_lrr_bals    = []
    post_fill_lrr_targets = []

    for N in range(1, max_N + 1):
        net        = _tcm_marginal_net(p, N)
        cum_net   += net
        budget_t   = budget_base * (1.0 + budget_growth) ** (N - 1)
        srr_target = srr_ratio * (cum_net / N)
        lrr_target = lrr_years * budget_t

        if not lrr_filled:
            new_srr = srr_bal + net
            if new_srr >= srr_target:
                srr_surplus = new_srr - srr_target
                srr_bal     = srr_target
            else:
                srr_surplus = 0.0
                srr_bal     = new_srr
            lrr_bal += srr_surplus
            if lrr_bal >= lrr_target:
                lrr_filled = True
        else:
            step = _post_fill_step(
                net, srr_bal, lrr_bal, srr_target, lrr_target,
                budget_t, lrr_failed, srr_failed,
            )
            srr_bal = step['srr_bal']
            lrr_bal = step['lrr_bal']
            if step['lrr_newly_failed']:
                tcm_lrr_failure_year = N
                lrr_failed           = True
            if step['srr_newly_failed']:
                tcm_srr_failure_year = N
                srr_failed           = True
            post_fill_cov_fracs.append(step['cov_frac'])
            post_fill_lrr_bals.append(lrr_bal)
            post_fill_lrr_targets.append(lrr_target)

    # Compute window metrics (TCM prefix)
    result = {
        'tcm_lrr_failure_year': tcm_lrr_failure_year,
        'tcm_srr_failure_year': tcm_srr_failure_year,
    }

    if lrr_filled and post_fill_cov_fracs:
        # LRR fill year = the year at which the post-fill phase started.
        # len(post_fill_cov_fracs) counts years AFTER lrr_fill, so:
        #   tcm_lrr_N = max_N - len(post_fill_cov_fracs)
        tcm_lrr_N = max_N - len(post_fill_cov_fracs)
        win = _compute_coverage_windows(
            post_fill_cov_fracs, post_fill_lrr_bals,
            post_fill_lrr_targets, returns,
            tcm_lrr_N, max_N, budget_base, budget_growth, prefix='tcm',
        )
        # Only propagate the coverage fraction keys into the sweep row.
        # Auxiliary keys (zero_cov_years, min_lrr_bal, lrr_below_floor_years)
        # are available in full SSM runs but not needed per-row for TCM.
        for W in COVERAGE_WINDOWS:
            result[f'tcm_cov_{W}'] = win.get(f'tcm_cov_{W}')
    else:
        for W in COVERAGE_WINDOWS:
            result[f'tcm_cov_{W}'] = None

    return result


def run_tcm(p, N=None, N_fill=None):
    """
    Taxpayer Cohort Model at horizon N — bracket×tier output table.

    This function produces the detailed per-bracket output for the
    markdown report (B.3 tables). It remains structurally similar to v7
    but is now understood as a snapshot at horizon N rather than the
    source of coverage ratios (those come from _tcm_coverage_windows).

    Returns a dict keyed by tier differential (float) mapping to a list
    of bracket dicts. Each bracket dict contains:
      label, N_pop, cell_pop, V0_m, V_at_N, TW,
      avg_net_gbp, wealth_burden, eff_rate,
      revenue_m, post_fill_net_m, post_fill_revenue_m, post_fill_net_gbp.
    """
    returns   = p['returns']
    brackets  = p['brackets']
    N         = N if N is not None else p['tcm_N']
    N_fill    = N_fill if N_fill is not None else N
    alpha     = 1.0
    N_periods = N + 1
    post_fill_periods = N - N_fill  # guarded below

    results = {}

    for tier in p['tiers']:
        diff   = tier['differential']
        weight = tier['weight']
        g_series = [returns[t] + diff for t in range(1, N + 1)]
        g_sell   = returns[N + 1] + diff

        tier_results = []
        for b in brackets:
            sim   = simulate(b['V0_m'], g_series, alpha, p)
            sy    = simulate_sell_year(sim, g_sell, p)
            V_at_N = sim[N]['V']

            total_net     = sum(r['L'] for r in sim[1:]) + sy['L_sell']
            post_fill_net = sum(r['L'] for r in sim[N_fill:N])

            W_sell   = sy['W_sell']
            L_sell   = sy['L_sell']
            tau_sell = sy['rate_sell']
            TW = (W_sell - L_sell / tau_sell) \
                 if (tau_sell > 0.0 and L_sell > 0.0) else W_sell

            avg_net_m           = total_net / N_periods
            avg_net_gbp         = avg_net_m * 1e6
            wealth_burden       = avg_net_m / TW if TW != 0.0 else 0.0
            eff_rate            = total_net / TW if TW != 0.0 else 0.0
            revenue_m           = avg_net_m * b['N'] * weight
            post_fill_net_m     = (post_fill_net / post_fill_periods
                                    if post_fill_periods > 0 else 0.0)
            post_fill_revenue_m = post_fill_net_m * b['N'] * weight
            cell_pop            = b['N'] * weight

            tier_results.append({
                'label':               b['label'],
                'N_pop':               b['N'],
                'cell_pop':            cell_pop,
                'V0_m':                b['V0_m'],
                'V_at_N':              V_at_N,
                'TW':                  TW,
                'avg_net_gbp':         avg_net_gbp,
                'wealth_burden':       wealth_burden,
                'eff_rate':            eff_rate,
                'revenue_m':           revenue_m,
                'post_fill_net_m':     post_fill_net_m,
                'post_fill_revenue_m': post_fill_revenue_m,
                'post_fill_net_gbp':   post_fill_net_m * 1e6,
            })
        results[diff] = tier_results

    return results


# ─────────────────────────────────────────────────────────────
# SECTION 5 — SWEEP REPORTING
# ─────────────────────────────────────────────────────────────

def report_start_year_sweep(sweep_results, p):
    """
    Print the full 73-row sweep table to stdout and return the eight
    extremal records plus the full results list.

    Extremal dimensions (v8):
      Speed:       fastest / slowest LRR fill year
      Margin:      thinnest / largest LRR surplus at fill
      Durability:  highest / lowest 50yr SSM coverage fraction
      Resilience:  latest / earliest LRR failure year
                   (no-failure rows are best case for resilience)

    Return value is a dict with keys:
      worst_speed, best_speed, worst_margin, best_margin,
      worst_durable, best_durable, worst_resilient, best_resilient, all.
    """
    W_line = 148
    print()
    print('=' * W_line)
    print('START-YEAR SENSITIVITY SWEEP  (all calendar years, Balanced parameters)')
    print('=' * W_line)

    filled = [r for r in sweep_results if r.get('lrr_fill_year') is not None]

    # Speed
    worst_speed = max(filled, key=lambda r: r['lrr_fill_year']) if filled else None
    best_speed  = min(filled, key=lambda r: r['lrr_fill_year']) if filled else None

    # Margin
    worst_margin = min(filled, key=lambda r: r['lrr_surplus_at_fill']) if filled else None
    best_margin  = max(filled, key=lambda r: r['lrr_surplus_at_fill']) if filled else None

    # Durability — 50yr SSM coverage fraction
    dur_rows = [r for r in filled if r.get('ssm_cov_50') is not None]
    worst_durable = min(dur_rows, key=lambda r: r['ssm_cov_50']) if dur_rows else None
    best_durable  = max(dur_rows, key=lambda r: r['ssm_cov_50']) if dur_rows else None

    # Resilience — latest/earliest LRR failure year
    # No-failure rows are the best case; among those pick fastest fill.
    failure_rows   = [r for r in filled if r.get('lrr_failure_year') is not None]
    nofailure_rows = [r for r in filled if r.get('lrr_failure_year') is None]
    worst_resilient = (min(failure_rows, key=lambda r: r['lrr_failure_year'])
                       if failure_rows else None)
    if nofailure_rows:
        best_resilient = min(nofailure_rows, key=lambda r: r['lrr_fill_year'])
    elif failure_rows:
        best_resilient = max(failure_rows, key=lambda r: r['lrr_failure_year'])
    else:
        best_resilient = None

    def _flags(r):
        fs = []
        if worst_speed    and r['calendar_year'] == worst_speed['calendar_year']:    fs.append('↓SPD')
        if best_speed     and r['calendar_year'] == best_speed['calendar_year']:     fs.append('↑SPD')
        if worst_margin   and r['calendar_year'] == worst_margin['calendar_year']:   fs.append('↓MRG')
        if best_margin    and r['calendar_year'] == best_margin['calendar_year']:    fs.append('↑MRG')
        if worst_durable  and r['calendar_year'] == worst_durable['calendar_year']:  fs.append('↓DUR')
        if best_durable   and r['calendar_year'] == best_durable['calendar_year']:   fs.append('↑DUR')
        if worst_resilient and r['calendar_year'] == worst_resilient['calendar_year']: fs.append('↓RES')
        if best_resilient  and r['calendar_year'] == best_resilient['calendar_year']:  fs.append('↑RES')
        return ' '.join(fs)

    print(f"{'Start':>5}  {'SRRfill':>7}  {'LRRfill':>7}  {'LRRsurp£b':>10}  "
          f"{'LRRfail':>7}  {'SRRfail':>7}  {'gap':>5}  "
          f"{'SSMcov5%':>9}  {'SSMcov10%':>10}  {'SSMcov20%':>10}  {'SSMcov50%':>10}  "
          f"{'TCMcov10%':>10}  {'TCMcov50%':>10}  Flags")
    print('-' * (W_line + 30))

    for r in sweep_results:
        def _f(v, w=7): return f"{v:>{w}}" if v is not None else f"{'—':>{w}}"
        def _fp(v, w=10):
            return f"{v:>{w-1}.1%}" if v is not None else f"{'—':>{w}}"
        flags     = _flags(r)
        lrr_surp  = (f"{r['lrr_surplus_at_fill']:>10.0f}"
                     if r.get('lrr_fill_year') is not None else f"{'—':>10}")
        row = (f"{r['calendar_year']:>5}  {_f(r.get('srr_fill_year'))}  "
               f"{_f(r.get('lrr_fill_year'))}  {lrr_surp}  "
               f"{_f(r.get('lrr_failure_year'))}  {_f(r.get('srr_failure_year'))}  "
               f"{_f(r.get('lrr_srr_failure_gap'), 5)}  "
               f"{_fp(r.get('ssm_cov_5'))}  {_fp(r.get('ssm_cov_10'))}  "
               f"{_fp(r.get('ssm_cov_20'))}  {_fp(r.get('ssm_cov_50'))}  "
               f"{_fp(r.get('tcm_cov_10'))}  {_fp(r.get('tcm_cov_50'))}")
        if flags:
            row += f"  {flags}"
        print(row)

    print()
    print('─' * W_line)
    print('EXTREMAL START YEARS BY DIMENSION')
    print('─' * W_line)

    def _profile(label, r):
        if r is None:
            print(f"  {label:<46}  no data")
            return
        lfail = str(r['lrr_failure_year']) if r.get('lrr_failure_year') else 'no failure'
        cov50 = (f"{r['ssm_cov_50']:.1%}" if r.get('ssm_cov_50') is not None else '—')
        print(f"  {label:<46}  {r['calendar_year']}  "
              f"LRRfill={r.get('lrr_fill_year')}  "
              f"surplus={r.get('lrr_surplus_at_fill', 0.0):.0f}£b  "
              f"LRRfail={lfail}  SSMcov50={cov50}")

    print('\n  Dimension 1 — Speed:')
    _profile('  Worst (slowest LRR fill)', worst_speed)
    _profile('  Best  (fastest LRR fill)', best_speed)
    print('\n  Dimension 2 — Safety margin at fill:')
    _profile('  Worst (thinnest LRR surplus)', worst_margin)
    _profile('  Best  (largest  LRR surplus)', best_margin)
    print('\n  Dimension 3 — Durability (50yr SSM coverage):')
    _profile('  Worst (lowest 50yr SSM coverage)',  worst_durable)
    _profile('  Best  (highest 50yr SSM coverage)', best_durable)
    print('\n  Dimension 4 — Resilience (LRR failure year):')
    _profile('  Worst (earliest LRR failure)',     worst_resilient)
    _profile('  Best  (latest/no LRR failure)',    best_resilient)
    if nofailure_rows:
        print(f"  ({len(nofailure_rows)} start years produce no LRR failure "
              f"within the 71-year window)")

    return {
        'worst_speed':     worst_speed,
        'best_speed':      best_speed,
        'worst_margin':    worst_margin,
        'best_margin':     best_margin,
        'worst_durable':   worst_durable,
        'best_durable':    best_durable,
        'worst_resilient': worst_resilient,
        'best_resilient':  best_resilient,
        'all':             sweep_results,
    }
