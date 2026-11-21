# 105: Correct three stock rows to the numbers the held files support

- **Status:** ready
- **Author/date:** K. Ogata with the guru, 2026-11-21
- **Depends on:** 102r (merged)
- **Read:** `docs/research/102r-parameter-map-stocks-and-cells.md` section 4; `docs/research/data/102r/existing_row_audit.csv`; the rows I-D4a, I-D4b, I-D4h in `docs/model-v3/inputs.md`; `pipeline/build_inputs.py`; `pipeline/check_gate.py`.

## Goal
Make the register say only what a cited, checkable source supports for I-D4a, I-D4b and I-D4h, with the smallest change to values.

## Decisions (author, 2026-11-21)
"Fix to what numbers we have a citation for."

## Design
1. **I-D4h.** Low 1.77 is an assumption that both published tables contradict. Set low to 1.86 (Table 2.13, 50,185,000 over 26,991,000 = 1.8593); central and high stay 1.93 (Table 2.11). Rewrite the caveat: the two tables differ by 1,858,000 adults and the held table does not say why; remove the sentence that ties the low to I-D4b's central.
2. **I-D4a.** Values unchanged (central 5.94 reproduces; low 5.80 and high 7.5 cite Resolution Foundation pages not held, so they stay and are marked unverified in the caveat). Add to the caveat: the held NBS S.14 net worth for 2021 over the same GDP gives 5.03 (not a replacement); the pack uses GDP 2,211.48bn (ratio 6.14), 3.2% below the register's 2,284bn, not reconciled in held files.
3. **I-D4b.** Values unchanged, because the central is a fit no held table can test and nothing cited replaces it. Correct the text: low 49.3 and high 64.3 are **household** shares at 300,000 and 150,000, labelled here as adult bounds; the held household bracket for the thresholds 200,000 to 85,000 is 59.2 to 72.7; the central 54.9 lies below that bracket and implies 1.77 adults per household against 1.86 to 1.93 in I-D4h. Mark the row unverified (J). Do not recompute the central in this brief; list it as an open question for the author.
4. Regenerate `registry/inputs.json` with `pipeline/build_inputs.py`, then the generated pages and the gate hash as the usual process requires.

## Touches
`docs/model-v3/inputs.md` (three rows and the judgement-row count text if it changes), `registry/inputs.json` (generated), anything the gate regenerates. No model code.

## Inputs and early check
I-D4h low feeds the adults-per-household conversion (`model_v3/core/base.py`, IDS['adults']). Before regenerating, run the v3 suites and record whether any digest or test changes with low 1.86. Stop and report the numbers if a digest moves.

## Acceptance criteria
- I-D4h low 1.86 with the Table 2.13 citation; I-D4a and I-D4b values unchanged with corrected caveats.
- `registry/inputs.json` regenerated; gate hash consistent; suites pass or the changed digests are listed for the author.
- `git diff --stat` limited to Touches.

## Checks to run
`python -I pipeline/build_inputs.py`; `python -I pipeline/check_gate.py`; the v3 suites in the background (never piped).

## Out of scope
Recomputing the I-D4b central; the pack GDP; any other register row.

## Open questions
Whether I-D4b's central should be refit with 1.86 to 1.93 adults per household (author).

## Implementation notes
<!-- progress:start -->
- **Done:**
- **Next:**
- **Decisions:**
- **Gotchas:**
- **Resume:** (branch, last block pushed, first action)
- **Not run:**
- **State:** ready; not started
<!-- progress:end -->
