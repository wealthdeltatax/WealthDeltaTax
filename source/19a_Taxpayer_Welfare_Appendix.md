---
title: "The Wealth Delta Tax: Taxpayer Welfare Comparison Appendix Tables"
shortcode: "WFR.A"
status: "draft"
zenodo_doi: "10.5281/zenodo.XXXXXXX"
keywords:
    - Wealth Delta Tax
    - welfare comparison
    - Domar-Musgrave
    - capital gains tax lock-in
    - return heterogeneity
    - revenue equivalence
---

### Revision History {.unnumbered .unlisted}

| Revision | Date          | Details                                      |
|:--------:|:-------------:|----------------------------------------------|
| 0.01     | 10 September 2026 | Initial generation of simulation tables. Sections A–E covering baseline single-agent comparison, progressive rate complications, CGT lock-in distortion, heterogeneous agent incidence and concentration, and welfare sweep analysis across revenue targets, start years, and logistic rate parameters. |

\newpage
\tableofcontents
\newpage

# A. Baseline Single-Agent Comparison

Revenue target: E[T] = 2% of $W_0$ across all systems. All CEW values are relative to a no-tax benchmark; negative values indicate a welfare cost relative to that benchmark. Tables A.1–A.4 correspond to the single-agent controlled baseline described in (WFR §3).

## A.1 Consumption-Equivalent Welfare (CEW) by System, γ, and Distribution

CEW is the proportional change in consumption under a no-tax counterfactual that would make the agent indifferent to the taxed system. Negative values indicate a welfare cost relative to the no-tax benchmark. Ver. A is the UK historical equity return sequence (73 observations, 1947–2019). Ver. B is an idealised two-state distribution with the same mean and standard deviation (p=0.5, R_good=E[R]+σ, R_bad=E[R]−σ).

| System | Ver. A γ=1 | Ver. A γ=2 | Ver. A γ=4 | Ver. B γ=1 | Ver. B γ=2 | Ver. B γ=4 |
|:---|---:|---:|---:|---:|---:|---:|
| Symmetric WDT | -1.8203% | -1.7539% | -1.6217% | -1.8198% | -1.7525% | -1.6188% |
| Stock Wealth Tax | -1.8870% | -1.8870% | -1.8870% | -1.8870% | -1.8870% | -1.8870% |
| Income Tax | -1.8288% | -1.7713% | -1.6583% | -1.8198% | -1.7525% | -1.6188% |
| CGT | -1.8288% | -1.7713% | -1.6583% | -1.8198% | -1.7525% | -1.6188% |
| Consumption Tax | -1.8870% | -1.8870% | -1.8870% | -1.8870% | -1.8870% | -1.8870% |

Income Tax and CGT show identical CEW and identical revenue-equivalent rates throughout this table. This is correct by construction: this module models CGT as a gains-only tax with the same base as income tax and no realisation decision. The two systems are structurally identical in a single-period model where all gains are realised each period. The lock-in distortion that separates CGT from income tax in practice is endogenous and enters only in Section C, where it generates the largest welfare difference in the model.

## A.2 Variance of Consumption by System (γ=2)

Variance of consumption across return states at revenue-equivalent rates. Lower variance indicates greater risk-sharing. The Domar-Musgrave prediction is Var(C_sym) = (1−$\tau$)² × Var(C_notax); confirmation at A.4 below.

| System | Ver. A Var(C) | Ver. B Var(C) |
|:---|---:|---:|
| Symmetric WDT | 0.0013 | 0.0013 |
| Stock Wealth Tax | 0.0027 | 0.0027 |
| Income Tax | 0.0014 | 0.0013 |
| CGT | 0.0014 | 0.0013 |
| Consumption Tax | 0.0027 | 0.0027 |

## A.3 Revenue-Equivalent Tax Rates (γ=2)

Rate $\tau$\* such that E[T($W_0$, dist, $\tau$\*)] = target. Rates differ across systems because tax bases differ. Stock wealth and consumption taxes require low rates (broad base); income tax and CGT require higher rates (gains only, no collection in loss states).

| System | Ver. A rate ($\tau$*) | Ver. B rate ($\tau$*) |
|:---|---:|---:|
| Symmetric WDT | 33.404% | 33.404% |
| Stock Wealth Tax | 1.887% | 1.887% |
| Income Tax | 32.067% | 33.404% |
| CGT | 32.067% | 33.404% |
| Consumption Tax | 1.923% | 1.923% |

## A.4 Domar-Musgrave Test: Symmetric WDT

The Domar-Musgrave prediction is Var(C_tax) / Var(C_notax) = (1−$\tau$)². A gap near zero confirms D-M holds for the flat-rate symmetric case. A progressive rate schedule breaks D-M — see Section B.

| Distribution | γ | $\tau$ (WDT) | (1−$\tau$)² | Actual ratio | Gap | Holds? |
|:---|---:|---:|---:|---:|---:|:---:|
| Ver. A | 1.0 | 33.4039% | 0.443505 | 0.443505 | -5.55e-17 | ✓ |
| Ver. A | 2.0 | 33.4039% | 0.443505 | 0.443505 | -5.55e-17 | ✓ |
| Ver. A | 4.0 | 33.4039% | 0.443505 | 0.443505 | -5.55e-17 | ✓ |
| Ver. B | 1.0 | 33.4039% | 0.443505 | 0.443505 | 9.44e-16 | ✓ |
| Ver. B | 2.0 | 33.4039% | 0.443505 | 0.443505 | 9.44e-16 | ✓ |
| Ver. B | 4.0 | 33.4039% | 0.443505 | 0.443505 | 9.44e-16 | ✓ |

