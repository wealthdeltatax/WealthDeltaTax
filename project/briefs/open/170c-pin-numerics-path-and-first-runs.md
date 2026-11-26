# 170: Pin the numerics path, finish 169c

- **Status:** ready; Agent 2 (same agent as 169c if it has tokens)
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
- **Done:** nothing yet.
- **Next:** stage A.
<!-- progress:end -->

## Change report
(The agent fills this in.)
