# 165: Rehearse the whole file move on a scratch copy

- **Status:** ready; Agent 6; runs alongside 160c and 161c (it changes nothing in the real repository); feeds 162c to 164c
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
- **Done:** block 0: `path_refs.py --apply <root>` written and run on a full-history scratch clone of `3efb03b` (1082 moved, 7 duplicates removed, 321 files edited, 1666 reference lines rewritten, 4 pinned lines left alone). First suite run on the applied copy: every model suite fails at collection (depth shifts and constructed paths), as expected.
- **Next:** triage the model side (tripwire, `tests/model/{data,gate,tools,model_v3}`): fix in the scratch copy with a constructed-path pass plus hand fixes, label hunks by stage, write `rehearsal-report.md`, push (push 1). Then project side, website, `--check`, proof (push 2).
- **Decisions:** `--apply` finds references afresh in the checkout instead of reading line numbers from `file-layout-references.csv`: that csv already differs from a fresh scan on 183 (file, line, token) entries because STATUS.md and active briefs changed after it was written; the map csv lacks `docs/briefs/165c-...md` (derived from RULES, reported).
- **Gotchas:** a shallow clone fails the tripwire pack check; the scratch clone is full (810 commits). Scratch copy lives in the session scratchpad, not in the repository.
- **Resume:** `python pipeline/path_refs.py --apply <scratch clone at 3efb03b>`, then per-suite `python -m pytest -q -p no:cacheprovider tests/model/<suite>` in the scratch copy.
- **Not run:** Quarto build, `layout`, full `quick` comparison (out of scope per brief).
- **State:** block 0 done, model-side triage in progress, nothing pushed yet except this block.
<!-- progress:end -->
