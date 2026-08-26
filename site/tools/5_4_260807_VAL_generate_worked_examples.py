"""
VAL Output Script C — Worked Example Figures
=============================================
Generates VAL_Worked_Examples_Figures.md

Produces the numerical figures for each worked example in VAL.B (§J–§N).
Each example uses the setup specified in VAL.B, with Option A convention
(N annual periods = N assessment windows) throughout.

Example setups:
  §J: Deferred delta       — Route C, α∈{1.0,0.8,0.5}, g=7%, N=5, $V_0$=£20m
  §K: Dilution compounds   — Route C, α∈{1.0,0.6}, g=15%, N=3, $V_0$=£20m
  §L: Route D vs annual    — Bespoke cash-flow illustration, g=5%, $V_0$=£8m
  §M: Voluntary settlement — Route D illustration, g=5%, $V_0$=£5m, N=10/15
  §N: Forecast exposure    — Route C, α∈{1.0,0.6,1.4}, g=7%, N=10, $V_0$=£8m (40% of £20m)

Model limitation notes are included per example.
All monetary values in £m. $\tau_0$=20%, $\tau_m$=70%, k=0.0001, W_min=£2m throughout
unless stated otherwise.
"""

import os
from datetime import date
from wdt_core import load_params, tau, simulate, simulate_sell, run_sim
from val_helpers import OUT_DIR, fm, fp

# BASE_P is built from load_params() in main() and passed to each example.
# Each example then overrides g, N, V0_m locally as before.
# The rate-function keys (k, tau_0, tau_m, W_min) come from the TOML.


# ─────────────────────────────────────────────────────────────
# EXAMPLE §J: THE DEFERRED DELTA
# Route C, α∈{1.0, 0.8, 0.5}, g=7%, N=5, $V_0$=£20m
# Illustrates: understatement defers, not eliminates
# ─────────────────────────────────────────────────────────────

