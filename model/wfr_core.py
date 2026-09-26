"""
wfr_core.py
===========
WFR Welfare Comparison Model — Computation Engine

Runs all five welfare modules and writes a single structured JSON file
(wfr_results.json) that fully describes every result.  wfr_tables.py and
wfr_charts.py are stateless readers of that file; neither module re-runs
any computation.

Replaces
--------
  19_2_module1_baseline.py   (all computation)
  19_3_module2_progression.py
  19_4_module3_lockin.py
  19_5_module4_heterogeneous.py
  19_6_module5_sweeps.py
  welfare_tables.py           (computation path only)
  welfare_core.py             (imported, not replaced)

Usage
-----
  python wfr_core.py                         # run everything
  python wfr_core.py --modules 1 2 3        # run specific modules
  python wfr_core.py --out my_results.json  # custom output path

The output JSON is self-describing: every key carries enough context (units,
parameters, labels) that a reader does not need to consult the source code.

JSON schema summary
-------------------
{
  "meta": { version, date, params_summary },

  "module1": {
    "distributions": {
      "<dist_label>": {
        "label": str,
        "n_states": int, "mean_net_return": float, "std_return": float,
        "returns": [...], "probs": [...],
        "welfare": {
          "<gamma>": {
            "<system>": {
              "tau": float|null, "eu": float|null, "cew": float|null,
              "expected_tax": float|null, "var_consumption": float|null,
              "state_taxes": [...], "state_wealth": [...], "state_cons": [...]
            }
          }
        },
        "dm_test": {
          "<gamma>": { var_notax, var_tax, predicted_ratio, actual_ratio, gap, dm_holds }
        }
      }
    }
  },

  "module2": {
    "rate_fn": { tau0, taum, k, W_min },
    "c1": { "<dist_label>": { "<gamma>": { ...c1 result... } } },
    "c2_leverage": [ { leverage_ratio, W0, et_nw, et_ar, cew_nw, cew_ar, ... } ],
    "c3_asymmetry": { "W0_vals": [...], "results": [ { ...c3 result... } ] }
  },

  "module3": {
    "asset_ref": { V, B, G, gain_ratio, tau_cgt, T, r_A, r_B_indiff, switch_cost },
    "sens_gain": [ { gain_ratio, cew_free, cew_locked, lock_in_cost_bp, p_locked, ... } ],
    "sens_T":    [ { T, r_B_indiff, lock_in_cost_bp, p_locked, ... } ],
    "full_comparison": {
      "<dist_label>": { wdt_cew, cgt_cew, cgt_with_lock_cew, lock_in_cost_bp, ... }
    }
  },

  "module4": {
    "tiers": [ { name, differential, pop_share, W0, bracket_label } ],
    "tier_welfare": {
      "<tier_name>": {
        "systems": { "<system>": { tau, eu, cew, expected_tax, var_consumption, et_pct_W0 } },
        "cew_progressive": float, "et_progressive": float
      }
    },
    "concentration": {
      "scenario": {
        "years": [...], "systems": {
          "<system>": { "<tier>": [wealth_path...] }
        }
      },
      "extended": {
        "years": [...], "systems": { "<system>": { "<tier>": [...] } },
        "crossover": { year, ratio_flat, ratio_prog, gap } | null
      }
    },
    "envelope": {
      "<tier>": { ever_binds, binding_years, min_slack, cum_tax_final, cum_ref_final, year_log }
    },
    "corner_check": {
      "corner_A": { label, W0, differential, systems: {...}, cew_progressive, et_progressive },
      "corner_B": { ... }
    }
  },

  "module5": {
    "sweep_a_revenue": { "<pct>": { "<dist>": { "<gamma>": { "<system>": cew } } } },
    "sweep_a_w0":      { "<W0>": { "<system>": cew } },
    "sweep_b_start_year": { "<year>": { "<system>": cew } },
    "sweep_c_params": {
      "<param_name>": { "<W0>": { "<param_val>": gap_bp } }
    }
  }
}
"""

from __future__ import annotations

import argparse
import json
import math
import sys
import numpy as np
from datetime import date
from pathlib import Path
from dataclasses import dataclass
from typing import Optional
from scipy.optimize import brentq

# ── project imports ───────────────────────────────────────────────────────────
from welfare_core import (
    load_params, TOML_PATH,
    ReturnDistribution,
    make_empirical_distribution_scenario,
    make_idealised_distribution_scenario,
    make_empirical_distribution_for_start,
    make_scenario_sequence,
    run_welfare_comparison,
    consumption_equiv_welfare,
    expected_utility,
    expected_tax,
    variance_of_consumption,
    solve_revenue_equivalent_rate,
    get_tax_fn,
    tax_symmetric_flat,
    dm_test,
    crra_utility,
    SYSTEM_LABELS,
    ProgressiveRateFunction,
    tax_progressive_wdt,
    expected_utility_progressive,
    expected_tax_progressive,
    module_output_dir,
)

