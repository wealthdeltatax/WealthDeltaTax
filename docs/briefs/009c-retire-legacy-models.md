# 009: Retire the legacy models (step R0 of the reorganisation)

- **Status:** ready once 057c and 148c have merged and no other branch is open; Agent 3; runs before 044c L1 (rewritten 2026-11-24)
- **Author/date:** K. Ogata with the guru, 2026-11-24
- **Depends on:** 057c and 148c merged; the author's ruling of 2026-11-24 (remove from the tree, keep in git history; one parallel pair later)
- **Read:** `docs/briefs/044c-file-layout-move.md` (rules R4, R5); `model_v3/pack/build_gbr.py` (it reads `model_v2/jst_r6.json` and `model_v2/wid_out/wid_long.csv`); `pipeline/config.py` and `pipeline/preprocess.py` (they read `model_v1`).

## Goal
Take the legacy models out of the tree, keeping what model v3 still reads, so the move that follows is smaller and the duplicate names are gone. History is the archive.

Rules, target tree and hazards: `docs/briefs/044c-file-layout-move.md` (R1 to R5, the tree, hazards 1 to 10); they apply here. One stage, one session, one push per block; any content change beyond paths and the R3 renames is stop-and-report; suites run in the background, never piped.

## Design
1. **Tag first.** Tag the current `main` commit `legacy-models-2026-11` and push the tag; record it in `docs/decisions.md`. Nothing below is lost: the tag restores everything.
2. **Keep what v3 reads.** `jst_r6.json` (one copy, to `data/jst/`), `wid_long.csv` (52.9 MB, to `data/wid/`) and the script that regenerates it, `wid_download.py` (to `data/wid/`), and `WID_Data_Guide.md` (to `data/wid/`). `model_v3/pack/build_gbr.py` is repointed to those two paths (path changes only); the pack's own `GBR/source/jst_r6.json` copy and every pack file stay byte-identical, including the `source` strings in `manifest.json` (they are citations of where the data came from). Check: running `build_gbr.py` reproduces the pack byte for byte; if it does not, stop and report.
3. **Remove from the tree.** All of `model_v2/` except the three kept files above (code, `RATES`, `EVAL`, `VAL`, `test`, `audit_d0`, the rest of `wid_out`, the code and README reference docs) and all of `model_v1/` (code, parameters, `OUTPUTS` figures, the second `jst_r6.json`). The duplicate names (`wdt_*.py`, `8_2_RATES_*`, `WDT_Params.toml`, `jst_r6.json`) go with them.
4. **Fix the readers.** `pipeline/config.py` and `pipeline/preprocess.py` skip a missing `model_v1` already; remove the dead reads. The site's old calculators and the old papers' figures lose their model assets (R5: accepted, listed in the report). Active docs (`OVERVIEW.md`, `README.md`, `START_HERE.md`, `AGENTS.md`, `docs/agents/*`, `docs/wdt-site-architecture.md`) say "removed, see tag `legacy-models-2026-11`" where they named the legacy folders; archived briefs and decision history are not edited. `check_agent_docs.py` passes. `docs/model-lessons/` stays (research).
5. **Report.** Size removed (files, MB), the list of red checks (R5), the tag, and a one-line note for the author: how to restore (`git checkout legacy-models-2026-11 -- model_v2`).

## Touches
`model_v1/`, `model_v2/` (removals and the three moves), `model_v3/pack/build_gbr.py`, `pipeline/config.py`, `pipeline/preprocess.py`, `.gitignore`, active docs named above, `docs/decisions.md`.

## Acceptance criteria
- The tag exists on the remote; `model_v1`, `model_v2` and `audit_d0` are not in the tree.
- `data/jst/jst_r6.json`, `data/wid/wid_long.csv`, `wid_download.py` and `WID_Data_Guide.md` exist; `build_gbr.py` reproduces the pack byte for byte.
- The legacy digest, the `inputs.json` hash and all model suites pass; any web check that fails because it read `model_v1` is listed (R5); `check_agent_docs.py` passes.
- Change report lists size removed and the restore command.

## Out of scope
Moving anything else (044c L1 onward); deleting history; the pack's files; the site's content.

## Open questions
None; the agent flags any call the rules cannot settle.

## Implementation notes
<!-- progress:start -->
- **Done:**
- **Next:**
- **Decisions:**
- **Gotchas:**
- **Resume:**
- **Not run:**
- **State:** not started
<!-- progress:end -->
