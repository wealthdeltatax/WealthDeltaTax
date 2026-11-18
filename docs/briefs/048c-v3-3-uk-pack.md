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
- **Done:**
- **Next:**
- **Decisions:**
- **Gotchas:**
- **Resume:**
- **Not run:**
- **State:** draft; not started
<!-- progress:end -->
