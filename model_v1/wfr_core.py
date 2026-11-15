"""
wfr_core.py — WDT Welfare Comparison Model
===========================================
Single file containing all primitives and computation logic for the WFR
welfare comparison model.  Merged from the former welfare_core.py
(shared primitives) and wfr_core.py (computation engine).  The split was
a legacy artefact; there are no other consumers of the welfare_core
primitives outside this pipeline.

Entry point
-----------
  python wfr_core.py                    # run all five modules
  python wfr_core.py --modules 1 2 3   # run specific modules
  python wfr_core.py --out path.json   # custom output path

Output
------
  OUTPUTS/WFR/wfr/wfr_results.json

JSON schema summary
-------------------
{
  "meta": { version, date, params_summary },
  "module1": { distributions: { <dist_label>: { welfare, dm_test } } },
  "module2": { rate_fn, c1, c2_leverage, c3_asymmetry },
  "module3": { asset_ref, threshold_curve, sens_gain, sens_T, full_comparison },
  "module4": { tiers, tier_welfare, concentration, envelope, corner_check },
  "module5": { sweep_a_revenue, sweep_a_w0, sweep_b_start_year, sweep_c_params },
}

Structure
---------
 0.  Paths and imports
 1.  Parameter loading
 2.  Return distributions
 3.  Tax systems
 4.  Welfare calculator (CRRA utility, CEW)
 5.  Revenue equivalence solver
 6.  Full welfare comparison runner
 7.  Diagnostics (stdout tables, D-M test)
 8.  Progressive rate function and welfare helpers
 9.  Module constants and serialisation helpers
10.  Module 1 — Baseline welfare comparison
11.  Module 2 — Progressive rates and D-M complications
12.  Module 3 — CGT lock-in distortion
13.  Module 4 — Heterogeneous agents
14.  Module 5 — Welfare sweep analysis
15.  CLI entry point
"""

from __future__ import annotations

import argparse
import json
import math
import sys
import numpy as np
from dataclasses import dataclass, field
from datetime import date
from pathlib import Path
from typing import Optional
from scipy.optimize import brentq

from wdt_fmt import fmt_pct, fmt_gbp_m


# ─────────────────────────────────────────────────────────────────────────────
# 0. PATHS
# ─────────────────────────────────────────────────────────────────────────────

_ROOT       = Path(__file__).resolve().parent
TOML_PATH   = _ROOT / "WDT_Params.toml"
OUTPUT_ROOT = _ROOT / "OUTPUTS"

if not TOML_PATH.exists():
    raise FileNotFoundError(
        f"WDT_Params.toml not found at {TOML_PATH}. "
        "Expected layout: WDT_Params.toml alongside wfr_core.py."
    )


def module_output_dir(module_name: str) -> Path:
    """Return (and create) the output subdirectory for a given module."""
    d = OUTPUT_ROOT / module_name
    d.mkdir(parents=True, exist_ok=True)
    return d


# ─────────────────────────────────────────────────────────────────────────────
# 1. PARAMETER LOADING
# ─────────────────────────────────────────────────────────────────────────────

def load_params(toml_path: str) -> dict:
    """
    Load all model parameters and return a unified dict.

    Delegates to wdt_core.load_params() so that the WFR pipeline and the
    rest of the model operate on an identical parameter dict.  The WFR-
    specific sub-dict views (p['rate'], p['tcm'], p['returns_meta']) are
    built by wdt_core.load_params() and are available here transparently.
    """
    from wdt_core import load_params as _core_load_params
    p = _core_load_params(toml_path)

    n_returns = len(p['returns_meta']['values'])
    if n_returns != 73:
        raise ValueError(
            f"Expected 73 return values in TOML, got {n_returns}."
        )
    return p


def make_scenario_sequence(p: dict, N: int) -> tuple[np.ndarray, list]:
    """
    Return the N-year return sequence starting at scenario_start_year.
    Wraps cyclically around the 73-year series if N exceeds remaining years.
    Returns (returns_array, years_list).
    """
    rm      = p["returns_meta"]
    full    = rm["array"]
    offset  = rm["offset"]
    base    = rm["series_base_year"]
    start_y = p["tcm"].get("scenario_start_year", base)
    total   = len(full)

    indices = [(offset + i) % total for i in range(N)]
    seq     = full[indices]
    years   = list(range(start_y, start_y + N))
    return seq, years


def make_empirical_distribution_scenario(p: dict, N: int) -> 'ReturnDistribution':
    """Version A: N-year scenario sequence, equal probability 1/N per year."""
    seq, _ = make_scenario_sequence(p, N)
    gross  = 1.0 + seq
    probs  = np.full(N, 1.0 / N)
    start  = p["tcm"].get("scenario_start_year", p["returns_meta"]["series_base_year"])
    return ReturnDistribution(
        returns=gross, probs=probs,
        label=f"Version A — UK Equity {start}–{start+N-1} ({N} obs, scenario)"
    )


def make_idealised_distribution_scenario(p: dict, N: int) -> 'ReturnDistribution':
    """Version B: Two-state distribution calibrated to scenario μ and σ."""
    seq, _ = make_scenario_sequence(p, N)
    mu     = float(np.mean(seq))
    sigma  = float(np.std(seq, ddof=0))
    R_good = 1.0 + mu + sigma
    R_bad  = 1.0 + mu - sigma
    if R_bad <= 0:
        raise ValueError(f"Scenario bad-state return non-positive: {R_bad:.4f}")
    start = p["tcm"].get("scenario_start_year", p["returns_meta"]["series_base_year"])
    return ReturnDistribution(
        returns=np.array([R_good, R_bad]), probs=np.array([0.5, 0.5]),
        label=(
            f"Version B — Idealised Two-State, scenario {start}–{start+N-1} "
            f"(R_good={R_good:.4f}, R_bad={R_bad:.4f})"
        )
    )


def make_empirical_distribution_for_start(
    p: dict, start_year: int, N: int,
) -> tuple:
    """
    Build a Version A distribution for an explicit start_year.
    Used by Module 5 Sweep B which iterates over all 73 start years.
    Returns (dist, seq) or (None, None) if start_year is out of range.
    """
    rm     = p["returns_meta"]
    base   = rm["series_base_year"]
    full   = rm["array"]
    total  = len(full)
    offset = start_year - base
    if not (0 <= offset < total):
        return None, None

    indices = [(offset + i) % total for i in range(N)]
    seq     = full[indices]
    gross   = 1.0 + seq
    probs   = np.full(N, 1.0 / N)
    dist    = ReturnDistribution(
        returns=gross, probs=probs,
        label=f"Version A — UK Equity {start_year}–{start_year + N - 1} ({N} obs)"
    )
    return dist, seq


def make_empirical_distribution(p: dict) -> 'ReturnDistribution':
    """Version A: full 73-year series, equal probability 1/73."""
    raw   = p["returns_meta"]["array"]
    gross = 1.0 + raw
    probs = np.full(len(gross), 1.0 / len(gross))
    return ReturnDistribution(
        returns=gross, probs=probs,
        label="Version A — UK Historical Equity (1947–2019, 73 obs)"
    )


def make_idealised_distribution(p: dict) -> 'ReturnDistribution':
    """Version B: Two-state distribution calibrated to full 73-year μ and σ."""
    raw   = p["returns_meta"]["array"]
    mu    = float(np.mean(raw))
    sigma = float(np.std(raw, ddof=0))
    R_good = 1.0 + mu + sigma
    R_bad  = 1.0 + mu - sigma
    if R_bad <= 0:
        raise ValueError(
            f"Idealised bad-state gross return is non-positive: {R_bad:.4f}."
        )
    return ReturnDistribution(
        returns=np.array([R_good, R_bad]), probs=np.array([0.5, 0.5]),
        label=(
            f"Version B — Idealised Two-State "
            f"(R_good={R_good:.4f}, R_bad={R_bad:.4f}, p=0.5/0.5)"
        )
    )


# ─────────────────────────────────────────────────────────────────────────────
# 2. RETURN DISTRIBUTIONS
# ─────────────────────────────────────────────────────────────────────────────

