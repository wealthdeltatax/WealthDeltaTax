# 023: Research: tax rates, receipts and gains

- **Status:** ready
- **Author/date:** K. Ogata with the guru, 2026-11-17
- **Depends on:** 012r (merged), 014g to 016g (merged). Runs in parallel with 022r, 024r.
- **Read:** `docs/agents/research.md` and the files in `docs/agents/reference/research/`, `docs/model-v3/inputs.md` (row format and the rows named below), `docs/model-v3/added/h1.md` and `welfare.md`. Nothing else need be opened.

## Goal
Source the tax and capital-gains data that the lifetime-rate, tax-mix and lock-in outputs lack.

## Decisions (author, 2026-11-17)
UK only; foreign evidence allowed where no UK evidence exists, flagged with the country and a line on transferability. Every row has low, central and high, unit, how the range was set, source with date accessed, licence and access, coverage, in repo, confidence (the 012r row format). No value is chosen for the model; each low and high says how it was set.

## Design
One file only: `docs/model-v3/inputs-added/tax.md`, with row ids `I-Tn`. The guru merges the three research files into `inputs.md` (shared file). Requests this brief answers: (014g 4) a worker's income tax and employee NICs: current bands, rates, allowance and median full-time earnings (ONS ASHE); (014g 5) investment income by wealth band and the income tax on it; (014g 10) receipts by head from the held IFS sheet, one row per head, reading the same cells as the retired-tax line M1e; (014g 6) accrued gains by wealth band; (014g 7) holding period and realisation by band; (014g 8) exempt-class shares of accrued gains by band (home, ISAs, pensions, business relief); (015g) current CGT rates by asset class and band, the annual exempt amount and the no-uplift-at-death rule.

## Touches
New `docs/model-v3/inputs-added/tax.md`, research notes under `docs/research/`, and this brief's progress block. Nothing in `registry/`, `source/`, `inputs.md` or the models.

## Acceptance criteria
- Every request below has rows, or a stated reason it cannot be sourced (with the nearest evidence).
- Every row has all ten fields; judgement rows are listed together; every source has a date accessed and a licence note.
- An empty-cell check passes on the tables.
- `git diff --stat` shows only the Touches list.

## Out of scope
Choosing model values, model code, editing papers or the bibliography, other countries beyond the flagged foreign evidence.

## Open questions
The implementer asks rather than guesses.

## Implementation notes
<!-- progress:start -->
- **Done:**
- **Next:**
- **State:** ready
<!-- progress:end -->
