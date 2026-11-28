# Run cost of model_v3 (brief 150c)

Timings: `model/studies/run-cost/timing.py` (wall seconds, best of 2, spec tau_m 0.5, k_ln 0.5, ratio 1.0, grid point median_mid, 2 cores, 7 GB, one process). Raw JSON: `run-cost/timing.json`. Block 1 only measures; nothing in the model changed.

## One evaluation

`ev(spec)` is `evaluate`: one `core_run` plus the `again` runs the groups ask for. It makes 5 `core_run` calls on both arms.

| paths | household | legacy | household/legacy |
|---:|---:|---:|---:|
| 20 | 8.9 s | 2.9 s | 3.0 |
| 200 | 18.5 s | 8.2 s | 2.3 |
| 1,000 | 76 s (RSS 2.0 GB) | 36 s (RSS 2.2 GB) | 2.1 |

The brief quoted 4.9 s (household) and 1.8 s (legacy) at 20 paths. This machine gives 8.9 s and 2.9 s; the brief's figures were probably taken on a faster machine or before 132c/133c. All projections below use this machine's numbers.

Cost is not linear in paths: at 20 paths it is already 8.9 s. About 8 s of it is fixed per evaluation (the year loop), about 0.07 s per path after that. Evaluations at few paths are the worst value.

## Cost by part (one evaluation, seconds)

`core_run` is the sum of its 5 calls. The groups' own `per_path` times include the `again` core runs they trigger, so the group rows overlap `core_run`; they are not additive.

| part | hh 20 | hh 200 | leg 20 | leg 200 |
|---|---:|---:|---:|---:|
| total | 8.5 | 19.2 | 3.3 | 8.5 |
| `core_run` (5 calls) | 6.6 | 16.5 | 3.0 | 7.4 |
| headlines | 0.01 | 0.09 | 0.01 | 0.10 |
| group revenue (incl. its core runs) | 3.8 | 10.3 | 2.4 | 5.7 |
| group burden | 0.07 | 0.58 | 0.07 | 0.61 |
| group support (welfare solves, M13) | 3.3 | 5.1 | 0.5 | 1.3 |
| group sweeps | 0.00 | 0.00 | 0.00 | 0.00 |
| not in `core_run` or headlines | 1.9 | 2.6 | 0.3 | 1.1 |

Reading: `core_run` is 78 to 86 % of an evaluation. The household arm's extra cost over legacy is in `core_run` (hook, lien, floor) and in the support group's welfare solves (3.3 s against 0.5 s at 20 paths). Groups burden and sweeps are negligible. `statics`: 0.02 s.

## Level 1 and O1e roots

| item | household | legacy |
|---|---:|---:|
| level 1, one schedule, 1,000 paths | 74 s | 36 s |
| O1e root, bracket check only (2 evals, no sign change) at 20 / 200 paths | 16.4 / 36.8 s | 5.4 / 14.6 s |
| O1e root with a sign change, about 12 evals | 12 x one evaluation | same |

`breakeven` evaluates both ends of [0, 15] first and returns nan when M1 does not change sign, so a root costs 2 evaluations or about 12 (2 plus the bisection to tol 1e-2: log2(15/0.01) is 10.5). Which roots bracket is not known before the run.

Legacy finding (not repaired, outside this brief): at 20 and 200 paths the O1e root on the legacy arm raises `ValueError: income_tax_gains: a rate of 1.0 raises 0.46, less than the target 0.53` from `solve_rate` in `core/support.py` at an end of the bracket. `run.py --arm legacy` would die in O1e the same way. Household does not.

## The smoke run

