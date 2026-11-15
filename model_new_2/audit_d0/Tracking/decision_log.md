# WDT data audit: decision log

Date: 17 Oct 2026 (first written 15 Oct). Spec deliverable (section 5). Status and gate outcomes: `WDT_audit_status_2026-10-16.md` (updated evening 16 Oct). Job plan: `WDT_research_completion_jobs.md`.

## Decisions

| Date | Area | Decision | Basis |
|:---|:---|:---|:---|
| 14 Oct | D1 | Identity route across usable-year gaps: solve c per contiguous JST run and pool. | User |
| 14 Oct | D1 | Grading convention: strict (any documented definitional gap caps at B). | User |
| 14 Oct | D1 | Pooling weights and minimum run overlap: suggested 20 years; **settled 16 Oct (below)**. | Settled |
| 14 Oct | Order | Close D4 open items before D3. | User |
| 15 Oct | D4 | Household tranche matches US Z.1 households and nonprofits: UK Individuals plus Charities etc. | User |
| 15 Oct | D3 | UK geography: Great Britain, WAS. | User |
| 15 Oct | D3, model | Unit is per adult. Baseline: equal split of household wealth among adults; sharing parameter s (0 as-owned to 1 equal split) as a stated scenario. s = 0 not available for property from WAS. | User, with Claude's design |
| 15 Oct | D3 | Validation target: share of adults in owner-occupier households. Basis for the first test **refined 17 Oct (below)**. | Follows the per-adult decision |
| 15 Oct | D3 | Validation tolerance: plus or minus 5 percentage points on the 10-year change. | User |
| 15 Oct | D3, model | W_min is per person. On household data with equal split it is half the median house price; `wmin_house_ratio` 1.0 to 0.5; rationale definitional. **Patch written 17 Oct; sensitivity scenario added (below).** | User |
| 15 Oct | D3 | Tolerance: three zones (pass within 5 points, inconclusive 5 to 10, fail beyond 10) and the one-sided pre-2006 test confirmed. Level tolerance: **set 16 Oct (below)**. | User |
| 15 Oct | D5 | Calibration B "comparable company burden": gross levy / GDP against corporation tax only (OECD 1200). | User confirmed |
| 15 Oct | D5 | Year basis: trailing 5-year average, latest year as sensitivity. **Confirmed 16 Oct (below).** | Claude, delegated; then user |
| 16 Oct | D1 | **WID is primary for every country** (balance-sheet window = first year all of pwfin, pwnfa, pwdeb exist; pweal = pwfin + pwnfa - pwdeb verified). Moatsos (NLD), Abildgren (DNK), Baselgia (CHE) and the 60-year AUS series are not reinstated as supplements; they stay as cross-checks with their grades and flags. | User |
| 16 Oct | D1 | Identity solve split at 1979/80 for DEU (1954-79, 1980-2025) and NLD (1880-1979, 1980-2025); other countries unsplit. Per-run minimum 20 years; pooling weight = retained overlap years. Consequence accepted: DEU falls to 41 usable years and fails the 50-year test; gate **8 of 16, met at the threshold** (JPN exactly 50, FRA 51). | User |
| 16 Oct | D1 | Back-cast headline years (before the component start) stay excluded. Sensitivity run to build: drop DEU 1980-95 and GBR 1980-87 debt years (dq 1). | User |
| 16 Oct | D5 | Year basis: trailing 5-year 2020-24 = 3.08% base case; latest year 3.47% as sensitivity. | User |
| 16 Oct | D3 | Level tolerance plus or minus 10 pp; change tolerance stays plus or minus 5 pp on the 10-year change. | User |
| 16 Oct | D5 / CORP | CIT owner-share sweep: 100%, 50%, 25%. | User |
| 16 Oct | Interpolation | Maximum gap 10 years for non-WID inputs that mark benchmarks; for WID the window start is the component start year, so no gap rule on WID series (WID exposes no interpolation flag). | User |
| 16 Oct | D4 | Mapping: 2024; rest of world 58.8%; household tranche 12.0%. | User |
| 16 Oct | `mc_gdp` | Wait for the Kuvshinov-Zimmermann appendix. `mc_gdp` after 2016 stays flagged unverified in every output; no stand-in. | User |
| 16 Oct | `adults_m` | 52.0 (18+, consistent with `pop_per_adult` 1.27). Patch written 17 Oct. | User |
| 17 Oct | D3 | Before 2006 (UK) the test is one-sided: the model's scope share must not exceed the owner-occupation share. The plus or minus 10 pp level band applies from 2006 (WAS). | User |
| 17 Oct | D3 | Basis: household diagnostic first, flagged; the adult basis becomes the primary test once adults per household by tenure is sourced (refines the 15 Oct per-adult row; no conversion until then). | User |
| 17 Oct | D1 | Pooling weight = retained overlap years (not equal weight, not capped), per-run minimum 20. | User |
| 17 Oct | VAL | Pass tolerances recorded before any run: `brg_tol` 1%, `hsc_tol` 1%, `state_tol` 2% (the current TOML values). | User |
| 17 Oct | RATES | Add sensitivity scenario `gain_ladder_wmin_full` (`wmin_house_ratio` 1.0) beside the 0.5 default; it is in the `[rates.run]` scenarios list. | User |
| 17 Oct | RATES | A rate ladder's first anchor follows the scenario's W_min (`rates_core.calibration`, helper `_anchors_at_wmin`): for 0 < W_min < second anchor the first anchor's W is W_min, its target rate unchanged; otherwise the TOML anchors are used. With ratio 0.5 the ladders start at £0.1125m. TOML anchors stay at 0.225 as the fallback. | User |
| 17 Oct | D1 | Norway stays in the pooled-c inputs, flagged: WID pweal/nninc is low (2.2 to 3.4 since 1980, against 4 to 5+ for SWE, DNK, GBR) and volatile in real terms (+11% 2020, -9% 2021, -17% 2022); the 1b metadata gives no definition or source. Flag carried into every output that uses NOR. | User |
| 17 Oct | D5 / CORP | J3 closed (`d5_hmrc_oecd_reconciliation_2026-10-17.md`): the OECD 1200 five-year total 2020-24 equals HMRC All Corporate Taxes within 0.6% (ratio 1.006); corporation tax proper is 0.93 of it. Levy target stays 3.08% of GDP, defined as all corporate taxes in HMRC's sense, so the levy replaces the bank surcharge, EPL, EGL and RPDT as well as corporation tax. `retire` share patched from 3.2% to 3.08% (`patch_NNN_ct_retire_308.py`, applied) with `[rates.levy_calibration]`. | User |
| 17 Oct | D5 / CORP | Sensitivities beside the 3.08% base case: 3.47% (latest year, 2024) and 2.86% (3.08% x 0.930, corporation tax proper only; the bank surcharge and other levies would stay in place). Both to be added to `[rates.levy_calibration]`; not yet in the TOML. | User |
| 17 Oct | D10 | `house_median_gbp_m` 0.225 relabelled in the TOML: ONS HPSSA England median, existing dwellings, year ending Dec 2017 (England £225,000; E&W £220,000); a median, not a mean. | Source check, status note 5 |

