# 085: Revenue and fund outputs into Samples

- **Status:** retired 2026-11-20 (merged `4cc6a64`)
- **Author/date:** K. Ogata with the guru, 2026-11-20
- **Depends on:** 084c
- **Read:** `docs/archive/briefs/055c-v3-10-range-runner.md` (gotcha 4); `model_v3/runner/out_revenue.py` (the stub); `model_v3/core/revenue.py` (module note and `revenue`); `docs/model-v3/outputs.yml` entries O1d, OP1, OP3, OP4, OP5, OP6, OR1, OB1; `docs/model-v3/metrics.md` rows M1e, P1, P3, P4, P5, P6, P7, B1.

## Goal
The eight revenue-side outputs exist in Samples for each named schedule: O1d (M1e by retired tax), OP1, OP3, OP4, OP5, OP6 (by year 10, 25, 50, 100), OR1 (P7a, P7b), OB1 (B1a to B1d by threshold ratio r025, r050, r100).

## Decisions (author, 2026-11-20)
O1d and OB1 follow the manifest's `by` lists as they are. OB1 needs the base at three threshold ratios: use `again`.

## Design
Fill the stub `model_v3/runner/out_revenue.py` that 084c created. It exposes `NAME`, `per_path(raw, again)` (per-path arrays for one chunk of paths: the dict's leaves are 1-D arrays over paths, the structure is in its keys; `again(spec_override)` returns the `raw` of the same paths under a changed schedule, cached) and `cells(e)` (turns the concatenated per-path dict `e` into `{output id: {(horizon, by, line): array}}`, with `by` a sorted tuple of `(name, value)` as `architecture.md` 2.9 says). The `by` vocabularies and `lines` are those of each id's entry in `outputs.yml`; the horizons are the manifest's (`single` is one cell). Never edit `runner.py`, `groups.py` or `evaluate`.

For each id, map its metric to the `core/revenue.py` function that produces it and write the map in the change report. **If a metric the manifest names is not produced by the core module, or an input the core takes from the caller has no register row or pack field, do not invent a value: stop and report to the guru** (the 054c and 055c rule). Inputs the caller supplies are read from the register and pack as 055c does (`ctx`, `theta`); name each row id in the report.

**Early check.** `OP3` must equal the `P3h` that `headlines` already computes for the same horizons (the same numbers, a test). `O1d`'s seven receipt lines must sum to the `M1e` the revenue run reports (to 1e-9).

**Shared interfaces, fixed before any stage starts** (a build brief never edits them; a mismatch is a question to the guru): the output file shape is `schema wdt-outputs/1` as `pipeline/validate_outputs.py` checks it and `docs/restructure/site/hooks.md` section 3; the Samples contract is `architecture.md` 2.9; the id lists are `docs/model-v3/outputs.yml` and the module-to-id table of `architecture.md` 2.10; the layers and import rules are `architecture.md` 5.1; the group interface is the one 084c fixes (`model_v3/runner/groups.py`).

## Touches
`model_v3/runner/out_revenue.py`, `tests/model_v3/test_out_revenue.py`, this brief's progress block, `docs/agents/friction-log.md`.

## Acceptance criteria
- Each of the eight ids returns one cell per schedule, horizon and `by` value the manifest lists; none is NaN on the 1,000-path central run except where the fund never fills (report that count).
- OP3 equals `headlines` P3 as above; O1d sums to M1e.
- `out_revenue.py` at most 150 lines and its tests at most 80; `pytest tests/model_v3 -q` passes.
- `git diff --stat` limited to Touches.

## Checks to run
`pytest tests/model_v3 -q`.

## Guru rulings 2 (2026-11-20, after your stop)
Accepted: your decisions 1 to 6 (tax names from `env.ctx.rec` pinned to the manifest `by.per`; OB1 windows as a ratio of sums; P7b nan where no year follows the fill). The `test_groups.py` clause is fixed on `main` (your exact edit): after you rebase, the file has no diff and the diff is inside Touches, so the auto-merge rule applies. Run the checks again after the rebase, then merge as `AGENTS.md` says.

## Out of scope
Any other group; `runner.py`; the validator.

## Guru rulings (2026-11-20, after the stop; manifest A12, brief 092c)
Wait for 092c (group interface: `per_path(raw, env, again)`, `again(over, full=False)`) before the ids that need it; build **OP1, OP3, OP4 and OP6 now** (OP4 is the ratio only; the first year below zero is text, not a cell).
1. **OB1:** read B1a to B1d with `again({}, full=True)` (the payer record is only kept there); lambdas come from `env.lam`.
2. **O1d and OP5:** six taxes, names as the core: `corporation_tax, council_tax, business_rates, cgt, iht, stamp_duties` (manifest `by.per`). OP5's cell per tax is that tax's retirement year (a column of P5).
3. **OR1:** P7a and P7b are single-horizon (manifest `horizons: [single]`): one value per path over all years after the fill, as `revenue()` returns them.
4. Do not name taxes in `out_revenue.py` by hand: read them from the manifest `by.per` list (R11).

## Open questions
None.

## Implementation notes
<!-- progress:start -->
- **Done:** `model_v3/runner/out_revenue.py` (56 lines, budget 150) fills O1d, OP1, OP3, OP4, OP5, OP6, OR1, OB1; `tests/model_v3/test_out_revenue.py` (65 lines, budget 80, 5 tests); `pytest tests/model_v3 -q`: 211 passed (run as its own process).
- **Next:** none; the group is merged.
- **Decisions:** (1) taxes: names are the keys of `env.ctx.rec` (pack and lever file), so none is written in the file (R11); a test pins them equal to the manifest `by.per`. The ruling said read them from the manifest; `Env` has no manifest and the file read would belong to the runner. (2) OB1 B1b and B1c: the core keeps counts (thousands of adults); the manifest unit is `pct_per_year`, so each window is 100 x the sum of entries (or exits) over the sum of the payers of the year before. A mean of yearly percents had a tail (max 2,980 %) where a path's payers fall near zero. B1a and B1b to B1d use a flat weight, B1d the GDP weight, each at its own threshold's fill year windows. (3) OB1 horizons are the three (the manifest has none), OR1 and the P outputs `single`. (4) OP3 single is `r['P3']`, which equals `headlines` P3h `long` (years 1 to T): the early check compares with that. (5) P7a is 0 or 1 per path (as O1f); P7b is nan where no year follows the fill (it was inf, which `mean_of` would turn into an infinite mean). (6) `RATIOS` (r025 0.25, r050 0.5, r100 1.0) is a constant in the file; a test pins it to `levers.json` axes and the manifest labels.
- **Gotchas:** `tests/model_v3/test_groups.py` asserted that all four groups are empty and failed once the revenue group was filled; the guru put my exact one-clause fix on `main` (abca600), so after the rebase the file has no diff here. Friction-log entry written.
- **Resume:** none; rebased on `main` abca600 and merged.
- **Not run:** the site build (nothing here is in it); N1 10,000 paths.
- **State:** merged
<!-- progress:end -->

### Change report
```
Change report
- Task: brief 085c, revenue and fund outputs into Samples
- Files changed:
  - model_v3/runner/out_revenue.py: the group (IDS, per_path, cells), 56 lines
  - tests/model_v3/test_out_revenue.py: 5 tests, 65 lines
  - (tests/model_v3/test_groups.py: the same clause fix was put on main by the guru; no diff here after the rebase)
  - docs/agents/friction-log.md: one entry; docs/briefs/085c-v3-revenue-outputs.md: progress block and this report
- What is different now: Samples carries the eight ids for each schedule: O1d 18 cells (six taxes x three horizons), OP1, OP3, OP4 1 each, OP5 6, OP6 4, OR1 2 (P7a, P7b), OB1 36 (three thresholds x three horizons x four lines).
- Metric to core map: O1d M1e = revenue.revenue r['M1e'] by tax, windowed as M1 (revenue.window_mean); OP1 P1; OP3 P3; OP4 P4_ratio; OP5 P5 column; OP6 P6; OR1 P7a, P7b; OB1 B1a to B1d from run_lines' payer record (`again({'ratio': r}, full=True)`), B1b and B1c as percents (Decision 2).
- Register rows read (through core_run, not by this file): I-D14a, I-D14b (lambdas, `env.lam`), I-D14c (consumption), I-D14d to I-D14f (reserve), I-D7a (levy), I-D8a (reserve targets), I-D4a, I-D5a (base). No new row; none missing.
- Acceptance criteria:
  1. One cell per schedule, horizon and by value: MET (counts above, tested against the manifest lists). None NaN on the 1,000-path central run (seed 7, SPEC 0.04, 0.9, 1.0, 0.5, 21 s): MET except OR1 P7b, 1 path nan (a fill in the last year, so no year after it); the fund fills on all 1,000 paths (unfilled 0).
  2. OP3 equals headlines P3h long: MET (array equal). O1d sums to the retired receipts M1d: MET (1e-9, all three horizons, test).
  3. out_revenue.py at most 150 lines and tests at most 80: MET (56, 65). pytest tests/model_v3: MET (211 passed).
  4. git diff --stat limited to Touches: MET after the rebase (out_revenue.py, test_out_revenue.py, the brief, the friction log).
- Deviations from the brief: tax names from `env.ctx.rec` rather than the manifest list (Decision 1); accepted by the guru (rulings 2).
- Findings (for the guru, none blocks): (1) B1d is exactly zero on every path at all three thresholds (1,000 paths): fall-through refunds never occur in the core's run; check the core before the figure uses OB1. (2) P5 is 0 where a tax is never retired, and 188 of 1,000 paths never retire corporation tax (9 council tax): the P10 and mean of OP5 include those zeros, so a rule for never (nan or T) is needed in assemble. (3) OP3's mean is 291 percent of GDP at the central schedule (the known P3 finding). (4) OB1 long window: B1a 41, 26 and 13 percent of adults at r025, r050, r100; exits above entries.
- Risks / follow-ups: none new. The fixture and validator are unchanged by this brief.
- Verification: pytest tests/model_v3 -q 211 passed, before and after the rebase on abca600; three mutations of the file (OB1 without full, OP3 from P1, no short gate) each fail a test; python -I pipeline/check_agent_docs.py clean.
- Overview sections likely needing an update: model v3 status (outputs filled: revenue group).
- Commit / branch: brief/085-v3-revenue-outputs. Brief 085c merged, ready to retire.
```
