# 061: Site: navigation and routing data (site.md B7)

- **Status:** ready
- **Author/date:** K. Ogata with the guru, 2026-11-18
- **Depends on:** none open (029s, the page registry, is merged)
- **Read:** `docs/restructure/site/nav.md` (whole; sections 3, 4, 5, 6, 9 and 10 carry the rules); `docs/restructure/site.md` section 7 (Q2, Q4, R7) and section 8 (B7 row, 8.1, 8.2); `docs/restructure/site/ids.md` (data-layer page ids, rule 7); `registry/pages.yml` (header comment and the menu spoke, appendix, pending, calculator and site rows); `pipeline/config.py` (`PAGES_YML`, `load_pages`, `validate_pages`); `pipeline/pages/` (existing modules, names only); `site/_quarto.yml` (current navbar, read only for structure); `tests/pages/conftest.py` (the fixture pattern); `docs/agents/web.md`.

## Goal
Build, as data and code with tests, everything the new navigation needs: the reader routing file and its checks, the navbar, breadcrumbs, Read next and search description generated from `pages.yml`, and the two-click reachability check. The live site keeps its current navbar until cutover (B16), so nothing a reader sees changes in this brief.

## Decisions (author, 2026-11-17 and 2026-11-18)
- `nav.md` section 10 (twelve answers) and `site.md` section 7 (all answers accepted as proposed on 2026-11-18) hold. The ones this brief builds on: navbar of five items (Questions, Data, Papers, Resources, About), no sidebar, search in the navbar (Q2 of nav.md and R7); the routing file is `registry/routing.yml` (site.md R7 overrides the `site/data/routing.yml` of `nav.md` 4.1); `label` and `order` come from `pages.yml`; title and `status` come from the spoke's front matter (site.md R4).
- Before cutover the new navbar does not exist on the live site and drafts are listed only under `/draft/` (site.md Q2). After cutover a spoke not yet accepted shows a "draft" mark in the menu. B16 switches the navbar; this brief only generates it.
- ADOPT, PILOT and HYPO are parent-reached (parents POL, POL, FALS), not in the menu: the menu stays at 15 spokes; `pages.yml` carries 7 appendix rows.
- Routing prompts are placeholders the writing lane replaces (nav.md Q10); the checks must pass on placeholders.
- The data gate holds: no spoke or hub prose. All work uses fixtures and the placeholders.

## Design
1. **`registry/routing.yml`:** the six routes of `nav.md` 4.1 (economist, lawyer, policy, business, sceptic, researcher) with the map's reader labels verbatim, placeholder `prompt` lines (at most 20 words, no digit) and the `start` lists as printed there (FIRST and WIDER, UNCER, LIMIT and FALS read through `ids-map.md`). Fields: `id`, `reader`, `prompt` (optional), `start` (1 to 5 ids, spoke shortcodes or the token `data`), `order` (optional).
2. **`pipeline/pages/routing.py`:** load and validate `routing.yml` against `pages.yml` and spoke front matter `depends`; the five checks of nav.md 4.2 as functions returning findings with a code, level (error or warning) and message: every `start` id exists in the registry; every route has `reader` and a non-empty `start`; every one of the 15 menu spokes is in at least one route; a route that includes a spoke before its `depends` is a warning; a `prompt` over 20 words or with a digit is an error. Plus the two renderers' data: for the hub, the routes as cards (reader, prompt, ordered links with the spoke's question and id chip, `data` shown as "The numbers" to DL0); for a spoke, Read next lines for only the routes containing it ("next" is the following entry in `start`, "Back to the hub" after the last). Output is plain data (dicts or small dataclasses); markup belongs to B8.
3. **`pipeline/pages/nav.py`:** from `pages.yml`: (a) the navbar as the structure of nav.md section 3, emitted as a YAML fragment compatible with Quarto's `website.navbar` (Questions = the 15 menu spokes in `order` with `label`, Data = DL0 to DL6 from `ids.md`, Papers = ADD, INST, SCOPE, Resources = References, Glossary, Retired papers, calculators labelled "Based on the retired model", a Pending review group of the ten pending pages, About = the author page) and the search block moved to the navbar (`location: navbar`); (b) breadcrumb data for a page (`Hub > FISC`, `Hub > VAL > DECL`); (c) the search meta description rule (spoke question plus the first sentence of its Short answer, at most 155 characters); (d) the draft mark for a spoke whose front matter `status` is not `accepted`; (e) the reachability check of nav.md section 9: compute click depth from the hub over navbar, parent link and routing links, and fail if any page of `pages.yml` that should be reachable is more than 2 clicks away or unreachable. The fragment is written by a function and a CLI (`python pipeline/pages/nav.py --write _build/navbar.generated.yml`); it is **not** wired into the build or into `site/_quarto.yml` (B15 and B16 do that).
4. **`site/_quarto.yml`:** one comment block at the top of the `navbar:` key stating that the live navbar is replaced at cutover by the generated fragment from `pipeline/pages/nav.py` and the search location moves with it. No key or value changes. If any rendered page or URL would differ, revert and stop.
5. **Tests in `tests/nav/`** on fixtures (a small `pages` fixture with menu spokes, appendices, a pending page and a standalone, and fixture front matter), no dependence on spoke prose: one test per check of nav.md 4.2 (each with a passing and a failing routing file), the Read next filtering and its last-entry case, the navbar structure (five items, 15 questions in `order`, no parent-reached page in any menu, pending pages in a group), breadcrumb for a menu spoke and an appendix, the 155-character description rule, the draft mark, and the reachability check (a fixture with a page three clicks away fails; the real registry passes with the data pages and pending pages as listed in section 9). One extra test runs the validators against the real `registry/pages.yml` and `registry/routing.yml`.
6. **Fixtures and pending pages.** The new spokes and data-layer pages have no files yet; navbar and reachability work from registry rows alone. Spoke titles and statuses are read from front matter only where a fixture supplies it; for real spokes without a file the code falls back to `label` and reports the missing file as information, not an error.

