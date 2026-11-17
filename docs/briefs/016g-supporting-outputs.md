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
- **Done:** `docs/model-v3/added/supporting.md` written: OB1, OR1, OD1, OM1, OL1, OF1, OT1 and the stress test (decided: a check, CK1), each with a metric row, inputs, the `outputs.yml` line and the claim. Five MISSING inputs (M-1 to M-5) with research requests.
- **Next:** the author reads the three choices at the end of the file; the guru merges this file with 014g and 015g into `metrics.md` and `outputs.yml`, then updates `STATUS.md` and `docs/lane-plan.html`.
- **State:** built, branch pushed, NEEDS THE AUTHOR (not merged)

Change report
- Task: 016g, define the remaining added outputs
- Files changed: `docs/model-v3/added/supporting.md` (new, the eight definitions); this brief's progress block
- What is different now: the manifest additions for the supporting outputs are specified and ready to merge; none are in `metrics.md` or `outputs.yml` yet
- New or changed interfaces: none. Proposed new metric ids B1a to B1d, P7a, P7b, M7c to M7e, M9, M4c, F1, T1 (all free); output ids OB1, OR1, OD1, OM1, OL1, OF1, OT1, CK1
- Acceptance criteria: (1) every listed output has all five items: met, eight of eight sections checked by pattern (metric row, inputs, `outputs.yml` line, claim, and the proposed id in the heading); (2) every input is an `inputs.md` ID or MISSING: met, every cited ID found in `inputs.md` (none absent), five MISSING flagged; (3) `git diff --stat` shows only the Touches list: see Verification
- Deviations from the brief: none
- Risks / follow-ups: (a) the refund event in B1d and the modal declaration in M7e rest on the ledger's pointers (CLOSE §4.3, §7.2; VAL §7), which I did not open; the code lane confirms them. (b) SWEEPS 7.5 uses mu of 7%, against I-D1a central 4.42% real, and its canonical amplitude gives about 5.7% volatility against I-D1b's 8.2%; the stress-test fixture needs the author's choice. (c) I-D6 gives incidence for the top decile and bottom five only, which already limits O4a by decile. (d) Three choices left to the author (end of the file)
- Verification: cited input IDs checked against `inputs.md` by script (none missing); section completeness checked by script; not run: any model code (none exists for these); no paper was read beyond SWEEPS 7.5
- Overview sections likely needing an update: none until the merge; then `docs/model-v3/` in the directory map and STATUS
- Commit / branch: branch `brief/016-supporting-outputs`; not merged to `main`, because the brief asks the guru to merge the three files after 014g and 015g, and the author's choices above are open
<!-- progress:end -->
