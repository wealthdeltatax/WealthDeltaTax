# 100r — JST cash-yield and holding-gain split

**Status: completed as a data design.** No pack, builder, manifest, register, or model code was changed.

## Answer

The held JST R6 data are sufficient to reconstruct a cash-yield / holding-gain split of the same annual nominal aggregate return that the pack already uses. For the UK, the reconstruction covers **117 observations, 1896–2019**, with the known 1940–1946 gap. The weighted nominal yield plus weighted nominal holding-gain residual reproduces `capital_tr` to a maximum absolute error of **1.183e-6 percentage points** (fraction residual × 100); the real split reproduces the pack's CPI-deflated return to **1.157e-6 percentage points**. Both are below the stated tolerance of 0.00001 percentage points.

Across those 117 years, the arithmetic mean decomposition is:

| Component | Mean per year |
|---|---:|
| Nominal cash-yield contribution | 4.197% |
| Nominal holding-gain contribution | 4.274% |
| Nominal total return (`capital_tr`) | 8.471% |
| Real cash-yield contribution | 4.034% |
| Real holding-gain contribution | 0.708% |
| Real total return | 4.742% |

This is a decomposition of the JST market-portfolio return. It is **not** a measure of household retained income, saving, or consumption.

## 1. Source variables and definitions

The source is `model_v2/jst_r6.json`, copied unchanged to `data/country-packs/GBR/source/jst_r6.json`, with the original workbook `data/rates/JSTdatasetR6.xlsx` held in the repository. The pack builder reads the JSON for `returns.csv` and asserts the workbook/JSON match for the GDP-per-head and expenditure series. The R6 JSON stores decimal rates (e.g. 0.05 = 5%); `returns.csv` multiplies return columns by 100 and stores percentage points.

| JST variable | Meaning used here | Units / treatment |
|---|---|---|
| `eq_div_rtn` | Equity dividend return: dividend cash flow divided by the preceding period's equity price | Nominal annual rate, decimal in JSON |
| `eq_capgain` | Equity capital gain: change in equity price divided by preceding period's price | Nominal annual rate |
| `eq_tr` | Equity total return; dividend return plus capital gain | Nominal annual rate |
| `housing_rent_rtn` | Housing rental return: rent divided by preceding period's housing price | Nominal annual rate; net rental income, including imputed rent on owner-occupied homes |
| `housing_capgain` | Housing capital gain: change in house price divided by preceding period's price | Nominal annual rate |
| `housing_tr` | Housing total return; rental return plus capital gain | Nominal annual rate |
| `bond_rate` | Bond income-rate proxy: coupon yield where available, otherwise yield to maturity | Nominal annual rate; **not a uniform observed coupon cash flow** |
| `bond_tr` | Government bond total return | Nominal annual rate; includes coupon and bond-price return |
| `bill_rate` | Bill / short-duration safe yield | Nominal annual rate; in earlier periods may be money-market or bank-deposit rates rather than Treasury bills |
| `risky_tr` | Weighted return on equity and housing | Nominal annual rate |
| `safe_tr` | Equal-weight average of bond and bill returns | Nominal annual rate |
| `capital_tr` | JST total return on wealth, weighted across equity, housing, bonds and bills | Nominal annual rate; the pack's total-return input |

Definitions are grounded in the JST return documentation: the total return is the capital-price change plus the yield component; equity and housing have separate dividend/rent and capital-gain series; owner-occupied housing includes imputed rent; safe returns equally weight bonds and bills; risky returns weight equity and housing; the overall wealth return weights risky and safe assets by their outstanding stocks. The R6 update documents the 2016–2020 extensions. See the source links below.

## 2. Coverage and data treatment

- The pack's return history is 1870–2019, but `capital_tr` and `risky_tr` are available only for 1896–2019, with 1940–1946 absent: 117 usable observations.
- Equity component and total-return series have 150 observations, 1871–2020. The pack uses 1871–2019 (149 observations).
- Housing component and total-return series have 118 observations, 1896–2020. The pack uses 1896–2019 (117 observations).
- Bond and bill series are available 1870–2020. The pack uses 1870–2019 (150 observations).
- 2020 is not used because the pack's return sample ends in 2019. No interpolation or gap-filling was done.

## 3. Reconstruction and identity checks

All rates below are decimal annual rates in the calculation; the CSV stores decimals, not percentage points.

### Individual classes

- **Equity:** `eq_div_rtn + eq_capgain = eq_tr`. Across 150 source observations, the maximum absolute residual is 5.215e-6 percentage points.
- **Housing:** `housing_rent_rtn + housing_capgain = housing_tr`. Across 118 source observations, the maximum absolute residual is 1.490e-6 percentage points.
- **Bonds:** define the holding-gain residual as `bond_tr - bond_rate`. This makes the arithmetic split add to `bond_tr`, but the yield leg is a proxy where `bond_rate` is yield to maturity rather than actual coupon cash flow. It must not be presented as a directly observed coupon series.
- **Bills:** `bill_rate` is the cash-yield proxy; nominal holding gain is set to zero as the short-duration bill convention. There is no separate bill price-gain series in the held JST variables.

