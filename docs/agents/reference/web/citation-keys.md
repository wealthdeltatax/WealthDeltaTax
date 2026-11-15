# Citation Key Conversion (Stage 1.5)

This file covers converting papers from prose APA citations to Quarto `@key` format,
enabling auto-generated bibliographies from `wdt_references.bib`.

**Stage 1 default:** Inline reference lists render as-is. No citation conversion is needed
to launch the site. Do Stage 1.5 one paper at a time, whenever the author is ready.

---

## Key naming conventions in `wdt_references.bib`

The `.bib` file uses these key conventions:

| Case | Convention | Examples |
|------|-----------|---------|
| 1 author | `AuthorYYYY` | `Kaldor1955`, `Piketty2014`, `Shakow1986` |
| 2 authors | `AuthorAuthorYYYY` | `DomarMusgrave1944`, `PosnerWeyl2018`, `SaezZucman2016` |
| 3+ authors | `AuthorEtAlYYYY` | `GuvenenEtAl2023`, `JakobsenEtAl2020`, `JakobsenEtAl2024` |
| Same author, same year | suffix `a`, `b`, ... | `Gangl2015a`, `Gangl2015b` |
| Special chars in name | stripped/simplified | `LondonoVelezAvilaMahecha2025` (accents removed) |

---

## Matching prose citations to `.bib` keys

Common prose forms and their keys:

| Prose in paper | `@key` |
|---------------|--------|
| `Domar and Musgrave (1944)` | `@DomarMusgrave1944` |
| `Haig (1921)` | `@Haig1921` |
| `Simons (1938)` | `@Simons1938` |
| `Kaldor (1955)` | `@Kaldor1955` |
| `Bradford (1986)` | `@Bradford1986` |
| `Auerbach (1991)` | `@Auerbach1991` |
| `Shakow (1986)` | `@Shakow1986` |
| `Harberger (1965)` | `@Harberger1965` |
| `Posner and Weyl (2018)` | `@PosnerWeyl2018` |
| `Piketty (2014)` | `@Piketty2014` |
| `Saez and Zucman (2016)` | `@SaezZucman2016` |
| `Saez and Zucman (2019)` | `@SaezZucman2019` |
| `Guvenen et al. (2023)` | `@GuvenenEtAl2023` |
| `Jakobsen et al. (2020)` | `@JakobsenEtAl2020` |
| `Jakobsen et al. (2024)` | `@JakobsenEtAl2024` |
| `Seim (2017)` | `@Seim2017` |
| `Brülhart et al. (2022)` | `@BrulhartEtAl2022` |
| `Londoño-Vélez and Avila-Mahecha (2025)` | `@LondonoVelezAvilaMahecha2025` |
| `Tyler (1990)` | `@Tyler1990` |
| `Kirchler (2007)` | `@Kirchler2007` |
| `Murphy and Nagel (2002)` | `@MurphyNagel2002` |
| `Dahl (1985)` | `@Dahl1985` |
| `Bartels (2008)` | `@Bartels2008` |
| `Gilens (2012)` | `@Gilens2012` |
| `Chamley (1986)` | `@Chamley1986` |
| `Judd (1985)` | `@Judd1985` |
| `Kopczuk (2015)` | `@Kopczuk2015` |

---

## Per-paper conversion workflow

When the author wants to convert a specific paper (e.g., WP):

**Step 1:** Ask the author to paste:
- One or two body paragraphs with citations
- The paper's inline reference list

**Step 2:** Identify all prose citations in the pasted text. For each:
- Find the matching `@key` from the table above
- If not in the table, derive the key from the naming convention
- Flag any citation that doesn't match any entry in `wdt_references.bib`

**Step 3:** Return:
- The body text with `@key` substituted for prose citations
- The reference list entries that should now be removed (Quarto will generate them)
- A list of any unmatched citations for the author to resolve

**Step 4:** Repeat for the next section.

**Do not** try to convert an entire paper in one pass — the context is too long and errors
compound. Work section by section, or reference-list by reference-list.

---

## Quarto citation format

In body text:
- `@DomarMusgrave1944` → renders as "Domar and Musgrave (1944)"
- `[@DomarMusgrave1944]` → renders as "(Domar and Musgrave, 1944)"
- `[@DomarMusgrave1944, p. 390]` → renders as "(Domar and Musgrave, 1944, p. 390)"

At the end of the paper, add:

```markdown
## References {.unnumbered}
```

Quarto will populate it automatically from all `@key` citations in that file, using the
CSL style specified in `_quarto.yml` (APA by default).

---

## Enabling bibliography in `_quarto.yml`

The `.bib` file must be registered at the project level. This is already done in the
template `_quarto.yml`:

```yaml
bibliography: wdt_references.bib
csl: apa.csl
```

The `apa.csl` file must be present in `site/style/`. Download it from:
https://github.com/citation-style-language/styles/blob/master/apa.csl

---

## Unified references page (Stage 1.5 deliverable)

Once all papers have been converted, add a `references.qmd` to the project:

```markdown
---
title: "References"
bibliography: wdt_references.bib
nocite: |
  @*
---

All works cited across the WDT paper series.
```

The `nocite: '@*'` tells Quarto to include every entry in the `.bib` file, even if not
directly cited in this page. This gives visitors a single bibliography for the entire
project with DOI links.

Add it to `_quarto.yml` sidebar under a "Reference" section:

```yaml
- text: "Full Bibliography"
  href: references.html
```

---

## Handling `.bib` note fields

Some entries in `wdt_references.bib` carry `note` fields flagging issues for the author
(unverified DOIs, citation errors in specific papers). These will not appear in the rendered
bibliography — standard CSL styles do not render `note` fields in the output. No action
needed; the notes are for the author's internal use.
