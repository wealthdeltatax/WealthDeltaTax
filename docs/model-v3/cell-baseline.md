# Cell baseline run (brief 110c)

Status: blocks 1 and 2 done; findings below are from one mid-point run only. The grid (block 3) is not run.

## Units and reconciliation
Source: `model_v3/runner/cell_baseline.py` (`build_cells`, `reconcile`), run by `docs/model-v3/cell-baseline/run_cell_baseline.py units`; tables in `cell-baseline/units.csv` and `cells.csv`. Wealth and income in pounds bn, households in thousands, persons 16+.

| Check | Cells | Reference | Gap |
|---|---:|---:|---:|
| Net worth, ten cells | 13,567.9 | pack `wealth_total` (all) 13,568.0; decile sum 13,567.9 | 0.00% (by construction: band wealth split by person share) |
| Wealth / GDP | 6.135 | pack 6.135 (GDP 2,211.48) | 0 |
| Households (thousand) | 26,991 | pack 26,991 | 0 |
| Income, cells (band mean household income x households) | 1,515.8 | ONS B.6g 2025 1,883.2 | **-19.5%** |
| Income, cells | 1,515.8 | B.6g plus D.8 2025 1,971.4 | **-23.1%** |

The wealth side closes because it is built from the pack's own band totals. The income side does not, and the gap is reported, not forced. The band means of I-D9 are household survey gross income at the FYE 2024 level, a different base from the national-accounts household sector (no imputed items, survey under-coverage, non-profit bodies in B.6g, a year's price drift). The retired fraction does not move the total (the band mean is kept); it moves only the split between the two stages of a band.

Consequence for block 2: a saving ratio applied to cell income (ONS non-pension saving ratio, 5.0 to 16.5%, median 7.1%) gives aggregate saving about a fifth below the national-accounts saving. The untaxed paths will therefore grow more slowly than the national accounts imply, for a reason that is the units gap and not the model. Per-household conversion with I-D4h (1.93 adults) is needed only for per-adult figures, not for the aggregates; the aggregate wealth/GDP is comparable with the pack's because both are household-basis totals over the same GDP.


