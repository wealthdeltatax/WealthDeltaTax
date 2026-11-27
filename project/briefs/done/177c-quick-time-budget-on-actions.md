# 177: `quick` time budget on Actions

- **Status:** done, merged 2026-11-28
- **Agent:** 3
- **Needs:** 154c, 176c
- **Length:** 1
- **Author/date:** K. Ogata with the guru, 2026-11-26
- **Depends on:** 154c (the budget is set from its figure), 176c (bench)
- **Read:** `.github/workflows/model-checks.yml` (jobs, `timeout-minutes`, the `lscpu` log step); `tests/model/model_v3/accept.sh`; `results/speedup/ledger.md`

## Goal
A slowdown shows up as a failed check, not as a surprise. A job runs `quick` (and, once 178c lands, the headline-only fast loop) and fails if the wall time passes a budget.

## Decisions (author, 2026-11-26)
Target: `quick` under 10 minutes. Where it is measured is a proposal (below) the author confirms.

## Design
1. **Where measured (proposal for the author):** on the hosted 4-core runner, because that is where runs happen unattended and it is the same machine every time. This 2-core machine and the author's computer are reported in the ledger but do not gate. The agent reads `nproc`, `free` and the CPU model from the Actions log and writes them into the budget note; if the runner has fewer than 4 cores, say so and set the budget from the measured figure.
2. **Budget:** `QUICK_BUDGET_S` in the workflow, set to the measured median of three runs plus 25% (runners differ by CPU family; the budget covers the two families seen: AMD EPYC 7763 and 9V74, Intel Xeon 8573C). A run over budget fails the job with the time, the budget and the CPU line in the message.
3. **Separate job `speed`** (manual and on pushes that touch `model/`), not part of `fast`; it runs `bench.py` small cases too and uploads the JSON as an artifact, so the ledger can cite a run id.
4. Bench numbers are informational; only the `quick` wall time gates.

## Touches
`.github/workflows/model-checks.yml` (a new job; reviewer: web), `results/speedup/ledger.md`, `project/agents/reference/code/speedup.md` (one line on the budget). Nothing under `model/`.

## Acceptance criteria
- Three Actions runs of the job on at least two CPU families, ids, times and CPU lines reported; budget set by the rule above.
- A deliberately slowed run (a sleep behind an env flag, not committed) fails the job with the message; reported.
- No run uses `--final`.

## Out of scope
Final-size timing (181c); gating on bench cases.

## Open questions
For the author: confirm the 4-core hosted runner as the gate (default), or name your own computer's cores and memory for a second reference line.

## Implementation notes
<!-- progress:start -->
- **Done:** the `speed` job in `.github/workflows/model-checks.yml` (manual `run_speed`, and pushes to `main` that touch `model/`); three runs on three CPU families; budget set; the slowed run fails the job; ledger section and one line in `speedup.md`.
- **Next:** the author's answers to the open question and the budget rule (below); then merge and retire.
- **Decisions:** `QUICK_BUDGET_S` = 1670 s = slowest of the three runs plus 25%, not the median rule (1219 s), which the EPYC 7763 would fail.
- **State:** review (branch pushed)
<!-- progress:end -->

Change report
- Task: brief 177c, `quick` time budget on Actions
- Files changed: `.github/workflows/model-checks.yml` (job `speed`, input `run_speed`), `results/speedup/ledger.md` (Actions timing section), `project/agents/reference/code/speedup.md` (rule 8), this brief
- What is different now: a job `speed` runs the bench small cases and `quick` (`--workers` from cores and memory, as accept.sh) and fails when `quick` takes longer than `QUICK_BUDGET_S`, with the time, the budget and the CPU line in the message. On pushes to `main` it runs only if the push touched `model/`.
- Acceptance criteria: three runs on three CPU families, 46065482351 (Xeon 6975P-C, 975 s), 46065485244 (EPYC 9V74, 954 s), 46065488130 (EPYC 7763, 1335 s), all 4 cores, 15 GB; bench small cases in the ledger. Budget 1670 s. Slowed run (a throwaway branch with `sleep 800`, deleted, never committed here): run 46068573100 on EPYC 9V74, `quick took 2017 s, over the budget of 1670 s (workers 4, CPU: AMD EPYC 9V74 80-Core Processor)`, job failed. No run used `--final`.
- Deviations from the brief: (1) budget is the slowest run plus 25% (1670 s), not the median plus 25% (1219 s), because the EPYC 7763 took 1335 s and would fail a median-based gate about one run in three; (2) the Xeon 8573C named in the brief did not come up, a Xeon 6975P-C did; (3) `quick` takes 954 to 1335 s, over the author's target of 600 s.
- Risks / follow-ups: the budget lets `quick` get 25% slower on the slowest family before it fails, and a lot slower on the fast ones; per-family budgets are possible if the author wants a tighter gate. A new CPU family slower than the 7763 would fail. The job on `main` pushes costs about 20 to 25 minutes of a runner for each push that touches `model/`.
- Instruction friction: none
- Verification: workflow YAML parsed; the four Actions runs above.
- Overview sections likely needing an update: none
- Commit / branch: brief/177-quick-budget. NEEDS THE AUTHOR: the brief's open question (confirm the 4-core hosted runner as the gate) and the budget rule (1670 s or 1219 s).
