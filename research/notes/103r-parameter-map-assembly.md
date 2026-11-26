# 103r: parameter map, assembly: one register, cross-side checks, unresolved data and proposed rulings

Accessed 2026-11-21. Brief `project/briefs/open/103r-parameter-map-assembly.md`. Closes deliverables A, B and E of the parameter map: merges 101r (flows) and 102r (stocks, cells, transitions, debt). Data and script: `research/tables/103r-parameter-map-assembly/` and `research/scripts/merge_and_check.py`. No register, code, pack or manifest edit; no model run.

Status: complete (all sections written).

## 1. Summary
- **One register.** `parameter_register.csv` has 73 rows: 36 flows (101r), 33 stocks (102r) and 4 dictionary rows for 094r terms that are not parameters (`T_WDT`, `dNW`, `r_f` endogenous; `I_D` unset). Every row is classified (observed 25, derived 15, proxy 15, unset 11, scenario 3, endogenous 3, legacy 1) and no unset row carries a value. The crosswalk has 25 sources. Every one of the 18 094r dictionary terms (and the physical-wealth class) and the 26 existing register rows named in 101r and 102r has a row or an entry.
- **Rulings (proposals).** Ready 22; scenario range 15; further data required 15; unset 11; audit 5; validation or proxy only 1; legacy comparator 1; not applicable (endogenous) 3. Each unset row's consequence for the first implementation is in section 5. 3.5% (I-D14c) is the legacy comparator (F-25); there is no replacement value anywhere in the register.
- **Cross-side checks (section 3; 14 checks, tolerances stated).** The aggregate income side closes and the two sides agree where both are held: net capital transfers match exactly (C07) and the yield-plus-gain split reproduces the register total return to 0.0024pp (C04). Three things do not close. **(1) Pension basis:** every pension row names one basis, but the flows (ONS national accounts) and the stock (WAS SCAPE-based, the author's ruling for the base) are on different bases, so pension accrual cannot be turned into a rate on the stock (C01, C02; DR-01). **(2) The wealth roll-forward** is outside 1% of opening net worth in 2020 and 2021 (2.95% and 2.36%) and in 21 of 28 years, because the dwelling and land revaluation is not held (C06; coverage). **(3) Survey against national accounts:** WAS wealth is 18 to 23% above NBS net worth, on definitional and coverage grounds that no held file separates (C08).
- **Worked cell (D4-5, per GBP 100).** For the property class the account and a total-return credit agree (0.617) only if owner-occupiers' imputed rent, which ONS counts in both income and household consumption, is consumed; crediting the total return without that consumption overstates by 1.409, and also counting the yield as saving by 2.819. The other three classes, 62.6% of the cell (pension 36.3%, physical 19.7%, net financial 6.6%), have no return in the held data, so a cell cannot yet be run end to end.
- **Unresolved data (section 4).** 16 requests merged into 7 supplies. The WAS microdata (SUP-1, 13 rows) and the ONS pension and revaluation series (SUP-2, 8 rows) matter most; no supply is needed to specify the design.
- **Existing register (section 6).** 11 rows supported, 6 with a part unverified, contradicted or to reclassify, 2 on different definitions, 5 not audited, 2 legacy or no disagreement. I-D4a, I-D4b and I-D4h were already annotated or corrected by 105c; the I-D4a GDP mismatch, the I-D4b central, the I-W3b reclassification and the I-W3c and I-W3d citations remain open.
- **For 104r and the author.** (a) The flows are on the ONS national-accounts pension basis while the base is on the SCAPE basis: decide whether pension accrual runs as an aggregate scenario until DR-01 reconciles them. (b) Fix two labels in the flows register against 094r B2: F-03 benefits belong to `T_C`, not `TR`; F-21 real erosion belongs to `CG`, not `O`. (c) Add physical wealth to the 094r asset list. (d) Choose one deflator for the account (CPI or the ONS household consumption deflator; they differ by 0.49pp a year on average and by up to 2.29pp). (e) Reclassify I-W3b.
- **No row was adjusted or chosen with regard to WDT revenue, fund fill or closure.** No value was derived beyond what 101r and 102r delivered; the arithmetic in the checks is on their committed numbers.


## 2. Merged register and crosswalk
Files in `research/tables/103r-parameter-map-assembly/`, built by `merge_and_check.py` from the committed 101r and 102r CSVs (no source file is re-read):
- `parameter_register.csv`: 73 rows = 36 flows (F-01 to F-36) + 33 stocks (S01 to S33) + 4 dictionary rows (D01 to D04). Columns: the common 14 of 101r and 102r, plus `class_norm`, `ruling_class`, `pension_basis` and `dictionary_terms`. 102r's rows carried a long definition in place of a name; the script gives each a short unique name (33 names, one per row).
- `source_crosswalk.csv`: 25 sources (12 from 101r with prefix A-, 13 from 102r with prefix B-), same columns. A source used by both sides appears twice, once per side's reference (the ONS household series A-X01 to A-X05 and the NBS series B-X08), and the two rows are not merged because their exact references differ.
- `dictionary_map.csv`: each 094r B2 term and the register rows that carry it.

**Structural checks (all pass, exit 0):** no repeated variable name or row id; no row without a classification; no unset row carries a value; every pension row carries exactly one stated basis from a closed set (section 3, check 1); every one of the 18 094r dictionary terms (and the physical-wealth class) names at least one existing row; every existing register row named in the 101r and 102r notes and audits (26 ids) appears in a merged row.

**Counts.** By classification: observed 25, derived 15, proxy 15, unset 11, scenario 3, endogenous 3, legacy 1. By ruling class: ready 22, scenario range 15, further data 15, unset 11, audit (no ruling) 5, validation or proxy only 1, legacy comparator 1, not applicable (endogenous) 3. Section 5 lists the rows.

**Dictionary rows added (D01 to D04).** Four 094r terms had no parameter row because they are not parameters: `T_WDT` (D01), `dNW` (D02) and `r_f` (D03) are model outputs or kernel settings and are classed *endogenous*; `I_D`, interest paid on debt, and principal repayment R (D04) have no household series and are classed *unset* with no number. D01 to D03 are never calibration targets.

**Existing-row coverage.** 102r audits grouped rows (S29 to S33 cover I-D4a, I-D4b, I-D4g, I-D4h, I-W4a to I-W4f, I-W5a to I-W5e) and 101r audits rows one by one (F-25 to F-32). The check confirms each named id appears in some merged row; section 6 gives one line per register row.

**094r dictionary mapping.**

| 094r term | Register rows |
|---|---|
| NW | S01; S05; S29 |
| A (H, E, B, M, PA) | S05; S06; S08; S09; F-20 |
| L = D | S10; S11; S12; S13 |
| dNW | D02; F-23 |
| S | F-07; F-08; F-09; F-10; F-24 |
| Y_L | F-01; F-02 |
| Y_P | F-14; F-15; F-16 |
| I_D | D04; S13 |
| T_C | F-03; F-04 |
| C | F-06; F-25 |
| K | F-11 |
| CG | F-18; F-20; F-22 |
| TR | S16; S17; S18; S19 |
| O | F-21; F-23 |
| T_WDT | D01 |
| B, R | S13; D04 |
| y, g_h, r | F-17; F-18; F-19; F-26; F-27 |
| r_f | D03 |
| Physical wealth (author decision 2026-11-21; not in the 094r dictionary) | S09 |

**Dictionary gap.** The author's 2026-11-21 ruling puts physical wealth (contents and vehicles) inside the WDT base as a separate asset class. The 094r asset list `A (H, E, B, M, PA)` has no such class, so S09 maps to a term the dictionary lacks (last row of the table). 104r should add it to the accounting conventions.


## 3. Consistency checks across the two sides
Script `cross_side_checks.py` reads the merged register and the committed 101r and 102r CSVs (plus the pack CPI and the register text of I-D1a) and writes `cross_side_checks.csv` (14 checks) and `worked_cell_d45.csv`. Hard checks (C01, C04, C05, C07) pass; the rest report a difference and its class. Thresholds are reporting thresholds, not statistical tests, and none was chosen with regard to WDT revenue. Result words: PASS (within the stated tolerance), INFO (a difference reported, no tolerance because the definitions differ), FLAG (a labelling or definitional issue for 104r), OUTSIDE (beyond the reporting threshold, class stated).

| # | Check | Numbers | Result and class |
|---|---|---|---|
| C01 | Every pension row on one stated basis | ONS national-accounts 9 rows (F-03, F-08, F-09, F-10 to F-14, F-24); WAS Round 8 SCAPE 7 (S01, S05 to S08, S29, S31); Resolution Foundation 2 (F-32, F-34, both validation only); excludes pensions 1 (F-36); register of the bases 1 (F-35) | PASS. Flow rows are ONS, stock rows are WAS: **the two sides are on different bases** (C02) |
| C02 | Pension accrual against the pension stock | D.8 2021 GBP 55.5bn over WAS R8 pension wealth GBP 4,807.7bn = 1.15% | INFO, definitional: numerator is ONS net equity for one year, denominator is the SCAPE-based stock for a two-year wave. Reported **so that it is not used** as an accrual or growth rate; a same-basis rate needs the AF.6 stock (DR-01) |
| C03 | Accounting-location labels against 094r B2 | 2 of 36 flows rows flagged: F-03 (social benefits D.62) is labelled TR, but in 094r TR is net capital transfers and benefits sit in `T_C` net of benefits; F-21 (real erosion of nominal liabilities) is labelled O, but in 094r B1 and B2 the real revaluation of nominal positions is a `CG` term | FLAG, labelling only; values unaffected; not edited (for 104r) |
| C04 | Cash yield plus holding gain against the register total return | JST 1896 to 2019: 4.0343 + 0.7081 = 4.7424% against I-D1a central 4.74 | PASS, diff 0.0024 against 0.005 (the register is to 2 dp); additivity of the split 1.2e-8 |
| C05 | Worked cell D4-5, property class (table below) | per GBP 100 of cell wealth: account 0.617; total return with the yield consumed 0.617 | PASS. Without that consumption 2.026 (excess 1.409); with the yield also counted in `S` 3.436 (excess 2.819) |
| C06 | Net-worth roll-forward, S.14: dNW against B.101g + B.102 + B.103 (flows against stocks) | 2020: 754.1 against 449.9, O = GBP 304.2bn = 2.95% of opening NW; 2021: 420.4 against 158.8, O = 261.6bn = 2.36%; 2024: 137.1 against 39.7, O = 97.4bn = 0.92%. Threshold 1% of opening NW | OUTSIDE in 2020 and 2021 (the WAS wave), PASS in 2024. Only 7 of 28 years (1998 to 2025) are within 1%. Class **coverage**: the held revaluation is financial only, so the dwelling and land revaluation sits in O (DR-05) |
| C07 | Net capital transfers: B.101g - B.8g (101r) against D.9r - D.9p (102r S16 lines) | 2024: -1,043 and -1,043 GBP m; maximum difference over the 11 years held 0.0 | PASS (tolerance GBP 3m as 101r ID10). The two sides agree exactly; transfers between households are outside these lines and net to zero in the sector |
| C08 | Survey total against national-account total | WAS R8 total wealth GBP 13,568bn against NBS S.14 net worth GBP 11,071.8bn (end-2020) and 11,492.2bn (end-2021): +2,496.2bn (22.5%) and +2,075.8bn (18.1%) | INFO, definitional and coverage: SCAPE pensions against national-accounts entitlements, contents and vehicles in WAS, GB against UK, mid-wave against end-year. Not reconciled and not averaged. The same gap is in I-D4a (5.94 on WAS against 5.03 on the held NBS 2021) |
| C09 | ONS 3222 debt against NBS financial liabilities | GBP 1,412.0bn against AF.L 1,999.6bn (2020) and 2,039.0bn (2021): ratio 0.71 and 0.69 | INFO, coverage and definitional; no WAS gross debt aggregate is held, so debt is not used as an input |
| C10 | Price basis: CPI against the ONS household consumption deflator | 1999 to 2019: mean 2.01% and 1.52%, mean difference 0.49pp, maximum 2.29pp; years beyond 1pp: 2009, 2010, 2012 | FLAG, definitional: **two deflators** sit in the account (pack CPI converts the JST returns to real; the ONS deflator converts the liability revaluation F-21) |

**Worked case, band D4-5 (one cell), GBP per 100 of cell wealth** (`worked_cell_d45.csv`). Composition is the 102r observed WAS Round 8 split (S05); yield and gain are the JST housing arithmetic real means, 1896 to 2019 (F-20).

| Class | Weight | Cash yield | Holding gain | Status |
|---|---|---|---|---|
| Property | 37.5 | 1.409 (37.5 x 3.758%) | 0.617 (37.5 x 1.6455%) | computed; the JST housing yield includes imputed rent (100r) |
| Net financial | 6.6 | not applicable | not applicable | no instrument split held, so equity, bond and bill weights are not known |
| Physical | 19.7 | not applicable | not applicable | no return series for contents and vehicles |
| Pension (SCAPE basis) | 36.3 | not applicable | not applicable | pension return unset (F-12, DR-01) |

For the property class the convention cannot double-count if the account is used as specified in 094r B4: owner-occupiers' imputed rent is in ONS income (F-02) and in ONS household final consumption (it "includes the concept of imputed rental for owner-occupied dwellings", ONS, *Differences between ONS household expenditure statistics*, accessed 2026-11-21), so it nets out of `S`, and the account's change in property wealth is the holding gain, 0.617. Crediting the total return (2.026) without that consumption overstates by 1.409 (the imputed rent, which never arrives as cash); also counting the yield as retained saving gives 3.436, an overstatement of 2.819. **The cell cannot be run end to end:** the three classes without a return hold 62.6% of its wealth (6.6 + 19.7 + 36.3; the published weights are rounded and sum to 100.1), the largest being the pension asset.

**What the checks say**
1. **The flows and stocks sit on different pension bases (C01, C02).** Each row names one basis and none mixes them, but the account's pension accrual (ONS) and the pension stock it accrues to (WAS SCAPE) are not reconcilable with held data. Until DR-01 is met, pension accrual can only be an aggregate scenario, not a rate on the stock.
2. **Two labelling conflicts with 094r B2 (C03)** and **two deflators (C10)** are for 104r to fix in the accounting conventions; they do not change any value here.
3. **The wealth roll-forward does not close without a non-financial revaluation (C06).** `O` stays a reported residual, so the housing component of the return cannot be validated against the accounts. By band there are no flows to roll forward at all.
4. **The aggregate sides agree where both are held (C07, C04).** Net capital transfers and the yield-plus-gain split reproduce exactly.
5. **Survey and national-account totals differ by 18 to 23% (C08)** for definitional and coverage reasons that no held file separates; the stock base for the WDT is the survey (pack) side, and the national-account constraints on the flows are on a different footing.

## 4. Unresolved-data list
The 16 requests of 101r (DR-01 to DR-09) and 102r (R1 to R7) are merged into **seven supplies**, each one thing the author, or the role that downloads it, can provide. `unresolved_data.csv` holds the full text; the script checks that every original request maps to a supply and that every row ruled *unset* or *further data required* (26 rows) is covered by a supply or carries a stated no-source reason. Order is by the number of register rows a supply would inform, not by any effect on WDT results.

| Supply | What | Merges | Rows informed | Without it | Access and licence |
|---|---|---|---|---|---|
| SUP-1 | WAS study 7215 (UKDS), Round 8 and panel, person and household files: household wealth with components, age and economic status of the reference person, gross secured and unsecured debt, DB/DC and in-payment pensions, gifts and inheritances received, income, and the longitudinal status and decile changes | 101r:DR-07; 101r:DR-08 (partly); 102r:R1 | F-01, F-06, F-13, F-29, S07, S10, S11, S13, S17, S22, S25, S28, D04 (13) | cells keep stage on the pack proxy (S06), stage and band transitions stay unset, debt and debt service stay unset, income and consumption by cell stay on scenario ranges | UK Data Service registration and the End User Licence for safeguarded study 7215 (098r section 6; 095r); commercial use may need data-owner approval; Secure Access study 6709 is the fallback (3 to 4 months, non-commercial, UK-based). UKDS End User Licence (safeguarded); not unrestricted |
| SUP-2 | ONS national accounts, household sector S.14: pension entitlements AF.6 stock by year; non-financial revaluation (dwellings and land); consumption of fixed capital on dwellings; B.2g split into dwelling services and other surplus; D.611/D.613 split into pension and NIC contributions; D.622 benefits by scheme type and age group (ONS or DWP) | 101r:DR-01 (stock); 101r:DR-02; 101r:DR-03; 101r:DR-04; 101r:DR-05 | F-02, F-11, F-12, F-13, F-16, F-23, F-24, F-35 (8) | pension accrual only as an aggregate scenario on the ONS basis, no pension return, saving stays gross of consumption of fixed capital, O stays a reported residual | ONS UK Economic Accounts and National Balance Sheet downloads; the ONS spreadsheet link was not parseable by the research interface (095r), so the author or code role downloads; series ids to be identified. ONS statistics are published under the Open Government Licence v3.0 (093r reading; licence page not re-checked here) |
| SUP-3 | ONS enquiry: reconciliation of household pension entitlements (AF.6) to WAS Round 8 SCAPE-based pension wealth; note on WAS Table 2.13 against Table 2.11 adult counts; ONS 3222 against NBS financial liabilities | 101r:DR-01 (reconciliation); 102r:R2; 102r:R6 (part) | F-12, F-35, S08, S12, S27 (5) | the three pension bases stay unconverted, adults per household stays on the I-D4h register value, S12 stays a reported mismatch | ONS enquiry (not a download); no response time known. not applicable (correspondence) |
| SUP-7 | Author or analyst items: the source PDFs for I-W1c and the I-W3 rows (Fagereng and others; Bangham and Leslie 2020; Advani, Bangham and Leslie 2021) and the page references; the GDP series behind the register ratio against the pack; the Round 8 top-wealth reconciliation | 101r:DR-09; 102r:R6 (part); 102r:R7 | F-28, F-30, S15, S29, S31 (5) | the four I-W3 rows and I-W1c stay validation context only and unverified; I-D4a and the pack GDP stay as audited in 102r | supplied by the author. as the publishers state; not checked |
| SUP-4 | Bank of England NMG 2011 to 2026 survey (workbook or microdata): values and wave coverage of saving, debt service and income-band variables (be2afree_c, soa1, qbe02, be08free_c, be07free_c, qincomev2) | 101r:DR-06; 102r:R5 | F-36, S13, D04 (3) | no NMG value is used; saving and debt service by income band stay scenario or unset | Bank of England publishes downloadable NMG microdata and example Stata code (095r); the raw files were not downloaded. licence not checked in the repository |
| SUP-5 | HMRC inheritance tax statistics: estates by size band and composition, current years (tables held as ODS in 097r but not parsed) | 102r:R3 | S17, S18 (2) | gifts and inheritances stay unset; the one-heir rule S19 stays the legacy modelling choice | HMRC statistics download. licence not checked in the repository |
| SUP-6 | Mortality by wealth or a linked wealth-mortality estimate for the UK (no source identified in 098r) | 102r:R4 | S24 (1) | mortality stays age and sex only (S24, ready); no wealth gradient | ONS enquiry; no direct published table identified. not applicable |

**Rows with no source known or wanted** (the model proceeds on the classification already given):
- F-25: legacy comparator; no data wanted (author ruling)
- F-28: UK return by rank is not published (101r); SUP-7 only verifies the registered figures
- F-29: no UK source known for saving by wealth band (101r DR-08); SUP-1 could give wealth change by band, not saving
- F-30: foreign figure, gross of gains; no UK counterpart wanted
- S26: no source identified for household formation and dissolution by band

Reading the list:
- **SUP-1 (the WAS microdata) is the largest single supply**: 13 rows, including income, consumption and debt by cell, the stage and band transition matrices and the retirement hazard. It is also the one with an access condition (End User Licence, possible data-owner approval for commercial use). Whether the panel gives *saving* by band is not known; the file could give wealth change by band, not saving (F-29).
- **SUP-2 and SUP-3 together decide the pension basis.** Pension is the largest block in every cell (32.5 to 36.4% of wealth in D4-5 to D10, 38.3% in D1-3; S05) and has no return (F-12) until the AF.6 stock and the SCAPE reconciliation are supplied.
- **No licence or terms are asserted that the repository does not record.** For the Bank of England and HMRC supplies the licence is "not checked in the repository".
- **Nothing here is needed for the first design step.** Every unset row has a stated consequence below, and the model can be specified without any supply.


## 5. Rulings summary and consequence of each unset row
Ruling classes of the 73 rows (the five of the brief, plus those that are not parameters):

| Ruling class | n | Rows |
|---|---|---|
| ready | 22 | F-05, F-07, F-09, F-15, F-19, F-22, F-23, F-26, F-27, F-34, S01, S02, S04, S05, S08, S09, S14, S16, S20, S21, S23, S24 |
| scenario range | 15 | F-03, F-04, F-08, F-10, F-14, F-17, F-18, F-20, F-21, F-31, F-32, F-33, S03, S15, S27 |
| further data | 15 | D04, F-01, F-02, F-06, F-11, F-13, F-36, S07, S10, S11, S13, S18, S22, S25, S28 |
| unset | 11 | F-12, F-16, F-24, F-25, F-28, F-29, F-30, F-35, S12, S17, S26 |
| audit (no ruling) | 5 | S29, S30, S31, S32, S33 |
| validation or proxy only | 1 | S06 |
| legacy comparator | 1 | S19 |
| not applicable (endogenous) | 3 | D01, D02, D03 |

Notes: *ready* rows are observed or derived values with a source and script; *scenario range* rows are implemented only as a labelled range with direction from the evidence; *further data* rows need one of the supplies in section 4; *unset* rows carry no value. S06 is *validation or proxy only* (age of the reference person is a proxy for stage); F-25 and S19 are the legacy rows. A ruling is a proposal for the guru and author; nothing in the register is changed.

**Consequence of each unset row for implementation**

| Row | Variable | Consequence |
|---|---|---|
| F-12 | Pension investment return | No rate for the pension asset: the pension class (about a third of every cell above D1-3) cannot be credited a return. Pension accrual enters only as an aggregate scenario on the ONS basis; 104r decides whether the pension class is held fixed in real terms or excluded from the growth step. |
| F-16 | Housing services yield cross-check | The housing-services yield stays a reported cross-check; the JST housing split (F-20) is the only scenario source, and the ONS B.2g figure cannot calibrate it. |
| F-24 | Aggregate saving over opening net worth (gross of CFC) | No saving rate on wealth is set. Saving enters through the income side of each cell (scenario or unset), never as a share of net worth. |
| F-25 | Legacy I-D14c: 3.5% consumption share of net worth | The kernel keeps 3.5% only as a labelled legacy comparator run; there is no replacement value to implement. |
| F-28 | Audit I-W1c: UK financial return gap, top decile minus bottom deciles (1.8 to 2.0 pp) | I-W1c is validation context only: no return difference by band is set. |
| F-29 | Audit I-W3a: net active saving rate by wealth, 6 to 8% of disposable income | No UK saving by wealth band: band saving is unset or a labelled scenario, direction only; the Norwegian figure is not used. |
| F-30 | Audit I-W3b: gross saving rate top 1% (about 35%) | I-W3b is not used as a saving parameter. |
| F-35 | Pension valuation basis register | No conversion between the three pension bases: flows (ONS) and the stock (WAS SCAPE) stay on their own bases; a rate across them is not formed (C02). |
| S12 | Aggregate liabilities cross-check, ONS 3222 against NBS AF.L | The aggregate liabilities mismatch (ONS 3222 against AF.L, ratio 0.69) is reported; no debt aggregate constrains the cells. |
| S17 | Gifts and inheritances by band and stage | No gifts or inheritances by cell: `TR` is zero in aggregate and absent by cell; the one-heir rule (S19) is the only transfer in the kernel. |
| S26 | Household formation and dissolution | Household formation and dissolution are absent: cell membership is fixed within a generation step. |

The 15 *further data* rows (F-01, F-02, F-06, F-11, F-13, F-36, S07, S10, S11, S13, S18, S22, S25, S28, D04) have the same consequence in kind: the parameter is absent until its supply arrives, and the model uses an aggregate or a labelled scenario range with no value chosen for effect on WDT.


## 6. Differences from the existing register
Read-only. 26 existing register rows are named across 101r and 102r; each has a line in `register_differences.csv`. Rows I-D4a, I-D4b and I-D4h were annotated or corrected on main by 105c after the 102r audit; those edits are listed as already made, and no other register edit is made or proposed here as an edit (the recommended actions are for the guru and author).

| Row | Verdict | Finding | Already on main (105c) | Recommended action |
|---|---|---|---|---|
| I-D1a | supports | JST arithmetic real mean 4.742% against 4.74 | none | no change |
| I-D1a2 | no disagreement; no additive split | geometric mean has no additive yield and gain split | none | keep as the geometric comparator; the split rows are arithmetic |
| I-D14c | legacy comparator, not evidence | 3.5% (0.5 to 5) has no UK source (093r); author decision 2026-11-21 | run labelling in 057c | keep only as a labelled legacy run; no replacement scalar |
| I-W1c | unverified; proxy for validation | composition-implied financial return gap; figures not in a held file; direction agrees with AB-05 | none | validation context only; verify with DR-09 (SUP-7) |
| I-W3a | foreign; proxy (J central) | Norway, % of disposable income; no UK saving by wealth band held | none | not a UK value; do not use as a band saving rate |
| I-W3b | reclassify: saving plus gains, not saving | gross of unrealised gains (S + CG), so it must not feed a saving term (094r B3 case 6c) | none | author or guru to reclassify as context only |
| I-W3c | validation moment; citation unreconciled | share of the change in financial wealth that is saving; register cites Bangham and Leslie 2020 Fig 6, 099r read the 2021 paper | none | resolve the citation with DR-09; midpoint 15 is not an estimate |
| I-W3d | validation moment; RF basis; page unreconciled | active saving about 40% of the total wealth gain; Resolution Foundation basis excludes DB pensions; page 22 against 099r pages 21, 13, 5 | none | resolve the page with DR-09; not on the WDT pension basis |
| I-D4a | central supports; low and high unverified; GDP differs from the pack | 5.94 reproduces; pack GDP 2,211.48bn gives 6.14 (3.2%); held NBS S.14 over the same GDP gives 5.03 | 105c annotated the row (unverified low and high, GDP mismatch); not reconciled | open: reconcile the pack GDP with the register GDP; verify low and high (SUP-7) |
| I-D4b | low supports; high inside the held bracket; central below it and untestable | low 49.3 reproduces as a household share; bracket 59.2 to 72.7; central 54.9 implies 1.77 adults per household | 105c relabelled the bounds as household shares and flagged the central | open for the author: the central (lognormal fit) cannot be tested by a held table |
| I-D4c | not tested; depends on the I-D4b central | share of wealth held by the adults above W_min; derived from I-D4b | none | moves with I-D4b; no separate evidence |
| I-D4d | supports as a range | top 1% share 14.4 to 23.0 published | none | keep as a range; WID 21.3 (2024) is on a different basis (S32) |
| I-D4e | supports as a range | wealth missing from the WAS top, 0 to 5.6% of total | none | keep as a range; no single value |
| I-D4g | supports the level; ratio not reproducible | held NBS S.14 net worth end-2025 GBP 10,829bn; ratio 3.6 uses a GDP not held | none | cross-check only; do not mix with the I-D4a survey basis (C08) |
| I-D4h | central supports; Table 2.13 differs; old low contradicted | 1.93 reproduces (1.9282); Table 2.13 gives 1.8593; the earlier low 1.77 was an assumption | 105c set the low to 1.86 | closed; the 16+ against 18+ definition stays an author decision |
| I-W4a | supports | 80% top-decile stay (AB-02) | none | no change |
| I-W4b | supports | 90% of entrants from the ninth decile (AB-02) | none | no change |
| I-W4c | supports; central is a midpoint | 74 and 77 reproduce (Table 1); 75.5 is the register midpoint (J) | none | age-adjusted income groups, not wealth bands |
| I-W4d | not audited against a held file | Norway 11-year move to the top 1% | none | foreign; context only |
| I-W4e | not audited against a held file | Norway bottom decile to the top decile | none | foreign; context only |
| I-W4f | not audited against a held file | UK rank-rank slope 0.27 to 0.37 | none | not audited; no held table |
| I-W5a | supports | 40.71 reproduces from Table 2.2; low 40.1 reproduces | none | high 43.9 depends on the I-D4e add-on |
| I-W5b | derived (J); not tested | Pareto-implied household top 1%; not tested against a held file | none | not tested here |
| I-W5c | definitions differ from the pack tail | WID top 1% 21.3 (2024 adults) against 14.4 to 23.0 (2016-18) | none | not averaged; different years and definitions |
| I-W5d | definitions differ from the pack tail | WID top 10% 57.1 (2024) against 52.4 to 52.5 (2016-18) | none | not averaged |
| I-W5e | supports | pension share 35.43 against 35.4 | none | no change |

Partition of the 26 rows by verdict: **supports or reproduces** 11 (I-D1a, I-D4a central, I-D4d, I-D4e, I-D4g level, I-D4h central, I-W4a, I-W4b, I-W4c, I-W5a, I-W5e); **a part unverified, contradicted or reclassified** 6 (I-D4b central, I-W1c, I-W3a, I-W3b, I-W3c, I-W3d; I-D4a low and high and the I-D4h low are further parts of rows counted above, already annotated or corrected by 105c); **definitions differ** 2 (I-W5c, I-W5d); **not audited or not testable** 5 (I-D4c, I-W4d, I-W4e, I-W4f, I-W5b); **legacy or no disagreement** 2 (I-D14c, I-D1a2). **Open after 105c:** the I-D4a GDP mismatch and unverified low and high; the I-D4b central; the I-W3b reclassification; the I-W3c and I-W3d citation and page differences.


## 7. Reproduction
From the repository root with `python -I`, in this order (each reads committed files only):
1. `research/scripts/merge_and_check.py` -> `parameter_register.csv` (73 rows), `source_crosswalk.csv` (25), `dictionary_map.csv`, `unresolved_data.csv`, `register_differences.csv`. Exits 1 on any structural failure (repeated name, unclassified row, unset row with a value, dictionary term without a row, named existing row without an entry, pension row without a basis, request or unset row left uncovered). Last run: 0 failures.
2. `research/scripts/cross_side_checks.py` -> `cross_side_checks.csv` (14 checks), `worked_cell_d45.csv`. Exits 1 if a hard check (C01, C04, C05, C07) fails. Last run: 0 hard failures.
The 101r and 102r scripts that produce the inputs are listed in their notes; they were not re-run here except as their CSVs are read.

