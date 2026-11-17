# 016: Define the remaining added outputs

- **Status:** ready
- **Author/date:** K. Ogata with the guru, 2026-11-17
- **Depends on:** 011g (A2 passed), 012r (merged), 013g stage B (merged). Runs in parallel with the other two of 014g, 015g and 016g.
- **Read:** `docs/model-v3/metrics.md`, `docs/model-v3/outputs.yml`, `docs/model-v3/drivers.md`, `docs/model-v3/inputs.md` (rows named below), `docs/restructure/ledger.md` section 6 and the sections named in the brief. Nothing else need be opened. Ledger sections: 4 (claims 3, 5, 7, 8, 9, 12, 13) and 6.2.

## Goal
Define the supporting outputs the ledger found missing, so the manifest is complete before stage C.

## Decisions (author, 2026-11-17)
The author accepted these outputs for the manifest (the problem-section ones "for now, will refine later"). Outputs: OB1 payer count, entries, exits and fall-through refund volume by threshold; OR1 reserve solvency (share of paths where the long reserve reaches zero, minimum cover); OD1 declaration curve across alpha (extends O7); OM1 net fiscal effect after migration; OL1 the worker's non-payer saving in pounds per month (a derived view of O4b); OF1 feasibility map over the schedule family; OT1 tornado; and the synthetic cyclical stress test (kept, SWEEPS 7.5: say whether it is an output or a check). Ledger section 6.2.

## Design
One file only, `docs/model-v3/added/supporting.md`. For each output: proposed id, a `metrics.md`-style row (name, formula, denominator, unit, horizon, summary form), the inputs it needs (`inputs.md` IDs, or `MISSING` with a research request), the `outputs.yml` line to add (same format, `element:` from the ledger), and one line on what claim it lets a spoke make. Follow the one-definition-per-metric rule: no second denominator for an existing metric, and reuse existing metrics where the output is a view of one. Do not edit `metrics.md` or `outputs.yml`: the guru merges the three files after all are done (shared files, `brief-template.md` Splitting).

## Touches
New `docs/model-v3/added/supporting.md` only, plus this brief's progress block.

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
