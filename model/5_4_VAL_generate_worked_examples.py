"""
VAL Output Script C — Worked Example Figures
=============================================
Generates VAL_Worked_Examples_Figures.md

Produces the numerical figures for each worked example in VAL.B (§J–§N).
Output format matches VAL.B exactly:
  - Table captions BELOW each table: "Table J.1: description. params."
  - Column headers use LaTeX: $\\alpha$, $\\tau$, etc.
  - Metric row labels bolded: **Entry basis $B_0$**
  - Section headers match VAL.B: ## J.3 Illustrative Figures / ### J.3.1 / ### J.3.2
  - Summary rows use VAL.B field names: "Total lifetime WDT (Net)", "Terminal net worth (TW)"
  - Narrative text uses $\\alpha$ notation and matches VAL.B §J.3.2/§K.3.3/§N.3.2 prose

All figures are TW_settled/Net_settled internally but presented as TW/Net in the
table labels to match VAL.B nomenclature. The settled correction is acknowledged
in the preamble only.
"""

import os
from datetime import date
from pathlib import Path
from wdt_core import load_params, tau, simulate, simulate_sell, run_sim
from wdt_fmt import fmt_gbp_m as fm, fmt_pct as fp, out_dir, ensure_dir

_OUT = out_dir('VAL')

BASE_P = None  # set in main()


# ─────────────────────────────────────────────────────────────
# EXAMPLE §J: THE DEFERRED DELTA
# ─────────────────────────────────────────────────────────────

