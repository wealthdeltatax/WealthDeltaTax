# 085: Revenue and fund outputs into Samples

- **Status:** ready
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
- **Done:**
- **Next:**
- **Decisions:**
- **Gotchas:**
- **Resume:**
- **Not run:**
- **State:** ready; not started
<!-- progress:end -->
