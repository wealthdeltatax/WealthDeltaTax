# Site design: navigation, hub layout and reader routing

Brief 021s, part of 013g stage D. Status: design draft for the guru; the guru merges it with the sibling files into `website/notes/site.md`. Design only: nothing is built, no prose or value is written. The author answered the 12 questions of section 10 on 2026-11-17; section 10 records the decisions.

Read: `website/notes/map.md` (sections 1 to 3 and 7), `website/notes/template.md` (sections 1, 2, 6), `shortcodes.md`, `ids-map.md`, `website/notes/site/ids.md` (017s, merged), and the current navigation in `website/site/_quarto.yml` (names only). Decisions the design did not own were numbered questions; section 10 records the author's answers.

## 1. What the site is after the restructure

One hub, 15 menu spokes, 4 spokes reached from a parent (DECL, BEHAV, WELF, ATTR), a data layer, 3 standalone papers and a few utility pages. Page ids are the shortcodes of `shortcodes.md` (the S numbers are planning labels, `ids-map.md`). Every menu spoke is one click from any page; every other page is at most two clicks from the hub. Section 9 proves it page type by page type.

| Before (current `website/site/_quarto.yml`) | After |
|---|---|
| A navbar "Papers" menu listing 33 papers in 9 themed groups, plus a docked sidebar of about 40 entries | A navbar with five items; the 15 menu spokes in one menu; no sidebar of papers |
| A numbered series: core, literature, mechanism, modelling, robustness, welfare, implementation, political | Hub plus questions: each spoke is titled by the reader's question |
| A table of contents on every long paper | A fixed four-anchor jump bar on every spoke; an "On this page" list on the hub only |
| "How To Navigate", "Project Map" and FAQ pages as entry points | The reader routing block in the hub (section 4) is the entry point; the three old pages stay live under Resources, Pending review, until the author decides (Q3) |
| Tables of numbers in papers and a Comparison Tables page | Figures with reference tables in each spoke's Data block (template 6a); no table in the prose |
| Per-paper revision history | The run metadata of the data layer; no revision narrative in a spoke (template writing rule 3) |

## 2. Page types and layout

| Type | Count | Source | Nav entry | Cap on size |
|---|---|---|---|---|
| Hub | 1 | the whitepaper file, sections H0 to H7 | brand link, `Home` | 5,000 to 7,000 words (map section 1) |
| Spoke | 15 | spoke file, four parts | `Questions` menu | 6,000 words counted prose |
| Parent-reached spoke | 4 (DECL under VAL, BEHAV and WELF under PAY, ATTR under CORP) | spoke file, registry `type: appendix` with a `parent` | from its parent only | 6,000 |
| Data-layer page | DL0 to DL6 and one DL1 page per manifest output (`ids.md`) | generated from the manifest, register and run file | `Data` menu | none |
| Standalone paper | 3 (ADD, INST, SCOPE) | spoke shape (author, 017s Q5a) | `Papers` menu | 6,000 |
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
[breadcrumb: Hub > FISC]                                  status chip if draft
H1  The reader question (the spoke title)               e.g. "What rate, what threshold, how much?"
[Short answer block: 80 to 150 words, visually distinct]
[Jump bar: Short answer | Evidence | Strongest objection | Data]    same four anchors on every spoke
[More-detail line, if any: "More detail: DECL Declaration incentives"]
Evidence                H2 sections, each opening with its claim; figures from figure blocks
[Strongest objection block, boxed]
[Data block]            generated, section 7 of hooks.md
[Read next block]       section 6
[footer]
```

- The short answer comes first and the whole answer fits above the fold on a phone at 360 px width without the navbar (the navbar collapses).
- The prerequisites line sits under the short answer: "Assumes: MECH, VAL" from the front matter `depends`, linked.
- Anchors: `#short-answer`, `#evidence`, `#strongest-objection`, `#data`; the builder wraps the Evidence H2 sections in one `section` with the id.
- No on-page contents list. The jump bar is the replacement and is the same on every spoke, so a reader learns it once.
- A figure's reference table sits in the Data block, in a `details` element closed on screen (Q8), opened in print, and linked from the figure caption by the caption's `Data: Table F-<spoke>-<n>` string.

