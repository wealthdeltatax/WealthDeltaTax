# Can the fund's reserves cover the gap years? (brief 166c, diagnostic)

Status: diagnostic, run. Nothing in the model changed; no design is recommended. The one design question is at the end and is the author's.

## The answer in plain English

On the constant 4.74% path the fund has the money. In the first year retired receipts (M1d) exceed relief, the idle stock above the short reserve is 14 to 30% of GDP, against a largest shortfall of 1.3 to 3.5% of GDP: the stock is 6 to 26 times the first-shortfall gap at 13 of the 15 cells (91 and 210 at the other two; part A, 6 phases). Above *both* reserves it is about 3% of GDP at `median_mid` (and negative at `median_low`), so the cover is the short reserve, not slack.

What the fund does not do today is use it. The core caps R at the lesser of R* and the idle stock, and R* averages recent net receipts, so R lags the retired receipts and the gap years go unfunded. Over 200 level-1 paths the strict F1 is 11% (`safe`) and 16% (`market`) on average over the 15 cells.

Three levers, each with its price:

- **A longer payout window** (`w_pay` 10 or 15) roughly doubles strict F1 (11.3 to 23.3 `safe`; 15.8 to 32.3 `market`). It removes only 13 to 20% of the failing paths, it retires fewer taxes in the short window (M1d 6.12 to 5.87 `safe`, 5.90 to 5.57 `market`), and over 100 years on the constant path it raises total P3 (15.0 to 25.1 at `w_pay` 10). `w_pay` 15 equals 10 in the short window, as the window cannot be longer than the data it has.
- **A shorter `a_window`** (10 with `w_pay` 3) buys little F1 (14.8 `safe`) and costs M1d (5.62) and P1 (7.0 to 6.4).
- **The gap top-up** lifts strict F1 to 87.6% (`safe`) and 95.2% (`market`). It does so by spending the long reserve: P7a (cover at or below zero after fill) is 88.0% (`safe`) and 43.2% (`market`) of paths, minimum cover goes to -1.90 (`safe`), and the fund at year 100 falls from 106 to 74% of GDP (`safe`) and from 1323 to 700% (`market`). P1 and M1d do not change. On the constant path the top-up never has a shortfall, and the long reserve is used (P7b 1.18 to 0.45).

So: the reserves can cover the gap years on the constant path, and a top-up would make them do it, but on stochastic paths the price is the long reserve, exhausted on most `safe` paths. Whether to take that price is the author's ruling (last section).

## Two results that contradict the brief's reading

1. The "about 20% above both reserves" is above the **short** reserve alone (14 to 30% of GDP). Above both reserves it is about 3% of GDP at `median_mid` (-0.5 to 8.3 over the cells at 6 phases, table A).
2. The year-13 gap is a 6-phase result. At the household arm's default of 10 death phases the constant-path first shortfall moves to year 33 to 63 at most points (year 10 to 12 at `max_mid` tm70/tm90, `median_low` and `median_high` tm70/tm90; never at `median_high` tm50), and the short-window P3 is 0 at `min_mid` and `median_mid`. The short-window failure is then mostly a path effect, not a constant-path one.

## Checks

- **Fund copy equals the core at `w_pay` 3.** 60 runs, 72 outputs each; largest absolute difference 0 (`b_fund_copy_check.csv`).
- **6-phase reproduction of 140c.** At 6 phases the constant-path first shortfall is year 13 at all 15 cells, and P3 matches 140c (table A, first block).

## Tables

All values are percent of GDP unless stated. Schedules tm50, tm70, tm90 are k_ln 1, ratio 0.5. Part A and the constant path use the `safe` stand-in return.

### A. Accounting on the constant path (no rule changed)

