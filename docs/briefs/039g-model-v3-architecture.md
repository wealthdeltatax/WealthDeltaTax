# 039: Model v3 stage C2: architecture

- **Status:** written, waiting for the author (C1 approved 2026-11-18; 037c, 038c and 036r merged)
- **Author/date:** K. Ogata with the guru, 2026-11-17
- **Depends on:** 035g (C1 approved), 037c, 038c, 036r (return module only)
- **Read:** `docs/briefs/011g-model-v3-design.md` (stage C check); `docs/model-v3/stage-c-decisions.md` (035g); `docs/model-v3/port-inventory.md` (037c); `docs/model-v3/country-pack.md` (038c); `docs/model-v3/returns-method.md` (036r); `docs/model-audit/synthesis.md` section 4; `docs/restructure/order.md` G1 and G2; `docs/briefs/030c-data-interface.md`.

## Goal
Write `docs/model-v3/architecture.md` so that stage D can write acceptance criteria and build briefs with no open design choice.

## Design
Guru only; one session; stops for the author. The document:
1. Fixes where v3 lives (`model_v3/`), the output at `model_v3/OUTPUTS/outputs.json` in the shape 030c validates, and where it reads `jst_r6.json` (through the country pack).
2. Lists the modules in dependence order: country data pack loader, returns generator, wealth and payer base, rate schedule and refund mechanics, revenue lines and fund, burden and savings, range runner, output writer. Each with inputs, outputs, ids it produces, and the C1 decision it implements.
3. Sets a line budget for the core and for the output layer (R9: output layer smaller than core), using the line totals in `port-inventory.md`.
4. Names what is ported by exception with the element that needs it, taken from the inventory's verdicts.
5. Lists the tests each module needs before the next is built (R7), including the identity check against v2's 7.34% (C1 item 3).
6. States the import rules (R4), the no-side-effects rule (R8), the run script and smoke test (R5), and the fate of `model_v1/` and `model_v2/` (009c stays parked; say when each folder can go).
7. Cuts the model into build stages, each a unit that one agent finishes in a session (the input for stage D's build briefs).

## Touches
`docs/model-v3/architecture.md` (new), `STATUS.md`, `docs/lane-plan.html`, this brief's progress block. Nothing else.

## Acceptance criteria
- The seven items above exist; R4, R5, R7, R8, R9 and R11 are each named with a place.
- Every module has a line budget and a test list; every ported item names an element.
- The build stages in item 7 have no shared files, or say which are sequential.
- `git diff --stat` shows only the Touches list; the author has approved C1 before this starts.

## Checks to run
A grep that each of R4, R5, R7, R8, R9 and R11 is named in `architecture.md`; module line budgets sum to the stated totals.

## Out of scope
Model code, acceptance criteria (040g), build briefs (040g), editing the register or manifest.

## Open questions
Settled in 035g C1; anything C1 left open stops this brief.

## Implementation notes
<!-- progress:start -->
- **Done:** `docs/model-v3/architecture.md`: layout, eight core files plus runner and output layer, budgets (core plus runner 3,900, output layer 700, total code 4,770, tests 2,930), port table, tests per module, identity check I1 to I3, 13 build stages, seven manifest amendments.
- **Next:** the author approves or changes section 9 (nine defaults) and section 8.1; then 040g D1 (`acceptance.md`); D2 build briefs only after D1 is approved.
- **Decisions:** kernel ported whole with all routes; seed 20261118; N1 10,000, level 2 200 x 1,000; horizons as year windows with an unfilled-path rule; levers in `model_v3/levers.json`; identity bounds 0.02 and 6.34; `WorkerPool` only if the run exceeds 60 minutes.
- **Gotchas:** the budgets other than the kernel are estimates, not measurements. `rates_core` and `valgen_core` were not in the port inventory, so `revenue.py` and `base.py` are written from `metrics.md` with v2's line ranges as reference. The seven `by` vocabularies are proposals.
- **Resume:** read `docs/model-v3/architecture.md` sections 7 to 9.
- **Not run:** no code; run time not measured; the I1 and I2 bounds are not measured.
- **State:** pushed, NEEDS THE AUTHOR (not merged).
<!-- progress:end -->

### Change report
```
Change report
- Task: brief 039g, model v3 stage C2, architecture
- Files changed:
  - docs/model-v3/architecture.md: new
  - STATUS.md: agent table and recently done
  - docs/lane-plan.html: 039g marked in review
  - docs/briefs/039g-model-v3-architecture.md: progress block, status and this report
- What is different now: stage D can write acceptance criteria and build briefs against a fixed layout, module list, budgets, test list and stage table. Nothing in model_v1/, model_v2/, source/, pipeline/ or registry/ changed.
- Acceptance criteria:
  1. The seven items exist: MET (sections 1, 2, 6.1, 4, 6.2, 5 with 6.5 and 8.2, 7).
  2. R4, R5, R7, R8, R9, R11 each named with a place: MET (R4 5.1, R5 3.1 and 5.5 and 6.4, R7 5.5 and 6.2, R8 5.2, R9 5.4 and 6.1, R11 5.3; grep counts 6, 7, 5, 2, 4, 3).
  3. Every module has a line budget and a test list; every ported item names an element: MET (6.1, 6.2; section 4 gives output ids).
  4. Build stages have no shared files or say which are sequential: MET (section 7; the chain is stated).
  5. Diff limited to Touches: MET.
- Checks: budget table parsed by script: core 3,240, runner 660, core plus runner 3,900, output layer 700, interface and run 170, total 4,770; tests 2,930; all equal the stated totals. Output-id table covers outputs.yml exactly (39 outputs and CK1, 40 ids, no duplicate).
- Deviations: none. Not measured: run time, the identity bounds, any budget except the kernel.
- Questions for the author: section 9 (nine defaults) and section 8.1 (seven manifest amendments).
- Commit / branch: brief/039-model-v3-architecture. NEEDS THE AUTHOR (not merged): the brief stops for the author. 040g is held.
```
