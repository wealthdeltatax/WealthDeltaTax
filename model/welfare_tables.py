"""
welfare_tables.py
=====================
Tabular output for the WFR Welfare Comparison Model.

Produces appendix-ready markdown tables from all four module results,
using the project's canonical helpers (wdt_md, wdt_fmt, wdt_style).

Each table is self-contained: it can be copied directly into the paper's
appendix without reformatting. Tables are also written individually so
each module can include only its own tables.

Table inventory
---------------
Section A — Module 1: Baseline Single-Agent Comparison
  Table A.1 — CEW comparison across systems and γ values (both distributions)
  Table A.2 — Variance of consumption by system (both distributions, γ=2)
  Table A.3 — Revenue-equivalent rates by system and distribution
  Table A.4 — Domar-Musgrave test results

Section B — Module 2: Progressive Rates and the Three D-M Complications
  Table B.1 — Flat vs progressive WDT CEW (both distributions, all γ)
  Table B.2 — Leverage effect on WDT tax base and welfare (by leverage ratio)
  Table B.3 — Two-period rate asymmetry by wealth level

Section C — Module 3: CGT Lock-In Distortion
  Table C.1 — Lock-in welfare cost — sensitivity to gain ratio
  Table C.2 — Lock-in welfare cost — sensitivity to holding period
  Table C.3 — Full welfare comparison WDT vs CGT (with/without lock-in)

Section D — Module 4: Heterogeneous Agents
  Table D.1 — Tier-by-tier CEW under all systems
  Table D.2 — Distributional incidence (expected tax as % of W₀)
  Table D.3 — Concentration path — Great/Poor wealth ratio at key years
  Table D.4 — Envelope binding summary by tier
  Table D.5 — Off-diagonal spot check — Great diff at Poor W₀ and Poor
                diff at Great W₀ vs the empirical diagonal

Section E — Module 5: Welfare Sweep Analysis
  Table E.1.1 — Sweep A: CEW by system and revenue target
  Table E.2.1 — Sweep B: Summary statistics across all start years
  Table E.2.2 — Sweep B: Curated worst-case start years
  Table E.3.1 — Sweep C: τ₀ sensitivity
  Table E.3.2 — Sweep C: τ_m sensitivity
  Table E.3.3 — Sweep C: k sensitivity
  Table E.3.4 — Sweep C: W_min sensitivity

All tables written to: model/OUTPUTS/WFR/tables/
Master document (all tables): WFR_appendix_tables.md
"""

import sys
import math
import numpy as np
from pathlib import Path

# ── project helpers ───────────────────────────────────────────────────────────
from welfare_paths import TOML_PATH, module_output_dir
from wdt_md  import MdDoc, md_table, LEFT, RIGHT, CENTER
from wdt_fmt import fmt_pct, fmt_pct0, fmt_pct1, fmt_pct4, fmt_gbp_m, today_iso

# ── welfare model imports ─────────────────────────────────────────────────────
from welfare_core import (
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
    make_empirical_distribution_scenario,
    make_idealised_distribution_scenario,
)

import importlib as _il

from welfare_progressive import ProgressiveRateFunction

_m2 = _il.import_module('19_3_module2_progression')
run_c1_analysis   = _m2.run_c1_analysis
run_c2_leverage   = _m2.run_c2_leverage
run_c3_two_period = _m2.run_c3_two_period
LeveragedAgent    = _m2.LeveragedAgent

_m3 = _il.import_module('19_4_module3_lockin')
AssetSwitchDecision = _m3.AssetSwitchDecision
compute_lock_in_welfare_cost = _m3.compute_lock_in_welfare_cost
sensitivity_gain_ratio = _m3.sensitivity_gain_ratio
sensitivity_holding_period = _m3.sensitivity_holding_period
full_comparison_with_lockin = _m3.full_comparison_with_lockin

_m4 = _il.import_module('19_5_module4_heterogeneous')
AgentTier = _m4.AgentTier
build_tiers = _m4.build_tiers
run_tier_comparison = _m4.run_tier_comparison
run_concentration_analysis = _m4.run_concentration_analysis
test_envelope_binding = _m4.test_envelope_binding
run_corner_check = _m4.run_corner_check

_m5 = _il.import_module('19_6_module5_sweeps')
run_sweep_a = _m5.run_sweep_a
run_sweep_b = _m5.run_sweep_b
run_sweep_c_param = _m5.run_sweep_c_param

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
    return fmt_pct(r.tau, dp=3) if r and r.tau is not None else '—'

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
    return fmt_pct4(v)

def _bp(v):
    if v is None: return '—'
    return f'{v:+.2f} bp'

def _ratio(v):
    if v is None or math.isnan(v): return '—'
    return f'{v:,.1f}×'


# ─────────────────────────────────────────────────────────────────────────────
# TABLE A..1  CEW by system, γ, distribution
# ─────────────────────────────────────────────────────────────────────────────

