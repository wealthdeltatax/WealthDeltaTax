# 035: Model v3 stage C: design decisions and architecture

- **Status:** ready
- **Author/date:** K. Ogata with the guru, 2026-11-17
- **Depends on:** 011g (stages A, A2 and B passed; this is its stage C). C1 can start now. C2's return module waits for 036r.
- **Read:** `docs/briefs/011g-model-v3-design.md` (stage C and D text); `docs/model-audit/synthesis.md` sections 3, 4, 5, 7 and 10; `docs/model-v3/drivers.md` (all, with the 2026-11-17 note); `docs/model-v3/tornado.md` sections 1 to 4; `docs/model-v3/metrics.md`; `docs/restructure/order.md` G1, G2 (what the gate reads); `docs/briefs/030c-data-interface.md` (output file shape); `docs/model-lessons/` only where a decision cites it; `docs/agents/guru.md`. The 036r note (`docs/model-v3/returns-method.md`) when it lands.

## Goal
Close the design questions the tier 1 tornado opened (the mean return, the sign of revenue, the rate that the identity needs), then write the architecture, so that stage D can write acceptance criteria and the first build brief with no open design choice. No model code.

## Decisions (author, 2026-11-17)
- The revenue identity takes the arithmetic mean return; paths compound at the geometric rate (`drivers.md` note).
- Retired receipts are 8.11% of GDP (corrected from 8.27).
- The tornado picked the mean return as the dominant driver; the return range is built from a method that a research brief (036r) recommends before the return module is fixed.
- Every page waits for G1 to G5; G1 needs `architecture.md` and `acceptance.md` (`order.md`).
- The earlier attempt kept building without control: each stage ends in a stop, and no implementation brief is written until stage D passes (011g).

## Design
Two stages, one session each, both guru, both ending in a stop for the author. This brief is a design brief: it parallelises nothing, because C2 uses C1's answers.

## Stages
- **C1: design decisions** (guru, with the author). Checkpoint: `docs/model-v3/stage-c-decisions.md`. Check: each question below has an answer, the reason, the file it changes, and the author's date; no question is closed by the guru alone. Put each to the author with the recommended default; one at a time, the first three first.
  1. **Mean return basis.** Confirm: arithmetic mean in the identity (a check and the tornado, not an input to the paths), geometric in compounding, the generator taking the parameter that 036r recommends. Record both figures. The default is as written; the open part is the exact arithmetic figure (4.74 or 4.76), which 036r settles.
  2. **The sign of revenue.** At central inputs M1 is +1.45% of GDP and zero at g = 3.55% (`tornado.md`). Decide: the model never floors or clips M1; one sign convention for every line (positive is a receipt to the state; M1c can be negative); the share of paths with M1 below zero is reported for each horizon; and whether the break-even return is a new output (it would need an id and an element under rule R1, so it goes through a manifest change the author approves, not an edit here). Default: yes to the first three; ask about the fourth.
  3. **The rate the identity needs.** ε is a lever, not an input (D2). Decide that the model computes ε from the named schedule over the wealth distribution, that the identity is only a check, and how the check is run, since v2's realised ε is not recorded (implied 24.5% to 30%, `tornado.md` section 4): by porting the kernel and reproducing v2's 7.34% at v2-like inputs within a stated tolerance. Default as written.
  4. **Replay or sampled paths.** Decide from 036r: the level 1 generator, whether historical replay stays as a cross-check, and how 100-year paths are made from 117 years. Level 2: the range the mean and standard deviation take, and the removal of the double count in the tornado's return swing. Waits for 036r; do the other questions first.
  5. **Refund cap.** The refund cap (cumulative refunds not above cumulative tax paid) makes net revenue non-linear in g, so the core tracks cumulative tax and refunds per payer path. Decide whether the core carries payer-level state or a stratified summary, and the effect on the identity (tornado assumption A3).
  6. **Seed, sample size and years.** Fixed seed recorded in every output (R5); the sample size comes from a convergence test across seeds (036r gives a first figure); base year and price basis; the year each horizon refers to; the reporting start year; how the three horizons map to year counts.
  7. **Behavioural response and capitalisation.** How D5 (shrinking the base) and D10 (capitalisation, metric S1 switched on or off) enter the core, and whether they are level 2 draws or switches.
  8. **Housekeeping the tornado asked for.** Replace 8.27 by 8.11 in `metrics.md` (M1e) and note it in `synthesis.md` section 10 and 5 and in `decisions.md`; the correction block already in section 10 stays. Record the tornado in `decisions.md` if not there. Check the M2 formula against the 0.35% of RATES (an open item of 012r B4).
- **C2: architecture** (guru). Checkpoint: `docs/model-v3/architecture.md`. Check (011g stage C, unchanged): it fixes where v3 lives (`model_v3/`, output at `model_v3/OUTPUTS/outputs.json`, the shape `030c` and the gate G2 read) and where it reads `jst_r6.json`; lists the modules in dependence order (country data pack, returns generator, wealth and payer base, rate schedule and refund mechanics, revenue lines and fund, burden and savings, range runner, output writer); sets a line budget for the core and for the output layer (R9: the output layer smaller than the core); names what is ported by exception with the element that needs it (`wdt_kernel`, `jst_r6.json`, the loss-refund and delta-tax mechanics, the decomposition identity); lists the tests each module needs before the next is built (R7); and states what happens to `model_v1/` and `model_v2/` (brief 009c stays parked; the architecture says when each folder can go). Also: the layering rule R4 as import rules; the country pack format (R11); the run script and smoke test (R5); where each C1 decision lands.
One session does one stage and stops.

## Touches
`docs/model-v3/stage-c-decisions.md` (new), `docs/model-v3/architecture.md` (new), `docs/model-v3/metrics.md` (M1e figure only), `docs/model-audit/synthesis.md` (correction note), `docs/decisions.md`, `STATUS.md`, `docs/lane-plan.html`, this brief's progress block. No change to `outputs.yml`, `inputs.md`, `model_v1/`, `model_v2/`, `source/`, `pipeline/`, `site/`.

## Acceptance criteria
- `stage-c-decisions.md` answers all eight items with the author's date; item 4 is answered after 036r lands or is marked open with the reason.
- `architecture.md` meets every check of 011g stage C above.
- Every requirement R1 to R11 of `synthesis.md` section 4 that touches architecture (R4, R5, R7, R8, R9, R11) has a named place in `architecture.md`.
- The 8.11 correction is in `metrics.md` and `decisions.md`.
- `git diff --stat` shows only the Touches list.
- The author has approved C1 before C2 starts.

## Checks to run
A grep that each of R4, R5, R7, R8, R9, R11 is named in `architecture.md`; a grep for `8.27` in `metrics.md`; `git diff --stat` limited to the Touches list.

## Out of scope
Model code, acceptance criteria and build briefs (stage D), rewriting the register or the manifest, the writing and site lanes, running v1 or v2.

## Open questions
Whether the break-even return is an output (C1 item 2); whether the core carries payer-level state (item 5); whether 036r recommends replay or sampled paths (item 4).

## Implementation notes
<!-- progress:start -->
- **Done:**
- **Next:** C1, items 1 to 3 with the author; item 4 after 036r.
- **Decisions:**
- **Gotchas:** the tornado's return swing mixes level 1 and level 2 (see 036r); do not trust it for the level 2 range.
- **Resume:**
- **Not run:**
- **State:** ready; not started
<!-- progress:end -->
