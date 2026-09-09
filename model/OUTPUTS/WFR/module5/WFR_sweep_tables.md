# WFR Welfare Sweep Analysis — Module 5

*Generated: 2026-09-09*
*All CEW values relative to no-tax benchmark. Negative = welfare cost. Revenue-equivalent rates used throughout.*

---

## Sweep A: Revenue Target Sensitivity

Question: are the welfare rankings stable across the realistic range of revenue targets? Covers E[T] = 1%–5% of W₀, spanning CGT-deferral-equivalent (1%) through income-tax-equivalent (5%). γ = 2. W₀ = 1.0 (normalised). Both distributions.

### Table WFR.S1 — CEW by System and Revenue Target (γ=2)

*Rows grouped by distribution. Columns = revenue target as % of W₀. Rankings that flip across the revenue range signal revenue-sensitivity; rankings that hold across the full range are structurally robust.*

| Distribution | System | E[T]=1% | E[T]=2% | E[T]=3% | E[T]=4% | E[T]=5% |
|:---|:---|---:|---:|---:|---:|---:|
| Ver. A | Symmetric WDT (flat) | -0.8705% | -1.7539% | -2.6504% | -3.5605% | -4.4846% |
| Ver. A | Stock Wealth Tax | -0.9435% | -1.8870% | -2.8305% | -3.7740% | -4.7175% |
| Ver. A | Income Tax (no refund) | -0.8809% | -1.7713% | -2.6715% | -3.5821% | -4.5033% |
| Ver. A | CGT (gains only) | -0.8809% | -1.7713% | -2.6715% | -3.5821% | -4.5033% |
| Ver. A | Consumption Tax | -0.9435% | -1.8870% | -2.8305% | -3.7740% | -4.7175% |
|  |  |  |  |  |  |  |
| Ver. B | Symmetric WDT (flat) | -0.8698% | -1.7525% | -2.6486% | -3.5585% | -4.4826% |
| Ver. B | Stock Wealth Tax | -0.9435% | -1.8870% | -2.8305% | -3.7740% | -4.7175% |
| Ver. B | Income Tax (no refund) | -0.8698% | -1.7525% | -2.6486% | -3.5585% | -4.4826% |
| Ver. B | CGT (gains only) | -0.8698% | -1.7525% | -2.6486% | -3.5585% | -4.4826% |
| Ver. B | Consumption Tax | -0.9435% | -1.8870% | -2.8305% | -3.7740% | -4.7175% |

---

## Sweep B: Start-Year Worst-Case Analysis

Question: does the WDT's structural advantage survive the historically adverse return sequences? Runs all 73 possible 30-year windows within the 1947–2019 series (with wrap-around). E[T] = 2% of W₀. γ = 2. Ver. A distribution.

### Table WFR.S2a — Summary Statistics Across All Start Years

*Min/median/mean/max CEW across all 73 start-year windows. WDT best? = fraction of start years where Symmetric WDT has highest CEW (lowest welfare cost) of the five systems.*

| System | Min CEW | Median CEW | Mean CEW | Max CEW | WDT best? (% of years) |
|:---|---:|---:|---:|---:|---:|
| Symmetric WDT (flat) | -1.7647% | -1.6727% | -1.6697% | -1.5870% | 100.0% |
| Stock Wealth Tax | -1.8936% | -1.8144% | -1.8125% | -1.7314% | — |
| Income Tax (no refund) | -1.7713% | -1.6751% | -1.6765% | -1.5881% | — |
| CGT (gains only) | -1.7713% | -1.6751% | -1.6765% | -1.5881% | — |
| Consumption Tax | -1.8936% | -1.8144% | -1.8125% | -1.7314% | — |

### Table WFR.S2b — Curated Worst-Case Start Years

*Six historically adverse sequences plus the canonical 2000-start (◄). Adverse years selected for: proximity to major market dislocations (1972 oil shock, 1987 Black Monday, 1999/2000 dot-com, 2006 GFC entry), post-war austerity (1946), and worst LRR fill speed (2006). WDT advantage column = (CEW_WDT − CEW_StockWealth) × 10,000 in basis points.*

