"""
module5_sweeps.py
=================
Module 5: Welfare Sweep Analysis

Three independent sweep axes, each isolating a distinct source of
variation in the welfare comparison:
E.1 Revenue target (E[T] as % of W₀)
    Question: how sensitive are the welfare rankings and magnitudes to
    the assumed revenue level? Runs the full Module 1 comparison at
    E[T] = 1%, 2%, 3%, 4%, 5% of W₀. All five systems. Both distributions.
    γ = 1, 2, 4. This sweep is parameter-free — it establishes the structural
    result across the realistic range of real-world effective tax burdens.

E.2 Start year (worst-case scenario analysis)
    Question: which historical sequences are worst-case for each system,
    and does the WDT's structural advantage survive them? Runs the Module 1
    comparison for every possible 30-year window within the 73-year series
    (53 start years: 1947–2019 minus the 30-year tail). Reports full
    distribution of CEW outcomes per system, plus a curated worst-case table
    for the six historically adverse start years identified in the TOML.
    Revenue target fixed at 2% of W₀ (canonical). γ = 2 (central case).

E.3 Rate parameter sensitivity
    Question: across the feasible parameter space (τ₀, τ_m, k, W_min), when
    does the progressive WDT have materially higher welfare cost than the
    revenue-equivalent flat WDT, and when does it not? Single-parameter
    sweeps holding others at canonical values, run at W₀ = £10m (mid-range)
    and W₀ = £100m (high wealth, logistic well above floor). Revenue target
    2% of W₀. γ = 2. Uses the scaled progressive rate function so comparison
    is always revenue-equivalent.

Outputs → OUTPUTS/WFR/module5/
    Charts:  E.1   m5_fig_e1_revenue_target.png
             E.1b  m5_fig_e1b_w0_sensitivity.png
             E.2.1 m5_fig_e2a_start_year_distribution.png
             E.2.2 m5_fig_e2b_timeseries.png
             E.3.1 m5_fig_e3a_tau0.png
             E.3.2 m5_fig_e3b_taum.png
             E.3.3 m5_fig_e3c_k.png
             E.3.4 m5_fig_e3d_wmin.png

"""

import os
import math
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
from pathlib import Path
from scipy.optimize import brentq
from dataclasses import dataclass
from typing import Optional

from welfare_paths import TOML_PATH, module_output_dir
from welfare_core import (
    load_params,
    ReturnDistribution,
    make_empirical_distribution_scenario,
    make_idealised_distribution_scenario,
    make_empirical_distribution_for_start,
    make_scenario_sequence,
    run_welfare_comparison,
    consumption_equiv_welfare,
    expected_utility,
    expected_tax,
    tax_symmetric_flat,
    SYSTEM_LABELS,
    get_tax_fn,
    solve_revenue_equivalent_rate,
)

from welfare_progressive import (
    ProgressiveRateFunction,
    expected_utility_progressive,
    expected_tax_progressive,
)

from wdt_md import MdDoc, md_table, LEFT, RIGHT, CENTER
from wdt_fmt import fmt_pct, fmt_pct0, fmt_pct4, fmt_gbp_m, today_iso
from wdt_style import (
    apply_style, save_fig,
    FIG_PAIR, FIG_WIDE, FIG_WIDE_L, FIG_QUAD,
    DPI_SCREEN,
)

OUTPUT_DIR = module_output_dir("module5")

# ─────────────────────────────────────────────────────────────────────────────
# CONSTANTS
# ─────────────────────────────────────────────────────────────────────────────

W0_BASE   = 1.0      # normalised (Sweep A)
GAMMA_CEN = 2.0      # central risk aversion

SYSTEMS_ORD = ["symmetric_wdt", "stock_wealth", "income", "cgt", "consumption"]

COLOURS = {
    "symmetric_wdt" : "#1a6fad",
    "stock_wealth"  : "#c0392b",
    "income"        : "#e67e22",
    "cgt"           : "#f1c40f",
    "consumption"   : "#7f8c8d",
}
MARKERS = {
    "symmetric_wdt" : "o",
    "stock_wealth"  : "s",
    "income"        : "^",
    "cgt"           : "D",
    "consumption"   : "P",
}


# ─────────────────────────────────────────────────────────────────────────────
# SCALED PROGRESSIVE RATE FUNCTION
# ─────────────────────────────────────────────────────────────────────────────

