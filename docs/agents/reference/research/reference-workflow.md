
# Reference workflow (references.bib and internal.json)

The research role manages the WDT project's reference database. The authoritative files are:

- **`internal.json`** — hand-maintained source of truth for internal paper tracking, cross-citation index, flags, and alt-author overrides. The research role reads it and updates it. Never overwrite fields the skill does not own (see §internal.json structure below).
- **`references.bib`** — the BibTeX database of all external references. Updated by the research role on every ingestion or web-check run. Single file, overwritten in place.

There is no separate Markdown reference document. `internal.json` carries the cross-citation data that was formerly in that document; `references.bib` carries the full bibliographic metadata.

Read `bib-conventions.md` for BibTeX format rules and entry-type mapping.

---

## internal.json — structure and ownership

`internal.json` has five top-level keys. The research role **reads all of them** and **writes only to `citations` and `flags`** (and only with author confirmation). Never touch `internal_papers`, `alt_author_overrides`, or `meta_note` — those are author-maintained.

| Key | Owner | What it contains |
|---|---|---|
| `meta_note` | Author | File-level notes |
| `alt_author_overrides` | Author | Non-standard author forms used in specific papers |
| `internal_papers` | Author | Paper registry: shortcode, version, `outbound_ext_citation_ids`, `outbound_internal`, `flag_ids`, notes |
| `citations` | **Research role (with confirmation)** | Granular cross-citation records: which sections of which paper cite which `ref_id` |
| `flags` | **Research role (with confirmation)** | Bibliographic issue records |

**`outbound_ext_citation_ids`** in each `internal_papers` entry lists citation keys in the format `AuthorYYYY__SHORTCODE`. The bare `ref_id` (before `__`) is the BibTeX key. This is the authoritative list of what a paper cites externally.

**`citations` array** entries have the shape:
```json
{
  "id": "AuthorYYYY__SHORTCODE",
  "ref_id": "AuthorYYYY",
  "paper_id": "SHORTCODE",
  "relationship": "in_text" | "references_only",
  "sections": ["2.1", "4.3"],
  "notes": null
}
```

**`flags` array** entries record open bibliographic issues (wrong year, wrong journal, orphan reference). When a new flag is raised by web-check, present it to the author and add it to the array only on confirmation.

---

## Main papers and appendices

**Main papers** (e.g. VAL) carry `@CiteKey` in-text citations. Their `outbound_ext_citation_ids` in `internal.json` will be non-empty. Use `internal.json` as the authority; scan the paper body as a verification check.

**Appendices** (e.g. VAL.A) often carry zero external citations — they are mathematical or simulation companions citing only internal WDT papers. When `outbound_ext_citation_ids` is `[]` and the body scan confirms no `@` citations, this is correct. No `.bib` entries are added from an appendix; its contribution is internal cross-reference data only.

**Paired ingestion** (main + appendix uploaded together): extract external citations from the main paper only; confirm the appendix is clean; update cross-citation data in `internal.json` for both; scope web-check to the main paper's new or changed entries.

---

## Entry Point 1 — Paper ingestion

**Trigger:** User names a paper or pair in `source/`, or asks to check/update references.

### Step 0 — Load internal.json and references.bib

Both files are in `registry/` (`registry/internal.json`, `registry/references.bib`). Load both before doing anything else.

From `internal.json`, extract for each paper being ingested:
- `outbound_ext_citation_ids` and `outbound_internal`
- `flag_ids` → look up each flag in the `flags` array for full text
- `notes`

From `citations`, pull all records matching the paper's shortcode as `paper_id`.

If `internal.json` is missing, note the gap and proceed with body-text extraction only, flagging that results are unverified.

If `references.bib` is missing, initialise it — see `bib-conventions.md` for structure.

### Step 1 — Extract citations

