# 001: Audit of model v1 and model v2 (no building)

- **Status:** built (merged)
- **Author/date:** K. Ogata with the guru, 2026-11-15
- **Depends on:** 003s, 004s, 005g, 006c, 008g, 010s
- **Read:** `docs/model-lessons/` (all three files), `docs/agents/reference/code/conventions.md`, `docs/agents/reference/framework.md` (section on checks), the two model folders (`model_v1/`, `model_v2/` after 010s; `model/`, `model_new_2/` until then) and the papers' figure and table list (`registry/contents.yml`).

## Goal
Know exactly what model v1 and model v2 compute, where each is wrong or needlessly complicated, and which outputs the papers need, so model v3 can be designed from facts. This brief changes no code and builds nothing.

## Decisions (author, 2026-11-15)
- This brief replaces the earlier "model v3" brief. Model v3 is not designed until the audit is finished (brief 011g).
- Model 1 has errors that an earlier agent identified; the agent was not controlled well enough and kept building. This time the agent audits only.
- Model 2 revised model 1 but grew too complicated.
- Housekeeping comes first; no audit work starts until the housekeeping briefs are merged.

## Design
Audit one model per stage, each stage ending in a written note and a stop. The agent writes only under `docs/model-audit/`.

For each model, the note answers:
1. **Inventory.** Modules, their order of dependence (cores, then tables, then charts), inputs (`WDT_Params.toml`, `jst_r6.json`, rate tables), outputs and which paper figure or table each output feeds. Lines of code per module.
2. **Mechanism.** What the model computes, in plain terms, stated against the tax mechanism in the papers (`site/pages/Project-Map.md`, relevant `source/` sections read by section).
3. **Errors.** Each error as: where (file, function), what is wrong, how it was shown (a number, a test or a hand calculation), its effect on a paper output. Start from `docs/model-lessons/drift-register.md`; confirm each item against the code, mark it confirmed, not reproduced or new.
4. **Complication.** For v2: what it added over v1, and for each addition whether a paper output needs it. Name the three largest sources of complexity with line counts.
5. **Tests.** What is tested, what is not, whether the tests pass today (run them if they take under 5 minutes, otherwise say not run).

The guru then writes the synthesis (stage E): the lessons note and the list of outputs v3 must produce.

## Touches
New folder `docs/model-audit/` only. Model folders are read, never edited or run beyond the test commands named above.

## Stages
- A: audit v1, inventory and mechanism. Checkpoint: `docs/model-audit/v1-inventory.md` pushed; check: every module in the folder appears in the note.
- B: audit v1 errors. Checkpoint: `docs/model-audit/v1-errors.md` pushed; check: every `drift-register.md` item has a status.
- C: audit v2, inventory and mechanism. Checkpoint: `docs/model-audit/v2-inventory.md`; check as A.
- D: audit v2 complication and tests. Checkpoint: `docs/model-audit/v2-complication.md`; check: three named sources of complexity, each with a line count.
- E (guru): synthesis and the v3 requirements list. Checkpoint: `docs/model-audit/synthesis.md` and a draft of brief 011g.
One session does one stage and stops. The agent does not start the next stage.

## Acceptance criteria
- Each stage's checkpoint file exists and meets its check.
- `git diff --stat main` shows changes only under `docs/model-audit/`.
- Each claim about the code cites a file and function name.
- Every error carries a number or a reproducible check, not only a description.

## Checks to run
`git diff --stat origin/main` limited to `docs/model-audit/`; a grep that each module name from `ls` appears in the inventory note.

## Out of scope
Fixing any error, writing or changing any model code, building any part of v3, changing paper text, running the full model scripts.

## Open questions
- Which outputs the rewritten papers will need (answered in stage E, with the author).
- Where v3 will live and where it reads `jst_r6.json` (decided in 011g).
- If the audit finds that the papers' published figures depend on a v1 error, stop and ask the author before continuing.

## Implementation notes
<!-- progress:start -->
- **Done:**
- **Next:**
- **Decisions:**
- **Gotchas:**
- **Resume:**
- **Not run:**
- **State:** stage E done 2026-11-16 (guru with the author, a question-and-answer session): `docs/model-audit/synthesis.md` written and brief 011g redrafted. The author reframed v3 as a range model with three headline outputs; see the synthesis. Merged, ready to retire.
<!-- progress:end -->
