# VAL.A Appendix C — Full Simulation Tables

**Generated:** 2026-08-29  
**Model version:** Python v1.0 (standalone, no Excel dependency)  
**Parameters:** $V_0$ = £20m · $	au_0$ = 15% · $	au_m$ = 70% · k = 0.001 · W_min = £2m · N = 29 · g = 10.45%  
**Validation status:** 0 FAILs across all primary matrices (confirmed against Excel 27 July 2026). All metrics updated to TW_settled / Net_settled (post-sale settlement correction; see wdt_core.py §settle_tw).  
**N-offset:** Tables C.7/C.8 show actual simulation N; Excel displayed N-5 in column headers — corrected here.  
**Beta formula:** Additive g_eff = g + β·ln(α); VAL.A §B.3 shows multiplicative form — that section requires update.  
**Table C.4 note:** Max 2.67% deviation from Excel (known snapshot issue); Python values used throughout.  

## C.1 Total Tax Paid Difference Relative to Honest Declaration, as Share of Terminal Net Worth

**Formula:** (Net_settled(α) − Net_settled(1)) / TW_settled(α)  ·  Positive = α pays more than honest; negative = pays less.

| α \ g | -4.5% | 0.4% | 5.9% | 8.4% | 10.4% | 11.4% | 13.9% | 16.4% | 20.4% | 25.4% |
|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| **0.1** | 13.25% | 11.80% | 1.91% | 0.73% | 0.58% | 0.74% | 2.15% | 6.22% | 25.65% | 30.18% |
| **0.2** | 11.52% | 10.34% | 1.63% | 0.55% | 0.36% | 0.47% | 1.51% | 4.58% | 18.39% | 19.84% |
| **0.5** | 6.64% | 6.18% | 0.90% | 0.18% | -0.04% | -0.05% | 0.24% | 1.29% | 5.38% | 4.33% |
| **0.8** | 2.16% | 2.37% | 0.31% | 0.01% | -0.12% | -0.15% | -0.15% | -0.02% | 0.55% | 0.14% |
| **1.0** | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% |
| **1.2** | 0.00% | -1.39% | -0.26% | 0.06% | 0.23% | 0.30% | 0.45% | 0.61% | 0.83% | 0.90% |
| **1.5** | 0.00% | -1.32% | -0.56% | 0.29% | 0.79% | 1.01% | 1.63% | 2.45% | 3.76% | 3.31% |
| **1.8** | 0.00% | -1.25% | -0.75% | 0.66% | 1.58% | 2.00% | 3.33% | 5.18% | 7.96% | 6.33% |
| **2.0** | 0.00% | -1.21% | -0.83% | 0.97% | 2.21% | 2.81% | 4.72% | 7.39% | 11.19% | 8.50% |

*Base parameters. α = 1.0 row is zero by construction. Positive values indicate understater pays more lifetime tax.*

## C.2 Effective Lifetime Tax Rate Difference from Honest Declaration

**Formula:** Net_settled(α)/TW_settled(α) − Net_settled(1)/TW_settled(1)  ·  Positive = α has higher effective rate than honest.

| α \ g | -4.5% | 0.4% | 5.9% | 8.4% | 10.4% | 11.4% | 13.9% | 16.4% | 20.4% | 25.4% |
|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| **0.1** | 13.25% | 12.03% | 3.47% | 2.52% | 2.53% | 2.78% | 4.53% | 9.45% | 33.61% | 32.53% |
| **0.2** | 11.52% | 10.53% | 2.99% | 2.12% | 2.06% | 2.24% | 3.57% | 7.31% | 24.52% | 21.68% |
| **0.5** | 6.64% | 6.30% | 1.71% | 1.11% | 0.97% | 1.00% | 1.43% | 2.76% | 8.01% | 5.71% |
| **0.8** | 2.16% | 2.42% | 0.63% | 0.37% | 0.27% | 0.25% | 0.29% | 0.50% | 1.32% | 0.79% |
| **1.0** | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% |
| **1.2** | 0.00% | -1.42% | -0.56% | -0.27% | -0.13% | -0.07% | 0.05% | 0.17% | 0.27% | 0.19% |
| **1.5** | 0.00% | -1.36% | -1.27% | -0.52% | -0.07% | 0.13% | 0.69% | 1.45% | 2.62% | 1.49% |
| **1.8** | 0.00% | -1.30% | -1.85% | -0.59% | 0.25% | 0.66% | 1.92% | 3.73% | 6.41% | 3.40% |
| **2.0** | 0.00% | -1.25% | -2.18% | -0.55% | 0.61% | 1.17% | 3.03% | 5.68% | 9.43% | 4.84% |

