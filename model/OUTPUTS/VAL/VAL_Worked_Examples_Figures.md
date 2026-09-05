# VAL.B Worked Examples — Numerical Figures

**Generated:** 2026-09-05  
**Model:** Python v1.0 standalone · Route C simulation throughout. All figures use TW_settled/Net_settled (post-sale settlement correction). Presented as TW/Net in table labels to match VAL.B nomenclature.  
**Parameters:** $\tau_0$=15%, $\tau_m$=70%, $k$=0.001, $W_{min}$=£2m (all examples unless stated).  
**Option A convention:** N annual periods used as assessment windows throughout.  §K limitation: 3 annual periods used as proxy for 3 multi-year windows — expected to produce variance from a window-aware model; directional claims unaffected.  §L and §M: bespoke closed-form arithmetic, not run_val_sim.  

## J.3 Illustrative Figures

| | **Honest ($\alpha$ = 1.0)** | **Moderate under ($\alpha$ = 0.8)** | **Significant under ($\alpha$ = 0.5)** |
|:---|---:|---:|---:|
| **Entry basis $B_0$** | £20.000m | £16.000m | £10.000m |
| **True value at sale $V_5$** | £30.015m | £30.015m | £30.015m |
| **Tax paid years 1–5** | £1.077m | £0.859m | £0.534m |
| **Final delta on sale (year 6)** | £1.641m | £7.053m | £15.175m |
| **Tax on final delta** | £0.251m | £1.080m | £2.324m |
| **Total lifetime WDT (Net)** | £1.295m | £1.796m | £2.550m |
| **Terminal net worth (TW)** | £28.478m | £27.763m | £26.690m |
| **TW vs honest** | — | -2.51% | -6.28% |
| **Net tax vs honest** | — | +38.68% | +96.95% |

Table J.1: Deferred delta comparison across declaration strategies, $g$ = 7%, N = 5, $\tau$ = 15%. Python model v1.0, $k$ = 0.001.

### J.3.1 Period-by-period: Honest declarer ($\alpha$ = 1.0)

| t | True V (£m) | Declared W (£m) | Delta (£m) | $\tau$ | Tax L (£m) | f |
|:---:|---:|---:|---:|:---:|---:|:---:|
| 0 (entry) | 20.000 | 20.000 | — | 15.21% | 0.000 | 1.0000 |
| 1 | 21.400 | 21.400 | 1.400 | 15.23% | 0.213 | 0.9900 |
| 2 | 22.898 | 22.670 | 1.270 | 15.25% | 0.194 | 0.9816 |
| 3 | 24.501 | 24.050 | 1.380 | 15.26% | 0.211 | 0.9730 |
| 4 | 26.216 | 25.508 | 1.458 | 15.28% | 0.223 | 0.9645 |
| 5 | 28.051 | 27.055 | 1.547 | 15.30% | 0.237 | 0.9561 |
| 6 (sell) | 30.015 | 28.696 | 1.641 | 15.32% | 0.251 | 0.9561 |

### J.3.2 Key mechanism: basis gap recovery at sale

At the sell year, the final delta differs by declaration strategy: honest ($\alpha$ = 1.0) £1.641m → tax £0.251m; $\alpha$ = 0.8 £7.053m → tax £1.080m (larger by £5.413m due to suppressed basis); $\alpha$ = 0.5 £15.175m → tax £2.324m (larger by £13.534m due to suppressed basis).

The $\alpha$ = 0.8 understater saved £0.218m in years 1–5 but paid £0.829m more at sale — net cost of understatement: £0.501m. The $\alpha$ = 0.5 understater saved £0.543m in years 1–5 but paid £2.073m more at sale — net cost of understatement: £1.255m.

## K.3 Illustrative Figures

