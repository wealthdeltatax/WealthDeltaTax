# Site design: navigation, hub layout and reader routing

Brief 021s, part of 013g stage D. Status: design draft for the guru; the guru merges it with the sibling files into `docs/restructure/site.md`. Design only: nothing is built, no prose or value is written. The author answered the 12 questions of section 10 on 2026-11-17; section 10 records the decisions.

Read: `docs/restructure/map.md` (sections 1 to 3 and 7), `docs/restructure/template.md` (sections 1, 2, 6), and the current navigation in `site/_quarto.yml` (names only). Decisions the design did not own were numbered questions; section 10 records the author's answers.

## 1. What the site is after the restructure

One hub, 12 main spokes, 4 appendix spokes, a data layer, 3 standalone papers and a few utility pages. All spokes are one click from any page. Every other page is at most two clicks from the hub. Section 9 proves it page type by page type.

| Before (current `site/_quarto.yml`) | After |
|---|---|
| A navbar "Papers" menu listing 33 papers in 9 themed groups, plus a docked sidebar of about 40 entries | A navbar with five items; the 12 spokes in one menu; no sidebar of papers |
| A numbered series: core, literature, mechanism, modelling, robustness, welfare, implementation, political | Hub plus questions: each spoke is titled by the reader's question |
| A table of contents on every long paper | A fixed four-anchor jump bar on every spoke; an "On this page" list on the hub only |
| "How To Navigate", "Project Map" and FAQ pages as entry points | The reader routing block in the hub (section 4) is the entry point; the three old pages stay live under Resources, Pending review, until the author decides (Q3) |
| Tables of numbers in papers and a Comparison Tables page | Figures with reference tables in each spoke's Data block (template 6a); no table in the prose |
| Per-paper revision history | The run metadata of the data layer; no revision narrative in a spoke (template writing rule 3) |

## 2. Page types and layout

| Type | Count | Source | Nav entry | Cap on size |
|---|---|---|---|---|
| Hub | 1 | the whitepaper file, sections H0 to H7 | brand link, `Home` | 5,000 to 7,000 words (map section 1) |
| Spoke | 12 | spoke file, four parts | `Questions` menu | 6,000 words counted prose |
| Appendix spoke | 4 (S4-A, S6-A, S6-B, S8-A) | spoke file with id suffix `-A`, `-B` | from its parent only | 6,000 |
| Data-layer page | 1 index, 1 per output (21 now), inputs, method | generated from the manifest, register and run file | `Data` | none |
| Standalone paper | 3 (ADD, INST, SCOPE) | old paper shape, kept | `Papers` menu | none |
| Utility | references, glossary, retired papers, about, 404 | hand-written or generated | footer and `Resources` menu | none |

Layouts below are described top to bottom. A phrase in brackets is a block the builder generates.

### 2.1 Hub

```
[navbar]
H1  Title of the whitepaper                       status chip if draft
H0  One-page summary (problem, the tax, three results by hook, where to go next)
[On this page: H1 The problem ... H7 Data and method]   right margin on desktop, collapsed on mobile
H1  The problem
H2  The tax in one page
H3  What it does          three headline results as P10, mean, P90 by named schedule (figures)
H4  Why it is fair
H5  How it could be wrong
H6  Where to go next      [reader routing block]  then one line to the standalone papers
H7  Data and method       links to the data layer
[footer: References, Glossary, About, run date and manifest version]
```

The hub does not use the four-part spoke shape and carries no Data block of its own: H7 links to the data layer, and any hook in H0 or H3 appears in a short generated "Numbers on this page" list at the foot of the page (the same row builder as the spoke Data block, section 7 of `hooks.md`, restricted to the Outputs cited, Run and Replicate rows). The hub is long, so it is the one page type that keeps an on-page contents list, with eight entries.

### 2.2 Spoke

```
[navbar]
[breadcrumb: Hub > S5]                                  status chip if draft
H1  The reader question (the spoke title)               e.g. "What rate, what threshold, how much?"
[Short answer block: 80 to 150 words, visually distinct]
[Jump bar: Short answer | Evidence | Strongest objection | Data]    same four anchors on every spoke
[Appendices line, if any: "More detail: S4-A Declaration incentives"]
Evidence                H2 sections, each opening with its claim; figures from figure blocks
[Strongest objection block, boxed]
[Data block]            generated, section 7 of hooks.md
[Read next block]       section 6
[footer]
```

