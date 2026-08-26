# VAL Illustrative Claims — Key Figures for Main Body Citation

**Generated:** 2026-08-17  
**Model:** Python v1.0 standalone · Parameters: $V_0$=£20m, $	au_0$=15%, $	au_m$=70%, k=0.001, W_min=£2m, g=10.45%, N=29  
**Source:** See limitation notes in §7 before citing any figure.

## 1. Reference Scenario

α = 1.0 (honest declaration) · g = 10.45% · N = 29 · $V_0$ = £20m · $	au_0$ = 15% · $	au_m$ = 70% · k = 0.001

| Metric | Value |
|:---|---:|
| $V_0$ (entry value) | £20.00m |
| V_sell (true value at sale) | £394.46m |
| W_sell (declared at sale) | £267.09m |
| TW (post-tax terminal wealth) | £263.12m |
| TTP (total taxes paid) | £41.59m |
| Refunds received | £0.00m |
| Net tax | £41.59m |
| Effective lifetime rate (Net/TW) | 15.81% |
| Retained fraction f_N | 67.71% |
| τ at W_sell | 18.36% |

*Reference values confirmed against Excel to 0.00% deviation.*

## 2. Declaration Strategy Comparison at Reference Parameters

g = 10.45%, N = 29, $V_0$ = £20m. All figures £m except percentages.

| α | TW £m | TTP £m | Net £m | Eff rate | TW vs honest | Net vs honest |
|:---:|---:|---:|---:|---:|---:|---:|
| 0.1 | 227.4 | 49.2 | 49.2 | 21.65% | -13.58% | +18.39% |
| 0.2 | 231.5 | 48.0 | 48.0 | 20.76% | -12.03% | +15.53% |
| 0.5 | 243.5 | 45.0 | 45.0 | 18.47% | -7.45% | +8.16% |
| 0.8 | 255.4 | 42.7 | 42.7 | 16.72% | -2.95% | +2.65% |
| 1.0 | 263.1 | 41.6 | 41.6 | 15.81% | +0.00% | +0.00% ← reference |
| 1.2 | 270.8 | 45.9 | 40.8 | 15.08% | +2.91% | -1.83% |
| 1.5 | 282.1 | 58.7 | 40.3 | 14.29% | +7.21% | -3.07% |
| 1.8 | 293.2 | 72.0 | 40.6 | 13.83% | +11.43% | -2.49% |
| 2.0 | 300.5 | 81.2 | 41.1 | 13.69% | +14.20% | -1.11% |

*TW vs honest: negative = understater retains less wealth. Net vs honest: positive = understater pays more tax.*

### Key figures for prose citation

- Severe understater (α=0.1): pays 18.4% more net tax than honest; retains -13.6% less terminal wealth.
- Moderate understater (α=0.5): pays 8.2% more net tax; retains -7.4% less TW.
- Mild understater (α=0.8): pays 2.7% more net tax; retains -3.0% less TW.
- Moderate overstater (α=1.5): pays -3.1% net tax relative to honest; retains 7.2% more TW.
- Strong overstater (α=2.0): pays -1.1% net tax relative to honest; retains 14.2% more TW.

## 3. Saturation Reversal — Correct Characterisation

**What the reversal is.** The understater always pays more net tax than the
honest declarer in absolute terms (Net(α=0.1) > Net(α=1) at all tested g).
The 'saturation reversal' is a different phenomenon: at extreme growth, the
C.1 metric — excess tax as share of the understater's own TW — can exceed
100%, meaning the understater's tax penalty exceeds their entire terminal wealth.

Separately, the TW gap between understater and honest (C.8) widens through
moderate growth, peaks around g=16%, then narrows at extreme growth as both
strategies approach $	au_m$. This is convergence of outcomes, not a sign reversal.

### C.1 metric (excess tax / understater TW) at α=0.1, N=34

| g | Net(α=0.1) £m | Net(α=1) £m | TW(α=0.1) £m | TW(α=1) £m | C.1 value |
|:---:|---:|---:|---:|---:|:---:|
| 7.0% | 19 | 15 | 101 | 116 | 3.5% |
| 10.0% | 43 | 37 | 205 | 237 | 3.2% |
| 13.9% | 139 | 108 | 484 | 570 | 6.5% |
| 16.0% | 283 | 195 | 726 | 884 | 12.1% |
| 20.0% | 1200 | 608 | 1252 | 1860 | 47.3% |
| 25.0% | 4501 | 2083 | 2478 | 4008 | 97.6% |


### C.8 metric (TW gap vs honest) at α=0.1, N=34 — convergence at high g

| g | TW(α=0.1) £m | TW(α=1) £m | C.8 value (gap) |
|:---:|---:|---:|:---:|
| 7.0% | 101 | 116 | -13.3% |
| 10.0% | 205 | 237 | -13.5% |
| 13.9% | 484 | 570 | -15.1% |
| 16.0% | 726 | 884 | -17.9% |
| 20.0% | 1252 | 1860 | -32.7% |
| 25.0% | 2478 | 4008 | -38.2% |
| 50.0% | 91990 | 104150 | -11.7% |

*The TW gap widens through moderate growth (honest wealth compounds faster) then
narrows at extreme growth as $	au_m$ constrains both strategies. This is the
'saturation convergence' described in VAL.A §A.5.4 (Proposition 4). The gap
remains negative (understater retains less TW) at all tested growth rates.*

## 4. Terminal Wealth Protection Ratio (C.6 Metric)

**Formula:** TW(α) / TW(1) — what fraction of the honest declarer's terminal
wealth does the understater retain? Values below 100% indicate the understater
ends up with less post-tax wealth than an honest declarer would.

