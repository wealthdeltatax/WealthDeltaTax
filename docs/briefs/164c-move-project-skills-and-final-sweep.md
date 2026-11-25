# 164: Move the project documents and skills, then sweep (reorganisation R6)

- **Status:** draft; released after 163c has merged; Agent 3
- **Author/date:** K. Ogata with the guru, 2026-11-24
- **Depends on:** 163c merged; read `docs/restructure/rehearsal-report.md` (164c section)
- **Read:** `docs/briefs/044c-file-layout-move.md` (rules, tree, hazards); `docs/restructure/file-layout-map.md` (the reviewed table from R1)

## Goal
All project management material is under `project/`, the skills are rewritten and rebuilt, every remaining old path is rewritten and the whole programme's acceptance criteria are met.

Rules, target tree and hazards: `docs/briefs/044c-file-layout-move.md` (R1 to R5, the tree, hazards 1 to 10); they apply here. One stage, one session, one push per block; any content change beyond paths and the R3 renames is stop-and-report; suites run in the background, never piped.

## Design
- `docs/` remainder to `project/`: STATUS, OVERVIEW, START_HERE, decisions, todo, lane plan, briefs (open and done, from `docs/archive/briefs`), agents, housekeeping, restructure, the loose notes (defaults in 044c), the archive remainder; `Tools/` to `project/skills/`.
- Rewrite `.claude/skills`, `AGENTS.md`, `project/agents/*`, README, START_HERE, active briefs and the lane-plan build; rebuild the `.skill` files with `build_skills.py`; list every changed skill line in the report so the guru can propose the account skill edits.
- Final sweep: the reference script over the whole tree, the duplicate-name script, the root check; fix what remains; the `check_agent_docs.py` token check.
- Check the whole programme's acceptance criteria (044c), with the tiers and one final background `quick` byte comparison; report any red check (R5), the local files to move by hand and the skill lines.

## Added from the rehearsal and the merges (2026-11-25)
- **Prose sweep by hand:** the rehearsal found 37 `check_agent_docs.py` findings that name an old folder whose files went to several places (`source/` 9, `pipeline/` 7, `model_v3/` 5, `docs/research/` 5, `docs/archive/` 4, `site/` 3, `docs/` 3, `registry/` 1), mostly in `AGENTS.md` (14) and `project/START_HERE.md` and `project/agents/*.md`: name each target folder.
- **Reading-copy converter:** `website/build/to_markdown.py` (it landed there with the web scripts) and `check_agent_docs.py --all` still scan `docs/research`; re-root them to `literature/` and `data/`, write readable copies under `literature/readable/`, drop the duplicate 129r reading copy, and decide the converter's home (a research or project tools folder suits its type better than `website/build/`); the file name `readable-copies-index.md` is a constant in the tool.
- **Skills:** the five `.skill` archives are generated from stubs the rewrite changes; regenerate (`project/skills/*.skill`).
- **Throwaway trees in project tests** keep their own paths (rehearsal rule); run `git clean -fdx` before the final run; the project test `test_cli_exit_status_and_real_repo_is_clean` passes only in a clean tree.

- **Proof allow file:** `path_rewrite_proof.py` prints FAIL for the declared edits unless given an `--allow` list; add the list for 162c's 72 declared edits so the final proof prints PASS; `file-layout-map.md` still says four pinned lines (there are more, see `PINNED_ALLOWED`); `path_refs.py --check` truncates at 50 lines.

## Touches
`docs/` remainder, `Tools/`, `.claude/`, `AGENTS.md`, `README.md`, `START_HERE.md`, `STATUS.md`, `OVERVIEW.md`, `.gitignore`, shared files; nothing in `model/`, `data/`, `results/` except path references.

## Acceptance criteria
- The programme's acceptance criteria all met (044c).
- `check_agent_docs.py` and all suites pass (R5 excepted, listed); skills rebuilt; skill change list in the report.

## Out of scope
Editing archived briefs or decision history; the Actions workflow; the speed-up briefs.

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
