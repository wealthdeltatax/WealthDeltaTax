# WDT data audit: receipt of manual-research files (16 Oct 2026)

Companion to `audit_progress_2026-10-15b.md`, `audit_progress_d7_d9_2026-10-15.md` and `Manual Research.md`. Every file below was opened in this pass. Nothing in the TOML, registers, matrices or JSON has been edited. WID is treated as provisional: the user is replacing the manual download with an API pull.

## 1. Item-by-item status against `Manual Research.md`

| # | Item | Received | Readable | Closes | Does not close |
|:--|:---|:---|:---|:---|:---|
| 1 | WID wealth (D1, D8) | `1a` data, `1b` metadata | Yes | D1 spans for 12 of 14 countries (section 2) | PT and CA absent; no per-year interpolation flags; no top shares (D8) |
| 2 | OECD Revenue Statistics, UK | `2a` full UK file (24,590 rows), `2b` country note | Yes | D5 calibration B target; leg shares of GDP (not yet extracted) | none |
| 3a | HMRC CGT Table 2 | Yes | Yes | CGT taxpayers, gains, tax by gain band, 2021-22 to 2024-25 | not by wealth band |
| 3b | HMRC CGT Table 3 | Yes | Yes | Same, by taxable income band, four years | not by wealth band |
| 3c | HMRC IHT Table 12.3 | Yes | Yes | Assets by net-estate band, 2023-24 (12.3a, 12.3b) | Table 12.1 not sent; 12.4 not sent |
| 3d | HMRC receipts `NS_Table` | Yes | Yes | Employer NI (`employer_share`), CGT, IHT, CT receipts, 2006-07 to 2025-26 | none |
| 3e | Corporation Tax statistics 2025 data tables | **No** | n/a | n/a | HMRC "Corporate Taxes" vs OECD 1200 reconciliation |
| 4a | EHS FT1101 tenure | Yes | Yes | Tenure 1939-2024-25 (annual from 1981) | adults per household by tenure |
| 4c | EHS Ch.1 tables and Annex | Yes | Yes | 1918-2013 benchmarks and 1980-2013 counts | same |
| 5 | Saez-Zucman main data | Yes | Yes | Top 0.1% saving rate (sheet `DataFig9a`, 1914-2011) | US only; saving over income, not net drawdown over wealth |
| 6 | HPSSA median price | Yes | Yes | `house_median_gbp_m` (section 3) | UK-wide median; post-2023 vintage |
| 7 | ONS population | Yes (Nomis) | Yes | UK total population 1991-2025 | **All ages only. No 16+/18+ split, so D9 and `adults_m` stay open** |
| 8 | JST house-price documentation | `NPLH_documentation.pdf` | Yes, now text | KSS sources by country | See section 4 |
| 9 | Moatsos et al. data (NLD) | No | n/a | n/a | Not gate-critical now |
| 10 | Abildgren data (DNK) | No | n/a | n/a | Not gate-critical now |
| 11 | Kuvshinov-Zimmermann appendix | **No** | n/a | n/a | `mc_gdp` after 2016 still unverified |
| 12 | WAS data dictionary (SN 7215) | **No** | n/a | n/a | D6 tax/NI variables still unconfirmed |

## 2. WID (provisional, replaced by the API pull)

- 70 series, 14 countries: AUS DNK FIN FRA DEU ITA JPN NLD NOR ESP SWE CHE USA GBR. **Missing from the 16: PRT, CAN.** BEL was not asked for.
- Per country: `apweal` (net private wealth, individuals), `ahweal` i (net personal wealth, individuals) and j (equal-split adults), `anninc` (national income), `agdpro` (GDP). All "average, constant 2025 PPP". W/Y is `apweal / anninc`, same unit.
- Spans (non-empty, quality above 0): 1800-2025 for 12 countries, FIN 1980-2025, CHE 1950-2025. The 2026 update (Bauluz et al. 2025) replaced the shorter spans in the 2020 technical note, so earlier D1 start years (AUS 1960, JPN 1970, NOR 1980, NLD 1995, DNK 1973) are superseded.
- Overlap with JST LEVY usable years (`usable_years.csv`):

