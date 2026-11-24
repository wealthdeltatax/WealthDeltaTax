# 095r addendum: Source acquisition and verification register for UK household flows

- **Date checked:** 2026-11-21
- **Parent:** `research/notes/095r-uk-household-flow-evidence-map.md`
- **Purpose:** resolve the nine acquisition and verification requests in 095r section 5 and section 8. This is a source register and verification note, not a calibrated model input.
- **Scope:** public sources were located and their published descriptions/figures checked. Controlled microdata were not accessed. Binary XLSX/ODS/PDF files are linked at their official repositories; this repository note does not contain copies of those binaries.
- **Decision:** no consumption/depletion parameter is inferred or changed.

## Executive result

The open-data route is now substantially clearer:

- **Request 3 (ONS sector accounts):** current official quarterly sector accounts and UK Economic Accounts datasets located. The ONS spreadsheet link itself is not parseable by the web research interface (unsupported XLSX content type), so no D41/D42/D44/D45 series values are claimed as extracted.
- **Request 4 (BoE/NMG):** Bank of England publishes downloadable NMG survey microdata for 2004–2011 and 2011–2026, plus Stata example code. This is materially better than relying only on the 2018 article. The raw files have not been downloaded or analysed here.
- **Request 5 (Bozio et al. 2013):** the IFS publication page is now located and confirms the paper's main result. The full PDF remains inaccessible through this research interface; RePEc gives a direct publisher PDF URL.
- **Request 6 (HMRC):** current CGT, IHT, Personal Incomes and Property Rental Income releases located. They provide useful realised gains, estate and income distributions, but none is a direct measure of accrued gains or retained property income by wealth decile.
- **Requests 1 and 2 (WAS):** UK Data Service study **7215** contains Waves 1–5 and Rounds 5–8 (2006–2022), including Round 7 and Round 8 person and household files. It is listed as safeguarded/EUL access, not simply as a generic special-licence dataset. A more detailed Secure Access counterpart is study **6709**. These are the main route to the panel and composition work.
- **Request 7 (ELSA):** Wave 11 is available; the standard UKDS series and special/secure variants are identifiable. The primary data are England, age 50+, so they complement rather than replace WAS.
- **Request 8 (matched LCF–WAS):** ONS confirms the published matched dataset is made by statistical matching LCF expenditure to WAS wealth. No separately downloadable matched microdata product was verified. Treat microdata access as an ONS/SRS enquiry, not an assumed public dataset.
- **Request 9:** all five items have been checked or qualified below.

## 1. WAS wealth composition and longitudinal panel (requests 1 and 2)

### Primary data catalogue records

