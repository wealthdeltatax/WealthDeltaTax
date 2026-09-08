"""
wdt_welfare_tables.py
=====================
Tabular output for the WFR Welfare Comparison Model.

Produces appendix-ready markdown tables from all four module results,
using the project's canonical helpers (wdt_md, wdt_fmt, wdt_style).

Each table is self-contained: it can be copied directly into the paper's
appendix without reformatting. Tables are also written individually so
each module can include only its own tables.

Table inventory
---------------
Table WFR.1  — Module 1: CEW comparison across systems and γ values
               (both distributions)
Table WFR.2  — Module 1: Variance of consumption by system
               (both distributions, γ=2)
Table WFR.3  — Module 1: Revenue-equivalent rates by system and distribution
Table WFR.4  — Module 1: Domar-Musgrave test results
Table WFR.5  — Module 2: C1 — Flat vs progressive WDT CEW
               (both distributions, all γ)
Table WFR.6b — Module 2: C2 — Leverage effect on WDT tax base and welfare
               (15-point leverage grid, gross assets £10m, γ=2, Ver. A)
Table WFR.6  — Module 2: C3 — Two-period rate asymmetry by wealth level
Table WFR.7  — Module 3: Lock-in welfare cost — sensitivity to gain ratio
Table WFR.8  — Module 3: Lock-in welfare cost — sensitivity to holding period
Table WFR.9  — Module 3: Full welfare comparison WDT vs CGT (with/without lock-in)
Table WFR.10 — Module 4: Tier-by-tier CEW under all systems
Table WFR.11 — Module 4: Distributional incidence (expected tax as % of W₀)
Table WFR.12 — Module 4: Concentration path — Great/Poor wealth ratio at
               key years (years 0, 10, 25, 50, 73)
Table WFR.13 — Module 4: Envelope binding summary by tier

All tables written to: model/OUTPUTS/WFR/tables/
Master document (all tables): WFR_appendix_tables.md
"""

import sys
import math
import numpy as np
from pathlib import Path

# ── project helpers ───────────────────────────────────────────────────────────
from wdt_welfare_paths import TOML_PATH, module_output_dir
from wdt_md  import MdDoc, md_table, LEFT, RIGHT, CENTER
from wdt_fmt import fmt_pct, fmt_pct1, fmt_gbp_m, fmt_f2, fmt_f4, today_iso

# ── welfare model imports ─────────────────────────────────────────────────────
from wdt_welfare_core import (
    load_params,
    make_empirical_distribution,
    make_idealised_distribution,
    run_welfare_comparison,
    solve_revenue_equivalent_rate,
    get_tax_fn,
    dm_test,
    variance_of_consumption,
    expected_tax,
    tax_symmetric_flat,
    SYSTEM_LABELS,
)
from module2_progression import (
    ProgressiveRateFunction,
    LeveragedAgent,
    run_c1_analysis,
    run_c2_leverage,
    run_c3_two_period,
)
from module3_lockin import (
    AssetSwitchDecision,
    compute_lock_in_welfare_cost,
    sensitivity_gain_ratio,
    sensitivity_holding_period,
    full_comparison_with_lockin,
)
from module4_heterogeneous import (
    AgentTier,
    build_tiers,
    run_tier_comparison,
    run_concentration_analysis,
    test_envelope_binding,
)

# ─────────────────────────────────────────────────────────────────────────────
# PATCH: add fmt_pct4 if not present in wdt_fmt
# ─────────────────────────────────────────────────────────────────────────────
try:
    from wdt_fmt import fmt_pct4
except ImportError:
    def fmt_pct4(v) -> str:
        if v is None: return '—'
        return f'{v * 100:.4f}%'

# ─────────────────────────────────────────────────────────────────────────────
# CONFIG
# ─────────────────────────────────────────────────────────────────────────────

OUTPUT_DIR  = module_output_dir("tables")
W0_BASE     = 1.0      # normalised (Module 1)
TARGET_ET   = 0.02
GAMMA_VALS  = [1.0, 2.0, 4.0]
SYSTEMS_ORD = ["symmetric_wdt", "stock_wealth", "income", "cgt", "consumption"]

# Short labels for table columns (space-constrained)
SYS_SHORT = {
    "symmetric_wdt" : "Symmetric WDT",
    "stock_wealth"  : "Stock Wealth Tax",
    "income"        : "Income Tax",
    "cgt"           : "CGT",
    "consumption"   : "Consumption Tax",
}

DIST_SHORT = {
    "A": "Version A (Empirical)",
    "B": "Version B (Idealised)",
}

# ─────────────────────────────────────────────────────────────────────────────
# HELPERS
# ─────────────────────────────────────────────────────────────────────────────

def _cew(r):
    """CEW formatted to 4dp%, or em-dash."""
    return fmt_pct4(r.cew) if r and r.cew is not None else '—'

def _tau(r):
    """Rate formatted to 3dp%, or em-dash."""
    if r and r.tau is not None:
        return f'{r.tau*100:.3f}%'
    return '—'

def _var(r):
    """Variance formatted to 4dp, or em-dash."""
    if r and r.var_consumption is not None:
        return f'{r.var_consumption:.4f}'
    return '—'

def _et(r):
    """Expected tax formatted to 4dp, or em-dash."""
    if r and r.expected_tax is not None:
        return f'{r.expected_tax:.4f}'
    return '—'

def _prog_cew(v):
    if v is None: return '—'
    return f'{v*100:.4f}%'

def _bp(v):
    if v is None: return '—'
    return f'{v:+.2f} bp'

def _ratio(v):
    if v is None or math.isnan(v): return '—'
    return f'{v:,.1f}×'


# ─────────────────────────────────────────────────────────────────────────────
# TABLE WFR.1  CEW by system, γ, distribution
# ─────────────────────────────────────────────────────────────────────────────

