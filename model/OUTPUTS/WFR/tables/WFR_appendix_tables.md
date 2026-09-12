# WFR Welfare Comparison Model — Appendix Tables

*Generated: 2026-09-10*
*Revenue target: E[T] = 2% of W₀ across all systems.*
*All CEW values relative to no-tax benchmark. Positive = welfare-superior to no-tax.*

---

## A. Baseline Single-Agent Comparison

### A.1 — Consumption-Equivalent Welfare (CEW) by system, γ, and distribution

*CEW = proportional consumption change under no-tax making agent indifferent to the taxed system. Negative = welfare cost relative to no-tax. Ver. A = UK historical equity (73 obs, 1947–2019). Ver. B = idealised two-state (p=0.5, R_good=E[R]+σ, R_bad=E[R]−σ).*

| System | Ver. B γ=1 | Ver. B γ=2 | Ver. B γ=4 | Ver. B γ=1 | Ver. B γ=2 | Ver. B γ=4 |
|:---|---:|---:|---:|---:|---:|---:|
| Symmetric WDT | -1.8203% | -1.7539% | -1.6217% | -1.8198% | -1.7525% | -1.6188% |
| Stock Wealth Tax | -1.8870% | -1.8870% | -1.8870% | -1.8870% | -1.8870% | -1.8870% |
| Income Tax | -1.8288% | -1.7713% | -1.6583% | -1.8198% | -1.7525% | -1.6188% |
| CGT | -1.8288% | -1.7713% | -1.6583% | -1.8198% | -1.7525% | -1.6188% |
| Consumption Tax | -1.8870% | -1.8870% | -1.8870% | -1.8870% | -1.8870% | -1.8870% |

*Note: Income Tax and CGT show identical CEW and identical revenue-equivalent rates throughout this table. This is correct by construction: A. Module 1 models CGT as a gains-only tax with the same base as income tax and no realisation decision. The two systems are structurally identical in a single-period model where all gains are realised each period. The lock-in distortion that separates CGT from income tax in practice is endogenous and enters only in C. Module 3, where it generates the largest welfare difference in the model.*

### A.2 — Variance of Consumption by system (γ=2)

*Variance of consumption across return states at revenue-equivalent rates. Lower variance indicates greater risk-sharing. D-M prediction: Var(C_sym) = (1−τ)² × Var(C_notax).*

| System | Ver. A Var(C) | Ver. B Var(C) |
|:---|---:|---:|
| Symmetric WDT | 0.0013 | 0.0013 |
| Stock Wealth Tax | 0.0027 | 0.0027 |
| Income Tax | 0.0014 | 0.0013 |
| CGT | 0.0014 | 0.0013 |
| Consumption Tax | 0.0027 | 0.0027 |

### A.3 — Revenue-Equivalent Tax Rates (γ=2)

*Rate τ* such that E[T(W₀, dist, τ*)] = target. Rates differ across systems because tax bases differ. Stock wealth and consumption taxes require low rates (broad base); income tax and CGT require higher rates (gains only, no collection in loss states).*

| System | Ver. A rate (τ*) | Ver. B rate (τ*) |
|:---|---:|---:|
| Symmetric WDT | 33.404% | 33.404% |
| Stock Wealth Tax | 1.887% | 1.887% |
| Income Tax | 32.067% | 33.404% |
| CGT | 32.067% | 33.404% |
| Consumption Tax | 1.923% | 1.923% |

### A.4 — Domar–Musgrave Test: Symmetric WDT

*Prediction: Var(C_tax) / Var(C_notax) = (1−τ)². Gap near zero confirms D-M holds for the flat-rate symmetric case. Progression breaks D-M — see B. Module 2.*

