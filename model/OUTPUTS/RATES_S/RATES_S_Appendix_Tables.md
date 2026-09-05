# B. WDT Rate Parameter Sensitivity Sweep

**Run date:** 2026-09-05  
**Model version:** v8 (rates_model.py / wdt_core.py)  
**Headline coverage window:** 10 years (SSMcov10/TCMcov10 columns; change HEADLINE_WINDOW in wdt_analytics.py)  
**Parameters file:** `WDT_Params.toml`  

## B.1. Purpose

This document sweeps each of the four WDT rate-function parameters independently, holding the other three at Balanced baseline values, and reports how key transition metrics vary across the full 73-year historical start-year sweep (1947–2019 UK equity return series). It is intended as orientation material for future Governing Council calibration work, not as a scenario recommendation. Parameter interactions are not modelled here; joint sweeps are a natural second-order extension.

### B.1.1 The Rate Function

The WDT logistic marginal rate function is:

$$\tau(W) = \frac{\tau_m}{1 + \left(\frac{\tau_m - \tau_0}{\tau_0}\right)e^{-k(W - W_{\min})}}, \quad \tau(W) = 0 \text{ if } W < W_{\min}$$

Note: the docstring in `rates_model.py` contains a typographical error writing $(1-\tau_0)/\tau_0$ as the denominator coefficient. The implementation in `wdt_core.tau()` correctly uses $(\tau_m - \tau_0)/\tau_0$. All results here use the correct formula.

### B.1.2 Balanced Baseline Parameters

| Parameter | Baseline value | Role |
|---|---|---|
| $\tau_0$ (floor rate) | 15% | Marginal rate at W = W_min; determines tax on the smallest deltas |
| $\tau_m$ (ceiling rate) | 70% | Asymptotic ceiling; determines the maximum rate as W → ∞ |
| k (steepness, per £m) | 0.001 | Controls how rapidly the rate climbs through the wealth distribution |
| W_min (£m) | £2.0m | Entry point; below this the rate is zero regardless of δ |

**SWF sizing parameters (Balanced baseline; swept in §§5–6):**

| Parameter | Baseline value | Role |
|---|---|---|
| SRR capitalisation ratio | 3.0× | SRR target = ratio × (cumulative net income / N); sets how long before the refund guarantee is credible |
| LRR floor | 3.0 years of expenditure | LRR target = lrr_years × prevailing government expenditure; sets the Phase Two viability threshold |

**Non-SWF parameters (held constant throughout all sweeps):**

| Parameter | Value |
|---|---|
| Budget base (£b) | £1,157.4b |
| Budget growth (p.a.) | 4.51% |
| Historical mean return | 10.45% |
| Wealth brackets | 10 |
| Growth tiers | 4 |

### B.1.3 Metrics

**Success (v8):** LRR fills within the 71-year modelling window AND the LRR buffer never hits zero (lrr_failure_year is None). At Balanced parameters, success rate is 100% across all 73 start years.

**SSMcov10 / TCMcov10 (headline window):** Average Step-5 coverage fraction (labour-tax-relief surplus / annual expenditure) over the first 10 post-fill years. SSM applies uniform historical returns (correlated-shock, worst-case floor); TCM applies heterogeneous tier differentials (persistent-heterogeneity ceiling). Zero in any year where the LRR or SRR balance hits zero drags the average down. The headline window is 10 years; change HEADLINE_WINDOW in wdt_analytics.py to switch all tables and charts simultaneously.

**SSMcov50:** Same metric averaged over 50 post-fill years. Shows long-run trajectory: rising values indicate WDT revenue compounds faster than expenditure; falling values indicate the coverage promise weakens with time.

**LRR fail n:** Count of the 73 historical start years where the LRR balance reaches zero within the 71-year modelling window (lrr_failure_year is not None). At Balanced parameters this is 0. Non-zero values under stressed parameters indicate the post-fill buffer is insufficient for some historical return sequences.

**LRR failure year:** First year the LRR balance hits zero post-fill. The LRR failing means the political buffer is exhausted; any further SRR deficit has no backstop. The SRR failure year (when the refund guarantee itself breaks) follows later.

**LRR fill year:** First year the LRR balance reaches the floor target. The primary transition-speed metric; gates full Phase Two fiscal replacement.

**SRR fill year:** First year the SRR reaches its capitalisation target. Should be invariant at ~3 across most calibrations.

**LRR surplus at fill:** LRR balance minus LRR target at the fill year, in £b. Safety margin above the floor at the breakeven point.

*All distributions are across the 73 historical start years 1947–2019. The 2006 start year is extracted separately as the worst-case historical scenario (longest LRR fill time at Balanced parameters).*

## B.2. Floor Rate (τ_0)

