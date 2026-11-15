# VALGEN tables and figures: build log (3 Oct)

Status (5 Oct 2026): VALGEN set built (steps 1 to 4 and 6 of `VAL_tables_figures_plan.md`), plus Phases 0 to 3 and the Phase 4 grounding changes at the end of this log. Step 5 (old-figure gap tables) written but NOT run on real data; `val_core.py` and `val_data.json` are still not in the Project.

## File layout (4 Oct, follows the EVAL pattern)
```
model/
├── WDT_Params.toml, wdt_core.py, wdt_fmt.py, wdt_md.py, wdt_style.py     (shared, unchanged location)
├── VAL/
│   ├── valgen_core.py, 5_6_VALGEN_tables.py, 5_7_VALGEN_charts.py, 5_8_VAL_gap_tables.py
│   ├── test_valgen_pairs.py, test_gap_tables_fixture.py
│   └── VALGEN_build_log.md, VAL_rewrite_plan.md   (plus VAL_tables_figures_plan.md)
└── OUTPUTS/VAL/
    ├── valgen_data.json   (and legacy val_data.json)
    ├── charts/
    └── tables/
```
Scripts in `VAL/` put the model root on `sys.path` (two-line bootstrap at the top) so `wdt_core` etc. import; run from anywhere, e.g. `python VAL/valgen_core.py`. All outputs now go to `OUTPUTS/VAL/` (was `OUTPUTS/VALGEN/`). Moving files changed no numbers: tests 18/18 and 5/5 pass; table G2 regenerated to the new path.
Still to do on the user's side: `val_core.py` and the old `5_3`/`5_4`/`5_5` scripts are not in this workspace, so they were not moved. Their output calls (`out_dir('VAL')` straight into the folder) still write flat into `OUTPUTS/VAL/`; they need `charts/` and `tables/` subfolders to match.

## What exists
| File | Role |
|:--|:--|
| `valgen_core.py` | adds `p5.headline` (G12 per-alpha best response), `worst_pv` / `worst_state` per search cell (G8). 64 checks pass. |
| `5_6_VALGEN_tables.py` | 13 table builders G1 to G13, `PAIRS`, `BUILDERS`, `_check_stamp`. |
| `5_7_VALGEN_charts.py` | 13 figure builders, same `PAIRS`. |
| `test_valgen_pairs.py` | pairing test: same ids and JSON keys, PNG and table exist, 3 table values appear in the figure series, no literal parameter values in script strings. Run `python test_valgen_pairs.py`. |
| `wdt_style.py` | new palette entries: C_CONV, C_WDT, C_WDT_BASE, C_CEILING, C_PASS, C_FAIL, RULE_COLOURS, CMAP_GAIN. |
| `WDT_Params.toml`, `wdt_core.py` | new `[val_gen] headline_rules`, `example_alphas`; new `[val]` keys `rate_table_W`, `cost_curve_alphas`, `surface_table_g`, `reversal_plateau_slope`, `reversal_g_cutoff_pct`. |
| `5_8_VAL_gap_tables.py` | gap tables for old Fig 5, 7.1b, 7.1c, 7.2b, 7.2c. Reads `OUTPUTS/VAL/val_data.json` directly (same chart keys as `5_4_VAL_charts.py`). Output `OUTPUTS/VAL/tables/val_table_gap_*.md`. Old scripts untouched. |
| `test_gap_tables_fixture.py` | plumbing test on a synthetic fixture. |

Run order: `python VAL/valgen_core.py`, then `VAL/5_6_VALGEN_tables.py`, `VAL/5_7_VALGEN_charts.py`, `VAL/5_8_VAL_gap_tables.py`.

## Numbers that moved
None. Every key of the pre-change `valgen_data.json` is identical (re-checked after the G2 change). New keys only: `examples['0.5']`, `p5.headline`, `search[...].worst_pv`, `.worst_state`, one added check (`headline_slice_never_beats_library_best`).

