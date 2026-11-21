# 101r: parameter map, side A: income, saving, consumption, returns and pension flows

Accessed 2026-11-21. Brief `docs/briefs/101r-parameter-map-flows-and-returns.md`. Evidence side A for the household account of `094r` (B1, B2); companions 102r (stocks, cells, debt) and 103r (assembly). Data and scripts: `docs/research/data/101r/`. No register, code, pack or manifest edit comes from this note, and no model was run.

## Status of this note
Built in blocks, one push each. Block 1 (ONS flows), block 2 (JST split, HMRC 3.7, tables) are committed with scripts. This file holds, in order: basis (2), crosswalk (3), register view (4), existing-row audit (5), flow-side constraints (6), data requests (7), reproduction list (8), and the closing summary (1, filled last).

## 1. Summary
(Filled at the last block.)

## 2. Basis and rules
- **Scenario B** (author, 2026-11-21): cells are wealth band by life stage; saving is on the income side; a parameter with no UK evidence is *unset* or a labelled *scenario*; there is no universal scalar; nothing is chosen for its effect on WDT revenue, fund fill or closure.
- **Pension wealth is inside the WDT base** on the ONS SCAPE-based basis the pack uses. Every pension row names its basis. Three bases appear and are never mixed: ONS national-accounts net equity (D.8, AF.6); WAS Round 8 SCAPE-method DB wealth (the pack); the Resolution Foundation basis (excludes DB; validation context only). No conversion factor is held (F-35).
- **3.5% (I-D14c)** is a legacy comparator. It is row F-25, classed *scenario (legacy comparator)*, intended use *neither*.
- Sources with different definitions are reported side by side and not averaged or spliced (for example UKEA against QSA vintages, DGD8 against CSJ8, ONS B.2g yield against the JST housing yield).
- Accounting locations are those of 094r B1 (`dNW = S + CG + TR + O - T_WDT`) and B2; `Y_L`, `Y_P`, `T_C`, `C`, `K`, `CG`, `O` as defined there.
- Classification: *observed*, *derived*, *proxy*, *scenario*, *unset*. Every value reproduces from a script in `docs/research/data/101r/` (section 8); tolerances are in the check files.

## 3. Source crosswalk (flows)
Full columns (period, unit and price basis, definitions, dimensions, revisions, whether the held file was checked against the published source) are in `docs/research/data/101r/flows_crosswalk.csv`. One line per source here.

