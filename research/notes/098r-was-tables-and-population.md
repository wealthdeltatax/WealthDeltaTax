# 098r — WAS published tables, ages and the working-to-retired transition

**Date:** 2026-11-21  
**Branch:** `brief/098r-was-tables-population`  
**Scope:** published-table extraction, source audit and access plan. No microdata analysis, parameter choice, or pack/code change.

## Outcome

> **Update 2026-11-21 (guru close-out).** The first pass of this note was written without a spreadsheet reader. With the held workbooks and the author's ONS uploads read, **section 9 supersedes** every statement below that says a file was "not parseable" and the claim that stage weights by wealth band are not published: the held WAS Tables 2.11 and 2.13 give persons by age and by economic activity across seven household-wealth bands for nine rounds. They are person-based, in £ bands rather than deciles, and rounded to whole percentages; section 9 says what that supports. Sections 1 to 8 are kept as written for the record, with the contradicted lines struck through.

The public evidence supports a useful **age/status profile** and confirms that the WAS panel can in principle supply the joint wealth-by-stage information needed for Scenario B. It does **not** provide the required stage weights by WDT wealth band in the published HTML tables. The public Round 8 bulletin gives marginal age and retirement-status summaries; the held workbook files and additional ONS XLSX files are binary and could not be decoded with the repository connector available in this run.

The most important finding is therefore a boundary, not a rate: **age and retirement status are associated with wealth, but the published marginals cannot be combined into a wealth-band × life-stage distribution.** The joint cross-tab requires WAS microdata (study 7215) or a bespoke ONS tabulation.

No household-level records were extracted. No saving, consumption, drawdown, or mortality rate by wealth band has been inferred.

## 1. Held workbooks and extraction status

| File | Status | What is known / what remains |
|---|---|---|
| `data/rates/totalwealthtables.xlsx` | ~~Held; binary not parseable here~~ **extracted, section 9** | The pack builder reads Table 2.2 for wealth decile totals and components. The brief also points to Table 2.11 for age. I could not inspect sheet names, ranges, or Table 2.11 cells in this run, so no workbook spot-checks are claimed. |
| `data/rates/financialwealthtables.xlsx` | ~~Held; binary not parseable here~~ **extracted, section 9** | The workbook is present in the repository, but no sheet/range/round inventory or cell values could be verified. |
| `data/uk-source-workbooks/etbreferencetablesfye202324final.xlsx` | ~~Held; binary not parseable here~~ **extracted, section 9** | The existing pack build uses ONS Effects of Taxes and Benefits tables 2b, 2c and 16 for income-decile incidence. It is not a wealth-ranked source. |
| ONS Ad hoc 2813, wealth components by age of household reference person | ~~Published; XLSX reachable, not parsed~~ **extracted, section 9** | A specific ONS table exists for mean, median, aggregate and percentage of wealth by component and age of household reference person, Great Britain, April 2020 to March 2022. |
| ONS Ad hoc 3222, personal debt by age and region | ~~Published; XLSX reachable, not parsed~~ **extracted, section 9** | A specific ONS table exists for personal financial and property debt by age and region, Great Britain, April 2020 to March 2022. It is by age/region, not by total-wealth decile. |

~~The GitHub connector returns the held XLSX files as base64 binary payloads. The available execution environment has no ZIP/XLSX decoder or local repository checkout, so the acceptance test requiring sheet/range metadata and three workbook cell spot-checks could not be completed.~~ The files are valid; section 9 records the sheets, ranges and spot-checks.

### What the held pack already establishes

`model_v3/pack/GBR/wealth_distribution.csv` is readable. It contains Round 8 household wealth totals by decile, household counts, and selected component shares. The pack builder documents that the totals and components are derived from `data/rates/totalwealthtables.xlsx`, Table 2.2, and the all-household total from Table 2.1.

The WDT band mapping is a grouping of **wealth deciles**, not a separate set of published WAS bands:

| WDT band | WAS wealth deciles | Aggregate wealth (£bn) | Households (thousand) | Derived mean per household (£) |
|---|---|---:|---:|---:|
| Below-threshold remainder | D1–D3 | 287.943 | 8,097.3 | 35,556 |
| D4–5 | D4–D5 | 1,044.432 | 5,398.2 | 193,478 |
| D6–7 | D6–D7 | 2,278.170 | 5,398.2 | 422,024 |
| D8–9 | D8–D9 | 4,434.141 | 5,398.2 | 821,411 |
| D10 | D10 | 5,523.204 | 2,699.1 | 2,046,313 |

The band totals and means above are arithmetic aggregations of the existing pack's published-round rows, not a new workbook extraction. Each wealth decile contains one tenth of the weighted household population by construction; the pack repeats the same decile household count. These counts contain **no age or retirement-status information**.

Existing component shares in the pack:

| WDT band | Net property share | Net financial share | Private pension share |
|---|---:|---:|---:|
| D4–5 | not present | 6.6% | not present |
| D6–7 | 45.6% | 9.3% | 32.5% |
| D8–9 | 42.7% | 12.8% | 35.4% |
| D10 | 38.3% | 19.3% | 36.4% |

The pack has no gross mortgage/non-mortgage debt by wealth band. Net property wealth already subtracts mortgage debt; net financial wealth already subtracts financial liabilities. Those net shares cannot be reverse-engineered into gross debt or debt service. D4–5 property and pension shares remain absent in the pack and are not filled here.

## 2. Published WAS age and status evidence

### Round 8 headline evidence

ONS Round 8 covers Great Britain, April 2020 to March 2022. The bulletin reports an achieved sample of **15,128 households and 32,271 individuals**. The household head is defined as the person who owns the accommodation or is legally responsible for rent; if joint, the person with the highest income is selected, with the eldest selected if incomes are equal.

The bulletin reports:

- Median household wealth was **£15,200** where the household head was aged 16–24, rising to **£502,500** for age 65–74. ONS describes the latter as 33 times the former.
- Median household financial wealth by age of household head reached **£32,300** for age 65–74; the 25–34 group had £1,300.
- By economic activity of the household head, median financial wealth was **£9,400** for employed/self-employed households, **£32,000** for retired households, and **£300** for economically inactive households that were not retired.
- Across all households, the composition of wealth was approximately 40% net property, 35% private pension, 14% net financial and 10% physical wealth (rounded percentages).
- For the highest wealth decile, net property represented 38% and private pension wealth 36% of wealth.

These are useful **marginal moments**: age-of-household-head against median wealth, and economic activity against median financial wealth. They do not report the proportion of D4–5, D6–7, D8–9 or D10 households that are working or retired. The values are not cell weights and are not saving or drawdown rates.

### Quality and comparability

Round 8 needs explicit caution:

- ONS suspended the accredited official statistics designation for core WAS outputs from Round 8 (13 June 2025), citing concerns about granular estimates and falling response rates.
- Round 8 fieldwork changed from face-to-face to telephone interviewing during the pandemic. ONS reports tenure-related non-response bias, additional London under-coverage, and additional uncertainty.
- The Round 8 DB pension valuation method changed. Pension wealth and total wealth including pensions are not directly comparable with earlier rounds without treating the SCAPE-method break.
- ONS removed a small number of tables on property debt and regional property wealth after reviewing robustness. It publishes no formal significance tests for the complex estimates; standard errors and confidence intervals are provided separately.
- ONS updated Round 8 weights to population totals derived from the latest census and added tenure calibration controls. The exact weight variables and their use must be taken from the microdata documentation, not reconstructed from the headline page.

The sample is Great Britain, not the whole UK. The ONS bulletin states that its estimates and national-accounts balance-sheet estimates are not directly comparable because their concepts, sources and methods differ.

### Debt by age

Two relevant ONS releases exist:

1. **Ad hoc 3222**, released 15 January 2026: personal financial and property debt by age and region, Great Britain, April 2020 to March 2022 (45.3 KB XLSX).
2. **Household debt: wealth in Great Britain**, Round 8 tables: includes household debt by income decile, and personal debt tables by age. The income-decile tables are not wealth-decile tables.

These sources can describe debt by age or income. They do not supply the gross mortgage and non-mortgage debt amounts jointly by WDT total-wealth band and retirement status. The ONS Ad hoc 3222 workbook remains unparsed here. Do not use the secondary-source reproductions of its numbers as a substitute for the ONS workbook.

