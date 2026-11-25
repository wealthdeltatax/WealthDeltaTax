# Site IDs, URLs and the fate of the old registry (brief 017s, stage D)

> **Ids (author, 2026-11-17).** Spoke shortcodes (`website/notes/shortcodes.md`) are the page ids, URLs, front-matter `spoke:` values and figure and table ids. Where this file still writes `S1` to `S12`, read it through `website/notes/ids-map.md`; the S numbers are planning labels only.

> **Questions.** All proposed answers in this file's question section were accepted by the author on 2026-11-17 (nothing else reads `site-index.json`), except where `ids-map.md` overrides the S ids. Guru follow-through done the same day: `outputs.yml` carries `unit`, `decimals`, `horizons`, `by` maps and `series` (hooks Q1 to Q4); the template's table label is `F-<spoke>-<n>` and its example is an output the spoke owns (hooks Q13, checker Q14 and Q17).

Status: design only, drafted 2026-11-17, waiting for the author on the questions in section 8. Builds nothing. The guru merges this file into `website/notes/site.md` with its siblings (`hooks.md`, `figures.md`, `spoke-checker`, `nav.md`).

> **Q5a and Q5b (author, 2026-11-17, asked directly, later than the note above).** Q5a: the three standalone papers (ADD, INST, SCOPE) move to the new spoke shape now, not kept in the old one. Q5b: the 30 retired numbered source files move to `docs/archive/papers/`, not deleted. Sections 3, 5, 6 and 7 are updated for these two; the other nine answers stand as proposed. If the earlier note and this one disagree on Q5a or Q5b, this one is the author's answer.


Inputs read: `website/registry/papers.yml`, `website/registry/contents.yml`, `pipeline/` (file names and module docstrings), `website/site/_quarto.yml`, `website/site/pages/`, `website/notes/map.md` (sections 4 and 7), `ledger.md` (sections 1, 7, 8), `ledger-sections.md` (redirect weights only), `template.md`, `model-specs/outputs.yml`, brief 007w. Nothing in the live site was fetched; current URLs are taken from `papers.yml` (`<output>.html` at the site root) and `_quarto.yml`.

## 1. The scheme (rules this file fixes)

1. **One id per page, permanent.** An id is never reused, renamed or recycled after a page retires. A spoke that splits keeps its id for the main page and adds `-A`, `-B` for the new pages.
2. **Id families.**

   | Family | Pattern | Meaning |
   |---|---|---|
   | Hub | `H` (page); `H0` to `H7` (sections) | the whitepaper |
   | Spoke | `S1` to `S12` | one reader question |
   | Appendix spoke | `S<n>-<letter>`, e.g. `S6-A`, `S6-B` | overflow of a spoke (map section 7); letters in order of creation |
   | Standalone | `ADD`, `INST`, `SCOPE` | papers outside the wheel; old shortcodes kept |
   | Data layer | `DL0` to `DL6`; `DL1-<output id>` | generated pages on the model and its inputs |
   | Site | `HOME`, `GLOSS`, `REFS`, `RET` | pages that are not argument |

   `DL` is chosen because `D1` to `D11` are the driver ids in `drivers.md` and the input register, and `D-H1a` is a data-fact id in the H1 work. `S1` is also the metric id of the property-tax sensitivity in `metrics.md` (its output is `OS1`): spoke `S1` and metric `S1` are different things. Rule: prose and cross-references cite output ids only (`OS1`), never metric ids; the generated data pages print the metric as "metric S1".
