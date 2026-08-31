# B. WDT Rate Parameter Sensitivity Sweep

**Run date:** 2026-08-31  
**Model version:** v6 (rates_model.py / wdt_core.py)  
**Parameters file:** `260812_WDT_Params.toml`  

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

**Success:** LRR fills within the 71-year modelling window AND (SRR never breaches OR SRR breach is fully covered by LRR balance at time of breach).

**SSM coverage ratio:** Average annual net SSM income over the capitalisation window (SRR fill to LRR fill) divided by average annual government expenditure over the same window. Applies the correlated-shock assumption (all taxpayers experience the same return simultaneously) — the worst-case floor.

**TCM coverage ratio:** Average annual TCM revenue over the same capitalisation window divided by average annual government expenditure. Applies four persistent heterogeneous growth tier differentials — the persistent-heterogeneity ceiling. Together the SSM and TCM ratios bracket the plausible revenue range.

**LRR fill year:** First year the LRR balance reaches the 3× expenditure floor. The primary transition-speed metric; gates full Phase Two fiscal replacement.

**SRR fill year:** First year the SRR reaches its capitalisation target. Should be invariant at ~3 across most calibrations.

**LRR surplus at fill:** LRR balance minus LRR target at the fill year, in £b. Safety margin above the floor at the breakeven point.

*All distributions are across the 73 historical start years 1947–2019. The 2006 start year is extracted separately as the worst-case historical scenario (longest LRR fill time at Balanced parameters).*

## B.2. Floor Rate (τ_0)

τ_0 sets the marginal rate at W = W_min. A higher floor raises effective rates across the entire taxable population (since every taxpayer above W_min pays at least τ_0 on their first pound of delta); a lower floor concentrates the rate gradient in the upper distribution.

### τ_0 sweep

Other parameters held at Balanced baseline: τ_m = 70%,  k = 0.001,  W_min = £2.0m.

**Sweep summary — distributions across 73 historical start years**

| Value | Success% | SSM cov (min/med/mean/max) | TCM cov (min/med/mean/max) | LRR fill yr (min/med/mean/max) | SRR fill yr (med) | LRR surplus £b (min/med) |
|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| 5% | 100% | 14.6% / 24.3% / 28.5% / 56.4% | 21.6% / 26.8% / 32.3% / 57.7% | 10 / 22 / 24 / 42 | 3 | 10 / 911 |
| 10% | 100% | 17.1% / 33.1% / 37.8% / 86.8% | 21.6% / 35.7% / 41.0% / 88.6% | 8 / 16 / 18 / 34 | 3 | 27 / 886 |
| 15% ◄ | 100% | 19.0% / 39.7% / 47.0% / 130.5% | 24.0% / 40.3% / 50.0% / 134.5% | 7 / 13 / 15 / 29 | 3 | 6 / 919 |
| 20% | 100% | 17.9% / 42.2% / 53.3% / 140.9% | 23.3% / 43.8% / 56.2% / 136.8% | 6 / 12 / 14 / 27 | 3 | 13 / 908 |
| 25% | 100% | 20.3% / 48.0% / 58.4% / 169.9% | 25.5% / 48.5% / 61.2% / 164.8% | 6 / 11 / 13 / 26 | 3 | 77 / 692 |
| 30% | 100% | 19.4% / 52.4% / 63.3% / 162.7% | 24.9% / 49.8% / 66.2% / 191.3% | 5 / 10 / 12 / 25 | 3 | 4 / 822 |
| 35% | 100% | 21.5% / 57.3% / 70.7% / 186.2% | 25.7% / 53.2% / 72.9% / 219.3% | 5 / 10 / 11 / 24 | 3 | 37 / 1095 |
| 40% | 100% | 20.1% / 61.4% / 74.3% / 203.6% | 23.9% / 57.4% / 74.9% / 208.5% | 5 / 10 / 11 / 24 | 3 | 30 / 1124 |
| 45% | 100% | 19.7% / 67.4% / 80.6% / 224.7% | 23.6% / 61.6% / 79.7% / 230.4% | 5 / 9 / 10 / 21 | 3 | 8 / 849 |
| 50% | 100% | 21.1% / 68.8% / 83.0% / 204.7% | 25.0% / 64.4% / 81.3% / 204.1% | 5 / 9 / 10 / 20 | 3 | 24 / 688 |