τ_0 sets the marginal rate at W = W_min. A higher floor raises effective rates across the entire taxable population (since every taxpayer above W_min pays at least τ_0 on their first pound of delta); a lower floor concentrates the rate gradient in the upper distribution.

### τ_0 sweep

Other parameters held at Balanced baseline: τ_m = 70%,  k = 0.001,  W_min = £2.0m.

**Sweep summary — distributions across 73 historical start years**

| Value | Success% | SSMcov10 (min/med/mean/max) | TCMcov10 (min/med/mean/max) | SSMcov50 (min/med) | LRR fail n | LRR fill yr (min/med/mean/max) | SRR fill yr (med) | LRR surplus £b (min/med) |
|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| 5% | 100% | 1.4% / 111.0% / 97.1% / 160.8% | 9.5% / 122.2% / 110.2% / 198.1% | 0.8% / 4.1% | 0 | 10 / 22 / 24 / 42 | 3 | 10 / 911 |
| 10% | 100% | 9.1% / 105.1% / 115.2% / 261.5% | 15.1% / 121.7% / 120.7% / 291.9% | 0.9% / 4.2% | 0 | 8 / 16 / 18 / 34 | 3 | 27 / 886 |
| 15% ◄ | 100% | 6.4% / 122.1% / 126.0% / 287.9% | 14.6% / 125.5% / 138.8% / 321.4% | 1.0% / 4.4% | 0 | 7 / 13 / 15 / 29 | 3 | 6 / 919 |
| 20% | 100% | 13.1% / 130.4% / 136.9% / 302.3% | 19.6% / 140.1% / 151.8% / 335.6% | 1.0% / 4.4% | 0 | 6 / 12 / 14 / 27 | 3 | 13 / 908 |
| 25% | 100% | 11.0% / 138.5% / 146.8% / 348.3% | 24.6% / 121.6% / 161.8% / 375.9% | 1.2% / 4.6% | 0 | 6 / 11 / 13 / 26 | 3 | 77 / 692 |
| 30% | 100% | 20.8% / 116.9% / 155.5% / 386.4% | 21.6% / 137.6% / 173.9% / 417.3% | 1.1% / 4.4% | 0 | 5 / 10 / 12 / 25 | 3 | 4 / 822 |
| 35% | 100% | 12.5% / 130.2% / 169.5% / 382.6% | 28.2% / 146.9% / 188.4% / 450.3% | 1.2% / 4.2% | 0 | 5 / 10 / 11 / 24 | 3 | 37 / 1095 |
| 40% | 100% | 17.9% / 132.6% / 177.4% / 408.4% | 34.2% / 146.8% / 195.1% / 476.0% | 1.2% / 4.0% | 0 | 5 / 10 / 11 / 24 | 3 | 30 / 1124 |
| 45% | 100% | 15.6% / 139.8% / 184.0% / 431.7% | 28.8% / 158.4% / 201.7% / 497.2% | 1.3% / 3.9% | 0 | 5 / 9 / 10 / 21 | 3 | 8 / 849 |
| 50% | 100% | 20.6% / 135.9% / 187.0% / 451.5% | 33.9% / 167.0% / 208.6% / 474.6% | 1.3% / 3.8% | 0 | 5 / 9 / 10 / 20 | 3 | 24 / 688 |

*◄ = Balanced baseline value. SSMcov10/TCMcov10: Step-5 coverage fraction averaged over 10 post-fill years (headline window; set HEADLINE_WINDOW in wdt_analytics.py to change). SSMcov50: 50yr window showing long-run trajectory. LRR fail n: start years where LRR buffer hits zero within 71-year window. Distributions across all 73 historical start years 1947–2019.*

**2006 start year (worst-case historical scenario)**

| Value | SSMcov10 | TCMcov10 | LRR fill yr | LRR surplus £b | LRR failure yr |
|:---:|:---:|:---:|:---:|:---:|:---:|
| 5% | 109.1% | 104.6% | 39 | 1595 | — (no failure) |
| 10% | 94.7% | 65.2% | 34 | 1229 | — (no failure) |
| 15% ◄ | 58.0% | 54.7% | 29 | 523 | — (no failure) |
| 20% | 42.8% | 75.0% | 26 | 1999 | — (no failure) |
| 25% | 58.0% | 46.1% | 25 | 973 | — (no failure) |
| 30% | 70.6% | 56.0% | 25 | 2606 | — (no failure) |
| 35% | 41.9% | 66.2% | 21 | 411 | — (no failure) |
| 40% | 49.4% | 74.5% | 21 | 1277 | — (no failure) |
| 45% | 56.4% | 81.6% | 21 | 2075 | — (no failure) |
| 50% | 64.5% | 59.8% | 20 | 434 | — (no failure) |

## B.3. Ceiling Rate (τ_m)

