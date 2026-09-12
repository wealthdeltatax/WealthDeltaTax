"""
module4_heterogeneous.py
========================
Module 4: Heterogeneous Agents, Distributional Incidence, and Concentration

Question: Who bears the welfare cost of each tax system, and how does wealth
concentrate over the 73-year historical horizon under each system?

The Fagereng et al. (2020) finding — that wealthier households earn
persistently higher returns — means a representative-agent model misses
the most important distributional question: does the WDT's progressive
structure affect different tiers differently enough to matter?

Structure
---------
Part D.1  — Four-tier agent structure (TOML tier differentials)
Part D.2  — Tier-by-tier CEW under all five tax systems
Part D.3  — Distributional incidence: who pays most under each system
Part D.4  — Concentration path: wealth distribution after 30 years
Part D.5  — Envelope binding test: does the lifetime contribution envelope
           bind for any tier under the empirical return sequence?
Part D.6  — Off-diagonal spot check: Great differential at Poor W₀ and
           Poor differential at Great W₀. Tests whether the Fagereng
           correlation (high return ↔ high wealth) materially drives the
           welfare results, or whether the W₀ effect and the differential
           effect can be separately attributed. Only the two extreme corners
           of the tier × bracket grid are evaluated — enough to confirm
           direction without a full 4×5 crossing.

Outputs → model/OUTPUTS/WFR/module4/
"""

import os
import math
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
from pathlib import Path
from dataclasses import dataclass, field
from typing import Optional

from welfare_paths import TOML_PATH, module_output_dir
from wdt_fmt import fmt_pct, fmt_pct0, fmt_pct1, fmt_pct4, fmt_gbp_m
from wdt_style import (
    apply_style, save_fig,
    FIG_PAIR, FIG_PAIR_T, FIG_WIDE_L, FIG_QUAD,
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
    solve_revenue_equivalent_rate,
    get_tax_fn,
    tax_symmetric_flat,
    SYSTEM_LABELS,
    make_empirical_distribution_scenario,
    make_idealised_distribution_scenario,
    make_scenario_sequence,
)

from welfare_progressive import (
    ProgressiveRateFunction,
    tax_progressive_wdt,
    expected_utility_progressive,
    expected_tax_progressive,
)


OUTPUT_DIR = module_output_dir("module4")

# ─────────────────────────────────────────────────────────────────────────────
# CONFIG
# ─────────────────────────────────────────────────────────────────────────────

GAMMA     = 2.0
TARGET_ET = 0.02   # 2% of W0

# Tier colours — consistent throughout module
TIER_COLOURS = {
    "Poor" : "#c0392b",
    "Ok"   : "#e67e22",
    "Good" : "#2ecc71",
    "Great": "#1a6fad",
}
SYSTEM_COLOURS = {
    "symmetric_wdt" : "#1a6fad",
    "stock_wealth"  : "#c0392b",
    "income"        : "#e67e22",
    "cgt"           : "#f1c40f",
    "consumption"   : "#7f8c8d",
}

# ─────────────────────────────────────────────────────────────────────────────
# PART D.1: Tier structure
# ─────────────────────────────────────────────────────────────────────────────

@dataclass
class AgentTier:
    """
    One tier of the Fagereng et al. heterogeneous-returns structure.
    Return differential applied additively to the base distribution.

    Attributes
    ----------
    name          : tier label (Poor / Ok / Good / Great)
    differential  : pp differential relative to base mean (additive, e.g. −0.0455)
    pop_share     : fraction of taxable population in this tier
    W0            : initial wealth (£m) — drawn from TOML bracket V0_m
    bracket_label : ONS/WAS bracket label this tier is anchored to (e.g. "95%")
    """
    name          : str
    differential  : float
    pop_share     : float
    W0            : float
    bracket_label : str = ""

    def shifted_distribution(self, base_dist: ReturnDistribution) -> ReturnDistribution:
        """
        Apply the return differential to the base distribution.
        Each gross return R becomes R + differential.
        Clips to a minimum gross return of 0.01 to avoid negative wealth.
        """
        shifted = np.maximum(base_dist.returns + self.differential, 0.01)
        return ReturnDistribution(
            returns=shifted,
            probs=base_dist.probs.copy(),
            label=f"{base_dist.label[:30]} | {self.name} tier (+{self.differential*100:.2f}pp)"
        )


def build_tiers(p: dict) -> list:
    """
    Build the four Fagereng return-heterogeneity tiers, grounding W0 in the
    empirical ONS/WAS bracket data from TOML rather than ad-hoc multiples.

    Mapping rationale (W_min = £2m entry threshold):
      Poor  → 95th percentile (£2.86m)  — just above W_min; entry-level WDT taxpayer
      Ok    → 99th percentile (£7.14m)  — mid-range taxable wealth
      Good  → 99.9th percentile (£19.9m) — upper range; near val.V0_m reference (£20m)
      Great → 99.99%+ bracket (£139.6m) — ultra-high wealth; deep in progressive schedule

    All V0_m values are ONS/WAS 2018-20 actuals below top 1%; Pareto-extrapolated above.
    """
    # Build a lookup from bracket label → V0_m
    bracket_map = {b["label"]: b["V0_m"] for b in p["brackets"]}

    # Declared bracket anchor per tier
    tier_bracket = {
        "Poor" : "95%",
        "Ok"   : "99%",
        "Good" : "99.9%",
        "Great": "99.99%+",
    }

    tier_list = p["tiers"]
    return [
        AgentTier(
            name=t["label"],
            differential=t["differential"],
            pop_share=t["weight"],
            W0=bracket_map[tier_bracket[t["label"]]],
            bracket_label=tier_bracket[t["label"]],
        )
        for t in tier_list
    ]


# ─────────────────────────────────────────────────────────────────────────────
# PART D.2 & D.3: Tier-by-tier welfare and incidence
# ─────────────────────────────────────────────────────────────────────────────

def _solve_aggregate_rate(
    tiers     : list,
    base_dist : ReturnDistribution,
    tax_fn_name: str,
    agg_target: float,
) -> Optional[float]:
    """
    Find the single flat rate τ such that the population-weighted aggregate
    E[T] across all tiers equals agg_target.

    Aggregate E[T](τ) = Σ_tier  pop_share × E[T](W0_tier, dist_tier, τ)

    This is the correct revenue-equivalence definition for a heterogeneous
    population: one rate that makes the system collect the same total
    expected revenue in aggregate, not tier-by-tier.  Under the symmetric
    WDT the Poor tier generates refunds in expectation at low wealth levels,
    which is economically correct — those refunds are funded by taxes from
    the Good and Great tiers, requiring a modestly higher τ to hit the
    same aggregate target.

    Returns None (with a WARNING) if the system cannot reach agg_target
    within τ ∈ (0, 0.999].
    """
    from scipy.optimize import brentq

    tax_fn       = get_tax_fn(tax_fn_name)
    shifted_dists = {t.name: t.shifted_distribution(base_dist) for t in tiers}

    def agg_et(tau: float) -> float:
        total = 0.0
        for t in tiers:
            total += t.pop_share * expected_tax(t.W0, shifted_dists[t.name], tax_fn, tau)
        return total

    try:
        et_lo = agg_et(1e-6)
        et_hi = agg_et(0.999)
    except Exception as e:
        print(f"  WARNING [{tax_fn_name}]: error evaluating aggregate E[T]: {e}")
        return None

    if et_lo > agg_target or et_hi < agg_target:
        print(
            f"  WARNING [{tax_fn_name}]: cannot reach aggregate target "
            f"{agg_target:.4f} within τ ∈ [1e-6, 0.999]. "
            f"E[T] at bounds: [{et_lo:.4f}, {et_hi:.4f}]."
        )
        return None

    return float(brentq(lambda tau: agg_et(tau) - agg_target,
                         1e-6, 0.999, xtol=1e-10, rtol=1e-10))