def table_a1(all_results: dict) -> str:
    """
    A.1: CEW (%) for all systems across γ = 1, 2, 4 and both distributions.
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
# TABLE A.2  Variance of consumption by system (γ=2, both distributions)
# ─────────────────────────────────────────────────────────────────────────────

def table_a2(all_results: dict) -> str:
    """A.2: Var(consumption) at γ=2 for both distributions."""
    dist_keys = list(all_results.keys())
    headers   = ['System', 'Ver. A Var(C)', 'Ver. B Var(C)']
    col_fmt   = [LEFT, RIGHT, RIGHT]
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
# TABLE A.3  Revenue-equivalent rates
# ─────────────────────────────────────────────────────────────────────────────

def table_a3(all_results: dict) -> str:
    """A.3: Revenue-equivalent tax rate τ* for each system and distribution (γ=2)."""
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
# TABLE A.4  Domar-Musgrave test
# ─────────────────────────────────────────────────────────────────────────────

def table_a4(all_results: dict, dists: dict) -> str:
    """A.4: D-M test results for symmetric WDT at all (dist, γ) combinations."""
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
# TABLE B.1  Module 2 C1: Flat vs progressive WDT
# ─────────────────────────────────────────────────────────────────────────────

def table_b1(c1_results: dict) -> str:
    """B.1: C1 flat vs progressive CEW and gap across γ and distributions."""
    headers = ['Distribution', 'γ', 'Flat WDT CEW', 'Progressive WDT CEW',
               'Gap (bp)', 'E[T] progressive']
    col_fmt = [LEFT, RIGHT, RIGHT, RIGHT, RIGHT, RIGHT]
    rows = []
    for dk, gamma_results in c1_results.items():
        for g, r in gamma_results.items():
            rows.append([
                dist_label_map_fn(dk),
                f'{g:.1f}',
                fmt_pct4(r['cew_flat']),
                fmt_pct4(r['cew_progressive']),
                f'{r["cew_gap_bp"]:+.2f}',
                fmt_gbp_m(r['et_progressive'], dp=4),
            ])
    return md_table(headers, rows, col_fmt=col_fmt)


# ─────────────────────────────────────────────────────────────────────────────
# TABLE B.2  Module 2 C3: Rate asymmetry by wealth level
# ─────────────────────────────────────────────────────────────────────────────

def table_b3(c3_results: list, W0_vals: list) -> str:
    """B.2: Two-period rate asymmetry — gain-then-loss path by initial wealth."""
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
# TABLE B.2b  Module 2 C2: Leverage effect on tax base and welfare
# ─────────────────────────────────────────────────────────────────────────────

def table_b2(lev_results: list) -> str:
    """
    B.2b: C2 leverage — net-worth delta base vs hypothetical asset-return base.

    Rows: leverage ratios swept from 0% to 70%.
    Columns: leverage ratio, W₀ (net worth after debt), E[T] under NW base,
             E[T] under asset-return base, CEW under NW base, CEW under
             asset-return base, CEW gap (NW − AR) in basis points.

    A positive gap means the WDT's actual NW-delta base produces higher
    welfare than a hypothetical asset-return base at the same rate schedule.
    A negative gap means leverage amplifies the NW delta enough to hurt
    welfare relative to the asset-return baseline.
    """
    headers = [
        'Leverage (%)',
        'W₀ net (£m)',
        'E[T] NW base',
        'E[T] asset-rtn base',
        'CEW NW base',
        'CEW asset-rtn base',
        'Gap (bp)',
    ]
    col_fmt = [RIGHT, RIGHT, RIGHT, RIGHT, RIGHT, RIGHT, RIGHT]
    rows = []
    for r in lev_results:
        rows.append([
            f'{r["leverage_ratio"]*100:.1f}',
            fmt_gbp_m(r['W0'], dp=2),
            f'{r["et_nw"]:.4f}',
            f'{r["et_ar"]:.4f}',
            fmt_pct4(r['cew_nw']),
            fmt_pct4(r['cew_ar']),
            f'{r["cew_gap_bp"]:+.2f}',
        ])
    return md_table(headers, rows, col_fmt=col_fmt)


# ─────────────────────────────────────────────────────────────────────────────
# TABLE C.1  Module 3: Lock-in cost vs gain ratio
# ─────────────────────────────────────────────────────────────────────────────

def table_c1(sens_gain: list) -> str:
    """C.1: Lock-in welfare cost by embedded gain ratio G/V."""
    headers = ['G/V (%)', 'CEW (free)', 'CEW (locked)', 'Lock-in cost (bp)',
               'P(total locked)', 'P(CGT distortion)', 'P(r_B < r_A)']
    col_fmt = [RIGHT, RIGHT, RIGHT, RIGHT, RIGHT, RIGHT, RIGHT]
    rows = []
    for r in sens_gain:
        rows.append([
            f'{r["gain_ratio"]*100:.1f}',
            fmt_pct4(r['cew_free']),
            fmt_pct4(r['cew_locked']),
            f'{r["lock_in_cost_bp"]:+.2f}',
            fmt_pct1(r['p_locked']),
            fmt_pct1(r.get('p_locked_cgt', float('nan'))),
            fmt_pct1(r.get('p_below_rA',   float('nan'))),
        ])
    return md_table(headers, rows, col_fmt=col_fmt)


# ─────────────────────────────────────────────────────────────────────────────
# TABLE C.2  Module 3: Lock-in cost vs holding period
# ─────────────────────────────────────────────────────────────────────────────

def table_c2(sens_T: list) -> str:
    """C.2: Lock-in welfare cost by remaining holding period T."""
    headers = ['T (years)', 'r_B* (%)', 'Lock-in cost (bp)',
               'P(total locked)', 'P(CGT distortion)', 'P(r_B < r_A)']
    col_fmt = [RIGHT, RIGHT, RIGHT, RIGHT, RIGHT, RIGHT]
    rows = []
    for r in sens_T:
        rows.append([
            str(r['T']),
            f'{r["r_B_indiff"]*100:.4f}%',
            f'{r["lock_in_cost_bp"]:+.2f}',
            fmt_pct1(r['p_locked']),
            fmt_pct1(r.get('p_locked_cgt', float('nan'))),
            fmt_pct1(r.get('p_below_rA',   float('nan'))),
        ])
    return md_table(headers, rows, col_fmt=col_fmt)


# ─────────────────────────────────────────────────────────────────────────────
# TABLE C.3  Module 3: Full WDT vs CGT comparison
# ─────────────────────────────────────────────────────────────────────────────

def table_c3(comp_A: dict, comp_B: dict) -> str:
    """C.3: Full WDT vs CGT welfare comparison including lock-in."""
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
# TABLE D.1  Module 4: Tier-by-tier CEW
# ─────────────────────────────────────────────────────────────────────────────

def table_d1(tier_results: dict) -> str:
    """D.1: CEW by tier and system (γ=2)."""
    tiers_ord = ["Poor", "Ok", "Good", "Great"]
    headers   = ['System'] + [
        f'{t} ({tier_results[t]["tier"].bracket_label}, '
        f'W\u2080={fmt_gbp_m(tier_results[t]["tier"].W0, dp=1)})'
        for t in tiers_ord
    ]
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
# TABLE D.2  Module 4: Distributional incidence
# ─────────────────────────────────────────────────────────────────────────────

def table_d2(tier_results: dict) -> str:
    """D.2: Expected tax as % of W₀ by tier and system (γ=2)."""
    tiers_ord = ["Poor", "Ok", "Good", "Great"]
    headers   = ['System'] + [
        f'{t} ({tier_results[t]["tier"].bracket_label}, '
        f'W\u2080={fmt_gbp_m(tier_results[t]["tier"].W0, dp=1)})'
        for t in tiers_ord
    ]
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
# TABLE D.3  Module 4: Concentration path at key years
# ─────────────────────────────────────────────────────────────────────────────

def table_d3(paths: dict, tiers: list, years: list) -> str:
    """
    D.3: Great/Poor wealth ratio at key years.
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
# TABLE D.4  Module 4: Envelope binding summary
# ─────────────────────────────────────────────────────────────────────────────