| Country | JST LEVY years | WID overlap | Earlier matrix | Gate (50) |
|:---|---:|---:|---:|:---|
| AUS | 115 | 115 | 60 | pass |
| CHE | 79 | 56 | 79 (Baselgia) | pass (WID begins 1950) |
| DEU | 114 | 114 | 112 | pass |
| DNK | 139 | 139 | 46 (WID) / 132 (Abildgren) | pass on WID |
| ESP | 112 | 112 | 112 | pass |
| FIN | 98 | 40 | 23 | **fail** |
| FRA | 143 | 143 | 142 | pass |
| GBR | 117 | 117 | 116 | pass |
| ITA | 86 | 86 | 52 | pass |
| JPN | 74 | 74 | 48 | pass |
| NLD | 85 | 85 | 25 (WID) / 84 (Moatsos) | pass on WID |
| NOR | 132 | 132 | 39 | pass |
| SWE | 137 | 137 | 137 | pass |
| USA | 130 | 130 | 129 | pass |
| BEL, PRT | n/a | none | none | fail |

  Result: **13 of 16 pass** on WID alone (was 11 on paper, 8 on verified spans). The gate no longer depends on Moatsos, Abildgren or Baselgia. Under principle 3 (supersession) that reverses two earlier supersessions (NLD, DNK); needs your confirmation.
- Cautions for the API pull:
  1. The download carries a data-quality score (0-5 scale assumed, not confirmed) but **no interpolation flags**, and quality is 3 or more in every year back to 1800. It cannot yet tell benchmark years from extrapolated years. D1 grading and the max-interpolation-gap decision need that flag.
  2. NOR W/Y in 2019 is 2.92; every other country is 3.3 to 7.9 (UK 5.22, US 5.40). Check the Norway series definition before use.
  3. `ahweal` j (equal-split adults) matches the per-adult decision but is patchy: none for AUS and JPN, NOR 2010-19, FIN 1995-2017, DNK 1980-2012. Ask for it, with quality, in the API pull.
  4. For D8: request top 1% and top 0.1% wealth shares (not in this download).

## 3. Values now available (not yet written into any register or the TOML)

- **OECD 1200, UK, % of GDP**: 1965 1.33, 1990 3.26, 2000 3.47, 2010 2.84, 2018 2.56, 2019 2.32, 2020 2.38, 2021 2.94, 2022 3.21, 2023 3.38, 2024 3.47. **Trailing 5-year average 2020-24: 3.08%** (the 2019-23 window gives 2.85%). Latest year as sensitivity: 3.47%. General government and central government are identical for 1200 (no sub-national CIT). Earlier note that old data gave 2.65-2.85% is now superseded.
- Same file carries 1100 (personal income incl. CGT), 2000/2100/2200 (SSC, employee, employer), 4100, 4300 (estate, inheritance and gift) and total tax, so leg shares of GDP can be extracted for 2024 (for example 1100 = 10.77, 2000 = 6.07, total = 34.37).
- **`house_median_gbp_m`**: HPSSA median price paid, existing dwellings, year ending Dec 2017: **England 225,000; England and Wales 220,000**. The TOML's 0.225 therefore equals the England median. The 15 Oct note calling it "a mean near the UK average" was wrong; label it "England median, existing dwellings, Dec 2017", no longer an unsourced placeholder. At `wmin_house_ratio` 0.5 (patch pending), W_min is £112,500 per adult. The workbook ends Mar 2023.
- **Employer NI** (`employer_share`): HMRC annual receipts show PAYE employer NIC1 of £143.9bn against employee £49.4bn and total NICs £200.8bn in 2025-26 (employer series starts 2015-16). Gives the aggregates the 0.25 judgment was waiting for; the mapping to "share of residual relief" is still a modelling choice.
- **Other HMRC 2025-26**: income tax £326.9bn, CGT £24.3bn, IHT £8.5bn, corporation tax £95.1bn. CGT 2024-25 individuals: about 3 thousand taxpayers with gains of £5m or more, £48.5bn of gains, £9.9bn of tax.
- **IHT 12.3b (2023-24)**: estates with net capital of £1m+ number about 1,040 and hold £8,170m of net capital, including £3,490m of securities. Bands are by net estate, not wealth.
- **EHS**: owner-occupier share of households 64.8% in 2024-25 (England). Annex benchmarks: 1918 23%, 1939 32%, 1953 32%, 1961 43%. The chapter text says 25% for 1918 and the figure data says 23%; use the data.
- **Saez-Zucman saving rate by wealth class** (`DataFig9a`): bottom 90%, top 10%, 5%, 1% and 0.1% from 1914-1917 to 2011, whole-population from 1913 to 2012. Closes the top 0.1% request.

