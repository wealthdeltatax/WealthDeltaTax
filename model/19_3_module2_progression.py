"""
module2_progression.py
======================
Module 2: Progressive Rates and the Three D-M Complications

Question: Does the D-M risk-sharing result survive when the flat symmetric
rate is replaced with the WDT's actual progressive logistic rate structure?
And how large is the welfare cost of each of the three complications LR.A
identifies as unresolved?

The three complications (from LR.A §2.1):
  C1. Progressive rates: government co-investment share varies with W.
  C2. Net-worth base ≠ asset return: diverges under leverage.
  C3. Multi-period asymmetry: gain-year rate > loss-year refund rate
      when wealth falls between periods.

Structure
---------
Part B.1  — Progressive rate function (logistic, from TOML)
Part B.2  — Welfare cost of progression alone (single period)
Part B.3  — Leverage extension — how debt changes the effective base
Part B.4  — Two-period rate asymmetry — gain then loss
Part B.5  — Combined: all three complications together
Part B.6  — Comparison: progressive WDT vs flat WDT vs stock wealth tax

Outputs → model/OUTPUTS/WFR/module2/
"""

import os
import math
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
from pathlib import Path
from dataclasses import dataclass
from typing import Optional

from wdt_fmt import fmt_pct, fmt_pct0, fmt_pct4, fmt_gbp_m
from wdt_style import (
    apply_style, save_fig,
    FIG_SINGLE, FIG_PAIR, FIG_WIDE,
    DPI_SCREEN,
)

from welfare_core import (
    load_params,
    make_empirical_distribution,
    make_idealised_distribution,
    ReturnDistribution,
    crra_utility,
    expected_utility,
    expected_tax,
    consumption_equiv_welfare,
    variance_of_consumption,
    run_welfare_comparison,
    print_welfare_table,
    dm_test,
    tax_symmetric_flat,
    tax_stock_wealth,
    SYSTEM_LABELS,
    make_empirical_distribution_scenario,
    make_idealised_distribution_scenario,
    module_output_dir, 
    TOML_PATH,
    ProgressiveRateFunction,
    tax_progressive_wdt,
    expected_utility_progressive,
    expected_tax_progressive,
    variance_progressive,
    
)

OUTPUT_DIR = module_output_dir("module2")

# ─────────────────────────────────────────────────────────────────────────────
# CONFIG
# ─────────────────────────────────────────────────────────────────────────────

W0_BASE     = 1.0        # normalised wealth; scaled by bracket for progression
TARGET_ET   = 0.02       # 2% of W0 — matches Module 1
GAMMA_VALS  = [1.0, 2.0, 4.0]

COLOURS = {
    "flat_wdt"        : "#1a6fad",
    "progressive_wdt" : "#0d3d6b",
    "stock_wealth"    : "#c0392b",
    "c1_only"         : "#2ecc71",
    "c3_only"         : "#e74c3c",
    "c1_c3_combined"  : "#8e44ad",
}

# ─────────────────────────────────────────────────────────────────────────────
# PART B: C1 — Welfare cost of progression (single period)
# Compares flat-rate WDT vs progressive WDT at same expected revenue
# ─────────────────────────────────────────────────────────────────────────────

