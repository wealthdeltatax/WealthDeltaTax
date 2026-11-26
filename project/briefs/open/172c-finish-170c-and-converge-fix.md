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
- **Done:** claimed 2026-11-26 from `main` at affacdf; stage A was done by the 170c agent (merged); stage B investigated: finding (1), see the report.
- **Next:** B2 pushed; stage C running; then D.
- **Not run:** stage C result, stage D.
- **State:** B2 done, C started
<!-- progress:end -->

## Change report
- Task: 172c, stage B (why `S.choose` returns None in the converge fixture); stage A was done and merged by 170c; stage C not started.
- Files changed: this brief only. No test, model or pin edited.
- What is different now: nothing in the code. The cause is known and it is possibility (1), a real finding, not a fixture difference.
- Evidence: (a) the fixture and `run.py --arm legacy` build the same thing: `named(*base)` passes the plain context `ctx` to `S.feasibility(R.make_ev(cp, tornado_crn.standard_normal((R.T, n))), S.grid(lv))` and then `S.choose(fmap, man['feasibility'])`; `run.py` line 93 to 97 does the same with `c0 = ctx` when the arm is legacy (the fixture only differs in the path count, 20, which equals `--size smoke`). (b) I reproduced the failure with a standalone script on the merged `main` (affacdf), seed `run.SEED`, rule `{m2_cap_pct_per_year: 2.0, m4a_floor_pct: 0, closure_share_pct: 75}`: 27 grid points, 0 feasible. At 20 paths the best closure share F1 is 25.0 (M2 3.94, M4a 25.07); at 50 paths 16.0 (M2 3.50, M4a 24.35). The best points miss both the F1 floor (75) and the M2 cap (2.0). A 1,000-path run was started and had not finished when I stopped. (c) So `run.py --arm legacy` would also exit with "no feasible schedule point under the manifest rule" at smoke size (20 paths) and at 50. (d) The two tests were switched to the legacy arm on 2026-11-25 by an author ruling (057c, C1 and C2) and merged on 2026-11-26; the evidence folder has no run of them on the legacy arm. `results/run-cost/run-cost.md` already records that `--arm legacy` cannot complete O1e.
- Acceptance criteria: two green `fast` runs on different CPU families: met by the 170c report (runs 45884613916 on EPYC 7763 and 45884808194 on EPYC 9V74; the brief's ids 45884609593 are the other dispatch). Converge: legacy-arm finding reported with evidence: met. Change reports written: met. No run used `--final`: met.
- Deviations from the brief: none; I stopped at (1) as the brief says, no fixture change.
- Risks / follow-ups: the legacy arm has no feasible named schedule, so C1 and C2 as ruled cannot run. Options for the author: (i) name the schedule for C1 and C2 from the household arm's `S_central` and run the level 1 draws on the legacy arm with it (changes the premise of the ruling); (ii) pick another arm that varies with the level 1 paths; (iii) relax the legacy arm's feasibility rule for the test only (changes a rule); (iv) revert C1 and C2 to the household arm and accept that they test nothing (the 2026-11-25 reason). Until then `accept.sh` step 2 and the converge job fail.
- Instruction friction: none.
- Verification: standalone script (not committed) run with `python -I` against `model/model_v3`; `fast` not re-run (no code change).
- Local-only files to move by hand: none.
- Overview sections likely needing an update: none.
- Commit / branch: `brief/172-converge-fixture`, brief edits only; NOT merged: `NEEDS THE AUTHOR`.


## Ruling on stage B and what remains (guru, 2026-11-26)
Stage B found, with evidence, that the legacy arm has no feasible schedule (best closure share 25.0% at 20 paths, 16.0% at 50, against the 75% floor; M2 and M4a also miss). **Author's ruling:** the legacy arm always fails the rule because of the 3.5% consumption assumption (I-D14c, abandoned as a central assumption); ignore the failure and keep the arm to learn from. The legacy arm is not changed and no rule is relaxed.
Assumption for challenge: "ignore" is read as "C1 and C2 must not depend on the legacy arm being feasible". They test sampling noise, which does not depend on which schedule is used.
- **B2 (code, the only change).** In `tests/model/model_v3/test_converge.py`, `named()` takes the schedule from `S.choose(...)` when it returns one (household arm, unchanged). When it returns None (the legacy arm), it uses the grid point with the highest F1 (ties: lowest M2 short) as the named schedule, and records in a module docstring line and in the test message that the legacy arm has no feasible schedule by design, with the reason. No change to `S.choose`, the rule, `run.py` or any model file. The tests keep the legacy arm, as ruled on 2026-11-25.
- **C (as before).** Start the converge job on the branch (`gh workflow run model-checks.yml --ref <branch> -f run_converge=true -f run_smoke=false -f run_accept=false`), read every test, report wall times. If C1 or C2 still fails on an assertion (not the setup), report the numbers (the spans per output and the doubling shifts) and stop; do not loosen a tolerance.
- **D (report only).** Does `run.py --arm legacy` exit with "no feasible schedule point under the manifest rule" (at smoke size, per your stage B)? Say what the legacy arm's `outputs.json` would then hold, and whether anything (the accept job, `accept.sh`, `check_gate.py`) calls `--arm legacy`. Report; change nothing. The author may want the legacy arm to write a labelled outcome instead of exiting, as a later brief.
- First: `git checkout brief/172-converge-fixture`, merge current `main`, read the report above.

### Stages B2, C and D (agent, 2026-11-26)
- **B2:** `named()` in `tests/model/model_v3/test_converge.py` now returns `S.choose(...)['S_central']` when a schedule is feasible (household arm, unchanged) and otherwise the grid point with the highest F1 short (ties: lowest M2 short); the module docstring says why. Nothing else changed: no model file, rule, pin or `run.py`. Commit `fff68c4` on `brief/172-converge-fixture` (main merged in; the only conflict was this brief, resolved by taking main's text and keeping this report).
- **C:** converge job started on the branch, run 45895885796 (`-f run_converge=true -f run_smoke=false -f run_accept=false`). Result: see the next line (filled in when it finishes).
- **D (report only, nothing changed):** yes, `run.py --arm legacy` exits with "no feasible schedule point under the manifest rule" at line 98, before any point is run, at smoke size (20 paths) and at 50; it writes no `outputs.json` at all (the `label` with `arm='legacy'` at line 111 is never reached today). Nothing calls `--arm legacy`: not `accept.sh`, not `.github/workflows/model-checks.yml`, not `check_gate.py` or its tests; only `run.py`'s own docstring and argument list name it. A labelled outcome instead of the exit would be a later brief (for example the highest-F1 point with `central=False`, as B2 does in the test).
