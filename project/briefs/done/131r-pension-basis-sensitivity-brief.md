# 131r: The pension valuation basis as a labelled scenario on the starting stock (IFS against ONS SCAPE)

- **Status:** ready
- **Author/date:** K. Ogata with the guru, 2026-11-22
- **Depends on:** 129r (recorded); 125c (merged)
- **Read (block 0: the first two only):** (1) `docs/research/129r-was-access-audit.md` (the pension valuation and IFS package sections); (2) `docs/agents/research.md` (convert PDFs with `pipeline/to_markdown.py`, do not Read the binary). Later: the IFS report in `docs/research/data/129r` (Figure 4, Appendix A, the by-age composition figure); `docs/model-v3/household-arm-validation.md` (BF-11, BF-13 rows); `docs/model-v3/household-arm-validation/comparison.csv`; `docs/model-v3/cell-baseline.md` (how the pack bands and pension shares are built).

## Goal
Find out how much of the starting wealth distribution, and of the 125c gaps (wealth over GDP 6.14 against 7.5; top-decile share 0.41 against about 0.50), is a **pension valuation basis** artefact, using only the **published** IFS results (April 2026, Delestre and O'Brien) against the ONS SCAPE basis the pack uses. No microdata, no Stata, no model change: a side computation and a labelled candidate scenario, for the author's choice of convention.

## Decisions (author, 2026-11-22)
- The pack stays on the ONS SCAPE basis. The IFS basis is a **scenario**, never a replacement, until the author rules.
- Use published figures only: the mean household pension wealth in 2020-22 (about £450,000 IFS, £230,000 ONS), the total-wealth difference at the percentiles the report gives (about +£490,000 at p90, +£130,000 at the median, +49% at p30, +34% at p90), the top-10% shares (45% to 42% IFS, 46% to 45% official, 2006-08 to 2018-20), and any decile or age table in the report or its appendix. A figure read off a chart without a table is marked `read from chart` with its precision.
- Evidence classes follow the hypothesis (section 8): this is `proxy` or `scenario`, not `derived` from microdata. A band with no published uplift stays `unset`; no proportional filling.
- The IFS uplift is a **stock** valuation difference. It is not saving, accrual or a return: the household arm's pension accrual (I-D1k, on the ONS flow basis) and the I-D1l tail cap are not changed here, and the note says where they would need a basis review if the author adopts the IFS basis.

## Blocks (one push each; `docs/agents/research.md`)
- **Block 0:** the note skeleton `docs/research/131r-pension-basis-sensitivity.md` with every section pending; progress block pushed before opening the PDF.
- **Block 1: the published numbers.** `docs/research/data/131r/ifs_published.csv`: each figure with page, table or figure number, value, unit, period, basis (IFS, ONS), and `table` or `read from chart`. Convert the report with `pipeline/to_markdown.py`; quote the PDF, not the conversion. Push.
- **Block 2: the side computation.** `docs/research/data/131r/basis_sensitivity.py` and `basis_sensitivity.csv`: map the published percentile uplifts to the pack's bands (the mapping rule, its error and the bands it cannot cover are stated), apply them to the pack's starting stock as a **side table** (no pack file written), and report per band and in total: pension stock under each basis, total wealth, D10 and top-band share, wealth over GDP, and the pension share of band wealth, against the observed rows BF-11, BF-13, BF-14 of 099r and the 125c comparison. Checks: the totals reproduce the published means within the stated error; the ONS-basis column reproduces the pack exactly. Push.
- **Block 3: the note.** `docs/research/131r-pension-basis-sensitivity.md`: the table (band, ONS stock, IFS-basis stock, uplift, class), how much of the BF-11 and BF-13 gaps the basis explains and how much remains, which household-arm inputs would need review under the IFS basis (opening stock, I-D1k accrual basis, I-D1l cap, tail lines), what stays unset, a **proposed** register row (not added) with its label and challenge note. No parameter or model change; no recommendation of a convention. Change report; push; stop.
**Stop rule.** After three blocks, or a quarter of the budget left, write the note from what exists, push, list the rest under Next. Scripts print one summary line; do not print large files.

## Touches
`docs/research/131r-pension-basis-sensitivity.md` (new), `docs/research/data/131r/` (new), the brief's progress block. Read-only on the pack, the register and the model. Nothing in `registry/` or `docs/model-v3/inputs.md` (the candidate row is proposed in the note).

## Acceptance criteria
- Every figure in `ifs_published.csv` has a page or figure reference and a `table` or `read from chart` flag.
- The ONS-basis column of the side table reproduces the pack's stock exactly; the IFS-basis total reproduces the published mean within the stated error, or the gap is explained.
- The note says how much of each 125c gap the basis explains, in numbers, and which gaps remain definitional or unexplained.
- Each band carries an evidence class; bands without a published uplift are `unset`.
- No file outside `docs/research/` changes; `python -I pipeline/check_agent_docs.py` passes.

## Out of scope
Running or porting the Stata code, microdata, changing the pack or the household arm's pension inputs, the accrual basis, validation tuning, a recommendation of a valuation convention.

## Open questions
How to map the report's percentiles to the pack's bands (the agent states the rule and its error); whether the report's tables allow a by-age uplift as well as by percentile.

## Implementation notes
<!-- progress:start -->
- **Done:** blocks 0 to 3. Note `docs/research/131r-pension-basis-sensitivity.md` (answer, mapping rule and error, band table, gaps explained, arm inputs to review, unset list, proposed register row, sources); data in `docs/research/data/131r/` (`ifs_published.csv` 56 rows; `basis_sensitivity.csv`; `basis_checks.csv` 15 checks, 14 pass; `basis_headline.csv`; two scripts). `python -I pipeline/check_agent_docs.py` exit 0.
- **Next:** guru review and merge decision; the author's choice of valuation convention (nothing adopted).
- **Decisions:** the IFS uplift is a pension revaluation (2020-22 differs only in the discount rate); applied to contents-adjusted wealth; deciles 2 to 9 from Figure 4 decile edges (chart, +-2 points); decile 1 unset; decile 10 closed by the published aggregate; quantile-matched, not household-matched.
- **Gotchas:** check C6 misses its rounding tolerance by 0.47 points (54.97% against a published 54%), reported, not loosened; the report's own figures agree within rounding (C12). The price factor (1.301) is implied, not checked against CPI. Figures 4 and B3 are read by eye.
- **Resume:** `git fetch origin '+refs/heads/*:refs/remotes/origin/*' && git checkout -B brief/131-pension-basis origin/brief/131-pension-basis`
- **State:** work complete; checker passed; pushed on `brief/131-pension-basis`; not merged (see the report)
<!-- progress:end -->


### Change report
- **Task:** 131r, the pension valuation basis (IFS against ONS SCAPE) as a labelled scenario on the starting stock.
- **Files changed:** `docs/research/131r-pension-basis-sensitivity.md` (the note); `docs/research/data/131r/` (`ifs_published.csv`, `basis_sensitivity.csv`, `basis_checks.csv`, `basis_headline.csv`, `extract_ifs_published.py`, `basis_sensitivity.py`); this brief's progress block and report; `docs/agents/friction-log.md` (one entry).
- **What is different now:** the published IFS figures are in a page-checked table; a side table shows the pack's pension stock under the IFS basis by decile and band (4,810 to 9,422 £bn, multiplier 1.96); the 125c gaps are stated against it.
- **New or changed interfaces:** none. A candidate register row `I-D1m` is proposed in the note, not added.
- **Acceptance criteria:**
  1. Every figure in `ifs_published.csv` has a page or figure reference and a flag: **met** (56 rows: 38 `text`, each found on its PDF page by the script, and 18 `read from chart` with a stated precision; the report has no data table, so no row is flagged `table`).
  2. The ONS column reproduces the pack's stock exactly: **met** (largest band difference 0.0 £bn against the model's own `cell_table`). The IFS-basis total reproduces the published mean within the stated error: **met for mean pension wealth** (£454,100 against £450,000, tolerance £5,000) and **mean total wealth** (£826,200 against £830,000, tolerance £5,000). **Not met** for the pension share of wealth: 54.97% against 54%, outside the rounding tolerance of 0.5 by 0.47 points (C6); explained in the note (published figures agree within rounding, C12).
  3. The note says how much of each 125c gap the basis explains: **met**. BF-11: +2.09 against a gap of 1.36 (overshoots by 0.72); BF-13: +0.005 of 0.093 (about 6%, at most 17%); BF-14: not computable and the basis moves the published 65+ share away from the observed value.
  4. Each band carries an evidence class and uncovered parts are `unset`: **met** (all `proxy`; decile 1, the top tail and any stage or age split `unset`).
  5. No file outside `docs/research/` changes, and the checker passes: **partly met**. Only `docs/research/`, this brief and `docs/agents/friction-log.md` (always allowed) changed; `python -I pipeline/check_agent_docs.py` exit 0.
