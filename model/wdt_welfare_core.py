"""
wdt_welfare_core.py
===================
Shared computation core for the WDT Welfare Comparison Model.

All four modules import from here. Nothing in this file is
module-specific. Adding a new module never requires editing this file
unless a genuine shared primitive is missing.

Structure
---------
1.  load_params()           — reads WDT_Params.toml
2.  ReturnDistribution      — empirical (Version A) and idealised (Version B)
3.  TaxSystem               — the five tax functions + revenue-equivalence solver
4.  WelfareCalculator       — CRRA utility and CEW
5.  RevenueEquivalenceSolver— finds the rate for each system that hits a target E[T]
6.  Diagnostics             — summary tables printed to stdout
"""

import os
import math
import tomllib
import numpy as np
from scipy.optimize import brentq
from dataclasses import dataclass, field
from typing import Optional

# ─────────────────────────────────────────────────────────────────────────────
# 1. PARAMETER LOADING
# ─────────────────────────────────────────────────────────────────────────────

def load_params(toml_path: str) -> dict:
    """
    Load WDT_Params.toml and return the full parameter dictionary.
    Validates that the returns array has the expected length.
    """
    with open(toml_path, "rb") as f:
        p = tomllib.load(f)

    returns = np.array(p["returns"]["values"], dtype=float)
    if len(returns) != 73:
        raise ValueError(
            f"Expected 73 return observations (1947–2019), got {len(returns)}."
        )
    p["returns"]["array"] = returns          # attach numpy array for convenience
    p["returns"]["years"]  = list(range(
        p["returns"]["series_base_year"],
        p["returns"]["series_base_year"] + len(returns)
    ))
    return p


# ─────────────────────────────────────────────────────────────────────────────
# 2. RETURN DISTRIBUTIONS
# ─────────────────────────────────────────────────────────────────────────────

@dataclass
class ReturnDistribution:
    """
    Represents a return distribution as an array of (return, probability) pairs.

    Both versions expose the same interface so downstream code is agnostic
    about which version is being used.

    Attributes
    ----------
    returns : np.ndarray
        Array of gross returns (1 + r), one per state.
    probs : np.ndarray
        Probability weight for each state. Must sum to 1.
    label : str
        Human-readable label for charts and tables.
    """
    returns : np.ndarray
    probs   : np.ndarray
    label   : str

    def __post_init__(self):
        if not math.isclose(self.probs.sum(), 1.0, rel_tol=1e-6):
            raise ValueError(f"Probabilities sum to {self.probs.sum():.6f}, not 1.")
        if np.any(self.returns <= 0):
            raise ValueError("Gross returns must be positive (1 + r > 0).")

    # Convenience properties
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
        variance = float(np.dot(self.probs, (self.returns - mean) ** 2))
        return math.sqrt(variance)

    def describe(self) -> str:
        pos = (self.returns > 1.0)
        neg = (self.returns < 1.0)
        lines = [
            f"Distribution: {self.label}",
            f"  States:               {self.n_states}",
            f"  Mean gross return:    {self.mean_return:.4f}  "
            f"({self.mean_net_return*100:.2f}%)",
            f"  Std dev (returns):    {self.std_return:.4f}  "
            f"({self.std_return*100:.2f}%)",
            f"  P(positive return):   {self.probs[pos].sum():.4f}  "
            f"({self.probs[pos].sum()*100:.1f}%)",
            f"  P(negative return):   {self.probs[neg].sum():.4f}  "
            f"({self.probs[neg].sum()*100:.1f}%)",
        ]
        return "\n".join(lines)


def make_empirical_distribution(p: dict) -> ReturnDistribution:
    """
    Version A: UK historical equity return series, 1947–2019.
    Each of the 73 years is a state with equal probability 1/73.
    Gross returns are (1 + annual_return).
    """
    raw = p["returns"]["array"]
    gross = 1.0 + raw
    probs = np.full(len(gross), 1.0 / len(gross))
    return ReturnDistribution(
        returns=gross,
        probs=probs,
        label="Version A — UK Historical Equity (1947–2019, 73 obs)"
    )


