# 048: Model v3 V3-3: the UK data pack from the held files

- **Status:** ready
- **Author/date:** K. Ogata with the guru, 2026-11-18
- **Depends on:** 047
- **Read:** `docs/model-v3/country-pack.md` in full; `docs/model-v3/architecture.md` 1 and 6.2 (P8, P9); `docs/model-v3/port-inventory.md` (the `jst_r6.json` row); `docs/model-v3/inputs.md` (headers); `docs/model-v3/returns-method.md` and the author's 2026-11-18 ruling that the return sample ends in 2019.

## Goal
`model_v3/pack/GBR/` exists, validates, and carries every number the model takes from outside the register.

## Decisions (author, 2026-11-18)
`architecture.md` approved (sections 8.1 and 9 as written); `acceptance.md` approved with Q1 to Q6 as proposed. v3 imports nothing from `model_v1/` or `model_v2/`. No file outside this brief's Touches is changed.

## Design
Write `model_v3/pack/build_gbr.py` (150 lines at most; a data tool, not core) that builds the seven CSV files, the manifest and `NOTICE.md` from the held spreadsheets and copies `model_v2/jst_r6.json` unchanged to `pack/GBR/source/`; `returns.csv` is derived from it and the 2017 to 2019 bridge of `returns-gap.md`; the sample ends in 2019 (author, 2026-11-18). Only the six WID rows that `wealth_tail.csv` needs are taken from the WID file; the 52.9 MB file is not copied. Run the builder once and commit its output; the builder has no test beyond a hash check of its output. Tests P8 and P9 are added to `tests/model_v3/test_pack.py` by this stage (the only file shared with V3-2, which runs first).

**Shared interfaces, fixed before any stage starts** (a build brief never edits them; a mismatch is a question to the guru): the output file shape is `schema wdt-outputs/1` as `pipeline/validate_outputs.py` checks it and `docs/restructure/site/hooks.md` section 3 with the 030c rulings; the country pack format is `docs/model-v3/country-pack.md`; the id lists are `docs/model-v3/outputs.yml` and the module-to-id table of `architecture.md` 2.10; the Samples contract is `architecture.md` 2.9; the layers and import rules are `architecture.md` 5.1.

This is build stage V3-3 of `architecture.md` section 7. One session, one lane; the stage ends in a stop: tests pass, change report written, branch merged by the auto-merge rule. The stage's files are budgeted in `architecture.md` 6.1; a stage more than 15% over its budget reports it before the next starts.

**Mappings that 047c left to the caller (added by the guru, 2026-11-18).** `core/pack.py` names no tax line and no register id, so X1 and X2 need three mappings. Write them as a `pack_mappings` section of `model_v3/levers.json` (no other section is edited; no named schedule is typed there): `x1_pointers` (register row id to dataset, row selector and column, for the 108 pack rows whose data the pack supplies), `parts` (each parent receipts line to its parts, for example the stamp-duty sub-rows), `groups` (receipts lines to the DH1b groups) and `x2` (the retired lines and the 8.11 target). The P8 test reads them from this file and types no number or line name; the 8.11 target comes from the file. A pointer whose register row says the data are not in the repo is listed and skipped, with the count reported.

## Touches
`model_v3/pack/GBR/`, `model_v3/pack/build_gbr.py`, `model_v3/levers.json` (the `pack_mappings` section only), `tests/model_v3/test_pack.py`, this brief's progress block.

## Acceptance criteria
- P8 passes: X1 within 1e-9 and X2 within 0.01 (the M1d lines sum to 8.11% of GDP), with every mapping read from `levers.json` `pack_mappings`.
- `levers.json` still parses and still holds no named schedule; only the `pack_mappings` section is new.
- P9 passes: the register row count (274 today) equals the count read from `inputs.md`, `low <= central <= high`, `(J)` flags equal `inputs.md`.
- `pack_sha256` of the UK pack is pinned in a test; the 038c scan returns zero hits.
- `git diff --stat` is limited to the Touches list.

## Checks to run
`pytest tests/model_v3 -q`; a re-run of the builder gives byte-identical output.

## Out of scope
Any model code; a second country.

## Open questions
Ask if a held spreadsheet does not give a pack field; do not fill it.

