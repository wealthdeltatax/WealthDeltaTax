# 097r — Open UK series collection

**Date:** 2026-11-21  
**Branch:** `brief/097r-open-series-collection`  
**Scope:** data acquisition and mechanical identity/unit checks only. No model parameters, wealth-band consumption rates, depletion assumptions or fiscal interpretation are introduced.

## Outcome

A useful part of the open series has been extracted from official ONS and HMRC HTML time-series/commentary pages. The larger ONS, Bank of England and HMRC spreadsheet downloads are published and linked, but the retrieval interface rejects their file content-types. Those files are recorded below for author upload rather than replaced by guesses or summaries.

New data files:

| File | Contents |
|---|---|
| `data/097r/ons_household_flows_annual.csv` | Annual ONS S.14 D.41 received/paid, D.42 received, D.45 received/paid, D.8, B.6g and saving ratio. 1997 onward where available. |
| `data/097r/ons_household_consumption_annual.csv` | Annual S.14 individual consumption expenditure (P.31), 1997–2025. |
| `data/097r/ons_household_saving_identity_check.csv` | Source series and derived gross-saving/saving-ratio reconciliation, 1997–2025. |
| `data/097r/ons_nbs_financial_annual.csv` | S.14 total financial assets, financial liabilities and net financial assets, 1997–2025. |
| `data/097r/hmrc_html_summary_extracts.csv` | Numeric summary extracts available in HMRC HTML commentary. Not a substitute for the underlying ODS tables. |

All extracted-series CSVs use the brief's required metadata: series/table, period, value, unit, price basis, seasonal adjustment, sector, sign convention, source link, retrieval date and one-line definition. The saving-identity file additionally identifies derived rows and their component source links.

## 1. ONS sector accounts and UK Economic Accounts

| Item / series | Status | Coverage and notes |
|---|---|---|
| S.14 D.41 interest received — HAXV | **Extracted** | Annual 1997–2025, £m, current prices, NSA. |
| S.14 D.41 interest paid — HACY | **Extracted** | Annual 1997–2025, £m, current prices, NSA. |
| S.14 D.42 distributed income of corporations received — HAXW | **Extracted** | Annual 1997–2024, £m, current prices, NSA. The extracted series is from the Blue Book 2025 vintage; 2025 is not present in that page. |
| S.14 D.42 paid | **Reachable but not parseable** | Not extracted separately. The current Quarterly Sector Accounts workbook is published as XLSX; its rows could not be read. |
| S.14 D.44 received and paid | **Reachable but not parseable** | No separate readable series table obtained. Included in the sector-account workbook, which could not be parsed. |
| S.14 D.45 rent received — M8MD | **Extracted** | Annual 1997–2024, £m, current prices, NSA; Blue Book 2025 vintage. |
| S.14 D.45 rent paid — RNMS | **Extracted** | Annual 1997–2025, £m, current prices, SA. |
| S.14 D.8 pension-entitlement adjustment — RNMB | **Extracted** | Annual 1997–2025, £m, current prices, SA. |
| S.14 gross disposable income B.6g — RPHA | **Extracted** | Annual 1997–2025, £m, current prices, SA. |
| S.14 saving ratio — DG5H | **Extracted** | Annual 1997–2025, percent, current-price measure, NSA. |
| S.14 individual consumption expenditure P.31 — ABPB | **Extracted** | Annual 1997–2025, £m, current prices, NSA. |
| Gross saving B.8g | **Derived for identity check** | Calculated as B.6g + D.8 − P.31. This is an arithmetic reconciliation, not an additional ONS series extraction. |
| Quarterly series | **Partially accessible / not collected here** | Individual ONS time-series pages expose quarterly observations for some series. This brief's CSVs contain annual values only; the current QSA workbook remains unparsed. |
| Other changes in volume and revaluation flows | **Reachable but not parseable** | Not extracted from the workbook. No flow or revaluation values are imputed. |

