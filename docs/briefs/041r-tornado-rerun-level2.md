# 041: Research: rerun the tier 1 tornado with the level 2 return band

- **Status:** ready
- **Author/date:** K. Ogata with the guru, 2026-11-18
- **Depends on:** 036r merged (done); 035g items 1 and 4 decided
- **Read:** `docs/model-v3/tornado.md` and `docs/model-v3/tornado/` (scripts and CSV); `docs/model-v3/returns-method.md` sections 1, 4 and 5; `docs/model-v3/stage-c-decisions.md` items 1 and 4; `docs/model-v3/inputs.md` rows I-D1a to I-D1g (now 274 rows); `docs/agents/research.md`.

## Goal
Correct the tornado: its return swing double counted level 1 return risk as parameter ignorance, and it used the geometric mean. Rerun it with the level 2 band on the arithmetic mean, so the ranking of inputs is the one stage C builds on.

## Decisions (author, 2026-11-18)
- The identity check and the generator use the arithmetic mean (4.742%); the level 2 band for the true mean is 3.41% to 6.07% (I-D1a); the SD band 7.47% to 8.96% (I-D1b); the lag-1 band 0.19 to 0.42 (I-D1b2); the level 1 spread of 30-year means (I-D1a0) is not a parameter range and leaves the tornado.
- Retired receipts are 8.11% of GDP; the revenue identity is a check, epsilon is computed by the model (item 3).
- No stock-wealth floor; no model run.

## Design
Rerun `tornado/tornado.py` (copy to a new version; keep the original) with: I-D1a at its level 2 band; the SD and lag-1 rows added where the identity can reach them (state where it cannot); the swing for the return recomputed (expected about 4.1 to 4.4 points of GDP per `returns-method.md`); the epsilon back-out redone at the arithmetic mean (7.34% at 4.74% gives epsilon about 29.97% held, or about 31% recalibrated, state both); the break-even mean return (zero crossing of M1) at the arithmetic mean, with the probability from level 2 alone; ranking and the 0.5 point tier 2 cut-off re-applied. Write a new `tornado.md` section 'Rerun 2026-11-18' and keep the old tables, marked superseded for I-D1a. Record each change from the first run in one table.

## Touches
`docs/model-v3/tornado.md` (new section and superseded marks), `docs/model-v3/tornado/` (new files), this brief's progress block. Nothing in `inputs.md`, `drivers.md`, `metrics.md`, `outputs.yml`, `source/`, `pipeline/`.

## Acceptance criteria
- The I-D1a swing is the level 2 band on the arithmetic mean and the old row is marked superseded.
- The ranking of inputs is restated with the table of changes.
- The break-even return and its level 2 probability are shown with the arithmetic.
- Every number traces to a register row id; a number that does not is labelled assumption.
- `git diff --stat` shows only the Touches list.

## Checks to run
Recompute the central M1 and two swings by a second method; script runs with `python -I`.

## Out of scope
Choosing values, editing the register, model runs, the stock-wealth floor.

## Open questions
Ask rather than guess.

## Implementation notes
<!-- progress:start -->
- **Done:**
- **Next:**
- **Decisions:**
- **Gotchas:**
- **Resume:**
- **Not run:**
- **State:**
<!-- progress:end -->
