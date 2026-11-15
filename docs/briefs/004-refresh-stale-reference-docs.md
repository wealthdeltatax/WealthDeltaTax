# 004: Refresh the stale site-architecture doc and retire the old model reference

- **Status:** draft
- **Author/date:** K. Ogata with the guru, 2026-11-15
- **Depends on:** 002
- **Read:** `docs/wdt-site-architecture.md`, `pipeline/`, `site/_quarto.yml`, `.github/workflows/deploy.yml`, `model/WDT_Model_Reference.md`

## Goal
Make the site architecture doc true again, and stop the old model reference from misleading agents.

## Decisions (author, 2026-11-15)
- `docs/wdt-site-architecture.md` is the web role's source of truth and must match the files.
- The v1 and v2 models are legacy and being replaced (brief 001), so their reference docs are not worth refreshing.

## Design
- Site architecture: fix the root path (`wdt-site/` is now the repo root), the directory tree, the paper count (33 entries in `registry/papers.yml`), the OUTPUTS claim (tracked, not gitignored), and the build scripts; split it by topic if it stays over about 15 KB (it is 29 KB). Show the diff to the author.
- `model/WDT_Model_Reference.md` (names `rates_model.py`, now `rates_core1.py`, and old script numbers): move to `docs/model-lessons/` with a legacy header, or delete. Same question for `model_new_2/WDT_Code_Reference.md`, decided in brief 002 and 006.
- Update `OVERVIEW.md` section 6 through the guru after.

## Touches
`docs/wdt-site-architecture.md`, `model/WDT_Model_Reference.md`, `OVERVIEW.md`.

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
