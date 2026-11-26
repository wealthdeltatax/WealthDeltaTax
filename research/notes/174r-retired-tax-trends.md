# 174r: Trends in the six retired taxes

Accessed 2026-11-26; completed 2026-11-26 (brief 175r) from the held IFS workbook. Historical descriptive evidence; no recommendation on indexation.

Status: complete for the retired-tax series. The annual series for all six taxes, 1978–79 to 2027–28, come from `data/rates/Revenue composition spreadsheet.xlsx` (IFS, "Composition of UK revenue") and are computed by `research/tables/174r-evidence/retired_tax_series.py`; the statistics are computed by `retired_tax_stats.py`. Statistics use the sheet's outturn years only (1978–79 to 2020–21, 43 years); 2021–22 to 2027–28 are flagged forecasts (OBR EFO March 2023 and later) and are shown only as end points.

## 1. Summary

Shares of UK GDP, cash basis, mean of the first three against the mean of the last three outturn years (1978–81 against 2018–21), percentage points; the verdict rule is in section 3.2.

- **Corporation tax** 1.91 to 2.56 (rose; the sheet's total, which includes offshore); largest swing of the six in level: from 3.41 in 1989–90 to 1.64 in 1981–82. Volatility (sd of annual change) 0.27 points.
- **Capital gains tax** 0.19 to 0.46 (rose); volatility 0.08; the lowest year 0.09 (1993–94), the highest 0.53 (2020–21).
- **Inheritance tax** 0.18 to 0.24 (about steady: +0.06); the smoothest series (volatility 0.017).
- **Stamp duties** (property transaction taxes and share stamp taxes together, as ruled) 0.24 to 0.70 (rose); from 1999–00 the property part rose (0.33 to 0.54) and the share part fell (0.33 to 0.17).
- **Business rates** 1.75 to 1.26 (fell); 2.11 in 1982–83, 0.96 in 2020–21 (pandemic reliefs).
- **Council tax** 1.32 to 1.62 (rose); the series is smooth (volatility 0.10) and trends up by 0.06 points a decade.
- **The six together** 5.60 to 6.85 (+1.25), between 4.89 (1993–94) and 7.61 (1988–89), volatility 0.38; the flagged forecast for 2027–28 is 8.70. Their sum is not constant: it moved by up to about 2.7 points between a trough and a peak.
- **Asset prices.** The annual change in each share has a weak to moderate positive correlation with the annual change in the UK house price to GDP ratio (−0.19 to +0.30 for single taxes, +0.50 for the six together; 42 years) and with the equity price to GDP ratio (−0.34 to +0.56). With 42 observations and policy breaks in every series, none of these is stable evidence of proportionality to household wealth.
- The evidence does not show the six taxes following household wealth one for one, and it does not show them staying at a fixed share of GDP either: each has its own base, policy history and timing. See section 5 (no recommendation).

## 2. Definitions, sources and comparability

The core annual series below are from OBR Working Paper 15, *The evolution of public sector receipts over the past decade* (April 2020), tables 2.3, 2.4, 2.5 and 3.4. These are receipts as a share of UK GDP, with council tax specifically Great Britain receipts divided by UK GDP. The OBR defines movements as a combination of changes in the tax base relative to GDP and changes in the effective tax rate.

Definitions:
- **Corporation tax:** OBR onshore corporation tax, excluding offshore oil and gas revenues; not identical to HMRC's broad cash-receipts "business taxes" grouping.
- **Council tax:** Great Britain receipts, per cent of UK GDP.
- **Business rates:** non-domestic rates; local government / national accounts coverage and relief treatment matter. OBR gives a trend statement for 2007–08 to 2018–19 and later EFO shares.
- **CGT:** cash receipts; the OBR shifts chargeable gains by one year for its base comparison. Tax receipts are affected by disposal timing and policy forestalling.
- **Stamp duty:** the historical OBR property transaction tax series includes UK property transaction taxes. By 2018–19 Scotland and Wales had moved to LBTT and LTT; the OBR series accounts for the devolved tax transition. Stamp duty on shares is separate and fell by 0.1 percentage points of GDP over 2007–08 to 2018–19.
- **IHT:** HMRC receipts as a share of GDP. It is not included as a separate annual table in OBR WP15; HMRC annual bulletin gives 2006–07 and 2025–26 endpoints.

Cash receipts and accrued public-finance receipts differ, especially for CGT, CT and timing-sensitive taxes. The latest HMRC annual bulletin states that receipts are cash-based and that 2025–26 values are aligned to HMRC's annual report; OBR's national accounts time-shifted CT series is a different basis. Do not join these without a reconciliation.

## 3. Each tax as a share of GDP

Source: `research/tables/174r-evidence/retired-tax-gdp-annual-full.csv` (719 rows: 10 series; cash basis 1978–79 to 2027–28 and national-accounts basis 1999–00 to 2027–28; the sheet, row, row label, flag and the sheet's own footnotes are in each row). Statistics: `retired-tax-stats.csv`. Values are percent of GDP, four decimals in the CSV, rounded here. The sheet gives its own caution that "Stamp duties" before 1999–00 is an aggregate (ONS series GTBC); the two components exist only from 1999–00 and are not extended backwards.

### 3.1 Level, trend and swings, cash basis, outturn 1978–79 to 2020–21

| Tax | first 3 yrs | last 3 yrs | change | lowest (year) | highest (year) | trend, points per decade | volatility (sd of annual change) | verdict |
|---|---:|---:|---:|---|---|---:|---:|---|
| Corporation tax (total) | 1.91 | 2.56 | +0.65 | 1.64 (1981–82) | 3.41 (1989–90) | +0.07 | 0.27 | rose, large swings |
| of which onshore | 1.81 | 2.50 | +0.69 | 1.41 (1981–82) | 3.29 (1989–90) | +0.08 | 0.27 | rose, large swings |
| Capital gains tax | 0.19 | 0.46 | +0.28 | 0.09 (1993–94) | 0.53 (2020–21) | +0.05 | 0.08 | rose, large relative swings |
| Inheritance tax | 0.18 | 0.24 | +0.06 | 0.15 (2009–10) | 0.26 (2020–21) | +0.01 | 0.017 | about steady |
| Stamp duties (total) | 0.24 | 0.70 | +0.46 | 0.17 (1992–93) | 0.90 (2007–08) | +0.14 | 0.095 | rose, large swings |
| of which property transaction taxes (from 1999–00) | 0.33 | 0.54 | +0.21 | 0.30 (1999–00) | 0.65 (2006–07) | +0.10 | 0.09 | rose |
| of which stamp taxes on shares (from 1999–00) | 0.33 | 0.17 | −0.17 | 0.13 (2012–13) | 0.40 (2000–01) | −0.07 | 0.04 | fell |
| Business rates | 1.75 | 1.26 | −0.49 | 0.96 (2020–21) | 2.11 (1982–83) | −0.14 | 0.12 | fell |
| Council tax | 1.32 | 1.62 | +0.30 | 1.05 (1991–92) | 1.75 (2020–21) | +0.06 | 0.10 | rose |
| The six together | 5.60 | 6.85 | +1.25 | 4.89 (1993–94) | 7.61 (1988–89) | +0.19 | 0.38 | rose |
| Total HMRC (context) | 25.48 | 28.23 | +2.75 | 23.52 (1993–94) | 29.11 (2007–08) | +0.46 | 0.72 | rose |

"The six together" is corporation tax (total), capital gains tax, inheritance tax, stamp duties (total), business rates and council tax. The flagged forecast values for 2027–28 (OBR, March 2023 EFO and later) are: corporation tax 3.71, CGT 0.89, IHT 0.29, stamp duties 0.78, business rates 1.22, council tax 1.81, the six 8.70, total HMRC 32.22. They are forecasts, not outturn, and are not used in the statistics.

### 3.2 Reading rule for the verdicts

"First 3" and "last 3" are the means of the first and last three outturn years. A change of 0.15 points or less is "about steady"; a larger rise or fall is "rose" or "fell". The rule is a convention of this note. Any cut-off between 0.07 and 0.16 gives the same verdicts: the smallest change after inheritance tax (+0.06) is the share stamp taxes (−0.17). The trend column is the ordinary least squares slope of the share on the year.

### 3.3 Basis: cash against national accounts, 1999–00 to 2020–21

The workbook's national-accounts sheet starts in 1999–00. Over the 22 outturn years both bases agree to within 0.001 points for CGT, IHT and the stamp components, within 0.05 points for business rates and 0.06 for council tax. They differ for corporation tax (up to 0.53 points in a year), which the two sheets define differently: the cash sheet's note says "net of enhanced and payable tax credits", the national-accounts sheet's "gross of reduced liability tax credits" and includes Pillar 2 taxes. Over 1999–2021 the total's trend is −0.26 points a decade on the national-accounts basis (first three years 3.07, last three 2.55); the cash series is longer and its trend is given in 3.1. The earlier 174r values for onshore corporation tax from OBR WP15 sit on the national-accounts basis: they differ from it by more than 0.1 point in 2 of 12 years (2017–18, 2018–19) and from the cash basis in 9 of 12. Choose the basis once per use; do not mix them.

### 3.4 Overlap with the earlier 174r values

`retired-tax-overlap-174r.csv` compares every earlier 174r value that the workbook also holds, on both bases (106 comparisons). Capital gains tax (largest difference 0.04 points), property transaction taxes (0.05), council tax (0.07 cash, 0.05 national accounts), inheritance tax (0.04) and stamp taxes combined (0.04 cash, 0.003 national accounts) agree within 0.1 point. Onshore corporation tax is the exception (above). The OBR March 2025 value for business rates, 2024–25, is 1.1% of GDP; the workbook has 1.33 (cash) and 1.32 (national accounts) for that year, a difference of 0.22: the two come from different vintages and the OBR figure is rounded; this is reported, not resolved.

### 3.5 Association with house and equity prices

Pearson correlation, 42 years (financial year 20XX–YY matched to calendar year 20XX), of the annual change in the share (points) with the annual log change of the ratio of the UK house price index (JST release 6, nominal) or the equity price index (cumulated JST equity price change) to nominal GDP; levels in brackets for completeness (two trending levels correlate spuriously, so they are not evidence).

| Tax | change vs house price/GDP | change vs equity price/GDP | levels: house | levels: equity |
|---|---:|---:|---:|---:|
| Corporation tax | +0.13 | +0.24 | (+0.15) | (+0.62) |
| Capital gains tax | +0.21 | −0.34 | (+0.57) | (−0.06) |
| Inheritance tax | +0.30 | +0.30 | (+0.57) | (+0.16) |
| Stamp duties (total) | +0.16 | +0.53 | (+0.63) | (+0.38) |
| Property transaction taxes (21 years) | +0.26 | +0.56 | (+0.51) | (−0.13) |
| Stamp taxes on shares (21 years) | +0.01 | +0.46 | (−0.46) | (+0.81) |
| Business rates | −0.19 | +0.10 | (−0.34) | (−0.47) |
| Council tax | +0.23 | −0.16 | (+0.70) | (−0.36) |
| The six together | +0.50 | +0.23 | (+0.30) | (+0.10) |

The JST data end in 2020. No policy-break indicator is held, so the coefficients mix policy changes with price effects. With 42 years a correlation must exceed about 0.30 in size to differ from zero at the 5% level even if the years were independent; they are not independent, and this table holds 18 coefficients, so only the larger ones (the six together with house prices, +0.50; the stamp duties and property transaction taxes with equity prices, +0.53 and +0.56) say anything, and they say it about the sign of the co-movement, not about its size or stability.

## 4. Volatility and asset-price relationships

### Corporation tax

Onshore CT fell 0.6 percentage points of GDP in 2008–09 (2.5% to 1.9%), partly following the main rate cut from 30% to 28%. It recovered to 2.2% in 2009–10 and was broadly flat until 2013–14, then rose to 2.6% by 2016–17. The OBR later reports 3.2% GDP in 2024–25, reflecting the 25% main rate introduced in April 2023 and a stronger profit base. CT is profit-cycle sensitive, but policy and timing changes are large confounders. It is not directly a function of household wealth.

### Council tax

Council tax was comparatively stable at 1.5–1.6% GDP over 2007–19. OBR attributes its 0.1 percentage-point rise to above-inflation increases in average bills; dwelling numbers grew by less than 1% a year. Later receipts were constrained by freezes and referendum limits (OBR tax-by-tax page). This is a policy-indexed local revenue stream, not a tax that automatically tracks market house prices.

### Business rates

Business rates rose by 0.1 percentage points GDP over 2007–19, mainly because rateable values were held constant through the crisis while property prices and GDP fell. Revaluations and reliefs subsequently only partly reversed the rise. The tax is linked to rateable rental values, but revaluation lags, multipliers and reliefs make the relation to current commercial property prices discontinuous. The OBR's 2024 UK Survey also notes that the system can discourage improvements that increase rateable value.

### Capital gains tax

CGT was 0.3% GDP in 2007–08, rose to 0.5% in 2008–09, fell to 0.2% in 2009–10, then recovered to 0.4% by 2016–19. OBR attributes the sharp 2009–10 base fall to the financial crisis and the unwinding of forestalling around taper relief abolition. The effective rate increased after taper relief was abolished and rates changed. The OBR's forecast model uses equity prices, average house prices and residential property transactions; it says the relationship between equity prices and disposals is historically volatile and uncertain. This is strong evidence of sensitivity, but not a stable elasticity.

### Stamp / property transaction taxes

Property transaction taxes fell from 0.6% GDP in 2007–08 to 0.3% in 2008–09 and 2009–10 as both property prices and transactions fell. Receipts recovered to 0.7% by 2017–18, then 0.6% in 2018–19. OBR says the tax base had not fully recovered by 2018–19 despite average prices exceeding the pre-crisis peak; policy (higher rates on additional properties and first-time buyer relief) also shifted the effective rate. HMRC's latest annual bulletin reports stamp-tax receipts at 0.9% GDP in 2006–07 and 0.7% in 2025–26; this wider grouping includes share stamp taxes and ATED and excludes devolved land transaction taxes from the point of devolution. OBR's later forecast analysis records a roughly 50% fall in property transaction tax receipts during the financial crisis and sharp pandemic-era falls and rebounds.

### Inheritance tax

IHT receipts rose from 0.2% GDP in 2006–07 to 0.3% in 2025–26. OBR attributes the post-2009–10 rise mainly to asset-price appreciation, particularly residential property, and fiscal drag from the frozen nil-rate band. The series also moves with death counts, policy changes and payment timing. OBR forecasts IHT from administrative estate data and projects asset values using house-price and equity-price forecasts. It is therefore sensitive to wealth valuations, but not a direct annual tax on the whole household wealth stock.

## 5. Fixed-GDP versus wealth-linked counterfactual indexation

The author's 26 November ruling is that retired taxes remain held at a fixed share of GDP, with a wealth-linked switch to be added later. This note does not recommend reversing that ruling.

The historical evidence shows why the switch is a meaningful scenario:
- A fixed-GDP comparator preserves a constant fiscal claim relative to the economy, independent of the historical volatility of the tax being retired.
- A wealth-linked comparator would rise or fall with a defined household-wealth stock, which can move sharply with asset prices and valuation conventions. It would not reproduce the observed historical path of any of these six taxes.
- For property and asset taxes, receipts are influenced by prices, transaction volumes, effective rates, thresholds, and lags. The fact that CGT/IHT/stamp receipts respond to asset prices does not mean they are proportional to total household wealth.
- For council tax and business rates, local policy, revaluations, reliefs and multipliers can dominate the link to property values. Corporation tax is mainly linked to corporate profits, not household wealth.
- A wealth-linked retired-tax comparator therefore needs a defined stock (net household wealth, gross wealth, taxable wealth, or selected assets) and a price/quantity treatment. Using total household wealth would import land and pension valuations into a comparator for taxes that did not historically tax those bases.

A minimal sensitivity can reuse the wealth/GDP drift candidates in the block-1 note: low −0.5%, central-for-illustration 0%, high +0.5% annual log drift in the wealth-linked retired-tax base relative to GDP. Over 50 years these imply multipliers of approximately 0.78, 1.00 and 1.28 relative to the fixed-GDP comparator. These are scenario-axis candidates, not empirical estimates of how the six retired taxes would have behaved.

Measured evidence for the indexation question (section 3): over 1978–2021 the six taxes together rose from 5.6 to 6.8% of GDP and moved between 4.9 and 7.6%, so a fixed share of GDP is not what they did in total; single taxes moved in different directions (business rates and share stamp taxes fell, corporation tax, stamp duties on property, CGT and council tax rose, IHT stayed within 0.15 to 0.26). The year-to-year changes of their sum have a correlation of +0.50 with the change in the house price to GDP ratio and +0.23 with the equity price to GDP ratio. That is consistent with some link to asset prices at the level of the group, and it is not strong enough, over one country and 42 years with policy changes throughout, to say that the group tracks household wealth in proportion. This note states the evidence only; the fixed share of GDP stays the working rule and the wealth-following switch is a later design.


## 6. Data and limitations

Answered by brief 175r: the annual series for every tax (the IFS workbook already held in `data/rates/`; the OBR historical database and the HMRC ODS table are not needed for it), the business rates and inheritance tax annual series, the council tax and business rates series, and the correlations with house and equity prices. Still true:

1. **Basis.** Cash and national accounts are both given and not mixed (3.3). Forecast years (2021–22 onwards in the workbook's cash sheet, flagged from the sheet's own row 2) are not in the statistics.
2. **Scope of the series.** The workbook's corporation tax is the total including offshore; the onshore row is kept separately. Council tax and business rates are the sheet's series (its title is UK revenue; the national-accounts sheet's note says its business rates exclude Northern Irish business rates); the earlier 174r council tax values were Great Britain receipts, which may account for part of the small differences in 3.4.
3. **Asset prices.** JST (release 6, ends 2020) gives the UK nominal house price index and equity price change; no commercial property, no land and no policy-break indicators are held, so business rates and council tax (rateable values and bands) are compared with house prices only as a rough proxy.
4. **Short history.** One country, 43 outturn years, serial correlation in every series; the coefficients are descriptive.
5. **Not held:** a series before 1978–79; accrued (time-shifted) corporation tax and CGT beyond the national-accounts sheet's 1999–00 start.

No observation was filled in or interpolated. A sheet cell left blank (the two stamp components before 1999–00) is absent from the CSV.

## 7. Reproduction

`python -I research/tables/174r-evidence/retired_tax_series.py` regenerates `retired-tax-gdp-annual-full.csv` and `retired-tax-overlap-174r.csv` byte for byte from the workbook; `python -I research/tables/174r-evidence/retired_tax_stats.py` then regenerates `retired-tax-stats.csv` (it reads that CSV and `data/jst/jst_r6.json`). `retired-tax-gdp-annual.csv` is the earlier partial series (OBR WP15 tables 2.3, 2.4, 2.5, 3.4; HMRC annual bulletin figures 5 and 11; OBR EFO March 2025 table 4.1), kept as the source of the overlap check. Checker: `python -I project/tools/check_agent_docs.py` (run for 175r, see its change report).

## 8. Open rulings

- ~~Whether "stamp duty" means property transaction taxes only, stamp duty on shares only, or both~~ Ruled 2026-11-26: both, as separate columns and as a sum (this note's `stamp_duties_total`).
- Whether to include devolved LBTT/LTT in a UK-wide stamp series from their introduction (the workbook's property transaction taxes include them, note e).
- Whether the retired-tax wealth-linked axis should use household NBS net worth or a narrower WDT-taxable wealth stock.
- Whether to apply one common wealth index to all six retired taxes or only to taxes whose bases historically move with household assets (the table in 3.5 is the evidence on that, and it is weak).
- Whether to use OBR accrued/time-shifted receipts or HMRC cash receipts as the primary historical series. They must not be silently mixed.
- Whether to add a series before 1978–79 (the OBR historical public finances database is the intended source; not needed for this note).

## References (not added to project bibliography)

- Mee, J. (2020), The evolution of public sector receipts over the past decade, OBR Working Paper 15, tables 2.3, 2.4, 2.5 and 3.4, paragraphs 2.11, 2.19–2.24 and 3.23–3.27.
- OBR (2025), Economic and fiscal outlook, March 2025, table 4.1.
- OBR (2026), Tax by tax, spend by spend: Onshore corporation tax; Council tax; Capital gains tax; Inheritance tax; Property transaction taxes.
- HMRC (2026), HMRC tax receipts and National Insurance contributions for the UK (annual bulletin), figures 5 and 11 and statistics table.
- OBR (2023), Historical public finances database, 300-year tax and spending series (not used; the IFS workbook is).
- Institute for Fiscal Studies, Composition of UK revenue (`data/rates/Revenue composition spreadsheet.xlsx`; sheets `% GDP (cash)` and `% GDP (national accounts)`); forecasts in it from OBR EFO March 2023 and later.
- Jordà, Schularick and Taylor, Macrohistory Database, release 6 (`data/jst/jst_r6.json`; UK `hpnom`, `eq_capgain`, `gdp`).