@dataclass
class ReturnDistribution:
    """
    A return distribution as (return, probability) pairs.

    Attributes
    ----------
    returns : np.ndarray  gross returns (1 + r), one per state
    probs   : np.ndarray  probability weights, must sum to 1
    label   : str         human-readable label
    """
    returns: np.ndarray
    probs  : np.ndarray
    label  : str

    def __post_init__(self):
        if not math.isclose(self.probs.sum(), 1.0, rel_tol=1e-6):
            raise ValueError(f"Probabilities sum to {self.probs.sum():.6f}, not 1.")
        if np.any(self.returns <= 0):
            raise ValueError("Gross returns must be positive (1 + r > 0).")

    @property
    def n_states(self) -> int:
        return len(self.returns)

    @property
    def mean_return(self) -> float:
        return float(np.dot(self.probs, self.returns))

    @property
    def mean_net_return(self) -> float:
        return self.mean_return - 1.0

    @property
    def std_return(self) -> float:
        mean = self.mean_return
        return math.sqrt(float(np.dot(self.probs, (self.returns - mean) ** 2)))

    def describe(self) -> str:
        pos = self.returns > 1.0
        neg = self.returns < 1.0
        return "\n".join([
            f"Distribution: {self.label}",
            f"  States:               {self.n_states}",
            f"  Mean gross return:    {self.mean_return:.4f}  ({self.mean_net_return*100:.2f}%)",
            f"  Std dev (returns):    {self.std_return:.4f}  ({self.std_return*100:.2f}%)",
            f"  P(positive return):   {self.probs[pos].sum():.4f}  ({self.probs[pos].sum()*100:.1f}%)",
            f"  P(negative return):   {self.probs[neg].sum():.4f}  ({self.probs[neg].sum()*100:.1f}%)",
        ])


# ─────────────────────────────────────────────────────────────────────────────
# 3. TAX SYSTEMS
# ─────────────────────────────────────────────────────────────────────────────

@dataclass
class TaxResult:
    """Output of applying one tax function to one return state."""
    gross_wealth   : float
    tax_paid       : float   # positive = tax, negative = refund
    post_tax_wealth: float
    consumption    : float   # = post_tax_wealth except for consumption tax


def tax_consumption(W0: float, R: float, tau: float) -> TaxResult:
    """Consumption tax: C = W₁ / (1 + τ).  No distortion on accumulation."""
    W1  = W0 * R
    tax = tau * W1 / (1.0 + tau)
    C   = W1 / (1.0 + tau)
    return TaxResult(gross_wealth=W1, tax_paid=tax, post_tax_wealth=W1, consumption=C)


def tax_income(W0: float, R: float, tau: float) -> TaxResult:
    """Income tax on positive returns only.  No refund on losses."""
    W1      = W0 * R
    tax     = tau * max(W1 - W0, 0.0)
    W1_post = W1 - tax
    return TaxResult(gross_wealth=W1, tax_paid=tax, post_tax_wealth=W1_post, consumption=W1_post)


def tax_cgt(W0: float, R: float, tau: float) -> TaxResult:
    """CGT — identical to income tax in Module 1 (lock-in enters Module 3)."""
    return tax_income(W0, R, tau)


def tax_stock_wealth(W0: float, R: float, tau: float) -> TaxResult:
    """Stock wealth tax on end-period wealth W₁, regardless of return sign."""
    W1      = W0 * R
    tax     = tau * W1
    W1_post = W1 - tax
    return TaxResult(gross_wealth=W1, tax_paid=tax, post_tax_wealth=W1_post, consumption=W1_post)


def tax_symmetric_flat(W0: float, R: float, tau: float) -> TaxResult:
    """Symmetric flat-rate WDT: tax base = W₁ − W₀ (delta), sign preserved."""
    W1      = W0 * R
    delta   = W1 - W0
    tax     = tau * delta
    W1_post = W1 - tax
    return TaxResult(gross_wealth=W1, tax_paid=tax, post_tax_wealth=W1_post, consumption=W1_post)


_TAX_REGISTRY = {
    "consumption"  : tax_consumption,
    "income"       : tax_income,
    "cgt"          : tax_cgt,
    "stock_wealth" : tax_stock_wealth,
    "symmetric_wdt": tax_symmetric_flat,
}

SYSTEM_LABELS = {
    "consumption"  : "Consumption Tax",
    "income"       : "Income Tax (no refund)",
    "cgt"          : "CGT (gains only)",
    "stock_wealth" : "Stock Wealth Tax",
    "symmetric_wdt": "Symmetric WDT (flat)",
}


def get_tax_fn(name: str):
    if name not in _TAX_REGISTRY:
        raise KeyError(
            f"Unknown tax system '{name}'. Available: {list(_TAX_REGISTRY.keys())}"
        )
    return _TAX_REGISTRY[name]


# ─────────────────────────────────────────────────────────────────────────────
# 4. WELFARE CALCULATOR
# ─────────────────────────────────────────────────────────────────────────────

def crra_utility(c: float, gamma: float) -> float:
    """
    CRRA utility: c^(1-γ)/(1-γ) for γ≠1, ln(c) for γ=1.
    Raises ValueError for c ≤ 0.
    """
    if c <= 0:
        raise ValueError(f"CRRA utility undefined for c={c:.4f} ≤ 0.")
    if math.isclose(gamma, 1.0, rel_tol=1e-9):
        return math.log(c)
    return (c ** (1.0 - gamma)) / (1.0 - gamma)


def expected_utility(
    W0: float, dist: ReturnDistribution, tax_fn, tau: float, gamma: float,
) -> float:
    """E[u(consumption)] for one tax system across all return states."""
    return sum(
        prob * crra_utility(tax_fn(W0, R, tau).consumption, gamma)
        for R, prob in zip(dist.returns, dist.probs)
    )


def expected_tax(W0: float, dist: ReturnDistribution, tax_fn, tau: float) -> float:
    """E[T]: expected tax collected (refunds count as negative)."""
    return sum(
        prob * tax_fn(W0, R, tau).tax_paid
        for R, prob in zip(dist.returns, dist.probs)
    )


def consumption_equiv_welfare(
    eu_tax: float, eu_notax: float, gamma: float,
) -> float:
    """
    CEW (λ): proportional consumption change that makes the agent indifferent
    between the taxed and no-tax allocations.

    Under CRRA (γ≠1):  λ = (EU_tax / EU_notax)^(1/(1-γ)) − 1
    Under log  (γ=1):   λ = exp(EU_tax − EU_notax) − 1

    Positive λ: taxed system has higher welfare than no-tax.
    Negative λ: taxed system has lower welfare (expected for any revenue-positive tax).
    Relative ranking across systems is what matters.
    """
    if math.isclose(gamma, 1.0, rel_tol=1e-9):
        return math.exp(eu_tax - eu_notax) - 1.0
    return (eu_tax / eu_notax) ** (1.0 / (1.0 - gamma)) - 1.0


def variance_of_consumption(
    W0: float, dist: ReturnDistribution, tax_fn, tau: float,
) -> float:
    """Variance of consumption across return states."""
    consumptions = np.array([tax_fn(W0, R, tau).consumption for R in dist.returns])
    mean_c = float(np.dot(dist.probs, consumptions))
    return float(np.dot(dist.probs, (consumptions - mean_c) ** 2))


# ─────────────────────────────────────────────────────────────────────────────
# 5. REVENUE EQUIVALENCE SOLVER
# ─────────────────────────────────────────────────────────────────────────────

def solve_revenue_equivalent_rate(
    W0: float, dist: ReturnDistribution, tax_fn, target_et: float,
    tau_lo: float = 1e-6, tau_hi: float = 0.999,
) -> float:
    """
    Find τ such that E[T(W0, dist, τ)] = target_et using Brent's method.
    Raises ValueError if target cannot be achieved within [tau_lo, tau_hi].
    """
    def objective(tau):
        return expected_tax(W0, dist, tax_fn, tau) - target_et

    try:
        et_lo = objective(tau_lo)
        et_hi = objective(tau_hi)
    except Exception as e:
        raise ValueError(f"Error evaluating tax function at bounds: {e}")

    if et_lo * et_hi > 0:
        raise ValueError(
            f"Cannot achieve target E[T]={target_et:.4f} for "
            f"{tax_fn.__name__} within τ ∈ [{tau_lo}, {tau_hi}]. "
            f"E[T] at bounds: [{et_lo + target_et:.4f}, {et_hi + target_et:.4f}]. "
            "The system may structurally be unable to raise this revenue."
        )
    return float(brentq(objective, tau_lo, tau_hi, xtol=1e-10, rtol=1e-10))


def solve_all_rates(
    W0: float, dist: ReturnDistribution, target_et: float,
    systems: Optional[list] = None,
) -> dict:
    """
    Solve revenue-equivalent rates for all (or a subset of) systems.
    Returns {system_name: tau_star}, with tau_star=None if unsolvable.
    """
    if systems is None:
        systems = list(_TAX_REGISTRY.keys())
    rates = {}
    for name in systems:
        tax_fn = get_tax_fn(name)
        try:
            rates[name] = solve_revenue_equivalent_rate(W0, dist, tax_fn, target_et)
        except ValueError as e:
            print(f"  WARNING [{name}]: {e}")
            rates[name] = None
    return rates