*◄ = Balanced baseline value. Coverage ratios: capitalisation-window averages (SRR fill to LRR fill). Distributions across all 73 historical start years 1947–2019.*

**2006 start year (worst-case historical scenario)**

| Value | SSM cov | TCM cov | LRR fill yr | LRR surplus £b | SRR breach covered |
|:---:|:---:|:---:|:---:|:---:|:---:|
| 5% | 16.4% | 23.7% | 39 | 1595 | — (no breach) |
| 10% | 18.0% | 24.6% | 34 | 1229 | — (no breach) |
| 15% ◄ | 20.8% | 27.1% | 29 | 523 | — (no breach) |
| 20% | 22.3% | 28.3% | 26 | 1999 | — (no breach) |
| 25% | 20.3% | 25.5% | 25 | 973 | YES |
| 30% | 24.6% | 28.8% | 25 | 2606 | YES |
| 35% | 29.7% | 29.6% | 21 | 411 | YES |
| 40% | 36.0% | 32.4% | 21 | 1277 | YES |
| 45% | 39.5% | 35.1% | 21 | 2075 | YES |
| 50% | 38.0% | 31.2% | 20 | 434 | YES |

## B.3. Ceiling Rate (τ_m)

τ_m is the asymptotic ceiling the marginal rate approaches but never reaches. Its primary effect is on the top brackets where W >> W_min; the logistic function brings effective rates close to τ_m only at very high declared wealth levels. Raising τ_m increases revenue from the highest-wealth, highest-growth cells disproportionately, since those cells also generate the largest absolute deltas.

### τ_m sweep

Other parameters held at Balanced baseline: τ_0 = 15%,  k = 0.001,  W_min = £2.0m.

**Sweep summary — distributions across 73 historical start years**

| Value | Success% | SSM cov (min/med/mean/max) | TCM cov (min/med/mean/max) | LRR fill yr (min/med/mean/max) | SRR fill yr (med) | LRR surplus £b (min/med) |
|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| 50% | 100% | 19.0% / 39.7% / 47.0% / 130.4% | 24.0% / 40.2% / 49.9% / 134.4% | 7 / 13 / 15 / 29 | 3 | 3 / 911 |
| 55% | 100% | 19.0% / 39.7% / 47.0% / 130.5% | 24.0% / 40.2% / 49.9% / 134.5% | 7 / 13 / 15 / 29 | 3 | 4 / 914 |
| 60% | 100% | 19.0% / 39.7% / 47.0% / 130.5% | 24.0% / 40.2% / 50.0% / 134.5% | 7 / 13 / 15 / 29 | 3 | 4 / 916 |
| 65% | 100% | 19.0% / 39.7% / 47.0% / 130.5% | 24.0% / 40.2% / 50.0% / 134.5% | 7 / 13 / 15 / 29 | 3 | 5 / 918 |
| 70% ◄ | 100% | 19.0% / 39.7% / 47.0% / 130.5% | 24.0% / 40.3% / 50.0% / 134.5% | 7 / 13 / 15 / 29 | 3 | 6 / 919 |
| 75% | 100% | 19.0% / 39.8% / 47.0% / 130.5% | 24.0% / 40.3% / 50.0% / 134.5% | 7 / 13 / 15 / 29 | 3 | 6 / 920 |
| 80% | 100% | 19.0% / 39.8% / 47.0% / 130.6% | 24.0% / 40.3% / 50.0% / 134.6% | 7 / 13 / 15 / 29 | 3 | 7 / 921 |
| 85% | 100% | 19.0% / 39.8% / 47.0% / 130.6% | 24.0% / 40.3% / 50.0% / 134.6% | 7 / 13 / 15 / 29 | 3 | 7 / 922 |
| 90% | 100% | 19.0% / 39.8% / 47.0% / 130.6% | 24.0% / 40.3% / 50.0% / 134.6% | 7 / 13 / 15 / 29 | 3 | 7 / 923 |
| 95% | 100% | 19.0% / 39.8% / 47.0% / 130.6% | 24.0% / 40.3% / 50.0% / 134.6% | 7 / 13 / 15 / 29 | 3 | 8 / 924 |
| 100% | 100% | 19.0% / 39.8% / 47.0% / 130.6% | 24.0% / 40.3% / 50.0% / 134.6% | 7 / 13 / 15 / 29 | 3 | 8 / 925 |

