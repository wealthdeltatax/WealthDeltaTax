# 087: Supporting outputs into Samples

- **Status:** ready
- **Author/date:** K. Ogata with the guru, 2026-11-20
- **Depends on:** 084c
- **Read:** `docs/archive/briefs/055c-v3-10-range-runner.md` (gotcha 4); `docs/archive/briefs/054c-v3-9-supporting-metrics.md` (progress block, gotchas); `model_v3/runner/out_support.py` (the stub); `model_v3/core/support.py`; `docs/model-v3/outputs.yml` entries O7, OD1, OW1, OW2, OW3, OM1, OS1; `docs/model-v3/metrics.md` rows M7, M7c, M7d (M7e is dropped), M9, M13, M14, M15a, M15b, S1.

## Goal
The seven supporting outputs exist in Samples: O7 (M7 tolerant zone), OD1 (M7c and M7d by alpha grid), OW1 (M13), OW2 (M14), OW3 (M15a with M15b on the transition horizon only), OM1 (M1, X, M9), OS1 (S1 by quantity; a switch, off in every headline cell).

## Decisions (author, 2026-11-20)
M7e is dropped (081g): no declared-alpha distribution and no `modal_alpha`. OD1 keeps `lines: [M7c, M7d]`. `core/support.py` still names M7e until the next time it is edited; do not edit it here, report each remaining mention.

