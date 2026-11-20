# Agent guides (read only what your job needs)

Start with `START_HERE.md` at the repo root.

| Job | Read |
|---|---|
| Design, positions, consistency, briefs, status | `guru.md`, then `reference/framework.md` when judging a new idea |
| Implement a brief, fix model or pipeline code | `code.md`, then `reference/code/conventions.md` and, for large-file edits, `reference/code/patch-and-test.md` |
| Draft, edit or format a paper | `writing.md`, then `reference/writing/style-guide.md`; `prose-rules.md` for the prose pass |
| Compress prose or remove AI tells | `reference/writing/prose-rules.md` |
| References, bibliography, literature coverage | `research.md`, then `reference/research/reference-workflow.md` |
| Site build, deploy, rendering problems | `web.md`, then `reference/web/preprocessing.md` or `citation-keys.md` as the task needs |
| Finish a task | `change-report.md` |
| Stop mid-task, or resume one | `handover.md` |
| An instruction or tool failed you | `friction-log.md` (append an entry) |
| Guru: keep overview and status true | `overview-maintenance.md` |
| Guru: write a brief | `brief-template.md` |

## Skills
The five role skills are stubs: `.claude/skills/<role>/SKILL.md` (10 lines, no rules) is the source and Claude Code loads it from the repo. `Tools/wdt-<role>.skill` is the same file zipped for the claude.ai account (plus `Tools/repo-scaffold.skill`). All rules live in this folder, never in a stub. After changing a stub, run `python pipeline/build_skills.py` (a zip with `wdt-<role>/SKILL.md` per role); `python pipeline/build_skills.py --check` verifies they match.

Reference files in `reference/` are long on purpose and are read only when the guide names them.

Do not open `OVERVIEW.md` in full, `docs/archive/`, `docs/model-lessons/` or finished briefs unless the task says so.