# ─────────────────────────────────────────────────────────────────────────────
# 6. FULL WELFARE COMPARISON
# ─────────────────────────────────────────────────────────────────────────────

@dataclass
class SystemResult:
    """Welfare results for one tax system at one (distribution, gamma) pair."""
    name           : str
    label          : str
    tau            : Optional[float]
    eu             : Optional[float]
    cew            : Optional[float]
    expected_tax   : Optional[float]
    var_consumption: Optional[float]
    state_taxes    : Optional[np.ndarray] = field(default=None, repr=False)
    state_wealth   : Optional[np.ndarray] = field(default=None, repr=False)
    state_cons     : Optional[np.ndarray] = field(default=None, repr=False)


def run_welfare_comparison(
    W0: float, dist: ReturnDistribution, gamma: float, target_et: float,
    systems: Optional[list] = None,
) -> dict:
    """
    Run the full welfare comparison for all systems at given (dist, gamma).
    Returns {system_name: SystemResult}.
    """
    if systems is None:
        systems = list(_TAX_REGISTRY.keys())

    eu_notax = expected_utility(W0, dist, tax_symmetric_flat, 0.0, gamma)
    rates    = solve_all_rates(W0, dist, target_et, systems)
    results  = {}

    for name in systems:
        tau = rates[name]
        if tau is None:
            results[name] = SystemResult(
                name=name, label=SYSTEM_LABELS[name],
                tau=None, eu=None, cew=None,
                expected_tax=None, var_consumption=None,
            )
            continue
        tax_fn = get_tax_fn(name)
        eu     = expected_utility(W0, dist, tax_fn, tau, gamma)
        results[name] = SystemResult(
            name=name, label=SYSTEM_LABELS[name],
            tau=tau,
            eu=eu,
            cew=consumption_equiv_welfare(eu, eu_notax, gamma),
            expected_tax=expected_tax(W0, dist, tax_fn, tau),
            var_consumption=variance_of_consumption(W0, dist, tax_fn, tau),
            state_taxes =np.array([tax_fn(W0, R, tau).tax_paid        for R in dist.returns]),
            state_wealth=np.array([tax_fn(W0, R, tau).post_tax_wealth  for R in dist.returns]),
            state_cons  =np.array([tax_fn(W0, R, tau).consumption      for R in dist.returns]),
        )
    return results


# ─────────────────────────────────────────────────────────────────────────────
# 7. DIAGNOSTICS
# ─────────────────────────────────────────────────────────────────────────────

def print_welfare_table(
    results: dict, dist_label: str, gamma: float, target_et: float, W0: float,
) -> None:
    """Print a formatted welfare comparison table to stdout."""
    col_w = 24
    order = ["symmetric_wdt", "stock_wealth", "income", "cgt", "consumption"]
    print(f"\n{'='*80}")
    print(f"Welfare Comparison  |  {dist_label}")
    print(f"γ = {gamma}  |  Target E[T] = £{target_et:.4f}  |  W₀ = £{W0:.2f}")
    print(f"{'='*80}")
    names = [results[s].label if s in results else s for s in order]
    print(f"{'':30s}" + "".join(f"{n:>{col_w}}" for n in names))
    print("-" * (30 + col_w * len(order)))
    rows = [
        ("Rate (τ)",         lambda r: f"{r.tau*100:.3f}%"       if r.tau            is not None else "N/A"),
        ("E[T] (£)",         lambda r: f"£{r.expected_tax:.4f}"  if r.expected_tax   is not None else "N/A"),
        ("E[u]",             lambda r: f"{r.eu:.8f}"              if r.eu             is not None else "N/A"),
        ("CEW vs no-tax",    lambda r: f"{r.cew*100:+.4f}%"      if r.cew            is not None else "N/A"),
        ("Var(consumption)", lambda r: f"{r.var_consumption:.4f}" if r.var_consumption is not None else "N/A"),
    ]
    for row_label, fmt_fn in rows:
        line = f"{row_label:30s}"
        for name in order:
            line += f"{fmt_fn(results[name]) if name in results else '—':>{col_w}}"
        print(line)
    print("-" * (30 + col_w * len(order)))
    ranked = sorted(
        [(n, results[n].cew) for n in order if n in results and results[n].cew is not None],
        key=lambda x: x[1], reverse=True,
    )
    print("\nCEW Ranking (best to worst welfare):")
    for rank, (name, cew) in enumerate(ranked, 1):
        print(f"  {rank}. {SYSTEM_LABELS[name]:35s} {cew*100:+.4f}%")


def dm_test(W0: float, dist: ReturnDistribution, tau: float) -> dict:
    """
    Domar-Musgrave test: confirms Var(C_tax) = (1-τ)² × Var(C_notax)
    for the symmetric flat WDT.
    """
    var_notax = variance_of_consumption(W0, dist, tax_symmetric_flat, 0.0)
    var_tax   = variance_of_consumption(W0, dist, tax_symmetric_flat, tau)
    predicted = (1.0 - tau) ** 2
    actual    = var_tax / var_notax if var_notax > 0 else float('nan')
    gap       = actual - predicted
    return {
        "var_notax":       var_notax,
        "var_tax":         var_tax,
        "predicted_ratio": predicted,
        "actual_ratio":    actual,
        "gap":             gap,
        "dm_holds":        bool(abs(gap) < 1e-6),
    }


# ─────────────────────────────────────────────────────────────────────────────
# 8. PROGRESSIVE RATE FUNCTION AND WELFARE HELPERS
# ─────────────────────────────────────────────────────────────────────────────

class ProgressiveRateFunction:
    """
    WDT logistic rate function.

    τ(W) = τ_m / (1 + A × exp(−k × (W − W_min)))   where A = (τ_m − τ_0) / τ_0
         = 0  if W ≤ W_min

    Properties: τ(W_min) = τ_0,  τ → τ_m as W → ∞,  strictly increasing.
    """

    def __init__(self, tau0: float, taum: float, k: float, W_min: float):
        self.tau0  = tau0
        self.taum  = taum
        self.k     = k
        self.W_min = W_min
        self.A     = (taum - tau0) / tau0

    def rate(self, W: float) -> float:
        if W <= self.W_min:
            return 0.0
        return self.taum / (1.0 + self.A * math.exp(-self.k * (W - self.W_min)))

    def effective_rate(self, W0: float, W1: float) -> float:
        """
        Effective rate on the delta (W1 − W0).
        Loss state: rate at W1 (lower wealth).
        Gain state: midpoint of rates at W0 and W1 (approximation to ∫τ dW).
        """
        if W1 <= W0:
            return self.rate(W1)
        return 0.5 * (self.rate(W0) + self.rate(W1))

    def describe(self) -> str:
        return (
            f"Progressive Rate Function:\n"
            f"  τ₀ = {fmt_pct(self.tau0, dp=1)}  τ_m = {fmt_pct(self.taum, dp=1)}"
            f"  k = {self.k}  W_min = {fmt_gbp_m(self.W_min, dp=0)}\n"
            f"  Rate at W_min:     {fmt_pct(self.rate(self.W_min))}\n"
            f"  Rate at 2×W_min:   {fmt_pct(self.rate(2*self.W_min))}\n"
            f"  Rate at 10×W_min:  {fmt_pct(self.rate(10*self.W_min))}\n"
            f"  Rate at 100×W_min: {fmt_pct(self.rate(100*self.W_min))}"
        )


def tax_progressive_wdt(W0: float, R: float, rate_fn: ProgressiveRateFunction):
    """
    Progressive WDT tax for one period.
    Returns (tax_paid, post_tax_wealth, consumption).
    Tax is negative (refund) in loss states.
    """
    W1      = W0 * R
    delta   = W1 - W0
    tax     = rate_fn.effective_rate(W0, W1) * delta
    W1_post = W1 - tax
    return tax, W1_post, W1_post


def expected_utility_progressive(
    W0: float, dist: ReturnDistribution,
    rate_fn: ProgressiveRateFunction, gamma: float,
) -> float:
    """E[u] under progressive WDT."""
    return sum(
        prob * crra_utility(tax_progressive_wdt(W0, R, rate_fn)[2], gamma)
        for R, prob in zip(dist.returns, dist.probs)
    )


def expected_tax_progressive(
    W0: float, dist: ReturnDistribution, rate_fn: ProgressiveRateFunction,
) -> float:
    """E[T] under progressive WDT."""
    return sum(
        prob * tax_progressive_wdt(W0, R, rate_fn)[0]
        for R, prob in zip(dist.returns, dist.probs)
    )


