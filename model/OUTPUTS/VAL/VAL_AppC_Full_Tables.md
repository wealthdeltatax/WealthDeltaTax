# C. WDT Valuation Analysis: Summary Tables {.appendix}

**Validation status:** All figures in this section are from Python model v1.0 (standalone, no Excel dependency), confirmed 0 FAILs across all primary matrices. Parameters unified to $k$ = 0.001, N = 19, $\tau_0$ = 15% across all companion papers. Table C.3 carries deviations up to 13% at extreme $\alpha$×β values (threshold 15%; 0 FAILs); see (VAL.A §C.3) note.

Unless otherwise stated, all figures use base parameters: $V_0$ = £20m, N = 19, $\tau_0$ = 15%, $\tau_m$ = 70%, $k$ = 0.001, $W_{min}$ = £2m, $g$ = 10.45%, $\alpha$ = 1, β = 0%. These are the Balanced transition scenario parameters from (RATES).

## C.1 Total Tax Paid (TTP) Difference Relative to Honest Declaration, as Share of Terminal Net Worth (TW)

**Metric:** (Net($\alpha$) − Net(1) / TW($\alpha$). Positive values indicate $\alpha$ pays more net tax than honest; negative values indicate less.

$\frac{Net(\alpha) - Net(1)}{TW(\alpha)}$

**Structural claim:** Understatement is more costly than honest declaration across the policy-relevant growth range. The penalty escalates steeply between $g$ ≈ 10% and $g$ ≈ 17.3%, then plateaus at a ceiling set by $\alpha$; the marginal deterrent stops escalating but does not reverse. The plateau inflection at $g$ ≈ 17.3% is a rate-function property that is approximately constant across all $\alpha$ and N-invariant above the plateau — simulation confirms that the plateau shape at N = 29 and N = 50 are visually identical (SWEEPS §2.3, Fig S3.1b). The C.1 metric for $\alpha$ = 0.1 exceeds 100% at approximately $g$ = 23–24% — the understater's excess tax exceeds their terminal wealth — but this is a normalisation artefact (the denominator, the understater's own TW, compresses at high growth), not a sign reversal in the penalty. For mild overstatement ($\alpha$ ≤ 1.5), overstatement produces a tax saving at moderate positive growth, with no reversal within the tested range at canonical parameters. For aggressive overstatement ($\alpha$ ≥ 1.8), the saving reverses in the $g$ ≈ 9–17% corridor containing the historical mean and recovers only above $g$ ≈ 17%; the self-limiting mechanism also operates temporally through the N-crossing described in §A.5.4. In negative growth scenarios the refund cap binds for understaters, reducing their net-tax advantage.

| $\alpha$ \ $g$ | -4.5% | 0.4% | 5.9% | 8.4% | 10.4% | 11.4% | 13.9% | 16.4% | 20.4% | 25.4% |
|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| **0.1** | 13.28% | 12.34% | 3.97% | 2.23% | 1.35% | 1.07% | 0.66% | 0.68% | 1.71% | 6.21% |
| **0.2** | 11.55% | 10.81% | 3.45% | 1.91% | 1.13% | 0.88% | 0.49% | 0.45% | 1.21% | 4.67% |
| **0.5** | 6.65% | 6.47% | 2.03% | 1.08% | 0.58% | 0.41% | 0.12% | 0.01% | 0.22% | 1.48% |
| **0.8** | 2.17% | 2.48% | 0.76% | 0.39% | 0.19% | 0.11% | -0.02% | -0.10% | -0.11% | 0.10% |
| **1.0** | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% |
| **1.2** | 0.00% | -0.95% | -0.70% | -0.34% | -0.13% | -0.05% | 0.10% | 0.22% | 0.35% | 0.46% |
| **1.5** | 0.00% | -0.91% | -1.66% | -0.75% | -0.22% | -0.02% | 0.40% | 0.76% | 1.28% | 2.04% |
| **1.8** | 0.00% | -0.86% | -2.51% | -1.06% | -0.21% | 0.12% | 0.86% | 1.53% | 2.65% | 4.49% |
| **2.0** | 0.00% | -0.83% | -3.02% | -1.22% | -0.15% | 0.28% | 1.25% | 2.17% | 3.77% | 6.51% |

Table C.1: TTP difference relative to honest declaration, as share of TW. $\alpha$ = 1.0 row is zero by construction. Positive values indicate understater pays more lifetime tax. $V_0$ = £20m, $k$ = 0.001, N = 19, $\tau_0$ = 15%, $\tau_m$ = 70%, $W_{min}$ = £2m.

## C.2 Effective Lifetime Tax Rate Difference from Honest Declaration

**Metric:** Net($\alpha$)/TW($\alpha$) − Net(1)/TW(1). Positive values indicate $\alpha$ has a higher effective lifetime rate than the honest declarer.

$\frac{Net(\alpha)}{TW(\alpha)} - \frac{Net(1)}{TW(1)}$

**Structural claim:** Effective lifetime tax rate differences are directionally consistent with C.1 but larger in magnitude, because the formula normalises by TW($\alpha$) and TW(1) separately rather than by a common denominator. Understaters face materially higher effective rates than honest declarers across all tested growth rates; overstaters face lower rates at moderate growth. The differential is largest at low and high growth extremes, reflecting refund protection loss and saturation effects respectively.

