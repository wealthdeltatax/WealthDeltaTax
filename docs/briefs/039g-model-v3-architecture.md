# 039: Model v3 stage C2: architecture

- **Status:** draft (starts when 035g C1 is approved and 037c, 038c and 036r have landed)
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
- **Done:**
- **Next:**
- **Decisions:**
- **Gotchas:**
- **Resume:**
- **Not run:**
- **State:** draft; not started
<!-- progress:end -->
