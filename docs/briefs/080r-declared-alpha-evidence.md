# 080: Find evidence on how payers declare value against true value (M-3)

- **Status:** ready
- **Author/date:** K. Ogata with the guru, 2026-11-20
- **Depends on:** none
- **Read:** `docs/model-v3/added/supporting.md` (M7, M7c to M7e, and data-gap row M-3); `docs/model-v3/metrics.md` rows M7, M7c to M7e; register rows I-D5a, I-D5b, I-D5d and their sources in `docs/model-v3/inputs.md`; `model_v3/core/support.py` (`declaration_curve`, `modal_alpha`, `tolerant_zone`); archived `docs/archive/briefs/069r-adults-per-household-row.md` and `043r-*.md` (how a research brief reports and how rows are proposed); `docs/model-v3/source-map.md`.

## Goal
Evidence for the **distribution of declared value against true value among payers** (alpha = declared over true): its centre, spread and shape, and any bunching or understatement pattern, so the guru can propose register rows for it. The old papers' "behavioural centre near 1.1" has no source the model can cite (the old definition sits in the VAL section 7 of the old papers).

## Decisions (author, 2026-11-20)
- The first provisional run goes ahead **without** M7e (modal declaration); OD1 reports M7c and M7d and the tolerant zone O7 needs no distribution. This brief supplies the evidence for a later run; it is not on the critical path.

## Design
1. Search for published evidence: wealth-tax and estate-tax valuation gaps (audit or reassessment of declared values: HMRC inheritance tax valuation challenges and probate valuations; Swiss cantons, Spain, Norway, the Netherlands, Colombia and Uruguay bunching studies; the Brülhart, Gruber, Krapf and Schmidheiny work on Swiss wealth tax declarations; Londoño-Vélez and Ávila-Mahecha), and any distribution of misreporting by asset type (private business, property, listed assets). Prefer UK data; say where a number is from another country and why it is used.
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
- **Done:**
- **Next:**
- **Decisions:**
- **Gotchas:**
- **Resume:**
- **Not run:**
- **State:** ready; not started
<!-- progress:end -->
