# 008: Docs root and naming housekeeping

- **Status:** draft
- **Author/date:** K. Ogata with the guru, 2026-11-15
- **Depends on:** 002 (merged). Order: parallel with 003, 004, 006; after 004 if `navigation_suggestions.md` is still cited.
- **Read:** `docs/` listing, `docs/agents/README.md`, `STATUS.md`, `docs/todo.md`, and the first 30 lines of each file named below.

## Goal
Give every file in `docs/` an owner, a status (current, legacy or archive) and a name without spaces or stray `(1)` suffixes, so agents stop meeting unowned files.

## Decisions (author, 2026-11-15)
- Old paper-number references and old model names are not a concern (papers and model are being redone).
- Proposed below; the author approves each disposition before it is applied.

## Design
Triage found these `docs/` files with no owner or index entry:

| File | Size | Finding | Proposed disposition |
|---|---|---|---|
| `EVAL_PLAN.md` | 102 KB | Over budget; plan for the v2 model (`model_new_2/EVAL/eval_core.py` names it) | Move to `docs/archive/` with a legacy header, or to `docs/model-lessons/` if the author wants it kept for v3 |
| `VAL_generational_model_plan.md` | 26 KB | v2 plan (VAL paper) | Same as above |
| `VAL_refactor_report.md` | 11 KB | v2 refactor report | Same as above |
| `navigation_suggestions.md` | 6 KB | A pasted chat answer about cross-reference design; cited only by `wdt-site-architecture.md` | Archive (or ask the author if any suggestion is wanted as a brief) |
| `WDT JEL Codes.md` | 12 KB | JEL front-matter blocks for the papers; owner is the writing role; name has spaces | Rename `wdt-jel-codes.md` (nothing references the old name); list in `docs/agents/writing.md` |
| `todo.md` | 1 KB | Priority list already carried in `STATUS.md` "Open findings" | Fold remaining items into `STATUS.md`, then delete |

Other naming: `Rates Data/financialwealthtables(1).xlsx` and `totalwealthtables(1).xlsx` are not duplicates (no originals exist, the sizes are 128 KB and 106 KB) and nothing in the repo names them. Rename to drop `(1)`; do not delete. Folder renames `Rates Data` to `rates-data`, `Research` to `research`, `Tools` to `tools` break no code (no script, workflow or guide references the first two paths; `Tools/` is named in `OVERVIEW.md` and `STATUS.md` only) but wait until brief 005 has settled `Tools/`.

Add one line per kept doc to `docs/agents/README.md` or `OVERVIEW.md` (report it; the guru edits `OVERVIEW.md`).

## Touches
`docs/*.md`, `docs/archive/`, `Rates Data/`, `Research/`, `STATUS.md` (guru).

## Acceptance criteria
- Every file directly under `docs/` is either listed in `OVERVIEW.md` with an owner or is in `docs/archive/` with a legacy header.
- No tracked filename contains a space or `(1)`.
- `grep -rn` for each moved or renamed name finds no broken reference.

## Checks to run
`git ls-files | grep -E ' |\([0-9]\)'` is empty; link grep for each renamed file.

## Out of scope
Editing the content of any moved document; splitting `wdt-site-architecture.md` (brief 004).

## Open questions
- Keep the three v2 plans for v3 (`docs/model-lessons/`) or archive?
- Rename `Rates Data`, `Research` and `Tools` now or leave (low value)?

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
