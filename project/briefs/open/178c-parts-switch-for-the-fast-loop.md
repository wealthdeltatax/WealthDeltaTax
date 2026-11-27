# 178: `--parts` switch, the fast loop

- **Status:** ready; 154c merged 2026-11-27
- **Agent:** 2
- **Needs:** 154c
- **Length:** 1
- **Author/date:** K. Ogata with the guru, 2026-11-26
- **Depends on:** 154c (both change `run.py`; do not edit it in parallel)
- **Read:** `model/model_v3/run.py` (`SIZES`, `NOT_RUN_RUN`, `run_point`, the O1e marker line); `model-specs/acceptance.md` (validation, `--final`); `model/model_v3/out/` validator entry; `results/run-cost/run-cost.md`

## Goal
The author will change variables many times. Most changes need only the level-1 headlines, not the tornado or the O1e roots. Add `--parts` so that loop takes about 3 to 5 minutes, while the full `quick` run stays the 10-minute check.

## Decisions (author, 2026-11-26)
The full `quick` run stays; the fast loop is a subset of it, never a different method.

## Design
1. `--parts` takes a comma list from `level1,map,tornado,o1e`; default is all four, and a default run is byte-identical to today's. Proposed fast loop: `--parts level1,map` (F1, M1 to M4 for the five points).
2. A run with fewer parts writes the same file with a header field `run.parts`; ids that belong to a part not run carry the existing marker word `not_run_this_run` (already used for the O1e range at zero draws). The validator checks only the ids of the requested parts and refuses `--final` with any subset.
3. The output files name the parts in the file name or the header, so a partial file cannot be mistaken for a full one by `accept.sh` or `check_gate.py`; both refuse a partial file.
4. Which ids belong to which part: the agent lists them from the manifest and the callers (`run_point`) and puts the table in the brief's notes before coding. If an id reads two parts, it goes with the later one and the table says so.
5. Timing with `bench.py`: `quick_headlines` and `quick_full`, this machine and one Actions run.

## Touches
`model/model_v3/run.py`, the validator and its tests (`tests/model/model_v3/`, `tests/model/gate/` if the gate reads the header), `tests/model/model_v3/accept.sh` (refuse partial), `model-specs/acceptance.md` (one paragraph), `results/speedup/ledger.md`. The manifest only if the marker word needs an entry; if it does, stop and ask the author (a manifest amendment is theirs to sign off).

## Acceptance criteria
- A default run is byte-identical to the file before the change.
- `--parts level1,map` output validates for the requested ids, carries the marker elsewhere, is refused by `--final`, `accept.sh` and `check_gate.py`.
- Wall time for the fast loop reported on this machine and on Actions, against the 3 to 5 minute target; if over 5, say which part dominates.

## Out of scope
Making any part cheaper (151c, 153c, kernel); changing a number.

## Open questions
For the author: what the fast loop must contain. Default: level-1 headlines and the feasibility map (`level1,map`); say if the tornado must be in it, which costs most of the time saved.

## Implementation notes

**Id-to-part table (agent, 2026-11-27, from `outputs.yml` and `run_point`; written before coding).**

| Part | Ids it produces | What it is |
|---|---|---|
| `map` | `OF1`, `CK1` (still the labelled `pending` entries, 140c/089c, in every run) | `S.feasibility` then `S.choose`: the `named` schedules. Every other part reads `named`, so `map` is a prerequisite. |
| `level1` | the 37 ids that are not `OT1`, `O1e`, `OF1`, `CK1` (`OW1` stays `withheld: legacy_only` at household points) | `R.level1` per grid point (headlines, groups, comparators, M1 to M4) |
| `tornado` | `OT1` | `S.tornado` per grid point, headline-only evaluator |
| `o1e` | `O1e` | `S.breakeven_return` at the first point, `fund_return=market`, and the draws |

No id reads two parts in its output. `OT1` and `O1e` read `named` (from `map`) as an input, not as an output, so they go with the later part, `tornado` and `o1e`.

Decisions taken inside the brief (no manifest change):
- A skipped part's ids are written `{"summary", "cells": [], "not_run": "not_run_this_run"}` (an entry-level marker, like `pending` and `withheld`). The existing marker word is reused; the manifest needs no entry, because the validator, not the manifest, lists entry markers.
- `run.parts` is written only when the list is not the full default, so a default file is byte-identical.
- `map` must be in the list (every other part needs it); a list without it is a usage error.
- The validator checks a partial file for its requested parts only, and refuses `--final` on any file that carries `run.parts`. `accept.sh` step 5 and `check_gate.py` G2 refuse it too.

