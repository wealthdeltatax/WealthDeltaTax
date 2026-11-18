# 056: Model v3 V3-11: output layer

- **Status:** ready
- **Author/date:** K. Ogata with the guru, 2026-11-18
- **Depends on:** 045, 046
- **Read:** `docs/model-v3/architecture.md` 2.9, 2.10 and 6.2 (W1 to W7); `docs/restructure/site/hooks.md` section 3 and the 030c rulings; `pipeline/validate_outputs.py` (V1 to V12); `docs/model-v3/outputs.yml` (after V3-0); `docs/model-v3/acceptance.md` V3-11 row.

## Goal
The only writer of `outputs.json`, built and tested against synthetic Samples before any model module exists.

## Decisions (author, 2026-11-18)
`architecture.md` approved (sections 8.1 and 9 as written); `acceptance.md` approved with Q1 to Q6 as proposed. v3 imports nothing from `model_v1/` or `model_v2/`. No file outside this brief's Touches is changed.

## Design
`out/assemble.py` (480 lines): one entry per manifest id over the full product of schedules, horizons and `by` vocabularies; summary forms `p10_mean_p90`, `point_and_range`, `point` and the level 2 form; P10 and P90 by `numpy.percentile` (linear), mean arithmetic, values in the manifest's unit. `out/writer.py` (220 lines): deterministic bytes, the `run` block and hashes (`inputs_sha256`, `manifest_sha256`, `pack_sha256`, `levers_sha256`), a non-finite value is an error in `final` and `null` in `provisional`; calls the validator after writing. Imports `interface`, the manifest, numpy, `json`, `hashlib`; not `core`, not `runner`.

**Shared interfaces, fixed before any stage starts** (a build brief never edits them; a mismatch is a question to the guru): the output file shape is `schema wdt-outputs/1` as `pipeline/validate_outputs.py` checks it and `docs/restructure/site/hooks.md` section 3 with the 030c rulings; the country pack format is `docs/model-v3/country-pack.md`; the id lists are `docs/model-v3/outputs.yml` and the module-to-id table of `architecture.md` 2.10; the Samples contract is `architecture.md` 2.9; the layers and import rules are `architecture.md` 5.1.

This is build stage V3-11 of `architecture.md` section 7. One session, one lane; the stage ends in a stop: tests pass, change report written, branch merged by the auto-merge rule. The stage's files are budgeted in `architecture.md` 6.1; a stage more than 15% over its budget reports it before the next starts.

## Touches
`model_v3/out/assemble.py`, `model_v3/out/writer.py`, `tests/model_v3/test_out.py`, this brief's progress block.

## Acceptance criteria
- W1 to W7 pass; each of V1 to V12 has a failing input the validator rejects.
- W7: the module-to-id table covers `outputs.yml` exactly (39 outputs and one check).
- `assemble.py` at most 480 lines and `writer.py` at most 220; `out/` is smaller than core plus runner (checked when all exist).
- `git diff --stat` is limited to the Touches list.

## Checks to run
`pytest tests/model_v3 tests/data -q`.

## Out of scope
Any model code; computing a metric.

## Open questions
Ask if the 030c file shape and the architecture disagree; the validator wins.

## Implementation notes
<!-- progress:start -->
- **Done:**
- **Next:**
- **Decisions:**
- **Gotchas:**
- **Resume:**
- **Not run:**
- **State:** draft; not started
<!-- progress:end -->
