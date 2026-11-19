# 060: Code: hook resolver (site.md B3)

- **Status:** ready
- **Author/date:** K. Ogata with the guru, 2026-11-18
- **Depends on:** none (B1 029s and B2 030c are merged; 032r and 043r supply the sidecars)
- **Read:** `docs/restructure/site/hooks.md` sections 1, 2, 4, 6 and the two "Guru rulings, 2026-11-18" blocks at its end; `docs/restructure/template.md` section 4 (hook grammar and the front matter `defaults`); `docs/model-v3/outputs.yml` (header, `unit_tags`, `line_horizons`, `by`); `pipeline/validate_outputs.py` (`load_entries`, `Entry`, `sha256_file`, V8); `pipeline/build_inputs.py` (how `registry/inputs-display.yml` is merged into `registry/inputs.json`); `registry/lit-figures.yml` (header and three entries); `docs/agents/code.md`.

## Goal
A resolver that expands `{{o:}}`, `{{i:}}`, `{{ref:}}` and `{{lit:}}` hooks in a spoke's text into formatted numbers, or into placeholders in a draft build, with every error code of `hooks.md` 4.7 and a `hooks-report.json`, tested on the fixture data file so spokes can be written against it as soon as the data gate opens.

## Decisions (author, 2026-11-18)
- `site.md` is approved; all build briefs work on fixtures and deliver without the model data. The data gate holds: no spoke or hub prose is written here.
- Units, rounding and wording come from the manifest and the register, never from the author (template section 4).
- `unit` tags the resolver formats: the ten of `outputs.yml` `unit_tags` plus the eight input-only tags accepted in the 032r ruling (`pp_per_year`, `usd_bn`, `gbp`, `gbp_m`, `gbp_k`, `coefficient`, `correlation`, `text`). `text` is never numeric: a hook on a `text` row is error H23.
- Id pattern of `hooks.md` 3.4 is wrong (030c ruling 3). This brief fixes it for hooks: the `o` id pattern must match every manifest id (DH1a to c, OH1b2, CK1 and the rest); build it from the manifest ids, not from a regex of the shape `O[A-Z]?[0-9]+[a-z]?`.
- `registry/references.bib` lacks ten keys that `lit-figures.yml` proposes (043r). H42 fires on them in the real registry; that is correct and expected. Tests use a small fixture bibliography.

## Design
Two modules, no side effects on import, numpy not needed.

1. **`pipeline/hook_format.py` (about 150 lines).** `format_value(value, unit, decimals)` and `format_range(lo, hi, unit, decimals)` per `hooks.md` 4.6: decimal half-up on the stored number's decimal representation (`Decimal(str(x))`, `0.125` at two decimals gives `0.13`), bands of a range rounded separately; a range whose ends round to the same string renders once and returns warning W2; negative values with a hyphen-minus; the unit once at the end of a range, `£` leading and `bn` trailing for `gbp_bn`; the placeholder renderer `placeholder(id, stat, schedule, horizon, by)` (fully expanded with defaults, `#KEY:VALUE` only for keys not `overall`). All 18 unit tags are one table, so an unknown tag is a single error.
2. **`pipeline/hooks.py` (about 330 lines).** Self-contained so it runs under `python -I`; it loads `pipeline/validate_outputs.py` and `hook_format.py` by path (as the 030c tests do), it does not import `preprocess.py`.
   - Parse: the grammar of 4.1 (`.` `@` `/` `#`); hooks are found in text outside code spans and fenced blocks and are not allowed in a figure caption; any text with `{{` that matches no form is H01. The `by` field takes several `key:value` pairs and the bare `#overall` form.
   - Resolve `{{o:}}` in the nine steps of 4.2, `{{i:}}` per 4.3 (statistics `central`, `low`, `high`, `range`; display spec from the merged `inputs.json`), `{{ref:}}` per 4.4 (`^fig-(S...)` replaced by the shortcode form: the spoke shortcode is the id, `fig-<SHORTCODE>-<n>`), `{{lit:}}` per 4.5 (`<bibkey>:<slug>`, `value`, `unit`, `decimals`, `verified`). H32 and R1r need the spoke checker's view of the whole file; the resolver implements them as functions `check_f4(text)` and `check_r1_reverse(spokes)` that B6 calls; the resolver's own run reports them.
   - Front matter: `spoke:` (the shortcode), `defaults: {schedule, horizon}`, `outputs:`. A hook with no schedule or horizon and no default is H09; an output with `once_not_per_schedule` takes no schedule and a hook that gives one is H04.
   - A cell is found by key `(schedule, horizon, line, by)`: see the open question on lines.
   - Modes by `WDT_MODE=draft|release` (default `draft`), `hooks.md` section 6: H11, H12 and H41 give the placeholder in draft and an error in release; every other code fails in both; reverse R1 is a warning in draft and an error in release; in release the data file must have `run.status` `final` (error code H13 with the validator's message when not) and V7 and V9 findings become errors.
   - Data file checks run by calling the validator's `validate`, not by copying it. A fixture file (`run.fixture: true`) is accepted only with `--fixture`; the draft build never reads a fixture as real data unless that flag is given.
   - Word counting: one hook counts as one word before resolution and an unresolved placeholder counts the same (function `count_words(text)`; B6 uses it).
   - CLI: `python pipeline/hooks.py resolve <spoke.md> --data <file> [--fixture] [--out <file>]` writes the resolved text; `python pipeline/hooks.py validate <file>` calls the validator; `python pipeline/hooks.py report <spoke.md ...>` writes `_build/hooks-report.json` (counts by outcome; unresolved list with file and line; warnings; the mode). Exit status non-zero on any error in the mode.
   - `hooks-report.json` schema: `{"schema": "wdt-hooks-report/1", "mode", "data_status", "counts": {"resolved", "placeholder", "error"}, "unresolved": [{"file","line","hook","code"}], "errors": [...], "warnings": [...]}`; its writing is byte-reproducible (sorted keys, no timestamps).
3. **Tests, `tests/hooks/` (about 520 lines in five files).** One test per error code H01 to H13, H20 to H23, H30 to H32, H40 to H42, R1r and A2 (28 tests), each built from a three-line spoke text and the fixture, plus: formatting for all 18 unit tags and the range cases; half-up on `0.125`; W2; the placeholder example of 4.6 (`[[O2.mean@S_central/short]]`); a hook in a code span and in a fenced block is ignored; a hook in a caption is an error; the ids that the old regex missed (DH1a, CK1, OH1b2) resolve; draft against release for the same input; `hooks-report.json` byte-identical on two runs; the real registry loads (`inputs.json` 274 rows, `lit-figures.yml` 67 entries). Fixtures in `tests/hooks/fixtures/` (a small `references.bib`, two spoke texts). The tests run on `tests/data/fixtures/outputs.fixture.json`, never on `outputs.json`.

## Touches
`pipeline/hooks.py`, `pipeline/hook_format.py`, `tests/hooks/` (new folder, including `fixtures/`), this brief's progress block. None of these exist yet. Nothing in `pipeline/preprocess.py` (B15 wires the resolver in), `pipeline/validate_outputs.py` (the model lane's brief 058c edits it; read only), `registry/`, `docs/model-v3/`, `source/`, `site/`. If a registry or manifest fact has to change, stop and report it to the guru.

