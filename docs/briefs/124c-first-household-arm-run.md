# 124: The first household-arm run, as ranges over scenario grid points

- **Status:** ready
- **Author/date:** K. Ogata with the guru, 2026-11-22
- **Depends on:** 123c (merged)
- **Read (block 0: the first two only):** (1) `docs/model-v3/household-arm-outputs.md`; (2) `docs/agents/code.md`. Later, by block: `model_v3/runner/arm.py` (`build`, `household_inputs`); `model_v3/runner/runner.py` (`Ctx`, `core_run`, how `tests/model_v3/test_arm_switch.py` builds a household context); `docs/model-v3/household-arm-account/ledger_table.py` (grid point and setup); `docs/model-v3/outputs.yml` (read only).

## Goal
Produce the first outputs of the household arm and show them to the author as **ranges over labelled scenario grid points**, with the checks that say the run is sound. No grid point is called central. The legacy arm is run on the same paths only as labelled context. There is no run script yet (057c is held): drive the runner the way the tests do.

## Decisions (author, 2026-11-22)
- Grid: the three saving values (min, median, max) at the `mid` regime, plus the two JST market regimes the stored inputs hold at median saving: five points. Everything else as the account's centre (schedule tau_0 0.04, tau_m 0.7, k_ln 1, ratio 0.5; B.6g income scale 1.3733; tail pension cap I-D1l; stand-in safe return).
- Class returns are fixed scenario rates (the market path is not read by the household arm); only GDP growth moves with the path. The note says so up front.
- The withheld ids stay withheld. No claim is made that a result is a forecast: every table carries its scenario label.
- The author reads ranges and the checks, then decides what is next; no tuning, no parameter change in this brief.

## Blocks (one push each; `docs/agents/code.md`, Long builds)
- **Block 0:** progress block pushed.
- **Block 1: the run script.** `docs/model-v3/household-arm-run/run_grid.py`: for each of the five grid points, one level 1 evaluation (a stated number of paths, at most 2,000; say which and why) through `core_run` and the output groups, writing a small CSV of headline results per grid point (M1 to M1d, fill, unfilled, M2 by band, M2b to M2d, OP/P series the manifest lists, in the units the manifest states) and the checks per run: I1, the account identity, the ledger ties, `unpaid_B`, shortfall lines. Tests: the script's checks on a two-path smoke. Push.
- **Block 2: the runs.** Run the grid (background, summary lines only on screen) and the legacy arm at `I-D14c` on the same paths as context. Push the CSVs. If a run fails or `unpaid_B` is non-zero, report the grid point, inputs and error; do not change a rule. Push.
- **Block 3: the note.** `docs/model-v3/household-arm-run.md`: the grid with labels; one table per output family as ranges across grid points (min to max, no central); the check results; the legacy-arm numbers beside them as labelled context; a short list of anything odd (negative values, fill that never happens, a headline an order of magnitude from the legacy arm, a band with an implausible M2). The tornado (OT1) and the feasibility map (OF1) on the full model under the household arm are run here only if they fit the session; otherwise listed under Next with the reason. Change report; push; stop.
**Stop rule.** After three blocks, or a quarter of the budget left, push what exists and list the rest under Next. Print only summary lines; suites in the background, never piped; paths limited as above.

## Touches
`docs/model-v3/household-arm-run/` (new script and CSVs), `docs/model-v3/household-arm-run.md` (new), tests (a smoke test for the script), `docs/model-v3/architecture.md` (budget rows only). Name any further file before editing it. Not the kernel, `revenue.py`, `burden.py`, the register, the pack, the runner, the manifest or the digest fixture; a bug found in any of them is reported with its inputs, not fixed here.

## Acceptance criteria
- `test_legacy_digest` and all suites pass; no model file changed.
- Five grid points run; every result carries its scenario label; no value is called central.
- The checks (I1, account identity, ledger ties, `unpaid_B`, shortfall lines) are reported per grid point and hold, or the failure is reported with its inputs.
- The note shows ranges and the legacy arm only as labelled context.

## Checks to run
`test_legacy_digest`; the v3 suites in the background; the run script with summary lines only; `python -I pipeline/check_agent_docs.py`.

## Out of scope
Any parameter change or tuning, validation against the 099r moments (125c), the comparators (126c), per-path return regimes, pension withdrawal, a saving gradient, a headline or a policy claim.

## Open questions
The number of paths per grid point, and whether OT1 and OF1 fit (the agent states both).

## Implementation notes
<!-- progress:start -->
- **Done:** none
- **Next:** block 0
- **Resume:** `git fetch origin '+refs/heads/*:refs/remotes/origin/*' && git checkout -B brief/124-first-run origin/brief/124-first-run`
- **State:** ready; not started
<!-- progress:end -->
