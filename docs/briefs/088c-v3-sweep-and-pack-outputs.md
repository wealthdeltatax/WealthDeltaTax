# 088: Sweep and pack outputs into Samples (O1e, OT1, DH1a, DH1b)

- **Status:** ready
- **Author/date:** K. Ogata with the guru, 2026-11-20
- **Depends on:** 084c
- **Read:** `docs/archive/briefs/055c-v3-10-range-runner.md` (gotchas 3, 4 and 7); `model_v3/runner/out_sweeps.py` (the stub); `model_v3/runner/sweeps.py` (`tornado`, `breakeven`, `breakeven_return`); `model_v3/runner/runner.py` `Level2`; `model_v3/core/pack.py` (the household data facts); `docs/model-v3/outputs.yml` entries O1e, OT1, DH1a, DH1b; `docs/model-v3/architecture.md` 2.9.

## Goal
The four outputs that come from the sweeps and the pack exist in Samples or Level2: O1e (break-even return, point and range), OT1 (the tornado, level 2 rows per tier 1 input), DH1a and DH1b (household data facts from the pack).

## Decisions (author, 2026-11-20)
OF1 (feasibility map) and CK1 wait for the author's ruling on the feasibility rule after the 083c diagnostic: brief 089c. Do not shape them here.

## Design
This group differs from 085c to 087c: O1e and OT1 are level 2 and sweep results, not per-path cells, and DH1a and DH1b are not per schedule. `out_sweeps.py` exposes the same four names (`NAME`, `IDS`, `per_path`, `cells`) but `per_path` returns `{}` for the two level 2 ids and `cells` for them is called from `Level2` assembly: say in the report how `Level2` carries them (the contract is `architecture.md` 2.9; if it does not fit, stop and report to the guru). DH1a and DH1b read the pack only (no kernel run); their summary forms are the manifest's (`point_and_range`, `point`).

**Shared interfaces, fixed before any stage starts** (a build brief never edits them; a mismatch is a question to the guru): the output file shape is `schema wdt-outputs/1` as `pipeline/validate_outputs.py` checks it and `docs/restructure/site/hooks.md` section 3; the Samples contract is `architecture.md` 2.9; the id lists are `docs/model-v3/outputs.yml` and the module-to-id table of `architecture.md` 2.10; the layers and import rules are `architecture.md` 5.1; the group interface is the one 084c fixes (`model_v3/runner/groups.py`).

## Touches
`model_v3/runner/out_sweeps.py`, `tests/model_v3/test_out_sweeps.py`, this brief's progress block, `docs/agents/friction-log.md`.

## Acceptance criteria
- O1e has the manifest's `single` horizon cell per schedule with its range from the draws; OT1 has a low and a high row for each tier 1 input in the manifest's `by.input` list (the 40 register ids; 35 swing exactly 0 and are listed as zero, not dropped).
- DH1a and DH1b match the pack's values (a test reads the pack file).
- `out_sweeps.py` at most 150 lines and its tests at most 80; `pytest tests/model_v3 -q` passes.
- `git diff --stat` limited to Touches.

## Checks to run
`pytest tests/model_v3 -q`.

## Out of scope
OF1, CK1 (089c); `runner.py`; the other groups.

## Guru rulings (2026-11-20, after the stop; manifest A12, brief 092c)
Your three proposed answers are accepted, with the manifest edit done (A12): DH1a is `by: {series: [wid_top1, wid_top10]}`, DH1b `by: {line: [the 16 pack lines]}`, both `once_not_per_schedule`, `horizons: [single]` (DH1a without wealth to GDP, DH1b without groups); OT1 is cells by input and headline per named schedule, point 0 with lo and hi the swings, `horizons: [single]`, `by.schedule` gone.
1. **DH1a, DH1b:** a `static(env)` function in `out_sweeps` (092c adds the hook; schedule `None` cells). Read the pack with `env.pack`.
2. **O1e and OT1:** plain functions `o1e(ev, specs, draws)` and `ot1(ev, specs, rows, read)` returning cells as `samples` does, called by the run script (057c); `per_path` and `cells` stay empty for the sweeps.
3. **Schedules:** test on the 27 grid points with schedule labels given, until 089c names S_low, S_central and S_high.
Wait for 092c before the code.