def example_j(base_p):
    p = dict(base_p); p['g'] = 0.07; p['N'] = 5; p['V0_m'] = 20.0
    alphas = [1.0, 0.8, 0.5]
    g = 0.07; N = 5

    lines = []
    lines.append("## J.3 Illustrative Figures")
    lines.append("")

    results = {alpha: run_sim(p, alpha=alpha, g=g, N=N) for alpha in alphas}
    r10 = results[1.0]; r08 = results[0.8]; r05 = results[0.5]
    sell10 = r10['sell']; sell08 = r08['sell']; sell05 = r05['sell']

    tax_10 = sum(r['L'] for r in r10['records'][1:] if r['L'] > 0)
    tax_08 = sum(r['L'] for r in r08['records'][1:] if r['L'] > 0)
    tax_05 = sum(r['L'] for r in r05['records'][1:] if r['L'] > 0)

    # Summary table — VAL.B J.3 format: no header row label, bolded metric names
    lines.append("| | **Honest ($\\alpha$ = 1.0)** | **Moderate under ($\\alpha$ = 0.8)** | **Significant under ($\\alpha$ = 0.5)** |")
    lines.append("|:---|---:|---:|---:|")
    lines.append(f"| **Entry basis $B_0$** | £20.000m | £16.000m | £10.000m |")
    lines.append(f"| **True value at sale $V_5$** | {fm(sell10['V_sell'])} | {fm(sell08['V_sell'])} | {fm(sell05['V_sell'])} |")
    lines.append(f"| **Tax paid years 1–5** | {fm(tax_10)} | {fm(tax_08)} | {fm(tax_05)} |")
    lines.append(f"| **Final delta on sale (year 6)** | {fm(sell10['delta_sell'])} | {fm(sell08['delta_sell'])} | {fm(sell05['delta_sell'])} |")
    lines.append(f"| **Tax on final delta** | {fm(max(0, sell10['L_sell']))} | {fm(max(0, sell08['L_sell']))} | {fm(max(0, sell05['L_sell']))} |")
    lines.append(f"| **Total lifetime WDT (Net)** | {fm(r10['Net_settled'])} | {fm(r08['Net_settled'])} | {fm(r05['Net_settled'])} |")
    lines.append(f"| **Terminal net worth (TW)** | {fm(r10['TW_settled'])} | {fm(r08['TW_settled'])} | {fm(r05['TW_settled'])} |")

    tw_diff_08 = (r08['TW_settled'] - r10['TW_settled']) / r10['TW_settled'] * 100
    tw_diff_05 = (r05['TW_settled'] - r10['TW_settled']) / r10['TW_settled'] * 100
    net_diff_08 = (r08['Net_settled'] - r10['Net_settled']) / r10['Net_settled'] * 100
    net_diff_05 = (r05['Net_settled'] - r10['Net_settled']) / r10['Net_settled'] * 100
    lines.append(f"| **TW vs honest** | — | {tw_diff_08:+.2f}% | {tw_diff_05:+.2f}% |")
    lines.append(f"| **Net tax vs honest** | — | {net_diff_08:+.2f}% | {net_diff_05:+.2f}% |")
    lines.append(f"")
    lines.append(f"Table J.1: Deferred delta comparison across declaration strategies, $g$ = 7%, N = 5, $\\tau$ = 15%. Python model v1.0, $k$ = {base_p['k']}.")
    lines.append(f"")

    # Period-by-period honest declarer — VAL.B §J.3.1 format
    lines.append("### J.3.1 Period-by-period: Honest declarer ($\\alpha$ = 1.0)")
    lines.append(f"")
    lines.append("| t | True V (£m) | Declared W (£m) | Delta (£m) | $\\tau$ | Tax L (£m) | f |")
    lines.append("|:---:|---:|---:|---:|:---:|---:|:---:|")
    for r in r10['records']:
        if r['t'] == 0:
            lines.append(f"| 0 (entry) | {r['V']:.3f} | {r['W']:.3f} | — | {fp(r['rate'])} | 0.000 | 1.0000 |")
        else:
            lines.append(f"| {r['t']} | {r['V']:.3f} | {r['W']:.3f} | {r['delta']:.3f} | {fp(r['rate'])} | {r['L']:.3f} | {r['f']:.4f} |")
    s = sell10
    lines.append(f"| 6 (sell) | {s['V_sell']:.3f} | {s['W_sell']:.3f} | {s['delta_sell']:.3f} | {fp(s['rate_sell'])} | {s['L_sell']:.3f} | {s['f_N']:.4f} |")
    lines.append(f"")

    # Key mechanism — VAL.B §J.3.2 format (inline prose, $\\alpha$ notation)
    lines.append("### J.3.2 Key mechanism: basis gap recovery at sale")
    lines.append(f"")
    extra_08 = sell08['delta_sell'] - sell10['delta_sell']
    extra_05 = sell05['delta_sell'] - sell10['delta_sell']
    more_tax_08 = max(0, sell08['L_sell']) - max(0, sell10['L_sell'])
    more_tax_05 = max(0, sell05['L_sell']) - max(0, sell10['L_sell'])
    net_cost_08 = r08['Net_settled'] - r10['Net_settled']
    net_cost_05 = r05['Net_settled'] - r10['Net_settled']
    saved_08 = tax_10 - tax_08
    saved_05 = tax_10 - tax_05

    lines.append(
        f"At the sell year, the final delta differs by declaration strategy: "
        f"honest ($\\alpha$ = 1.0) {fm(sell10['delta_sell'])} → tax {fm(max(0, sell10['L_sell']))}; "
        f"$\\alpha$ = 0.8 {fm(sell08['delta_sell'])} → tax {fm(max(0, sell08['L_sell']))} "
        f"(larger by {fm(extra_08)} due to suppressed basis); "
        f"$\\alpha$ = 0.5 {fm(sell05['delta_sell'])} → tax {fm(max(0, sell05['L_sell']))} "
        f"(larger by {fm(extra_05)} due to suppressed basis)."
    )
    lines.append(f"")
    lines.append(
        f"The $\\alpha$ = 0.8 understater saved {fm(saved_08)} in years 1–5 but paid "
        f"{fm(more_tax_08)} more at sale — net cost of understatement: {fm(net_cost_08)}. "
        f"The $\\alpha$ = 0.5 understater saved {fm(saved_05)} in years 1–5 but paid "
        f"{fm(more_tax_05)} more at sale — net cost of understatement: {fm(net_cost_05)}."
    )
    lines.append(f"")
    return '\n'.join(lines)