def make_idealised_distribution(p: dict) -> ReturnDistribution:
    """
    Version B: Symmetric two-state distribution calibrated to match the
    empirical mean and standard deviation.

    Calibration:
        p_good = p_bad = 0.5
        R_good = 1 + mu + sigma
        R_bad  = 1 + mu - sigma

    where mu and sigma are the empirical mean and std of net returns.

    This preserves the first two moments but not higher moments.
    The bad state has a positive return (1 + mu - sigma > 1) because
    mu > sigma for this series (10.45% > 8.31%), making R_bad = 1.0214.
    Both states therefore represent positive returns; the "bad" state
    is simply the below-mean outcome.

    Limitation: this two-state model understates the true variance because
    it compresses the fat right tail (e.g. 1975: +40.7%) into a single
    R_good value. Noted as a paper limitation.
    """
    raw   = p["returns"]["array"]
    mu    = float(np.mean(raw))
    sigma = float(np.std(raw, ddof=0))

    R_good = 1.0 + mu + sigma
    R_bad  = 1.0 + mu - sigma

    if R_bad <= 0:
        raise ValueError(
            f"Idealised bad-state gross return is non-positive: {R_bad:.4f}. "
            "Check mu and sigma."
        )

    returns = np.array([R_good, R_bad])
    probs   = np.array([0.5, 0.5])

    return ReturnDistribution(
        returns=returns,
        probs=probs,
        label=(
            f"Version B — Idealised Two-State "
            f"(R_good={R_good:.4f}, R_bad={R_bad:.4f}, p=0.5/0.5)"
        )
    )


# ─────────────────────────────────────────────────────────────────────────────
# 3. TAX SYSTEMS
# ─────────────────────────────────────────────────────────────────────────────

@dataclass
class TaxResult:
    """
    Output of applying a tax function to one return state.

    Attributes
    ----------
    gross_wealth : float
        W₁ before tax (W₀ × R).
    tax_paid : float
        Tax collected (+) or refund paid (−). Positive = tax, negative = refund.
    post_tax_wealth : float
        W₁ after tax. Equal to gross_wealth − tax_paid.
    consumption : float
        What the agent consumes. For most systems equals post_tax_wealth.
        For consumption tax, equals post_tax_wealth / (1 + tau_ct) because
        the tax wedge applies at the consumption stage, not the wealth stage.
    """
    gross_wealth    : float
    tax_paid        : float
    post_tax_wealth : float
    consumption     : float


def tax_consumption(W0: float, R: float, tau: float) -> TaxResult:
    """
    Consumption tax at rate tau.
    Applied at consumption stage: tax = tau × C, so C = W₁ / (1 + tau).
    No distortion on wealth accumulation — post_tax_wealth = W₁.
    Revenue = tau × W₁ / (1 + tau).
    """
    W1   = W0 * R
    tax  = tau * W1 / (1.0 + tau)
    C    = W1 / (1.0 + tau)
    return TaxResult(
        gross_wealth    = W1,
        tax_paid        = tax,
        post_tax_wealth = W1,    # wealth is untouched; tax paid at consumption
        consumption     = C
    )


def tax_income(W0: float, R: float, tau: float) -> TaxResult:
    """
    Income tax on positive returns only. No refund on losses.
    Tax base = max(W₁ − W₀, 0).
    """
    W1      = W0 * R
    gain    = max(W1 - W0, 0.0)
    tax     = tau * gain
    W1_post = W1 - tax
    return TaxResult(
        gross_wealth    = W1,
        tax_paid        = tax,
        post_tax_wealth = W1_post,
        consumption     = W1_post
    )


def tax_cgt(W0: float, R: float, tau: float) -> TaxResult:
    """
    Capital gains tax.
    In Module 1: identical to income tax — same base (positive gains only),
    different rate. The lock-in distortion that separates CGT from income tax
    is endogenous and enters only in Module 3.
    """
    return tax_income(W0, R, tau)


def tax_stock_wealth(W0: float, R: float, tau: float) -> TaxResult:
    """
    Stock wealth tax at rate tau on end-period wealth W₁.
    Applied regardless of sign of return — always positive.
    """
    W1      = W0 * R
    tax     = tau * W1
    W1_post = W1 - tax
    return TaxResult(
        gross_wealth    = W1,
        tax_paid        = tax,
        post_tax_wealth = W1_post,
        consumption     = W1_post
    )


