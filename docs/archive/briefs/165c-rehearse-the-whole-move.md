# 165: Rehearse the whole file move on a scratch copy

- **Status:** done, merged 2026-11-25
- **Author/date:** K. Ogata with the guru, 2026-11-24
- **Depends on:** 044c R1 round 2 merged (it is: the map and the checks are on `main`)
- **Read:** `docs/briefs/044c-file-layout-move.md` (rules, programme, verification tiers); `docs/restructure/file-layout-map.md` and its csv files; `pipeline/path_refs.py` (`--map`, `--check`); `docs/restructure/path_rewrite_proof.py`; `docs/restructure/move_tripwire.py`; `docs/agents/friction-log.md` (the shallow-clone tripwire entry)

## Goal
Find the real breakages of the whole move before the stage agents hit them: apply the full map to a scratch copy, run the suites and the tripwire there, and hand the stage agents a grouped list of what fails and the fix for each. The real repository is not changed except for the three deliverables.

## Design
1. **Scratch copy.** A full-history clone or worktree of `origin/main` in the scratchpad, outside the repository (a shallow clone makes the tripwire report `FAIL pack`). Work only there; delete it at the end.
2. **Apply mode.** If `pipeline/path_refs.py` has no mode that applies the map (the `git mv` of every file, the R3 renames, the duplicate removals, the path-only rewrites of the reference lines, the four pinned lines left alone), add `--apply <root>` driven by `file-layout-map.csv` and `file-layout-references.csv`. This is the one change to the real repo besides the report and the patch, and the stage agents may use it.
3. **Model side first, then the rest.** Apply the whole map, but triage in this order so a token run-out still leaves something useful: (a) the model: `model/`, `tests/model`, the model tools, the pack, `data/`; run the tripwire (`move_tripwire.py`, against the baseline) and `tests/model` in the background; (b) the project side: `check_agent_docs.py`, `tests/project`; (c) the website: `tests/website` as far as it runs (no Quarto here: list the build and `layout` as not run); (d) `path_refs.py --check` and `path_rewrite_proof.py` over everything. Each suite its own `pytest` run, in the background, never piped or combined.
4. **Triage.** For every failure or error: the cause, the fix, and the stage that owns the file (160c data, literature, research; 161c website and papers; 162c model; 163c specs and results; 164c project and skills). Look at the 498 depth-based lines in `file-layout-depth.csv` (which fail and the right fix), the references of kind `other` (globs, placeholders), the readers of the 77 renamed files, and any file that finds another by a constructed name or scans a folder.
5. **Fix in the scratch copy** what can be fixed, to prove the fix, and keep the fixes as one patch, hunks labelled by stage.
6. **Two pushes.** After step 3(a) and its triage: push the `--apply` mode (if needed) and a first `rehearsal-report.md` covering the model side. If tokens remain, extend to (b) to (d) and push once more.

## Deliverables (three)
1. `pipeline/path_refs.py` `--apply <root>` (only if it was missing; tested on the scratch copy).
2. `docs/restructure/rehearsal-report.md`: the failures grouped by stage owner, each with cause and fix; the depth-based lines that need a change; what could not be tested (the Quarto build, `layout`, the full `quick` comparison).
3. `docs/restructure/rehearsal-fixes.patch`: the fixes applied in the scratch copy, hunks labelled by stage.

## Touches
`pipeline/path_refs.py` (apply mode only) and two new files in `docs/restructure/`. Nothing in the real repository moves; no model code changes.

## Acceptance criteria
- The report names every failing suite and test file after the full-map apply, with a cause, a fix and an owning stage; the model side is complete; any side not reached is listed as not run.
- The patch applies cleanly to the scratch copy and the model side's suites and tripwire pass with it.
- The scratch copy is deleted; `git status` of the real repo shows only the three files.

## Out of scope
Moving anything in the real repo; fixing content problems (a failure that is not a path problem is reported, not fixed); the Quarto build; the full `quick` run; changing the map (a map error is reported and the guru corrects it).

## Open questions
None; stop and report a map error or a failure that looks like a content problem.

Rules that apply: one block, one push per part; suites in the background, never piped; any `arm.py` or kernel change is stop-and-report (none is expected).

## Implementation notes
<!-- progress:start -->
- **Done:** `path_refs.py --apply <root>` (shared `Rewriter`), full rehearsal on a full-history scratch clone of `3efb03b`, `rehearsal-report.md`, `rehearsal-fixes.patch` (138 files, labelled by stage, applies cleanly). On the fixed copy: tripwire PASS; `tests/model` data 103, gate 17, tools 5, model_v3 408 passed; `tests/website` 201 passed, 41 skipped; proof on the apply alone: 0 changed. `tests/project`: 1 failure in a clean tree (the prose sweep, 164c).
- **Next:** NEEDS THE AUTHOR / guru: five map decisions in the report (pack folder name, pinned list, shared `Rewriter` in the proof, readable-copies place, 165c row). No auto-merge. Then merge 165c and start 160c.
- **Decisions:** `--apply` scans the checkout afresh (the references csv is stale by 199 entries); the proof was not changed (a check); its proposed change is described in the report.
- **Gotchas:** full-history clone for the tripwire; one pytest per suite; leftover empty old folders hide failures (use `git clean -fdx`); never pipe the rehearsal script into `head`.
- **Resume:** apply, then the patch, in a fresh clone.
- **Not run:** Quarto build, `layout` (40 skipped as in the baseline), full `quick` comparison.
- **State:** scratch copy and worktree deleted; branch pushed.
<!-- progress:end -->


Change report
- Task: 165c rehearse the whole move
- Files changed: `pipeline/path_refs.py` (`--apply`, `Rewriter`, `:N` suffixes, `_folder_news` ignores renamed file names); `docs/restructure/rehearsal-report.md`, `rehearsal-fixes.patch` (new); brief progress, friction log, brief suggestions
- What is different now: the stage agents have a tested apply, a grouped list of failures with fixes, and a patch
- New or changed interfaces: `python pipeline/path_refs.py --apply <scratch root>` (refuses this repo)
- Acceptance criteria: report names every failing suite per stage (met); model side complete, tripwire and four suites pass with the patch (met); patch applies cleanly (met); scratch deleted, git status shows the three files plus the brief and logs (met, with the logs as extra)
- Deviations from the brief: friction log, brief suggestions and the brief's own block are also edited (the rules ask for them); the proof was not changed
- Risks / follow-ups: five map decisions (report end); the prose sweep (164c); 50 constructed chains not individually triaged
- Instruction friction: one entry added
- Verification: tripwire, tests/model x4, tests/website, proof, check; not run: Quarto, layout, quick
- Overview sections likely needing an update: none
- Commit / branch: see push, `brief/165c-rehearse-the-whole-move`
