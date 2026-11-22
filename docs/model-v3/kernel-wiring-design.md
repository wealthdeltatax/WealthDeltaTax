# Kernel wiring design: `household_step` inside the payer-line book

Brief `docs/briefs/112r-kernel-wiring-design.md`. Design only: no code, test, register or pack change. Status: in progress (block 1 written; sections 2 to 5 and the summary pending).

## Summary
*pending (written last)*

## 1. The book as it is (block 1)
Line numbers are those of `origin/main` at 16c4493. No proposals in this section.

### 1.1 What a payer line carries
A **line** is one representative adult at a point of the wealth distribution (`base.py:6-11`): fourteen lines (D1 to D9, D10a, D10b, three Rich List tiers), each with wealth, weight, and, only for bands D4 and above, income and liquid assets (`base.py:56-67`, `142-147`). The kernel's **book** (`kernel.py:109-188`) holds `n` lines (lines x paths; the runner folds paths into the line axis, `revenue.py:64`, `support.py:154`).

| State | Where | Meaning |
|---|---|---|
| route `r` in A, B, C, D (+ Cv) | `Book.R[r]` (`kernel.py:140-153`) | a **tax route**, not an asset class: the line's wealth is split across routes by one **register mix** I-D13a to d, the same for every line (`base.py:131-133`, `V0 = wealth x share`, `base.py:147`) |
| `V`, `f`, `s`, `tot`, `sold` | per route | price per unit, family units, state units, total units, units sold (consumed); `f + s + sold = tot` is the invariant `check()` tests (`kernel.py:178-179`) |
| `dd`, `Wp`, `ppu` | per route | declared price per unit; declared value at the last assessment; price at last assessment |
| `E_cash`, `EC`, `uo`, `LB`, `A_D`, `vD`, `inc_left`, `inc_paid` | per line | refund envelopes, units paid in kind, deferred balance (lien), accrued Route D liability, auctioned share, income-mode envelopes |
| `paid`, `refunded`, `lost_refund` | per line | lifetime payer record; not reset at death |
| `state_cash` | per line | external income paid to the state (income mode only) |
| not carried | | asset class (housing, equity, pension, cash), debt, income, saving, age or stage, cohort |

Consequences for cells: a line has **no class mix**; its units are tax-routing units that all grow at one return `g`. `base.income` and `base.liquid` live on the `Base`, not the book; they feed only burden metrics (`burden.py:115`, `M2b`, `M2c`) and, in the income mode, `inc_allow`. "Cohort" is a generation clock (`G = 30`, `run_lines` deaths at `G, 2G, ...`), not an age.

### 1.2 Where each operation acts on the book (one year, `step_year`, `kernel.py:450-475`)
1. `LB x (1 + r_def)` and the income allowance reset (`kernel.py:458-459`).
2. **Growth then consumption**, `grow_and_consume` (`324-341`): every route's `V` times `1 + g`, then each route sells `f x c` units (`sold`); the line's wealth is `W (1+g)(1-c)`. No cash, no income, no saving, no debt.
3. **Declaration** (`declare`, `343-368`): `dd` per route (C at `alpha_C x V`, D with auction share `vD`).
4. Verification of C (`verify_C`, `370`).
5. **One assessment** on total declared wealth, `delta = W_new - W_prev`, `L = rate x delta` allocated across routes by the sign-matched delta shares (`assess`, `275-311`); each route settles its share (`_route_tax`, `219-272`): A and B (sale mode) by `_move` of units at the true price into the state and into `E_cash`; C in kind at `dd`; D accrues `A_D`; B lien adds to `LB`; B income mode pays from `inc_left` first. Refunds are capped by the cash envelope and the state's stake (`_refund_cash`, `208`).
6. `rebase` (`313`).
7. **Death** every `G` years (`step_death`, `478-512`): verify C, auction D, settle `LB`, reset envelopes, tax the heir on the receipt as a delta from zero. Terminal settlement of D and B (`515`).

The state's side is `s x V` per route plus `state_cash`; `state_true()` (`kernel.py:167`) is **read by no module outside the kernel** (grep of `core/` and `runner/`). Revenue reads the same payment a second time as a cash flow (below).