def run_c1_analysis(
    W0       : float,
    dist     : ReturnDistribution,
    rate_fn  : ProgressiveRateFunction,
    gamma    : float,
    target_et: float,
) -> dict:
    """
    C1: Progressive rates break the flat D-M result.

    Revenue-equivalence convention (corrected):
    The progressive WDT is applied at its canonical logistic schedule and
    its natural E[T] is computed first.  The flat WDT rate is then solved
    to match that same E[T], not the global 2%-of-W₀ target.  This ensures
    the CEW comparison is made at equal revenue — the only clean basis for
    a welfare comparison between structural alternatives.

    The global target (target_et) is retained in the return dict for
    reference so callers can see how much the progressive schedule deviates
    from the 2% benchmark, but it does NOT govern the flat calibration.

    Computes:
    1. Progressive WDT results at canonical rate function
    2. Flat WDT at revenue-equivalent rate = E[T]_progressive
    3. CEW for both and the welfare gap

    Returns dict of key metrics.
    """
    from welfare_core import solve_revenue_equivalent_rate, get_tax_fn

    flat_fn  = get_tax_fn("symmetric_wdt")
    eu_notax = expected_utility(W0, dist, flat_fn, 0.0, gamma)

    # Step 1: progressive WDT at canonical schedule
    et_prog  = expected_tax_progressive(W0, dist, rate_fn)
    eu_prog  = expected_utility_progressive(W0, dist, rate_fn, gamma)
    cew_prog = consumption_equiv_welfare(eu_prog, eu_notax, gamma)
    var_prog = variance_progressive(W0, dist, rate_fn)

    # Step 2: flat WDT revenue-matched to et_prog (NOT to target_et)
    # If et_prog <= 0 the flat solver cannot match it; fall back to target_et
    # with a flag so the caller knows the comparison is not clean.
    revenue_matched = True
    if et_prog > 0:
        flat_target = et_prog
    else:
        flat_target     = target_et
        revenue_matched = False

    tau_flat = solve_revenue_equivalent_rate(W0, dist, flat_fn, flat_target)
    eu_flat  = expected_utility(W0, dist, flat_fn, tau_flat, gamma)
    cew_flat = consumption_equiv_welfare(eu_flat, eu_notax, gamma)
    var_flat = variance_of_consumption(W0, dist, flat_fn, tau_flat)
    et_flat  = expected_tax(W0, dist, flat_fn, tau_flat)

    return {
        "tau_flat"         : tau_flat,
        "et_flat"          : et_flat,          # = et_prog when revenue_matched=True
        "et_flat_target"   : target_et,         # the 2%-of-W₀ benchmark (reference only)
        "eu_flat"          : eu_flat,
        "cew_flat"         : cew_flat,
        "var_flat"         : var_flat,
        "et_progressive"   : et_prog,
        "eu_progressive"   : eu_prog,
        "cew_progressive"  : cew_prog,
        "var_progressive"  : var_prog,
        "cew_gap_bp"       : (cew_flat - cew_prog) * 10000,  # flat better if positive
        "eu_notax"         : eu_notax,
        "revenue_matched"  : revenue_matched,   # False = comparison not clean; see note
    }


# ─────────────────────────────────────────────────────────────────────────────
# PART C: C2 — Leverage extension
# Net-worth base ≠ asset return when agent holds debt
# ─────────────────────────────────────────────────────────────────────────────

@dataclass
class LeveragedAgent:
    """
    Agent holds gross assets A with outstanding debt D.
    Net worth W = A - D.
    Return R applies to A, not W.
    Debt is fixed in nominal terms (no mark-to-market on debt).
    """
    gross_assets  : float   # A
    debt          : float   # D (positive = borrowed)

    @property
    def net_worth(self) -> float:
        return self.gross_assets - self.debt

    @property
    def leverage_ratio(self) -> float:
        return self.debt / self.gross_assets if self.gross_assets > 0 else 0.0

    def net_worth_after_return(self, R: float) -> float:
        """W₁ = A×R - D  (debt fixed nominally)."""
        return self.gross_assets * R - self.debt

    def asset_return(self, R: float) -> float:
        """Return on gross assets."""
        return R - 1.0

    def net_worth_return(self, R: float) -> float:
        """
        Return on net worth = ΔW / W₀.
        Differs from asset return when leverage > 0.
        """
        W0 = self.net_worth
        W1 = self.net_worth_after_return(R)
        return (W1 - W0) / W0 if W0 > 0 else 0.0