# ─────────────────────────────────────────────────────────────────────────────
# CONSTANTS
# ─────────────────────────────────────────────────────────────────────────────

W0_NORM   = 1.0    # Module 1 normalised wealth
TARGET_ET = 0.02   # 2 % of W0 canonical revenue target
GAMMA_VALS = [1.0, 2.0, 4.0]
GAMMA_CEN  = 2.0
SYSTEMS    = ["symmetric_wdt", "stock_wealth", "income", "cgt", "consumption"]

OUTPUT_ROOT = module_output_dir("wfr")   # creates .../OUTPUTS/WFR/wfr/


# ─────────────────────────────────────────────────────────────────────────────
# HELPERS
# ─────────────────────────────────────────────────────────────────────────────

def _f(v):
    """Scalar float → python float or None; numpy arrays rejected here."""
    if v is None:
        return None
    if isinstance(v, float) and math.isnan(v):
        return None
    return float(v)

def _arr(v):
    """ndarray or list → plain python list of floats."""
    if v is None:
        return None
    return [float(x) for x in v]

def _dist_summary(dist: ReturnDistribution) -> dict:
    return {
        "label": dist.label,
        "n_states": int(dist.n_states),
        "mean_net_return": _f(dist.mean_net_return),
        "std_return": _f(dist.std_return),
        "returns": _arr(dist.returns),
        "probs": _arr(dist.probs),
    }


# ─────────────────────────────────────────────────────────────────────────────
# PROGRESSIVE RATE FUNCTION HELPERS
# ─────────────────────────────────────────────────────────────────────────────

def build_rate_fn(p: dict) -> ProgressiveRateFunction:
    rp = p["rate"]
    return ProgressiveRateFunction(
        tau0=rp["tau_0"], taum=rp["tau_m"],
        k=rp["k"], W_min=rp["W_min"],
    )


class ScaledRateFn(ProgressiveRateFunction):
    """Uniform scale applied to every effective_rate / rate call."""
    def __init__(self, base: ProgressiveRateFunction, scale: float):
        super().__init__(base.tau0, base.taum, base.k, base.W_min)
        self.scale = scale

    def effective_rate(self, W0: float, W1: float) -> float:
        return self.scale * super().effective_rate(W0, W1)

    def rate(self, W: float) -> float:
        return self.scale * super().rate(W)


def _solve_progressive_scale(
    W0: float,
    dist: ReturnDistribution,
    rate_fn: ProgressiveRateFunction,
    target_et: float,
) -> Optional[float]:
    def _et(s):
        scaled = ScaledRateFn(rate_fn, s)
        return expected_tax_progressive(W0, dist, scaled) - target_et
    try:
        lo, hi = _et(1e-4), _et(50.0)
    except Exception:
        return None
    if lo * hi > 0:
        return None
    return float(brentq(_et, 1e-4, 50.0, xtol=1e-10, rtol=1e-10))


# ─────────────────────────────────────────────────────────────────────────────
# MODULE 1 — Baseline welfare comparison
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

    out = {"distributions": {}}

    for dist in [dist_A, dist_B]:
        dk = dist.label
        entry = _dist_summary(dist)
        entry["welfare"] = {}
        entry["dm_test"] = {}

        for gamma in GAMMA_VALS:
            print(f"  {dk[:40]}  γ={gamma}")
            results = run_welfare_comparison(
                W0=W0_NORM, dist=dist, gamma=gamma,
                target_et=TARGET_ET,
            )
            entry["welfare"][str(gamma)] = {
                name: _welfare_result_to_dict(r)
                for name, r in results.items()
            }
            # D-M test at flat WDT rate
            tau_wdt = results.get("symmetric_wdt", None)
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
# MODULE 2 — Progressive rates and D-M complications
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


