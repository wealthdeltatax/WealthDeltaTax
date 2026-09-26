# WFR Welfare Comparison Model — Appendix Tables

*Generated: 2026-09-26*
*Revenue target: E[T] = 2% of W₀. Canonical N = 30. Scenario start = 2000.*
*All CEW values relative to no-tax benchmark. Negative = welfare cost.*

---

## A. Baseline Single-Agent Comparison

### A.1 — CEW by System, γ, and Distribution

*CEW = proportional consumption change under no-tax making agent indifferent to the taxed system. Negative = welfare cost relative to no-tax. Ver. A = UK historical equity (scenario window). Ver. B = idealised two-state (p=0.5, R_good=E[R]+σ, R_bad=E[R]−σ).*

| System | Ver. A γ=1 | Ver. A γ=2 | Ver. A γ=4 | Ver. B γ=1 | Ver. B γ=2 | Ver. B γ=4 |
|:---|---:|---:|---:|---:|---:|---:|
| Symmetric WDT | -1.8203% | -1.7539% | -1.6217% | -1.8198% | -1.7525% | -1.6188% |
| Stock Wealth Tax | -1.8870% | -1.8870% | -1.8870% | -1.8870% | -1.8870% | -1.8870% |
| Income Tax | -1.8288% | -1.7713% | -1.6583% | -1.8198% | -1.7525% | -1.6188% |
| CGT | -1.8288% | -1.7713% | -1.6583% | -1.8198% | -1.7525% | -1.6188% |
| Consumption Tax | -1.8870% | -1.8870% | -1.8870% | -1.8870% | -1.8870% | -1.8870% |

### A.2 — Variance of Consumption (γ=2)

*Variance of consumption across return states at revenue-equivalent rates. Lower variance indicates greater risk-sharing. D-M prediction: Var(C_sym) = (1−τ)² × Var(C_notax).*

| System | Ver. A Var(C) | Ver. B Var(C) |
|:---|---:|---:|
| Symmetric WDT | 0.0013 | 0.0013 |
| Stock Wealth Tax | 0.0027 | 0.0027 |
| Income Tax | 0.0014 | 0.0013 |
| CGT | 0.0014 | 0.0013 |
| Consumption Tax | 0.0027 | 0.0027 |

### A.3 — Revenue-Equivalent Tax Rates (γ=2)

*Rate τ* such that E[T(W₀, dist, τ*)] = target. Stock wealth and consumption taxes require low rates (broad base); income tax and CGT require higher rates (gains only, no collection in loss states).*

| System | Ver. A rate (τ*) | Ver. B rate (τ*) |
|:---|---:|---:|
| Symmetric WDT | 33.404% | 33.404% |
| Stock Wealth Tax | 1.887% | 1.887% |
| Income Tax | 32.067% | 33.404% |
| CGT | 32.067% | 33.404% |
| Consumption Tax | 1.923% | 1.923% |

### A.4 — Domar–Musgrave Test: Symmetric WDT

*Prediction: Var(C_tax) / Var(C_notax) = (1−τ)². Gap near zero confirms D-M holds for the flat-rate symmetric case.*

| Distribution | γ | τ (WDT) | (1−τ)² | Actual ratio | Gap | Holds? |
|:---|---:|---:|---:|---:|---:|:---:|
| Ver. A | 1.0 | 33.4039% | 0.443505 | 0.443505 | -5.55e-17 | ✓ |
| Ver. A | 2.0 | 33.4039% | 0.443505 | 0.443505 | -5.55e-17 | ✓ |
| Ver. A | 4.0 | 33.4039% | 0.443505 | 0.443505 | -5.55e-17 | ✓ |
| Ver. B | 1.0 | 33.4039% | 0.443505 | 0.443505 | 9.44e-16 | ✓ |
| Ver. B | 2.0 | 33.4039% | 0.443505 | 0.443505 | 9.44e-16 | ✓ |
| Ver. B | 4.0 | 33.4039% | 0.443505 | 0.443505 | 9.44e-16 | ✓ |

---

## B. Progressive Rates and the Three D-M Complications

### B.1 — Flat WDT vs Progressive WDT CEW

