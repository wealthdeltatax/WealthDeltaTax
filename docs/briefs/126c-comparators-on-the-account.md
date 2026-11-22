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
- **Done:** blocks 0, 1, 2. Block 1: M3, OH1b, OH1c and OT1's M3 head on the household arm (`HouseholdHook.free`, per-line `free_path`, `Env.arm(base)`). Block 2: OW1 (M13) on the account: `support.system_run`, `solve_rate`, `welfare` and `wdt_run` take a `hook`; `HouseholdHook.system(kind, rate, G, payer)` runs the stock tax (opening net worth, pension included), the tax on gains (CG) and the consumption tax (C) on the account, paid from the non-pension classes (what they cannot cover is not paid); the WDT line's terminal wealth is units plus pension; the household arm runs the kernel on one path (it ignores g); `arm.WITHHELD` is OW3 and OM1; manifest `arms` removed for OW1.
- **Next:** block 3 (M15 and M9: state per id whether the account gives a base; manifest, validator and fixtures, the note `household-arm-comparators.md`, change report).
- **Decisions:** M3's denominator is the run's positive net change in wealth, saving included, as under legacy. `Env` has a field `arm(base)` (layer 3.5 cannot import arm.py). The comparators and the WDT are over the first generation (G = 30), no deaths, as legacy. `arm.py` budget 245 (now 242).
- **Gotchas:** data and model_v3 suites cannot run in one pytest session: `run_suites.py`. Pushing needed `--force-with-lease` once (the branch was rebased onto main after block 0).
- **Resume:** `git fetch origin '+refs/heads/*:refs/remotes/origin/*' && git checkout -B brief/126-comparators origin/brief/126-comparators`; last block pushed: 2.
- **Not run:** block 3.
- **State:** in progress; block 2 pushed
<!-- progress:end -->
