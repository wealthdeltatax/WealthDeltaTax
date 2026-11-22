# The taxed household arm: the account of each line (briefs 118c and 119c, W5b)

For the author's review. One row per line and saving value for years 1 and 30; years 10 and 100 are in `household-arm-account/account_table.csv` (14 lines, three saving values, years 1, 10, 30 and 100). **No revenue, fund or burden number appears here or in the CSV.**

## What was run

`python -I docs/model-v3/household-arm-account/account_table.py`: the taxed household hook (`runner/arm.py`, convention A, default arm still legacy) on the 14 lines, one path, 100 years, each line run alone (the kernel treats lines independently). Schedule: the digest's centre grid point, tau_0 0.04, tau_m 0.7, k_ln 1, threshold ratio 0.5 (logistic in ln W); register central inputs (the tail lines' pension capped at I-D1l, 119c), mid return regime (0.052 total, yield 0.0426115 so net financial and pension gain 0.0094, property 0.016455, physical 0), income growth 0.0157, pension accrual 0.0483 of income (as observed), incomes scaled to the B.6g factor 1.3733 (`cell-baseline/inputs_used.json`), wealth scale and behavioural loss as the runner shapes the base; Route C verified with lam_C and Route D with lam_D from the register. Routes: the base's A, B, C, D split, sale mode for Route B. Deaths at years 30, 60 and 90; the horizon (year 100) settled. Saving values (the ONS non-pension saving ratio, 1998 to 2025): min -0.0261, median 0.0101, max 0.1354; none is called central.

Units: millions of pounds per adult, real pounds of the pack's CPI basis. Ratios are fractions (1 = 100%).

## Columns

- `dNW`: closing minus opening net worth of the year (pension included). `S`: saving, labour income plus pension accrual minus consumption. `CG`: holding gains (property, net financial, physical, pension; a negative property or net financial balance earns nothing). `T_WDT`: value moved to the state in the year, taken pro rata from the positive non-pension class balances; pension is never sold. A death year (30, 60, 90) includes the death tax, the settlement of Routes B and D and the heir's tax on the receipt; year 100 includes the horizon settlement.
- `identity_residual`: dNW - (S + CG - T_WDT), checked to 1e-9 in every line and year of the run (largest in the CSV 1.1e-11; the three richest lines carry values of 1e4, so their absolute residuals are larger than the others).
- `pension_share` (added by 119c): the pension balance over total wealth at the end of the year.
- `unpaid_B`: the kernel's cumulative payment shortfall, the amount a line was assessed and could not pay from its non-pension wealth. A model alarm, expected zero.
- `pay_over_net_financial`, `pay_over_nonpension`: the year's payment over the net financial balance and over the non-pension total, both after growth and saving, before the payment (0 where nothing is paid).

## Shortfall count (rerun with the tail pension ceiling, brief 119c)

`shortfall_lines` is **empty** in all three saving values: no line has a payment shortfall in any year (`unpaid_B` is 0 in every row; the largest payment over non-pension wealth is 0.6025, in a death year). The year-100 rows are present for all 14 lines in each saving value (168 rows, 14 lines times three saving values times years 1, 10, 30 and 100). The account identity holds to 1.1e-11 in every row, and no line has negative total wealth. The 118c run had stopped RL3, RL2 and RL1 in year 69.

What changed: the tail lines' opening pension is at most **0.386 £m per adult, real** (register row I-D1l), the D10 mean pension per adult (WAS Round 8, April 2020 to March 2022: D10 pension share 36.4% of D10 wealth, times D10 mean wealth per adult of 1.06 £m). **This is a labelled scenario, not a measurement.** It is a ceiling because no distribution of pension wealth is held (and no unit-record licence); the replacement would be the p90 or p99 of private pension wealth, or a lifetime-allowance-based figure, from an ONS pension-wealth-by-percentile table, a one-value change in I-D1l. The wealth the ceiling displaces went to property, net financial and physical pro rata to D10's mix. The ceiling applies to the opening balance only: accrual (4.83% of income) and the pension's gain continue on top of it, so a line's pension can grow past 0.386 later (D10a, whose proportional pension 0.24 is below the ceiling, goes from 0.37 of its wealth at year 1 to 0.64 at year 100).

