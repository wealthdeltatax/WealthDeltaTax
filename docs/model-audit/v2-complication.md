# Model v2: complication and tests (brief 001c, stage D)

Audit of `model_v2/` against `model_v1/`. Read-only: no model file edited, no core, table or chart script run. Date: 2026-11-16, repo at `525c435` (branch `brief/001-model-audit`). Builds on `v2-inventory.md` (stage C); facts there are not repeated. Errors in v2 and v1 are not in this stage; where a size fact looks like a fault it is listed in section 6 only. Evidence marks as in stage C: **[code]**, **[run]**, **[doc]**.

## 1. Headline facts

1. **v2 is not larger than v1 in model Python; it is denser and has more inputs.** Model Python, excluding tests and (for v2) the 1,237 lines of WID/D0 data tooling: v1 18,136 lines (21 modules), v2 17,729. Including the data tooling v2 is 18,966. TOML: v1 554, v2 1,839 (+1,285). Line counts by `wc -l`.
2. **The three largest sources of complexity** (section 3): (1) the output layer, 5,150 lines producing 55 figures and 56 tables (+5 gap tables) against 19 figure names the papers embed; (2) `valgen_core.py`, 3,353 lines, of which 764 are seven embedded validators and 431 is one `main`; (3) `eval_core.py`, 2,718 lines, which cannot import in v2 and which no v2 file imports.
3. v2 dropped five v1 pieces: SWEEPS (`sweeps_core`, `wdt_analytics`, four `16_*` scripts: 4,214 lines), WFR output scripts (`19_2`, `19_3`: 2,200), LDW (`ldw_core`: 530) and the v1 test suite for helper modules (1,683 lines in `model_v1/test/`). It added `wdt_kernel` (564), `wdt_jst` (243), `wdt_par` (196), 40 new functions in `wdt_core` (831 lines) and the `[rates]` TOML (1,066 lines).
4. **The one test fires a warning and passes.** `python test/test_hlc_drift.py` [run, 0.2 s] prints `WARN [val_gen.hlc] is a PLACEHOLDER: HLC pair is skipped by valgen`, exit 0 (warnings are not failures without `--strict`). No other test exists in v2.
5. **27 of 101 rate scenarios are never referenced** by `[rates.run].scenarios` (74), `[rates.figures]` or another scenario [run, TOML walk]. They cost 5 lines each of the 677 lines of `[rates.scenarios]`; roughly 135 lines [estimate: median 5 keys per scenario, not summed per scenario].

## 2. What v2 added over v1, and whether a paper needs it

"Paper names it" means a grep of `source/` (case-insensitive, whole folder) finds the concept; it does not mean the paper needs this implementation. "No paper mention" is a grep with 0 files. Deciding what the rewritten papers need is stage E.

