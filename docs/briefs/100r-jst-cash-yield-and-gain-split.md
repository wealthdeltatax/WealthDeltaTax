# 100: Split the JST total return into cash yield and holding gain (data design)

- **Status:** ready
- **Author/date:** K. Ogata with the guru, 2026-11-21
- **Depends on:** none
- **Read:** `docs/model-v3/household-flow-plan.md`; `docs/research/094r-kernel-map-and-household-accounts.md` (A2 and B4); `model_v3/pack/build_gbr.py`; `model_v3/pack/GBR/returns.csv`; `model_v3/pack/GBR/source/jst_r6.json` (`meta.variable_descriptions_note`); `docs/model-v3/inputs.md` (I-D1a, I-D1a2).

## Goal
The kernel credits one total real return. The household account needs cash yield `y` and holding gain `g_h` apart, by asset class. The split exists in the JST file and the pack builder drops it. Design the pack table that would carry it, and show that it reproduces the pack's total return.

## Decisions (author, 2026-11-21)
Same as 097r; Scenario B. This is a data design: **no pack, builder or code edit**, and no change to I-D1a.

## Design
1. List the JST variables for the UK (`eq_div_rtn`, `eq_capgain`, `housing_rent_rtn`, `housing_capgain`, `bond_rate`, `bill_rate`, and any total-return or price series), with their JST definitions, units and years, from the file and the JST documentation (`Rates Data/JSTdatasetR6.xlsx`).
2. Show, by year and by class, whether `y + g_h` reproduces the total return columns the pack already uses (`eq_tr`, `housing_tr`, `bond_tr`, `capital_tr`), to a stated tolerance (arithmetic against geometric combination: say which), and list the years and classes where it does not and why.
3. Real conversion: how `y` and `g_h` convert to real terms with the pack's CPI, and whether the nominal-position revaluation (cash, bonds, debt) belongs in `g_h`.
4. The **portfolio-weighted** split: how `capital_tr` is built from the classes in the pack (weights), and the implied aggregate `y` and `g_h` for the same weights.
5. A proposed table schema for the pack (columns, units, years, provenance) and the manifest change it needs, as a spec only.
6. What the split is **not**: it is the market return decomposition, not the household's retained income; say so.

## Touches
`docs/research/100r-jst-cash-yield-and-gain-split.md` (new), `docs/research/data/100r/*.csv` (new, the reconstruction), this brief's progress block, `docs/agents/friction-log.md`. No code, pack, register or manifest edits.

## Acceptance criteria
- The reconstruction table is committed and the identity check (item 2) is shown with its tolerance and exceptions.
- The schema (item 5) is specified without editing the pack.
- No claim about household saving or retained income.

## Checks to run
`python -I pipeline/check_agent_docs.py`.

## Out of scope
Changing the builder, the pack hash or I-D1a; any use of the split in the model.

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