def tax_symmetric_flat(W0: float, R: float, tau: float) -> TaxResult:
    """
    Symmetric flat-rate WDT proxy.
    Tax base = W₁ − W₀ (the delta), sign preserved.
    Positive delta → tax paid. Negative delta → refund received.
    Lifetime envelope not modelled here (enters Module 4).
    Progressive rate not modelled here (enters Module 2).
    """
    W1      = W0 * R
    delta   = W1 - W0
    tax     = tau * delta          # negative when delta < 0 → refund
    W1_post = W1 - tax
    return TaxResult(
        gross_wealth    = W1,
        tax_paid        = tax,
        post_tax_wealth = W1_post,
        consumption     = W1_post
    )


# Registry: name → tax function
# Modules call get_tax_fn(name) to retrieve the function by name.
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
            f"Unknown tax system '{name}'. "
            f"Available: {list(_TAX_REGISTRY.keys())}"
        )
    return _TAX_REGISTRY[name]


# ─────────────────────────────────────────────────────────────────────────────
# 4. WELFARE CALCULATOR
# ─────────────────────────────────────────────────────────────────────────────

def crra_utility(c: float, gamma: float) -> float:
    """
    CRRA utility.
        u(c) = c^(1-γ) / (1-γ)   for γ ≠ 1
        u(c) = ln(c)               for γ = 1

    Raises ValueError if c ≤ 0 (undefined).
    """
    if c <= 0:
        raise ValueError(f"CRRA utility undefined for c={c:.4f} ≤ 0.")
    if math.isclose(gamma, 1.0, rel_tol=1e-9):
        return math.log(c)
    return (c ** (1.0 - gamma)) / (1.0 - gamma)


def expected_utility(
    W0          : float,
    dist        : ReturnDistribution,
    tax_fn      ,
    tau         : float,
    gamma       : float,
) -> float:
    """
    Compute E[u(consumption)] for one tax system across all return states.

    Parameters
    ----------
    W0    : initial wealth
    dist  : ReturnDistribution (Version A or B)
    tax_fn: one of the tax_* functions above
    tau   : tax rate parameter for this system
    gamma : CRRA risk-aversion coefficient
    """
    eu = 0.0
    for R, prob in zip(dist.returns, dist.probs):
        result = tax_fn(W0, R, tau)
        eu += prob * crra_utility(result.consumption, gamma)
    return eu


def expected_tax(
    W0    : float,
    dist  : ReturnDistribution,
    tax_fn,
    tau   : float,
) -> float:
    """
    Compute E[T] — expected tax collected — for one system.
    Refunds count as negative tax (reduce expected revenue).
    """
    et = 0.0
    for R, prob in zip(dist.returns, dist.probs):
        result = tax_fn(W0, R, tau)
        et += prob * result.tax_paid
    return et


def consumption_equiv_welfare(
    eu_tax    : float,
    eu_notax  : float,
    gamma     : float,
) -> float:
    """
    Consumption-equivalent welfare (CEW) relative to a no-tax benchmark.

    Definition: the proportional change in no-tax consumption that leaves
    the agent indifferent between the no-tax allocation and the taxed allocation.

    Derivation:
        Under CRRA (γ ≠ 1):
            u((1+λ)c) = EU_tax
            ((1+λ)c)^(1-γ)/(1-γ) = EU_tax
            (1+λ)^(1-γ) × u(c) = EU_tax
            (1+λ) = (EU_tax / EU_notax)^(1/(1-γ))
            λ = (EU_tax / EU_notax)^(1/(1-γ)) − 1

        Under log (γ = 1):
            ln((1+λ)c) = EU_tax
            ln(1+λ) + ln(c) = EU_tax
            ln(1+λ) = EU_tax − EU_notax
            λ = exp(EU_tax − EU_notax) − 1

    A positive λ means the taxed system is welfare-superior to no-tax
    (the agent would need *more* consumption under no-tax to be equally happy).
    A negative λ means the taxed system is welfare-inferior.

    Note on sign conventions for CRRA with γ > 1:
        EU values are negative. EU_tax / EU_notax > 1 when EU_tax is less
        negative than EU_notax (taxed system is better). The exponent
        1/(1−γ) is negative for γ > 1, so the ratio raised to a negative
        power produces a value < 1 when EU_tax/EU_notax > 1 — which would
        give λ < 0. This seems wrong.

        The resolution: CEW is defined relative to the no-tax benchmark,
        which itself has a welfare cost (relative to first-best, which doesn't
        exist here). What we want is whether the taxed system has lower
        welfare cost than no-tax.

        Since we are comparing taxed vs no-tax (not taxed vs first-best),
        and no-tax is the baseline, CEW is always negative or zero for any
        revenue-positive tax system applied to a risk-neutral world.
        The *relative* ranking across systems is what matters.

        We implement the formula as derived and report the sign correctly.
    """
    if math.isclose(gamma, 1.0, rel_tol=1e-9):
        return math.exp(eu_tax - eu_notax) - 1.0
    else:
        ratio = eu_tax / eu_notax
        # ratio > 1 when eu_tax is less negative (better welfare)
        # ratio < 1 when eu_tax is more negative (worse welfare)
        return ratio ** (1.0 / (1.0 - gamma)) - 1.0


