# 092c: V3 group interface: give the output groups what they read

- **Status:** ready
- **Author/date:** K. Ogata with the guru, 2026-11-20
- **Depends on:** none (084c, 055c merged). Blocks 085c, 086c, 087c, 088c (they resume after this merges).
- **Read:** `AGENTS.md`, `docs/agents/code.md`, `docs/model-v3/architecture.md` 2.8, 2.9, 5.1, 6.1; `model_v3/runner/runner.py` (`Raw`, `core_run`, `evaluate`, `level1`, `level2`, `samples`), `groups.py`, the four `out_*.py` stubs, `tests/model_v3/test_groups.py`; the stop reports in `docs/briefs/085c` to `088c` (on branches `brief/085-v3-revenue-outputs`, `brief/086-work`, `brief/087-support-outputs`, `brief/088-sweep-pack-outputs`; read with `git show`).

## Goal
Four group briefs stopped for the same reason: `per_path(raw, again)` gives a group none of `ctx`, `theta`, the pack, a seeded rng, or the payer record. Widen the interface once, in `runner.py` and `groups.py`, so the groups can be written. No output is built here and no number changes.

## Decisions (author, 2026-11-20)
The guru confirmed this scope after the four stops. Manifest A12 and the rows I-T3q and I-D14h (091g) are merged: this brief does not touch the manifest or the register.

## Design
1. **`Env`**, a frozen dataclass in `runner.py`: `ctx`, `theta` (the inputs of this evaluation, so a level 2 draw's values), `pack` (`ctx.pack` if that is where it lives), `lam` (`lam_C`, `lam_D` as `core_run` builds them, fractions), and `rng(name)`: a numpy Generator that is deterministic for (run seed, chunk, name) and differs between chunks. It must not consume or reorder draws of the run's own rng: every existing digest (`test_groups.PIN` and the runner pins) stays byte-identical. Derive it from the run rng's `bit_generator.seed_seq` (spawn) or from the seed and chunk index, your choice; say which.
2. **Signature:** `per_path(raw, env, again)` for every group (stubs, `evaluate`, the tests). `again(over, full=False)`: `full=True` takes the receipts from `revenue.run_lines` (B1a to B1d are non-zero only then), cached per (spec, full).
3. **Static cells.** A group may define `static(env)` returning `{output id: {(horizon, by, line): array}}` for outputs that do not depend on paths or schedules (DH1a, DH1b). `samples` puts them in with schedule `None`, same checks as other cells (id in the manifest and in the group's `IDS`, no doubled owner), and only for ids the manifest marks `once_not_per_schedule`. Optional: a group without `static` is unchanged.
4. **Tests.** `test_groups.py` asserted every group's `IDS == ()` and an empty-group digest: replace the first with "IDS are manifest ids and no two groups share one", keep the digest test for the empty groups that remain empty at this point (a monkeypatched empty group stays the check), and add: `Env.rng` is reproducible and chunk-distinct; `again(over, full=True)` gives non-zero `B1a`; a static cell reaches `samples` with schedule `None`; a static id that is not `once_not_per_schedule` raises.
5. **Sweeps are not in this brief.** `out_sweeps` will expose plain functions the run script calls (088c); leave `per_path` and `cells` as they are.
6. **Budgets.** `runner.py` 360 (now 322), `groups.py` 40 (architecture 6.1 already raised, taken from `sweeps.py`, now 280). Stay inside; if not, stop and report.

## Touches
`model_v3/runner/runner.py`, `model_v3/runner/groups.py`, the four `model_v3/runner/out_*.py` (the stub signature only), `tests/model_v3/test_groups.py`, `tests/model_v3/test_runner.py` (only if a call site needs the new signature), this brief's progress block. Nothing in `core/`, `docs/model-v3/`, `registry/`.

## Acceptance criteria
- `per_path(raw, env, again)` everywhere; `Env` has the five members above.
- Every existing digest and pin is byte-identical; `pytest tests/model_v3` passes (208 at the time of writing, plus the new tests).
- Budgets met; `python pipeline/run_suites.py` passes all suites.
- The four new tests in Design 4 pass and each fails when its rule is removed.

## Checks to run
`python pipeline/run_suites.py`; `python -m pytest tests/model_v3 -q`.

## Out of scope
Building any output, the sweep functions, `sweeps.py`, the manifest, the register, `core/`.

## Open questions
The implementer asks rather than guesses. If `ctx` does not hold the pack, say where it lives and add it to `Env` without changing `ctx`.

## Implementation notes
<!-- progress:start -->
- **Done:** `Env` (ctx, theta, pack, lam, rng; plus `seq` and `key` that feed `rng`) in `runner.py`; `per_path(raw, env, again)` in `evaluate`, `groups.py` docs and the four stubs; `again(over, full=False)` cached per (spec, full); optional `static(env)` per group, run by `statics` (level 1 once, level 2 per draw) and stored by `samples(by_schedule, ids, once, static)` with schedule None, only for ids in `once`. `context(..., once=())` and `Ctx.once` carry the manifest's `once_not_per_schedule` ids. Tests: `test_groups.py` 60 lines (budget 60), 4 rules tested, each fails when its rule is removed (checked by mutation: chunk key, name hash, `full` ignored, `once` check, schedule None).
- **Decisions:** `env.rng(name)` is `default_rng(SeedSequence(entropy=seq.entropy, spawn_key=(*seq.spawn_key, *key, hash(name))))`, from the run stream's `bit_generator.seed_seq` (level 1: key = chunk index; level 2: key = draw index). It spawns nothing and draws nothing, so no digest moves. The pack lives in `ctx.pack`; `Env.pack` points at it, `ctx` unchanged. With no `seq` given, `evaluate` uses `SeedSequence(0)`.
- **Gotchas:** (1) The suite is 206 tests, not 208 plus new: I folded 084c's four tests into five (the `IDS == ()` assert became "manifest ids, none shared"; the static tests share one) to stay at `test_groups.py` 60. (2) A level 2 static cell is the mean over paths of each draw's static array, like every other level 2 value. (3) `static` is not called for a group without it; no group defines one yet. (4) 085c to 088c branches carry the old stub signature: they rebase onto this.
- **Next:** 085c to 088c resume.
- **Resume:** none.
- **Not run:** a full level 2 (no group defines `static`).
- **State:** done; merged to main; ready to retire.
<!-- progress:end -->
