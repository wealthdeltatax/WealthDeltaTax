# 102r: parameter map, evidence side B: stocks, stage weights, debt, transfers and mobility

Written 2026-11-21. Brief `project/briefs/open/102r-parameter-map-stocks-and-cells.md`; companions 101r (flows and returns) and 103r (assembly). The crosswalk and register are data files: `research/tables/102r-parameter-map-stocks-and-cells/stocks_crosswalk.csv` (13 sources) and `stocks_register.csv` (33 rows), built by `build_stocks_tables.py` from the committed derivation outputs. Nothing here edits the register, pack, code or manifest, no model was run, and no value was chosen with regard to WDT revenue, fund fill or closure.

## Answer in brief
- **Stocks and structure are far better held than flows, but only at the level of the whole band.** Opening composition by pack band is **observed** (WAS Round 8, Table 2.2, sums to the total within tolerance). Cell sizes by band and stage are **derived** from the WAS tables but only as a **proxy** for the pack deciles, because the WAS stage table is by fixed GBP wealth bands and those bands miss the pack deciles by up to 4.9 percentage points of households.
- **Not held anywhere in the repository (unset, with stated consequences):** gross debt and debt service by band or stage, a DB against DC pension split, inter-household transfers and estates by band, a full band or stage transition matrix, a retirement-entry hazard, a wealth gradient in mortality, household formation, and household-level stage weights. Each has a data request below.
- **Summary measures only for mobility:** two-year top-decile persistence (80%, 90% of entrants from decile 9) and a four-year rank correlation (74 / 77), from different populations that are not spliced. They are validation moments, not parameters.
- **Pension stock rows are all on the ONS SCAPE-based Round 8 basis.** The Round 7 to Round 8 break and the Resolution Foundation basis (which excludes DB and pensions in payment) are named and never mixed.
- **Existing rows (audit, no edits):** I-D4a central, I-D4b low and high, I-D4h central, I-W5a, I-W5e and I-W4a to I-W4c reproduce. Disagreements are reported in section 4, including a correction to Agent 4's draft verdict on I-D4b.
- **One note for 096r.** 096r listed the property and pension shares of D4-5 as unset because the pack has no such rows. They are derivable from the held Table 2.2 (37.5% and 36.3%, row S05).

## 1. Runtime check
This session has a local checkout and a shell. Each derivation script ran once from the branch as checked out: `derive_bands_stages.py`, `derive_debt_demography.py`, `derive_transfers_audit_coverage.py` and `build_stocks_tables.py` all exit 0 with every stated tolerance met. The held workbooks in `data/rates/` were read in place. The held files were checked **internally** (sums and tolerances), not against the live published pages, and the crosswalk says so per row.

## 2. Source crosswalk
Thirteen rows in `stocks_crosswalk.csv`, with the columns of 101r (exact file, table or series; publisher and link; period; population, unit, frequency, price basis; definitions and coverage; dimensions; revisions and sampling limits; whether the held file was checked against the published source).

| Id | Source | Used for |
|---|---|---|
| X01 | WAS Round 8 Table 2.2 (components by decile) | composition by band (S05, S08, S09) |
| X02 | WAS Tables 2.5, 2.11, 2.13 (households by GBP band; persons by age) | band reconciliation, weights (S02, S27) |
| X03 | WAS economic status by wealth band (098r extract) | stage weights (S03, S04) |
| X04 | ONS ad hoc 2813 (components by age of HRP) | composition by age proxy (S06) |
| X05 | ONS ad hoc 3222 (personal debt by age and region) | debt (S10, S11) |
| X06, X07 | ONS population projections; ONS ad hoc 3459 (qx) | demography (S23, S24) |
| X08 | ONS national balance sheet household stocks (097r) | aggregate cross-checks (S12, S29) |
| X09 | ONS sector accounts S.14 capital account (097r) | cross-sector transfers (S16) |
| X10 | ONS ETB Tables 3b, 4b (income, retired and non-retired) | stage income context only: income-ranked, not wealth-ranked |
| X11 | pack `wealth_distribution.csv`, `wealth_tail.csv` | opening state, tail (S01, S14) |
| X12 | 099r moments (BF-03, BF-04, BF-06, BF-13, BF-14, AB-02, EER-01, TD-02, TZ-01) | mobility, tail, estates (S15, S18, S20, S21) |
| X13 | pension valuation breaks | basis statement for every pension row (S08) |

## 3. Register by variable group
Classification counts in the 33 rows: observed 11, derived 5, proxy 7, scenario 1, legacy 1, unset 8. "Ruling" is the proposal for 103r, not a decision.

