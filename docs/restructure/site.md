# Site and pipeline requirements (013g stage D, merged)

Brief 026g, stage A. Status: draft for the author; stage B (`order.md`) starts only after the author approves this file and answers section 7. Design only: nothing here is built and no spoke or hub prose is written. This file replaces nothing: the five sibling files stay the detailed record, and where this file and a sibling disagree, this file's section 6 (settled) or section 7 (open) says which holds.

Siblings: [ids](site/ids.md) (017s), [hooks](site/hooks.md) (018s), [figures](site/figures.md) (019s), [checker](site/checker.md) (020w), [nav](site/nav.md) (021s). Supporting: [shortcodes](shortcodes.md), [ids-map](ids-map.md), [template](template.md), `docs/model-v3/outputs.yml` (version `stage-A5-falsifiability-elements-2026-11-17`).

## 1. The site in one page

One hub (`index.html`, sections H0 to H7), 15 menu spokes, parent-reached spokes (DECL, BEHAV, WELF, ATTR, and, if Q4 is accepted, ADOPT, PILOT, HYPO), 3 standalone papers (ADD, INST, SCOPE), a generated data layer (DL0 to DL6 and one page per manifest output), and utility pages. Page ids are the shortcodes of `shortcodes.md`. Every spoke is the same four parts: Short answer, Evidence, Strongest objection, generated Data block. No number is typed in prose: a hook (`{{o:...}}`) is resolved from one data file at build, and the Data block lists every value, input and figure a page uses.

```
model v3 run --> outputs.json ----+
inputs.md --> inputs.json --------+--> hook resolver --> spoke HTML (draft or release)
metrics.md, outputs.yml ----------+        |                 ^
lit-figures.yml, references.bib --+        +--> Data block --+--> figure renderer (SVG, table, CSV)
registry/pages.yml, routing.yml --> navbar, breadcrumbs, routing, redirects
spoke .md --> spoke checker (source mode, then build mode)
```

## 2. Ids and URLs (ids.md, nav.md section 3)

- **Id and URL.** The shortcode is the page id. URL is the lower-cased id at the site root (`fisc.html`); front matter and file use the upper-case id (`spoke: FISC`, `source/spokes/FISC.md`). Hub is `index.html`; `wp.html` is the only redirect on the site (nav Q1, Q5).
- **Sections and figures.** The build writes explicit ids: `#fisc-2` for the second Evidence H2, `#h0` to `#h7` on the hub. Figures `fig-FISC-1`, tables `F-FISC-1`. Cross-references `(FISC §2)`, `(H3)`, `(DL2)`, `(DL1-O1)`.
- **Data layer.** `data.html` (DL0), `data/outputs.html`, `data/<id lower-case>.html` per output, `data/inputs.html#i-d4b`, `data/metrics.html`, `data/method.html`, `data/downloads.html`, `data/uk-pack.html`; reference tables as `data/csv/<table id>.csv`.
- **Registry.** `registry/pages.yml` lists every hand-written page: `id`, `type`, `title`, `url`, `source`, `status`, `parent`, `aliases`, plus `label` and `order` (nav). It replaces `registry/papers.yml`. New files: `retired.yml` (old section to new page, feeds the retired-papers page only), `glossary.yml`, `inputs.json` (generated), `inputs-display.yml`, `lit-figures.yml`, `figure-style.yml`, `routing.yml`.
- **Old files.** Legacy registry and pipeline files retire at cutover (ids section 5); the 30 retired numbered sources move to `docs/archive/papers/`; ADD, INST and SCOPE stay in `source/` until rewritten.

## 3. Hooks, data file and builds (hooks.md)

