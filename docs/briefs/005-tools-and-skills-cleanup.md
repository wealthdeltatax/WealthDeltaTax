# 005: Tools folder and skill archives: one home for agent instructions

- **Status:** draft (blocked on the author testing the new `.skill` files)
- **Author/date:** K. Ogata with the guru, 2026-11-15
- **Depends on:** 002 (merged); the author has tested the new `.skill` files. Order: after 003, 004, 006, 008; independent of 001.
- **Read:** `Tools/`, `.claude/skills/`, `docs/agents/`, `docs/archive/`

## Goal
Leave one copy of each skill and no copy of any rule outside `docs/agents/`.

## Decisions (author, 2026-11-15)
- The five role skills are stubs (`wdt-guru`, `wdt-code`, `wdt-write`, `wdt-research`, `wdt-web`) packaged as flat `.skill` files in `Tools/`. Rules live in `docs/agents/`.
- Formatter and laconic are redundant; the librarian is a failed project kept only for reference (already in `docs/archive/`).

## Design
Triage (brief 002) verified: the SKILL.md inside each of the five current `Tools/*.skill` archives is byte-identical to `.claude/skills/<role>/SKILL.md`, and each is 10 lines with no rule text. `Tools/` is 152 KB, of which 98 KB is the five files to delete; `Tools/web_search.json` (12 KB) is referenced by nothing in the repo.

- After the author's test, delete from `Tools/`: `wdt-doc-coauthoring.skill`, `wdt-formatter.skill`, `wdt-laconic.skill`, `wdt-model.skill`, `wdt-reference.skill`.
- `Tools/web_search.json` is an unrelated Open WebUI script: delete or move out of the repo (the author decides).
- Recommended: keep `.claude/skills/<role>/SKILL.md` as the source (Claude Code loads it from the repo) and treat `Tools/*.skill` as packages for the claude.ai account, rebuilt from it. Add a one-line rule to `docs/agents/README.md` saying so, and a small check (unzip and diff) that the two match. The alternative is to delete `Tools/` and upload from `.claude/skills/` directly.
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
- Keep both `.claude/skills/` and `Tools/*.skill` (recommended, with the diff check), or one?
- `Tools/web_search.json`: delete or move out of the repo?

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
