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
- **Done:** `pipeline/page_cards.py` writes 26 cards to `docs/restructure/pages/` (22 spokes, ADD, INST, SCOPE, HUB); `tests/cards/test_cards.py` (8 tests, pass).
- **Next:** guru reads a card; writing briefs start from the cards. If 029s lands `registry/pages.yml`, the script can read page ids and questions from it.
- **Decisions:** kept = K rows (standalones also show SA rows). Hub card collects rows targeting H0 to H7 and lists the UK data pack and O7 method rows. Spoke front matter only on spoke cards; `inputs: []` is left for drafting, the families and their register ids are listed on the card. Families come from `order.md` section 3, outputs from `outputs.yml`, neighbours from `order.md` section 2. ADOPT, PILOT and HYPO have no ledger rows until the split is taken (ledger 9.2), so their cards show zero words and say so.
- **Gotchas:** merged words in `ledger-sections.md` differ from `ledger.md` section 2 on 12 pages (e.g. FISC 9,050 vs 8,445, MECH 2,629 vs 1,587); kept words agree on all 19 pages. `ledger-sections.md` row "21 sec 3" has 0 words.
- **Resume:** `python pipeline/page_cards.py` then `pytest tests/cards`.
- **Not run:** none.
- **State:** done

```
Change report
- Task: 034c, page cards generator
- Files changed: pipeline/page_cards.py (new); docs/restructure/pages/*.md (26 generated); tests/cards/test_cards.py (new); docs/briefs/034c-page-cards.md (progress block)
- What is different now: each page has a generated card with ledger rows, outputs, register families, neighbours, front matter skeleton and kept words
- New or changed interfaces: python pipeline/page_cards.py [--out DIR]
- Acceptance criteria:
  - 26 cards, kept words agree with ledger.md section 2: met. FAIR 5,947; LIT 8,580; MECH 6,972; VAL 6,784; DECL 10,700; FISC 8,164; PAY 4,212; BEHAV 6,797; WELF 9,671; FUND 6,210; CORP 9,671; ATTR 6,498; GOV 10,668; POL 13,238; FIRST 1,010; WIDER 6,054; UNCER 0; LIMIT 204; FALS 12,135; hub H1+H2 293 (141+152). Standalone SA words ADD 6,789, INST 14,264, SCOPE 2,537 (ledger.md section 3)
  - Every element entry on exactly its pages: met (test over all 37 outputs)
  - Rerun changes nothing: met (byte-identical, test)
  - git diff --stat only Touches: met
- Deviations from the brief: none. Merged words are not checked (see Gotchas)
- Risks / follow-ups: ledger-sections merged words disagree with ledger.md section 2 on 12 pages; the guru should say which is current. ADOPT, PILOT, HYPO cards are empty of rows until the split is taken
- Verification: pytest tests/cards (8 passed); FIRST card read in full; rerun gives no git change
- Overview sections likely needing an update: restructure section (add pages/ and page_cards.py)
- Commit / branch: brief/034-page-cards
```
<!-- progress:end -->
