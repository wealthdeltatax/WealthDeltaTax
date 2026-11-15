I read the files you attached and did not run anything, so "done" below means the code is there and matches the plan. I didn't see the test files (`kernel_test.py`, `test_valgen_pairs.py`) or any downstream scripts.

## Recap

### Done

| Plan item | State |
|:--|:--|
| D1b, JST loader with loop (1.1) | `wdt_jst.py` is wired into `rates_core` (`loop_windows`, `usable_years`) and into valgen's replay. |
| D1, D1a, real basis (1.2) | `wdt_core.jst_basis` and `with_val_basis` work, and the TOML sets `basis = "jst"`. valgen derives `g_real` and `index_rate` from JST. |
| D1c, ρ sweep | The `[rho]` block exists. SST is the primary state test and SPT is reported by ρ (`spt_by_rho`). |
| D2, gain ladder as baseline | `[rates.defaults]` now uses `gain_ladder` with `wmin_house_ratio = 1`. `[rate]` and the `[sweep]` canon rate values are retired. |
| New TOML blocks (1.3) | `[archetypes.*]`, `[verification]`, `[route_b]`, `[income]` and `[rho]` are all in. |
| D4a, D4b, Route B in valgen | `run_family3` has sale, lien and income modes. `_p6_validate` includes hand-case checks. |
| D4c, breakeven spread | `_p6_breakeven_spread` solves it per archetype. |
| Death verifies C (valgen side) | `death_verify` is in `run_family3`. |
| Archetype runs in valgen | `_p6_archetypes` runs all five archetypes under sale, lien and income. |
| D5, D7, D1b in RATES | `ratio_mirror` refunds were already in. T = 100 with the wrap loop, and `headline_contiguous` are in. |
| Route B in RATES | `run_lines` handles lien and income. The fund counts settled cash and the receivable is reported separately (D4d). |
| RATES outputs 1, 2, 3, 6 | T26 and F26 (effective windows), T27 and F27 (decade relief), T28–T30 and F28–F30 (Route B). |
| D12 kernel | `wdt_kernel.py` exists and implements the D6 rules. |
| D11 inventory | `D11_retirement_inventory.md` is written. The rest waits on the downstream scripts. |

### Not done

| Item | Gap |
|:--|:--|
| D12 | The kernel is not wired into either core. There are now three engines: `run_family3`, RATES `run_lines` and the kernel. The Route B logic is duplicated in `rates_core`, which is the divergence risk the plan named. |
| D9 bridge test | No file exists. `kernel_test.py` covers kernel against valgen only, and nothing compares RATES against valgen. |
| D6 in valgen | `reset_interval = 10` and `death_waiver` are still live in the TOML and used throughout. Headline runs still use a scheduled Route D reset, which contradicts the plan. |
| D6 (hazards) | `_p5_opts` ties `verify_hazard_D` to the single `lam`, so λ_C and λ_D are not independent. `lambda_sweep` in `[verification]` is not used by valgen. |
| D6 (strategies) | Voluntary reset is not a strategy action. `pre_reset_deviation` and `reset_gaming` still depend on the clock. |
| Phase 2.4 | The strategy library is not revised, and there are no Route B strategies. |
| Phase 2.5 | The V0 sweep across the RATES bands is missing. |
| Phase 2.6 (HSC) | HSC is still the tautological version. The honest-error-plus-shock variant is missing. |
| D1d, Phase 2.7 | The HLC pair (average payer and top 0.1%) is missing. `_conventional_rate` still calibrates only to the honest WDT. |
| Phase 2.8 | The VAL table and figure rebuild is untouched. `5_6` and `5_7` still read `p3_reset_sensitivity` (RIS). The replay, archetype, ρ and breakeven outputs have no tables or figures, and `[names.val]` has no entries for them. |
| D4 and Phase 3.1 | RATES only has a Route B share by wealth. It has no A, C or D routes, no λ or death verification, and no archetype mixture by band. |
| RATES output 4 | The archetype sweep is missing. |
| RATES output 2 (partial) | Cumulative income paid is not reported. T30 shows wealth only, and the plan said to report income paid separately. |
| D11 | Nothing is deleted. `load_params` still hard-reads `[swf]`, `[budget]`, `[returns]`, `[tcm]`, `[[tiers]]` and `[[brackets]]`, and runs the legacy SSM on every load. valgen `_bridge` still uses `p['returns']`, and `_validate` and `meta` still use `N_fill` and `scenario_start_year`. |
| D8, D10 | Both correctly wait on the new runs. |

### Smaller drift

- **Duplicate loaders:** there are two JST loaders (`rates_core.load_jst` and `wdt_jst.load_jst`). `rates_core.valid_windows` is now dead.
- **Duplicate real-return code:** real return and `index_rate` are computed in two places (`wdt_jst` and `rates_core.panel`). Add a test that they agree.
- **Stale docstrings:**
  - The valgen docstring stops at P5, but P6 and P7 exist.
  - The `rates_core` docstring doesn't mention Route B or the loop.
  - The `8_2` header lists only tables 1–19.
  - `WDT_Code_Reference.md` is out of date.
  - TOML comments are stale: `[meta]` still says v7, `[synthetic_scenario]` says 2% against a value of 0.07, the `[tcm]` note, and `index_wmin` still cites `budget_growth`.
