"""
wfr_charts.py
=============
WFR Welfare Comparison Model — Chart Generator

Reads wfr_results.json (produced by wfr_core.py) and writes all PNGs
to OUTPUTS/WFR/charts/.

Stateless: no computation, no model imports.  Only reads JSON
and renders matplotlib figures.

Usage
-----
  python wfr_charts.py                                 # default paths
  python wfr_charts.py --json path/to/wfr_results.json
  python wfr_charts.py --out  path/to/output_dir/
  python wfr_charts.py --modules 1 2 3               # subset of charts

Chart inventory
---------------
Module 1
  wfr_fig_3_1a_cew_by_gamma.png         CEW across γ — both distributions
  wfr_fig_3_1b_wdt_advantage.png        WDT advantage over competitors in bp
  wfr_fig_3_1c_annual_tax.png           Annual tax/refund by year (Ver. A)
  wfr_fig_3_2_variance.png              Variance of consumption — bar chart

Module 2
  wfr_fig_4_1a_rate_function.png        Progressive logistic rate function
  wfr_fig_4_1b_flat_vs_progressive.png  Flat vs progressive CEW
  wfr_fig_4_1c_leverage.png             Leverage effect on tax base
  wfr_fig_4_1d_asymmetry.png            Two-period rate asymmetry

Module 3
  wfr_fig_4_2_1_lock_in_threshold.png   CGT lock-in threshold curve
  wfr_fig_4_2_2a_full_comparison.png    WDT vs CGT full welfare comparison
  wfr_fig_4_2_2b_sensitivity_gain.png   Sensitivity: gain ratio
  wfr_fig_4_2_2c_sensitivity_T.png      Sensitivity: holding period

Module 4
  wfr_fig_4_3_2_concentration_path.png  Wealth concentration path (N=30)
  wfr_fig_4_3_3_tier_cew.png            Heatmap + grouped bars: tier × system
  wfr_fig_4_3_4_incidence.png           Distributional incidence
  wfr_fig_4_3_5_envelope_binding.png    Envelope slack over time
  wfr_fig_4_3_6_corner_check.png        Off-diagonal spot check

Module 4 Part F
  wfr_fig_7_4a_progressive_vs_flat_extended.png   N=73 flat vs progressive
  wfr_fig_7_4b_full_concentration_extended.png     N=73 all systems

Module 5
  wfr_fig_4_5_1a_revenue_target.png     CEW vs revenue target
  wfr_fig_4_5_1b_w0_sensitivity.png     CEW vs W₀
  wfr_fig_4_5_2a_start_year_distribution.png  Box plot: start-year CEW
  wfr_fig_4_5_2b_timeseries.png         CEW by start year (time series)
  wfr_fig_4_5_3a_tau0.png               τ₀ parameter sensitivity
  wfr_fig_4_5_3b_taum.png               τ_m parameter sensitivity
  wfr_fig_4_5_3c_k.png                  k parameter sensitivity
  wfr_fig_4_5_3d_wmin.png               W_min parameter sensitivity
"""

from __future__ import annotations

import argparse
import json
import math
import sys
import numpy as np
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
import matplotlib.patches as mpatches

from wdt_style import (
    apply_style, save_fig,
    FIG_SINGLE, FIG_PAIR, FIG_PAIR_T, FIG_WIDE, FIG_WIDE_L, FIG_QUAD,
    DPI_SCREEN,
    C_DARK, C_ANNOTATION, C_GRID,
)
from wdt_fmt import fmt_pct, fmt_pct0, fmt_pct1, fmt_pct4, fmt_gbp_m

# ─────────────────────────────────────────────────────────────────────────────
# CONSTANTS
# ─────────────────────────────────────────────────────────────────────────────

SYSTEMS = ["symmetric_wdt", "stock_wealth", "income", "cgt", "consumption"]
SYSTEM_LABELS = {
    "symmetric_wdt":  "Symmetric WDT (flat)",
    "stock_wealth":   "Stock Wealth Tax",
    "income":         "Income Tax (no refund)",
    "cgt":            "CGT (gains only)",
    "consumption":    "Consumption Tax",
}
COLOURS = {
    "symmetric_wdt":  "#1a6fad",
    "stock_wealth":   "#c0392b",
    "income":         "#e67e22",
    "cgt":            "#f1c40f",
    "consumption":    "#7f8c8d",
    "progressive_wdt": "#0d3d6b",
}
MARKERS = {
    "symmetric_wdt":  "o",
    "stock_wealth":   "s",
    "income":         "^",
    "cgt":            "D",
    "consumption":    "P",
}
TIER_COLOURS = {
    "Poor":  "#c0392b",
    "Ok":    "#e67e22",
    "Good":  "#2ecc71",
    "Great": "#1a6fad",
}
GAMMA_VALS = [1.0, 2.0, 4.0]


# ─────────────────────────────────────────────────────────────────────────────
# OUTPUT SETUP
# ─────────────────────────────────────────────────────────────────────────────

def _save(fig, out_dir: Path, name: str):
    save_fig(fig, out_dir / name, dpi=DPI_SCREEN)


def _dist_short(label: str) -> str:
    return "Ver. A" if "Version A" in label else "Ver. B"


def _style_ax(ax, title="", xlabel="", ylabel=""):
    ax.set_title(title, fontsize=11, fontweight="bold", pad=8)
    ax.set_xlabel(xlabel, fontsize=9)
    ax.set_ylabel(ylabel, fontsize=9)
    ax.tick_params(labelsize=8)
    ax.grid(axis="y", linestyle="--", alpha=0.4)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)


# ─────────────────────────────────────────────────────────────────────────────
# MODULE 1 CHARTS
# ─────────────────────────────────────────────────────────────────────────────

def fig_3_1a_cew_by_gamma(m1: dict, out_dir: Path, target_et: float):
    dist_keys = list(m1["distributions"].keys())
    apply_style()
    fig, axes = plt.subplots(1, len(dist_keys), figsize=FIG_PAIR, sharey=True)
    if len(dist_keys) == 1:
        axes = [axes]

    fig.suptitle(
        f"Fig 3.1a — CEW vs No-Tax Benchmark — by Risk Aversion (γ)\n"
        f"Revenue target E[T] = {fmt_pct0(target_et)} of W₀",
        fontsize=12, fontweight="bold"
    )
    for ax, dk in zip(axes, dist_keys):
        for name in SYSTEMS:
            cews = []
            for g in GAMMA_VALS:
                v = m1["distributions"][dk]["welfare"].get(str(g), {}).get(name, {}).get("cew")
                cews.append(v * 100 if v is not None else np.nan)
            ax.plot(GAMMA_VALS, cews, color=COLOURS[name], marker=MARKERS[name],
                    linewidth=2, markersize=7, label=SYSTEM_LABELS[name])
        ax.axhline(0, color="black", linewidth=0.8, linestyle="--", alpha=0.5)
        ax.yaxis.set_major_formatter(mtick.PercentFormatter(decimals=2))
        _style_ax(ax, _dist_short(dk)[:55], xlabel="γ (risk aversion)", ylabel="CEW (%)")
        ax.set_xticks(GAMMA_VALS)

    axes[-1].legend(fontsize=8, loc="lower right")
    fig.tight_layout()
    _save(fig, out_dir, "wfr_fig_3_1a_cew_by_gamma.png")


