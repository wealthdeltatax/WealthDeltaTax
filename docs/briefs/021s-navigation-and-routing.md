# 021: Navigation, hub layout and reader routing

- **Status:** ready
- **Author/date:** K. Ogata with the guru, 2026-11-17
- **Depends on:** 013g stage C (merged); part of 013g stage D. Runs in parallel with 2 (with 017s, 018s, 019s, 020w).
- **Read:** `docs/restructure/map.md` (sections 1 to 3 and 7), `docs/restructure/template.md` sections 1, 2 and 6, and the current site navigation (`site/_quarto.yml` or equivalent, names only). Nothing else need be opened.

## Goal
Design the flat site: page types, navigation, the hub page and its reader-routing block, spoke and appendix page layout, and where standalone papers sit.

## Decisions (author, 2026-11-17)
The spoke template (`docs/restructure/template.md`) is approved, including section 6a (figures and tables). Hub and spokes: `docs/restructure/map.md` section 7. The data gate holds: no spoke prose until the data is final. This brief designs; it builds nothing.

## Design
One file only: `docs/restructure/site/nav.md`. Cover: the page types and their layout (hub, spoke with short answer first, appendix, data-layer page, standalone paper); the navigation (flat: one level from the hub, appendix reached from its spoke); the routing block as data (reader to starting spokes, in `map.md` section 3) and how it renders; links from spoke to spoke and to the data layer; search; mobile and print; and how a reader who lands on any spoke finds the hub and the next step. State what the site no longer has (long numbered series, per-paper tables of contents) and what replaces it. For every point where the document needs a decision it does not own, write a numbered question with a proposed answer; do not guess. The guru merges the sibling files into `docs/restructure/site.md` (shared file; `brief-template.md`, Splitting).

## Touches
New `docs/restructure/site/nav.md` and this brief's progress block. Nothing in `source/`, `pipeline/`, `site/`, `registry/`, `model_v1/`, `model_v2/`.

## Acceptance criteria
- Every page type has a layout stated in words or a sketch.
- The routing block is specified as a data file with fields.
- The navigation reaches every page in at most two clicks from the hub.
- Standalone papers and the data layer have a stated place.
- `git diff --stat` shows only the Touches list.

## Out of scope
Building the pipeline, writing spoke or hub prose, editing `template.md`, choosing values.

## Open questions
The implementer asks rather than guesses.

## Implementation notes
<!-- progress:start -->
- **Done:**
- **Next:**
- **State:** ready
<!-- progress:end -->
