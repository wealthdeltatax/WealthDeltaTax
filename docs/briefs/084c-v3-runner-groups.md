# 084: Runner groups: split `evaluate` so output groups can be added in parallel, and move `payer_taxes` into the lever file

- **Status:** ready
- **Author/date:** K. Ogata with the guru, 2026-11-20
- **Depends on:** 055c (merged, `e4993a4`)
- **Read:** `docs/archive/briefs/055c-v3-10-range-runner.md` (progress block, gotchas 4 and 6); `model_v3/runner/runner.py` (`context`, `evaluate`, `make_ev`, `cat`, `samples`, `level1`, `level2`); `docs/model-v3/architecture.md` 2.9, 2.10, 5.1 and 6.1; `model_v3/levers.json`.

## Goal
`runner.evaluate` keeps its numbers but exposes the raw core results to four output groups, so briefs 085c to 088c can each fill one file without touching `runner.py`; and `payer_taxes` lives in `levers.json`, not in a caller argument.

## Decisions (author, 2026-11-20)
The 055c runner builds only O1, O1a to O1c, O2, O3, O4a and O1f into Samples (plus the sweep functions); the other 32 manifest ids are assembled by group files. `payer_taxes` belongs in the lever file (055c gotcha 6).

## Design
1. Split `evaluate` into `core_run(ctx, theta, spec, g, gdp_g, full=False)` returning a `Raw` (a small dataclass: the shaped base, rate, line flows, run, revenue result, window bounds, incidence) and `headlines(raw, ctx, theta)` returning exactly what `evaluate` returns now. `evaluate` = `core_run`, then `headlines`, then, for each module of `GROUPS`, `{module.NAME: module.per_path(raw, again)}` merged into the result. `again(spec_override)` calls `core_run` with the same `ctx`, `theta`, `g`, `gdp_g` and the changed spec, cached per call on the spec.
2. `model_v3/runner/groups.py` (about 15 lines): `GROUPS = (out_revenue, out_burden, out_support, out_sweeps)`, imported explicitly (no discovery, no silent skip).
3. Create the four stubs `out_revenue.py`, `out_burden.py`, `out_support.py`, `out_sweeps.py`: each has `NAME`, `IDS = ()`, `per_path(raw, again) -> {}` and `cells(e) -> {}`.
4. `samples()` adds, per schedule, `module.cells(e[module.NAME])` for each group, and fails (raises) if two groups return the same output id or an id that is not in the manifest (R1).
5. `payer_taxes`: add `"payer_taxes": ["cgt", "iht"]` to `levers.json` (the names the 055c tests pass), read it in `context`, drop the argument, update the tests and the `levers_sha256` pins; report which tests pinned the hash.
6. Add the four new files and their test files to the budgets table in `architecture.md` 6.1 (proposed: each group 150 code, 80 tests; `groups.py` 20, 0), and amend `runner.py` to whatever it grows to, up to 360.
7. Add one test per group stub: the empty group changes no existing number (the `samples` output equals 055c's, byte for byte, for the same seed).

This brief cannot be split: it edits `runner.py`, which every group brief depends on.

## Touches
`model_v3/runner/runner.py`, `model_v3/runner/groups.py`, `model_v3/runner/out_revenue.py`, `out_burden.py`, `out_support.py`, `out_sweeps.py`, `model_v3/levers.json`, `tests/model_v3/test_runner.py`, `tests/model_v3/test_groups.py`, `docs/model-v3/architecture.md` (6.1 budget rows only), this brief's progress block, `docs/agents/friction-log.md`.

## Acceptance criteria
- Every existing runner test passes unchanged except those that passed `payer_taxes`; `samples` for the 055c ids is byte-identical to before for the same seed.
- `runner.py` at most 360 lines; `levers.json` still passes the `levers` rule tests; `pytest tests/model_v3 -q` and `python pipeline/run_suites.py` pass.
- `git diff --stat` limited to Touches.

## Checks to run
`pytest tests/model_v3 -q`; `python pipeline/run_suites.py`.

## Out of scope
Any group's per-path code (085c to 088c); the feasibility rule (089c); a new output.

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