def run_c2_leverage(
    agent    : LeveragedAgent,
    dist     : ReturnDistribution,
    rate_fn  : ProgressiveRateFunction,
    gamma    : float,
) -> dict:
    """
    C2: Shows how leverage changes the effective WDT base and tax burden.

    Compares two tax bases:
      - Asset-return base: τ × A × (R - 1)   [as if WDT taxed asset returns]
      - Net-worth delta base: τ × ΔW          [actual WDT base]

    The difference is the leverage distortion: the WDT taxes the amplified
    (or dampened) net-worth change, not the underlying asset return.
    """
    W0 = agent.net_worth

    results_by_state = []
    for R, prob in zip(dist.returns, dist.probs):
        W1        = agent.net_worth_after_return(R)
        delta_W   = W1 - W0
        delta_A   = agent.gross_assets * (R - 1.0)

        # Tax under WDT (net-worth delta base)
        tau_eff   = rate_fn.effective_rate(W0, W1) if W1 > 0 else rate_fn.rate(max(W1, 0))
        tax_nw    = tau_eff * delta_W

        # Hypothetical tax if base were asset return
        tau_eff_a = rate_fn.effective_rate(agent.gross_assets, agent.gross_assets * R)
        tax_ar    = tau_eff_a * delta_A

        C_nw  = max(W1 - tax_nw, 1e-9)   # consumption under net-worth base
        C_ar  = max(W1 - tax_ar, 1e-9)   # consumption under asset-return base

        results_by_state.append({
            "R"        : R,
            "prob"     : prob,
            "W1"       : W1,
            "delta_W"  : delta_W,
            "delta_A"  : delta_A,
            "tax_nw"   : tax_nw,
            "tax_ar"   : tax_ar,
            "C_nw"     : C_nw,
            "C_ar"     : C_ar,
            "u_nw"     : crra_utility(C_nw, gamma),
            "u_ar"     : crra_utility(C_ar, gamma),
        })

    eu_nw  = sum(s["prob"] * s["u_nw"] for s in results_by_state)
    eu_ar  = sum(s["prob"] * s["u_ar"] for s in results_by_state)
    et_nw  = sum(s["prob"] * s["tax_nw"] for s in results_by_state)
    et_ar  = sum(s["prob"] * s["tax_ar"] for s in results_by_state)

    # Welfare under no-tax (consume all of W1)
    eu_notax = sum(
        prob * crra_utility(max(agent.net_worth_after_return(R), 1e-9), gamma)
        for R, prob in zip(dist.returns, dist.probs)
    )

    cew_nw = consumption_equiv_welfare(eu_nw, eu_notax, gamma)
    cew_ar = consumption_equiv_welfare(eu_ar, eu_notax, gamma)

    return {
        "leverage_ratio"  : agent.leverage_ratio,
        "W0"              : W0,
        "et_nw"           : et_nw,
        "et_ar"           : et_ar,
        "eu_nw"           : eu_nw,
        "eu_ar"           : eu_ar,
        "cew_nw"          : cew_nw,
        "cew_ar"          : cew_ar,
        "cew_gap_bp"      : (cew_nw - cew_ar) * 10000,
        "states"          : results_by_state,
    }


# ─────────────────────────────────────────────────────────────────────────────
# PART D: C3 — Two-period rate asymmetry
# Gain in period 1 taxed at high rate; loss in period 2 refunded at low rate
# ─────────────────────────────────────────────────────────────────────────────