def _run_c1(W0, dist, rate_fn, gamma, target_et) -> dict:
    """C1: flat WDT vs progressive WDT at revenue-equivalent rates."""
    flat_fn  = get_tax_fn("symmetric_wdt")
    eu_notax = expected_utility(W0, dist, flat_fn, 0.0, gamma)

    et_prog  = expected_tax_progressive(W0, dist, rate_fn)
    eu_prog  = expected_utility_progressive(W0, dist, rate_fn, gamma)
    cew_prog = consumption_equiv_welfare(eu_prog, eu_notax, gamma)
    var_prog = variance_of_consumption.__wrapped__(W0, dist, rate_fn) if hasattr(
        variance_of_consumption, '__wrapped__') else _var_progressive(W0, dist, rate_fn)

    # Flat WDT revenue-matched to et_prog (not to global 2% target)
    revenue_matched = True
    flat_target = et_prog if et_prog > 0 else target_et
    if et_prog <= 0:
        revenue_matched = False

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
        "tau_flat":         _f(tau_flat),
        "et_flat":          _f(et_flat),
        "et_flat_target":   _f(target_et),
        "eu_flat":          _f(eu_flat),
        "cew_flat":         _f(cew_flat),
        "var_flat":         _f(var_flat),
        "et_progressive":   _f(et_prog),
        "eu_progressive":   _f(eu_prog),
        "cew_progressive":  _f(cew_prog),
        "cew_gap_bp":       _f((cew_flat - cew_prog) * 10000) if (cew_flat is not None and cew_prog is not None) else None,
        "revenue_matched":  revenue_matched,
    }


def _var_progressive(W0, dist, rate_fn):
    consumptions = np.array([
        tax_progressive_wdt(W0, R, rate_fn)[2] for R in dist.returns
    ])
    mean_c = float(np.dot(dist.probs, consumptions))
    return float(np.dot(dist.probs, (consumptions - mean_c) ** 2))


def _run_c2_leverage(agent: LeveragedAgent, dist: ReturnDistribution,
                     rate_fn: ProgressiveRateFunction, gamma: float) -> dict:
    W0 = agent.net_worth
    states = []
    for R, prob in zip(dist.returns, dist.probs):
        W1 = agent.net_worth_after_return(R)
        delta_W = W1 - W0
        delta_A = agent.gross_assets * (R - 1.0)

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

    eu_nw  = sum(s["prob"] * crra_utility(s["C_nw"], gamma) for s in states)
    eu_ar  = sum(s["prob"] * crra_utility(s["C_ar"], gamma) for s in states)
    et_nw  = sum(s["prob"] * s["tax_nw"] for s in states)
    et_ar  = sum(s["prob"] * s["tax_ar"] for s in states)
    eu_notax = sum(
        prob * crra_utility(max(agent.net_worth_after_return(R), 1e-9), gamma)
        for R, prob in zip(dist.returns, dist.probs)
    )
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
    W1 = W0 * R1_good
    tau1_prog = rate_fn.effective_rate(W0, W1)
    tax1_prog = tau1_prog * (W1 - W0)
    W1p = W1 - tax1_prog

    W1f = W1 - tau_flat * (W1 - W0)
    W2p = W1p * R2_bad
    W2f = W1f * R2_bad

    delta2p = W2p - W1p
    delta2f = W2f - W1f
    tau2_prog = rate_fn.effective_rate(W1p, W2p)
    refund_prog = tau2_prog * delta2p
    refund_flat = tau_flat  * delta2f

    C_prog = W2p - refund_prog
    C_flat = W2f - refund_flat

    return {
        "W0":               _f(W0),
        "W1":               _f(W1),
        "tau1_progressive": _f(tau1_prog),
        "tax1_progressive": _f(tax1_prog),
        "tax1_flat":        _f(tau_flat * (W1 - W0)),
        "W1_post_prog":     _f(W1p),
        "W1_post_flat":     _f(W1f),
        "W2_prog":          _f(W2p),
        "W2_flat":          _f(W2f),
        "tau2_progressive": _f(tau2_prog),
        "refund_prog":      _f(refund_prog),
        "refund_flat":      _f(refund_flat),
        "C_prog":           _f(C_prog),
        "C_flat":           _f(C_flat),
        "net_tax_prog":     _f(tax1_prog + refund_prog),
        "net_tax_flat":     _f(tau_flat * (W1 - W0) + refund_flat),
        "net_tax_excess":   _f((tax1_prog + refund_prog) - (tau_flat * (W1 - W0) + refund_flat)),
        "rate_asymmetry":   _f(tau1_prog - tau2_prog),
    }


