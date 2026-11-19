# 075: Agent docs link and path checker

- **Status:** ready
- **Author/date:** K. Ogata with the guru, 2026-11-19
- **Depends on:** none
- **Read:** `AGENTS.md`, `docs/agents/code.md`, `docs/agents/README.md`, `docs/agents/agent-system-improvement-plan.md` (PR #1 on branch `docs/agent-system-improvement-plan`, section section 3, Priority 5; if not yet on main read it with `git show origin/docs/agent-system-improvement-plan:docs/agents/agent-system-improvement-plan.md`).

## Goal
A script that fails on a broken link or named path in the agent guides, so stale pointers (a missing brief, a moved folder) are caught before merge.

## Decisions (author, 2026-11-19)
Adopted from the external plan (PR #1) because each replaces a rule agents must remember with a check. Keep it narrow: a small script tied to an observed failure, not a framework. No new agent role.

## Design
`pipeline/check_agent_docs.py`, standard library only, run under `python -I`. Scan `AGENTS.md`, `START_HERE.md`, `docs/agents/*.md` and `.claude/skills/*/SKILL.md`. (1) Markdown links `[text](path)` resolve **relative to the file that contains them** (the guides use `reference/...` relative to `docs/agents/`; never rewrite them as root-relative); skip `http`, `mailto` and pure `#anchor` links; check a `path#anchor` target file exists. (2) Backticked tokens that look like repo paths (contain `/` and a known extension or end in `/`) must exist, except an allow-list in the script for glob patterns, placeholders (`NNN`, `<role>`, `*`) and generated or untracked paths (`_build/`, `_site/`). (3) Each `.claude/skills/<role>/SKILL.md` names `AGENTS.md` and `docs/agents/<guide>.md` and that guide exists. Print one line per finding (`file:line message`) and exit 1 if any. Report the allow-list entries in the change report.

## Touches
`pipeline/check_agent_docs.py`, `tests/hooks/test_check_agent_docs.py` (or `tests/scaffold/` if that suite exists; say which), this brief.

## Acceptance criteria
- Runs clean on current main, or each finding is fixed in the docs it names (docs edits allowed only to fix a genuine broken pointer; list them).
- A test per rule: a temp tree with a broken link, a missing backticked path, and a skill pointing at a missing guide each fail; a root-relative rewrite of a `reference/` link is not flagged falsely.
- Under 150 lines.

## Checks to run
`python -I pipeline/check_agent_docs.py`; the new test as its own command.

## Out of scope
Wiring into CI (a later brief once it works locally); any change to the rules the checks enforce.

## Open questions
The implementer asks rather than guesses.

## Implementation notes
<!-- progress:start -->
- **Done:**
- **Next:**
- **Decisions:**
- **Gotchas:**
- **Resume:**
- **Not run:**
- **State:** ready; not started
<!-- progress:end -->
