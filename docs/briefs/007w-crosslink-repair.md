# 007: Crosslink errors in the papers

- **Status:** parked
- **Author/date:** K. Ogata with the guru, 2026-11-15
- **Depends on:** author's paper rewrite. Order: last; nothing else waits on it.
- **Read:** `check.txt` (or a fresh `python pipeline/wdt_crosslinks.py check`), `docs/agents/reference/writing/style-guide.md` (post-update crosslink workflow)

## Goal
Clear the crosslink errors once the author's rewrite settles the section structure.

## Decisions (author, 2026-11-15)
- The author is rewriting the papers, so old reference codes are not a concern now. Do not repair against the current text.

## Design
- Last known state (`check.txt`): 6 duplicate section numbers (ADD §1 to §5 in `18_Addendums.md`, RATES §7.4), 5 sections not found (SCOPE §5.5, RATES §9.7, WFR §7, SWEEPS §B.5, SWEEPS §E.2) and 307 stale anchors.
- When the rewrite lands, run the check fresh, then follow the workflow in the style guide: errors first, then `scrape_contents.py` and `build_anchors.py`.
- The stale-anchor count is mostly a regeneration job, not a writing job.

## Touches
`source/`, `registry/` (writing role, with the author's review).

## Acceptance criteria
- `wdt_crosslinks.py check` reports no errors.

## Checks to run
`python pipeline/check_wdt_format.py`, `python pipeline/wdt_crosslinks.py check`.

## Out of scope
Anything before the rewrite is done.

## Open questions
- None.

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