| Start year | Symmetric WDT | Stock Wealth Tax | Income Tax | CGT (gains only) | Consumption Tax | WDT adv. vs Stock (bp) |
|:---|---:|---:|---:|---:|---:|---:|
| 1972 | -1.6260% | -1.7439% | -1.6262% | -1.6262% | -1.7439% | +11.8 |
| 1987 | -1.6975% | -1.8252% | -1.7103% | -1.7103% | -1.8252% | +12.8 |
| 1999 | -1.7411% | -1.8790% | -1.7583% | -1.7583% | -1.8790% | +13.8 |
| 2000 ◄ canonical | -1.7539% | -1.8870% | -1.7713% | -1.7713% | -1.8870% | +13.3 |
| 2006 | -1.7445% | -1.8907% | -1.7625% | -1.7625% | -1.8907% | +14.6 |

---

## Sweep C: Progressive WDT Parameter Sensitivity

Question: across the feasible WDT parameter space, when does the progressive structure add meaningful welfare cost relative to a revenue-equivalent flat rate? Single-parameter sweeps holding all other parameters at canonical values. Revenue-equivalent: progressive rate scaled to match flat system's E[T]. E[T] = 2% of W₀. γ = 2. Gap (bp) = (CEW_flat − CEW_progressive) × 10,000; positive = flat WDT has lower welfare cost; negative = progressive is cheaper.

### Table WFR.S3a — τ₀ Sweep (Entry Rate Floor)

*τ₀ (entry rate at W_min). τ_m, k, W_min at canonical values.*

| τ₀ (entry rate) | W₀=£10m | W₀=£30m | W₀=£100m |
|:---|---:|---:|---:|
| 0.05 | -0.00 | -0.00 | -0.01 |
| 0.1 | -0.00 | -0.00 | -0.01 |
| 0.15 | -0.00 | -0.00 | -0.01 |
| 0.2 | -0.00 | -0.00 | -0.01 |
| 0.25 | -0.00 | -0.00 | -0.01 |
| 0.3 | -0.00 | -0.00 | -0.00 |

### Table WFR.S3b — τ_m Sweep (Ceiling Rate)

*τ_m (asymptotic ceiling). τ₀, k, W_min at canonical values.*

| τ_m (ceiling rate) | W₀=£10m | W₀=£30m | W₀=£100m |
|:---|---:|---:|---:|
| 0.4 | -0.00 | -0.00 | -0.00 |
| 0.5 | -0.00 | -0.00 | -0.01 |
| 0.6 | -0.00 | -0.00 | -0.01 |
| 0.7 | -0.00 | -0.00 | -0.01 |
| 0.8 | -0.00 | -0.00 | -0.01 |
| 0.9 | -0.00 | -0.00 | -0.01 |

### Table WFR.S3c — k Sweep (Logistic Steepness)

*k (steepness per £m). τ₀, τ_m, W_min at canonical values.*

| k (steepness per £m) | W₀=£10m | W₀=£30m | W₀=£100m |
|:---|---:|---:|---:|
| 0.0001 | -0.00 | -0.00 | -0.00 |
| 0.0005 | -0.00 | -0.00 | -0.00 |
| 0.001 | -0.00 | -0.00 | -0.01 |
| 0.005 | -0.00 | -0.01 | -0.03 |
| 0.01 | -0.01 | -0.02 | -0.05 |
| 0.05 | -0.03 | -0.05 | +0.00 |

### Table WFR.S3d — W_min Sweep (Entry-Point Wealth)

*W_min (£m). τ₀, τ_m, k at canonical values.*

| W_min (£m) | W₀=£10m | W₀=£30m | W₀=£100m |
|:---|---:|---:|---:|
| 0.5 | -0.00 | -0.00 | -0.01 |
| 1.0 | -0.00 | -0.00 | -0.01 |
| 2.0 | -0.00 | -0.00 | -0.01 |
| 5.0 | -0.00 | -0.00 | -0.01 |
| 10.0 | +1.74 | -0.00 | -0.01 |

---

## Parameter Reference

| Parameter | Canonical value |
|:---|---:|
| τ₀ | 15% |
| τ_m | 70% |
| k | 0.001 per £m |
| W_min | £2m |
| canonical_N | 30 years |
| scenario_start_year | 2000 |
| γ (central) | 2.0 |
