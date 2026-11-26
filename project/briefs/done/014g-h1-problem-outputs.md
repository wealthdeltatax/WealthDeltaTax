# 014: Define the hub problem outputs

- **Status:** built (merged and integrated 2026-11-17; retired)
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
- **Done:** `docs/model-v3/added/h1.md`: OH1a, OH1b, OH1c and D-H1a to D-H1c, each with a metric or fact row, inputs, an `outputs.yml` line and a claim; 12 research requests; items for the guru's merge.
- **Next:** the guru merges 014g to 016g into `metrics.md` and `outputs.yml` and renumbers the provisional metric ids MH1a to MH1c; research picks up requests 1 to 12 (1 to 3 gate OH1a).
- **Decisions:** metric ids provisional; OH1b and OH1c are today's-system quantities, reported once, not per schedule; OH1a owns the concentration definition (015g refers to it); D-H1c uses deciles of all adults (ONS convention).
- **Gotchas:** the ledger's "top 10% about half" holds on one basis only (51% against 40.7%); wealth to GDP is 5.8 to 7.5 or 3.6 by source; M3 "gains" and M4a "decile of the non-payers" each have two readings.
- **Not run:** no model code; no inputs checked against the sources.
- **State:** done on branch `brief/014-h1-problem-outputs`; not merged (open questions for the guru and author, see section 8 of `h1.md`)
<!-- progress:end -->
