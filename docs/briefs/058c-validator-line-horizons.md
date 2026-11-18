# 058: The validator and fixture read `line_horizons` and the added run fields

- **Status:** ready
- **Author/date:** K. Ogata with the guru, 2026-11-18
- **Depends on:** none (045g and 056c are merged)
- **Read:** `docs/brief-suggestions.md` (entry "Validator and fixture ignore `line_horizons`"); `docs/model-v3/outputs.yml` (header `run_fields_added`, OW3 `line_horizons`); `pipeline/validate_outputs.py` (`load_entries`, V7, V8, V12); `tests/data/make_fixture.py`; `docs/restructure/site/hooks.md` 3.4 and 4.6 (read only).

## Goal
A complete `--final` model file passes the validator: coverage (V7) counts a line only at its own horizons, and the run fields `pack_sha256`, `pack_country` and `levers_sha256` are known fields, so no complete file is rejected for the shape the manifest now describes.

## Decisions (author, 2026-11-18)
- Manifest is the contract: `line_horizons` (OW3 M15b: transition only) and `run_fields_added` are right; the validator and fixture follow the manifest, not the reverse.
- `horizons` stays the union of all windows an output uses (045g decision).

## Design
- **V7:** the expected cells of an entry are the product of schedule, horizon, line and `by` combinations, with a line's horizons taken from `line_horizons[line]` where given and otherwise the entry's `horizons`. A cell present for a line at a horizon outside its `line_horizons` is an error in every mode (unexpected cell), not only when final.
- **V8 and V12:** the names in the manifest's `run_fields_added` are known run fields (no V12 warning); in final mode a missing one is a V8 error, in provisional mode a warning. `pack_country` must equal `run.country_pack`; the validator checks that and nothing else about them.
- **Fixture:** `tests/data/make_fixture.py` follows the same rule; regenerate `tests/data/fixtures/outputs.fixture.json` (OW3 loses its 60 M15b cells outside transition; it then holds 30) and give it the three run fields.
- No change to `outputs.yml`, `metrics.json`, or hooks.md (the guru records the rule in hooks.md 3.4 afterwards).

## Touches
`pipeline/validate_outputs.py`, `tests/data/make_fixture.py`, `tests/data/fixtures/outputs.fixture.json`, `tests/data/test_validate_outputs.py`, this brief's progress block.

## Acceptance criteria
- `python pipeline/validate_outputs.py tests/data/fixtures/outputs.fixture.json --fixture` exits 0.
- A test builds a file from the fixture with a transition-only M15b line complete and `run.status` final: V7 passes; the same file with one M15b cell for another window fails V7 in every mode; with one transition cell missing fails V7 when final.
- A final file lacking any of the three run fields fails V8; a provisional one warns.
- `pytest tests/data -q`, `pytest tests/gate -q` and `pytest tests/model_v3 -q` pass (separate commands); the 75 existing data tests keep passing except tests that assert the old behaviour, each changed one named in the report.
- `git diff --stat` limited to the Touches list.

## Checks to run
The commands above, and `python pipeline/build_metrics.py` (unchanged output).

## Out of scope
The model code, `outputs.yml`, `hooks.md`, the site build, any new validator rule beyond V7, V8 and V12 behaviour above.

## Open questions
None. If `run_fields_added` is empty or missing in a manifest, the validator behaves as today.

## Implementation notes
<!-- progress:start -->
- **Done:**
- **Next:**
- **Decisions:**
- **Gotchas:**
- **Resume:**
- **Not run:**
- **State:** ready; not started
<!-- progress:end -->
