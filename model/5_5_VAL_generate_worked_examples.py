"""
VAL Output Script C — Worked Example Figures (v2 — data-driven)
================================================================
Generates VAL_Worked_Examples_Figures.md

All simulation data is loaded from OUTPUTS/VAL/val_data.json
(produced by val_core.py). No wdt_core simulation calls here.

To regenerate output:
    python val_core.py                          # run simulations
    python 5_5_VAL_generate_worked_examples.py # render markdown

Output format matches VAL.B exactly:
  - Table captions BELOW each table: "Table J.1: description. params."
  - Column headers use LaTeX: $\\alpha$, $\\tau$, etc.
  - Metric row labels bolded: **Entry basis $B_0$**
  - Section headers match VAL.B: ## J.3 / ### J.3.1 / ### J.3.2

All figures use TW_settled/Net_settled internally but are presented
as TW/Net in table labels to match VAL.B nomenclature.
"""

from datetime import date
from pathlib import Path

from val_core import load_val_data
from wdt_fmt import fmt_gbp_m as fm, fmt_pct as fp, out_dir, ensure_dir

_OUT = out_dir('VAL')


# ─────────────────────────────────────────────────────────────
# EXAMPLE §J: THE DEFERRED DELTA
# ─────────────────────────────────────────────────────────────

