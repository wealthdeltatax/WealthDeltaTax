# Untaxed cell baseline (brief 110c, rerun by 111c)

**Status (2026-11-22).** The sections from "What came out" to "Answers to the open questions" are the first run (110c, the accrual as a share of opening net worth, withdrawn). The current run, with the accrual on income and income scaled to B.6g 2024, is the last section, "Rerun with the accrual on income", and its tables replace the 110c tables; the CSVs hold the current run only.

Ten cells (five pack bands by retired or not) run for 100 years with no WDT, using `household_step` under convention A, against the legacy 3.5% rule on the same cells. A first look at the baseline the new arm produces. **Nothing is tuned**: every input is a register row, a held table or a labelled scenario value, and the results are reported as they come. Script: `docs/model-v3/cell-baseline/cell_baseline.py` (rerun from the repository root; deterministic). Paths: `cell_paths.csv` (run, cell, year, positions by class, `dNW`, `S`, `CG`, `CG_wedge`, `O`), `aggregates.csv` (wealth, wealth over GDP, saving ratio, band shares) and `inputs_used.json`. Module: `model_v3/core/cells.py` (layer 2, standalone: the kernel and runner do not import it).

> **Superseded in part by the rerun below (brief 111c).** The sections "What came out", "Inputs, as used" (pension accrual row), "Limits" and "Answers" and the run tables describe the 110c baseline, where the pension accrual was a share of opening net worth (I-D1k at 1.12%, a mid-point label). That basis is withdrawn. The wealth-over-GDP figures that stand are those of "Rerun with the accrual on income": 0.75, 1.29 and 4.42 at year 100 across the return regimes, median saving. The legacy path (0.61) and the identity and convention findings are unchanged.

## What came out (110c, superseded)

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

## Rerun with the accrual on income (brief 111c)

The pension accrual is now a share of the cell's income, D.8 over B.6g (I-D1k: 3.01% low, **4.83% central, the observed 2024 value (0.048267), not a mid-point**, 9.74% high; 1998 to 2025 median 7.30% as reference). Every cell's income is scaled by one factor (1.3733) so that households times income equal B.6g for calendar 2024 (1,801.4 billion pounds, no price adjustment): the main runs are **aggregate-constrained**, and `S_unscaled` keeps the unscaled income as a sensitivity. Everything else is as in 110c (ETB retired fraction 0.4386, return regimes, saving ratio, convention A, no tax). Sixteen runs; all identity residuals are below 1e-10, and the legacy arm still equals `grow_and_consume`.

### What changed against 110c

- **Wealth over GDP at year 100, median saving:** 0.75 (low return), **1.29** (mid-point return) and 4.42 (high), against 0.85, 2.04 and 9.9 in 110c. Year 10 and 50 at the mid-point return: 1.03 and 1.16 (110c: 1.08 and 1.45). The spread across return regimes is narrower and the central path is nearer flat, because the accrual no longer grows with wealth.
- **The accrual now matches today's flow.** Year-1 accrual is 87.0 billion pounds, the share times B.6g (4.83% of 1,801.4) and within 0.07% of ONS D.8 for 2024 (86.9; the difference is the rounding of 4.83 against 4.8267). In 110c the mid-point label gave 152, 2.7 times the 2021 value.
- **The realised saving ratio is constant at 5.8% of income** (4.83 accrual plus the median 1.01 non-pension) for all 100 years, since both are shares of income; at the minimum and maximum saving ratios it is 2.2% and 18.4%. In wealth terms saving is 0.77% of wealth in year 1 (0.64 accrual, 0.13 non-pension), falling to 0.60% by year 100 as wealth outgrows income.
- **Negative positions are fewer.** With the accrual on income no cell's net worth goes negative in any run (110c: the poorest cell at year 34 at the minimum saving ratio). Net financial wealth still goes negative at the minimum saving ratio, from year 1 in D1-3 and year 7 to 8 in D4-5 (table below); the design has no borrowing constraint.
- **Legacy, untaxed, is unchanged:** 0.95, 0.78 and 0.61 at years 10, 50 and 100.