def example_j(base_p):
    p = dict(base_p); p['g'] = 0.07; p['N'] = 5; p['V0_m'] = 20.0
    alphas = [1.0, 0.8, 0.5]
    g = 0.07; N = 5

    lines = []
    lines.append("## §J: The Deferred Delta")
    lines.append("")
    lines.append("**Setup:** Route C fungible asset · $V_0$ = £20m · g = 7% · N = 5 years · τ = 20% at entry")
    lines.append("**Claim illustrated:** VAL §1, §5.3 — understatement defers tax, does not eliminate it.")
    lines.append("**Model note:** Annual periods used as assessment windows (Option A).")
    lines.append("")

    results = {alpha: run_sim(p, alpha=alpha, g=g, N=N) for alpha in alphas}

    # Summary table (matches Table J.1 in VAL.B)
    lines.append("### Table J.1: Deferred Delta Comparison")
    lines.append("")
    lines.append("| Metric | Honest (α=1.0) | Moderate under (α=0.8) | Significant under (α=0.5) |")
    lines.append("|:---|---:|---:|---:|")

    r10 = results[1.0]; r08 = results[0.8]; r05 = results[0.5]
    sell10 = r10['sell']; sell08 = r08['sell']; sell05 = r05['sell']

    lines.append(f"| Entry basis B₀ | {fm(20.0*1.0)} | {fm(20.0*0.8)} | {fm(20.0*0.5)} |")
    lines.append(f"| True value at sale V₅ | {fm(sell10['V_sell'])} | {fm(sell08['V_sell'])} | {fm(sell05['V_sell'])} |")

    tax_10_15 = sum(r['L'] for r in r10['records'][1:] if r['L'] > 0)
    tax_08_15 = sum(r['L'] for r in r08['records'][1:] if r['L'] > 0)
    tax_05_15 = sum(r['L'] for r in r05['records'][1:] if r['L'] > 0)
    lines.append(f"| Tax paid years 1–5 | {fm(tax_10_15)} | {fm(tax_08_15)} | {fm(tax_05_15)} |")
    lines.append(f"| Final delta on sale (year 6) | {fm(sell10['delta_sell'])} | {fm(sell08['delta_sell'])} | {fm(sell05['delta_sell'])} |")
    lines.append(f"| Tax on final delta | {fm(max(0,sell10['L_sell']))} | {fm(max(0,sell08['L_sell']))} | {fm(max(0,sell05['L_sell']))} |")
    lines.append(f"| Total lifetime WDT (Net) | {fm(r10['Net'])} | {fm(r08['Net'])} | {fm(r05['Net'])} |")
    lines.append(f"| Terminal net worth (TW) | {fm(r10['TW'])} | {fm(r08['TW'])} | {fm(r05['TW'])} |")
    lines.append(f"| TW vs honest | — | {(r08['TW']-r10['TW'])/r10['TW']*100:+.2f}% | {(r05['TW']-r10['TW'])/r10['TW']*100:+.2f}% |")
    lines.append(f"| Net tax vs honest | — | {(r08['Net']-r10['Net'])/r10['Net']*100:+.2f}% | {(r05['Net']-r10['Net'])/r10['Net']*100:+.2f}% |")
    lines.append("")

    # Period-by-period detail for honest (α=1.0) only to show mechanism
    lines.append("### Period-by-period: Honest declarer (α=1.0)")
    lines.append("")
    lines.append("| t | True V (£m) | Declared W (£m) | Delta (£m) | τ | Tax L (£m) | f |")
    lines.append("|:---:|---:|---:|---:|:---:|---:|:---:|")
    for r in r10['records']:
        if r['t'] == 0:
            lines.append(f"| 0 (entry) | {r['V']:.3f} | {r['W']:.3f} | — | {fp(r['rate'])} | 0.000 | 1.0000 |")
        else:
            lines.append(f"| {r['t']} | {r['V']:.3f} | {r['W']:.3f} | {r['delta']:.3f} | {fp(r['rate'])} | {r['L']:.3f} | {r['f']:.4f} |")
    s = sell10
    lines.append(f"| 6 (sell) | {s['V_sell']:.3f} | {s['W_sell']:.3f} | {s['delta_sell']:.3f} | {fp(s['rate_sell'])} | {s['L_sell']:.3f} | {s['f_N']:.4f} |")
    lines.append("")

    # Highlight the key mechanism
    lines.append("### Key mechanism: basis gap recovery at sale")
    lines.append("")
    lines.append(f"At the sell year, the final delta differs by declaration strategy:")
    lines.append(f"- Honest (α=1.0): final delta = {fm(sell10['delta_sell'])} → tax = {fm(max(0,sell10['L_sell']))}")
    lines.append(f"- α=0.8: final delta = {fm(sell08['delta_sell'])} → tax = {fm(max(0,sell08['L_sell']))} "
                 f"(larger by {fm(sell08['delta_sell']-sell10['delta_sell'])} due to suppressed basis)")
    lines.append(f"- α=0.5: final delta = {fm(sell05['delta_sell'])} → tax = {fm(max(0,sell05['L_sell']))} "
                 f"(larger by {fm(sell05['delta_sell']-sell10['delta_sell'])} due to suppressed basis)")
    lines.append("")
    lines.append(f"The α=0.8 understater saved {fm(tax_10_15-tax_08_15)} in years 1–5 but paid "
                 f"{fm(max(0,sell08['L_sell'])-max(0,sell10['L_sell']))} more at sale — "
                 f"net cost of understatement: {fm(r08['Net']-r10['Net'])}.")
    lines.append(f"The α=0.5 understater saved {fm(tax_10_15-tax_05_15)} in years 1–5 but paid "
                 f"{fm(max(0,sell05['L_sell'])-max(0,sell10['L_sell']))} more at sale — "
                 f"net cost of understatement: {fm(r05['Net']-r10['Net'])}.")
    lines.append("")
    return '\n'.join(lines)


# ─────────────────────────────────────────────────────────────
# EXAMPLE §K: DILUTION COMPOUNDS WITH GROWTH
# Route C, α∈{1.0, 0.6}, g=15%, N=3 (Option A), $V_0$=£20m
# Illustrates: must-transfer rule costs track the asset's trajectory
# ─────────────────────────────────────────────────────────────