- **UK Data Service study 7215:** [Wealth and Assets Survey, Waves 1–5 and Rounds 5–8, 2006–2022](https://datacatalogue.ukdataservice.ac.uk/studies/study/7215)
  - Study number: 7215; DOI: [10.5255/UKDA-SN-7215-20](https://doi.org/10.5255/UKDA-SN-7215-20).
  - Latest catalogue edition located: 20th edition, October 2026.
  - Contains Round 7 and Round 8 person and household files, plus earlier waves/rounds, and is longitudinal/panel data.
  - Catalogue access classification: **safeguarded**; EUL access. The catalogue says users should consider study 6709 if they need the more detailed geographic variables available under Secure Access.
  - The catalogue notes an ONS warning about a small number of Round 7 outliers affecting detailed pension-wealth breakdowns within the wealthiest decile. Medians and headline total wealth are stated to be unaffected, but fine pension-tail estimates need caution.
- **Secure Access counterpart:** [UKDS study 6709](https://datacatalogue.ukdataservice.ac.uk/studies/study/6709), [read-me/documentation](https://doc.ukdataservice.ac.uk/doc/6709/read6709.htm). The current catalogue description says Secure Access and requires depositor approval, DEA research application, Safe Researcher training/accreditation and UK-based access.
- **ONS WAS methodology and access guide:** [Wealth and Assets Survey guide](https://www.ons.gov.uk/peoplepopulationandcommunity/personalandhouseholdfinances/debt/methodologies/wealthandassetssurveyqmi).
  - Confirms WAS is biennial and Great Britain, with microdata covering wealth, assets, savings and debt.
  - Round 8 DB pension valuation uses SCAPE-based assumptions, introducing a discontinuity between Round 7 and Round 8.
  - The survey excludes state pension entitlement and does not capture all offshore holdings/trust structures/business assets in its headline wealth measure.
- **ONS published pension-decile table:** [Saving for retirement in Great Britain, April 2018 to March 2020](https://www.ons.gov.uk/peoplepopulationandcommunity/personalandhouseholdfinances/incomeandwealth/bulletins/pensionwealthingreatbritain/april2018tomarch2020). It confirms the top decile by private-pension wealth held 64% of private pension wealth; the bottom five deciles held less than 1%. This is a published distributional result, but it is not the requested multi-component wealth-band table for Rounds 7 and 8.
- **ONS decile composition xlsx:** the 095r note's inaccessible ONS spreadsheet is not replaced by a guessed link. Request the exact table from the WAS team if it cannot be retrieved from the bulletin's data links.

### What can be done with it

Study 7215 is the first dataset to try for the top-decile panel decomposition. It has Rounds 7 and 8 and a longitudinal history, subject to access conditions. First test whether the EUL files contain the necessary asset values and identifiers to construct a reliable passive/active split; only then apply for Secure Access if variables or detail are insufficient.

For the component table, derive weighted deciles from the microdata separately for each round, and report property, financial, DB pension, DC pension and debt components on consistent definitions. Do not mechanically compare DB pension wealth across R7/R8 without a SCAPE break adjustment or a separate sensitivity analysis.

## 2. ONS sector accounts and property income (request 3)

Official data entry points:

- [Quarterly sector accounts dataset](https://www.ons.gov.uk/economy/nationalaccounts/uksectoraccounts/datasets/quarterlysectoraccounts) — latest dataset edition located: Q2 2026; historical spreadsheets include Q4 2025 and earlier.
- [UK Economic Accounts dataset](https://www.ons.gov.uk/economy/nationalaccounts/uksectoraccounts/datasets/ukeconomicaccounts) — broader integrated national accounts workbook, latest edition Q2 2026.
- [UK National Balance Sheet time series](https://www.ons.gov.uk/economy/nationalaccounts/uksectoraccounts/datasets/nationalbalancesheet) — downloadable CSV/XLSX/structured text, latest release 10 June 2026.
- ONS sector accounts contact: **sector.accounts@ons.gov.uk**.

The requested S.14 items are the correct national-accounts concepts to retrieve:
- D41: interest;
- D42: distributed income of corporations;
- D44: investment income attributable to insurance policyholders and pension entitlements;
- D45: rent.

Retrieve both **resources/received** and **uses/paid** where published, and identify the S.14 household-sector row rather than mixing it with S.15 NPISH or the consolidated household-and-NPISH sector. D44 is not disposable cash yield that can simply be added to household cash income; it is linked to insurance and pension entitlements and requires consistent pension-account treatment.

**Acquisition limitation:** ONS dataset pages and spreadsheet editions were located, but the XLSX download endpoint returned an unsupported spreadsheet content type to the research interface. No series values are represented here as extracted. The next analyst should download the QSA/UKEA spreadsheets directly and record the table, series identifier, unit, seasonal adjustment, time coverage and sign convention for each code.

HMRC's [Personal Incomes Statistics 2023–24](https://www.gov.uk/government/statistics/personal-incomes-statistics-for-the-tax-year-2023-to-2024) is a complementary distributional source, not a substitute for S.14. It provides income by property, bank/building-society interest and dividends by total-income range. In 2023–24, the combined property/interest/dividend/other income total was £125bn; bank/building-society interest was £18.3bn. The sample is based on taxpayers/individuals potentially liable to Income Tax, so it omits or under-represents non-taxpayers and income outside the relevant tax reporting scope.

## 3. Bank of England NMG survey (request 4)

- [Bank of England research datasets](https://www.bankofengland.co.uk/statistics/research-datasets) publishes:
  - [NMG survey data 2004–2011](https://www.bankofengland.co.uk/-/media/boe/files/statistics/research-datasets/boe-nmg-household-survey-data-2004-11.xlsx) (XLSX, 7 MB);
  - [NMG survey data 2011–2026](https://www.bankofengland.co.uk/-/media/boe/files/statistics/research-datasets/boe-nmg-household-survey-data.xlsx) (XLSX, 71 MB);
  - [supporting Stata code](https://www.bankofengland.co.uk/-/media/boe/files/statistics/research-datasets/household-incomes-and-deciles-stata-file.do) (DO-file).
- The Bank says this annual survey asks households about income and spending. The example Stata code creates household income variables and income deciles.
- [2018 NMG article](https://www.bankofengland.co.uk/quarterly-bulletin/2018/2018-q4/the-financial-position-of-british-households-evidence-from-the-2018-nmg-consulting-survey) remains useful contextual documentation. Its published charts show behaviour by gross financial wealth decile and DTI/DSR group. For example, the chart on spending changes explicitly excludes savings and debt repayment from spending, which is conceptually useful when separating consumption from saving and loan repayment.

The raw NMG files are a high-value public acquisition. The next step is to inspect codebooks/questionnaires and variables for:
- household saving / change in savings;
- income and age;
- debt outstanding;
- mortgage and unsecured debt repayments;
- interest payments versus principal repayments, if separately observed;
- gross financial wealth.

Do not assume every variable is observed for every survey year or that a survey-reported saving measure is identical to national-accounts saving.

## 4. Bozio, Emmerson, O'Dea and Tetlow (2013) (request 5)

- IFS publication page: [Savings and wealth of the lifetime rich: evidence from the UK and US](https://ifs.org.uk/publications/savings-and-wealth-lifetime-rich-evidence-uk-and-us).
- RePEc record: [IFS Working Paper W13/30](https://ideas.repec.org/p/ifs/ifsewp/13-30.html).
- Direct publisher PDF URL recorded by RePEc: [wp201330.pdf](https://www.ifs.org.uk/wps/wp201330.pdf).

The IFS publication page confirms that the study combines individual survey wealth holdings with administrative earnings histories and finds a positive relationship between saving rates/wealth accumulation and permanent income. This supports heterogeneity by lifetime income, but the abstract does not provide the numerical gradients needed for calibration.

**Full-text status:** direct PDF URL is known, but the PDF could not be retrieved by the web research interface. The paper is not treated as fully read. If a local copy is available, add it to the project and extract the tables/results before using numerical claims.

## 5. HMRC sources (request 6)

### Capital gains

- [Capital Gains Tax statistics](https://www.gov.uk/government/statistics/capital-gains-tax-statistics), updated 27 August 2026.
- [Latest commentary](https://www.gov.uk/government/statistics/capital-gains-tax-statistics/capital-gains-tax-commentary--2).
- [Background quality report](https://www.gov.uk/government/statistics/background-quality-report-capital-gains-tax-cgt-statistics/background-quality-report-capital-gains-tax-statistics--2).

Useful current facts:
- 2024–25 realised gains reported: £127.3bn; 584,000 taxpayers.
- 45% of CGT liabilities came from individuals/trusts with gains of £5m or more, a group representing less than 1% of CGT taxpayers.
- 2024–25, 52% of gains for CGT-liable individuals came from the 17% with taxable income above £125,140.
- These are **realised, taxable/reportable gains**, not accrued gains on the entire wealth stock. The statistics cover CGT-liable taxpayers, not all households or all asset appreciation.

### Inheritance and estates

- [Inheritance Tax liabilities statistics](https://www.gov.uk/government/statistics/inheritance-tax-liabilities-statistics).
- [Latest commentary](https://www.gov.uk/government/statistics/inheritance-tax-liabilities-statistics/inheritance-tax-liabilities-statistics-commentary).

For 2023–24, 4.72% of UK deaths (30,400 estates) resulted in an IHT charge; liabilities were £7.03bn. The tables include estate composition, net-estate ranges, exemptions and reliefs. These cover estates passing on death and do not measure all lifetime gifts or transfers between households. The taxpaying-estate sample is not representative of all household transfers.

### Property income and interest/dividends

- [Property rental income statistics 2026](https://www.gov.uk/government/statistics/property-rental-income-statistics/property-rental-income-statistics-2026).
- [Personal Incomes Statistics 2023–24](https://www.gov.uk/government/statistics/personal-incomes-statistics-for-the-tax-year-2023-to-2024), especially Tables 3.5–3.7 and the ODS files.

HMRC property-rental data report £58.99bn of rental income declared by unincorporated landlords in 2024–25, of which £49.81bn was declared by individuals. It excludes incorporated landlords and taxpayers not required to file or declare the income. It is gross declared rental income, not net rental yield and not the amount retained after consumption.

Personal Incomes Table 3.7 breaks property, bank interest, dividends and other income down by total-income range. It is useful for income-distribution analysis but not wealth-decile analysis and does not identify the fraction retained.

## 6. ELSA housing and pension wealth (request 7)

- [ELSA access page](https://www.elsa-project.ac.uk/accessing-elsa-data).
- [ELSA data and documentation](https://www.elsa-project.ac.uk/data-and-documentation).
- [Wave reports and tables](https://www.elsa-project.ac.uk/wave-reports-and-tables).
- Standard UKDS latest-wave record: [English Longitudinal Study of Ageing: Waves 1–11, 2002–2024, study 5050](https://datacatalogue.ukdataservice.ac.uk/studies/study/5050).
- A 2026 special-licence record surfaced for Waves 4–11: [UKDS study 8346](https://datacatalogue.ukdataservice.ac.uk/studies/study/8346).

ELSA Wave 11 fieldwork took place October 2023–October 2024; Wave 11 data are now available. It provides longitudinal data on people aged 50+ in England, including wealth, housing, pensions, income and retirement. It is the right extension to test whether financial-wealth drawdown is accompanied by housing or pension drawdown, but it cannot identify working-age household drawdown and is not a UK-wide sample.

## 7. ONS matched LCF–WAS data (request 8)

- [ONS matched income, spending and wealth article](https://www.ons.gov.uk/peoplepopulationandcommunity/personalandhouseholdfinances/incomeandwealth/articles/incomespendingandwealthhowdoyoucompare/2022-03-09).
- [ONS LCF quality/methodology guide](https://www.ons.gov.uk/peoplepopulationandcommunity/personalandhouseholdfinances/incomeandwealth/methodologies/livingcostsandfoodsurveyqmi).
- [ONS Secure Research Service](https://www.ons.gov.uk/aboutus/whatwedo/statistics/requestingstatistics/secureresearchservice/aboutthesecureresearchservice).

ONS confirms that the published matched dataset is constructed by statistically matching LCF income/spending data onto WAS wealth data. It is an experimental statistical match, not a single survey in which the same household reported all three. LCF microdata are available through UKDS and SRS; WAS microdata are separately available through UKDS/SRS subject to their own access conditions.

No independently downloadable, already-matched household-level LCF–WAS microdata product was verified. Ask ONS whether the matched analytical file and matching weights/code can be supplied within SRS. If not, reproduce the statistical match under a defensible documented procedure; do not treat a matched synthetic record as an observed joint record.

## 8. Verification pass on the five carried figures (request 9)

| Claim carried in 095r | Verification result | Correct interpretation / caveat |
|---|---|---|
| 2017 saving gap: cash basis −0.8%, national-accounts basis 4.1% | **Confirmed** by ONS's 4 July 2018 article. | These are two different accounting presentations. Cash basis removes imputed transactions including imputed rent, pension-entitlement adjustment and FISIM. The national-accounts measure includes them. This is not a simple correction from a wrong figure; the measures answer different questions. |
| 92% of realised gains to top 1% | **Confirmed**, but source attribution and ranking need correction. | The 92% result is from Advani, Bangham and Summers, *Capital Gains and UK Inequality* (2020), for 2018 gains ranked by **total remuneration**, not wealth and not ordinary taxable income. The same paper reports 47% when ranked by income alone. It is not an HMRC wealth-decile statistic. [Working paper PDF](https://warwick.ac.uk/fac/soc/economics/research/centres/cage/manage/publications/wp465.2020.pdf). |
| 64% of private pension wealth held by top decile | **Confirmed** by ONS. | The ONS bulletin says the top decile held 64% and the bottom five deciles less than 1%, April 2018–March 2020. This is the decile ranking by private pension wealth for the relevant pension-wealth distribution, not a measure of all household wealth held by the top total-wealth decile. Round 7 outlier caveat and Round 8 SCAPE break matter for longitudinal comparison. |
| Pension-offset range: OBR 7% against Resolution Foundation 34% additionality (66p offset) | **Both headline calculations located, but not a like-for-like range.** | OBR's 7% is its 2009 decomposition of employee and employer pension contributions, describing only around £5bn of direct employee payments relative to roughly £35bn interest/dividends accrued on existing pension assets plus £48bn employer contributions. It is not a general causal estimate that only 7% of every new pension contribution is additional household saving. RF's 66p is the amount of each £1 of *higher auto-enrolment contributions* funded by less other saving or more debt when default rates rose in 2018–19. The arithmetic residual is 34p, but this is a specific policy-change estimate and "less saving or more debt" combines two different balance-sheet effects. Do not present 7–34% as a common confidence interval. |
| State pension treatment: WAS against national accounts | **Corrected: neither includes the accrued value of the unfunded State Pension as household net wealth in its headline balance sheet.** | ONS says WAS excludes State Pension entitlement and reflects it through tax/NI paid while working and pension income received in retirement. ONS also says the State Pension is an unfunded social-security benefit and is not recorded as a liability in UK National Accounts/public-sector net debt/net worth. It is therefore wrong to say national-accounts household wealth includes the State Pension liability while WAS excludes it. [ONS WAS FOI explanation](https://www.ons.gov.uk/aboutus/transparencyandgovernance/freedomofinformationfoi/wealthdistributionstatistics); [ONS wider public-sector debt discussion](https://www.ons.gov.uk/economy/governmentpublicsectorandtaxes/publicsectorfinance/articles/widermeasuresofpublicsectornetdebt/latest). |

## 9. Priority order for actual acquisition and analysis

1. **Download and inspect BoE NMG 2011–2026 plus its Stata code.** This is public and directly useful for income/age saving and debt behaviour.
2. **Use UKDS study 7215 (WAS EUL) first.** Establish whether R7/R8 panel variables and asset composition are sufficient for passive/active wealth-change decomposition. Apply for study 6709 only if EUL detail is insufficient.
3. **Download ONS QSA and UK Economic Accounts spreadsheets.** Extract S.14 D41, D42, D44, D45 received/paid with units and series IDs. This is the remaining major open-data task for property-income levels.
4. **Use HMRC Personal Incomes Table 3.7 and Property Rental Income tables** to understand property/interest/dividend income by taxable-income bracket, while preserving the distinction from wealth distribution and net retained income.
5. **Download ELSA Wave 11** if housing/pension drawdown beyond financial assets is required.
6. **Request ONS/SRS matched LCF–WAS access only if the matched joint distribution is essential.** The published experimental match does not itself prove a microdata release is available.
7. **Read the full Bozio paper** from a local PDF or IFS mirror before quoting numerical gradients.

## 10. Implications for 096r and the WDT model

- The strongest new acquisition is the public NMG raw survey data and the current WAS panel catalogue entry. They move requests 2 and 4 from vague leads to concrete, actionable datasets.
- The 64% pension concentration and 92% realised-gain concentration figures are not measures of net saving or wealth depletion. They describe distribution/concentration, with different rankings and populations.
- The 7% OBR and 66p RF pension figures must remain distinct; they concern different mechanisms and periods.
- State Pension should be treated as an income stream/exogenous social-security entitlement in a household wealth model unless WDT deliberately expands its boundary to include an imputed actuarial value. It is not a marketable household asset in WAS or a recognised household balance-sheet asset in national accounts.
- No result in this source pass identifies a universal or band-specific consumption/depletion percentage. The 3.5% remains abandoned as the preferred assumption.