- **Grammar.** `{{o:ID[.STAT][@SCHEDULE][/HORIZON][#KEY:VALUE,...]}}`, `{{i:ID[.STAT]}}`, `{{ref:fig-CODE-N}}`, `{{lit:KEY}}`; fixed order `.` `@` `/` `#`. Defaults come from front matter. A hook counts as one word.
- **Data file.** `model_v3/OUTPUTS/outputs.json`, generated, never hand-edited, copied to `_build/data/`. Top level `run` (manifest version, country pack, date, `status: provisional|final`, `inputs_sha256`, `fixture`) and one entry per output with p10, mean, p90 (or point, lo, hi) per schedule, horizon and `by` key. Validator rules V1 to V12; error codes H01 to H42.
- **Resolution.** Manifest membership, `element:` membership (rule R1 forward), summary-form check of STAT, schedule and horizon discipline, then format by unit tag. A hook that cannot resolve renders `[[...]]` in draft and fails in release.
- **Builds.** `WDT_MODE=draft|release` (default draft). The deploy workflow stays on draft until the data gate opens. A draft page carries a banner and a placeholder count; `_build/hooks-report.json` lists every unresolved hook.
- **Data block.** Generated at the foot of every spoke: Outputs cited, Figures, Reference tables, Run, Inputs, Literature figures, Reading note (60 words, front matter `reading_note`), Replicate. Reference tables are HTML (`F-CODE-N`) and CSV; summary rows are visible and each table is in a closed `details` (open in print).
- **Other inputs.** `registry/lit-figures.yml` (key, value, unit, locator, `verified`) feeds `{{lit:}}`; `registry/inputs-display.yml` gives unit tag and decimals per register row.

## 4. Figures (figures.md)

- **Renderer.** Static inline SVG from one Python module, no chart library; wide (720) and narrow (360) layouts per figure; one shared stylesheet and script on pages with a figure. Six kinds: `line`, `band`, `bar`, `dot`, `stack`, `map`; a default kind for every manifest role.
- **One data path.** A `FigureData` object built once from the data file, manifest and metric register; the SVG, the reference table and the CSV are emitted from it, and a build self-check re-reads all three and stops the build on any difference (counts, displayed values, mark positions inverted through the scale).
- **Style.** The `dataviz` palette, light and dark validated sets; three schedules as one-hue ordinal ramp, interval drawn for S_central only; categorical colours fixed per entity in `registry/figure-style.yml`; at most eight colours, three for all-pairs forms.
- **Access and print.** Alt text (form, not finding), one keyboard stop per figure with a readout from the table cells, table always in the page, forced-colours and contrast variants, print stylesheet with texture, a standalone light SVG per figure for the PDF build.
- **Tests.** Twelve fixture figures and nine cross-cutting tests (FX-*, T-*), from seeded fake data flagged `fixture: true`.

## 5. Spoke checker (checker.md) and navigation (nav.md)

**Checker.** `pipeline/check_spokes.py`, two modes: source (on save and in CI) and build (after the resolver). About 100 checks in ten families: front matter FM1 to FM12, shape PT1 to PT8, word budget WC1 to WC4, objection block OB1 to OB7, hooks HK1 to HK17, typed figures TF1 to TF3, figure blocks FG1 to FG10 and caption lint F1 to F6, cross-references XR1 to XR9, writing rules WR1 to WR12 and SA1, Data block DB1 to DB8. Severities E (fails), W, I. A spoke with `status: draft` downgrades count and coverage errors to W; `--release` makes every unresolved hook an E. A W can be waived on one line with a reason; an E never. Nineteen rules stay manual (a prose pass is a line in the change report). The old `check_wdt_format.py` runs on legacy papers until cutover.

**Navigation.** Navbar of five items (Questions, Data, Papers, Resources, About) generated from `pages.yml`; no sidebar. Spoke layout: breadcrumb, question as title, Short answer, four-anchor jump bar, Evidence, boxed objection, Data block, Read next. Parent-reached spokes carry a banner and appear only from their parent. A routing block (six reader routes, from `routing.yml`) renders as cards in hub H6 and, filtered, as Read next on each spoke. Static search in the navbar. Print stylesheet; no PDF per spoke. Every page is at most two clicks from the hub. Pending pages (ten) and calculators stay live and unchanged under Resources.

## 6. Reconciliation: settled

