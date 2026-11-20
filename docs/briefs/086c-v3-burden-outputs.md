# 086: Burden and savings outputs into Samples

- **Status:** ready
- **Author/date:** K. Ogata with the guru, 2026-11-20
- **Depends on:** 084c
- **Read:** `docs/archive/briefs/055c-v3-10-range-runner.md` (gotcha 4); `model_v3/runner/out_burden.py` (the stub); `model_v3/core/burden.py` (module note, `line_flows`, `m2`, `m4`, `m3`, incidence); `docs/model-v3/outputs.yml` entries O2d, O2b, O2c, O4b, O5, O6, O8, OL1, OH1b, OH1b2, OH1c, DH1c; `docs/model-v3/metrics.md` rows M2b to M6, M8, M11, M12, M4c; `docs/model-v3/metrics.md` "Closed on 2026-11-20" (what 053c did not build).

## Goal
The twelve burden-side outputs exist in Samples: O2d (M2 including settlement at death), O2b and O2c (M2 below W_min cutoffs), O4b, O5, O6, O8, OL1 (M4c by reference worker), OH1b (M3 by wealth band), OH1b2 (M11), OH1c (M12 by cause), DH1c (the non-payers' bill by income decile, a data fact).

## Decisions (author, 2026-11-20)
053c's limits stand: OH1b all-tax line, M8 non-payer saving, M2b and M2c below W_min and thresholds on line means were not built; if the core cannot produce one of these, report it as a limit of the first run (it goes to `metrics.md` "Closed on 2026-11-20" as a limit), do not build it here. M5 has no with-death line (open for the author, 079g): do not add one. O2d needs the death flows that `evaluate` zeroes when `full=False`: read them from `again`'s `full=True` run or from the line flows, whichever the core supports, and say which.

## Design
Fill the stub `model_v3/runner/out_burden.py` that 084c created. It exposes `NAME`, `per_path(raw, again)` (per-path arrays for one chunk of paths: the dict's leaves are 1-D arrays over paths, the structure is in its keys; `again(spec_override)` returns the `raw` of the same paths under a changed schedule, cached) and `cells(e)` (turns the concatenated per-path dict `e` into `{output id: {(horizon, by, line): array}}`, with `by` a sorted tuple of `(name, value)` as `architecture.md` 2.9 says). The `by` vocabularies and `lines` are those of each id's entry in `outputs.yml`; the horizons are the manifest's (`single` is one cell). Never edit `runner.py`, `groups.py` or `evaluate`.

For each id, map its metric to the `core/burden.py` function that produces it and write the map in the change report. **If a metric the manifest names is not produced by the core module, or an input the core takes from the caller has no register row or pack field, do not invent a value: stop and report to the guru** (the 054c and 055c rule). Inputs the caller supplies are read from the register and pack as 055c does (`ctx`, `theta`); name each row id in the report.

**Early check.** O2d minus O2 (in life) over the short window must reproduce 053c's pattern: death flows are the larger part of M2 including death (22.2% a year with them, 2.8% without at 053c's central run). Report both numbers; stop and report if they differ by more than a tenth.

**Shared interfaces, fixed before any stage starts** (a build brief never edits them; a mismatch is a question to the guru): the output file shape is `schema wdt-outputs/1` as `pipeline/validate_outputs.py` checks it and `docs/restructure/site/hooks.md` section 3; the Samples contract is `architecture.md` 2.9; the id lists are `docs/model-v3/outputs.yml` and the module-to-id table of `architecture.md` 2.10; the layers and import rules are `architecture.md` 5.1; the group interface is the one 084c fixes (`model_v3/runner/groups.py`).

## Touches
`model_v3/runner/out_burden.py`, `tests/model_v3/test_out_burden.py`, this brief's progress block, `docs/agents/friction-log.md` (and `model_v3/runner/runner.py` with `tests/model_v3/test_runner.py` for the one narrow edit in ruling 4, only if needed).

## Acceptance criteria
- Each built id returns one cell per schedule, horizon and `by` value in the manifest; every id not built is listed with the reason (a stated limit of the first run).
- The early check numbers are in the report.
- `out_burden.py` at most 150 lines and its tests at most 80; `pytest tests/model_v3 -q` passes.
- `git diff --stat` limited to Touches.

## Checks to run
`pytest tests/model_v3 -q`.

## Guru rulings 2 (2026-11-20, after your second stop; manifest A13 is on `main`)
Rebase onto `main` first (it holds A13 and the regenerated fixture; no test pin moves). Resume from branch `brief/086-work` and build the five ids:
1. **O5** (`by.comparator`: zucman, uk_minimum, union, green, once; `lines`: burden, diff; units pct_per_year and pp): `burden` = `m5` burden, in life; `diff` = its `<comparator>_diff` against the same schedule's M2 in life (`m2_wdt`). No with-death line (079g, still open for the author): do not add one.
2. **O6** (`by.wealth_band`; `lines`: gains, estates, total; pct_per_year): `m6(reg)` values. They come from the register only, so every path has the same value; the manifest keeps them per schedule and horizon, as for DH1c.
3. **O8** (short only; `by.reform`: property, gains; `lines`: burden, diff): `burden` = `m8(...)['burden']` with M1 in pounds per path from `raw.r` (check against the M1 headline) and `bd.reform_shares(env.pack)`; `diff` = that burden minus the same schedule's M2 in life, percentage points. The non-payer saving form stays a limit.
4. **OH1b and OH1c** (`static(env)`, single horizon, once): threshold ratio **0.5** (the v2 reference ratio), **1,000 paths** (`CHUNK`) of returns from `env.rng('burden.static')` with the AR(1) generator at `env.theta`'s mean, sd and phi, GDP growth `ctx.gdp_g`, base `bs.build_base(env.pack, env.ctx.reg, 0.5)` unshaped (at central inputs the shaping scales payer wealth uniformly and M3 and M12 are ratios, so it cancels: say so if a test shows otherwise). Cells are p10, mean, p90 over the paths. If something needed is not reachable from `Env` without importing `runner` (layer rule), you may make the smallest edit to `runner.py` (`Env` or `statics`), name it in the report, keep the file at most 360 lines and the 084c and 092c digests unchanged; `runner.py` and `tests/model_v3/test_runner.py` are then in Touches for that edit only. In tests pass `once=` to `context`; the run script passing it is 057c's.
5. **DH1c and OH1b2** stay per schedule and horizon as built. The M5 and M8 line-mean thresholds stay a limit of the first run.

Stop again only for a gap in these rulings, and name it.

## Out of scope
Any other group; `runner.py`; building the 053c limits.

## Guru rulings (2026-11-20, after the stop; brief 092c)
Your five ids stay. Wait for 092c: the signature becomes `per_path(raw, env, again)` with `env.ctx`, `env.theta`, `env.pack`; rebase onto main after it merges and build O5, O6, O8, OH1b, OH1b2, OH1c and DH1c from `env`. 092c changes the two `test_groups.py` pins you hit; do not edit them. O8 takes M1 in pounds per path from `raw.r` (check against the M1 headline). Note the manifest A12 does not change DH1c (still per schedule and horizon); say in your report if that looks wrong.

## Open questions
None.

## Implementation notes
<!-- progress:start -->
- **Done:** all twelve ids in `out_burden.py` (106 lines, budget 150), tests 78 lines (budget 80); `pytest tests/model_v3` 222 passed, `run_suites` 10 of 10; cells checked against the manifest vocabulary (by, lines, horizons): no mismatch. Metric map: O2d = `m2d(raw.fl, lo, hi)` (the death flows are in `raw.fl`, the line flows the core keeps; `again` unused); O2b, O2c = `m2b`/`m2c` shares of payers above each cut-off (all net WDT, the burden.py default; the payer mean has no cell); O4b = `m4(...)['M4b']` with `raw.base.income_deciles`; OL1 = `m4c` on it; OH1b2 = `m11(ctx.reg)` (I-T1d); DH1c = `dh1c(env.pack, ctx.rec, mp['parts'], mp['payer_taxes'])['bill_pct_income']` (share of income: the manifest has unit pct); O5 = `m5(base.wealth, base.adults_k, reg, m2_in_life_overall)` per horizon, `burden` and `diff`, no with-death line (079g); O6 = `m6(reg)` (I-M6a to I-M6i, the same on every path); O8 = `m8(...)['burden']` short only, revenue = post-fill window mean of `raw.r['M1'] * raw.r['gdp']` in pounds bn (its share of GDP equals the M1 headline, tested), shares `reform_shares(env.pack)`, `diff` = burden minus M2 in life; OH1b = `m3_today`, OH1c = `m12` inside `static(env)`: 1000 paths from `env.rng('burden.static')` (`returns.ar1_paths` at I-D1a, I-D1b, I-D1b2), `build_base(pack, reg, 0.5)` unshaped, rates I-D11a to c, c I-D14c; `exempt_law` is the manifest's `exempt_by_law`.
- **Early check (200 paths, seed 7, SPEC, short):** M2 in life 3.00, M2d 23.48 against 053c's 2.8 and 22.2: within a tenth. Long: 1.01 and 12.42.
- **Other central values (same run):** O5 burden 1.0 to 2.0% a year (once 1.0, green 1.58, zucman and uk_minimum 1.8, union 1.99), diff -1.0 to -2.0 points; O6 overall 0.14 gains + 0.06 estates = 0.20; OH1b overall 8.1% (D10 11.4), OH1b2 19.4%; OH1c overall deferral 25.7% and exempt 42.4% (053c: 25.6 and 42.4); O8 short, gains reform, p10, p50, p90 of burden 3.6, 28.2, 97.2 and of diff 1.0, 24.6, 92.6.
- **Decisions:** none new. The unshaped base is a fair stand-in (the test compares M3-today on the shaped and unshaped base within 5%).
- **Gotchas:** (1) **O8 is dominated by M1.** SPEC (tau_m 90%) raises revenue many times the GDP share of a mild schedule, so the reform that raises the same amount burdens 28% of wealth a year at the median, and the diff against M2 in life (3%) is +24.6 points; against M2d (with death, 23%) it would be +5. The ruling compares with M2 in life, as built; the guru may want the with-death comparison (as for M2d). (2) A reform with no base share for a band that holds payers (property in D4-5, at a low threshold ratio in the sweep) gives nan, not an error: a limit of the first run, named here. (3) `static` returns only the ids `ctx.once` holds, as 088c's does, so the shared test fixture (no once ids) is unchanged: no edit to `test_runner.py` and none to `runner.py` (360 lines). The run script passing `once` is 057c's. My first push to main carried a fixture edit that broke 088c's `test_dh1a_and_dh1b...`; this commit reverts it. (4) M5 and M8 line-mean thresholds and the all-tax OH1b line stay limits.
- **Resume:** none.
- **Not run:** a full level 2 with `static` (OH1b, OH1c are computed per draw there, 1000 paths each).
- **State:** done; merged to main; ready to retire.
<!-- progress:end -->
