# 030: Code: data interface and output validator (site.md B2)

- **Status:** ready
- **Author/date:** K. Ogata with the guru, 2026-11-17
- **Depends on:** none
- **Read:** `docs/restructure/site/hooks.md` sections 1 to 4, 9; `docs/model-v3/outputs.yml`, `metrics.md` (headers), `inputs.md` (row format and header only); `docs/agents/code.md`.

## Goal
Turn the register and the metric register into machine-readable files, and write the validator for the output data file, so the resolver, figures and checker can read data that has a fixed shape, using a fixture until the model exists.

## Decisions (author, 2026-11-17)
`docs/restructure/site.md` is approved with its eight answers (drafts under `/draft/`, hub Data block, ADOPT, PILOT and HYPO reached from their parents, `source/hub.md`, pending-page links rewritten to `retired.html`, glossary seeding before the gate, standalones move after the gate). The data gate holds: no spoke or hub prose. This brief builds on fixtures and delivers without the model data. It is one of the first parallel set (029s, 030c, 031s, 032r, 033c, 034c); the Touches lists do not overlap.

## Design
1. `pipeline/build_inputs.py`: parse the 269 rows of `inputs.md` into `registry/inputs.json` (id, input, unit, low, central, high, source ids, `(J)` flag, coverage); fail on a row with other than twelve cells or a duplicate id; keep `not found` and bracket cells as explicit nulls with a reason.
2. `pipeline/build_metrics.py`: parse `metrics.md` into `registry/metrics.json` (id, name, unit tag, horizon rule) and cross-check against `outputs.yml` (`metric:` and `unit:` agree).
3. `pipeline/validate_outputs.py`: validate an output data file against `outputs.yml` and the schema of `hooks.md` section 3, rules V1 to V12, with V7, V9 and V11 as errors in final mode. Flags: `--final`, `--fixture`. Findings: `hooks.md` id regex misses DH1a, CK1 and OH1b2 (site.md R12), and six outputs still carry `by` as a list (OW2, OB1, OD1, OL1, OF1, OT1): report both in the change report; do not edit `outputs.yml`.
4. A fixture data file `tests/data/fixtures/outputs.fixture.json` covering every manifest output with fake numbers and `run.fixture: true`, a final-mode failure test, and tests in `tests/data/`.

## Touches
`pipeline/build_inputs.py`, `pipeline/build_metrics.py`, `pipeline/validate_outputs.py`, `registry/inputs.json`, `registry/metrics.json` (generated files), `tests/data/`, this brief's progress block. Nothing in `docs/model-v3/`, `source/`, `site/`.

## Acceptance criteria
- `inputs.json` has 269 entries and `metrics.json` agrees with `outputs.yml`.
- The validator passes the fixture in fixture mode, fails it in final mode, and reports every V rule it implements.
- The two findings above are in the change report.
- `git diff --stat` shows only the Touches list.

## Checks to run
`pytest tests/data`; run both build scripts twice and confirm the output is byte-identical; run with `python -I` where the script reads untrusted files.

## Out of scope
The resolver (next brief), figures, the model, editing the register or manifest.

## Open questions
The implementer asks rather than guesses.

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
