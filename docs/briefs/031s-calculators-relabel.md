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
- **Done:** note added to the four pages; local build, render and browser check run; calculator results recorded before and after.
- **Next:** the author decides on the revenue calculator row below; then merge (rebase on `origin/main`, re-run the build, `git push origin HEAD:main`, watch the Action).
- **Decisions:** one inline-styled note (amber border, light tint, so it reads in light and dark) rather than a new CSS class, because the styles files are outside Touches; the link is `/retired.html` as the brief says.
- **Gotchas:** the taxpayer fragment is also injected into `avoidance.md` (`WDT_CALC_INJECT`), so `avoidance.html` shows the note too; the revenue calculator cannot start on `main` (it fetches `rates_model.py`, now `rates_core1.py`; architecture doc Issue 16, `docs/brief-suggestions.md`).
- **Resume:** `python pipeline/preprocess.py; quarto render _build; grep -l "Based on the retired model" -r _build/_site --include=*.html`
- **Not run:** the Action after merge (not merged); a real Pyodide run in a browser (the CDN is unreachable from the sandbox); revenue calculator results (cannot run before or after).
- **State:** pushed on `brief/031s-calculators-relabel` (code commit d254c00).
<!-- progress:end -->

### Change report
```
Change report
- Task: 031s Site: relabel the calculators (site.md B11)
- Files changed:
  - site/pages/calculator_index.md: note above the three cards
  - site/tools/taxpayer_calc.html, revenue_calc.html, ldw_calc.html: note at the top of each fragment (5 lines each, insertions only)
  - this brief's notes
- What is different now: each of the four pages opens with "Based on the retired model", one sentence on what that means, and a link to /retired.html. The same note also appears on avoidance.html, which embeds the taxpayer calculator.
- New or changed interfaces: none. /retired.html does not exist yet (dependency: the retired-page brief, B10); until it does the link is a 404.
- Acceptance criteria:
  - Each of the four pages shows the label: met. Headless Chromium, light and dark, shows the note visible on calculator_index, model/taxpayer, model/revenue and model/ldw (and avoidance); one screenshot checked.
  - Results for three fixed inputs identical before and after: PARTLY MET. Taxpayer and labour-dividend: identical (the recorded JSON is byte-identical on main and on this branch). Revenue: not measurable, it fails to start on main and on this branch (rates_model.py missing, known Issue 16), so there are no results to compare. The pages' scripts are untouched: the diff is 5 inserted lines per fragment and no deletions.
    - Taxpayer 1: V0 = 10^1.301 £m, N = 29, alpha = 1.0, g = 0.1045: honest TW 263.099, alpha TW 263.099
    - Taxpayer 2: V0 = 10^2.0 £m, N = 20, alpha = 0.6, g = 0.05: honest TW 240.3305, alpha TW 224.873
    - Taxpayer 3: V0 = 10^0.5 £m, N = 40, alpha = 1.4, g = 0.15: honest TW 451.8837, alpha TW 477.6756
      (tau_0 0.15, tau_m 0.70, k 10^-3, W_min 2.0 throughout; all seven outputs and every yearly row compared, row hashes ee2d1521623a5670, 7869400de327f7f5, 1276daf3c0b93c03)
    - LDW 1: salary 39,039, VAT share 0.55, energy cut 0.30: employee NICs 2,117.52, employer NICs 5,105.85, energy gain 526.50 a year
    - LDW 2: salary 25,000, VAT share 0.70, energy cut 0.10: employee NICs 994.40, employer NICs 3,000.00, energy gain 175.50 a year
    - LDW 3: salary 120,000, VAT share 0.40, energy cut 0.60: employee NICs 4,410.60, employer NICs 17,250.00, energy gain 1,053.00 a year
      (the full ldw_calc result dict compared in each case)
  - git diff --stat shows only the Touches list: met (four site files plus this brief).
- Deviations from the brief: none. Results come from running each page's own Python call path natively on the same model_v1 core files, because the Pyodide CDN is blocked in the sandbox.
- Risks / follow-ups:
  - NEEDS THE AUTHOR: accept that the revenue calculator cannot be measured (then merge), or fix it first in its own brief.
  - /retired.html is a 404 until the retired-page brief lands.
  - avoidance.html now carries the note, a side effect of the injected fragment; say if you want it removed there.
  - The note's wording ("the new series is replacing") is mine; the author may want to reword it.
- Verification: preprocess exit 0; quarto render exit 0; output page list identical (53 pages); label found in 5 rendered pages; calculator results identical for taxpayer and LDW. Not run: the Action, a real Pyodide run, mobile and accessibility beyond the visible-note check.
- Overview sections likely needing an update: the calculators description (labelled as the retired model).
- Commit / branch: d254c00, brief/031s-calculators-relabel. NEEDS THE AUTHOR: not merged.
```
