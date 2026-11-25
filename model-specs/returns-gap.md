# Model v3: bridging the return data from 2019 to 2025 (brief 042r)

Status: research result; no value is chosen, no splice is made, nothing in the register or the generator is edited. Date 2026-11-18. Script `returns/gap.py` (run `python3 -I gap.py` in `results/returns/`); results `returns/gap_results.json`. UK only. Pages were read through the fetch tool on 2026-11-18.

## 1. What it says
1. **JST Release 6 is licensed CC BY-NC-SA 4.0** (R6 documentation, July 2022). The repo may hold, cite and share the file and the json for non-commercial use with attribution, under identical licence terms. It may not relicense them, and commercial data providers may not integrate them. The repo has no LICENSE file, so the share-alike condition is not yet met (section 2).
2. **No later release was found.** The NBER page and the author's page state no release number. macrohistory.net itself was not on the fetch allowlist, so Release 7 stays open.
3. **A licensed 2020 to 2025 wealth return cannot be built from open series in this session.** CPI (ONS) and house prices (ONS and HM Land Registry) are Open Government Licence v3.0 and were read. Equity total return (FTSE) needs an LSEG licence. Gilt yields are open (Bank of England, OGL) but no yield values could be read here. Rents have a licensed series but no annual values were read.
4. **One year can be filled from held data: 2020.** JST's own 2020 asset returns, weighted by JST's composition (036r section 6), give a real wealth return of **-0.44%** (estimated, error about 1 point against JST's own years, section 4).
5. **The six-year effect is bracketed, not computed.** Adding 2020 moves the mean from 4.74 to 4.70. Adding 2021 to 2025 at a housing-only proxy gives 4.61 and an 80% band 3.34 to 5.88 (from 3.41 to 6.07). Under an illustrative 3 or 6 point stress on those five years the mean is 4.49 or 4.37. The band moves by 0.1 to 0.4 points at the low end; SD stays 8.1 to 8.3 and lag-1 0.29 to 0.32 (section 5). None of these is a wealth return for 2021 to 2025.
6. **The housing proxy has a timing problem.** The ONS index is December on December; JST's 2020 house price change is 2.83% (capital gain, nominal) against 8.5% December on December. JST's series is not year-end, so a splice on calendar year-end would shift returns by a year's lag. That alone blocks a splice (section 4).

## 2. Licence of the JST data
| Source read | What it says (quoted) | URL | Accessed |
|---|---|---|---|
| JST Release 6 documentation, "Release 6", "July 2022" (copy on the authors' page host) | "We grant every user at no cost a license (see below) to use and/or share the licensed material, in whole or in part," "provided that it is for non-commercial (e.g., academic) purposes," "Commercial data providers are thus strictly forbidden to integrate all or parts of the dataset", "provided that it may only be shared under identical license terms." Licence: "AttributionNonCommercial-ShareAlike 4.0 International License." | https://sfff5b3ac9317c4be.jimcontent.com/download/version/1676279836/module/9834516169/name/JST_documentationR6.pdf (first 100,000 of 570,066 characters) | 2026-11-18 |
| NBER, JST Macrohistory page | "no-cost open access under a license"; commercial providers barred from integrating or selling; "Source Jordà, Schularick, Taylor"; no release number; links the full terms on macrohistory.net | https://www.nber.org/research/data/jorda-schularick-taylor-macrohistory | 2026-11-18 |
| macrohistory.net/database and /data | **not read**: not on the fetch allowlist | | |
| Oscar Jordà's data page | no terms stated; names the NMA 2016 paper for the data description | https://sites.google.com/site/oscarjorda/home/macrofinancial-data | 2026-11-18 |

**Citation** (R6 documentation, as quoted): cite Jordà, Schularick and Taylor (2017), Macrofinancial History and the New Business Cycle Facts (NMA 31); for asset-price and rate-of-return data also Jordà, Knoll, Kuvshinov, Schularick and Taylor (2019), The Rate of Return on Everything, QJE 134(3) 1225-1298 (the bib key `JordaEtAl2019` exists; the 2017 paper has no key in `references.bib`).

**What the repo may do** (not legal advice; for the author to confirm): keep `data/rates/JSTdatasetR6.xlsx` and `model_v2/jst_r6.json`, cite as above, and share them non-commercially under CC BY-NC-SA 4.0. Two consequences. (a) The files and adaptations of them (the 036r series, tables built on JST returns) are share-alike: a notice stating the licence should sit beside them; the repo has no LICENSE file and no such notice was found. (b) The licence is non-commercial: if the site or the papers are ever offered commercially, JST-based material needs the authors' consent or removal. The terms page itself should be re-read once macrohistory.net is reachable, and the register note "licence unconfirmed" (I-D1a) can then be replaced by "CC BY-NC-SA 4.0 (R6 documentation, read 2026-11-18)".

**Later release:** none found (search and both pages read). A new release would state its sample end year; R6 is documented to 2020 for the asset series and to 2019 for the wealth return.

## 3. Candidate series, 2020 to 2025
| Series | Coverage and frequency | Licence statement (page read) | Exact table or file | Accessed | Used? |
|---|---|---|---|---|---|
| ONS CPI index, all items, 2015=100, ID D7BT | annual and monthly series from 1988; annual averages 2018 to 2025 read | "All content is available under the Open Government Licence v3.0, except where otherwise stated." | https://www.ons.gov.uk/economy/inflationandpriceindices/timeseries/d7bt (annual table; release 18 Nov 2026) | 2026-11-18 | **Yes** (deflator) |
| UK HPI average price, annual change, December releases | monthly, England, Scotland, Wales, NI | "licensed under the terms of the Open Government Licence v3.0 except where otherwise stated" (Crown copyright) | HM Land Registry summaries, Dec 2021, 2022, 2023, 2024, 2025 (gov.uk/government/statistics/uk-house-price-index-for-december-YYYY/...-summary-december-YYYY); Dec 2020 from the ONS bulletin https://www.ons.gov.uk/economy/inflationandpriceindices/bulletins/housepriceindex/december2020 | 2026-11-18 | **Yes**, December on December, as first published |
| ONS Private rent and house prices, UK (PIPR) | rents monthly from January 2015; a linked series 2005 to Feb 2025 | "The content is available under the Open Government Licence v3.0" | https://www.ons.gov.uk/economy/inflationandpriceindices/bulletins/privaterentandhousepricesuk/february2026 | 2026-11-18 | **No**: licence fine, but no annual 2020 to 2025 values were on the page; rent return held at JST's 2020 value (assumption) |
| FTSE All-Share total return (LSEG) | daily, index data | "Use and distribution of LSEG data requires a licence from LSEG and/or its licensors." (LSEG insight page, which also carries no All-Share return) | https://www.lseg.com/en/insights/ftse-russell/non-us-and-emerging-equity-markets-took-the-leadership-baton-in-2025 | 2026-11-18 | **No**: listed, licence required |
| Bank of England Statistical Database, gilt yields | daily and monthly | "Reproduction of data in the Database is subject to the terms of the UK Open Government Licence" (selected exchange rate series excluded) | https://www.bankofengland.co.uk/legal; yield values not retrieved (database link over the fetch tool's length limit) | 2026-11-18 | **No**: licence allows, but no values read, so no gilt return |
| DMO historical average daily conventional gilt yields | monthly averages from April 1998 | "Use of these data assumes compliance with the DMO's terms of use"; "© Crown Copyright" (terms page not read) | https://dmo.gov.uk/data/ExportReport?reportCode=D4H (report page only, no values) | 2026-11-18 | **No**: terms not read, no values |
| Nationwide house price index; Land Registry full file | | not read | | | **No**: listed only |
| JST Release 6 asset series to 2020 | annual, 1870 to 2020 (asset series), 2019 (wealth) | CC BY-NC-SA 4.0 (section 2) | `data/rates/JSTdatasetR6.xlsx`, `model_v2/jst_r6.json` (eq_tr, housing_tr, bond_tr, bill_rate, cpi, 2020) | held | **Yes** (2020 only, and the composition) |

Two limits. The fetch tool read each gov.uk or ONS page in turn; the full HPI download tables were not opened, so annual HPI values are the December headline changes as first published and later revised. And an index total return for equities or gilts needs the dividend or coupon stream; the open series above give no such stream.

## 4. Annual real returns, 2020 to 2025
All rows are **estimates**. Real return = (1 + nominal return) / (1 + CPI inflation) - 1, CPI inflation = change in the ONS annual average index.

| Year | CPI avg index (D7BT) | CPI inflation | HPI Dec on Dec | Housing nominal (HPI + 2.28 rent return) | **Housing-only real (estimate)** | Wealth real (estimate) |
|---|---|---|---|---|---|---|
| 2019 | 107.8 | | | | | 6.9 (JST, actual, real) |
| 2020 | 108.7 | 0.83% | +8.5% | 10.78% | 9.86% | **-0.44% (JST composition; estimate)** |
| 2021 | 111.6 | 2.67% | +10.8% | 13.08% | 10.14% | not computable |
| 2022 | 121.7 | 9.05% | +9.8% | 12.08% | 2.78% | not computable |
| 2023 | 130.5 | 7.23% | -1.4% | 0.88% | -5.92% | not computable |
| 2024 | 133.9 | 2.61% | +4.6% | 6.88% | 4.17% | not computable |
| 2025 | 138.4 | 3.36% | +2.4% | 4.68% | 1.28% | not computable |

**Method.** Housing nominal = December on December HPI change plus a rent return of 2.28%, held at JST's 2020 `housing_rent_rtn` (assumption; no 2021 to 2025 rent values were read). 2020 wealth: risky = 0.35 equity + 0.65 housing, safe = half bonds and half bills (both JST 2020), wealth = 0.85 risky + 0.15 safe, with the 1990 to 2019 median weights of `returns-method.md` section 6; the same recipe applied to 2010 to 2019 reproduces JST's own real wealth return to within 0.1 to 1.5 points (2019: 5.9 against 6.9; 2018: -2.0 against -3.5; 2011: -3.5 against -3.0), so the 2020 estimate carries about 1 point of error. Equity (2020: -9.44%), housing (5.11%), bonds (5.75%), bills (0.04%) and CPI (194.848 over 193.11) are JST R6 2020 values.

**Hand check, 2022:** (1 + 0.098 + 0.0228) / (121.7 / 111.6) - 1 = 1.1208 / 1.09050 - 1 = 2.78%. The script prints 2.78%.

**Timing caveat, shown by the one year where both exist.** JST's 2020 housing return is 5.11% nominal (capital gain 2.83% plus rent 2.28%). The December on December ONS figure for the same year is 10.78% on the same basis. JST's house price is not a year-end series (its 2020 change is close to a year-average change), so the proxy shifts returns by about half a year: the 2020 to 2021 housing boom enters 2020 in the proxy and 2021 in JST. The 2020 proxy for housing is 5.7 points above JST's own, so the proxy rows are not comparable with the 1871 to 2019 series. They are shown to give the shape of the period (a 2022 real fall for bonds and for housing after inflation, 2023 the weakest housing year), not as inputs.

## 5. Effect on the level 2 band of I-D1a
Same method as `returns-method.md` section 4: sample arithmetic mean, SE = sd / sqrt(n) x sqrt((1 + rho) / (1 - rho)), 80% band = mean -/+ 1.2816 SE. S0 reproduces the register (4.74, 8.22, 0.30, 3.41 to 6.07).

| Scenario | n | Mean | SD | Lag-1 | SE | 80% band | Geometric |
|---|---|---|---|---|---|---|---|
| S0 JST to 2019 (register) | 117 | 4.74 | 8.22 | 0.30 | 1.04 | 3.41 to 6.07 | 4.42 |
| S1 + 2020 (JST composition estimate) | 118 | 4.70 | 8.20 | 0.30 | 1.03 | 3.38 to 6.02 | 4.38 |
| S2 S1 + 2021 to 2025 at the housing-only proxy (not a wealth return) | 123 | 4.61 | 8.11 | 0.29 | 0.99 | 3.34 to 5.88 | 4.30 |
| S3a S2 with 2021 to 2025 3 points lower (illustrative stress; assumption) | 123 | 4.49 | 8.16 | 0.30 | 1.01 | 3.20 to 5.78 | 4.17 |
| S3b S2 with 2021 to 2025 6 points lower (illustrative stress; assumption) | 123 | 4.37 | 8.26 | 0.32 | 1.04 | 3.04 to 5.69 | 4.04 |

Reading. Mean: -0.04 (2020 alone), -0.13 (all six, housing proxy), -0.25 to -0.38 under the stress. SD: -0.02 to +0.04. Lag-1: -0.01 to +0.02. The band's width is stable (2.53 to 2.66 points); it shifts down by 0.03 to 0.37 at the low end and 0.06 to 0.38 at the high end. **The rule for what the missing years would do**: adding five years at a mean return m moves the mean by 5/123 x (m - 4.70); m = 0 gives -0.19, m = 2 gives -0.11, m = 6 gives +0.05, m = 8 gives +0.13. The five years would need a real wealth return of about 4.7% a year to leave the mean unchanged. Each of S2 and S3 is bracketed by that line; none replaces a measured series.

Why not more. The effect on the true mean is small against a standard error of 1.04, and the generator's central parameters (mean 4.74, SD 8.22, lag-1 0.30) would move inside their own bands for any plausible 2021 to 2025 outcome. The check against 2020 to 2025 (the crash and rebound, the 2022 inflation and gilt shock, the 2022 to 2024 house price fall) needs the equity and gilt series; the housing leg is above.

## 6. What stays uncovered
- Equity total return 2021 to 2025: FTSE data is licensed; no licence-free proxy was read.
- Gilt and bill returns 2021 to 2025, including the 2022 gilt shock: the Bank of England series is open but no yield values were retrievable here, and a total return also needs duration and coupon.
- Rents 2021 to 2025: ONS PIPR is open but no annual values were on the pages read; the 2.28% rent return is held at JST 2020.
- A year-average house price series on the JST basis, to remove the timing mismatch.
- The wealth composition after 2019 (weights are the 1990 to 2019 medians).
- JST release number and the macrohistory.net terms text.
- The 2020 wealth estimate is one estimate with about 1 point of error, and 2020 is the last JST asset year; 2019's wealth return in the register is 6.9% real.

## 7. Checks
- `gap.py` runs under `python3 -I`; S0 reproduces 4.742, 8.219, 0.303, 3.411 to 6.074 (register I-D1a, I-D1b, I-D1b2).
- Hand recomputation of 2022 from the cited series (section 4) agrees with the script (2.78%). Also hand: 2023: (1 - 0.014 + 0.0228) / (130.5 / 121.7) - 1 = 1.0088 / 1.07231 - 1 = -5.92%.
- CPI inflation matches JST for 2020 (ONS annual average 0.83% against JST 0.90%): the CPI bases agree.

## 8. For the author and guru
- Add a licence notice for the JST files (and derived tables) and confirm the non-commercial condition fits the site; consider a LICENSE file for the repo.
- Provide an LSEG-licensed or other licence-clear equity and gilt series for 2020 to 2025, or accept that the level 2 band rests on 1871 to 2019 (plus 2020 if wanted). The effect of the five years is bounded by section 5.
- Decide whether I-D1e (gap 5, 6, 6 years) should read "2020 estimated, 2021 to 2025 open" and whether the I-D1a licence note should change (the register is not edited here).