3. **URL = lower-case id, `.html`, at the site root**, dots and hyphens as today (`val-a.html`, `lr-a.html`). Data layer pages sit under `/data/`. The id is the URL, so a reader or an agent can go from `(S6-A)` to `/s6-a.html` without a lookup. The reader question is the page title, not part of the URL: questions get reworded, URLs do not.
4. **Anchors inside a page are written by the build, not by Quarto's slugger.** The hub gets `#h0` to `#h7` on its eight sections. In a spoke the build gives each H2 an explicit id `<id>-<n>` by position (`#s5-2` for the second H2 of S5; `#s6-a-1` in S6-A). `(S5 §2)` resolves to `/s5.html#s5-2`. Today `build_anchors.py` re-implements Quarto's slug rules and has 307 stale anchors (brief 007w); explicit ids remove that class of error. Figures keep `#fig-S5-1`, their tables `#F-S5-1` (template 6a).
5. **Cross-reference grammar** (for the spoke checker, 020w, to fix): fully bracketed, `(S5)`, `(S5 §2)`, `(S6-A §1)`, `(H3)`, `(DL2)`, `(DL1-O1)`, and `(ADD §3)` for a standalone. Proposed pattern: `H[0-7] | S\d{1,2}(-[A-Z])? | DL\d(-O[A-Za-z0-9]+)? | ADD | INST | SCOPE`, each with an optional ` §N`. The pattern in `check_wdt_format.py` (`[A-Z][A-Za-z]*(\.[A-Z])?`) cannot match `S5` or `S6-A`, so the old checker cannot be reused for spokes.
6. **Source files.** Hub and spokes live in `source/` as `papers/legacy/hub.md`, `papers/legacy/s5.md`, `papers/legacy/s4-a.md`, named as their URL. The 33 numbered files stay where they are until their paper retires (section 6).
7. **Page registry.** One new file, `literature/pages.yml`, lists every hand-written page: `id`, `type` (hub, spoke, appendix, standalone, data, site, legacy), `title`, `url`, `source`, `status` (draft, author-review, accepted, legacy), `parent` (for appendices), `aliases` (old URLs that redirect here). Per-output data pages are not listed: the build creates one per manifest entry (section 2).
8. **Redirects.** GitHub Pages cannot send HTTP 301. Quarto's `aliases:` front-matter key writes a small page with a meta refresh and a canonical link at each old URL; the build emits it from `aliases` in `pages.yml`. This is the only mechanism proposed; no new service or workflow.

## 2. Every new page

Titles of main spokes are the questions in `map.md` section 4. The four appendix titles are working titles; the spoke's `question:` front matter has the last word (`template.md` section 1).

| Id | Title | URL | Type |
|---|---|---|---|
| H | The Wealth Delta Tax (whitepaper); sections H0 to H7 at `#h0` to `#h7` | `/whitepaper.html` | hub |
| S1 | Is it fair? | `/s1.html` | spoke |
| S2 | What exists, what is missing? | `/s2.html` | spoke |
| S3 | What exactly is taxed and when? | `/s3.html` | spoke |
| S4 | How is wealth measured? | `/s4.html` | spoke |
| S4-A | Declaration incentives | `/s4-a.html` | appendix |
| S5 | What rate, what threshold, how much? | `/s5.html` | spoke |
| S6 | Who pays, what do they do? | `/s6.html` | spoke |
| S6-A | What taxpayers do (behaviour) | `/s6-a.html` | appendix |
| S6-B | Welfare comparison | `/s6-b.html` | appendix |
| S7 | Where does the money go? | `/s7.html` | spoke |
| S8 | How are firms treated? | `/s8.html` | spoke |
| S8-A | Entity attribution | `/s8-a.html` | appendix |
| S9 | Who runs it, on what law? | `/s9.html` | spoke |
| S10 | Can it pass, how is it staged? | `/s10.html` | spoke |
| S11 | What are the wider effects? | `/s11.html` | spoke |
| S12 | How could it be wrong? | `/s12.html` | spoke |
| ADD | Addendums | `/add.html` | standalone (URL unchanged) |
| INST | Institutional Selection | `/inst.html` | standalone (URL unchanged) |
| SCOPE | Scope and Boundaries | `/scope.html` | standalone (URL unchanged) |
| DL0 | The data layer (what it holds, how to read a number) | `/data.html` | data |
| DL1 | Outputs (index of every output) | `/data/outputs.html` | data, generated |
| DL1-`<id>` | One page per output in the manifest: title, summary form, schedules, horizons, `by` keys, value tables, the spokes that cite it. Today 21 entries (O1 to OP6); the 2026-11-17 decisions add OH1a to OH1c, OW1 to OW3 and seven manifest items, about 34 | `/data/<id lower-case>.html`, e.g. `/data/o1.html`, `/data/o2b.html`, `/data/oh1a.html` | data, generated |
| DL2 | Input register (every `{{i:}}` name, value, unit, source) | `/data/inputs.html` | data, generated from `inputs.md` |
| DL3 | Metrics and reading rules (summary forms, horizons, rule A2) | `/data/metrics.html` | data, generated from `metrics.md` |
| DL4 | Method (model v3 in prose; the method notes the ledger moved to the data layer, e.g. the O7 note) | `/data/method.html` | data, hand-written |
| DL5 | Downloads and run record (data file, CSVs, manifest version, country pack, run date) | `/data/downloads.html` | data, generated |
| DL6 | UK data pack (JUR data tables, gaps, provenance) | `/data/uk-pack.html` | data, hand-written from JUR |
| HOME | Home (a short landing page that points to H; content in `nav.md`) | `/` | site |
| GLOSS | Glossary | `/glossary.html` | site, generated |
| REFS | References | `/references.html` | site, generated |
| RET | Where the old papers went (section concordance) | `/retired.html` | site, generated, new |