def run_c3_two_period(
    W0       : float,
    R1_good  : float,   # period-1 return (positive)
    R2_bad   : float,   # period-2 return (negative delta)
    rate_fn  : ProgressiveRateFunction,
    gamma    : float,
    tau_flat : float,   # flat rate for comparison
) -> dict:
    """
    C3: Two-period sequence: gain then loss.

    Period 1: W₀ → W₁ = W₀×R1  (gain; taxed at τ(W₁))
    Period 2: W₁ → W₂ = W₁×R2  (loss; refunded at τ(W₂))

    Under flat rate: tax in P1 = τ×(W₁-W₀); refund in P2 = τ×(W₂-W₁)
    Net: τ×(W₂-W₀) — equivalent to one period with the same net change.

    Under progressive rate: τ_gain at high wealth ≠ τ_refund at lower wealth.
    Net tax is higher than the flat-rate equivalent for the same W₂.
    This is the C3 asymmetry: the agent pays more over a gain-then-loss
    sequence than they would under a flat rate achieving the same W₂.

    The welfare cost is the difference in CEW between progressive and flat.
    """
    # Period 1: gain
    W1 = W0 * R1_good
    tau1_prog = rate_fn.effective_rate(W0, W1)
    tax1_prog = tau1_prog * (W1 - W0)
    W1_post_prog = W1 - tax1_prog

    tau1_flat = tau_flat
    tax1_flat = tau1_flat * (W1 - W0)
    W1_post_flat = W1 - tax1_flat

    # Period 2: loss (refund) — rates based on post-period-1 wealth
    W2_prog = W1_post_prog * R2_bad
    W2_flat = W1_post_flat * R2_bad

    delta2_prog = W2_prog - W1_post_prog
    delta2_flat = W2_flat - W1_post_flat

    # Progressive refund: rate at W2 (lower wealth after loss)
    tau2_prog = rate_fn.effective_rate(W1_post_prog, W2_prog)
    refund_prog = tau2_prog * delta2_prog     # negative

    tau2_flat = tau_flat
    refund_flat = tau2_flat * delta2_flat     # negative

    C_prog = W2_prog - refund_prog    # consumption = post-tax final wealth
    C_flat = W2_flat - refund_flat

    net_tax_prog = tax1_prog + refund_prog
    net_tax_flat = tax1_flat + refund_flat

    # Single-period equivalent: what would a flat-rate apply to the same
    # net change W2 - W0?
    net_delta = (W0 * R1_good * R2_bad) - W0
    net_tax_single_flat = tau_flat * net_delta

    return {
        # Period-by-period detail
        "W0"              : W0,
        "W1"              : W1,
        "tax1_progressive": tax1_prog,
        "tau1_progressive": tau1_prog,
        "tax1_flat"       : tax1_flat,
        "W1_post_prog"    : W1_post_prog,
        "W1_post_flat"    : W1_post_flat,
        "W2_prog"         : W2_prog,
        "W2_flat"         : W2_flat,
        "tau2_progressive": tau2_prog,
        "refund_prog"     : refund_prog,
        "refund_flat"     : refund_flat,
        "C_prog"          : C_prog,
        "C_flat"          : C_flat,
        # Net position
        "net_tax_prog"    : net_tax_prog,
        "net_tax_flat"    : net_tax_flat,
        "net_tax_single"  : net_tax_single_flat,
        # Key asymmetry metric
        "rate_asymmetry"  : tau1_prog - tau2_prog,   # > 0 means gain taxed at higher rate
        "net_tax_excess"  : net_tax_prog - net_tax_flat,  # > 0 means progression costs more
        # Welfare
        "u_prog"          : crra_utility(max(C_prog, 1e-9), gamma),
        "u_flat"          : crra_utility(max(C_flat, 1e-9), gamma),
        "welfare_gap"     : crra_utility(max(C_prog, 1e-9), gamma) - crra_utility(max(C_flat, 1e-9), gamma),
    }


# ─────────────────────────────────────────────────────────────────────────────
# CHARTS
# ─────────────────────────────────────────────────────────────────────────────

def _save(fig, name: str):
    # DPI_SCREEN (150) is intentional for WFR preview outputs.
    # Use save_fig(fig, path) directly (default DPI_PRINT=300) for publication.
    save_fig(fig, OUTPUT_DIR / name, dpi=DPI_SCREEN)


def chart_rate_fig_4_1a_rate_functionunction(rate_fn: ProgressiveRateFunction, W_min_m: float):
    """Chart 4.1a: The logistic rate function across wealth levels."""
    W_vals = np.linspace(W_min_m, W_min_m * 50, 500)
    rates  = [rate_fn.rate(W) * 100 for W in W_vals]
    W_plot = W_vals / W_min_m    # express as multiples of W_min

    apply_style()
    fig, ax = plt.subplots(figsize=FIG_SINGLE)
    ax.plot(W_plot, rates, color=COLOURS["progressive_wdt"], linewidth=2.5)
    ax.axhline(rate_fn.tau0 * 100, color="grey", linestyle="--", linewidth=1,
               label=f"τ₀ = {fmt_pct0(rate_fn.tau0)} (entry rate)")
    ax.axhline(rate_fn.taum * 100, color=COLOURS["stock_wealth"], linestyle="--", linewidth=1,
               label=f"τ_m = {fmt_pct0(rate_fn.taum)} (ceiling)")
    ax.set_xlabel("Wealth as multiple of W_min (£2m threshold)", fontsize=9)
    ax.set_ylabel("Marginal WDT rate (%)", fontsize=9)
    ax.set_title("Figure 4.1a — Progressive WDT Rate Function (Logistic)\n"
                 f"τ₀={fmt_pct0(rate_fn.tau0)}, τ_m={fmt_pct0(rate_fn.taum)}, k={rate_fn.k}",
                 fontsize=11, fontweight="bold")
    ax.yaxis.set_major_formatter(mtick.PercentFormatter())
    ax.legend(fontsize=8)
    ax.grid(axis="y", linestyle="--", alpha=0.4)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    _save(fig, "wfr_fig_4_1a_rate_function.png")


