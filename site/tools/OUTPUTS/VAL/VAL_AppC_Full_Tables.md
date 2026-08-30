# C. WDT Valuation Analysis: Summary Tables {.appendix}

**Validation status:** All figures in this section are from Python model v1.0 (standalone, no Excel dependency), confirmed 0 FAILs across all primary matrices. Parameters unified to $k$ = 0.001, N = 29, $\tau_0$ = 15% across all companion papers. Table C.3 carries deviations up to 13% at extreme $\alpha$×β values (threshold 15%; 0 FAILs); see (VAL.A §C.3) note.

Unless otherwise stated, all figures use base parameters: $V_0$ = £20m, N = 29, $\tau_0$ = 15%, $\tau_m$ = 70%, $k$ = 0.001, $W_{min}$ = £2m, $g$ = 10.45%, $\alpha$ = 1, β = 0%. These are the Balanced transition scenario parameters from (RATES).

## C.1 Total Tax Paid (TTP) Difference Relative to Honest Declaration, as Share of Terminal Net Worth (TW)

**Metric:** (Net($\alpha$) − Net(1) / TW($\alpha$). Positive values indicate $\alpha$ pays more net tax than honest; negative values indicate less.

$\frac{Net(\alpha) - Net(1)}{TW(\alpha)}$

**Structural claim:** Understatement is more costly than honest declaration across the policy-relevant growth range. The penalty escalates steeply between $g$ ≈ 10% and $g$ ≈ 17.3%, then plateaus at a ceiling set by $\alpha$; the marginal deterrent stops escalating but does not reverse. The plateau inflection at $g$ ≈ 17.3% is a rate-function property that is approximately constant across all $\alpha$ and N-invariant above the plateau — simulation confirms that the plateau shape at N = 29 and N = 50 are visually identical (SWEEPS §2.3, Fig S3.1b). The C.1 metric for $\alpha$ = 0.1 exceeds 100% at approximately $g$ = 23–24% — the understater's excess tax exceeds their terminal wealth — but this is a normalisation artefact (the denominator, the understater's own TW, compresses at high growth), not a sign reversal in the penalty. For mild overstatement ($\alpha$ ≤ 1.5), overstatement produces a tax saving at moderate positive growth, with no reversal within the tested range at canonical parameters. For aggressive overstatement ($\alpha$ ≥ 1.8), the saving reverses in the $g$ ≈ 9–17% corridor containing the historical mean and recovers only above $g$ ≈ 17%; the self-limiting mechanism also operates temporally through the N-crossing described in §A.5.4. In negative growth scenarios the refund cap binds for understaters, reducing their net-tax advantage.

| $\alpha$ \ $g$ | -4.5% | 0.4% | 5.9% | 8.4% | 10.4% | 11.4% | 13.9% | 16.4% | 20.4% | 25.4% |
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

Table C.1: TTP difference relative to honest declaration, as share of TW. $\alpha$ = 1.0 row is zero by construction. Positive values indicate understater pays more lifetime tax. $V_0$ = £20m, $k$ = 0.001, N = 29, $\tau_0$ = 15%, $\tau_m$ = 70%, $W_{min}$ = £2m.

## C.2 Effective Lifetime Tax Rate Difference from Honest Declaration

**Metric:** Net($\alpha$)/TW($\alpha$) − Net(1)/TW(1). Positive values indicate $\alpha$ has a higher effective lifetime rate than the honest declarer.

$\frac{Net(\alpha)}{TW(\alpha)} - \frac{Net(1)}{TW(1)}$

**Structural claim:** Effective lifetime tax rate differences are directionally consistent with C.1 but larger in magnitude, because the formula normalises by TW($\alpha$) and TW(1) separately rather than by a common denominator. Understaters face materially higher effective rates than honest declarers across all tested growth rates; overstaters face lower rates at moderate growth. The differential is largest at low and high growth extremes, reflecting refund protection loss and saturation effects respectively.