Reserved, not pages: reference tables as CSV at `/data/csv/<table id>.csv` (for example `/data/csv/F-S5-1.csv`); the data file and figure asset paths belong to `hooks.md` and `figures.md`. Unchanged and outside this scheme: `/model/taxpayer.html`, `/model/revenue.html`, `/model/ldw.html`, `/calculator_index.html`, `/flowcharts.html`, `/author_page.html`, `/404.html`, `/site-index.json`, `CNAME`, `robots.txt`, `BingSiteAuth.xml`.

The reader routing block (H6) names spokes by id; `nav.md` owns it.

## 3. The 33 old papers

Rule for the target: the spoke that receives the most kept or merged words (K and M rows in `ledger-sections.md`); an appendix goes to the matching appendix spoke where `map.md` section 7 names one, otherwise to its parent's target; the whitepaper goes to the hub. Kept words are the ledger's, which predate the S4, S6 and S8 splits, so the splits are applied from `map.md` section 7. The action for every paper that does not stay is **redirect**: `aliases:` on the target page, so the old URL lands on the target. No old paper is kept as an archived page (question Q2). Section-level targets for every old section (980 rows) are the content of RET.

| Old | Old URL | Action | New page | Basis (kept words by target, from the ledger) |
|---|---|---|---|---|
| WP | `/wp.html` | redirect | H | whitepaper to hub; its words go to S3, S4, S2, S6 |
| MF | `/mf.html` | redirect | S1 | S1 4,254 |
| LR.A | `/lr-a.html` | redirect | S2 | S2 3,302 |
| LR.B | `/lr-b.html` | redirect | S2 | S2 3,656 |
| JUR | `/jur.html` | redirect | S9 | S9 2,262; data tables to DL6 (2,775) |
| VAL | `/val.html` | redirect | S4 | S4 11,312 |
| VAL.A | `/val-a.html` | redirect | S4-A | map section 7; method note for O7 to DL4 |
| VAL.B | `/val-b.html` | redirect | S4-A | S4 4,798, appendix routing |
| CORP | `/corp.html` | redirect | S8 | S8 5,863 |
| CORP.A | `/corp-a.html` | redirect | S8-A | S8 7,289; ENT (6,498) is S8-A |
| GOV | `/gov.html` | redirect | S9 | S9 7,405 |
| GOV.A | `/gov-a.html` | redirect | S12 | S12 1,688 |
| GOV.B | `/gov-b.html` | redirect | S7 | S7 1,026, S9 692 |
| RATES | `/rates.html` | redirect | S5 | S5 4,875 |
| RATES.A | `/rates-a.html` | redirect | S5 | no kept words; parent's target |
| SWEEPS | `/sweeps.html` | redirect | S5 | S5 10,160 |
| SWEEPS.A | `/sweeps-a.html` | redirect | S5 | no kept words; parent's target |
| BEHAV | `/behav.html` | redirect | S6-A | S6 5,133; map section 7 puts BEHAV in S6-A |
| BEHAV.A | `/behav-a.html` | redirect | S6-A | S6 1,199 |
| CLOSE | `/close.html` | redirect | S3 | S3 5,520 |
| POL | `/pol.html` | redirect | S10 | S10 5,489 |
| POL.A | `/pol-a.html` | redirect | S1 | S1 1,693 (kept material is philosophical; the author may prefer S10) |
| PHASE1 | `/phase1.html` | redirect | S10 | S10 4,706 |
| ENV | `/env.html` | redirect | S11 | S11 6,394 |
| FM | `/fm.html` | redirect | S10 | S10 2,985 |
| MOD | `/mod.html` | redirect | S10 | S10 1,655 |
| SCOPE | `/scope.html` | keep URL | SCOPE | standalone (ledger SA) |
| ADD | `/add.html` | keep URL | ADD | standalone (ledger SA) |
| WFR | `/wfr.html` | redirect | S6-B | map section 7; ledger S6 12,674 |
| WFR.A | `/wfr-a.html` | redirect | S6-B | no kept words; parent's target |
| INST | `/inst.html` | keep URL | INST | standalone (ledger SA, 14,264) |
| LDW | `/ldw.html` | redirect | S11 | S11 3,914, S6 1,618 |
| FAL | `/fal.html` | redirect | S12 | S12 11,360 |

