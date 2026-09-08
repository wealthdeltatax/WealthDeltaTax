# WFR Welfare Comparison Model — Appendix Tables

*Generated: 2026-09-08*
*Revenue target: E[T] = 2% of W₀ across all systems.*
*All CEW values relative to no-tax benchmark. Positive = welfare-superior to no-tax.*

---

## Module 1: Baseline Single-Agent Comparison

### Table WFR.1 — Consumption-Equivalent Welfare (CEW) by system, γ, and distribution

*CEW = proportional consumption change under no-tax making agent indifferent to the taxed system. Negative = welfare cost relative to no-tax. Numbers are for the 30-year scenario sequence starting 2000 (canonical_N = 30 from TOML [tcm]); they differ from full 73-year series values (1947–2019) by construction — the scenario and full-series runs are separate sensitivity configurations. Ver. A = empirical returns 2000–2029 (30 obs, equal probability 1/30). Ver. B = idealised two-state calibrated to scenario μ and σ (p=0.5, R_good=E[R]+σ, R_bad=E[R]−σ). Full 73-year series numbers appear in the backbone reference figures.*

| System | Ver. A γ=1 | Ver. A γ=2 | Ver. A γ=4 | Ver. B γ=1 | Ver. B γ=2 | Ver. B γ=4 |
|:---|---:|---:|---:|---:|---:|---:|
| Symmetric WDT | -1.7245% | -1.6408% | -1.4813% | -1.7208% | -1.6308% | -1.4540% |
| Stock Wealth Tax | -1.8107% | -1.8107% | -1.8107% | -1.8107% | -1.8107% | -1.8107% |
| Income Tax | -1.7276% | -1.6474% | -1.4953% | -1.7208% | -1.6308% | -1.4540% |
| CGT | -1.7276% | -1.6474% | -1.4953% | -1.7208% | -1.6308% | -1.4540% |
| Consumption Tax | -1.8107% | -1.8107% | -1.8107% | -1.8107% | -1.8107% | -1.8107% |

### Table WFR.2 — Variance of Consumption by system (γ=2)

*Variance of consumption across return states at revenue-equivalent rates. Lower variance indicates greater risk-sharing. D-M prediction: Var(C_sym) = (1−τ)² × Var(C_notax).*

| System | Ver. A Var(C) | Ver. B Var(C) |
|:---|---:|---:|
| Symmetric WDT | 0.0045 | 0.0045 |
| Stock Wealth Tax | 0.0067 | 0.0067 |
| Income Tax | 0.0046 | 0.0045 |
| CGT | 0.0046 | 0.0045 |
| Consumption Tax | 0.0067 | 0.0067 |

### Table WFR.3 — Revenue-Equivalent Tax Rates (γ=2)

*Rate τ* such that E[T(W₀, dist, τ*)] = target. Rates differ across systems because tax bases differ. Stock wealth and consumption taxes require low rates (broad base); income tax and CGT require higher rates (gains only, no collection in loss states).*

| System | Ver. A rate (τ*) | Ver. B rate (τ*) |
|:---|---:|---:|
| Symmetric WDT | 19.134% | 19.134% |
| Stock Wealth Tax | 1.811% | 1.811% |
| Income Tax | 18.944% | 19.134% |
| CGT | 18.944% | 19.134% |
| Consumption Tax | 1.844% | 1.844% |

### Table WFR.4 — Domar–Musgrave Test: Symmetric WDT

*Prediction: Var(C_tax) / Var(C_notax) = (1−τ)². Gap near zero confirms D-M holds for the flat-rate symmetric case. Progression breaks D-M — see Module 2.*

| Distribution | γ | τ (WDT) | (1−τ)² | Actual ratio | Gap | Holds? |
|:---|---:|---:|---:|---:|---:|:---:|
| Ver. A | 1.0 | 19.1337% | 0.653935 | 0.653935 | -1.11e-16 | ✓ |
| Ver. A | 2.0 | 19.1337% | 0.653935 | 0.653935 | -1.11e-16 | ✓ |
| Ver. A | 4.0 | 19.1337% | 0.653935 | 0.653935 | -1.11e-16 | ✓ |
| Ver. B | 1.0 | 19.1337% | 0.653935 | 0.653935 | -7.77e-16 | ✓ |
| Ver. B | 2.0 | 19.1337% | 0.653935 | 0.653935 | -7.77e-16 | ✓ |
| Ver. B | 4.0 | 19.1337% | 0.653935 | 0.653935 | -7.77e-16 | ✓ |

