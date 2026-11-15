# D1 provenance, decisions and gate (household wealth / GDP history)

Date: 14 October 2026. Status: coverage census only. No series values extracted yet.
Companion file: `coverage_matrix_d1.csv`. D0 inputs: `usable.csv` (first, last, n_usable per country and set).

## Verification status

| Source | Status | What was actually opened |
|:---|:---|:---|
| WID Technical Note 2020/14 (Bauluz and Brassac, Nov 2020) | verified | Full text. Table 1 spans and per-country sources taken from it. |
| Piketty and Zucman (2014), QJE 129(3), working-paper version Dec 2013 | verified | Full text. Wealth definition (Section 3.1) taken from it. Table 1 country spans were cut off in the fetched text, so they are not relied on. |
| Artola Blanco, Bauluz, Martinez-Toledano (2021), Economic Journal | unverified | Abstract and bibliographic records only. Span 1900-2017 also appears in the WID note, which is why the span is marked verified there. |
| Waldenstrom (2017), JEH | unverified | Abstract and bibliographic records. Span 1810-2019 also appears in the WID note. |
| Baselgia and Martinez (2020, 2022) Switzerland | unverified | Abstracts only. |
| Moatsos et al. (2022) Netherlands | unverified | Fragments of the working paper from search results (series 1854-2019, household balance sheets, ratio to net national income). Author list not confirmed. |
| Abildgren (2015) Denmark | unverified | Abstract only. |
| Cardoso and Cunha (2005) Portugal | unverified | Abstract and fragments only. |
| Goldsmith (1985) | unverified | Catalogue records only. |
| WID data files themselves | not opened | Needed to confirm annual coverage and which years are interpolated. |

## Definition fidelity (principle 4)

Verified in Piketty and Zucman (2014), Section 3.1, and carried by WID:

- Private wealth is net wealth (assets minus liabilities) of households and non-profit institutions serving households (NPISH). NPISH is under 10% of the total.
- Includes non-financial assets, unincorporated businesses, life insurance and pension funds. Corporations enter through the market value of equities.
- Excludes pay-as-you-go pension wealth, and excludes durable goods (cars, furniture), which the paper puts at about 30 to 50% of national income, 5 to 10% of net private wealth.
- Denominator is net-of-depreciation national income, not GDP.

Gaps against the model concept (household net worth per adult including pension wealth, WAS-style): durables excluded, NPISH included, PAYG pensions excluded.

## Decision log (D1, proposed)

1. **Grading convention.** Post-1995 official balance sheets are graded A, treating the durables and NPISH differences as minor and documented. Pre-1995 reconstructions are graded B. If a strict reading is preferred (any definitional gap means B), every row drops one grade.
2. **Supersession (principle 3).** Netherlands: Moatsos et al. (1854-2019) is proposed to replace the WID series (1995-2019, from an unpublished BA thesis plus CBS). Pending: open the paper and its data.
3. **Denmark.** Two candidates. WID is private wealth but only 1973-2018 (46 overlap years, fails the gate alone). Abildgren is national wealth (includes government) over 1845-2013. Using Abildgren needs either a private-wealth component or a flagged concept adjustment, grade B/C.
4. **Timing (principle 6).** WID series are mid-year averages while raw sources are end-year. Verified in the WID note. The model uses wealth at the end of start minus 1, so a half-year alignment decision is needed before the identity route.
5. **Denominator.** Wealth ratios use net national income. JST gives GDP. The identity route uses growth in W/Y, so only drift in the ratio of national income to GDP matters (depreciation share, net foreign income). To be checked once series are in hand.
6. **Countries excluded.** CAN and IRL have no usable JST years (D0). CAN has a WID series (1971-2019) that stays unused.

## Gate: at least 8 of 16 countries with at least 50 usable years

Overlap figures are upper bounds from the first and last years only. JST usable years contain gaps, so exact counts need the usable-year list.