| $\alpha$ \ $g$ | -4.5% | 0.4% | 5.9% | 8.4% | 10.4% | 11.4% | 13.9% | 16.4% | 20.4% | 25.4% |
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

Table C.2: Effective lifetime tax rate difference from honest declaration. $\alpha$ = 1.0 row is zero by construction. $V_0$ = £20m, $k$ = 0.001, N = 29, $\tau_0$ = 15%, $\tau_m$ = 70%, $W_{min}$ = £2m.

*Note: this table measures the difference in effective lifetime tax rate relative to honest declaration, not an absolute rate.*

## C.3 Exploratory Extension: Investor Confidence Effects β (Overstatement Only)

*This section is exploratory and not required for the operation of WDT. The beta mechanism is not empirically calibrated. Results are sensitivity testing, not prediction.*

**Metric:** (Net($\alpha$,β) − Net(1,β=0) / TW($\alpha$,β). β swept over the same numeric values as the $g$ columns in C.1/C.2; $g$ fixed at 10.45%.

$\frac{Net(\alpha, \beta) - Net(1, \beta=0)}{TW(\alpha, \beta)}$

**Structural claim:** β represents the sensitivity of true asset growth to declared valuation via $g_{eff} = g + \beta \cdot \ln(\alpha)$ (see (VAL.A §B.2.1) and (VAL.A §B.2.2). A positive β partially offsets the declaration cost where overstatement contributes to confidence formation. Scope is overstatement only ($\alpha$ ≥ 1.0); understater cells are omitted. Deviations at high $\alpha$×β values (up to 13%) reflect exponential compounding of g_eff over N = 29; directional claims are unaffected. No empirical calibration for β exists.

| $\alpha$ \ β | β=-4.5% | β=0.4% | β=5.9% | β=8.4% | β=10.4% | β=11.4% | β=13.9% | β=16.4% | β=20.4% | β=25.4% |
|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| **1.0** | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% |
| **1.2** | -3.61% | 0.58% | 4.38% | 5.92% | 7.10% | 7.63% | 8.96% | 10.25% | 12.19% | 14.51% |
| **1.5** | -8.77% | 1.56% | 9.26% | 12.19% | 14.47% | 15.53% | 18.33% | 21.33% | 26.47% | 33.54% |
| **1.8** | -13.78% | 2.70% | 13.78% | 18.31% | 22.20% | 24.09% | 29.37% | 34.99% | 43.15% | 50.41% |
| **2.0** | -17.08% | 3.56% | 17.07% | 23.08% | 28.41% | 31.00% | 37.86% | 44.14% | 50.64% | 56.02% |

Table C.3: Investor confidence β sensitivity (overstatement only). Sign convention: positive = $\alpha$ pays more than honest. β column values are the same numeric sweep as $g$ in C.1/C.2; $g$ fixed at 10.45%, N=29 throughout. Deviations increase at high $\alpha$×β due to exponential compounding; max deviation vs Excel 13% (threshold 15%; 0 FAILs). $V_0$ = £20m, $k$ = 0.001, $\tau_0$ = 15%, $\tau_m$ = 70%, $W_{min}$ = £2m.

## C.4 Effective Lifetime Tax Rate by $k$ Parameter and Initial Wealth ($V_0$)

**Metric:** TTP($\alpha$=1) / TW($\alpha$=1). Honest declaration throughout. Rows = k; columns = $V_0$ (£m).

$\frac{TTP(\alpha=1)}{TW(\alpha=1)}$

**Structural claim:** The S-curve rate function produces an effective lifetime rate that is low at small $V_0$ and rises toward $\tau_m$ at very large $V_0$ × high $k$ combinations. The policy-relevant $k$ range is approximately 1e-04 to 1e-03; values above 5e-03 are analytically extreme and included for completeness only. The rate ceiling of approximately 60.67% reflects the logistic bound at $\tau_m$ = 70% over N = 29 years.

| $k$ \ $V_0$ | £1m | £10m | £50m | £100m | £250m | £500m | £1000m | £2500m | £5000m | £10000m |
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

Table C.4: Effective lifetime tax rate by $k$ and $V_0$. All at $\alpha$=1, β=0, $g$=10.45%, N=29. $k$ values above 1e-03 are analytically extreme; included for completeness.

## C.5 Sensitivity of $k$ and Alpha: Terminal Net Worth Difference vs Honest

**Metric:** (TW($\alpha$,k) − TW(1,k) / TW(1,k). Positive values indicate $\alpha$ retains more terminal net worth than honest; negative values indicate less.

$\frac{TW(\alpha,k) - TW(1,k)}{TW(1,k)}$

**Structural claim:** TW differences are directionally consistent across the tested $k$ range. Understater penalties scale with $k$ up to the logistic saturation boundary, beyond which further increases have diminishing effect. The overstater advantage follows the same pattern, accelerating at high $k$ ($k$ ≥ 1e-02) as the rate function's bracket ascent steepens. $k$ values above 1e-03 are analytically extreme.

| $\alpha$ \ $k$ | 1e-04 | 2e-04 | 5e-04 | 1e-03 | 2e-03 | 5e-03 | 1e-02 | 5e-02 | 1e-01 |
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

Table C.5: TW difference vs honest, by $k$ and $\alpha$. $\alpha$ = 1.0 row is zero by construction. $g$ = 10.45%, N = 29 throughout.

## C.6 Terminal Net Worth After Refunds: Refund Protection Ratio

**Metric:** TW($\alpha$) / TW(1). Values below 100% indicate reduced TW relative to honest. Negative $g$ scenarios only.

$\frac{TW(\alpha)}{TW(1)}$

**Structural claim:** Understaters receive materially reduced terminal wealth in negative growth scenarios because the refund is calculated on the declared basis, not the true value. The protection loss is determined almost entirely by the entry declaration and is stable across negative growth rates for each $\alpha$ — the ratio at $g$ = −4.5% characterises the full negative-$g$ regime. Overstaters show 100% throughout: the lifetime cap prevents refunds exceeding prior contributions, which in a purely negative growth environment are zero for all strategies.

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

Table C.6: Refund protection ratio vs honest declaration. Negative $g$ scenarios only. $\alpha$ = 1.0 is 100% by construction. Understater protection loss proportional to basis gap at entry. $V_0$ = £20m, $k$ = 0.001, N = 29, $\tau_0$ = 15%, $\tau_m$ = 70%, $W_{min}$ = £2m.

## C.7 Total Tax Paid Compared to Honest Taxpayer, Adjusted for N

**Metric:** (Net($\alpha$,N) − Net(1,N) / Net(1,N). Positive values indicate $\alpha$ pays more net tax than honest. N values shown are actual simulation N (5 to 60). Earlier Excel display showed N-5 in column headers; corrected here.

$\frac{Net(\alpha,N) - Net(1,N)}{Net(1,N)}$

**Structural claim:** Understatement imposes a persistent and substantial net-tax penalty across all holding periods tested. The penalty is largest at short horizons (N = 5) where the basis gap recovery dominates a small total tax base, and compresses as the holding period extends. For overstatement, the initial advantage narrows and can reverse at extended horizons where the honest declarer has accumulated more basis history. Understater N = 5 penalties above 100% reflect the realisation delta dominating a near-zero prior-year contribution.

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

Table C.7: Net tax compared to honest taxpayer, adjusted for N. $\alpha$ = 1.0 row is zero by construction. $g$ = 10.45% throughout. $V_0$ = £20m, $k$ = 0.001, $\tau_0$ = 15%, $\tau_m$ = 70%, $W_{min}$ = £2m.

## C.8 Terminal Net Worth Compared to Honest Taxpayer, Adjusted for N

**Metric:** (TW($\alpha$,N) − TW(1,N) / TW(1,N). Negative values indicate $\alpha$ retains less TW than honest. N correction as C.7 — actual N shown.

$\frac{TW(\alpha,N) - TW(1,N)}{TW(1,N)}$

**Structural claim:** TW differences widen materially as N rises — the basis gap compounds into more pronounced divergence at $k$ = 0.001 than at lower k. The understater penalty at $\alpha$ = 0.1 grows from −12.76% at N = 5 to −41.99% at N = 60. Overstater advantages widen on the same trajectory. No convergence toward zero occurs within realistic holding periods at $g$ = 10.45%.

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

Table C.8: TW compared to honest taxpayer, adjusted for N. $\alpha$ = 1.0 row is zero by construction. $g$ = 10.45% throughout. $V_0$ = £20m, $k$ = 0.001, $\tau_0$ = 15%, $\tau_m$ = 70%, $W_{min}$ = £2m.

## C.9 Summary of Declaration Incentives Across Growth Regimes

**Metric:** TW(£m) and Net tax (£m) at $\alpha$ ∈ {2.0, 1.0, 0.1} across the $g$ sweep; ratios vs honest. N = 29 throughout.

**Structural claim:** The mechanism's fundamental properties hold across the full tested growth range. Understatement consistently costs more than honest declaration in absolute net-tax terms at every positive $g$ tested. The understater penalty escalates steeply between $g$ ≈ 10% and $g$ ≈ 17.3%, then plateaus — the rate ceiling stops further escalation but does not reverse it. The plateau ceiling scales with the degree of understatement: $\alpha$ = 0.1 plateaus near 98% of true wealth, $\alpha$ = 0.2 near 70%, $\alpha$ = 0.5 near 24%, $\alpha$ = 0.8 near 6%. The inflection at $g$ ≈ 17.3% is a rate-function property, approximately constant across all $\alpha$ and N-invariant above the plateau (see §A.5.4 and SWEEPS §2.3, Fig S3.1b). For overstaters, this table captures the contemporaneous growth-corridor effect for aggressive overstatement; the temporal N-crossing correction operates across holding periods and is documented in §C.8 and SWEEPS.A §A.4. The TW(0.1)/TW(1) ratio declines from approximately 86–87% at moderate growth to 63.2% at $g$ = 25.4%, reflecting compounding basis gap effects consistent with the penalty plateau. The C.1 metric exceeding 100% at $g$ = 25.4% for $\alpha$ = 0.1 is a normalisation artefact: it means the excess tax exceeds the understater's terminal wealth, not that the penalty reverses.

| $g$ | TW($\alpha$=2) £m | TW($\alpha$=1) £m | TW($\alpha$=0.1) £m | Net($\alpha$=2) £m | Net($\alpha$=1) £m | Net($\alpha$=0.1) £m | TW(0.1)/TW(1) | Net(0.1)/Net(1) |
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

Table C.9: Summary of declaration incentives across growth regimes. TW and Net tax in £m. N = 29 throughout. Net($\alpha$=0.1)/Net($\alpha$=1) shown only where Net < 0 (refund scenario, negative $g$); '—' at positive $g$ where both Net values are positive. $V_0$ = £20m, $k$ = 0.001, N = 29, $\tau_0$ = 15%, $\tau_m$ = 70%, $W_{min}$ = £2m.

## C.10 2006 Historical Return Series — Reference Scenario Results

**Source:** RATES Balanced worst-case reference scenario (p['returns'] rotated to 2007 start year). $V_0$ = £20m, $\tau_0$ = 15%, $\tau_m$ = 70%, $k$ = 0.001, $W_{min}$ = £2m. No β adjustment applied.

**Purpose:** Locates the RATES worst-case scenario within the analytical space of C.1–C.9. The 2006 series includes the 2008 crash and subsequent recovery. The realised mean growth rate across N = 29 periods is 5.64%, below the 10.45% historical mean used in C.1–C.9; results here represent a harder test than the constant-$g$ tables.

### C.10.1 Declaration strategy comparison ($\alpha$ sweep, N = 29)

Each row uses p['returns'][:N] as the holding-period series and p['returns'][N] as the sell-year rate. The g_mean column is the arithmetic mean of the N holding-period returns.

| $\alpha$ | TW (£m) | TTP (£m) | Net (£m) | Eff rate | TW vs honest | Net vs honest |
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

Table C.10.1: Declaration strategy comparison, 2006 historical return series, N = 29. $\alpha$ = 1.0 row is the honest baseline; TW vs honest and Net vs honest are zero by construction. Positive Net vs honest = understater pays more net tax than honest under the historical series.

### C.10.2 Honest declarer trajectory by N ($\alpha$ = 1.0)

Each row uses p['returns'][:N] as the holding-period series and p['returns'][N] as the sell-year rate. The g_mean column is the arithmetic mean of the N holding-period returns; it shifts as more years of the 2006 series are included, most notably around N = 3 (2008 crash enters) and N = 4 (2009 recovery enters).

| N | TW (£m) | Net (£m) | Mean $g$ of series[:N] |
|:---:|:---:|:---:|:---:|
| 5 | 24.05 | 0.62 | 3.39% |
| 10 | 33.94 | 2.13 | 5.53% |
| 15 | 36.52 | 2.53 | 4.83% |
| 20 | 46.80 | 4.13 | 4.43% |
| 25 | 67.54 | 7.38 | 5.12% |
| **29** | **84.63** | **10.11** | **5.64%** |
| 30 | 86.26 | 10.37 | 5.82% |

Table C.10.2: Honest declarer trajectory under 2006 historical return series by holding period. N = 29 row is the RATES reference scenario. TW and Net grow with N as additional years of compounding and WDT payments accumulate. Unlike C.7/C.8 (constant $g$ throughout), each row reflects a different prefix of the realised return history, making path-dependence explicit.

## C.11 Overstater TW Advantage Decomposition

**Purpose:** Identifies the three mechanical sources of the overstater TW advantage shown in C.8. For each ($\alpha$, $g$) cell the TW advantage relative to honest declaration is split into: (1) excess periodic net tax paid during the holding period, (2) the sell-year settlement delta, and (3) the post-sale oscillation delta. These three terms sum to the C.8 figure (sign-adjusted). An additional sub-table shows $f_N$ — the retained equity fraction at end of holding period — as a ratio to the honest declarer's $f_N$, quantifying the dilution cost of overstatement.

**Identity (corrected):** TW_settled($\alpha$) $-$ TW_settled(1) $=$ W_sell_delta $-$ RefundDelta $-$ SettleDelta  (verified to machine precision across all tested $(\alpha, g)$ pairs).  W_sell_delta $\leq 0$: f_N erosion reduces sell-year proceeds.  RefundDelta $\leq 0$: overstater receives a larger sell-year refund.  SettleDelta $\geq 0$: post-sale oscillation taxes back part of the refund.  Note: ExcessPeriodic (holding-period net tax difference) is **not** additive in this identity — it feeds into TW_advantage indirectly through f_N erosion and is shown in C.11a for reference only.

**Scope:** Overstaters only ($\alpha$ ≥ 1.0). All values at canonical N = 29, $k$ = 0.001, $V_0$ = £20m. Rows = $\alpha$; columns = $g$ (same grid as C.1). Sub-tables C.11a–C.11d expressed as % of TW_settled(1); C.11e is dimensionless.

### C.11a — W_sell_delta as % of Honest TW_settled  [Additive Term 1]

**Formula:** (W_sell($\alpha$) $-$ W_sell(1)) / TW_settled(1)  $\leq 0$ for $\alpha > 1$.  W_sell $= f_N \times V_{sell}$; the overstater's f_N is depleted faster by higher periodic tax, reducing the sell-year declared value.  This is the f_N erosion cost of overstatement: the overstater owns a smaller fraction of the asset at sale.  Note: ExcessPeriodic (holding-period net tax difference) is related but **not** equal to W_sell_delta — the excess periodic tax is approximately 6× larger than |W_sell_delta| at canonical parameters because most of the excess is returned via the sell-year refund (C.11b).  ExcessPeriodic is shown separately in C.11f for reference.

| $\alpha$ \ $g$ | -4.5% | 0.4% | 5.9% | 8.4% | 10.4% | 11.4% | 13.9% | 16.4% | 20.4% | 25.4% |
|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| **1.0** | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% |
| **1.2** | 0.00% | -0.00% | -0.14% | -0.29% | -0.51% | -0.65% | -1.20% | -2.14% | -4.31% | -5.91% |
| **1.5** | 0.00% | -0.01% | -0.35% | -0.74% | -1.27% | -1.62% | -2.97% | -5.21% | -9.87% | -12.77% |
| **1.8** | 0.00% | -0.02% | -0.56% | -1.18% | -2.03% | -2.58% | -4.70% | -8.10% | -14.51% | -18.04% |
| **2.0** | 0.00% | -0.03% | -0.70% | -1.47% | -2.53% | -3.22% | -5.83% | -9.91% | -17.20% | -20.96% |

Table C.11a: W_sell_delta as % of honest TW_settled (additive term 1). Always $\leq 0$ for $\alpha > 1$: f_N erosion reduces sell-year proceeds. $V_0$ = £20m, $k$ = 0.001, N = 29.

*Always $\leq 0$ for $\alpha > 1$: the overstater surrenders more equity as periodic tax, depressing the sell-year declared value.  The magnitude grows with both $\alpha$ and $g$ but is much smaller than the refund benefit (C.11b) — this is why the net TW advantage (C.11d) remains positive across the tested range.*

### C.11b — Sell-Year Settlement Delta as % of Honest TW_settled

**Formula:** ($L_{sell}$($\alpha$) $-$ $L_{sell}$(1)) / TW_settled(1)  · Negative = overstater receives a larger refund (or smaller tax) at sale. The declared basis at sale always exceeds true proceeds for $\alpha$ > 1 at any finite $g$, generating a refund that partially offsets the periodic cost.

| $\alpha$ \ $g$ | -4.5% | 0.4% | 5.9% | 8.4% | 10.4% | 11.4% | 13.9% | 16.4% | 20.4% | 25.4% |
|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| **1.0** | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% |
| **1.2** | 0.00% | -2.02% | -3.08% | -3.20% | -3.41% | -3.57% | -4.21% | -5.44% | -8.94% | -12.32% |
| **1.5** | 0.00% | -2.52% | -7.67% | -7.97% | -8.47% | -8.82% | -10.28% | -13.00% | -20.34% | -28.17% |
| **1.8** | 0.00% | -3.02% | -12.25% | -12.69% | -13.43% | -13.95% | -16.08% | -19.91% | -29.90% | -41.78% |
| **2.0** | 0.00% | -3.36% | -15.29% | -15.81% | -16.70% | -17.31% | -19.80% | -24.19% | -35.50% | -49.92% |

Table C.11b: Sell-year settlement delta as % of honest TW_settled. Negative = overstater received a larger refund at sale. $V_0$ = £20m, $k$ = 0.001, N = 29.

*Negative throughout (refund benefit) for all $\alpha$ > 1. Magnitude grows with $\alpha$ but is bounded by the lifetime cap. At high $g$ the honest declarer also pays a large sell-year tax, compressing the relative benefit.*

### C.11c — Post-Sale Settlement Delta as % of Honest TW_settled

**Formula:** (net_settle_tax($\alpha$) $-$ net_settle_tax(1)) / TW_settled(1)  · Positive = the post-sale oscillation taxes back more of the overstater's sell-year refund than it does for the honest declarer. This is the damping cost: a larger sell-year refund creates a larger positive delta in the first post-sale period, which is taxed back.

| $\alpha$ \ $g$ | -4.5% | 0.4% | 5.9% | 8.4% | 10.4% | 11.4% | 13.9% | 16.4% | 20.4% | 25.4% |
|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| **1.0** | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% |
| **1.2** | 0.00% | 0.27% | 0.43% | 0.47% | 0.53% | 0.58% | 0.78% | 1.24% | 2.86% | 4.91% |
| **1.5** | 0.00% | 0.33% | 1.07% | 1.16% | 1.32% | 1.44% | 1.94% | 3.02% | 6.77% | 11.46% |
| **1.8** | 0.00% | 0.40% | 1.71% | 1.86% | 2.11% | 2.29% | 3.08% | 4.72% | 10.27% | 17.23% |
| **2.0** | 0.00% | 0.44% | 2.13% | 2.33% | 2.64% | 2.86% | 3.82% | 5.80% | 12.42% | 20.72% |

Table C.11c: Post-sale settlement delta as % of honest TW_settled. Positive = oscillation recovered more from overstater's refund. $V_0$ = £20m, $k$ = 0.001, N = 29.

*Positive throughout for $\alpha$ > 1: the settle_tw() oscillation always recovers some of the sell-year refund via subsequent tax. The damping cost is smaller than the refund benefit (C.11b) in all tested cases — the net refund position remains favourable.*

### C.11d — Total TW Advantage as % of Honest TW_settled (Cross-Check)

**Formula:** (TW_settled($\alpha$) $-$ TW_settled(1)) / TW_settled(1)  · Should equal C.8 at the canonical N column. Values here are computed from the full decomposition and serve as an internal consistency check on C.11a–C.11c.

| $\alpha$ \ $g$ | -4.5% | 0.4% | 5.9% | 8.4% | 10.4% | 11.4% | 13.9% | 16.4% | 20.4% | 25.4% |
|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| **1.0** | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% |
| **1.2** | 0.00% | 1.74% | 2.51% | 2.44% | 2.38% | 2.34% | 2.22% | 2.06% | 1.77% | 1.51% |
| **1.5** | 0.00% | 2.17% | 6.25% | 6.07% | 5.87% | 5.76% | 5.37% | 4.77% | 3.71% | 3.95% |
| **1.8** | 0.00% | 2.60% | 9.98% | 9.65% | 9.29% | 9.08% | 8.30% | 7.09% | 5.12% | 6.51% |
| **2.0** | 0.00% | 2.89% | 12.45% | 12.02% | 11.52% | 11.23% | 10.15% | 8.47% | 5.88% | 8.24% |

Table C.11d: Total TW advantage as % of honest TW_settled. Should match C.5 (at canonical $k$) and C.8 (at canonical N) for each $\alpha$. $V_0$ = £20m, $k$ = 0.001, N = 29.

*Should match C.5 (at canonical $k$) and C.8 (at canonical N) for each $\alpha$. Any discrepancy exceeding 0.01pp indicates a decomposition error.*

### C.11e — Retained Equity Fraction Ratio at End of Holding Period

**Formula:** $f_N$($\alpha$) / $f_N$(1)  · Values below 1.0 indicate the overstater has surrendered more equity as tax during the holding period. This is the dilution cost: the overstater owns a smaller fraction of their asset at sale, which is why the sell-year declared value ($f_N \times V_{sell}$) is lower than it would otherwise be. The $f_N$ ratio is independent of $g$ within holding periods but shifts across $g$ because the progressive rate responds to declared wealth level.

| $\alpha$ \ $g$ | -4.5% | 0.4% | 5.9% | 8.4% | 10.4% | 11.4% | 13.9% | 16.4% | 20.4% | 25.4% |
|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| **1.0** | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 |
| **1.2** | 1.0000 | 1.0000 | 0.9986 | 0.9971 | 0.9950 | 0.9936 | 0.9882 | 0.9791 | 0.9586 | 0.9440 |
| **1.5** | 1.0000 | 0.9999 | 0.9965 | 0.9927 | 0.9875 | 0.9840 | 0.9709 | 0.9492 | 0.9053 | 0.8790 |
| **1.8** | 1.0000 | 0.9998 | 0.9944 | 0.9884 | 0.9800 | 0.9746 | 0.9539 | 0.9211 | 0.8607 | 0.8290 |
| **2.0** | 1.0000 | 0.9997 | 0.9930 | 0.9854 | 0.9750 | 0.9683 | 0.9428 | 0.9035 | 0.8349 | 0.8014 |

Table C.11e: Retained equity fraction ratio $f_N$($\alpha$) / $f_N$(1). Values below 1.0 = overstater surrendered more equity during holding period. $V_0$ = £20m, $k$ = 0.001, N = 29.

*Always < 1.0 for $\alpha$ > 1: the overstater's retained fraction is lower at every $g$. The ratio shrinks with $\alpha$ (more dilution) and with $g$ (higher declared wealth pushes the rate function higher, increasing $q$ each period). The $f_N$ ratio is the mechanism through which the declared basis at sale falls below $\alpha \times$ true value — it is not $\alpha \times f_N$(honest) $\times V_{sell}$ but rather $f_N$($\alpha$) $\times V_{sell}$, where $f_N$($\alpha$) < $f_N$(honest).*

*Key design implication: the overstater cannot manufacture a TW advantage by overstatement alone. The advantage in C.11d / C.8 persists because the sell-year refund benefit (C.11b) swamps the f_N erosion cost (C.11a) and the damping cost (C.11c) across all tested ($\alpha$, $g$) — by a factor of approximately 6:1 at canonical parameters. Whether this relationship holds beyond the tested range — particularly at very high $g$ where $f_N$ is heavily depleted — requires extension of the $g$ sweep above 25%.*

### C.11f — Excess Periodic Net Tax as % of Honest TW_settled  [Informational]

**Formula:** (Net_holding($\alpha$) $-$ Net_holding(1)) / TW_settled(1)  · Positive = overstater paid more net tax during the holding period.  **This term is NOT additive in the C.11 identity** — it is shown for reference only.  ExcessPeriodic feeds into tw_advantage indirectly through f_N erosion (higher periodic tax depletes f faster, reducing W_sell), but ExcessPeriodic $\gg$ |W_sell_delta| because most of the excess is returned as a sell-year refund (C.11b).  The correct additive decomposition uses W_sell_delta (C.11a), not ExcessPeriodic.

| $\alpha$ \ $g$ | -4.5% | 0.4% | 5.9% | 8.4% | 10.4% | 11.4% | 13.9% | 16.4% | 20.4% | 25.4% |
|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| **1.0** | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% |
| **1.2** | 0.00% | 0.33% | 2.38% | 2.80% | 3.13% | 3.30% | 3.89% | 4.83% | 6.92% | 8.33% |
| **1.5** | 0.00% | 0.83% | 6.01% | 7.11% | 7.98% | 8.45% | 10.06% | 12.55% | 17.47% | 20.15% |
| **1.8** | 0.00% | 1.33% | 9.71% | 11.55% | 13.04% | 13.84% | 16.62% | 20.73% | 27.99% | 31.29% |
| **2.0** | 0.00% | 1.67% | 12.22% | 14.57% | 16.52% | 17.57% | 21.18% | 26.39% | 34.93% | 38.39% |

Table C.11f: Excess periodic net tax as % of honest TW_settled (informational). Positive = overstater paid more net tax during holding period. Compare with C.11a (W_sell_delta): ExcessPeriodic is approximately 6× larger in magnitude, confirming that most of the periodic overpayment is recovered via the sell-year refund. $V_0$ = £20m, $k$ = 0.001, N = 29.

*Positive throughout at $g$ \geq ~8\%: the overstater pays more every period due to a larger declared delta and higher progressive rate. Despite this persistent periodic cost, the sell-year refund (C.11b) exceeds both the erosion cost (C.11a) and the damping cost (C.11c), producing the net TW advantage shown in C.11d.*
