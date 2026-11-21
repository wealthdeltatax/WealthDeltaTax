# 104r: parameter map, design side: cell coverage, accounting conventions, public side

Accessed 2026-11-21. Brief `docs/briefs/104r-parameter-map-design.md`. Closes deliverables C and D of the parameter map from the 103r register (`docs/research/data/103r/parameter_register.csv`). Proposals with a recommendation each; the author rules. No code, register, pack or manifest edit; no model run; no replacement for 3.5%.

Status: in progress; sections marked pending are not yet written.

## 1. Summary
(pending)

## 2. Cell coverage matrix (item 1)
Script `docs/research/data/104r/coverage_matrix.py` reads the 103r register and the 102r cell inputs and writes `cell_weights.csv`, `coverage_matrix.csv` (15 variable groups x 5 pack bands x 2 stages = 150 entries), `resolution_by_row.csv` (every 103r row with the finest resolution it supports) and `resolution_pivot.csv`. It fails if a cell or a register row is missing. The matrix classifies evidence; it holds no value for any cell.

**Definitions.** Pack bands are the five used by 102r and the schedule: D1-3 (below the assessed threshold, one remainder line), D4-5, D6-7, D8-9, D10. Stage is the author's proxy, the person's economic status in the held WAS table (four groups: working, unemployed, inactive not retired, retired); two stages are used here, **retired** and **not retired** (the other three together), and the three non-retired groups are shown separately in the weight table. The household reference person's status is a data request (SUP-1), not a blocker.

### 2.1 What is held by cell: weights only
| Pack band | Stage | Persons 16+ (WAS R8) | Rounding bound | Share of band adults | Band-edge mismatch |
|---|---|---|---|---|---|
| D1-3 | not retired | 10,662,020 | +-385,450 | 86.7% | -2.7pp of households |
| D1-3 | retired | 1,629,600 | +-116,400 | 13.3% | -2.7pp of households |
| D4-5 | not retired | 9,198,350 | +-385,450 | 82.3% | +3.4pp of households |
| D4-5 | retired | 1,978,800 | +-116,400 | 17.7% | +3.4pp of households |
| D6-7 | not retired | 5,565,890 | +-192,725 | 73.8% | -4.9pp of households |
| D6-7 | retired | 1,978,800 | +-58,200 | 26.2% | -4.9pp of households |
| D8-9 | not retired | 7,663,730 | +-192,725 | 70.2% | +0.1pp of households |
| D8-9 | retired | 3,259,200 | +-58,200 | 29.8% | +0.1pp of households |
| D10 | not retired | 5,357,350 | +-192,725 | 64.8% | +4.1pp of households |
| D10 | retired | 2,910,000 | +-58,200 | 35.2% | +4.1pp of households |

The ten cells hold 50.20 million persons (37.91 million above D1-3); this is the 102r Round 8 table, not the 52.04 million of Table 2.11 used for I-D4h (103r audit, not reconciled). Cell sizes are weighted counts, derived from whole-number percentages of band adults, grouped by GBP band edges that differ from the pack deciles by up to 4.9pp of households. Sample sizes are not published, and two source cells in the D4-5 band are suppressed in the held table (`stage_weights_by_pack_band.csv`, column `suppressed_cells_in_band`), so the D4-5 weights carry that uncertainty on top of the rounding bound.

### 2.2 Evidence class by variable group and cell
Within a group the class is the same for the four D4-5 to D10 bands except where noted: D1-3 differs for composition (shares unstable at small or negative net totals) and for income (not held below D4); the tail group applies to D10 only.