τ_m is the asymptotic ceiling the marginal rate approaches but never reaches. Its primary effect is on the top brackets where W >> W_min; the logistic function brings effective rates close to τ_m only at very high declared wealth levels. Raising τ_m increases revenue from the highest-wealth, highest-growth cells disproportionately, since those cells also generate the largest absolute deltas.

### τ_m sweep

Other parameters held at Balanced baseline: τ_0 = 15%,  k = 0.001,  W_min = £2.0m.

**Sweep summary — distributions across 73 historical start years**

| Value | Success% | SSMcov10 (min/med/mean/max) | TCMcov10 (min/med/mean/max) | SSMcov50 (min/med) | LRR fail n | LRR fill yr (min/med/mean/max) | SRR fill yr (med) | LRR surplus £b (min/med) |
|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| 50% | 100% | 6.3% / 121.8% / 125.8% / 287.3% | 14.6% / 125.1% / 138.5% / 320.5% | 0.9% / 4.3% | 0 | 7 / 13 / 15 / 29 | 3 | 3 / 911 |
| 55% | 100% | 6.4% / 121.9% / 125.8% / 287.5% | 14.6% / 125.2% / 138.6% / 320.8% | 1.0% / 4.4% | 0 | 7 / 13 / 15 / 29 | 3 | 4 / 914 |
| 60% | 100% | 6.4% / 122.0% / 125.9% / 287.7% | 14.6% / 125.3% / 138.7% / 321.0% | 1.0% / 4.4% | 0 | 7 / 13 / 15 / 29 | 3 | 4 / 916 |
| 65% | 100% | 6.4% / 122.1% / 126.0% / 287.8% | 14.6% / 125.4% / 138.8% / 321.2% | 1.0% / 4.4% | 0 | 7 / 13 / 15 / 29 | 3 | 5 / 918 |
| 70% ◄ | 100% | 6.4% / 122.1% / 126.0% / 287.9% | 14.6% / 125.5% / 138.8% / 321.4% | 1.0% / 4.4% | 0 | 7 / 13 / 15 / 29 | 3 | 6 / 919 |
| 75% | 100% | 6.4% / 122.2% / 126.1% / 288.0% | 14.7% / 125.6% / 138.9% / 321.5% | 1.0% / 4.4% | 0 | 7 / 13 / 15 / 29 | 3 | 6 / 920 |
| 80% | 100% | 6.4% / 122.2% / 126.1% / 288.1% | 14.7% / 125.6% / 138.9% / 321.7% | 1.0% / 4.4% | 0 | 7 / 13 / 15 / 29 | 3 | 7 / 921 |
| 85% | 100% | 6.4% / 122.3% / 126.1% / 288.2% | 14.7% / 125.7% / 139.0% / 321.8% | 1.0% / 4.4% | 0 | 7 / 13 / 15 / 29 | 3 | 7 / 922 |
| 90% | 100% | 6.4% / 122.3% / 126.2% / 288.3% | 14.7% / 125.7% / 139.0% / 321.9% | 1.0% / 4.4% | 0 | 7 / 13 / 15 / 29 | 3 | 7 / 923 |
| 95% | 100% | 6.4% / 122.3% / 126.2% / 288.4% | 14.7% / 125.7% / 139.1% / 322.0% | 1.0% / 4.4% | 0 | 7 / 13 / 15 / 29 | 3 | 8 / 924 |
| 100% | 100% | 6.4% / 122.4% / 126.2% / 288.4% | 14.7% / 125.8% / 139.1% / 322.0% | 1.0% / 4.4% | 0 | 7 / 13 / 15 / 29 | 3 | 8 / 925 |

*◄ = Balanced baseline value. SSMcov10/TCMcov10: Step-5 coverage fraction averaged over 10 post-fill years (headline window; set HEADLINE_WINDOW in wdt_analytics.py to change). SSMcov50: 50yr window showing long-run trajectory. LRR fail n: start years where LRR buffer hits zero within 71-year window. Distributions across all 73 historical start years 1947–2019.*

**2006 start year (worst-case historical scenario)**

| Value | SSMcov10 | TCMcov10 | LRR fill yr | LRR surplus £b | LRR failure yr |
|:---:|:---:|:---:|:---:|:---:|:---:|
| 50% | 57.8% | 54.5% | 29 | 514 | — (no failure) |
| 55% | 57.9% | 54.6% | 29 | 517 | — (no failure) |
| 60% | 57.9% | 54.6% | 29 | 519 | — (no failure) |
| 65% | 57.9% | 54.7% | 29 | 521 | — (no failure) |
| 70% ◄ | 58.0% | 54.7% | 29 | 523 | — (no failure) |
| 75% | 58.0% | 54.7% | 29 | 524 | — (no failure) |
| 80% | 58.0% | 54.7% | 29 | 525 | — (no failure) |
| 85% | 58.0% | 54.8% | 29 | 526 | — (no failure) |
| 90% | 58.0% | 54.8% | 29 | 527 | — (no failure) |
| 95% | 58.0% | 54.8% | 29 | 528 | — (no failure) |
| 100% | 58.1% | 54.8% | 29 | 529 | — (no failure) |

