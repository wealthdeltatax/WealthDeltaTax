# 129r: Longitudinal household wealth data: what is reachable without a licence (access and feasibility audit)

- **Status:** ready
- **Author/date:** K. Ogata with the guru, 2026-11-22
- **Depends on:** 125c (merged)
- **Read (block 0: the first two only):** (1) `docs/hypotheses/longitudinal-identification-of-household-wealth-flows.md` (sections 2.3, 3, 6 and 9); (2) `docs/agents/research.md`. Later: `docs/model-v3/household-arm-validation.md` and `docs/research/data/099r/moments.csv` (what is already held; do not redo it).

## Goal
The author approved the **audit only** of the longitudinal-identification phase, and will not get the UKDS licence: say, with sources, what longitudinal evidence on wealth transitions, active and passive accumulation, retirement decumulation, pension valuation and the top tail can be obtained **without a licence** (published tables, working papers, replication material), what a licence would add, and which model parameters each source could inform. No extraction of microdata, no parameter or model change.

## Decisions (author, 2026-11-22)
- Evidence classes follow the hypothesis (section 8): empirically identified, derived, proxy, scenario only, unset. A failure to identify is a valid result and is reported, not hidden.
- Measurement rules of the hypothesis (section 5) bind: wealth change is not saving; active accumulation is a residual; gradients by starting wealth; no transitions from repeated cross-sections; no calibration to fiscal outcomes.
- UKDS Study 7215 (WAS longitudinal) is audited as a source, with its access tier and what it would add, but nothing is assumed obtainable.

## Blocks (one push each; `docs/agents/research.md`, Long data briefs)
- **Block 0:** the note skeleton `docs/research/129r-was-access-audit.md` with every section pending; progress block pushed, before any source is opened.
- **Block 1: the source register.** `docs/research/data/129r/source_register.csv`: one row per candidate source (WAS longitudinal Study 7215, ONS WAS published tables including any longitudinal or transition tables, Resolution Foundation *Before the Fall* tables, ELSA and IFS retirement-wealth work, IFS 2026 on DB pension valuation, Advani-Summers-Tarrant 2025, HMRC Distribution of Personal Wealth, and anything else found): dataset or report, URL, version or date, access tier (open, registered, safeguarded or special licence; what is required), population, unit, wave coverage, weights, what it can identify against hypothesis propositions P1 to P5, limitations, and **whether this session could fetch it** (say plainly where a source was not reachable: a data request for the author, not a finding). Push.
- **Block 2: the feasibility map.** `docs/research/data/129r/feasibility_map.csv`: for each model parameter family (saving by wealth band, active accumulation, wealth transitions, retirement decumulation and pension withdrawal, asset allocation by band, DB pension valuation basis, top-tail stock and composition) one row: best source reachable without a licence, what it identifies, its evidence class, what a licence would add, whether the model can proceed without it (as a labelled scenario or unset). Push.
- **Block 3: the note and the request list.** Fill `129r-was-access-audit.md`: the findings per proposition P1 to P5, the table of classes (counts by evidence class), a ranked **data-access request list** (exact file or table, the parameter it informs, why public data are insufficient), and what the model could take **now** from open sources (candidates only; no register row is added). No recommendation of values: evidence and confidence only. Change report; push; stop.
**Stop rule.** After three blocks, or a quarter of the budget left, write the note from what exists, push, and list unfinished source groups under Next. Scripts print one summary line; do not print large files.

## Touches
`docs/research/129r-was-access-audit.md` (new), `docs/research/data/129r/` (new), the brief's progress block. Nothing in `registry/`, the model, the pack or `docs/model-v3/inputs.md` (candidate rows are proposed in the note, for the guru and author).

## Acceptance criteria
- Every row cites a retrievable source and says what was and was not fetched; a source not reachable is a listed data request.
- Every model parameter family in the feasibility map has an evidence class and a stated fallback (scenario or unset).
- The note separates what is direct observation, residual, proxy and scenario; no point estimate is offered for an unidentified cell.
- Nothing in the repo outside `docs/research/` changes; `python -I pipeline/check_agent_docs.py` passes.

## Out of scope
Any microdata extraction, parameter values, register rows, calibration, model changes, the pilot and full extraction briefs (written only if access appears).

## Implementation notes
<!-- progress:start -->
- **Done:** none
- **Next:** block 0
- **Resume:** `git fetch origin '+refs/heads/*:refs/remotes/origin/*' && git checkout -B brief/129-was-audit origin/brief/129-was-audit`
- **State:** ready; not started
<!-- progress:end -->
