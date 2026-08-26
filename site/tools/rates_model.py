"""
WDT Rates and Revenue — Model Module
======================================
Extracted from 7_3_260807_WDT_Rates_and_Revenue_Python_Model.py (v6).

This file contains only computational logic: parameter loading,
the SSM, the TCM, the start-year sweep, extremal profiles, and
the statistical pass. It has no file I/O, no matplotlib dependency,
and no Excel checker.

Output generation (Markdown report and charts) lives in rates_output.py,
which imports this module.

PUBLIC API
----------
  load_params(toml_path=None)         -> dict
  validate_params(p)                  -> None  (raises on error)
  run_ssm(p, max_N=71)               -> list[dict]
  run_tcm(p, N=None, N_fill=None)    -> dict[float, list[dict]]
  run_start_year_sweep(p)            -> list[dict]
  run_scenario_profiles(extremals, p) -> list[dict]
  compute_statistics(sweep_results)  -> dict

  report_start_year_sweep(sweep, p)  -> dict   (also prints to stdout)
  report_scenario_profiles(prof, p)  -> None   (prints to stdout)
  report_statistics(stats, p)        -> None   (prints to stdout)

ARCHITECTURE
------------
  Inputs:     TOML parameters file via wdt_core.load_params().
  SSM:        cohort marginal model, N=1..max_N.
  SRR target: srr_ratio × (cumulative net income / N).
  LRR:        accumulates SRR surplus until floor target met,
              then funds government expenditure.
  Rate fn:    tau_m / (1 + ((1-tau_0)/tau_0) * exp(-k*(W-W_min))),
              0 if W < W_min.
  Route C:    equity transfer, delta on declared wealth.
  Sweep:      returns series rotated per calendar start year; 73 years.
"""

import math
from pathlib import Path

from wdt_core import (load_params as _core_load_params,
                      tau, simulate, simulate_sell_year)

# Default path — used when no toml_path is supplied to load_params().
DEFAULT_PARAMS = Path(__file__).parent / '260812_WDT_Params.toml'


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
# SECTION 2 — CORE MECHANICS
# ─────────────────────────────────────────────────────────────

# tau(), simulate(), and simulate_sell_year() are imported from wdt_core
# and re-exported here so callers only need to import rates_model.


# ─────────────────────────────────────────────────────────────
# SECTION 3 — SSM
# ─────────────────────────────────────────────────────────────

