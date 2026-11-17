# 029: Site: page registry and ids (site.md B1)

- **Status:** ready
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
- **Done:**
- **Next:**
- **Decisions:**
- **Gotchas:**
- **Resume:**
- **Not run:**
- **State:**
<!-- progress:end -->