| Distribution | γ | τ (WDT) | (1−τ)² | Actual ratio | Gap | Holds? |
|:---|---:|---:|---:|---:|---:|:---:|
| Ver. B | 1.0 | 33.4039% | 0.443505 | 0.443505 | -5.55e-17 | ✓ |
| Ver. B | 2.0 | 33.4039% | 0.443505 | 0.443505 | -5.55e-17 | ✓ |
| Ver. B | 4.0 | 33.4039% | 0.443505 | 0.443505 | -5.55e-17 | ✓ |
| Ver. B | 1.0 | 33.4039% | 0.443505 | 0.443505 | 9.44e-16 | ✓ |
| Ver. B | 2.0 | 33.4039% | 0.443505 | 0.443505 | 9.44e-16 | ✓ |
| Ver. B | 4.0 | 33.4039% | 0.443505 | 0.443505 | 9.44e-16 | ✓ |

---

## B. Progressive Rates and the Three D-M Complications

### B.1 — Flat WDT vs Progressive WDT CEW

*C1 complication: under a progressive rate, the government co-investment share varies with wealth level, breaking the flat D-M result. Gap (bp) = (CEW_flat − CEW_progressive) × 10,000. Positive = flat WDT better. W₀ = 5 × W_min = £10m for both distributions.*

| Distribution | γ | Flat WDT CEW | Progressive WDT CEW | Gap (bp) | E[T] progressive |
|:---|---:|---:|---:|---:|---:|
| Ver. B | 1.0 | -0.8197% | -0.8197% | -0.00 | £0.0904m |
| Ver. B | 2.0 | -0.7865% | -0.7865% | -0.00 | £0.0904m |
| Ver. B | 4.0 | -0.7205% | -0.7205% | -0.00 | £0.0904m |
| Ver. B | 1.0 | -0.8195% | -0.8195% | -0.00 | £0.0904m |
| Ver. B | 2.0 | -0.7858% | -0.7858% | -0.00 | £0.0904m |
| Ver. B | 4.0 | -0.7191% | -0.7191% | -0.00 | £0.0904m |

### B.2 — Leverage Effect on WDT Tax Base and Welfare

*C2 complication: when an agent holds gross assets A with outstanding debt D, net worth W = A − D and the WDT taxes the amplified (or dampened) net-worth delta rather than the underlying asset return. NW base = actual WDT base (ΔW = A×R − D − W₀); asset-return base = hypothetical alternative taxing only A×(R−1). The two bases are identical at zero leverage and diverge as D/A rises. Gap (bp) = (CEW_NW − CEW_AR) × 10,000; positive means WDT's NW base produces higher welfare than the asset-return alternative at the same rate. Gross assets = £10m (5×W_min). Progressive rate function. γ=2. Version A distribution.*

| Leverage (%) | W₀ net (£m) | E[T] NW base | E[T] asset-rtn base | CEW NW base | CEW asset-rtn base | Gap (bp) |
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

### B.3 — Two-Period Rate Asymmetry by Initial Wealth

*Sequence: +18.8% gain (μ+σ) in period 1, −8.3% loss (σ) in period 2. τ gain = effective rate on period-1 delta at (W₀, W₁). τ refund = effective rate on period-2 loss at (W₁, W₂). Asymmetry = τ gain − τ refund (pp); positive means gain taxed at higher rate. Excess = net tax progressive − net tax flat; positive = progression costs more.*

| W₀ (£m) | τ gain (%) | τ refund (%) | Asymmetry (pp) | Net tax: progressive | Net tax: flat | Excess |
|---:|---:|---:|---:|---:|---:|---:|
| 3.0 | 15.015 | 15.014 | +0.0011 | £0.0411m | £0.0943m | -0.0532 |
| 4.0 | 15.028 | 15.027 | +0.0015 | £0.0549m | £0.1258m | -0.0709 |
| 10.0 | 15.106 | 15.102 | +0.0037 | £0.1379m | £0.3144m | -0.1765 |
| 20.0 | 15.236 | 15.228 | +0.0074 | £0.2783m | £0.6288m | -0.3505 |
| 40.0 | 15.498 | 15.483 | +0.0153 | £0.5667m | £1.2575m | -0.6908 |
| 100.0 | 16.305 | 16.263 | +0.0415 | £1.4950m | £3.1438m | -1.6488 |
| 200.0 | 17.713 | 17.619 | +0.0946 | £3.2656m | £6.2876m | -3.0220 |

