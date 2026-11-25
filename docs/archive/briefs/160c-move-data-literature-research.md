# 160: Move datasets, PDFs and research notes (reorganisation R2)

- **Status:** done, merged 2026-11-25
- **Author/date:** K. Ogata with the guru, 2026-11-24
- **Depends on:** 044c R1 merged and reviewed; no other branch touching these paths
- **Read:** `docs/briefs/044c-file-layout-move.md` (rules, tree, hazards); `docs/restructure/file-layout-map.md` (the reviewed table from R1)

## Goal
Datasets, literature and research notes each end up in one branch, with unique descriptive names and no byte-identical duplicates.

Rules, target tree and hazards: `docs/briefs/044c-file-layout-move.md` (R1 to R5, the tree, hazards 1 to 10); they apply here. One stage, one session, one push per block; any content change beyond paths and the R3 renames is stop-and-report; suites run in the background, never piped.

## Design
- `Research/` PDFs and the 129r PDFs to `literature/`; their converted reading copies (`docs/research/readable`) to `literature/readable/`.
- `docs/research/data` (097r, 098r, 129r) and `Rates Data` to `data/` by source (`data/uk-wealth-tables/`, `data/rates/`); the data the model reads stays for 162c (`data/input-register`, `data/country-pack-GBR`).
- The notes (`docs/research/NNNr-*.md`), `docs/hypotheses/`, `docs/model-audit/`, `docs/audit/`, `docs/model-lessons/` to `research/`.
- Duplicates: byte-identical files (the 129r PDFs and workbooks against `Research/`, `Rates Data` and 098r) reduced to one, hash-checked and listed; generic names renamed under R3 with every reader rewritten.
- Rewrite references to the moved paths; update `.gitignore` entries for the 097r workbooks and list the local files to move by hand (hazard 5).
- Check: the reference script reports none of the old paths for these; hooks, data and docs checks pass; no model file changed.

## Touches
`Research/`, `Rates Data/`, `docs/research/`, `docs/hypotheses/`, `docs/model-audit/`, `docs/audit/`, `docs/model-lessons/`, readers of those paths (docs, scripts that read the 097r data), `.gitignore` lines for them.

## Acceptance criteria
- The tree has one branch each for datasets, literature and research notes; no name repeated; no byte duplicate.
- Reference script clean for the moved paths; hooks, data, gate and docs checks pass; model suites unchanged.
- Local-only files listed with old and new paths; the duplicate list is in the report.

## Out of scope
The model's own inputs (162c); the website (161c); skills and the shared files (164c).

## Open questions
None; the agent flags any call the rules cannot settle.