*C1 complication: progressive rate breaks the flat D-M result. Flat WDT revenue-matched to progressive WDT's E[T]. Gap (bp) = (CEW_flat − CEW_progressive) × 10,000. Positive = flat WDT better.*

| Distribution | γ | Flat WDT CEW | Progressive WDT CEW | Gap (bp) | E[T] progressive |
|:---|---:|---:|---:|---:|---:|
| Ver. A | 1.0 | -0.8197% | -0.8197% | -0.00 bp | £0.0904m |
| Ver. A | 2.0 | -0.7865% | -0.7865% | -0.00 bp | £0.0904m |
| Ver. A | 4.0 | -0.7205% | -0.7205% | -0.00 bp | £0.0904m |
| Ver. B | 1.0 | -0.8195% | -0.8195% | -0.00 bp | £0.0904m |
| Ver. B | 2.0 | -0.7858% | -0.7858% | -0.00 bp | £0.0904m |
| Ver. B | 4.0 | -0.7191% | -0.7191% | -0.00 bp | £0.0904m |

### B.2 — Leverage Effect on WDT Tax Base and Welfare

*C2 complication: WDT taxes the amplified net-worth delta rather than underlying asset return. NW base = actual WDT base; asset-return base = hypothetical alternative. Gap (bp) = (CEW_NW − CEW_AR) × 10,000.*

| Leverage (%) | W₀ net (£m) | E[T] NW base | E[T] asset-rtn base | CEW NW base | CEW asset-rtn base | Gap (bp) |
|---:|---:|---:|---:|---:|---:|---:|
| 0.0 | £10.00m | 0.0904 | 0.0904 | -0.7865% | -0.7865% | +0.00 bp |
| 5.0 | £9.50m | 0.0904 | 0.0904 | -0.8219% | -0.8222% | +0.03 bp |
| 10.0 | £9.00m | 0.0903 | 0.0904 | -0.8606% | -0.8612% | +0.07 bp |
| 15.0 | £8.50m | 0.0903 | 0.0904 | -0.9031% | -0.9042% | +0.11 bp |
| 20.0 | £8.00m | 0.0903 | 0.0904 | -0.9501% | -0.9516% | +0.15 bp |
| 25.0 | £7.50m | 0.0902 | 0.0904 | -1.0022% | -1.0042% | +0.20 bp |
| 30.0 | £7.00m | 0.0902 | 0.0904 | -1.0604% | -1.0629% | +0.25 bp |
| 35.0 | £6.50m | 0.0902 | 0.0904 | -1.1257% | -1.1288% | +0.31 bp |
| 40.0 | £6.00m | 0.0901 | 0.0904 | -1.1995% | -1.2033% | +0.38 bp |
| 45.0 | £5.50m | 0.0901 | 0.0904 | -1.2836% | -1.2882% | +0.46 bp |
| 50.0 | £5.00m | 0.0901 | 0.0904 | -1.3801% | -1.3856% | +0.55 bp |
| 55.0 | £4.50m | 0.0900 | 0.0904 | -1.4920% | -1.4985% | +0.65 bp |
| 60.0 | £4.00m | 0.0900 | 0.0904 | -1.6228% | -1.6306% | +0.78 bp |
| 65.0 | £3.50m | 0.0900 | 0.0904 | -1.7771% | -1.7863% | +0.93 bp |
| 70.0 | £3.00m | 0.0899 | 0.0904 | -1.9602% | -1.9712% | +1.10 bp |

### B.3 — Two-Period Rate Asymmetry by Initial Wealth

*C3 complication: gain-year rate ≠ refund-year rate under progression. Sequence: gain (μ+σ) in period 1, loss (σ) in period 2. Excess = net tax progressive − net tax flat.*

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

Reference parameters: V=£10m, G/V=50%, r_A=10.45%, τ_cgt=24%, T=5 years.

### C.1 — Lock-In Welfare Cost by Embedded Gain Ratio

*Lock-in cost (bp) = (CEW_free − CEW_locked) × 10,000. CEW_free: agent switches whenever r_B > r_A. CEW_locked: agent stays in A when r_B < indifference return r_B*. Ver. A distribution. γ=2.*

