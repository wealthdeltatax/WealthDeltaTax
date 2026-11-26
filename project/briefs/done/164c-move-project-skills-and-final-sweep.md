# 164: Move the project documents and skills, then sweep (reorganisation R6)

- **Status:** done, merged 2026-11-26
- **Author/date:** K. Ogata with the guru, 2026-11-24
- **Depends on:** 163c merged; read `website/notes/rehearsal-report.md` (164c section)
- **Read:** `project/briefs/open/044c-file-layout-move.md` (rules, tree, hazards); `project/restructure/file-layout-map.md` (the reviewed table from R1)

## Goal
All project management material is under `project/`, the skills are rewritten and rebuilt, every remaining old path is rewritten and the whole programme's acceptance criteria are met.

Rules, target tree and hazards: `project/briefs/open/044c-file-layout-move.md` (R1 to R5, the tree, hazards 1 to 10); they apply here. One stage, one session, one push per block; any content change beyond paths and the R3 renames is stop-and-report; suites run in the background, never piped.

## Design
- `docs/` remainder to `project/`: STATUS, OVERVIEW, START_HERE, decisions, todo, lane plan, briefs (open and done, from `project/briefs/done`), agents, housekeeping, restructure, the loose notes (defaults in 044c), the archive remainder; `Tools/` to `project/skills/`.
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
`docs/` remainder, `Tools/`, `.claude/`, `AGENTS.md`, `README.md`, `project/START_HERE.md`, `project/STATUS.md`, `project/OVERVIEW.md`, `.gitignore`, shared files; nothing in `model/`, `data/`, `results/` except path references.

## Acceptance criteria
- The programme's acceptance criteria all met (044c).
- `check_agent_docs.py` and all suites pass (R5 excepted, listed); skills rebuilt; skill change list in the report.

## Out of scope
Editing archived briefs or decision history; the Actions workflow; the speed-up briefs.

## Open questions
None; the agent flags any call the rules cannot settle.

## Implementation notes
<!-- progress:start -->
- **Done:** all blocks; rebased on main 5a4be18; checks as in the change report.
- **Next:** the author decides on the merge (diff outside Touches, see the report); then the guru updates OVERVIEW and STATUS.
- **Decisions:** converter lives in `project/tools/`; reading copies mirror the source path under `literature/readable/`; duplicate 129r copy dropped.
- **Gotchas:** `run_suites.py` does not discover `tests/project/tools` and `tests/model/tools`.
- **Resume:** `git checkout brief/164-move-project-skills-and-final-sweep`.
- **Not run:** the full `quick` byte comparison (057c not merged).
- **State:** finished, not merged
<!-- progress:end -->

