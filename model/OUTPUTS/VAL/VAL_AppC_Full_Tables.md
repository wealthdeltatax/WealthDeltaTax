# C. WDT Valuation Analysis: Summary Tables {.appendix}

**Validation status:** All figures from Python model v1.1 (standalone, no Excel dependency). Parameters unified to $k$ = 0.001, N = 30, $\tau_0$ = 15%. Every table runs at N = 30 explicitly (the SSM LRR fill year, N = 19, is a fund-mechanics quantity and is not used here). 23 automated cross-checks passed at generation (including C.11.4 = C.8 and C.5 = C.8 at N = 30, the C.11 identity, and the in-kind payment identity used by C.12).

Unless otherwise stated, all figures use base parameters: $V_0$ = £20m, N = 30, $\tau_0$ = 15%, $\tau_m$ = 70%, $k$ = 0.001, $W_{min}$ = £2m, $g$ = 10.45%, $\alpha$ = 1, β = 0%.

**Metric convention.** C.1, C.1b and C.12 are all expressed as a fraction of the same denominator, honest terminal net worth TW_settled(1). C.1 (net tax) and C.12 (present value) are positive when the strategy pays more; C.1b (terminal wealth) is positive when the strategy retains more. Net tax is the fiscal view; terminal wealth is the taxpayer's view. Under in-kind settlement they can differ in sign.

## C.1 Net Tax Paid Difference Relative to Honest Declaration, as Share of Honest Terminal Net Worth TW(1)

**Metric:** (Net($\alpha$) − Net(1)) / TW(1). Positive values indicate $\alpha$ pays more net tax than honest; negative values indicate less. Net is Net_settled (including post-sale settlement); TW is TW_settled.

$\frac{Net(\alpha) - Net(1)}{TW(1)}$

**Reading note:** C.1 counts credited pounds. Under Route C settlement in kind, credited liability and the true value surrendered coincide only at $\alpha$ = 1, so a net-tax saving in C.1 does not by itself mean the taxpayer is better off. Read C.1 together with C.1b (terminal wealth) and C.12 (present value of true value surrendered).

| $\alpha$ \ $g$ | -4.5% | 0.4% | 5.9% | 8.4% | 10.4% | 11.4% | 13.9% | 16.4% | 20.4% | 25.4% |
|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| **0.1** | 11.70% | 10.36% | 1.56% | 0.59% | 0.55% | 0.76% | 2.34% | 6.77% | 24.04% | 26.30% |
| **0.2** | 10.33% | 9.21% | 1.34% | 0.44% | 0.34% | 0.49% | 1.69% | 5.11% | 17.90% | 16.71% |
| **0.5** | 6.22% | 5.75% | 0.76% | 0.12% | -0.05% | -0.04% | 0.34% | 1.57% | 5.61% | 3.14% |
| **0.8** | 2.12% | 2.30% | 0.27% | -0.01% | -0.13% | -0.15% | -0.14% | 0.03% | 0.59% | -0.07% |
| **1.0** | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% |
| **1.2** | 0.00% | -1.46% | -0.23% | 0.10% | 0.27% | 0.34% | 0.50% | 0.67% | 0.89% | 0.95% |
| **1.5** | 0.00% | -1.39% | -0.50% | 0.39% | 0.93% | 1.17% | 1.88% | 2.82% | 4.06% | 3.29% |
| **1.8** | 0.00% | -1.33% | -0.67% | 0.87% | 1.91% | 2.41% | 3.97% | 6.10% | 8.63% | 6.26% |
| **2.0** | 0.00% | -1.28% | -0.74% | 1.30% | 2.73% | 3.44% | 5.73% | 8.79% | 12.15% | 8.46% |

Table C.1: Net tax difference relative to honest declaration, as share of honest TW. $\alpha$ = 1.0 row is zero by construction. Positive values indicate pays more net tax. $V_0$ = £20m, $k$ = 0.001, N = 30, $\tau_0$ = 15%, $\tau_m$ = 70%, $W_{min}$ = £2m.

## C.1b Terminal Net Worth Difference Relative to Honest Declaration, as Share of Honest Terminal Net Worth TW(1)

**Metric:** (TW($\alpha$) − TW(1)) / TW(1). Positive values indicate $\alpha$ retains more terminal net worth than honest; negative values indicate less. Same $\alpha$ × $g$ grid and denominator as C.1; opposite sign convention (positive = better off).

$\frac{TW(\alpha) - TW(1)}{TW(1)}$

| $\alpha$ \ $g$ | -4.5% | 0.4% | 5.9% | 8.4% | 10.4% | 11.4% | 13.9% | 16.4% | 20.4% | 25.4% |
|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| **0.1** | -11.70% | -11.85% | -11.40% | -11.24% | -11.19% | -11.21% | -11.64% | -13.54% | -21.26% | 3.55% |
| **0.2** | -10.33% | -10.53% | -10.13% | -9.97% | -9.90% | -9.90% | -10.19% | -11.58% | -16.95% | 1.84% |
| **0.5** | -6.22% | -6.58% | -6.31% | -6.19% | -6.11% | -6.08% | -6.09% | -6.46% | -7.73% | -1.33% |
| **0.8** | -2.12% | -2.63% | -2.52% | -2.46% | -2.41% | -2.39% | -2.33% | -2.32% | -2.34% | -1.09% |
| **1.0** | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% |
| **1.2** | 0.00% | 1.80% | 2.51% | 2.44% | 2.37% | 2.33% | 2.20% | 2.02% | 1.72% | 1.48% |
| **1.5** | 0.00% | 2.24% | 6.25% | 6.06% | 5.85% | 5.72% | 5.28% | 4.61% | 3.61% | 4.10% |
| **1.8** | 0.00% | 2.68% | 9.97% | 9.63% | 9.23% | 9.00% | 8.12% | 6.77% | 4.99% | 6.99% |
| **2.0** | 0.00% | 2.98% | 12.44% | 11.98% | 11.44% | 11.12% | 9.89% | 8.04% | 5.75% | 8.99% |

Table C.1b: Terminal net worth difference relative to honest declaration, as share of honest TW. $\alpha$ = 1.0 row is zero by construction. Positive values indicate retains more. $V_0$ = £20m, $k$ = 0.001, N = 30, $\tau_0$ = 15%, $\tau_m$ = 70%, $W_{min}$ = £2m.

## C.2 Effective Lifetime Tax Rate Difference from Honest Declaration

**Metric:** Net($\alpha$)/TW($\alpha$) − Net(1)/TW(1).

$\frac{Net(\alpha)}{TW(\alpha)} - \frac{Net(1)}{TW(1)}$