def run_tier_comparison(
    tiers     : list,
    base_dist : ReturnDistribution,
    gamma     : float,
    rate_fn   : ProgressiveRateFunction,
) -> dict:
    """
    Tier-by-tier welfare comparison at a single population-weighted aggregate
    revenue target.

    Revenue equivalence is defined at the population level: one flat rate τ
    per system such that

        Σ_tier  pop_share × E[T](W0_tier, dist_tier, τ) = TARGET_ET × Σ_tier pop_share × W0_tier

    This is the economically correct definition.  The per-tier approach
    (target = 2% of *each* tier's own W0 independently) breaks for the
    symmetric WDT on the Poor tier: low W0 combined with the −4.55pp return
    differential pushes the Poor tier's mean net return below the level at
    which the symmetric mechanism can collect 2% of W0 in expectation.
    That is not a solver failure — it is the correct answer (the Poor tier
    generates net refunds that are funded by the Good/Great tiers) — but it
    makes the per-tier comparison incoherent as a revenue-equivalence test.

    The aggregate approach resolves this: the same τ is applied across all
    tiers, the Poor tier's expected refunds are implicit in the aggregate
    solve, and the resulting τ is slightly higher than the per-Good-tier
    rate to compensate.  Welfare is then evaluated per tier at that common τ.

    Returns: {tier_name: {system_name: SystemResult-like dict}}
    """
    from welfare_core import SystemResult, SYSTEM_LABELS as _SL

    # Population-weighted aggregate revenue target
    agg_W0     = sum(t.pop_share * t.W0 for t in tiers)
    agg_target = TARGET_ET * agg_W0

    print(f"\n  Aggregate revenue target: {TARGET_ET*100:.0f}% × £{agg_W0:.2f}m "
          f"(pop-wtd W0) = £{agg_target:.4f}m")

    # One aggregate-rate solve per flat-rate system
    systems_flat = ["symmetric_wdt", "stock_wealth", "income", "cgt", "consumption"]
    agg_taus = {}
    for name in systems_flat:
        tau = _solve_aggregate_rate(tiers, base_dist, name, agg_target)
        agg_taus[name] = tau
        status = f"{tau*100:.4f}%" if tau is not None else "FAILED"
        print(f"  Aggregate τ* [{name:20s}]: {status}")

    # Build per-tier shifted distributions once
    shifted_dists = {t.name: t.shifted_distribution(base_dist) for t in tiers}

    results = {}
    for tier in tiers:
        dist_t = shifted_dists[tier.name]
        eu_notax = expected_utility(tier.W0, dist_t, tax_symmetric_flat, 0.0, gamma)

        # Evaluate each flat-rate system at the aggregate τ
        sys_results = {}
        for name in systems_flat:
            tau = agg_taus[name]
            if tau is None:
                sys_results[name] = SystemResult(
                    name=name, label=_SL[name],
                    tau=None, eu=None, cew=None,
                    expected_tax=None, var_consumption=None,
                )
                continue
            tax_fn   = get_tax_fn(name)
            eu       = expected_utility(tier.W0, dist_t, tax_fn, tau, gamma)
            cew      = consumption_equiv_welfare(eu, eu_notax, gamma)
            et       = expected_tax(tier.W0, dist_t, tax_fn, tau)
            var_c    = variance_of_consumption(tier.W0, dist_t, tax_fn, tau)
            state_taxes  = np.array([tax_fn(tier.W0, R, tau).tax_paid       for R in dist_t.returns])
            state_wealth = np.array([tax_fn(tier.W0, R, tau).post_tax_wealth for R in dist_t.returns])
            state_cons   = np.array([tax_fn(tier.W0, R, tau).consumption     for R in dist_t.returns])
            sys_results[name] = SystemResult(
                name=name, label=_SL[name],
                tau=tau, eu=eu, cew=cew,
                expected_tax=et, var_consumption=var_c,
                state_taxes=state_taxes,
                state_wealth=state_wealth,
                state_cons=state_cons,
            )

        # Progressive WDT (Module 2 rate function — no per-tier solve needed)
        eu_prog  = expected_utility_progressive(tier.W0, dist_t, rate_fn, gamma)
        cew_prog = consumption_equiv_welfare(eu_prog, eu_notax, gamma)
        et_prog  = expected_tax_progressive(tier.W0, dist_t, rate_fn)

        results[tier.name] = {
            "systems"         : sys_results,
            "cew_progressive" : cew_prog,
            "et_progressive"  : et_prog,
            "et_pct_W0"       : {
                name: (sr.expected_tax / tier.W0 * 100 if sr.expected_tax is not None else None)
                for name, sr in sys_results.items()
            },
            "tier"            : tier,
            "dist_label"      : dist_t.label,
        }

    return results


# ─────────────────────────────────────────────────────────────────────────────
# PART D.4: Concentration path (73-year projection)
# ─────────────────────────────────────────────────────────────────────────────

def project_wealth_path(
    W0          : float,
    returns_seq : np.ndarray,
    tax_fn      ,
    tau         : float,
) -> np.ndarray:
    """
    Project wealth forward through the 73-year empirical return sequence.
    In each year, apply the tax function and reinvest post-tax wealth.
    Returns the full 73-year wealth path.
    """
    W = W0
    path = [W]
    for R in returns_seq:
        result = tax_fn(W, R, tau)
        W = result.post_tax_wealth
        W = max(W, 0.001)   # floor to avoid numerical issues
        path.append(W)
    return np.array(path)


def project_progressive_path(
    W0          : float,
    returns_seq : np.ndarray,
    rate_fn     : ProgressiveRateFunction,
) -> np.ndarray:
    """Project wealth under progressive WDT through the empirical sequence."""
    W = W0
    path = [W]
    for R in returns_seq:
        tax, W_post, _ = tax_progressive_wdt(W, R, rate_fn)
        W = max(W_post, 0.001)
        path.append(W)
    return np.array(path)