<!-- progress:start -->
- **Done:** `--parts` implemented; id-to-part table above; validator, `accept.sh` step 5, `check_gate.py` G2 refuse a partial file; tests; `acceptance.md` paragraph; ledger row; timings measured here. Default smoke byte-identical; model_v3 suite 438 passed, gate 17 passed.
- **Next:** author: (1) the fast-loop target is not met (31 min here), see the open question; (2) the Actions timing; (3) merge on request.
- **Resume:** nothing pending in the code.
- **State:** done, not merged
<!-- progress:end -->


### Measurements (this machine: 2 cores, 8 GB, `NPY_DISABLE_CPU_FEATURES=X86_V4`, workers 1; `bench.py` is not merged, so wall time of `run.main`)
- Default run, `--size smoke`: `cmp` byte-identical to the file before the change.
- `--size smoke --parts level1,map`: 404 s (with a second run alongside); validates; `--final`, `accept.sh --check` refuse it; the 39 ids it ran equal the full smoke's cell for cell. `--parts map,tornado,o1e` likewise (4 ids ran, all equal).
- `--size quick --parts level1,map` (five points): **1,875 s (31 min)**, validates (`results/178c-evidence/quick-level1-map-outputs.json`). Full `quick` is about 2,350 s (151c and 154c figures, not re-timed). The fast loop saves about 8 min, not the hoped 5 to 6 times.
- Which part dominates: level 1, about 287 s per point x 5 = 1,435 s; the map is about 319 s (one evaluation grid, 27 points); the tornado is about 73 s per point and O1e about 60 s, so skipping both saves only about 425 s. Estimates, not measured: `level1,map --point median_mid` would be about 10 min (map 319 s, one point 287 s); `--paths 200` on top, about 7 min, with the map then dominant. Nothing here makes a part cheaper (out of scope).
- Actions timing: not run by me; the author's.

```
Change report
- Task: 178c `--parts` switch for the fast loop
- Files changed: model/model_v3/run.py (`--parts`, part gating, `run.parts`, `not_run` entries; still 120 lines); model/tools/validate_outputs.py (`run.parts` check, `not_run` entries, partial never final); model/tools/check_gate.py (G2 refuses `run.parts`); tests/model/model_v3/accept.sh (step 5 refuses `run.parts`); tests/model/model_v3/test_smoke.py (three tests); tests/model/gate/test_gate.py (one case); model-specs/acceptance.md (one paragraph); results/speedup/ledger.md (one row); results/178c-evidence/ (the quick partial file); this brief
- What is different now: `--parts level1,map,tornado,o1e` (default all four; `map` required). A subset writes `run.parts`, and the ids of parts not run are `{"cells": [], "not_run": "not_run_this_run"}`. A default run is byte-identical and writes no `run.parts`.
- New or changed interfaces: `run.py --parts`; file field `run.parts`; entry field `not_run`. Manifest unchanged.
- Acceptance criteria: default run byte-identical: met (smoke `cmp`; the quick-size default was not re-run, 40 min). `--parts level1,map` validates for its ids, carries the marker elsewhere, refused by `--final`, `accept.sh`, `check_gate.py`: met (tests; real smoke and quick files). Fast-loop wall time: this machine 1,875 s against the 3 to 5 min target: NOT met, level 1 dominates; Actions: not measured.
- Deviations from the brief: `map` is required in the list (every other part reads its schedules); a skipped part is an entry-level marker (`not_run`), not a marker in each cell, because the cells do not exist when a part is skipped; `OF1` and `CK1` stay `pending` in every run, so `map` adds no ids of its own to a partial file. The file is not named for its parts: the header names them.
- Risks / follow-ups: the target needs a smaller loop than `level1,map` at `quick` size: one grid point and fewer paths, or a cheaper level 1 (153c, kernel). `bench.py` cases `quick_headlines` and `quick_full` not added (176c unmerged).
- Instruction friction: none
- Verification: tests/model/model_v3 not converge: 438 passed; tests/model/gate: 17 passed; smoke default `cmp` identical; smoke partials validated and compared with the full smoke. Not run: the convergence test, `accept.sh` end to end, `check_gate.py --all`, the Actions timing.
- Overview sections likely needing an update: the run script and acceptance notes (`--parts`)
- Commit / branch: see below, brief/178c-parts-switch (not merged)
```
