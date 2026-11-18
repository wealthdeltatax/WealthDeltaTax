# 045: Model v3 V3-0: manifest amendments and levers file

- **Status:** draft (ready when the author approves 040g D2)
- **Author/date:** K. Ogata with the guru, 2026-11-18
- **Depends on:** none (architecture approved 2026-11-18)
- **Read:** `docs/model-v3/architecture.md` sections 3.3 and 8.1; `docs/model-v3/outputs.yml`; `docs/model-v3/metrics.md`; `docs/model-v3/stage-c-decisions.md`; `docs/restructure/site/hooks.md` (the 030c rulings); `tests/data/make_fixture.py`.

## Goal
The manifest carries the vocabularies and fields the model and the writer need, and `levers.json` holds the schedule grid, so every later stage reads one settled contract.

## Decisions (author, 2026-11-18)
`architecture.md` approved (sections 8.1 and 9 as written); `acceptance.md` approved with Q1 to Q6 as proposed. v3 imports nothing from `model_v1/` or `model_v2/`. No file outside this brief's Touches is changed.

## Design
Apply amendments A1 to A7 of `architecture.md` 8.1 to `outputs.yml` and `metrics.md`: `by` becomes a map `dimension: [values]` for the six list-valued outputs (OW2, OB1, OD1, OL1, OF1, OT1) and CK1; line-level horizons (A3); cells for the nets of O1 and OM1 (A4); feasibility constants as manifest fields (A5); the `run.pack_sha256` and `run.levers_sha256` fields for G2 (A6, a note in the manifest header; the validator edit belongs to the resolver work and is not made here); A7 is a check only: every id in the manifest must match `[A-Z]{1,2}[0-9]+[a-z]?[0-9]?`. Write `model_v3/levers.json` with the grid of `architecture.md` 3.3 (`tau_m` 0.5, 0.7, 0.9; `k_ln` 0.5, 1, 2; `tau_0` 0.04; threshold ratio 0.25, 0.5, 1.0; the retirement order). Bump `version`. Regenerate `registry/metrics.json` with `pipeline/build_metrics.py` and the fixture with `tests/data/make_fixture.py`.

**Shared interfaces, fixed before any stage starts** (a build brief never edits them; a mismatch is a question to the guru): the output file shape is `schema wdt-outputs/1` as `pipeline/validate_outputs.py` checks it and `docs/restructure/site/hooks.md` section 3 with the 030c rulings; the country pack format is `docs/model-v3/country-pack.md`; the id lists are `docs/model-v3/outputs.yml` and the module-to-id table of `architecture.md` 2.10; the Samples contract is `architecture.md` 2.9; the layers and import rules are `architecture.md` 5.1.

This is build stage V3-0 of `architecture.md` section 7. One session, one lane; the stage ends in a stop: tests pass, change report written, branch merged by the auto-merge rule. The stage's files are budgeted in `architecture.md` 6.1; a stage more than 15% over its budget reports it before the next starts.

## Touches
`docs/model-v3/outputs.yml`, `docs/model-v3/metrics.md`, `model_v3/levers.json`, `registry/metrics.json`, `tests/data/fixtures/`, this brief's progress block.

## Acceptance criteria
- `outputs.yml` carries A1 to A7 and a new `version`; a script finds no list-valued `by`.
- `model_v3/levers.json` parses and holds every axis named above; the named schedules S_low, S_central and S_high are not typed in it.
- `python pipeline/build_metrics.py` exits 0; `python pipeline/validate_outputs.py <fixture> --fixture` exits 0; `pytest tests/data -q` passes.
- Every manifest id matches the A7 pattern; every output has a non-empty `element:` (script).
- `git diff --stat` is limited to the Touches list.

## Checks to run
`pytest tests/data tests/gate -q`; the two scripts of the criteria. No model code is run. `registry/` is touched, so also run the local site build of AGENTS.md or say why it is skipped.

## Out of scope
Model code; the validator and resolver (they read the new manifest later); changing any metric definition.

## Open questions
Ask before changing a vocabulary value proposed in A1 or A2.

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