def example_j(data: dict) -> str:
    ex    = data['examples']['J']
    p_meta = data['params']
    g     = ex['g']; N = ex['N']
    res   = ex['results']

    def r(alpha_key):
        return res[str(alpha_key)]

    # Re-derive summary scalars from stored records
    def tax_paid(records):
        return sum(rec['L'] for rec in records[1:] if rec['L'] > 0)

    lines = []
    lines.append("## J.3 Illustrative Figures")
    lines.append("")

    r10, r08, r05 = r(1.0), r(0.8), r(0.5)
    sell10, sell08, sell05 = r10['sell'], r08['sell'], r05['sell']

    tax_10 = tax_paid(r10['records'])
    tax_08 = tax_paid(r08['records'])
    tax_05 = tax_paid(r05['records'])

    tw_diff_08  = (r08['TW_settled']  - r10['TW_settled'])  / r10['TW_settled']  * 100
    tw_diff_05  = (r05['TW_settled']  - r10['TW_settled'])  / r10['TW_settled']  * 100
    net_diff_08 = (r08['Net_settled'] - r10['Net_settled']) / r10['Net_settled'] * 100
    net_diff_05 = (r05['Net_settled'] - r10['Net_settled']) / r10['Net_settled'] * 100

    lines.append("| | **Honest ($\\alpha$ = 1.0)** | **Moderate under ($\\alpha$ = 0.8)** | **Significant under ($\\alpha$ = 0.5)** |")
    lines.append("|:---|---:|---:|---:|")
    lines.append(f"| **Entry basis $B_0$** | £20.000m | £16.000m | £10.000m |")
    lines.append(f"| **True value at sale $V_5$** | {fm(sell10['V_sell'])} | {fm(sell08['V_sell'])} | {fm(sell05['V_sell'])} |")
    lines.append(f"| **Tax paid years 1–5** | {fm(tax_10)} | {fm(tax_08)} | {fm(tax_05)} |")
    lines.append(f"| **Final delta on sale (year 6)** | {fm(sell10['delta_sell'])} | {fm(sell08['delta_sell'])} | {fm(sell05['delta_sell'])} |")
    lines.append(f"| **Tax on final delta** | {fm(max(0, sell10['L_sell']))} | {fm(max(0, sell08['L_sell']))} | {fm(max(0, sell05['L_sell']))} |")
    lines.append(f"| **Total lifetime WDT (Net)** | {fm(r10['Net_settled'])} | {fm(r08['Net_settled'])} | {fm(r05['Net_settled'])} |")
    lines.append(f"| **Terminal net worth (TW)** | {fm(r10['TW_settled'])} | {fm(r08['TW_settled'])} | {fm(r05['TW_settled'])} |")
    lines.append(f"| **TW vs honest** | — | {tw_diff_08:+.2f}% | {tw_diff_05:+.2f}% |")
    lines.append(f"| **Net tax vs honest** | — | {net_diff_08:+.2f}% | {net_diff_05:+.2f}% |")
    lines.append("")
    lines.append(f"Table J.1: Deferred delta comparison across declaration strategies, $g$ = 7%, N = 5, $\\tau$ = 15%. Python model v1.0, $k$ = {p_meta['k']}.")
    lines.append("")

    # §J.3.1 Period-by-period
    lines.append("### J.3.1 Period-by-period: Honest declarer ($\\alpha$ = 1.0)")
    lines.append("")
    lines.append("| t | True V (£m) | Declared W (£m) | Delta (£m) | $\\tau$ | Tax L (£m) | f |")
    lines.append("|:---:|---:|---:|---:|:---:|---:|:---:|")
    for rec in r10['records']:
        if rec['t'] == 0:
            lines.append(f"| 0 (entry) | {rec['V']:.3f} | {rec['W']:.3f} | — | {fp(rec['rate'])} | 0.000 | {rec['f']:.4f} |")
        else:
            lines.append(f"| {rec['t']} | {rec['V']:.3f} | {rec['W']:.3f} | {rec['delta']:.3f} | {fp(rec['rate'])} | {rec['L']:.3f} | {rec['f']:.4f} |")
    s = sell10
    lines.append(f"| 6 (sell) | {s['V_sell']:.3f} | {s['W_sell']:.3f} | {s['delta_sell']:.3f} | {fp(s['rate_sell'])} | {s['L_sell']:.3f} | {s['f_N']:.4f} |")
    lines.append("")

    # §J.3.2 Key mechanism
    lines.append("### J.3.2 Key mechanism: basis gap recovery at sale")
    lines.append("")
    extra_08    = sell08['delta_sell'] - sell10['delta_sell']
    extra_05    = sell05['delta_sell'] - sell10['delta_sell']
    more_tax_08 = max(0, sell08['L_sell']) - max(0, sell10['L_sell'])
    more_tax_05 = max(0, sell05['L_sell']) - max(0, sell10['L_sell'])
    net_cost_08 = r08['Net_settled'] - r10['Net_settled']
    net_cost_05 = r05['Net_settled'] - r10['Net_settled']
    saved_08    = tax_10 - tax_08
    saved_05    = tax_10 - tax_05

    lines.append(
        f"At the sell year, the final delta differs by declaration strategy: "
        f"honest ($\\alpha$ = 1.0) {fm(sell10['delta_sell'])} → tax {fm(max(0, sell10['L_sell']))}; "
        f"$\\alpha$ = 0.8 {fm(sell08['delta_sell'])} → tax {fm(max(0, sell08['L_sell']))} "
        f"(larger by {fm(extra_08)} due to suppressed basis); "
        f"$\\alpha$ = 0.5 {fm(sell05['delta_sell'])} → tax {fm(max(0, sell05['L_sell']))} "
        f"(larger by {fm(extra_05)} due to suppressed basis)."
    )
    lines.append("")
    lines.append(
        f"The $\\alpha$ = 0.8 understater saved {fm(saved_08)} in years 1–5 but paid "
        f"{fm(more_tax_08)} more at sale — net cost of understatement: {fm(net_cost_08)}. "
        f"The $\\alpha$ = 0.5 understater saved {fm(saved_05)} in years 1–5 but paid "
        f"{fm(more_tax_05)} more at sale — net cost of understatement: {fm(net_cost_05)}."
    )
    lines.append("")
    return '\n'.join(lines)


# ─────────────────────────────────────────────────────────────
# EXAMPLE §K: DILUTION COMPOUNDS WITH GROWTH
# ─────────────────────────────────────────────────────────────

