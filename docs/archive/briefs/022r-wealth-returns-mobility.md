# 022: Research: wealth, returns and mobility

- **Status:** built (merged 2026-11-17; retired)
- **Author/date:** K. Ogata with the guru, 2026-11-17
- **Depends on:** 012r (merged), 014g to 016g (merged). Runs in parallel with 023r, 024r.
- **Read:** `docs/agents/research.md` and the files in `docs/agents/reference/research/`, `docs/model-v3/inputs.md` (row format and the rows named below), `docs/model-v3/added/h1.md`, `welfare.md` and `supporting.md`. Nothing else need be opened.

## Goal
Source the wealth-distribution and return inputs that the problem outputs and the envelope and feasibility outputs lack.

## Decisions (author, 2026-11-17)
UK only; foreign evidence allowed where no UK evidence exists, flagged with the country and a line on transferability. Every row has low, central and high, unit, how the range was set, source with date accessed, licence and access, coverage, in repo, confidence (the 012r row format). No value is chosen for the model; each low and high says how it was set.

## Design
One file only: `docs/model-v3/inputs-added/wealth.md`, with row ids `I-Wn`. The guru merges the three research files into `inputs.md` (shared file). Requests this brief answers: (014g 1) return by wealth rank, top 1% against the median; (014g 2) saving rate by wealth band and mobility in and out of the top 1%; (014g 3) top 1% and 10% shares on the Round 8 per-adult basis with the pension-basis note; (014g 9) the UK top-1% and top-10% share series from WID (held under `model_v2/wid_out/`); (015g) persistence of return differences by wealth percentile; (016g M-1) share of adults and of wealth above each threshold on a grid from about 150,000 pounds to 10 million; (016g M-2) how often adults cross a threshold in a year; (016g M-3) the distribution of declared against true value, or the nearest bunching and understatement evidence.

## Touches
New `docs/model-v3/inputs-added/wealth.md`, research notes under `docs/research/`, and this brief's progress block. Nothing in `registry/`, `source/`, `inputs.md` or the models.

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
- **Done:** `docs/model-v3/inputs-added/wealth.md`: 45 rows (I-W1 to I-W9), 12 cells each, no empty cell; derivations in `docs/research/022r-derivations.md`.
- **Next:** the guru merges the three research files into `inputs.md`.
- **State:** done; brief 022 merged, ready to retire
<!-- progress:end -->

### Change report
```
Change report
- Task: brief 022r, wealth, returns and mobility
- Files changed: docs/model-v3/inputs-added/wealth.md (new, 45 rows, sources SW1 to SW10, gaps, request map); docs/research/022r-derivations.md (new); this brief
- What is different now: the register has the wealth-distribution and return inputs for 014g 1 to 3 and 9, 015g persistence and 016g M-1 to M-3, as a separate file. Examples: P90-P10 return gap 10 to 18 points (Norway); UK top-decile two-year persistence 80%; Round 8 decile-10 share 40.7% (40.1% without pensions); share of households above £1m 14.1%, above £2m 2.9% to 3.5%; WID UK top 1% 21.3% in 2024; Colombian elasticity of reported wealth 0.6 to 2.0.
- New or changed interfaces: none
- Acceptance criteria: every request has rows or a stated reason: met (partly sourced, with the nearest evidence stated, for 014g 1, 2, 3, 015g persistence, M-2 and M-3; fully for 014g 9 and M-1 on a household basis); all fields on every row and judgement rows listed together (29): met; sources have a date accessed and a licence note: met; empty-cell check: passed (45 rows, 12 cells); git diff --stat inside Touches: met.
- Deviations from the brief: none
- Risks / follow-ups: no UK return-by-rank, UK saving-by-wealth-band or UK valuation-understatement evidence was found; the grid above £1m and the Round 8 top-1% share are fitted tails (judgement rows); the extraction tool returned only the first 100,000 characters of some long PDFs, so Fagereng Figure 5 and the intergenerational section were not read; the Swiss paper body was not returned. A per-adult Round 8 grid needs the microdata (not held).
- Verification: empty-cell parse; derivations rerun in python3 -I; figures checked against the fetched text. Not run: no model code.
- Overview sections likely needing an update: none
- Commit / branch: brief/022-wealth, merged to main
```
