# 046: Model v3 V3-1: scaffold, interface and rules tests

- **Status:** draft (ready when the author approves 040g D2)
- **Author/date:** K. Ogata with the guru, 2026-11-18
- **Depends on:** none (architecture approved)
- **Read:** `docs/model-v3/architecture.md` sections 1, 2.9, 5, 6.1 and 6.2; `docs/model-v3/acceptance.md` sections 2, 3 (V3-1 row) and 4; `docs/model-v3/country-pack.md` (the 038c scan, classes N, T and A); `docs/agents/code.md`.

## Goal
The empty v3 tree, the Samples contract and the tests that enforce layering, import hygiene, no country in code and file budgets, so every later stage is checked from its first line.

## Decisions (author, 2026-11-18)
`architecture.md` approved (sections 8.1 and 9 as written); `acceptance.md` approved with Q1 to Q6 as proposed. v3 imports nothing from `model_v1/` or `model_v2/`. No file outside this brief's Touches is changed.

## Design
Create `model_v3/__init__.py` (empty) and `model_v3/interface.py` (the `Samples` and `Level2` types of 2.9, 50 lines). Write `tests/model_v3/conftest.py`, `test_rules.py` (R4 import graph by `ast` from the layer table of 5.1; no function-level import; R8 subprocess import test with `python -B -I` comparing environment, working directory and tree; orphan-function test; R11 country scan of the 038c classes) and `test_budget.py` (parses the `budgets` block of `architecture.md` 6.1; each file within budget; `out/` smaller than core plus runner; totals 4,770 and 3,020). Each rule test must be shown to fail on a seeded violation held in the test as a temporary tree, and to pass on the clean tree.

**Shared interfaces, fixed before any stage starts** (a build brief never edits them; a mismatch is a question to the guru): the output file shape is `schema wdt-outputs/1` as `pipeline/validate_outputs.py` checks it and `docs/restructure/site/hooks.md` section 3 with the 030c rulings; the country pack format is `docs/model-v3/country-pack.md`; the id lists are `docs/model-v3/outputs.yml` and the module-to-id table of `architecture.md` 2.10; the Samples contract is `architecture.md` 2.9; the layers and import rules are `architecture.md` 5.1.

This is build stage V3-1 of `architecture.md` section 7. One session, one lane; the stage ends in a stop: tests pass, change report written, branch merged by the auto-merge rule. The stage's files are budgeted in `architecture.md` 6.1; a stage more than 15% over its budget reports it before the next starts.

## Touches
`model_v3/__init__.py`, `model_v3/interface.py`, `tests/model_v3/conftest.py`, `tests/model_v3/test_rules.py`, `tests/model_v3/test_budget.py`, this brief's progress block.

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
- **Done:**
- **Next:**
- **Decisions:**
- **Gotchas:**
- **Resume:**
- **Not run:**
- **State:** draft; not started
<!-- progress:end -->
