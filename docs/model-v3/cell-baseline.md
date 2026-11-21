# Cell baseline run (brief 110c)

Status: block 1 done (units and inputs); runs, findings and limits pending.

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
*Pending (blocks 2 and 3).*

## Findings
*Pending (block 4).*

## Limits
*Pending (block 4).*