class ScaledProgressiveRateFunction(ProgressiveRateFunction):
    """
    ProgressiveRateFunction with a uniform scale factor applied to every
    effective rate call. Used to revenue-match the progressive system to an
    arbitrary target without altering the shape of progression.

    scale = 1.0 recovers the canonical logistic.
    scale > 1.0 raises all rates proportionally (hits higher revenue target).
    scale < 1.0 lowers all rates (hits lower revenue target).

    Preserves structure: τ_eff_scaled(W0, W1) = scale × τ_eff(W0, W1).
    The ratio of rates at any two wealth levels is unchanged by scaling,
    so the relative progressivity is invariant. Only the level shifts.
    """

    def __init__(self, tau0, taum, k, W_min, scale=1.0):
        super().__init__(tau0, taum, k, W_min)
        self.scale = scale

    def effective_rate(self, W0: float, W1: float) -> float:
        return self.scale * super().effective_rate(W0, W1)

    def rate(self, W: float) -> float:
        return self.scale * super().rate(W)


def solve_progressive_scale(
    W0       : float,
    dist     : ReturnDistribution,
    rate_fn  : ProgressiveRateFunction,
    target_et: float,
    scale_lo : float = 1e-4,
    scale_hi : float = 50.0,
) -> float:
    """
    Find the scale factor such that E[T]_progressive(scale) = target_et.
    Returns the scale; caller wraps rate_fn in ScaledProgressiveRateFunction.
    """
    def et_at_scale(s):
        scaled = ScaledProgressiveRateFunction(
            rate_fn.tau0, rate_fn.taum, rate_fn.k, rate_fn.W_min, scale=s
        )
        return expected_tax_progressive(W0, dist, scaled) - target_et

    try:
        lo = et_at_scale(scale_lo)
        hi = et_at_scale(scale_hi)
    except Exception as e:
        raise ValueError(f"Scale solve bounds error: {e}")

    if lo * hi > 0:
        raise ValueError(
            f"Cannot achieve target E[T]={target_et:.4f} for progressive WDT "
            f"within scale ∈ [{scale_lo}, {scale_hi}]. "
            f"E[T] at bounds: [{lo+target_et:.4f}, {hi+target_et:.4f}]."
        )
    return float(brentq(et_at_scale, scale_lo, scale_hi, xtol=1e-10, rtol=1e-10))


def run_progressive_cew(
    W0       : float,
    dist     : ReturnDistribution,
    rate_fn  : ProgressiveRateFunction,
    gamma    : float,
    target_et: float,
) -> dict:
    """
    Revenue-matched progressive WDT CEW.
    Scales the rate function to hit target_et, then computes CEW.
    Returns dict with keys: scale, cew, eu, et, flat_cew, gap_bp.
    flat_cew and gap_bp compare against the flat WDT at the same target_et.
    """
    flat_fn = get_tax_fn("symmetric_wdt")
    eu_notax = expected_utility(W0, dist, flat_fn, 0.0, gamma)

    # Scale progressive to revenue target
    try:
        scale = solve_progressive_scale(W0, dist, rate_fn, target_et)
    except ValueError:
        return {"scale": None, "cew": None, "eu": None, "et": None,
                "flat_cew": None, "gap_bp": None}

    scaled_fn = ScaledProgressiveRateFunction(
        rate_fn.tau0, rate_fn.taum, rate_fn.k, rate_fn.W_min, scale=scale
    )
    eu_prog  = expected_utility_progressive(W0, dist, scaled_fn, gamma)
    cew_prog = consumption_equiv_welfare(eu_prog, eu_notax, gamma)
    et_prog  = expected_tax_progressive(W0, dist, scaled_fn)

    # Flat WDT at same target
    tau_flat = solve_revenue_equivalent_rate(W0, dist, flat_fn, target_et)
    eu_flat  = expected_utility(W0, dist, flat_fn, tau_flat, gamma)
    cew_flat = consumption_equiv_welfare(eu_flat, eu_notax, gamma)

    return {
        "scale"    : scale,
        "cew"      : cew_prog,
        "eu"       : eu_prog,
        "et"       : et_prog,
        "flat_cew" : cew_flat,
        "gap_bp"   : (cew_flat - cew_prog) * 10000,  # positive = flat cheaper
    }