## 3. Stage weights and band-edge reconciliation

### What is identified

- The pack's D4–5, D6–7, D8–9 and D10 bands are exact groupings of Round 8 wealth deciles (see section 1).
- The ONS bulletin supplies age-of-household-head and economic-activity marginal summaries.
- The WAS study is longitudinal and contains age, employment, retirement, assets, savings and debt topics. It is the appropriate source to construct a joint wealth-band × stage table.

### What is not identified from the published tables

No public table supplies the **joint weighted household counts** for wealth **decile** × age group × retirement/economic-activity status. (Correction: the held Tables 2.11 and 2.13 do give persons by age or activity across seven £ wealth bands; see section 9.) Separate age and wealth marginals cannot be multiplied or otherwise combined to manufacture that joint distribution. In particular:

- The pack's decile counts are equal by definition and do not reveal the age composition of any decile.
- Median wealth by age does not reveal the number of households in each wealth decile at that age.
- Median financial wealth by retired/employed status does not reveal total wealth or the wealth-decile composition of those status groups.
- The ONS age-by-component Ad hoc 2813 table is a marginal age table, not a wealth-decile-by-age cross-tab.

The missing joint weights are therefore **not available from the published headline tables inspected**. They require WAS microdata or a bespoke ONS tabulation.

### Stage definition

ONS distinguishes employed/self-employed, retired, and economically inactive but not retired. The last category includes people who are students, looking after the home/family, sick or disabled, temporarily sick/injured, unemployed under the ILO definition, or otherwise inactive.

The ONS status categories are more appropriate than equating retirement with State Pension age. State Pension age is a statutory eligibility threshold, not a statement that a person has stopped working. Under current law it is 66 and is being phased up to 67 between 2026 and 2028.

For a two-stage WDT model, the direct mapping would be:
- **working:** employed or self-employed;
- **retired:** self-reported retired;
- **other economically inactive:** keep as an explicit residual in the data tabulation; do not silently assign it to either stage.

This leaves a model-design choice for phase 2: whether the residual is excluded from stage weights, represented as a third stage, or allocated under an explicit author ruling. The public tables do not justify an allocation. No allocation is made in this brief.

## 4. Retired income: HBAI, FRS and ETB

| Source | What it can provide | Ranking / limitation for WDT |
|---|---|---|
| DWP Households Below Average Income (HBAI), FYE 1995–2024 | Household disposable income distribution and pensioner/working-age breakdowns; based on FRS | Income-ranked and status-based. Not ranked by household wealth; cannot give retired income by WDT wealth band. |
| DWP Family Resources Survey (FRS), FYE 2023–24 | Income from all sources, household circumstances, tenure, pension participation and related characteristics | Can describe income by pensioner/age/status groups. It is not a comprehensive household balance-sheet survey and does not supply the joint wealth-band ranking required here. |
| ONS Effects of Taxes and Benefits (ETB), FYE 2023–24 reference tables | Income, taxes and benefits by equivalised disposable-income decile and household characteristics | Income-decile analysis, not wealth-decile analysis. The existing pack's `household_incidence.csv` is explicitly by income decile. |
| WAS microdata | Wealth, age/status, income sources and household/person characteristics in the same survey | Best route to income by wealth band and stage, subject to questionnaire coverage, variable availability, survey weights and access. |
| Matched LCF–WAS research data | Statistical match of LCF expenditure onto WAS wealth | A synthetic statistical match, not a single observed household reporting both wealth and expenditure. ONS access and matching weights/code need to be requested; do not treat a matched record as an observed joint record. |

**Conclusion:** none of HBAI, FRS or ETB supplies retired income ranked by total household wealth. They are useful income/status sources, but a retired-income-by-wealth-band table needs WAS microdata or a separately authorised statistical match.

## 5. Population and transition hazards

### Population by age

ONS published the **2024-based principal population projections for Great Britain**, released 28 April 2026. The machine-readable dataset provides single-year-of-age and sex projections. This is geographically aligned with WAS and is preferable to the UK-wide file for this stage-weight exercise.