---

## C. CGT Lock-In Distortion

Reference parameters: V=£10m, G/V=50%, r_A=10.45% (empirical equity mean), τ_cgt=24% (UK 2024 higher rate), T=5 years remaining.

### C.1 — Lock-In Welfare Cost by Embedded Gain Ratio

*Lock-in cost (bp) = (CEW_free − CEW_locked) × 10,000. CEW_free: agent switches whenever r_B > r_A (no lock-in). CEW_locked: agent locked in under CGT when r_B < indifference return r_B*. P(locked in) includes two components: states where r_B < r_A (agent stays regardless of CGT — fundamental preference, not a distortion) and states where r_A ≤ r_B < r_B* (CGT lock-in distortion proper — agent would switch without CGT but switching cost exceeds benefit). The welfare cost is attributable to the second component only; the first component is present with or without CGT. Version A distribution. γ=2.*

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

### C.2 — Lock-In Welfare Cost by Remaining Holding Period

*G/V=50% fixed. T varies from 1 to 20 years. Lock-in cost rises from T=1 and plateaus at longer horizons — the direction is upward, not downward. At T=1 the agent has only one period to benefit from switching to B, so the opportunity cost of lock-in is low. Each additional year that Asset B compounds ahead of Asset A raises the foregone return from remaining locked in. The plateau appears as r_B* converges toward r_A and the trapped zone (r_A ≤ r_B < r_B*) collapses — states that triggered lock-in at short T now fall below r_A (agent stays regardless) or above r_B* (agent switches). Indifference return r_B* does converge to r_A as T→∞, confirming lock-in eventually disappears at infinite horizons; but across all empirically relevant horizons (T ≤ 20 yr) the welfare cost is substantially above the T=1 baseline.*

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

### C.3 — Full Welfare Comparison: WDT vs CGT (with and without lock-in)

*A. Module 1 showed WDT ≈ CGT when lock-in was absent. This table adds the lock-in cost to CGT, correcting that comparison. WDT advantage (with lock-in) = CEW_WDT − CEW_CGT_locked.*

| Metric | Version A (Empirical) | Version B (Idealised) |
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

---

## D. Heterogeneous Agents — Incidence and Concentration

Tier differentials from Fagereng et al. (2020): Poor −4.55pp, Ok −2.05pp, Good +0.95pp, Great +3.45pp relative to UK historical equity mean (10.45%). Version A distribution with tier-shifted returns. γ=2.

### D.1 — CEW by Tier and Tax System

*Progressive WDT uses logistic rate function from TOML (τ₀=15%, τ_m=70%, k=0.001, W_min=£2m). All flat-rate systems revenue-equivalent at 2% of Good-tier W₀.*

| System | Poor (95%, W₀=£2.9m) | Ok (99%, W₀=£7.1m) | Good (99.9%, W₀=£19.9m) | Great (99.99%+, W₀=£139.6m) |
|:---|---:|---:|---:|---:|
| Symmetric WDT | -0.2194% | -0.7816% | -1.4211% | -1.9269% |
| Stock Wealth Tax | -1.8424% | -1.8424% | -1.8424% | -1.8424% |
| Income Tax | -0.6000% | -0.9274% | -1.4413% | -1.9161% |
| CGT | -0.6000% | -0.9274% | -1.4413% | -1.9161% |
| Consumption Tax | -1.8424% | -1.8424% | -1.8424% | -1.8424% |
| Progressive WDT | -0.1375% | -0.5004% | -0.9223% | -1.3814% |

### D.2 — Distributional Incidence: Expected Tax as % of W₀

*E[T] / W₀ × 100. All systems calibrated to the same revenue target. Rates differ across tiers because shifted return distributions change E[T]. Progressive WDT incidence not shown here — see Table D.1 CEW column.*