# ─────────────────────────────────────────────────────────────────────────────
# HELPERS
# ─────────────────────────────────────────────────────────────────────────────

def _save(fig, name):
    # DPI_SCREEN (150) is intentional for WFR preview outputs.
    # Use save_fig(fig, path) directly (default DPI_PRINT=300) for publication.
    save_fig(fig, OUTPUT_DIR / name, dpi=DPI_SCREEN)


def _style_ax(ax, title="", xlabel="", ylabel=""):
    ax.set_title(title, fontsize=10, fontweight="bold", pad=6)
    ax.set_xlabel(xlabel, fontsize=9)
    ax.set_ylabel(ylabel, fontsize=9)
    ax.tick_params(labelsize=8)
    ax.grid(axis="y", linestyle="--", alpha=0.35)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)


def _make_dist_for_start(p, start_year, N):
    """
    Build a ReturnDistribution for a given start year.
    Delegates to welfare_core.make_empirical_distribution_for_start so the
    rotation logic is not duplicated here.
    Returns (dist, seq) or (None, None) if start_year is out of range.
    """
    return make_empirical_distribution_for_start(p, start_year, N)


# ─────────────────────────────────────────────────────────────────────────────
# SWEEP A — Revenue target
# ─────────────────────────────────────────────────────────────────────────────

def run_sweep_a(p):
    """
    Sweep E[T] as % of W₀ from 1% to 5%.
    Runs Module 1 comparison (flat systems only) at each target.
    W₀ = 1.0 (normalised). Both distributions. γ = 1, 2, 4.
    Returns nested dict: {target_pct: {dist_label: {gamma: {system: cew}}}}
    """
    sw           = p["sweep"]
    target_pcts  = sw["wfr_target_et_pct"]
    gamma_vals   = sw["wfr_gamma_vals"]
    N            = p["tcm"]["canonical_N"]

    dist_A = make_empirical_distribution_scenario(p, N)
    dist_B = make_idealised_distribution_scenario(p, N)
    dists  = {"A": dist_A, "B": dist_B}

    results = {}
    for pct in target_pcts:
        target_et = (pct / 100.0) * W0_BASE
        results[pct] = {}
        for dlabel, dist in dists.items():
            results[pct][dlabel] = {}
            for gamma in gamma_vals:
                comp = run_welfare_comparison(W0_BASE, dist, gamma, target_et)
                results[pct][dlabel][gamma] = {
                    name: (r.cew if r.cew is not None else None)
                    for name, r in comp.items()
                }
            print(f"  SweepA: E[T]={pct:.0f}%  dist={dlabel}  done")

    return results, dists


def chart_sweep_a(results):
    """
    Two charts side by side — Ver. A and Ver. B.
    x-axis: revenue target (%). y-axis: CEW (%). One line per system.
    γ = 2 (central case).
    """
    gamma = GAMMA_CEN
    dist_labels = ["A", "B"]
    dist_names  = {"A": "Ver. A (Empirical)", "B": "Ver. B (Idealised)"}
    target_pcts = sorted(results.keys())

    apply_style()
    fig, axes = plt.subplots(1, 2, figsize=FIG_PAIR, sharey=True)
    fig.suptitle(
        "E.1 CEW vs Revenue Target (E[T] as % of W₀)\n"
        f"γ = {gamma} | All systems revenue-equivalent",
        fontsize=11, fontweight="bold"
    )

    for ax, dlabel in zip(axes, dist_labels):
        for name in SYSTEMS_ORD:
            cews = [results[pct][dlabel][gamma].get(name) for pct in target_pcts]
            cews_pct = [c * 100 if c is not None else np.nan for c in cews]
            ax.plot(
                target_pcts, cews_pct,
                color=COLOURS[name], marker=MARKERS[name],
                linewidth=2, markersize=7,
                label=SYSTEM_LABELS[name]
            )
        ax.axhline(0, color="black", linewidth=0.7, linestyle="--", alpha=0.5)
        ax.yaxis.set_major_formatter(mtick.PercentFormatter(decimals=2))
        ax.set_xticks(target_pcts)
        ax.set_xticklabels([f"{p:.0f}%" for p in target_pcts])
        _style_ax(ax, dist_names[dlabel],
                  xlabel="Revenue target E[T] (% of W₀)",
                  ylabel="CEW (%)")

    axes[1].legend(fontsize=8, loc="lower left")
    fig.tight_layout()
    _save(fig, "m5_fig_e1_revenue_target.png")