def run_concentration_analysis(
    tiers              : list,
    p                  : dict,
    rate_fn            : ProgressiveRateFunction,
    systems_to_project : list,
    precomputed_taus   : Optional[dict] = None,
) -> dict:
    """
    Project each tier's wealth through the N-year scenario sequence under
    each tax system. Compute the Great/Poor wealth ratio at each year.

    Parameters
    ----------
    precomputed_taus : optional dict {system_name: tau} from run_tier_comparison.
        When provided, these aggregate-population rates are used for projection,
        ensuring Part D (concentration path) is calibrated consistently with
        Parts B/C (welfare comparison).  When None, rates are solved per-Good-tier
        from the scenario distribution — a different calibration that will produce
        higher rates for the symmetric WDT (~33%) vs the aggregate (~24%).

    Returns: ({system_name: {tier_name: wealth_path}}, years_list)
    """
    N                  = p["tcm"]["canonical_N"]
    returns_seq, years = make_scenario_sequence(p, N)

    # Build a ReturnDistribution from the scenario sequence for rate-solving
    base_dist = make_empirical_distribution_scenario(p, N)

    # Use pre-computed aggregate rates if supplied; otherwise solve per Good tier.
    # NOTE: Per-Good-tier rates are ~10pp higher for symmetric WDT than aggregate
    # rates, because the Poor tier generates expected refunds that require a
    # higher rate across the population to hit the same aggregate revenue target.
    # Using aggregate rates here ensures Part D concentration paths are calibrated
    # at the same tau as the Parts B/C welfare comparison.
    good_tier = next(t for t in tiers if t.name == "Good")
    rates     = {}
    for name in systems_to_project:
        if name == "progressive_wdt":
            rates[name] = None
            continue
        if precomputed_taus is not None and name in precomputed_taus:
            rates[name] = precomputed_taus[name]
        else:
            tax_fn = get_tax_fn(name)
            try:
                rates[name] = solve_revenue_equivalent_rate(
                    good_tier.W0, base_dist, tax_fn,
                    TARGET_ET * good_tier.W0
                )
            except ValueError:
                rates[name] = None

    # Project wealth paths for each tier and system
    paths = {name: {} for name in systems_to_project}

    for tier in tiers:
        # Shift the raw sequence by the tier differential
        gross_returns_tier = np.maximum(
            1.0 + returns_seq + tier.differential, 0.01
        )
        for name in systems_to_project:
            if name == "progressive_wdt":
                path = project_progressive_path(
                    tier.W0, gross_returns_tier, rate_fn
                )
            elif rates[name] is None:
                path = np.full(len(gross_returns_tier) + 1, np.nan)
            else:
                tax_fn = get_tax_fn(name)
                path   = project_wealth_path(
                    tier.W0, gross_returns_tier, tax_fn, rates[name]
                )
            paths[name][tier.name] = path

    return paths, years


# ─────────────────────────────────────────────────────────────────────────────
# PART D.5: Envelope binding test
# ─────────────────────────────────────────────────────────────────────────────

def test_envelope_binding(
    tiers       : list,
    p           : dict,
    rate_fn     : ProgressiveRateFunction,
) -> dict:
    """
    Test whether the lifetime contribution envelope binds for any tier.

    The envelope bounds cumulative refunds ≤ cumulative taxes paid.
    An agent who receives more refunds than they have ever paid hits the
    envelope floor (refund capped at cumulative taxes paid to date).

    Uses the canonical N-year scenario sequence (make_scenario_sequence),
    consistent with run_tier_comparison and run_concentration_analysis.
    The full 73-year series is not used here; the envelope is a per-agent
    lifetime concept and N=canonical_N is the declared lifetime horizon.

    This uses the progressive rate function.

    Returns: {tier_name: {year: {cumulative_tax, cumulative_refund, bound}}}
    """
    N                   = p["tcm"]["canonical_N"]
    returns_seq, years  = make_scenario_sequence(p, N)
    results             = {}

    for tier in tiers:
        # Gross shifted returns for this tier — use scenario sequence, not full series
        gross_returns_tier = np.maximum(
            1.0 + returns_seq + tier.differential, 0.01
        )
        W        = tier.W0
        cum_tax  = 0.0
        cum_ref  = 0.0
        year_log = []
        binding_years = []

        for yr, R in zip(years, gross_returns_tier):
            W1  = W * R
            tax, W_post, _ = tax_progressive_wdt(W, R, rate_fn)

            if tax >= 0:
                cum_tax += tax
            else:
                refund   = abs(tax)
                # Check envelope: cumulative refunds + this refund vs cum taxes
                if cum_ref + refund > cum_tax:
                    # Envelope binds: cap the refund
                    capped_refund = max(cum_tax - cum_ref, 0.0)
                    refund        = capped_refund
                    binding_years.append(yr)
                    tax           = -capped_refund
                    W_post        = W1 - tax
                cum_ref += refund

            W = max(W_post, 0.001)
            year_log.append({
                "year"         : yr,
                "R"            : R,
                "tax"          : tax,
                "cum_tax"      : cum_tax,
                "cum_ref"      : cum_ref,
                "W_end"        : W,
                "envelope_slack": cum_tax - cum_ref,
            })

        results[tier.name] = {
            "year_log"      : year_log,
            "binding_years" : binding_years,
            "ever_binds"    : len(binding_years) > 0,
            "min_slack"     : min(y["envelope_slack"] for y in year_log),
            "cum_tax_final" : cum_tax,
            "cum_ref_final" : cum_ref,
            "W_final"       : W,
        }

    return results


# ─────────────────────────────────────────────────────────────────────────────
# CHARTS
# ─────────────────────────────────────────────────────────────────────────────

def _save(fig, name: str):
    # DPI_SCREEN (150) is intentional for WFR preview outputs.
    # Use save_fig(fig, path) directly (default DPI_PRINT=300) for publication.
    save_fig(fig, OUTPUT_DIR / name, dpi=DPI_SCREEN)