Counts: 30 redirects, 3 URLs kept. The three standalone papers keep their ids and URLs and move to the new (spoke) shape now (author, Q5a): their `pages.yml` entries are `type: standalone`, `status: legacy` until each is rewritten, and from then on they take positional section ids (`#add-2`), the spoke reference grammar and the spoke checker.

Side effects the redirects do not cover:
- A fragment in an old link (`wp.html#the-tax-base`) is lost: a meta refresh does not carry it. RET gives the section-level answer. Accepted unless Q3 says otherwise.
- The 33 Zenodo records still point at the old site URLs and old DOIs until the author replaces them (author, 2026-11-17: "replaced later"). Their site links keep working through the redirects.
- The PDF button and Cite panel (`inject_front_matter`) disappear with the paper pages; hub and spokes get their own, when `pdf.py` and `zenodo_upload.py` are redesigned (Q10).

## 4. Other hand-written site pages

| Page | Today | Fate | Where it goes |
|---|---|---|---|
| `index.md` (`/`) | landing; says "32 working papers" | change | HOME: short landing to H (`nav.md`) |
| `research.md` (`/research.html`) | "How to navigate" the 33 papers | retire, redirect | `/whitepaper.html#h6` (the routing block) |
| `corpus.html` (generated "All Papers") | reading paths over 33 papers | retire, redirect | `/whitepaper.html#h6` |
| `faq.md` | twelve objections, links to papers | hold, then fold (Q7) | proposed: H5 and S12, then redirect to `/whitepaper.html#h5` |
| `comparison-tables.md` | WDT against realisation and stock wealth tax, WFR results | hold, then fold (Q7) | proposed: S6-B, redirect |
| `avoidance.md` | six decisions to minimise liability, embeds a calculator | hold, then fold (Q7) | proposed: S6-A, redirect; the calculator embed stays until replaced |
| `corporate-levy-taxpayer.md` | corporate levy credits for listed holders | hold, then fold (Q7) | proposed: S8, redirect |
| `Project-Map.md` | positions per paper, open questions, shortcode definitions | retire (Q6) | redirect to `/s12.html`; the register is rebuilt in `docs/` by the guru |
| `calculator_index.md`, `/model/*.html` | three calculators on the v1 core | keep (Q8) | unchanged until a v3 calculator replaces each |
| `internal_bibliography.md` | Zenodo citations of the 33 papers | keep until Zenodo is replaced, then retire (Q10) | |
| `revision_history.md` | pre-publication history of the old papers | keep | linked from RET as the record of the old series |
| `author_page.md`, `404.qmd` | | keep; 404 changes to point at H | |
| `flowcharts.html` (generated) | five mechanism diagrams | keep | nav decides placement |
| `link-map.html` (generated) | force graph of the 33 papers | retire, redirect to `/whitepaper.html` | nodes come from `internal.json` `internal_papers`; nothing to draw once the papers go |

## 5. Registry, generated files and scripts

Fates: **keep**, **change**, **retire**. "At cutover" means at the step in section 7 where the last legacy paper retires; until then the legacy tools run for the legacy papers.

