### Units and reconciliation (nothing rescaled)

Money is carried in thousands of pounds per household inside the module (so the identity check is not at the mercy of rounding) and reported in pounds. Weights are households.

| quantity | cells | reference | gap |
|---|---|---|---|
| households (millions) | 26.991 | 26.991 (pack, all) | 0.00% |
| persons 16+ (millions, cell_weights) | 50.204 | 52.093 (households times I-D4h 1.93); 50.203 at 1.86 | -3.6% against central, 0.0% against low |
| wealth (pounds, billions) | 13568.9 | 13568 (pack, all) | 0.01% |
| wealth over GDP at the start | 6.14 | 2211 billion GDP (pack, 2020 to 2022 mean) | by construction the pack total |
| pension accrual in year 1 (pounds, billions), I-D1k mid-point label times wealth | 152 | 42 (ONS D.8 2020), 55 (2021), 84 (2022) | 2.7 times the 2021 value |
| non-pension saving in year 1 at the median ratio (pounds, billions) | 13 | 137 (ONS non-pension saving 2021) | not comparable in level (a ratio of income) |
| income (pounds, billions, per household table, FYE 2024 level, gross) | 1312 | 1404 (ONS B.6g 2020), 1468 (2021), 1554 (2022); disposable, a different concept | -11% against 2021 |

The wealth total matches the pack by construction (band wealth over band households); the income gap is a concept and price-year gap (gross against disposable, FYE 2024 income against 2020 to 2022 wealth), reported and not forced.


### Runs: wealth over GDP (index, start = 1.00) and the realised saving ratio (saving including the pension accrual, over cell income, percent; year 0 shows year 1)

| run | saving % | W/GDP y0 | W/GDP y10 | W/GDP y50 | W/GDP y100 | ratio y0 | ratio y10 | ratio y50 | ratio y100 | identity residual |
|---|---|---|---|---|---|---|---|---|---|---|
| A_low_min | -2.61 | 1.00 | 0.94 | 0.78 | 0.68 | 9.0 | 8.4 | 6.4 | 5.3 | 1.2e-12 |
| A_low_median | 1.01 | 1.00 | 0.97 | 0.89 | 0.85 | 12.6 | 12.3 | 11.4 | 10.8 | 1.5e-12 |
| A_low_max | 13.54 | 1.00 | 1.08 | 1.30 | 1.43 | 25.1 | 26.0 | 28.6 | 30.1 | 1.6e-12 |
| A_mid_min | -2.61 | 1.00 | 1.04 | 1.25 | 1.60 | 9.0 | 9.4 | 11.9 | 15.9 | 3.5e-12 |
| A_mid_median | 1.01 | 1.00 | 1.08 | 1.45 | 2.04 | 12.6 | 13.4 | 17.7 | 24.5 | 3.8e-12 |
| A_mid_max | 13.54 | 1.00 | 1.20 | 2.12 | 3.57 | 25.1 | 27.2 | 37.8 | 54.5 | 4.2e-12 |
| A_high_min | -2.61 | 1.00 | 1.17 | 2.55 | 8.29 | 9.0 | 10.7 | 26.3 | 91.1 | 2.3e-11 |
| A_high_median | 1.01 | 1.00 | 1.21 | 2.90 | 9.89 | 12.6 | 14.7 | 33.8 | 112.7 | 2.3e-11 |
| A_high_max | 13.54 | 1.00 | 1.34 | 4.10 | 15.45 | 25.1 | 28.6 | 59.8 | 187.9 | 2.2e-11 |
| legacy | 0.00 | 1.00 | 0.95 | 0.78 | 0.61 | -37.9 | -36.3 | -29.8 | -23.3 | 1.4e-12 |

### Account terms: saving plus gain over opening wealth, against GDP growth 1.57%

