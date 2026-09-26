"""
wfr_tables.py
=============
WFR Welfare Comparison Model — Table Generator

Reads wfr_results.json (produced by wfr_core.py) and writes
WFR_appendix_tables.md to the same directory.

Stateless: no computation, no model imports.  Only reads JSON,
formats numbers, and assembles markdown.

Usage
-----
  python wfr_tables.py                                 # default paths
  python wfr_tables.py --json path/to/wfr_results.json
  python wfr_tables.py --out  path/to/output.md

Table inventory
---------------
A.1  CEW by system, γ, distribution (Module 1)
A.2  Variance of consumption by system
A.3  Revenue-equivalent rates by system
A.4  Domar–Musgrave test results
B.1  Flat vs progressive WDT CEW (Module 2 C1)
B.2  Leverage effect on WDT tax base and welfare (C2)
B.3  Two-period rate asymmetry by wealth level (C3)
C.1  Lock-in welfare cost vs embedded gain ratio (Module 3)
C.2  Lock-in welfare cost vs holding period
C.3  Full WDT vs CGT comparison
D.1  CEW by tier and system (Module 4)
D.2  Distributional incidence: expected tax as % of W₀
D.3  Wealth concentration at key years (scenario, N=30)
D.4  Lifetime contribution envelope binding summary
D.5  Off-diagonal corner spot check
F.2  Extended concentration path key years (N=73)
F.3  Flat vs progressive WDT crossover summary
F.4  All-tier concentration matrix at N=73
E.1  Sweep A: CEW by system and revenue target (Module 5)
E.1b Sweep A: CEW by system and W₀
E.2a Sweep B: summary statistics across all start years
E.2b Sweep B: curated worst-case start years
E.3  Sweep C: parameter sensitivity (τ₀, τ_m, k, W_min)
"""

from __future__ import annotations

import argparse
import json
import math
import sys
from pathlib import Path

from wdt_md  import MdDoc, md_table, LEFT, RIGHT, CENTER
from wdt_fmt import fmt_pct, fmt_pct0, fmt_pct1, fmt_pct4, fmt_gbp_m, today_iso

# ─────────────────────────────────────────────────────────────────────────────
# CONSTANTS
# ─────────────────────────────────────────────────────────────────────────────

SYSTEMS = ["symmetric_wdt", "stock_wealth", "income", "cgt", "consumption"]
SYS_SHORT = {
    "symmetric_wdt" : "Symmetric WDT",
    "stock_wealth"  : "Stock Wealth Tax",
    "income"        : "Income Tax",
    "cgt"           : "CGT",
    "consumption"   : "Consumption Tax",
}
GAMMA_VALS = [1.0, 2.0, 4.0]


# ─────────────────────────────────────────────────────────────────────────────
# FORMAT HELPERS
# ─────────────────────────────────────────────────────────────────────────────

def _cew(v) -> str:
    return fmt_pct4(v) if v is not None else "—"

def _tau(v) -> str:
    return fmt_pct(v, dp=3) if v is not None else "—"

def _var(v) -> str:
    return f"{v:.4f}" if v is not None else "—"

def _bp(v) -> str:
    return f"{v:+.2f} bp" if v is not None else "—"

def _ratio(v) -> str:
    if v is None or (isinstance(v, float) and math.isnan(v)):
        return "—"
    return f"{v:,.1f}×"

def _pct1(v) -> str:
    return fmt_pct1(v) if v is not None else "—"

def _gbpm(v, dp=3) -> str:
    return fmt_gbp_m(v, dp=dp) if v is not None else "—"

def _dist_short(label: str) -> str:
    if "Version A" in label:
        return "Ver. A"
    return "Ver. B"


# ─────────────────────────────────────────────────────────────────────────────
# MODULE 1 TABLES
# ─────────────────────────────────────────────────────────────────────────────

def table_a1(m1: dict) -> str:
    """A.1: CEW by system, γ, and distribution."""
    dist_keys  = list(m1["distributions"].keys())
    col_groups = [(dk, g) for dk in dist_keys for g in GAMMA_VALS]
    headers    = ["System"] + [f"{_dist_short(dk)} γ={g:.0f}" for dk, g in col_groups]
    col_fmt    = [LEFT] + [RIGHT] * len(col_groups)
    rows = []
    for name in SYSTEMS:
        row = [SYS_SHORT[name]]
        for dk, g in col_groups:
            v = m1["distributions"][dk]["welfare"].get(str(g), {}).get(name, {}).get("cew")
            row.append(_cew(v))
        rows.append(row)
    return md_table(headers, rows, col_fmt=col_fmt)


def table_a2(m1: dict) -> str:
    """A.2: Variance of consumption at γ=2."""
    dist_keys = list(m1["distributions"].keys())
    headers   = ["System"] + [f"{_dist_short(dk)} Var(C)" for dk in dist_keys]
    col_fmt   = [LEFT] + [RIGHT] * len(dist_keys)
    rows = []
    for name in SYSTEMS:
        row = [SYS_SHORT[name]]
        for dk in dist_keys:
            v = m1["distributions"][dk]["welfare"].get("2.0", {}).get(name, {}).get("var_consumption")
            row.append(_var(v))
        rows.append(row)
    return md_table(headers, rows, col_fmt=col_fmt)


def table_a3(m1: dict) -> str:
    """A.3: Revenue-equivalent tax rates at γ=2."""
    dist_keys = list(m1["distributions"].keys())
    headers   = ["System"] + [f"{_dist_short(dk)} rate (τ*)" for dk in dist_keys]
    col_fmt   = [LEFT] + [RIGHT] * len(dist_keys)
    rows = []
    for name in SYSTEMS:
        row = [SYS_SHORT[name]]
        for dk in dist_keys:
            v = m1["distributions"][dk]["welfare"].get("2.0", {}).get(name, {}).get("tau")
            row.append(_tau(v))
        rows.append(row)
    return md_table(headers, rows, col_fmt=col_fmt)


