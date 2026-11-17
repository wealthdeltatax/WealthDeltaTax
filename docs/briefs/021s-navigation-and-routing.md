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
- **Done:** `docs/restructure/site/nav.md` written (page types with layouts, flat navigation and URLs, routing block as `site/data/routing.yml` with checks, page registry, search, mobile and print, what the site no longer has, reachability table, 12 numbered questions with proposed answers).
- **Next:** the guru reviews the 12 questions with the author and merges the file into `docs/restructure/site.md`.
- **State:** done, NEEDS THE AUTHOR (open questions remain; not merged)
<!-- progress:end -->

### Change report
```
Change report
- Task: brief 021s, navigation, hub layout and reader routing
- Files changed: docs/restructure/site/nav.md (new, the design); docs/briefs/021s-navigation-and-routing.md (this progress block)
- What is different now: the flat site is specified: page types and layouts, a five-item navbar, URL scheme, the routing block as data, and where the data layer and standalone papers sit. Nothing is built.
- New or changed interfaces: none built. Proposed: site/data/routing.yml, registry/pages.yml, `successor` field in registry/papers.yml, URL scheme in nav.md section 3.
- Acceptance criteria:
  - Every page type has a layout: met (section 2: hub, spoke, appendix, data, standalone, utility).
  - Routing block is a data file with fields: met (section 4.1, checks 4.2); the six routes are map.md section 3 verbatim; all 12 main spokes appear in at least one route (checked by hand).
  - Every page within two clicks of the hub: met (section 9, longest path 2).
  - Standalone papers and the data layer have a stated place: met (sections 2.4, 2.5, 3).
  - git diff --stat shows only the Touches list: met, see Verification.
- Deviations from the brief: none. Section 10 Q3 proposes dispositions for pages the restructure documents do not mention (FAQ, Comparison Tables, Project Map, Avoidance, Corporate Levy and others); these are proposals, not decisions.
- Risks / follow-ups: Quarto `aliases` for redirects is not used in the pipeline today and is unverified for this build (Q5). Routing `prompt` lines are placeholders for the writing lane (Q10). Link targets here settle the data-page URLs that the sibling hooks design (018s, Q14) asked for; the two files must be merged consistently.
- Verification: appendix ids (S4-A, S6-A, S6-B, S8-A) and the 6,000 cap checked against map.md and template.md; page count recomputed (49). No em dashes in the file. No build run: the diff touches no site file.
- Overview sections likely needing an update: none until the guru merges site.md; section 2 directory map gains docs/restructure/site/.
- Commit / branch: branch brief/021-navigation-and-routing. NEEDS THE AUTHOR: open questions remain, so the auto-merge rule does not apply.
```
