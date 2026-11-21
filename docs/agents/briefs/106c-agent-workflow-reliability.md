# 106c · Agent workflow reliability

**Status:** ready  
**Role:** code / repository operations  
**Priority:** medium  
**Created:** 2026-11-21

## Objective

Reduce avoidable rework and false conclusions caused by gaps in the agent workflow. Use the recent friction log as the evidence base. Deliver a small set of enforceable improvements to brief design, checkpointing, research-runtime checks, and friction-log maintenance.

This is a workflow-hardening task, not a general redesign of the agent system. Prefer explicit rules and lightweight checks over additional orchestration.

## Why this brief exists

The friction log shows recurring failures in four areas:

1. **Code brief integration:** briefs omit required module-layer declarations, function inputs, affected tests, or files that must be changed. This caused failed R4 checks, out-of-scope edits, and rewrites (083c–088c).
2. **Research runtime mismatch:** agents were asked to inspect XLSX/ODS/ZIP/Stata files or run repository checkers without a local checkout, shell, or suitable parsers. In 098r, inability to inspect held workbooks led to an incorrect conclusion that a published joint distribution did not exist (095r, 097r, 098r, 100r).
3. **Weak handovers:** progress blocks did not reliably identify the actual branch, commit, completed work, or next action. Successors had to reconstruct state and occasionally infer unfinished work (101r, 102r).
4. **Long-session context loss:** 099r attempted too many full-PDF extractions in one session; intermediate work was lost and had to be repeated.

The central reliability rule is:

> Failure to access or inspect evidence is not evidence that the evidence does not exist.

## Read first

- `AGENTS.md`
- `docs/agents/friction-log.md`
- `docs/agents/research.md`
- `docs/agents/reference/research/reference-workflow.md`
- `docs/agents/reference/research/bib-conventions.md`
- The current code architecture document, especially its module-layer table (architecture.md §5.1 or current equivalent)
- The brief template and any existing brief/check scripts

If a path named above has moved, locate the current canonical file and report the path correction. Do not create a duplicate guide.

## Work

### 1. Triage the friction log

Review every active entry in `docs/agents/friction-log.md`.

For each entry:

- Determine whether the underlying cause is fixed, mitigated, still open, or should be dropped.
- Distinguish a real capability fix from a documentation/workflow mitigation.
- Do not mark an issue fixed merely because a rule now tells agents how to work around it.
- Where a fix or mitigation is evidenced by a commit, record its short SHA.
- Move entries that are genuinely fixed or dropped to `docs/archive/friction-log-archive.md`, preserving their text and history.
- Resolve duplicate or contradictory Status lines only where the evidence supports a clear resolution. Preserve the original incident description.
- Keep the active log concise and under its stated approximate 100-line limit.

Use these status meanings:

- `open`: the cause remains unresolved.
- `mitigated <commit>`: a guardrail or workaround reduces recurrence, but the underlying capability or failure mode remains.
- `fixed <commit>`: the underlying cause has been removed and the relevant check demonstrates this.
- `dropped (reason)`: intentionally not pursued, with a short reason.

The status vocabulary is a proposed clarification to the current convention. Update the log's instructions to match it. Do not claim a runtime capability has been added unless it has actually been provisioned and tested.

The guru owns status decisions. If this brief is executed by another agent, prepare a proposed triage table and leave Status edits and archival to the guru.

### 2. Add a mandatory checkpoint / handover format

Update the canonical brief template and the relevant agent guidance so every resumable brief records, at minimum:

- **Branch:** exact branch name.
- **Commit:** exact latest checkpoint SHA.
- **Done:** completed work, with paths or output locations.
- **Next:** the next concrete action, not a vague phase label.
- **Evidence:** files, tables, source pages, tests, or outputs that support the work.
- **Open issues:** blockers, unresolved questions, and assumptions.
- **Resume:** the exact first action a successor should take.

Require this block to be updated in the same commit as every WIP checkpoint. At handover, it must describe the pushed branch head, not an earlier local state.

A successor should be able to resume without guessing which branch to fetch or reconstructing the previous agent's plan.

### 3. Add a code-brief architectural preflight

Update the canonical brief template or code-agent instructions with a short preflight that must be completed before implementation.

The preflight must check:

1. **Layer compatibility:** every new or changed module and every proposed import edge is compatible with the architecture layer table and R4 rules.
2. **Function contracts:** named functions, signatures, and required inputs match the current implementation. Trace each required input to the object or fixture that supplies it.
3. **Tests:** list the tests that will be affected, including tests that currently assert empty/unimplemented outputs or pin manifests/digests.
4. **Touches completeness:** every file expected to change is named in Touches, including test fixtures, architecture tables, manifests, and documentation.
5. **Test consequences:** state which assertions or fixtures need changing and why. Do not discover this only after implementation.

The preflight should be compact enough to use on every code brief. It should not duplicate the full architecture document.

### 4. Establish an honest research-runtime gate

Review the current research guidance and repository CI/runtime options.

Document the actual capabilities available to agents for:

- Local repository checkout and branch operations.
- Shell execution and Python.
- XLSX and ODS parsing.
- ZIP inspection.
- Stata file inspection.
- PDF extraction and page-level verification.
- Running repository validation scripts.

Separate **available and tested**, **available but untested**, and **not available**. Do not infer capability from a tool's name or from an earlier agent's environment.

If a reliable local research runtime already exists, document how to access it and test the relevant formats. If it does not exist, do not pretend this brief can provision one. Instead:

- Make the research brief gate explicit: if a task requires unavailable local capability, stop before making a substantive finding and request the missing file/runtime.
- Require inaccessible evidence to be recorded as `not inspected` or `not run`, with the reason.
- Prohibit conclusions such as "not published", "does not exist", or "unavailable" unless the relevant source was actually searched or inspected adequately.
- Identify the smallest practical follow-up needed to provide a usable runtime, such as a standard checked-out workspace or CI job. Do not implement a new environment unless the repository already has a clear, bounded mechanism for doing so.

### 5. Add incremental-work rules for long evidence tasks

Review the existing long-data-brief guidance and make sure it explicitly covers long PDF and multi-source extraction:

- Work in bounded source groups.
- Persist each completed source group's extracted rows and notes to the branch before moving to the next group.
- Update the progress block with the checkpoint.
- Avoid keeping the only copy of extracted values in conversational context.
- When the session budget is low, stop cleanly, commit what is complete, and identify the remaining source groups.
- A resumed agent must verify the branch head and progress block before continuing.

Reuse existing rules where they already solve the problem. Do not add a second, conflicting checkpoint system.

### 6. Add lightweight reliability metrics

Define a minimal way to record, per completed brief:

- **Friction incidents:** incidents logged during the brief.
- **Rework incidents:** incidents that caused a rewrite, repeated extraction, incorrect action, or out-of-scope change.
- **Blocked checks:** required checks that could not be run because of environment or access limitations.

Do not build a dashboard or analytics pipeline for this task. A small field in the change report or a simple periodic manual summary is sufficient. Define the counting rule so the same incident is not counted twice.

## Touches

Expected files (confirm canonical paths before editing):

- `docs/agents/friction-log.md`
- `docs/archive/friction-log-archive.md`
- `docs/agents/research.md`
- The canonical brief template
- The code-agent / architecture guidance that owns code-brief preflight
- The long-task / checkpoint guidance, if separate from the brief template
- `AGENTS.md` only if a short top-level pointer is required
- Any existing checker or test that validates brief structure, if the template changes require it

Do not edit unrelated research findings, model code, or old briefs except where a minimal correction is required to make the new workflow rules consistent.

## Deliverables

1. Updated friction log and archive, with status decisions evidenced and no history silently deleted.
2. One canonical checkpoint/handover block, referenced by all relevant brief types.
3. A concise code-brief preflight checklist.
4. A factual research-runtime capability table and explicit stop/recording rules.
5. Clear incremental extraction guidance for long evidence tasks.
6. A lightweight metric definition and a short close-out report listing the baseline counts observable from the current log.

## Acceptance criteria

- [ ] Every active friction-log entry has a deliberate status or is explicitly left open with a reason.
- [ ] Entries moved to the archive are genuinely fixed or dropped; mitigations are not mislabelled as fixes.
- [ ] The 097r/098r/100r environment incidents distinguish documented workarounds from actual runtime capability.
- [ ] The 098r failure mode is explicitly prevented: inaccessible workbooks cannot support a claim that a table or distribution is absent.
- [ ] The canonical brief template contains the complete checkpoint fields and requires updates at each pushed WIP checkpoint.
- [ ] A code brief cannot pass preflight without layer/import, function-input, test-impact, and Touches checks.
- [ ] Long extraction work persists results incrementally rather than relying on conversational context.
- [ ] The runtime capability table reports only tested capabilities as tested.
- [ ] Reliability metrics have unambiguous counting rules and a baseline from the current friction log.
- [ ] Existing documentation checks pass, or any unrun check is explicitly recorded with the reason.
- [ ] The diff is limited to the workflow documentation and directly related checks.

## Checks

Run the repository's documented agent-documentation checker and relevant tests if the environment supports them. First verify the local checkout and shell are available. If they are not, state that the check was not run; do not imply that a GitHub API edit is equivalent to running the checker.

Inspect the final diff against Touches. Confirm that all referenced paths exist and that no duplicate or contradictory instructions were introduced.

## Non-goals

- Building a general agent orchestration framework.
- Creating dashboards, scoring systems, or elaborate performance reporting.
- Rewriting the entire agent handbook.
- Provisioning a new cloud or local runtime without a separately agreed implementation path.
- Changing WDT economic assumptions, model logic, or research conclusions.

## Progress

- **Done:** Brief drafted from the active friction log and current research guidance.
- **Next:** Confirm canonical brief/template paths; execute preflight and workflow changes.
- **Branch:** `brief/106c-agent-workflow-reliability`
- **Commit:** pending initial brief commit.
- **Resume:** Read this brief, inspect the current canonical template and code-agent guidance, then complete the runtime capability inventory before editing workflow rules.
