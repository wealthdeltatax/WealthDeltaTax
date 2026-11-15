# WDT data audit: status summary and items left to address

Date: 15 October 2026. Covers D0 to D10. All values are from sources opened in this audit; each dataset has a coverage matrix and a provenance register (`coverage_matrix_dN.csv`, `provenance_register_dN.md`). Placeholders: `placeholder_register.md`.

## 1. Gate outcomes

| Dataset | Gate (spec) | Outcome | Notes |
|:---|:---|:---|:---|
| D0 JST audit | none | Done, verified | Table 26 reproduces; CAN and IRL have no usable years. |
| D1 household wealth / GDP | at least 8 of 16 countries with at least 50 usable years | **Pass on paper (11 of 16); 8 on verified spans (no margin)** | Exact counts from `usable_years.csv`. ITA 52 is the marginal verified country. JPN 48, NOR 39, FIN 23, PRT 8, BEL none: fallback (pooled c, grade C). DNK, NLD, CHE passes rest on unverified sources. |
| D2 saving by wealth | shape evidence for UK, US, one Nordic | **Not met for the UK** | US (Saez-Zucman) and Norway (Fagereng et al.) exist; UK only ELSA financial wealth, over-50s. Pooled shape, grade C, for the UK. |
| D3 ownership | UK and US full series | **Census done; values not extracted** | UK 1918 to 2013 (sparse early), annual from 1980; US annual from 1965. Third variable (adults above median house value) only from WAS 2006 and SCF 1989. |
| D4 equity ownership | UK from first year; others by era, grade C fallback | **UK pass (1963 to 2024, 28 survey years); US pass (1945 to 2025)** | Euro area from 1995 at best. Market cap / GDP: awaiting your data. |
| D5 corporate tax | UK full; others if profits series exist | **UK likely pass; others undecided** | Annual OECD 1200 series and HMRC tables not yet opened. |
| D6 burden allocation | joint cut or flag as placeholder | **Fallback: income profile is a placeholder** | CGT and IHT aggregates by band exist, not by wealth band. |
| D7 house prices | D0 coverage; record windows lost | **Done: 153 windows lost vs LEVY (ESP 66, PRT 40, ITA 36, JPN 6, GBR 5)** | Contiguous at T=30: 859 to 781; T=100 unchanged (69). Level price-to-income only from 1970 (OECD). |
| D8 concentration | none (context) | **Census done, no values extracted** | UK from 1895 (estate multipliers); WID sparse and partly imputed elsewhere. |
| D9 demographics | none (documentation) | **Partly recorded** | Age at inheritance 55-64 peak, projected mode 61; adults per head and G not verified. |
| D10 placeholders | source or replace | **Register complete; no placeholder replaced** | See `placeholder_register.md`. |

## 2. Decisions made

| Date | Decision |
|:---|:---|
| 14 Oct | D1 identity route: solve c per contiguous JST run and pool the run estimates. |
| 14 Oct | D1 grading: strict (any documented definitional gap caps at B). |
| 14 Oct | Close D4 open items before D3. |
| 15 Oct | D4 household tranche matches US Z.1 "households and nonprofit organizations": UK Individuals plus Charities etc. (2024: 12.0%). |
| 15 Oct | **D3 validation tolerance: plus or minus 5 percentage points on the 10-year change** (spec open item 3 closed for the primary test). |
| 15 Oct | **W_min per person**: half the median house price on household data (TOML `wmin_house_ratio` 1.0 to 0.5, patch pending). Three zones and one-sided pre-2006 test confirmed. |
| 15 Oct | D3 UK geography: Great Britain (WAS). |
| 15 Oct | **Unit: per adult.** Baseline = equal split of household wealth among adults; sharing parameter s (0 as-owned to 1 equal split) is a stated scenario, not a behavioural estimate. D3 target becomes the share of adults in owner households. |
| 15 Oct | D5 calibration B "comparable company burden": gross levy / GDP against corporation tax only (OECD 1200). Year basis (my call as delegated): trailing 5-year average, latest year as sensitivity. |

## 3. Decisions still needed from you

1. ~~D3 validation tolerance~~ **Decided 15 Oct: plus or minus 5 percentage points on the 10-year change.** Still to set: the level tolerance, and to confirm the three zones and the one-sided pre-2006 test (see D3 register).
2. **CIT owner-share sweep values** (spec open item 2). Evidence so far (one German estimate, about 49% owners) supports 100%, 50%, 25%.
3. **Maximum interpolation gap** and sensitivity (spec open item 4); default 10 years.
4. **D1 per-run parameters:** minimum overlap for solving c on a run (suggested 20 years) and pooling weights (suggested overlap length). Suggested 20 drops CHE runs 1-2, DEU run 2, NLD-Moatsos run 1.
5. **mc_gdp stand-in:** approve World Bank market cap / GDP (FRED) as a flagged grade C source for years after 2016, or wait for Kuvshinov and Zimmermann.
6. **D4 tranche mapping:** which ONS year or average sets `f_inc` and `f_attr`, and which categories map to which tranche.
7. **D5 year window:** confirm the 5-year trailing average or choose another.