def run_module2(p: dict) -> dict:
    print("\n=== Module 2: Progressive Rates and D-M Complications ===")
    N      = p["tcm"]["canonical_N"]
    dist_A = make_empirical_distribution_scenario(p, N)
    dist_B = make_idealised_distribution_scenario(p, N)
    rate_fn = build_rate_fn(p)
    rp      = p["rate"]

    out = {
        "rate_fn": {
            "tau0": _f(rate_fn.tau0), "taum": _f(rate_fn.taum),
            "k": _f(rate_fn.k), "W_min": _f(rate_fn.W_min),
        }
    }

    # C1 — flat vs progressive
    print("  C1: flat vs progressive...")
    W0_c1 = rp["W_min"] * 5
    c1 = {}
    for dist in [dist_A, dist_B]:
        c1[dist.label] = {}
        for gamma in GAMMA_VALS:
            c1[dist.label][str(gamma)] = _run_c1(
                W0_c1, dist, rate_fn, gamma, TARGET_ET * W0_c1
            )
    out["c1"] = c1

    # C2 — leverage
    print("  C2: leverage sweep...")
    gross_assets = rp["W_min"] * 5
    lev_grid = np.linspace(0.0, 0.70, 15)
    out["c2_leverage"] = [
        _run_c2_leverage(
            LeveragedAgent(gross_assets=gross_assets, debt=gross_assets * lev),
            dist_A, rate_fn, gamma=GAMMA_CEN
        )
        for lev in lev_grid
    ]

    # C3 — two-period asymmetry
    print("  C3: two-period asymmetry...")
    mu    = p["tcm"]["hist_mean"]
    sigma = float(np.std(p["returns"]["array"], ddof=0))
    R1    = 1.0 + mu + sigma
    R2    = 1.0 - sigma
    W0_c1_ref = rp["W_min"] * 5

    flat_fn  = get_tax_fn("symmetric_wdt")
    try:
        tau_flat = solve_revenue_equivalent_rate(W0_c1_ref, dist_A, flat_fn, TARGET_ET * W0_c1_ref)
    except ValueError:
        tau_flat = 0.02

    W0_vals = [rp["W_min"] * m for m in [1.5, 2, 5, 10, 20, 50, 100]]
    out["c3_asymmetry"] = {
        "W0_vals": W0_vals,
        "R1_good": _f(R1),
        "R2_bad":  _f(R2),
        "tau_flat_ref": _f(tau_flat),
        "results": [
            _run_c3_two_period(W0, R1, R2, rate_fn, GAMMA_CEN, tau_flat)
            for W0 in W0_vals
        ],
    }

    return out


# ─────────────────────────────────────────────────────────────────────────────
# MODULE 3 — CGT lock-in distortion
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
        npv_stay   = self.V * ((1 + self.r_A) ** self.T)
        switch_val = self.V - self.switch_cost_pv()
        return npv_stay - switch_val * ((1 + r_B_grid) ** self.T)


def _compute_lockin_cost(asset: AssetSwitchDecision,
                         dist: ReturnDistribution, gamma: float) -> dict:
    r_B_indiff = asset.indifference_return()
    states = []
    for R, prob in zip(dist.returns, dist.probs):
        r_B = R - 1.0
        C_free = asset.V * (1.0 + r_B) if r_B > asset.r_A else asset.V * (1.0 + asset.r_A)
        if r_B >= r_B_indiff:
            after_tax = asset.V - asset.switch_cost_pv()
            C_locked  = after_tax * (1.0 + r_B)
        else:
            C_locked = asset.V * (1.0 + asset.r_A)
        C_free   = max(C_free,   1e-9)
        C_locked = max(C_locked, 1e-9)
        states.append({
            "R": _f(R), "prob": _f(prob), "r_B": _f(r_B),
            "C_free": _f(C_free), "C_locked": _f(C_locked),
            "locked_in": bool(r_B < r_B_indiff),
        })

    eu_free   = sum(s["prob"] * crra_utility(s["C_free"],   gamma) for s in states)
    eu_locked = sum(s["prob"] * crra_utility(s["C_locked"], gamma) for s in states)
    eu_notax  = sum(
        s["prob"] * crra_utility(max(asset.V * s["R"], 1e-9), gamma)
        for s in states
    )
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
    m1 = run_welfare_comparison(W0, dist, gamma, target_et)
    wdt_cew = m1["symmetric_wdt"].cew
    cgt_cew = m1["cgt"].cew

    lock = _compute_lockin_cost(asset, dist, gamma)
    lock_bp = lock["lock_in_cost_bp"]
    cgt_with_lock_cew = cgt_cew - lock_bp / 10000

    return {
        "wdt_cew":              _f(wdt_cew),
        "cgt_cew":              _f(cgt_cew),
        "lock_in_cost_bp":      lock_bp,
        "cgt_with_lock_cew":    _f(cgt_with_lock_cew),
        "wdt_adv_no_lock_bp":   _f((wdt_cew - cgt_cew) * 10000),
        "wdt_adv_with_lock_bp": _f((wdt_cew - cgt_with_lock_cew) * 10000),
        "p_locked":             lock["p_locked"],
        "p_locked_cgt":         lock["p_locked_cgt"],
        "p_below_rA":           lock["p_below_rA"],
        "r_B_indiff":           lock["r_B_indiff"],
        "m1_cgt_tau":           _f(m1["cgt"].tau),
        "m1_wdt_tau":           _f(m1["symmetric_wdt"].tau),
    }