- The short answer comes first and the whole answer fits above the fold on a phone at 360 px width without the navbar (the navbar collapses).
- The prerequisites line sits under the short answer: "Assumes: S3, S4" from the front matter `depends`, linked.
- Anchors: `#short-answer`, `#evidence`, `#strongest-objection`, `#data`; the builder wraps the Evidence H2 sections in one `section` with the id.
- No on-page contents list. The jump bar is the replacement and is the same on every spoke, so a reader learns it once.
- A figure's reference table sits in the Data block, in a `details` element closed on screen (Q8), opened in print, and linked from the figure caption by the caption's `Data: Table F-<spoke>-<n>` string.

### 2.3 Appendix spoke

The same layout and the same four parts, with its own front matter, cap and Data block. Differences:

- The breadcrumb reads `Hub > S4 > S4-A`.
- A banner under the title: "Appendix to S4, <parent question>. The main spoke stands without it." with a link up.
- No appendix of its own, and no navbar entry. It appears in the parent's Appendices line, in the parent's Read next block, and in search (Q6).
- Its Short answer states what the appendix adds, not the parent's answer.

### 2.4 Data-layer pages

| Page | URL (decided, Q2) | Content |
|---|---|---|
| Data index | `data/index.html` | run metadata (manifest version, country pack, run date, status); one table of all outputs: id, title, spokes that cite it, link; links to the inputs page, the method page and the CSV downloads |
| Output page | `data/outputs/<id>.html`, lowercase id | title and definition (one sentence from the metric register), unit, summary form; the spokes that cite it (from the manifest `element`); a table of every cell (schedules by horizons by `by` values); download of the output's CSV; link back to each citing spoke |
| Inputs page | `data/inputs.html` | the 89-row input register as a filterable table with a stable anchor per row (`#i-d4b`), the source table S1 to S43 with licences, and the country coverage column (this is the UK data pack) |
| Method page | `data/method.html` | the metric register, range design, reading rules and the model description; the target of hub section H7 |

Layout: the data index is the only page with a sketch of its own (title, run block, outputs table, three links). The others are a heading, a short paragraph and one table. The tables scroll horizontally inside their own wrapper on mobile (section 8). Links from a spoke's Data block go straight to these pages, so a reader is one click from the numbers.

### 2.5 Standalone paper

The old paper layout is kept for ADD, INST and SCOPE: the page title, the paper's own table of contents (these are the only pages that keep one), the body, and the paper's references. Additions:

- A banner under the title: "Standalone paper. The argument in the hub does not depend on it." with a link to the hub, and for SCOPE: "Outside the argument; sets the project's boundaries."
- URLs unchanged (`add.html`, `inst.html`, `scope.html`) so existing citations stay valid.
- Exempt from the spoke checker and from hooks (they use the old format check, `check_wdt_format.py`).
- A standalone paper may link into any spoke. A spoke may link to a standalone paper but never relies on it for the argument (map section 1).

### 2.6 Utility pages

| Page | Notes |
|---|---|
| References, Glossary | keep as generated pages (`references.qmd`, glossary); linked from the footer and the `Resources` menu |
| Retired papers | one generated table: old shortcode, title, the spoke or spokes that absorbed it. The old papers are removed and their URLs are not redirected (Q5) |
| Pending pages | FAQ, Comparison Tables, Project Map, How To Navigate, Avoidance, Corporate Levy, Flowcharts, Link Map, Internal Bibliography, Revision History: stay live at their current URLs, unchanged, until the author decides each one (Q3) |
| Calculators | the three existing calculators stay on their current URLs, labelled "Based on the retired model", and are updated to the newest model when it is done (Q4) |
| About the author and contacts | keep; navbar `About` |
| 404 | keeps the hub link and the routing block |

## 3. Navigation

Flat: one level from the hub. The navbar is the same on every page.