**External citations:** Strip `__SHORTCODE` suffixes from `outbound_ext_citation_ids` to get the bare BibTeX keys. Cross-check against `@`-style citations in the paper body. Flag any discrepancy between `internal.json` and the body text rather than silently resolving it.

For each `ref_id`, look up its `citations` record (matching `ref_id` + `paper_id`) to get section data and relationship type. If no `citations` record exists yet for this paper × reference pair, that is a gap to fill in Step 3.

**Internal citations:** Use `outbound_internal`. These go into the Internal Bibliography block of a generated References section; they are not added to `references.bib`.

**Appendix with no external citations:** Record as clean and proceed. Nothing is added to `.bib`.

### Step 2 — Check references.bib

For each bare `ref_id` extracted in Step 1, check whether a BibTeX entry with that key already exists in `references.bib`.

- **Already present:** No `.bib` action needed. Proceed to update cross-citation data in Step 3.
- **Missing:** The entry must be added. Attempt to construct it from the paper's References section text. If that text is not available or is ambiguous, flag it for web-check in Step 4.

### Step 3 — Update internal.json cross-citation data

For each `ref_id` in this paper's citation set:

**New `citations` record** (no existing entry for this `paper_id` × `ref_id` pair): draft the record with `ref_id`, `paper_id`, `relationship` (from `internal.json` `outbound_ext_citation_ids` or body scan), and `sections` (from the `citations` array or body scan). Present to the author for confirmation before writing.

**Existing `citations` record**: if sections have changed (e.g. paper has been revised), present the diff and ask for confirmation before updating.

**Flags:** For any `ref_id` whose `flag_ids` list a known issue, copy the flag text into the `.bib` `note` field for that entry. Do not silently propagate errors.