def example_k(base_p):
    p = dict(base_p); p['g'] = 0.15; p['N'] = 3; p['V0_m'] = 20.0
    alphas = [1.0, 0.6]
    g = 0.15; N = 3

    lines = []
    lines.append("## §K: Dilution Compounds with Growth")
    lines.append("")
    lines.append("**Setup:** Route C, 60% founder stake · $V_0$ = £20m · g = 15% · N = 3")
    lines.append("**Claim illustrated:** VAL §5.2 — must-transfer cost tracks the asset's trajectory.")
    lines.append("")
    lines.append("**Model limitation (Option A).** VAL.B §K uses three *assessment windows* of")
    lines.append("unspecified length. This model uses N=3 *annual* periods as a proxy.")
    lines.append("A window-aware model would produce different equity accumulation figures.")
    lines.append("The directional claim (dilution is more expensive at high g) is unaffected.")
    lines.append("")
    lines.append("**Founder stake framing.** The model treats the full $V_0$ = £20m as the")
    lines.append("declared portfolio. VAL.B §K describes a 60% stake in a company worth £20m")
    lines.append("total (stake value £12m). For comparability the model runs at $V_0$=£20m")
    lines.append("representing the stake value directly, not the company valuation.")
    lines.append("")

    results = {alpha: run_sim(p, alpha=alpha, g=g, N=N) for alpha in alphas}
    r10 = results[1.0]; r06 = results[0.6]

    # Build equity accumulation table
    lines.append("### Table K.1: Accumulated Dilution Under Understatement")
    lines.append("")
    lines.append("| Period | True V (£m) | Honest W (£m) | Honest f | Understater W (£m) | Understater f | State equity (honest) | State equity (α=0.6) |")
    lines.append("|:---:|---:|---:|:---:|---:|:---:|:---:|:---:|")

    for t in range(N + 1):
        rh = r10['records'][t]
        ru = r06['records'][t]
        state_h = f"{(1.0 - rh['f'])*100:.3f}%" if t > 0 else "0.000%"
        state_u = f"{(1.0 - ru['f'])*100:.3f}%" if t > 0 else "0.000%"
        label = "entry" if t == 0 else str(t)
        lines.append(f"| {label} | {rh['V']:.3f} | {rh['W']:.3f} | {rh['f']:.4f} | "
                     f"{ru['W']:.3f} | {ru['f']:.4f} | {state_h} | {state_u} |")

    # Sell year
    sh = r10['sell']; su = r06['sell']
    lines.append(f"| sell | {sh['V_sell']:.3f} | {sh['W_sell']:.3f} | {sh['f_N']:.4f} | "
                 f"{su['W_sell']:.3f} | {su['f_N']:.4f} | "
                 f"{(1-sh['f_N'])*100:.3f}% | {(1-su['f_N'])*100:.3f}% |")
    lines.append("")

    # True value of state stake at N=3
    state_true_h  = (1.0 - r10['records'][N]['f']) * r10['records'][N]['V']
    state_true_u  = (1.0 - r06['records'][N]['f']) * r06['records'][N]['V']
    founder_true_h = r10['records'][N]['f'] * r10['records'][N]['V']
    founder_true_u = r06['records'][N]['f'] * r06['records'][N]['V']

    lines.append("### Summary at period N=3")
    lines.append("")
    lines.append(f"| Metric | Honest (α=1.0) | Understater (α=0.6) |")
    lines.append(f"|:---|---:|---:|")
    lines.append(f"| Founder retained fraction | {r10['records'][N]['f']*100:.3f}% | {r06['records'][N]['f']*100:.3f}% |")
    lines.append(f"| State equity stake | {(1-r10['records'][N]['f'])*100:.3f}% | {(1-r06['records'][N]['f'])*100:.3f}% |")
    lines.append(f"| True value of state stake (£m) | {fm(state_true_h)} | {fm(state_true_u)} |")
    lines.append(f"| True value of founder stake (£m) | {fm(founder_true_h)} | {fm(founder_true_u)} |")
    lines.append(f"| Tax paid (Net) (£m) | {fm(r10['Net'])} | {fm(r06['Net'])} |")
    lines.append(f"| Terminal net worth TW (£m) | {fm(r10['TW'])} | {fm(r06['TW'])} |")
    lines.append(f"| Implicit cost of understatement vs honest (£m) | — | {fm(r06['Net']-r10['Net'])} |")
    lines.append("")

    # Key mechanism explanation
    lines.append("### Key mechanism: underpriced equity transfer")
    lines.append("")
    lines.append(f"The understater transfers equity at their declared value (60% of true value).")
    lines.append(f"The state acquires this equity at an underpriced rate; it then appreciates at")
    lines.append(f"the true rate (15% per year). After {N} periods:")
    lines.append(f"- Honest: state holds {(1-r10['records'][N]['f'])*100:.3f}% of the asset, true value {fm(state_true_h)}")
    lines.append(f"- Understater: state holds {(1-r06['records'][N]['f'])*100:.3f}% of the asset, true value {fm(state_true_u)}")
    lines.append(f"")
    lines.append(f"The understater's state stake is worth {fm(state_true_u)} vs {fm(state_true_h)} for the honest")
    lines.append(f"declarer — the understater has transferred more economic value per unit of tax paid.")
    lines.append(f"This gap is the 'implicit cost of understatement' under Route C: {fm(r06['Net']-r10['Net'])} extra net tax.")
    lines.append("")
    return '\n'.join(lines)


