# Brief suggestions

Any agent appends here when it finds a problem that needs its own brief and is outside its current brief. Do not fix it. The guru reads this file, writes briefs for the worth-doing entries, and marks each `briefed NNN` or `dropped (reason)`. Only the guru changes an entry's status.

Entry format, newest at the bottom:
```
### <short title>
- Found by: <role / brief>, <date>
- Where: <files or area>
- Problem: <what is wrong, with a number or an error message>
- Suggested lane: g | w | c | r | s
- Status: open
```

### `wdt_analytics` does not import
- Found by: guru review of 006c, 2026-11-15
- Where: `model_v1/wdt_analytics.py` (was `model/`)
- Problem: `import rates_core` fails with ModuleNotFoundError; the module is now `rates_core1.py`. Present before 006c (baseline 16b06df has only `rates_core1.py`). Legacy; may be moot after the audit 001c.
- Suggested lane: c
- Status: taken (brief 058c)

### Revenue calculator fetches a file that no longer exists
- Found by: brief 010s, 2026-11-15
- Where: `site/tools/revenue_calc.html`, `site/_quarto.yml` (resources)
- Problem: both name `model/rates_model.py` (now `rates_core1.py`, and not published), so the calculator probably fails. Needs the author's decision (fix, replace or remove); architecture doc Issue 16.
- Suggested lane: s
- Status: parked (author, 2026-11-16): a new revenue calculator comes after model v3.

### Hardcoded Zenodo sandbox token
- Found by: brief 004s, 2026-11-15
- Where: `pipeline/zenodo_upload.py`; git history
- Problem: a sandbox token is in the source (Issue 7). The author revokes it; then read it from an environment variable.
- Suggested lane: s
- Status: wontfix for now (author, 2026-11-16): Zenodo sandbox is a non-critical test environment.

### Site build leaves tracked files modified
- Found by: brief 003s, 2026-11-15
- Where: `registry/contents.yml`, `site/pages/glossary.md`, `registry/references.json`
- Problem: the build rewrites them (561 + 244 changed lines in the first two) so it is not `git status` clean. Needs the author's decision on whether they stay tracked.
- Suggested lane: s
- Status: done 2026-11-16: `references.json` and `glossary.md` untracked and ignored; `contents.yml` stays tracked (hand-written titles; the build only syncs it).

### Rename the wdt-web skill to wdt-site
- Found by: author, 2026-11-16 ("i might even rename wdt-web to wdt-site for consistency")
- Where: `.claude/skills/wdt-web/`, `Tools/wdt-web.skill`, the role name `web` in `AGENTS.md`, `docs/agents/`, `OVERVIEW.md`, and the claude.ai account skill
- Problem: the lane letter is `s` (site) but the role and skill are called web. Not decided; the author may do it.
- Suggested lane: g
- Status: open

### RATES 0.35% burden uses terminal wealth, M2 in metrics.md uses start-of-year wealth
- Found by: research / brief 012r stage B4, 2026-11-17
- Where: `source/8_Rates_and_Revenue.md` (burden table, "Revenue-weighted average 0.35%"), `source/8a_Rates_and_Revenue_Appendix.md` B.3.3, `docs/model-v3/metrics.md` M2
- Problem: the paper's 0.35% is tax over post-settlement terminal wealth (N = 30), weighted by terminal wealth. M2 is the tax-weighted mean of T_i/W_i with W_i start-of-year wealth. From the printed tables the same tax gives 0.39% on terminal wealth, about 1.2% on a crude path average and 4.1% on starting wealth (`docs/research/012r-b4-derivations.md`). The claim "structurally below the 1 to 2% of stock levies" holds only on the terminal denominator. The author has to choose M2's denominator, then writing may need to state it in RATES.
- Suggested lane: g
- Status: closed 2026-11-16 (author: start-of-year, `metrics.md` M2 denominator, `stage-c-decisions.md`), reconfirmed 2026-11-20; writing states the denominator in RATES when the papers are rewritten.

### Validator and fixture ignore `line_horizons`, so a final model file cannot pass V7 (OW3)
- Found by: code / brief 056c, 2026-11-18
- Where: `pipeline/validate_outputs.py` (`load_entries`, V7 coverage), `tests/data/make_fixture.py`, `docs/restructure/site/hooks.md` 3.4; also the `run` fields `pack_sha256`, `pack_country`, `levers_sha256` (A6), which V8 reports as unknown (V12 warning)
- Problem: `outputs.yml` gives OW3 line M15b the horizon `transition` only (A3), and the output layer writes only those cells. The validator expects the full product, so a `--final` check of a complete file fails with `V7 error OW3: 30 cell(s) missing`; the fixture still holds 90 OW3 cells. Provisional files pass (V7 is a warning). Needs the validator to read `line_horizons`, the fixture to follow, and A6 fields accepted.
- Suggested lane: c
- Status: taken (brief 058c)

### Register I-D4a (wealth to GDP 5.94) disagrees with the pack GDP
- Found by: guru review of 067c, 2026-11-19
- Where: `docs/model-v3/inputs.md` I-D4a; `model_v3/pack/GBR/wealth_distribution.csv` (`wealth_total` all 13,568, `gdp` 2,211.48)
- Problem: the pack gives 13,568 / 2,211.48 = 6.14; the register central is 5.94 on calendar-2021 GDP of 2,284 (OECD via FRED, not held). The base reads the pack, so the register row and the pack disagree on the same ratio. Decide whether the register row is recomputed from the pack (a `(J)` row, author decides) or the pack GDP is replaced
- Suggested lane: r
- Status: open

### Pack rebuild needs a full git history
- Found by: guru review of 067c, 2026-11-19
- Where: `model_v3/pack/build_gbr.py` `added()`
- Problem: the manifest `retrieved` dates come from `git log --follow` of each source file (066c). In a shallow clone the builder writes 2026-11-17 for every file and the committed manifest (2026-09-30 and 2026-11-15) is not reproduced, so the byte-identical rebuild check fails there. It passes in a full clone
- Suggested lane: c
- Status: open

### I-D4b central assumes fewer adults per household than I-D4h
- Found by: guru review of 069r, 2026-11-19
- Where: `docs/model-v3/inputs.md` I-D4b (central, method of `012r-b1-derivations.md`) and I-D4h
- Problem: I-D4b's central implies 1.77 adults per household; I-D4h's central, read from Tables 2.9 and 2.11, is 1.93 and counts people 16 and over. The two rows can drive different adult counts in `base.py`. Author to choose whether I-D4b's central is recomputed with 1.93 and whether an 18-and-over count is needed (the author could upload ONS mid-2021 population by age to separate the 16 and 17-year-olds)
- Suggested lane: r
- Status: open

### Fixture fake numbers are positional, so inserting an output shifts pinned test values
- Found by: guru / 079g, 2026-11-20
- Where: `tests/data/make_fixture.py`; pins in `tests/hooks/test_hooks.py` and `tests/hooks/test_cli.py`
- Problem: adding O2d to the manifest changed every later fixture number (CK1 P1 4.6 to 2.8, O3 1.00 to 1.30), failing five pinned hooks tests. Every manifest addition will repeat this.
- Suggested lane: c (derive each fake number from a hash of the output id, cell key and field, so only new cells appear; re-pin once)
- Status: done 2026-11-20 (091g `e64fd95`: numbers keyed by cell)
