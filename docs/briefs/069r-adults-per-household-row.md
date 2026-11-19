# 069: Add adults per household to the input register

- **Status:** ready
- **Author/date:** K. Ogata with the guru, 2026-11-19
- **Depends on:** 067c (merged), 068g (merged)
- **Read:** `docs/model-v3/inputs.md` (conventions; rows I-D4b, I-D4c and their research note, `docs/research/012r-b1-derivations.md`); `docs/briefs/067c-pack-base-fields.md` progress block (why adults are not in the pack); `docs/briefs/068g` in `docs/archive/briefs/` (how a family is added); `pipeline/build_inputs.py`.

## Goal
`core/base.py` needs adults per household to turn household wealth bands into adult counts. 067c found no held table with adults by decile and left adults out of the pack, saying 051c would take adults per household from a register row. No such row exists: the number appears only inside the method behind I-D4b and I-D4c. Add it as a row with a range and a source.

## Decisions (author and guru, 2026-11-19)
- One row, family D4 (wealth distribution), id `I-D4g` or the next free D4 letter (report the id): "Adults per household, all households, Great Britain", unit `adults`, with low, central and high.
- The value is read from a held ONS file or a cited ONS source with its table and cell named. If the held files give only whole-number shares (Table 2.10, persons by seven wealth bands), say so and give the range they support; do not assume a household size. A derived central is allowed if the derivation is written in the How cell and flagged `(J)`.
- The row must agree with the bounds already used in I-D4b: its low and high must lie within 1 and 2 adults (the two bounds I-D4b uses), or the How cell says why not.

## Design
1. Find the figure and range in the held files (`Rates Data/totalwealthtables.xlsx`, the ONS households files if held); if not held, cite the ONS source and say which file the author could upload.
2. Add the row in the register's format; add it to `judgement-decisions.md` if flagged `(J)`; update counts in the register header.
3. Regenerate: `python pipeline/build_inputs.py`, `registry/inputs-display.yml` entry, `python pipeline/page_cards.py`, `python tests/data/make_fixture.py`; update the row-count pins in `tests/data/test_build_inputs.py`.

## Touches
`docs/model-v3/inputs.md`, `docs/model-v3/judgement-decisions.md` (only if `(J)`), `registry/inputs.json` (regenerated), `registry/inputs-display.yml`, `docs/restructure/pages/` (regenerated), `tests/data/` (count pins and the regenerated fixture), this brief's progress block.

## Acceptance criteria
- One new row with low <= central <= high, a cited source and cell, and a Coverage cell.
- `python pipeline/build_inputs.py` exit 0; `pytest tests/data`, `tests/gate`, `tests/cards`, `tests/model_v3` pass (separate commands).
- `git diff --stat` limited to the Touches list.

## Checks to run
The commands above.

## Out of scope
The pack, `base.py`, other register rows, I-D4a (see the guru's note in `STATUS.md` on the GDP mismatch).

## Open questions
If no held or cited source gives the figure, stop and say what the author should upload.

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
