# Model v1: errors (brief 001c, stage B)

Audit of `model_v1/` against `research/model-lessons/drift-register.md`. Read-only: no model file was edited, no model `main` or `run_all` was run, nothing was written outside `research/model-audit/`. Date 2026-11-15, repo at `0b4ead9` (main). Stage A note: `v1-inventory.md`.

**NEEDS THE AUTHOR (brief rule: "if the audit finds that the papers' published figures depend on a v1 error, stop and ask").** Item B1: the two C.1 denominators move a published boundary. The tolerant-zone upper bound is **α = 1.85** in the SWEEPS code path and **α = 1.80** in the VAL code path, at the same parameters (section 2, B1). Paper 5a defines C.1 with TW(α); `val_core` (paper 5 tables) divides by TW(1); `wdt_analytics.c1` (paper 9 figures) divides by TW(α). Decision wanted: which denominator is canonical. Stage C is not started.

## 1. How to read this note

Evidence tags: **[code]** read in the named file and line; **[run]** short Python snippet, in memory only, `PYTHONDONTWRITEBYTECODE=1`, `git status` clean after each run; **[json]** read from a tracked file in `model_v1/OUTPUTS/`.

Statuses, as the brief asks:
- **confirmed**: the item is present in the code today, with the evidence given.
- **not reproduced**: the item as described is not present today (fixed since the register, or never true).
- **partly**: some of the item is present, some fixed.
- **new**: found in this stage, not in the register.
- **not checked**: not tested in this stage, with the reason.

Because `import rates_core` fails (stage A: the file is `rates_core1.py`), every [run] that touches the RATES module used an in-memory alias `sys.modules['rates_core'] = importlib.import_module('rates_core1')`. No file was changed to do this. Register items that name `rates_core` are read as `rates_core1.py`.

Totals: 42 register items (A 7, B 13, C 13, D 5, E 4) and 3 new findings. Counts by status are in section 6.

## 2. Section B first (numerics): the items with numbers

### B1. C.1 has two denominators: **confirmed, affects published figures**
- Where: `wdt_core.run_pair` (line 736 on) divides by `TW_settled(1)`; `wdt_analytics.c1` (line 295 on) divides by `TW_settled(alpha)` (its docstring and its return line). `val_core` uses `run_pair`; `sweeps_core` and `16_x` use `c1`.
- Shown [run], canonical parameters, `g = 10.45%`, `N = 30`:

| α | `c1` (TW(α)) | `run_pair.net_pct` (TW(1)) | TW(α) | TW(1) | c1 / net_pct |
|---:|---:|---:|---:|---:|---:|
| 0.5 | −0.000563 | −0.000529 | 269.39 | 286.91 | 1.0650 |
| 0.8 | −0.001310 | −0.001278 | 279.99 | 286.91 | 1.0247 |
| 1.0 | 0 | 0 | 286.91 | 286.91 | n/a |
| 1.5 | +0.008829 | +0.009345 | 303.68 | 286.91 | 0.9448 |
| 1.8 | +0.017487 | +0.019101 | 313.40 | 286.91 | 0.9155 |

  The ratio of the two metrics equals TW(1)/TW(α) in every row, so the numerator (Net(α) − Net(1)) is identical and only the denominator differs. Sign never changes; magnitude differs by up to 8.5% (α = 1.8) and 6.5% (α = 0.5).
- Effect on a published output [run]: the tolerant zone (|C.1| < 2pp, `TZONE_THRESHOLD = 0.02`, α grid step 0.05, N = 30, g = 10.45%) is 0.10 to 1.85 with `c1` and 0.10 to 1.80 with the TW(1) metric. Paper 9 states the |C.1| < 2pp zone (`9_Parameter_Sweeps.md` lines 67, 125) and its figure captions say "(Net(α) − Net(1)) / TW(α)" (lines 155, 195, 231). Paper 5a line 517 also defines C.1 with TW(α), while the tables in paper 5 come from `val_core` with TW(1) (`val_core.py` header lines 30 to 36; tracked `val_data.json` meta: "common TW(1) denominator").
- So: paper 9 code and captions agree (TW(α)); paper 5 code (TW(1)) disagrees with the paper 5a definition (TW(α)). N-crossing counts are unaffected (they depend on the sign of the numerator).
- Open for the author: which denominator is canonical. Not fixed.

