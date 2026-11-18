# 047: Model v3 V3-2: country pack and register loader

- **Status:** ready
- **Author/date:** K. Ogata with the guru, 2026-11-18
- **Depends on:** 046 (the tests scaffold)
- **Read:** `docs/model-v3/architecture.md` 2.1 and 6.2 (`pack` tests P1 to P7, P10); `docs/model-v3/country-pack.md` in full; `registry/inputs.json` and `docs/model-v3/inputs.md` (headers only); `docs/model-v3/acceptance.md` V3-2 row.

## Goal
`core/pack.py` reads and validates any country pack and the register, so the UK data and a test pack load through the same code.

## Decisions (author, 2026-11-18)
`architecture.md` approved (sections 8.1 and 9 as written); `acceptance.md` approved with Q1 to Q6 as proposed. v3 imports nothing from `model_v1/` or `model_v2/`. No file outside this brief's Touches is changed.

## Design
Implement `core/pack.py` (340 lines) as `architecture.md` 2.1 says: manifest first, folder name equals `country`, per-file sha256, header equals schema, first violation raises with file, row and column, no fill or interpolation or clipping; `pack_sha256`; the register as low, central and high per id with `(J)` flags and unit; the consistency checks X1 and X2 (they run only when the UK pack is present, so this stage tests them on the fixture only); accessors; the data facts DH1a and DH1b. Build the ZZZ fixture pack under `tests/model_v3/fixtures/pack_ZZZ/` (small, invented numbers, flagged in its NOTICE).

**Shared interfaces, fixed before any stage starts** (a build brief never edits them; a mismatch is a question to the guru): the output file shape is `schema wdt-outputs/1` as `pipeline/validate_outputs.py` checks it and `docs/restructure/site/hooks.md` section 3 with the 030c rulings; the country pack format is `docs/model-v3/country-pack.md`; the id lists are `docs/model-v3/outputs.yml` and the module-to-id table of `architecture.md` 2.10; the Samples contract is `architecture.md` 2.9; the layers and import rules are `architecture.md` 5.1.

This is build stage V3-2 of `architecture.md` section 7. One session, one lane; the stage ends in a stop: tests pass, change report written, branch merged by the auto-merge rule. The stage's files are budgeted in `architecture.md` 6.1; a stage more than 15% over its budget reports it before the next starts.

## Touches
`model_v3/core/pack.py`, `tests/model_v3/test_pack.py`, `tests/model_v3/fixtures/pack_ZZZ/`, this brief's progress block.

## Acceptance criteria
- P1 to P7 and P10 pass; the ZZZ pack loads with no code change (R11).
- A changed byte in a fixture file fails on the sha256 and names file, row and column.
- `core/pack.py` is at most 340 lines (`test_budget.py`) and imports only numpy and the standard library.
- `git diff --stat` is limited to the Touches list.

## Checks to run
`pytest tests/model_v3 -q`.

## Out of scope
The UK pack (V3-3); P8 and P9 (V3-3, they need it).

## Open questions
Ask where the country pack format is ambiguous; do not extend the format.

## Implementation notes
<!-- progress:start -->
- **Done:** `model_v3/core/pack.py` (339 lines, budget 340; numpy and stdlib only), `tests/model_v3/test_pack.py` (231, budget 240), the ZZZ fixture `tests/model_v3/fixtures/pack_ZZZ/` (manifest, seven CSV files, NOTICE; invented numbers). P1 to P7 and P10 pass, plus 30 further checks (every schema rule, manifest rules, register loader, X1, X2, DH1a, DH1b, imports). `pytest tests/model_v3 -q`: 63 passed (rules and budget tests included). The fixture pack hash is pinned in P7.
- **Next:** V3-3 (UK pack from the held files), which needs the pointer map for X1 and the part-of and group mappings for `levers.json` (V3-0).
- **Decisions:** author's answer 2026-11-18: the caller passes the part-of relation, so `pack.py` names no tax line. `receipts_sum(pack, lines, parts)`, `check_parts`, `check_x2(pack, lines, target, ...)`, `dh1b(pack, groups)` and `check_x1(pack, register, pointers)` take mappings from the caller; the 8.11 target and the pointers are not in the code. DH1a returns the top-share series of the tail file (latest year as point with low and high, plus history); wealth to GDP stays a register row (I-D4a). DH1b returns pct_gdp by line and by the caller's groups. Band order in tax_rules is checked per (rule, tax_year) across subjects. Percent range uses the unit prefix `pct`. The register loader keeps null low, central or high as None (21 of 274 rows have them) and raises on anything non-numeric or a duplicate id.
- **Gotchas:** (1) The brief's fixture folder is `pack_ZZZ` but 038c requires the folder named by `country`, so tests copy it to `.../ZZZ` before loading (a folder-name test is built in). (2) P2 as worded (a changed byte fails "naming file, row and column") cannot be met for a changed value that stays valid: a hash alone gives no row or column. The loader names the file always, and adds row and column when the changed file also breaks its schema; both cases are tested. A per-row hash in the manifest would fix it but extends the format (guru). (3) `registry/inputs.json` has 274 rows, `inputs.md` and the 038c tally say 269; P9 (V3-3) will meet this. (4) `pack_sha256` text layout (country line, header JSON, file lines) is my reading of 038c section 5 and is written in the module docstring (R6). (5) Vocabulary checks (allowed `line`, `series`, `variable` and `rule` keys) are not in the loader: they are country-specific names, so R11 forbids them in code.
- **Resume:** none needed.
- **Not run:** P8, P9 (V3-3, need the UK pack); X1 and X2 on the UK pack.
- **State:** done; merged to main by the auto-merge rule
<!-- progress:end -->

### Change report
```
Change report
- Task: brief 047c, model v3 stage V3-2: country pack and register loader
- Files changed: model_v3/core/pack.py (new, 339 lines); tests/model_v3/test_pack.py (new, 231); tests/model_v3/fixtures/pack_ZZZ/ (new: manifest.json, seven CSV files, NOTICE.md); this brief's progress block and report
- What is different now: v3 can read, validate and hash any country pack and the register; the invented ZZZ pack loads through the same code a UK pack will.
- New or changed interfaces: PackError, Pack, Row, load_pack, load_register, lookup, series, receipts_sum, check_parts, check_x1, check_x2, dh1a, dh1b in model_v3.core.pack
- Acceptance criteria: P1 to P7 and P10 pass, ZZZ loads with no code change (met); a changed byte fails on sha256 and names the file, with row and column when the file also fails its schema (partly met: see Risks, item 1); pack.py 339 of 340 lines, numpy and stdlib imports only (met, test_budget and an import test); git diff --stat limited to Touches (met)
- Deviations from the brief: tests load the fixture from a copy named ZZZ, because 038c requires folder name equals country.
- Risks / follow-ups: (1) row and column of a valid-looking changed byte cannot be derived from a per-file hash; a per-row hash would need a manifest amendment. (2) the register has 274 rows against 269 in inputs.md (P9). (3) pack.py has one line of budget left. (4) levers.json (V3-0) must carry the part-of, group and X1 pointer mappings.
- Verification: pytest tests/model_v3 -q: 63 passed; rules tests (layering, lazy import, import side effects, orphans, country scan, budget) pass on the tree with pack.py.
- Overview sections likely needing an update: model v3 build status (V3-2 done)
- Commit / branch: brief/047-pack-loader, merged to main
```