def example_k(data: dict) -> str:
    ex    = data['examples']['K']
    p_meta = data['params']
    N     = ex['N']
    res   = ex['results']

    r10, r06 = res['1.0'], res['0.6']

    lines = []
    lines.append("## K.3 Illustrative Figures")
    lines.append("")
    lines.append(
        f"**Model note.** (VAL.B §K) uses three *assessment windows* of unspecified length. "
        f"This model uses N = 3 *annual* periods as a proxy (Option A). A window-aware model would "
        f"produce different equity accumulation figures; the directional claim (dilution is more "
        f"expensive at high $g$) is unaffected."
    )
    lines.append("")

    # K.3.1
    lines.append("### K.3.1 Period-by-period accumulation")
    lines.append("")
    lines.append(
        "| Period | True V (£m) | Honest W (£m) | Honest f | Understater W (£m) | "
        "Understater f | State equity (honest) | State equity ($\\alpha$=0.6) |"
    )
    lines.append("|:---:|---:|---:|:---:|---:|:---:|:---:|:---:|")
    for t in range(N + 1):
        rh = r10['records'][t]; ru = r06['records'][t]
        state_h = f"{(1.0 - rh['f'])*100:.3f}%" if t > 0 else "0.000%"
        state_u = f"{(1.0 - ru['f'])*100:.3f}%" if t > 0 else "0.000%"
        label = "entry" if t == 0 else str(t)
        lines.append(
            f"| {label} | {rh['V']:.3f} | {rh['W']:.3f} | {rh['f']:.4f} | "
            f"{ru['W']:.3f} | {ru['f']:.4f} | {state_h} | {state_u} |"
        )
    sh, su = r10['sell'], r06['sell']
    lines.append(
        f"| sell | {sh['V_sell']:.3f} | {sh['W_sell']:.3f} | {sh['f_N']:.4f} | "
        f"{su['W_sell']:.3f} | {su['f_N']:.4f} | "
        f"{(1-sh['f_N'])*100:.3f}% | {(1-su['f_N'])*100:.3f}% |"
    )
    lines.append("")

    # K.3.2
    rN_h = r10['records'][N]; rN_u = r06['records'][N]
    state_true_h   = (1.0 - rN_h['f']) * rN_h['V']
    state_true_u   = (1.0 - rN_u['f']) * rN_u['V']
    founder_true_h = rN_h['f'] * rN_h['V']
    founder_true_u = rN_u['f'] * rN_u['V']
    implicit_cost  = r06['Net_settled'] - r10['Net_settled']

    lines.append("### K.3.2 Summary at period N = 3")
    lines.append("")
    lines.append("| Metric | Honest ($\\alpha$ = 1.0) | Understater ($\\alpha$ = 0.6) |")
    lines.append("|:---|---:|---:|")
    lines.append(f"| **Founder retained fraction** | {rN_h['f']*100:.3f}% | {rN_u['f']*100:.3f}% |")
    lines.append(f"| **State equity stake** | {(1-rN_h['f'])*100:.3f}% | {(1-rN_u['f'])*100:.3f}% |")
    lines.append(f"| **True value of state stake (£m)** | {fm(state_true_h)} | {fm(state_true_u)} |")
    lines.append(f"| **True value of founder stake (£m)** | {fm(founder_true_h)} | {fm(founder_true_u)} |")
    lines.append(f"| **Tax paid (Net) (£m)** | {fm(r10['Net_settled'])} | {fm(r06['Net_settled'])} |")
    lines.append(f"| **Terminal net worth TW (£m)** | {fm(r10['TW_settled'])} | {fm(r06['TW_settled'])} |")
    lines.append(f"| **Implicit cost of understatement vs honest (£m)** | — | {fm(implicit_cost)} |")
    lines.append("")
    lines.append(
        f"Table K.1: Accumulated dilution under understatement, $g$ = 15%, Route C, "
        f"N = 3 annual periods as proxy for three-year window, $\\tau$ = 15%. "
        f"Python model v1.0, $k$ = {p_meta['k']}."
    )
    lines.append("")

    # K.3.3
    lines.append("### K.3.3 Key mechanism: underpriced equity transfer")
    lines.append("")
    lines.append(
        f"The understater transfers equity at their declared value (60% of true value). "
        f"The state acquires this equity at a 40% discount to reality; it then appreciates at "
        f"the true rate (15% per year). After 3 periods, the state holds "
        f"{(1-rN_u['f'])*100:.3f}% vs {(1-rN_h['f'])*100:.3f}% for "
        f"the honest declarer. The understater has transferred less equity in percentage terms "
        f"but at a steeper discount, so net tax cost is higher: {fm(implicit_cost)} extra."
    )
    lines.append("")
    return '\n'.join(lines)


