# WDT data audit: progress pass of 15 Oct 2026 (afternoon)

Companion to `WDT_audit_summary_open_items.md`. Nothing here has been written into the TOML or the other registers. "Verified" means a page or paper was actually read in this pass; ODS/XLSX files could not be read (proxy blocks assets.publishing.service.gov.uk; binary files come back unreadable).

## 1. D1: per-run parameters (decision 4), computed from `d1_overlap_runs.csv`

Rule tested: drop any run whose overlap with the wealth series is shorter than a minimum, then sum the remaining overlap years (LEVY set).

| Country (source) | all runs | min 20 | min 30 |
|:---|---:|---:|---:|
| CHE (Baselgia) | 79 | 56 | 56 |
| DEU (WID) | 112 | 98 | 98 |
| NLD (Moatsos) | 84 | 70 | 70 |
| DNK (Abildgren) | 132 | 132 | 112 |
| all other countries | unchanged | unchanged | FIN and NLD-WID drop to 0 (already failing) |

Result: the 50-year gate outcome is identical at minimums of 10, 20 and 30 years. Only runs CHE 1-2, DEU 2 and NLD-Moatsos 1 are dropped at 20. Recommendation: minimum 20, pooling weight = retained overlap years. This is not sensitive, so it can be fixed now.

## 2. D1: source verification (opened this pass)

| Item | Finding | Effect |
|:---|:---|:---|
| NLD | Authors are Toussaint, de Vicq, Moatsos, van der Valk. WID WP 2022/19 (HAL halshs-04104429); European Economic Review 178 (2025), DOI 10.1016/j.euroecorev.2025.105099. Household wealth 1854-2019, SNA basis, net national income denominator. Annual 1880-1938 (historical accounts), benchmarks 1938/1946-52/1958/1960 with 1947-1969 interpolated, annual 1970-2019. Pensions reported separately ("semi-private"). No data link found. | NLD verified at conference-paper level; correct author list in the matrix. Interpolation share to carry as flag. |
| DNK | Abildgren: Nationalbanken WP 92 (2015); Nationaløkonomisk Tidsskrift 2016(1). Annual 1845-2013, national wealth (non-financial assets + net foreign assets; oil and gas 1950-2013 only), no private/government split. Data on request from the author. | DNK has no household-concept series beyond WID 1973-2018 (46 years, fails). Abildgren is a flagged concept proxy, grade C only. |
| CHE | Baselgia and Martinez: WID WP 2020/28 and CESifo WP 9976. Private wealth, NPISH included, excludes PAYG pensions and durables, 1900-2018 / 1900-2020. Annual from 1981; earlier years extrapolated from tax and pension data ("annual in form only"). Downloadable at wid.world. | Definition matches WID (same gaps as other rows). Pre-1981 is interpolated: flag. |
| PRT | Cardoso and Cunha: Banco de Portugal WP 4/2005, 1980-2004, financial assets and liabilities plus housing. | Fail confirmed. Fallback pooled c, grade C. |
| JPN | Bauluz 2017 update and Technical Note 2020/14: private wealth starts 1970. The 2026 WID note lists Piketty-Zucman Japan coverage as 1960. | Unresolved: needs the WID download. JPN stays 48 (fail) until checked. |
| WID start years (2026 note, PZ coverage) | DEU 1870, FRA 1700, GBR 1700, USA 1770, ITA 1965, ESP 1900, SWE 1810, AUS 1970. The 2017 update gave AUS 1960 and ITA 1966. | AUS: if the series starts 1970, LEVY overlap is 50, exactly at the gate with no margin. Check in the download. |

Gate on household concept after this pass: 10 of 16 (AUS, DEU, ESP, FRA, GBR, ITA, SWE, USA verified at WID level, plus NLD and CHE), 11 only if DNK on national wealth is allowed as grade C. Still at or above 8. AUS (possibly 50) and ITA (52) are the marginal ones.

## 3. D2: numbers read