### 1.3 The sites of `(1+g)(1-c)`
| # | File and line | Form | What it feeds | Called from |
|---|---|---|---|---|
| 1 | `kernel.py:324-341` `grow_and_consume` | `V(1+g)`, then `f(1-c)` per route | the book itself: tax, refund, death flows, `paid`, `refunded` | `step_year` (`458-461`), from `revenue.run_lines:84`, `burden.line_flows:106`, `support.wdt_run:154` |
| 2 | `revenue.py:83` | `W1 = W0 (1+g)(1-c)` | `pay1` and `rate1` for `wbase` and `wtau` (`94-95`, `113-114`) | inside `revenue.run_lines`, parallel to the kernel's own step: a **re-derivation**, not a read of the book |
| 3 | `revenue.py:241` `identity` | `gacc = max((1+g)(1-c) - 1, 0)` | the epsilon check I3: `assessed` against `eps x gacc x wbase` | `runner.py` (via `revenue`/`out_revenue`) |
| 4 | `burden.py:175` `free_path` | `f = (1+g)(1-c)`, cumulative product | wealth with no tax: `m3_today` (`190`), `m12` (`201`) | `burden.m3_today`, `burden.m12` |
| 5 | `support.py:131-132` `system_run` | `grown (1-c) - tax` | the comparator systems of M13 and their solved rates (`solve_rate`, `139-148`) | `support.py:163-169` |

Where `c` is read: `runner.py:202` (`theta['I-D14c'] / 100`), passed to `bd.line_flows`, `rv.run_lines`, `rv.revenue` (`211`) and the support functions. Where `g` is read as the **fund's return**: `revenue.py:208`, `fund(wdt + lev, E, g, ...)` with `safe_share` mixing a safe return (`fund`, `121-130`). The fund is a recursion `Sp (1+r) + net` (`revenue.py:140` onward) with no link to the book's `s x V`.

### 1.4 What depends on each site (outputs, tests)
| Site | Outputs that move if it changes | Tests that reference it (count of matching lines) |
|---|---|---|
| 1 | every revenue, burden and support output; the fund; `delta`, `paid`, `refunded` | `test_kernel` (4), `test_revenue` (3), `test_burden` (1), `test_support` (8), `test_out_burden` (1) |
| 2 | payer base outputs `wbase`, `wtau` and hence eps | `test_revenue` |
| 3 | the I3 identity gap and the manifest's epsilon outputs | `test_revenue` |
| 4 | M3 (today's wealth tax comparison) and M12 | `test_burden` |
| 5 | M13 comparator rates and certainty-equivalent costs | `test_support` (8) |

Digests: `runner.digest` (`runner.py:346-353`) hashes a `Samples` mapping (sorted keys and array bytes). The tests that use it (`test_runner.py:51`) check only that equal runs give equal digests and different runs different ones; **no stored digest of a fixed run was found in `tests/model_v3/` or `docs/`**. The tracked `model_v3/OUTPUTS/outputs.json` records `inputs_sha256`, `levers_sha256` and `pack_sha256` (the run record). A test that proves "the legacy arm does not move" therefore needs a reference captured from `origin/main` **before** any wiring change (section 3.5, build order item 0).

### 1.5 Already built beside the book (not wired)
`core/household.py` (`household_step`, layer 1, 77 lines) advances one cell's positions by class under convention A, B or `legacy`, with the identity `dNW = S + CG + TR + O - T_WDT` checked to 1e-9, a pro rata payment on the non-pension classes, and `TR` fixed at 0; its `legacy` mode is `(1-c) p (1+r)` per class (`household.py:40-46`). `core/cells.py` (59 lines) runs ten untaxed cells (five bands by stage) on it. Neither is imported by the kernel, runner or revenue code. The note `cell-baseline.md`, section "Rerun", gives the untaxed baseline: legacy wealth over GDP 0.95, 0.78, 0.61 at years 10, 50, 100; convention A at the mid-point return 1.03, 1.16, 1.29 (pension accrual 4.83% of income, I-D1k).


## 2. Mapping a payer line to a cell (block 2)
*pending*

## 3. The replacement (block 3)
*pending*

## 4. Build order and rulings (block 4)
*pending*

## 5. Answers to the five design questions
*pending*