def fig_3_1b_wdt_advantage(m1: dict, out_dir: Path):
    dist_keys   = list(m1["distributions"].keys())
    competitors = ["stock_wealth", "income", "cgt", "consumption"]
    apply_style()
    fig, axes = plt.subplots(1, len(dist_keys), figsize=FIG_PAIR, sharey=True)
    if len(dist_keys) == 1:
        axes = [axes]
    fig.suptitle(
        "Fig 3.1b — WDT Welfare Advantage over Competitors\n"
        "(CEW_WDT − CEW_competitor, in basis points; positive = WDT better)",
        fontsize=12, fontweight="bold"
    )
    for ax, dk in zip(axes, dist_keys):
        for comp in competitors:
            gaps = []
            for g in GAMMA_VALS:
                gstr = str(g)
                wdt = m1["distributions"][dk]["welfare"].get(gstr, {}).get("symmetric_wdt", {}).get("cew")
                cmp = m1["distributions"][dk]["welfare"].get(gstr, {}).get(comp, {}).get("cew")
                gaps.append((wdt - cmp) * 10000 if (wdt is not None and cmp is not None) else np.nan)
            ax.plot(GAMMA_VALS, gaps, color=COLOURS[comp], marker=MARKERS[comp],
                    linewidth=2, markersize=7, label=SYSTEM_LABELS[comp])
        ax.axhline(0, color="black", linewidth=0.8, linestyle="--", alpha=0.6)
        ax.yaxis.set_major_formatter(mtick.FormatStrFormatter("%.1f bp"))
        _style_ax(ax, _dist_short(dk)[:55],
                  xlabel="γ (risk aversion)", ylabel="WDT advantage (basis points)")
        ax.set_xticks(GAMMA_VALS)
    axes[-1].legend(fontsize=8, loc="upper left")
    fig.tight_layout()
    _save(fig, out_dir, "wfr_fig_3_1b_wdt_advantage.png")


def fig_3_1c_annual_tax(m1: dict, out_dir: Path, scenario_start: int, N: int):
    """Annual tax/refund per £1 W₀ for flat WDT, stock wealth, income tax."""
    # Use first Version A distribution
    dk = next(dk for dk in m1["distributions"] if "Version A" in dk)
    welfare = m1["distributions"][dk]["welfare"].get("2.0", {})
    returns = m1["distributions"][dk]["returns"]
    years   = list(range(scenario_start, scenario_start + N))
    systems = ["symmetric_wdt", "stock_wealth", "income"]

    apply_style()
    fig, axes = plt.subplots(3, 1, figsize=FIG_QUAD, sharex=True)
    fig.suptitle(
        f"Fig 3.1c — Annual Tax Paid (+) / Refund Received (−) per £1 of W₀\n"
        f"Version A — UK Equity {years[0]}–{years[-1]} ({N} obs, scenario)",
        fontsize=12, fontweight="bold"
    )
    neg_years = [years[i] for i, R in enumerate(returns) if R < 1.0]

    for ax, name in zip(axes, systems):
        taxes = welfare.get(name, {}).get("state_taxes")
        if taxes is None:
            taxes = [0.0] * N
        colors = ["#c0392b" if t < 0 else COLOURS[name] for t in taxes]
        ax.bar(years, taxes, color=colors, width=0.8, alpha=0.85)
        ax.axhline(0, color="black", linewidth=0.8)
        for ny in neg_years:
            ax.axvline(ny, color="grey", linestyle=":", linewidth=0.8, alpha=0.6)
        ax.set_ylabel(f"{SYSTEM_LABELS[name]}\ntax paid (£)", fontsize=8)
        ax.tick_params(labelsize=7)
        ax.grid(axis="y", linestyle="--", alpha=0.3)
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)

    axes[-1].set_xlabel("Year", fontsize=9)
    neg_note = ", ".join(str(y) for y in neg_years) or "none"
    fig.text(0.01, 0.5, f"Dotted lines = negative return years: {neg_note}",
             va="center", rotation="vertical", fontsize=7, color="grey")
    fig.tight_layout(rect=[0.02, 0, 1, 1])
    _save(fig, out_dir, "wfr_fig_3_1c_annual_tax.png")


def fig_3_2_variance(m1: dict, out_dir: Path, target_et: float):
    dist_keys = list(m1["distributions"].keys())
    gamma     = "2.0"
    apply_style()
    fig, axes = plt.subplots(1, len(dist_keys), figsize=FIG_PAIR, sharey=False)
    if len(dist_keys) == 1:
        axes = [axes]
    fig.suptitle(
        "Fig 3.2 — Variance of Consumption by Tax System\n"
        f"(γ=2, E[T] = {fmt_pct0(target_et)} of W₀)",
        fontsize=12, fontweight="bold"
    )
    for ax, dk in zip(axes, dist_keys):
        names  = SYSTEMS
        labels = [SYSTEM_LABELS[n].replace(" (", "\n(").replace(" Tax", "\nTax") for n in names]
        vars_  = [m1["distributions"][dk]["welfare"].get(gamma, {}).get(n, {}).get("var_consumption")
                  for n in names]
        vars_f = [v if v is not None else np.nan for v in vars_]
        bars = ax.bar(labels, vars_f, color=[COLOURS[n] for n in names],
                      edgecolor="white", linewidth=0.8, alpha=0.85)
        notax_var = m1["distributions"][dk]["welfare"].get(gamma, {}).get("symmetric_wdt", {}).get("var_consumption", 0)
        ax.axhline(notax_var, color="black", linestyle="--", linewidth=1.2,
                   label=f"WDT notax proxy ({notax_var:.4f})")
        for bar, v in zip(bars, vars_f):
            if not np.isnan(v):
                ax.text(bar.get_x() + bar.get_width() / 2, v * 1.01,
                        f"{v:.4f}", ha="center", va="bottom", fontsize=7.5)
        ax.legend(fontsize=8)
        _style_ax(ax, _dist_short(dk)[:55], ylabel="Var(consumption)")
    fig.tight_layout()
    _save(fig, out_dir, "wfr_fig_3_2_variance.png")


# ─────────────────────────────────────────────────────────────────────────────
# MODULE 2 CHARTS
# ─────────────────────────────────────────────────────────────────────────────

def fig_4_1a_rate_function(m2: dict, out_dir: Path):
    rf    = m2["rate_fn"]
    tau0  = rf["tau0"]; taum = rf["taum"]; k = rf["k"]; W_min = rf["W_min"]
    A     = (taum - tau0) / tau0

    def rate(W):
        if W <= W_min:
            return 0.0
        return taum / (1.0 + A * math.exp(-k * (W - W_min)))

    W_vals = np.linspace(W_min, W_min * 50, 500)
    rates  = [rate(W) * 100 for W in W_vals]
    W_plot = W_vals / W_min

    apply_style()
    fig, ax = plt.subplots(figsize=FIG_SINGLE)
    ax.plot(W_plot, rates, color=COLOURS["progressive_wdt"], linewidth=2.5)
    ax.axhline(tau0 * 100, color="grey", linestyle="--", linewidth=1,
               label=f"τ₀ = {fmt_pct0(tau0)} (entry rate)")
    ax.axhline(taum * 100, color=COLOURS["stock_wealth"], linestyle="--", linewidth=1,
               label=f"τ_m = {fmt_pct0(taum)} (ceiling)")
    ax.set_xlabel("Wealth as multiple of W_min (£2m threshold)", fontsize=9)
    ax.set_ylabel("Marginal WDT rate (%)", fontsize=9)
    ax.set_title(
        f"Figure 4.1a — Progressive WDT Rate Function (Logistic)\n"
        f"τ₀={fmt_pct0(tau0)}, τ_m={fmt_pct0(taum)}, k={k}",
        fontsize=11, fontweight="bold"
    )
    ax.yaxis.set_major_formatter(mtick.PercentFormatter())
    ax.legend(fontsize=8)
    ax.grid(axis="y", linestyle="--", alpha=0.4)
    ax.spines["top"].set_visible(False); ax.spines["right"].set_visible(False)
    fig.tight_layout()
    _save(fig, out_dir, "wfr_fig_4_1a_rate_function.png")