### B2. `5_4` reads legacy keys: **partly**
- `5_4_VAL_charts.py` now reads `matrix_net`, `matrix_tw_cost`, `matrix_pv` (lines 161, 162, 454, 455, 723 to 725) [code]. The register description is out of date.
- Still true: it reads `surfaces` (line 639) and `val_core` still writes the legacy keys `matrix` (593, 811), `c1_matrix` (735), `surfaces` (799) as aliases. Nothing crashes. The fig 7.2c title is wrong (see D4).

### B3. `5_3` prose stale: **partly**
- Fixed: C.1 now says it divides by TW(1) (`5_3` header, line 22); the C.12 section text describes the true-value PV (lines 288, 317); the footer says v1.1 (line 559), matching `val_core` meta (line 1125).
- Confirmed [code]: the C.11 "Purpose" paragraph (lines 78 to 84) still lists "excess periodic net tax" as one of three summands. The decomposition in `wdt_core.decompose_tw_advantage` uses W_sell_delta, refund_delta, settle_delta; the check from stage A gave identity residual 1.6e-13 at α = 1.5, g = 10.45%, N = 30 (W_sell_delta −4.0058, refund_delta −24.6958, settle_delta +3.9188, tw_advantage 16.7713). The paragraph two lines later (125) says excess periodic tax "is not equal to W_sell_delta".
- Confirmed [code]: `5_5_VAL_generate_worked_examples.py` line 77 still says "Python model v1.0".

### B4. `8_2.write_report` uses undefined `model`: **confirmed**
- `8_2_RATES_tables.py` line 109: `py_tcm_burden = model.run_tcm(...)`. [run] after the import alias: `hasattr(module, 'model')` is False and `model` is not in builtins, so the branch (taken when `py_tcm_burden is None`) raises `NameError`. Not triggered today because `main` passes `py_tcm_30` (line 38). The branch itself was not executed.

### B5. Burden sweep N: **confirmed**
- `rates_core1.tcm_burden_sweep` (line 929) runs `run_tcm(p, N=p_base['N'], N_fill=1)` (line 960). [run] `p['N'] = 19`, `p['N_fill'] = 19`, `p['N_val'] = 30`, `p['tcm_N'] = 30`. So the sweep runs at N = 19 while `16_4` titles it "fixed N={p_base['tcm_N']}" (= 30) (`16_4` lines 193, 340) and the canonical burden horizon is 30 (`build_rates_output` line 1532 uses `burden_N`). Which N is intended is a design question; the title and the computation disagree by 11 years.

### B6. Two rate functions: **confirmed (boundary only)**
- [run] at `W = W_min = 2.0`: `wdt_core.tau` returns 0.150000; `wfr_core.ProgressiveRateFunction.rate` returns 0.000000 (`wfr_core.py` line 606, `W <= W_min`). The `effective_rate` midpoint approximation is close to the exact mean rate over the interval: absolute differences 5.1e-08 (W 3 to 6), 4.1e-06 (3 to 30), 4.5e-05 (10 to 100), so the register's concern about the midpoint is **not reproduced** as material. Effect on WFR outputs not measured (would need running `wfr_core`).

### B7. Stale canonical marker: **confirmed**
- `sweeps_core.py` line 272: `'τ₀=20% (canon)': make_p(tau_0=0.20)`; `WDT_Params.toml` line 51 and the cache meta (`canon_tau0 = 0.15`) say 0.15. Whether `16_2` marks that bar by index: not checked (grep for "canon" in `16_2` finds nothing).

### B8. Synthetic scenario tangled: **confirmed**
- TOML `[synthetic_scenario]`: `mu = 0.07`, `amplitude = 0.08`, `period = 10` (lines 543 to 546); its comments say mu = 2%, A = 4%, g between −2% and +6% (lines 527 to 546). [json] `sweep_cache.json` `rates_s.synthetic_params` = mu 0.07, amplitude 0.08; the cached 80-value series runs from −0.61% to +14.61%. So the actual scenario is neither the commented one nor what the comment says it stress-tests.
- Fallback literals disagree: `sweeps_core` amplitude 0.05, mu `hist_mean` (lines 353 to 361); `wdt_analytics` mu 0.1045, amplitude 0.05 (lines 965 to 967). The `16_3` fallback was not found by grep.
- Which values the papers state: not checked. Not picked in passing (per the register).

### B9. `val_core._to_json_safe` does not null NaN or inf: **confirmed**
- [run] input `{'a': nan, 'b': inf, 'c': 1.0}` returns the same values; `json.dumps(..., allow_nan=False)` then raises `ValueError: Out of range float values are not JSON compliant: nan`. The other three sanitisers return `None` for both (`rates_core1._sanitise`, `wfr_core._sanitise`, `sweeps_core._jsonify`).

