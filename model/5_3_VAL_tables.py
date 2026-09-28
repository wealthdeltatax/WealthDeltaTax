"""
VAL Output Script A — Full Appendix C Tables (v2 — data-driven)
================================================================
Generates VAL_AppC_Full_Tables.md

All simulation data is loaded from OUTPUTS/VAL/val_data.json
(produced by val_core.py). This script contains no simulation calls:
it is pure formatting and markdown assembly.

To regenerate output:
    python val_core.py          # run simulations
    python 5_3_VAL_tables.py   # render tables

If val_data.json is current (parameters unchanged) you can re-run
this script alone to adjust formatting without re-running simulations.
"""

from pathlib import Path

from val_core import load_val_data
from wdt_fmt import fmt_pct as pct_str, out_dir, ensure_dir
from wdt_md import md_table, pct_table

_OUT = out_dir('VAL')

# ─────────────────────────────────────────────────────────────
# HELPERS — restore typed dicts from JSON string keys
# ─────────────────────────────────────────────────────────────

def _rekey_float(d: dict) -> dict:
    """Restore float-keyed dicts from string-keyed JSON objects."""
    return {float(k): v for k, v in d.items()}


# _build_pct_table — unchanged alias for the wdt_md function
_build_pct_table = pct_table


# ─────────────────────────────────────────────────────────────
# C.11 — MARKDOWN WRITER  (logic unchanged; data now from JSON)
# ─────────────────────────────────────────────────────────────

