# Model v3 stage C1: design decisions

Brief 035g. Each item: the decision, the reason, the file it changes, and the author's date. No item is closed by the guru alone. Item 4 waits for 036r.

| # | Item | Status |
|---|---|---|
| 1 | Mean return basis | decided 2026-11-18 (revised) |
| 2 | Sign of revenue | decided 2026-11-17; one manifest proposal awaits approval |
| 3 | The rate the identity needs | decided 2026-11-17 |
| 4 | Replay or sampled paths | decided 2026-11-18 |
| 5 | Refund cap state | decided 2026-11-17 |
| 6 | Seed, sample size and years | decided 2026-11-17; numbers set later |
| 7 | Behaviour and capitalisation | decided 2026-11-18 |
| 8 | Housekeeping | done |
| 9 | Refund rule | decided 2026-11-18 |
| 10 | Envelope at death | decided 2026-11-18 |

## 1. Mean return basis
**Decision (author, 2026-11-18, revised after the explanation of arithmetic and geometric means):** the generator and the revenue identity check both use the observed **arithmetic** mean (4.742%, SD 8.219%, lag-1 autocorrelation 0.30, `returns-method.md`); the figure quoted to readers as the holder's return is the **geometric** mean (4.42%), which comes out of compounding the generator's paths. No half-variance adjustment anywhere. This replaces the answer of 2026-11-17 (geometric throughout) and the note of 2026-11-17 in `drivers.md`. **Reason:** a simulation draws annual returns, so it needs the arithmetic mean; the expected tax in a single year is the rate on the arithmetic average gain; the geometric mean is what a long-run holder experiences. **Consequence:** the identity check at central inputs lifts M1 by about 0.5 points of GDP against the tornado (which ran at the geometric 4.42%); the tornado is rerun with the level 2 band (brief 041r). **Files:** `drivers.md` (note of 2026-11-18, second version).

## 2. The sign of revenue
**Decision (author, 2026-11-17):** (a) the model never floors or clips M1; (b) one sign convention for every line: positive is a receipt to the state, and M1c (fund income) can be negative; (c) the share of paths with M1 below zero is reported for each horizon; (d) the break-even return is a new reported output. **Reason:** at central inputs M1 is +1.45% of GDP and zero at a return of 3.55% (`tornado.md`); a clipped M1 would hide the central risk. **Files:** `architecture.md` (039g); `outputs.yml` and `metrics.md` change only after the author approves the id and element below.

**Proposal for approval (nothing edited):** new metric `M1f`, "Break-even mean return: the geometric mean real return at which M1 is zero, at the named schedule and central other inputs", unit `pct`, decimals 2, horizons all three. New outputs `O1e` (break-even return, `summary: point_and_range`, `by: [schedule]`, element `FISC`, `UNCER`) and `O1f` (share of paths with M1 below zero, `summary: point_and_range`, `by: [horizon, schedule]`, unit `pct`, element `FISC`, `UNCER`). Rule R1: both would be cited by FISC and UNCER; neither exists until the author says yes.

## 3. The rate the identity needs
**Decision (author, 2026-11-17, after clarifying that the question meant the model computes it):** the effective rate on gains ε is a lever, not an input. The model computes each payer's tax from the named schedule over the wealth distribution; ε is an output of that. The identity `M1a ≈ ε · g · ω − refunds` is a check only. v2's realised ε is not recorded (implied 24.5% to 30%, `tornado.md` section 4), so the check is run by porting the kernel and reproducing v2's 7.34% of GDP at v2-like inputs within a tolerance set in 039g from the port inventory (037c). **Files:** `architecture.md`, `acceptance.md` (040g).