### B10. Fixed-N assumptions in `val_core._validate`: **not checked**
- `_validate` (line 941) reads `N_val`, `g_vals` and `n_actual_vals` and raises `AssertionError("VALIDATION FAILED ...")` on a failed check (line 957). Showing that a changed TOML grid fails it needs running `val_core`, which is out of scope.

### B11. `16_1` simulates: **confirmed**
- `16_1_SWEEPS_V_tables.py` calls `run_sim` at lines 131, 132, 166, 167 and `n_crossing` at line 256, though its docstring (lines 7 to 9) says everything comes from the cache. `main` prints "Section B.9: figure index..." (line 305) and no `section_b9` function exists (grep: only `section_b1` to `section_b8`).

### B12. `8_3` presentation simulating: **confirmed**
- `simulate(...)` at line 583. `g_sell` is assigned (line 582) and never read (one grep hit). In `fig_7_3b`: legend label `f'Zero coverage ({n_zero_cov} years'` is missing `)` (line 764); the suptitle ends with a dangling `|  ` (line 776).

### B13. Static claims in prose: **confirmed (static), currently consistent**
- `16_3_SWEEPS_R_tables.py` lines 361 to 362: "100% success across all 73 start years" is typed text. [json] check: in `rates_output.json` the 73 sweep rows have no row with a failure year set (0 of 73), so it holds on the tracked data today; the code does not check it.

## 3. Section A: hardcoded values (7 items)

| ID | Item | Status | Evidence |
|:---|:---|:---|:---|
| A1 | `rates_core` fixed numbers | confirmed | `rates_core1.py`: `max_N=71` (lines 19, 211, 376, 548, 726, 1095), `COVERAGE_WINDOWS = [5, 10, 20, 50]` (115), `burden_N=30` default (1476, should be `N_val`), `assert len(p['returns']) == 73` (148), `CYCLE_BUCKETS` (790), duplicated in `wdt_style.py` (179) |
| A2 | `sweeps_core` grids and variants | confirmed | `sweeps_core.py`: `tau0_fine range(5,45)` (110), `taum_fine` (144), `k_fine` (161), `wmin_fine` (177), `v0_points` (162), `g_plateau` (133), `under_alphas` redefined locally (132), `variants` dict (269 to 283) |
| A3 | `val_core` example parameters and grids | confirmed (listed lines) | `val_core.py`: `0.944` (898), `0.02` auction cost (905), `g_scenarios` (602), `n_right range(5,61)` (722), `[1.2,1.5,1.8,2.0]` (724, 781); the §J to §N example parameters beyond those lines were not individually checked |
| A4 | `wfr_core` constants | confirmed (listed lines) | `wfr_core.py`: `W0_NORM`, `TARGET_ET`, `GAMMA_VALS`, `GAMMA_CEN` (681 to 684), `W0_vals` multiples (1023), `tau_cgt = 0.24`, `V_ref = 10.0`, gain 0.50, `T=5` (1127 to 1132), tier-to-bracket map (1196), `range(base_yr, base_yr + 73)` (1504); whether the TOML `wfr_gamma_vals` duplicates `GAMMA_VALS`, and the leverage grid: not checked |
| A5 | `ldw_core` all hardcoded, no `load_params` | confirmed | `ldw_core.py`: `IT_BASIC_RATE = 0.20` (76), `VAT_RATE` (96), `_PAPER_SALARIES` (285); grep for `load_params` finds nothing |
| A6 | Typed numbers in presentation text | confirmed | `5_5` lines 67, 77, 359, 417 ("£20.000m/£16.000m/£10.000m", "g = 7%, N = 5/10, τ = 15%"); `19_3` lines 758 to 759, 1009; `19_2` lines 450 to 451, 513, 691; `8_3` lines 382, 422, 773. The corner labels "+3.45pp" and "−4.55pp" equal the TOML tier differentials (lines 222, 237), so they are hardcoded but currently correct; "£2.86m" and "£139.6m" were not checked against `wfr_results.json` |
| A7 | `rates_core._compute_coverage_windows` uses `3.0 * budget_base` | confirmed, latent | the function is `_tcm_coverage_windows`; `rates_core1.py` line 364: `lrr_tgt_ext = (3.0 * budget_base * ...)` where lines 433, 582, 1115 use `lrr_years`. [run] canonical `lrr_years = 3.0`, so the two agree and no tracked output is affected today. Differential run with `lrr_years != 3` not done |