---

## Module 2: Progressive Rates and the Three D-M Complications

### Table WFR.5 — C1: Flat WDT vs Progressive WDT CEW

*C1 complication: under a progressive rate, the government co-investment share varies with wealth level, breaking the flat D-M result. Revenue-equivalence calibration: the flat rate τ* is solved to match the progressive system's natural E[T], not the global 2%-of-W₀ target. Both systems therefore collect the same expected revenue; the gap measures the pure structural welfare difference from rate progression alone. The "vs 2% target" column shows how much the canonical logistic schedule deviates from the 2% benchmark at each W₀ — a negative figure means the logistic schedule is less aggressive than the global target at this wealth level. Gap (bp) = (CEW_flat − CEW_progressive) × 10,000; positive = flat WDT has lower welfare cost. W₀ = 5 × W_min = £10m for both distributions.*

| Distribution | γ | Flat WDT CEW | Progressive CEW | Gap (bp) | E[T] matched (£m) | vs 2% target (£m) |
|:---|---:|---:|---:|---:|---:|---:|
| Ver. A | 1.0 | -1.3600% | -1.3599% | -0.00 | £0.1579m | -0.0421 |
| Ver. A | 2.0 | -1.2926% | -1.2926% | -0.00 | £0.1579m | -0.0421 |
| Ver. A | 4.0 | -1.1643% | -1.1642% | -0.01 | £0.1579m | -0.0421 |
| Ver. B | 1.0 | -1.3570% | -1.3570% | -0.00 | £0.1579m | -0.0421 |
| Ver. B | 2.0 | -1.2845% | -1.2845% | -0.00 | £0.1579m | -0.0421 |
| Ver. B | 4.0 | -1.1422% | -1.1421% | -0.00 | £0.1579m | -0.0421 |

### Table WFR.6b — C2: Leverage Effect on WDT Tax Base and Welfare

*C2 complication: when an agent holds debt, the WDT net-worth delta base (ΔW = W₁ − W₀) amplifies or dampens the underlying asset return. An unlevered agent has ΔW = A×(R−1) = ΔA; with leverage, ΔW = ΔA at the asset level but net worth swings more sharply, enlarging the tax base in rising markets and the refund base in falling markets. Gross assets fixed at £10m throughout; net worth W₀ declines as leverage rises (W₀ = A − D = A × (1 − lev. ratio)). E[T] excess = E[T]_NW − E[T]_AR; CEW gap = (CEW_NW − CEW_AR) × 10,000. Positive excess means the actual WDT collects more in expectation than a hypothetical asset-return base would at the same progressive rate schedule — the direction switches if expected asset returns are negative. Version A distribution (scenario 2000), γ=2.*

| Lev. ratio | W₀ (£m) | E[T] NW base | E[T] AR base | E[T] excess | CEW NW base | CEW AR base | CEW gap (bp) |
|---:|---:|---:|---:|---:|---:|---:|---:|
| 0.0% | £10.000m | £0.1579m | £0.1579m | £-0.0000m | -1.2926% | -1.2926% | +0.00 |
| 5.0% | £9.500m | £0.1578m | £0.1579m | £-0.0001m | -1.3475% | -1.3480% | +0.05 |
| 10.0% | £9.000m | £0.1578m | £0.1579m | £-0.0001m | -1.4072% | -1.4083% | +0.11 |
| 15.0% | £8.500m | £0.1577m | £0.1579m | £-0.0002m | -1.4726% | -1.4744% | +0.17 |
| 20.0% | £8.000m | £0.1576m | £0.1579m | £-0.0002m | -1.5445% | -1.5469% | +0.24 |
| 25.0% | £7.500m | £0.1576m | £0.1579m | £-0.0003m | -1.6238% | -1.6270% | +0.32 |
| 30.0% | £7.000m | £0.1575m | £0.1579m | £-0.0004m | -1.7118% | -1.7158% | +0.41 |
| 35.0% | £6.500m | £0.1575m | £0.1579m | £-0.0004m | -1.8100% | -1.8150% | +0.50 |
| 40.0% | £6.000m | £0.1574m | £0.1579m | £-0.0005m | -1.9202% | -1.9263% | +0.61 |
| 45.0% | £5.500m | £0.1573m | £0.1579m | £-0.0006m | -2.0449% | -2.0522% | +0.73 |
| 50.0% | £5.000m | £0.1573m | £0.1579m | £-0.0006m | -2.1870% | -2.1957% | +0.87 |
| 55.0% | £4.500m | £0.1572m | £0.1579m | £-0.0007m | -2.3505% | -2.3608% | +1.03 |
| 60.0% | £4.000m | £0.1571m | £0.1579m | £-0.0007m | -2.5403% | -2.5525% | +1.22 |
| 65.0% | £3.500m | £0.1571m | £0.1579m | £-0.0008m | -2.7632% | -2.7776% | +1.44 |
| 70.0% | £3.000m | £0.1570m | £0.1579m | £-0.0009m | -3.0279% | -3.0449% | +1.70 |

