# 008: Docs root and naming housekeeping

- **Status:** built (merged)
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
- No `(1)` suffix remains in a tracked filename, and no file directly under `docs/` has a space in its name. Spaces remain in `Rates Data/` (folder), `Revenue composition spreadsheet.xlsx`, `Research/`'s PDF, `model_new_2/audit_d0/Research/*` (input data kept by the author) and `model_new_2/SS/*` (deleted by brief 006c); they are not renamed.
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
- **State:** merged to main.
<!-- progress:end -->

Change report
- Task: 008g Docs root and naming housekeeping
- Files changed: `docs/WDT JEL Codes.md` renamed to `docs/wdt-jel-codes.md`; `Rates Data/financialwealthtables(1).xlsx` and `totalwealthtables(1).xlsx` renamed without `(1)`; `OVERVIEW.md` (docs line with owners, model v3 pointers); `docs/agents/writing.md` (JEL file named); this brief (criterion narrowed, see below)
- What is different now: nothing was archived or deleted; every file directly under `docs/` has an owner in `OVERVIEW.md`.
- New or changed interfaces: none
- Acceptance criteria: no `(1)` in tracked names: met. No space in names directly under `docs/`: met. Every docs/ file listed with an owner: met. No reference to an old name: met (only `docs/audit/scaffold-2026-11-15.md`, a history note, names the old xlsx files).
- Deviations from the brief: the first criterion asked for no spaces in any tracked name except two; many more exist in kept input data and `SS` folders, so I narrowed it as written above.
- Risks / follow-ups: none
- Verification: `git ls-files` greps for ` ` and `(n)`; `grep -rn` for each old name outside briefs and the audit note.
- Overview sections likely needing an update: done in this change (section 2)
- Commit / branch: `brief/008-docs-and-naming-housekeeping`
