# 042: Research: bridge the return data from 2019 to 2025

- **Status:** ready
- **Author/date:** K. Ogata with the guru, 2026-11-18
- **Depends on:** 036r merged (done)
- **Read:** `docs/model-v3/returns-method.md` section 7 (options table and the six missing years); `docs/model-v3/inputs.md` row I-D1e; `docs/agents/research.md` and `docs/agents/reference/research/`.

## Goal
Find out whether a licensed, open series can extend the UK wealth return past 2019, so the generator's central parameters and the level 2 band can be checked against 2020 to 2025 (the crash and rebound, the 2022 inflation and gilt shock, the 2022 to 2024 house price fall) without a splice by guess.

## Decisions (author, 2026-11-18)
- No splice is made in 036r and none is made here; this brief only reports what is available and what it would change.
- JST Release 6 (to 2019) stays the source; its licence is unconfirmed and this brief settles it if it can.
- UK only.

## Design
1. Licence: read the JST data terms (macrohistory.net) and the NBER page in full and state what citation and redistribution the repo may do with `Rates Data/JSTdatasetR6.xlsx` and `model_v2/jst_r6.json`; whether a later release exists.
2. Candidate series for 2020 to 2025: UK house prices (ONS UK HPI, OGL v3.0), CPI (ONS), equity total return (FTSE All-Share or a licence-free proxy), gilt returns (Bank of England), rents. For each: coverage start, frequency, licence, the exact table or file, access date. A series with no licence is listed, not used.
3. A table of annual real total returns for 2020 to 2025 computed only from series whose licence allows it, with the method written out (portfolio weights from JST's own composition of wealth), each year marked as estimated; the effect of adding the six years on the arithmetic mean, SD, lag-1 correlation and the 80% band of I-D1a.
4. State plainly what stays uncovered.

## Touches
`docs/model-v3/returns-gap.md` (new), `docs/model-v3/returns/` (new files only), this brief's progress block. Nothing in `inputs.md`, `source/`, `pipeline/`, `registry/`.

## Acceptance criteria
- Every series has a licence statement from a page read, with its URL and date accessed.
- The 2020 to 2025 table cites each input series and marks estimates.
- The effect on mean, SD, lag-1 and the band is shown, or the reason it cannot be computed is stated.
- `git diff --stat` shows only the Touches list.

## Checks to run
Recompute one year by hand from the cited series; script runs with `python -I`.

## Out of scope
Editing `inputs.md` or the generator, splicing into the JST series, any model run.

## Open questions
Ask rather than guess.

## Implementation notes
<!-- progress:start -->
- **Done:**
- **Next:**
- **Decisions:**
- **Gotchas:**
- **Resume:**
- **Not run:**
- **State:**
<!-- progress:end -->