| point | sched | fill | first shortfall | years with shortfall (of 100) | largest shortfall (year) | S - short reserve in first shortfall year | S - both reserves | (S - short) / shortfall | P3 to end of short window | S - short reserve at window start | P3 / that |
|---|---|---|---|---|---|---|---|---|---|---|---|
| min_mid | tm50 | 7 | 13 | 58 | 1.56 (99) | 18.4 | 2.8 | 16 | 2.38 | 18.6 | 0.13 |
| min_mid | tm70 | 7 | 13 | 58 | 1.58 (99) | 19.9 | 3.1 | 18 | 2.20 | 19.9 | 0.11 |
| min_mid | tm90 | 7 | 13 | 61 | 1.58 (99) | 21.2 | 3.4 | 20 | 2.08 | 21.0 | 0.10 |
| median_mid | tm50 | 7 | 13 | 38 | 1.28 (98) | 18.9 | 2.7 | 19 | 2.03 | 19.3 | 0.11 |
| median_mid | tm70 | 7 | 13 | 39 | 1.29 (98) | 20.5 | 2.9 | 22 | 1.84 | 20.6 | 0.09 |
| median_mid | tm90 | 7 | 13 | 39 | 1.29 (98) | 21.8 | 3.3 | 26 | 1.71 | 21.8 | 0.08 |
| max_mid | tm50 | 7 | 13 | 39 | 3.52 (18) | 20.9 | 1.4 | 91 | 0.43 | 21.9 | 0.02 |
| max_mid | tm70 | 7 | 13 | 36 | 3.47 (13) | 22.5 | 1.7 | 6 | 6.90 | 23.4 | 0.29 |
| max_mid | tm90 | 7 | 13 | 36 | 3.38 (13) | 23.9 | 2.0 | 7 | 6.73 | 24.7 | 0.27 |
| median_low | tm50 | 7 | 13 | 74 | 2.30 (74) | 13.8 | -0.5 | 8 | 3.91 | 15.3 | 0.26 |
| median_low | tm70 | 7 | 13 | 70 | 2.35 (74) | 15.0 | -0.4 | 9 | 3.63 | 16.3 | 0.22 |
| median_low | tm90 | 7 | 13 | 71 | 2.37 (74) | 16.0 | -0.3 | 10 | 3.46 | 17.1 | 0.20 |
| median_high | tm50 | 7 | 13 | 33 | 3.42 (18) | 26.4 | 7.0 | 210 | 0.29 | 23.8 | 0.01 |
| median_high | tm70 | 7 | 13 | 31 | 3.32 (13) | 28.5 | 7.6 | 9 | 6.62 | 25.6 | 0.26 |
| median_high | tm90 | 7 | 13 | 32 | 3.22 (18) | 30.4 | 8.3 | 9 | 6.39 | 27.2 | 0.24 |

Same at the household arm's default of 10 phases:

| point | sched | fill | first shortfall | years with shortfall (of 100) | largest shortfall (year) | S - short reserve in first shortfall year | S - both reserves | (S - short) / shortfall | P3 to end of short window | S - short reserve at window start | P3 / that |
|---|---|---|---|---|---|---|---|---|---|---|---|
| min_mid | tm50 | 7 | 33 | 68 | 1.20 (98) | 20.8 | 6.0 | 136 | 0.00 | 19.3 | 0.00 |
| min_mid | tm70 | 7 | 33 | 68 | 1.26 (98) | 23.2 | 8.0 | 161 | 0.00 | 20.8 | 0.00 |
| min_mid | tm90 | 7 | 33 | 68 | 1.29 (98) | 25.2 | 9.9 | 114 | 0.00 | 22.1 | 0.00 |
| median_mid | tm50 | 7 | 63 | 37 | 0.54 (98) | 19.7 | 5.3 | 86 | 0.00 | 20.0 | 0.00 |
| median_mid | tm70 | 7 | 63 | 37 | 0.58 (98) | 22.2 | 7.9 | 74 | 0.00 | 21.6 | 0.00 |
| median_mid | tm90 | 7 | 61 | 39 | 0.61 (98) | 23.4 | 8.6 | 10471 | 0.00 | 22.9 | 0.00 |
| max_mid | tm50 | 7 | 62 | 1 | 0.01 (62) | 32.8 | 11.5 | 6422 | 0.00 | 22.7 | 0.00 |
| max_mid | tm70 | 7 | 10 | 47 | 1.22 (14) | 24.8 | 2.8 | 23 | 9.32 | 24.4 | 0.38 |
| max_mid | tm90 | 7 | 10 | 47 | 0.84 (14) | 26.4 | 3.0 | 39 | 6.24 | 25.7 | 0.24 |
| median_low | tm50 | 7 | 10 | 91 | 1.95 (100) | 15.9 | 0.4 | 284 | 2.76 | 16.1 | 0.17 |
| median_low | tm70 | 7 | 12 | 87 | 2.01 (100) | 19.3 | 2.7 | 117 | 0.58 | 17.2 | 0.03 |
| median_low | tm90 | 8 | 10 | 91 | 5.39 (100) | 16.5 | -1.4 | 12 | 28.34 | 25.2 | 1.13 |
| median_high | tm50 | 7 | never | 0 | 0.00 (0) |  |  |  | 0.00 | 24.6 | 0.00 |
| median_high | tm70 | 7 | 10 | 41 | 1.05 (11) | 29.1 | 7.0 | 28 | 7.80 | 26.6 | 0.29 |
| median_high | tm90 | 7 | 10 | 41 | 0.97 (33) | 31.1 | 7.5 | 51 | 4.86 | 28.3 | 0.17 |

