# 005: Tools folder and skill archives: one home for agent instructions

- **Status:** draft
- **Author/date:** K. Ogata with the guru, 2026-11-15
- **Depends on:** 002; the author has tested the new `.skill` files
- **Read:** `Tools/`, `.claude/skills/`, `docs/agents/`, `docs/archive/`

## Goal
Leave one copy of each skill and no copy of any rule outside `docs/agents/`.

## Decisions (author, 2026-11-15)
- The five role skills are stubs (`wdt-guru`, `wdt-code`, `wdt-write`, `wdt-research`, `wdt-web`) packaged as flat `.skill` files in `Tools/`. Rules live in `docs/agents/`.
- Formatter and laconic are redundant; the librarian is a failed project kept only for reference (already in `docs/archive/`).

## Design
- After the author's test, delete from `Tools/`: `wdt-doc-coauthoring.skill`, `wdt-formatter.skill`, `wdt-laconic.skill`, `wdt-model.skill`, `wdt-reference.skill`.
- `Tools/web_search.json` is an unrelated Open WebUI script: delete or move out of the repo (the author decides).
- Decide whether `.claude/skills/<role>/SKILL.md` stays alongside the `.skill` files. They hold the same text; `.claude/skills/` is what makes a Claude Code session in the repo load them. If both stay, a script or a rule must keep them identical.
- Remove the uploaded `wdt-*` skills from the author's account so they do not clash.
- Record the result in `docs/decisions.md`.

## Touches
`Tools/`, `.claude/skills/`, `docs/decisions.md`.

## Acceptance criteria
- `Tools/` holds only current `.skill` files; `grep` finds no rule text in a stub.

## Checks to run
Unzip each `.skill` and diff against `.claude/skills/<role>/SKILL.md`.

## Out of scope
Changing role guides.

## Open questions
- Keep both `.claude/skills/` and `Tools/*.skill`, or one?

## Implementation notes
<!-- progress:start -->
- **Done:**
- **Next:**
- **Decisions:**
- **Gotchas:**
- **Resume:**
- **Not run:**
- **State:**
<!-- progress:end -->
