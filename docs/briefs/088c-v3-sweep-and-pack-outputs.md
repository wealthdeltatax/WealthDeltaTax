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

## Open questions
None.

## Implementation notes
<!-- progress:start -->
- **Done:** read the stub, `groups.py`, `runner.samples`, `Level2`/`TornadoRow` (`interface.py`), `out/assemble.py`, the validator, `pack.dh1a`/`dh1b` and the four manifest entries. No code written.
- **Next:** the guru answers the three questions below (one manifest amendment and one group-interface change, both outside this brief's Touches); then build.
- **Decisions:** none taken: each answer changes a shared interface.
- **Gotchas:** (1) **DH1a and DH1b cannot be carried as the manifest stands.** Their entries have no `by`, no `horizons` and no `once_not_per_schedule`, so `assemble._expected` wants 3 schedules x 3 horizons = 9 cells of one number each, while `pk.dh1a` returns several series with their history and `pk.dh1b` every receipts line and group; nothing says which number goes in a cell. And `runner.samples` puts the schedule in front of every cell a group returns, so a schedule-free cell (key schedule `None`) cannot come out of a group. (2) **OT1 has no home.** The manifest wants cells by input x headline x schedule (a `schedule` dimension on top of the top-level schedules, default three horizons: 4,320 cells), while `interface.Level2` and `level2.<id>` hold one list of `TornadoRow(input, low_effect, high_effect)` per output id, with no headline, schedule or horizon; `sweeps.tornado` returns rows per (schedule, headline, horizon). (3) **O1e and OT1 are sweeps, not per-path cells**: they need the evaluator `ev` and the level 2 draws, which `per_path(raw, again)` and `cells(e)` (one schedule, one block of paths) do not see. And S_low, S_central and S_high do not exist until the author rules on the feasibility rule (083c: no feasible point; 089c), so there are no named schedules to run them on.
- **Resume:** proposed answers (guru to confirm or change): (a) amend the manifest: DH1a `once_not_per_schedule: true`, `horizons: [single]`, `by: {series: [...]}` (the latest value as point, its low and high as range); DH1b the same with `by: {line: [...]}` (and the groups as extra values of the same dimension), and let `samples` accept a schedule-free cell (a key with schedule `None`) from a group. (b) OT1: cells by input x headline for each named schedule, one `single` horizon (M1, M2 and M4a at the short window, M3 single), array [0, low swing, high swing] (the central value is the zero of the swing), drop `by.schedule` from the manifest as redundant; the `level2` object then carries only the P10 to P90 of each headline's level 1 mean (a tornado list for O1, O2, O4a and O3 is optional). (c) `out_sweeps` exposes two plain functions, `o1e(ev, specs, draws)` and `ot1(ev, specs, rows, read)`, returning Samples cells, called by the run script (V3-12) next to `level2`; `per_path` and `cells` stay empty for the group, and the tests run on the 27 grid points with schedule labels given, until 089c names the schedules.
- **Not run:** everything; no code or test written, no check run.
- **State:** blocked; NEEDS THE GURU (questions above)
<!-- progress:end -->
