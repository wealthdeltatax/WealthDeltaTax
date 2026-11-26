# 174: Evidence for the SWF redesign: wealth to GDP, saving by wealth class, growth effect, retired-tax trends

- **Status:** ready (research only; no code; feeds the SWF redesign specification after the model speed-ups)
- **Author/date:** K. Ogata with the guru, 2026-11-26
- **Depends on:** nothing; read-only on the model and pack
- **Read (block 0: the first two only):** (1) `project/decisions.md`, the entries of 2026-11-25 on the SWF layers, the capped fund and the retired-tax question; (2) `project/agents/agent-research.md`. Later: `results/reserve-diagnostic/`, `model-specs/household-arm-paths.md`, `research/notes/145r-withdrawal-and-saving-evidence.md`, `research/notes/146r-*.md` (do not redo them)

## Goal
Give the author evidence ranges, not a central forecast, for four questions the SWF redesign depends on. Every figure has a source page and a flag; every range is labelled as a scenario axis candidate.

## Questions
1. **Wealth to GDP.** UK household net wealth relative to GDP over time (ONS, Bank of England, JST, Piketty-Zucman, Advani-Summers): level, trend and variation over 1900 to now; the share that is financial (taxable returns) versus housing and pensions. The author expects wealth to outgrow GDP; the guru's scratch run showed it is scenario-dependent (the median-saving scenario had M1a falling from 2.9% to 1.6% of GDP). Evidence for and against, with ranges for the long-run drift of the wealth-to-GDP ratio.
2. **Saving by wealth class.** Saving rates and wealth accumulation by wealth decile or class (WAS, ONS savings ratios; top-1% tail evidence from 146r), so the household arm's saving assumption can be bracketed. What spread across classes is defensible?
3. **Growth effect of replacing taxes.** The author's hypothesis is that raising equal revenue with the WDT in place of the taxes it displaces raises productivity and growth. Evidence on the growth effects of the phase-one taxes (corporation tax, council tax, business rates, CGT, stamp duty, IHT) and of wealth-based taxation: ranges for the effect on GDP growth per percentage point of GDP of revenue switched (e.g. OECD, IFS Mirrlees Review, Arnold et al., Akcigit, Kleven; the literature in `literature/`). Give a low, a zero and a high setting; mark which are model-based and which are empirical; say plainly where evidence is weak.
4. **Retired-tax trends.** Each of the six phase-one taxes as a share of GDP, annual series for as long as the held data allow (`data/`, OBR and ONS public finances tables): level, trend, volatility, and how each moves with house prices and asset prices. The author's open question: if a retired tax is held at a fixed share of GDP, is that a fair comparison with a WDT that follows household wealth? Say what the history implies for the retired-tax indexing switch (fixed share of GDP versus following wealth), with ranges, not a recommendation.

## Blocks (one push each; `project/agents/agent-research.md`)
- **Block 0:** progress block pushed.
- **Block 1:** questions 1 and 2: `research/notes/174r-wealth-saving-evidence.md` with CSVs in `research/tables/174r-evidence/`.
- **Block 2:** question 3: `research/notes/174r-growth-effect-evidence.md`.
- **Block 3:** question 4: `research/notes/174r-retired-tax-trends.md` with the series CSV and a small chart-ready table (share of GDP by year per tax).
- **Block 4:** change report with the open rulings for the author; push; stop.
**Stop rule.** No model, register, manifest or pack change. After four blocks or a quarter of the budget left, push and list the rest. A file that cannot be fetched is a data request for the author, not a finding.

## Touches
New: `research/notes/174r-*.md`, `research/tables/174r-evidence/`. Read-only use of `model/`, `data/`, `literature/`. Nothing in `literature/references.bib` or `internal.json` without the author's confirmation (list proposed additions instead).

## Acceptance criteria
Every figure has a page or table and a flag; every range is labelled low, central-for-illustration, high and as an axis candidate; weak or conflicting evidence is stated; computations are reproducible with a command; open rulings are listed; `check_agent_docs.py` exits 0.

## Out of scope
Any model change, forecasting, a recommendation on the retired-tax switch, the SWF specification itself.

## Open questions
Ask the author before adding any source to the bibliography.

## Implementation notes
<!-- progress:start -->
- **Done:** nothing yet.
- **Next:** block 0.
<!-- progress:end -->

## Change report
(The agent fills this in.)