```
[brand: The WDT -> hub]  Questions v   Data v   Papers v   Resources v   About        [search]
```

| Item | Contents | Click depth from the hub |
|---|---|---|
| Brand, `Home` | the hub | 0 |
| `Questions` | the 12 main spokes, in order, each as "S5 Rates and revenue" (label) with the question as the second line on desktop | 1 |
| `Data` | opens the data index | 1 |
| `Papers` | ADD, INST, SCOPE | 1 |
| `Resources` | References, Glossary, Retired papers, Calculators (labelled old model), and a Pending review group listing the ten pending pages | 1 |
| `About` | the author page | 1 |

Rules:

- Appendix spokes are not in any menu. They are reached from their main spoke (two clicks from the hub).
- Output and inputs pages are reached from the data index (two clicks), and directly from any spoke's Data block (one click from the spoke).
- No docked sidebar. The 40-entry sidebar is deleted; the navbar already reaches every spoke from every page.
- Draft spokes appear in the menu with a "draft" mark until `status` is `accepted`; the mark comes from front matter.
- The menu is generated from the page registry (section 5), so adding or renaming a spoke edits one data file.

URLs (decided, Q2): flat and lowercase, as today (`rates.html`, `lr-a.html`).

| Page | URL |
|---|---|
| Hub | `index.html` |
| Spoke S5, appendix S4-A | `s5.html`, `s4-a.html` |
| Data | `data/index.html`, `data/outputs/o2.html`, `data/inputs.html`, `data/method.html`, `data/csv/<id>.csv` |
| Standalone | `add.html`, `inst.html`, `scope.html` |
| Utility | `references.html`, `glossary.html`, `retired.html`, `author_page.html` |

## 4. The reader routing block

The routing block is data, not prose. It lives in the hub (H6) and, filtered, in every spoke's Read next block.

### 4.1 Data file

`site/data/routing.yml`, hand-written, read by the build. Content from `map.md` section 3:

```yaml
routes:
  - id: economist
    reader: "Economist"
    prompt: "I want to check the mechanism and the numbers."
    start: [S4, S5, S6, data]
  - id: lawyer
    reader: "Tax lawyer or administrator"
    prompt: "I want to know what is taxed, how it is valued and who runs it."
    start: [S3, S4, S9]
  - id: policy
    reader: "Policymaker or adviser"
    prompt: "I want revenue, the fund, adoption and the wider effects."
    start: [S5, S7, S10, S11]
  - id: business
    reader: "Business owner or accountant"
    prompt: "I want to know how firms are treated and how my wealth is valued."
    start: [S8, S4]
  - id: sceptic
    reader: "Philosopher or sceptic"
    prompt: "I want the case for fairness, what exists already, and how it could fail."
    start: [S1, S2, S12]
  - id: researcher
    reader: "Researcher wanting the numbers"
    prompt: "I want the data first."
    start: [data, S5]
```

