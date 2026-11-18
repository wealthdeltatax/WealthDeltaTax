# 033: Code: spoke gate checker (order.md B17)

- **Status:** ready
- **Author/date:** K. Ogata with the guru, 2026-11-17
- **Depends on:** 029s and 030c for real inputs (soft: build against the formats in the Read files and fixtures; wire to the real files when they land)
- **Read:** `docs/restructure/order.md` sections 4 and 6.5; `docs/restructure/site.md` sections 3 and 6; `docs/restructure/site/hooks.md` section 9 (run metadata); `docs/model-v3/outputs.yml`; `docs/model-v3/inputs.md` (the `(J)` flag); `docs/model-v3/judgement-decisions.md`; `docs/agents/code.md`.

## Goal
Make "the data gate is open" a command, not an opinion: one script that tests the five gate checks for a page or for all 26 units.

## Decisions (author, 2026-11-17)
`docs/restructure/site.md` is approved with its eight answers (drafts under `/draft/`, hub Data block, ADOPT, PILOT and HYPO reached from their parents, `source/hub.md`, pending-page links rewritten to `retired.html`, glossary seeding before the gate, standalones move after the gate). The data gate holds: no spoke or hub prose. This brief builds on fixtures and delivers without the model data. It is one of the first parallel set (029s, 030c, 031s, 032r, 033c, 034c); the Touches lists do not overlap. The gate is G1 to G5 of `order.md` 4.1; the page needs table is `order.md` 4.2 (default: every page waits for G1 to G5, author, 2026-11-17).

## Design
`python pipeline/check_gate.py --page <ID>` prints G1 to G5 for the page with pass or fail and a reason and exits 0 only if the page's needs are met; `--all` prints the table of `order.md` 4.2 for the 26 units. Implement the commands of `order.md` 4.1 as written: G1 files and the acceptance command named in `acceptance.md`; G2 the `outputs.json` run fields and hashes and the validator; G3 the `(J)` set equals the ids in `judgement-decisions.md` and each has a dated decision; G4 per-page outputs and inputs complete, with R1 both ways against front matter; G5 the build briefs merged and the tests pass. Needs per page come from a small table in the script's data file, not hard-coded in prose. Tests on fixtures: gate closed with the repository as it is today (G1, G2, G3 fail), and open for a synthetic complete fixture.

## Touches
`pipeline/check_gate.py` (new), `tests/gate/` (new), this brief's progress block. Nothing else.

## Acceptance criteria
- With today's repository, `--all` exits non-zero and names the failing checks with reasons.
- A synthetic fixture with every input present exits 0.
- G3 counts 87 flagged rows today and reports them as pending.
- `git diff --stat` shows only the Touches list.

## Checks to run
`pytest tests/gate`; run `--all` on the repository and read the reasons.

## Out of scope
Building the data files, the model, the resolver, writing prose.

## Open questions
The implementer asks rather than guesses.

## Implementation notes
<!-- progress:start -->
- **Done:** `pipeline/check_gate.py` (`--page ID`, `--all`, `--root`) and `tests/gate/` (17 tests, pass). Needs table is `PAGES` inside the script (order.md 4.2), with escalation to G1-G5 when a page cites outputs and to G3 when it lists inputs. Real repo: `--all` exits 1, 0 of 26 open, G1/G2/G3/G5 fail with reasons, G3 "87 flagged (J) rows, 87 pending, 0 decided"; the decisions file ids equal the flagged ids.
- **Next:** guru/author confirm the assumed formats below; when B2, B3, B15 and 011g stage D land, re-run `--all`; retire `test_real_repository_is_closed_today` once the gate opens.
- **Decisions:** needs table lives in the script, not a separate data file (Touches allows no other file). G4 coverage = schedules x horizons x `by` vocabulary from the manifest; where `by` is a list of names with no vocabulary (OW2, OB1, OD1...) only non-null cells are checked, B2's V7 owns the rest. `once_not_per_schedule` outputs ignore schedule.
- **Gotchas (assumed formats, not in any spec yet):** (1) acceptance.md must hold exactly one line `Acceptance command: \`...\``. (2) `run.fixture` must be present and false (hooks.md section 9 does not list the field; 030c fixture sets it). (3) validator is called `python pipeline/validate_outputs.py --final <outputs.json>` (flags from 030c; argument form assumed). (4) `_build/hooks-report.json` needs `unresolved` (count or list). (5) The fixture-spoke release build has no command until B15: `Config.fixture_build` is None, so G5 fails by design. (6) "Merged" for B2..B6, B15 = their Touches files exist. (7) Page source found via `registry/pages.yml` (`id`, `source`) else `source/<id>.md`; hub id is `HUB`. (8) `registry/inputs.json` accepted as a list of `{id}`, `{id: row}` or `{inputs: ...}`.
- **Resume:** none needed.
- **Not run:** the G1 acceptance run, the G2 validator and the G5 build/pytest against the real repo (their files do not exist yet); only fixtures exercised them.
- **State:** done; pushed on `brief/033-gate-checker`; NEEDS THE AUTHOR (assumed formats)
<!-- progress:end -->

### Change report
```
Change report
- Task: brief 033c, spoke gate checker (order.md B17)
- Files changed: pipeline/check_gate.py (new: G1-G5 checker, --page/--all); tests/gate/ (new: conftest.py fixtures, test_gate.py, 17 tests); docs/briefs/033c-gate-checker.md (progress block, this report)
- What is different now: "the data gate is open" is a command. Today it reports all 26 units closed with the failing checks and reasons.
- New or changed interfaces: python pipeline/check_gate.py --page <ID> | --all [--root DIR]; exit 0 only if open.
- Acceptance criteria: --all on today's repo exits 1 and names failing checks with reasons (met); synthetic complete fixture exits 0 (met, test_complete_fixture_all_open); G3 counts 87 flagged rows and reports them pending (met); git diff --stat shows only the Touches list (met).
- Deviations from the brief: needs table is inside check_gate.py, because Touches allows no separate data file.
- Risks / follow-ups: eight assumed formats (progress block, Gotchas) need confirming by 011g stage D, B2, B3, B15; coverage rule for list-valued `by` is partial until B2's V7 is wired. Guru: decide whether to fold these formats into acceptance.md and hooks.md section 9.
- Verification: pytest tests/gate: 17 passed; --all and --page VAL run on the repo and read. Not run: G1 acceptance run, validator, G5 build against the real repo (inputs absent).
- Overview sections likely needing an update: site build items (B17 done); gate section of order.md
- Commit / branch: brief/033-gate-checker (NEEDS THE AUTHOR; not merged)
```