- Saez and Zucman (2016): bottom 90% about 3%, next 9% about 15%, top 1% about 20-25% of pre-tax income; saving is net of asset price changes (synthetic), includes retained earnings; top 0.1% not seen. Appendix data file `SaezZucman2015MainData.xlsx` (Table B33) not readable here.
- Fagereng et al. (NBER w26588): net saving rate "flat around seven percent" over income; gross rate rises to 35% for the top 1% (includes capital gains). Normalised over income; saving over wealth is Figure 10d (no numbers read).
- Mian, Straub, Sufi (NBER w26941): by INCOME percentile: top 1% over 40%, next 9% 20%, 51-90 12%, bottom 50% about zero. Net of valuation effects.
- UK: no saving-by-wealth tabulation found (Resolution Foundation "Before the fall" 2025 splits saving by income quintile; passive gains explain 60% of average family wealth growth). The D2 UK gate stays unmet; pooled shape, grade C.
- Method note: all three sources are saving over income, not net drawdown over wealth. The model's c needs wealth/income by group to convert.

## 4. D3: sources located

English Housing Survey live table FT1101 (S101) "Trends in tenure" (ODS, updated 9 July 2026, data to 2024-25) at gov.uk/government/statistical-data-sets/tenure-trends-and-cross-tenure-analysis; Chapter 1 Trends in tenure 2013-14 Figure 1.1 bars 1918, 1939, 1953, 1961, 1971, 1981, 1991, 2001, 2013-14, with Annex Table 1 behind it. Text values 1918 25%, 1953 32%, 1961 43%, 1971 51%, 2013-14 63%.

## 5. D4: tranche mapping, checked against `uk_holder_shares_ons.csv`

- `household_tranche_z1_equiv` equals individuals + charities_etc in every row (max difference 4e-15).
- Rest of world: 56.3 (2020), 57.7 (2022), 58.8 (2024); three-edition mean 57.6. Recommend 2024 (58.8), year-matched with end-2024 `mc_gdp`. Matches the TOML's 0.588.
- Survey-year gaps: 6, 6, 6, 8 (1981-89), then 3 (1994-97), annual or biennial after. Largest 8, inside the 10-year default.

## 6. D5 / D6: what was and was not obtained

- OECD 1200, UK, all-government, 2015-2024 (Revenue Statistics 2025): NOT retrieved (country note PDF refused, DBnomics API refused, country tables page lacks the UK). Earlier DBnomics central-government series (April 2024 vintage), 1973-2022, was read: 2018-22 = 2.549, 2.305, 2.393, 2.916, 3.105.
- HMRC definitions confirmed. "Corporate Taxes" = corporation tax (onshore and offshore) plus bank levy, bank surcharge, residential property developer tax, energy profits levy, electricity generator levy.
- HMRC CGT (latest 2024-25): 584,000 taxpayers, gains 127.3bn, liabilities 24.2bn; gains of 5m+ are under 1% of taxpayers and 45% of CGT. Tables 2 and 3 (size of gain; by income) are ODS only, not readable.
- HMRC IHT 2023-24: 30,400 taxpaying estates, 7.03bn; 2m-7.5m band 3,156 estates, effective rate 25%; over 10m 220 estates, 18%. Table 12.3 (assets by net estate) ODS not readable.

## 7. D10 placeholders: findings

- `adults_m = 54.0`: inconsistent with `pop_per_adult = 1.27`. ONS mid-2017 UK population 66,040,229 / 1.27 = 52.0m. ONS projected 18+ for 2018 is 52.4m; 16+ in mid-2017 is about 53.5m (derived). 54.0 fits only a 16+ count around 2018-19. Suggested: 52.0 for consistency, or state it as a 16+ figure.
- `house_median_gbp_m = 0.225`: UK HPI mean December 2017 was 226,756 (England 243,582), so 0.225 is a MEAN near the UK average, not a median. A median (HPSSA, year ending Dec 2017) was not retrieved. Label stays placeholder.
- `mc_gdp`: do not use the World Bank market-cap series for the UK (different scope; the series seen ends 2014 at 115.7% and CEIC shows 70.4% for 2023 against the model's 87.6% for 2024). For the UK, divide the ONS grossed market-value series by GDP; use World Bank only for non-UK countries, grade C.