| File | Role today | Fate | Detail |
|---|---|---|---|
| `website/registry/papers.yml` | source to output mapping, 33 entries | retire at M1 | replaced by `literature/pages.yml`, which carries the 33 as `type: legacy` entries at first |
| `literature/pages.yml` | | new | section 1, rule 7 |
| `website/registry/contents.yml` | headings of 33 papers; feeds anchors, glossary, site-index | retire at cutover | tracked until then; spokes need no contents file because the build reads their headings |
| `literature/anchors.yml` (generated, ignored) | `PAPER§N` to `page#anchor` | retire at cutover | spokes get build-time ids (rule 4) |
| `website/registry/crosslinks.json` (generated) | index of links and issues | retire at cutover | not used by the site build; replaced by the spoke checker's report, written to `_build/` |
| `literature/references.bib` | external bibliography, Quarto `bibliography:`, PDF and Zenodo | keep | `{{lit:KEY}}` reads it; the research role keeps maintaining it |
| `literature/references.json` (generated) | | keep | still generated by `bib_to_json.py` |
| `literature/internal.json` | `internal_papers`, `citations` (365), `flags` (17) | change | keep `flags`; drop `internal_papers` and `citations` at cutover; "Cited in" on the references page is computed from the spokes' `{{lit:}}` keys at build instead of kept by hand |
| `literature/redirects.yml` | | not needed | aliases live in `pages.yml` (rule 7) |
| `website/registry/retired.yml` | | new | old section to new page, converted once from `ledger-sections.md` (980 rows); frozen; feeds RET |
| `website/registry/glossary.yml` | | new (Q11) | term, definition, home spoke; seeded once from the 276-word whitepaper glossary and the other papers' glossary sections (ledger DL rows) |
| `website/site/pages/glossary.md` (generated) | | keep as output | built from `glossary.yml` after cutover |
| `website/site/pages/Project-Map.md` | | retire (Q6) | section 4 |
| `project/agents/reference/writing/style-guide.md` | prose rules and the post-update crosslink workflow | change | prose rules stay; the shortcode table and crosslink workflow retire at cutover (guru, writing role) |
| `project/briefs/open/007w-crosslink-repair.md` | repair crosslinks in the old papers | retire | obsolete: the papers are rewritten, not repaired; the guru writes the decisions entry |
| `website/build/config.py` | paths, `extract_paper_meta`, link map from `contents.yml` | change | load `pages.yml`; `extract_paper_meta` stays for legacy and standalone papers until cutover |
| `website/build/preprocess.py` | orchestrator; reads `papers.yml` | change | reads `pages.yml`; branches on `type`; new steps are in `hooks.md` and `figures.md` |
| `website/build/transforms.py` | `convert_crossrefs`, `inject_front_matter` | change | new reference grammar (rule 5); `inject_front_matter` for hub and spokes without revision-table parsing |
| `website/build/scrape_contents.py` | headings to `contents.yml` | retire at cutover | |
| `website/build/build_anchors.py` | `contents.yml` to `anchors.yml` | retire at cutover | |
| `website/build/build_glossary.py` | per-paper Glossary sections to `glossary.md` | change | reads `glossary.yml`; keeps its feature of linking each term to the spokes that use it |
| `website/build/wdt_crosslinks.py` | scan, check, query, remap for the old shape | retire at cutover | its `remap` idea is worth carrying into the spoke checker (positional section ids, section 8 Q1) |
| `website/build/check_wdt_format.py` | format checker, old paper shape | retire at cutover | cannot check spokes (rule 5); the spoke checker (020w) also covers the three standalones once rewritten (Q5a) |
| `website/build/pages/corpus.py` | All Papers page | retire at cutover | |
| `website/build/pages/references.py` | References page | change | `_ABBREV_TO_CANONICAL` and "Cited in" links retarget to spoke ids |
| `website/build/pages/site_index.py` | `site-index.json` | change | same URL, new schema (`version: 2`, pages and hooks instead of papers); no known consumer beyond the site itself (Q9) |
| `website/build/link_map.py` | link-map page | retire at cutover | |
| `website/build/diagrams.py`, `tools.py`, `bib_to_json.py` | flowcharts, calculators, references.json | keep | unchanged |
| `website/build/pdf.py`, `website/build/zenodo_upload.py` | PDF and Zenodo builds for papers | keep, untouched for now | `project/agents/agent-web.md` says not to touch them; their redesign for hub and spokes is Q10 |
| `.github/workflows/deploy.yml` | runs scrape, glossary, anchors, preprocess, render | change at cutover | drop "Scrape contents" and "Build anchors"; add hook, figure and checker steps when `hooks.md`, `figures.md` and the checker land |
| `website/site/_quarto.yml` | navbar and sidebar listing 33 papers | change | nav is `nav.md`'s; until cutover the 33-paper lists stay |
| `website/wdt-site-architecture.md` | | change | updated at every step in section 7 (web role rule) |
| `_build/figures/` (copy of `model_v1/OUTPUTS/`) | legacy figures | retire at cutover | |

## 6. What happens to the old source files