## 3b. Per-adult unification: open items

- Model unit: checked. The Advani, Bangham and Leslie (2021) shares rank families (single adults or couples), wealth per adult within the family, but the TOML labels the cells top fractions of adults; re-express on an adult basis (their appendices give an individual version) or flag. W_min decision made (half median house price); TOML patch pending.
- Adults per household by tenure (WAS or EHS tables) to convert D3 to the adult basis; adult age cut-off.
- As-owned sensitivity for property: **not buildable from WAS** (it splits main residence and physical wealth equally among adults over 16; pensions individual). s = 0 is available only for pensions and partly for financial wealth.
- Within-couple gap: the equal-split baseline treats couples as symmetric; WAS has no within-couple gender split in the text opened (single women hold less than single men in every group).
- Spousal transfer treatment under the WDT (mechanism papers).
- Carer and disability variables in WAS for the net-change display.

## 4. Data to obtain

| Item | Who | Status |
|:---|:---|:---|
| Kuvshinov and Zimmermann market cap / GDP data or online appendix (tables E.1 to E.17) | You | Not retrievable here; supplied later. |
| `usable_years.csv` | You | **Received 15 Oct**; used. |
| OECD Revenue Statistics annual series (code 1200, 1965 on) for 16 countries | Me | Not opened. |
| HMRC CGT and IHT ODS tables | Me | Located, not opened. |
| WAS data dictionary (variable level, SN 7215) | You or me | Income variables confirmed at note level; tax/NI not found; dictionary not opened. |
| Saez-Zucman appendix; Fagereng et al. body (percentile anchors) | Me | Located, not read. |
| WID data files (confirm annual coverage, interpolated years) | Me | Not opened. |

## 5. Verification still outstanding

- D1: Baselgia and Martinez (CHE), Moatsos et al. (NLD), Abildgren (DNK), Cardoso and Cunha (PRT), Goldsmith: abstract or fragment only. Artola Blanco et al. and Waldenstrom: abstract only.
- D1: JPN 1960s years in the Bauluz 2019 update (would lift JPN from 48 to about 58).
- D3: English Housing Survey Annex Table 1 and live tables; US pre-1965 census values; US outright ownership span; Eurostat tenure categories.
- D4: JPX Excel categories; Bundesbank long series; Eurostat F511 listed shares; holder history for France, Italy, Spain, Netherlands, Norway, Switzerland (grade C until found).
- D5: HMRC "Corporate Taxes" versus OECD 1200 reconciliation; OSR notes on profit statistics; statutory rate before 1981.
- D2: Mian-Straub-Sufi; Dynan-Skinner-Zeldes years; UK saving by wealth.

## 6. Method points to carry into the model work

- **Timing.** WID series are mid-year averages; raw sources end-year. A half-year alignment is needed before the identity route (D1 decision log 4).
- **Denominator.** Wealth ratios use net national income; JST uses GDP. Only drift in the ratio matters for the identity route (D1 decision log 5).
- **Flags to carry into every output.** UK holder shares 1998 to 2008 `carried`; D1 grades strict; D2 shape pooled and grade C for UK; D6 income profile placeholder; mc_gdp unverified.
- **Pooled c for failing countries** is grade C and must be flagged wherever used.
- **Units.** D3 observed series are household shares; `scope_share_t` is adult-based (accepted, flagged).
- **No tuning to outcomes.** D3 is validation only; do not recalibrate on ownership.

## 7. Not started

Spec step 5, the decision review (for each gate: pass, fallback or fail, and what the fallback changes in the claims). Not written; depends on the decisions in section 3.

## 8. Files

`coverage_matrix_d1.csv` (regenerated: exact overlaps, strict grades), `d1_overlap_runs.csv`, `provenance_register_d1.md`, `d0_jst_audit.py`, D2 to D9 matrices and registers, `uk_holder_shares_ons.csv`, `placeholder_register.md`, and this summary. None is saved to the WDT RESEARCH project yet.

## 9. Added after D7 to D9

- D7: confirm the JST house-price source for ITA, ESP, PRT (KSS cover 14 economies, not these three); open the KSS data file and OECD/BIS documentation; decide whether a pre-1970 price-to-income level is needed.
- D8: extract UK and US top shares if a historical comparison is wanted; WID imputed country-years should not be treated as independent evidence.
- D9: ONS adults per head and generation-gap sources; both unverified.
