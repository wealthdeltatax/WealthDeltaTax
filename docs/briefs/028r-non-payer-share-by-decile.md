# 028: Research: non-payer share by income decile

- **Status:** ready
- **Author/date:** K. Ogata with the guru, 2026-11-17
- **Depends on:** 024r (merged). Runs in parallel with 027r.
- **Read:** `docs/agents/research.md` and the files in `docs/agents/reference/research/`; `docs/model-v3/inputs.md` rows I-H2a, I-H2b, I-D9a to I-D9d and the 014g 12 line; `docs/model-v3/metrics.md` M4a and M4b; `docs/model-v3/inputs-added/hh.md` (row format).

## Goal
Fill the one household input still missing: the share of adults who would pay nothing under WDT (below the threshold W_min), by income decile of all adults. It is needed for the non-payer savings headline (O4a, by income decile).

## Decisions (author, 2026-11-17)
UK only. "Non-payer" means below W_min (the h1.md reading): deciles of all adults, then the non-payers inside each. The ETB workbook cannot answer this (it has no wealth variable). Row format as in 012r (twelve cells, low, central, high, how the range was set).

## Design
1. Find the joint distribution of income decile and wealth that supports the share below W_min = £150,000 (I-D4b). Routes: ONS WAS Round 8 tables (the Table 2.6 inversion behind I-D9a to I-D9d is held), any WAS table with household wealth by income quintile or decile, ONS ad hoc 12451 (FYE 2019, file `householdsnotax.xlsx`) if it can be found, IFS or Resolution Foundation work on wealth by income.
2. Produce rows I-H2a1 to I-H2a10 (or quintiles if deciles do not exist, labelled) with low, central, high. If only quintiles exist, say how deciles would be interpolated and do not interpolate.
3. If no source gives the joint distribution, say so, give the nearest proxy (for example wealth by age and tenure against income), and mark confidence low. Do not invent a distribution.
4. Say where the answer would change if W_min moved to £100,000 and £200,000 (rows or a note), if the source allows.

## Touches
`docs/model-v3/inputs-added/hh2.md` (new), this brief's progress block. Nothing in `inputs.md` (the guru merges), `source/`, `pipeline/`, `model_v1/`, `model_v2/`.

## Acceptance criteria
- Each row has twelve cells and a unique id; sources have date accessed and licence.
- The joint-distribution route is stated, or the gap is stated with the nearest proxy.
- No row is filled with a figure that has no source.
- `git diff --stat` shows only the Touches list.

## Checks to run
Row count and cell count by script (`python -I`); one source figure re-read from its table.

## Out of scope
Merging into `inputs.md`, choosing the value for the model, wealth-tax thresholds other than W_min, the stock-wealth floor.

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
