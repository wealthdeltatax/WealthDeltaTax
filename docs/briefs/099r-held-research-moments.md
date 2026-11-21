# 099: Extract the moments from the research already held

- **Status:** ready
- **Author/date:** K. Ogata with the guru, 2026-11-21
- **Depends on:** none
- **Read:** `docs/model-v3/household-flow-plan.md`; `docs/research/095r-bozio-2013-reading.md` (done by the guru; do not redo); `docs/research/096r-cohort-cell-design.md` section 5 (the validation moments); `docs/research/095r-uk-household-flow-evidence-map.md`; and, so that nothing is redone or contradicted, `docs/research/097r-open-series-collection.md` (sections 9 and 10) and `docs/research/098r-was-tables-and-population.md` (section 9), which already hold, as checked CSVs in `docs/research/data/097r/` and `098r/`: ONS household flows, saving and the pension split, the national balance sheet, NMG variables, HMRC tables, WAS tables 2.5, 2.11 and 2.13, ONS population and qx, and ETB tables 3b and 4b.

**Runtime.** This brief needs a reader that gives page numbers (pdftotext or equivalent, in a local checkout). If a PDF cannot be read, log the file and stop on it; do not work from a search summary. The first passes of 097r and 098r ran without a reader and reached a wrong conclusion that the guru had to correct.

## Goal
Read the PDFs in `Research/` that bear on household wealth flows, and extract each usable **moment** with its page, so phase 2 can set cell parameters and validation targets from numbers checked against the file.

## Decisions (author, 2026-11-21)
Same as 097r and 098r. Scenario B. A moment is not a parameter: record it, do not set anything. Stage means self-reported retired, not State Pension age; the economically inactive who are not retired are a separate group, never folded into working or retired (098r). A wealth band is stated as either a pack decile band or a WAS £ band, and where a source uses £ bands the 098r band-edge mapping (`was_band_edge_mapping.csv`) says how far it fits the pack.

## Design
Read in full the files that bear on the topic: `Before-the-fall.pdf` (passive and active by group, annex tables), `Fiscal Studies - 2021 - Advani - Behavioural responses to a wealth tax.pdf`, `Summers 2023 (OxREP).pdf`, `TippetZucman2026.pdf`, `Koster_How-do-households_Author.pdf`, `1-s2.0-S0014292125001266-main.pdf`, `1475_5890.12286.pdf`, `Adam et al. (IFS).pdf`, `Final_The_IFS_Green_Budget_2025_full_report_amended 2.pdf`, `Effects of taxes and benefits on UK household income financial year ending 2024.pdf`, and any other file in `Research/` that turns out to bear on saving, wealth accumulation, drawdown, transfers or returns by group. Skip those with no bearing and list them with the reason.
1. For each file: what it measures, population, years, definitions (saving, income, wealth, returns), and **each usable number with its page and table**, checked against the file.
2. A **moments table**: flow, source, value, population, years, what it mixes (state whether pension accrual is included: the ONS saving ratio is roughly half pension, 097r section 9), by band or age or income if given, and whether it can be a **parameter range**, a **validation moment**, or **context only**. Add a column **held as data**: where the same series is already extracted in 097r or 098r (ETB deciles, ONS saving and flows, WAS band tables, NBS stocks), cite that CSV and compare the PDF figure with it, noting any vintage difference (D.42 differed by up to £3.8bn between releases); do not re-extract. The ETB bulletin PDF is the narrative of the ETB tables already extracted, and ranks by income, not wealth. Also list which of the 096r section 5 validation moments (passive and active share, retired financial wealth change, band transition matrix, share with falling wealth) each file supplies.
3. For Advani and Summers and Tippet and Zucman: what they say about the saving, returns and capital-gains component of top-tail wealth, and whether any figure is a UK band-level share.
4. Note any wealth or saving evidence cited in these files that is not held and would need uploading. Exclude what 097r and 098r now hold; what is still not held includes WAS microdata (study 7215), ELSA, decile-exact household-based stage weights and gross debt by wealth band (098r).

## Touches
`docs/research/099r-held-research-moments.md` (new), `docs/research/data/099r/*.csv` (new, the moments table as text, same columns as the note), this brief's progress block, `docs/agents/friction-log.md`. No code, pack, register or manifest edits.

## Acceptance criteria
- Every number in the moments table carries a page checked against the PDF; none from a search summary.
- Each moment is classed (parameter range, validation moment, context); none is turned into a saving or depletion rate it does not measure.
- Skipped files are listed with the reason.
- Each moment says its band scheme, its stage definition and whether it includes pension accrual, or says the source does not state it.
- Where a moment duplicates a series held in 097r or 098r, the held CSV is cited and any difference is stated.

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