## Change report
- Task: 164c, move the project documents and skills to `project/`, re-root the reading copies, sweep the old paths (reorganisation R6)
- Files changed: 292 renamed, 72 edited, 6 added, 7 deleted (counted by `git status` in the scratch copy before commit 1). Moves: `docs/` remainder to `project/` (briefs open and `done/`, agents, housekeeping, restructure, STATUS, OVERVIEW, START_HERE, decisions, todo, lane plan) and to `website/notes/` (site notes); `Tools/` to `project/skills/`; `pipeline/{build_skills,check_agent_docs,path_refs}.py` to `project/tools/`; `registry/{references.bib,internal.json}` to `literature/`; `tests/hooks/{test_build_skills,test_check_agent_docs}` to `tests/project/tools/`. Also moved, outside the map: `to_markdown.py` to `project/tools/`, its test to `tests/project/tools/`, and the 37 reading copies to the new mirror layout.
- What is different now: the repository root holds only the allowed files and folders; every project document is under `project/`; the five `.skill` archives are rebuilt from the rewritten stubs; reading copies live at `literature/readable/` (a file under `data/` keeps its repository path plus `.md`; a file under `literature/` drops that folder); `check_agent_docs.py` warns about binaries under `data/` and `literature/` that lack a copy (it was `docs/research`). No number changed; the tripwire equals the baseline.
- New or changed interfaces: `python -I project/tools/to_markdown.py <file>` (was `website/build/to_markdown.py`); `python -I project/tools/build_skills.py` writes `project/skills/`; `python project/tools/check_agent_docs.py`; `python project/tools/path_refs.py`; the web build reads `literature/references.bib`, `literature/internal.json` and writes `literature/references.json`. The proof takes `--allow` by lines (names with spaces) and honours it for binary files.
- Acceptance criteria: root holds only the allowed entries: met. No name repeated outside the R3 exceptions: met except fixtures (pack fixture, spoke fixtures), `conftest.py`, `__init__.py`, `README.md`, `SKILL.md` and `NOTICE.md`; one byte-identical duplicate remains, `data/country-packs/GBR/source/jst_r6.json` equal to `data/jst/jst_r6.json`, because the pack tree is hashed (pinned bytes). Reference script: no old path outside archived briefs, decisions, the map's own data, the scaffold audit and the allow-listed pinned lines; the tripwire pairs and the `tests/model/tools` throwaway tree keep old names on purpose. Depth-based paths: `build_skills`, `check_agent_docs`, `path_refs` (root now `parents[2]`) and two tests (`parents[3]`) fixed; the rest verified. Suites pass; the gate checker gives the same result as on `main` (pages closed, only its path text updated).
- Deviations from the brief: (1) the converter moved to `project/tools/` (the brief asked for a decision); (2) `check_gate.py` B4 to B6 names `website/build/...` (it said `pipeline/...`, files that never existed); (3) the diff touches `website/build/{bib_to_json,config,pdf,zenodo_upload,wdt_crosslinks,pages/site_index,pages/retired}.py`, `research/scripts/*.py`, `tests/` and `model/tools/check_gate.py`, which the brief's Touches do not list, because they read the moved files; (4) `docs/hypotheses`-type history lines in the friction log and `STATUS.md` keep their old names (dated history).
- Risks / follow-ups: `run_suites.py` does not discover `tests/project/tools` and `tests/model/tools` (no conftest, two suites named `tools`): run them by hand, or give discovery a rule; `OVERVIEW.md` still describes the old layout in its file-layout section (the guru edits it); `path_refs.py --check` prints folder-level noise on a moved tree (it builds its rows from the current tree), so the sweep used a scan against the committed map; 24 binaries under `data/` and `literature/` have no reading copy yet (warnings only); `.github/workflows/` untouched (out of scope).
- Instruction friction: none new beyond the friction-log entries already present.
- Verification: `check_agent_docs.py` exit 0; `compileall` clean; clean tree (`git clean -fdx`) before the runs; suites (one pytest each, background): model/data, model/gate, model/tools, project/tools, website cards, hooks, glossary, layout, nav, pages, retired all pass, model_v3 408 passed (9 min); `move_tripwire.py` PASS (inputs 0.0 s, legacy 54.2 s, pack 3.3 s, evaluation 50.7 s); `path_rewrite_proof.py --base origin/main` with the stage map `project/restructure/file-layout-map-164c-base.csv` and `--allow project/restructure/proof-allow-164c.txt`: moved 978, path-only 61, removed 1, changed 71 (all declared), PASS; local Quarto build (scrape, glossary, anchors, preprocess, `quarto render _build`) BUILD_OK; `check_gate.py --all` same as `main`. Not run: the full `quick` byte comparison (057c not merged, as 044c says).
- Skill lines changed (for the account skill edits): in each of the five stubs (`wdt-code`, `wdt-guru`, `wdt-research`, `wdt-web`, `wdt-write`) two lines: "Read `AGENTS.md`, then `project/agents/agent-<role>.md`, then only the files that guide names..." (was `docs/agents/<role>.md`) and "End every task with the change report (`project/agents/change-report.md`)." (was `docs/agents/change-report.md`).
- Local-only files to move by hand (old to new): any local `docs/` content not tracked (scratch notes) to `project/`; `Tools/*.skill` to `project/skills/`; `registry/references.json` (generated) to `literature/`; `_build/` and `print/` are ignored and regenerate; `Rates Data/` and `Research/` were handled by 160c.
- Overview sections likely needing an update: the whole file-layout block, the registry line, the agents table (paths), STATUS entries naming `docs/`.
- Commit / branch: `brief/164-move-project-skills-and-final-sweep`, pushed; NOT merged: `NEEDS THE AUTHOR` because the diff goes beyond the brief's Touches (list under Deviations 3), and `main` moved by one docs commit since the branch was cut.
