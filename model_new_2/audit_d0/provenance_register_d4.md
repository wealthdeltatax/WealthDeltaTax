# D4 provenance and status (equity ownership and market capitalisation)

Date: 14 October 2026. Status: open-item pass done. Coverage census only; no series values extracted.
Companion: `coverage_matrix_d4.csv`. Model hook: per-year tranche shares in `levy_path` in place of the scalars `f_inc`, `f_attr`, `mc_gdp`.

## What was actually opened

| Source | Status | Opened |
|:---|:---|:---|
| ONS Ownership of UK quoted shares, 2022 and 2012 bulletins | verified | Full pages. Series start (1963), holder categories, anchor shares, CREST break. |
| ONS dataset "Share ownership time series" (id srs), CSV attached by the user (release 29 Jan 2026) | verified, extracted | 68 year-rows, 217 columns. Percent-of-equity block extracted to `uk_holder_shares_ons.csv` (28 survey years, 1963-2024). Grossed and ungrossed market-value blocks, and industry/FTSE splits, are present but not yet used. |
| ONS dataset "Ownership of UK shares" (reference tables, editions 2010-2024) | located, not read | Dataset page only. |
| Kuvshinov and Zimmermann, CEPR DP 14468 and the 2018 EHES WP 136 / MPRA 88581 version | verified, appendix not retrievable | Body text read to the tool's 100000-character limit (the last 18,312 characters and the Data Appendix were not returned). No data link on the MPRA page. Repository page returned an access-denied error. |
| Fed Z.1, FRED series for households and for rest of world | verified | Both annual, market value, 1945 to 2025. |
| Fed Z.1 table L.223 | partly | One 2018-2021 release; sector list only. |
| JPX Share Ownership Survey | partly | Archive pages list 2016-2025, with files shown only for 2015 and 2024; the Excel files were not opened. |
| Bundesbank sectoral financial accounts table | partly | One vintage covering 2020-2025; shows listed shares by holder sector with a rest-of-world split. |
| Eurostat nasa_10_f_bs (via an aggregator page) | partly | Series run 1995-2024 for the countries shown. Listed-share instrument and Norway/Switzerland not confirmed. |
| OECD, Owners of the World's Listed Companies (2019) | verified | Coverage and categories. |

## Findings

1. **UK holder shares.** The ONS series starts in 1963 with 11 holder categories. Individuals held 54.0% in 1963, 11.5% in 2010 and 10.8% in 2022; rest of the world 57.7% in 2022. Survey years are selected, not annual. The time-series workbook exists with a direct link but has not been read.
2. **UK data-quality flags to carry into every output.** The 1998 move to CREST broke the series. The 1998-2008 split of pooled nominee accounts was carried forward from a 1997 register analysis, so that period is an assumption (label it `carried`, not `interp`). The 2012 method change moved other financial institutions. CREST covers about 80% of value, and pooled accounts (50.6% of value in 2022) are allocated from sampled registers. Coverage is UK-incorporated, LSE-listed shares only.
3. **US holder shares.** Resolved: households and nonprofits, and rest of world, both annual at market value from 1945 to 2025. This gives a long foreign-share and household-share series for the US.
4. **Euro area and others.** Eurostat annual financial balance sheets begin in 1995 for the EU countries shown, so holder shares for those countries start in 1995 at best. The Bundesbank table shows the needed split (listed shares by holder sector, rest of world separate) but only for 2020-2025 in the file opened. Long history for Germany, France, Italy, Spain, the Netherlands, Norway and Switzerland is not confirmed; grade C fallback applies unless found.
5. **Japan.** The JPX survey is annual and offers both unit-base and market-value tables, but only 2015 onward was visible; categories are inside the Excel files.
6. **Market cap / GDP.** Kuvshinov and Zimmermann cover all 16 countries in scope (plus Canada), 1870-2016. Per-country first years and any public release are not retrievable with the tools here. Japan starts in 1899 and its early years assume a constant share.
7. **Attribution shares** remain unobserved and stay a swept parameter.

## Still open (and who can close it)

1. **ONS workbook.** Closed. Survey years are 1963, 1969, 1975, 1981, annual 1989-94 and 1997-2004, then 2006, 2008 and biennial to 2024. The largest gap is 8 years (1981 to 1989), inside the 10-year default. Category shares sum to 100 within rounding. The 2008 to 2010 step in institutional shares (pension funds 12.8 to 5.6, insurers 13.4 to 8.8, unit trusts 1.8 to 8.8) is the end of the carried-forward 1997 pooled-account split, so use pre-2010 institutional shares only as `carried`. Individuals, the likely household tranche, barely move across it (10.2 to 10.6), though pooled holdings may still bias them. The grossed market-value columns have no unit in the file header and were not summed (a column sum mixed sub-tables).
2. **Kuvshinov and Zimmermann appendix and data.** Re-tried 15 Oct, not closed. Read past the earlier cut-off with the fetch offset on the CEPR DP 14468 PDF, the MPRA 88581 PDF and the author-site copies (dkuvshinov.com, two versions). All end at the references or the conclusion; none contains the Data Appendix, so tables E.1-E.17 are in a separate online appendix. Bonn dissertation and 1library copies are blocked (access denied, login wall). No public dataset link found by search (MPRA, CEPR, UPF repository, Zenodo/GitHub/ICPSR queries). Needs the appendix PDF or the dataset from you, or the authors.
3. **Holder-share history outside the US and UK.** Candidates not yet opened: Banque de France and Banca d'Italia flow of funds, Statistics Norway, Swiss National Bank, older JPX archives, Bundesbank long series.
4. **Market cap / GDP for 2017 onward.** Not sourced.
5. **Household tranche definition.** Closed (decided 15 Oct): match the US so the data are comparable. UK household tranche = ONS "Individuals" + "Charities etc.", the nearest equivalent of Z.1 "households and nonprofit organizations" (column `household_tranche_z1_equiv` in `uk_holder_shares_ons.csv`; 1963 56.1, 2022 11.5, 2024 12.0). This is my reading of the instruction; confirm. Caveats: (a) Z.1 households hold directly only, with mutual funds, pensions and insurers as separate sectors, as ONS does with unit trusts and funds, so the two are alike in scope but not identical. (b) Z.1 levels are in $ millions and need a total corporate equities denominator (L.223 total) to become shares. (c) Z.1 covers US-issued equities held by all holders, and ONS covers UK-incorporated LSE-listed shares only. (d) UK pre-2010 shares for pooled nominee accounts are `carried`; individuals move little across the break, but treat 1998-2008 as less certain. (e) The ONS charities category may include some bodies Z.1 classes elsewhere.

## Gate (spec): UK history from first available year; other countries by era with grade C fallback

UK passes on span (1963 on) conditional on the survey-year spacing; interpolation must respect the 10-year maximum gap. The US passes comfortably (1945-2025). The euro-area countries pass only from 1995. The rest use the fallback.

## Cross-check against the model TOML (15 Oct)

The TOML sets `f_attr + f_inc = 0.588`, citing ONS 2024 (rest of the world). That equals the 2024 rest-of-the-world value in `uk_holder_shares_ons.csv` (58.8). `f_inc` = 0.10 is a stated placeholder (sweep 0.02 to 0.20) because the attribution split is unobserved. `mc_gdp` = 0.876 uses 2.54tn pounds (end 2024) over 2.90tn.