## Touches
`registry/routing.yml` (new), `pipeline/pages/routing.py` (new), `pipeline/pages/nav.py` (new), `site/_quarto.yml` (one comment block only), `tests/nav/` (new), this brief's progress block. `pipeline/pages/` already holds `__init__.py`, `corpus.py`, `references.py` and `site_index.py`; leave them as they are. Nothing in `source/`, `site/includes/`, `site/style/` (B8), `pipeline/preprocess.py` (B1 then B15), `registry/pages.yml` (a defect there is a question to the guru), `.github/` or the docs.

## Acceptance criteria
- `registry/routing.yml` has six routes, every `start` id exists in `pages.yml`, every one of the 15 menu spokes is in at least one route, no prompt exceeds 20 words or contains a digit (script check and test).
- Each check of nav.md 4.2 has a test that fails on a deliberately broken routing file and passes on the real one.
- The generated navbar has exactly five items; `Questions` lists the 15 menu spokes in `order` with the registry `label`; no appendix, pending or data page appears in `Questions`; pending pages and calculators are under Resources.
- The reachability check passes on the real registry with every page at most 2 clicks from the hub, and fails on a fixture with a page 3 clicks away.
- The local site build passes and the list of output pages and URLs is identical to the build before the change (diff the lists); `/model/` and every existing URL are unchanged.
- `pytest tests/nav -q`, `pytest tests/pages -q` pass; `git diff --stat` shows only the Touches list.

## Checks to run
The local build (`python pipeline/preprocess.py`, then `quarto render _build`; Quarto may not be on the PATH in the workspace, see the 029s progress block in `docs/archive/briefs/029s-page-registry-and-ids.md` for how it was run); diff of the built page and URL list before and after; `pytest tests/nav tests/pages -q`; the routing script check above. The change touches `site/_quarto.yml`, so the build must pass before any merge to main (AGENTS.md). Skipped: accessibility and mobile (no layout change; B8).

## Out of scope
Markup, CSS, layouts, jump bar, banners (B8); wiring into `preprocess.py` or the deploy workflow (B15); switching the live navbar or home (B16); the final routing prompts (writing lane); the hub text; the data-layer pages themselves (B9); redirects other than the existing `wp.html` alias (already a registry field).

## Open questions
Ask the guru rather than guess. Known to ask about: a registry row the checks cannot classify (for example a data page not yet in `pages.yml`: the Data menu is built from `ids.md` DL0 to DL6 until B9 adds rows); any case where the reachability check conflicts with `nav.md` section 9.

**Shared interfaces, fixed before any stage starts** (a build brief never edits them; a mismatch is a question to the guru): the output file shape is `schema wdt-outputs/1` as `pipeline/validate_outputs.py` checks it and `docs/restructure/site/hooks.md` section 3 with the 030c rulings; the country pack format is `docs/model-v3/country-pack.md`; the id lists are `docs/model-v3/outputs.yml` and the module-to-id table of `architecture.md` 2.10; the Samples contract is `architecture.md` 2.9; the layers and import rules are `architecture.md` 5.1. For this brief the shared files are `registry/pages.yml` and the front matter template (`docs/restructure/template.md`), both read only.

Standing rules: this is one session and one lane. If a criterion cannot be met, or a change would touch `source/` or alter any rendered page, stop with NEEDS THE AUTHOR and say which. Rebase on `origin/main`, re-run the checks and fast-forward push; never force.

## Guru rulings, 2026-11-18
Routing file at `registry/routing.yml` (site.md R7): accepted; the guru corrects `nav.md` 4.1. Only a comment block in `site/_quarto.yml`, the navbar generated as a fragment and not wired in until cutover (Q2): accepted. The Data menu is built from `ids.md` DL0 to DL6 until B9 adds rows: accepted. The menu stays at 15 spokes with the seven appendix rows of the registry; the count in `nav.md` is stale and the guru corrects it.

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
