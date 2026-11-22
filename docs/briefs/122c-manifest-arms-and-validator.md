# 122: Manifest `arms`, the validator, and the tornado head under the household arm

- **Status:** ready
- **Author/date:** K. Ogata with the guru, 2026-11-22
- **Depends on:** 121c (merged)
- **Read (block 0: the first two only):** (1) `docs/model-v3/household-arm-outputs.md` (the proposed manifest amendment and the OT1 row); (2) `docs/agents/code.md`. Later: `docs/model-v3/outputs.yml`; `pipeline/validate_outputs.py` (`ENTRY_FIELDS`, V7, V12); `docs/restructure/site/hooks.md` section 3.4 (V1 to V12); `model_v3/runner/sweeps.py` (the M3 head, line ~81); `tests/data/test_validate_outputs.py`.

## Goal
Make a household-arm output file valid. The author signed off the amendment of 121c (2026-11-22): the six withheld ids carry `arms: [legacy]` in the manifest, and the validator accepts a withheld entry under the household arm and still rejects it otherwise.

## Decisions (author, 2026-11-22)
- `outputs.yml`: add `arms: [legacy]` to O3, OH1b, OH1c, OW1, OW3 and OM1 and nothing else; bump the manifest `version`.
- Validator: add `withheld` to `ENTRY_FIELDS` and `arm` to the run block's known fields (so V12 stops warning). V7: an entry with `arms: [legacy]`, `withheld: legacy_only` and empty `cells` is covered when the run's `arm` is `household`; the same entry under a legacy or missing arm is an error; a household-arm file with a value under a withheld id is an error.
- OT1 (the tornado) under the household arm: the M3 head is **withheld and labelled**, not computed with a legacy `c`; the other heads run. No new numbers are shown to the author.

## Blocks (one push each)
- **Block 0:** progress block pushed.
- **Block 1: manifest and validator.** The `outputs.yml` edit and the validator change above, with the failing-input tests the acceptance table (V3-11) requires for each rule changed (a household file with the withheld ids empty passes; a legacy file with an `arms: [legacy]` id empty fails V7; a value under a withheld id fails). Update the gate's pinned counts and the fixtures that depend on the manifest version, as 119c did for a register row; report each file touched. Push.
- **Block 2: OT1 and the check.** The tornado's M3 head withheld under the household arm (`sweeps.py`); a smoke run of `assemble` under the household arm validated with `validate_outputs.py --final` on a small run file; summary lines only. Change report; push; stop.
**Stop rule.** After two blocks, or a quarter of the budget left, push what exists and list the rest under Next. Suites in the background, never piped.

## Touches
`docs/model-v3/outputs.yml`, `pipeline/validate_outputs.py`, `model_v3/runner/sweeps.py`, tests (`tests/data/test_validate_outputs.py`, `tests/model_v3/test_arm_switch.py`), generated fixtures and pins that the manifest version changes (report each), `docs/model-v3/household-arm-outputs.md` (mark the amendment applied), `docs/model-v3/architecture.md` (budget rows only). Name any further file before editing it. Not the kernel, `revenue.py`, `burden.py`, the register or the pack.

## Acceptance criteria
- `test_legacy_digest` and every suite pass (including `check_gate`/data suites that pin the manifest).
- The validator behaviours above each have a failing-input test.
- A household-arm file with the six ids withheld passes `--final`; the same file labelled legacy fails V7.
- OT1 under the household arm does not raise and carries the withheld M3 head.

## Checks to run
`test_legacy_digest`; the data, gate and model_v3 suites in the background; `python -I pipeline/check_agent_docs.py`.

## Out of scope
The comparators on the account (M3, M12, M13, M15, M9), the `fl` horizon fix (123c), any number reviewed by the author.

## Implementation notes
<!-- progress:start -->
- **Done:** none
- **Next:** block 0
- **Resume:** `git fetch origin '+refs/heads/*:refs/remotes/origin/*' && git checkout -B brief/122-manifest-arms origin/brief/122-manifest-arms`
- **State:** ready; not started
<!-- progress:end -->
