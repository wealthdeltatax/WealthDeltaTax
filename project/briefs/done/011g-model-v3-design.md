# 011: Model v3 design

- **Status:** done (stages A to D complete; 040g D2 approved 2026-11-18); retired
- **Author/date:** K. Ogata with the guru, 2026-11-16
- **Depends on:** 001c (merged; synthesis in `docs/model-audit/synthesis.md`)
- **Read:** `docs/model-audit/synthesis.md`, then `docs/model-audit/lessons-so-far.md`. Nothing else need be opened until a stage names it.

## Goal
Design model v3 as a range model with three headline outputs, so that each build brief written afterwards is small, staged and measurable. This brief writes designs and briefs; it builds no model code.

## Decisions (author, 2026-11-16)
All of `synthesis.md` section 3. In short: three headline ranges (government revenue, taxpayer burden, non-payer savings) reported as sampled P10, mean and P90; a year-by-year path with a steady-state summary; a fixed allocation order (refunds, SWF share, relief); a sampled family of progressive rate schedules (logistic in ln W); burden reported both as a share of wealth and as a gain-weighted lifetime rate, each against suggested wealth taxes and today's income tax and CGT; C.1 over TW(1) as a supporting output; the corporate levy reported as its own revenue line; CGT, IHT, stamp duties, council tax, business rates and corporation tax retired at the same moment (headline revenue is the net fiscal effect, every line shown); a threshold of half the median house price per adult; UK data only, through one country data pack (R11); a clean slate with port by exception; the papers are rewritten to follow the results.
- The earlier attempt kept building without control: every stage below ends in a stop, and no implementation brief is written until stage D passes.

## Design
Five design stages (A, A2, B, C, D), each producing one document under `docs/model-v3/` (new folder). The guru writes stages A, A2, C and D with the author; stage B is a research brief.

## Stages
- **A: output manifest and metric register** (guru, with the author). Checkpoint: `docs/model-v3/outputs.yml` and `docs/model-v3/metrics.md` pushed. Check: each of the three headline outputs and the supporting tolerant zone has a formula, a denominator, a unit, a horizon and the whitepaper element it feeds; no metric has two denominators; the burden and savings definitions and the threshold approach are settled; the retired taxes are phased in steps as relief arrives (decided), and the order, the trigger and the year or years each headline refers to are stated. The v2 check in `synthesis.md` section 10 shows the closure turns on both (retired 8.27% of GDP against relief of about 3% to 15%).
- **A2: design review and driver table** (guru, with the author; added 2026-11-16 after the author accepted the review in chat). Checkpoint: `docs/model-v3/drivers.md`, with `metrics.md` and `outputs.yml` amended. Check: policy levers (rate schedule, threshold, retirement order) are swept as named schedules and the exogenous inputs are sampled at two levels reported apart (return risk, parameter ignorance); the revenue identity and a driver table name what moves each headline; the long window is read as a steady-state property; the three added outputs (cash-flow burden M2b and M2c, reform-in-place benchmark M8, capitalisation sensitivity S1) and the public wealth path P6 have a formula, denominator, unit and horizon; stage B is tiered by the drivers.
- **B: input register** (research lane; a separate brief `012r`, written after A). Checkpoint: `docs/model-v3/inputs.md`. Check: every tier 1 input of `drivers.md` (returns and loss years, wealth distribution and tail, behavioural response, retired-tax incidence, income and liquid assets by band, house-price response) has a low, central and high value, a unit and a cited source; tier 2 inputs have one documented range; the tail dataset and its licence are named; the tornado (`docs/model-v3/tornado.md`) is run on tier 1 before stage C. The rate schedule and threshold are levers, not research inputs.
- **C: architecture** (guru). Checkpoint: `docs/model-v3/architecture.md`. Check: it fixes where v3 lives and where it reads `jst_r6.json`; lists the modules in dependence order; sets a line budget for the core and for the output layer; names what is ported by exception with the element that needs it; lists the tests each module needs before the next is built; and states what happens to `model_v1/` and `model_v2/` (brief 009c).
- **D: acceptance plan and build briefs** (guru). Checkpoint: `docs/model-v3/acceptance.md` and the first build brief written. Check: every build stage has a stop and a measurable criterion (a test, a bound, a reproducible number); the smoke test, the seed and sample-size policy and the run script are specified; each requirement R1 to R11 of the synthesis maps to a criterion.
One session does one stage and stops. No model code is written in this brief.

**Split (2026-11-17).** Stage C is run by: 035g (C1 design decisions, with the author), 036r (research: return range method), 037c (code: v2 port inventory), 038c (code: country pack spec) and 039g (C2 architecture, after the others). Stage D is 040g (D1 acceptance, D2 build briefs). Stage checks above are unchanged; each child meets the part of them it names. This brief retires when 040g D2 is approved.

## Touches
New folder `docs/model-v3/`, `docs/briefs/` (new briefs), `STATUS.md`, `docs/lane-plan.html`, `docs/decisions.md`, and one amendment note in `docs/model-audit/synthesis.md` section 3.

## Acceptance criteria
- Stages A, A2, B, C and D checkpoints exist and meet their checks.
- `git diff --stat` shows no change to `model_v1/`, `model_v2/`, `source/` or `pipeline/`.
- Every requirement R1 to R11 appears in `acceptance.md` with its criterion.
- The author has approved stage A and stage A2 before stage B starts, and stage D before any build brief starts.

## Checks to run
A grep that each of R1 to R11 is named in `acceptance.md`; `git diff --stat` limited to the Touches list.

## Out of scope
Writing model code, fixing v1 or v2, writing or editing papers, choosing the whitepaper outline, running the legacy models.

## Open questions
`synthesis.md` section 7: the closure and phasing rule (section 10), the reporting year, seed and sample size, horizon and returns, data gaps. Stage A closes the first; stage B the data gaps; stage C the rest.

## Implementation notes
<!-- progress:start -->
- **Done:** stage A (manifest and metric register), A2 (drivers, range design), B (input register, now 274 rows; 012r, 022r to 024r, 028r, 036r), the tier 1 tornado (027r), C1 design decisions (035g, approved 2026-11-18), and the C inputs: 036r return method, 037c port inventory, 038c country pack spec.
- **Next:** 039g (C2 architecture), then the author approves it; 040g D1 (`acceptance.md`), approval; 040g D2 (build briefs), approval; then this brief retires. 041r (tornado rerun) and 042r (return data gap) run in parallel and feed 039g and the architecture's return module.
- **Decisions:** see `docs/model-v3/stage-c-decisions.md` and `docs/decisions.md`.
- **Gotchas:** 011g's stage texts are the check each child must meet; the split changed who does the work, not the checks.
- **Resume:** read `docs/model-v3/stage-c-decisions.md`, then 039g.
- **Not run:** none.
- **State:** stages A, A2, B and C1 passed; C2 ready.
<!-- progress:end -->
