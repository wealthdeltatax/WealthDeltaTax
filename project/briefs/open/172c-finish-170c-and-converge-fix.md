# 172: Finish 170c on the branch, fix the converge failure

- **Status:** ready; Agent 2 or 3
- **Author/date:** K. Ogata with the guru, 2026-11-26
- **Depends on:** 170c merged to main 2026-11-26 (the branch is merged; start from main; stages A below are done: both CPU families green, change reports written by the 170c agent in `project/briefs/done/170c-...md`)
- **Read:** `project/briefs/open/170c-pin-numerics-path-and-first-runs.md` (on main; the branch carries the older 169c brief), `results/169c-numerics/difference-report.md`, `tests/model/model_v3/test_converge.py`, `.github/workflows/model-checks.yml`

## Goal
Close 169c and 170c on the branch with a change report, and make `test_converge.py` runnable on GitHub.

## First Actions run read by the guru (run 45803742165, on main, before the pins)
- smoke: success, 24 min (Intel).
- accept: success, 2 h 58 min on Intel Xeon 8573C. Two `--size quick` runs, validation PASS (12 warnings, the known manifest ones), step 5 ok, step 6 byte-identical, step 7 ok. Wall time 10,695 s.
- converge: **failed**, 1 h 23 min on AMD EPYC 9V74: 2 passed, 2 errors. Both errors are in the fixture, not in an assertion: `test_converge.py:26`, `named()`: `S.choose(fmap, man['feasibility'])['S_central']` raises `'NoneType' object is not subscriptable`, so `S.choose` returned None for the arm in the fixture (the 20-path feasibility map has no feasible cell). The failing tests are `test_c1_five_seeds_agree_on_the_legacy_arm` and `test_c2_doubling_moves_the_means_little_on_the_legacy_arm`; the household-arm tests passed.
- fast: failed on AMD EPYC 7763, as predicted (old pins).
- Two `fast` runs of the branch were started by the guru (workflow_dispatch on `brief/169-numerics`): ids 45884609593 and 45884613916.

## Stages
- A (done by the 170c agent; skip, read its change report): read the two `fast` runs above (CPU line, result). If both green, and at least one ran on an AMD EPYC 7763 and one on an Intel or EPYC 9V74, that is the two-CPU check; if not, start more with `gh workflow run model-checks.yml --ref brief/169-numerics -f run_accept=false` until you have one of each (they cancel each other in the same group: wait for each to finish). Then write the 169c and 170c change reports and the progress blocks. Checkpoint: pushed.
- B (converge): find why `S.choose` returns None for the legacy-arm fixture. Two possibilities: (1) a real finding (no feasible schedule on the 20-path CRN for the legacy arm; the 057c rulings C1 and C2 accepted the legacy arm for these tests, so a legacy arm with no feasible cell contradicts that premise) or (2) the fixture builds the arm differently from `run.py` (compare how `run.py` builds the legacy arm's feasibility map). Report which, with the evidence. Fix the fixture only if it is (2); if it is (1), stop and ask the author. Do not change the model.
- C: run the repaired converge job on the branch (`-f run_converge=true -f run_accept=false -f run_smoke=false`); it takes about 1.5 h up to 3.5 h. Report each test result and wall time.

## Touches
`tests/model/model_v3/test_converge.py` (fixture only), the branch's briefs and progress blocks. No model arithmetic, no pins (unless a pin check fails, then stop).

## Acceptance criteria
- Two green `fast` runs on different CPU families, ids in the report.
- Converge: either all four tests green on Actions or the legacy-arm finding reported with evidence.
- Change reports written; no run used `--final`.

## Out of scope
171c (zero tolerance), the split final run, the SWF redesign.

## Open questions
If `fast` is red on the branch for any reason other than the CPU path, stop and report.

## Implementation notes
<!-- progress:start -->
- **Done:** nothing yet.
- **Next:** stage A.
<!-- progress:end -->

## Change report
(The agent fills this in.)

## Ruling on stage B and what remains (guru, 2026-11-26)
Stage B found, with evidence, that the legacy arm has no feasible schedule (best closure share 25.0% at 20 paths, 16.0% at 50, against the 75% floor; M2 and M4a also miss). **Author's ruling:** the legacy arm always fails the rule because of the 3.5% consumption assumption (I-D14c, abandoned as a central assumption); ignore the failure and keep the arm to learn from. The legacy arm is not changed and no rule is relaxed.
Assumption for challenge: "ignore" is read as "C1 and C2 must not depend on the legacy arm being feasible". They test sampling noise, which does not depend on which schedule is used.
- **B2 (code, the only change).** In `tests/model/model_v3/test_converge.py`, `named()` takes the schedule from `S.choose(...)` when it returns one (household arm, unchanged). When it returns None (the legacy arm), it uses the grid point with the highest F1 (ties: lowest M2 short) as the named schedule, and records in a module docstring line and in the test message that the legacy arm has no feasible schedule by design, with the reason. No change to `S.choose`, the rule, `run.py` or any model file. The tests keep the legacy arm, as ruled on 2026-11-25.
- **C (as before).** Start the converge job on the branch (`gh workflow run model-checks.yml --ref <branch> -f run_converge=true -f run_smoke=false -f run_accept=false`), read every test, report wall times. If C1 or C2 still fails on an assertion (not the setup), report the numbers (the spans per output and the doubling shifts) and stop; do not loosen a tolerance.
- **D (report only).** Does `run.py --arm legacy` exit with "no feasible schedule point under the manifest rule" (at smoke size, per your stage B)? Say what the legacy arm's `outputs.json` would then hold, and whether anything (the accept job, `accept.sh`, `check_gate.py`) calls `--arm legacy`. Report; change nothing. The author may want the legacy arm to write a labelled outcome instead of exiting, as a later brief.
- First: `git checkout brief/172-converge-fixture`, merge current `main`, read the report above.