def fig_4_1b_flat_vs_progressive(m2: dict, out_dir: Path):
    c1 = m2["c1"]
    dist_keys = list(c1.keys())
    apply_style()
    fig, axes = plt.subplots(1, len(dist_keys), figsize=FIG_PAIR, sharey=True)
    if len(dist_keys) == 1:
        axes = [axes]
    fig.suptitle("Figure 4.1b — Flat WDT vs Progressive WDT\n"
                 "(gap in basis points; positive = flat WDT better welfare)",
                 fontsize=11, fontweight="bold")
    for ax, dk in zip(axes, dist_keys):
        gammas = [float(g) for g in c1[dk].keys()]
        cews_flat = [c1[dk][str(g)].get("cew_flat") for g in gammas]
        cews_prog = [c1[dk][str(g)].get("cew_progressive") for g in gammas]
        ax.plot(gammas, [v * 100 if v else np.nan for v in cews_flat],
                color=COLOURS["symmetric_wdt"], marker="o", linewidth=2, markersize=7, label="Flat WDT")
        ax.plot(gammas, [v * 100 if v else np.nan for v in cews_prog],
                color=COLOURS["progressive_wdt"], marker="s", linewidth=2, markersize=7,
                label="Progressive WDT", linestyle="--")
        ax.set_title(_dist_short(dk)[:50], fontsize=9)
        ax.set_xlabel("γ (risk aversion)", fontsize=9)
        ax.set_ylabel("CEW (%)", fontsize=9)
        ax.yaxis.set_major_formatter(mtick.PercentFormatter(decimals=3))
        ax.set_xticks(gammas)
        ax.grid(axis="y", linestyle="--", alpha=0.4)
        ax.spines["top"].set_visible(False); ax.spines["right"].set_visible(False)
    axes[-1].legend(fontsize=8)
    fig.tight_layout()
    _save(fig, out_dir, "wfr_fig_4_1b_flat_vs_progressive.png")


def fig_4_1c_leverage(m2: dict, out_dir: Path):
    lev = m2["c2_leverage"]
    lev_ratios = [r["leverage_ratio"] * 100 for r in lev]
    cew_gaps   = [r.get("cew_gap_bp", 0) or 0 for r in lev]
    et_nw      = [r.get("et_nw", 0) or 0 for r in lev]
    et_ar      = [r.get("et_ar", 0) or 0 for r in lev]

    apply_style()
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=FIG_WIDE)
    fig.suptitle("Figure 4.1c — Leverage Effect on WDT Tax Base", fontsize=11, fontweight="bold")

    ax1.plot(lev_ratios, cew_gaps, color="#2ecc71", marker="o", linewidth=2, markersize=7)
    ax1.axhline(0, color="black", linewidth=0.8, linestyle="--", alpha=0.5)
    ax1.set_xlabel("Leverage ratio (debt / gross assets, %)", fontsize=9)
    ax1.set_ylabel("CEW gap (basis points)\n(NW base − asset-return base)", fontsize=9)
    ax1.set_title("Welfare gap: NW base vs asset-return base", fontsize=9)
    ax1.grid(axis="y", linestyle="--", alpha=0.4)
    ax1.spines["top"].set_visible(False); ax1.spines["right"].set_visible(False)

    ax2.plot(lev_ratios, et_nw, color=COLOURS["symmetric_wdt"], marker="o",
             linewidth=2, markersize=7, label="Net-worth delta base (WDT)")
    ax2.plot(lev_ratios, et_ar, color=COLOURS["stock_wealth"], marker="s",
             linewidth=2, markersize=7, label="Asset-return base (hypothetical)")
    ax2.set_xlabel("Leverage ratio (%)", fontsize=9)
    ax2.set_ylabel("Expected tax E[T]", fontsize=9)
    ax2.set_title("Revenue: NW base vs asset-return base", fontsize=9)
    ax2.legend(fontsize=8)
    ax2.grid(axis="y", linestyle="--", alpha=0.4)
    ax2.spines["top"].set_visible(False); ax2.spines["right"].set_visible(False)

    fig.tight_layout()
    _save(fig, out_dir, "wfr_fig_4_1c_leverage.png")


def fig_4_1d_asymmetry(m2: dict, out_dir: Path):
    c3   = m2["c3_asymmetry"]
    W0_vals = c3["W0_vals"]
    results = c3["results"]
    excess  = [r.get("net_tax_excess", 0) or 0 for r in results]
    asym    = [(r.get("rate_asymmetry", 0) or 0) * 100 for r in results]

    apply_style()
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=FIG_WIDE)
    fig.suptitle("Figure 4.1d — Two-Period Rate Asymmetry\n(Gain then loss)", fontsize=11, fontweight="bold")

    ax1.plot(W0_vals, excess, color="#e74c3c", marker="o", linewidth=2, markersize=7)
    ax1.axhline(0, color="black", linewidth=0.8, linestyle="--", alpha=0.5)
    ax1.set_xlabel("Initial wealth W₀ (£m)", fontsize=9)
    ax1.set_ylabel("Net tax excess vs flat rate (£m)", fontsize=9)
    ax1.set_title("Extra tax from progression (gain-then-loss path)", fontsize=9)
    ax1.grid(axis="y", linestyle="--", alpha=0.4)
    ax1.spines["top"].set_visible(False); ax1.spines["right"].set_visible(False)

    ax2.plot(W0_vals, asym, color="#8e44ad", marker="s", linewidth=2, markersize=7)
    ax2.axhline(0, color="black", linewidth=0.8, linestyle="--", alpha=0.5)
    ax2.set_xlabel("Initial wealth W₀ (£m)", fontsize=9)
    ax2.set_ylabel("Rate asymmetry τ_gain − τ_refund (pp)", fontsize=9)
    ax2.set_title("Progressive rate asymmetry between gain and loss periods", fontsize=9)
    ax2.grid(axis="y", linestyle="--", alpha=0.4)
    ax2.spines["top"].set_visible(False); ax2.spines["right"].set_visible(False)

    fig.tight_layout()
    _save(fig, out_dir, "wfr_fig_4_1d_asymmetry.png")


# ─────────────────────────────────────────────────────────────────────────────
# MODULE 3 CHARTS
# ─────────────────────────────────────────────────────────────────────────────

def fig_4_2_1_lock_in_threshold(m3: dict, out_dir: Path):
    tc = m3["threshold_curve"]
    ar = m3["asset_ref"]
    apply_style()
    fig, ax = plt.subplots(figsize=FIG_SINGLE)
    r_B_grid = tc["r_B_grid"]
    npv_diff = tc["npv_diff"]
    r_B_indiff = tc["r_B_indiff"]

    ax.plot([r * 100 for r in r_B_grid], npv_diff, color=COLOURS["cgt"], linewidth=2.5,
            label="NPV(stay in A) − NPV(switch to B)")
    ax.axhline(0, color="black", linewidth=0.9)
    if r_B_indiff is not None:
        ax.axvline(r_B_indiff * 100, color="#c0392b", linewidth=1.5, linestyle="--",
                   label=f"r_B* = {fmt_pct(r_B_indiff)}")
    ax.axvline(ar["r_A"] * 100, color="grey", linewidth=1.2, linestyle=":",
               label=f"r_A = {fmt_pct(ar['r_A'])}")

    ax.fill_between(
        [r * 100 for r in r_B_grid], npv_diff, 0,
        where=[r < (r_B_indiff or 0) for r in r_B_grid],
        alpha=0.15, color="#c0392b", label="Lock-in region"
    )
    ax.set_xlabel("Asset B expected return r_B (%)", fontsize=9)
    ax.set_ylabel("NPV preference for Asset A (£m)", fontsize=9)
    ax.set_title(
        f"Figure 4.2.1 — CGT Lock-In Threshold\n"
        f"V={fmt_gbp_m(ar['V'], dp=0)}, G/V={fmt_pct0(ar['gain_ratio'])}, "
        f"τ_cgt={fmt_pct0(ar['tau_cgt'])}, T={ar['T']}yr",
        fontsize=10, fontweight="bold"
    )
    ax.legend(fontsize=8)
    ax.grid(axis="y", linestyle="--", alpha=0.4)
    ax.spines["top"].set_visible(False); ax.spines["right"].set_visible(False)
    fig.tight_layout()
    _save(fig, out_dir, "wfr_fig_4_2_1_lock_in_threshold.png")