At cutover the 30 retired numbered files in `source/` are no longer built. Decided (Q5b): the 30 retired numbered files move to `docs/archive/papers/` (a `git mv`, so history follows); the three standalone files stay in `source/` until rewritten. `docs/archive/` is already off the agents' reading list, so the move costs no reading; it keeps about 340,000 words in the tree. A git tag before the move (`old-series-2026-11`) is still advised as a cheap marker. Nothing in `source/` is touched by this brief.

## 7. Migration order (the site deploys at every step)

`main` deploys on every push, so every step is a branch that leaves `main` building and the live pages unchanged except where stated. After each step run `website/build/build_and_render.bat` locally (AGENTS.md rule for site changes) and compare the list of files in `_site/`.

| Step | What changes | Live site after the step | Check |
|---|---|---|---|
| M0 | Stage D designs merged into `site.md`; author answers the questions below | unchanged | none (docs only) |
| M1 | `literature/pages.yml` created with the 33 legacy entries plus the new page ids as `status: draft`; `config.py` and `preprocess.py` read it; `papers.yml` removed | identical | `_site/` file list and the 33 paper HTML files are identical to before apart from build timestamps |
| M2 | `aliases` generation from `pages.yml`; `website/registry/retired.yml` and the RET generator, not yet linked or populated with live redirects | identical | a unit check with one fixture alias; no old URL changes yet |
| M3 | Page types built from fixtures: hub, spoke, appendix and data-layer templates, hook resolver, Data block, figure renderer, spoke checker (briefs 018s, 019s, 020w, 021s). Fixture pages are `draft` and excluded from the deployed site, or published as in Q4 | identical (fixtures not deployed) | release build fails on an unresolved hook; fixture spoke passes the checker |
| M4 | Data layer pages DL0 to DL6 and the per-output pages published, from the manifest, `inputs.md` and `metrics.md`; no values yet (no run), so output pages show the manifest only | new `/data/` pages added; nothing removed | internal links on the new pages resolve; `[[…]]` placeholders never appear on a deployed page |
| M5 (repeated, one per group, after the data gate opens and the author accepts) | Add the accepted hub or spokes at `status: accepted`; add `aliases` for the old papers that group replaces and put them in `retired.yml`; turn that group's old pages into redirects | each group: new pages live, matching old URLs redirect | every old URL in the group returns the redirect page; the link check on the rest of the site passes; references to a retired shortcode inside live old papers resolve to the new page without a fragment, and the old crosslink check reports them as warnings, not errors |
| M6 (cutover) | Last legacy paper retired; nav switched to `nav.md`; HOME, `research`, `corpus`, `link-map` and the folded site pages redirect; legacy tools and registry files removed (section 5); workflow steps dropped; `check_wdt_format.py` retired; glossary from `glossary.yml` | final structure | no `type: legacy` entry remains; `_site/` has no page without an id; the architecture doc matches |

Group order for M5 follows the writing order, which is stage E's decision. The only dependency this design adds: the hub is accepted last or together with S3, because every retired paper's redirect and RET row point at pages that must exist.

## 8. Questions for the author

**All eleven answered 2026-11-17.** Accepted as proposed: Q1, Q2, Q3, Q4, Q6, Q7, Q8, Q9, Q10, Q11. Changed by the author: **Q5a** (standalones move to the new shape now, not kept in the old one) and **Q5b** (old sources move to `docs/archive/papers/`, not deleted). The text below is the record of each question; section 3 and the tables above are updated for Q5a and Q5b.

**Q1. Positional or named section ids in spokes?** `(S5 §2)` means "second H2 of S5". Reordering sections silently changes what a reference points at, and the resolver cannot know. *Proposed:* keep positional ids as `template.md` has them; once a spoke is `accepted`, a section move or insertion runs a remap over every reference to that spoke (the idea of `wdt_crosslinks.py remap`), and the spoke checker refuses a build whose accepted spoke changed its H2 order without a remap file. If you prefer named ids (`(S5 §rates-threshold)`), `template.md` rule 7 changes.

**Q2. Old paper pages: redirect only, or keep archived copies?** You said the old papers are done away with and Zenodo records get replaced later. *Proposed:* no archived page on the site; the 30 redirects, RET, the git tag in Q5b, and the Zenodo records are the record. This also avoids the old papers staying indexed beside the new series.

**Q3. Lost fragments.** Links from outside the site to a section of an old paper (`wp.html#…`) land on the target page top, not the section. *Proposed:* accept; RET lists every old section against its new page for anyone who needs it. A script on each redirect page that forwards the fragment to RET is possible but not proposed.

