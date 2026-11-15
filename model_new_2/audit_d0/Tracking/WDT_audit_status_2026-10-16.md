# WDT data audit: consolidated status (16 Oct 2026)

Single status note for D0 to D10. It replaces `WDT_audit_summary_open_items.md`, `audit_progress_2026-10-15b.md`, `audit_progress_d7_d9_addendum_2026-10-15.md`, `Manual Research.md`, `audit_progress_2026-10-16_data_receipt.md` and, since sections 7 and 8 absorb its findings, `audit_progress_d7_d9_2026-10-15.md`. Per-dataset detail stays in `coverage_matrix_dN.csv` and `provenance_register_dN.md`; placeholders in `placeholder_register.md`; decisions in `decision_log.md`.

Status of edits: nothing in the TOML, registers, matrices or `wdt_audit.json` has been changed by this note. They still carry stale statuses (section 11). WID is provisional: the manual download is being replaced by an API pull. Everything else is treated as final.

## 1. Gate outcomes

| Dataset | Gate (spec) | Outcome | Notes |
|:---|:---|:---|:---|
| D0 JST audit | none | Done, verified | Table 26 reproduces; CAN and IRL have no usable years. |
| D1 household wealth / GDP | at least 8 of 16 countries with at least 50 usable years | **Pass: 13 of 16 on WID alone** | Section 3. FIN fails (40); BEL and PRT have no WID series. Gate no longer rests on Moatsos, Abildgren or Baselgia. Provisional until the API pull. |
| D2 saving by wealth | shape evidence for UK, US, one Nordic | **Not met for the UK** | US (Saez-Zucman, now in hand) and Norway (Fagereng et al.) exist. UK pooled shape, grade C. |
| D3 ownership | UK and US full series | **UK series in hand; adult basis open** | EHS FT1101 annual from 1981, benchmarks from 1918. Adults per household by tenure still missing. US annual from 1965. |
| D4 equity ownership | UK from first year; others by era, grade C fallback | **UK pass (1963 to 2024, 28 survey years); US pass (1945 to 2025)** | Euro area from 1995 at best. `mc_gdp` after 2016 unverified (K-Z appendix not received). |
| D5 corporate tax | UK full; others if profits series exist | **UK pass: target now fixed** | OECD 1200 UK file received. HMRC "Corporate Taxes" reconciliation not done (CT statistics tables not received). |
| D6 burden allocation | joint cut or flag as placeholder | **Fallback: income profile is a placeholder** | CGT and IHT aggregates by band exist, not by wealth band. WAS dictionary not received. |
| D7 house prices | D0 coverage; record windows lost | **Done: 153 windows lost vs LEVY (ESP 66, PRT 40, ITA 36, JPN 6, GBR 5)** | Contiguous at T=30: 859 to 781; T=100 unchanged (69). JST source for ITA, ESP, PRT unconfirmed. |
| D8 concentration | none (context) | **Census done; values extractable from WID API pull** | UK from 1895 (estate multipliers). Top shares not in the manual download. |
| D9 demographics | none (documentation) | **Partly recorded** | Age at inheritance 55-64 peak, projected mode 61; 16+/18+ series still open. |
| D10 placeholders | source or replace | **Register complete; `house_median_gbp_m` now sourced, others open** | Section 6. |

## 2. Item-by-item receipt against the manual-research list

