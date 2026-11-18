# 064: Site: glossary registry and generator (site.md B14)

- **Status:** ready
- **Author/date:** K. Ogata with the guru, 2026-11-18
- **Depends on:** none (B1, `registry/pages.yml`, is merged)
- **Read:** `docs/restructure/site.md` (Q7 and the author's answers, section 8.1 and 8.2); `docs/restructure/site/ids.md` section 5 (the `glossary.yml` and `build_glossary.py` rows) and Q11; `docs/restructure/site/nav.md` section 2.6 (utility pages); `docs/restructure/order.md` section 3 rule of 2026-11-17 (glossary seeding by copying is allowed); `registry/pages.yml` (header comment and the `GLOSS` and spoke rows); `pipeline/build_glossary.py` (legacy, read whole: 404 lines); `site/pages/glossary.md` (the legacy output, shape only); `docs/model-v3/metrics.md` and `docs/model-v3/stage-c-decisions.md` (where the seed terms are fixed); `docs/agents/web.md`.

## Goal
Replace the paper-only glossary build with a hand-kept `registry/glossary.yml` (one row per term: definition, owning page, aliases), a generator that writes the glossary page and a lookup file the spoke checker can read, and tests that keep the registry honest. The legacy mode keeps running until cutover, so the live site does not change.

## Decisions (author, 2026-11-18)
- Q7 and Q11 of `site.md` and `ids.md`: one hand-kept `registry/glossary.yml` (term, definition, home spoke); spokes have no `# Glossary` section, a spoke defines a term in a clause where it uses it. `build_glossary.py` keeps linking each term to the pages that use it.
- Seeding by copying existing definitions is not spoke prose and may start before the data gate; any new or reworded definition waits for the gate.
- This brief builds on fixtures and delivers without the model data. It writes no spoke or hub prose.

## Design
1. **Schema of `registry/glossary.yml`** (a top-of-file comment states it, as `pages.yml` does): a list of rows with `term` (display form, unique ignoring case and surrounding spaces), `definition` (one paragraph, plain markdown, no hooks), `owner` (a page id from `registry/pages.yml`, type `spoke`, `hub`, `appendix` or `standalone`; the page that defines the term), `aliases` (list of other spellings the generator and checker accept; may be empty), `source` (the file in this repository the definition was taken from, as a path and section, so a reviewer can check it; required for seeded rows), `status` (`seeded` or `written`; this brief creates only `seeded`). A definition that contains a number from the model is a hook (`{{o:ID}}` or `{{i:ID}}`), never a typed figure; `hooks.md` section 4 is read only. The brief does not resolve hooks.
2. **Seed (copy only, with citation).** Enter a row only where a definition is already fixed in a design document of this repository, copied in the document's own words and cited in `source`. The expected set, from `metrics.md` and `stage-c-decisions.md`: level 1 and level 2 uncertainty, the three named schedules (S_low, S_central, S_high), closure share, break-even mean return, retired taxes, the taxpayer burden M2, non-payer savings M4a. Owner pages: UNCER, FISC, PAY and FUND as the page list in `pages.yml` and the ledger dispose; where the owner is not stated in a design document, set it to the page of the metric's `element:` in `docs/model-v3/outputs.yml` and say so in the change report. The legacy glossary entries of the old papers (about 12,300 words in `source/`, merged into `site/pages/glossary.md`) are **not** copied by this brief; Q7 allows it, but the deduplication of 30 papers is its own job, left for the guru to brief. Do not read `source/` papers; reading `site/pages/glossary.md` for its shape is enough.
3. **Generator.** `pipeline/build_glossary.py` gains a second mode, selected by `--registry registry/glossary.yml` (with `--pages registry/pages.yml`, `--out <glossary.md>`, `--lookup <glossary-lookup.json>`, both paths arguments with no default that writes into a tracked file). Legacy mode (`--papers`, `--contents`, `--out`) is unchanged byte for byte, so `deploy.yml` and the current site keep working and the workflow is not edited. In registry mode the generator: validates the file (design 4), writes the glossary page in the same front-matter and entry markup as the legacy output (title, description, A to Z jump bar, one block per term with its definition and "Defined on" link to the owner page's URL from `pages.yml`), and links each term to the pages that use it only when `--contents` is given (sections of legacy papers), otherwise omits "Used in"; the new spokes have no usage list yet and this is stated in the page.
4. **Validation (run by the generator and by tests):** required fields present; no unknown field; duplicate term (case-insensitive); an alias equal to another row's term or alias (collision); an alias equal to its own term; owner not in `pages.yml` or of a type that cannot own a definition (calculator, pending, legacy, site); `status` not in the two values; `source` missing on a `seeded` row, or naming a file that does not exist; a definition with a typed figure matching a pattern the guru lists in the test (a digit sequence followed by `%` or `pp`), unless inside a hook. Every error names the row's term. Exit code 1 on any error.
5. **Lookup file for the spoke checker (B6).** `--lookup` writes JSON: `{"schema": "wdt-glossary/1", "terms": [{"term", "owner", "aliases", "slug"}...]}` sorted by term, with `slug` the anchor on the glossary page (`glossary.html#<slug>`). B6 reads exactly this: it uses `term` and `aliases` to tell a defined term from an undefined one on first use, `owner` to check that a spoke defining a term is its owner and that other pages cross-reference rather than redefine, and `slug` to build the link. The checker's word lists and waiver syntax are not in this brief. A change to this shape after B6 starts is a question to the guru.

**Shared interfaces, fixed before any stage starts** (a build brief never edits them; a mismatch is a question to the guru): the output file shape is `schema wdt-outputs/1` as `pipeline/validate_outputs.py` checks it and `docs/restructure/site/hooks.md` section 3 with the 030c rulings; the country pack format is `docs/model-v3/country-pack.md`; the id lists are `docs/model-v3/outputs.yml` and the module-to-id table of `architecture.md` 2.10; the Samples contract is `architecture.md` 2.9; the layers and import rules are `architecture.md` 5.1.

This is build item B14 of `site.md` section 8. One session, one lane; the brief ends in a stop: tests pass, change report written, branch merged by the auto-merge rule. If a criterion cannot be met, or any file in `source/` would have to be touched, stop with NEEDS THE AUTHOR.

## Touches
`registry/glossary.yml` (new), `pipeline/build_glossary.py`, `tests/glossary/` (new), this brief's progress block. Nothing in `source/`, `site/`, `.github/`, `registry/pages.yml`, `model_v1/`, `model_v2/`, `model_v3/`, docs outside this brief. `pipeline/build_glossary.py` is not edited elsewhere by any brief before cutover (B15 and B16 wire it into the workflow).

## Acceptance criteria
- `registry/glossary.yml` validates in registry mode with exit code 0; every seeded row has a `source` that exists and an owner that exists in `pages.yml`.
- Legacy mode output is identical to the output of the unchanged script on the same inputs (diff, using `source`, `registry/contents.yml`, to a temporary path).
- `--lookup` writes the JSON of design 5; a test loads it and checks the sorted order, the slugs and that every alias is present.
- Tests under `tests/glossary/` cover: schema (missing and unknown fields, bad `status`), duplicate terms, an alias colliding with a term or another alias, an unresolved owner and an owner of a forbidden type, a missing `source` file, a typed figure, a hook accepted, and the page markup (jump bar, one block per term, owner link). Each failing test uses a fixture file under `tests/glossary/fixtures/`.
- `git diff --stat` shows only the Touches list.

## Checks to run
`pytest tests/glossary -q`; the legacy-mode diff above; `pytest tests/pages -q` (unchanged). The local site build of `docs/agents/web.md` is not needed because no site file, workflow or page changes; skip it and say so. Run the new tests as their own command (the `conftest.py` files of the test folders clash in one session).

## Out of scope
Copying the legacy glossary entries; writing or rewording a definition; hook resolution; the checker; the glossary link text in spokes; the deploy workflow and the navbar (`Glossary` already links to `glossary.html`); cutover.

## Open questions
Ask rather than guess: an owner page for a seed term that no design document names; a term whose design-document definition contains a figure.

## Guru rulings, 2026-11-18
A second `--registry` mode with the legacy mode unchanged byte for byte: accepted. The 12,300 words of legacy glossary are not copied; a de-duplication brief is the guru's to write later. Number 064 is free (059r, 060c to 064s are the guru's reservation).

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