# ─────────────────────────────────────────────────────────────
# EXAMPLE §K: DILUTION COMPOUNDS WITH GROWTH
# ─────────────────────────────────────────────────────────────

def example_k(base_p):
    p = dict(base_p); p['g'] = 0.15; p['N'] = 3; p['V0_m'] = 20.0
    alphas = [1.0, 0.6]
    g = 0.15; N = 3

    lines = []
    lines.append("## K.3 Illustrative Figures")
    lines.append(f"")
    lines.append(
        f"**Model note.** (VAL.B §K) uses three *assessment windows* of unspecified length. "
        f"This model uses N = 3 *annual* periods as a proxy (Option A). A window-aware model would "
        f"produce different equity accumulation figures; the directional claim (dilution is more "
        f"expensive at high $g$) is unaffected. The model treats $V_0$ = £20m as the declared "
        f"portfolio (representing the stake value directly, not the company valuation at £20m with "
        f"a 60% stake = £12m stake value)."
    )
    lines.append(f"")

    results = {alpha: run_sim(p, alpha=alpha, g=g, N=N) for alpha in alphas}
    r10 = results[1.0]; r06 = results[0.6]

    # K.3.1 Period-by-period — VAL.B format
    lines.append("### K.3.1 Period-by-period accumulation")
    lines.append(f"")
    lines.append(
        "| Period | True V (£m) | Honest W (£m) | Honest f | Understater W (£m) | "
        "Understater f | State equity (honest) | State equity ($\\alpha$=0.6) |"
    )
    lines.append("|:---:|---:|---:|:---:|---:|:---:|:---:|:---:|")

    for t in range(N + 1):
        rh = r10['records'][t]
        ru = r06['records'][t]
        state_h = f"{(1.0 - rh['f'])*100:.3f}%" if t > 0 else "0.000%"
        state_u = f"{(1.0 - ru['f'])*100:.3f}%" if t > 0 else "0.000%"
        label = "entry" if t == 0 else str(t)
        lines.append(
            f"| {label} | {rh['V']:.3f} | {rh['W']:.3f} | {rh['f']:.4f} | "
            f"{ru['W']:.3f} | {ru['f']:.4f} | {state_h} | {state_u} |"
        )

    sh = r10['sell']; su = r06['sell']
    lines.append(
        f"| sell | {sh['V_sell']:.3f} | {sh['W_sell']:.3f} | {sh['f_N']:.4f} | "
        f"{su['W_sell']:.3f} | {su['f_N']:.4f} | "
        f"{(1-sh['f_N'])*100:.3f}% | {(1-su['f_N'])*100:.3f}% |"
    )
    lines.append(f"")

    # K.3.2 Summary — VAL.B format with bolded metric names
    state_true_h  = (1.0 - r10['records'][N]['f']) * r10['records'][N]['V']
    state_true_u  = (1.0 - r06['records'][N]['f']) * r06['records'][N]['V']
    founder_true_h = r10['records'][N]['f'] * r10['records'][N]['V']
    founder_true_u = r06['records'][N]['f'] * r06['records'][N]['V']
    implicit_cost = r06['Net_settled'] - r10['Net_settled']

    lines.append("### K.3.2 Summary at period N = 3")
    lines.append(f"")
    lines.append("| Metric | Honest ($\\alpha$ = 1.0) | Understater ($\\alpha$ = 0.6) |")
    lines.append("|:---|---:|---:|")
    lines.append(f"| **Founder retained fraction** | {r10['records'][N]['f']*100:.3f}% | {r06['records'][N]['f']*100:.3f}% |")
    lines.append(f"| **State equity stake** | {(1-r10['records'][N]['f'])*100:.3f}% | {(1-r06['records'][N]['f'])*100:.3f}% |")
    lines.append(f"| **True value of state stake (£m)** | {fm(state_true_h)} | {fm(state_true_u)} |")
    lines.append(f"| **True value of founder stake (£m)** | {fm(founder_true_h)} | {fm(founder_true_u)} |")
    lines.append(f"| **Tax paid (Net) (£m)** | {fm(r10['Net_settled'])} | {fm(r06['Net_settled'])} |")
    lines.append(f"| **Terminal net worth TW (£m)** | {fm(r10['TW_settled'])} | {fm(r06['TW_settled'])} |")
    lines.append(f"| **Implicit cost of understatement vs honest (£m)** | — | {fm(implicit_cost)} |")
    lines.append(f"")
    lines.append(
        f"Table K.1: Accumulated dilution under understatement, $g$ = 15%, Route C, "
        f"N = 3 annual periods as proxy for three-year window, $\\tau$ = 15%. "
        f"Python model v1.0, $k$ = {base_p['k']}."
    )
    lines.append(f"")

    # K.3.3 Key mechanism — VAL.B format
    lines.append("### K.3.3 Key mechanism: underpriced equity transfer")
    lines.append(f"")
    lines.append(
        f"The understater transfers equity at their declared value (60% of true value). "
        f"The state acquires this equity at a 40% discount to reality; it then appreciates at "
        f"the true rate (15% per year). After 3 periods, the state holds "
        f"{(1-r06['records'][N]['f'])*100:.3f}% vs {(1-r10['records'][N]['f'])*100:.3f}% for "
        f"the honest declarer. The understater has transferred less equity in percentage terms "
        f"but at a steeper discount, so net tax cost is higher: {fm(implicit_cost)} extra."
    )
    lines.append(f"")
    return '\n'.join(lines)


