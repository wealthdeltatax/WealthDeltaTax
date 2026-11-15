"""W2-07  Docs sync: WDT_Code_Reference.md and the WDT_Refactor_Plan.md status line, after S1-S5, S7 and D11.

If the .md files are outside Model/, pass --root <folder holding them>.  Text only; numbers neutral.
Not covered: the drift register (not provided).  Review the Code Reference sections on wdt_kernel / valgen P3-P5 once: they are
rewritten from the code as it stands, not from a design note.
"""
import re
from patchlib import Patch
P = Patch('W2-07', __doc__)
S = re.S | re.M
R = 'WDT_Refactor_Plan.md'
C = 'WDT_Code_Reference.md'

# ---- Refactor plan ----------------------------------------------------------------------------------------------------
P.replace(R, "Status: agreed in discussion, 10 October 2026. No code written yet.",
"Status (14 October 2026): agreed 10 October. Built: Phase 1 (JST loop `wdt_jst`, real basis, ladder baseline, archetypes, [verification], [route_b], [income], [rho]), "
"the shared kernel (D12, `wdt_kernel`), Phase 2 `valgen_core` (S1, S5 tables and charts), Phase 3 `rates_core` (S2, S4, T = 100), and D11 (patches W2-01 to W2-07: legacy SSM, "
"`[swf]` `[budget]` `[returns]` `[tcm]` `[[tiers]]` `[[brackets]]` and `N_fill` removed; `p['g']` is `p['g_real']`; HLC burdens held in `[val_gen.hlc]`). "
"Bridge test D9 passes (A: kernel vs `run_family3`; B1: RATES line exact). Pending: S6 (downstream overhaul), the real HLC calibration, "
"the single-life block retires to `wdt_legacy_v7.py` after D9 sign-off, Phase 5 re-run and claims (D8, D10).")

# ---- Code reference -----------------------------------------------------------------------------------------------------
P.replace(C,
"- `valgen_core` imports `wdt_core` and `wdt_fmt`. `rates_core` imports `wdt_core` and `wdt_fmt`. Cores do not import each other.",
"- `valgen_core` imports `wdt_core`, `wdt_kernel`, `wdt_jst` and `wdt_fmt`. `rates_core` imports `wdt_core`, `wdt_kernel`, `wdt_jst` and `wdt_fmt`. Cores do not import each other, and presentation never imports a core.\n"
"- `wdt_kernel` is the shared route-settlement kernel (D12). `wdt_jst` loads the JST history and builds loop windows and the real basis inputs.")

P.regex(C, r"\| `\[rate\]` \| Legacy logistic.*?\n\| `\[val\]` \|",
"| Retired (D11) | `[rate]`, `[swf]`, `[budget]`, `[returns]`, `[tcm]`, `[[tiers]]`, `[[brackets]]` are gone. The rate design is `[rates.defaults]` / `[rates.scenarios.*]` (VAL picks one with `[val_gen] rate_scenario`); the fund is sized by `ms`, `ml` in `[rates.defaults]`; return tiers are `[rates.cohorts.*]`. |\n"
"| `[rho]` | State-side discount rate: base and sweep (real). |\n"
"| `[route_b]`, `[income]`, `[verification]`, `[archetypes.*]` | Route B payment mode (sale, lien, income), deferral rate, external income caps and ratios, lambda_C / lambda_D, the five route-mix archetypes. Read by both cores. |\n"
"| `[val]` |", count=1, flags=S)
P.replace(C,
"| `[val_gen]` | Generational model: `T`, `G`, route shares, consumption, reset interval, lambda grids, strategy grids, test tolerances, hec/dmg/uos settings, `rate_scenario`, optional `g_real` / `index_rate`. |",
"| `[val_gen]` | Generational model: `T`, `G`, route shares, consumption, voluntary-reset sensitivity (`reset_sens`), lambda grids, strategy grids, test tolerances, hec/dmg/uos settings. Required: `rate_scenario` and `basis` (`jst` derives `g_real` and `index_rate` from JST; `manual` needs both as numbers). |\n"
"| `[val_gen.hlc]` | HLC calibration (D1d): `average_stock_rate` (net payers), `top_stock_rate` (top 0.1%), source scenario, stamp. `placeholder = true` makes valgen skip the HLC pair. Regenerate with `test/print_hlc_calibration.py --write` after a RATES run. valgen reads no RATES output. |")
P.replace(C,
"| `[sweep]` | Shared analytical grids and canonical baseline values for VAL.S, RATES.S and WFR. |",
"| `[sweep]` | Shared analytical grids. `g_offsets` (pp around `g_real`) become `g_vals = g_real + offsets` in `with_val_basis`. The `*_canon`, `rates_*_sweep` and `wfr_*` keys are retired. |")
P.regex(C, r"- \*\*Active `\[rate\]` and `\[sweep\]` canonical values differ\.\*\*.*?overrides `\[rate\]` for VAL\.\n",
"- **One rate design.** The baseline is the gain ladder (D2). Logistic schedules survive only as comparison scenarios (`logistic_ref` and others).\n"
"- **Real basis only.** There is no nominal `g`. `p['g_real']` and `p['index_rate']` exist only after `with_val_basis`; `load_params` does not set them.\n", count=1, flags=S)