## 4. Replay or sampled paths
**Decision (author, 2026-11-18, on the recommendation of `returns-method.md`):** (a) **level 1 generator: AR(1) with normal innovations**, parameterised by the arithmetic mean, the marginal standard deviation and the lag-1 autocorrelation (4.742%, 8.219%, 0.30); a stationary block bootstrap (mean block 3) is run as a robustness check and reported beside it; historical window replay is not the generator (it is not a distribution: all 117 windows share the 6-year loss run). (b) **100-year paths** are sampled from the generator, not resampled from 117 years; the history carries about 63 effective annual observations (0.63 of an independent 100-year path), a limit stated in the papers. (c) **Level 2:** the true mean's 80% band is 3.41% to 6.07% (arithmetic, central 4.74), the SD 7.47% to 8.96%, lag-1 autocorrelation 0.19 to 0.42 (`returns-method.md` section 4). (d) **Pool all 117 years**; no structural break is modelled (p = 0.38); the war years are a named sensitivity of about +0.5 points on the mean, reported not drawn. (e) **The tornado's return swing is a double count** (level 1 spread of 30-year paths reported as parameter ignorance): replace it with the level 2 band (swing 8.78 to about 4.4 points of GDP); rerun brief 041r. (f) **The gap 2020 to 2025:** no splice now; a research brief checks licences and series (042r). **Files:** `architecture.md`; replacement register rows (below) applied to `inputs.md` by the guru.

## 5. Refund cap
**Decision (author, 2026-11-17):** the core carries **payer-level state per path** (cumulative tax paid, cumulative refunds), so the cap and fall-through refunds are exact and tested directly. **Reason:** the cap (cumulative refunds not above cumulative tax paid) makes net revenue non-linear in the return, so the identity's refund term (tornado assumption A3) cannot be a closed form. **Consequence:** heavier compute; the sample size comes from the convergence test of item 6. **Files:** `architecture.md`.

## 6. Seed, sample size and years
**Decision (author, 2026-11-17):** one fixed seed recorded in every output file (R5); sample size from a convergence test across seeds (036r: 10,000 paths is the first size within 0.1 point across five seeds on the toy statistics; the full test is stage C's); base year 2025-26 in 2025-26 prices; the three horizons are year counts set in the architecture (the year each horizon refers to is stated beside it); reporting starts at the first year after introduction. **Numbers still to set:** the seed, the sample size and the horizon year counts, in `architecture.md` after 036r and the convergence test.

## 7. Behavioural response and capitalisation
**Decision (author, 2026-11-18):** (a) D5, the response that shrinks the base, is a **level 2 draw**: its strength is drawn from the register range (I-D5a to I-D5d) in each level 2 draw, so it widens the p10 and p90 like any other ignorance; (b) D10, capitalisation (metric S1), is a **switch, off in the headline**: one extra reported variant shows S1 on; it is a regime, not a parameter, and is not averaged into the range. **Files:** `architecture.md`; S1 reported as a variant, not a manifest change.

## 8. Housekeeping
- 8.27 replaced by 8.11 in `metrics.md` (M1e), a correction note in `synthesis.md` section 10, and a `decisions.md` entry (all done 2026-11-17). `synthesis.md` section 5 holds no figure at 8.27.
- Tornado recorded in `decisions.md` (done).
- M2 against the RATES paper's 0.35% (012r B4): closed by the author on 2026-11-16 (`metrics.md` M2 denominator: same year, start-of-year wealth). RATES divides by terminal wealth 30 years on; the two are a different quantity and are not compared. The RATES claim "below 1 to 2%" is re-derived when v3 runs, not before.

## 9. Refund rule
**Decision (author, 2026-11-18):** the papers' rule: a loss is refunded at the marginal rate on an equivalent gain (**tau x loss**), not v2's ratio-mirror (tau x loss x new wealth / old wealth). **Reason:** simplest, and it is what the papers say. **Consequence:** the port reproduction of v2's 7.34% differs slightly from v2; the difference is measured and reported, and the kernel gets explicit cap and refund-rule tests. **Files:** `architecture.md`, `acceptance.md`.

## 10. Envelope at death
**Decision (author, 2026-11-18):** the loss-refund envelope **resets at death**, as v2 does. **Consequence:** WP section 3.5 says the family's contribution history persists; the paper text is changed to describe the reset (a writing-lane item, recorded for the spoke that covers the cap: FUND or MECH). **Files:** `architecture.md`; ledger note for the writing briefs.

## Also decided 2026-11-18 (not C1 items)
- `logistic_ln_ref` is not run to record v2's realised epsilon (default kept).
- RATES section 4's tau formula differs from v2 and VAL section 5 (`port-inventory.md` section 3.3 C): a writing item, to be fixed when the spoke that covers the rate schedule is written.

