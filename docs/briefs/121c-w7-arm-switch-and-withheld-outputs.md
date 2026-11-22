# 121 (W7): The arm switch, labels and withheld outputs

- **Status:** ready
- **Author/date:** K. Ogata with the guru, 2026-11-22
- **Depends on:** 120c (merged)
- **Read (block 0: the first two only):** (1) `docs/model-v3/kernel-wiring-design.md` sections 3.6, 3.7 and the W7 row of section 4; (2) `docs/agents/code.md`. Later, by block: `model_v3/runner/runner.py` (`core_run`, `env_of`, `RUN`, `headlines`); `model_v3/runner/arm.py` (`HouseholdHook`, `line_state`, `returns`, `d10_pension`); `docs/model-v3/household-arm-account/account_table.py` (`setup`, `SPEC`: how the hook is built today, to be reused, not copied); `model_v3/runner/out_burden.py`, `out_support.py` (the sites that pass `c`); `docs/model-v3/outputs.yml` (read only).

## Goal
A run can choose the household arm. The arm is written into the run record and every output label; the outputs that cannot be like for like under it are withheld and labelled `legacy_only`; the author gets the list of what a household-arm run produces and withholds, before any number is read. The default stays `legacy` and its digest does not move.

## Decisions (author, 2026-11-22)
- `arm in {legacy, household}` read in `core_run`; default `legacy` (Q9). A household-arm result is never labelled or stored as a legacy result.
- Under the household arm M3, M12, M13 (the sites that still read `c`: `out_burden.py:77-79`, `out_support.py:57,82,105`, `burden.free_path`, `support.system_run`) are **withheld and labelled `legacy_only`**; they are not computed with a legacy `c` and shown beside household numbers (Q5). They return in their own later brief (comparators on the account).
- The household arm is **scenario-labelled**: saving (the three-value axis), the class returns (I-D1h to I-D1j and the market regimes), the pension accrual (I-D1k), the tail pension cap (I-D1l) are scenario rows. A run states which grid point it used; **no run is called central** and no headline revenue or fund number is shown to the author in this brief.
- Safe-asset return: until a register row exists, the safe class earns the **net financial class return** as a labelled stand-in, stated in the run label and the note. (120c left production with no `safe` series; this brief supplies one.)
- The arm's hook is built by the runner and passed down; the kernel stays numpy-only. Build it by moving the account script's `setup` into `arm.py` as one builder; the script then calls the builder (one construction, not two).
- Budgets: `runner.py` stays at 360 (net zero lines: move code out into `arm.py`, report if impossible); `arm.py` budget row is raised as needed and named.

## Blocks (one push each; `docs/agents/code.md`, Long builds)
- **Block 0:** progress block pushed.
- **Block 1: the arm switch and the builder.** `arm.build(arm, ctx, theta, spec, ...)` in `arm.py` returns the legacy hook (`c = I-D14c / 100`, as today) or the household hook with its state, class returns, saving, pension cap and safe series; `core_run` calls it and writes `arm` and the grid point into the run record (`Raw`) and the output labels. `account_table.py` uses the same builder. Tests: `legacy` bit equal (`test_legacy_digest` unchanged); a household run through `core_run` passes I1, the account identity and the ledger ties of 120c; the run record carries `arm`. Push.
- **Block 2: withheld outputs.** Under the household arm the M3, M12 and M13 outputs, and any other output that reads site 4 or 5, are replaced by a labelled `legacy_only` marker, never a number, and the output validator and the module-to-id table (`acceptance.md` V3-11) still cover `outputs.yml` exactly. Under `legacy` nothing changes. Tests: each withheld id under the household arm; no `legacy_only` value appears as a result; every other id is produced with the `household` label. Push.
- **Block 3: the output list for the author.** Run the household arm once at a stated scenario grid point (a smoke run, summary lines only) and write `docs/model-v3/household-arm-outputs.md`: every manifest id, one row each: produced, or withheld `legacy_only`, with the reason and the later brief that brings it back; the labels; the scenario grid point; the stand-in safe return. **Do not edit `outputs.yml`**: propose the manifest amendment as a diff inside the note, for the author's sign-off. **No revenue, fund or burden number in the note.** Change report; push; stop.
**Stop rule.** After three blocks, or a quarter of the budget left, push what exists and list the rest under Next. Print only summary lines; suites in the background, never piped.

## Touches
`model_v3/runner/runner.py` (net zero), `model_v3/runner/arm.py`, `model_v3/runner/out_burden.py`, `out_support.py` and the other `out_*` / `groups.py` files only where an output is withheld, `model_v3/out/` only for labels, tests (new `test_arm_switch.py`, additions), `docs/model-v3/household-arm-account/account_table.py`, `docs/model-v3/household-arm-outputs.md` (new), `docs/model-v3/architecture.md` (budget rows). Name any further file before editing it. Not `outputs.yml` (proposal only), the register, the pack, the kernel's tax code, `revenue.py` beyond a bug fix (report it), or the digest fixture.

## Acceptance criteria
- `test_legacy_digest` passes unchanged after every block; all suites pass.
- `arm` is in the run record and every household-arm output label; the default is `legacy`.
- A household-arm run completes through `core_run`: I1, the account identity and the ledger identities hold; `unpaid_B` is zero or reported as a model error with its inputs.
- M3, M12 and M13 (and any other site 4 or 5 output) are withheld under the household arm and labelled `legacy_only`; no `legacy_only` value is a result; the manifest/module table check still passes.
- `runner.py` stays at 360; R4 layering passes; diff within Touches.

## Checks to run
`test_legacy_digest` after each block; v3 suites in the background (never piped); the smoke run with summary lines only; `python -I pipeline/check_agent_docs.py`.

## Out of scope
Comparators on the account (the brief that returns M3, M12, M13), pension withdrawal, a saving gradient, validation against the 099r moments, any revenue, fund or burden result, editing `outputs.yml`, a register row for the safe return.

## Open questions
Which scenario grid point the smoke run uses (the agent states it, with the register rows it reads); how the class returns relate to the run's market path `g` (the agent states the rule it implements and why, reusing the account script's).

## Implementation notes
<!-- progress:start -->
- **Done:** none
- **Next:** block 0
- **Resume:** `git fetch origin '+refs/heads/*:refs/remotes/origin/*' && git checkout brief/121-w7-arm-switch`
- **State:** ready; not started
<!-- progress:end -->
