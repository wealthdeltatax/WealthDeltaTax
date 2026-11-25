# Model v3: inventory of v2 for the port by exception (brief 037c)

Status: read-only inventory for stage C; verdicts are recommendations for 039g and the author, not decisions. Date 2026-11-18. Paths: the four files are in `model_v2/`; `valgen_core.py` is `model_v2/VAL/valgen_core.py`, `rates_core.py` is `model_v2/RATES/rates_core.py`. Repo at `67b3ccb` (main), branch `brief/037-v2-port-inventory`. No file in `model_v2/` was edited, moved or formatted; every command below was run with bytecode writing off. Sources: `docs/briefs/011g-model-v3-design.md`, `research/model-audit/synthesis.md` sections 4, 5 and 10, `docs/model-v3/outputs.yml` and `metrics.md`, the four v2 files, `model_v2/test/`, and the papers named per item.

## 0. What this says

1. **Port the kernel, not the legacy taxpayer code.** `wdt_kernel.py` (564 lines) carries all of v3's tax mechanics; all 6 large functions port, 2 as is and 4 with change. The legacy single-taxpayer functions in `wdt_core.py` (`simulate`, `simulate_sell`, `settle_tw_flows`, `run_sim`, `run_sim_hist`, 226 lines) serve only the valgen bridge and `eval_core`; keep them in `model_v2/` as the test oracle, do not copy them.
2. **The rest of `wdt_core.py` is a rewrite or a drop.** 646 of its 1,000 table lines are rewrites (parsers, a JSON helper, the identity, three output-layer functions that sit in a base module, R4) and 323 are drops. No test exists for any of it.
3. **JST and the window rule port.** `jst_r6.json` reproduces the register: GBR real capital return 4.42% over 117 years. `wdt_jst.py` has the only passing self-test in the four files.
4. **Two paper-versus-code mismatches need the author before 039g** (section 3.3): v2's kernel refund is tau x abs(delta) x W_new / W_prev, not the tau x loss that WP section 3.5 states; and the rate formula printed in RATES section 4 gives 10.5% at W_min, not the 15.0% the paper and v2 use.
5. **v2's tests are nearly absent.** Four test files that `WDT_Code_Reference.md` names do not exist. The kernel has no unit test. `pytest model_v2/test` aborts; the folder has no runner (section 5).
6. **v2's identity is two terms in practice.** `settle_delta` is exactly 0 at 70 of 70 (alpha, g, N) points, so a v3 identity test needs a case where the third term is non-zero (section 3.4).

## 1. Function table