| Group | Not retired, D1-3 | Not retired, D4-5 to D10 | Retired, D1-3 | Retired, D4-5 to D10 | Evidence form | Register rows |
|---|---|---|---|---|---|---|
| G01 Cell weights (persons by band and stage) | derived | derived | derived | derived | derived from direct observation | S02, S03, S04 |
| G02 Opening band wealth (mean and total) | observed | observed | unset | unset | direct observation | S01, S29 |
| G03 Asset composition: property, net financial, physical, pension | observed (unstable shares) | observed | proxy | proxy | direct observation at band; age of reference person as a proxy for stage | S05, S06, S07, S08, S09 |
| G04 Gross debt, interest and repayment | unset | unset | unset | unset | none by band (age totals observed, aggregate cross-check only) | S10, S11, S12, S13, D04 |
| G05 Labour income and benefits (Y_L; transfer income) | unset | proxy | unset | unset | aggregate constraint; band means are register judgement rows | F-01, F-02, F-03, F-05 |
| G06 Ordinary taxes net of benefits (T_C) | proxy | proxy | proxy | proxy | modelled allocation (income decile mapped to wealth band by judgement) | F-04 |
| G07 Consumption (C), and the legacy comparator | unset | unset | unset | unset | aggregate constraint | F-06, F-25 |
| G08 Net saving (S) and saving over wealth | unset | unset | unset | unset | aggregate constraint; average-family and foreign proxies are validation moments only | F-07, F-08, F-09, F-24, F-29, F-30, F-31, F-32, F-33, F-34, F-36 |
| G09 Pension flows: contributions, accrual, withdrawal | scenario | scenario | scenario | scenario | aggregate constraint on the ONS basis; one labelled aggregate scenario (author ruling 2026-11-21) | F-10, F-11, F-13, F-35 |
| G10 Retained cash yield and the yield and gain by asset class | externally specified | externally specified | externally specified | externally specified | externally specified path (JST market portfolio); retained fraction by band unset | F-14, F-15, F-16, F-17, F-18, F-19, F-20, F-26, F-27 |
| G11 Return on classes with no held return: pension, physical, net financial | scenario | scenario | scenario | scenario | labelled scenario range per class (author ruling 2026-11-21) | F-12 |
| G12 Liability revaluation and residual O | unset | unset | unset | unset | aggregate constraint | F-21, F-22, F-23 |
| G13 Gifts, inheritances, inter-household transfers (TR) | unset | unset | unset | unset | aggregate (sector with other sectors only); legacy heir rule is the comparator | S16, S17, S18, S19 |
| G14 Transitions: band mobility, retirement entry, mortality, household formation | proxy | proxy | unset | unset | proxy: whole-distribution and income-group mobility moments; mortality age-sex only | S20, S21, S22, S23, S24, S25, S26, S27, S28, S33 |
| G15 Top tail within D10 | n/a | scenario (D10 only) | n/a | scenario (D10 only) | observed tail shares (WID, WAS) with a labelled adjustment range | S14, S15, S31, S32, F-28 |

Forms, as the brief asks, are kept apart: **direct observation** (band wealth, band composition), **derived from observation** (cell weights), **modelled allocation** (only the income-decile mapping of ordinary taxes; no other allocation is made, and none by wealth share, per the hypothesis rule), **aggregate constraint** (consumption, saving, pension flows, liability revaluation, the residual `O`), **externally specified path** (the JST market return and its split) and **scenario** (author rulings: one aggregate pension scenario; a range per class for pension, physical and net financial returns).

### 2.3 What resolution each register row supports
| Finest resolution the row supports | observed | derived | proxy | scenario | unset | endogenous | legacy | total |
|---|---|---|---|---|---|---|---|---|
| aggregate | 15 | 6 | 4 | 0 | 0 | 0 | 0 | 25 |
| market path, not household | 1 | 5 | 0 | 0 | 0 | 0 | 0 | 6 |
| band | 3 | 2 | 0 | 0 | 0 | 0 | 0 | 5 |
| other axis (age, income, estate size, stage only) | 4 | 1 | 4 | 1 | 2 | 0 | 0 | 12 |
| top tail or distribution moment | 2 | 0 | 5 | 1 | 0 | 0 | 0 | 8 |
| band x stage | 0 | 1 | 1 | 0 | 7 | 0 | 0 | 9 |
| none | 0 | 0 | 1 | 1 | 2 | 3 | 1 | 8 |

Reading the pivot: **25 of the 73 rows are observed, derived or proxy at the aggregate**, 6 more at market-path level, 5 at band level, and only **2 at band x stage** (S03 weights as a proxy, S04 sizes derived) against **7 unset** at that resolution (S07, S13, S17, S22, S25, S26, S28). The data hold state variables at band, weights at band x stage, and every flow at aggregate only.

### 2.4 The smallest cell structure the data support
- **State and weights: five bands by two stages (ten cells).** Weights are derived per cell, opening wealth and composition are observed per band; the stage split of composition has only the age-of-reference-person proxy (S06). This is where the evidence ends; it is not a preferred number of cells.
- **Flows: one aggregate each.** Consumption, saving, pension contributions and accrual, retained cash income, liability revaluation and `O` are observed only for the household sector. A cell flow is an **allocation of that aggregate by a labelled scenario**, never an observation and never an allocation in proportion to wealth.
- **Splits that are scenarios only:** the retired cell's flows (income, drawdown, pension withdrawal); a separate high-wealth cell inside D10 (the tail is a range, G15); the inactive-not-retired and unemployed stages as cells of their own (they are weights only: unemployed 1.1% to 5.5% and inactive not retired 7.7% to 29.9% of band adults, the highest shares in D1-3); within-band distribution.
- **Not supported at any resolution:** debt and debt service, gifts and inheritances, saving by band, consumption by band, mortality by wealth, household formation.
- **Consequence for the model.** A cell model can be specified now as a **weighting and balance-sheet structure** with an aggregate flow account allocated by scenario. Treating its band by stage cells as separate behavioural units would give them flow parameters the data do not hold. The four illustrative cells of 096r (a working saver, a low-saving working cell, a retired cell, a high-wealth cell) remain illustrations.

## 3. Accounting conventions (item 2)
(pending)

## 4. Public-side representation and settlement (item 3)
(pending)

## 5. Interface to v3 (item 4)
(pending)

## 6. Rulings table (item 5)
(pending)

## 7. Validation moments (item 6)
(pending)

## 8. Reproduction
(pending)