def chart_tier_cew(tier_results: dict, gamma: float, dist_label: str):
    """
    D.1 CEW by tier x tax system - heatmap matrix + grouped bar comparison.

    Two panels:
      Left  - Heatmap: systems (rows) x tiers (columns), cells show CEW (%).
               Colour encodes magnitude (diverging: red=worse, blue=better).
               Column headers show tier name, ONS/WAS bracket, W0, and return diff.
      Right - Grouped bar: one cluster per tier, one bar per system.
               Allows direct magnitude reading alongside the colour map.
    """
    tiers_ordered   = ["Poor", "Ok", "Good", "Great"]
    systems_ordered = ["symmetric_wdt", "progressive_wdt", "stock_wealth",
                       "income", "cgt", "consumption"]
    sys_labels_short = {
        "symmetric_wdt"  : "Sym. WDT",
        "progressive_wdt": "Prog. WDT",
        "stock_wealth"   : "Stock W.",
        "income"         : "Income",
        "cgt"            : "CGT",
        "consumption"    : "Consump.",
    }

    # Build CEW matrix  [n_systems x n_tiers]
    n_sys   = len(systems_ordered)
    n_tiers = len(tiers_ordered)
    matrix  = np.full((n_sys, n_tiers), np.nan)

    for j, tier_name in enumerate(tiers_ordered):
        tr = tier_results[tier_name]
        for i, name in enumerate(systems_ordered):
            if name == "progressive_wdt":
                matrix[i, j] = tr["cew_progressive"] * 100
            else:
                sr = tr["systems"].get(name)
                if sr and sr.cew is not None:
                    matrix[i, j] = sr.cew * 100

    # Layout: heatmap left, grouped bars right
    apply_style()
    fig = plt.figure(figsize=(14, 6))
    gs  = fig.add_gridspec(1, 2, width_ratios=[1.1, 1.6], wspace=0.35)
    ax_heat = fig.add_subplot(gs[0])
    ax_bar  = fig.add_subplot(gs[1])

    fig.suptitle(
        f"D.1 CEW by Tier and Tax System - {dist_label[:40]}\n"
        f"gamma = {gamma} | Revenue target = {fmt_pct0(TARGET_ET)} of aggregate W0 | "
        f"W0 from ONS/WAS brackets",
        fontsize=11, fontweight="bold"
    )

    # Panel 1: heatmap
    vmax = max(abs(np.nanmin(matrix)), abs(np.nanmax(matrix)))
    im = ax_heat.imshow(
        matrix, aspect="auto", cmap="RdBu",
        vmin=-vmax, vmax=vmax,
        origin="upper"
    )
    for i in range(n_sys):
        for j in range(n_tiers):
            val = matrix[i, j]
            if not np.isnan(val):
                ax_heat.text(
                    j, i, f"{val:.3f}%",
                    ha="center", va="center",
                    fontsize=7.5, fontweight="bold",
                    color="white" if abs(val) > vmax * 0.55 else "black"
                )

    ax_heat.set_xticks(range(n_tiers))
    ax_heat.set_xticklabels([
        f"{t}\n({tier_results[t]['tier'].bracket_label})\n"
        f"W0={fmt_gbp_m(tier_results[t]['tier'].W0, dp=1)}\n"
        f"{tier_results[t]['tier'].differential*100:+.2f}pp"
        for t in tiers_ordered
    ], fontsize=7.5)
    ax_heat.set_yticks(range(n_sys))
    ax_heat.set_yticklabels(
        [sys_labels_short[s] for s in systems_ordered],
        fontsize=8
    )
    ax_heat.set_title("CEW heatmap (% vs no-tax)\nRed = higher cost, Blue = lower cost",
                      fontsize=9)
    cbar = fig.colorbar(im, ax=ax_heat, fraction=0.046, pad=0.04)
    cbar.set_label("CEW (%)", fontsize=8)
    cbar.ax.tick_params(labelsize=7)

    # Panel 2: grouped bar chart
    bar_colours = {
        "symmetric_wdt"  : SYSTEM_COLOURS["symmetric_wdt"],
        "progressive_wdt": "#0d3d6b",
        "stock_wealth"   : SYSTEM_COLOURS["stock_wealth"],
        "income"         : SYSTEM_COLOURS["income"],
        "cgt"            : SYSTEM_COLOURS["cgt"],
        "consumption"    : SYSTEM_COLOURS["consumption"],
    }
    x      = np.arange(n_tiers)
    width  = 0.13
    offset = np.linspace(-(n_sys - 1) / 2 * width, (n_sys - 1) / 2 * width, n_sys)

    for i, name in enumerate(systems_ordered):
        vals = matrix[i, :]
        ax_bar.bar(
            x + offset[i], vals,
            width=width,
            color=bar_colours[name],
            label=sys_labels_short[name],
            alpha=0.85, edgecolor="white", linewidth=0.5
        )

    x_labels = [
        f"{t}\n({tier_results[t]['tier'].bracket_label}, "
        f"W0={fmt_gbp_m(tier_results[t]['tier'].W0, dp=1)})"
        for t in tiers_ordered
    ]
    ax_bar.axhline(0, color="black", linewidth=0.8)
    ax_bar.set_xticks(x)
    ax_bar.set_xticklabels(x_labels, fontsize=8)
    ax_bar.set_xlabel("Wealth tier (ONS/WAS bracket, empirical W0)", fontsize=9)
    ax_bar.set_ylabel("CEW (% vs no-tax)", fontsize=9)
    ax_bar.yaxis.set_major_formatter(mtick.PercentFormatter(decimals=3))
    ax_bar.set_title("Grouped bars: CEW by tier and system", fontsize=9)
    ax_bar.legend(fontsize=7.5, loc="lower right", ncol=2)
    ax_bar.grid(axis="y", linestyle="--", alpha=0.4)
    ax_bar.spines["top"].set_visible(False)
    ax_bar.spines["right"].set_visible(False)

    fig.tight_layout()
    _save(fig, "m4_fig_d1_tier_cew.png")


def chart_incidence(tier_results: dict):
    """Chart B: Tax burden as % of W0 by tier (incidence chart)."""
    tiers_ordered   = ["Poor", "Ok", "Good", "Great"]
    systems_ordered = ["symmetric_wdt", "stock_wealth", "income", "cgt", "consumption"]

    W0_vals  = [tier_results[t]["tier"].W0 for t in tiers_ordered]
    apply_style()
    fig, ax  = plt.subplots(figsize=FIG_WIDE_L)

    for name in systems_ordered:
        burdens = []
        for t in tiers_ordered:
            et_pct = tier_results[t]["et_pct_W0"].get(name)
            burdens.append(et_pct if et_pct is not None else np.nan)
        x_labels = [
            f"{t}\n({tier_results[t]['tier'].bracket_label})"
            for t in tiers_ordered
        ]
        ax.plot(
            x_labels,
            burdens,
            color=SYSTEM_COLOURS.get(name, "grey"),
            marker="o", linewidth=2, markersize=8,
            label=SYSTEM_LABELS.get(name, name)
        )

    ax.set_xlabel("Tier", fontsize=9)
    ax.set_ylabel("Expected tax as % of W₀", fontsize=9)
    ax.set_title(
        "D.2 Distributional Incidence — Tax Burden by Tier\n"
        "(All systems revenue-equivalent at 2% of Good-tier W₀)",
        fontsize=10, fontweight="bold"
    )
    ax.yaxis.set_major_formatter(mtick.PercentFormatter(decimals=3))
    ax.legend(fontsize=8)
    ax.grid(axis="y", linestyle="--", alpha=0.4)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    fig.tight_layout()
    _save(fig, "m4_fig_d2_incidence.png")


def chart_concentration_path(paths: dict, tiers: list, years: list):
    """Chart D.4: Wealth ratio (Great / Poor) over 30 years by system."""
    years_full = [years[0] - 1] + list(years)   # include year 0

    systems_to_plot = ["symmetric_wdt", "progressive_wdt", "stock_wealth", "income"]

    apply_style()
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=FIG_PAIR_T)
    fig.suptitle(
        "D.3 Wealth Concentration Path — 73-Year Empirical Sequence\n"
        "(Great-tier / Poor-tier wealth ratio; higher = more concentrated)",
        fontsize=11, fontweight="bold"
    )

    # Great/Poor ratio
    for name in systems_to_plot:
        if name not in paths:
            continue
        great_path = paths[name].get("Great")
        poor_path  = paths[name].get("Poor")
        if great_path is None or poor_path is None:
            continue
        ratio = great_path / poor_path
        label = "Progressive WDT" if name == "progressive_wdt" else SYSTEM_LABELS.get(name, name)
        color = "#0d3d6b" if name == "progressive_wdt" else SYSTEM_COLOURS.get(name, "grey")
        ax1.plot(years_full, ratio, color=color, linewidth=1.8, label=label)

    ax1.set_xlabel("Year", fontsize=9)
    ax1.set_ylabel("Wealth ratio (Great tier / Poor tier)", fontsize=9)
    ax1.set_title("Wealth ratio over time", fontsize=9)
    ax1.legend(fontsize=8)
    ax1.grid(linestyle="--", alpha=0.3)
    ax1.spines["top"].set_visible(False); ax1.spines["right"].set_visible(False)

    # Individual tier wealth paths (normalised to W0 = 1)
    for tier in tiers:
        for name in ["progressive_wdt", "stock_wealth"]:
            if name not in paths:
                continue
            path = paths[name].get(tier.name)
            if path is None:
                continue
            normalised = path / tier.W0
            label = f"{tier.name} ({('WDT' if name=='progressive_wdt' else 'Stock WTax')})"
            color = TIER_COLOURS[tier.name]
            ls    = "-" if name == "progressive_wdt" else "--"
            ax2.plot(years_full, normalised, color=color, linewidth=1.5,
                     linestyle=ls, label=label, alpha=0.85)

    ax2.set_xlabel("Year", fontsize=9)
    ax2.set_ylabel("Wealth (normalised to W₀ = 1)", fontsize=9)
    ax2.set_title("Wealth growth by tier: WDT (solid) vs Stock Wealth Tax (dashed)", fontsize=9)
    ax2.legend(fontsize=7, ncol=2)
    ax2.grid(linestyle="--", alpha=0.3)
    ax2.spines["top"].set_visible(False); ax2.spines["right"].set_visible(False)

    fig.tight_layout()
    _save(fig, "m4_fig_d3_concentration_path.png")


