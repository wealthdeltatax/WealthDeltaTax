### Units and reconciliation (wealth and households as the pack has them; income scaled to B.6g 2024)

Money is carried in thousands of pounds per household inside the module (so the identity check is not at the mercy of rounding) and reported in pounds. Weights are households.

| quantity | cells | reference | gap |
|---|---|---|---|
| households (millions) | 26.991 | 26.991 (pack, all) | 0.00% |
| persons 16+ (millions, cell_weights) | 50.204 | 52.093 (households times I-D4h 1.93); 50.203 at 1.86 | -3.6% against central, 0.0% against low |
| wealth (pounds, billions) | 13568.9 | 13568 (pack, all) | 0.01% |
| wealth over GDP at the start | 6.14 | 2211 billion GDP (pack, 2020 to 2022 mean) | by construction the pack total |
| pension accrual in year 1 (pounds, billions), I-D1k observed 2024 share times cell income | 87.0 | 86.9 (ONS D.8 2024); share of B.6g 0.0483 times 1801.4 | 0.07% |
| non-pension saving in year 1 at the median ratio (pounds, billions) | 18 | 92 (ONS non-pension saving 2024) | a ratio of income, not matched in level |
| income, scaled (pounds, billions): every cell times one factor | 1801.4 | 1801.4 (ONS B.6g, calendar 2024, no price adjustment) | 0.0000% (by construction) |
| income before scaling (pounds, billions, per household table, FYE 2024, gross) | 1311.8 | factor 1.3733 to reach B.6g 2024 | -27.2% before scaling |

Wealth matches the pack by construction. The main runs are aggregate-constrained: income is scaled by the one factor above (band proportions and the retired split kept; B.6g is disposable income and the per-household table is gross, so the factor is a concept-and-level adjustment, not a correction). The run `S_unscaled` keeps the unscaled income as a sensitivity.


### Runs: wealth over GDP (index, start = 1.00) and the realised saving ratio (saving including the pension accrual, over cell income, percent; year 0 shows year 1)

| run | saving % | W/GDP y0 | W/GDP y10 | W/GDP y50 | W/GDP y100 | ratio y0 | ratio y10 | ratio y50 | ratio y100 | identity residual |
|---|---|---|---|---|---|---|---|---|---|---|
| A_low_min | -2.61 | 1.00 | 0.89 | 0.67 | 0.58 | 2.2 | 2.2 | 2.2 | 2.2 | 1.1e-12 |
| A_low_median | 1.01 | 1.00 | 0.94 | 0.80 | 0.75 | 5.8 | 5.8 | 5.8 | 5.8 | 1.3e-12 |
| A_low_max | 13.54 | 1.00 | 1.08 | 1.24 | 1.30 | 18.4 | 18.4 | 18.4 | 18.4 | 1.2e-12 |
| A_mid_min | -2.61 | 1.00 | 0.99 | 0.95 | 0.94 | 2.2 | 2.2 | 2.2 | 2.2 | 1.6e-12 |
| A_mid_median | 1.01 | 1.00 | 1.03 | 1.16 | 1.29 | 5.8 | 5.8 | 5.8 | 5.8 | 1.9e-12 |
| A_mid_max | 13.54 | 1.00 | 1.19 | 1.86 | 2.51 | 18.4 | 18.4 | 18.4 | 18.4 | 2.3e-12 |
| A_high_min | -2.61 | 1.00 | 1.10 | 1.73 | 3.34 | 2.2 | 2.2 | 2.2 | 2.2 | 6.3e-12 |
| A_high_median | 1.01 | 1.00 | 1.15 | 2.08 | 4.42 | 5.8 | 5.8 | 5.8 | 5.8 | 7.7e-12 |
| A_high_max | 13.54 | 1.00 | 1.33 | 3.29 | 8.19 | 18.4 | 18.4 | 18.4 | 18.4 | 9.3e-12 |
| legacy | 0.00 | 1.00 | 0.95 | 0.78 | 0.61 | -27.6 | -26.4 | -21.7 | -17.0 | 1.4e-12 |

### Account terms: saving plus gain over opening wealth, against GDP growth 1.57%

