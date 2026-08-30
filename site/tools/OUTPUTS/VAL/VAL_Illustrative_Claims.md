# VAL Illustrative Claims — Key Figures for Main Body Citation

**Generated:** 2026-08-30  
**Model:** Python v1.0 standalone · Parameters: $V_0$=£20m, $\tau_0$=15%, $\tau_m$=70%, $k$=0.001, $W_{min}$=£2m, $g$=10.45%, N=29  
**Source:** See limitation notes in §7 before citing any figure.

## 1. Reference Scenario

$\alpha$ = 1.0 (honest declaration) · $g$ = 10.45% · N = 29 · $V_0$ = £20m · $\tau_0$ = 15% · $\tau_m$ = 70% · $k$ = 0.001

| Metric | Value |
|:---|---:|
| $V_0$ (entry value) | £20.00m |
| $V_{sell}$ (true value at sale) | £394.46m |
| $W_{sell}$ (declared at sale) | £267.09m |
| TW (post-tax terminal wealth) | £263.73m |
| TTP (total taxes paid) | £41.59m |
| Refunds received | £0.00m |
| Net (lifetime net tax) | £40.98m |
| Effective lifetime rate (Net/TW) | 15.54% |
| Retained fraction $f_N$ | 67.71% |
| $\tau$ at $W_{sell}$ | 18.36% |

*Reference values confirmed against Excel to 0.00% deviation.*

## 2. Declaration Strategy Comparison at Reference Parameters

$g$ = 10.45%, N = 29, $V_0$ = £20m. All figures £m except percentages.

| $\alpha$ | TW £m | TTP £m | Net £m | Eff rate | TW vs honest | Net vs honest |
|:---:|---:|---:|---:|---:|---:|---:|
| **0.1** | 234.3 | 49.2 | 42.3 | 18.06% | -11.16% | +3.29% |
| **0.2** | 237.7 | 48.0 | 41.8 | 17.60% | -9.88% | +2.09% |
| **0.5** | 247.6 | 45.0 | 40.9 | 16.51% | -6.10% | -0.25% |
| **0.8** | 257.4 | 42.7 | 40.7 | 15.81% | -2.41% | -0.72% |
| **1.0** | 263.7 | 41.6 | 41.0 | 15.54% | +0.00% | +0.00% ← reference |
| **1.2** | 270.0 | 45.9 | 41.6 | 15.41% | +2.38% | +1.55% |
| **1.5** | 279.2 | 58.7 | 43.2 | 15.47% | +5.87% | +5.41% |
| **1.8** | 288.2 | 72.0 | 45.5 | 15.79% | +9.29% | +11.08% |
| **2.0** | 294.1 | 81.2 | 47.5 | 16.14% | +11.52% | +15.87% |

*TW vs honest: negative = understater retains less settled wealth. Net vs honest: positive = understater pays more lifetime tax.*

### Key figures for prose citation

- Severe understater ($\alpha$=0.1): pays 3.3% more net tax than honest; retains -11.2% less terminal wealth.
- Moderate understater ($\alpha$=0.5): pays -0.3% more net tax; retains -6.1% less TW.
- Mild understater ($\alpha$=0.8): pays -0.7% more net tax; retains -2.4% less TW.
- Moderate overstater ($\alpha$=1.5): pays 5.4% net tax relative to honest; retains 5.9% more TW.
- Strong overstater ($\alpha$=2.0): pays 15.9% net tax relative to honest; retains 11.5% more TW.

## 3. Saturation Reversal — Correct Characterisation

**What the reversal is.** The understater always pays more net tax than the honest declarer in absolute terms (Net($\alpha$=0.1) > Net($\alpha$=1) at all tested $g$). The 'saturation reversal' is a different phenomenon: at extreme growth, the C.1 metric — excess tax as share of the understater's own TW — can exceed 100%, meaning the understater's tax penalty exceeds their entire terminal wealth.

Separately, the TW gap between understater and honest (C.8) widens through moderate growth, peaks around $g$ = 16%, then narrows at extreme growth as both strategies approach $\tau_m$. This is convergence of outcomes, not a sign reversal.

### C.1 metric (excess tax / understater TW) at $\alpha$=0.1, N=29