# ─────────────────────────────────────────────────────────────
# EXAMPLE §L: WHY ROUTE D DEFERS TO REALISATION
# Bespoke cash-flow illustration (not run_val_sim)
# g=5%, $V_0$=£8m (sculpture collection entry value)
# ─────────────────────────────────────────────────────────────

def example_l(base_p):
    # Timeline A: annual cash settlement (what Route D avoids)
    # Timeline B: Route D (deferred to realisation at year 15)
    V0 = 8.0; g = 0.05
    N_annual = 5   # years for Timeline A comparison
    N_route_d = 15 # years Route D holds to inheritance

    sim_p = {k: base_p[k] for k in ('k', 'tau_0', 'tau_m', 'W_min')}

    def tau_at(W):
        return tau(W, sim_p)

    lines = []
    lines.append("## §L: Why Route D Defers to Realisation")
    lines.append("")
    lines.append("**Setup:** Sculpture collection · Entry basis B₀ = £8m · g = 5% · τ ≈ 20% at entry")
    lines.append("**Claim illustrated:** VAL §6.1 — annual cash settlement on illiquid assets")
    lines.append("recreates forced-realisation pressure; Route D avoids this.")
    lines.append("")
    lines.append("**Model note.** This example uses bespoke cash-flow arithmetic, not run_val_sim.")
    lines.append("The WDT liability is approximated as τ(V_t) × (V_t − V_{t-1}) in each year,")
    lines.append("treating the collection as honestly self-declared at true value each period.")
    lines.append("This understates the mechanism detail but captures the cash-demand structure.")
    lines.append("")

    # Timeline A: annual cash settlement for 5 years
    lines.append("### Timeline A: Annual Cash Settlement (what Route D avoids)")
    lines.append("")
    lines.append("| Year | True V (£m) | Annual WDT liability (£m) | Cumulative liability (£m) |")
    lines.append("|:---:|---:|---:|---:|")

    V = V0; cum_liab = 0.0
    tl_a_rows = []
    V_prev = V0
    for yr in range(1, N_annual + 1):
        V = V_prev * (1.0 + g)
        delta = V - V_prev
        rate = tau_at(V)
        liab = rate * delta
        cum_liab += liab
        tl_a_rows.append((yr, V, liab, cum_liab))
        lines.append(f"| {yr} | {V:.3f} | {liab:.3f} | {cum_liab:.3f} |")
        V_prev = V
    lines.append("")
    lines.append(f"**Total annual WDT liability over {N_annual} years: {fm(cum_liab)}**")
    lines.append(f"This cash must be sourced from outside the illiquid collection. If funded by")
    lines.append(f"distress-selling individual works, the collection's value is impaired in the")
    lines.append(f"process — the tax partially destroys the value it is attempting to capture.")
    lines.append("")

    # Timeline B: Route D — deferred to inheritance at year 15
    lines.append("### Timeline B: Route D (deferred to inheritance at year 15)")
    lines.append("")
    V15 = V0 * (1.0 + g) ** N_route_d
    V15_delta = V15 - V0
    rate_15 = tau_at(V15)
    liab_15 = rate_15 * V15_delta

    lines.append(f"| Event | Value (£m) |")
    lines.append(f"|:---|---:|")
    lines.append(f"| Entry basis B₀ | {fm(V0)} |")
    lines.append(f"| True value at inheritance (year {N_route_d}) | {fm(V15)} |")
    lines.append(f"| Total gain (V15 − B₀) | {fm(V15_delta)} |")
    lines.append(f"| τ at V15 | {fp(rate_15)} |")
    lines.append(f"| WDT liability at inheritance | {fm(liab_15)} |")
    lines.append(f"| No annual cash demand during years 1–{N_route_d} | £0.000m/year |")
    lines.append("")
    lines.append(f"**Full 15-year appreciation is taxed in one calculation at realisation.**")
    lines.append(f"No forced sale occurred during the holding period. The heir pays {fm(liab_15)}")
    lines.append(f"from estate liquid assets and retains the collection, or allows the")
    lines.append(f"inheritance auction to establish a market price and settles from proceeds.")
    lines.append("")

    # Comparison
    lines.append("### Comparison")
    lines.append("")
    lines.append(f"| Metric | Timeline A (annual) | Timeline B (Route D) |")
    lines.append(f"|:---|---:|---:|")
    lines.append(f"| Annual cash demand | {fm(cum_liab/N_annual)}/yr avg | £0.000m/yr |")
    lines.append(f"| Total tax collected | {fm(cum_liab)} (yrs 1–5 only) | {fm(liab_15)} (full 15 yrs) |")
    lines.append(f"| Forced realisation risk | High | None during holding |")
    lines.append(f"| Tax base | Partial appreciation | Full gain B₀ → V15 |")
    lines.append(f"| Settlement mechanism | Cash from external source | Cash from estate or auction |")
    lines.append("")
    lines.append("*Route D collects more tax (full 15-year gain vs 5-year partial) while")
    lines.append("eliminating the cash-demand problem. Annual settlement is not just")
    lines.append("administratively inconvenient — it structurally undermines the tax base.*")
    lines.append("")
    return '\n'.join(lines)


