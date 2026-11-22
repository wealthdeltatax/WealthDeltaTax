# Model v3: architecture (stage C2, brief 039g)

Status: approved by the author, 2026-11-18 (sections 8.1 and 9 as written). Written 2026-11-18 by the guru from `stage-c-decisions.md` (035g, approved), `port-inventory.md` (037c), `country-pack.md` (038c), `returns-method.md` (036r), `synthesis.md` section 4 (R1 to R11) and `hooks.md` section 3 with the 030c rulings. No model code, acceptance criteria or build briefs are written here: those are 040g. Section 9 lists the defaults I chose where C1 left a number or a choice open; the author confirms or changes them before 040g starts.

## 0. What this says
1. v3 lives in `model_v3/`. It has three layers (R4): **core** (`model_v3/core/`, eight files in dependence order), **range runner** (`model_v3/runner/`) and **output layer** (`model_v3/out/`). Data enter through one country pack (`model_v3/pack/GBR/`) and the register (`registry/inputs.json`); the one output file is `model_v3/OUTPUTS/outputs.json`.
2. Code budget: core plus runner 3,900 lines, output layer 700, interface and run script 170; **4,770 in all**, against 17,730 lines scanned in `model_v2/` (R9; the output layer is 18% of core plus runner, v2's was 5,150 lines, the largest part of its bulk). Tests are budgeted apart at 3,020 lines.
3. Port by exception: the kernel (564 lines, all of it) with five changes, the rate function `tau`, the window rule, the real-basis function and `jst_r6.json`. Everything else in v2 is rewritten from `metrics.md` or dropped (section 4).
4. Thirteen build stages (section 7). Each is one session and one lane; each has its own files. Three can start at once (V3-0, V3-1, V3-4). The model path is one chain; the output writer and the manifest amendments run beside it.
5. Settled here and left open by C1: seed 20261118, 10,000 level 1 paths, 200 level 2 draws, horizons as year windows (section 3.4), the identity tolerance (section 6.3), kernel routes kept whole, a lever file, seven manifest amendments (section 8).

## 1. Layout and data flow

```
model_v3/
  __init__.py            empty
  interface.py           the Samples type and the Results contract (section 2.9)
  run.py                 run script: python -m model_v3.run (section 6.5)
  levers.json            schedule family grid, thresholds, retirement order (section 2.9, 3.3)
  pack/
    GBR/                 country data pack of 038c (manifest.json, seven CSV files, NOTICE.md, source/jst_r6.json)
    build_gbr.py         one-off builder of the UK pack from the held spreadsheets (data tooling, not core)
  core/
    pack.py  returns.py  base.py  schedule.py  kernel.py  revenue.py  burden.py  support.py
  runner/
    runner.py  sweeps.py        (pool.py only if section 6.5 says so)
  out/
    assemble.py  writer.py
  OUTPUTS/
    outputs.json         the model's output file (tracked)
    scratch/             git-ignored; smoke and trial runs
tests/model_v3/          one test file per module, plus rules and budget tests
```

**Where each thing is read from.** The model reads `docs/model-v3/outputs.yml` (the manifest, hashed into the run), `registry/inputs.json` (the register: low, central and high, with the `(J)` flag; hashed into the run), `model_v3/levers.json` and `model_v3/pack/<ISO>/`. `jst_r6.json` is read only through the pack: `build_gbr.py` copies the file unchanged to `pack/GBR/source/` and derives `returns.csv` from it (pack file 3.1 of 038c), and the loader reads `returns.csv`. Nothing under `model_v2/` or `model_v1/` is read by v3 code or by v3 tests.

**Output.** `model_v3/OUTPUTS/outputs.json`, schema `wdt-outputs/1` as `pipeline/validate_outputs.py` (030c) checks it. The run script writes to `--out`, default `model_v3/OUTPUTS/`; the smoke test and trial runs write to a temporary directory or `OUTPUTS/scratch/` (R5, output location). The file is tracked; a run with `status: final` is committed only on the author's word (G2 of `order.md`).

**Run record.** Written by the writer into `run` (hooks.md section 9) plus, from 038c section 5 and this document: `pack_sha256`, `pack_country`, `levers_sha256`, `seed`, `paths`, `level2_draws`, `level2_paths`, `unfilled_paths`, `model_version` (git commit), `base_year`. G2 should also read `pack_sha256` and `levers_sha256` (section 8, amendment A6).

**Flow.** `pack` and the register give inputs; `returns` gives paths; `base` gives payer lines; `schedule` and `kernel` settle each line each year; `revenue`, `burden` and `support` turn line flows into per-path metric values; the runner calls them for each schedule and each level 2 draw and hands per-path arrays to the writer; the writer summarises and writes the file. Dependence is one way, from the top of that list to the bottom (section 5.1).

## 2. The modules, in dependence order

Each entry: purpose, inputs, outputs (and the manifest ids it produces), the C1 decision it implements, budget. Budgets are `wc -l` of the file, blank lines and comments included (the convention of `port-inventory.md`).

### 2.1 `core/pack.py`: country pack and register loader (355 lines)
- **Does.** Reads and validates a pack as 038c sections 2, 3 and 5 say: manifest first, folder name equals `country`, per-file sha256, header equals the schema, first violation raises with file, row and column, no fill, no interpolation, no clipping. Computes `pack_sha256`. Reads `registry/inputs.json` into low, central and high per row id, with `(J)` flags and unit. Runs the interim consistency checks X1 (register value of a pack row equals the pack-derived value within 1e-9) and X2 (the M1d lines sum to 8.11% of GDP within 0.01). Provides the accessors the other modules use and the two data-fact outputs.
- **Inputs.** `model_v3/pack/<ISO>/`, `registry/inputs.json`.
- **Outputs.** Typed dicts of pack tables and register values; `DH1a` and `DH1b` (data facts read from the pack, point forms).
- **Implements.** R3 (register with low, central, high), R11 (the only module that handles `country`, `currency` and labels), R5 (hash). C1 item 8 housekeeping (stamp-duty sub-rows never summed with their parent).
- **Imports.** numpy, standard library only.
- **Brief 109c (2026-11-21):** two datasets added to the loader, `cell_weights` (persons by band and stage; unique on band and stage) and `band_composition` (shares of band net wealth by class; unique, and the classes of a band sum to 100 within 0.5), so a pack built with them loads. Budget raised from 340 to 355 code lines and 240 to 265 test lines for this reason only (the two schema rows, one cross-check, and the tests of the fixture and of the UK pack). The pack version is 2.

### 2.2 `core/returns.py`: return generator (260 lines)
- **Does.** The level 1 generator: AR(1) with normal innovations, parameterised by the **arithmetic** mean, the marginal SD and lag-1 autocorrelation (4.742%, 8.219%, 0.30 at the sample), starting from the stationary distribution; returns real annual arithmetic returns as a `(T, paths)` array from a seed stream. The stationary block bootstrap (mean block 3, wrapping inside each contiguous segment) as the robustness check. The level 2 draw: mean, SD and lag-1 drawn from their register ranges (3.41 to 6.07; 7.47 to 8.96; 0.19 to 0.42). Sample statistics from the pack series (arithmetic and geometric mean, SD, lag-1, effective sample 63). Window rule `loop_windows` for the identity check and the 30-year spread display.
- **Inputs.** `returns` table of the pack; register rows I-D1a, I-D1b, I-D1b2.
- **Outputs.** Path arrays; parameter draws; sample statistics. No manifest id: every return-risk output depends on it.
- **Implements.** C1 items 1 and 4 (generator, arithmetic basis, 100-year sampled paths, pool all 117 years, replay is not the generator, war years a reported sensitivity not a draw); item 6 (seed streams, section 3.1).
- **Imports.** numpy; `core/pack.py` types only.

### 2.3 `core/base.py`: wealth and payer base (380 lines)
- **Does.** Turns the pack's wealth distribution, tail and household tables into the payer lines the kernel runs: line initial values by route, weights, cohort and death age structure (G = 30), income and liquid assets by band (for M2b and M2c), income deciles of non-payers (for M4a), and the threshold W_min as a multiple of median house price per adult. Calibrates the weights to the pack totals; fails if a band does not partition. Replaces v2's `build_dist`, `calibrate`, `cohort_spec` and `build_scenario` (`rates_core.py` 408 to 599, which `port-inventory.md` did not scope: they are read as the specification, not ported).
- **Inputs.** `wealth_distribution`, `wealth_tail`, `household_incidence` tables; register rows for the route mix, consumption, income ratios; `levers.json` threshold.
- **Outputs.** `Base`: arrays `V0` by route (n lines), weights, band and decile labels, W_min, income and liquid assets per line.
- **Implements.** C1 item 5 (payer-level lines, so each line carries its own cumulative paid and refunded); item 7 (D5 behaviour enters as a base-shrink factor drawn at level 2).
- **Imports.** `core/pack.py`.

### 2.4 `core/schedule.py` and `core/kernel.py`: rate schedule and refund mechanics (170 + 620 lines)
- **`schedule.py`.** The marginal-rate function `tau(W)`: logistic in W and logistic in ln W (the ladder branch is dropped). Uses the formula of VAL section 5 with `(tau_m - tau_0) / tau_0`, the form v2 uses; RATES section 4's printed form is a writing item. **Rejects** a non-progressive draw: monotone marginal rate checked on a grid before any run (R10). Builds the schedule family grid and the named schedules from `levers.json`. The rate function arrives at the kernel as a callable, as in v2.
- **`kernel.py`.** The ported `wdt_kernel.py`, vectorised over a line axis. Changes (section 4): refund is **tau x loss** (C1 item 9); the envelope **resets at death** as v2 does (item 10; the paper text changes, a writing item); each line carries **cumulative tax paid and cumulative refunds** so the cap is exact (item 5); the `fresh_entrant` heir rule is dropped; the growth input is a `(T, n)` matrix, so many paths run in one call (section 3.2). All routes (A, B, C, D, Cv) and the three Route B modes are kept (section 9, item 1).
- **Inputs.** `Base`, a growth matrix, the schedule callable, register scalars (consumption, verification hazards, deferral rate).
- **Outputs.** Per-year flows per line (`Flows`: tax, refund, rate, delta, units by route), the final `Book`, the cumulative payer state.
- **Implements.** C1 items 3 (the model computes each payer's tax from the schedule; epsilon is an output), 5, 9, 10; R10.
- **Imports.** `schedule.py` imports numpy only; `kernel.py` imports numpy only (as in v2).

### 2.5 `core/revenue.py`: revenue lines and fund (520 lines)
- **Does.** Per path and year: M1a (tax minus refunds), M1b (corporate levy), M1c (fund income net of retention), M1d and M1e (retired receipts, one line per tax, retired in the lever's order, ascending by receipts, by the trigger of `metrics.md`), M1 = M1a + M1b + M1c - M1d **with no floor and no clip**, one sign convention (positive is a receipt to the state). The fund: short and long reserve, fill rule, retention (`rates_core.run_fund` 1109 to 1193 is the specification, written again, not ported). B1a to B1d (payers, entries, exits, fall-through refunds as a split of M1a). The fill year and the horizon windows (section 3.4). P1, P3, P4, P5, P6, P7a, P7b. The revenue identity M1a ~ epsilon x g x omega - refunds as a computed check, never as an input.
- **Inputs.** Kernel flows, `Base`, pack `receipts` and `public_expenditure`, register rows, `levers.json` retirement order.
- **Outputs and ids.** `O1, O1a, O1b, O1c, O1d, OP1, OP3, OP4, OP5, OP6, OR1, OB1` (as per-path arrays by schedule, horizon, by and line).
- **Implements.** C1 items 2 and 3, R10 (through `schedule`), the staged retirement rule (P3 must be zero).
- **Imports.** `pack`, `base`, `schedule`, `kernel`.

### 2.6 `core/burden.py`: burden and savings (430 lines)
- **Does.** M2 (burden as a share of wealth, revenue-weighted, start-of-year wealth denominator), M2b and M2c (cash-flow burden against income and liquid assets, at the cutoffs of the manifest), M3 (gain-weighted lifetime rate, G = 30), M4a and M4b (non-payer savings by income decile, including the retired taxes they pay), M4c (pounds per month for a reference worker), M5 and M6 (comparators from the pack: suggested wealth taxes, income tax, CGT and IHT), M8 (reform in place at the same revenue and the same people), M11, M12 (today's lifetime rate and the share of gains that escape tax). The decile table of the pack is the denominator of DH1c.
- **Ids.** `O2, O2d, O3, O2b, O2c, O4a, O4b, O5, O6, O8, OL1, OH1b, OH1b2, OH1c, DH1c`.
- **Imports.** `pack`, `base`, `schedule`, `kernel`, `revenue`.

### 2.7 `core/support.py`: supporting metrics (520 lines)
- **Does.** M7 and the declaration curve M7c and M7d (C.1 over TW(1), refund protection lost), M13 (certainty-equivalent welfare of the four tax systems at equal revenue; risk aversion drawn at level 2), M14 (CGT lock-in, a post-processing pass over the same payer paths), M15a and M15b (the contribution envelope, from the cumulative payer state), M9 (net fiscal effect after migration), S1 (capitalisation of retired property taxes). S1 is a **switch**: off in every headline cell; one extra variant run with it on (C1 item 7b). It is not averaged into any range.
- **Ids.** `O7, OD1, OW1, OW2, OW3, OM1, OS1`.
- **Imports.** `pack`, `base`, `schedule`, `kernel`, `revenue`. It does not import `burden` (R4: no import across cores at the same layer).

### 2.8 `runner/`: range runner (runner.py 360, sweeps.py 300 lines; pool.py 70 only if section 6.5 triggers)
- **`runner.py`.** The two-level run. Level 1: for fixed parameters, `N1` paths (section 3.1), each of the three named schedules, summarised by the writer as P10, mean and P90. Level 2: `N2` parameter draws, each with `N2P` paths, giving the P10 to P90 of the level 1 mean; the D5 behaviour strength, the risk aversion and every tier 1 input of `drivers.md` are drawn here (C1 item 7a), independently, as in section 9 item 4. Seed streams. Folds paths into the kernel's line axis in chunks (section 3.2). Produces `Samples` (section 2.9).
- **`sweeps.py`.** The schedule sweep: the feasibility map over the schedule grid (`OF1`), then the named schedules chosen by the confirmed rule (S_central is the feasible-map point with the highest closure share under the burden cap; S_low and S_high are the edges of the feasible region), then everything at those three. The tornado (`OT1`): one input at a time at low and high, every other input central, for M1, M2, M4a and M3, at each named schedule. The break-even return and the share of paths with negative M1 (`O1e`, `O1f`, C1 item 2d). The synthetic cyclical stress test (`CK1`). The bootstrap robustness run and the 30-year spread display (C1 item 4a).
- **Ids.** `O1e, O1f, OF1, OT1, CK1`.
- **Implements.** C1 items 2, 4, 6, 7; R5.
- **Imports.** all core modules; no import of `out`.

### 2.9 `out/` (assemble.py 480, writer.py 220 lines) and the contract (interface.py 50 lines)
- **The contract.** `interface.Samples` is a mapping `output id -> {key: ndarray}` where `key = (schedule, horizon, by, line)` and `schedule` is `None` for once-not-per-schedule outputs, `by` a sorted tuple of `(name, value)`, `line` `None` or a metric id; each array has one entry per level 1 path (or, for level 2 results, per draw). `interface.Level2` carries the tornado rows and the level 2 P10 and P90. The writer depends on this file and the manifest only, so it can be built and tested against synthetic `Samples` before any model module exists.
- **`assemble.py`.** Reads the manifest and builds one entry per output: cells over the full product of schedules, horizons and `by` vocabularies; summary forms A (`p10_mean_p90`), B (`point_and_range`), the value-only `point`, and C (level 2); P10 and P90 by `numpy.percentile` with linear interpolation, mean arithmetic; values in the manifest's unit, never rescaled. Data-driven: no per-output code except a table from output id to the metric key.
- **`writer.py`.** The only writer of the file. Deterministic bytes (sorted keys, fixed float format). The nan and inf rule: a non-finite value is an error in a `final` run and `null` in a `provisional` one (V5), never converted silently (the 30-line spec of `json_safe`, rewritten with a test). Writes the `run` block and the hashes. The run script calls `pipeline/validate_outputs.py` after writing and exits non-zero on any error.
- **Implements.** R1 (every entry is a manifest id; an unknown id raises), R4 (third layer), R9.
- **Imports.** `interface`, the manifest, numpy, `json`, `hashlib`. Not `core` and not `runner` (R4).

### 2.10 Output ids by module (every manifest id appears once)
| Module | Ids |
|---|---|
| `core/pack.py` | DH1a, DH1b |
| `core/revenue.py` | O1, O1a, O1b, O1c, O1d, OP1, OP3, OP4, OP5, OP6, OR1, OB1 |
| `core/burden.py` | O2, O2d, O3, O2b, O2c, O4a, O4b, O5, O6, O8, OL1, OH1b, OH1b2, OH1c, DH1c |
| `core/support.py` | O7, OD1, OW1, OW2, OW3, OM1, OS1 |
| `runner/sweeps.py` | O1e, O1f, OF1, OT1, CK1 |

39 outputs and one check; a test in stage V3-11 asserts that this table covers `outputs.yml` exactly.

### 2.11 `core/household.py`: the household step (120 lines; brief 108c)
A pure function `household_step(cell, pos, flows, rets, defl, convention, ...)` that advances one cell's positions (property, net financial, physical, pension, debt) by one year under convention A (credit the holding gain; saving carries the retained yield once), B (total return, an equivalence check) or `legacy` (the kernel's `W(1+g)(1-c)`, bit-equal). It returns the new positions and the account `dNW = S + CG + TR + O - T_WDT` (identity checked to 1e-9, the deflator wedge as its own entry of `CG`, `O` an input residual, `TR` fixed at 0). Pension is illiquid: the WDT payment falls pro rata on the non-pension classes (or by `source_weights`), never on pension, and the liquidity diagnostic is returned. Layer 1 (it imports nothing from `model_v3`, so the kernel may import it later). Not called by the kernel, runner or revenue code in 108c. Design: `docs/research/104r-parameter-map-design.md` sections 3 and 5.1.

### 2.12 `core/cells.py`: the untaxed cell baseline (80 lines; brief 110c)
`cell_table(pack, reg, retired)` builds the ten cells (five pack bands by retired or not: households, income, positions per household by class, in thousands of pounds) and `run_cell(...)` advances one cell with `household_step` under convention A, B or legacy. Standalone and untaxed: no tax, no pension withdrawal, no transition between cells, no death. Layer 2 (it imports `household` and `pack`; nothing in the kernel or runner imports it). The run script and findings are `docs/model-v3/cell-baseline/` and `cell-baseline.md`.

## 3. Numbers C1 left to the architecture

### 3.1 Seed and sample size
- **Seed.** One master seed, **20261118**, recorded in `run.seed`. Streams are `numpy.random.SeedSequence(20261118).spawn(5)` in this fixed order: `level1_paths`, `level2_draws`, `bootstrap_check`, `welfare_risk`, `tornado_crn`. A new stream is appended, never inserted, so earlier results do not change. No module calls a global random function.
- **Sample size (starting values).** `N1 = 10,000` level 1 paths per schedule (036r: first size within 0.1 point across five seeds on toy statistics). Level 2: `N2 = 200` parameter draws (Latin hypercube) each with `N2P = 1,000` paths on common random numbers; the tornado uses `N2P` paths per input value, on the same common numbers. These are starting values. The convergence test of 040g may raise them, never lower them.

### 3.2 Paths in one call
The kernel's lines are independent: state is per line and routes sum within a line. The runner therefore folds paths into the line axis (`n = lines x paths`, growth matrix `(T, n)`), in chunks of at most 1,000 paths, instead of calling the kernel path by path. A kernel test (section 6.2) shows a line gives the same result alone and inside a batch, to 1e-12. If that test fails, stage V3-10 falls back to a per-path loop and section 6.5's pool rule applies.

### 3.3 Levers
`model_v3/levers.json` holds what is a lever and not an input (`metrics.md`, range design; `drivers.md` item 3). Proposed contents (author to confirm, section 9 item 5): axes of the schedule family, centred on v2's `logistic_ln_ref` point (`tau_0` 4%, `tau_m` 90%, `k_ln` 1, threshold at half the median house price per adult): `tau_m` in {0.5, 0.7, 0.9}, `k_ln` in {0.5, 1, 2}, `tau_0` fixed at 0.04, threshold ratio in {0.25, 0.5, 1.0}; the retirement order (ascending by receipts); the feasibility rule's cap on M2, floor on M4a and the closure share, set by the author in the manifest's amendment A5. The named schedules S_low, S_central and S_high are **computed** from the grid by the confirmed rule (section 2.8), not typed.

### 3.4 Horizons
- **Base year** 2025-26, money in 2025-26 prices (the pack's `base_year`). Introduction is at the start of year 1; **reporting starts at the first year after introduction** (C1 item 6). Every path runs **T = 100 years**.
- **Transition:** years 1 to the fill year of that path (the year the long reserve first reaches the fill rule). **Short term:** the 10 years after the fill year. **Long term:** the mean of years 51 to 100 and the year 100 value (confirmed 2026-11-16). The long window is read as a steady-state property.
- **A path that does not fill by year 90** is `unfilled`: P1 records T = 100 for it, it is left out of the short-window statistics, and the number of such paths is written to `run.unfilled_paths` and shown beside the cell. (Section 9 item 3 flags this.)

## 4. Port by exception

Source: `port-inventory.md` (27 rows; the table is the evidence). "Element" is the output id that needs the mechanism; the manifest ties each output to its whitepaper elements (R1).

| v2 item (lines) | Verdict | v3 home | Change | Needed by |
|---|---|---|---|---|
| `wdt_kernel.Flows` (80-114) | port | `kernel.py` | none | O1a, OB1, O2b |
| `wdt_kernel.Book` (121-194) | port with change | `kernel.py` | add cumulative paid and refunded per line; keep envelopes and `lost_refund` | O1a, OB1, OW3 |
| `wdt_kernel._route_tax` (222-269) | port with change | `kernel.py` | refund caps follow the new refund rule; all routes kept | O1a, O2b, O2c |
| `wdt_kernel.assess` (276-311) | port with change | `kernel.py` | refund tau x loss (item 9) | O1a, O2, O3, OD1 |
| `wdt_kernel.step_death` (479-516) | port with change | `kernel.py` | keep `delta` heir rule only; envelope reset kept (item 10) | O3, O1a |
| `wdt_kernel.run_lines` (528-564) | port | `kernel.py` | none; takes a `(T, n)` matrix | O1a, O2, O3, OP1 |
| 13 kernel functions under 30 lines (168 lines: `_arr`, `_div`, `_move`, `_refund_cash`, `rebase`, `grow_and_consume`, `declare`, `verify_C`, `verified_share`, `settle_D`, `settle_B`, `step_year`, `settle_terminal`) and the kernel header (128 lines outside functions) | port | `kernel.py` | `_refund_cash` caps follow `Book` change | as the row above |
| `wdt_core.tau` (147-177) | port with change | `schedule.py` | keep two logistic branches; drop the ladder; add R10 rejection | every output, through the schedule |
| `wdt_jst.loop_windows` (58-88) | port | `returns.py` | none | the identity check I1 (O1); the 30-year spread display |
| `wdt_jst.real_basis_inputs` (130-172) | port with change | `returns.py` | add arithmetic mean, SD and lag-1; 117-year span | O1a through the generator; register I-D1a |
| `model_v2/jst_r6.json` | port unchanged | `pack/GBR/source/` | none; `returns.csv` derived from it | the returns module |

Rewritten, from `metrics.md` and not from v2 text: `threshold_outcomes`, `threshold_beneficiaries`, `band_net_position` (revenue and burden), `json_safe` (writer), `_parse_rates`, `_parse_phase2`, `load_params` (replaced by register and pack), `decompose_tw_advantage` (now a test on the kernel, section 6.2). Dropped (323 lines of `wdt_core.py`, 64 of `wdt_par.py`): the single-taxpayer functions, `rate_spec_from_scenario`, `breakeven_rho`, `npv_tax_advantage`, the scenario machinery, `WorkerPool` (unless section 6.5 triggers). **Not in the inventory and not ported:** `rates_core.py`, `valgen_core.py`, `eval_core.py`, the table and chart scripts; v2's functions at the line ranges of `port-inventory.md` section 4 are the specification for `revenue.py`. The v2 tests that exist (`wdt_jst` and `wdt_par` self-tests) travel with their code; nothing else exists to port.

## 5. Rules

### 5.1 R4: import rules and layers
Layers, lowest first: **L0** `core/pack.py`; **L1** `core/returns.py`, `core/base.py`, `core/schedule.py`, `core/kernel.py`; **L2** `core/revenue.py`; **L3** `core/burden.py`, `core/support.py`; **L3.5** `runner/out_revenue.py`, `out_burden.py`, `out_support.py`, `out_sweeps.py` (the output groups: each reads `core` and takes the runner's `Raw` as an argument, and imports no other group); **L3.6** `runner/arm.py` (numpy only: the hooks the runner builds and passes down, 114c); **L3.7** `runner/groups.py`; **L4** `runner/`; **L5** `out/`, with `interface.py` importable from L4 and L5 only. A module imports only from strictly lower layers (and the standard library and numpy); no two modules of one layer import each other; `kernel.py` and `schedule.py` import no project module; `out/` imports no `core` and no `runner`; nothing imports `out`. The test (stage V3-1) builds the import graph with `ast` from this table and fails on any other edge, and fails on an import inside a function (no lazy imports to hide layering).

### 5.2 R8: no side effects, no orphans
No module-level statement except definitions, constants and the `if __name__` guard. No module reads a file, sets an environment variable, changes the working directory or writes at import. The test imports every module in a subprocess with `python -B -I`, compares `os.environ`, the working directory and a listing of the tree before and after, and fails on a difference. No code is kept that nothing calls: the test lists every top-level function and fails on one no module and no test references.

### 5.3 R11: no country in the code
The 038c scan (classes N, T and A over `model_v3/**/*.py`, comments excluded, `pack/build_gbr.py` and `tests/` excepted) must return **zero** hits outside `core/pack.py`'s own handling of `country` and the manifest labels. The test ships in stage V3-1; stage V3-2 adds a second, tiny pack (`ZZZ`) in the test fixtures that loads with no code change. A second country is a pack, not a v3 feature.

### 5.4 R9: size
The budgets of section 6.1 are machine-readable in the fenced block there. `tests/model_v3/test_budget.py` counts lines of every file, fails when a file is over its budget, when the output layer (`out/`) is not smaller than core plus runner, or when the sums differ from the stated totals. A build brief may raise a budget only by editing this document, with a reason.

### 5.5 R5, R6, R7
- **R5.** One seed (3.1), recorded; the same inputs give the same file, byte for byte, under `python -I`. The run script and the smoke test (section 6.5) fail loudly when a file is renamed or an import breaks. The output location is a command argument, never a path inside a module.
- **R6.** Any change of convention is written next to the code (module docstring) and in `docs/decisions.md` the day it changes. The three C1 conventions that v3 starts with (arithmetic basis; tau x loss; envelope reset) are entered by the guru when this document is approved.
- **R7.** Each stage ends with its tests passing, and a stage does not start until the stages it needs have passed (section 7). Nothing is retired before its tests are ported or rewritten (section 8).

## 6. Budgets and tests

### 6.1 Line budgets

```budgets
file                          code  tests
core/pack.py                   360    280
core/returns.py                260    220
core/base.py                   380    220
core/schedule.py               170    120
core/kernel.py                 660    450
core/revenue.py                520    350
core/burden.py                 430    250
core/support.py                520    300
core/household.py             120    150
core/pension_lien.py            80     80
core/cells.py                  80     60
runner/runner.py               360    150
runner/arm.py                  280    330
runner/sweeps.py               280    100
runner/groups.py                40     60
runner/out_revenue.py          150     80
runner/out_burden.py           150     80
runner/out_support.py          150     80
runner/out_sweeps.py           150     80
out/assemble.py                480    180
out/writer.py                  220    120
interface.py                    50      0
run.py                         120     80
rules and budget tests           0    150
tests/model_v3/accept.sh         0     30
tests/model_v3/test_converge.py 0     60
tests/model_v3/test_pack_base.py 0     58
```

| Group | Code lines | Test lines |
|---|---:|---:|
| Core (ten files; `household.py` added by 108c, `cells.py` by 110c; `kernel.py` raised to 660 by 114c; `pack.py` to 360 and its tests to 280 by 115c; `pension_lien.py` added by 132c) | 3,580 | 2,538 |
| Runner (`runner.py`, `sweeps.py`, `groups.py`, four `out_*.py` groups; 084c; `arm.py` by 114c, its tests raised to 330 by 118c, itself to 160 by 119c, 180 by 120c, 215 by 121c, 245 by 126c and 255 by 127c and 280 by 132c) | 1,550 | 960 |
| **Core plus runner** | **5,140** | **3,498** |
| Output layer (`out/`) | 700 | 300 |
| `interface.py` and `run.py` | 170 | 80 |
| Rules, budget and smoke tests | 0 | 150 |
| Acceptance script and convergence test (040g Q1) | 0 | 90 |
| **Total** | **6,010** | **4,118** |

Core plus runner 5,140 (132c: `pension_lien.py` 80 and `arm.py` 280 for the lien calls and `settle`; 127c: `arm.py` 255 for the class floor; earlier raise: 5,025, raised from 4,995 by 121c: `arm.py` 225 for the withheld table; 126c: `arm.py` 245 for the household untaxed path `free` and the comparators' account `system`) is a ceiling, not a target; `runner/pool.py` (70) is outside it and counted only if triggered. The data tooling `pack/build_gbr.py` has its own budget of 200 lines (067c) and no test beyond a hash check of its output. Output layer 700 is 14% of core plus runner; R9 asks for smaller.

**The household hook (114c, kernel-wiring-design 3.2).** `kernel.step_year(hook=None)` is the legacy kernel; a hook object (`pre(book, t, g) -> (g_N, x)`, `post(book, fl)`, plus `grown`, `gain`, `free` for the sites that read `c`) is built by the runner and passed through `revenue.run_lines`, `burden.line_flows` and `support.wdt_run`; `runner/arm.py` holds `LegacyHook(c)`, which equals the `c` rule bit for bit. Brief 117c (W5a) adds `line_state`, `returns` and `HouseholdHook` (the untaxed household year, convention A, on class balances per line; imports `core/household.py`, so L3.6 is numpy and `household`): `arm.py` is 112 of 140 lines and its tests (`test_arm.py` 60, `test_household_hook.py` 125) within 210; brief 118c (W5b) lets `post` pay the value the kernel moves to the state from the non-pension classes (pro rata to the positive balances, pension never sold) and adds `reconcile` for value moved outside `post` (deaths, heir tax, horizon): `arm.py` is 139 of 140 (brief 119c raises it to 160: the tail pension cap, 158) and the taxed tests (`test_household_tax.py` 80) take the arm's test budget to 330; `revenue.run_lines` reads the assessed base as units plus `book.pen` and records `wgain` under a hook (sites 2 and 3). `kernel.py` goes from 620 to 660 lines for the signed flow share and the hook calls (the kernel stays at L1 and imports no hook).

### 6.2 Tests each module needs before the next is built (R7)
Names are the test ids a build brief and `acceptance.md` cite.

| Module | Tests (all must pass before the next module is built) |
|---|---|
| `pack` | P1 loads the ZZZ fixture pack; P2 a changed byte fails on the sha256 and names the file, and the row and column too when the file also breaks its schema (author, 2026-11-18: a per-file hash cannot give more); P3 header order wrong fails; P4 an empty cell where not allowed fails; P5 a percent outside [0, 100] fails; P6 partition sums to 100 within 0.5; P7 the pack hash of the fixture is pinned; P8 X1 (register equals pack) and X2 (8.11 within 0.01) on the UK pack, P9 the register row count equals the count read from `inputs.md` at test time (no pinned number), low <= central <= high, `(J)` flags match `inputs.md`; P10 stamp-duty sub-rows are never summed with their parent |
| `returns` | R1 the sample statistics pin: n = 117, arithmetic 4.742, geometric 4.420, SD 8.219, lag-1 0.303 (to 0.001); R2 the generator's mean, SD and lag-1 at 100,000 paths are within 0.05, 0.05 and 0.02 of the inputs; R3 the same seed gives the same array, a different seed a different one; R4 the bootstrap (mean block 3) mean and SD within 0.1 of the sample; R5 the level 2 80% band reproduces 3.41 and 6.07 within 0.02; R6 `loop_windows` self-test (10 windows, 7 contiguous, 3 wrapping) ported; R7 no draw is clipped (a generated return below -100% is an error, not a clip) |
| `base` | B1 band shares partition and sum to the pack totals; B2 W_min equals the lever ratio times the pack's median house price per adult; B3 `V0` by route sums to line value; B4 income deciles and liquid assets are non-negative and ordered; B5 the base is the same under two runs |
| `schedule` | S1 tau at W_min equals tau_0 and rises to tau_m; S2 marginal rate is monotone on a grid; S3 a non-progressive draw raises (R10); S4 the logistic-in-ln-W formula equals VAL section 5 at five points; S5 no ladder branch exists |
| `kernel` | K1 a hand-computed one-line case for each route A, B, C, D; K2 a loss is refunded at tau x loss (hand case); K3 the cap: refund equals cumulative tax paid exactly, and one pound over is held back; K4 the envelope resets at death; K5 lien recursion; K6 a line gives the same result alone and in a batch of 1,000 (1e-12); K7 cumulative paid and refunded per line equal the sum of the flows; K8 the decomposition identity tw_adv = W_sell_delta - refund_delta - settle_delta on the 70-point grid of `port-inventory.md` section 3.4 to 1e-12, **and** one case with settle_delta not zero; K9 the `(T, n)` growth matrix equals n separate runs; K10 tax and refund on hand cases written in this stage from the kernel docstring (v2 has no kernel test) |
| `revenue` | M1 sign convention: every line positive is a receipt; M1 equals M1a + M1b + M1c - M1d to 1e-12 on random paths; M2 M1 is never clipped: a path with negative M1 passes through unchanged; M3 the share of paths with negative M1 is counted; M4 fund fill and retention on a hand case against `run_fund`'s rule; M5 retirement order ascending by receipts; M6 P3 is zero under staged retirement on 1,000 paths; M7 B1d is a split of M1a and never exceeds it; **I1 and I2, section 6.3** |
| `burden` | D1 M2 revenue-weighted hand case; D2 M3 gain-weighted hand case; D3 M4a by income decile hand case; D4 DH1c equals the pack decile table; D5 M8 equals O1's revenue at the same people; D6 the comparators read only pack and register values |
| `support` | U1 C.1 uses TW(1) as denominator; U2 M13 CRRA certainty equivalent on a hand case; U3 M15a envelope binding agrees with the kernel's `lost_refund`; U4 M9 equals M1 minus X; U5 S1 off equals S1 absent; U6 M14 reduces to zero when CGT is neutral |
| `runner` | N1 the same seed gives byte-identical `Samples`; N2 level 1 and level 2 are separate objects; N3 tornado rows are in descending absolute effect; N4 the break-even root on a toy case; N5 the named schedules follow the choice rule on a toy feasibility map; N6 CK1 sinusoid gives P3 zero up to a stated amplitude; N7 the run time of one 10,000-path schedule is measured and written to `run` |
| `out` | W1 the fixture of 030c round-trips; W2 each of V1 to V12 has a failing input; W3 P10, mean and P90 equal `numpy.percentile` on a known array; W4 non-finite values are errors in `final` and `null` in `provisional`; W5 bytes are identical for the same input; W6 an id not in the manifest raises; W7 module-to-id table of section 2.10 covers `outputs.yml` exactly |

### 6.3 The identity check against v2 (C1 item 3)
The check is two tests in stage V3-7, run at v2-like inputs: the `logistic_ln_ref` scenario (`tau_0` 0.04, `logistic_ln`, `tau_m` 0.90, `k_ln` 1, threshold ratio 0.5, `body_split` 5), UK windows with T = 100 and stride 1 over the 117 usable windows (`loop_windows`), post-fill 10-year mean WDT take as a share of GDP. The reference number is the recorded **7.34**; v2 is not run and not imported.
- **Statistic (guru correction, 2026-11-19, from the 078c recording).** v2's 7.34 is the **mean over the 117 windows** of the per-window post-fill take (net individual WDT: tax + death tax + heirs - refunds, no levy; years fill to fill+9; ratio of sums over GDP). The median over windows is 6.59. Wherever this section or `acceptance.md` says "post-fill 10-year WDT take" it means that mean. The I1 and I2 tests compare the v3 mean, and may also compare window by window against `tests/model_v3/fixtures/v2_logistic_ln_ref.json`. Earlier v3 numbers (3.5, 5.02, 6.66) were medians and are not comparable with 7.34.
- **Restatement (author, 2026-11-19, after 052c).** v3 learns from v2 and does not replicate it. With v2's inputs and v2's fill year, v3's per-window take equals v2's to 1e-5 points in all 117 windows (mean 7.3416): that is the port check. The full chain with v3's own fund differs (mean 7.51 against 7.34), only through the fund's fill year in 39 windows, because v3 charges the register's constant levy (I-D7a) and v2 charges a per-year path; that difference is **reported, not a failure**. I1 and I2 below are read as follows: **I1** = the take matches v2's in every window at v2's fill year (1e-5); **I2** = at v2's fill year, the mean with the model's refund lies in 6.34 to 7.36 (not above 7.36), the difference from I1 written into the change report; the fill-year difference is recorded as a finding for the papers. The wording below is superseded where it says "7.34 within 0.02".
- **I1, the port.** With the ratio-mirror refund written into the test as a patch on the ported `assess` (the test owns that patch; it is not in the model), v3 gives **7.34 within 0.02 points of GDP** (7.34 is rounded to two places, and v2's exact value is not recorded). This shows the kernel, schedule, base and fund agree with v2 on everything except the refund rule.
- **I2, the rule change.** With the model's own refund (tau x loss), v3 gives a post-fill WDT take **not above 7.34 + 0.02 and not below 6.34**. The measured difference is written into the change report. The 1.0 point lower bound is my judgement of how large the refund rule can matter; the author may set another (section 9 item 6). A result outside the bound is not tuned away: it stops the build and goes to the author.
- **I3, the epsilon check.** The computed M1a, the computed epsilon and omega satisfy M1a ~ epsilon x g x omega - refunds within 5% of M1a on the same windows (a check of accounting, not of the policy; the tolerance is 5% because the refund term is not closed-form).

### 6.4 Smoke and acceptance
- **Smoke test** (`tests/model_v3/test_smoke.py`, R5): `python -I -m model_v3.run --smoke --out <tmpdir>` with `N1 = 50`, `N2 = 3`, `N2P = 20`; it exits 0, writes `outputs.json` with `run.status` `provisional` and `run.paths` 50, and `pipeline/validate_outputs.py` passes it in provisional mode. Renaming any module file or breaking one import makes it fail.
- **Acceptance run** (named in `acceptance.md`, 040g): one command that runs every test, the smoke test, the convergence test and the full run, and exits 0 only if all pass. The architecture fixes only that it is one command.

### 6.5 Run script and run time
`python -m model_v3.run [--paths N] [--seed S] [--out DIR] [--smoke] [--final]`. It reads the manifest, the register, `levers.json` and the pack; runs the sweep, then every named schedule, level 2 and the tornado; writes the file; validates it; prints the run record. `--final` is passed only on the author's word and is refused unless `N1`, `N2` and `N2P` are at least their starting values and every test has passed. It sets no environment variable and spawns no process unless `pool.py` exists.

Run time is not measured yet. An estimate for the folded kernel: one numpy call over `1,000 x lines` elements per operation, about 100 operations per year, 100 years, 200 draws and three schedules is of the order of minutes (unmeasured). Stage V3-10 measures it (test N7). **If the full run exceeds 60 minutes on the reference machine, or test K6 fails, `WorkerPool` is ported into `runner/pool.py` (64 lines of v2 plus its self-test), with the BLAS thread variables passed as an argument to `open()` and not set in `os.environ` (R8).** Otherwise it stays dropped.

## 7. Build stages (input to 040g D2)

Thirteen stages. "Files" are the only files a stage may change; no file appears in two stages. Stage names are `V3-n`; they are not the site build items B1 to B18 of `order.md`.

| Stage | Task | Lane | Files (only these) | Needs | May run with |
|---|---|---|---|---|---|
| V3-0 | Manifest and levers amendments A1 to A7 (section 8) and `levers.json` | guru | `docs/model-v3/outputs.yml`, `docs/model-v3/metrics.md`, `model_v3/levers.json`, regenerated `registry/metrics.json`, the fixture | author approval of section 8 | V3-1, V3-4 |
| V3-1 | Scaffold, `interface.py`, rules, budget and import tests | c | `model_v3/__init__.py`, `model_v3/interface.py`, `tests/model_v3/conftest.py`, `test_rules.py`, `test_budget.py` | this document approved | V3-0, V3-4 |
| V3-2 | Pack and register loader | c | `core/pack.py`, `tests/model_v3/test_pack.py`, `tests/model_v3/fixtures/pack_ZZZ/` | V3-1 | V3-4 |
| V3-3 | UK pack from the held files | c | `model_v3/pack/GBR/` (all), `model_v3/pack/build_gbr.py` | V3-2 | V3-4, V3-11 |
| V3-4 | Schedule and kernel (port) | c | `core/schedule.py`, `core/kernel.py`, `tests/model_v3/test_schedule.py`, `test_kernel.py` | none | V3-1 to V3-3, V3-11 |
| V3-5 | Return generator | c | `core/returns.py`, `tests/model_v3/test_returns.py` | V3-3 | V3-6 once V3-4 is done |
| V3-6 | Wealth and payer base | c | `core/base.py`, `tests/model_v3/test_base.py` | V3-3, V3-4 | V3-5 |
| V3-7 | Revenue, fund and the identity check | c | `core/revenue.py`, `tests/model_v3/test_revenue.py` | V3-4, V3-5, V3-6 | V3-11 |
| V3-8 | Burden and savings | c | `core/burden.py`, `tests/model_v3/test_burden.py` | V3-7 | V3-9, V3-11 |
| V3-9 | Supporting metrics | c | `core/support.py`, `tests/model_v3/test_support.py` | V3-7 | V3-8, V3-11 |
| V3-10 | Range runner | c | `runner/runner.py`, `runner/sweeps.py`, `runner/pool.py` (conditional), `tests/model_v3/test_runner.py` | V3-8, V3-9 | V3-11 |
| V3-11 | Output layer | c | `out/assemble.py`, `out/writer.py`, `tests/model_v3/test_out.py` | V3-0, V3-1 | V3-2 to V3-10 |
| V3-12 | Run script, smoke test, acceptance wiring | c | `model_v3/run.py`, `tests/model_v3/test_smoke.py`, `tests/model_v3/accept.sh`, `tests/model_v3/test_converge.py` | V3-10, V3-11 | none |

**Sequential chain:** V3-1, V3-2, V3-3, V3-5 and V3-6, V3-7, then V3-8 with V3-9, then V3-10, then V3-12. V3-4 and V3-11 sit outside the chain and meet it at V3-5 and V3-12. First wave: V3-0, V3-1, V3-4. A stage that needs another does not start until the earlier stage's tests pass and its branch is merged (R7).

**After V3-12.** The first provisional run, then the author's decision on the final run (G2), then the retirement of the old models (section 8). These are not build stages.

## 8. Manifest amendments, `model_v1/` and `model_v2/`

### 8.1 Amendments to the manifest for the author (stage V3-0)
The manifest is out of scope here. These are what stage V3-0 edits once approved; the vocabularies are proposals.

| # | Amendment | Why |
|---|---|---|
| A1 | Vocabularies for the six `by` lists: `embedded_gain_band` {25pct, 50pct, 75pct of asset value}; `holding_period` {5, 10, 20} years; `w_min` {0.25, 0.5, 1.0} of median house price per adult; `alpha_grid` {0.5, 0.75, 1.0, 1.25, 1.5, 2.0, 3.0, 5.0}; `reference_worker` {p25, p50, p75, p90} of the income distribution; `schedule_grid` the nine cells `tm{50,70,90}_k{05,1,2}` | `hooks.md` rulings, 2026-11-18, item 4: `by` is a bare list in OW2, OB1, OD1, OL1, OF1, OT1 and CK1 |
| A2 | `input` vocabulary of OT1 and CK1's `amplitude` {1, 3, 5, 8, 12}: `input` is the ids of the tier 1 register families D1, D4, D5, D6, D9, D10 and I-D1b/b2, resolved from `registry/inputs.json` by family prefix; `headline` {M1, M2, M4a, M3}; `schedule` as the manifest's | same; amplitude grid runs to about 12 (`metrics.md` CK1) |
| A3 | Line-level horizons: M15a all three, M15b transition only | ruling 4, second point |
| A4 | Cells for O1's own net (line M1) and OM1's own net (line M9) | ruling 4, third point |
| A5 | Feasibility rule constants (cap on M2, floor on M4a, closure share) as manifest fields | choice rule of the named schedules needs them |
| A6 | G2 reads `run.pack_sha256` and `run.levers_sha256` as well as `inputs_sha256` | `country-pack.md` section 5 |
| A7 | The hooks.md id regex matches DH1a to c, OH1b2 and CK1 | ruling 3 (next resolver brief) |
| A9 | CK1 declares lines P1, P3, P7b | 065g |
| A10 | O2d with-death burden (M2d) | 079g |
| A11 | M7e dropped | 081g |
| A12 | Output groups (2026-11-20, `stage-A12-group-outputs-2026-11-20`): O1d and OP5 carry six taxes named as the core (`cgt`, `iht`, `stamp_duties`); OP4 is the ratio only; OR1 and its lines are single-horizon; DH1a (`series`) and DH1b (`line`) are once-not-per-schedule single cells, DH1a without wealth to GDP and DH1b without groups; OT1 is cells by input and headline per named schedule, point 0 with the low and high swings, single horizon | the four stopped group briefs 085c to 088c (091g) |

### 8.2 `model_v1/` and `model_v2/` (brief 009c stays parked)
v3 never imports, runs or reads either folder, and no v3 test does. They are not touched by any build stage.
- **`model_v2/`** can leave the tree when all of these hold: V3-3 has copied `jst_r6.json` and the WID rows `wealth_tail.csv` needs into the pack (the 52.9 MB `wid_out/wid_long.csv` is not copied; only its six rows); V3-7's tests I1 and I2 have passed (they carry v2's number as a constant, so v2 is not needed to rerun them); the first run has been accepted final (G2); and no `source/`, `pipeline/` or `registry/` file reads `model_v2/`. Then brief 009c is unparked and its own check decides the move.
- **`model_v1/`** can go when no `source/`, `pipeline/` or `site/` file reads `model_v1/OUTPUTS/` (009c's grep), which I have not run. Until then it stays; its `OUTPUTS/` is generated and not edited.
- Neither folder is deleted by a build brief.

## 9. Where I chose, for the author to confirm
1. **Routes.** The kernel is ported whole: routes A, B, C, D and Cv, and the three Route B modes. `port-inventory.md` found no kernel line to drop and left the route set to this document; trimming a route is a later brief with its own tests. The route mix and modes are register values.
2. **Seed and sample size.** 20261118; `N1` 10,000; `N2` 200 draws of 1,000 paths. Starting values; 040g's convergence test can raise them.
3. **Horizons.** T = 100; the windows of 3.4; the unfilled-path rule (P1 = 100, left out of short-window statistics, count shown). The alternative is to report short-window values for unfilled paths over years 91 to 100, which overlaps the long window.
4. **Level 2 draws.** Independent draws, Latin hypercube, a normal matched to each input's 10th and 90th percentiles, truncated at any bound the register states; the three return parameters are drawn independently, not jointly. Correlation between inputs is not modelled, a limit stated in UNCER.
5. **Levers.** The grid values in 3.3 and the new file `levers.json`.
6. **Identity bounds.** I1 within 0.02; I2 not below 6.34 (a 1.0 point allowance for the refund rule). The architecture could not measure either.
7. **Run time rule.** `WorkerPool` is ported only if the full run exceeds 60 minutes or K6 fails.
8. **The budgets** of 6.1. The kernel figure comes from the port inventory (564 lines ported, 620 budgeted); the others are my estimates from the metric definitions, not measurements. The first build brief that lands more than 15% over its budget reports it before the next stage starts.
9. **`outputs.json` tracked.** Scratch runs never write to it.

## Checks run
See the change report in `docs/archive/briefs/039g-model-v3-architecture.md`.