P.replace(C,
"- `with_val_basis` switches VAL to a real basis (`g_real`, `index_rate`) when those keys are set.",
"- `with_val_basis` puts VAL on the real basis: `basis = \"jst\"` derives `g_real` (geometric-mean real capital return) and `index_rate` (real GDP/head growth) from the JST history of `[rates].uk_iso` (`jst_basis`); `\"manual\"` takes both from `[val_gen]`. It sets `p['g_real']`, `p['index_rate']`, `p['val_basis']` and `p['sweep']['g_vals']`.")

P.regex(C, r"- \*\*N is never implicit\.\*\* `_require_N` raises if `N` is missing\.\n.*?  - `p\['N'\]` is a legacy alias of `N_fill`\.\n",
"- **N is never implicit.** `_require_N` raises if `N` is missing. `N_val` (30) is the taxpayer holding period. The SSM fill year `N_fill` and the alias `p['N']` are retired (D11); the fund fills inside each RATES window (`fill_year` in the JSON).\n", count=1, flags=S)
P.regex(C, r"### Legacy SSM\n.*?(?=### Tax replacement)",
"### Retired legacy and what stays\n"
"The SSM (`_ssm_marginals`, `_ssm_lrr_fill_year`) and the readers of `[swf]`, `[budget]`, `[returns]`, `[tcm]`, `[[tiers]]`, `[[brackets]]` are deleted, so `load_params` is instant. "
"Kept until the D9 bridge is signed off (then moved to `wdt_legacy_v7.py`): the single-life Route C block (`simulate`, `run_pair`, `run_sim_hist`, `settle_tw_flows` and relatives, `run_sim`, `g_eff`, `synthetic_returns`). "
"`run_sim_hist` takes its series as `p['returns']`; valgen's bridge passes a JST real series explicitly.\n\n"
"### wdt_kernel (D12)\n"
"The shared route-settlement kernel. Routes A, B, C, D plus the verified tranche Cv. Route B pays by `sale`, `lien` (deferred balance at `r_def`, settled at death) or `income` (external income up to the cap, shortfall sold). "
"Route C caps are `units` or `units_and_value`. Refund is the ratio mirror (D5). lambda_C and lambda_D are independent; death verifies C; a voluntary reset is an action, not a rule. "
"`step_year` and `step_death` operate on a `Book`; `step_death` has no line mask, so `rates_core` cuts sub-books (`_sub_book`, `_write_back`). Unit tests: `kernel_test.py`; parity with both cores: `bridge_test.py`.\n\n"
"### wdt_jst\n"
"`load_jst`, `real_return_series`, `real_basis_inputs`, and `loop_windows` (windows wrap within a country's series; a window that repeats years is flagged `repeat`, one that crosses the seam is not `contiguous`; every result is reported for the full loop and for contiguous windows).\n\n", count=1, flags=S)