# ─────────────────────────────────────────────────────────────
# EXAMPLE §M: VOLUNTARY SETTLEMENT
# Route D illustration, g=5%, $V_0$=£5m, N=10 (options A/B), N=15 (option C)
# ─────────────────────────────────────────────────────────────

def example_m(base_p):
    B0 = 5.0; g = 0.05; N_reset = 10; N_death = 15
    sim_p = {k: base_p[k] for k in ('k', 'tau_0', 'tau_m', 'W_min')}

    def tau_at(W):
        return tau(W, sim_p)

    V10 = B0 * (1.0 + g) ** N_reset
    V15 = B0 * (1.0 + g) ** N_death
    V10_soft = V10 * 0.944   # conservative self-declaration at £8.5m, scaled

    lines = []
    lines.append("## §M: Voluntary Settlement — Certainty, Not Avoidance")
    lines.append("")
    lines.append("**Setup:** Commercial property · B₀ = £5m · g = 5% · Approximate V₁₀ ≈ £8.15m")
    lines.append("**Claim illustrated:** VAL §6.4 — soft and hard basis resets give certainty, not avoidance.")
    lines.append("")
    lines.append("**Model note.** This example uses closed-form arithmetic, not run_val_sim.")
    lines.append("Liabilities calculated as τ(V) × (V − prior_basis) for each settlement event.")
    lines.append("VAL.B §M specifies V₁₀ ≈ £9m (true) and a soft reset declared at £8.5m.")
    lines.append("This model uses g=5% compounded: V₁₀ = £8.144m, V₁₅ = £10.395m.")
    lines.append("")

    # True values
    lines.append(f"**Computed true values:** V₁₀ = {fm(V10)}, V₁₅ = {fm(V15)}")
    lines.append(f"**Soft reset declared value (Option A):** {fm(V10_soft)} (conservative, ~94% of true)")
    lines.append("")

    # Option A: Soft basis reset at year 10
    gain_soft = V10_soft - B0
    rate_soft = tau_at(V10_soft)
    liab_soft = rate_soft * gain_soft

    # Option B: Hard basis reset at year 10 (auction at true value)
    gain_hard = V10 - B0
    rate_hard = tau_at(V10)
    liab_hard = rate_hard * gain_hard
    auction_cost = V10 * 0.02  # approx 2% auction costs

    # Option C: No reset, inheritance at year 15
    gain_death = V15 - B0
    rate_death = tau_at(V15)
    liab_death = rate_death * gain_death

    lines.append("### Table M.1: Voluntary Settlement Options Compared")
    lines.append("")
    lines.append("| Metric | Option A: Soft reset (yr 10) | Option B: Hard reset (yr 10) | Option C: No reset (yr 15) |")
    lines.append("|:---|---:|---:|---:|")
    lines.append(f"| Settlement value | {fm(V10_soft)} (self-declared) | {fm(V10)} (auction) | {fm(V15)} (inheritance auction) |")
    lines.append(f"| Gain from B₀ = £5m | {fm(gain_soft)} | {fm(gain_hard)} | {fm(gain_death)} |")
    lines.append(f"| τ at settlement | {fp(rate_soft)} | {fp(rate_hard)} | {fp(rate_death)} |")
    lines.append(f"| WDT liability | {fm(liab_soft)} | {fm(liab_hard)} | {fm(liab_death)} |")
    lines.append(f"| Auction costs | nil | {fm(auction_cost)} | nil (estate cost) |")
    lines.append(f"| New recognised basis | {fm(V10_soft)} | {fm(V10)} | {fm(V15)} (heir's entry basis) |")
    lines.append(f"| Basis verified? | No (self-declared) | Yes (market auction) | Yes (inheritance auction) |")
    lines.append(f"| Future refund basis | Unverified | Market-verified | Market-verified |")
    lines.append("")
    lines.append("*Liabilities calculated at τ(settlement value) × gain from B₀. g=5%, compounded.*")
    lines.append("")

    # Key insight
    lines.append("### What the example shows")
    lines.append("")
    lines.append(f"None of the three options avoids the WDT. The full gain from B₀ to settlement")
    lines.append(f"value is taxed in every case. Option A settles earlier at a conservative")
    lines.append(f"self-declared value: lower immediate liability ({fm(liab_soft)}) but an unverified")
    lines.append(f"basis for future calculations. Option B settles at market: higher liability")
    lines.append(f"({fm(liab_hard)}) plus auction costs ({fm(auction_cost)}) but a verified basis.")
    lines.append(f"Option C defers to inheritance: largest single liability ({fm(liab_death)}),")
    lines.append(f"timing set by death rather than the taxpayer's choice.")
    lines.append("")
    lines.append(f"Present value favours earlier settlement only if the marginal rate at year 10")
    lines.append(f"({fp(rate_soft)}–{fp(rate_hard)}) is materially lower than at year 15 ({fp(rate_death)}),")
    lines.append(f"which at these wealth levels is approximately true but not decisive at the")
    lines.append(f"reference k=0.0001 (the rate function is relatively flat in this range).")
    lines.append("")
    return '\n'.join(lines)


