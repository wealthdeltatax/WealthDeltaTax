# Model v2: inventory and mechanism (brief 001c, stage C)

Audit of `model_v2/`. Read-only: no model file was edited and no core, table or chart script was run. Date: 2026-11-16, repo at `0b4ead9` (main). Stage D (complication and tests) is not started: where this note meets a size or a test fact it records it and leaves the verdict to stage D. Errors in v2 are not audited here.

Evidence marks: **[code]** read in the named file and function; **[run]** short Python snippet from the shell with `PYTHONDONTWRITEBYTECODE=1`; **[doc]** stated in `model_v2/WDT_Code_Reference.md` or a module docstring and not re-derived. `jst_r6.json` was not opened (guide rule).

## 1. Headline facts

1. v2 is 29 Python files, 19,558 lines (`wc -l`): 7 base modules 4,381; 3 cores 8,198; 7 table/chart scripts plus `rates_view.py` 5,150; 6 data-audit scripts 1,237; 5 test/patch helpers 592. Plus `WDT_Params.toml` 1,839 lines (v1: 554), 154 MB on disk, 187 tracked files (of which `wid_out/` 81 MB and `audit_d0/` 70 MB are data, not model).
2. **The papers' figure names do not match v2.** The sources embed 19 distinct `val_fig_*` / `rates_fig_*` names (10 VAL, 9 RATES). v2 RATES produces 30 names of the form `rates_fig_<n>_<slug>`; exact matches: 0 [run, regex over `source/*.md` and `8_3_RATES_charts.py`]. v2 VAL names are `val_fig_<ID>_<slug>` (`5_7_VALGEN_charts.py`); no embedded VAL name has that form. Embeds are the v1 numbering, and the papers are being rewritten.
3. **v2 changes the basis convention of the single-life mechanics.** `wdt_core.simulate` (line 441) carries the post-surrender basis `f*alpha*V` into the next year; v1 `simulate` carried `W_new`. Constant `BASIS_CONVENTION = 'post'` (line 121); the cited `BASIS_CHANGE.md` is not tracked. At identical inputs (v1 rate parameters tau_0 0.15, tau_m 0.70, k 0.001, W_min 2.0; V0 20; g 10.45%; N 30) [run]:

| alpha | metric | v1 | v2 |
|---:|:---|---:|---:|
| 1.5 | net_pct | +0.009345 | +0.013219 |
| 1.5 | tw_gap | +0.058455 | +0.065870 |
| 1.5 | pv_pct | -0.014155 | -0.025397 |
| 0.5 | net_pct | -0.000529 | -0.001878 |
| 0.5 | tw_gap | -0.061059 | -0.069481 |
| 0.5 | pv_pct | +0.014729 | +0.026627 |

   `pv_pct` also depends on rho (v1 0.05, v2 base 0.035), so only `net_pct` and `tw_gap` isolate the basis change. `run_pair`, `simulate_sell`, `settle_tw` and `npv_tax` are text-identical to v1; `simulate`, `settle_tw_flows`, `run_sim`, `tau` and `decompose_tw_advantage` differ (diff of function source with `ast`). Whether the v1 convention was a v1 error is stage B's register, not decided here.
4. **v2 baseline is not the papers' rate function.** The baseline is the gain ladder (`[rates.defaults] schedule = "gain_ladder"`): statutory rate on the annual delta from `rate_spec_from_scenario`/`ladder_to_tau` is 0 below W_min 0.1125 (£m), 0.0713 at 0.2, 0.1250 at 0.5, 0.1875 at 1.0, 0.3750 at 2.5, 0.4688 at 5, 0.5437 at 25, 0.5625 from 100 [run]. The papers' logistic (15% at £2m rising to 70%) survives only as comparison scenarios (`logistic_ref`).
5. **Retired v1 inputs are gone.** `load_params` returns no `returns`, `tcm`, `brackets`, `tiers`, `N` or `N_fill` and takes 0.013 s [run] (v1: 0.05 s). `[rates.scenarios]` holds 101 scenarios [run].
6. 23 of the 24 files imported load without error [run, import only; the 5 `test/` helpers were not imported]. `EVAL/eval_core.py` fails: `ModuleNotFoundError: No module named 'wfr_core'` (line 62; `wfr_core` is a v1 module not in v2). Static check: it also reads retired TOML sections `p['brackets']`, `p['tiers']`, `p['tcm']` (lines 1445, 1579, 1724, 2287, 2341, 2666). EVAL is orphaned from v2.
7. No unresolved names: every `wdt_core.x`, `wdt_fmt.x`, `wdt_md.x`, `wdt_style.x`, `wdt_kernel.x`, `wdt_jst.x`, `rates_view.x`, `wdt_par.x` reference and `from ... import` in all v2 files resolves to a definition (AST check, 0 unresolved).
8. Import-time side effects: `wid_checks.py` and `wid_summarise.py` have no `main()` guard; importing them rewrites CSV/JSON under `wid_out/summary*` (see the stage C report, deviations).