| Id | Held file or table | Publisher | Period | Checked against published | Register rows |
|---|---|---|---|---|---|
| X-01 | docs/research/data/097r/ons_ukea_household_annual.csv (UKEA tables 6.2.3 to 6.2.7, 6.1.9, 6.1.10; series ids per row) | ONS | 1997-2025 annual (financial 1998-2025) | Identities pass internally (derive_ons_flows.py, 392 checks); not re-fetched, the workspac | F-01 to F-14, F-21 to F-24 |
| X-02 | docs/research/data/097r/qsa_household_annual_2026q2.csv (sheets HH_1 to HH_3, HH_Alt) | ONS | 1948-2025 annual (varies by series) | Workbook held (quarterlysectoraccounts2026q2.xlsx); the CSV was extracted by 097r; QSA1 ch | F-05, F-07 to F-10 |
| X-03 | docs/research/data/097r/ons_nbs_household_stocks_annual.csv (E45V, E46V, E44N, E462, E3VW) | ONS National balance sheet | 1997-2025 end-year | Identity E45V=AN.1+AN.2+BF.90 passes (ID8); not re-fetched | F-16, F-23, F-24 |
| X-04 | docs/research/data/097r/ons_nbs_financial_annual.csv (NYOH, NITF, NIWJ) | ONS | 1997-2025 | Used in ID8; not re-fetched | F-21, F-23 |
| X-05 | docs/research/data/097r/ons_household_consumption_annual.csv (ABPB) | ONS UKEA | 1997-2025 | Equals ABPB in X-01 | F-06 |
| X-06 | docs/research/data/097r/hmrc_csv/Collated_Tables_3_1_to_3_11_2324__Table_3_7.csv | HMRC Personal Incomes Statistics | Tax year 2023-24 | Column sums reproduce 'All ranges' within 1.5% (derive_hmrc_37.py) | F-14, F-15 |
| X-07 | docs/research/data/097r/hmrc_html_summary_extracts.csv; property_rental_income_statistics_tables_2026.ods | HMRC rental income | 2023-24, 2024-25 | No | context only; no register row |
| X-08 | docs/research/data/097r/nmg_variable_inventory_2011_2026.csv | Bank of England NMG household survey | 2011-2026 (waves) | Inventory only | F-36 |
| X-09 | docs/research/data/100r/returns_decomposition.csv | Jorda-Schularick-Taylor R6 via 100r | UK 1896-2019, 117 years (1940-46 absent) | Reproduced to 0.0004pp (derive_jst_split.py) | F-16 to F-20, F-26, F-27 |
| X-10 | docs/research/095r-bozio-2013-reading.md | Bozio | 1978-2009 (LCFS), ELSA linked records | No | F-33 |
| X-11 | docs/research/data/099r/moments.csv (BF-02, AB-01, AB-05, GB-01) | Resolution Foundation Before the fall; Advani-Bangham-Leslie | 2008-2022 | Rows as recorded by 099r | F-28, F-31, F-32, F-34 |
| X-12 | docs/model-v3/inputs.md rows I-W3a to I-W3d, I-W1c | Fagereng et al.; Bangham and Leslie 2020 (source PDFs not he | Norway 2005-15; GB 2008-22 | No | F-28 to F-32 |

Reading the crosswalk:
- X-01 to X-05 are the ONS series held by 097r; the script `derive_ons_flows.py` reproduces the saving identity and the pension and non-pension split from them (392 checks, 0 hard failures).
- X-07 is context only: the rental income ODS contents were not parsed, so it feeds no row.
- X-08 is a variable inventory only (696 variable names and labels, no values); NMG microdata and the workbook are not held, so no NMG value is used (F-36, data request DR-06).
- X-10 to X-12 are secondary or foreign sources and are used for direction or validation only; X-12's figures are not verifiable from held files because the source PDFs are not held.

## 4. Parameter register (flows)
One row per parameter in `docs/research/data/101r/flows_register.csv` (14 columns: definition, accounting location, target cell dimension, classification, exact source reference, calculation and script, value or range, caveats, intended use, proposed ruling, relation to an existing register row, data request). This table is the short view; an unset row has no number.

| Id | Variable | Class | Value or range (only where supported) | Use | Ruling |
|---|---|---|---|---|---|
| F-01 | Labour income: compensation of employees (D.1), share of gross primary income | Observed (aggregate) | 2024: 66.8%; 1998-2025 min/median/max 61.8/67.0/68.9% | calibration (aggregate constraint) and validation | further data required (by cell) |
| F-02 | Self-employment and housing services: gross operating surplus plus mixed income (B.2g+B.3g), share of B.5g | Observed (aggregate) | 2024: 21.3%; 1998-2025 min/median/max 17.7/20.4/22.0% | constraint and validation | further data required (split of B.2g into imputed rent and lettings) |
| F-03 | Transfer income: social benefits in cash (D.62) share of disposable income | Observed (aggregate) | D.62 share of B.6g 2024: 27.2%; 1998-2025 min/median/max 22.9/26.3/29.0%; D.622 only 2024: 9.2%; 1998-2025 min/median/max 7.4/9.1/ | calibration (aggregate) | implement with scenario range |
| F-04 | Taxes on income and wealth (D.5), share of gross primary income | Observed (aggregate) | 2024: 17.4%; 1998-2025 min/median/max 14.4/15.3/17.8% | calibration (aggregate) | implement with scenario range |
| F-05 | Gross disposable income B.6g | Observed | 2024: GBP 1801.4bn | calibration | ready for implementation |
| F-06 | Household final consumption (P.31) as a share of B.6g | Observed (aggregate) | 2024: 94.9%; 1998-2025 min/median/max 86.1/98.9/102.8% | calibration (aggregate); validation | further data required (by band) |
| F-07 | Saving ratio, published | Observed | 2024: 9.5%; 1998-2025 min/median/max 5.0/7.1/16.5% | validation | ready for implementation |
| F-08 | Non-pension saving: B.8g - D.8 (the part of the ratio not pension accrual) | Derived | ratio contribution 2024: 4.9pp; 1998-2025 min/median/max -2.6/1.0/13.5pp | validation (aggregate); calibration only with a labelled sce | implement with scenario range |
| F-09 | Cash-basis saving ratio (CSJ8) | Observed (alternative definition) | 2024: 7.4%; 1998-2025 min/median/max -3.6/1.6/17.2% | validation | ready for implementation (as a reported alternative) |
| F-10 | Pension accrual: adjustment for change in pension entitlements D.8 | Observed (aggregate) | share of B.6g 2024: 4.8%; 1998-2025 min/median/max 3.0/7.3/9.7%; of open net worth 2024: 0.8%; 1998-2025 min/median/max 0.4/1.2/1. | calibration (aggregate pension flow) with named basis | implement with scenario range |
| F-11 | Pension contributions (employee and employer) | Proxy | levels in derived_ons_flows.csv only; no pension-only series | context only | further data required |
| F-12 | Pension investment return | Unset | unset | none | remain unset |
| F-13 | Pension withdrawal and decumulation | Proxy | ratio D8/D622 descriptive: 2024: 0.53; 1998-2025 min/median/max 0.31/0.78/1.18 | context only | further data required |
| F-35 | Pension valuation basis register | Observed (labelling) | unset | validation context only for RF | remain unset (no conversion factor) |
| F-14 | Retained cash property income (D.4 received excluding D.441 and D.442), share of B.6g | Derived | 2024: 13.3%; 1998-2025 min/median/max 8.6/10.8/14.1% | calibration (aggregate constraint) | implement with scenario range |
| F-15 | HMRC taxable interest and dividends against ONS D.41 and D.42 | Observed | interest 0.19 and dividends 0.52 of ONS 2024 (tax-year 2023-24 against calendar 2024) | validation only | ready for implementation (as a coverage check) |
| F-16 | Housing services yield cross-check | Proxy | ONS 4.66% vs JST 3.00% (1998-2019 mean); difference 1.66pp | validation only | remain unset (as a calibration) |
| F-17 | Cash yield, portfolio, real (JST market portfolio, arithmetic mean of annual components) | Derived | 1896-2019 mean 4.034% (sd 1.0); 1980-2019 mean 3.857%; 1896-1939 3.722%; 1947-1979 4.665% | calibration with a scenario range across the period means; n | implement with scenario range |
| F-18 | Holding gain, portfolio, real (JST market portfolio, arithmetic mean of annual components) | Derived | 1896-2019 mean 0.708% (sd 8.0); 1980-2019 mean 3.106%; 1896-1939 -0.022%; 1947-1979 -1.225% | calibration with a scenario range across the period means; n | implement with scenario range |
| F-19 | Total return, real, arithmetic (JST) | Derived | 1896-2019 mean 4.742% (I-D1a central 4.74) | calibration | ready for implementation (already in the register) |
| F-20 | Cash yield and gain by asset class (real) | Derived | 1896-2019 mean real yield equity 4.352, housing 3.758, bond 5.270, bill 4.393 (% per year) | calibration via cell asset weights (102r) | implement with scenario range |
| F-21 | Revaluation of nominal liabilities (real erosion) | Derived | as share of opening net worth 2024: 0.58%; 1998-2025 min/median/max -0.11/0.33/1.44% | constraint and validation | implement with scenario range |
| F-22 | Holding gains on financial assets (B.103) and other volume changes (B.102) | Observed | B.103 2024: GBP -168.1bn; of which equity 58bn, pension and insurance -218bn | validation | ready for implementation (as a reported series) |
| F-23 | Net-worth residual O | Derived | share of opening NW: 2024: 0.9%; 1998-2025 min/median/max -8.5/2.4/10.3% | constraint | ready for implementation (as a reported residual) |
| F-24 | Aggregate saving over opening net worth (gross of CFC) | Derived | all saving 2024: 1.7%; 1998-2025 min/median/max 0.7/1.3/2.3%; non-pension 2024: 0.9%; 1998-2025 min/median/max -0.5/0.2/1.9% | constraint (aggregate saving over wealth) | remain unset (as a rate) |
| F-25 | Legacy I-D14c: 3.5% consumption share of net worth | Scenario (legacy comparator) | 3.5 as legacy comparator only (range 0.5 to 5 in the register) | neither | remain unset |
| F-26 | Existing row I-D1a (arithmetic mean real total return 4.74) | Observed (source JST); proxy for household return | reproduced 4.742% | calibration | ready for implementation |
| F-27 | Existing row I-D1a2 (geometric 4.42) | Derived | no additive split | calibration | ready for implementation |
| F-28 | Audit I-W1c: UK financial return gap, top decile minus bottom deciles (1.8 to 2.0 pp) | Proxy | row range 1.8 to 2.0 pp (as registered) | validation only | remain unset (as calibration); keep as validation |
| F-29 | Audit I-W3a: net active saving rate by wealth, 6 to 8% of disposable income | Proxy (foreign) | row range 6 to 8% (as registered) | context only | remain unset (UK) |
| F-30 | Audit I-W3b: gross saving rate top 1% (about 35%) | Proxy (foreign), different definition | row point 35% | context only | remain unset |
| F-31 | Audit I-W3c: net saving share of the change in family financial wealth (7 to 24%) | Proxy (validation) | row range 7 to 24% (as registered) | validation only | implement with scenario range (validation) |
| F-32 | Audit I-W3d: active saving about 40% of total wealth gain, 2018-20 to 2020-22 | Proxy (validation) | row point 40% | validation only | implement with scenario range (validation) |
| F-33 | Saving by lifetime income and education (direction) | Scenario | direction only; gap of the order of 4 points of income (median, highest education against compulsory-only), a nearest UK bound, no | scenario range (labelled) | implement with scenario range |
| F-34 | Passive and active share of wealth change (validation moments) | Observed (moment) | 53%; 60%; 76 to 93% (as published) | validation only | ready for implementation (as validation moments) |
| F-36 | NMG survey saving and debt-service variables | Unset | unset | none | further data required |

## 5. Audit of existing register rows (I-W3a to I-W3d, I-W1c)
Read-only: the register is not edited. "Held check" says what a held file lets me verify. The four source PDFs (Fagereng and others; Bangham and Leslie 2020; Advani, Bangham and Leslie 2021; Before the fall) are not all held; where a figure was read by 099r from a held PDF the moment id is given. Detail rows: F-28 to F-32 in `flows_register.csv`.

| Row | What it is | Does the source support the definition and population? | Held check | Classification the evidence gives | Disagreement or caution |
|---|---|---|---|---|---|
| I-W1c (1.8 to 2.0 pp) | UK mean financial return implied by portfolio composition, top wealth decile against bottom deciles, WAS 2016-18, financial wealth only | Yes as a *composition-implied* return, which the row says. It is not an observed return and not a total return on wealth | The figures (2.2% top, 0.2 to 0.4% bottom) are not in a held file. Direction agrees with AB-05 (share of financial wealth in zero-return assets falls from 71% in the lowest to 17% in the top decile, read from a chart) | **Proxy**, validation only (register says judgement) | The numeric gap cannot be verified here; the authors say the true gap is probably larger. Excludes housing and pensions, so it cannot calibrate a return by band on the WDT base |
| I-W3a (6 to 8%) | Net active saving rate by wealth percentile, Norway 2005-15, % of disposable income | Supports its own definition (Norway, read from a figure); the register says foreign | Not verifiable: PDF not held | **Proxy (foreign)**; context only | Not a UK value. No UK saving by wealth band is held (F-33 is by income and education). The UK aggregate non-pension saving (F-08) has a different denominator and is for scale only, not a test. The central is the midpoint of a figure reading (J) |
| I-W3b (35%) | Gross saving rate of the top 1%, Norway, **includes unrealised capital gains** | Yes, and the register says it is not comparable with a household saving ratio | Not verifiable | **Proxy (foreign), different definition**: it is `S + CG`, not `S` | **Contradicts use as a saving rate** in the 094r account: it mixes saving and holding gains, so feeding it to an `S` term would count gains twice (094r B3 case 6c). Keep as context only |
| I-W3c (7 to 24%, central 15) | Share of the change in GB family *financial* wealth that is net saving, the residual after asset prices and yields | Supports: 099r AB-01 gives asset-price-and-yield shares of 93, 93, 82, 76 and 79%, so saving 7 to 24%. It is a **share of change**, not a saving rate | Bar labels read from a page image by 099r; the text names only the first (93%) | **Proxy (validation)**: average family, financial wealth only, not by band | Citation differs: the register cites Bangham and Leslie 2020 Fig 6 (p. 18); 099r read the chart in the 2021 journal paper (PDF p. 15) and notes the source is the 2020 report. Same method, two citations, not reconciled. The central 15 is the midpoint of a range that varies by period, not an estimate. Excludes pensions, so it does not map to the WDT base |
| I-W3d (about 40%) | Active saving as a share of the total wealth gain, 2018-20 to 2020-22, GB, including housing | Supports: 099r BF-02 gives active 40% in the latest period (47% over the longer period since 2010-12) | Read from text by 099r; the report is held | **Proxy (validation moment)**; one two-year window including pandemic saving | Resolution Foundation basis **excludes DB pensions**, so it is not the WDT pension basis (F-35). The register cites p. 22 Fig 7; 099r records pages 21, 13 and 5; the page difference is not resolved here (printed against PDF page not checked) |

Findings from the audit:
1. **Four rows, four denominators.** I-W3a is a share of disposable income; I-W3b a share of disposable income including gains; I-W3c a share of the change in financial wealth; I-W3d a share of the change in total wealth. They cannot be compared with each other or with the ONS saving ratio without a conversion that no held file supports. They are not averaged here.
2. **None is a UK saving rate by wealth band.** The nearest UK evidence is aggregate (F-07 to F-10) or by income and education (F-33). So the band-specific saving parameter stays *unset or a labelled scenario* in Scenario B.
3. **Only I-W3c and I-W3d are UK, and both are validation moments** for the split of wealth change into saving and gains, on bases that exclude pensions (financial wealth only) or DB pensions (RF basis). They check an output; they do not set an input.
4. **I-W3b should not feed a saving term** (a classification, not an edit: for the author or guru).
5. **I-D1a is reproduced** (F-26: 4.742% against 4.74; `derive_jst_split.py`) and **I-D1a2 cannot be split** into yield and gain (F-27): geometric means are not additive.