# ─────────────────────────────────────────────────────────────
# EXAMPLE §N: FORECAST EXPOSURE
# Route C, α∈{1.0, 0.6, 1.4}, g=7%, N=10, $V_0$=£8m (40% stake of £20m company)
# Illustrates: honest declaration has no directional exposure to trajectory
# ─────────────────────────────────────────────────────────────

def example_n(base_p):
    p = dict(base_p)
    p['V0_m'] = 8.0   # 40% stake in a £20m company
    p['g']    = 0.07
    p['N']    = 10
    alphas = [1.0, 0.6, 1.4]
    g = 0.07; N = 10

    lines = []
    lines.append("## §N: Forecast Exposure")
    lines.append("")
    lines.append("**Setup:** Route C · Three founders, identical 40% stakes · $V_0$ = £8m (each) · g = 7% · N = 10")
    lines.append("**Claim illustrated:** VAL §7.1 — honest declaration has no directional forecast exposure.")
    lines.append("**Founders:** A (α=1.0, honest), B (α=0.6, expects underperformance), C (α=1.4, expects outperformance)")
    lines.append("")

    results = {alpha: run_sim(p, alpha=alpha, g=g, N=N) for alpha in alphas}
    rA = results[1.0]; rB = results[0.6]; rC = results[1.4]
    sellA = rA['sell']; sellB = rB['sell']; sellC = rC['sell']

    # Summary table matching Table N.1 in VAL.B
    lines.append("### Table N.1: Three-Founder Comparison")
    lines.append("")
    lines.append("| Metric | Founder A (α=1.0) | Founder B (α=0.6) | Founder C (α=1.4) |")
    lines.append("|:---|---:|---:|---:|")

    tax_A_110 = sum(r['L'] for r in rA['records'][1:] if r['L'] > 0)
    tax_B_110 = sum(r['L'] for r in rB['records'][1:] if r['L'] > 0)
    tax_C_110 = sum(r['L'] for r in rC['records'][1:] if r['L'] > 0)
    ref_A_110 = sum(r['L'] for r in rA['records'][1:] if r['L'] < 0)
    ref_B_110 = sum(r['L'] for r in rB['records'][1:] if r['L'] < 0)
    ref_C_110 = sum(r['L'] for r in rC['records'][1:] if r['L'] < 0)

    lines.append(f"| Entry basis | {fm(p['V0_m']*1.0)} | {fm(p['V0_m']*0.6)} | {fm(p['V0_m']*1.4)} |")
    lines.append(f"| True value at sale (year 11) | {fm(sellA['V_sell'])} | {fm(sellB['V_sell'])} | {fm(sellC['V_sell'])} |")
    lines.append(f"| Tax paid years 1–10 | {fm(tax_A_110)} | {fm(tax_B_110)} | {fm(tax_C_110)} |")
    lines.append(f"| Refunds received years 1–10 | {fm(abs(ref_A_110))} | {fm(abs(ref_B_110))} | {fm(abs(ref_C_110))} |")
    lines.append(f"| Post-sale delta (year 11) | {fm(sellA['delta_sell'])} | {fm(sellB['delta_sell'])} | {fm(sellC['delta_sell'])} |")
    lines.append(f"| Tax/refund on post-sale delta | {fm(sellA['L_sell'])} | {fm(sellB['L_sell'])} | {fm(sellC['L_sell'])} |")
    lines.append(f"| Total lifetime WDT (Net) | {fm(rA['Net'])} | {fm(rB['Net'])} | {fm(rC['Net'])} |")
    lines.append(f"| Terminal net worth (TW) | {fm(rA['TW'])} | {fm(rB['TW'])} | {fm(rC['TW'])} |")
    lines.append(f"| TW vs Founder A | — | {(rB['TW']-rA['TW'])/rA['TW']*100:+.2f}% | {(rC['TW']-rA['TW'])/rA['TW']*100:+.2f}% |")
    lines.append(f"| Net tax vs Founder A | — | {(rB['Net']-rA['Net'])/rA['Net']*100:+.2f}% | {(rC['Net']-rA['Net'])/rA['Net']*100:+.2f}% |")
    lines.append(f"| Effective rate (Net/TW) | {rA['Net']/rA['TW']*100:.2f}% | {rB['Net']/rB['TW']*100:.2f}% | {rC['Net']/rC['TW']*100:.2f}% |")
    lines.append("")

    # Period-by-period for all three founders
    lines.append("### Period-by-period: All three founders")
    lines.append("")
    lines.append("| t | V (£m) | A: W | A: L | A: f | B: W | B: L | B: f | C: W | C: L | C: f |")
    lines.append("|:---:|---:|---:|---:|:---:|---:|---:|:---:|---:|---:|:---:|")
    for t in range(N + 1):
        rAr = rA['records'][t]; rBr = rB['records'][t]; rCr = rC['records'][t]
        if t == 0:
            lines.append(f"| 0 | {rAr['V']:.3f} | {rAr['W']:.3f} | — | {rAr['f']:.4f} | "
                         f"{rBr['W']:.3f} | — | {rBr['f']:.4f} | "
                         f"{rCr['W']:.3f} | — | {rCr['f']:.4f} |")
        else:
            lines.append(f"| {t} | {rAr['V']:.3f} | {rAr['W']:.3f} | {rAr['L']:.3f} | {rAr['f']:.4f} | "
                         f"{rBr['W']:.3f} | {rBr['L']:.3f} | {rBr['f']:.4f} | "
                         f"{rCr['W']:.3f} | {rCr['L']:.3f} | {rCr['f']:.4f} |")
    sA = rA['sell']; sB = rB['sell']; sC = rC['sell']
    lines.append(f"| sell | {sA['V_sell']:.3f} | {sA['W_sell']:.3f} | {sA['L_sell']:.3f} | {sA['f_N']:.4f} | "
                 f"{sB['W_sell']:.3f} | {sB['L_sell']:.3f} | {sB['f_N']:.4f} | "
                 f"{sC['W_sell']:.3f} | {sC['L_sell']:.3f} | {sC['f_N']:.4f} |")
    lines.append("")

    # Key findings
    lines.append("### Key findings")
    lines.append("")
    lines.append(f"**Founder B (pessimist, α=0.6):** Paid {fm(tax_B_110)} in years 1–10 vs {fm(tax_A_110)} for Founder A.")
    lines.append(f"At sale, the suppressed basis produced a large positive delta ({fm(sellB['delta_sell'])}).")
    lines.append(f"Total net tax: {fm(rB['Net'])} vs {fm(rA['Net'])} for Founder A — "
                 f"{(rB['Net']-rA['Net'])/rA['Net']*100:+.1f}% more despite lower annual payments.")
    lines.append(f"Terminal wealth: {fm(rB['TW'])} vs {fm(rA['TW'])} — "
                 f"{(rB['TW']-rA['TW'])/rA['TW']*100:+.1f}%.")
    lines.append("")
    lines.append(f"**Founder C (optimist, α=1.4):** Paid {fm(tax_C_110)} in years 1–10 vs {fm(tax_A_110)} for Founder A.")
    lines.append(f"At sale, the inflated basis produced a {'positive' if sellC['delta_sell'] > 0 else 'negative'} "
                 f"delta ({fm(sellC['delta_sell'])}) → "
                 f"{'tax' if sellC['L_sell'] > 0 else 'refund'} of {fm(abs(sellC['L_sell']))}.")
    lines.append(f"Total net tax: {fm(rC['Net'])} vs {fm(rA['Net'])} for Founder A — "
                 f"{(rC['Net']-rA['Net'])/rA['Net']*100:+.1f}% relative to honest.")
    lines.append(f"Terminal wealth: {fm(rC['TW'])} vs {fm(rA['TW'])} — "
                 f"{(rC['TW']-rA['TW'])/rA['TW']*100:+.1f}%.")
    lines.append("")
    lines.append(f"**Founder A (honest, α=1.0):** No directional forecast exposure. Paid exactly")
    lines.append(f"the tax on the wealth actually accumulated — {fm(rA['Net'])} net, retaining {fm(rA['TW'])}.")
    lines.append(f"Neither Founder B nor C improves on this outcome at g=7%, N=10.")
    lines.append("")
    lines.append("*VAL.B §N.5 note on signalling: Founder C's overstatement may generate real")
    lines.append("external benefits (investor credibility, lender terms) outside this model.")
    lines.append("Those benefits are not modelled here. The WDT prices the declaration;")
    lines.append("whether the external benefit exceeds the tax cost is a question the model")
    lines.append("cannot answer — it is handled by the β parameter in VAL.A §C.3.*")
    lines.append("")
    return '\n'.join(lines)