# ─────────────────────────────────────────────────────────────────────────────
# SWEEP B — Start year
# ─────────────────────────────────────────────────────────────────────────────

def run_sweep_b(p):
    """
    Full start-year sweep: all valid start years in the 73-year series.
    A valid start year is one where a complete N-year window fits without
    exceeding the series end (i.e. start_year ≤ 2019 − N + 1 = 1990 for N=30).
    With wrap-around enabled, all 73 years are valid — the window wraps.
    Revenue target: 2% of W₀ (canonical). γ = 2. Ver. A only.

    Returns:
        full_results : {start_year: {system: cew}}
        curated      : {start_year: {system: cew}} — adverse years only
    """
    sw           = p["sweep"]
    curated_yrs  = sw["wfr_start_years_curated"]
    N            = p["tcm"]["canonical_N"]
    target_et    = 0.02 * W0_BASE
    base_year    = p["returns"]["series_base_year"]   # 1947
    all_years    = list(range(base_year, base_year + 73))  # 1947–2019

    full_results = {}
    for start_yr in all_years:
        dist, _ = _make_dist_for_start(p, start_yr, N)
        if dist is None:
            continue
        try:
            comp = run_welfare_comparison(W0_BASE, dist, GAMMA_CEN, target_et)
            full_results[start_yr] = {
                name: (r.cew if r.cew is not None else None)
                for name, r in comp.items()
            }
        except ValueError:
            full_results[start_yr] = {name: None for name in SYSTEMS_ORD}

        if start_yr % 10 == 0:
            print(f"  SweepB: start_year={start_yr} done")

    curated = {yr: full_results[yr] for yr in curated_yrs if yr in full_results}
    return full_results, curated


def chart_sweep_b_distribution(full_results):
    """
    Box plot / distribution of CEW outcomes across all start years, per system.
    Shows the full range of welfare outcomes the model produces across all
    historical sequences — the key robustness chart.
    """
    apply_style()
    fig, ax = plt.subplots(figsize=FIG_WIDE)
    fig.suptitle(
        "E.2.1 CEW Distribution Across All Start Years (1947–2019)\n"
        f"30-year windows with wrap-around | E[T] = 2% of W₀ | γ = {GAMMA_CEN}",
        fontsize=11, fontweight="bold"
    )

    all_cews = {}
    for name in SYSTEMS_ORD:
        vals = [
            full_results[yr][name] * 100
            for yr in sorted(full_results)
            if full_results[yr].get(name) is not None
        ]
        all_cews[name] = vals

    positions = list(range(1, len(SYSTEMS_ORD) + 1))
    bp = ax.boxplot(
        [all_cews[n] for n in SYSTEMS_ORD],
        positions=positions,
        patch_artist=True,
        widths=0.5,
        medianprops=dict(color="white", linewidth=2),
        whiskerprops=dict(linewidth=1.2),
        capprops=dict(linewidth=1.2),
        flierprops=dict(marker=".", markersize=4, alpha=0.5),
    )
    for patch, name in zip(bp["boxes"], SYSTEMS_ORD):
        patch.set_facecolor(COLOURS[name])
        patch.set_alpha(0.8)

    ax.set_xticks(positions)
    ax.set_xticklabels(
        [SYSTEM_LABELS[n].replace(" (", "\n(").replace(" Tax", "\nTax")
         for n in SYSTEMS_ORD],
        fontsize=8
    )
    ax.yaxis.set_major_formatter(mtick.PercentFormatter(decimals=2))
    ax.set_ylabel("CEW (%)", fontsize=9)
    ax.grid(axis="y", linestyle="--", alpha=0.35)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    # Annotate with WDT advantage: median(WDT) − median(worst competitor)
    wdt_median  = float(np.median(all_cews["symmetric_wdt"]))
    sw_median   = float(np.median(all_cews["stock_wealth"]))
    adv_bp      = (wdt_median - sw_median) * 100  # already in %; convert to bp
    ax.text(0.98, 0.02,
            f"WDT median advantage vs Stock Wealth Tax: {adv_bp:+.1f} bp",
            transform=ax.transAxes, ha="right", va="bottom", fontsize=8,
            color=COLOURS["symmetric_wdt"])

    fig.tight_layout()
    _save(fig, "m5_fig_e2a_start_year_distribution.png")


