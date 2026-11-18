# 040: Model v3 stage D: acceptance plan and build briefs

- **Status:** draft (starts when 039g is approved)
- **Author/date:** K. Ogata with the guru, 2026-11-17
- **Depends on:** 039g
- **Read:** `docs/briefs/011g-model-v3-design.md` (stage D check); `docs/model-v3/architecture.md`; `docs/model-audit/synthesis.md` section 4 (R1 to R11); `docs/restructure/order.md` G1 (the acceptance run it reads); `docs/agents/brief-template.md`.

## Goal
Write `docs/model-v3/acceptance.md` and the build briefs, one per architecture build stage, so each is small, staged, measurable and runs on its own agent.

## Design
Two stages, guru only, each ending in a stop.
- **D1: acceptance plan.** Checkpoint: `docs/model-v3/acceptance.md`. Check: every build stage has a stop and a measurable criterion (a test, a bound, a reproducible number); the smoke test, the seed and sample-size policy, the convergence test and the run script are specified; every requirement R1 to R11 maps to a criterion; the single command that G1 runs as the acceptance run is named and exits 0 only when all stages pass. `acceptance.md` holds exactly one line of the form `Acceptance command: \`...\`` (the gate checker, 033c, reads it; `order.md` guru rulings of 2026-11-18).
- **D2: build briefs.** Checkpoint: one brief per build stage under `docs/briefs/`, each with its own number, one lane letter, a `Touches` list that overlaps no sibling, shared interfaces fixed in advance (the output file shape, the country pack format, the id lists), and `Depends on` set so that independent stages run at once. Check: a script lists the Touches of all build briefs and reports any overlap; each brief fits one session (about 5 files or one module).
Stage D2 is the point at which build briefs may be written; none exists before D1 is approved.

## Touches
`docs/model-v3/acceptance.md` (new), `docs/briefs/` (new build briefs), `STATUS.md`, `docs/lane-plan.html`, `docs/decisions.md`, this brief's progress block, and the retirement of 011g (moved to `docs/archive/briefs/`) when D2 is approved.

## Acceptance criteria
- Each of R1 to R11 appears in `acceptance.md` with its criterion (grep).
- The acceptance run command is named once and nowhere ambiguous.
- Build briefs: no Touches overlap between siblings that can run in parallel (script).
- The author has approved D1 before D2 starts.

## Checks to run
The grep for R1 to R11; the Touches overlap script; `git diff --stat` limited to the Touches list.

## Out of scope
Model code, running any model.

## Open questions
Settled by 039g; list any that remain.

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