## 4. Gaps and corrections

1. **JST house-price source for ITA, ESP, PRT: still open.** The "NPLH_documentation.pdf" supplied is the Knoll-Schularick-Steger online appendix, not a JST file. It covers 14 economies (AUS BEL CAN DNK FIN FRA DEU JPN NLD NOR SWE CHE GBR USA) and none of ITA, ESP, PRT, IRL. It does give per-country source tables, for example the UK series begins 1899, which agrees with the GBR HOUSE start of 1900.
2. **Nomis file is all ages**, despite the title "by single year of age". Re-export with age as single year, or 16+ and 18+ aggregates, gender Total, UK, 1971 onwards (Nomis may start at 1991 for this dataset; ONS mid-year estimates go earlier).
3. **Adults per household by tenure**: not in either EHS file or any other file received. Still needed to convert D3 to the adult basis.
4. **UK saving by wealth (D2 gate)**: no new evidence. Still pooled, grade C.
5. **Kuvshinov-Zimmermann, WAS dictionary, Corporation Tax statistics tables, IHT 12.1 and 12.4**: not received.

## 5. What you need to decide or supply

Decisions:
1. Confirm WID as primary for NLD and DNK (reverses the Moatsos and Abildgren supersessions) and for CHE from 1950.
2. D5 year basis: the window can now be fixed (trailing 5-year 2020-24 = 3.08%, sensitivity 3.47%). Confirm.
3. Carried over, unchanged: D3 level tolerance; CIT owner-share sweep values; maximum interpolation gap; D1 per-run minimum overlap (20) and pooling weights; D4 year and category mapping; `mc_gdp` stand-in; TOML patch `wmin_house_ratio` 1.0 to 0.5.

Data to supply or request:
1. WID API pull: add PRT (and CAN if wanted), per-year interpolation flags, `ahweal` j with quality, top 1% and 0.1% shares, NOR definition check.
2. Nomis or ONS: UK population by single year of age (or 16+/18+).
3. EHS or WAS: adults per household by tenure.
4. Kuvshinov-Zimmermann appendix (tables E.1 to E.17) or a UK substitute for market cap / GDP after 2016.
5. WAS data dictionary (SN 7215).
6. HMRC Corporation Tax statistics 2025 data tables; IHT 12.1 (and 12.4 if it exists for later years).
7. JST house-price documentation for ITA, ESP, PRT (the macrohistory.net PDF is image-only; a manual read or OCR is needed).

## 6. Extractions that can be done now, with no new data

OECD leg shares 2024 and 5-year averages; HMRC CGT and IHT band tables to CSV; HMRC receipts series to CSV; EHS tenure series to CSV; Saez-Zucman saving by class to CSV; HPSSA 2017 median recorded in the D10 register; the WID-based D1 gate table above regenerated by script once the API pull lands.