**Important definition caution:** D.45 is the national-accounts rent-on-land transaction, not a synonym for gross rental income declared by landlords. Do not use D.45 as a substitute for HMRC property-rental income.

The latest QSA edition page identifies the Q2 2026 workbook (release 30 September 2026; next release 22 December 2026):
- Dataset: https://www.ons.gov.uk/economy/nationalaccounts/uksectoraccounts/datasets/quarterlysectoraccounts
- Exact workbook: https://www.ons.gov.uk/file?uri=%2Feconomy%2Fnationalaccounts%2Fuksectoraccounts%2Fdatasets%2Fquarterlysectoraccounts%2Fquarter2aprtojune2026%2Fquarterlysectoraccounts2026q2.xlsx

## 2. ONS national balance sheet

| Item / series | Status | Coverage and notes |
|---|---|---|
| Total financial assets — NITF | **Extracted** | S.14 annual 1997–2025, £m, current prices, NSA. |
| Total financial liabilities — NIWJ | **Extracted** | S.14 annual 1997–2025, £m, current prices, NSA. |
| Net financial assets — NYOH | **Extracted** | S.14 annual 1997–2025, £m, current prices, NSA. |
| Total household net worth | **Headline only; component series not extracted** | ONS preliminary 2025 bulletin reports household net worth at £10.8tn and an increase of £146.1bn between 2024 and 2025. This is a rounded bulletin headline, not a row in the extracted financial-stocks CSV. |
| Non-financial assets and asset components (dwellings, land, etc.) | **Reachable but not parseable** | Present in the NBS dataset; the dataset download could not be parsed in this environment. |
| Revaluation / other-volume-change split by asset class | **Reachable but not parseable** | Not extracted. No allocation across dwellings, land, equities or other asset classes has been inferred. |

Sources:
- NBS dataset page: https://www.ons.gov.uk/economy/nationalaccounts/uksectoraccounts/datasets/nationalbalancesheet
- Exact current CSV: https://www.ons.gov.uk/file?uri=%2Feconomy%2Fnationalaccounts%2Fuksectoraccounts%2Fdatasets%2Fnationalbalancesheet%2Fcurrent%2Fnbs.csv
- 2025 preliminary bulletin: https://www.ons.gov.uk/economy/nationalaccounts/uksectoraccounts/bulletins/thenationalbalancesheetandcapitalstockspreliminaryestimatesuk/2026/previous/v1

The three extracted financial-stock series reconcile exactly as net financial assets = total financial assets − total financial liabilities. This checks the financial balance-sheet block only; it does not establish total household net worth.

## 3. Bank of England NMG household survey

The Bank describes the NMG survey as an annual survey asking about household income and spending. The following published files were reached but not parseable here; therefore no microdata variables or year coverage have been claimed.

| File | Status | Exact link |
|---|---|---|
| `boe-nmg-household-survey-data-2004-11.xlsx` | **Reachable but not parseable** | https://www.bankofengland.co.uk/-/media/boe/files/statistics/research-datasets/boe-nmg-household-survey-data-2004-11.xlsx |
| `boe-nmg-household-survey-data.xlsx` (2011–2026) | **Reachable but not parseable** | https://www.bankofengland.co.uk/-/media/boe/files/statistics/research-datasets/boe-nmg-household-survey-data.xlsx |
| `household-incomes-and-deciles-stata-file.do` | **Reachable but not parseable** | https://www.bankofengland.co.uk/-/media/boe/files/statistics/research-datasets/household-incomes-and-deciles-stata-file.do |

Landing page: https://www.bankofengland.co.uk/statistics/research-datasets.

The landing page describes the newer workbook as 71 MB; the Bank's statistics sitemap lists 80.7 MB. This discrepancy is left unresolved. The variable inventory requested by the brief (saving, income, debt, repayments, interest, financial wealth and age, with year coverage) remains outstanding until the author supplies readable files. No household-level records were extracted.

## 4. HMRC