## B.4. Steepness (k)

k (per £m) controls how rapidly the marginal rate climbs from τ_0 toward τ_m through the wealth distribution. Low k produces a shallow gradient — most taxpayers face rates close to τ_0 even at high wealth levels, with τ_m approached only at very large holdings. High k produces a steep step — the rate reaches τ_m quickly above W_min, compressing the gradient into a narrow wealth band.

*Sweep is log-spaced: 0.0001, 0.0002, 0.0005, 0.0010, 0.0020, 0.0050, 0.0100, 0.0500, 0.1000*

### k sweep (log-spaced)

Other parameters held at Balanced baseline: τ_0 = 15%,  τ_m = 70%,  W_min = £2.0m.

**Sweep summary — distributions across 73 historical start years**

| Value | Success% | SSMcov10 (min/med/mean/max) | TCMcov10 (min/med/mean/max) | SSMcov50 (min/med) | LRR fail n | LRR fill yr (min/med/mean/max) | SRR fill yr (med) | LRR surplus £b (min/med) |
|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| 0.0001 | 100% | 6.2% / 119.9% / 124.1% / 283.1% | 16.6% / 122.8% / 136.8% / 315.3% | 0.9% / 3.7% | 0 | 7 / 13 / 15 / 29 | 3 | 14 / 859 |
| 0.0002 | 100% | 6.2% / 120.2% / 124.3% / 283.7% | 16.6% / 123.1% / 137.1% / 316.0% | 0.9% / 3.8% | 0 | 7 / 13 / 15 / 29 | 3 | 17 / 866 |
| 0.0005 | 100% | 6.3% / 120.9% / 125.0% / 285.3% | 14.4% / 124.0% / 137.5% / 318.1% | 0.9% / 4.1% | 0 | 7 / 13 / 15 / 29 | 3 | 29 / 886 |
| 0.0010 ◄ | 100% | 6.4% / 122.1% / 126.0% / 287.9% | 14.6% / 125.5% / 138.8% / 321.4% | 1.0% / 4.4% | 0 | 7 / 13 / 15 / 29 | 3 | 6 / 919 |
| 0.0020 | 100% | 6.6% / 124.5% / 127.9% / 292.9% | 15.1% / 127.9% / 139.9% / 322.7% | 1.0% / 4.8% | 0 | 7 / 13 / 15 / 29 | 3 | 0 / 939 |
| 0.0050 | 100% | 7.3% / 129.9% / 131.3% / 306.1% | 16.2% / 130.9% / 143.8% / 338.9% | 1.1% / 5.6% | 0 | 6 / 13 / 15 / 29 | 3 | 22 / 727 |
| 0.0100 | 100% | 8.4% / 131.1% / 135.7% / 324.9% | 17.9% / 139.9% / 151.6% / 361.6% | 1.2% / 6.2% | 0 | 6 / 13 / 15 / 29 | 3 | 4 / 718 |
| 0.0500 | 100% | 11.2% / 152.4% / 155.9% / 342.1% | 24.7% / 155.5% / 179.1% / 468.9% | 1.7% / 6.6% | 0 | 6 / 12 / 14 / 27 | 3 | 3 / 845 |
| 0.1000 | 100% | 13.8% / 170.8% / 174.9% / 396.1% | 21.9% / 164.9% / 196.9% / 446.6% | 1.7% / 6.1% | 0 | 6 / 12 / 14 / 27 | 3 | 70 / 1067 |

*◄ = Balanced baseline value. SSMcov10/TCMcov10: Step-5 coverage fraction averaged over 10 post-fill years (headline window; set HEADLINE_WINDOW in wdt_analytics.py to change). SSMcov50: 50yr window showing long-run trajectory. LRR fail n: start years where LRR buffer hits zero within 71-year window. Distributions across all 73 historical start years 1947–2019.*

**2006 start year (worst-case historical scenario)**

| Value | SSMcov10 | TCMcov10 | LRR fill yr | LRR surplus £b | LRR failure yr |
|:---:|:---:|:---:|:---:|:---:|:---:|
| 0.0001 | 56.9% | 52.4% | 29 | 457 | — (no failure) |
| 0.0002 | 57.0% | 52.5% | 29 | 464 | — (no failure) |
| 0.0005 | 57.4% | 54.0% | 29 | 486 | — (no failure) |
| 0.0010 ◄ | 58.0% | 54.7% | 29 | 523 | — (no failure) |
| 0.0020 | 59.1% | 56.0% | 29 | 596 | — (no failure) |
| 0.0050 | 62.2% | 59.4% | 29 | 809 | — (no failure) |
| 0.0100 | 66.7% | 64.2% | 29 | 1136 | — (no failure) |
| 0.0500 | 44.4% | 88.4% | 26 | 1442 | — (no failure) |
| 0.1000 | 55.2% | 105.0% | 26 | 2820 | — (no failure) |