| # | Item | Received | Closes | Does not close |
|:--|:---|:---|:---|:---|
| 1 | WID wealth (D1, D8) | `1a` data, `1b` metadata | D1 spans for 12 of 14 countries | PT and CA absent; no interpolation flags; no top shares |
| 2 | OECD Revenue Statistics, UK | `2a` (24,590 rows), `2b` country note | D5 target; leg shares of GDP | none |
| 3a | HMRC CGT Table 2 | Yes | Taxpayers, gains, tax by gain band, 2021-22 to 2024-25 | not by wealth band |
| 3b | HMRC CGT Table 3 | Yes | Same, by taxable income band | not by wealth band |
| 3c | HMRC IHT Table 12.3 | Yes | Assets by net-estate band, 2023-24 | Tables 12.1 and 12.4 not sent |
| 3d | HMRC receipts `NS_Table` | Yes | Employer NI, CGT, IHT, CT receipts, 2006-07 to 2025-26 | none |
| 3e | Corporation Tax statistics 2025 data tables | **No** | n/a | HMRC vs OECD 1200 reconciliation |
| 4a, 4c | EHS FT1101; Chapter 1 and Annex | Yes | Tenure 1918-2024-25 | adults per household by tenure |
| 5 | Saez-Zucman main data | Yes | Top 0.1% saving rate (`DataFig9a`, 1914-2011) | US only; saving over income, not net drawdown over wealth |
| 6 | HPSSA median price | Yes | `house_median_gbp_m` | UK-wide median; vintage ends Mar 2023 |
| 7 | ONS population (Nomis) | Yes | UK total population 1991-2025 | **All ages only; no 16+/18+ split** |
| 8 | JST house-price documentation | `NPLH_documentation.pdf` (KSS appendix) | KSS sources for 14 economies | ITA, ESP, PRT not covered |
| 9 | Moatsos et al. (NLD) | No | n/a | Not gate-critical now |
| 10 | Abildgren (DNK) | No | n/a | Not gate-critical now |
| 11 | Kuvshinov-Zimmermann appendix | **No** | n/a | `mc_gdp` after 2016 |
| 12 | WAS data dictionary (SN 7215) | **No** | n/a | D6 tax/NI variables |

## 3. D1: WID overlap with JST LEVY usable years (provisional)

- 70 series, 14 countries (AUS DNK FIN FRA DEU ITA JPN NLD NOR ESP SWE CHE USA GBR). **Missing: PRT, CAN.** BEL was not asked for.
- Series: `apweal` (net private wealth, individuals), `ahweal` i (individuals) and j (equal-split adults), `anninc` (national income), `agdpro` (GDP); all average, constant 2025 PPP. W/Y = `apweal / anninc`.
- Spans (non-empty, quality above 0): 1800-2025 for 12 countries, FIN 1980-2025, CHE 1950-2025. The 2026 update (Bauluz et al. 2025) replaces the shorter spans in the 2020 technical note, so earlier start years (AUS 1960 or 1970, JPN 1970 or 1960, NOR 1980, NLD 1995, DNK 1973, ITA 1965) are superseded.

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
| BEL, PRT | n/a | none | none | fail (pooled c, grade C) |

Under principle 3 (supersession) this reverses the NLD and DNK supersessions of Moatsos and Abildgren and the CHE reliance on Baselgia from 1950; needs confirmation (section 9).

**Cautions for the API pull**
1. The download has a data-quality score (0-5 assumed, not confirmed) but **no interpolation flags**; quality is 3 or more in every year back to 1800. It cannot separate benchmark from extrapolated years, which D1 grading and the maximum-interpolation-gap decision need.
2. NOR W/Y in 2019 is 2.92; every other country is 3.3 to 7.9 (UK 5.22, US 5.40). Check the Norway definition.
3. `ahweal` j (equal-split adults) fits the per-adult decision but is patchy: none for AUS and JPN, NOR 2010-19, FIN 1995-2017, DNK 1980-2012. Request it with quality.
4. For D8 request top 1% and top 0.1% wealth shares.

**Per-run minimum overlap** (computed on the pre-WID sources in `d1_overlap_runs.csv`): dropping runs shorter than a minimum leaves the gate outcome identical at minimums of 10, 20 and 30. At 20, only CHE runs 1-2 (79 to 56), DEU run 2 (112 to 98) and NLD-Moatsos run 1 (84 to 70) are dropped; DNK-Abildgren is unchanged at 20 and falls to 112 at 30. Recommendation: minimum 20, pooling weight = retained overlap years. Rerun on the WID series once the API pull lands (the CHE figure already equals the WID overlap of 56).

**Source verification** (superseded for gate purposes, but kept for grades and flags)

| Item | Finding | Effect |
|:---|:---|:---|
| NLD | Toussaint, de Vicq, Moatsos, van der Valk; WID WP 2022/19; Eur. Econ. Rev. 178 (2025), DOI 10.1016/j.euroecorev.2025.105099. Household wealth 1854-2019, SNA basis. Annual 1880-1938, benchmarks 1938/1946-52/1958/1960 with 1947-1969 interpolated, annual 1970-2019. Pensions separate. | Correct the author list in the matrix; interpolation share to flag if the series is used. |
| DNK | Abildgren, Nationalbanken WP 92 (2015). National wealth 1845-2013, no private/government split. Data on request. | Concept proxy, grade C only. |
| CHE | Baselgia and Martinez, WID WP 2020/28. Private wealth incl. NPISH, excludes PAYG pensions and durables. Annual from 1981; earlier years extrapolated. | Pre-1981 interpolated: flag. |
| PRT | Cardoso and Cunha, Banco de Portugal WP 4/2005, 1980-2004. | Fail confirmed; pooled c, grade C. |
| JPN, AUS | Earlier open start-year questions (JPN 1970 vs 1960; AUS 1960 vs 1970) | **Closed by the WID download**: both now 1800 or later; JPN 74, AUS 115. |

