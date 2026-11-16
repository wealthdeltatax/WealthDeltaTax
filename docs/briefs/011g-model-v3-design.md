# 011: Model v3 design

- **Status:** underway (stage A passed 2026-11-16: `docs/model-v3/metrics.md`, `docs/model-v3/outputs.yml`, author confirmed all four items; stage B not yet started)
- **Author/date:** K. Ogata with the guru, 2026-11-16
- **Depends on:** 001c (merged; synthesis in `docs/model-audit/synthesis.md`)
- **Read:** `docs/model-audit/synthesis.md`, then `docs/model-audit/lessons-so-far.md`. Nothing else need be opened until a stage names it.

## Goal
Design model v3 as a range model with three headline outputs, so that each build brief written afterwards is small, staged and measurable. This brief writes designs and briefs; it builds no model code.

## Decisions (author, 2026-11-16)
All of `synthesis.md` section 3. In short: three headline ranges (government revenue, taxpayer burden, non-payer savings) reported as sampled P10, mean and P90; a year-by-year path with a steady-state summary; a fixed allocation order (refunds, SWF share, relief); a sampled family of progressive rate schedules (logistic in ln W); burden reported both as a share of wealth and as a gain-weighted lifetime rate, each against suggested wealth taxes and today's income tax and CGT; C.1 over TW(1) as a supporting output; the corporate levy reported as its own revenue line; CGT, IHT, stamp duties, council tax, business rates and corporation tax retired at the same moment (headline revenue is the net fiscal effect, every line shown); a threshold of half the median house price per adult; UK data only, through one country data pack (R11); a clean slate with port by exception; the papers are rewritten to follow the results.
- The earlier attempt kept building without control: every stage below ends in a stop, and no implementation brief is written until stage D passes.

## Design
Four design stages, each producing one document under `docs/model-v3/` (new folder). The guru writes stages A, C and D with the author; stage B is a research brief.

## Stages
- **A: output manifest and metric register** (guru, with the author). Checkpoint: `docs/model-v3/outputs.yml` and `docs/model-v3/metrics.md` pushed. Check: each of the three headline outputs and the supporting tolerant zone has a formula, a denominator, a unit, a horizon and the whitepaper element it feeds; no metric has two denominators; the burden and savings definitions and the threshold approach are settled; the retired taxes are phased in steps as relief arrives (decided), and the order, the trigger and the year or years each headline refers to are stated. The v2 check in `synthesis.md` section 10 shows the closure turns on both (retired 8.27% of GDP against relief of about 3% to 15%).
- **B: input register** (research lane; a separate brief `012r`, written after A). Checkpoint: `docs/model-v3/inputs.md`. Check: every ranged input (wealth distribution and threshold, returns and loss years, behavioural response, rate schedule family) has a low, central and high value, a unit and a cited source; the tail dataset and its licence are named.
- **C: architecture** (guru). Checkpoint: `docs/model-v3/architecture.md`. Check: it fixes where v3 lives and where it reads `jst_r6.json`; lists the modules in dependence order; sets a line budget for the core and for the output layer; names what is ported by exception with the element that needs it; lists the tests each module needs before the next is built; and states what happens to `model_v1/` and `model_v2/` (brief 009c).
- **D: acceptance plan and build briefs** (guru). Checkpoint: `docs/model-v3/acceptance.md` and the first build brief written. Check: every build stage has a stop and a measurable criterion (a test, a bound, a reproducible number); the smoke test, the seed and sample-size policy and the run script are specified; each requirement R1 to R11 of the synthesis maps to a criterion.
One session does one stage and stops. No model code is written in this brief.

## Touches
New folder `docs/model-v3/`, `docs/briefs/` (new briefs), `STATUS.md`, `docs/lane-plan.html`, `docs/decisions.md`.

## Acceptance criteria
- Stages A to D checkpoints exist and meet their checks.
- `git diff --stat` shows no change to `model_v1/`, `model_v2/`, `source/` or `pipeline/`.
- Every requirement R1 to R11 appears in `acceptance.md` with its criterion.
- The author has approved stage A before stage B starts, and stage D before any build brief starts.

## Checks to run
A grep that each of R1 to R11 is named in `acceptance.md`; `git diff --stat` limited to the Touches list.

## Out of scope
Writing model code, fixing v1 or v2, writing or editing papers, choosing the whitepaper outline, running the legacy models.

## Open questions
`synthesis.md` section 7: the closure and phasing rule (section 10), the reporting year, seed and sample size, horizon and returns, data gaps. Stage A closes the first; stage B the data gaps; stage C the rest.

## Implementation notes
<!-- progress:start -->
- **Done:** stage A passed: 16 entries in the manifest, every metric in the register; windows, retirement order (ascending by receipts), revenue-weighted M2 and G = 30 confirmed.
- **Next:** stage B, research brief 012r (input register), once the author has answered the design questions raised on 2026-11-16 (see State).
- **Decisions:** six taxes retired, stamp duties carry two receipt lines (seven M1e lines); the retirement trigger is the stated default that follows from P3, not yet confirmed.
- **Gotchas:** the brief's earlier note said 14 outputs; the manifest has 16.
- **Resume:** read `docs/model-v3/metrics.md`, then write 012r.
- **Not run:** the M2 check against the RATES paper's 0.35%; the Green Book schedule check (both go to 012r or the writing lane).
- **State:** stage A passed; 012r is held while the author considers a design review of the approach (sampled policy schedules, 100-year horizon, missing comparators)
<!-- progress:end -->