**Q4. Do draft pages publish?** The template marks drafts (`status: draft`, `[[O2.mean@…]]` placeholders) and the release build fails on unresolved hooks, but a draft hub is not something to show readers. *Proposed:* `draft` and `author-review` pages build, carry a visible Draft banner and `noindex`, are absent from nav, sitemap and RET, and are published to the live URL so you can read them on any device (the site is the only preview there is; no new workflow). Alternative: drafts build only locally.

**Q5. Standalone papers.** (a) ADD, INST and SCOPE keep their ids and URLs. Should they keep the old paper shape (numbered sections, `(ADD §3)` references, `check_wdt_format.py`) until you rewrite them? *Proposed:* yes; spokes and the hub never link into them for the argument (map section 1), but may cite them as `(ADD §3)`; their `registry` entry stays in the old form until they are rewritten. (b) Tag the repository and delete the 30 retired source files at cutover? *Proposed:* yes, tag `old-series-2026-11` first; alternative `docs/archive/papers/`, which keeps about 340,000 words in the tree.

**Q6. Project Map.** `website/site/pages/Project-Map.md` (84 KB) holds positions per paper, the open-questions register and shortcode definitions, and `project/OVERVIEW.md` and `framework.md` point at it. The papers it describes retire. *Proposed:* retire the public page at cutover, redirect to `/s12.html`, and the guru rebuilds the positions and open-questions register under `docs/` for hub and spokes before then. Say if you want a public register.

**Q7. FAQ, comparison tables, avoidance guide, corporate levy page.** They carry reader-facing material (and v1 numbers) not in the 33 papers' ledger. *Proposed:* leave all four untouched until the data gate, then fold each into the spoke named in section 4 and redirect; the ledger has no rows for them, so the guru adds a short disposition table for these four pages first. Alternative: keep the FAQ as a permanent page.

**Q8. Calculators.** Taxpayer and LDW calculators run Pyodide on the v1 core (`wdt_core.py`, `ldw_core.py`, `WDT_Params.toml`) published under `/model/`; you decided on 2026-11-16 that the revenue calculator is replaced after model v3. *Proposed:* leave all three at their URLs until a v3 calculator replaces each, and add to brief 009c's boundary that the files Pyodide loads from `model_v1/` stay until then. This brief and its siblings do not touch them.

**Q9. `site-index.json` schema.** The endpoint's `papers` and `anchors` keys describe the old series. *Proposed:* keep the URL, change the schema to `version: 2` (pages, sections, hooks, outputs), no shim for the old keys. Is anything outside this repo reading it?

**Q10. PDF and Zenodo for hub and spokes.** `pdf.py` and `zenodo_upload.py` assume `extract_paper_meta()` and numbered papers. *Proposed:* leave both untouched now; a later brief decides whether hub and each spoke get a PDF and a Zenodo record, and whether the internal bibliography page then regenerates or retires.

**Q11. Glossary source.** `build_glossary.py` reads a `# Glossary` section in each old paper; spokes do not have one (a spoke defines a term in a clause where it uses it). *Proposed:* one hand-kept `website/registry/glossary.yml` (term, definition, home spoke), seeded once from the ledger's glossary rows (about 12,300 words of glossary rows across the papers, deduplicated to the longest per term), and `build_glossary.py` keeps linking each term to the spokes that use it. Alternative: no glossary page.

## 9. Checks run

| Check | Result |
|---|---|
| Every old paper has an action | 33 rows in section 3: 30 redirect, 3 keep; count matches `papers.yml` (33) |
| Shortcodes against source front matter | 33 shortcodes read from `source/*.md`; all appear in section 3 |
| Every new page has id, title, URL, type | section 2 |
| Id collisions | `D1` to `D11` (drivers), `D-H1a` (data facts), `S1` (metric), `H1` and `OH1a`, `F-S5-1`, `fig-S5-1` checked; `DL` prefix and the output-id rule remove the clashes |
| Every registry, generated and pipeline file has a fate | section 5 (registry and pipeline listed in the repo today, plus the three new files) |
| Migration keeps the site deployable | section 7, one check per step |
| Touches | this file and brief 017's progress block only |
| Author answers applied | Q5a and Q5b change sections 3, 5, 6 and 7; the other nine need no change |