| run | year | S/W % | CG/W % | dNW/W % | GDP growth % |
|---|---|---|---|---|---|
| A_low_median | 1 | 1.22 | 0.06 | 1.27 | 1.57 |
| A_low_median | 10 | 1.22 | 0.08 | 1.30 | 1.57 |
| A_low_median | 50 | 1.23 | 0.18 | 1.41 | 1.57 |
| A_low_median | 100 | 1.23 | 0.27 | 1.51 | 1.57 |
| A_mid_median | 1 | 1.22 | 1.13 | 2.34 | 1.57 |
| A_mid_median | 10 | 1.21 | 1.13 | 2.34 | 1.57 |
| A_mid_median | 50 | 1.19 | 1.11 | 2.30 | 1.57 |
| A_mid_median | 100 | 1.17 | 1.08 | 2.25 | 1.57 |
| A_high_median | 1 | 1.22 | 2.20 | 3.42 | 1.57 |
| A_high_median | 10 | 1.20 | 2.37 | 3.57 | 1.57 |
| A_high_median | 50 | 1.15 | 2.84 | 3.99 | 1.57 |
| A_high_median | 100 | 1.13 | 3.03 | 4.16 | 1.57 |
| legacy | 1 | -3.67 | 4.74 | 1.07 | 1.57 |
| legacy | 10 | -3.67 | 4.74 | 1.07 | 1.57 |
| legacy | 50 | -3.67 | 4.74 | 1.07 | 1.57 |
| legacy | 100 | -3.67 | 4.74 | 1.07 | 1.57 |

### Share of wealth by band

| run | year | D1-3 | D4-5 | D6-7 | D8-9 | D10 |
|---|---|---|---|---|---|---|
| A_mid_median | 0 | 2.1 | 7.7 | 16.8 | 32.7 | 40.7 |
| A_mid_median | 10 | 2.2 | 7.7 | 16.9 | 32.7 | 40.5 |
| A_mid_median | 50 | 2.5 | 7.9 | 17.1 | 32.7 | 39.8 |
| A_mid_median | 100 | 2.8 | 8.0 | 17.4 | 32.7 | 39.1 |
| legacy | 0 | 2.1 | 7.7 | 16.8 | 32.7 | 40.7 |
| legacy | 10 | 2.1 | 7.7 | 16.8 | 32.7 | 40.7 |
| legacy | 50 | 2.1 | 7.7 | 16.8 | 32.7 | 40.7 |
| legacy | 100 | 2.1 | 7.7 | 16.8 | 32.7 | 40.7 |

### Sensitivities (return mid-point label, saving median)

| run | W/GDP y10 | y50 | y100 |
|---|---|---|---|
| S_accrual_low | 1.01 | 1.05 | 1.11 |
| A_mid_median | 1.08 | 1.45 | 2.04 |
| S_accrual_high | 1.16 | 2.02 | 3.89 |
| A_mid_median | 1.08 | 1.45 | 2.04 |
| S_retired_0.6 | 1.08 | 1.45 | 2.05 |
| S_retired_0.8 | 1.08 | 1.45 | 2.06 |

Rows in order: accrual low, accrual mid (the main run), accrual high, then retired fraction 0.439 (the ETB value, the main run), 0.6, 0.8.


### Convention B check (return mid, saving median)

Year 1 aggregate dNW: A 3.181900e+08 (per-household money units, summed), B 3.181900e+08; relative difference 0.00e+00. Identity residual A 3.8e-12, B 3.0e-11. The paths then differ (W/GDP y100 2.04 in A, 4.99 in B) because B credits the yield to the class that earns it and A leaves it in net financial wealth: the two conventions are equal in the first year, not in composition afterwards.


### Negative positions (first year)

| run | net worth below zero | net financial wealth below zero |
|---|---|---|
| A_low_min | D1-3|not retired y34, D1-3|retired y74 | D1-3|not retired y1, D1-3|retired y1, D4-5|not retired y9, D4-5|retired y18, D6-7|not retired y19, D6-7|retired y34, D8-9|not retired y34, D8-9|retired y55, D10|not retired y70, D10|retired y96 |
| A_low_median | none | none |
| A_low_max | none | none |
| A_mid_min | D1-3|not retired y34, D1-3|retired y80 | D1-3|not retired y1, D1-3|retired y1, D4-5|not retired y10, D4-5|retired y22, D6-7|not retired y23, D6-7|retired y48, D8-9|not retired y49, D8-9|retired y96 |
| A_mid_median | none | none |
| A_mid_max | none | none |
| A_high_min | D1-3|not retired y36 | D1-3|not retired y1, D1-3|retired y1, D4-5|not retired y11, D4-5|retired y28, D6-7|not retired y31 |
| A_high_median | none | none |
| A_high_max | none | none |
| legacy | none | none |
