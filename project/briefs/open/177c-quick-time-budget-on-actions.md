# 177: `quick` time budget on Actions

- **Status:** ready; 154c merged 2026-11-27
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
- **Done:**
- **Next:**
- **Resume:**
- **State:** draft
<!-- progress:end -->