*VAL.A §C.2 describes this as 'effective lifetime tax rate from terminal wealth' but the formula is a difference relative to honest. Label in VAL.A §C.2 heading requires correction.*

## C.3 Exploratory Extension: Investor Confidence Effects β (Overstatement Only)

**Formula:** (Net_settled(α,β) − Net_settled(1,β=0)) / TW_settled(α,β)  ·  β swept over same numeric values as g columns; g fixed at 10.45%.
**Beta formula:** g_eff = g + β·ln(α) [additive — confirmed from Excel; VAL.A §B.3 states multiplicative form incorrectly].
**Scope:** Overstatement only (α ≥ 1.0). Understater cells omitted — analytical scope for signalling is overstatement.

| α \ β | β=-4.5% | β=0.4% | β=5.9% | β=8.4% | β=10.4% | β=11.4% | β=13.9% | β=16.4% | β=20.4% | β=25.4% |
|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| **1.0** | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% |
| **1.2** | -3.61% | 0.58% | 4.38% | 5.92% | 7.10% | 7.63% | 8.96% | 10.25% | 12.19% | 14.51% |
| **1.5** | -8.77% | 1.56% | 9.26% | 12.19% | 14.47% | 15.53% | 18.33% | 21.33% | 26.47% | 33.54% |
| **1.8** | -13.78% | 2.70% | 13.78% | 18.31% | 22.20% | 24.09% | 29.37% | 34.99% | 43.15% | 50.41% |
| **2.0** | -17.08% | 3.56% | 17.07% | 23.08% | 28.41% | 31.00% | 37.86% | 44.14% | 50.64% | 56.02% |

*Exploratory only. No empirical calibration for β exists. Sign convention: positive = α pays more than honest. Deviations increase at high α×β due to exponential compounding over N=34.*

## C.4 Effective Lifetime Tax Rate by k Parameter and Initial Wealth ($V_0$)

**Formula:** TTP(α=1) / TW_settled(α=1)  ·  Honest declaration throughout. TTP is a holding-period quantity; denominator is settled TW. Rows = k; columns = $V_0$ (£m).
**Note:** Max 2.67% deviation from Excel (known snapshot — Excel AppC cells computed at different params state). Python values used.

| k \ $V_0$ | £1m | £10m | £50m | £100m | £250m | £500m | £1000m | £2500m | £5000m | £10000m |
|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| 1e-04 | 13.31% | 14.14% | 14.48% | 14.91% | 16.24% | 18.52% | 23.10% | 34.54% | 45.24% | 53.62% |
| 2e-04 | 13.31% | 14.22% | 14.91% | 15.79% | 18.51% | 23.10% | 31.23% | 45.24% | 53.62% | 58.19% |
| 5e-04 | 13.33% | 14.47% | 16.23% | 18.51% | 25.30% | 34.54% | 45.24% | 55.50% | 58.90% | 59.62% |
| 1e-03 | 13.37% | 14.89% | 18.49% | 23.08% | 34.53% | 45.23% | 53.61% | 58.90% | 59.62% | 59.65% |
| 2e-03 | 13.44% | 15.75% | 23.06% | 31.19% | 45.22% | 53.61% | 58.18% | 59.62% | 59.65% | 59.65% |
| 5e-03 | 13.65% | 18.40% | 34.45% | 45.18% | 55.48% | 58.89% | 59.62% | 59.65% | 59.65% | 59.65% |
| 1e-02 | 14.00% | 22.87% | 45.12% | 53.55% | 58.88% | 59.62% | 59.65% | 59.65% | 59.65% | 59.65% |
| 5e-02 | 16.94% | 44.62% | 58.83% | 59.62% | 59.65% | 59.65% | 59.65% | 59.65% | 59.65% | 59.65% |
| 1e-01 | 20.73% | 52.92% | 59.61% | 59.65% | 59.65% | 59.65% | 59.65% | 59.65% | 59.65% | 59.65% |

