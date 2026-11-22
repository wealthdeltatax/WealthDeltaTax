# 125: The household arm against the held 099r moments

- **Status:** ready
- **Author/date:** K. Ogata with the guru, 2026-11-22
- **Depends on:** 123c (merged); independent of 124c
- **Read (block 0: the first two only):** (1) `docs/research/099r-held-research-moments.md`; (2) `docs/agents/code.md`. Later, by block: `docs/research/data/099r/moments.csv` (the rows with `validation_moment_096r` set and `held_as_data` yes); `docs/model-v3/household-arm-account/account_table.py` and `model_v3/runner/arm.py` (`household_inputs`, `HouseholdHook.account`); `model_v3/core/cells.py` (`run_cell`, the untaxed cell baseline); `docs/model-v3/cell-baseline.md`.

## Goal
Compare what the household arm implies, untaxed and taxed, with the observed moments the research phase held (099r), so the author can see where the scenario values sit against data. A comparison, not a calibration: **no parameter is changed in this brief**.

## Decisions (author, 2026-11-22)
- Use only moments marked as held as data and as validation moments. A moment with no held data is listed as `not held` with what it would need (no invented value).
- For each moment, the model's analogue is computed on the **untaxed** cell baseline or the account at the three saving values and the mid regime (scenario axes, no central). Say which population and definition the moment has (`what_it_mixes`, `population`, `stage_definition`) and how the model's analogue differs from it; a mismatch of definition is reported as a mismatch, not adjusted.
- Saving by wealth gradient, pension withdrawal and per-path return regimes are known gaps; a moment that these would drive is marked as such and not forced.
- Result format per moment: observed, model range over the saving axis, the gap, and a plain label: `inside`, `outside`, `definition differs`, `not held`.

## Blocks (one push each; `docs/agents/code.md`, Long builds)
- **Block 0:** progress block pushed.
- **Block 1: the moment list.** `docs/model-v3/household-arm-validation/moments_map.csv`: one row per moment in `moments.csv` (id, held or not, validation moment yes or no, the model analogue and where it is computed, the definitions that differ). Push.
- **Block 2: the comparison.** `docs/model-v3/household-arm-validation/validate.py` and `comparison.csv` for the moments that are held and computable at the three saving values; tests for the script's helper functions on a toy case. Summary lines only on screen. Push.
- **Block 3: the note.** `docs/model-v3/household-arm-validation.md`: the table (observed, model range, gap, label); which scenario axes drive each gap; which gaps are definitional; what better data would resolve. No ruling and no tuning: the author reads it and decides. Change report; push; stop.
**Stop rule.** After three blocks, or a quarter of the budget left, push what exists and list the rest under Next. Suites in the background, never piped.

## Touches
`docs/model-v3/household-arm-validation/` (new), `docs/model-v3/household-arm-validation.md` (new), tests for the script, `docs/model-v3/architecture.md` (budget rows only). Not any model file, the register, the pack, or `moments.csv` (a wrong row is reported, not edited).

## Acceptance criteria
- `test_legacy_digest` and all suites pass; no model file changed.
- Every row of `moments.csv` is in `moments_map.csv` with a status; every comparison row names its observed value's source and the definitional differences.
- No parameter, register row or label is changed; any suggestion is written as a suggestion in the note.

## Out of scope
Calibration, new research, the comparators, a saving gradient, pension withdrawal, per-path regimes, UKDS data.

## Open questions
None the agent must resolve; a moment whose analogue is unclear is marked `definition differs` with the reason.

## Implementation notes
<!-- progress:start -->
- **Done:** blocks 0 to 3: `moments_map.csv` (33 rows), `validate.py`, `comparison.csv` (9 rows), `tests/model_v3/test_validate_125.py`, the note `docs/model-v3/household-arm-validation.md`.
- **Next:** none for this brief; see the note's Next (wealth by stage and a top-tail row in the pack).
- **Resume:** not needed.
- **State:** done; merged
<!-- progress:end -->

**Change report**
```
Change report
- Task: brief 125c, the household arm against the held 099r moments
- Files changed: docs/model-v3/household-arm-validation/ (make_map.py, moments_map.csv, validate.py, comparison.csv); docs/model-v3/household-arm-validation.md (the note); tests/model_v3/test_validate_125.py (helpers on a toy case, observed series)
- What is different now: a comparison of the untaxed cells at three saving values against the held moments, with a status for every 099r row
- New or changed interfaces: `python -I docs/model-v3/household-arm-validation/make_map.py` and `validate.py`
- Acceptance criteria: test_legacy_digest and all suites pass: met (10 of 10; model_v3 314 passed); no model file changed: met; every row of moments.csv in moments_map.csv with a status: met (33 rows); every comparison row names its observed source and the definitional differences: met; no parameter, register row or label changed, suggestions only in the note: met
- Deviations from the brief: none. Only one validation moment (BF-14) is also held, so the comparison is mostly consistency checks, said in the note; AB-04 is `not held` (its observed value is the paper's)
- Risks / follow-ups: the saving axis comes from the same ONS series as the observed ratio, so `inside` is by construction; BF-14's model number is the person share; needs wealth by stage and a top-tail row in the pack
- Instruction friction: none
- Verification: `python pipeline/run_suites.py` 10 of 10 passed; validate.py and make_map.py run; check_agent_docs run
- Overview sections likely needing an update: household-arm validation status
- Commit / branch: brief/125-validate-099r; brief 125 merged, ready to retire
```

