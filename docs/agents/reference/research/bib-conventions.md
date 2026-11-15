# BibTeX Conventions for wdt_references.bib

Full specification for the WDT BibTeX companion file. Read this whenever creating or updating `wdt_references.bib`.

---

## File header

The file opens with a comment block:

```bibtex
% WDT Master Reference Database — BibTeX format
% Converted from: 0_4_YYMMDD[a]_WDT_References.md (NNN entries)
% Conversion date: YYYY-MM-DD
%
% Conventions:
%   Citation keys:  AuthorYYYY (1–2 authors); AuthorEtAlYYYY (3+)
%                   Disambiguated with a/b where needed (e.g. Gangl2015a)
%   Entry types:    @article, @book, @incollection, @techreport (NBER/CESifo),
%                   @unpublished (SSRN-only), @misc (institutional/gov reports)
%   DOIs:           Included where present in 0.4; unverified DOIs flagged in note field
%   Diacritics:     LaTeX-encoded throughout
%   Open flags:     Noted inline where they bear on the entry itself
%   Internal refs:  WDT companion papers excluded (project tracking, not bibliography)
```

Update "Converted from" and "Conversion date" on every run.

---

## Citation key format

| Authors | Key format | Example |
|---|---|---|
| 1 author | `SurnameYYYY` | `Perret2021` |
| 2 authors | `Surname1Surname2YYYY` | `DomarMusgrave1944` |
| 3+ authors | `FirstSurnameEtAlYYYY` | `AgrawalEtAl2025` |
| Same author(s), same year | Append `a`, `b` | `Gangl2015a`, `Gangl2015b` |

Rules:
- Surname only — no initials, no spaces, no hyphens
- For hyphenated surnames, concatenate without hyphen: `LondonoVelezAvilaMahecha2025`
- For surnames with diacritics in the key, drop the diacritic: `Jorda` not `Jordà`, `Brulhart` not `Brülhart`
- Institutional authors: use the institution acronym + year: `OECD2018`, `HMRC2025a`

---

## Entry types

| Work type | BibTeX type | Notes |
|---|---|---|
| Journal article | `@article` | Standard |
| Book | `@book` | |
| Book chapter | `@incollection` | Requires `booktitle`, `editor`, `pages` |
| NBER / CESifo / IMF working paper | `@techreport` | Use `type` and `number` fields |
| SSRN-only working paper | `@unpublished` | No `institution` field; put SSRN number in `note` |
| Government / institutional report | `@misc` | Use `howpublished` for the issuing body |
| Legislation / statute | **Do not add** | Cite in paper text only; not in 0.4 or .bib |
| Website without stable authorship | **Do not add** | |

---

## Required fields by type

### @article
```bibtex
@article{Key,
  author  = {},
  title   = {},
  journal = {},
  year    = {},
  volume  = {},
  number  = {},   % omit if not applicable
  pages   = {},
  doi     = {},   % omit if unavailable
  note    = {}    % flags, verification status, discrepancy notes
}
```

### @book
```bibtex
@book{Key,
  author    = {},   % or editor = {} if edited volume
  title     = {},
  publisher = {},
  year      = {},
  address   = {},   % omit unless disambiguation is needed
  note      = {}
}
```

### @incollection
```bibtex
@incollection{Key,
  author    = {},
  title     = {},
  booktitle = {},
  editor    = {},
  publisher = {},
  year      = {},
  pages     = {},
  note      = {}
}
```

### @techreport (NBER, CESifo, IMF, etc.)
```bibtex
@techreport{Key,
  author      = {},
  title       = {},
  institution = {},   % e.g. {National Bureau of Economic Research}
  year        = {},
  type        = {Working Paper},   % or {Occasional Paper}, {Policy Brief}, etc.
  number      = {},   % e.g. {34512}
  doi         = {},
  note        = {}    % include verification date, revision notes
}
```