*All at α=1, β=0, g=10.45%, N=34. k values above 0.001 are analytically extreme; included for completeness.*

## C.5 Sensitivity of k and Alpha: Terminal Net Worth Difference vs Honest

**Formula:** (TW_settled(α,k) − TW_settled(1,k)) / TW_settled(1,k)  ·  Positive = α retains more settled TW than honest; negative = less.

| α \ k | 1e-04 | 2e-04 | 5e-04 | 1e-03 | 2e-03 | 5e-03 | 1e-02 | 5e-02 | 1e-01 |
|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| **0.1** | -10.90% | -10.92% | -10.99% | -11.16% | -11.71% | -14.95% | -21.77% | 7.32% | 13.88% |
| **0.2** | -9.68% | -9.70% | -9.75% | -9.88% | -10.30% | -12.75% | -17.62% | 2.02% | 1.44% |
| **0.5** | -6.05% | -6.05% | -6.06% | -6.10% | -6.24% | -7.05% | -8.41% | -4.04% | -7.46% |
| **0.8** | -2.42% | -2.42% | -2.41% | -2.41% | -2.42% | -2.51% | -2.65% | -2.64% | -4.36% |
| **1.0** | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% |
| **1.2** | 2.41% | 2.41% | 2.40% | 2.38% | 2.33% | 2.18% | 2.06% | 3.43% | 5.38% |
| **1.5** | 6.03% | 6.02% | 5.97% | 5.87% | 5.65% | 4.95% | 4.44% | 9.56% | 14.66% |
| **1.8** | 9.64% | 9.61% | 9.50% | 9.29% | 8.79% | 7.27% | 6.33% | 16.54% | 24.81% |
| **2.0** | 12.04% | 12.00% | 11.84% | 11.52% | 10.78% | 8.63% | 7.43% | 21.56% | 31.87% |

*α = 1.0 row is zero by construction. g = 10.45%, N = 34 throughout.*

## C.6 Terminal Net Worth After Refunds: Refund Protection Ratio

**Formula:** TW_settled(α) / TW_settled(1)  ·  Values below 100% = reduced settled TW relative to honest. Negative g scenarios only.

| α \ g | -4.5% |
|:---:|:---:|
| **0.1** | 88.30% |
| **0.2** | 89.67% |
| **0.5** | 93.78% |
| **0.8** | 97.88% |
| **1.0** | 100.00% |
| **1.2** | 100.00% |
| **1.5** | 100.00% |
| **1.8** | 100.00% |
| **2.0** | 100.00% |

*Negative g scenarios only. α = 1.0 is 100% by construction. Understater protection loss proportional to basis gap at entry.*

## C.7 Total Tax Paid Compared to Honest Taxpayer, Adjusted for N

**Formula:** (Net_settled(α,N) − Net_settled(1,N)) / Net_settled(1,N)  ·  Positive = α pays more net tax than honest.
**N correction:** Values shown are actual simulation N (5 to 60). Excel headers showed N-5 (0 to 55) — corrected here.

| α \ N | 5 | 10 | 15 | 20 | 25 | 30 | 35 | 40 | 45 | 50 | 55 | 60 |
|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| **0.1** | 105.67% | 40.00% | 17.61% | 7.86% | 3.85% | 3.47% | 6.25% | 12.68% | 24.00% | 41.38% | 61.99% | 73.51% |
| **0.2** | 93.79% | 35.35% | 15.38% | 6.58% | 2.82% | 2.18% | 4.16% | 9.08% | 17.77% | 30.87% | 45.68% | 52.60% |
| **0.5** | 58.35% | 21.72% | 9.08% | 3.35% | 0.64% | -0.34% | 0.01% | 1.63% | 4.68% | 9.05% | 13.24% | 13.86% |
| **0.8** | 23.23% | 8.54% | 3.42% | 1.03% | -0.20% | -0.81% | -1.02% | -0.91% | -0.51% | 0.10% | 0.61% | 0.54% |
| **1.0** | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% |
| **1.2** | -23.09% | -8.34% | -3.14% | -0.62% | 0.80% | 1.70% | 2.36% | 2.90% | 3.37% | 3.70% | 3.78% | 3.52% |
| **1.5** | -57.45% | -20.46% | -7.31% | -0.79% | 3.11% | 5.92% | 8.35% | 10.77% | 13.14% | 14.90% | 15.17% | 13.55% |
| **1.8** | -80.00% | -32.13% | -10.84% | -0.05% | 6.77% | 12.10% | 17.17% | 22.52% | 27.73% | 31.18% | 31.05% | 26.97% |
| **2.0** | -77.69% | -39.66% | -12.84% | 0.96% | 9.95% | 17.29% | 24.57% | 32.33% | 39.69% | 44.12% | 43.25% | 37.04% |