def write_c11_md(tables, p, over_vals, g_vals, g_labels):
    """Format C.11 as markdown section.  data comes from val_data['tables']."""
    N  = p['N_demo']
    k  = p['k']
    V0 = p['V0_m']

    c11a = _rekey_float(tables['c11a'])
    c11b = _rekey_float(tables['c11b'])
    c11c = _rekey_float(tables['c11c'])
    c11d = _rekey_float(tables['c11d'])
    c11e = _rekey_float(tables['c11e'])
    ep   = _rekey_float(tables['c11_ep'])

    lines = []
    lines.append("## C.11 Overstater TW Advantage Decomposition")
    lines.append("")
    lines.append(
        "**Purpose:** Identifies the three mechanical sources of the "
        "overstater TW advantage shown in C.8. For each ($\\alpha$, $g$) cell the "
        "TW advantage relative to honest declaration is split into: "
        "(1) excess periodic net tax paid during the holding period, "
        "(2) the sell-year settlement delta, and "
        "(3) the post-sale oscillation delta. "
        "These three terms sum to the C.8 figure (sign-adjusted). "
        "An additional sub-table shows $f_N$ — the retained equity fraction "
        "at end of holding period — as a ratio to the honest declarer's "
        "$f_N$, quantifying the dilution cost of overstatement."
    )
    lines.append("")
    lines.append(
        "**Identity (corrected):** TW_settled($\\alpha$) $-$ TW_settled(1) "
        "$=$ W_sell_delta $-$ RefundDelta $-$ SettleDelta  "
        "(verified to machine precision across all tested $(\\alpha, g)$ pairs).  "
        "W_sell_delta $\\leq 0$: f_N erosion reduces sell-year proceeds.  "
        "RefundDelta $\\leq 0$: overstater receives a larger sell-year refund.  "
        "SettleDelta $\\geq 0$: post-sale oscillation taxes back part of the refund.  "
        "Note: ExcessPeriodic (holding-period net tax difference) is **not** additive "
        "in this identity — it feeds into TW_advantage indirectly through f_N erosion "
        "and is shown in C.11.1 for reference only."
    )
    lines.append("")
    lines.append(
        f"**Scope:** Overstaters only ($\\alpha$ ≥ 1.0). "
        f"All values at canonical N = {N}, $k$ = {k}, "
        f"$V_0$ = £{V0:.0f}m. "
        f"Rows = $\\alpha$; columns = $g$ (same grid as C.1). "
        f"Sub-tables C.11.1–C.11.4 expressed as % of TW_settled(1); "
        f"C.11.5 is dimensionless."
    )
    lines.append("")

    headers = ['$\\alpha$ \\ $g$'] + g_labels

    # ── C.11.1 ───────────────────────────────────────────────
    lines.append("### C.11.1 — W_sell_delta as % of Honest TW_settled  [Additive Term 1]")
    lines.append("")
    lines.append(
        "**Formula:** (W_sell($\\alpha$) $-$ W_sell(1)) / TW_settled(1)  "
        "$\\leq 0$ for $\\alpha > 1$.  "
        "W_sell $= f_N \\times V_{sell}$; the overstater's f_N is depleted faster "
        "by higher periodic tax, reducing the sell-year declared value.  "
        "This is the f_N erosion cost of overstatement: the overstater owns a "
        "smaller fraction of the asset at sale.  "
        "Note: ExcessPeriodic (holding-period net tax difference) is related but "
        "**not** equal to W_sell_delta — the excess periodic tax is approximately "
        "6× larger than |W_sell_delta| at canonical parameters because most of "
        "the excess is returned via the sell-year refund (C.11.2).  "
        "ExcessPeriodic is shown separately in C.11.6 for reference."
    )
    lines.append("")
    rows = [[f"**{a}**"] + c11a[a] for a in over_vals]
    lines.append(md_table(headers, rows, fmt_fn=lambda v: pct_str(v, 2)))
    lines.append("")
    lines.append(
        f"Table C.11.1: W_sell_delta as % of honest TW_settled (additive term 1). "
        f"Always $\\leq 0$ for $\\alpha > 1$: f_N erosion reduces sell-year proceeds. "
        f"$V_0$ = £{V0:.0f}m, $k$ = {k}, N = {N}."
    )
    lines.append("")
    lines.append(
        "*Always $\\leq 0$ for $\\alpha > 1$: the overstater surrenders more equity "
        "as periodic tax, depressing the sell-year declared value.  "
        "The magnitude grows with both $\\alpha$ and $g$ but is much smaller than "
        "the refund benefit (C.11.2) — this is why the net TW advantage (C.11.4) "
        "remains positive across the tested range.*"
    )
    lines.append("")

    # ── C.11.2 ───────────────────────────────────────────────
    lines.append("### C.11.2 — Sell-Year Settlement Delta as % of Honest TW_settled")
    lines.append("")
    lines.append(
        "**Formula:** ($L_{sell}$($\\alpha$) $-$ $L_{sell}$(1)) / TW_settled(1)  "
        "· Negative = overstater receives a larger refund (or smaller tax) at sale. "
        "The declared basis at sale always exceeds true proceeds for $\\alpha$ > 1 at any "
        "finite $g$, generating a refund that partially offsets the periodic cost."
    )
    lines.append("")
    rows = [[f"**{a}**"] + c11b[a] for a in over_vals]
    lines.append(md_table(headers, rows, fmt_fn=lambda v: pct_str(v, 2)))
    lines.append("")
    lines.append(
        f"Table C.11.2: Sell-year settlement delta as % of honest TW_settled. "
        f"Negative = overstater received a larger refund at sale. "
        f"$V_0$ = £{V0:.0f}m, $k$ = {k}, N = {N}."
    )
    lines.append("")
    lines.append(
        "*Negative throughout (refund benefit) for all $\\alpha$ > 1. "
        "Magnitude grows with $\\alpha$ but is bounded by the lifetime cap. "
        "At high $g$ the honest declarer also pays a large sell-year tax, "
        "compressing the relative benefit.*"
    )
    lines.append("")

    # ── C.11.3 ───────────────────────────────────────────────
    lines.append("### C.11.3 — Post-Sale Settlement Delta as % of Honest TW_settled")
    lines.append("")
    lines.append(
        "**Formula:** (net_settle_tax($\\alpha$) $-$ net_settle_tax(1)) / TW_settled(1)  "
        "· Positive = the post-sale oscillation taxes back more of the "
        "overstater's sell-year refund than it does for the honest declarer. "
        "This is the damping cost: a larger sell-year refund creates a larger "
        "positive delta in the first post-sale period, which is taxed back."
    )
    lines.append("")
    rows = [[f"**{a}**"] + c11c[a] for a in over_vals]
    lines.append(md_table(headers, rows, fmt_fn=lambda v: pct_str(v, 2)))
    lines.append("")
    lines.append(
        f"Table C.11.3: Post-sale settlement delta as % of honest TW_settled. "
        f"Positive = oscillation recovered more from overstater's refund. "
        f"$V_0$ = £{V0:.0f}m, $k$ = {k}, N = {N}."
    )
    lines.append("")
    lines.append(
        "*Positive throughout for $\\alpha$ > 1: the settle_tw() oscillation always "
        "recovers some of the sell-year refund via subsequent tax. "
        "The damping cost is smaller than the refund benefit (C.11.2) in all "
        "tested cases — the net refund position remains favourable.*"
    )
    lines.append("")

    # ── C.11.4 ───────────────────────────────────────────────
    lines.append("### C.11.4 — Total TW Advantage as % of Honest TW_settled (Cross-Check)")
    lines.append("")
    lines.append(
        "**Formula:** (TW_settled($\\alpha$) $-$ TW_settled(1)) / TW_settled(1)  "
        "· Should equal C.8 at the canonical N column. "
        "Values here are computed from the full decomposition and serve as "
        "an internal consistency check on C.11.1–C.11.3."
    )
    lines.append("")
    rows = [[f"**{a}**"] + c11d[a] for a in over_vals]
    lines.append(md_table(headers, rows, fmt_fn=lambda v: pct_str(v, 2)))
    lines.append("")
    lines.append(
        f"Table C.11.4: Total TW advantage as % of honest TW_settled. "
        f"Should match C.5 (at canonical $k$) and C.8 (at canonical N) for each $\\alpha$. "
        f"$V_0$ = £{V0:.0f}m, $k$ = {k}, N = {N}."
    )
    lines.append("")
    lines.append(
        "*Should match C.5 (at canonical $k$) and C.8 (at canonical N) for each $\\alpha$. "
        "Any discrepancy exceeding 0.01pp indicates a decomposition error.*"
    )
    lines.append("")

    # ── C.11.5 ───────────────────────────────────────────────
    lines.append("### C.11.5 — Retained Equity Fraction Ratio at End of Holding Period")
    lines.append("")
    lines.append(
        "**Formula:** $f_N$($\\alpha$) / $f_N$(1)  · Values below 1.0 indicate the "
        "overstater has surrendered more equity as tax during the holding "
        "period. This is the dilution cost: the overstater owns a smaller "
        "fraction of their asset at sale, which is why the sell-year declared "
        "value ($f_N \\times V_{sell}$) is lower than it would otherwise be."
    )
    lines.append("")
    rows = [[f"**{a}**"] + c11e[a] for a in over_vals]
    lines.append(md_table(headers, rows, fmt_fn=lambda v: f"{v:.4f}"))
    lines.append("")
    lines.append(
        f"Table C.11.5: Retained equity fraction ratio $f_N$($\\alpha$) / $f_N$(1). "
        f"Values below 1.0 = overstater surrendered more equity during holding period. "
        f"$V_0$ = £{V0:.0f}m, $k$ = {k}, N = {N}."
    )
    lines.append("")

    # ── C.11.6 — excess_periodic (informational) ──────────────
    lines.append("### C.11.6 — Excess Periodic Net Tax as % of Honest TW_settled  [Informational]")
    lines.append("")
    lines.append(
        "**Formula:** (Net_holding($\\alpha$) $-$ Net_holding(1)) / TW_settled(1)  "
        "· Positive = overstater paid more net tax during the holding period.  "
        "**This term is NOT additive in the C.11 identity** — it is shown for "
        "reference only."
    )
    lines.append("")
    rows = [[f"**{a}**"] + ep[a] for a in over_vals]
    lines.append(md_table(headers, rows, fmt_fn=lambda v: pct_str(v, 2)))
    lines.append("")
    lines.append(
        f"Table C.11.6: Excess periodic net tax as % of honest TW_settled (informational). "
        f"$V_0$ = £{V0:.0f}m, $k$ = {k}, N = {N}."
    )
    lines.append("")

    return '\n'.join(lines)