# ─────────────────────────────────────────────────────────────
# EXAMPLE §L: WHY ROUTE D DEFERS TO REALISATION
# ─────────────────────────────────────────────────────────────

def example_l(base_p):
    V0 = 8.0; g = 0.05
    N_annual = 5
    N_route_d = 15
    sim_p = {k: base_p[k] for k in ('k', 'tau_0', 'tau_m', 'W_min')}

    def tau_at(W):
        return tau(W, sim_p)

    lines = []

    # L.3.1 Timeline A
    lines.append("### L.3.1 Timeline A: Annual Cash Settlement (what Route D avoids)")
    lines.append(f"")
    lines.append("| Year | True V (£m) | Annual WDT liability (£m) | Cumulative liability (£m) |")
    lines.append("|:---:|---:|---:|---:|")

    V_prev = V0; cum_liab = 0.0
    for yr in range(1, N_annual + 1):
        V = V_prev * (1.0 + g)
        delta = V - V_prev
        rate = tau_at(V)
        liab = rate * delta
        cum_liab += liab
        lines.append(f"| {yr} | {V:.3f} | {liab:.3f} | {cum_liab:.3f} |")
        V_prev = V
    lines.append(f"")

    # L.3.2 Timeline B
    lines.append("### L.3.2 Timeline B: Route D (deferred to inheritance at year 15)")
    lines.append(f"")

    V15 = V0 * (1.0 + g) ** N_route_d
    V15_delta = V15 - V0
    rate_15 = tau_at(V15)
    liab_15 = rate_15 * V15_delta

    lines.append("| Event | Value (£m) |")
    lines.append("|:---|---:|")
    lines.append(f"| Entry basis $B_0$ | {fm(V0)} |")
    lines.append(f"| True value at inheritance (year {N_route_d}) | {fm(V15)} |")
    lines.append(f"| Total gain (V15 − $B_0$) | {fm(V15_delta)} |")
    lines.append(f"| $\\tau$ at V15 | {fp(rate_15)} |")
    lines.append(f"| WDT liability at inheritance | {fm(liab_15)} |")
    lines.append(f"| Annual cash demand during years 1–{N_route_d} | £0.000m/year |")
    lines.append(f"")

    # L.3.3 Comparison
    lines.append("### L.3.3 Comparison")
    lines.append(f"")
    lines.append("| Metric | Timeline A (annual) | Timeline B (Route D) |")
    lines.append("|:---|---:|---:|")
    lines.append(f"| Annual cash demand | {fm(cum_liab/N_annual)}/yr avg | £0.000m/yr |")
    lines.append(f"| Total tax collected | {fm(cum_liab)} (yrs 1–5 only) | {fm(liab_15)} (full 15 yrs) |")
    lines.append(f"| Forced realisation risk | High | None during holding |")
    lines.append(f"| Tax base | Partial appreciation | Full gain $B_0$ → V15 |")
    lines.append(f"| Settlement mechanism | Cash from external source | Cash from estate or auction |")
    lines.append(f"")
    lines.append(
        f"Route D collects more tax (full 15-year gain vs 5-year partial) while eliminating "
        f"the cash-demand problem. Annual settlement structurally undermines the tax base."
    )
    lines.append(f"")
    return '\n'.join(lines)


