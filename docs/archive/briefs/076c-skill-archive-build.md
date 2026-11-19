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
- **Done:** `pipeline/build_skills.py` (74 lines), `tests/hooks/test_build_skills.py` (6 tests), README skills paragraph updated.
- **Next:** none; wiring into CI is a later brief.
- **Decisions:** `--out DIR` added so the byte-identity check writes outside `Tools/`; archives are named after the stub folder (`wdt-code.skill`, entry `wdt-code/SKILL.md`); fixed timestamp 1980-01-01, deflate, mode 0644, creator Unix.
- **Gotchas:** the committed archives already match the stubs, so `Tools/wdt-*.skill` is not rebuilt; a rebuild would change their bytes (timestamp) with no content change.
- **Resume:** none.
- **Not run:** site build (the script is not part of it).
- **State:** merged
<!-- progress:end -->

### Change report
```
Change report
- Task: brief 076c, build the .skill archives from the stubs
- Files changed:
  - pipeline/build_skills.py: build and --check, standard library, python -I
  - tests/hooks/test_build_skills.py: determinism, content, stale check, missing archive, scaffold untouched, real archives match
  - docs/agents/README.md: the skills paragraph now says run build_skills.py; --check verifies
  - docs/briefs/076c-skill-archive-build.md: progress block and this report
- What is different now: `python pipeline/build_skills.py` builds the five archives; `--check` names a stale one and exits 1. Tools/ is unchanged.
- Acceptance criteria:
  1. Byte-identical builds: MET (two builds to separate folders, sha256 lists equal for all five).
  2. --check passes on the result and fails after a one-character stub change: MET (test); on the committed archives it passes now, so there was no drift.
  3. Unzipped content equals each stub: MET (test, and --check on the real repo).
  4. Under 80 lines: MET (74).
- Deviations from the brief: none.
- Findings: none.
- Verification: python -I pipeline/build_skills.py --check exit 0; pytest tests/hooks/test_build_skills.py 6 passed; python -I pipeline/check_agent_docs.py clean after the README edit. Two deliberate mutations: the check disabled fails 2 tests; a varying timestamp is caught by the timestamp assertion.
- Overview sections likely needing an update: pipeline/ script list.
- Commit / branch: brief/076-skill-archive-build. Brief 076c merged, ready to retire.
```