*g = 10.45% throughout. α = 1.0 row is zero by construction. Understater penalty at N=5 reflects large realisation delta on short horizon.*

## C.8 Terminal Net Worth Compared to Honest Taxpayer, Adjusted for N

**Formula:** (TW_settled(α,N) − TW_settled(1,N)) / TW_settled(1,N)  ·  Negative = α retains less settled TW than honest.
**N correction:** As C.7 — actual N shown.

| α \ N | 5 | 10 | 15 | 20 | 25 | 30 | 35 | 40 | 45 | 50 | 55 | 60 |
|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| **0.1** | -11.03% | -11.04% | -11.04% | -11.06% | -11.09% | -11.19% | -11.41% | -11.96% | -13.26% | -16.04% | -20.30% | -21.96% |
| **0.2** | -9.81% | -9.81% | -9.81% | -9.82% | -9.84% | -9.90% | -10.06% | -10.46% | -11.41% | -13.43% | -16.37% | -17.09% |
| **0.5** | -6.13% | -6.12% | -6.12% | -6.11% | -6.10% | -6.11% | -6.13% | -6.23% | -6.49% | -7.04% | -7.71% | -7.43% |
| **0.8** | -2.45% | -2.45% | -2.44% | -2.43% | -2.42% | -2.41% | -2.39% | -2.38% | -2.37% | -2.39% | -2.39% | -2.23% |
| **1.0** | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% |
| **1.2** | 2.45% | 2.44% | 2.43% | 2.42% | 2.40% | 2.37% | 2.32% | 2.24% | 2.12% | 1.96% | 1.79% | 1.69% |
| **1.5** | 6.12% | 6.10% | 6.07% | 6.03% | 5.96% | 5.85% | 5.66% | 5.35% | 4.90% | 4.30% | 3.77% | 3.62% |
| **1.8** | 9.07% | 9.75% | 9.70% | 9.61% | 9.47% | 9.23% | 8.84% | 8.22% | 7.28% | 6.15% | 5.22% | 5.15% |
| **2.0** | 9.97% | 12.18% | 12.10% | 11.98% | 11.78% | 11.44% | 10.89% | 9.99% | 8.70% | 7.18% | 6.01% | 6.04% |

*g = 10.45% throughout. α = 1.0 row is zero by construction.*

## C.9 Summary of Declaration Incentives Across Growth Regimes

**Columns:** TW(£m) and Net tax (£m) at α∈{2.0, 1.0, 0.1}; ratios vs honest. N = 34 throughout.

| g | TW_s(α=2) £m | TW_s(α=1) £m | TW_s(α=0.1) £m | Net_s(α=2) £m | Net_s(α=1) £m | Net_s(α=0.1) £m | TW_s(0.1)/TW_s(1) | Net_s(0.1)/Net_s(1) |
|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| 25.4% | 4801.4 | 4435.8 | 4229.0 | 2535.4 | 2127.4 | 3403.9 | 95.3% | — |
| 20.4% | 2165.3 | 2045.0 | 1634.7 | 890.9 | 648.5 | 1067.8 | 79.9% | — |
| 16.4% | 1057.6 | 975.0 | 849.7 | 291.9 | 213.7 | 266.6 | 87.1% | — |
| 13.9% | 630.3 | 572.2 | 506.6 | 135.1 | 105.4 | 116.3 | 88.5% | — |
| 11.4% | 364.9 | 328.1 | 291.4 | 63.4 | 53.2 | 55.4 | 88.8% | — |
| 10.4% | 294.1 | 263.7 | 234.3 | 47.5 | 41.0 | 42.3 | 88.8% | — |
| 8.4% | 182.5 | 162.9 | 144.6 | 24.8 | 23.0 | 24.1 | 88.8% | — |
| 5.9% | 100.1 | 89.0 | 78.8 | 10.0 | 10.8 | 12.3 | 88.6% | — |
| 0.4% | 23.1 | 22.5 | 19.8 | 0.1 | 0.4 | 2.7 | 88.2% | — |

