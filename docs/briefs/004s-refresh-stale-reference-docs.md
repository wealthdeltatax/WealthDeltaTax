# 004: Refresh the stale site-architecture doc

- **Status:** ready
- **Author/date:** K. Ogata with the guru, 2026-11-15
- **Depends on:** 002 (merged); 003 only if both edit `deploy.yml` descriptions. Order: with 003, 006, 008 (parallel).
- **Read:** `docs/wdt-site-architecture.md`, `pipeline/`, `site/_quarto.yml`, `.github/workflows/deploy.yml`, `docs/agents/web.md`

## Goal
Make the site architecture doc true again. It is the single source of truth for the site build (named in `docs/agents/web.md`).

## Decisions (author, 2026-11-15)
- `docs/wdt-site-architecture.md` is the web role's source of truth and must match the files.
- The v1 and v2 models are legacy and being replaced (brief 001), so their reference docs are not worth refreshing. Their disposition moved to brief 009c (triage, 2026-11-15) so the model decisions are made in one place.

## Design
- Site architecture: fix the root path (`wdt-site/` is now the repo root), the directory tree, the paper count (33 entries in `registry/papers.yml`), the OUTPUTS claim (tracked, not gitignored), and the build scripts; split it by topic if it stays over about 15 KB (it is 29 KB). Show the diff to the author.
- `docs/navigation_suggestions.md` is cited by the architecture doc but is a pasted chat answer with no owner; if the architecture doc still needs it, keep the point inside the doc, otherwise brief 008 archives the file.
- Report the OVERVIEW changes; the guru updates `OVERVIEW.md` section 6 after.

## Touches
`docs/wdt-site-architecture.md` only (plus a change report for the guru).

## Acceptance criteria
- Every path and script named in the architecture doc exists, or the doc says it is planned.

## Checks to run
A script that checks the paths named in backticks exist; the build still runs.

## Out of scope
Changing site behaviour.

## Open questions
- Split the architecture doc into several files, or only correct it?

## Implementation notes
<!-- progress:start -->
Change report
- Task: 004s refresh the site-architecture doc
- Files changed: `docs/wdt-site-architecture.md` (corrected against the files); this brief (notes)
- What is different now: root path, directory tree, preprocess step order, model/ section (tracked OUTPUTS, `rates_core1.py`), workflow description and issue statuses match the repo on 2026-11-15. New Issue 16 added; Issue 4 reworded as fixed in `source/`; Issue 7 marked still present.
- New or changed interfaces: none
- Acceptance criteria: every path and script named in backticks exists or is documented as missing/generated. Measured with a script over the doc's backticked names: the only non-existent names left are generated outputs (`corpus.qmd`, `site-index.json` ...), bare extensions, the former root `wdt-site/`, `right-panel-search.html` (doc says it does not exist) and `rates_model.py` (doc says it is gone, Issue 16).
- Deviations from the brief: not split by topic. The doc is 32 KB (target about 15 KB). Splitting would add files outside `Touches`, and `docs/agents/web.md` names this single file. Correct-only was chosen (the brief's open question, author said merge). Also not checked against the live site, and Issues 1, 3, 5, 6, 8, 9, 10, 11, 12, 13, 14, 15 were rechecked in code only.
- Risks / follow-ups: (1) Issue 16: the National Revenue calculator probably fails because `rates_model.py` is gone; needs a decision. (2) Issue 7: a Zenodo sandbox token is still hardcoded in `pipeline/zenodo_upload.py`; revoke and rotate it, and check git history. (3) Split the doc later if wanted.
- Verification: path-check script (above); doc-only diff, so no new build run (the 003 build passed on the same tree).
- Overview sections likely needing an update: section 6 first bullet (architecture doc is now synced, 15 Nov); add Issue 16 and Issue 7.
- Commit / branch: brief/004-refresh-stale-reference-docs
- Merged by the author's instruction ("merge all good, continue", 2026-11-15 21:10). Brief stays live until the author retires it.
<!-- progress:end -->
