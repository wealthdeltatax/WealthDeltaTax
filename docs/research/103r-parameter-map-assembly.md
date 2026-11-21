# 103r: parameter map, assembly: one register, cross-side checks, unresolved data and proposed rulings

Accessed 2026-11-21. Brief `docs/briefs/103r-parameter-map-assembly.md`. Closes deliverables A, B and E of the parameter map: merges 101r (flows) and 102r (stocks, cells, transitions, debt). Data and script: `docs/research/data/103r/`. No register, code, pack or manifest edit; no model run.

Status: in progress; sections still marked pending are not yet written.

## 1. Summary
(pending)

## 2. Merged register and crosswalk
Files in `docs/research/data/103r/`, built by `merge_and_check.py` from the committed 101r and 102r CSVs (no source file is re-read):
- `parameter_register.csv`: 73 rows = 36 flows (F-01 to F-36) + 33 stocks (S01 to S33) + 4 dictionary rows (D01 to D04). Columns: the common 14 of 101r and 102r, plus `class_norm`, `ruling_class`, `pension_basis` and `dictionary_terms`. 102r's rows carried a long definition in place of a name; the script gives each a short unique name (33 names, one per row).
- `source_crosswalk.csv`: 25 sources (12 from 101r with prefix A-, 13 from 102r with prefix B-), same columns. A source used by both sides appears twice, once per side's reference (the ONS household series A-X01 to A-X05 and the NBS series B-X08), and the two rows are not merged because their exact references differ.
- `dictionary_map.csv`: each 094r B2 term and the register rows that carry it.

**Structural checks (all pass, exit 0):** no repeated variable name or row id; no row without a classification; no unset row carries a value; every pension row carries exactly one stated basis from a closed set (section 3, check 1); every one of the 19 dictionary terms names at least one existing row; every existing register row named in the 101r and 102r notes and audits (26 ids) appears in a merged row.

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
(pending)

## 5. Rulings summary and consequence of each unset row
(pending)

## 6. Differences from the existing register
(pending)

## 7. Reproduction
(pending)
