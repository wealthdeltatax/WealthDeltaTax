# The taxed household arm: the account of each line (brief 118c, W5b)

For the author's review. One row per line and saving value for years 1 and 30; years 10 and 100 are in `household-arm-account/account_table.csv` (14 lines, three saving values, years 1, 10, 30 and 100). **No revenue, fund or burden number appears here or in the CSV.**

## What was run

`python -I docs/model-v3/household-arm-account/account_table.py`: the taxed household hook (`runner/arm.py`, convention A, default arm still legacy) on the 14 lines, one path, 100 years, each line run alone (the kernel treats lines independently). Schedule: the digest's centre grid point, tau_0 0.04, tau_m 0.7, k_ln 1, threshold ratio 0.5 (logistic in ln W); register central inputs, mid return regime (0.052 total, yield 0.0426115 so net financial and pension gain 0.0094, property 0.016455, physical 0), income growth 0.0157, pension accrual 0.0483 of income (as observed), incomes scaled to the B.6g factor 1.3733 (`cell-baseline/inputs_used.json`), wealth scale and behavioural loss as the runner shapes the base; Route C verified with lam_C and Route D with lam_D from the register. Routes: the base's A, B, C, D split, sale mode for Route B. Deaths at years 30, 60 and 90; the horizon (year 100) settled. Saving values (the ONS non-pension saving ratio, 1998 to 2025): min -0.0261, median 0.0101, max 0.1354; none is called central.

Units: millions of pounds per adult, real pounds of the pack's CPI basis. Ratios are fractions (1 = 100%).

## Columns

- `dNW`: closing minus opening net worth of the year (pension included). `S`: saving, labour income plus pension accrual minus consumption. `CG`: holding gains (property, net financial, physical, pension; a negative property or net financial balance earns nothing). `T_WDT`: value moved to the state in the year, taken pro rata from the positive non-pension class balances; pension is never sold. A death year (30, 60, 90) includes the death tax, the settlement of Routes B and D and the heir's tax on the receipt; year 100 includes the horizon settlement.
- `identity_residual`: dNW - (S + CG - T_WDT), checked to 1e-9 in every line and year of the run (largest in the CSV 5e-12; the three richest lines carry values of 1e4, so their absolute residuals are larger than the others).
- `unpaid_B`: the kernel's cumulative payment shortfall, the amount a line was assessed and could not pay from its non-pension wealth. A model alarm, expected zero.
- `pay_over_net_financial`, `pay_over_nonpension`: the year's payment over the net financial balance and over the non-pension total, both after growth and saving, before the payment (0 where nothing is paid).

## Shortfall count