The HMRC ODS files are published and their exact links were obtained, but the ODS contents could not be parsed. The accompanying HTML commentaries were readable, so a limited set of summary values is in `hmrc_html_summary_extracts.csv`. These are expressly labelled as summary extracts, not as full-table replacements.

| Item | Status | Notes / exact file |
|---|---|---|
| Personal Incomes Table 3.7, property/interest/dividends by total-income range | **Reachable but not parseable** | 2023–24 ODS: https://assets.publishing.service.gov.uk/media/69f20fe2b8ce27acfa096850/Table_3.7_2324.ods. HTML commentary yields selected proportions and aggregates, but not the full band-by-band table. |
| CGT Table 1, taxpayers/gains/liabilities by year | **Reachable but not parseable** | https://assets.publishing.service.gov.uk/media/6a7b23f1bbafcd1db3b6e420/Table_1_2026_Taxpayer_numbers_gains_and_tax_liabilities.ods |
| CGT Table 2, by size of gain | **Reachable but not parseable** | https://assets.publishing.service.gov.uk/media/6a7b240b423b0bdba0290eca/Table_2_2026_Size_of_gain.ods |
| CGT Table 3, by gain size and taxable income | **Reachable but not parseable** | https://assets.publishing.service.gov.uk/media/6a85a2e654bcee010d51454b/Table_3_2026_Size_of_gain_by_income.ods |
| IHT Table 12.1, estates and tax due | **Reachable but not parseable** | https://assets.publishing.service.gov.uk/media/6a61fe84243ee000f7127e8b/table_12_1_final.ods |
| IHT Table 12.2, exemptions and reliefs | **Reachable but not parseable** | https://assets.publishing.service.gov.uk/media/6a60bb74b00f3323bf1a2422/table_12_2_final.ods |
| IHT Table 12.3, assets by net-estate range and tax due | **Reachable but not parseable** | https://assets.publishing.service.gov.uk/media/6a60bb8534dfb74772f96d28/table_12_3_final.ods |
| Property rental income tables 2026 | **Reachable but not parseable** | https://assets.publishing.service.gov.uk/media/6a882b0febba21482c58cc23/property_rental_income_statistics_tables_2026.ods |

Readable HTML source pages:
- Personal Incomes commentary: https://www.gov.uk/government/statistics/personal-incomes-statistics-for-the-tax-year-2023-to-2024/personal-incomes-statistics-2023-to-2024-commentary
- CGT commentary: https://www.gov.uk/government/statistics/capital-gains-tax-statistics/capital-gains-tax-commentary--2
- IHT commentary: https://www.gov.uk/government/statistics/inheritance-tax-liabilities-statistics/inheritance-tax-liabilities-statistics-commentary
- Property rental commentary: https://www.gov.uk/government/statistics/property-rental-income-statistics/property-rental-income-statistics-2026

Coverage cautions:
- Table 3.7 is by taxpayers' **total income**, not household wealth. It cannot be relabelled as wealth-band income.
- CGT realised gains are not the same thing as accrued wealth appreciation in the WDT tax base.
- IHT figures are liabilities created on wealth transfers on death, not annual changes in household net worth or cash receipts.
- Property rental statistics cover unincorporated landlords filing ITSA returns. They exclude incorporated businesses and income below the relevant reporting thresholds. They do not provide a full population estimate of rental cash flows.

## 5. Mechanical checks

### Household saving identity

Using the national-accounts identity:

`B.8g = B.6g + D.8 - P.31`

and:

`saving\ ratio = B.8g / (B.6g + D.8)`

the extracted series give:

| Year | Derived gross saving (£m) | Derived ratio | Published DG5H | Difference |
|---:|---:|---:|---:|---:|
| 2023 | 113,799 | 6.433% | 6.4% | +0.033 pp |
| 2024 | 179,433 | 9.502% | 9.5% | +0.002 pp |
| 2025 | 188,993 | 9.587% | 9.6% | −0.013 pp |

