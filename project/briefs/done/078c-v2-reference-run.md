# 078: Run v2 once at logistic_ln_ref and record its output as a fixture

- **Status:** ready
- **Author/date:** K. Ogata with the guru, 2026-11-19
- **Depends on:** none (074c's table is on branch `brief/052c-rework`: `git show origin/brief/052c-rework:docs/model-v3/i1-gap.md`)
- **Read:** `docs/model-v3/i1-gap.md` (above, "Not recovered" and "Recommended fix"); `docs/model-v3/architecture.md` lines 228 to 233 (I1, I2); `docs/model-v3/tornado.md` section 4; `model_v2/README.md`, `model_v2/WDT_Code_Reference.md`, `model_v2/WDT_Params.toml` (the `logistic_ln_ref` scenario at its line about 915); `synthesis.md` section 10 (the recorded 7.34); `docs/agents/code.md`.

## Goal
One run of v2 at the `logistic_ln_ref` scenario, with its per-window output and the distribution table it used written to a data file, so identity test I1 can stay strict and the unexplained 0.68 points can be located. The author has decided v2 is run **once** for this, as a reference recording; v2 stays out of the model and is never imported by `model_v3/`.

## Decisions (author, 2026-11-19)
- Run v2 unchanged. Do not edit anything under `model_v2/`. Run it from a scratch copy if the run writes files into its own folders.
- The product is a fixture, not code: v3 tests read the file; nothing in `model_v3/` calls v2.

## Design
1. Find how v2's recorded headline is produced (which statistic: median or mean over the 117 windows, the post-fill 10-year take, net or gross of refunds, as % of GDP) and say so in the report with the file and function. Reproduce the 7.34; if the run gives a different number, stop and report (do not tune).
2. Write `tests/model_v3/fixtures/v2_logistic_ln_ref.json` with: the headline value to full precision and its definition; per window (117): window start year, fill year, take gross and net as % of GDP, realised eps if v2 computes it; the distribution table v2 used (the 41 cells: share of adults and wealth in £bn at calibration, total, adults, GDP, W_min, `house_median_gbp_m`); the settings that were in force (scenario name, toml hash or the toml values read); v2's `gpc_real` series used for the threshold index (117 values or the years it spans); the code version (commit hash) and date.
3. Add a README block at the top of the JSON (a `_meta` key) with the exact command run and its output's last lines.
4. A small test `tests/model_v3/test_v2_reference.py`: the fixture loads, has 117 windows, the headline equals the median (or whichever statistic found in step 1) of the per-window array to 1e-9, and the 41 cells sum to the recorded total.

## Touches
`tests/model_v3/fixtures/v2_logistic_ln_ref.json` (new), `tests/model_v3/test_v2_reference.py` (new), this brief's progress block. Nothing under `model_v2/` and nothing in `model_v3/`.

## Acceptance criteria
- The recorded headline reproduces 7.34 (to the two places) or the report says it does not and stops.
- Fixture holds every field in Design 2; the new test passes; `pytest tests/model_v3 -q` otherwise unchanged.
- `git diff --stat` limited to Touches; `git status` shows nothing changed under `model_v2/`.

## Checks to run
`pytest tests/model_v3 -q`; `git status --short model_v2`.

## Out of scope
Any change to v2 or v3 model code; I1 and I2 themselves (052c).

## Open questions
Ask rather than guess: if the run needs data that is not in the repo or takes more than about an hour, stop and report the time and what is missing.

## Implementation notes
<!-- progress:start -->
- **Done:** v2 run once at `logistic_ln_ref` (UK, 117 windows, 2.5 s) from a scratch copy; fixture `tests/model_v3/fixtures/v2_logistic_ln_ref.json` and `tests/model_v3/test_v2_reference.py` (3 tests). `pytest tests/model_v3 -q`: 145 passed. `git status --short model_v2`: empty.
- **Next:** 052c rework uses the fixture; I1 should compare the mean, not the median.
- **Decisions:** (1) The scratch copy of `WDT_Params.toml` got one line, `store_windows = true` under `[rates.scenarios.logistic_ln_ref]` (window rows are not kept otherwise; the 2026-11-16 closure check did the same); no number changes. (2) Per-window fields in the fixture are fractions of GDP as v2 writes them; headline numbers are percent. (3) The fixture holds `_meta` with the command, the last output lines and the extraction script.
- **Gotchas:** (1) **The recorded 7.34 is a mean.** It is the mean over the 117 windows of `wdt_gdp_h`, written by `rates_core._horizon_cols` (line 1498): net individual WDT (tax + death tax + heirs - refunds, no levy), years fill to fill+9, ratio of sums over GDP. Mean 7.3416. The median, which `rates_core.headline` prints, is 6.594. 074c and 052c compared a v3 median with 7.34: different statistics, and the gap 7.34 - 6.59 = 0.75 is what a mean-for-median swap alone explains of 074c's 0.68 remainder. (2) v2 computes no gross post-fill take and no realised eps; the fixture keeps the net take, whole-window means of tax, refunds and net, and `er_gain_all` / `er_stock_all`. (3) Levy: entry rate calibrated to a 3.08% base (nominal median); the levy actually paid post-fill, `levy_gdp_h`, has median 2.774%, the 2.77 in synthesis section 10. (4) Fill year median 7, no censored window. (5) The 41 cells: total 15,120bn, 51.0m adults, GDP 2,097.1bn, W_min 0.1125 (0.5 x 0.225), wealth/GDP 7.21; they match the 074c rewrite's totals.
- **Resume:** none.
- **Not run:** nothing in the brief.
- **State:** done; criteria met; merged
<!-- progress:end -->

### Change report
```
Change report
- Task: brief 078c, v2 reference run recorded as a fixture
- Files changed: tests/model_v3/fixtures/v2_logistic_ln_ref.json (new); tests/model_v3/test_v2_reference.py (new); this brief
- What is different now: v3 tests can read v2's per-window output, 41-cell table, settings and gpc_real at logistic_ln_ref; the recorded 7.34 is identified as a mean (median 6.594).
- New or changed interfaces: none
- Acceptance criteria: headline reproduces 7.34 (met: mean 7.3416); fixture holds every Design 2 field and the new test passes, suite 145 passed (met); diff limited to Touches, model_v2 untouched (met)
- Deviations from the brief: one line added to the scratch copy's toml to keep window rows (not the repo)
- Risks / follow-ups: 052c's I1 and I2 should compare the v3 mean (not median) with 7.34 and 074c's table should be reread with that; the fixture records no gross take and no realised eps (v2 does not compute them)
- Verification: pytest tests/model_v3 -q: 145 passed; git status --short model_v2: empty
- Overview sections likely needing an update: model v3 status (I1 definition)
- Commit / branch: brief/078-v2-reference; brief 078c merged, ready to retire
```