| G/V (%) | CEW (free) | CEW (locked) | Lock-in cost (bp) | P(total locked) | P(CGT distortion) | P(r_B < r_A) |
|---:|---:|---:|---:|---:|---:|---:|
| 5.0 | 5.0343% | 4.8704% | +16.39 bp | 86.7% | 0.0% | 86.7% |
| 9.5 | 5.0343% | 4.7208% | +31.35 bp | 86.7% | 0.0% | 86.7% |
| 13.9 | 5.0343% | 4.5683% | +46.60 bp | 86.7% | 0.0% | 86.7% |
| 18.4 | 5.0343% | 4.4129% | +62.15 bp | 86.7% | 0.0% | 86.7% |
| 22.9 | 5.0343% | 4.2543% | +78.00 bp | 86.7% | 0.0% | 86.7% |
| 27.4 | 5.0343% | 4.0927% | +94.17 bp | 86.7% | 0.0% | 86.7% |
| 31.8 | 5.0343% | 3.9278% | +110.66 bp | 86.7% | 0.0% | 86.7% |
| 36.3 | 5.0343% | 4.0239% | +101.05 bp | 90.0% | 3.3% | 86.7% |
| 40.8 | 5.0343% | 3.8954% | +113.89 bp | 90.0% | 3.3% | 86.7% |
| 45.3 | 5.0343% | 3.7642% | +127.01 bp | 90.0% | 3.3% | 86.7% |
| 49.7 | 5.0343% | 3.6302% | +140.42 bp | 90.0% | 3.3% | 86.7% |
| 54.2 | 5.0343% | 3.9006% | +113.37 bp | 93.3% | 6.7% | 86.7% |
| 58.7 | 5.0343% | 3.8075% | +122.68 bp | 93.3% | 6.7% | 86.7% |
| 63.2 | 5.0343% | 3.7122% | +132.21 bp | 93.3% | 6.7% | 86.7% |
| 67.6 | 5.0343% | 3.6146% | +141.97 bp | 93.3% | 6.7% | 86.7% |
| 72.1 | 5.0343% | 3.5147% | +151.96 bp | 93.3% | 6.7% | 86.7% |
| 76.6 | 5.0343% | 3.4124% | +162.19 bp | 93.3% | 6.7% | 86.7% |
| 81.1 | 5.0343% | 3.9658% | +106.86 bp | 96.7% | 10.0% | 86.7% |
| 85.5 | 5.0343% | 3.9124% | +112.20 bp | 96.7% | 10.0% | 86.7% |
| 90.0 | 5.0343% | 3.8576% | +117.68 bp | 96.7% | 10.0% | 86.7% |

### C.2 — Lock-In Welfare Cost by Remaining Holding Period

*G/V=50% fixed. T varies from 1 to 20 years. Indifference return r_B* converges to r_A as T→∞.*

| T (years) | r_B* (%) | Lock-in cost (bp) | P(total locked) | P(CGT distortion) | P(r_B < r_A) |
|---:|---:|---:|---:|---:|---:|
| 1 | 25.5114% | +56.11 bp | 100.0% | 13.3% | 86.7% |
| 2 | 17.7401% | +73.27 bp | 96.7% | 10.0% | 86.7% |
| 3 | 15.2581% | +73.27 bp | 96.7% | 10.0% | 86.7% |
| 4 | 14.0368% | +104.80 bp | 93.3% | 6.7% | 86.7% |
| 5 | 13.3102% | +141.22 bp | 90.0% | 3.3% | 86.7% |
| 6 | 12.8284% | +141.22 bp | 90.0% | 3.3% | 86.7% |
| 7 | 12.4856% | +141.22 bp | 90.0% | 3.3% | 86.7% |
| 8 | 12.2291% | +181.13 bp | 86.7% | 0.0% | 86.7% |
| 9 | 12.0300% | +181.13 bp | 86.7% | 0.0% | 86.7% |
| 10 | 11.8710% | +181.13 bp | 86.7% | 0.0% | 86.7% |
| 11 | 11.7411% | +181.13 bp | 86.7% | 0.0% | 86.7% |
| 12 | 11.6329% | +181.13 bp | 86.7% | 0.0% | 86.7% |
| 13 | 11.5414% | +181.13 bp | 86.7% | 0.0% | 86.7% |
| 14 | 11.4631% | +181.13 bp | 86.7% | 0.0% | 86.7% |
| 15 | 11.3953% | +181.13 bp | 86.7% | 0.0% | 86.7% |
| 16 | 11.3360% | +181.13 bp | 86.7% | 0.0% | 86.7% |
| 17 | 11.2837% | +181.13 bp | 86.7% | 0.0% | 86.7% |
| 18 | 11.2372% | +181.13 bp | 86.7% | 0.0% | 86.7% |
| 19 | 11.1956% | +181.13 bp | 86.7% | 0.0% | 86.7% |
| 20 | 11.1582% | +181.13 bp | 86.7% | 0.0% | 86.7% |

