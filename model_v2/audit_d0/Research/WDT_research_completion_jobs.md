# WDT research completion: parallel jobs

Date: 17 Oct 2026 (replaces the 16 Oct version). Source: `WDT_audit_status_2026-10-16.md` **as updated the evening of 16 Oct after the WID API pull** (project path `claude/WDT_audit_status_2026-10-16.md`; sections 1, 3, 9 and 12 differ from the earlier copy), the registers, `decision_log.md`, `placeholder_register.md`.
Nothing here changes model code except Job 10 (TOML and `rates_core` patches, via numbered patch plus test in `Model/test/`).

Each job lists: **Goal**, **Needs from you**, **Give the agent these files**, **Output**, **Blocked by**.
"Give the agent" means attach these to the session that does the job. Files marked (not in project) are ones I have not seen and you must supply, or are new data.

## What changed since the 16 Oct version

- J0 is closed: every decision is made (table below).
- J1 (WID pull) is done. Remaining J1 work is analysis only.
- The D1 gate is **8 of 16, met at the threshold** (WID primary everywhere, DEU and NLD split at 1979/80), not "13 of 16". The 13 counted back-cast years. Claims must say the gate is met narrowly (JPN exactly 50, FRA 51).
- J10 is split: the first part (W_min, `adults_m`, sensitivity scenario, ladder anchor) is written and tested; the corporation-tax part waits for J3.
- J3 no longer blocked by a decision, but the CT retire-share patch waits for its HMRC reconciliation.
- The agent file lists use the project's current names. Files made this session sit under `claude/` in the project.

## Waves (what can run at the same time)

| Wave | Jobs | Condition |
|:---|:---|:---|
| 0 | J0 decisions | **Done 17 Oct.** |
| 1 (all parallel) | J1 (analysis left), J3, J4, J5, J6, J7 (needs K-Z file), J8, J9 | No dependency on each other. |
| 2 | J2 (needs J1 analysis), J10b (needs J3, J5, and J4 or J7 values if used) | |
| 3 | J11 stale files, J12 decision review | After the Wave 1 and 2 results they record. |
| 4 | J13 model-side gaps | After J10b so the numbers move once. |

The first patch pair (J10a) is already written: apply it and re-run RATES and VAL at your convenience. J10b will force a second re-run, so skip any polishing run in between.

---

## J0. Decisions: all made

| # | Decision | Made |
|:--|:---|:---|
| 1 | WID primary for every country, including NLD, DNK, CHE (from 1950) and AUS. Earlier sources (Moatsos, Abildgren, Baselgia, the 60-year AUS series) stay as cross-checks with their grades and flags. | 16 Oct |
| 2 | D5 year basis: trailing 5-year 2020-24 = 3.08%; latest year 3.47% as sensitivity. | 16 Oct |
| 3 | D1 per-run minimum overlap 20 years; pooling weight = retained overlap years. DEU and NLD identity solves split at 1979/80. Back-cast years excluded; sensitivity run drops DEU 1980-95 and GBR 1980-87 debt years (dq 1). | 16 and 17 Oct |
| 4 | D3: level tolerance plus or minus 10 pp; change tolerance plus or minus 5 pp on the 10-year change; three zones. **Before 2006 (UK) a one-sided upper-bound test** (scope share must not exceed owner-occupation share); the band applies from 2006 (WAS). **Basis: household diagnostic now, adult basis as primary once adults per household by tenure is sourced.** | 16 and 17 Oct |
| 5 | CIT owner-share sweep 100%, 50%, 25%. | 16 Oct |
| 6 | Maximum interpolation gap 10 years for non-WID inputs that mark benchmarks; WID window start = component start, no gap rule on WID series. | 16 Oct |
| 7 | D4: 2024; rest of world 58.8%; household tranche = individuals + charities etc (12.0%). | 16 Oct |
| 8 | `mc_gdp`: wait for the K-Z appendix; flag `mc_gdp` after 2016 unverified in every output; no stand-in. | 16 Oct |
| 9 | `adults_m` = 52.0 (18+, consistent with `pop_per_adult` 1.27). | 16 Oct |
| 10 | VAL tolerances stay at `brg_tol` 1%, `hsc_tol` 1%, `state_tol` 2%; recorded before any run. | 17 Oct |
| 11 | W_min = half the median house price (`wmin_house_ratio` 0.5); sensitivity scenario `gain_ladder_wmin_full` at 1.0; ladder first anchor follows W_min in `rates_core`. | 15 and 17 Oct |
| 12 | Corporation tax `retire` share stays 3.2% until J3 reconciles HMRC "Corporate Taxes" to OECD 1200; then patch to the chosen target (3.08%). | 17 Oct |

