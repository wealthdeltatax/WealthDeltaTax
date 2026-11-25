# Kernel wiring design: `household_step` inside the payer-line book

Brief `project/briefs/open/112r-kernel-wiring-design.md`. Design only: no code, test, register or pack change. Status: complete (blocks 0 to 4). Design only; the author rules on section 4.1.

## Summary
- **The book has no classes.** A payer line carries wealth split across four tax routes (A, B, C, D) by one register mix; growth is one return `g` and consumption sells `c` of the units, in five places (`kernel.py:324`, `revenue.py:83`, `revenue.py:241`, `burden.py:175`, `support.py:132`). The state's stake `s x V` is read by nothing outside the kernel and the fund is a second recursion.
- **Design.** Routes are settlement channels crossed with classes: every route's units carry the line's non-pension class mix, so a route sale is the pro rata sale the author ruled; pension is a balance beside the units, in the assessed base and never sold. The household step runs in two halves around the kernel's assessment through a **hook object** built by the runner; the kernel stays numpy-only and needs one signed-flow change. One public ledger by class replaces the stake and the fund's bare return.
- **Legacy.** `arm = legacy` is the default and must be bit equal to a digest captured **before** any change (none is stored today): W1.
- **Build order:** seven briefs W1 to W7, each with three or fewer deliverables; the author reviews a per-line account table (W5), the ledger identity (W6) and the output list (W7), never a revenue number.
- **Rulings:** ten questions (4.1); the ones that change the build are Q4 (payment above non-pension wealth), Q5 (M3, M12, M13 withheld under the household arm) and Q7 (budgets: `runner.py` is at 360 of 360).
- **Blocks the taxed run:** the return ranges for pension, net financial and physical (author to set), the comparators on the account, and the shortfall rule.

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

Digests: `runner.digest` (`runner.py:346-353`) hashes a `Samples` mapping (sorted keys and array bytes). The tests that use it (`test_runner.py:51`) check only that equal runs give equal digests and different runs different ones; **no stored digest of a fixed run was found in `tests/model/model_v3/` or `docs/`**. The tracked `model_v3/OUTPUTS/outputs.json` records `inputs_sha256`, `levers_sha256` and `pack_sha256` (the run record). A test that proves "the legacy arm does not move" therefore needs a reference captured from `origin/main` **before** any wiring change (section 3.5, build order item 0).

### 1.5 Already built beside the book (not wired)
`core/household.py` (`household_step`, layer 1, 77 lines) advances one cell's positions by class under convention A, B or `legacy`, with the identity `dNW = S + CG + TR + O - T_WDT` checked to 1e-9, a pro rata payment on the non-pension classes, and `TR` fixed at 0; its `legacy` mode is `(1-c) p (1+r)` per class (`household.py:43-47`). `core/cells.py` (59 lines) runs ten untaxed cells (five bands by stage) on it. Neither is imported by the kernel, runner or revenue code. The note `cell-baseline.md`, section "Rerun", gives the untaxed baseline: legacy wealth over GDP 0.95, 0.78, 0.61 at years 10, 50, 100; convention A at the mid-point return 1.03, 1.16, 1.29 (pension accrual 4.83% of income, I-D1k).


## 2. Mapping a payer line to a cell (block 2)
**The problem.** A cell (096r, 104r 2.4) is a band by stage with a band-mean balance sheet. A line (section 1.1) is a point in the wealth distribution inside a band: D4 and D5 are two lines of the D4-5 band, D10 is five lines (D10a, D10b, three Rich List tiers), and the lines are per adult (`base.py:136`) where the cells are per household (`cells.py:7-9`). Three things must be decided for a line: its **class mix**, its **income and saving**, and its **pension**. Evidence status is stated for each; nothing is chosen for its effect on revenue.

### 2.0 The unit conversion and the band key
Lines map to a band by `base.BANDS` (`base.py:45`): D4, D5 to D4-5; D6, D7; D8, D9; D10a, D10b and the three tiers to D10; **D1 to D3 have no band key** (`''`; `income` and `liquid` are nan and the lines sit below `W_min`, `base.py:144-145`). `cells.py` runs D1-3 as a cell (income at the low bound of I-D9a). A line's per-adult income is `I-D9x / per_hh / 1e6` (`base.py:139`); a cell's per-household income is `I-D9x`. The conversion is the register's adults per household (I-D4h, 1.93; reproduced from Tables 2.9 and 2.11 in 101r). One conversion, applied once, in the base.