### C.3 — Full Welfare Comparison: WDT vs CGT

*Adds lock-in cost to CGT welfare, correcting the Module 1 comparison. WDT advantage (with lock-in) = CEW_WDT − CEW_CGT_locked.*

| Metric | Ver. A | Ver. B |
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

Tier differentials from Fagereng et al. (2020). Version A distribution with tier-shifted returns. γ=2. Revenue target = 2% of population-weighted aggregate W₀.

### D.1 — CEW by Tier and Tax System

*Progressive WDT uses logistic rate function from TOML. All flat-rate systems calibrated at population-weighted aggregate revenue target.*

| System | Poor (95%, W₀=£2.9m) | Ok (99%, W₀=£7.1m) | Good (99.9%, W₀=£19.9m) | Great (99.99%+, W₀=£139.6m) |
|:---|---:|---:|---:|---:|
| Symmetric WDT | -0.2194% | -0.7816% | -1.4211% | -1.9269% |
| Stock Wealth Tax | -1.8424% | -1.8424% | -1.8424% | -1.8424% |
| Income Tax | -0.6000% | -0.9274% | -1.4413% | -1.9161% |
| CGT | -0.6000% | -0.9274% | -1.4413% | -1.9161% |
| Consumption Tax | -1.8424% | -1.8424% | -1.8424% | -1.8424% |
| Progressive WDT | -0.1375% | -0.5004% | -0.9223% | -1.3814% |

### D.2 — Distributional Incidence: Expected Tax as % of W₀

*E[T] / W₀ × 100. Rates are population-aggregate equivalent, not per-tier.*

| System | Poor (95%, W₀=£2.9m) | Ok (99%, W₀=£7.1m) | Good (99.9%, W₀=£19.9m) | Great (99.99%+, W₀=£139.6m) |
|:---|---:|---:|---:|---:|
| Symmetric WDT | 0.3362% | 0.9208% | 1.6225% | 2.2071% |
| Stock Wealth Tax | 1.8689% | 1.9150% | 1.9703% | 2.0163% |
| Income Tax | 0.6779% | 1.0489% | 1.6348% | 2.1903% |
| CGT | 0.6779% | 1.0489% | 1.6348% | 2.1903% |
| Consumption Tax | 1.8689% | 1.9150% | 1.9703% | 2.0163% |

### D.3 — Wealth Concentration Path: Great/Poor Ratio at Key Years

*All systems calibrated at the aggregate tau from D.1. Progressive WDT uses logistic rate function directly. Initial ratio reflects W₀ difference only.*

| System | Initial | 2004 | 2009 | 2019 | 2029 |
|:---|---:|---:|---:|---:|---:|
| Flat WDT | 48.8× | 65.1× | 87.4× | 157.2× | 286.3× |
| Progressive WDT | 48.8× | 66.1× | 90.3× | 162.3× | 288.1× |
| Stock Wealth Tax | 48.8× | 70.5× | 103.3× | 220.1× | 479.0× |
| Income Tax | 48.8× | 65.5× | 90.2× | 166.1× | 320.2× |
| Consumption Tax | 48.8× | 70.5× | 103.3× | 220.1× | 479.0× |

### D.4 — Lifetime Contribution Envelope: Binding Summary

*Envelope binds when cumulative refunds would exceed cumulative taxes paid. Refund capped at cumulative taxes paid to date when binding occurs.*

