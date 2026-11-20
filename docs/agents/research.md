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
- `registry/references.json` is generated from the `.bib` and `internal.json` by `pipeline/bib_to_json.py`; regenerate it, do not hand-edit.

## Definition of done
Every added or changed entry verified or flagged, discrepancies and flags reported, confirmed records written, change report lists entries added and updated.

## Boundaries
Prose rewrites go to writing. Recommendations and design decisions belong to the guru and the author; research reports evidence and confidence.
