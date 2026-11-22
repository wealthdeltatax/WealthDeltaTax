# 115 (W3): Decile class composition in the pack

- **Status:** ready
- **Author/date:** K. Ogata with the guru, 2026-11-22
- **Depends on:** 114c (merged), 109c (pack v2)
- **Read (block 0: the first two only):** (1) `docs/model-v3/kernel-wiring-design.md` section 2.2 and the W3 row of section 4; (2) `docs/agents/code.md`. Later, by block: `docs/model-v3/kernel-wiring/decile_composition.py` and `.csv` (the derivation and its output); `model_v3/pack/build_gbr.py` (the `cells()` function from 109c is the model to follow); `model_v3/core/pack.py` (loader and cross-checks); `tests/model_v3/test_pack.py` and `tests/model_v3/fixtures/pack_ZZZ/`; `model_v3/pack/GBR/band_composition.csv`.

## Goal
Put the ten decile class mixes into the pack as a new dataset, built by `build_gbr.py` from the held table, so the household hook (W5) can give each payer line a class mix. Nothing reads it yet. No model result may move.

## Decisions (author, 2026-11-22)
- Confirm the mix as held: Table 2.2 decile shares of net wealth by class (property, net financial, physical, pension), net of debt, **negative shares included** (D1: property -4.72, net financial -104.92, physical 169.46, pension 40.18).
- D10b and the Rich List tiers take the D10 mix, labelled an assumption in the `basis` column (the survey misses business wealth).
- For W5, recorded now: a negative net financial or property balance earns 0% real, a labelled assumption; the debt-rate range stays unset. Not part of this brief.

## Blocks (one push each; `docs/agents/code.md`, Long builds)
- **Block 0:** progress block pushed.
- **Block 1: the dataset.** `decile_composition` in `build_gbr.py` (columns: decile, band, class, value, unit, basis, year; the value as printed, two decimals, the held rounding), `GBR/decile_composition.csv`, manifest entry and NOTICE line, pack version 3, and a byte-identical second run. Before pushing, run `tests/model_v3/test_legacy_digest.py`: if the digest moves only because the pack manifest or hash is part of what it hashes, stop and report exactly what moved (a recapture needs the author's word); if it does not move, continue. Push.
- **Block 2: loader and tests.** `core/pack.py` accepts the dataset (and the cross-check below); the `pack_ZZZ` fixture gets matching rows; `test_pack.py`: schema and key uniqueness, each decile's classes sum to 100 within rounding, the persons-weighted (or household-weighted: use the same weights as `cell_weights`, say which) mean of the decile rows reproduces the `band_composition` row for each band to 0.06 percentage points, D1 as published. Update pins that the new file legitimately moves (the pack hash and the ZZZ pin) and nothing else; list each. Push.
- **Block 3: report.** Budget rows if the files grew; change report; push; stop.
**Stop rule.** After three blocks, or a quarter of the budget left, push what exists and write Next.

## Touches
`model_v3/pack/build_gbr.py`, `model_v3/pack/GBR/` (new dataset, manifest, NOTICE), `model_v3/core/pack.py`, `tests/model_v3/test_pack.py`, `tests/model_v3/fixtures/pack_ZZZ/`, `docs/model-v3/architecture.md` (budget rows only). Name any further file before editing it. Not the register, the kernel, the runner, `household.py` or the digest fixture.

## Acceptance criteria
- Ten decile rows by four classes in the pack, byte-identical on a second build, as held, with the tail assumption labelled.
- The decile rows reproduce the band rows to 0.06 pp; classes sum to 100 per decile within rounding.
- `test_legacy_digest` passes unchanged, or the brief stops and reports what moved; every existing suite passes (pre-existing data, cards and hooks failures reported as on main).
- Diff limited to Touches.

## Checks to run
`python3 -B -I model_v3/pack/build_gbr.py` twice and compare (needs a full clone: `git fetch --unshallow` if shallow); `test_legacy_digest`; v3 suites in the background (never piped); `python -I pipeline/check_agent_docs.py`.

## Out of scope
The household hook, class returns, debt treatment, anything in the kernel or runner (W4 onward), any register edit.

## Open questions
Whether the digest hashes the pack manifest (agent reports).

## Implementation notes
<!-- progress:start -->
- **Done:** block 0; block 1: `decile_composition` in `build_gbr.py` (40 rows: decile, band, class, value, unit `pct_of_decile`, basis, year; read from the held `docs/model-v3/kernel-wiring/decile_composition.csv`, values to two decimals; the D10 rows' basis states the tail assumption), `GBR/decile_composition.csv`, manifest entry, NOTICE paragraph, `pack_version` 3; two builds byte-identical (GBR folder and `levers.json`). The loader accepts the dataset (needed to load the pack: schema, `_x_composition(by='decile')`, `pct_of_decile` exempt from the 0 to 100 rule because D1's shares are negative); `core/pack.py` budget 355 to 360 (357 lines). `test_legacy_digest` passes unchanged: the digest does not hash the manifest or the pack hash.
- **Next:** block 2: `pack_ZZZ` rows; `test_pack.py` tests; update the three pins the new file moves (`test_p1_fixture_loads_every_dataset`, `test_p7_the_uk_pack_hash_is_pinned`, `test_the_uk_pack_carries_the_cell_inputs_and_they_close`).
- **Decisions:** the held file is the source (as 109c); two-decimal strings; `pct_of_decile` unit.
- **Gotchas:** the repo was shallow; `git fetch --unshallow` before the build. The band shares are value-weighted sums of Table 2.2 decile rows, so the reproduction test must weight by decile net wealth, not persons or households (to be confirmed by the test).
- **Resume:** branch `brief/115-decile-composition`; `git fetch origin && git checkout brief/115-decile-composition`; first action: edit `tests/model_v3/fixtures/pack_ZZZ` and `test_pack.py`.
- **Not run:** the three pack tests fail on this branch until block 2 (pins).
- **State:** in progress, block 1 done
<!-- progress:end -->