## 4. D2 to D6: values and readings

**D2 saving by wealth.** All sources are saving over income, not net drawdown over wealth; the model's c needs wealth/income by group to convert.
- Saez and Zucman (2016): bottom 90% about 3%, next 9% about 15%, top 1% about 20-25% of pre-tax income; synthetic, net of asset price changes, includes retained earnings. `DataFig9a` now gives bottom 90%, top 10%, 5%, 1% and 0.1%, 1914-2011.
- Fagereng et al. (NBER w26588): net saving rate flat around 7% over income; gross rate rises to 35% for the top 1% (includes capital gains). Saving over wealth is Figure 10d (numbers not read).
- Mian, Straub, Sufi (NBER w26941), by INCOME percentile: top 1% over 40%, next 9% 20%, 51-90 12%, bottom 50% about zero; net of valuation effects.
- UK: no saving-by-wealth tabulation found. Resolution Foundation "Before the fall" (2025) splits saving by income quintile; passive gains explain 60% of average family wealth growth. Candidates located but not opened: IFS R71, Wealth Tax Commission EP1. D2 UK gate unmet; pooled shape, grade C.

**D3 housing and tenure.**
- Owner-occupier share of households 64.8% in 2024-25 (England). Annex benchmarks 1918 23%, 1939 32%, 1953 32%, 1961 43%. The chapter text says 25% for 1918 and the figure data says 23%; use the data.
- FT1101 annual from 1981 (earlier benchmarks 1939-1981); Chapter 1 Figure 1.1 bars 1918, 1939, 1953, 1961, 1971, 1981, 1991, 2001, 2013-14.
- Observed series are household shares; `scope_share_t` is adult-based (accepted, flagged).

**D4 holder shares.** Checked against `uk_holder_shares_ons.csv`:
- `household_tranche_z1_equiv` equals individuals + charities_etc in every row (max difference 4e-15). 2024: 12.0%.
- Rest of world: 56.3 (2020), 57.7 (2022), 58.8 (2024); three-edition mean 57.6. Recommend 2024 (58.8), year-matched with end-2024 `mc_gdp`; matches the TOML's 0.588.
- Survey-year gaps 6, 6, 6, 8 (1981-89), then 3 (1994-97), annual or biennial after. Largest 8, inside the 10-year default.
- UK 1998 to 2008 shares are `carried`.

**D5 corporate tax.**
- OECD 1200, UK, % of GDP: 1965 1.33, 1990 3.26, 2000 3.47, 2010 2.84, 2018 2.56, 2019 2.32, 2020 2.38, 2021 2.94, 2022 3.21, 2023 3.38, 2024 3.47. **Trailing 5-year average 2020-24: 3.08%** (2019-23 gives 2.85%); latest year 3.47% as sensitivity. General and central government identical for 1200. The earlier 2.65-2.85% figure from old data and the DBnomics 2018-22 values (2.549, 2.305, 2.393, 2.916, 3.105; April 2024 vintage) are superseded.
- Same file carries 1100, 2000/2100/2200, 4100, 4300 and total tax; 2024 for example 1100 = 10.77, 2000 = 6.07, total = 34.37.
- HMRC "Corporate Taxes" = corporation tax (onshore and offshore) plus bank levy, bank surcharge, residential property developer tax, energy profits levy, electricity generator levy. Reconciliation to OECD 1200 awaits the CT statistics tables.

**D6 HMRC.**
- Receipts 2025-26: income tax £326.9bn, CGT £24.3bn, IHT £8.5bn, corporation tax £95.1bn; PAYE employer NIC1 £143.9bn against employee £49.4bn, total NICs £200.8bn (employer series from 2015-16). Gives the aggregates `employer_share` (0.25 judgment) was waiting for; mapping to "share of residual relief" remains a modelling choice.
- CGT 2024-25: 584,000 taxpayers, gains £127.3bn, liabilities £24.2bn; gains of £5m+ are under 1% of taxpayers and 45% of CGT; about 3 thousand taxpayers with £5m+ gains, £48.5bn of gains, £9.9bn of tax (individuals).
- IHT 2023-24: 30,400 taxpaying estates, £7.03bn; £2m-£7.5m band 3,156 estates at 25% effective; over £10m 220 estates at 18%. Table 12.3b: estates with net capital of £1m+ about 1,040, holding £8,170m net capital incl. £3,490m securities. Bands are by net estate, not wealth.
- Table 12.4 (cited by the D6 register for 2019-20) vs 12.3 (pointed to by the 2023-24 commentary): send both if they exist.