# ─────────────────────────────────────────────────────────────
# C.12 — MARKDOWN WRITER
# ─────────────────────────────────────────────────────────────

def write_c12_md(c12_raw, p, alpha_vals, g_vals, g_labels):
    c12 = _rekey_float(c12_raw)
    N   = p['N_demo']
    k   = p['k']
    V0  = p['V0_m']
    rho = p['rho']
    t0  = p['tau_0'] * 100
    tm  = p['tau_m'] * 100

    lines = []
    lines.append("## C.12 NPV-Adjusted Tax Position: Present Value of Tax Difference vs Honest")
    lines.append("")
    lines.append(
        "**Purpose:** Adjusts the C.1 nominal tax-difference metric for the time value of money."
    )
    lines.append("")
    lines.append(
        f"**Metric:** $(NPV_{{tax}}(\\alpha) - NPV_{{tax}}(1))$ / TW_settled(1), "
        f"where $NPV_{{tax}}(\\alpha) = \\sum_{{t=1}}^{{N+1}} L_t / (1+\\rho)^t$ "
        f"and $\\rho = {rho*100:.0f}\\%$."
    )
    lines.append("")
    lines.append(f"$\\frac{{NPV_{{tax}}(\\alpha) - NPV_{{tax}}(1)}}{{TW_{{settled}}(1)}}$")
    lines.append("")
    lines.append(
        "**Sign convention:** Positive = alpha pays more in present-value terms than honest "
        "(understater disadvantage). Negative = alpha pays less in PV terms (overstater advantage). "
        "Same as C.1, so tables are directly comparable."
    )
    lines.append("")
    lines.append(
        f"**Scope:** Full α grid (same as C.1). "
        f"All values at canonical N = {N}, $k$ = {k}, $V_0$ = £{V0:.0f}m, "
        f"$\\rho$ = {rho*100:.0f}%, $\\tau_0$ = {t0:.0f}%, $\\tau_m$ = {tm:.0f}%."
    )
    lines.append("")

    lines.extend(_build_pct_table(alpha_vals, g_labels, c12))
    lines.append("")
    lines.append(
        f"Table C.12: NPV-adjusted tax difference vs honest declaration, as % of honest "
        f"TW_settled. $\\alpha$ = 1.0 row is zero by construction. "
        f"$\\rho$ = {rho*100:.0f}%, $V_0$ = £{V0:.0f}m, $k$ = {k}, N = {N}, "
        f"$\\tau_0$ = {t0:.0f}%, $\\tau_m$ = {tm:.0f}%, $W_{{min}}$ = £{p['W_min']:.0f}m."
    )
    lines.append("")

    return '\n'.join(lines)