def table_wfr1(all_results: dict) -> str:
    """
    WFR.1: CEW (%) for all systems across γ = 1, 2, 4 and both distributions.
    One row per system. One group of columns per (distribution, γ) combination.
    """
    # Build column headers: one per (dist_key, gamma)
    dist_keys  = list(all_results.keys())
    col_groups = [(dk, g) for dk in dist_keys for g in GAMMA_VALS]

    headers = ['System'] + [
        f"{DIST_SHORT.get(dk[:9], dk[:9])} γ={g:.0f}"
        for dk, g in col_groups
    ]
    # Shorten dist labels
    dist_label_map = {}
    for dk in dist_keys:
        if 'Historical' in dk:
            dist_label_map[dk] = 'Ver. A'
        else:
            dist_label_map[dk] = 'Ver. B'

    headers = ['System'] + [
        f"{dist_label_map[dk]} γ={g:.0f}"
        for dk, g in col_groups
    ]
    col_fmt = [LEFT] + [RIGHT] * len(col_groups)

    rows = []
    for name in SYSTEMS_ORD:
        row = [SYS_SHORT[name]]
        for dk, g in col_groups:
            r = all_results[dk][g].get(name)
            row.append(_cew(r))
        rows.append(row)

    return md_table(headers, rows, col_fmt=col_fmt)


# ─────────────────────────────────────────────────────────────────────────────
# TABLE WFR.2  Variance of consumption by system (γ=2, both distributions)
# ─────────────────────────────────────────────────────────────────────────────

def table_wfr2(all_results: dict) -> str:
    """WFR.2: Var(consumption) at γ=2 for both distributions."""
    dist_keys = list(all_results.keys())
    headers   = ['System'] + [dist_label_map_fn(dk) for dk in dist_keys] + ['No-Tax (Ver. A)', 'No-Tax (Ver. B)']
    col_fmt   = [LEFT] + [RIGHT] * (len(dist_keys) + 2)

    # No-tax variance for each distribution
    notax_vars = {}
    for dk in dist_keys:
        # Get from first system result (symmetric WDT at tau=0)
        r0 = all_results[dk][2.0].get("symmetric_wdt")
        # Compute directly
        notax_vars[dk] = '—'  # placeholder; filled below

    rows = []
    for name in SYSTEMS_ORD:
        row = [SYS_SHORT[name]]
        for dk in dist_keys:
            r = all_results[dk][2.0].get(name)
            row.append(_var(r))
        rows.append(row)

    # Simpler version: just two dist columns
    headers = ['System', 'Ver. A Var(C)', 'Ver. B Var(C)']
    col_fmt = [LEFT, RIGHT, RIGHT]
    rows = []
    for name in SYSTEMS_ORD:
        row = [SYS_SHORT[name]]
        for dk in dist_keys:
            r = all_results[dk][2.0].get(name)
            row.append(_var(r))
        rows.append(row)

    return md_table(headers, rows, col_fmt=col_fmt)


def dist_label_map_fn(dk):
    if 'Historical' in dk: return 'Ver. A'
    return 'Ver. B'


# ─────────────────────────────────────────────────────────────────────────────
# TABLE WFR.3  Revenue-equivalent rates
# ─────────────────────────────────────────────────────────────────────────────

def table_wfr3(all_results: dict) -> str:
    """WFR.3: Revenue-equivalent tax rate τ* for each system and distribution (γ=2)."""
    dist_keys = list(all_results.keys())
    headers   = ['System', 'Ver. A rate (τ*)', 'Ver. B rate (τ*)']
    col_fmt   = [LEFT, RIGHT, RIGHT]
    rows = []
    for name in SYSTEMS_ORD:
        row = [SYS_SHORT[name]]
        for dk in dist_keys:
            r = all_results[dk][2.0].get(name)
            row.append(_tau(r))
        rows.append(row)
    return md_table(headers, rows, col_fmt=col_fmt)


# ─────────────────────────────────────────────────────────────────────────────
# TABLE WFR.4  Domar-Musgrave test
# ─────────────────────────────────────────────────────────────────────────────

def table_wfr4(all_results: dict, dists: dict) -> str:
    """WFR.4: D-M test results for symmetric WDT at all (dist, γ) combinations."""
    headers = ['Distribution', 'γ', 'τ (WDT)', '(1−τ)²', 'Actual ratio', 'Gap', 'Holds?']
    col_fmt = [LEFT, RIGHT, RIGHT, RIGHT, RIGHT, RIGHT, CENTER]
    rows = []
    for dk, gamma_results in all_results.items():
        for g, sys_results in gamma_results.items():
            wdt_r = sys_results.get("symmetric_wdt")
            if wdt_r is None or wdt_r.tau is None:
                continue
            dm = dm_test(W0_BASE, dists[dk], wdt_r.tau)
            rows.append([
                dist_label_map_fn(dk),
                f'{g:.1f}',
                f'{wdt_r.tau*100:.4f}%',
                f'{dm["predicted_ratio"]:.6f}',
                f'{dm["actual_ratio"]:.6f}',
                f'{dm["gap"]:.2e}',
                '✓' if dm["dm_holds"] else '✗',
            ])
    return md_table(headers, rows, col_fmt=col_fmt)


# ─────────────────────────────────────────────────────────────────────────────
# TABLE WFR.5  Module 2 C1: Flat vs progressive WDT
# ─────────────────────────────────────────────────────────────────────────────