def table_d4(envelope_results: dict, tiers: list) -> str:
    """D.4: Lifetime contribution envelope binding by tier."""
    headers = ['Tier', 'Bracket', 'W\u2080 (£m)', 'Cumulative tax (£m)',
               'Cumulative refund (£m)', 'Min slack (£m)',
               'Binding years', 'Ever binds?']
    col_fmt = [LEFT, LEFT, RIGHT, RIGHT, RIGHT, RIGHT, CENTER, CENTER]

    rows = []
    tier_lookup = {t.name: t for t in tiers}
    for tier_name, er in envelope_results.items():
        tier_obj      = tier_lookup.get(tier_name)
        W0_val        = tier_obj.W0            if tier_obj else 0
        bracket_label = tier_obj.bracket_label if tier_obj else '—'
        binding_str   = ', '.join(str(y) for y in er['binding_years']) if er['binding_years'] else '—'
        rows.append([
            tier_name,
            bracket_label,
            fmt_gbp_m(W0_val, dp=1),
            fmt_gbp_m(er['cum_tax_final'],  dp=3),
            fmt_gbp_m(er['cum_ref_final'],  dp=3),
            fmt_gbp_m(er['min_slack'],      dp=4),
            binding_str,
            '⚠ Yes' if er['ever_binds'] else 'No',
        ])
    return md_table(headers, rows, col_fmt=col_fmt)


# ─────────────────────────────────────────────────────────────────────────────
# TABLE D.2.1  Module 4, Part F: Off-diagonal spot check
# ─────────────────────────────────────────────────────────────────────────────

def table_d5(corner_results: dict, tier_results: dict) -> str:
    """
    D.2.1: Off-diagonal corner CEW vs diagonal cells.

    Two row-groups, one per corner:
      Corner A — Great differential (+3.45pp) at Poor W₀ (£2.86m)
      Corner B — Poor differential (−4.55pp) at Great W₀ (£139.6m)

    Columns: Corner CEW | Diagonal (same W₀) | Diagonal (same diff) | Δ (bp)

    The Δ column isolates how much the CEW changes when the return
    differential is decoupled from the empirically correlated wealth level.
    A small Δ means the diagonal result is robust to the correlation
    assumption; a large Δ means both dimensions drive the main result jointly.
    """
    systems_ordered = ["symmetric_wdt", "stock_wealth", "income", "cgt", "consumption"]
    sys_labels_short = {
        "symmetric_wdt" : "Symmetric WDT",
        "stock_wealth"  : "Stock Wealth Tax",
        "income"        : "Income Tax",
        "cgt"           : "CGT",
        "consumption"   : "Consumption Tax",
    }

    corner_configs = [
        ("corner_A", "Corner A: Great diff (+3.45pp), Poor W₀ (£2.86m)", "Poor",  "Great"),
        ("corner_B", "Corner B: Poor diff (−4.55pp), Great W₀ (£139.6m)", "Great", "Poor"),
    ]

    headers = [
        'Corner / System',
        'Corner CEW',
        'Diagonal (same W₀)',
        'Diagonal (same diff)',
        'Δ vs same-W₀ (bp)',
    ]
    col_fmt = [LEFT, RIGHT, RIGHT, RIGHT, RIGHT]
    rows = []

    for corner_key, corner_label, diag_w0_tier, diag_diff_tier in corner_configs:
        cr        = corner_results[corner_key]
        diag_w0   = tier_results[diag_w0_tier]
        diag_diff = tier_results[diag_diff_tier]

        # Section header row (blank cells for data columns)
        rows.append([f'**{corner_label}**', '', '', '', ''])

        for name in systems_ordered:
            sr_c  = cr["systems"].get(name)
            sr_w0 = diag_w0["systems"].get(name)
            sr_d  = diag_diff["systems"].get(name)

            c_cew  = sr_c.cew  if sr_c  and sr_c.cew  is not None else None
            w0_cew = sr_w0.cew if sr_w0 and sr_w0.cew is not None else None
            d_cew  = sr_d.cew  if sr_d  and sr_d.cew  is not None else None
            delta  = (c_cew - w0_cew) * 10000 if (c_cew is not None and w0_cew is not None) else None

            rows.append([
                f'\u00a0\u00a0{sys_labels_short[name]}',   # indent with non-breaking spaces
                fmt_pct4(c_cew),
                fmt_pct4(w0_cew),
                fmt_pct4(d_cew),
                f'{delta:+.2f}' if delta is not None else '—',
            ])

        # Progressive WDT row
        c_prog  = cr["cew_progressive"]
        w0_prog = diag_w0["cew_progressive"]
        d_prog  = diag_diff["cew_progressive"]
        delta_p = (c_prog - w0_prog) * 10000
        rows.append([
            '\u00a0\u00a0Progressive WDT',
            fmt_pct4(c_prog),
            fmt_pct4(w0_prog),
            fmt_pct4(d_prog),
            f'{delta_p:+.2f}',
        ])

        # Blank separator between corners
        rows.append(['', '', '', '', ''])

    # Drop trailing blank row
    if rows and rows[-1] == ['', '', '', '', '']:
        rows = rows[:-1]

    return md_table(headers, rows, col_fmt=col_fmt)


