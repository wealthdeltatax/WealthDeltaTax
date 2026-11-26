# 029: Site: page registry and ids (site.md B1)

- **Status:** done, merged 2026-11-18 (author accepted ids old-<stem> and the 15 menu labels)
- **Author/date:** K. Ogata with the guru, 2026-11-17
- **Depends on:** none (site.md approved)
- **Read:** `docs/restructure/site.md` (sections 2, 5, 6, 8); `docs/restructure/site/ids.md`; `docs/restructure/site/nav.md` section 5; `docs/restructure/shortcodes.md`, `ids-map.md`; `pipeline/config.py`, `pipeline/preprocess.py`, `pipeline/transforms.py` (names and entry points only); `registry/papers.yml`; `docs/agents/web.md`.

## Goal
Replace the paper-only registry with `registry/pages.yml`, so every page (33 legacy, new spokes, pending, calculators) has one row, and make the build read it, so later briefs add pages by editing data.

## Decisions (author, 2026-11-17)
`docs/restructure/site.md` is approved with its eight answers (drafts under `/draft/`, hub Data block, ADOPT, PILOT and HYPO reached from their parents, `source/hub.md`, pending-page links rewritten to `retired.html`, glossary seeding before the gate, standalones move after the gate). The data gate holds: no spoke or hub prose. This brief builds on fixtures and delivers without the model data. It is one of the first parallel set (029s, 030c, 031s, 032r, 033c, 034c); the Touches lists do not overlap.

## Design
1. `registry/pages.yml` with fields `id, type, title, url, source, status, parent, aliases, label, order` (site.md section 2; `ids.md` section 5): rows for the 33 legacy papers (status `legacy`), the 22 new spokes, the hub, ADD, INST, SCOPE (type `standalone`, status `legacy`), the ten pending pages, the three calculators and utility pages. New spoke URLs are lower-case shortcodes (`/fisc.html`); drafts publish under `/draft/<id>.html` (not built in this brief).
2. `pipeline/config.py` and `pipeline/preprocess.py` read `pages.yml` instead of `papers.yml` for page lists; `registry/papers.yml` stays as the legacy source for the 33 rows until cutover. The site must build exactly as it does today (same pages, same URLs).
3. Explicit section ids and the shortcode cross-reference grammar of `ids.md` section 1 in `transforms.py`, applied only to new-spoke source files; legacy papers are untouched.
4. Tests under `tests/pages/` on fixture pages: id uniqueness, parent exists, URL collision between a legacy and a new row (site.md Q1) is reported, not published.
The shared file `pipeline/preprocess.py` is also edited later by the integration brief (B15); keep your change small and recorded.

## Touches
`registry/pages.yml` (new), `registry/papers.yml`, `pipeline/config.py`, `pipeline/preprocess.py`, `pipeline/transforms.py`, `tests/pages/`, this brief's progress block. Nothing in `source/`, `site/`, `.github/`, `model_v1/`, `model_v2/`, docs outside this brief.

## Acceptance criteria
- `pages.yml` has one row per page named above and validates in the tests.
- The local site build (the command in `docs/agents/web.md`) passes and the list of output pages and URLs is identical to the build before the change (diff the list).
- Colliding legacy and new URLs are reported by a test, not silently overwritten.
- `git diff --stat` shows only the Touches list.

## Checks to run
The local build named in `docs/agents/web.md`; `pytest tests/pages`; diff of the built page list before and after. The change touches `pipeline/` so the build must pass before any merge to main (AGENTS.md).

## Out of scope
Navigation, routing, layouts, hooks, the checker, the draft index, cutover. Writing spoke prose.

## Open questions
The implementer asks rather than guesses.