Gaps are at floating-point precision (10⁻¹⁶ to 10⁻¹⁷), confirming the D-M property holds exactly for the flat symmetric case.

\newpage

# B. Progressive Rates and the Three D-M Complications

Tables B.1–B.3 quantify the three complications that a progressive rate schedule introduces to the Domar-Musgrave architecture, corresponding to the analysis in (WFR §4.1). All three complications are real; all three are second-order at canonical parameters. The logistic rate function uses $\tau_0$=15%, $\tau_m$=70%, k=0.001, $W_{min}$=£2m throughout this section unless noted.

## B.1 Flat WDT vs Progressive WDT CEW

C1 complication: under a progressive rate, the government co-investment share varies with wealth level, breaking the flat D-M result. Gap (bp) = (CEW_flat − CEW_progressive) × 10,000; positive means flat WDT produces lower welfare cost. $W_0$ = 5 × $W_{min}$ = £10m for both distributions.

| Distribution | γ | Flat WDT CEW | Progressive WDT CEW | Gap (bp) | E[T] progressive |
|:---|---:|---:|---:|---:|---:|
| Ver. A | 1.0 | -0.8197% | -0.8197% | -0.00 | £0.0904m |
| Ver. A | 2.0 | -0.7865% | -0.7865% | -0.00 | £0.0904m |
| Ver. A | 4.0 | -0.7205% | -0.7205% | -0.00 | £0.0904m |
| Ver. B | 1.0 | -0.8195% | -0.8195% | -0.00 | £0.0904m |
| Ver. B | 2.0 | -0.7858% | -0.7858% | -0.00 | £0.0904m |
| Ver. B | 4.0 | -0.7191% | -0.7191% | -0.00 | £0.0904m |

## B.2 Leverage Effect on WDT Tax Base and Welfare

C2 complication: when an agent holds gross assets A with outstanding debt D, net worth W = A − D and the WDT taxes the amplified (or dampened) net-worth delta rather than the underlying asset return. NW base = actual WDT base (ΔW = A×R − D − $W_0$); asset-return base = hypothetical alternative taxing only A×(R−1). The two bases are identical at zero leverage and diverge as D/A rises. Gap (bp) = (CEW_NW − CEW_AR) × 10,000; positive means the WDT's NW base produces higher welfare than the asset-return alternative at the same rate. Gross assets = £10m (5×$W_{min}$). Progressive rate function. γ=2. Ver. A distribution.

| Leverage (%) | $W_0$ net (£m) | E[T] NW base | E[T] asset-rtn base | CEW NW base | CEW asset-rtn base | Gap (bp) |
|---:|---:|---:|---:|---:|---:|---:|
| 0.0 | £10.00m | 0.0904 | 0.0904 | -0.7865% | -0.7865% | +0.00 |
| 5.0 | £9.50m | 0.0904 | 0.0904 | -0.8219% | -0.8222% | +0.03 |
| 10.0 | £9.00m | 0.0903 | 0.0904 | -0.8606% | -0.8612% | +0.07 |
| 15.0 | £8.50m | 0.0903 | 0.0904 | -0.9031% | -0.9042% | +0.11 |
| 20.0 | £8.00m | 0.0903 | 0.0904 | -0.9501% | -0.9516% | +0.15 |
| 25.0 | £7.50m | 0.0902 | 0.0904 | -1.0022% | -1.0042% | +0.20 |
| 30.0 | £7.00m | 0.0902 | 0.0904 | -1.0604% | -1.0629% | +0.25 |
| 35.0 | £6.50m | 0.0902 | 0.0904 | -1.1257% | -1.1288% | +0.31 |
| 40.0 | £6.00m | 0.0901 | 0.0904 | -1.1995% | -1.2033% | +0.38 |
| 45.0 | £5.50m | 0.0901 | 0.0904 | -1.2836% | -1.2882% | +0.46 |
| 50.0 | £5.00m | 0.0901 | 0.0904 | -1.3801% | -1.3856% | +0.55 |
| 55.0 | £4.50m | 0.0900 | 0.0904 | -1.4920% | -1.4985% | +0.65 |
| 60.0 | £4.00m | 0.0900 | 0.0904 | -1.6228% | -1.6306% | +0.78 |
| 65.0 | £3.50m | 0.0900 | 0.0904 | -1.7771% | -1.7863% | +0.93 |
| 70.0 | £3.00m | 0.0899 | 0.0904 | -1.9602% | -1.9712% | +1.10 |

## B.3 Two-Period Rate Asymmetry by Initial Wealth

C3 complication: under a progressive schedule, a gain in period 1 increases wealth and attracts a higher effective rate than the refund received in period 2 on an equivalent loss, because the loss is assessed at the lower post-gain wealth level. Sequence: +18.8% gain (μ+σ) in period 1, −8.3% loss (σ) in period 2. $\tau$ gain = effective rate on the period-1 delta at ($W_0$, W₁). $\tau$ refund = effective rate on the period-2 loss at (W₁, W₂). Asymmetry = $\tau$ gain − $\tau$ refund (pp); positive means the gain is taxed at a higher rate than the equivalent loss. Excess = net tax progressive − net tax flat; negative means progression collects less than the flat revenue-equivalent rate.

