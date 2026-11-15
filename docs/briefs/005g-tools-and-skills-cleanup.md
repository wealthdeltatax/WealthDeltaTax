# 005: Tools folder and skill archives: one home for agent instructions

- **Status:** built (merged)
- **Author/date:** K. Ogata with the guru, 2026-11-15
- **Depends on:** 002. Order: guru lane, any time; must be merged before 001c starts.
- **Read:** `Tools/`, `.claude/skills/`, `docs/agents/`, `docs/archive/`

## Goal
Leave one copy of each skill and no copy of any rule outside `docs/agents/`.

## Decisions (author, 2026-11-15)
- The five role skills are stubs (`wdt-guru`, `wdt-code`, `wdt-write`, `wdt-research`, `wdt-web`) packaged as flat `.skill` files in `Tools/`. Rules live in `docs/agents/`.
- Formatter and laconic are redundant; the librarian is a failed project kept only for reference (already in `docs/archive/`).
- Delete the old skill files (the `SS` copies in `Tools/` and the originals) and `web_search.json` (author, 2026-11-15).

## Design
On 2026-11-15 the author copied the old archives into `Tools/SS/` (the originals are still at the top of `Tools/`) and added `Tools/repo-scaffold.skill` (17 KB). Triage (brief 002) verified: the SKILL.md inside each of the five current `Tools/*.skill` archives is byte-identical to `.claude/skills/<role>/SKILL.md`, and each is 10 lines with no rule text. `Tools/` is 152 KB, of which 98 KB is the five files to delete; `Tools/web_search.json` (12 KB) is referenced by nothing in the repo.

- Delete `Tools/SS/` entirely, and from the top of `Tools/` delete `wdt-doc-coauthoring.skill`, `wdt-formatter.skill`, `wdt-laconic.skill`, `wdt-model.skill`, `wdt-reference.skill` and `web_search.json` (an unrelated Open WebUI script that nothing references).
- Keep the five role `.skill` files and `repo-scaffold.skill`.
- Recommended: keep `.claude/skills/<role>/SKILL.md` as the source (Claude Code loads it from the repo) and treat `Tools/*.skill` as packages for the claude.ai account, rebuilt from it. Add a one-line rule to `docs/agents/README.md` saying so, and a small check (unzip and diff) that the two match. The alternative is to delete `Tools/` and upload from `.claude/skills/` directly.
- Remove the uploaded `wdt-*` skills from the author's account so they do not clash.
- Record the result in `docs/decisions.md`.

## Touches
`Tools/`, `.claude/skills/`, `docs/decisions.md`.

## Acceptance criteria
- `git ls-files Tools` lists exactly the five role `.skill` files and `repo-scaffold.skill`; `grep` finds no rule text in a stub.

## Checks to run
Unzip each `.skill` and diff against `.claude/skills/<role>/SKILL.md`.

## Out of scope
Changing role guides.

## Open questions
- Keep both `.claude/skills/` and `Tools/*.skill` (recommended, with the diff check), or one? Not yet answered by the author; do the recommended thing and report (not a stop condition for auto-merge).

## Implementation notes
<!-- progress:start -->
- **Done:**
- **Next:**
- **Decisions:**
- **Gotchas:**
- **Resume:**
- **Not run:**
- **State:** merged to main.
<!-- progress:end -->

Change report
- Task: 005g Tools folder and skill archives
- Files changed: `Tools/SS/*` (6 files deleted); `docs/agents/README.md` (Skills section); `docs/decisions.md` (entry); this brief
- What is different now: `Tools/` holds six files: the five role `.skill` files and `repo-scaffold.skill`. The top-level old archives and `web_search.json` were already gone from `main`.
- New or changed interfaces: none
- Acceptance criteria: `git ls-files Tools` lists exactly the five role `.skill` files and `repo-scaffold.skill`: met. No rule text in a stub: met (each SKILL.md is 10 lines).
- Deviations from the brief: top-level deletions were already done (author's move); only `Tools/SS/` remained.
- Risks / follow-ups: the author removes the old uploaded `wdt-*` skills from the account (cannot be done from the repo).
- Verification: unzipped each role `.skill` and diffed against `.claude/skills/<role>/SKILL.md`: all five identical. Grep found no references to the deleted files outside briefs, the audit and history notes.
- Overview sections likely needing an update: section 2 (`Tools/` line)
- Commit / branch: `brief/005-tools-and-skills-cleanup`