### Aggregate portfolio weights

The RORE/JST method defines:

1. `safe_tr = (bond_tr + bill_rate) / 2` (equal bond/bill weights).
2. `risky_tr = w_eq|risky × eq_tr + (1 − w_eq|risky) × housing_tr`.
3. `capital_tr = w_risky × risky_tr + (1 − w_risky) × safe_tr`.

The component weights can therefore be recovered from the held composite returns:

- `w_risky = (capital_tr − safe_tr) / (risky_tr − safe_tr)`
- `w_eq|risky = (risky_tr − housing_tr) / (eq_tr − housing_tr)`
- `w_eq = w_risky × w_eq|risky`; `w_housing = w_risky × (1 − w_eq|risky)`
- `w_bond = w_bill = (1 − w_risky) / 2`

Mean weights over the 117 observations:

| Asset | Mean weight |
|---|---:|
| Equity | 28.59% |
| Housing | 41.21% |
| Government bonds | 15.10% |
| Government bills / short safe assets | 15.10% |

The underlying weights are not separate columns in the held JSON. These are algebraically recovered weights from `risky_tr`, `safe_tr`, and `capital_tr`, using the documented JST composite-return identities. They are time-varying market-stock weights, not household-specific portfolio weights.

### Reproduction against the pack

The annual reconstruction is compared with the existing `data/country-packs/GBR/returns.csv`. Each pack total-return column is a direct copy of the matching JST series (percentage points in the CSV, decimals in the JSON):

| Pack column | Matched observations | Maximum absolute source/pack difference |
|---|---:|---:|
| `eq_tr` | 149 | 4.828e-7 percentage points |
| `housing_tr` | 117 | 4.987e-7 percentage points |
| `bond_tr` | 150 | 4.976e-7 percentage points |
| `capital_tr` | 117 | 4.908e-7 percentage points |

The weighted reconstruction residual against JST `capital_tr` is 1.183e-6 percentage points; the real decomposition residual is 1.157e-6 percentage points. Tolerance: **1e-7 in decimal-return units** (0.00001 percentage points). All observations pass. The pack has no separate `bill_tr` column; its bill leg is `bill_rate`.

**What these checks do and do not test.** The weights are solved from `capital_tr`, `risky_tr` and `safe_tr`, so the weighted identity (nominal and real) holds by construction: its residuals show floating-point noise, not independent confirmation. The substantive tests are (a) the equity and housing component identities against the source, (b) the pack-copy comparison, (c) the recovered weights being sensible (all in [0, 1], summing to 1, equity 0.10 to 0.49, housing 0.16 to 0.66, each bond and bill weight 0.05 to 0.30), and (d) the mean real yield plus mean real holding gain (4.034% + 0.708%) equalling the register's I-D1a central value of 4.74%.

## 4. Real conversion and nominal revaluation

Let nominal cash yield be \(y_t\), nominal holding gain be \(g_{h,t}\), and CPI inflation be \(\pi_t = CPI_t/CPI_{t-1}-1\). The JST nominal arithmetic identity is:

\[
r_t^{nom}=y_t+g_{h,t}.
\]

The combination used throughout is **arithmetic and additive within a year**: yield and gain add to the annual return, and averages across years are arithmetic means. No geometric (compounded) decomposition is attempted; a geometric mean of the total return (I-D1a2) does not split additively into yield and gain, so the split must not be used for compounded wealth paths. The exact additive real decomposition consistent with the pack's gross-return deflator is:

\[
y_t^{real}=\frac{y_t}{1+\pi_t},\qquad
g_{h,t}^{real}=\frac{g_{h,t}-\pi_t}{1+\pi_t},
\]

so that:

\[
y_t^{real}+g_{h,t}^{real}
=\frac{1+r_t^{nom}}{1+\pi_t}-1.
\]

This matches `model/model_v3/core/returns.py:real_series`, which computes `(1 + capital_tr) / (CPI_t / CPI_(t-1)) - 1`. The CSV applies the same deflator to each class and to the weighted portfolio.

**Where revaluation belongs:** nominal asset-price changes belong in the holding-gain leg. For bonds, that includes price movements as yields change, captured in the residual `bond_tr − bond_rate`. For bills and cash-like nominal claims, there may be no nominal price gain, but CPI erosion appears in the real holding-gain leg. For nominal household debt, inflation reduces the real value of the liability and therefore raises the borrower's real net worth; that effect belongs in the net-worth revaluation/holding-gain account with the liability sign reversed. JST's `capital_tr` does not include a household-debt series, nor does it separately identify bank-cash holdings.

