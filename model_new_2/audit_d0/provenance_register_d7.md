# D7 provenance and status (house prices)

Date: 15 October 2026. Companion: `coverage_matrix_d7.csv`. Hook: `house` index mode (sensitivity) and the ownership validation (D3). Gate (spec): D0 reports coverage; windows without house prices drop under that mode; record how many.

## What was opened

| Source | Status | Opened |
|:---|:---|:---|
| D0 outputs (`audit_d0.md`, `usable_years.csv`) | verified | Per-country HOUSE usable years and window counts. |
| Knoll, Schularick, Steger, CESifo WP 5006 | verified (text) | Countries, start years, methods, sources. Data file not opened. |
| ICPSR 113055 (replication data) | partly | One file listed, no variable names, no licence stated. |
| OECD Analytical house prices indicators (DBnomics) | partly | Measures and sample spans (annual 1970-2025 for price and price-to-income series shown). |
| BIS residential property price statistics | located | Documentation PDFs only; not opened. |

## Windows lost under the house index (gate record)

HOUSE set (hpg_real required) against LEVY, from `audit_d0.md`:

| T | LEVY total | HOUSE total | LEVY contiguous | HOUSE contiguous | Contiguous lost | Countries with contiguous (LEVY to HOUSE) |
|---:|---:|---:|---:|---:|---:|:---|
| 30 | 1728 | 1575 | 859 | 781 | 78 | 16 to 15 |
| 40 | 1728 | 1575 | 637 | 575 | 62 | 16 to 15 |
| 50 | 1728 | 1575 | 463 | 410 | 53 | 14 to 13 |
| 60 | 1728 | 1575 | 317 | 283 | 34 | 12 to 10 |
| 100 | 1728 | 1575 | 69 | 69 | 0 | 2 to 2 |

Total windows lost: 153 (1728 to 1575), which equals ESP 66, PRT 40, ITA 36, JPN 6, GBR 5. Against BASE (1801) the loss is 226. Under house mode the contiguous set loses ESP, ITA and PRT altogether at long T, and the sample leans further to countries with long house-price series (the 14 KSS economies plus post-1970 Italy and Spain).

## Findings

1. **Coverage.** House prices restrict three countries heavily: ESP (1972 on), ITA (1971 on) and PRT (2005 on). Everything else is within 6 years of its LEVY coverage, and the 11 other countries match.
2. **JST source.** The JST house-price history is understood to build on the KSS series for 14 economies from 1870 to 2012 (not verified in this session). KSS include neither Italy, Spain nor Portugal, so the JST source for those three was not confirmed here. Their start years are consistent with BIS and OECD post-1970 data.
3. **House-price / income.** The OECD price-to-income ratio (annual from 1970) gives a level ratio post-1970; before 1970 there is no level ratio. JST hpnom with gdp yields an index of price to GDP per head only, so it cannot give a level without a base-year anchor.
4. **Quality caveats from KSS.** Mixed methods (hedonic, repeat sales, stratification, SPAR, mean or median prices); some series discontinuous; rural or existing-dwelling series for early years (for example Denmark 1875-1937, rural existing dwellings).

## Gate

Pass in the sense of the spec: coverage is recorded and the loss is counted. The house sensitivity should be reported with the 153 windows dropped and the loss of ESP, ITA and PRT stated.

## Open

1. Open the KSS data file and the BIS and OECD documentation; confirm the JST source for ITA, ESP, PRT.
2. Confirm the OECD price-to-income definition and country list.
3. Decide whether a price-to-income level before 1970 is needed (for the ownership validation) or whether the index suffices.