## 4. Sections C, D, E

### C. Layering and duplication (13 items)

| ID | Item | Status | Evidence |
|:---|:---|:---|:---|
| C1 | Four JSON sanitisers | confirmed | `val_core._to_json_safe` (89), `rates_core1._sanitise` (1572), `sweeps_core._jsonify` (75), `wfr_core._sanitise` (717); behaviour differs (B9) |
| C2 | `_weighted_quantiles` unused copy | confirmed | canonical `rates_core1.py` 887; `16_4_SWEEPS_R_charts.py` 114 defines it, no call found |
| C3 | Core-to-core and presentation-to-core imports | confirmed | `sweeps_core.py` 68, `wdt_analytics.py` 99 import `rates_core`; `8_2` 51 to 52, `8_3` 55, `16_3` 26, `16_4` 33 import it; `5_3`, `5_4`, `5_5` import `val_core`; `16_3` 27 to 28 imports `8_2` by `importlib`; `8_2` imports private `_tcm_coverage_windows` |
| C4 | `wdt_analytics` hosts core and chart code | confirmed (unused import not checked) | `run_param_sweep` (706), `run_g_sweep` (871), `run_synthetic_sweep` (929), `draw_c1_heatmap` (503); imports `median, mean, success` from `wdt_fmt` (98) |
| C5 | Capitalisation logic in four places | confirmed, in sync today | `rates_core1.run_ssm` (376), `_ssm_stripped` (537), `_tcm_coverage_windows` (1078), `wdt_core._ssm_lrr_fill_year` (991). [run] `_ssm_stripped` and `wdt_core._ssm_lrr_fill_year` both give LRR fill year 19 and SRR fill year 3 at canonical, so they do not diverge on that output |
| C6 | `load_params` is slow (full SSM pass per call) | not reproduced | `wdt_core.load_params` does call `_ssm_lrr_fill_year` (once, sets `N_fill`), but [run] it took 0.097 s (`wdt_core`) and 0.031 s (`rates_core1`); stage A measured 0.05 s |
| C7 | `wfr_core` own paths and `load_params` | confirmed | `wfr_core.py` 72 (`TOML_PATH`), 73 (`OUTPUT_ROOT`), 82 (`module_output_dir`), 93 (`load_params`) |
| C8 | `rates_core` mixes console reporting; imports private `_ssm_marginals` | confirmed | `rates_core1.py` 693, 751, 982, 1274 (`run_scenario_profiles`, `report_*`); 105 to 107 import `_ssm_marginals` |
| C9 | `16_2` is three scripts concatenated | confirmed | `_load` defined at 20 and 32, `_save` at 24 and 37; mid-file docstrings at 41, 50, 370, 380, 602, 613 |
| C10 | `16_4` module-level mutable state | confirmed (print not found) | `BASELINE`, `SWEEP_*` at lines 50 to 56; "prints the whole params dict": grep finds no such print |
| C11 | Presentation bypasses shared style | confirmed (`19_3` only checked) | `19_3` defines `_style_ax` (132), saves at `DPI_SCREEN` (125), 35 lines with `_style_ax` or inline hex; `16_2`, `16_4`, `8_3` inline hex and `_FIG_*`: not checked |
| C12 | `5_3`, `5_5` raw `lines.append`; `5_5` uses `date.today()`; `ldw_core` duplicates `wdt_md` separator map | partly | `5_5` line 439 `date.today().isoformat()`; `5_3`, `5_5` use `lines.append`; the `ldw_core` separator map was **not found** by grep (`wdt_md._SEP` at 64 is the only map) |
| C13 | Cache path computed two ways | confirmed | `sweeps_core.py` 71 `Path(__file__).parent / 'OUTPUTS' / ...`; `16_1`/`16_2`/`16_3` use `out_dir('.').parent / 'OUTPUTS' / ...` (lines 23, 17, 32) |

### D. Layout and naming (5 items)

