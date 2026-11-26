# 046: Model v3 V3-1: scaffold, interface and rules tests

- **Status:** ready
- **Author/date:** K. Ogata with the guru, 2026-11-18
- **Depends on:** none (architecture approved)
- **Read:** `docs/model-v3/architecture.md` sections 1, 2.9, 5, 6.1 and 6.2; `docs/model-v3/acceptance.md` sections 2, 3 (V3-1 row) and 4; `docs/model-v3/country-pack.md` (the 038c scan, classes N, T and A); `docs/agents/code.md`.

## Goal
The empty v3 tree, the Samples contract and the tests that enforce layering, import hygiene, no country in code and file budgets, so every later stage is checked from its first line.

## Decisions (author, 2026-11-18)
`architecture.md` approved (sections 8.1 and 9 as written); `acceptance.md` approved with Q1 to Q6 as proposed. v3 imports nothing from `model_v1/` or `model_v2/`. No file outside this brief's Touches is changed.

## Design
Create `model_v3/__init__.py` (empty) and `model_v3/interface.py` (the `Samples` and `Level2` types of 2.9, 50 lines). Create the empty `__init__.py` of `core/`, `runner/`, `out/` and `pack/` (0 lines each). Write `tests/model_v3/conftest.py`, `test_rules.py` (R4 import graph by `ast` from the layer table of 5.1; no function-level import; R8 subprocess import test with `python -B -I` comparing environment, working directory and tree; orphan-function test; R11 country scan of the 038c classes) and `test_budget.py` (parses the `budgets` block of `architecture.md` 6.1; each file within budget; `out/` smaller than core plus runner; totals 4,770 and 3,020). Each rule test must be shown to fail on a seeded violation held in the test as a temporary tree, and to pass on the clean tree.

**Shared interfaces, fixed before any stage starts** (a build brief never edits them; a mismatch is a question to the guru): the output file shape is `schema wdt-outputs/1` as `pipeline/validate_outputs.py` checks it and `docs/restructure/site/hooks.md` section 3 with the 030c rulings; the country pack format is `docs/model-v3/country-pack.md`; the id lists are `docs/model-v3/outputs.yml` and the module-to-id table of `architecture.md` 2.10; the Samples contract is `architecture.md` 2.9; the layers and import rules are `architecture.md` 5.1.

This is build stage V3-1 of `architecture.md` section 7. One session, one lane; the stage ends in a stop: tests pass, change report written, branch merged by the auto-merge rule. The stage's files are budgeted in `architecture.md` 6.1; a stage more than 15% over its budget reports it before the next starts.

## Touches
`model_v3/__init__.py`, `model_v3/interface.py`, `tests/model_v3/conftest.py`, `tests/model_v3/test_rules.py`, `tests/model_v3/test_budget.py`, `model_v3/core/__init__.py`, `model_v3/runner/__init__.py`, `model_v3/out/__init__.py`, `model_v3/pack/__init__.py`, this brief's progress block.

## Acceptance criteria
- `pytest tests/model_v3 -q` passes on the scaffold.
- Each of five seeded violations (a cross-layer import, a lazy import, a side effect on import, a country name in code, a file over budget) makes its rule test fail.
- `test_budget.py` totals equal 4,770 and 3,020 and read the block, not constants.
- `git diff --stat` is limited to the Touches list.

## Checks to run
`pytest tests/model_v3 -q`; `git diff --stat` limited to Touches.

## Out of scope
Any core module; `levers.json` (V3-0).

## Open questions
If a rule cannot be tested as the architecture words it, ask rather than weaken it.

## Implementation notes
<!-- progress:start -->
- **Done:** `model_v3/` tree (`__init__.py`, empty `core/ runner/ out/ pack/` packages), `model_v3/interface.py` (35 lines: `Samples`, `Level2`, `TornadoRow`, `Results`), `tests/model_v3/conftest.py`, `test_rules.py`, `test_budget.py` (150 lines together = the 150 budget). 23 tests pass. Nine seeded violations (cross-layer import, out imports core, lazy import, env set on import, file written on import, orphan function, country name, tax name, file over budget) each fail their rule and each rule passes on the clean tree.
- **Next:** V3-2 (pack and register loader), which may also start V3-4 in parallel.
- **Decisions:** R11 scan reads the N, T and A patterns from `country-pack.md` section 6, not constants. Budget test reads the `budgets` block and the stated totals (4,770 and 3,020, equal today) and does not pin the numbers. Unknown modules (anything not in the 5.1 layer table, such as `interface`, `pack/build_gbr.py`) may import no project module; `run.py` may import any. Out-of-layer rule: `out/` imports only `interface`. `interface.Level2` is per output (tornado rows, p10, p90); `Results = (Samples, {id: Level2})`. The checkers live in `conftest.py` and reach tests through an `R` fixture (two `conftest.py` files in `tests/` clash if imported by name).
- **Gotchas:** the three rules and budget test files are exactly at their 150-line budget, so any later rule needs a budget edit in `architecture.md` 6.1 (guru). The orphan test sees a function as used if any name or attribute anywhere in `model_v3/` or the tests matches; it does not prove the call is reachable. The "tests" budget for `interface.py` and `run.py` rows is only enforced if `test_interface.py` or `test_run.py` exist.
- **Resume:** none needed.
- **Not run:** A2 (numeric literals equal to a pack value; needs the pack). The ZZZ pack load (V3-2).
- **State:** done; merged to main by the auto-merge rule
<!-- progress:end -->

### Change report
```
Change report
- Task: brief 046c, model v3 stage V3-1: scaffold, interface and rules tests
- Files changed: model_v3/__init__.py, core/__init__.py, runner/__init__.py, out/__init__.py, pack/__init__.py (empty); model_v3/interface.py (Samples contract); tests/model_v3/conftest.py (rule checkers), test_rules.py (R4, R8, R11 and seeded violations), test_budget.py (R9); this brief's progress block and report
- What is different now: v3 has an empty, checked tree: layering, lazy imports, import side effects, orphans, country names and file budgets are enforced from the first line.
- New or changed interfaces: model_v3.interface.Samples, Level2, TornadoRow, Results (architecture.md 2.9)
- Acceptance criteria: pytest tests/model_v3 -q passes, 23 passed (met); five seeded violations each fail their rule test (met, nine seeded in all; outputs checked by hand); test_budget totals equal 4,770 and 3,020 and read the block (met; test compares block sums to the table's stated totals); git diff --stat limited to Touches (met)
- Deviations from the brief: none. Rule and budget test files are exactly 150 lines.
- Risks / follow-ups: no headroom in the 150-line test budget for later rules; the orphan test is name-based; run.py layer is "may import anything" (architecture 5.1 does not place it).
- Verification: pytest tests/model_v3 -q (bare pytest and python -m pytest); pytest tests/model_v3 tests/gate together: 40 passed; seeded outputs printed.
- Overview sections likely needing an update: model v3 build status (V3-1 done)
- Commit / branch: brief/046-v3-scaffold, merged to main
```