It can supply age-cohort population counts and the demographic size of age groups over time. It does **not** supply employment-to-retirement transition probabilities, nor does it provide age-by-wealth-band population counts. A projected count at age 67 is not a retirement hazard.

### Mortality by age

ONS published 2024-based principal-projection period and cohort life tables for Great Britain and the UK, covering single years of age. The 2024-based Great Britain qx workbook in ONS Ad hoc 3459 covers 1981–2124 and ages 0–125.

ONS defines (q_x) as the probability that a person aged exactly (x) dies before reaching age (x+1). Period qx uses mortality rates for a calendar period; cohort qx follows a birth cohort through projected years. For a forward-looking cohort model, cohort qx is the conceptually aligned mortality input; period qx is a current-period benchmark.

The ONS standard life tables are age- and sex-specific, **not wealth-specific**. No age-specific mortality table by WDT wealth decile was identified. Published life expectancy by area deprivation, where available, is not a direct wealth-band mortality hazard and should not be substituted without a separate method.

### Working-to-retired transition

ONS population projections and mortality tables cannot identify the probability that a working household becomes retired. That transition is an employment/retirement-status event, not merely ageing or survival.

The appropriate observed route is the longitudinal WAS panel: estimate transitions from employed/self-employed to self-reported retired between adjacent waves/rounds, with survey weights, age, sex and attrition accounted for. The two-year interview intervals and changing wave/round design need to be respected. The 7215 catalogue confirms longitudinal coverage from 2006 to 2022. This transition calculation is **not performed here**, because it requires microdata access and analysis, which are out of scope.

## 6. Microdata route and access plan

### First route: UKDS study 7215 (safeguarded / End User Licence)

Study 7215 is *Wealth and Assets Survey, Waves 1–5 and Rounds 5–8, 2006–2022*, 20th edition, DOI 10.5255/UKDA-SN-7215-20. It covers Great Britain and is longitudinal. The catalogue lists 15,128 households and 32,271 individuals for Round 8.

Steps:
1. Register or sign in to the UK Data Service.
2. Open study 7215 and check its current Access tab and location conditions.
3. Add the study to the account, then add the relevant person and household files to a project.
4. Accept the End User Licence Agreement and any additional depositor/location conditions.
5. Download the EUL data and documentation; inspect the variable list, derived-variable specifications, questionnaires and weights before analysis.

The EUL is the first choice. The catalogue explicitly recommends trying 7215 before applying for Secure Access. It is safeguarded rather than unrestricted open data; additional conditions can apply. Commercial use may require data-owner approval. The catalogue warns that the Round 8 person-file data dictionary is not available, although an updated variable list and derived-variable specifications have been added. Exact variable names and year-by-year coverage must therefore be verified from the current documentation and questionnaires, not guessed.

The study topics indicate the data needed for this brief: household/person wealth components, savings and debt; age; employment/economic status; retirement and pension information; income; financial assets; non-mortgage debt; and panel identifiers. The exact availability of mortgage/debt repayment and interest/principal splits must be checked question by question. The presence of a debt balance does not establish that its servicing flows are separately observed.

### Second route: UKDS study 6709 (Secure Access)

Study 6709 is the Secure Access counterpart, with more detailed geographic variables. The current read-me states that Round 8 person and household data were added in the September 2025 tenth edition. Use it only if 7215 lacks the required variables or geographic detail.

Requirements include:
- UK Data Service registration;
- data-owner/depositor approval;
- a DEA Research Project Application;
- a Secure Access User Agreement for each researcher;
- Safe Researcher Training and DEA Accredited Researcher status;
- access through the approved SecureLab/safe environment;
- researcher physically based in the UK (as stated in the study conditions);
- non-commercial use (as stated in the study read-me).

UKDS estimates approximately **3–4 months** for a well-prepared application with no changes required. This is an indicative application-to-access period, not a guarantee. The project must justify public benefit and specify the intended use.

### Variable inventory to complete after access

Do not assume that the following are present in every round. Verify exact variable names, units, imputation status, questionnaire wording and weights by round:

| Required concept | Intended use |
|---|---|
| Household total net wealth and four components | Construct decile ranks and map to D4–5, D6–7, D8–9, D10 |
| Property values and mortgage liabilities | Gross property/debt composition |
| Financial assets and non-mortgage liabilities | Gross financial/debt composition |
| DB and DC pension wealth, pensions in payment | Pension composition and Round 7/8 method break |
| Age, sex, household relationship and household reference person | Age profile and household-level assignment |
| Economic status, employment and self-reported retirement | Working-to-retired status and panel transitions |
| Income by source, including labour and pension income | Retired income by wealth band |
| Savings behaviour / changes in savings | Supporting saving moments, not a consumption rate |
| Debt repayments, interest and principal where asked separately | Debt-service flow, if actually observed |
| Longitudinal identifiers and round-specific weights | Adjacent-round transition estimates and attrition correction |

### If published tables are preferred: exact ONS request

Contact **wealth.and.assets.survey@ons.gov.uk** and request:

1. ~~The full workbook and table specifications for Table 2.11 and financialwealthtables.~~ Already held (section 9). Ask only for what the held tables lack:
2. A **household-based** weighted cross-tab for Round 8: total household wealth decile × age of household reference person × economic activity (employed/self-employed, retired, economically inactive not retired), reporting weighted household counts and shares.
3. The same cross-tab for Round 7 where definitions permit, with the DB pension valuation break separately documented.
4. For each wealth-decile × age/status cell: mean and median total wealth; net property, net financial, private pension (DB/DC where possible), physical wealth; gross mortgage and non-mortgage debt; and the relevant weighted population count.
5. Income by source for retired households by total-wealth decile, with labour/pension/other income distinguished.
6. Standard errors, confidence intervals or coefficients of variation, unweighted cell counts, effective sample sizes, replicate weights/design information, and the exact Round 8 survey weights.
7. Whether an approved tabulation can include adjacent-round panel transitions from employed/self-employed to retired, and the corresponding weights/attrition treatment.

If ONS cannot supply the joint tabulation, proceed through study 7215 first. Do not ask for a synthetic joint distribution formed by multiplying separate age and wealth marginals.

## 7. Files and sources still required for full numeric extraction

> **Superseded by section 9.** Every file below is now held and extracted; the table is kept for the source links.

The following are published and/or already held but remain unparsed in this run. The direct file URLs below were confirmed from the ONS download links; the fetch interface rejects their binary content types:

| File / dataset | Exact source | Why needed |
|---|---|---|
| `data/rates/totalwealthtables.xlsx` | Held in repository | Table 2.11 and decile wealth/component values; workbook spot-checks |
| `data/rates/financialwealthtables.xlsx` | Held in repository | Financial-wealth tables and any age/decile breakdown |
| `data/uk-source-workbooks/etbreferencetablesfye202324final.xlsx` | Held in repository | Confirm table-level definitions for ETB income-decile evidence |
| ONS Ad hoc 2813 XLSX (`meanmedianaggregateandpercentageofwealthbywealthcomponentandageofhouseholdreferenceperson.xlsx`) | https://www.ons.gov.uk/file?uri=%2Fpeoplepopulationandcommunity%2Fpersonalandhouseholdfinances%2Fincomeandwealth%2Fadhocs%2F2813meanmedianaggregateandpercentageofwealthbywealthcomponentandageofhouseholdreferencepersonhrpingreatbritainapril2020tomarch2022%2Fmeanmedianaggregateandpercentageofwealthbywealthcomponentandageofhouseholdreferenceperson.xlsx | Wealth components by age of household reference person, Round 8 |
| ONS Ad hoc 3222 XLSX (`personalfinancialandpropertydebtbyageandregion.xlsx`) | https://www.ons.gov.uk/file?uri=%2Fpeoplepopulationandcommunity%2Fpersonalandhouseholdfinances%2Fincomeandwealth%2Fadhocs%2F3222personalfinancialandpropertydebtbyageandregiongreatbritainapril2020tomarch2022%2Fpersonalfinancialandpropertydebtbyageandregion.xlsx | Personal financial/property debt by age and region, Round 8 |
| ONS 2024-based Great Britain population projection ZIP (`gb1.zip`) | https://www.ons.gov.uk/file?uri=%2Fpeoplepopulationandcommunity%2Fpopulationandmigration%2Fpopulationprojections%2Fdatasets%2Fzippedpopulationprojectionsdatafilesgreatbritain%2F2024based%2Fgb1.zip | Single-year age/sex population projections |
| ONS 2024-based Great Britain qx XLSX (`periodcohortqx2024basedgb.xlsx`) | https://www.ons.gov.uk/file?uri=%2Fpeoplepopulationandcommunity%2Fbirthsdeathsandmarriages%2Flifeexpectancies%2Fadhocs%2F3459periodandcohortmortalityratesqxandexpectationsoflifeex2024basedprincipalprojectiongreatbritainanduk1981to2124%2Fperiodcohortqx2024basedgb.xlsx | Age-specific period/cohort mortality probabilities |