## Acceptance criteria
- Every code of `hooks.md` 4.7 is implemented and has a named test; the test count is stated in the change report.
- `python pipeline/hooks.py resolve` on the two fixture spokes under `WDT_MODE=draft` gives placeholders for hooks to a missing cell and the formatted number for the rest; the same file under `release` exits non-zero on every placeholder.
- `python pipeline/hooks.py report` writes `hooks-report.json` byte-identical on two runs.
- `pytest tests/hooks -q`, `pytest tests/data -q`, `pytest tests/gate -q` and `pytest tests/model_v3 -q` pass (run as separate commands: the `conftest.py` files clash in one session).
- `git diff --stat` shows only the Touches list. Line budgets: `hooks.py` at most 330, `hook_format.py` at most 150, tests at most 520; over by more than 15% means report before finishing.

## Checks to run
The four pytest commands; both modes on the fixture spokes; an import check with `python -I` (`sys.path.insert(0, '.')` first, as in `code.md`). No site build: nothing here is wired into the site (B15).

## Out of scope
Wiring into `preprocess.py` or the workflow, the Data block generator and figure renderer (B4, B5), the spoke checker (B6; this brief only exports the functions above), editing `outputs.yml`, `inputs.md`, `inputs-display.yml`, `lit-figures.yml` or `references.bib`, spoke prose, the references rework. Stop with NEEDS THE AUTHOR if a criterion cannot be met or `source/` would be touched.

## Shared interfaces, fixed before any stage starts
A build brief never edits them; a mismatch is a question to the guru: the output file shape is `schema wdt-outputs/1` as `pipeline/validate_outputs.py` checks it and `docs/restructure/site/hooks.md` section 3 with the 030c rulings; the country pack format is `docs/model-v3/country-pack.md`; the id lists are `docs/model-v3/outputs.yml` and the module-to-id table of `architecture.md` 2.10; the Samples contract is `architecture.md` 2.9; the layers and import rules are `architecture.md` 5.1.

## Standing rules
One session, one lane; the brief ends in a stop: tests pass, change report written, branch merged by the auto-merge rule. No `__init__.py` is added anywhere (the pipeline scripts are loaded by path). Commit messages end with `Co-Authored-By: Claude Sonnet 5.5 <noreply@anthropic.com>` and the `Claude-Session:` trailer.