def table_wfr5(c1_results: dict) -> str:
    """
    WFR.5: C1 flat vs progressive CEW — revenue-equivalent comparison.

    The flat WDT rate is solved to match the progressive system's natural E[T],
    not the 2%-of-W₀ global target.  This makes the welfare comparison clean:
    same revenue, different structure, pure distortion difference.

    Columns
    -------
    Flat WDT CEW      : CEW at the revenue-matched flat rate
    Progressive CEW   : CEW at the canonical logistic schedule
    Gap (bp)          : (CEW_flat − CEW_prog) × 10,000; positive = flat WDT lower cost
    E[T] matched (£m) : expected revenue collected by both systems (equal by construction)
    vs 2% target (£m) : E[T]_progressive − E[T]_2%target; shows deviation from benchmark
    """
    headers = [
        'Distribution', 'γ',
        'Flat WDT CEW', 'Progressive CEW', 'Gap (bp)',
        'E[T] matched (£m)', 'vs 2% target (£m)',
    ]
    col_fmt = [LEFT, RIGHT, RIGHT, RIGHT, RIGHT, RIGHT, RIGHT]
    rows = []
    for dk, gamma_results in c1_results.items():
        for g, r in gamma_results.items():
            et_dev  = r['et_progressive'] - r['et_flat_target']
            flag    = '' if r.get('revenue_matched', True) else ' [!]'
            rows.append([
                dist_label_map_fn(dk),
                f'{g:.1f}',
                fmt_pct4(r['cew_flat']),
                fmt_pct4(r['cew_progressive']),
                f'{r["cew_gap_bp"]:+.2f}',
                fmt_gbp_m(r['et_progressive'], dp=4) + flag,
                f'{et_dev:+.4f}',
            ])
    return md_table(headers, rows, col_fmt=col_fmt)


# ─────────────────────────────────────────────────────────────────────────────
# TABLE WFR.6b  Module 2 C2: Leverage effect on WDT tax base and welfare
# ─────────────────────────────────────────────────────────────────────────────

def table_wfr6b(c2_lev_results: list) -> str:
    """
    WFR.6b: C2 leverage — net-worth delta base vs hypothetical asset-return base.

    Each row is one point on the 15-point leverage grid (0% → 70% of gross assets).
    Gross assets fixed at £10m; net worth W₀ = A × (1 − leverage ratio).

    Columns
    -------
    Lev. ratio  : D / A — debt as fraction of gross assets
    W₀ (£m)     : net worth after subtracting debt
    E[T] NW base: expected tax under actual WDT (net-worth delta base)
    E[T] AR base: expected tax under hypothetical asset-return base
    E[T] excess : E[T]_nw − E[T]_ar (positive = NW base collects more)
    CEW NW base : consumption-equivalent welfare under NW base
    CEW AR base : CEW under asset-return base
    CEW gap (bp): (CEW_nw − CEW_ar) × 10,000 — welfare difference
    """
    headers = [
        'Lev. ratio', 'W₀ (£m)',
        'E[T] NW base', 'E[T] AR base', 'E[T] excess',
        'CEW NW base', 'CEW AR base', 'CEW gap (bp)',
    ]
    col_fmt = [RIGHT, RIGHT, RIGHT, RIGHT, RIGHT, RIGHT, RIGHT, RIGHT]
    rows = []
    for r in c2_lev_results:
        rows.append([
            f'{r["leverage_ratio"]*100:.1f}%',
            fmt_gbp_m(r['W0'], dp=3),
            fmt_gbp_m(r['et_nw'], dp=4),
            fmt_gbp_m(r['et_ar'], dp=4),
            fmt_gbp_m(r['et_nw'] - r['et_ar'], dp=4),
            fmt_pct4(r['cew_nw']),
            fmt_pct4(r['cew_ar']),
            f'{r["cew_gap_bp"]:+.2f}',
        ])
    return md_table(headers, rows, col_fmt=col_fmt)


# ─────────────────────────────────────────────────────────────────────────────
# TABLE WFR.6  Module 2 C3: Rate asymmetry by wealth level
# ─────────────────────────────────────────────────────────────────────────────

def table_wfr6(c3_results: list, W0_vals: list) -> str:
    """WFR.6: Two-period rate asymmetry — gain-then-loss path by initial wealth."""
    headers = ['W₀ (£m)', 'τ gain (%)', 'τ refund (%)', 'Asymmetry (pp)',
               'Net tax: progressive', 'Net tax: flat', 'Excess']
    col_fmt = [RIGHT] * 7
    col_fmt[0] = RIGHT
    rows = []
    for W0, r in zip(W0_vals, c3_results):
        rows.append([
            f'{W0:.1f}',
            f'{r["tau1_progressive"]*100:.3f}',
            f'{r["tau2_progressive"]*100:.3f}',
            f'{r["rate_asymmetry"]*100:+.4f}',
            fmt_gbp_m(r['net_tax_prog'], dp=4),
            fmt_gbp_m(r['net_tax_flat'], dp=4),
            f'{r["net_tax_excess"]:+.4f}',
        ])
    return md_table(headers, rows, col_fmt=col_fmt)


# ─────────────────────────────────────────────────────────────────────────────
# TABLE WFR.7  Module 3: Lock-in cost vs gain ratio
# ─────────────────────────────────────────────────────────────────────────────

def table_wfr7(sens_gain: list) -> str:
    """WFR.7: Lock-in welfare cost by embedded gain ratio G/V."""
    headers = ['G/V (%)', 'CEW (free)', 'CEW (locked)', 'Lock-in cost (bp)', 'P(locked in)']
    col_fmt = [RIGHT, RIGHT, RIGHT, RIGHT, RIGHT]
    rows = []
    for r in sens_gain:
        rows.append([
            f'{r["gain_ratio"]*100:.1f}',
            fmt_pct4(r['cew_free']),
            fmt_pct4(r['cew_locked']),
            f'{r["lock_in_cost_bp"]:+.2f}',
            fmt_pct1(r['p_locked']),
        ])
    return md_table(headers, rows, col_fmt=col_fmt)


# ─────────────────────────────────────────────────────────────────────────────
# TABLE WFR.8  Module 3: Lock-in cost vs holding period
# ─────────────────────────────────────────────────────────────────────────────