| System | Poor (95%, W₀=£2.9m) | Ok (99%, W₀=£7.1m) | Good (99.9%, W₀=£19.9m) | Great (99.99%+, W₀=£139.6m) |
|:---|---:|---:|---:|---:|
| Symmetric WDT | 0.3362% | 0.9208% | 1.6225% | 2.2071% |
| Stock Wealth Tax | 1.8689% | 1.9150% | 1.9703% | 2.0163% |
| Income Tax | 0.6779% | 1.0489% | 1.6348% | 2.1903% |
| CGT | 0.6779% | 1.0489% | 1.6348% | 2.1903% |
| Consumption Tax | 1.8689% | 1.9150% | 1.9703% | 2.0163% |

### D.3 — Wealth Concentration Path: Great/Poor Ratio at Key Years

*Great-tier wealth / Poor-tier wealth at selected years. All systems calibrated at the population-weighted aggregate tau from Table D.1 (same rate as Parts B/C welfare comparison). Progressive WDT uses the logistic rate function directly. Initial ratio reflects W₀ difference only (150 / 3 = 50×). Return heterogeneity compounds over 30-year scenario horizon starting 2000.*

| System | Initial | 2004 | 2009 | 2019 | 2029 |
|:---|---:|---:|---:|---:|---:|
| Symmetric WDT | 48.8× | 65.1× | 87.4× | 157.2× | 286.3× |
| Progressive WDT | 48.8× | 66.1× | 90.3× | 162.3× | 288.1× |
| Stock Wealth Tax | 48.8× | 70.5× | 103.3× | 220.1× | 479.0× |
| Income Tax | 48.8× | 65.5× | 90.2× | 166.1× | 320.2× |
| Consumption Tax | 48.8× | 70.5× | 103.3× | 220.1× | 479.0× |

### D.4 — Lifetime Contribution Envelope: Binding Summary

*Envelope binds when cumulative refunds would exceed cumulative taxes paid. Refund capped at cumulative taxes paid to date when binding occurs. Min slack = minimum of (cum. tax − cum. refund) over the scenario window; zero means the envelope was exactly hit but not exceeded. The Poor tier binding in the first year of the scenario (2000) is the concrete numerical realisation of the ENV paper's SRR early-year funding gap: the Poor tier's −4.55pp return differential produces a loss in the first scenario year before any cumulative tax has been paid, so the refund that would be owed exceeds the cumulative contribution to date. The envelope floor binds and the refund is capped at zero. Policy implication: the SRR must be pre-funded from sources other than WDT receipts (e.g. initial government capitalisation) to honour refunds in early years for low-return-tier entrants, or the entry-year assessment must provide an initial credit against future taxes. This result holds for the 2000-start sequence; it may differ under other start years — see E. Module 5 Sweep B for the full start-year distribution.*

| Tier | Bracket | W₀ (£m) | Cumulative tax (£m) | Cumulative refund (£m) | Min slack (£m) | Binding years | Ever binds? |
|:---|:---|---:|---:|---:|---:|:---:|:---:|
| Poor | 95% | £2.9m | £0.473m | £0.270m | £0.0000m | 2001 | ⚠ Yes |
| Ok | 99% | £7.1m | £2.440m | £0.398m | £0.0423m | — | No |
| Good | 99.9% | £19.9m | £16.503m | £0.310m | £0.2097m | — | No |
| Great | 99.99%+ | £139.6m | £330.303m | £1.423m | £2.2100m | — | No |

### D.5 — Off-Diagonal Spot Check: Decoupling W₀ from Return Differential

*Corner A: Great return differential (+3.45pp) applied at Poor-tier W₀ (£2.86m). Corner B: Poor return differential (−4.55pp) applied at Great-tier W₀ (£139.6m). These are the two extreme off-diagonal cells of the 4-tier × 4-bracket grid — enough to bound the interaction without computing all 16 combinations. Diagonal (same W₀) = the standard Part B result for the tier sharing this corner's wealth level. Diagonal (same diff) = the standard Part B result for the tier sharing this corner's return differential. Δ vs same-W₀ (bp) = (Corner CEW − Diagonal same-W₀ CEW) × 10,000: positive means decoupling the differential upward improves welfare; negative means the lower return differential of the diagonal tier was welfare-reducing. Revenue target = 2% of each corner's own W₀ (per-corner solve, not aggregate). γ=2. Version A distribution.*

