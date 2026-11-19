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
- **Done:** `pipeline/check_agent_docs.py` (93 lines), `tests/hooks/test_check_agent_docs.py` (9 tests), one pointer fixed in `docs/agents/code.md`.
- **Next:** none; wiring into CI is a later brief.
- **Decisions:** a backticked path resolves from the repo root or from the file's own folder (the guides write `reference/...` relative to `docs/agents/`); rule 3 needs `AGENTS.md` and at least one guide other than README, change-report, handover, brief-template, overview-maintenance; tests live in `tests/hooks` (no `tests/scaffold` exists).
- **Gotchas:** the guides contain no markdown links at all, so rule 1 guards future ones; the real work is rule 2.
- **Resume:** none.
- **Not run:** site build (the script is not part of it).
- **State:** merged
<!-- progress:end -->

### Change report
```
Change report
- Task: brief 075c, agent docs link and path checker
- Files changed:
  - pipeline/check_agent_docs.py: the checker, three rules, stdlib only, runs under python -I
  - tests/hooks/test_check_agent_docs.py: one test per rule plus CLI exit status and a clean-repo run
  - docs/agents/code.md: line 17 `patch-kit/extract_jst_sample.py` to `reference/code/patch-kit/extract_jst_sample.py` (a genuine broken pointer)
  - docs/briefs/075c-agent-docs-link-checker.md: progress block and this report
- What is different now: a stale pointer in the agent guides fails `python -I pipeline/check_agent_docs.py` with `file:line message`. Not wired into CI.
- Allow-list entries (skipped, in the script): tokens with NNN, <...>, *, {}, ... or https; prefixes _build/, _site/, model_v1/OUTPUTS/, registry/anchors.yml, registry/crosslinks.json, registry/references.json (generated, gitignored), Tools/ (the author's own folder).
- Acceptance criteria:
  1. Clean on current main: MET after one doc fix (first run: code.md:17 genuine; research.md:6 and :20 registry/references.json is generated and gitignored, so allow-listed, not edited).
  2. A test per rule: MET (broken link, missing backticked path, skill with a missing guide, skill with no AGENTS.md or guide each fail; root-relative and file-relative forms of a reference/ path both pass). Four deliberate mutations of the script each failed the tests.
  3. Under 150 lines: MET (93).
- Deviations from the brief: none.
- Findings: none outside the brief.
- Verification: python -I pipeline/check_agent_docs.py exit 0; pytest tests/hooks/test_check_agent_docs.py 9 passed; pytest tests/hooks 76 passed.
- Overview sections likely needing an update: pipeline/ script list.
- Commit / branch: brief/075-agent-docs-link-checker. Brief 075c merged, ready to retire.
```