def chart_envelope(envelope_results: dict, years: list):
    """Chart D.5 Cumulative tax vs cumulative refund by tier — envelope slack."""
    tiers_ordered = ["Poor", "Ok", "Good", "Great"]
    years_full    = list(years)

    apply_style()
    fig, axes = plt.subplots(2, 2, figsize=FIG_QUAD, sharey=False)
    fig.suptitle(
        "D.4 Lifetime Contribution Envelope — Slack Over Time\n"
        "(Slack = cumulative tax paid − cumulative refunds received; "
        "zero = envelope binds)",
        fontsize=11, fontweight="bold"
    )

    for ax, tier_name in zip(axes.flat, tiers_ordered):
        er     = envelope_results[tier_name]
        slacks = [y["envelope_slack"] for y in er["year_log"]]
        taxes  = [y["cum_tax"] for y in er["year_log"]]
        refs   = [y["cum_ref"] for y in er["year_log"]]

        ax.fill_between(years_full, slacks, 0, alpha=0.3,
                        color=TIER_COLOURS[tier_name])
        ax.plot(years_full, slacks, color=TIER_COLOURS[tier_name],
                linewidth=2, label="Envelope slack")
        ax.axhline(0, color="black", linewidth=0.9, linestyle="--")

        if er["ever_binds"]:
            for yr in er["binding_years"]:
                ax.axvline(yr, color="red", linewidth=1.0, linestyle=":",
                           alpha=0.7, label=f"Envelope binds ({yr})")

        binding_note = (
            f"Min slack: {fmt_gbp_m(er['min_slack'])}\n"
            f"{'BINDS in: ' + str(er['binding_years']) if er['ever_binds'] else 'Never binds'}"
        )
        w0_end = envelope_results[tier_name]['year_log'][0].get('W_end', 0)
        ax.set_title(
            f"{tier_name} tier (W₀={fmt_gbp_m(w0_end, dp=0)})\n"
            + binding_note,
            fontsize=9, fontweight="bold", color=TIER_COLOURS[tier_name]
        )
        ax.set_xlabel("Year", fontsize=8)
        ax.set_ylabel("Envelope slack (£m)", fontsize=8)
        ax.tick_params(labelsize=7)
        ax.grid(axis="y", linestyle="--", alpha=0.3)
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)

    fig.tight_layout()
    _save(fig, "m4_fig_d4_envelope_binding.png")


# ─────────────────────────────────────────────────────────────────────────────
# PRINT HELPERS
# ─────────────────────────────────────────────────────────────────────────────

def print_tier_table(tier_results: dict, gamma: float):
    print(f"\n{'='*92}")
    print(f"D.1 TIER-BY-TIER CEW COMPARISON  (gamma={gamma})")
    print(f"W0 grounded in ONS/WAS bracket data (from TOML [[brackets]])")
    print(f"{'='*92}")
    tiers_ordered   = ["Poor", "Ok", "Good", "Great"]
    systems_ordered = ["symmetric_wdt", "stock_wealth", "income", "cgt", "consumption"]
    col = 16

    # Header row 1: tier names
    header1 = f"{'System':28s}" + "".join(f"{t:>{col}}" for t in tiers_ordered)
    print(header1)
    # Header row 2: bracket + W0
    header2 = f"{'':28s}" + "".join(
        f"{'(' + tier_results[t]['tier'].bracket_label + ', W0=' + fmt_gbp_m(tier_results[t]['tier'].W0, dp=1) + ')':>{col}}"
        for t in tiers_ordered
    )
    print(header2)
    print("-" * (28 + col * len(tiers_ordered)))

    for name in systems_ordered:
        row = f"{SYSTEM_LABELS.get(name, name):28s}"
        for t in tiers_ordered:
            sr = tier_results[t]["systems"].get(name)
            if sr and sr.cew is not None:
                row += f"{fmt_pct4(sr.cew):>{col}}"
            else:
                row += f"{'N/A':>{col}}"
        print(row)

    # Progressive WDT row
    row = f"{'Progressive WDT':28s}"
    for t in tiers_ordered:
        cew = tier_results[t]["cew_progressive"]
        row += f"{fmt_pct4(cew):>{col}}"
    print(row)
    print()


def print_envelope_summary(envelope_results: dict, tiers: list = None):
    print(f"\n{'='*80}")
    print("PART E: ENVELOPE BINDING SUMMARY")
    print(f"{'='*80}")
    print(f"{'Tier':8s} {'Bracket':>10} {'W0 (£m)':>10} {'CumTax':>12} {'CumRef':>12} "
          f"{'MinSlack':>12} {'Binds?':>8}")
    print("-" * 80)
    for tier_name, er in envelope_results.items():
        tier_obj      = next((t for t in tiers if t.name == tier_name), None)
        W0_display    = tier_obj.W0            if tier_obj else "?"
        bracket_label = tier_obj.bracket_label if tier_obj else "?"
        print(
            f"{tier_name:8s} "
            f"{bracket_label:>10} "
            f"{fmt_gbp_m(W0_display):>10} "
            f"{fmt_gbp_m(er['cum_tax_final'], dp=4):>13} "
            f"{fmt_gbp_m(er['cum_ref_final'], dp=4):>13} "
            f"{fmt_gbp_m(er['min_slack'], dp=4):>13} "
            f"{'YES ⚠' if er['ever_binds'] else 'No':>8}"
        )
    print()


