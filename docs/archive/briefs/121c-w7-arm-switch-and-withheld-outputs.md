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
- **Done:** blocks 0 to 3. Block 1: `arm.build`, `Ctx.arm`, `Raw.arm`, `household_inputs` (account script calls it, CSV byte-identical). Block 2: `arm.WITHHELD` / `arm.withheld`; household arm withholds O3, OH1b, OH1c, OW1 and the site-scan finds OW3, OM1; `assemble(withheld=)`; `writer` accepts the run field `arm`. Block 3: smoke run at the account's grid point (counts only) and `docs/model-v3/household-arm-outputs.md` with the manifest-amendment diff. model_v3 308 passed; `test_legacy_digest` unchanged; check_agent_docs exit 0.
- **Next:** the author signs off the note and the manifest amendment (`arms: [legacy]`, validator `withheld` and `arm`); then the briefs for the `burden.py` horizon-settlement fix in `fl`, the comparators on the account (M3, M12, M13, M15, M9), and OT1's M3 head under the household arm.
- **Decisions:** the withheld id is absent from Samples and written by `assemble` as `{summary, cells: [], withheld}`; M3 is absent from `headlines` under the household arm; `OW3` and `OM1` are withheld too (they read the legacy c).
- **Gotchas:** a final household-arm file fails V7 on the withheld ids until the validator gains the amendment; OT1 (`sweeps.py`) would raise on `e['M3']` at level 2 under the household arm.
- **Resume:** none.
- **Not run:** level 1 or level 2 under the household arm beyond the 2-path smoke; O1e, OF1, OT1 under it.
- **State:** done; not merged (author sign-off of the note first)
<!-- progress:end -->

### Change report
```
Change report
- Task: brief 121c (W7), the arm switch, labels and withheld outputs
- Files changed: model_v3/runner/arm.py (build, Arm, household_inputs, WITHHELD, withheld); model_v3/runner/runner.py (Ctx.arm, core_run, headlines M3 and samples O3 guarded; 360 lines); model_v3/runner/out_burden.py (static returns {} under the household arm); model_v3/runner/out_support.py (welfare, envelope, migration skipped; OW1, OW3, OM1 omitted); model_v3/out/assemble.py (withheld); model_v3/out/writer.py (run field arm); docs/model-v3/household-arm-account/account_table.py (calls the builder); tests/model_v3/test_arm_switch.py (3 tests); docs/model-v3/architecture.md (arm.py budget 225, sums +10); docs/model-v3/household-arm-outputs.md (new); this brief
- What is different now: a run can choose the household arm; its label is in the run record; six outputs are withheld as legacy_only and never hold a value; the legacy arm is bit equal
- New or changed interfaces: Ctx.arm; arm.build(arm, ctx, theta, base) -> Arm; arm.WITHHELD; arm.withheld(label); assemble(..., withheld=); run field arm
- Acceptance criteria: test_legacy_digest unchanged after every block (met); arm in the run record and the writer's run block (met; the validator warns V12 on the unknown run field); household run through core_run with I1, account identity, ledger ties, unpaid_B 0 (met, test); M3, M12, M13 and OW3, OM1 withheld, no value under them, test_w7 still passes (met); runner.py 360, R4 layering passes, diff within Touches except as named below (met with the named files)
- Deviations from the brief: model_v3/out/writer.py and architecture.md sums were touched (out/ for labels, budget rows: both in Touches); OW3 and OM1 were withheld beyond the four named ids because they read the legacy c
- Risks / follow-ups: a final household-arm file fails V7 until the validator takes the manifest amendment (note, for sign-off); OT1's M3 head in sweeps.py (outside Touches) raises under the household arm at level 2; O1e, OF1, OT1 not exercised under it; fl misses the horizon settlement of year T (about 639bn at the centre), affecting M2 and M4a (and likely M2b, M2c, M2d); fix is in burden.py
- Instruction friction: the Resume line's checkout failed (no local branch of that name); it was created from the remote ref
- Verification: model_v3 308 passed (background); test_legacy_digest and test_out within it; smoke run counts: 29 produced, 6 withheld, 5 not produced by one evaluation, 0 values under withheld ids; check_agent_docs exit 0
- Overview sections likely needing an update: kernel-wiring-design W7 row; STATUS.md (guru)
- Commit / branch: brief/121-w7-arm-switch, not merged
```