- **Pass on paper (11):** AUS 60, CHE 113 (LEVY 79), DEU 112, DNK 134 (via Abildgren, concept caveat), ESP 112, FRA 142, GBR 116, ITA 52 (borderline), NLD 106 (LEVY 84, via Moatsos), SWE 137, USA 129.
- **Borderline (1):** JPN 48 on the WID span, about 58 if the 1960-69 years survive in the Bauluz 2019 update.
- **Fail (4):** BEL (no series found), FIN 23, NOR 39, PRT about 40 at best.
- **Dependence.** Five of the 11 rest on sources not yet opened (CHE, DNK, NLD, plus unverified detail for ESP, SWE). With only the verified WID spans, the pass count is 8 (AUS, DEU, ESP, FRA, GBR, ITA, SWE, USA), which still clears the gate with no margin.
- **Fallback for failing countries:** pooled cross-country c, grade C, flagged (per the spec).

## Issues to resolve before extraction

1. **Gaps in JST usable years versus a single constant c.** D0 shows multiple runs for most countries (DEU 3 runs, 35 span breaks; JPN 15 breaks; CHE LEVY 35 breaks). The identity route solves for the c that reproduces endpoint W/Y over the usable span, which is undefined across breaks. Options: use only the longest run per country, solve c per run and pool, or chain runs using W/Y at run boundaries. This is a design decision for the user.
2. **Interpolation share.** Pre-1970 series for DEU, FRA, GBR, USA rest on sparse historical estimates (the published figures use decennial averages). The share of interpolated years, and whether any gap exceeds the 10-year default, is unknown until the data appendix or WID files are opened.
3. **Exact overlap.** `d0_jst_audit.py` does not write the usable years themselves. A few-line addition (emit `usable_years.csv` with country, set, year) would turn the upper bounds above into exact counts.

## Exact gate result from `usable_years.csv` (15 Oct)

Source: `usable_years.csv` from the D0 rerun (5,104 usable country-year rows across BASE, HOUSE and LEVY). Overlap = JST usable years inside each candidate wealth span. Per-run detail is in `d1_overlap_runs.csv`; the matrix `coverage_matrix_d1.csv` now carries exact overlaps and strict grades (`grade_strict`).

| | LEVY overlap | Gate (50) | Source status |
|:---|---:|:---|:---|
| AUS | 60 | pass | WID verified |
| CHE | 79 | pass | Baselgia, unverified |
| DEU | 112 | pass | WID verified |
| DNK | 132 (Abildgren) / 46 (WID) | pass / fail | Abildgren unverified, national wealth |
| ESP | 112 | pass | WID spans verified |
| FRA | 142 | pass | WID verified |
| GBR | 116 | pass | WID verified |
| ITA | 52 | pass (margin 2) | WID verified |
| NLD | 84 (Moatsos) / 25 (WID) | pass / fail | Moatsos unverified |
| SWE | 137 | pass | WID spans verified |
| USA | 129 | pass | WID verified |
| JPN | 48 | fail (about 58 if 1960s exist in Bauluz 2019) | WID verified |
| NOR | 39 | fail | WID verified |
| FIN | 23 | fail | WID verified |
| PRT | 8 | fail | Cardoso and Cunha, unverified |
| BEL | none | fail | no series found |
| CAN, IRL | zero usable JST years | excluded | |

Outcome: 11 of 16 pass under LEVY (same counts under BASE except CHE 113, NLD 106, PRT 25). On verified spans only: 8 (AUS, DEU, ESP, FRA, GBR, ITA, SWE, USA), exactly the gate with no margin. ITA is the marginal verified country. HOUSE mode drops ESP to 46, ITA to 50, PRT to 15, so the house-price sensitivity loses ESP.

Per-run implications (decision 1b: solve c per run, then pool). Runs with short overlap: CHE runs 1-2 (13, 10 years), DEU run 2 (14), NLD-Moatsos run 1 (14), DNK-Abildgren run 2 (20), ESP run 1 (35). Pooling weights are still to be set (suggested: overlap length). A minimum overlap per run for solving c is a parameter, not yet set (suggested 20 years, which would drop CHE runs 1-2, DEU run 2 and NLD-Moatsos run 1).