### @unpublished (SSRN-only)
```bibtex
@unpublished{Key,
  author = {},
  title  = {},
  year   = {},
  note   = {SSRN Working Paper No.\ NNNN. doi:10.2139/ssrn.NNNN.
            [Any flag notes.]}
}
```

### @misc (government and institutional reports)
```bibtex
@misc{Key,
  author       = {},   % use {{Institution Name}} for corporate authors
  title        = {},
  year         = {},
  howpublished = {},   % e.g. {GOV.UK} or {OECD Publishing}
  url          = {},   % omit if unavailable
  note         = {}
}
```

---

## Author field encoding

- Multiple authors: separate with ` and ` (not commas)
- Corporate / institutional authors: wrap in double braces to suppress splitting: `{{HM Revenue and Customs}}`
- Diacritics: use LaTeX encoding throughout
  - é → `{\'e}` 
  - ö → `{\"o}`
  - ø → `{\o}`
  - ñ → `{\~n}`
  - à → `{\`a}`
  - î → `{\^i}`

Common encodings for author names in this database:
- Martínez-Toledano → `Mart{\'i}nez-Toledano`
- Muñoz → `Mu{\~n}oz`
- Londoño-Vélez → `Londo{\~n}o-V{\'e}lez`
- Jordà → `Jord{\`a}`
- Brülhart → `Br{\"u}lhart`
- Iacono (no diacritic) → `Iacono`
- Smedsvik (no diacritic) → `Smedsvik`
- Bjørnar → `Bj{\o}rnar`
- Straub / Werning → no diacritics

---

## Title field encoding

- Title case for books and reports; sentence case for journal articles — follow the APA 7th rule in the Markdown file
- Proper nouns and acronyms retain capitals: wrap them in braces to prevent BibTeX downcasing: `{German}`, `{Latin America}`, `{HMRC}`, `{UK}`, `{Denmark}`, `{Norway}`
- Em dashes in titles: use `--` (en-dash) in BibTeX, consistent with the Markdown file

---

## Note field usage

The `note` field carries four categories of information:

1. **Verification status:** `Verified YYYY-MM-DD.` (date of web-check)
2. **Flag references:** `Flag N: [description]. Action required in [PAPER].`
3. **Revision history notes:** e.g. `Middle initial corrected YYYY-MM-DD.`
4. **Edition / revision notes:** e.g. `Original issue June 2023; revised May 2026. Not yet journal-published -- update citation on journal publication.`

Multiple notes are separated by a line break within the field (use `\n` or just a blank line inside the braces — both compile). Keep notes concise. The full flag text lives in `internal.json` → `flags`; the `.bib` note field carries only what is needed to identify the issue.

---

## DOI field

- Include DOI wherever it appears in the Markdown 0.4 entry
- Format: bare DOI string, e.g. `10.1257/app.20220615` (no `https://doi.org/` prefix — BibTeX styles add that)
- If DOI is unverified (Flag 27 pattern), include it but add `Unverified DOI -- confirm before publication.` to the `note` field
- If no DOI exists, omit the field entirely (do not use `doi = {N/A}`)

---

## Alphabetical ordering within the .bib file

The `.bib` file is sorted alphabetically by citation key (A to Z), matching the sort order of Section 1 of the Markdown file. This makes manual cross-checking between the two files straightforward. Group entries under letter-divider comments:

```bibtex
% -----------------------------------------------------------------------
% A
% -----------------------------------------------------------------------

@article{AgrawalEtAl2025, ...}

% -----------------------------------------------------------------------
% B
% -----------------------------------------------------------------------

@book{Bradford1986, ...}
```

---

## Sync rules (references.bib ↔ internal.json)

After every ingestion or web-check run, verify:

1. **Key alignment:** Every `ref_id` in `internal.json` → `citations` must have a corresponding entry in `references.bib`. If a `citations` record exists for a `ref_id` with no `.bib` entry, that is a gap to resolve before delivering outputs.

2. **DOI consistency:** If a DOI was confirmed during web-check, the `.bib` `doi` field must carry the verified value (bare, without `https://doi.org/` prefix).

