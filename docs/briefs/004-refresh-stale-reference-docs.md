# 004: Refresh the stale site-architecture doc

- **Status:** ready
- **Author/date:** K. Ogata with the guru, 2026-11-15
- **Depends on:** 002 (merged); 003 only if both edit `deploy.yml` descriptions. Order: with 003, 006, 008 (parallel).
- **Read:** `docs/wdt-site-architecture.md`, `pipeline/`, `site/_quarto.yml`, `.github/workflows/deploy.yml`, `docs/agents/web.md`

## Goal
Make the site architecture doc true again. It is the single source of truth for the site build (named in `docs/agents/web.md`).

## Decisions (author, 2026-11-15)
- `docs/wdt-site-architecture.md` is the web role's source of truth and must match the files.
- The v1 and v2 models are legacy and being replaced (brief 001), so their reference docs are not worth refreshing. Their disposition moved to brief 009 (triage, 2026-11-15) so the model decisions are made in one place.

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
- **Done:**
- **Next:**
- **Decisions:**
- **Gotchas:**
- **Resume:**
- **Not run:**
- **State:**
<!-- progress:end -->