**Give the agent:** `claude/WDT_audit_status_2026-10-16.md`, `decision_log.md`.
**Output:** copy this table into `decision_log.md` (section 9 "Made" of the status note still lacks the 17 Oct rows: 3 pooling confirmed, 4 pre-2006 and basis, 10, 11 sensitivity and anchor, 12).

---

## J1. WID API pull (D1, D8): pull done, analysis left

**Done (16 Oct):** `wid_download.py` run, 361,536 rows, 14 countries; `wid_summarise.py` and `wid_checks.py` run; `WID_Data_Guide.md` written. Findings: money is constant local currency, not PPP; annual 1800 start is back-cast; real start is the composition window; `dq` is a regime flag; WID exposes no interpolation flag; PRT not in WID; DEU and NLD have true 1979/80 splice breaks.
**Goal now:** (a) NOR definition check (pweal/nninc 2.16 in 2000, 2.61 in 2025; nweal/nninc 7.63); (b) extract UK and US top 1% and 0.1% `hweal` shares (age 992, pop j) for D8; (c) build the D1 sensitivity run (drop DEU 1980-95, GBR 1980-87).
**Needs from you:** nothing new; a second `fetch` only if you want another vintage. For (a), `wid_long.csv` rows for NOR `pweal`, `nweal`, `nwnxa`, `nwgxa`, `nwgxd`, `nninc` (small extract).
**Give the agent:**
- `claude/wid_download.py`, `claude/wid_summarise.py`, `claude/wid_checks.py`, `claude/WID_Data_Guide.md`
- `claude/WDT_audit_status_2026-10-16.md` (section 3)
- `coverage_matrix_d1.csv`, `provenance_register_d1.md`, `coverage_matrix_d8.csv`, `provenance_register_d8.md`
- (not in project) `wid_out/summary/` and `wid_out/summary2/`, `catalogue.csv`, `manifest.json`; the NOR and UK/US top-share extracts
**Output:** NOR reading; D8 UK and US top-share series; sensitivity run result.
**Blocked by:** nothing.

## J2. D1 gate rerun and c per country

**Goal:** regenerate the D1 gate table from the WID series (gate currently 8 of 16 at the threshold), do the per-run overlap at minimum 20 with the DEU and NLD splits, run the debt-year sensitivity, write `c_country.csv` and `c_shape.csv` skeletons.
**Give the agent:**
- `usable_years.csv`, `usable.csv`, `windows.csv`, `d1_overlap_runs.csv`
- `coverage_matrix_d1.csv`, `provenance_register_d1.md`
- `WDT_Data_Audit_Spec.md` (D1 identity and flow routes, deliverable formats)
- `wdt_jst.py` (window and run rules), `audit_d0.md`
- `claude/WID_Data_Guide.md`, J1 outputs
**Output:** gate table (with the threshold caveat), per-run overlap with min 20, `c_country.csv`, sensitivity comparison. Grading strict; failing countries (AUS, CHE, DEU, DNK, FIN, NOR, BEL, PRT) take pooled c, grade C.
**Blocked by:** J1 (b and c only).

## J3. D5 corporate tax target

**Goal:** reconcile HMRC "Corporate Taxes" (corporation tax plus bank levy, surcharge, RPDT, EPL, EGL) to OECD 1200; extract leg shares of GDP; fix the target for the levy calibration. Target base case already decided: 3.08% (2020-24), 3.47% sensitivity.
**Needs from you:** (not in project) OECD 1200 UK file (`2a`, `2b`, received); **HMRC Corporation Tax statistics 2025 data tables (ODS), not yet received**.
**Give the agent:**
- OECD file `2a`, `2b`, HMRC CT ODS tables, HMRC receipts `NS_Table`
- `provenance_register_d5.md`, `coverage_matrix_d5.csv`
- `WDT_Params.toml` (`[rates.replacement]` `retire` and legs, `[rates.levy_calibration]`)
- `WDT_Code_Reference.md` (CORP levy and calibration)
**Output:** reconciliation note, confirmed target, leg share table to feed J10b and J4.
**Blocked by:** the CT tables (decision is made).

