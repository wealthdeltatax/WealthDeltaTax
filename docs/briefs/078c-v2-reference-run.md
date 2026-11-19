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
- **Done:**
- **Next:**
- **Decisions:**
- **Gotchas:**
- **Resume:**
- **Not run:**
- **State:** ready; not started
<!-- progress:end -->
