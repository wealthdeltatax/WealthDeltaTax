# 130: Readable copies of every research file (markitdown)

- **Status:** ready (released 2026-11-23: all agents free; low priority, no code dependency; report the 129r file sizes in the note)
- **Author/date:** K. Ogata with the guru, 2026-11-22
- **Depends on:** nothing; best run when no research brief is writing under `docs/research/`
- **Read (block 0: the first two only):** (1) `pipeline/to_markdown.py` and `docs/agents/research.md` ("Reading PDFs, Office files, ODS and RTF"); (2) `docs/agents/code.md`. Later: the file-type survey in block 1.

## Goal
Every binary research file under `docs/research/` (PDF, XLSX, XLS, ODS, RTF, DOCX, anything else not plain text) gets a **committed Markdown reading copy**, so agents and the author read text, not binaries, and the heavy files stop being opened through slow routes. The sources stay where they are; the copy is a reading aid, not a source of record.

## Decisions (author, 2026-11-22)
- Tool: Microsoft markitdown, through the repo's `pipeline/to_markdown.py` (already present, local files only, no plugins, no cloud OCR). It is extended, not replaced.
- Agents also convert **on the fly**: any new research file or any file they investigate is converted with the script before reading (rule already added to `AGENTS.md` and `docs/agents/research.md`). After this brief, a new binary file under `docs/research/` is committed with its reading copy.
- Location: a mirror tree `docs/research/readable/<same relative path>.md`, committed. `scratch/converted/` stays the git-ignored default for ad-hoc conversions.
- CSV, JSON, TXT, MD, PY and DO files are already text and are not converted.
- Formats markitdown does not read (ODS, RTF, possibly others: the agent checks) go through a documented fallback (LibreOffice headless to XLSX then markitdown for ODS; pandoc or `striprtf` for RTF). The fallback is recorded per file in the index.

## Blocks (one push each; stop rule at the end)
- **Block 0:** progress block pushed.
- **Block 1: survey and the tool.** A table in `docs/research/readable/INDEX.md` of every binary file under `docs/research/` (path, type, size, pages or sheets, route: markitdown or fallback). Extend `pipeline/to_markdown.py` with `--readable`: writes to `docs/research/readable/<relative path>.md`, adds a header (source path, tool and version, date, "reading copy: quote numbers from the source"), caps very wide sheets (a row cap per sheet with a visible truncation note and the sheet's row count), and falls back as above. Tests for the header, the mirror path and the cap on small fixtures. Push.
- **Block 2: PDFs and Office files.** Convert the PDFs, DOCX and XLSX/XLS; check each output (non-empty, tables present, page count against the source); record scanned or garbled files in the index as `poor` with the reason, do not hand-fix them. Push.
- **Block 3: ODS and RTF.** The fallback routes; the 18 RTF data dictionaries (large: report output sizes and keep each file under the size cap, splitting by section only if a file is too big to read) and the ODS workbooks. Push.
- **Block 4: the index and the rule.** Finish `INDEX.md` (status per file: ok, poor, skipped with reason, total size); a check in `pipeline/check_agent_docs.py` (warning, not an error) that every binary under `docs/research/` has a reading copy; one line in `docs/agents/research.md` and `docs/agents/code.md` pointing to `--readable`. Change report; push; stop.
**Stop rule.** After two blocks, or a quarter of the budget left, push what exists and list the rest under Next. Print only summary lines (files converted, failures, bytes); never print converted text. Run conversions in the background in batches.

## Touches
`docs/research/readable/` (new), `pipeline/to_markdown.py`, `pipeline/check_agent_docs.py` (one warning), `tests/` for the script, `docs/agents/research.md`, `docs/agents/code.md`, `.gitignore` only if `readable/` needs un-ignoring. Not the source files, `moments.csv` or any data CSV, the model, the register or the manifest. Name any other file before editing it.

## Acceptance criteria
- Every binary under `docs/research/` has a reading copy or an index row saying why not.
- Copies carry the header and, where capped, a visible truncation note; none is hand-edited.
- Total added size is reported; if it exceeds 30 MB, stop and report before pushing the RTF block.
- `pipeline/to_markdown.py --readable` works on a new file; its tests pass; `python -I pipeline/check_agent_docs.py` passes (the new check warns, never fails).
- No source file moved or changed.

## Out of scope
Moving or deleting the sources, large-file storage policy (a question for the author: 201 MB sits in `docs/research/data/129r` today), OCR of scanned files, editing converted text, files outside `docs/research/`.

## Open questions
Whether the 129r PDFs and data dictionaries should leave git once converted (the agent reports sizes; the author decides).

## Implementation notes
<!-- progress:start -->
- **Done:** blocks 0 to 4. All 38 binaries under `docs/research/` (5 pdf, 7 xlsx, 8 ods, 18 rtf; no docx or xls present) have a committed reading copy at `docs/research/readable/<path>.md` plus `INDEX.md` and `status.json`: 38 ok, 0 poor, 0 failed. Copies total 26.7 MB (under the 30 MB stop); sources untouched. `to_markdown.py --readable` (mirror path, header, 300-row cap with a visible note, ODS via soffice, RTF via pandoc, `--all`, `--index`); `check_agent_docs.py` warns on a missing copy; one line each in `docs/agents/research.md` and `code.md`. Suites: data 102, hooks 88, gate 17 pass; check_agent_docs exit 0.
- **129r sizes (for the author's question):** `docs/research/data/129r` is 201 MB in git, of which the 18 RTF data dictionaries are 194 MB (largest 35.8 MB); their copies are 22.9 MB (largest 4.1 MB) and the whole 129r folder's copies are 23 MB. Whether the sources should leave git is the author's decision.
- **Next:** none for this brief.
- **Resume:** none.
- **State:** done; merged
<!-- progress:end -->

### Change report
```
Change report
- Task: brief 130c, readable copies of every research file
- Files changed: pipeline/to_markdown.py (--readable, --all, --force, --rows, --index, routes, status record); pipeline/check_agent_docs.py (one warning); tests/data/test_to_markdown.py (new, 6 tests); tests/hooks/test_check_agent_docs.py (1 test); docs/agents/research.md and docs/agents/code.md (one rule each); docs/research/readable/ (38 copies, INDEX.md, status.json); this brief
- What is different now: every binary under docs/research has a generated Markdown reading copy with a header (source, route, tool, date, quote-from-source warning); spreadsheets are capped at 300 rows a table with a visible note (cut tables are listed in the header); a new binary is committed with its copy and a missing one is warned
- New or changed interfaces: to_markdown.py --readable [--all] [--force] [--rows N] [--index] [--root DIR]; readable/status.json
- Acceptance criteria: every binary has a copy or an index row (met: 38 ok); headers present, caps visible, none hand-edited (met); added size reported, under 30 MB (met: 26.7 MB); --readable works on a new file, tests and check_agent_docs pass, the new check only warns (met); no source file moved or changed (met)
- Deviations from the brief: none; the RTF copies are not split (largest 4.1 MB, read by offset or grep)
- Risks / follow-ups: the cap drops rows from long sheets in the copy (quarterlysectoraccounts2026q2 and gb_ppp_machine_readable: tables of 636 to 1,039 rows), so numbers from those sheets come from the source; the copies add 26.7 MB to git; 129r sources are 201 MB (author to decide whether they leave git)
- Instruction friction: none
- Verification: data 102, hooks 88, gate 17 passed; check_agent_docs exit 0; summary lines only (no converted text printed)
- Overview sections likely needing an update: none
- Commit / branch: brief/130-readable-research, merged to main
```