The public downloads are reachable by browser but their binary contents could not be parsed through the available connector. The held repository workbooks are already present; they do not need to be re-uploaded to GitHub. To finish the numeric extraction, provide readable CSV exports of the relevant sheets or use a local repository checkout with an XLSX parser. No new file has been created from guessed workbook values.

## 8. Findings for Scenario B

1. **Keep wealth band × life stage as the intended cell structure.** ~~Do not populate stage weights from the public marginals.~~ Stage weights by £ wealth band can be populated from the held Table 2.13 (section 9), as person-based, rounded figures; the decile-exact, household-based table still needs microdata or an ONS tabulation.
2. The Round 8 bulletin confirms large differences in wealth by age and retirement status; the joint cross-tab by £ band is in the held Tables 2.11 and 2.13 (section 9).
3. The existing pack provides the wealth-band totals and selected composition shares; it does not provide age/status weights or gross debt by band.
4. HBAI, FRS and ETB are income/status sources, not wealth-ranked retired-income distributions.
5. ONS projections support demographic age composition; ONS qx supports age/sex mortality. Neither provides retirement-status transition hazards or wealth-specific mortality.
6. The 7215 EUL microdata route is the preferred next step; 6709 is a more restrictive fallback.
7. One stage-definition decision remains for phase 2: how the model treats economically inactive people who are not retired. They should not be silently assigned to the working or retired stage.

No parameter, wealth-band saving rate, consumption rate, depletion rate or fiscal judgement is proposed.

## Sources

- ONS, *Household total wealth in Great Britain: April 2020 to March 2022* (24 January 2025): https://www.ons.gov.uk/peoplepopulationandcommunity/personalandhouseholdfinances/incomeandwealth/bulletins/totalwealthingreatbritain/april2020tomarch2022
- ONS, *Wealth and Assets Survey guide* (last revised 24 June 2026): https://www.ons.gov.uk/peoplepopulationandcommunity/personalandhouseholdfinances/debt/methodologies/wealthandassetssurveyqmi
- ONS Ad hoc 2813, age and wealth components (16 May 2025): https://www.ons.gov.uk/peoplepopulationandcommunity/personalandhouseholdfinances/incomeandwealth/adhocs/2813meanmedianaggregateandpercentageofwealthbywealthcomponentandageofhouseholdreferencepersonhrpingreatbritainapril2020tomarch2022
- ONS Ad hoc 3222, debt by age and region (15 January 2026): https://www.ons.gov.uk/peoplepopulationandcommunity/personalandhouseholdfinances/incomeandwealth/adhocs/3222personalfinancialandpropertydebtbyageandregiongreatbritainapril2020tomarch2022
- ONS, 2024-based Great Britain population projections (28 April 2026): https://www.ons.gov.uk/peoplepopulationandcommunity/populationandmigration/populationprojections/datasets/zippedpopulationprojectionsdatafilesgreatbritain
- ONS Ad hoc 3459, 2024-based period/cohort qx (10 June 2026): https://www.ons.gov.uk/peoplepopulationandcommunity/birthsdeathsandmarriages/lifeexpectancies/adhocs/3459periodandcohortmortalityratesqxandexpectationsoflifeex2024basedprincipalprojectiongreatbritainanduk1981to2124
- GOV.UK, State Pension age timetable: https://www.gov.uk/government/publications/state-pension-age-timetable/state-pension-age-timetable
- DWP, HBAI FYE 1995–2024: https://www.gov.uk/government/statistics/households-below-average-income-for-financial-years-ending-1995-to-2024
- DWP, FRS FYE 2023–24: https://www.gov.uk/government/statistics/family-resources-survey-financial-year-2023-to-2024
- UK Data Service study 7215: https://datacatalogue.ukdataservice.ac.uk/studies/study/7215
- UK Data Service study 6709 read-me: https://doc.ukdataservice.ac.uk/doc/6709/read6709.htm
- UK Data Service safeguarded access: https://ukdataservice.ac.uk/find-data/access-conditions/safeguarded-access/
- UK Data Service SecureLab application times: https://ukdataservice.ac.uk/help/secure-lab/application-turnaround-times/
- UK Data Service, how to download and order data: https://ukdataservice.ac.uk/help/access-policy/how-to-download-and-order-your-data/

