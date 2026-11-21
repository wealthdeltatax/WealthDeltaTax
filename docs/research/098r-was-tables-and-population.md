# 098r — WAS published tables, ages and the working-to-retired transition

**Date:** 2026-11-21  
**Branch:** `brief/098r-was-tables-population`  
**Scope:** published-table extraction, source audit and access plan. No microdata analysis, parameter choice, or pack/code change.

## Outcome

The public evidence supports a useful **age/status profile** and confirms that the WAS panel can in principle supply the joint wealth-by-stage information needed for Scenario B. It does **not** provide the required stage weights by WDT wealth band in the published HTML tables. The public Round 8 bulletin gives marginal age and retirement-status summaries; the held workbook files and additional ONS XLSX files are binary and could not be decoded with the repository connector available in this run.

The most important finding is therefore a boundary, not a rate: **age and retirement status are associated with wealth, but the published marginals cannot be combined into a wealth-band × life-stage distribution.** The joint cross-tab requires WAS microdata (study 7215) or a bespoke ONS tabulation.

No household-level records were extracted. No saving, consumption, drawdown, or mortality rate by wealth band has been inferred.

## 1. Held workbooks and extraction status

| File | Status | What is known / what remains |
|---|---|---|
| `Rates Data/totalwealthtables.xlsx` | **Held; binary not parseable here** | The pack builder reads Table 2.2 for wealth decile totals and components. The brief also points to Table 2.11 for age. I could not inspect sheet names, ranges, or Table 2.11 cells in this run, so no workbook spot-checks are claimed. |
| `Rates Data/financialwealthtables.xlsx` | **Held; binary not parseable here** | The workbook is present in the repository, but no sheet/range/round inventory or cell values could be verified. |
| `Research/etbreferencetablesfye202324final.xlsx` | **Held; binary not parseable here** | The existing pack build uses ONS Effects of Taxes and Benefits tables 2b, 2c and 16 for income-decile incidence. It is not a wealth-ranked source. |
| ONS Ad hoc 2813, wealth components by age of household reference person | **Published; XLSX reachable, not parsed** | A specific ONS table exists for mean, median, aggregate and percentage of wealth by component and age of household reference person, Great Britain, April 2020 to March 2022. |
| ONS Ad hoc 3222, personal debt by age and region | **Published; XLSX reachable, not parsed** | A specific ONS table exists for personal financial and property debt by age and region, Great Britain, April 2020 to March 2022. It is by age/region, not by total-wealth decile. |

The GitHub connector returns the held XLSX files as base64 binary payloads. The available execution environment has no ZIP/XLSX decoder or local repository checkout, so the acceptance test requiring sheet/range metadata and three workbook cell spot-checks could not be completed. This is a tooling limitation, not evidence that the files are corrupt or absent.

### What the held pack already establishes

`model_v3/pack/GBR/wealth_distribution.csv` is readable. It contains Round 8 household wealth totals by decile, household counts, and selected component shares. The pack builder documents that the totals and components are derived from `Rates Data/totalwealthtables.xlsx`, Table 2.2, and the all-household total from Table 2.1.

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

No public table located in this review supplies the **joint weighted household counts** for wealth decile × age group × retirement/economic-activity status. Separate age and wealth marginals cannot be multiplied or otherwise combined to manufacture that joint distribution. In particular:

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

1. The full workbook and table specifications for totalwealthtables Table 2.11 and financialwealthtables, including sheet names, table ranges, rounds, definitions, units, weights and suppression rules.
2. A weighted cross-tab for Round 8: total household wealth decile × age of household reference person × economic activity (employed/self-employed, retired, economically inactive not retired), reporting weighted household counts and shares.
3. The same cross-tab for Round 7 where definitions permit, with the DB pension valuation break separately documented.
4. For each wealth-decile × age/status cell: mean and median total wealth; net property, net financial, private pension (DB/DC where possible), physical wealth; gross mortgage and non-mortgage debt; and the relevant weighted population count.
5. Income by source for retired households by total-wealth decile, with labour/pension/other income distinguished.
6. Standard errors, confidence intervals or coefficients of variation, unweighted cell counts, effective sample sizes, replicate weights/design information, and the exact Round 8 survey weights.
7. Whether an approved tabulation can include adjacent-round panel transitions from employed/self-employed to retired, and the corresponding weights/attrition treatment.