**Model note.** (VAL.B §K) uses three *assessment windows* of unspecified length. This model uses N = 3 *annual* periods as a proxy (Option A). A window-aware model would produce different equity accumulation figures; the directional claim (dilution is more expensive at high $g$) is unaffected. The model treats $V_0$ = £20m as the declared portfolio (representing the stake value directly, not the company valuation at £20m with a 60% stake = £12m stake value).

### K.3.1 Period-by-period accumulation

| Period | True V (£m) | Honest W (£m) | Honest f | Understater W (£m) | Understater f | State equity (honest) | State equity ($\alpha$=0.6) |
|:---:|---:|---:|:---:|---:|:---:|:---:|:---:|
| entry | 20.000 | 20.000 | 1.0000 | 12.000 | 1.0000 | 0.000% | 0.000% |
| 1 | 23.000 | 23.000 | 0.9801 | 13.800 | 0.9803 | 1.989% | 1.975% |
| 2 | 26.450 | 25.924 | 0.9632 | 15.557 | 0.9635 | 3.679% | 3.653% |
| 3 | 30.417 | 29.299 | 0.9462 | 17.584 | 0.9466 | 5.379% | 5.339% |
| sell | 34.980 | 33.099 | 0.9462 | 33.112 | 0.9466 | 5.379% | 5.339% |

### K.3.2 Summary at period N = 3

| Metric | Honest ($\alpha$ = 1.0) | Understater ($\alpha$ = 0.6) |
|:---|---:|---:|
| **Founder retained fraction** | 94.621% | 94.661% |
| **State equity stake** | 5.379% | 5.339% |
| **True value of state stake (£m)** | £1.636m | £1.624m |
| **True value of founder stake (£m)** | £28.781m | £28.793m |
| **Tax paid (Net) (£m)** | £1.928m | £2.916m |
| **Terminal net worth TW (£m)** | £32.592m | £31.043m |
| **Implicit cost of understatement vs honest (£m)** | — | £0.988m |

Table K.1: Accumulated dilution under understatement, $g$ = 15%, Route C, N = 3 annual periods as proxy for three-year window, $\tau$ = 15%. Python model v1.0, $k$ = 0.001.

### K.3.3 Key mechanism: underpriced equity transfer

The understater transfers equity at their declared value (60% of true value). The state acquires this equity at a 40% discount to reality; it then appreciates at the true rate (15% per year). After 3 periods, the state holds 5.339% vs 5.379% for the honest declarer. The understater has transferred less equity in percentage terms but at a steeper discount, so net tax cost is higher: £0.988m extra.

### L.3.1 Timeline A: Annual Cash Settlement (what Route D avoids)

| Year | True V (£m) | Annual WDT liability (£m) | Cumulative liability (£m) |
|:---:|---:|---:|---:|
| 1 | 8.400 | 0.060 | 0.060 |
| 2 | 8.820 | 0.063 | 0.124 |
| 3 | 9.261 | 0.067 | 0.190 |
| 4 | 9.724 | 0.070 | 0.260 |
| 5 | 10.210 | 0.073 | 0.333 |

### L.3.2 Timeline B: Route D (deferred to inheritance at year 15)

| Event | Value (£m) |
|:---|---:|
| Entry basis $B_0$ | £8.000m |
| True value at inheritance (year 15) | £16.631m |
| Total gain (V15 − $B_0$) | £8.631m |
| $\tau$ at V15 | 15.17% |
| WDT liability at inheritance | £1.310m |
| Annual cash demand during years 1–15 | £0.000m/year |

### L.3.3 Comparison

| Metric | Timeline A (annual) | Timeline B (Route D) |
|:---|---:|---:|
| Annual cash demand | £0.067m/yr avg | £0.000m/yr |
| Total tax collected | £0.333m (yrs 1–5 only) | £1.310m (full 15 yrs) |
| Forced realisation risk | High | None during holding |
| Tax base | Partial appreciation | Full gain $B_0$ → V15 |
| Settlement mechanism | Cash from external source | Cash from estate or auction |