def chart_sweep_b_timeseries(full_results):
    """
    Line chart: CEW for each system vs start year.
    Shows how welfare costs track historical return sequences.
    Highlights curated worst-case years.
    """
    apply_style()
    years    = sorted(full_results.keys())
    fig, ax  = plt.subplots(figsize=FIG_WIDE_L)
    fig.suptitle(
        "E.2.2 CEW by Start Year — All Historical Windows\n"
        f"E[T] = 2% of W₀ | γ = {GAMMA_CEN} | 30-year windows",
        fontsize=11, fontweight="bold"
    )

    for name in SYSTEMS_ORD:
        cews = [
            full_results[yr].get(name, None) for yr in years
        ]
        cews_pct = [c * 100 if c is not None else np.nan for c in cews]
        ax.plot(years, cews_pct,
                color=COLOURS[name], linewidth=1.5,
                label=SYSTEM_LABELS[name], alpha=0.85)

    # Mark the canonical 2000-start scenario
    ax.axvline(2000, color="black", linewidth=1.0, linestyle="--",
               alpha=0.6, label="Canonical (2000)")

    ax.yaxis.set_major_formatter(mtick.PercentFormatter(decimals=2))
    ax.set_xlabel("Scenario start year", fontsize=9)
    ax.set_ylabel("CEW (%)", fontsize=9)
    ax.legend(fontsize=8, loc="lower right")
    ax.grid(axis="y", linestyle="--", alpha=0.3)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    fig.tight_layout()
    _save(fig, "m5_fig_e2b_timeseries.png")


# ─────────────────────────────────────────────────────────────────────────────
# SWEEP C — Rate parameter sensitivity (progressive WDT welfare surface)
# ─────────────────────────────────────────────────────────────────────────────

def run_sweep_c_param(p, param_name, param_vals, W0_vals, dist, gamma, target_et_frac):
    """
    Single-parameter sweep for the progressive-vs-flat welfare gap.
    param_name : one of 'tau_0', 'tau_m', 'k', 'W_min'
    param_vals : sweep grid for that parameter
    W0_vals    : wealth levels at which to evaluate (e.g. [10.0, 100.0])
    Returns: {W0: {param_val: gap_bp}}
    """
    rp      = p["rate"]
    results = {W0: {} for W0 in W0_vals}

    for pval in param_vals:
        # Build rate function with this parameter overridden
        kwargs = dict(
            tau0=rp["tau_0"], taum=rp["tau_m"],
            k=rp["k"], W_min=rp["W_min"]
        )
        if param_name == "tau_0":
            kwargs["tau0"] = pval
        elif param_name == "tau_m":
            kwargs["taum"] = pval
        elif param_name == "k":
            kwargs["k"] = pval
        elif param_name == "W_min":
            kwargs["W_min"] = pval

        # tau_0 must be < tau_m; skip invalid combinations
        if kwargs["tau0"] >= kwargs["taum"]:
            for W0 in W0_vals:
                results[W0][pval] = None
            continue

        rate_fn = ProgressiveRateFunction(**kwargs)

        for W0 in W0_vals:
            target_et = target_et_frac * W0
            r = run_progressive_cew(W0, dist, rate_fn, gamma, target_et)
            results[W0][pval] = r.get("gap_bp")

    return results


