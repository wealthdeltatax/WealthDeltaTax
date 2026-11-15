# 006: Model folders: duplicates, backups and superseded material

- **Status:** draft
- **Author/date:** K. Ogata with the guru, 2026-11-15
- **Depends on:** 001, 002
- **Read:** `model/`, `model_new_2/`, `docs/model-lessons/`, brief 002's duplicate list

## Goal
Reduce the two legacy model folders to what model v3 needs as input, and stop tracking backups and duplicates.

## Decisions (author, 2026-11-15)
- Both `model/` and `model_new_2/` are legacy; model v3 is a complete rework (brief 001).
- Old paper-number references and script names do not matter.

## Design
- `model_new_2/` contains four `SS` (superseded) folders, 61 tracked `.bak` files and duplicate patch scripts: delete the superseded material (history is in git and the author's backup).
- `model/jst_r6.json` and `model_new_2/jst_r6.json` are identical: keep one copy where model v3 will read it, or reference one from the other.
- `model_new_2/wid_out` (81 MB) and `audit_d0` (70 MB) are data and audit dumps: decide keep, regenerate, or untrack.
- `model/test/welfare_core.py` and `welfare_tables.py` are not tests: move or delete.
- Decide whether `model/` stays at all once `docs/model-lessons/` and model v3 inputs are captured. `model/OUTPUTS/` stays tracked for now (author's decision) until the papers are rewritten.
- Do not rename scripts.

## Touches
`model/`, `model_new_2/`, `.gitignore`.

## Acceptance criteria
- No tracked `.bak` or `SS` folder remains under the model folders; each duplicate has one copy; the repo size is reported before and after.

## Checks to run
`git count-objects -vH` before and after; model v3 inputs listed in brief 001 still exist.

## Out of scope
Rewriting any model code.

## Open questions
- Is `model_new_2/wid_out` needed as committed data?

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
