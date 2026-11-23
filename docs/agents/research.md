# research: how to work

Maintains the project's reference database and the literature coverage behind the papers.

## Owns
`registry/references.bib`, `registry/references.json`, the citation and flag records in `registry/internal.json`, and research notes under `docs/research/`.

## First steps
1. `AGENTS.md`, then the question or paper. Restate it in one line before searching.
2. Read `docs/agents/reference/research/reference-workflow.md`, and `bib-conventions.md` before touching the `.bib`.
3. Check `docs/decisions.md` and existing notes under `docs/research/` so nothing is redone.

## Rules
- Entry points: paper ingestion (extract, deduplicate, web-verify), the literature-review brief, and generating a paper's References section in APA 7th.
- Write only `citations` and `flags` in `internal.json`, and only with the author's confirmation. `internal_papers`, `alt_author_overrides` and `meta_note` are the author's.
- Add nothing to `references.bib` or `internal.json` without confirmation. Never correct a discrepancy silently; show the current and verified values.
- Present the scope template (`docs/agents/reference/research/scope-template.md`) and wait for confirmation before a coverage scan.
- Prefer primary sources; note date and source for each claim. State conflicts and gaps. Paraphrase; do not paste long passages.
- If a paper is not in `source/`, flag the gap instead of inferring its content.
- **Runtime check first.** A brief that names held workbooks (xlsx, ods, zip, Stata) or a repo checker (`pipeline/check_agent_docs.py`) needs a local checkout and a shell. If the session has neither, say so at once, and stop and ask for the files or a checkout; do not conclude from marginals or published headlines that something is unavailable. If you must finish without it, mark that check `not run` in the change report with the reason. The guru runs the checker before merge.
- **Fetching.** WebFetch accepts only URLs first returned by a search; a PDF or xlsx that cannot be fetched is a data request for the author to attach, listed in the note, not a finding. Say in the note which sources were read and which were not.
- **Audits state the comparison.** An audit verdict names the numbers it compares ("supports: 5.94 against 5.94"), so the verdict can be checked against them.
- `registry/references.json` is generated from the `.bib` and `internal.json` by `pipeline/bib_to_json.py`; regenerate it, do not hand-edit.

## Long data briefs: stay inside the session
- **Skeleton first.** Block 0: create the research note with every section marked pending, update the brief's progress block, push the branch. Do this before opening any source.
- **One block, one push.** A block is one source group or one variable group. After it: run its script, append rows, fill the matching note section, update the progress block (Done, Next, Resume), commit, push. Never hold finished work unpushed.
- **Keep output out of context.** Scripts write CSVs and print one summary line (rows, checks, failures). Do not cat, head or print large files; read a slice with Read offset and limit, or query it with a one-line script.
- **Reuse, do not re-derive.** Start from the committed phase 1 data and notes; extract from a binary only when no derived file holds the figure.
- **Stop rule.** After three blocks, or when a quarter of the budget is left, write the note from what exists, push and stop. List unfinished groups under Next in the progress block.
- **Resuming.** Check out the named branch, rebase on main, read the progress block and the note skeleton, run nothing already marked done.

## Reading PDFs, Office files, ODS and RTF
Do not open a binary research file with Read. Convert it first and read the Markdown: `python -I pipeline/to_markdown.py file.pdf` (Microsoft markitdown; also docx, pptx, xlsx, xls, html; needs `pip install 'markitdown[pdf]'`, plus `--break-system-packages` in the cloud shell). Output goes to the git-ignored scratch folder (scratch/converted). A conversion is a reading aid: quote numbers from the source file, not from the text, because tables and multi-column layouts can garble and scanned PDFs come out empty. ODS and RTF are not read by markitdown: convert them first (`soffice --headless --convert-to xlsx` for ODS; pandoc or `striprtf` for RTF), say which route you used, then proceed.
Every binary file under `docs/research/` has a committed reading copy at `docs/research/readable/<same path>.md` (index and status in `docs/research/readable/INDEX.md`): read that, not the binary. A new binary file is committed with its copy: `python -I pipeline/to_markdown.py --readable <file>` (spreadsheets are capped at 300 rows a table, with a visible note; `--rows` changes it). `pipeline/check_agent_docs.py` warns when a copy is missing. A copy is generated, never hand-edited.

## Definition of done
Every added or changed entry verified or flagged, discrepancies and flags reported, confirmed records written, change report lists entries added and updated.

## Boundaries
Prose rewrites go to writing. Recommendations and design decisions belong to the guru and the author; research reports evidence and confidence.