### Table WFR.6 — C3: Two-Period Rate Asymmetry by Initial Wealth

*Sequence: +18.8% gain (μ+σ) in period 1, −8.3% loss (σ) in period 2. τ gain = effective rate on period-1 delta at (W₀, W₁). τ refund = effective rate on period-2 loss at (W₁, W₂). Asymmetry = τ gain − τ refund (pp); positive means gain taxed at higher rate. Excess = net tax progressive − net tax flat; positive = progression costs more.*

| W₀ (£m) | τ gain (%) | τ refund (%) | Asymmetry (pp) | Net tax: progressive | Net tax: flat | Excess |
|---:|---:|---:|---:|---:|---:|---:|
| 3.0 | 15.015 | 15.014 | +0.0011 | £0.0411m | £0.0527m | -0.0116 |
| 4.0 | 15.028 | 15.027 | +0.0015 | £0.0549m | £0.0703m | -0.0155 |
| 10.0 | 15.106 | 15.102 | +0.0037 | £0.1379m | £0.1758m | -0.0379 |
| 20.0 | 15.236 | 15.228 | +0.0074 | £0.2783m | £0.3516m | -0.0733 |
| 40.0 | 15.498 | 15.483 | +0.0153 | £0.5667m | £0.7033m | -0.1366 |
| 100.0 | 16.305 | 16.263 | +0.0415 | £1.4950m | £1.7582m | -0.2632 |
| 200.0 | 17.713 | 17.619 | +0.0946 | £3.2656m | £3.5164m | -0.2508 |

---

## Module 3: CGT Lock-In Distortion

Reference parameters: V=£10m, G/V=50%, r_A=10.45% (empirical equity mean), τ_cgt=24% (UK 2024 higher rate), T=5 years remaining.

### Table WFR.7 — Lock-In Welfare Cost by Embedded Gain Ratio

*Lock-in cost (bp) = (CEW_free − CEW_locked) × 10,000. CEW_free: agent switches whenever r_B > r_A (no lock-in). CEW_locked: agent locked in under CGT when r_B < indifference return r_B*. Version A distribution. γ=2.*

| G/V (%) | CEW (free) | CEW (locked) | Lock-in cost (bp) | P(locked in) |
|---:|---:|---:|---:|---:|
| 5.0 | 3.3647% | 2.8511% | +51.36 | 57.5% |
| 9.5 | 3.3647% | 2.3883% | +97.65 | 57.5% |
| 13.9 | 3.3647% | 1.9996% | +136.51 | 60.3% |
| 18.4 | 3.3647% | 1.5564% | +180.84 | 60.3% |
| 22.9 | 3.3647% | 1.1070% | +225.77 | 60.3% |
| 27.4 | 3.3647% | 0.6515% | +271.33 | 60.3% |
| 31.8 | 3.3647% | 0.1895% | +317.52 | 60.3% |
| 36.3 | 3.3647% | -0.1748% | +353.95 | 61.6% |
| 40.8 | 3.3647% | -0.6336% | +399.84 | 61.6% |
| 45.3 | 3.3647% | -0.9697% | +433.44 | 63.0% |
| 49.7 | 3.3647% | -1.1352% | +449.99 | 65.8% |
| 54.2 | 3.3647% | -1.2479% | +461.27 | 68.5% |
| 58.7 | 3.3647% | -1.6502% | +501.49 | 68.5% |
| 63.2 | 3.3647% | -2.0592% | +542.39 | 68.5% |
| 67.6 | 3.3647% | -2.4752% | +583.99 | 68.5% |
| 72.1 | 3.3647% | -2.8983% | +626.30 | 68.5% |
| 76.6 | 3.3647% | -3.3288% | +669.35 | 68.5% |
| 81.1 | 3.3647% | -3.2828% | +664.75 | 71.2% |
| 85.5 | 3.3647% | -3.1770% | +654.18 | 74.0% |
| 90.0 | 3.3647% | -3.2828% | +664.75 | 75.3% |