def table_wfr8(sens_T: list) -> str:
    """WFR.8: Lock-in welfare cost by remaining holding period T."""
    headers = ['T (years)', 'Indifference return r_B*', 'Lock-in cost (bp)', 'P(locked in)']
    col_fmt = [RIGHT, RIGHT, RIGHT, RIGHT]
    rows = []
    for r in sens_T:
        rows.append([
            str(r['T']),
            f'{r["r_B_indiff"]*100:.4f}%',
            f'{r["lock_in_cost_bp"]:+.2f}',
            fmt_pct1(r['p_locked']),
        ])
    return md_table(headers, rows, col_fmt=col_fmt)


# ─────────────────────────────────────────────────────────────────────────────
# TABLE WFR.9  Module 3: Full WDT vs CGT comparison
# ─────────────────────────────────────────────────────────────────────────────

def table_wfr9(comp_A: dict, comp_B: dict) -> str:
    """WFR.9: Full WDT vs CGT welfare comparison including lock-in."""
    headers = ['Metric', 'Version A (Empirical)', 'Version B (Idealised)']
    col_fmt = [LEFT, RIGHT, RIGHT]
    rows = [
        ['WDT CEW',                         fmt_pct4(comp_A['wdt_cew']),             fmt_pct4(comp_B['wdt_cew'])],
        ['CGT CEW (no lock-in)',             fmt_pct4(comp_A['cgt_cew']),             fmt_pct4(comp_B['cgt_cew'])],
        ['Lock-in welfare cost',             _bp(comp_A['lock_in_cost_bp']),          _bp(comp_B['lock_in_cost_bp'])],
        ['CGT CEW (with lock-in)',           fmt_pct4(comp_A['cgt_with_lock_cew']),   fmt_pct4(comp_B['cgt_with_lock_cew'])],
        ['WDT advantage (no lock-in)',       _bp(comp_A['wdt_adv_no_lock_bp']),       _bp(comp_B['wdt_adv_no_lock_bp'])],
        ['WDT advantage (with lock-in)',     _bp(comp_A['wdt_adv_with_lock_bp']),     _bp(comp_B['wdt_adv_with_lock_bp'])],
        ['P(agent locked in)',               fmt_pct1(comp_A['p_locked']),            fmt_pct1(comp_B['p_locked'])],
        ['CGT indifference return r_B*',     f'{comp_A["r_B_indiff"]*100:.4f}%',      f'{comp_B["r_B_indiff"]*100:.4f}%'],
        ['Revenue-equivalent CGT rate',      f'{comp_A["m1_cgt_tau"]*100:.4f}%',      f'{comp_B["m1_cgt_tau"]*100:.4f}%'],
    ]
    return md_table(headers, rows, col_fmt=col_fmt)


# ─────────────────────────────────────────────────────────────────────────────
# TABLE WFR.10  Module 4: Tier-by-tier CEW
# ─────────────────────────────────────────────────────────────────────────────

def table_wfr10(tier_results: dict) -> str:
    """WFR.10: CEW by tier and system (γ=2)."""
    tiers_ord = ["Poor", "Ok", "Good", "Great"]
    headers   = ['System'] + tiers_ord
    col_fmt   = [LEFT] + [RIGHT] * len(tiers_ord)

    rows = []
    for name in SYSTEMS_ORD:
        row = [SYS_SHORT[name]]
        for t in tiers_ord:
            r = tier_results[t]["systems"].get(name)
            row.append(_cew(r))
        rows.append(row)

    # Progressive WDT row
    prog_row = ['Progressive WDT']
    for t in tiers_ord:
        prog_row.append(fmt_pct4(tier_results[t]['cew_progressive']))
    rows.append(prog_row)

    return md_table(headers, rows, col_fmt=col_fmt)


# ─────────────────────────────────────────────────────────────────────────────
# TABLE WFR.11  Module 4: Distributional incidence
# ─────────────────────────────────────────────────────────────────────────────

def table_wfr11(tier_results: dict) -> str:
    """WFR.11: Expected tax as % of W₀ by tier and system (γ=2)."""
    tiers_ord = ["Poor", "Ok", "Good", "Great"]
    headers   = ['System'] + [f'{t} (W₀=£{tier_results[t]["tier"].W0:.0f}m)' for t in tiers_ord]
    col_fmt   = [LEFT] + [RIGHT] * len(tiers_ord)

    rows = []
    for name in SYSTEMS_ORD:
        row = [SYS_SHORT[name]]
        for t in tiers_ord:
            et_pct = tier_results[t]['et_pct_W0'].get(name)
            row.append(f'{et_pct:.4f}%' if et_pct is not None else '—')
        rows.append(row)
    return md_table(headers, rows, col_fmt=col_fmt)


# ─────────────────────────────────────────────────────────────────────────────
# TABLE WFR.12  Module 4: Concentration path at key years
# ─────────────────────────────────────────────────────────────────────────────