*◄ = Balanced baseline value. Coverage ratios: capitalisation-window averages (SRR fill to LRR fill). Distributions across all 73 historical start years 1947–2019.*

**2006 start year (worst-case historical scenario)**

| Value | SSM cov | TCM cov | LRR fill yr | LRR surplus £b | SRR breach covered |
|:---:|:---:|:---:|:---:|:---:|:---:|
| 50% | 20.8% | 27.0% | 29 | 514 | — (no breach) |
| 55% | 20.8% | 27.0% | 29 | 517 | — (no breach) |
| 60% | 20.8% | 27.1% | 29 | 519 | — (no breach) |
| 65% | 20.8% | 27.1% | 29 | 521 | — (no breach) |
| 70% ◄ | 20.8% | 27.1% | 29 | 523 | — (no breach) |
| 75% | 20.8% | 27.1% | 29 | 524 | — (no breach) |
| 80% | 20.8% | 27.1% | 29 | 525 | — (no breach) |
| 85% | 20.8% | 27.1% | 29 | 526 | — (no breach) |
| 90% | 20.8% | 27.1% | 29 | 527 | — (no breach) |
| 95% | 20.8% | 27.1% | 29 | 528 | — (no breach) |
| 100% | 20.8% | 27.1% | 29 | 529 | — (no breach) |

## B.4. Steepness (k)

k (per £m) controls how rapidly the marginal rate climbs from τ_0 toward τ_m through the wealth distribution. Low k produces a shallow gradient — most taxpayers face rates close to τ_0 even at high wealth levels, with τ_m approached only at very large holdings. High k produces a steep step — the rate reaches τ_m quickly above W_min, compressing the gradient into a narrow wealth band.

*Sweep is log-spaced: 0.0001, 0.0002, 0.0005, 0.0010, 0.0020, 0.0050, 0.0100, 0.0500, 0.1000*

### k sweep (log-spaced)

Other parameters held at Balanced baseline: τ_0 = 15%,  τ_m = 70%,  W_min = £2.0m.

**Sweep summary — distributions across 73 historical start years**

| Value | Success% | SSM cov (min/med/mean/max) | TCM cov (min/med/mean/max) | LRR fill yr (min/med/mean/max) | SRR fill yr (med) | LRR surplus £b (min/med) |
|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| 0.0001 | 100% | 18.9% / 39.6% / 46.8% / 129.9% | 23.8% / 40.1% / 49.6% / 133.8% | 7 / 13 / 15 / 29 | 3 | 14 / 859 |
| 0.0002 | 100% | 18.9% / 39.6% / 46.8% / 129.9% | 23.8% / 40.1% / 49.6% / 133.9% | 7 / 13 / 15 / 29 | 3 | 17 / 866 |
| 0.0005 | 100% | 18.9% / 39.6% / 46.9% / 130.2% | 23.9% / 40.1% / 49.7% / 134.1% | 7 / 13 / 15 / 29 | 3 | 29 / 886 |
| 0.0010 ◄ | 100% | 19.0% / 39.7% / 47.0% / 130.5% | 24.0% / 40.3% / 50.0% / 134.5% | 7 / 13 / 15 / 29 | 3 | 6 / 919 |
| 0.0020 | 100% | 19.1% / 40.0% / 47.2% / 131.3% | 24.2% / 40.5% / 50.1% / 135.3% | 7 / 13 / 15 / 29 | 3 | 0 / 939 |
| 0.0050 | 100% | 19.2% / 40.6% / 47.1% / 112.2% | 24.0% / 41.1% / 50.0% / 109.3% | 6 / 13 / 15 / 29 | 3 | 22 / 727 |
| 0.0100 | 100% | 18.9% / 41.2% / 47.7% / 115.0% | 24.7% / 40.7% / 50.7% / 112.1% | 6 / 13 / 15 / 29 | 3 | 4 / 718 |
| 0.0500 | 100% | 16.7% / 41.5% / 51.9% / 133.4% | 22.6% / 44.2% / 55.0% / 131.0% | 6 / 12 / 14 / 27 | 3 | 3 / 845 |
| 0.1000 | 100% | 18.4% / 43.1% / 55.7% / 151.3% | 23.5% / 44.9% / 59.0% / 149.2% | 6 / 12 / 14 / 27 | 3 | 70 / 1067 |