### 2.3 Parent-reached spoke

The same layout and the same four parts, with its own front matter, cap and Data block. Differences:

- The breadcrumb reads `Hub > VAL > DECL`.
- A banner under the title: "More detail for VAL, <parent question>. The parent spoke stands without it." with a link up.
- No appendix of its own, and no navbar entry. It appears in the parent's More-detail line, in the parent's Read next block, and in search (Q6).
- Its Short answer states what the appendix adds, not the parent's answer.

### 2.4 Data-layer pages

Page ids, URLs and contents are those of `ids.md`: DL0 (`/data.html`, what the layer holds and how to read a number), DL1 (`/data/outputs.html`, index of outputs) and one DL1 page per manifest output (`/data/<id>.html`), DL2 inputs (`/data/inputs.html`), DL3 metrics, DL4 method (`/data/method.html`), DL5 downloads and run record, DL6 UK data pack; reference tables as CSV at `/data/csv/<table id>.csv`. This file adds only the navigation:

- The navbar `Data` item is a menu of DL0 to DL6, so each is one click from the hub and a DL1 output page is two.
- Each DL1 output page lists the spokes that cite the output (the manifest `element`), so a reader can go back to them.
- DL2 keeps a stable anchor per input row (`#i-d4b`).
- DL4 is the target of hub section H7.

Layout: DL0 (title, run block, how to read a number, links to DL1 to DL6) is the only data page with a sketch of its own; the others are a heading, a short paragraph and one table. Tables scroll horizontally inside their own wrapper on mobile (section 7). Links from a spoke's Data block go straight to the DL pages, so a reader is one click from the numbers.

### 2.5 Standalone paper

ADD, INST and SCOPE use the spoke shape (four parts, jump bar, Data block), as the author decided for 017s (Q5a); they sit outside the wheel. Additions:

- A banner under the title: "Standalone paper. The argument in the hub does not depend on it." with a link to the hub, and for SCOPE: "Outside the argument; sets the project's boundaries."
- URLs unchanged (`add.html`, `inst.html`, `scope.html`), so existing citations stay valid.
- They follow the spoke checker and hooks like any spoke.
- A standalone paper may link into any spoke. A spoke may link to a standalone paper but never relies on it for the argument (map section 1).

### 2.6 Utility pages

| Page | Notes |
|---|---|
| References, Glossary | keep as generated pages (`references.qmd`, glossary); linked from the footer and the `Resources` menu |
| Retired papers (RET in `ids.md`) | one generated table: old shortcode, title, the spoke or spokes that absorbed it. The old papers are removed and their URLs are not redirected (Q5) |
| Pending pages | FAQ, Comparison Tables, Project Map, How To Navigate, Avoidance, Corporate Levy, Flowcharts, Link Map, Internal Bibliography, Revision History: stay live at their current URLs, unchanged, until the author decides each one (Q3); the dispositions proposed in `ids.md` are the starting point for that decision |
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
| `Questions` | the 15 menu spokes in registry order, each as "FISC Rates and revenue" (label) with the question as the second line on desktop | 1 |
| `Data` | a menu of DL0 to DL6 | 1 |
| `Papers` | ADD, INST, SCOPE | 1 |
| `Resources` | References, Glossary, Retired papers, Calculators (labelled old model), and a Pending review group listing the ten pending pages | 1 |
| `About` | the author page | 1 |

Rules:

- Parent-reached spokes are not in any menu. They are reached from their parent (two clicks from the hub).
- DL pages are one click from the hub through the `Data` menu, DL1 output pages two (through DL1), and any of them one click from a spoke's Data block.
- No docked sidebar. The 40-entry sidebar is deleted; the navbar already reaches every spoke from every page.
- Draft spokes appear in the menu with a "draft" mark until `status` is `accepted`; the mark comes from front matter.
- The menu is generated from the page registry (section 5), so adding or renaming a spoke edits one data file.

