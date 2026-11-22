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
- **Done:** blocks 0 to 3. `decile_composition` (40 rows, ten deciles by four classes, two decimals as held, negatives included, D10's `basis` states the tail assumption) built by `build_gbr.py` from the held `docs/model-v3/kernel-wiring/decile_composition.csv`, in `GBR/` with manifest entry, NOTICE paragraph and `pack_version` 3; two builds byte-identical. Loader: schema, `_x_composition(by='decile')`, `pct_of_decile` exempt from the 0 to 100 rule. ZZZ fixture: 12 rows. Tests: two ZZZ error rows, one UK test (40 rows, each decile sums to 100 within 0.05, D1 as published, tail label, band reproduction). Pins updated: `PINNED` (ZZZ hash), `GBR_SHA`, `p.version == 3`; nothing else.
- **Next:** W4 (pension in the book) and W5 read this table.
- **Decisions:** the held CSV is the source (as 109c); unit `pct_of_decile`; the tail assumption is in the D10 rows' `basis`, no D10b rows; band reproduction is weighted by the decile's net wealth (`wealth_distribution` `wealth_total`), the max difference is 0.048 pp, under 0.06.
- **Gotchas:** persons or households as weights (the brief's wording) cannot reproduce the band rows: the band share is value-weighted (the sum of the decile rows of Table 2.2 over the band total), households per decile are equal by construction. The repo was shallow; `git fetch --unshallow` before the build.
- **Resume:** none; merged.
- **Not run:** nothing.
- **State:** done; merged

Change report
- Task: brief 115c (W3), decile class composition in the pack
- Files changed: `model_v3/pack/build_gbr.py` (dataset, source, manifest, NOTICE; 219 to 232 lines, outside the 200 budget test); `model_v3/pack/GBR/decile_composition.csv` (new), `manifest.json`, `NOTICE.md`; `model_v3/core/pack.py` (schema, cross-check, the percent rule); `tests/model_v3/test_pack.py`; `tests/model_v3/fixtures/pack_ZZZ/` (`decile_composition.csv`, manifest); `docs/model-v3/architecture.md` (budget rows); this brief
- What is different now: the pack carries the class mix of each wealth decile (pack_version 3). Nothing reads it yet; no result moved (`test_legacy_digest` passes unchanged: the digest does not hash the manifest or the pack hash).
- New or changed interfaces: dataset `decile_composition` (`decile band class value unit basis year`); `pk.SCHEMA` has it; `pct_of_decile` values may be negative.
- Acceptance criteria: ten decile rows by four classes, byte-identical on a second build, as held, tail labelled: met. Decile rows reproduce the band rows to 0.06 pp: met (0.048 at most, net-wealth weights); classes sum to 100 per decile within rounding: met (at most 0.01 off). `test_legacy_digest` unchanged: met. Existing suites: model_v3 261 passed; data (5), cards (1), hooks (1) fail as on main. Diff limited to Touches: met.
- Deviations from the brief: (1) the reproduction is weighted by decile net wealth, not persons or households (the only weights that reproduce it, see Gotchas); (2) the pack loader needed the dataset in block 1 to load the pack at all, so schema and cross-check landed in block 1; (3) budgets raised: `core/pack.py` 355 to 360 (357 lines), `test_pack.py` 265 to 280 (274 lines), totals updated.
- Risks / follow-ups: `build_gbr.py` is 232 lines against the 200 of 067c (no test enforces it); W5 must give a negative net financial or property balance 0% real (author's decision, not in this brief).
- Instruction friction: none
- Verification: `build_gbr.py` twice, `diff -r` of `GBR/` and `cmp` of `levers.json` identical; `test_legacy_digest`; `python pipeline/run_suites.py` (7 of 10, failures as on main); `python -I pipeline/check_agent_docs.py` exit 0.
- Overview sections likely needing an update: none
- Commit / branch: `brief/115-decile-composition`; brief 115 merged, ready to retire
<!-- progress:end -->