def fig_4_2_2a_full_comparison(m3: dict, out_dir: Path):
    # Use first distribution
    dk    = list(m3["full_comparison"].keys())[0]
    comp  = m3["full_comparison"][dk]
    labels = ["WDT\n(Module 1)", "CGT\n(no lock-in,\nModule 1)", "CGT\n(with lock-in)"]
    values = [comp.get("wdt_cew", 0) * 100, comp.get("cgt_cew", 0) * 100,
              comp.get("cgt_with_lock_cew", 0) * 100]
    colors = [COLOURS["symmetric_wdt"], COLOURS["cgt"], "#e67e22"]

    apply_style()
    fig, ax = plt.subplots(figsize=FIG_SINGLE)
    bars = ax.bar(labels, values, color=colors, edgecolor="white", linewidth=0.8, alpha=0.88, width=0.45)
    for bar, val in zip(bars, values):
        ax.text(bar.get_x() + bar.get_width() / 2, val - 0.002,
                fmt_pct4(val / 100), ha="center", va="top", fontsize=9,
                fontweight="bold", color="white")

    lock_bp = comp.get("lock_in_cost_bp", 0)
    p_locked = comp.get("p_locked", 0)
    ax.axhline(0, color="black", linewidth=0.8)
    ax.set_ylabel("CEW vs No-Tax (%)", fontsize=9)
    ax.set_title(
        f"Figure 4.2.2a — Full Welfare Comparison — WDT vs CGT\n"
        f"γ=2 | P(locked in) = {fmt_pct1(p_locked)} | "
        f"WDT advantage = {comp.get('wdt_adv_with_lock_bp', 0):+.2f} bp",
        fontsize=9, fontweight="bold"
    )
    ax.yaxis.set_major_formatter(mtick.PercentFormatter(decimals=4))
    ax.grid(axis="y", linestyle="--", alpha=0.4)
    ax.spines["top"].set_visible(False); ax.spines["right"].set_visible(False)
    fig.tight_layout()
    _save(fig, out_dir, "wfr_fig_4_2_2a_full_comparison.png")


def fig_4_2_2b_sensitivity_gain(m3: dict, out_dir: Path):
    sens = m3["sens_gain"]
    gr    = [r["gain_ratio"] * 100 for r in sens]
    costs = [r.get("lock_in_cost_bp", 0) or 0 for r in sens]
    p_loc = [(r.get("p_locked", 0) or 0) * 100 for r in sens]

    apply_style()
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=FIG_WIDE)
    fig.suptitle("Figure 4.2.2b — Sensitivity — Embedded Gain Ratio G/V", fontsize=11, fontweight="bold")

    ax1.plot(gr, costs, color="#8e44ad", marker="o", linewidth=2, markersize=6)
    ax1.set_xlabel("Embedded gain as % of asset value (G/V)", fontsize=9)
    ax1.set_ylabel("Lock-in welfare cost (basis points)", fontsize=9)
    ax1.set_title("Welfare cost of CGT lock-in", fontsize=9)
    ax1.grid(axis="y", linestyle="--", alpha=0.4)
    ax1.spines["top"].set_visible(False); ax1.spines["right"].set_visible(False)

    ax2.plot(gr, p_loc, color="#c0392b", marker="s", linewidth=2, markersize=6)
    ax2.set_xlabel("Embedded gain as % of asset value (G/V)", fontsize=9)
    ax2.set_ylabel("P(agent locked in) — % of return states", fontsize=9)
    ax2.set_title("Probability of being locked in", fontsize=9)
    ax2.yaxis.set_major_formatter(mtick.PercentFormatter())
    ax2.grid(axis="y", linestyle="--", alpha=0.4)
    ax2.spines["top"].set_visible(False); ax2.spines["right"].set_visible(False)

    fig.tight_layout()
    _save(fig, out_dir, "wfr_fig_4_2_2b_sensitivity_gain.png")


def fig_4_2_2c_sensitivity_T(m3: dict, out_dir: Path):
    sens  = m3["sens_T"]
    T_vals = [r["T"] for r in sens]
    costs  = [r.get("lock_in_cost_bp", 0) or 0 for r in sens]
    indiff = [(r.get("r_B_indiff", 0) or 0) * 100 for r in sens]

    apply_style()
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=FIG_WIDE)
    fig.suptitle("Figure 4.2.2c — Sensitivity — Remaining Holding Period T", fontsize=11, fontweight="bold")
    ax1.plot(T_vals, costs, color="#8e44ad", marker="o", linewidth=2, markersize=6)
    ax1.set_xlabel("Remaining holding period T (years)", fontsize=9)
    ax1.set_ylabel("Lock-in welfare cost (basis points)", fontsize=9)
    ax1.set_title("Welfare cost vs holding period", fontsize=9)
    ax1.grid(axis="y", linestyle="--", alpha=0.4)
    ax1.spines["top"].set_visible(False); ax1.spines["right"].set_visible(False)

    ax2.plot(T_vals, indiff, color="#c0392b", marker="s", linewidth=2, markersize=6)
    ax2.set_xlabel("Remaining holding period T (years)", fontsize=9)
    ax2.set_ylabel("Indifference return r_B* (%)", fontsize=9)
    ax2.set_title("Indifference return converges to r_A as T→∞", fontsize=9)
    ax2.yaxis.set_major_formatter(mtick.PercentFormatter(decimals=2))
    ax2.grid(axis="y", linestyle="--", alpha=0.4)
    ax2.spines["top"].set_visible(False); ax2.spines["right"].set_visible(False)

    fig.tight_layout()
    _save(fig, out_dir, "wfr_fig_4_2_2c_sensitivity_T.png")


# ─────────────────────────────────────────────────────────────────────────────
# MODULE 4 CHARTS
# ─────────────────────────────────────────────────────────────────────────────

def fig_4_3_2_concentration_path(m4: dict, out_dir: Path):
    conc    = m4["concentration"]["scenario"]
    years   = conc["years"]
    paths   = conc["systems"]
    tiers   = m4["tiers"]
    years_f = [years[0] - 1] + list(years)

    systems_to_plot = ["symmetric_wdt", "progressive_wdt", "stock_wealth", "income"]
    apply_style()
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=FIG_PAIR_T)
    fig.suptitle(
        "Figure 4.3.2 — Wealth Concentration Path\n"
        "(Great-tier / Poor-tier wealth ratio; higher = more concentrated)",
        fontsize=11, fontweight="bold"
    )
    for name in systems_to_plot:
        if name not in paths:
            continue
        great = paths[name].get("Great", [])
        poor  = paths[name].get("Poor",  [])
        if not great:
            continue
        ratio = [g / p if (p and p > 0) else np.nan for g, p in zip(great, poor)]
        label = "Progressive WDT" if name == "progressive_wdt" else SYSTEM_LABELS.get(name, name)
        color = COLOURS.get(name, "grey")
        ax1.plot(years_f, ratio, color=color, linewidth=1.8, label=label)

    ax1.set_xlabel("Year", fontsize=9); ax1.set_ylabel("Great / Poor wealth ratio", fontsize=9)
    ax1.set_title("Wealth ratio over time", fontsize=9)
    ax1.legend(fontsize=8); ax1.grid(linestyle="--", alpha=0.3)
    ax1.spines["top"].set_visible(False); ax1.spines["right"].set_visible(False)

    for tier in tiers:
        for name in ["progressive_wdt", "stock_wealth"]:
            if name not in paths:
                continue
            path = paths[name].get(tier["name"])
            if not path:
                continue
            W0 = tier["W0"]
            norm = [v / W0 if v else np.nan for v in path]
            label = f"{tier['name']} ({'WDT' if name=='progressive_wdt' else 'Stock WTax'})"
            ls    = "-" if name == "progressive_wdt" else "--"
            ax2.plot(years_f, norm, color=TIER_COLOURS[tier["name"]], linewidth=1.5,
                     linestyle=ls, label=label, alpha=0.85)

    ax2.set_xlabel("Year", fontsize=9)
    ax2.set_ylabel("Wealth (normalised to W₀ = 1)", fontsize=9)
    ax2.set_title("Wealth growth by tier: WDT (solid) vs Stock WTax (dashed)", fontsize=9)
    ax2.legend(fontsize=7, ncol=2); ax2.grid(linestyle="--", alpha=0.3)
    ax2.spines["top"].set_visible(False); ax2.spines["right"].set_visible(False)

    fig.tight_layout()
    _save(fig, out_dir, "wfr_fig_4_3_2_concentration_path.png")


