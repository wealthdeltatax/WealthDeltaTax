# 126: The comparators on the account: M3, M12, M13, M15, M9 return under the household arm

- **Status:** ready
- **Author/date:** K. Ogata with the guru, 2026-11-22
- **Depends on:** 123c (merged); 122c (merged)
- **Read (block 0: the first two only):** (1) `docs/model-v3/kernel-wiring-design.md` section 3.6 (sites 4 and 5 and the consequence paragraph); (2) `docs/agents/code.md`. Later, by block: `model_v3/core/burden.py` (`free_path`, `m3`, `m3_today`, `m12`); `model_v3/core/support.py` (`system_run`, `_record`, the comparators); `model_v3/runner/arm.py` (`WITHHELD`, `WITHHELD_BY`, `HouseholdHook.account`, the untaxed path); `model_v3/runner/out_burden.py` and `out_support.py` (the withheld sites); `docs/model-v3/household-arm-outputs.md`.

## Goal
Bring back the outputs withheld as `legacy_only`: M3 and M12 (burden against the household arm's untaxed path), M13 (the comparators: stock tax, tax on gains, consumption tax, against the WDT), M15a/b and M9, each computed on the household account (saving S, holding gain CG, consumption C, the untaxed path) instead of the legacy `c`. Not like for like comparisons are never shown.

## Decisions (author, 2026-11-22)
- Every comparator reads its base from the account of the same line: a stock tax on the net-worth stock (pension included on the ONS basis), a tax on gains on CG, a consumption tax on C. The base each uses is written in the note.
- `burden.free_path` under the household arm is the hook's untaxed path (`T = 0` through the same step; design 3.6 site 4).
- The legacy arm does not move (`test_legacy_digest` bit equal).
- A comparator whose base the account cannot give (no held rate, no base) stays withheld, with the reason; it is not approximated with a legacy `c`.
- The withheld ids that return lose their `arms` entries in `outputs.yml` (author sign-off here, as for 122c); ids that stay withheld keep theirs.

## Blocks (one push each; `docs/agents/code.md`, Long builds; each block closes one output family)
- **Block 0:** progress block pushed.
- **Block 1: M3 and M12.** The household arm's untaxed path in `free_path`, `m3`, `m3_today`, `m12`; withheld markers removed for O3, OH1b, OH1c; tests (household `m3` equals the burden on the account path in a hand-computed toy case; legacy bit equal). Push.
- **Block 2: M13 and the comparators.** `support.system_run` and the comparators on the account's CG and C; OW1 un-withheld; tests (each comparator on a toy line against a hand calculation; the same revenue basis as the WDT line is stated). Push.
- **Block 3: M15 and M9, the manifest, the note.** OW3 and OM1 on the account where their base exists (otherwise they stay withheld, with the reason); the manifest `arms` entries removed for the ids that returned; validator and fixtures follow as in 122c; the note `docs/model-v3/household-arm-comparators.md` lists each id: returned or still withheld, the base used, the test. No revenue or burden number for the author. Change report; push; stop.
**Stop rule.** One block per family; if the budget runs short, push the families completed and list the rest under Next (the ids not returned stay withheld). Suites in the background, never piped.

## Touches
`model_v3/core/burden.py`, `model_v3/core/support.py`, `model_v3/runner/arm.py`, `model_v3/runner/out_burden.py`, `out_support.py`, `runner.py` only to drop a withheld id (net zero lines), `docs/model-v3/outputs.yml` (the `arms` entries of returned ids), `pipeline/validate_outputs.py` and the fixtures that follow the manifest version (report each), tests, `docs/model-v3/household-arm-outputs.md` and the new note, `docs/model-v3/architecture.md` (budget rows). Name any further file before editing it. Not the kernel, `revenue.py` beyond a bug fix (report it), the register, the pack or the digest fixture.

## Acceptance criteria
- `test_legacy_digest` unchanged; all suites pass.
- Each returned id is computed on the account with the base stated; each id that stays withheld has its reason in the note and keeps `arms: [legacy]`.
- A household-arm output file with the returned ids present and the others withheld passes `validate_outputs.py --final`.
- No legacy `c` is read under the household arm (a test scans the household path).

## Checks to run
`test_legacy_digest` after each block; v3, data and gate suites in the background; `python -I pipeline/check_agent_docs.py`.

## Out of scope
Pension withdrawal, a saving gradient, per-path regimes, new comparator designs, validation against moments, any result headline.

## Open questions
Whether M15 and M9 have a base on the account (the agent states it per id).

## Implementation notes
<!-- progress:start -->
- **Done:** blocks 0 to 3 (all ids on the account; nothing stays withheld)
- **Next:** none; merged to main
- **Resume:** n/a
- **State:** finished
<!-- progress:end -->

```
Change report
- Task: brief 126c, the comparators on the account: M3, M12, M13, M15 and M9 under the household arm
- Files changed: model_v3/core/burden.py, support.py (blocks 1 and 2: the hook passed to free_path, system_run, welfare, wdt_run); model_v3/runner/arm.py (`HouseholdHook.free`, `system`, `consumption`; `WITHHELD` now empty; 245 of 245); out_burden.py, out_support.py (`_record` under the household hook, `_migration`'s spend from C, the `old` gates removed), runner.py (Env.arm, net zero on withheld ids); docs/model-v3/outputs.yml (every `arms` and `arms_by` entry gone; version stage-A16-comparators-2026-11-22); tests/data/fixtures/outputs.fixture.json (regenerated by make_fixture.py, version only); tests/data/test_validate_outputs.py (V7 tested on a manifest that restores `arms: [legacy]` on OW3 and OM1); tests/model_v3/test_comparators.py, test_arm_switch.py, test_run_grid.py; docs/model-v3/household-arm-outputs.md; new docs/model-v3/household-arm-comparators.md; docs/model-v3/architecture.md (arm.py budget rows, block 2).
- What is different now: under the household arm every id is produced and none is withheld. M3, M12 (OH1b, OH1c, O3, OT1's head) on the untaxed path T = 0; M13 (OW1) on the account's CG and C with the opening net worth (pension included) for the stock tax; M15a/b (OW3) from the kernel rerun under the household hook; M9 (OM1) with the leavers' spend the account's consumption C = (1 - saving) x income instead of c x wealth. The legacy arm is bit equal.
- New or changed interfaces: `HouseholdHook.consumption()`, `HouseholdHook.system()`, `arm.WITHHELD == {}`; manifest has no `arms`.
- Acceptance criteria: test_legacy_digest unchanged (run after the final edit); all five suites pass (model_v3 324, data 96, gate 17, cards 8, hooks 87); each returned id has its base in the note, none stays withheld; a household file with every id present passes `--final` (test_a_household_file_with_every_id_present_passes_final); no legacy c is read under the household arm (tests set I-D14c to nan: M3, M12, M13, M15 and M9 finite).
- Deviations from the brief: (1) the manifest now has no `arms` entry at all, so the data tests that exercised V7 on OW3 and OM1 use a copy of the manifest with `arms: [legacy]` restored (the validator mechanism is kept and tested; the findings of those tests did not change). (2) test_run_grid's id assertion changed (OW3 and OM1 are now produced), as the brief says. (3) `arm.py` budget 245 (block 2) is used in full (245).
- Risks / follow-ups: the household arm ignores g, so the paths of one schedule are identical and the p10/p90 of OW1, OW3 and OM1 are degenerate until per-path regimes (128c). M15a and M15b are 0 in all 20 cells of the smoke run (the envelope never binds under the scenario's returns); the hand case shows it binds when wealth falls. M9's X is not comparable with the legacy X (different spend base).
- Instruction friction: none.
- Verification: test_legacy_digest, test_budget, test_run_grid; the model_v3, data, gate, cards and hooks suites; pipeline/check_agent_docs.py exit 0; hand cases (M15 toy 0.15, 0.12, 0.096, 0.0768; M9 spend 0.09 million).
- Overview sections likely needing an update: household arm outputs (all ids on the account; manifest without `arms`).
- Commit / branch: brief/126-comparators (merged to main)
```
