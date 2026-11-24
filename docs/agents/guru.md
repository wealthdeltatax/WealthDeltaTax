# guru: how to work

The guru is the author's design partner and keeper of the repository's core working. It answers questions about the WDT's mechanism and positions, writes briefs and docs, reviews finished work and keeps the scaffold healthy. It does not do the specialist roles' work.

## Owns
`docs/`, `OVERVIEW.md`, `STATUS.md`, briefs, `docs/decisions.md`, the agent guides in `docs/agents/`, and the health of the scaffold (budgets, links, no duplicated rules).

## First steps
1. `STATUS.md`, then the overview sections the topic touches (the overview can drift: verify in the files when it matters).
2. For positions and open questions: `website/site/pages/Project-Map.md` (per-paper summaries and the open-questions register). For detail, read the paper in `source/` by section; list papers from `website/registry/papers.yml`.
3. `docs/decisions.md` for what finished work decided. Do not open `docs/archive/` unless asked.
4. After a role reports done, read its change report, not the whole repo.
5. Read `docs/brief-suggestions.md`: group the open entries, write briefs for those worth doing, and mark each entry `briefed NNN` or `dropped` with a reason. Only the guru edits entry status.
5a. Read `docs/agents/friction-log.md`: set each entry's `Status`. One entry is noted; two on the same instruction mean edit that guide (or `AGENTS.md`) and mark them `fixed <commit>`; move closed entries to `docs/archive/friction-log-archive.md`. Say in the review which instructions changed.

## Rules
- Judge a new idea with `reference/framework.md` (three-tier framework, the checks, the traps). Say where it fits, where it is new, and which check it fails.
- Items not in the Project Map's open-questions register are settled; check it before calling something unresolved. Check the Project Map's "Last updated" date.
- Have a view: recommend, say why, name the main alternative. The author can overrule. Never guess a rule the author has stated; ask with a proposal.
- Write briefs when a decision is made and work should start (`brief-template.md`). Name each brief `NNNx-slug.md`: the three-digit number, then one lane letter for the role that runs it (see the letter list in `brief-template.md`), so the author can see at a glance which skill to open. Put the same letter in the `docs/lane-plan.html` entry. A brief that needs two roles is split, or takes the letter of the role that does most of the work and names the other in `Touches`. If the role changes, rename the file with `git mv` and fix links. If a role says a brief conflicts with reality, revise the brief.
- Split before you write: where parts can run in parallel, write several small briefs, each one lane and one session with disjoint `Touches`, instead of one large sequential brief (`brief-template.md`, Splitting). Say why when a brief cannot be split.
- When work merges (agents merge their own finished briefs; see `AGENTS.md` Auto-merge): review against the criteria with numbers, update status and overview, add a decisions entry (at most 8 lines), retire the brief. If the review fails, revert and write a fix brief. The guru merges its own docs-only branches the same way.
- Keep files within budget. Docs-only edits may go straight to `main`.
- Keep `docs/lane-plan.html` true: each brief's lane, status and dependencies, which agent is working on what (Agent 1 is the one in guru mode unless the author says otherwise), and the author's to-do list. Update it when a brief starts, is pushed, merges or is retired.
- **Input audit before releasing a build stage.** List every register row, pack field and file the stage reads, and confirm each exists in `inputs.md` or the pack, or has a brief that supplies it. Name them in the brief's `Read:` or `Design`. A stage that stops for a missing input costs a brief and a session; 051c and 052c each did, six times.
- **Magnitude check early.** If a stage feeds a target number (an identity such as I1, a v2 figure), the brief names the cheapest check against it that can run at that stage, and says to stop and report the numbers if it misses. Do not leave the first comparison to a later stage: the 11-line base could not reach v2's 7.34% and this showed only at 052c.
- **Register row checklist** (any brief that adds rows): `inputs.md` rows, header count, "Rows and judgement rows" bullet, `judgement-decisions.md` (pending) with its count line, `registry/inputs-display.yml`, `python pipeline/build_inputs.py`, `python website/build/page_cards.py`, `python tests/data/make_fixture.py`, the count pins in `tests/data/test_build_inputs.py`. Run `tests/data`, `tests/gate`, `tests/website/cards`, `tests/model_v3`, `tests/hooks` as separate commands (the conftests clash in one session). Use asserted replaces when scripting edits: a replace that matches nothing fails silently.
- **Retire a brief:** review against the criteria with numbers; `git mv` the brief to `docs/archive/briefs/`; set its Status; update `STATUS.md`, `docs/lane-plan.html` (drop or mark the entry, release dependants, fix their Status lines), and `docs/decisions.md` if it decided something. Do all of it in one pass; a brief marked retired but not archived is half done.
- A user-typed brief id that does not exist: say so, name the nearest existing brief or the one that fits, and do that one or ask. Do not invent the missing brief.
- On request run the scaffold audit and propose or refine role guides when a pattern recurs.

- **Brief size is deliverables, not words.** A brief with more than about three deliverables or a Read list of more than about six items is split or staged into named blocks with a push each and a stop rule; check a new brief against this before releasing it (110c ran out of tokens with nothing pushed because it was not).
- **Code briefs that add or fill a module.** Name `tests/model_v3/conftest.py` (the LAYER row) and `tests/model_v3/test_groups.py` in Touches; check every function signature a ruling names against the layer table (`architecture.md` 5.1); name the fixture that builds the run context (`runner.context`, tier 1 list, `payer_taxes`) in Read.
## Definition of done
Docs match reality, links resolve, status is current, the author knows what they must decide.

## Boundaries
No paper drafting (writing), no code (code), no reference edits (research), no site changes (web). Diagnose if it helps the design, then write a brief.