*Net_s = Net_settled; TW_s = TW_settled. Net_s(α=0.1)/Net_s(α=1) shown only where Net_settled < 0 (refund scenario, negative g). '—' at positive g where both Net_settled values are positive.*

## C.10 2006 Historical Return Series — Reference Scenario Results

**Source:** p['returns'] rotated to 2007 start year (RATES Balanced worst-case reference scenario).  N = 29 holding periods + sell year.  $V_0$ = £20m, $	au_0$ = 15%, $	au_m$ = 70%, k = 0.001.  No beta/signalling adjustment applied.

**Purpose:** Locates the RATES worst-case scenario within the analytical space characterised by C.1–C.9. The 2006 series includes the 2008 crash and subsequent recovery; the realised mean growth rate across N=29 periods is below the 10.45% hist_mean used in C.1–C.9, so results here represent a harder test than the constant-g tables.

### C.10a — Declaration strategy comparison (α sweep, N = 29)

*Realised mean g across N=29 periods: 5.64% (varies by N; this figure is for Part A's N=29).*

| α | TW (£m) | TTP (£m) | Net (£m) | Eff rate | TW vs honest | Net vs honest |
|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| **0.1** | 75.33 | 13.46 | 11.70 | 15.54% | -10.99% | +15.81% |
| **0.2** | 76.37 | 13.11 | 11.50 | 15.05% | -9.76% | +13.75% |
| **0.5** | 79.48 | 12.13 | 10.92 | 13.74% | -6.08% | +8.04% |
| **0.8** | 82.58 | 11.22 | 10.41 | 12.61% | -2.43% | +2.99% |
| **1.0** | 84.63 | 10.64 | 10.11 | 11.94% | +0.00% | +0.00% ← honest |
| **1.2** | 86.68 | 11.40 | 9.83 | 11.35% | +2.42% | -2.70% |
| **1.5** | 89.74 | 14.38 | 9.48 | 10.57% | +6.04% | -6.18% |
| **1.8** | 92.79 | 17.42 | 9.20 | 9.91% | +9.64% | -8.99% |
| **2.0** | 94.81 | 19.48 | 9.05 | 9.54% | +12.03% | -10.49% |

*α = 1.0 row is the honest baseline; TW vs honest and Net vs honest are zero by construction for that row. Positive Net vs honest = understater pays more net tax than honest under the historical series.*

### C.10b — Honest declarer trajectory by N (α = 1.0)

*Each row uses p['returns'][:N] as the holding-period series and p['returns'][N] as the sell-year rate. g_mean is the arithmetic mean of the N holding-period returns; it shifts as more years of the 2006 series are included, most notably around N=3 (2008 crash enters) and N=4 (2009 recovery enters).*

| N | TW (£m) | Net (£m) | Mean g of series[:N] |
|:---:|:---:|:---:|:---:|
| 5 | 24.05 | 0.62 | 3.39% |
| 10 | 33.94 | 2.13 | 5.53% |
| 15 | 36.52 | 2.53 | 4.83% |
| 20 | 46.80 | 4.13 | 4.43% |
| 25 | 67.54 | 7.38 | 5.12% |
| 29 ← RATES ref | 84.63 | 10.11 | 5.64% |
| 30 | 86.26 | 10.37 | 5.82% |

*TW and Net grow with N as additional years of compounding and WDT payments accumulate. The g_mean column makes the path-dependence explicit: unlike C.7/C.8 (constant g throughout), each row here reflects a different prefix of the realised return history.*