def run_ssm(p, max_N=71):
    """
    SWF Solvency Model — cohort marginal approach, N=1..max_N.

    Applies the historical return series uniformly across the entire
    taxable population (correlated-shock assumption).  Tracks year-by-year
    SRR and LRR balances.

    Returns a list of dicts, one per year, containing:
      year, g, ttp, refunds, net, srr_target, srr_balance, srr_surplus,
      budget, lrr_net, lrr_target, lrr_balance, lrr_filled.
    The final dict also carries post-fill summary fields:
      post_fill_avg_net_b, post_fill_avg_budget_b, post_fill_years,
      ssm_post_fill_coverage.
    """
    returns  = p['returns']
    brackets = p['brackets']
    alpha    = 1.0

    srr_ratio     = p['srr_ratio']
    lrr_years     = p['lrr_years']
    budget_base   = p['budget_base']
    budget_growth = p['budget_growth']

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

    srr_bal    = 0.0
    lrr_bal    = 0.0
    lrr_filled = False
    cum_net    = 0.0
    results    = []

    post_fill_cum_net    = 0.0
    post_fill_cum_budget = 0.0
    post_fill_years      = 0

    for m in marginal:
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
            lrr_net  = srr_surplus
            if lrr_bal >= lrr_target:
                lrr_filled = True
        else:
            lrr_net  = srr_surplus - budget_t
            lrr_bal += lrr_net

        if srr_target > 0 and srr_bal >= srr_target * 0.9999 and not lrr_filled:
            post_fill_cum_net    += net
            post_fill_cum_budget += budget_t
            post_fill_years      += 1

        results.append({
            'year':        N,
            'g':           m['g'],
            'ttp':         m['ttp'],
            'refunds':     m['ref'],
            'net':         net,
            'srr_target':  srr_target,
            'srr_balance': srr_bal,
            'srr_surplus': srr_surplus,
            'budget':      budget_t,
            'lrr_net':     lrr_net,
            'lrr_target':  lrr_target,
            'lrr_balance': lrr_bal,
            'lrr_filled':  lrr_filled,
        })

    if results and post_fill_years > 0:
        avg_pf_net    = post_fill_cum_net    / post_fill_years
        avg_pf_budget = post_fill_cum_budget / post_fill_years
        ssm_pf_cov    = avg_pf_net / avg_pf_budget if avg_pf_budget > 0 else None
        results[-1]['post_fill_avg_net_b']    = avg_pf_net
        results[-1]['post_fill_avg_budget_b'] = avg_pf_budget
        results[-1]['post_fill_years']        = post_fill_years
        results[-1]['ssm_post_fill_coverage'] = ssm_pf_cov
    elif results:
        results[-1]['post_fill_avg_net_b']    = None
        results[-1]['post_fill_avg_budget_b'] = None
        results[-1]['post_fill_years']        = 0
        results[-1]['ssm_post_fill_coverage'] = None

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

    Used by run_start_year_sweep() to avoid the overhead of a full
    run_ssm() call when only solvency metrics are needed.

    Returns a dict of transition metrics for one start year.
    """
    alpha         = 1.0
    srr_ratio     = p['srr_ratio']
    lrr_years     = p['lrr_years']
    budget_base   = p['budget_base']
    budget_growth = p['budget_growth']
    brackets      = p['brackets']
    max_N         = 71

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

    srr_bal    = 0.0
    lrr_bal    = 0.0
    lrr_filled = False
    cum_net    = 0.0

    srr_fill_year           = None
    lrr_fill_year           = None
    lrr_surplus_at_fill     = 0.0
    srr_balance_at_lrr_fill = 0.0
    lrr_breach_year         = None
    srr_breach_year         = None
    srr_breach_magnitude    = 0.0
    lrr_bal_at_srr_breach   = None
    srr_bal_at_lrr_breach   = None
    max_lrr_breach          = 0.0

    post_fill_cum_net    = 0.0
    post_fill_cum_budget = 0.0
    post_fill_years      = 0

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

        if srr_fill_year is None and srr_target > 0 and srr_bal >= srr_target * 0.9999:
            srr_fill_year = N

        if srr_breach_year is None and srr_bal < 0:
            srr_breach_year      = N
            srr_breach_magnitude = abs(srr_bal)
            lrr_bal_at_srr_breach = lrr_bal

        budget_t   = budget_base * (1.0 + budget_growth) ** (N - 1)
        lrr_target = lrr_years * budget_t

        if not lrr_filled:
            lrr_bal += srr_surplus
            if lrr_bal >= lrr_target:
                lrr_filled              = True
                lrr_fill_year           = N
                lrr_surplus_at_fill     = lrr_bal - lrr_target
                srr_balance_at_lrr_fill = srr_bal
        else:
            lrr_bal += srr_surplus - budget_t

        if lrr_filled and lrr_breach_year is None and lrr_bal < 0:
            lrr_breach_year       = N
            srr_bal_at_lrr_breach = srr_bal

        if lrr_bal < max_lrr_breach:
            max_lrr_breach = lrr_bal

        if srr_target > 0 and srr_bal >= srr_target * 0.9999 and not lrr_filled:
            post_fill_cum_net    += net
            post_fill_cum_budget += budget_t
            post_fill_years      += 1

    years_fill_to_breach = (
        (lrr_breach_year - lrr_fill_year)
        if (lrr_fill_year is not None and lrr_breach_year is not None)
        else None
    )

    srr_breach_covered = (
        (lrr_bal_at_srr_breach is not None and
         lrr_bal_at_srr_breach >= srr_breach_magnitude)
        if srr_breach_year is not None else None
    )

    ssm_post_fill_coverage = (
        (post_fill_cum_net / post_fill_years) /
        (post_fill_cum_budget / post_fill_years)
        if post_fill_years > 0 else None
    )

    return {
        'srr_fill_year':           srr_fill_year,
        'lrr_fill_year':           lrr_fill_year,
        'lrr_surplus_at_fill':     lrr_surplus_at_fill,
        'srr_balance_at_lrr_fill': srr_balance_at_lrr_fill,
        'lrr_breach_year':         lrr_breach_year,
        'years_fill_to_breach':    years_fill_to_breach,
        'max_lrr_breach':          max_lrr_breach,
        'srr_breach_year':         srr_breach_year,
        'srr_breach_magnitude':    srr_breach_magnitude,
        'lrr_bal_at_srr_breach':   lrr_bal_at_srr_breach,
        'srr_bal_at_lrr_breach':   srr_bal_at_lrr_breach,
        'srr_breach_covered':      srr_breach_covered,
        'ssm_post_fill_coverage':  ssm_post_fill_coverage,
        'post_fill_years':         post_fill_years,
    }


def run_start_year_sweep(p):
    """
    Run the stripped SSM and a full TCM across all 73 calendar start years.

    Returns a list of dicts (one per start year) containing all solvency
    metrics from _ssm_stripped() plus tcm_post_fill_coverage.
    """
    base  = p['series_base_year']
    raw   = p.get('canonical_returns', p['returns'])
    years = list(range(base, base + len(raw)))
    results = []

    for cal_year in years:
        rotated = _rotate_returns(raw, cal_year, base)
        metrics = _ssm_stripped(rotated, p)
        metrics['calendar_year'] = cal_year

        lrr_N      = metrics.get('lrr_fill_year')
        srr_N      = metrics.get('srr_fill_year')
        tcm_pf_cov = None

        if lrr_N is not None and srr_N is not None:
            p_rot = dict(p)
            p_rot['returns'] = rotated
            tcm_result = run_tcm(p_rot, N=lrr_N, N_fill=srr_N)

            total_pf_rev = sum(
                sum(r['post_fill_revenue_m'] for r in tcm_result[t['differential']]) / 1000
                for t in p['tiers']
            )

            post_fill_years = lrr_N - srr_N
            if post_fill_years > 0:
                avg_pf_budget = sum(
                    p['budget_base'] * (1.0 + p['budget_growth']) ** (t - 1)
                    for t in range(srr_N, lrr_N)
                ) / post_fill_years
                if avg_pf_budget > 0:
                    tcm_pf_cov = total_pf_rev / avg_pf_budget

        metrics['tcm_post_fill_coverage'] = tcm_pf_cov
        results.append(metrics)

    return results


# ─────────────────────────────────────────────────────────────
# SECTION 3c — EXTREMAL SCENARIO PROFILES
# ─────────────────────────────────────────────────────────────

def run_scenario_profiles(sweep_extremals, p):
    """
    Run the full SSM at each of the six extremal start years identified
    by report_start_year_sweep().

    Returns a list of profile dicts, each containing:
      calendar_year, dimension_labels, ssm (full year-by-year list), metrics.
    """
    base = p['series_base_year']
    raw  = p.get('canonical_returns', p['returns'])

    label_map = {}
    for dim_label, key in [
        ('Worst speed',      'worst_speed'),
        ('Best speed',       'best_speed'),
        ('Worst margin',     'worst_margin'),
        ('Best margin',      'best_margin'),
        ('Worst durability', 'worst_durable'),
        ('Best durability',  'best_durable'),
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

        srr_fill   = next((r['year'] for r in ssm_result
                           if r['srr_target'] > 0
                           and r['srr_balance'] >= r['srr_target'] * 0.9999), None)
        lrr_fill_r = next((r for r in ssm_result if r.get('lrr_filled')), None)
        lrr_fill   = lrr_fill_r['year']                                 if lrr_fill_r else None
        lrr_surplus= (lrr_fill_r['lrr_balance'] - lrr_fill_r['lrr_target']) if lrr_fill_r else 0.0
        srr_at_lrr = lrr_fill_r['srr_balance']                          if lrr_fill_r else 0.0

        max_lrr_breach = min(min(r['lrr_balance'] for r in ssm_result), 0.0)

        srr_breach_row        = next((r for r in ssm_result if r['srr_balance'] < 0), None)
        srr_breach            = srr_breach_row['year']             if srr_breach_row else None
        srr_breach_magnitude  = abs(srr_breach_row['srr_balance']) if srr_breach_row else 0.0
        lrr_bal_at_srr_breach = srr_breach_row['lrr_balance']      if srr_breach_row else None

        lrr_breach_row        = next((r for r in ssm_result
                                      if r.get('lrr_filled') and r['lrr_balance'] < 0), None)
        lrr_breach            = lrr_breach_row['year']             if lrr_breach_row else None
        srr_bal_at_lrr_breach = lrr_breach_row['srr_balance']      if lrr_breach_row else None
        gap = (lrr_breach - lrr_fill) if (lrr_fill and lrr_breach) else None

        srr_covered = (
            (lrr_bal_at_srr_breach is not None and
             lrr_bal_at_srr_breach >= srr_breach_magnitude)
            if srr_breach is not None else None
        )

        profiles.append({
            'calendar_year':    cy,
            'dimension_labels': labels,
            'ssm':              ssm_result,
            'metrics': {
                'srr_fill_year':           srr_fill,
                'lrr_fill_year':           lrr_fill,
                'lrr_surplus_at_fill':     lrr_surplus,
                'srr_balance_at_lrr_fill': srr_at_lrr,
                'lrr_breach_year':         lrr_breach,
                'years_fill_to_breach':    gap,
                'max_lrr_breach':          max_lrr_breach,
                'srr_breach_year':         srr_breach,
                'srr_breach_magnitude':    srr_breach_magnitude,
                'lrr_bal_at_srr_breach':   lrr_bal_at_srr_breach,
                'srr_bal_at_lrr_breach':   srr_bal_at_lrr_breach,
                'srr_breach_covered':      srr_covered,
            },
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
          f"{'LRRsurp£b':>10}  {'LRRbrch':>7}  {'gap':>5}  "
          f"{'maxLRRbrch£b':>13}  {'SRRbrch':>7}  {'SRRmag£b':>10}  "
          f"{'LRR@SRRbrch£b':>14}  {'covered':>7}")
    print('-' * W)

    for prof in profiles:
        m   = prof['metrics']
        cy  = prof['calendar_year']
        dim = ', '.join(prof['dimension_labels'])
        cov = ('YES' if m['srr_breach_covered'] is True
               else ('NO' if m['srr_breach_covered'] is False else '—'))

        def _c(v, w=7): return f"{v:>{w}}" if v is not None else f"{'—':>{w}}"
        lrr_s  = f"{m['lrr_surplus_at_fill']:>10.0f}" if m['lrr_fill_year'] else f"{'—':>10}"
        lrr_ab = (f"{m['lrr_bal_at_srr_breach']:>14.0f}"
                  if m['lrr_bal_at_srr_breach'] is not None else f"{'—':>14}")

        print(f"{cy:>5}  {dim:<30}  {_c(m['srr_fill_year'])}  {_c(m['lrr_fill_year'])}  "
              f"{lrr_s}  {_c(m['lrr_breach_year'])}  {_c(m['years_fill_to_breach'], 5)}  "
              f"{m['max_lrr_breach']:>13.0f}  {_c(m['srr_breach_year'])}  "
              f"{m['srr_breach_magnitude']:>10.0f}  {lrr_ab}  {cov:>7}")

    print()
    print('  covered: LRR balance in SRR breach year >= SRR breach magnitude')
    print('  max LRR breach: peak government borrowing needed under zero-governance assumption')


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
    if r['lrr_fill_year'] is None:
        return False
    return r['srr_breach_year'] is None or r['srr_breach_covered'] is True


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

    Returns a dict with keys: overall, by_bucket, distributions,
    covered_breakdown.
    """
    n_total      = len(sweep_results)
    n_success    = sum(1 for r in sweep_results if _success(r))
    n_lrr_fills  = sum(1 for r in sweep_results if r['lrr_fill_year'] is not None)
    n_srr_breach = sum(1 for r in sweep_results if r['srr_breach_year'] is not None)
    n_covered    = sum(1 for r in sweep_results
                       if r['srr_breach_year'] is not None
                       and r['srr_breach_covered'] is True)
    n_uncovered  = sum(1 for r in sweep_results
                       if r['srr_breach_year'] is not None
                       and r['srr_breach_covered'] is False)

    overall = {
        'n_total':        n_total,
        'n_success':      n_success,
        'success_rate':   _pct(n_success, n_total),
        'n_lrr_fills':    n_lrr_fills,
        'lrr_fill_rate':  _pct(n_lrr_fills, n_total),
        'n_srr_breach':   n_srr_breach,
        'srr_breach_rate':_pct(n_srr_breach, n_total),
        'n_srr_covered':  n_covered,
        'n_srr_uncovered':n_uncovered,
    }

    by_bucket = []
    for label, yr_from, yr_to in CYCLE_BUCKETS:
        bucket = [r for r in sweep_results
                  if yr_from <= r['calendar_year'] <= yr_to]
        if not bucket:
            continue
        nb = len(bucket)
        ns = sum(1 for r in bucket if _success(r))
        nf = sum(1 for r in bucket if r['lrr_fill_year'] is not None)
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
        'lrr_fill_year':          _dist('lrr_fill_year'),
        'srr_fill_year':          _dist('srr_fill_year'),
        'lrr_surplus_at_fill':    _dist('lrr_surplus_at_fill'),
        'years_fill_to_breach':   _dist('years_fill_to_breach'),
        'max_lrr_breach':         _dist('max_lrr_breach'),
        'srr_breach_magnitude':   _dist('srr_breach_magnitude'),
        'ssm_post_fill_coverage': _dist('ssm_post_fill_coverage'),
        'tcm_post_fill_coverage': _dist('tcm_post_fill_coverage'),
    }

    covered_breakdown = {
        'no_srr_breach': n_total - n_srr_breach,
        'srr_covered':   n_covered,
        'srr_uncovered': n_uncovered,
    }

    return {
        'overall':           overall,
        'by_bucket':         by_bucket,
        'distributions':     distributions,
        'covered_breakdown': covered_breakdown,
    }


