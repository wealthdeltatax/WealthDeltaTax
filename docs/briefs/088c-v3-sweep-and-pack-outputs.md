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
- **Done:**
- **Next:**
- **Decisions:**
- **Gotchas:**
- **Resume:**
- **Not run:**
- **State:** ready; not started
<!-- progress:end -->