def variance_progressive(
    W0: float, dist: ReturnDistribution, rate_fn: ProgressiveRateFunction,
) -> float:
    """Var(consumption) under progressive WDT."""
    consumptions = np.array([
        tax_progressive_wdt(W0, R, rate_fn)[2] for R in dist.returns
    ])
    mean_c = float(np.dot(dist.probs, consumptions))
    return float(np.dot(dist.probs, (consumptions - mean_c) ** 2))


# ─────────────────────────────────────────────────────────────────────────────
# 9. MODULE CONSTANTS AND SERIALISATION HELPERS
# ─────────────────────────────────────────────────────────────────────────────

W0_NORM   = 1.0
TARGET_ET = 0.02
GAMMA_VALS = [1.0, 2.0, 4.0]
GAMMA_CEN  = 2.0
SYSTEMS    = ["symmetric_wdt", "stock_wealth", "income", "cgt", "consumption"]

OUTPUT_DIR = module_output_dir("WFR")


def _f(v):
    """Scalar → python float or None."""
    if v is None:
        return None
    if isinstance(v, float) and math.isnan(v):
        return None
    return float(v)


def _arr(v):
    """ndarray or list → plain list of floats."""
    if v is None:
        return None
    return [float(x) for x in v]


def _dist_summary(dist: ReturnDistribution) -> dict:
    return {
        "label":          dist.label,
        "n_states":       int(dist.n_states),
        "mean_net_return": _f(dist.mean_net_return),
        "std_return":     _f(dist.std_return),
        "returns":        _arr(dist.returns),
        "probs":          _arr(dist.probs),
    }


def _sanitise(obj):
    """
    Recursively convert the result dict to plain JSON-safe Python types.

    Using a pre-pass rather than cls=JSONEncoder subclass or default= hook
    avoids the CPython fast path that handles numpy scalars before any custom
    encoder sees them, which caused numpy.bool_ and numpy nan/inf to raise
    TypeError / ValueError with the encoder subclass approach.

    Rules:
    - dict / list / tuple: recurse
    - numpy ndarray: tolist() then recurse
    - numpy bool_: bool()
    - numpy integer: int()
    - numpy float, Python float: float(), then None if not finite
    - everything else (str, int, bool, None): return unchanged
    """
    if isinstance(obj, dict):
        return {k: _sanitise(v) for k, v in obj.items()}
    if isinstance(obj, (list, tuple)):
        return [_sanitise(v) for v in obj]
    if isinstance(obj, np.ndarray):
        return [_sanitise(v) for v in obj.tolist()]
    if isinstance(obj, np.bool_):
        return bool(obj)
    if isinstance(obj, np.integer):
        return int(obj)
    if isinstance(obj, np.floating):
        v = float(obj)
        return None if not math.isfinite(v) else v
    if isinstance(obj, float):
        return None if not math.isfinite(obj) else obj
    return obj


# ─────────────────────────────────────────────────────────────────────────────
# 10. MODULE 1 — BASELINE WELFARE COMPARISON
# ─────────────────────────────────────────────────────────────────────────────

def _welfare_result_to_dict(r) -> dict:
    return {
        "tau":             _f(r.tau),
        "eu":              _f(r.eu),
        "cew":             _f(r.cew),
        "expected_tax":    _f(r.expected_tax),
        "var_consumption": _f(r.var_consumption),
        "state_taxes":     _arr(r.state_taxes),
        "state_wealth":    _arr(r.state_wealth),
        "state_cons":      _arr(r.state_cons),
    }


def run_module1(p: dict) -> dict:
    print("\n=== Module 1: Baseline Welfare Comparison ===")
    N      = p["tcm"]["canonical_N"]
    dist_A = make_empirical_distribution_scenario(p, N)
    dist_B = make_idealised_distribution_scenario(p, N)
    out    = {"distributions": {}}

    for dist in [dist_A, dist_B]:
        dk    = dist.label
        entry = _dist_summary(dist)
        entry["welfare"]  = {}
        entry["dm_test"]  = {}

        for gamma in GAMMA_VALS:
            print(f"  {dk[:40]}  γ={gamma}")
            results = run_welfare_comparison(
                W0=W0_NORM, dist=dist, gamma=gamma, target_et=TARGET_ET,
            )
            entry["welfare"][str(gamma)] = {
                name: _welfare_result_to_dict(r) for name, r in results.items()
            }
            tau_wdt = results.get("symmetric_wdt")
            if tau_wdt and tau_wdt.tau is not None:
                dm = dm_test(W0_NORM, dist, tau_wdt.tau)
                entry["dm_test"][str(gamma)] = {
                    "var_notax":       _f(dm["var_notax"]),
                    "var_tax":         _f(dm["var_tax"]),
                    "predicted_ratio": _f(dm["predicted_ratio"]),
                    "actual_ratio":    _f(dm["actual_ratio"]),
                    "gap":             _f(dm["gap"]),
                    "dm_holds":        bool(dm["dm_holds"]),
                }

        out["distributions"][dk] = entry
    return out


# ─────────────────────────────────────────────────────────────────────────────
# 11. MODULE 2 — PROGRESSIVE RATES AND D-M COMPLICATIONS
# ─────────────────────────────────────────────────────────────────────────────

@dataclass
class LeveragedAgent:
    gross_assets: float
    debt: float

    @property
    def net_worth(self) -> float:
        return self.gross_assets - self.debt

    @property
    def leverage_ratio(self) -> float:
        return self.debt / self.gross_assets if self.gross_assets > 0 else 0.0

    def net_worth_after_return(self, R: float) -> float:
        return self.gross_assets * R - self.debt


def build_rate_fn(p: dict) -> ProgressiveRateFunction:
    rp = p["rate"]
    return ProgressiveRateFunction(
        tau0=rp["tau_0"], taum=rp["tau_m"], k=rp["k"], W_min=rp["W_min"],
    )


class ScaledRateFn(ProgressiveRateFunction):
    """Uniform scale factor applied to every effective_rate / rate call."""
    def __init__(self, base: ProgressiveRateFunction, scale: float):
        super().__init__(base.tau0, base.taum, base.k, base.W_min)
        self.scale = scale

    def effective_rate(self, W0: float, W1: float) -> float:
        return self.scale * super().effective_rate(W0, W1)

    def rate(self, W: float) -> float:
        return self.scale * super().rate(W)


def _solve_progressive_scale(
    W0: float, dist: ReturnDistribution,
    rate_fn: ProgressiveRateFunction, target_et: float,
) -> Optional[float]:
    def _et(s):
        return expected_tax_progressive(W0, dist, ScaledRateFn(rate_fn, s)) - target_et
    try:
        lo, hi = _et(1e-4), _et(50.0)
    except Exception:
        return None
    if lo * hi > 0:
        return None
    return float(brentq(_et, 1e-4, 50.0, xtol=1e-10, rtol=1e-10))


def _run_c1(W0, dist, rate_fn, gamma, target_et) -> dict:
    flat_fn  = get_tax_fn("symmetric_wdt")
    eu_notax = expected_utility(W0, dist, flat_fn, 0.0, gamma)
    et_prog  = expected_tax_progressive(W0, dist, rate_fn)
    eu_prog  = expected_utility_progressive(W0, dist, rate_fn, gamma)
    cew_prog = consumption_equiv_welfare(eu_prog, eu_notax, gamma)

    revenue_matched = et_prog > 0
    flat_target = et_prog if revenue_matched else target_et
    try:
        tau_flat = solve_revenue_equivalent_rate(W0, dist, flat_fn, flat_target)
    except ValueError:
        tau_flat = None

    if tau_flat is not None:
        eu_flat  = expected_utility(W0, dist, flat_fn, tau_flat, gamma)
        cew_flat = consumption_equiv_welfare(eu_flat, eu_notax, gamma)
        var_flat = variance_of_consumption(W0, dist, flat_fn, tau_flat)
        et_flat  = expected_tax(W0, dist, flat_fn, tau_flat)
    else:
        eu_flat = cew_flat = var_flat = et_flat = None

    return {
        "tau_flat":        _f(tau_flat),
        "et_flat":         _f(et_flat),
        "et_flat_target":  _f(target_et),
        "eu_flat":         _f(eu_flat),
        "cew_flat":        _f(cew_flat),
        "var_flat":        _f(var_flat),
        "et_progressive":  _f(et_prog),
        "eu_progressive":  _f(eu_prog),
        "cew_progressive": _f(cew_prog),
        "cew_gap_bp":      _f((cew_flat - cew_prog) * 10000)
                           if (cew_flat is not None and cew_prog is not None) else None,
        "revenue_matched": revenue_matched,
    }


