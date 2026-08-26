# VAL.A Appendix C — Full Simulation Tables

**Generated:** 2026-08-17  
**Model version:** Python v1.0 (standalone, no Excel dependency)  
**Parameters:** $V_0$ = £20m · $	au_0$ = 15% · $	au_m$ = 70% · k = 0.001 · W_min = £2m · N = 29 · g = 10.45%  
**Validation status:** 0 FAILs across all primary matrices (confirmed against Excel 27 July 2026)  
**N-offset:** Tables C.7/C.8 show actual simulation N; Excel displayed N-5 in column headers — corrected here.  
**Beta formula:** Additive g_eff = g + β·ln(α); VAL.A §B.3 shows multiplicative form — that section requires update.  
**Table C.4 note:** Max 2.67% deviation from Excel (known snapshot issue); Python values used throughout.  

## C.1 Total Tax Paid Difference Relative to Honest Declaration, as Share of Terminal Net Worth

**Formula:** (Net(α) − Net(1)) / TW(α)  ·  Positive = α pays more than honest; negative = pays less.

| α \ g | -4.5% | 0.4% | 5.9% | 8.4% | 10.4% | 11.4% | 13.9% | 16.4% | 20.4% | 25.4% |
|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| **0.1** | 15.55% | 14.14% | 4.16% | 3.17% | 3.36% | 3.80% | 6.50% | 14.03% | 54.21% | 97.95% |
| **0.2** | 13.49% | 12.35% | 3.59% | 2.68% | 2.79% | 3.12% | 5.27% | 11.20% | 40.62% | 69.57% |
| **0.5** | 7.71% | 7.34% | 2.06% | 1.44% | 1.39% | 1.51% | 2.42% | 4.94% | 15.62% | 24.49% |
| **0.8** | 2.49% | 2.79% | 0.75% | 0.49% | 0.43% | 0.45% | 0.66% | 1.31% | 3.88% | 6.25% |
| **1.0** | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% |
| **1.2** | 0.00% | -1.65% | -0.67% | -0.39% | -0.28% | -0.26% | -0.31% | -0.60% | -1.97% | -3.88% |
| **1.5** | 0.00% | -1.64% | -1.55% | -0.80% | -0.45% | -0.34% | -0.21% | -0.42% | -2.65% | -7.17% |
| **1.8** | 0.00% | -1.64% | -2.27% | -1.03% | -0.35% | -0.09% | 0.48% | 0.74% | -1.68% | -8.73% |
| **2.0** | 0.00% | -1.63% | -2.68% | -1.09% | -0.15% | 0.23% | 1.21% | 1.95% | -0.49% | -9.20% |

*Base parameters. α = 1.0 row is zero by construction. Positive values indicate understater pays more lifetime tax.*

## C.2 Effective Lifetime Tax Rate Difference from Honest Declaration

**Formula:** Net(α)/TW(α) − Net(1)/TW(1)  ·  Positive = α has higher effective rate than honest.

| α \ g | -4.5% | 0.4% | 5.9% | 8.4% | 10.4% | 11.4% | 13.9% | 16.4% | 20.4% | 25.4% |
|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| **0.1** | 15.55% | 14.41% | 6.04% | 5.38% | 5.85% | 6.44% | 9.88% | 19.36% | 72.58% | 129.18% |
| **0.2** | 13.49% | 12.58% | 5.23% | 4.61% | 4.95% | 5.42% | 8.18% | 15.69% | 54.97% | 94.30% |
| **0.5** | 7.71% | 7.47% | 3.03% | 2.58% | 2.67% | 2.86% | 4.08% | 7.37% | 22.10% | 36.63% |
| **0.8** | 2.49% | 2.85% | 1.13% | 0.92% | 0.91% | 0.96% | 1.28% | 2.16% | 5.89% | 10.31% |
| **1.0** | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% |
| **1.2** | 0.00% | -1.68% | -1.02% | -0.79% | -0.73% | -0.73% | -0.87% | -1.33% | -3.51% | -7.22% |
| **1.5** | 0.00% | -1.68% | -2.38% | -1.77% | -1.52% | -1.46% | -1.50% | -2.09% | -5.96% | -14.55% |
| **1.8** | 0.00% | -1.68% | -3.55% | -2.51% | -1.97% | -1.79% | -1.46% | -1.69% | -6.34% | -19.31% |
| **2.0** | 0.00% | -1.68% | -4.24% | -2.89% | -2.12% | -1.81% | -1.12% | -0.93% | -5.89% | -21.57% |

