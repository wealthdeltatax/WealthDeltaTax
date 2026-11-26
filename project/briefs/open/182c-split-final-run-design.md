# 182: Split final run, design of the partial files and the exact merge

- **Status:** ready (design only, no code)
- **Author/date:** K. Ogata with the guru, 2026-11-26
- **Depends on:** none. Reads `run.py` as it is on main; 154c and 178c change it later, so the design names the seams, not line numbers.
- **Read:** `model/model_v3/run.py` (`run_point`, `main`, the O1e and `ends` lines); `model/model_v3/out/assemble.py` and `out/writer.py`; `model/model_v3/runner/rt.py` or wherever `streams` lives; `results/run-cost/run-cost.md` (projection tables); `.github/workflows/model-checks.yml` (the `run_final_size` input and the jobs' `timeout-minutes`); `results/169c-numerics/difference-report.md` (why byte-identical merges matter)

## Goal
A final-size run is hours to days of serial work (level 1 and tornado about 79 min per grid point at 1,000 paths on this machine, plus 603 O1e roots at the first point), and a hosted job is capped at 6 hours. Design how to cut the run into jobs, and how to merge their partial outputs so the merged file equals the unsplit file to the byte. The first official final run (181c) needs it. Design first, as the author and the 168c review ruled; 183c builds it.

## Design (what the note must settle)
1. **Units of work and their seams.** Per grid point: level 1 and tornado (5 units, about 80 min each before 151c and 154c). O1e: roots by (schedule, draw) in batches; the first point only (`be`). Name the batch size from the per-root cost and the 6-hour cap with a margin, and say what a failed shard costs to redo.
2. **Draws must not depend on the split.** `draw_theta(level2_draws, ..., n2)` makes all draws from one stream; a shard that takes draws i to j must get the same theta rows as the unsplit run. State how (generate all, slice) and test it.
3. **Partial files.** `--point` today writes an assembled single-point `outputs.json`, which cannot be merged (targets, O1e ends and level 1 info are in memory only). Specify the partial: raw samples before `reduce`, hex floats, the chosen schedule names, the feasibility map, `cap`, `ends`, `info`, and a header (size, seed, arm, point, numerics setting, git SHA, input hashes). Say which of these the merge checks for equality across shards (all but the point and the batch).
4. **The merge.** A module that reads the partials, refuses any mismatch in the header, concatenates in canonical order (point order, then draw order), and calls the same `reduce` and `asm.assemble` as the unsplit run, so there is one assembly code path. List every place the unsplit path computes something across points (the range merge, the O1e at the first point, `tg`) and say where it lives in the merge.
5. **The proof.** Smoke size: split into the same units, merge, compare to the unsplit file byte for byte; also with the batches in a different order and with one shard rerun. Say what 183c must show and which test pins it.
6. **Workflow.** A matrix job per unit with `actions/upload-artifact`, then a merge job; the `run_final_size` input exists and does nothing today. Say how many jobs and how long, for the final run, at 2 and at 4 cores, from the measured cost per unit; the free-tier limit on concurrent jobs is read from GitHub's documentation, not assumed (the guru's figure of 20 is unchecked).
7. Never `--final`: the run refuses it and the split does not change that.

## Touches
`results/split-run/design.md` (new). Nothing else. The note ends with the stage plan for 183c: files, tests, checkpoints.

## Acceptance criteria
- Items 1 to 7 each answered with a decision and the evidence (file and line for the seams; numbers for the unit costs).
- A sentence on what could still make the merge differ from the unsplit file (float summation order across batches is the main one) and how the design avoids it.
- Open questions listed for the author, each with a proposal.

## Out of scope
Code; the merge module itself; the first run (181c).

## Open questions
Written by the agent. Guru's: the batch size, whether level 1 and tornado of one point may be separate shards, and whether the merge may reread level 1 from a cache.

## Implementation notes
<!-- progress:start -->
- **Done:** design note `results/split-run/design.md`: items 1 to 7, the merge-difference paragraph, 7 open questions, the 183c stage plan. No code.
- **Next:** author reads the open questions (1 first: final-size O1e draws are 0 in `SIZES`, not 200).
- **Resume:** none.
- **State:** done, pushed on `brief/182-split-run-design`; not merged.
<!-- progress:end -->

## Change report
Design written to `results/split-run/design.md` (the only file besides this brief). Decisions: units are `plan`, one `point` unit per grid point (level 1 and tornado together), O1e batches of 25 draws of one schedule plus an `o1e-point` unit; every O1e shard generates all draws and slices; the merge reads assembled per-point documents (not raw samples: about 104 MB per point at 10,000 paths would break the 500 MB Free artifact storage) and raw hex-float roots; the unsplit run becomes plan, units, merge in one process, so there is one assembly path. Wall time of the final run on hosted runners: 1.6 to 7.4 h at 4 workers (3.0 h at the smoke-like mix) against 32 to 160 h serial; 20 concurrent jobs on Free, 6 h per job, 256 matrix jobs, 4 vCPU on public repos, all read from GitHub's documentation. Two unmeasured factors (hosted/local 1.4, 4-worker speed-up 2.5) are replaced by 183c's calibration.
Findings, not repaired: `SIZES['final']` has 0 O1e draws; `workers` is written into the output file; `cap` records are lost in pool workers.
Open questions: seven, in the note; the first is the final-size O1e draws.
