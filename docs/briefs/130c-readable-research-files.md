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
- **Done:** block 0 (branch from main cee5b03)
- **Next:** block 1 (survey, `--readable`, tests)
- **Resume:** `git fetch origin '+refs/heads/*:refs/remotes/origin/*' && git checkout -B brief/130-readable-research origin/brief/130-readable-research`
- **State:** in progress, block 0 pushed
<!-- progress:end -->
