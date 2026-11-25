# Household-flow refactor: plan

- **Status:** agreed in outline by the author, 2026-11-21 (Scenario B). Phases 1 and 2 are briefed; later phases are written after the one before reports.
- **Why:** the v3 kernel has one household term, the drawdown `c` (I-D14c, 3.5%). It compresses income, consumption and saving into a rate on the whole stock, so wealth is never replenished. In 090c, wealth/GDP falls to 47% of its start by year 100 (62% with the tax off) and receipts collapse (083c). The 3.5% began as a v2 steady-state device (D16), became a "consumption share" in the register, and was never tested against the steady state it was for. Findings: `research/notes/093r`, `094r`, `095r`, `096r`.
- **What we solve:** a coherent untaxed baseline from household income, saving, returns and consumption, with WDT assessed on top by the existing mechanisms. Not a fiscal outcome; either direction of the effect on WDT is open. 3.5% stays only as a labelled legacy comparator.
- **Scenario B (author):** cells of wealth band by life stage; saving specified on the income side; where no UK range exists the parameter is **unset** or run as a **labelled judgement scenario**; no universal scalar.

## Phases
| # | Phase | Output | Status |
|---|---|---|---|
| 1 | **Collect** every reachable source, and confirm what is not reachable (what the author must upload) | 097r open series; 098r WAS published tables and population; 099r held PDFs extracted to a moments table; 100r JST cash-yield and gain split | briefed |
| 2 | **Parameter map** (guru): per cell and flow, what is data, unset, scenario; resolve the 096r open questions with the author | one table plus rulings | after phase 1 |
| 3 | **Household step first** (code): one function behind the five `(1+g)(1-c)` sites, legacy mode reproducing today's digests exactly; no behaviour change | code brief | after 2 |
| 4 | **Pack additions** (code): cash-yield/gain table, income, stage weights, whatever phase 1 found | code brief | after 2 |
| 5 | **Cell model** (code): cells, transitions, public-side unification, new outputs; legacy arm kept | code briefs (split by layer) | after 3 and 4 |
| 6 | **Validation** against WAS moments, then **comparison** of arms with attribution | briefs | after 5 |

Held until phase 2 is ruled on: 089c (feasibility rule), 057c (run script; it labels its run legacy).

## Rules for the collection briefs
- Agents reach sources by web search and fetch only; the shell cannot download. Binary files (xlsx, ods, pdf, microdata) that a fetch cannot parse are **logged as unreachable with the exact file and link**, and the author uploads them to `literature/`.
- Every number has a source, page or table, and a definition, and is checked against the held file where one is held. A number read from a search summary is marked as such and is not evidence for a parameter.
- No value is chosen for its effect on revenue, and no band-level rate is inferred where the data do not give one.