| ID | Item | Status | Evidence |
|:---|:---|:---|:---|
| D1 | Output layout and JSON names | confirmed | [code] `ls`: only `OUTPUTS/WFR/charts/` exists; no `tables/` folder; `sweep_cache.json` in `OUTPUTS/` root; JSON names `val_data`, `rates_output`, `wfr_results`, `sweep_cache`; `LDW` holds only a markdown file |
| D2 | `run_all.bat` typo and stale comment | confirmed, wider | `run_all.bat` line 15 `sweeeps_core.py`; line 14 `rates_core.py` (also absent, new vs register); lines 4 to 5 mention helper modules that no longer exist |
| D3 | Script numbering not uniform; renames decided | confirmed (not done) | file names are still `5_3`, `5_4`, `5_5`, `16_1` to `16_4`, `8_2`, `8_3`, `19_2`, `19_3`, and `ldw_core.py` has no `21_2` script |
| D4 | Figure prefixes and numbers inconsistent | confirmed | tracked PNG prefixes: `wfr_fig` 27, `SWEEPS_v_fig` 21, `val_fig` 14, `sweeps_r_fig` 12, `rates_fig` 10; `5_4` line 435 titles fig 7.2c "Figure 7.3"; `16_2` lines 87 and 157 title both the τ₀ and τ_m heatmaps "Figure 3.1a"; `16_4` docstring lists `sweep_fig_01` to `05` (lines 8 to 12) while files are `sweeps_r_fig_*`. The `8_3` docstring claim (`rates_fig_01…`): not reproduced (no such text found) |
| D5 | `generate_charts` flag unused | confirmed | parsed at `wdt_core.py` 1105, `true` in TOML line 36, read by no other `.py` file (grep) |

### E. Stale documentation (4 items)

| ID | Item | Status | Evidence |
|:---|:---|:---|:---|
| E1 | `WDT_Model_Reference.md` stale | confirmed (partly checked) | `rates_model` appears 11 times (module is `rates_core1.py`); mentions `5_6` (line 467), `16_5` (472), `16_6`, `16_7` (457, 473), "ten output scripts" (line 15); `FIGURE_REGISTRY` and `generate_charts` mentions: not checked |
| E2 | Docstring self-names | confirmed | `sweeps_core.py` 2 ("16_0_compute.py"), `ldw_core.py` 2 ("wdt_ldw.py"), `wfr_core.py` 18 (`OUTPUTS/WFR/wfr/`), `16_1` 7, `16_2` 45, `16_3` 373 ("16_6_RATES_S_tables.py") |
| E3 | `WDT_Params.toml` stale | confirmed (partly checked) | `version = "v7"` (30); comments cite `module5_sweeps.py` (472), "3.4.1 to 3.4.4" (307), `wfr_start_years_full` (508, no such key defined by grep); the `[sweep]` duplication of `[rate]`, `[val]`, `[tcm]` values: not checked |
| E4 | Tests | partly | the register's "480 tests" are not in the repo. Today: 4 scripts, 320 assertions pass in 3, the fourth (`test_wdt_analytics.py`) cannot import (stage A). `test_wdt_analytics.py` still calls `A.success` (line 413); whether it needs v8 updates: not checked (cannot run) |

## 5. New findings (not in the register)

- **N1. Tolerant zone differs by denominator**: 1.85 vs 1.80 at canonical parameters (B1). New as a measured effect on a published boundary.
- **N2. Paper text and code disagree on C.1**: `5a_Valuing_Wealth_Mathematical_and_Simulation_Appendix.md` line 517 defines C.1 with TW(α), while `val_core` computes TW(1) for paper 5 (B1).
- **N3. `run_all.bat` also names `rates_core.py`**, which does not exist (D2). Together with `sweeps_core`/`16_x` this is why 8 of 16 entries cannot start (stage A).

## 6. Coverage check

Every item in the register has a status above. Counts by status:

| Status | Items | IDs |
|:---|---:|:---|
| confirmed (includes "latent", "in sync today", "wider") | 36 | A1 to A7; B1, B4 to B9, B11 to B13; C1 to C5, C7 to C11, C13; D1 to D5; E1 to E3 |
| partly | 4 | B2, B3, C12, E4 |
| not reproduced | 1 | C6 |
| not checked | 1 | B10 |
| **Total** | **42** | |

Some "confirmed" items have a named sub-claim that was not reproduced or not checked (B6 midpoint concern, B7 index marking, A3, A4, A6, C4, C10, C11, D4 `8_3` docstring, E1, E3). Those sub-claims are named in the item's own row or paragraph.

What was not done and why: `val_core`, `wfr_core`, `rates_core1 main`, any table or chart script and `run_all` were not run (brief: "running the full model scripts" is out of scope), so effects on `OUTPUTS/` files were not measured except through the tracked JSON. The tracked outputs are dated 2026-09-28 to 2026-09-30 and were not regenerated.