| Tier | Bracket | W₀ (£m) | Cumulative tax (£m) | Cumulative refund (£m) | Min slack (£m) | Binding years | Ever binds? |
|:---|:---|---:|---:|---:|---:|:---:|:---:|
| Poor | 95% | £2.9m | £0.473m | £0.270m | £0.0000m | 2001 | ⚠ Yes |
| Ok | 99% | £7.1m | £2.440m | £0.398m | £0.0423m | — | No |
| Good | 99.9% | £19.9m | £16.503m | £0.310m | £0.2097m | — | No |
| Great | 99.99%+ | £139.6m | £330.303m | £1.423m | £2.2100m | — | No |

### D.5 — Off-Diagonal Spot Check

*Corner A: Great return differential at Poor-tier W₀. Corner B: Poor return differential at Great-tier W₀. Δ vs same-W₀ (bp) = (Corner CEW − Diagonal same-W₀ CEW) × 10,000.*

| Corner / System | Corner CEW | Diagonal (same W₀) | Diagonal (same diff) | Δ vs same-W₀ (bp) |
|:---|---:|---:|---:|---:|
| **Corner A: Great diff (+3.45pp), Poor W₀** |  |  |  |  |
|   Symmetric WDT | -1.7451% | -0.2194% | -1.9269% | -152.58 |
|   Stock Wealth Tax | -1.8275% | -1.8424% | -1.8424% | +1.49 |
|   Income Tax | -1.7488% | -0.6000% | -1.9161% | -114.88 |
|   CGT | -1.7488% | -0.6000% | -1.9161% | -114.88 |
|   Consumption Tax | -1.8275% | -1.8424% | -1.8424% | +1.49 |
|   Progressive WDT | -1.2343% | -0.1375% | -1.3814% | -109.69 |
|  |  |  |  |  |
| **Corner B: Poor diff (−4.55pp), Great W₀** |  |  |  |  |
|   Symmetric WDT | — | -1.9269% | -0.2194% | — |
|   Stock Wealth Tax | -1.9717% | -1.8424% | -1.8424% | -12.92 |
|   Income Tax | -1.8049% | -1.9161% | -0.6000% | +11.12 |
|   CGT | -1.8049% | -1.9161% | -0.6000% | +11.12 |
|   Consumption Tax | -1.9717% | -1.8424% | -1.8424% | -12.92 |
|   Progressive WDT | -0.1568% | -1.3814% | -0.1375% | +122.46 |

---

## F. Extended Concentration Horizon (N=73)

Same tiers, systems, and rates as D. Horizon extends to full 1947–2019 historical sequence (no rotation). Rates carried forward from D.

### F.2 — Extended Concentration Path (Key Years)

*Great/Poor wealth ratio at selected years across the full 1947–2019 sequence.*

| System | Initial | 1957 | 1967 | 1977 | 1987 | 1997 | 2000 | 2007 | 2019 |
|:---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Flat WDT | 48.8× | 94.5× | 167.9× | 290.7× | 500.5× | 882.6× | 1,045.6× | 1,558.3× | 3,173.2× |
| Progressive WDT | 48.8× | 99.8× | 175.4× | 222.3× | 169.6× | 152.5× | 146.2× | 138.7× | 177.8× |
| Stock Wealth Tax | 48.8× | 115.1× | 240.2× | 481.9× | 956.5× | 1,974.6× | 2,451.0× | 4,082.9× | 10,239.8× |
| Income Tax | 48.8× | 100.9× | 181.8× | 320.8× | 553.5× | 998.3× | 1,183.6× | 1,776.0× | 3,793.5× |
| Consumption Tax | 48.8× | 115.1× | 240.2× | 481.9× | 956.5× | 1,974.6× | 2,451.0× | 4,082.9× | 10,239.8× |

### F.3 — Flat vs Progressive WDT: Crossover Horizon

*Reports whether and when the progressive WDT Great/Poor ratio drops below the flat WDT ratio at extended horizons.*

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

*Great/Poor, Great/Ok, and Ok/Poor ratios at the N=73 terminal horizon.*

| System | Great/Poor | Great/Ok | Ok/Poor |
|:---|---:|---:|---:|
| Flat WDT | 3,173.2× | 336.1× | 9.4× |
| Progressive WDT | 177.8× | 18.5× | 9.6× |
| Stock Wealth Tax | 10,239.8× | 739.6× | 13.8× |
| Income Tax | 3,793.5× | 358.5× | 10.6× |
| Consumption Tax | 10,239.8× | 739.6× | 13.8× |