`python -m model_v3.run --smoke` (057c branch, 56a0a14): n1 = 50, n2 = 3 draws, n2p = 20, one point (median_mid), household. 783 s wall, 13 minutes, in which the run computed everything and then stopped at assembly: `every grid point failed: median_mid: DH1c ('S_low', 'transition', ...): point_and_r...` (the validator on 057c's branch; the message is cut by the script at 80 characters). The compute time is complete; the output file was not written. That failure is 057c's, not this brief's.

Split of the 783 s, by evaluation counts (a tornado is 1 + 2 x 5 read inputs = 11 evaluations per schedule, 3 schedules; level 1 at 50 paths is small):

| part | evaluations | seconds |
|---|---:|---:|
| tornado (n2p 20) | 33 | about 295 |
| level 1 (3 schedules, 50 paths) | n/a | about 10 (at 74 ms per path) |
| O1e (3 schedules x 4 roots) | remainder | about 480, about 54 evaluations, 4.5 per root |

The O1e share is inferred as the remainder, not timed separately. It implies most smoke roots had no sign change.

## Projection, full run, serial, this machine

Evaluations in the run are at n2p = 1,000 paths: 76 s each (household). N1 = 10,000, N2 = 200. Author decision 2026-11-23: O1e at `median_mid` only; the other four points carry level 1 and the tornado.

| part, per grid point | evaluations or paths | time |
|---|---:|---:|
| level 1, 3 schedules x 10,000 paths | 30,000 paths | 2,220 s (37 min) |
| tornado, 3 schedules x 11 | 33 evaluations | 2,510 s (42 min) |
| one point without O1e | | 4,730 s (79 min) |
| O1e, 3 x (1 + 200) = 603 roots | | |
| - every root has no sign change (2 evals) | 1,206 | 91,600 s (25 h) |
| - smoke-like mix (4.5 evals per root, inferred) | 2,700 | 206,000 s (57 h) |
| - every root brackets (12 evals) | 7,236 | 550,000 s (153 h) |

Full run, one-point O1e, one process: 4 x 79 min + 79 min + O1e = 6.6 h + 25 to 153 h, central 64 h, about 2.7 days. `accept.sh` runs it twice. Without one-point O1e the same five points would take 5 times the O1e figure.

Memory: 2 GB per process at 1,000 paths. Two workers on this machine fit (4 GB of 7).

## Parallel evaluation (blocks 2 and 3)

`model/model_v3/runner/pool.py`: `pmap(f, items, workers)`, an ordered map over forked processes; `workers` 1 is the plain loop (default), 0 one per core, N is N. `S.feasibility`, `S.tornado` and `S.breakeven_return` take `workers=` and make their independent units go through it: one evaluation per spec (map), one per (schedule, input, side) (tornado), one root per (schedule, draw) (O1e). Units are handed out one at a time. No model, register, kernel or `arm.py` code changed; level 1 is not parallelised.

**Same results.** `tests/model/model_v3/test_pool.py` compares serial with 2 and 3 workers to the last byte (floats by hex, arrays by buffer) for the map, the tornado and the roots on a noisy evaluator, and for the tornado on the model. `speedup.py` repeats the check on the household arm below: every row says identical.

### Speed-up, this machine (2 cores), household, 20 paths, `speedup.py`

| work | workers 1 | 2 | 4 | identical to serial |
|---|---:|---:|---:|---|
| tornado, one schedule (11 evaluations) | 74.4 s | 42.4 s (1.75x) | 40.3 s (1.85x) | yes, yes |
| O1e, one schedule, 7 roots (14 evaluations) | 97.2 s | 54.1 s (1.80x) | 48.9 s (1.99x) | yes, yes |

Two cores cap it at 2x; 4 workers on 2 cores add little. The tornado's 11 units over 2 workers are 6 + 5, which is why it sits under the roots. At 1,000 paths the per-unit work is 76 s against a fork and pickle cost of well under a second, so the efficiency should be at least what is measured here; not measured at 1,000 paths with more than 2 workers (no cores to do it on).

### Projection of the full run (one-point O1e, N1 10,000, N2 200, n2p 1,000)

Serial parts: level 1, 5 points x 37 min = 3.1 h (not parallelised). Parallel parts: the tornado, 5 x 42 min = 3.5 h, and O1e, 25 h (no root brackets), 57 h (smoke-like, inferred) or 153 h (every root brackets).

| machine | O1e 25 h | O1e 57 h | O1e 153 h |
|---|---:|---:|---:|
| this one, serial | 31.6 h | 63.6 h | 159.6 h |
| this one, 2 workers (1.85x measured) | 18.5 h | 35.8 h | 88.8 h |
| 16 cores, 32 GB, 14 workers (efficiency 0.9, 12.6x assumed; 2 GB each) | 5.4 h | 7.9 h | 15.5 h |

The 16-core line is an assumption from the 2-core efficiency, not a measurement. `accept.sh` runs the full run twice: double each figure.

### What is left

1. **The roots.** They are over 90 % of the run and each is a serial bisection of up to 12 evaluations, each of 5 `core_run` calls (about 80 % of an evaluation). Parallelism divides this by the worker count and no more; a faster root needs a cheaper evaluation (kernel) or fewer evaluations per root (a looser `tol`, a bracket from the previous root: both change the numbers or the method, so not done here).
2. **Level 1 is now the serial floor**: 3.1 h on any machine, 40 % of the 16-core central figure. It folds paths in chunks of 1,000 and the chunks are independent (30 units per point); `pmap` would take them. That is a change to `runner.py`, which is at its 360-line budget, and it was not asked: a follow-up brief.
3. **Grid points.** The five points run one after another and each parallelises inside. Running points side by side adds nothing once the workers are busy.
4. **Memory** bounds the worker count: 2 GB per worker at 1,000 paths.

### The switch in `run.py` (057c's file; not edited here)

`run.py` is not on main, so the switch is given as the change 057c makes (all keyword arguments default to serial):

```diff
-def run_point(ctx, inp, pt, named, man, n1, n2p, draws, seed, tol):
+def run_point(ctx, inp, pt, named, man, n1, n2p, draws, seed, tol, workers=1):
-    smp.update(osw.ot1(S.tornado(ev, named, {i: cp.reg[i] for i in cp.tier1}, R.reads(cp))))
-    smp.update(osw.o1e(S.breakeven_return(ev, named, R.RET['mean'], draws=draws, tol=tol)))
+    smp.update(osw.ot1(S.tornado(ev, named, {i: cp.reg[i] for i in cp.tier1}, R.reads(cp), workers=workers)))
+    smp.update(osw.o1e(S.breakeven_return(ev, named, R.RET['mean'], draws=draws, tol=tol, workers=workers)))
 ...
+    p.add_argument('--workers', type=int, default=1, help='processes for the tornado, the roots and the map: 1 serial (default), 0 one per core')
 ...
-    fmap, _ = S.feasibility(R.make_ev(c0, ...), S.grid(lv))
+    fmap, _ = S.feasibility(R.make_ev(c0, ...), S.grid(lv), workers=a.workers)
 ...
-            d, i = run_point(ctx, inp, pt, named, man, n1, n2p, draws, a.seed, 1.0 if a.smoke else 1e-2)
+            d, i = run_point(ctx, inp, pt, named, man, n1, n2p, draws, a.seed, 1.0 if a.smoke else 1e-2, a.workers)
```

## Findings for the author (none repaired here)

- The smoke run on 057c's branch (56a0a14) computes for 783 s and then fails at assembly on DH1c (`point_and_range`); see above. 057c's.
- O1e on the legacy arm raises from `solve_rate` at an end of the bracket (see above): `--arm legacy` cannot complete O1e.
- The household evaluation is 8.9 s at 20 paths here against 4.9 s in the brief.
- `test_budget` was failing on main: the housekeeping commit 472e88e added `runner/switches.py 200` to the budget block and not to the totals. The totals now include it (5,440 and 6,310 with `pool.py` 50 and 75 test lines); say if the reservation was meant to stay outside.

## Headline-only evaluation (151c, 2026-11-27)

**Change.** `make_ev(ctx, eps, seq=None, heads=False)`: with `heads=True` `evaluate` stops after `headlines(raw, ...)`, so one `core_run` and no output groups. `run.py` builds the tornado's and the O1e roots' evaluator with it; the feasibility map keeps the full one (it reads `e['sweeps']['of1']`, a group result). `tests/model/model_v3/test_heads_only.py`: every headline key equal to the last byte on both arms, 3 specs x 3 input settings.

**Setting.** 2 cores, `NPY_DISABLE_CPU_FEATURES=X86_V4` for every number below (169c is not on main; the variable set by hand), household arm, median_mid, spec tau_0 0.04, tau_m 0.5, k_ln 0.5, ratio 1.0; `model/studies/run-cost/heads_only.py`, 20 paths, best of two. Raw numbers: `heads-only-timing.json`.

| unit | full evaluator | headline-only | saving | result bytes |
|---|---:|---:|---:|---|
| tornado, one schedule (11 evaluations) | 100.7 s | 18.3 s | 5.49x | identical |
| one O1e root (tol 1.0) | 18.9 s | 3.4 s | 5.49x | identical |
| the `quick` run, 5 points, serial (one run each) | 4,193 s (70 min) | 2,182 s (36 min) | 1.92x | see below |

The 5.49x is five `core_run` calls (the 55 `run_lines` calls of 11 evaluations become 11) with the groups gone. The guru's estimate was 3 to 5x; the unit saving is a little above it.

**The `quick` comparison.** Before: main `6719d06`; after: this branch `504a248` (block 1's code); same machine, same setting, run one after the other. The two `outputs.json` (377,764 bytes each) differ in one line and in nothing else: `run_date` (`2026-11-26` before, `2026-11-27` after: the second run finished after midnight on the machine's clock). `diff` shows exactly that line; sha256 starts `4101cd34...` and `96275e68...`. By the brief's stop rule a failed byte comparison stops the block; this one is reported, not accepted: a strict comparison needs both runs on the same date (about 106 minutes for both again, or rerun the after run and read `run_date` aside, the author's choice). `accept.sh` has the same exposure: its `cmp` of two `quick` runs fails when the runs straddle midnight.

