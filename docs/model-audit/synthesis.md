# Audit synthesis and v3 requirements (brief 001c, stage E)

Guru and author, 2026-11-16. Inputs: `v1-inventory.md`, `v1-errors.md`, `v2-inventory.md`, `v2-complication.md`, `lessons-so-far.md`. Neither model is fixed; v3 is a clean slate and a piece of v1 or v2 is ported only when a named whitepaper element needs it and a test exists.

## 1. What the audit found, in four lines
1. v1 is narrow and has drifted: two C.1 denominators, a stale canonical marker, 8 of 16 run entries that cannot start, 42 register items (all with a status) plus 3 new.
2. v2 tried to cover everything: 17,729 Python lines (v1: 18,136), a 1,839-line parameter file with 101 scenarios (27 unused), 55 figures and 56 tables, and an orphaned `eval_core` (2,718 lines) that cannot import.
3. Neither produces what the papers embed: 0 of 19 embedded VAL and RATES names match v2; v1 leaves 6 embeds with no file.
4. The failures were process failures (no metric register, no output-to-paper link, no tests that travel), not arithmetic ones. The lessons are in `lessons-so-far.md` and stand unchanged.

## 2. The author's reframe (2026-11-16)
The model cannot cover the whole economic parameter space. v3 therefore **estimates ranges** and the papers are rewritten to follow its results, not the other way round. The paper series becomes one whitepaper with supporting appendices, not a sequence read in order. This replaces the earlier question "which existing outputs do the papers need": the output list below is the model's, and the whitepaper cites it.

## 3. Decisions (author, 2026-11-16)
| Topic | Decision |
|---|---|
| Headline outputs | Three: government revenue; proportional tax burden on taxpayers; proportional tax savings on non-WDT taxpayers |
| Supporting output | The tolerant zone, with C.1 defined over TW(1) |
| Savings metric | Two named metrics, each defined once: share of current tax bill, and share of income. The whitepaper picks one as headline |
| Range method | Sampled. Each ranged input has one stated range and a source; the model samples them and reports P10, mean and P90 per output. No hand-picked scenarios |
| Ranged inputs | Wealth distribution and threshold; asset returns and loss years; behavioural response (avoidance, migration, valuation understatement); rate schedule and design |
| Rate function | Arbitrary provided it is progressive: the incentive mathematics holds for any progressive schedule, so the rate is a revenue and burden question. v3 samples over a stated family of progressive schedules and the model enforces progressivity |
| Time | Year-by-year path over N years with a steady-state summary; headline numbers reported at steady state and at a stated year |
| Allocation | One fixed order: refunds first, then a stated SWF share, then relief for non-payers from the remainder |
| Wealth data | Official survey for the bulk plus a rich-list tail; the tail's uncertainty is a stated input range |
| Build approach | Clean slate, port by exception |
| Legacy design choices | The gain ladder, the fresh-entrant heir rule and the strategy verdicts BRG, HSC, SPT and SST appear in 0 papers and are not carried over unless the whitepaper needs them |

## 4. Requirements for v3
**R1 Output manifest.** One file lists every output: ID, whitepaper element it feeds, metric, formula, unit. The whitepaper and appendices cite IDs. An output with no element does not exist (lessons 6, 6a, 7).
**R2 Metric register.** One definition per metric, in one place that code and papers cite: numerator, denominator, unit, horizon. C.1 uses TW(1) (lesson 1; v1-errors B1).
**R3 Parameter file.** Every ranged input has a low, central and high value (or a distribution), a unit and a source. No duplicated or stale values, no unused entries, no numbers typed into presentation text (lesson 3; v1-errors B7, B8; v2's 27 unused scenarios).
**R4 Layering.** Core computation, then range runner, then output writer. The core imports no presentation code and nothing imports across cores (lesson 2; v1-errors C3).
**R5 Reproducibility.** A fixed seed and stated sample size; the same inputs give the same P10, mean and P90. A run script and a smoke test that fail loudly when a file is renamed or an import breaks (lesson 4; v1 `run_all`).
**R6 Convention log.** Any change of convention (basis, denominator, rate form) is written down next to the code and in `docs/decisions.md` the day it changes (lesson 5; `BASIS_CHANGE.md` was cited and untracked).
**R7 Tests travel.** Each core has tests before anything else is built on it; nothing is retired before its tests are ported or rewritten (lessons 6b, 6c).
**R8 No side effects on import, no orphan code.** Nothing rewrites data on import; nothing unused or unported stays in the tree (lessons 6b, 8).
**R9 Size.** A stated line budget for the core and for the output layer, set in 011g stage C and checked in each build brief. As a starting proposal: the output layer is smaller than the core (v2's was 5,150 lines, the largest single source of complexity).
**R10 Progressive schedules.** The sampled rate family is monotone in marginal rate, and the model rejects a non-progressive draw instead of running it.

## 5. What carries over, and what does not
Candidates to port by exception (each needs a named element and a test): v2's layering and `wdt_kernel` (564 lines), the JST return series `jst_r6.json`, the loss-refund and delta-tax mechanics as stated in the papers, and the decomposition identity (residual 1.6e-13 in stage A).
Not carried over: the gain ladder, the fresh-entrant heir rule, strategy verdicts, `eval_core`, the 101 scenarios, the 55 figures and 56 tables, the v1 and v2 output scripts, and any item in `drift-register.md` (the register stays as history; v3 inherits the lessons, not the items).

## 6. Consequences for the other lanes
- **Writing:** the whitepaper outline follows the output manifest, so v3 stage A comes before the outline. The 33-entry paper series is rewritten; the old figure names disappear.
- **Research:** a brief to source the wealth survey and rich-list tail, the return series, and the behavioural ranges (including the Norway leakage figure already cited in the Project Map).
- **Web:** nothing now. The revenue calculator is replaced after v3 (author, 2026-11-16).
- **Crosslinks (007w) and retiring the legacy folders (009c):** both wait for the rewrite and v3.

## 7. Open questions, none blocking the draft of 011g
1. Burden denominator: share of wealth, or the gain-weighted effective lifetime rate, or both (the RATES paper used both: 0.35% and 13.0%).
2. Sample size and seed policy; whether P10 and P90 are reported per output (not per scenario, so a P90 burden and a P10 revenue need not come from one draw).
3. The progressive rate family and its parameters.
4. The SWF share, the horizon N and the start year or years for the path.
5. Whether the model is UK-only (the papers are).
6. The tail dataset and its licence; research confirms before any build.