## 2. Inventory

Order of dependence: parameters, base, cores, JSON, presentation. "Imports" lists project modules only (AST; `wdt_core` imports `wdt_jst` lazily inside `jst_basis`, line 316).

### 2.1 Modules

| Module | Lines | Role | Imports (project) | Reads | Writes |
|:---|---:|:---|:---|:---|:---|
| `wdt_core.py` | 2,043 | Base: `load_params`, `_parse_rates`, rate schedules (`tau`, `rate_vec`, `ladder_to_tau`, `fit_k`), rule sets (`parse_rule`), real basis (`with_val_basis`, `jst_basis`), single-life Route C (`simulate`, `simulate_sell`, `settle_tw`, `run_pair`, `decompose_tw_advantage`), tax-replacement solver (`calibrated_legs`, `solve_threshold`, `band_net_position`), JSON helpers (`save_json`, `load_json`) | `wdt_jst` (lazy) | `WDT_Params.toml` | none |
| `wdt_kernel.py` | 564 | Base: route-settlement kernel for routes A, B, C, D and verified tranche; `Book`, `assess`, `step_year`, `step_death`, `run_lines` | none (numpy) | n/a | n/a |
| `wdt_jst.py` | 243 | Base: JST loader, `loop_windows` (wrap, `repeat`, `contiguous`), `real_basis_inputs`, `real_return_series` | none | `jst_r6.json` via `load_jst` | n/a |
| `wdt_par.py` | 196 | Base: ordered process-pool map `WorkerPool`, `resolve_workers` | none (stdlib) | n/a | n/a |
| `wdt_fmt.py` | 470 | Formatting, `out_dir` (`model_v2/OUTPUTS/<code>`) | none | n/a | n/a |
| `wdt_md.py` | 532 | Markdown assembly (`md_table`, `pct_table`, `key_value_table`, `MdDoc`) | none | n/a | n/a |
| `wdt_style.py` | 333 | Figure style, `save_fig` | none | n/a | n/a |
| `valgen_core.py` | 3,353 | VAL core: double-entry family ledger, strategy search, verdict tests (section 5.3) | `wdt_core`, `wdt_fmt`, `wdt_jst`, `wdt_kernel` | TOML, JST | `OUTPUTS/VAL/valgen_data.json` (`main`, line 2919) |
| `rates_core.py` | 2,127 | RATES core: JST window replay onto UK distribution, fund, CORP levy, representativeness (section 5.4) | `wdt_core`, `wdt_fmt`, `wdt_jst`, `wdt_kernel`, `wdt_par` | TOML, JST | `OUTPUTS/RATES/rates_data.json` (`main`, line 2082) |
| `eval_core.py` | 2,718 | EVAL: N=30 WDT vs CGT welfare, modules E1 to E7; own `DynamicCGTPath` | `wdt_core`, `wfr_core` (missing) | TOML | `OUTPUTS/EVAL/eval_results.json` |
| `5_6_VALGEN_tables.py` | 988 | VAL tables | `wdt_core`, `wdt_fmt`, `wdt_md` | `valgen_data.json` | `val_table_<id>_<slug>.md`, `val_tables_all.md`, `val_names.md` |
| `5_7_VALGEN_charts.py` | 1,196 | VAL figures (25 builders) | `wdt_core`, `wdt_fmt`, `wdt_style` | `valgen_data.json` | `val_fig_<ID>_<slug>.png` |
| `5_8_VAL_gap_tables.py` | 274 | VAL gap tables (5 builders, F7.1b/c, F7.2b/c) | `wdt_core`, `wdt_fmt`, `wdt_md` | `valgen_data.json` | `val_table_gap_*.md` |
| `5_9_VAL_numbers.py` | 90 | VAL numbers register | `wdt_core`, `wdt_fmt`, `wdt_md` | `valgen_data.json` | `val_numbers.json`, `tables/val_numbers.md` |
| `5_10_VAL_examples.py` | 110 | VAL worked examples L and M | `wdt_core`, `wdt_fmt`, `wdt_md` | `valgen_data.json` | `val_example_<id>.md` |
| `8_2_RATES_tables.py` | 1,317 | RATES tables T1 to T31 | `rates_view`, `wdt_core`, `wdt_fmt`, `wdt_md` | `rates_data.json` | `rates_table_<n>_<slug>.md`, `rates_tables_all.md` |
| `8_3_RATES_charts.py` | 1,088 | RATES figures F1 to F31 (30 names; F29 absent) | `rates_view`, `wdt_core`, `wdt_fmt`, `wdt_style` | `rates_data.json` | `rates_fig_<n>_<slug>.png` |
| `rates_view.py` | 87 | Read-only helpers over `rates_data.json` | `wdt_fmt` | JSON | none |
| `d0_jst_audit.py` | 336 | Standalone JST coverage audit (pandas) | none | `jst_r6.json` | `audit_d0/` CSVs |
| `wid_download.py` | 372 | WID API downloader (`discover`, `fetch`) | none | network | `wid_out/` |
| `wid_summarise.py` | 107 | WID summary files | none | `wid_long.csv` (not tracked) | `wid_out/summary/` |
| `wid_checks.py` | 88 | WID identity and seam checks | none | `wid_long.csv` | `wid_out/summary2/` |
| `audit_d0/d1_identity.py` | 171 | D1 identity runs | `wdt_jst` | `jst_r6.json`, WID | `d1_identity_runs*.csv` |
| `audit_d0/wdt_audit_to_json.py` | 163 | Audit register to JSON | none | `audit_d0/` | `wdt_audit.json` |
| `test/test_hlc_drift.py` | 23 | HLC calibration drift test | `print_hlc_calibration` | TOML | none |
| `test/print_hlc_calibration.py` | 60 | HLC calibration printer (`--write` edits the TOML) | none | `rates_data.json` | TOML (with `--write`) |
| `test/wdt_patchlib.py` | 371 | Patch/sandbox library | none | n/a | n/a |
| `test/patchlib.py` | 108 | Older patch helper | none | n/a | n/a |
| `test/diff_json.py` | 30 | JSON comparison | none | two JSON | stdout |

