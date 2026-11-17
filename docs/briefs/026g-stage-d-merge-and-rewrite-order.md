# 026: Stage D merge and rewrite order (013g stages D checkpoint and E)

- **Status:** ready
- **Author/date:** K. Ogata with the guru, 2026-11-17
- **Depends on:** 013g stages A to C; 017s to 021s and 025w (all merged); `outputs.yml` as amended by 025w
- **Read:** `docs/briefs/013g-restructure-the-series.md`; `docs/restructure/map.md`, `ledger.md` (sections 2, 8, 9), `shortcodes.md`, `ids-map.md`, `template.md`; `docs/restructure/site/ids.md`, `hooks.md`, `figures.md`, `checker.md`, `nav.md`; `docs/model-v3/outputs.yml`, `metrics.md`, `inputs.md` (headers and judgement rows only); `docs/model-v3/drivers.md`; `docs/briefs/011g-model-v3-design.md` (stage list); `docs/agents/guru.md`, `docs/agents/brief-template.md`.

## Goal
Close stage D with one reviewed site and pipeline requirements document, then write the order in which the spokes are written and the condition that opens the data gate (stage E). Two files for the author to approve, plus the build briefs they imply.

## Decisions (author, 2026-11-17)
- Shortcodes are page ids; cap 6,000 words per page; POL splits into POL, ADOPT, PILOT and FALS into FALS and HYPO; the other splits are measured at stage E.
- **Gate:** no spoke prose until the data is finalised. Spoke prose means any spoke or hub text, including drafts. Planning, outlines and tests of one paragraph are allowed.
- The author's answers to the 017s, 018s (accepted), 019s, 020w (four asked, the rest accepted under blanket approval) and 021s questions are final unless the siblings contradict each other; where they do, ask.
- The old 33 papers are retired and only guide the rewrite.
- The stock-wealth floor hypothesis (`docs/model-v3/stock-floor-hypothesis.md`) is exploratory. Do not design around it. Note in `order.md` which spokes and outputs it would touch if adopted, in one short table.

## Design
Two stages, sequential: `order.md` needs the list of build items that `site.md` produces.

1. **site.md.** Merge the five sibling files into `docs/restructure/site.md`: ids and URLs, hooks and data file, figures, checker, navigation. Do not copy them; summarise each in one page, link to the sibling for detail, and write one reconciliation section where they overlap or disagree (page registry fields, `routing.yml`, URLs of data pages, draft and release builds, front matter keys, the checker's view of figure blocks). Settle each conflict or list it as a numbered question with a proposed answer. Then list the build work as **a table of proposed briefs**: lane letter, one-line goal, Touches, Depends on, what can run in parallel. Each must fit one session and touch files no sibling touches (`brief-template.md`, Splitting). Include: registry and ids, data file and resolver, Data block generator, figures renderer, navigation and routing, spoke checker tool, redirects, calculators label. Do not write those briefs; write them only after the author approves `site.md`.
2. **order.md.** (a) The order spokes and the hub are written in, with the reason for each position (outputs needed, spokes it cites, spoke that is cited by others, reader value). (b) For each spoke: the outputs and inputs it needs (from `outputs.yml` `element:` and `inputs.md`), the data it needs frozen, and the old papers to read (from `ledger.md`). (c) The **gate**: a written, checkable condition that opens it, built from: model v3 stages complete, `run.status` final, input register judgement rows decided, `outputs.json` produced for every output the spoke cites, checker and resolver working. State which of these a spoke needs, so a spoke whose outputs are frozen early can start early if the author agrees. (d) Measure the optional splits of `ledger.md` section 9.2 against 6,000 words after compression and say which to take (or list as a question). (e) Writing briefs: how many, one per spoke or per group, what each needs as a shared input, which can run in parallel after the gate, and the review loop (checker, then guru, then author). (f) What the author must still decide, as numbered questions with a proposed answer. (g) The still-open items from `ledger.md` 8(e): the concentration output for WELF 4.3, the comparison-tables page, and the avoidance guide.

Cannot be split further: the two files are one agent's work because `order.md` places the build items from `site.md` on the gate.

## Touches
`docs/restructure/site.md`, `docs/restructure/order.md`, this brief's progress block. At the end only: `STATUS.md`, `docs/lane-plan.html`, `docs/decisions.md`, `docs/briefs/013g-restructure-the-series.md` (status line). Nothing in `source/`, `pipeline/`, `site/`, `registry/`, `model_v1/`, `model_v2/`, `outputs.yml`, `metrics.md`, `inputs.md`, `template.md`, or the sibling files under `docs/restructure/site/` (if one is wrong, note it as a question).

## Stages
- A: `site.md` merged with the reconciliation section, the question list and the table of proposed briefs. Checkpoint: pushed to branch; check: every sibling file is linked, each conflict has a ruling or a question, every proposed brief names disjoint Touches.
- B: `order.md`. Checkpoint: pushed; check: every one of the 19 shortcodes plus ADOPT, PILOT, HYPO, the hub and the three standalone papers has a position and a data need; the gate condition can be tested by a command or file check.

## Acceptance criteria
- `site.md` exists, links all five siblings, and leaves no unresolved conflict that is not a numbered question.
- `order.md` lists every page, the gate, the writing briefs plan and the questions.
- The gate is written as checks, not as a feeling.
- No spoke or hub prose is written.
- `git diff --stat` shows only the Touches list.

## Checks to run
Script check that every shortcode in `shortcodes.md` and the three splits appears in `order.md`, and that every `element:` value in `outputs.yml` resolves to a page in `order.md`. No build run (no site file touched).

## Out of scope
Writing the build briefs, spoke or hub prose, editing `outputs.yml`, `template.md` or any sibling file, model work, the stock-wealth floor design.

## Open questions
The agent asks rather than guesses. It records questions in the brief and stops with NEEDS THE AUTHOR at the end of each stage; the author approves each stage before the next starts.

## Implementation notes
<!-- progress:start -->
- **Done:**
- **Next:**
- **Decisions:**
- **Gotchas:**
- **Resume:**
- **Not run:**
- **State:**
<!-- progress:end -->
