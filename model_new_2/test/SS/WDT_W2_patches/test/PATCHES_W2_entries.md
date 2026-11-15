<!-- Paste into Model/test/PATCHES.md; renumber W2-0x to the next free numbers if the log uses a single sequence. -->

## W2-01  rates_core fixes  (patch_W2_01_rates_fixes.py, test_W2_01_rates_fixes.py)
rates_core: `rel_cov_never_share` and `income_short_share_band{i}` written; `figure_scenarios()` adds `[rates.figures].route_b` and
the `gl_arch_*` scenarios; `_route_plan`/`_verification` cached per scenario (`_plan_ver`); docstring covers kernel / Route B / loop.
bridge_test.py: `rates_line()` builds a per-line `plan`; guard expects `(plan, ver)`.
**Numbers:** no existing number moves. New JSON keys; `--quick` runs more scenarios.

## W2-02  HLC burdens from a TOML calibration  (patch_W2_02_hlc_calibration.py, test_W2_02_hlc_calibration.py)
New `[val_gen.hlc]` (PLACEHOLDER until `print_hlc_calibration.py --write`); wdt_core parses it; valgen `_rates_burdens` reads it and
no longer touches rates_data.json. Definition now D1d (net payers / top 0.1%), was richest band. `test_hlc_drift.py` warns on drift.
**Numbers:** HLC pair is absent until calibrated, then differs from before (definition change). Nothing else moves.

## W2-03  p['g'] -> p['g_real']  (patch_W2_03_g_real_rename.py, test_W2_03_g_real_rename.py)
Parameter-dict reads/writes in wdt_core, valgen_core (28) and 3 tests. JSON output keys 'g' unchanged (downstream tables unaffected).
**Numbers:** neutral. Prove: `python test/diff_json.py before.json valgen_data.json`.

## W2-04  D11 code  (patch_W2_04_d11_code.py, test_W2_04_d11_code.py)
SSM deleted; load_params stops reading [swf] [budget] [returns] [tcm] [[tiers]] [[brackets]]; N_fill, p['N'], p['tcm'], p['returns'],
p['returns_meta'], p['rate'] gone; g_real only from with_val_basis (jst|manual); `[val_gen]` basis and rate_scenario required;
`[sweep]` g_offsets -> g_vals at with_val_basis; valgen `_ir`, `_RETIRED_KEYS`; rates_test.py stale checks removed.
Kept until D9 passes: simulate, run_pair, run_sim_hist, settle_tw_flows and relatives, run_sim, g_eff, synthetic_returns.
**Numbers:** g_vals grids move (recentred on g_real). Everything else in valgen unchanged; RATES unchanged. load_params ~instant.

## W2-05  TOML cleanup  (patch_W2_05_toml_cleanup.py, test_W2_05_toml_cleanup.py)
Retired blocks and `[sweep]` canon / rates_* / wfr_* deleted; g_vals -> g_offsets; `[synthetic_scenario] mu` 0.07 -> 0.02; stale comments.
**Numbers:** as W2-04 (apply the two together); synthetic mu only read by synthetic_returns.

### Docs to sync after the run (not patched: files not seen)
WDT_Code_Reference.md: Route B, loop windows (T=100), wdt_jst, kernel, archetypes, [val_gen.hlc], D11 removals, g_real.
WDT_Refactor_Plan.md: status line (S1-S5, S7, D11 done; D9 pending) and drift register.

## W2-06  Presentation follows W2-02  (patch_W2_06_presentation.py, test_W2_06_presentation.py)
5_6 `build_HLP` caption and "not built" note, 5_7 HLP footnote (burdens now come from `[val_gen.hlc]`); 8_2 docstring contract rewritten to what rates_core writes.
**Numbers:** neutral. 8_3 not touched (not provided; duplicates 8_2 helpers).

## W2-07  Docs sync  (patch_W2_07_docs.py, test_W2_07_docs.py)
WDT_Code_Reference.md (kernel, wdt_jst, D11 removals, hlc, g_real, loop, route plan) and the WDT_Refactor_Plan.md status line. Pass `--root` if the .md files are outside Model/.
**Numbers:** neutral.

## W2-08  Shared RATES view helpers  (patch_W2_08_rates_view.py, test_W2_08_rates_view.py, rates_view_new.py)
New Model/rates_view.py (med, hl, pq, years, need, route_b_names, default_of_mode, rb_label); the eight duplicated helpers removed from 8_2 and 8_3 and imported with the old underscore names. Tables keep their longer Route B labels (`long=True`).
**Numbers:** neutral. Re-run 8_2 and 8_3 and diff the .md output; 8_3's route_b_names now also prints the missing-scenario note.
