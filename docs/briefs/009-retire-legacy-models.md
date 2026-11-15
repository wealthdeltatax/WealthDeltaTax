# 009: Retire the legacy models: shared files, data dumps and reference docs

- **Status:** draft (blocked on brief 001 settling what v3 reads)
- **Author/date:** K. Ogata with the guru, 2026-11-15
- **Depends on:** 001, 006
- **Read:** `docs/briefs/001-model-v3.md` (final inputs list), `docs/briefs/002-repo-triage.md`, directory listings of `model/` and `model_new_2/`.

## Goal
After v3 exists, leave one copy of every shared file and no model documentation that describes code that is gone, and decide the fate of the 151 MB of data dumps.

## Decisions (author, 2026-11-15)
- `model/` and `model_new_2/` are legacy; `model/OUTPUTS/` stays tracked until the papers are rewritten.
- Old script names and paper numbers are not constraints.

## Design
Triage findings, each needing a disposition:
- **`jst_r6.json`** (1.77 MB, byte-identical in `model/` and `model_new_2/`): keep one copy where v3 reads it; delete the other with its legacy folder. Do not dedupe earlier; each model reads it by relative path.
- **`wdt_md.py`** (19 KB, identical in both): same rule. In `model/` it is imported by 7 scripts after brief 006 (8 before), so it goes only when `model/` goes.
- **Legacy reference docs:** `model/WDT_Model_Reference.md` (37 KB, names scripts that no longer exist) and `model_new_2/WDT_Code_Reference.md` (24 KB): move to `docs/model-lessons/` with a legacy header (agents are told not to open that folder) or delete. Recommended: move, because `docs/model-lessons/` is where v3 lessons live. `model_new_2/README.md` is a 19-byte placeholder ("Model Test"): delete.
- **`model_new_2/WID_Data_Guide.md`** (6.8 KB): documents WID data v3 may use; keep next to the data it describes, or move into v3's folder.
- **`model_new_2/wid_out/`** (81 MB, 90 files, `wid_download.py` regenerates it) and **`audit_d0/`** (70 MB, 60 files, produced by `d0_jst_audit.py`): both are regenerable output. Options: keep tracked, untrack and regenerate on demand, or keep only the small summaries (`wid_out/summary`, `summary2`, `catalogue*.csv`; `audit_d0/audit_d0.md`). Recommended: keep the summaries, untrack the rest and add it to `.gitignore`, and keep the generating scripts.
- **Which legacy folder goes:** with v3 in place, delete `model/` (35 MB, 126 files; `OUTPUTS/` 32 MB) only after the papers are rewritten and v3 reproduces the figures they cite. `model_new_2/` can go sooner.

## Touches
`model/`, `model_new_2/`, `docs/model-lessons/`, `.gitignore`.

## Acceptance criteria
- One copy of `jst_r6.json` and `wdt_md.py` in the repo.
- No document under the legacy folders names a script that does not exist.
- Tracked size before and after reported; every item above has a recorded disposition in `docs/decisions.md`.
- Every input listed in brief 001 still exists.

## Checks to run
`sha1sum` on the shared files; `git count-objects -vH`; v3 run reads its inputs.

## Out of scope
Rewriting git history (the pack is 106 MB and would stay that size); paper text.

## Open questions
- Data dumps: keep, regenerate or keep summaries only?
- When does `model/` go: after v3, or only after the papers are rewritten?

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
