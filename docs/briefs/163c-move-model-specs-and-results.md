# 163: Split the model documents into specs and results (reorganisation R5)

- **Status:** draft; released after 162c has merged; Agent 6
- **Author/date:** K. Ogata with the guru, 2026-11-24
- **Depends on:** 162c merged
- **Read:** `docs/briefs/044c-file-layout-move.md` (rules, tree, hazards); `docs/restructure/file-layout-map.md` (the reviewed table from R1); `docs/model-v3/outputs.yml` and its readers; `docs/restructure/rehearsal-report.md` (the 162c and 163c sections)

## Goal
`docs/model-v3/` (188 files) is split by type: what the model should do goes to `model-specs/`; every run report and its csv go to `results/<study>/` with unique names.

Rules, target tree and hazards: `docs/briefs/044c-file-layout-move.md` (R1 to R5, the tree, hazards 1 to 10); they apply here. One stage, one session, one push per block; any content change beyond paths and the R3 renames is stop-and-report; suites run in the background, never piped.

## Design
- Specifications (architecture, acceptance, metrics, the outputs manifest `outputs.yml`, input-register docs, country-pack spec, drivers, design notes, `what-we-know`) to `model-specs/`.
- Reports and csv of each study (death-phases, feasibility-map, household-arm-run, -validation, -lien, -paths, f1-diagnostic, f1-household, cell-baseline, tornado, returns, run-cost, wealth-ratio-diagnostic, of1-ck1, and the others) to `results/<study>/`, each file renamed under R3 so no name repeats (phase, fund and variant in the name: `f1-phases06-safe-grid.csv`). Every reader (manifest, tests, drivers in `model/studies/`, docs) rewritten.
- Rule of thumb for the call on each file: a document that says what the model is meant to do is a spec; a file that reports what a run produced is a result; the script that makes it is a study driver (already moved).
- Check: the 044c tiers; the output manifest unchanged but for paths. At the end, one full `quick` run in the background (44 minutes) compared byte for byte with the pre-move reference; it blocks closing the programme, not this merge.

## Added from the rehearsal (165c, 2026-11-25)
- Only three pinned lines reach this stage (`inputs.md` line 145, the `outputs.yml` shortcodes comment, the `inputs.md` readers); they keep their old text (162c lists them); nothing else in `model-specs/` or `results/` is read by code beyond depth and constructed paths.
- A study folder that holds both a driver and its outputs is split: the driver is in `model/studies/<study>` (162c), the reports and csv go to `results/<study>/`. A variable or `sys.path` line naming the old folder cannot be rewritten as one path: `sys.path` means the code folder; `VAR / 'file'` becomes that file's own new path. Check every driver for output paths it writes.
- Use `git clean -fdx` before the stage's final run; throwaway trees built by tests keep their paths.
- The 163c section of `rehearsal-fixes.patch` is a guide only (it is built on the pre-160c tree).

## Touches
`docs/model-v3/` (all), `model/studies/` (paths), tests and docs that read them.

## Acceptance criteria
- `model-specs/` holds only specifications and `results/` only run outputs; no name repeated in either.
- Suites and `check_agent_docs.py` pass; manifest unchanged but for paths; tripwire and path-rewrite proof clean; the `quick` comparison reported when it finishes.

## Out of scope
Changing any number or text except paths and R3 names; project documents and skills (164c).

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
