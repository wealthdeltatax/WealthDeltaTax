# 076: Build the .skill archives from the stubs

- **Status:** ready
- **Author/date:** K. Ogata with the guru, 2026-11-19
- **Depends on:** none
- **Read:** `AGENTS.md`, `docs/agents/code.md`, `docs/agents/README.md`, `docs/agents/agent-system-improvement-plan.md` (PR #1 on branch `docs/agent-system-improvement-plan`, section section 3, Priority 6; if not yet on main read it with `git show origin/docs/agent-system-improvement-plan:docs/agents/agent-system-improvement-plan.md`).

## Goal
Generate `Tools/wdt-<role>.skill` from `.claude/skills/<role>/SKILL.md` by script and check they match, so the manual rebuild and diff in `docs/agents/README.md` goes away.

## Decisions (author, 2026-11-19)
Adopted from the external plan (PR #1) because each replaces a rule agents must remember with a check. Keep it narrow: a small script tied to an observed failure, not a framework. No new agent role.

## Design
`pipeline/build_skills.py` (standard library, `python -I`). For each of the five `wdt-*` roles, write a zip containing `wdt-<role>/SKILL.md` taken from `.claude/skills/<role>/SKILL.md`, with fixed timestamps and sorted entries so the archive is byte-identical on rerun. `--check` rebuilds in memory and compares to the committed `.skill` (unzipped content, not bytes of the zip), exits 1 on a stale one and names it. Do not touch `Tools/repo-scaffold.skill`. First run: report whether the committed archives already match; rebuild them only if the brief finds drift and say which. Update the README paragraph on skill stubs to say "run `python pipeline/build_skills.py`; `--check` verifies" (README is the only doc edit allowed).

## Touches
`pipeline/build_skills.py`, `Tools/wdt-*.skill` (only if stale), `docs/agents/README.md` (the one paragraph), `tests/hooks/test_build_skills.py` (say which suite), this brief.

## Acceptance criteria
- Build twice: byte-identical zips.
- `--check` passes on the result and fails after a one-character change to a stub (test).
- Unzipped content equals each stub.
- Under 80 lines.

## Checks to run
`python -I pipeline/build_skills.py` twice with `sha256sum`; `python -I pipeline/build_skills.py --check`; the new test as its own command.

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
