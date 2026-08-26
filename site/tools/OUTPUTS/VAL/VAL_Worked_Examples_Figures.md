# VAL.B Worked Examples — Numerical Figures

**Generated:** 2026-08-17  
**Model:** Python v1.0 standalone · Route C simulation throughout  
**Parameters:** $	au_0$=15%, $	au_m$=70%, k=0.001, W_min=£2m (all examples unless stated)  
**Option A convention:** N annual periods used as assessment windows throughout.  
**§K limitation:** 3 annual periods used as proxy for 3 multi-year windows —
expected to produce variance from a window-aware model; directional claims unaffected.  
**§L and §M:** Bespoke closed-form arithmetic, not run_val_sim.  

## §J: The Deferred Delta

**Setup:** Route C fungible asset · $V_0$ = £20m · g = 7% · N = 5 years · τ = 20% at entry
**Claim illustrated:** VAL §1, §5.3 — understatement defers tax, does not eliminate it.
**Model note:** Annual periods used as assessment windows (Option A).

### Table J.1: Deferred Delta Comparison

| Metric | Honest (α=1.0) | Moderate under (α=0.8) | Significant under (α=0.5) |
|:---|---:|---:|---:|
| Entry basis B₀ | £20.000m | £16.000m | £10.000m |
| True value at sale V₅ | £30.015m | £30.015m | £30.015m |
| Tax paid years 1–5 | £1.077m | £0.859m | £0.534m |
| Final delta on sale (year 6) | £1.641m | £7.053m | £15.175m |
| Tax on final delta | £0.251m | £1.080m | £2.324m |
| Total lifetime WDT (Net) | £1.328m | £1.939m | £2.858m |
| Terminal net worth (TW) | £28.444m | £27.620m | £26.382m |
| TW vs honest | — | -2.90% | -7.25% |
| Net tax vs honest | — | +45.99% | +115.21% |

### Period-by-period: Honest declarer (α=1.0)

| t | True V (£m) | Declared W (£m) | Delta (£m) | τ | Tax L (£m) | f |
|:---:|---:|---:|---:|:---:|---:|:---:|
| 0 (entry) | 20.000 | 20.000 | — | 15.21% | 0.000 | 1.0000 |
| 1 | 21.400 | 21.400 | 1.400 | 15.23% | 0.213 | 0.9900 |
| 2 | 22.898 | 22.670 | 1.270 | 15.25% | 0.194 | 0.9816 |
| 3 | 24.501 | 24.050 | 1.380 | 15.26% | 0.211 | 0.9730 |
| 4 | 26.216 | 25.508 | 1.458 | 15.28% | 0.223 | 0.9645 |
| 5 | 28.051 | 27.055 | 1.547 | 15.30% | 0.237 | 0.9561 |
| 6 (sell) | 30.015 | 28.696 | 1.641 | 15.32% | 0.251 | 0.9561 |

### Key mechanism: basis gap recovery at sale

At the sell year, the final delta differs by declaration strategy:
- Honest (α=1.0): final delta = £1.641m → tax = £0.251m
- α=0.8: final delta = £7.053m → tax = £1.080m (larger by £5.413m due to suppressed basis)
- α=0.5: final delta = £15.175m → tax = £2.324m (larger by £13.534m due to suppressed basis)

The α=0.8 understater saved £0.218m in years 1–5 but paid £0.829m more at sale — net cost of understatement: £0.611m.
The α=0.5 understater saved £0.543m in years 1–5 but paid £2.073m more at sale — net cost of understatement: £1.530m.

## §K: Dilution Compounds with Growth

**Setup:** Route C, 60% founder stake · $V_0$ = £20m · g = 15% · N = 3
**Claim illustrated:** VAL §5.2 — must-transfer cost tracks the asset's trajectory.

**Model limitation (Option A).** VAL.B §K uses three *assessment windows* of
unspecified length. This model uses N=3 *annual* periods as a proxy.
A window-aware model would produce different equity accumulation figures.
The directional claim (dilution is more expensive at high g) is unaffected.