*◄ = Balanced baseline value. Coverage ratios: capitalisation-window averages (SRR fill to LRR fill). Distributions across all 73 historical start years 1947–2019.*

**2006 start year (worst-case historical scenario)**

| Value | SSM cov | TCM cov | LRR fill yr | LRR surplus £b | SRR breach covered |
|:---:|:---:|:---:|:---:|:---:|:---:|
| 0.0001 | 20.7% | 26.9% | 29 | 457 | — (no breach) |
| 0.0002 | 20.7% | 26.9% | 29 | 464 | — (no breach) |
| 0.0005 | 20.7% | 27.0% | 29 | 486 | — (no breach) |
| 0.0010 ◄ | 20.8% | 27.1% | 29 | 523 | — (no breach) |
| 0.0020 | 20.9% | 27.3% | 29 | 596 | — (no breach) |
| 0.0050 | 21.3% | 27.9% | 29 | 809 | YES |
| 0.0100 | 21.8% | 28.7% | 29 | 1136 | YES |
| 0.0500 | 21.3% | 28.1% | 26 | 1442 | YES |
| 0.1000 | 25.3% | 31.8% | 26 | 2820 | YES |

## B.5. Entry Point (W_min)

W_min (£m) is the wealth level below which the rate function produces zero liability. It is a rate design parameter, not a population boundary — all UK adults are within the taxable population regardless of W_min. Lower W_min pulls more of the 50th–80th percentile brackets into material liability; higher W_min concentrates the tax on the top percentiles. W_min also affects refund exposure in loss years, since a taxpayer below W_min receives no refund even if their delta is negative.

### W_min sweep

Other parameters held at Balanced baseline: τ_0 = 15%,  τ_m = 70%,  k = 0.001.

**Sweep summary — distributions across 73 historical start years**

| Value | Success% | SSM cov (min/med/mean/max) | TCM cov (min/med/mean/max) | LRR fill yr (min/med/mean/max) | SRR fill yr (med) | LRR surplus £b (min/med) |
|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| £0.1m | 100% | 19.8% / 47.6% / 58.9% / 141.3% | 22.8% / 45.1% / 60.4% / 142.4% | 6 / 10 / 12 / 26 | 3 | 1 / 557 |
| £0.25m | 100% | 19.8% / 47.6% / 58.9% / 141.3% | 22.8% / 45.1% / 60.4% / 142.4% | 6 / 10 / 12 / 26 | 3 | 1 / 557 |
| £0.5m | 100% | 19.8% / 47.6% / 59.1% / 141.2% | 22.9% / 45.3% / 60.5% / 142.4% | 6 / 11 / 12 / 26 | 3 | 49 / 545 |
| £1.0m | 100% | 18.6% / 44.1% / 56.3% / 137.5% | 22.0% / 45.4% / 58.4% / 136.6% | 6 / 11 / 13 / 27 | 3 | 2 / 895 |
| £2.0m ◄ | 100% | 19.0% / 39.7% / 47.0% / 130.5% | 24.0% / 40.3% / 50.0% / 134.5% | 7 / 13 / 15 / 29 | 3 | 6 / 919 |
| £3.0m | 100% | 18.0% / 33.9% / 39.2% / 89.8% | 24.9% / 38.0% / 44.0% / 98.9% | 8 / 15 / 17 / 33 | 3 | 52 / 976 |
| £5.0m | 100% | 15.7% / 27.8% / 33.0% / 72.2% | 23.5% / 34.0% / 39.9% / 79.9% | 9 / 18 / 20 / 35 | 3 | 72 / 1210 |
| £7.5m | 100% | 14.2% / 24.8% / 29.5% / 61.3% | 20.7% / 32.9% / 36.9% / 62.7% | 10 / 21 / 22 / 37 | 3 | 12 / 1001 |
| £10.0m | 100% | 13.4% / 23.3% / 26.9% / 51.8% | 21.9% / 34.3% / 36.4% / 63.2% | 11 / 22 / 24 / 39 | 3 | 79 / 1250 |

*◄ = Balanced baseline value. Coverage ratios: capitalisation-window averages (SRR fill to LRR fill). Distributions across all 73 historical start years 1947–2019.*

**2006 start year (worst-case historical scenario)**

