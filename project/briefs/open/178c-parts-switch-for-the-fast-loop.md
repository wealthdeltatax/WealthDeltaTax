# 178: `--parts` switch, the fast loop

- **Status:** hold; draft, ready after 154c merges
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
<!-- progress:start -->
- **Done:**
- **Next:**
- **Resume:**
- **State:** draft
<!-- progress:end -->