### 2.1 Stage within band
| Option | What it does | Consequence |
|---|---|---|
| S1. Split every line in two (working, retired) with the band's person shares (`cell_weights.csv`) | 14 lines become 28; each runs with its own income | doubles `n` in `Book` (runtime, tests, outputs by line); the retired flows (income 0.4386 of non-retired from ETB, 111c) are the only difference unless withdrawal exists; **the stage split of wealth and composition is not held** (a proxy of age of reference person), so both halves carry the same balance sheet |
| **S2. Carry stage as a label and a weight on the line, do not split yet** | 14 lines, band-mean income, stage share recorded for a later split | no new behaviour until withdrawal, a retirement transition or a stage gradient has a parameter; the I-D9 rows are all-household band means, so the band income already mixes stages; keeps the book size and every legacy output |
| S3. Fold stage into income only: line income = band mean x (working share + 0.4386 x retired share) | one blended income per line | double counts the stage mix already inside the all-household mean; no |
*Recommendation: S2.* Evidence: weights are a person-based proxy (+-0.5 pp of a rounded percent, `cell_weights.csv`); retired and non-retired income differ by a held ratio (ETB FYE 2024), but nothing else about stage is held. The split becomes worth its cost when a transition or a withdrawal scenario is written (a later brief, listed in section 4).

