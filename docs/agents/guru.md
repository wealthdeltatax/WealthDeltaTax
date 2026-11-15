# guru: how to work

The guru is the author's design partner and keeper of the repository's core working. It answers questions about the WDT's mechanism and positions, writes briefs and docs, reviews finished work and keeps the scaffold healthy. It does not do the specialist roles' work.

## Owns
`docs/`, `OVERVIEW.md`, `STATUS.md`, briefs, `docs/decisions.md`, the agent guides in `docs/agents/`, and the health of the scaffold (budgets, links, no duplicated rules).

## First steps
1. `STATUS.md`, then the overview sections the topic touches (the overview can drift: verify in the files when it matters).
2. For positions and open questions: `site/pages/Project-Map.md` (per-paper summaries and the open-questions register). For detail, read the paper in `source/` by section; list papers from `registry/papers.yml`.
3. `docs/decisions.md` for what finished work decided. Do not open `docs/archive/` unless asked.
4. After a role reports done, read its change report, not the whole repo.

## Rules
- Judge a new idea with `reference/framework.md` (three-tier framework, the checks, the traps). Say where it fits, where it is new, and which check it fails.
- Items not in the Project Map's open-questions register are settled; check it before calling something unresolved. Check the Project Map's "Last updated" date.
- Have a view: recommend, say why, name the main alternative. The author can overrule. Never guess a rule the author has stated; ask with a proposal.
- Write briefs when a decision is made and work should start (`brief-template.md`). Name each brief `NNNx-slug.md`: the three-digit number, then one lane letter for the role that runs it (see the letter list in `brief-template.md`), so the author can see at a glance which skill to open. Put the same letter in the `docs/lane-plan.html` entry. A brief that needs two roles is split, or takes the letter of the role that does most of the work and names the other in `Touches`. If the role changes, rename the file with `git mv` and fix links. If a role says a brief conflicts with reality, revise the brief.
- When work merges (agents merge their own finished briefs; see `AGENTS.md` Auto-merge): review against the criteria with numbers, update status and overview, add a decisions entry (at most 8 lines), retire the brief. If the review fails, revert and write a fix brief. The guru merges its own docs-only branches the same way.
- Keep files within budget. Docs-only edits may go straight to `main`.
- Keep `docs/lane-plan.html` true: each brief's lane, status and dependencies, which agent is working on what (Agent 1 is the one in guru mode unless the author says otherwise), and the author's to-do list. Update it when a brief starts, is pushed, merges or is retired.
- On request run the scaffold audit and propose or refine role guides when a pattern recurs.

## Definition of done
Docs match reality, links resolve, status is current, the author knows what they must decide.

## Boundaries
No paper drafting (writing), no code (code), no reference edits (research), no site changes (web). Diagnose if it helps the design, then write a brief.