| $W_0$ (£m) | $\tau$ gain (%) | $\tau$ refund (%) | Asymmetry (pp) | Net tax: progressive | Net tax: flat | Excess |
|---:|---:|---:|---:|---:|---:|---:|
| 3.0 | 15.015 | 15.014 | +0.0011 | £0.0411m | £0.0943m | -0.0532 |
| 4.0 | 15.028 | 15.027 | +0.0015 | £0.0549m | £0.1258m | -0.0709 |
| 10.0 | 15.106 | 15.102 | +0.0037 | £0.1379m | £0.3144m | -0.1765 |
| 20.0 | 15.236 | 15.228 | +0.0074 | £0.2783m | £0.6288m | -0.3505 |
| 40.0 | 15.498 | 15.483 | +0.0153 | £0.5667m | £1.2575m | -0.6908 |
| 100.0 | 16.305 | 16.263 | +0.0415 | £1.4950m | £3.1438m | -1.6488 |
| 200.0 | 17.713 | 17.619 | +0.0946 | £3.2656m | £6.2876m | -3.0220 |

The Excess column is uniformly negative because the tested wealth levels sit in the near-flat entry region of the logistic, well below the inflection point, where effective rates barely exceed $\tau_0$. A progressive schedule operating in this region collects less net tax than the flat rate calibrated to the same revenue target. The gain-at-higher-rate asymmetry that textbook bracket analysis would predict requires wealth to sit at or above the logistic inflection point, which the canonical population does not reach.

\newpage

# C. CGT Lock-In Distortion

Reference parameters throughout this section: V=£10m, G/V=50%, r_A=10.45% (empirical equity mean from JST dataset), $\tau_{cgt}$=24% (UK 2024 higher rate), T=5 years remaining. Tables C.1–C.3 correspond to the lock-in analysis in (WFR §4.2).

## C.1 Lock-In Welfare Cost by Embedded Gain Ratio

Lock-in cost (bp) = (CEW_free − CEW_locked) × 10,000. CEW_free: agent switches whenever r_B > r_A (no lock-in). CEW_locked: agent locked in under CGT when r_B < indifference return r_B*. P(locked in) includes two components: states where r_B < r_A (agent stays regardless of CGT — fundamental market preference, not a tax distortion) and states where r_A ≤ r_B < r_B* (CGT lock-in distortion proper — agent would switch without CGT but the switching cost exceeds the benefit). The welfare cost is attributable to the second component only; the first component is present with or without CGT. Ver. A distribution. γ=2.

| G/V (%) | CEW (free) | CEW (locked) | Lock-in cost (bp) | P(total locked) | P(CGT distortion) | P(r_B < r_A) |
|---:|---:|---:|---:|---:|---:|---:|
| 5.0 | 5.0343% | 4.8704% | +16.39 | 86.7% | 0.0% | 86.7% |
| 9.5 | 5.0343% | 4.7208% | +31.35 | 86.7% | 0.0% | 86.7% |
| 13.9 | 5.0343% | 4.5683% | +46.60 | 86.7% | 0.0% | 86.7% |
| 18.4 | 5.0343% | 4.4129% | +62.15 | 86.7% | 0.0% | 86.7% |
| 22.9 | 5.0343% | 4.2543% | +78.00 | 86.7% | 0.0% | 86.7% |
| 27.4 | 5.0343% | 4.0927% | +94.17 | 86.7% | 0.0% | 86.7% |
| 31.8 | 5.0343% | 3.9278% | +110.66 | 86.7% | 0.0% | 86.7% |
| 36.3 | 5.0343% | 4.0239% | +101.05 | 90.0% | 3.3% | 86.7% |
| 40.8 | 5.0343% | 3.8954% | +113.89 | 90.0% | 3.3% | 86.7% |
| 45.3 | 5.0343% | 3.7642% | +127.01 | 90.0% | 3.3% | 86.7% |
| 49.7 | 5.0343% | 3.6302% | +140.42 | 90.0% | 3.3% | 86.7% |
| 54.2 | 5.0343% | 3.9006% | +113.37 | 93.3% | 6.7% | 86.7% |
| 58.7 | 5.0343% | 3.8075% | +122.68 | 93.3% | 6.7% | 86.7% |
| 63.2 | 5.0343% | 3.7122% | +132.21 | 93.3% | 6.7% | 86.7% |
| 67.6 | 5.0343% | 3.6146% | +141.97 | 93.3% | 6.7% | 86.7% |
| 72.1 | 5.0343% | 3.5147% | +151.96 | 93.3% | 6.7% | 86.7% |
| 76.6 | 5.0343% | 3.4124% | +162.19 | 93.3% | 6.7% | 86.7% |
| 81.1 | 5.0343% | 3.9658% | +106.86 | 96.7% | 10.0% | 86.7% |
| 85.5 | 5.0343% | 3.9124% | +112.20 | 96.7% | 10.0% | 86.7% |
| 90.0 | 5.0343% | 3.8576% | +117.68 | 96.7% | 10.0% | 86.7% |