def fig_4_3_3_tier_cew(m4: dict, out_dir: Path):
    tiers_ord   = ["Poor", "Ok", "Good", "Great"]
    systems_ord = ["symmetric_wdt", "progressive_wdt", "stock_wealth", "income", "cgt", "consumption"]
    sys_short   = {
        "symmetric_wdt": "Sym. WDT", "progressive_wdt": "Prog. WDT",
        "stock_wealth":  "Stock W.",  "income": "Income",
        "cgt":           "CGT",       "consumption": "Consump.",
    }
    bar_colours = {
        "symmetric_wdt": COLOURS["symmetric_wdt"], "progressive_wdt": "#0d3d6b",
        "stock_wealth":  COLOURS["stock_wealth"],  "income": COLOURS["income"],
        "cgt":           COLOURS["cgt"],           "consumption": COLOURS["consumption"],
    }
    tw   = m4["tier_welfare"]
    tmeta = {t["name"]: t for t in m4["tiers"]}

    n_sys = len(systems_ord); n_tiers = len(tiers_ord)
    matrix = np.full((n_sys, n_tiers), np.nan)
    for j, tn in enumerate(tiers_ord):
        for i, name in enumerate(systems_ord):
            if name == "progressive_wdt":
                v = tw[tn].get("cew_progressive")
            else:
                v = tw[tn]["systems"].get(name, {}).get("cew")
            if v is not None:
                matrix[i, j] = v * 100

    apply_style(grid=False)
    fig = plt.figure(figsize=(14, 6))
    gs  = fig.add_gridspec(1, 2, width_ratios=[1.1, 1.6], wspace=0.35)
    ax_heat = fig.add_subplot(gs[0])
    ax_bar  = fig.add_subplot(gs[1])

    fig.suptitle("Figure 4.3.3 — CEW by Tier and Tax System\nγ=2 | Revenue-equivalent",
                 fontsize=11, fontweight="bold")

    vmax = max(abs(np.nanmin(matrix)), abs(np.nanmax(matrix)))
    im = ax_heat.imshow(matrix, aspect="auto", cmap="RdBu", vmin=-vmax, vmax=vmax, origin="upper")
    for i in range(n_sys):
        for j in range(n_tiers):
            val = matrix[i, j]
            if not np.isnan(val):
                ax_heat.text(j, i, f"{val:.3f}%", ha="center", va="center", fontsize=7.5,
                             fontweight="bold", color="white" if abs(val) > vmax * 0.55 else "black")

    ax_heat.set_xticks(range(n_tiers))
    ax_heat.set_xticklabels([
        f"{tn}\n({tmeta[tn]['bracket_label']})\nW₀={fmt_gbp_m(tmeta[tn]['W0'], dp=1)}\n"
        f"{tmeta[tn]['differential']*100:+.2f}pp"
        for tn in tiers_ord
    ], fontsize=7.5)
    ax_heat.set_yticks(range(n_sys))
    ax_heat.set_yticklabels([sys_short[s] for s in systems_ord], fontsize=8)
    ax_heat.set_title("CEW heatmap (% vs no-tax)\nRed = higher cost, Blue = lower cost", fontsize=9)
    cbar = fig.colorbar(im, ax=ax_heat, fraction=0.046, pad=0.04)
    cbar.set_label("CEW (%)", fontsize=8); cbar.ax.tick_params(labelsize=7)

    x     = np.arange(n_tiers)
    width = 0.13
    offs  = np.linspace(-(n_sys - 1) / 2 * width, (n_sys - 1) / 2 * width, n_sys)
    for i, name in enumerate(systems_ord):
        ax_bar.bar(x + offs[i], matrix[i, :], width, color=bar_colours[name],
                   label=sys_short[name], alpha=0.85, edgecolor="white", linewidth=0.5)
    x_labels = [f"{tn}\n({tmeta[tn]['bracket_label']}, W₀={fmt_gbp_m(tmeta[tn]['W0'], dp=1)})"
                for tn in tiers_ord]
    ax_bar.axhline(0, color="black", linewidth=0.8)
    ax_bar.set_xticks(x); ax_bar.set_xticklabels(x_labels, fontsize=8)
    ax_bar.set_ylabel("CEW (% vs no-tax)", fontsize=9)
    ax_bar.yaxis.set_major_formatter(mtick.PercentFormatter(decimals=3))
    ax_bar.set_title("Grouped bars: CEW by tier and system", fontsize=9)
    ax_bar.legend(fontsize=7.5, loc="upper right", ncol=2,
                  frameon=True, facecolor="white", edgecolor=C_DARK, framealpha=1.0)
    ax_bar.grid(axis="y", linestyle="--", alpha=0.4)
    ax_bar.spines["top"].set_visible(False); ax_bar.spines["right"].set_visible(False)

    fig.subplots_adjust(top=0.85, bottom=0.20)
    _save(fig, out_dir, "wfr_fig_4_3_3_tier_cew.png")


def fig_4_3_4_incidence(m4: dict, out_dir: Path):
    tiers_ord = ["Poor", "Ok", "Good", "Great"]
    tmeta     = {t["name"]: t for t in m4["tiers"]}
    tw        = m4["tier_welfare"]
    apply_style()
    fig, ax = plt.subplots(figsize=FIG_WIDE_L)
    for name in SYSTEMS:
        burdens = [tw[t]["systems"].get(name, {}).get("et_pct_W0") for t in tiers_ord]
        x_labels = [f"{t}\n({tmeta[t]['bracket_label']})" for t in tiers_ord]
        ax.plot(x_labels, [v if v else np.nan for v in burdens],
                color=COLOURS.get(name, "grey"), marker="o", linewidth=2, markersize=8,
                label=SYSTEM_LABELS.get(name, name))
    ax.set_xlabel("Tier", fontsize=9); ax.set_ylabel("Expected tax as % of W₀", fontsize=9)
    ax.set_title("Figure 4.3.4 — Distributional Incidence — Tax Burden by Tier",
                 fontsize=10, fontweight="bold")
    ax.yaxis.set_major_formatter(mtick.PercentFormatter(decimals=3))
    ax.legend(fontsize=8); ax.grid(axis="y", linestyle="--", alpha=0.4)
    ax.spines["top"].set_visible(False); ax.spines["right"].set_visible(False)
    fig.tight_layout()
    _save(fig, out_dir, "wfr_fig_4_3_4_incidence.png")


def fig_4_3_5_envelope_binding(m4: dict, out_dir: Path):
    env = m4["envelope"]
    tiers_ord = ["Poor", "Ok", "Good", "Great"]
    apply_style()
    fig, axes = plt.subplots(2, 2, figsize=FIG_QUAD, sharey=False)
    fig.suptitle(
        "Figure 4.3.5 — Lifetime Contribution Envelope — Slack Over Time\n"
        "(Slack = cumulative tax − cumulative refunds; zero = envelope binds)",
        fontsize=11, fontweight="bold"
    )
    for ax, tn in zip(axes.flat, tiers_ord):
        er     = env[tn]
        years  = [y["year"] for y in er["year_log"]]
        slacks = [y["envelope_slack"] for y in er["year_log"]]
        ax.fill_between(years, slacks, 0, alpha=0.3, color=TIER_COLOURS[tn])
        ax.plot(years, slacks, color=TIER_COLOURS[tn], linewidth=2, label="Envelope slack")
        ax.axhline(0, color="black", linewidth=0.9, linestyle="--")
        if er.get("ever_binds"):
            for yr in er.get("binding_years", []):
                ax.axvline(yr, color="red", linewidth=1.0, linestyle=":", alpha=0.7)
        note = (f"Min slack: {fmt_gbp_m(er['min_slack'])}\n"
                + ("BINDS in: " + str(er["binding_years"]) if er.get("ever_binds") else "Never binds"))
        ax.set_title(f"{tn} tier\n{note}", fontsize=9, fontweight="bold", color=TIER_COLOURS[tn])
        ax.set_xlabel("Year", fontsize=8); ax.set_ylabel("Envelope slack (£m)", fontsize=8)
        ax.tick_params(labelsize=7); ax.grid(axis="y", linestyle="--", alpha=0.3)
        ax.spines["top"].set_visible(False); ax.spines["right"].set_visible(False)
    fig.tight_layout()
    _save(fig, out_dir, "wfr_fig_4_3_5_envelope_binding.png")


