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

- **No central estimate (author, 2026-11-21):** where the register format needs a central cell, it holds a labelled mid-point reference (state it as such in the caveat and the row's first sentence), never an estimate; the whole-sample 4.74 is a reference, not the central, for pension and net financial. Say in the change report which cells are mid-point labels.

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
Whether `build_inputs.py` or the register tests object to a mid-point label in a central cell (agent reports; do not change the parser without asking).

## Implementation notes
<!-- progress:start -->
- **Done:** four register rows I-D1h to I-D1k; registry regenerated (297 rows); pack version 2 with cell_weights and band_composition built by build_gbr.py (byte-identical second run); loader, ZZZ fixture and tests extended; v3 243 passed; check_agent_docs exit 0.
- **Next:** the wiring brief that reads these rows and files; the author may replace the mid-point labels with chosen values.
- **Decisions:** author answered "Extend loader, update pins" (core/pack.py and the ZZZ fixture are outside Touches); ids I-D1h to I-D1k (D1 is the returns block); `registry/inputs-display.yml` gets four entries because the hooks test needs one per register row (precedent: 091g, 072g).
- **Gotchas:** the clone was shallow, so `retrieved` dates came out wrong until `git fetch --unshallow`; with a full clone the existing files' dates are unchanged.
- **Resume:** none.
- **Not run:** none.
- **State:** done; merged
<!-- progress:end -->

### Change report
```
Change report
- Task: brief 109c, scenario return ranges, pension accrual range and cell inputs
- Files changed: docs/model-v3/inputs.md (rows I-D1h to I-D1k, counts, 2026-11-21 bullet); registry/inputs.json (generated); registry/inputs-display.yml (four entries, named: hooks test needs one per row); tests/data/test_build_inputs.py (pin 293 to 297); model_v3/pack/build_gbr.py (cells(), schema, version 2, notice); model_v3/pack/GBR/ (cell_weights.csv, band_composition.csv, manifest, NOTICE); model_v3/core/pack.py (two datasets and one cross-check, named: the loader rejects unknown datasets); tests/model_v3/fixtures/pack_ZZZ/ (two files, manifest, named); tests/model_v3/test_pack.py (pins, 6 tests); docs/model-v3/architecture.md (pack budget 340/240 to 355/265, totals, 2.1 note)
- What is different now: the register holds the scenario ranges the household step needs; the pack carries persons by band and stage and the composition by band; nothing reads them yet.
- New or changed interfaces: pack datasets cell_weights (band, stage, persons, max_rounding, basis) and band_composition (band, class, value, unit, basis, year); pack_version 2.
- Acceptance criteria: four rows with exact values: I-D1h pension and I-D1i net financial real return 3.44 / 5.20 / 6.96 (1947-1979 mean 3.4396 over 33 years; 1980-2019 mean 6.9639 over 40; 1896-2019 4.7423 as reference text), I-D1j physical 0 / 0 / 0 (assumption), I-D1k pension accrual 0.41 / 1.12 / 1.84 % of opening net worth (1998-2025 min 0.4095 in 2020, max 1.8356 in 1998, median 1.18) (met); mid-point labels in the central cells of I-D1h, I-D1i and I-D1k (mid-point of low and high; I-D1j is 0 in all three as an assumption); pack byte-identical on a second run (met, diff -r); every existing digest unchanged except the two pack hashes that must move when files are added: GBR_SHA a9d8312678... to 19f3ebcc82... and the ZZZ fixture pin 339cb474... to 291b63c2... (reported; the author's answer covered this); registry regenerated, v3 243 passed, data 5 failed and hooks 1 failed, the pre-existing ones (same as main); diff limited to Touches plus the named files above (partly met: core/pack.py, the ZZZ fixture and inputs-display.yml are outside Touches, covered by the author's answer or named)
- Deviations from the brief: band_composition has no debt row: the 102r file gives property and net financial net of debt, and no sheet gives debt by band, so it is left out; stage is a person-based proxy and says so in the basis column; the tax_rules manifest date moved to the build date 2026-11-21 (no source file); build_gbr.py is now over its 200-line budget (it was 201, no test counts it)
- Risks / follow-ups: build_inputs and the register tests accept a mid-point central without change (no parser edit); levers.json needs no mapping (no pack pointer for the new rows, they are read by id from the register); STATUS.md and country-pack.md still quote older row counts (guru-owned); build_gbr.py needs a full clone (this one was shallow)
- Instruction friction: none
- Verification: python -I pipeline/build_inputs.py (297 inputs); build_gbr.py twice, diff -r identical; pytest tests/model_v3: 243 passed; run_suites data hooks: 5 and 1 failures, all pre-existing; python -I pipeline/check_agent_docs.py: exit 0
- Overview sections likely needing an update: register size (297 rows, 112 judgement rows); pack contents and version
- Commit / branch: brief/109-scenario-cell-pack, merged to main
```
