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
- **Done:** `docs/restructure/site/nav.md` written (page types with layouts, flat navigation and URLs, routing block as `site/data/routing.yml` with checks, page registry, search, mobile and print, what the site no longer has, reachability table). The author answered all 12 questions on 2026-11-17 and section 10 records the decisions.
- **Next:** the guru merges the file into `docs/restructure/site.md` with `hooks.md`.
- **State:** done, merged (brief 021s merged, ready to retire)
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
- Deviations from the brief: none. Reconciled with main's 017s (`ids.md`), `shortcodes.md` and `ids-map.md`: page ids are shortcodes; 15 menu spokes plus 4 parent-reached (DECL, BEHAV, WELF, ATTR); data-layer pages and registry fields follow `ids.md`; standalone papers use the spoke shape (017s Q5a); the `Data` navbar item is a menu so output pages stay two clicks from the hub. Two author answers of 2026-11-17 supersede 017s: hub at `index.html` and no redirects except `wp.html`; the lines of `ids.md` and `hooks.md` for the guru to amend are listed at the end of nav.md section 10. Author decisions (2026-11-17) that shaped the design: no redirects for old paper URLs, except `wp.html` to the hub (Q5, Q1); ten existing pages stay live as Pending review until the author decides each (Q3); calculators stay, labelled old model, until updated (Q4).
- Risks / follow-ups: existing citations to the removed papers, including Zenodo, will not resolve (the author accepts this, Q5). Routing `prompt` lines are placeholders for the writing lane to draft and the author to approve (Q10). Link targets here settle the data-page URLs that the sibling hooks design (018s, Q14) asked for; the two files must be merged consistently.
- Verification: 6,000 cap checked against template.md; nav.md re-read against shortcodes.md, ids-map.md and ids.md (S numbers remain only in the note on the routes); the six routes cover all 15 menu spokes (checked by hand). No em dashes in the file. No build run: the diff touches no site file.
- Overview sections likely needing an update: none until the guru merges site.md; section 2 directory map gains docs/restructure/site/.
- Commit / branch: branch brief/021-navigation-and-routing. Merged to main under the auto-merge rule: no open question remains, every criterion is met, the diff stays inside Touches. Brief 021s merged, ready to retire.
```