**Why the `quick` run saves only 1.92x.** At quick sizes (N1 1,000, 50 tornado paths) the run is: level 1, 3 schedules x 1,000 paths, 287 s per point = 1,437 s (5 points; unchanged, 66% of the after run); the feasibility map, 27 grid points x 11.8 s (full evaluator, 50 paths) = 319 s once; the tornado 5 x 33 x 2.2 s = 363 s (before: 5 x 33 x 11.8 s = 1,947 s); the O1e roots of the first point and the assembly (the remainder, about 60 s). Level 1 and the map do not use the headline-only evaluator and are most of what is left.

**Profile, top ten by own time, one tornado (20 paths).** Before / after (calls and seconds): `sum` 5.9M / 940k calls, 15.6 / 2.6 s; `household.apply_payment` 499k / 66k, 13.1 / 1.9 s; `household_step` 193k / 22k, 8.8 / 1.1 s; `kernel._div` 1.64M / 323k, 6.9 / 1.4 s; `kernel.assess` 119k / 23k, 6.5 / 1.3 s; `kernel._route_tax` 576k / 114k, 6.0 / 1.2 s; `arm._restart` 111k / 22k, 5.7 / 1.1 s; `kernel.add` 2.08M / 411k, 5.0 / 1.0 s; `revenue.run_lines` 55 / 11, 4.3 / 0.9 s; `arm.pre` 111k / 22k, 4.1 / 0.8 s. The same ten functions in the same order, each five times cheaper: the profile did not change shape, so what remains is the per-year household loop itself (152c) and the number of evaluations (153c).

