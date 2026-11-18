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
- **Done:** validator reads `line_horizons` (V7 expected cells per line; a cell at a horizon outside the line's own is a V7 error in every mode) and `run_fields_added` (known run fields; missing is a V8 error when final, a warning otherwise; `pack_country` must equal `run.country_pack`). Fixture maker follows; fixture regenerated with the three run fields.
- **Next:** guru records the rule in hooks.md 3.4.
- **Decisions:** an unexpected line cell also stops that cell counting toward coverage. Absent or empty `run_fields_added` behaves as before.
- **Gotchas:** the brief says OW3 loses 60 M15b cells and keeps 30; the fixture had 45 M15b cells (5 bands, 3 schedules, 3 horizons), now 15, so it lost 30. `build_metrics.py` prints its usual warnings; `registry/metrics.json` unchanged.
- **Resume:** `pytest tests/data -q`, `tests/gate`, `tests/model_v3`.
- **Not run:** none.
- **State:** done

```
Change report
- Task: 058c, validator and fixture follow line_horizons and run_fields_added
- Files changed: pipeline/validate_outputs.py; tests/data/make_fixture.py; tests/data/fixtures/outputs.fixture.json (regenerated); tests/data/test_validate_outputs.py (9 tests added); this brief
- What is different now: a complete final file with M15b at transition only passes V7; the three added run fields are known
- New or changed interfaces: none (Entry gains line_horizons)
- Acceptance criteria:
  - Fixture passes in --fixture mode, exit 0: met
  - Transition-only M15b complete and final passes V7; other-window cell fails V7 in every mode; missing transition cell fails when final: met (tests)
  - Final file lacking a run field fails V8, provisional warns: met (3 fields, tests)
  - pytest tests/data 84 passed (75 old + 9 new), tests/gate 17, tests/model_v3 108: met; no old test asserted the old behaviour, none changed
  - git diff --stat only Touches: met
- Deviations from the brief: cell counts in the brief (60 lost, 30 kept) differ from the fixture (30 lost, 15 kept)
- Risks / follow-ups: none
- Verification: the pytest runs above; build_metrics.py output unchanged
- Overview sections likely needing an update: none
- Commit / branch: brief/058-validator-line-horizons
```
<!-- progress:end -->
