# 106: Agent workflow reliability

- **Status:** ready
- **Author/date:** guru with the author, 2026-11-21
- **Depends on:** none
- **Read:** `AGENTS.md`; `docs/agents/brief-template.md`; `docs/agents/guru.md`; `docs/agents/code.md`; `docs/agents/research.md`; `docs/agents/handover.md`; `docs/agents/friction-log.md`; `docs/agents/change-report.md`; current architecture guide and its layer table.

## Goal

Reduce avoidable rework and false conclusions caused by gaps in the agent workflow. Turn the recent friction log into a small set of enforceable improvements to brief design, checkpointing, research-runtime checks, and incident tracking.

## Decisions (author, 2026-11-21)

- Treat the friction log as evidence of recurring workflow failures, not as a performance scorecard.
- Keep the solution lightweight: explicit preflight rules, reliable checkpoints, and honest capability reporting. Do not build an orchestration framework or dashboard.
- The key research rule is that inability to inspect evidence is not evidence that the evidence does not exist.
- The guru owns friction-log status decisions and archival.

## Design

The active friction log currently records 14 incidents. They cluster into four recurring failure modes:

1. **Code brief integration (083c–088c):** missing module-layer declarations, mismatched function inputs, omitted tests, and incomplete Touches lists caused failed checks, out-of-scope edits, and rewrites.
2. **Research runtime mismatch (095r, 097r, 098r, 100r):** agents were asked to inspect held XLSX/ODS/ZIP/Stata files or run repository checkers without a local checkout, shell, or suitable parsers. In 098r, inability to inspect workbooks led to an incorrect conclusion that a published joint distribution did not exist.
3. **Weak handovers (101r, 102r):** progress blocks omitted the actual branch/commit or a concrete next action, forcing successors to reconstruct state.
4. **Long-session context loss (099r):** too much PDF extraction was attempted in one session; intermediate work was lost and had to be repeated.

This brief cannot be split into parallel child briefs: the changes define one shared workflow contract across the brief template, role guides, handover guide, and friction log. Editing those independently risks creating contradictory instructions.

### Stage 1: Establish the source of truth and triage incidents

Review the active friction log and the current canonical guidance. For each entry, determine whether the cause is fixed, mitigated, still open, or should be dropped.

Use these meanings:

- `open`: cause remains unresolved.
- `mitigated <commit>`: a guardrail or workaround reduces recurrence, but the underlying capability or failure mode remains.
- `fixed <commit>`: the underlying cause has been removed and the relevant check demonstrates this.
- `dropped (reason)`: intentionally not pursued, with a short reason.

Update the friction-log instructions to include these meanings. Do not mark a documentation workaround as a capability fix. In particular, distinguish the 097r/098r/100r runtime incidents from the documentation rules added at `fc3906e`: those rules may mitigate the risk but do not themselves provision a local checkout, shell, or file parsers.

The guru sets Status. If another agent executes this brief, it must submit a proposed triage table and leave Status edits and archival to the guru. Move only genuinely fixed or dropped entries to `docs/archive/friction-log-archive.md`; preserve their text and history. Resolve duplicate or contradictory Status lines only where evidence supports a clear resolution. Keep the active log under its stated approximate 100-line limit.

### Stage 2: Make checkpoints and handovers reproducible

Consolidate the canonical checkpoint format across `docs/agents/brief-template.md` and `docs/agents/handover.md`. It must record:

- **Branch:** exact branch name.
- **Commit/state:** exact pushed checkpoint SHA.
- **Done:** completed work and output paths.
- **Next:** one concrete next action.
- **Decisions:** constraints the successor must not revisit.
- **Gotchas/open issues:** blockers, uncertainties, and assumptions.
- **Evidence:** files, source pages, tables, outputs, or tests supporting the work.
- **Resume:** exact fetch/checkout command and first action.
- **Not run:** required checks not run and why.

Require the progress block to be updated in the same commit as each pushed WIP checkpoint. It must describe the branch head being handed over. Reuse the existing progress block; do not create a competing handover mechanism. Keep the block within the existing 15-line limit where practical, using compact evidence references.

### Stage 3: Add code-brief architectural preflight

Update the canonical brief template and, only if needed, the code guide with a compact preflight that must be completed before implementation.

It must check:

1. **Layer compatibility:** every new/changed module and proposed import edge against the architecture layer table and R4 rules.
2. **Function contracts:** named functions, signatures, and required inputs against current implementations; identify the object or fixture supplying each input.
3. **Tests:** affected tests, including tests that assert empty/unimplemented outputs or pin manifests/digests.
4. **Touches completeness:** every expected changed file, including tests, fixtures, architecture tables, manifests, and documentation.
5. **Assertion consequences:** which assertions or fixtures need changing and why.

Do not duplicate the architecture guide or turn the preflight into a lengthy design review.

### Stage 4: Make the research-runtime gate factual

Audit the actual capabilities available in the research execution environment. For each item, record **available and tested**, **available but untested**, or **not available**:

- Local repository checkout and branch operations.
- Shell execution and Python.
- XLSX and ODS parsing.
- ZIP inspection.
- Stata file inspection.
- PDF extraction and page-level verification.
- Running repository validation scripts.

Test capabilities where the environment permits. Do not infer availability from tool names or prior agents' environments. If no stable local research runtime is available, say so. Do not claim this brief has provisioned one.

Make the stop rule explicit in `docs/agents/research.md` and the brief template: if a task requires an unavailable capability, stop before making a substantive finding and request the missing file or runtime. Record inaccessible evidence as `not inspected` and checks as `not run`, with the reason. Do not conclude that a table, dataset, or source is absent unless the relevant source has actually been searched or inspected adequately.