*VAL.A §C.2 describes this as 'effective lifetime tax rate from terminal wealth' but the formula is a difference relative to honest. Label in VAL.A §C.2 heading requires correction.*

## C.3 Exploratory Extension: Investor Confidence Effects β (Overstatement Only)

**Formula:** (Net(α,β) − Net(1,β=0)) / TW(α,β)  ·  β swept over same numeric values as g columns; g fixed at 10.45%.
**Beta formula:** g_eff = g + β·ln(α) [additive — confirmed from Excel; VAL.A §B.3 states multiplicative form incorrectly].
**Scope:** Overstatement only (α ≥ 1.0). Understater cells omitted — analytical scope for signalling is overstatement.

| α \ β | β=-4.5% | β=0.4% | β=5.9% | β=8.4% | β=10.4% | β=11.4% | β=13.9% | β=16.4% | β=20.4% | β=25.4% |
|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| **1.0** | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% |
| **1.2** | -4.16% | 0.07% | 3.89% | 5.44% | 6.63% | 7.15% | 8.49% | 9.78% | 11.70% | 14.00% |
| **1.5** | -9.96% | 0.30% | 7.78% | 10.52% | 12.60% | 13.53% | 15.94% | 18.40% | 22.32% | 27.26% |
| **1.8** | -15.46% | 0.73% | 10.97% | 14.73% | 17.69% | 19.04% | 22.46% | 25.58% | 29.38% | 33.38% |
| **2.0** | -19.02% | 1.14% | 13.18% | 17.74% | 21.26% | 22.77% | 26.13% | 28.36% | 30.49% | 34.48% |

*Exploratory only. No empirical calibration for β exists. Sign convention: positive = α pays more than honest. Deviations increase at high α×β due to exponential compounding over N=34.*

## C.4 Effective Lifetime Tax Rate by k Parameter and Initial Wealth ($V_0$)

**Formula:** TTP(α=1) / TW(α=1)  ·  Honest declaration throughout. Rows = k; columns = $V_0$ (£m).
**Note:** Max 2.67% deviation from Excel (known snapshot — Excel AppC cells computed at different params state). Python values used.

| k \ $V_0$ | £1m | £10m | £50m | £100m | £250m | £500m | £1000m | £2500m | £5000m | £10000m |
|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| 1e-04 | 13.33% | 14.16% | 14.51% | 14.94% | 16.28% | 18.58% | 23.24% | 34.97% | 45.96% | 54.53% |
| 2e-04 | 13.33% | 14.25% | 14.94% | 15.83% | 18.58% | 23.24% | 31.56% | 45.96% | 54.53% | 59.18% |
| 5e-04 | 13.36% | 14.50% | 16.27% | 18.57% | 25.49% | 34.96% | 45.96% | 56.45% | 59.91% | 60.64% |
| 1e-03 | 13.39% | 14.92% | 18.56% | 23.22% | 34.95% | 45.95% | 54.53% | 59.90% | 60.64% | 60.67% |
| 2e-03 | 13.46% | 15.78% | 23.20% | 31.53% | 45.94% | 54.52% | 59.18% | 60.64% | 60.67% | 60.67% |
| 5e-03 | 13.67% | 18.47% | 34.88% | 45.90% | 56.43% | 59.90% | 60.64% | 60.67% | 60.67% | 60.67% |
| 1e-02 | 14.03% | 23.01% | 45.84% | 54.47% | 59.89% | 60.64% | 60.67% | 60.67% | 60.67% | 60.67% |
| 5e-02 | 17.00% | 45.33% | 59.84% | 60.64% | 60.67% | 60.67% | 60.67% | 60.67% | 60.67% | 60.67% |
| 1e-01 | 20.85% | 53.82% | 60.63% | 60.67% | 60.67% | 60.67% | 60.67% | 60.67% | 60.67% | 60.67% |