def run_module3(p: dict) -> dict:
    print("\n=== Module 3: CGT Lock-In ===")
    N      = p["tcm"]["canonical_N"]
    dist_A = make_empirical_distribution_scenario(p, N)
    dist_B = make_idealised_distribution_scenario(p, N)

    tau_cgt = 0.24
    V_ref   = 10.0
    G_ref   = V_ref * 0.50
    r_A     = p["tcm"]["hist_mean"]

    asset_ref = AssetSwitchDecision(V=V_ref, B=V_ref - G_ref, tau_cgt=tau_cgt, T=5, r_A=r_A)

    # Lock-in threshold curve data
    r_B_grid = np.linspace(r_A * 0.5, r_A * 2.5, 300)
    threshold_curve = {
        "r_B_grid": _arr(r_B_grid),
        "npv_diff": _arr(asset_ref.value_of_stay(r_B_grid)),
        "r_B_indiff": _f(asset_ref.indifference_return()),
    }

    # Sensitivity: gain ratio
    print("  Sensitivity: gain ratio sweep...")
    gain_ratios = np.linspace(0.05, 0.90, 20)
    sens_gain = []
    for gr in gain_ratios:
        G = V_ref * gr
        a = AssetSwitchDecision(V=V_ref, B=V_ref - G, tau_cgt=tau_cgt, T=5, r_A=r_A)
        r = _compute_lockin_cost(a, dist_A, GAMMA_CEN)
        r["gain_ratio"] = _f(gr)
        sens_gain.append(r)

    # Sensitivity: holding period
    print("  Sensitivity: holding period sweep...")
    T_vals = list(range(1, 21))
    sens_T = []
    for T in T_vals:
        a = AssetSwitchDecision(V=V_ref, B=V_ref - G_ref, tau_cgt=tau_cgt, T=T, r_A=r_A)
        r = _compute_lockin_cost(a, dist_A, GAMMA_CEN)
        r["T"] = T
        sens_T.append(r)

    # Full comparison
    print("  Full welfare comparison...")
    full = {}
    for dist in [dist_A, dist_B]:
        full[dist.label] = _full_lockin_comparison(
            10.0, dist, GAMMA_CEN, TARGET_ET * 10.0, asset_ref
        )

    return {
        "asset_ref": {
            "V": _f(V_ref), "B": _f(V_ref - G_ref), "G": _f(G_ref),
            "gain_ratio": _f(asset_ref.gain_ratio),
            "tau_cgt": _f(tau_cgt), "T": int(asset_ref.T), "r_A": _f(r_A),
            "r_B_indiff": _f(asset_ref.indifference_return()),
            "switch_cost": _f(asset_ref.switch_cost_pv()),
        },
        "threshold_curve": threshold_curve,
        "sens_gain": sens_gain,
        "sens_T":    sens_T,
        "full_comparison": full,
    }


# ─────────────────────────────────────────────────────────────────────────────
# MODULE 4 — Heterogeneous agents
# ─────────────────────────────────────────────────────────────────────────────

@dataclass
class AgentTier:
    name: str; differential: float; pop_share: float
    W0: float; bracket_label: str = ""

    def shifted_distribution(self, base_dist: ReturnDistribution) -> ReturnDistribution:
        shifted = np.maximum(base_dist.returns + self.differential, 0.01)
        return ReturnDistribution(
            returns=shifted, probs=base_dist.probs.copy(),
            label=f"{base_dist.label[:30]} | {self.name} tier (+{self.differential*100:.2f}pp)"
        )