Route D collects more tax (full 15-year gain vs 5-year partial) while eliminating the cash-demand problem. Annual settlement structurally undermines the tax base.

## M.5 Comparison

**Model note.** This example uses closed-form arithmetic, not run_val_sim. Liabilities calculated as $\tau$(V) × (V − prior_basis) for each settlement event. Computed true values: $V_{10}$ = £8.144m, $V_{15}$ = £10.395m ($g$ = 5% compounded from $B_0$ = £5m). Soft reset declared value: £7.688m (conservative, ~94% of true $V_{10}$), consistent with Option A setup.

| Metric | Option A: Soft reset (yr 10) | Option B: Hard reset (yr 10) | Option C: No reset (yr 15) |
|:---|---:|---:|---:|
| **Settlement value** | £7.688m (self-declared) | £8.144m (auction) | £10.395m (inheritance auction) |
| **Gain from $B_0$ = £5m** | £2.688m | £3.144m | £5.395m |
| **$\tau$ at settlement** | 15.07% | 15.07% | 15.10% |
| **WDT liability** | £0.405m | £0.474m | £0.815m |
| **Auction costs** | nil | £0.163m | nil (estate cost) |
| **New recognised basis** | £7.688m | £8.144m | £10.395m (heir's entry basis) |
| **Basis verified?** | No (self-declared) | Yes (market auction) | Yes (inheritance auction) |
| **Future refund basis** | Unverified | Market-verified | Market-verified |

Table M.1: Voluntary settlement options compared. Entry basis £5m; $g$ = 5% compounded. Python model v1.0 (closed-form arithmetic), $k$ = 0.001.

## N.3 Illustrative Figures

| Metric | Founder A ($\alpha$=1.0) | Founder B ($\alpha$=0.6) | Founder C ($\alpha$=1.4) |
|:---|---:|---:|---:|
| **Entry basis** | £8.000m | £4.800m | £11.200m |
| **True value at sale (year 11)** | £16.839m | £16.839m | £16.839m |
| **Tax paid years 1–10** | £0.988m | £0.591m | £1.388m |
| **Refunds received years 1–10** | £0.000m | £0.000m | £0.000m |
| **Post-sale delta (year 11)** | £0.883m | £6.700m | £-4.932m |
| **Tax/refund on post-sale delta** | £0.134m | £1.016m | £-0.748m |
| **Total lifetime WDT (Net)** | £1.104m | £1.473m | £0.738m |
| **Terminal net worth (TW)** | £15.304m | £14.543m | £16.065m |
| **TW vs Founder A** | — | -4.98% | +4.97% |
| **Net tax vs Founder A** | — | +33.39% | -33.13% |
| **Effective rate (Net/TW)** | 7.22% | 10.13% | 4.60% |

Table N.1: Three-founder comparison, $g$ = 7%, N = 10, Route C, $\tau$ = 15%. Python model v1.0, $k$ = 0.001.

### N.3.1 Period-by-period: All three founders

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

### N.3.2 Key findings

**Founder B (pessimist, $\alpha$=0.6):** Paid £0.591m in years 1–10 vs £0.988m for Founder A. At sale, the suppressed basis produced a large positive delta (£6.700m). Total net tax: £1.473m vs £1.104m for Founder A — +33.4% more despite lower annual payments. Terminal wealth: £14.543m vs £15.304m — -5.0%.

**Founder C (optimist, $\alpha$=1.4):** Paid £1.388m in years 1–10 vs £0.988m for Founder A. At sale, the inflated basis produced a negative delta (£-4.932m) → refund of £0.748m. Total net tax: £0.738m vs £1.104m for Founder A — -33.1% relative to honest. Terminal wealth: £16.065m vs £15.304m — +5.0%.

**Founder A (honest, $\alpha$=1.0):** No directional forecast exposure. Paid exactly the tax on the wealth actually accumulated — £1.104m net, retaining £15.304m. Neither Founder B nor C improves on this outcome at $g$=7%, N=10.