| Value | SSM cov | TCM cov | LRR fill yr | LRR surplus £b | SRR breach covered |
|:---:|:---:|:---:|:---:|:---:|:---:|
| £0.1m | 20.6% | 23.1% | 25 | 267 | — (no breach) |
| £0.25m | 20.6% | 23.1% | 25 | 266 | — (no breach) |
| £0.5m | 20.4% | 23.0% | 25 | 207 | — (no breach) |
| £1.0m | 23.2% | 26.7% | 26 | 1779 | — (no breach) |
| £2.0m ◄ | 20.8% | 27.1% | 29 | 523 | — (no breach) |
| £3.0m | 19.2% | 28.1% | 32 | 961 | — (no breach) |
| £5.0m | 19.5% | 31.6% | 35 | 4518 | — (no breach) |
| £7.5m | 14.2% | 26.4% | 35 | 115 | — (no breach) |
| £10.0m | 14.0% | 30.1% | 38 | 2710 | — (no breach) |

## B.6. SRR Capitalisation Ratio (srr_ratio)

srr_ratio sets the SRR capitalisation target as a multiple of average annual net WDT income. A higher ratio means the SRR must accumulate more before it is considered fully capitalised, which delays SRR fill and thereby reduces the flow into the LRR during the early accumulation period. A lower ratio allows faster SRR fill and faster LRR accumulation, but at the cost of a thinner refund buffer. The Governing Council recommended floor is 3×; the working SSM-derived value is 3×.

*Note: srr_ratio does not affect the rate function or individual taxpayer burden — it affects only the milestone timing (SRR fill year and LRR fill year). The burden distribution panel in the chart companion is flat across this sweep.*

### srr_ratio sweep

Other parameters held at Balanced baseline: τ_0 = 15%,  τ_m = 70%,  k = 0.001,  W_min = £2.0m,  lrr_years = 3.0.

**Sweep summary — distributions across 73 historical start years**

| Value | Success% | SSM cov (min/med/mean/max) | TCM cov (min/med/mean/max) | LRR fill yr (min/med/mean/max) | SRR fill yr (med) | LRR surplus £b (min/med) |
|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| 1.0× | 100% | 18.5% / 32.1% / 37.7% / 78.0% | 21.2% / 33.9% / 39.2% / 87.1% | 5 / 12 / 14 / 28 | 1 | 10 / 641 |
| 1.5× | 100% | 18.6% / 33.8% / 40.0% / 89.4% | 21.8% / 35.7% / 42.1% / 91.4% | 6 / 12 / 14 / 28 | 2 | 0 / 580 |
| 2.0× | 100% | 18.5% / 36.7% / 42.1% / 90.3% | 23.1% / 38.2% / 44.2% / 88.7% | 6 / 13 / 15 / 29 | 2 | 17 / 654 |
| 2.5× | 100% | 18.8% / 39.3% / 45.2% / 110.0% | 23.4% / 38.4% / 47.5% / 107.0% | 6 / 13 / 15 / 29 | 3 | 17 / 657 |
| 3.0× ◄ | 100% | 19.0% / 39.7% / 47.0% / 130.5% | 24.0% / 40.3% / 50.0% / 134.5% | 7 / 13 / 15 / 29 | 3 | 6 / 919 |
| 4.0× | 100% | 18.8% / 44.6% / 52.2% / 126.9% | 24.5% / 50.5% / 56.3% / 132.3% | 8 / 14 / 16 / 29 | 4 | 28 / 956 |
| 5.0× | 100% | 18.7% / 45.6% / 57.8% / 149.5% | 24.5% / 50.4% / 62.1% / 152.5% | 8 / 15 / 17 / 30 | 5 | 2 / 831 |
| 6.0× | 100% | 20.7% / 50.5% / 63.2% / 157.9% | 28.4% / 49.9% / 68.2% / 165.7% | 9 / 16 / 18 / 31 | 6 | 31 / 840 |
| 8.0× | 100% | 21.5% / 61.2% / 77.8% / 238.7% | 29.9% / 65.1% / 84.3% / 245.1% | 11 / 17 / 19 / 33 | 8 | 4 / 1026 |
| 10.0× | 100% | 22.8% / 65.1% / 91.7% / 276.3% | 31.9% / 62.8% / 99.6% / 287.3% | 13 / 19 / 21 / 34 | 10 | 2 / 1073 |