### What now sets the path

- **The return regime, as before.** At the mid-point return wealth grows 1.90% a year (saving 0.77% plus holding gain 1.13%) against GDP per head 1.57% in year 1, easing to 1.76% by year 100; the ratio rises but slowly. At the low regime the holding gain on pension and net financial wealth is negative (-1.2%) and the ratio falls (0.75); at the high regime the gain is 3.1% and it rises to 4.4. No run is flat; the closest is the mid-point return at the minimum saving ratio (0.99, 0.95, 0.94), because there saving is only 2.2% of income and the gain is below GDP growth.
- **The accrual still moves it, less than before.** At the mid-point return and median saving: accrual 3.01% gives 1.11 at year 100, 4.83% gives 1.29, 9.74% gives 1.77. The accrual is 83% of the saving ratio at the median (4.83 of 5.8).
- **Income scaling raises it.** Unscaled income gives 1.14 against 1.29: the factor 1.37 lifts the whole saving flow, since both parts are shares of income. The retired fraction (0.439, 0.6, 0.8) changes nothing to two decimals once income is scaled to the total: the factor absorbs it.
- **Composition moves for a reason that is partly an artefact.** Saving is a flat share of income and does not depend on wealth, so the low-wealth bands gain wealth share: D1-3 from 2.1% to 10.8% of wealth and D10 from 40.7% to 28.0% by year 100 in the central run. This is the missing saving gradient (out of scope), not a finding about distribution.
- **Convention B** agrees with A in the first year and differs in composition afterwards (3.63 against 1.29 at year 100), as in 110c.

### Limits (the open question for the author)

D.8 over B.6g counts employer contributions and benefit accrual in funded and unfunded schemes, and it is a ratio of national totals applied equally to every cell's income. A household pension that is never drawn here receives the full flow while nothing leaves it (no withdrawal, no decumulation, so the retired cells keep accruing), and the pension class grows from accrual and gain alone. Whether D.8 over B.6g is the right base for a pension that is never drawn is for the author to rule. Also unchanged from 110c: no transitions, mortality or inheritance; fixed weights; debt netted inside the 102r classes (the erosion wedge is 0); no saving gradient; wealth at the 2020 to 2022 level against income at 2024; B.6g is disposable income and the per-household table is gross.

### Tables

#### Units and reconciliation (wealth and households as the pack has them; income scaled to B.6g 2024)

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


#### Runs: wealth over GDP (index, start = 1.00) and the realised saving ratio (saving including the pension accrual, over cell income, percent; year 0 shows year 1)

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

#### Account terms: saving plus gain over opening wealth, against GDP growth 1.57%

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

#### Share of wealth by band

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

#### Sensitivities (return mid-point label, saving median)

| variant | W/GDP y10 | y50 | y100 |
|---|---|---|---|
| accrual low (3.01% of income) | 1.01 | 1.05 | 1.11 |
| accrual observed 2024 (4.83%, the main run) | 1.03 | 1.16 | 1.29 |
| accrual high (9.74%) | 1.09 | 1.43 | 1.77 |
| income not scaled | 1.01 | 1.07 | 1.14 |
| retired fraction 0.439 (the main run) | 1.03 | 1.16 | 1.29 |
| retired fraction 0.6 | 1.03 | 1.16 | 1.29 |
| retired fraction 0.8 | 1.03 | 1.16 | 1.29 |

#### Convention B check (return mid, saving median)

Year 1 aggregate dNW: A 2.581533e+08 (per-household money units, summed), B 2.581533e+08; relative difference 0.00e+00. Identity residual A 1.9e-12, B 2.8e-11. The paths then differ (W/GDP y100 1.29 in A, 3.63 in B) because B credits the yield to the class that earns it and A leaves it in net financial wealth: the two conventions are equal in the first year, not in composition afterwards.


#### Negative positions (first year)

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