URLs (decided, Q2): flat and lowercase, the shortcode lower-cased (`ids-map.md`, `ids.md` rule 3).

| Page | URL |
|---|---|
| Hub | `index.html` |
| Spoke FISC, parent-reached DECL | `fisc.html`, `decl.html` |
| Data | as `ids.md`: `data.html`, `data/outputs.html`, `data/<id>.html`, `data/inputs.html`, `data/method.html`, `data/csv/<table id>.csv` |
| Standalone | `add.html`, `inst.html`, `scope.html` |
| Utility | `references.html`, `glossary.html`, `retired.html`, `author_page.html` |

## 4. The reader routing block

The routing block is data, not prose. It lives in the hub (H6) and, filtered, in every spoke's Read next block.

### 4.1 Data file

`website/site/data/routing.yml`, hand-written, read by the build. Content from `map.md` section 3:

```yaml
routes:
  - id: economist
    reader: "Economist"
    prompt: "I want to check the mechanism and the numbers."
    start: [VAL, FISC, PAY, data]
  - id: lawyer
    reader: "Tax lawyer or administrator"
    prompt: "I want to know what is taxed, how it is valued and who runs it."
    start: [MECH, VAL, GOV]
  - id: policy
    reader: "Policymaker or adviser"
    prompt: "I want revenue, the fund, adoption and the wider effects."
    start: [FISC, FUND, POL, FIRST, WIDER]
  - id: business
    reader: "Business owner or accountant"
    prompt: "I want to know how firms are treated and how my wealth is valued."
    start: [CORP, VAL]
  - id: sceptic
    reader: "Philosopher or sceptic"
    prompt: "I want the case for fairness, what exists already, and how it could fail."
    start: [FAIR, LIT, UNCER, LIMIT, FALS]
  - id: researcher
    reader: "Researcher wanting the numbers"
    prompt: "I want the data first."
    start: [data, FISC]
```

(The `prompt` lines are placeholders for the writing lane; the reader labels are the map's, verbatim. The `start` lists are the map's with S ids read through `ids-map.md`: S11 becomes FIRST and WIDER and S12 becomes UNCER, LIMIT and FALS, so two routes have five entries.)

| Field | Type | Rule |
|---|---|---|
| `id` | string | unique, lowercase, used as an anchor |
| `reader` | string | the label shown; the map's wording |
| `prompt` | string, optional | one sentence in the reader's voice; no number, no hook, at most 20 words |
| `start` | list of page ids | 1 to 5 entries, no duplicates; each is a spoke shortcode or the token `data` (DL0); the first entry is the entry point |
| `order` | integer, optional | display order; default is file order |

### 4.2 Checks (build)

| Check | Level |
|---|---|
| every `start` id exists in the page registry | error |
| every route has a `reader` and a non-empty `start` | error |
| every menu spoke is an entry in at least one route (today all 15 are) | error |
| a route that includes a spoke without its `depends` earlier in the same route | warning (FISC depends on MECH and VAL; the policy route omits both, and the spoke page states its prerequisites) |
| `prompt` over 20 words, or containing a digit | error |

### 4.3 Rendering

- **Hub (H6):** all routes, as cards in a two-column grid on desktop and one column on mobile. A card shows the reader label, the prompt, and the ordered start list as links. Link text is the spoke's question from its front matter, with the id as a small chip; the first link is the primary button. The token `data` renders as "The numbers" linking to DL0. The cards carry no number and no hook.
- **Spoke, Read next block:** only the routes that contain this spoke, one line each: "If you are a <reader>: next, <next entry's question>". The next entry is the entry after this spoke in that route's `start`; the last entry shows "Back to the hub".
- **404:** the hub link and the cards.
- **Standalone papers:** one line under the cards in H6: "Related papers, not needed for the argument:" and the three paper links.

## 5. Page registry

The menu, breadcrumbs, routing and the retired-papers table read `literature/pages.yml` (decided, Q7). Its page list and fields are fixed in `ids.md` rule 7 (`id`, `type`, `title`, `url`, `source`, `status`, `parent`, `aliases`). Navigation adds two fields:

