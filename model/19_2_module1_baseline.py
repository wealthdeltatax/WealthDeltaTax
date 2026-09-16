"""
module1_baseline.py
===================
Module 1: Baseline Single-Agent Welfare Comparison

Question: Under revenue equivalence, what is the welfare cost of each tax
system relative to a no-tax benchmark, across the empirical UK equity return
distribution (Version A) and the idealised two-state distribution (Version B)?

Outputs
-------
1.  Welfare table at γ = 1, 2, 4 for both distributions (stdout)
2.  CEW ranking chart across γ values (both distributions)
3.  Variance-of-consumption chart (both distributions)
4.  D-M test confirmation table
5.  Year-by-year tax burden chart (Version A only) — shows which years
    each system imposes a loss vs provides a refund
6.  Summary of key findings (stdout)

All outputs written to outputs/module1/
"""

import os
import math
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
from pathlib import Path

from wdt_fmt import fmt_pct, fmt_pct0
from wdt_style import (
    apply_style, save_fig,
    FIG_PAIR, FIG_WIDE_L, FIG_QUAD,
    DPI_SCREEN,
)

from welfare_core import (
    load_params,
    make_empirical_distribution,
    make_idealised_distribution,
    run_welfare_comparison,
    print_welfare_table,
    dm_test,
    expected_tax,
    variance_of_consumption,
    get_tax_fn,
    SYSTEM_LABELS,
    tax_symmetric_flat,
    make_empirical_distribution_scenario,
    make_idealised_distribution_scenario,
    module_output_dir, 
    TOML_PATH
)

# ─────────────────────────────────────────────────────────────────────────────
# CONFIG
# ─────────────────────────────────────────────────────────────────────────────

OUTPUT_DIR = module_output_dir("module1")

W0          = 1.0          # normalised initial wealth
TARGET_ET   = 0.02         # 2% of W0 — consistent with toy model experiments
GAMMA_VALS  = [1.0, 2.0, 4.0]

# Ordered for consistent display
SYSTEMS_ORDERED = ["symmetric_wdt", "stock_wealth", "income", "cgt", "consumption"]

# Colours — consistent across all Module 1 charts
COLOURS = {
    "symmetric_wdt" : "#1a6fad",   # WDT: strong blue
    "stock_wealth"  : "#c0392b",   # stock wealth: red
    "income"        : "#e67e22",   # income tax: orange
    "cgt"           : "#f1c40f",   # CGT: yellow
    "consumption"   : "#7f8c8d",   # consumption: grey
}
MARKERS = {
    "symmetric_wdt" : "o",
    "stock_wealth"  : "s",
    "income"        : "^",
    "cgt"           : "D",
    "consumption"   : "P",
}

# ─────────────────────────────────────────────────────────────────────────────
# CHART HELPERS
# ─────────────────────────────────────────────────────────────────────────────

def _save(fig, name: str):
    # DPI_SCREEN (150) is intentional for WFR preview outputs.
    # Use save_fig(fig, path) directly (default DPI_PRINT=300) for publication.
    save_fig(fig, OUTPUT_DIR / name, dpi=DPI_SCREEN)


def _style_ax(ax, title: str, xlabel: str = "", ylabel: str = ""):
    ax.set_title(title, fontsize=11, fontweight="bold", pad=8)
    ax.set_xlabel(xlabel, fontsize=9)
    ax.set_ylabel(ylabel, fontsize=9)
    ax.tick_params(labelsize=8)
    ax.grid(axis="y", linestyle="--", alpha=0.4)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)


# ─────────────────────────────────────────────────────────────────────────────
# CHART 3.1a: CEW across γ — one panel per distribution
# ─────────────────────────────────────────────────────────────────────────────