# ─────────────────────────────────────────────────────────────
# EXAMPLE §L: WHY ROUTE D DEFERS TO REALISATION
# ─────────────────────────────────────────────────────────────

def example_l(data: dict) -> str:
    ex = data['examples']['L']

    lines = []

    # L.3.1
    lines.append("### L.3.1 Timeline A: Annual Cash Settlement (what Route D avoids)")
    lines.append("")
    lines.append("| Year | True V (£m) | Annual WDT liability (£m) | Cumulative liability (£m) |")
    lines.append("|:---:|---:|---:|---:|")
    for row in ex['annual_rows']:
        lines.append(f"| {row['yr']} | {row['V']:.3f} | {row['liab']:.3f} | {row['cum_liab']:.3f} |")
    lines.append("")

    # L.3.2
    lines.append("### L.3.2 Timeline B: Route D (deferred to inheritance at year 15)")
    lines.append("")
    N_d = ex['N_route_d']
    lines.append("| Event | Value (£m) |")
    lines.append("|:---|---:|")
    lines.append(f"| Entry basis $B_0$ | {fm(ex['V0'])} |")
    lines.append(f"| True value at inheritance (year {N_d}) | {fm(ex['V15'])} |")
    lines.append(f"| Total gain (V15 − $B_0$) | {fm(ex['V15'] - ex['V0'])} |")
    lines.append(f"| $\\tau$ at V15 | {fp(ex['rate15'])} |")
    lines.append(f"| WDT liability at inheritance | {fm(ex['liab15'])} |")
    lines.append(f"| Annual cash demand during years 1–{N_d} | £0.000m/year |")
    lines.append("")

    # L.3.3
    N_a = ex['N_annual']
    cum = ex['cum_liab']
    lines.append("### L.3.3 Comparison")
    lines.append("")
    lines.append("| Metric | Timeline A (annual) | Timeline B (Route D) |")
    lines.append("|:---|---:|---:|")
    lines.append(f"| Annual cash demand | {fm(cum/N_a)}/yr avg | £0.000m/yr |")
    lines.append(f"| Total tax collected | {fm(cum)} (yrs 1–5 only) | {fm(ex['liab15'])} (full 15 yrs) |")
    lines.append(f"| Forced realisation risk | High | None during holding |")
    lines.append(f"| Tax base | Partial appreciation | Full gain $B_0$ → V15 |")
    lines.append(f"| Settlement mechanism | Cash from external source | Cash from estate or auction |")
    lines.append("")
    lines.append(
        f"Route D collects more tax (full 15-year gain vs 5-year partial) while eliminating "
        f"the cash-demand problem. Annual settlement structurally undermines the tax base."
    )
    lines.append("")
    return '\n'.join(lines)


# ─────────────────────────────────────────────────────────────
# EXAMPLE §M: VOLUNTARY SETTLEMENT
# ─────────────────────────────────────────────────────────────

