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
(pending: pension basis; cash-yield and gain convention with a worked cell; flows against stocks; survey against national accounts; units and price basis)

## 4. Unresolved-data list
(pending)

## 5. Rulings summary and consequence of each unset row
(pending)

## 6. Differences from the existing register
(pending)

## 7. Reproduction
(pending)