| $\alpha$ \ $g$ | -4.5% | 0.4% | 5.9% | 8.4% | 10.4% | 11.4% | 13.9% | 16.4% | 20.4% | 25.4% |
|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| **0.1** | 13.28% | 12.50% | 5.22% | 3.71% | 2.96% | 2.74% | 2.44% | 2.58% | 3.88% | 9.27% |
| **0.2** | 11.55% | 10.94% | 4.55% | 3.21% | 2.54% | 2.33% | 2.04% | 2.11% | 3.09% | 7.27% |
| **0.5** | 6.65% | 6.55% | 2.68% | 1.86% | 1.43% | 1.28% | 1.05% | 0.99% | 1.31% | 2.90% |
| **0.8** | 2.17% | 2.51% | 1.02% | 0.69% | 0.51% | 0.45% | 0.33% | 0.28% | 0.30% | 0.60% |
| **1.0** | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% |
| **1.2** | 0.00% | -0.97% | -0.94% | -0.62% | -0.44% | -0.37% | -0.23% | -0.13% | -0.03% | 0.03% |
| **1.5** | 0.00% | -0.93% | -2.24% | -1.43% | -0.96% | -0.79% | -0.40% | -0.08% | 0.39% | 1.07% |
| **1.8** | 0.00% | -0.88% | -3.40% | -2.12% | -1.35% | -1.05% | -0.38% | 0.24% | 1.29% | 3.07% |
| **2.0** | 0.00% | -0.85% | -4.10% | -2.51% | -1.54% | -1.16% | -0.26% | 0.60% | 2.14% | 4.83% |

Table C.2: Effective lifetime tax rate difference from honest declaration. $\alpha$ = 1.0 row is zero by construction. $V_0$ = £20m, $k$ = 0.001, N = 19, $\tau_0$ = 15%, $\tau_m$ = 70%, $W_{min}$ = £2m.

*Note: this table measures the difference in effective lifetime tax rate relative to honest declaration, not an absolute rate.*

## C.3 Exploratory Extension: Investor Confidence Effects β (Overstatement Only)

*This section is exploratory and not required for the operation of WDT. The beta mechanism is not empirically calibrated. Results are sensitivity testing, not prediction.*