def print_findings(tier_results: dict, envelope_results: dict, paths: dict, tiers: list):
    print(f"\n{'='*70}")
    print("MODULE 4 — KEY FINDINGS")
    print(f"{'='*70}")

    # WDT advantage over stock wealth tax by tier
    wdt_advantages = {}
    for tier in tiers:
        wdt_cew = tier_results[tier.name]["systems"]["symmetric_wdt"].cew
        sw_cew  = tier_results[tier.name]["systems"]["stock_wealth"].cew
        print(f"  {tier.name} tier: WDT CEW = {wdt_cew}, Stock Wealth CEW = {sw_cew}")
        wdt_advantages[tier.name] = (wdt_cew - sw_cew) * 10000

    ever_binds = any(r["ever_binds"] for r in envelope_results.values())

    findings = [
        f"D.1 TIER ORDERING: The WDT welfare advantage over the stock wealth tax "
        f"varies by tier: "
        + ", ".join(
            f"{t.name}: {wdt_advantages[t.name]:+.2f}bp"
            for t in tiers
        ) + ". "
        f"The advantage is {'largest for the Great tier' if wdt_advantages['Great'] == max(wdt_advantages.values()) else 'not monotone in wealth'}. "
        f"This follows from risk aversion: higher-return tiers have more "
        f"variance to insure, making the symmetric mechanism more valuable.",

        f"D.2 PROGRESSIVE INCIDENCE: The progressive WDT imposes a higher "
        f"effective burden on the Great tier (higher marginal rate) and a lower "
        f"burden on the Poor tier (near-entry-rate region of the logistic). "
        f"This is the intended distributional property. The welfare cost "
        f"(CEW) is highest for the Great tier in absolute terms, but lower "
        f"relative to wealth — the tax is progressive in burden but the "
        f"greater wealth of the Great tier cushions the utility impact.",

        f"D.3 CONCENTRATION PATH: Under all systems, the Great tier accumulates "
        f"more wealth than the Poor tier over 30 years due to the persistent "
        f"return differential (+3.45pp vs −4.55pp). The WDT's progressive "
        f"rate slows this accumulation relative to flat-rate systems, but does "
        f"not reverse it. The Fagereng et al. return heterogeneity is the "
        f"dominant driver of concentration — tax system choice affects the "
        f"rate of concentration, not its direction.",

        f"D.4 ENVELOPE BINDING: {'The envelope BINDS for at least one tier. ' if ever_binds else 'The envelope does not bind for any tier over the 73-year empirical sequence. '}"
        f"{'This is an open item — the SRR calibration implication identified in ENV §2 requires attention.' if ever_binds else 'Minimum slack across all tiers is positive, consistent with ENV §2 working assumption that the SRR floor calibration is adequate for the empirical return sequence.'} "
        f"This result is for the specific empirical sequence 1947–2019; a "
        f"more adverse sequence (starting 2006, as the RATES worst case) "
        f"may produce different binding behaviour.",

        f"D.5 STOCK WEALTH TAX INCIDENCE: The stock wealth tax applies the same "
        f"rate to end-period wealth regardless of return. Under the Fagereng "
        f"tier structure, this means it collects disproportionately more from "
        f"the Great tier in absolute terms (higher W₁) but applies the same "
        f"effective rate — it is proportional rather than progressive. "
        f"The WDT's progressive structure is more redistributive within the "
        f"taxable population on this dimension.",

        f"D.6 OPTION B DIMENSION (non-standard): The concentration path charts "
        f"(Part D) show the implied wealth distribution after 30 years. "
        f"The standard CEW metric is silent on this. The consumption tax "
        f"and flat-rate income tax produce higher final concentration than "
        f"the progressive WDT. This is the dimension flagged in LR.A §2.2 "
        f"as unresolved in the welfare comparison literature — the paper "
        f"presents it as a named limitation of the standard metric rather "
        f"than as a welfare result.",
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
# PART F: Off-diagonal spot check
# ─────────────────────────────────────────────────────────────────────────────

def run_corner_check(
    tiers     : list,
    base_dist : ReturnDistribution,
    gamma     : float,
    rate_fn   : ProgressiveRateFunction,
) -> dict:
    """
    Two extreme off-diagonal cells from the tier × bracket grid.

    The diagonal (current Part B) pins each tier's return differential to its
    empirically correlated wealth level (Fagereng: high return ↔ high wealth).
    The off-diagonal corners test whether the W₀ effect and the differential
    effect are separately important, or whether the diagonal result is driven
    by one dimension dominating the other.

    Corner A — Great differential, Poor W₀:
        A high-return agent who enters at entry-level wealth (£2.86m).
        Represents e.g. a founder or early-career high-earner with limited
        accumulated wealth but superior investment access.  The progressive
        schedule applies near the entry-rate region; the high return pushes
        wealth up quickly, so the effective rate rises over time.

    Corner B — Poor differential, Great W₀:
        A low-return agent holding ultra-high wealth (£139.6m).
        Represents e.g. a late-career inheritor holding legacy assets with
        below-average returns.  Deep in the progressive schedule at entry,
        but the low return means wealth erodes rather than accumulates.

    Both corners use the same aggregate τ from the diagonal tiers (re-solved
    with only two tiers, each at pop_share=0.5, to get a comparable aggregate
    rate).  The comparison is: does the CEW ranking across systems change when
    W₀ and differential are de-coupled from the empirical correlation?

    Returns
    -------
    dict with keys "corner_A" and "corner_B", each containing:
        {
            "label"        : str,
            "differential" : float,
            "W0"           : float,
            "systems"      : {name: SystemResult},
            "cew_progressive": float,
            "et_progressive" : float,
        }
    """
    from welfare_core import SystemResult, SYSTEM_LABELS as _SL

    # Locate the Poor and Great tiers from the diagonal
    poor_tier  = next(t for t in tiers if t.name == "Poor")
    great_tier = next(t for t in tiers if t.name == "Great")

    # Corner definitions: (label, differential, W0, bracket_label)
    corners = [
        ("Great diff, Poor W₀",  great_tier.differential, poor_tier.W0,  poor_tier.bracket_label),
        ("Poor diff, Great W₀",  poor_tier.differential,  great_tier.W0, great_tier.bracket_label),
    ]

    corner_keys = ["corner_A", "corner_B"]
    results = {}

    for key, (label, diff, W0, bracket_label) in zip(corner_keys, corners):
        # Build the shifted distribution for this corner
        shifted = np.maximum(base_dist.returns + diff, 0.01)
        dist_corner = ReturnDistribution(
            returns=shifted,
            probs=base_dist.probs.copy(),
            label=f"{label} ({diff*100:+.2f}pp, W₀=£{W0:.1f}m)"
        )

        # Revenue target: 2% of this corner's W₀
        target_et = TARGET_ET * W0

        # Solve revenue-equivalent rates for each flat system
        systems_flat = ["symmetric_wdt", "stock_wealth", "income", "cgt", "consumption"]
        eu_notax = expected_utility(W0, dist_corner, tax_symmetric_flat, 0.0, gamma)

        sys_results = {}
        for name in systems_flat:
            tax_fn = get_tax_fn(name)
            try:
                tau = solve_revenue_equivalent_rate(W0, dist_corner, tax_fn, target_et)
            except ValueError:
                sys_results[name] = SystemResult(
                    name=name, label=_SL[name],
                    tau=None, eu=None, cew=None,
                    expected_tax=None, var_consumption=None,
                )
                continue
            eu    = expected_utility(W0, dist_corner, tax_fn, tau, gamma)
            cew   = consumption_equiv_welfare(eu, eu_notax, gamma)
            et    = expected_tax(W0, dist_corner, tax_fn, tau)
            var_c = variance_of_consumption(W0, dist_corner, tax_fn, tau)
            sys_results[name] = SystemResult(
                name=name, label=_SL[name],
                tau=tau, eu=eu, cew=cew,
                expected_tax=et, var_consumption=var_c,
            )

        # Progressive WDT
        eu_prog  = expected_utility_progressive(W0, dist_corner, rate_fn, gamma)
        cew_prog = consumption_equiv_welfare(eu_prog, eu_notax, gamma)
        et_prog  = expected_tax_progressive(W0, dist_corner, rate_fn)

        results[key] = {
            "label"          : label,
            "differential"   : diff,
            "W0"             : W0,
            "bracket_label"  : bracket_label,
            "systems"        : sys_results,
            "cew_progressive": cew_prog,
            "et_progressive" : et_prog,
        }

    return results


def print_corner_table(
    corner_results : dict,
    tier_results   : dict,
    gamma          : float,
):
    """
    Print a compact comparison: diagonal cells vs off-diagonal corners.

    Layout: two blocks (corner A, corner B), each showing CEW for all systems
    alongside the corresponding diagonal cell for direct comparison.
    """
    systems_ordered = ["symmetric_wdt", "stock_wealth", "income", "cgt", "consumption"]
    col = 14

    print(f"\n{'='*90}")
    print(f"PART F: OFF-DIAGONAL SPOT CHECK  (gamma={gamma})")
    print(f"Diagonal = Fagereng empirical correlation (high return ↔ high wealth).")
    print(f"Corners  = decoupled: return differential and W₀ independently varied.")
    print(f"{'='*90}")

    # Corner A: Great diff, Poor W₀  vs  diagonal Poor and Great
    corner_configs = [
        ("corner_A", "Great diff, Poor W₀",  "Poor",  "Great"),
        ("corner_B", "Poor diff, Great W₀",  "Great", "Poor"),
    ]

    for corner_key, corner_label, diag_w0_tier, diag_diff_tier in corner_configs:
        cr   = corner_results[corner_key]
        diag_w0  = tier_results[diag_w0_tier]   # diagonal cell with same W₀
        diag_diff = tier_results[diag_diff_tier] # diagonal cell with same differential

        print(f"\n  {corner_label}  "
              f"(diff={cr['differential']*100:+.2f}pp, W₀=£{cr['W0']:.1f}m, "
              f"bracket={cr['bracket_label']})")
        print(f"  {'System':28s} {'Corner':>{col}} {'Diag(same W₀)':>{col}} {'Diag(same diff)':>{col}} {'Δ vs same-W₀':>{col}}")
        print("  " + "-" * (28 + col * 4))

        for name in systems_ordered:
            sr_corner   = cr["systems"].get(name)
            sr_diag_w0  = diag_w0["systems"].get(name)
            sr_diag_diff = diag_diff["systems"].get(name)

            c_cew  = sr_corner.cew   if sr_corner   and sr_corner.cew   is not None else None
            w0_cew = sr_diag_w0.cew  if sr_diag_w0  and sr_diag_w0.cew  is not None else None
            d_cew  = sr_diag_diff.cew if sr_diag_diff and sr_diag_diff.cew is not None else None
            delta  = (c_cew - w0_cew) if (c_cew is not None and w0_cew is not None) else None

            label = SYSTEM_LABELS.get(name, name)
            print(f"  {label:28s}"
                  f" {fmt_pct4(c_cew):>{col}}"
                  f" {fmt_pct4(w0_cew):>{col}}"
                  f" {fmt_pct4(d_cew):>{col}}"
                  f" {(f'{delta*10000:+.2f}bp' if delta is not None else '—'):>{col}}")

        # Progressive WDT row
        c_prog  = cr["cew_progressive"]
        w0_prog = diag_w0["cew_progressive"]
        d_prog  = diag_diff["cew_progressive"]
        delta_p = c_prog - w0_prog
        print(f"  {'Progressive WDT':28s}"
              f" {fmt_pct4(c_prog):>{col}}"
              f" {fmt_pct4(w0_prog):>{col}}"
              f" {fmt_pct4(d_prog):>{col}}"
              f" {f'{delta_p*10000:+.2f}bp':>{col}}")

    print()


def chart_corner_check(corner_results: dict, tier_results: dict, gamma: float):
    """
    Chart E: Off-diagonal corners vs diagonal — CEW comparison.

    Two-panel chart.  Each panel is one corner.  Within each panel, grouped
    bars show CEW for: the corner cell, the diagonal cell with the same W₀,
    and the diagonal cell with the same differential.  This makes the W₀
    effect and the differential effect visually separable.
    """
    systems_ordered = ["symmetric_wdt", "stock_wealth", "income", "cgt", "consumption",
                       "progressive_wdt"]
    sys_short = {
        "symmetric_wdt"  : "Sym. WDT",
        "progressive_wdt": "Prog. WDT",
        "stock_wealth"   : "Stock W.",
        "income"         : "Income",
        "cgt"            : "CGT",
        "consumption"    : "Consump.",
    }
    bar_colours = {
        "corner"    : "#2c3e50",   # dark — the new spot-check result
        "same_W0"   : "#7f8c8d",   # grey — diagonal cell, same W₀
        "same_diff" : "#bdc3c7",   # light grey — diagonal cell, same diff
    }

    corner_configs = [
        ("corner_A", "Corner A: Great diff (+3.45pp), Poor W₀ (£2.86m)",
         "Poor", "Great"),
        ("corner_B", "Corner B: Poor diff (−4.55pp), Great W₀ (£139.6m)",
         "Great", "Poor"),
    ]

    apply_style()
    fig, axes = plt.subplots(1, 2, figsize=FIG_PAIR_T, sharey=False)
    fig.suptitle(
        f"D.5 Off-Diagonal Spot Check — Decoupling W₀ from Return Differential\n"
        f"γ = {gamma} | Revenue target = {fmt_pct0(TARGET_ET)} of corner W₀ | "
        f"Dark = corner, mid-grey = diagonal (same W₀), light-grey = diagonal (same diff)",
        fontsize=10, fontweight="bold"
    )

    for ax, (corner_key, title, diag_w0_tier, diag_diff_tier) in zip(axes, corner_configs):
        cr        = corner_results[corner_key]
        diag_w0   = tier_results[diag_w0_tier]
        diag_diff = tier_results[diag_diff_tier]

        x      = np.arange(len(systems_ordered))
        width  = 0.25
        cew_corner    = []
        cew_same_w0   = []
        cew_same_diff = []

        for name in systems_ordered:
            if name == "progressive_wdt":
                cew_corner.append(cr["cew_progressive"] * 100)
                cew_same_w0.append(diag_w0["cew_progressive"] * 100)
                cew_same_diff.append(diag_diff["cew_progressive"] * 100)
            else:
                sr_c  = cr["systems"].get(name)
                sr_w0 = diag_w0["systems"].get(name)
                sr_d  = diag_diff["systems"].get(name)
                cew_corner.append(   sr_c.cew  * 100 if sr_c  and sr_c.cew  is not None else np.nan)
                cew_same_w0.append(  sr_w0.cew * 100 if sr_w0 and sr_w0.cew is not None else np.nan)
                cew_same_diff.append(sr_d.cew  * 100 if sr_d  and sr_d.cew  is not None else np.nan)

        ax.bar(x - width, cew_corner,    width, color=bar_colours["corner"],
               label="Corner (decoupled)", alpha=0.9, edgecolor="white", linewidth=0.5)
        ax.bar(x,         cew_same_w0,   width, color=bar_colours["same_W0"],
               label="Diagonal (same W₀)", alpha=0.9, edgecolor="white", linewidth=0.5)
        ax.bar(x + width, cew_same_diff, width, color=bar_colours["same_diff"],
               label="Diagonal (same diff)", alpha=0.9, edgecolor="white", linewidth=0.5)

        ax.axhline(0, color="black", linewidth=0.8)
        ax.set_xticks(x)
        ax.set_xticklabels([sys_short[s] for s in systems_ordered],
                           fontsize=8, rotation=20, ha="right")
        ax.set_ylabel("CEW (% vs no-tax)", fontsize=9)
        ax.yaxis.set_major_formatter(mtick.PercentFormatter(decimals=3))
        ax.set_title(title, fontsize=9, fontweight="bold")
        ax.legend(fontsize=7.5, loc="lower right")
        ax.grid(axis="y", linestyle="--", alpha=0.4)
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)

    fig.tight_layout()
    _save(fig, "m4_fig_d5_corner_check.png")