Reading: "first shortfall" is the first year M1d exceeds relief. The column "(S - short) / shortfall" is the idle stock over the gap in that year (blank: no shortfall). "P3 / that" is short-window P3 over the idle stock at the window start.

### B. Longer payout window

`w_pay` 3 is the core (proved by the copy check). 5, 10, 15 and `a10` (`a_window` 10, `w_pay` 3) are in the D tables below, next to the core. The window is the R* averaging window in post-fill years.

### C. Gap top-up

R = min(max(R*, M1d need), S_pre minus short reserve), where the need is retired M1d at the start of the year as a share of GDP (assumption 1). Results are the `topup` rows below.

### D. Variants side by side

D-1. 200 level-1 paths (seed 20261118), mean over the 5 scenario points and 3 schedules. F1 relaxed is tolerance 1 GDP-point with retirement margin 25%. M1 columns are the short-window means; P6 columns are the fund at years 10, 25, 50 and 100.

**Fund `safe`**

| variant | F1 strict % | F1 tol 1, m 25% % | M1a | M1c | M1d | M1 | P1 | P6 y10 | y25 | y50 | y100 | P7a % | P7b mean | P7b min |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| core | 11.3 | 43.2 | 3.68 | -0.50 | 6.12 | -0.12 | 7.0 | 46 | 51 | 61 | 106 | 0.0 | 0.92 | 0.32 |
| w5 | 12.5 | 54.4 | 3.68 | -0.58 | 5.99 | -0.07 | 7.0 | 46 | 52 | 65 | 118 | 0.0 | 0.91 | 0.28 |
| w10 | 23.3 | 67.5 | 3.68 | -0.66 | 5.87 | -0.03 | 7.0 | 46 | 56 | 76 | 146 | 0.0 | 0.95 | 0.44 |
| w15 | 23.3 | 67.5 | 3.68 | -0.66 | 5.87 | -0.03 | 7.0 | 46 | 58 | 86 | 170 | 0.0 | 0.94 | 0.33 |
| a10 | 14.8 | 54.2 | 3.56 | -0.41 | 5.62 | 0.35 | 6.4 | 44 | 49 | 57 | 99 | 0.3 | 0.92 | -0.43 |
| topup | 87.6 | 91.0 | 3.68 | 0.34 | 6.11 | 0.72 | 7.0 | 46 | 38 | 38 | 74 | 88.0 | 0.02 | -1.90 |

**Fund `market`**

| variant | F1 strict % | F1 tol 1, m 25% % | M1a | M1c | M1d | M1 | P1 | P6 y10 | y25 | y50 | y100 | P7a % | P7b mean | P7b min |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| core | 15.8 | 56.9 | 3.74 | -0.34 | 5.90 | 0.32 | 6.3 | 53 | 91 | 240 | 1323 | 0.0 | 1.16 | 0.65 |
| w5 | 18.1 | 67.8 | 3.74 | -0.45 | 5.73 | 0.39 | 6.3 | 54 | 93 | 255 | 1431 | 0.0 | 1.16 | 0.51 |
| w10 | 32.3 | 80.2 | 3.74 | -0.59 | 5.57 | 0.40 | 6.3 | 54 | 98 | 280 | 1609 | 0.0 | 1.16 | 0.38 |
| w15 | 32.3 | 80.2 | 3.74 | -0.59 | 5.57 | 0.40 | 6.3 | 54 | 100 | 297 | 1732 | 0.0 | 1.15 | 0.41 |
| a10 | 17.0 | 56.0 | 3.72 | -0.27 | 5.89 | 0.38 | 6.1 | 51 | 87 | 231 | 1290 | 0.0 | 1.26 | 0.52 |
| topup | 95.2 | 96.7 | 3.74 | 0.32 | 5.90 | 0.98 | 6.3 | 52 | 72 | 153 | 700 | 43.2 | 0.61 | -1.11 |