| # | Addition | Where, lines | v1 equivalent | Paper names it? | Fed to which output |
|---:|:---|---:|:---|:---|:---|
| 1 | Route kernel for A, B, C, D, verified tranche: `Book`, `assess`, `_route_tax`, `step_year`, `step_death`, `run_lines` | `wdt_kernel.py` 564 (functions 436) | none: v1 `simulate` is Route C only | Route D: 18 sources (grep); verification: papers 5, 6a, 7b, 10, 11, 19 | `valgen_core` via `_LedgerHook` 718 to 792; `rates_core` via `run_lines` |
| 2 | Real JST basis: `load_jst`, `loop_windows`, `real_basis_inputs`, `jst_basis`, `with_val_basis` | `wdt_jst.py` 243, `wdt_core` 41 | v1 hardcodes 73 UK returns in `[returns]` | JST or Jordà: papers 4, 8, 19, 22 | RATES windows; VAL `basis = "jst"` |
| 3 | Gain-ladder and stock-ladder rate schedules, `ladder_to_tau`, `fit_k`, `rate_vec`, `rate_spec_from_scenario`, `with_rate_scenario` | `wdt_core` 129 | logistic `tau` only | "ladder": **0 papers**. Logistic τ(W) is the papers' rate | baseline of VAL and RATES (`gain_ladder`) |
| 4 | Rule sets (`units/allow/off`, `units_and_value/reset/on`), `parse_rule`, `resolve_rule` | `wdt_core` 22; TOML `[rules]` 4, `[rates.defaults]` | none | rule-set names not found in `source/`; the generic word "reset" matches 8 papers (not checked) | heir rule `delta` vs `fresh_entrant`; "fresh entrant": **0 papers** |
| 5 | Parameter parsing for `[rates]` with cross-reference checks: `_parse_rates`, `_parse_phase2`, `_rates_cfg`, `_parse_rules`, `load_rates_params`, `rate_params`, `_rate_key` | `wdt_core` 288 | `load_params` only | not a paper concept | all of RATES |
| 6 | Tax-replacement legs: `calibrated_legs`, `solve_threshold`, `band_net_position`, `threshold_*`, `person_saving`, `leg_*`, `_leg_tables` | `wdt_core` 260; TOML `[rates.replacement]` 60 | none | CGT replacement: papers 1, 14, 22 mention replacing existing taxes | RATES tables (replacement), no v1 output |
| 7 | Double-entry family ledger, generations (`G = 30`), horizon `T = 100`, strategy library, verdict tests BRG, HSC, SPT, SST | `valgen_core` 3,353 (v1 `val_core` 1,161, +2,192) | v1 `val_core` Route C tables C.1 to C.12 | verdict names BRG, HSC, SPT, SST: **0 papers**; "honest error": paper 5; "strategy" matches 17 papers as a generic word (not checked) | VAL figures `val_fig_<ID>_*`, tables, `valgen_data.json` |
| 8 | Fund with SRR/LRR rules, trailing-mean targets, CORP levy in three modes (`nominal`, `real`, `none`), cohort model, representativeness | `rates_core` 2,127 (v1 `rates_core1` 1,709, +418) | v1 SSM fund and TCM cohorts | trailing: papers 7b, 18 only | RATES tables T1 to T31, figures F1 to F31 |
| 9 | Block bootstrap, window censoring, process-pool runner | `rates_core` `block_bootstrap` 41, `wdt_par` 196 | v1 73-start-year sweep | bootstrap: papers 1, 7, 8, 9, 10, 12, 15, 17, 18, 20, 22; "censor": **0 papers** | RATES window statistics |
| 10 | Welfare (EVAL) modules E1 to E7, `DynamicCGTPath` | `eval_core` 2,718 (v1 `wfr_core` 1,635, +1,083) | v1 WFR | welfare: papers 1, 2, 3b, 4, 5, 6, 7, 8, 12, 13, 14, 15, 19, 20, 21, 22 | none: module fails at import (section 5) |
| 11 | Output scripts for the above | 5,150 lines in 8 files (section 3.1) | v1 4,172 lines in 5 files (`5_3`, `5_4`, `5_5`, `8_2`, `8_3`) | 19 embedded names, 0 match | PNG and Markdown, not read by any paper today |
| 12 | WID data tooling and D0/D1 data audit | 1,237 lines in 6 scripts; `wid_out/` 81 MB, `audit_d0/` 70 MB | none | not paper code | audit only; not model |

Reading the table: rows 1, 2, 8 and 9 serve claims the papers make (routes, historical windows, fund fill, resampling). Rows 3, 4 and 7 are the v2 design, not found in any paper's text. Row 10 serves welfare, which 16 papers mention, but it does not run. Whether the papers should adopt the gain ladder and the strategy verdicts is a stage E and author decision.

## 3. The three largest sources of complexity

Ranked by lines of the thing that causes the complexity, with line counts [code, `wc -l` and `ast`]. "Feature size" counts code that exists only for that feature.

### 3.1 The output layer: 5,150 lines, 55 figures, 56 tables