def _build_tiers(p: dict) -> list:
    bracket_map = {b["label"]: b["V0_m"] for b in p["brackets"]}
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
    tax_fn = get_tax_fn(tax_fn_name)
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
    agg_W0 = sum(t.pop_share * t.W0 for t in tiers)
    agg_target = TARGET_ET * agg_W0

    agg_taus = {}
    for name in SYSTEMS:
        tau = _solve_aggregate_rate(tiers, base_dist, name, agg_target)
        agg_taus[name] = tau

    shifted = {t.name: t.shifted_distribution(base_dist) for t in tiers}

    tier_results = {}
    for tier in tiers:
        dist_t   = shifted[tier.name]
        eu_notax = expected_utility(tier.W0, dist_t, tax_symmetric_flat, 0.0, gamma)
        sys_results = {}

        for name in SYSTEMS:
            tau = agg_taus[name]
            if tau is None:
                sys_results[name] = {
                    "tau": None, "eu": None, "cew": None,
                    "expected_tax": None, "var_consumption": None, "et_pct_W0": None,
                }
                continue
            tax_fn = get_tax_fn(name)
            eu     = expected_utility(tier.W0, dist_t, tax_fn, tau, gamma)
            cew    = consumption_equiv_welfare(eu, eu_notax, gamma)
            et     = expected_tax(tier.W0, dist_t, tax_fn, tau)
            var_c  = variance_of_consumption(tier.W0, dist_t, tax_fn, tau)
            sys_results[name] = {
                "tau": _f(tau), "eu": _f(eu), "cew": _f(cew),
                "expected_tax": _f(et), "var_consumption": _f(var_c),
                "et_pct_W0": _f(et / tier.W0 * 100),
            }

        eu_prog  = expected_utility_progressive(tier.W0, dist_t, rate_fn, gamma)
        cew_prog = consumption_equiv_welfare(eu_prog, eu_notax, gamma)
        et_prog  = expected_tax_progressive(tier.W0, dist_t, rate_fn)

        tier_results[tier.name] = {
            "systems":          sys_results,
            "cew_progressive":  _f(cew_prog),
            "et_progressive":   _f(et_prog),
            "agg_taus":         {k: _f(v) for k, v in agg_taus.items()},
        }

    return tier_results


def _project_wealth_path(W0, returns_seq, tax_fn, tau) -> list:
    W = W0
    path = [W]
    for R in returns_seq:
        result = tax_fn(W, R, tau)
        W = max(result.post_tax_wealth, 0.001)
        path.append(W)
    return [_f(x) for x in path]


def _project_progressive_path(W0, returns_seq, rate_fn) -> list:
    W = W0
    path = [W]
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
                tax_fn = get_tax_fn(name)
                paths[name][tier.name] = _project_wealth_path(
                    tier.W0, gross, tax_fn, precomputed_taus[name]
                )

    return paths, [int(y) for y in years]