# ─────────────────────────────────────────────────────────────
# MAIN MARKDOWN WRITER
# ─────────────────────────────────────────────────────────────

def write_appc_md(data: dict) -> str:
    p       = data['params']
    grids   = data['grids']
    tables  = data['tables']

    G_VALS        = grids['g_vals']
    G_LABELS      = grids['g_labels']
    ALPHA_VALS    = grids['alpha_vals']
    K_VALS        = grids['k_vals']
    V0_VALS       = grids['v0_vals']
    N_ACTUAL_VALS = grids['n_actual_vals']
    OVER_VALS     = grids['over_vals']

    # Restore float-keyed dicts
    t1 = _rekey_float(tables['t1'])
    t2 = _rekey_float(tables['t2'])
    t3 = _rekey_float(tables['t3'])
    t4 = _rekey_float(tables['t4'])
    t5 = _rekey_float(tables['t5'])
    t7 = _rekey_float(tables['t7'])
    t8 = _rekey_float(tables['t8'])
    neg_g_vals   = tables['neg_g_vals']
    neg_g_labels = tables['neg_g_labels']

    N   = p['N_demo']
    k   = p['k']
    t0  = p['tau_0'] * 100
    tm  = p['tau_m'] * 100
    g_p = p['g'] * 100
    V0  = p['V0_m']

    def param_str(extra=''):
        base = (f"$V_0$ = £{V0:.0f}m, $k$ = {k}, N = {N}, "
                f"$\\tau_0$ = {t0:.0f}%, $\\tau_m$ = {tm:.0f}%, "
                f"$W_{{min}}$ = £{p['W_min']:.0f}m")
        return base + (', ' + extra if extra else '')

    lines = []

    # ── Section header ────────────────────────────────────────
    lines.append("# C. WDT Valuation Analysis: Summary Tables {.appendix}")
    lines.append("")
    lines.append(
        f"**Validation status:** All figures from Python model v1.0 "
        f"(standalone, no Excel dependency). "
        f"Parameters unified to $k$ = {k}, N = {N}, $\\tau_0$ = {t0:.0f}%."
    )
    lines.append("")
    lines.append(
        f"Unless otherwise stated, all figures use base parameters: "
        f"$V_0$ = £{V0:.0f}m, N = {N}, $\\tau_0$ = {t0:.0f}%, $\\tau_m$ = {tm:.0f}%, "
        f"$k$ = {k}, $W_{{min}}$ = £{p['W_min']:.0f}m, $g$ = {g_p:.2f}%, $\\alpha$ = 1, β = 0%."
    )
    lines.append("")

    # ── C.1 ──────────────────────────────────────────────────
    lines.append("## C.1 Total Tax Paid (TTP) Difference Relative to Honest Declaration, as Share of Terminal Net Worth (TW)")
    lines.append("")
    lines.append(f"**Metric:** (Net($\\alpha$) − Net(1) / TW($\\alpha$). Positive values indicate $\\alpha$ pays more net tax than honest; negative values indicate less.")
    lines.append("")
    lines.append(f"$\\frac{{Net(\\alpha) - Net(1)}}{{TW(\\alpha)}}$")
    lines.append("")
    lines.append(
        f"**Structural claim:** Understatement is more costly than honest declaration across the "
        f"policy-relevant growth range. The penalty escalates steeply between $g$ ≈ 10% and "
        f"$g$ ≈ 17.3%, then plateaus at a ceiling set by $\\alpha$; the marginal deterrent stops "
        f"escalating but does not reverse."
    )
    lines.append("")
    lines += _build_pct_table(ALPHA_VALS, G_LABELS, t1)
    lines.append("")
    lines.append(
        f"Table C.1: TTP difference relative to honest declaration, as share of TW. "
        f"$\\alpha$ = 1.0 row is zero by construction. {param_str()}."
    )
    lines.append("")

    # ── C.2 ──────────────────────────────────────────────────
    lines.append("## C.2 Effective Lifetime Tax Rate Difference from Honest Declaration")
    lines.append("")
    lines.append(f"**Metric:** Net($\\alpha$)/TW($\\alpha$) − Net(1)/TW(1).")
    lines.append("")
    lines.append(f"$\\frac{{Net(\\alpha)}}{{TW(\\alpha)}} - \\frac{{Net(1)}}{{TW(1)}}$")
    lines.append("")
    lines += _build_pct_table(ALPHA_VALS, G_LABELS, t2)
    lines.append("")
    lines.append(
        f"Table C.2: Effective lifetime tax rate difference from honest declaration. "
        f"$\\alpha$ = 1.0 row is zero by construction. {param_str()}."
    )
    lines.append("")

    # ── C.3 ──────────────────────────────────────────────────
    lines.append("## C.3 Exploratory Extension: Investor Confidence Effects β (Overstatement Only)")
    lines.append("")
    lines.append(f"*This section is exploratory. β swept over same values as $g$ columns; $g$ fixed at {g_p:.2f}%.*")
    lines.append("")
    lines.append(f"$\\frac{{Net(\\alpha, \\beta) - Net(1, \\beta=0)}}{{TW(\\alpha, \\beta)}}$")
    lines.append("")
    beta_labels = [f"β={g * 100:.1f}%" for g in G_VALS]
    lines += _build_pct_table(OVER_VALS, beta_labels, t3, row_label='$\\alpha$ \\ β')
    lines.append("")
    lines.append(
        f"Table C.3: Investor confidence β sensitivity (overstatement only). "
        f"$g$ fixed at {g_p:.2f}%, N={N} throughout. "
        f"$V_0$ = £{V0:.0f}m, $k$ = {k}, $\\tau_0$ = {t0:.0f}%, $\\tau_m$ = {tm:.0f}%, $W_{{min}}$ = £{p['W_min']:.0f}m."
    )
    lines.append("")

    # ── C.4 ──────────────────────────────────────────────────
    lines.append("## C.4 Effective Lifetime Tax Rate by $k$ Parameter and Initial Wealth ($V_0$)")
    lines.append("")
    lines.append(f"**Metric:** TTP($\\alpha$=1) / TW($\\alpha$=1). Rows = k; columns = $V_0$ (£m).")
    lines.append("")
    lines.append(f"$\\frac{{TTP(\\alpha=1)}}{{TW(\\alpha=1)}}$")
    lines.append("")
    v0_labels = [f"£{v}m" for v in V0_VALS]
    k_row_label = '$k$ \\ $V_0$'
    h4 = [k_row_label] + v0_labels
    lines.append('| ' + ' | '.join(h4) + ' |')
    lines.append('|' + '|'.join(':---:' for _ in h4) + '|')
    for k_val in K_VALS:
        cells = [f'{k_val:.0e}'] + [pct_str(v, 2) for v in t4[k_val]]
        lines.append('| ' + ' | '.join(cells) + ' |')
    lines.append("")
    lines.append(
        f"Table C.4: Effective lifetime tax rate by $k$ and $V_0$. "
        f"All at $\\alpha$=1, β=0, $g$={g_p:.2f}%, N={N}."
    )
    lines.append("")

    # ── C.5 ──────────────────────────────────────────────────
    lines.append("## C.5 Sensitivity of $k$ and Alpha: Terminal Net Worth Difference vs Honest")
    lines.append("")
    lines.append(f"**Metric:** (TW($\\alpha$,k) − TW(1,k) / TW(1,k).")
    lines.append("")
    lines.append(f"$\\frac{{TW(\\alpha,k) - TW(1,k)}}{{TW(1,k)}}$")
    lines.append("")
    k_labels = [f'{kv:.0e}' for kv in K_VALS]
    lines += _build_pct_table(ALPHA_VALS, k_labels, t5, row_label='$\\alpha$ \\ $k$')
    lines.append("")
    lines.append(
        f"Table C.5: TW difference vs honest, by $k$ and $\\alpha$. "
        f"$\\alpha$ = 1.0 row is zero by construction. $g$ = {g_p:.2f}%, N = {N} throughout."
    )
    lines.append("")

    # ── C.6 ──────────────────────────────────────────────────
    lines.append("## C.6 Terminal Net Worth After Refunds: Refund Protection Ratio")
    lines.append("")
    lines.append(f"**Metric:** TW($\\alpha$) / TW(1). Negative $g$ scenarios only.")
    lines.append("")
    lines.append(f"$\\frac{{TW(\\alpha)}}{{TW(1)}}$")
    lines.append("")
    t6_neg = _rekey_float(tables['t6'])
    lines += _build_pct_table(ALPHA_VALS, neg_g_labels, t6_neg)
    lines.append("")
    lines.append(
        f"Table C.6: Refund protection ratio vs honest declaration. "
        f"Negative $g$ scenarios only. $\\alpha$ = 1.0 is 100% by construction. "
        f"{param_str()}."
    )
    lines.append("")

    # ── C.7 ──────────────────────────────────────────────────
    lines.append("## C.7 Total Tax Paid Compared to Honest Taxpayer, Adjusted for N")
    lines.append("")
    lines.append(f"**Metric:** (Net($\\alpha$,N) − Net(1,N) / Net(1,N).")
    lines.append("")
    lines.append(f"$\\frac{{Net(\\alpha,N) - Net(1,N)}}{{Net(1,N)}}$")
    lines.append("")
    n_labels = [str(n) for n in N_ACTUAL_VALS]
    lines += _build_pct_table(ALPHA_VALS, n_labels, t7, row_label='$\\alpha$ \\ N')
    lines.append("")
    lines.append(
        f"Table C.7: Net tax compared to honest taxpayer, adjusted for N. "
        f"$\\alpha$ = 1.0 row is zero by construction. $g$ = {g_p:.2f}% throughout. "
        f"{param_str()}."
    )
    lines.append("")

    # ── C.8 ──────────────────────────────────────────────────
    lines.append("## C.8 Terminal Net Worth Compared to Honest Taxpayer, Adjusted for N")
    lines.append("")
    lines.append(f"**Metric:** (TW($\\alpha$,N) − TW(1,N) / TW(1,N).")
    lines.append("")
    lines.append(f"$\\frac{{TW(\\alpha,N) - TW(1,N)}}{{TW(1,N)}}$")
    lines.append("")
    lines += _build_pct_table(ALPHA_VALS, n_labels, t8, row_label='$\\alpha$ \\ N')
    lines.append("")
    lines.append(
        f"Table C.8: TW compared to honest taxpayer, adjusted for N. "
        f"$\\alpha$ = 1.0 row is zero by construction. $g$ = {g_p:.2f}% throughout. "
        f"{param_str()}."
    )
    lines.append("")

    # ── C.9 ──────────────────────────────────────────────────
    lines.append("## C.9 Summary of Declaration Incentives Across Growth Regimes")
    lines.append("")
    lines.append(f"**Metric:** TW(£m) and Net tax (£m) at $\\alpha$ ∈ {{2.0, 1.0, 0.1}} across the $g$ sweep. N = {N} throughout.")
    lines.append("")
    h9 = ['$g$', 'TW($\\alpha$=2) £m', 'TW($\\alpha$=1) £m', 'TW($\\alpha$=0.1) £m',
          'Net($\\alpha$=2) £m', 'Net($\\alpha$=1) £m', 'Net($\\alpha$=0.1) £m',
          'TW(0.1)/TW(1)', 'Net(0.1)/Net(1)']
    lines.append('| ' + ' | '.join(h9) + ' |')
    lines.append('|' + '|'.join(':---:' for _ in h9) + '|')
    for row in tables['t9']:
        g_disp = f"{row['g']*100:.1f}%"
        tw_r   = f"{row['TW_a01']/row['TW_a1']*100:.1f}%" if abs(row['TW_a1']) > 1e-12 else "—"
        net_r  = (f"{row['Net_a01']/row['Net_a1']*100:.1f}%"
                  if row['refund_ratio'] is not None else "—")
        lines.append(
            f"| {g_disp} | {row['TW_a2']:.1f} | {row['TW_a1']:.1f} | {row['TW_a01']:.1f} | "
            f"{row['Net_a2']:.1f} | {row['Net_a1']:.1f} | {row['Net_a01']:.1f} | "
            f"{tw_r} | {net_r} |"
        )
    lines.append("")
    lines.append(
        f"Table C.9: Summary of declaration incentives across growth regimes. "
        f"TW and Net tax in £m. N = {N} throughout. {param_str()}."
    )
    lines.append("")

    # ── C.10 ─────────────────────────────────────────────────
    scen_year = data['meta']['scenario_start_year']
    lines.append("## C.10 Historical Return Series — Reference Scenario Results")
    lines.append("")
    lines.append(
        f"**Source:** RATES Balanced worst-case reference scenario "
        f"(returns rotated to {scen_year} start year). "
        f"$V_0$ = £{V0:.0f}m, $\\tau_0$ = {t0:.0f}%, $\\tau_m$ = {tm:.0f}%, $k$ = {k}, "
        f"$W_{{min}}$ = £{p['W_min']:.0f}m. No β adjustment applied."
    )
    lines.append("")

    lines.append(f"### C.10.1 Declaration strategy comparison ($\\alpha$ sweep, N = {N})")
    lines.append("")
    h10a = ['$\\alpha$', 'TW (£m)', 'TTP (£m)', 'Net (£m)', 'Eff rate', 'TW vs honest', 'Net vs honest']
    lines.append('| ' + ' | '.join(h10a) + ' |')
    lines.append('|' + '|'.join(':---:' for _ in h10a) + '|')
    for row in tables['t10_alpha']:
        marker = ' ← honest' if row['alpha'] == 1.0 else ''
        lines.append(
            f"| **{row['alpha']}** | {row['TW']:.2f} | {row['TTP']:.2f} | {row['Net']:.2f} | "
            f"{row['eff_rate']*100:.2f}% | {row['tw_vs_honest']*100:+.2f}% | "
            f"{row['net_vs_honest']*100:+.2f}%{marker} |"
        )
    lines.append("")
    lines.append(
        f"Table C.10.1: Declaration strategy comparison, {scen_year} historical return series, N = {N}."
    )
    lines.append("")

    lines.append(f"### C.10.2 Honest declarer trajectory by N ($\\alpha$ = 1.0)")
    lines.append("")
    h10b = ['N', 'TW (£m)', 'Net (£m)', 'Mean $g$ of series[:N]']
    lines.append('| ' + ' | '.join(h10b) + ' |')
    lines.append('|' + '|'.join(':---:' for _ in h10b) + '|')
    for row in tables['t10_n']:
        is_ref = row['N'] == N
        n_str  = f"**{row['N']}**"  if is_ref else str(row['N'])
        tw_str = f"**{row['TW']:.2f}**"  if is_ref else f"{row['TW']:.2f}"
        net_str = f"**{row['Net']:.2f}**" if is_ref else f"{row['Net']:.2f}"
        g_str  = f"**{row['g_mean']*100:.2f}%**" if is_ref else f"{row['g_mean']*100:.2f}%"
        lines.append(f"| {n_str} | {tw_str} | {net_str} | {g_str} |")
    lines.append("")
    lines.append(f"Table C.10.2: Honest declarer trajectory under {scen_year} historical return series.")
    lines.append("")

    # ── C.11 ─────────────────────────────────────────────────
    lines.append(write_c11_md(tables, p, OVER_VALS, G_VALS, G_LABELS))

    # ── C.12 ─────────────────────────────────────────────────
    lines.append(write_c12_md(tables['c12'], p, ALPHA_VALS, G_VALS, G_LABELS))

    return '\n'.join(lines)


# ─────────────────────────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────────────────────────

def main():
    print("5_3_VAL_tables.py — loading val_data.json...")
    data = load_val_data()
    print(f"Data loaded. Generated: {data['meta']['generated']}")

    print("Formatting markdown (VAL.A §C format)...")
    md = write_appc_md(data)

    ensure_dir(_OUT)
    out_path = _OUT / "VAL_AppC_Full_Tables.md"
    out_path.write_text(md, encoding="utf-8")
    print(f"Written: {out_path}")
    print(f"Lines: {len(md.splitlines())}")


if __name__ == '__main__':
    main()
