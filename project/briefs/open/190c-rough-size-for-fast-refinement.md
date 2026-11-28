# 190: A rough size for fast refinement runs

- **Status:** hold; waits for 187c (it measures the noise at small path counts)
- **Agent:** 6
- **Needs:** 187c
- **Length:** 1
- **Asks:** which outputs the rough run must show (default: the headlines and O1f, O2b, O2c, F1 closure share, and the replacement time), and the longest acceptable wait (author's wish: as quick as possible, a few minutes)
- **Author/date:** K. Ogata with the guru, 2026-11-28
- **Depends on:** 187c (noise by path count); 178c (`--parts`) and 189c are merged or in progress and only make it faster
- **Read:** `model/model_v3/run.py` (`SIZES`, `--parts`, `--point`, `--paths`); `results/speedup/profile-after-154c.md`; the 187c report `results/converge/c1-noise.md` once it exists; `project/agents/reference/code/speedup.md`

## Goal
The author refines the model by running it, reading rough numbers and checking by intuition that a change moves in the right direction. That wants numbers in minutes, not the 20 to 32 minutes of `quick`, accepting more noise; the proper check is a later full run. Add a `rough` size (a fourth beside smoke, quick and final), say plainly in its output that it is for refinement and not acceptance, and measure what it costs and how noisy it is.

## Design
1. Candidate `rough`: level 1 at a few hundred paths per schedule, one grid point (the central point) or two, tornado at 20 paths, O1e root only, `--parts` chosen so the outputs the author names are present. Pick the numbers from the 179c part shares and the 187c noise table: the path count where the noise on the named outputs is still small enough to see a direction (state the rule: for example the noise sd under a quarter of the change a typical lever makes; the agent proposes the rule, the author signs).
2. Measure on the hosted 4-core runner and on 2 cores: wall time for `rough` against `quick`; the same outputs from `rough` and `quick` side by side for the central point (difference against the 187c noise at that path count).
3. The run file carries `run.size = rough` and the validator refuses it as a final file like partial files (178c); `accept.sh` and the gate refuse it.
4. Optionally a `workflow_dispatch` input `run_rough` so the author can start it from the Actions page and read the numbers in the job summary.

## Touches
`model/model_v3/run.py` (stay within 120 lines; the size row and a refusal), `model/tools/validate_outputs.py`, `model/tools/check_gate.py`, `tests/model/model_v3/`, `.github/workflows/model-checks.yml` (one input and job), `results/speedup/`.

## Acceptance criteria
- `rough` time and noise table in the ledger, from real runs; the rule for the path count written and the numbers from it.
- Refused as a final file by the validator, `accept.sh` and the gate (tests).
- Time to numbers on Actions stated; if over 5 minutes, say which part dominates.

## Out of scope
The full run, the split final run (183c), any change to the model.

## Implementation notes
<!-- progress:start -->
- **Done:**
- **Next:**
- **Resume:**
- **State:** draft
<!-- progress:end -->
