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
- **Next:** the author decides on the revenue calculator row below; then merge (rebase on , re-run the build, , watch the Action).
- **Decisions:** one inline-styled note (amber border, transparent tint, so it reads in light and dark) rather than a new CSS class, because the styles files are outside Touches; the link is  as the brief says.
- **Gotchas:** the taxpayer fragment is also injected into  (), so  shows the note too; the revenue calculator cannot start on  (it fetches , now ; architecture doc Issue 16, ).
- **Resume:**   Reading references.bib...
  Reading internal.json...
  Merging (177 external refs, 31 papers, 365 citations, 17 flags)...
  ✓ references.json written (177 external refs)
  Looking for papers.yml at: /home/claude/wealthdeltatax/registry/papers.yml
  ✓ 1_Wealth_Delta_Tax_Whitepaper.md: [WP] v1.06 (14,278 words)
  ✓ 2_Moral_and_Philosophical_Foundations.md: [MF] v1.06 (6,685 words)
  ✓ 3a_Research_Gaps.md: [LR.A] v1.02 (4,049 words)
  ✓ 3b_Intellectual_Background.md: [LR.B] v1.02 (8,904 words)
  ✓ 4_UK_Jurisdiction_and_Data_Reference_Paper.md: [JUR] v1.01 (5,547 words)
  ✓ 5_Valuing_Wealth.md: [VAL] v1.09 (15,369 words)
  ✓ 5a_Valuing_Wealth_Mathematical_and_Simulation_Appendix.md: [VAL.A] v1.08 (16,967 words)
  ✓ 5b_Valuing_Wealth_Worked_Examples_Appendix.md: [VAL.B] v1.04 (5,216 words)
  ✓ 6_Corporate_Architecture.md: [CORP] v1.03 (7,861 words)
  ✓ 6a_Corporate_Architecture_Appendix.md: [CORP.A] v1.01 (15,307 words)
  ✓ 7_Constitutional_Governance.md: [GOV] v1.03 (9,894 words)
  ✓ 7a_WDT_Constitutional_Governance_Intellectual_Appendix.md: [GOV.A] v1.01 (7,703 words)
  ✓ 7b_Constitutional_Governance_Operational_Appendix.md: [GOV.B] v1.04 (22,223 words)
  ✓ 8_Rates_and_Revenue.md: [RATES] v1.05 (12,556 words)
  ✓ 8a_Rates_and_Revenue_Appendix.md: [RATES.A] v1.01 (8,004 words)
  ✓ 9_Parameter_Sweeps.md: [SWEEPS] v1.04 (17,057 words)
  ✓ 9a_Parameter_Sweeps_Appendix.md: [SWEEPS.A] v1.02 (18,275 words)
  ✓ 10_Behavioural_Robustness_and_Administrative_Experience.md: [BEHAV] v1.03 (8,091 words)
  ✓ 10a_Behavioural_Robustness_and_Administrative_Experience_Appendix.md: [BEHAV.A] v0.01 (4,691 words)
  ✓ 11_Position_Closure.md: [CLOSE] v1.04 (10,349 words)
  ✓ 12_Political_Architecture.md: [POL] v1.02 (10,806 words)
  ✓ 12a_Political_Architecture_Appendix.md: [POL.A] v0.01 (1,964 words)
  ✓ 13_Phase_One.md: [PHASE1] v1.02 (6,058 words)
  ✓ 14_Environmental_Effects_and_Transmission_Channels.md: [ENV] v1.02 (9,686 words)
  ✓ 15_First_Mover.md: [FM] v1.03 (3,516 words)
  ✓ 16_Modular_Adoption.md: [MOD] v1.00 (1,677 words)
  ✓ 17_Scope_Boundary.md: [SCOPE] v0.05 (2,602 words)
  ✓ 18_Addendums.md: [ADD] v0.03 (7,006 words)
  ✓ 19_Taxpayer_Welfare.md: [WFR] v0.03 (19,071 words)
  ✓ 19a_Taxpayer_Welfare_Appendix.md: [WFR.A] v0.01 (5,684 words)
  ✓ 20_Institutional_Selection.md: [INST] v0.08 (14,535 words)
  ✓ 21_Labour_Dividend_Welfare.md: [LDW] v0.06 (8,716 words)
  ✓ 22_Falsification_Hypotheses.md: [FAL] v0.02 (11,615 words)
  Extracted metadata for 33 papers.

  ⚠ section not in anchors.yml: GOV§4.2
  ⚠ section not in anchors.yml: MF§9.4.9
  ⚠ section not in anchors.yml: GOV§4.2
  ⚠ section not in anchors.yml: INST§0.03
  ✓ Injected taxpayer_calc.html into avoidance.md
  ⚠ section not in anchors.yml: WP§11
  ⚠ section not in anchors.yml: GOV§2.2
  ⚠ section not in anchors.yml: GOV§3.3
  ⚠ section not in anchors.yml: GOV§9
  ⚠ section not in anchors.yml: GOV§10
  ⚠ section not in anchors.yml: WP§11.4
  ⚠ section not in anchors.yml: WP§11.4
  ⚠ section not in anchors.yml: WP§11.4
  ⚠ section not in anchors.yml: WP§11.4
  ⚠ section not in anchors.yml: WP§11.11
  ⚠ section not in anchors.yml: WP§11.4
  ⚠ section not in anchors.yml: WP§11.10
  ⚠ section not in anchors.yml: WP§11.6
  ⚠ section not in anchors.yml: GOV§10
  ⚠ section not in anchors.yml: WP§11
  ⚠ section not in anchors.yml: WP§11
  ⚠ section not in anchors.yml: MF§3.5
  ⚠ section not in anchors.yml: MF§9.6
  ⚠ section not in anchors.yml: GOV§11.1
  ⚠ section not in anchors.yml: MF§9.7
  ⚠ section not in anchors.yml: MF§9.7
  ⚠ section not in anchors.yml: MF§E.2
  ⚠ section not in anchors.yml: MF§9.8
  ⚠ section not in anchors.yml: MF§9.9
  ⚠ section not in anchors.yml: GOV§9
  ⚠ section not in anchors.yml: GOV§9
  ⚠ section not in anchors.yml: GOV§10
  ⚠ section not in anchors.yml: GOV§8.3
  ⚠ section not in anchors.yml: VAL§8.4
  ⚠ section not in anchors.yml: VAL§8.4
  ⚠ section not in anchors.yml: VAL.B§1
  ⚠ section not in anchors.yml: VAL.B§2
  ⚠ section not in anchors.yml: VAL.B§5
  ⚠ section not in anchors.yml: VAL§J
  ⚠ section not in anchors.yml: VAL§8.4
  ⚠ section not in anchors.yml: VAL§8.4
  ⚠ section not in anchors.yml: VAL§G
  ⚠ section not in anchors.yml: GOV§8.5
  ⚠ section not in anchors.yml: GOV§8.3
  ⚠ section not in anchors.yml: GOV§9.3
  ⚠ section not in anchors.yml: VAL§8.4
  ⚠ section not in anchors.yml: GOV§8.5
  ⚠ section not in anchors.yml: GOV§9.3
  ⚠ section not in anchors.yml: VAL.B§5.2
  ⚠ section not in anchors.yml: VAL.B§5.2
  ⚠ section not in anchors.yml: VAL.B§5.2
  ⚠ section not in anchors.yml: VAL.B§5.2
  ⚠ section not in anchors.yml: VAL.A§I
  ⚠ section not in anchors.yml: CORP§B.2
  ⚠ section not in anchors.yml: GOV§11.1
  ⚠ section not in anchors.yml: GOV§10
  ⚠ section not in anchors.yml: GOV.A§4
  ⚠ section not in anchors.yml: GOV§10
  ⚠ section not in anchors.yml: GOV§10
  ⚠ section not in anchors.yml: GOV§9
  ⚠ section not in anchors.yml: GOV§10
  ⚠ section not in anchors.yml: GOV§8.3
  ⚠ section not in anchors.yml: GOV.B§I
  ⚠ section not in anchors.yml: GOV.B§I
  ⚠ section not in anchors.yml: GOV§6.2.3
  ⚠ section not in anchors.yml: GOV§10
  ⚠ section not in anchors.yml: GOV§6.2.3
  ⚠ section not in anchors.yml: GOV§6.2.2
  ⚠ section not in anchors.yml: GOV§6.2.2
  ⚠ section not in anchors.yml: GOV§8.3
  ⚠ section not in anchors.yml: GOV§8.3
  ⚠ section not in anchors.yml: GOV§8.8
  ⚠ section not in anchors.yml: GOV§8.3
  ⚠ section not in anchors.yml: GOV§8.4
  ⚠ section not in anchors.yml: GOV§9.1
  ⚠ section not in anchors.yml: GOV§9.3
  ⚠ section not in anchors.yml: GOV§10
  ⚠ section not in anchors.yml: GOV§10.3
  ⚠ section not in anchors.yml: GOV§10.3
  ⚠ section not in anchors.yml: GOV§8.7
  ⚠ section not in anchors.yml: RATES§7.5
  ⚠ section not in anchors.yml: RATES§D
  ⚠ section not in anchors.yml: RATES§D
  ⚠ section not in anchors.yml: RATES.A§B.3a
  ⚠ section not in anchors.yml: RATES.A§B.3i
  ⚠ section not in anchors.yml: RATES.A§B.3h
  ⚠ section not in anchors.yml: RATES.A§B.3a
  ⚠ section not in anchors.yml: GOV§10
  ⚠ section not in anchors.yml: GOV§8.8
  ⚠ section not in anchors.yml: GOV§10
  ⚠ section not in anchors.yml: GOV§8.8
  ⚠ section not in anchors.yml: GOV§8.6
  ⚠ section not in anchors.yml: MF§9.4.9
  ⚠ section not in anchors.yml: GOV.B§E.9
  ✓ model_v1/sweeps_core.py → _build/model/sweeps_core.py (runtime)
  ✓ model_v1/val_core.py → _build/model/val_core.py (runtime)
  ✓ model_v1/wfr_core.py → _build/model/wfr_core.py (runtime)
  ✓ model_v1/ldw_core.py → _build/model/ldw_core.py (runtime)
  ✓ model_v1/19_2_WFR_tables.py → _build/model/19_2_WFR_tables.py (runtime)
  ✓ model_v1/wdt_fmt.py → _build/model/wdt_fmt.py (runtime)
  ✓ model_v1/8_2_RATES_tables.py → _build/model/8_2_RATES_tables.py (runtime)
  ✓ model_v1/16_1_SWEEPS_V_tables.py → _build/model/16_1_SWEEPS_V_tables.py (runtime)
  ✓ model_v1/5_3_VAL_tables.py → _build/model/5_3_VAL_tables.py (runtime)
  ✓ model_v1/wdt_analytics.py → _build/model/wdt_analytics.py (runtime)
  ✓ model_v1/rates_core1.py → _build/model/rates_core1.py (runtime)
  ✓ model_v1/19_3_WFR_charts.py → _build/model/19_3_WFR_charts.py (runtime)
  ✓ model_v1/wdt_style.py → _build/model/wdt_style.py (runtime)
  ✓ model_v1/16_3_SWEEPS_R_tables.py → _build/model/16_3_SWEEPS_R_tables.py (runtime)
  ✓ model_v1/wdt_md.py → _build/model/wdt_md.py (runtime)
  ✓ model_v1/5_5_VAL_generate_worked_examples.py → _build/model/5_5_VAL_generate_worked_examples.py (runtime)
  ✓ model_v1/16_4_SWEEPS_R_charts.py → _build/model/16_4_SWEEPS_R_charts.py (runtime)
  ✓ model_v1/wdt_core.py → _build/model/wdt_core.py (runtime)
  ✓ model_v1/5_4_VAL_charts.py → _build/model/5_4_VAL_charts.py (runtime)
  ✓ model_v1/WDT_Params.toml → _build/model/WDT_Params.toml (runtime)
  ✓ model_v1/8_3_RATES_charts.py → _build/model/8_3_RATES_charts.py (runtime)
  ✓ model_v1/16_2_SWEEPS_V_charts.py → _build/model/16_2_SWEEPS_V_charts.py (runtime)
  ✓ model_v1/test_wdt_style.py → _build/model/test_wdt_style.py (runtime)
  ✓ model_v1/test_wdt_md.py → _build/model/test_wdt_md.py (runtime)
  ✓ model_v1/test_wdt_fmt.py → _build/model/test_wdt_fmt.py (runtime)
  ✓ model_v1/test_wdt_analytics.py → _build/model/test_wdt_analytics.py (runtime)
  ✓ Copied image outputs → _build/figures/ (95 files)
  ✓ Generated corpus.qmd (33 papers, 6 reading paths)
  ✓ Generated references.qmd (177 entries, 0 pending)
  ✓ WDT_Flowchart_LR.png (cached, 608,413 bytes)
  ✓ WDT_Skeleton_LR.png (cached, 142,966 bytes)
  ✓ UK_Tax_Flowchart_LR.png (cached, 1,074,013 bytes)
  ✓ UK_Skeleton_LR.png (cached, 442,928 bytes)
  ✓ WDT_Bidirectional_LR.png (cached, 20,655 bytes)
  ✓ Generated flowcharts.qmd (5 diagrams, side-by-side layout)
  [link_map] wrote /home/claude/wealthdeltatax/_build/link-map.qmd (31 papers)
  ✓ tools/taxpayer_calc.html → _build/model/taxpayer.qmd
  ✓ tools/revenue_calc.html → _build/model/revenue.qmd
  ✓ tools/ldw_calc.html → _build/model/ldw.qmd
  ✓ references.json → references.json
  ✓ anchors.yml → anchors.yml
  ✓ contents.yml → wdt-contents.yml
  ✓ references.bib → references.bib
  ✓ Generated site-index.json (33 papers, 1304 anchors, 1337 search records)
  ✓ 1_Wealth_Delta_Tax_Whitepaper.md → wp.qmd
  ⚠ section not in anchors.yml: MF§9.4.9
  ✓ 2_Moral_and_Philosophical_Foundations.md → mf.qmd
  ✓ 3a_Research_Gaps.md → lr-a.qmd
  ✓ 3b_Intellectual_Background.md → lr-b.qmd
  ⚠ section not in anchors.yml: GOV.B§A.3.7
  ✓ 4_UK_Jurisdiction_and_Data_Reference_Paper.md → jur.qmd
  ✓ 5_Valuing_Wealth.md → val.qmd
  ✓ 5a_Valuing_Wealth_Mathematical_and_Simulation_Appendix.md → val-a.qmd
  ✓ 5b_Valuing_Wealth_Worked_Examples_Appendix.md → val-b.qmd
  ✓ 6_Corporate_Architecture.md → corp.qmd
  ✓ 6a_Corporate_Architecture_Appendix.md → corp-a.qmd
  ⚠ section not in anchors.yml: GOV.B§E.9
  ⚠ section not in anchors.yml: GOV.B§E.9
  ⚠ section not in anchors.yml: GOV.B§E.9
  ✓ 7_Constitutional_Governance.md → gov.qmd
  ✓ 7a_WDT_Constitutional_Governance_Intellectual_Appendix.md → gov-a.qmd
  ⚠ section not in anchors.yml: GOV.B§E.8
  ⚠ section not in anchors.yml: GOV.B§E.9
  ⚠ section not in anchors.yml: GOV.B§C.8
  ⚠ section not in anchors.yml: GOV.B§E.9
  ⚠ section not in anchors.yml: GOV.B§E.8
  ⚠ section not in anchors.yml: GOV.B§E.8
  ⚠ section not in anchors.yml: GOV.B§E.9
  ⚠ section not in anchors.yml: GOV.B§E.9
  ⚠ section not in anchors.yml: GOV.B§E.8
  ⚠ section not in anchors.yml: GOV.B§E.8
  ✓ 7b_Constitutional_Governance_Operational_Appendix.md → gov-b.qmd
  ✓ 8_Rates_and_Revenue.md → rates.qmd
  ✓ 8a_Rates_and_Revenue_Appendix.md → rates-a.qmd
  ⚠ section not in anchors.yml: GOV§E.2
  ✓ 9_Parameter_Sweeps.md → sweeps.qmd
  ✓ 9a_Parameter_Sweeps_Appendix.md → sweeps-a.qmd
  ✓ 10_Behavioural_Robustness_and_Administrative_Experience.md → behav.qmd
  ✓ 10a_Behavioural_Robustness_and_Administrative_Experience_Appendix.md → behav-a.qmd
  ✓ 11_Position_Closure.md → close.qmd
  ✓ 12_Political_Architecture.md → pol.qmd
  ✓ 12a_Political_Architecture_Appendix.md → pol-a.qmd
  ✓ 13_Phase_One.md → phase1.qmd
  ✓ 14_Environmental_Effects_and_Transmission_Channels.md → env.qmd
  ✓ 15_First_Mover.md → fm.qmd
  ✓ 16_Modular_Adoption.md → mod.qmd
  ⚠ section not in anchors.yml: GOV.B§A.3.7
  ⚠ section not in anchors.yml: GOV.B§A.3.7
  ✓ 17_Scope_Boundary.md → scope.qmd
  ⚠ section not in anchors.yml: GOV.B§A.3.7
  ✓ 18_Addendums.md → add.qmd
  ✓ 19_Taxpayer_Welfare.md → wfr.qmd
  ✓ 19a_Taxpayer_Welfare_Appendix.md → wfr-a.qmd
  ✓ 20_Institutional_Selection.md → inst.qmd
  ✓ 21_Labour_Dividend_Welfare.md → ldw.qmd
  ✓ 22_Falsification_Hypotheses.md → fal.qmd

Done. 33 papers staged, 0 not available.
Run: quarto render /home/claude/wealthdeltatax/_build
- **Not run:** the Action after merge (not merged); a real Pyodide run in a browser (the CDN is unreachable from the sandbox); revenue calculator results (cannot run before or after).
- **State:** pushed  on .
<!-- progress:end -->

### Change report