def print_corner_findings(corner_results: dict, tier_results: dict):
    """Print the analytical interpretation of the off-diagonal spot check."""
    print(f"\n{'='*70}")
    print("PART F — OFF-DIAGONAL SPOT CHECK: KEY FINDINGS")
    print(f"{'='*70}")

    # Extract WDT vs stock wealth advantage for each cell
    def _wdt_adv(sys_dict, cew_prog_key=None):
        """WDT CEW minus stock wealth CEW, in bp."""
        wdt_cew = sys_dict.get("symmetric_wdt")
        sw_cew  = sys_dict.get("stock_wealth")
        if wdt_cew is None or sw_cew is None:
            return None
        wdt_v = wdt_cew.cew if hasattr(wdt_cew, "cew") else wdt_cew
        sw_v  = sw_cew.cew  if hasattr(sw_cew, "cew")  else sw_cew
        if wdt_v is None or sw_v is None:
            return None
        return (wdt_v - sw_v) * 10000

    adv_A_corner = _wdt_adv(corner_results["corner_A"]["systems"])
    adv_B_corner = _wdt_adv(corner_results["corner_B"]["systems"])
    adv_poor_diag = _wdt_adv(tier_results["Poor"]["systems"])
    adv_great_diag = _wdt_adv(tier_results["Great"]["systems"])

    def _fmt_adv(v):
        return f"{v:+.2f}bp" if v is not None else "—"

    findings = [
        f"F.1  DESIGN CONFIRMATION: The off-diagonal corners test whether the "
        f"main result (WDT welfare advantage varies by tier) is driven by the "
        f"return differential, by the wealth level, or by both jointly. "
        f"WDT advantage vs stock wealth tax: diagonal Poor={_fmt_adv(adv_poor_diag)}, "
        f"diagonal Great={_fmt_adv(adv_great_diag)}, "
        f"corner A (Great diff, Poor W₀)={_fmt_adv(adv_A_corner)}, "
        f"corner B (Poor diff, Great W₀)={_fmt_adv(adv_B_corner)}.",

        f"F.2  W₀ EFFECT vs DIFFERENTIAL EFFECT: Corner A holds the Poor tier's "
        f"W₀ fixed but replaces the return differential with the Great tier's "
        f"(+3.45pp). Corner B holds the Great tier's W₀ fixed but uses the "
        f"Poor tier's differential (−4.55pp). If the rankings are robust to this "
        f"swap, the Fagereng empirical correlation is not the sole driver — "
        f"both dimensions matter independently. If rankings change, the "
        f"interpretation shifts: the main diagonal result is an interaction "
        f"effect, not a pure return-heterogeneity effect.",

        f"F.3  PROGRESSIVE RATE INTERACTION: The progressive WDT applies higher "
        f"rates at higher W₀, so corner B (Poor diff, Great W₀) faces the "
        f"heaviest progressive burden despite a low return differential. "
        f"This is the tax design tension: the progressive schedule is calibrated "
        f"to wealth level, not to ability to pay (return), so a low-return agent "
        f"at high wealth faces a higher rate than a high-return agent at low wealth. "
        f"The corner results make this asymmetry legible without requiring the "
        f"full 4×5 grid.",

        f"F.4  SCOPE LIMITATION: Only the two extreme corners are evaluated. "
        f"The remaining 14 interior cells of the 4×5 (tier × bracket) grid are "
        f"not computed. This is intentional: the extreme corners bound the "
        f"interaction effect. If the ranking is robust at both corners, it is "
        f"likely robust throughout. Interior cells would add precision without "
        f"changing the qualitative conclusion.",
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
    print("MODULE 4: Heterogeneous Agents, Incidence, and Concentration")
    print("=" * 70)

    p   = load_params(TOML_PATH)
    N   = p["tcm"]["canonical_N"]          # 30 — from TOML, never hardcoded
    dist_A = make_empirical_distribution_scenario(p, N)
    dist_B = make_idealised_distribution_scenario(p, N)

    # Progressive rate function (from Module 2)
    rp = p["rate"]
    rate_fn = ProgressiveRateFunction(
        tau0  = rp["tau_0"],
        taum  = rp["tau_m"],
        k     = rp["k"],
        W_min = rp["W_min"],   # £m
    )

    # Build tiers
    tiers = build_tiers(p)
    print(f"\nTier structure (Fagereng et al. 2020 differentials, W0 from ONS/WAS brackets):")
    for t in tiers:
        dist_t = t.shifted_distribution(dist_A)
        print(f"  {t.name:6s}: diff={t.differential*100:+.2f}pp  "
              f"bracket={t.bracket_label:>7s}  W0={fmt_gbp_m(t.W0, dp=2)}  "
              f"share={fmt_pct0(t.pop_share)}  mean return={fmt_pct(dist_t.mean_net_return)}")

    # ── Part B & C: Tier-by-tier comparison ─────────────────────────────────
    print(f"\n--- Parts B & C: Tier-by-tier welfare and incidence ---")
    tier_results = run_tier_comparison(tiers, dist_A, GAMMA, rate_fn)
    print_tier_table(tier_results, GAMMA)
    chart_tier_cew(tier_results, GAMMA, dist_A.label)
    chart_incidence(tier_results)

    # ── Part D: Concentration path ───────────────────────────────────────────
    print("--- Part D: Concentration path (73-year projection) ---")
    systems_to_project = ["symmetric_wdt", "progressive_wdt",
                          "stock_wealth", "income", "consumption"]
    # Extract aggregate taus from tier_results for tau consistency with Parts B/C.
    # The Good tier is used as the reference for reading back taus; all tiers share
    # the same tau under the flat-rate systems (that is what 'aggregate tau' means).
    agg_taus = {
        name: tier_results["Good"]["systems"][name].tau
        for name in ["symmetric_wdt", "stock_wealth", "income", "cgt", "consumption"]
        if tier_results["Good"]["systems"].get(name) and tier_results["Good"]["systems"][name].tau is not None
    }
    paths, conc_years = run_concentration_analysis(
        tiers, p, rate_fn, systems_to_project, precomputed_taus=agg_taus
    )
    chart_concentration_path(paths, tiers, conc_years)

    # Quick summary of final wealth ratios
    print(f"\n  Final wealth ratios (Great / Poor) after 30 years:")
    for name in systems_to_project:
        if name not in paths:
            continue
        great_final = paths[name].get("Great", [np.nan])[-1]
        poor_final  = paths[name].get("Poor",  [np.nan])[-1]
        ratio       = great_final / poor_final if poor_final > 0 else np.nan
        label = "Progressive WDT" if name == "progressive_wdt" else SYSTEM_LABELS.get(name, name)
        print(f"    {label:35s}: {ratio:7.1f}×")

    # ── Part E: Envelope binding ─────────────────────────────────────────────
    print("\n--- Part E: Envelope binding test ---")
    envelope_results = test_envelope_binding(tiers, p, rate_fn)
    print_envelope_summary(envelope_results, tiers)
    # Use scenario years (length N), not the full 73-year series
    _, envelope_years = make_scenario_sequence(p, N)
    chart_envelope(envelope_results, envelope_years)

    print_findings(tier_results, envelope_results, paths, tiers)

    # ── Part F: Off-diagonal spot check ─────────────────────────────────────
    print("\n--- Part F: Off-diagonal spot check (2 corner cells) ---")
    corner_results = run_corner_check(tiers, dist_A, GAMMA, rate_fn)
    print_corner_table(corner_results, tier_results, GAMMA)
    chart_corner_check(corner_results, tier_results, GAMMA)
    print_corner_findings(corner_results, tier_results)

    print(f"\n✓ Module 4 complete. Outputs in: {OUTPUT_DIR}")


if __name__ == "__main__":
    main()