def _run_concentration_extended(tiers, p, rate_fn, systems, precomputed_taus) -> tuple:
    returns_seq = p["returns"]["array"]
    years = p["returns"]["years"]
    paths = {name: {} for name in systems}

    for tier in tiers:
        gross = np.maximum(1.0 + returns_seq + tier.differential, 0.01)
        for name in systems:
            if name == "progressive_wdt":
                paths[name][tier.name] = _project_progressive_path(tier.W0, gross, rate_fn)
            elif precomputed_taus.get(name) is None:
                paths[name][tier.name] = [None] * (len(returns_seq) + 1)
            else:
                tax_fn = get_tax_fn(name)
                paths[name][tier.name] = _project_wealth_path(
                    tier.W0, gross, tax_fn, precomputed_taus[name]
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
        gap = (gp / pp) - (gf / pf)
        if gap < -threshold:
            year = start_year - 1 if idx == 0 else start_year + idx - 1
            return {"year": int(year), "ratio_flat": _f(gf / pf),
                    "ratio_prog": _f(gp / pp), "gap": _f(gap)}
    return None


def _test_envelope_binding(tiers, p, rate_fn, N) -> dict:
    returns_seq, years = make_scenario_sequence(p, N)
    results = {}
    for tier in tiers:
        gross = np.maximum(1.0 + returns_seq + tier.differential, 0.01)
        W = tier.W0; cum_tax = 0.0; cum_ref = 0.0
        year_log = []; binding_years = []

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
            "ever_binds":     len(binding_years) > 0,
            "binding_years":  binding_years,
            "min_slack":      _f(min(y["envelope_slack"] for y in year_log)),
            "cum_tax_final":  _f(cum_tax),
            "cum_ref_final":  _f(cum_ref),
            "W_final":        _f(W),
            "year_log":       year_log,
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
                tau = solve_revenue_equivalent_rate(W0, dist_c, tax_fn, target_et)
                eu  = expected_utility(W0, dist_c, tax_fn, tau, gamma)
                cew = consumption_equiv_welfare(eu, eu_notax, gamma)
                et  = expected_tax(W0, dist_c, tax_fn, tau)
                var_c = variance_of_consumption(W0, dist_c, tax_fn, tau)
                sys_res[name] = {"tau": _f(tau), "eu": _f(eu), "cew": _f(cew),
                                  "expected_tax": _f(et), "var_consumption": _f(var_c)}
            except ValueError:
                sys_res[name] = {"tau": None, "eu": None, "cew": None,
                                  "expected_tax": None, "var_consumption": None}

        eu_prog  = expected_utility_progressive(W0, dist_c, rate_fn, gamma)
        cew_prog = consumption_equiv_welfare(eu_prog, eu_notax, gamma)
        et_prog  = expected_tax_progressive(W0, dist_c, rate_fn)

        out[key] = {
            "label": label, "W0": _f(W0), "differential": _f(diff),
            "bracket_label": bracket,
            "systems": sys_res,
            "cew_progressive": _f(cew_prog), "et_progressive": _f(et_prog),
        }
    return out


def run_module4(p: dict) -> dict:
    print("\n=== Module 4: Heterogeneous Agents ===")
    N      = p["tcm"]["canonical_N"]
    dist_A = make_empirical_distribution_scenario(p, N)
    rate_fn = build_rate_fn(p)
    tiers   = _build_tiers(p)

    tiers_out = [
        {"name": t.name, "differential": _f(t.differential),
         "pop_share": _f(t.pop_share), "W0": _f(t.W0),
         "bracket_label": t.bracket_label}
        for t in tiers
    ]

    print("  Tier welfare comparison...")
    tier_welfare = _run_tier_comparison(tiers, dist_A, GAMMA_CEN, rate_fn)

    # Extract aggregate taus from Good tier (all tiers share same tau)
    agg_taus = {
        name: tier_welfare["Good"]["agg_taus"].get(name)
        for name in SYSTEMS
        if tier_welfare["Good"]["agg_taus"].get(name) is not None
    }

    systems_proj = ["symmetric_wdt", "progressive_wdt", "stock_wealth", "income", "consumption"]

    print("  Concentration analysis (scenario, N=30)...")
    conc_paths, conc_years = _run_concentration(tiers, p, rate_fn, systems_proj, agg_taus, N)

    print("  Concentration analysis (extended, N=73)...")
    ext_paths, ext_years = _run_concentration_extended(tiers, p, rate_fn, systems_proj, agg_taus)
    crossover = _find_progressive_crossover_from_paths(ext_paths, ext_years[0])

    print("  Envelope binding test...")
    envelope = _test_envelope_binding(tiers, p, rate_fn, N)

    print("  Corner check (off-diagonal)...")
    corners = _run_corner_check(tiers, dist_A, GAMMA_CEN, rate_fn)

    return {
        "tiers": tiers_out,
        "tier_welfare": tier_welfare,
        "concentration": {
            "scenario": {
                "years": conc_years,
                "systems": conc_paths,
            },
            "extended": {
                "years": ext_years,
                "systems": ext_paths,
                "crossover": crossover,
            },
        },
        "envelope": envelope,
        "corner_check": corners,
    }


def _find_progressive_crossover_from_paths(paths, start_year, threshold=1.0):
    return _find_crossover(paths, start_year, threshold)


# ─────────────────────────────────────────────────────────────────────────────
# MODULE 5 — Welfare sweep analysis
# ─────────────────────────────────────────────────────────────────────────────

def _run_sweep_a_revenue(p: dict) -> dict:
    """Sweep E[T] as % of W0 from 1 to 5%."""
    print("  Sweep A: revenue target...")
    sw     = p["sweep"]
    target_pcts = sw["wfr_target_et_pct"]
    gamma_vals  = sw["wfr_gamma_vals"]
    N = p["tcm"]["canonical_N"]
    dist_A = make_empirical_distribution_scenario(p, N)
    dist_B = make_idealised_distribution_scenario(p, N)
    dists  = {"A": dist_A, "B": dist_B}

    out = {}
    for pct in target_pcts:
        target_et = (pct / 100.0) * W0_NORM
        out[str(pct)] = {}
        for dlabel, dist in dists.items():
            out[str(pct)][dlabel] = {}
            for gamma in gamma_vals:
                comp = run_welfare_comparison(W0_NORM, dist, gamma, target_et)
                out[str(pct)][dlabel][str(gamma)] = {
                    name: _f(r.cew) for name, r in comp.items()
                }
    return out


def _run_sweep_a_w0(p: dict) -> dict:
    """Sweep W0 across wealth-tier range at 2% target."""
    print("  Sweep A: W0 sensitivity...")
    N      = p["tcm"]["canonical_N"]
    dist_A = make_empirical_distribution_scenario(p, N)
    W0_vals = p["sweep"]["wfr_W0_sweep"]
    out = {}
    for W0 in W0_vals:
        target_et = 0.02 * W0
        try:
            comp = run_welfare_comparison(W0, dist_A, GAMMA_CEN, target_et)
            out[str(W0)] = {name: _f(r.cew) for name, r in comp.items()}
        except ValueError:
            out[str(W0)] = {name: None for name in SYSTEMS}
    return out


def _run_sweep_b_start_year(p: dict) -> dict:
    """Full start-year sweep over all 73 windows."""
    print("  Sweep B: start-year sweep (73 windows)...")
    N        = p["tcm"]["canonical_N"]
    base_yr  = p["returns"]["series_base_year"]
    all_yrs  = list(range(base_yr, base_yr + 73))
    target_et = 0.02 * W0_NORM
    out = {}
    for start_yr in all_yrs:
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
    """Single-parameter sweeps for progressive-vs-flat gap."""
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
                kwargs = dict(tau0=rp["tau_0"], taum=rp["tau_m"],
                              k=rp["k"], W_min=rp["W_min"])
                if param_name == "tau_0":
                    kwargs["tau0"] = pval
                elif param_name == "tau_m":
                    kwargs["taum"] = pval
                elif param_name == "k":
                    kwargs["k"] = pval
                elif param_name == "W_min":
                    kwargs["W_min"] = pval

                if kwargs["tau0"] >= kwargs["taum"]:
                    out[param_name][str(W0)][str(pval)] = None
                    continue

                rate_fn = ProgressiveRateFunction(**kwargs)
                target_et = 0.02 * W0
                scale = _solve_progressive_scale(W0, dist_A, rate_fn, target_et)
                if scale is None:
                    out[param_name][str(W0)][str(pval)] = None
                    continue

                scaled_fn  = ScaledRateFn(rate_fn, scale)
                flat_fn    = get_tax_fn("symmetric_wdt")
                eu_notax   = expected_utility(W0, dist_A, flat_fn, 0.0, GAMMA_CEN)
                eu_prog    = expected_utility_progressive(W0, dist_A, scaled_fn, GAMMA_CEN)
                cew_prog   = consumption_equiv_welfare(eu_prog, eu_notax, GAMMA_CEN)
                tau_flat   = solve_revenue_equivalent_rate(W0, dist_A, flat_fn, target_et)
                eu_flat    = expected_utility(W0, dist_A, flat_fn, tau_flat, GAMMA_CEN)
                cew_flat   = consumption_equiv_welfare(eu_flat, eu_notax, GAMMA_CEN)
                gap_bp     = (cew_flat - cew_prog) * 10000

                out[param_name][str(W0)][str(pval)] = _f(gap_bp)

        print(f"    {param_name} done")
    return out


def run_module5(p: dict) -> dict:
    print("\n=== Module 5: Welfare Sweeps ===")
    return {
        "sweep_a_revenue":   _run_sweep_a_revenue(p),
        "sweep_a_w0":        _run_sweep_a_w0(p),
        "sweep_b_start_year": _run_sweep_b_start_year(p),
        "sweep_c_params":    _run_sweep_c_params(p),
    }


# ─────────────────────────────────────────────────────────────────────────────
# JSON SERIALISER — handle numpy types
# ─────────────────────────────────────────────────────────────────────────────

class _NumpyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, (np.integer,)):
            return int(obj)
        if isinstance(obj, (np.floating,)):
            return None if math.isnan(obj) else float(obj)
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return super().default(obj)


