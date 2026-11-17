# 014: Define the hub problem outputs

- **Status:** ready
- **Author/date:** K. Ogata with the guru, 2026-11-17
- **Depends on:** 011g (A2 passed), 012r (merged), 013g stage B (merged). Runs in parallel with the other two of 014g, 015g and 016g.
- **Read:** `docs/model-v3/metrics.md`, `docs/model-v3/outputs.yml`, `docs/model-v3/drivers.md`, `docs/model-v3/inputs.md` (rows named below), `docs/restructure/ledger.md` section 6 and the sections named in the brief. Nothing else need be opened. Ledger sections: 6.1 and 4 (claim 21).

## Goal
Give hub section H1 (the problem) evidence: define the three problem outputs and three data facts so the hub can state the problem without the tax.

## Decisions (author, 2026-11-17)
The author accepted these outputs for the manifest (the problem-section ones "for now, will refine later"). Outputs: OH1a (concentration path with and without the WDT, top 1% share at years 10, 25 and 50), OH1b (rate on gains for large holders today against a median worker's income tax and NICs), OH1c (share of lifetime gains that escape tax today, by wealth band), and data facts D-H1a (wealth shares, wealth to GDP), D-H1b (tax mix), D-H1c (non-payers' tax bill by decile). Ledger section 6.1.

## Design
One file only, `docs/model-v3/added/h1.md`. For each output: proposed id, a `metrics.md`-style row (name, formula, denominator, unit, horizon, summary form), the inputs it needs (`inputs.md` IDs, or `MISSING` with a research request), the `outputs.yml` line to add (same format, `element:` from the ledger), and one line on what claim it lets a spoke make. Follow the one-definition-per-metric rule: no second denominator for an existing metric, and reuse existing metrics where the output is a view of one. Do not edit `metrics.md` or `outputs.yml`: the guru merges the three files after all are done (shared files, `brief-template.md` Splitting).

## Touches
New `docs/model-v3/added/h1.md` only, plus this brief's progress block.

## Acceptance criteria
- Every listed output has all five items above.
- Every input is an `inputs.md` ID or flagged `MISSING`.
- `git diff --stat` shows only the Touches list.

## Out of scope
Model code, edits to `metrics.md`, `outputs.yml`, `inputs.md` or papers, choosing values.

## Open questions
The implementer asks rather than guesses.

## Implementation notes
<!-- progress:start -->
- **Done:**
- **Next:**
- **State:** ready
<!-- progress:end -->
