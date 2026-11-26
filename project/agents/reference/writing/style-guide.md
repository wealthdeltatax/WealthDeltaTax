# WDT paper style guide

This section governs structure, formatting, markup, citations, and tone for any paper in the Wealth Delta Tax (WDT) project — the whitepaper and its companion papers (moral/philosophical foundations, literature review, valuation, jurisdiction, corporate). It is derived from the project's own whitepaper (the reference exemplar). When drafting or revising a WDT document, follow this guide rather than the generic defaults in `coauthoring-workflow.md`.

### Build pipeline

All WDT papers compile via:

```
pandoc [file.md] --standalone --template=template.tex --pdf-engine=lualatex --lua-filter=tabularx.lua --toc -o [file.pdf]
```

Three things this means for drafting:

**Inline LaTeX is intentional.** The following commands appear in markdown source and must be included exactly as shown, never paraphrased or removed: `\medskip`, `\newpage`, `\tableofcontents`. They are consumed by LuaLaTeX during compilation.

**Tables use standard markdown pipe syntax only.** The `tabularx.lua` filter rewrites all markdown tables to LaTeX automatically. Do not write LaTeX table environments by hand. Do not use HTML table tags.

**The `{.unnumbered .unlisted}` Pandoc attribute is load-bearing.** It controls section numbering and ToC inclusion in the compiled PDF. Include it exactly as specified below.

### Document file structure

The sequences below are taken from VAL (main paper), VAL.A and VAL.B (appendix companions). Every top-level block is separated by a standalone `\newpage`, including one immediately after the YAML block and one at the very end of the file.

**Main paper** (e.g. VAL):

```
YAML block
\newpage
### Revision History {.unnumbered .unlisted}
[Revision table]
\newpage
# Abstract {.unnumbered .unlisted}
[Abstract prose]
\newpage
# Glossary {.unnumbered .unlisted}
[Glossary entries]
[Glossary navigation paragraph]
\newpage
\tableofcontents
\newpage
# 1. [First Section Title]
```

The **Glossary navigation paragraph** is a plain prose paragraph (not bold, not a glossary entry) placed after the last glossary term. It routes readers to companion papers, e.g. "References throughout this paper to (VAL.A §A) to (VAL.A §F) refer to sections of the mathematical and simulation companion (VAL.A): (VAL.A §A) (mathematical model and propositions), (VAL.A §B) (simulation methodology), …". Include it whenever the paper has a mathematical, simulation or worked-example companion.

Elements **not observed** in VAL (include only if confirmed for a specific paper): visible title block with `\medskip`, `### Keywords {.unnumbered .unlisted}` block, `### Author Disclosure {.unnumbered .unlisted}` block, `## Internal Bibliography {.unnumbered .unlisted}` block.

**Appendix companion paper** (e.g. VAL.A, VAL.B). Formatted like the main paper (Revision History, table of contents, then sections), except that top-level sections are lettered.

```
YAML block
\newpage
### Revision History {.unnumbered .unlisted}
[Revision table]
\newpage
[optional, see below: # Reader's Guide {.unnumbered .unlisted} ... \newpage]
\tableofcontents
\newpage
# A. [First Section Title]
## A.1 [Subsection]
...
\newpage
# B. [Second Section Title]
...
\newpage
```

Companions have no Abstract and no Glossary. Top-level sections use capital letters starting at A in every companion: VAL.B begins at A, it does not continue from the last letter of VAL.A. Below the top level, numbers follow the letter with dots (`A.2`, `A.2.1`, `A.2.1.1`). Lower-case letters never appear in a section number: `(VAL.A §A.2)` is valid, `(VAL.A §A.2.b)` is not. The shortcode in every cross-reference tells the reader which companion is meant: (VAL.A §A.2) and (VAL.B §A.2) are different sections.

A **Reader's Guide** (`# Reader's Guide {.unnumbered .unlisted}`, placed between Revision History and the table of contents) is used in companions that illustrate discrete claims from the main paper, as in VAL.B. It states what the companion is for, maps each section to the claim it illustrates and the case used (table), and gives the shared parameter conventions. Omit it in companions that are a continuous formal treatment, as in VAL.A.

### YAML front-matter block

Fenced with `---`. Field order and indentation are fixed, as in VAL:

```yaml
---
title: "The Wealth Delta Tax: Valuing Wealth"
shortcode: "VAL"
status: "active"
keywords:
    - Wealth Delta Tax
    - wealth taxation
    - keyword three
zenodo_doi: "10.5072/zenodo.611202"
jel:
  - H24   # Personal income and other nonbusiness taxes and subsidies
  - D82   # Asymmetric and private information; Mechanism design
  - G12   # Asset pricing; Trading volume; Bond interest rates
