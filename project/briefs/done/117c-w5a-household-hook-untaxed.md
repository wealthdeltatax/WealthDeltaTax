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
- **Done:** blocks 0 to 3. `arm.line_state`, `arm.returns`, `arm.HouseholdHook(state, gain, growth, c=None)` (`pre`, `post`, `grown`, `gain`, `free`); `revenue.run_lines` sites 2 and 3; 11 tests in `tests/model_v3/test_household_hook.py` (125 lines); `arm.py` 112 of 140. `pytest tests/model_v3 -q`: 283 passed, the legacy digest and the 084c and 092c pins unchanged.
- **Next:** none for W5a. W5b (the taxed arm: payment through `apply_payment`, I1 after payment) is the next brief.
- **Decisions:** (1) `pre` returns `x = N1 / (N0 (1 + g_N)) - 1`, not `S/N`, so growth then flow hit the household step's closing non-pension total exactly (I1 by construction; `post` checks it every year to 1e-9 relative). (2) A new book (each phase) restarts the hook's state; its route values are rescaled to N and `pen = penp = pension`, so every line holds route units. (3) `line_state` normalises each decile's printed class shares to sum to 1 (they sum to 100 +- 0.01), else the classes would not sum to the line's wealth. (4) `post` raises if value moves to the state: the taxed arm is W5b. (5) `free` raises: site 4 stays legacy (M3, M12 withheld). (6) Legacy mode (`c` given): the book runs the LegacyHook path (bit for bit), the classes follow the legacy rule including the pension, I1 checked on all classes.
- **Gotchas:** (1) `run_lines` now takes `W0 = family_true() + book.pen` (pen is zero in the legacy arm, so no change there) and reads `W1`, `pay1`, `rate1` after the `step_year` loop (pure for legacy, bit equal) so that the hook's `W_after` exists; it records `wgain` only when a hook is given. (2) `hook.gain` now takes `(g, run)`; `LegacyHook.gain(g, run=None)`. (3) `household.py` needed no edit: `household_step` is already array-valued; the hook folds paths by tiling the line arrays `n // L` times (path-major, as the book does; tested). (4) The I3 identity is tested for one taxed year only, with a test subclass that leaves the payment out; later years need W5b.
- **Resume:** done.
- **Not run:** nothing skipped.
- **State:** done
<!-- progress:end -->

### Equivalence results
| Check | Result |
|---|---|
| Hook (T = 0) against `cells.run_cell`, ten cells, 40 years, all four classes | max gap 9.9e-14 (thousand pounds per household); the brief asks 1e-9 |
| Aggregate wealth at years 1, 10, 50, 100 against the stored 111c `aggregates.csv` (A_mid_median) | max relative gap 1.1e-14; the brief asks 1e-9 |
| I1 (book units equal N, book pension equals the pension balance), every year | holds to 1e-9 relative (checked in `post`) |
| Legacy mode against `LegacyHook`, 20 years of random path returns | `np.array_equal` on every route array, `paid` and the family value |
| Convention B first-year dNW against the hook, ten cells | max gap below 1e-9 (no double count) |
| Debt rule | a negative net financial or property balance earns 0 real; D1-3 at minimum saving differ from `run_cell`, which still credits the gain (the rule is W5a's, labelled) |
| Sites 2 and 3, one taxed year | `wbase` is units plus pension; the I3 gap `identity(...)['assessed']` is below 1e-9 |

Change report
- Task: brief 117c, W5a, the household hook, untaxed
- Files changed: `model_v3/runner/arm.py`; `model_v3/core/revenue.py` (sites 2 and 3); `tests/model_v3/test_household_hook.py` (new); `docs/model-v3/architecture.md` (one note); this brief
- What is different now: the kernel can run the household arm with no tax, for all 14 lines, with a legacy mode that reproduces the legacy path.
- New or changed interfaces: `arm.line_state`, `arm.returns`, `arm.HouseholdHook`; `hook.gain(g, run)`
- Acceptance criteria: all met and measured (table above); budgets met (`arm.py` 112 <= 140, tests 60 + 125 <= 210); `git diff --stat` within Touches
- Deviations from the brief: `line_state` normalises the printed shares; `household.py` not edited (already vectorised)
- Risks / follow-ups: W5b must add payment and re-test I3 over several years; death steps under the hook are untested while untaxed
- Instruction friction: none
- Verification: full `pipeline/run_suites.py` (model_v3 283 passed; data 5, cards 1, hooks 1 failed, all three also fail on main); `check_agent_docs.py` clean
- Overview sections likely needing an update: none
- Commit / branch: `brief/117-w5a-household-hook`; merged, ready to retire