*All at α=1, β=0, g=10.45%, N=34. k values above 0.001 are analytically extreme; included for completeness.*

## C.5 Sensitivity of k and Alpha: Terminal Net Worth Difference vs Honest

**Formula:** (TW(α,k) − TW(1,k)) / TW(1,k)  ·  Positive = α retains more TW than honest; negative = less.

| α \ k | 1e-04 | 2e-04 | 5e-04 | 1e-03 | 2e-03 | 5e-03 | 1e-02 | 5e-02 | 1e-01 |
|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| **0.1** | -12.62% | -12.70% | -13.00% | -13.58% | -15.13% | -22.49% | -36.64% | -35.14% | -32.43% |
| **0.2** | -11.21% | -11.29% | -11.54% | -12.03% | -13.34% | -19.45% | -30.99% | -31.86% | -33.06% |
| **0.5** | -7.00% | -7.04% | -7.18% | -7.45% | -8.13% | -11.19% | -16.76% | -21.12% | -24.20% |
| **0.8** | -2.80% | -2.81% | -2.86% | -2.95% | -3.18% | -4.13% | -5.89% | -8.72% | -10.38% |
| **1.0** | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% |
| **1.2** | 2.80% | 2.81% | 2.85% | 2.91% | 3.08% | 3.75% | 5.10% | 8.96% | 11.04% |
| **1.5** | 6.99% | 7.01% | 7.08% | 7.21% | 7.51% | 8.76% | 11.69% | 22.76% | 28.52% |
| **1.8** | 11.17% | 11.20% | 11.29% | 11.43% | 11.74% | 13.20% | 17.40% | 36.98% | 46.77% |
| **2.0** | 13.96% | 13.99% | 14.07% | 14.20% | 14.45% | 15.90% | 20.89% | 46.69% | 59.22% |

*α = 1.0 row is zero by construction. g = 10.45%, N = 34 throughout.*

## C.6 Terminal Net Worth After Refunds: Refund Protection Ratio

**Formula:** TW(α) / TW(1)  ·  Values below 100% = reduced TW relative to honest. Negative g scenarios only.

| α \ g | -4.5% |
|:---:|:---:|
| **0.1** | 86.54% |
| **0.2** | 88.12% |
| **0.5** | 92.84% |
| **0.8** | 97.57% |
| **1.0** | 100.00% |
| **1.2** | 100.00% |
| **1.5** | 100.00% |
| **1.8** | 100.00% |
| **2.0** | 100.00% |

*Negative g scenarios only. α = 1.0 is 100% by construction. Understater protection loss proportional to basis gap at entry.*

## C.7 Total Tax Paid Compared to Honest Taxpayer, Adjusted for N

**Formula:** (Net(α,N) − Net(1,N)) / Net(1,N)  ·  Positive = α pays more net tax than honest.
**N correction:** Values shown are actual simulation N (5 to 60). Excel headers showed N-5 (0 to 55) — corrected here.

| α \ N | 5 | 10 | 15 | 20 | 25 | 30 | 35 | 40 | 45 | 50 | 55 | 60 |
|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| **0.1** | 129.59% | 57.45% | 32.74% | 22.19% | 18.29% | 18.82% | 23.55% | 33.45% | 50.46% | 75.96% | 104.86% | 121.86% |
| **0.2** | 115.06% | 50.87% | 28.83% | 19.32% | 15.66% | 15.84% | 19.55% | 27.55% | 41.31% | 61.73% | 84.41% | 96.99% |
| **0.5** | 71.66% | 31.43% | 17.50% | 11.33% | 8.68% | 8.22% | 9.64% | 13.18% | 19.37% | 28.31% | 37.70% | 42.32% |
| **0.8** | 28.56% | 12.43% | 6.79% | 4.23% | 3.03% | 2.62% | 2.84% | 3.70% | 5.32% | 7.67% | 10.17% | 11.58% |
| **1.0** | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% |
| **1.2** | -28.43% | -12.23% | -6.52% | -3.83% | -2.44% | -1.74% | -1.50% | -1.69% | -2.36% | -3.61% | -5.27% | -6.79% |
| **1.5** | -70.82% | -30.22% | -15.78% | -8.83% | -4.99% | -2.69% | -1.30% | -0.65% | -0.97% | -2.82% | -6.45% | -10.86% |
| **1.8** | -100.00% | -47.77% | -24.41% | -12.92% | -6.21% | -1.70% | 1.74% | 4.37% | 5.53% | 3.71% | -2.03% | -10.10% |
| **2.0** | -100.00% | -59.22% | -29.82% | -15.15% | -6.30% | 0.04% | 5.29% | 9.75% | 12.26% | 10.48% | 3.06% | -7.80% |