def table_wfr12(paths: dict, tiers: list, years: list) -> str:
    """
    WFR.12: Great/Poor wealth ratio at key years.
    Key years are chosen to span the path evenly given actual path length.
    Rows = system. Columns = scenario years.
    """
    systems   = ["symmetric_wdt", "progressive_wdt", "stock_wealth", "income", "consumption"]
    sys_labels= {
        "symmetric_wdt"  : "Symmetric WDT",
        "progressive_wdt": "Progressive WDT",
        "stock_wealth"   : "Stock Wealth Tax",
        "income"         : "Income Tax",
        "consumption"    : "Consumption Tax",
    }

    # Infer path length from first available Great-tier path.
    # Path has N+1 entries: index 0 = initial W0, index N = end of year N.
    path_len = 0
    for name in systems:
        if name in paths and "Great" in paths[name]:
            path_len = len(paths[name]["Great"])
            break
    N = path_len - 1  # number of projection years

    # Build key year indices spanning [0, N] evenly (5 columns).
    # Always include initial (0) and final (N) as anchor points.
    if N >= 73:
        key_indices = [0, 10, 25, 50, 73]
    elif N >= 30:
        key_indices = [0, 5, 10, 20, N]
    else:
        step = max(1, N // 4)
        key_indices = sorted(set([0, step, 2 * step, 3 * step, N]))

    # Map path index → calendar year label.
    # years is the list of scenario years (length N, one per projection step).
    # Index 0 in path = start of year years[0] (W0 before any return is applied).
    year0 = years[0] if years else 0
    def _year_label(idx):
        if idx == 0:
            return 'Initial'
        cal_year = year0 + idx - 1
        return str(cal_year)

    headers = ['System'] + [_year_label(ky) for ky in key_indices]
    col_fmt = [LEFT] + [RIGHT] * len(key_indices)

    rows = []
    for name in systems:
        if name not in paths:
            continue
        great_path = paths[name].get("Great", [])
        poor_path  = paths[name].get("Poor",  [])
        if len(great_path) == 0:
            continue
        row = [sys_labels.get(name, name)]
        for ky in key_indices:
            idx = min(ky, len(great_path) - 1)
            if poor_path[idx] > 0:
                ratio = great_path[idx] / poor_path[idx]
                row.append(_ratio(ratio))
            else:
                row.append('—')
        rows.append(row)
    return md_table(headers, rows, col_fmt=col_fmt)


# ─────────────────────────────────────────────────────────────────────────────
# TABLE WFR.13  Module 4: Envelope binding summary
# ─────────────────────────────────────────────────────────────────────────────

def table_wfr13(envelope_results: dict, tiers: list) -> str:
    """WFR.13: Lifetime contribution envelope binding by tier."""
    headers = ['Tier', 'W₀ (£m)', 'Cumulative tax (£m)',
               'Cumulative refund (£m)', 'Min slack (£m)',
               'Binding years', 'Ever binds?']
    col_fmt = [LEFT, RIGHT, RIGHT, RIGHT, RIGHT, CENTER, CENTER]

    rows = []
    tier_w0 = {t.name: t.W0 for t in tiers}
    for tier_name, er in envelope_results.items():
        binding_str = ', '.join(str(y) for y in er['binding_years']) if er['binding_years'] else '—'
        rows.append([
            tier_name,
            fmt_gbp_m(tier_w0.get(tier_name, 0), dp=1),
            fmt_gbp_m(er['cum_tax_final'],  dp=3),
            fmt_gbp_m(er['cum_ref_final'],  dp=3),
            fmt_gbp_m(er['min_slack'],      dp=4),
            binding_str,
            '⚠ Yes' if er['ever_binds'] else 'No',
        ])
    return md_table(headers, rows, col_fmt=col_fmt)


# ─────────────────────────────────────────────────────────────────────────────
# MASTER DOCUMENT ASSEMBLY
# ─────────────────────────────────────────────────────────────────────────────

def build_appendix(
    all_results   : dict,
    dists         : dict,
    c1_results    : dict,
    c2_lev_results: list,
    c3_results    : list,
    W0_vals_c3    : list,
    sens_gain     : list,
    sens_T        : list,
    comp_A        : dict,
    comp_B        : dict,
    tier_results  : dict,
    paths         : dict,
    conc_years    : list,
    envelope      : dict,
    tiers         : list,
    p             : dict,
) -> MdDoc:
    """Assemble the full appendix markdown document."""

    doc = MdDoc()
    doc.h1('WFR Welfare Comparison Model — Appendix Tables')
    doc.blank()
    doc.add(f'*Generated: {today_iso()}*')
    doc.add(f'*Revenue target: E[T] = {TARGET_ET*100:.0f}% of W₀ across all systems.*')
    doc.add('*All CEW values relative to no-tax benchmark. Positive = welfare-superior to no-tax.*')
    doc.blank()
    doc.rule()

    # ── Module 1 ──────────────────────────────────────────────────────────────
    doc.blank()
    doc.h2('Module 1: Baseline Single-Agent Comparison')
    doc.blank()

    doc.h3('Table WFR.1 — Consumption-Equivalent Welfare (CEW) by system, γ, and distribution')
    scenario_start = p["tcm"].get("scenario_start_year", p["returns"]["series_base_year"])
    canonical_N    = p["tcm"].get("canonical_N", 30)
    doc.note(
        f'CEW = proportional consumption change under no-tax making agent indifferent '
        f'to the taxed system. Negative = welfare cost relative to no-tax. '
        f'Numbers are for the {canonical_N}-year scenario sequence starting '
        f'{scenario_start} (canonical_N = {canonical_N} from TOML [tcm]); '
        f'they differ from full 73-year series values (1947–2019) by construction — '
        f'the scenario and full-series runs are separate sensitivity configurations. '
        f'Ver. A = empirical returns {scenario_start}–{scenario_start + canonical_N - 1} '
        f'({canonical_N} obs, equal probability 1/{canonical_N}). '
        f'Ver. B = idealised two-state calibrated to scenario μ and σ '
        f'(p=0.5, R_good=E[R]+σ, R_bad=E[R]−σ). '
        f'Full 73-year series numbers appear in the backbone reference figures.'
    )
    doc.add_block(table_wfr1(all_results))
    doc.blank()

    doc.h3('Table WFR.2 — Variance of Consumption by system (γ=2)')
    doc.note(
        'Variance of consumption across return states at revenue-equivalent rates. '
        'Lower variance indicates greater risk-sharing. '
        'D-M prediction: Var(C_sym) = (1−τ)² × Var(C_notax).'
    )
    doc.add_block(table_wfr2(all_results))
    doc.blank()

    doc.h3('Table WFR.3 — Revenue-Equivalent Tax Rates (γ=2)')
    doc.note(
        'Rate τ* such that E[T(W₀, dist, τ*)] = target. '
        'Rates differ across systems because tax bases differ. '
        'Stock wealth and consumption taxes require low rates (broad base); '
        'income tax and CGT require higher rates (gains only, no collection in loss states).'
    )
    doc.add_block(table_wfr3(all_results))
    doc.blank()

    doc.h3('Table WFR.4 — Domar–Musgrave Test: Symmetric WDT')
    doc.note(
        'Prediction: Var(C_tax) / Var(C_notax) = (1−τ)². '
        'Gap near zero confirms D-M holds for the flat-rate symmetric case. '
        'Progression breaks D-M — see Module 2.'
    )
    doc.add_block(table_wfr4(all_results, dists))
    doc.blank()
    doc.rule()

    # ── Module 2 ──────────────────────────────────────────────────────────────
    doc.blank()
    doc.h2('Module 2: Progressive Rates and the Three D-M Complications')
    doc.blank()

    doc.h3('Table WFR.5 — C1: Flat WDT vs Progressive WDT CEW')
    doc.note(
        'C1 complication: under a progressive rate, the government co-investment share '
        'varies with wealth level, breaking the flat D-M result. '
        'Revenue-equivalence calibration: the flat rate τ* is solved to match the '
        'progressive system\'s natural E[T], not the global 2%-of-W₀ target. '
        'Both systems therefore collect the same expected revenue; the gap measures '
        'the pure structural welfare difference from rate progression alone. '
        'The "vs 2% target" column shows how much the canonical logistic schedule '
        'deviates from the 2% benchmark at each W₀ — a negative figure means the '
        'logistic schedule is less aggressive than the global target at this wealth level. '
        'Gap (bp) = (CEW_flat − CEW_progressive) × 10,000; positive = flat WDT has lower '
        'welfare cost. '
        'W₀ = 5 × W_min = £10m for both distributions.'
    )
    doc.add_block(table_wfr5(c1_results))
    doc.blank()

    doc.h3('Table WFR.6b — C2: Leverage Effect on WDT Tax Base and Welfare')
    gross_assets_m = p['rate']['W_min'] * 5
    doc.note(
        f'C2 complication: when an agent holds debt, the WDT net-worth delta base '
        f'(ΔW = W₁ − W₀) amplifies or dampens the underlying asset return. '
        f'An unlevered agent has ΔW = A×(R−1) = ΔA; with leverage, ΔW = ΔA at the '
        f'asset level but net worth swings more sharply, enlarging the tax base in '
        f'rising markets and the refund base in falling markets. '
        f'Gross assets fixed at £{gross_assets_m:.0f}m throughout; net worth W₀ '
        f'declines as leverage rises (W₀ = A − D = A × (1 − lev. ratio)). '
        f'E[T] excess = E[T]_NW − E[T]_AR; CEW gap = (CEW_NW − CEW_AR) × 10,000. '
        f'Positive excess means the actual WDT collects more in expectation than a '
        f'hypothetical asset-return base would at the same progressive rate schedule — '
        f'the direction switches if expected asset returns are negative. '
        f'Version A distribution (scenario {p["tcm"].get("scenario_start_year", "—")}), γ=2.'
    )
    doc.add_block(table_wfr6b(c2_lev_results))
    doc.blank()

    doc.h3('Table WFR.6 — C3: Two-Period Rate Asymmetry by Initial Wealth')
    doc.note(
        'Sequence: +18.8% gain (μ+σ) in period 1, −8.3% loss (σ) in period 2. '
        'τ gain = effective rate on period-1 delta at (W₀, W₁). '
        'τ refund = effective rate on period-2 loss at (W₁, W₂). '
        'Asymmetry = τ gain − τ refund (pp); positive means gain taxed at higher rate. '
        'Excess = net tax progressive − net tax flat; positive = progression costs more.'
    )
    doc.add_block(table_wfr6(c3_results, W0_vals_c3))
    doc.blank()
    doc.rule()

    # ── Module 3 ──────────────────────────────────────────────────────────────
    doc.blank()
    doc.h2('Module 3: CGT Lock-In Distortion')
    doc.blank()
    doc.add(
        'Reference parameters: V=£10m, G/V=50%, r_A=10.45% (empirical equity mean), '
        'τ_cgt=24% (UK 2024 higher rate), T=5 years remaining.'
    )
    doc.blank()

    doc.h3('Table WFR.7 — Lock-In Welfare Cost by Embedded Gain Ratio')
    doc.note(
        'Lock-in cost (bp) = (CEW_free − CEW_locked) × 10,000. '
        'CEW_free: agent switches whenever r_B > r_A (no lock-in). '
        'CEW_locked: agent locked in under CGT when r_B < indifference return r_B*. '
        'Version A distribution. γ=2.'
    )
    doc.add_block(table_wfr7(sens_gain))
    doc.blank()

    doc.h3('Table WFR.8 — Lock-In Welfare Cost by Remaining Holding Period')
    doc.note(
        'G/V=50% fixed. T varies. Lock-in cost declines as T increases '
        'because future switching opportunities reduce the cost of current lock-in. '
        'Indifference return r_B* converges to r_A as T→∞.'
    )
    doc.add_block(table_wfr8(sens_T))
    doc.blank()

    doc.h3('Table WFR.9 — Full Welfare Comparison: WDT vs CGT (with and without lock-in)')
    doc.note(
        'Module 1 showed WDT ≈ CGT when lock-in was absent. '
        'This table adds the lock-in cost to CGT, correcting that comparison. '
        'WDT advantage (with lock-in) = CEW_WDT − CEW_CGT_locked.'
    )
    doc.add_block(table_wfr9(comp_A, comp_B))
    doc.blank()
    doc.rule()

    # ── Module 4 ──────────────────────────────────────────────────────────────
    doc.blank()
    doc.h2('Module 4: Heterogeneous Agents — Incidence and Concentration')
    doc.blank()
    doc.add(
        'Tier differentials from Fagereng et al. (2020): Poor −4.55pp, Ok −2.05pp, '
        'Good +0.95pp, Great +3.45pp relative to UK historical equity mean (10.45%). '
        'Version A distribution with tier-shifted returns. γ=2.'
    )
    doc.blank()

    doc.h3('Table WFR.10 — CEW by Tier and Tax System')
    doc.note(
        'Progressive WDT uses logistic rate function from TOML '
        '(τ₀=15%, τ_m=70%, k=0.001, W_min=£2m). '
        'All flat-rate systems revenue-equivalent at 2% of Good-tier W₀.'
    )
    doc.add_block(table_wfr10(tier_results))
    doc.blank()

    doc.h3('Table WFR.11 — Distributional Incidence: Expected Tax as % of W₀')
    doc.note(
        'E[T] / W₀ × 100. All systems calibrated to the same revenue target. '
        'Rates differ across tiers because shifted return distributions change E[T]. '
        'Progressive WDT incidence not shown here — see Table WFR.10 CEW column.'
    )
    doc.add_block(table_wfr11(tier_results))
    doc.blank()

    doc.h3('Table WFR.12 — Wealth Concentration Path: Great/Poor Ratio at Key Years')
    doc.note(
        'Great-tier wealth / Poor-tier wealth at selected years. '
        'All systems calibrated at the population-weighted aggregate tau from '
        'Table WFR.10 (same rate as Parts B/C welfare comparison). '
        'Progressive WDT uses the logistic rate function directly. '
        'Initial ratio reflects W₀ difference only (150 / 3 = 50×). '
        f'Return heterogeneity compounds over {p["tcm"].get("canonical_N", 30)}-year scenario horizon '
        f'starting {p["tcm"].get("scenario_start_year", "—")}.'
    )
    doc.add_block(table_wfr12(paths, tiers, conc_years))
    doc.blank()

    doc.h3('Table WFR.13 — Lifetime Contribution Envelope: Binding Summary')
    doc.note(
        'Envelope binds when cumulative refunds would exceed cumulative taxes paid. '
        'Refund capped at cumulative taxes paid to date when binding occurs. '
        'Min slack = minimum of (cum. tax − cum. refund) over all 73 years. '
        'Zero min slack means envelope was exactly hit but not exceeded.'
    )
    doc.add_block(table_wfr13(envelope, tiers))
    doc.blank()
    doc.rule()

    doc.blank()
    doc.h2('Parameter Reference')
    doc.blank()
    doc.add('| Parameter | Value | Source |')
    doc.add('|:---|---:|:---|')
    rp = p['rate']
    doc.add(f'| W₀ (normalised Module 1) | {W0_BASE:.1f} | — |')
    doc.add(f'| Revenue target E[T] | {TARGET_ET*100:.0f}% of W₀ | — |')
    doc.add(f'| γ (central case) | 2.0 | Flavin & Yamashita (2002) |')
    doc.add(f'| τ₀ (WDT entry rate) | {rp["tau_0"]*100:.0f}% | TOML [rate] |')
    doc.add(f'| τ_m (WDT ceiling) | {rp["tau_m"]*100:.0f}% | TOML [rate] |')
    doc.add(f'| k (logistic steepness) | {rp["k"]} | TOML [rate] |')
    doc.add(f'| W_min (£m) | £{rp["W_min"]:.0f}m | TOML [rate] |')
    doc.add(f'| UK equity mean (1947–2019) | {p["tcm"]["hist_mean"]*100:.2f}% | JST dataset |')
    doc.add(f'| UK equity std dev | {np.std(p["returns"]["array"])*100:.2f}% | JST dataset |')
    doc.blank()

    return doc


# ─────────────────────────────────────────────────────────────────────────────
# INDIVIDUAL TABLE WRITERS  (called from each module if needed standalone)
# ─────────────────────────────────────────────────────────────────────────────

def write_table(content: str, filename: str, caption: str = '') -> Path:
    """Write a single table as a standalone markdown file."""
    doc = MdDoc()
    if caption:
        doc.add(f'*{caption}*')
        doc.blank()
    doc.add_block(content)
    path = OUTPUT_DIR / filename
    return doc.write(path)


# ─────────────────────────────────────────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────────────────────────────────────────

def main():
    print('=' * 70)
    print('WFR Welfare Tables — Appendix Generation')
    print('=' * 70)

    p      = load_params(str(TOML_PATH))
    dist_A = make_empirical_distribution(p)
    dist_B = make_idealised_distribution(p)
    dists  = {dist_A.label: dist_A, dist_B.label: dist_B}

    rp = p['rate']
    rate_fn = ProgressiveRateFunction(
        tau0=rp['tau_0'], taum=rp['tau_m'],
        k=rp['k'], W_min=rp['W_min']
    )

    # ── Module 1 results ──────────────────────────────────────────────────────
    print('\n--- Running Module 1 ---')
    all_results = {}
    for dist in [dist_A, dist_B]:
        all_results[dist.label] = {}
        for gamma in GAMMA_VALS:
            all_results[dist.label][gamma] = run_welfare_comparison(
                W0=W0_BASE, dist=dist, gamma=gamma, target_et=TARGET_ET
            )

    # ── Module 2 results ──────────────────────────────────────────────────────
    print('--- Running Module 2 ---')
    W0_c1 = rp['W_min'] * 5   # £10m
    c1_results = {}
    for dist in [dist_A, dist_B]:
        c1_results[dist.label] = {}
        for gamma in GAMMA_VALS:
            c1_results[dist.label][gamma] = run_c1_analysis(
                W0_c1, dist, rate_fn, gamma, TARGET_ET * W0_c1
            )

    mu    = p['tcm']['hist_mean']
    sigma = float(np.std(p['returns']['array'], ddof=0))
    R1_good = 1.0 + mu + sigma
    R2_loss = 1.0 - sigma

    flat_fn  = get_tax_fn('symmetric_wdt')
    tau_flat = solve_revenue_equivalent_rate(W0_c1, dist_A, flat_fn, TARGET_ET * W0_c1)

    # C2: leverage grid — 0% to 70% in 15 steps, gross assets = W_min × 5
    gross_assets_c2  = rp['W_min'] * 5     # £10m (same reference as C1)
    leverage_grid    = np.linspace(0.0, 0.70, 15)
    c2_lev_results   = []
    for lev in leverage_grid:
        agent = LeveragedAgent(
            gross_assets=gross_assets_c2,
            debt=gross_assets_c2 * lev,
        )
        c2_lev_results.append(run_c2_leverage(agent, dist_A, rate_fn, gamma=2.0))

    W0_vals_c3 = [rp['W_min'] * m for m in [1.5, 2, 5, 10, 20, 50, 100]]
    c3_results = [
        run_c3_two_period(W0, R1_good, R2_loss, rate_fn, 2.0, tau_flat)
        for W0 in W0_vals_c3
    ]

    # ── Module 3 results ──────────────────────────────────────────────────────
    print('--- Running Module 3 ---')
    V_ref   = 10.0
    G_ref   = V_ref * 0.50
    r_A     = p['tcm']['hist_mean']
    tau_cgt = 0.24

    asset_ref = AssetSwitchDecision(
        V=V_ref, B=V_ref - G_ref, tau_cgt=tau_cgt, T=5, r_A=r_A
    )

    gain_ratios = np.linspace(0.05, 0.90, 20)
    sens_gain   = sensitivity_gain_ratio(V_ref, r_A, 5, tau_cgt, dist_A, 2.0, gain_ratios)
    sens_T      = sensitivity_holding_period(V_ref, G_ref, r_A, tau_cgt, dist_A, 2.0, list(range(1, 21)))

    comp_A = full_comparison_with_lockin(10.0, dist_A, 2.0, TARGET_ET * 10.0, asset_ref)
    comp_B = full_comparison_with_lockin(10.0, dist_B, 2.0, TARGET_ET * 10.0, asset_ref)

    # ── Module 4 results ──────────────────────────────────────────────────────
    print('--- Running Module 4 ---')
    tiers        = build_tiers(p)
    tier_results = run_tier_comparison(tiers, dist_A, 2.0, rate_fn)

    # Extract aggregate taus for consistent calibration with Parts B/C
    agg_taus = {
        name: tier_results["Good"]["systems"][name].tau
        for name in ["symmetric_wdt", "stock_wealth", "income", "cgt", "consumption"]
        if tier_results["Good"]["systems"].get(name)
        and tier_results["Good"]["systems"][name].tau is not None
    }

    systems_proj = ['symmetric_wdt', 'progressive_wdt', 'stock_wealth', 'income', 'consumption']
    # Unpack tuple (paths_dict, years_list) returned by run_concentration_analysis
    paths, conc_years = run_concentration_analysis(
        tiers, p, rate_fn, systems_proj, precomputed_taus=agg_taus
    )
    envelope     = test_envelope_binding(tiers, p, rate_fn)

    # ── Assemble and write ─────────────────────────────────────────────────────
    print('\n--- Assembling appendix ---')
    doc = build_appendix(
        all_results=all_results, dists=dists,
        c1_results=c1_results,
        c2_lev_results=c2_lev_results,
        c3_results=c3_results, W0_vals_c3=W0_vals_c3,
        sens_gain=sens_gain, sens_T=sens_T,
        comp_A=comp_A, comp_B=comp_B,
        tier_results=tier_results,
        paths=paths, conc_years=conc_years, envelope=envelope,
        tiers=tiers, p=p,
    )

    out_path = OUTPUT_DIR / 'WFR_appendix_tables.md'
    doc.write(out_path)

    # Also write each table individually
    print('\n--- Writing individual tables ---')
    write_table(table_wfr1(all_results),  'WFR_T01_cew_by_system.md',
                'Table WFR.1: CEW by system, γ, and distribution.')
    write_table(table_wfr2(all_results),  'WFR_T02_variance.md',
                'Table WFR.2: Variance of consumption (γ=2).')
    write_table(table_wfr3(all_results),  'WFR_T03_rates.md',
                'Table WFR.3: Revenue-equivalent rates.')
    write_table(table_wfr4(all_results, dists), 'WFR_T04_dm_test.md',
                'Table WFR.4: Domar–Musgrave test.')
    write_table(table_wfr5(c1_results),   'WFR_T05_c1_progression.md',
                'Table WFR.5: C1 flat vs progressive WDT.')
    write_table(table_wfr6b(c2_lev_results), 'WFR_T06b_c2_leverage.md',
                'Table WFR.6b: C2 leverage effect on WDT tax base and welfare.')
    write_table(table_wfr6(c3_results, W0_vals_c3), 'WFR_T06_c3_asymmetry.md',
                'Table WFR.6: C3 two-period rate asymmetry.')
    write_table(table_wfr7(sens_gain),    'WFR_T07_lockin_gain.md',
                'Table WFR.7: Lock-in cost by gain ratio.')
    write_table(table_wfr8(sens_T),       'WFR_T08_lockin_T.md',
                'Table WFR.8: Lock-in cost by holding period.')
    write_table(table_wfr9(comp_A, comp_B), 'WFR_T09_wdt_vs_cgt.md',
                'Table WFR.9: WDT vs CGT including lock-in.')
    write_table(table_wfr10(tier_results), 'WFR_T10_tier_cew.md',
                'Table WFR.10: CEW by tier and system.')
    write_table(table_wfr11(tier_results), 'WFR_T11_incidence.md',
                'Table WFR.11: Distributional incidence.')
    write_table(table_wfr12(paths, tiers, conc_years),
                'WFR_T12_concentration.md',
                'Table WFR.12: Wealth concentration path.')
    write_table(table_wfr13(envelope, tiers), 'WFR_T13_envelope.md',
                'Table WFR.13: Envelope binding summary.')

    print(f'\n✓ Tables complete. Outputs in: {OUTPUT_DIR}')
    print(f'  Master document: {out_path}')


if __name__ == '__main__':
    main()