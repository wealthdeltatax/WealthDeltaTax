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
- **Done:** `pipeline/run_suites.py` (75 lines), `tests/hooks/test_run_suites.py` (5 tests), one line in `docs/agents/code.md`.
- **Next:** none; wiring into CI is a later brief.
- **Decisions:** the suite list is the five named suites (when the folder exists) plus every other `tests/<dir>` with a `conftest.py`, as the brief says to discover; that adds glossary, layout, nav, pages and retired, so the default run has ten suites, not five. An unknown suite name exits 2; a suite that exits non-zero (including "no tests collected") counts as failed; `--root` added so the tests can use temp trees.
- **Gotchas:** `tests/cards` has no `conftest.py`, so it is in the fixed list; `tests/layout` reports 40 skipped (exit 0). Default run takes about 55 s.
- **Resume:** none.
- **Not run:** site build (the script is not part of it).
- **State:** merged
<!-- progress:end -->

### Change report
```
Change report
- Task: brief 077c, isolated test-suite orchestrator
- Files changed:
  - pipeline/run_suites.py: discover suites, run each as its own `python -m pytest tests/<dir> -q`, table, failed-test names, exit 1 on any failure
  - tests/hooks/test_run_suites.py: discovery, failing suite does not stop the rest, exact command and exit per row, exit codes
  - docs/agents/code.md: the sentence listing the suites by hand replaced by a pointer to run_suites.py
  - docs/briefs/077c-test-orchestrator.md: progress block and this report
- What is different now: `python pipeline/run_suites.py` runs every suite in its own process and reports one table. Not wired into CI.
- Acceptance criteria:
  1. Default run reports the existing suites with the same counts as by hand: MET. Current counts: data 84, gate 17, cards 8, model_v3 142, hooks 82 (87 with this brief's tests), glossary 27, layout 40 skipped, nav 59, pages 28, retired 13. By hand: model_v3 142 and hooks 76 before 076c, which matches. Brief's numbers were from earlier (model_v3 134, hooks 67); the extra are tests added by later briefs and by 075c and 076c. "Five suites" became ten by discovery (see Decisions).
  2. A deliberately failing temp suite is reported and does not stop the others: MET (test; a mutation that stops at the first failure fails it).
  3. Under 100 lines: MET (75).
- Deviations from the brief: none.
- Findings: tests/layout runs 40 tests, all skipped; the cause was not checked (outside the brief).
- Verification: python pipeline/run_suites.py exit 0, 10 of 10 passed; --list; pytest tests/hooks/test_run_suites.py 5 passed; python -I pipeline/check_agent_docs.py clean after the code.md edit.
- Overview sections likely needing an update: pipeline/ script list.
- Commit / branch: brief/077-test-orchestrator. Brief 077c merged, ready to retire.
```