## B.5. Entry Point (W_min)

W_min (£m) is the wealth level below which the rate function produces zero liability. It is a rate design parameter, not a population boundary — all UK adults are within the taxable population regardless of W_min. Lower W_min pulls more of the 50th–80th percentile brackets into material liability; higher W_min concentrates the tax on the top percentiles. W_min also affects refund exposure in loss years, since a taxpayer below W_min receives no refund even if their delta is negative.

### W_min sweep

Other parameters held at Balanced baseline: τ_0 = 15%,  τ_m = 70%,  k = 0.001.

**Sweep summary — distributions across 73 historical start years**

| Value | Success% | SSMcov10 (min/med/mean/max) | TCMcov10 (min/med/mean/max) | SSMcov50 (min/med) | LRR fail n | LRR fill yr (min/med/mean/max) | SRR fill yr (med) | LRR surplus £b (min/med) |
|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| £0.1m | 100% | 8.4% / 85.0% / 96.7% / 242.4% | 13.5% / 81.0% / 112.6% / 263.9% | 0.7% / 3.6% | 0 | 6 / 10 / 12 / 26 | 3 | 1 / 557 |
| £0.25m | 100% | 8.4% / 85.0% / 96.7% / 242.3% | 13.5% / 81.0% / 112.6% / 263.9% | 0.7% / 3.6% | 0 | 6 / 10 / 12 / 26 | 3 | 1 / 557 |
| £0.5m | 100% | 6.7% / 86.6% / 97.7% / 242.4% | 13.6% / 81.0% / 113.1% / 264.2% | 0.7% / 3.6% | 0 | 6 / 11 / 12 / 26 | 3 | 49 / 545 |
| £1.0m | 100% | 10.0% / 95.1% / 104.8% / 247.5% | 12.0% / 106.0% / 119.8% / 267.3% | 0.8% / 3.9% | 0 | 6 / 11 / 13 / 27 | 3 | 2 / 895 |
| £2.0m ◄ | 100% | 6.4% / 122.1% / 126.0% / 287.9% | 14.6% / 125.5% / 138.8% / 321.4% | 1.0% / 4.4% | 0 | 7 / 13 / 15 / 29 | 3 | 6 / 919 |
| £3.0m | 100% | 10.9% / 133.4% / 142.8% / 290.2% | 15.5% / 148.5% / 152.0% / 318.3% | 1.1% / 4.8% | 0 | 8 / 15 / 17 / 33 | 3 | 52 / 976 |
| £5.0m | 100% | 11.7% / 157.2% / 173.0% / 348.2% | 23.7% / 176.4% / 188.4% / 395.6% | 1.3% / 5.2% | 0 | 9 / 18 / 20 / 35 | 3 | 72 / 1210 |
| £7.5m | 100% | 11.7% / 225.9% / 194.9% / 392.8% | 24.8% / 206.3% / 210.5% / 453.0% | 1.5% / 5.7% | 0 | 10 / 21 / 22 / 37 | 3 | 12 / 1001 |
| £10.0m | 100% | 11.1% / 249.0% / 217.6% / 431.2% | 25.4% / 229.1% / 231.1% / 506.6% | 1.9% / 6.4% | 0 | 11 / 22 / 24 / 39 | 3 | 79 / 1250 |

*◄ = Balanced baseline value. SSMcov10/TCMcov10: Step-5 coverage fraction averaged over 10 post-fill years (headline window; set HEADLINE_WINDOW in wdt_analytics.py to change). SSMcov50: 50yr window showing long-run trajectory. LRR fail n: start years where LRR buffer hits zero within 71-year window. Distributions across all 73 historical start years 1947–2019.*

**2006 start year (worst-case historical scenario)**

| Value | SSMcov10 | TCMcov10 | LRR fill yr | LRR surplus £b | LRR failure yr |
|:---:|:---:|:---:|:---:|:---:|:---:|
| £0.1m | 34.1% | 58.6% | 25 | 267 | — (no failure) |
| £0.25m | 34.1% | 58.5% | 25 | 266 | — (no failure) |
| £0.5m | 34.0% | 58.6% | 25 | 207 | — (no failure) |
| £1.0m | 32.2% | 58.1% | 26 | 1779 | — (no failure) |
| £2.0m ◄ | 58.0% | 54.7% | 29 | 523 | — (no failure) |
| £3.0m | 103.0% | 49.1% | 32 | 961 | — (no failure) |
| £5.0m | 149.4% | 90.1% | 35 | 4518 | — (no failure) |
| £7.5m | 142.3% | 166.1% | 35 | 115 | — (no failure) |
| £10.0m | 241.3% | 228.4% | 38 | 2710 | — (no failure) |