*◄ = Balanced baseline value. Coverage ratios: capitalisation-window averages (SRR fill to LRR fill). Distributions across all 73 historical start years 1947–2019.*

**2006 start year (worst-case historical scenario)**

| Value | SSM cov | TCM cov | LRR fill yr | LRR surplus £b | SRR breach covered |
|:---:|:---:|:---:|:---:|:---:|:---:|
| 1.0× | 18.5% | 21.6% | 26 | 282 | YES |
| 1.5× | 18.6% | 21.8% | 26 | 67 | YES |
| 2.0× | 20.9% | 26.3% | 29 | 1002 | YES |
| 2.5× | 21.7% | 27.1% | 29 | 762 | — (no breach) |
| 3.0× ◄ | 20.8% | 27.1% | 29 | 523 | — (no breach) |
| 4.0× | 21.1% | 27.5% | 29 | 43 | — (no breach) |
| 5.0× | 22.0% | 30.1% | 30 | 1146 | — (no breach) |
| 6.0× | 22.6% | 30.7% | 30 | 601 | — (no breach) |
| 8.0× | 24.0% | 33.2% | 32 | 768 | — (no breach) |
| 10.0× | 26.1% | 36.4% | 34 | 2489 | — (no breach) |

## B.7. LRR Floor (lrr_years)

lrr_years sets the LRR floor as a multiple of prevailing government expenditure. The LRR target therefore grows over time as nominal expenditure grows at 4.51% p.a. A higher floor requires the LRR to accumulate more before Phase Two becomes viable, directly extending the LRR fill year. A lower floor brings LRR fill earlier but with a thinner buffer against sustained drawdown post-fill. The recommended minimum is 3 years.

*Note: lrr_years does not affect the rate function or individual taxpayer burden — it affects only the LRR milestone timing and the safety margin above the floor. The burden distribution panel in the chart companion is flat across this sweep.*

### lrr_years sweep

Other parameters held at Balanced baseline: τ_0 = 15%,  τ_m = 70%,  k = 0.001,  W_min = £2.0m,  srr_ratio = 3.0×.

**Sweep summary — distributions across 73 historical start years**

| Value | Success% | SSM cov (min/med/mean/max) | TCM cov (min/med/mean/max) | LRR fill yr (min/med/mean/max) | SRR fill yr (med) | LRR surplus £b (min/med) |
|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| 0.5 yrs | 100% | -0.4% / 20.3% / 26.3% / 109.8% | -0.0% / 20.7% / 27.6% / 107.8% | 4 / 6 / 7 / 12 | 3 | 3 / 192 |
| 1.0 yrs | 100% | 7.5% / 25.4% / 32.3% / 93.2% | 10.0% / 27.8% / 33.3% / 96.7% | 5 / 8 / 9 / 19 | 3 | 4 / 311 |
| 1.5 yrs | 100% | 10.5% / 28.4% / 35.7% / 88.1% | 13.8% / 27.9% / 37.7% / 102.7% | 5 / 10 / 11 / 24 | 3 | 6 / 582 |
| 2.0 yrs | 100% | 13.3% / 29.9% / 38.6% / 110.0% | 17.4% / 33.1% / 41.2% / 107.0% | 6 / 11 / 13 / 26 | 3 | 16 / 421 |
| 2.5 yrs | 100% | 14.2% / 35.0% / 43.4% / 110.0% | 18.8% / 37.2% / 45.9% / 107.0% | 6 / 12 / 14 / 27 | 3 | 4 / 685 |
| 3.0 yrs ◄ | 100% | 19.0% / 39.7% / 47.0% / 130.5% | 24.0% / 40.3% / 50.0% / 134.5% | 7 / 13 / 15 / 29 | 3 | 6 / 919 |
| 4.0 yrs | 100% | 23.7% / 45.0% / 51.6% / 122.0% | 29.7% / 48.8% / 55.5% / 124.3% | 8 / 15 / 18 / 34 | 3 | 6 / 895 |
| 5.0 yrs | 100% | 27.6% / 51.9% / 57.9% / 126.6% | 34.9% / 53.6% / 61.8% / 127.2% | 8 / 17 / 20 / 36 | 3 | 39 / 1220 |
| 6.0 yrs | 100% | 32.9% / 55.9% / 65.0% / 134.0% | 39.1% / 57.5% / 69.4% / 141.1% | 9 / 20 / 22 / 39 | 3 | 62 / 1383 |
| 8.0 yrs | 100% | 43.2% / 63.8% / 75.8% / 147.2% | 55.9% / 68.6% / 82.4% / 150.3% | 10 / 24 / 25 / 42 | 3 | 20 / 2037 |