Pension share of wealth by tail line, median saving (the shares at opening before the ceiling were 0.364 in every tail line):

| line | opening before | year 1 | year 30 | year 100 |
|---|---:|---:|---:|---:|
| D10a | 0.364 | 0.366 | 0.46 | 0.64 |
| D10b | 0.364 | 0.098 | 0.17 | 0.39 |
| RL3 | 0.364 | 0.00033 | 0.0011 | 0.027 |
| RL2 | 0.364 | 0.000073 | 0.00024 | 0.0069 |
| RL1 | 0.364 | 0.000010 | 0.000033 | 0.00098 |

D10a is not affected by the ceiling (its proportional pension is below it), and every row of D1 to D10a is bit for bit that of 118c; D10b to RL1 are capped. The saving value moves the shares of D10a (year 100: 0.41 at max saving, 0.77 at min) and D10b (0.34 to 0.40), and the richest three lines not at all to two digits; all are in the CSV column `pension_share`.

Year 100, median saving, the three lines that were blank in 118c (millions of pounds per adult): RL3 dNW -36.97, S 0.0139, CG 1.536, T_WDT 38.52, payment over non-pension wealth 0.366; RL2 dNW -168.9, CG 6.387, T_WDT 175.3, 0.398; RL1 dNW -1237, CG 45.61, T_WDT 1283, 0.407 (the year-100 rows include the horizon settlement). All three rows have `unpaid_B` 0 and an identity residual of zero to the printed digits. **No revenue, fund or burden number is computed or written here.**

## Other things that look odd