The non-monotonicity above G/V = 81% is a discretisation artefact: as r_B* rises with the embedded gain, it approaches the upper boundary of the empirical return distribution and the probability of any return state exceeding r_B* shrinks rapidly. States that were generating lock-in costs are absorbed into the P(r_B < r_A) category. This is a boundary effect of the finite empirical distribution and should not be read as evidence that lock-in costs decline at very high embedded gain ratios.

## C.2 Lock-In Welfare Cost by Remaining Holding Period

G/V=50% fixed. T varies from 1 to 20 years. The lock-in cost rises from T=1 and plateaus at longer horizons. At T=1 the agent has only one period in which to benefit from switching to B, so the opportunity cost of lock-in is low. Each additional year that asset B compounds ahead of asset A raises the foregone return from remaining locked in. The plateau appears as r_B* converges toward r_A and the trapped zone (r_A ≤ r_B < r_B*) collapses — states that triggered lock-in at short T now fall below r_A (agent stays regardless) or above r_B* (agent switches). Indifference return r_B* converges to r_A as T→∞, confirming lock-in eventually disappears at infinite horizons; but across all empirically relevant horizons (T ≤ 20 yr) the welfare cost is substantially above the T=1 baseline.

| T (years) | r_B* (%) | Lock-in cost (bp) | P(total locked) | P(CGT distortion) | P(r_B < r_A) |
|---:|---:|---:|---:|---:|---:|
| 1 | 25.5114% | +56.11 | 100.0% | 13.3% | 86.7% |
| 2 | 17.7401% | +73.27 | 96.7% | 10.0% | 86.7% |
| 3 | 15.2581% | +73.27 | 96.7% | 10.0% | 86.7% |
| 4 | 14.0368% | +104.80 | 93.3% | 6.7% | 86.7% |
| 5 | 13.3102% | +141.22 | 90.0% | 3.3% | 86.7% |
| 6 | 12.8284% | +141.22 | 90.0% | 3.3% | 86.7% |
| 7 | 12.4856% | +141.22 | 90.0% | 3.3% | 86.7% |
| 8 | 12.2291% | +181.13 | 86.7% | 0.0% | 86.7% |
| 9 | 12.0300% | +181.13 | 86.7% | 0.0% | 86.7% |
| 10 | 11.8710% | +181.13 | 86.7% | 0.0% | 86.7% |
| 11 | 11.7411% | +181.13 | 86.7% | 0.0% | 86.7% |
| 12 | 11.6329% | +181.13 | 86.7% | 0.0% | 86.7% |
| 13 | 11.5414% | +181.13 | 86.7% | 0.0% | 86.7% |
| 14 | 11.4631% | +181.13 | 86.7% | 0.0% | 86.7% |
| 15 | 11.3953% | +181.13 | 86.7% | 0.0% | 86.7% |
| 16 | 11.3360% | +181.13 | 86.7% | 0.0% | 86.7% |
| 17 | 11.2837% | +181.13 | 86.7% | 0.0% | 86.7% |
| 18 | 11.2372% | +181.13 | 86.7% | 0.0% | 86.7% |
| 19 | 11.1956% | +181.13 | 86.7% | 0.0% | 86.7% |
| 20 | 11.1582% | +181.13 | 86.7% | 0.0% | 86.7% |

## C.3 Full Welfare Comparison: WDT vs CGT (With and Without Lock-In)

Section A showed WDT $\approx$ CGT when lock-in was absent. This table adds the lock-in cost to CGT, correcting that comparison. WDT advantage (with lock-in) = CEW_WDT − CEW_CGT_locked.

| Metric | Ver. A (Empirical) | Ver. B (Idealised) |
|:---|---:|---:|
| WDT CEW | -1.7539% | -1.7525% |
| CGT CEW (no lock-in) | -1.7713% | -1.7525% |
| Lock-in welfare cost | +141.22 bp | +41.19 bp |
| CGT CEW (with lock-in) | -3.1834% | -2.1644% |
| WDT advantage (no lock-in) | +1.74 bp | +0.00 bp |
| WDT advantage (with lock-in) | +142.96 bp | +41.19 bp |
| P(agent locked in) | 90.0% | 100.0% |
| CGT indifference return r_B* | 13.3102% | 13.3102% |
| Revenue-equivalent CGT rate | 32.0667% | 33.4039% |

\newpage

# D. Heterogeneous Agents — Incidence and Concentration

Tier return differentials from Fagereng et al. (2020): Poor −4.55pp, Ok −2.05pp, Good +0.95pp, Great +3.45pp, relative to the UK historical equity mean of 10.45%. Ver. A distribution with tier-shifted returns. γ=2. Tables D.1–D.5 correspond to the heterogeneous-agent analysis in (WFR §4.3).

Tier wealth levels: Poor (95th percentile) $W_0$=£2.9m; Ok (99th) $W_0$=£7.1m; Good (99.9th) $W_0$=£19.9m; Great (99.99th+) $W_0$=£139.6m. Progressive WDT uses logistic rate function with $\tau_0$=15%, $\tau_m$=70%, k=0.001, $W_{min}$=£2m. All flat-rate systems calibrated at revenue-equivalent rates producing E[T] = 2% of Good-tier $W_0$.