| run | year | S/W % | CG/W % | dNW/W % | GDP growth % |
|---|---|---|---|---|---|
| A_low_median | 1 | 0.77 | 0.06 | 0.83 | 1.57 |
| A_low_median | 10 | 0.82 | 0.13 | 0.95 | 1.57 |
| A_low_median | 50 | 0.97 | 0.35 | 1.32 | 1.57 |
| A_low_median | 100 | 1.04 | 0.48 | 1.52 | 1.57 |
| A_mid_median | 1 | 0.77 | 1.13 | 1.90 | 1.57 |
| A_mid_median | 10 | 0.75 | 1.14 | 1.89 | 1.57 |
| A_mid_median | 50 | 0.67 | 1.16 | 1.83 | 1.57 |
| A_mid_median | 100 | 0.60 | 1.16 | 1.76 | 1.57 |
| A_high_median | 1 | 0.77 | 2.20 | 2.97 | 1.57 |
| A_high_median | 10 | 0.68 | 2.34 | 3.02 | 1.57 |
| A_high_median | 50 | 0.38 | 2.73 | 3.11 | 1.57 |
| A_high_median | 100 | 0.18 | 2.94 | 3.12 | 1.57 |
| legacy | 1 | -3.67 | 4.74 | 1.07 | 1.57 |
| legacy | 10 | -3.67 | 4.74 | 1.07 | 1.57 |
| legacy | 50 | -3.67 | 4.74 | 1.07 | 1.57 |
| legacy | 100 | -3.67 | 4.74 | 1.07 | 1.57 |

### Share of wealth by band

| run | year | D1-3 | D4-5 | D6-7 | D8-9 | D10 |
|---|---|---|---|---|---|---|
| A_mid_median | 0 | 2.1 | 7.7 | 16.8 | 32.7 | 40.7 |
| A_mid_median | 10 | 3.5 | 8.4 | 17.2 | 32.2 | 38.7 |
| A_mid_median | 50 | 7.7 | 10.6 | 18.4 | 30.6 | 32.7 |
| A_mid_median | 100 | 10.8 | 12.3 | 19.4 | 29.5 | 28.0 |
| legacy | 0 | 2.1 | 7.7 | 16.8 | 32.7 | 40.7 |
| legacy | 10 | 2.1 | 7.7 | 16.8 | 32.7 | 40.7 |
| legacy | 50 | 2.1 | 7.7 | 16.8 | 32.7 | 40.7 |
| legacy | 100 | 2.1 | 7.7 | 16.8 | 32.7 | 40.7 |

### Sensitivities (return mid-point label, saving median)

| variant | W/GDP y10 | y50 | y100 |
|---|---|---|---|
| accrual low (3.01% of income) | 1.01 | 1.05 | 1.11 |
| accrual observed 2024 (4.83%, the main run) | 1.03 | 1.16 | 1.29 |
| accrual high (9.74%) | 1.09 | 1.43 | 1.77 |
| income not scaled | 1.01 | 1.07 | 1.14 |
| retired fraction 0.439 (the main run) | 1.03 | 1.16 | 1.29 |
| retired fraction 0.6 | 1.03 | 1.16 | 1.29 |
| retired fraction 0.8 | 1.03 | 1.16 | 1.29 |

### Convention B check (return mid, saving median)

Year 1 aggregate dNW: A 2.581533e+08 (per-household money units, summed), B 2.581533e+08; relative difference 0.00e+00. Identity residual A 1.9e-12, B 2.8e-11. The paths then differ (W/GDP y100 1.29 in A, 3.63 in B) because B credits the yield to the class that earns it and A leaves it in net financial wealth: the two conventions are equal in the first year, not in composition afterwards.


### Negative positions (first year)

| run | net worth below zero | net financial wealth below zero |
|---|---|---|
| A_low_min | none | D1-3|not retired y1, D1-3|retired y1, D4-5|not retired y7, D4-5|retired y14, D6-7|not retired y15, D6-7|retired y27, D8-9|not retired y28, D8-9|retired y47, D10|not retired y60, D10|retired y86 |
| A_low_median | none | none |
| A_low_max | none | none |
| A_mid_min | none | D1-3|not retired y1, D1-3|retired y1, D4-5|not retired y8, D4-5|retired y16, D6-7|not retired y17, D6-7|retired y36, D8-9|not retired y37, D8-9|retired y75 |
| A_mid_median | none | none |
| A_mid_max | none | none |
| A_high_min | none | D1-3|not retired y1, D1-3|retired y1, D4-5|not retired y8, D4-5|retired y20, D6-7|not retired y21, D6-7|retired y63, D8-9|not retired y67 |
| A_high_median | none | none |
| A_high_max | none | none |
| legacy | none | none |
