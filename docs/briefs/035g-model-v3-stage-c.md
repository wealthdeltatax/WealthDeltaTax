# 035: Model v3 stage C1: design decisions

- **Status:** ready
- **Author/date:** K. Ogata with the guru, 2026-11-17
- **Depends on:** 011g (stages A, A2 and B passed; this is its stage C1). Starts now; item 4 waits for 036r. Stage C2 (architecture) is brief 039g.
- **Read:** `docs/briefs/011g-model-v3-design.md` (stage C and D text); `docs/model-audit/synthesis.md` sections 3, 4, 5, 7 and 10; `docs/model-v3/drivers.md` (all, with the 2026-11-17 note); `docs/model-v3/tornado.md` sections 1 to 4; `docs/model-v3/metrics.md`; `docs/restructure/order.md` G1, G2 (what the gate reads); `docs/briefs/030c-data-interface.md` (output file shape); `docs/model-lessons/` only where a decision cites it; `docs/agents/guru.md`. The 036r note (`docs/model-v3/returns-method.md`) when it lands.

## Goal
Close the design questions the tier 1 tornado opened (the mean return, the sign of revenue, the rate that the identity needs), so that the architecture (039g) can be written with no open design choice. No model code.

## Decisions (author, 2026-11-17)
- The revenue identity takes the arithmetic mean return; paths compound at the geometric rate (`drivers.md` note).
- Retired receipts are 8.11% of GDP (corrected from 8.27).
- The tornado picked the mean return as the dominant driver; the return range is built from a method that a research brief (036r) recommends before the return module is fixed.
- Every page waits for G1 to G5; G1 needs `architecture.md` and `acceptance.md` (`order.md`).
- The earlier attempt kept building without control: each stage ends in a stop, and no implementation brief is written until stage D passes (011g).

## Design
One stage, guru with the author, ending in a stop. The model design now splits into: 035g (this, C1), 036r (return method), 037c (v2 port inventory), 038c (country pack spec), 039g (C2, architecture), 040g (stage D). 036r, 037c and 038c run in parallel with C1.

## Stages
- **C1: design decisions** (guru, with the author). Checkpoint: `docs/model-v3/stage-c-decisions.md`. Check: each question below has an answer, the reason, the file it changes, and the author's date; no question is closed by the guru alone. Put each to the author with the recommended default; one at a time, the first three first.
  1. **Mean return basis.** Confirm: arithmetic mean in the identity (a check and the tornado, not an input to the paths), geometric in compounding, the generator taking the parameter that 036r recommends. Record both figures. The default is as written; the open part is the exact arithmetic figure (4.74 or 4.76), which 036r settles.
  2. **The sign of revenue.** At central inputs M1 is +1.45% of GDP and zero at g = 3.55% (`tornado.md`). Decide: the model never floors or clips M1; one sign convention for every line (positive is a receipt to the state; M1c can be negative); the share of paths with M1 below zero is reported for each horizon; and whether the break-even return is a new output (it would need an id and an element under rule R1, so it goes through a manifest change the author approves, not an edit here). Default: yes to the first three; ask about the fourth.
  3. **The rate the identity needs.** ε is a lever, not an input (D2). Decide that the model computes ε from the named schedule over the wealth distribution, that the identity is only a check, and how the check is run, since v2's realised ε is not recorded (implied 24.5% to 30%, `tornado.md` section 4): by porting the kernel and reproducing v2's 7.34% at v2-like inputs within a stated tolerance (where v2 computes ε is in `port-inventory.md`, 037c). Default as written.
  4. **Replay or sampled paths.** Decide from 036r: the level 1 generator, whether historical replay stays as a cross-check, and how 100-year paths are made from 117 years. Level 2: the range the mean and standard deviation take, and the removal of the double count in the tornado's return swing. Waits for 036r; do the other questions first.
  5. **Refund cap.** The refund cap (cumulative refunds not above cumulative tax paid) makes net revenue non-linear in g, so the core tracks cumulative tax and refunds per payer path. Decide whether the core carries payer-level state or a stratified summary, and the effect on the identity (tornado assumption A3).
  6. **Seed, sample size and years.** Fixed seed recorded in every output (R5); the sample size comes from a convergence test across seeds (036r gives a first figure); base year and price basis; the year each horizon refers to; the reporting start year; how the three horizons map to year counts.
  7. **Behavioural response and capitalisation.** How D5 (shrinking the base) and D10 (capitalisation, metric S1 switched on or off) enter the core, and whether they are level 2 draws or switches.
  8. **Housekeeping the tornado asked for.** Replace 8.27 by 8.11 in `metrics.md` (M1e) and note it in `synthesis.md` section 10 and 5 and in `decisions.md`; the correction block already in section 10 stays. Record the tornado in `decisions.md` if not there. Check the M2 formula against the 0.35% of RATES (an open item of 012r B4).
- **C2: architecture** is now brief 039g (needs this stage approved, and 037c port inventory, 038c country pack spec and 036r).
One session does one stage and stops.

## Touches
`docs/model-v3/stage-c-decisions.md` (new), `docs/model-v3/metrics.md` (M1e figure only), `docs/model-audit/synthesis.md` (correction note), `docs/decisions.md`, `STATUS.md`, `docs/lane-plan.html`, this brief's progress block. No change to `outputs.yml`, `inputs.md`, `model_v1/`, `model_v2/`, `source/`, `pipeline/`, `site/`.

## Acceptance criteria
- `stage-c-decisions.md` answers all eight items with the author's date; item 4 is answered after 036r lands or is marked open with the reason.
- The 8.11 correction is in `metrics.md` and `decisions.md`.
- `git diff --stat` shows only the Touches list.
- The author has approved C1 before 039g starts.

## Checks to run
A grep for `8.27` in `metrics.md`; `git diff --stat` limited to the Touches list.

## Out of scope
Model code, acceptance criteria and build briefs (stage D), rewriting the register or the manifest, the writing and site lanes, running v1 or v2.

## Open questions
Whether the break-even return is an output (C1 item 2); whether the core carries payer-level state (item 5); whether 036r recommends replay or sampled paths (item 4).

## Implementation notes
<!-- progress:start -->
- **Done:**
- **Next:** items 1 to 3 with the author; item 4 after 036r.
- **Decisions:**
- **Gotchas:** the tornado's return swing mixes level 1 and level 2 (see 036r); do not trust it for the level 2 range.
- **Resume:**
- **Not run:**
- **State:** ready; not started
<!-- progress:end -->