Other files: `WDT_Params.toml` (inputs), `jst_r6.json` (1.7 MB), `WDT_Code_Reference.md` (278 lines), `WID_Data_Guide.md` (66), `README.md` (2 lines, "Model Test"), `VAL/md/` (four build notes, 331 lines), `audit_d0/` (data-audit CSVs, registers, `Research/` source files), `wid_out/` (81 MB, 68 raw JSON). There is no run script (no `.bat`); the running order exists only as prose in `WDT_Code_Reference.md` section 6. No `OUTPUTS/` is tracked, so no generated output can be compared to the papers.

### 2.2 Dependency order

```
WDT_Params.toml ─► wdt_core ─┬─► valgen_core ─► valgen_data.json ─► 5_6, 5_7, 5_8, 5_9, 5_10
 jst_r6.json ─► wdt_jst ─────┤   (+ wdt_kernel, wdt_jst)
                  wdt_kernel ┼─► rates_core ──► rates_data.json ──► 8_2, 8_3 (+ rates_view)
                  wdt_par ───┘   (+ wdt_kernel, wdt_jst, wdt_par)
eval_core ─► wdt_core + wfr_core (missing)       leaves: wdt_fmt, wdt_md, wdt_style
```

[code, AST] Cores do not import each other; no presentation script imports a core; `wdt_fmt`, `wdt_md`, `wdt_style`, `wdt_kernel`, `wdt_par` import no project module. This matches the layering in `docs/agents/reference/code/conventions.md` sections 1 and 2 (the v1 breaches are gone in v2). The one cross-layer path is data: `valgen_core` reads no RATES output; the HLC calibration travels RATES output → `test/print_hlc_calibration.py --write` → TOML → `valgen_core` [doc]. `[rates] valgen_dir` is parsed (`wdt_core._parse_rates`, line 1817) but `rates_core` never reads it (grep).

## 3. Inputs

`WDT_Params.toml` v7, dated 2026-09-08 [run]. 1,839 lines: `[rates]` 1,066 (58%), `[names]` 296, `[val_gen]` 163, `[rho]` 73, `[sweep]` 60, `[archetypes]` 43, `[val]` 37, `[output]` 23, `[synthetic_scenario]` 21, `[income]` 14, `[route_b]` 7, `[verification]` 6, `[meta]` 6, `[rules]` 4. Retired sections absent: `rate`, `swf`, `budget`, `returns`, `tcm`, `tiers`, `brackets`.
Canonical values [run]: `[val] V0_m` 20.0, `N_demo` 30; `[rho] base` 0.035; `[val_gen]` `T` 100, `G` 30, `rate_scenario` "gain_ladder", `basis` "jst", `consumption` 0.035; `[rates]` `uk_iso` GBR, `calibration_year` 2017, `exp_ref_year` 2019; `[rates.defaults]` `T` 100, `ms` 3.0, `ml` 3.0, `horizon` 10, `c` 0.035, `heir_rule` "delta", `rule_set` "candidate" (`units_and_value/reset/on`; `base` is `units/allow/off`).
`jst_r6.json` is read through `wdt_jst.load_jst` by both cores, `d0_jst_audit.py` and `d1_identity.py`.