| Group | Rows | What is held | Classification | Proposed ruling |
|---|---|---|---|---|
| Band definitions and edges | S01, S02 | Pack deciles; the GBP-band reconciliation (R8 household shares by band group: D1-3 27.3 vs 30, D4-5 23.4 vs 20, D6-7 15.1 vs 20, D8-9 20.1 vs 20, D10 14.1 vs 10) | observed; derived | ready as a reported mismatch |
| Stage weights | S03, S04 | persons by band and stage (table below); rounding bound per cell | proxy | implement with a scenario range (alternative band edges) |
| Asset composition | S05 to S09 | property, financial, physical, pension shares by band (observed); by age of HRP (proxy); DB against DC split (unset) | observed; proxy; unset | ready for band; DB/DC further data required |
| Liabilities and debt service | S10 to S13 | GB debt totals and by age (persons); cross-check against AF.L not reconciled; debt service by band unset | observed; proxy; unset | validation only; further data required |
| Top tail | S14, S15 | WID series; a labelled adjustment range for wealth missing from the WAS top | observed; scenario | scenario range, no value chosen |
| Transfers | S16 to S19 | cross-sector capital transfers (observed); inter-household gifts, bequests and estates (unset); heir rule (legacy) | observed; unset; legacy | baseline TR = 0 until the author rules |
| Mobility | S20 to S22 | two summary moments from different populations; no matrix | proxy; unset | validation only |
| Demography and weights | S23 to S28 | age structure, period mortality, adults per household (two bases); retirement hazard, household formation, household stage weights unset | observed; derived; unset | age hazard ready; hazards unset |
| Existing rows | S29 to S33 | audit of I-D4a to I-D4h, I-W4a to I-W4f, I-W5a to I-W5e | see section 4 | report, no register edit |

**Persons aged 16 and over by pack band and stage, Round 8** (GBP-band groups used as a proxy for the pack deciles; each cell within +-0.5pp of its row total, so for example +-116,400 for D4-5 retired; bound in `stage_rounding_bounds_r8.csv`):

| Band | Working | Unemployed | Inactive, not retired | Retired |
|---|---|---|---|---|
| D1-3 | 6,317,850 (51.4%) | 675,000 (5.5%) | 3,669,170 (29.9%) | 1,629,600 (13.3%) |
| D4-5 | 7,822,100 (70.0%) | 283,500 (2.5%) | 1,092,750 (9.8%) | 1,978,800 (17.7%) |
| D6-7 | 4,813,600 (63.8%) | 94,500 (1.3%) | 657,790 (8.7%) | 1,978,800 (26.2%) |
| D8-9 | 6,618,700 (60.6%) | 202,500 (1.9%) | 842,530 (7.7%) | 3,259,200 (29.8%) |
| D10 | 4,512,750 (54.6%) | 94,500 (1.1%) | 750,100 (9.1%) | 2,910,000 (35.2%) |

Stage is the table's economic status of the person. The household reference person's status basis is not stated in the held table, and economically inactive not retired (students, carers, long-term sick) is a separate group, not a third retirement state. No cell here is built by spreading an aggregate in proportion to wealth.

**Pension basis.** Every pension row (S05, S06, S08) uses the ONS WAS Round 8 SCAPE-based DB valuation. Round 8 total wealth including pensions is not comparable with Round 7 without the break. The Resolution Foundation passive and active figures, which exclude DB and pensions in payment, appear only as validation context (X12), never in a stock row.

## 4. Existing-row audit (no register edits)
From `existing_row_audit.csv`; "supports" means the held files reproduce the register value within rounding.

