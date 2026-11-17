# 013: Restructure the series (hub and spokes)

- **Status:** underway (stages A, B and C passed; stage D ready)
- **Author/date:** K. Ogata with the guru, 2026-11-16
- **Depends on:** 011g (model v3 design) for the data gate; 012r feeds it
- **Read:** `docs/restructure/map.md`, then `docs/model-v3/outputs.yml`. Nothing else until a stage names it.

## Goal
Replace the 33 long, semilinear papers with a hub (general-reader whitepaper, problem first), about 12 short spokes and a few standalone papers, all resting on a data layer. Plan it fully before any prose is written.

## Decisions (author, 2026-11-16)
- Hub for the general reader; economists and policymakers routed to their area.
- Full rewrite of everything; the old papers are done away with and only guide the new ones. Renaming, moving and cutting are open. ADD and INST may be standalone.
- The hub leads with the problem the tax solves. The moral and mechanism arguments stand; the gap is raw data and calculations.
- Flatter in navigation and in content.
- **Gate: no spoke is written until the data is finalised.** In v1 and v2 papers were written before results, and later results (Sweeps) forced changes back through VAL and RATES.

## Design
Five stages, each ending in a stop. One session does one stage.

## Stages
- **A: hub outline and spoke map** (guru). Checkpoint: `docs/restructure/map.md` marked up by the author; check: every hub section and spoke has a job, a reader and a list of data hooks.
- **B: content ledger** (guru, may be split by paper group). Checkpoint: `docs/restructure/ledger.md`; check: every section of all 33 papers has a disposition (keep to spoke X, merge, drop as redundant, standalone, archive) and a flag for whether it needs model numbers. The flagged claims are listed as demanded outputs and checked against `outputs.yml` for coverage before v3 outputs freeze; fill `element:` in `outputs.yml` with spoke IDs. Also list, per spoke and for hub section H1, the outputs it needs that `outputs.yml` lacks (proposed additions, not yet added), and the old words kept per spoke against its budget.
- **C: spoke template and writing rules** (guru with the writing lane). Checkpoint: `docs/restructure/template.md`; check: shape, word budget, data-hook syntax, objection block and Data block defined; one paragraph written as a test only.
- **D: site and pipeline requirements** (guru, then a site brief). Checkpoint: `docs/restructure/site.md`; check: new ID scheme, how hooks fill from model outputs at build, routing block, what happens to `papers.yml`, anchors, crosslinks, the format checker, the Project Map and brief 007w (obsolete).
- **E: rewrite order and gate** (guru). Checkpoint: `docs/restructure/order.md`; check: the order spokes are written in, the data each needs, and the frozen-data condition that opens the gate.

## Touches
New folder `docs/restructure/`, `docs/briefs/`, `STATUS.md`, `docs/lane-plan.html`, `docs/decisions.md`; at stage B one edit to `docs/model-v3/outputs.yml` (the `element:` field).

## Acceptance criteria
- Stages A to E checkpoints exist and meet their checks.
- `git diff --stat` shows no change to `source/`, `pipeline/`, `site/`, `model_v1/` or `model_v2/`.
- The author has approved each stage before the next starts.
- The gate is written into `order.md` and no spoke exists before it opens.

## Out of scope
Writing spoke or hub prose, editing old papers, site changes, model code.

## Open questions
See section 5 of `map.md`.

## Implementation notes
<!-- progress:start -->
- **Done:** stage A passed; author decisions are in `map.md` section 5 (FAL into S12; SCOPE, ADD, INST standalone; WFR and LDW into spokes; add outputs for the problem section; 2,000 to 4,000 words provisional).
- **Stage B drafted (2026-11-17):** `docs/restructure/ledger.md` (summary, budget finding, demanded outputs, proposed additions) and `ledger-sections.md` (980 rows, all 33 papers); `element:` filled for all 21 outputs. Waiting for the author on the decisions in `ledger.md` section 8.
- **Stage B passed (2026-11-17):** author decisions in `ledger.md` section 8 and `map.md` section 7.
- **Stage C drafted (2026-11-17, Agent 6):** `docs/restructure/template.md`; guru applied the stage B decisions (cap 6,000, appendix spokes). Author approved it 2026-11-17 and added section 6a (figures and tables).
- **Next:** stage D; briefs 014g to 016g define the added outputs in parallel; then stage D (site and hooks).
- **State:** stage C passed; stage D ready
<!-- progress:end -->