def fig_3_1a_cew_by_gamma(all_results: dict):
    """
    all_results: {dist_label: {gamma: {system: SystemResult}}}
    """
    dist_labels = list(all_results.keys())
    n_panels = len(dist_labels)

    apply_style()
    fig, axes = plt.subplots(1, n_panels, figsize=FIG_PAIR, sharey=True)
    if n_panels == 1:
        axes = [axes]

    fig.suptitle(
        "Fig 3.1a — CEW vs No-Tax Benchmark — by Risk Aversion (γ)\n"
        f"Revenue target E[T] = {fmt_pct0(TARGET_ET)} of W₀",
        fontsize=12, fontweight="bold"
    )

    for ax, dist_label in zip(axes, dist_labels):
        for name in SYSTEMS_ORDERED:
            cews = []
            for g in GAMMA_VALS:
                r = all_results[dist_label][g].get(name)
                cews.append(r.cew * 100 if r and r.cew is not None else np.nan)

            ax.plot(
                GAMMA_VALS, cews,
                color=COLOURS[name], marker=MARKERS[name],
                linewidth=2, markersize=7,
                label=SYSTEM_LABELS[name]
            )

        ax.axhline(0, color="black", linewidth=0.8, linestyle="--", alpha=0.5)
        ax.yaxis.set_major_formatter(mtick.PercentFormatter(decimals=2))
        _style_ax(ax, dist_label[:55], xlabel="γ (risk aversion)", ylabel="CEW (%)")
        ax.set_xticks(GAMMA_VALS)

    axes[-1].legend(fontsize=8, loc="lower right")
    fig.tight_layout()
    _save(fig, "wfr_fig_3_1a_cew_by_gamma.png")


# ─────────────────────────────────────────────────────────────────────────────
# CHART 3.2: Variance of consumption — bar chart, both distributions
# ─────────────────────────────────────────────────────────────────────────────

def fig_3_2_variance(all_results: dict):
    """Bar chart of Var(consumption) at γ=2 for both distributions."""
    dist_labels = list(all_results.keys())
    gamma = 2.0

    apply_style()
    fig, axes = plt.subplots(1, len(dist_labels), figsize=FIG_PAIR, sharey=False)
    if len(dist_labels) == 1:
        axes = [axes]

    fig.suptitle(
        "Fig 3.2 — Variance of Consumption by Tax System\n"
        f"(γ = {gamma}, E[T] = {fmt_pct0(TARGET_ET)} of W₀)",
        fontsize=12, fontweight="bold"
    )

    for ax, dist_label in zip(axes, dist_labels):
        names  = SYSTEMS_ORDERED
        labels = [SYSTEM_LABELS[n].replace(" (", "\n(").replace(" Tax", "\nTax") for n in names]
        vars_  = []
        for name in names:
            r = all_results[dist_label][gamma].get(name)
            vars_.append(r.var_consumption if r and r.var_consumption is not None else np.nan)

        bars = ax.bar(labels, vars_,
                      color=[COLOURS[n] for n in names],
                      edgecolor="white", linewidth=0.8, alpha=0.85)

        # No-tax variance as a horizontal reference line
        notax_var = variance_of_consumption(W0, _dists[dist_label], tax_symmetric_flat, 0.0)
        ax.axhline(notax_var, color="black", linestyle="--", linewidth=1.2,
                   label=f"No-tax variance ({notax_var:.4f})")

        # Value labels on bars
        for bar, v in zip(bars, vars_):
            if not np.isnan(v):
                ax.text(bar.get_x() + bar.get_width() / 2, v + notax_var * 0.01,
                        f"{v:.4f}", ha="center", va="bottom", fontsize=7.5)

        ax.legend(fontsize=8)
        _style_ax(ax, dist_label[:55], ylabel="Var(consumption)")

    fig.tight_layout()
    _save(fig, "wfr_fig_3_2_variance.png")


# ─────────────────────────────────────────────────────────────────────────────
# CHART 3.1c: Year-by-year tax burden (Version A only)
# ─────────────────────────────────────────────────────────────────────────────

