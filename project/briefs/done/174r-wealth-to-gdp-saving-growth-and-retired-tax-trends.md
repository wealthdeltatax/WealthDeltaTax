# 174: Evidence for the SWF redesign: wealth to GDP, saving by wealth class, growth effect, retired-tax trends

- **Status:** done, retired 2026-11-26
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
- **Done:** blocks 0–4 (three research notes, two evidence CSVs, change report and author handoff).
- **Next:** author supplies/approves the missing receipts data route and guru runs local validation. No merge until the incomplete criteria are resolved.
- **Resume:** `brief/174r-wealth-saving-growth-tax-trends`; read the change report and block-3 data requests before continuing.
- **Resume:** `brief/174r-wealth-saving-growth-tax-trends`; read the progress block and the note before continuing.
- **Resume:** `brief/174r-wealth-saving-growth-tax-trends`; read this progress block and the three note skeletons before continuing.
<!-- progress:end -->

## Change report
## Change report

Change report
- Task: 174r, Evidence for the SWF redesign: wealth to GDP, saving by wealth class, growth effect, retired-tax trends.
- Files changed:
  - research/notes/174r-wealth-saving-evidence.md — historical wealth/GDP evidence, wealth composition, saving-by-class evidence boundary, scenario candidates and limitations.
  - research/tables/174r-evidence/wealth-saving-evidence.csv — source-flagged published observations and selected aggregate saving-ratio values.
  - research/notes/174r-growth-effect-evidence.md — six-tax and wealth-tax growth literature, evidence-type matrix, low/zero/high model sensitivity.
  - research/notes/174r-retired-tax-trends.md — annual OBR receipts series for four taxes, latest endpoints/trend evidence for business rates and IHT, indexation comparison and data requests.
  - research/tables/174r-evidence/retired-tax-gdp-annual.csv — exact OBR annual observations plus clearly flagged trend-only and endpoint rows.
  - project/briefs/open/174r-wealth-to-gdp-saving-growth-and-retired-tax-trends.md — progress and this report.
- What is different now: the SWF redesign has evidence ranges rather than a single wealth-growth forecast; the absence of UK saving rates by wealth class is explicit; the growth dividend is a scenario rather than an empirical coefficient; the fixed-GDP versus wealth-linked retired-tax comparison is framed without overriding the author's 26 November ruling.
- New or changed interfaces: none.
- Acceptance criteria:
  - Every figure has a source page/table and flag: met for figures included in the notes; no unsupported annual values were imputed.
  - Every range is labelled low, central-for-illustration and high, and as an axis candidate: met for the wealth/GDP drift and growth-effect sensitivity.
  - Weak or conflicting evidence stated: met.
  - Computations reproducible with a command: partly met. Arithmetic formulae and source tables are named, but the full annual tax series and wealth/GDP extraction are not locally reproduced.
  - Open rulings listed: met.
  - check_agent_docs.py exits 0: not run; no local checkout/shell was available.
- Deviations from the brief:
  - Block 3 annual receipts series is incomplete for business rates and IHT; stamp taxes are combined at the available HMRC endpoints. OBR historical public-finances workbook returned HTTP 403; HMRC ODS annual receipts table was not fetched. This is a data-access limitation, not a claim that the series do not exist.
  - No model, register, manifest, pack, bibliography or internal reference database changes.
- Risks / follow-ups:
  - Author to provide the OBR historical public-finances workbook and/or HMRC ODS table, or a local checkout, to complete the missing annual tax series and run the checker.
  - Decide whether “stamp duty” means property transaction taxes, share stamp taxes, or both.
  - Decide whether to retain ±0.5% annual wealth/GDP drift and ±0.05 percentage-point annual GDP-growth effect per 1% GDP switched as the core sensitivity axes.
  - No recommendation made on fixed-GDP versus wealth-linked retired-tax indexing; the existing fixed-GDP ruling is preserved.
- Instruction friction: none. The author explicitly authorised continuing with external research and GitHub markdown/CSV writes despite the absence of a local shell; no workflow rule was silently bypassed.
- Verification: GitHub writes succeeded on the task branch. External sources checked include ONS, OSR, OBR, HMRC, OECD, IFS, HMRC/OBR and peer-reviewed papers. Local scripts, repository tests, and project/tools/check_agent_docs.py not run.
- Overview sections likely needing an update: none until the author accepts the remaining data limitations and the guru reviews the findings.
- Commit / branch: branch brief/174r-wealth-saving-growth-tax-trends; report commit 4bd0a1fc91b906a595447d682cd0427f848867ca; branch remains ahead of main. Not merged.

**NEEDS THE AUTHOR** — the data completeness and local checker acceptance criteria remain unmet.