Each row is a point where two files overlap or disagree and the author's own recorded decisions or the file that owns the subject settle it. No author question is needed.

| # | Topic | Files | Ruling and reason |
|---|---|---|---|
| R1 | Spoke ids | `ids`, `hooks`, `figures`, `checker` write `S5`, `S6-A`; `nav` and `ids-map` use shortcodes | `ids-map.md` holds (author). Every pattern widens: spoke id `[A-Z]{3,5}` (a code from `pages.yml`), hub section `H[0-7]`, data page `DL[0-6]`, `DL1-<output id>`. The `-A` suffix and the S-form patterns (`ids.md` rule 5, `hooks.md` 4.4 `fig-(S..)`, `checker.md` FM5 and XR1) retire. The checker reads the id list from `pages.yml` |
| R2 | Hub URL and home page | `ids` row H `/whitepaper.html` plus HOME; `nav` Q1 `index.html` | `nav` Q1 holds: it states that it supersedes `ids`. Drop the HOME page and the `/whitepaper.html` row |
| R3 | Redirects | `ids` 30 redirects, milestone M2, `aliases` per paper; `nav` Q5 none but `wp.html` | `nav` Q5 holds (states it supersedes). `aliases` keeps one entry. The `successor` field lives on the legacy rows of `pages.yml` (not `papers.yml`, which retires at M1) and is frozen into `retired.yml` at cutover; the Quarto `aliases` check is dropped |
| R4 | Registry fields | `ids` rule 7 lists `title`, `status`; `nav` Q7 reads both from spoke front matter | `nav` Q7 holds for spokes: `pages.yml` carries `title` and `status` only for pages with no front matter of the spoke kind (hub, data, site, legacy, pending); a spoke row that sets either is a build error, so there is one source |
| R5 | Link to a data page | `hooks` Q14 `data/outputs/<ID>.html`; `ids`, `nav` `/data/<id>.html` | `/data/<id lower-case>.html` (`ids` section 2, `nav` follow-through) |
| R6 | Case of generated file paths | `ids` and `figures` write `F-S5-1.csv`, `fig-S5-1.svg`; URLs are lower-case | File paths are lower-case (`data/csv/f-fisc-1.csv`, `data/fig/fig-fisc-1.svg`); ids and anchors keep their case (`#F-FISC-1`). One rule: URLs lower-case, ids as written |
| R7 | Routing file location | `nav` `site/data/routing.yml`; every other registry file in `registry/` | `registry/routing.yml`; the build and the checker read `registry/` only |
| R8 | Draft and release switches | `hooks` `WDT_MODE`; `checker` `--release` and per-spoke `status` | One build switch: `WDT_MODE=release` passes `--release`. `status` still downgrades the count errors in either mode; only unresolved hooks are mode-controlled. Reverse R1 is a warning in draft and an error in release (`hooks` Q11, `checker` Q4 agree) |
| R9 | Figure block fields | `template` 6a has no `lines`, `at`, `unit`, `layout`; `checker` FG4 and FG6 assume one `by` list and one horizon | `figures` Q2 and Q3 (accepted) hold: optional `lines`, `at`, `unit`, `layout`; `by` is a key of the manifest `by` map; `horizon` is omitted for a year path, a list for facets, one value otherwise. FG4, FG6 and FG9 follow. Template edit is guru follow-through (section 9) |
| R10 | Alt-text lint | `figures` adds F7; `checker` FG8 is weaker | FG8 absorbs F7 (length 20 to 250, starts with a form word, no result words, no number of three digits except a year) |
| R11 | Hook grammar details | `checker` Q10 uses `.lo`, `.hi` on inputs; `hooks` Q8 `.low`, `.central`, `.high` | `hooks` owns the grammar: `low`, `central`, `high`, `range`. `checker` HK9 follows |
| R12 | Output id pattern | `hooks` 4.1 regex `O[A-Z]?[0-9]+[a-z]?` cannot match `DH1a`, `CK1` or `OH1b2` (all in the manifest) | Widen to `[A-Z]{1,2}[0-9]+[a-z]?[0-9]?`; `{{o:CK1}}` resolves from `checks:` (`checker` Q8). The manifest, not a pattern, is the authority (HK2) |
| R13 | Register size | `hooks` Q8 "89 register rows" | The register has 260 rows (merged 2026-11-17); `inputs-display.yml` covers all of them |
| R14 | Dropped output | `figures` section 6 draws OH1a | OH1a was dropped by the author 2026-11-17 (`outputs.yml` comment); the figure rows for it fall away. `FX-SCEN` stays as a drawing test of a two-scenario line |
| R15 | Retired shortcodes in the checker | `checker` XR1 allows old codes with a warning | Only codes the new series does not reuse (`MF`, `WP`, `LR`, `JUR`, `CLOSE`, and so on) are "retired". `VAL`, `CORP`, `GOV`, `POL`, `BEHAV`, `ADD`, `INST`, `SCOPE` always mean the new page; legacy papers keep the old checker (Q1 keeps them from colliding) |
| R16 | Standalone papers and the checker | `ids` Q5a (new shape now), `nav` 2.5 (spoke shape, checker applies) | Standalones are `type: standalone`, `status: legacy` until rewritten; the spoke checker applies from the rewrite (timing: Q8) |
| R17 | Manifest version in the sibling examples | `checker` DB4 and `figures` cite older version strings | Tests read the version from `outputs.yml`; no version string is typed into a test |