D-2. One cell, `median_mid`, tm70. The standard error of an F1 share at 200 paths is 1 to 3.5 points (binomial; the column shows it), so differences under about 5 points are not distinguishable from path noise: in strict F1 `w5` and `a10` against the core are within noise here; `w10`, `w15` and the top-up are not.

**Fund `safe`**

| variant | F1 strict % | F1 tol 1, m 25% % | M1a | M1b | M1c | M1d | P1 | P6 y10 | y25 | y50 | y100 | P7a % | P7b mean | P7b min |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| core | 12.5 ± 2.3 | 45.5 ± 3.5 | 3.42 | 2.82 | -0.42 | 6.12 | 7.0 | 45 | 48 | 50 | 56 | 0.0 | 0.95 | 0.68 |
| w5 | 10.5 ± 2.2 | 54.5 ± 3.5 | 3.42 | 2.82 | -0.49 | 6.00 | 7.0 | 45 | 49 | 53 | 63 | 0.0 | 0.95 | 0.57 |
| w10 | 22.5 ± 3.0 | 65.5 ± 3.4 | 3.42 | 2.82 | -0.54 | 5.90 | 7.0 | 45 | 52 | 61 | 78 | 0.0 | 0.98 | 0.57 |
| w15 | 22.5 ± 3.0 | 65.5 ± 3.4 | 3.42 | 2.82 | -0.54 | 5.90 | 7.0 | 45 | 53 | 67 | 91 | 0.0 | 0.96 | 0.49 |
| a10 | 14.5 ± 2.5 | 57.5 ± 3.5 | 3.30 | 2.82 | -0.36 | 5.48 | 6.4 | 44 | 46 | 47 | 54 | 0.0 | 0.99 | 0.22 |
| topup | 84.0 ± 2.6 | 88.0 ± 2.3 | 3.42 | 2.82 | 0.47 | 6.11 | 7.0 | 44 | 34 | 24 | 29 | 98.0 | -0.07 | -0.90 |

**Fund `market`**

| variant | F1 strict % | F1 tol 1, m 25% % | M1a | M1b | M1c | M1d | P1 | P6 y10 | y25 | y50 | y100 | P7a % | P7b mean | P7b min |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| core | 13.5 ± 2.4 | 59.5 ± 3.5 | 3.48 | 2.82 | -0.32 | 5.77 | 6.2 | 53 | 88 | 232 | 1266 | 0.0 | 1.17 | 0.65 |
| w5 | 14.5 ± 2.5 | 70.0 ± 3.2 | 3.48 | 2.82 | -0.40 | 5.62 | 6.2 | 53 | 91 | 244 | 1345 | 0.0 | 1.17 | 0.55 |
| w10 | 32.5 ± 3.3 | 83.5 ± 2.6 | 3.48 | 2.82 | -0.53 | 5.44 | 6.2 | 53 | 95 | 262 | 1472 | 0.0 | 1.17 | 0.44 |
| w15 | 32.5 ± 3.3 | 83.5 ± 2.6 | 3.48 | 2.82 | -0.53 | 5.44 | 6.2 | 53 | 96 | 273 | 1558 | 0.0 | 1.16 | 0.47 |
| a10 | 15.5 ± 2.6 | 55.0 ± 3.5 | 3.46 | 2.82 | -0.24 | 5.74 | 6.1 | 51 | 85 | 224 | 1234 | 0.0 | 1.27 | 0.55 |
| topup | 95.0 ± 1.5 | 97.0 ± 1.2 | 3.48 | 2.82 | 0.37 | 5.77 | 6.2 | 51 | 68 | 136 | 571 | 44.0 | 0.60 | -0.39 |

D-3. F1 strict by scenario point (`safe`, mean of the 3 schedules):