def chart_sweep_c_param(sweep_results, param_name, param_vals, W0_vals, param_label):
    """
    Line chart: progressive-vs-flat CEW gap (bp) vs parameter value.
    One line per W₀. Positive gap = flat WDT has lower welfare cost.
    """
    # Canonical filename and chart-number for each parameter — matches docstring.
    _PARAM_META = {
        "tau_0": ("m5_fig_e3a_tau0.png",  "E.3.1"),
        "tau_m": ("m5_fig_e3b_taum.png",  "E.3.2"),
        "k":     ("m5_fig_e3c_k.png",     "E.3.3"),
        "W_min": ("m5_fig_e3d_wmin.png",  "E.3.4"),
    }
    filename, chart_num = _PARAM_META.get(
        param_name,
        (f"m5_fig_e3x_{param_name}.png", "E.3.x"),
    )

    apply_style()
    fig, ax = plt.subplots(figsize=FIG_WIDE)

    W0_colours = {
        3.0:   "#c0392b",
        10.0:  "#e67e22",
        30.0:  "#2ecc71",
        100.0: "#1a6fad",
        150.0: "#8e44ad",
    }
    fallback_colours = ["#555555", "#999999", "#cccccc"]

    for i, W0 in enumerate(W0_vals):
        gaps = [sweep_results[W0].get(pv) for pv in param_vals]
        gaps = [g if g is not None else np.nan for g in gaps]
        colour = W0_colours.get(W0, fallback_colours[i % len(fallback_colours)])
        ax.plot(param_vals, gaps, color=colour, marker="o",
                linewidth=2, markersize=6, label=f"W₀ = £{W0:.0f}m")

    ax.axhline(0, color="black", linewidth=0.8, linestyle="--", alpha=0.6)
    ax.set_xlabel(param_label, fontsize=9)
    ax.set_ylabel("Flat WDT − Progressive WDT (basis points)\nPositive = flat cheaper", fontsize=9)
    ax.set_title(
        f"{chart_num} Progressive vs Flat WDT — {param_label} sensitivity\n"
        f"Revenue-equivalent comparison | E[T] = 2% of W₀ | γ = {GAMMA_CEN}",
        fontsize=10, fontweight="bold"
    )
    ax.legend(fontsize=8)
    ax.grid(axis="y", linestyle="--", alpha=0.35)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    fig.tight_layout()
    _save(fig, filename)


def run_sweep_a_w0(p):
    """
    Sweep W₀ across the wealth tier range at canonical 2% target.
    Shows how welfare costs vary across the wealth distribution at fixed revenue%.
    γ = 2. Ver. A. All five flat systems.
    Returns: {W0: {system: cew}}
    """
    sw       = p["sweep"]
    W0_vals  = sw["wfr_W0_sweep"]
    N        = p["tcm"]["canonical_N"]
    dist_A   = make_empirical_distribution_scenario(p, N)

    results = {}
    for W0 in W0_vals:
        target_et = 0.02 * W0
        try:
            comp = run_welfare_comparison(W0, dist_A, GAMMA_CEN, target_et)
            results[W0] = {name: (r.cew if r.cew is not None else None)
                           for name, r in comp.items()}
        except ValueError as e:
            results[W0] = {name: None for name in SYSTEMS_ORD}
            print(f"  SweepA-W0: W0={W0} failed: {e}")
        print(f"  SweepA-W0: W0=£{W0:.0f}m done")

    return results, dist_A


def chart_sweep_a_w0(w0_results, W0_vals):
    """CEW vs W₀ for all systems. Shows wealth-level dependence."""
    apply_style()
    fig, ax = plt.subplots(figsize=FIG_WIDE)
    fig.suptitle(
        "E.1.1 CEW vs Initial Wealth W₀\n"
        f"E[T] = 2% of W₀ | γ = {GAMMA_CEN} | Ver. A distribution",
        fontsize=11, fontweight="bold"
    )

    for name in SYSTEMS_ORD:
        cews = [w0_results[W0].get(name) for W0 in W0_vals]
        cews_pct = [c * 100 if c is not None else np.nan for c in cews]
        ax.plot(W0_vals, cews_pct,
                color=COLOURS[name], marker=MARKERS[name],
                linewidth=2, markersize=7, label=SYSTEM_LABELS[name])

    ax.axhline(0, color="black", linewidth=0.7, linestyle="--", alpha=0.5)
    ax.yaxis.set_major_formatter(mtick.PercentFormatter(decimals=2))
    ax.set_xlabel("Initial wealth W₀ (£m)", fontsize=9)
    ax.set_ylabel("CEW (%)", fontsize=9)
    ax.legend(fontsize=8, loc="lower right")
    ax.grid(axis="y", linestyle="--", alpha=0.35)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    fig.tight_layout()
    _save(fig, "m5_fig_e1b_w0_sensitivity.png")


# ─────────────────────────────────────────────────────────────────────────────
# DOCUMENT ASSEMBLY
# ─────────────────────────────────────────────────────────────────────────────

