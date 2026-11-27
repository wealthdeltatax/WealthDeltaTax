# Notes for agents working on this repo

Read `project/START_HERE.md`, then the guide for your role in `project/agents/`. This file holds only rules every role shares; role rules live in the role's own guide.

## Roles
- **guru**: design partner, owns docs, overview, status, briefs, scaffold health.
- **code**: model and pipeline code, tests, tools.
- **writing**: drafts, edits, formats and compresses the papers.
- **research**: references, bibliography, literature.
- **web**: Quarto site, build, deploy.
- **The author** (K. Ogata) decides open questions.

## Who owns what
By path; where a task crosses a line, name one change owner and the other role as reviewer, and do not edit the same file in parallel.

| Path | Owner | Note |
|---|---|---|
| `model/`, `tests/`, `project/tools/`, `results/` | code | tests: others propose, code implements |
| `website/`, `.github/workflows/` | web | no change to paper claims |
| `papers/legacy/` | writing | substantive argument changes need the author |
| `literature/references.bib`, reference records, `research/`, `literature/` | research | author-controlled fields need confirmation |
| `project/` (overview, status, briefs, agents, skills), `model-specs/` | guru | does not override the rows above |
| Unclear or cross-role | guru coordinates | ask the author if it changes substance |

## Git
- `main` deploys the live site on every push (the workflow runs only on `main`, never on a branch). Push to `main` only by the auto-merge rule below, or for guru docs-only edits.
- One branch per task: `brief/NNN-slug` or `fix/<slug>`, from the latest `main`. Commit and push to the branch.
- Never force-push `main`. `git pull --rebase` before pushing.
- Branch only from a fresh main: `git fetch`, then `git checkout main && git reset --hard origin/main` (nothing of yours on local main), then branch. Do not rely on a local main you have not just reset.
- Never pipe `git rebase`, `git push` or `git merge` through `tail` or `head`: the pipe hides the exit code and the next command runs mid-conflict. Run it bare, then `git status -sb`. After a merge to `main`, do not rebase older commits onto it; if a rebase replays commits already merged, `git rebase --abort` and fast-forward instead.
- `project/STATUS.md` and `project/lane-plan.html` are edited by several agents and conflict often. Fetch immediately before editing them, keep the edit to your own lines, and on a conflict take upstream and reapply your lines. Do not resolve by keeping both sides.
- A stop-hook warning of unpushed commits is checked, not trusted: `git ls-remote origin <branch>` against `git rev-parse HEAD`. If they match, say it is stale and do not re-push.
- Commit message: `type(scope): imperative summary`; types `feat fix refactor docs chore perf`. Stage specific files; one logical change per commit.

## Auto-merge
When a brief is finished, its agent merges its own branch into `main`; the author does not need to approve.
- **Merge when all hold:** every acceptance criterion is met and measured; every check the brief names has run and passed; the change report is written and committed; the diff stays inside the brief's `Touches` (plus `project/agents/friction-log.md`); no open question for the author remains.
- **How:** `git fetch`, rebase the branch on `origin/main`, re-run the brief's fast checks if the rebase brought in changes, then `git push origin HEAD:main`. Fast-forward only; never force. Then say "brief NNN merged, ready to retire" in the change report.
- **Before merging a change that affects the site** (anything under `website/`, `data/input-register/`, `literature/`, `model/`, `.github/`): the local build named in the brief must pass first, because the push deploys at once. After the push, watch the Action; if it fails, revert the merge commit on `main` immediately and report.
- **Do not merge, leave the branch pushed and say `NEEDS THE AUTHOR`, when:** a criterion is unmet or a check was not run; the brief says the author reviews; the diff touches `papers/legacy/` (paper text) or deletes tracked files the brief does not name; a rebase conflict needs a judgement call.
- The guru reviews after the merge (criteria with numbers, status, decisions entry) and may revert.

## Skills
Role skills are stubs that point here. To change how a role behaves, edit the instructions the stub points to (`AGENTS.md`, `project/agents/`), never the skill, and do not propose skill edits for a rule, a routine or a path: a rule written in a stub is not read by the other agents. The stub changes only if the file it points to is renamed or moved (`project/agents/README.md` says how).

## Generated files (never edit by hand)
`_build/`, `_site/`, `website/registry/anchors.yml`, `website/registry/crosslinks.json`. Change the source and regenerate.

## Reading
- Router first, then your role guide, then only the files the task names. Do not open `project/briefs/done/` or `research/model-lessons/`.
- `project/OVERVIEW.md` is a map and can be out of date; the files are the truth. Read by section.
- A PDF, Office file, ODS or RTF you need to read: convert it first with `python -I project/tools/to_markdown.py file` and read the Markdown (details and the ODS/RTF route in `project/agents/agent-research.md`). Do not Read the raw binary.
- `papers/legacy/` is canonical. Never rewrite a paper to make a check pass.

## Finishing
- End every task that changed files with the change report (`project/agents/change-report.md`). A question answered or a review given in the reply needs no report.
- A session can end at any time: checkpoint as `project/agents/handover.md` says.
- If a result misses its target, say so with numbers. Do not change the check to make it pass.
- When an instruction, workflow or tool fails you (missing or stale rule, command that does not work as written, forced guess), append an entry to `project/agents/friction-log.md` at once; it is always allowed in a brief's `Touches`. Name it in the change report.
- A problem outside your brief that needs its own brief: do not fix it. Append an entry to `project/brief-suggestions.md` (format at the top of that file) and mention it in the change report.
- If the task conflicts with the repo or is ambiguous on something that matters, stop and ask with a proposed resolution.
- Only the guru edits `project/OVERVIEW.md` and `project/STATUS.md`; others report changes and flag drift.
