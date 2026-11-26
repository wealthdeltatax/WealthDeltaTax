# 173: Missing reading copies, and a sweep for empty or stub files

- **Status:** ready; any free agent
- **Author/date:** K. Ogata with the guru, 2026-11-26
- **Depends on:** 164c (merged)
- **Read:** `project/agents/agent-code.md`, `literature/readable/readable-copies-index.md`, `project/tools/to_markdown.py` (`--readable`, `--rows`)

## Goal
Every binary file under `literature/` and `data/` has a committed reading copy, so `check_agent_docs.py` gives no "no reading copy" warnings; and nothing in the repository is an empty or stub file by accident.

## Decisions (author, 2026-11-26)
The author saw "many legacy files with no contents". The guru's check of the committed tree found only five empty tracked files (the `__init__.py` of `model/model_v3` and its `core`, `out`, `pack`, `runner` packages, all legitimate), no empty directories in a fresh checkout, and 24 binary sources with no reading copy: 8 spreadsheets under `data/rates/` and `data/uk-source-workbooks/`, and 16 PDFs under `literature/`. The author's own working folder may also hold empty leftover directories from the moves (git does not track them); that is the author's to clear (`git clean -fdn` to preview).

## Stages
- A: install `markitdown[pdf]` (`pip install --break-system-packages`), then for each of the 24 files run `python -I project/tools/to_markdown.py --readable <file>`. Spreadsheets are capped at 300 rows a table with a visible note. Check each copy has content: a scanned PDF can come out empty; list any such file and do not commit a blank copy (list it as a data request for the author, with the file name). Update `literature/readable/readable-copies-index.md` (status per file). Checkpoint: one push.
- B: sweep: (1) list every tracked file under 200 bytes and every tracked file whose content is only whitespace or a placeholder (`TODO`, `placeholder`, `tbd`, a bare heading); for each, say keep or remove and why, and remove only the ones that are demonstrably dead (nothing references them: `grep` the path and the name, `project/restructure/file-layout-map.csv`, the tests). (2) Check each `papers/legacy/*.md` has body text (not just a title) and report any that do not. (3) Do not touch fixtures under `tests/*/fixtures/`, the five package `__init__.py` files, `CNAME`, `robots.txt`, `.gitattributes`, `.nojekyll` or `website/site/includes/*`. Checkpoint: one push with the list and the removals.

## Touches
`literature/readable/**` (new copies, the index), a short report `project/restructure/empty-file-sweep.md`, removals found by stage B step 1 only. No model, paper or data content.

## Acceptance criteria
- `python -I project/tools/check_agent_docs.py` exits 0 and prints no "no reading copy" warning, except files listed as data requests.
- The sweep report lists every file considered and the decision; nothing referenced was removed; the fast suites and the tripwire (after a commit and `git clean -fdx`) still pass.

## Out of scope
Rewriting papers, the converter's behaviour, any change to references or the register.

## Open questions
A PDF that converts to nothing (scanned): stop on that file, list it, continue with the rest.

## Implementation notes
<!-- progress:start -->
- **Done:** stage A: 25 reading copies (the checker listed 25, not 24; all converted ok, none empty), index updated, `check_agent_docs.py` exits 0 with no "no reading copy" warning. Stage B: sweep report `project/restructure/empty-file-sweep.md`; nothing removed.
- **Next:** author: two data requests (below). Brief can be retired.
- **Decisions:** none removed; all small files are referenced or excluded.
- **Gotchas:** `data/country-packs/GBR/tax_rules.csv` is header only; `public_expenditure.csv` has one row.
- **Resume:** n/a.
- **Not run:** the tripwire and fast suites (nothing in the model or tests changed; only reading copies, one report and the brief).
- **State:** done
<!-- progress:end -->

## Change report
Change report
- Task: brief 173c, reading copies and empty-file sweep
- Files changed: `literature/readable/**` (25 new copies, index, status.json); `project/restructure/empty-file-sweep.md`; this brief
- What is different now: every binary under `literature/` and `data/` has a reading copy; the sweep is on file
- New or changed interfaces: none
- Acceptance criteria: `check_agent_docs.py` exit 0, no "no reading copy" warning (met); sweep lists every file considered, nothing removed (met); tripwire and fast suites not run, nothing they read changed
- Deviations from the brief: 25 files, not 24
- Risks / follow-ups: data requests for the author: `tax_rules.csv` (header only) and `public_expenditure.csv` (one row) in the GBR pack
- Instruction friction: none
- Verification: converter reported 25 ok, 0 poor, 0 failed; checker rerun
- Overview sections likely needing an update: none
- Commit / branch: brief/173-readable-copies