If ONS cannot supply the joint tabulation, proceed through study 7215 first. Do not ask for a synthetic joint distribution formed by multiplying separate age and wealth marginals.

## 7. Files and sources still required for full numeric extraction

The following are published and/or already held but remain unparsed in this run. The direct file URLs below were confirmed from the ONS download links; the fetch interface rejects their binary content types:

| File / dataset | Exact source | Why needed |
|---|---|---|
| `Rates Data/totalwealthtables.xlsx` | Held in repository | Table 2.11 and decile wealth/component values; workbook spot-checks |
| `Rates Data/financialwealthtables.xlsx` | Held in repository | Financial-wealth tables and any age/decile breakdown |
| `Research/etbreferencetablesfye202324final.xlsx` | Held in repository | Confirm table-level definitions for ETB income-decile evidence |
| ONS Ad hoc 2813 XLSX (`meanmedianaggregateandpercentageofwealthbywealthcomponentandageofhouseholdreferenceperson.xlsx`) | https://www.ons.gov.uk/file?uri=%2Fpeoplepopulationandcommunity%2Fpersonalandhouseholdfinances%2Fincomeandwealth%2Fadhocs%2F2813meanmedianaggregateandpercentageofwealthbywealthcomponentandageofhouseholdreferencepersonhrpingreatbritainapril2020tomarch2022%2Fmeanmedianaggregateandpercentageofwealthbywealthcomponentandageofhouseholdreferenceperson.xlsx | Wealth components by age of household reference person, Round 8 |
| ONS Ad hoc 3222 XLSX (`personalfinancialandpropertydebtbyageandregion.xlsx`) | https://www.ons.gov.uk/file?uri=%2Fpeoplepopulationandcommunity%2Fpersonalandhouseholdfinances%2Fincomeandwealth%2Fadhocs%2F3222personalfinancialandpropertydebtbyageandregiongreatbritainapril2020tomarch2022%2Fpersonalfinancialandpropertydebtbyageandregion.xlsx | Personal financial/property debt by age and region, Round 8 |
| ONS 2024-based Great Britain population projection ZIP (`gb1.zip`) | https://www.ons.gov.uk/file?uri=%2Fpeoplepopulationandcommunity%2Fpopulationandmigration%2Fpopulationprojections%2Fdatasets%2Fzippedpopulationprojectionsdatafilesgreatbritain%2F2024based%2Fgb1.zip | Single-year age/sex population projections |
| ONS 2024-based Great Britain qx XLSX (`periodcohortqx2024basedgb.xlsx`) | https://www.ons.gov.uk/file?uri=%2Fpeoplepopulationandcommunity%2Fbirthsdeathsandmarriages%2Flifeexpectancies%2Fadhocs%2F3459periodandcohortmortalityratesqxandexpectationsoflifeex2024basedprincipalprojectiongreatbritainanduk1981to2124%2Fperiodcohortqx2024basedgb.xlsx | Age-specific period/cohort mortality probabilities |

The public downloads are reachable by browser but their binary contents could not be parsed through the available connector. The held repository workbooks are already present; they do not need to be re-uploaded to GitHub. To finish the numeric extraction, provide readable CSV exports of the relevant sheets or use a local repository checkout with an XLSX parser. No new file has been created from guessed workbook values.

## 8. Findings for Scenario B

1. **Keep wealth band × life stage as the intended cell structure**, but do not populate stage weights from the public marginals.
2. The Round 8 bulletin confirms large differences in wealth by age and retirement status, but not the joint cross-tab.
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
