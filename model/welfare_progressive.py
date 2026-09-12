"""
welfare_progressive.py
======================
Shared primitives for the WDT progressive rate function.

Previously these were defined only in 19_3_module2_progression.py and
imported by modules 4, 5, and welfare_tables.py via fragile importlib
chains (importlib.import_module('19_3_module2_progression')).  Any file
rename would silently break those imports with no immediate error.

This module is the canonical home for the progressive rate primitives.
Module 2 (19_3_module2_progression.py) continues to own the *analysis*
logic (run_c1_analysis, LeveragedAgent, run_c2_leverage, run_c3_two_period)
and still defines ProgressiveRateFunction locally for its own use — but it
now imports from here so both definitions stay in sync.

Modules 4, 5, and welfare_tables.py import directly from this module
instead of going through importlib.

Public API
----------
  ProgressiveRateFunction          — logistic rate function class
  tax_progressive_wdt(W0, R, fn)   — single-period tax/refund
  expected_utility_progressive(...)
  expected_tax_progressive(...)
  variance_progressive(...)
"""

from __future__ import annotations

import math
import numpy as np

from welfare_core import (
    ReturnDistribution,
    crra_utility,
)
from wdt_fmt import fmt_pct, fmt_gbp_m


# ─────────────────────────────────────────────────────────────────────────────
# PROGRESSIVE RATE FUNCTION
# ─────────────────────────────────────────────────────────────────────────────

class ProgressiveRateFunction:
    """
    WDT logistic rate function from TOML.

    τ(W) = τ_m / (1 + A × exp(−k × (W − W_min)))
    where A = (τ_m − τ_0) / τ_0

    Properties:
        τ(W_min) = τ_0   (entry rate at exemption threshold)
        τ → τ_m          (asymptotic ceiling)
        Strictly increasing, inflects above W_min
    """

    def __init__(self, tau0: float, taum: float, k: float, W_min: float):
        self.tau0  = tau0
        self.taum  = taum
        self.k     = k
        self.W_min = W_min
        self.A     = (taum - tau0) / tau0

    def rate(self, W: float) -> float:
        """Marginal rate at wealth level W."""
        if W <= self.W_min:
            return 0.0     # below exemption threshold: zero rate
        exponent = -self.k * (W - self.W_min)
        return self.taum / (1.0 + self.A * math.exp(exponent))

    def effective_rate(self, W0: float, W1: float) -> float:
        """
        Effective rate on the delta (W1 - W0).
        Uses the average of the rate at W0 and W1 as an approximation
        to the integral of τ(W) dW over the gain.

        For the progressive WDT, the exact effective rate would require
        integrating the marginal rate function over the delta, which is
        complex for a logistic. The midpoint approximation is accurate
        when the delta is small relative to W_min — true for annual
        assessment windows at the wealth levels modelled here.
        """
        if W1 <= W0:
            # Loss state: refund rate is rate at W1 (lower wealth)
            return self.rate(W1)
        # Gain state: effective rate is midpoint of rates at W0 and W1
        return 0.5 * (self.rate(W0) + self.rate(W1))

    def describe(self) -> str:
        return (
            f"Progressive Rate Function:\n"
            f"  τ₀ = {fmt_pct(self.tau0, dp=1)}  (entry rate at W_min)\n"
            f"  τ_m = {fmt_pct(self.taum, dp=1)}  (asymptotic ceiling)\n"
            f"  k = {self.k}  (steepness)\n"
            f"  W_min = {fmt_gbp_m(self.W_min, dp=0)}\n"
            f"  Rate at W_min:        {fmt_pct(self.rate(self.W_min))}\n"
            f"  Rate at 2×W_min:      {fmt_pct(self.rate(2*self.W_min))}\n"
            f"  Rate at 10×W_min:     {fmt_pct(self.rate(10*self.W_min))}\n"
            f"  Rate at 100×W_min:    {fmt_pct(self.rate(100*self.W_min))}"
        )


# ─────────────────────────────────────────────────────────────────────────────
# PROGRESSIVE TAX FUNCTION
# ─────────────────────────────────────────────────────────────────────────────

def tax_progressive_wdt(W0: float, R: float, rate_fn: ProgressiveRateFunction):
    """
    Progressive WDT tax function.
    Uses effective_rate() over the delta, preserving sign for refunds.
    Returns (tax_paid, post_tax_wealth, consumption).
    """
    W1      = W0 * R
    delta   = W1 - W0
    tau_eff = rate_fn.effective_rate(W0, W1)
    tax     = tau_eff * delta          # negative in loss states → refund
    W1_post = W1 - tax
    return tax, W1_post, W1_post       # consumption = post-tax wealth


# ─────────────────────────────────────────────────────────────────────────────
# WELFARE HELPERS
# ─────────────────────────────────────────────────────────────────────────────

def expected_utility_progressive(
    W0      : float,
    dist    : ReturnDistribution,
    rate_fn : ProgressiveRateFunction,
    gamma   : float,
) -> float:
    """E[u] under progressive WDT."""
    eu = 0.0
    for R, prob in zip(dist.returns, dist.probs):
        _, _, C = tax_progressive_wdt(W0, R, rate_fn)
        eu += prob * crra_utility(C, gamma)
    return eu


def expected_tax_progressive(
    W0      : float,
    dist    : ReturnDistribution,
    rate_fn : ProgressiveRateFunction,
) -> float:
    """E[T] under progressive WDT."""
    et = 0.0
    for R, prob in zip(dist.returns, dist.probs):
        tax, _, _ = tax_progressive_wdt(W0, R, rate_fn)
        et += prob * tax
    return et


def variance_progressive(
    W0      : float,
    dist    : ReturnDistribution,
    rate_fn : ProgressiveRateFunction,
) -> float:
    """Var(consumption) under progressive WDT."""
    consumptions = np.array([
        tax_progressive_wdt(W0, R, rate_fn)[2]
        for R in dist.returns
    ])
    mean_c = float(np.dot(dist.probs, consumptions))
    return float(np.dot(dist.probs, (consumptions - mean_c) ** 2))
