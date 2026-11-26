# 012: Model v3 input register

- **Status:** built (merged 2026-11-17; retired)
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
- **Done:** B1, B2, B3 and B4. 89 rows in `docs/model-v3/inputs.md` (B4 added D7 4, D8 3, D11 4); sources S1 to S43; derivations in `docs/research/012r-b1-` to `-b4-derivations.md`; empty-cell check passed (89 rows, 12 cells each); gaps summary at the top of `inputs.md`.
- **Next:** the guru reviews, runs the tornado (`docs/model-v3/tornado.md`), and decides the two open items below. Stage C after that. Then the author answers open question 3 (add references to `registry/references.bib`).
- **Decisions:** Tail fallback is Advani, Summers, Tarrant 2025 (author, 2026-11-16). B3 and B4 judgement calls as in the change reports. Needs the author: M2's wealth denominator (see the M2 check in `inputs.md` and the new entry in `docs/brief-suggestions.md`).
- **Gotchas:** gov.uk HMRC pages and the Green Book itself were off the fetch allowlist. The branch is behind `main` (013g and restructure files exist there): rebase before any merge.
- **Resume:** `git checkout brief/012-v3-input-register`; nothing left to do in 012r except review.
- **Not run:** no model code (so the M2 path average is a crude proxy); Green Book text not read; ETB decile workbook, Round 9, WTC PDF, Zucman full report, Tax Justice March 2025 paper and Green manifesto not read; no change to `registry/`.
- **State:** all four stages done; NEEDS THE AUTHOR (M2 denominator, branch rebase); not merged
<!-- progress:end -->

### Change report (stage B4)
```
Change report
- Task: 012r stage B4, tier 2 (D7, D8, D11) and the two checks
- Files changed: docs/model-v3/inputs.md (tier 2 rows, sources S41 to S43, M2 check, gaps summary at the top, counts); docs/research/012r-b4-derivations.md (new); docs/brief-suggestions.md (one entry appended); this brief
- What is different now: 89 rows. D7: levy yield 2.77 to 2.88% of GDP (v2 output) against corporation tax 3.37% retired, ratio 0.82 to 0.85; receipts £96.6bn to £101.1bn across three series. D8: multiple 3 (a lever); long reserve fill 6 to 10 years, median 7; short reserve median 3 (no spread). D11: 3.00%, 2.50%, 2.25% for the three bands, previous 3.50%, 3.00%, 2.50% as the sensitivity.
- New or changed interfaces: none
- Acceptance criteria: D7, D8, D11 each have a documented range: met (D7 and D8 ranges come from v2 model output in the repo, not independent sources; the short reserve has a median only). Green Book schedule compared with the HM Treasury text, differences reported: PARTLY MET. Confirmed against the Treasury response (Box 1.A p. 7, para 2.36 p. 15) and the review's Table 1; the Green Book text itself was not reachable. Differences: no effective date given (October 2026 publication), no rate beyond year 125. M2 checked against 0.35%: met as a check, with a finding: 0.35% is tax over terminal wealth, M2 uses start-of-year wealth, and the result moves from 0.39% to about 1.2% (crude) to 4.1% by denominator. Pushed with a gaps summary at the top: met. All fields filled on 89 rows. git diff --stat: inputs.md, the new derivations note, brief-suggestions.md, this brief.
- Deviations from the brief: brief-suggestions.md edited (the AGENTS.md route for a problem outside the brief). RATES read from the repo copy, not the site.
- Risks / follow-ups: M2 denominator is the author's decision; path-average figure needs the model's yearly wealth. T was derived as burden times terminal wealth and does not reproduce the appendix's per-year net tax tables cell by cell (99th percentile Great: 0.39% against 0.46%); cause not found. Branch is behind main.
- Verification: empty-cell parse (89 rows, 12 cells, no empty, no duplicate IDs); replication of the paper's 0.24% (0.243%) and 0.35% (0.361%) in python3 -I; Green Book rates read from two primary PDFs. Not run: no model code, per the brief.
- Overview sections likely needing an update: none (the M2 decision may touch metrics.md, guru only)
- Commit / branch: wip(012): stage B4 done, brief/012-v3-input-register
```