### Table WFR.8 — Lock-In Welfare Cost by Remaining Holding Period

*G/V=50% fixed. T varies. Lock-in cost declines as T increases because future switching opportunities reduce the cost of current lock-in. Indifference return r_B* converges to r_A as T→∞.*

| T (years) | Indifference return r_B* | Lock-in cost (bp) | P(locked in) |
|---:|---:|---:|---:|
| 1 | 25.5114% | +265.06 | 95.9% |
| 2 | 17.7401% | +314.85 | 82.2% |
| 3 | 15.2581% | +411.80 | 69.9% |
| 4 | 14.0368% | +424.01 | 68.5% |
| 5 | 13.3102% | +452.50 | 65.8% |
| 6 | 12.8284% | +496.43 | 61.6% |
| 7 | 12.4856% | +496.43 | 61.6% |
| 8 | 12.2291% | +511.83 | 60.3% |
| 9 | 12.0300% | +511.83 | 60.3% |
| 10 | 11.8710% | +511.83 | 60.3% |
| 11 | 11.7411% | +511.83 | 60.3% |
| 12 | 11.6329% | +511.83 | 60.3% |
| 13 | 11.5414% | +511.83 | 60.3% |
| 14 | 11.4631% | +511.83 | 60.3% |
| 15 | 11.3953% | +511.83 | 60.3% |
| 16 | 11.3360% | +511.83 | 60.3% |
| 17 | 11.2837% | +511.83 | 60.3% |
| 18 | 11.2372% | +511.83 | 60.3% |
| 19 | 11.1956% | +511.83 | 60.3% |
| 20 | 11.1582% | +528.75 | 58.9% |

### Table WFR.9 — Full Welfare Comparison: WDT vs CGT (with and without lock-in)

*Module 1 showed WDT ≈ CGT when lock-in was absent. This table adds the lock-in cost to CGT, correcting that comparison. WDT advantage (with lock-in) = CEW_WDT − CEW_CGT_locked.*

| Metric | Version A (Empirical) | Version B (Idealised) |
|:---|---:|---:|
| WDT CEW | -1.6408% | -1.6308% |
| CGT CEW (no lock-in) | -1.6474% | -1.6308% |
| Lock-in welfare cost | +452.50 bp | +642.56 bp |
| CGT CEW (with lock-in) | -6.1724% | -8.0564% |
| WDT advantage (no lock-in) | +0.65 bp | +0.00 bp |
| WDT advantage (with lock-in) | +453.15 bp | +642.56 bp |
| P(agent locked in) | 65.8% | 50.0% |
| CGT indifference return r_B* | 13.3102% | 13.3102% |
| Revenue-equivalent CGT rate | 18.9441% | 19.1337% |

---

## Module 4: Heterogeneous Agents — Incidence and Concentration

Tier differentials from Fagereng et al. (2020): Poor −4.55pp, Ok −2.05pp, Good +0.95pp, Great +3.45pp relative to UK historical equity mean (10.45%). Version A distribution with tier-shifted returns. γ=2.

### Table WFR.10 — CEW by Tier and Tax System

*Progressive WDT uses logistic rate function from TOML (τ₀=15%, τ_m=70%, k=0.001, W_min=£2m). All flat-rate systems revenue-equivalent at 2% of Good-tier W₀.*