## 7. Reconciliation: questions for the author

Each has a proposed answer; this file and the briefs of section 8 assume the proposal until the author decides.

**Q1. Old and new URLs collide, and drafts publish to live URLs.** The new `val.html`, `corp.html`, `gov.html`, `pol.html`, `behav.html`, `add.html`, `inst.html` and `scope.html` are also the old papers' URLs. `ids` Q4 publishes drafts to the live URL; `ids` M5 swaps one group at a time; `nav` Q5 removes old papers with no redirect. A draft VAL would overwrite the live old VAL paper. *Proposed:* before cutover drafts publish under `/draft/<id>.html` (banner, `noindex`, not in the sitemap), with an index at `/draft/`; M5 is dropped; at cutover (M6) every accepted page goes live at its root URL in one release and the old papers are removed in the same release. The old series stays whole until then.

**Q2. Drafts in the menu.** `ids` Q4: draft pages are absent from navigation. `nav` section 3: draft spokes appear in the menu with a "draft" mark. *Proposed:* before cutover the navbar of `nav.md` does not exist (the old navbar stays) and drafts are listed only at `/draft/`; after cutover a spoke not yet `accepted` shows in the menu with the mark, as `nav` says.

**Q3. Does the hub have a Data block?** `nav` 2.1: no Data block, a short "Numbers on this page" list. `figures` Q7 (accepted): a collapsed Data block at the foot, because a figure's table must be on its page. *Proposed:* one generated "Data" block on the hub, built by the same generator, with the rows Outputs cited, Figures and reference tables (closed), Run, Replicate; drop the separate "Numbers on this page".

**Q4. Where do ADOPT, PILOT and HYPO sit?** `decisions.md` (025w) splits POL into POL, ADOPT, PILOT and FALS into FALS and HYPO. `nav`, `ids-map` and the routing file know only 19 pages and a 15-item menu. *Proposed:* ADOPT and PILOT are parent-reached from POL, HYPO from FALS (the `ids-map` rule: an overflow page gets its own shortcode, reached from its parent); the menu stays at 15; `pages.yml` rows are `type: appendix` with `parent`; 22 spokes in all. The routes need no change. Say if you want any of the three in the menu.

**Q5. Hub and standalone source files.** `ids-map` fixes `source/spokes/FISC.md` for spokes. Nothing fixes the hub file, its front matter, or the standalones after rewrite. *Proposed:* hub at `source/hub.md` with front matter `page: hub`, `status`, `budget` (cap 6,000), `defaults`, `outputs` (the union of every output whose `element:` lists H0 to H7), `inputs`, `reading_note`; no `question` or `depends`; the checker runs it with `--hub` (parts, word and objection checks off). Rewritten standalones move to `source/spokes/ADD.md`, `INST.md`, `SCOPE.md`.

