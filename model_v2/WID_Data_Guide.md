# WID data guide (WDT project) - status 2026-10-16

Purpose: tell any future agent what the WID download is, how to read it, and how it relates to the audit (D1, D8, D9). Read this before touching `wid_long.csv`.

## 1. Files
| File | Role |
|---|---|
| `wid_download.py` | Downloader. `discover` -> `catalogue.csv`; `fetch` -> `wid_long.csv`, `wid_coverage.csv`, `wid_wide_*.csv`, `manifest.json`, `raw/`. API logic ported from the official R package `wid` (get-requests.R, download-wid.R). |
| `wid_summarise.py` | Makes `wid_out/summary/` (8 small files) from `wid_long.csv`. |
| `wid_checks.py` | Makes `wid_out/summary2/`: dq run-lengths, balance-sheet identities, 1979/80 seam by component. |
| `wid_long.csv` (user's machine only, 361,536 rows) | Tidy long table. Too big for the project. |

Vintage 2026-10-16. 14 countries (AU CH DE DK ES FI FR GB IT JP NL NO SE US). BE and PT were not downloaded; PT is not in WID.

## 2. How to read a row
`series_key` = `<type letter><concept>_<percentile>_<age>_<pop>`, e.g. `apweal_p0p100_999_i`.
- Type: a average per person, m total, w ratio to national income, y ratio to GDP, s share, t threshold, g Gini, b inverted Pareto, n population, x exchange rate.
- Concepts used: pweal private wealth (household + NPISH); hweal household wealth (differs from pweal by up to ~18%; use pweal for D1); nweal national wealth; pwfin/pwnfa/pwdeb private financial, non-financial, debts (pweal = pwfin + pwnfa - pwdeb checks to <0.2% at latest-year medians); nwhou housing; nwdwe dwellings; nwlan land; nwbus business assets; nwagr agricultural land; nwodk other domestic capital; nwnxa net foreign assets; nwgxa/nwgxd foreign assets/liabilities; nwboo, cwres (see dictionary); nninc net national income; gdpro GDP; ndpro net domestic product; ptinc/diinc pre-tax/post-tax national income; fiinc fiscal income; pllin/pkkin labour/capital income; popul population.
- Ages: 999 all, 992 adults 20+, 996 20-64, 014, 156, 991, 997. Pop: i individuals, j equal-split adults, t tax unit. At p0p100 `i` and `j` are identical for hweal.
- Percentiles available for distribution: p0p50, p50p90, p90p100, p99p100, p99.9p100, p0p90, p90p99 (distribution series are mostly pop j, age 992, from 1800 for wealth but see section 4).

Columns: `value`, `unit`, `aux` (JSON `{"dq": 0-5}`), `is_extrapolated`, `vintage`, `preset`.

## 3. Facts learned from the first download
- **Units**: monetary series are constant local currency of the reference year, NOT PPP and NOT comparable across countries in level (latest-year medians: 75k to 5m per head). Ratios (w, y, s, g, b) are unit-free. Convert with lcusp (PPP) / lcusx (market) if levels are ever needed.
- **`aux.dq`** is the WID 0-5 quality flag (5 observed ... 0 regional average); `null` also occurs. `is_extrapolated` is False on every row: the extrapolation metadata is not returned by this API response, so IGNORE `is_extrapolated`. Use `dq` and, better, the start year of the underlying composition series (section 4).
- Use WID's own `w` series (`wpweal_p0p100_999_i` = W/NNI, `ypweal...` = W/GDP) for ratios; they match the ratio of the `a` series. nninc/gdpro ratio (`w` of gdpro) is 1.02-1.29.
- Mid-year averages; household sector includes NPISH.

## 4. Data start years (this is the provenance of "1800")
Headline pweal/nweal/nninc are annual 1800-2025 for 12 countries because pre-1980 values are back-cast from growth rates (WID TN 2026/03), NOT because data exists. First year of the private balance-sheet components (pwfin/pwdeb; pwnfa in brackets if different):

| AU | CH | DE | DK | ES | FI | FR | GB | IT | JP | NL | NO | SE | US |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1977 (1959) | 1980 | 1954 | 1973 | 1901 | 1980 | 1970 | 1920 | 1951 (1966) | 1970 | 1880 | 1976 (1979) | 1811 | 1913 |

All contiguous to 2025 (pwdeb/pwfin to 2025). Headline pweal starts: CH 1950, FI 1980, others 1800. nweal starts 1980 for CH and FI.
Housing (nwhou) starts: AU 1959, DE 1970, ES 1900, FR 1820, GB 1920, IT 1966, JP 1970, US 1913, others 1980 (NO 1979). Land/dwelling detail (nwlan, nwdwe) is mostly from 1979-1996.

## 5. D1 gate, on this data
Spec gate: at least 8 of 16 countries with at least 50 usable years.
- On headline pweal/nninc: 13 of 14 pass (FI 46 fails; CH 76).
- On honest start (first composition year): AU 49 fails, CH 46 fails, FI 46 fails; DK 53, NO 50 pass narrowly; 11 of 14 pass. The gate is met either way. BE and PT are absent (16 countries nominal, so 14 candidates).
- The runs are contiguous (no gaps), so the min-20-overlap rule does not bind within WID; it binds on the JST side (JST window coverage).

## 6. Known problem: 1979/80 seam in W/NNI
Same in this download as in the first: DE +22.9% (pweal/nninc), IT +7.8, JP +7.4, US +6.9, NL +5.3, GB +3.8, AU +1.5, FR +1.1, DK +0.5, CH -0.8, ES -2.2, NO -8.7, SE -8.4 (hweal: SE -10.8). It marks the splice between the old GWP-based pre-1980 series and the new 1980+ WID series. Options: (a) solve c on 1980+ only; (b) keep each side but drop the 1979->80 growth term from g_{W/Y}; (c) use only the post-start composition years from section 4. Decision pending (user). `wid_checks.py` output (`seam_growth.csv`, `identity_private.csv`) will show whether pweal itself or only some components jump.

## 7. Independence rule (spec principle 1)
WID wealth/income levels fix D1; JST supplies returns, prices and windows. Do not use WID returns or WID-derived asset-price growth to validate the identity-route c on the same sample. WID national income and JST GDP are different measures; nninc/gdpro ratio is 0.78-1.03 in the earlier file, so state which denominator was used.

## 8. Mapping to audit datasets
- D1: apweal/anninc/agdpro (or the w, y series), age 999, pop i, p0p100.
- D8: hweal distribution (s, a, t, g, b at p0p50 ... p99.9p100, age 992 pop j). Negative bottom-50 shares occur (min -0.109), so do not assume non-negative.
- D9 adults per head: npopul age 992 / age 999 (population 20+ ratio), ages 996, 014, 997 available. This is a 20+ convention, not 18+.
- D2/D4 composition and saving context: pw*/nw* series above.
- CH: private wealth 1950+ only; nweal 1980+. FI: 1980+ throughout.

## 9. Still unknown (do not assume)
- Per-series dq change points (needs `dq_runs.csv`).
- Whether pweal equals the component sum before the components start (needs `identity_private.csv`).
- Meaning of dq = null, and why dq 4/5 dominate pre-1950 rows in aggregate (back-cast flags).
- Whether the 0-5 flag matches the TN definition for this vintage.

## 10. Rules for future agents
1. Never use `is_extrapolated`. 2. Never call 1800 a data start. 3. Quote the vintage. 4. Re-run `wid_download.py fetch` for a new vintage, keep old raw files. 5. Ratios across countries; levels only within a country.
