# 034: Code: page cards for the writing briefs (order.md B18)

- **Status:** ready
- **Author/date:** K. Ogata with the guru, 2026-11-17
- **Depends on:** none (reads `registry/pages.yml` if 029s has landed)
- **Read:** `docs/restructure/order.md` sections 3 and 6.2; `docs/restructure/ledger-sections.md` (row format) and `ledger.md` sections 2 and 9; `docs/restructure/shortcodes.md`; `docs/model-v3/outputs.yml`, `inputs.md` (families, headers); `docs/restructure/template.md` section 2 (front matter); `docs/agents/code.md`.

## Goal
Generate one page card per page from the ledger, the manifest and the register, so a writer starts from a card that cannot drift from them.

## Decisions (author, 2026-11-17)
`docs/restructure/site.md` is approved with its eight answers (drafts under `/draft/`, hub Data block, ADOPT, PILOT and HYPO reached from their parents, `source/hub.md`, pending-page links rewritten to `retired.html`, glossary seeding before the gate, standalones move after the gate). The data gate holds: no spoke or hub prose. This brief builds on fixtures and delivers without the model data. It is one of the first parallel set (029s, 030c, 031s, 032r, 033c, 034c); the Touches lists do not overlap.

## Design
`python pipeline/page_cards.py` writes one file `docs/restructure/pages/<ID>.md` for each of the 26 units (the 22 spokes, three standalones and the hub), each holding: the ledger rows whose target is the page (K and M rows, with disposition, model flag, words and note); the outputs whose `element:` lists the page; the register input families it needs (ids from the outputs' metrics and the ledger flags); its neighbours from `order.md` section 2 (cites, cited by, wave, position); the front matter skeleton of `template.md` section 2 (`spoke`, `question` empty, `depends`, `outputs`, `inputs`, `budget` 6000, `status: draft`); and kept words against the cap. Generated, never edited by hand: a banner says so. The cards are data and contain no spoke prose; `question` is left blank for the writer and author.

## Touches
`pipeline/page_cards.py` (new), `docs/restructure/pages/` (generated), `tests/cards/` (new), this brief's progress block. Nothing else.

## Acceptance criteria
- 26 cards exist; the kept-word totals agree with `ledger.md` section 2 (listed in the change report).
- Every `element:` entry of `outputs.yml` appears on exactly the cards of its pages.
- Rerunning the script changes nothing.
- `git diff --stat` shows only the Touches list.

## Checks to run
`pytest tests/cards`; sum of words per card against `ledger.md` section 2; one card read in full.

## Out of scope
Writing any page text, choosing questions, editing the ledger or the manifest.

## Open questions
The implementer asks rather than guesses.

## Implementation notes
<!-- progress:start -->
- **Done:**
- **Next:**
- **Decisions:**
- **Gotchas:**
- **Resume:**
- **Not run:**
- **State:**
<!-- progress:end -->