## B.6. SRR Capitalisation Ratio (srr_ratio)

srr_ratio sets the SRR capitalisation target as a multiple of average annual net WDT income. A higher ratio means the SRR must accumulate more before it is considered fully capitalised, which delays SRR fill and thereby reduces the flow into the LRR during the early accumulation period. A lower ratio allows faster SRR fill and faster LRR accumulation, but at the cost of a thinner refund buffer. The Governing Council recommended floor is 3×; the working SSM-derived value is 3×.

*Note: srr_ratio does not affect the rate function or individual taxpayer burden — it affects only the milestone timing (SRR fill year and LRR fill year). The burden distribution panel in the chart companion is flat across this sweep.*

### srr_ratio sweep

Other parameters held at Balanced baseline: τ_0 = 15%,  τ_m = 70%,  k = 0.001,  W_min = £2.0m,  lrr_years = 3.0.

**Sweep summary — distributions across 73 historical start years**

| Value | Success% | SSMcov10 (min/med/mean/max) | TCMcov10 (min/med/mean/max) | SSMcov50 (min/med) | LRR fail n | LRR fill yr (min/med/mean/max) | SRR fill yr (med) | LRR surplus £b (min/med) |
|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| 1.0× | 100% | 7.5% / 124.4% / 120.2% / 279.2% | 18.3% / 125.5% / 132.5% / 307.1% | 0.9% / 4.3% | 0 | 5 / 12 / 14 / 28 | 1 | 10 / 641 |
| 1.5× | 100% | 6.9% / 121.8% / 120.0% / 269.4% | 16.8% / 124.1% / 134.6% / 299.6% | 0.9% / 4.2% | 0 | 6 / 12 / 14 / 28 | 2 | 0 / 580 |
| 2.0× | 100% | 9.6% / 119.2% / 121.6% / 263.1% | 16.2% / 126.6% / 134.8% / 289.6% | 1.0% / 4.4% | 0 | 6 / 13 / 15 / 29 | 2 | 17 / 654 |
| 2.5× | 100% | 7.2% / 116.6% / 122.1% / 261.5% | 16.0% / 126.8% / 138.6% / 329.0% | 1.0% / 4.5% | 0 | 6 / 13 / 15 / 29 | 3 | 17 / 657 |
| 3.0× ◄ | 100% | 6.4% / 122.1% / 126.0% / 287.9% | 14.6% / 125.5% / 138.8% / 321.4% | 1.0% / 4.4% | 0 | 7 / 13 / 15 / 29 | 3 | 6 / 919 |
| 4.0× | 100% | 6.8% / 125.2% / 125.4% / 270.5% | 15.3% / 130.8% / 140.2% / 368.7% | 1.1% / 4.4% | 0 | 8 / 14 / 16 / 29 | 4 | 28 / 956 |
| 5.0× | 100% | 9.0% / 119.8% / 125.4% / 311.8% | 16.1% / 141.4% / 142.5% / 352.2% | 1.1% / 4.4% | 0 | 8 / 15 / 17 / 30 | 5 | 2 / 831 |
| 6.0× | 100% | 12.6% / 114.4% / 126.2% / 293.3% | 17.9% / 139.5% / 143.1% / 324.1% | 1.1% / 4.4% | 0 | 9 / 16 / 18 / 31 | 6 | 31 / 840 |
| 8.0× | 100% | 15.1% / 119.1% / 134.8% / 297.6% | 21.7% / 139.7% / 151.4% / 382.6% | 1.3% / 4.3% | 0 | 11 / 17 / 19 / 33 | 8 | 4 / 1026 |
| 10.0× | 100% | 16.7% / 125.2% / 135.0% / 297.0% | 24.1% / 143.5% / 158.1% / 370.4% | 1.4% / 4.3% | 0 | 13 / 19 / 21 / 34 | 10 | 2 / 1073 |

*◄ = Balanced baseline value. SSMcov10/TCMcov10: Step-5 coverage fraction averaged over 10 post-fill years (headline window; set HEADLINE_WINDOW in wdt_analytics.py to change). SSMcov50: 50yr window showing long-run trajectory. LRR fail n: start years where LRR buffer hits zero within 71-year window. Distributions across all 73 historical start years 1947–2019.*

**2006 start year (worst-case historical scenario)**