### Change report (stage B3)
```
Change report
- Task: 012r stage B3, comparators (M5 wealth tax proposals, M6 today's CGT, IHT and income tax, M8 reform benchmarks)
- Files changed: docs/model-v3/inputs.md (B3 sections, sources S24 to S40, B3 gaps, counts); docs/research/012r-b3-derivations.md (new, method for derived rows); this brief (progress block, report)
- What is different now: inputs.md holds 78 rows. M5: Zucman global 2% above US$1bn (US$200-250bn), Tippet and Zucman UK 2% above £100m (£10.41bn net 2026), Tax Justice UK 2% above £10m (£24bn), Green Party 1% above £10m and 2% above £1bn (£15bn claimed), Wealth Tax Commission one-off (£260bn), IFS cross-check. M6: IHT 0.056% and CGT 0.144% of the wealth of adults above W_min (central); IHT 0.112% and CGT 0.238% of D10 wealth; IHT effective rates by estate band. M8: CGT alignment £8-12bn, end of uplift £2-2.3bn, property tax rate 0.44-0.81%, LVT 1.28% revenue-neutral.
- New or changed interfaces: none
- Acceptance criteria: Zucman and the UK proposals each have rate, threshold and citation: met. Today's CGT, IHT and income tax paid by people above the threshold, by wealth band, from HMRC or ONS: PARTLY MET. No such series exists; CGT and IHT by band are derived from HMRC liabilities and held ONS wealth (flagged judgement), income tax is not banded (top-income rate and all-household ratio only). M8 strongest published version of each of the three reforms, each with rate, revenue estimate and citation: met for CGT, property tax rate and LVT; property tax revenue is the council tax plus stamp duty base, not a costed net change; no source costs deemed disposal at death. All ten fields on every row: met (78 rows, no empty cell). Rows 78, judgement rows 39 (B3: 12). Redistribution restrictions listed. git diff --stat shows only inputs.md, the new derivations note and this brief.
- Deviations from the brief: the brief file itself was edited for the progress block and report, which earlier stages did too. The CGT 2024-25 totals are from press summaries of HMRC, not the HMRC page.
- Risks / follow-ups: the M6 by-band allocations rest on assumptions (D10 share of CGT 45-100%, £2m-7.5m estate average); a joint wealth and tax file would replace them. Three proposals' revenues are the proponents' own. Branch is behind main; rebase before merge. Open question 3 (add references to references.bib after B4) still for the author.
- Verification: empty-cell parse (78 rows, 12 cells, no empty, no duplicate IDs); rows per driver counted; judgement list reconciled with the table (39); arithmetic for the ratios run in python3 -I and shown in the derivations note. Not run: no model code, per the brief.
- Overview sections likely needing an update: none
- Commit / branch: wip(012): stage B3 done, brief/012-v3-input-register
```

### Change report (stage B2)
```
Change report
- Task: 012r stage B2, behaviour, incidence, capitalisation (D5, D6, D10), plus the S12 reconciliation and the tail decision
- Files changed: docs/model-v3/inputs.md (D5, D6, D10 sections, row I-D4g, sources S13 to S23, gaps and tail decision); docs/research/012r-b2-derivations.md (new, method and script); docs/briefs/012r-v3-input-register.md (progress block and this report)
- What is different now: 22 new rows (41 in total). Foreign-evidence base for D5; council tax capitalisation range for D10; derived decile incidence for the six retired taxes
- New or changed interfaces: none
- Acceptance criteria (B2): avoidance, migration, valuation understatement each have a range (I-D5b, c, d; met, judgement and foreign); incidence of each of the six taxes by decile with stamp duties as property and shares, each summing to 100% within plus or minus 0.1 point (met, but all are derived allocations, not published incidence: partly met); house-price response has a range for council tax (I-D10a, b) and one temporary-holiday point for stamp duty with logical bounds (I-D10c), no usable evidence on a permanent stamp duty retirement (met as stated)
- Deviations from the brief: brief file edited for the progress block and report; S12 reconciled in B2 at the author's request, not B4
- Risks / follow-ups: ONS ETB FYE 2024 decile workbook not retrieved, so council tax and stamp duty deciles can be replaced if the author attaches it; no UK evidence for business rates or corporation tax incidence, nor valuation understatement; migration row rests on non-doms and a secondary summary; Koster and Pinchbeck title not confirmed; HMRC CGT page inconsistent (52% vs 55%); IHT and stamp taxes by income decile are weakly linked to wealth
- Verification: empty-cell and column-count script passed (41 rows, 0 empty cells); rows per driver D4 7, D9 8, D1 5, D5 4, D6 14, D10 3; 27 judgement rows; arithmetic of I-D5b and I-D10b rerun; git diff stat limited to the Touches list plus the brief. Not run: no model code
- Overview sections likely needing an update: none
- Commit / branch: wip(012): stage B2 done, brief/012-v3-input-register
```

### Change report (stage B1)
```
Change report
- Task: 012r stage B1, wealth, income and returns (D4, D9, D1)
- Files changed: docs/model-v3/inputs.md (new, tier 1 sections for D4, D9, D1 and source register); docs/research/012r-b1-derivations.md (new, methods and code); docs/briefs/012r-v3-input-register.md (progress block and this report)
- What is different now: model v3 has a sourced low, central and high for 19 inputs; latest usable WAS wave named (Round 8)
- New or changed interfaces: none
- Acceptance criteria (B1): wealth-to-GDP 5.80 / 5.94 / 7.5 met; share of adults above W_min 49.3 / 54.9 / 64.3% and of wealth 89.7 / 92.7 / 96.4% met (judgement bounds); tail dataset named with licence status met (licence unverified, flagged); income and liquid assets by band met with caveats (derived income, financial-wealth proxy); UK real return mean, spread, loss years, longest run, gap met; every row has all fields (script: 19 rows, 0 empty cells)
- Deviations from the brief: brief file edited for the progress block and report (handover rules; outside the Touches list)
- Risks / follow-ups: Rich List licence unverified; Round 9 release not confirmed; wealth-to-GDP conflict with the ONS balance sheet (S12) unresolved, check in B4; income by wealth band is weakest row; JST post-2020 data missing
- Verification: empty-cell and column-count script on inputs.md passed; rows per driver D4 6, D1 5, D9 8; 7 judgement rows; git diff stat limited to the files above plus the brief. Not run: no model code
- Overview sections likely needing an update: none
- Commit / branch: wip commit, brief/012-v3-input-register
```