The differences are consistent with the published saving ratio being rounded to one decimal place. The annual inputs are sourced from ONS series pages; B.6g and D.8 are marked SA, while P.31 and DG5H are NSA. This mixed presentation is recorded rather than silently harmonised. It does not prevent the displayed annual identity from reconciling to the published ratio at its reported precision.

### Financial balance-sheet identity

| Year | Financial assets (£m) | Financial liabilities (£m) | Net financial assets (£m) | Difference |
|---:|---:|---:|---:|---:|
| 2023 | 6,417,975 | 2,192,022 | 4,225,953 | 0 |
| 2024 | 6,400,576 | 2,248,228 | 4,152,348 | 0 |
| 2025 | 6,595,014 | 2,323,752 | 4,271,262 | 0 |

All three are current-price £m, end-year household-sector stocks. The 2025 vintage is the ONS NBS dataset released 10 June 2026. These rows reconcile exactly.

### Source-value spot checks

- ONS consumption P.31: 2023 £1,655,276m; 2024 £1,708,930m; 2025 £1,782,389m, matching the ABPB time-series page.
- ONS D.41 received HAXV: 2023 £86,092m; 2024 £98,189m; 2025 £95,477m. D.41 paid HACY: 2023 £83,391m; 2024 £93,356m; 2025 £87,001m.
- HMRC CGT commentary: 2024–25 gains £127bn, liabilities £24.2bn and 584,000 taxpayers.
- HMRC IHT commentary: 2023–24 30,400 chargeable estates and £7.03bn liabilities.
- HMRC property rental commentary: 2024–25 individuals £49.81bn, partnerships £9.18bn, total £58.99bn.

## 6. Author upload list

To complete the remaining source extraction, upload the exact files listed above, especially:

1. ONS Q2 2026 Quarterly Sector Accounts workbook and current NBS CSV/XLSX.
2. Bank of England NMG 2004–2011 and 2011–2026 workbooks, plus the Stata do-file.
3. HMRC Personal Incomes Table 3.7 2023–24 ODS; CGT Tables 1–3; IHT Tables 12.1–12.3; Property Rental Income Tables 2026.

Once readable files are available, the remaining work is to extract the missing series/variable inventory and add them to this same register. No further model work is authorised by this brief.

## 7. Boundary

Nothing in these data is a universal depletion rate, a consumption rate by wealth band, or a chosen fiscal parameter. National accounts are aggregate household-sector flows; HMRC tables are taxpayer or estate distributions; the NMG survey is household microdata. They are different statistical objects and must not be collapsed into one another without a separately authorised method.


## 8. Follow-up after author upload (2026-11-21)

The requested source files have now been committed under `docs/research/data/097r/` on the working branch. The upload is confirmed by the branch diff. The files present are:

| Uploaded file | Source block | Inspection outcome in this environment |
|---|---|---|
| `quarterlysectoraccounts2026q2.xlsx` | ONS QSA Q2 2026 | GitHub connector returned the binary payload as base64; workbook contents could not be decoded in the available repository-only runtime. |
| `nbs.xlsx` | ONS National Balance Sheet | Binary payload returned as base64; workbook contents could not be decoded here. |
| `boe-nmg-household-survey-data-2004-11.xlsx` | BoE NMG 2004–2011 | Uploaded and present in branch; workbook contents not inspected. |
| `boe-nmg-household-survey-data.xlsx` | BoE NMG 2011–2026 | Uploaded and present in branch; the file-content endpoint returned an empty payload, so no claim is made about its workbook contents. |
| `household-incomes-and-deciles-stata-file.do` | BoE NMG processing example | **Read and reviewed as text.** Findings below. |
| `Collated_Tables_3_1_to_3_11_2324.ods` | HMRC Personal Incomes 2023–24 | Binary payload returned as base64; ODS contents could not be decoded here. |
| `Table_1_2026_Taxpayer_numbers_gains_and_tax_liabilities.ods` | HMRC CGT Table 1 | Uploaded; ODS contents not inspected. |
| `Table_2_2026_Size_of_gain.ods` | HMRC CGT Table 2 | Uploaded; ODS contents not inspected. |
| `Table_3_2026_Size_of_gain_by_income.ods` | HMRC CGT Table 3 | Uploaded; ODS contents not inspected. |
| `table_12_1_final.ods` | HMRC IHT Table 12.1 | Uploaded; ODS contents not inspected. |
| `table_12_2_final.ods` | HMRC IHT Table 12.2 | Uploaded; ODS contents not inspected. |
| `table_12_3_final.ods` | HMRC IHT Table 12.3 | Uploaded; ODS contents not inspected. |
| `property_rental_income_statistics_tables_2026.ods` | HMRC property rental statistics | Uploaded; ODS contents not inspected. |

