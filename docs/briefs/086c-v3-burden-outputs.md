# 086: Burden and savings outputs into Samples

- **Status:** ready
- **Author/date:** K. Ogata with the guru, 2026-11-20
- **Depends on:** 084c
- **Read:** `docs/archive/briefs/055c-v3-10-range-runner.md` (gotcha 4); `model_v3/runner/out_burden.py` (the stub); `model_v3/core/burden.py` (module note, `line_flows`, `m2`, `m4`, `m3`, incidence); `docs/model-v3/outputs.yml` entries O2d, O2b, O2c, O4b, O5, O6, O8, OL1, OH1b, OH1b2, OH1c, DH1c; `docs/model-v3/metrics.md` rows M2b to M6, M8, M11, M12, M4c; `docs/model-v3/metrics.md` "Closed on 2026-11-20" (what 053c did not build).

## Goal
The twelve burden-side outputs exist in Samples: O2d (M2 including settlement at death), O2b and O2c (M2 below W_min cutoffs), O4b, O5, O6, O8, OL1 (M4c by reference worker), OH1b (M3 by wealth band), OH1b2 (M11), OH1c (M12 by cause), DH1c (the non-payers' bill by income decile, a data fact).

## Decisions (author, 2026-11-20)
053c's limits stand: OH1b all-tax line, M8 non-payer saving, M2b and M2c below W_min and thresholds on line means were not built; if the core cannot produce one of these, report it as a limit of the first run (it goes to `metrics.md` "Closed on 2026-11-20" as a limit), do not build it here. M5 has no with-death line (open for the author, 079g): do not add one. O2d needs the death flows that `evaluate` zeroes when `full=False`: read them from `again`'s `full=True` run or from the line flows, whichever the core supports, and say which.

## Design
Fill the stub `model_v3/runner/out_burden.py` that 084c created. It exposes `NAME`, `per_path(raw, again)` (per-path arrays for one chunk of paths: the dict's leaves are 1-D arrays over paths, the structure is in its keys; `again(spec_override)` returns the `raw` of the same paths under a changed schedule, cached) and `cells(e)` (turns the concatenated per-path dict `e` into `{output id: {(horizon, by, line): array}}`, with `by` a sorted tuple of `(name, value)` as `architecture.md` 2.9 says). The `by` vocabularies and `lines` are those of each id's entry in `outputs.yml`; the horizons are the manifest's (`single` is one cell). Never edit `runner.py`, `groups.py` or `evaluate`.

For each id, map its metric to the `core/burden.py` function that produces it and write the map in the change report. **If a metric the manifest names is not produced by the core module, or an input the core takes from the caller has no register row or pack field, do not invent a value: stop and report to the guru** (the 054c and 055c rule). Inputs the caller supplies are read from the register and pack as 055c does (`ctx`, `theta`); name each row id in the report.

**Early check.** O2d minus O2 (in life) over the short window must reproduce 053c's pattern: death flows are the larger part of M2 including death (22.2% a year with them, 2.8% without at 053c's central run). Report both numbers; stop and report if they differ by more than a tenth.

**Shared interfaces, fixed before any stage starts** (a build brief never edits them; a mismatch is a question to the guru): the output file shape is `schema wdt-outputs/1` as `pipeline/validate_outputs.py` checks it and `docs/restructure/site/hooks.md` section 3; the Samples contract is `architecture.md` 2.9; the id lists are `docs/model-v3/outputs.yml` and the module-to-id table of `architecture.md` 2.10; the layers and import rules are `architecture.md` 5.1; the group interface is the one 084c fixes (`model_v3/runner/groups.py`).

## Touches
`model_v3/runner/out_burden.py`, `tests/model_v3/test_out_burden.py`, this brief's progress block, `docs/agents/friction-log.md`.

## Acceptance criteria
- Each built id returns one cell per schedule, horizon and `by` value in the manifest; every id not built is listed with the reason (a stated limit of the first run).
- The early check numbers are in the report.
- `out_burden.py` at most 150 lines and its tests at most 80; `pytest tests/model_v3 -q` passes.
- `git diff --stat` limited to Touches.

## Checks to run
`pytest tests/model_v3 -q`.

## Out of scope
Any other group; `runner.py`; building the 053c limits.

## Guru rulings (2026-11-20, after the stop; brief 092c)
Your five ids stay. Wait for 092c: the signature becomes `per_path(raw, env, again)` with `env.ctx`, `env.theta`, `env.pack`; rebase onto main after it merges and build O5, O6, O8, OH1b, OH1b2, OH1c and DH1c from `env`. 092c changes the two `test_groups.py` pins you hit; do not edit them. O8 takes M1 in pounds per path from `raw.r` (check against the M1 headline). Note the manifest A12 does not change DH1c (still per schedule and horizon); say in your report if that looks wrong.

## Open questions
None.

## Implementation notes
<!-- progress:start -->
- **Done:** `out_burden.py` (57 lines) builds O2d, O2b, O2c, O4b, OL1 (75 + 15 + 45 + 45 + 33 + 12 cells per schedule: one per horizon and `by`); tests 45 lines, 5 pass. Metric map: O2d = `m2d(raw.fl, lo, hi)` (death flows are in `raw.fl`, so `again` is unused); O2b and O2c = `m2b`/`m2c` shares of payers above each cut-off (burden.py default, all net WDT; the payer mean is not in the manifest); O4b = `m4(raw.r['P5'], hi, raw.inc, bill, income)['M4b']` with bill and income from `raw.base.income_deciles`; OL1 = `m4c` on that. Register and pack rows read: none (all from `Raw`).
- **Early check (200 paths, seed 7, SPEC, short window):** M2 in life 3.00, M2d 23.48 (053c: 2.8 and 22.2); within a tenth. Long: 1.01 and 12.42.
- **Next:** the guru decides the interface question below; then the seven ids.
- **Decisions:** none by me.
- **Gotchas:** (1) **Not built: O5, O6, O8, OH1b, OH1b2, OH1c, DH1c.** `per_path(raw, again)` receives no pack or register and `Raw` holds neither (`ctx`, `theta` stay in `evaluate`), while `m5`, `m6`, `m8` (shares), `m3_today`, `m11`, `m12`, `dh1c` need them. I did not reach into `again`'s closure. Fix is an interface edit (`runner.py` is out of scope): pass `ctx` and `theta` to `per_path`, or put them on `Raw`. (2) 084c's `test_groups.py` fails twice with any group filled: `IDS == ()` for all groups, and the empty-group digest PIN for `burden`. Not in Touches, not edited. (3) O8 also needs the M1 revenue in billions per path (from `raw.r`), not checked. (4) O5 has no with-death line (079g), as the brief says.
- **Resume:** branch `brief/086-work`; after the interface change, add the seven ids to `out_burden.py` (line budget 150: now 57) and tests (budget 80: now 45).
- **Not run:** the full level 2; the seven ids.
- **State:** partly built, NOT merged (needs the guru: interface). `pytest tests/model_v3 -q`: 206 passed, 2 failed (the two 084c tests above).
<!-- progress:end -->