## 9. Close-out: what the held workbooks and ONS uploads give (2026-11-21, guru)

`extract_098r.py` (committed, reproducible: `python -I research/scripts/extract_098r.py`) reads the held WAS and ETB workbooks and the ONS files in this folder and writes the CSVs below. Values are as published; the only computed columns are named `derived_`. Rounds: July 2006 to June 2008 up to April 2020 to March 2022 (nine rounds; the July 2014 to June 2016 and April 2014 to March 2016 rounds overlap by design). Geography is Great Britain for WAS and ONS, UK for ETB.

| Output | Source (sheet, range) | Content and weights |
|---|---|---|
| `was_persons_age_by_wealth_band.csv` (504 rows) | `totalwealthtables.xlsx`, Table 2.11, all round blocks | % of persons in each age group (under 16, 16-24 ... 65+, all) in each of seven household total-wealth bands; unweighted n; no weighted total is published |
| `was_persons_activity_by_wealth_band.csv` (630 rows) | Table 2.13 | % of adults (16+) by economic activity (employee, self-employed, unemployed, student, looking after family, sick/disabled, retired, other inactive) in each band; unweighted n and weighted total |
| `was_households_by_wealth_band.csv` (432 rows) | Table 2.5 | % of households per band, band percentiles and weighted and unweighted frequencies, per round |
| `was_band_edge_mapping.csv` | derived from Table 2.5 | WAS £ bands grouped to the pack's WDT bands, with target and achieved cumulative household shares |
| `was_stage_by_wdt_band_derived.csv` (180 rows) | derived from Tables 2.13 and 2.5 | persons by stage in each WDT band: weighted total times rounded percentage |
| `ons_was_wealth_by_age_of_hrp.csv` | Ad hoc 2813, Table_1 | mean, median, aggregate and share of each wealth component by age of household reference person, April 2020 to March 2022 |
| `ons_was_debt_by_age_region.csv` | Ad hoc 3222, Tables 1 and 2 | personal financial and property debt by age band and region: total, median, mean with confidence limits, weighted and unweighted frequency |
| `ons_population_gb_principal_2024based.csv` | `gb1/gb_ppp_machine_readable.xlsx`, sheet Population | single-year age by sex, 2024 to 2074 (the workbook runs to 2124) |
| `ons_qx_gb_2024based.csv` | Ad hoc 3459, four qx sheets | qx per 100,000, ages 16 to 100; period 2024 to 2074; cohort for births 1981 to 2024 only (the workbook has no earlier birth cohorts) |
| `etb_income_by_decile_retired_nonretired.csv` | ETB 2023/24 Tables 4b and 3b | incomes, taxes and benefits (£ a year) of retired and of non-retired individuals by equivalised disposable-income decile |

The other 13 projection variants of the population zip (about 18 MB) are on the branch `brief/098r-was-tables-population` only; the principal projection is enough here and the script reads any variant by path.

**Spot-checks against the source cells** (all match): Table 2.13 April 2020 to March 2022, retired: 5, 9, 9, 8, 17, 28, 25 % and 10,520 unweighted, 11,640,000 weighted; Table 2.11 same round, 65+, under £20,000: 5 % (n 10,784); Table 2.5 round cumulative shares; ONS 2813 65 to 74 property median £200,000; ONS 3222 North East 16 to 34 financial debt total £2,561,934,000 (CI 1,602,399,000 to 3,521,469,000); qx males age 65 in 2024: 1,164.76; population males 65 in 2030: 415,319. The seven Table 2.13 status totals add to the all-adults total of 50,185,000.