def example_m(data: dict) -> str:
    ex     = data['examples']['M']
    p_meta = data['params']

    soft  = ex['soft']
    hard  = ex['hard']
    death = ex['death']

    lines = []
    lines.append("## M.5 Comparison")
    lines.append("")
    lines.append(
        f"**Model note.** Liabilities calculated as $\\tau$(V) × (V − prior_basis) for each "
        f"settlement event. Computed true values: $V_{{10}}$ = {fm(ex['V10'])}, "
        f"$V_{{15}}$ = {fm(ex['V15'])} ($g$ = 5% compounded from $B_0$ = £5m). "
        f"Soft reset declared value: {fm(ex['V10_soft'])} (conservative, ~94% of true $V_{{10}}$)."
    )
    lines.append("")
    lines.append("| Metric | Option A: Soft reset (yr 10) | Option B: Hard reset (yr 10) | Option C: No reset (yr 15) |")
    lines.append("|:---|---:|---:|---:|")
    lines.append(f"| **Settlement value** | {fm(ex['V10_soft'])} (self-declared) | {fm(ex['V10'])} (auction) | {fm(ex['V15'])} (inheritance auction) |")
    lines.append(f"| **Gain from $B_0$ = £5m** | {fm(soft['gain'])} | {fm(hard['gain'])} | {fm(death['gain'])} |")
    lines.append(f"| **$\\tau$ at settlement** | {fp(soft['rate'])} | {fp(hard['rate'])} | {fp(death['rate'])} |")
    lines.append(f"| **WDT liability** | {fm(soft['liab'])} | {fm(hard['liab'])} | {fm(death['liab'])} |")
    lines.append(f"| **Auction costs** | nil | {fm(hard['auction_cost'])} | nil (estate cost) |")
    lines.append(f"| **New recognised basis** | {fm(ex['V10_soft'])} | {fm(ex['V10'])} | {fm(ex['V15'])} (heir's entry basis) |")
    lines.append(f"| **Basis verified?** | No (self-declared) | Yes (market auction) | Yes (inheritance auction) |")
    lines.append(f"| **Future refund basis** | Unverified | Market-verified | Market-verified |")
    lines.append("")
    lines.append(
        f"Table M.1: Voluntary settlement options compared. Entry basis £5m; "
        f"$g$ = 5% compounded. Python model v1.0 (closed-form arithmetic), $k$ = {p_meta['k']}."
    )
    lines.append("")
    return '\n'.join(lines)


# ─────────────────────────────────────────────────────────────
# EXAMPLE §N: FORECAST EXPOSURE
# ─────────────────────────────────────────────────────────────

