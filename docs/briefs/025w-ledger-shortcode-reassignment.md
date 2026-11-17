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
- **Done:**
- **Next:**
- **State:** ready
<!-- progress:end -->
