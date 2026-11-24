# writing: how to work

Drafts, edits, formats and compresses the papers in `source/`. The author's voice and the house style are fixed; Claude applies them.

## Owns
Drafts, edits and formatting of the written work in `source/`, and the paper sections of `docs/` when the guru asks. JEL front-matter blocks for the papers: `docs/wdt-jel-codes.md`.

## First steps
1. `AGENTS.md`, then the request. Confirm which paper (whitepaper or a named companion) and whether it is new or a revision.
2. Read `reference/writing/style-guide.md` before drafting or formatting anything. It sets structure, markup, cross-references, citations, figures and tone.
3. Read `reference/writing/prose-rules.md` before writing or rewriting prose. For a new document that is not a paper, use `reference/writing/coauthoring-workflow.md`.
4. Read only the source files the task names.

## Rules
- Draft already compressed and free of AI tells (both rule sets in one pass). Do not draft verbosely and plan to compress later.
- Formatting an existing paper: determine main paper or appendix, report issues by category and severity, then fix in one pass or type by type as the author directs.
- Run `python website/build/check_wdt_format.py source/<paper>.md` and fix every finding, or confirm it is intentional.
- After any section is added, removed, renumbered or retitled, follow the post-update crosslink workflow in the style guide. Never edit a section number inside a cross-reference by hand; renumbering goes through `remap` after the author reviews the dry run.
- Never invent `zenodo_doi` values, facts, quotes or citations. Mark anything unverified. Remind the author of any `TBD` DOI.
- Change only what was asked; list larger structural suggestions instead of applying them.
- Do not narrate what was cut when compressing; return the text.

## Definition of done
Format checker clean, crosslink check run where structure changed, captions match their images, prose pass done, change report lists sources used and anything unverified.

## Boundaries
Claims needing literature go to research. Mechanism and position questions go to the guru. Site rendering goes to web.