# ─────────────────────────────────────────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────────────────────────────────────────

def main(modules: list = None, out_path: Path = None):
    if modules is None:
        modules = [1, 2, 3, 4, 5]
    if out_path is None:
        out_path = OUTPUT_ROOT / "wfr_results.json"

    print(f"WFR Core — running modules {modules}")
    p = load_params(str(TOML_PATH))

    result = {
        "meta": {
            "version": "wfr_core_v1",
            "date": date.today().isoformat(),
            "modules_run": modules,
            "params": {
                "toml_path": str(TOML_PATH),
                "canonical_N": p["tcm"]["canonical_N"],
                "scenario_start_year": p["tcm"].get("scenario_start_year"),
                "hist_mean": p["tcm"]["hist_mean"],
                "rate": p["rate"],
                "W0_norm": W0_NORM,
                "target_et_frac": TARGET_ET,
                "gamma_vals": GAMMA_VALS,
            },
        }
    }

    if 1 in modules:
        result["module1"] = run_module1(p)
    if 2 in modules:
        result["module2"] = run_module2(p)
    if 3 in modules:
        result["module3"] = run_module3(p)
    if 4 in modules:
        result["module4"] = run_module4(p)
    if 5 in modules:
        result["module5"] = run_module5(p)

    out_path.parent.mkdir(parents=True, exist_ok=True)
    with open(out_path, "w", encoding="utf-8") as fh:
        json.dump(result, fh, cls=_NumpyEncoder, indent=2)
    print(f"\n✓ Results written to: {out_path}")
    return result


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="WFR Welfare Computation Engine")
    parser.add_argument("--modules", nargs="+", type=int, choices=[1,2,3,4,5],
                        help="Which modules to run (default: all)")
    parser.add_argument("--out", type=Path, help="Output JSON path")
    args = parser.parse_args()
    main(modules=args.modules, out_path=args.out)
