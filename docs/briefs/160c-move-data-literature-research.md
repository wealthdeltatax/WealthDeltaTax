# 160: Move datasets, PDFs and research notes (reorganisation R2)

- **Status:** ready (044c R1 merged and settled); Agent 4; runs in parallel with 161c; the authority is `docs/restructure/file-layout-map.md` and its csv
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
- **Done:** block 0: branch `brief/160-move-data-literature-research` from `aa367e7`; brief, 044c and the map read; 309 files of this stage identified (map rows under `Research/`, `Rates Data/`, `docs/research/`, `docs/hypotheses/`, `docs/model-audit/`, `docs/audit/`, `docs/model-lessons/`).
- **Next:** block 1 moves (`git mv`, three duplicates hash-checked and removed); block 2 reader rewrites (path rewriter of `path_rewrite_proof.py` over a subset map, then the 13 research scripts by hand); block 3 checks, friction log, change report.
- **Decisions:** moves and rewrites follow `docs/restructure/file-layout-map.csv` exactly. Out of Touches and left to their stages: `docs/EVAL_PLAN.md`, `VAL_*`, `wdt-jel-codes.md` (map: `research/`) and the bibliography in `registry/` (map: `literature/`).
- **Gotchas:** `model_v3/pack/build_gbr.py` opens moved files (only its path constants change; its NOTICE text and `NOTICE.md` are pinned by the tripwire pack tree hash, ruling 3 says stop-and-report); `pipeline/to_markdown.py` keys sources and reading copies to one root, which the split breaks (a logic change, flagged not made); `path_refs.py --check` builds its map from the current tree, so after a move it cannot see old paths (an equivalent check from the committed map is used); the tripwire needs full history.
- **Resume:** `git checkout brief/160-move-data-literature-research`; see the commits for the block reached.
- **Not run:** everything below block 0.
- **State:** block 0 done, nothing moved yet.
<!-- progress:end -->