def write_tables(
    sweep_a_results, sweep_b_full, sweep_b_curated,
    sweep_c_tables, p
):
    """Assemble all sweep tables into a single markdown document."""
    sw  = p["sweep"]
    doc = MdDoc()

    doc.h1("WFR Welfare Sweep Analysis — Module 5")
    doc.blank()
    doc.add(f"*Generated: {today_iso()}*")
    doc.add(
        "*All CEW values relative to no-tax benchmark. "
        "Negative = welfare cost. Revenue-equivalent rates used throughout.*"
    )
    doc.blank()
    doc.rule()

    # ── Sweep A: revenue target ───────────────────────────────────────────────
    doc.blank()
    doc.h2("Sweep A: Revenue Target Sensitivity")
    doc.blank()
    doc.add(
        "Question: are the welfare rankings stable across the realistic range "
        "of revenue targets? Covers E[T] = 1%–5% of W₀, spanning CGT-deferral-"
        "equivalent (1%) through income-tax-equivalent (5%). "
        "γ = 2. W₀ = 1.0 (normalised). Both distributions."
    )
    doc.blank()
    doc.h3("Table WFR.S1 — CEW by System and Revenue Target (γ=2)")
    doc.note(
        "Rows grouped by distribution. Columns = revenue target as % of W₀. "
        "Rankings that flip across the revenue range signal revenue-sensitivity; "
        "rankings that hold across the full range are structurally robust."
    )
    doc.add_block(table_sweep_a(sweep_a_results))
    doc.blank()
    doc.rule()

    # ── Sweep B: start year ───────────────────────────────────────────────────
    doc.blank()
    doc.h2("Sweep B: Start-Year Worst-Case Analysis")
    doc.blank()
    doc.add(
        "Question: does the WDT's structural advantage survive the historically "
        "adverse return sequences? Runs all 73 possible 30-year windows within "
        "the 1947–2019 series (with wrap-around). "
        "E[T] = 2% of W₀. γ = 2. Ver. A distribution."
    )
    doc.blank()
    doc.h3("Table WFR.S2a — Summary Statistics Across All Start Years")
    doc.note(
        "Min/median/mean/max CEW across all 73 start-year windows. "
        "WDT best? = fraction of start years where Symmetric WDT has highest CEW "
        "(lowest welfare cost) of the five systems."
    )
    doc.add_block(table_sweep_b_summary(sweep_b_full))
    doc.blank()

    doc.h3("Table WFR.S2b — Curated Worst-Case Start Years")
    doc.note(
        "Six historically adverse sequences plus the canonical 2000-start (◄). "
        "Adverse years selected for: proximity to major market dislocations "
        "(1972 oil shock, 1987 Black Monday, 1999/2000 dot-com, 2006 GFC entry), "
        "post-war austerity (1946), and worst LRR fill speed (2006). "
        "WDT advantage column = (CEW_WDT − CEW_StockWealth) × 10,000 in basis points."
    )
    doc.add_block(table_sweep_b_worst_case(sweep_b_full, sw["wfr_start_years_curated"]))
    doc.blank()
    doc.rule()

    # ── Sweep C: parameter sensitivity ───────────────────────────────────────
    doc.blank()
    doc.h2("Sweep C: Progressive WDT Parameter Sensitivity")
    doc.blank()
    doc.add(
        "Question: across the feasible WDT parameter space, when does the "
        "progressive structure add meaningful welfare cost relative to a "
        "revenue-equivalent flat rate? Single-parameter sweeps holding "
        "all other parameters at canonical values. "
        "Revenue-equivalent: progressive rate scaled to match flat system's E[T]. "
        "E[T] = 2% of W₀. γ = 2. Gap (bp) = (CEW_flat − CEW_progressive) × 10,000; "
        "positive = flat WDT has lower welfare cost; negative = progressive is cheaper."
    )
    doc.blank()

    param_display = {
        "tau_0": ("Table WFR.S3a — τ₀ Sweep (Entry Rate Floor)",
                  "τ₀ (entry rate at W_min). τ_m, k, W_min at canonical values."),
        "tau_m": ("Table WFR.S3b — τ_m Sweep (Ceiling Rate)",
                  "τ_m (asymptotic ceiling). τ₀, k, W_min at canonical values."),
        "k":     ("Table WFR.S3c — k Sweep (Logistic Steepness)",
                  "k (steepness per £m). τ₀, τ_m, W_min at canonical values."),
        "W_min": ("Table WFR.S3d — W_min Sweep (Entry-Point Wealth)",
                  "W_min (£m). τ₀, τ_m, k at canonical values."),
    }

    for param_name, tbl_str in sweep_c_tables.items():
        if param_name not in param_display:
            continue
        title, note_text = param_display[param_name]
        doc.h3(title)
        doc.note(note_text)
        doc.add_block(tbl_str)
        doc.blank()

    doc.rule()
    doc.blank()
    doc.h2("Parameter Reference")
    doc.blank()
    rp = p["rate"]
    doc.add("| Parameter | Canonical value |")
    doc.add("|:---|---:|")
    doc.add(f"| τ₀ | {fmt_pct0(rp['tau_0'])} |")
    doc.add(f"| τ_m | {fmt_pct0(rp['tau_m'])} |")
    doc.add(f"| k | {rp['k']} per £m |")
    doc.add(f"| W_min | {fmt_gbp_m(rp['W_min'], dp=0)} |")
    doc.add(f"| canonical_N | {p['tcm']['canonical_N']} years |")
    doc.add(f"| scenario_start_year | {p['tcm']['scenario_start_year']} |")
    doc.add(f"| γ (central) | {GAMMA_CEN} |")
    doc.blank()

    out_path = Path(OUTPUT_DIR) / "WFR_sweep_tables.md"
    doc.write(out_path)
    return out_path


