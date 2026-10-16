# WDT Site Architecture

**Project:** Public-facing GitHub Pages website for the Wealth Delta Tax research programme
**Generator:** Quarto (non-negotiable)
**Root directory:** `wdt-site/`
**Last synced:** 5 Oct 2026, against the repo files only. The live site was not fetched. Items under "Issues and recommended fixes" come from reading code and should be confirmed on the live site before acting.

The site takes Markdown source files for 33 WDT papers (`registry/papers.yml` has 33 entries), preprocesses them into Quarto-ready `.qmd` files, and publishes the result as a static HTML site via GitHub Pages. The build is a chain of Python steps followed by a Quarto render. Two further Python pipelines (PDF build, Zenodo upload) share code with it but are not part of the site build.

---

## Directory structure

```
wdt-site/
├── pipeline/
│   ├── build.bat                (full pipeline minus quarto render)
│   ├── build_and_render.bat     (full pipeline + quarto render)
│   ├── scrape_contents.py       (headings from source .md -> registry/contents.yml)
│   ├── build_glossary.py        (per-paper Glossary sections -> site/pages/glossary.md)
│   ├── build_anchors.py         (contents.yml -> registry/anchors.yml)
│   ├── bib_to_json.py           (references.bib + internal.json -> references.json)
│   ├── preprocess.py            (orchestrator)
│   ├── config.py                (paths, constants, extract_paper_meta(), SiteConfig, load())
│   ├── transforms.py            (per-paper text transforms; also used by pdf.py)
│   ├── diagrams.py              (.mmd -> PNG with cache, flowcharts.qmd)
│   ├── link_map.py              (generates _build/link-map.qmd)
│   ├── tools.py                 (TOOLS registry, calculator .qmd wrappers)
│   ├── pdf.py                   (standalone PDF build: pandoc + lualatex -> print/YYMMDD/)
│   ├── zenodo_upload.py         (bulk Zenodo upload/metadata refresh; writes DOIs back to source)
│   └── pages/
│       ├── __init__.py
│       ├── corpus.py            (Papers index with reading paths)
│       ├── references.py        (External References page)
│       └── site_index.py        (static data endpoints + site-index.json)
├── registry/
│   ├── contents.yml             (hand + scrape_contents --write; paper/section hierarchy)
│   ├── anchors.yml              (GENERATED, gitignored)
│   ├── papers.yml               (source -> output mapping, 33 entries)
│   ├── internal.json            (hand-maintained: internal_papers, citations, flags)
│   ├── references.bib           (hand-maintained external bibliography)
│   └── references.json          (GENERATED every build; never edit)
├── source/                      (33 paper .md files; read-only to the pipeline)
├── site/
│   ├── _quarto.yml
│   ├── pages/
│   │   ├── 404.qmd, BingSiteAuth.xml
│   │   ├── index.md, research.md, faq.md, Project-Map.md
│   │   ├── comparison-tables.md, avoidance.md, corporate-levy-taxpayer.md
│   │   ├── calculator_index.md, glossary.md (GENERATED), internal_bibliography.md
│   │   ├── revision_history.md, author_page.md
│   ├── style/
│   │   ├── styles.css, page-components.css, tools.css, dark.css
│   │   ├── apa.csl, svg-pan-zoom.min.js, geocities.html
│   ├── diagrams/                (.mmd sources AND cached .png renders)
│   └── tools/                   (taxpayer_calc.html, revenue_calc.html, ldw_calc.html)
├── model/
│   ├── WDT_Params.toml          (no date prefix any more)
│   ├── wdt_core.py, rates_model.py, ldw_core.py   (Pyodide runtime files)
│   ├── val_helpers.py, val_s_helpers.py, rates_s_helpers.py
│   ├── numbered output scripts (5_3 ... 16_7) and run_all.bat
│   └── OUTPUTS/                 (gitignored; copied to _build/figures/)
├── print/                       (gitignored: PDFs in YYMMDD/, template.tex, tabularx.lua, zenodo_dois.json, logs)
├── docs/                        (this file's canonical copy, navigation_suggestions.md, Old Index/)
├── .github/workflows/deploy.yml
├── .gitignore                   (_build/, _site/, .quarto/, __pycache__/, anchors.yml, pdfs/, print/ ...)
├── CNAME, robots.txt            (repo root; see Issue 8)
└── _build/                      (fully generated; never edit)
```

