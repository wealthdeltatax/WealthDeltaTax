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