def _var_progressive(W0, dist, rate_fn):
    consumptions = np.array([tax_progressive_wdt(W0, R, rate_fn)[2] for R in dist.returns])
    mean_c = float(np.dot(dist.probs, consumptions))
    return float(np.dot(dist.probs, (consumptions - mean_c) ** 2))


def _run_c2_leverage(
    agent: LeveragedAgent, dist: ReturnDistribution,
    rate_fn: ProgressiveRateFunction, gamma: float,
) -> dict:
    W0 = agent.net_worth
    states = []
    for R, prob in zip(dist.returns, dist.probs):
        W1       = agent.net_worth_after_return(R)
        delta_W  = W1 - W0
        delta_A  = agent.gross_assets * (R - 1.0)
        tau_eff  = rate_fn.effective_rate(W0, W1) if W1 > 0 else rate_fn.rate(max(W1, 0))
        tax_nw   = tau_eff * delta_W
        tau_eff_a = rate_fn.effective_rate(agent.gross_assets, agent.gross_assets * R)
        tax_ar   = tau_eff_a * delta_A
        C_nw = max(W1 - tax_nw, 1e-9)
        C_ar = max(W1 - tax_ar, 1e-9)
        states.append({
            "R": _f(R), "prob": _f(prob),
            "W1": _f(W1), "delta_W": _f(delta_W), "delta_A": _f(delta_A),
            "tax_nw": _f(tax_nw), "tax_ar": _f(tax_ar),
            "C_nw": _f(C_nw), "C_ar": _f(C_ar),
        })

    eu_notax = sum(
        prob * crra_utility(max(agent.net_worth_after_return(R), 1e-9), gamma)
        for R, prob in zip(dist.returns, dist.probs)
    )
    eu_nw  = sum(s["prob"] * crra_utility(s["C_nw"], gamma) for s in states)
    eu_ar  = sum(s["prob"] * crra_utility(s["C_ar"], gamma) for s in states)
    et_nw  = sum(s["prob"] * s["tax_nw"] for s in states)
    et_ar  = sum(s["prob"] * s["tax_ar"] for s in states)
    cew_nw = consumption_equiv_welfare(eu_nw, eu_notax, gamma)
    cew_ar = consumption_equiv_welfare(eu_ar, eu_notax, gamma)

    return {
        "leverage_ratio": _f(agent.leverage_ratio),
        "W0":             _f(W0),
        "et_nw":          _f(et_nw),
        "et_ar":          _f(et_ar),
        "cew_nw":         _f(cew_nw),
        "cew_ar":         _f(cew_ar),
        "cew_gap_bp":     _f((cew_nw - cew_ar) * 10000),
    }


def _run_c3_two_period(W0, R1_good, R2_bad, rate_fn, gamma, tau_flat) -> dict:
    W1        = W0 * R1_good
    tau1_prog = rate_fn.effective_rate(W0, W1)
    tax1_prog = tau1_prog * (W1 - W0)
    W1p       = W1 - tax1_prog
    W1f       = W1 - tau_flat * (W1 - W0)
    W2p       = W1p * R2_bad
    W2f       = W1f * R2_bad
    tau2_prog = rate_fn.effective_rate(W1p, W2p)
    refund_prog = tau2_prog * (W2p - W1p)
    refund_flat = tau_flat  * (W2f - W1f)
    C_prog    = W2p - refund_prog
    C_flat    = W2f - refund_flat
    return {
        "W0":               _f(W0),   "W1":               _f(W1),
        "tau1_progressive": _f(tau1_prog),
        "tax1_progressive": _f(tax1_prog),
        "tax1_flat":        _f(tau_flat * (W1 - W0)),
        "W1_post_prog":     _f(W1p),  "W1_post_flat":     _f(W1f),
        "W2_prog":          _f(W2p),  "W2_flat":          _f(W2f),
        "tau2_progressive": _f(tau2_prog),
        "refund_prog":      _f(refund_prog),
        "refund_flat":      _f(refund_flat),
        "C_prog":           _f(C_prog), "C_flat": _f(C_flat),
        "net_tax_prog":     _f(tax1_prog + refund_prog),
        "net_tax_flat":     _f(tau_flat * (W1 - W0) + refund_flat),
        "net_tax_excess":   _f((tax1_prog + refund_prog) - (tau_flat * (W1 - W0) + refund_flat)),
        "rate_asymmetry":   _f(tau1_prog - tau2_prog),
    }


def run_module2(p: dict) -> dict:
    print("\n=== Module 2: Progressive Rates and D-M Complications ===")
    N       = p["tcm"]["canonical_N"]
    dist_A  = make_empirical_distribution_scenario(p, N)
    dist_B  = make_idealised_distribution_scenario(p, N)
    rate_fn = build_rate_fn(p)
    rp      = p["rate"]
    out     = {"rate_fn": {"tau0": _f(rate_fn.tau0), "taum": _f(rate_fn.taum),
                            "k": _f(rate_fn.k), "W_min": _f(rate_fn.W_min)}}

    print("  C1: flat vs progressive...")
    W0_c1 = rp["W_min"] * 5
    c1 = {}
    for dist in [dist_A, dist_B]:
        c1[dist.label] = {}
        for gamma in GAMMA_VALS:
            c1[dist.label][str(gamma)] = _run_c1(W0_c1, dist, rate_fn, gamma, TARGET_ET * W0_c1)
    out["c1"] = c1

    print("  C2: leverage sweep...")
    gross_assets = rp["W_min"] * 5
    lev_grid = np.linspace(0.0, 0.70, 15)
    out["c2_leverage"] = [
        _run_c2_leverage(
            LeveragedAgent(gross_assets=gross_assets, debt=gross_assets * lev),
            dist_A, rate_fn, gamma=GAMMA_CEN,
        )
        for lev in lev_grid
    ]

    print("  C3: two-period asymmetry...")
    mu    = p["tcm"]["hist_mean"]
    sigma = float(np.std(p["returns_meta"]["array"], ddof=0))
    R1    = 1.0 + mu + sigma
    R2    = 1.0 - sigma
    W0_c1_ref = rp["W_min"] * 5
    flat_fn   = get_tax_fn("symmetric_wdt")
    try:
        tau_flat = solve_revenue_equivalent_rate(W0_c1_ref, dist_A, flat_fn, TARGET_ET * W0_c1_ref)
    except ValueError:
        tau_flat = 0.02
    W0_vals = [rp["W_min"] * m for m in [1.5, 2, 5, 10, 20, 50, 100]]
    out["c3_asymmetry"] = {
        "W0_vals": W0_vals, "R1_good": _f(R1), "R2_bad": _f(R2),
        "tau_flat_ref": _f(tau_flat),
        "results": [_run_c3_two_period(W0, R1, R2, rate_fn, GAMMA_CEN, tau_flat) for W0 in W0_vals],
    }
    return out


# ─────────────────────────────────────────────────────────────────────────────
# 12. MODULE 3 — CGT LOCK-IN DISTORTION
# ─────────────────────────────────────────────────────────────────────────────

@dataclass
class AssetSwitchDecision:
    V: float; B: float; tau_cgt: float; T: int; r_A: float

    @property
    def embedded_gain(self): return self.V - self.B

    @property
    def gain_ratio(self): return self.embedded_gain / self.V if self.V > 0 else 0.0

    def switch_cost_pv(self): return self.tau_cgt * self.embedded_gain

    def indifference_return(self) -> float:
        after_tax = self.V - self.switch_cost_pv()
        if after_tax <= 0:
            return float('inf')
        return ((self.V / after_tax) ** (1.0 / self.T)) * (1 + self.r_A) - 1

    def value_of_stay(self, r_B_grid: np.ndarray) -> np.ndarray:
        npv_stay  = self.V * ((1 + self.r_A) ** self.T)
        switch_val = self.V - self.switch_cost_pv()
        return npv_stay - switch_val * ((1 + r_B_grid) ** self.T)


