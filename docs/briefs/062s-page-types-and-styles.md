# 062: Site: page types and styles (site.md B8)

- **Status:** ready
- **Author/date:** K. Ogata with the guru, 2026-11-18
- **Depends on:** B1 (029s, merged)
- **Read:** `docs/restructure/site/nav.md` sections 2 (2.1 to 2.6), 7, 8 and 10 (decisions 1, 2, 5, 6, 8, 11, 12); `docs/restructure/site.md` section 8 (B8 row, 8.1, 8.2); `docs/restructure/site/hooks.md` section 6 (draft banner, `WDT_MODE`); `docs/restructure/site/figures.md` only where it sets print or layout limits (figure width, reference table `details`); `registry/pages.yml` (page types, the `old-wp` row and its alias); `site/_quarto.yml` (the `format.html.css` list and `include-in-header`); `site/style/` (existing CSS, to avoid class clashes); `site/pages/404.qmd`; `docs/agents/web.md` (the local build).

## Goal
Every page type of the restructured site has its layout, styles and banners as plain includes and CSS, proved on fixture pages, so the integration brief (B15) only has to inject them. No spoke or hub prose is written.

## Decisions (author, 2026-11-17 and 2026-11-18)
`nav.md` section 10 holds: the hub is the home page and `wp.html` is the only redirect (decisions 1 and 5); parent-reached spokes are in no menu (6); a figure's reference table is in a `details` element, closed on screen and open in print (8); the hub keeps an on-page contents list of its eight sections and spokes only the four-anchor jump bar (11); standalone papers carry a banner saying they are not needed for the argument (12). The data gate holds: this brief builds on fixtures and delivers without the model data.