One row per function or class of 30 lines or more in the four files (27 rows; the nested `Book.__init__` is counted inside `Book`). Line counts are `end - start + 1` from `ast`. Module-level imports: `wdt_kernel` `__future__`, `dataclasses`, `numpy`; `wdt_core` `math`, `tomllib`, `pathlib`, `bisect`, `functools`, `json`; `wdt_jst` `json`, `math`, `pathlib`; `wdt_par` `math`, `os`, `concurrent.futures`, `multiprocessing`. None imports another project module at module level; `wdt_core` imports `wdt_jst` inside `jst_basis` (line 316). The Imports column shows only imports made inside the row. Verdicts: **port** (as is), **port with change**, **rewrite** (v3 needs it, v2's form does not fit), **drop**.

| File and lines | Name (lines) | Computes | Imports in row | Tests | Needed by (`outputs.yml`) | Verdict | Reason |
|---|---|---|---|---|---|---|---|
| `wdt_kernel.py` 80-114 | `Flows` (35) | Per-line results of one operation: signed value, credited value and units by route, plus rate, delta, L (+ tax, - refund), income | - | T1 | O1a, OB1, O2b | **port** | Plain dataclass that every output reads. The `income` field stays only if Route B income mode does. |
| `wdt_kernel.py` 121-194 | `Book` (74) | State of n family lines over routes A, B, C, D, Cv: holdings, basis, declared price, envelopes (`E_cash`, `EC`, `uo`), `lost_refund`, lien, accrued D | - | T1 | OW3, OB1, O1a | **port with change** | Keep the envelopes and `lost_refund` (M15a, B1d). Add cumulative paid and refunded per line per year: M15a needs "first year it binds", the Book keeps only the current balance and a `min_E_cash` diagnostic. Drop `verify_down` and the Cv state if verification is out of v3. |
| `wdt_kernel.py` 131-171 | `__init__` (41) | `Book` constructor: validates `c_cap`, `b_mode`, `verify_down`; allocates the state vectors | - | T1 | as Book | **inside Book** | Nested method. Counted in Book; left out of the totals so no line counts twice. |
| `wdt_kernel.py` 222-269 | `_route_tax` (48) | Settle route r's share of the year's tax (+) or refund (-): A and B by sale, lien or income; C and Cv in kind; D accrues | - | T1 | O1a, O2b, O2c | **port with change** | The route set and Route B modes are a 039g decision. The refund caps (lines 211-221, 255-262) follow whichever envelope rule the author fixes (section 3.3). |
| `wdt_kernel.py` 276-311 | `assess` (36) | One assessment on total declared wealth: tax tau x delta on a rise, refund tau x abs(delta) x W_new / W_prev on a fall (line 301), split across routes by delta shares | - | T1 | O1a, O2, O3, OD1 | **port with change** | Structure ports. The refund line is v2's ratio-mirror, smaller than the papers' tau x loss by the factor W_new / W_prev (section 3.3); the author fixes the rule. |
| `wdt_kernel.py` 479-516 | `step_death` (38) | Death of the holder: verify C, auction D, settle B, zero the envelopes (lines 507-510), tax the heir as a delta from zero | - | T1 | O3, O1a | **port with change** | Keep the `delta` heir rule only; the fresh-entrant rule is not carried over (decision). The envelope reset conflicts with the inheritance sentence of WP section 3.5 (section 3.3). |
| `wdt_kernel.py` 528-564 | `run_lines` (37) | Run n lines for T years with a death every G years, calling `step_year` and `step_death` | - | T1 | O1a, O2, O3, OP1 | **port** | Thin driver. It takes any T x n growth matrix, so v3 return paths feed it unchanged. |
| `wdt_core.py` 147-177 | `tau` (31) | Marginal rate at declared wealth: logistic in W, logistic in ln W, or a ladder of anchors; 0 below W_min | - | T1 | O1a, O2, OF1, OT1 (every output, through the schedule D2) | **port with change** | Keep the two logistic branches; drop the ladder branch (decision). Add the R10 rejection of a non-progressive draw. The entry-rate form differs from the formula printed in RATES section 4 (section 3.3). |
| `wdt_core.py` 216-248 | `rate_spec_from_scenario` (33) | Turns a `[rates.scenarios.NAME]` block into `tau()` inputs in pounds m | - | none | none | **drop** | Serves the 101-scenario table, which is not carried over. |
| `wdt_core.py` 376-409 | `settle_tw_flows` (34) | Settles the post-sale tax/refund oscillation and returns the flows | - | T4 | none | **drop** | Legacy device 'kept for the bridge only' (`valgen_core.py` line 99). M7 is net tax over the horizon (metrics.md); no v3 output has a post-sale oscillation. In v2 it contributed 0 at 70 of 70 grid points (section 3.4). |
| `wdt_core.py` 441-487 | `simulate` (47) | One Route C taxpayer over N holding periods: delta tax, refund tau x delta capped by cumulative tax (line 477), in kind | - | T4 | none directly; OD1 and O7 through the kernel | **drop** | The kernel is the single code path for v3. Keep this function in `model_v2/` as the oracle for the single-life reduction test, and freeze its numbers at a few (alpha, g, N) as expected values in a v3 test. |
| `wdt_core.py` 494-538 | `simulate_sell` (45) | Terminal Route C sell event (period N+1): sell-year delta, refund, terminal wealth | - | T4 | none | **drop** | Same reason; its only extra consumer is `eval_core`, which does not import (section 5). |
| `wdt_core.py` 563-615 | `run_sim` (53) | Constant-g simulation, then the post-sale settlement | - | none | none | **drop** | Reached only through `run_pair`; the one other mention is a docstring in `wdt_fmt.py` 252. |
| `wdt_core.py` 622-668 | `run_sim_hist` (47) | The same, driven by a return series `p_in["returns"]` | - | T4 | none | **drop** | Only `valgen_core` calls it (bridge at 1121, `_p7_replay`). |
| `wdt_core.py` 900-933 | `breakeven_rho` (34) | Discount rate at which the state's PV shortfall from alpha equals a tolerance (VAL.A C.12) | - | none | none | **drop** | No caller outside its own file; no output id. |
| `wdt_core.py` 966-995 | `npv_tax_advantage` (30) | PV(alpha) - PV(1) of tax, as a fraction of terminal wealth (VAL.A C.12) | - | none | none | **drop** | Called only by `breakeven_rho`. |
| `wdt_core.py` 1002-1068 | `decompose_tw_advantage` (67) | Splits TW_settled(alpha) - TW_settled(1) into W_sell_delta, refund_delta, settle_delta and returns `identity_error` | - | none (returns its own `identity_error`; nothing asserts it) | none (no output id; nearest OD1 / M7d) | **rewrite** | The identity is a candidate (decision) and v3 needs it as a test, not a function. v2's form calls the legacy functions that are dropped. Rewrite on the kernel path (section 3.4). |
| `wdt_core.py` 1291-1325 | `threshold_outcomes` (35) | What a relief (share of GDP) buys under `[rates.replacement]`: retire taxes in order, then lift the threshold | - | none | O4a, O4b, O1d, OP5 | **rewrite** | Output-layer logic inside a base module (R4). By launch-wealth band and static growth; M4a and M4b need income deciles and retired taxes by incidence. |
| `wdt_core.py` 1349-1391 | `threshold_beneficiaries` (43) | Who gains when the common threshold is x, and by how much (static, growth-adjusted) | numpy | none | O4a, O4b | **rewrite** | As above; read only by the RATES tables and charts scripts. |
| `wdt_core.py` 1393-1484 | `band_net_position` (92) | Net position of each launch-wealth band under the tax replacement | - | none | O4a, O4b, O2 | **rewrite** | As above. The largest function in this group (92 lines), by wealth band, not income decile. |
| `wdt_core.py` 1490-1520 | `json_safe` (31) | Converts numpy scalars and arrays, nan and inf to plain JSON types | math, numpy | none | none (output writer, R4 third layer) | **rewrite** | v3 needs a writer in its own layer; the nan and inf rule is a 30-line spec to re-implement with a test, not to carry in the core. |
| `wdt_core.py` 1645-1828 | `_parse_rates` (184) | Validates and normalises the `[rates]` section (the `[rates]` section) | - | none | none (register R3) | **rewrite** | v3's inputs are a register with low, central and high (R3, `inputs.md`), not v2's `[rates]`. |
| `wdt_core.py` 1831-1871 | `_parse_phase2` (41) | Validates `[route_b]`, `[income]`, `[verification]`, `[archetypes.*]` | - | none | none | **rewrite** | The allowed values of the kernel options travel as constructor checks in `Book.__init__` (line 135); the TOML schema does not. |
| `wdt_core.py` 1891-2043 | `load_params` (153) | Loads the TOML into one parameter dict; default path `Path(__file__).parent / "WDT_Params.toml"` (line 118) | - | none | none (register R3, country pack R11) | **rewrite** | New parameter file and country pack (038c). The hard-wired default path and the schema of v2's sections do not fit. |
| `wdt_jst.py` 58-88 | `loop_windows` (31) | Windows of length T over the usable years: contiguous or wrapping at the seam, with flags | - | T2 | OP1, OR1, OF1, if 036r keeps historical windows | **port** | Pure, 31 lines, self-tested. Both v2 cores already share it (D1b). Contingent on 036r. |
| `wdt_jst.py` 130-172 | `real_basis_inputs` (43) | Geometric-mean real capital return and real GDP/head growth of one country from the raw JST record | - | T2 | drivers I-D1a; O1a | **port with change** | Reproduces the register: GBR 1896-2019, 117 years, g_real = 0.0442 (section 3.2). Add the arithmetic mean that `drivers.md` section 1 needs (about 4.76%). |
| `wdt_par.py` 83-146 | `WorkerPool` (64) | Persistent ordered process pool with thread-count limits (line 99 sets BLAS thread variables) | - | T3 | none | **drop** | No output id needs it. v3's range runner may: decide after 039g sizes the run, and then port it with its self-test. |

- **T1**: no unit test in the repo. `kernel_test.py` and `bridge_test.py` are named in `WDT_Code_Reference.md` sections 3 and 6 and do not exist. Indirect: the in-`main` bridge and validators of `valgen_core` (`_bridge` 1064, `_validate` 1132); not run.
- **T2**: self-test `python model_v2/wdt_jst.py` (lines 210-243, synthetic data): PASS, 0.03 s.
- **T3**: self-test `python model_v2/wdt_par.py` (lines 161-192): PASS, 0.59 s.
- **T4**: `valgen_core._validate` check `single_life_equals_legacy_simulate` (line 1195, tolerance 1e-9) and the bridge at 1105-1121; not run.

Output ids are those of `outputs.yml`; "needed by" means the output cannot be produced without the mechanism, as far as `metrics.md` defines it. Which routes and modes v3 keeps is a 039g decision, so route-specific rows are conditional on it.

## 2. Line totals by verdict

Top-level rows only (the nested `Book.__init__` would count 41 lines twice). "Short functions" are top-level functions under 30 lines; "outside" is the module docstring, imports, constants and blank lines.

| File | `wc -l` | port | port with change | rewrite | drop | Rows total | Short functions (count) | Outside any function | Check |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| `wdt_kernel.py` | 564 | 72 | 196 | 0 | 0 | 268 | 168 (13) | 128 | 268+168+128 = 564 |
| `wdt_core.py` | 2043 | 0 | 31 | 646 | 323 | 1000 | 662 (51) | 381 | 1000+662+381 = 2043 |
| `wdt_jst.py` | 243 | 31 | 43 | 0 | 0 | 74 | 58 (6) | 111 | 74+58+111 = 243 |
| `wdt_par.py` | 196 | 0 | 0 | 0 | 64 | 64 | 60 (7) | 72 | 64+60+72 = 196 |

Kernel: 268 of 268 table lines port (72 as is, 196 with change); the other 168 lines are 13 short functions listed below. Core: 31 port with change, 646 rewrite, 323 drop, of 1000 table lines; 662 more lines sit in 51 short functions, which follow the neighbours they serve (parsers, rate and window helpers, formatting) and are covered by the same verdicts. `wdt_jst.py`: 31 port, 43 port with change. `wdt_par.py`: 64 drop.

Kernel functions under 30 lines (line, length), all of which go with the kernel: `_arr` 64 (3), `_div` 69 (4), `_move` 201 (8), `_refund_cash` 211 (9), `rebase` 314 (5), `grow_and_consume` 325 (17), `declare` 344 (25), `verify_C` 371 (29), `verified_share` 402 (6), `settle_D` 410 (16), `settle_B` 428 (16), `step_year` 450 (27), `settle_terminal` 519 (3). Exception: `verify_C`, `verified_share` and the Route D / Cv part of `declare` serve the verification hazard (lambda_C, lambda_D). No output id in `outputs.yml` names it; port them only if 039g keeps verification. `valgen_core` calls `verified_share` once (`VAL/valgen_core.py` 780) and reports it in the `p4_lambda_sweep` JSON that the VAL tables and charts read.


## 3. The four candidates

### 3.1 v2's layering and `wdt_kernel` (candidate 1)

- **Where.** `model_v2/wdt_kernel.py`, 564 lines; imports `__future__`, `dataclasses`, `numpy` and no project module. Line ranges are in section 1. `rates_core.py` 150-154 imports `wdt_core`, `wdt_kernel`, `wdt_par`, `wdt_fmt`, `wdt_jst`; `valgen_core.py` 125-128 imports `wdt_kernel`, named `wdt_core` functions, `wdt_fmt`, `wdt_jst`. The kernel is therefore a clean base: nothing under it, two cores above it.
- **Where the layering fails (R4).** The third layer, the output writer, is not separate. `8_2_RATES_tables.py:65` and `8_3_RATES_charts.py:56` import `wdt_core as wc` and call `threshold_outcomes`, `threshold_beneficiaries` and `band_net_position`, which are output-layer logic in a base module (section 6).
- **Tests, existing.** None for the kernel itself (T1). **Missing, and needed under R7:** hand-computed single-line cases for each route; the ratio-mirror round trip (a loss then the same rise, section 3.3); the lien recursion; the envelope binding (`lost_refund` > 0); the single-life reduction to a frozen `simulate` result; the `delta` heir rule across a death.
- **Papers require.** RATES section 4 and WP section 3.5 for the tax and refund; GOV clause 2 (`papers/legacy/7_Constitutional_Governance.md` 268) for corrective over-declaration: a Route D auction gives a basis correction and no refund, which is what the kernel's `reset` does. The default `verify_down='allow'` (write-down) is set by the `[rules]` sets in `WDT_Params.toml` (147-151, 212, 754).
- **Verdict.** Port the kernel with the changes in section 1; the layering is a rule for v3, not code to copy.

### 3.2 The JST series `model_v2/jst_r6.json` (candidate 2)

- **Where.** `model_v2/jst_r6.json`, 1,769,472 bytes, 18 countries; GBR covers 1870-2020 (151 years). Loaded by `wdt_jst.load_jst` (181-197); used by `rates_core.py` 154, `valgen_core.py` 128 and `wdt_core.jst_basis` (308-). `synthesis.md` section 10 used 14 countries for a spread check.
- **Check run.** `real_basis_inputs(J, 'GBR')` gives g_real 0.0442 over n = 117 (1896-2019) and index_rate 0.018718. That reproduces register I-D1a (4.42%).
- **Tests, existing.** The `wdt_jst` self-test uses synthetic data only (T2); no test opens the file. **Missing:** a pin test that GBR gives 4.42% over 117 years, a row count per country, and a checksum so a data change shows (R5).
- **Papers require.** RATES section 5 (`papers/legacy/8_Rates_and_Revenue.md` about 295: 73 years of UK equity data) and section 6 (SSM uses actual historical returns; TCM uses rotated series). The data in the file is longer than the papers state; 036r decides which sample v3 uses.
- **Verdict.** Port the file unchanged, with `loop_windows`, `real_basis_inputs` (plus the arithmetic mean) and `real_return_series`.

### 3.3 Loss-refund and delta-tax mechanics as the papers state them (candidate 3)

- **Where.** Tax and refund in `wdt_kernel.assess` 276-311 (the refund line is about 301); caps in `_refund_cash` 211-221 (A, B, D, by the pooled cash envelope `E_cash`) and `_route_tax` 255-262 (Route C, by units paid `uo`, and `EC` under `units_and_value`); `lost_refund` records what the cap forgoes. Death in `step_death` 479-516. The papers' form is the legacy `simulate` (`wdt_core.py` 441-487): about line 475 `rate = tau(W_new, p)`, 477 `L = max(-cum, rate*delta) if (delta>0 or cum>0) else 0`, 480 `cum += L`.
- **Mismatch A: refund size.** The kernel refunds `rate * abs(delta) * W_new / W_prev`, with `rate = rate_fn(W_new / idx)`: tau x loss x (W_new / W_prev). WP section 3.5 and RATES section 4 state the refund as the marginal rate on an equivalent gain, 25% of the loss at a 25% rate. The ratio-mirror is author decision D5 (`docs/VAL_generational_model_plan.md` 30, 64, 93); the papers (`source/`) never state it. The author fixes which rule v3 uses before 039g.
- **Mismatch B: envelope at death.** `step_death` 507-510 zeroes `uo`, `EC` and `E_cash`; WP section 3.5 says the family's accumulated contribution history persists in the envelope.
- **Mismatch C: rate formula.** `papers/legacy/8_Rates_and_Revenue.md` 237 prints tau(W) = tau_m / (1 + ((1 - tau_0) / tau_0) e^{-k(W - W_min)}). v2 `tau` (`wdt_core.py` 147-177) uses (tau_m - tau_0) / tau_0 in place of (1 - tau_0) / tau_0, which is what VAL section 5 states. At W_min = 2 (GBP m), tau_0 = 0.15, tau_m = 0.70, k = 0.001 the printed formula gives 10.50% and the code 15.00%; at W = 200 they give 12.39% and 17.46%; at W = 1000, 22.66% and 29.77%. Not fixed here; for the guru and the writing lane.
- **Not in v2.** The papers' "excess repaid first by future gains" rule and voluntary repayment do not exist in the kernel; under the cap they do not arise.
- **Tests, existing.** None on the kernel (T1); the legacy form is checked against the kernel only in the valgen bridge (T4). **Missing:** the cap cases (refund = cumulative tax exactly; one pound over), each of mismatches A to C as an explicit test once the author rules.
- **Verdict.** Port the structure; the refund rule and the envelope reset are the two lines the author must decide.

### 3.4 The decomposition identity (candidate 4)

- **Where.** `wdt_core.decompose_tw_advantage` 1002-1068; the definitions are at 1046-1056 and it returns `identity_error`. The identity: tw_adv = W_sell_delta - refund_delta - settle_delta. No function outside `wdt_core` calls it and nothing asserts it.
- **Measured (read-only call).** At alpha = 1.5, g = 10.45%, N = 30: residual -1.4e-14 with the default logistic and 7.1e-15 with `with_rate_scenario` (ladder). Over a 70-point grid (alpha 0.5 to 5, g -3% to 20%, N 10 and 30) the worst |identity_error| is 5.68e-14.
- **Gap.** `settle_delta` is exactly 0 at all 70 points, so v2 never exercises the third term. The v1 case in the audit had +3.9188 (`research/model-audit/v1-errors.md` 47 and `v1-inventory.md` 125: same point, settle_delta +3.9188 in v1). A v3 test needs a case where it is non-zero.
- **Tests, existing.** None. **Missing:** the identity as an assertion on the kernel path at the 70-point grid, plus one case with settle_delta != 0, tolerance 1e-12.
- **Papers require.** VAL section 5.2 (Fig 5.2b caption) and VAL.A section C.11.
- **Verdict.** Rewrite as a test on the kernel path (section 1), not a core function.

## 4. Where v2 computes the pieces C1 item 3 needs

C1 item 3 must reproduce v2's 7.34% of GDP at v2-like inputs. That number is `wdt_gdp_h` of the `logistic_ln_ref` scenario: the post-fill 10-year mean WDT take, % of GDP (`synthesis.md` section 10: 117 UK windows; relief 9.62 = WDT 7.34 + levy 2.77 - 0.6 net fund). It is not the 100-year mean. `rates_core.py` unless stated; inputs come from `run_window` 1508-1673.

| Piece | Where | Inputs read |
|---|---|---|
| Wealth-weighted effective rate (epsilon) | `effective_rates` 1038-1067, called at 1547; exposed as `er_*` columns (`er_stock_payers`, `er_gain_payers`) | `out['lvl']` (`net_b`, `wealth_b`, `gain_b` = r x prev_w, built in `run_cohorts` 985-1035) and `cal['share']`. Gain rate = sum(net) / sum(r_t x W_{t-1}) over all adults, payers and top-q. Net includes inheritance receipts. |
| Refund cap | `wdt_kernel.py` 211-221 and 255-262 (section 3.3) | `E_cash`, `uo`, `EC` |
| Reserve fill | `run_fund` 1109-1193 with `trailing_mean` 1100-1106; `make_cfg` 1206-1215 | net, E, r, refund, safe, ms = 3, ml = 3, a_window = 5, w_relief, safe_share, horizon = 10. A_t = trailing mean of max(net, 0). Fill when S_pre >= (ms + ml) x A_t. After the fill R* = trailing mean of surplus after upkeep and R = min(R*, S_pre - SRR). Failure events: unmet, ring, insolvent. |
| Fund metrics and identity | `_fund_metrics` 1436-1459 (`relief_gdp`, `cov_ref`); identity stated at line 109 and in `_horizon_cols` 1474-1505 | `wdt_gdp_h` (the 7.34), `levy_gdp_h`, `fund_inc_gdp_h`, `fund_ret_gdp_h`, `stockrate_h_band{i}` |
| Closure test | **Not in tracked v2 code.** The `synthesis.md` section 10 test (relief against retired receipts) was run on a scratch copy with `store_windows` forced on. Nearest code: `calibration` 1281-1289 (`replaced_ref`, `rev_ref`, `exp_ref` from `rp['closure']['replaced_tax_gdp']`); `run_window` 1605 and 1662-1667 (`nonwdt_req_*`, `wdt_share_of_spend`); `calibrate_levy` 1388-1433; `build_meta` 2033-2041 (`closure_replaced_tax_gdp`); `[rates.replacement]` (`WDT_Params.toml` 980, `retire` order) with `wdt_core.threshold_outcomes` | |
| Decomposition identity | `wdt_core.py` 1002-1068 (section 3.4) | alpha, g, N, `p` |

- **Realised epsilon is not recorded in the repo.** `tornado.md` section 4 backs it out of 7.34%: 30.0% at register inputs, 24.5% at v2-like inputs. `effective_rates` covers the whole 100-year window; no post-fill gain rate is recorded, so the 7.34 cannot be matched to epsilon without a run (section 7, question 1).
- **Inputs of `logistic_ln_ref`** (`WDT_Params.toml` 1364): tau_0 = 0.04, schedule `logistic_ln`, `wmin_house_ratio` 0.5, `dist_kw` body_split 5; the WID distribution (`build_dist` 408-462, `calibrate` 496-525, `cohort_spec` 528-557, `build_scenario` 560-599); UK JST windows (T = 100, start_stride 1); `horizon`; expenditure growth.

## 5. Existing tests

Run read-only, with `python3 -B -I` so no bytecode is written to `model_v2/`. Python 3.13, pytest 9.1.1, numpy 2.5.3, pandas 3.0.5.

| Command | Result | Time | In v3? |
|---|---|---|---|
| `python3 -m pytest -p no:cacheprovider model_v2/test` | **INTERNALERROR**, "no tests ran": `test_hlc_drift.py` line 23 calls `sys.exit(0)` at import | 0.39 s | Pytest is not a usable runner for that folder. |
| `python3 model_v2/test/test_hlc_drift.py` | exit 0; prints `WARN [val_gen.hlc] is a PLACEHOLDER: HLC pair is skipped by valgen` (`--strict` not run; by the code it would exit 1 on a warning) | 0.06 s | Drop: v2-specific. Keep the drift-test pattern only. |
| `python3 model_v2/wdt_jst.py` | PASS: `wdt_jst self-tests ok: {'total': 10, 'contiguous': 7, 'wraps': 3, 'repeat': 0, 'repeat_share': 0.0}` | 0.03 s | Travels with `loop_windows` and `real_basis_inputs`. |
| `python3 model_v2/wdt_par.py` | PASS: `wdt_par self-test ok` | 0.59 s | Travels only with `WorkerPool`. |

- `model_v2/test/` holds `test_hlc_drift.py`, `print_hlc_calibration.py`, `wdt_patchlib.py`, `patchlib.py` and `diff_json.py`; only the first is a test. `diff_json.py` is a possible R5 regression tool.
- `kernel_test.py`, `bridge_test.py`, `rates_test.py` and `test_valgen_pairs.py` are named in `WDT_Code_Reference.md` (sections 3 and 6 and elsewhere) and exist nowhere in the repo.
- **Not run:** the in-`main` bridge and validators of `valgen_core` (`_bridge` 1064, `_validate` 1132, `_p2b_validate`, `_p5_validate`, `_p6_validate`) and `rates_core.validate` 2056-2079; they run the scenario machinery, which is out of scope.

## 6. Layering violations and import side effects (R4, R8)

- **Import side effects: none.** Importing the four files takes 0.100 s, leaves the environment unchanged and writes only `__pycache__`. numpy is imported at import time (kernel). The only module-level statements besides definitions are the `if __name__ == '__main__'` guards (`wdt_jst.py` 210, `wdt_par.py` 195); no module-level calls.
- **R4, `wdt_core.py` is not a core.** Path and IO: `_DEFAULT_TOML = Path(__file__).parent / 'WDT_Params.toml'` (118), TOML opens (1880, 1902), `save_json` (about 1547), `load_json` (1554). A pandas helper `table_to_frame` (about 1560). Output-layer functions `threshold_outcomes` 1291, `threshold_beneficiaries` 1349, `band_net_position` 1393, `json_safe` 1490, read only by the RATES tables and charts scripts (`8_2_RATES_tables.py:65`, `8_3_RATES_charts.py:56`).
- **R4, lazy imports to hide layering.** `wdt_core` imports `wdt_jst` inside `jst_basis` (316), numpy inside functions (1099, 1115, 1132, 1205, 1217, 1360, 1498), pandas (1560), json (1524, 1553). Module-level `pathlib` (116), `bisect` (142), `functools` and `json` (1193-1194).
- **R4, `wdt_jst`.** Reads data from `_HERE` and `_JST_DIRS` (175-177; opens at 194), so the loader is not separate from the pure window rule.
- **R8, `wdt_par`.** Line 99 sets five BLAS thread variables in `os.environ` when a pool opens (inherited by workers; a side effect at `__enter__`, not at import).
- **R8, orphan code.** `model_v2/EVAL/eval_core.py` does not import (`wfr_core`, a v1 module, line 62) and reads retired TOML sections. The legacy functions of section 1 are reached only by `valgen_core` (bridge and `_p7_replay`) and that orphan; `valgen_core.py` 99 calls them a "LEGACY DEVICE KEPT FOR THE BRIDGE ONLY". `breakeven_rho` and `npv_tax_advantage` have no caller outside their file.
- **R5, output location.** `rates_core.json_path()` writes under `model_v2/OUTPUTS/`, which is absent and not git-ignored (`git check-ignore` finds no rule); a scenario run in place would dirty the tree.

## 7. Open questions, suggested entries and the check

**Questions for the author** (answered 2026-11-18: 1. no run of `logistic_ln_ref`; 2. the papers' rule, tau x loss, for the refund; the envelope resets at death, as v2 does. Recorded in `stage-c-decisions.md` items 9 and 10.)
1. Run `logistic_ln_ref` once to record its realised epsilon? Default: no. How: `rates_core.main` (2082-2124) has `--scenario`, `--fresh`, `--workers`, `--stride`, `--toml`; it writes `model_v2/OUTPUTS/RATES/rates_data.json` (`rates_core.py` 7 and 176-178, `wdt_fmt.out_dir` 390; folder absent, not git-ignored), so the run must be in a scratch copy outside the repo; `store_windows` is not set for this scenario (true at `WDT_Params.toml` 1074 and 1346 for others); run time is unmeasured. A post-fill gain rate would also need a small change to `effective_rates`, which is not part of this brief.
2. The refund rule for v3: tau x loss as the papers state, or v2's ratio-mirror (section 3.3, A)? And does the envelope persist at death (B)?

**Suggested `docs/brief-suggestions.md` entries** (not added: the brief's Touches list forbids other files)
- RATES section 4 formula at `papers/legacy/8_Rates_and_Revenue.md` 237 does not match v2 or VAL section 5 (section 3.3, C). Lane: guru and writing.
- `model_v2/test/test_hlc_drift.py` calls `sys.exit(0)` at import, so pytest aborts on the folder. Lane: none unless v2 is revived.
- `kernel_test.py`, `bridge_test.py`, `rates_test.py` and `test_valgen_pairs.py` named in `WDT_Code_Reference.md` do not exist.

**Check script** (row count against the source; the table in section 1 is read from this file). Run from the repo root as `python3 -B -I check.py` after saving the block:

```python
import ast, re
FILES = ['wdt_kernel.py', 'wdt_core.py', 'wdt_jst.py', 'wdt_par.py']
want = set()
for f in FILES:
    src = open('model_v2/' + f, encoding='utf-8').read()
    for n in ast.walk(ast.parse(src)):
        if isinstance(n, (ast.FunctionDef, ast.ClassDef)) and n.end_lineno - n.lineno + 1 >= 30:
            want.add((f, n.name, n.lineno, n.end_lineno))
doc = open('docs/model-v3/port-inventory.md', encoding='utf-8').read().split('## 1. ')[1].split('## 2. ')[0]
have = {(m[0], m[3], int(m[1]), int(m[2])) for m in re.findall(r'^\| `(\w+\.py)` (\d+)-(\d+) \| `(\w+)` \(', doc, re.M)}
assert have == want, (sorted(want - have), sorted(have - want))
print('table rows match the source:', len(want))
```