def _compute_lockin_cost(
    asset: AssetSwitchDecision, dist: ReturnDistribution, gamma: float,
) -> dict:
    r_B_indiff = asset.indifference_return()
    states = []
    for R, prob in zip(dist.returns, dist.probs):
        r_B    = R - 1.0
        C_free = asset.V * (1.0 + r_B) if r_B > asset.r_A else asset.V * (1.0 + asset.r_A)
        if r_B >= r_B_indiff:
            C_locked = (asset.V - asset.switch_cost_pv()) * (1.0 + r_B)
        else:
            C_locked = asset.V * (1.0 + asset.r_A)
        states.append({
            "R": _f(R), "prob": _f(prob), "r_B": _f(r_B),
            "C_free": _f(max(C_free, 1e-9)), "C_locked": _f(max(C_locked, 1e-9)),
            "locked_in": bool(r_B < r_B_indiff),
        })

    eu_notax  = sum(prob * crra_utility(max(asset.V * R, 1e-9), gamma)
                    for R, prob in zip(dist.returns, dist.probs))
    eu_free   = sum(s["prob"] * crra_utility(s["C_free"],   gamma) for s in states)
    eu_locked = sum(s["prob"] * crra_utility(s["C_locked"], gamma) for s in states)
    cew_free   = consumption_equiv_welfare(eu_free,   eu_notax, gamma)
    cew_locked = consumption_equiv_welfare(eu_locked, eu_notax, gamma)

    p_below_rA   = sum(s["prob"] for s in states if s["r_B"] <  asset.r_A)
    p_locked_cgt = sum(s["prob"] for s in states if asset.r_A <= s["r_B"] < r_B_indiff)

    return {
        "cew_free":        _f(cew_free),
        "cew_locked":      _f(cew_locked),
        "lock_in_cost_bp": _f((cew_free - cew_locked) * 10000),
        "p_locked":        _f(p_below_rA + p_locked_cgt),
        "p_locked_cgt":    _f(p_locked_cgt),
        "p_below_rA":      _f(p_below_rA),
        "r_B_indiff":      _f(r_B_indiff),
        "switch_cost":     _f(asset.switch_cost_pv()),
    }


def _full_lockin_comparison(W0, dist, gamma, target_et, asset) -> dict:
    m1      = run_welfare_comparison(W0, dist, gamma, target_et)
    wdt_cew = m1["symmetric_wdt"].cew
    cgt_cew = m1["cgt"].cew
    lock    = _compute_lockin_cost(asset, dist, gamma)
    lock_bp = lock["lock_in_cost_bp"]
    return {
        "wdt_cew":              _f(wdt_cew),
        "cgt_cew":              _f(cgt_cew),
        "lock_in_cost_bp":      lock_bp,
        "cgt_with_lock_cew":    _f(cgt_cew - lock_bp / 10000),
        "wdt_adv_no_lock_bp":   _f((wdt_cew - cgt_cew) * 10000),
        "wdt_adv_with_lock_bp": _f((wdt_cew - (cgt_cew - lock_bp / 10000)) * 10000),
        "p_locked":             lock["p_locked"],
        "p_locked_cgt":         lock["p_locked_cgt"],
        "p_below_rA":           lock["p_below_rA"],
        "r_B_indiff":           lock["r_B_indiff"],
        "m1_cgt_tau":           _f(m1["cgt"].tau),
        "m1_wdt_tau":           _f(m1["symmetric_wdt"].tau),
    }


def run_module3(p: dict) -> dict:
    print("\n=== Module 3: CGT Lock-In ===")
    N       = p["tcm"]["canonical_N"]
    dist_A  = make_empirical_distribution_scenario(p, N)
    dist_B  = make_idealised_distribution_scenario(p, N)
    tau_cgt = 0.24
    V_ref   = 10.0
    G_ref   = V_ref * 0.50
    r_A     = p["tcm"]["hist_mean"]

    asset_ref = AssetSwitchDecision(V=V_ref, B=V_ref - G_ref, tau_cgt=tau_cgt, T=5, r_A=r_A)
    r_B_grid  = np.linspace(r_A * 0.5, r_A * 2.5, 300)

    print("  Sensitivity: gain ratio sweep...")
    gain_ratios = np.linspace(0.05, 0.90, 20)
    sens_gain = []
    for gr in gain_ratios:
        a = AssetSwitchDecision(V=V_ref, B=V_ref - V_ref * gr, tau_cgt=tau_cgt, T=5, r_A=r_A)
        r = _compute_lockin_cost(a, dist_A, GAMMA_CEN)
        r["gain_ratio"] = _f(gr)
        sens_gain.append(r)

    print("  Sensitivity: holding period sweep...")
    sens_T = []
    for T in range(1, 21):
        a = AssetSwitchDecision(V=V_ref, B=V_ref - G_ref, tau_cgt=tau_cgt, T=T, r_A=r_A)
        r = _compute_lockin_cost(a, dist_A, GAMMA_CEN)
        r["T"] = T
        sens_T.append(r)

    print("  Full welfare comparison...")
    full = {
        dist.label: _full_lockin_comparison(10.0, dist, GAMMA_CEN, TARGET_ET * 10.0, asset_ref)
        for dist in [dist_A, dist_B]
    }

    return {
        "asset_ref": {
            "V": _f(V_ref), "B": _f(V_ref - G_ref), "G": _f(G_ref),
            "gain_ratio": _f(asset_ref.gain_ratio), "tau_cgt": _f(tau_cgt),
            "T": int(asset_ref.T), "r_A": _f(r_A),
            "r_B_indiff": _f(asset_ref.indifference_return()),
            "switch_cost": _f(asset_ref.switch_cost_pv()),
        },
        "threshold_curve": {
            "r_B_grid": _arr(r_B_grid),
            "npv_diff": _arr(asset_ref.value_of_stay(r_B_grid)),
            "r_B_indiff": _f(asset_ref.indifference_return()),
        },
        "sens_gain": sens_gain,
        "sens_T":    sens_T,
        "full_comparison": full,
    }


# ─────────────────────────────────────────────────────────────────────────────
# 13. MODULE 4 — HETEROGENEOUS AGENTS
# ─────────────────────────────────────────────────────────────────────────────

@dataclass
class AgentTier:
    name: str; differential: float; pop_share: float
    W0: float; bracket_label: str = ""

    def shifted_distribution(self, base_dist: ReturnDistribution) -> ReturnDistribution:
        shifted = np.maximum(base_dist.returns + self.differential, 0.01)
        return ReturnDistribution(
            returns=shifted, probs=base_dist.probs.copy(),
            label=f"{base_dist.label[:30]} | {self.name} (+{self.differential*100:.2f}pp)"
        )


def _build_tiers(p: dict) -> list:
    bracket_map  = {b["label"]: b["V0_m"] for b in p["brackets"]}
    tier_bracket = {"Poor": "95%", "Ok": "99%", "Good": "99.9%", "Great": "99.99%+"}
    return [
        AgentTier(
            name=t["label"], differential=t["differential"],
            pop_share=t["weight"],
            W0=bracket_map[tier_bracket[t["label"]]],
            bracket_label=tier_bracket[t["label"]],
        )
        for t in p["tiers"]
    ]


def _solve_aggregate_rate(tiers, base_dist, tax_fn_name, agg_target) -> Optional[float]:
    tax_fn  = get_tax_fn(tax_fn_name)
    shifted = {t.name: t.shifted_distribution(base_dist) for t in tiers}

    def agg_et(tau):
        return sum(t.pop_share * expected_tax(t.W0, shifted[t.name], tax_fn, tau) for t in tiers)

    try:
        lo, hi = agg_et(1e-6), agg_et(0.999)
    except Exception:
        return None
    if lo > agg_target or hi < agg_target:
        return None
    return float(brentq(lambda tau: agg_et(tau) - agg_target, 1e-6, 0.999, xtol=1e-10, rtol=1e-10))


def _run_tier_comparison(tiers, base_dist, gamma, rate_fn) -> dict:
    agg_W0     = sum(t.pop_share * t.W0 for t in tiers)
    agg_target = TARGET_ET * agg_W0
    agg_taus   = {name: _solve_aggregate_rate(tiers, base_dist, name, agg_target) for name in SYSTEMS}
    shifted    = {t.name: t.shifted_distribution(base_dist) for t in tiers}

    tier_results = {}
    for tier in tiers:
        dist_t   = shifted[tier.name]
        eu_notax = expected_utility(tier.W0, dist_t, tax_symmetric_flat, 0.0, gamma)
        sys_res  = {}
        for name in SYSTEMS:
            tau = agg_taus[name]
            if tau is None:
                sys_res[name] = {"tau": None, "eu": None, "cew": None,
                                  "expected_tax": None, "var_consumption": None, "et_pct_W0": None}
                continue
            tax_fn = get_tax_fn(name)
            eu     = expected_utility(tier.W0, dist_t, tax_fn, tau, gamma)
            et     = expected_tax(tier.W0, dist_t, tax_fn, tau)
            sys_res[name] = {
                "tau": _f(tau), "eu": _f(eu),
                "cew": _f(consumption_equiv_welfare(eu, eu_notax, gamma)),
                "expected_tax": _f(et),
                "var_consumption": _f(variance_of_consumption(tier.W0, dist_t, tax_fn, tau)),
                "et_pct_W0": _f(et / tier.W0 * 100),
            }

        eu_prog  = expected_utility_progressive(tier.W0, dist_t, rate_fn, gamma)
        eu_notax2 = expected_utility(tier.W0, dist_t, tax_symmetric_flat, 0.0, gamma)
        tier_results[tier.name] = {
            "systems":         sys_res,
            "cew_progressive": _f(consumption_equiv_welfare(eu_prog, eu_notax2, gamma)),
            "et_progressive":  _f(expected_tax_progressive(tier.W0, dist_t, rate_fn)),
            "agg_taus":        {k: _f(v) for k, v in agg_taus.items()},
        }
    return tier_results


