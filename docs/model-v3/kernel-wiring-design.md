# Kernel wiring design: `household_step` inside the payer-line book

Brief `docs/briefs/112r-kernel-wiring-design.md`. Design only: no code, test, register or pack change. Status: in progress (blocks 1 and 2 written; sections 3 to 5 and the summary pending).

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
**The problem.** A cell (096r, 104r 2.4) is a band by stage with a band-mean balance sheet. A line (section 1.1) is a point in the wealth distribution inside a band: D4 and D5 are two lines of the D4-5 band, D10 is five lines (D10a, D10b, three Rich List tiers), and the lines are per adult (`base.py:136`) where the cells are per household (`cells.py:7-9`). Three things must be decided for a line: its **class mix**, its **income and saving**, and its **pension**. Evidence status is stated for each; nothing is chosen for its effect on revenue.

### 2.0 The unit conversion and the band key
Lines map to a band by `base.BANDS` (`base.py:42`): D4, D5 to D4-5; D6, D7; D8, D9; D10a, D10b and the three tiers to D10; **D1 to D3 have no band key** (`''`; `income` and `liquid` are nan and the lines sit below `W_min`, `base.py:144-145`). `cells.py` runs D1-3 as a cell (income at the low bound of I-D9a). A line's per-adult income is `I-D9x / per_hh / 1e6` (`base.py:139`); a cell's per-household income is `I-D9x`. The conversion is the register's adults per household (I-D4h, 1.93; reproduced from Tables 2.9 and 2.11 in 101r). One conversion, applied once, in the base.

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
*Recommendation: P1.* Basis: **ONS SCAPE-based throughout**; no row of the wiring mixes the Resolution Foundation basis (the 7.5 of I-D4a high is not used). The unresolved consequence is a **shortfall rule**: when the payment exceeds the line's non-pension wealth the household step raises (`household.py:66`); the book must say what happens (ruling Q4 in section 4: the existing lien in B-lien mode defers it; the payment is capped at non-pension wealth; or the run is flagged). For D4-5 non-pension wealth is 63.7% of net wealth, so the shortfall is a question of the tax rate, not of the data.

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
*pending*

## 4. Build order and rulings (block 4)
*pending*

## 5. Answers to the five design questions
*pending*