- **Hardcodes in presentation:**
  - Table 20's caption hardcodes `fmt_pct0(0.01)` for `c_ref`.
  - Figures 13, 18 and 19 use inline `figsize` instead of `wdt_style` constants.
- **Bootstrap:** `block_years = 100` against start years spanning about 150 gives only a handful of blocks per country. The `n_eff` figures will be very noisy. This is by design (plan risk 8), but report it prominently.

## Parallel tasks

The tasks below don't intersect on files. Each stream owns its files outright. TOML edits are split by section, with each stream editing only the sections it owns.

**Wave 1 (all start now)**

1. **S1: valgen engine (`valgen_core.py` only).WIP**
   - Rebuild `run_family3` as a ledger wrapper over `wdt_kernel`, which retires `reset_interval` and `death_waiver`.
   - Add independent λ_C and λ_D, voluntary reset as a strategy action, Route B strategies, the V0 sweep across the bands, and the HSC variant.
   - Re-point `_bridge` at a JST series and drop `N_fill` and `scenario_start_year` from `meta` and `_validate`.
   - Owns the `[val_gen]` and `[verification]` sections of the TOML.
   - Done when: `valgen_core.py` runs clean with no live reader of `reset_interval` or `death_waiver`.
   - Leave HLC for last. It needs S2's JSON for the burdens and should read it through `wc.load_json`, not import `rates_core`.
2. **S2: RATES engine (`rates_core.py` only). WIP**
   - Replace the inline `run_lines` with a kernel call.
   - Add A, B, C and D route shares by band from the archetype mixture, the archetype sweep, cumulative income paid, and λ pass-through.
   - Remove `valid_windows` and the duplicate `load_jst`.
   - Owns the `[rates.*]`, `[route_b]` and `[income]` sections of the TOML.
   - Done when: the existing scenarios reproduce current numbers with `route_b_mode = "sale"`.
3. **S3: kernel and bridge (`wdt_kernel.py`, `kernel_test.py`, new `bridge_test.py`). DONE**
   - Write the D9 test now against the two engines that exist: a RATES line at α = 1 versus `run_family3`, across all five archetypes and both Route B modes.
   - Expect cap differences, since RATES treats the non-B share as in-kind units while valgen settles A and D in cash with a pooled envelope.
   - The test output tells S1 and S2 what to align.
   - S3 is the only stream that edits the kernel. S1 and S2 send it bug reports.
4. **S4: RATES presentation (`8_2_RATES_tables.py`, `8_3_RATES_charts.py`). DONE**
   - Add the archetype sweep table and figure, the income-paid column, and a tenth-year coverage row if needed.
   - Fix the header docstrings, the `c_ref` hardcode and the inline `figsize` values.
   - Work against a JSON contract S2 agrees first, and stub with `_need()` until the JSON exists.
5. **S5: VAL presentation (`5_6_VALGEN_tables.py`, `5_7_VALGEN_charts.py`).WIP**
   - Add tables and figures for the replay (full loop and contiguous), archetypes, the ρ and SPT sensitivity, and the breakeven spread, then the HLC pair.
   - Replace RIS with the λ and voluntary-reset sensitivity.
   - Owns the `[names.val]` section of the TOML.
   - The contract with S1 is the `data['replay']`, `data['p6']` and `data['rho']` keys, which already exist.
6. **S6: downstream D11 audit (read-only).**
   - Grep WFR, VAL.A, VAL.S, SWEEPS, RATES.S, `module5_sweeps.py`, `print_val_real_inputs.py` and `rates_test.py` for the retiring keys, using the regex in the inventory's §6.
   - Update `D11_retirement_inventory.md` with LIVE or DEAD for each reader.
   - No code edits, so it can't conflict with anything.
7. **S7: docs.**
   - Update `WDT_Code_Reference.md` (Route B, the loop, `wdt_jst`, the kernel, archetypes, T = 100) and the status line in `WDT_Refactor_Plan.md`.
   - Update the skill's drift register.
   - Docstrings stay with the code owners.

**Wave 2 (serial, after S1, S2 and S6 finish)**

8. **D11 deletion (`wdt_core.py`, the legacy TOML blocks).**
   - Make the retiring blocks optional in `load_params`, drop the SSM call, `N_fill`, `p['N']` and `p['tcm']`, and require `g_real`, `index_rate` and `rate_scenario`.
   - Re-run `kernel_test.py` and valgen, delete the TOML blocks, then remove the dead code.
   - Tag `legacy-v7` first (Phase 0).
   - It has to come after S1 because `_bridge` and `_validate` read the legacy keys today.

**Wave 3**

9. Run `bridge_test.py`, `valgen_core.py` and `rates_core.py`, then the tables and charts. Then do D8 (VAL headline claims) and D10 (paper restatements).

## Decisions I need from you

- **Single-life block:** do we keep `simulate`, `run_pair` and the related functions in `wdt_core` until D9 passes, as the inventory recommends, or freeze the bridge numbers as golden values now?
- **Naming:** does `p['g']` survive, or does it become `g_real`?
- **Plan open items 1–3:** sweep the deferral spread beyond the breakeven? What order to rebuild the VAL tables? Is the 50% and 75% income-cap sweep enough?
- **HLC burden source:** valgen reads RATES' burden from `rates_data.json`, which stays inside the layering since only JSON crosses. Do you want that, or a TOML-held calibration for HLC instead?

If you say go, I can launch S1–S7 as parallel agents.