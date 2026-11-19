# 077: Isolated test-suite orchestrator

- **Status:** ready
- **Author/date:** K. Ogata with the guru, 2026-11-19
- **Depends on:** none
- **Read:** `AGENTS.md`, `docs/agents/code.md`, `docs/agents/README.md`, `docs/agents/agent-system-improvement-plan.md` (PR #1 on branch `docs/agent-system-improvement-plan`, section section 3, Priority 7; if not yet on main read it with `git show origin/docs/agent-system-improvement-plan:docs/agents/agent-system-improvement-plan.md`).

## Goal
One command that runs the repo's test suites each in its own process, so nobody runs them by hand or in one pytest session (the conftests clash).

## Decisions (author, 2026-11-19)
Adopted from the external plan (PR #1) because each replaces a rule agents must remember with a check. Keep it narrow: a small script tied to an observed failure, not a framework. No new agent role.

## Design
`pipeline/run_suites.py` (standard library). Suites: `tests/data`, `tests/gate`, `tests/cards`, `tests/model_v3`, `tests/hooks`, plus any other `tests/<dir>` with its own `conftest.py` (discover, do not hard-code only these). Arguments: suite names to run (default all); `--list`. Each suite: its own `python -m pytest tests/<dir> -q` subprocess; record the exact command, exit status and last line; continue past failures; print a table and the first failing test names for a failed suite; exit 1 if any failed. Never combine collection or change expectations. Add one line to `docs/agents/code.md` pointing to it (replace the sentence listing the suites by hand).

## Touches
`pipeline/run_suites.py`, `docs/agents/code.md` (one line), `tests/hooks/test_run_suites.py` (say which suite), this brief.

## Acceptance criteria
- Default run reports all five existing suites with the same pass counts as running each by hand (data 84, gate 17, cards 8, model_v3 134, hooks 67 at the time of writing; use the current counts).
- A deliberately failing temp suite is reported and does not stop the others.
- Under 100 lines.

## Checks to run
`python pipeline/run_suites.py`; `python pipeline/run_suites.py --list`; the new test as its own command.

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