## D.1 CEW by Tier and Tax System

| System | Poor (95%, $W_0$=£2.9m) | Ok (99%, $W_0$=£7.1m) | Good (99.9%, $W_0$=£19.9m) | Great (99.99%+, $W_0$=£139.6m) |
|:---|---:|---:|---:|---:|
| Symmetric WDT | -0.2194% | -0.7816% | -1.4211% | -1.9269% |
| Stock Wealth Tax | -1.8424% | -1.8424% | -1.8424% | -1.8424% |
| Income Tax | -0.6000% | -0.9274% | -1.4413% | -1.9161% |
| CGT | -0.6000% | -0.9274% | -1.4413% | -1.9161% |
| Consumption Tax | -1.8424% | -1.8424% | -1.8424% | -1.8424% |
| Progressive WDT | -0.1375% | -0.5004% | -0.9223% | -1.3814% |

## D.2 Distributional Incidence: Expected Tax as % of $W_0$

E[T] / $W_0$ × 100. All systems calibrated to the same aggregate revenue target. Rates differ across tiers because shifted return distributions change E[T]. Progressive WDT incidence is captured via the CEW column in D.1 rather than a simple rate.

| System | Poor (95%, $W_0$=£2.9m) | Ok (99%, $W_0$=£7.1m) | Good (99.9%, $W_0$=£19.9m) | Great (99.99%+, $W_0$=£139.6m) |
|:---|---:|---:|---:|---:|
| Symmetric WDT | 0.3362% | 0.9208% | 1.6225% | 2.2071% |
| Stock Wealth Tax | 1.8689% | 1.9150% | 1.9703% | 2.0163% |
| Income Tax | 0.6779% | 1.0489% | 1.6348% | 2.1903% |
| CGT | 0.6779% | 1.0489% | 1.6348% | 2.1903% |
| Consumption Tax | 1.8689% | 1.9150% | 1.9703% | 2.0163% |

## D.3 Wealth Concentration Path: Great/Poor Ratio at Key Years

Great-tier wealth / Poor-tier wealth at selected years. All systems calibrated at the population-weighted aggregate rate from D.2 (same target as the B and C welfare comparisons). Progressive WDT uses the logistic rate function directly. The initial ratio of 48.8× reflects the $W_0$ difference only (£139.6m / £2.9m). Return heterogeneity compounds over a 30-year scenario horizon starting in 2000.

| System | Initial | 2004 | 2009 | 2019 | 2029 |
|:---|---:|---:|---:|---:|---:|
| Symmetric WDT | 48.8× | 65.1× | 87.4× | 157.2× | 286.3× |
| Progressive WDT | 48.8× | 66.1× | 90.3× | 162.3× | 288.1× |
| Stock Wealth Tax | 48.8× | 70.5× | 103.3× | 220.1× | 479.0× |
| Income Tax | 48.8× | 65.5× | 90.2× | 166.1× | 320.2× |
| Consumption Tax | 48.8× | 70.5× | 103.3× | 220.1× | 479.0× |

## D.4 Lifetime Contribution Envelope: Binding Summary

The envelope binds when cumulative refunds would exceed cumulative taxes paid to date. Refunds are capped at cumulative taxes paid when binding occurs. Min slack = minimum of (cumulative tax − cumulative refund) over the scenario window; zero means the envelope was exactly reached but not exceeded.

The Poor-tier binding in 2001 — the first assessment year — is the concrete numerical realisation of the ENV paper's SRR early-year funding gap. The Poor tier's −4.55pp return differential produces a loss in the first scenario year before any cumulative tax has been paid, so the refund that would be owed exceeds the cumulative contribution to date. The envelope floor binds and the refund is capped at zero. The policy implication is that the SRR must be pre-funded from non-WDT sources to honour refunds in early years for low-return-tier entrants — or the entry-year assessment must provide an initial credit against future taxes. This result holds for the 2000-start sequence; the full start-year distribution is examined in Section E.2.

| Tier | Bracket | $W_0$ (£m) | Cumulative tax (£m) | Cumulative refund (£m) | Min slack (£m) | Binding years | Ever binds? |
|:---|:---|---:|---:|---:|---:|:---:|:---:|
| Poor | 95% | £2.9m | £0.473m | £0.270m | £0.0000m | 2001 | ⚠ Yes |
| Ok | 99% | £7.1m | £2.440m | £0.398m | £0.0423m | — | No |
| Good | 99.9% | £19.9m | £16.503m | £0.310m | £0.2097m | — | No |
| Great | 99.99%+ | £139.6m | £330.303m | £1.423m | £2.2100m | — | No |

## D.5 Off-Diagonal Spot Check: Decoupling $W_0$ from Return Differential

Corner A: Great return differential (+3.45pp) applied at Poor-tier $W_0$ (£2.86m). Corner B: Poor return differential (−4.55pp) applied at Great-tier $W_0$ (£139.6m). These are the two extreme off-diagonal cells of the 4-tier × 4-bracket grid, sufficient to bound the interaction without computing all 16 combinations. Diagonal (same $W_0$) = the standard result for the tier sharing this corner's wealth level. Diagonal (same diff) = the standard result for the tier sharing this corner's return differential. Δ vs same-$W_0$ (bp) = (Corner CEW − Diagonal same-$W_0$ CEW) × 10,000: positive means decoupling the differential upward improves welfare. Revenue target = 2% of each corner's own $W_0$ (per-corner solve, not aggregate). γ=2. Ver. A distribution.

