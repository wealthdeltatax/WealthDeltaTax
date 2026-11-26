# 175: Complete the retired-tax series from the held IFS workbook

- **Status:** ready; Agent 6 (needs a shell; research and a small script)
- **Author/date:** K. Ogata with the guru, 2026-11-26
- **Depends on:** 174r (merged in part)
- **Read:** `research/notes/174r-retired-tax-trends.md` and `research/tables/174r-evidence/retired-tax-gdp-annual.csv` (the partial result), `project/agents/agent-research.md`, `literature/readable/data/rates/Revenue composition spreadsheet.xlsx.md` (reading copy, to find the sheets; quote numbers from the xlsx, not the copy)

## Goal
174r stopped at 2018-19 and with no annual business rates or IHT because the agent had no shell and the OBR download returned 403. The data are already held: `data/rates/Revenue composition spreadsheet.xlsx` (IFS, "Composition of UK revenue"). Its `% GDP (cash)` sheet gives, for 1978-79 to 2027-28 (50 years), corporation tax, capital gains tax, inheritance tax, stamp duties, stamp taxes on shares, business rates, council tax and total HMRC as a share of GDP. Its `% GDP (national accounts)` sheet runs from 1999-00 to 2027-28. Replace the partial 174r series with the full ones, computed by a script.

## Decisions (author, 2026-11-26)
- "Stamp duty" means **both** property transaction taxes and share stamp taxes; carry them as separate columns and as a sum.
- Keep the proposed axes from 174r: wealth to GDP drift of 0.5% a year; growth effect of 0.05 points a year per 1% of GDP switched (still labelled axis candidates).
- No recommendation on retired-tax indexing; fixed share of GDP stays, a switch (following household wealth) is a later design.

## Blocks (one push each)
- **Block 0:** progress block pushed.
- **Block 1:** `research/tables/174r-evidence/retired-tax-gdp-annual-full.csv` and the script `research/tables/174r-evidence/retired_tax_series.py`: for each of the six taxes (and the two stamp components, and total HMRC) the cash and the national-accounts annual share of GDP, with sheet, row label, a flag (`outturn` or `forecast`, from the sheet's own row 2 labels; forecasts from OBR EFO March 2023 and later) and the source file path. `python -I research/tables/174r-evidence/retired_tax_series.py` must regenerate the CSV byte for byte. Check the 2007-08 to 2018-19 values against the 174r OBR WP15 values and report any difference above 0.1 point.
- **Block 2:** rewrite `research/notes/174r-retired-tax-trends.md` section 3 and the summary from the full series: per tax the level, trend, volatility (standard deviation of annual changes), the correlation of each tax's share of GDP with the ratio of the house price index and the equity index to GDP where those are held (`data/`; else say not held), and the plain comparison the author asked for: has each tax held steady, risen or fallen as a share of GDP over 1978 to 2025, and how large are the swings, in a table. State plainly what this does and does not say about fixed share of GDP versus wealth-following. Remove the data-request paragraphs that are now answered. Run `python -I project/tools/check_agent_docs.py` (exit 0).
- **Block 3:** change report; push; stop.

## Touches
`research/tables/174r-evidence/`, `research/notes/174r-retired-tax-trends.md`, this brief. Read-only on `data/`. No model, register, pack or bibliography change.

## Acceptance criteria
Full annual series for all six taxes with flags and sheet references; the script regenerates the CSV; the overlap check with 174r is reported; the note's indexation paragraph states the evidence without a recommendation; checker exits 0.

## Out of scope
The retired-tax indexing switch itself, the OBR workbook (not needed now), anything in the model.

## Open questions
If a row label is ambiguous (e.g. "Stamp duties" before and after 1999-00, which the sheet notes say is an aggregate before 1999-00), keep the sheet's own note in the CSV and ask the author only if the series cannot be joined.

## Implementation notes
<!-- progress:start -->
- **Done:** blocks 0 to 3; criteria met; merged by the auto-merge rule (see the change report).
- **Next:** guru retires the brief.
- **Resume:** none
<!-- progress:end -->

## Change report
```
Change report
- Task: 175r complete the retired-tax series from the held IFS workbook
- Files changed: research/tables/174r-evidence/retired_tax_series.py (new: workbook to CSV); retired-tax-gdp-annual-full.csv (new, 719 rows); retired-tax-overlap-174r.csv (new, 106 comparisons); retired_tax_stats.py (new: level, trend, volatility, correlations); retired-tax-stats.csv (new, 20 series); research/notes/174r-retired-tax-trends.md (summary, section 3, evidence paragraph in 5, sections 6 to 8 rewritten; section 2 and 4 kept); this brief
- What is different now: the retired-tax shares of GDP are complete for 1978-79 to 2027-28 (cash) and 1999-00 to 2027-28 (national accounts), with outturn or forecast flags, sheet, row, label and the sheet's own footnotes; the note states level, trend, volatility and the correlation with house and equity prices from them
- New or changed interfaces: `python -I research/tables/174r-evidence/retired_tax_series.py`, then `retired_tax_stats.py`; both regenerate their CSVs byte for byte (run twice, md5 equal)
- Acceptance criteria: full annual series for the six taxes with flags and sheet references (met; also onshore corporation tax, both stamp components, total HMRC); script regenerates the CSV (met); overlap with 174r reported (met: 106 comparisons, 13 differ by more than 0.1 point: onshore corporation tax 9 of 12 years on the cash basis and 2 of 12 on the national-accounts basis (max 0.25 and 0.16), business rates 2024-25 (1.1 against 1.33; 0.22)); indexation paragraph states the evidence without a recommendation (met); checker exits 0 (met)
- Deviations from the brief: statistics use outturn years only, 1978-79 to 2020-21 (the sheet flags 2021-22 onwards as forecast), not "to 2025"; a sum of the six taxes is added as a series; the two stamp components exist only from 1999-00 (blank in the sheet, kept blank)
- Risks / follow-ups: correlations use JST release 6 (ends 2020, nominal house price index, no policy-break indicators) and are descriptive; cash and national-accounts corporation tax differ by up to 0.53 points in a year and are kept apart; the 174r council tax values were Great Britain receipts, the workbook's are the sheet's UK series
- Instruction friction: none (asked: nothing in the guide, the brief or the tools failed; the git remote reports that the repository moved to wealthdeltatax/WealthDeltaTax, a notice only)
- Verification: both scripts run twice with equal md5; `check_agent_docs.py` exit 0; the numbers in the note's tables were compared with `retired-tax-stats.csv` by hand (rounding only); not run: Quarto build (not touched)
- Overview sections likely needing an update: none
- Commit / branch: brief/175r-complete-retired-tax-series; brief 175r merged, ready to retire
```