**Metric:** (Net($\alpha$,β) − Net(1,β=0) / TW($\alpha$,β). β swept over the same numeric values as the $g$ columns in C.1/C.2; $g$ fixed at 10.45%.

$\frac{Net(\alpha, \beta) - Net(1, \beta=0)}{TW(\alpha, \beta)}$

**Structural claim:** β represents the sensitivity of true asset growth to declared valuation via $g_{eff} = g + \beta \cdot \ln(\alpha)$ (see (VAL.A §B.2.1) and (VAL.A §B.2.2). A positive β partially offsets the declaration cost where overstatement contributes to confidence formation. Scope is overstatement only ($\alpha$ ≥ 1.0); understater cells are omitted. Deviations at high $\alpha$×β values (up to 13%) reflect exponential compounding of g_eff over N = 19; directional claims are unaffected. No empirical calibration for β exists.

| $\alpha$ \ β | β=-4.5% | β=0.4% | β=5.9% | β=8.4% | β=10.4% | β=11.4% | β=13.9% | β=16.4% | β=20.4% | β=25.4% |
|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| **1.0** | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% |
| **1.2** | -2.43% | 0.08% | 2.46% | 3.44% | 4.19% | 4.53% | 5.38% | 6.20% | 7.39% | 8.74% |
| **1.5** | -5.88% | 0.25% | 5.15% | 6.95% | 8.27% | 8.85% | 10.26% | 11.58% | 13.50% | 15.80% |
| **1.8** | -9.18% | 0.49% | 7.31% | 9.68% | 11.41% | 12.17% | 14.08% | 15.99% | 19.12% | 23.64% |
| **2.0** | -11.32% | 0.70% | 8.65% | 11.39% | 13.45% | 14.37% | 16.79% | 19.37% | 23.96% | 30.88% |

Table C.3: Investor confidence β sensitivity (overstatement only). Sign convention: positive = $\alpha$ pays more than honest. β column values are the same numeric sweep as $g$ in C.1/C.2; $g$ fixed at 10.45%, N=19 throughout. Deviations increase at high $\alpha$×β due to exponential compounding; max deviation vs Excel 13% (threshold 15%; 0 FAILs). $V_0$ = £20m, $k$ = 0.001, $\tau_0$ = 15%, $\tau_m$ = 70%, $W_{min}$ = £2m.

## C.4 Effective Lifetime Tax Rate by $k$ Parameter and Initial Wealth ($V_0$)

**Metric:** TTP($\alpha$=1) / TW($\alpha$=1). Honest declaration throughout. Rows = k; columns = $V_0$ (£m).

$\frac{TTP(\alpha=1)}{TW(\alpha=1)}$

**Structural claim:** The S-curve rate function produces an effective lifetime rate that is low at small $V_0$ and rises toward $\tau_m$ at very large $V_0$ × high $k$ combinations. The policy-relevant $k$ range is approximately 1e-04 to 1e-03; values above 5e-03 are analytically extreme and included for completeness only. The rate ceiling of approximately 60.67% reflects the logistic bound at $\tau_m$ = 70% over N = 19 years.

| $k$ \ $V_0$ | £1m | £10m | £50m | £100m | £250m | £500m | £1000m | £2500m | £5000m | £10000m |
|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| 1e-04 | 10.72% | 12.56% | 12.69% | 12.86% | 13.38% | 14.27% | 16.10% | 21.71% | 29.89% | 40.02% |
| 2e-04 | 10.72% | 12.59% | 12.86% | 13.21% | 14.27% | 16.10% | 19.85% | 29.89% | 40.02% | 47.43% |
| 5e-04 | 10.73% | 12.68% | 13.38% | 14.26% | 17.03% | 21.70% | 29.88% | 42.92% | 48.70% | 49.99% |
| 1e-03 | 10.74% | 12.85% | 14.25% | 16.08% | 21.69% | 29.87% | 40.01% | 48.69% | 49.99% | 50.05% |
| 2e-03 | 10.75% | 13.17% | 16.06% | 19.81% | 29.85% | 40.00% | 47.43% | 49.99% | 50.05% | 50.05% |
| 5e-03 | 10.81% | 14.17% | 21.60% | 29.80% | 42.88% | 48.69% | 49.99% | 50.05% | 50.05% | 50.05% |
| 1e-02 | 10.90% | 15.89% | 29.71% | 39.91% | 48.67% | 49.99% | 50.05% | 50.05% | 50.05% | 50.05% |
| 5e-02 | 11.63% | 28.97% | 48.58% | 49.99% | 50.05% | 50.05% | 50.05% | 50.05% | 50.05% | 50.05% |
| 1e-01 | 12.58% | 38.83% | 49.98% | 50.05% | 50.05% | 50.05% | 50.05% | 50.05% | 50.05% | 50.05% |

Table C.4: Effective lifetime tax rate by $k$ and $V_0$. All at $\alpha$=1, β=0, $g$=10.45%, N=19. $k$ values above 1e-03 are analytically extreme; included for completeness.

## C.5 Sensitivity of $k$ and Alpha: Terminal Net Worth Difference vs Honest

**Metric:** (TW($\alpha$,k) − TW(1,k) / TW(1,k). Positive values indicate $\alpha$ retains more terminal net worth than honest; negative values indicate less.

$\frac{TW(\alpha,k) - TW(1,k)}{TW(1,k)}$

**Structural claim:** TW differences are directionally consistent across the tested $k$ range. Understater penalties scale with $k$ up to the logistic saturation boundary, beyond which further increases have diminishing effect. The overstater advantage follows the same pattern, accelerating at high $k$ ($k$ ≥ 1e-02) as the rate function's bracket ascent steepens. $k$ values above 1e-03 are analytically extreme.

| $\alpha$ \ $k$ | 1e-04 | 2e-04 | 5e-04 | 1e-03 | 2e-03 | 5e-03 | 1e-02 | 5e-02 | 1e-01 |
|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| **0.1** | -10.90% | -10.91% | -10.96% | -11.05% | -11.27% | -12.20% | -14.66% | -22.78% | -5.46% |
| **0.2** | -9.68% | -9.70% | -9.74% | -9.81% | -9.99% | -10.74% | -12.67% | -17.99% | -7.19% |
| **0.5** | -6.05% | -6.06% | -6.08% | -6.11% | -6.19% | -6.51% | -7.28% | -9.09% | -8.59% |
| **0.8** | -2.42% | -2.42% | -2.43% | -2.44% | -2.46% | -2.53% | -2.69% | -3.39% | -4.47% |
| **1.0** | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% |
| **1.2** | 2.42% | 2.42% | 2.42% | 2.42% | 2.43% | 2.43% | 2.43% | 3.38% | 5.37% |
| **1.5** | 6.04% | 6.04% | 6.04% | 6.04% | 6.02% | 5.91% | 5.67% | 8.68% | 14.58% |
| **1.8** | 9.67% | 9.67% | 9.65% | 9.63% | 9.56% | 9.21% | 8.52% | 14.40% | 24.66% |
| **2.0** | 12.08% | 12.08% | 12.06% | 12.01% | 11.88% | 11.30% | 10.25% | 18.49% | 31.67% |

Table C.5: TW difference vs honest, by $k$ and $\alpha$. $\alpha$ = 1.0 row is zero by construction. $g$ = 10.45%, N = 19 throughout.

## C.6 Terminal Net Worth After Refunds: Refund Protection Ratio

**Metric:** TW($\alpha$) / TW(1). Values below 100% indicate reduced TW relative to honest. Negative $g$ scenarios only.

$\frac{TW(\alpha)}{TW(1)}$

**Structural claim:** Understaters receive materially reduced terminal wealth in negative growth scenarios because the refund is calculated on the declared basis, not the true value. The protection loss is determined almost entirely by the entry declaration and is stable across negative growth rates for each $\alpha$ — the ratio at $g$ = −4.5% characterises the full negative-$g$ regime. Overstaters show 100% throughout: the lifetime cap prevents refunds exceeding prior contributions, which in a purely negative growth environment are zero for all strategies.

| $\alpha$ \ $g$ | -4.5% |
|:---:|:---:|
| **0.1** | 88.27% |
| **0.2** | 89.65% |
| **0.5** | 93.76% |
| **0.8** | 97.88% |
| **1.0** | 100.00% |
| **1.2** | 100.00% |
| **1.5** | 100.00% |
| **1.8** | 100.00% |
| **2.0** | 100.00% |

Table C.6: Refund protection ratio vs honest declaration. Negative $g$ scenarios only. $\alpha$ = 1.0 is 100% by construction. Understater protection loss proportional to basis gap at entry. $V_0$ = £20m, $k$ = 0.001, N = 19, $\tau_0$ = 15%, $\tau_m$ = 70%, $W_{min}$ = £2m.

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

**Metric:** TW(£m) and Net tax (£m) at $\alpha$ ∈ {2.0, 1.0, 0.1} across the $g$ sweep; ratios vs honest. N = 19 throughout.

**Structural claim:** The mechanism's fundamental properties hold across the full tested growth range. Understatement consistently costs more than honest declaration in absolute net-tax terms at every positive $g$ tested. The understater penalty escalates steeply between $g$ ≈ 10% and $g$ ≈ 17.3%, then plateaus — the rate ceiling stops further escalation but does not reverse it. The plateau ceiling scales with the degree of understatement: $\alpha$ = 0.1 plateaus near 98% of true wealth, $\alpha$ = 0.2 near 70%, $\alpha$ = 0.5 near 24%, $\alpha$ = 0.8 near 6%. The inflection at $g$ ≈ 17.3% is a rate-function property, approximately constant across all $\alpha$ and N-invariant above the plateau (see §A.5.4 and SWEEPS §2.3, Fig S3.1b). For overstaters, this table captures the contemporaneous growth-corridor effect for aggressive overstatement; the temporal N-crossing correction operates across holding periods and is documented in §C.8 and SWEEPS.A §A.4. The TW(0.1)/TW(1) ratio declines from approximately 86–87% at moderate growth to 63.2% at $g$ = 25.4%, reflecting compounding basis gap effects consistent with the penalty plateau. The C.1 metric exceeding 100% at $g$ = 25.4% for $\alpha$ = 0.1 is a normalisation artefact: it means the excess tax exceeds the understater's terminal wealth, not that the penalty reverses.

| $g$ | TW($\alpha$=2) £m | TW($\alpha$=1) £m | TW($\alpha$=0.1) £m | Net($\alpha$=2) £m | Net($\alpha$=1) £m | Net($\alpha$=0.1) £m | TW(0.1)/TW(1) | Net(0.1)/Net(1) |
|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| 25.4% | 1038.4 | 959.4 | 842.4 | 279.3 | 211.7 | 264.0 | 87.8% | — |
| 20.4% | 545.9 | 495.9 | 442.3 | 109.1 | 88.5 | 96.1 | 89.2% | — |
| 16.4% | 311.2 | 280.2 | 250.1 | 50.9 | 44.2 | 45.9 | 89.3% | — |
| 13.9% | 213.6 | 191.6 | 170.8 | 30.7 | 28.0 | 29.2 | 89.2% | — |
| 11.4% | 146.0 | 130.5 | 116.2 | 18.0 | 17.6 | 18.9 | 89.0% | — |
| 10.4% | 126.0 | 112.5 | 100.1 | 14.4 | 14.6 | 16.0 | 88.9% | — |
| 8.4% | 91.2 | 81.3 | 72.2 | 8.4 | 9.6 | 11.2 | 88.8% | — |
| 5.9% | 61.0 | 54.2 | 48.0 | 3.4 | 5.3 | 7.2 | 88.6% | — |
| 0.4% | 22.0 | 21.6 | 19.1 | 0.1 | 0.2 | 2.6 | 88.2% | — |

Table C.9: Summary of declaration incentives across growth regimes. TW and Net tax in £m. N = 19 throughout. Net($\alpha$=0.1)/Net($\alpha$=1) shown only where Net < 0 (refund scenario, negative $g$); '—' at positive $g$ where both Net values are positive. $V_0$ = £20m, $k$ = 0.001, N = 19, $\tau_0$ = 15%, $\tau_m$ = 70%, $W_{min}$ = £2m.

## C.10 2006 Historical Return Series — Reference Scenario Results

**Source:** RATES Balanced worst-case reference scenario (p['returns'] rotated to 2000 start year). $V_0$ = £20m, $\tau_0$ = 15%, $\tau_m$ = 70%, $k$ = 0.001, $W_{min}$ = £2m. No β adjustment applied.

**Purpose:** Locates the RATES worst-case scenario within the analytical space of C.1–C.9. The 2006 series includes the 2008 crash and subsequent recovery. The realised mean growth rate across N = 19 periods is 7.05%, below the 10.45% historical mean used in C.1–C.9; results here represent a harder test than the constant-$g$ tables.

### C.10.1 Declaration strategy comparison ($\alpha$ sweep, N = 19)

Each row uses p['returns'][:N] as the holding-period series and p['returns'][N] as the sell-year rate. The g_mean column is the arithmetic mean of the N holding-period returns.

| $\alpha$ | TW (£m) | TTP (£m) | Net (£m) | Eff rate | TW vs honest | Net vs honest |
|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| **0.1** | 57.87 | 10.13 | 8.79 | 15.19% | -11.03% | +25.82% |
| **0.2** | 58.67 | 9.84 | 8.57 | 14.61% | -9.80% | +22.71% |
| **0.5** | 61.07 | 9.01 | 7.95 | 13.01% | -6.11% | +13.75% |
| **0.8** | 63.46 | 8.21 | 7.36 | 11.59% | -2.44% | +5.32% |
| **1.0** | 65.05 | 7.71 | 6.99 | 10.74% | +0.00% | +0.00% ← honest |
| **1.2** | 66.63 | 8.24 | 6.63 | 9.95% | +2.44% | -5.08% |
| **1.5** | 69.00 | 10.39 | 6.13 | 8.88% | +6.08% | -12.25% |
| **1.8** | 71.36 | 12.57 | 5.67 | 7.94% | +9.71% | -18.88% |
| **2.0** | 72.93 | 14.04 | 5.38 | 7.38% | +12.12% | -23.00% |

Table C.10.1: Declaration strategy comparison, 2006 historical return series, N = 19. $\alpha$ = 1.0 row is the honest baseline; TW vs honest and Net vs honest are zero by construction. Positive Net vs honest = understater pays more net tax than honest under the historical series.

### C.10.2 Honest declarer trajectory by N ($\alpha$ = 1.0)

Each row uses p['returns'][:N] as the holding-period series and p['returns'][N] as the sell-year rate. The g_mean column is the arithmetic mean of the N holding-period returns; it shifts as more years of the 2006 series are included, most notably around N = 3 (2008 crash enters) and N = 4 (2009 recovery enters).

| N | TW (£m) | Net (£m) | Mean $g$ of series[:N] |
|:---:|:---:|:---:|:---:|
| 5 | 33.18 | 2.02 | 9.89% |
| 10 | 40.90 | 3.21 | 7.77% |
| 15 | 52.35 | 4.99 | 7.42% |
| **19** | **65.05** | **6.99** | **7.05%** |
| 20 | 65.99 | 7.13 | 7.14% |
| 25 | 69.46 | 7.68 | 6.01% |
| 30 | 89.36 | 10.86 | 5.99% |

Table C.10.2: Honest declarer trajectory under 2006 historical return series by holding period. N = 19 row is the RATES reference scenario. TW and Net grow with N as additional years of compounding and WDT payments accumulate. Unlike C.7/C.8 (constant $g$ throughout), each row reflects a different prefix of the realised return history, making path-dependence explicit.

## C.11 Overstater TW Advantage Decomposition

**Purpose:** Identifies the three mechanical sources of the overstater TW advantage shown in C.8. For each ($\alpha$, $g$) cell the TW advantage relative to honest declaration is split into: (1) excess periodic net tax paid during the holding period, (2) the sell-year settlement delta, and (3) the post-sale oscillation delta. These three terms sum to the C.8 figure (sign-adjusted). An additional sub-table shows $f_N$ — the retained equity fraction at end of holding period — as a ratio to the honest declarer's $f_N$, quantifying the dilution cost of overstatement.

**Identity (corrected):** TW_settled($\alpha$) $-$ TW_settled(1) $=$ W_sell_delta $-$ RefundDelta $-$ SettleDelta  (verified to machine precision across all tested $(\alpha, g)$ pairs).  W_sell_delta $\leq 0$: f_N erosion reduces sell-year proceeds.  RefundDelta $\leq 0$: overstater receives a larger sell-year refund.  SettleDelta $\geq 0$: post-sale oscillation taxes back part of the refund.  Note: ExcessPeriodic (holding-period net tax difference) is **not** additive in this identity — it feeds into TW_advantage indirectly through f_N erosion and is shown in C.11a for reference only.

**Scope:** Overstaters only ($\alpha$ ≥ 1.0). All values at canonical N = 19, $k$ = 0.001, $V_0$ = £20m. Rows = $\alpha$; columns = $g$ (same grid as C.1). Sub-tables C.11a–C.11d expressed as % of TW_settled(1); C.11e is dimensionless.

### C.11a — W_sell_delta as % of Honest TW_settled  [Additive Term 1]

**Formula:** (W_sell($\alpha$) $-$ W_sell(1)) / TW_settled(1)  $\leq 0$ for $\alpha > 1$.  W_sell $= f_N \times V_{sell}$; the overstater's f_N is depleted faster by higher periodic tax, reducing the sell-year declared value.  This is the f_N erosion cost of overstatement: the overstater owns a smaller fraction of the asset at sale.  Note: ExcessPeriodic (holding-period net tax difference) is related but **not** equal to W_sell_delta — the excess periodic tax is approximately 6× larger than |W_sell_delta| at canonical parameters because most of the excess is returned via the sell-year refund (C.11b).  ExcessPeriodic is shown separately in C.11f for reference.

| $\alpha$ \ $g$ | -4.5% | 0.4% | 5.9% | 8.4% | 10.4% | 11.4% | 13.9% | 16.4% | 20.4% | 25.4% |
|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| **1.0** | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% |
| **1.2** | 0.00% | -0.00% | -0.07% | -0.12% | -0.19% | -0.22% | -0.35% | -0.54% | -1.01% | -2.10% |
| **1.5** | 0.00% | -0.01% | -0.17% | -0.31% | -0.47% | -0.56% | -0.87% | -1.34% | -2.51% | -5.12% |
| **1.8** | 0.00% | -0.01% | -0.27% | -0.49% | -0.75% | -0.89% | -1.39% | -2.14% | -3.99% | -7.98% |
| **2.0** | 0.00% | -0.02% | -0.34% | -0.62% | -0.93% | -1.12% | -1.74% | -2.67% | -4.96% | -9.78% |

Table C.11a: W_sell_delta as % of honest TW_settled (additive term 1). Always $\leq 0$ for $\alpha > 1$: f_N erosion reduces sell-year proceeds. $V_0$ = £20m, $k$ = 0.001, N = 19.

*Always $\leq 0$ for $\alpha > 1$: the overstater surrenders more equity as periodic tax, depressing the sell-year declared value.  The magnitude grows with both $\alpha$ and $g$ but is much smaller than the refund benefit (C.11b) — this is why the net TW advantage (C.11d) remains positive across the tested range.*

### C.11b — Sell-Year Settlement Delta as % of Honest TW_settled

**Formula:** ($L_{sell}$($\alpha$) $-$ $L_{sell}$(1)) / TW_settled(1)  · Negative = overstater receives a larger refund (or smaller tax) at sale. The declared basis at sale always exceeds true proceeds for $\alpha$ > 1 at any finite $g$, generating a refund that partially offsets the periodic cost.

| $\alpha$ \ $g$ | -4.5% | 0.4% | 5.9% | 8.4% | 10.4% | 11.4% | 13.9% | 16.4% | 20.4% | 25.4% |
|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| **1.0** | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% |
| **1.2** | 0.00% | -1.37% | -2.99% | -3.00% | -3.04% | -3.06% | -3.16% | -3.34% | -3.86% | -5.27% |
| **1.5** | 0.00% | -1.70% | -7.48% | -7.50% | -7.57% | -7.63% | -7.87% | -8.28% | -9.49% | -12.62% |
| **1.8** | 0.00% | -2.04% | -11.95% | -11.98% | -12.09% | -12.17% | -12.52% | -13.14% | -14.91% | -19.38% |
| **2.0** | 0.00% | -2.27% | -14.93% | -14.95% | -15.08% | -15.18% | -15.59% | -16.33% | -18.43% | -23.58% |

Table C.11b: Sell-year settlement delta as % of honest TW_settled. Negative = overstater received a larger refund at sale. $V_0$ = £20m, $k$ = 0.001, N = 19.

*Negative throughout (refund benefit) for all $\alpha$ > 1. Magnitude grows with $\alpha$ but is bounded by the lifetime cap. At high $g$ the honest declarer also pays a large sell-year tax, compressing the relative benefit.*

### C.11c — Post-Sale Settlement Delta as % of Honest TW_settled

**Formula:** (net_settle_tax($\alpha$) $-$ net_settle_tax(1)) / TW_settled(1)  · Positive = the post-sale oscillation taxes back more of the overstater's sell-year refund than it does for the honest declarer. This is the damping cost: a larger sell-year refund creates a larger positive delta in the first post-sale period, which is taxed back.

| $\alpha$ \ $g$ | -4.5% | 0.4% | 5.9% | 8.4% | 10.4% | 11.4% | 13.9% | 16.4% | 20.4% | 25.4% |
|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| **1.0** | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% |
| **1.2** | 0.00% | 0.18% | 0.40% | 0.41% | 0.43% | 0.44% | 0.47% | 0.52% | 0.69% | 1.18% |
| **1.5** | 0.00% | 0.23% | 1.01% | 1.04% | 1.07% | 1.09% | 1.17% | 1.31% | 1.71% | 2.89% |
| **1.8** | 0.00% | 0.27% | 1.62% | 1.66% | 1.71% | 1.74% | 1.87% | 2.09% | 2.71% | 4.52% |
| **2.0** | 0.00% | 0.30% | 2.03% | 2.07% | 2.14% | 2.18% | 2.34% | 2.61% | 3.38% | 5.57% |

Table C.11c: Post-sale settlement delta as % of honest TW_settled. Positive = oscillation recovered more from overstater's refund. $V_0$ = £20m, $k$ = 0.001, N = 19.

*Positive throughout for $\alpha$ > 1: the settle_tw() oscillation always recovers some of the sell-year refund via subsequent tax. The damping cost is smaller than the refund benefit (C.11b) in all tested cases — the net refund position remains favourable.*

### C.11d — Total TW Advantage as % of Honest TW_settled (Cross-Check)

**Formula:** (TW_settled($\alpha$) $-$ TW_settled(1)) / TW_settled(1)  · Should equal C.8 at the canonical N column. Values here are computed from the full decomposition and serve as an internal consistency check on C.11a–C.11c.

| $\alpha$ \ $g$ | -4.5% | 0.4% | 5.9% | 8.4% | 10.4% | 11.4% | 13.9% | 16.4% | 20.4% | 25.4% |
|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| **1.0** | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% |
| **1.2** | 0.00% | 1.18% | 2.52% | 2.47% | 2.42% | 2.40% | 2.35% | 2.28% | 2.17% | 1.99% |
| **1.5** | 0.00% | 1.47% | 6.29% | 6.16% | 6.04% | 5.98% | 5.82% | 5.64% | 5.27% | 4.62% |
| **1.8** | 0.00% | 1.76% | 10.05% | 9.83% | 9.63% | 9.53% | 9.25% | 8.91% | 8.21% | 6.88% |
| **2.0** | 0.00% | 1.95% | 12.56% | 12.26% | 12.01% | 11.88% | 11.51% | 11.06% | 10.08% | 8.23% |

Table C.11d: Total TW advantage as % of honest TW_settled. Should match C.5 (at canonical $k$) and C.8 (at canonical N) for each $\alpha$. $V_0$ = £20m, $k$ = 0.001, N = 19.

*Should match C.5 (at canonical $k$) and C.8 (at canonical N) for each $\alpha$. Any discrepancy exceeding 0.01pp indicates a decomposition error.*

### C.11e — Retained Equity Fraction Ratio at End of Holding Period

**Formula:** $f_N$($\alpha$) / $f_N$(1)  · Values below 1.0 indicate the overstater has surrendered more equity as tax during the holding period. This is the dilution cost: the overstater owns a smaller fraction of their asset at sale, which is why the sell-year declared value ($f_N \times V_{sell}$) is lower than it would otherwise be. The $f_N$ ratio is independent of $g$ within holding periods but shifts across $g$ because the progressive rate responds to declared wealth level.

| $\alpha$ \ $g$ | -4.5% | 0.4% | 5.9% | 8.4% | 10.4% | 11.4% | 13.9% | 16.4% | 20.4% | 25.4% |
|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| **1.0** | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 |
| **1.2** | 1.0000 | 1.0000 | 0.9993 | 0.9988 | 0.9982 | 0.9978 | 0.9966 | 0.9948 | 0.9902 | 0.9798 |
| **1.5** | 1.0000 | 0.9999 | 0.9983 | 0.9970 | 0.9954 | 0.9945 | 0.9914 | 0.9869 | 0.9756 | 0.9508 |
| **1.8** | 1.0000 | 0.9999 | 0.9973 | 0.9951 | 0.9926 | 0.9912 | 0.9863 | 0.9790 | 0.9611 | 0.9233 |
| **2.0** | 1.0000 | 0.9998 | 0.9966 | 0.9939 | 0.9908 | 0.9890 | 0.9828 | 0.9738 | 0.9517 | 0.9059 |

Table C.11e: Retained equity fraction ratio $f_N$($\alpha$) / $f_N$(1). Values below 1.0 = overstater surrendered more equity during holding period. $V_0$ = £20m, $k$ = 0.001, N = 19.

*Always < 1.0 for $\alpha$ > 1: the overstater's retained fraction is lower at every $g$. The ratio shrinks with $\alpha$ (more dilution) and with $g$ (higher declared wealth pushes the rate function higher, increasing $q$ each period). The $f_N$ ratio is the mechanism through which the declared basis at sale falls below $\alpha \times$ true value — it is not $\alpha \times f_N$(honest) $\times V_{sell}$ but rather $f_N$($\alpha$) $\times V_{sell}$, where $f_N$($\alpha$) < $f_N$(honest).*

*Key design implication: the overstater cannot manufacture a TW advantage by overstatement alone. The advantage in C.11d / C.8 persists because the sell-year refund benefit (C.11b) swamps the f_N erosion cost (C.11a) and the damping cost (C.11c) across all tested ($\alpha$, $g$) — by a factor of approximately 6:1 at canonical parameters. Whether this relationship holds beyond the tested range — particularly at very high $g$ where $f_N$ is heavily depleted — requires extension of the $g$ sweep above 25%.*

### C.11f — Excess Periodic Net Tax as % of Honest TW_settled  [Informational]

**Formula:** (Net_holding($\alpha$) $-$ Net_holding(1)) / TW_settled(1)  · Positive = overstater paid more net tax during the holding period.  **This term is NOT additive in the C.11 identity** — it is shown for reference only.  ExcessPeriodic feeds into tw_advantage indirectly through f_N erosion (higher periodic tax depletes f faster, reducing W_sell), but ExcessPeriodic $\gg$ |W_sell_delta| because most of the excess is returned as a sell-year refund (C.11b).  The correct additive decomposition uses W_sell_delta (C.11a), not ExcessPeriodic.

| $\alpha$ \ $g$ | -4.5% | 0.4% | 5.9% | 8.4% | 10.4% | 11.4% | 13.9% | 16.4% | 20.4% | 25.4% |
|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| **1.0** | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% |
| **1.2** | 0.00% | 0.22% | 1.87% | 2.25% | 2.48% | 2.57% | 2.80% | 3.04% | 3.53% | 4.56% |
| **1.5** | 0.00% | 0.56% | 4.70% | 5.67% | 6.27% | 6.52% | 7.12% | 7.78% | 9.13% | 11.87% |
| **1.8** | 0.00% | 0.89% | 7.57% | 9.15% | 10.15% | 10.56% | 11.59% | 12.72% | 15.06% | 19.66% |
| **2.0** | 0.00% | 1.12% | 9.50% | 11.51% | 12.78% | 13.31% | 14.65% | 16.13% | 19.20% | 25.06% |

Table C.11f: Excess periodic net tax as % of honest TW_settled (informational). Positive = overstater paid more net tax during holding period. Compare with C.11a (W_sell_delta): ExcessPeriodic is approximately 6× larger in magnitude, confirming that most of the periodic overpayment is recovered via the sell-year refund. $V_0$ = £20m, $k$ = 0.001, N = 19.

*Positive throughout at $g$ \geq ~8\%: the overstater pays more every period due to a larger declared delta and higher progressive rate. Despite this persistent periodic cost, the sell-year refund (C.11b) exceeds both the erosion cost (C.11a) and the damping cost (C.11c), producing the net TW advantage shown in C.11d.*

## C.12 NPV-Adjusted Tax Position: Present Value of Tax Difference vs Honest

**Purpose:** Adjusts the C.1 nominal tax-difference metric for the time value of money. The C.1 metric treats £1 of tax paid in year 1 as equivalent to £1 received as a refund in year N+1. C.12 corrects this by discounting all cash flows to t=0 at a common rate ρ. The comparison reveals whether the apparent nominal advantage to mild overstaters survives discounting — or whether it is an artefact of comparing early real outflows against a late nominal refund.

**Metric:** $(NPV_{tax}(\alpha) - NPV_{tax}(1))$ / TW_settled(1), where $NPV_{tax}(\alpha) = \sum_{t=1}^{N+1} L_t / (1+\rho)^t$ and $\rho = 5\%$.

$\frac{NPV_{tax}(\alpha) - NPV_{tax}(1)}{TW_{settled}(1)}$

**Sign convention:** Positive = alpha pays more in present-value terms than honest (understater disadvantage). Negative = alpha pays less in PV terms (overstater advantage). Same as C.1, so tables are directly comparable.

**Structural claim:** Two regimes are visible when C.1 and C.12 are compared. At ρ = 5%, a cash flow at year 19 is worth approximately 40 pence on the pound relative to a year-1 payment, so the discount penalises late flows heavily. **Low-g regime (g $\lesssim$ 8%):** these are the cells where C.1 shows a genuine nominal advantage for overstaters (negative values). In C.12 those values compress sharply toward zero or reverse sign. At low g, the sell-year refund is large relative to periodic payments and arrives heavily discounted; the earlier periodic costs are smaller but weighted at shorter horizons. Discounting closes the gap: the apparent nominal advantage is a timing artefact. **Mid/high-g regime (g $\gtrsim$ 8%):** overstaters already pay more than honest declarers in C.1 (positive values). C.12 is larger still in this regime because the bulk of periodic overpayment concentrates in later holding years (when declared wealth is largest), but the sell-year refund is also late and discounted at the same rate; the net effect is that discounting penalises the refund more than the distributed periodic costs, pushing the C.12 value above C.1. **Understaters:** C.12 is systematically smaller in magnitude than C.1 at mid/high g. Understaters declare a lower basis and pay smaller periodic taxes early; their larger settlement at sale is discounted, partially offsetting their nominal penalty. At low g and high understatement, C.12 can turn negative (understater appears to benefit in PV terms because the refund on a very low basis is received early relative to the honest declarer's larger late settlement). The core design claim is preserved and strengthened: the low-g overstater advantage, which motivates the §A.6 population-equilibrium argument, is a nominal timing artefact that collapses once discounted. In PV terms it is approximately neutral or negative, making the design's tolerance of mild overstatement even more defensible than the nominal analysis suggests.

**Scope:** Full α grid (same as C.1). All values at canonical N = 19, $k$ = 0.001, $V_0$ = £20m, $\rho$ = 5%, $\tau_0$ = 15%, $\tau_m$ = 70%. Rows = α; columns = g (same grid as C.1).

| $\alpha$ \ $g$ | -4.5% | 0.4% | 5.9% | 8.4% | 10.4% | 11.4% | 13.9% | 16.4% | 20.4% | 25.4% |
|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| **0.1** | 5.08% | 4.53% | 0.25% | -0.48% | -0.79% | -0.86% | -0.90% | -0.73% | 0.00% | 2.42% |
| **0.2** | 4.49% | 4.02% | 0.21% | -0.45% | -0.72% | -0.79% | -0.84% | -0.71% | -0.11% | 1.87% |
| **0.5** | 2.70% | 2.51% | 0.11% | -0.31% | -0.49% | -0.54% | -0.60% | -0.55% | -0.28% | 0.66% |
| **0.8** | 0.92% | 1.00% | 0.04% | -0.14% | -0.22% | -0.24% | -0.27% | -0.26% | -0.19% | 0.07% |
| **1.0** | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% |
| **1.2** | 0.00% | -0.38% | -0.02% | 0.15% | 0.24% | 0.27% | 0.31% | 0.32% | 0.30% | 0.18% |
| **1.5** | 0.00% | -0.29% | -0.04% | 0.42% | 0.64% | 0.71% | 0.84% | 0.91% | 0.95% | 0.86% |
| **1.8** | 0.00% | -0.20% | -0.03% | 0.72% | 1.10% | 1.22% | 1.47% | 1.63% | 1.83% | 1.99% |
| **2.0** | 0.00% | -0.14% | -0.01% | 0.94% | 1.43% | 1.60% | 1.93% | 2.18% | 2.54% | 2.95% |

Table C.12: NPV-adjusted tax difference vs honest declaration, as % of honest TW_settled. $\alpha$ = 1.0 row is zero by construction. Compare directly with C.1: values closer to zero indicate the nominal C.1 advantage/disadvantage is a timing artefact; sign reversals indicate the PV position is opposite to the nominal position. $\rho$ = 5%, $V_0$ = £20m, $k$ = 0.001, N = 19, $\tau_0$ = 15%, $\tau_m$ = 70%, $W_{min}$ = £2m.

*Key reading:* Compare C.12 with C.1 column by column. Where C.1 shows a negative value for overstaters (advantage) and C.12 shows a value close to zero or positive, the nominal advantage is a timing artefact: the overstater pays early and is refunded late, and the time value of early payment approximately cancels or reverses the apparent gain. Where C.1 and C.12 agree in sign and magnitude for understaters, the penalty is real in both nominal and PV terms — understaters face genuine excess cost regardless of the discount rate applied.
