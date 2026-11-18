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
- **Done:** `docs/model-v3/returns-gap.md` and `returns/gap.py` (+ `gap_results.json`). JST R6 licence settled from the R6 documentation: CC BY-NC-SA 4.0 (non-commercial, share-alike, citation of JST 2017 and JKKST 2019); no later release found. Series table with licence statements and URLs (ONS CPI and UK HPI: OGL v3.0, used; FTSE: LSEG licence needed, not used; Bank of England: OGL but no values retrievable, not used; rents: OGL but no annual values read). 2020 wealth return estimated from JST's own 2020 series: -0.44% real. 2021 to 2025 housing-only proxy: 10.14, 2.78, -5.92, 4.17, 1.28 (estimates, not wealth returns). Effect on I-D1a: mean 4.74 to 4.70 (2020), 4.61 (proxy), 4.49 or 4.37 (stress); band 3.41 to 6.07 becomes 3.38 to 6.02 / 3.34 to 5.88; SD 8.1 to 8.3; lag-1 0.29 to 0.32. S0 reproduces the register; 2022 and 2023 hand checks agree.
- **Next:** author supplies a licensed equity and gilt series (or accepts 2019 as the end); guru decides on a JST licence notice and whether I-D1e should be reworded.
- **Decisions:** no splice; the housing proxy is shown only for shape (it is December on December, JST's house price is not: 5.7 points apart in 2020); rent return held at JST 2020 (assumption); stress shifts of 3 and 6 points are labelled assumptions.
- **Gotchas:** macrohistory.net is not on the fetch allowlist, so the licence came from the R6 documentation copy (first 100,000 of 570,066 characters) and the NBER page; re-read the terms page when reachable. HPI values are the first-published December changes, later revised. No LICENSE file in the repo.
- **Resume:** n/a
- **Not run:** any model run; equity and gilt returns; HPI download tables.
- **State:** done, merged.
<<!-- progress:end -->
