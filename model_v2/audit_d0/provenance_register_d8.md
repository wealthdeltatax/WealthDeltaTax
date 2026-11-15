# D8 provenance and status (historical wealth concentration; context only)

Date: 15 October 2026. Priority: low (spec). Hook: none directly. The model distribution is a 2016-18 snapshot; this dataset shows how far history departs from it. Companion: `coverage_matrix_d8.csv`.

## What was opened

| Source | Status | Opened |
|:---|:---|:---|
| Alvaredo, Atkinson, Morelli (2018) | partly | Abstract: span and method only; no values. |
| WID technical note 2025/10 (distributional series 1800-2024) | partly | Coverage text and Table 4 country-year listing; no values. |
| Saez and Zucman (2016) | partly | See D2; not opened for shares here. |

## Findings

1. **UK.** A top-share history exists from 1895 to the present, estate-multiplier based. The shape: roughly constant before 1914, a sharp fall 1914 to 1979, rising since 1980. No values were extracted.
2. **Coverage elsewhere.** WID's wealth series reach back to 1820 but are sparse: the entries for the pre-1910 period cover Canada, Germany, France, Great Britain, Italy, the Netherlands and Sweden; US from 1913; Norway from 2010, Denmark and Finland from 1980 or later. Missing country-years are imputed from income distribution, so the imputed values are not independent wealth evidence.
3. **Use.** Context only. The graded comparison should be restricted to the UK and US, where estimates are not imputed.

## Definition fidelity

- UK and US series use different methods (estate multiplier versus capitalised income); WID imputations are a third basis. State which when comparing.
- Top shares relate to personal wealth of adults, not households, in the sources opened.

## Gate

None in the spec. Extraction is deferred until the model needs a historical comparison.