def table_a4(m1: dict) -> str:
    """A.4: Domar–Musgrave test results."""
    headers = ["Distribution", "γ", "τ (WDT)", "(1−τ)²",
               "Actual ratio", "Gap", "Holds?"]
    col_fmt = [LEFT, RIGHT, RIGHT, RIGHT, RIGHT, RIGHT, CENTER]
    rows = []
    for dk, dist_data in m1["distributions"].items():
        for g in GAMMA_VALS:
            dm = dist_data.get("dm_test", {}).get(str(g))
            if dm is None:
                continue
            tau_wdt = dist_data["welfare"].get(str(g), {}).get("symmetric_wdt", {}).get("tau")
            rows.append([
                _dist_short(dk),
                f"{g:.1f}",
                f"{tau_wdt*100:.4f}%" if tau_wdt is not None else "—",
                f'{dm["predicted_ratio"]:.6f}',
                f'{dm["actual_ratio"]:.6f}',
                f'{dm["gap"]:.2e}',
                "✓" if dm["dm_holds"] else "✗",
            ])
    return md_table(headers, rows, col_fmt=col_fmt)


# ─────────────────────────────────────────────────────────────────────────────
# MODULE 2 TABLES
# ─────────────────────────────────────────────────────────────────────────────

def table_b1(m2: dict) -> str:
    """B.1: Flat WDT vs progressive WDT CEW across γ and distributions."""
    headers = ["Distribution", "γ", "Flat WDT CEW", "Progressive WDT CEW",
               "Gap (bp)", "E[T] progressive"]
    col_fmt = [LEFT, RIGHT, RIGHT, RIGHT, RIGHT, RIGHT]
    rows = []
    for dk, gamma_results in m2["c1"].items():
        for g_str, r in gamma_results.items():
            rows.append([
                _dist_short(dk), g_str,
                _cew(r.get("cew_flat")),
                _cew(r.get("cew_progressive")),
                _bp(r.get("cew_gap_bp")),
                _gbpm(r.get("et_progressive"), dp=4),
            ])
    return md_table(headers, rows, col_fmt=col_fmt)


def table_b2(m2: dict) -> str:
    """B.2: Leverage effect on WDT tax base and welfare."""
    headers = [
        "Leverage (%)", "W₀ net (£m)", "E[T] NW base", "E[T] asset-rtn base",
        "CEW NW base", "CEW asset-rtn base", "Gap (bp)",
    ]
    col_fmt = [RIGHT] * 7
    rows = []
    for r in m2["c2_leverage"]:
        rows.append([
            f'{r["leverage_ratio"]*100:.1f}',
            _gbpm(r.get("W0"), dp=2),
            f'{r["et_nw"]:.4f}' if r.get("et_nw") is not None else "—",
            f'{r["et_ar"]:.4f}' if r.get("et_ar") is not None else "—",
            _cew(r.get("cew_nw")),
            _cew(r.get("cew_ar")),
            _bp(r.get("cew_gap_bp")),
        ])
    return md_table(headers, rows, col_fmt=col_fmt)


def table_b3(m2: dict) -> str:
    """B.3: Two-period rate asymmetry by initial wealth."""
    c3 = m2["c3_asymmetry"]
    W0_vals = c3["W0_vals"]
    headers = [
        "W₀ (£m)", "τ gain (%)", "τ refund (%)", "Asymmetry (pp)",
        "Net tax: progressive", "Net tax: flat", "Excess",
    ]
    col_fmt = [RIGHT] * 7
    rows = []
    for W0, r in zip(W0_vals, c3["results"]):
        tau1 = r.get("tau1_progressive")
        tau2 = r.get("tau2_progressive")
        asym = r.get("rate_asymmetry")
        rows.append([
            f"{W0:.1f}",
            f"{tau1*100:.3f}" if tau1 is not None else "—",
            f"{tau2*100:.3f}" if tau2 is not None else "—",
            f"{asym*100:+.4f}" if asym is not None else "—",
            _gbpm(r.get("net_tax_prog"), dp=4),
            _gbpm(r.get("net_tax_flat"), dp=4),
            f'{r["net_tax_excess"]:+.4f}' if r.get("net_tax_excess") is not None else "—",
        ])
    return md_table(headers, rows, col_fmt=col_fmt)


# ─────────────────────────────────────────────────────────────────────────────
# MODULE 3 TABLES
# ─────────────────────────────────────────────────────────────────────────────

def table_c1(m3: dict) -> str:
    """C.1: Lock-in welfare cost by embedded gain ratio."""
    headers = [
        "G/V (%)", "CEW (free)", "CEW (locked)", "Lock-in cost (bp)",
        "P(total locked)", "P(CGT distortion)", "P(r_B < r_A)",
    ]
    col_fmt = [RIGHT] * 7
    rows = []
    for r in m3["sens_gain"]:
        rows.append([
            f'{r["gain_ratio"]*100:.1f}',
            _cew(r.get("cew_free")),
            _cew(r.get("cew_locked")),
            _bp(r.get("lock_in_cost_bp")),
            _pct1(r.get("p_locked")),
            _pct1(r.get("p_locked_cgt")),
            _pct1(r.get("p_below_rA")),
        ])
    return md_table(headers, rows, col_fmt=col_fmt)