## Drift noticed
- G12 reads `p5.headline`, not `p5.search[...].all` as the plan says.
- WDT alpha = 0 is undefined (Route C units = L / declared price). The conventional curve still draws it.
- alpha = 0.01 exists only in the headline slice (library has no 0.01), so the library-subset check covers library alphas only.
- G12 base rule at lambda = 0 reaches +45.8% at alpha = 0.01 against +58.2% conventional. The base rule alone is weak without verification; the candidate is +4.1%.
- Candidate rule fails G1 at lambda 0, 1, 2% and passes at 5, 10%. G3 fails on stake at every lambda (near-miss -2.1% at 5%, -2.3% at 10%).
- G13: every rule shows exactly 0.000% honest cost. Honest declarations never touch the caps or resets.
- G2 now shows honest, understater (0.5) and overstater (2.0) via `[val_gen] example_alphas`. The ledger's "declared W" is the declared value of units still held, so the honest case sits below true value as units are sold.
- Step 5 NOT run on real data: `val_core.py` and `val_data.json` are not in the Project. Only a synthetic fixture was tested (shapes, keys, values present in the JSON). Run `python 5_8_VAL_gap_tables.py` next to the real JSON and read the tables.
- Old `val_data.json` stores cost curves and surfaces in percentage points of honest TW(1), tau as a fraction. Gap tables label the unit in the header.
- Old `5_4_VAL_charts.py` hardcodes constants that the gap tables took from TOML instead: Fig 7.2b slope tolerance 0.05, g cutoff 50% (index `50/0.1`), plateau search cap 400 steps and fallback 40.0; Fig 7.2c/7.1c alpha lists [1.2,1.5,1.8,2.0]; Fig 5 axis ticks and label positions; Fig 7.1b colours by g. Table 7.2b searches to the cutoff, not the old 400 steps, so plateau onset can differ from the figure's label if the grid is not 0.1%. Fix by moving these into TOML when the old charts are next touched.
- New bare filenames written to the Project landed under `claude/`.

## Left to the user
Final figure numbers; separate paper or paper 5 addendum; which old figures retire; audits in the conventional baseline; whether 1% / 1% / 2% thresholds stay. Decided 3 Oct: G12 axis stops at alpha = 1 (no overstatement side); G12 keeps the base rule.

## Phase 0 (4 Oct 2026): names registry
- `[names.val.<ACR>]` registry added to `WDT_Params.toml`; loaded as `p['names_val']`; table generated to `OUTPUTS/VAL/tables/val_names.md`.
- Output ids G1..G13 renamed UCC, WLG, CDS, RIS, DSH, VSY, ABL, VMP, FBR, PSS, GLM, HLC, HCS; files now `val_table_<ACR>_<slug>.md`, `val_fig_<ACR>_<slug>.png`.
- Verdicts G1/G2/G3 renamed BRG/HSC and split SPT (state PV) and SST (state stake). JSON: `BRG_pass`, `SPT_pass`, `SST_pass`, `HSC_cost`, `n_conflict_spt/sst`.
- TOML/JSON keys: `g1_tol`->`brg_tol`, `g2_tol`->`hsc_tol`, `tol_rev`->`state_tol`, `tol_rev_sens`->`state_tol_sens`.
- Check: regenerated JSON equals baseline numerically under the key map (no value differences). Tests: pairs + registry pass.
- Deferred: JSON block prefixes p2..p5 still legacy; to rename with the Phase 2 core merge.

## Phase 2, slice 1 (4 Oct 2026): DMG
- `_p5_dmg` in `valgen_core.py`; TOML `dmg_rules`; JSON `p5.dmg`. 35 scenarios (5 g x 5 lambda, 2 shocks x 5 lambda) per rule set, 428 strategies.
- Result: 6 strategies (Route C overstating in generation 0 only, alpha 1.2 to 5.0) gain in every scenario under BASE and CORR; minimum gain <= +0.04%; none above brg_tol. Core run time rises by about 2 minutes.
- Spec section 10 corrected: the library and headline grid already cover overstatement to alpha 10.

## Phase 2, slice 2 (4 Oct 2026): HEC
- `_hec_paths`, `_p5_hec`; TOML `hec_sigmas` [0, 5, 10, 20]%, `hec_paths` 200, `hec_phi` 0.5, `hec_seed` (all placeholders pending the Phase 4 appraisal-error brief); JSON `p5.hec`.
- Honest error is multiplicative lognormal AR(1) on Routes C and D, independent paths, error-free honest as reference.
- Result: honest error is mildly profitable on average under BASE at lambda 0 (mean gain +0.10%, +0.24%, +0.62% at sigma 5, 10, 20%; 80 to 88% of paths gain) because downside errors refund. Under CORR the mean falls to +0.03 to +0.07% and the gain share to 56 to 70%. State stake falls 0.2% to 2.3% (BASE) and 0.1% to 2.0% (CORR). Verification (lambda 5%) shrinks both.

## Phase 2, slice 3 (4 Oct 2026): UOS (understatement vs overstatement by Route C share)
- `_direction`, `_p5_direction`; TOML `c_share_vals` [2, 5, 8, 15, 25]% (placeholder pending the Route C share brief); JSON `p5.uos`. Best gain by deviation direction (under, over, mixed), rule set (BASE, CORR), lambda (0, 5%).
- BASE: best gain grows with C share; at 8% it is +24.9% (under) and +18.6% (over) at lambda 0.
- CORR, lambda 0: under +1.5% (C 2%) to +9.1% (C 25%); over +1.2% to +7.2%.
- CORR, lambda 5%: under +0.3% to +1.6%; over +0.4% to +3.1%. Overstatement is the larger channel from C share 15% (over +1.50% vs under +1.00%; at 25%, +3.10% vs +1.56%), and exceeds the 1% BRG placeholder from 15%.
- Reading: BND holds (gains bounded, scale with C share); NDS and HLR depend on the C share and lambda ranges that Phase 4 must ground.