| Corner / System | Corner CEW | Diagonal (same $W_0$) | Diagonal (same diff) | Δ vs same-$W_0$ (bp) |
|:---|---:|---:|---:|---:|
| **Corner A: Great diff (+3.45pp), Poor $W_0$ (£2.86m)** |  |  |  |  |
|   Symmetric WDT | -1.7451% | -0.2194% | -1.9269% | -152.58 |
|   Stock Wealth Tax | -1.8275% | -1.8424% | -1.8424% | +1.49 |
|   Income Tax | -1.7488% | -0.6000% | -1.9161% | -114.88 |
|   CGT | -1.7488% | -0.6000% | -1.9161% | -114.88 |
|   Consumption Tax | -1.8275% | -1.8424% | -1.8424% | +1.49 |
|   Progressive WDT | -1.2343% | -0.1375% | -1.3814% | -109.69 |
|  |  |  |  |  |
| **Corner B: Poor diff (−4.55pp), Great $W_0$ (£139.6m)** |  |  |  |  |
|   Symmetric WDT | — | -1.9269% | -0.2194% | — |
|   Stock Wealth Tax | -1.9717% | -1.8424% | -1.8424% | -12.92 |
|   Income Tax | -1.8049% | -1.9161% | -0.6000% | +11.12 |
|   CGT | -1.8049% | -1.9161% | -0.6000% | +11.12 |
|   Consumption Tax | -1.9717% | -1.8424% | -1.8424% | -12.92 |
|   Progressive WDT | -0.1568% | -1.3814% | -0.1375% | +122.46 |

The "—" entry for Corner B Symmetric WDT requires explanation. At Great-tier initial wealth of £139.6m with the Poor-tier return differential of −4.55pp, the flat symmetric WDT generates expected refunds large enough that the aggregate revenue target cannot be reached within the feasible rate space $\tau$ ∈ (0, 0.999]. The revenue-equivalence solver fails to converge: no flat rate can collect E[T] = 2% of $W_0$ in expectation when the refund commitment at any positive rate exceeds the collection in gain states by this margin. This is a solver boundary condition reflecting a parameter combination outside the feasible calibration space, not a model failure. The cell is undefined for the flat symmetric WDT; all other systems have solutions here because they either pay no refunds or (in the case of progressive WDT) apply a low enough effective entry rate that the revenue target remains reachable.

\newpage

# E. Welfare Sweep Analysis

Three independent sweep axes: Sweep A varies the revenue target from 1% to 5% of $W_0$; Sweep B examines worst-case outcomes across all 73 historical 30-year windows (1947–2019); Sweep C measures the progressive-vs-flat WDT welfare gap across logistic rate parameters. All sweeps use γ=2 as the central case unless noted. Tables E.1–E.3.4 correspond to the robustness analysis in (WFR §4) and the sweep results reported throughout that section.

## E.1 Sweep A: CEW by System and Revenue Target (γ=2)

E[T] as % of $W_0$ swept from 1% to 5%. Columns = revenue target; rows grouped by distribution. Rankings that hold across the full range are structurally robust; rankings that flip signal revenue-sensitivity. γ=2. $W_0$=1.0 (normalised).

| Distribution | System | E[T]=1% | E[T]=2% | E[T]=3% | E[T]=4% | E[T]=5% |
|:---|:---|---:|---:|---:|---:|---:|
| Ver. A | Symmetric WDT | -0.8705% | -1.7539% | -2.6504% | -3.5605% | -4.4846% |
| Ver. A | Stock Wealth Tax | -0.9435% | -1.8870% | -2.8305% | -3.7740% | -4.7175% |
| Ver. A | Income Tax | -0.8809% | -1.7713% | -2.6715% | -3.5821% | -4.5033% |
| Ver. A | CGT | -0.8809% | -1.7713% | -2.6715% | -3.5821% | -4.5033% |
| Ver. A | Consumption Tax | -0.9435% | -1.8870% | -2.8305% | -3.7740% | -4.7175% |
|  |  |  |  |  |  |  |
| Ver. B | Symmetric WDT | -0.8698% | -1.7525% | -2.6486% | -3.5585% | -4.4826% |
| Ver. B | Stock Wealth Tax | -0.9435% | -1.8870% | -2.8305% | -3.7740% | -4.7175% |
| Ver. B | Income Tax | -0.8698% | -1.7525% | -2.6486% | -3.5585% | -4.4826% |
| Ver. B | CGT | -0.8698% | -1.7525% | -2.6486% | -3.5585% | -4.4826% |
| Ver. B | Consumption Tax | -0.9435% | -1.8870% | -2.8305% | -3.7740% | -4.7175% |

### E.1.1 — Sweep A: CEW by System and Initial Wealth W₀ (γ=2)

*E[T] fixed at 2% of W₀; W₀ swept across the wealth-tier range. CEW is invariant to W₀ under this fixed-percentage design — the flat-rate revenue-equivalence normalisation holds the relative burden constant regardless of wealth level. Confirms the flat series in Figure 4.5.1b. γ=2. Ver. A distribution.*

