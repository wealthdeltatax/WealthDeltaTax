# 170: Pin the numerics path, finish 169c

- **Status:** done, merged 2026-11-26 (author: merge now; gate G1 stays deselected in fast, read from the Actions accept job); open items continue in 172c and 171c
- **Author/date:** K. Ogata with the guru, 2026-11-26
- **Depends on:** 169c stage A (b), stage B and the difference report (branch `brief/169-numerics`, bb36bc25)
- **Read:** the branch's `project/briefs/open/169c-actions-numerics-and-first-runs.md` (progress block), `results/169c-numerics/difference-report.md`, `model/model_v3/numerics.py`, `project/restructure/move_tripwire.py`, `.github/workflows/model-checks.yml`

## Goal
`fast` is green on every runner and on the author's machine; the long checks have run once on GitHub and been read.

## Decisions (author, 2026-11-26)
The 169c stop rule is answered: **regenerate the pins on the forced path (`NPY_DISABLE_CPU_FEATURES=X86_V4`) now**, even though the difference is not last-bit only. The cause is knife-edge counts (values that are zero in theory, about 1e-15, fall either side of zero: O1f flips 3 of 600; O2b and O2c move by up to 0.22 relative on 10 values). Tolerance for those counts is a separate brief (171c) and is not part of this one. Do not change model arithmetic, O1f, O2b or O2c here.