def _project_wealth_path(W0, returns_seq, tax_fn, tau) -> list:
    W, path = W0, [W0]
    for R in returns_seq:
        W = max(tax_fn(W, R, tau).post_tax_wealth, 0.001)
        path.append(W)
    return [_f(x) for x in path]


def _project_progressive_path(W0, returns_seq, rate_fn) -> list:
    W, path = W0, [W0]
    for R in returns_seq:
        _, W_post, _ = tax_progressive_wdt(W, R, rate_fn)
        W = max(W_post, 0.001)
        path.append(W)
    return [_f(x) for x in path]


def _run_concentration(tiers, p, rate_fn, systems, precomputed_taus, N) -> tuple:
    returns_seq, years = make_scenario_sequence(p, N)
    paths = {name: {} for name in systems}
    for tier in tiers:
        gross = np.maximum(1.0 + returns_seq + tier.differential, 0.01)
        for name in systems:
            if name == "progressive_wdt":
                paths[name][tier.name] = _project_progressive_path(tier.W0, gross, rate_fn)
            elif precomputed_taus.get(name) is None:
                paths[name][tier.name] = [None] * (N + 1)
            else:
                paths[name][tier.name] = _project_wealth_path(
                    tier.W0, gross, get_tax_fn(name), precomputed_taus[name]
                )
    return paths, [int(y) for y in years]


def _run_concentration_extended(tiers, p, rate_fn, systems, precomputed_taus) -> tuple:
    returns_seq = p["returns_meta"]["array"]
    years       = p["returns_meta"]["years"]
    paths = {name: {} for name in systems}
    for tier in tiers:
        gross = np.maximum(1.0 + returns_seq + tier.differential, 0.01)
        for name in systems:
            if name == "progressive_wdt":
                paths[name][tier.name] = _project_progressive_path(tier.W0, gross, rate_fn)
            elif precomputed_taus.get(name) is None:
                paths[name][tier.name] = [None] * (len(returns_seq) + 1)
            else:
                paths[name][tier.name] = _project_wealth_path(
                    tier.W0, gross, get_tax_fn(name), precomputed_taus[name]
                )
    return paths, [int(y) for y in years]


def _find_crossover(paths_ext, start_year, threshold=1.0) -> Optional[dict]:
    great_flat = paths_ext.get("symmetric_wdt", {}).get("Great")
    poor_flat  = paths_ext.get("symmetric_wdt", {}).get("Poor")
    great_prog = paths_ext.get("progressive_wdt", {}).get("Great")
    poor_prog  = paths_ext.get("progressive_wdt", {}).get("Poor")
    if not all([great_flat, poor_flat, great_prog, poor_prog]):
        return None
    for idx, (gf, pf, gp, pp) in enumerate(zip(great_flat, poor_flat, great_prog, poor_prog)):
        if pf is None or pp is None or pf <= 0 or pp <= 0:
            continue
        if (gp / pp) - (gf / pf) < -threshold:
            year = start_year - 1 if idx == 0 else start_year + idx - 1
            return {"year": int(year), "ratio_flat": _f(gf/pf), "ratio_prog": _f(gp/pp),
                    "gap": _f((gp/pp) - (gf/pf))}
    return None


def _test_envelope_binding(tiers, p, rate_fn, N) -> dict:
    returns_seq, years = make_scenario_sequence(p, N)
    results = {}
    for tier in tiers:
        gross = np.maximum(1.0 + returns_seq + tier.differential, 0.01)
        W, cum_tax, cum_ref = tier.W0, 0.0, 0.0
        year_log, binding_years = [], []
        for yr, R in zip(years, gross):
            tax, W_post, _ = tax_progressive_wdt(W, R, rate_fn)
            if tax >= 0:
                cum_tax += tax
            else:
                refund = abs(tax)
                if cum_ref + refund > cum_tax:
                    capped = max(cum_tax - cum_ref, 0.0)
                    refund = capped; tax = -capped; W_post = W * R - tax
                    binding_years.append(int(yr))
                cum_ref += refund
            W = max(W_post, 0.001)
            year_log.append({
                "year": int(yr), "R": _f(R), "tax": _f(tax),
                "cum_tax": _f(cum_tax), "cum_ref": _f(cum_ref),
                "W_end": _f(W), "envelope_slack": _f(cum_tax - cum_ref),
            })
        results[tier.name] = {
            "ever_binds":    len(binding_years) > 0,
            "binding_years": binding_years,
            "min_slack":     _f(min(y["envelope_slack"] for y in year_log)),
            "cum_tax_final": _f(cum_tax),
            "cum_ref_final": _f(cum_ref),
            "W_final":       _f(W),
            "year_log":      year_log,
        }
    return results


def _run_corner_check(tiers, base_dist, gamma, rate_fn) -> dict:
    poor  = next(t for t in tiers if t.name == "Poor")
    great = next(t for t in tiers if t.name == "Great")
    corners = [
        ("corner_A", "Great diff, Poor W₀",  great.differential, poor.W0,  poor.bracket_label),
        ("corner_B", "Poor diff, Great W₀",  poor.differential,  great.W0, great.bracket_label),
    ]
    out = {}
    for key, label, diff, W0, bracket in corners:
        shifted = np.maximum(base_dist.returns + diff, 0.01)
        dist_c  = ReturnDistribution(
            returns=shifted, probs=base_dist.probs.copy(),
            label=f"{label} ({diff*100:+.2f}pp, W₀=£{W0:.1f}m)"
        )
        target_et = TARGET_ET * W0
        eu_notax  = expected_utility(W0, dist_c, tax_symmetric_flat, 0.0, gamma)
        sys_res   = {}
        for name in SYSTEMS:
            tax_fn = get_tax_fn(name)
            try:
                tau   = solve_revenue_equivalent_rate(W0, dist_c, tax_fn, target_et)
                eu    = expected_utility(W0, dist_c, tax_fn, tau, gamma)
                sys_res[name] = {
                    "tau": _f(tau),
                    "eu":  _f(eu),
                    "cew": _f(consumption_equiv_welfare(eu, eu_notax, gamma)),
                    "expected_tax":    _f(expected_tax(W0, dist_c, tax_fn, tau)),
                    "var_consumption": _f(variance_of_consumption(W0, dist_c, tax_fn, tau)),
                }
            except ValueError:
                sys_res[name] = {"tau": None, "eu": None, "cew": None,
                                  "expected_tax": None, "var_consumption": None}

        eu_prog  = expected_utility_progressive(W0, dist_c, rate_fn, gamma)
        out[key] = {
            "label": label, "W0": _f(W0), "differential": _f(diff),
            "bracket_label": bracket, "systems": sys_res,
            "cew_progressive": _f(consumption_equiv_welfare(eu_prog, eu_notax, gamma)),
            "et_progressive":  _f(expected_tax_progressive(W0, dist_c, rate_fn)),
        }
    return out