def report_statistics(stats, p):
    """Print the statistical pass summary to stdout."""
    W = 90
    print()
    print('=' * W)
    print('STATISTICAL PASS — success rates across all economic cycles')
    print(f"  Parameters: $\tau_0$={p['tau_0']:.0%}  $\tau_m$={p['tau_m']:.0%}  "
          f"k={p['k']}  W_min=£{p['W_min']}m  "
          f"SRR={p['srr_ratio']}×  LRR={p['lrr_years']}yrs")
    print('  Success = LRR fills within window AND '
          '(SRR never breaches OR breach covered by LRR)')
    print('=' * W)

    ov = stats['overall']
    print()
    print('OVERALL (all 73 start years):')
    print(f"  Success rate:          {ov['success_rate']:>6.1f}%  "
          f"({ov['n_success']}/{ov['n_total']} start years)")
    print(f"  LRR fills:             {ov['lrr_fill_rate']:>6.1f}%  "
          f"({ov['n_lrr_fills']}/{ov['n_total']})")
    print(f"  SRR breaches:          {ov['srr_breach_rate']:>6.1f}%  "
          f"({ov['n_srr_breach']}/{ov['n_total']})")

    cb = stats['covered_breakdown']
    print(f"  Of which covered:      {ov['n_srr_covered']}  "
          f"uncovered: {ov['n_srr_uncovered']}  "
          f"no breach: {cb['no_srr_breach']}")

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
        ('lrr_fill_year',          'LRR breakeven year',            '{:.0f}'),
        ('srr_fill_year',          'SRR fill year',                 '{:.0f}'),
        ('lrr_surplus_at_fill',    'LRR surplus at breakeven (£b)', '{:.0f}'),
        ('years_fill_to_breach',   'LRR breach lag (yrs)',          '{:.0f}'),
        ('max_lrr_breach',         'Peak LRR deficit (£b)',         '{:.0f}'),
        ('srr_breach_magnitude',   'SRR deficit at breach (£b)',    '{:.0f}'),
        ('ssm_post_fill_coverage', 'SSM coverage ratio',            '{:.1%}'),
        ('tcm_post_fill_coverage', 'TCM coverage ratio',            '{:.1%}'),
    ]
    print(f"  {'Metric':<32}  {'N':>3}  {'Min':>10}  "
          f"{'Median':>10}  {'Mean':>10}  {'Max':>10}")
    print('  ' + '-' * 82)
    for key, label, fmt in dist_rows:
        d = stats['distributions'][key]
        def _f(v, f=fmt): return f.format(v) if v is not None else '—'
        print(f"  {label:<32}  {d['n']:>3}  "
              f"{_f(d['min']):>10}  {_f(d['median']):>10}  "
              f"{_f(d['mean']):>10}  {_f(d['max']):>10}")