*g = 10.45% throughout. α = 1.0 row is zero by construction. Understater penalty at N=5 reflects large realisation delta on short horizon.*

## C.8 Terminal Net Worth Compared to Honest Taxpayer, Adjusted for N

**Formula:** (TW(α,N) − TW(1,N)) / TW(1,N)  ·  Negative = α retains less TW than honest.
**N correction:** As C.7 — actual N shown.

| α \ N | 5 | 10 | 15 | 20 | 25 | 30 | 35 | 40 | 45 | 50 | 55 | 60 |
|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| **0.1** | -12.76% | -12.81% | -12.89% | -13.03% | -13.26% | -13.69% | -14.49% | -16.09% | -19.35% | -25.60% | -34.87% | -41.99% |
| **0.2** | -11.34% | -11.39% | -11.46% | -11.57% | -11.77% | -12.12% | -12.80% | -14.13% | -16.82% | -21.91% | -29.41% | -35.24% |
| **0.5** | -7.09% | -7.11% | -7.15% | -7.21% | -7.31% | -7.49% | -7.84% | -8.51% | -9.83% | -12.25% | -15.76% | -18.76% |
| **0.8** | -2.83% | -2.84% | -2.85% | -2.87% | -2.91% | -2.97% | -3.07% | -3.28% | -3.68% | -4.41% | -5.48% | -6.55% |
| **1.0** | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% |
| **1.2** | 2.83% | 2.84% | 2.85% | 2.86% | 2.88% | 2.92% | 2.99% | 3.13% | 3.39% | 3.88% | 4.67% | 5.66% |
| **1.5** | 7.08% | 7.09% | 7.10% | 7.13% | 7.17% | 7.23% | 7.34% | 7.56% | 8.00% | 8.91% | 10.57% | 12.96% |
| **1.8** | 10.50% | 11.33% | 11.35% | 11.37% | 11.40% | 11.44% | 11.52% | 11.70% | 12.13% | 13.22% | 15.55% | 19.25% |
| **2.0** | 11.55% | 14.16% | 14.17% | 14.18% | 14.19% | 14.20% | 14.22% | 14.31% | 14.66% | 15.80% | 18.50% | 23.03% |

*g = 10.45% throughout. α = 1.0 row is zero by construction.*

## C.9 Summary of Declaration Incentives Across Growth Regimes

**Columns:** TW(£m) and Net tax (£m) at α∈{2.0, 1.0, 0.1}; ratios vs honest. N = 34 throughout.

| g | TW(α=2) £m | TW(α=1) £m | TW(α=0.1) £m | Net(α=2) £m | Net(α=1) £m | Net(α=0.1) £m | TW(0.1)/TW(1) | Net(0.1)/Net(1) |
|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| 25.4% | 5559.5 | 4274.7 | 2699.9 | 1777.2 | 2288.5 | 4933.0 | 63.2% | — |
| 20.4% | 2379.5 | 2005.2 | 1306.1 | 676.7 | 688.3 | 1396.4 | 65.1% | — |
| 16.4% | 1106.6 | 967.4 | 784.8 | 242.9 | 221.3 | 331.5 | 81.1% | — |
| 13.9% | 649.6 | 569.7 | 483.6 | 115.8 | 107.9 | 139.3 | 84.9% | — |
| 11.4% | 373.4 | 327.2 | 282.0 | 55.0 | 54.1 | 64.8 | 86.2% | — |
| 10.4% | 300.5 | 263.1 | 227.4 | 41.1 | 41.6 | 49.2 | 86.4% | — |
| 8.4% | 186.0 | 162.6 | 140.9 | 21.3 | 23.3 | 27.8 | 86.6% | — |
| 5.9% | 101.9 | 88.9 | 77.0 | 8.2 | 10.9 | 14.1 | 86.7% | — |
| 0.4% | 23.2 | 22.5 | 19.4 | -0.0 | 0.4 | 3.1 | 86.3% | — |