**Q6. Pending pages built on the retired series.** `nav` Q3 keeps ten pages live and unchanged. Two are generated from the 33 papers (`link-map.html` from `internal.json`, and the Project Map points at them), and FAQ, Comparison Tables, Avoidance and others link to old paper URLs that will end at cutover. `ids` retires the machinery that builds them. *Proposed:* at cutover the generated pending pages (Link Map) are committed once as static snapshots with a "map of the retired series" note; `corpus.html` (All Papers, not in the ten) retires with no redirect; and one scripted edit rewrites links to retired paper URLs in the ten pending pages to `retired.html#<old code>`, the only change to them. If you want them byte-for-byte unchanged, their old-paper links will 404.

**Q7. Does the gate cover the glossary?** The glossary is built from `registry/glossary.yml`, seeded from existing definitions. *Proposed:* seeding by copying existing definitions is not spoke prose and may start before the gate; any new or reworded definition waits for it.

**Q8. When do ADD, INST and SCOPE move to the spoke shape?** `ids` Q5a says now; the gate says no spoke prose until the data is final, and the move rewrites text into four parts with hooks. *Proposed:* now means the registry row and the URL (type `standalone`, status `legacy`); the text moves after the gate, in the order of `order.md`.

## 8. Proposed briefs

Numbers are assigned when each is written (next unused, 027 onward). Lane letters as `brief-template.md`. "A" is the author's approval of this file with section 7 answered. All build briefs work on fixtures and deliver without the data gate; none writes spoke or hub prose. `Touches` are disjoint between briefs that may run together; a file shared by two briefs is listed in section 8.2 and the pair is on a Depends chain.