| Row | Held value | Verdict |
|---|---|---|
| I-D4a central 5.94 | 5.94 on GDP 2,284bn | supports |
| I-D4a on the pack GDP | 6.14 (pack GDP 2,211.48bn, 3.2% lower) | the register and the pack use different GDP; **not reconciled** in held files |
| I-D4a low 5.80 | held NBS S.14 net worth 2021 over 2,284bn gives 5.03 | contradicts as to basis (the register's low is a different year and series) |
| I-D4g | NBS S.14 net worth end-2025 about 10.8tn (S.14 plus S.15 11.2tn) | supports the level; the 3.6 ratio needs a GDP not held |
| I-D4b low 49.3 | 49.3 (households at or above 300,000) | supports; the register calls it an adult share |
| I-D4b high 64.3 and central 54.9 | held household bracket 59.2 to 72.7 (at or above 200,000 to at or above 85,000) | **high inside; central below the bracket**; the central is an adult share from a lognormal fit the held tables cannot test. This corrects the draft verdict "supports (bounds inside)", which the numbers do not bear out |
| I-D4h central 1.93 | 1.9282 (Table 2.11) but 1.8593 (Table 2.13) | supports the central; the two published tables differ by 1.858m adults, not mentioned by the register |
| I-D4h low 1.77 | both tables give 1.86 to 1.93 | contradicts (the low is an assumption below both) |
| I-W5a 40.7, low 40.1 | 40.71, 40.1 | supports |
| I-W5e 35.4 | 35.43 (the register shows 4,806bn pensions, the table sums to 4,807.7bn) | supports |
| I-W5c, I-W5d | WID 2024: 21.3 and 57.1 against 14.4 to 23.0 and 52.4 to 52.5 (2016-18) | definitions and years differ; not averaged |
| I-W4a to I-W4c | 80 / 90 and 74 / 77 as in 099r AB-02 and BF-04 | supports; I-W4c central 75.5 is a register midpoint (J) |
| I-W4d to I-W4f, I-W5b | not audited: no held table | open |

## 5. Cell coverage inputs (item 5)
`cell_coverage_inputs.csv` lists, per pack band and stage, the classes of the structure rows. The same pattern holds for all twenty cells: stage weight **derived** (proxy for deciles, rounded percentages); composition **derived at band level only** (not by stage); debt, transfers **unset**; mobility **proxy at best** (summary measures, not pack bands); mortality **age-only**. The band mismatch against the deciles ranges from -4.9pp (D6-7) to +4.1pp (D10). The coverage matrix itself is 104r's.

## 6. Reproducibility
| Script | Reads | Writes | Tolerance |
|---|---|---|---|
| `derive_bands_stages.py` | `data/rates/totalwealthtables.xlsx`, 098r CSVs, pack | band reconciliation, composition, stage weights, weights | 1.0pp against the 098r rounded shares; Table 2.1 against Table 2.2 sums as stated in `check_table21_vs_table22.csv` |
| `derive_debt_demography.py` | 098r ONS extracts | debt by age, demography, deaths, survival | mean times N within 2.4% of totals; deaths within 5 |
| `derive_transfers_audit_coverage.py` | 097r sector accounts, workbook, pack, 099r | transfers, audit, coverage | as printed in each CSV |
| `build_stocks_tables.py` | the outputs above | `stocks_crosswalk.csv`, `stocks_register.csv` | share 0.05pp, pounds 0.5bn, counts exact; fails on an unset row carrying a number |

## 7. Data requests (stocks and structure)
| # | Request | Informs | Model can proceed | Access route |
|---|---|---|---|---|
| 1 | WAS person and household files: status by wealth decile, band-by-stage composition, DB/DC/in-payment pension, gross debt and debt service, gifts and inheritances, retirement entry in the panel | S03, S06, S07, S10 to S13, S17, S22, S25, S28 | stage on a proxy; the rest unset | UK Data Service study 7215 (safeguarded licence); study 6709 secure |
| 2 | ONS note on Table 2.13 against Table 2.11 adult counts | S27, I-D4h | on a scenario range of the two bases | ONS request |
| 3 | HMRC inheritance tax: estates by size and composition, current years | S18 | TR unset | HMRC statistics (tables 12.1 to 12.3 are held as ods but not parsed for this) |
| 4 | ONS mortality by wealth or deprivation | S24 | age hazard only | ONS or linked data request |
| 5 | NMG debt-service tables by income, age and tenure | S13 | debt service unset | Bank of England publication tables |
| 6 | GDP series behind the register and the pack | S29 | report the disagreement | author |
| 7 | Round 8 reconciliation of the WAS top (Advani and Tarrant style) | S15 | scenario range only | author or analyst |

## 8. Open questions for the author
1. **Stage definition.** Is the person's economic status (the held table) the intended stage, or the household reference person's? Proposed resolution: use the held person-based table as the proxy and request the household file (data request 1).
2. **Physical wealth.** Should contents and vehicles (6.0% to 53.6% of total wealth by band) be inside the WDT base or outside the cell asset classes? Proposed resolution: 103r asks the guru; the register carries it as a separate class.
3. **Register disagreements.** I-D4a (GDP), I-D4b central and I-D4h low disagree with the held files. Proposed resolution: the author or guru decides whether to edit the register; this note does not.

## Sources
Repository: the brief, `research/scripts/` scripts, `research/tables/102r-parameter-map-stocks-and-cells/` outputs, `research/notes/098r-was-tables-and-population.md`, `research/notes/097r-open-series-collection.md`, `research/notes/099r-held-research-moments.md`, `research/notes/096r-cohort-cell-design.md`, `model-specs/inputs.md`, `data/country-packs/GBR/`. External sources are cited by exact file and table in `stocks_crosswalk.csv`: ONS Household total wealth in Great Britain (April 2020 to March 2022) and its tables, ONS ad hoc 2813, 3222 and 3459, ONS 2024-based population projections, ONS national balance sheet and quarterly sector accounts, ONS Effects of taxes and benefits FYE 2024, and, through 099r, the Resolution Foundation (Before the fall, 2025) and Advani, Bangham and Leslie (2021).