## 5. Corrections to earlier statements

- `house_median_gbp_m = 0.225` is **not** a mean near the UK average (15 Oct claim, based on UK HPI mean Dec 2017 of £226,756). It equals the HPSSA England median, existing dwellings, year ending Dec 2017 (England £225,000; E&W £220,000). Label it that way.
- The KSS appendix supplied as "NPLH_documentation.pdf" is not a JST file; the macrohistory.net version is image-only.
- Nomis "by single year of age" is all ages only.
- "11 of 16" and "8 on verified spans" for D1 are superseded by 13 of 16.

## 6. D10 placeholders

- `house_median_gbp_m = 0.225`: sourced (section 5). At `wmin_house_ratio` 0.5 (patch pending, from 1.0), W_min = £112,500 per adult.
- `adults_m = 54.0`: inconsistent with `pop_per_adult = 1.27`. ONS mid-2017 UK population 66,040,229 / 1.27 = 52.0m; ONS projected 18+ for 2018 is 52.4m; 16+ in mid-2017 about 53.5m (derived). 54.0 fits only a 16+ count around 2018-19. Use 52.0 for consistency or state it as a 16+ figure.
- `mc_gdp`: do not use the World Bank market-cap series for the UK (different scope; the series seen ends 2014 at 115.7%; CEIC shows 70.4% for 2023 against the model's 87.6% for 2024). For the UK divide the ONS grossed market-value series by GDP; World Bank only for non-UK countries, grade C. Resolved properly only by the K-Z appendix.
- `employer_share = 0.25`: still a judgment (section 4, D6).

## 7. D7 house prices

- Window counts reproduce from `windows.csv` and `usable.csv`: LEVY 1728 to HOUSE 1575 (-8.9%); against BASE 1801 the loss is 226. Contiguous losses 78 / 62 / 53 / 34 / 0 at T = 30 / 40 / 50 / 60 / 100.
- T = 100: the contiguous loss is 0 only because just SWE and USA have 100-year contiguous runs; report the total 1728 to 1575 beside the T = 30-60 table. Repeating-year windows are 27.6% (LEVY) and 28.0% (HOUSE).
- PRT has contiguous windows only at T of 40 or less (runs 40 and 15), so for T of 50 or more it is already out of LEVY; the HOUSE loss there is ESP and ITA (ITA keeps one window at T = 50, none at 60).
- Pre-1970 price-to-income level (D7 open item 3): not needed. `house` index mode uses only `hpg_real`; W_min is anchored once at launch. (My reading of the Code Reference; say if a level is wanted elsewhere.)
- **JST house-price source for ITA, ESP, PRT: open.** KSS cover 14 economies, none of these (nor IRL). BIS post-1970 sources: Italy = Bank of Italy (Consulente Immobiliare) and Istat; Spain = Ministerio de Fomento, INE and Bank of Spain; Portugal = Confidencial Imobiliario and Statistics Portugal. D0 start years (ITA 1971, ESP 1972, PRT 2005) are consistent with these but unconfirmed. PRT 2005 matches a private-vendor series: quality caveat. KSS give UK from 1899, agreeing with GBR HOUSE start 1900.

## 8. D8 and D9

**D8.** No gate. UK and US top 1% and 0.1% net personal wealth shares can come from the WID API pull. Treat WID imputed country-years as non-independent.

**D9.**
- `pop_per_adult = 1.27` behaves as an 18+ convention (66.04m / 1.27 = 52.0m vs ONS 18+ projection 52.4m for 2018; a 16+ basis gives about 1.23). Record as 18+.
- Generation gap G: ONS mean age of mother at birth 30.9 (2023), 30.0 (2013); father 33.8 (2023), 32.8 (2013). G = 30 sits at the mothers' mean.
- Correction to the D9 register: G is the parent's age when the heir was born (= parent's age at death minus heir's age at inheritance), so read it against mean parental age at birth, not "the length of a parent's remaining life". A Resolution Foundation inheritance mode of 61 implies a parent age at death near 91 at G = 30, a projection for today's 20-35 year olds, not a check on G.
- Open: long-run mean age at birth and adults per head before 2010. ONS ad hoc 2871 (16+ by UK country, 2024) and 2713 (median age 1971-2023) exist; the mid-year estimates dataset is the route.

## 9. Decisions

**Made**

| Date | Decision |
|:---|:---|
| 14 Oct | D1 identity route: solve c per contiguous JST run and pool the run estimates. |
| 14 Oct | D1 grading: strict (any documented definitional gap caps at B). |
| 14 Oct | Close D4 open items before D3. |
| 15 Oct | D4 household tranche matches US Z.1 "households and nonprofit organizations": UK Individuals plus Charities etc. |
| 15 Oct | D3 validation tolerance: plus or minus 5 percentage points on the 10-year change. Level tolerance still to set. |
| 15 Oct | W_min per person: half the median house price (`wmin_house_ratio` 1.0 to 0.5, patch pending). Three zones and one-sided pre-2006 test confirmed. |
| 15 Oct | D3 UK geography: Great Britain (WAS). |
| 15 Oct | Unit: per adult. Baseline = equal split of household wealth among adults; sharing parameter s (0 as-owned to 1 equal split) is a stated scenario. D3 target = share of adults in owner households. |
| 15 Oct | D5 calibration B: gross levy / GDP against corporation tax only (OECD 1200); trailing 5-year average, latest year as sensitivity. |

**Needed from you**
1. Confirm WID as primary for NLD and DNK (reversing the Moatsos and Abildgren supersessions) and for CHE from 1950.
2. D5 year basis: confirm trailing 5-year 2020-24 = 3.08%, sensitivity 3.47%.
3. D1 per-run minimum overlap 20 and pooling weight = retained overlap years (not sensitive; can be fixed now).
4. D3 level tolerance; confirm three zones and the one-sided pre-2006 test.
5. CIT owner-share sweep values (spec open item 2); evidence (one German estimate, about 49% owners) supports 100%, 50%, 25%.
6. Maximum interpolation gap (spec open item 4); default 10 years. Needs the interpolation flags.
7. D4 year and category mapping (2024, 58.8% rest of world proposed).
8. `mc_gdp` stand-in: flagged grade C World Bank for non-UK years after 2016, UK from ONS, or wait for K-Z.
9. TOML patch `wmin_house_ratio` 1.0 to 0.5; `adults_m` 52.0 vs 16+ label.

**Per-adult unification: open items**
- Model unit: the Advani, Bangham and Leslie (2021) shares rank families, wealth per adult within the family; the TOML labels cells as top fractions of adults. Re-express on an adult basis (their appendices give an individual version) or flag.
- Adults per household by tenure (WAS or EHS tables) and the adult age cut-off.
- As-owned sensitivity for property is not buildable from WAS (main residence and physical wealth split equally among adults over 16; pensions individual).
- Within-couple gap: equal-split treats couples as symmetric; single women hold less than single men in every group.
- Spousal transfer treatment under the WDT (mechanism papers); carer and disability variables in WAS for the net-change display.

## 10. Data to supply or obtain, with links

Links are those seen in earlier sessions. If a hashed gov.uk asset link has gone stale, use the landing page.

| Priority | Item | What to send | Links |
|:---|:---|:---|:---|
| 1 | WID API pull (replaces `1a`/`1b`) | Add PRT (and CAN if wanted); per-year interpolation flags; `ahweal` j with quality; top 1% and 0.1% shares; NOR definition check | [data](https://wid.world/data/), [codes dictionary](https://wid.world/codes-dictionary/) |
| 1 | Corporation Tax statistics 2025 data tables | ODS from the page | [CT statistics 2025](https://www.gov.uk/government/statistics/corporation-tax-statistics-2025) |
| 1 | HMRC IHT Table 12.1 (and 12.4 if it exists) | ODS | [IHT page](https://www.gov.uk/government/statistics/inheritance-tax-liabilities-statistics), [Table 12.1](https://assets.publishing.service.gov.uk/media/6a61fe84243ee000f7127e8b/table_12_1_final.ods) |
| 2 | ONS population by single year of age, or 16+/18+, UK, 1971 onwards | Re-export (Nomis may start at 1991 for this dataset) | [mid-2017 bulletin](https://www.ons.gov.uk/peoplepopulationandcommunity/populationandmigration/populationestimates/bulletins/annualmidyearpopulationestimates/mid2017), [UK/E&W/Scotland/NI estimates dataset](https://www.ons.gov.uk/Peoplepopulationandcommunity/Populationandmigration/Populationestimates/Datasets/Populationestimatesforukenglandandwalesscotlandandnorthernireland) |
| 2 | Adults per household by tenure | EHS or WAS table | [tenure trends collection](https://www.gov.uk/government/statistical-data-sets/tenure-trends-and-cross-tenure-analysis) |
| 2 | JST house-price documentation for ITA, ESP, PRT | Pages for those countries (PDF image-only: manual read or OCR) | [macrohistory.net/database](https://www.macrohistory.net/database/) |
| 3 | Kuvshinov-Zimmermann Data Appendix (tables E.1 to E.17) or UK market cap / GDP substitute after 2016 | Search "The Big Bang: Stock market capitalization in the long run" (CEPR DP 14468; MPRA 88581); no working URL found | none |
| 3 | WAS data dictionary (SN 7215) | UK Data Service record; tells which income, tax and NI variables exist | none found |
| 3 | Moatsos et al. data (NLD) | Email authors; not gate-critical now | [WP](https://shs.hal.science/halshs-04104429/file/WorldInequalityLab_WP202219.pdf) |
| 3 | Abildgren data (DNK) | On request from author; not gate-critical now | [article](https://ideas.repec.org/a/hhs/jdaecn/0021.html) |
| Low | UK saving by wealth group | Nothing found; candidates not opened | [IFS R71](https://ifs.org.uk/sites/default/files/output_url_files/r71.pdf), [WTC EP1](https://www.wealthandpolicy.com/wp/EP1_Distribution.pdf) |
| Ref | Already received (do not resend) | CGT tables 2 and 3, IHT 12.3, `NS_Table`, FT1101, EHS Ch.1, Saez-Zucman, HPSSA, OECD 1200 | [CGT page](https://www.gov.uk/government/statistics/capital-gains-tax-statistics), [Saez-Zucman data](https://gabriel-zucman.eu/files/SaezZucman2015MainData.xlsx), [appendix](https://gabriel-zucman.eu/files/SaezZucman2016QJEAppendix.pdf), [HPSSA 2017](https://www.ons.gov.uk/peoplepopulationandcommunity/housing/bulletins/housepricestatisticsforsmallareas/yearendingdecember2017/relateddata) |

## 11. Stale items still in other files

- `coverage_matrix_d1.csv` and `wdt_audit.json`: NLD "author list not confirmed", CHE "unverified (abstract only)", JPN 48, AUS 60, ITA 52, NOR 39, DNK 46 and NLD 25 on WID, FIN 23: all superseded by section 3.
- `provenance_register_d1/d3/d5/d6/d7`: D3 "sources located" now received; D5 "not retrieved" and D6 "ODS not readable" now received; D7 source text for ITA, ESP, PRT unchanged.
- `placeholder_register.md`: `house_median_gbp_m` row (mean claim); `adults_m` row.
- `variables_available.txt`, `variables.csv`: confirm after the API pull.
- `decision_log.md`: add the supersession reversal for NLD, DNK, CHE once confirmed.
- Spec step 5 (decision review: for each gate, pass, fallback or fail, and what the fallback changes in the claims) is not written; it depends on section 9.

## 12. Method points to carry into the model work

- **Timing.** WID series are mid-year averages; raw sources end-year. Half-year alignment needed before the identity route (D1 decision log 4).
- **Denominator.** Wealth ratios use net national income; JST uses GDP. Only drift in the ratio matters for the identity route (D1 decision log 5).
- **Flags to carry into every output.** UK holder shares 1998 to 2008 `carried`; D1 grades strict; D2 shape pooled and grade C for UK; D6 income profile placeholder; `mc_gdp` unverified; pooled c for failing countries (FIN, BEL, PRT) grade C.
- **No tuning to outcomes.** D3 is validation only; do not recalibrate on ownership.

## 13. Extractions possible now, no new data

OECD leg shares 2024 and 5-year averages; HMRC CGT and IHT band tables and receipts series to CSV; EHS tenure series to CSV; Saez-Zucman saving by class to CSV; HPSSA 2017 median into the D10 register; the section 3 gate table regenerated by script once the API pull lands.