## Inputs
| Item | Rule | Source |
|---|---|---|
| Cells | five pack bands times not retired and retired | `cell_weights` (persons 16+) |
| Band wealth | sum of the deciles (D1-3 = D1 + D2 + D3) | `wealth_distribution` `wealth_total` |
| Stage split of wealth and households | by person share (assumption: the pack gives no wealth by stage) | `cell_weights` |
| Classes | property, net financial, physical, pension; % of band wealth rescaled to sum to 1 (the pack's rounded shares sum to 100.0 to 100.1) | `band_composition` |
| Households per band | decile count x 2,699.1 thousand | `wealth_distribution` `households` |
| Band mean income | D4-5 I-D9a, D6-7 I-D9b, D8-9 I-D9c, D10 I-D9d (central); D1-3 takes the I-D9a low bound, 40,200 | register |
| Retired income | not retired income x f, the band mean kept; f = 0.6, range 0.4 to 0.8, a labelled assumption: no held table gives retired income by wealth band (098r) | assumption |
| Saving ratio (block 2) | ONS non-pension saving ratio, 1998-2025: min 5.05%, median 7.13%, max 16.46% | `101r/derived_ons_flows.csv` |
| Returns (block 2) | property yield and gain from the JST housing split by regime (1947-79 low, 1980-2019 high, mid-point label); pension and net financial I-D1h, I-D1i (3.44, 5.20, 6.96); physical I-D1j (0); pension accrual I-D1k (0.41, 1.12, 1.84) on the pension class | `101r/jst_split_stats.csv`, register |
| T_WDT, TR | 0 | brief |

Layer: `runner/cell_baseline.py`, layer 4 (imports `core/pack` L0 and, from block 2, `core/household` L1; nothing imports it). Budget row 100 / 70 added to `architecture.md` 6.1 with the totals (core plus runner 4,755 / 3,083; total 5,625 / 3,703).


## Runs
Author ruling (2026-11-21): every cell's income is scaled by one factor so the total equals ONS B.6g. **Year matched: 2024** (1,801.4 bn): I-D9 is at the FYE 2024 level, so 2024 is the nearest calendar year; wealth is a 2020-22 base and the pack's CPI series ends in 2019, so no price adjustment is made between the 2020-22 wealth and the 2024 income (a limit). Factor 1.188 (the unscaled gap to 2024 is -15.9%). The main run is labelled **aggregate-constrained**; the unscaled run is the sensitivity.

Run: mid-point regime (property gain 2.64% and yield 3.83% real, the mean of 1947-79 and 1980-2019; net financial and pension 5.20%; physical 0), median non-pension saving ratio 7.13%, pension accrual 1.12% of opening net worth, convention A, 100 years, T_WDT = 0. Cell income grows with real GDP (1.57% a year, the runner's mean growth): **a decision of mine, the brief does not say**. Non-pension saving is s x income and lands in net financial wealth; pension accrual is added on top and goes to the pension class. Aggregate = sum over cells in pounds bn on a household basis (no person or household weights needed for a sum; I-D4h is not used). Wealth/GDP is indexed to year 0 (6.135), GDP growing at 1.57%.

| Run | Year | Wealth (bn) | Wealth/GDP index | Realised saving ratio | D10 share | Residual |
|---|---:|---:|---:|---:|---:|---:|
| Scaled (aggregate-constrained) | 0 | 13,568 | 1.000 | | 0.407 | 0 |
| | 10 | 23,829 | 1.503 | 0.193 | 0.394 | 0 |
| | 50 | 251,997 | 8.52 | 0.759 | 0.370 | 0 |
| | 100 | 5,239,167 | 81.3 | 6.62 | 0.364 | 0 |
| Unscaled (sensitivity) | 10 | 23,539 | 1.485 | 0.214 | 0.397 | 0 |
| | 50 | 243,747 | 8.24 | 0.862 | 0.378 | 0 |
| | 100 | 5,044,480 | 78.3 | 7.57 | 0.374 | 0 |
| Legacy arm (`W(1+r)(1-c)`, r = I-D1a 4.74%, c = I-D14c 3.5%) | 10 | 15,098 | 0.952 | n/a | 0.407 | 0 |
| | 50 | 23,148 | 0.783 | n/a | 0.407 | 0 |
| | 100 | 39,491 | 0.613 | n/a | 0.407 | 0 |

Realised saving ratio is S over cell income including pension accrual; the non-pension part is 7.13% by construction. Files: `cell-baseline/run_mid_median_A_scaled_*.csv`, `..._unscaled_*.csv`, `run_legacy_*.csv` (cells and aggregate, years 0 to 100). Identity residual (stock change against `dNW`) is below 1e-9 in every cell and year; `household_step` also raises on any gap. Legacy arm equals the kernel's `grow_and_consume` on the same cells to 1e-12 (test). The legacy wealth/GDP index at year 100 is **0.613 here, not the 0.47 the brief cites**: the 0.47 is not reproduced by the arithmetic-mean deterministic path; a geometric return (about 4.4%) gives about 0.44, so the 0.47 probably comes from the stochastic kernel runs. Not investigated further; no input changed.


## Findings
From the one mid-point run (not the grid; nothing here is a range):
1. **Untaxed wealth outruns GDP by a wide margin.** Wealth/GDP rises 50% in ten years and 81 times in a hundred, against 0.61 on the legacy rule. The mechanism is arithmetic, not a data result: at the mid-point regime every wealth class except physical earns 2.6% to 5.2% real while income grows 1.57%, and saving is added on top.
2. **The pension accrual drives the late path.** Accrual is a fixed 1.12% of opening net worth, so it compounds with wealth while income does not; the realised saving ratio goes from 15.6% in year 1 (7.13% non-pension plus 8.4% pension) to 76% at year 50 and 662% at year 100. That ratio is a symptom: no consumption response to wealth exists in the new arm (the legacy rule's c is the only wealth-dependent outflow), so nothing brakes the path. I have not run a no-accrual arm to measure its share.
3. **Distribution barely moves.** The top band's wealth share falls from 0.407 to 0.364 and the lowest band's rises from 0.021 to 0.063, because saving is proportional to income, not wealth, and the lowest band's financial class starts at zero. Cells do not mix.
4. **Scaling income matters little.** The unscaled run ends at 78 against 81 times; the 19.5% income gap changes the path by about 4% at year 100.
5. **The legacy arm is a different model, not a baseline for this one.** It has one class, no income and no saving, so it cannot be compared line by line; it agrees with the kernel to 1e-12.
No input was adjusted.

## Limits
- One run only: regime, saving ratio and convention B (one-step equivalence is tested, not run over 100 years) are not varied; block 3 is the grid.
- No consumption response to wealth, no pension withdrawal or sale, no transitions between cells, no mortality or inheritance; pension is never drawn (brief).
- Income grows with real GDP and is not tied to wealth: my decision.
- Wealth is a 2020-22 base and income a 2024 level with no price adjustment (the pack's CPI ends in 2019).
- Stage split of wealth and households by person share; class shares rescaled to sum to 1; D1-3 income is the D4-5 low bound; retired fraction 0.6 is an assumption with range 0.4 to 0.8 (sensitivity not run; it changes only the stage split of income).
- Per-class returns for net financial and pension are regime ranges, not estimates (I-D1h, I-D1i); the mid-point is a label.
- `household_step` emitted an `invalid value in multiply` runtime warning in one test (the pay-share line, `inf` times a zero mask); results closed to 1e-9 and I have not traced when it triggers. Reported, not changed (outside Touches).
