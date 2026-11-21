# 096: Design the simplest viable household cohort model (test D)

- **Status:** ready
- **Author/date:** K. Ogata with the guru, 2026-11-20
- **Depends on:** 094r and 095r (both reported and reviewed)
- **Read:** the 094r and 095r notes in `docs/research/`; `docs/hypotheses/household-consumption-and-wealth-replenishment.md` (sections 11 to 14); `model_v3/core/kernel.py`; `docs/model-v3/architecture.md`.

## Goal
Specify, on paper, the smallest cell structure that applies the 094r household identity and can be calibrated from what 095r found identifiable. The output is a design the author reviews before any implementation brief.

## Decisions (author, 2026-11-20)
- No universal depletion scalar and no fiscal targeting (see 094r Decisions). 3.5% appears only as a labelled legacy comparator.
- Test cells are illustrations of the same identity, not claims that every household in a group behaves alike. Do not force positive saving in every cell, assume all retirees decumulate, or assume all high-wealth households preserve wealth.
- The model may be partial equilibrium, with GDP, labour income and return paths external; say so and do not claim stock-flow closure with firms, government, banks or abroad.

## Guru notes, 2026-11-21 (from the 094r and 095r reviews)
- **Use only what 095r identified.** 095r found no UK rate by wealth band for any flow. Entries 095r marked **recheck** were verified on 2026-11-21 in `docs/research/095r-source-acquisition-and-verification.md` (section 8): read that note and use its corrected readings, not 095r's. In short: the 92% gains share is ranked by remuneration, not wealth; 64% is the share of private pension wealth held by the top decile of pension wealth; neither the national accounts nor WAS counts the state pension as household wealth; the 7% (OBR) and 34% (RF) pension figures are different mechanisms and not a range. None is a depletion or saving rate. Its section 7 rows are **not entered** in the register and the pension additionality "range" mixes two bases: do not use it. Cell parameters with no identified range stay unset or are labelled illustrative or judgement.
- **094r found:** the kernel's c is the retained cash yield less net saving, as a share of the grown stock (not consumption); `consumed` is a sink nothing reads; the state's units and the fund's cash flow are two unlinked public representations (note A3); c acts on pension and housing wealth and on lines below the threshold; WDT is assessed after c. Part 4 below must say how the new design resolves the public-side representation.
- **Code impact (item 4).** The form `(1+g)(1-c)` is repeated outside the kernel (`revenue.py` payer status and the M1a identity, `burden.free_path`, `support.system_run`, `revenue.identity`). Say whether a single household-step function would be introduced first, and list the five call sites, the pack inputs missing (income by wealth band, consumption, liabilities, age, pension flows, the cash-yield split already in `jst_r6.json`), the tests and digests that would move, and which layers stay as they are (assessment, settlement, fund, retirement, outputs).

## Design
1. **Cells.** At least four test cells: a working household with positive net saving; a low- or zero-saving cell; a retired or dissaving cell; a high-wealth cell whose saving and wealth preservation may differ. Minimum segmentation is wealth and income, with working or retired status or age added where 095r says data support it; asset liquidity or composition only where data identify or bound it. Say why each split earns its place and what it costs in data.
2. For each cell: opening balance sheet or distribution, income flow, consumption, saving or dissaving, returns (cash and gains kept apart), transfers, debt, WDT paid, with each parameter marked **data, calibrated, externally specified, judgement or illustrative**, using 095r's ranges only where it gave one.
3. **Aggregation and transitions.** How cells aggregate to the household sector and to the bands the WDT schedule uses; which demographic transitions (ageing into retirement, household formation, inheritance) are needed to preserve the relevant aggregates and distribution, and which are left out and why.
4. **Interface to v3.** Where the design would replace `grow_and_consume` and what the kernel, pack, register and manifest would need (new inputs, new outputs, the legacy-comparator mode); a gap list only, no edits.
5. **Validation plan** (Test E as a plan, not a run): which UK periods overlap, which holdout is possible, which aggregates and distributional moments are compared, with attrition, definition changes and reconciliation residuals named. A model that matches aggregate wealth but misses the distribution does not pass.
6. **Comparison plan** (Test F as a plan, not a run): common starting distributions, return paths, schedules and seeds for the legacy, new baseline and defensible low and high scenarios; the outputs to report; attribution of differences to flow mechanisms only.

## Touches
`docs/research/096r-cohort-cell-design.md` (new), this brief's progress block, `docs/agents/friction-log.md`. No code, register or manifest edits.

## Acceptance criteria
- Four test cells specified with the same identity and every parameter labelled by status.
- Each segmentation choice justified against 095r's identification table; flows with no supportable range stay unset.
- The v3 interface gap list, the validation plan and the comparison plan are present.
- No scalar depletion rate appears as a proposal; no result is described as favourable or unfavourable to WDT.

## Checks to run
`python -I pipeline/check_agent_docs.py`.

## Out of scope
Implementation, backcasts and WDT runs (later code briefs, after the author authorises); register edits.

## Open questions
None.

## Implementation notes
<!-- progress:start -->
- **Done:** note `docs/research/096r-cohort-cell-design.md`: segmentation table against 095r, four test cells with a status-labelled parameter matrix, aggregation and transitions, v3 interface gap list (five call sites, public-side resolution, missing pack inputs, tests and digests that move), validation plan (test E), comparison plan (test F), open questions.
- **Next:** author rules on the open questions (note section 7); then an implementation brief, only after the author authorises.
- **Decisions:** cells are wealth band x working/retired; consumption specified on the income side per cell and left unset; no scalar depletion rate; one public-side representation (fund) with units kept as settlement bookkeeping, pending the author.
- **Gotchas:** nearly every flow parameter by cell is unset because 095r found no band rates; recheck items and 095r section 7 rows were not used; pack rows for D4-5 property and pension share are absent.
- **Resume:** n/a
- **Not run:** no model code or runs (design); the five call-site line numbers were read, not executed.
- **State:** done; not merged (open questions, note section 7)
<!-- progress:end -->

Change report
- Task: brief 096r, design of the simplest viable household cohort model (test D)
- Files changed: `docs/research/096r-cohort-cell-design.md` (new note); this brief (progress block, report)
- What is different now: the cell design, interface gap list, validation plan and comparison plan exist on paper for author review
- New or changed interfaces: none
- Acceptance criteria: four test cells with one identity and every parameter labelled: met (many labelled unset); segmentation justified against 095r: met; interface gap list, validation plan, comparison plan present: met; no scalar depletion rate proposed and no favourable/unfavourable description: met
- Deviations from the brief: none
- Risks / follow-ups: five open questions in note section 7; most cell flows cannot be run until data requests from 095r are filled
- Instruction friction: none
- Verification: `python -I pipeline/check_agent_docs.py` (passed, exit 0); worked-example arithmetic checked by hand
- Overview sections likely needing an update: none
- Commit / branch: see git log, brief/096-cohort-cell-design