def run_module4(p: dict) -> dict:
    print("\n=== Module 4: Heterogeneous Agents ===")
    N       = p["tcm"]["canonical_N"]
    dist_A  = make_empirical_distribution_scenario(p, N)
    rate_fn = build_rate_fn(p)
    tiers   = _build_tiers(p)

    tiers_out = [
        {"name": t.name, "differential": _f(t.differential),
         "pop_share": _f(t.pop_share), "W0": _f(t.W0), "bracket_label": t.bracket_label}
        for t in tiers
    ]

    print("  Tier welfare comparison...")
    tier_welfare = _run_tier_comparison(tiers, dist_A, GAMMA_CEN, rate_fn)
    agg_taus = {
        name: tier_welfare["Good"]["agg_taus"].get(name)
        for name in SYSTEMS
        if tier_welfare["Good"]["agg_taus"].get(name) is not None
    }

    systems_proj = ["symmetric_wdt", "progressive_wdt", "stock_wealth", "income", "consumption"]

    print("  Concentration analysis (scenario)...")
    conc_paths, conc_years = _run_concentration(tiers, p, rate_fn, systems_proj, agg_taus, N)

    print("  Concentration analysis (extended)...")
    ext_paths, ext_years = _run_concentration_extended(tiers, p, rate_fn, systems_proj, agg_taus)
    crossover = _find_crossover(ext_paths, ext_years[0])

    print("  Envelope binding test...")
    envelope = _test_envelope_binding(tiers, p, rate_fn, N)

    print("  Corner check...")
    corners = _run_corner_check(tiers, dist_A, GAMMA_CEN, rate_fn)

    return {
        "tiers":        tiers_out,
        "tier_welfare": tier_welfare,
        "concentration": {
            "scenario": {"years": conc_years, "systems": conc_paths},
            "extended":  {"years": ext_years,  "systems": ext_paths, "crossover": crossover},
        },
        "envelope":    envelope,
        "corner_check": corners,
    }


# ─────────────────────────────────────────────────────────────────────────────
# 14. MODULE 5 — WELFARE SWEEP ANALYSIS
# ─────────────────────────────────────────────────────────────────────────────

def _run_sweep_a_revenue(p: dict) -> dict:
    print("  Sweep A: revenue target...")
    sw          = p["sweep"]
    target_pcts = sw["wfr_target_et_pct"]
    gamma_vals  = sw["wfr_gamma_vals"]
    N           = p["tcm"]["canonical_N"]
    dist_A      = make_empirical_distribution_scenario(p, N)
    dist_B      = make_idealised_distribution_scenario(p, N)
    dists       = {"A": dist_A, "B": dist_B}
    out         = {}
    for pct in target_pcts:
        target_et = (pct / 100.0) * W0_NORM
        out[str(pct)] = {}
        for dlabel, dist in dists.items():
            out[str(pct)][dlabel] = {}
            for gamma in gamma_vals:
                comp = run_welfare_comparison(W0_NORM, dist, gamma, target_et)
                out[str(pct)][dlabel][str(gamma)] = {name: _f(r.cew) for name, r in comp.items()}
    return out


def _run_sweep_a_w0(p: dict) -> dict:
    print("  Sweep A: W0 sensitivity...")
    N      = p["tcm"]["canonical_N"]
    dist_A = make_empirical_distribution_scenario(p, N)
    out    = {}
    for W0 in p["sweep"]["wfr_W0_sweep"]:
        try:
            comp = run_welfare_comparison(W0, dist_A, GAMMA_CEN, 0.02 * W0)
            out[str(W0)] = {name: _f(r.cew) for name, r in comp.items()}
        except ValueError:
            out[str(W0)] = {name: None for name in SYSTEMS}
    return out


def _run_sweep_b_start_year(p: dict) -> dict:
    print("  Sweep B: start-year sweep (73 windows)...")
    N         = p["tcm"]["canonical_N"]
    base_yr   = p["returns_meta"]["series_base_year"]
    target_et = 0.02 * W0_NORM
    out       = {}
    for start_yr in range(base_yr, base_yr + 73):
        dist, _ = make_empirical_distribution_for_start(p, start_yr, N)
        if dist is None:
            continue
        try:
            comp = run_welfare_comparison(W0_NORM, dist, GAMMA_CEN, target_et)
            out[str(start_yr)] = {name: _f(r.cew) for name, r in comp.items()}
        except ValueError:
            out[str(start_yr)] = {name: None for name in SYSTEMS}
        if start_yr % 10 == 0:
            print(f"    start_year={start_yr}")
    return out


def _run_sweep_c_params(p: dict) -> dict:
    print("  Sweep C: parameter sensitivity...")
    N      = p["tcm"]["canonical_N"]
    dist_A = make_empirical_distribution_scenario(p, N)
    rp     = p["rate"]
    sw     = p["sweep"]
    W0_vals = [10.0, 30.0, 100.0]
    param_configs = [
        ("tau_0", sw["wfr_tau_0_sweep"]),
        ("tau_m", sw["wfr_tau_m_sweep"]),
        ("k",     sw["wfr_k_sweep"]),
        ("W_min", sw["wfr_wmin_sweep"]),
    ]
    out = {}
    for param_name, param_vals in param_configs:
        out[param_name] = {}
        for W0 in W0_vals:
            out[param_name][str(W0)] = {}
            for pval in param_vals:
                kwargs = dict(tau0=rp["tau_0"], taum=rp["tau_m"], k=rp["k"], W_min=rp["W_min"])
                if param_name == "tau_0":   kwargs["tau0"]  = pval
                elif param_name == "tau_m": kwargs["taum"]  = pval
                elif param_name == "k":     kwargs["k"]     = pval
                elif param_name == "W_min": kwargs["W_min"] = pval

                if kwargs["tau0"] >= kwargs["taum"]:
                    out[param_name][str(W0)][str(pval)] = None
                    continue

                rate_fn   = ProgressiveRateFunction(**kwargs)
                target_et = 0.02 * W0
                scale     = _solve_progressive_scale(W0, dist_A, rate_fn, target_et)
                if scale is None:
                    out[param_name][str(W0)][str(pval)] = None
                    continue

                scaled_fn = ScaledRateFn(rate_fn, scale)
                flat_fn   = get_tax_fn("symmetric_wdt")
                eu_notax  = expected_utility(W0, dist_A, flat_fn, 0.0, GAMMA_CEN)
                eu_prog   = expected_utility_progressive(W0, dist_A, scaled_fn, GAMMA_CEN)
                cew_prog  = consumption_equiv_welfare(eu_prog, eu_notax, GAMMA_CEN)
                tau_flat  = solve_revenue_equivalent_rate(W0, dist_A, flat_fn, target_et)
                eu_flat   = expected_utility(W0, dist_A, flat_fn, tau_flat, GAMMA_CEN)
                cew_flat  = consumption_equiv_welfare(eu_flat, eu_notax, GAMMA_CEN)
                out[param_name][str(W0)][str(pval)] = _f((cew_flat - cew_prog) * 10000)
        print(f"    {param_name} done")
    return out


def run_module5(p: dict) -> dict:
    print("\n=== Module 5: Welfare Sweeps ===")
    return {
        "sweep_a_revenue":    _run_sweep_a_revenue(p),
        "sweep_a_w0":         _run_sweep_a_w0(p),
        "sweep_b_start_year": _run_sweep_b_start_year(p),
        "sweep_c_params":     _run_sweep_c_params(p),
    }


# ─────────────────────────────────────────────────────────────────────────────
# 15. CLI ENTRY POINT
# ─────────────────────────────────────────────────────────────────────────────

def main(modules: list = None, out_path: Path = None) -> dict:
    """
    Run the specified modules and write wfr_results.json.

    Parameters
    ----------
    modules  : list of ints 1–5, or None for all
    out_path : output JSON path, or None to use default
    """
    if modules is None:
        modules = [1, 2, 3, 4, 5]
    if out_path is None:
        out_path = OUTPUT_DIR / "wfr_results.json"

    print(f"WFR Core — running modules {modules}")
    p = load_params(str(TOML_PATH))

    result = {
        "meta": {
            "version":    "wfr_core_v2",
            "date":       date.today().isoformat(),
            "modules_run": modules,
            "params": {
                "toml_path":          str(TOML_PATH),
                "canonical_N":        p["tcm"]["canonical_N"],
                "scenario_start_year": p["tcm"].get("scenario_start_year"),
                "hist_mean":          p["tcm"]["hist_mean"],
                "rate":               p["rate"],
                "W0_norm":            W0_NORM,
                "target_et_frac":     TARGET_ET,
                "gamma_vals":         GAMMA_VALS,
            },
        }
    }

    if 1 in modules: result["module1"] = run_module1(p)
    if 2 in modules: result["module2"] = run_module2(p)
    if 3 in modules: result["module3"] = run_module3(p)
    if 4 in modules: result["module4"] = run_module4(p)
    if 5 in modules: result["module5"] = run_module5(p)

    out_path.parent.mkdir(parents=True, exist_ok=True)
    with open(out_path, "w", encoding="utf-8") as fh:
        json.dump(_sanitise(result), fh, indent=2)
    print(f"\n✓ Results written to: {out_path}")
    return result


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="WFR Welfare Computation Engine")
    parser.add_argument("--modules", nargs="+", type=int, choices=[1, 2, 3, 4, 5],
                        help="Which modules to run (default: all)")
    parser.add_argument("--out", type=Path, help="Output JSON path")
    args = parser.parse_args()
    main(modules=args.modules, out_path=args.out)
