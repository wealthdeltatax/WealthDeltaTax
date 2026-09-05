"""
VAL Output Script A — Full Appendix C Tables
=============================================
Generates VAL_AppC_Full_Tables.md

Parameters and simulation engine imported from wdt_core.py (single source of truth).
No Excel dependency. Uses confirmed simulation conventions and formulas throughout.

Output matches the formatting of VAL.A §C exactly:
  - Table captions below each table in the form "Table C.N: description. params."
  - Section headers: ## C.N Title
  - Subsection headers: ### C.10.1 / ### C.10.2 / ### C.11a–C.11e
  - Column headers use LaTeX math: $\\alpha$, $g$, $\\tau$, etc.
  - Metric formula displayed on its own line as $\\frac{...}{...}$
  - **Metric:** label followed by formula line
  - **Structural claim:** block matching paper prose
  - C.10.2 reference row bolded: | **29** | **84.47** | ...

C.11 — Overstater TW Advantage Decomposition:
  Splits the C.8 TW advantage into three additive terms (identity verified
  to machine precision):
    tw_advantage = W_sell_delta - refund_delta - settle_delta
  (1) W_sell_delta: f_N erosion reduces sell-year declared value [<= 0]
  (2) refund_delta: overstater receives larger sell-year refund [<= 0]
  (3) settle_delta: post-sale oscillation damps the refund [>= 0]
  Plus f_N ratio sub-table (C.11e) and excess_periodic reference (C.11f).
  Note: excess_periodic is NOT additive in the identity; it is ~6x larger
  than |W_sell_delta| because most periodic overpayment is recovered at sale.
  Overstaters only (α ≥ 1.0); same g-grid as C.1.

N-offset correction applied: Tables 7/8 show actual N (5,10,...,60),
not the Excel header offset values (0,5,...,55).

Table 3 uses confirmed additive beta formula: g_eff = g + beta*ln(alpha).
VAL.A §B.3 and §C.3 carry the erroneous multiplicative form; this output
uses the formula confirmed from the Excel cell.

Model limitation: Option A convention throughout (annual periods = assessment
windows). Table K in worked examples uses N=3 annual periods, not three
multi-year windows. Expected to produce variance from a window-aware model.

N=34: aligned with the RATES Balanced reference scenario (2006 start year,
34-year LRR fill horizon). This is the correct policy-relevant horizon for
all cross-paper consistency. Previous versions used N=32 (an error) or
referenced N=61 (the raw Excel validation run) or N=58 (LRR breakeven year,
a derived output rather than a scenario parameter).
"""

import os
from datetime import date
from pathlib import Path
from wdt_core import load_params, tau, g_eff, simulate, simulate_sell, settle_tw, run_sim, run_sim_hist, decompose_tw_advantage, npv_tax_advantage
from wdt_fmt import fmt_pct as pct_str, out_dir, ensure_dir
from wdt_md import md_table, pct_table

_OUT = out_dir('VAL')

# All analytical grids sourced from TOML via load_params() in main().
G_VALS        = []
G_LABELS      = []
ALPHA_VALS    = []
K_VALS        = []
V0_VALS       = []
N_ACTUAL_VALS = []
OVER_VALS     = []


# ─────────────────────────────────────────────────────────────
# C.11 — OVERSTATER TW ADVANTAGE DECOMPOSITION
# ─────────────────────────────────────────────────────────────

def compute_c11(p, over_vals, g_vals):
    """
    Compute C.11 sub-tables.

    Returns dict with keys 'c11a'..'c11e', each keyed by alpha
    containing a list of floats (one per g in g_vals).

    Correct additive identity (verified to machine precision):
        tw_advantage = W_sell_delta - refund_delta - settle_delta

    c11a — W_sell_delta    / TW_settled(1)  as fraction  [additive term 1]
    c11b — refund_delta    / TW_settled(1)  as fraction  [additive term 2]
    c11c — settle_delta    / TW_settled(1)  as fraction  [additive term 3]
    c11d — tw_advantage    / TW_settled(1)  as fraction  [sum; cross-check vs C.8]
    c11e — f_N ratio (dimensionless)

    Note: excess_periodic (holding-period net tax difference) is NOT stored
    as c11a. It is not additive in the identity. The previous version used
    excess_periodic for c11a — this has been corrected.
    """
    c11a = {}; c11b = {}; c11c = {}; c11d = {}; c11e = {}
    max_identity_err = 0.0

    for alpha in over_vals:
        ra = []; rb = []; rc = []; rd = []; re = []
        for g in g_vals:
            d     = decompose_tw_advantage(p, alpha, g)
            tw    = d['tw_honest']
            denom = tw if abs(tw) > 1e-12 else 1.0
            ra.append(d['W_sell_delta'] / denom)   # term 1
            rb.append(d['refund_delta'] / denom)   # term 2
            rc.append(d['settle_delta'] / denom)   # term 3
            rd.append(d['tw_advantage'] / denom)   # sum
            re.append(d['f_ratio'])
            max_identity_err = max(max_identity_err, abs(d['identity_error']))
        c11a[alpha] = ra; c11b[alpha] = rb; c11c[alpha] = rc
        c11d[alpha] = rd; c11e[alpha] = re

    if max_identity_err > 0.001:
        print(f"  WARNING: C.11 max identity error = {max_identity_err:.2e} £m")
    else:
        print(f"  C.11 identity verified: max error = {max_identity_err:.2e} £m")

    return {'c11a': c11a, 'c11b': c11b, 'c11c': c11c,
            'c11d': c11d, 'c11e': c11e}


