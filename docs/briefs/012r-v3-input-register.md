# 012: Model v3 input register

- **Status:** ready
- **Author/date:** K. Ogata with the guru, 2026-11-16
- **Depends on:** 011g stages A and A2 (both passed)
- **Read:** `docs/model-v3/drivers.md` (sections 2 and 4), the input names in `docs/model-v3/metrics.md`, `docs/model-audit/synthesis.md` section 9 (data held and data to get), `docs/agents/research.md` and the three files in `docs/agents/reference/research/`. Nothing else need be opened.

## Goal
Give model v3 a sourced range for every input that moves the headlines, so the guru can run the tornado and stage C can fix the architecture. This brief finds and cites data; it does not choose model values, build code or edit papers.

## Decisions (author, 2026-11-16)
- UK only. Everything country-specific goes into one data pack later; record what each source covers outside the UK (R11) in one short note.
- Every ranged input has a low, central and high value, a unit and a cited source. The rate schedule and the threshold are levers, not research inputs (drivers D2, D3).
- Tier 1 inputs are sourced fully; tier 2 inputs get one documented range and no further sourcing (`drivers.md` section 4). Tier 1: returns and loss years (D1), wealth distribution and tail (D4), behavioural response (D5), retired-tax incidence (D6), income and liquid assets by wealth band (D9), house-price response (D10). Tier 2: corporate levy base (D7), reserve rule (D8), discount schedule (D11).
- No hand-picked scenarios: each low and high states how it was set (observed spread, published interval, or a stated judgement, flagged as judgement).
- Discount rate: the HM Treasury Green Book schedule (3.0% to year 30, 2.5% to year 75, 2.25% to year 125, October 2026 revision), checked against the Green Book text; the previous 3.5% and 3.0% schedule as the sensitivity.
- Comparators: the Zucman global minimum tax (2% above about £1bn), UK wealth tax proposals of about 2%, and today's CGT, IHT and income tax for the same people.

## Design
One file, `docs/model-v3/inputs.md`, built up over four sessions. One table per tier. Row fields, all required:

| Field | Content |
|---|---|
| ID | `I-` plus the driver, for example `I-D4a` |
| Input | name and what it feeds (metric IDs) |
| Unit | with base year for money |
| Low, central, high | numbers |
| How the range was set | observed spread, published interval, or judgement |
| Source | author, year, table or page, URL |
| Licence and access | can the data be redistributed or only cited; flag any restriction |
| Coverage | years and geography; one line on coverage outside the UK |
| In repo | path if already held (`synthesis.md` section 9) |
| Confidence | high, medium or low, with one line of reason |

Evidence rules (`research.md`): primary sources first, date accessed for each, paraphrase and never paste long passages, state conflicts and gaps. Foreign evidence (for example Norway for avoidance and migration) is allowed where no UK evidence exists, flagged with the country and one line on transferability; the author can overrule. Add nothing to `registry/references.bib` or `internal.json`: keep full references in `inputs.md` and the change report will ask the author which to add.

## Touches
New `docs/model-v3/inputs.md`; research notes under `docs/research/` if needed; nothing in `registry/`, `source/`, `model_v1/`, `model_v2/` or `pipeline/`.

## Stages
- **B1: wealth, income and returns** (D4, D9, D1). Checkpoint: `inputs.md` tier 1 sections for these pushed. Check: wealth-to-GDP, the share of wealth and of adults above W_min (half the median house price), the tail source and its licence, income and liquid assets by wealth band, and UK real return statistics (mean, spread, loss-year frequency, longest run, gap to the latest year) all have every field. The latest ONS Wealth and Assets Survey wave is named; if it cannot be used, the 2016-18 wave in the repo is the fallback and is flagged.
- **B2: behaviour, incidence, capitalisation** (D5, D6, D10). Checkpoint: the matching `inputs.md` sections pushed. Check: avoidance, migration and valuation understatement each have a range; incidence of each of the six retired taxes by income decile (stamp duties as property and shares), each tax's deciles summing to 100% within a stated tolerance; the house-price response to retiring stamp duty and council tax has a range or is stated as having no usable evidence.
- **B3: comparators** (M5, M6, M8 inputs). Checkpoint: pushed. Check: the Zucman proposal and the UK wealth tax proposals each have rate, threshold and a citation; today's CGT, IHT and income tax paid by people above the threshold, by wealth band, from HMRC or ONS; for M8 the strongest published version of CGT at death with no uplift, a proportional property tax after revaluation, and a land value tax, each with rate and revenue estimate and a citation.
- **B4: tier 2 and two checks.** Checkpoint: pushed, with a one-paragraph summary of gaps at the top of `inputs.md`. Check: D7, D8 and D11 each have a documented range; the Green Book schedule is compared with the HM Treasury text and any difference reported; M2 is computed with the metric register's revenue-weighted formula on the data from B1 and compared with the RATES paper's 0.35% (report only: the paper is not edited, and the RATES paper is read by section).
One session finishes one stage and stops. After B4 the guru runs the tornado (`docs/model-v3/tornado.md`); stage C starts after that.

## Acceptance criteria
- Every tier 1 and tier 2 driver D1 to D11 has rows, or a line stating why not (D2 and D3 are levers; D8 is fixed by the papers and recorded).
- Every row has all ten fields; the row count and the count of rows marked judgement are reported, and judgement rows are listed together.
- Every source has a date accessed and a licence note; every redistribution restriction is listed.
- The tail dataset is named with its licence.
- The M2 check and the Green Book check each report a number or a stated difference.
- `git diff --stat` shows only the Touches list.

## Checks to run
A one-line script that parses the tables in `inputs.md` and fails on any empty cell; a count of rows per driver; `git diff --stat`. No model code is run.

## Out of scope
Choosing the values the model uses, running the tornado, building code, editing papers, editing the bibliography, other countries' data beyond the one-line coverage note, and the rate schedule and threshold.

## Open questions
1. If the Sunday Times Rich List licence blocks reuse, which tail is the fallback (Advani, Bangham and Leslie top shares, HMRC, or a fitted Pareto)? Report the options with licences; the author chooses.
2. Which foreign evidence is acceptable where UK evidence on avoidance and migration is missing? Proposed: any peer-reviewed or official source, flagged with its country; the author can narrow it.
3. Whether the author wants the cited references added to `registry/references.bib` after B4.

## Implementation notes
<!-- progress:start -->
- **Done:**
- **Next:** B1
- **Decisions:**
- **Gotchas:**
- **Resume:**
- **Not run:**
- **State:** ready, not started
<!-- progress:end -->