**Founder stake framing.** The model treats the full $V_0$ = £20m as the
declared portfolio. VAL.B §K describes a 60% stake in a company worth £20m
total (stake value £12m). For comparability the model runs at $V_0$=£20m
representing the stake value directly, not the company valuation.

### Table K.1: Accumulated Dilution Under Understatement

| Period | True V (£m) | Honest W (£m) | Honest f | Understater W (£m) | Understater f | State equity (honest) | State equity (α=0.6) |
|:---:|---:|---:|:---:|---:|:---:|:---:|:---:|
| entry | 20.000 | 20.000 | 1.0000 | 12.000 | 1.0000 | 0.000% | 0.000% |
| 1 | 23.000 | 23.000 | 0.9801 | 13.800 | 0.9803 | 1.989% | 1.975% |
| 2 | 26.450 | 25.924 | 0.9632 | 15.557 | 0.9635 | 3.679% | 3.653% |
| 3 | 30.417 | 29.299 | 0.9462 | 17.584 | 0.9466 | 5.379% | 5.339% |
| sell | 34.980 | 33.099 | 0.9462 | 33.112 | 0.9466 | 5.379% | 5.339% |

### Summary at period N=3

| Metric | Honest (α=1.0) | Understater (α=0.6) |
|:---|---:|---:|
| Founder retained fraction | 94.621% | 94.661% |
| State equity stake | 5.379% | 5.339% |
| True value of state stake (£m) | £1.636m | £1.624m |
| True value of founder stake (£m) | £28.781m | £28.793m |
| Tax paid (Net) (£m) | £2.006m | £3.233m |
| Terminal net worth TW (£m) | £32.515m | £30.726m |
| Implicit cost of understatement vs honest (£m) | — | £1.228m |

### Key mechanism: underpriced equity transfer

The understater transfers equity at their declared value (60% of true value).
The state acquires this equity at an underpriced rate; it then appreciates at
the true rate (15% per year). After 3 periods:
- Honest: state holds 5.379% of the asset, true value £1.636m
- Understater: state holds 5.339% of the asset, true value £1.624m

The understater's state stake is worth £1.624m vs £1.636m for the honest
declarer — the understater has transferred more economic value per unit of tax paid.
This gap is the 'implicit cost of understatement' under Route C: £1.228m extra net tax.

## §L: Why Route D Defers to Realisation

**Setup:** Sculpture collection · Entry basis B₀ = £8m · g = 5% · τ ≈ 20% at entry
**Claim illustrated:** VAL §6.1 — annual cash settlement on illiquid assets
recreates forced-realisation pressure; Route D avoids this.

**Model note.** This example uses bespoke cash-flow arithmetic, not run_val_sim.
The WDT liability is approximated as τ(V_t) × (V_t − V_{t-1}) in each year,
treating the collection as honestly self-declared at true value each period.
This understates the mechanism detail but captures the cash-demand structure.

### Timeline A: Annual Cash Settlement (what Route D avoids)

| Year | True V (£m) | Annual WDT liability (£m) | Cumulative liability (£m) |
|:---:|---:|---:|---:|
| 1 | 8.400 | 0.060 | 0.060 |
| 2 | 8.820 | 0.063 | 0.124 |
| 3 | 9.261 | 0.067 | 0.190 |
| 4 | 9.724 | 0.070 | 0.260 |
| 5 | 10.210 | 0.073 | 0.333 |

**Total annual WDT liability over 5 years: £0.333m**
This cash must be sourced from outside the illiquid collection. If funded by
distress-selling individual works, the collection's value is impaired in the
process — the tax partially destroys the value it is attempting to capture.

### Timeline B: Route D (deferred to inheritance at year 15)

| Event | Value (£m) |
|:---|---:|
| Entry basis B₀ | £8.000m |
| True value at inheritance (year 15) | £16.631m |
| Total gain (V15 − B₀) | £8.631m |
| τ at V15 | 15.17% |
| WDT liability at inheritance | £1.310m |
| No annual cash demand during years 1–15 | £0.000m/year |

**Full 15-year appreciation is taxed in one calculation at realisation.**
No forced sale occurred during the holding period. The heir pays £1.310m
from estate liquid assets and retains the collection, or allows the
inheritance auction to establish a market price and settles from proceeds.