## Implementation notes
<!-- progress:start -->
- **Done:** `registry/pages.yml` (77 rows); `config.py` loader, validator, collision report, `paper_registry`; `preprocess.py` reads `pages.yml`; `transforms.py` spoke section ids and cross-reference grammar; `tests/pages` (28 tests).
- **Next:** the author answers the three decisions below; then merge (rebase on `origin/main`, re-run the checks, `git push origin HEAD:main`, watch the Action).
- **Decisions:** legacy row ids are `old-<url stem>` (new codes VAL, CORP, GOV, POL, BEHAV take the bare ids); the 3 standalones are rows of the 33, not extra rows; menu labels are drafted from `shortcodes.md`; types `pending` and `calculator` added; spoke rows carry no `title` or `status` (site.md R4).
- **Gotchas:** build order is output order (`corpus.qmd` lists papers in `papers.yml` order), so the 33 paper rows keep that order; Quarto is not on the sandbox PATH by default (v1.6.43 unpacked under the scratchpad); `site/pages/glossary.md` and `registry/anchors.yml` are generated and git-ignored.
- **Resume:** `python pipeline/build_glossary.py --papers source --contents registry/contents.yml --out site/pages/glossary.md; python pipeline/build_anchors.py; python pipeline/preprocess.py; quarto render _build; python -m pytest tests/pages`
- **Not run:** the Action after merge (not merged); live-site fetch; accessibility and mobile (no layout change).
- **State:** pushed `229ef5b` on `brief/029s-page-registry`.
<!-- progress:end -->

### Change report
```
Change report
- Task: 029s Site: page registry and ids (site.md B1)
- Files changed:
  - registry/pages.yml (new): one row per page, 77 rows
  - registry/papers.yml: header comment only; stays the legacy source for zenodo, pdf, scrape_contents
  - pipeline/config.py: PAGES_YML, load_pages, validate_pages, find_url_collisions, paper_registry
  - pipeline/preprocess.py: reads pages.yml, validates it, prints URL collisions, aborts on invalid registry or two live rows on one URL
  - pipeline/transforms.py: add_section_ids, convert_spoke_refs, process_spoke_text, is_spoke_source (spoke files only; process_file does not call them)
  - tests/pages/ (new): conftest, fixture, test_registry.py, test_spoke_grammar.py
  - this brief's notes
- What is different now: the paper list comes from pages.yml. Seven URLs are claimed twice (new spoke or hub against a live legacy or home page); the live page is built, the new row is held, and preprocess prints each one.
- New or changed interfaces: none for the site. Python: the config.py functions above; transforms.py spoke functions (not wired into the build yet).
- Acceptance criteria:
  - pages.yml has one row per page named and validates: met. 30 legacy + 3 standalone = 33 papers, 22 spokes (15 menu, 7 parent-reached), hub, 10 pending, 3 calculators, 8 site pages; the 53 live rows equal the 53 rendered pages.
  - Local build passes and page list identical: met. preprocess exits 0; `_build` file list and sha256 of every .qmd and .html identical before and after; `quarto render _build` exits 0 and the 53 output HTML pages and URLs are identical (diff empty).
  - Colliding URLs reported, not overwritten: met. test_real_collisions_are_the_known_set, test_legacy_vs_new_collision_is_reported_and_held, test_colliding_new_row_is_never_in_the_build_list.
  - git diff --stat only Touches: met.
- Deviations from the brief:
  - The brief lists "33 legacy papers" and "ADD, INST, SCOPE" separately; they overlap (ids.md section 3), so there are 30 legacy rows and 3 standalone rows.
  - New row types `pending` and `calculator`; spoke-kind rows omit `title` and `status` (site.md R4), so a draft spoke's status is not in the registry.
  - Data-layer pages DL0 to DL6 have no rows: the brief does not name them and B9 adds them.
  - docs/wdt-site-architecture.md not updated (web.md asks for it; Touches excludes it). It now says papers.yml drives the build.
- Risks / follow-ups:
  - Legacy ids `old-<stem>` and the 15 menu labels are my choices: NEEDS THE AUTHOR (or the guru) before B7 (nav) and B10 (retired page) build on them.
  - Guru: update docs/wdt-site-architecture.md (steps 2 and 295) and OVERVIEW.md registry line.
  - The hub (`/index.html`, alias `wp.html`) collides with the live home page and `wp.html` until cutover; expected.
  - convert_spoke_refs leaves an unknown bare `(ABC)` as prose and reports only unknown codes with a section number; the spoke checker (B6) decides the stricter rule.
- Verification: pytest tests/pages 28 passed; preprocess; quarto render; before/after diffs as above. Not run: the deploy Action, live site fetch, accessibility, mobile.
- Overview sections likely needing an update: registry file list; "Paper shortcodes are defined in registry/papers.yml".
- Commit / branch: 229ef5b, brief/029s-page-registry. NEEDS THE AUTHOR: not merged (open decisions above).
```