# ─────────────────────────────────────────────────────────────
# EXAMPLE §M: VOLUNTARY SETTLEMENT
# ─────────────────────────────────────────────────────────────

def example_m(base_p):
    B0 = 5.0; g = 0.05; N_reset = 10; N_death = 15
    sim_p = {k: base_p[k] for k in ('k', 'tau_0', 'tau_m', 'W_min')}

    def tau_at(W):
        return tau(W, sim_p)

    V10 = B0 * (1.0 + g) ** N_reset
    V15 = B0 * (1.0 + g) ** N_death
    V10_soft = V10 * 0.944

    # Option A
    gain_soft = V10_soft - B0
    rate_soft = tau_at(V10_soft)
    liab_soft = rate_soft * gain_soft

    # Option B
    gain_hard = V10 - B0
    rate_hard = tau_at(V10)
    liab_hard = rate_hard * gain_hard
    auction_cost = V10 * 0.02

    # Option C
    gain_death = V15 - B0
    rate_death = tau_at(V15)
    liab_death = rate_death * gain_death

    lines = []

    # M.5 Comparison — VAL.B format
    lines.append("## M.5 Comparison")
    lines.append(f"")
    lines.append(
        f"**Model note.** This example uses closed-form arithmetic, not run_val_sim. "
        f"Liabilities calculated as $\\tau$(V) × (V − prior_basis) for each settlement event. "
        f"Computed true values: $V_{{10}}$ = {fm(V10)}, $V_{{15}}$ = {fm(V15)} ($g$ = 5% compounded from $B_0$ = £5m). "
        f"Soft reset declared value: {fm(V10_soft)} (conservative, ~94% of true $V_{{10}}$), "
        f"consistent with Option A setup."
    )
    lines.append(f"")

    lines.append("| Metric | Option A: Soft reset (yr 10) | Option B: Hard reset (yr 10) | Option C: No reset (yr 15) |")
    lines.append("|:---|---:|---:|---:|")
    lines.append(f"| **Settlement value** | {fm(V10_soft)} (self-declared) | {fm(V10)} (auction) | {fm(V15)} (inheritance auction) |")
    lines.append(f"| **Gain from $B_0$ = £5m** | {fm(gain_soft)} | {fm(gain_hard)} | {fm(gain_death)} |")
    lines.append(f"| **$\\tau$ at settlement** | {fp(rate_soft)} | {fp(rate_hard)} | {fp(rate_death)} |")
    lines.append(f"| **WDT liability** | {fm(liab_soft)} | {fm(liab_hard)} | {fm(liab_death)} |")
    lines.append(f"| **Auction costs** | nil | {fm(auction_cost)} | nil (estate cost) |")
    lines.append(f"| **New recognised basis** | {fm(V10_soft)} | {fm(V10)} | {fm(V15)} (heir's entry basis) |")
    lines.append(f"| **Basis verified?** | No (self-declared) | Yes (market auction) | Yes (inheritance auction) |")
    lines.append(f"| **Future refund basis** | Unverified | Market-verified | Market-verified |")
    lines.append(f"")
    lines.append(
        f"Table M.1: Voluntary settlement options compared. Entry basis £5m; "
        f"$g$ = 5% compounded. Python model v1.0 (closed-form arithmetic), $k$ = {base_p['k']}."
    )
    lines.append(f"")
    return '\n'.join(lines)


