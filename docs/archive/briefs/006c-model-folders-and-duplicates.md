# 006: Model folders: remove superseded material, backups and in-folder duplicates

- **Status:** built (merged)
- **Author/date:** K. Ogata with the guru, 2026-11-15
- **Depends on:** 002 (merged). Does not wait for 001. Order: parallel with 003s, 004s, 008g. Must be merged before 010s, which renames the folders, and before 001c. Cross-folder decisions (`jst_r6.json`, `wdt_md.py`, data dumps, legacy reference docs) are in brief 009c, now parked: the author keeps them for now (2026-11-15).
- **Read:** `docs/archive/briefs/002g-repo-triage.md` (findings below), `model_new_2/` and `model/test/` directory listings. Nothing else need be opened.

## Goal
Take the dead weight out of the two legacy model folders without touching anything model v3 might need as input.

## Decisions (author, 2026-11-15)
- Both `model/` and `model_new_2/` are legacy; model v3 is a complete rework (brief 001).
- `SS` means superseded; history is in git and the author's backup, so deleting is fine.
- Old paper-number references and script names do not matter. Do not rename scripts.
- Folder names change in brief 010s (`model_v1`, `model_v2`); this brief uses the current names.

## Design
Triage numbers (tracked files, 2026-11-15): `model_new_2/` is 411 files and 192 MB; `SS` folders hold 218 files (`model_new_2/SS` 155, `test/SS` 52, `RATES/SS` 6, `VAL/SS` 5), including 29 MB `SS/sweep_out`, 1.8 MB `sweep_results.csv` and all 61 tracked `.bak` files (51 + 5 + 5).
- Delete the four `SS` folders under `model_new_2/`. Every duplicate found inside them has a surviving copy outside (`rates_view.py`, `diff_json.py`, `patchlib.py`, `test_hlc_drift.py`, `print_hlc_calibration.py`) or is a copy of a `model/` file (`5_3_VAL_tables.py`, `5_4_VAL_charts.py`, `5_5_VAL_generate_worked_examples.py`), so nothing is lost.
- Delete `model_new_2/test/_backups/` (6 tracked patch backups).
- Delete `model/test/welfare_core.py` and `welfare_tables.py`. `model/wfr_core.py` says it was merged from `welfare_core.py` and that there are no other consumers; re-run the grep before deleting. Keep `model/test/test_wdt_md.py`.
- Leave `jst_r6.json`, `wdt_md.py`, `wid_out/`, `audit_d0/` and both reference docs alone (brief 009).
- Confirm no file outside `SS` imports from it before deleting: `grep -rn "SS" model model_new_2 --include=*.py`.

## Touches
`model_new_2/SS`, `model_new_2/*/SS`, `model_new_2/test/_backups`, `model/test/welfare_*.py`.

## Stages
- A: delete the `SS` folders and `_backups`. Checkpoint: branch pushed; check: `git ls-files | grep -E '/SS/|\.bak|_backups'` is empty.
- B: delete the `welfare_*` files. Checkpoint: branch pushed; check: `python -I -c "import sys; sys.path.insert(0, '.'); import wfr_core"` run from inside `model/` still works (`-I` drops the current directory from the import path, so it is added explicitly).

## Acceptance criteria
- No tracked `.bak`, `SS` or `_backups` path remains under `model/` or `model_new_2/`.
- Expected tracked-file drop of about 226 files and about 37 MB (`du -sh model_new_2/SS` is 37 MB); report the actual number from `git ls-files` and `du`.
- `model/` and `model_new_2/` core imports still resolve.
- Repo size reported before and after (`git count-objects -vH`; the pack will not shrink because history stays).

## Checks to run
`git ls-files` greps above; `python -I -c "import sys; sys.path.insert(0, '.'); import wfr_core"` run from inside `model/`. The model run scripts are not run (they take long and are legacy).

## Out of scope
Rewriting git history to shrink the pack (the pack is 106 MB; ask the author if that matters). Anything in brief 009.

## Open questions
- None blocking. If any non-`SS` file imports from an `SS` path, stop and ask.

## Implementation notes
<!-- progress:start -->
- **Done:** Stage A (four `SS` folders and `model_new_2/test/_backups` deleted) and stage B (`model/test/welfare_core.py`, `welfare_tables.py` deleted). Both pushed to `brief/006-model-folders`.
- **Next:** The guru retires the brief.
- **Decisions:** Ran the `wfr_core` import check with `sys.path.insert(0, '.')` added (see Gotchas) and also on the pre-change baseline 16b06df, which behaves the same.
- **Gotchas:** The brief's check `python -I -c "import wfr_core"` fails with ModuleNotFoundError, before and after this change, because `-I` leaves the current directory off `sys.path`. Wording fixed in this brief on the author's explicit permission (2026-11-15): `sys.path.insert(0, '.')` added to the command. Same intent, not a weaker check.
- **Resume:** Merged to `main` on the author's permission; nothing to resume.
- **Not run:** Model run scripts (legacy, long; the brief excludes them). No site build named in the brief.
- **State:** merged, ready to retire.

```
Change report
- Task: 006c Model folders: remove superseded material, backups and in-folder duplicates
- Files changed: 224 files deleted under model_new_2/SS, model_new_2/test/SS, model_new_2/RATES/SS, model_new_2/VAL/SS, model_new_2/test/_backups (superseded material and 61 .bak backups); 2 files deleted: model/test/welfare_core.py, welfare_tables.py (unused shims); this brief's notes
- What is different now: legacy model folders no longer carry superseded copies or backups; model/test holds only the four test_*.py files
- New or changed interfaces: none
- Acceptance criteria:
  - No tracked .bak, SS or _backups path remains: met, `git ls-files | grep -E '/SS/|\.bak|_backups'` returns 0 lines (224 before)
  - Tracked-file drop about 226 files and about 37 MB: met, 709 -> 483 tracked files (226 deleted, 174,118 lines); model_new_2 tracked 411 -> 187; model_new_2 on disk 192 MB -> 154 MB (38 MB)
  - Core imports still resolve: met, wdt_core, wdt_kernel, wdt_jst, wdt_par in model_new_2 and wdt_core, wfr_core, wdt_md in model all import
  - Repo size before and after: git pack 105.83 MiB before and after (history kept, as expected)
- Deviations from the brief: import check run with sys.path.insert(0, '.') because the literal command cannot work under -I; the author approved the wording fix and the merge
- Risks / follow-ups: welfare_* comments remain in model/wfr_core.py and model/wdt_core.py (harmless, left alone); `OVERVIEW.md` still says the SS folder exists
- Verification: grep for SS references in .py files found only files inside SS; re-grep for welfare_(core|tables) found only comments and the shims themselves; ls-files grep empty; imports above; diff vs 16b06df stays inside Touches
- Overview sections likely needing an update: section 2 (model_new_2 line), section 6 (SS folder and model/test bullets)
- Commit / branch: fbcd969 and e9cf79c, brief/006-model-folders (notes commit follows)
```
<!-- progress:end -->