- No line has negative total wealth in any year of any run; the negative class shares of D1 (property and net financial) make no payment (D1 pays nothing in the years shown).
- In the death year (30) the three richest lines pay 2.2 times their net financial balance (but 0.60 of non-pension wealth, so property and physical assets are sold; min saving, 2.21 to 2.22). D10b pays 1.32 times its net financial balance in year 30 (0.35 of non-pension; min saving).
- A death year's dNW is negative and large for D6 to RL1 (D5 is barely positive) (it contains the heir's tax on the whole receipt, pension included, assessed from zero), so the death year is not a year of ordinary saving and gain.
- Payment over non-pension wealth never exceeds 0.6025 (no row above 1; the script's own check counts none).
- Route D's accrued liability is settled by the kernel (`settle_D`) in death years and at the horizon; the hook sees it as value moved and pays it the same way.

## The death step and the pension

The death step needs no separate path for the pension. The pension balance is held in `book.pen` outside the route units; the kernel's death steps never move it, and the hook leaves it untouched, so it passes to the next generation unchanged (tests: `book.pen` equals the pension class after every step, including death years). What the death step does move is value from the units, and that is paid from the non-pension classes by `HouseholdHook.reconcile`, because the kernel calls no hook after `step_death` and `settle_terminal`: the gap between the class total and the book's family value is the payment. `revenue.run_lines` does not call `reconcile` (the file is outside this brief), so a run through it pays deaths and the horizon from the classes only at the start of the next year's `pre`; the final settlement is not read by anything after it.

## Table (years 1 and 30)

| line | saving | year | dNW | S | CG | T_WDT | payment / net financial | payment / non-pension | note |
|---|---|---:|---:|---:|---:|---:|---:|---:|---|
| D1 | min (-0.0261) | 1 | 0.0006457 | 0.0006356 | 1.006e-05 | 0 | 0 | 0 |  |
| D1 | min (-0.0261) | 30 | 0.001546 | 0.0009987 | 0.0005472 | 0 | 0 | 0 | death year |
| D2 | min (-0.0261) | 1 | 0.0006824 | 0.0006356 | 4.683e-05 | 0 | 0 | 0 |  |
| D2 | min (-0.0261) | 30 | 0.001587 | 0.0009987 | 0.0005882 | 0 | 0 | 0 | death year |
| D3 | min (-0.0261) | 1 | 0.0008798 | 0.0006356 | 0.0002442 | 0 | 0 | 0 |  |
| D3 | min (-0.0261) | 30 | 0.001848 | 0.0009987 | 0.0008492 | 0 | 0 | 0 | death year |
| D4 | min (-0.0261) | 1 | 0.001514 | 0.0007953 | 0.0007187 | 0 | 0 | 0 |  |
| D4 | min (-0.0261) | 30 | 0.002932 | 0.00125 | 0.001682 | 0 | 0 | 0 | death year |
| D5 | min (-0.0261) | 1 | 0.00212 | 0.0007953 | 0.001324 | 0 | 0 | 0 |  |
| D5 | min (-0.0261) | 30 | 0.003784 | 0.00125 | 0.002535 | 0 | 0 | 0 | death year |
| D6 | min (-0.0261) | 1 | 0.002712 | 0.0009961 | 0.001816 | 0.0001002 | 0.008015 | 0.0009215 |  |
| D6 | min (-0.0261) | 30 | -1.01e-05 | 0.001565 | 0.00334 | 0.004915 | inf | 0.04631 | death year |
| D7 | min (-0.0261) | 1 | 0.003404 | 0.0009961 | 0.00258 | 0.0001721 | 0.008014 | 0.001132 |  |
| D7 | min (-0.0261) | 30 | -0.003632 | 0.001565 | 0.004338 | 0.009535 | inf | 0.05726 | death year |
| D8 | min (-0.0261) | 1 | 0.00436 | 0.00113 | 0.003527 | 0.0002968 | 0.008531 | 0.001459 |  |
| D8 | min (-0.0261) | 30 | -0.009342 | 0.001776 | 0.005618 | 0.01674 | inf | 0.07298 | death year |
| D9 | min (-0.0261) | 1 | 0.005702 | 0.00113 | 0.005124 | 0.000552 | 0.009341 | 0.001942 |  |
| D9 | min (-0.0261) | 30 | -0.02288 | 0.001776 | 0.007732 | 0.03239 | 1.703 | 0.09591 | death year |
| D10a | min (-0.0261) | 1 | 0.00694 | 0.001129 | 0.006667 | 0.0008564 | 0.007685 | 0.002307 |  |
| D10a | min (-0.0261) | 30 | -0.04069 | 0.001774 | 0.009777 | 0.05224 | 0.6323 | 0.1157 | death year |
| D10b | min (-0.0261) | 1 | 0.03229 | 0.001129 | 0.04908 | 0.01791 | 0.01641 | 0.004965 |  |
| D10b | min (-0.0261) | 30 | -1.497 | 0.001774 | 0.06596 | 1.564 | 1.315 | 0.3462 | death year |
| RL3 | min (-0.0261) | 1 | 6.29 | 0.001129 | 14.97 | 8.678 | 0.02413 | 0.007304 |  |
| RL3 | min (-0.0261) | 30 | -823.3 | 0.001774 | 18.62 | 841.9 | 2.21 | 0.6008 | death year |
| RL2 | min (-0.0261) | 1 | 28.43 | 0.001129 | 67.81 | 39.38 | 0.02416 | 0.007314 |  |
| RL2 | min (-0.0261) | 30 | -3738 | 0.001774 | 84.32 | 3823 | 2.215 | 0.6022 | death year |
| RL1 | min (-0.0261) | 1 | 207.6 | 0.001129 | 495.5 | 287.9 | 0.02417 | 0.007316 |  |
| RL1 | min (-0.0261) | 30 | -2.733e+04 | 0.001774 | 616 | 2.795e+04 | 2.216 | 0.6025 | death year |
| D1 | median (0.0101) | 1 | 0.001679 | 0.001669 | 1.006e-05 | 0 | 0 | 0 |  |
| D1 | median (0.0101) | 30 | 0.003249 | 0.002623 | 0.0006256 | 0 | 0 | 0 | death year |
| D2 | median (0.0101) | 1 | 0.001716 | 0.001669 | 4.683e-05 | 0 | 0 | 0 |  |
| D2 | median (0.0101) | 30 | 0.00333 | 0.002623 | 0.0007073 | 0 | 0 | 0 | death year |
| D3 | median (0.0101) | 1 | 0.001914 | 0.001669 | 0.0002442 | 0 | 0 | 0 |  |
| D3 | median (0.0101) | 30 | 0.00361 | 0.002623 | 0.0009872 | 0 | 0 | 0 | death year |
| D4 | median (0.0101) | 1 | 0.002808 | 0.002089 | 0.0007187 | 0 | 0 | 0 |  |
| D4 | median (0.0101) | 30 | 0.005156 | 0.003282 | 0.001874 | 0 | 0 | 0 | death year |
| D5 | median (0.0101) | 1 | 0.003413 | 0.002089 | 0.001324 | 0 | 0 | 0 |  |
| D5 | median (0.0101) | 30 | 0.0008018 | 0.003282 | 0.002756 | 0.005236 | 0.1951 | 0.04125 | death year |
| D6 | median (0.0101) | 1 | 0.004273 | 0.002616 | 0.001816 | 0.0001593 | 0.01129 | 0.001444 |  |
| D6 | median (0.0101) | 30 | -0.001686 | 0.004111 | 0.003636 | 0.009433 | 0.262 | 0.05553 | death year |
| D7 | median (0.0101) | 1 | 0.004945 | 0.002616 | 0.00258 | 0.0002517 | 0.0109 | 0.001638 |  |
| D7 | median (0.0101) | 30 | -0.00655 | 0.004111 | 0.004729 | 0.01539 | 0.327 | 0.06671 | death year |
| D8 | median (0.0101) | 1 | 0.00608 | 0.002969 | 0.003527 | 0.0004161 | 0.01136 | 0.002027 |  |
| D8 | median (0.0101) | 30 | -0.01427 | 0.004665 | 0.006166 | 0.0251 | 0.3819 | 0.08323 | death year |
| D9 | median (0.0101) | 1 | 0.007376 | 0.002969 | 0.005124 | 0.0007168 | 0.01176 | 0.002506 |  |
| D9 | median (0.0101) | 30 | -0.03 | 0.004665 | 0.008334 | 0.043 | 0.4547 | 0.1054 | death year |
| D10a | median (0.0101) | 1 | 0.008572 | 0.002965 | 0.006667 | 0.001061 | 0.009364 | 0.002844 |  |
| D10a | median (0.0101) | 30 | -0.04968 | 0.004659 | 0.01036 | 0.06469 | 0.4124 | 0.1244 | death year |
| D10b | median (0.0101) | 1 | 0.03347 | 0.002965 | 0.04908 | 0.01857 | 0.01699 | 0.005145 |  |
| D10b | median (0.0101) | 30 | -1.519 | 0.004659 | 0.06629 | 1.59 | 1.265 | 0.3481 | death year |
| RL3 | median (0.0101) | 1 | 6.291 | 0.002965 | 14.97 | 8.679 | 0.02413 | 0.007305 |  |
| RL3 | median (0.0101) | 30 | -823.3 | 0.004659 | 18.62 | 842 | 2.21 | 0.6008 | death year |
| RL2 | median (0.0101) | 1 | 28.43 | 0.002965 | 67.81 | 39.38 | 0.02416 | 0.007314 |  |
| RL2 | median (0.0101) | 30 | -3738 | 0.004659 | 84.32 | 3823 | 2.215 | 0.6022 | death year |
| RL1 | median (0.0101) | 1 | 207.6 | 0.002965 | 495.5 | 287.9 | 0.02417 | 0.007316 |  |
| RL1 | median (0.0101) | 30 | -2.733e+04 | 0.004659 | 616 | 2.795e+04 | 2.216 | 0.6025 | death year |
| D1 | max (0.1354) | 1 | 0.005265 | 0.005255 | 1.006e-05 | 0 | 0 | 0 |  |
| D1 | max (0.1354) | 30 | 0.01027 | 0.008256 | 0.00201 | 0 | 0 | 0 | death year |
| D2 | max (0.1354) | 1 | 0.005301 | 0.005255 | 4.683e-05 | 0 | 0 | 0 |  |
| D2 | max (0.1354) | 30 | 0.003945 | 0.008256 | 0.002093 | 0.006405 | 0.03815 | 0.03593 | death year |
| D3 | max (0.1354) | 1 | 0.005499 | 0.005255 | 0.0002442 | 0 | 0 | 0 |  |
| D3 | max (0.1354) | 30 | 0.002728 | 0.008256 | 0.002357 | 0.007885 | 0.04684 | 0.04142 | death year |
| D4 | max (0.1354) | 1 | 0.007294 | 0.006575 | 0.0007187 | 0 | 0 | 0 |  |
| D4 | max (0.1354) | 30 | -0.001915 | 0.01033 | 0.00352 | 0.01577 | 0.07569 | 0.05931 | death year |
| D5 | max (0.1354) | 1 | 0.007899 | 0.006575 | 0.001324 | 0 | 0 | 0 |  |
| D5 | max (0.1354) | 30 | -0.006753 | 0.01033 | 0.004353 | 0.02144 | 0.101 | 0.06971 | death year |
| D6 | max (0.1354) | 1 | 0.009678 | 0.008235 | 0.001816 | 0.0003728 | 0.01889 | 0.003216 |  |
| D6 | max (0.1354) | 30 | -0.01536 | 0.01294 | 0.005618 | 0.03391 | 0.1273 | 0.08597 | death year |
| D7 | max (0.1354) | 1 | 0.01028 | 0.008235 | 0.00258 | 0.0005357 | 0.01866 | 0.003362 |  |
| D7 | max (0.1354) | 30 | -0.02389 | 0.01294 | 0.006669 | 0.0435 | 0.1573 | 0.09619 | death year |
| D8 | max (0.1354) | 1 | 0.01203 | 0.009346 | 0.003527 | 0.0008396 | 0.01952 | 0.003967 |  |
| D8 | max (0.1354) | 30 | -0.03965 | 0.01468 | 0.008307 | 0.06264 | 0.1937 | 0.1143 | death year |
| D9 | max (0.1354) | 1 | 0.01317 | 0.009346 | 0.005124 | 0.001297 | 0.01927 | 0.004434 |  |
| D9 | max (0.1354) | 30 | -0.06174 | 0.01468 | 0.01039 | 0.08682 | 0.2484 | 0.134 | death year |
| D10a | max (0.1354) | 1 | 0.01422 | 0.009333 | 0.006667 | 0.001777 | 0.01486 | 0.004685 |  |
| D10a | max (0.1354) | 30 | -0.08676 | 0.01466 | 0.01235 | 0.1138 | 0.279 | 0.1509 | death year |
| D10b | max (0.1354) | 1 | 0.03755 | 0.009333 | 0.04908 | 0.02086 | 0.01897 | 0.005767 |  |
| D10b | max (0.1354) | 30 | -1.599 | 0.01466 | 0.06747 | 1.681 | 1.129 | 0.3545 | death year |
| RL3 | max (0.1354) | 1 | 6.293 | 0.009333 | 14.97 | 8.683 | 0.02414 | 0.007308 |  |
| RL3 | max (0.1354) | 30 | -823.4 | 0.01466 | 18.62 | 842 | 2.209 | 0.6009 | death year |
| RL2 | max (0.1354) | 1 | 28.44 | 0.009333 | 67.81 | 39.39 | 0.02416 | 0.007315 |  |
| RL2 | max (0.1354) | 30 | -3738 | 0.01466 | 84.32 | 3823 | 2.214 | 0.6022 | death year |
| RL1 | max (0.1354) | 1 | 207.6 | 0.009333 | 495.5 | 287.9 | 0.02417 | 0.007316 |  |
| RL1 | max (0.1354) | 30 | -2.733e+04 | 0.01466 | 616 | 2.795e+04 | 2.216 | 0.6025 | death year |