---
```

Order: `title`, `shortcode`, `status`, `keywords`, `zenodo_doi`, `jel`. Keyword items are indented four spaces; JEL items two spaces.

**`title`** — `The Wealth Delta Tax: <Paper Title>`. Appendix companions use the main paper's title followed by an em dash and a descriptor, as in VAL.A and VAL.B ("… — Mathematical and Simulation Appendix", "… — Worked Examples Appendix"). This is the one place the em dash is kept.

**`shortcode`** — the capitalised abbreviation used in cross-references throughout the project (`VAL`, `GOV`, `CORP`). Dot suffixes denote appendix companions (`VAL.A`, `GOV.B`). Required.

**`status`** — `"active"` for published papers, `"draft"` for works in progress.

**`keywords`** — YAML list, one per line. Machine-readable only; a rendered Keywords block does not appear in the papers examined and is not added unless requested.

**`zenodo_doi`** — the paper's Zenodo DOI as a quoted string, `"10.5072/zenodo.NNNNNN"` (prefix `10.5072` in all three VAL papers). **The author assigns and updates these manually.** Never invent a number, never infer one from a sibling paper's number, and never change an existing value when revising. For a new paper write `"10.5072/zenodo.TBD"` and tell the author in the same reply that the DOI needs filling in. Each companion has its own DOI. DOIs are not recorded in the Revision History.

**`jel`** — YAML list of JEL classification codes, each line `  - X00   # Official description` (two spaces, dash, code, three spaces, `#`, description). Use three to six codes. `H24` leads in all three VAL papers and `D82` follows wherever the paper is about valuation incentives or mechanism design. A companion carries the subset of its main paper's codes that its content supports and may add codes for its technical content (VAL.A adds `C61`). Codes and descriptions already used in the project:

| Code | Description as written in the comment |
|:---|:---|
| H24 | Personal income and other nonbusiness taxes and subsidies |
| H21 | Efficiency; Optimal taxation |
| D82 | Asymmetric and private information; Mechanism design |
| D44 | Auctions |
| G12 | Asset pricing; Trading volume; Bond interest rates |
| G13 | Contingent pricing; Futures pricing |
| C61 | Optimization techniques; Programming models; Dynamic analysis |

Reuse these descriptions verbatim. For a code outside this table, check the AEA JEL classification (web search if available) before using it; do not guess codes or descriptions.

**Fields NOT seen in published papers** (do not add unless requested): `author`, `date`, `toc`, `numbersections`, `documentclass`, `fontsize`, `geometry`. These are handled by the build template.

### Visible title block

The visible title block (author name, affiliation, version, date in bold labels) is **not present** in the VAL paper — the title is rendered by `template.tex` from the YAML `title:` field, and no additional title block appears in the markdown source. Do not add one unless the author explicitly requests it.

If a paper does include a visible title block (some earlier papers may), it appears immediately below the YAML block:

```markdown
**K. Ogata**  
Independent Researcher  

\medskip

**Version:** 1.x  
**Date:** DD Month YYYY  

\medskip
```

Author name bold, affiliation plain, two trailing spaces on each line (forces a line break in Pandoc). Version and Date: bold label, value on the same line. `\medskip` between field groups (not `<br>`).

### Front matter blocks

**Keywords block** — not present in VAL; keywords appear in YAML only. If a paper does include a rendered keywords block: H3, both attributes: `### Keywords  {.unnumbered .unlisted}`. Keywords on one line, separated by ` · ` (space, middle dot U+00B7, space). Do not add by default.

**Author Disclosure** — not present in VAL. If present in another paper: H3, both attributes: `### Author Disclosure  {.unnumbered .unlisted}`. Single paragraph, plain prose. Do not add by default.

**Revision History** — H3, both attributes: `### Revision History {.unnumbered .unlisted}`. Table with three columns: Revision (centred), Date (centred), Details (left-aligned):

```markdown
| Revision | Date          | Details         |
|:--------:|:-------------:|-----------------|
```

Version numbers: two decimal places in pre-publication drafts (`0.01`), then one decimal place after first publication (`1.00`, `1.01`). Dates: day month year, month in full (`15 August 2026`).

**Details column**: each revision entry is a dense, section-by-section account of every change made. List each changed section explicitly, written as a cross-reference (`(VAL §5.2) updated with…; (VAL §7.1) updated with…`) rather than summarising thematically. Include figure renumbering events. Separate changes with semicolons. This level of granularity is the house standard — the Revision History is a changelog, not a summary.

**Internal Bibliography** — H2, both attributes: `## Internal Bibliography {.unnumbered .unlisted}`. Each entry its own paragraph. Format:

```
[SHORTCODE] Author, A. (Year). *Full Title: Subtitle*. Unpublished.
```

Shortcodes: capitalised abbreviations (e.g. `[GOV]`, `[CORP]`, `[VAL]`). Dot suffixes for appendix companions (`GOV.A`, `CORP.A`). Title italicised. Always ends with `Unpublished.` Internal WDT papers appear here only — not in the References section.

**Abstract and Glossary headings** — both carry `{.unnumbered .unlisted}`:

```markdown
# Abstract {.unnumbered .unlisted}
# Glossary {.unnumbered .unlisted}
```

**ToC placeholder** — if the paper includes a ToC, place it after Glossary:

```markdown
\tableofcontents
\newpage
```

VAL, VAL.A and VAL.B all include it: the sequence is `\newpage`, `\tableofcontents`, `\newpage`, then the first numbered section.

### Page breaks

`\newpage` is a standalone line between all major structural units: immediately after the YAML block; Revision History → Abstract (or Reader's Guide, or ToC in companions); Abstract → Glossary; Glossary → `\tableofcontents` → first numbered section; before every top-level numbered section; References → first Appendix if present; and once at the end of the file. The same pattern applies in appendix companions. Do not insert `\newpage` within a section.

### Document skeleton (body sections)

A full paper (the whitepaper is the complete case) runs in this order:

1. **Introduction** — often with a numbered first subsection laying out a foundational principle the rest of the paper builds on.
2. **Intellectual Context and Prior Literature** — survey section, organized by tradition or strand, each ending with what that strand leaves unresolved.
3. **Mechanism Design / core proposal** — the longest section, broken into one subsection per structural component.
4. **Supporting institutional sections** (e.g., a fund, a governance body) where applicable.
5. **Revenue/impact properties.**
6. **Sequencing or implementation pathway**, if the proposal has phases.
7. **Principal Objections** — one subsection per objection, each stated fairly before being answered.
8. **Limitations and Required Further Work** — an honest, non-defensive accounting of what the paper does not establish, in five fixed subsections and placed immediately before the Conclusion. See "The Limitations and Required Further Work section" below. This section replaces the former Open Questions section; there is no separate Open Questions section.
9. **Conclusion** — restates the components and their interdependence; does not introduce new claims.
10. **References** — see "Citations and references" below.
11. **Appendices** — used for material that supports the argument but would slow the main text.

**Section count**: companion papers routinely run to 14–15 numbered sections. The skeleton above is a structural template, not a section count ceiling. VAL (a companion paper) runs to §15 (Conclusion), with dedicated sections for each major mechanism component, a standalone §11 for the auction mechanism's three use-cases, §12 for assessment window design, §13 for the self-declared valuation register, §14 for objections and limitations, and §15 for the conclusion. Plan sections to match the paper's actual structural components, not to fit a target number.

A **companion paper** doesn't need every element of the whitepaper. It typically keeps the Revision History, Abstract, Glossary (only for terms not already in the whitepaper's), a body organized around its own specific contribution, a Limitations and Required Further Work section, a Conclusion, and References. It should explicitly state at the start how it relates to the whitepaper and which of the whitepaper's limitations or SCOPE items it is addressing.

### Heading hierarchy and explicit numbering

All numbered body headings carry their number explicitly in the markdown source.

| Level | Tag | Use |
|---|---|---|
| H1 | `#` | Top-level numbered sections; Abstract, Glossary, Reader's Guide, References |
| H2 | `##` | Primary subsections within a section; Internal Bibliography |
| H3 | `###` | Sub-subsections; front-matter metadata blocks (Keywords, Author Disclosure, Revision History) |
| H4 | `####` | Named sub-topics within H3 — used sparingly |

**H1 body sections:** Arabic numerals, starting at 1.

```markdown
# 1. Introduction
# 2. Intellectual Context and Prior Literature
# 3. The Wealth Delta Tax: Mechanism Design
```

**H2 subsections:** Parent number, dot, child number.

```markdown
## 2.1 The Haig-Simons Definition and the Comprehensive Income Tradition
## 2.2 The Empirical Literature on Wealth Taxation
```

**H3 sub-subsections:** Three levels deep.

```markdown
### 3.1.1 The Tax Base
### 3.1.2 The Individual as the Unit of Taxation
```

**H4:** Four levels deep, used sparingly.

```markdown
#### 3.1.2.1 Voluntary Participation Below the Threshold
```

**Appendix companion headings:** a capital letter for the top level (`# A. Mathematical Model and Incentive Analysis`), dot numbers below it (`## A.1 Purpose`, `### A.2.1 Finding 1: Honest declaration lies within a locally stable region`). Lettering restarts at A in each companion. No lower-case letters, no `{.appendix}` attribute.

Appendices are separate companion files (see "Appendix companion papers" below); VAL embeds none in the main paper. If an author asks for material embedded in a main paper, ask how it should be lettered before writing it.

**Unnumbered structural headings** (Abstract, Glossary, References, Internal Bibliography): `{.unnumbered .unlisted}`. Limitations and Required Further Work is a normal numbered section.

### The Limitations and Required Further Work section

This section is where every unresolved item lives. It replaces the former Open Questions / Cross-Paper References section, which no longer exists: do not add an Open Questions section, and do not fold open items into a loose "Limitations" paragraph. Items outside the project's scope point to SCOPE instead of being left open in the paper.

Heading: an ordinary numbered top-level section, `# 9. Limitations and Required Further Work` (adjust the number to its position), placed immediately before the Conclusion. It always has the same five H2 subsections, with the same titles in the same order, with the number written in the heading text:

```markdown
## 9.1 Formal modelling gaps
## 9.2 Phase One empirical unknowns
## 9.3 Jurisdiction-specific legal and implementation work
## 9.4 Structural and irreducible limits of the design
## 9.5 Governing Council calibration parameters
```

All five appear in every main paper. A subsection with nothing to report says `No items in this paper.` and is not omitted or renamed. Only one new subsection level is allowed below them, an H3 inside §9.4 for individually named compromises (MF §9.4.1 to §9.4.9).

**What each subsection holds.**
- **Formal modelling gaps.** Analysis the paper needs and does not contain (a model, a derivation, a quantification), with what the work would require and where it is assigned. Gaps that are outside the project go to SCOPE (see below).
- **Phase One empirical unknowns.** Questions only a live system can answer, each stated with the specific quantity or behaviour that is unknown and what the paper's own figures assume in the meantime (CLOSE §9.2: RATES assumes no behavioural exit response). Point to (PHASE1) where it specifies the evaluation design.
- **Jurisdiction-specific legal and implementation work.** Constitutional, statutory and operational questions that depend on a jurisdiction, assigned by name to JUR, to the dedicated legal paper, or to a future paper (named even if unwritten).
- **Structural and irreducible limits of the design.** What the paper does not and cannot establish, and the named compromises: trade-offs the project accepts and states. A named compromise is not a pending item; say so (MF §9.4.9: "none is a pending design item"). Say which paper holds the framework for predicting what this paper does not quantify (CLOSE §9.4 points to BEHAV).
- **Governing Council calibration parameters.** One paragraph per parameter: what it is, the process that sets it (e.g. the Tier 1 process), the trade-off the value balances, the evidence that will inform it, and the closing phrase that the value awaits that evidence. Cross-reference where the principles are specified, e.g. `(GOV.B §E.3)`.

**Routing to SCOPE.** Every item names where it goes next. Items outside the project's scope are classified in SCOPE, and the paper says so with a cross-reference, as LR.A does: "This gap is classified in (SCOPE §3.1)." SCOPE's four categories are modelling tasks left to future researchers (§2), questions requiring legal or jurisdictional expertise (§3), questions requiring international coordination (§4), and questions sequentially deferred to post-Phase One (§5). Do not guess the SCOPE section from the topic: ask the author, or check `website/registry/contents.yml`. SCOPE records the classification and the resolution path; it does not resolve the question or add positions, so the paper still states the item and what closing it would require. If the paper adds, drops or reclassifies an item that SCOPE records, SCOPE needs a matching update, and the author makes it in SCOPE. SCOPE reuses subsection titles under §3 and §4 (and §6 and §8), so until `build_anchors.py` suffixes duplicate anchors, a link to (SCOPE §4.1) lands on §3.1's anchor in the rendered site; tell the author when a paper cites one of these.

**Closure.** Items are never silently dropped between revisions. When a later paper closes an item, the subsection stays and states the closure in the present tense with a cross-reference to the closing paper and what it established (WP §9.1: three gaps "closed by (WFR)", each with its section). The Revision History row records the change. Do not use italic closure notices and do not write "has since been".

### Glossary

One entry per paragraph. Term bold, colon immediately after, definition on same line. No bullets, numbered lists, or blank lines within an entry.

```markdown
**Delta base:** The rolling average of net worth change across a defined window of assessment years.

**Exemption threshold:** The net-worth level above which a person falls within the WDT system.
```

Entries are alphabetical; plain declarative sentences only (no examples or hedging inside the glossary itself).

### Cross-references

Every cross-reference is fully enclosed in brackets and carries the shortcode, including references to the paper being written. The bracket opens before the shortcode and closes after the section number.

