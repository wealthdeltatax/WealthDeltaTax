# 099: Extract the moments from the research already held

- **Status:** ready
- **Author/date:** K. Ogata with the guru, 2026-11-21
- **Depends on:** none
- **Read:** `docs/model-v3/household-flow-plan.md`; `docs/research/095r-bozio-2013-reading.md` (done by the guru; do not redo); `docs/research/096r-cohort-cell-design.md` section 5 (the validation moments); `docs/research/095r-uk-household-flow-evidence-map.md`.

## Goal
Read the PDFs in `Research/` that bear on household wealth flows, and extract each usable **moment** with its page, so phase 2 can set cell parameters and validation targets from numbers checked against the file.

## Decisions (author, 2026-11-21)
Same as 097r. Scenario B. A moment is not a parameter: record it, do not set anything.

## Design
Read in full the files that bear on the topic: `Before-the-fall.pdf` (passive and active by group, annex tables), `Fiscal Studies - 2021 - Advani - Behavioural responses to a wealth tax.pdf`, `Summers 2023 (OxREP).pdf`, `TippetZucman2026.pdf`, `Koster_How-do-households_Author.pdf`, `1-s2.0-S0014292125001266-main.pdf`, `1475_5890.12286.pdf`, `Adam et al. (IFS).pdf`, `Final_The_IFS_Green_Budget_2025_full_report_amended 2.pdf`, `Effects of taxes and benefits on UK household income financial year ending 2024.pdf`, and any other file in `Research/` that turns out to bear on saving, wealth accumulation, drawdown, transfers or returns by group. Skip those with no bearing and list them with the reason.
1. For each file: what it measures, population, years, definitions (saving, income, wealth, returns), and **each usable number with its page and table**, checked against the file.
2. A **moments table**: flow, source, value, population, years, what it mixes, by band or age or income if given, and whether it can be a **parameter range**, a **validation moment**, or **context only**.
3. For Advani and Summers and Tippet and Zucman: what they say about the saving, returns and capital-gains component of top-tail wealth, and whether any figure is a UK band-level share.
4. Note any wealth or saving evidence cited in these files that is not held and would need uploading.

## Touches
`docs/research/099r-held-research-moments.md` (new), this brief's progress block, `docs/agents/friction-log.md`. No code, pack, register or manifest edits.

## Acceptance criteria
- Every number in the moments table carries a page checked against the PDF; none from a search summary.
- Each moment is classed (parameter range, validation moment, context); none is turned into a saving or depletion rate it does not measure.
- Skipped files are listed with the reason.

## Checks to run
`python -I pipeline/check_agent_docs.py`.

## Out of scope
Fetching anything not held (log it in item 4); choosing parameters.

## Open questions
None.

## Implementation notes
<!-- progress:start -->
- **Done:**
- **Next:**
- **Decisions:**
- **Gotchas:**
- **Resume:**
- **Not run:**
- **State:** ready; not started
<!-- progress:end -->