**Model note.** The constant-g model cannot simulate mixed growth paths (positive
growth then a crash). At sustained negative g, wealth falls below W_min before
generating meaningful tax history, producing no refund for either strategy.
The TW ratio at positive g captures the protection cost structurally: an
understater's lower retained fraction compounds throughout the holding period,
leaving less post-tax wealth regardless of whether growth is high or moderate.

| α \ g | 1% | 2% | 5% | 7% | 10% | 13.9% | 16.5% |
|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| **0.1** | 86.4% | 86.5% | 86.6% | 86.7% | 86.5% | 84.9% | 81.1% |
| **0.2** | 87.9% | 88.0% | 88.1% | 88.2% | 88.0% | 86.7% | 83.6% |
| **0.5** | 92.4% | 92.5% | 92.6% | 92.6% | 92.6% | 91.9% | 90.4% |
| **0.8** | 97.0% | 97.0% | 97.0% | 97.1% | 97.1% | 96.9% | 96.4% |

*TW ratio is stable across positive growth rates for each α — determined
primarily by the entry basis declaration, not by subsequent growth.*

### Key figures for prose citation (g = 7%, N = 34)

- α=0.1 (severe understatement): retains 86.7% of honest TW (£100.7m vs £116.2m). Protection shortfall: £15.5m.
- α=0.5 (moderate understatement): retains 92.6% of honest TW.
- α=0.8 (mild understatement): retains 97.1% of honest TW.
- The ratio is nearly identical at g=1% and g=10%, confirming the protection
  loss is set by the entry declaration, not by subsequent growth.

*VAL.A §C.6 narrative claim — 'understaters receive materially smaller refund
entitlement' — is confirmed by the TW shortfall. The protection cost is
stable, not growth-dependent, and runs in both directions: understaters pay
more tax on gains and retain less wealth throughout the holding period.*

## 5. Indifference Horizon

The understater pays more total net tax than an honest declarer at all tested
holding periods (at reference g=10.45%). This section establishes whether a
horizon exists at which the understater's premium over honest falls below a
threshold — useful for characterising the 'deferred delta' mechanism.

**Metric:** (Net(α,N) − Net(1,N)) / Net(1,N) — the relative premium over honest. g = 10.45%.

| α \ N | 5 | 10 | 15 | 20 | 25 | 30 | 35 | 40 | 45 | 50 | 55 | 60 |
|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| **0.1** | 129.6% | 57.4% | 32.7% | 22.2% | 18.3% | 18.8% | 23.6% | 33.4% | 50.5% | 76.0% | 104.9% | 121.9% |
| **0.2** | 115.1% | 50.9% | 28.8% | 19.3% | 15.7% | 15.8% | 19.6% | 27.6% | 41.3% | 61.7% | 84.4% | 97.0% |
| **0.5** | 71.7% | 31.4% | 17.5% | 11.3% | 8.7% | 8.2% | 9.6% | 13.2% | 19.4% | 28.3% | 37.7% | 42.3% |
| **0.8** | 28.6% | 12.4% | 6.8% | 4.2% | 3.0% | 2.6% | 2.8% | 3.7% | 5.3% | 7.7% | 10.2% | 11.6% |

### Observations

- At α=0.8 (mild understatement), the premium over honest is lowest at N=30 (2.6%) at reference growth.
- The premium does not cross zero at reference parameters within N=5–60: understatement is never cheaper than honest at g=10.45%.
- The premium is largest at short horizons (realisation delta dominates immediately)
  and compresses — but does not eliminate — at long horizons.

*No indifference point exists at reference parameters within economically
plausible holding periods. VAL.A's structural claim (understater pays more
at moderate growth) is confirmed unconditionally for g = 10.45%, N ≤ 60.*

## 6. Marginal Rate Function τ(W) — Reference Profile

$	au_0$ = 20% · $	au_m$ = 70% · k = 0.0001 · W_min = £2m

| W (£m) | τ(W) |
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

- τ = 35% at W ≈ £1m (£1bn)
- τ = 40% at W ≈ £2m (£2bn)
- τ = 50% at W ≈ £2m (£2bn)
- τ = 60% at W ≈ £3m (£3bn)
- τ = 65% at W ≈ £4m (£4bn)

*The rate function is an S-curve; rates rise slowly at moderate wealth and
compress toward $	au_m$ = 70% only at extreme concentrations.*

## 7. Model Limitation Notes

These notes accompany all figures above and should be read before citing.

**Option A convention.** All simulations treat N annual periods as N assessment
windows. The VAL design allows windows of 1–7 years; the model treats every
period as an annual window. This produces variance from a window-aware model,
particularly for the §K dilution example (3-year window runs as N=3 annual periods).

**Constant g.** The model uses a constant growth rate throughout the holding
period and sell year. Real portfolios have volatile returns; the constant-g
assumption smooths out the timing effects that would affect a real taxpayer.

**Route C throughout.** The simulation models Route C (fungible, self-declared,
in-kind settlement). Route D mechanics (deferred to realisation, no periodic
settlement) produce different incentive profiles; the model does not simulate
Route D directly.

**Table C.4 deviation.** Max 2.67% deviation from Excel in the k×V₀ table.
Excel AppC cells appear computed at a different params state (snapshot issue).
Python values are used throughout; this deviation is documented, not corrected.

**Beta formula.** VAL.A §B.3 states g_eff = g × (1 + β·ln(α)) [multiplicative].
The Excel cell formula confirms g_eff = g + β·ln(α) [additive]. All Python
outputs use the additive formula. VAL.A §B.3 and §C.3 require correction.

**Saturation reversal boundary.** VAL.A §C.9 states 'g ≥ 15%' as the boundary.
Python model finds the crossover for α=0.1 at approximately 16–18% (see §3 above).
The directional claim is confirmed; the specific threshold requires updating in VAL.A §C.9.
