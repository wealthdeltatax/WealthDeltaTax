# 008: Docs root and naming housekeeping

- **Status:** ready
- **Author/date:** K. Ogata with the guru, 2026-11-15
- **Depends on:** 002. Order: guru lane; any time before 001c.
- **Read:** `docs/` listing, `docs/agents/README.md`, `OVERVIEW.md` section 2, `Rates Data/` listing.

## Goal
Give every file directly under `docs/` an owner in `OVERVIEW.md`, and fix the filenames that contain spaces or a `(1)` suffix, without deleting anything.

## Decisions (author, 2026-11-15)
- "Rename and keep": nothing is archived or deleted in this brief.
- Old paper-number references and old model names are not a concern.

## Design
Triage found these `docs/` files with no owner or index entry. All stay where they are; each gets a one-line entry in `OVERVIEW.md` (the guru edits it).

| File | Size | What it is | Owner |
|---|---|---|---|
| `EVAL_PLAN.md` | 102 KB | Plan for the v2 model (named by `model_new_2/EVAL/eval_core.py`); over the size budget | code (legacy) |
| `VAL_generational_model_plan.md` | 26 KB | v2 plan for the VAL paper | code (legacy) |
| `VAL_refactor_report.md` | 11 KB | v2 refactor report | code (legacy) |
| `navigation_suggestions.md` | 6 KB | Pasted chat answer on cross-reference design; cited by `wdt-site-architecture.md` | web |
| `WDT JEL Codes.md` | 12 KB | JEL front-matter blocks for the papers | writing |
| `todo.md` | 1 KB | Priority list also carried in `STATUS.md` | guru |

Renames (nothing in the repo references the old names):
- `docs/WDT JEL Codes.md` to `docs/wdt-jel-codes.md`.
- `Rates Data/financialwealthtables(1).xlsx` to `financialwealthtables.xlsx`, and `totalwealthtables(1).xlsx` to `totalwealthtables.xlsx`. They are not duplicates: no originals exist.
- The `Rates Data`, `Research` and `Tools` folder names are left as they are (`Tools/` is named in `OVERVIEW.md` and `STATUS.md`).

## Touches
`docs/wdt-jel-codes.md` (renamed), `Rates Data/` (two renames), `OVERVIEW.md` and `docs/agents/writing.md` (a list entry; guru).

## Acceptance criteria
- `git ls-files | grep -E ' |\([0-9]\)'` is empty except `Rates Data/` and `Revenue composition spreadsheet.xlsx` (folder and file names with spaces that the author keeps).
- Every file directly under `docs/` is listed in `OVERVIEW.md` with an owner.
- `grep -rn` for each old name finds no reference.

## Checks to run
The `git ls-files` grep and one link grep per renamed file.

## Out of scope
Moving, archiving or editing the content of any document; splitting `wdt-site-architecture.md` (brief 004s).

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