| Value | SSMcov10 | TCMcov10 | LRR fill yr | LRR surplus £b | LRR failure yr |
|:---:|:---:|:---:|:---:|:---:|:---:|
| 1.0× | 31.3% | 61.1% | 26 | 282 | — (no failure) |
| 1.5× | 30.2% | 59.5% | 26 | 67 | — (no failure) |
| 2.0× | 60.7% | 57.9% | 29 | 1002 | — (no failure) |
| 2.5× | 59.3% | 56.3% | 29 | 762 | — (no failure) |
| 3.0× ◄ | 58.0% | 54.7% | 29 | 523 | — (no failure) |
| 4.0× | 55.1% | 50.7% | 29 | 43 | — (no failure) |
| 5.0× | 62.5% | 47.8% | 30 | 1146 | — (no failure) |
| 6.0× | 59.5% | 44.8% | 30 | 601 | — (no failure) |
| 8.0× | 86.8% | 62.6% | 32 | 768 | — (no failure) |
| 10.0× | 108.9% | 71.6% | 34 | 2489 | — (no failure) |

## B.7. LRR Floor (lrr_years)

lrr_years sets the LRR floor as a multiple of prevailing government expenditure. The LRR target therefore grows over time as nominal expenditure grows at 4.51% p.a. A higher floor requires the LRR to accumulate more before Phase Two becomes viable, directly extending the LRR fill year. A lower floor brings LRR fill earlier but with a thinner buffer against sustained drawdown post-fill. The recommended minimum is 3 years.

*Note: lrr_years does not affect the rate function or individual taxpayer burden — it affects only the LRR milestone timing and the safety margin above the floor. The burden distribution panel in the chart companion is flat across this sweep.*

### lrr_years sweep

Other parameters held at Balanced baseline: τ_0 = 15%,  τ_m = 70%,  k = 0.001,  W_min = £2.0m,  srr_ratio = 3.0×.

**Sweep summary — distributions across 73 historical start years**

| Value | Success% | SSMcov10 (min/med/mean/max) | TCMcov10 (min/med/mean/max) | SSMcov50 (min/med) | LRR fail n | LRR fill yr (min/med/mean/max) | SRR fill yr (med) | LRR surplus £b (min/med) |
|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| 0.5 yrs | 100% | 7.5% / 48.9% / 70.3% / 196.6% | 12.5% / 63.8% / 83.7% / 250.1% | 0.7% / 2.4% | 0 | 4 / 6 / 7 / 12 | 3 | 3 / 192 |
| 1.0 yrs | 100% | 7.2% / 55.4% / 79.7% / 232.6% | 11.8% / 64.8% / 94.8% / 251.4% | 0.7% / 3.2% | 0 | 5 / 8 / 9 / 19 | 3 | 4 / 311 |
| 1.5 yrs | 100% | 7.2% / 72.5% / 95.9% / 228.6% | 15.9% / 80.0% / 107.2% / 276.4% | 0.8% / 3.8% | 0 | 5 / 10 / 11 / 24 | 3 | 6 / 582 |
| 2.0 yrs | 100% | 7.7% / 94.4% / 102.7% / 250.9% | 16.6% / 85.4% / 115.6% / 276.0% | 0.9% / 3.8% | 0 | 6 / 11 / 13 / 26 | 3 | 16 / 421 |
| 2.5 yrs | 100% | 8.9% / 115.7% / 113.8% / 248.7% | 15.9% / 117.2% / 126.6% / 321.9% | 1.0% / 4.1% | 0 | 6 / 12 / 14 / 27 | 3 | 4 / 685 |
| 3.0 yrs ◄ | 100% | 6.4% / 122.1% / 126.0% / 287.9% | 14.6% / 125.5% / 138.8% / 321.4% | 1.0% / 4.4% | 0 | 7 / 13 / 15 / 29 | 3 | 6 / 919 |
| 4.0 yrs | 100% | 8.9% / 133.1% / 144.6% / 280.8% | 15.1% / 157.8% / 157.1% / 387.3% | 1.0% / 4.6% | 0 | 8 / 15 / 18 / 34 | 3 | 6 / 895 |
| 5.0 yrs | 100% | 12.2% / 141.4% / 159.1% / 341.5% | 19.6% / 180.7% / 190.1% / 385.5% | 1.1% / 4.8% | 0 | 8 / 17 / 20 / 36 | 3 | 39 / 1220 |
| 6.0 yrs | 100% | 8.0% / 207.1% / 179.9% / 329.5% | 19.6% / 203.4% / 201.4% / 373.3% | 1.2% / 4.9% | 0 | 9 / 20 / 22 / 39 | 3 | 62 / 1383 |
| 8.0 yrs | 100% | 4.2% / 234.8% / 216.4% / 407.0% | 13.4% / 292.6% / 244.0% / 476.8% | 1.3% / 5.3% | 0 | 10 / 24 / 25 / 42 | 3 | 20 / 2037 |