| System | W₀=£3m | W₀=£5m | W₀=£8m | W₀=£10m | W₀=£20m | W₀=£30m | W₀=£50m | W₀=£100m | W₀=£150m |
|:---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Symmetric WDT | -1.7539% | -1.7539% | -1.7539% | -1.7539% | -1.7539% | -1.7539% | -1.7539% | -1.7539% | -1.7539% |
| Stock Wealth Tax | -1.8870% | -1.8870% | -1.8870% | -1.8870% | -1.8870% | -1.8870% | -1.8870% | -1.8870% | -1.8870% |
| Income Tax | -1.7713% | -1.7713% | -1.7713% | -1.7713% | -1.7713% | -1.7713% | -1.7713% | -1.7713% | -1.7713% |
| CGT | -1.7713% | -1.7713% | -1.7713% | -1.7713% | -1.7713% | -1.7713% | -1.7713% | -1.7713% | -1.7713% |
| Consumption Tax | -1.8870% | -1.8870% | -1.8870% | -1.8870% | -1.8870% | -1.8870% | -1.8870% | -1.8870% | -1.8870% |

## E.2 Sweep B: CEW by Start Year (γ=2)

### E.2.1 Sweep B: Summary Statistics Across All Start Years

Min/median/mean/max CEW across all 73 start-year windows (1947–2019). "WDT best?" = fraction of windows in which the Symmetric WDT has the highest CEW (lowest welfare cost) of the five systems. E[T] = 2% of $W_0$. γ=2. Ver. A distribution.

| System | Min CEW | Median CEW | Mean CEW | Max CEW | WDT best? (% of windows) |
|:---|---:|---:|---:|---:|---:|
| Symmetric WDT | -1.7647% | -1.6727% | -1.6697% | -1.5870% | 100.0% |
| Stock Wealth Tax | -1.8936% | -1.8144% | -1.8125% | -1.7314% | — |
| Income Tax | -1.7713% | -1.6751% | -1.6765% | -1.5881% | — |
| CGT | -1.7713% | -1.6751% | -1.6765% | -1.5881% | — |
| Consumption Tax | -1.8936% | -1.8144% | -1.8125% | -1.7314% | — |

### E.2.2 Sweep B: Curated Worst-Case Start Years

Six historically adverse start years plus the canonical 2000 (◄). Adverse years selected: 1972 (oil shock), 1987 (Black Monday), 1999 (GFC in window), 2000 (dot-com + GFC), 2006 (worst LRR fill speed). WDT adv. = (CEW_WDT − CEW_StockWealth) × 10,000 in basis points.

| Start year | Symmetric WDT | Stock Wealth Tax | Income Tax | CGT | Consumption Tax | WDT adv. vs Stock (bp) |
|:---|---:|---:|---:|---:|---:|---:|
| 1972 | -1.6260% | -1.7439% | -1.6262% | -1.6262% | -1.7439% | +11.8 |
| 1987 | -1.6975% | -1.8252% | -1.7103% | -1.7103% | -1.8252% | +12.8 |
| 1999 | -1.7411% | -1.8790% | -1.7583% | -1.7583% | -1.8790% | +13.8 |
| 2000 ◄ canonical | -1.7539% | -1.8870% | -1.7713% | -1.7713% | -1.8870% | +13.3 |
| 2006 | -1.7445% | -1.8907% | -1.7625% | -1.7625% | -1.8907% | +14.6 |

## E.3 Sweep C: CEW Parameter Sensitivy Sweep

### E.3.1 Sweep C: $\tau_0$ Sensitivity

Gap (bp) = (CEW_flat − CEW_progressive) × 10,000. Positive = flat WDT has lower welfare cost than progressive. $\tau_m$, $k$,$W_{min}$ held at canonical values.

| $\tau_0$ (entry rate) | $W_0$=£10m | $W_0$=£30m | $W_0$=£100m |
|:---|---:|---:|---:|
| 0.05 | -0.00 | -0.00 | -0.01 |
| 0.1 | -0.00 | -0.00 | -0.01 |
| 0.15 | -0.00 | -0.00 | -0.01 |
| 0.2 | -0.00 | -0.00 | -0.01 |
| 0.25 | -0.00 | -0.00 | -0.01 |
| 0.3 | -0.00 | -0.00 | -0.00 |

### E.3.2 Sweep C: $\tau_m$ Sensitivity

$\tau_0$, $k$,$W_{min}$ held at canonical values.

| $\tau_m$ (ceiling rate) | $W_0$=£10m | $W_0$=£30m | $W_0$=£100m |
|:---|---:|---:|---:|
| 0.4 | -0.00 | -0.00 | -0.00 |
| 0.5 | -0.00 | -0.00 | -0.01 |
| 0.6 | -0.00 | -0.00 | -0.01 |
| 0.7 | -0.00 | -0.00 | -0.01 |
| 0.8 | -0.00 | -0.00 | -0.01 |
| 0.9 | -0.00 | -0.00 | -0.01 |

### E.3.3 Sweep C: $k$ Sensitivity

$\tau_0$, $\tau_m$, $W_{min}$ held at canonical values.

