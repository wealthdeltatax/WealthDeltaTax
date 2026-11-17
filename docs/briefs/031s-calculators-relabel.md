# 031: Site: relabel the calculators (site.md B11)

- **Status:** ready
- **Author/date:** K. Ogata with the guru, 2026-11-17
- **Depends on:** none
- **Read:** `docs/restructure/site.md` section 8 (B11) and Q6; `docs/restructure/site/nav.md` sections 2.6 and 10; the four files under Touches; `docs/agents/web.md`.

## Goal
Label the three existing calculators as based on the retired model, so no reader takes them for the new model's results, with no change to what they compute.

## Decisions (author, 2026-11-17)
`docs/restructure/site.md` is approved with its eight answers (drafts under `/draft/`, hub Data block, ADOPT, PILOT and HYPO reached from their parents, `source/hub.md`, pending-page links rewritten to `retired.html`, glossary seeding before the gate, standalones move after the gate). The data gate holds: no spoke or hub prose. This brief builds on fixtures and delivers without the model data. It is one of the first parallel set (029s, 030c, 031s, 032r, 033c, 034c); the Touches lists do not overlap. Author (nav Q4): the calculators stay on their current URLs, labelled "Based on the retired model", and are updated when the newest model is done.

## Design
Add a visible note at the top of each calculator page and of the calculators index: "Based on the retired model", with one sentence on what that means and a link to `/retired.html` (the page may not exist yet; link it by URL anyway and note the dependency in the change report). Do not change formulas, inputs, outputs or URLs.

## Touches
`site/pages/calculator_index.md`, `site/tools/taxpayer_calc.html`, `site/tools/revenue_calc.html`, `site/tools/ldw_calc.html`, this brief's progress block.

## Acceptance criteria
- Each of the four pages shows the label.
- The calculators' results for three fixed inputs are identical before and after (record the inputs and results).
- `git diff --stat` shows only the Touches list.

## Checks to run
The local build named in `docs/agents/web.md` must pass (the push deploys at once); load each calculator page and read the label. The diff touches `site/` so the Action must be watched after merge (AGENTS.md).

## Out of scope
Any change to the calculators' logic or to the navigation, the retired page itself.

## Open questions
The implementer asks rather than guesses.

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