P.replace(C,
"- **P3 `run_family3`:** four routes with shares of V0 (A/B/C/D).",
"- **P3 `run_family3` (and `run_batch`):** a ledger wrapper (`_LedgerHook`) around `wdt_kernel`; the kernel does the settlement. Four routes with shares of V0 (A/B/C/D).")
P.regex(C, r"  - \*\*Route D reset:\*\* a voluntary hard reset every `reset_interval` years, with `death_waiver` skipping the death auction\.\n",
"  - **Route D reset:** `reset_interval` and `death_waiver` are retired (they raise `TypeError`). A reset is a voluntary action in the strategy space (`reset_sens` cycles); death verifies Routes C and D with certainty.\n", count=1, flags=S)
P.replace(C,
"- **P4 verification hazard:** each year a share `lambda` of unverified Route C units",
"- **P4 verification hazard:** `lambda_C` and `lambda_D` are independent. Each year a share `lambda_C` of unverified Route C units")
P.replace(C,
"| SPT | Among gaining strategies, state PV within `state_tol`. |\n| SST | Among gaining strategies, state terminal stake within `state_tol`. |",
"| SPT | Among gaining strategies, state PV within `state_tol`, at each rho in `[rho]` sweep (a sensitivity). |\n| SST | Among gaining strategies, state terminal stake within `state_tol`. Discount-free: the PRIMARY state test (D1c). |")
P.replace(C,
"### Other analyses\n",
"### Other analyses\n"
"- **Added by the refactor:** `_lam_D` couples lambda_D to lambda_C unless `[verification] lambda_D > 0`; lambda_C x lambda_D grid (`_p3_lambda_grid`); V0 sweep over the RATES bands (`_v0_sweep`); Route B archetypes and the breakeven deferral spread (`p6`); JST replay (`_p7_replay`, full loop and contiguous); rho sensitivity; HLC pair from `[val_gen.hlc]` (`_hlc_pair`); the legacy bridge now runs on a JST real series (`_bridge_series`).\n")

P.replace(C,
"- **L3 engine (`run_lines`, `run_cohorts`):** vectorised honest declaration (`alpha = 1`) across lines. A line is a bracket by tier by death-phase, weighted by population share. Yearly mechanics:",
"- **L3 engine (`run_lines`, `run_cohorts`):** vectorised honest declaration (`alpha = 1`) across lines, settled through `wdt_kernel`. `_route_plan` gives each cell's A/B/C/D shares (archetype mixture by launch wealth, a blend, or one archetype), the Route B mode, `r_def`, income cap and income ratio; `_verification` gives lambda_C, lambda_D and death verification (pass-through: honest lines, so they bite only with `verify_down = reset` in price-fall years). Both are built once per scenario. A line is a bracket by tier by death-phase, weighted by population share. The fund counts settled cash only: a Route B lien and an accrued Route D liability are receivables (`lien_out`, `accr_d_out`). Yearly mechanics:")
P.replace(C,
"- **L5 sweep:** every valid (country, start, index mode) window, with stride and country filters.",
"- **L5 sweep:** every JST loop window (`wdt_jst.loop_windows`, T = 100; wrap flagged, `contiguous` reported separately) for each index mode, with stride and country filters. Bootstrap block length is `block_years` = 100.")
P.replace(C,
"4. If you touch `wdt_core`, the TOML or anything that can move `N_fill`, re-run everything downstream.",
"4. If you touch `wdt_core`, `wdt_kernel`, the TOML or the JST basis, re-run everything downstream. After a RATES run, refresh `[val_gen.hlc]` with `python test/print_hlc_calibration.py --write`, then re-run `valgen_core.py` (HLC pair).\n"
"5. Tests (Model/test): `kernel_test.py`, `bridge_test.py`, `rates_test.py`, `test_valgen_pairs.py`, `test_hlc_drift.py`; `diff_json.py` compares two JSON outputs.")
P.run()
