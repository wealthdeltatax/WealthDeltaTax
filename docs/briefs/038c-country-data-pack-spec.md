# 038: Code: country data pack specification (model v3 requirement R11)

- **Status:** ready
- **Author/date:** K. Ogata with the guru, 2026-11-17
- **Depends on:** none (reads `registry/inputs.json` if 030c has landed; otherwise `inputs.md`)
- **Read:** `docs/model-audit/synthesis.md` section 4 (R3, R4, R11) and section 9; `docs/model-v3/inputs.md` (header, families, source and file columns); `docs/model-v3/drivers.md` section 2; `docs/briefs/030c-data-interface.md` (file shapes it creates); `docs/restructure/order.md` G2 (hashes the gate reads); `model_v2/wdt_jst.py` and the head of `jst_r6.json` (the one series file that exists); `docs/agents/code.md`.

## Goal
Specify the country data pack: one folder, one documented format, everything country-specific in it, so the v3 core and output layer contain no UK name, rate or amount and a second country is a test of the format, not a feature.

## Decisions (author, 2026-11-16)
UK data only, through one country pack (R11). v3 ships the UK pack only. v2 ran 14 countries at once and that was a source of bulk. Every ranged input has a low, central and high value, a unit and a source (R3).

## Design
Write `docs/model-v3/country-pack.md`, and a worked UK listing in it, covering:
1. **Boundary.** What lives in the pack and what in the register: series and tables (returns, wealth distribution, baseline tax receipts, expenditure, income and liquid assets by band, currency and base year) in the pack; scalar ranged parameters stay in `inputs.md` and `registry/inputs.json`. For each of the 269 register rows say which side it is on, as a table by family, with the count.
2. **Layout.** Folder name, file names, file formats, required header fields (country code, currency, base year, source, licence, retrieved date, hash), one file per dataset.
3. **Schema.** For each dataset: columns, units, allowed missing values, and the validation rule a loader applies; failing loudly (R5).
4. **The UK pack file list**, each with its current source file in the repo (`jst_r6.json`, the IFS revenue sheet, the wealth survey and the tail source named in the register) and what is missing from the repo.
5. **Hash and provenance.** How the pack is hashed so a run records it next to `run.inputs_sha256` (gate G2); how a pack change invalidates a run.
6. **The test of R11.** A check that finds a UK name, rate or amount in core or output code (a grep rule the gate checker can run), and what a second country would have to supply.
7. **Licences.** The licence of each dataset as far as the register states it; mark unverified ones (JST is unverified).

## Touches
`docs/model-v3/country-pack.md` (new), this brief's progress block. No schema file, loader or data file is created in this brief; nothing in `registry/`, `model_v2/`, `pipeline/`.

## Acceptance criteria
- The 269 register rows are each assigned to pack or register, and the counts sum to 269 (checked by script).
- Every dataset has columns, units, validation rule and source.
- A reader can write the loader from the note alone; the loader is not written here.
- The R11 grep rule is given and run once against `model_v2/`, with the count of hits as an example (not a fix).
- `git diff --stat` shows only the Touches list.

## Checks to run
A script that reads `inputs.md` or `registry/inputs.json` and tallies the assignment; the grep rule against `model_v2/`.

## Out of scope
Writing the loader or any pack file, fetching data, choosing sources (the register has them), a second country.

## Open questions
Whether the wealth distribution is stored as survey microdata or as a binned table (the register's tail source decides); ask rather than guess.

## Implementation notes
<!-- progress:start -->
- **Done:** `docs/model-v3/country-pack.md`: boundary table (108 pack, 161 register, sum 269, by script), layout and manifest header, schema for seven datasets, UK file list with repo sources and gaps, hash and run record, R11 grep rule run once on `model_v2/` (288 hits outside comments), licences.
- **Next:** guru reads the note; `030c` build can read pack rows from it once a pack exists. A later brief writes the loader and the UK pack files.
- **Decisions:** wealth distribution is a binned table plus tail points, no microdata (the register's tail sources publish shares, not unit records). A row is pack only if one cell of a multi-cell dataset and not `(J)`. Pack hash = sha256 over header JSON plus per-file hashes; run records `run.pack_sha256`.
- **Gotchas:** register has 87 `(J)` rows, not the 70 in gate G3; 38 `(J)` rows are pack-shaped and stay in the register. 23 pack rows have no data in the repo.
- **Resume:** tally script is in the appendix of the note; run `python -I tally.py docs/model-v3/inputs.md` after saving it.
- **Not run:** rule A2 (pack-value literals), needs a pack; no loader or pack file exists.
- **State:** done

```
Change report
- Task: 038c, country data pack spec. Design note only.
- Files changed: docs/model-v3/country-pack.md (new); docs/briefs/038c-country-data-pack-spec.md (progress block)
- What is different now: R11 has a written boundary, layout, schema, hash and test for the UK pack
- New or changed interfaces: none yet (proposed: manifest.json header, run.pack_sha256)
- Acceptance criteria:
  - 269 rows assigned, counts sum to 269, checked by script: met (108 + 161)
  - Every dataset has columns, units, validation rule and source: met
  - A reader can write the loader from the note alone: met on the note's own terms; not tested by writing one
  - Grep rule given and run once on model_v2/: met (288 union hits outside comments)
  - git diff --stat only Touches: met
- Deviations from the brief: none
- Risks / follow-ups: flags listed at the end of the note (stale 260 row bullet, G3 says 70 vs 87, G2 needs run.pack_sha256, synthesis wid_long.csv claim, 125 rows "In repo: no", rates_core break wider than its suggestions entry); JST licence unverified
- Verification: tally script asserts and prints the table; table sums re-added by script; grep run once
- Overview sections likely needing an update: model v3 section (add country-pack.md)
- Commit / branch: brief/038-country-data-pack-spec
```
<!-- progress:end -->