## Phase 2, slice 4 (4 Oct 2026): LIFE block in the single core
- `_life_results` in `valgen_core.py`; JSON `life`: alpha x g grid at N_val (gain, net, pv, pv_rel), alpha x N at g0, alpha x g x rho PV grid, and worked examples J, K, N run through `run_life`. Inputs in TOML `[val_gen.life_examples.J|K|N]` (were hardcoded in legacy `_compute_examples`).
- Check: examples J, K, N match legacy `run_sim` to 4e-15 (TW_settled and Net_settled). The LIFE bridge over the legacy grids already passes at 1e-9 in every run.
- Legacy outputs now covered by the core: C.1, C.1-TW, C.12 (net, TW, PV heatmaps), C.7/C.8 (N sweep), C.12 rho sweep, examples J, K, N.
- Legacy outputs not yet re-homed (D5 audit, recommendation): examples L, M (closed-form arithmetic, move to Route D via the core); C.2, C.3 (beta), C.4 (k x V0), C.5 (k x alpha), C.6 (refund protection), C.9, C.10 (history), C.11 decomposition, tolerance zone and breakeven rho, uncertainty Monte Carlo. Recommend: drop C.2, C.3, C.9 and the Monte Carlo (superseded by HEC); keep C.6 as the HSC single-life view; keep C.4, C.5 only if the draft cites them; re-home C.10, C.11 and the breakeven if the draft needs them. Decision pending with the user.

## Phase 2, slice 5 (4 Oct 2026): worked examples L and M through the core
- `_route_d_examples`; TOML `[val_gen.route_d_examples.L|M]` (inputs were hardcoded in legacy `_compute_examples`, including the 0.944 soft factor and the 2% auction cost); JSON `life.route_d_examples`. Single-route family runs, no death event (terminal settlement).
- L (V0 8, g 5%, 15 years): annual settlement (Route A) demands £1.091m cash-equivalent over 15 years (£0.060m in year 1, £0.096m in year 15); Route D accrues £1.306m with no annual payment, settled in units at true value at the end. Legacy text said £1.310m and "no liability accrues": under the current mechanism a liability does accrue (A_D). Prose and VAL §6.1 argument need restating.
- M (B0 5, g 5%, reset at 10, end at 15): hard reset settles £0.473m at year 10 (legacy £0.474m) and £0.264m at 15; no reset settles £0.813m at 15 (legacy £0.815m). Soft reset (94.4% declared at year 10 only) ends within 0.01% of no reset: family £9.5816m vs £9.5817m. Hard reset leaves the family £0.039m lower (£9.5424m) because early settlement forgoes growth on the units paid; the 2% auction cost (£0.163m) is not in these figures.
- Reading for the draft: "certainty, not avoidance" survives; the soft reset gives no measurable advantage over no reset in this engine; any claim that a soft reset saves tax needs a different declaration pattern.

## Phase 3, slice 1 (4 Oct 2026): four new pairs
- New registered outputs and paired table/figure builders: DOMG (dominance grid), HERR (honest error), UOS (understatement against overstatement by Route C share), LGR (single-life gain grid, legacy C.1-TW). Registry test no longer requires a legacy id. All pair tests pass.
- New figures carry no title (caption lives in the table); the older figures still print "Figure <ACR>:" titles and are to be swept next, with the test updated in the same pass.
- LGR reading: in a single life an overstater gains in almost every growth cell (alpha 2.0: +12.4% at g 5.9%, +3.0% at g 0.4%), and a deep understater gains only at g 25.4% (alpha 0.1: +3.6%). Same direction as UOS: the overstatement channel is real under the base rule (single life has no verification and no corrective auction).

## Phase 3, slice 2 (4 Oct 2026): titles removed, numbers register
- All 13 older figures lose their "Figure <ACR>:" image titles; `test_no_figure_titles_in_images` added. 24 pair and structure tests pass; gap fixture tests pass.
- `5_9_VAL_numbers.py`: numbers register (24 named numbers with source key and meaning) to `OUTPUTS/VAL/val_numbers.json` and `tables/val_numbers.md`. Prose will cite ids, never values.
- Correction to the slice 3 reading (UOS): under CORR at lambda 5% overstating beats understating at every Route C share in the sweep (UOS_CROSS_CAND is the first share, 2%), but the margin is under 0.1 pp until 8% and widens from 15% (+1.50% against +1.00%; +3.10% against +1.56% at 25%). The best gain exceeds the 1% BRG placeholder from a 15% share (UOS_BRGC_CAND).