def example_n(data: dict) -> str:
    ex     = data['examples']['N']
    p_meta = data['params']
    N      = ex['N']
    res    = ex['results']

    rA, rB, rC = res['1.0'], res['0.6'], res['1.4']
    sellA, sellB, sellC = rA['sell'], rB['sell'], rC['sell']

    def tax_paid(records):
        return sum(rec['L'] for rec in records[1:] if rec['L'] > 0)
    def refunds(records):
        return sum(rec['L'] for rec in records[1:] if rec['L'] < 0)

    tax_A = tax_paid(rA['records']); ref_A = refunds(rA['records'])
    tax_B = tax_paid(rB['records']); ref_B = refunds(rB['records'])
    tax_C = tax_paid(rC['records']); ref_C = refunds(rC['records'])

    tw_diff_B  = (rB['TW_settled'] - rA['TW_settled']) / rA['TW_settled'] * 100
    tw_diff_C  = (rC['TW_settled'] - rA['TW_settled']) / rA['TW_settled'] * 100
    net_diff_B = (rB['Net_settled'] - rA['Net_settled']) / rA['Net_settled'] * 100
    net_diff_C = (rC['Net_settled'] - rA['Net_settled']) / rA['Net_settled'] * 100
    eff_A = rA['Net_settled'] / rA['TW_settled'] * 100
    eff_B = rB['Net_settled'] / rB['TW_settled'] * 100
    eff_C = rC['Net_settled'] / rC['TW_settled'] * 100

    V0 = ex['V0_m']

    lines = []
    lines.append("## N.3 Illustrative Figures")
    lines.append("")
    lines.append("| Metric | Founder A ($\\alpha$=1.0) | Founder B ($\\alpha$=0.6) | Founder C ($\\alpha$=1.4) |")
    lines.append("|:---|---:|---:|---:|")
    lines.append(f"| **Entry basis** | {fm(V0 * 1.0)} | {fm(V0 * 0.6)} | {fm(V0 * 1.4)} |")
    lines.append(f"| **True value at sale (year 11)** | {fm(sellA['V_sell'])} | {fm(sellB['V_sell'])} | {fm(sellC['V_sell'])} |")
    lines.append(f"| **Tax paid years 1–10** | {fm(tax_A)} | {fm(tax_B)} | {fm(tax_C)} |")
    lines.append(f"| **Refunds received years 1–10** | {fm(abs(ref_A))} | {fm(abs(ref_B))} | {fm(abs(ref_C))} |")
    lines.append(f"| **Post-sale delta (year 11)** | {fm(sellA['delta_sell'])} | {fm(sellB['delta_sell'])} | {fm(sellC['delta_sell'])} |")
    lines.append(f"| **Tax/refund on post-sale delta** | {fm(sellA['L_sell'])} | {fm(sellB['L_sell'])} | {fm(sellC['L_sell'])} |")
    lines.append(f"| **Total lifetime WDT (Net)** | {fm(rA['Net_settled'])} | {fm(rB['Net_settled'])} | {fm(rC['Net_settled'])} |")
    lines.append(f"| **Terminal net worth (TW)** | {fm(rA['TW_settled'])} | {fm(rB['TW_settled'])} | {fm(rC['TW_settled'])} |")
    lines.append(f"| **TW vs Founder A** | — | {tw_diff_B:+.2f}% | {tw_diff_C:+.2f}% |")
    lines.append(f"| **Net tax vs Founder A** | — | {net_diff_B:+.2f}% | {net_diff_C:+.2f}% |")
    lines.append(f"| **Effective rate (Net/TW)** | {eff_A:.2f}% | {eff_B:.2f}% | {eff_C:.2f}% |")
    lines.append("")
    lines.append(
        f"Table N.1: Three-founder comparison, $g$ = 7%, N = 10, Route C, $\\tau$ = 15%. "
        f"Python model v1.0, $k$ = {p_meta['k']}."
    )
    lines.append("")

    # N.3.1 period-by-period
    lines.append("### N.3.1 Period-by-period: All three founders")
    lines.append("")
    lines.append("| t | V (£m) | A: W | A: L | A: f | B: W | B: L | B: f | C: W | C: L | C: f |")
    lines.append("|:---:|---:|---:|---:|:---:|---:|---:|:---:|---:|---:|:---:|")
    for t in range(N + 1):
        rAr = rA['records'][t]; rBr = rB['records'][t]; rCr = rC['records'][t]
        if t == 0:
            lines.append(
                f"| 0 | {rAr['V']:.3f} | {rAr['W']:.3f} | — | {rAr['f']:.4f} | "
                f"{rBr['W']:.3f} | — | {rBr['f']:.4f} | "
                f"{rCr['W']:.3f} | — | {rCr['f']:.4f} |"
            )
        else:
            lines.append(
                f"| {t} | {rAr['V']:.3f} | {rAr['W']:.3f} | {rAr['L']:.3f} | {rAr['f']:.4f} | "
                f"{rBr['W']:.3f} | {rBr['L']:.3f} | {rBr['f']:.4f} | "
                f"{rCr['W']:.3f} | {rCr['L']:.3f} | {rCr['f']:.4f} |"
            )
    sA = sellA; sB = sellB; sC = sellC
    lines.append(
        f"| sell | {sA['V_sell']:.3f} | {sA['W_sell']:.3f} | {sA['L_sell']:.3f} | {sA['f_N']:.4f} | "
        f"{sB['W_sell']:.3f} | {sB['L_sell']:.3f} | {sB['f_N']:.4f} | "
        f"{sC['W_sell']:.3f} | {sC['L_sell']:.3f} | {sC['f_N']:.4f} |"
    )
    lines.append("")

    # N.3.2 Key findings
    lines.append("### N.3.2 Key findings")
    lines.append("")
    refund_C   = abs(sC['L_sell']) if sC['L_sell'] < 0 else 0.0
    delta_sign = 'negative' if sellC['delta_sell'] < 0 else 'positive'

    lines.append(
        f"**Founder B (pessimist, $\\alpha$=0.6):** Paid {fm(tax_B)} in years 1–10 vs {fm(tax_A)} for Founder A. "
        f"At sale, the suppressed basis produced a large positive delta ({fm(sellB['delta_sell'])}). "
        f"Total net tax: {fm(rB['Net_settled'])} vs {fm(rA['Net_settled'])} for Founder A — "
        f"{net_diff_B:+.1f}% more despite lower annual payments. "
        f"Terminal wealth: {fm(rB['TW_settled'])} vs {fm(rA['TW_settled'])} — {tw_diff_B:+.1f}%."
    )
    lines.append("")
    lines.append(
        f"**Founder C (optimist, $\\alpha$=1.4):** Paid {fm(tax_C)} in years 1–10 vs {fm(tax_A)} for Founder A. "
        f"At sale, the inflated basis produced a {delta_sign} delta ({fm(sellC['delta_sell'])}) "
        f"→ refund of {fm(refund_C)}. "
        f"Total net tax: {fm(rC['Net_settled'])} vs {fm(rA['Net_settled'])} for Founder A — "
        f"{net_diff_C:+.1f}% relative to honest. "
        f"Terminal wealth: {fm(rC['TW_settled'])} vs {fm(rA['TW_settled'])} — {tw_diff_C:+.1f}%."
    )
    lines.append("")
    lines.append(
        f"**Founder A (honest, $\\alpha$=1.0):** No directional forecast exposure. Paid exactly "
        f"the tax on the wealth actually accumulated — {fm(rA['Net_settled'])} net, retaining "
        f"{fm(rA['TW_settled'])}. Neither Founder B nor C improves on this outcome at $g$=7%, N=10."
    )
    lines.append("")
    return '\n'.join(lines)