| $\alpha$ \ $g$ | -4.5% | 0.4% | 5.9% | 8.4% | 10.4% | 11.4% | 13.9% | 16.4% | 20.4% | 25.4% |
|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| **0.1** | 13.25% | 11.98% | 3.35% | 2.48% | 2.60% | 2.95% | 5.15% | 11.43% | 39.72% | 23.67% |
| **0.2** | 11.52% | 10.49% | 2.88% | 2.08% | 2.12% | 2.36% | 4.04% | 8.79% | 28.51% | 15.50% |
| **0.5** | 6.64% | 6.28% | 1.64% | 1.07% | 0.97% | 1.03% | 1.59% | 3.26% | 8.93% | 3.86% |
| **0.8** | 2.16% | 2.41% | 0.60% | 0.35% | 0.26% | 0.25% | 0.31% | 0.57% | 1.42% | 0.48% |
| **1.0** | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% |
| **1.2** | 0.00% | -1.47% | -0.53% | -0.25% | -0.10% | -0.05% | 0.08% | 0.20% | 0.29% | 0.20% |
| **1.5** | 0.00% | -1.40% | -1.20% | -0.45% | 0.01% | 0.22% | 0.84% | 1.68% | 2.73% | 1.17% |
| **1.8** | 0.00% | -1.34% | -1.73% | -0.46% | 0.41% | 0.84% | 2.25% | 4.25% | 6.60% | 2.56% |
| **2.0** | 0.00% | -1.29% | -2.02% | -0.38% | 0.83% | 1.44% | 3.51% | 6.42% | 9.64% | 3.59% |

Table C.2: Effective lifetime tax rate difference from honest declaration. $\alpha$ = 1.0 row is zero by construction. $V_0$ = £20m, $k$ = 0.001, N = 30, $\tau_0$ = 15%, $\tau_m$ = 70%, $W_{min}$ = £2m.

## C.3 Exploratory Extension: Investor Confidence Effects β (Overstatement Only)

*This section is exploratory. β swept over same values as $g$ columns; $g$ fixed at 10.45%.*

$\frac{Net(\alpha, \beta) - Net(1, \beta=0)}{TW(1, \beta=0)}$

| $\alpha$ \ β | β=-4.5% | β=0.4% | β=5.9% | β=8.4% | β=10.4% | β=11.4% | β=13.9% | β=16.4% | β=20.4% | β=25.4% |
|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| **1.0** | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% |
| **1.2** | -3.17% | 0.65% | 6.08% | 9.12% | 11.92% | 13.33% | 17.38% | 22.11% | 30.95% | 45.04% |
| **1.5** | -6.22% | 1.86% | 18.04% | 29.82% | 42.55% | 49.62% | 72.67% | 104.45% | 176.83% | 318.32% |
| **1.8** | -8.26% | 3.41% | 35.33% | 64.49% | 100.19% | 121.43% | 194.86% | 300.60% | 537.95% | 982.74% |
| **2.0** | -9.30% | 4.64% | 51.13% | 99.12% | 160.58% | 197.56% | 324.50% | 500.86% | 882.38% | 1650.99% |

Table C.3: Investor confidence β sensitivity (overstatement only). Denominator is honest TW(1, β=0) for consistency with C.1. $g$ fixed at 10.45%, N=30 throughout. $V_0$ = £20m, $k$ = 0.001, $\tau_0$ = 15%, $\tau_m$ = 70%, $W_{min}$ = £2m.

## C.4 Effective Lifetime Tax Rate by $k$ Parameter and Initial Wealth ($V_0$)

**Metric:** TTP($\alpha$=1) / TW($\alpha$=1). Rows = k; columns = $V_0$ (£m).

$\frac{TTP(\alpha=1)}{TW(\alpha=1)}$

| $k$ \ $V_0$ | £1m | £10m | £50m | £100m | £250m | £500m | £1000m | £2500m | £5000m | £10000m |
|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| 1e-04 | 13.46% | 14.24% | 14.61% | 15.08% | 16.54% | 19.03% | 24.02% | 36.00% | 46.62% | 54.64% |
| 2e-04 | 13.47% | 14.33% | 15.08% | 16.05% | 19.03% | 24.02% | 32.60% | 46.62% | 54.64% | 58.95% |
| 5e-04 | 13.49% | 14.60% | 16.53% | 19.03% | 26.37% | 35.99% | 46.62% | 56.43% | 59.63% | 60.31% |
| 1e-03 | 13.53% | 15.06% | 19.01% | 24.00% | 35.98% | 46.61% | 54.64% | 59.63% | 60.31% | 60.34% |
| 2e-03 | 13.61% | 16.00% | 23.97% | 32.57% | 46.60% | 54.63% | 58.95% | 60.31% | 60.34% | 60.34% |
| 5e-03 | 13.84% | 18.92% | 35.91% | 46.56% | 56.40% | 59.62% | 60.31% | 60.34% | 60.34% | 60.34% |
| 1e-02 | 14.24% | 23.79% | 46.50% | 54.58% | 59.61% | 60.31% | 60.34% | 60.34% | 60.34% | 60.34% |
| 5e-02 | 17.55% | 46.03% | 59.56% | 60.31% | 60.34% | 60.34% | 60.34% | 60.34% | 60.34% | 60.34% |
| 1e-01 | 21.77% | 53.99% | 60.30% | 60.34% | 60.34% | 60.34% | 60.34% | 60.34% | 60.34% | 60.34% |

Table C.4: Effective lifetime tax rate by $k$ and $V_0$. All at $\alpha$=1, β=0, $g$=10.45%, N=30.

## C.5 Sensitivity of $k$ and Alpha: Terminal Net Worth Difference vs Honest