| Field | Type | Rule |
|---|---|---|
| `label` | string | menu text, 1 to 4 words (the map's names: "Rates and revenue") |
| `order` | integer | menu order; the 15 menu spokes have `order` 1 to 15 |

Rules: a page of `type: appendix` has a `parent` that is a menu spoke; a menu spoke has none; every id appears once. The spoke's title and `status` are read from its own front matter (the title is its `question:`), so spoke front matter gains no `label` field. `aliases` holds one entry only: `wp.html` on the hub (Q1, Q5).

## 6. Links, search, and finding the hub and the next step

**Spoke to spoke.** A cross-reference uses the shortcode form `(FISC §2)`, which resolves to the spoke's anchor.

**Spoke to the data layer.** Two paths: the Data block's rows (output page links, input register links, literature keys) and any hook value, which renders as plain text with no link (a link on every number would crowd the prose; the Data block row carries the link). The Replicate row of the Data block links each DL1 output page.

**A reader who lands on any page finds the hub and the next step by four routes:**

1. The brand link at top left is the hub on every page.
2. The breadcrumb on every spoke and appendix names the hub.
3. The Read next block at the foot of every spoke gives the next spoke per route, and the hub.
4. The 404 page and the standalone-paper banner both link to the hub.

**Search.** Keep Quarto's built-in static search, moved to the navbar (the sidebar is gone). The index covers the hub, spokes, parent-reached spokes, standalone papers, utility pages and the DL pages; it excludes `_build` placeholders and the CSV files. Each spoke's meta description is built from its question and the first sentence of its Short answer, at most 155 characters, so a result shows the answer.

## 7. Mobile and print

**Mobile.**
- The navbar collapses to a menu; `Questions` opens as one list of 15.
- The Short answer is the first block after the title.
- The jump bar is a single row that scrolls sideways.
- Routing cards stack in one column.
- Tables sit in a wrapper with horizontal scroll; figure reference tables are in closed `details` elements.
- Tap targets are at least 44 px high. Not checked here: any measured performance or accessibility score.

**Print.**
- A print stylesheet hides the navbar, search, jump bar, Read next block and footer menus.
- It opens every `details` so each Data block table prints.
- Header: the page title and the draft banner if present. Footer: the page URL, the run date and the manifest version.
- A spoke prints alone; the spokes reached from it do not print with it.
- PDFs per spoke are out of scope (Q9); the existing PDF pipeline is separate and untouched.

## 8. What the site no longer has, and what replaces it

| Gone | Replaced by |
|---|---|
| The numbered series of 33 papers and their appendices as peers | 1 hub and 19 spokes (15 in the menu, 4 reached from a parent); old shortcodes appear only on the retired papers page |
| The themed "Papers" mega-menu and the docked sidebar | the five-item navbar (section 3) |
| Per-paper tables of contents | the fixed jump bar (spokes), the on-page list (hub only) |
| "How To Navigate" and "Project Map" as the entry points | the routing block (section 4) and the hub's H0 and H6; the two pages stay live, pending (Q3) |
| Tables in prose | figures with reference tables in the Data block; the Comparison Tables page stays live, pending (Q3) |
| Per-paper revision history | the run record (DL0 and DL5); a spoke carries no revision narrative |
| Typed model numbers | hooks resolved from the data file |
| Old paper URLs (`wp.html`, `rates.html` and so on) | nothing: the retired papers are removed and their URLs end; `wp.html` alone redirects to the hub (Q1, Q5) |

Pages whose disposition is not decided stay live until the author decides each one (Q3).

## 9. Reachability check

Click depth from the hub, using the navbar that every page carries.

| Page | Path | Clicks |
|---|---|---|
| any menu spoke | hub, `Questions`, spoke (or a routing card) | 1 |
| any parent-reached spoke | hub, parent, More-detail link | 2 |
| DL0 to DL6 | hub, `Data` menu (DL4 also from H7) | 1 |
| one output's DL1 page | hub, `Data` menu, DL1, output row | 2 |
| standalone paper | hub, `Papers`, paper | 1 |
| references, glossary, retired papers | hub, `Resources`, page | 1 |
| about | hub, `About` | 1 |
| pending pages, calculators | hub, `Resources`, page | 1 |

Longest path is 2 clicks. Pages: the hub; 19 spokes; the data layer of `ids.md` (DL0 to DL6 and one page per manifest output, about 34 once the added outputs join); 3 standalone papers; REFS, GLOSS, RET, about and 404; 10 pending pages (Q3); 3 calculators (Q4).

## 10. Decisions

The author answered all twelve on 2026-11-17. Each line states the decision and what it fixes in this file.

1. **Hub is the home page.** The hub is `index.html`; `wp.html` redirects to it; the current plain-English overview is replaced by H0. This is the only redirect on the site. It is later than 017s and supersedes the `/whitepaper.html` hub row and the HOME landing page of `ids.md`.
2. **URL scheme.** Flat and lowercase as in section 3; standalone paper URLs unchanged; data-layer URLs are those of `ids.md` (`/data/<id>.html`, `/data/inputs.html#i-d4b`).
3. **Pages with no home in the restructure documents.** Decide page by page later. The ten pages in section 2.6 stay live and unchanged at their current URLs, listed under Resources, Pending review. The author notes they may be rewritten or removed once the data and papers are done. The navbar of section 3 does not change when they go.
4. **Calculators.** Kept under Resources, labelled "Based on the retired model", and updated to the newest model when it is done. No new work in this design.
5. **Old paper URLs.** No redirects. The old papers are removed permanently, superseded by the new ones, and their URLs end (the author accepts that existing citations, including Zenodo, will not resolve). The retired papers page stays as a generated old-to-successor table; the `successor` field in `website/registry/papers.yml` feeds that table only, and the Quarto `aliases` check is dropped. This is later than 017s and supersedes its redirect rows and milestone M2, except the single `wp.html` alias.
6. **Parent-reached spokes (DECL, BEHAV, WELF, ATTR).** Reached from the parent only; in no menu; included in search.
7. **Page registry.** `literature/pages.yml` as in `ids.md` rule 7, with `label` and `order` added; title and `status` are read from spoke front matter, so the template front matter gains no `label` field.
8. **Data block tables.** The Data block's summary rows are visible; each figure's reference table is in a `details` element, closed on screen and open in print.
9. **PDF per spoke.** Not now; the print stylesheet is enough, and the existing PDF pipeline is untouched.
10. **Routing prompts.** The prompt lines in section 4.1 are placeholders; the writing lane drafts the final ones and the author approves them.
11. **Hub contents list.** The hub keeps an on-page contents list of its eight sections; spokes keep only the four-anchor jump bar.
12. **Standalone papers.** The hub links to them only in the line under the routing cards and in the Papers menu; each carries a banner saying it is not needed for the argument; no spoke's Short answer links to one.

### For the guru: follow-through on files this brief does not touch

- `ids.md`: remove the HOME row and make the hub `/` (Q1); drop rule 8, the old-paper redirect rows, milestone M2 and the Zenodo line that says old links keep working, keeping only the `wp.html` alias (Q5); the dispositions for research, corpus, FAQ, link map and the other pending pages are superseded by Q3 until the author decides each.
- `hooks.md`: the link placeholders of Q14 (`data/outputs/<ID>.html`) read `/data/<id>.html` (`ids.md`).
- `project/STATUS.md` and the lane plan: 021s is no longer waiting for the author.

## 11. Checks run

| Check | Result |
|---|---|
| Every page type has a layout | section 2 (hub, spoke, parent-reached spoke, data, standalone, utility) |
| Routing block is a data file with fields | section 4.1, rules in 4.2; the six routes are the map's section 3 |
| Every page within two clicks of the hub | section 9 (longest path 2) |
| Standalone papers and data layer have a stated place | sections 2.4, 2.5, 3 |
| Every menu spoke is in a route | all 15 appear in the six routes (checked by hand against the list) |
