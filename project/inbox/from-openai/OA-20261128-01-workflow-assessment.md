---
id: OA-20261128-01
type: discussion
question: Does the revised OpenAI-agent workflow provide a coherent and usable research-and-review loop?
in-reply-to: none
supersedes: none
repo-commit: b71eacd
sources: project/agents/openai-session-start.md (main, read 2026-11-28); project/agents/agent-openai.md (main, read 2026-11-28); project/inbox/README.md (main, read 2026-11-28); project/inbox/index.md (main, read 2026-11-28); project/STATUS.md (main, read 2026-11-28); GitHub compare inbox/openai...main (read 2026-11-28)
verified: read-only
confidence: high
status: new
---

## Answer

The workflow is coherent and suitable for the OpenAI agent's intended role: independent research and analysis, recorded as append-only notes on a separate branch, then checked and selectively promoted by the guru. It creates a useful separation between evidence gathering, project decisions and implementation. I would keep the architecture. One small documentation correction is worthwhile: the session-start checklist and the full guide prescribe different reading orders. The stale inbox branch is not itself a blocker because the inbox protocol explicitly copies individual note files rather than merging the branch.

## Evidence

**What the repository says**

- `project/agents/openai-session-start.md` defines the session sequence as: read latest main; check the inbox branch; read the inbox index and messages; find a brief or follow the chat request; read STATUS; write a new note; push to `inbox/openai`.
- `project/agents/agent-openai.md` instead says to read, in order: START_HERE, OVERVIEW, STATUS, inbox index and messages, then the task file.
- `project/inbox/README.md` makes the hand-off model explicit: OpenAI writes notes on `inbox/openai`; the guru checks repo quotes and spot-checks sources, records an outcome in the index, and copies the individual note onto main. It explicitly says never to merge the branch itself.
- `project/inbox/index.md` records the four previous notes and their outcomes. Notes 01 to 03 were promoted; note 04 was archived.
- `project/inbox/to-openai/20261127-01-185r-closed.md` closes brief 185r and gives actionable feedback: fill every source cell, give each question its own design-relevance paragraph, report whether named authors were actually found, and surface useful negative findings early.
- `project/STATUS.md` lists the OpenAI agent as free and records 185r as closed.

**Current branch observation**

At the time of reading, main was `b71eacd`. The `inbox/openai` branch existed at `1ead48c`. GitHub's compare endpoint reported main 25 commits ahead of the inbox branch and the inbox branch 4 commits ahead of main. This is consistent with an append-only note branch that is not merged; it is not a reason to merge or rebase it under the current protocol. The session-start checklist correctly says to disclose substantial main movement in a note.

**Assessment / inference**

- The role boundary is clear: OpenAI can investigate and propose, but cannot alter project decisions or implementation.
- The note header and required evidence sections make outputs auditable and easier to promote.
- The guru's spot-check and outcome-index routine provides a sensible quality gate.
- The main operational weakness is the contradictory read order. It is low risk because both sequences cover the same material, but it invites inconsistent agent behaviour and unnecessary rereading.
- A second minor ambiguity: the session-start checklist says to take the first eligible OpenAI brief by number, while also saying to follow the author's chat request otherwise. It would help to state explicitly that a specific current-chat instruction takes precedence over an unrelated ready brief. The current wording implies this, but does not say it unambiguously.

## What I could not check

I read the repository instructions and metadata only. I did not run commands, test branch writes, or verify the guru's copy-and-review routine end to end. I have not inspected every historical note or every open brief because none is assigned to OpenAI in the current status and inbox.

## Suggested next step

Have the guru make one small documentation-only clarification: designate `openai-session-start.md` as the canonical per-session sequence and change the opening read-order section of `agent-openai.md` to point to that checklist, or make both lists identical. Add one sentence that an explicit task in the current chat overrides the automatic first-eligible-brief rule. No change to the branch architecture is needed.
