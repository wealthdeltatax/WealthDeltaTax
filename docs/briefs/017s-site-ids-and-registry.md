# 017: Site IDs, URLs and the fate of the old registry

- **Status:** ready
- **Author/date:** K. Ogata with the guru, 2026-11-17
- **Depends on:** 013g stage C (merged); part of 013g stage D. Runs in parallel with 2 (with 018s, 019s, 020w, 021s).
- **Read:** `registry/papers.yml`, `registry/contents.yml`, the pipeline file list (names only), `docs/restructure/map.md`, `docs/restructure/ledger.md` sections 1 and 7, and brief `007w-crosslink-repair.md`. Nothing else need be opened.

## Goal
Fix the ID scheme, the URL map and what happens to the old registry, anchors, crosslinks and old paper pages, so the site build can be redesigned.

## Decisions (author, 2026-11-17)
The spoke template (`docs/restructure/template.md`) is approved, including section 6a (figures and tables). Hub and spokes: `docs/restructure/map.md` section 7. The data gate holds: no spoke prose until the data is final. This brief designs; it builds nothing.

## Design
One file only: `docs/restructure/site/ids.md`. Cover: ids for the hub (H0 to H7), spokes (S1 to S12), appendix spokes (`-A`), standalone papers (ADD, INST, SCOPE) and the data layer pages; the URL for each; what each of the 33 old paper URLs does (redirect to the nearest new page, or archived page; the author said the old papers are done away with and Zenodo records get replaced later); the future of `papers.yml`, `contents.yml`, `anchors.yml`, `crosslinks.json`, `references.json`, the glossary, the Project Map and the style guide; the format checker (`check_wdt_format.py`) for the old shape; brief 007w (obsolete); and a migration order that keeps the site deploying on every push. For every point where the document needs a decision it does not own, write a numbered question with a proposed answer; do not guess. The guru merges the sibling files into `docs/restructure/site.md` (shared file; `brief-template.md`, Splitting).

## Touches
New `docs/restructure/site/ids.md` and this brief's progress block. Nothing in `source/`, `pipeline/`, `site/`, `registry/`, `model_v1/`, `model_v2/`.

## Acceptance criteria
- A table of every new page: id, title, URL, type (hub, spoke, appendix, standalone, data).
- A table of all 33 old papers with the action for each.
- Every registry and generated file has a stated fate (keep, change, retire).
- A migration order with a deployable state after each step.
- `git diff --stat` shows only the Touches list.

## Out of scope
Building the pipeline, writing spoke or hub prose, editing `template.md`, choosing values.

## Open questions
The implementer asks rather than guesses.

## Implementation notes
<!-- progress:start -->
- **Done:**
- **Next:**
- **State:** ready
<!-- progress:end -->
