# 072: Add the top-tail construction settings to the input register

- **Status:** ready
- **Author/date:** K. Ogata with the guru, 2026-11-19
- **Depends on:** none
- **Read:** the 052c report on branch `brief/052-revenue` (`git show origin/brief/052-revenue:docs/briefs/052c-v3-7-revenue-fund-identity.md`, Gotchas 1); `model_v2/RATES/rates_core.py` `_build_advani` and its callers (lines 408 to 599, specification only); `model_v2/WDT_Params.toml` lines 824 to 850 (`rich_list_*`, `tier_alpha`, `[rates.dist.advani]`); `docs/model-v3/inputs.md` rows I-D4d, I-D4e, I-D4f, I-W5c, I-W5d, I-W7a, I-W7b and the conventions as 071g followed them (archived `docs/archive/briefs/071g-run-settings-rows.md`); `docs/model-v3/judgement-decisions.md`; `docs/model-v3/stage-c-decisions.md`.

## Goal
The register holds every setting the base's top tail needs that it does not already hold, so `core/base.py` builds the tail from register rows and invents nothing.

## Decisions (author, 2026-11-19)
- The v3 base adopts v2's tail construction (Advani, Bangham and Leslie 2021 survey totals, the Rich List added on top, a Pareto tail splitting the named tier): the register's existing rows supply the survey top shares (I-D4d), the missing-wealth share (I-D4e) and the Rich List total (I-D4f, 350 entries, £784bn, 2026).
- New judgement rows `(J)`, framing values from v2 and not estimates, as v2's own comments say: **tail Pareto alpha** (v2 `tier_alpha` 1.5, "stylised, not sourced"; low 1.2, central 1.5, high 2.0: choose the range from v2's own sweeps if any exist, else say the range is a stated reason) and **tier cuts** (the named Rich List tier split into three cells at 1%, 10% and 100% of its members; text or three numeric rows, choose and say).
- Rich List number of entries (350): add a row if I-D4f's label does not already carry it as a number the model can read; report.
- v2's 2017/18 Rich List constants (1,000 entries, £700bn, entry £100m) and its survey constants (`s10_survey` 0.51, `s1_survey` 0.18, `s1_upper` 0.23, 5% extra) are **not** rows: the identity test I1 holds them as constants of its own (decision 2026-11-19), so it checks the port, not the data.

## Design
1. Add the rows following the register's conventions (choose family and ids, report them); each with low, central and high (ordering rule) except text rows.
2. Add them to `judgement-decisions.md` (pending) and update the header counts.
3. Regenerate `registry/inputs.json` (`python pipeline/build_inputs.py`), add `registry/inputs-display.yml` entries, regenerate the cards (`python pipeline/page_cards.py`) and the data fixture if it embeds the register, update the pinned count tests in `tests/data/`.
4. Report whether `tests/model_v3/` pins the register count (P9 reads it; do not edit).

## Touches
`docs/model-v3/inputs.md`, `docs/model-v3/judgement-decisions.md`, `registry/inputs.json` (regenerated), `registry/inputs-display.yml`, `docs/restructure/pages/` (regenerated), `tests/data/` (count pins, regenerated fixture), this brief's progress block.

## Acceptance criteria
- The new rows exist with their sources stated; counts in the register header correct.
- `python pipeline/build_inputs.py` exit 0; `pytest tests/data`, `tests/gate`, `tests/cards`, `tests/model_v3` pass (separate commands).
- `git diff --stat` limited to the Touches list.

## Checks to run
The commands above.

## Out of scope
The model, the pack, any other register row.

## Open questions
None.

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