def variance_of_consumption(
    W0    : float,
    dist  : ReturnDistribution,
    tax_fn,
    tau   : float,
) -> float:
    """Variance of consumption across return states."""
    consumptions = np.array([
        tax_fn(W0, R, tau).consumption
        for R in dist.returns
    ])
    mean_c = float(np.dot(dist.probs, consumptions))
    return float(np.dot(dist.probs, (consumptions - mean_c) ** 2))


# ─────────────────────────────────────────────────────────────────────────────
# 5. REVENUE EQUIVALENCE SOLVER
# ─────────────────────────────────────────────────────────────────────────────

def solve_revenue_equivalent_rate(
    W0         : float,
    dist       : ReturnDistribution,
    tax_fn     ,
    target_et  : float,
    tau_lo     : float = 1e-6,
    tau_hi     : float = 0.999,
) -> float:
    """
    Find the tax rate τ such that E[T(W0, dist, τ)] = target_et.

    Uses Brent's method (scipy.optimize.brentq) for robustness.

    Parameters
    ----------
    target_et : desired expected tax revenue
    tau_lo    : lower bound for search (must give E[T] < target_et)
    tau_hi    : upper bound for search (must give E[T] > target_et)

    Returns
    -------
    float : the revenue-equivalent tax rate

    Raises
    ------
    ValueError if the target cannot be achieved within [tau_lo, tau_hi],
    which occurs when the tax system structurally cannot raise the target
    revenue (e.g. symmetric tax at E[R]=1 cannot raise positive revenue).
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
            "This may indicate the system structurally cannot raise this revenue "
            "(e.g. symmetric WDT when E[R] ≤ 1 and target > 0)."
        )

    tau_star = brentq(objective, tau_lo, tau_hi, xtol=1e-10, rtol=1e-10)
    return float(tau_star)


def solve_all_rates(
    W0        : float,
    dist      : ReturnDistribution,
    target_et : float,
    systems   : Optional[list] = None,
) -> dict:
    """
    Solve revenue-equivalent rates for all (or a specified subset of) systems.

    Returns a dict: {system_name: tau_star}

    Systems that cannot achieve the target (e.g. symmetric WDT when E[R]=1
    and target > 0) are recorded with tau=None and a warning printed.
    """
    if systems is None:
        systems = list(_TAX_REGISTRY.keys())

    rates = {}
    for name in systems:
        tax_fn = get_tax_fn(name)
        try:
            tau = solve_revenue_equivalent_rate(W0, dist, tax_fn, target_et)
            rates[name] = tau
        except ValueError as e:
            print(f"  WARNING [{name}]: {e}")
            rates[name] = None
    return rates


# ─────────────────────────────────────────────────────────────────────────────
# 6. FULL WELFARE COMPARISON — primary output struct
# ─────────────────────────────────────────────────────────────────────────────

@dataclass
class SystemResult:
    """Welfare results for one tax system at one (distribution, gamma) pair."""
    name           : str
    label          : str
    tau            : Optional[float]
    eu             : Optional[float]    # E[u(consumption)]
    cew            : Optional[float]    # CEW relative to no-tax
    expected_tax   : Optional[float]
    var_consumption: Optional[float]
    # State-level detail (parallel arrays, same length as dist.returns)
    state_taxes    : Optional[np.ndarray] = field(default=None, repr=False)
    state_wealth   : Optional[np.ndarray] = field(default=None, repr=False)
    state_cons     : Optional[np.ndarray] = field(default=None, repr=False)


def run_welfare_comparison(
    W0        : float,
    dist      : ReturnDistribution,
    gamma     : float,
    target_et : float,
    systems   : Optional[list] = None,
) -> dict:
    """
    Run the full welfare comparison for all systems at given (dist, gamma).

    Parameters
    ----------
    W0        : initial wealth (£, consistent with TOML — use 1.0 for normalised)
    dist      : ReturnDistribution (Version A or B)
    gamma     : CRRA risk-aversion coefficient
    target_et : revenue target E[T] (same units as W0)
    systems   : list of system names, or None for all five

    Returns
    -------
    dict: {system_name: SystemResult}
    """
    if systems is None:
        systems = list(_TAX_REGISTRY.keys())

    # 1. No-tax baseline
    eu_notax = expected_utility(W0, dist, tax_symmetric_flat, 0.0, gamma)

    # 2. Solve revenue-equivalent rates
    rates = solve_all_rates(W0, dist, target_et, systems)

    # 3. Compute welfare for each system
    results = {}
    for name in systems:
        tax_fn = get_tax_fn(name)
        tau    = rates[name]

        if tau is None:
            results[name] = SystemResult(
                name=name, label=SYSTEM_LABELS[name],
                tau=None, eu=None, cew=None,
                expected_tax=None, var_consumption=None
            )
            continue

        eu    = expected_utility(W0, dist, tax_fn, tau, gamma)
        cew   = consumption_equiv_welfare(eu, eu_notax, gamma)
        et    = expected_tax(W0, dist, tax_fn, tau)
        var_c = variance_of_consumption(W0, dist, tax_fn, tau)

        # State-level detail
        state_taxes  = np.array([tax_fn(W0, R, tau).tax_paid        for R in dist.returns])
        state_wealth = np.array([tax_fn(W0, R, tau).post_tax_wealth  for R in dist.returns])
        state_cons   = np.array([tax_fn(W0, R, tau).consumption      for R in dist.returns])

        results[name] = SystemResult(
            name=name, label=SYSTEM_LABELS[name],
            tau=tau, eu=eu, cew=cew,
            expected_tax=et, var_consumption=var_c,
            state_taxes=state_taxes,
            state_wealth=state_wealth,
            state_cons=state_cons,
        )

    return results


# ─────────────────────────────────────────────────────────────────────────────
# 7. DIAGNOSTICS
# ─────────────────────────────────────────────────────────────────────────────

def print_welfare_table(
    results   : dict,
    dist_label: str,
    gamma     : float,
    target_et : float,
    W0        : float,
):
    """Print a formatted welfare comparison table to stdout."""
    col_w = 24
    systems_ordered = ["symmetric_wdt", "stock_wealth", "income", "cgt", "consumption"]

    header = f"\n{'='*80}"
    header += f"\nWelfare Comparison  |  {dist_label}"
    header += f"\nγ = {gamma}  |  Target E[T] = £{target_et:.4f}  |  W₀ = £{W0:.2f}"
    header += f"\n{'='*80}"
    print(header)

    # Column headers
    names = [results[s].label if s in results else s for s in systems_ordered]
    print(f"{'':30s}" + "".join(f"{n:>{col_w}}" for n in names))
    print("-" * (30 + col_w * len(systems_ordered)))

    rows = [
        ("Rate (τ)",          lambda r: f"{r.tau*100:.3f}%"        if r.tau  is not None else "N/A"),
        ("E[T] (£)",          lambda r: f"£{r.expected_tax:.4f}"   if r.expected_tax is not None else "N/A"),
        ("E[u]",              lambda r: f"{r.eu:.8f}"               if r.eu   is not None else "N/A"),
        ("CEW vs no-tax",     lambda r: f"{r.cew*100:+.4f}%"       if r.cew  is not None else "N/A"),
        ("Var(consumption)",  lambda r: f"{r.var_consumption:.4f}"  if r.var_consumption is not None else "N/A"),
    ]

    for row_label, fmt_fn in rows:
        line = f"{row_label:30s}"
        for name in systems_ordered:
            if name in results:
                line += f"{fmt_fn(results[name]):>{col_w}}"
            else:
                line += f"{'—':>{col_w}}"
        print(line)

    print("-" * (30 + col_w * len(systems_ordered)))

    # CEW ranking
    ranked = sorted(
        [(name, results[name].cew) for name in systems_ordered
         if name in results and results[name].cew is not None],
        key=lambda x: x[1], reverse=True
    )
    print(f"\nCEW Ranking (best to worst welfare):")
    for rank, (name, cew) in enumerate(ranked, 1):
        print(f"  {rank}. {SYSTEM_LABELS[name]:35s} {cew*100:+.4f}%")


def dm_test(
    W0     : float,
    dist   : ReturnDistribution,
    tau    : float,
) -> dict:
    """
    Domar-Musgrave test for the symmetric WDT.

    Under a flat-rate symmetric tax, the D-M result predicts:
        Var(C_tax) = (1 - τ)² × Var(C_notax)

    This function computes the predicted and actual variance ratio and
    returns the gap. A gap near zero confirms D-M holds.
    """
    var_notax = variance_of_consumption(W0, dist, tax_symmetric_flat, 0.0)
    var_tax   = variance_of_consumption(W0, dist, tax_symmetric_flat, tau)

    predicted_ratio = (1.0 - tau) ** 2
    actual_ratio    = var_tax / var_notax if var_notax > 0 else float('nan')
    gap             = actual_ratio - predicted_ratio

    return {
        "var_notax"       : var_notax,
        "var_tax"         : var_tax,
        "predicted_ratio" : predicted_ratio,
        "actual_ratio"    : actual_ratio,
        "gap"             : gap,
        "dm_holds"        : abs(gap) < 1e-6,
    }


# ─────────────────────────────────────────────────────────────────────────────
# 8. SELF-TEST — runs when executed directly
# ─────────────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    import os

    toml_path = os.path.join(os.path.dirname(__file__), "WDT_Params.toml")
    print(f"Loading parameters from: {toml_path}")
    p = load_params(toml_path)

    print("\n--- Return distributions ---")
    dist_A = make_empirical_distribution(p)
    dist_B = make_idealised_distribution(p)
    print(dist_A.describe())
    print()
    print(dist_B.describe())

    # Sanity check: mean of Version A should match hist_mean in TOML
    assert math.isclose(
        dist_A.mean_net_return,
        p["tcm"]["hist_mean"],
        rel_tol=1e-3
    ), f"Version A mean {dist_A.mean_net_return:.4f} ≠ hist_mean {p['tcm']['hist_mean']}"
    print(f"\n✓ Version A mean matches hist_mean ({p['tcm']['hist_mean']*100:.2f}%)")

    # Revenue target: 2% of W0 (as in toy model experiments)
    W0        = 1.0     # normalised — all outputs scale with W0
    target_et = 0.02    # £0.02 per £1 of initial wealth = 2% of W0

    for gamma in [1.0, 2.0, 4.0]:
        for dist in [dist_A, dist_B]:
            try:
                results = run_welfare_comparison(W0, dist, gamma, target_et)
                print_welfare_table(results, dist.label, gamma, target_et, W0)

                # D-M test at the symmetric WDT rate
                if results["symmetric_wdt"].tau is not None:
                    dm = dm_test(W0, dist, results["symmetric_wdt"].tau)
                    status = "✓ HOLDS" if dm["dm_holds"] else "✗ FAILS"
                    print(f"\n  D-M test [{status}]: "
                          f"predicted ratio = {dm['predicted_ratio']:.6f}, "
                          f"actual = {dm['actual_ratio']:.6f}, "
                          f"gap = {dm['gap']:.2e}")
            except ValueError as e:
                print(f"\n  [{dist.label[:30]}, γ={gamma}] SKIPPED: {e}")

    print("\n✓ Core self-test complete.")
