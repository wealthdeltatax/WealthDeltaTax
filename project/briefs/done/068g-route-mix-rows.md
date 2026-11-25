# 068: Add the route mix to the input register

- **Status:** done, merged 2026-11-19
- **Author/date:** K. Ogata with the guru, 2026-11-19
- **Depends on:** none
- **Read:** `docs/model-v3/inputs.md` (conventions: row format, `(J)`, the Coverage and Source cells, how an added family is declared); `docs/model-v3/architecture.md` 2.3 and the module table (`base`: "register rows for the route mix"); `model_v2/WDT_Params.toml` lines 116 to 135, 195 to 205 and 270 to 277 (`[val_gen.route_shares]`, `c_share_sens`), 1595 to 1610 (`[route_b]`); `docs/model-v3/judgement-decisions.md`; `pipeline/build_inputs.py`; `registry/inputs-display.yml`.

## Goal
The register holds the route mix the kernel runs on, so `base.py` reads it from the register rather than inventing it (the architecture said "register values" but no rows existed).

## Decisions (author, 2026-11-19)
- Adopt v2's baseline D13 as central: initial value split A 50%, B 25%, C 8%, D 17%. Route C low 5 and high 10 (v2's `c_share_sens`, 5, 8, 10), with Route A absorbing the difference (A low 48, central 50, high 53; B and D fixed). Route B is paid by sale (payment mode `sale`) in the central run.
- All of these are judgement rows `(J)`, listed in `judgement-decisions.md` as pending for the author (gate G3); the evidence cell says plainly that the source is the v2 baseline, a framing value and not an estimate, as v2's own comments say.
- `[route_b].share_by_wealth` and the other Route B payment modes (lien, income) are not rows: they are placeholders in v2 and unused under `sale`; say so in the Coverage cell and leave them out.

## Design
1. Add rows for the four shares and the Route B payment mode in the family where the register's conventions put valuation and routes (choose; report the ids). Shares are in % of initial value; the mode row is text (`sale`) with its alternatives named.
2. Add the rows to `judgement-decisions.md` (pending) and update the counts in the register header (rows and `(J)`).
3. Regenerate: `python pipeline/build_inputs.py`; add display entries to `registry/inputs-display.yml`; regenerate the page cards (`python pipeline/page_cards.py`) and any fixture the data tests embed (`python tests/data/make_fixture.py`).
4. Update the pinned row-count tests in `tests/data/` (they read 274 and the (J) count; the model's P9 reads the count from the register).

## Touches
`docs/model-v3/inputs.md`, `docs/model-v3/judgement-decisions.md`, `registry/inputs.json` (regenerated), `registry/inputs-display.yml`, `docs/restructure/pages/` (regenerated), `tests/data/` (count pins and the regenerated fixture), this brief's progress block. If `model_v3/` tests pin the count (P9), report it to the guru and do not edit them.

## Acceptance criteria
- Five new rows (four shares, one mode) with low, central, high satisfying the ordering rule except the mode; the four shares at central sum to 100 and at each end of the C range sum to 100.
- `python pipeline/build_inputs.py` exit 0; `pytest tests/data`, `tests/gate`, `tests/cards`, `tests/model_v3` pass (separate commands).
- `git diff --stat` limited to the Touches list.

## Checks to run
The commands above.

## Out of scope
The model, `base.py`, the pack, any other register row.

## Open questions
None. If a register convention forbids a text row, say so and propose the form.

## Implementation notes
<!-- progress:start -->
- **Done:** family D13 (route mix, tier 2) in `inputs.md`: I-D13a Route A 48/50/53, I-D13b Route B 25/25/25, I-D13c Route C 5/8/10, I-D13d Route D 17/17/17 (% of initial value), I-D13e Route B payment mode `sale`. All five `(J)`, evidence cell says framing value from the v2 baseline. Shares sum to 100 at central, at C low (53+25+5+17) and at C high (48+25+10+17). Added to `judgement-decisions.md` (pending); counts now 279 rows and 95 `(J)`; display entries added; `registry/inputs.json`, the fixture regenerated; row-count pins in `tests/data/test_build_inputs.py` 274 to 279.
- **Next:** the author decides the five rows at gate G3; 051c can read the route mix from the register.
- **Decisions:** family D13 (v2's own name for the baseline), placed after D11 under Tier 2; ids I-D13a to e. Columns of the A and C rows are not one scenario (A low pairs with C high); the evidence cell says so.
- **Gotchas:** the mode row is text, so `inputs.json` has `low`, `central` and `high` null for I-D13e and the word is kept in `nulls.<col>.raw` (`sale`), as for I-D11d; `base.py` must read it from there. The register summary in `inputs.md` still carries the older row-count history in its first paragraph.
- **Resume:** none; merged.
- **Not run:** none. `pytest` on `tests/data`, `gate`, `cards`, `model_v3`, `hooks` (separately): 84, 17, 8, 116, 64 pass; P9 reads the count from the register and passes at 279. The page cards regenerate unchanged.
- **State:** merged to main.
<!-- progress:end -->
