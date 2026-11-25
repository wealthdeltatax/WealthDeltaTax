# 024: Research: households, leavers and welfare parameters

- **Status:** done, merged, retired 2026-11-17 (014g 11 met by the follow-up that read the ONS workbook; 014g 12 not met, see `docs/decisions.md`)
- **Author/date:** K. Ogata with the guru, 2026-11-17
- **Depends on:** 012r (merged), 014g to 016g (merged). Runs in parallel with 022r, 023r.
- **Read:** `docs/agents/research.md` and the files in `docs/agents/reference/research/`, `docs/model-v3/inputs.md` (row format and the rows named below), `docs/model-v3/added/h1.md`, `welfare.md` and `supporting.md`. Nothing else need be opened.

## Goal
Source the household, migration and welfare-parameter inputs that the non-payer, migration and welfare outputs lack.

## Decisions (author, 2026-11-17)
UK only; foreign evidence allowed where no UK evidence exists, flagged with the country and a line on transferability. Every row has low, central and high, unit, how the range was set, source with date accessed, licence and access, coverage, in repo, confidence (the 012r row format). No value is chosen for the model; each low and high says how it was set.

## Design
One file only: `docs/model-v3/inputs-added/hh.md`, with row ids `I-Hn`. The guru merges the three research files into `inputs.md` (shared file). Requests this brief answers: (014g 11) total tax paid by income decile, all taxes, from the ONS Effects of Taxes and Benefits FYE 2024 decile workbook (it could not be downloaded in 012r; the author may attach it); (014g 12) the non-payer share in each income decile; (016g M-5) mean household income by income decile and published earnings for the median worker and a care worker; (016g M-4) income tax, NICs and VAT paid per pound of wealth by the people most likely to leave, and their consumption share; (015g) relative risk aversion range used in published UK or comparable welfare work, with a defensible low, central and high; (015g) a dated pair of UK real return series for an asset a payer holds and the one they would switch to, with the cross-correlation; (015g) UK consumption to wealth ratios by wealth band (required: the author keeps the consumption tax as a comparator, 2026-11-17, because it is the WDT's main intellectual competitor).

## Touches
New `docs/model-v3/inputs-added/hh.md`, research notes under `docs/research/`, and this brief's progress block. Nothing in `registry/`, `source/`, `inputs.md` or the models.

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
- **Done:** `docs/model-v3/inputs-added/hh.md` (46 rows I-H1a to I-H7e, 9 judgement rows, sources SH1 to SH10), `docs/research/024r-derivations.md`. Empty-cell check passed.
- **Next:** author attaches the ONS ETB FYE 2024 decile workbook (and ad hoc 12451) to fill I-H1, I-H2, I-H3 by decile; guru merges the three added files.
- **Decisions:** nearest evidence used where the workbook is missing (FYE 2023 quintiles, secondary); UK real returns computed from the held JST data (to 2020).
- **Gotchas:** fetch-tool summary mis-divided the ONS spending ratios (recomputed); no UK data on leavers (proxy: additional-rate taxpayers).
- **State:** done, merged
<!-- progress:end -->

### Change report
- **Task:** 024r, households, leavers and welfare parameters.
- **Files changed:** new `docs/model-v3/inputs-added/hh.md`, new `docs/research/024r-derivations.md`, this brief.
- **What is different now:** 46 rows answer 015g (risk aversion, returns, consumption to wealth), 016g M-4 and M-5 in part; gaps listed in the file.
- **Acceptance:** every request has rows or a stated reason: met (014g 11, 12 by stated reason and nearest evidence); all fields present: met; judgement rows listed: met; sources dated with licence: met; empty-cell check: met; diff within Touches: met.
- **Deviations:** none. **Risks:** tax rows are quintile and FYE 2023 from a secondary table; leaver rows are proxies.
- **Verification:** empty-cell script; return statistics recomputed from the held JST file.