### 2.2 Class mix of a line
Today a line has none (section 1.1). Classes (property, net financial, physical, pension) need a share per line.
| Option | What a line gets | Evidence | Consequence |
|---|---|---|---|
| C1. The pack's **band** shares for every line in the band | five mixes (`band_composition.csv`) | observed by band, derived from WAS R8 Table 2.2 | the two deciles of a band share one mix; within-band gap up to 7.07 pp (D4 against D5: property 34.1 and 39.5, physical 24.1 and 17.0; `decile_composition.csv`) |
| **C2. Decile shares** for lines D1 to D10 (D10a, D10b and the tiers take D10) | ten mixes | observed by decile in the same table (101r script rows, this note's `decile_composition.py`) | a **new pack table** (`decile_composition.csv`) derived from held data, no new data; resolves the within-band gap; the tail (D10b, tiers) is still the D10 mix, which is an assumption (the Rich List holds business wealth the survey misses, S5) |
| C3. Tail lines on a labelled scenario mix | D10a on D10; D10b and tiers scenario | none held | the tail's class mix drives its return; the missing 5% (I-D4e) has no composition either |
*Recommendation: C2 for D1 to D10a, with the D10 mix for D10b and the tiers labelled as an assumption (C3 deferred).* Net wealth shares (property net of mortgage, net financial net of other debt) are the held basis, so **debt is netted and the debt class is 0** in the first wiring, as in `cells.py`. Pension shares are on the ONS SCAPE-based basis only (no Resolution Foundation basis enters).

### 2.3 Income of a line within its band
| Option | Line income | Evidence | Consequence |
|---|---|---|---|
| I1. **Band mean** (today's `base.income`) | every line in the band takes I-D9x | register, judgement, all-households mean | simple; the top-decile mean I-D9d is the register's weakest and misses the top tail |
| I2. Proportional to the line's wealth | income grows with wealth within a band | none; 104r 2.4 forbids allocating a flow in proportion to wealth | gives the tail an income of tens of millions; rejected |
| I3. Band mean, tail lines on a labelled scenario (the same pound income, or a scaled multiple) | D10b and tiers differ | none | the saving of a tail line is small beside its wealth either way; its growth is the holding gain |
*Recommendation: I1 for lines with a band source; the tail lines take the D10 mean in pounds, labelled as the same income and no more (I3 with multiple 1).* A scale factor on all incomes so that households times income equals B.6g (1.3733 in 111c) is a **separate scenario switch**, not default, because it changes every cell's level at once.
Growth of income: real GDP per head (`runner.context`; 1.57% a year arithmetic), as `base.income` already grows in the burden metrics.

### 2.4 Saving share
The aggregate non-pension saving ratio is held (101r: 4.90% in 2024 on the ONS gross basis; 1998 to 2025 median 1.01%, minimum -2.61%, maximum 13.54%). **No UK saving by wealth band is held** (095r section 4; I-W3a is Norway, I-W3b a top 1% gross rate that includes unrealised gains). The author's decision rules out a universal scalar as a finding.
| Option | What it is | Consequence |
|---|---|---|
| **V1. One saving ratio of income per run, taken from a labelled range (min, median, max of the aggregate series), same for every line** | `C = (1 - s) x income` | what 111c ran; the ratio is a scenario axis (three values), the aggregate is a **check** on the weighted sum, not a calibration |
| V2. A gradient with wealth or income (Bozio direction: higher lifetime income, higher saving) | `s` rises across bands | direction only (a median gap of about 4 points of income for the most educated; active saving only; not by wealth); no size; later scenario brief |
| V3. Saving as residual of a consumption rule | `S = income - C(wealth)` | no UK consumption by wealth band; this is the legacy rule in disguise |
*Recommendation: V1 in the first wiring; V2 listed as a later scenario brief.* The consequence to state in every output: the wired arm's behaviour is set by two scenario values (the saving ratio and the pension and financial return regimes), not by data.

### 2.5 The pension class for a line: units or a class balance
| Option | What it does | Consequence |
|---|---|---|
| **P1. A class balance `PA` per line, outside the route units** | the line keeps `PA` as a number; it grows at the pension scenario return (I-D1h), takes accrual `pen_in` (D.8 over B.6g applied to income, I-D1k, accepted for now); it is **in the assessed wealth** but is never a unit that can be sold | matches the author's ruling (pension in the base, never sold, payment pro rata on non-pension); needs the assessment to read `PA` as a part of `W_new` and `W_prev` and the settlement to take the whole payment from route units |
| P2. Pension as units in a route (say a fifth route P) | pension is a route with its own `f`, `V`, `s` | the route machinery would sell pension units to pay (`_move`), contradicting the ruling; would need a "no sale" flag on a route and a rule for the unsettled share |
| P3. Pension as a deferred liability to the state (lien) | the tax on pension change accrues in `LB`, paid at death | a different policy from the ruling (the author kept the lien for Route D only); a scenario at most |
*Recommendation: P1.* Basis: **ONS SCAPE-based throughout**; no row of the wiring mixes the Resolution Foundation basis (the 7.5 of I-D4a high is not used). The unresolved consequence is a **shortfall rule**: when the payment exceeds the line's non-pension wealth the household step raises (`household.py:69-70`); the book must say what happens (ruling Q4 in section 4: the existing lien in B-lien mode defers it; the payment is capped at non-pension wealth; or the run is flagged). For D4-5 non-pension wealth is 63.7% of net wealth, so the shortfall is a question of the tax rate, not of the data.

### 2.6 What the mapping leaves unset
| Quantity | Status | Stand-in for a taxed run |
|---|---|---|
| debt `D` and `I_D` | unset (no gross debt by band) | netted inside classes; debt 0 |
| saving by band | unset | one ratio per run, three-point scenario range |
| pension withdrawal and accrual by cell | unset (D.8 aggregate on income, I-D1k, is the accepted stand-in) | I-D1k range 3.01, 4.83, 9.74; withdrawal 0 |
| transfers `TR` | unset | 0; the heir rule stays the kernel's legacy death step (section 3.6) |
| class mix of the tail | unset | the D10 mix, labelled |
| returns on pension, net financial, physical | scenario ranges I-D1h to j | 3.44 / 5.20 / 6.96; physical 0 |

## 3. The replacement (block 3)

### 3.1 The principle: classes are the household's state, routes are how the tax settles
A route is a **tax-settlement channel** (A sale, B payment from the asset, C self-declared in kind, D deferred auction; shares I-D13a to d, one mix for every line). A class is an **asset type** (property, net financial, physical, pension). The two are crossed, not identified: **every route's units are a slice of the line's non-pension wealth and carry its class mix**, so a sale of route units is a pro rata sale across the non-pension classes (the author's settlement ruling) and the route shares only decide how the assessed tax is declared and settled. Pension is a **separate balance outside the units** (section 2.5, P1). Two invariants make this testable:
- **I1 (family value).** For every line and year, `sum_r f_r V_r = N`, the line's non-pension class total, and `N + PA - D = NW`.
- **I2 (class split).** The family's class positions after any sale are the pre-sale positions times `(1 - x / N)`, with `x` the true value moved: the pro rata rule of `household_step` (`household.py:60-67`).

### 3.2 Where `household_step` is called, and the one change to the kernel
**Per line and year, in this order** (the kernel's order, with the account inserted; `step_year`, `kernel.py:450-475`):
1. **Pre-tax household step** (`household_step`, `T_WDT = 0`): from the opening class positions and the line's flows (`Y_L`, `Y_P`, `C`, pension accrual `pen_in`), give closing pre-tax positions, the account `S`, `CG` and the line's **non-pension return** `g_N = sum_k g_k P_k / N` and **signed flow share** `x = S_nonpension / N` (negative for consumption, positive for saving).
2. **Growth and flow in the book.** `grow_and_consume` (`kernel.py:324`) takes `g_N` (it already accepts a per-line `g`, `_arr(g, n)`) and a **signed** share: `f <- f (1 + x)`. A negative `x` sells units to the market exactly as now (`sold`); a positive `x` buys units (`sold` negative, `tot` up). Legacy passes `x = -c`, so `cu = f x c` and `f - cu` are the same operations in the same order (bit equal).
3. Declaration, verification, **assessment** (`assess`, `275`) on `W_new = sum_r f dd + PA - LB`, `W_prev` likewise; the delta is the pre-tax `dNW` (decision D17 retained). Pension enters the total, **not the route allocation**: `w[r]` weights use route deltas only, and a fallback to route value shares is needed when every route delta is non-positive while the total delta is positive (otherwise tax is lost to `_div`).
4. **Settlement by the routes** (`_route_tax`, `219`; `_move`, `191`): unchanged. The value moved `x_true = fl.value` (true price, not credited `L`: C pays at `dd`) is the line's payment.
5. **Payment half of the household step.** A new pure function `apply_payment(q, T, source_weights)` (extracted from `household.py:60-67`, which `household_step` then calls; its tests do not change) reduces the non-pension classes pro rata by `x_true`, adds the lien to debt, and closes the account `dNW = S + CG + TR + O - T_WDT`.
6. **Reconcile.** I1 is checked; the book's `V_r` for every route is rescaled so that `sum_r f V_r = N` (a no-op when the class returns enter `g_N` exactly, a check otherwise).

**Where the call lives.** The kernel is layer L1, imports numpy only (`kernel.py:11-13`) and may not import `household`. The existing strategy-hook pattern (`alpha_C(t, gen, yrs)` callables, `run_lines`, `kernel.py:524`) carries the household: `step_year(..., hook=None)` calls `hook.pre(book, t)` for `(g_N, x)` and `hook.post(book, fl)` after settlement; **the hook object is built by the runner (L4) from `household.py` (L1) and the pack** and is passed down through `revenue.run_lines`, `burden.line_flows` and `support.wdt_run` in the place of `c`. No new layer and no upward import. `hook=None` is the legacy kernel.

### 3.3 Routes against classes: what reconciles
| Book term | Meaning under the new arm | Check |
|---|---|---|
| `f_r`, `s_r` units; `V_r` | slices of the line's (family) and the state's non-pension wealth; one price `V` per route, common to all routes because all carry the same mix | I1 each year |
| `tot_r`, `sold_r` | units ever issued; units sold to (or, negative, bought from) the market: consumption and saving are both `sold` flows | `f + s + sold = tot` (existing `check()`, `kernel.py:178`) |
| `dd_r` | declared value per unit (C: `alpha_C V`; D: `alpha_D V` with auction share `vD`); pension is declared at the true value | unchanged |
| `LB`, `A_D` | liabilities to the state: appear as `debt` in the account (the lien is `D` up, 094r B3 case 3); do not reduce class positions until settled by sale | settle at death and horizon |
| `PA` | new per-line field `pen` (and `penp` at the last assessment) | in `W_new`, `W_prev`; never in `f`, `s` |

### 3.4 The lien, `_move` and the settlement shortfall
- **`_move`** (`kernel.py:191`) keeps its meaning (family to state at the true price); the class consequence is I2. Route C moves `u_pay = L / dd` units, so a declared price below the true price (`alpha_C < 1`) moves **more** true value than `L`; the account's `T_WDT` is the true value moved, and the gap to the credited tax is the existing kernel difference, reported.
- **Lien (Route B `lien` mode, Route D accrual).** `LB` and `A_D` accrue at `r_def` and the auction; they are liabilities (debt) and are settled by pro rata sale at death and at the horizon (`settle_B`, `settle_D`). The household account shows them as `D`; `I_D` on them is the kernel's `r_def` accrual, not a separate rate.
- **Shortfall.** `household_step` raises when `T > non-pension wealth` (`household.py:69-70`). The book never raises: the A and B sale routes already cap a sale at holdings (`_div`), so the rule must be stated (**correction, 116c: the sale routes did not in fact cap at holdings; `_div` only guards a zero divisor. W4 added the cap in `_route_tax` and `kernel.shortfall_lines`; `check()` still has no minimum-units entry**): **a payment above non-pension wealth is capped at it and the excess is reported as `unpaid_B`** (the field exists, `kernel.py:159`) and counted in the liquidity diagnostic. Ruling Q4.
- **Refunds.** The cap is `min(rest, E_cash, s x V)` (`kernel.py:208-216`); under the ledger (3.5) the third term reads the ledger's class value of that route's stake.

### 3.5 The public ledger, and what it replaces
Today the state's stake is `s x V` per route (`kernel.py:167`, read by no module) and `core/revenue.py:208` runs the fund as a second recursion on cash `wdt + lev` at the return path `g`. One ledger replaces both:
- **Shape.** `L[k]` per class k (property, net financial, physical, plus the safe asset), per path and year, at market value; `L_t+1 = L_t (1 + g_k) + receipts_k - payout_k`. The pension is not a ledger class.
- **Receipts by class.** A payment of true value `x` from a line enters the ledger in the line's **non-pension class mix at the time of payment** (the unit slice it moves, 3.1); cash receipts (the corporate levy `lev`) enter under the fund rule `safe_share` (I-D14f). The ledger's class returns are the same `g_k` as the household's, scenario ranges for the classes with no held return (I-D1h to j).
- **Reads.** `fund()` (`revenue.py:121`) keeps its reserve rules, but its balance `S` and return are **read from the ledger** (`rr = sum_k L_k g_k / L`), and `core/revenue.py:208` stops passing the bare path `g`. `burden.free_path` and `support.py` do not read the fund. `state_true` becomes the ledger value.
- **Tying test (new).** Per path and year: `sum_lines weight x T_WDT_line = ledger receipts` (household minus public is zero, the 104r reconciliation), and `dL = receipts + return - payout` to 1e-9. The legacy two-recursion agreement (stake and fund equal only with one return and no payout, 104r section 4) is no longer needed.
- **What it does not do.** No price response to a sale; the market counterparty is outside the modelled sectors (104r limits).

### 3.6 The five sites under the hook
| # | Site | Legacy hook (`c`) | Household hook |
|---|---|---|---|
| 1 | `kernel.grow_and_consume` | unchanged code path | per-line `g_N` and signed `x` from the pre-tax household step (3.2) |
| 2 | `revenue.run_lines:83` `W1` | `W0 (1+g)(1-c)` in the same operation order | read the book's post-flow family value: the `growth` `Flows` gets a field `W_after` set by the hook |
| 3 | `revenue.identity:241` `gacc` | `max((1+g)(1-c)-1, 0)` | `run` records the wealth-weighted pre-tax gain rate by year (from `fl.delta / W0`) and `identity` reads it; the I3 gap is unchanged in meaning |
| 4 | `burden.free_path:175` | `(1+g)(1-c)` cumulative | the hook's untaxed path (`T = 0` through the same step) |
| 5 | `support.system_run:131-132` | `grown (1-c) - tax` | **stays legacy in the first wiring**: the comparators (stock tax, tax on gains, consumption tax) are alternative taxes and need their own bases on the account (CG, C) |
**Consequence of 5.** M13 (`support.py`, `out_support.py:30`) compares the WDT with the comparators: with the WDT on the new arm and the comparators on legacy the comparison is **not like for like**, and `m3_today` and `m12` (site 4) differ in the same way. Proposal: **under the household arm the outputs that read sites 4 and 5 are withheld and labelled `legacy_only`** until their own brief (section 4); the manifest question is ruling Q5.

### 3.7 The legacy switch and the test that proves the digests do not move
- **Switch.** One register-level choice, `arm in {legacy, household}`, read in `runner.core_run` (`runner.py:202`): `legacy` builds the legacy hook (`c = I-D14c / 100`, behaviour as today), `household` builds the household hook. Default `legacy` until the author rules otherwise. The arm is written into the run record and the output labels (a household-arm result is never a legacy result, decision of 2026-11-19).
- **No stored digest exists** (section 1.4), so the first code brief **captures one on `origin/main` before it changes anything**: for fixed seeds, the `runner.digest` of the `Samples` for a small schedule grid and `P = 20` paths, and the SHA-256 of the output groups, committed as `tests/model/model_v3/fixtures/legacy_digest.json`.
- **Proving test.** (a) `test_legacy_digest`: with `arm = legacy`, the digest equals the fixture exactly (bit equal); (b) `test_hook_none_equals_c`: `step_year(hook=None)` and the legacy hook give the same `Book` on a grid of `c` and `g` to 0.0 (not a tolerance); (c) the existing suites pass unchanged under `legacy`. A change to any of sites 1 to 5 that moves (a) fails the brief.

### 3.8 What breaks, what does not, which tests move
**Does not break:** the route mechanics, the refund cap, the death step, the declared-value logic, `Flows` fields, `check()` (I1 is extra), `household_step` and its tests, and every legacy output. **Moves under the household arm (stated, not hidden):** every revenue, burden and support output (growth is no longer `(1+g)(1-c)`), the fund balance and the I3 identity; `delta` includes saving and pension accrual. **Cannot be compared with legacy** without the arm label. Tests by file: `test_kernel` (signed flow, `hook=None` bit equality, I1), `test_revenue` (ledger tie, `W_after`, `gacc`), `test_burden` (free path), `test_support` (comparators stay legacy), `test_out_*` (withheld outputs, arm label), `test_runner` (arm switch), `test_groups` and `conftest` LAYER rows for any new module.

## 4. Build order and rulings (block 4)
Sizes are lines of code and of tests against the budgets of `architecture.md` 6.1 (code budget, now used): `kernel.py` 620 (567, 53 free), `revenue.py` 520 (246), `burden.py` 430 (324), `support.py` 520 (234), `household.py` 120 (77), `runner/runner.py` 360 (**360, no headroom**), `build_gbr.py` 200. Brief numbers are for the guru to assign; the order is W1 to W7. Every brief runs the whole legacy suite and the digest of W1.

| Brief | Deliverables (3 or fewer) | Touches | Size | Tests | Review point (author) |
|---|---|---|---|---|---|
| **W1 Capture the legacy reference** | (1) `tests/model/model_v3/fixtures/legacy_digest.json` captured on `origin/main` (`runner.digest` of `Samples` and SHA-256 of the output groups, fixed seeds, a small schedule grid, `P = 20`); (2) `test_legacy_digest.py` | tests only | 0 code, about 60 test | the digest reproduces in a second run and on a clean checkout | none (the gate for every later brief) |
| **W2 Hook plumbing, legacy hook only** | (1) `step_year(hook=None)` and a signed flow share in `grow_and_consume`; (2) `LegacyHook(c)` in a new `runner/arm.py` and its use at sites 2 to 5 in place of `c` (`revenue.py:83,241`, `burden.py:175`, `support.py:132,154`); (3) the tests | `kernel.py`, `revenue.py`, `burden.py`, `support.py`, new `runner/arm.py`, `runner.py` (the `c` read becomes a hook build: **needs a 5-line saving elsewhere or a budget raise, Q7**) | kernel +25, revenue +15, burden +10, support +10, arm 60; tests 120 | W1 digest bit equal; `hook=None` equals the legacy hook to 0.0 | none: no output moves |
| **W3 Pack: decile composition** | (1) `decile_composition.csv` in the pack (this note's script and CSV are the derivation: ten deciles by four classes); (2) `build_gbr.py` row and manifest hash; (3) loader and `test_pack` rows | `pack/GBR/`, `build_gbr.py`, `core/pack.py` | build +25, pack +15; tests 40 | rows sum to 100, reproduce `band_composition` as the weighted band mean to 0.06 pp | the author confirms the decile mix for D1 to D3 (net financial about 0, physical 54% in D1-3) |
| **W4 Pension in the book; the payment half** | (1) `Book.pen`, `penp`; `assess` adds them to `W_new`, `W_prev` with the route-share fallback; (2) `apply_payment` extracted in `household.py`; (3) the shortfall cap and report (`unpaid_B`) | `kernel.py`, `household.py` | kernel +20 (**about 612 of 620: ask a budget row, Q7**), household +25 (102 of 120); tests 90 | `sum_r L_r = L` with pension delta positive and route deltas non-positive; shortfall capped; `household_step` tests unchanged | none |
| **W5 The household hook (untaxed, then taxed)** | (1) `HouseholdHook` (class state per line from the pack, `pre`, `post`, I1 reconcile) in `runner/arm.py`; (2) site 2 `W_after`, site 3 recorded gain rate; (3) equivalence test: the hook with `T = 0` reproduces `cells.run_cell` (identity 1e-9) and with `c` reproduces the legacy baseline | `runner/arm.py`, `revenue.py`, tests | arm +80, revenue +15; tests 130 | I1 each year; account closes to 1e-9; no double count (convention B check) | **a per-line table, one schedule, three saving scenarios: `dNW`, `S`, `CG`, payment as a share of net financial and of non-pension wealth, shortfall count. No revenue or fund headline** |
| **W6 The public ledger** | (1) ledger by class in `revenue.py` (receipts by class, returns, `safe_share`); (2) `fund()` reads its balance and return from it; `state_true` reads it; (3) the tying tests | `revenue.py`, `kernel.py` (`state_true`), `burden.py` (`free_path` unchanged) | revenue +60, kernel +5; tests 100 | household minus public is zero per path and year; `dL = receipts + return - payout` to 1e-9 | the author reads the ledger identity table (cells by year), not the fund fill |
| **W7 Arm switch, labels and withheld outputs** | (1) `arm in {legacy, household}` read in `core_run`, written to the run record and labels; (2) outputs that read sites 4 and 5 withheld and labelled `legacy_only` under the household arm; (3) manifest amendment | `runner/runner.py`, `runner/arm.py`, `out/`, `model-specs/outputs.yml` (author sign-off) | runner +0 (see Q7), out +30; tests 80 | `legacy` unchanged (W1 digest); household arm emits no `legacy_only` value as a result | the author reviews the **list of outputs** a household-arm run produces and withholds, before any number is read |
**Later scenario briefs, not in this order:** comparators on the account (sites 4 and 5: the stock tax, tax on gains and consumption tax on the same classes, then M3, M12, M13 return); stage split of lines (S1); pension withdrawal (a labelled scenario); a saving gradient (V2); a class mix for the tail; debt by band if the author supplies it; validation against the 099r moments; a comparison with legacy.

### 4.1 Rulings table for the author (recommendation first)
| # | Question | Recommendation | Alternatives | Consequence of the recommendation |
|---|---|---|---|---|
| Q1 | Stage within band | **S2**: carry the stage share on the line as a label and weight; no split yet | S1 split every line (14 to 28 lines) | no stage behaviour until a transition or withdrawal parameter exists |
| Q2 | Class mix of a line | **C2**: decile shares from Table 2.2 (D10 mix for D10b and the tiers, labelled) | C1 band shares (pack as is, no W3) | a new derived pack table; the within-band gap (up to 7.07 pp) is kept |
| Q3 | Income of the tail lines | **I3 at multiple 1**: the D10 mean in pounds, no more; an income scale to B.6g is a separate switch, off by default | scale to B.6g by default (1.3733) | tail growth is almost all holding gain; the scale switch is a scenario |
| Q4 | Payment above non-pension wealth | **cap at non-pension wealth, report the excess** (`unpaid_B`) and count it | auto-defer the excess as a lien; or flag the run invalid | a rate high enough to exceed non-pension wealth is visible, not an error |
| Q5 | M3, M12 and M13 under the household arm | **withhold and label `legacy_only`** until the comparator brief | run the comparators on legacy `c` (not like for like) ; or build them first | the household arm has fewer outputs until the later brief |
| Q6 | Where the household sits relative to the kernel | **a hook object built by the runner**; the kernel stays numpy-only | the kernel imports `household` (needs an R4 amendment) | no layer change; one extra argument down three call chains |
| Q7 | Budgets | **add `runner/arm.py` (about 140 lines, tests 210) and raise `kernel.py` to 660**; `runner.py` stays at 360 | raise `runner.py` instead | the architecture budget table gains one row and one change |
| Q8 | Saving scenario axis | **three values (min, median, max of the 1998 to 2025 aggregate non-pension ratio) carried as a scenario axis**, as in 111c | median only | outputs carry a scenario label; no value is called central |
| Q9 | Default arm | **`legacy`** until the author rules otherwise | household | no existing result changes |
| Q10 | Corporate levy into the ledger | **cash under the fund rule `safe_share`** (as today) | a separate cash class | the levy keeps its present treatment; only the WDT receipts enter by class |

## 5. Answers to the five design questions
1. **What breaks and what does not.** Under growth plus consumption the book needs one per-line return and one signed flow (a small change to `grow_and_consume`), pension as a balance beside the units, and a payment half of the household step. The route mechanics, the refund cap, the death step, declared values, `check()` and every legacy output do not change; I1 (family value equals non-pension class total) is the one new invariant. Details in 3.8.
2. **Is the payer line the right unit?** Yes, with additions (names only): a class vector `pos` for property, net financial and physical; `pen` and `penp` for pension; `income` and `s_ratio`; a `stage` label and weight; `W_after` (a `Flows` field); `LB` and `A_D` read as debt; and the conversion between per-adult lines and per-household cells (I-D4h, once, in the base). Routes stay as they are, crossed with classes (3.1), not equal to them.
3. **Tests, digests and pins.** Under `legacy` none moves; W1 captures the digest and every brief is gated on it. Under the household arm every revenue, burden and support output, the fund balance and I3 change, by design; M3, M12, M13 are withheld. Suites that change: `test_kernel`, `test_revenue`, `test_burden`, `test_support`, `test_out_burden`, `test_runner`, plus new tests for I1, the payment, the ledger and the hook (3.8, section 4).
4. **What the public ledger replaces.** In `revenue.py`: the fund's bare return path (`revenue.py:208`) and its cash-only recursion, which now read the ledger; in the kernel, `state_true` (read by nothing outside it) and the refund cap's stake term. `support.py` does not read the stake or the fund (grep of `core/`), so only site 5 matters there. **Tying test:** household payments equal ledger receipts per path and year, and `dL = receipts + return - payout` to 1e-9 (3.5).
5. **Still unset, and what stands in for it in a taxed run.**
| Unset | Blocks a taxed run? | Stand-in |
|---|---|---|
| gross debt by band | no | debt netted; `LB` and `A_D` as the only liabilities |
| saving by band | no | one ratio per run on a three-point scenario axis (Q8) |
| pension withdrawal and accrual by cell | no | I-D1k on income (3.01, 4.83, 9.74); withdrawal 0 |
| returns on pension, net financial, physical | **yes, until the author sets a range** | I-D1h and i (3.44, 5.20, 6.96, mid-point a label), I-D1j 0; every output labelled |
| transfers `TR` | no | 0 (the kernel's heir rule is the legacy death step) |
| tail class mix and tail income | no | the D10 mix and the D10 mean in pounds, labelled |
| comparators on the account (sites 4, 5) | **yes for M3, M12, M13** | withheld under the household arm (Q5) |
| stage behaviour | no | label and weight only (Q1) |
| shortfall rule | **yes** | cap and report (Q4) |