| Brief | Lane | Goal | Touches | Depends on |
|---|---|---|---|---|
| B1 | s | Page registry and ids: `pages.yml` with the 33 legacy, new, pending and calculator rows; `config.py` and `preprocess.py` read it; explicit section ids; shortcode cross-reference grammar | `registry/pages.yml`, `registry/papers.yml`, `pipeline/config.py`, `pipeline/preprocess.py`, `pipeline/transforms.py`, `tests/pages/` | A |
| B2 | c | Data interface: parse the register to `inputs.json` and metrics to `metrics.json`; the output data file validator (V1 to V12) and a fixture data file | `pipeline/build_inputs.py`, `pipeline/build_metrics.py`, `pipeline/validate_outputs.py`, `registry/inputs.json`, `registry/metrics.json`, `tests/data/` | A |
| B3 | c | Hook resolver: parse, resolve, format, error codes H01 to H42, `WDT_MODE`, `hooks-report.json` | `pipeline/hooks.py`, `pipeline/hook_format.py`, `tests/hooks/` | B2 |
| B4 | c | Data block generator, `FigureData`, reference tables and CSV | `pipeline/data_block.py`, `pipeline/figure_data.py`, `tests/data_block/` | B3 |
| B5 | c | Figure renderer: six kinds, palette, access, print, self-check, fixtures FX-* and T-* | `pipeline/figures/`, `registry/figure-style.yml`, `tests/figures/` | B4 |
| B6 | c | Spoke checker, source and build modes, word lists, waiver syntax | `pipeline/check_spokes.py`, `pipeline/check_spokes_lists.py`, `tests/spokes/` | B3, B1 |
| B7 | s | Navigation and routing: navbar from the registry, `routing.yml` and its checks, Read next, breadcrumb data, search config | `site/_quarto.yml`, `registry/routing.yml`, `pipeline/pages/routing.py`, `pipeline/pages/nav.py`, `tests/nav/` | B1 |
| B8 | s | Page types and styles: hub, spoke, parent-reached, standalone layouts, jump bar, banners, draft banner and `noindex`, 404, print stylesheet, `wp.html` alias | `site/includes/`, `site/style/spoke.css`, `site/style/print.css`, `site/pages/404.qmd`, `tests/layout/` | B1 |
| B9 | s | Data-layer pages DL0 to DL6 (generated parts) and one page per manifest output | `pipeline/pages/data_layer.py`, `site/pages/data.md`, `tests/datalayer/` | B1, B2 |
| B10 | s | Retired papers page: `retired.yml` from `ledger-sections.md`, generator, frozen `successor` | `registry/retired.yml`, `pipeline/pages/retired.py`, `tests/retired/` | B1 |
| B11 | s | Calculators relabel ("Based on the retired model"); no model change | `site/pages/calculator_index.md`, `site/tools/taxpayer_calc.html`, `site/tools/revenue_calc.html`, `site/tools/ldw_calc.html` | A |
| B12 | r | Sidecars: `lit-figures.yml` (candidates from register sources) and `inputs-display.yml` for all 260 rows | `registry/lit-figures.yml`, `registry/inputs-display.yml` | A |
| B13 | s | References page and `site-index.json` v2: "Cited in" from `{{lit:}}` keys, new schema | `pipeline/pages/references.py`, `pipeline/pages/site_index.py`, `tests/index/` | B1, B3 |
| B14 | s | Glossary registry and generator (Q7) | `registry/glossary.yml`, `pipeline/build_glossary.py`, `tests/glossary/` | B1 |
| B15 | s | Integration: wire hooks, data block, figures, checker and draft and release into the build; `/draft/` index; workflow draft steps; architecture doc | `pipeline/preprocess.py`, `.github/workflows/deploy.yml`, `docs/wdt-site-architecture.md`, `site/pages/draft.qmd` | B3, B4, B5, B6, B7, B8, B9 |
| B16 | s | Cutover (M6), written last: publish switch, retire legacy files, archive the 30 sources, switch navbar and home (author reviews; touches `source/`) | `source/`, `docs/archive/papers/`, `.github/workflows/deploy.yml`, `pipeline/scrape_contents.py`, `pipeline/build_anchors.py`, `pipeline/wdt_crosslinks.py`, `pipeline/check_wdt_format.py`, `pipeline/link_map.py`, `pipeline/pages/corpus.py`, `site/pages/index.md` | B15, gate, author |

**8.1 Order.** B1, B2, B11 and B12 start together after A. B3 follows B2; B7, B8, B10 and B14 follow B1; B9 follows B1 and B2. B4 then B5 follow B3; B6 and B13 follow B3 (and B1). B15 waits for the seven briefs it names; B16 is written and run last.

**8.2 Shared files, on a Depends chain.** `pipeline/preprocess.py` (B1, then B15); `.github/workflows/deploy.yml` (B15, then B16). No other file appears twice.

**8.3 Not briefs (guru and author).** The data file itself is model v3 work (011g stages). The writing of hub, spokes and data-layer prose (DL4, DL6) is `order.md`. Guru follow-through is in section 9.

## 9. Guru follow-through (after the author approves; not done here)

- `template.md`: add the optional figure-block fields (`lines`, `at`, `unit`, `layout`) and F7; confirm the 6a example is an output its spoke owns.
- `outputs.yml`: split OP4 into two output ids (`figures` Q5); `by` map for any output still a list (OW2, OB1, OD1, OL1, OF1, OT1 are lists today) so figures and the checker can read values; optional `indexed:` field (`checker` Q7).
- `ids.md`, `hooks.md`, `checker.md`, `figures.md`: sibling notes that a pointer to this file overrides them are enough; the siblings are not rewritten.
- STATUS.md, lane plan, `decisions.md` and the 013g status line: at the end of 026g only.

## 10. Checks run

Run for stage A, results recorded in the brief's progress block: every sibling file is linked from this file; every conflict found has a ruling (section 6) or a numbered question (section 7); every pair of briefs with a common file in `Touches` is on a Depends chain (section 8.2). Not run: any build; nothing in `source/`, `pipeline/`, `site/` or `registry/` was opened for change.