def fig_4_1b_flat_vs_progressive(c1_results: dict):
    """Chart 4.1b: Flat vs progressive WDT CEW gap across γ and distributions."""
    apply_style()
    dist_labels = list(c1_results.keys())
    fig, axes = plt.subplots(1, len(dist_labels), figsize=FIG_PAIR, sharey=True)
    if len(dist_labels) == 1:
        axes = [axes]

    fig.suptitle("Figure 4.1b — Flat WDT vs Progressive WDT\n"
                 "(gap in basis points; positive = flat WDT better welfare)",
                 fontsize=11, fontweight="bold")

    for ax, dist_label in zip(axes, dist_labels):
        gammas = list(c1_results[dist_label].keys())
        gaps   = [c1_results[dist_label][g]["cew_gap_bp"] for g in gammas]
        cews_flat = [c1_results[dist_label][g]["cew_flat"] * 100 for g in gammas]
        cews_prog = [c1_results[dist_label][g]["cew_progressive"] * 100 for g in gammas]

        ax.plot(gammas, cews_flat, color=COLOURS["flat_wdt"], marker="o",
                linewidth=2, markersize=7, label="Flat WDT")
        ax.plot(gammas, cews_prog, color=COLOURS["progressive_wdt"], marker="s",
                linewidth=2, markersize=7, label="Progressive WDT", linestyle="--")

        ax.set_title(dist_label[:50], fontsize=9)
        ax.set_xlabel("γ (risk aversion)", fontsize=9)
        ax.set_ylabel("CEW (%)", fontsize=9)
        ax.yaxis.set_major_formatter(mtick.PercentFormatter(decimals=3))
        ax.set_xticks(gammas)
        ax.grid(axis="y", linestyle="--", alpha=0.4)
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)

    axes[-1].legend(fontsize=8)
    fig.tight_layout()
    _save(fig, "wfr_fig_4_1b_flat_vs_progressive.png")


def fig_4_1c_leverage(leverage_results: list):
    """Chart 4.1c: How leverage ratio affects CEW gap (NW base vs asset-return base)."""
    lev_ratios = [r["leverage_ratio"] * 100 for r in leverage_results]
    cew_gaps   = [r["cew_gap_bp"] for r in leverage_results]
    et_nw      = [r["et_nw"] for r in leverage_results]
    et_ar      = [r["et_ar"] for r in leverage_results]

    apply_style()
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=FIG_WIDE)
    fig.suptitle("Figure 4.1c — Leverage Effect on WDT Tax Base\n"
                 "(Net-worth base vs hypothetical asset-return base)",
                 fontsize=11, fontweight="bold")

    ax1.plot(lev_ratios, cew_gaps, color=COLOURS["c1_only"], marker="o",
             linewidth=2, markersize=7)
    ax1.axhline(0, color="black", linewidth=0.8, linestyle="--", alpha=0.5)
    ax1.set_xlabel("Leverage ratio (debt / gross assets, %)", fontsize=9)
    ax1.set_ylabel("CEW gap (basis points)\n(NW base − asset-return base)", fontsize=9)
    ax1.set_title("Welfare gap: NW base vs asset-return base", fontsize=9)
    ax1.grid(axis="y", linestyle="--", alpha=0.4)
    ax1.spines["top"].set_visible(False)
    ax1.spines["right"].set_visible(False)

    ax2.plot(lev_ratios, et_nw, color=COLOURS["flat_wdt"], marker="o",
             linewidth=2, markersize=7, label="Net-worth delta base (WDT)")
    ax2.plot(lev_ratios, et_ar, color=COLOURS["stock_wealth"], marker="s",
             linewidth=2, markersize=7, label="Asset-return base (hypothetical)")
    ax2.set_xlabel("Leverage ratio (debt / gross assets, %)", fontsize=9)
    ax2.set_ylabel("Expected tax E[T]", fontsize=9)
    ax2.set_title("Revenue: NW base vs asset-return base", fontsize=9)
    ax2.legend(fontsize=8)
    ax2.grid(axis="y", linestyle="--", alpha=0.4)
    ax2.spines["top"].set_visible(False)
    ax2.spines["right"].set_visible(False)

    fig.tight_layout()
    _save(fig, "wfr_fig_4_1c_leverage.png")


