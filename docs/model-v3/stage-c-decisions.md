# Model v3 stage C1: design decisions

Brief 035g. Each item: the decision, the reason, the file it changes, and the author's date. No item is closed by the guru alone. Item 4 waits for 036r.

| # | Item | Status |
|---|---|---|
| 1 | Mean return basis | decided 2026-11-17 |
| 2 | Sign of revenue | decided 2026-11-17; one manifest proposal awaits approval |
| 3 | The rate the identity needs | decided 2026-11-17 |
| 4 | Replay or sampled paths | **open: waits for 036r** |
| 5 | Refund cap state | decided 2026-11-17 |
| 6 | Seed, sample size and years | decided 2026-11-17; numbers set later |
| 7 | Behaviour and capitalisation | decided 2026-11-18 |
| 8 | Housekeeping | done |

## 1. Mean return basis
**Decision (author, 2026-11-17):** one mean return throughout, the geometric mean (I-D1a, 4.42%): in the paths, in the identity check and in the tornado. The earlier answer of the same evening (arithmetic for the identity) is withdrawn. **Reason:** keep the assumptions as few as possible; with symmetric refunds a payer's cumulative net tax follows their compounding net gain. **Consequence:** the 0.34 point difference to the arithmetic mean (about 0.5 points of GDP of M1) is not in the model; v2's 7.34% used the arithmetic 4.74%, so the port-reproduction test of item 3 uses v2's own parameter. Brief 036r still recommends the generator's parameters. **Files:** `drivers.md` (note of 2026-11-18, supersedes 2026-11-17).

## 2. The sign of revenue
**Decision (author, 2026-11-17):** (a) the model never floors or clips M1; (b) one sign convention for every line: positive is a receipt to the state, and M1c (fund income) can be negative; (c) the share of paths with M1 below zero is reported for each horizon; (d) the break-even return is a new reported output. **Reason:** at central inputs M1 is +1.45% of GDP and zero at a return of 3.55% (`tornado.md`); a clipped M1 would hide the central risk. **Files:** `architecture.md` (039g); `outputs.yml` and `metrics.md` change only after the author approves the id and element below.

**Proposal for approval (nothing edited):** new metric `M1f`, "Break-even mean return: the geometric mean real return at which M1 is zero, at the named schedule and central other inputs", unit `pct`, decimals 2, horizons all three. New outputs `O1e` (break-even return, `summary: point_and_range`, `by: [schedule]`, element `FISC`, `UNCER`) and `O1f` (share of paths with M1 below zero, `summary: point_and_range`, `by: [horizon, schedule]`, unit `pct`, element `FISC`, `UNCER`). Rule R1: both would be cited by FISC and UNCER; neither exists until the author says yes.

## 3. The rate the identity needs
**Decision (author, 2026-11-17, after clarifying that the question meant the model computes it):** the effective rate on gains ε is a lever, not an input. The model computes each payer's tax from the named schedule over the wealth distribution; ε is an output of that. The identity `M1a ≈ ε · g · ω − refunds` is a check only. v2's realised ε is not recorded (implied 24.5% to 30%, `tornado.md` section 4), so the check is run by porting the kernel and reproducing v2's 7.34% of GDP at v2-like inputs within a tolerance set in 039g from the port inventory (037c). **Files:** `architecture.md`, `acceptance.md` (040g).

## 4. Replay or sampled paths
**Open.** Waits for 036r (`returns-method.md`): the level 1 generator, whether historical replay stays as a cross-check, how 100-year paths are made from 117 years, the level 2 range for mean and standard deviation, and the removal of the double count in the tornado's return swing. Do not read the tornado's return swing as the level 2 range: it mixes level 1 and level 2.

## 5. Refund cap
**Decision (author, 2026-11-17):** the core carries **payer-level state per path** (cumulative tax paid, cumulative refunds), so the cap and fall-through refunds are exact and tested directly. **Reason:** the cap (cumulative refunds not above cumulative tax paid) makes net revenue non-linear in the return, so the identity's refund term (tornado assumption A3) cannot be a closed form. **Consequence:** heavier compute; the sample size comes from the convergence test of item 6. **Files:** `architecture.md`.

## 6. Seed, sample size and years
**Decision (author, 2026-11-17):** one fixed seed recorded in every output file (R5); sample size from a convergence test across seeds (036r gives a first figure); base year 2025-26 in 2025-26 prices; the three horizons are year counts set in the architecture (the year each horizon refers to is stated beside it); reporting starts at the first year after introduction. **Numbers still to set:** the seed, the sample size and the horizon year counts, in `architecture.md` after 036r and the convergence test.

## 7. Behavioural response and capitalisation
**Decision (author, 2026-11-18):** (a) D5, the response that shrinks the base, is a **level 2 draw**: its strength is drawn from the register range (I-D5a to I-D5d) in each level 2 draw, so it widens the p10 and p90 like any other ignorance; (b) D10, capitalisation (metric S1), is a **switch, off in the headline**: one extra reported variant shows S1 on; it is a regime, not a parameter, and is not averaged into the range. **Files:** `architecture.md`; S1 reported as a variant, not a manifest change.

## 8. Housekeeping
- 8.27 replaced by 8.11 in `metrics.md` (M1e), a correction note in `synthesis.md` section 10, and a `decisions.md` entry (all done 2026-11-17). `synthesis.md` section 5 holds no figure at 8.27.
- Tornado recorded in `decisions.md` (done).
- M2 against the RATES paper's 0.35% (012r B4): closed by the author on 2026-11-16 (`metrics.md` M2 denominator: same year, start-of-year wealth). RATES divides by terminal wealth 30 years on; the two are a different quantity and are not compared. The RATES claim "below 1 to 2%" is re-derived when v3 runs, not before.
