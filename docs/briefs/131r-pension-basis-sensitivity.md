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
- **Done:** none
- **Next:** block 0
- **Resume:** `git fetch origin '+refs/heads/*:refs/remotes/origin/*' && git checkout -B brief/131-pension-basis origin/brief/131-pension-basis`
- **State:** ready; not started
<!-- progress:end -->