def fig_4_1d_asymmetry(c3_results: list, W0_vals: list):
    """Chart 4.1d: C3 rate asymmetry — net tax excess over flat, by initial wealth.
    W0_vals is already in £m (W_min * multiplier, W_min = 2.0 £m).
    """
    excess = [r["net_tax_excess"] for r in c3_results]
    asym   = [r["rate_asymmetry"] * 100 for r in c3_results]
    W_plot = list(W0_vals)    # already in £m — no unit conversion needed

    apply_style()
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=FIG_WIDE)
    fig.suptitle("Figure 4.1d — Two-Period Rate Asymmetry\n"
                 "(Gain in period 1, loss in period 2)",
                 fontsize=11, fontweight="bold")

    ax1.plot(W_plot, excess, color=COLOURS["c3_only"], marker="o",
             linewidth=2, markersize=7)
    ax1.axhline(0, color="black", linewidth=0.8, linestyle="--", alpha=0.5)
    ax1.set_xlabel("Initial wealth W₀ (£m)", fontsize=9)
    ax1.set_ylabel("Net tax excess vs flat rate (£m)", fontsize=9)
    ax1.set_title("Extra tax from progression (gain-then-loss path)", fontsize=9)
    ax1.grid(axis="y", linestyle="--", alpha=0.4)
    ax1.spines["top"].set_visible(False)
    ax1.spines["right"].set_visible(False)

    ax2.plot(W_plot, asym, color=COLOURS["c1_c3_combined"], marker="s",
             linewidth=2, markersize=7)
    ax2.axhline(0, color="black", linewidth=0.8, linestyle="--", alpha=0.5)
    ax2.set_xlabel("Initial wealth W₀ (£m)", fontsize=9)
    ax2.set_ylabel("Rate asymmetry τ_gain − τ_refund (pp)", fontsize=9)
    ax2.set_title("Progressive rate asymmetry between gain and loss periods", fontsize=9)
    ax2.grid(axis="y", linestyle="--", alpha=0.4)
    ax2.spines["top"].set_visible(False)
    ax2.spines["right"].set_visible(False)

    fig.tight_layout()
    _save(fig, "wfr_fig_4_1d_asymmetry.png")


def fig_4_1_combined_gamma(
    dist_label: str,
    gamma: float,
    cew_flat_wdt   : float,
    cew_prog_wdt   : float,
    cew_stock      : float,
    fig_index      : int,                          # 0 → e, 1 → f, 2 → g
):
    """Chart 4.1E/4.1F/4.1G: Final comparison — progressive WDT vs flat WDT vs stock wealth tax."""
    fig_letter = ["e", "f", "g"][fig_index]

    labels = ["Flat WDT\n(Module 1\nbenchmark)",
              "Progressive WDT\n(with all three\ncomplications)",
              "Stock Wealth Tax\n(Module 1\nbenchmark)"]
    values = [cew_flat_wdt * 100, cew_prog_wdt * 100, cew_stock * 100]
    colors = [COLOURS["flat_wdt"], COLOURS["progressive_wdt"], COLOURS["stock_wealth"]]

    apply_style()
    fig, ax = plt.subplots(figsize=FIG_SINGLE)
    bars = ax.bar(labels, values, color=colors, edgecolor="white",
                  linewidth=0.8, alpha=0.88, width=0.5)

    for bar, val in zip(bars, values):
        ax.text(bar.get_x() + bar.get_width() / 2,
                val - 0.005 if val < 0 else val + 0.005,
                f"{val:.3f}%", ha="center", va="top" if val < 0 else "bottom",
                fontsize=9, fontweight="bold")

    ax.axhline(0, color="black", linewidth=0.8)
    ax.set_ylabel("CEW vs No-Tax (%)", fontsize=9)
    ax.set_title(
        f"4.1{fig_letter} — Progressive WDT vs Flat WDT vs Stock Wealth Tax\n"
        f"γ = {gamma} | {dist_label[:50]}",
        fontsize=10, fontweight="bold"
    )
    ax.yaxis.set_major_formatter(mtick.PercentFormatter(decimals=3))
    ax.grid(axis="y", linestyle="--", alpha=0.4)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    fig.tight_layout()
    _save(fig, f"wfr_fig_4_1{fig_letter}_combined_gamma{int(gamma)}.png")