---

## Build sequence

```
registry/references.bib + internal.json --(bib_to_json)--> registry/references.json
source/*.md --(scrape_contents --write)--> registry/contents.yml
contents.yml + source/*.md --(build_glossary)--> site/pages/glossary.md
contents.yml --(build_anchors)--> registry/anchors.yml
everything --(preprocess.py)--> _build/ --(quarto render _build)--> _build/_site/
```

Run order, full: `pipeline/build_and_render.bat` runs `scrape_contents.py --write`, `build_glossary.py`, `build_anchors.py`, `preprocess.py`, then `quarto render _build`. `pipeline/build.bat` is the same without the render. CI runs the same sequence on Linux.

### Actual order inside `preprocess.py main()`

1. `bib_to_json.run()` regenerates `references.json`.
2. Read `papers.yml`; call `config.extract_paper_meta()` on every source file to build `paper_meta` (shortcode comes from the file's own front matter).
3. `config.load(paper_meta=...)` builds the `SiteConfig`.
4. Delete and recreate `_build/`.
5. Copy `site/` into `_build/` (rules below), including the `WDT_CALC_INJECT` replacement in `.md` pages.
6. Copy `model/` runtime files (everything except `.html` and `OUTPUTS/`) to `_build/model/`.
7. Copy `model/OUTPUTS/**` flat into `_build/figures/`.
8. `generate_corpus_qmd`, `generate_references_qmd`, `generate_flowcharts_qmd`, `generate_link_map_html`, `generate_tool_pages`.
9. `copy_machine_readable_assets` (includes `site-index.json`).
10. `process_file()` on every paper.

**Ordering consequence:** step 9 runs before step 10, and `_build/` was wiped in step 4. `site_index.py` reads `_build/<paper>.qmd` to build search text, so those files do not exist yet. See Issue 1.

### Asset copy rules (step 5)

| Source path | Behaviour |
|---|---|
| `site/pages/*.md` | Flattened to `_build/` root, renamed `.qmd`, `strip_latex` + `convert_crossrefs` applied, `WDT_CALC_INJECT` sentinels replaced |
| `site/pages/*` other (`.qmd`, `.xml`) | Flattened, copied verbatim |
| everything else under `site/` | Copied with relative path preserved. **This includes `site/tools/*.html` and `site/diagrams/*.mmd`**; there is no exclusion in the code (older docs said otherwise) |

`WDT_CALC_INJECT`: a comment `<!-- WDT_CALC_INJECT: taxpayer_calc.html -->` in a page is replaced with a `{=html}` block holding that fragment from `site/tools/`, shell-stripped. `avoidance.md` uses it. Fragments injected into root-level pages must fetch runtime files by absolute path (see Calculators).

---

## `pipeline/`

### `scrape_contents.py`
Reads headings from `source/*.md` and merges new entries into `registry/contents.yml` (never overwrites existing keys). Modes: `--report` (default), `--write`, `--dry-run`. Shortcode comes from each file's front matter. Skips headings with `{.unnumbered}`/`{.unlisted}` and prose-only titles (abstract, glossary, internal bibliography, revision history, keywords, author disclosure). Appendix h1 with no letter prefix is flagged as an edge case, never written.

### `build_glossary.py`
Extracts `**Term:** definition` pairs from each paper's `# Glossary` section only, deduplicates (longer definition wins), finds every section that mentions each term (exact, lower, sentence-case, acronym base, naive plural), and writes `site/pages/glossary.md` with raw-HTML letter anchors and a jump bar. Papers map to shortcodes by fuzzy match on the front-matter `title:`, not on `shortcode:`. Never edit `glossary.md`; edit the per-paper Glossary sections.
Known defects: Issue 3 and Issue 4.

### `build_anchors.py`
Derives Quarto anchors for every `PAPER§KEY` in `contents.yml` and writes `registry/anchors.yml`. Rules: numeric keys (`1`, `1.1`) slugify the title only; single letters A to H keep a dot (`a.-the-chambers-in-full`); single letters I to Z have no dot (`j-the-deferred-delta`, unverified; the script prints these for browser verification); letter-dot-numeric keeps the full prefix (`a.1-the-taxpayer-chamber-tp`). Must be re-run after any change to `contents.yml`.

### `bib_to_json.py`
Merges `references.bib` and `internal.json` into `references.json`. Type map: `@article` to `journal_article`, `@book` to `book`, `@incollection` to `book_chapter`, `@unpublished` to `working_paper`, `@techreport` to `working_paper` (NBER/CESifo/WID or `type = Working Paper`) otherwise `report`, `@misc` to `institutional_report`. `note` field parsing: `Verified YYYY-MM-DD` sets `verified`; `Flag N` adds flag ids only if present in `internal.json`. Current output: **177 external refs, 31 internal papers, 365 citations, 17 flags** (`meta.date` 260929).

### `preprocess.py`
See "Actual order" above. Imports `_strip_html_shell` from `tools.py` for sentinel injection.

### `config.py`
Paths, `SITE_URL`, `AUTHOR`, `AFFILIATION`, `DISCLOSURE`, date helpers, `SiteConfig`, `load()`.
`extract_paper_meta()` returns: `shortcode, title, status, keywords, jel, version, version_date (ISO), version_date_display, word_count, zenodo_doi, cite_keys`. Version/date come from the last row of the revision-history table (two-step regex so later pipe tables cannot match). Word count runs from the first numbered heading (or first lettered heading for appendix papers) to the end. `_format_date()` (YYMMDD to ISO) is legacy, used only for `internal.json` dates.

### `transforms.py`
Seven calls in `process_file()`: `strip_latex`, `fix_image_paths` (all to `figures/<name>`), `convert_crossrefs`, `convert_internal_bibliography`, `inject_front_matter`, `inject_under_construction` (versions starting `0.`), `build_jsonld`.
`inject_front_matter` now also builds, from `zenodo_doi`: a PDF download button and a checkbox-toggle Cite panel (APA + BibTeX with copy buttons). It injects `.paper-meta` and `.paper-disclosure` before the revision-history table.
**`pdf.py` imports from here and from `config.py`.** Do not change function signatures without checking `pdf.py`.

### `diagrams.py`
`DIAGRAMS` registry now uses undated names: `WDT_Flowchart_LR.mmd`, `WDT_Skeleton_LR.mmd`, `UK_Tax_Flowchart_LR.mmd`, `UK_Skeleton_LR.mmd`, `WDT_Bidirectional_LR.mmd`.
`render_pngs()` is **cache-aware**: if `site/diagrams/<name>.png` exists it is copied to `_build/diagrams/`; otherwise `mmdc` renders (width 3600) into `site/diagrams/` and then copies. To regenerate, delete the PNG and rebuild; commit the new PNG. In CI, `PUPPETEER_CONFIG` is passed to `mmdc`. `_METRICS` (node/decision/edge counts) is hardcoded; update when diagrams change. `generate_flowcharts_qmd()` writes `_build/flowcharts.qmd` (side-by-side layout, metrics table, lightbox).

### `link_map.py`
`generate_link_map_html(dest, refs_data, link_map)` **writes `_build/link-map.qmd`** (suffix replaced), not HTML. The page uses `page-layout: full`, hides the sidebar and title with CSS, and overlays a fixed-position force-directed graph below the navbar (height measured by `lmFitToNavbar`). Nodes come from `refs_data["internal_papers"]`, so a paper missing from `internal.json` has no node. Group is looked up in `_GROUPS` (fallback "Analysis"). Edges are built only as "out" links.
Known defects: Issue 6.

### `tools.py`
`TOOLS` has three entries: `taxpayer_calc.html` to `model/taxpayer.qmd`, `revenue_calc.html` to `model/revenue.qmd`, `ldw_calc.html` to `model/ldw.qmd`. `_wrap_as_qmd` writes front matter (`toc: false`) plus a `{=html}` block with `quarto-disable-processing=true`.

### `pdf.py` (separate pipeline)
Per paper: strip LaTeX (keeping `\newpage`, `\tableofcontents`), fix image paths, extract Pattern-B figure captions, convert crossrefs, convert internal bibliography, inject front matter, strip Quarto blocks (rescuing figure divs), inject disclosure as plain italic, append `# References`. Renders with `pandoc --pdf-engine=lualatex --citeproc -f markdown-implicit_figures` using `print/template.tex`, `print/tabularx.lua`, `registry/references.bib`, `site/style/apa.csl`. Output `print/YYMMDD/The Wealth Delta Tax - {Group} - {Short Title}.pdf`. `SECTION_ORDER` here is a third copy of the paper grouping (see Group lists below). Windows-style `--resource-path` separator (`;`). Not run in CI.

### `zenodo_upload.py` (separate pipeline)
Bulk upload of PDFs to Zenodo using `extract_paper_meta()`, abstracts from the `# Abstract` section, JEL subjects, plain-text references from `references.bib`, related identifiers (site URL + sibling DOIs). Modes: `--sandbox` or `--publish`, `--dry-run`, `--only`, `--update-metadata`. Writes `print/zenodo_dois.json` and writes `zenodo_doi:` back into each source file's front matter, which the site then uses for the Download PDF button, Cite panel and the DOI column on the Papers page. **Contains a hardcoded sandbox token default; see Issue 7.**

### `pages/corpus.py`
Rewritten. Produces `corpus.qmd` with: reading-path tabs (`READING_PATHS`: new, serious, economist, legal, political, full) with estimated reading time at 250 wpm; a legend and coloured domain chip map that highlights or dims chips for the selected path; a words/reading-time toggle; and nine section tables (`SECTION_ORDER`: Core, Prior literature, Jurisdiction, Valuation, Revenue modelling, Robustness & limits, Welfare & distribution, Implementation, Political & strategic). Table columns: Paper, Title, Version, Words, Status, DOI. Also emits collection JSON-LD and a "Reading dependencies" section. All CSS and JS are inline in the generated page.
Known defect: Issue 2.

### `pages/references.py`
Alphabetical bibliography with `## A`, `## B` headings (`toc: true` set in generated front matter). APA formatting per type, DOI/URL title links, verified badge, "Cited in" links. `_ABBREV_TO_CANONICAL` maps abbreviated `paper_id` values (LRA, LRB, CORPA, GOVA, GOVB, RATESA, SWEEPSA, VALA, VALB, BEHAVB, POLA) to dotted shortcodes before `link_map` lookup. `_PENDING_ORPHANS` is empty. Typo: `BEHAVB` maps to `BEHAVE.B` (Issue 14).

### `pages/site_index.py`
Copies `references.json`, `anchors.yml`, `contents.yml` (as `wdt-contents.yml`), `references.bib` to `_build/`, then writes `site-index.json` (`meta`, `papers`, `anchors`, `search`). The docstring says search records feed `right-panel-search.html`; that file was not among the files reviewed.

---

## `registry/`

| File | Maintained by | Rule |
|---|---|---|
| `contents.yml` | Hand + `scrape_contents --write` | Drives anchors, glossary, site-index |
| `anchors.yml` | `build_anchors.py` | Never edit; gitignored; regenerate after a fresh clone |
| `papers.yml` | Hand | 33 entries; `source` is the exact filename (filename must stay lowercase for Linux CI) |
| `internal.json` | Hand | Paper records, citations, flags. Currently **31 paper records: `FAL` and `POL.A` are missing** (Issue 6) |
| `references.bib` | Hand | External bibliography; also Quarto's `bibliography:` and the PDF/Zenodo pipelines |
| `references.json` | `bib_to_json.py` | Never edit |

`contents.yml` has 33 entries (LR was removed). `internal.json` flags: 17 present; open at last sync: flag_10 (Gangl 2015a/b disambiguation), flag_27 (Shakow DOI unverified), flag_35 (`@IMF2020Norway` should be `@IMF2021Norway` in FAL), flag_36 (`@DAgostino2026` in FAL unlocatable).

---

## `site/`

### `_quarto.yml`
- `project.render`: `"*.qmd"`, `"model/*.qmd"`. `resources`: `model/wdt_core.py`, `model/rates_model.py`, `model/ldw_core.py`, `model/WDT_Params.toml`, `diagrams/`.
- `website`: title, description, site-url, Open Graph, Twitter card, `search: sidebar textbox`.
- **Navbar (left):** Home (`index.html`), How To Navigate (`research.html`), FAQ, Comparison Tables, Project Map, **Papers** menu (All Papers to `corpus.html`, then groups: Core, Prior Literature, Jurisdiction, Mechanism & Valuation, Revenue Modelling, Robustness & Limits, Welfare & Distribution, Implementation, Political & Strategic; main papers only, appendices not listed except none), Avoidance, **Corporate Levy** (`corporate-levy-taxpayer.html`), **Tools** menu (Calculators index, Taxpayer, National Revenue, Labour Dividend, Flowcharts, Link Map), **Resources** menu (References, Glossary, Internal Bibliography, Revision History), About the Author and Contacts.
- **Sidebar (docked, collapse-level 1), nine sections:** Core; Prior Literature; Jurisdiction; Mechanism & Valuation (VAL, VAL.A, VAL.B, CORP, CORP.A, GOV, GOV.A, GOV.B); Revenue Modelling (RATES, RATES.A, SWEEPS, SWEEPS.A); Robustness & Limits (BEHAV, BEHAV.A, FAL, SCOPE); Welfare & Distribution (WFR, WFR.A, LDW, ENV); Implementation (CLOSE, PHASE1); Political & Strategic (POL, POL.A, FM, MOD, INST, ADD). Appendices appear in the sidebar only.
- **Footer:** left CC BY 4.0; centre contact email; right Zenodo DOI `10.5281/zenodo.21964119`.
- **format.html:** `include-in-header: style/geocities.html`; theme light `cosmo`, dark `darkly`; CSS order `styles.css`, `tools.css`, `page-components.css`, `dark.css`; `toc: true`, `toc-depth: 2`; hover citations and footnotes; `csl: style/apa.csl`; top-level `bibliography: references.bib`.

### `site/pages/`
| File | Notes |
|---|---|
| `index.md` | Now plain markdown: one-minute example, bidirectional diagram, symmetry table, current-system gaps, "what the money is for" (LDW figures), SWF, comparison table, Sceptical quote block linking to FAQ ids, where-to-go table. The old 7-screen hero layout is gone |
| `research.md` | "How To Navigate": five-paper spine, domain table, paper question tables, reading guide. Uses bare `(WP)` style crossrefs |
| `faq.md` | Twelve objections as `##` headings with explicit ids: revenue, crash, val, corp, definition, liquidity, behav, pol, growth, gov, labour, threshold |
| `Project-Map.md` | Now has YAML front matter (title, a description holding "Last updated" and the paper list, author). Narrative summary of every paper plus open-question register. "Last updated 30 September 2026" |
| `comparison-tables.md` | One section per criterion, each a 3-column table (current system, stock wealth tax, WDT). WFR figures. Windows line endings |
| `avoidance.md` | "How to minimise your WDT liability": six decisions, plain markdown with MathJax; injects `taxpayer_calc.html` via `WDT_CALC_INJECT` |
| `corporate-levy-taxpayer.md` | **New.** Taxpayer-facing guide to corporate delta levy credits (tranches, broker role, 12-month credit deadline, worked example) |
| `calculator_index.md` | `.tool-card` links; currently lists three calculators |
| `glossary.md` | GENERATED |
| `internal_bibliography.md`, `revision_history.md`, `author_page.md` | Static |
| `404.qmd`, `BingSiteAuth.xml` | Pass-through |

### `site/style/`
- `styles.css` v3: all colours are CSS custom properties in `:root` (palette documented at the top of the file). Geocities-era look retained.
- `page-components.css`: glossary jump bar, `.paper-meta` bar with `.paper-meta-buttons`, **Cite panel** (`.cite-panel`, `.cite-toggle-input`, `.cite-dropdown`, `.cite-block`, `.cite-copy`), disclosure block, plus classes for the older welcome/index/FAQ/avoidance layouts (see Issue 13).
- `tools.css`: calculator classes. `.wdt-tool-panel`, `.wdt-tool-inner`, `.wdt-tool-header` are **still present** in the file (older docs said removed).
- `dark.css`: **new.** Overrides under `body.quarto-dark` for every component; palette documented at the top.
- `apa.csl`; `svg-pan-zoom.min.js` (probably unused since the PNG migration).

### `site/style/geocities.html`
Loaded globally by `include-in-header`. **Auto-initialises on DOMContentLoaded:** inserts a scrolling slogan banner after the navbar and a footer strip (`[Netscape badge] [webring] [counter]`) before the footer; also adds a click handler so a whole inline citation is clickable. Public API `WDTGeocities.inject(keys, target)`, `injectAll`, `html(key)` with keys `banner`, `counter`, `webring`, `netscape`, `contact`. `WEBRING_PAGES` (14 entries) and `BANNER_SLOGANS` are hand-maintained. Page-level `inject([...])` calls now duplicate the auto-init (Issue 6). This file **is** copied into `_build/style/` by the normal asset copy.

### `site/diagrams/`
Holds the five `.mmd` sources and their cached `.png` renders (commit the PNGs).

### `site/tools/` and Calculators
Three body fragments, no shell. Pyodide loads from jsDelivr (`v0.27.5`).
| Fragment | Runtime files fetched | Fetch style |
|---|---|---|
| `taxpayer_calc.html` | `wdt_core.py`, `WDT_Params.toml` | **absolute** `/model/...` (works on `model/taxpayer.html` and when injected into `avoidance.html`) |
| `revenue_calc.html` | `wdt_core.py`, `rates_model.py`, `WDT_Params.toml` | relative (works only on `/model/` pages) |
| `ldw_calc.html` | `ldw_core.py` | relative; overrides `ldw_core.VAT_SPEND_FRACTION` and `ENERGY_REDUCTION` before calling `ldw_calc(salary)` |

Any fragment injected into a page outside `/model/` must use absolute fetch paths.

---

## `model/`
Runtime (loaded by Pyodide): `WDT_Params.toml`, `wdt_core.py`, `rates_model.py`, `ldw_core.py`. Output scripts (`5_3 ...`, `8_3 ...`, `16_2 ... 16_7`, helpers, `run_all.bat`) run locally and write to `model/OUTPUTS/`. Everything except `.html` and `OUTPUTS/` is copied to `_build/model/`; the four runtime files are also in `resources:`.

---

## `.github/workflows/deploy.yml`
(Not re-reviewed this sync; details as previously recorded.) On push to `main`: Python 3.11, Quarto, `pip install pyyaml bibtexparser`, install `mmdc` with a no-sandbox Puppeteer config, then `scrape_contents --write`, `build_glossary`, `build_anchors`, `preprocess`, `quarto render _build`, upload `_build/_site/`, deploy with `deploy-pages`. `pdf.py` and `zenodo_upload.py` are not run in CI.

---

## `_build/` (generated)
After `preprocess.py`: one `.qmd` per paper; `corpus.qmd`, `references.qmd`, `flowcharts.qmd`, `link-map.qmd`; `model/taxpayer.qmd`, `model/revenue.qmd`, `model/ldw.qmd` plus runtime files; flattened `site/pages/*`; `style/`; `tools/*.html` and `diagrams/*.mmd` (unintended copies); `diagrams/*.png`; `figures/`; the static endpoints and `site-index.json`. Rendered output is `_build/_site/`.

## Cross-reference system
`(PAPER §X.Y)`, `(PAPER)` and `PAPER §X.Y` are converted to links by `convert_crossrefs` using `anchor_map` for deep links and `link_map` for page links. Unknown sections fall back to the page root with a console warning. Inline `@Key` citations are resolved by Quarto against `references.bib`.

## Machine-readable endpoints
`/references.json`, `/wdt-contents.yml`, `/anchors.yml`, `/references.bib`, `/site-index.json`.

## Group lists that must be kept in sync by hand
Paper grouping exists in **four** places: `_quarto.yml` (navbar + sidebar), `pages/corpus.py` (`SECTION_ORDER`, `READING_PATHS`), `link_map.py` (`_GROUPS`, `_GROUP_ORDER`), `pdf.py` (`SECTION_ORDER`). Update all four when adding a paper.

## Paper-count reconciliation
Registry: 33 papers. Text says: `index.md` and `research.md` "32", `link_map.py` front matter "26", Project-Map description lists 33 codes, older docs "27". `corpus.py` computes the number dynamically. Decide the public number and update the static strings.

---

## Issues and recommended fixes
Found by reading code and content. Confirm on the live site before treating as fact.

| # | Severity | Issue | Fix |
|---|---|---|---|
| 1 | High | **Search text is empty.** `copy_machine_readable_assets()` (builds `site-index.json`) runs before the per-paper loop, but `_build/` was deleted at the start, so `_load_search_text()` finds no paper `.qmd` files | In `preprocess.py`, move the per-paper `process_file` loop above `copy_machine_readable_assets` |
| 2 | High | `pages/corpus.py` `SECTION_ORDER` last group: `["POL", "POL.A" "FM", ...]` is missing a comma, producing the string `"POL.AFM"`, so the FM and POL.A chips and table rows are dropped | Add the comma |
| 3 | Medium | `build_glossary.py` strips LaTeX with `re.sub(r'\\[a-zA-Z]+...')`, which also deletes `\tau`, `\alpha` etc. Visible in `glossary.md` as `$_{prov}$`, `$_h$`, `$$ $$ 1.1`. Terms starting `$\tau` also sort before "A" | Restrict the strip to layout commands (`newpage`, `medskip`, `bigskip`, `smallskip`, `clearpage`, `noindent`, `tableofcontents`); sort on the term with `$` and `\` removed |
| 4 | Medium | The Administrator glossary entry contains pasted editing instructions ("This can sit after the existing sentence ending...") | Fix in the GOV source Glossary section, then rebuild |
| 5 | Medium | `revenue_calc.html` start-year list is `length: 60` (1947 to 2006) but the default is set to 2007, so the select is blank and historical mode returns NaN | Use `length: 73` as in the taxpayer calculator |
| 6 | Medium | `link_map.py`: the template's raw HTML fence is never closed and ends with a stray `{=html}` plus a `WDTGeocities.inject([...])` call that duplicates the auto-init. "Inbound only" shows no edges (all links are typed "out"). `_GROUPS` lacks LDW, FAL, BEHAV.A, POL.A (falls back to Analysis) and still lists LR. `internal.json` has no `FAL` or `POL.A`, so those papers have no node | Close the fence, delete the trailing block, derive inbound edges (or drop that option), update `_GROUPS`, add FAL and POL.A to `internal.json` |
| 7 | High (security) | `zenodo_upload.py` has a real-looking Zenodo sandbox token as the default value | Revoke and rotate it; read tokens only from environment variables; check git history |
| 8 | Medium | `robots.txt` and `CNAME` are at the repo root, but the deployed artifact is `_build/_site/`, so they are probably not served | Put `robots.txt` in `site/pages/` (flattened to root, copied as-is) and add it to `resources:`; verify at `/robots.txt`. A CNAME file is not needed for Actions deploys if the domain is set in repo settings |
| 9 | Low | Broken in-page anchors: `faq.md` links `index.html#the-public-wealth-fund` (heading is "The Sovereign Wealth Fund"); `index.md` links `faq.html#close` (no such id; FAQ Q4 is `#corp`) | Fix the two links |
| 10 | Low | Paper count text inconsistent (see reconciliation above) | Pick one number |
| 11 | Low | Calculator defaults lag the papers: both calculators default to the 2007 start and N = 29, while RATES v1.02 to v1.03 moved the reference scenario to 2000 Balanced and N = 30. Fetch style differs between fragments (see Calculators) | Update defaults and the "LRR breakeven" note; standardise on absolute `/model/` paths |
| 12 | Low | Unintended copies into `_build/`: `site/tools/*.html` and `site/diagrams/*.mmd` | Skip `tools` in the copy loop (calculators are generated by `tools.py`); decide whether `.mmd` should be public |
| 13 | Low | Probable dead CSS after the page rewrites: hero/diagram-placeholder/anchor-sentence/flow/reasons/skeptic-box, argument-spine/domain-header/paper-list/open-questions, `.wdt-faq-*`, `.avoid-intro`/`.strategy-*`/`.mechanic`/`.verdict-box`, `.wdt-marquee`, `.wdt-diagram-tabset`, `.wdt-tool-panel/inner/header`, `svg-pan-zoom.min.js` | `grep` the built HTML before deleting |
| 14 | Low | `_ABBREV_TO_CANONICAL["BEHAVB"] = "BEHAVE.B"` is a typo; `internal_bibliography.md` description says `[BEHAVE.A]` (should be `BEHAV.A`) | Fix both |
| 15 | Low | `build_and_render.bat` hardcodes `C:\Users\kyleo\...\Quarto\bin`; `zenodo_upload.py` opens its log in `print/` which must already exist | Parametrise or document; `mkdir` the directory |

---

## Adding a new paper: checklist
1. Add the source `.md` with front matter (`shortcode`, `title`, `status`, `keywords`, optional `jel`, `zenodo_doi`) and a `### Revision History` table with at least one row.
2. Add the entry to `registry/papers.yml`.
3. `python pipeline/scrape_contents.py --dry-run`, then `--write`.
4. `python pipeline/build_anchors.py`.
5. Add the paper record to `registry/internal.json` (`internal_papers`). **Required for the Link Map node.**
6. Add to the sidebar in `site/_quarto.yml`; add to the Papers menu if it is a main paper.
7. Add to `SECTION_ORDER` (and relevant `READING_PATHS`) in `pages/corpus.py`.
8. Add to `_GROUPS` in `link_map.py` and `SECTION_ORDER` in `pdf.py`.
9. Update `research.md`, `Project-Map.md`, `internal_bibliography.md`, and the paper-count strings.
10. After PDF build and Zenodo upload, `zenodo_doi:` is written to the source file automatically.

## Adding a new calculator: checklist
1. Create `site/tools/{name}_calc.html` as a clean body fragment; fetch runtime files by absolute `/model/` path.
2. Add an entry to `TOOLS` in `pipeline/tools.py`.
3. Put any `.py`/`.toml` runtime files in `model/` and list them in `_quarto.yml` `resources:`.
4. Add the page to the Tools menu and to `calculator_index.md`.
5. Add any CSS to `tools.css` (and a dark override in `dark.css` if it uses hardcoded light colours).

## Known constraints
- Quarto sidebar sections only expand interactively on that paper's own page.
- Runtime `.py`/`.toml` files are public by design.
- `mmdc` must be installed locally on Windows: `npm install -g @mermaid-js/mermaid-cli`.
- `anchors.yml` is gitignored; regenerate after a fresh clone.
