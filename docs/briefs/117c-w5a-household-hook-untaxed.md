# 117 (W5a): The household hook, untaxed

- **Status:** ready
- **Author/date:** K. Ogata with the guru, 2026-11-22
- **Depends on:** 116c, 115c, 114c, 113c (merged)
- **Read (block 0: the first two only):** (1) `docs/model-v3/kernel-wiring-design.md` sections 2.3, 2.4, 3.2, 3.6 and the W5 row of section 4; (2) `docs/agents/code.md`. Later, by block: `model_v3/runner/arm.py` (`LegacyHook`); `model_v3/core/household.py` and `cells.py` (`run_cell`, `scaled`) with their tests; `model_v3/core/kernel.py` (`step_year`, `grow_and_consume`, `Book`); `model_v3/core/revenue.py:83,241` (sites 2 and 3); `docs/model-v3/cell-baseline.md` ("Rerun" section only); the pack `decile_composition.csv`, `cell_weights.csv` and register rows I-D1h to I-D1k, I-D9a to I-D9d.

## Goal
A `HouseholdHook` that runs the household account inside the kernel's year loop with **no WDT** (`T = 0`), so the untaxed household arm can be compared with the stored cell baseline before any tax enters. Not switched on anywhere: the arm switch is W7, and the default stays legacy.

## Decisions (author, 2026-11-22)
- Convention A. Class mix of a line from the pack's decile composition (D10b and the tiers take D10, labelled). Income of a line: the band mean I-D9 per line (D1-3 takes the D4-5 low bound); tail lines the D10 mean at multiple 1; the income scale to B.6g (factor 1.3733) is a **separate switch, off by default**.
- Saving: three values as a scenario axis (min, median, max of the 1998 to 2025 non-pension ratio), never a central; pension accrual from I-D1k (D.8 over B.6g, observed 2024 central) on income.
- Return scenarios from I-D1h to I-D1j; property from the JST housing split.
- **Negative net positions earn 0% real** (a labelled assumption; the debt-rate range stays unset): a negative property or net financial balance gets zero return in the hook.
- A line with a pension and no route value must not silently pay nothing (116c gotcha 2): the hook gives every line route units at the start, or raises a clear error.

## Blocks (one push each; `docs/agents/code.md`, Long builds)
- **Block 0:** progress block pushed.
- **Block 1: line state.** A pure function in `runner/arm.py` building the per-line class balances, income, saving share and accrual share for the 14 lines from the pack and register (arrays; no file reads inside; the debt rule applied as a return mask). Tests: class balances sum to line wealth; D1 keeps its negative shares as held; tail lines carry D10's mix; shapes fold with paths. Push.
- **Block 2: the hook.** `HouseholdHook.pre(book, t, g)` returns the per-line non-pension return `g_N` and signed flow share `x` from `household_step` run with `T_WDT = 0` (vectorised over lines; vectorise `household_step` in `household.py` if it is scalar-only, keeping its tests bit-equal); `post(book, fl)` writes the class balances back (including `book.pen`) and reconciles `sum_r f V_r = N` (invariant I1, checked every year). Same interface as `LegacyHook`. Push.
- **Block 3: the sites and the equivalence.** Site 2 (`revenue.py:83`) reads `W_after` set by the hook; site 3 (`revenue.py:241`) reads the recorded pre-tax gain rate. Equivalence tests: with `T = 0` the hook reproduces `cells.run_cell` on the ten band cells (identity 1e-9, the 111c baseline numbers within 1e-9), and with legacy `c` the household hook's legacy mode reproduces the `LegacyHook` path to 0.0. Registration, budget rows (`arm.py` about 113 of 140), change report; push; stop.
**Stop rule.** After three blocks, or a quarter of the budget left, push what exists and write Next. Print only summary lines; suites in the background, never piped.

## Touches
`model_v3/runner/arm.py`, `model_v3/core/household.py` (only to vectorise, tests unchanged), `model_v3/core/revenue.py` (sites 2 and 3 under the hook only), `tests/model_v3/test_arm.py` (additions) and a new `tests/model_v3/test_household_hook.py`, `docs/model-v3/architecture.md` (budget rows). Name any further file before editing it. Not the register, the pack, `runner.py`, the `out_*` files, the kernel's tax code, or the digest fixture.

## Acceptance criteria
- `test_legacy_digest` passes unchanged after every block (the default arm is legacy and nothing selects the hook); all suites pass (pre-existing data, cards and hooks failures reported as on main).
- Identity (I1) holds in every year of every test run; `T = 0` hook equals the stored 111c cell baseline within 1e-9; no double count (convention B check on one case).
- No line pays nothing for want of route units; the debt rule is a test (D1's negative net financial earns 0).
- `arm.py` within 140, `household.py` within 120, no upward import (R4); diff limited to Touches.

## Checks to run
`test_legacy_digest` after each block; v3 suites in the background (never piped); `python -I pipeline/check_agent_docs.py`.

## Out of scope
Any WDT payment through the hook (W5b), the `out_*` call sites, the arm switch, the ledger, the saving gradient, withdrawal, any register or pack edit.

## Open questions
Whether the hook should carry paths in the line axis as `revenue.py:64` folds them (agent reports how it threads `P`).

## Implementation notes
<!-- progress:start -->
- **Done:** block 0 (this block; nothing else read yet).
- **Next:** block 1, the line-state function in `runner/arm.py` with tests.
- **Decisions:**
- **Gotchas:**
- **Resume:** `git fetch origin && git checkout brief/117-w5a-household-hook`; last block pushed: 0; first action: read the design note sections 2.3, 2.4, 3.2, 3.6, section 4 W5 row, then `household.py`, `cells.py`, `arm.py`.
- **Not run:** everything.
- **State:** in progress, block 0 pushed
<!-- progress:end -->