## 5. Proposed pack schema (specification only)

Proposed file: `returns_decomposition.csv`, one row per year, 1896–2019 where the portfolio composite exists. Store decimal annual rates and fractional weights (not percentages), matching the core kernel's conventions.

| Column group | Columns | Unit / definition |
|---|---|---|
| Key | `year` | Calendar year |
| Portfolio weights | `weight_equity`, `weight_housing`, `weight_bond`, `weight_bill` | Fraction of total JST portfolio; sum to 1 |
| Nominal class split | `equity_y_nominal`, `equity_g_nominal`, `housing_y_nominal`, `housing_g_nominal`, `bond_y_proxy_nominal`, `bond_g_residual_nominal`, `bill_y_proxy_nominal`, `bill_g_nominal` | Decimal annual rates; bond yield caveat applies; bill gain is zero by convention |
| Nominal checks | `equity_tr_nominal`, `housing_tr_nominal`, `bond_tr_nominal`, `bill_tr_nominal`, `risky_tr_nominal`, `safe_tr_nominal`, `capital_tr_nominal` | Decimal annual returns |
| Deflator | `cpi_inflation` | Annual CPI change, decimal |
| Real class split | Matching `*_y_real`, `*_g_real`, `*_tr_real` columns | Decimal annual rates using the pack CPI deflator |
| Aggregate | `portfolio_y_nominal`, `portfolio_g_nominal`, `portfolio_y_real`, `portfolio_g_real` | Weighted yield and holding-gain contributions |
| Audit | `eq_identity_residual_nominal`, `housing_identity_residual_nominal`, `portfolio_identity_residual_nominal`, `portfolio_identity_residual_real`, `pack_capital_tr_residual` | Decimal residuals; must be within tolerance |

The committed reconstruction in `research/tables/100r-jst-cash-yield-and-gain-split/returns_decomposition.csv` uses this schema plus audit columns. No manifest row, pack file, or builder logic has been added.

## 6. What this split is not

It is the market-return decomposition of a JST aggregate asset portfolio. It does not say that a household receives all dividend/rental/bond income as cash, retains it, consumes it, or saves it. It does not include household-specific asset weights, tax, maintenance beyond the net-rent construction, reinvestment choices, pension contributions/accrual, household borrowing, or transfers. It therefore cannot be substituted for household saving or income in the household-flow identity. The household account must separately specify how much of cash income is consumed, saved, taxed, or otherwise transferred.

## Sources and provenance

- Held source data: `model_v2/jst_r6.json` (SHA `1c16b0ccf7e10d6b97ee192caace93c4b82c2d2b`); copied unchanged to `data/country-packs/GBR/source/jst_r6.json`.
- Held source workbook: `data/rates/JSTdatasetR6.xlsx`; builder asserts selected source values against the JSON.
- Pack total-return table: `data/country-packs/GBR/returns.csv`; built by `model/model_v3/pack/build_gbr.py`.
- Pack real conversion: `model/model_v3/core/returns.py`.
- JST Macrohistory Database R6 codebook, pp. 6–7 (variable labels and formulas for `eq_tr`, `housing_tr`, `bond_tr`, `bill_rate`, `bond_rate`, component returns and composite returns): https://www.macrohistory.net/app/download/9834516169/JST_documentationR6.pdf?t=1676279836 (accessed 2026-11-21).
- Chen et al. (2022), *Documentation on the JST Database Update 2016–2020*, pp. 3–10 (R6 update to bill, bond, equity, housing and composite returns): https://www.macrohistory.net/app/download/9918957869/JST_RORE_Documentation_R6.pdf?t=1658254098 (accessed 2026-11-21).
- Jordà, Knoll, Kuvshinov, Schularick and Taylor (2019), *The Rate of Return on Everything, 1870–2015*, QJE 134(3), 1225–1298; return-data documentation: https://www.macrohistory.net/app/download/9834516469/RORE_documentation.pdf?t=1614633099 (accessed 2026-11-21).
- Licence: JST data are made available under CC BY-NC-SA 4.0; comply with the non-commercial and share-alike conditions and cite the 2019 return paper when using returns.

## Checks

- Source data and pack data read from the repository.
- Equity and housing identities checked against all non-missing source observations.
- Safe-return identity and portfolio weighted identity checked.
- Real decomposition checked against the pack's CPI-deflated return formula.
- Pack `capital_tr` checked against source `capital_tr`.
- `python -I project/tools/check_agent_docs.py`: run by the guru on the branch tip with a local checkout, 2026-11-21; exit 0. The research agent could not run it (no checkout or shell).
- Guru re-verification from the committed CSV: 117 rows, 1896 to 2019, none in 1940 to 1946; weight sums 1 to 1e-12; weighted yield recomputes to 7e-13; largest residual against the pack `capital_tr` 4.9e-7 percentage points.