| File | Lines | Builders |
|:---|---:|---:|
| `5_6_VALGEN_tables.py` | 988 | 25 tables |
| `5_7_VALGEN_charts.py` | 1,196 | 25 figures |
| `5_8_VAL_gap_tables.py` | 274 | 5 tables |
| `5_9_VAL_numbers.py` | 90 | numbers register |
| `5_10_VAL_examples.py` | 110 | 2 worked examples |
| `8_2_RATES_tables.py` | 1,317 | 31 tables |
| `8_3_RATES_charts.py` | 1,088 | 31 builders (30 names; F29 absent) |
| `rates_view.py` | 87 | helpers |
| **Total** | **5,150** | |

v1 had 4,172 lines for the same job (`5_3` 858, `5_4` 1,042, `5_5` 478, `8_2` 935, `8_3` 859) plus 2,796 for SWEEPS output scripts and 2,200 for WFR output scripts that v2 dropped (v1 whole output layer 9,168). So v2's output layer is +978 over v1's like-for-like and 4,018 lines smaller than v1's whole output layer, but it is the largest single block and none of its output is currently embedded: 0 of the 19 names in `source/` match [stage C, fact 2].

### 3.2 `valgen_core.py`: 3,353 lines, 91 definitions

| Part | Lines | Detail |
|:---|---:|:---|
| `main` | 431 | one function, lines 2919 to 3349 |
| seven validators | 764 | `_validate` 25, `_p2_validate` 98, `_p2b_validate` 124, `_p3_validate` 112, `_p4_validate` 103, `_p5_validate` 159, `_p6_validate` 143 |
| strategy search and growth/direction/dominance analyses | 318 | `_strategies` 80, `_p5_search`, `_p5_growth_surface`, `_p5_dmg`, `_p5_hec`, `_p5_direction`, `_p5_headline`, `_lam_D` [`ast`] |
| ledger and family runs | 311 | `run_life`, `run_family`, `run_family3`, `run_batch` 236; `_LedgerHook` 75 [`ast`] |
| rest | 1,529 | imports, config, 70 smaller helpers (remainder of 3,353) |

It is 2.9 times v1 `val_core` (1,161). Each build step P1 to P6 carries its own validator that re-runs the step at its off-switches and compares to the previous step [doc: `VAL/md/VALGEN_build_log.md`, 331 lines across four notes]. The validators are 23% of the file and `main` calls all seven unconditionally (lines 2944 to 3122); the only switch is `--dry-run`, which skips every simulation and validator [code, `main` 2919 to 2931]. This is the layering the build log calls "reduces to the previous step", which gives v2 its self-checks and makes `valgen_core` unreadable in one pass.

### 3.3 `eval_core.py`: 2,718 lines, importing nothing that exists

`DynamicCGTPath` (242 lines), `run_module_e1` (208), E2 to E5, `run_tau_sweep`, `main` 67. It imports `wfr_core` (a v1 module not in `model_v2`; import fails at line 62 [run]) and reads `p['brackets']`, `p['tiers']`, `p['tcm']` (six sites, lines 1445 to 2666), which `load_params` no longer returns. No v2 file imports it (grep: 0 hits outside `EVAL/`). It is 15% of v2's Python. It is a v1 module carried forward and not ported.

### 3.4 Next four, for reference

| Source | Lines | Note |
|:---|---:|:---|
| `[rates]` TOML | 1,066 (58% of the file) | `[rates.scenarios]` 677 for 101 scenarios; `[rates.run]` 88; `[rates.defaults]` 84; `[rates.replacement]` 60 |
| `rates_core.py` | 2,127 | `run_window` 166, `run_lines` 145; only +418 over v1 |
| `wdt_core.py` | 2,043 | 40 new definitions, 831 lines; parsing 288 and tax replacement 260 are the largest groups |
| `wdt_kernel.py` | 564 | used by both cores; smallest and best-bounded |