---

## E. Welfare Sweep Analysis

### E.1 — Sweep A: CEW by System and Revenue Target (γ=2)

*E[T] as % of W₀ swept from 1% to 5%. Columns = revenue target.*

| Distribution | System | E[T]=1.0% | E[T]=2.0% | E[T]=3.0% | E[T]=4.0% | E[T]=5.0% |
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

### E.1b — Sweep A: CEW by System and W₀ (γ=2, E[T]=2%)

*W₀ swept across the wealth-tier range at fixed 2% revenue target. CEW is invariant to W₀ under this fixed-percentage design.*

| System | W₀=£3m | W₀=£5m | W₀=£8m | W₀=£10m | W₀=£20m | W₀=£30m | W₀=£50m | W₀=£100m | W₀=£150m |
|:---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Symmetric WDT | -1.7539% | -1.7539% | -1.7539% | -1.7539% | -1.7539% | -1.7539% | -1.7539% | -1.7539% | -1.7539% |
| Stock Wealth Tax | -1.8870% | -1.8870% | -1.8870% | -1.8870% | -1.8870% | -1.8870% | -1.8870% | -1.8870% | -1.8870% |
| Income Tax | -1.7713% | -1.7713% | -1.7713% | -1.7713% | -1.7713% | -1.7713% | -1.7713% | -1.7713% | -1.7713% |
| CGT | -1.7713% | -1.7713% | -1.7713% | -1.7713% | -1.7713% | -1.7713% | -1.7713% | -1.7713% | -1.7713% |
| Consumption Tax | -1.8870% | -1.8870% | -1.8870% | -1.8870% | -1.8870% | -1.8870% | -1.8870% | -1.8870% | -1.8870% |

### E.2a — Sweep B: Summary Statistics Across All Start Years

*Min/median/mean/max CEW across all 73 start-year windows (1947–2019). WDT best? = fraction of windows where Symmetric WDT has the lowest welfare cost.*

| System | Min CEW | Median CEW | Mean CEW | Max CEW | WDT best? (% of windows) |
|:---|---:|---:|---:|---:|---:|
| Symmetric WDT | -1.7647% | -1.6727% | -1.6697% | -1.5870% | 100.0% |
| Stock Wealth Tax | -1.8936% | -1.8144% | -1.8125% | -1.7314% | — |
| Income Tax | -1.7713% | -1.6751% | -1.6765% | -1.5881% | — |
| CGT | -1.7713% | -1.6751% | -1.6765% | -1.5881% | — |
| Consumption Tax | -1.8936% | -1.8144% | -1.8125% | -1.7314% | — |

### E.2b — Sweep B: Curated Worst-Case Start Years

*Six historically adverse start years plus the canonical 2000 (◄). WDT adv. = (CEW_WDT − CEW_StockWealth) × 10,000 in basis points.*

| Start year | Symmetric WDT | Stock Wealth Tax | Income Tax | CGT | Consumption Tax | WDT adv. vs Stock (bp) |
|:---|---:|---:|---:|---:|---:|---:|
| 1972 | -1.6260% | -1.7439% | -1.6262% | -1.6262% | -1.7439% | +11.8 |
| 1987 | -1.6975% | -1.8252% | -1.7103% | -1.7103% | -1.8252% | +12.8 |
| 1999 | -1.7411% | -1.8790% | -1.7583% | -1.7583% | -1.8790% | +13.8 |
| 2000 ◄ canonical | -1.7539% | -1.8870% | -1.7713% | -1.7713% | -1.8870% | +13.3 |
| 2006 | -1.7445% | -1.8907% | -1.7625% | -1.7625% | -1.8907% | +14.6 |

### E.3.1 — Sweep C: τ₀ Sensitivity

*Gap (bp) = (CEW_flat − CEW_progressive) × 10,000. τ_m, k, W_min at canonical values.*

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

## G. Parameter Reference

| Parameter | Value |
|:---|---:|
| W₀ (normalised) | 1.0 |
| Revenue target E[T] | 2% of W₀ |
| γ (central case) | 2.0 |
| τ₀ | 15% |
| τ_m | 70% |
| k | 0.001 per £m |
| W_min | £2.0m |
| canonical_N | 30 years |
| hist_mean | 10.45% |