*Net(α=0.1)/Net(α=1) shown only where Net < 0 (refund scenario, negative g). '—' at positive g where both Net values are positive.*

## C.10 2006 Historical Return Series — Reference Scenario Results

**Source:** p['returns'] rotated to 2007 start year (RATES Balanced worst-case reference scenario).  N = 29 holding periods + sell year.  $V_0$ = £20m, $	au_0$ = 15%, $	au_m$ = 70%, k = 0.001.  No beta/signalling adjustment applied.

**Purpose:** Locates the RATES worst-case scenario within the analytical space characterised by C.1–C.9. The 2006 series includes the 2008 crash and subsequent recovery; the realised mean growth rate across N=29 periods is below the 10.45% hist_mean used in C.1–C.9, so results here represent a harder test than the constant-g tables.

### C.10a — Declaration strategy comparison (α sweep, N = 29)

*Realised mean g across N=29 periods: 5.64% (varies by N; this figure is for Part A's N=29).*

| α | TW (£m) | TTP (£m) | Net (£m) | Eff rate | TW vs honest | Net vs honest |
|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| **0.1** | 73.62 | 13.46 | 13.42 | 18.23% | -12.84% | +30.64% |
| **0.2** | 74.83 | 13.11 | 13.04 | 17.43% | -11.41% | +26.95% |
| **0.5** | 78.45 | 12.13 | 11.95 | 15.23% | -7.12% | +16.30% |
| **0.8** | 82.07 | 11.22 | 10.92 | 13.31% | -2.84% | +6.30% |
| **1.0** | 84.47 | 10.64 | 10.27 | 12.16% | +0.00% | +0.00% ← honest |
| **1.2** | 86.86 | 11.40 | 9.66 | 11.12% | +2.83% | -6.01% |
| **1.5** | 90.44 | 14.38 | 8.79 | 9.71% | +7.07% | -14.49% |
| **1.8** | 94.01 | 17.42 | 7.98 | 8.49% | +11.29% | -22.31% |
| **2.0** | 96.37 | 19.48 | 7.48 | 7.77% | +14.10% | -27.15% |

*α = 1.0 row is the honest baseline; TW vs honest and Net vs honest are zero by construction for that row. Positive Net vs honest = understater pays more net tax than honest under the historical series.*

### C.10b — Honest declarer trajectory by N (α = 1.0)

*Each row uses p['returns'][:N] as the holding-period series and p['returns'][N] as the sell-year rate. g_mean is the arithmetic mean of the N holding-period returns; it shifts as more years of the 2006 series are included, most notably around N=3 (2008 crash enters) and N=4 (2009 recovery enters).*

| N | TW (£m) | Net (£m) | Mean g of series[:N] |
|:---:|:---:|:---:|:---:|
| 5 | 24.02 | 0.64 | 3.39% |
| 10 | 33.89 | 2.18 | 5.53% |
| 15 | 36.52 | 2.53 | 4.83% |
| 20 | 46.70 | 4.23 | 4.43% |
| 25 | 67.33 | 7.59 | 5.12% |
| 29 ← RATES ref | 84.47 | 10.27 | 5.64% |
| 30 | 86.25 | 10.38 | 5.82% |

*TW and Net grow with N as additional years of compounding and WDT payments accumulate. The g_mean column makes the path-dependence explicit: unlike C.7/C.8 (constant g throughout), each row here reflects a different prefix of the realised return history.*