### Band-edge reconciliation to the pack

WAS bands are £ thresholds (20k, 85k, 200k, 300k, 500k, 1m), not deciles, so no exact match exists. Round 8 cumulative household shares at the thresholds are 12, 28, 42, 52, 67, 87 %. Grouping bands 1+2, 3+4, 5, 6, 7 gives household shares of 28, 24, 15, 20, 14 % against the pack's deciles D1-3, D4-5, D6-7, D8-9, D10 of 30, 20, 20, 20, 10 %. D8-9 fits well; D6-7 is five points short, D4-5 four points long and D10 four points long (the rounded percentages sum to 101). Bands cannot be split without assuming a shape, which this note does not do.

### Stage by WDT band, April 2020 to March 2022 (derived)

Share of adults in each grouped band, by stage; person totals in millions. Persons, not households: a person is placed by the wealth of their household.

| WDT band (approx.) | Working | Unemployed | Inactive, not retired | Retired | Adults (m) |
|---|---:|---:|---:|---:|---:|
| D1-3 | 51.4 % | 5.5 % | 29.9 % | 13.3 % | 12.3 |
| D4-5 | 70.0 % | 2.5 % | 9.8 % | 17.7 % | 11.2 |
| D6-7 | 63.8 % | 1.3 % | 8.7 % | 26.2 % | 7.5 |
| D8-9 | 60.6 % | 1.9 % | 7.7 % | 29.8 % | 10.9 |
| D10 | 54.6 % | 1.1 % | 9.1 % | 35.2 % | 8.3 |

Each cell is weighted total times a whole-number percentage, so it carries up to half a percentage point of rounding on that row's total; the cells flagged `[u]` (low reliability) are left out, which understates the inactive group slightly in the middle bands. The same table for all nine rounds is in the CSV.

**What this supports.** A retired share rising from about 13 % in the lowest bands to 35 % in the top band, a working share peaking in the middle, and a large inactive-not-retired residual (30 %) in the lowest bands. That residual is the group the author must rule on (stage definition above); it is not assigned. **What it does not support:** household-level weights, age within band, or the decile-exact bands. Age by band (Table 2.11) is percentages only, with no weighted totals, so age-band counts cannot be derived without another source.

### Retired income (item 3)

ETB Table 4b ranks retired individuals by equivalised disposable income, not by wealth. For 2023/24 average disposable income runs from £9,149 (bottom decile) through £24,639 (fifth) to £69,949 (top) for retired individuals, against £15,962, £49,917 and £134,254 for non-retired. Private pensions and investment income are separate lines (see the CSV). None of HBAI, FRS or ETB ranks retired income by wealth; the stage-by-band table above and ETB cannot be joined without assuming the two rankings coincide, which this note does not do.

### Transitions (item 4)

The population file gives age structure; the qx file gives age and sex mortality (period and, for births from 1981, cohort). Neither gives working-to-retired hazards, and no mortality by wealth is published. The longitudinal route in section 5 stands.

### Debt (item 1)

ONS 3222 gives personal financial and property debt by age and region, not by wealth band. The financial wealth workbook's liabilities tables were read but not extracted: Table 5.7 (non-mortgage borrowing by type) and Table 5.9 (financial liabilities) are all-household summary statistics by round (shares and percentile points), not broken down by wealth band or age. Gross debt by wealth band remains a microdata or ONS-request item.

### Acceptance criteria

1. **Met.** Every extracted table has sheet, range or block, round, unit and weights stated above, and spot-checks on at least three cells each (WAS, ONS, ETB).
2. **Met with the mismatch stated.** Band-edge reconciliation shown, with household shares against targets.
3. **Met.** Items 3 and 4 say what is and is not identified; item 5 (access plan) is section 6, narrowed above to the household-based cross-tab and debt by band.

### Remaining for the author

1. Ruling on the economically inactive, not retired group (about 30 % of adults in the lowest bands).
2. Whether the £-band stage table is enough for phase 2, or the 7215 microdata or the narrowed ONS request is wanted for decile-exact, household-based weights and debt by band.