## Open questions
None.

## Implementation notes
<!-- progress:start -->
- **Done:** `out_sweeps.py` (51 lines): `IDS=('DH1a','DH1b','O1e','OT1')`; `static(env)` (DH1a, DH1b from `env.pack`); `o1e(roots)`, `ot1(rows)`; `per_path`, `cells` empty. `test_out_sweeps.py` (41 lines).
- **Next:** 057c run script calls `sweeps.breakeven_return` and `sweeps.tornado` on the named schedules, passes the results to `o1e` and `ot1`, and merges the cells into Samples.
- **Decisions:** `o1e` and `ot1` format sweep results instead of running the sweeps (layer rule R4: a group cannot import `sweeps`); OT1 reads M1, M2, M4a at the short window and M3 at `single`; the O1e range is the p10 and p90 of the draw roots; `static` returns only ids in `Ctx.once`.
- **Gotchas:** the DH1a rows of the GBR pack have no `low` or `high` (blank), so `lo` and `hi` are the point itself (zero-width range); `tests/model_v3/test_runner.py::ctx` passes no `once`, so a static id is only emitted when the context has it.
- **Resume:** none.
- **Not run:** nothing; the 27 grid points stand in for S_low, S_central, S_high until 089c.
- **State:** done; merged

Change report
- Task: brief 088c, sweep and pack outputs into Samples (O1e, OT1, DH1a, DH1b)
- Files changed: `model_v3/runner/out_sweeps.py` (the group: static DH1a and DH1b, `o1e`, `ot1`); `tests/model_v3/test_out_sweeps.py` (new); this brief; `docs/agents/friction-log.md` (one entry)
- What is different now: the four ids have producers. DH1a and DH1b come out of `samples` as schedule-None cells through `static`; O1e and OT1 come from two formatting functions the run script calls, keyed (schedule, 'single', by, None) as Samples are. Their keys equal `assemble._expected` (O1e 3 cells, OT1 480 = 3 x 40 x 4, DH1a 2, DH1b 16).
- New or changed interfaces: `out_sweeps.IDS`, `static(env)`, `o1e(roots)` from `sweeps.breakeven_return`, `ot1(rows)` from `sweeps.tornado`. No change to runner.py or sweeps.py.
- Acceptance criteria: O1e single cell per schedule with range from the draws: met (test, 27 schedules). OT1 low and high for the 40 inputs, unread ones kept as zero: met (480 cells per schedule, 27 x 40 x 4 in the test, all but the one read input zero). DH1a, DH1b equal the pack: met (test reads the pack). Lines: `out_sweeps.py` 51 of 150, tests 41 of 80: met. `pytest tests/model_v3 -q`: 209 passed. Diff inside Touches: met.
- Deviations from the brief: (1) the ruled signatures `o1e(ev, specs, draws)` and `ot1(ev, specs, rows, read)` became `o1e(roots)` and `ot1(rows)`: R4 forbids a group importing `runner/sweeps`, and a lazy import would still be an edge; the run script calls the sweeps. (2) `static` filters on `Ctx.once`, because the shared test fixture builds a context without `once` and `samples` raises on a static id outside it; `test_runner.py` is outside Touches. (3) DH1a `lo` and `hi` fall back to the point where the pack has no range (GBR has none): a zero-width range, not an invented one.
- Risks / follow-ups: the guru may want the pack to carry a real range for the top shares, or DH1a changed to `point`. 057c must pass `once` to `runner.context` or DH1a and DH1b will be missing (final assembly would raise).
- Instruction friction: one entry added (the ruled signature conflicts with R4).
- Verification: `pytest tests/model_v3 -q` 209 passed; `python pipeline/run_suites.py` 10 of 10 suites passed.
- Overview sections likely needing an update: none
- Commit / branch: see git log, branch `brief/088b-sweep-pack-outputs`; brief 088 merged, ready to retire
<!-- progress:end -->
