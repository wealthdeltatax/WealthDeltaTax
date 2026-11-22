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
- **Done:** block 0; block 1 (`moments_map.csv`: 33 rows; held yes 5, partly 4, no 24; validation moments 10; only BF-14 is both held and a validation moment; computable 5, definition differs 3, not held 25); block 2 (`validate.py`, `comparison.csv` 9 rows, `tests/model_v3/test_validate_125.py`; budget and rule tests pass).
- **Next:** block 3: the note `docs/model-v3/household-arm-validation.md`, suites in the background, check_agent_docs, change report, push.
- **Decisions:** AB-04 `not held` (its 1.4tn to 2.3tn is the paper's); BF-12, EER-01, TZ-01 `definition differs` (no analogue). BF-11, BF-13, BF-14 labelled `definition differs` with numbers shown; GB-01 and BF-15 compared with the held annual DGD8 (2019, 2020, 2022, 2024, 2025).
- **Gotchas:** the saving axis is built from the same ONS series as the observed ratio, so `inside` is by construction; the retired wealth share is the person share (stage split by person share).
- **Resume:** `git fetch origin '+refs/heads/*:refs/remotes/origin/*' && git checkout -B brief/125-validate-099r origin/brief/125-validate-099r`; last block pushed: 2.
- **Not run:** block 3, suites.
- **State:** in progress; block 2 pushed
<!-- progress:end -->