# ─────────────────────────────────────────────────────────────────────────────
# TABLES E.1.1–E.3.4  Module 5: Sweep Analysis
# ─────────────────────────────────────────────────────────────────────────────

SYSTEMS_ORD_M5 = ["symmetric_wdt", "stock_wealth", "income", "cgt", "consumption"]
SYS_SWEEP_LABEL = {
    "symmetric_wdt" : "Symmetric WDT",
    "stock_wealth"  : "Stock Wealth Tax",
    "income"        : "Income Tax",
    "cgt"           : "CGT",
    "consumption"   : "Consumption Tax",
}


def table_e1(sweep_a_results: dict) -> str:
    """
    E.1.1: CEW by system and revenue target (E[T] as % of W₀).
    Rows grouped by distribution (A/B), then system.
    Columns: one per target percentage.  γ = 2 (central case).
    sweep_a_results: {target_pct: {dist_key: {gamma: {system: cew}}}
    """
    gamma       = 2.0
    target_pcts = sorted(sweep_a_results.keys())
    headers     = ['Distribution', 'System'] + [f'E[T]={p:.0f}%' for p in target_pcts]
    col_fmt     = [LEFT, LEFT] + [RIGHT] * len(target_pcts)
    rows        = []

    for dlabel, dist_name in [('A', 'Ver. A'), ('B', 'Ver. B')]:
        for name in SYSTEMS_ORD_M5:
            row = [dist_name, SYS_SWEEP_LABEL[name]]
            for pct in target_pcts:
                v = sweep_a_results[pct][dlabel][gamma].get(name)
                row.append(fmt_pct4(v))
            rows.append(row)
        rows.append([''] * len(headers))  # blank separator row between distributions

    return md_table(headers, rows[:-1], col_fmt=col_fmt)  # drop trailing blank


def table_e2a(sweep_b_full: dict) -> str:
    """
    E.2.1: Summary statistics (min/median/mean/max CEW) across all start years.
    Plus: fraction of windows where Symmetric WDT ranks first.
    sweep_b_full: {start_year: {system: cew | None}}
    """
    all_years = sorted(sweep_b_full.keys())
    headers   = ['System', 'Min CEW', 'Median CEW', 'Mean CEW', 'Max CEW',
                 'WDT best? (% of windows)']
    col_fmt   = [LEFT, RIGHT, RIGHT, RIGHT, RIGHT, RIGHT]
    rows      = []

    # Count windows where WDT is best
    wdt_best_count = 0
    for yr in all_years:
        yr_res = sweep_b_full[yr]
        valid  = {n: yr_res[n] for n in SYSTEMS_ORD_M5 if yr_res.get(n) is not None}
        if valid and max(valid, key=valid.get) == 'symmetric_wdt':
            wdt_best_count += 1
    wdt_best_pct = wdt_best_count / len(all_years) * 100 if all_years else 0

    for name in SYSTEMS_ORD_M5:
        vals = [sweep_b_full[yr].get(name) for yr in all_years
                if sweep_b_full[yr].get(name) is not None]
        if not vals:
            rows.append([SYS_SWEEP_LABEL[name]] + ['—'] * 5)
            continue
        rows.append([
            SYS_SWEEP_LABEL[name],
            fmt_pct4(min(vals)),
            fmt_pct4(float(np.median(vals))),
            fmt_pct4(float(np.mean(vals))),
            fmt_pct4(max(vals)),
            f'{wdt_best_pct:.1f}%' if name == 'symmetric_wdt' else '—',
        ])
    return md_table(headers, rows, col_fmt=col_fmt)


def table_e2b(sweep_b_full: dict, curated_years: list) -> str:
    """
    E.2.2: Curated worst-case start years.
    Rows: start years (including canonical 2000).
    Extra column: WDT advantage vs stock wealth tax in bp.
    """
    all_display = sorted(set(curated_years) | {2000})
    headers = (
        ['Start year']
        + [SYS_SWEEP_LABEL[n] for n in SYSTEMS_ORD_M5]
        + ['WDT adv. vs Stock (bp)']
    )
    col_fmt = [LEFT] + [RIGHT] * (len(SYSTEMS_ORD_M5) + 1)
    rows    = []

    for yr in all_display:
        if yr not in sweep_b_full:
            continue
        yr_res = sweep_b_full[yr]
        wdt_c  = yr_res.get('symmetric_wdt')
        sw_c   = yr_res.get('stock_wealth')
        adv    = ((wdt_c - sw_c) * 10000) if (wdt_c is not None and sw_c is not None) else None
        row = [str(yr) + (' ◄ canonical' if yr == 2000 else '')]
        for name in SYSTEMS_ORD_M5:
            row.append(fmt_pct4(yr_res.get(name)))
        row.append(f'{adv:+.1f}' if adv is not None else '—')
        rows.append(row)

    return md_table(headers, rows, col_fmt=col_fmt)


