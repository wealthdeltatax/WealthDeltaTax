# 066: Apply two manifest rulings that 048c missed

- **Status:** ready
- **Author/date:** K. Ogata with the guru, 2026-11-19
- **Depends on:** none (048c is merged)
- **Read:** the archived `docs/archive/briefs/048c-v3-3-uk-pack.md` (Guru rulings 2026-11-19); `model_v3/pack/build_gbr.py`; `model_v3/pack/GBR/manifest.json`, `NOTICE.md`; `docs/model-v3/country-pack.md` (manifest fields); `tests/model_v3/test_pack.py` (the pinned `pack_sha256`).

## Goal
The UK pack's manifest says what the 048c rulings said: the price base is 2025-26 and each file's `retrieved` date is the date the source file entered the repository. 048c merged with `base_year: null` and `retrieved` 2026-11-16 for every file.

## Decisions (author and guru, 2026-11-19)
- `base_year` is `"2025-26"` (stage C1: one fixed price base, 2025-26 prices); the manifest `notes` say that pack values are as published and the model expresses them in 2025-26 prices.
- `retrieved` per file is the date that file was added to the repository: `git log --diff-filter=A --format=%as -1 -- <source path>`, the oldest if several sources feed one file; `NOTICE.md` says so. No guess.
- Nothing else in the pack changes.

## Design
Edit `build_gbr.py` (it writes the manifest and NOTICE; keep it at 150 lines or fewer, say so if it grows), rebuild once with `python model_v3/pack/build_gbr.py`, confirm a second run is byte-identical, update the pinned `pack_sha256` in `test_pack.py`. Only `manifest.json` and `NOTICE.md` change among the pack files (check with `git diff --stat`); if any CSV changes, stop and report.

## Touches
`model_v3/pack/build_gbr.py`, `model_v3/pack/GBR/manifest.json`, `model_v3/pack/GBR/NOTICE.md`, `tests/model_v3/test_pack.py` (the pin only), this brief's progress block.

## Acceptance criteria
- `manifest.json` has `base_year: "2025-26"` and a real `retrieved` date for every file; no 2026-11-16 left unless that is the true date.
- `pytest tests/model_v3 -q` passes (116); a second builder run is byte-identical.
- `git diff --stat` is limited to the Touches list and the CSV files are unchanged.

## Checks to run
`pytest tests/model_v3 -q`, `pytest tests/data -q`, `pytest tests/gate -q` (separate commands).

## Out of scope
The CSV contents, `levers.json`, the loader, anything in `core/`.

## Open questions
None.

## Implementation notes
<!-- progress:start -->
- **Done:** `base_year` is `"2025-26"`; manifest `notes` added; `retrieved` per file is the day its source file entered the repository (builder runs `git log --follow --diff-filter=A`, oldest): returns 2026-09-30 (jst_r6.json, followed through the rename from `model/`), wealth_distribution and receipts and wealth_tail 2026-11-15, household_incidence 2026-11-17. `NOTICE.md` says so. New `pack_sha256` pinned: f6f66aaf...5866.
- **Next:** none.
- **Decisions:** `--follow` is used (the brief's command has none): without it `jst_r6.json` reads 2026-11-15, the day of the folder rename, not the day it was added. `tax_rules.csv` and `public_expenditure.csv` have no source file, so they carry the build date 2026-11-18 and NOTICE says so; if the author wants another rule for them, say so. The loader accepts the string base_year and the extra `notes` key without a change; `notes` is not hashed, `base_year` is.
- **Gotchas:** the clone was shallow; I ran `git fetch --unshallow` (needed for the dates). The builder now needs git history to run.
- **Resume:** `python model_v3/pack/build_gbr.py`, `pytest tests/model_v3 -q`.
- **Not run:** none.
- **State:** done

```
Change report
- Task: 066c, manifest rulings of 048c (base_year and retrieved)
- Files changed: model_v3/pack/build_gbr.py; model_v3/pack/GBR/manifest.json; model_v3/pack/GBR/NOTICE.md; tests/model_v3/test_pack.py (the pin); this brief
- What is different now: the UK pack manifest states the 2025-26 price base and true source dates
- New or changed interfaces: none (pack_sha256 changed because base_year is hashed)
- Acceptance criteria: manifest has base_year and real retrieved dates, 2026-11-16 gone (met); pytest tests/model_v3 116 passed, second builder run byte-identical incl. levers.json (met); diff limited to Touches, CSV files unchanged (met)
- Deviations from the brief: --follow added; build_gbr.py is 159 lines, 6% over its 150 budget; two files carry the build date
- Risks / follow-ups: the builder depends on full git history
- Verification: pytest model_v3, data, gate separately (116, 84, 17); builder run twice and diffed
- Overview sections likely needing an update: none
- Commit / branch: brief/066-pack-manifest-rulings
```
<!-- progress:end -->
