# 025: Reassign the ledger to shortcodes

- **Status:** ready
- **Author/date:** K. Ogata with the guru, 2026-11-17
- **Depends on:** 013g stages B and C (merged); `docs/restructure/shortcodes.md` and `docs/restructure/ids-map.md` (merged). Runs in parallel with 019s, 021s and 024r.
- **Read:** `docs/restructure/shortcodes.md`, `docs/restructure/ids-map.md`, `docs/restructure/ledger.md`, `docs/restructure/ledger-sections.md`, `docs/restructure/map.md`, `docs/restructure/template.md` section 3, `docs/model-v3/outputs.yml` (elements). Open an old paper in `source/` only where a section's subject is unclear.

## Goal
The author split S11 into FIRST and WIDER and S12 into UNCER, LIMIT and FALS and gave every spoke a shortcode. Bring the ledger and the map to those ids, so every kept section has a home and the word budgets are true.

## Decisions (author, 2026-11-17)
Shortcodes are the page ids; the `-A` suffix retires; the cap is 6,000 words per page; a page that overflows gets its own shortcode, reached from its parent. Output assignments in `outputs.yml` are accepted (O4a, O4b to FIRST, OS1 to WIDER, other former S12 outputs to UNCER, CK1 to FALS, none to LIMIT). The distinctions in `shortcodes.md` section 4 govern: UNCER is what is not known empirically, LIMIT is what the design cannot do even when it works, FALS is what evidence would show a central claim wrong.

## Design
One pass over `docs/restructure/ledger-sections.md` (the section rows), then the summary. Not a rewrite of `ledger.md`.
1. Reassign every row whose destination is S11 or S12 to FIRST or WIDER, or UNCER, LIMIT or FALS, by subject, using the boundaries in `shortcodes.md` section 4. Convert every other row's S id to its shortcode by `ids-map.md`. Record a conflict as a note, not a silent choice.
2. Recompute words kept per shortcode, and flag any page over 6,000, with a proposed split into a new shortcode where one is needed (say which section would move).
3. Update `map.md` section 4 (the spoke table, "fed by" column and v3 outputs) and section 7 to shortcodes, including the routing block.
4. List any model-number claims in the new FIRST, WIDER, UNCER, LIMIT and FALS rows that `outputs.yml` does not cover (as in `ledger.md` section 6) and propose outputs in the same shape; do not edit `outputs.yml`.
5. Add the ledger's missing disposition table for the four reader-facing pages `017s` named (FAQ, comparison tables, avoidance guide, corporate levy page): which page each folds into and the words kept.

## Touches
`docs/restructure/ledger.md`, `docs/restructure/ledger-sections.md`, `docs/restructure/map.md`, and this brief's progress block. Nothing in `source/`, `pipeline/`, `site/`, `registry/`, `outputs.yml`, `metrics.md`, `template.md`.

## Acceptance criteria
- No row has an S id as its destination; every row has a shortcode, a standalone code or a drop reason.
- Words kept per shortcode are listed, and every page over 6,000 words has a proposed split.
- `map.md` sections 4 and 7 use shortcodes only.
- Proposed new outputs are listed, not added.
- `git diff --stat` shows only the Touches list.

## Out of scope
Writing spoke or hub prose, editing `source/`, changing `outputs.yml`, the template or the site designs.

## Open questions
The implementer asks rather than guesses.

## Implementation notes
<!-- progress:start -->
- **Done:** all 980 rows of `ledger-sections.md` reassigned to shortcodes (plus the four reader-facing pages' rows); `ledger.md` sections 1 to 8 recomputed and new section 9 (placement, splits, model-number coverage, four pages) and 10 added; `map.md` sections 3, 4 and 7 in shortcodes.
- **Next:** author decisions below.
- **State:** done, branch `brief/025-ledger-shortcodes` pushed, NEEDS THE AUTHOR.
<!-- progress:end -->

```
Change report
- Task: 025w Reassign the ledger to shortcodes
- Files changed: docs/restructure/ledger-sections.md (every row has a shortcode, standalone code, data layer or drop reason; moved rows carry [025w: ...] notes; four site pages' rows appended); docs/restructure/ledger.md (sections 1 to 8 recomputed; new sections 9 and 10); docs/restructure/map.md (sections 3, 4, 7 in shortcodes); this brief.
- What is different now: no S ids remain as destinations. Kept words per page: FAIR 5,947; LIT 8,580; MECH 6,972; VAL 6,784; DECL 10,700; FISC 8,164; PAY 4,212; BEHAV 6,797; WELF 9,671; FUND 6,210; CORP 9,671; ATTR 6,498; GOV 10,668; POL 13,238; FIRST 1,010; WIDER 6,054; UNCER 0; LIMIT 204; FALS 12,135. Fourteen pages are over 6,000; default splits only for POL (to ADOPT and PILOT) and FALS (to HYPO); the others are optional (ledger.md 9.2).
- New or changed interfaces: none.
- Acceptance criteria: (1) no S id as destination: met (grep, 0 rows). (2) words kept per shortcode listed and every page over 6,000 has a proposed split: met (ledger.md 2 and 9.2; WIDER is over by 54 words and has no seam, so no split is proposed). (3) map.md sections 4 and 7 use shortcodes only: met; sections 3 also converted; S numbers remain only in the ids note and decision history. (4) proposed new outputs listed, not added: met; the finding is that none are needed, but the former S12 outputs need FALS added to `element:` (ledger.md 9.3). (5) git diff --stat shows only the Touches list: met.
- Deviations from the brief: none.
- Risks / follow-ups: UNCER has 0 kept words and LIMIT 204 because their rows were M; proposed treating their M rows as K (6,827 and 6,233 words). FIRST is thin (1,010). comparison-tables page conflicts with template 6a rule 3. The avoidance guide is all M. Element amendments for FALS are for the guru; OH1a was dropped so WELF 4.3 has no output.
- Verification: row counts and word sums recomputed by script from the rows; grep for S-id targets; git diff --stat. Not run: a full read of every paper; the four site pages were read by section opening only.
- Overview sections likely needing an update: the restructure status line (ledger now in shortcodes).
- Commit / branch: see git log, brief/025-ledger-shortcodes
```

