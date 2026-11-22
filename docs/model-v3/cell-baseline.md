# Untaxed cell baseline (brief 110c)

Ten cells (five pack bands by retired or not) run for 100 years with no WDT, using `household_step` under convention A, against the legacy 3.5% rule on the same cells. A first look at the baseline the new arm produces. **Nothing is tuned**: every input is a register row, a held table or a labelled scenario value, and the results are reported as they come. Script: `docs/model-v3/cell-baseline/cell_baseline.py` (rerun from the repository root; deterministic). Paths: `cell_paths.csv` (run, cell, year, positions by class, `dNW`, `S`, `CG`, `CG_wedge`, `O`), `aggregates.csv` (wealth, wealth over GDP, saving ratio, band shares) and `inputs_used.json`. Module: `model_v3/core/cells.py` (layer 2, standalone: the kernel and runner do not import it).

## What came out

- **The path is set by two labelled scenario values, not by saving.** At the mid-point labels (return 5.20%, accrual 1.12%) with the median saving ratio, wealth over GDP is 1.08 of its start at year 10, 1.45 at year 50 and **2.04 at year 100**. Wealth grows 2.3% a year (saving 1.2% of wealth plus holding gain 1.1%) against GDP per head growth of 1.57%, so the ratio rises and keeps rising slowly (2.34% at year 1, 2.25% at year 100). Of the 1.2% saving, 1.12 points are the pension accrual and 0.10 the non-pension saving out of income.
- **The return regime flips the direction.** At the low regime (3.44% total, a holding gain of -1.2% on pension and net financial wealth) wealth grows 1.3% to 1.5% a year, below GDP: the ratio **falls to 0.85** at year 100 (0.68 at the minimum saving ratio, 1.43 at the maximum). At the high regime (6.96%, a gain of 3.1%) wealth grows 3.4% to 4.2% a year and the ratio reaches **9.9** (8.3 to 15.4). The ratio is flat only where saving plus gain equals GDP growth, which none of the nine runs hits exactly; the low regime at the median saving ratio comes closest (1.27% at year 1 rising to 1.51% at year 100 against 1.57%).
- **The accrual label matters more than the saving ratio.** At the mid return and median saving, the accrual at its low value (0.41%) gives 1.11 at year 100; at the mid-point label (1.12%) 2.04; at the high value (1.84%) 3.89. The mid-point label gives a year-1 accrual of 152 billion pounds against 55 billion in the ONS D.8 series for 2021 (2.7 times; 42 in 2020, 84 in 2022): the mid-point of a range that falls from 1.84% (1998) to 0.41% (2020) overstates today's flow on today's larger wealth. It is a label, not an estimate, and it is not changed here.
- **The saving ratio is small beside the accrual.** The ONS non-pension saving ratio runs from -2.61% (2005) through a median of 1.01% to 13.54% (2020, the pandemic year). At the minimum, every cell's net financial wealth goes negative (D1-3 from year 1, D10 from about year 70 at the low regime) and the poorest cell's net worth goes negative at year 34 (a limit of the flat-ratio design: no borrowing constraint, no gradient); at the maximum the realised ratio, accrual included, starts at 25% of income. These are reported, not corrected.
- **Retired fraction is not a driver here.** The held ETB (FYE 2024, Tables 3a and 4a) gives retired households 0.439 of non-retired households' mean gross income (household-weighted over the five quintiles). Running 0.6 and 0.8 instead moves wealth over GDP at year 100 from 2.04 to 2.05 and 2.06: the retired cells' non-pension saving is small and pension is not drawn.
- **Legacy, untaxed:** wealth over GDP is 0.95, 0.78 and **0.61** at years 10, 50 and 100, the same as the 0.62 of 090c (tax off). The 47% there includes the tax. In account terms the legacy rule is saving -3.67% of wealth (consumption of 3.5% of wealth, grown) plus gain 4.74%: 1.07% growth against GDP 1.57%, every year, so the ratio falls without limit. It has no income side: the same account puts saving at about -38% of income (not a household saving ratio).
- **Convention B agrees with A in the first year** (same aggregate `dNW`, zero relative difference) and the identity closes in both. The paths then differ (2.04 in A, 4.99 in B at year 100) because B credits the yield to the class that earns it and A leaves it in net financial wealth: the conventions agree on the account, not on composition, so any later comparison must fix one convention.
- **The identity** closes to below 3e-11 in every year of every run, and the legacy arm reproduces `grow_and_consume` on the same cells (a test, relative 1e-12).

## Inputs, as used

| input | value | source |
|---|---|---|
| households and persons by cell | band households (pack, a tenth per decile) split by the person shares of `cell_weights` | pack v2; a person-based proxy for stage |
| wealth per household | band mean (pack `wealth_total` over `households`), the same for both stages; classes from `band_composition`; debt netted inside them, so debt 0 | pack; no stage gradient is held |
| income per household | I-D9a (D1-3 takes its low bound, 40,200), I-D9b, I-D9c, I-D9d, central; retired cells 0.4386 of it | register; ETB FYE 2024 Tables 3a and 4a for the fraction |
| income growth | real GDP per head, 1.57% a year (the arithmetic mean the runner uses) | `runner.context` |
| saving | one uniform ratio of income, non-pension: min -2.61%, median 1.01%, max 13.54% (1998 to 2025) | `ratio_nonpension_part_pct`, 101r |
| property return | gain 1.6455% (F-20, JST housing, all years); the yield 3.758% is inside saving | `jst_split_stats` |
| pension and net financial return | total I-D1h and I-D1i (3.44, 5.20, 6.96); the gain is the total minus the regime's JST portfolio yield (4.6648% in 1947 to 1979, 3.8575% in 1980 to 2019, their mean for the mid-point) | register; `jst_split_stats` |
| physical return | 0 (I-D1j) | register |
| pension accrual | I-D1k as a share of opening net worth, 1.12% (0.41% and 1.84% as sensitivities), added to saving and to the pension class | register |
| settlement | none (T_WDT = 0); sink for saving is net financial wealth | design |

## Limits

Pension is accumulated and never drawn (no withdrawal flow), so the retired cells grow their pension like the others. No transition between cells, no mortality or inheritance, no population or household growth: the weights are fixed and only per-household values move. Debt is netted inside the 102r classes, so the erosion wedge line is 0 throughout. Saving is a flat ratio of income with no wealth gradient (a later sensitivity). Wealth is the 2020 to 2022 pack level and income the FYE 2024 level, with no deflation between them. Income is gross and the ONS comparison is to disposable income.

## Answers to the open questions

- **Retired fraction:** from the held ETB, 0.4386 (the brief's fallback 0.6, range 0.4 to 0.8, is shown as a sensitivity and changes nothing material).
- **Aggregate wealth over GDP comparable with the pack's:** yes. Cells are weighted by households, so total wealth is the pack's 13,569 billion pounds (0.01% from rounding) and wealth over GDP starts at 6.14. The persons in `cell_weights` (50.204 million) equal households times the low bound of I-D4h (1.86 adults), and are 3.6% below the central 1.93; persons are not used as weights.

## Tables

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
