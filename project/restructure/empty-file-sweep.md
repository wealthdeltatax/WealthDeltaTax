# Empty and stub file sweep (brief 173c, stage B)

Swept 1,165 tracked files on `origin/main` (2026-11-26). Nothing removed: no file is demonstrably dead (each is referenced by code, a test, the layout map or a note).

## Files under 200 bytes, and header-only or placeholder files

| File | Bytes | Decision | Why |
|---|---|---|---|
| `model/model_v3/__init__.py`, `core/`, `out/`, `pack/`, `runner/` `__init__.py` | 0 | keep | the five package files; excluded by the brief |
| `.gitattributes`, `CNAME`, `robots.txt` | 43, 18, 72 | keep | excluded by the brief; each does its job |
| `website/site/includes/*` (7 files) | 39 to 181 | keep | excluded by the brief |
| `tests/*/fixtures/*` (7 files) | 43 to 163 | keep | excluded by the brief |
| `website/build/pages/__init__.py` | 51 | keep | a comment-only package marker; `project/decisions.md` and the tripwire name it |
| `website/site/pages/BingSiteAuth.xml` | 85 | keep | the Bing site verification file; the site architecture note names it |
| `data/country-packs/GBR/tax_rules.csv` | 51 | keep, **data request** | header only, no rows; read by `test_pack.py` and the pack manifest (066c). Empty by design today; the author should confirm whether rows are owed |
| `data/country-packs/GBR/public_expenditure.csv` | 68 | keep, **data request** | one row (`total`, 2019, 36.82 % GDP, no GBP figure); read by `build_gbr.py`. A stub by content; the author should confirm it is complete |
| `research/tables/102r-parameter-map-stocks-and-cells/debt_gb_totals.csv` | 93 | keep | two rows, a real small table read by two research scripts |
| `results/057c-evidence/scripts/final1.txt` | 90 | keep | one measured wall time, cited in the evidence README |
| `results/death-phases/f1_phases_{6,15,30}/*-f1-safe-failed.csv`, `results/f1-household/f1_market_failed.csv`, `results/household-arm-run/**/lien_alarms_*.csv`, `floor-restart-lien-alarms.csv` | 51 to 191 | keep | real result files: the cells whose alarm fired; short because few cells failed; listed in the layout map and cited by the notes |
| `results/death-phases/checks_f1.md` | 270 | keep | a two-line check result |

No tracked file is whitespace only, and no tracked text file over 200 bytes is a bare heading or a `TODO`, `tbd` or `placeholder`.

## `papers/legacy/*.md`

33 files; every one has body text (the smallest has well over 300 words besides headings). None reported.

## Not tracked

Empty directories in the author's own working folder (leftovers from the moves) are not in git; `git clean -fdn` previews them. A fresh checkout has none.