Identify the smallest practical follow-up needed to provide a usable runtime (for example, a standard checked-out workspace or a CI job), but do not implement a new environment unless an existing, bounded mechanism makes it straightforward.

### Stage 5: Protect long evidence tasks from context loss

Review the existing long-data-brief rules in `docs/agents/research.md`. Ensure they explicitly require bounded source groups, incremental persistence of extracted rows and notes, progress-block updates at each checkpoint, and a clean stop when the session budget is low. The only copy of extracted values must never live in conversational context. Reuse the existing skeleton-first / one-block-one-push rules rather than duplicating them.

### Stage 6: Define minimal reliability measures

Define three simple counts for completed briefs:

- **Friction incidents:** distinct friction-log entries attributable to the brief.
- **Rework incidents:** distinct incidents that caused a rewrite, repeated extraction, incorrect action, or out-of-scope change.
- **Blocked checks:** distinct required checks that could not run because of environment or access limitations.

One incident may contribute to more than one measure, but count it only once within each measure. Do not build a dashboard or pipeline. Use the change report or a periodic manual summary. Establish a baseline from the current active log and state any classification ambiguity rather than manufacturing precision.

## Touches

Confirm paths before editing. Expected files:

- `docs/agents/friction-log.md`
- `docs/archive/friction-log-archive.md`
- `docs/agents/brief-template.md`
- `docs/agents/handover.md`
- `docs/agents/research.md`
- `docs/agents/code.md` (only if the preflight cannot be expressed cleanly in the brief template)
- `docs/agents/change-report.md` (only if the metric definitions belong there)
- `docs/briefs/106g-agent-workflow-reliability.md` (this brief's progress and change report)

Do not edit unrelated research findings, model code, or old briefs except where a minimal correction is required to make the new workflow rules consistent. Do not edit `AGENTS.md` unless a short pointer is necessary.

## Stages

- **1. Triage and evidence map:** classify all active friction entries; identify canonical guidance and existing mitigations. Checkpoint: proposed triage table and runtime capability inventory; check: every active entry accounted for.
- **2. Shared workflow contract:** update friction-log statuses, checkpoint/handover rules, and code preflight in their canonical locations. Checkpoint: docs changes committed; check: cross-read the affected guides for contradictions.
- **3. Research safeguards and measures:** update runtime stop rules and incremental extraction guidance; define the three metrics and baseline. Checkpoint: completed docs and change report; check: documented checks run where available, all unavailable checks explicitly recorded.

## Inputs and early check

- Friction evidence: all active entries in `docs/agents/friction-log.md`.
- Runtime guidance: `docs/agents/research.md` and its long-data-brief sections.
- Existing checkpoint contract: `docs/agents/handover.md` and the progress block in `docs/agents/brief-template.md`.
- Code architecture contract: current architecture guide and R4 layer table; confirm its exact path before editing.
- Before making edits, verify the current active-log entry count and inspect whether `fc3906e` changed guidance only or added executable runtime support. Do not infer the latter.

## Acceptance criteria

- [ ] Every active friction entry has a deliberate status or is explicitly left open with a reason; archival preserves the full original entry.
- [ ] Mitigations are not labelled as fixes. The 097r/098r/100r runtime incidents distinguish workflow guardrails from actual runtime capability.
- [ ] The 098r failure mode is explicitly prevented: inaccessible workbooks cannot support a claim that a table or distribution is absent.
- [ ] The canonical brief template and handover guide share one complete checkpoint contract, updated at each pushed WIP checkpoint.
- [ ] Code briefs require layer/import, function-input, test-impact, and Touches preflight.
- [ ] Long evidence tasks persist results incrementally and can resume without reconstructing prior conversational context.
- [ ] The runtime capability inventory reports only tested capabilities as tested.
- [ ] The three reliability measures have unambiguous counting rules and a baseline from the current log.
- [ ] Existing documentation checks pass, or each unrun check is explicitly recorded with its reason.
- [ ] The diff stays within Touches and introduces no duplicate or contradictory instructions.

## Checks to run

First verify whether the session has a local checkout and shell. If it does, run the documented agent-documentation checker and relevant tests for changed workflow files. If it does not, record the checker as **not run**; a GitHub API edit is not equivalent to executing it.

Inspect the final diff against Touches. Confirm every referenced path exists, every archived entry is genuinely closed, and the updated guides agree on the checkpoint and runtime rules.

## Out of scope

- Building a general agent orchestration framework.
- Creating dashboards, scoring systems, or elaborate performance reporting.
- Provisioning a new cloud/local runtime without a separately agreed implementation path.
- Rewriting the entire agent handbook.
- Changing WDT economic assumptions, model logic, or research conclusions.

## Open questions

None for the documentation changes. If the runtime audit finds that a usable local research runtime does not exist, report the smallest practical provision option; do not silently expand this brief into an infrastructure project.

## Implementation notes

<!-- progress:start -->
- **Done:** Brief drafted from the friction log and canonical agent guides.
- **Next:** Verify architecture-guide path and runtime capabilities; then execute Stage 1.
- **Decisions:** Guru owns friction-log Status edits and archival; distinguish mitigation from capability fix.
- **Gotchas:** GitHub API access alone does not provide a local checkout, shell, or workbook parsers.
- **Resume:** `git fetch origin brief/106c-agent-workflow-reliability:refs/remotes/origin/brief/106c-agent-workflow-reliability`; check out that remote branch; read this progress block and begin Stage 1.
- **Not run:** Repository checker and local runtime capability tests; brief authoring used GitHub API only.
- **State:** Initial brief commit; see branch head in the handover message.
<!-- progress:end -->