# ─────────────────────────────────────────────────────────────
# SECTION 4 — TCM
# ─────────────────────────────────────────────────────────────

def run_tcm(p, N=None, N_fill=None):
    """
    Taxpayer Cohort Model at horizon N.

    For each tier × bracket cell, simulates cumulative tax and refund
    flows over N regular periods plus a terminal sell year, using the
    actual historical return series rotated to the active scenario's
    start year, plus each tier's persistent differential.

    Returns a dict keyed by tier differential (float) mapping to a list
    of bracket dicts.  Each bracket dict contains:

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
    # Capitalisation window: sim years N_fill..N-1, matching the budget denominator
    # range(srr_N, lrr_N) used in run_start_year_sweep() and run_ssm().
    # The sell year (year N+1) is a terminal liquidation event, not an annual flow,
    # and is excluded from the coverage-ratio average on both sides.
    post_fill_periods = N - N_fill  # 0 if srr fills same year as lrr — guarded below

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
            # sim[N_fill:N] = periods N_fill..N-1 (lrr_N - 1), matching range(srr_N, lrr_N).
            # Sell year excluded: it's a one-off terminal event outside the cap window.
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


def report_start_year_sweep(sweep_results, p):
    """
    Print the full 73-row sweep table to stdout and return the six
    extremal records plus the full results list.

    Return value is a dict with keys:
      worst_speed, best_speed, worst_margin, best_margin,
      worst_durable, best_durable, nobreach_count, all.
    """
    W = 132
    print()
    print('=' * W)
    print('START-YEAR SENSITIVITY SWEEP  (all calendar years, Balanced parameters)')
    print('=' * W)

    filled        = [r for r in sweep_results if r['lrr_fill_year'] is not None]
    worst_speed   = max(filled, key=lambda r: r['lrr_fill_year'])           if filled else None
    best_speed    = min(filled, key=lambda r: r['lrr_fill_year'])           if filled else None
    worst_margin  = min(filled, key=lambda r: r['lrr_surplus_at_fill'])     if filled else None
    best_margin   = max(filled, key=lambda r: r['lrr_surplus_at_fill'])     if filled else None
    breach_rows   = [r for r in filled if r['years_fill_to_breach'] is not None]
    nobreach_rows = [r for r in filled if r['years_fill_to_breach'] is None]
    worst_durable = min(breach_rows, key=lambda r: r['years_fill_to_breach']) if breach_rows else None
    if nobreach_rows:
        best_durable = min(nobreach_rows, key=lambda r: r['lrr_fill_year'])
    elif breach_rows:
        best_durable = max(breach_rows, key=lambda r: r['years_fill_to_breach'])
    else:
        best_durable = None

    def _flags(r):
        fs = []
        if worst_speed   and r['calendar_year'] == worst_speed['calendar_year']:   fs.append('↓SPD')
        if best_speed    and r['calendar_year'] == best_speed['calendar_year']:    fs.append('↑SPD')
        if worst_margin  and r['calendar_year'] == worst_margin['calendar_year']:  fs.append('↓MRG')
        if best_margin   and r['calendar_year'] == best_margin['calendar_year']:   fs.append('↑MRG')
        if worst_durable and r['calendar_year'] == worst_durable['calendar_year']: fs.append('↓DUR')
        if best_durable  and r['calendar_year'] == best_durable['calendar_year']:  fs.append('↑DUR')
        return ' '.join(fs)

    print(f"{'Start':>5}  {'SRRfill':>7}  {'LRRbrkevn':>9}  {'LRRsurp£b':>10}  "
          f"{'SRR@brkevn£b':>13}  {'LRRbrch':>7}  {'brch lag':>8}  "
          f"{'peakLRRdef£b':>13}  {'SRRbrch':>7}  {'SRRdef£b':>9}  "
          f"{'LRR@SRRbrch£b':>14}  {'covered':>7}  {'SSMcov%':>7}  "
          f"{'TCMcov%':>7}  Flags")
    print('-' * (W + 62))

    for r in sweep_results:
        def _f(v, w=7): return f"{v:>{w}}" if v is not None else f"{'—':>{w}}"
        flags     = _flags(r)
        lrr_surp  = (f"{r['lrr_surplus_at_fill']:>10.0f}"
                     if r['lrr_fill_year'] is not None else f"{'—':>10}")
        srr_atl   = (f"{r['srr_balance_at_lrr_fill']:>14.0f}"
                     if r['lrr_fill_year'] is not None else f"{'—':>14}")
        max_lrr_b = f"{r['max_lrr_breach']:>13.0f}"
        srr_mag   = f"{r['srr_breach_magnitude']:>13.0f}"
        lrr_abrch = (f"{r['lrr_bal_at_srr_breach']:>14.0f}"
                     if r['lrr_bal_at_srr_breach'] is not None else f"{'—':>14}")
        cov = ('YES' if r['srr_breach_covered'] is True
               else ('NO' if r['srr_breach_covered'] is False else '—'))
        ssm_str = (f"{r['ssm_post_fill_coverage']:>6.1%}"
                   if r.get('ssm_post_fill_coverage') is not None else f"{'—':>7}")
        tcm_str = (f"{r['tcm_post_fill_coverage']:>6.1%}"
                   if r.get('tcm_post_fill_coverage') is not None else f"{'—':>7}")
        row = (f"{r['calendar_year']:>5}  {_f(r['srr_fill_year'])}  "
               f"{_f(r['lrr_fill_year'])}  {lrr_surp}  {srr_atl}  "
               f"{_f(r['lrr_breach_year'])}  {_f(r['years_fill_to_breach'], 9)}  "
               f"{max_lrr_b}  {_f(r['srr_breach_year'])}  "
               f"{srr_mag}  {lrr_abrch}  {cov:>7}  {ssm_str}  {tcm_str}")
        if flags:
            row += f"  {flags}"
        print(row)

    print()
    print('─' * W)
    print('EXTREMAL START YEARS BY DIMENSION')
    print('─' * W)

    def _profile(label, r):
        if r is None:
            print(f"  {label:<42}  no data")
            return
        lag = (str(r['years_fill_to_breach'])
               if r['years_fill_to_breach'] is not None else 'no breach')
        print(f"  {label:<42}  {r['calendar_year']}  "
              f"SRR={r['srr_fill_year']}  LRR breakeven={r['lrr_fill_year']}  "
              f"surplus={r['lrr_surplus_at_fill']:.0f}£b  "
              f"breach lag={lag}  peak LRR deficit={r['max_lrr_breach']:.0f}£b")

    print('\n  Dimension 1 — Speed:')
    _profile('  Worst (slowest LRR breakeven)', worst_speed)
    _profile('  Best  (fastest LRR breakeven)', best_speed)
    print('\n  Dimension 2 — Safety margin at breakeven:')
    _profile('  Worst (thinnest LRR surplus)', worst_margin)
    _profile('  Best  (largest  LRR surplus)', best_margin)
    print('\n  Dimension 3 — Durability after breakeven:')
    _profile('  Worst (shortest LRR breach lag)', worst_durable)
    _profile('  Best  (longest  LRR breach lag)', best_durable)
    if nobreach_rows:
        print(f"  ({len(nobreach_rows)} start years produce no LRR breach "
              f"within the 71-year window)")

    return {
        'worst_speed':    worst_speed,
        'best_speed':     best_speed,
        'worst_margin':   worst_margin,
        'best_margin':    best_margin,
        'worst_durable':  worst_durable,
        'best_durable':   best_durable,
        'nobreach_count': len(nobreach_rows),
        'all':            sweep_results,
    }