## Design
Fill the stub `model_v3/runner/out_support.py` that 084c created. It exposes `NAME`, `per_path(raw, again)` (per-path arrays for one chunk of paths: the dict's leaves are 1-D arrays over paths, the structure is in its keys; `again(spec_override)` returns the `raw` of the same paths under a changed schedule, cached) and `cells(e)` (turns the concatenated per-path dict `e` into `{output id: {(horizon, by, line): array}}`, with `by` a sorted tuple of `(name, value)` as `architecture.md` 2.9 says). The `by` vocabularies and `lines` are those of each id's entry in `outputs.yml`; the horizons are the manifest's (`single` is one cell). Never edit `runner.py`, `groups.py` or `evaluate`.

For each id, map its metric to the `core/support.py` function that produces it and write the map in the change report. **If a metric the manifest names is not produced by the core module, or an input the core takes from the caller has no register row or pack field, do not invent a value: stop and report to the guru** (the 054c and 055c rule). Inputs the caller supplies are read from the register and pack as 055c does (`ctx`, `theta`); name each row id in the report.

`support.py` takes inputs from the caller (054c gotchas): consumption spend and its rate (I-D14 rows), the second asset's returns (`returns.csv` `housing_tr`, `bond_tr`), embedded-gain bands (I-T4e), the gains-tax realisation rate (I-T5e and I-T5f), and the horizon rows. The 055c guru note already confirmed this map; name each row id in the report and stop if one has none.

**Early check.** O7's tolerant zone for the central schedule must contain alpha 1.0 (a truthful declaration is never penalised); report the bounds.

**Shared interfaces, fixed before any stage starts** (a build brief never edits them; a mismatch is a question to the guru): the output file shape is `schema wdt-outputs/1` as `pipeline/validate_outputs.py` checks it and `docs/restructure/site/hooks.md` section 3; the Samples contract is `architecture.md` 2.9; the id lists are `docs/model-v3/outputs.yml` and the module-to-id table of `architecture.md` 2.10; the layers and import rules are `architecture.md` 5.1; the group interface is the one 084c fixes (`model_v3/runner/groups.py`).

## Touches
`model_v3/runner/out_support.py`, `tests/model_v3/test_out_support.py`, this brief's progress block, `docs/agents/friction-log.md`.

## Acceptance criteria
- Each of the seven ids returns one cell per schedule, horizon and `by` value in the manifest (OW3: M15b on `transition` only, as `line_horizons` says).
- The early check bounds are in the report.
- `out_support.py` at most 150 lines and its tests at most 80; `pytest tests/model_v3 -q` passes.
- `git diff --stat` limited to Touches.

## Checks to run
`pytest tests/model_v3 -q`.

## Out of scope
Any other group; `runner.py`; `core/support.py`; M7e.

## Guru rulings (2026-11-20, after the stop; manifest A12, brief 092c, register 091g)
Wait for 092c (`per_path(raw, env, again)`, `env.ctx`, `env.theta`, `env.pack`, `env.rng(name)`) before writing code. Rulings on the five blockers:
1. **VAT (M9, OM1):** `rate_spend` is the register row **I-T3q** (VAT standard rate, 20%, divide by 100); `spend` is the leaver's consumption (consumption share I-D14c times wealth, as the core defines it).
2. **Reference holder (M7, O7, OD1):** `V0` is the register row **I-D14h** (£20m; `support.declaration_runs` takes pounds m).
3. **Second asset (M14, OW2):** joint bootstrap of whole years of `housing_tr` and `bond_tr` from `returns.csv` (the same year for both), drawn with `env.rng('support')`; say in the report how many years and the resulting means.
4. **Envelope record (M15a, OW3):** the group reruns the kernel itself with per-year capture (about 40 lines), inside its budget; `burden.py` is not edited.
5. **S1, OS1:** call `core_run` with a changed `ctx` (`dataclasses.replace`) and the same paths and `theta`; take m2 and payer_count from `raw.base`.
Certainty-equivalent outputs (OW1, OW2): your decision on chunks stands. If any of this does not hold when you read the code, stop and say which line.

## Guru rulings 2 (2026-11-20, after your stop)
1. **OS1 (ruling 5 replaced).** You are right: `core_run` is L4 and `again` only overrides the spec. Do not duplicate the core rerun. Make this narrow edit to `runner.py`: `core_run(..., tweak=None)` applies `b = tweak(b)` to the shaped base, and `again(override=None, full=False, tweak=None)` passes it on, cached on (spec, full, tweak). Then OS1 is `again({}, tweak=lambda b: replace(b, wealth=sp.capitalise(b.wealth, share, uplift, on=True)))` against `raw`, with the property share from the pack, the uplift from I-D10b (divide by 100), the threshold untouched, and `s1_effect` on m1, m2 and `payer_count`. `runner.py`, `tests/model_v3/test_runner.py` and `tests/model_v3/test_groups.py` (a test for `tweak`) are in Touches for this edit only; keep `runner.py` at most 360 lines and the 084c and 092c digests unchanged (the default is no tweak).
2. **`test_groups.py` clause:** take `main`'s version on rebase (it now guards groups with ids); drop your edit of that line.
3. **D4_5 band with no payer:** keep nan, as O2 and O2d do. The final run's policy on non-finite cells is 057c's; noted there.
4. Everything else in your report stands (O7 cell, the 16 OD1 cells, OW3 `entry_year`, the chunk-repeated CE values).

## Open questions
None.

## Implementation notes
<!-- progress:start -->
- **Done:** six of seven ids in Samples: O7, OD1, OW1, OW2, OW3, OM1 (`out_support.py` 113 lines, `test_out_support.py` 62). Cell counts: O7 1, OD1 16, OW1 20, OW2 9, OW3 20 (M15a 5 bands x 3 horizons, M15b transition only), OM1 9. `pytest tests/model_v3 -q`: 212 passed.
- **Next:** OS1 (S1), needs the guru (see Gotchas). Then add `OS1` to `IDS`/`cells` and the brief can merge.
- **Decisions:** O7 cell = [1.0, mean zone lo, mean zone hi]; OD1/others with p10_mean_p90 keep the per-path array, point_and_range ids = [mean, P10, P90]; OD1 = [mean, P10, P90] over paths; OW3 `entry_year` = 'value_per_cohort'; M15b N = I-D14e years; envelope rerun has one death phase (deaths every G years); X uses household income I-D9d per leaver and spend = I-D14c x mean payer wealth; CE values are one per chunk, repeated over its paths; a band with no payer at launch (D4_5, wealth under w_min) is nan, as in O2 (assemble treats non-finite as an error in a final run: guru to confirm nan vs 0).
- **Gotchas:** (1) Ruling 5 cannot be followed: `core_run` lives in `runner.py` (L4), `out_support` is L3.5 and may not import it (R4, no lazy imports); `again` only overrides the spec, not the base. Options: a ~12-line duplicate core rerun in the group (needs line budget), or a core-run hook in the group interface. OS1 left out of `IDS`. (2) `test_groups.py` asserted every group's `per_path(None, None, None) == {}`; now guarded for groups with ids (outside Touches). (3) `bd._groups` is private to burden; used for the same band masks.
- **Resume:** branch `brief/087-support-outputs`; add OS1 after the ruling.
- **Not run:** the named S_central (sweep) schedule; used the grid-centre spec (tau_0 .04, tau_m .9, k_ln 1, ratio .5), synthetic paths, 1,000 paths.
- **State:** blocked on OS1; six ids done
<!-- progress:end -->

### Early-check bounds and bootstrap (grid-centre spec, 1,000 paths)
- O7 tolerant zone [0.860, 1.147] contains alpha 1.0 (OD1 M7c at alpha 1.0 is 0).
- Second asset: 117 usable consecutive years of `housing_tr` and `bond_tr` in the GBR returns table; drawn jointly with `env.rng('support')`; real arithmetic means 5.4% (housing) and 1.8% (bond) on a 20 x 1,000 draw.
- OM1 on synthetic paths: X about 2.0 per cent of GDP-window, M9 = M1 - X exactly.
- M7e mentions left in `core/support.py` (not edited): module docstring line 7 ("M7c to M7e"), line 35, and `modal_alpha` (lines 77-78, "supporting.md M-3").

Change report
- Task: brief 087c, v3 support outputs
- Files changed: `model_v3/runner/out_support.py` (six ids filled); `tests/model_v3/test_out_support.py` (new); `tests/model_v3/test_groups.py` (empty-group assertion guarded, outside Touches); this brief; `docs/agents/friction-log.md`
- What is different now: Samples carries O7, OD1, OW1, OW2, OW3, OM1 per schedule/horizon/by.
- New or changed interfaces: none (group interface of 092c unchanged)
- Acceptance criteria: one cell per vocabulary value met for six ids; OS1 not met (layer rule); O7 zone contains 1.0 met; line budgets met (113 <= 150, 62 <= 80); `pytest tests/model_v3 -q` 212 passed; `git diff --stat` within Touches except test_groups.py
- Deviations from the brief: ruling 5 not followed (impossible under R4); OS1 omitted
- Risks / follow-ups: guru to rule on OS1 route and on nan for payer-less bands; U-shape of assemble on non-finite values
- Instruction friction: one entry added to the friction log
- Verification: full model_v3 suite; early-check measured; named S_central not run
- Overview sections likely needing an update: none
- Commit / branch: see git log, `brief/087-support-outputs` (not merged: NEEDS THE GURU)