# ─────────────────────────────────────────────────────────────────────────────
# PRINT HELPERS
# ─────────────────────────────────────────────────────────────────────────────

def print_c1_table(c1_results: dict):
    print("\n" + "=" * 80)
    print("PROGRESSION — Flat WDT vs Progressive WDT (revenue-equivalent comparison)")
    print("Flat rate solved to match progressive E[T], not the 2%-of-W₀ global target.")
    print("=" * 80)
    print(f"{'Distribution':38s} {'γ':>4} {'Flat CEW':>10} {'Prog CEW':>10} "
          f"{'Gap (bp)':>10} {'E[T] matched':>13} {'vs 2% target':>13}")
    print("-" * 80)
    for dist_label, gamma_results in c1_results.items():
        for g, r in gamma_results.items():
            et_dev = r['et_progressive'] - r['et_flat_target']
            flag   = "" if r.get("revenue_matched", True) else " [!]"
            print(
                f"{dist_label[:38]:38s} {g:>4.1f} "
                f"{fmt_pct4(r['cew_flat']):>10} "
                f"{fmt_pct4(r['cew_progressive']):>10} "
                f"{r['cew_gap_bp']:>+10.2f} "
                f"{fmt_gbp_m(r['et_progressive'], dp=4):>13} "
                f"{et_dev:>+12.4f}m{flag}"
            )
    print("  [!] = et_prog <= 0; flat calibrated to 2% target instead (comparison not clean)")
    print()


def print_c3_table(c3_results: list, W0_vals: list, gamma: float):
    print("\n" + "=" * 70)
    print(f"TWO-PERIOD ASYMMETRY (γ={gamma})")
    print("Sequence: +11.5% gain then −8.3% loss (empirical mean ± 1σ)")
    print("=" * 70)
    print(f"{'W₀ (£m)':>10} {'τ_gain':>8} {'τ_refund':>10} {'Asym (pp)':>10} "
          f"{'Net tax prog':>14} {'Net tax flat':>14} {'Excess':>10}")
    print("-" * 70)
    for W0, r in zip(W0_vals, c3_results):
        # W0 is already in £m (W_min * multiplier, W_min = 2.0 £m)
        print(
            f"{W0:>10.1f} "
            f"{fmt_pct(r['tau1_progressive']):>8} "
            f"{fmt_pct(r['tau2_progressive']):>10} "
            f"{r['rate_asymmetry']*100:>+9.2f}pp "
            f"{fmt_gbp_m(r['net_tax_prog'], dp=4):>14} "
            f"{fmt_gbp_m(r['net_tax_flat'], dp=4):>14} "
            f"{r['net_tax_excess']:>+10.4f}"
        )
    print()

# ─────────────────────────────────────────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────────────────────────────────────────