### Comparison

| Metric | Timeline A (annual) | Timeline B (Route D) |
|:---|---:|---:|
| Annual cash demand | £0.067m/yr avg | £0.000m/yr |
| Total tax collected | £0.333m (yrs 1–5 only) | £1.310m (full 15 yrs) |
| Forced realisation risk | High | None during holding |
| Tax base | Partial appreciation | Full gain B₀ → V15 |
| Settlement mechanism | Cash from external source | Cash from estate or auction |

*Route D collects more tax (full 15-year gain vs 5-year partial) while
eliminating the cash-demand problem. Annual settlement is not just
administratively inconvenient — it structurally undermines the tax base.*

## §M: Voluntary Settlement — Certainty, Not Avoidance

**Setup:** Commercial property · B₀ = £5m · g = 5% · Approximate V₁₀ ≈ £8.15m
**Claim illustrated:** VAL §6.4 — soft and hard basis resets give certainty, not avoidance.

**Model note.** This example uses closed-form arithmetic, not run_val_sim.
Liabilities calculated as τ(V) × (V − prior_basis) for each settlement event.
VAL.B §M specifies V₁₀ ≈ £9m (true) and a soft reset declared at £8.5m.
This model uses g=5% compounded: V₁₀ = £8.144m, V₁₅ = £10.395m.

**Computed true values:** V₁₀ = £8.144m, V₁₅ = £10.395m
**Soft reset declared value (Option A):** £7.688m (conservative, ~94% of true)

### Table M.1: Voluntary Settlement Options Compared

