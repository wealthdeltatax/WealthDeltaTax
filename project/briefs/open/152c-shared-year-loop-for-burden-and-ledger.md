# 152: One year loop shared by burden and ledger (household arm)

- **Status:** author; implemented and pushed on `brief/152-shared-year-loop`, NOT byte-identical in 2 of 27 grid schedules (about 1e-7 relative); waiting for the author's tolerance decision
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
- **Needs the author:** accept a tolerance rule for the household-arm burden outputs (about 1e-7 relative on O2, O2d, O5 at steep schedules; pins that hold household values would move), or drop 152c.
- **Not done:** pins (none regenerated), `quick` comparison against a tolerance, removal of the temporary `.github/workflows/152c-quick.yml`.
<!-- progress:end -->