(The `prompt` lines are placeholders for the writing lane; the reader labels and `start` lists are the map's, verbatim.)

| Field | Type | Rule |
|---|---|---|
| `id` | string | unique, lowercase, used as an anchor |
| `reader` | string | the label shown; the map's wording |
| `prompt` | string, optional | one sentence in the reader's voice; no number, no hook, at most 20 words |
| `start` | list of page ids | 1 to 4 entries, no duplicates; each is a main spoke id, an appendix id, or the token `data` (the data index); the first entry is the entry point |
| `order` | integer, optional | display order; default is file order |

### 4.2 Checks (build)

| Check | Level |
|---|---|
| every `start` id exists in the page registry | error |
| every route has a `reader` and a non-empty `start` | error |
| every main spoke is an entry in at least one route (today all 12 are) | error |
| a route that includes a spoke without its `depends` earlier in the same route | warning (S5 depends on S3 and S4; the policy route omits both, and the spoke page states its prerequisites) |
| `prompt` over 20 words, or containing a digit | error |

### 4.3 Rendering

- **Hub (H6):** all routes, as cards in a two-column grid on desktop and one column on mobile. A card shows the reader label, the prompt, and the ordered start list as links. Link text is the spoke's question from its front matter, with the id as a small chip; the first link is the primary button. The token `data` renders as "The numbers" linking to the data index. The cards carry no number and no hook.
- **Spoke, Read next block:** only the routes that contain this spoke, one line each: "If you are a <reader>: next, <next entry's question>". The next entry is the entry after this spoke in that route's `start`; the last entry shows "Back to the hub".
- **404:** the hub link and the cards.
- **Standalone papers:** one line under the cards in H6: "Related papers, not needed for the argument:" and the three paper links.

## 5. Page registry

The menu, breadcrumbs, routing and the retired-papers table read one registry: `registry/pages.yml` (decided, Q7). Hand-maintained for hub, data, standalone and utility pages; for spokes it holds only the fields front matter does not (label, order, parent), and the build reads `question` and `status` from the spoke's own front matter so there is one source for them.

| Field | Type | Rule |
|---|---|---|
| `id` | string | `hub`, `S1` to `S12`, `S4-A`, `S6-A`, `S6-B`, `S8-A`, `data`, `ADD`, `INST`, `SCOPE`, utility ids; unique |
| `type` | enum | `hub`, `spoke`, `appendix`, `data`, `standalone`, `utility` |
| `label` | string | menu text, 1 to 4 words (the map's names: "Rates and revenue") |
| `parent` | id | appendix only; must be a main spoke |
| `url` | string | derived from the id by the rule in section 3 unless overridden |
| `order` | integer | menu order |

Rules: an appendix has a `parent` that is a main spoke; a main spoke has none; every page id appears exactly once; the 12 main spokes have `order` 1 to 12.

## 6. Links, search, and finding the hub and the next step

**Spoke to spoke.** A cross-reference uses the shortcode form `(S5 §2)`, which resolves to the spoke's anchor.

**Spoke to the data layer.** Two paths: the Data block's rows (output page links, input register links, literature keys) and any hook value, which renders as plain text with no link (a link on every number would crowd the prose; the Data block row carries the link). The Replicate row of the Data block links each output page.

**A reader who lands on any page finds the hub and the next step by four routes:**

1. The brand link at top left is the hub on every page.
2. The breadcrumb on every spoke and appendix names the hub.
3. The Read next block at the foot of every spoke gives the next spoke per route, and the hub.
4. The 404 page and the standalone-paper banner both link to the hub.

**Search.** Keep Quarto's built-in static search, moved to the navbar (the sidebar is gone). The index covers the hub, spokes, appendix spokes, standalone papers, utility pages and data index and output pages; it excludes `_build` placeholders and the CSV files. Each spoke's meta description is built from its question and the first sentence of its Short answer, at most 155 characters, so a result shows the answer.

## 7. Mobile and print

**Mobile.**
- The navbar collapses to a menu; `Questions` opens as one list of 12.
- The Short answer is the first block after the title.
- The jump bar is a single row that scrolls sideways.
- Routing cards stack in one column.
- Tables sit in a wrapper with horizontal scroll; figure reference tables are in closed `details` elements.
- Tap targets are at least 44 px high. Not checked here: any measured performance or accessibility score.

**Print.**
- A print stylesheet hides the navbar, search, jump bar, Read next block and footer menus.
- It opens every `details` so each Data block table prints.
- Header: the page title and the draft banner if present. Footer: the page URL, the run date and the manifest version.
- A spoke prints alone; its appendices do not print with it.
- PDFs per spoke are out of scope (Q9); the existing PDF pipeline is separate and untouched.

## 8. What the site no longer has, and what replaces it

| Gone | Replaced by |
|---|---|
| The numbered series of 33 papers and their appendices as peers | 1 hub, 12 questions, 4 appendices; old shortcodes appear only on the retired papers page |
| The themed "Papers" mega-menu and the docked sidebar | the five-item navbar (section 3) |
| Per-paper tables of contents | the fixed jump bar (spokes), the on-page list (hub only) |
| "How To Navigate" and "Project Map" as the entry points | the routing block (section 4) and the hub's H0 and H6; the two pages stay live, pending (Q3) |
| Tables in prose | figures with reference tables in the Data block; the Comparison Tables page stays live, pending (Q3) |
| Per-paper revision history | run metadata on the data index; a spoke carries no revision narrative |
| Typed model numbers | hooks resolved from the data file |
| Old paper URLs (`wp.html`, `rates.html` and so on) | nothing: the retired papers are removed and their URLs end; `wp.html` alone redirects to the hub (Q1, Q5) |

Pages whose disposition is not decided stay live until the author decides each one (Q3).

## 9. Reachability check

Click depth from the hub, using the navbar that every page carries.

| Page | Path | Clicks |
|---|---|---|
| any main spoke | hub, `Questions`, spoke (or a routing card) | 1 |
| any appendix spoke | hub, spoke, appendix link | 2 |
| data index | hub, `Data` (or H7) | 1 |
| output page | hub, `Data`, output row | 2 |
| inputs page, method page | hub, `Data`, link | 2 |
| standalone paper | hub, `Papers`, paper | 1 |
| references, glossary, retired papers | hub, `Resources`, page | 1 |
| about | hub, `About` | 1 |
| pending pages, calculators | hub, `Resources`, page | 1 |

Longest path is 2 clicks. Pages: 1 hub, 12 spokes, 4 appendices, 1 data index, 21 output pages (the manifest's 21 entries; more if the proposed outputs of `docs/model-v3/added/` join), inputs, method, 3 standalone, 5 utility (references, glossary, retired papers, about, 404), 10 pending pages (Q3) and 3 calculators (Q4): 62 pages with the manifest as it stands.

## 10. Decisions

The author answered all twelve on 2026-11-17. Each line states the decision and what it fixes in this file.

1. **Hub is the home page.** The hub is `index.html`; `wp.html` redirects to it; the current plain-English overview is replaced by H0. This is the only redirect on the site.
2. **URL scheme.** Flat and lowercase as in section 3; standalone paper URLs unchanged; output and input pages `data/outputs/o2.html` and `data/inputs.html#i-d4b`. This also settles the link targets asked in Q14 of `hooks.md`.
3. **Pages with no home in the restructure documents.** Decide page by page later. The ten pages in section 2.6 stay live and unchanged at their current URLs, listed under Resources, Pending review. The author notes they may be rewritten or removed once the data and papers are done. The navbar of section 3 does not change when they go.
4. **Calculators.** Kept under Resources, labelled "Based on the retired model", and updated to the newest model when it is done. No new work in this design.
5. **Old paper URLs.** No redirects. The old papers are removed permanently, superseded by the new ones, and their URLs end (the author accepts that existing citations, including Zenodo, will not resolve). The retired papers page stays as a generated old-to-successor table; the `successor` field in `registry/papers.yml` feeds that table only, and the Quarto `aliases` check is dropped.
6. **Appendix spokes.** Reached from the parent only; in no menu; included in search.
7. **Page registry.** `registry/pages.yml` holds ids, labels, order and parent; `question` and `status` are read from spoke front matter, so the template front matter gains no `label` field.
8. **Data block tables.** The Data block's summary rows are visible; each figure's reference table is in a `details` element, closed on screen and open in print.
9. **PDF per spoke.** Not now; the print stylesheet is enough, and the existing PDF pipeline is untouched.
10. **Routing prompts.** The prompt lines in section 4.1 are placeholders; the writing lane drafts the final ones and the author approves them.
11. **Hub contents list.** The hub keeps an on-page contents list of its eight sections; spokes keep only the four-anchor jump bar.
12. **Standalone papers.** The hub links to them only in the line under the routing cards and in the Papers menu; each carries a banner saying it is not needed for the argument; no spoke's Short answer links to one.

## 11. Checks run

| Check | Result |
|---|---|
| Every page type has a layout | section 2 (hub, spoke, appendix, data, standalone, utility) |
| Routing block is a data file with fields | section 4.1, rules in 4.2; the six routes are the map's section 3 |
| Every page within two clicks of the hub | section 9 (longest path 2) |
| Standalone papers and data layer have a stated place | sections 2.4, 2.5, 3 |
| Every main spoke is in a route | all 12 appear in the six routes of the map (checked by hand against the list) |