If the question is "what makes v2 hard to rebuild", the answer by this table is, in order, the output layer, `valgen_core`, `eval_core`, then the `[rates]` input block.
## 4. Tests

### 4.1 What exists

| File | Lines | What it checks | Result |
|:---|---:|:---|:---|
| `test/test_hlc_drift.py` | 23 | `[val_gen.hlc]` in the TOML matches `rates_data.json` (average and top stock rate to 5e-6; scenario name) | runs, exit 0, one WARN (placeholder) [run] |
| `test/print_hlc_calibration.py` | 60 | tool, not a test; `--write` edits the TOML | not run (it needs `rates_data.json`, not in the repo, and `--write` edits a model file) |
| `test/wdt_patchlib.py` 371, `test/patchlib.py` 108, `test/diff_json.py` 30 | 509 | patch and comparison helpers, no assertions | not tests |

### 4.2 What is not tested

- `wdt_core`, `wdt_kernel`, `wdt_jst`, `wdt_par`, `wdt_fmt`, `wdt_md`, `wdt_style` have no test. v1 had 320 passing assertions for `wdt_fmt`, `wdt_md`, `wdt_style`, `wdt_analytics` (stage A, fact 6); none were carried to v2.
- The four files `WDT_Code_Reference.md` names (`kernel_test.py`, `bridge_test.py`, `rates_test.py`, `test_valgen_pairs.py`) do not exist in the repo [`git ls-files`, stage C section 7]. So v2's central guarantee in the reference, that `valgen_core` and `rates_core` agree on the same line, has no executable check.
- Self-checks inside the cores: `valgen_core` seven validators (764 lines) and `rates_core.validate` 24 lines, `_verification` 22. They run inside `main` and were not run here (a full run is out of scope).
- Cross-version: no test compares v2 `run_pair` with v1. At identical inputs they differ (stage C, fact 3); that is an unexplained difference unless the basis change is documented, and `BASIS_CHANGE.md` is untracked.

### 4.3 Not run, and why

`valgen_core.main`, `rates_core.main`, `eval_core`, table and chart scripts: full model runs, out of scope. `print_hlc_calibration.py`: needs `rates_data.json`. The v1 tests were not re-run (stage A did).

## 5. Dead and orphaned code, measured

| Item | Lines | Evidence |
|:---|---:|:---|
| `EVAL/eval_core.py` | 2,718 | import fails (`wfr_core`); 0 importers [run, grep] |
| `[val_gen.hlc]` pair | the `_hlc_pair` function 15 plus TOML block 6 | TOML `placeholder = true`, so valgen skips the HLC pair [run: the drift test message; code: `_hlc_pair` 2887 to 2901] |
| `[rates] valgen_dir` | 1 key, parsed at `wdt_core` line 1817 | `rates_core` never reads it [grep, stage C] |
| 27 unreferenced scenarios | about 135 TOML lines | section 1, fact 5 |
| `wdt_jst` module docstring | 1 sentence | still says "not yet wired" |
| `test/patchlib.py` vs `test/wdt_patchlib.py` | 108 and 371 | two patch helpers; not checked which is current |

## 6. Open points and limits

1. The "roughly 135 lines" for unreferenced scenarios (section 1, fact 5) is an estimate from the median of 5 keys per scenario, not summed per scenario.
2. `_hlc_pair` is 15 lines (2887 to 2901); I did not check whether other HLC code in `valgen_core` exists beyond its loader just above it (lines 2872 to 2885).
3. "Paper names it" is a text match in `source/`, not a reading of what the paper claims. Generic words (strategy, reset) over-match.
4. `valgen_core.main` calls a "bridge to legacy `run_pair` / `run_sim_hist`" first (line 2938). v2 therefore still carries a comparison path to v1-style functions inside its core; its size was not measured.
5. Two patch helpers (`test/patchlib.py`, `test/wdt_patchlib.py`) both exist; which is current was not checked.
