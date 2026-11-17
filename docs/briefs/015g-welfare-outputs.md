# 015: Define the welfare outputs, combined with v3

- **Status:** ready
- **Author/date:** K. Ogata with the guru, 2026-11-17
- **Depends on:** 011g (A2 passed), 012r (merged), 013g stage B (merged). Runs in parallel with the other two of 014g, 015g and 016g.
- **Read:** `docs/model-v3/metrics.md`, `docs/model-v3/outputs.yml`, `docs/model-v3/drivers.md`, `docs/model-v3/inputs.md` (rows named below), `docs/restructure/ledger.md` section 6 and the sections named in the brief. Nothing else need be opened. Ledger sections: 4 (claims 10, 19) and 6.2.

## Goal
Define OW1 to OW3 (certainty-equivalent welfare, CGT lock-in cost, concentration and contribution envelope) so that they are produced by the same v3 run as the headlines and not by a separate model.

## Decisions (author, 2026-11-17)
The author accepted these outputs for the manifest (the problem-section ones "for now, will refine later"). Outputs: OW1 certainty-equivalent welfare of the tax systems at revenue equivalence (FAL H4, WFR section 3), OW2 CGT lock-in cost (WFR 4.2), OW3 contribution envelope binding and concentration (WFR 4.3). Ledger section 4 claims 10 and 19, section 6.2 (S6). State what each needs from the v3 state (heterogeneous returns, payer paths) and flag any that cannot be produced without a second model.

## Design
One file only, `docs/model-v3/added/welfare.md`. For each output: proposed id, a `metrics.md`-style row (name, formula, denominator, unit, horizon, summary form), the inputs it needs (`inputs.md` IDs, or `MISSING` with a research request), the `outputs.yml` line to add (same format, `element:` from the ledger), and one line on what claim it lets a spoke make. Follow the one-definition-per-metric rule: no second denominator for an existing metric, and reuse existing metrics where the output is a view of one. Do not edit `metrics.md` or `outputs.yml`: the guru merges the three files after all are done (shared files, `brief-template.md` Splitting).

## Touches
New `docs/model-v3/added/welfare.md` only, plus this brief's progress block.

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
- **Done:** `docs/model-v3/added/welfare.md` written: OW1, OW2, OW3 with id, metric row, inputs (IDs or MISSING with research requests), outputs.yml line and spoke claim; v3 state needs and second-model flags (section 5).
- **Next:** author answers the four questions in section 6 of welfare.md; guru merges into metrics.md, outputs.yml, inputs.md after 014g and 016g.
- **State:** needs the author
<!-- progress:end -->