## Supersessions and fallbacks

| Item | Change | Reason |
|:---|:---|:---|
| D3 basis | Per household (early 15 Oct) replaced by per adult; 17 Oct: household diagnostic first, adult basis primary when sourced | The WDT is per adult; adults per household by tenure not yet available. |
| NLD wealth | Earlier supersession of WID (25 overlap years) by Moatsos et al. (84) **reversed 16 Oct**: WID is primary (85 overlap years, 71 kept after the 1979/80 split) | WID's composition window starts 1880, the manual download understated it. |
| DNK wealth | Earlier supersession of WID (46) by Abildgren (132, national wealth) **reversed 16 Oct**: WID primary (48 usable years, fails the gate) | Abildgren is national wealth, concept proxy, grade C only. |
| CHE wealth | Baselgia (79) not relied on; WID primary from its 1980 component start (36 usable years, fails the gate) | Baselgia annual from 1981, earlier years extrapolated. |
| AUS wealth | The 60-year series not reinstated; WID from 1977 (43 usable years, fails the gate) | WID is primary everywhere. |
| JPN | Passes on WID (exactly 50 usable years, JST ends 2019) | Replaces the earlier fail on the manual download. |
| AUS, CHE, DEU (split), DNK, FIN, NOR, BEL, PRT | Pooled c, grade C, flagged | Fail the 50-year test or have no WID series (BEL, PRT). |
| D1 gate count | 13 of 16 (and the interim 10 of 14) replaced by **8 of 16** | Earlier counts used headline or back-cast years; usable years are JST LEVY years inside the balance-sheet window, runs of 20 or more. |
| UK D2 shape | Pooled shape, grade C | No UK saving-by-wealth evidence found. |
| D6 income profile | Placeholder, labelled in the net-change display | No joint income-by-wealth cut. |

## Still open

- **Data to supply:** K-Z appendix (`mc_gdp` after 2016), IHT Table 12.1 and 12.4, ONS single-year-of-age population, adults per household by tenure, WAS data dictionary, JST house-price pages for ITA, ESP, PRT. (Corporation Tax statistics 2025 tables: received, J3 closed 17 Oct.)
- **Waiting on those:** the D3 adult-basis primary test; D6 income profile.
- **TOML:** add the 3.47% and 2.86% levy-target sensitivities to `[rates.levy_calibration]`.
- **Method:** Norway definition (pweal/nninc 2.16 in 2000, 2.61 in 2025; checked 17 Oct against the manual download: low and volatile, the 1b metadata gives no definition or source, see status below); D1 identity solve and debt-year sensitivity: run 17 Oct (`d1_identity.py`, `c_country.csv`, `c_country_debt.csv`); gate 8 of 16 in both, base reproduces the logged retained years (DEU 41, JPN 50, FRA 51, DNK 48, AUS 43, CHE 36, NLD 71); pooled c 0.0303 base and 0.0303 debt-year, GBR own c 0.0275 to 0.0272; extraction of UK and US top shares for D8.
- **Modelling (not audit gates):** re-expressing the Advani, Bangham and Leslie shares on an adult basis (they rank families); as-owned property sensitivity; within-couple gap; spousal transfers.
- **Not yet applied on the real tree** (written and tested on a mock only): the TOML patch (W_min 0.5, `adults_m` 52.0, `gain_ladder_wmin_full`, `house_median_gbp_m` comment) and the `rates_core` ladder-anchor patch. Log both in `Model/test/PATCHES.md` once applied.