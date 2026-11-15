# Decisions digest

One entry per finished brief or settled question, at most 8 lines each. Newest first. Maintained by the guru.

## 2026-11-15: tools and skills cleanup (brief 005)
- Deleted `Tools/SS/` (old doc-coauthoring, formatter, laconic, model and reference skills, `web_search.json`); the author had moved them there.
- `Tools/` holds the five role `.skill` files and `repo-scaffold.skill`. Each role file matches `.claude/skills/<role>/SKILL.md` (checked); both locations stay, `.claude/skills/` is the source.
- Still the author's: remove the old uploaded `wdt-*` skills from the claude.ai account.

## 2026-11-15: agent scaffold
- Roles are guru, code, writing, research, web. Skills are repo stubs in `.claude/skills/` that point at `docs/agents/`.
- Formatter and laconic skills folded into the writing role; the co-authoring skill became `wdt-write`.
- The librarian skill was a failed project and is kept only as an archive.
- `SS` ("superseded") folders deleted; history is in git and the author's separate backup.
- Model v1/v2 is legacy; a third refactor starts from a clean slate (brief 001).
- `model/OUTPUTS/` stays tracked; old paper-number references are not being fixed because the papers are being rewritten.
