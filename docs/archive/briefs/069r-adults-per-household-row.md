# 069: Add adults per household to the input register

- **Status:** done, merged and retired 2026-11-19
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
- **Done:** added I-D4h, adults per household, GB: 1.77 / 1.93 / 1.93, flagged (J). Central = persons aged 16+ in Table 2.11 (52,043,000, R8, rows 69-74 col K) over households in Table 2.9 (26,991,000, K58). Low 1.77 = adults implied by I-D4b's assumed counts per household type (47.64m / 26.99m). Both inside 1 to 2. Added to judgement-decisions.md (96 rows); register header counts, display sidecar, inputs.json, page cards, fixture and the count pins (279 to 280) regenerated. Checks: build_inputs exit 0; tests/data 84, gate 17, cards 8, model_v3 118 passed; tests/hooks also run.
- **Next:** author to choose whether I-D4b's central should use the table-based 1.93 (its method implies 1.77); guru decides on an 18+ count (author could upload ONS mid-year population by age for 2021 to separate 16-17s).
- **Decisions:** next free D4 letter was h (I-D4g is the national balance sheet row). High equals central because no held cell supports more than 1.93. Display unit tag `ratio` with display_unit "adults per household" (no `adults` tag exists in the hooks list).
- **Gotchas:** Table 2.10 and 2.11 count individuals of all ages (63.9m); only 2.11's age bands give a 16+ count. 2.13/2.14 adult totals (50.2m, 47.1m) are 16+ not in full-time education, with missing-data exclusions: not used.
- **Resume:** n/a
- **Not run:** site build.
- **State:** done, merged
<!-- progress:end -->