**Projection of the full run (one-point O1e, N1 10,000, N2 200, n2p 1,000), serial, this machine.** The tornado: 5 x 42 min becomes 5 x 7.6 min = 0.6 h. O1e: 25 h, 57 h or 153 h (every root with no sign change, smoke-like mix, every root brackets) becomes 4.6 h, 10.4 h or 27.9 h. Level 1: 5 x 37 min = 3.1 h, unchanged. The feasibility map (not in the old table): 27 x 76 s = 0.6 h, unchanged. Total 8.9 h, 14.7 h or 32.2 h against 31.6 h, 63.6 h or 159.6 h before (the earlier table left the map out; with it they were 32.2 h, 64.2 h and 160.2 h): 3.6x, 4.4x and 5.0x. `accept.sh` runs the full run twice: double.

**What this says for 152c to 154c.** After this brief the largest shares of the full run are, in order: O1e (4.6 to 27.9 h; the root count is the lever: 153c), then level 1 (3.1 h, serial: 154c, `pmap` over chunks), then the per-year household loop under everything (152c: the burden and ledger loops shared, each evaluation is now one `core_run`). The feasibility map is a new candidate: it needs the `sweeps` group, so it is untouched here (a full evaluation is about five core runs, 11.8 s against 2.2 s headline-only at 50 paths; how many of them the group needs was not analysed). A map-only evaluator would take its 0.6 h down: a smaller prize than the other three.