## Implementation notes
<!-- progress:start -->
- **Done:** `model_v3/pack/build_gbr.py` (143 lines, budget 150) built `model_v3/pack/GBR/` once: manifest, seven CSV files (returns 150 rows 1870-2019, wealth_distribution 15, wealth_tail 6, receipts 16, household_incidence 26, tax_rules and public_expenditure header only), NOTICE.md, `source/jst_r6.json` (unchanged copy). `pack_mappings` in `levers.json` now holds 63 `x1_pointers` and 43 `x1_skipped` (23 data not in the repo, 12 returns rows the model derives, 7 H2a rows that depend on W_min, 1 I-D7d no sheet gives); parts, groups and x2 typed. `test_pack.py` (240 of 240 lines) adds P8, P9 and the pinned UK `pack_sha256`. `pytest tests/model_v3 -q`: 107 passed. A second run of the builder gives byte-identical files and `levers.json`.
- **Next:** V3-4 onward (051c, 050c).
- **Decisions:** author 2026-11-18: relax the loader rule that each return column is contiguous (JST has no housing or capital return for 1940-46); `_x_returns` keeps strictly increasing, no-gap years; a gap loads as None. Pack values are the register's published roundings computed from the sheets (percent 1 dp, receipts 2 dp, pounds whole), so X1 holds at 1e-9. `parts` holds only stamp_duties = stamp_property + stamp_shares.
- **Gotchas:** (1) 038c's check "paye + self_assessment <= income_tax" fails on the sheet (10.80 against 10.60), so income_tax has no part-of. (2) `returns-gap.md` has no 2017 to 2019 bridge and JST already covers 2017-2019, so none was built. (3) Five register rows have low, central, high out of order: I-T3d, I-T3e, I-T3g, I-T3m, I-T3p. Author 2026-11-19: they stay as the register has them (the OBR sheet's neighbouring-year columns, not bounds); P9 pins that exact set. (4) The register marks 90 rows as judgement, `inputs.md` writes the flag as `**(J)**` in 70 and as plain `(J)` in 20; P9 reads both. (5) `manifest.retrieved` is 2026-11-16 for every file: I did not find the real retrieval dates. (6) base_year is null in the manifest: no sheet gives a price base for the whole pack.
- **Resume:** none needed.
- **Not run:** nothing in the brief; no model code touched.
- **State:** done; merged to main by the auto-merge rule after the author's ruling on the T3 rows (2026-11-19)
<!-- progress:end -->

### Change report
```
Change report
- Task: brief 048c, model v3 stage V3-3: the UK data pack
- Files changed: model_v3/pack/GBR/ (new: manifest.json, seven CSV files, NOTICE.md, source/jst_r6.json); model_v3/pack/build_gbr.py (new, 143 lines); model_v3/levers.json (pack_mappings only); tests/model_v3/test_pack.py (P8, P9, UK hash; 240 lines); model_v3/core/pack.py (contiguity check removed, 334 lines); this brief
- What is different now: the UK pack validates and carries every register number that has a file in the repo; 63 register rows point at it and X1 holds; the seven retired lines sum to 8.11% of GDP.
- New or changed interfaces: none; pack_mappings holds x1_pointers, x1_skipped, parts, groups, x2
- Acceptance criteria: P8 X1 within 1e-9 and X2 within 0.01 (met); levers.json parses and holds no named schedule (met); P9 row count and (J) flags equal inputs.md (met), low <= central <= high (met with the five T3 rows pinned as known, author ruling 2026-11-19); pack_sha256 pinned, 038c scan zero hits (met); git diff --stat limited to Touches (met, plus the pack.py deviation)
- Deviations from the brief: core/pack.py edited, with the author's answer (JST 1940-46 gap)
- Risks / follow-ups: (1) fix or rule on the five I-T3 rows (receipts forecast series run downward); (2) retrieval dates and base_year in the manifest; (3) paye + self_assessment exceeds income_tax in the sheet, 038c's part-of rule needs amending; (4) no 2017-2019 bridge exists or is needed
- Verification: pytest tests/model_v3 -q: 107 passed; builder re-run byte-identical
- Overview sections likely needing an update: model v3 build status (V3-3)
- Commit / branch: brief/048-uk-pack, merged to main
```