This changes the status from **author upload outstanding** to **author upload received; binary extraction still outstanding**. The remaining limitation is no longer missing source files. It is the inability of the GitHub connector/runtime available for this task to decode the committed XLSX/ODS payloads. No workbook values have been inferred from filenames or file sizes.

### BoE Stata do-file: what it actually supports

The uploaded `household-incomes-and-deciles-stata-file.do` is an example construction script for the 2024 and March 2025 NMG waves, not a complete codebook or a general-purpose survey extraction script.

It:
- imports the 2024 and March 2025 workbook sheets;
- creates wave dates (September 2024 and March 2025);
- combines reported annual income for the main respondent, partner/second earner and other household earners;
- combines continuous numeric responses with imputed midpoints from income bands;
- creates a constructed household annual income variable (`fihhyr2_m`);
- calculates household-income decile thresholds separately within each wave.

Important limitations for any later use:
- The script demonstrates income construction only. It does not identify or construct consumption, saving, debt balances, debt repayments, interest payments/receipts, financial wealth or age variables.
- The resulting deciles are **income deciles within survey wave**, not wealth deciles and not WDT wealth bands.
- Band responses are midpoint-imputed. The top band (>=£100,000) is assigned £125,000, which is an imposed representative value for an open-ended category, not an observed midpoint. Sensitivity to this top-band treatment would need checking before using aggregate income estimates.
- The script hard-codes `randomgen=2` and constructs the type-2 income question route shown. It should not be assumed to cover every income-question type or every wave in the workbook.
- The combined household measure requires non-negative values for the respondent, partner and other earners; don't-know, refusal and missing codes propagate to the household total. This affects usable sample size and should be quantified from the actual microdata before analysis.
- It is an example script with placeholder import/save paths. It is not a ready-to-run pipeline without editing.

**Implication:** the Stata file gives a concrete method for constructing household income in two recent waves, but it does not establish that NMG can answer the household saving/consumption/debt/wealth questions in 097r. The workbook variable inventory remains unverified. No household-level records have been extracted.

### Revised completion state

- Source upload step: **met**; the requested ONS, BoE and HMRC files are present in the branch.
- Stata example review: **met**; its purpose and limitations are now documented.
- ONS workbook series extraction: **not yet met**; uploaded XLSX contents remain unread.
- BoE NMG variable inventory: **not yet met**; uploaded workbooks remain unread.
- HMRC detailed table extraction: **not yet met**; uploaded ODS contents remain unread.
- Existing HTML-derived CSVs and mechanical checks remain unchanged.
- No model parameters, wealth-band rates or fiscal conclusions have been added.

To complete the remaining work, the binary files need to be opened in a local checkout or supplied in a form the analysis runtime can parse. Once parsed, update this same register and the relevant CSVs; do not create substitute series from the HTML summary extracts.


## 9. Binary extraction completed by the guru (2026-11-21)

The agent's runtime could not decode the uploaded workbooks; the files are valid and open with openpyxl, pandas and odfpy. `docs/research/data/097r/extract_binaries.py` (committed, reproducible) now writes text from them. Sections 1 to 8 above are unchanged; where they say "not parseable" or "uploaded, not inspected", this section supersedes them.

