# D5 provenance and status (corporate tax base and burden)

Date: 15 October 2026. Status: coverage census only; no series extracted. Companion: `coverage_matrix_d5.csv`.
Role (spec): drives calibration A (median net levy revenue equals CIT revenue) and B (gross levy equals comparable company burden). Gate: UK full; others only if profits series exist.

## What was opened

| Source | Status | Opened |
|:---|:---|:---|
| OECD Revenue Statistics 2025, chapter on tax levels and structures | partly | Table 3.9 for code 1200 (1990, 2000, 2010, 2022, 2023). Full annual series online, not opened. |
| HMRC Corporation Tax statistics 2025 | partly | Landing page: tables, scope, publication date. ODS tables not opened. |
| ONS NRJK (PNFC gross operating surplus, 1948-2025) | verified | Series page. |
| ONS LRWX (UK continental shelf companies gross operating surplus, 1997-2024) | verified | Series page. |
| Millennium of Macroeconomic Data for the UK | partly | README only; the workbook was not read. |
| OECD corporate income tax rates database | not informative | No years or rate definitions on the page. |
| ICTD Government Revenue Dataset | not informative | Page opened had no coverage or variable details. |

## Findings

1. **UK CIT/GDP.** OECD code 1200: 3.3% (1990), 3.5% (2000), 2.8% (2010), 3.2% (2022), 3.4% (2023). The spec's "UK current 3.2%" is the 2022 value; 2023 is 3.4%. Decide which year the calibration refers to.
2. **Two UK definitions.** OECD 1200 and HMRC "Corporate Taxes" are not the same. HMRC's covers corporation tax plus the bank levy, bank surcharge, residential property developer tax, energy profits levy and electricity generator levy. Calibration A must state which it matches.
3. **UK profits.** NRJK covers 1948-2025, so a CIT/profits path is feasible over that span. It is a gross operating surplus (before depreciation) of private non-financial companies, so an effective rate on it understates the rate on taxable profit and excludes financial companies, whose tax is included in CIT.
4. **Both calibration-B measures are derivable** from the above (CIT/GDP; CIT over profits). The choice (spec open item 1) can be made on evidence once the series are extracted.
5. **Other countries.** OECD Revenue Statistics 1965 onward is the candidate for CIT/GDP. Profits series were not examined, so the gate for other countries is undecided.

## Mismatch flags

- **Numerator and denominator scope.** CIT includes financial companies and North Sea; NRJK excludes financial companies. Use a like-for-like ratio or flag the mismatch.
- **JST.** Has total revenue only, so it cannot replace these.
- **Capital transfers** adjustments differ by country in OECD 1200.

## Gate

UK passes on span for CIT/GDP (OECD annual series stated from 1965, not opened) and profits (1948 on). Others unresolved.

## Open

1. Open the OECD annual 1200 series for all 16 countries (or the OECD data explorer), and the HMRC data tables.
2. Pair NRJK with GDP. Check the OSR notes on profit-statistic quality.
3. Statutory rate history before 1981.
4. Profits series for other countries.

## Decision: "comparable company burden" for calibration B (spec open item 1)

**Confirmed by user 15 Oct: gross levy / GDP, corporation tax only (OECD 1200).** Year basis delegated to me and set below.

**Original proposal.** Primary measure: gross company-paid levy / GDP, compared with OECD 1200 CIT / GDP. Secondary, reported alongside but not calibrated to: the same levy as a share of profits, using PNFC gross operating surplus (NRJK) paired with GDP.

Reasons:
1. The levy is a charge on equity value, not profit. Its yearly size tracks market capitalisation, while CIT tracks profits. A target in % of GDP is dimensionally the same for both, and the model already carries GDP-scaled quantities (`mc_gdp`, `levy_path`). A profits target would need an extra profits/GDP path in the model.
2. Calibration A (net state revenue = CIT) and B (gross company-paid levy = comparable burden) then differ only in gross versus net, which is the side-by-side the spec intends. A profits-based B changes both the target and the netting, so the two calibrations could not be read against each other.
3. The profits measure is weaker: NRJK is gross of depreciation and excludes financial companies, while CIT includes them, so the ratio mixes scopes.

Cross-check from the series pulled (OECD CIT/GDP; ONS NRJK over ONS GDP at market prices YBHA): 2022 profit share of GDP 18.7%, implied CIT over gross operating surplus 17.1%; 2023 19.1% and 17.8%. Both are scope-mismatched ratios, shown only to indicate the size of the gap between the two definitions.

Scope of "burden": CIT only (OECD 1200). Employer NI, business rates and the HMRC extras (energy profits levy, bank levy and surcharge) are excluded, since the spec treats employer NI as a firm-side line. If you want the HMRC wider "Corporate Taxes" measure, state it, since it changes the target.

Year basis still needs fixing: 2022 (3.2%) or 2023 (3.4%), or a multi-year average to avoid a single-year target.

**Year basis (decided 15 Oct, my call as delegated).** Target = trailing 5-year average of OECD 1200 CIT / GDP over the latest five available years, to be extracted from the annual series (only 2022 3.2% and 2023 3.4% seen so far). Reasons: the observed values range 2.8% to 3.5% across 1990-2023, so a single year is a noisy target; the latest single year (2023) is reported as the sensitivity. The window length is a parameter.
