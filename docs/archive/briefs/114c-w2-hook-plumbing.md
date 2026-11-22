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
- **Done:** blocks 0 to 3. Kernel: `grow_and_consume(share=None)`, `step_year(hook=None, t=0)`, `run_lines(hook=None)` (574 lines of 660). `runner/arm.py` `LegacyHook(c)` (33 lines). The hook threaded through `core/revenue.run_lines`, `identity`; `core/burden.line_flows`, `free_path`, `m3_today`, `m12`; `core/support.wdt_run`. `runner.core_run` builds it; `runner.py` 360. LAYER row `runner/arm` 3.6. Budgets and the layer line in `architecture.md`. `test_arm.py` 4 tests (60 lines).
- **Next:** W3 (decile composition in the pack); W5 swaps `LegacyHook` for the household hook and also moves `out_support.py:57,82,105` and `out_burden.py:77-79` (they still pass `c`).
- **Decisions:** `pre(book, t, g)` not `(book, t)` (the legacy hook needs g; `step_year` gets `t=0`); the `runner.py` saving is the `headlines` docstring cut from two lines to one; `support.system_run` stays legacy (design 3.6 site 5), so it takes no hook; `arm` at layer 3.6; the brief's `runner/revenue.py`, `burden.py`, `support.py` are the `core/` files.
- **Gotchas:** `runner.py` takes the hook with a walrus on `c` in `core_run`, to add no line.
- **Resume:** none; merged.
- **Not run:** nothing.
- **State:** done; merged

Change report
- Task: brief 114c (W2), hook plumbing with the legacy hook only
- Files changed: `model_v3/core/kernel.py` (signed flow share, `hook` and `t` in `step_year` and `run_lines`); `model_v3/runner/arm.py` (new, `LegacyHook`); `model_v3/core/revenue.py`, `burden.py`, `support.py` (`hook=None` at sites 2 to 4 and `wdt_run`); `model_v3/runner/runner.py` (builds and passes the hook; one docstring line saved); `tests/model_v3/conftest.py` (LAYER row); `tests/model_v3/test_arm.py` (new); `docs/model-v3/architecture.md` (layer line, budget rows and totals, a short paragraph); this brief
- What is different now: the legacy arm runs through a hook object at the kernel, `revenue.run_lines`, `revenue.identity` and `burden.free_path`; with `hook=None` every function is the old code. No result moved.
- New or changed interfaces: `step_year(..., hook=None, t=0)`; `run_lines(..., hook=None)` (kernel, revenue), `line_flows(..., hook=None)`, `free_path`, `m3_today`, `m12` and `identity` take `hook=None`; `wdt_run(..., hook=None)`; `grow_and_consume(..., share=None)`; `arm.LegacyHook(c)` with `pre`, `post`, `grown`, `gain`, `free`.
- Acceptance criteria: `test_legacy_digest` passes after blocks 1 and 2 and in the final suite (bit equal): met. Existing suites unchanged: model_v3 258 passed; data (5), cards (1), hooks (1) fail as on main: met. `hook=None` equals `LegacyHook(c)` to 0.0 on a grid of 16 (c, g) pairs and on a driver run; the site methods equal the old expressions bit for bit; the unit invariant holds for a negative `sold`: met. `runner.py` 360, `kernel.py` 574 of 660, `arm.py` 33 of 140, no upward import (`test_rules` passes): met. Diff inside Touches: met, with the path correction below.
- Deviations from the brief: (1) the hook method is `pre(book, t, g)`, not `(book, t)`; (2) the brief's `runner/revenue.py`, `burden.py`, `support.py` are `model_v3/core/`; (3) site 5 `support.system_run` takes no hook (design 3.6 keeps it legacy); (4) `out_support.py:57,82,105` and `out_burden.py:77-79` still pass `c` (outside Touches; W5).
- Risks / follow-ups: W5 must move the `out_*` call sites to the hook or the comparators and M3 today/M12 stay legacy under the household arm (labelled `legacy_only` by W7).
- Instruction friction: none
- Verification: `python pipeline/run_suites.py` (7 of 10 suites passed; failures as on main); `test_legacy_digest` after each block; `python -I pipeline/check_agent_docs.py` exit 0.
- Overview sections likely needing an update: none
- Commit / branch: `brief/114-hook-plumbing`; brief 114 merged, ready to retire
<!-- progress:end -->
