# 009: Retire the legacy models (step R0 of the reorganisation)

- **Status:** ready now (057c is paused and 148c has merged; 009c touches none of their files); Agent 3; runs before 044c L1 (rewritten 2026-11-24)
- **Author/date:** K. Ogata with the guru, 2026-11-24
- **Depends on:** nothing open (148c merged; 057c paused and independent); the author's ruling of 2026-11-24 (remove from the tree, keep in git history; one parallel pair later)
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
- **Done:** all design steps 2 to 5 on `brief/009-retire-legacy-models`; local tag `legacy-models-2026-11` on `16b26e4`; ten suites pass as at the baseline.
- **Next:** the author pushes the tag (`git push origin legacy-models-2026-11`; the session proxy refused it with HTTP 403) and asks for the merge.
- **Decisions:** the pack, its `source` strings and `levers.json` untouched (a re-run of `build_gbr.py` gives no diff); `wid_download.py` and `WID_Data_Guide.md` moved byte-identical (their internal `wid_out` and removed-script mentions are unchanged: content change, out of scope).
- **Gotchas:** `build_gbr.py` needs a full clone (done with `git fetch --unshallow`); `site/_quarto.yml` `resources:` still lists `model/*` files (outside Touches).
- **Resume:** `git checkout brief/009-retire-legacy-models`; `python pipeline/run_suites.py`.
- **Not run:** the site build and render (no Quarto here), the `layout` suite (skipped, needs a build).
- **State:** NEEDS THE AUTHOR (tag not on the remote)
<!-- progress:end -->

Change report
- Task: brief 009c, retire the legacy models (step R0)
- Files changed: removed `model_v1/` and `model_v2/` (307 files, 134.9 MB; `audit_d0` was inside `model_v2/`); moved with identical content `data/jst/jst_r6.json` (the three copies, in `model_v1`, `model_v2` and the pack, had the same hash), `data/wid/wid_long.csv` (52.9 MB), `wid_download.py`, `WID_Data_Guide.md`; `model_v3/pack/build_gbr.py` (two read paths and the docstring; the `source` and `FROM` strings that become manifest text are unchanged); `docs/model-v3/returns/common.py` (path); `pipeline/config.py` (`MODEL_DIR` removed), `pipeline/preprocess.py` (the two dead copy blocks and `_TOOL_RUNTIME_SUFFIXES` removed), `pipeline/transforms.py` (a comment); `OVERVIEW.md`, `README.md`, `START_HERE.md`, `AGENTS.md`, `docs/agents/code.md`, `docs/agents/reference/code/conventions.md` and `patch-and-test.md` (a one-line "removed, see tag" each), `docs/wdt-site-architecture.md`; `docs/decisions.md` (one entry). `.gitignore` needed no change.
- What is different now: the tree has no `model_v1`, `model_v2` or `audit_d0`; `data/` holds the two kept inputs; the site build copies no model assets or figures.
- Acceptance criteria: tree without the three folders: MET; the four kept files exist: MET; `build_gbr.py` reproduces the pack byte for byte (run in a full clone; `git status` shows only `build_gbr.py` changed): MET; all ten suites pass (data 103, gate 17, cards 8, model_v3 408, hooks 88, glossary 27, layout 40 skipped, nav 59, pages 28, retired 13), identical to the baseline run on `16b26e4`, so the legacy digest and the `inputs.json` hash pass; `check_agent_docs.py` passes (exit 0). NOT MET: the tag on the remote: `git push origin legacy-models-2026-11` was refused (HTTP 403 from the session proxy, a policy denial, not retried or routed around); the tag exists locally on `16b26e4`.
- Red checks (R5), expected: not measured, because no Quarto render ran here; known by reading: the site's old calculators fetch `/model/*` (`taxpayer`, `revenue`, `ldw`) and `site/_quarto.yml` lists `model/wdt_core.py`, `model/rates_model.py` (already gone), `model/ldw_core.py` and `model/WDT_Params.toml` under `resources:`; the old papers' figures (`figures/*.png`) lose their source (`model_v1/OUTPUTS`, 95 files). The `layout` suite is skipped without a build.
- Restore: `git checkout legacy-models-2026-11 -- model_v2` (and `-- model_v1`), or by commit `git checkout 16b26e4 -- model_v1 model_v2`.
- Deviations: none from the design; the tag is local until the author pushes it. `docs/decisions.md` records the commit hash for that reason.
- Instruction friction: one entry in `docs/agents/friction-log.md` (tag push refused).
- Verification: as above; not run: the site build and render.
- Overview sections likely needing an update: OVERVIEW.md section 2 (repository map; edited here for the removed folders only), 044c's map.
- Commit / branch: `brief/009-retire-legacy-models`; not merged (the tag criterion is unmet and the author asks for merges).