**What is now extracted**
| Output | From | Content |
|---|---|---|
| `qsa_household_annual_2026q2.csv` (1,655 rows) | `quarterlysectoraccounts2026q2.xlsx` sheets HH_1, HH_2, HH_3, HH_Alt, annual table 1 | S.14 primary income, secondary distribution, use of disposable income, and the cash-basis alternative, 1948 or 1997 to 2025, with ONS series ids. It reproduces the agent's HTML-page figures (gross saving 113,799, 179,433, 188,993 for 2023 to 2025) |
| `hmrc_csv/` (47 files) | the seven HMRC `.ods` files, every table sheet | Personal Incomes 3.1 to 3.11 (2023-24, including 3.7 property, interest and dividends by total-income range), CGT tables 1 to 3, IHT 12.1 to 12.3, property rental tables, as plain text. Not yet reconciled to the commentary figures |
| `nmg_variable_inventory_2011_2026.csv` (696 variables) | `boe-nmg-household-survey-data.xlsx`, sheet "Data description" | Variable names and question labels. The year-by-year availability sheet holds uncached formulas and was not computed |

**New facts the ONS workbook gives**
- ONS splits the saving ratio into non-pension and pension parts: non-pension (JS8S) 1.7, 4.8 and 5.1 points and pension (JS97) 4.0, 4.6 and 4.5 points in 2019, 2024 and 2025 (total 5.7, 9.5, 9.6). Roughly half of the 9.5% is pension accrual. 093r's "1.6% of net worth" used the whole ratio, so it is a pension-inclusive figure; a model check on aggregate saving must apply this split.
- The cash-basis ratio (CSJ8, experimental, which removes imputed items and the pension adjustment) is 2.4, 7.4 and 7.8% in 2019, 2024 and 2025.
- The non-pension contribution swings widely (13.6 in 2020, -0.1 in 2022), so a single year is not a baseline.

**Bank of England NMG (2011 to 2026)**
- 18 online waves, about 6,000 households each (995 in 2011, 4,003 in 2012); weights `we_factor` and, from the September 2026 release, `we_factor_adjusted`; raw, uncleaned data.
- Relevant variables: monthly cash saved from income (`be2afree_c`), cash savings held in ranges (`boe65a`), mortgage and secured-loan balance (`be07free_c`) and monthly instalment (`be08free_c`, `be08re`), total unsecured debt (`totaldebt`, `qbe16refree_c`), monthly payments on credit cards and other loans (`be17a`, `be17b`), household income in ranges (`qincomev1`, `qincomev2`), age (`dage`, `nage`), working status (`a20workingstatus`), and mortgage rate (`boe47`).
- Absent: pension wealth, investments, housing value (only value at purchase, `be401free_c`), and inheritance or gifts. So NMG gives **income-side saving and debt service by income and age**, not wealth bands.
- The 2004 to 2011 face-to-face file (7 MB) has its own numbered variable list; not parsed.
- The BoE do-file builds income deciles only (see section 8).

**Still outstanding**
1. **`nbs.xlsx` is empty** (one sheet, one cell). The National Balance Sheet needs downloading again from `ons.gov.uk/file?uri=%2Feconomy%2Fnationalaccounts%2Fuksectoraccounts%2Fdatasets%2Fnationalbalancesheet%2Fcurrent%2Fnbs.csv` as the CSV: author upload.
2. The QSA workbook's revaluation and other-changes-in-volume sheets (B.9, BF.90 hold lending and financial net worth only; no revaluation sheet exists in this edition). Revaluation by asset class has to come from the balance sheet.
3. D.42 paid, D.44 received and paid: not in the HH sheets of this workbook; look in the UK Economic Accounts workbook.
4. HMRC CSVs are raw sheet dumps; the numbers need reconciling to the commentary.
5. NMG year-by-year variable availability.

**Repository note.** The two NMG workbooks (80 MB and 7 MB) and the empty `nbs.xlsx` are not committed (80 MB in git history is permanent); they are listed in `.gitignore` and kept locally. The branch history holds them until deleted.