**`references_only` entries** (appear in a paper's References section but have no in-text `@` citation): flag for author decision — these may be orphan references. Do not add a `citations` record with sections for them; set `sections: []` and `relationship: "references_only"`.

**Alt-author overrides:** Where `alt_author_overrides` applies to a `ref_id` for this paper, note it in the `citations` record's `notes` field for use when generating that paper's References section.

After presenting proposed `internal.json` updates and receiving confirmation, write the updated file.

### Step 4 — Web-check

Before running web-check, present the scope template from `scope-template.md` and wait for the user to confirm or fill it.

**Pass A — Verification.** For entries added or updated in Step 2 (not the full `.bib` — only new or changed entries this run), search and verify: author names, year, journal, volume, issue, pages, DOI. Flag every discrepancy. Do not correct silently — present each discrepancy with the current `.bib` value and the verified value, and update only on confirmation. If a verified correction resolves an open flag, note it and ask the author to confirm the flag can be closed.

**Pass B — Coverage scan.** Search for relevant literature not yet in `references.bib`. For each candidate: state which WDT strand it bears on and provide the full APA 7th citation. Ask whether to add it. Do not add without confirmation. Confirmed additions go into `.bib` immediately; a `citations` record is created if the author indicates which paper(s) will cite it.

### Step 5 — Write outputs

Write the updated `registry/references.bib` in place (on a branch).

If `internal.json` was updated in Step 3, write `registry/internal.json` in place as well.

Report a brief summary: `.bib` entries added, entries updated, discrepancies found, flags raised or closed, coverage candidates flagged, `internal.json` records updated.

---

## Entry Point 2 — LR brief

**Trigger:** User explicitly requests the LR brief or an update to it.

**What the brief is:** A structured editorial document for the writing role to use when writing the new Systematic Literature Review. It is the plan, not the prose.

**What the brief contains:**

1. **Scope statement.** Derived from the scope template the user has confirmed.

2. **Section architecture.** Proposed top-level sections for the new LR, each with a one-sentence rationale. Grounded in `references.bib` coverage — sections map to strands the database actually contains references for.

3. **Literature strand map.** For each section: key anchor citations (from `references.bib`), a note on what has changed since the original LR, and the forward-link target — which WDT companion paper and section picks up that strand. Forward-link targets are derived from `website/site/pages/Project-Map.md`. Read it before producing the brief.

4. **New coverage additions.** References added via Pass B that are not in the original LR, organised by strand.

5. **Reference to .bib.** The brief points to `references.bib` for BibTeX-formatted citations. It uses shorthand (Author, Year) in the brief body; the writing role pulls full entries from the `.bib`.

**Update briefs:** Produce a dated diff addendum, not a full reissue. The addendum covers: new references added since the last brief (by strand), web-check corrections affecting cited works, forward-link target changes.

**Output:** `LR_Brief_YYMMDD.md` (or `LR_Brief_YYMMDD_update.md` for addenda). Write to `research/notes/`.

---

## Entry Point 3 — Generate a paper's References section

**Trigger:** User asks to generate or regenerate a References section for a specific WDT paper.

### Step 1 — Identify citations

Load `internal.json`. Retrieve the paper's `outbound_ext_citation_ids` — strip `__SHORTCODE` to get BibTeX keys. Load `references.bib`. Check `alt_author_overrides` for any applicable override for this paper. Retrieve `outbound_internal` for the Internal Bibliography block.

If the paper is available, scan its body to confirm the citation set.

**Appendix papers:** If `outbound_ext_citation_ids` is empty, no References section is generated — only an Internal Bibliography block (if the document format uses one).

### Step 2 — Render

Retrieve each BibTeX entry from `references.bib`. Render as APA 7th Markdown, applying any `alt_author_overrides`. Sort alphabetically by first author surname, then year. See `bib-conventions.md §Generating a paper's References section from the .bib` for render patterns.

```markdown
## References {.unnumbered}

Author, A. B., & Author, C. D. (Year). Title. *Journal*, *vol*(issue), pp–pp. https://doi.org/xxxxx
```

Append an Internal Bibliography block for any `outbound_internal` citations, in the format from `bib-conventions.md §Internal Bibliography format`.

### Step 3 — Deliver

Output in-conversation or as a file — ask the user which they prefer before writing. Flag any entries whose `.bib` `note` field carries an unresolved flag.

---

## What the research role does not do

- Does not rewrite LR prose — that is the writing role's job.
- Does not make formatting or voice changes to WDT papers — that is the writing role's job.
- Does not update `internal_papers`, `alt_author_overrides`, or `meta_note` in `internal.json` — those are author-maintained.
- Does not add to `references.bib` or `internal.json` without author confirmation.
- Does not infer content from papers not available for reading — flags the gap instead.

---

## Paper shortcodes

| Shortcode | Paper |
|---|---|
| WP | The White Paper |
| MF | Moral and Philosophical Foundations |
| LR | A Systematic Literature Review |
| LR.A | Research Gaps in the Existing Literature |
| LR.B | Intellectual Background and Reference Guide |
| VAL | Valuing Wealth |
| VAL.A | Valuing Wealth — Mathematical and Simulation Companion |
| VAL.B | Valuing Wealth — Worked Examples |
| JUR | UK Jurisdiction and Data Reference Paper |
| CORP | Corporate Architecture |
| CORP.A | Corporate Architecture Appendix |
| GOV | Constitutional Governance |
| GOV.A | Constitutional Governance Appendix |
| GOV.B | Constitutional Governance — Operational Appendix |
| RATES | Rates and Revenue |
| RATES.A | Rates and Revenue Appendix |
| SWEEPS | Parameter Sweep Analysis |
| SWEEPS.A | Parameter Sweep Analysis Appendix |
| BEHAV | Behavioural Robustness and Administrative Experience |
| CLOSE | Position Closure |
| POL | Political Architecture |
| PHASE1 | Phase One |
| ENV | Environmental Effects and Transmission Channels |
| FM | First Mover |
| MOD | Modular Adoption |
| SCOPE | Scope Boundary |
| ADD | Addendum |
