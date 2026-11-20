# 080: Find evidence on how payers declare value against true value (M-3)

- **Status:** ready
- **Author/date:** K. Ogata with the guru, 2026-11-20
- **Depends on:** none
- **Read:** `docs/model-v3/added/supporting.md` (M7, M7c to M7e, and data-gap row M-3); `docs/model-v3/metrics.md` rows M7, M7c to M7e; register rows I-D5a, I-D5b, I-D5d and their sources in `docs/model-v3/inputs.md`; `model_v3/core/support.py` (`declaration_curve`, `modal_alpha`, `tolerant_zone`); archived `docs/archive/briefs/069r-adults-per-household-row.md` and `043r-*.md` (how a research brief reports and how rows are proposed); `docs/model-v3/source-map.md`.

## What is already held (guru check, 2026-11-20)
M-3 was researched once (brief 022r): register rows **I-W9a to I-W9e** hold bunching and understatement evidence, all foreign: Colombia excess mass 4.6 at the notch and inventories understated 22%, undisclosed wealth 15.3% of the top 0.01% (I-W9d, mostly foreign assets), Switzerland 55% of the reported-wealth response (I-W9e, a judgement). `inputs.md` coverage table line "016g M-3" says: no distribution of declared against true value exists, and no UK evidence on valuation. **Do not repeat that search.** Build on it: look for what it missed (UK evidence above all: HMRC probate and IHT valuation reassessments, valuation-office or tribunal outcomes for private business and land; Norwegian and Dutch declared-against-assessed value studies) and say plainly if there is none.

## Goal
Evidence for the **distribution of declared value against true value among payers** (alpha = declared over true): its centre, spread and shape, and any bunching or understatement pattern, so the guru can propose register rows for it. The old papers' "behavioural centre near 1.1" has no source the model can cite (the old definition sits in the VAL section 7 of the old papers).

## Decisions (author, 2026-11-20)
- The first provisional run goes ahead **without** M7e (modal declaration); OD1 reports M7c and M7d and the tolerant zone O7 needs no distribution. This brief supplies the evidence for a later run; it is not on the critical path.

## Design
1. Search for evidence **not already in I-W9a to I-W9e**: wealth-tax and estate-tax valuation gaps (audit or reassessment of declared values: HMRC inheritance tax valuation challenges and probate valuations; Swiss cantons, Spain, Norway, the Netherlands, Colombia and Uruguay bunching studies; the Brülhart, Gruber, Krapf and Schmidheiny work on Swiss wealth tax declarations; Londoño-Vélez and Ávila-Mahecha), and any distribution of misreporting by asset type (private business, property, listed assets). Prefer UK data; say where a number is from another country and why it is used.
2. For each source: the quantity measured, the number (centre, spread, share who understate or overstate), the sample, the year, and the licence if data is reproduced. Use the repository's research-note form (as in `docs/research/`); do not paste long extracts.
3. Propose, as a table only (do not edit the register), the rows the model needs for M7e: whether a support-and-weights form or a parametric form fits the evidence; low, central and high for each; whether each is data or a judgement (J); how it connects to I-D5b and I-D5d. If the evidence cannot support a distribution, say so and say what weaker statement it can support.
4. Say how much the answer would change OD1 (M7c, M7d) if at all: M7e is a reading of who chooses what, the curve itself does not depend on it.

## Touches
`docs/research/080r-declared-alpha-evidence.md` (new), `docs/model-v3/inputs-added/` only if the research note convention puts proposed rows there (follow 069r), this brief's progress block. No register, code or manifest edits.

## Acceptance criteria
- The note lists at least the sources found with the quantity, number, sample and year, or says plainly that none was found.
- The proposed-rows table is present, with (J) marked for judgement.
- `git diff --stat` limited to Touches.

## Checks to run
`python pipeline/run_suites.py` unchanged (docs only).

## Out of scope
The register, the model, the manifest, any change to OD1.

## Open questions
Ask rather than guess: if the evidence is only from outside the UK and the author's reading is needed on whether to use it.

## Implementation notes
<!-- progress:start -->
- **Done:** note `docs/research/080r-declared-alpha-evidence.md`: 14 sources with quantity, number, sample, year (Sweden, Colombia, Switzerland, Norway, UK IHT gap and valuation scrutiny, UK and US valuation noise, euro-area owner reports); four searched and not usable; proposed rows P1 to P5 (table only, (J) marked); effect on OD1 stated.
- **Next:** author answers the two open questions in section 5 of the note (use of foreign evidence; I-D5d wording). The guru then decides whether to propose register rows.
- **Decisions:** parametric mixture proposed over support-and-weights (eight bin weights would have no source). P2 is the existing I-D5d, so no new row. P5 (overstatement for refund protection) has no evidence and no value is proposed.
- **Gotchas:** no source measures the distribution; no UK measurement of alpha. Seim's understater share is 75 to 80% in the held S13 and 75 to 85% in the fetched Seim text; not reconciled. Most sources were read through the fetch tool (shell cannot reach sites), so page numbers are unchecked except S13. On the OD1 grid M7e reads 1.00 for any centre 0.875 to 1.125.
- **Resume:** n/a
- **Not run:** primary PDFs of Seim, Londoño-Vélez and Ávila-Mahecha, SSB, ECB, MSCI not opened directly.
- **State:** note written; branch pushed; not merged (open question for the author)
<!-- progress:end -->

```
Change report
- Task: 080r, evidence on declared value against true value (M-3)
- Files changed: docs/research/080r-declared-alpha-evidence.md (new, the research note); docs/briefs/080r-declared-alpha-evidence.md (progress block and this report)
- What is different now: the repo has a sourced answer to M-3: no distribution exists; the nearest evidence, a mixture form and rows P1 to P5 for the guru to propose
- New or changed interfaces: none
- Acceptance criteria: sources listed with quantity, number, sample, year: met (14 sources, 4 not usable). Proposed-rows table with (J) marked: met (P1 to P5). git diff --stat limited to Touches: met (two files)
- Deviations from the brief: none. Not merged: the brief's open-question rule applies (evidence outside the UK); two questions in section 5 of the note
- Risks / follow-ups: most page numbers are from the fetch tool, not opened PDFs; Seim 75 to 80% (held) against 75 to 85% (fetched) unreconciled; M7e reads 1.00 on the OD1 grid for any centre 0.875 to 1.125 (for the guru)
- Instruction friction: none
- Verification: python pipeline/run_suites.py, 10 of 10 suites passed (layout skipped 40); figures in the note checked against held S13 (Seim 75 to 80%, Colombia 22% and 35%, Swiss half-elasticity, valuation range); route shares checked against I-D13a to I-D13d and kernel `declare`
- Overview sections likely needing an update: none
- Commit / branch: brief/080-declared-alpha-evidence (see push)
```