## Design
All files are static (HTML partials, CSS); nothing here reads the data file or `registry/`. Class names and anchors are a contract with B6 (checker), B7 (navigation) and B15 (integration), so document them once in `site/includes/LAYOUT.md`.
1. **Layout partials in `site/includes/`**, one per element of `nav.md` 2.1 to 2.5: the spoke frame (breadcrumb slot, status chip slot, Short answer block, prerequisites line, jump bar with `#short-answer #evidence #strongest-objection #data`, More-detail line slot, Strongest objection box, Data block frame, Read next slot), the hub frame (H0, the eight-entry on-page contents list in the right margin on desktop and collapsed on mobile, "Numbers on this page" foot), the parent-reached banner ("More detail for <parent>. The parent spoke stands without it."), the standalone banner (and the SCOPE variant), the data-layer table wrapper, and the draft banner ("Draft: numbers are not final" plus a placeholder count slot). Slots are empty elements with a documented class or `data-slot`; B15 fills them.
2. **`site/style/spoke.css`**: styles for all of the above, mobile first. The Short answer block is visually distinct and, with the title, fits above the fold at 360 px without the navbar. The jump bar is one row that scrolls sideways. Routing-card slots stack in one column under 600 px. Tables sit in a wrapper that scrolls horizontally inside itself. Tap targets at least 44 px high. Works with the existing `dark.css`; do not edit existing CSS files.
3. **`site/style/print.css`** (`@media print`): hide navbar, search, jump bar, Read next and footer menus; show every `details` open (use `details::details-content` content-visibility where supported and a `beforeprint` script in an include as the fallback); a print header with the page title and the draft banner if present; a print footer element (page URL set by script, plus `data-run-date` and `data-manifest-version` slots the builder fills); a spoke prints alone.
4. **Draft partials.** `site/includes/draft-head.html` holds `<meta name="robots" content="noindex">`; the draft banner partial is above. Release pages simply do not include them. Which pages get them (by `WDT_MODE`) is decided by B15; this brief only proves that a fixture page with the partials renders the banner and the meta tag and a fixture page without them renders neither.
5. **`site/pages/404.qmd`** rewritten in the new shape: a short message, a link to the hub, and an empty routing-block slot (B7 fills it from `routing.yml`). The existing inline-styled 404 content is replaced.
6. **`wp.html` alias.** The hub fixture carries `aliases: [wp.html]` in front matter; the test shows Quarto writes a redirect `wp.html` to `index.html` for it. Do not touch `source/`, `registry/pages.yml` or the real `wp` paper: the collision with the legacy `wp.html` is resolved at cutover (B16).
7. **Fixtures** in `tests/layout/fixtures/`: one `.qmd` page per type (hub, spoke, parent-reached, standalone, standalone SCOPE, data-layer, utility) in release form, plus a draft form of the spoke, each with invented neutral filler text, no WDT claims or numbers.
8. **How the new files are included without editing `site/_quarto.yml`** (that file is B7's: navbar and search). The fixtures declare them per page in front matter: `format: html: css: [style/spoke.css, style/print.css]`, `include-before-body` and `include-after-body` for the partials, `include-in-header` for `draft-head.html` where drafting. The tests render with a temporary copy of the site config. Adding the two CSS files to the global `format.html.css` list (so every page gets them) is left to B7 or B15; state in the change report which of the two should do it and why. If you find a simpler route that does not touch `_quarto.yml`, take it and say so.

**Shared interfaces, fixed before any stage starts** (a build brief never edits them; a mismatch is a question to the guru): the output file shape is `schema wdt-outputs/1` as `pipeline/validate_outputs.py` checks it and `docs/restructure/site/hooks.md` section 3 with the 030c rulings; the country pack format is `docs/model-v3/country-pack.md`; the id lists are `docs/model-v3/outputs.yml` and the module-to-id table of `architecture.md` 2.10; the Samples contract is `architecture.md` 2.9; the layers and import rules are `architecture.md` 5.1. For this brief the ones that bite are the page types and anchors of `nav.md` 2 and the draft and release rules of `hooks.md` 6.

One session, one lane. The stage ends in a stop: tests pass, change report written, branch merged by the auto-merge rule. Standing rules: stop with NEEDS THE AUTHOR if a criterion cannot be met or `source/` would be touched; no spoke or hub prose; a mismatch with a shared interface is a question to the guru.

## Touches
`site/includes/` (new: the partials and `LAYOUT.md`), `site/style/spoke.css` (new), `site/style/print.css` (new), `site/pages/404.qmd`, `tests/layout/` (new, with fixtures), this brief's progress block. Verified: none of the new paths exists today; `404.qmd` exists and is replaced. Nothing in `source/`, `registry/`, `pipeline/`, `.github/`, `site/_quarto.yml`, existing `site/style/*.css`, or docs outside this brief.

## Acceptance criteria
- Each page type fixture renders with Quarto and, in the rendered HTML, carries the elements of `nav.md` 2 for its type: spoke and parent-reached and standalone have the four anchors in the jump bar and a section for each; the hub has an eight-entry contents list and no jump bar; the parent-reached fixture has the "More detail for" banner and a three-step breadcrumb slot; both standalone variants have their banner text; a test per type checks this.
- The draft spoke fixture contains the draft banner text and `<meta name="robots" content="noindex">`; the release spoke fixture contains neither (test).
- A Playwright test at 375 px width loads every fixture page and asserts `document.documentElement.scrollWidth <= 375` (no horizontal page scroll); a second at 360 px asserts that the Short answer block's bottom is within the first viewport height on the spoke fixture, with the navbar collapsed.
- A Playwright test with print media emulated asserts: navbar, jump bar, Read next slot and footer menu are not displayed; every `details` content is visible; the print header and footer elements are displayed and hidden on screen.
- Tap targets: jump bar links and routing slot links have a computed height of at least 44 px at 375 px (test).
- The hub fixture build writes `wp.html` as a redirect to `index.html`.
- The `404.qmd` build output has a link to the hub and the routing-block slot.
- The existing site build (command in `docs/agents/web.md`) passes unchanged and its list of output pages and URLs is identical to the build before the change (diff the list); the existing CSS is byte-identical.
- `git diff --stat` shows only the Touches list.

## Checks to run
The local build named in `docs/agents/web.md`; `pytest tests/layout -q` (needs Quarto and the installed Playwright Chromium; Quarto is not on the sandbox PATH by default, see the gotcha in the archived 029s brief); diff of the built page list before and after. The brief touches `site/`, so the build must pass before any merge to main (AGENTS.md).

## Out of scope
Navbar and menus, `routing.yml`, breadcrumb and Read next generation (B7); the data layer pages' content (B9); hook resolution, the Data block generator and figures (B3 to B5); the spoke checker (B6); wiring partials into the build, draft or release selection, the `/draft/` index, workflow edits (B15); `_quarto.yml` edits; writing prose; any `source/` change or redirect other than the `wp.html` alias.

## Open questions
For the guru, answered before the brief starts if possible: (1) the include route in design item 8: per-page front matter now and the global CSS lines added by B7 or B15 (recommended), against a one-line edit to `_quarto.yml` made here (touches B7's file). The implementer asks rather than guesses on anything else.

## Guru rulings, 2026-11-18
Fixtures declare CSS and includes in per-page front matter and tests render against a temporary copy of the config; B7 or B15 adds the global CSS lines later: accepted. Draft partials only; B15 decides by `WDT_MODE`: accepted. The `wp.html` alias is proved on a hub fixture only; the real collision with the legacy file is B16's.

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