## J4. D6 burden allocation (HMRC and WAS)

**Goal:** extract CGT and IHT by band, employer NI aggregates; decide what the income profile can honestly say; test the owner-share sweep 100%, 50%, 25%.
**Needs from you:** CGT Tables 2 and 3, IHT 12.3 and `NS_Table` (received); **IHT Table 12.1 and 12.4 (not received)**; **WAS data dictionary SN 7215 (not received)**.
**Give the agent:**
- the HMRC files above
- `provenance_register_d6.md`, `coverage_matrix_d6.csv`
- `placeholder_register.md` (rows `employer_share`, `income_by_wealth`, taxpayer-count curves, leg shares)
- `WDT_Params.toml` (`[rates.replacement]` and `.legs.*`, `.income_by_wealth`)
- `wdt_core.py` (`calibrated_legs`, `leg_cost`, `band_net_position`)
- `RATES/8_2_RATES_tables.py` (tables 17 to 22 captions that state placeholders)
**Output:** CSVs of bands and receipts; `employer_share` recommendation; statement for table 22 on income profile status (placeholder unless the WAS joint cut is found).
**Blocked by:** nothing (decision made).

## J5. D3 ownership, D9 demographics, adult basis

**Goal:** adults per household by tenure; 16+/18+ series; D3 observed target on an adult basis (primary once available; household diagnostic runs first); correct the D9 wording (G is the parent's age at the heir's birth, `pop_per_adult` is an 18+ convention).
**Needs from you:** ONS population by single year of age 1971 on (Nomis gave all ages only; re-export or mid-year estimates dataset); EHS or WAS adults per household by tenure; EHS FT1101, EHS Chapter 1 and Annex (received).
**Give the agent:**
- `provenance_register_d3.md`, `coverage_matrix_d3.csv`, `provenance_register_d9.md`, `coverage_matrix_d9.csv`
- `decision_log.md` (per-adult and tolerance decisions: level plus or minus 10 pp, change plus or minus 5 pp, one-sided pre-2006 test)
- `placeholder_register.md` (rows `adults_m`, `wmin_house_ratio`)
- `WDT_Params.toml` (`pop_per_adult`, `[rates.replacement].adults_m`, `wmin_house_ratio`)
- the data files above
**Output:** adult-basis ownership series, adults-per-head history, a check of `adults_m` 52.0 against ONS 18+, D9 register corrections.
**Blocked by:** nothing for the household diagnostic; the adult-basis series waits for the adults-per-household table.

## J6. D7 house-price source for ITA, ESP, PRT

**Goal:** confirm the JST source and quality for those three countries; keep the 153-window loss count current (ESP 66, PRT 40, ITA 36, JPN 6, GBR 5).
**Needs from you:** JST documentation pages for ITA, ESP, PRT (image-only PDF: manual read or OCR text). The KSS appendix covers 14 economies, none of these.
**Give the agent:**
- `provenance_register_d7.md`, `coverage_matrix_d7.csv`
- `audit_d0.md`, `windows.csv`, `usable.csv`, `variables.csv`
- `d0_jst_audit.py`
- the KSS appendix (`NPLH_documentation.pdf`) and the new documentation pages
**Output:** source and grade per country; updated HOUSE-mode caveats.
**Blocked by:** nothing.

## J7. D4 equity ownership and `mc_gdp`

**Goal:** close `mc_gdp` after 2016; euro-area holder-share history. Tranche mapping is decided (2024, 58.8%, household tranche 12.0%).
**Needs from you:** Kuvshinov-Zimmermann Data Appendix (tables E.1 to E.17) or dataset. Until it arrives, `mc_gdp` after 2016 stays flagged unverified; no stand-in.
**Give the agent:**
- `provenance_register_d4.md`, `coverage_matrix_d4.csv`
- `uk_holder_shares_ons.csv`, `EVAL/srs.csv`
- `WDT_Params.toml` (the `levy = {...}` block and its comments)
- `WDT_Code_Reference.md` (CORP levy section)
**Output:** `mc_gdp` series and source; euro-area holder shares.
**Blocked by:** the K-Z file.

## J8. D2 saving by wealth