## Level 1 through the parallel map (154c, 2026-11-27)

**Change.** `runner.level1(..., workers=1, cap=None)`: the chunks' paths are drawn in the serial order, then one unit per (chunk, schedule) goes through `pmap`: 3 units at quick size (one chunk of 1,000 paths), 30 per grid point at final size. The seed key is the chunk, never the worker, so a result does not depend on the worker count. The cap store (`support.capping`) is module state: a forked unit records its shortfall into its own copy, so each unit records into a local store and the records are merged into the caller's in (chunk, schedule) order, the first standing, as in the serial run. `accept.sh` passes `--workers W` to both `quick` runs, W = min(cores, (MemTotal GB - 2) // 3), and logs it.

**Setting.** 2 cores, 8 GB, `NPY_DISABLE_CPU_FEATURES=X86_V4`, household arm, median_mid. Raw: `level1-parallel-timing.json`; ledger row in `results/speedup/ledger.md`.

| unit | workers 1 | workers 2 | saving | result |
|---|---:|---:|---:|---|
| level 1, 3 schedules, 1,000 paths (`level1_3sched_1000`) | 327 s | 217 s (workers 0 = 2 cores: 216 s) | 1.51x | digest identical |

The brief's `level1_1sched_1000` is one unit at quick size (one chunk, one schedule): nothing to parallelise, so the measure is the three schedules of one chunk.

**Why 1.51x and not 2x.** Three units of equal cost on two workers: one worker runs two, the other one; the makespan is 2/3 of the serial time at best (1.5x). With four cores the same three units finish in one unit's time (3x at best); at final size 30 units balance over any core count. The fork and pickle cost was not measured apart; 1.51x is within 1% of the 1.5x the unit counts allow.

**Memory.** One level 1 unit (household, 1,000 paths) peaks at 3.0 GB (`pool.py` says about 2 GB; not corrected here). On this 8 GB machine two workers at 1,000 paths were OOM-killed (cgroup, `BrokenProcessPool`) in 2 of 5 attempts, and a `quick` run with `--workers 2` was killed at its fourth point after 1,060 s (the parent probably holds more by then; not analysed). So `--workers 0` is not safe here and `accept.sh` leaves 2 GB for the parent: W = 1 on this machine, 4 on a 16 GB 4-core runner. The `quick` figure with workers 2 cannot be stated from a completed run here; the three points that finished took 1,060 s including the 319 s feasibility map, against about 1,520 s serial (map plus three points of about 400 s): about 1.4x, an estimate.

**Byte checks.** (1) Level 1 at workers 1, 2 and 3 on the real model, 3 chunks: byte-equal (`test_pool.py`). (2) A unit that meets a shortfall in a forked worker reaches the caller's store, first chunk first, at workers 1, 2 and 3 (`test_pool.py`, fake evaluator). (3) `quick`, workers 1: main's code 2,319 s, this branch 2,412 s; the two `outputs.json` are byte-equal (same machine, same day, same numerics; validator PASS). (4) `smoke`, workers 1 against workers 2: the two files differ in one line, the run record's own `"workers": 1` / `2`; every number is equal. A parallel `quick` run is therefore never byte-equal to a serial one by construction; two runs at the same worker count are (as `accept.sh` compares).

**Projection.** Level 1 is 3.1 h of the final-size run (5 points x 37 min), serial in the old numbers. On four cores with 16 GB the 30 units per point give up to 4x (about 0.8 h); on this machine 1.5x to 1.9x at most (about 1.6 to 2.1 h). Not measured at final size; the figure to read is the Actions one (the accept job's first `quick` step: `accept.sh` logs `nproc`, memory and W).

**What remains.** On this machine memory, not cores, limits level 1 to about one worker. The next lever is the 3.0 GB per unit (the evaluation holds every group's per-path arrays at 1,000 paths); 152c shares the year loop and may cut it.


## The feasibility map runs only the OF1 group (186c, 2026-11-27)
The map read `e['sweeps']['of1']` and nothing else, but `evaluate` ran all four groups and their `again` core runs. `evaluate` and `make_ev` now take `only=` (group names; default all); `run.py` builds the map's evaluator with `only=('sweeps',)`. The OF1 group reads only `raw` (no `again`, so no extra `core_run`), and each group draws from its own `env.rng(name)` (`runner.py` `Env.rng`, a hash of the name), so skipping the others cannot change its stream.

Measured with `model/studies/run-cost/map_only.py` (household arm, `NPY_DISABLE_CPU_FEATURES=X86_V4`, 2 cores, best of 1; the map is the whole lever grid, quick size = 50 tornado paths):

| case | full evaluator | `only=('sweeps',)` | saving |
|---|---:|---:|---:|
| one map point, 20 paths | 8.4 s | 1.5 s | 5.5x |
| whole map, 20 paths, workers 1 | 236.9 s | 42.9 s | 5.5x |
| one map point, 50 paths | 12.3 s | 2.3 s | 5.4x |
| whole quick map, workers 1 | 328.7 s | 61.5 s | 5.3x |
| whole quick map, workers 0 (2 cores) | 174.0 s | 33.1 s | 5.3x |

The guess (about 330 s to under 100 s) holds: 329 s to 62 s. The results (points and OF1) are byte-identical in every case. What remains is the base `core_run`, the headlines and the OF1 retirement (`revenue.retire` per margin), about 19% of the old time.

## Projections after 151c, 154c and 186c (179c, 2026-11-28)

Basis: `results/speedup/profile-after-154c.md` (2 cores, 8 GB, `NPY_DISABLE_CPU_FEATURES=X86_V4`, household, one `quick` run per setting). This section replaces the projection tables above (150c to 154c) for planning; those stay as history.

### `quick`

| workers | wall | label |
|---|---:|---|
| serial (1) | 1,942 s (32 min) | **measured** here (level 1 1,465, tornado 352, map 59, roots 61, other 4) |
| 2 (`--workers 0`, 2 cores) | 1,210 s (20 min) | **measured** here (level 1 1.52x, the other parts 1.94 to 1.96x) |
| 4 | 954 to 1,335 s, median 975 s | **measured** on 4-core Actions runners (177c, three different CPUs); not measured on this machine (no 4 cores) |
| 14 | about 530 s (9 min) | **estimated**: level 1 is 3 units per point, so 98 s per point, 488 s for five; the rest (476 s) divided by 12.6 (90% efficiency) is 38 s |

Level 1 is the floor of a parallel `quick`: three units per point cannot use more than 3 workers. The author's 10-minute target (600 s) is met only at 14 workers, by estimate.

### Final run (N1 10,000, N2 200, n2p 1,000; one-point O1e), hours

Unit costs: level 1 = 30 units per point x 97.7 s (the `quick` unit time) x 5 points = 4.1 h serial (**estimated** from the quick measurement; 154c's note said 3.1 h from the old unit time, which 179c's `quick` run does not support). Tornado = 33 headline-only evaluations at 1,000 paths per point (1.42 s + 14.0 ms x 1,000 = 15.4 s each, fit from `scale.json`) x 5 = 0.7 h. O1e carried from the 151c section (4.6 h if no root brackets, 10.4 h smoke-like, 27.9 h if every root brackets); not re-measured here (the roots at quick size cost 61 s, which fits). Parallel divisors: 2 workers 1.52x (level 1, measured), 1.96x (other, measured); 4 workers 3.8x; 14 workers 12.6x (assumed, 30 units on 14 workers is 3 rounds, 0.41 h). Memory: 3 GB per unit at 1,000 paths, so 14 workers need 42 GB or more (a 16 GB machine holds 4).

| workers | level 1 | tornado | O1e 4.6 / 10.4 / 27.9 h scenarios, total run | label |
|---|---:|---:|---|---|
| serial | 4.1 h | 0.7 h | 9.4 / 15.2 / 32.7 h | level 1 and tornado **estimated** from measured quick units; O1e carried (estimated) |
| 2 | 2.7 h | 0.36 h | 5.5 / 8.6 / 17.8 h | **estimated**; speed-ups measured on `quick` |
| 4 | 1.1 h | 0.18 h | 2.5 / 4.0 / 8.6 h | **estimated** |
| 14 | 0.41 h | 0.06 h | 0.9 / 1.3 / 2.7 h | **estimated**, speed-up assumed |

`accept.sh` runs the final run twice: double each figure. No final-size figure here is measured; the speed-ups are measured at `quick` size only.