| Corner / System | Corner CEW | Diagonal (same W₀) | Diagonal (same diff) | Δ vs same-W₀ (bp) |
|:---|---:|---:|---:|---:|
| **Corner A: Great diff (+3.45pp), Poor W₀ (£2.86m)** |  |  |  |  |
|   Symmetric WDT | -1.7451% | -0.2194% | -1.9269% | -152.58 |
|   Stock Wealth Tax | -1.8275% | -1.8424% | -1.8424% | +1.49 |
|   Income Tax | -1.7488% | -0.6000% | -1.9161% | -114.88 |
|   CGT | -1.7488% | -0.6000% | -1.9161% | -114.88 |
|   Consumption Tax | -1.8275% | -1.8424% | -1.8424% | +1.49 |
|   Progressive WDT | -1.2343% | -0.1375% | -1.3814% | -109.69 |
|  |  |  |  |  |
| **Corner B: Poor diff (−4.55pp), Great W₀ (£139.6m)** |  |  |  |  |
|   Symmetric WDT | — | -1.9269% | -0.2194% | — |
|   Stock Wealth Tax | -1.9717% | -1.8424% | -1.8424% | -12.92 |
|   Income Tax | -1.8049% | -1.9161% | -0.6000% | +11.12 |
|   CGT | -1.8049% | -1.9161% | -0.6000% | +11.12 |
|   Consumption Tax | -1.9717% | -1.8424% | -1.8424% | -12.92 |
|   Progressive WDT | -0.1568% | -1.3814% | -0.1375% | +122.46 |

---

## E. Welfare Sweep Analysis

Three independent sweep axes: (A) revenue target 1–5% of W₀; (B) start-year worst-case over all 73 historical 30-year windows; (C) progressive-vs-flat WDT welfare gap across rate parameters. All at γ=2 (central case) unless noted.

### E.1 — Sweep A: CEW by System and Revenue Target (γ=2)

*E[T] as % of W₀ swept from 1% to 5%. Columns = revenue target; rows grouped by distribution. Rankings that hold across the full range are structurally robust; rankings that flip signal revenue-sensitivity. γ=2. W₀=1.0 (normalised).*

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

### E.2.1 — Sweep B: Summary Statistics Across All Start Years

*Min/median/mean/max CEW across all 73 start-year windows (1947–2019). WDT best? = fraction of windows where Symmetric WDT has the highest CEW (lowest welfare cost) of the five systems. E[T] = 2% of W₀. γ=2. Version A distribution.*

| System | Min CEW | Median CEW | Mean CEW | Max CEW | WDT best? (% of windows) |
|:---|---:|---:|---:|---:|---:|
| Symmetric WDT | -1.7647% | -1.6727% | -1.6697% | -1.5870% | 100.0% |
| Stock Wealth Tax | -1.8936% | -1.8144% | -1.8125% | -1.7314% | — |
| Income Tax | -1.7713% | -1.6751% | -1.6765% | -1.5881% | — |
| CGT | -1.7713% | -1.6751% | -1.6765% | -1.5881% | — |
| Consumption Tax | -1.8936% | -1.8144% | -1.8125% | -1.7314% | — |

### E.2.2 — Sweep B: Curated Worst-Case Start Years

*Six historically adverse start years plus the canonical 2000 (◄). Adverse years: 1946 (post-war austerity), 1972 (oil shock), 1987 (Black Monday), 1999 (GFC in window), 2000 (dot-com + GFC), 2006 (worst LRR fill speed). WDT adv. = (CEW_WDT − CEW_StockWealth) × 10,000 in basis points.*