**Goal:** read percentile anchors for US and Norway; look for UK evidence; build the pooled grade C shape. Sources are saving over income, so a wealth/income conversion is needed.
**Needs from you:** Saez-Zucman main data and appendix (received), Fagereng et al. paper body (Figure 10d), Mian-Straub-Sufi, IFS R71, WTC EP1.
**Give the agent:**
- `provenance_register_d2.md`, `coverage_matrix_d2.csv`
- `WDT_Data_Audit_Spec.md` (D2 hook and gate)
- `WDT_Params.toml` (`[rates.cohorts.*]`, consumption `c`, `payout_top`)
- `RATES/rates_core.py` (functions `cohort_spec`, `run_window` payout block) only if the shape is to be wired
**Output:** `c_shape.csv` anchors, pooled shape, UK fallback statement.
**Blocked by:** nothing.

## J9. Advani family basis to adult basis

**Goal:** re-express the wealth distribution cells on an adult basis (or quantify the bias). This is the "per-adult unification" model-side item; the other open items in section 9 of the status note (adults per household, as-owned sensitivity, within-couple gap, spousal transfers) are modelling questions, not audit gates.
**Needs from you:** Advani, Bangham, Leslie (CAGE WP 576) appendix with the individual version.
**Give the agent:**
- `placeholder_register.md` (the unit row)
- `WDT_Params.toml` (`[rates.dist]`, `[rates.dist.advani]`)
- `RATES/rates_core.py` (L1 dist: `build_dist`, `_build_advani`, `_fit_tail`, `_body_cells`)
- `provenance_register_d3.md` (Advani section)
**Output:** adult-basis shares for `s10_survey`, `s1_survey`, `s1_upper`, or a bias note.
**Blocked by:** nothing.

## J10. Patches (change model inputs)

### J10a. Written and tested on a mock tree (17 Oct); apply on your machine
- `patch_NNN_wmin_half_adults_52.py` (+ test): `wmin_house_ratio` 1.0 to 0.5 in `[rates.defaults]` and the 47 scenarios that set 1.0; `adults_m` 54.0 to 52.0; scenario labels; new `gain_ladder_wmin_full` (ratio 1.0) and its entry in the `[rates.run]` list; `house_median_gbp_m` comment relabelled (HPSSA England median, not a mean).
- `patch_NNN_ladder_anchor_follows_wmin.py` (+ test), `rates_core.py`: a ladder's first anchor sits at the scenario's W_min.
- Apply together. Moves: every scenario with the house-price W_min, ladder scenarios (start at £0.1125m), VAL (reads W_min from the scenario), `adults_m` figures. Re-run: `rates_core`, `valgen_core`, then the tables and charts (RATES scope and levy tables T12 to T25; VAL tables and charts).
- If the first patch pair was applied before the sensitivity scenario and relabel were added, re-running the patch applies only the new edits.

### J10b. Still to write
**Patches:** corporation-tax `retire` share and the `[rates.levy_calibration]` target (after J3); any J4, J5, J7 values.
**Give the agent:**
- `WDT_Params.toml`, `wdt_core.py` (`_parse_rates`), `RATES/rates_core.py`
- `decision_log.md`, `placeholder_register.md`
- `Model/test/wdt_patchlib.py`, `Model/test/PATCHES.md` (not in project)
- outputs of J3, J4, J5, J7
**Output:** `patch_NNN_*.py`, `test_patch_NNN_*.py`; state which tables and figures move.
**Blocked by:** J3 (and J4, J5, J7 where used).

## J11. Stale-file cleanup

**Goal:** bring registers and matrices in line with results.
**Give the agent:**
- `coverage_matrix_d1.csv`, `wdt_audit.json`, `wdt_audit_to_json.py`
- `provenance_register_d1.md`, `_d3`, `_d5`, `_d6`, `_d7`, `_d9`
- `placeholder_register.md`, `decision_log.md`
- `wdt_audit_references.bib`
- `variables_available.txt`, `variables.csv` (refresh after J1)
- `claude/WID_Data_Guide.md` (still says 10 of 14 on the balance-sheet window; correct to the JST-overlap gate, 8 of 16)
- `claude/audit_d1_wid_download_2026-10-16.md` (earlier manual-file review; its 11 of 14 and seam figures are superseded)
- outputs of J1 to J9
**Specific stale items:** `coverage_matrix_d1.csv` and `wdt_audit.json` (NLD, CHE, JPN 48, AUS 60, ITA 52, NOR 39, DNK 46, NLD 25, FIN 23); `provenance_register_d1.md` and the spec gate line (8 of 16, no margin, back-cast caveat); `_d3` sources now received, `_d5` and `_d6` tables now received; `placeholder_register.md` rows `house_median_gbp_m` and `adults_m`; `decision_log.md` (supersession reversal for NLD, DNK, CHE; the 17 Oct rows).
**Output:** corrected files; regenerated `wdt_audit.json` (`python wdt_audit_to_json.py --dir . --usable-years usable_years.csv`).
**Blocked by:** the jobs whose results it records.