## Phase 3, slice 3 (4 Oct 2026): LNS pair and example tables
- LNS pair (single-life holding-period sweep, legacy C.8): overstating gains stay positive at every holding period to 60 years (alpha 2.0: about +12% at 10 years, +6% at 55 to 60 years); understating loses and loses more beyond 40 years. 25 tests pass.
- `5_10_VAL_examples.py`: table-only outputs for the five worked examples, ids DEF (J), DIL (K), RDD (L), VOL (M), FEX (N), registered with kind `example`. Example N reproduces the legacy figures (net tax 1.104, 1.473, 0.738; terminal wealth 15.304, 14.543, 16.065). Examples J and K reproduce legacy to machine precision (checked in slice 4).
- Note for prose: FEX shows the overstating founder ends 4.97% ahead of honest. The "forecast exposure" claim cannot stand as written; it must be re-argued from the UOS and DOMG evidence.

## Phase 4 (5 Oct 2026): grounding changes
- Decisions: Route C is valued at the owner's belief on the assessment date, with no marketability-discount rule; honest bias is not modelled; base rho = 3.5% real (HMT Green Book STPR, years 0 to 30). Evidence and corrections in `VAL_phase4_consolidated.md` and `brief_phase4_grounding.md` (4.3, 4.4).
- Config: `rho` 0.035; `rho_sweep` gains 0.035; `rho_display` shows 0.035 and 5%; `c_share_vals` gains 0.40 (stress point, judgment); optional `hec_phi_C` and `hec_phi_D` (default `hec_phi`, so no HEC number moves); stale `[names.val]` notes for DOM and HEC fixed; kind comment fixed.
- Code: `wdt_core.load_params` reads the two optional keys; `_hec_paths` uses them (checked identical to the old paths when equal); JSON `p5.hec` gains `phi_C`, `phi_D`; HERR caption handles both; `5_9` gains `RHO_BASE`, `LAMBDA_BASE`, `LAM_MINPASS_*`, `SST_MINTOL_*`, `SPT_MINTOL_*`.
- Checks run: all files compile; `load_params` loads; dry run passes; HEC paths unchanged; no literal parameter value in the 5_6 and 5_7 strings with rho = 3.5%; the new register ids run on a synthetic fixture. NOT run: `valgen_core.py` in full, the pair tests (they need `valgen_data.json`), `5_9` and `5_6` on real data.
- Tested directly: gain and state stake do not depend on rho, only `pv_rel` does. Constant alpha_C of 0.5 to 0.8: gain +0.05% to +0.37% at lambda 0, -0.18% to -1.41% at lambda 5%; state PV moves by at most 0.22%.
- UOS at a 40% Route C share (CORR, lambda 5%): best gain +5.4% overstating, +2.7% understating (25%: +3.1% and +1.6%, matching the register). BASE at lambda 5%: +24.8% and +4.4%.
- Numbers that move on the next full run: `UOS_OVERMAX_*` and `UOS_UNDERMAX_*` (the sweep now reaches 40%), possibly `UOS_CROSS_*` and `UOS_BRGC_*`; every PV-based table (CDS, PSS, SPT flags, life `pv`, `by_rho`); the UOS table and figure gain a column. The BRG, DMG, HEC, SST and LIFE ids should not move; if they do, something other than these changes is responsible.
- Not done: route-switching strategy family; HSC made non-vacuous (apply HEC error in the market-fall scenario); `5_9` and `5_10` still have no tests of their own.

## Parameter changes and the plan fixtures (5 Oct 2026)
- `plan_s1_no_verification_table` and `flat_rate_stake_equals_plan` compare against values quoted at the baseline calibration (tau_0 0.15, tau_m 0.70, k 0.001, W_min 2.0, V0_m 20, g 0.1045). They failed on any other rate parameters. They are now skipped (reported as SKIP, not PASS) unless the parameters they depend on equal `PLAN_S1_BASELINE`; the JSON key `p2_plan_fixture_applies` records which case applies, and the UCC table caption and figure say so.
- `test_valgen_pairs.py`: zero-valued parameters are excluded from the literal-in-string test (W_min = 0 formats as "0.0%", which the CDS chart legitimately contains).
- Checked on tau_0 0.30, tau_m 0.90, k 0.005, W_min 0: all validation stages pass, the full run completes, tables, charts, register and examples build, 25 of 25 tests pass. The BRG verdicts change with the calibration (candidate rule, best response +9.8% at lambda 0 and +1.0% / +1.6% at lambda 5% / 10%), so verdicts do not transfer between calibrations.
- `[sweep]` canon keys (`tau_0_canon` etc.) are separate from `[rate]` and were not changed.