# ─────────────────────────────────────────────────────────────
# EXAMPLE §N: FORECAST EXPOSURE
# ─────────────────────────────────────────────────────────────

def example_n(base_p):
    p = dict(base_p)
    p['V0_m'] = 8.0
    p['g']    = 0.07
    p['N']    = 10
    alphas = [1.0, 0.6, 1.4]
    g = 0.07; N = 10

    lines = []

    results = {alpha: run_sim(p, alpha=alpha, g=g, N=N) for alpha in alphas}
    rA = results[1.0]; rB = results[0.6]; rC = results[1.4]
    sellA = rA['sell']; sellB = rB['sell']; sellC = rC['sell']

    tax_A = sum(r['L'] for r in rA['records'][1:] if r['L'] > 0)
    tax_B = sum(r['L'] for r in rB['records'][1:] if r['L'] > 0)
    tax_C = sum(r['L'] for r in rC['records'][1:] if r['L'] > 0)
    ref_A = sum(r['L'] for r in rA['records'][1:] if r['L'] < 0)
    ref_B = sum(r['L'] for r in rB['records'][1:] if r['L'] < 0)
    ref_C = sum(r['L'] for r in rC['records'][1:] if r['L'] < 0)

    tw_diff_B  = (rB['TW_settled'] - rA['TW_settled']) / rA['TW_settled'] * 100
    tw_diff_C  = (rC['TW_settled'] - rA['TW_settled']) / rA['TW_settled'] * 100
    net_diff_B = (rB['Net_settled'] - rA['Net_settled']) / rA['Net_settled'] * 100
    net_diff_C = (rC['Net_settled'] - rA['Net_settled']) / rA['Net_settled'] * 100
    eff_A = rA['Net_settled'] / rA['TW_settled'] * 100
    eff_B = rB['Net_settled'] / rB['TW_settled'] * 100
    eff_C = rC['Net_settled'] / rC['TW_settled'] * 100

    # N.3 Summary table — VAL.B format
    lines.append("## N.3 Illustrative Figures")
    lines.append(f"")
    lines.append("| Metric | Founder A ($\\alpha$=1.0) | Founder B ($\\alpha$=0.6) | Founder C ($\\alpha$=1.4) |")
    lines.append("|:---|---:|---:|---:|")
    lines.append(f"| **Entry basis** | {fm(p['V0_m']*1.0)} | {fm(p['V0_m']*0.6)} | {fm(p['V0_m']*1.4)} |")
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
    lines.append(f"")
    lines.append(
        f"Table N.1: Three-founder comparison, $g$ = 7%, N = 10, Route C, $\\tau$ = 15%. "
        f"Python model v1.0, $k$ = {base_p['k']}."
    )
    lines.append(f"")

    # N.3.1 Period-by-period — VAL.B format
    lines.append("### N.3.1 Period-by-period: All three founders")
    lines.append(f"")
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
    sA = rA['sell']; sB = rB['sell']; sC = rC['sell']
    lines.append(
        f"| sell | {sA['V_sell']:.3f} | {sA['W_sell']:.3f} | {sA['L_sell']:.3f} | {sA['f_N']:.4f} | "
        f"{sB['W_sell']:.3f} | {sB['L_sell']:.3f} | {sB['f_N']:.4f} | "
        f"{sC['W_sell']:.3f} | {sC['L_sell']:.3f} | {sC['f_N']:.4f} |"
    )
    lines.append(f"")

    # N.3.2 Key findings — VAL.B format with $\\alpha$ notation
    lines.append("### N.3.2 Key findings")
    lines.append(f"")
    lines.append(
        f"**Founder B (pessimist, $\\alpha$=0.6):** Paid {fm(tax_B)} in years 1–10 vs {fm(tax_A)} for Founder A. "
        f"At sale, the suppressed basis produced a large positive delta ({fm(sellB['delta_sell'])}). "
        f"Total net tax: {fm(rB['Net_settled'])} vs {fm(rA['Net_settled'])} for Founder A — "
        f"{net_diff_B:+.1f}% more despite lower annual payments. "
        f"Terminal wealth: {fm(rB['TW_settled'])} vs {fm(rA['TW_settled'])} — {tw_diff_B:+.1f}%."
    )
    lines.append(f"")
    refund_C = abs(sC['L_sell']) if sC['L_sell'] < 0 else 0.0
    delta_sign = 'negative' if sellC['delta_sell'] < 0 else 'positive'
    lines.append(
        f"**Founder C (optimist, $\\alpha$=1.4):** Paid {fm(tax_C)} in years 1–10 vs {fm(tax_A)} for Founder A. "
        f"At sale, the inflated basis produced a {delta_sign} delta ({fm(sellC['delta_sell'])}) "
        f"→ refund of {fm(refund_C)}. "
        f"Total net tax: {fm(rC['Net_settled'])} vs {fm(rA['Net_settled'])} for Founder A — "
        f"{net_diff_C:+.1f}% relative to honest. "
        f"Terminal wealth: {fm(rC['TW_settled'])} vs {fm(rA['TW_settled'])} — {tw_diff_C:+.1f}%."
    )
    lines.append(f"")
    lines.append(
        f"**Founder A (honest, $\\alpha$=1.0):** No directional forecast exposure. Paid exactly "
        f"the tax on the wealth actually accumulated — {fm(rA['Net_settled'])} net, retaining "
        f"{fm(rA['TW_settled'])}. Neither Founder B nor C improves on this outcome at $g$=7%, N=10."
    )
    lines.append(f"")
    return '\n'.join(lines)