*◄ = Balanced baseline value. Coverage ratios: capitalisation-window averages (SRR fill to LRR fill). Distributions across all 73 historical start years 1947–2019.*

**2006 start year (worst-case historical scenario)**

| Value | SSM cov | TCM cov | LRR fill yr | LRR surplus £b | SRR breach covered |
|:---:|:---:|:---:|:---:|:---:|:---:|
| 0.5 yrs | 12.4% | 13.6% | 9 | 13 | — (no breach) |
| 1.0 yrs | 15.6% | 15.4% | 13 | 108 | — (no breach) |
| 1.5 yrs | 12.5% | 15.4% | 21 | 309 | — (no breach) |
| 2.0 yrs | 13.5% | 17.4% | 25 | 583 | — (no breach) |
| 2.5 yrs | 17.6% | 22.5% | 26 | 1166 | — (no breach) |
| 3.0 yrs ◄ | 20.8% | 27.1% | 29 | 523 | — (no breach) |
| 4.0 yrs | 25.1% | 33.6% | 34 | 2595 | — (no breach) |
| 5.0 yrs | 29.0% | 38.6% | 35 | 2708 | — (no breach) |
| 6.0 yrs | 34.6% | 44.1% | 38 | 5138 | — (no breach) |
| 8.0 yrs | 44.0% | 56.2% | 39 | 150 | — (no breach) |

# C. Reading Notes

**Coverage ratio direction.** SSM and TCM coverage ratios move together when a parameter raises or lowers the rate on the bulk of the distribution. The gap between them (TCM − SSM) measures the sensitivity of revenue to persistent growth heterogeneity; a wide gap means higher-tier taxpayers contribute disproportionately more than the correlated-shock assumption would imply.

**Success rate at 100%.** The Balanced baseline achieves 100% success across all 73 start years. Parameters that reduce revenue significantly may bring the success rate below 100%, meaning the LRR fails to fill within the 71-year window for some historical starting conditions. This is the primary solvency constraint.

**SRR fill year.** Should remain ~3 across most calibrations. If it rises significantly, the refund guarantee becomes credible only after more than one political cycle, which is a materially different political position.

**LRR surplus.** A near-zero surplus at fill (see e.g. the 1953 start year at Balanced parameters, £28b surplus) indicates the mechanism passed its solvency test narrowly. A calibration that systematically reduces surplus increases the risk that a slightly worse return sequence would cause LRR non-fill.

**Pre-behavioural baseline.** All figures are pre-behavioural. Behavioural responses — migration, restructuring, avoidance — are not modelled and will reduce actual revenue by an unknown amount. See RATES §9.1 and BEHAV.

**Joint calibration.** These sweeps vary one parameter at a time. In practice, τ_0 and τ_m jointly determine both the level and shape of revenue; W_min and k jointly determine where in the wealth distribution the gradient falls. A second-order analysis (e.g. a τ_0 × τ_m grid, or a k × W_min grid) would capture interaction effects but is outside this document.

**SRR and LRR interaction.** The SRR and LRR sizing parameters interact: a higher srr_ratio diverts more net income into SRR accumulation before any surplus flows to the LRR, so rising srr_ratio extends the LRR fill year even when lrr_years is held constant. Conversely, a lower srr_ratio accelerates LRR accumulation but leaves a thinner refund buffer. The single-parameter-at-a-time sweeps in §§5–6 capture the first-order effect of each; a joint srr_ratio × lrr_years grid would expose the interaction surface and is a natural second-order extension.

**Rate parameters vs. SWF sizing parameters.** The sweeps in §§1–4 vary the rate function and therefore affect both revenue generation and individual taxpayer burden. The sweeps in §§5–6 vary only the capitalisation thresholds for the SRR and LRR; they do not alter the rate function or any individual tax liability. The burden distribution is therefore invariant across §§5–6 — those panels are flat by design, not an artefact. The sole effect is on when the SWF milestones are reached.

---

*Generated by `rates_param_sweep.py`. Source: `rates_model.py` / `wdt_core.py` / `7_4_…_Params.toml`. No existing project files were modified.*