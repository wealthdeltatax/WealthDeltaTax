# S2 report: RATES engine on wdt_kernel (Work Order, Wave 1)

**Status: delivered as a patch, verified in a reconstructed sandbox, NOT run on the real pipeline.** `wdt_core.py`, `wdt_fmt.py`, `valgen_core.py` and the JST JSON are not in the Project, so I rebuilt stand-ins (a synthetic JST, a stand-in `wdt_core`) and ran the legacy `rates_core.py` and the patched one side by side. The first thing to do is run the real parity check (below).

## Files
- `apply_rates_s2.py`: idempotent, CRLF-safe, anchor-asserting patcher for `RATES/rates_core.py` and `WDT_Params.toml` (keeps `*.pre_s2` backups, refuses a half-patched state, compiles before writing).
- `rates_engine_test.py`: 20 engine checks (no JST needed) + `--parity <rates_core.py.pre_s2>` for legacy parity on the real JST.

Run: `python apply_rates_s2.py --model-dir <Model>` then `cd RATES; python rates_engine_test.py; python rates_engine_test.py --parity rates_core.py.pre_s2`.

## What changed (scope: rates_core.py + TOML keys S2 owns)
- `run_lines` now drives `wdt_kernel` (`Book`, `step_year`, `step_death`); the inline mechanics are gone. Honest lines (alpha = 1) as before.
- A/B/C/D shares by launch-wealth band from the archetype mixture (`route_mix = "wealth"`), a fixed blend, or one archetype everywhere (the archetype sweep). Route B mode (sale / lien / income) and external income per archetype from `[income]`.
- Cumulative external income paid, Route D settled at death and accrued (a receivable, not in the fund: D4d), lambda pass-through (`lam_C`, `lam_D`, `death_verify`, with `verify_down` from the rule set).
- Removed: `valid_windows` (unused), the local `load_jst` (it shadowed the `wdt_jst` import), `_route_b_cell`.
- TOML `[rates.defaults]`: `route_mix`, `route_mix_weights`, `lam_C`, `lam_D`, `death_verify` (defaults reproduce the old behaviour). 11 new scenarios `gl_arch_*`, appended to `[rates.run].scenarios`. `[route_b]`, `[income]`, `[archetypes.*]` untouched.

## Verification (sandbox, stride 20, 26 windows per scenario)
| check | result |
|---|---|
| Done-when: `route_b_mode = "sale"` reproduces current numbers: gain_ladder, gl_rb_sale, gain_ladder_rule_base, heir_fresh, cohort_central, gl_top6_1 | **0 differences** in every legacy key of the scenario JSON block (tolerance 1e-9) |
| Engine checks: mixture sums to 1, anchors exact, D accrues then settles at death, a death touches only its own lines, lambda invariant under `allow` and weakly costly under `reset`, income cap respected, finite through a crash | 20/20 |
| Patcher: second run is a no-op; CRLF input gives identical output; a half-patched state is refused | pass |
| Kernel transcription: `kernel_test.py` | 14/14 |

**Drift to report (numbers that change):** lien and income modes are not identical to the old inline engine. `wdt_gdp_mean` differs from legacy by a median of 0.3% (lien), 6.5% (lien, spread 6%), 0.9% (income) and 0.6% (income, cap 50%) across windows. Cause: the old engine applied the Route B share to each year's tax; the kernel holds Route B as a share of holdings and allocates the assessment by route. Lien outstanding at window end differs more (about 35% lower in a single-line probe, 60x on the sandbox median); the heir tax is paid rather than deferred into the balance. I did not change any numerics to hide this; the work order only requires parity in sale mode. Please confirm that the kernel semantics are the intended ones for lien/income, and S3 should confirm the heir-tax handling.

**Speed:** sale mode about 1.0x to 1.7x the legacy time; archetype scenarios about 2x. Use `--stride` or `--scenario` for iteration. The run list is 11 scenarios longer.

## Needs the real pipeline / your call
1. Run `--parity` on the real JST (stride 1 would be the strict test).
2. `check_inputs` stops with a message if `wdt_core` drops the new `[rates.defaults]` keys or does not expose `p['archetypes']`; I could not see the real parser.
3. `rates_core.load_jst(rp)` no longer exists locally: `main` now calls `wdt_jst.load_jst(p['rates']['jst_path'])`. Any other caller (rates_test.py, tables) that passed `rp` must change.
4. Request to S3 (kernel): `step_death(..., mask=None)`. Until it exists, a death cuts the dying lines out of the Book, runs `step_death` on the smaller Book and writes back (`_sub_book` / `_write_back`, uses `copy.copy`).
5. Decisions still open from the Work Order (single-life block, `p['g']` naming, plan open items 1 to 3, HLC burden source): not touched.

## JSON contract for S4 (all additive; no legacy key changed)
- Scenario block: `routes` = `{mix, archetypes, b_mode, r_def, income_cap, in_kind_baseline, band_edges_gbp_m, band_wealth_share{A,B,C,D: per band}, band_income_ratio}`; `verification_applied` = `{toml, applied{lam_C, lam_D, lam_D_input, dauc, death_verify, verify_down}}`.
- Window rows: `dsettle_gdp_mean`, `accr_d_gdp_end`, `accr_d_gdp_max`, `income_gdp_mean`, `income_cum_gdp`, `income_cum_gdp_band{i}` (shares of GDP). Income is included in `tax_gdp_mean` and net, shown separately; `accr_d_gdp_end` and `lien_out_gdp_end` are receivables, not in the fund. `wdt_gdp_mean` now includes Route D settled at deaths.

## Which of code or skill I followed
Where the skill and the code agreed (kernel is the single source for route mechanics; cores never import each other; TOML owns inputs) I followed both. Where they differed (the old inline lien/income semantics vs the kernel's) I followed the Work Order and the kernel, and report it above rather than matching the old numbers.