def table_e3(all_param_results: dict, param_configs: list, W0_vals: list) -> dict:
    """
    E.3.1–E.3.4: One table per parameter.
    Returns {param_name: md_table_str}.
    all_param_results: {param_name: {W0: {param_val: gap_bp}}}
    param_configs: list of (param_name, param_vals, param_label)
    W0_vals: list of W₀ levels used in the sweep
    """
    tables = {}
    for param_name, param_vals, param_label in param_configs:
        if param_name not in all_param_results:
            continue
        headers = [param_label] + [f'W₀=£{W0:.0f}m' for W0 in W0_vals]
        col_fmt = [LEFT] + [RIGHT] * len(W0_vals)
        rows    = []
        for pval in param_vals:
            row = [f'{pval}']
            for W0 in W0_vals:
                gap = all_param_results[param_name][W0].get(pval)
                row.append(f'{gap:+.2f}' if gap is not None else '—')
            rows.append(row)
        tables[param_name] = md_table(headers, rows, col_fmt=col_fmt)
    return tables


# ─────────────────────────────────────────────────────────────────────────────
# MASTER DOCUMENT ASSEMBLY
# ─────────────────────────────────────────────────────────────────────────────

def build_appendix(
    all_results        : dict,
    dists              : dict,
    c1_results         : dict,
    c2_lev_results     : list,
    c3_results         : list,
    W0_vals_c3         : list,
    sens_gain          : list,
    sens_T             : list,
    comp_A             : dict,
    comp_B             : dict,
    tier_results       : dict,
    paths              : dict,
    conc_years         : list,
    envelope           : dict,
    tiers              : list,
    p                  : dict,
    corner_results     : dict = None,   # Module 4 Part F off-diagonal spot check
    # Module 5 sweep results (optional — omit to skip Module 5 section)
    sweep_a_results    : dict = None,
    sweep_b_full       : dict = None,
    sweep_b_curated    : list = None,
    sweep_c_results    : dict = None,
    sweep_c_configs    : list = None,
    sweep_c_W0_vals    : list = None,
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
    doc.h2('A. Baseline Single-Agent Comparison')
    doc.blank()

    doc.h3('A.1 — Consumption-Equivalent Welfare (CEW) by system, γ, and distribution')
    doc.note(
        'CEW = proportional consumption change under no-tax making agent indifferent '
        'to the taxed system. Negative = welfare cost relative to no-tax. '
        'Ver. A = UK historical equity (73 obs, 1947–2019). '
        'Ver. B = idealised two-state (p=0.5, R_good=E[R]+σ, R_bad=E[R]−σ).'
    )
    doc.add_block(table_a1(all_results))
    doc.note(
        'Note: Income Tax and CGT show identical CEW and identical revenue-equivalent '
        'rates throughout this table. This is correct by construction: A. Module 1 '
        'models CGT as a gains-only tax with the same base as income tax and no '
        'realisation decision. The two systems are structurally identical in a '
        'single-period model where all gains are realised each period. '
        'The lock-in distortion that separates CGT from income tax in practice '
        'is endogenous and enters only in C. Module 3, where it generates the '
        'largest welfare difference in the model.'
    )

    doc.h3('A.2 — Variance of Consumption by system (γ=2)')
    doc.note(
        'Variance of consumption across return states at revenue-equivalent rates. '
        'Lower variance indicates greater risk-sharing. '
        'D-M prediction: Var(C_sym) = (1−τ)² × Var(C_notax).'
    )
    doc.add_block(table_a2(all_results))
    doc.blank()

    doc.h3('A.3 — Revenue-Equivalent Tax Rates (γ=2)')
    doc.note(
        'Rate τ* such that E[T(W₀, dist, τ*)] = target. '
        'Rates differ across systems because tax bases differ. '
        'Stock wealth and consumption taxes require low rates (broad base); '
        'income tax and CGT require higher rates (gains only, no collection in loss states).'
    )
    doc.add_block(table_a3(all_results))
    doc.blank()

    doc.h3('A.4 — Domar–Musgrave Test: Symmetric WDT')
    doc.note(
        'Prediction: Var(C_tax) / Var(C_notax) = (1−τ)². '
        'Gap near zero confirms D-M holds for the flat-rate symmetric case. '
        'Progression breaks D-M — see B. Module 2.'
    )
    doc.add_block(table_a4(all_results, dists))
    doc.blank()
    doc.rule()

    # ── Module 2 ──────────────────────────────────────────────────────────────
    doc.blank()
    doc.h2('B. Progressive Rates and the Three D-M Complications')
    doc.blank()

    doc.h3('B.1 — Flat WDT vs Progressive WDT CEW')
    doc.note(
        'C1 complication: under a progressive rate, the government co-investment share '
        'varies with wealth level, breaking the flat D-M result. '
        'Gap (bp) = (CEW_flat − CEW_progressive) × 10,000. Positive = flat WDT better. '
        'W₀ = 5 × W_min = £10m for both distributions.'
    )
    doc.add_block(table_b1(c1_results))
    doc.blank()

    doc.h3('B.2 — Leverage Effect on WDT Tax Base and Welfare')
    doc.note(
        'C2 complication: when an agent holds gross assets A with outstanding debt D, '
        'net worth W = A − D and the WDT taxes the amplified (or dampened) net-worth '
        'delta rather than the underlying asset return. '
        'NW base = actual WDT base (ΔW = A×R − D − W₀); '
        'asset-return base = hypothetical alternative taxing only A×(R−1). '
        'The two bases are identical at zero leverage and diverge as D/A rises. '
        'Gap (bp) = (CEW_NW − CEW_AR) × 10,000; positive means WDT\'s NW base '
        'produces higher welfare than the asset-return alternative at the same rate. '
        'Gross assets = £10m (5×W_min). Progressive rate function. γ=2. Version A distribution.'
    )
    doc.add_block(table_b2(c2_lev_results))
    doc.blank()

    doc.h3('B.3 — Two-Period Rate Asymmetry by Initial Wealth')
    doc.note(
        'Sequence: +18.8% gain (μ+σ) in period 1, −8.3% loss (σ) in period 2. '
        'τ gain = effective rate on period-1 delta at (W₀, W₁). '
        'τ refund = effective rate on period-2 loss at (W₁, W₂). '
        'Asymmetry = τ gain − τ refund (pp); positive means gain taxed at higher rate. '
        'Excess = net tax progressive − net tax flat; positive = progression costs more.'
    )
    doc.add_block(table_b3(c3_results, W0_vals_c3))
    doc.blank()

    doc.rule()

    # ── Module 3 ──────────────────────────────────────────────────────────────
    doc.blank()
    doc.h2('C. CGT Lock-In Distortion')
    doc.blank()
    doc.add(
        'Reference parameters: V=£10m, G/V=50%, r_A=10.45% (empirical equity mean), '
        'τ_cgt=24% (UK 2024 higher rate), T=5 years remaining.'
    )
    doc.blank()

    doc.h3('C.1 — Lock-In Welfare Cost by Embedded Gain Ratio')
    doc.note(
        'Lock-in cost (bp) = (CEW_free − CEW_locked) × 10,000. '
        'CEW_free: agent switches whenever r_B > r_A (no lock-in). '
        'CEW_locked: agent locked in under CGT when r_B < indifference return r_B*. '
        'P(locked in) includes two components: states where r_B < r_A '
        '(agent stays regardless of CGT — fundamental preference, not a distortion) '
        'and states where r_A ≤ r_B < r_B* (CGT lock-in distortion proper — '
        'agent would switch without CGT but switching cost exceeds benefit). '
        'The welfare cost is attributable to the second component only; '
        'the first component is present with or without CGT. '
        'Version A distribution. γ=2.'
    )
    doc.add_block(table_c1(sens_gain))
    doc.blank()

    doc.h3('C.2 — Lock-In Welfare Cost by Remaining Holding Period')
    doc.note(
        'G/V=50% fixed. T varies from 1 to 20 years. '
        'Lock-in cost rises from T=1 and plateaus at longer horizons — '
        'the direction is upward, not downward. '
        'At T=1 the agent has only one period to benefit from switching to B, '
        'so the opportunity cost of lock-in is low. '
        'Each additional year that Asset B compounds ahead of Asset A raises '
        'the foregone return from remaining locked in. '
        'The plateau appears as r_B* converges toward r_A and the trapped zone '
        '(r_A ≤ r_B < r_B*) collapses — states that triggered lock-in at short T '
        'now fall below r_A (agent stays regardless) or above r_B* (agent switches). '
        'Indifference return r_B* does converge to r_A as T→∞, '
        'confirming lock-in eventually disappears at infinite horizons; '
        'but across all empirically relevant horizons (T ≤ 20 yr) '
        'the welfare cost is substantially above the T=1 baseline.'
    )
    doc.add_block(table_c2(sens_T))
    doc.blank()

    doc.h3('C.3 — Full Welfare Comparison: WDT vs CGT (with and without lock-in)')
    doc.note(
        'A. Module 1 showed WDT ≈ CGT when lock-in was absent. '
        'This table adds the lock-in cost to CGT, correcting that comparison. '
        'WDT advantage (with lock-in) = CEW_WDT − CEW_CGT_locked.'
    )
    doc.add_block(table_c3(comp_A, comp_B))
    doc.blank()
    doc.rule()

    # ── Module 4 ──────────────────────────────────────────────────────────────
    doc.blank()
    doc.h2('D. Heterogeneous Agents — Incidence and Concentration')
    doc.blank()
    doc.add(
        'Tier differentials from Fagereng et al. (2020): Poor −4.55pp, Ok −2.05pp, '
        'Good +0.95pp, Great +3.45pp relative to UK historical equity mean (10.45%). '
        'Version A distribution with tier-shifted returns. γ=2.'
    )
    doc.blank()

    doc.h3('D.1 — CEW by Tier and Tax System')
    doc.note(
        'Progressive WDT uses logistic rate function from TOML '
        '(τ₀=15%, τ_m=70%, k=0.001, W_min=£2m). '
        'All flat-rate systems revenue-equivalent at 2% of Good-tier W₀.'
    )
    doc.add_block(table_d1(tier_results))
    doc.blank()

    doc.h3('D.2 — Distributional Incidence: Expected Tax as % of W₀')
    doc.note(
        'E[T] / W₀ × 100. All systems calibrated to the same revenue target. '
        'Rates differ across tiers because shifted return distributions change E[T]. '
        'Progressive WDT incidence not shown here — see Table D.1 CEW column.'
    )
    doc.add_block(table_d2(tier_results))
    doc.blank()

    doc.h3('D.3 — Wealth Concentration Path: Great/Poor Ratio at Key Years')
    doc.note(
        'Great-tier wealth / Poor-tier wealth at selected years. '
        'All systems calibrated at the population-weighted aggregate tau from '
        'Table D.1 (same rate as Parts B/C welfare comparison). '
        'Progressive WDT uses the logistic rate function directly. '
        'Initial ratio reflects W₀ difference only (150 / 3 = 50×). '
        f'Return heterogeneity compounds over {p["tcm"].get("canonical_N", 30)}-year scenario horizon '
        f'starting {p["tcm"].get("scenario_start_year", "—")}.'
    )
    doc.add_block(table_d3(paths, tiers, conc_years))
    doc.blank()

    doc.h3('D.4 — Lifetime Contribution Envelope: Binding Summary')
    scenario_start = p["tcm"].get("scenario_start_year", p["returns"]["series_base_year"])
    doc.note(
        'Envelope binds when cumulative refunds would exceed cumulative taxes paid. '
        'Refund capped at cumulative taxes paid to date when binding occurs. '
        'Min slack = minimum of (cum. tax − cum. refund) over the scenario window; '
        'zero means the envelope was exactly hit but not exceeded. '
        'The Poor tier binding in the first year of the scenario ('
        + str(scenario_start) + ') is the concrete numerical realisation of the '
        'ENV paper\'s SRR early-year funding gap: the Poor tier\'s '
        '−4.55pp return differential produces a loss in the first scenario year '
        'before any cumulative tax has been paid, so the refund that would be '
        'owed exceeds the cumulative contribution to date. '
        'The envelope floor binds and the refund is capped at zero. '
        'Policy implication: the SRR must be pre-funded from sources other than '
        'WDT receipts (e.g. initial government capitalisation) to honour refunds '
        'in early years for low-return-tier entrants, or the entry-year assessment '
        'must provide an initial credit against future taxes. '
        'This result holds for the ' + str(scenario_start) + '-start sequence; '
        'it may differ under other start years — see E. Module 5 Sweep B for '
        'the full start-year distribution.'
    )
    doc.add_block(table_d4(envelope, tiers))
    doc.blank()

    if corner_results is not None:
        doc.h3('D.5 — Off-Diagonal Spot Check: Decoupling W₀ from Return Differential')
        doc.note(
            'Corner A: Great return differential (+3.45pp) applied at Poor-tier W₀ (£2.86m). '
            'Corner B: Poor return differential (−4.55pp) applied at Great-tier W₀ (£139.6m). '
            'These are the two extreme off-diagonal cells of the 4-tier × 4-bracket grid — '
            'enough to bound the interaction without computing all 16 combinations. '
            'Diagonal (same W₀) = the standard Part B result for the tier sharing this corner\'s '
            'wealth level. Diagonal (same diff) = the standard Part B result for the tier '
            'sharing this corner\'s return differential. '
            'Δ vs same-W₀ (bp) = (Corner CEW − Diagonal same-W₀ CEW) × 10,000: '
            'positive means decoupling the differential upward improves welfare; '
            'negative means the lower return differential of the diagonal tier was welfare-reducing. '
            'Revenue target = 2% of each corner\'s own W₀ (per-corner solve, not aggregate). '
            'γ=2. Version A distribution.'
        )
        doc.add_block(table_d5(corner_results, tier_results))
        doc.blank()

    doc.rule()

    # ── Module 5 (optional — included only when sweep results are supplied) ────
    if sweep_a_results is not None:
        doc.blank()
        doc.h2('E. Welfare Sweep Analysis')
        doc.blank()
        doc.add(
            'Three independent sweep axes: (A) revenue target 1–5% of W₀; '
            '(B) start-year worst-case over all 73 historical 30-year windows; '
            '(C) progressive-vs-flat WDT welfare gap across rate parameters. '
            'All at γ=2 (central case) unless noted.'
        )
        doc.blank()

        doc.h3('E.1 — Sweep A: CEW by System and Revenue Target (γ=2)')
        doc.note(
            'E[T] as % of W₀ swept from 1% to 5%. '
            'Columns = revenue target; rows grouped by distribution. '
            'Rankings that hold across the full range are structurally robust; '
            'rankings that flip signal revenue-sensitivity. γ=2. W₀=1.0 (normalised).'
        )
        doc.add_block(table_e1(sweep_a_results))
        doc.blank()

        if sweep_b_full is not None:
            doc.h3('E.2.1 — Sweep B: Summary Statistics Across All Start Years')
            doc.note(
                'Min/median/mean/max CEW across all 73 start-year windows (1947–2019). '
                'WDT best? = fraction of windows where Symmetric WDT has the highest CEW '
                '(lowest welfare cost) of the five systems. '
                'E[T] = 2% of W₀. γ=2. Version A distribution.'
            )
            doc.add_block(table_e2a(sweep_b_full))
            doc.blank()

            curated = sweep_b_curated if sweep_b_curated is not None else []
            doc.h3('E.2.2 — Sweep B: Curated Worst-Case Start Years')
            doc.note(
                'Six historically adverse start years plus the canonical 2000 (◄). '
                'Adverse years: 1946 (post-war austerity), 1972 (oil shock), '
                '1987 (Black Monday), 1999 (GFC in window), 2000 (dot-com + GFC), '
                '2006 (worst LRR fill speed). '
                'WDT adv. = (CEW_WDT − CEW_StockWealth) × 10,000 in basis points.'
            )
            doc.add_block(table_e2b(sweep_b_full, curated))
            doc.blank()

        if sweep_c_results is not None and sweep_c_configs is not None:
            s3_tables = table_e3(sweep_c_results, sweep_c_configs,
                                      sweep_c_W0_vals or [10.0, 30.0, 100.0])
            param_display = {
                'tau_0': ('E.3.1 — Sweep C: τ₀ Sensitivity',
                          'Gap (bp) = (CEW_flat − CEW_progressive) × 10,000. '
                          'Positive = flat WDT has lower welfare cost. '
                          'τ_m, k, W_min at canonical values.'),
                'tau_m': ('E.3.2 — Sweep C: τ_m Sensitivity',
                          'τ₀, k, W_min at canonical values.'),
                'k':     ('E.3.3 — Sweep C: k Sensitivity',
                          'τ₀, τ_m, W_min at canonical values.'),
                'W_min': ('E.3.4 — Sweep C: W_min Sensitivity',
                          'τ₀, τ_m, k at canonical values.'),
            }
            for param_name, tbl_str in s3_tables.items():
                if param_name in param_display:
                    title, note_text = param_display[param_name]
                    doc.h3(title)
                    doc.note(note_text)
                    doc.add_block(tbl_str)
                    doc.blank()

        doc.rule()

    doc.blank()
    doc.h2('Parameter Reference')
    doc.blank()
    doc.add('| Parameter | Value | Source |')
    doc.add('|:---|---:|:---|')
    rp = p['rate']
    doc.add(f'| W₀ (normalised A. Module 1) | {W0_BASE:.1f} | — |')
    doc.add(f'| Revenue target E[T] | {fmt_pct0(TARGET_ET)} of W₀ | — |')
    doc.add(f'| γ (central case) | 2.0 | Flavin & Yamashita (2002) |')
    doc.add(f'| τ₀ (WDT entry rate) | {fmt_pct0(rp["tau_0"])} | TOML [rate] |')
    doc.add(f'| τ_m (WDT ceiling) | {fmt_pct0(rp["tau_m"])} | TOML [rate] |')
    doc.add(f'| k (logistic steepness) | {rp["k"]} | TOML [rate] |')
    doc.add(f'| W_min (£m) | {fmt_gbp_m(rp["W_min"], dp=0)} | TOML [rate] |')
    doc.add(f'| UK equity mean (1947–2019) | {fmt_pct(p["tcm"]["hist_mean"])} | JST dataset |')
    doc.add(f'| UK equity std dev | {fmt_pct(float(np.std(p["returns"]["array"])))} | JST dataset |')
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
    N      = p['tcm']['canonical_N']   # 30 — matches all module scripts
    dist_A = make_empirical_distribution_scenario(p, N)
    dist_B = make_idealised_distribution_scenario(p, N)
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

    W0_vals_c3 = [rp['W_min'] * m for m in [1.5, 2, 5, 10, 20, 50, 100]]
    c3_results = [
        run_c3_two_period(W0, R1_good, R2_loss, rate_fn, 2.0, tau_flat)
        for W0 in W0_vals_c3
    ]

    # C2: leverage sweep — matches module2 Part C setup exactly
    gross_assets_c2  = rp['W_min'] * 5          # £10m gross assets
    leverage_grid_c2 = np.linspace(0.0, 0.70, 15)
    c2_lev_results   = [
        run_c2_leverage(
            LeveragedAgent(gross_assets=gross_assets_c2,
                           debt=gross_assets_c2 * lev),
            dist_A, rate_fn, gamma=2.0,
        )
        for lev in leverage_grid_c2
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

    # Part F: off-diagonal spot check (uses same dist_A and rate_fn as Parts B–E)
    dist_A_m4    = make_empirical_distribution_scenario(p, p['tcm']['canonical_N'])
    corner_results = run_corner_check(tiers, dist_A_m4, 2.0, rate_fn)

    # ── Module 5 results ──────────────────────────────────────────────────────
    print('--- Running Module 5 sweeps (this may take a few minutes) ---')

    # Sweep A: revenue target
    sweep_a_results, _sweep_dists = run_sweep_a(p)

    # Sweep B: start year
    sweep_b_full, _sweep_b_curated = run_sweep_b(p)
    sweep_b_curated_years = p['sweep'].get('wfr_start_years_curated', [])

    # Sweep C: rate parameter sensitivity
    N_m5          = p['tcm']['canonical_N']
    dist_A_m5     = make_empirical_distribution_scenario(p, N_m5)
    sw            = p['sweep']
    sweep_c_W0    = [10.0, 30.0, 100.0]
    sweep_c_cfgs  = [
        ('tau_0', sw['wfr_tau_0_sweep'], 'τ₀ (entry rate)'),
        ('tau_m', sw['wfr_tau_m_sweep'], 'τ_m (ceiling rate)'),
        ('k',     sw['wfr_k_sweep'],     'k (steepness per £m)'),
        ('W_min', sw['wfr_wmin_sweep'],  'W_min (£m)'),
    ]
    sweep_c_results = {}
    for param_name, param_vals, param_label in sweep_c_cfgs:
        print(f'  Sweep C: {param_name} ({len(param_vals)} values)')
        sweep_c_results[param_name] = run_sweep_c_param(
            p, param_name, param_vals, sweep_c_W0,
            dist_A_m5, 2.0, 0.02
        )

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
        corner_results=corner_results,
        sweep_a_results=sweep_a_results,
        sweep_b_full=sweep_b_full,
        sweep_b_curated=sweep_b_curated_years,
        sweep_c_results=sweep_c_results,
        sweep_c_configs=sweep_c_cfgs,
        sweep_c_W0_vals=sweep_c_W0,
    )

    out_path = OUTPUT_DIR / 'WFR_appendix_tables.md'
    doc.write(out_path)

    print(f'  Master document: {out_path}')


if __name__ == '__main__':
    main()