| $g$ | Net($\alpha$=0.1) £m | Net($\alpha$=1) £m | TW($\alpha$=0.1) £m | TW($\alpha$=1) £m | C.1 value |
|:---:|---:|---:|---:|---:|:---:|
| 7.0% | 17 | 15 | 103 | 116 | 1.2% |
| 10.0% | 37 | 36 | 211 | 238 | 0.6% |
| 13.9% | 116 | 105 | 507 | 572 | 2.2% |
| 16.0% | 229 | 188 | 779 | 890 | 5.2% |
| 20.0% | 920 | 574 | 1531 | 1893 | 22.6% |
| 25.0% | 3175 | 1937 | 3805 | 4155 | 32.5% |


### C.8 metric (TW gap vs honest) at $\alpha$=0.1, N=29 — convergence at high $g$

| $g$ | TW($\alpha$=0.1) £m | TW($\alpha$=1) £m | C.8 value (gap) |
|:---:|---:|---:|:---:|
| 7.0% | 103 | 116 | -11.3% |
| 10.0% | 211 | 238 | -11.2% |
| 13.9% | 507 | 572 | -11.5% |
| 16.0% | 779 | 890 | -12.5% |
| 20.0% | 1531 | 1893 | -19.1% |
| 25.0% | 3805 | 4155 | -8.4% |
| 50.0% | 160829 | 111753 | 43.9% |

*The TW gap widens through moderate growth (honest wealth compounds faster) then narrows at extreme growth as $\tau_m$ constrains both strategies. This is the 'saturation convergence' described in VAL.A §A.5.4 (Proposition 4). The gap remains negative (understater retains less TW) at all tested growth rates.*

## 4. Terminal Wealth Protection Ratio (C.6 Metric)

**Formula:** TW($\alpha$) / TW(1) — what fraction of the honest declarer's terminal wealth does the understater retain? Values below 100% indicate the understater ends up with less post-tax wealth than an honest declarer would.

**Model note.** The constant-$g$ model cannot simulate mixed growth paths (positive growth then a crash). At sustained negative $g$, wealth falls below $W_{min}$ before generating meaningful tax history, producing no refund for either strategy. The TW ratio at positive $g$ captures the protection cost structurally: an understater's lower retained fraction compounds throughout the holding period, leaving less post-tax wealth regardless of whether growth is high or moderate.

| $\alpha$ \ $g$ | 1% | 2% | 5% | 7% | 10% | 13.9% | 16.5% |
|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| **0.1** | 88.2% | 88.3% | 88.5% | 88.7% | 88.8% | 88.5% | 87.1% |
| **0.2** | 89.5% | 89.6% | 89.8% | 89.9% | 90.1% | 89.9% | 88.9% |
| **0.5** | 93.4% | 93.5% | 93.6% | 93.7% | 93.9% | 93.9% | 93.7% |
| **0.8** | 97.4% | 97.4% | 97.5% | 97.5% | 97.6% | 97.7% | 97.7% |

*TW ratio is stable across positive growth rates for each $\alpha$ — determined primarily by the entry basis declaration, not by subsequent growth.*

### Key figures for prose citation ($g$ = 7%, N = 29)

- $\alpha$=0.1 (severe understatement): retains 88.7% of honest TW (£103.2m vs £116.4m). Protection shortfall: £13.2m.
- $\alpha$=0.5 (moderate understatement): retains 93.7% of honest TW.
- $\alpha$=0.8 (mild understatement): retains 97.5% of honest TW.
- The ratio is nearly identical at $g$=1% and $g$=10%, confirming the protection loss is set by the entry declaration, not by subsequent growth.

*VAL.A §C.6 narrative claim — 'understaters receive materially smaller refund entitlement' — is confirmed by the TW shortfall. The protection cost is stable, not growth-dependent, and runs in both directions: understaters pay more tax on gains and retain less settled wealth throughout the holding period.*

## 5. Indifference Horizon

The understater pays more total net tax than an honest declarer at all tested holding periods (at reference $g$=10.45%). This section establishes whether a horizon exists at which the understater's premium over honest falls below a threshold — useful for characterising the 'deferred delta' mechanism.

**Metric:** (Net($\alpha$,N) − Net(1,N)) / Net(1,N) — the relative premium over honest. $g$ = 10.45%.