| point | core | w10 | top-up | top-up P7a % |
|---|---|---|---|---|
| min_mid | 11.5 | 24.7 | 84.5 | 99.0 |
| median_mid | 12.2 | 23.8 | 85.2 | 97.3 |
| max_mid | 10.7 | 22.7 | 91.2 | 80.7 |
| median_low | 6.2 | 16.0 | 80.8 | 97.8 |
| median_high | 16.0 | 29.2 | 96.5 | 65.0 |

D-4. Constant path, `median_mid`, first year of shortfall (relief below M1d) and P3 summed over 100 years. The constant path has no path return, so `safe` and `market` coincide except where the fund return enters P6 and P7b.

| variant | safe: first shortfall | P3 100 y | P6 y25 | P7b | market: first shortfall | P3 100 y | P6 y25 | P7b |
|---|---|---|---|---|---|---|---|---|
| core | 63 | 15.02 | 40 | 1.18 | 63 | 15.02 | 77 | 1.14 |
| w5 | 32 | 21.20 | 41 | 1.18 | 32 | 21.20 | 79 | 1.14 |
| w10 | 40 | 25.09 | 43 | 1.18 | 40 | 25.09 | 84 | 1.14 |
| w15 | 41 | 31.51 | 44 | 1.18 | 41 | 31.51 | 86 | 1.14 |
| a10 | 63 | 15.02 | 38 | 1.17 | 63 | 15.02 | 77 | 1.43 |
| topup | never | 0.00 | 40 | 0.45 | never | 0.00 | 77 | 1.14 |

Reading the costs: the gains in F1 come with (a) fewer retired taxes (M1d falls with `w_pay` and `a_window`), (b) a larger 100-year P3 on the constant path for the longer windows (they delay relief, so more years fall short), and (c) for the top-up, the long reserve. Longer windows raise P6 at years 50 and 100 (the fund grows because it pays less), which is the same cost seen from the stock side.

## Assumptions, labelled for challenge

1. **Top-up need** is M1d at the start of the year (the retire rule replayed per year with the taxes already done), not the year's realised receipts. A need measured on the year-end figure would be smaller or larger depending on timing.
2. **Idle stock** is measured at year-end, S minus the short reserve, then S_pre in the cap. The brief's wording is "S_pre minus short reserve"; the two differ by that year's flows.
3. **Return**: A and D use the `safe` stand-in (net financial class return plus the path's deviation); `market` is shown only in D. Part A is not run on `market` because the constant path has no path deviation to carry.
4. **F1 relaxed** is read as tolerance 1.0 GDP-point and retirement margin 25%, the loosest cell of 083c's grid. Strict is tolerance 0, margin 0.
5. **Paths** are the 089c-style level-1 paths with seed 20261118 and n 200, the same as brief 140c, so the cells are comparable to it.
6. **Six-phase check** uses a local wrapper that overrides `n_phase`, because the household arm now passes it itself (default 10). Both phase counts are reported; the main run is at 10.
7. **`w_pay` above the data** (15) is clamped to the years available, which is why `w15` equals `w10` in short-window F1.
8. **Kernel once per cell**: variants re-run only `rv.revenue` with `rv.fund` replaced at run time; no file was edited, and the copy check shows equality with the core.
9. **Scenario points** are the five labelled points of 140c (none central); the means over them are for compactness, not a central case.

## What was not run

- No fund other than `safe` and `market`; no other schedule than tm50/tm70/tm90.
- No `a_window` other than 10; no top-up variants with a cap on R, a floor on the long reserve, or a share of the idle stock.
- No 1,000-path run; 200 paths only (SE above).
- No change to the register, `outputs.yml`, the gate, `arm.py` or the core.
- The growth hypothesis in the brief is a note, not tested.
- No test suites: no model code changed.

## Reproduce

From the repository root: `python -I model/studies/reserve-diagnostic/reserve_diagnostic.py check | a | d` (about 3 minutes for all). Outputs are the CSVs in `results/reserve-diagnostic/`.

## Question for the author

Should the Sovereign Wealth Fund be allowed to cover retired-tax gaps? On the evidence above, the constant-path reserves are large enough to do so, and a top-up would lift strict F1 from about 11 to 16% to about 88 to 95%. The price is the long reserve: on `safe` paths it is at or below zero after fill on 88% of paths. This is a design ruling, not the agent's call.