def fig_3_1c_annual_tax(dist_A, results_A_gamma2: dict, scenario_years: list):
    """
    For Version A at γ=2, show the annual tax/refund for each year in the
    scenario window for the three most distinct systems: symmetric WDT,
    stock wealth tax, and income tax.

    years and R_vals are derived from the distribution and scenario_years,
    not hardcoded — so this works for any N-year scenario window.
    """
    years  = scenario_years                     # length N, matches dist_A
    R_vals = dist_A.returns                     # length N gross returns
    N      = len(years)

    neg_year_note = ", ".join(
        str(years[i]) for i in range(N) if R_vals[i] < 1.0
    ) or "none in this window"

    systems_to_show = ["symmetric_wdt", "stock_wealth", "income"]

    apply_style()
    fig, axes = plt.subplots(3, 1, figsize=FIG_QUAD, sharex=True)
    fig.suptitle(
        f"Fig 3.1c — Annual Tax Paid (+) / Refund Received (−) per £1 of W₀\n"
        f"Version A — UK Equity {years[0]}–{years[-1]} ({N} obs, scenario)",
        fontsize=12, fontweight="bold"
    )

    for ax, name in zip(axes, systems_to_show):
        r      = results_A_gamma2[name]
        taxes  = r.state_taxes if r.state_taxes is not None else np.zeros(N)
        colors = ["#c0392b" if t < 0 else COLOURS[name] for t in taxes]

        ax.bar(years, taxes, color=colors, width=0.8, alpha=0.85)
        ax.axhline(0, color="black", linewidth=0.8)

        # Mark negative return years within the scenario window
        neg_years = [years[i] for i in range(N) if R_vals[i] < 1.0]
        for ny in neg_years:
            ax.axvline(ny, color="grey", linestyle=":", linewidth=0.8, alpha=0.6)

        ax.set_ylabel(f"{SYSTEM_LABELS[name]}\ntax paid (£)", fontsize=8)
        ax.tick_params(labelsize=7)
        ax.grid(axis="y", linestyle="--", alpha=0.3)
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)

    axes[-1].set_xlabel("Year", fontsize=9)
    fig.text(0.01, 0.5, f"Dotted lines = negative return years: {neg_year_note}",
             va="center", rotation="vertical", fontsize=7, color="grey")
    fig.tight_layout(rect=[0.02, 0, 1, 1])
    _save(fig, "wfr_fig_3_1c_annual_tax.png")


# ─────────────────────────────────────────────────────────────────────────────
# CHART 3.1b: CEW gap — WDT advantage over each competitor
# ─────────────────────────────────────────────────────────────────────────────

def fig_3_1b_wdt_advantage(all_results: dict):
    """
    Shows (CEW_WDT − CEW_competitor) in basis points for each competitor,
    across γ and both distributions. A positive value means WDT has lower
    welfare cost (better welfare).
    """
    dist_labels = list(all_results.keys())
    competitors = ["stock_wealth", "income", "cgt", "consumption"]

    apply_style()
    fig, axes = plt.subplots(1, len(dist_labels), figsize=FIG_PAIR, sharey=True)
    if len(dist_labels) == 1:
        axes = [axes]

    fig.suptitle(
        "Fig 3.1b — WDT Welfare Advantage over Competitors\n"
        "(CEW_WDT − CEW_competitor, in basis points; positive = WDT better)",
        fontsize=12, fontweight="bold"
    )

    for ax, dist_label in zip(axes, dist_labels):
        for comp in competitors:
            gaps = []
            for g in GAMMA_VALS:
                res   = all_results[dist_label][g]
                wdt_r = res.get("symmetric_wdt")
                cmp_r = res.get(comp)
                if wdt_r and cmp_r and wdt_r.cew is not None and cmp_r.cew is not None:
                    gap_bp = (wdt_r.cew - cmp_r.cew) * 10000  # in basis points
                    gaps.append(gap_bp)
                else:
                    gaps.append(np.nan)

            ax.plot(
                GAMMA_VALS, gaps,
                color=COLOURS[comp], marker=MARKERS[comp],
                linewidth=2, markersize=7,
                label=SYSTEM_LABELS[comp]
            )

        ax.axhline(0, color="black", linewidth=0.8, linestyle="--", alpha=0.6)
        ax.yaxis.set_major_formatter(mtick.FormatStrFormatter("%.1f bp"))
        _style_ax(
            ax, dist_label[:55],
            xlabel="γ (risk aversion)",
            ylabel="WDT advantage (basis points)"
        )
        ax.set_xticks(GAMMA_VALS)

    axes[-1].legend(fontsize=8, loc="upper left")
    fig.tight_layout()
    _save(fig, "wfr_fig_3_1b_wdt_advantage.png")