# ─────────────────────────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────────────────────────

def main():
    print("5_5_VAL_generate_worked_examples.py — loading val_data.json...")
    data = load_val_data()
    print(f"Data loaded. Generated: {data['meta']['generated']}")
    p    = data['params']

    ensure_dir(_OUT)
    out_path = _OUT / "VAL_Worked_Examples_Figures.md"

    lines = []
    lines.append("# VAL.B Worked Examples — Numerical Figures")
    lines.append("")
    lines.append(f"**Generated:** {date.today().isoformat()}  ")
    lines.append(
        f"**Model:** Python v1.0 standalone · Route C simulation throughout. "
        f"All figures use TW_settled/Net_settled (post-sale settlement correction). "
        f"Presented as TW/Net in table labels to match VAL.B nomenclature.  "
    )
    lines.append(
        f"**Parameters:** $\\tau_0$={p['tau_0']*100:.0f}%, $\\tau_m$={p['tau_m']*100:.0f}%, "
        f"$k$={p['k']}, $W_{{min}}$=£{p['W_min']:.0f}m (all examples unless stated).  "
    )
    lines.append(
        f"**Option A convention:** N annual periods used as assessment windows throughout.  "
        f"§K limitation: 3 annual periods used as proxy for 3 multi-year windows.  "
        f"§L and §M: bespoke closed-form arithmetic.  "
    )
    lines.append("")

    print("Example §J: Deferred delta...")
    lines.append(example_j(data))

    print("Example §K: Dilution compounds...")
    lines.append(example_k(data))

    print("Example §L: Route D vs annual...")
    lines.append(example_l(data))

    print("Example §M: Voluntary settlement...")
    lines.append(example_m(data))

    print("Example §N: Forecast exposure...")
    lines.append(example_n(data))

    md = '\n'.join(lines)
    out_path.write_text(md, encoding="utf-8")
    print(f"Written: {out_path}")
    print(f"Lines: {len(md.splitlines())}")


if __name__ == '__main__':
    main()