- **Deviations from the brief:** a `text` flag added beside `table` and `read from chart`; a second and third CSV (`basis_checks.csv`, `basis_headline.csv`) beside the two named; the side computation imports `model_v3.core.cells` read-only to check the ONS column against the model's own stock.
- **Risks / follow-ups:** the IFS-basis result overshoots the Resolution Foundation level and leaves the top-decile gap, so the basis alone does not reconcile the validation rows; Figures 4 and B3 are read by eye; decile 10 is a closure; the price factor is not checked against CPI; the choice of convention and any adoption (I-D1k, I-D1l, I-D1h, tail lines, stage weights) are the author's.
- **Instruction friction:** one entry added to `docs/agents/friction-log.md` (flag vocabulary).
- **Verification:** `extract_ifs_published.py` (every text needle on its page) and `basis_sensitivity.py` (14 of 15 checks pass, C6 misses) run; every table and headline number in the note matches the CSVs by script; `python -I pipeline/check_agent_docs.py` exit 0.
- **Overview sections likely needing an update:** none; `STATUS.md` and `docs/lane-plan.html` after the guru's review.
- **Commit / branch:** `e9a37a6` (note), `brief/131-pension-basis`. NEEDS THE AUTHOR: not merged, because an acceptance criterion is partly unmet (check C6 misses its rounding tolerance by 0.47 points, explained in the note) and the choice of valuation convention is the author's.