*◄ = Balanced baseline value. SSMcov10/TCMcov10: Step-5 coverage fraction averaged over 10 post-fill years (headline window; set HEADLINE_WINDOW in wdt_analytics.py to change). SSMcov50: 50yr window showing long-run trajectory. LRR fail n: start years where LRR buffer hits zero within 71-year window. Distributions across all 73 historical start years 1947–2019.*

**2006 start year (worst-case historical scenario)**

| Value | SSMcov10 | TCMcov10 | LRR fill yr | LRR surplus £b | LRR failure yr |
|:---:|:---:|:---:|:---:|:---:|:---:|
| 0.5 yrs | 7.5% | 14.4% | 9 | 13 | — (no failure) |
| 1.0 yrs | 7.2% | 14.0% | 13 | 108 | — (no failure) |
| 1.5 yrs | 23.2% | 40.2% | 21 | 309 | — (no failure) |
| 2.0 yrs | 40.7% | 34.1% | 25 | 583 | — (no failure) |
| 2.5 yrs | 33.5% | 61.3% | 26 | 1166 | — (no failure) |
| 3.0 yrs ◄ | 58.0% | 54.7% | 29 | 523 | — (no failure) |
| 4.0 yrs | 126.8% | 86.9% | 34 | 2595 | — (no failure) |
| 5.0 yrs | 126.9% | 148.6% | 35 | 2708 | — (no failure) |
| 6.0 yrs | 202.0% | 193.2% | 38 | 5138 | — (no failure) |
| 8.0 yrs | 210.7% | 349.1% | 39 | 150 | — (no failure) |

# C. Reading Notes

**Coverage window direction.** SSMcov and TCMcov move together when a parameter raises or lowers revenue across the distribution. The SSM–TCM gap measures sensitivity to persistent growth heterogeneity; a wide gap means higher-tier taxpayers contribute disproportionately more than the correlated-shock assumption. The 50yr window is larger than the headline window because WDT revenue compounds on a growing wealth base; falling 50yr values relative to the headline signal that the coverage promise weakens in the long run for that calibration.

**LRR failure vs. non-fill.** Two distinct failure modes: (1) LRR never fills (success_rate < 100%) — the mechanism does not reach Phase Two at all for some start years; (2) LRR fails post-fill (LRR fail n > 0) — Phase Two begins but the post-fill buffer is later exhausted. Both are solvency constraints, but at Balanced parameters only stressed SWF sizing parameters (high srr_ratio or lrr_years) or very low rate parameters produce non-zero LRR fail n.

**Success rate at 100%.** The Balanced baseline achieves 100% success across all 73 start years. Parameters that reduce revenue significantly may bring the success rate below 100%, meaning the LRR fails to fill within the 71-year window for some historical starting conditions. This is the primary solvency constraint.

**SRR fill year.** Should remain ~3 across most calibrations. If it rises significantly, the refund guarantee becomes credible only after more than one political cycle, which is a materially different political position.

**LRR surplus.** A near-zero surplus at fill (see e.g. the 1953 start year at Balanced parameters, £28b surplus) indicates the mechanism passed its solvency test narrowly. A calibration that systematically reduces surplus increases the risk that a slightly worse return sequence would cause LRR non-fill.

**Pre-behavioural baseline.** All figures are pre-behavioural. Behavioural responses — migration, restructuring, avoidance — are not modelled and will reduce actual revenue by an unknown amount. See RATES §9.1 and BEHAV.

**Joint calibration.** These sweeps vary one parameter at a time. In practice, τ_0 and τ_m jointly determine both the level and shape of revenue; W_min and k jointly determine where in the wealth distribution the gradient falls. A second-order analysis (e.g. a τ_0 × τ_m grid, or a k × W_min grid) would capture interaction effects but is outside this document.

**SRR and LRR interaction.** The SRR and LRR sizing parameters interact: a higher srr_ratio diverts more net income into SRR accumulation before any surplus flows to the LRR, so rising srr_ratio extends the LRR fill year even when lrr_years is held constant. Conversely, a lower srr_ratio accelerates LRR accumulation but leaves a thinner refund buffer. The single-parameter-at-a-time sweeps in §§5–6 capture the first-order effect of each; a joint srr_ratio × lrr_years grid would expose the interaction surface and is a natural second-order extension.

**Rate parameters vs. SWF sizing parameters.** The sweeps in §§1–4 vary the rate function and therefore affect both revenue generation and individual taxpayer burden. The sweeps in §§5–6 vary only the capitalisation thresholds for the SRR and LRR; they do not alter the rate function or any individual tax liability. The burden distribution is therefore invariant across §§5–6 — those panels are flat by design, not an artefact. The sole effect is on when the SWF milestones are reached.

---

*Generated by `rates_param_sweep.py`. Source: `rates_model.py` / `wdt_core.py` / `7_4_…_Params.toml`. No existing project files were modified.*