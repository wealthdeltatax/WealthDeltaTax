# 109: Scenario return ranges, pension accrual range and cell inputs in the register and pack

- **Status:** ready
- **Author/date:** K. Ogata with the guru, 2026-11-21
- **Depends on:** 108c (merged), 107c (merged)
- **Read:** `docs/research/104r-parameter-map-design.md` sections 3 and 5.2 (pack inputs that do not exist) and 6 (question 4: new register rows); `docs/research/data/103r/parameter_register.csv` rows F-10, F-12, F-17 to F-20, S03, S04, S05, S09; `docs/research/data/100r/returns_decomposition.csv`; `docs/research/data/101r/` (jst_split_stats.csv, ons flow derivations); `docs/research/data/102r/` (band_composition_by_pack_band.csv, stage_weights_by_pack_band.csv); `docs/research/data/104r/cell_weights.csv`; `model_v3/pack/build_gbr.py` and `model_v3/pack/GBR/manifest.json`; `docs/model-v3/inputs.md` (row format, the judgement flag, the register-total text); `pipeline/build_inputs.py`; `tests/model_v3/test_pack.py`; `docs/agents/code.md`.

## Goal
Put the scenario ranges the household step needs into the register as labelled judgement rows, and put the cell inputs (cell weights, composition by band) into the pack, so a later brief can wire `household_step` to real inputs. No model wiring, no run.

## Decisions (author, 2026-11-21)
- **Return ranges for the three classes with no held return** (pension, net financial, physical): a scenario range, never a central value. Pension and net financial take the JST market-portfolio real total return across the two held regimes: low = the 1947 to 1979 mean, high = the 1980 to 2019 mean (about 3.4% and 7.0%; compute them from `returns_decomposition.csv` and state the exact values and years); the 1896 to 2019 mean (4.74, I-D1a) is shown as a reference in the text, not as the central. Physical wealth is held at 0% real return (low, central and high all 0), labelled an assumption: no series is held.
- **Pension accrual** is one labelled aggregate scenario on the ONS basis: range = the 1998 to 2025 min and max of D.8 over opening net worth (0.4% to 1.8%, median 1.2% as reference; recompute from the 101r derivation). No rate on the WAS SCAPE stock.
- Convention A, settlement by the existing routes, and the other 104r rulings stand (`docs/decisions.md`).

## Design
1. **Register rows** (follow the numbering and column conventions of `inputs.md`; name the ids you choose): three real-return ranges (pension, net financial, physical), one pension accrual range. Each is a judgement row, "scenario, not an estimate", with the regime years and source files in the caveat and the central cell equal to the stated reference or marked as a mid-point label, not as an estimate; follow the register's own rule for rows that have no central (report what the format requires and say so). Update the register-total and judgement-count text, `registry/inputs.json` and the row-count pin in `tests/data/test_build_inputs.py`.
2. **Pack additions** (a new version of the pack with a manifest bump; the legacy digests must not move): `cell_weights` (five bands by two stages, from `cell_weights.csv`; stage is the person-based proxy, say so in the basis column) and `band_composition` (property, net financial, physical, pension, debt shares by pack band, from the 102r file). Build them in `build_gbr.py` (not by hand), keep its rules (rounded to printed precision, byte-identical re-run, a value no sheet gives is left out).
3. Extend `test_pack.py` for the new files (schema, key uniqueness, the band shares sum to 100 within rounding, the weights sum to the 102r total of 50.20m persons within the stated rounding).
4. State which `levers.json` mappings, if any, the new rows need (do not add a mapping for I-D14c).

## Touches
`docs/model-v3/inputs.md`, `registry/inputs.json` (generated), `tests/data/test_build_inputs.py` (row-count pin), `model_v3/pack/build_gbr.py`, `model_v3/pack/GBR/` (new files, manifest, NOTICE), `tests/model_v3/test_pack.py`. Name any further file before editing it (`levers.json`, `judgement-decisions.md`, docs that list the register size).

## Acceptance criteria
- Four new rows with exact regime values and years computed from the held files; no central presented as an estimate.
- The pack builds byte-identically on a second run; new files tested; every existing digest and pin unchanged (report any that move and stop).
- Registry regenerated; suites run in the background (never piped); the pre-existing failures (five in `data`, one in `hooks`, same on main) reported as such.
- Diff limited to Touches.

## Checks to run
`python -I pipeline/build_inputs.py`; `python3 -B -I model_v3/pack/build_gbr.py` twice and compare; v3, data and hooks suites in the background; `python -I pipeline/check_agent_docs.py`.

## Out of scope
Wiring into the kernel or runner, the public ledger, settlement, income and consumption allocation by cell (still unset), the lien, any paper text.

## Open questions
How the register represents a row with no central estimate (agent reports what `inputs.md` requires).

## Implementation notes
<!-- progress:start -->
- **Done:**
- **Next:**
- **Decisions:**
- **Gotchas:**
- **Resume:** (exact branch name and fetch line, last block pushed, first action)
- **Not run:**
- **State:** ready; not started
<!-- progress:end -->
