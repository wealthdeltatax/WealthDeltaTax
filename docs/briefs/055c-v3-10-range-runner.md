# 055: Model v3 V3-10: range runner

- **Status:** ready
- **Author/date:** K. Ogata with the guru, 2026-11-18
- **Depends on:** 053, 054
- **Read:** `docs/model-v3/architecture.md` 2.8, 3.1 to 3.3, 6.2 (N1 to N7) and 6.5; `docs/model-v3/drivers.md`; `docs/model-v3/tornado.md`; `docs/model-v3/stage-c-decisions.md` items 2, 6, 7; `docs/model-v3/acceptance.md` V3-10 row and section 4 (R3, R10).

## Goal
The two-level run, the schedule sweep, the tornado and the stress test, producing Samples.

## Decisions (author, 2026-11-18)
`architecture.md` approved (sections 8.1 and 9 as written); `acceptance.md` approved with Q1 to Q6 as proposed. v3 imports nothing from `model_v1/` or `model_v2/`. No file outside this brief's Touches is changed.

## Design
`runner/runner.py` (360 lines): level 1 at `N1` = 10,000 per schedule, level 2 at `N2` = 200 Latin hypercube draws of `N2P` = 1,000 paths on common random numbers, folded into the kernel's line axis in chunks of 1,000 paths; seed streams. `runner/sweeps.py` (300 lines): the feasibility map over the lever grid, the three named schedules by the confirmed rule, the tornado, break-even and negative-M1 share (`O1e`, `O1f`), CK1 and the bootstrap run. `runner/pool.py` (70 lines) only if the full run would exceed 60 minutes or K6 failed. Add the set-equality test between the drawn level 2 ids and the tier 1 list of `drivers.md` (R3), and the monotone check over every cell of the lever grid (R10).

**Shared interfaces, fixed before any stage starts** (a build brief never edits them; a mismatch is a question to the guru): the output file shape is `schema wdt-outputs/1` as `pipeline/validate_outputs.py` checks it and `docs/restructure/site/hooks.md` section 3 with the 030c rulings; the country pack format is `docs/model-v3/country-pack.md`; the id lists are `docs/model-v3/outputs.yml` and the module-to-id table of `architecture.md` 2.10; the Samples contract is `architecture.md` 2.9; the layers and import rules are `architecture.md` 5.1.

This is build stage V3-10 of `architecture.md` section 7. One session, one lane; the stage ends in a stop: tests pass, change report written, branch merged by the auto-merge rule. The stage's files are budgeted in `architecture.md` 6.1; a stage more than 15% over its budget reports it before the next starts.

## Touches
`model_v3/runner/runner.py`, `model_v3/runner/sweeps.py`, `model_v3/runner/pool.py`, `tests/model_v3/test_runner.py`, this brief's progress block.

## Acceptance criteria
- N1 to N7 pass; the same seed gives byte-identical `Samples`.
- The R3 set-equality and R10 grid tests pass.
- N7: the time of one 10,000-path schedule is measured and written to the change report; `pool.py` exists only if its trigger fired.
- `runner.py` at most 360 lines and `sweeps.py` at most 300.
- `git diff --stat` is limited to the Touches list.

## Checks to run
`pytest tests/model_v3 -q`.

## Out of scope
The writer (V3-11); the convergence test (V3-12); a final run.

## Open questions
Ask if N7 shows the full run would take over 60 minutes and K6 passed: the pool rule is the answer, but confirm the reference machine.

## Guru note, 2026-11-19 (after 054c)
`core/support.py` takes some inputs from the caller (054c gotchas): the distribution of declared alpha (M7e), consumption spend and its rate (the migration loss), the second asset's returns and the embedded-gain bands (M14), and the gains-tax realisation rate (M13). The runner supplies them from the register and pack: consumption from I-D14, the second asset's returns from `returns.csv` (`housing_tr`, `bond_tr`), embedded gain from I-T4e and realisation from the I-T5 rows. Map each to a row id in your report. If an input has no row (the likely one is the distribution of declared alpha: the register holds only the shift I-D5b), do **not** invent a value: stop and report to the guru, who writes a register brief. Same for any other input the runner needs and the register lacks.

## Implementation notes
<!-- progress:start -->
- **Done:** read the brief, architecture 2.8, 3.1 to 3.4, 6.2, 6.5, drivers, stage-c items 2, 6, 7, the V3-10 and R3/R10 rows of acceptance, `outputs.yml` for O1e, O1f, OF1, OT1, CK1, `levers.json`, and the interfaces of `revenue`, `burden`, `support`, `returns`. Checked the guru note's inputs against `registry/inputs.json` (291 rows) and the pack. No code written.
- **Next:** the guru's register brief for the missing row below; then build `runner.py`, `sweeps.py`, `test_runner.py`.
- **Decisions:** none taken.
- **Gotchas:** input-to-row map as far as it exists: consumption spend and rate = I-D14c (3.5%, 0.5 to 5); second asset returns = pack `returns.csv` `housing_tr` and `bond_tr` (mean and SD also at I-H6c to I-H6f, cross-correlations I-H6g to I-H6i); embedded gain = I-T4e (20, 35, 50 % of value; band wealth I-T4a to I-T4d); realisation of gains = I-T5e (all households, 0.9, 1.7, 1.7 % a year) and I-T5f (D10, 1.1, 2.1, 2.2); risk aversion = I-H5a (1.5). **Missing: the distribution of declared alpha (M7e, which feeds `support.declaration_curve`, `modal_alpha`, `tolerant_zone`, OD1 and O7).** The register holds only I-D5b (6.0 % of base, a shift of declared alpha), no shape, support or weights. Per the guru note I did not invent one. Also noted: I-D13e (Route B payment mode) is a text row and `load_register` returns None for it, so the runner would pass the mode `sale` as a kernel argument, not read it (the 054c reading); the guru may want a register value for it. The OT1 list has 40 inputs, of which I-D6a to I-D6p are incidence shares that only enter M4a through `burden.incidence`; I will map each of the 40 to a model argument when building.
- **Resume:** when the alpha-distribution row exists (low, central, high, unit and what the numbers mean: support points and weights, or a parametric form), rerun `/wdt-code do brief 055c` from this branch.
- **Not run:** everything; no code.
- **State:** blocked, NEEDS THE GURU (register brief for the distribution of declared alpha); not started
<!-- progress:end -->

### Change report
```
Change report
- Task: brief 055c, model v3 V3-10 range runner: stopped at the guru note's input check
- Files changed: this brief only (progress block)
- What is different now: nothing in the model; the missing input is named
- Acceptance criteria: none attempted
- Deviations from the brief: none; the brief's own rule (guru note 2026-11-19) says stop and report when a row is missing
- Risks / follow-ups: register brief needed for the distribution of declared alpha (M7e); optional: a value for I-D13e
- Verification: grep of the ids in core modules against registry/inputs.json (none absent); pack columns read
- Overview sections likely needing an update: none
- Commit / branch: brief/055-runner (pushed, not merged): NEEDS THE GURU
```