## Stages
- A: continue on `brief/169-numerics` (merge current main into it first: it carries the workflow). (1) Wire the variable into `model-checks.yml` (workflow-level env) if 169c did not. (2) Regenerate the pin families on the forced path, one commit per family with old and new value in the message: `legacy_digest.json`, the `test_groups` pin, the tripwire baseline (inputs, legacy, pack, evaluation hashes), stored run hashes, any `quick` reference file. Commit before the tripwire (it reads git history). (3) Add a short note to the difference report: the decision, the pins changed, and that O1f, O2b, O2c are knife-edge counts awaiting 171c. (4) Document the variable in `project/agents/agent-code.md` and `model-specs/acceptance.md` (the author's machine must set it; `run.py` and the model conftest already do). Checkpoint: pushed; check: tripwire PASS and all fast suites locally after `git clean -fdx`.
- B: `accept.sh` runs whole: step 1 now collects under `-I` (fixed in 169c); make the `accept` job call the whole script if it fits in one job (about 5 hours; else keep `--check`, `--compare`, `--r6` and say why). Step 5 on `quick-q4` passes. Checkpoint: pushed.
- C: after the author says merge, `fast` on two runs that landed on different CPU models (log the CPU line; an AMD EPYC 7763 run is the one that failed before) is green.
- D: read the first Actions run (45803742165, started by the guru on main: smoke green; converge and accept running when this brief was written; its `fast` job failed on an AMD EPYC 7763 as expected). Report each job's result, wall time and CPU model; if converge or accept failed, say why, and which part is the CPU path (rerun on the branch after stage A) and which is real. Do not tick `run_final_size`.

## Touches
Pin files, `model-checks.yml`, `accept.sh`, docs named above, `results/169c-numerics/`. No model arithmetic.

## Acceptance criteria
`fast` green on runners with and without AVX512; tripwire PASS locally and on Actions; `accept.sh` passes whole locally; first run results written up with run ids; no run used `--final`.

## Out of scope
Tolerance for O1f and O2 counts (171c), stage D of 169c (split final run), the SWF redesign.

## Open questions
Stop and report if a pin changes by more than its hash (a changed value in a committed results file), or if the AMD runner still fails after the pins move.

## Implementation notes
<!-- progress:start -->
- **Done:** stage A (variable in the workflow; three pin families regenerated, one commit each with old and new value; note in the difference report; variable documented in `agent-code.md` and `acceptance.md`). Stage B (accept job calls `accept.sh` whole; `ACCEPT_KEEP=1`). Stage D read. Stage C measured on the branch (below). Pushed on `brief/169-numerics`, draft PR 4.
- **Next:** author. Decide the two items under NEEDS THE AUTHOR, then say merge. Not merged.
- **Decisions:** the gate real-repository test is deselected in `fast` (it runs the whole acceptance); the "Gate table" step is dropped.
- **Gotchas:** converge fails on the legacy arm on both CPU paths (real, not CPU). `accept.sh` was not run whole locally (about 5 h on 2 cores, and it stops at step 2).
<!-- progress:end -->

## Change report

**Status: NEEDS THE AUTHOR.** Two acceptance criteria are not met as measured (below). Nothing merged. No run used `--final`; `run_final_size` not ticked.

**Stage A.** `NPY_DISABLE_CPU_FEATURES: 'X86_V4'` is in the workflow-level `env:`. Pins regenerated on that path, one commit per family (old and new value in each message): `legacy_digest.json`; `PIN` in `test_groups.py` (`ce75c164...` to `a7763389...`); `move-tripwire-baseline.json`. `results/057c-evidence/quick-q4/outputs.json` untouched (no test compares it with a fresh run). No pin changed by more than its hash, so the first stop rule did not fire. Tripwire PASS (pack hashes unchanged). After `git clean -fdx` all fast suites pass locally (model_v3 408 passed). The difference note is in `results/169c-numerics/difference-report.md`. O1f, O2b, O2c wait for 171c; model arithmetic unchanged.

**Stage B.** The accept job runs `bash tests/model/model_v3/accept.sh` whole; the timeout is 350 min. Step 1 collects under `-I`; `ACCEPT_KEEP=1` keeps the two run folders for the artifact. Whole-script time estimate: smoke 24 min + converge 83 min + two quick runs 2 x 89 min = about 5 h, so it fits one job. Step 5 on `quick-q4` passes. NOT MET: "accept.sh passes whole locally" was not run (about 5 h on 2 cores), and it cannot pass today because step 2 (converge) fails.

**Stage C (branch, not main).** `fast` is green on both CPU kinds, same commit 2781106:
- run 45884613916 (dispatch), job 140132104110: AMD EPYC 7763 (no AVX512), 965 s, success. This is the CPU that failed before.
- run 45884808194 (PR 4), job 140132741296: AMD EPYC 9V74 (AVX512), 673 s, success.
So the AMD stop rule did not fire. The run after merge on main is still to do once the author says merge.

**Stage D, first run 45803742165 (main, 4d91022 era, old pins, started 10:41 UTC, ended 13:40 UTC).** Conclusion: failure.
| job | result | wall | CPU |
|---|---|---|---|
| fast (139853407280) | failure | 836 s | AMD EPYC 7763 |
| smoke (139853407240) | success | 1465 s | AMD EPYC 9V74 |
| converge (139853406715) | failure | 5019 s | AMD EPYC 9V74 |
| accept, two quick runs (139853407082) | success | 10695 s | Intel Xeon Platinum 8573C |
- fast: CPU path. The old pins fail on the EPYC 7763; fixed by stage A (green above).
- converge: real, not CPU. `S.choose` returns None for the legacy arm at 20 paths, on both numerics paths (about 160 s each). Likely no grid point meets the manifest feasibility rule for that arm on the 20-path fixture; not investigated further, no test or model change.
- accept: run 1 and run 2 passed validation (0 errors, 12 warnings), step 5, the byte compare and step 7 (R6). Outputs uploaded as `accept-outputs`.
- smoke: green.

**Deviations.** (1) `fast` deselects `tests/model/gate/test_gate.py::test_real_repository_is_closed_today`, and the "Gate table (report only)" step is dropped: `check_gate` G1 runs the real `accept.sh`, which now passes step 1 and so runs for hours. `check_gate.py` itself unchanged. (2) `ACCEPT_KEEP` is new in `accept.sh`.

**NEEDS THE AUTHOR.**
1. Converge legacy arm fails for real (test or fixture or model); needs a brief.
2. The gate G1 and its test run the whole acceptance: stub it, or retire the test, or accept the deselect.
3. 171c tolerance for O1f, O2b, O2c still open.