3. **Flag consistency:** Every open flag in `internal.json` → `flags` that bears on a specific `.bib` entry must have a corresponding note in that entry's `note` field. Closed flags do not need to appear in the `.bib`.

4. **`references_only` entries:** Where a `citations` record has `"relationship": "references_only"` and `"sections": []`, the `.bib` entry's `note` field should carry the orphan-reference flag text so it is visible at reference-generation time.

---

## Internal Bibliography format

WDT companion papers are tracked in the Markdown file's Section 2 (Internal Bibliography Index) and are **not** added to the `.bib`. The `.bib` comment header states this explicitly: `Internal refs: WDT companion papers excluded`.

When generating a paper's References section (Entry Point 3), internal WDT papers cited via the Internal Bibliography Index are rendered in a separate block at the end of the References section (or as an Internal Bibliography appendix if the paper uses that structure), using this plain-text format (not BibTeX):

```
[SHORTCODE] — Full paper title (vX.X, DD Month YYYY). Internal WDT document.
```

Example:
```
[GOV] — The Wealth Delta Tax: Constitutional Governance (v2.8, 10 August 2026). Internal WDT document.
[RATES] — The Wealth Delta Tax: Rates and Revenue (v2.3, 8 August 2026). Internal WDT document.
```

Version and date are taken from `internal.json` → `internal_papers` → `version` and `version_date` for the cited paper. If those fields are absent, fall back to the 0.0 Summary header block.

---

## Generating a paper's References section from the .bib

When Entry Point 3 is triggered:

1. Identify the paper's citation set from `internal.json` → `internal_papers` → `outbound_ext_citation_ids` for the target paper. Strip `__SHORTCODE` suffixes to get bare BibTeX keys.
2. For each identified external citation key, retrieve the BibTeX entry.
3. Render as APA 7th Markdown using these rules:

| BibTeX type | APA 7th render pattern |
|---|---|
| `@article` | `Surname, A. B. (Year). Title. *Journal*, *vol*(issue), pp–pp. https://doi.org/xxx` |
| `@book` | `Surname, A. B. (Year). *Title*. Publisher.` |
| `@incollection` | `Surname, A. B. (Year). Chapter title. In E. Editor (Ed.), *Book title* (pp. pp–pp). Publisher.` |
| `@techreport` | `Surname, A. B. (Year). *Title* (Type No. NNN). Institution. https://doi.org/xxx` |
| `@unpublished` | `Surname, A. B. (Year). *Title* (SSRN Working Paper No. NNNN). https://doi.org/10.2139/ssrn.NNNN` |
| `@misc` | `Author/Institution. (Year). *Title*. Publisher/Howpublished. URL` |

4. Sort rendered entries alphabetically by first author surname, then year (per `0.4_structure.md §Sorting rules`).
5. Append Internal Bibliography block if any companion papers are cited.
6. Flag any entries where the `.bib` `note` field contains an unresolved flag — list these separately after the References section so the author knows what needs checking before submission.

---

## Example complete entry

```bibtex
@article{AgrawalEtAl2025,
  author  = {Agrawal, David R. and Foremny, Dirk and
             Mart{\'i}nez-Toledano, Clara},
  title   = {Wealth Tax Mobility and Tax Coordination},
  journal = {American Economic Journal: Applied Economics},
  year    = {2025},
  volume  = {17},
  number  = {1},
  pages   = {402--430},
  doi     = {10.1257/app.20220615},
  note    = {Verified 2026-07-27.}
}
```

Corresponding Markdown entry in 0.4:

```
Agrawal, D. R., Foremny, D., & Martínez-Toledano, C. (2025). Wealth tax mobility and tax coordination. *American Economic Journal: Applied Economics*, *17*(1), 402–430. https://doi.org/10.1257/app.20220615
[verified 260727]

→ LR §3, §10, §12
→ BEHAV §2.1, §9.2
→ CLOSE §1.2, §3, §9
```