def table_c2(m3: dict) -> str:
    """C.2: Lock-in welfare cost by remaining holding period T."""
    headers = [
        "T (years)", "r_B* (%)", "Lock-in cost (bp)",
        "P(total locked)", "P(CGT distortion)", "P(r_B < r_A)",
    ]
    col_fmt = [RIGHT] * 6
    rows = []
    for r in m3["sens_T"]:
        r_indiff = r.get("r_B_indiff")
        rows.append([
            str(r["T"]),
            f'{r_indiff*100:.4f}%' if r_indiff is not None else "—",
            _bp(r.get("lock_in_cost_bp")),
            _pct1(r.get("p_locked")),
            _pct1(r.get("p_locked_cgt")),
            _pct1(r.get("p_below_rA")),
        ])
    return md_table(headers, rows, col_fmt=col_fmt)


def table_c3(m3: dict) -> str:
    """C.3: Full WDT vs CGT welfare comparison."""
    dist_keys = list(m3["full_comparison"].keys())
    headers   = ["Metric"] + [_dist_short(dk) for dk in dist_keys]
    col_fmt   = [LEFT] + [RIGHT] * len(dist_keys)

    def _row(label, key, fmt_fn=_cew):
        return [label] + [fmt_fn(m3["full_comparison"][dk].get(key)) for dk in dist_keys]

    def _pct_row(label, key):
        return [label] + [
            f'{m3["full_comparison"][dk][key]*100:.4f}%'
            if m3["full_comparison"][dk].get(key) is not None else "—"
            for dk in dist_keys
        ]

    rows = [
        _row("WDT CEW",                     "wdt_cew"),
        _row("CGT CEW (no lock-in)",         "cgt_cew"),
        _row("Lock-in welfare cost",         "lock_in_cost_bp", _bp),
        _row("CGT CEW (with lock-in)",       "cgt_with_lock_cew"),
        _row("WDT advantage (no lock-in)",   "wdt_adv_no_lock_bp",   _bp),
        _row("WDT advantage (with lock-in)", "wdt_adv_with_lock_bp", _bp),
        _row("P(agent locked in)",           "p_locked", _pct1),
        _pct_row("CGT indifference return r_B*", "r_B_indiff"),
        _pct_row("Revenue-equivalent CGT rate",  "m1_cgt_tau"),
    ]
    return md_table(headers, rows, col_fmt=col_fmt)


# ─────────────────────────────────────────────────────────────────────────────
# MODULE 4 TABLES
# ─────────────────────────────────────────────────────────────────────────────

def _tier_header(tier_info: dict, tiers_list: list) -> str:
    t = next((x for x in tiers_list if x["name"] == tier_info), None)
    if t is None:
        return tier_info
    return f'{t["name"]} ({t["bracket_label"]}, W₀={_gbpm(t["W0"], dp=1)})'


def table_d1(m4: dict) -> str:
    """D.1: CEW by tier and system."""
    tiers_ord = ["Poor", "Ok", "Good", "Great"]
    tiers_meta = m4["tiers"]
    tw = m4["tier_welfare"]
    headers = ["System"] + [_tier_header(t, tiers_meta) for t in tiers_ord]
    col_fmt = [LEFT] + [RIGHT] * len(tiers_ord)
    rows = []
    for name in SYSTEMS:
        row = [SYS_SHORT[name]]
        for t in tiers_ord:
            v = tw[t]["systems"].get(name, {}).get("cew")
            row.append(_cew(v))
        rows.append(row)
    # Progressive WDT row
    prog_row = ["Progressive WDT"]
    for t in tiers_ord:
        prog_row.append(_cew(tw[t].get("cew_progressive")))
    rows.append(prog_row)
    return md_table(headers, rows, col_fmt=col_fmt)


def table_d2(m4: dict) -> str:
    """D.2: Distributional incidence — expected tax as % of W₀."""
    tiers_ord  = ["Poor", "Ok", "Good", "Great"]
    tiers_meta = m4["tiers"]
    tw = m4["tier_welfare"]
    headers = ["System"] + [_tier_header(t, tiers_meta) for t in tiers_ord]
    col_fmt = [LEFT] + [RIGHT] * len(tiers_ord)
    rows = []
    for name in SYSTEMS:
        row = [SYS_SHORT[name]]
        for t in tiers_ord:
            v = tw[t]["systems"].get(name, {}).get("et_pct_W0")
            row.append(f"{v:.4f}%" if v is not None else "—")
        rows.append(row)
    return md_table(headers, rows, col_fmt=col_fmt)