| System | Poor | Ok | Good | Great |
|:---|---:|---:|---:|---:|
| Symmetric WDT | -0.7068% | -1.0552% | -1.4522% | -1.7666% |
| Stock Wealth Tax | -1.7718% | -1.7718% | -1.7718% | -1.7718% |
| Income Tax | -0.8682% | -1.1078% | -1.4573% | -1.7635% |
| CGT | -0.8682% | -1.1078% | -1.4573% | -1.7635% |
| Consumption Tax | -1.7718% | -1.7718% | -1.7718% | -1.7718% |
| Progressive WDT | -0.6832% | -1.0246% | -1.4369% | -1.9344% |

### Table WFR.11 — Distributional Incidence: Expected Tax as % of W₀

*E[T] / W₀ × 100. All systems calibrated to the same revenue target. Rates differ across tiers because shifted return distributions change E[T]. Progressive WDT incidence not shown here — see Table WFR.10 CEW column.*

| System | Poor (W₀=£3m) | Ok (W₀=£8m) | Good (W₀=£30m) | Great (W₀=£150m) |
|:---|---:|---:|---:|---:|
| Symmetric WDT | 0.9164% | 1.3045% | 1.7703% | 2.1584% |
| Stock Wealth Tax | 1.8763% | 1.9206% | 1.9738% | 2.0181% |
| Income Tax | 1.0576% | 1.3490% | 1.7720% | 2.1527% |
| CGT | 1.0576% | 1.3490% | 1.7720% | 2.1527% |
| Consumption Tax | 1.8763% | 1.9206% | 1.9738% | 2.0181% |

### Table WFR.12 — Wealth Concentration Path: Great/Poor Ratio at Key Years

*Great-tier wealth / Poor-tier wealth at selected years. All systems calibrated at the population-weighted aggregate tau from Table WFR.10 (same rate as Parts B/C welfare comparison). Progressive WDT uses the logistic rate function directly. Initial ratio reflects W₀ difference only (150 / 3 = 50×). Return heterogeneity compounds over 30-year scenario horizon starting 2000.*

| System | Initial | 2004 | 2009 | 2019 | 2029 |
|:---|---:|---:|---:|---:|---:|
| Symmetric WDT | 50.0× | 68.4× | 94.7× | 180.4× | 348.9× |
| Progressive WDT | 50.0× | 67.6× | 92.3× | 165.0× | 290.9× |
| Stock Wealth Tax | 50.0× | 72.2× | 105.8× | 225.4× | 490.4× |
| Income Tax | 50.0× | 68.7× | 96.6× | 186.7× | 374.7× |
| Consumption Tax | 50.0× | 72.2× | 105.8× | 225.4× | 490.4× |

### Table WFR.13 — Lifetime Contribution Envelope: Binding Summary

*Envelope binds when cumulative refunds would exceed cumulative taxes paid. Refund capped at cumulative taxes paid to date when binding occurs. Min slack = minimum of (cum. tax − cum. refund) over all 73 years. Zero min slack means envelope was exactly hit but not exceeded.*

| Tier | W₀ (£m) | Cumulative tax (£m) | Cumulative refund (£m) | Min slack (£m) | Binding years | Ever binds? |
|:---|---:|---:|---:|---:|:---:|:---:|
| Poor | £3.0m | £0.497m | £0.284m | £0.0000m | 2001 | ⚠ Yes |
| Ok | £8.0m | £2.738m | £0.446m | £0.0475m | — | No |
| Good | £30.0m | £25.490m | £0.475m | £0.3195m | — | No |
| Great | £150.0m | £362.668m | £1.551m | £2.3943m | — | No |

---

## Parameter Reference

| Parameter | Value | Source |
|:---|---:|:---|
| W₀ (normalised Module 1) | 1.0 | — |
| Revenue target E[T] | 2% of W₀ | — |
| γ (central case) | 2.0 | Flavin & Yamashita (2002) |
| τ₀ (WDT entry rate) | 15% | TOML [rate] |
| τ_m (WDT ceiling) | 70% | TOML [rate] |
| k (logistic steepness) | 0.001 | TOML [rate] |
| W_min (£m) | £2m | TOML [rate] |
| UK equity mean (1947–2019) | 10.45% | JST dataset |
| UK equity std dev | 8.31% | JST dataset |