## Open questions
The implementer asks the guru rather than guessing on these.
1. **Lines.** A cell of an output with `lines` (O1, OM1, OW3 and others) carries a `line` field, but the hook grammar has no line selector. Proposed: add `:LINE` after the id in the `o` hook, `{{o:O1:M1.mean@S_central/short}}`, required for an output with lines (error H08 when missing); if the author or guru prefers another form the grammar changes before the build.
2. **`once_not_per_schedule` outputs.** Cells omit `schedule`; proposed that a hook with an `@SCHEDULE` on such an output is H04 and the default schedule is ignored.
3. **`series` and form C (`level2`).** Hookable? Proposed not in this brief: `.series` and `level2` hooks are H03, and the guru decides with B4 and B5.
4. **Figure id.** `hooks.md` 4.4 writes `fig-S5-1`; ids are now shortcodes (`ids-map.md`). Proposed `fig-<SHORTCODE>-<n>`, matching `F-<spoke>-<n>` of the template.

## Guru rulings, 2026-11-18
Hook line selector `{{o:O1:M1.mean...}}` with H08 when it is missing: accepted. `@SCHEDULE` on a `once_not_per_schedule` output is H04: accepted. `series` and `level2` hooks return H03 until a page needs them: accepted. Figure ids are `fig-<SHORTCODE>-<n>`: accepted. The id regex of `hooks.md` 3.4 is corrected by building the pattern from the manifest ids; the guru edits `hooks.md` afterwards. H42 failing on the ten proposed bib keys is expected: report it, do not work around it.

## Implementation notes
<!-- progress:start -->
- **Done:** `pipeline/hook_format.py` (78 lines) and `pipeline/hooks.py` (366 lines): grammar with `:LINE`, 4.2 nine steps, `i`, `ref`, `lit`, modes by `WDT_MODE`, `check_f4`, `check_r1_reverse`, `check_a2`, `count_words`, CLI resolve, validate, report. Tests in `tests/hooks/` (five files, 403 lines, 64 tests).
- **Next:** B15 wires it into `preprocess.py`; B6 calls `check_f4`, `check_r1_reverse`, `count_words`.
- **Decisions:** the hook is parsed with a generic id and the id is checked against the manifest (H02), so an unknown id is H02 and not H01; the effect is the ruling's (pattern from manifest ids). `inputs.json` does not carry the display spec (the brief says merged), so the resolver reads `row["display"]` if present and else `registry/inputs-display.yml`. Release with `--fixture` validates in fixture mode (so the resolver itself can be tested; V7 and V9 stay warnings there) and every placeholder is still an error. A figure is cited if at least one citing sentence holds an `o` hook (lenient). Hub front matter `spoke: HUB` accepts outputs whose element is H0 to H7. Extra code F1 for a hook in a caption.
- **Gotchas:** (1) CK1 cannot be hooked: its `unit` and `decimals` are maps over P1, P3, P7b but the entry has no `lines` and its cells carry no metric, so the resolver returns H13. Needs a manifest decision (add `lines` or a selector). (2) H42 fires on 10 bib keys, 46 of 67 lit keys: AdamEtAl2025, AdvaniBanghamLeslie2021, AdvaniSummersTarrant2025, AdvaniTarrant2021, BesleyEtAl2014, BestKleven2018, BroomeKanabar2025, FuestEtAl2017, KosterPinchbeck2018, TippetZucman2026 (expected per ruling). (3) `registry/references.bib` is read with a regex for `@type{key,`; the tests use `tests/hooks/fixtures/references.bib`.
- **Resume:** `pytest tests/hooks -q` (separate command from the other suites).
- **Not run:** no site build (not wired).
- **State:** done

```
Change report
- Task: 060c, hook resolver and number formatter
- Files changed: pipeline/hooks.py, pipeline/hook_format.py (new); tests/hooks/ (conftest, 4 test files, fixtures: pay.md, fisc.md, references.bib); this brief
- What is different now: hooks resolve to formatted numbers or placeholders, with the checks B6 needs exported
- New or changed interfaces: CLI `hooks.py resolve|validate|report`; functions format_value, format_range, placeholder, check_f4, check_r1_reverse, check_a2, count_words
- Acceptance criteria:
  - Every code of 4.7 implemented and tested: met. 26 named code tests (the brief says 28; 4.7 has 25 codes: H01 to H13, H20 to H23, H30 to H32, H40 to H42, plus R1r and A2, plus F1), 64 tests in all
  - resolve on both fixture spokes in draft: placeholder for a missing cell, number for the rest; release exits non-zero on every placeholder: met (test_cli)
  - report byte-identical on two runs: met
  - pytest tests/hooks 64, tests/data 84, tests/gate 17, tests/model_v3 108: pass, run separately
  - git diff --stat only Touches: met
  - Line budgets: hook_format 78 (max 150), tests 403 (max 520), hooks.py 366 (max 330, +11%, inside the 15% allowance)
- Deviations from the brief: display spec read from inputs-display.yml because inputs.json has none; id check by membership (see Decisions)
- Risks / follow-ups: CK1 unhookable (Gotchas 1); H42 on 10 bib keys (Gotchas 2); hooks.md 3.4 id regex to be corrected by the guru
- Verification: four pytest suites, both modes on both fixture spokes, python -I import check
- Overview sections likely needing an update: none
- Commit / branch: brief/060-hook-resolver
```
<!-- progress:end -->
