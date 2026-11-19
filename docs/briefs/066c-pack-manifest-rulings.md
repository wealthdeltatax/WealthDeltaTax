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
- **Done:**
- **Next:**
- **Decisions:**
- **Gotchas:**
- **Resume:**
- **Not run:**
- **State:** ready; not started
<!-- progress:end -->