## J12. Decision review (spec step 5)

**Goal:** for each gate D1 to D10, record pass, fallback or fail, and what the fallback changes in the claims; carry the flags.
**Give the agent:**
- `WDT_Data_Audit_Spec.md`, `claude/WDT_audit_status_2026-10-16.md`
- `decision_log.md`, `placeholder_register.md`
- all `provenance_register_dN.md` (after J11)
**Output:** `decision_review.md`; flag list for every output: `carried` UK shares 1998-2008; strict D1 grades; **D1 gate met at the threshold (8 of 16)**; UK D2 pooled grade C; D6 placeholder income profile; `mc_gdp` after 2016 unverified (waiting for K-Z); pooled c, grade C, for countries failing the 50-year test (AUS, CHE, DEU, DNK, FIN, NOR, BEL, PRT).
**Blocked by:** J11.

## J13. Model-side gaps (VAL and RATES, not audit)

**Goal:** decide build or flag for: route switching, HEC bias and persistence by route, HSC non-vacuous check, HLC pair calibration.
**Give the agent:**
- `VAL/valgen_core.py`, `wdt_kernel.py`, `wdt_core.py`, `WDT_Params.toml` (`[val_gen]`, `[val_gen.hlc]`)
- `VAL/md/VAL_placeholder_grounding.md`, `VAL/md/VAL_phase4_consolidated.md`, `VAL/md/VALGEN_build_log.md`, `VAL/md/val_numbers.md`
- `VAL/5_9_VAL_numbers.py`, `VAL/5_6_VALGEN_tables.py`
- `WDT_Code_Reference.md`
- (not in project) `test/print_hlc_calibration.py`, `OUTPUTS/RATES/rates_data.json`, `OUTPUTS/VAL/valgen_data.json`
**Output:** list of built versus flagged limitations; regenerated `[val_gen.hlc]` after the next RATES run (`python test/print_hlc_calibration.py --write`).
**Blocked by:** J10b (so a single rerun picks up all input changes). The HLC calibration is stale after any RATES run that moves W_min.

---

## File index: which jobs use which file

| File | Jobs |
|:---|:---|
| `claude/WDT_audit_status_2026-10-16.md` | J0, J1, J12 |
| `decision_log.md` | J0, J5, J10, J11, J12 |
| `placeholder_register.md` | J4, J5, J9, J10, J11, J12 |
| `WDT_Data_Audit_Spec.md` | J2, J8, J12 |
| `coverage_matrix_d1.csv`, `provenance_register_d1.md` | J1, J2, J11 |
| `d1_overlap_runs.csv`, `usable_years.csv`, `usable.csv`, `windows.csv` | J2, J6 |
| `audit_d0.md`, `d0_jst_audit.py`, `variables.csv` | J2, J6 |
| `*_d2.*` | J8 |
| `*_d3.*`, `*_d9.*` | J5, J11 |
| `*_d4.*`, `uk_holder_shares_ons.csv`, `EVAL/srs.csv` | J7 |
| `*_d5.*` | J3, J11 |
| `*_d6.*` | J4, J11 |
| `*_d7.*` | J6, J11 |
| `*_d8.*` | J1 |
| `wdt_audit.json`, `wdt_audit_to_json.py`, `wdt_audit_references.bib` | J11 |
| `claude/wid_download.py`, `wid_summarise.py`, `wid_checks.py`, `WID_Data_Guide.md` | J1, J11 |
| `WDT_Params.toml` | J3, J4, J5, J7, J8, J9, J10, J13 |
| `wdt_core.py` | J4, J10, J13 |
| `wdt_jst.py` | J2 |
| `RATES/rates_core.py` | J8 (optional), J9, J10 |
| `RATES/8_2_RATES_tables.py` | J4 |
| `WDT_Code_Reference.md` | J3, J7, J13 |
| `VAL/*`, `wdt_kernel.py` | J13 |