| Reference type | Format |
|---|---|
| Whole sibling paper | `(GOV)`, `(CORP)`, `(VAL)` |
| Section in this paper | `(VAL §5.2)` (use this paper's own shortcode) |
| Section in another paper | `(GOV §9)`, `(CORP §4.1)`, `(VAL.A §A.2)` |
| Contiguous range | `(VAL §5.2) to (VAL §5.5)` |
| Two references | `(VAL §7.2) and (VAL §7.3)` |
| Longer list | `(VAL §5.2), (VAL §7.1), and (VAL §9)` |
| Figure or table in another paper | `(SWEEPS Figure 11c)`, `(VAL.A Table C.3)` |
| Proposition or finding | `(VAL.A §A.5.1) (Proposition 1)` |

Never write a bare `§5.2`, `§§5.2–5.5`, `(VAL §5.2–5.5)`, `(VAL §5.2 to §5.5)`, or a range with "through" or a dash. Main-paper section numbers are Arabic (`(VAL §5.2)`); appendix sections take one capital letter then dot numbers (`(VAL.A §A.2)`). Never use a lower-case letter in a section number (`(VAL.A §A.2.b)`). Never put extra words inside the brackets. The rule holds in body text, figure and table captions, the Glossary navigation paragraph, and the Revision History. Never write "Section 3" or "see above" when a reference is possible, and never write "the governance paper" without the shortcode. Every cross-reference must be resolvable: if pointing to a section that does not exist yet, name the future paper rather than leaving a dangling reference.

References to figures and tables in the same paper are plain text (`Figure 7.1a`, `Figure A.2b`, `Table C.2`), not bracketed.

### Notation and symbols

| Symbol | Use |
|---|---|
| `§` | All section references |
| ` · ` | Keyword separators in Keywords block |
| `τ₀` | Variables (subscript inline, Unicode) |
| `\newpage` | Page breaks |
| `\medskip` | Vertical spacing in title block |
| `\tableofcontents` | ToC placeholder before first section |

**Em dashes (`—`):** Not used. Restructure the sentence to remove them. If the content is parenthetical, use parentheses. If the sentence can be split, split it.

### Citations and references

**In-text citations — Pandoc `@Key` syntax:**

Papers use Pandoc citation keys, not manually typed author–year strings. The citation key is typically `AuthorYear` or `AuthorNameYear` (no spaces, no punctuation).

- Narrative (author as grammatical subject): `@PereiraGray2021 identified…` → renders as "Pereira Gray (2021) identified…"
- Parenthetical: `(@Harberger1965)` → renders as "(Harberger, 1965)"
- Placement: citation follows the claim, before the full stop.
- Titles in body text: plain, not italicised (italics reserved for References section).

Do **not** type `(Piketty, 2014)` by hand — use `(@Piketty2014)`. The rendered format is determined by the CSL style file, which follows APA 7th.

**References section — strict APA 7th:**

Alphabetical by first author surname. Entries separated by blank lines. En dash (`–`) for page ranges, not hyphen. Internal WDT papers do not appear here — they are in the Internal Bibliography only.

Journal articles:
```
Surname, A. B., & Surname, C. D. (Year). Title of article in sentence case. *Journal Name in Title Case*, *volume*(issue), page–page. https://doi.org/xxxxx
```

Books:
```
Surname, A. B. (Year). *Title of book in sentence case*. Publisher.
```

Working papers:
```
Surname, A. B. (Year). *Title of working paper in sentence case* (Working Paper No. XXXXX). Institution Name. https://doi.org/xxxxx
```

Title case rules: journal/book/chapter titles in sentence case (capitalise first word, first word after colon, proper nouns); journal names in title case; publisher names in title case.

### Lists and emphasis

**Bullet lists:** Not used anywhere in body text or appendices.

**Numbered lists in body prose:** Not used. Enumerate in prose: "Three distinct arguments… The first is… The second is…"

**Numbered subsections in Limitations and Required Further Work:** Structured as H2 with the number in the heading text, not a markdown list. Items inside a subsection are prose paragraphs.

**Bold:** Only for glossary terms and metadata labels in the title block (Version, Date).

**Italics:** Only for titles in References and Internal Bibliography and journal names in References.

### Tables

Used for: structured metadata (Revision History), comparative reference data, notation definitions, parameter sweeps, simulation output. Header row always present. Column alignment set explicitly. Standard markdown pipe syntax only. No HTML table tags.

**Table captions**: placed on the line immediately below the table (not above). Plain text, no heading tag. Format: `Table C.1: Brief description. Parameter note.` — section-prefixed number (appendix section letter plus running index in appendix companions), colon, description, then key parameters (e.g. `$V_0$ = £20m, $k$ = 0.001, N = 30`).

**Interpretation notes**: in appendix companion papers, each table is followed by an italicised paragraph (`*Interpretation text.*`) explaining the structural claim the table illustrates. This note is not bold and is not a separate subsection — it is inline, directly after the caption.

### Figures

Figures sit inline at the point of first reference: a prose sentence introduces the figure ("Figure 7.1a makes this structure visible."), the image follows, then a reading paragraph explains what to look for. The reading paragraph is body text, not caption.

```markdown
![Figure 7.1b: Declaration equilibrium cost curve. Net tax relative to honest declaration as a function of declaration ratio $\alpha$, at multiple growth rates. Solid lines are constant $g$; the purple dash-dot line is the 2000 historical series. N = 30, $V_0$ = £20m, $k$ = 0.001. Source: (VAL.A §C.1), (VAL.A §C.9).](../figures/val_fig_7_1b_declaration_equilibrium_cost_curve.png){width=100%}
```

**Figure name.** The figure number is the number of the lowest-level section the image sits in. A figure in the body of (VAL §5) before its first subsection is Figure 5; figures in (VAL §5.2) are Figure 5.2a and 5.2b; four figures in (VAL §7.1) are 7.1a to 7.1d. A section holding one figure carries no letter (Figure 7.3). A section holding two or more letters all of them, in order of appearance (a, b, c…). If a second figure is added to a section that had one, the first gains the letter `a`; update every prose reference and record the renumbering in the Revision History. Never use a running number across the paper (no "Figure 10").

**Appendix figures** use the same rule with the appendix section label: two figures in (VAL.A §A.2) are Figure A.2a and Figure A.2b; a single figure there is Figure A.2.

**Filename.** `../figures/<shortcode lowercase, dot as underscore>_fig_<label lowercase, dots as underscores>_<snake_case_slug>.png`, e.g. `val_fig_7_1b_declaration_equilibrium_cost_curve.png`, `val_fig_5_rate_function_tau_w.png`, and for appendix figures `val_a_fig_a_2a_<slug>.png`. The appendix filename pattern is inferred from the label rule; confirm it with the author before naming the first appendix figure. The path is always relative (`../figures/`). Width is always `{width=100%}`.

**Caption anatomy**, in this order, as one paragraph with no line breaks:

1. `Figure N:` label.
2. Short descriptive title as a noun phrase, ending in a full stop.
3. What the figure shows: panels (`Left:` / `Right:`), colours and line styles, contours and markers, annotated values.
4. Fixed parameters in the paper's notation (`N = 30, $V_0$ = £20m, $k$ = 0.001`).
5. `Source:` followed by the appendix section(s) that produced the data, as cross-references, comma-separated when there are several. The caption ends with this and a full stop. This is the link to the corresponding appendix section and is required on every figure. For a figure plotted from a formula, cite the section that defines it.

Only describe elements that are visible in the image and quote only values that appear in its annotations. Check the image before writing or revising a caption; a caption that describes a legend line or panel the figure does not contain is an error. Interpretation belongs in the reading paragraph.

### Appendix companion papers (separate files, e.g. VAL.A, VAL.B)

When mathematical, simulation or worked-example material is large enough to be its own file, it is a standalone companion paper, formatted as in "Document file structure" above: top-level sections lettered A, B, C from A, a `\tableofcontents`, and YAML front matter with its own `shortcode`, `zenodo_doi` and `jel`. No `{.appendix}` attribute. The main paper points to companion sections with `(VAL.A §A.2)`. A companion opens its first section by stating which main-paper section it supports. Appendix companions carry no Limitations and Required Further Work section (it has been removed from GOV.B and CORP.A); their limits are recorded in the main paper's section.

**Numbering carries the section.** Subsections use dot notation: `## A.1 Purpose`, `### A.2.1 Finding 1: Title`. Tables take the section prefix (`Table C.1`), equations likewise (`(A.3.1)`), figures follow the figure rule above (`Figure A.2a`).

**Findings subsections**: `### A.2.X Finding N: Descriptive Title`. Each finding states the result concisely, then directs the reader to the relevant Proposition.

**Proposition format**:
```markdown
### A.5.1 Proposition 1: Title

**Proposition.** Statement of the formal claim in one or two sentences.

**Interpretation.** Plain-English meaning, including scope limitations and what the proposition does not claim.
```

**Proposition summary table**: after the final proposition, a table collects all propositions:
```markdown
| **Proposition** | **Result** | **Interpretation** |
|----|----|----|
| **Proposition 1** | ... | ... |
```

**Equation display**: inline as `$formula$ (A.3.1)`, with the equation number in parentheses on the same line.

**Worked-example companions** (VAL.B pattern): each section opens with `**Claim illustrated:**` naming the claim and its main-paper reference, then runs `## J.1 Setup`, `## J.2 The Mechanism`, `## J.3 Illustrative Figures`, `## J.4 What the Example Shows` (letter of the section), and the last section is a summary table of the design properties illustrated with a cross-reference column. A model note states any closed-form shortcut used in place of the simulation.

**No Abstract, Glossary, References or Internal Bibliography** in companions. Citations are cross-references to WDT shortcodes in the standard format.

**Structural validation note** (simulation tables): the first paragraph under each table subsection states the structural claim the table supports. It appears before the table, not after it.

### Tone and prose rules

- **Continuous prose is the default**, even for technical mechanism description. A reader should be able to follow the core mechanism sections without encountering a single bullet list.
- **State objections fairly before answering them.** Every "Principal Objections" subsection opens with the strongest version of the objection, not a weakened strawman, before the paper's response.
- **Name trade-offs explicitly rather than disguising them as natural extensions of the theory.** When the design departs from its own stated principles, say so directly — "this is an administrative necessity, not a principled position" is the house phrasing pattern.
- **Distinguish three kinds of unresolved claims** and use the right label and subsection for each:
  - **Open question** — nobody has done the work yet; it goes in §N.1 (modelling) or §N.3 (legal and implementation), assigned to a future paper, and to SCOPE where it is outside the project.
  - **Named compromise** — a trade-off the project has already accepted and stated; not pending further work, just acknowledged. It goes in §N.4.
  - **Genuinely empirical** — explicitly flagged as something only real-world implementation can resolve. It goes in §N.2.
- **Hedge with precision, not vagueness.** State the specific condition under which something might not work, not just that it might not.
- **One paragraph, one structural idea.** Paragraphs build an argument linearly — claim, mechanism, implication, limitation — rather than listing parallel points.
- **Avoid restating the same caveat in multiple places.** If a limitation is named once, cross-reference it elsewhere rather than re-explaining it.
- **Don't oversell.** The paper's own voice routinely undercuts its strongest claims with a direct statement of what remains unproven.
- **Do not write temporal artifacts.** A finished paper states its positions in present tense as settled fact. It does not narrate how it arrived at them. If the current design replaced an earlier one, the earlier one simply does not appear. The test: would this sentence make sense to a reader encountering the paper for the first time, with no knowledge of prior versions?

### Writing rules

All prose drafted for a WDT paper follows the two rule sets in `prose-rules.md` (compression and AI-tell removal), applied in a single pass while drafting. Do not draft verbosely and plan to compress later. The pre-flight savings estimate and word-count rule in `prose-rules.md` apply only when rewriting an existing file; they do not apply when drafting.

### Pre-publication consistency pass

Before Reader Testing, and again before the author publishes, run the checker on the paper's markdown file:

```bash
python website/build/check_wdt_format.py source/<paper>.md
```

It reports, with line numbers: missing or misordered front-matter fields, malformed `zenodo_doi` and `jel` lines; bare `§` references, ranges written with dashes or "through", lower-case letters inside section numbers and extra words inside reference brackets; stray `{.appendix}`; figure labels that do not match their section, wrong or missing letters, wrong filenames, missing `{width=100%}`, captions not ending in `Source: (…)`; and em dashes in prose. Fix every finding, or confirm with the author that a finding is intentional. The checker is mechanical and does not read the prose, so also check by eye that each caption matches its image and that each cross-reference points to a section that exists. Remind the author of any `zenodo_doi` still set to `TBD`.

The checker validates the syntax of references, not whether their targets exist or still say what the sentence claims. Resolution is checked by `wdt_crosslinks.py`; see the next section.

The checker does not inspect the Limitations section. Check by eye that a main paper has no Open Questions heading, that Limitations and Required Further Work sits immediately before the Conclusion with exactly the five standard subsections in order, that empty subsections say `No items in this paper.`, and that every `(SCOPE §N)` reference names a section that exists.

### Post-update crosslink workflow (wdt_crosslinks.py)

`website/build/wdt_crosslinks.py` treats the headings in `source/*.md` as the source of truth. It extracts every `(X §N)`, bare `§N`, `[X]` and "Section N" reference, then validates each against the headings, `literature/anchors.yml` and `literature/internal.json`. It checks numbers, never wording: `(MF §5)` passes if MF has a §5, whatever the sentence says about it. `check_wdt_format.py` checks reference syntax; `wdt_crosslinks.py` checks resolution. Run both.

**Severities.** Error: `section_not_found`, `duplicate_section_number`. Warn: `anchor_stale`, `not_in_anchors`, `target_retitled`, `prose_reference`. Info: `paper_not_in_source`, `registry_outbound_missing`. Revision History rows are skipped by the tool, so check their references by eye.

**Commands.** Read-only: `scan` (writes `website/registry/crosslinks.json`), `check`, `query --to X§N` / `--from X§N`, `anchors` (writes `anchors.generated.yml`), `contents`. Writing: `remap --map renumber.yml` rewrites link text only, and only with `--apply`. It never touches headings or `anchors.yml`. The registry files are fed by two other scripts: `website/build/scrape_contents.py` syncs `website/registry/contents.yml` to the headings (it replaces titles, removes stale keys and adds new ones; `--additive` is the legacy add-only mode), and `website/build/build_anchors.py` regenerates `anchors.yml` from `contents.yml`. `wdt_crosslinks.py contents` and `anchors` only emit comparison files.

**Roles.**
- The author edits headings and decides every renumbering. Claude works in the repo, so it can run the scripts itself.
- Claude never changes a section number inside a cross-reference by hand. Numbers change only through a `remap`, applied after the author has reviewed the dry run.
- Claude drafts `renumber.yml` (one `OLD: NEW` per line, e.g. `CLOSE§5: CLOSE§6`), reviews dry-run output, triages `check` output, rewrites sentences whose target changed, drafts Revision History rows, and proposes `internal.json` updates.
- Run with explicit paths when needed: `python website/build/wdt_crosslinks.py check --source source --anchors literature/anchors.yml --internal literature/internal.json`. If only part of `source/` is present, links to absent papers are unverified, not passed; say so.
- When the author says a paper was updated, ask which sections were added, removed, renumbered or retitled, and run `check`. Do not infer either.

**Sequence after a paper update.** Give the author these steps in order, adapted to what changed.

1. Before editing, commit clean so `website/registry/crosslinks.json` in HEAD is the baseline.
2. After editing, run the format checker on the edited file and fix every finding.
3. Run the crosslink check against the committed baseline, unfiltered:
   ```
   git show HEAD:website/registry/crosslinks.json > /tmp/base.json
   python website/build/wdt_crosslinks.py check --baseline /tmp/base.json --min-severity info
   ```
   Do not add `--paper X` when reviewing an update to X. The filter applies to the source paper of each link, so it hides broken links in other papers that point at X. Drift is only reported against `--baseline`; `scan` overwrites the previous file, so a second scan shows none.
4. Fix errors first. `section_not_found` means a section was renumbered or removed, or the reference has a typo. If numbers moved, write `renumber.yml` (`scrape_contents.py --suggest-map renumber.suggested.yml` drafts one by matching unchanged titles under changed numbers; run it before step 6, because `--write` removes the evidence, and it misses sections that were renumbered and retitled together), run `remap --map renumber.yml` as a dry run, paste the output to Claude, and apply only after review. `remap` cascades by prefix by default (`WP§3` also rewrites `WP§3.x`; the longest matching key wins), `--no-cascade` limits it to exact keys, and it is single-pass, so swaps such as `X§5: X§6` with `X§6: X§5` are safe. It skips prose references, paper-only links and Revision History unless `--include-history`.
5. Review meaning. For every section whose content changed, even if its number did not, run `query --to X§N` and send Claude the output. Each result includes the sentence around the link. Claude judges whether the claim still fits the target and rewrites it where it does not. Also run `query --to SCOPE§N` for each SCOPE section the paper cites, and check that SCOPE still classifies the item the way the paper says. Flagged `target_retitled` links and descriptive labels ("the cognitive moral hazard of the current system (MF §5)") are the main targets.
6. Sync the registry. `scrape_contents.py` rebuilds each paper's `sections` from its headings in document order:
   ```
   python website/build/scrape_contents.py MF               # report: + added, ~ retitled, > renumbered, - removed
   python website/build/scrape_contents.py MF --dry-run     # YAML diff
   python website/build/scrape_contents.py MF --write
   python website/build/build_anchors.py
   ```
   Omit the shortcode to sync every paper. Read the report before `--write`; it exits 1 if any paper is blocked. Rules to explain to the author:
   - Math headings (`$...$`) keep their existing `contents.yml` title, because anchors are built from the title text and math headings need a hand-written plain-text title (e.g. `tau 0 = 10%`). A new math heading is added with its raw LaTeX and flagged; write the plain title by hand before running `build_anchors.py`.
   - A duplicate section number inside a paper blocks that paper (not synced). Fix the heading first.
   - A paper with edge-case headings (no parseable key, e.g. an appendix h1 without a letter) keeps stale keys an edge heading could own and flags them. An edge h1 can own only undotted keys; an edge h2 or deeper can own any key. Resolve the edge case, then re-run.
   - `page` and `title` of a paper entry are only set when missing. Papers in `contents.yml` but not in `papers.yml` are untouched; a new paper needs a `papers.yml` entry.
   - Front matter and fenced code blocks are skipped, levels 1 to 6 are read, and bare-letter headings such as `# J The Deferred Delta` (J to Z) parse as keys. The parser is kept aligned with `wdt_crosslinks.py`; if the two disagree on a paper's section keys, find out why before continuing.

   Cross-check anchors with `wdt_crosslinks.py anchors` and `diff literature/anchors.yml literature/anchors.generated.yml`. Expect differences on math headings (`unverifiable`, check by hand) and on duplicate titles. `build_anchors.py` gives repeated titles ("The Problem", "The Clarity Principle") the same anchor, while Pandoc suffixes later ones `-1`, `-2`; at the last check `anchors.yml` had 27 such shared targets (ADD, BEHAV, FAL, INST), so links to the later sections land on the first. Until `build_anchors.py` suffixes duplicates, treat those diffs as known, and verify any new link to a repeated-title section in the rendered page.
7. Update `internal.json`: `version`, `version_date` (YYMMDD), `notes`, `outbound_internal`, `inbound_internal`, the citation records if `@` citations changed, and `open_question_ids` if the paper added, closed or reclassified an item that SCOPE records (SCOPE's own `open_question_ids` list what it classifies).
8. Write the Revision History row for the edited paper, listing each changed section as a cross-reference. Papers whose links were rewritten get their own row naming the links changed.
9. Run `check` again until it is clean, then `scan` and commit the papers, `contents.yml`, `anchors.yml`, `internal.json` and `crosslinks.json` together. That `crosslinks.json` becomes the next baseline.

**Cascade guards.** One structural change per paper per pass, with a scan before and after. Inserting a section mid-paper renumbers every later sibling and every inbound link, and shows up as many `target_retitled` warnings; treat that list as the to-do list. Where the structure allows, append a section or add a subsection instead of inserting a top-level one. Never apply `remap` to a paper while a second structural change is pending in the same paper. Run the `scrape_contents.py` report before `--write` and keep its output; after the write, `contents.yml` matches the headings and the record of what changed is gone.

**Triage order for pasted `check` output.** Must fix: errors. Fix wording: `target_retitled` and any label that no longer matches its target. Regenerate: `anchor_stale`, `not_in_anchors` (fix `contents.yml` first, then run `build_anchors.py`; editing `anchors.yml` directly is overwritten). Convert: `prose_reference` to `(X §N)`. Usually ignorable: `paper_not_in_source` when only some papers are loaded, orphaned anchors for sections that no longer exist (remove the stale keys from `contents.yml`, then regenerate), registry notes. Report counts per class, then the must-fix items with file and line.