# ─────────────────────────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────────────────────────

def main():
    base_p = load_params()
    print(f"Parameters loaded: k={base_p['k']}, tau_0={base_p['tau_0']}, "
          f"tau_m={base_p['tau_m']}, W_min=£{base_p['W_min']}m")

    ensure_dir(_OUT)
    out_path = _OUT / "VAL_Worked_Examples_Figures.md"

    lines = []
    lines.append("# VAL.B Worked Examples — Numerical Figures")
    lines.append(f"")
    lines.append(f"**Generated:** {date.today().isoformat()}  ")
    lines.append(
        f"**Model:** Python v1.0 standalone · Route C simulation throughout. "
        f"All figures use TW_settled/Net_settled (post-sale settlement correction). "
        f"Presented as TW/Net in table labels to match VAL.B nomenclature.  "
    )
    lines.append(
        f"**Parameters:** $\\tau_0$={base_p['tau_0']*100:.0f}%, $\\tau_m$={base_p['tau_m']*100:.0f}%, "
        f"$k$={base_p['k']}, $W_{{min}}$=£{base_p['W_min']:.0f}m (all examples unless stated).  "
    )
    lines.append(
        f"**Option A convention:** N annual periods used as assessment windows throughout.  "
        f"§K limitation: 3 annual periods used as proxy for 3 multi-year windows — "
        f"expected to produce variance from a window-aware model; directional claims unaffected.  "
        f"§L and §M: bespoke closed-form arithmetic, not run_val_sim.  "
    )
    lines.append(f"")

    print("Example §J: Deferred delta...")
    lines.append(example_j(base_p))

    print("Example §K: Dilution compounds...")
    lines.append(example_k(base_p))

    print("Example §L: Route D vs annual...")
    lines.append(example_l(base_p))

    print("Example §M: Voluntary settlement...")
    lines.append(example_m(base_p))

    print("Example §N: Forecast exposure...")
    lines.append(example_n(base_p))

    md = '\n'.join(lines)
    out_path.write_text(md, encoding="utf-8")
    print(f"Written: {out_path}")
    print(f"Lines: {len(md.splitlines())}")


if __name__ == '__main__':
    main()