`shortfall_lines` is **not empty** in this run: three lines, RL3, RL2 and RL1, have a payment shortfall in year 69 under all three saving values (unpaid_B in year 69, median saving: RL3 1.64, RL2 13.3, RL1 107.7 millions per adult). The payment of that year equals the whole non-pension wealth of the line (ratio 1 within 1e-12). The model is expected to give zero, so this is reported as a model error, with its inputs above. The hook cannot carry a line with no non-pension wealth (no route units: the next year's growth and flow shares are undefined), so those lines stop in year 69; their year 100 rows are blank, with the status. In every other line and year `unpaid_B` is 0 and I1 holds to 1e-9. The test runs of the hook (`tests/model_v3/test_household_tax.py`: 12 years with no deaths, 9 years with deaths every 4 years in Route B sale and lien modes, the horizon, a schedule of tau_0 0.05 and tau_m 0.5) have `shortfall_lines` empty.

What the table shows about the cause, stated as observations: the kernel assesses the tax on the delta of total wealth with the pension balance in it, while the payment can only come from non-pension wealth. In RL1 (median saving), pension is 37% of wealth at year 5 (1.5e4 beside 2.5e4 non-pension) and keeps growing (accrual plus its gain), while the non-pension total is 2.7e4 at year 30, 1.0e4 after the first death (year 35), 5.8e2 at year 65 and nothing at year 69. The payment takes 1.0% of non-pension wealth in year 1 for the three richest lines and 62% of it in the first death year. The saving value changes none of this (the stop year is 69 in all three).

## Other things that look odd

- No line has negative total wealth in any year of any run; the negative class shares of D1 (property and net financial) make no payment (D1 pays nothing in the years shown).
- In the death year (30) the three richest lines pay 2.27 times their net financial balance (but 0.62 of non-pension wealth, so property and physical assets are sold). D10b pays 1.28 times its net financial balance in year 30 (0.35 of non-pension).
- A death year's dNW is negative and large for D6 to RL1 (D5 is barely positive) (it contains the heir's tax on the whole receipt, pension included, assessed from zero), so the death year is not a year of ordinary saving and gain.
- Payment over non-pension wealth never exceeds 1; the four rows above 1 in the script's own check are the shortfall rows equal to 1 within 1e-12.
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
| D10b | min (-0.0261) | 1 | 0.03002 | 0.001129 | 0.04554 | 0.01664 | 0.02165 | 0.006545 |  |
| D10b | min (-0.0261) | 30 | -1.007 | 0.001774 | 0.0591 | 1.068 | 1.359 | 0.3525 | death year |
| RL3 | min (-0.0261) | 1 | 5.686 | 0.001129 | 13.53 | 7.845 | 0.03428 | 0.01038 |  |
| RL3 | min (-0.0261) | 30 | -484.1 | 0.001774 | 16.04 | 500.1 | 2.265 | 0.6159 | death year |
| RL2 | min (-0.0261) | 1 | 25.7 | 0.001129 | 61.3 | 35.6 | 0.03434 | 0.01039 |  |
| RL2 | min (-0.0261) | 30 | -2197 | 0.001774 | 72.66 | 2270 | 2.27 | 0.6172 | death year |
| RL1 | min (-0.0261) | 1 | 187.7 | 0.001129 | 447.9 | 260.2 | 0.03435 | 0.0104 |  |
| RL1 | min (-0.0261) | 30 | -1.606e+04 | 0.001774 | 530.9 | 1.659e+04 | 2.271 | 0.6176 | death year |
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
| D10b | median (0.0101) | 1 | 0.0312 | 0.002965 | 0.04554 | 0.0173 | 0.02245 | 0.006799 |  |
| D10b | median (0.0101) | 30 | -1.028 | 0.004659 | 0.05945 | 1.092 | 1.282 | 0.3547 | death year |
| RL3 | median (0.0101) | 1 | 5.687 | 0.002965 | 13.53 | 7.846 | 0.03429 | 0.01038 |  |
| RL3 | median (0.0101) | 30 | -484.1 | 0.004659 | 16.04 | 500.1 | 2.265 | 0.6159 | death year |
| RL2 | median (0.0101) | 1 | 25.7 | 0.002965 | 61.3 | 35.6 | 0.03434 | 0.01039 |  |
| RL2 | median (0.0101) | 30 | -2197 | 0.004659 | 72.66 | 2270 | 2.27 | 0.6172 | death year |
| RL1 | median (0.0101) | 1 | 187.7 | 0.002965 | 447.9 | 260.2 | 0.03435 | 0.0104 |  |
| RL1 | median (0.0101) | 30 | -1.606e+04 | 0.004659 | 530.9 | 1.659e+04 | 2.271 | 0.6176 | death year |
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
| D10b | max (0.1354) | 1 | 0.03529 | 0.009333 | 0.04554 | 0.01959 | 0.0252 | 0.007677 |  |
| D10b | max (0.1354) | 30 | -1.102 | 0.01466 | 0.06068 | 1.178 | 1.091 | 0.3621 | death year |
| RL3 | max (0.1354) | 1 | 5.69 | 0.009333 | 13.53 | 7.85 | 0.0343 | 0.01038 |  |
| RL3 | max (0.1354) | 30 | -484.2 | 0.01466 | 16.04 | 500.2 | 2.263 | 0.6159 | death year |
| RL2 | max (0.1354) | 1 | 25.71 | 0.009333 | 61.3 | 35.6 | 0.03434 | 0.0104 |  |
| RL2 | max (0.1354) | 30 | -2197 | 0.01466 | 72.66 | 2270 | 2.27 | 0.6172 | death year |
| RL1 | max (0.1354) | 1 | 187.7 | 0.009333 | 447.9 | 260.2 | 0.03435 | 0.0104 |  |
| RL1 | max (0.1354) | 30 | -1.606e+04 | 0.01466 | 530.9 | 1.659e+04 | 2.271 | 0.6176 | death year |
