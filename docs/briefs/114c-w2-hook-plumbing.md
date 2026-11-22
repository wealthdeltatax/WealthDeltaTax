# 114 (W2): Hook plumbing with the legacy hook only

- **Status:** ready
- **Author/date:** K. Ogata with the guru, 2026-11-22
- **Depends on:** 113c (merged: `tests/model_v3/fixtures/legacy_digest.json`)
- **Read (block 0: the first two only):** (1) `docs/model-v3/kernel-wiring-design.md` sections 3.2, 3.6, 3.7 and the W2 row of section 4; (2) `docs/agents/code.md` ("Adding or filling a model module", "Layer check", "Long builds"). Later, by block: `model_v3/core/kernel.py` (`step_year`, `grow_and_consume`, `run_lines`); `model_v3/runner/revenue.py:83,241`, `burden.py:175`, `support.py:132,154`; `model_v3/runner/runner.py` (`core_run`, where `c` is read); `docs/model-v3/architecture.md` 5.1 and 6.1.

## Goal
Change **no result**. Introduce the hook that will later carry the household step, and route the legacy `c` through it at all five sites, so W5 can replace the legacy hook without touching the sites again. Every digest and output stays bit-equal.

## Decisions (author, 2026-11-22)
112r adopted: a hook object built by the runner (Q6), a new `runner/arm.py` of about 140 lines with tests 210, `kernel.py` budget raised to 660, `runner.py` stays at 360 (Q7), default arm legacy (Q9).

## Blocks (one push each; `docs/agents/code.md`, Long builds)
- **Block 0:** progress block pushed; read nothing beyond the first two Read items.
- **Block 1: the kernel.** `step_year(hook=None)` and a signed flow share in `grow_and_consume`: legacy passes `x = -c`, and `cu = f*x*c` and `f - cu` stay the same operations in the same order (bit equal). `hook=None` is the legacy kernel. Tests: `step_year(hook=None)` equals the legacy hook to 0.0 (not a tolerance) on a grid of `c` and `g`; the `f + s + sold = tot` invariant holds with a negative `sold` (a buy) in a hand case. Run `test_legacy_digest` after the change; it must pass. Push.
- **Block 2: `LegacyHook` and the sites.** New `model_v3/runner/arm.py` with `LegacyHook(c)` (methods `pre`, `post` as designed, 3.2) and its use at sites 2 to 5 in place of `c` (`revenue.py:83,241`, `burden.py:175`, `support.py:132,154`), threaded through `revenue.run_lines`, `burden.line_flows` and `support.wdt_run`; `runner.py` builds the hook where it reads `c` today and **stays at 360 lines** (find a saving of the same size elsewhere in the file; report it). Run `test_legacy_digest` and the v3 suites; push.
- **Block 3: registration and report.** LAYER row for `runner/arm.py`; budget rows in `architecture.md` 6.1 (`arm.py` about 140 / tests 210, `kernel.py` 660) and the totals; `test_groups.py` only if needed; change report; push; stop.
**Stop rule.** After three blocks, or a quarter of the budget left, push what exists and write Next. Print only summary lines; run suites in the background, never piped.

## Touches
`model_v3/core/kernel.py`, `model_v3/runner/arm.py` (new), `model_v3/runner/revenue.py`, `burden.py`, `support.py`, `runner.py`, `tests/model_v3/conftest.py` (LAYER), `tests/model_v3/test_kernel.py` or a new `test_arm.py`, `docs/model-v3/architecture.md` (budgets). Name any further file before editing it. Not the register, the pack, `household.py`, `cells.py`, or the legacy digest fixture.

## Acceptance criteria
- `test_legacy_digest` passes unchanged after every block (bit equal); every existing suite passes unchanged (pre-existing data, cards and hooks failures reported as on main).
- `hook=None` and `LegacyHook(c)` give equal books to 0.0 on the grid; the invariant holds for a negative `sold`.
- `runner.py` still 360 lines; `kernel.py` within 660; the new module within its budget; no upward import (R4).
- No output, digest or pin moves; if any does, stop and report the numbers.
- Diff limited to Touches.

## Checks to run
`test_legacy_digest` after each block (about 2 minutes); v3 suites in the background (never piped); `python -I pipeline/check_agent_docs.py`.

## Out of scope
The household hook, the arm switch, pension in the book, the ledger, any register or pack change (W3 to W7).

## Open questions
Where the 5-line saving in `runner.py` comes from (agent reports).

## Implementation notes
<!-- progress:start -->
- **Done:**
- **Next:**
- **Decisions:**
- **Gotchas:**
- **Resume:** (exact branch name and fetch line, last block pushed, first action)
- **Not run:**
- **State:** ready; not started
<!-- progress:end -->