def fig_4_3_6_corner_check(m4: dict, out_dir: Path):
    tw  = m4["tier_welfare"]
    cr  = m4["corner_check"]
    systems_ord = ["symmetric_wdt", "stock_wealth", "income", "cgt", "consumption", "progressive_wdt"]
    sys_short   = {
        "symmetric_wdt": "Sym. WDT", "progressive_wdt": "Prog. WDT",
        "stock_wealth":  "Stock W.",  "income": "Income",
        "cgt":           "CGT",       "consumption": "Consump.",
    }
    bar_colours = {
        "symmetric_wdt": COLOURS["symmetric_wdt"], "progressive_wdt": "#0d3d6b",
        "stock_wealth":  COLOURS["stock_wealth"],  "income": COLOURS["income"],
        "cgt":           COLOURS["cgt"],           "consumption": COLOURS["consumption"],
    }
    alphas = {"corner": 0.95, "same_W0": 0.55, "same_diff": 0.30}
    corner_configs = [
        ("corner_A", "Corner A: Great diff (+3.45pp), Poor W₀ (£2.86m)", "Poor",  "Great"),
        ("corner_B", "Corner B: Poor diff (−4.55pp), Great W₀ (£139.6m)", "Great", "Poor"),
    ]
    apply_style()
    fig, axes = plt.subplots(1, 2, figsize=FIG_PAIR_T, sharey=False)
    fig.suptitle(
        "Figure 4.3.6 — Off-Diagonal Spot Check — Decoupling W₀ from Return Differential\n"
        "γ=2 | Dark = corner, medium = diagonal same-W₀, light = diagonal same-diff",
        fontsize=10, fontweight="bold"
    )
    for ax, (key, title, dw0, ddiff) in zip(axes, corner_configs):
        corner = cr.get(key, {})
        x = np.arange(len(systems_ord)); width = 0.25
        cew_c, cew_w0, cew_d = [], [], []
        for name in systems_ord:
            if name == "progressive_wdt":
                cew_c.append((corner.get("cew_progressive") or 0) * 100)
                cew_w0.append((tw.get(dw0, {}).get("cew_progressive") or 0) * 100)
                cew_d.append((tw.get(ddiff, {}).get("cew_progressive") or 0) * 100)
            else:
                cew_c.append((corner.get("systems", {}).get(name, {}).get("cew") or 0) * 100)
                cew_w0.append((tw.get(dw0,   {}).get("systems", {}).get(name, {}).get("cew") or 0) * 100)
                cew_d.append((tw.get(ddiff, {}).get("systems", {}).get(name, {}).get("cew") or 0) * 100)
        colours = [bar_colours[n] for n in systems_ord]
        ax.bar(x - width, cew_c,  width, color=colours, alpha=alphas["corner"],    edgecolor="white", linewidth=0.5)
        ax.bar(x,         cew_w0, width, color=colours, alpha=alphas["same_W0"],   edgecolor="white", linewidth=0.5)
        ax.bar(x + width, cew_d,  width, color=colours, alpha=alphas["same_diff"], edgecolor="white", linewidth=0.5)
        ax.axhline(0, color="black", linewidth=0.8)
        ax.set_xticks(x)
        ax.set_xticklabels([sys_short[s] for s in systems_ord], fontsize=8, rotation=20, ha="right")
        ax.set_ylabel("CEW (% vs no-tax)", fontsize=9)
        ax.yaxis.set_major_formatter(mtick.PercentFormatter(decimals=3))
        ax.set_title(title, fontsize=9, fontweight="bold")
        ax.grid(axis="y", linestyle="--", alpha=0.4)
        ax.spines["top"].set_visible(False); ax.spines["right"].set_visible(False)

    legend_handles = [
        mpatches.Patch(facecolor=C_DARK, alpha=alphas["corner"],    label="Corner (decoupled)"),
        mpatches.Patch(facecolor=C_DARK, alpha=alphas["same_W0"],   label="Diagonal (same W₀)"),
        mpatches.Patch(facecolor=C_DARK, alpha=alphas["same_diff"], label="Diagonal (same diff)"),
    ]
    fig.legend(handles=legend_handles, loc="lower center", bbox_to_anchor=(0.5, 0.0),
               ncol=3, fontsize=8.5, frameon=True, facecolor="white", edgecolor=C_DARK, framealpha=1.0)
    fig.tight_layout(); fig.subplots_adjust(bottom=0.13)
    _save(fig, out_dir, "wfr_fig_4_3_6_corner_check.png")


# ─────────────────────────────────────────────────────────────────────────────
# MODULE 4 PART F CHARTS
# ─────────────────────────────────────────────────────────────────────────────

def fig_7_4a_progressive_vs_flat_extended(m4: dict, out_dir: Path):
    ext   = m4["concentration"]["extended"]
    years = ext["years"]
    paths = ext["systems"]
    co    = ext.get("crossover")
    years_f = [years[0] - 1] + list(years)

    great_flat = paths.get("symmetric_wdt",   {}).get("Great", [])
    poor_flat  = paths.get("symmetric_wdt",   {}).get("Poor",  [])
    great_prog = paths.get("progressive_wdt", {}).get("Great", [])
    poor_prog  = paths.get("progressive_wdt", {}).get("Poor",  [])

    ratio_flat = [g / p if (p and p > 0) else np.nan for g, p in zip(great_flat, poor_flat)]
    ratio_prog = [g / p if (p and p > 0) else np.nan for g, p in zip(great_prog, poor_prog)]

    apply_style()
    fig, ax = plt.subplots(figsize=FIG_WIDE_L)
    fig.suptitle(
        "Figure 7.4a — Concentration Path: Flat vs Progressive WDT — N=73 (1947–2019)\n"
        "Great/Poor wealth ratio; rates carried forward from Part D",
        fontsize=11, fontweight="bold"
    )
    ax.plot(years_f, ratio_flat, color=COLOURS["symmetric_wdt"],  linewidth=2, label="Flat WDT")
    ax.plot(years_f, ratio_prog, color="#0d3d6b", linewidth=2, linestyle="--", label="Progressive WDT")

    n30_year = years[0] + 29
    ax.axvline(n30_year, color=C_ANNOTATION, linewidth=1.0, linestyle=":", label=f"30yr anchor ({n30_year})")

    gap_n73 = (ratio_prog[-1] or 0) - (ratio_flat[-1] or 0)
    note    = f"Gap at N=73: {gap_n73:+.1f}×"
    note   += f"\nCrossover: {co['year']}" if co else "\nNo crossover within N=73"
    ax.text(0.02, 0.96, note, transform=ax.transAxes, va="top", ha="left", fontsize=8, color=C_DARK,
            bbox=dict(boxstyle="round", facecolor="white", edgecolor=C_GRID, alpha=0.9))

    ax.set_xlabel("Year", fontsize=9); ax.set_ylabel("Great / Poor wealth ratio", fontsize=9)
    ax.legend(fontsize=8, loc="lower right"); ax.grid(linestyle="--", alpha=0.3)
    ax.spines["top"].set_visible(False); ax.spines["right"].set_visible(False)
    fig.tight_layout()
    _save(fig, out_dir, "wfr_fig_7_4a_progressive_vs_flat_extended.png")


