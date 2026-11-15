# 006: Model folders: remove superseded material, backups and in-folder duplicates

- **Status:** ready
- **Author/date:** K. Ogata with the guru, 2026-11-15
- **Depends on:** 002 (merged). Does not wait for 001. Order: parallel with 003s, 004s, 008g. Must be merged before 010s, which renames the folders, and before 001c. Cross-folder decisions (`jst_r6.json`, `wdt_md.py`, data dumps, legacy reference docs) are in brief 009c, now parked: the author keeps them for now (2026-11-15).
- **Read:** `docs/briefs/002-repo-triage.md` (findings below), `model_new_2/` and `model/test/` directory listings. Nothing else need be opened.

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
- B: delete the `welfare_*` files. Checkpoint: branch pushed; check: `python -I -c "import wfr_core"` run from inside `model/` still works.

## Acceptance criteria
- No tracked `.bak`, `SS` or `_backups` path remains under `model/` or `model_new_2/`.
- Expected tracked-file drop of about 226 files and about 37 MB (`du -sh model_new_2/SS` is 37 MB); report the actual number from `git ls-files` and `du`.
- `model/` and `model_new_2/` core imports still resolve.
- Repo size reported before and after (`git count-objects -vH`; the pack will not shrink because history stays).

## Checks to run
`git ls-files` greps above; `python -I -c "import wfr_core"` run from inside `model/`. The model run scripts are not run (they take long and are legacy).

## Out of scope
Rewriting git history to shrink the pack (the pack is 106 MB; ask the author if that matters). Anything in brief 009.

## Open questions
- None blocking. If any non-`SS` file imports from an `SS` path, stop and ask.

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