| Start year | Symmetric WDT | Stock Wealth Tax | Income Tax | CGT | Consumption Tax | WDT adv. vs Stock (bp) |
|:---|---:|---:|---:|---:|---:|---:|
| 1972 | -1.6260% | -1.7439% | -1.6262% | -1.6262% | -1.7439% | +11.8 |
| 1987 | -1.6975% | -1.8252% | -1.7103% | -1.7103% | -1.8252% | +12.8 |
| 1999 | -1.7411% | -1.8790% | -1.7583% | -1.7583% | -1.8790% | +13.8 |
| 2000 ◄ canonical | -1.7539% | -1.8870% | -1.7713% | -1.7713% | -1.8870% | +13.3 |
| 2006 | -1.7445% | -1.8907% | -1.7625% | -1.7625% | -1.8907% | +14.6 |

### E.3.1 — Sweep C: τ₀ Sensitivity

*Gap (bp) = (CEW_flat − CEW_progressive) × 10,000. Positive = flat WDT has lower welfare cost. τ_m, k, W_min at canonical values.*

| τ₀ (entry rate) | W₀=£10m | W₀=£30m | W₀=£100m |
|:---|---:|---:|---:|
| 0.05 | -0.00 | -0.00 | -0.01 |
| 0.1 | -0.00 | -0.00 | -0.01 |
| 0.15 | -0.00 | -0.00 | -0.01 |
| 0.2 | -0.00 | -0.00 | -0.01 |
| 0.25 | -0.00 | -0.00 | -0.01 |
| 0.3 | -0.00 | -0.00 | -0.00 |

### E.3.2 — Sweep C: τ_m Sensitivity

*τ₀, k, W_min at canonical values.*

| τ_m (ceiling rate) | W₀=£10m | W₀=£30m | W₀=£100m |
|:---|---:|---:|---:|
| 0.4 | -0.00 | -0.00 | -0.00 |
| 0.5 | -0.00 | -0.00 | -0.01 |
| 0.6 | -0.00 | -0.00 | -0.01 |
| 0.7 | -0.00 | -0.00 | -0.01 |
| 0.8 | -0.00 | -0.00 | -0.01 |
| 0.9 | -0.00 | -0.00 | -0.01 |

### E.3.3 — Sweep C: k Sensitivity

*τ₀, τ_m, W_min at canonical values.*

| k (steepness per £m) | W₀=£10m | W₀=£30m | W₀=£100m |
|:---|---:|---:|---:|
| 0.0001 | -0.00 | -0.00 | -0.00 |
| 0.0005 | -0.00 | -0.00 | -0.00 |
| 0.001 | -0.00 | -0.00 | -0.01 |
| 0.005 | -0.00 | -0.01 | -0.03 |
| 0.01 | -0.01 | -0.02 | -0.05 |
| 0.05 | -0.03 | -0.05 | +0.00 |

### E.3.4 — Sweep C: W_min Sensitivity

*τ₀, τ_m, k at canonical values.*

| W_min (£m) | W₀=£10m | W₀=£30m | W₀=£100m |
|:---|---:|---:|---:|
| 0.5 | -0.00 | -0.00 | -0.01 |
| 1.0 | -0.00 | -0.00 | -0.01 |
| 2.0 | -0.00 | -0.00 | -0.01 |
| 5.0 | -0.00 | -0.00 | -0.01 |
| 10.0 | +1.74 | -0.00 | -0.01 |

---

## Parameter Reference

| Parameter | Value | Source |
|:---|---:|:---|
| W₀ (normalised A. Module 1) | 1.0 | — |
| Revenue target E[T] | 2% of W₀ | — |
| γ (central case) | 2.0 | Flavin & Yamashita (2002) |
| τ₀ (WDT entry rate) | 15% | TOML [rate] |
| τ_m (WDT ceiling) | 70% | TOML [rate] |
| k (logistic steepness) | 0.001 | TOML [rate] |
| W_min (£m) | £2m | TOML [rate] |
| UK equity mean (1947–2019) | 10.45% | JST dataset |
| UK equity std dev | 8.31% | JST dataset |