def fig_7_4b_full_concentration_extended(m4: dict, out_dir: Path):
    ext    = m4["concentration"]["extended"]
    years  = ext["years"]
    paths  = ext["systems"]
    tiers  = m4["tiers"]
    years_f = [years[0] - 1] + list(years)
    n30    = years[0] + 29
    systems_to_plot = ["symmetric_wdt", "progressive_wdt", "stock_wealth", "income"]

    apply_style()
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=FIG_PAIR_T)
    fig.suptitle("Figure 7.4b — Full Concentration Path, All Systems — N=73 (1947–2019)",
                 fontsize=11, fontweight="bold")

    for name in systems_to_plot:
        if name not in paths:
            continue
        great = paths[name].get("Great", [])
        poor  = paths[name].get("Poor",  [])
        if not great:
            continue
        ratio = [g / p if (p and p > 0) else np.nan for g, p in zip(great, poor)]
        label = "Progressive WDT" if name == "progressive_wdt" else SYSTEM_LABELS.get(name, name)
        color = "#0d3d6b" if name == "progressive_wdt" else COLOURS.get(name, "grey")
        ax1.plot(years_f, ratio, color=color, linewidth=1.6, label=label)

    ax1.axvline(n30, color=C_ANNOTATION, linewidth=1.0, linestyle=":", label=f"N=30 ({n30})")
    ax1.set_xlabel("Year", fontsize=9); ax1.set_ylabel("Great / Poor wealth ratio", fontsize=9)
    ax1.set_title("Wealth ratio over time, all systems", fontsize=9)
    ax1.legend(fontsize=7.5); ax1.grid(linestyle="--", alpha=0.3)
    ax1.spines["top"].set_visible(False); ax1.spines["right"].set_visible(False)

    for tier in tiers:
        for name in ["progressive_wdt", "stock_wealth"]:
            if name not in paths:
                continue
            path = paths[name].get(tier["name"])
            if not path:
                continue
            norm  = [v / tier["W0"] if v else np.nan for v in path]
            label = f"{tier['name']} ({'WDT' if name=='progressive_wdt' else 'Stock WTax'})"
            ls    = "-" if name == "progressive_wdt" else "--"
            ax2.plot(years_f, norm, color=TIER_COLOURS[tier["name"]], linewidth=1.4,
                     linestyle=ls, label=label, alpha=0.85)

    ax2.axvline(n30, color=C_ANNOTATION, linewidth=1.0, linestyle=":")
    ax2.set_xlabel("Year", fontsize=9); ax2.set_ylabel("Wealth (normalised to W₀=1)", fontsize=9)
    ax2.set_title("Wealth growth by tier: WDT (solid) vs Stock WTax (dashed)", fontsize=9)
    ax2.legend(fontsize=7, ncol=2); ax2.grid(linestyle="--", alpha=0.3)
    ax2.spines["top"].set_visible(False); ax2.spines["right"].set_visible(False)

    fig.tight_layout()
    _save(fig, out_dir, "wfr_fig_7_4b_full_concentration_extended.png")


# ─────────────────────────────────────────────────────────────────────────────
# MODULE 5 CHARTS
# ─────────────────────────────────────────────────────────────────────────────

def fig_4_5_1a_revenue_target(m5: dict, out_dir: Path):
    rev_data = m5["sweep_a_revenue"]
    target_pcts = sorted(rev_data.keys(), key=float)
    gamma    = "2.0"
    dist_labels = {"A": "Ver. A (Empirical)", "B": "Ver. B (Idealised)"}

    apply_style()
    fig, axes = plt.subplots(1, 2, figsize=FIG_PAIR, sharey=True)
    fig.suptitle("Figure 4.5.1a — CEW vs Revenue Target (E[T] as % of W₀)\nγ=2 | All systems revenue-equivalent",
                 fontsize=11, fontweight="bold")

    for ax, dlabel in zip(axes, ["A", "B"]):
        for name in SYSTEMS:
            cews = [rev_data.get(pct, {}).get(dlabel, {}).get(gamma, {}).get(name) for pct in target_pcts]
            ax.plot([float(p) for p in target_pcts],
                    [v * 100 if v is not None else np.nan for v in cews],
                    color=COLOURS[name], marker=MARKERS[name], linewidth=2, markersize=7,
                    label=SYSTEM_LABELS[name])
        ax.axhline(0, color="black", linewidth=0.7, linestyle="--", alpha=0.5)
        ax.yaxis.set_major_formatter(mtick.PercentFormatter(decimals=2))
        ax.set_xticks([float(p) for p in target_pcts])
        ax.set_xticklabels([f"{float(p):.0f}%" for p in target_pcts])
        _style_ax(ax, dist_labels[dlabel], xlabel="Revenue target E[T] (% of W₀)", ylabel="CEW (%)")

    axes[1].legend(fontsize=8, loc="lower left")
    fig.tight_layout()
    _save(fig, out_dir, "wfr_fig_4_5_1a_revenue_target.png")


def fig_4_5_1b_w0_sensitivity(m5: dict, out_dir: Path):
    w0_data = m5["sweep_a_w0"]
    W0_vals = sorted(w0_data.keys(), key=float)
    apply_style()
    fig, ax = plt.subplots(figsize=FIG_WIDE)
    fig.suptitle("Figure 4.5.1b — CEW vs Initial Wealth W₀\nE[T]=2% of W₀ | γ=2 | Ver. A",
                 fontsize=11, fontweight="bold")
    for name in SYSTEMS:
        cews = [w0_data.get(w, {}).get(name) for w in W0_vals]
        ax.plot([float(w) for w in W0_vals],
                [v * 100 if v is not None else np.nan for v in cews],
                color=COLOURS[name], marker=MARKERS[name], linewidth=2, markersize=7,
                label=SYSTEM_LABELS[name])
    ax.axhline(0, color="black", linewidth=0.7, linestyle="--", alpha=0.5)
    ax.yaxis.set_major_formatter(mtick.PercentFormatter(decimals=2))
    ax.set_xlabel("Initial wealth W₀ (£m)", fontsize=9)
    ax.set_ylabel("CEW (%)", fontsize=9)
    ax.legend(fontsize=8, loc="lower right")
    ax.grid(axis="y", linestyle="--", alpha=0.35)
    ax.spines["top"].set_visible(False); ax.spines["right"].set_visible(False)
    fig.tight_layout()
    _save(fig, out_dir, "wfr_fig_4_5_1b_w0_sensitivity.png")


def fig_4_5_2a_start_year_distribution(m5: dict, out_dir: Path):
    sy_data = m5["sweep_b_start_year"]
    all_yrs = sorted(sy_data.keys())
    all_cews = {}
    for name in SYSTEMS:
        all_cews[name] = [
            sy_data[yr][name] * 100
            for yr in all_yrs
            if sy_data[yr].get(name) is not None
        ]

    apply_style()
    fig, ax = plt.subplots(figsize=FIG_WIDE)
    fig.suptitle("Figure 4.5.2a — CEW Distribution Across All Start Years (1947–2019)\n"
                 "30-year windows | E[T]=2% | γ=2",
                 fontsize=11, fontweight="bold")

    positions = list(range(1, len(SYSTEMS) + 1))
    bp = ax.boxplot(
        [all_cews[n] for n in SYSTEMS], positions=positions, patch_artist=True,
        widths=0.5, medianprops=dict(color="white", linewidth=2),
        whiskerprops=dict(linewidth=1.2), capprops=dict(linewidth=1.2),
        flierprops=dict(marker=".", markersize=4, alpha=0.5),
    )
    for patch, name in zip(bp["boxes"], SYSTEMS):
        patch.set_facecolor(COLOURS[name]); patch.set_alpha(0.8)
    ax.set_xticks(positions)
    ax.set_xticklabels([SYSTEM_LABELS[n].replace(" (", "\n(").replace(" Tax", "\nTax") for n in SYSTEMS], fontsize=8)
    ax.yaxis.set_major_formatter(mtick.PercentFormatter(decimals=2))
    ax.set_ylabel("CEW (%)", fontsize=9)
    ax.grid(axis="y", linestyle="--", alpha=0.35)
    ax.spines["top"].set_visible(False); ax.spines["right"].set_visible(False)
    fig.tight_layout()
    _save(fig, out_dir, "wfr_fig_4_5_2a_start_year_distribution.png")