**Metric:** (TW($\alpha$,k) − TW(1,k) / TW(1,k).

$\frac{TW(\alpha,k) - TW(1,k)}{TW(1,k)}$

| $\alpha$ \ $k$ | 1e-04 | 2e-04 | 5e-04 | 1e-03 | 2e-03 | 5e-03 | 1e-02 | 5e-02 | 1e-01 |
|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| **0.1** | -10.90% | -10.92% | -10.99% | -11.19% | -11.82% | -15.54% | -22.45% | 9.79% | 14.91% |
| **0.2** | -9.68% | -9.70% | -9.75% | -9.90% | -10.38% | -13.18% | -18.04% | 3.28% | 1.69% |
| **0.5** | -6.05% | -6.05% | -6.06% | -6.11% | -6.26% | -7.17% | -8.44% | -3.84% | -7.45% |
| **0.8** | -2.42% | -2.42% | -2.41% | -2.41% | -2.42% | -2.51% | -2.63% | -2.62% | -4.36% |
| **1.0** | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% |
| **1.2** | 2.41% | 2.41% | 2.39% | 2.37% | 2.31% | 2.14% | 2.03% | 3.43% | 5.38% |
| **1.5** | 6.03% | 6.01% | 5.95% | 5.85% | 5.59% | 4.82% | 4.38% | 9.59% | 14.66% |
| **1.8** | 9.64% | 9.60% | 9.48% | 9.23% | 8.66% | 7.03% | 6.24% | 16.60% | 24.81% |
| **2.0** | 12.04% | 11.98% | 11.80% | 11.44% | 10.60% | 8.31% | 7.34% | 21.64% | 31.87% |

Table C.5: TW difference vs honest, by $k$ and $\alpha$. $\alpha$ = 1.0 row is zero by construction. $g$ = 10.45%, N = 30 throughout.

## C.6 Terminal Net Worth After Refunds: Refund Protection Ratio

**Metric:** TW($\alpha$) / TW(1). Negative $g$ scenarios only.

$\frac{TW(\alpha)}{TW(1)}$

| $\alpha$ \ $g$ | -4.5% |
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

Table C.6: Refund protection ratio vs honest declaration. Negative $g$ scenarios only. $\alpha$ = 1.0 is 100% by construction. $V_0$ = £20m, $k$ = 0.001, N = 30, $\tau_0$ = 15%, $\tau_m$ = 70%, $W_{min}$ = £2m.

## C.7 Total Tax Paid Compared to Honest Taxpayer, Adjusted for N

**Metric:** (Net($\alpha$,N) − Net(1,N) / Net(1,N).

$\frac{Net(\alpha,N) - Net(1,N)}{Net(1,N)}$

| $\alpha$ \ N | 5 | 10 | 15 | 20 | 25 | 30 | 35 | 40 | 45 | 50 | 55 | 60 |
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

Table C.7: Net tax compared to honest taxpayer, adjusted for N. $\alpha$ = 1.0 row is zero by construction. $g$ = 10.45% throughout. $V_0$ = £20m, $k$ = 0.001, N = 30, $\tau_0$ = 15%, $\tau_m$ = 70%, $W_{min}$ = £2m.

## C.8 Terminal Net Worth Compared to Honest Taxpayer, Adjusted for N

**Metric:** (TW($\alpha$,N) − TW(1,N) / TW(1,N).

$\frac{TW(\alpha,N) - TW(1,N)}{TW(1,N)}$

| $\alpha$ \ N | 5 | 10 | 15 | 20 | 25 | 30 | 35 | 40 | 45 | 50 | 55 | 60 |
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

Table C.8: TW compared to honest taxpayer, adjusted for N. $\alpha$ = 1.0 row is zero by construction. $g$ = 10.45% throughout. $V_0$ = £20m, $k$ = 0.001, N = 30, $\tau_0$ = 15%, $\tau_m$ = 70%, $W_{min}$ = £2m.

## C.9 Summary of Declaration Incentives Across Growth Regimes

**Metric:** TW(£m) and Net tax (£m) at $\alpha$ ∈ {2.0, 1.0, 0.1} across the $g$ sweep. N = 30 throughout.

| $g$ | TW($\alpha$=2) £m | TW($\alpha$=1) £m | TW($\alpha$=0.1) £m | Net($\alpha$=2) £m | Net($\alpha$=1) £m | Net($\alpha$=0.1) £m | TW(0.1)/TW(1) | Net(0.1)/Net(1) |
|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| 25.4% | 5539.4 | 5082.6 | 5263.2 | 2998.3 | 2568.5 | 3905.4 | 103.6% | — |
| 20.4% | 2448.6 | 2315.4 | 1823.2 | 1069.6 | 788.3 | 1344.8 | 78.7% | — |
| 16.4% | 1184.1 | 1096.0 | 947.6 | 348.2 | 251.9 | 326.1 | 86.5% | — |
| 13.9% | 699.1 | 636.2 | 562.1 | 157.0 | 120.6 | 135.5 | 88.4% | — |
| 11.4% | 399.2 | 359.2 | 319.0 | 71.7 | 59.3 | 62.1 | 88.8% | — |
| 10.4% | 319.7 | 286.9 | 254.8 | 53.1 | 45.3 | 46.9 | 88.8% | — |
| 8.4% | 195.5 | 174.6 | 154.9 | 27.3 | 25.0 | 26.1 | 88.8% | — |
| 5.9% | 105.1 | 93.5 | 82.8 | 10.8 | 11.5 | 13.0 | 88.6% | — |
| 0.4% | 23.2 | 22.6 | 19.9 | 0.1 | 0.4 | 2.7 | 88.2% | — |

Table C.9: Summary of declaration incentives across growth regimes. TW and Net tax in £m. N = 30 throughout. $V_0$ = £20m, $k$ = 0.001, N = 30, $\tau_0$ = 15%, $\tau_m$ = 70%, $W_{min}$ = £2m.

## C.10 Historical Return Series — Reference Scenario Results

**Source:** RATES Balanced worst-case reference scenario (returns rotated to 2000 start year). $V_0$ = £20m, $\tau_0$ = 15%, $\tau_m$ = 70%, $k$ = 0.001, $W_{min}$ = £2m. No β adjustment applied.

### C.10.1 Declaration strategy comparison ($\alpha$ sweep, N = 30)

| $\alpha$ | TW (£m) | TTP (£m) | Net (£m) | Eff rate | TW vs honest | Net vs honest |
|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| **0.1** | 78.82 | 14.14 | 12.29 | 15.59% | -11.79% | +13.13% |
| **0.2** | 80.00 | 13.81 | 12.09 | 15.11% | -10.47% | +11.32% |
| **0.5** | 83.53 | 12.89 | 11.56 | 13.84% | -6.53% | +6.40% |
| **0.8** | 87.04 | 12.05 | 11.11 | 12.77% | -2.60% | +2.29% |
| **1.0** | 89.36 | 11.55 | 10.86 | 12.16% | +0.00% | +0.00% ← honest |
| **1.2** | 91.68 | 13.79 | 10.65 | 11.62% | +2.59% | -1.94% |
| **1.5** | 95.14 | 17.41 | 10.41 | 10.94% | +6.46% | -4.17% |
| **1.8** | 98.57 | 21.11 | 10.25 | 10.40% | +10.31% | -5.59% |
| **2.0** | 100.85 | 23.62 | 10.20 | 10.11% | +12.86% | -6.10% |

Table C.10.1: Declaration strategy comparison, 2000 historical return series, N = 30.

### C.10.2 Honest declarer trajectory by N ($\alpha$ = 1.0)

| N | TW (£m) | Net (£m) | Mean $g$ of series[:N] |
|:---:|:---:|:---:|:---:|
| 5 | 33.18 | 2.02 | 9.89% |
| 10 | 40.90 | 3.21 | 7.77% |
| 15 | 52.35 | 4.99 | 7.42% |
| 20 | 65.99 | 7.13 | 7.14% |
| 25 | 69.46 | 7.68 | 6.01% |
| **30** | **89.36** | **10.86** | **5.99%** |

Table C.10.2: Honest declarer trajectory under 2000 historical return series. The N = 30 row equals the honest row of C.10.1 (asserted at generation).

## C.11 Overstater TW Advantage Decomposition

**Purpose:** Identifies the three mechanical sources of the overstater TW advantage shown in C.8. For each ($\alpha$, $g$) cell the TW advantage relative to honest declaration is split into: (1) excess periodic net tax paid during the holding period, (2) the sell-year settlement delta, and (3) the post-sale oscillation delta. These three terms sum to the C.8 figure (sign-adjusted). An additional sub-table shows $f_N$ — the retained equity fraction at end of holding period — as a ratio to the honest declarer's $f_N$, quantifying the dilution cost of overstatement.

**Identity (corrected):** TW_settled($\alpha$) $-$ TW_settled(1) $=$ W_sell_delta $-$ RefundDelta $-$ SettleDelta  (verified to machine precision across all tested $(\alpha, g)$ pairs).  W_sell_delta $\leq 0$: f_N erosion reduces sell-year proceeds.  RefundDelta $\leq 0$: overstater receives a larger sell-year refund.  SettleDelta $\geq 0$: post-sale oscillation taxes back part of the refund.  Note: ExcessPeriodic (holding-period net tax difference) is **not** additive in this identity — it feeds into TW_advantage indirectly through f_N erosion and is shown in C.11.1 for reference only.

**Scope:** Overstaters only ($\alpha$ ≥ 1.0). All values at canonical N = 30, $k$ = 0.001, $V_0$ = £20m. Rows = $\alpha$; columns = $g$ (same grid as C.1). Sub-tables C.11.1–C.11.4 expressed as % of TW_settled(1); C.11.5 is dimensionless.

### C.11.1 — W_sell_delta as % of Honest TW_settled  [Additive Term 1]

**Formula:** (W_sell($\alpha$) $-$ W_sell(1)) / TW_settled(1)  $\leq 0$ for $\alpha > 1$.  W_sell $= f_N \times V_{sell}$; the overstater's f_N is depleted faster by higher periodic tax, reducing the sell-year declared value.  This is the f_N erosion cost of overstatement: the overstater owns a smaller fraction of the asset at sale.  Note: ExcessPeriodic (holding-period net tax difference) is related but **not** equal to W_sell_delta — the excess periodic tax is approximately 6× larger than |W_sell_delta| at canonical parameters because most of the excess is returned via the sell-year refund (C.11.2).  ExcessPeriodic is shown separately in C.11.6 for reference.

| $\alpha$ \ $g$ | -4.5% | 0.4% | 5.9% | 8.4% | 10.4% | 11.4% | 13.9% | 16.4% | 20.4% | 25.4% |
|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| **1.0** | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% |
| **1.2** | 0.00% | -0.01% | -0.15% | -0.32% | -0.56% | -0.72% | -1.35% | -2.42% | -4.69% | -5.98% |
| **1.5** | 0.00% | -0.01% | -0.38% | -0.80% | -1.40% | -1.79% | -3.33% | -5.86% | -10.59% | -12.87% |
| **1.8** | 0.00% | -0.02% | -0.60% | -1.28% | -2.23% | -2.85% | -5.26% | -9.04% | -15.42% | -18.15% |
| **2.0** | 0.00% | -0.03% | -0.75% | -1.59% | -2.78% | -3.56% | -6.51% | -11.01% | -18.19% | -21.07% |

Table C.11.1: W_sell_delta as % of honest TW_settled (additive term 1). Always $\leq 0$ for $\alpha > 1$: f_N erosion reduces sell-year proceeds. $V_0$ = £20m, $k$ = 0.001, N = 30.

*Always $\leq 0$ for $\alpha > 1$: the overstater surrenders more equity as periodic tax, depressing the sell-year declared value.  The magnitude grows with both $\alpha$ and $g$ but is much smaller than the refund benefit (C.11.2) — this is why the net TW advantage (C.11.4) remains positive across the tested range.*

### C.11.2 — Sell-Year Settlement Delta as % of Honest TW_settled

**Formula:** ($L_{sell}$($\alpha$) $-$ $L_{sell}$(1)) / TW_settled(1)  · Negative = overstater receives a larger refund (or smaller tax) at sale. The declared basis at sale always exceeds true proceeds for $\alpha$ > 1 at any finite $g$, generating a refund that partially offsets the periodic cost.

| $\alpha$ \ $g$ | -4.5% | 0.4% | 5.9% | 8.4% | 10.4% | 11.4% | 13.9% | 16.4% | 20.4% | 25.4% |
|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| **1.0** | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% |
| **1.2** | 0.00% | -2.08% | -3.09% | -3.23% | -3.48% | -3.65% | -4.40% | -5.85% | -9.67% | -12.51% |
| **1.5** | 0.00% | -2.59% | -7.70% | -8.04% | -8.61% | -9.01% | -10.71% | -13.87% | -21.88% | -28.74% |
| **1.8** | 0.00% | -3.11% | -12.29% | -12.79% | -13.64% | -14.24% | -16.70% | -21.10% | -32.06% | -42.83% |
| **2.0** | 0.00% | -3.46% | -15.34% | -15.94% | -16.95% | -17.65% | -20.52% | -25.54% | -38.00% | -51.34% |

Table C.11.2: Sell-year settlement delta as % of honest TW_settled. Negative = overstater received a larger refund at sale. $V_0$ = £20m, $k$ = 0.001, N = 30.

*Negative throughout (refund benefit) for all $\alpha$ > 1. Magnitude grows with $\alpha$ but is bounded by the lifetime cap. At high $g$ the honest declarer also pays a large sell-year tax, compressing the relative benefit.*

### C.11.3 — Post-Sale Settlement Delta as % of Honest TW_settled

**Formula:** (net_settle_tax($\alpha$) $-$ net_settle_tax(1)) / TW_settled(1)  · Positive = the post-sale oscillation taxes back more of the overstater's sell-year refund than it does for the honest declarer. This is the damping cost: a larger sell-year refund creates a larger positive delta in the first post-sale period, which is taxed back.

| $\alpha$ \ $g$ | -4.5% | 0.4% | 5.9% | 8.4% | 10.4% | 11.4% | 13.9% | 16.4% | 20.4% | 25.4% |
|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| **1.0** | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% |
| **1.2** | 0.00% | 0.28% | 0.43% | 0.47% | 0.55% | 0.60% | 0.85% | 1.40% | 3.26% | 5.06% |
| **1.5** | 0.00% | 0.34% | 1.07% | 1.18% | 1.37% | 1.50% | 2.10% | 3.40% | 7.69% | 11.77% |
| **1.8** | 0.00% | 0.41% | 1.72% | 1.89% | 2.18% | 2.39% | 3.32% | 5.29% | 11.64% | 17.69% |
| **2.0** | 0.00% | 0.46% | 2.15% | 2.37% | 2.72% | 2.98% | 4.11% | 6.49% | 14.06% | 21.28% |

Table C.11.3: Post-sale settlement delta as % of honest TW_settled. Positive = oscillation recovered more from overstater's refund. $V_0$ = £20m, $k$ = 0.001, N = 30.

*Positive throughout for $\alpha$ > 1: the settle_tw() oscillation always recovers some of the sell-year refund via subsequent tax. The damping cost is smaller than the refund benefit (C.11.2) in all tested cases — the net refund position remains favourable.*

### C.11.4 — Total TW Advantage as % of Honest TW_settled (Cross-Check)

**Formula:** (TW_settled($\alpha$) $-$ TW_settled(1)) / TW_settled(1)  · Should equal C.8 at the canonical N column. Values here are computed from the full decomposition and serve as an internal consistency check on C.11.1–C.11.3.

| $\alpha$ \ $g$ | -4.5% | 0.4% | 5.9% | 8.4% | 10.4% | 11.4% | 13.9% | 16.4% | 20.4% | 25.4% |
|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| **1.0** | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% |
| **1.2** | 0.00% | 1.80% | 2.51% | 2.44% | 2.37% | 2.33% | 2.20% | 2.02% | 1.72% | 1.48% |
| **1.5** | 0.00% | 2.24% | 6.25% | 6.06% | 5.85% | 5.72% | 5.28% | 4.61% | 3.61% | 4.10% |
| **1.8** | 0.00% | 2.68% | 9.97% | 9.63% | 9.23% | 9.00% | 8.12% | 6.77% | 4.99% | 6.99% |
| **2.0** | 0.00% | 2.98% | 12.44% | 11.98% | 11.44% | 11.12% | 9.89% | 8.04% | 5.75% | 8.99% |

Table C.11.4: Total TW advantage as % of honest TW_settled. Should match C.5 (at canonical $k$) and C.8 (at canonical N) for each $\alpha$. $V_0$ = £20m, $k$ = 0.001, N = 30.

*Should match C.5 (at canonical $k$) and C.8 (at canonical N) for each $\alpha$. Any discrepancy exceeding 0.01pp indicates a decomposition error. This equality is now asserted by the val_core validation harness (C11.4_equals_C8, C5_equals_C8).*

### C.11.5 — Retained Equity Fraction Ratio at End of Holding Period

**Formula:** $f_N$($\alpha$) / $f_N$(1)  · Values below 1.0 indicate the overstater has surrendered more equity as tax during the holding period. This is the dilution cost: the overstater owns a smaller fraction of their asset at sale, which is why the sell-year declared value ($f_N \times V_{sell}$) is lower than it would otherwise be.

| $\alpha$ \ $g$ | -4.5% | 0.4% | 5.9% | 8.4% | 10.4% | 11.4% | 13.9% | 16.4% | 20.4% | 25.4% |
|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| **1.0** | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 |
| **1.2** | 1.0000 | 0.9999 | 0.9985 | 0.9968 | 0.9945 | 0.9929 | 0.9868 | 0.9764 | 0.9551 | 0.9433 |
| **1.5** | 1.0000 | 0.9999 | 0.9963 | 0.9921 | 0.9862 | 0.9824 | 0.9673 | 0.9430 | 0.8985 | 0.8780 |
| **1.8** | 1.0000 | 0.9998 | 0.9940 | 0.9874 | 0.9780 | 0.9719 | 0.9484 | 0.9121 | 0.8522 | 0.8279 |
| **2.0** | 1.0000 | 0.9997 | 0.9925 | 0.9842 | 0.9725 | 0.9649 | 0.9361 | 0.8929 | 0.8257 | 0.8003 |

Table C.11.5: Retained equity fraction ratio $f_N$($\alpha$) / $f_N$(1). Values below 1.0 = overstater surrendered more equity during holding period. $V_0$ = £20m, $k$ = 0.001, N = 30.

### C.11.6 — Excess Periodic Net Tax as % of Honest TW_settled  [Informational]

**Formula:** (Net_holding($\alpha$) $-$ Net_holding(1)) / TW_settled(1)  · Positive = overstater paid more net tax during the holding period.  **This term is NOT additive in the C.11 identity** — it is shown for reference only.

| $\alpha$ \ $g$ | -4.5% | 0.4% | 5.9% | 8.4% | 10.4% | 11.4% | 13.9% | 16.4% | 20.4% | 25.4% |
|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| **1.0** | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% |
| **1.2** | 0.00% | 0.34% | 2.43% | 2.85% | 3.20% | 3.38% | 4.05% | 5.12% | 7.30% | 8.40% |
| **1.5** | 0.00% | 0.86% | 6.13% | 7.25% | 8.18% | 8.69% | 10.50% | 13.29% | 18.25% | 20.26% |
| **1.8** | 0.00% | 1.38% | 9.90% | 11.77% | 13.37% | 14.26% | 17.36% | 21.91% | 29.04% | 31.41% |
| **2.0** | 0.00% | 1.73% | 12.45% | 14.87% | 16.95% | 18.11% | 22.14% | 27.83% | 36.09% | 38.51% |

Table C.11.6: Excess periodic net tax as % of honest TW_settled (informational). $V_0$ = £20m, $k$ = 0.001, N = 30.

## C.12 Present-Value Tax Position: PV of True Value Surrendered, Difference vs Honest

**Purpose:** Adjusts the C.1 net-tax metric for the time value of money, valuing every payment at the true value the taxpayer actually surrenders. Under Route C the holding-period liability $L_t$ is settled in kind at the declared price; the true value of the equity transferred is $L_t/\alpha$, so a payment credited at $L_t$ costs an understater ($\alpha < 1$) more than $L_t$ and an overstater ($\alpha > 1$) less. Sell-year and post-sale flows are cash at true prices ($\alpha$ drops out at liquidation).

**Metric:** $(PV_{true}(\alpha) - PV_{true}(1))$ / TW_settled(1), where $PV_{true}(\alpha) = \sum_{t=1}^{N} \frac{L_t/\alpha}{(1+\rho)^t} + \frac{L_{sell}}{(1+\rho)^{N+1}} + \sum_{i \geq 1} \frac{L^{post}_i}{(1+\rho)^{N+1+i}}$ and $\rho = 5\%$.

$\frac{PV_{true}(\alpha) - PV_{true}(1)}{TW_{settled}(1)}$

**Sign convention:** Positive = alpha pays more in present-value terms than honest. Negative = alpha pays less. Same sign and same denominator as C.1, so the tables are directly comparable; C.1b gives the terminal-wealth view of the same grid (opposite sign: positive = retains more).

**Superseded version:** the pre-refactor C.12 discounted the credited liability $L_t$ rather than $L_t/\alpha$ and omitted post-sale settlement flows. That version mis-valued in-kind payments for $\alpha \neq 1$ (it showed an understater deferral gain at moderate growth that the terminal-wealth results do not). It is retained in val_data.json as `c12_declared_legacy` for audit only.

**Scope:** Full α grid (same as C.1). All values at canonical N = 30, $k$ = 0.001, $V_0$ = £20m, $\rho$ = 5%, $\tau_0$ = 15%, $\tau_m$ = 70%.

| $\alpha$ \ $g$ | -4.5% | 0.4% | 5.9% | 8.4% | 10.4% | 11.4% | 13.9% | 16.4% | 20.4% | 25.4% |
|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| **0.1** | 2.59% | 2.62% | 2.55% | 2.59% | 2.69% | 2.78% | 3.23% | 4.35% | 8.65% | 11.02% |
| **0.2** | 2.29% | 2.33% | 2.26% | 2.29% | 2.39% | 2.46% | 2.83% | 3.76% | 7.22% | 9.39% |
| **0.5** | 1.38% | 1.46% | 1.41% | 1.43% | 1.47% | 1.51% | 1.71% | 2.17% | 3.78% | 5.29% |
| **0.8** | 0.47% | 0.58% | 0.56% | 0.57% | 0.58% | 0.60% | 0.66% | 0.81% | 1.30% | 1.93% |
| **1.0** | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% |
| **1.2** | 0.00% | -0.40% | -0.56% | -0.56% | -0.57% | -0.58% | -0.63% | -0.74% | -1.10% | -1.73% |
| **1.5** | 0.00% | -0.49% | -1.40% | -1.40% | -1.42% | -1.43% | -1.53% | -1.73% | -2.49% | -4.05% |
| **1.8** | 0.00% | -0.59% | -2.23% | -2.22% | -2.24% | -2.26% | -2.36% | -2.61% | -3.66% | -6.10% |
| **2.0** | 0.00% | -0.65% | -2.78% | -2.76% | -2.78% | -2.79% | -2.89% | -3.15% | -4.35% | -7.36% |

Table C.12: PV of true value surrendered, difference vs honest declaration, as % of honest TW_settled. $\alpha$ = 1.0 row is zero by construction. $\rho$ = 5%, $V_0$ = £20m, $k$ = 0.001, N = 30, $\tau_0$ = 15%, $\tau_m$ = 70%, $W_{min}$ = £2m.

## C.12b Discount-Rate Sweep and the State Tolerance Zone

**Metric:** as C.12 (PV of true value surrendered, difference vs honest, fraction of TW(1)), evaluated at several discount rates $\rho$ from a single simulation per $(\alpha, g)$. Positive = the state receives more present value than from an honest declarer; negative = the state receives less. The state is taken to be unconcerned where the difference lies within $\pm$2 percentage points of TW(1) (the tolerance zone).

**g = 5.9%**

| $\alpha$ \ $\rho$ | 0% | 2% | 3% | 4% | 5% | 6% | 7% | 8% | 9% | 10% | 12% |
|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| **0.1** | 11.72% | 6.32% | 4.66% | 3.44% | 2.55% | 1.89% | 1.40% | 1.04% | 0.78% | 0.58% | 0.32% |
| **0.2** | 10.40% | 5.61% | 4.13% | 3.05% | 2.26% | 1.68% | 1.24% | 0.93% | 0.69% | 0.51% | 0.28% |
| **0.5** | 6.48% | 3.50% | 2.58% | 1.90% | 1.41% | 1.04% | 0.78% | 0.58% | 0.43% | 0.32% | 0.18% |
| **0.8** | 2.59% | 1.39% | 1.03% | 0.76% | 0.56% | 0.42% | 0.31% | 0.23% | 0.17% | 0.13% | 0.07% |
| **1.0** | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% |
| **1.2** | -2.58% | -1.39% | -1.02% | -0.76% | -0.56% | -0.42% | -0.31% | -0.23% | -0.17% | -0.13% | -0.07% |
| **1.5** | -6.42% | -3.46% | -2.55% | -1.89% | -1.40% | -1.03% | -0.77% | -0.57% | -0.42% | -0.32% | -0.17% |
| **1.8** | -10.25% | -5.53% | -4.07% | -3.01% | -2.23% | -1.65% | -1.23% | -0.91% | -0.68% | -0.50% | -0.28% |
| **2.0** | -12.79% | -6.89% | -5.08% | -3.75% | -2.78% | -2.06% | -1.53% | -1.14% | -0.85% | -0.63% | -0.35% |

**g = 10.4%**

| $\alpha$ \ $\rho$ | 0% | 2% | 3% | 4% | 5% | 6% | 7% | 8% | 9% | 10% | 12% |
|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| **0.1** | 12.58% | 6.75% | 4.96% | 3.65% | 2.69% | 1.99% | 1.47% | 1.09% | 0.81% | 0.60% | 0.33% |
| **0.2** | 11.14% | 5.98% | 4.39% | 3.23% | 2.39% | 1.76% | 1.30% | 0.96% | 0.71% | 0.53% | 0.29% |
| **0.5** | 6.88% | 3.69% | 2.71% | 2.00% | 1.47% | 1.09% | 0.80% | 0.60% | 0.44% | 0.33% | 0.18% |
| **0.8** | 2.72% | 1.46% | 1.07% | 0.79% | 0.58% | 0.43% | 0.32% | 0.24% | 0.17% | 0.13% | 0.07% |
| **1.0** | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% |
| **1.2** | -2.68% | -1.44% | -1.06% | -0.78% | -0.57% | -0.42% | -0.31% | -0.23% | -0.17% | -0.13% | -0.07% |
| **1.5** | -6.62% | -3.55% | -2.61% | -1.92% | -1.42% | -1.05% | -0.77% | -0.57% | -0.42% | -0.31% | -0.17% |
| **1.8** | -10.48% | -5.62% | -4.12% | -3.04% | -2.24% | -1.65% | -1.22% | -0.90% | -0.67% | -0.49% | -0.27% |
| **2.0** | -13.00% | -6.97% | -5.12% | -3.77% | -2.78% | -2.05% | -1.51% | -1.12% | -0.83% | -0.61% | -0.33% |

**g = 20.4%**

| $\alpha$ \ $\rho$ | 0% | 2% | 3% | 4% | 5% | 6% | 7% | 8% | 9% | 10% | 12% |
|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| **0.1** | 41.29% | 21.96% | 16.06% | 11.78% | 8.65% | 6.36% | 4.69% | 3.46% | 2.55% | 1.89% | 1.03% |
| **0.2** | 34.51% | 18.34% | 13.42% | 9.83% | 7.22% | 5.31% | 3.91% | 2.88% | 2.12% | 1.57% | 0.85% |
| **0.5** | 18.12% | 9.62% | 7.03% | 5.15% | 3.78% | 2.77% | 2.04% | 1.50% | 1.10% | 0.81% | 0.44% |
| **0.8** | 6.23% | 3.31% | 2.42% | 1.77% | 1.30% | 0.95% | 0.70% | 0.51% | 0.38% | 0.28% | 0.15% |
| **1.0** | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% |
| **1.2** | -5.28% | -2.81% | -2.05% | -1.50% | -1.10% | -0.81% | -0.59% | -0.44% | -0.32% | -0.23% | -0.13% |
| **1.5** | -11.93% | -6.34% | -4.64% | -3.40% | -2.49% | -1.83% | -1.34% | -0.98% | -0.72% | -0.53% | -0.28% |
| **1.8** | -17.49% | -9.31% | -6.81% | -4.99% | -3.66% | -2.68% | -1.97% | -1.45% | -1.06% | -0.78% | -0.42% |
| **2.0** | -20.76% | -11.06% | -8.09% | -5.93% | -4.35% | -3.19% | -2.34% | -1.72% | -1.27% | -0.93% | -0.50% |

Table C.12b: PV of true value surrendered, difference vs honest declaration, as % of honest TW_settled, by discount rate, at g = 5.9%, 10.4%, 20.4%. $V_0$ = £20m, $k$ = 0.001, N = 30.

### C.12b.1 Share of overstatement outside the tolerance zone

| $\rho$ | $\alpha \leq$ 2: cells costing the state > 2pp | $\alpha \leq$ 2: worst shortfall | $\alpha \leq$ 5: cells costing the state > 2pp | $\alpha \leq$ 5: worst shortfall |
|:---:|:---:|:---:|:---:|:---:|
| 0% | 84% | -30.62pp | 92% | -87.67pp |
| 2% | 69% | -16.59pp | 86% | -47.85pp |
| 3% | 60% | -12.26pp | 82% | -35.49pp |
| 4% | 47% | -9.07pp | 76% | -26.38pp |
| 5% | 32% | -6.73pp | 69% | -19.65pp |
| 6% | 13% | -5.00pp | 61% | -14.66pp |
| 7% | 6% | -3.72pp | 51% | -10.97pp |
| 8% | 2% | -2.77pp | 39% | -8.21pp |
| 9% | 0% | -2.07pp | 25% | -6.16pp |
| 10% | 0% | -1.54pp | 10% | -4.63pp |
| 12% | 0% | -0.86pp | 1% | -2.62pp |

Table C.12b.1: Overstatement grid on a log-spaced $\alpha$ axis (1, 5], g from 0 to 25% in steps of 0.5%, N = 30. Shares are shares of grid cells, so they depend on the grid; the breakeven rates in C.12b.3 do not.

### C.12b.2 State revenue at the declarer's terminal-wealth-maximising declaration

| $\rho$ | PV vs honest at $g$ = hist. mean | Worst PV (g ≤ 25%) | Worst PV (all g) |
|:---:|:---:|:---:|:---:|
| 0% | -46.56pp | -87.67pp | -113.12pp |
| 2% | -24.94pp | -47.85pp | -62.78pp |
| 3% | -18.31pp | -35.49pp | -47.00pp |
| 4% | -13.46pp | -26.38pp | -35.30pp |
| 5% | -9.92pp | -19.65pp | -26.60pp |
| 6% | -7.31pp | -14.66pp | -20.10pp |
| 7% | -5.40pp | -10.97pp | -15.24pp |
| 8% | -3.99pp | -8.21pp | -11.59pp |
| 9% | -2.95pp | -6.16pp | -8.84pp |
| 10% | -2.17pp | -4.63pp | -6.76pp |
| 12% | -1.18pp | -2.62pp | -3.99pp |

Table C.12b.2: At each g the declarer picks $\alpha^*$ in [0.1, 5] to maximise TW. $\alpha^*$ = 5.0 (the grid maximum) at 80 of 80 positive-growth grid points: in this model terminal wealth keeps rising with $\alpha$ (TW advantage +40.40% at the historical mean g), so no interior optimum exists and the limit on overstatement must come from outside the model.

### C.12b.3 Breakeven discount rate

| $\alpha$ | g = 5.0% | g = 10.0% | g = 20.0% | g = 30.0% |
|:---:|:---:|:---:|:---:|:---:|
| **1.2** | 0.8% | 0.9% | 2.9% | 5.2% |
| **1.5** | 3.8% | 3.8% | 5.5% | 8.2% |
| **2.0** | 6.1% | 6.1% | 7.3% | 10.3% |
| **3.0** | 8.4% | 8.3% | 9.0% | 12.3% |
| **5.0** | 10.7% | 10.3% | 10.4% | 14.1% |

Table C.12b.3: Discount rate $\rho^*$ at which the state's PV shortfall from overstatement at $\alpha$ equals 2pp of TW(1). For $\rho > \rho^*$ the state is within the tolerance zone. Solved by bisection; N = 30. At g = 10% (nearest 1% grid point to the historical mean), $\rho^*$ rises from 0.9% ($\alpha$ = 1.2) to 10.3% ($\alpha$ = 5.0).

## C.13 Declaration Under Uncertainty

**Design.** In C.1–C.12 the declaration is a fixed multiple $\alpha$ of the true value in every year, which implicitly assumes the taxpayer knows $V_t$. Here the taxpayer targets a declaration level $m$ but the market reveals the true value, so the realised ratio $\alpha_t = D_t / V_t$ is an outcome, not a choice. Annual returns are lognormal with the historical mean growth rate and volatility $\sigma$; every comparison is paired with an honest declarer on the same return path (1000 paths per $\sigma$, N = 30). Two declaration rules: *committed* ($D_t = m V_0 (1+g)^t$, no market feedback) and *anchored* ($D_t = m V_{t-1}(1+g)$, re-declared on the previous year's observed value). At $\sigma$ = 0 both reduce exactly to the constant-$\alpha$ results of C.1–C.12. State shortfall is the PV of true value received, vs honest, at $\rho$ = 5%, in percentage points of honest TW; the state is outside its tolerance zone when the shortfall exceeds 2pp.

### C.13.1 Committed path

| $\sigma$ | Metric | m = 0.81 | m = 1.00 | m = 1.18 | m = 1.53 | m = 1.97 | m = 3.01 | m = 5.00 |
|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| **0** | E[TW gap] | -2.3% | +0.0% | +2.2% | +6.2% | +11.1% | +22.0% | +40.5% |
|  | 5th pct TW gap | -2.3% | +0.0% | +2.2% | +6.2% | +11.1% | +22.0% | +40.5% |
|  | P(TW gain) | 0% | 0% | 100% | 100% | 100% | 100% | 100% |
|  | P(realised $\alpha_N$ > 1) | 0% | 100% | 100% | 100% | 100% | 100% | 100% |
|  | P(state short > 2pp) | 0% | 0% | 0% | 0% | 100% | 100% | 100% |
| **8.3%** | E[TW gap] | -2.6% | +0.1% | +2.6% | +7.3% | +13.1% | +25.9% | +47.7% |
|  | 5th pct TW gap | -3.8% | -1.3% | +0.8% | +4.0% | +7.3% | +13.8% | +24.5% |
|  | P(TW gain) | 4% | 35% | 100% | 100% | 100% | 100% | 100% |
|  | P(realised $\alpha_N$ > 1) | 40% | 58% | 74% | 89% | 96% | 100% | 100% |
|  | P(state short > 2pp) | 0% | 3% | 14% | 44% | 75% | 98% | 100% |
| **15.0%** | E[TW gap] | -1.3% | +2.5% | +6.1% | +12.7% | +21.0% | +39.4% | +71.0% |
|  | 5th pct TW gap | -6.2% | -3.9% | -1.8% | +1.3% | +4.5% | +10.3% | +18.3% |
|  | P(TW gain) | 19% | 38% | 70% | 99% | 100% | 100% | 100% |
|  | P(realised $\alpha_N$ > 1) | 54% | 64% | 72% | 82% | 89% | 96% | 99% |
|  | P(state short > 2pp) | 11% | 24% | 36% | 57% | 73% | 92% | 98% |
| **25.0%** | E[TW gap] | +17.4% | +27.2% | +36.7% | +54.0% | +75.7% | +121.5% | +204.5% |
|  | 5th pct TW gap | -12.6% | -10.2% | -8.1% | -4.7% | -1.3% | +4.3% | +12.2% |
|  | P(TW gain) | 39% | 49% | 59% | 74% | 90% | 99% | 100% |
|  | P(realised $\alpha_N$ > 1) | 70% | 74% | 77% | 84% | 90% | 94% | 97% |
|  | P(state short > 2pp) | 40% | 51% | 60% | 71% | 80% | 91% | 96% |

Table C.13.1: Committed path declaration, N = 30, g = 10.45%. TW gap = (TW(declarer) − TW(honest)) / TW(honest) on the same path. The declarer's best $m$ on this grid (maximum 5) by mean TW gain is 5, 5, 5, 5 and by 5th-percentile TW gain 5, 5, 5, 5 for $\sigma$ = 0, 8.3%, 15.0%, 25.0%. Means at high $\sigma$ are dominated by the upper tail and should be read alongside the percentiles.

### C.13.2 Anchored

| $\sigma$ | Metric | m = 0.81 | m = 1.00 | m = 1.18 | m = 1.53 | m = 1.97 | m = 3.01 | m = 5.00 |
|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| **0** | E[TW gap] | -2.3% | +0.0% | +2.2% | +6.2% | +11.1% | +22.0% | +40.5% |
|  | 5th pct TW gap | -2.3% | +0.0% | +2.2% | +6.2% | +11.1% | +22.0% | +40.5% |
|  | P(TW gain) | 0% | 0% | 100% | 100% | 100% | 100% | 100% |
|  | P(realised $\alpha_N$ > 1) | 0% | 0% | 100% | 100% | 100% | 100% | 100% |
|  | P(state short > 2pp) | 0% | 0% | 0% | 0% | 100% | 100% | 100% |
| **8.3%** | E[TW gap] | -2.2% | +0.1% | +2.3% | +6.3% | +11.2% | +22.2% | +40.9% |
|  | 5th pct TW gap | -2.6% | -0.1% | +1.9% | +5.3% | +9.4% | +18.2% | +31.8% |
|  | P(TW gain) | 0% | 52% | 100% | 100% | 100% | 100% | 100% |
|  | P(realised $\alpha_N$ > 1) | 1% | 51% | 99% | 100% | 100% | 100% | 100% |
|  | P(state short > 2pp) | 0% | 0% | 0% | 0% | 100% | 100% | 100% |
| **15.0%** | E[TW gap] | -1.9% | +0.4% | +2.6% | +6.7% | +11.7% | +22.7% | +41.7% |
|  | 5th pct TW gap | -2.8% | -0.3% | +1.7% | +4.7% | +8.3% | +15.2% | +25.1% |
|  | P(TW gain) | 1% | 63% | 100% | 100% | 100% | 100% | 100% |
|  | P(realised $\alpha_N$ > 1) | 9% | 52% | 88% | 100% | 100% | 100% | 100% |
|  | P(state short > 2pp) | 0% | 0% | 0% | 14% | 92% | 100% | 100% |
| **25.0%** | E[TW gap] | -1.6% | +0.8% | +3.1% | +7.2% | +12.2% | +23.2% | +42.6% |
|  | 5th pct TW gap | -3.2% | -0.8% | +1.0% | +3.6% | +6.1% | +9.9% | +17.3% |
|  | P(TW gain) | 8% | 75% | 99% | 100% | 100% | 100% | 100% |
|  | P(realised $\alpha_N$ > 1) | 26% | 56% | 79% | 97% | 100% | 100% | 100% |
|  | P(state short > 2pp) | 7% | 9% | 15% | 37% | 72% | 93% | 97% |

Table C.13.2: Anchored declaration, N = 30, g = 10.45%. TW gap = (TW(declarer) − TW(honest)) / TW(honest) on the same path. The declarer's best $m$ on this grid (maximum 5) by mean TW gain is 5, 5, 5, 5 and by 5th-percentile TW gain 5, 5, 5, 5 for $\sigma$ = 0, 8.3%, 15.0%, 25.0%. Means at high $\sigma$ are dominated by the upper tail and should be read alongside the percentiles.
