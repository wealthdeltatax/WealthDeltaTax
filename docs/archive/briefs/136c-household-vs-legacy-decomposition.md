# 136: Why the household arm differs from legacy: flow and revenue decomposition

- **Status:** ready
- **Author/date:** K. Ogata with the guru, 2026-11-22
- **Depends on:** 124c (merged); independent of 133c (runs at the three grid points that complete)
- **Read (block 0: the first two only):** (1) `docs/model-v3/household-arm-run.md` (the checks, the household and legacy tables, "Odd"); (2) `docs/agents/code.md`. Later, by block: `model_v3/runner/arm.py` (`LegacyHook`, `HouseholdHook.account`); `docs/model-v3/household-arm-account/account_table.py` and `ledger_table.py` (how the account is read); `model_v3/core/burden.py` (M2, M2d definitions); `docs/model-v3/outputs.yml` (M1a, M2, M4a, P6 titles and units, read only).

## Goal
124c showed the arms agree on some outputs and differ sharply on others, and nobody has said why. Gross receipts are similar (M1a short 2.43 to 4.48 household against 3.66 legacy; long 0.88 to 6.66 against 1.18), but **M2, the burden in life as a share of wealth, is far lower** (overall 0.15 to 0.38 against 1.27; D10 0.20 to 0.46 against 1.50), the long-run M1 net and M1c (fund return) differ in sign or size, and the public wealth path P6 (fund assets, % of GDP) is far lower (22 to 78 against 1,170 per cent at the quoted years). Find out, with numbers, **which differences between the arms produce each gap**, and whether any gap is a defect.

## Decisions (author, 2026-11-22)
- Diagnosis only: no parameter, rule, register row or model file changes. A suspected defect is reported with its inputs and a minimal case, not fixed here.
- Compare on **common ground first**: both arms on the same constant market path (the household arm's mean `mu`, no spread; the legacy arm on a constant path of that mean), at the three held grid points (`median_mid`, `max_mid`, `median_low`), so path variation and the I1 alarms drop out. Then, as a check, the legacy arm on its own stochastic paths.
- The legacy arm is a comparator only (the 3.5% is abandoned as a central value). The note does not judge which arm is "right"; it says what each assumes.
- Every result is labelled with its scenario point; no figure is called central, no headline.

## Blocks (one push each; `docs/agents/code.md`)
- **Block 0:** progress block pushed.
- **Block 1: the flow comparison.** `docs/model-v3/household-vs-legacy/flows.py` and `flows.csv`: per line (all 14), at years 1, 10, 30, 100, for each arm: wealth path, the effective growth rate of wealth, the **implied consumption-equivalent** (`c_eq = 1 - (W[t+1]/W[t])/(1+g)` for legacy; the same quantity on the household account), and the household account terms as shares of wealth (saving S, holding gain CG, transfers TR, residual O, tax T). One table says where the household line's wealth path sits against the legacy path and why (saving above or below the 3.5% depletion, retained yield, deaths, income). Push.
- **Block 2: the revenue and burden decomposition.** `docs/model-v3/household-vs-legacy/decomp.py` and `decomp.csv`: for M1a, M2, M2d and P6 write each output as `base x rate` (the wealth base summed over lines with their weights, and tax over base), then the ratio household to legacy as `base ratio x rate ratio`, by horizon and band; for P6, the fund path split into receipts, the fund return (M1c) and payout. State the denominators (what M2's "share of wealth" divides by in each arm) and whether the two arms' denominators are like for like. Checks: the decomposition reproduces the 124c numbers within the stated error. Push.
- **Block 3: the note.** `docs/model-v3/household-vs-legacy.md`: for each of M1a, M2, M2d, M1 net long, M1c and P6, the ranked reasons for the gap with their numbers (base size from lower depletion, tax rate, death settlement timing, income and the B.6g scaling, pension inside the base, class composition and returns, fund return and the safe stand-in, anything else), the share of each gap each reason explains, what remains unexplained, and a **defects list** (anything inconsistent: a denominator that differs, a unit, a path that cannot be right). No recommendation of values or of which arm to keep. Change report; push; stop.
**Stop rule.** After three blocks, or a quarter of the budget left, push what exists and list the rest under Next. Run grids in the background; print summary lines only; suites never piped.

## Touches
`docs/model-v3/household-vs-legacy/` (new scripts and CSVs), `docs/model-v3/household-vs-legacy.md` (new), tests for the helper functions, `docs/model-v3/architecture.md` (budget rows only if a test file is added). Read-only on the kernel, `revenue.py`, `burden.py`, `arm.py`, the register and the pack. Name any further file before editing it.

## Acceptance criteria
- `test_legacy_digest` and all suites pass; no model file changed.
- Each of M1a, M2, M2d, M1 net long, M1c and P6 has a decomposition whose parts reproduce the household and legacy values within a stated error.
- The note says what each of the M2 and P6 gaps is made of in numbers, what stays unexplained, and lists defects with minimal cases (or says none were found).
- Scenario labels on every table; no central value, no headline.

## Out of scope
Fixing anything found, changing the denominators, calibration, the saving gradient, pension withdrawal, per-path household behaviour, validation against moments, the lien (133c).

## Open questions
Whether the P6 quoted values (22 to 78 against 1,170) are the same quantity in the two arms (the agent checks the units and the years first and says so before decomposing).

## Implementation notes
<!-- progress:start -->
- **Done:** blocks 0, 1, 2, 3 (note `docs/model-v3/household-vs-legacy.md`; one defect candidate: the M2 denominator `w0` excludes the pension from year 2 under the household arm)
- **Next:** none; the author rules on the defect
- **Resume:** `git fetch origin '+refs/heads/*:refs/remotes/origin/*' && git checkout -B brief/136-household-vs-legacy origin/brief/136-household-vs-legacy`
- **State:** done, awaiting review (do not merge)
<!-- progress:end -->