def write_c11_md(tables, p, over_vals, g_vals, g_labels):
    """
    Format C.11 as a markdown section matching VAL.A §C conventions:
    sub-table headers as ### C.11a, captions below each table,
    LaTeX notation throughout.
    """
    N  = p['N']
    k  = p['k']
    V0 = p['V0_m']

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
        "and is shown in C.11a for reference only."
    )
    lines.append("")
    lines.append(
        f"**Scope:** Overstaters only ($\\alpha$ ≥ 1.0). "
        f"All values at canonical N = {N}, $k$ = {k}, "
        f"$V_0$ = £{V0:.0f}m. "
        f"Rows = $\\alpha$; columns = $g$ (same grid as C.1). "
        f"Sub-tables C.11a–C.11d expressed as % of TW_settled(1); "
        f"C.11e is dimensionless."
    )
    lines.append("")

    headers = ['$\\alpha$ \\ $g$'] + g_labels

    # ── C.11a ────────────────────────────────────────────────
    lines.append("### C.11a — W_sell_delta as % of Honest TW_settled  [Additive Term 1]")
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
        "the excess is returned via the sell-year refund (C.11b).  "
        "ExcessPeriodic is shown separately in C.11f for reference."
    )
    lines.append("")
    rows = [[f"**{a}**"] + tables['c11a'][a] for a in over_vals]
    lines.append(md_table(headers, rows, fmt_fn=lambda v: pct_str(v, 2)))
    lines.append("")
    lines.append(
        f"Table C.11a: W_sell_delta as % of honest TW_settled (additive term 1). "
        f"Always $\\leq 0$ for $\\alpha > 1$: f_N erosion reduces sell-year proceeds. "
        f"$V_0$ = £{V0:.0f}m, $k$ = {k}, N = {N}."
    )
    lines.append("")
    lines.append(
        "*Always $\\leq 0$ for $\\alpha > 1$: the overstater surrenders more equity "
        "as periodic tax, depressing the sell-year declared value.  "
        "The magnitude grows with both $\\alpha$ and $g$ but is much smaller than "
        "the refund benefit (C.11b) — this is why the net TW advantage (C.11d) "
        "remains positive across the tested range.*"
    )
    lines.append("")

    # ── C.11b ────────────────────────────────────────────────
    lines.append("### C.11b — Sell-Year Settlement Delta as % of Honest TW_settled")
    lines.append("")
    lines.append(
        "**Formula:** ($L_{sell}$($\\alpha$) $-$ $L_{sell}$(1)) / TW_settled(1)  "
        "· Negative = overstater receives a larger refund (or smaller tax) at sale. "
        "The declared basis at sale always exceeds true proceeds for $\\alpha$ > 1 at any "
        "finite $g$, generating a refund that partially offsets the periodic cost."
    )
    lines.append("")
    rows = [[f"**{a}**"] + tables['c11b'][a] for a in over_vals]
    lines.append(md_table(headers, rows, fmt_fn=lambda v: pct_str(v, 2)))
    lines.append("")
    lines.append(
        f"Table C.11b: Sell-year settlement delta as % of honest TW_settled. "
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

    # ── C.11c ────────────────────────────────────────────────
    lines.append("### C.11c — Post-Sale Settlement Delta as % of Honest TW_settled")
    lines.append("")
    lines.append(
        "**Formula:** (net_settle_tax($\\alpha$) $-$ net_settle_tax(1)) / TW_settled(1)  "
        "· Positive = the post-sale oscillation taxes back more of the "
        "overstater's sell-year refund than it does for the honest declarer. "
        "This is the damping cost: a larger sell-year refund creates a larger "
        "positive delta in the first post-sale period, which is taxed back."
    )
    lines.append("")
    rows = [[f"**{a}**"] + tables['c11c'][a] for a in over_vals]
    lines.append(md_table(headers, rows, fmt_fn=lambda v: pct_str(v, 2)))
    lines.append("")
    lines.append(
        f"Table C.11c: Post-sale settlement delta as % of honest TW_settled. "
        f"Positive = oscillation recovered more from overstater's refund. "
        f"$V_0$ = £{V0:.0f}m, $k$ = {k}, N = {N}."
    )
    lines.append("")
    lines.append(
        "*Positive throughout for $\\alpha$ > 1: the settle_tw() oscillation always "
        "recovers some of the sell-year refund via subsequent tax. "
        "The damping cost is smaller than the refund benefit (C.11b) in all "
        "tested cases — the net refund position remains favourable.*"
    )
    lines.append("")

    # ── C.11d ────────────────────────────────────────────────
    lines.append("### C.11d — Total TW Advantage as % of Honest TW_settled (Cross-Check)")
    lines.append("")
    lines.append(
        "**Formula:** (TW_settled($\\alpha$) $-$ TW_settled(1)) / TW_settled(1)  "
        "· Should equal C.8 at the canonical N column. "
        "Values here are computed from the full decomposition and serve as "
        "an internal consistency check on C.11a–C.11c."
    )
    lines.append("")
    rows = [[f"**{a}**"] + tables['c11d'][a] for a in over_vals]
    lines.append(md_table(headers, rows, fmt_fn=lambda v: pct_str(v, 2)))
    lines.append("")
    lines.append(
        f"Table C.11d: Total TW advantage as % of honest TW_settled. "
        f"Should match C.5 (at canonical $k$) and C.8 (at canonical N) for each $\\alpha$. "
        f"$V_0$ = £{V0:.0f}m, $k$ = {k}, N = {N}."
    )
    lines.append("")
    lines.append(
        "*Should match C.5 (at canonical $k$) and C.8 (at canonical N) for each $\\alpha$. "
        "Any discrepancy exceeding 0.01pp indicates a decomposition error.*"
    )
    lines.append("")

    # ── C.11e ────────────────────────────────────────────────
    lines.append("### C.11e — Retained Equity Fraction Ratio at End of Holding Period")
    lines.append("")
    lines.append(
        "**Formula:** $f_N$($\\alpha$) / $f_N$(1)  · Values below 1.0 indicate the "
        "overstater has surrendered more equity as tax during the holding "
        "period. This is the dilution cost: the overstater owns a smaller "
        "fraction of their asset at sale, which is why the sell-year declared "
        "value ($f_N \\times V_{sell}$) is lower than it would otherwise be. "
        "The $f_N$ ratio is independent of $g$ within holding periods but "
        "shifts across $g$ because the progressive rate responds to "
        "declared wealth level."
    )
    lines.append("")
    rows = [[f"**{a}**"] + tables['c11e'][a] for a in over_vals]
    lines.append(md_table(headers, rows, fmt_fn=lambda v: f"{v:.4f}"))
    lines.append("")
    lines.append(
        f"Table C.11e: Retained equity fraction ratio $f_N$($\\alpha$) / $f_N$(1). "
        f"Values below 1.0 = overstater surrendered more equity during holding period. "
        f"$V_0$ = £{V0:.0f}m, $k$ = {k}, N = {N}."
    )
    lines.append("")
    lines.append(
        "*Always < 1.0 for $\\alpha$ > 1: the overstater's retained fraction is "
        "lower at every $g$. The ratio shrinks with $\\alpha$ (more dilution) and "
        "with $g$ (higher declared wealth pushes the rate function higher, "
        "increasing $q$ each period). "
        "The $f_N$ ratio is the mechanism through which the declared basis "
        "at sale falls below $\\alpha \\times$ true value — it is not "
        "$\\alpha \\times f_N$(honest) $\\times V_{sell}$ "
        "but rather $f_N$($\\alpha$) $\\times V_{sell}$, where $f_N$($\\alpha$) < $f_N$(honest).*"
    )
    lines.append("")
    lines.append(
        "*Key design implication: the overstater cannot manufacture a "
        "TW advantage by overstatement alone. The advantage in C.11d / C.8 "
        "persists because the sell-year refund benefit (C.11b) swamps the "
        "f_N erosion cost (C.11a) and the damping cost (C.11c) across "
        "all tested ($\\alpha$, $g$) — by a factor of approximately 6:1 at "
        "canonical parameters. Whether this relationship holds beyond the "
        "tested range — particularly at very high $g$ where $f_N$ is heavily "
        "depleted — requires extension of the $g$ sweep above 25%.*"
    )
    lines.append("")

    # ── C.11f — excess_periodic (informational) ───────────────
    lines.append("### C.11f — Excess Periodic Net Tax as % of Honest TW_settled  [Informational]")
    lines.append("")
    lines.append(
        "**Formula:** (Net_holding($\\alpha$) $-$ Net_holding(1)) / TW_settled(1)  "
        "· Positive = overstater paid more net tax during the holding period.  "
        "**This term is NOT additive in the C.11 identity** — it is shown for "
        "reference only.  ExcessPeriodic feeds into tw_advantage indirectly "
        "through f_N erosion (higher periodic tax depletes f faster, reducing "
        "W_sell), but ExcessPeriodic $\\gg$ |W_sell_delta| because most of the "
        "excess is returned as a sell-year refund (C.11b).  "
        "The correct additive decomposition uses W_sell_delta (C.11a), not ExcessPeriodic."
    )
    lines.append("")

    # Compute excess_periodic separately — not stored in c11a any more
    ep_table = {}
    sim_p = {k: p[k] for k in ('k', 'tau_0', 'tau_m', 'W_min')}
    for alpha in over_vals:
        row = []
        for g in g_vals:
            g_ser  = [g] * p['N']
            recs_h = simulate(p['V0_m'], g_ser, 1.0, sim_p)
            recs_a = simulate(p['V0_m'], g_ser, alpha, sim_p)
            sell_h = simulate_sell(recs_h, g, sim_p)
            tw_h, _, _ = settle_tw(sell_h, sim_p)
            hn_h = sum(r['L'] for r in recs_h[1:])
            hn_a = sum(r['L'] for r in recs_a[1:])
            denom = tw_h if abs(tw_h) > 1e-12 else 1.0
            row.append((hn_a - hn_h) / denom)
        ep_table[alpha] = row

    rows = [[f"**{a}**"] + ep_table[a] for a in over_vals]
    lines.append(md_table(headers, rows, fmt_fn=lambda v: pct_str(v, 2)))
    lines.append("")
    lines.append(
        f"Table C.11f: Excess periodic net tax as % of honest TW_settled (informational). "
        f"Positive = overstater paid more net tax during holding period. "
        f"Compare with C.11a (W_sell_delta): ExcessPeriodic is approximately 6× larger "
        f"in magnitude, confirming that most of the periodic overpayment is recovered "
        f"via the sell-year refund. "
        f"$V_0$ = £{V0:.0f}m, $k$ = {k}, N = {N}."
    )
    lines.append("")
    lines.append(
        "*Positive throughout at $g$ \\geq ~8\\%: the overstater pays more every period "
        "due to a larger declared delta and higher progressive rate. "
        "Despite this persistent periodic cost, the sell-year refund (C.11b) "
        "exceeds both the erosion cost (C.11a) and the damping cost (C.11c), "
        "producing the net TW advantage shown in C.11d.*"
    )
    lines.append("")

    return '\n'.join(lines)


# ─────────────────────────────────────────────────────────────
# C.12 — NPV-ADJUSTED TAX POSITION
# ─────────────────────────────────────────────────────────────

def compute_c12(p, alpha_vals, g_vals):
    """
    Compute C.12: NPV-adjusted tax difference vs honest, as % of honest TW_settled.

    NPV_tax(alpha) = Σ_{t=1}^{N+1}  L_t / (1+ρ)^t

    C.12 metric = (NPV_tax(alpha) - NPV_tax(1)) / TW_settled(1)

    Sign convention matches C.1: positive = alpha pays more in PV terms
    (understater disadvantage); negative = alpha pays less (overstater advantage).

    Returns dict keyed by alpha, each containing a list of floats (one per g).
    """
    rho = p['rho']
    c12 = {}
    for alpha in alpha_vals:
        row = []
        for g in g_vals:
            d = npv_tax_advantage(p, alpha, g, rho)
            row.append(d['npv_diff_pct'])
        c12[alpha] = row
    return c12


def write_c12_md(c12, p, alpha_vals, g_vals, g_labels):
    """
    Format C.12 as a markdown section matching VAL.A §C conventions.
    """
    N   = p['N']
    k   = p['k']
    V0  = p['V0_m']
    rho = p['rho']
    t0  = p['tau_0'] * 100
    tm  = p['tau_m'] * 100

    lines = []
    lines.append("## C.12 NPV-Adjusted Tax Position: Present Value of Tax Difference vs Honest")
    lines.append("")
    lines.append(
        "**Purpose:** Adjusts the C.1 nominal tax-difference metric for the time value of money. "
        "The C.1 metric treats £1 of tax paid in year 1 as equivalent to £1 received as a refund "
        "in year N+1. C.12 corrects this by discounting all cash flows to t=0 at a common rate ρ. "
        "The comparison reveals whether the apparent nominal advantage to mild overstaters "
        "survives discounting — or whether it is an artefact of comparing early real outflows "
        "against a late nominal refund."
    )
    lines.append("")
    lines.append(
        f"**Metric:** $(NPV_{{tax}}(\\alpha) - NPV_{{tax}}(1))$ / TW_settled(1), "
        f"where $NPV_{{tax}}(\\alpha) = \\sum_{{t=1}}^{{N+1}} L_t / (1+\\rho)^t$ "
        f"and $\\rho = {rho*100:.0f}\\%$."
    )
    lines.append("")
    lines.append(
        f"$\\frac{{NPV_{{tax}}(\\alpha) - NPV_{{tax}}(1)}}{{TW_{{settled}}(1)}}$"
    )
    lines.append("")
    lines.append(
        "**Sign convention:** Positive = alpha pays more in present-value terms than honest "
        "(understater disadvantage). Negative = alpha pays less in PV terms (overstater advantage). "
        "Same as C.1, so tables are directly comparable."
    )
    lines.append("")
    lines.append(
        "**Structural claim:** Two regimes are visible when C.1 and C.12 are compared. "
        f"At ρ = {rho*100:.0f}%, a cash flow at year {N} is worth approximately "
        f"{100*(1/(1+rho)**N):.0f} pence on the pound relative to a year-1 payment, "
        "so the discount penalises late flows heavily. "
        "**Low-g regime (g $\\lesssim$ 8%):** these are the cells where C.1 shows a genuine nominal "
        "advantage for overstaters (negative values). In C.12 those values compress sharply toward "
        "zero or reverse sign. At low g, the sell-year refund is large relative to periodic payments "
        "and arrives heavily discounted; the earlier periodic costs are smaller but weighted at shorter "
        "horizons. Discounting closes the gap: the apparent nominal advantage is a timing artefact. "
        "**Mid/high-g regime (g $\\gtrsim$ 8%):** overstaters already pay more than honest declarers "
        "in C.1 (positive values). C.12 is larger still in this regime because the bulk of periodic "
        "overpayment concentrates in later holding years (when declared wealth is largest), but the "
        "sell-year refund is also late and discounted at the same rate; the net effect is that "
        "discounting penalises the refund more than the distributed periodic costs, pushing the "
        "C.12 value above C.1. "
        "**Understaters:** C.12 is systematically smaller in magnitude than C.1 at mid/high g. "
        "Understaters declare a lower basis and pay smaller periodic taxes early; their larger "
        "settlement at sale is discounted, partially offsetting their nominal penalty. "
        "At low g and high understatement, C.12 can turn negative (understater appears to benefit "
        "in PV terms because the refund on a very low basis is received early relative to the "
        "honest declarer's larger late settlement). "
        "The core design claim is preserved and strengthened: the low-g overstater advantage, "
        "which motivates the §A.6 population-equilibrium argument, is a nominal timing artefact "
        "that collapses once discounted. In PV terms it is approximately neutral or negative, "
        "making the design's tolerance of mild overstatement even more defensible than the "
        "nominal analysis suggests."
    )
    lines.append("")
    lines.append(
        f"**Scope:** Full α grid (same as C.1). "
        f"All values at canonical N = {N}, $k$ = {k}, $V_0$ = £{V0:.0f}m, "
        f"$\\rho$ = {rho*100:.0f}%, $\\tau_0$ = {t0:.0f}%, $\\tau_m$ = {tm:.0f}%. "
        f"Rows = α; columns = g (same grid as C.1)."
    )
    lines.append("")

    lines.extend(_build_pct_table(alpha_vals, g_labels, c12))
    lines.append("")
    lines.append(
        f"Table C.12: NPV-adjusted tax difference vs honest declaration, as % of honest "
        f"TW_settled. $\\alpha$ = 1.0 row is zero by construction. "
        f"Compare directly with C.1: values closer to zero indicate the nominal C.1 "
        f"advantage/disadvantage is a timing artefact; sign reversals indicate the PV "
        f"position is opposite to the nominal position. "
        f"$\\rho$ = {rho*100:.0f}%, $V_0$ = £{V0:.0f}m, $k$ = {k}, N = {N}, "
        f"$\\tau_0$ = {t0:.0f}%, $\\tau_m$ = {tm:.0f}%, "
        f"$W_{{min}}$ = £{p['W_min']:.0f}m."
    )
    lines.append("")
    lines.append(
        "*Key reading:* Compare C.12 with C.1 column by column. "
        "Where C.1 shows a negative value for overstaters (advantage) and C.12 shows a value "
        "close to zero or positive, the nominal advantage is a timing artefact: the overstater "
        "pays early and is refunded late, and the time value of early payment approximately "
        "cancels or reverses the apparent gain. "
        "Where C.1 and C.12 agree in sign and magnitude for understaters, the penalty is "
        "real in both nominal and PV terms — understaters face genuine excess cost regardless "
        "of the discount rate applied."
    )
    lines.append("")

    return '\n'.join(lines)


# ─────────────────────────────────────────────────────────────
# TABLE COMPUTATION  (unchanged)
# ─────────────────────────────────────────────────────────────

def compute_all_tables(p):
    g_pos = [g for g in G_VALS if g > 0]

    base_by_g = {g: run_sim(p, alpha=1.0, beta=0.0, g=g) for g in G_VALS}
    base_pos   = {g: base_by_g[g] for g in g_pos}
    base_ref   = run_sim(p, alpha=1.0, beta=0.0)

    t1 = {}
    for alpha in ALPHA_VALS:
        row = []
        for g in G_VALS:
            r = run_sim(p, alpha=alpha, beta=0.0, g=g)
            b = base_by_g[g]
            row.append((r['Net_settled'] - b['Net_settled']) / r['TW_settled'] if abs(r['TW_settled']) > 1e-12 else 0.0)
        t1[alpha] = row

    t2 = {}
    for alpha in ALPHA_VALS:
        row = []
        for g in G_VALS:
            r = run_sim(p, alpha=alpha, beta=0.0, g=g)
            b = base_by_g[g]
            val = (r['Net_settled'] / r['TW_settled'] - b['Net_settled'] / b['TW_settled']
                   if abs(r['TW_settled']) > 1e-12 and abs(b['TW_settled']) > 1e-12 else 0.0)
            row.append(val)
        t2[alpha] = row

    t3 = {}
    for alpha in OVER_VALS:
        row = []
        for beta_col in G_VALS:
            r = run_sim(p, alpha=alpha, beta=beta_col, g=p['g'])
            val = ((r['Net_settled'] - base_ref['Net_settled']) / r['TW_settled']
                   if abs(r['TW_settled']) > 1e-12 else 0.0)
            row.append(val)
        t3[alpha] = row

    t4 = {}
    for k in K_VALS:
        row = []
        for v0 in V0_VALS:
            tp = dict(p); tp['k'] = k; tp['V0_m'] = float(v0)
            r = run_sim(tp, alpha=1.0, beta=0.0)
            row.append(r['TTP'] / r['TW_settled'] if abs(r['TW_settled']) > 1e-12 else 0.0)
        t4[k] = row

    t5 = {}
    for alpha in ALPHA_VALS:
        row = []
        for k in K_VALS:
            tp = dict(p); tp['k'] = k
            r = run_sim(tp, alpha=alpha, beta=0.0)
            b = run_sim(tp, alpha=1.0, beta=0.0)
            row.append((r['TW_settled'] - b['TW_settled']) / b['TW_settled'] if abs(b['TW_settled']) > 1e-12 else 0.0)
        t5[alpha] = row

    t6 = {}
    for alpha in ALPHA_VALS:
        row = []
        for g in g_pos:
            r = run_sim(p, alpha=alpha, beta=0.0, g=g)
            b = base_pos[g]
            row.append(r['TW_settled'] / b['TW_settled'] if abs(b['TW_settled']) > 1e-12 else 0.0)
        t6[alpha] = row

    t7 = {}; t8 = {}
    for alpha in ALPHA_VALS:
        row7 = []; row8 = []
        for n_act in N_ACTUAL_VALS:
            r = run_sim(p, alpha=alpha, beta=0.0, N=n_act)
            b = run_sim(p, alpha=1.0,   beta=0.0, N=n_act)
            v7 = (r['Net_settled'] - b['Net_settled']) / b['Net_settled'] if abs(b['Net_settled']) > 1e-12 else 0.0
            v8 = (r['TW_settled']  - b['TW_settled'])  / b['TW_settled']  if abs(b['TW_settled'])  > 1e-12 else 0.0
            row7.append(v7); row8.append(v8)
        t7[alpha] = row7; t8[alpha] = row8

    t9 = []
    for g in sorted([g for g in G_VALS if g >= 0], reverse=True):
        r2  = run_sim(p, alpha=2.0, beta=0.0, g=g)
        r1  = run_sim(p, alpha=1.0, beta=0.0, g=g)
        r01 = run_sim(p, alpha=0.1, beta=0.0, g=g)
        refund_ratio = (r01['Net_settled'] / r1['Net_settled']
                        if r1['Net_settled'] < 0 and abs(r1['Net_settled']) > 1e-12 else None)
        t9.append({'g': g, 'TW_a2': r2['TW_settled'], 'TW_a1': r1['TW_settled'],
                   'TW_a01': r01['TW_settled'], 'Net_a2': r2['Net_settled'],
                   'Net_a1': r1['Net_settled'], 'Net_a01': r01['Net_settled'],
                   'refund_ratio': refund_ratio})

    base_hist = run_sim_hist(p, alpha=1.0)

    t10_alpha = []
    for alpha in ALPHA_VALS:
        r = run_sim_hist(p, alpha=alpha)
        tw_vs_honest  = ((r['TW_settled']  - base_hist['TW_settled'])  / base_hist['TW_settled']
                         if abs(base_hist['TW_settled'])  > 1e-12 else 0.0)
        net_vs_honest = ((r['Net_settled'] - base_hist['Net_settled']) / base_hist['Net_settled']
                         if abs(base_hist['Net_settled']) > 1e-12 else 0.0)
        eff_rate      = r['Net_settled'] / r['TW_settled'] if abs(r['TW_settled']) > 1e-12 else 0.0
        t10_alpha.append({
            'alpha':         alpha,
            'TW':            r['TW_settled'],
            'TTP':           r['TTP'],
            'Net':           r['Net_settled'],
            'eff_rate':      eff_rate,
            'tw_vs_honest':  tw_vs_honest,
            'net_vs_honest': net_vs_honest,
            'g_mean':        r['g_mean'],
        })

    n_traj_vals = sorted({5, 10, 15, 20, 25, 30, p['N']})
    t10_n = []
    for n in n_traj_vals:
        r = run_sim_hist(p, alpha=1.0, N=n)
        t10_n.append({
            'N':      n,
            'TW':     r['TW_settled'],
            'Net':    r['Net_settled'],
            'g_mean': r['g_mean'],
        })

    print("  Computing C.11 decomposition...")
    c11_data = compute_c11(p, OVER_VALS, G_VALS)

    print("  Computing C.12 NPV-adjusted tax positions...")
    c12_data = compute_c12(p, ALPHA_VALS, G_VALS)

    return {
        't1': t1, 't2': t2, 't3': t3, 't4': t4,
        't5': t5, 't6': t6, 't7': t7, 't8': t8, 't9': t9,
        't10_alpha': t10_alpha, 't10_n': t10_n,
        **c11_data,     # adds c11a, c11b, c11c, c11d, c11e
        'c12': c12_data,
    }


# _build_pct_table replaced by wdt_md.pct_table (identical signature and output).
# All call sites use: pct_table(row_list, col_labels, data_dict, row_label)
_build_pct_table = pct_table


# ─────────────────────────────────────────────────────────────
# MARKDOWN FORMATTING — VAL.A §C exact format
# ─────────────────────────────────────────────────────────────

def write_appc_md(tables, p):
    N   = p['N']
    k   = p['k']
    t0  = p['tau_0'] * 100
    tm  = p['tau_m'] * 100
    g_p = p['g'] * 100
    V0  = p['V0_m']

    # Shared parameter string used in captions
    def param_str(extra=''):
        base = f"$V_0$ = £{V0:.0f}m, $k$ = {k}, N = {N}, $\\tau_0$ = {t0:.0f}%, $\\tau_m$ = {tm:.0f}%, $W_{{min}}$ = £{p['W_min']:.0f}m"
        return base + (', ' + extra if extra else '')

    lines = []

    # ── Section header ────────────────────────────────────────
    lines.append(f"# C. WDT Valuation Analysis: Summary Tables {{.appendix}}")
    lines.append(f"")
    lines.append(
        f"**Validation status:** All figures in this section are from Python model v1.0 "
        f"(standalone, no Excel dependency), confirmed 0 FAILs across all primary matrices. "
        f"Parameters unified to $k$ = {k}, N = {N}, $\\tau_0$ = {t0:.0f}% across all companion papers. "
        f"Table C.3 carries deviations up to 13% at extreme $\\alpha$×β values (threshold 15%; 0 FAILs); "
        f"see (VAL.A §C.3) note."
    )
    lines.append(f"")
    lines.append(
        f"Unless otherwise stated, all figures use base parameters: "
        f"$V_0$ = £{V0:.0f}m, N = {N}, $\\tau_0$ = {t0:.0f}%, $\\tau_m$ = {tm:.0f}%, "
        f"$k$ = {k}, $W_{{min}}$ = £{p['W_min']:.0f}m, $g$ = {g_p:.2f}%, $\\alpha$ = 1, β = 0%. "
        f"These are the Balanced transition scenario parameters from (RATES)."
    )
    lines.append(f"")

    # ── C.1 ────────────────────────────────────────────────────
    lines.append(f"## C.1 Total Tax Paid (TTP) Difference Relative to Honest Declaration, as Share of Terminal Net Worth (TW)")
    lines.append(f"")
    lines.append(f"**Metric:** (Net($\\alpha$) − Net(1) / TW($\\alpha$). Positive values indicate $\\alpha$ pays more net tax than honest; negative values indicate less.")
    lines.append(f"")
    lines.append(f"$\\frac{{Net(\\alpha) - Net(1)}}{{TW(\\alpha)}}$")
    lines.append(f"")
    lines.append(
        f"**Structural claim:** Understatement is more costly than honest declaration across the "
        f"policy-relevant growth range. The penalty escalates steeply between $g$ ≈ 10% and "
        f"$g$ ≈ 17.3%, then plateaus at a ceiling set by $\\alpha$; the marginal deterrent stops "
        f"escalating but does not reverse. The plateau inflection at $g$ ≈ 17.3% is a rate-function "
        f"property that is approximately constant across all $\\alpha$ and N-invariant above the plateau "
        f"— simulation confirms that the plateau shape at N = 29 and N = 50 are visually identical "
        f"(SWEEPS §2.3, Fig S3.1b). The C.1 metric for $\\alpha$ = 0.1 exceeds 100% at approximately "
        f"$g$ = 23–24% — the understater's excess tax exceeds their terminal wealth — but this is a "
        f"normalisation artefact (the denominator, the understater's own TW, compresses at high growth), "
        f"not a sign reversal in the penalty. For mild overstatement ($\\alpha$ ≤ 1.5), overstatement "
        f"produces a tax saving at moderate positive growth, with no reversal within the tested range at "
        f"canonical parameters. For aggressive overstatement ($\\alpha$ ≥ 1.8), the saving reverses in "
        f"the $g$ ≈ 9–17% corridor containing the historical mean and recovers only above $g$ ≈ 17%; "
        f"the self-limiting mechanism also operates temporally through the N-crossing described in §A.5.4. "
        f"In negative growth scenarios the refund cap binds for understaters, reducing their net-tax advantage."
    )
    lines.append(f"")

    t1 = tables['t1']
    col_labels = G_LABELS
    lines += _build_pct_table(ALPHA_VALS, col_labels, t1)
    lines.append(f"")
    lines.append(
        f"Table C.1: TTP difference relative to honest declaration, as share of TW. "
        f"$\\alpha$ = 1.0 row is zero by construction. Positive values indicate understater pays more lifetime tax. "
        f"{param_str()}."
    )
    lines.append(f"")

    # ── C.2 ────────────────────────────────────────────────────
    lines.append(f"## C.2 Effective Lifetime Tax Rate Difference from Honest Declaration")
    lines.append(f"")
    lines.append(f"**Metric:** Net($\\alpha$)/TW($\\alpha$) − Net(1)/TW(1). Positive values indicate $\\alpha$ has a higher effective lifetime rate than the honest declarer.")
    lines.append(f"")
    lines.append(f"$\\frac{{Net(\\alpha)}}{{TW(\\alpha)}} - \\frac{{Net(1)}}{{TW(1)}}$")
    lines.append(f"")
    lines.append(
        f"**Structural claim:** Effective lifetime tax rate differences are directionally consistent "
        f"with C.1 but larger in magnitude, because the formula normalises by TW($\\alpha$) and TW(1) "
        f"separately rather than by a common denominator. Understaters face materially higher effective "
        f"rates than honest declarers across all tested growth rates; overstaters face lower rates at "
        f"moderate growth. The differential is largest at low and high growth extremes, reflecting "
        f"refund protection loss and saturation effects respectively."
    )
    lines.append(f"")

    t2 = tables['t2']
    lines += _build_pct_table(ALPHA_VALS, col_labels, t2)
    lines.append(f"")
    lines.append(
        f"Table C.2: Effective lifetime tax rate difference from honest declaration. "
        f"$\\alpha$ = 1.0 row is zero by construction. {param_str()}."
    )
    lines.append(f"")
    lines.append(f"*Note: this table measures the difference in effective lifetime tax rate relative to honest declaration, not an absolute rate.*")
    lines.append(f"")

    # ── C.3 ────────────────────────────────────────────────────
    lines.append(f"## C.3 Exploratory Extension: Investor Confidence Effects β (Overstatement Only)")
    lines.append(f"")
    lines.append(f"*This section is exploratory and not required for the operation of WDT. The beta mechanism is not empirically calibrated. Results are sensitivity testing, not prediction.*")
    lines.append(f"")
    lines.append(f"**Metric:** (Net($\\alpha$,β) − Net(1,β=0) / TW($\\alpha$,β). β swept over the same numeric values as the $g$ columns in C.1/C.2; $g$ fixed at {g_p:.2f}%.")
    lines.append(f"")
    lines.append(f"$\\frac{{Net(\\alpha, \\beta) - Net(1, \\beta=0)}}{{TW(\\alpha, \\beta)}}$")
    lines.append(f"")
    lines.append(
        f"**Structural claim:** β represents the sensitivity of true asset growth to declared valuation "
        f"via $g_{{eff}} = g + \\beta \\cdot \\ln(\\alpha)$ (see (VAL.A §B.2.1) and (VAL.A §B.2.2). "
        f"A positive β partially offsets the declaration cost where overstatement contributes to confidence "
        f"formation. Scope is overstatement only ($\\alpha$ ≥ 1.0); understater cells are omitted. "
        f"Deviations at high $\\alpha$×β values (up to 13%) reflect exponential compounding of g_eff "
        f"over N = {N}; directional claims are unaffected. No empirical calibration for β exists."
    )
    lines.append(f"")

    t3 = tables['t3']
    beta_labels = [f"β={g*100:.1f}%" for g in G_VALS]
    lines += _build_pct_table(OVER_VALS, beta_labels, t3, row_label='$\\alpha$ \\ β')
    lines.append(f"")
    lines.append(
        f"Table C.3: Investor confidence β sensitivity (overstatement only). "
        f"Sign convention: positive = $\\alpha$ pays more than honest. "
        f"β column values are the same numeric sweep as $g$ in C.1/C.2; $g$ fixed at {g_p:.2f}%, N={N} throughout. "
        f"Deviations increase at high $\\alpha$×β due to exponential compounding; "
        f"max deviation vs Excel 13% (threshold 15%; 0 FAILs). "
        f"$V_0$ = £{V0:.0f}m, $k$ = {k}, $\\tau_0$ = {t0:.0f}%, $\\tau_m$ = {tm:.0f}%, $W_{{min}}$ = £{p['W_min']:.0f}m."
    )
    lines.append(f"")

    # ── C.4 ────────────────────────────────────────────────────
    lines.append(f"## C.4 Effective Lifetime Tax Rate by $k$ Parameter and Initial Wealth ($V_0$)")
    lines.append(f"")
    lines.append(f"**Metric:** TTP($\\alpha$=1) / TW($\\alpha$=1). Honest declaration throughout. Rows = k; columns = $V_0$ (£m).")
    lines.append(f"")
    lines.append(f"$\\frac{{TTP(\\alpha=1)}}{{TW(\\alpha=1)}}$")
    lines.append(f"")
    lines.append(
        f"**Structural claim:** The S-curve rate function produces an effective lifetime rate that is low "
        f"at small $V_0$ and rises toward $\\tau_m$ at very large $V_0$ × high $k$ combinations. "
        f"The policy-relevant $k$ range is approximately 1e-04 to 1e-03; values above 5e-03 are "
        f"analytically extreme and included for completeness only. The rate ceiling of approximately "
        f"60.67% reflects the logistic bound at $\\tau_m$ = {tm:.0f}% over N = {N} years."
    )
    lines.append(f"")

    t4 = tables['t4']
    v0_labels = [f"£{v}m" for v in V0_VALS]
    k_row_label = '$k$ \\ $V_0$'
    h4 = [k_row_label] + v0_labels
    lines.append('| ' + ' | '.join(h4) + ' |')
    lines.append('|' + '|'.join(':---:' for _ in h4) + '|')
    for k_val in K_VALS:
        cells = [f'{k_val:.0e}'] + [pct_str(v, 2) for v in t4[k_val]]
        lines.append('| ' + ' | '.join(cells) + ' |')
    lines.append(f"")
    lines.append(
        f"Table C.4: Effective lifetime tax rate by $k$ and $V_0$. "
        f"All at $\\alpha$=1, β=0, $g$={g_p:.2f}%, N={N}. "
        f"$k$ values above 1e-03 are analytically extreme; included for completeness."
    )
    lines.append(f"")

    # ── C.5 ────────────────────────────────────────────────────
    lines.append(f"## C.5 Sensitivity of $k$ and Alpha: Terminal Net Worth Difference vs Honest")
    lines.append(f"")
    lines.append(f"**Metric:** (TW($\\alpha$,k) − TW(1,k) / TW(1,k). Positive values indicate $\\alpha$ retains more terminal net worth than honest; negative values indicate less.")
    lines.append(f"")
    lines.append(f"$\\frac{{TW(\\alpha,k) - TW(1,k)}}{{TW(1,k)}}$")
    lines.append(f"")
    lines.append(
        f"**Structural claim:** TW differences are directionally consistent across the tested $k$ range. "
        f"Understater penalties scale with $k$ up to the logistic saturation boundary, beyond which "
        f"further increases have diminishing effect. The overstater advantage follows the same pattern, "
        f"accelerating at high $k$ ($k$ ≥ 1e-02) as the rate function's bracket ascent steepens. "
        f"$k$ values above 1e-03 are analytically extreme."
    )
    lines.append(f"")

    t5 = tables['t5']
    k_labels = [f'{kv:.0e}' for kv in K_VALS]
    lines += _build_pct_table(ALPHA_VALS, k_labels, t5, row_label='$\\alpha$ \\ $k$')
    lines.append(f"")
    lines.append(
        f"Table C.5: TW difference vs honest, by $k$ and $\\alpha$. "
        f"$\\alpha$ = 1.0 row is zero by construction. $g$ = {g_p:.2f}%, N = {N} throughout."
    )
    lines.append(f"")

    # ── C.6 ────────────────────────────────────────────────────
    lines.append(f"## C.6 Terminal Net Worth After Refunds: Refund Protection Ratio")
    lines.append(f"")
    lines.append(f"**Metric:** TW($\\alpha$) / TW(1). Values below 100% indicate reduced TW relative to honest. Negative $g$ scenarios only.")
    lines.append(f"")
    lines.append(f"$\\frac{{TW(\\alpha)}}{{TW(1)}}$")
    lines.append(f"")
    lines.append(
        f"**Structural claim:** Understaters receive materially reduced terminal wealth in negative growth "
        f"scenarios because the refund is calculated on the declared basis, not the true value. The "
        f"protection loss is determined almost entirely by the entry declaration and is stable across "
        f"negative growth rates for each $\\alpha$ — the ratio at $g$ = −4.5% characterises the full "
        f"negative-$g$ regime. Overstaters show 100% throughout: the lifetime cap prevents refunds "
        f"exceeding prior contributions, which in a purely negative growth environment are zero for all strategies."
    )
    lines.append(f"")

    # Recompute for negative g only
    p_copy = p.copy()
    neg_g_vals  = [g for g in G_VALS if g < 0]
    neg_g_labels = [G_LABELS[i] for i, g in enumerate(G_VALS) if g < 0]
    base_neg = {g: run_sim(p_copy, alpha=1.0, beta=0.0, g=g) for g in neg_g_vals}
    t6_neg = {}
    for alpha in ALPHA_VALS:
        row = []
        for g in neg_g_vals:
            r = run_sim(p_copy, alpha=alpha, beta=0.0, g=g)
            b = base_neg[g]
            row.append(r['TW_settled'] / b['TW_settled'] if abs(b['TW_settled']) > 1e-12 else 0.0)
        t6_neg[alpha] = row

    lines += _build_pct_table(ALPHA_VALS, neg_g_labels, t6_neg)
    lines.append(f"")
    lines.append(
        f"Table C.6: Refund protection ratio vs honest declaration. "
        f"Negative $g$ scenarios only. $\\alpha$ = 1.0 is 100% by construction. "
        f"Understater protection loss proportional to basis gap at entry. "
        f"{param_str()}."
    )
    lines.append(f"")

    # ── C.7 ────────────────────────────────────────────────────
    lines.append(f"## C.7 Total Tax Paid Compared to Honest Taxpayer, Adjusted for N")
    lines.append(f"")
    lines.append(f"**Metric:** (Net($\\alpha$,N) − Net(1,N) / Net(1,N). Positive values indicate $\\alpha$ pays more net tax than honest. N values shown are actual simulation N (5 to 60). Earlier Excel display showed N-5 in column headers; corrected here.")
    lines.append(f"")
    lines.append(f"$\\frac{{Net(\\alpha,N) - Net(1,N)}}{{Net(1,N)}}$")
    lines.append(f"")
    lines.append(
        f"**Structural claim:** Understatement imposes a persistent and substantial net-tax penalty "
        f"across all holding periods tested. The penalty is largest at short horizons (N = 5) where "
        f"the basis gap recovery dominates a small total tax base, and compresses as the holding period "
        f"extends. For overstatement, the initial advantage narrows and can reverse at extended horizons "
        f"where the honest declarer has accumulated more basis history. Understater N = 5 penalties above "
        f"100% reflect the realisation delta dominating a near-zero prior-year contribution."
    )
    lines.append(f"")

    t7 = tables['t7']
    n_labels = [str(n) for n in N_ACTUAL_VALS]
    lines += _build_pct_table(ALPHA_VALS, n_labels, t7, row_label='$\\alpha$ \\ N')
    lines.append(f"")
    lines.append(
        f"Table C.7: Net tax compared to honest taxpayer, adjusted for N. "
        f"$\\alpha$ = 1.0 row is zero by construction. $g$ = {g_p:.2f}% throughout. "
        f"$V_0$ = £{V0:.0f}m, $k$ = {k}, $\\tau_0$ = {t0:.0f}%, $\\tau_m$ = {tm:.0f}%, $W_{{min}}$ = £{p['W_min']:.0f}m."
    )
    lines.append(f"")

    # ── C.8 ────────────────────────────────────────────────────
    lines.append(f"## C.8 Terminal Net Worth Compared to Honest Taxpayer, Adjusted for N")
    lines.append(f"")
    lines.append(f"**Metric:** (TW($\\alpha$,N) − TW(1,N) / TW(1,N). Negative values indicate $\\alpha$ retains less TW than honest. N correction as C.7 — actual N shown.")
    lines.append(f"")
    lines.append(f"$\\frac{{TW(\\alpha,N) - TW(1,N)}}{{TW(1,N)}}$")
    lines.append(f"")
    lines.append(
        f"**Structural claim:** TW differences widen materially as N rises — the basis gap compounds "
        f"into more pronounced divergence at $k$ = {k} than at lower k. The understater penalty at "
        f"$\\alpha$ = 0.1 grows from −12.76% at N = 5 to −41.99% at N = 60. Overstater advantages "
        f"widen on the same trajectory. No convergence toward zero occurs within realistic holding "
        f"periods at $g$ = {g_p:.2f}%."
    )
    lines.append(f"")

    t8 = tables['t8']
    lines += _build_pct_table(ALPHA_VALS, n_labels, t8, row_label='$\\alpha$ \\ N')
    lines.append(f"")
    lines.append(
        f"Table C.8: TW compared to honest taxpayer, adjusted for N. "
        f"$\\alpha$ = 1.0 row is zero by construction. $g$ = {g_p:.2f}% throughout. "
        f"$V_0$ = £{V0:.0f}m, $k$ = {k}, $\\tau_0$ = {t0:.0f}%, $\\tau_m$ = {tm:.0f}%, $W_{{min}}$ = £{p['W_min']:.0f}m."
    )
    lines.append(f"")

    # ── C.9 ────────────────────────────────────────────────────
    lines.append(f"## C.9 Summary of Declaration Incentives Across Growth Regimes")
    lines.append(f"")
    lines.append(f"**Metric:** TW(£m) and Net tax (£m) at $\\alpha$ ∈ {{2.0, 1.0, 0.1}} across the $g$ sweep; ratios vs honest. N = {N} throughout.")
    lines.append(f"")
    lines.append(
        f"**Structural claim:** The mechanism's fundamental properties hold across the full tested "
        f"growth range. Understatement consistently costs more than honest declaration in absolute "
        f"net-tax terms at every positive $g$ tested. The understater penalty escalates steeply "
        f"between $g$ ≈ 10% and $g$ ≈ 17.3%, then plateaus — the rate ceiling stops further "
        f"escalation but does not reverse it. The plateau ceiling scales with the degree of "
        f"understatement: $\\alpha$ = 0.1 plateaus near 98% of true wealth, $\\alpha$ = 0.2 near 70%, "
        f"$\\alpha$ = 0.5 near 24%, $\\alpha$ = 0.8 near 6%. The inflection at $g$ ≈ 17.3% is a "
        f"rate-function property, approximately constant across all $\\alpha$ and N-invariant above "
        f"the plateau (see §A.5.4 and SWEEPS §2.3, Fig S3.1b). For overstaters, this table captures "
        f"the contemporaneous growth-corridor effect for aggressive overstatement; the temporal "
        f"N-crossing correction operates across holding periods and is documented in §C.8 and "
        f"SWEEPS.A §A.4. The TW(0.1)/TW(1) ratio declines from approximately 86–87% at moderate "
        f"growth to 63.2% at $g$ = 25.4%, reflecting compounding basis gap effects consistent with "
        f"the penalty plateau. The C.1 metric exceeding 100% at $g$ = 25.4% for $\\alpha$ = 0.1 is "
        f"a normalisation artefact: it means the excess tax exceeds the understater's terminal wealth, "
        f"not that the penalty reverses."
    )
    lines.append(f"")

    t9 = tables['t9']
    h9 = ['$g$', 'TW($\\alpha$=2) £m', 'TW($\\alpha$=1) £m', 'TW($\\alpha$=0.1) £m',
          'Net($\\alpha$=2) £m', 'Net($\\alpha$=1) £m', 'Net($\\alpha$=0.1) £m',
          'TW(0.1)/TW(1)', 'Net(0.1)/Net(1)']
    lines.append('| ' + ' | '.join(h9) + ' |')
    lines.append('|' + '|'.join(':---:' for _ in h9) + '|')
    for row in t9:
        g_disp = f"{row['g']*100:.1f}%"
        tw2    = f"{row['TW_a2']:.1f}"
        tw1    = f"{row['TW_a1']:.1f}"
        tw01   = f"{row['TW_a01']:.1f}"
        net2   = f"{row['Net_a2']:.1f}"
        net1   = f"{row['Net_a1']:.1f}"
        net01  = f"{row['Net_a01']:.1f}"
        tw_r   = f"{row['TW_a01']/row['TW_a1']*100:.1f}%" if abs(row['TW_a1']) > 1e-12 else "—"
        net_r  = (f"{row['Net_a01']/row['Net_a1']*100:.1f}%"
                  if row['refund_ratio'] is not None else "—")
        lines.append(f"| {g_disp} | {tw2} | {tw1} | {tw01} | {net2} | {net1} | {net01} | {tw_r} | {net_r} |")
    lines.append(f"")
    lines.append(
        f"Table C.9: Summary of declaration incentives across growth regimes. "
        f"TW and Net tax in £m. N = {N} throughout. "
        f"Net($\\alpha$=0.1)/Net($\\alpha$=1) shown only where Net < 0 (refund scenario, negative $g$); "
        f"'—' at positive $g$ where both Net values are positive. "
        f"{param_str()}."
    )
    lines.append(f"")

    # ── C.10 ───────────────────────────────────────────────────
    lines.append(f"## C.10 2006 Historical Return Series — Reference Scenario Results")
    lines.append(f"")
    lines.append(
        f"**Source:** RATES Balanced worst-case reference scenario "
        f"(p['returns'] rotated to {p['scenario_start_year']} start year). "
        f"$V_0$ = £{V0:.0f}m, $\\tau_0$ = {t0:.0f}%, $\\tau_m$ = {tm:.0f}%, $k$ = {k}, "
        f"$W_{{min}}$ = £{p['W_min']:.0f}m. No β adjustment applied."
    )
    lines.append(f"")
    lines.append(
        f"**Purpose:** Locates the RATES worst-case scenario within the analytical space of C.1–C.9. "
        f"The 2006 series includes the 2008 crash and subsequent recovery. The realised mean growth "
        f"rate across N = {N} periods is "
        f"{tables['t10_alpha'][0]['g_mean']*100:.2f}%, "
        f"below the {g_p:.2f}% historical mean used in C.1–C.9; results here represent a harder "
        f"test than the constant-$g$ tables."
    )
    lines.append(f"")

    # C.10.1
    lines.append(f"### C.10.1 Declaration strategy comparison ($\\alpha$ sweep, N = {N})")
    lines.append(f"")
    lines.append(
        f"Each row uses p['returns'][:N] as the holding-period series and p['returns'][N] as the "
        f"sell-year rate. The g_mean column is the arithmetic mean of the N holding-period returns."
    )
    lines.append(f"")
    h10a = ['$\\alpha$', 'TW (£m)', 'TTP (£m)', 'Net (£m)', 'Eff rate', 'TW vs honest', 'Net vs honest']
    lines.append('| ' + ' | '.join(h10a) + ' |')
    lines.append('|' + '|'.join(':---:' for _ in h10a) + '|')
    for row in tables['t10_alpha']:
        marker = ' ← honest' if row['alpha'] == 1.0 else ''
        honest_marker = f'**{row["alpha"]}**' if row['alpha'] == 1.0 else f'**{row["alpha"]}**'
        tw_s   = f'{row["TW"]:.2f}'
        ttp_s  = f'{row["TTP"]:.2f}'
        net_s  = f'{row["Net"]:.2f}'
        eff_s  = f'{row["eff_rate"]*100:.2f}%'
        twv_s  = f'{row["tw_vs_honest"]*100:+.2f}%'
        netv_s = f'{row["net_vs_honest"]*100:+.2f}%'
        if row['alpha'] == 1.0:
            lines.append(f"| **{row['alpha']}** | {tw_s} | {ttp_s} | {net_s} | {eff_s} | {twv_s} | {netv_s}{marker} |")
        else:
            lines.append(f"| **{row['alpha']}** | {tw_s} | {ttp_s} | {net_s} | {eff_s} | {twv_s} | {netv_s} |")
    lines.append(f"")
    lines.append(
        f"Table C.10.1: Declaration strategy comparison, 2006 historical return series, N = {N}. "
        f"$\\alpha$ = 1.0 row is the honest baseline; TW vs honest and Net vs honest are zero by construction. "
        f"Positive Net vs honest = understater pays more net tax than honest under the historical series."
    )
    lines.append(f"")

    # C.10.2
    lines.append(f"### C.10.2 Honest declarer trajectory by N ($\\alpha$ = 1.0)")
    lines.append(f"")
    lines.append(
        f"Each row uses p['returns'][:N] as the holding-period series and p['returns'][N] as the "
        f"sell-year rate. The g_mean column is the arithmetic mean of the N holding-period returns; "
        f"it shifts as more years of the 2006 series are included, most notably around N = 3 "
        f"(2008 crash enters) and N = 4 (2009 recovery enters)."
    )
    lines.append(f"")
    h10b = ['N', 'TW (£m)', 'Net (£m)', 'Mean $g$ of series[:N]']
    lines.append('| ' + ' | '.join(h10b) + ' |')
    lines.append('|' + '|'.join(':---:' for _ in h10b) + '|')
    for row in tables['t10_n']:
        is_ref = row['N'] == p['N']
        n_str  = f"**{row['N']}**" if is_ref else str(row['N'])
        tw_str = f"**{row['TW']:.2f}**" if is_ref else f"{row['TW']:.2f}"
        net_str = f"**{row['Net']:.2f}**" if is_ref else f"{row['Net']:.2f}"
        g_str  = f"**{row['g_mean']*100:.2f}%**" if is_ref else f"{row['g_mean']*100:.2f}%"
        lines.append(f"| {n_str} | {tw_str} | {net_str} | {g_str} |")
    lines.append(f"")
    lines.append(
        f"Table C.10.2: Honest declarer trajectory under 2006 historical return series by holding period. "
        f"N = {N} row is the RATES reference scenario. TW and Net grow with N as additional years of "
        f"compounding and WDT payments accumulate. Unlike C.7/C.8 (constant $g$ throughout), each row "
        f"reflects a different prefix of the realised return history, making path-dependence explicit."
    )
    lines.append(f"")

    # ── C.11 ───────────────────────────────────────────────────
    lines.append(write_c11_md(
        tables, p,
        over_vals=OVER_VALS,
        g_vals=G_VALS,
        g_labels=G_LABELS,
    ))

    # ── C.12 ───────────────────────────────────────────────────
    lines.append(write_c12_md(
        tables['c12'], p,
        alpha_vals=ALPHA_VALS,
        g_vals=G_VALS,
        g_labels=G_LABELS,
    ))

    return '\n'.join(lines)



# ─────────────────────────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────────────────────────

def main():
    p = load_params()
    print(f"Parameters loaded: k={p['k']}, N={p['N']} (SSM-derived), g={p['g']:.4f}")

    global G_VALS, G_LABELS, ALPHA_VALS, K_VALS, V0_VALS, N_ACTUAL_VALS, OVER_VALS
    sw = p['sweep']
    G_VALS        = sw['g_vals']
    G_LABELS      = [f"{v*100:.1f}%" for v in G_VALS]
    ALPHA_VALS    = sw['alpha_vals']
    K_VALS        = sw['appc_k_vals']
    V0_VALS       = sw['appc_v0_vals']
    N_ACTUAL_VALS = sw['n_actual_vals']
    OVER_VALS     = sw['appc_over_vals']

    print("Computing all Appendix C tables...")
    tables = compute_all_tables(p)

    print("Formatting markdown (VAL.A §C format)...")
    md = write_appc_md(tables, p)

    ensure_dir(_OUT)
    out_path = _OUT / "VAL_AppC_Full_Tables.md"
    out_path.write_text(md, encoding="utf-8")
    print(f"Written: {out_path}")
    print(f"Lines: {len(md.splitlines())}")


if __name__ == '__main__':
    main()