# ─────────────────────────────────────────────────────────────────────────────
# D-M TEST TABLE
# ─────────────────────────────────────────────────────────────────────────────

def print_dm_table(all_results: dict):
    """Print D-M test results for all (distribution, γ) combinations."""
    print("\n" + "=" * 70)
    print("DOMAR-MUSGRAVE TEST: Symmetric WDT (flat rate)")
    print("Prediction: Var(C_tax) / Var(C_notax) = (1 − τ)²")
    print("=" * 70)
    print(f"{'Distribution':40s} {'γ':>4} {'τ':>8} {'(1-τ)²':>10} {'Actual':>10} {'Gap':>10} {'Result':>8}")
    print("-" * 70)

    for dist_label, gamma_results in all_results.items():
        for g, sys_results in gamma_results.items():
            wdt_r = sys_results.get("symmetric_wdt")
            if wdt_r is None or wdt_r.tau is None:
                continue
            dm = dm_test(W0, _dists[dist_label], wdt_r.tau)
            status = "✓ HOLDS" if dm["dm_holds"] else "✗ FAILS"
            print(
                f"{dist_label[:40]:40s} {g:>4.1f} "
                f"{wdt_r.tau*100:>7.3f}% "
                f"{dm['predicted_ratio']:>10.6f} "
                f"{dm['actual_ratio']:>10.6f} "
                f"{dm['gap']:>10.2e} "
                f"{status:>8}"
            )
    print()

# ─────────────────────────────────────────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────────────────────────────────────────

# Global dict so chart helpers can access distributions by label
_dists = {}

def main():
    global _dists

    print("=" * 70)
    print("MODULE 1: Baseline Single-Agent Welfare Comparison")
    print("=" * 70)

    p   = load_params(TOML_PATH)
    N   = p["tcm"]["canonical_N"] 
    dist_A = make_empirical_distribution_scenario(p, N)
    dist_B = make_idealised_distribution_scenario(p, N)

    _dists[dist_A.label] = dist_A
    _dists[dist_B.label] = dist_B

    distributions = [dist_A, dist_B]

    # Run welfare comparison for all (dist, gamma) combinations
    # Structure: {dist_label: {gamma: {system_name: SystemResult}}}
    all_results = {}

    for dist in distributions:
        all_results[dist.label] = {}
        print(f"\n{dist.describe()}\n")

        for gamma in GAMMA_VALS:
            results = run_welfare_comparison(
                W0=W0,
                dist=dist,
                gamma=gamma,
                target_et=TARGET_ET,
            )
            all_results[dist.label][gamma] = results
            print_welfare_table(results, dist.label, gamma, TARGET_ET, W0)

    # Charts
    print("\n--- Generating charts ---")
    fig_3_1a_cew_by_gamma(all_results)
    fig_3_2_variance(all_results)
    # Scenario years (length N) — consistent with dist_A, not the full 73-year series
    from welfare_core import make_scenario_sequence
    _, scenario_years = make_scenario_sequence(p, N)
    fig_3_1c_annual_tax(dist_A, all_results[dist_A.label][2.0], scenario_years)
    fig_3_1b_wdt_advantage(all_results)

    # D-M table
    print_dm_table(all_results)

    print(f"\n✓ Module 1 complete. Outputs in: {OUTPUT_DIR}")


if __name__ == "__main__":
    main()