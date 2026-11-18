# 030: Code: data interface and output validator (site.md B2)

- **Status:** done, merged 2026-11-18 (guru fixed the manifest units; rulings in `docs/restructure/site/hooks.md`)
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
- **Done:** `build_inputs.py` (269 rows, 47 explicit null cells), `build_metrics.py` (43 metrics, cross-check against `outputs.yml`), `validate_outputs.py` (V1 to V12, `--final`, `--fixture`), `tests/data/make_fixture.py` and the fixture, 75 tests. Generated `registry/inputs.json` and `registry/metrics.json`.
- **Next:** the author answers the open questions below; the guru fixes the manifest and register findings; then merge (criterion 1 is partly met, so not merged).
- **Decisions:** cells of a `once_not_per_schedule` output omit `schedule`; a cell of an output with `lines` carries a `line` field; `checks` (CK1) are manifest ids in the data file; summary `point` is a value-only form; V11 implemented as written (every `by.year` vocabulary value has a cell); in `--fixture` mode a stale hash or manifest version is a warning, and `test_fixture_is_current` is the alarm; `build_metrics.py` writes the JSON and exits 1 when a unit disagrees; register unit text maps by a fixed table (`alpha` to `ratio`; `millions`, `year`, `real pounds` stay unmapped).
- **Gotchas:** `metrics.md` M7 has an unescaped `|` (`|C.1|`), rejoined by position (warning X10). Scripts are self-contained so they run under `python -I`; the tests load them by path.
- **Resume:** branch `brief/030-data-interface`, nothing uncommitted after the commit below. Rebuild with `python pipeline/build_inputs.py`, `python pipeline/build_metrics.py`, `python tests/data/make_fixture.py`; check with `pytest tests/data`.
- **Not run:** no local site build (nothing here is wired into the site build yet). No rebase onto a newer `origin/main` (not merging).
- **State:** pushed, NEEDS THE AUTHOR.
<!-- progress:end -->

### Change report
```
Change report
- Task: brief 030c, data interface and output validator (site.md B2)
- Files changed:
  - pipeline/build_inputs.py: parse the 269 register rows of inputs.md into registry/inputs.json
  - pipeline/build_metrics.py: parse metrics.md into registry/metrics.json; cross-check against outputs.yml
  - pipeline/validate_outputs.py: validate an output data file, rules V1 to V12, --final, --fixture
  - registry/inputs.json, registry/metrics.json: generated, never edited by hand
  - tests/data/make_fixture.py, tests/data/fixtures/outputs.fixture.json: fake-number fixture for every manifest id, run.fixture true
  - tests/data/conftest.py, test_build_inputs.py, test_build_metrics.py, test_validate_outputs.py: 75 tests
  - docs/briefs/030c-data-interface.md: progress block and this report
- What is different now: the register, metric register and output file have a fixed machine-readable shape, and a validator and a fixture exist for the resolver and figures to build on. Nothing in docs/model-v3/, source/ or site/ changed; nothing is wired into the site build.
- New or changed interfaces: python pipeline/build_inputs.py; python pipeline/build_metrics.py (exit 1 on a unit error); python pipeline/validate_outputs.py FILE [--final | --fixture]; python tests/data/make_fixture.py [--check]. Data file shape as hooks.md section 3, plus the cell field `line` (decisions above).
- Acceptance criteria:
  1. inputs.json has 269 entries: MET (269, no duplicate id, every row twelve cells). metrics.json agrees with outputs.yml: PARTLY MET. All metric ids, unit maps and unit tags agree. Three unit disagreements remain (error X05): O2 and the M2 line of OF1 declare `pct` while metrics.md gives M2 as "% per year"; the M15b line of OW3 inherits `pct` while metrics.md gives "% of GDP" (and transition only; the manifest says all three windows). I did not edit either file and did not map the units to hide the gap.
  2. Validator passes the fixture in fixture mode: MET (0 errors, 0 warnings). Fails it in final mode: MET (2 errors, V8: status provisional, run.fixture true). Reports every V rule it implements: MET (one line for each of V1 to V12 every run; each rule has a failing-input test, and mutating the validator makes the tests fail).
  3. The two findings are in this report: MET (below).
  4. git diff --stat shows only the Touches list: MET (11 new files, all under pipeline/, registry/, tests/data/, plus the brief).
- Deviations from the brief: none. `docs/brief-suggestions.md` is not appended, to keep the diff inside Touches; the findings below are the suggestions.
- Findings (do not edit outputs.yml; for the guru):
  1. hooks.md id regex O[A-Z]?[0-9]+[a-z]? matches none of DH1a, DH1b, DH1c, OH1b2, CK1 (five ids, not the three named: it needs an O prefix and allows one trailing letter).
  2. `by` is a list in OW2, OB1, OD1, OL1, OF1, OT1, and also in the check CK1: no vocabulary, so the validator cannot check those values or their coverage (the fixture uses v1, v2).
  3. Unit disagreements above (O2, OF1 line M2, OW3 line M15b).
  4. hooks.md gaps: no `line` key for cells of outputs with `lines` (O1, OW3, OB1, OR1, OD1, OM1, OF1); O1 and OM1 have no cell for their own net (M1, M9); summary `point` (DH1b, OH1b2) is not a form in section 3.3.
  5. metrics.md: unescaped `|` in the M7 row; no unit stated for M5, M6, M8, S1, P1, P3, P4, P5, P6 (warnings X06); O1 line M1d and OM1 line X have no register row; P2 is cited by no output.
  6. inputs.md: rows I-H2a1 to I-H2a10 cite SN1 and SN3, which are in no source table.
- Risks / follow-ups: the fixture embeds hashes of outputs.yml and inputs.json; when either changes, test_fixture_is_current fails until `python tests/data/make_fixture.py` is run. Cell-shape decisions (once_not_per_schedule, line) must be confirmed before the resolver brief relies on them.
- Verification: pytest tests/data: 75 passed. Both build scripts run twice under python -I: byte-identical (sha256 prefixes equal). Fixture: fixture mode PASS, final mode FAIL. Five deliberate validator mutations each failed the tests. Not run: site build (not wired in), rebase on origin/main.
- Overview sections likely needing an update: registry/ and pipeline/ file lists; the data-interface section of the site design.
- Commit / branch: see git log, brief/030-data-interface. NEEDS THE AUTHOR (not merged): criterion 1 is partly met and the questions below are open.
```

Questions for the author: (1) M2 and M15b units: change the manifest or the register? (2) Confirm the `line` cell field and that `once_not_per_schedule` cells omit `schedule`. (3) Are `checks` such as CK1 written to the output file?