## Implementation notes
<!-- progress:start -->
- **Done:** block 2: readers rewritten, research scripts re-pointed (`DIRS` maps, `HERE` to the new table folders) and re-run; the 104r cell weights file renamed under R3 with its writer and `build_gbr.py` constant. Block 1: 306 `git mv` (all 100% renames), 3 duplicates removed (`Before-the-fall.pdf`, the 129r `meanmedian...xlsx`, the 129r `totalwealthtables.xlsx`). Block 0: branch `brief/160-move-data-literature-research` from `aa367e7`; brief, 044c and the map read; 309 files of this stage identified (map rows under `Research/`, `Rates Data/`, `docs/research/`, `docs/hypotheses/`, `docs/model-audit/`, `docs/audit/`, `docs/model-lessons/`).
- **Next:** block 1 moves (`git mv`, three duplicates hash-checked and removed); block 2 reader rewrites (path rewriter of `path_rewrite_proof.py` over a subset map, then the 13 research scripts by hand); block 3 checks, friction log, change report.
- **Decisions:** moves and rewrites follow `docs/restructure/file-layout-map.csv` exactly. Out of Touches and left to their stages: `docs/EVAL_PLAN.md`, `VAL_*`, `wdt-jel-codes.md` (map: `research/`) and the bibliography in `registry/` (map: `literature/`).
- **Gotchas:** `model_v3/pack/build_gbr.py` opens moved files (only its path constants change; its NOTICE text and `NOTICE.md` are pinned by the tripwire pack tree hash, ruling 3 says stop-and-report); `pipeline/to_markdown.py` keys sources and reading copies to one root, which the split breaks (a logic change, flagged not made); `path_refs.py --check` builds its map from the current tree, so after a move it cannot see old paths (an equivalent check from the committed map is used); the tripwire needs full history.
- **Resume:** `git checkout brief/160-move-data-literature-research`; see the commits for the block reached.
- **Not run:** `extract_binaries.py` and `extract_ukea_nbs.py` (need the local NMG and UKEA workbooks).
- **State:** block 3 done, NEEDS THE AUTHOR (see the report below). Block 2 done (readers rewritten: 128 files by the proof's path rewriter, 23 research scripts by hand and re-run: 21 reproduce their tables byte for byte, 2 need local workbooks); checks and change report next (block 3).
<!-- progress:end -->
### Change report (160c)
```
Change report
- Task: brief 160c, move datasets, literature and research notes (044c stage R2)
- Files changed: 306 files moved by git mv (all 100% renames) into data/rates (7), data/uk-source-workbooks (2), data/uk-wealth-tables (097r, 098r, 129r tables), literature (PDFs, readable copies), research/{notes,tables,scripts,hypotheses,model-audit,model-lessons,scaffold-audit}; 3 byte-identical 129r copies removed. 137 files had references rewritten (proof rewriter), 23 research scripts re-pointed by hand, build_gbr.py (path constants only), cell_baseline.py, make_map.py, validate.py, tests/model_v3/test_saving_shape.py (path segments), .gitignore (097r workbooks), AGENTS.md and docs/agents (paths), docs/agents/friction-log.md (one entry).
- What is different now: datasets, literature and research notes each live in one branch; scripts that wrote beside themselves now read data/uk-wealth-tables and write research/tables; the 104r cell weights file is 104r-parameter-map-design-cell-weights.csv (R3).
- New or changed interfaces: none (run scripts from the repository root as before: python -I research/scripts/<name>.py).
- Acceptance criteria:
  1. One branch each, no name repeated: MET for sources and tables (310 files under data/, literature/, research/; 0 repeated names; 0 byte duplicates among sources). PARTLY: the two reading copies of the meanmedian workbook (literature/readable/data/098r/098r-meanmedian...-xlsx.md and .../129r/129r-meanmedian...-xlsx.md) are now byte-identical, because the 129r source was a duplicate and its header path resolves to the kept copy. Left as the map has them; proposal: drop the 129r copy when the converter is re-rooted.
  2. Reference script clean: NOT MET as stated. path_refs.py --check cannot see old paths after a move (it reads the current tree), so an equivalent scan from the committed map was used. Remaining old-path lines, all deliberate: STATUS.md (13) and OVERVIEW.md (2) (guru-owned, 164c); docs/briefs 044c and 160c (describe the move); docs/restructure/file-layout.md (design); pipeline/to_markdown.py, pipeline/check_agent_docs.py and their two tests (see Deviations); model_v3/pack/GBR/NOTICE.md and the NOTICE text in build_gbr.py (pinned, see below); research/scaffold-audit (a dated audit, left as written); one generated index header; docs/archive history. Hooks 88 passed, data suite passed, gate passed, docs check (check_agent_docs.py) rc 0.
  3. Model suites unchanged: tests/model_v3 passed after four path-only fixes (3 tests failed first because they built the old paths from segments; fixed, 17 passed); tripwire PASS (inputs, legacy, pack byte-identical, evaluation hashes); suites 10 of 10 ran, layout skipped 40 as before.
  4. Local-only files and duplicate list: below.
- Deviations from the brief: (a) no model file changed is not true to the letter: build_gbr.py path constants and tests/model_v3/test_saving_shape.py changed, because they read the moved tables; nothing else in model_v3. (b) pipeline/to_markdown.py, check_agent_docs.py and their tests were NOT changed: they key sources and reading copies to one root (docs/research); re-rooting is a logic change (stop-and-report). Today to_markdown.py --all finds nothing and the missing-copy warning is silent. (c) NOTICE.md and the NOTICE text in build_gbr.py still quote old paths: the tripwire hashes the pack tree including NOTICE.md and ruling 3 makes a pinned file stop-and-report. (d) Out of Touches and left to their stages: docs/EVAL_PLAN.md, VAL_*, wdt-jel-codes.md, the bibliography under registry/.
- Risks / follow-ups: NEEDS THE AUTHOR for (b), (c) and the duplicate reading copy. Proposals: (b) a brief to re-root the converter (source roots literature/, data/; mirror under literature/readable/); (c) allow-list the two NOTICE lines like the four pinned lines, or re-baseline the tripwire on your word; the duplicate copy goes with (b). Two scripts not re-run: extract_binaries.py, extract_ukea_nbs.py (need local NMG and UKEA workbooks); compile-checked. The branch is based on aa367e7; main has since added only STATUS, decisions, lane plan and briefs 165c/166c (no overlap), so the rebase is clean.
- Instruction friction: one entry in docs/agents/friction-log.md (--check blind after a move; NOTICE not in the pinned list; converter family; CRLF in text-mode rewrites; proof on a subset map).
- Verification: path_rewrite_proof.py on the 160c subset map: moved 204, path-only 69, removed 3, pending 0, changed 33 (all hand edits listed above: 23 scripts, 9 notes and the audit synthesis, 1 prose); 21 of 23 research scripts re-run, outputs identical to the committed tables (ignoring line endings only because the scripts write CRLF on Linux); tripwire PASS 112.8 s; run_suites all: 9 of 10 passed first, model_v3 3 failures fixed and re-run green; check_agent_docs rc 0; compileall rc 0. Not run: extract_binaries.py, extract_ukea_nbs.py, the site build (nothing under site/ changed; registry/lit-figures.yml paths only, pages suite passed).
- Overview sections likely needing an update: file layout and where data, literature and research notes live; the reading-copy workflow (to_markdown.py) once re-rooted.
- Commit / branch: brief/160-move-data-literature-research, cee3cec (+ this report). NEEDS THE AUTHOR; not merged.
```
Duplicates removed (SHA-256, first 16 hex): 0958a86d29d48864 `docs/research/data/129r/Before-the-fall.pdf` = `literature/Before-the-fall.pdf`; 8d091ade5a1572c0 `docs/research/data/129r/meanmedian...xlsx` = `data/uk-wealth-tables/098r/meanmedian...xlsx`; ae70c721b88b60ee `docs/research/data/129r/totalwealthtables.xlsx` = `data/rates/totalwealthtables.xlsx`.

Local-only files to move by hand (ignored, never tracked): `docs/research/data/097r/boe-nmg-*.xlsx`, `docs/research/data/097r/nbs.xlsx`, `docs/research/data/097r/ukea2026q2.xlsx` to `data/uk-wealth-tables/097r/` (the `.gitignore` lines now name the new place). The empty old folders (`Research/`, `Rates Data/`, `docs/research/` and the others) can be deleted locally.