# ─────────────────────────────────────────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────────────────────────────────────────

def main():
    print("=" * 70)
    print("MODULE 5: Welfare Sweep Analysis")
    print("=" * 70)

    p  = load_params(TOML_PATH)
    sw = p["sweep"]
    N  = p["tcm"]["canonical_N"]
    rp = p["rate"]

    # Canonical rate function (unscaled)
    rate_fn = ProgressiveRateFunction(
        tau0=rp["tau_0"], taum=rp["tau_m"],
        k=rp["k"], W_min=rp["W_min"]
    )

    # ── Sweep A: revenue target ───────────────────────────────────────────────
    print("\n--- Sweep A: Revenue target sensitivity ---")
    sweep_a_results, dists = run_sweep_a(p)
    chart_sweep_a(sweep_a_results)

    print("\n--- Sweep A: W₀ sensitivity ---")
    w0_results, dist_A = run_sweep_a_w0(p)
    chart_sweep_a_w0(w0_results, sw["wfr_W0_sweep"])

    # ── Sweep B: start year ───────────────────────────────────────────────────
    print("\n--- Sweep B: Start-year sweep (73 windows) ---")
    sweep_b_full, sweep_b_curated = run_sweep_b(p)
    chart_sweep_b_distribution(sweep_b_full)
    chart_sweep_b_timeseries(sweep_b_full)

    # ── Sweep C: parameter sensitivity ───────────────────────────────────────
    print("\n--- Sweep C: Parameter sensitivity ---")
    dist_A_canon = make_empirical_distribution_scenario(p, N)

    # Wealth levels for C sweep: mid-range and high-wealth
    W0_sweep_c = [10.0, 30.0, 100.0]

    param_configs = [
        ("tau_0", sw["wfr_tau_0_sweep"], "τ₀ (entry rate)"),
        ("tau_m", sw["wfr_tau_m_sweep"], "τ_m (ceiling rate)"),
        ("k",     sw["wfr_k_sweep"],     "k (steepness per £m)"),
        ("W_min", sw["wfr_wmin_sweep"],  "W_min (£m)"),
    ]

    all_param_results = {}
    for param_name, param_vals, param_label in param_configs:
        print(f"  Sweep C: {param_name} ({len(param_vals)} values × {len(W0_sweep_c)} W₀ levels)")
        res = run_sweep_c_param(
            p, param_name, param_vals, W0_sweep_c,
            dist_A_canon, GAMMA_CEN, 0.02
        )
        all_param_results[param_name] = res
        chart_sweep_c_param(res, param_name, param_vals, W0_sweep_c, param_label)


    print(f"\n✓ Module 5 complete.")
    print(f"  Charts:  {OUTPUT_DIR}")


if __name__ == "__main__":
    main()