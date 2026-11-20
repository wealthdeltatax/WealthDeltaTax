# 095: UK evidence and calibration map for household wealth flows (test C)

- **Status:** ready
- **Author/date:** K. Ogata with the guru, 2026-11-20
- **Depends on:** 093r (merged); runs in parallel with 094r
- **Read:** `docs/research/093r-consumption-depletion-evidence.md` (all; its section 7 lists the next evidence to fetch); `docs/hypotheses/household-consumption-and-wealth-replenishment.md` (sections 11 to 14); `docs/model-v3/inputs.md` (I-W3a to I-W3d, I-D4 rows, S5 on top-tail coverage); `docs/agents/reference/research/reference-workflow.md`; archived `docs/archive/briefs/080r-declared-alpha-evidence.md`.

## Goal
Map what UK data can and cannot identify for each flow of a household net-worth account: net saving from current income, retained property income, capital gains, net transfers, debt, pensions and drawdown. Build on 093r rather than repeating it. The product is a table that tells the cohort design (096r) which flows have a measured level, rate, transition or only a bound, and which are gaps.

## Decisions (author, 2026-11-20)
- No replacement for the legacy 3.5%, and no band-level depletion rate where the data do not identify one (see 094r Decisions).
- Do **not** convert the aggregate household saving ratio into a wealth-depletion rate (093r section 3.2 shows why: the ratio includes saving out of labour income, pension accrual and property income, while c acts on the existing stock).
- Keep **labour-funded saving, retained property income, capital gains, transfers and dissaving apart** in every figure, or say which a figure mixes.
- No value is selected for its effect on WDT revenue.

## Design
1. **Sources to cover** (UK first; say what is foreign and why it is used):
   - ONS Wealth and Assets Survey: longitudinal change by wealth band and age, asset and liability composition, pension wealth; what published tables give without microdata.
   - ONS household income, spending and wealth (matched, experimental; keep that label); ONS sector accounts and household balance sheet (saving, revaluation, other changes in volume, property income, holding gains by year); ONS household property income series (needed for the income yield `y` in 093r 3.2).
   - ELSA and IFS retirement drawdown (England, 50 plus, financial wealth only); Bozio, Emmerson, O'Dea and Tetlow (2013) full text for saving against permanent income (093r flagged that the numbers were not read).
   - Resolution Foundation passive and active wealth work, the Bank of England and academic work on saving, dissaving and wealth accumulation at the top.
2. **For each flow** (net saving, property income, capital gains, transfers given and received, liabilities and debt service, pension contributions and accrual, drawdown): the quantity measured, the number (by band, age or tenure where given), population, years, definitions, what it mixes, licence, and whether the data identify a **level, rate, transition or only a bound**.
3. **Definitions that do not match.** A bridge table between national-account and survey definitions for saving, income, net wealth and consumption (gross or net of fixed capital, pension treatment, imputed rent). Do not combine survey and account figures without saying how they differ.
4. **Gaps and data requests.** List what only microdata or a non-public table can give (WAS by decile, top-tail adjustments, NMG survey), with the access route and licence, as requests the author can action. The shell cannot reach the sites; sources are read by search and fetch, so mark each number as read from a fetched page and not yet checked against the primary file.
5. **Per-flow table for 096r:** flow, best UK evidence, what it identifies, range if one is supportable, data or judgement, and the gap. A flow with no supportable range says so; do not fill it.
6. **Income-funded saving at the top.** What UK evidence says about the share of top-decile wealth change that comes from saving out of income against returns; if none, say so and name the nearest bound.

## Touches
`docs/research/095r-uk-household-flow-evidence-map.md` (new), this brief's progress block, `docs/agents/friction-log.md`. No register, code or manifest edits; proposed register rows go in the note only (080r form).

## Acceptance criteria
- Each flow in item 2 has an entry with quantity, number, population, years, definitions and identification status, or is marked as a gap with a stated reason.
- The bridge table (item 3) and the per-flow table (item 5) are present.
- No figure is used across definitions without the bridge; mixed quantities are labelled.
- The data-request list (item 4) names the access route for each.
- Sources list with links; `git diff --stat` limited to Touches.

## Checks to run
None to run (a research note); the guru checks cited numbers against the sources before review.

## Out of scope
Kernel mapping and account specification (094r); cohort cells (096r); calibrating or choosing any parameter; backcasts; WDT results.

## Open questions
None.

## Implementation notes
<!-- progress:start -->
- **Done:**
- **Next:**
- **Decisions:**
- **Gotchas:**
- **Resume:**
- **Not run:**
- **State:** ready; not started
<!-- progress:end -->