# ─────────────────────────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────────────────────────

def main():
    base_p = load_params()
    print(f"Parameters loaded: k={base_p['k']}, $\tau_0$={base_p['tau_0']}, $\tau_m$={base_p['tau_m']}, W_min=£{base_p['W_min']}m")

    os.makedirs(OUT_DIR, exist_ok=True)
    out_path = os.path.join(OUT_DIR, "VAL_Worked_Examples_Figures.md")

    lines = []
    lines.append("# VAL.B Worked Examples — Numerical Figures")
    lines.append("")
    lines.append(f"**Generated:** {date.today().isoformat()}  ")
    lines.append(f"**Model:** Python v1.0 standalone · Route C simulation throughout  ")
    lines.append(f"**Parameters:** $\tau_0$={base_p['tau_0']*100:.0f}%, $\tau_m$={base_p['tau_m']*100:.0f}%, k={base_p['k']}, W_min=£{base_p['W_min']:.0f}m (all examples unless stated)  ")
    lines.append(f"**Option A convention:** N annual periods used as assessment windows throughout.  ")
    lines.append(f"**§K limitation:** 3 annual periods used as proxy for 3 multi-year windows —")
    lines.append(f"expected to produce variance from a window-aware model; directional claims unaffected.  ")
    lines.append(f"**§L and §M:** Bespoke closed-form arithmetic, not run_val_sim.  ")
    lines.append("")

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
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(md)
    print(f"Written: {out_path}")
    print(f"Lines: {len(md.splitlines())}")


if __name__ == '__main__':
    main()