## 4. Outputs and the papers

v2 has no tracked outputs, so the map is by code. VAL: 25 table builders, 25 chart builders, 5 gap-table builders, plus numbers and two worked examples. RATES: 31 tables (T1 to T31) and 30 figures (F1 to F31, `f29` not defined). Output names do not match any embed in the papers (headline fact 2). Papers 5 (Valuing Wealth) and 8 (Rates and Revenue) are the only sources that embed model figures of the VAL/RATES kind; which of the 55 v2 charts and 56 tables the rewritten papers need is a stage E question.

## 5. Mechanism

Stated against `website/site/pages/Project-Map.md` sections VAL and RATES.

### 5.1 Base: `wdt_core`, `wdt_kernel`, `wdt_jst`

- **Rate functions** `tau`, `rate_vec` [code, 147 to 177, 1124 to 1149]: three schedules, `logistic` (the papers' τ(W)), `logistic_ln`, `ladder` (anchors linear in ln W). `ladder_to_tau` [1152] converts a target effective rate to the statutory rate on the delta: at the top anchor 0.45 becomes 0.5625 (= 0.45 / ((r_ref − c_ref)/r_ref) with r_ref 0.05, c_ref 0.01) [run].
- **Single-life Route C** (`simulate` 441, `simulate_sell` 494, `settle_tw` 412): same structure as v1 with the basis change in fact 3. Declared wealth `W = f*alpha*V`; tax in kind `q = L/W_new`; refund capped by cumulative tax. Matches VAL §4 Route C and §7.
- **Kernel** `wdt_kernel` [code]: `Book` holds line-vectorised state; `assess` (276) makes one assessment on total declared W; `_route_tax` (222) splits tax or refund across routes; `step_year` (450) and `step_death` (479) advance a year and handle death and the heir. This implements the four-route architecture of VAL §4 (A/B professional, C in kind, D deferred) as one code path used by both cores [doc: the bridge test that checks valgen/rates agreement is not in the repo, see section 7].
- **JST windows** `loop_windows` [58 to 88]: windows of length T over a country's usable years, wrapping at the seam; flagged `repeat` and `contiguous`. The module docstring still says "not yet wired" while `wdt_core.jst_basis` (316) and both cores use it: stale docstring.
- **Tax replacement** (`calibrated_legs` 1241, `solve_threshold` 1266, `band_net_position` 1393): relief retires CGT, IHT and corporation tax in order; a common income-tax/NI threshold is solved by bisection; taxpayer-count curves are placeholders [doc]. This has no counterpart in the Project-Map RATES section.

### 5.2 Parameter loading

`load_params` (1891 to 2043) parses the whole TOML; `_parse_rates` (1645 to 1828, 184 lines) validates `[rates]` and its scenario, figure and cohort cross-references and raises on unknown keys [code]. `with_rate_scenario`, `rate_spec_from_scenario` and `with_val_basis` (251, 216, 329) put VAL on the RATES rate design and the real JST basis.

### 5.3 VAL: `valgen_core` (paper 5)

A family line on a double-entry ledger over horizon T = 100 with a death every G = 30 years [doc, TOML]. Build steps, each reducing to the previous at its off-switches [doc]: P1 `run_life` (331), P2/P2b `run_family` (440, Route C only, heir rule `delta` or `fresh_entrant`), P3 `run_family3` (824) and `run_batch` (899) through `_LedgerHook` (718) around `wdt_kernel`, P4 verification hazard (`_lam_D` 1811), P5 strategy search `_strategies` (1679), `_p5_search` (1837), with verdict tests BRG, HSC, SPT, SST. Extra analyses: lambda grid `_p3_lambda_grid` (2833), V0 sweep `_v0_sweep` (2848), JST replay `_p7_replay` (2784), HLC pair `_hlc_pair` (2887), growth surface `_p5_growth_surface` (2030), dominance grid `_p5_dmg` (2058), honest-error HEC `_p5_hec` (2126), under/over-statement `_p5_direction` (2185). `main` (2919 to 3349) is 431 lines; validators are `_p2b_validate` (124 lines), `_p5_validate` (159), `_p6_validate` (143).
Against the papers: Route C in-kind with a unit-capped refund and Route D deferred settlement match VAL §4; the strategy search over declaration ratios is the v2 counterpart of the tolerant-zone claim (VAL §7.1) but tests it with a strategy library and a no-tax ceiling instead of the α = 0.8 to 1.5 grid. The Route D corrective auction of VAL §11 is represented as an expected-value share (`vD = 1 − (1 − lambda)^t`) declared at the true price [doc], not as a bidding process. The papers' "behavioural centre α ≈ 1.1" has no direct v2 output identified [not checked in `valgen_data.json`; not run].

### 5.4 RATES: `rates_core` (paper 8)

Replays each JST country-history window onto today's UK-calibrated wealth distribution and rate schedule [doc, docstring]. Layers [code]: panel and flags (`panel` 200, `flag_years` 225); distribution and scenario (`calibration` 1233, `build_scenario` 560, `cohort_spec` 528); engine (`run_lines` 825 to 969, 145 lines, `run_cohorts` 985, `_route_plan` 653, `_verification` 733); fund (`run_fund` 1109 to 1193); window driver (`run_window` 1508 to 1673, 166 lines); scenario driver (`run_scenario` 1986) with `block_bootstrap` (1886) and `validate` (2056); `main` (2082). The fund runs the SRR/LRR rules with trailing-mean targets `ms*A_t` and `(ms+ml)*A_t`, fills inside each window, reports censored windows rather than dropping them, and runs every window three times for the CORP levy cases `nominal`, `real`, `none` [doc]. `--workers` uses `wdt_par.WorkerPool`.
Against the papers (Project-Map RATES): the papers' four properties (SRR fills at year 3 in all 73 UK start years, 100% success, LRR breakeven 7 to 29 years, 2000 reference scenario year 19, logistic τ 15% to 70%, N = 30) are v1 outputs. v2 has no 73-start-year UK sweep and no N_fill; it reports `fill_year` per JST window over 14 countries, T = 100, stride from `start_stride`, on the gain-ladder baseline. None of those four numbers can be read from v2 without a run; not run here.

### 5.5 EVAL: `eval_core`

N = 30 WDT vs CGT certainty-equivalent welfare over 43 rolling windows [doc, docstring], modules E1 to E7 (`run_module_e1` 1706 to 1913, 208 lines, to `run_tau_sweep` 2589), with `DynamicCGTPath` (542 to 783, 242 lines). It is the v1 EVAL/WFR line of work, still on the retired `p['brackets']`, `p['tiers']`, `p['tcm']` and the missing `wfr_core` (fact 6). Not part of the `WDT_Code_Reference.md` layering.

## 6. Presentation layer

Seven scripts read one JSON each and write Markdown or PNG. Convention check [code, AST]: none imports a core. Output paths come from `wdt_fmt.out_dir` (`model_v2/OUTPUTS/<CODE>/`); `5_9_VAL_numbers.py` also writes a JSON (`val_numbers.json`).

## 7. Tests (inventory only; stage D runs and judges)

Tracked in `model_v2/test/`: `test_hlc_drift.py` (23 lines), the three helpers `print_hlc_calibration.py`, `wdt_patchlib.py`, `patchlib.py`, and `diff_json.py`. `WDT_Code_Reference.md` section 6 and section 3 name `kernel_test.py`, `bridge_test.py`, `rates_test.py` and `test_valgen_pairs.py`; none exists anywhere in the tracked repo (`git ls-files`), so the kernel unit tests and the valgen/rates bridge guard it describes are absent. The cores have internal validators (`valgen_core._p5_validate` etc., `rates_core.validate`) that run inside `main`. Not run.

## 8. Not run, and why

- `valgen_core.main`, `rates_core.main`, `eval_core`, any table or chart script: out of scope for the audit.
- `jst_r6.json` was not opened; the window counts, fill years and figures of v2 are therefore not measured here.
- Errors in v2 and the complication analysis: stage D (and stage B for v1 items).

## 9. Pointers for stage D (facts only)

- Size to attribute: `valgen_core` 3,353, `rates_core` 2,127, `wdt_core` 2,043, `eval_core` 2,718, `[rates]` TOML 1,066 lines, and the 101 scenarios; v2's non-test, non-data-tooling Python (17,729 lines) is smaller than v1's (18,136), the growth is in the TOML (1,839 vs 554) and the data-audit tooling (1,237 lines).
- Whether the basis change (fact 3) is documented in the repo: `BASIS_CHANGE.md` is cited but untracked.
- Whether `eval_core` is dead in v2 (fact 6).
- Missing test files named by the reference doc (section 7).