def table_d3(m4: dict) -> str:
    """D.3: Wealth concentration — Great/Poor ratio at key years (scenario)."""
    conc  = m4["concentration"]["scenario"]
    years = conc["years"]
    paths = conc["systems"]
    year0 = years[0] if years else 0
    N = len(years)

    if N >= 30:
        key_idxs = [0, 5, 10, 20, N]
    else:
        step = max(1, N // 4)
        key_idxs = sorted(set([0, step, 2*step, 3*step, N]))

    def _label(idx):
        return "Initial" if idx == 0 else str(year0 + idx - 1)

    sys_labels = {
        "symmetric_wdt":   "Flat WDT",
        "progressive_wdt": "Progressive WDT",
        "stock_wealth":    "Stock Wealth Tax",
        "income":          "Income Tax",
        "consumption":     "Consumption Tax",
    }
    systems = ["symmetric_wdt", "progressive_wdt", "stock_wealth", "income", "consumption"]
    headers = ["System"] + [_label(i) for i in key_idxs]
    col_fmt = [LEFT] + [RIGHT] * len(key_idxs)
    rows = []
    for name in systems:
        if name not in paths:
            continue
        great = paths[name].get("Great", [])
        poor  = paths[name].get("Poor",  [])
        if not great:
            continue
        row = [sys_labels.get(name, name)]
        for idx in key_idxs:
            i = min(idx, len(great) - 1)
            if poor[i] and poor[i] > 0 and great[i]:
                row.append(_ratio(great[i] / poor[i]))
            else:
                row.append("—")
        rows.append(row)
    return md_table(headers, rows, col_fmt=col_fmt)


def table_d4(m4: dict) -> str:
    """D.4: Envelope binding summary by tier."""
    headers = [
        "Tier", "Bracket", "W₀ (£m)", "Cumulative tax (£m)",
        "Cumulative refund (£m)", "Min slack (£m)", "Binding years", "Ever binds?",
    ]
    col_fmt = [LEFT, LEFT, RIGHT, RIGHT, RIGHT, RIGHT, CENTER, CENTER]
    tier_meta = {t["name"]: t for t in m4["tiers"]}
    rows = []
    for tier_name, er in m4["envelope"].items():
        t    = tier_meta.get(tier_name, {})
        W0   = t.get("W0", 0)
        brac = t.get("bracket_label", "—")
        binding = ", ".join(str(y) for y in er.get("binding_years", [])) or "—"
        rows.append([
            tier_name, brac,
            _gbpm(W0, dp=1),
            _gbpm(er.get("cum_tax_final"), dp=3),
            _gbpm(er.get("cum_ref_final"), dp=3),
            _gbpm(er.get("min_slack"), dp=4),
            binding,
            "⚠ Yes" if er.get("ever_binds") else "No",
        ])
    return md_table(headers, rows, col_fmt=col_fmt)


def table_d5(m4: dict) -> str:
    """D.5: Off-diagonal corner check."""
    tw  = m4["tier_welfare"]
    cr  = m4["corner_check"]
    corner_configs = [
        ("corner_A", "Corner A: Great diff (+3.45pp), Poor W₀",  "Poor",  "Great"),
        ("corner_B", "Corner B: Poor diff (−4.55pp), Great W₀",  "Great", "Poor"),
    ]
    sys_short = {
        "symmetric_wdt":  "Symmetric WDT",  "stock_wealth": "Stock Wealth Tax",
        "income": "Income Tax",             "cgt": "CGT",
        "consumption": "Consumption Tax",
    }
    headers = [
        "Corner / System", "Corner CEW",
        "Diagonal (same W₀)", "Diagonal (same diff)", "Δ vs same-W₀ (bp)",
    ]
    col_fmt = [LEFT, RIGHT, RIGHT, RIGHT, RIGHT]
    rows = []
    for key, label, diag_w0, diag_diff in corner_configs:
        rows.append([f"**{label}**", "", "", "", ""])
        corner = cr.get(key, {})
        for name in SYSTEMS:
            c_cew  = corner.get("systems", {}).get(name, {}).get("cew")
            w0_cew = tw.get(diag_w0,   {}).get("systems", {}).get(name, {}).get("cew")
            d_cew  = tw.get(diag_diff, {}).get("systems", {}).get(name, {}).get("cew")
            delta  = (c_cew - w0_cew) * 10000 if (c_cew is not None and w0_cew is not None) else None
            rows.append([
                f"\u00a0\u00a0{sys_short[name]}",
                _cew(c_cew), _cew(w0_cew), _cew(d_cew),
                f"{delta:+.2f}" if delta is not None else "—",
            ])
        c_prog  = corner.get("cew_progressive")
        w0_prog = tw.get(diag_w0,   {}).get("cew_progressive")
        d_prog  = tw.get(diag_diff, {}).get("cew_progressive")
        delta_p = (c_prog - w0_prog) * 10000 if (c_prog is not None and w0_prog is not None) else None
        rows.append([
            "\u00a0\u00a0Progressive WDT",
            _cew(c_prog), _cew(w0_prog), _cew(d_prog),
            f"{delta_p:+.2f}" if delta_p is not None else "—",
        ])
        rows.append(["", "", "", "", ""])

    if rows and rows[-1] == ["", "", "", "", ""]:
        rows = rows[:-1]
    return md_table(headers, rows, col_fmt=col_fmt)


# ─────────────────────────────────────────────────────────────────────────────
# MODULE 4 PART F TABLES (N=73 extended horizon)
# ─────────────────────────────────────────────────────────────────────────────

_F_SYS = ["symmetric_wdt", "progressive_wdt", "stock_wealth", "income", "consumption"]
_F_SYS_LABELS = {
    "symmetric_wdt":   "Flat WDT",
    "progressive_wdt": "Progressive WDT",
    "stock_wealth":    "Stock Wealth Tax",
    "income":          "Income Tax",
    "consumption":     "Consumption Tax",
}


def table_f2(m4: dict) -> str:
    """F.2: Extended concentration path at key years (N=73)."""
    ext   = m4["concentration"]["extended"]
    years = ext["years"]
    paths = ext["systems"]
    year0 = years[0] if years else 1947
    key_years = ["Initial", 1957, 1967, 1977, 1987, 1997, 2000, 2007, 2019]

    def _idx(label):
        return 0 if label == "Initial" else (label - year0 + 1)

    headers = ["System"] + [str(y) for y in key_years]
    col_fmt = [LEFT] + [RIGHT] * len(key_years)
    rows = []
    for name in _F_SYS:
        if name not in paths:
            continue
        great = paths[name].get("Great", [])
        poor  = paths[name].get("Poor",  [])
        if not great:
            continue
        row = [_F_SYS_LABELS[name]]
        for label in key_years:
            idx = min(_idx(label), len(great) - 1)
            if poor[idx] and poor[idx] > 0 and great[idx]:
                row.append(_ratio(great[idx] / poor[idx]))
            else:
                row.append("—")
        rows.append(row)
    return md_table(headers, rows, col_fmt=col_fmt)


def table_f3(m4: dict) -> str:
    """F.3: Flat vs progressive WDT crossover summary."""
    ext   = m4["concentration"]["extended"]
    paths = ext["systems"]
    co    = ext.get("crossover")
    scen  = m4["concentration"]["scenario"]
    sp    = scen["systems"]

    def _ratio_last(p, name, tier_num, tier_den):
        great = p.get(name, {}).get(tier_num, [None])
        poor  = p.get(name, {}).get(tier_den, [None])
        if great and poor and great[-1] and poor[-1] and poor[-1] > 0:
            return great[-1] / poor[-1]
        return None

    rf_n30 = _ratio_last(sp, "symmetric_wdt",   "Great", "Poor")
    rp_n30 = _ratio_last(sp, "progressive_wdt",  "Great", "Poor")
    rf_n73 = _ratio_last(paths, "symmetric_wdt",  "Great", "Poor")
    rp_n73 = _ratio_last(paths, "progressive_wdt","Great", "Poor")

    headers = ["Metric", "Value"]
    col_fmt = [LEFT, RIGHT]
    rows = [
        ["Great/Poor ratio: Flat WDT at N=30",         _ratio(rf_n30)],
        ["Great/Poor ratio: Progressive WDT at N=30",  _ratio(rp_n30)],
        ["Gap at N=30 (Progressive − Flat)",
         f"{rp_n30 - rf_n30:+.1f}×" if (rp_n30 and rf_n30) else "—"],
        ["Great/Poor ratio: Flat WDT at N=73",         _ratio(rf_n73)],
        ["Great/Poor ratio: Progressive WDT at N=73",  _ratio(rp_n73)],
        ["Gap at N=73 (Progressive − Flat)",
         f"{rp_n73 - rf_n73:+.1f}×" if (rp_n73 and rf_n73) else "—"],
        ["First year Progressive WDT ratio < Flat WDT ratio",
         str(co["year"]) if co else "No crossover within N=73"],
    ]
    if co:
        rows.append(["Gap at crossover year", f'{co["gap"]:+.2f}×'])
    return md_table(headers, rows, col_fmt=col_fmt)


def table_f4(m4: dict) -> str:
    """F.4: All-tier concentration matrix at N=73."""
    paths   = m4["concentration"]["extended"]["systems"]
    headers = ["System", "Great/Poor", "Great/Ok", "Ok/Poor"]
    col_fmt = [LEFT, RIGHT, RIGHT, RIGHT]
    rows = []
    for name in _F_SYS:
        if name not in paths:
            continue
        great = paths[name].get("Great", [None])
        ok    = paths[name].get("Ok",    [None])
        poor  = paths[name].get("Poor",  [None])
        if not great or great[-1] is None:
            continue
        gp = great[-1] / poor[-1]  if (poor[-1]  and poor[-1]  > 0) else None
        go = great[-1] / ok[-1]    if (ok[-1]    and ok[-1]    > 0) else None
        op = ok[-1]    / poor[-1]  if (poor[-1]  and poor[-1]  > 0 and ok[-1]) else None
        rows.append([_F_SYS_LABELS[name], _ratio(gp), _ratio(go), _ratio(op)])
    return md_table(headers, rows, col_fmt=col_fmt)


# ─────────────────────────────────────────────────────────────────────────────
# MODULE 5 TABLES
# ─────────────────────────────────────────────────────────────────────────────

def table_e1(m5: dict) -> str:
    """E.1: CEW by system and revenue target (γ=2)."""
    gamma    = "2.0"
    rev_data = m5["sweep_a_revenue"]
    target_pcts = sorted(rev_data.keys(), key=float)
    headers  = ["Distribution", "System"] + [f"E[T]={p}%" for p in target_pcts]
    col_fmt  = [LEFT, LEFT] + [RIGHT] * len(target_pcts)
    rows = []
    for dlabel, dist_name in [("A", "Ver. A"), ("B", "Ver. B")]:
        for name in SYSTEMS:
            row = [dist_name, SYS_SHORT[name]]
            for pct in target_pcts:
                v = rev_data.get(pct, {}).get(dlabel, {}).get(gamma, {}).get(name)
                row.append(_cew(v))
            rows.append(row)
        rows.append([""] * len(headers))
    return md_table(headers, rows[:-1], col_fmt=col_fmt)


def table_e1b(m5: dict) -> str:
    """E.1b: CEW by system and W₀ (γ=2, E[T]=2%)."""
    w0_data = m5["sweep_a_w0"]
    W0_vals = sorted(w0_data.keys(), key=float)
    headers = ["System"] + [f"W₀=£{float(w):.0f}m" for w in W0_vals]
    col_fmt = [LEFT] + [RIGHT] * len(W0_vals)
    rows = []
    for name in SYSTEMS:
        row = [SYS_SHORT[name]]
        for w in W0_vals:
            v = w0_data.get(w, {}).get(name)
            row.append(_cew(v))
        rows.append(row)
    return md_table(headers, rows, col_fmt=col_fmt)


def table_e2a(m5: dict) -> str:
    """E.2a: Summary statistics across all start years."""
    import statistics
    sy_data = m5["sweep_b_start_year"]
    headers = ["System", "Min CEW", "Median CEW", "Mean CEW", "Max CEW",
               "WDT best? (% of windows)"]
    col_fmt = [LEFT, RIGHT, RIGHT, RIGHT, RIGHT, RIGHT]

    all_years = sorted(sy_data.keys())
    wdt_best = sum(
        1 for yr in all_years
        if (sy_data[yr].get("symmetric_wdt") is not None and
            all(sy_data[yr].get("symmetric_wdt", float('-inf')) >= sy_data[yr].get(n, float('-inf'))
                for n in SYSTEMS if sy_data[yr].get(n) is not None))
    )
    wdt_best_pct = wdt_best / len(all_years) * 100 if all_years else 0

    rows = []
    for name in SYSTEMS:
        vals = [sy_data[yr][name] for yr in all_years if sy_data[yr].get(name) is not None]
        if not vals:
            rows.append([SYS_SHORT[name]] + ["—"] * 5)
            continue
        rows.append([
            SYS_SHORT[name],
            _cew(min(vals)),
            _cew(statistics.median(vals)),
            _cew(sum(vals) / len(vals)),
            _cew(max(vals)),
            f"{wdt_best_pct:.1f}%" if name == "symmetric_wdt" else "—",
        ])
    return md_table(headers, rows, col_fmt=col_fmt)


def table_e2b(m5: dict, curated_years: list) -> str:
    """E.2b: Curated worst-case start years."""
    sy_data = m5["sweep_b_start_year"]
    display = sorted(set(curated_years) | {2000})
    headers = (
        ["Start year"] +
        [SYS_SHORT[n] for n in SYSTEMS] +
        ["WDT adv. vs Stock (bp)"]
    )
    col_fmt = [LEFT] + [RIGHT] * (len(SYSTEMS) + 1)
    rows = []
    for yr in display:
        key = str(yr)
        if key not in sy_data:
            continue
        yr_res = sy_data[key]
        wdt_c  = yr_res.get("symmetric_wdt")
        sw_c   = yr_res.get("stock_wealth")
        adv    = (wdt_c - sw_c) * 10000 if (wdt_c is not None and sw_c is not None) else None
        row = [str(yr) + (" ◄ canonical" if yr == 2000 else "")]
        for name in SYSTEMS:
            row.append(_cew(yr_res.get(name)))
        row.append(f"{adv:+.1f}" if adv is not None else "—")
        rows.append(row)
    return md_table(headers, rows, col_fmt=col_fmt)


def tables_e3(m5: dict) -> dict:
    """E.3: Parameter sensitivity tables (returns dict of param_name → md str)."""
    param_data = m5["sweep_c_params"]
    out = {}
    param_labels = {
        "tau_0": "τ₀ (entry rate)",
        "tau_m": "τ_m (ceiling rate)",
        "k":     "k (steepness per £m)",
        "W_min": "W_min (£m)",
    }
    for param_name, w0_results in param_data.items():
        W0_keys    = sorted(w0_results.keys(), key=float)
        param_vals = sorted(list(w0_results[W0_keys[0]].keys()), key=float)
        headers    = [param_labels.get(param_name, param_name)] + [f"W₀=£{float(w):.0f}m" for w in W0_keys]
        col_fmt    = [LEFT] + [RIGHT] * len(W0_keys)
        rows = []
        for pval in param_vals:
            row = [str(pval)]
            for w in W0_keys:
                v = w0_results[w].get(pval)
                row.append(f"{v:+.2f}" if v is not None else "—")
            rows.append(row)
        out[param_name] = md_table(headers, rows, col_fmt=col_fmt)
    return out


# ─────────────────────────────────────────────────────────────────────────────
# DOCUMENT ASSEMBLY
# ─────────────────────────────────────────────────────────────────────────────

def build_doc(data: dict) -> MdDoc:
    doc = MdDoc()
    params = data["meta"]["params"]
    has = lambda mod: mod in data

    doc.h1("WFR Welfare Comparison Model — Appendix Tables")
    doc.blank()
    doc.add(f"*Generated: {today_iso()}*")
    doc.add(f"*Revenue target: E[T] = {params['target_et_frac']*100:.0f}% of W₀. "
            f"Canonical N = {params['canonical_N']}. "
            f"Scenario start = {params['scenario_start_year']}.*")
    doc.add("*All CEW values relative to no-tax benchmark. Negative = welfare cost.*")
    doc.blank()
    doc.rule()

    # ── A: Module 1 ────────────────────────────────────────────────────────
    if has("module1"):
        m1 = data["module1"]
        doc.blank()
        doc.h2("A. Baseline Single-Agent Comparison")
        doc.blank()

        doc.h3("A.1 — CEW by System, γ, and Distribution")
        doc.note(
            "CEW = proportional consumption change under no-tax making agent indifferent "
            "to the taxed system. Negative = welfare cost relative to no-tax. "
            "Ver. A = UK historical equity (scenario window). "
            "Ver. B = idealised two-state (p=0.5, R_good=E[R]+σ, R_bad=E[R]−σ)."
        )
        doc.add_block(table_a1(m1))
        doc.blank()

        doc.h3("A.2 — Variance of Consumption (γ=2)")
        doc.note(
            "Variance of consumption across return states at revenue-equivalent rates. "
            "Lower variance indicates greater risk-sharing. "
            "D-M prediction: Var(C_sym) = (1−τ)² × Var(C_notax)."
        )
        doc.add_block(table_a2(m1))
        doc.blank()

        doc.h3("A.3 — Revenue-Equivalent Tax Rates (γ=2)")
        doc.note(
            "Rate τ* such that E[T(W₀, dist, τ*)] = target. "
            "Stock wealth and consumption taxes require low rates (broad base); "
            "income tax and CGT require higher rates (gains only, no collection in loss states)."
        )
        doc.add_block(table_a3(m1))
        doc.blank()

        doc.h3("A.4 — Domar–Musgrave Test: Symmetric WDT")
        doc.note(
            "Prediction: Var(C_tax) / Var(C_notax) = (1−τ)². "
            "Gap near zero confirms D-M holds for the flat-rate symmetric case."
        )
        doc.add_block(table_a4(m1))
        doc.blank()
        doc.rule()

    # ── B: Module 2 ────────────────────────────────────────────────────────
    if has("module2"):
        m2 = data["module2"]
        doc.blank()
        doc.h2("B. Progressive Rates and the Three D-M Complications")
        doc.blank()

        doc.h3("B.1 — Flat WDT vs Progressive WDT CEW")
        doc.note(
            "C1 complication: progressive rate breaks the flat D-M result. "
            "Flat WDT revenue-matched to progressive WDT's E[T]. "
            "Gap (bp) = (CEW_flat − CEW_progressive) × 10,000. Positive = flat WDT better."
        )
        doc.add_block(table_b1(m2))
        doc.blank()

        doc.h3("B.2 — Leverage Effect on WDT Tax Base and Welfare")
        doc.note(
            "C2 complication: WDT taxes the amplified net-worth delta rather than underlying asset return. "
            "NW base = actual WDT base; asset-return base = hypothetical alternative. "
            "Gap (bp) = (CEW_NW − CEW_AR) × 10,000."
        )
        doc.add_block(table_b2(m2))
        doc.blank()

        doc.h3("B.3 — Two-Period Rate Asymmetry by Initial Wealth")
        doc.note(
            "C3 complication: gain-year rate ≠ refund-year rate under progression. "
            "Sequence: gain (μ+σ) in period 1, loss (σ) in period 2. "
            "Excess = net tax progressive − net tax flat."
        )
        doc.add_block(table_b3(m2))
        doc.blank()
        doc.rule()

    # ── C: Module 3 ────────────────────────────────────────────────────────
    if has("module3"):
        m3 = data["module3"]
        doc.blank()
        doc.h2("C. CGT Lock-In Distortion")
        doc.blank()
        ar  = m3["asset_ref"]
        doc.add(
            f"Reference parameters: V=£{ar['V']:.0f}m, G/V={ar['gain_ratio']*100:.0f}%, "
            f"r_A={ar['r_A']*100:.2f}%, τ_cgt={ar['tau_cgt']*100:.0f}%, T={ar['T']} years."
        )
        doc.blank()

        doc.h3("C.1 — Lock-In Welfare Cost by Embedded Gain Ratio")
        doc.note(
            "Lock-in cost (bp) = (CEW_free − CEW_locked) × 10,000. "
            "CEW_free: agent switches whenever r_B > r_A. "
            "CEW_locked: agent stays in A when r_B < indifference return r_B*. "
            "Ver. A distribution. γ=2."
        )
        doc.add_block(table_c1(m3))
        doc.blank()

        doc.h3("C.2 — Lock-In Welfare Cost by Remaining Holding Period")
        doc.note(
            "G/V=50% fixed. T varies from 1 to 20 years. "
            "Indifference return r_B* converges to r_A as T→∞."
        )
        doc.add_block(table_c2(m3))
        doc.blank()

        doc.h3("C.3 — Full Welfare Comparison: WDT vs CGT")
        doc.note(
            "Adds lock-in cost to CGT welfare, correcting the Module 1 comparison. "
            "WDT advantage (with lock-in) = CEW_WDT − CEW_CGT_locked."
        )
        doc.add_block(table_c3(m3))
        doc.blank()
        doc.rule()

    # ── D: Module 4 ────────────────────────────────────────────────────────
    if has("module4"):
        m4 = data["module4"]
        doc.blank()
        doc.h2("D. Heterogeneous Agents — Incidence and Concentration")
        doc.blank()
        doc.add(
            "Tier differentials from Fagereng et al. (2020). "
            "Version A distribution with tier-shifted returns. γ=2. "
            "Revenue target = 2% of population-weighted aggregate W₀."
        )
        doc.blank()

        doc.h3("D.1 — CEW by Tier and Tax System")
        doc.note(
            "Progressive WDT uses logistic rate function from TOML. "
            "All flat-rate systems calibrated at population-weighted aggregate revenue target."
        )
        doc.add_block(table_d1(m4))
        doc.blank()

        doc.h3("D.2 — Distributional Incidence: Expected Tax as % of W₀")
        doc.note("E[T] / W₀ × 100. Rates are population-aggregate equivalent, not per-tier.")
        doc.add_block(table_d2(m4))
        doc.blank()

        doc.h3("D.3 — Wealth Concentration Path: Great/Poor Ratio at Key Years")
        doc.note(
            "All systems calibrated at the aggregate tau from D.1. "
            "Progressive WDT uses logistic rate function directly. "
            "Initial ratio reflects W₀ difference only."
        )
        doc.add_block(table_d3(m4))
        doc.blank()

        doc.h3("D.4 — Lifetime Contribution Envelope: Binding Summary")
        doc.note(
            "Envelope binds when cumulative refunds would exceed cumulative taxes paid. "
            "Refund capped at cumulative taxes paid to date when binding occurs."
        )
        doc.add_block(table_d4(m4))
        doc.blank()

        if m4.get("corner_check"):
            doc.h3("D.5 — Off-Diagonal Spot Check")
            doc.note(
                "Corner A: Great return differential at Poor-tier W₀. "
                "Corner B: Poor return differential at Great-tier W₀. "
                "Δ vs same-W₀ (bp) = (Corner CEW − Diagonal same-W₀ CEW) × 10,000."
            )
            doc.add_block(table_d5(m4))
            doc.blank()

        doc.rule()

        # Part F — extended horizon
        ext = m4["concentration"]["extended"]
        if ext.get("years"):
            doc.blank()
            doc.h2("F. Extended Concentration Horizon (N=73)")
            doc.blank()
            doc.add(
                "Same tiers, systems, and rates as D. Horizon extends to full 1947–2019 "
                "historical sequence (no rotation). Rates carried forward from D."
            )
            doc.blank()

            doc.h3("F.2 — Extended Concentration Path (Key Years)")
            doc.note("Great/Poor wealth ratio at selected years across the full 1947–2019 sequence.")
            doc.add_block(table_f2(m4))
            doc.blank()

            doc.h3("F.3 — Flat vs Progressive WDT: Crossover Horizon")
            doc.note(
                "Reports whether and when the progressive WDT Great/Poor ratio drops below "
                "the flat WDT ratio at extended horizons."
            )
            doc.add_block(table_f3(m4))
            doc.blank()

            doc.h3("F.4 — All-Tier Concentration Matrix at N=73")
            doc.note("Great/Poor, Great/Ok, and Ok/Poor ratios at the N=73 terminal horizon.")
            doc.add_block(table_f4(m4))
            doc.blank()
            doc.rule()

    # ── E: Module 5 ────────────────────────────────────────────────────────
    if has("module5"):
        m5 = data["module5"]
        curated = data["meta"]["params"].get("wfr_start_years_curated",
                  [1946, 1972, 1987, 1999, 2000, 2006])
        doc.blank()
        doc.h2("E. Welfare Sweep Analysis")
        doc.blank()

        doc.h3("E.1 — Sweep A: CEW by System and Revenue Target (γ=2)")
        doc.note("E[T] as % of W₀ swept from 1% to 5%. Columns = revenue target.")
        doc.add_block(table_e1(m5))
        doc.blank()

        doc.h3("E.1b — Sweep A: CEW by System and W₀ (γ=2, E[T]=2%)")
        doc.note(
            "W₀ swept across the wealth-tier range at fixed 2% revenue target. "
            "CEW is invariant to W₀ under this fixed-percentage design."
        )
        doc.add_block(table_e1b(m5))
        doc.blank()

        doc.h3("E.2a — Sweep B: Summary Statistics Across All Start Years")
        doc.note(
            "Min/median/mean/max CEW across all 73 start-year windows (1947–2019). "
            "WDT best? = fraction of windows where Symmetric WDT has the lowest welfare cost."
        )
        doc.add_block(table_e2a(m5))
        doc.blank()

        doc.h3("E.2b — Sweep B: Curated Worst-Case Start Years")
        doc.note(
            "Six historically adverse start years plus the canonical 2000 (◄). "
            "WDT adv. = (CEW_WDT − CEW_StockWealth) × 10,000 in basis points."
        )
        doc.add_block(table_e2b(m5, curated))
        doc.blank()

        e3_tables = tables_e3(m5)
        param_meta = {
            "tau_0": ("E.3.1 — Sweep C: τ₀ Sensitivity",
                      "Gap (bp) = (CEW_flat − CEW_progressive) × 10,000. "
                      "τ_m, k, W_min at canonical values."),
            "tau_m": ("E.3.2 — Sweep C: τ_m Sensitivity", "τ₀, k, W_min at canonical values."),
            "k":     ("E.3.3 — Sweep C: k Sensitivity",   "τ₀, τ_m, W_min at canonical values."),
            "W_min": ("E.3.4 — Sweep C: W_min Sensitivity","τ₀, τ_m, k at canonical values."),
        }
        for param_name, tbl_str in e3_tables.items():
            if param_name in param_meta:
                title, note_text = param_meta[param_name]
                doc.h3(title)
                doc.note(note_text)
                doc.add_block(tbl_str)
                doc.blank()

        doc.rule()

    # ── G: Parameter reference ──────────────────────────────────────────────
    doc.blank()
    doc.h2("G. Parameter Reference")
    doc.blank()
    rp = params["rate"]
    doc.add("| Parameter | Value |")
    doc.add("|:---|---:|")
    doc.add(f"| W₀ (normalised) | {params['W0_norm']:.1f} |")
    doc.add(f"| Revenue target E[T] | {params['target_et_frac']*100:.0f}% of W₀ |")
    doc.add(f"| γ (central case) | 2.0 |")
    doc.add(f"| τ₀ | {fmt_pct0(rp['tau_0'])} |")
    doc.add(f"| τ_m | {fmt_pct0(rp['tau_m'])} |")
    doc.add(f"| k | {rp['k']} per £m |")
    doc.add(f"| W_min | £{rp['W_min']:.1f}m |")
    doc.add(f"| canonical_N | {params['canonical_N']} years |")
    doc.add(f"| hist_mean | {fmt_pct(params['hist_mean'])} |")
    doc.blank()

    return doc


# ─────────────────────────────────────────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────────────────────────────────────────

def main(json_path: Path = None, out_path: Path = None):
    if json_path is None:
        # default: same directory as this script
        json_path = Path(__file__).parent / "OUTPUTS" / "WFR" / "wfr" / "wfr_results.json"
    if out_path is None:
        out_path = json_path.parent / "WFR_appendix_tables.md"

    if not json_path.exists():
        print(f"ERROR: results file not found: {json_path}", file=sys.stderr)
        print("Run wfr_core.py first.", file=sys.stderr)
        sys.exit(1)

    print(f"Reading: {json_path}")
    with open(json_path, encoding="utf-8") as fh:
        data = json.load(fh)

    print("Building tables...")
    doc = build_doc(data)
    doc.write(out_path)
    print(f"✓ Tables written to: {out_path}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="WFR Table Generator")
    parser.add_argument("--json", type=Path, help="Path to wfr_results.json")
    parser.add_argument("--out",  type=Path, help="Output markdown path")
    args = parser.parse_args()
    main(json_path=args.json, out_path=args.out)
