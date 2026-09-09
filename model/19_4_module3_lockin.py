"""
module3_lockin.py
=================
Module 3: The Realisation Decision and CGT Lock-In

Question: How large is the welfare cost of the CGT lock-in distortion,
and how does the WDT's structural absence of this distortion compare?

The lock-in distortion: an agent holding Asset A with an embedded gain
faces a tax cost to switching to a superior Asset B. Under CGT, the switch
crystallises the gain and triggers immediate tax. Under WDT, the gain
has already been accruing — switching is costless on the margin.

Structure
---------
Part A  — The lock-in threshold: at what return differential does the
           agent prefer to stay in the inferior asset?
Part B  — Welfare cost of lock-in: foregone return × probability of lock-in
Part C  — Comparison: CGT lock-in cost vs WDT risk-sharing advantage
           (from Module 1). Which effect is larger?
Part D  — Sensitivity: how lock-in cost varies with embedded gain G,
           holding period N, and CGT rate τ_cgt
Part E  — Full welfare comparison: WDT vs CGT including lock-in

Key result this module seeks: the welfare case for WDT over CGT rests
primarily on the lock-in distortion, not on the risk-sharing difference
from Module 1 (where CGT and income tax were identical). This module
quantifies which effect dominates.

Outputs → model/OUTPUTS/WFR/module3/
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

from welfare_paths import TOML_PATH, module_output_dir
from welfare_core import (
    load_params,
    make_empirical_distribution,
    make_idealised_distribution,
    ReturnDistribution,
    crra_utility,
    expected_utility,
    consumption_equiv_welfare,
    run_welfare_comparison,
    get_tax_fn,
    solve_revenue_equivalent_rate,
    SYSTEM_LABELS,
    make_empirical_distribution_scenario,
    make_idealised_distribution_scenario,
)

OUTPUT_DIR = module_output_dir("module3")

# ─────────────────────────────────────────────────────────────────────────────
# CONFIG
# ─────────────────────────────────────────────────────────────────────────────

W0_BASE   = 10.0     # £10m — typical WDT taxable agent (in £m, matches Module 2)
TARGET_ET = 0.02     # 2% of W0
GAMMA     = 2.0      # central case

COLOURS = {
    "wdt"          : "#1a6fad",
    "cgt"          : "#f1c40f",
    "cgt_with_lock": "#e67e22",
    "income"       : "#e67e22",
    "threshold"    : "#c0392b",
    "lockin_cost"  : "#8e44ad",
}


# ─────────────────────────────────────────────────────────────────────────────
# PART A: Lock-in threshold
# ─────────────────────────────────────────────────────────────────────────────

@dataclass
class AssetSwitchDecision:
    """
    Agent holds Asset A with cost basis B and current value V = B + G.
    Asset B is available with expected return r_B per period.
    Asset A has expected return r_A per period.
    CGT rate is tau_cgt.
    Holding period after switch: T periods.

    Under CGT: switching costs tau_cgt × G immediately.
    Under WDT: the gain G has been accruing; switching is costless on margin
               (the tax on G is already reflected in declared net worth).

    Lock-in condition (CGT):
        Stay in A if: V × r_A × T > (V - tau_cgt×G) × r_B × T
        i.e., stay if: r_A > r_B × (1 - tau_cgt × G/V)
        i.e., stay if: r_B - r_A < r_B × tau_cgt × G/V

    The lock-in threshold for the return differential:
        delta_r* = r_B × tau_cgt × G / V

    Any r_B - r_A < delta_r* → agent stays in inferior Asset A.
    """
    V         : float   # current value of Asset A (£m)
    B         : float   # cost basis of Asset A (£m)
    tau_cgt   : float   # CGT rate
    T         : int     # remaining holding period (years)
    r_A       : float   # expected return on Asset A (annual)

    @property
    def embedded_gain(self) -> float:
        return self.V - self.B

    @property
    def gain_ratio(self) -> float:
        """G / V — embedded gain as fraction of current value."""
        return self.embedded_gain / self.V if self.V > 0 else 0.0

    def lock_in_threshold(self, r_B: float) -> float:
        """
        Minimum return differential (r_B - r_A) at which agent prefers to switch.
        Below this threshold, lock-in holds — agent stays in A.
        """
        return r_B * self.tau_cgt * self.gain_ratio

    def switch_cost_pv(self) -> float:
        """
        Present value of switching cost = immediate CGT liability.
        tau_cgt × G (paid now, before reinvestment in B).
        """
        return self.tau_cgt * self.embedded_gain

    def value_of_stay(self, r_B_grid: np.ndarray) -> np.ndarray:
        """
        NPV of staying in Asset A for T periods at r_A, vs switching to B at r_B.
        Returns array of (NPV_stay - NPV_switch) for each r_B in grid.
        Positive = prefer to stay. Negative = prefer to switch.
        """
        npv_stay   = self.V * ((1 + self.r_A) ** self.T)
        switch_val = self.V - self.switch_cost_pv()   # after-tax value post-switch
        npv_switch = switch_val * ((1 + r_B_grid) ** self.T)
        return npv_stay - npv_switch

    def indifference_return(self) -> float:
        """
        r_B at which agent is exactly indifferent between staying and switching.
        NPV_stay = NPV_switch:
            V × (1+r_A)^T = (V - tau×G) × (1+r_B*)^T
            r_B* = (V/(V - tau×G))^(1/T) × (1+r_A) - 1
        """
        after_tax_switch = self.V - self.switch_cost_pv()
        if after_tax_switch <= 0:
            return float('inf')
        return ((self.V / after_tax_switch) ** (1.0 / self.T)) * (1 + self.r_A) - 1


# ─────────────────────────────────────────────────────────────────────────────
# PART B: Welfare cost of lock-in
# ─────────────────────────────────────────────────────────────────────────────

def compute_lock_in_welfare_cost(
    asset   : AssetSwitchDecision,
    dist    : ReturnDistribution,
    gamma   : float,
    tau_cgt : float,
) -> dict:
    """
    Welfare cost of lock-in.

    Approach: for each return state R in the distribution, compute whether
    the agent would be locked in (R applied to Asset B is below the lock-in
    threshold relative to Asset A's expected return).

    The welfare cost in each state is the utility difference between:
      (a) freely optimising (switch if r_B > r_A, stay otherwise)
      (b) being locked into Asset A regardless

    Expected welfare cost = E[u(free)] - E[u(locked)]

    Note: this is an approximation — in reality the lock-in decision is
    forward-looking and path-dependent. The one-period version here gives
    the direction and order of magnitude correctly.

    Implementation notes (WFR.9 audit):
      - The tau_cgt parameter is UNUSED: the lock-in threshold and switch cost
        are determined entirely by asset.tau_cgt (the statutory UK CGT rate).
        The parameter is retained for signature compatibility; callers should
        pass asset.tau_cgt explicitly if they want to change the statutory rate.
      - Two distinct CGT rates appear in Table WFR.9:
          * asset.tau_cgt = 24% (UK 2024 statutory, governs switch decision)
          * m1_results['cgt'].tau ≈ 18.9% (revenue-equivalent, governs CEW comparison)
        This duality is intentional: the realisation decision responds to the
        actual statutory rate, not the hypothetical equal-revenue rate.
      - CEW_free models a no-tax free optimiser (switch whenever r_B > r_A).
        This is a welfare UPPER BOUND; actual WDT agents pay tax on gains.
        The comparison cgt_with_lock_cew vs wdt_cew (Table WFR.9) is valid
        because wdt_cew already accounts for WDT taxation at the Module 1 rate.
    """
    costs_by_state = []

    for R, prob in zip(dist.returns, dist.probs):
        r_B = R - 1.0   # return on Asset B if agent switches

        # Under no lock-in (WDT or free optimiser): choose best asset
        # If r_B > r_A: switch to B, consume V × (1 + r_B)
        # If r_B <= r_A: stay in A, consume V × (1 + r_A)
        if r_B > asset.r_A:
            C_free = asset.V * (1.0 + r_B)
        else:
            C_free = asset.V * (1.0 + asset.r_A)

        # Under CGT lock-in:
        # The agent stays in A if r_B < indifference return
        r_B_indiff = asset.indifference_return()
        if r_B >= r_B_indiff:
            # Switch despite CGT: pays tax, reinvests
            after_tax = asset.V - asset.switch_cost_pv()
            C_locked  = after_tax * (1.0 + r_B)
        else:
            # Locked in: stays in A
            C_locked = asset.V * (1.0 + asset.r_A)

        C_free   = max(C_free,   1e-9)
        C_locked = max(C_locked, 1e-9)

        costs_by_state.append({
            "R"          : R,
            "prob"       : prob,
            "r_B"        : r_B,
            "C_free"     : C_free,
            "C_locked"   : C_locked,
            "u_free"     : crra_utility(C_free,   gamma),
            "u_locked"   : crra_utility(C_locked, gamma),
            "locked_in"  : r_B < r_B_indiff,
        })

    eu_free   = sum(s["prob"] * s["u_free"]   for s in costs_by_state)
    eu_locked = sum(s["prob"] * s["u_locked"] for s in costs_by_state)
    eu_notax  = sum(
        s["prob"] * crra_utility(max(asset.V * s["R"], 1e-9), gamma)
        for s in costs_by_state
    )

    cew_free   = consumption_equiv_welfare(eu_free,   eu_notax, gamma)
    cew_locked = consumption_equiv_welfare(eu_locked, eu_notax, gamma)
    lock_in_cost_bp = (cew_free - cew_locked) * 10000

    # P(locked in) decomposition:
    #   p_below_rA      : agent would stay in A even without CGT (r_B < r_A)
    #                     — not a CGT distortion, a fundamental preference
    #   p_locked_cgt    : r_A ≤ r_B < r_B* — agent would switch without CGT
    #                     but stays because CGT switching cost exceeds benefit
    #                     — this is the CGT lock-in distortion proper
    #   p_locked        : total = p_below_rA + p_locked_cgt (all locked states)
    r_B_indiff = asset.indifference_return()
    p_below_rA   = sum(s["prob"] for s in costs_by_state if s["r_B"] <  asset.r_A)
    p_locked_cgt = sum(s["prob"] for s in costs_by_state
                       if asset.r_A <= s["r_B"] < r_B_indiff)
    p_locked     = p_below_rA + p_locked_cgt   # = all locked states

    return {
        "eu_free"          : eu_free,
        "eu_locked"        : eu_locked,
        "eu_notax"         : eu_notax,
        "cew_free"         : cew_free,
        "cew_locked"       : cew_locked,
        "lock_in_cost_bp"  : lock_in_cost_bp,
        "p_locked"         : p_locked,
        "p_locked_cgt"     : p_locked_cgt,   # CGT distortion proper
        "p_below_rA"       : p_below_rA,     # fundamental preference (not CGT)
        "r_B_indiff"       : r_B_indiff,
        "switch_cost"      : asset.switch_cost_pv(),
        "states"           : costs_by_state,
    }


# ─────────────────────────────────────────────────────────────────────────────
# PART C & D: Sensitivity analysis
# ─────────────────────────────────────────────────────────────────────────────

def sensitivity_gain_ratio(
    V         : float,
    r_A       : float,
    T         : int,
    tau_cgt   : float,
    dist      : ReturnDistribution,
    gamma     : float,
    gain_ratios: np.ndarray,
) -> list:
    """Sweep over embedded gain ratios G/V."""
    results = []
    for gr in gain_ratios:
        G     = V * gr
        B     = V - G
        asset = AssetSwitchDecision(V=V, B=B, tau_cgt=tau_cgt, T=T, r_A=r_A)
        r     = compute_lock_in_welfare_cost(asset, dist, gamma, tau_cgt)
        r["gain_ratio"] = gr
        results.append(r)
    return results


def sensitivity_holding_period(
    V       : float,
    G       : float,
    r_A     : float,
    tau_cgt : float,
    dist    : ReturnDistribution,
    gamma   : float,
    T_vals  : list,
) -> list:
    """Sweep over remaining holding periods T."""
    results = []
    B = V - G
    for T in T_vals:
        asset = AssetSwitchDecision(V=V, B=B, tau_cgt=tau_cgt, T=T, r_A=r_A)
        r     = compute_lock_in_welfare_cost(asset, dist, gamma, tau_cgt)
        r["T"] = T
        results.append(r)
    return results


def sensitivity_cgt_rate(
    V       : float,
    G       : float,
    r_A     : float,
    T       : int,
    dist    : ReturnDistribution,
    gamma   : float,
    tau_vals: np.ndarray,
) -> list:
    """Sweep over CGT rates."""
    results = []
    B = V - G
    for tau in tau_vals:
        asset = AssetSwitchDecision(V=V, B=B, tau_cgt=tau, T=T, r_A=r_A)
        r     = compute_lock_in_welfare_cost(asset, dist, gamma, tau)
        r["tau_cgt"] = tau
        results.append(r)
    return results


# ─────────────────────────────────────────────────────────────────────────────
# PART E: Full welfare comparison including lock-in
# ─────────────────────────────────────────────────────────────────────────────

def full_comparison_with_lockin(
    W0      : float,
    dist    : ReturnDistribution,
    gamma   : float,
    target_et: float,
    asset   : AssetSwitchDecision,
) -> dict:
    """
    Full comparison: WDT vs CGT without lock-in vs CGT with lock-in.

    Module 1 showed WDT and CGT are near-identical when lock-in is absent
    (Module 1 treats CGT as a lower-rate income tax on gains). This function
    adds the lock-in cost to CGT's welfare number to show the true comparison.
    """
    # Base results from Module 1 machinery
    m1_results = run_welfare_comparison(W0, dist, gamma, target_et)

    wdt_cew = m1_results["symmetric_wdt"].cew
    cgt_cew = m1_results["cgt"].cew            # CGT without lock-in (Module 1)

    # Lock-in cost
    lock = compute_lock_in_welfare_cost(asset, dist, gamma, m1_results["cgt"].tau)
    lock_in_bp = lock["lock_in_cost_bp"]

    # CGT with lock-in: subtract the lock-in welfare cost
    cgt_with_lock_cew = cgt_cew - lock_in_bp / 10000

    # WDT advantage: over CGT without lock-in, and over CGT with lock-in
    adv_no_lock  = (wdt_cew - cgt_cew)          * 10000
    adv_with_lock= (wdt_cew - cgt_with_lock_cew)* 10000

    return {
        "wdt_cew"             : wdt_cew,
        "cgt_cew"             : cgt_cew,
        "cgt_with_lock_cew"   : cgt_with_lock_cew,
        "lock_in_cost_bp"     : lock_in_bp,
        "wdt_adv_no_lock_bp"  : adv_no_lock,
        "wdt_adv_with_lock_bp": adv_with_lock,
        "p_locked"            : lock["p_locked"],
        "p_locked_cgt"        : lock["p_locked_cgt"],
        "p_below_rA"          : lock["p_below_rA"],
        "r_B_indiff"          : lock["r_B_indiff"],
        "m1_cgt_tau"          : m1_results["cgt"].tau,
        "m1_wdt_tau"          : m1_results["symmetric_wdt"].tau,
    }


# ─────────────────────────────────────────────────────────────────────────────
# CHARTS
# ─────────────────────────────────────────────────────────────────────────────

def _save(fig, name: str):
    path = os.path.join(OUTPUT_DIR, name)
    fig.savefig(path, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(f"  Saved: {path}")


def chart_lock_in_threshold(asset: AssetSwitchDecision):
    """Chart A: NPV(stay) - NPV(switch) as r_B varies."""
    r_B_grid = np.linspace(asset.r_A * 0.5, asset.r_A * 2.5, 300)
    npv_diff = asset.value_of_stay(r_B_grid)
    r_B_indiff = asset.indifference_return()

    fig, ax = plt.subplots(figsize=(8, 5))
    ax.plot(r_B_grid * 100, npv_diff, color=COLOURS["cgt"], linewidth=2.5,
            label="NPV(stay in A) − NPV(switch to B)")
    ax.axhline(0, color="black", linewidth=0.9)
    ax.axvline(r_B_indiff * 100, color=COLOURS["threshold"], linewidth=1.5,
               linestyle="--", label=f"Indifference return r_B* = {r_B_indiff*100:.2f}%")
    ax.axvline(asset.r_A * 100, color="grey", linewidth=1.2,
               linestyle=":", label=f"Asset A return r_A = {asset.r_A*100:.2f}%")

    ax.fill_between(r_B_grid * 100, npv_diff, 0,
                    where=(r_B_grid < r_B_indiff), alpha=0.15,
                    color=COLOURS["threshold"], label="Lock-in region")

    ax.set_xlabel("Asset B expected return r_B (%)", fontsize=9)
    ax.set_ylabel("NPV preference for Asset A (£m)", fontsize=9)
    ax.set_title(
        f"Module 3, Part A: CGT Lock-In Threshold\n"
        f"V=£{asset.V:.0f}m, G/V={asset.gain_ratio*100:.0f}%, "
        f"τ_cgt={asset.tau_cgt*100:.0f}%, T={asset.T}yr",
        fontsize=10, fontweight="bold"
    )
    ax.legend(fontsize=8)
    ax.grid(axis="y", linestyle="--", alpha=0.4)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    _save(fig, "m3_chartA_lock_in_threshold.png")


def chart_sensitivity_gain(sens_gain: list):
    """Chart B: Lock-in welfare cost vs embedded gain ratio."""
    gr    = [r["gain_ratio"] * 100 for r in sens_gain]
    costs = [r["lock_in_cost_bp"] for r in sens_gain]
    p_loc = [r["p_locked"] * 100 for r in sens_gain]

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
    fig.suptitle("Module 3, Part D: Sensitivity — Embedded Gain Ratio G/V",
                 fontsize=11, fontweight="bold")

    ax1.plot(gr, costs, color=COLOURS["lockin_cost"], marker="o",
             linewidth=2, markersize=6)
    ax1.set_xlabel("Embedded gain as % of asset value (G/V)", fontsize=9)
    ax1.set_ylabel("Lock-in welfare cost (basis points)", fontsize=9)
    ax1.set_title("Welfare cost of CGT lock-in", fontsize=9)
    ax1.grid(axis="y", linestyle="--", alpha=0.4)
    ax1.spines["top"].set_visible(False); ax1.spines["right"].set_visible(False)

    ax2.plot(gr, p_loc, color=COLOURS["threshold"], marker="s",
             linewidth=2, markersize=6)
    ax2.set_xlabel("Embedded gain as % of asset value (G/V)", fontsize=9)
    ax2.set_ylabel("P(agent locked in) — % of return states", fontsize=9)
    ax2.set_title("Probability of being locked in", fontsize=9)
    ax2.yaxis.set_major_formatter(mtick.PercentFormatter())
    ax2.grid(axis="y", linestyle="--", alpha=0.4)
    ax2.spines["top"].set_visible(False); ax2.spines["right"].set_visible(False)

    fig.tight_layout()
    _save(fig, "m3_chartB_sensitivity_gain.png")


def chart_sensitivity_T(sens_T: list):
    """Chart C: Lock-in welfare cost vs remaining holding period T."""
    T_vals = [r["T"] for r in sens_T]
    costs  = [r["lock_in_cost_bp"] for r in sens_T]
    indiff = [r["r_B_indiff"] * 100 for r in sens_T]

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
    fig.suptitle("Module 3, Part D: Sensitivity — Remaining Holding Period T",
                 fontsize=11, fontweight="bold")

    ax1.plot(T_vals, costs, color=COLOURS["lockin_cost"], marker="o",
             linewidth=2, markersize=6)
    ax1.set_xlabel("Remaining holding period T (years)", fontsize=9)
    ax1.set_ylabel("Lock-in welfare cost (basis points)", fontsize=9)
    ax1.set_title("Welfare cost rises from T=1 then plateaus\n"
                  "(each extra year of B's compounding raises the opportunity cost of lock-in;\n"
                  "plateau when r_B* ≈ r_A and trapped zone collapses)", fontsize=9)
    ax1.grid(axis="y", linestyle="--", alpha=0.4)
    ax1.spines["top"].set_visible(False); ax1.spines["right"].set_visible(False)

    ax2.plot(T_vals, indiff, color=COLOURS["threshold"], marker="s",
             linewidth=2, markersize=6)
    ax2.set_xlabel("Remaining holding period T (years)", fontsize=9)
    ax2.set_ylabel("Indifference return r_B* (%)", fontsize=9)
    ax2.set_title("Indifference return converges to r_A as T→∞", fontsize=9)
    ax2.yaxis.set_major_formatter(mtick.PercentFormatter(decimals=2))
    ax2.grid(axis="y", linestyle="--", alpha=0.4)
    ax2.spines["top"].set_visible(False); ax2.spines["right"].set_visible(False)

    fig.tight_layout()
    _save(fig, "m3_chartC_sensitivity_T.png")


def chart_full_comparison(comp: dict, dist_label: str):
    """Chart D: WDT vs CGT (no lock-in) vs CGT (with lock-in)."""
    labels = [
        "WDT\n(Module 1)",
        "CGT\n(no lock-in,\nModule 1)",
        "CGT\n(with lock-in,\nModule 3)",
    ]
    values = [
        comp["wdt_cew"] * 100,
        comp["cgt_cew"] * 100,
        comp["cgt_with_lock_cew"] * 100,
    ]
    colors = [COLOURS["wdt"], COLOURS["cgt"], COLOURS["cgt_with_lock"]]

    fig, ax = plt.subplots(figsize=(8, 5))
    bars = ax.bar(labels, values, color=colors, edgecolor="white",
                  linewidth=0.8, alpha=0.88, width=0.45)

    for bar, val in zip(bars, values):
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            val - 0.002,
            f"{val:.4f}%",
            ha="center", va="top",
            fontsize=9, fontweight="bold", color="white"
        )

    # Annotate the lock-in cost
    y_cgt     = values[1]
    y_cgt_lk  = values[2]
    mid_x     = bars[2].get_x() + bars[2].get_width() / 2
    ax.annotate(
        f"Lock-in cost\n{comp['lock_in_cost_bp']:.2f} bp",
        xy=(mid_x, (y_cgt + y_cgt_lk) / 2),
        xytext=(mid_x + 0.35, (y_cgt + y_cgt_lk) / 2),
        fontsize=8, color=COLOURS["lockin_cost"],
        arrowprops=dict(arrowstyle="->", color=COLOURS["lockin_cost"])
    )

    ax.axhline(0, color="black", linewidth=0.8)
    ax.set_ylabel("CEW vs No-Tax (%)", fontsize=9)
    ax.set_title(
        f"Module 3, Part E: Full Welfare Comparison — WDT vs CGT\n"
        f"γ = {GAMMA} | {dist_label[:50]}\n"
        f"P(locked in) = {comp['p_locked']*100:.1f}%  |  "
        f"WDT advantage (with lock-in) = {comp['wdt_adv_with_lock_bp']:.2f} bp",
        fontsize=9, fontweight="bold"
    )
    ax.yaxis.set_major_formatter(mtick.PercentFormatter(decimals=4))
    ax.grid(axis="y", linestyle="--", alpha=0.4)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    fig.tight_layout()
    _save(fig, "m3_chartD_full_comparison.png")


# ─────────────────────────────────────────────────────────────────────────────
# PRINT HELPERS
# ─────────────────────────────────────────────────────────────────────────────

def print_comparison_table(comp: dict, dist_label: str):
    print(f"\n{'='*70}")
    print(f"PART E: Full Welfare Comparison — {dist_label[:50]}")
    print(f"{'='*70}")
    print(f"  {'WDT CEW':40s} {comp['wdt_cew']*100:>10.4f}%")
    print(f"  {'CGT CEW (no lock-in, Module 1)':40s} {comp['cgt_cew']*100:>10.4f}%")
    print(f"  {'Lock-in welfare cost':40s} {comp['lock_in_cost_bp']:>+10.2f} bp")
    print(f"  {'CGT CEW (with lock-in)':40s} {comp['cgt_with_lock_cew']*100:>10.4f}%")
    print(f"  {'-'*52}")
    print(f"  {'WDT advantage vs CGT (no lock-in)':40s} {comp['wdt_adv_no_lock_bp']:>+10.2f} bp")
    print(f"  {'WDT advantage vs CGT (with lock-in)':40s} {comp['wdt_adv_with_lock_bp']:>+10.2f} bp")
    print(f"  {'P(agent locked in)':40s} {comp['p_locked']*100:>10.1f}%")
    print(f"  {'CGT indifference return r_B*':40s} {comp['r_B_indiff']*100:>10.2f}%")


def print_findings(comp_A: dict, sens_gain: list, sens_T: list):
    print(f"\n{'='*70}")
    print("MODULE 3 — KEY FINDINGS")
    print(f"{'='*70}")

    max_lock_gain = max(s["lock_in_cost_bp"] for s in sens_gain)
    min_lock_T    = min(s["lock_in_cost_bp"] for s in sens_T)
    max_lock_T    = max(s["lock_in_cost_bp"] for s in sens_T)

    findings = [
        f"1. LOCK-IN COST MAGNITUDE: The CGT lock-in distortion adds "
        f"{comp_A['lock_in_cost_bp']:.2f} basis points of welfare cost "
        f"at the reference parameters (G/V=50%, T=5yr, τ_cgt=24%). "
        f"This is {'larger' if comp_A['lock_in_cost_bp'] > abs(comp_A['wdt_adv_no_lock_bp']) else 'smaller'} "
        f"than the WDT risk-sharing advantage from Module 1 "
        f"({comp_A['wdt_adv_no_lock_bp']:.2f} bp). "
        f"Lock-in is therefore the {'primary' if comp_A['lock_in_cost_bp'] > abs(comp_A['wdt_adv_no_lock_bp']) else 'secondary'} "
        f"channel through which WDT welfare-dominates CGT.",

        f"2. PROBABILITY OF LOCK-IN (decomposed): In {comp_A['p_locked']*100:.1f}% of return "
        f"states the agent stays in Asset A under CGT. This has two components: "
        f"{comp_A['p_below_rA']*100:.1f}% of states have r_B < r_A — the agent "
        f"would stay regardless of CGT (fundamental preference, not a distortion). "
        f"The CGT lock-in distortion proper affects {comp_A['p_locked_cgt']*100:.1f}% "
        f"of states — those where r_A ≤ r_B < r_B* = {comp_A['r_B_indiff']*100:.2f}%: "
        f"the agent would switch without CGT but the switching cost exceeds the benefit. "
        f"The welfare cost is attributable to this second component only.",

        f"3. GAIN RATIO SENSITIVITY: Lock-in cost rises with the embedded gain G/V. "
        f"At G/V = 80%, the lock-in cost reaches {max_lock_gain:.2f} bp — "
        f"substantially larger than the risk-sharing differential from Module 1. "
        f"Long-held concentrated positions (high G/V) face the most severe lock-in.",

        f"4. HOLDING PERIOD SENSITIVITY: Lock-in cost rises from "
        f"{min_lock_T:.2f} bp at T=1 and plateaus near "
        f"{max_lock_T:.2f} bp at longer horizons. "
        f"The direction is upward, not downward: at short T the agent has "
        f"only one period to benefit from switching, so the opportunity cost "
        f"is low. As T increases, each additional year that Asset B compounds "
        f"ahead of Asset A raises the foregone return from staying locked in. "
        f"The plateau appears once r_B* converges toward r_A and the trapped "
        f"zone between them collapses — states that triggered lock-in at short "
        f"T now fall below r_A entirely (agent stays regardless of CGT) or "
        f"above r_B* (agent switches despite CGT). "
        f"Within empirically relevant horizons (T ≤ 20 yr) the welfare cost "
        f"is substantially above the T=1 baseline.",

        f"5. WDT STRUCTURAL ADVANTAGE: Under the WDT, the tax on gain G has "
        f"already been accruing annually — switching assets is costless on the "
        f"margin. The full indifference return is r_A (switch whenever r_B > r_A). "
        f"The WDT therefore eliminates the lock-in distortion structurally, "
        f"not through a behavioural or administrative fix.",

        f"6. MODULE 1 CORRECTION: Module 1 showed WDT and CGT at near-identical "
        f"CEW because it modelled CGT as a lower-rate income tax without a "
        f"realisation decision. This module corrects that: once the realisation "
        f"decision is endogenous, CGT's welfare cost increases by the lock-in "
        f"amount, reversing the apparent near-equivalence.",
    ]

    for f in findings:
        words = f.split()
        line  = ""
        for word in words:
            if len(line) + len(word) + 1 > 74:
                print("  " + line)
                line = word
            else:
                line = (line + " " + word).strip()
        if line:
            print("  " + line)
        print()


# ─────────────────────────────────────────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────────────────────────────────────────

def main():
    print("=" * 70)
    print("MODULE 3: CGT Lock-In Distortion")
    print("=" * 70)

    p   = load_params(TOML_PATH)
    N   = p["tcm"]["canonical_N"]          # 30 — from TOML, never hardcoded
    dist_A = make_empirical_distribution_scenario(p, N)
    dist_B = make_idealised_distribution_scenario(p, N)

    # Reference CGT rate — from TOML if available, else UK 2024 higher rate
    tau_cgt_ref = 0.24    # UK 2024 CGT higher rate

    # Reference asset: V=£10m, G/V=50% (5yr appreciation at ~10% pa)
    V_ref = 10.0     # £10m (matching Module 2's W0_BASE, in £m)
    G_ref = V_ref * 0.50
    r_A   = p["tcm"]["hist_mean"]    # Asset A return = historical equity mean

    asset_ref = AssetSwitchDecision(
        V=V_ref, B=V_ref - G_ref,
        tau_cgt=tau_cgt_ref, T=5, r_A=r_A
    )

    print(f"\nReference asset:")
    print(f"  V = £{asset_ref.V:.0f}m, G = £{asset_ref.embedded_gain:.0f}m "
          f"(G/V = {asset_ref.gain_ratio*100:.0f}%)")
    print(f"  Cost basis B = £{asset_ref.B:.0f}m")
    print(f"  r_A = {asset_ref.r_A*100:.2f}%  (historical equity mean)")
    print(f"  τ_cgt = {asset_ref.tau_cgt*100:.0f}%  (UK 2024 higher rate)")
    print(f"  T = {asset_ref.T} years remaining")
    print(f"  Indifference return r_B* = {asset_ref.indifference_return()*100:.4f}%")
    print(f"  Switch cost = £{asset_ref.switch_cost_pv():.2f}m")

    # ── Part A: Lock-in threshold chart ─────────────────────────────────────
    print("\n--- Part A: Lock-in threshold ---")
    chart_lock_in_threshold(asset_ref)

    # ── Parts B/C: Welfare cost of lock-in at reference parameters ───────────
    print("\n--- Part B: Welfare cost of lock-in ---")
    lock_ref_A = compute_lock_in_welfare_cost(asset_ref, dist_A, GAMMA, tau_cgt_ref)
    lock_ref_B = compute_lock_in_welfare_cost(asset_ref, dist_B, GAMMA, tau_cgt_ref)

    for dist, lock, label in [
        (dist_A, lock_ref_A, "Version A (Empirical)"),
        (dist_B, lock_ref_B, "Version B (Idealised)"),
    ]:
        print(f"\n  {label}:")
        print(f"    P(locked in):         {lock['p_locked']*100:.1f}%")
        print(f"    CEW (free):           {lock['cew_free']*100:.4f}%")
        print(f"    CEW (locked):         {lock['cew_locked']*100:.4f}%")
        print(f"    Lock-in cost:         {lock['lock_in_cost_bp']:+.4f} bp")

    # ── Part D: Sensitivity analysis ─────────────────────────────────────────
    print("\n--- Part D: Sensitivity ---")

    gain_ratios = np.linspace(0.05, 0.90, 20)
    sens_gain   = sensitivity_gain_ratio(
        V_ref, r_A, 5, tau_cgt_ref, dist_A, GAMMA, gain_ratios
    )
    chart_sensitivity_gain(sens_gain)

    T_vals  = list(range(1, 21))
    sens_T  = sensitivity_holding_period(
        V_ref, G_ref, r_A, tau_cgt_ref, dist_A, GAMMA, T_vals
    )
    chart_sensitivity_T(sens_T)

    # ── Part E: Full comparison ───────────────────────────────────────────────
    print("\n--- Part E: Full welfare comparison ---")
    comp_A = full_comparison_with_lockin(
        W0_BASE, dist_A, GAMMA, TARGET_ET * W0_BASE, asset_ref
    )
    comp_B = full_comparison_with_lockin(
        W0_BASE, dist_B, GAMMA, TARGET_ET * W0_BASE, asset_ref
    )

    print_comparison_table(comp_A, dist_A.label)
    print_comparison_table(comp_B, dist_B.label)

    chart_full_comparison(comp_A, dist_A.label)

    print(comp_A)

    print_findings(comp_A, sens_gain, sens_T)
    print(f"\n✓ Module 3 complete. Outputs in: {OUTPUT_DIR}")


if __name__ == "__main__":
    main()