def main():
    print("=" * 70)
    print("MODULE 2: Progressive Rates and the Three D-M Complications")
    print("=" * 70)

    p   = load_params(TOML_PATH)
    N   = p["tcm"]["canonical_N"] 
    dist_A = make_empirical_distribution_scenario(p, N)
    dist_B = make_idealised_distribution_scenario(p, N)

    # Build rate function from TOML
    vp = p["rate"]
    rate_fn = ProgressiveRateFunction(
        tau0  = vp["tau_0"],
        taum  = vp["tau_m"],
        k     = vp["k"],
        W_min = vp["W_min"]   # TOML stores W_min in £m; k also expects £m,
    )
    print(f"\n{rate_fn.describe()}\n")

    # ── Part A: Rate function chart ──────────────────────────────────────────
    print("--- Part A: Rate function ---")
    chart_rate_fig_4_1a_rate_functionunction(rate_fn, vp["W_min"])

    # ── Part B: C1 — Flat vs progressive (single period) ────────────────────
    print("\n--- Part B: C1 — Progression effect ---")
    c1_results = {}
    for dist in [dist_A, dist_B]:
        c1_results[dist.label] = {}
        for gamma in GAMMA_VALS:
            # W0 set to W_min × 5 — middle of the taxable population
            W0_c1 = vp["W_min"] * 5
            r = run_c1_analysis(W0_c1, dist, rate_fn, gamma, TARGET_ET * W0_c1)
            c1_results[dist.label][gamma] = r

    print_c1_table(c1_results)
    fig_4_1b_flat_vs_progressive(c1_results)

    # ── Part C: C2 — Leverage ────────────────────────────────────────────────
    print("--- Part C: C2 — Leverage ---")
    gross_assets  = vp["W_min"] * 5     # £10m gross assets
    leverage_grid = np.linspace(0.0, 0.70, 15)  # 0% to 70% leverage
    lev_results   = []
    for lev in leverage_grid:
        agent = LeveragedAgent(
            gross_assets = gross_assets,
            debt         = gross_assets * lev,
        )
        r = run_c2_leverage(agent, dist_A, rate_fn, gamma=2.0)
        lev_results.append(r)
        print(f"  Leverage {lev*100:4.0f}%: W₀={fmt_gbp_m(r['W0']/1e6)}  "
              f"E[T]_nw={r['et_nw']:.4f}  E[T]_ar={r['et_ar']:.4f}  "
              f"CEW gap={r['cew_gap_bp']:+.2f}bp")

    fig_4_1c_leverage(lev_results)

    # ── Part D: C3 — Two-period rate asymmetry ───────────────────────────────
    print("\n--- Part D: C3 — Rate asymmetry (gain then loss) ---")
    # Use empirical mean ± σ as the two-period scenario
    mu    = p["tcm"]["hist_mean"]
    sigma = float(np.std(p["returns"]["array"], ddof=0))
    R1_good = 1.0 + mu + sigma   # ~18.76% gain
    R2_bad  = 1.0 + mu - sigma   # ~2.14% gain (still positive — real UK data)

    # For a more illustrative C3, use a genuine loss in period 2
    R2_loss = 1.0 - sigma        # ~8.3% loss — makes the asymmetry visible

    W0_vals = [vp["W_min"] * m for m in [1.5, 2, 5, 10, 20, 50, 100]]

    from welfare_core import solve_revenue_equivalent_rate, get_tax_fn
    flat_fn  = get_tax_fn("symmetric_wdt")
    tau_flat = solve_revenue_equivalent_rate(
        vp["W_min"] * 5, dist_A, flat_fn, TARGET_ET * vp["W_min"] * 5
    )

    c3_results = []
    for W0_c3 in W0_vals:
        r = run_c3_two_period(W0_c3, R1_good, R2_loss, rate_fn, 2.0, tau_flat)
        c3_results.append(r)

    print_c3_table(c3_results, W0_vals, gamma=2.0)
    fig_4_1d_asymmetry(c3_results, W0_vals)

    # ── Part E/F: Combined comparison ────────────────────────────────────────
    print("--- Part F: Combined comparison ---")
    for fig_index, gamma in enumerate(GAMMA_VALS):
        W0_ref = vp["W_min"] * 5
        # Flat WDT CEW from Module 1 results (recompute for this W0)
        flat_results = run_welfare_comparison(
            W0=W0_ref, dist=dist_A, gamma=gamma,
            target_et=TARGET_ET * W0_ref
        )
        cew_flat  = flat_results["symmetric_wdt"].cew
        cew_stock = flat_results["stock_wealth"].cew

        # Progressive WDT CEW
        eu_notax  = expected_utility(W0_ref, dist_A, flat_fn, 0.0, gamma)
        eu_prog   = expected_utility_progressive(W0_ref, dist_A, rate_fn, gamma)
        cew_prog  = consumption_equiv_welfare(eu_prog, eu_notax, gamma)

        print(f"\n  γ={gamma}: Flat WDT CEW={cew_flat*100:.4f}%  "
              f"Progressive WDT CEW={cew_prog*100:.4f}%  "
              f"Stock WTax CEW={cew_stock*100:.4f}%")

        fig_4_1_combined_gamma(
            dist_A.label, gamma, cew_flat, cew_prog, cew_stock,
            fig_index=fig_index,
        )

    print(f"\n✓ Module 2 complete. Outputs in: {OUTPUT_DIR}")


if __name__ == "__main__":
    main()