| Metric | Option A: Soft reset (yr 10) | Option B: Hard reset (yr 10) | Option C: No reset (yr 15) |
|:---|---:|---:|---:|
| Settlement value | £7.688m (self-declared) | £8.144m (auction) | £10.395m (inheritance auction) |
| Gain from B₀ = £5m | £2.688m | £3.144m | £5.395m |
| τ at settlement | 15.07% | 15.07% | 15.10% |
| WDT liability | £0.405m | £0.474m | £0.815m |
| Auction costs | nil | £0.163m | nil (estate cost) |
| New recognised basis | £7.688m | £8.144m | £10.395m (heir's entry basis) |
| Basis verified? | No (self-declared) | Yes (market auction) | Yes (inheritance auction) |
| Future refund basis | Unverified | Market-verified | Market-verified |

*Liabilities calculated at τ(settlement value) × gain from B₀. g=5%, compounded.*

### What the example shows

None of the three options avoids the WDT. The full gain from B₀ to settlement
value is taxed in every case. Option A settles earlier at a conservative
self-declared value: lower immediate liability (£0.405m) but an unverified
basis for future calculations. Option B settles at market: higher liability
(£0.474m) plus auction costs (£0.163m) but a verified basis.
Option C defers to inheritance: largest single liability (£0.815m),
timing set by death rather than the taxpayer's choice.

Present value favours earlier settlement only if the marginal rate at year 10
(15.07%–15.07%) is materially lower than at year 15 (15.10%),
which at these wealth levels is approximately true but not decisive at the
reference k=0.0001 (the rate function is relatively flat in this range).

## §N: Forecast Exposure

**Setup:** Route C · Three founders, identical 40% stakes · $V_0$ = £8m (each) · g = 7% · N = 10
**Claim illustrated:** VAL §7.1 — honest declaration has no directional forecast exposure.
**Founders:** A (α=1.0, honest), B (α=0.6, expects underperformance), C (α=1.4, expects outperformance)

### Table N.1: Three-Founder Comparison

| Metric | Founder A (α=1.0) | Founder B (α=0.6) | Founder C (α=1.4) |
|:---|---:|---:|---:|
| Entry basis | £8.000m | £4.800m | £11.200m |
| True value at sale (year 11) | £16.839m | £16.839m | £16.839m |
| Tax paid years 1–10 | £0.988m | £0.591m | £1.388m |
| Refunds received years 1–10 | £0.000m | £0.000m | £0.000m |
| Post-sale delta (year 11) | £0.883m | £6.700m | £-4.932m |
| Tax/refund on post-sale delta | £0.134m | £1.016m | £-0.748m |
| Total lifetime WDT (Net) | £1.122m | £1.607m | £0.640m |
| Terminal net worth (TW) | £15.287m | £14.409m | £16.164m |
| TW vs Founder A | — | -5.74% | +5.74% |
| Net tax vs Founder A | — | +43.21% | -42.95% |
| Effective rate (Net/TW) | 7.34% | 11.15% | 3.96% |

### Period-by-period: All three founders

| t | V (£m) | A: W | A: L | A: f | B: W | B: L | B: f | C: W | C: L | C: f |
|:---:|---:|---:|---:|:---:|---:|---:|:---:|---:|---:|:---:|
| 0 | 8.000 | 8.000 | — | 1.0000 | 4.800 | — | 1.0000 | 11.200 | — | 1.0000 |
| 1 | 8.560 | 8.560 | 0.084 | 0.9901 | 5.136 | 0.051 | 0.9902 | 11.984 | 0.119 | 0.9901 |
| 2 | 9.159 | 9.069 | 0.077 | 0.9818 | 5.441 | 0.046 | 0.9818 | 12.696 | 0.108 | 0.9817 |
| 3 | 9.800 | 9.622 | 0.083 | 0.9732 | 5.773 | 0.050 | 0.9733 | 13.470 | 0.117 | 0.9732 |
| 4 | 10.486 | 10.206 | 0.088 | 0.9648 | 6.124 | 0.053 | 0.9649 | 14.287 | 0.124 | 0.9647 |
| 5 | 11.220 | 10.826 | 0.094 | 0.9565 | 6.496 | 0.056 | 0.9566 | 15.155 | 0.131 | 0.9564 |
| 6 | 12.006 | 11.483 | 0.099 | 0.9482 | 6.891 | 0.059 | 0.9484 | 16.075 | 0.140 | 0.9481 |
| 7 | 12.846 | 12.181 | 0.105 | 0.9400 | 7.310 | 0.063 | 0.9402 | 17.051 | 0.148 | 0.9398 |
| 8 | 13.745 | 12.921 | 0.112 | 0.9319 | 7.754 | 0.067 | 0.9321 | 18.086 | 0.157 | 0.9317 |
| 9 | 14.708 | 13.705 | 0.119 | 0.9238 | 8.225 | 0.071 | 0.9240 | 19.184 | 0.167 | 0.9236 |
| 10 | 15.737 | 14.538 | 0.126 | 0.9158 | 8.725 | 0.075 | 0.9160 | 20.348 | 0.177 | 0.9155 |
| sell | 16.839 | 15.420 | 0.134 | 0.9158 | 15.425 | 1.016 | 0.9160 | 15.416 | -0.748 | 0.9155 |

### Key findings

**Founder B (pessimist, α=0.6):** Paid £0.591m in years 1–10 vs £0.988m for Founder A.
At sale, the suppressed basis produced a large positive delta (£6.700m).
Total net tax: £1.607m vs £1.122m for Founder A — +43.2% more despite lower annual payments.
Terminal wealth: £14.409m vs £15.287m — -5.7%.

**Founder C (optimist, α=1.4):** Paid £1.388m in years 1–10 vs £0.988m for Founder A.
At sale, the inflated basis produced a negative delta (£-4.932m) → refund of £0.748m.
Total net tax: £0.640m vs £1.122m for Founder A — -43.0% relative to honest.
Terminal wealth: £16.164m vs £15.287m — +5.7%.

**Founder A (honest, α=1.0):** No directional forecast exposure. Paid exactly
the tax on the wealth actually accumulated — £1.122m net, retaining £15.287m.
Neither Founder B nor C improves on this outcome at g=7%, N=10.

*VAL.B §N.5 note on signalling: Founder C's overstatement may generate real
external benefits (investor credibility, lender terms) outside this model.
Those benefits are not modelled here. The WDT prices the declaration;
whether the external benefit exceeds the tax cost is a question the model
cannot answer — it is handled by the β parameter in VAL.A §C.3.*