| $k$ (steepness per £m) | $W_0$=£10m | $W_0$=£30m | $W_0$=£100m |
|:---|---:|---:|---:|
| 0.0001 | -0.00 | -0.00 | -0.00 |
| 0.0005 | -0.00 | -0.00 | -0.00 |
| 0.001 | -0.00 | -0.00 | -0.01 |
| 0.005 | -0.00 | -0.01 | -0.03 |
| 0.01 | -0.01 | -0.02 | -0.05 |
| 0.05 | -0.03 | -0.05 | +0.00 |

### E.3.4 Sweep C: $W_{min}$ Sensitivity

$\tau_0$, $\tau_m$, $k$ held at canonical values.

| $W_{min}$ (£m) | $W_0$=£10m | $W_0$=£30m | $W_0$=£100m |
|:---|---:|---:|---:|
| 0.5 | -0.00 | -0.00 | -0.01 |
| 1.0 | -0.00 | -0.00 | -0.01 |
| 2.0 | -0.00 | -0.00 | -0.01 |
| 5.0 | -0.00 | -0.00 | -0.01 |
| 10.0 | +1.74 | -0.00 | -0.01 |

\newpage

---

## F. Extended Concentration Horizon (N=73)

### F.1 — Setup and Scope
Same tiers, systems, and revenue-equivalent rates as D. Heterogeneous Agents — only the horizon extends from the canonical N=30 scenario window (2000-2029, wrap-around) to the full N=73 historical sequence, run chronologically from 1947 to 2019 with no rotation. Rates are carried forward from D — not re-solved at N=73 — because the question is what happens to concentration if the same calibrated system runs longer, not what rate a 73-year revenue target would imply.

### F.2 — Extended Concentration Path (Key Years)

*Great/Poor wealth ratio at selected years across the full 1947-2019 sequence. 2000 and 2019 anchor points allow comparison against the D.3 N=30 window (2000-2029); D.3's 2029 endpoint falls outside the 1947-2019 series and is not repeated here.*

| System | Initial | 1957 | 1967 | 1977 | 1987 | 1997 | 2000 | 2007 | 2019 |
|:---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Flat WDT | 48.8× | 94.5× | 167.9× | 290.7× | 500.5× | 882.6× | 1,045.6× | 1,558.3× | 3,173.2× |
| Progressive WDT | 48.8× | 99.8× | 175.4× | 222.3× | 169.6× | 152.5× | 146.2× | 138.7× | 177.8× |
| Stock Wealth Tax | 48.8× | 115.1× | 240.2× | 481.9× | 956.5× | 1,974.6× | 2,451.0× | 4,082.9× | 10,239.8× |
| Income Tax | 48.8× | 100.9× | 181.8× | 320.8× | 553.5× | 998.3× | 1,183.6× | 1,776.0× | 3,793.5× |
| Consumption Tax | 48.8× | 115.1× | 240.2× | 481.9× | 956.5× | 1,974.6× | 2,451.0× | 4,082.9× | 10,239.8× |

### F.3 — Flat vs Progressive WDT: Crossover Horizon

*At N=30, progressive WDT shows marginally HIGHER Great/Poor concentration than flat WDT (D.3; the logistic operates near its entry rate at canonical wealth levels, so progression barely bites). This table reports whether and when that inverts at longer horizons.*

| Metric | Value |
|:---|---:|
| Great/Poor ratio: Flat WDT at N=30 | 286.3× |
| Great/Poor ratio: Progressive WDT at N=30 | 288.1× |
| Gap at N=30 (Progressive − Flat) | +1.8× |
| Great/Poor ratio: Flat WDT at N=73 | 3,173.2× |
| Great/Poor ratio: Progressive WDT at N=73 | 177.8× |
| Gap at N=73 (Progressive − Flat) | -2995.4× |
| First year Progressive WDT ratio < Flat WDT ratio | 1971 |
| Gap at crossover year | -1.34× |

### F.4 — All-Tier Concentration Matrix at N=73

*Great/Poor, Great/Ok, and Ok/Poor wealth ratios at the N=73 terminal horizon, analogous to D.3 but at the extended horizon — shows where across the tier structure any progressive-vs-flat divergence concentrates.*

| System | Great/Poor | Great/Ok | Ok/Poor |
|:---|---:|---:|---:|
| Flat WDT | 3,173.2× | 336.1× | 9.4× |
| Progressive WDT | 177.8× | 18.5× | 9.6× |
| Stock Wealth Tax | 10,239.8× | 739.6× | 13.8× |
| Income Tax | 3,793.5× | 358.5× | 10.6× |
| Consumption Tax | 10,239.8× | 739.6× | 13.8× |

---

## G. Parameter Reference

| Parameter | Value | Source |
|:---|---:|:---|
| W₀ (normalised A. Module 1) | 1.0 | — |
| Revenue target E[T] | 2% of W₀ | — |
| γ (central case) | 2.0 | Flavin & Yamashita (2002) |
| $\tau_0$ (WDT entry rate) | 15% | TOML [rate] |
|  $\tau_m$  (WDT ceiling) | 70% | TOML [rate] |
| k (logistic steepness) | 0.001 | TOML [rate] |
| W_min (£m) | £2m | TOML [rate] |
| UK equity mean (1947–2019) | 10.45% | JST dataset |
| UK equity std dev | 8.31% | JST dataset |

\newpage