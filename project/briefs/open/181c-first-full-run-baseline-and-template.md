# 181: First full run, as the baseline and the template

- **Status:** hold; draft, the author starts it
- **Agent:** 4
- **Needs:** 183c, 171c, 154c
- **Length:** 1
- **Author/date:** K. Ogata with the guru, 2026-11-26
- **Depends on:** 183c (split run on Actions), 171c (zero tolerance), 151c and 154c (byte-identical levers; merged first so the baseline costs hours, not days)
- **Read:** `results/split-run/design.md`; `results/speedup/ledger.md`; `model-specs/acceptance.md`; `results/run-cost/run-cost.md` (the projection tables)

## Goal
Run the final-size run once, split over Actions jobs, and keep it as (1) the reference every later change is compared with, and (2) the template for how a full run is started, recorded and read. The author reserves the full run for when it is needed; this is the first one.

## Decisions (author, 2026-11-26)
"The full first run will run so we can get a comparison and a template." A fuller run is waited for, especially on Actions.

## Guru proposal for the order (challenge it)
Run it after 151c, 154c, 171c and 183c. 151c and 154c are byte-identical, so the numbers are the numbers the slow code would have given; running the old code first would cost days and add nothing but a measured "before" time. That time is replaced by the 150c projection (about 64 h serial, central), labelled an estimate, plus the per-unit costs measured on the way. Non-byte-identical levers (153c, the compiled kernel) are compared with this run under their tolerance rules.

## Design
1. Start the split jobs from the Actions tab (`run_final_size`), no `--final`. The agent records the run id, every shard's CPU line, cores and wall time.
2. Merge, validate (the merge job and `check_gate.py` in report mode), and commit the merged `outputs.json` hash and the validation result under `results/final-run/` (the file itself only if under the repository's size rule; otherwise its hash and the Actions artifact name with its retention date).
3. Write `results/final-run/run-record.md`, which is also the template: command and inputs, SHA, numerics setting, jobs and times per unit, hashes, validation, wall time total, what failed and was rerun, cost per unit against the 150c projection. A short `how-to-run.md` beside it: the exact steps for the next full run.
4. Add the final-size rows to `results/speedup/ledger.md` as the baseline for all later levers.

## Touches
`results/final-run/` (new), `results/speedup/ledger.md`. The workflow only if a job fails for a reason the 183c build missed (then a fix brief).

## Acceptance criteria
- The merged file validates; headline outputs read and listed in the record (F1, M1 to M4 per point, O1e at the first point); anything that fails the manifest rules is reported with numbers, nothing loosened.
- Per-unit times recorded against the projection; the largest gap named.
- The record is enough for someone else to start the next full run without asking.

## Out of scope
`--final` (the author's act under the every-test rule); any model change; the SWF redesign.

## Open questions
For the author: the order proposed above, and whether this run counts as the first official run or as the baseline only.

## Implementation notes
<!-- progress:start -->
- **Done:**
- **Next:**
- **Resume:**
- **State:** draft
<!-- progress:end -->
