# 152: One year loop shared by burden and ledger (household arm)

- **Status:** author; done on `brief/152-shared-year-loop`, pushed, not merged; needs the author to merge (tolerance rule decided 2026-11-28; the output movement below is for the author to read)
- **Agent:** 5
- **Needs:** ~179c
- **Length:** 1
- **Author/date:** K. Ogata with the guru, 2026-11-26
- **Depends on:** 179c (the profile says whether it is worth it), 171c
- **Read:** `results/speedup/profile-after-154c.md` (when it exists); `model/model_v3/runner/arm.py` (329 of 330 lines: new code goes in `switches.py` or a new file); `model/model_v3/core/burden.py`; `model-specs/architecture.md` 5.1

## Goal
Under the household arm the burden run and the revenue and ledger run each walk the same years over the same lines. Share one year loop if the profile shows the duplication costs a real share of `core_run`. Small to medium gain by the guru's guess; probably not byte-identical, because shared sums change the order of float additions.

## Design
Decided only after 179c. Until then: the profile row it must show (share of `core_run` spent in the duplicated work), the proof (byte-identical if the order of operations is kept; else a tolerance rule signed off, as 153c), the layer check, the `arm.py` budget.

## Touches
Named after 179c; at least `runner/arm.py` or `switches.py`, `core/burden.py`, `tests/model/model_v3/`, `results/speedup/ledger.md`.

## Acceptance criteria
Written when the brief is released: the profile share, the proof, the bench times before and after.

## Out of scope
The compiled kernel (180c): if the kernel brief goes ahead, this one may be dropped because the loop is rewritten there.

## Open questions
Whether to do it at all if 180c is adopted; decided after 179c and 180c stage A.

## Implementation notes
<!-- progress:start -->
- **Claimed:** branch `brief/152-shared-year-loop` (from main cc3c844).
- **Design:** `revenue.run_lines(..., tap=)` feeds a `burden.Tap` each flow and year (`add`, `year`); `tap.flows()` is the dict `line_flows` returns; `core_run` uses it under the household arm (`ar.name != 'legacy'`), so the kernel is walked once. The legacy arm is unchanged. Runner stays at 368 lines.
- **Speed** (one `core_run` + headlines, household, 2 cores, serial, best of 2): 20 paths 1.97 to 1.14 s; 200 paths 4.97 to 2.79 s; 1,000 paths 18.25 to 11.0 s (1.66x to 1.78x). Quick on Actions, separate hosted machines: before 29m53s, after 18m29s. 179c's estimate (helps only the 24%) was too low: this removes a whole kernel pass.
- **Proof:** full household evaluation (headlines and all groups), 20 paths, three schedules: same hash on old and new tree. Flows of the shared walk equal `line_flows` to the byte for those schedules (`test_shared_walk.py`). **But not everywhere:** scanning the 27-schedule lever grid at 20 paths, 25 are byte-identical and 2 differ (tau_m 0.7 k_ln 2 ratio 0.25: max abs 4.3e-4 on a net scale 2.8e4; tau_m 0.9 k_ln 2 ratio 0.25: 8.1e-3 on 3.3e4), about 1e-7 relative. Smoke outputs, old against new tree: O2 6 values (max rel 4.6e-7), O2d 9 (2.0e-5), O5 15 (4.5e-8), all at S_high long (and short for O5/O2d where listed); nothing else. The quick `outputs.json` differs by one digit (270,542 against 270,543 characters).
- **Cause (probable, not isolated):** `run_lines` keeps the public ledger (`book.ledger`), and `kernel.py:184` and `:228-230` read it (the state's stake by class); the burden's own walk (`line_flows`) never set it. So the two old walks differed for steep schedules; the shared walk gives the burden the ledger-aware numbers.
- **Decision (author, 2026-11-28):** accept the ledger-aware numbers. Rule: burden flows within 1e-6 of the net scale on every grid schedule (test). I first proposed also 1e-4 relative on O2, O2d, O5; the quick run shows O2b and O2c (threshold shares: a few lines crossing) move more, so no output tolerance is written; the measured movement is in `model-specs/metrics.md`.
- **Quick movement, old against new tree** (Actions run 46136243148, forced path): 41 of 45 outputs byte-equal; O2 1 of 66 values differ (max rel 3.5e-4), O2b 7 of 200 (6.9e-2), O2c 6 of 222 (1.1e-2), O2d 6 of 66 (4.4e-3). Quick wall time on separate hosted machines: before 32m13s, after 21m34s.
- **Pins:** none moved: `fast` has no household pin; smoke passes (Actions run 46136242651). The tripwire and the quick pins in `project/restructure` are legacy-arm only.
<!-- progress:end -->

```
Change report
- Task: 152c One year loop shared by burden and ledger (household arm)
- Files changed: model/model_v3/core/burden.py (`_flows`, `Tap`); core/revenue.py (`run_lines(tap=)`); runner/runner.py (`core_run`; 368 lines); tests/model/model_v3/test_shared_walk.py (new, 4 tests), test_arm_switch.py (the hook's check count is one walk's: 1000 to 500); model-specs/architecture.md and metrics.md (notes, tolerance rule); results/run-cost/run-cost.md, results/speedup/ledger.md; project/lane-plan.html (regenerated); this brief.
- What is different now: the household arm walks the kernel once per schedule, not twice. The burden's line flows now come from the ledger's walk, so they include the ledger the old burden walk never had. The legacy arm is unchanged.
- New or changed interfaces: `revenue.run_lines(..., tap=None)`, `burden.Tap`; none on the command line.
- Acceptance criteria (written at release: the profile share, the proof, the bench times): profile share: the duplicated walk is about 40% of a household `core_run` (18.25 s to 11.0 s at 1,000 paths): met by measurement. Proof: byte-identical on the legacy arm and on 25 of 27 grid schedules; 2 steep schedules differ by 1e-7 of the net scale, within the tolerance rule the author accepted: met. Bench: one `core_run` plus headlines, 1.97 to 1.14 s (20 paths), 4.97 to 2.79 s (200), 18.25 to 11.0 s (1,000); quick wall 32m13s to 21m34s on Actions (separate machines).
- Deviations from the brief: the brief expected a byte-identical result with different summation order; the cause of the difference is instead the public ledger (kernel.py:184, 228-230), which the burden's old walk never set. The 179c estimate (gain only on the 24%) was too low.
- Risks / follow-ups: the cause was not isolated by an experiment (giving `line_flows` the ledger); the grid test shows the effect is confined to steep schedules. O2b and O2c move up to 6.9e-2 at quick size in 7 values (a few lines crossing a threshold); the author reads that. 189c (fewer array passes) now builds on a faster `core_run`.
- Instruction friction: the stop hook warns of unpushed commits when the remote branch exists at HEAD (stale), as before; the fast job's lane-plan check fails after any brief status change until `build_lane_plan.py` is run.
- Verification: tests above; `fast` rerun after this commit (see the branch); temporary workflow `152c-quick.yml` removed in this commit.
- Overview sections likely needing an update: none
- Commit / branch: see the branch head, `brief/152-shared-year-loop`
```