def fig_4_5_2b_timeseries(m5: dict, out_dir: Path):
    sy_data = m5["sweep_b_start_year"]
    years   = sorted([int(y) for y in sy_data.keys()])
    apply_style()
    fig, ax = plt.subplots(figsize=FIG_WIDE_L)
    fig.suptitle("Figure 4.5.2b — CEW by Start Year — All Historical Windows\nE[T]=2% | γ=2 | 30-year windows",
                 fontsize=11, fontweight="bold")
    for name in SYSTEMS:
        cews = [sy_data.get(str(yr), {}).get(name) for yr in years]
        ax.plot(years, [v * 100 if v is not None else np.nan for v in cews],
                color=COLOURS[name], linewidth=1.5, label=SYSTEM_LABELS[name], alpha=0.85)
    ax.axvline(2000, color="black", linewidth=1.0, linestyle="--", alpha=0.6, label="Canonical (2000)")
    ax.yaxis.set_major_formatter(mtick.PercentFormatter(decimals=2))
    ax.set_xlabel("Scenario start year", fontsize=9); ax.set_ylabel("CEW (%)", fontsize=9)
    ax.legend(fontsize=8, loc="lower right")
    ax.grid(axis="y", linestyle="--", alpha=0.3)
    ax.spines["top"].set_visible(False); ax.spines["right"].set_visible(False)
    fig.tight_layout()
    _save(fig, out_dir, "wfr_fig_4_5_2b_timeseries.png")


def fig_4_5_3x_param(m5: dict, out_dir: Path, param_name: str,
                      filename: str, chart_num: str, param_label: str):
    param_data = m5["sweep_c_params"].get(param_name, {})
    if not param_data:
        return
    W0_keys    = sorted(param_data.keys(), key=float)
    param_vals = sorted(list(param_data[W0_keys[0]].keys()), key=float)

    W0_colours = {
        "3.0": "#c0392b", "10.0": "#e67e22", "30.0": "#2ecc71",
        "100.0": "#1a6fad", "150.0": "#8e44ad",
    }
    apply_style()
    fig, ax = plt.subplots(figsize=FIG_WIDE)
    for w in W0_keys:
        gaps = [param_data[w].get(str(pval)) for pval in param_vals]
        colour = W0_colours.get(w, "#555555")
        ax.plot(param_vals, [v if v is not None else np.nan for v in gaps],
                color=colour, marker="o", linewidth=2, markersize=6, label=f"W₀=£{float(w):.0f}m")

    ax.axhline(0, color="black", linewidth=0.8, linestyle="--", alpha=0.6)
    ax.set_xlabel(param_label, fontsize=9)
    ax.set_ylabel("Flat WDT − Progressive WDT (bp)\nPositive = flat cheaper", fontsize=9)
    ax.set_title(f"{chart_num} Progressive vs Flat WDT — {param_label} sensitivity\n"
                 f"Revenue-equivalent | E[T]=2% of W₀ | γ=2",
                 fontsize=10, fontweight="bold")
    ax.legend(fontsize=8)
    ax.grid(axis="y", linestyle="--", alpha=0.35)
    ax.spines["top"].set_visible(False); ax.spines["right"].set_visible(False)
    fig.tight_layout()
    _save(fig, out_dir, filename)


# ─────────────────────────────────────────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────────────────────────────────────────

def main(json_path: Path = None, out_dir: Path = None, modules: list = None):
    if json_path is None:
        json_path = Path(__file__).parent / "OUTPUTS" / "WFR" / "wfr" / "wfr_results.json"
    if out_dir is None:
        out_dir = json_path.parent / "charts"
    if modules is None:
        modules = [1, 2, 3, 4, 5]

    if not json_path.exists():
        print(f"ERROR: results file not found: {json_path}", file=sys.stderr)
        print("Run wfr_core.py first.", file=sys.stderr)
        sys.exit(1)

    out_dir.mkdir(parents=True, exist_ok=True)
    print(f"Reading: {json_path}")
    with open(json_path, encoding="utf-8") as fh:
        data = json.load(fh)

    params = data["meta"]["params"]
    scenario_start = params.get("scenario_start_year", 2000)
    N = params.get("canonical_N", 30)
    target_et = params.get("target_et_frac", 0.02)

    if 1 in modules and "module1" in data:
        print("Module 1 charts...")
        m1 = data["module1"]
        fig_3_1a_cew_by_gamma(m1, out_dir, target_et)
        fig_3_1b_wdt_advantage(m1, out_dir)
        fig_3_1c_annual_tax(m1, out_dir, scenario_start, N)
        fig_3_2_variance(m1, out_dir, target_et)

    if 2 in modules and "module2" in data:
        print("Module 2 charts...")
        m2 = data["module2"]
        fig_4_1a_rate_function(m2, out_dir)
        fig_4_1b_flat_vs_progressive(m2, out_dir)
        fig_4_1c_leverage(m2, out_dir)
        fig_4_1d_asymmetry(m2, out_dir)

    if 3 in modules and "module3" in data:
        print("Module 3 charts...")
        m3 = data["module3"]
        fig_4_2_1_lock_in_threshold(m3, out_dir)
        fig_4_2_2a_full_comparison(m3, out_dir)
        fig_4_2_2b_sensitivity_gain(m3, out_dir)
        fig_4_2_2c_sensitivity_T(m3, out_dir)

    if 4 in modules and "module4" in data:
        print("Module 4 charts...")
        m4 = data["module4"]
        fig_4_3_2_concentration_path(m4, out_dir)
        fig_4_3_3_tier_cew(m4, out_dir)
        fig_4_3_4_incidence(m4, out_dir)
        fig_4_3_5_envelope_binding(m4, out_dir)
        if m4.get("corner_check"):
            fig_4_3_6_corner_check(m4, out_dir)
        # Part F
        if data["module4"]["concentration"]["extended"].get("years"):
            fig_7_4a_progressive_vs_flat_extended(m4, out_dir)
            fig_7_4b_full_concentration_extended(m4, out_dir)

    if 5 in modules and "module5" in data:
        print("Module 5 charts...")
        m5 = data["module5"]
        fig_4_5_1a_revenue_target(m5, out_dir)
        fig_4_5_1b_w0_sensitivity(m5, out_dir)
        fig_4_5_2a_start_year_distribution(m5, out_dir)
        fig_4_5_2b_timeseries(m5, out_dir)
        param_configs = [
            ("tau_0", "wfr_fig_4_5_3a_tau0.png", "4.5.3a", "τ₀ (entry rate)"),
            ("tau_m", "wfr_fig_4_5_3b_taum.png", "4.5.3b", "τ_m (ceiling rate)"),
            ("k",     "wfr_fig_4_5_3c_k.png",    "4.5.3c", "k (steepness per £m)"),
            ("W_min", "wfr_fig_4_5_3d_wmin.png",  "4.5.3d", "W_min (£m)"),
        ]
        for pname, fname, cnum, plabel in param_configs:
            fig_4_5_3x_param(m5, out_dir, pname, fname, cnum, plabel)

    print(f"\n✓ Charts written to: {out_dir}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="WFR Chart Generator")
    parser.add_argument("--json",    type=Path,          help="Path to wfr_results.json")
    parser.add_argument("--out",     type=Path,          help="Output directory for PNGs")
    parser.add_argument("--modules", nargs="+", type=int, choices=[1,2,3,4,5])
    args = parser.parse_args()
    main(json_path=args.json, out_dir=args.out, modules=args.modules)
