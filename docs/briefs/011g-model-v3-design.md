# 011: Model v3 design

- **Status:** underway (stage A passed 2026-11-16, author confirmed all four items; stage A2 drafted 2026-11-16 after the author accepted the design review: `docs/model-v3/drivers.md`, amended `metrics.md` and `outputs.yml`; the author reviews A2 before stage B starts)
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
- **Done:** stage A passed (16 entries; windows, order, revenue-weighted M2, G = 30 confirmed). Stage A2 drafted: `drivers.md`, range design and reading rule in `metrics.md`, new metrics M2b, M2c, M8, S1 and P6, manifest now 21 entries.
- **Next:** the author reviews A2 (and confirms the retirement trigger default, the named-schedule choice rule and the 0.5-point tornado cut-off, all PROPOSED); then write 012r around the tier 1 inputs.
- **Decisions:** the author accepted the design review of 2026-11-16: levers swept and not sampled; two-level uncertainty; long window read as steady state; added cash-flow burden, reform-in-place benchmark and capitalisation sensitivity. Six taxes retire; stamp duties carry two receipt lines.
- **Gotchas:** my chat figure of 3% of GDP for the identity was an unsourced guess and disagrees with v2's 7.34% post-fill WDT (`drivers.md` section 1). The earlier note said 14 outputs; it is now 21.
- **Resume:** read `docs/model-v3/drivers.md`, then `metrics.md` range design, then write 012r.
- **Not run:** M2 against the RATES paper's 0.35%; the Green Book schedule check; the tornado (it needs 012r's values).
- **State:** stage A2 drafted; waiting for the author's review
<!-- progress:end -->
