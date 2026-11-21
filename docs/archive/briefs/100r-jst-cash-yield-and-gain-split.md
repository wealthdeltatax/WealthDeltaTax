# 100: Split the JST total return into cash yield and holding gain (data design)

- **Status:** retired 2026-11-21 (merged to main, guru review)
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
- **Done:** Read the household-flow plan, 094r account map, pack builder, JST R6 source JSON, pack returns, input register and core real-return conversion. Read the official JST R6 codebook and RORE return documentation. Committed `docs/research/100r-jst-cash-yield-and-gain-split.md` and the 117-row `docs/research/data/100r/returns_decomposition.csv`. Verified equity and housing component identities, safe-return identity, aggregate weighted reconstruction, CPI-deflated identity and pack source matches.
- **Next:** Merged after guru review; retire.
- **Decisions:** Scenario B; data design only. No pack, builder, register, manifest or model edits. Bond cash yield uses `bond_rate` as a proxy; where it is YTM, the residual is not a pure observed coupon/price decomposition. Bill nominal holding gain is zero by the short-bill convention.
- **Gotchas:** `capital_tr` is available 1896–2019 with 1940–1946 missing (117 observations). JST weights are market-stock weights, not household portfolio weights. JST does not separately identify household cash or debt. The split is not household retained income or saving.
- **Resume:** `git checkout brief/100r-jst-cash-yield-gain-split`; review `docs/research/100r-jst-cash-yield-and-gain-split.md` and `docs/research/data/100r/returns_decomposition.csv`.
- **Not run:** nothing outstanding. The checker could not be run by the research agent; the guru ran it on the branch (exit 0).
- **State:** work complete; checker passed; merged to main on 2026-11-21
<!-- progress:end -->


### Change report
- **Task:** 100r — split JST total return into cash yield and holding gain.
- **Files changed:** `docs/research/100r-jst-cash-yield-and-gain-split.md` (methods, definitions, checks, real conversion and proposed schema); `docs/research/data/100r/returns_decomposition.csv` (117 annual reconstructions); this brief's progress block and report; `docs/agents/friction-log.md` (checker unavailable without local checkout).
- **What is different now:** The JST market-portfolio return is decomposed into weighted yield and holding-gain contributions. The CSV contains nominal and real class splits, annual weights and audit residuals.
- **New or changed interfaces:** None. The proposed pack schema is documentation only.
- **Acceptance criteria:**
  1. Reconstruction committed and identity shown: **met**. 117 portfolio years; equity and housing component identities pass; weighted nominal and real identities pass a tolerance of 1e-7 in decimal-return units (0.00001 percentage points). Exceptions: 1940–1946 missing; bond yield is a proxy in years using YTM; bill holding gain is zero by convention.
  2. Schema specified without pack edits: **met**. No pack, builder, manifest, register or model files changed.
  3. No claim about household saving or retained income: **met**. The note explicitly distinguishes market return from household cash retention and saving.
- **Deviations from the brief:** None substantive. The research agent could not run the checker (no local checkout or shell); the guru ran it afterwards (exit 0).
- **Risks / follow-ups:** The bond yield proxy is not uniformly an observed coupon cash flow. The weights are market-stock weights, not household-specific weights. Check the note's named limitations before phase 2 uses the series.
- **Instruction friction:** Added a 100r entry to `docs/agents/friction-log.md` for the unavailable local checker.
- **Verification:** CSV read back from GitHub: 118 lines including header, 44 columns, 117 data rows, all rows have the same width. Recalculated identities against the held JST JSON and `returns.csv`. `python -I pipeline/check_agent_docs.py`: not run by the research agent; run by the guru, exit 0.
- **Overview sections likely needing an update:** None until the branch is merged.
- **Commit / branch:** `a9127b7acabd432cf7adfa4240d6a0deadc6c1f4`, `brief/100r-jst-cash-yield-gain-split`.