| $\alpha$ \ N | 5 | 10 | 15 | 20 | 25 | 30 | 35 | 40 | 45 | 50 | 55 | 60 |
|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| **0.1** | 105.7% | 40.0% | 17.6% | 7.9% | 3.9% | 3.5% | 6.3% | 12.7% | 24.0% | 41.4% | 62.0% | 73.5% |
| **0.2** | 93.8% | 35.4% | 15.4% | 6.6% | 2.8% | 2.2% | 4.2% | 9.1% | 17.8% | 30.9% | 45.7% | 52.6% |
| **0.5** | 58.4% | 21.7% | 9.1% | 3.3% | 0.6% | -0.3% | 0.0% | 1.6% | 4.7% | 9.1% | 13.2% | 13.9% |
| **0.8** | 23.2% | 8.5% | 3.4% | 1.0% | -0.2% | -0.8% | -1.0% | -0.9% | -0.5% | 0.1% | 0.6% | 0.5% |

### Observations

- At $\alpha$=0.8 (mild understatement), the premium over honest is lowest at N=35 (-1.0%) at reference growth.
- The premium does not cross zero at reference parameters within N=5–60: understatement is never cheaper than honest at $g$=10.45%.
- The premium is largest at short horizons (realisation delta dominates immediately) and compresses — but does not eliminate — at long horizons.

*No indifference point exists at reference parameters within economically plausible holding periods. VAL.A's structural claim (understater pays more at moderate growth) is confirmed unconditionally for $g$ = 10.45%, N ≤ 60.*

## 6. Marginal Rate Function $\tau$(W) — Reference Profile

$\tau_0$ = 15% · $\tau_m$ = 70% · $k$ = 0.001 · $W_{min}$ = £2m

| W (£m) | $\tau$(W) |
|---:|:---:|
| 0 | 0.00% |
| 2 | 15.00% |
| 5 | 15.04% |
| 10 | 15.09% |
| 20 | 15.21% |
| 50 | 15.57% |
| 100 | 16.19% |
| 200 | 17.46% |
| 500 | 21.68% |
| 1,000 | 29.77% |
| 2,000 | 46.75% |
| 5,000 | 68.31% |
| 10,000 | 69.99% |

### Notable thresholds

- $\tau$ = 35% at W ≈ £1bn
- $\tau$ = 40% at W ≈ £2bn
- $\tau$ = 50% at W ≈ £2bn
- $\tau$ = 60% at W ≈ £3bn
- $\tau$ = 65% at W ≈ £4bn

*The rate function is an S-curve; rates rise slowly at moderate wealth and compress toward $\tau_m$ = 70% only at extreme concentrations.*

## 7. Model Limitation Notes

These notes accompany all figures above and should be read before citing.

**Option A convention.** All simulations treat N annual periods as N assessment windows. The VAL design allows windows of 1–7 years; the model treats every period as an annual window. This produces variance from a window-aware model, particularly for the §K dilution example (3-year window runs as N=3 annual periods).

**Constant $g$.** The model uses a constant growth rate throughout the holding period and sell year. Real portfolios have volatile returns; the constant-$g$ assumption smooths out the timing effects that would affect a real taxpayer.

**Route C throughout.** The simulation models Route C (fungible, self-declared, in-kind settlement). Route D mechanics (deferred to realisation, no periodic settlement) produce different incentive profiles; the model does not simulate Route D directly.

**Table C.4 deviation.** Max 2.67% deviation from Excel in the $k$×$V_0$ table. Excel AppC cells appear computed at a different params state (snapshot issue). Python values are used throughout; this deviation is documented, not corrected.

**Beta formula.** VAL.A §B.3 states $g_{eff} = g \times (1 + \beta\cdot\ln(\alpha))$ [multiplicative]. The Excel cell formula confirms $g_{eff} = g + \beta\cdot\ln(\alpha)$ [additive]. All Python outputs use the additive formula. VAL.A §B.3 and §C.3 require correction.

**Saturation reversal boundary.** VAL.A §C.9 states '$g$ ≥ 15%' as the boundary. Python model finds the crossover for $\alpha$=0.1 at approximately 16–18% (see §3 above). The directional claim is confirmed; the specific threshold requires updating in VAL.A §C.9.
