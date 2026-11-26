# Split final run: partial files and the exact merge (182c)

Design only; no code was written or run for this note. Written 2026-11-26 against `main` at 86038f0. Seams are named by function, with the line numbers of that commit for the reader (154c and 178c will move them).

## Summary of the decisions

1. **Units:** one `plan` job (feasibility map, the three named schedules), one `point` unit per grid point (level 1 and tornado together, never split further), and O1e roots in batches of 25 draws of one schedule, plus one small `o1e-point` unit (the three point roots and the end values). At 200 draws: 1 + 5 + 24 + 1 = 31 compute jobs and a merge job.
2. **Draws:** generate all `n2` draws in every O1e shard and slice `[a:b]`; the header carries a hash of the full draw table, and the merge checks it.
3. **Partials:** a `point` partial holds the point's *assembled* document (the unsplit run assembles per point too), not raw per-path samples; an `o1e` partial holds raw roots as hex floats. This departs from the brief's "raw samples before `reduce`" for a measured reason (item 3).
4. **Merge:** `main` becomes plan, units, merge, and the unsplit run is those same steps in one process. There is one assembly code path because there is one code path.
5. **Proof:** smoke size, two points, split versus unsplit, byte for byte; shuffled input order; one shard rerun. Pinned by `tests/model/model_v3/test_split_run.py`.
6. **Workflow:** plan, then two matrix jobs, then merge. With 4 workers per hosted job: about 1.6 h (no root brackets) to 7.4 h (every root brackets), 3.0 h at the smoke-like mix, against 64 h serial now. Concurrency on the Free plan is 20 jobs (read from GitHub's documentation, below).
7. **`--final`:** untouched. `--size final` is not `--final`.

Three findings the brief did not expect (details where they arise): `SIZES['final']` has **0 O1e draws**, not 200 (item 1); `workers` is written into the output file, so two runs that differ only in worker count differ in bytes (item 4); the shortfall record `cap` is lost for evaluations that run in pool workers (item 4).

## 1. Units of work and their seams

**What the unsplit run does** (`run.main`, run.py:79-117): `S.feasibility` over the whole lever grid at central inputs on the first point's arm (run.py:96); `S.choose` (97); `draw_theta` (99); then per point `run_point` (62-77): level 1 (`R.level1`, 67), the tornado `S.tornado` (69) and, at the first point only (`be`, 70), `S.breakeven_return` and the end values (72-73); then `scenario_range`, `mark_no_payer`, the O1e fix-ups, the run block, `wr.write_outputs` (108-116).

**Grid size** (`levers.json`): 3 tau_m x 3 k_ln x 1 tau_0 x 3 ratios = 27 points, so the feasibility map is 27 evaluations at `n2p` paths.

**Unit costs.** One household evaluation at 1,000 paths is 76 s on the 2-core measuring machine (`results/run-cost/run-cost.md`). Hosted runners are slower: the quick run of the accept job (170c) took 89 min on a hosted runner against about 65 min computed from the same cost model on this machine, so the planning factor is **1.4** (one comparison, approximate; 183c's first calibration run replaces it). Costs below are hosted, serial, unless stated.

| unit | work | evaluations | hosted, serial | 2 workers (1.85x measured) | 4 workers (2.5x, unmeasured) |
|---|---|---:|---:|---:|---:|
| `plan` | feasibility map, 27 grid points | 27 | 48 min | 26 min | 19 min |
| `point` | level 1 (3 schedules x 10,000 paths, serial, 52 min) + tornado (33 evaluations) | 33 + level 1 | 111 min | 83 min | 75 min |
| `o1e` root | one bisection | 2 to 12 | 3.5 to 21 min | | |
| `o1e` batch of 25 draws | 25 roots, `pmap` over roots | 50 to 300 | 1.5 to 8.9 h | 0.8 to 4.8 h | 0.6 to 3.6 h |
| `o1e-point` | the 3 point roots and the end values | about 6 to 40 | 11 to 64 min | 6 to 35 min | 4 to 26 min |

Only the tornado and the roots go through `pmap` (level 1 is serial: run-cost.md, "What is left" 2). The 2-worker speed-up is measured on 2 cores; the 4-worker figure is an assumption (a 4-vCPU hosted runner is probably two cores with two threads each, so 2.5x rather than 3.4x), to be measured by 183c.

**Which roots bracket is not known before the run** (run-cost.md): a root costs 2 evaluations when M1 does not change sign on [0, 15] and about 12 when it does. The batch size is set by the worst case, not the mean.

**O1e batch size: 25 draws of one schedule.** The hosted cap is 6 hours per job (GitHub, "Limits in GitHub Actions"). The planning limit is 5 hours, which leaves for set-up, install and a margin of one hour. Worst case (all 12 evaluations) per root is 21 min serial; at 2 workers 25 roots take 4.8 h, at 4 workers 3.6 h. 25 is the largest round number that fits at 2 workers. At 200 draws: 8 batches per schedule, 3 schedules, 24 batches.

**`SIZES['final']` has 0 O1e draws** (run.py:19: `final=(R.N1, R.N2P, 0, 1e-2, 5)`; `R.N2` = 200 is defined and unused there). The brief and run-cost.md assume 603 roots (3 x (1 + 200)). With 0 draws the run does the 3 point roots only and the O1e batches vanish (the design handles both; the numbers in item 6 show both). This is the author's to rule (open question 1): run.py:109 and the 2026-11-23 ruling "range over draws `not_run_this_run` at 0 draws" suggest 0 was deliberate for quick, and may not have been meant for final.

**Whether the level 1 and tornado of one point may be separate shards (the guru's question): no.** A point shard is 75 to 83 min (hosted, 2 or 4 workers), a fifth of the cap, and its raw per-path samples would be the large thing to move (item 3). Splitting would buy nothing and cost an artifact. The tornado's 33 units are independent and could be split later if a point ever exceeds the cap; the seam is `S.tornado` (sweeps.py:117), whose units are `(schedule, input, side)`.

**Cost of a failed shard:** the shard's own time and nothing else; shards share no state and their partials are files. Point shard: at most about 1.4 h. O1e batch: 0.6 to 4.8 h by the mix. `plan`: 19 to 26 min but it blocks everything after it, so a failed plan is the cheapest to rerun and the most visible. A rerun of failed jobs on the same run keeps the partials of the jobs that succeeded (item 6).

## 2. Draws must not depend on the split

`draw_theta(rng, ctx, ids, n)` (runner.py:107-126) takes every row's draws from one generator in sequence: `level2_draw` first (three Latin hypercube permutations of `n`), then one `rng.permutation(n)` and `rng.random(n)` per further id. Draw `i` of a row depends on the permutation of the whole `n`, so a shard cannot compute draws `a..b` by calling with `n = b - a`: that would be a different Latin hypercube.

**Decision: every O1e shard calls `draw_theta` with the full `n2` and slices `[a:b]`.** The cost is milliseconds (a few hundred normal quantiles). The stream is `st['level2_draws']` of `rt.streams(seed)` (returns.py:28-30), spawned from `SeedSequence(seed)` in a fixed order, so a fresh `streams(seed)` in each process gives the same generator state. The shard must not use any other stream first: `level2_draws` is drawn only here.

The header holds `draws_sha256`, the SHA-256 of the full table (ids in `ctx.tier1` order, values as float64 bytes). The merge checks that all O1e partials carry the same hash and, because it also holds `n2`, that the batch ranges tile `[0, n2)` exactly once.

**Test (pins this):** `test_draw_slices`: for `n2` = 7 and ranges `[0:3], [3:5], [5:7]`, the concatenated slices equal the full table to the byte; and a negative check showing that `draw_theta(..., n=3)` differs from the first three of `n=7` (so nobody "optimises" the call later).

The other streams are untouched by the split: level 1 draws `st['level1_paths']` in chunks of 1,000 (runner.py:320-330), each point creating its own `streams(seed)` (run.py:65), so every point sees the same paths in any order; the tornado and O1e use `st['tornado_crn']` for `eps` (run.py:68), regenerated identically in every shard that needs `ev`. The `Env.rng` seeds depend on `(run entropy, chunk or draw key, name hash)` only (runner.py:167-169), never on advance state, so units are pure functions of their inputs (pool.py header). This is the property the whole split rests on; `test_pool.py` already pins it for worker counts.

## 3. The partial files

**Departure from the brief, with the evidence.** The brief asks for raw samples before `reduce`. The unsplit run does not carry them across points: `run_point` already assembles each point (`asm.assemble`, run.py:77) and `scenario_range` combines the *assembled* documents (run.py:29-43, 108). So the per-point document is exactly the object the cross-point step reads, and the merge needs nothing else from level 1 and the tornado. Raw per-path samples would be large: the manifest has 1,305 per-path cells per point once OF1's 5,832 are excluded (OF1 is `pending`, run.py:23, 110), so at 10,000 paths about 104 MB of float64 per point, about 290 MB as hex text; five points would exceed the 500 MB artifact storage of the Free plan (GitHub, "Limits in GitHub Actions": Free 500 MB, not raisable). The assembled document of a point is about 0.3 MB (the whole five-point quick file is 378 KB).

**Where raw values do cross a shard boundary: O1e roots only.** Those are floats and are written as hex floats (`float.hex`, exact round trip).

**Format.** UTF-8 JSON, sorted keys, one indent, no timestamps, no CPU name, no wall time, so a rerun of a shard gives the same bytes. Time, CPU model and cores go in a sidecar `<unit>.meta.json` that the merge never reads.

Header (every partial):

| field | content | merge checks |
|---|---|---|
| `schema` | `wdt-split-partial/1`, `kind` (`plan`, `point`, `o1e`) | equal schema; kinds as expected |
| `size`, `seed`, `arm` | as run.py | equal |
| `n1`, `n2p`, `n2`, `tol` | the effective sizes after overrides | equal |
| `points` | the ordered list of grid points of the run | equal (this fixes the canonical order) |
| `git_sha` | `git rev-parse HEAD` of the job | equal: shards from different commits are refused |
| `inputs` | SHA-256 of the manifest, `inputs.json`, `levers.json`, `inputs_used.json`, and `pack_sha256` | equal |
| `numerics` | the `NPY_DISABLE_CPU_FEATURES` value, numpy and Python versions, and a probe hash (exp, log, pow of 100,000 fixed values: the informational step of the workflow already computes it) | equal |
| `plan_sha256` | hash of the `plan` partial the shard read | equal |
| `draws_sha256` | the full draw table (o1e kind; also the `o1e-point` unit) | equal |
| `unit` | `{point}` or `{schedule, a, b}` | not compared: it is the identity |
| `workers` | how many processes the shard used | **not checked** (results are the same to the last bit, `test_pool.py`) |

Everything is compared except the unit identity and `workers`, as the brief says (all but the point and the batch).

Body by kind:

- **plan:** `named` (the three specs, hex floats), `feasibility` (per grid point: labels, F1, M2, M4a by horizon, hex floats; for audit, and so OF1 can be built later), `chosen_from` (the point whose arm it was).
- **point:** `doc` (the assembled outputs of the point), `info` (`unfilled_paths` by schedule), `cap` (`{kind: [reached, target]}`, hex floats), `failed` (the 80-character message, or null; exactly the `ValueError` rule of run.py:103-104, in which case `doc` is null).
- **o1e:** `roots` as `[schedule, draw_index or null, hex]`, `cap`, `ends` (end values at 0 and 15 for a schedule with no point root, only in the `o1e-point` unit), `error` (a `ValueError` message or null).

## 4. The merge

A module `model/model_v3/split.py` (new; 183c) with `plan`, `unit` and `merge`, and `run.py` reduced to arguments: `--plan`, `--unit KIND:ID`, `--merge DIR`. **The unsplit run becomes `plan`, then every unit in canonical order, then `merge`, in one process, with the partials passed in memory after one trip through the file encoding.** There is then one assembly path, not two that are tested to agree, and "byte-identical" reduces to: the encoding round trip is exact (hex floats, JSON of already-rounded floats), the draw slicing is exact (item 2) and the units are pure (pool.py). `run_point` is split at two seams the code already has: the `be` block (run.py:70-73) becomes the `o1e` and `o1e-point` units, and the lines after it (74-77) stay in the `point` unit.

**Every place the unsplit path computes something across points or across the pieces of a point, and where it lives in the merge:**

| unsplit computation | line | in the merge |
|---|---|---|
| feasibility map and `choose` | 96-98 | the `plan` unit; shards read `named`; no shard recomputes it |
| `draws` | 99 | each `o1e` shard (item 2) |
| `info = info or i` (first surviving point's level 1 record) | 105 | merge: first point in canonical order with `failed` null |
| `ends = ends or x['ends']` | 105 | merge: the `o1e-point` unit's `ends` (first point only) |
| `tg` (targets, `shortfalls` from `cap`) | 105 | merge: per point, in canonical order, from `cap` (below) |
| the O1e roots at the first point and `osw.o1e(roots)`, or the 0-draw form `np.full(3, r)` (run.py:72) | 72 | merge: assemble `{'O1e': ...}` from the o1e roots with the same function, `asm.assemble` for that id, and place it in the first point's `doc` before `scenario_range`; the function is shared with `run_point`, not copied |
| `scenario_range(docs)` | 108 | merge, called as is on the point documents in canonical order |
| `mark_no_payer(outs)` | 108 | merge, as is |
| the O1e fix-ups `NO_SIGN`, `NOT_RUN_RUN` | 109 | merge, as is |
| `PENDING` ids (OF1, CK1) | 110 | merge, as is |
| the run label, `targets`, `met`, `points`, `failed`, `o1e` block | 111-113 | merge |
| the run block, `run_date`, `wr.run_block`, `wr.document`, `wr.write_outputs` with the validator | 114-116 | merge, the writer unchanged |

**Rounding order.** `asm._round` (12 significant digits, assemble.py:62-63) is applied inside `assemble`, per point, before `scenario_range` takes min and max across points. The merge reads the points' already-rounded documents and so does the same.

**The `cap` record and the "first record stands" rule.** `U.capping` records `{kind: (reached, target)}` with `setdefault` (support.py:144-162): the first record stands, level 1 running first. In the split, the `point` partial holds the cap of level 1 and the tornado; each `o1e` partial holds the cap of its own roots; the merge applies the point's, then the `o1e-point`'s, then the batches' in canonical order (schedule order, then `a`), each with `setdefault`. That reproduces the unsplit order. **Finding (not repaired, outside this brief):** an evaluation that runs inside a `pmap` worker writes to the worker's copy of `cap`, which the parent never sees (pool.py forks; `_CAP` is a module global). With `workers > 1` the tornado's and the roots' records are lost; with `workers = 1` they are kept. Whether that can change `targets` in a real run is not known (level 1 at central inputs probably records every kind first). 183c measures it at smoke size (workers 1 versus 2 against the same file) and, if it differs, the proof is against `--workers 1`, and a repair is a separate brief.

**`workers` is written into the output file** (run.py:113, `workers=a.workers`), so two runs that differ only in worker count are different files, though the model results are identical. The merged file must equal the unsplit file, so the merge takes `--workers` (default 1) for the label and the proof uses the same value on both sides. Proposal (open question 2): stop writing `workers` into the file; it is not a result.

**`run_date`** is `datetime.date.today()` (run.py:114), taken at the end. The merge takes `--run-date` (default today), and so does the unsplit run, so the proof can compare bytes without patching the clock.

**Refusals (all before any output is written, none repaired):** a header field that differs; a missing unit; two partials for one unit whose bytes differ (a rerun that does not reproduce is a defect to see, not to average); a batch range that does not tile `[0, n2)` per schedule; an `o1e` partial with an `error` or a failed first point: the unsplit run raises the `ValueError` inside `run_point`, which fails the whole point (run.py:103-104), and then crashes at `outs['O1e']` if the first point is the one that failed. The merge refuses with the message instead of a `KeyError`; that is the one deliberate difference from the unsplit behaviour, and it is on a path that has no valid file.

**What could still make the merged file differ from the unsplit file.** Float summation order across batches is the one the brief names, and the design removes it rather than controls it: no float is summed across shards. Level 1 and the tornado are never split, so their means, percentiles and sums are computed over the same arrays in the same order as before. The O1e cells use `np.nanpercentile` over the roots (`osw.o1e`, out_sweeps.py:50-58): a percentile is a sort, not a sum, and the merge concatenates the roots in draw order anyway. What remains: (1) a different numpy or CPU dispatch between shards (header check on versions and the probe hash; the forced `X86_V4` path of 169c and 170c holds on three runner CPUs so far); (2) the `cap` order above; (3) `workers` and `run_date` in the file; (4) a shard rerun on a different commit (header `git_sha`).

## 5. The proof

**What 183c must show**, on a runner, at smoke size with two points (`--point median_mid --point max_mid`, 50 paths, 3 draws), the smallest run that crosses a point boundary and has O1e draws:

1. The unsplit file (`run.py`, `--workers 1`, a fixed `--run-date`).
2. The split run: `plan`, the two `point` units, the `o1e-point` unit and the `o1e` batches (batch size 2 draws, so 2 batches per schedule), `merge`. `cmp` with 1: identical.
3. The same partials merged with the input list in a different order, and with the O1e batches *executed* in reverse order: identical.
4. One shard rerun (an `o1e` batch, then a `point` unit): the rerun partial is byte-identical to the first, and the merge is identical.
5. Refusals: a header mismatch (a changed seed in one partial), a missing batch, a duplicate unit with different bytes, a range gap: each refused with a message and no file written.

Time: about 31 min unsplit on a hosted runner (the smoke job takes 24 min for one point, plus a second point's level 1 and tornado), the same again for the split run, plus the reruns: about 75 minutes. It goes in its own manual job (`run_split_proof`), not in `fast`.

**The pin:** `tests/model/model_v3/test_split_run.py`, in two parts. *Fast* (no model run; part of `fast`): the draw slices (item 2); partial encode and decode round trip, hex floats, bytes stable across a rerun; the header refusals and the tiling check on synthetic partials; the merge over synthetic point documents equals `scenario_range` called directly in every order of the input list. *Slow* (`-m split`, not collected by default and not in `fast`): items 1 to 4 above on the model. The smoke test's marker pattern in `test_smoke.py` is the model for it.

## 6. Workflow

Today `run_final_size` is an input that nothing reads (workflow lines 24-27). Proposed jobs, all on `ubuntu-latest`, each with the same install and numerics step as `accept`:

```
plan   (1 job; outputs: matrix JSON of units from n2 and the batch size)
points (matrix: the 5 grid points, needs plan)
o1e    (matrix: 'point' unit + 24 batches, needs plan; none when n2 = 0 except 'point')
merge  (needs points and o1e; downloads partial-*; writes outputs.json; validates)
```

Each unit job runs `python -I ... run.py --unit ... --workers 4`, then `actions/upload-artifact` of `partial-<unit>.json` and its meta file with `retention-days: 14`. `strategy.fail-fast: false`, `timeout-minutes: 350` (the cap is 360). `merge` runs `cmp`-free: it only merges and validates. No job passes `--final`; the run refuses it, and `--size final` is a different thing (a size, status provisional). A guard test in `tests/model/model_v3` reads the workflow text for the substring `--final` outside a comment.

**GitHub's limits, read from its documentation** (Limits in GitHub Actions; Supported runners and hardware resources): 6 hours per job; **20 concurrent jobs on the Free plan** (40 Pro, 60 Team, 500 Enterprise; the guru's 20 is right); at most 256 matrix jobs per workflow run; 500 MB artifact storage on Free; public repositories get **4 vCPU, 16 GB** on `ubuntu-latest` (private: 2 vCPU, 8 GB) and standard runners are "free and unlimited" on public repositories. This repository is public (checked with the API), so 4 workers at 2 GB each fit.

**Wall time of the final run** (hosted; list-scheduled on 20 concurrent jobs; `plan` first, then the 5 point jobs and the o1e jobs together, then `merge`, which is minutes). From the unit costs of item 1:

| O1e draws and root mix | jobs | 2 workers | 4 workers | longest job (4 workers) |
|---|---:|---:|---:|---:|
| 0 draws (`SIZES['final']` as it is) | 1 + 5 + 1 + merge = 8 | 1.9 h | 1.6 h | 1.3 h |
| 200 draws, no root brackets (2 evaluations each) | 32 | 2.0 h | 1.6 h | 1.3 h |
| 200 draws, smoke-like (4.5 evaluations per root, inferred) | 32 | 4.0 h | 3.0 h | 1.3 h |
| 200 draws, every root brackets (12 evaluations) | 32 | 10.0 h | 7.4 h | 3.6 h |

(0-draw row: plan, the points and the 3 point roots, no batches.) For comparison the serial figure on the 2-core machine is 6.6 h plus 25 to 153 h of O1e (run-cost.md): 32 to 160 h. At the central mix the split run is about 3 hours of wall time on 4-vCPU runners and 4 hours on 2, by a factor of about 20 to 50 against one process. Total job time is 21 to 123 h by mix; it costs nothing on a public repository. The wall time in the last row is above 6 h only because more than 20 jobs queue behind the 20 slots, which is one reason to leave the batch at 25 draws and not lower. The estimate rests on two unmeasured factors (the hosted-to-local factor 1.4 and the 4-worker speed-up 2.5); 183c's calibration run replaces both.

**Reruns.** "Re-run failed jobs" in the Actions UI reruns only the failed matrix jobs on the same commit and keeps the partials of the others. `upload-artifact@v4` artifacts are immutable per run, so a unit that must run again after it succeeded needs `overwrite: true`; the design sets it.

## 7. Never `--final`

Nothing here changes `run.py:87`: `--final` is refused and the split adds no path to it. The merge writes `status: provisional` through the same `wr.run_block` call. The workflow has no input for it; the guard test of item 6 keeps it so.

## Open questions for the author

1. **O1e draws at final size.** `SIZES['final']` says 0 (run.py:19), the brief and run-cost.md say 200. With 0 the final run is about 1.6 h on hosted runners; with 200 it is 1.6 to 7.4 h and the O1e range is a computed number instead of the marker `not_run_this_run`. Proposal: decide in 181c; the design serves both, and the final-size run should use 200 if the 2026-11-23 ruling "range over draws `not_run_this_run` at 0 draws" was about quick only.
2. **`workers` in the output file.** It makes files differ with no change in results. Proposal: 183c stops writing it (a run-block label change; the validator does not read it, to be confirmed by 183c) so the proof does not need a fixed `--workers`.
3. **The `cap` loss in pool workers.** Proposal: 183c measures it at smoke (workers 1 versus 2); if `targets` differ, a separate brief makes the pool return the record. Not repaired here.
4. **Batch size.** 25 draws of one schedule. Proposal: keep, and change it to 20 if 183c's calibration shows the hosted-to-local factor above 1.6 or the 4-worker speed-up below 2.
5. **The merge rereading level 1 from a cache (the guru's question).** Not needed: nothing in the merge reads level 1 samples, only the assembled point documents. Proposal: no cache.
6. **Per-point sharding of level 1 (30 chunk units per point, `pmap`).** It would shorten a point shard from 75 to about 35 min, and it is a change to `runner.py`, at its budget (architecture.md budgets block). Proposal: not in 183c; the point shard is far inside the cap.
7. **The proof's runtime (about 75 min).** Proposal: manual dispatch input `run_split_proof`, run once per change to `split.py` or `run.py`, not on every push.

## Stage plan for 183c

Files: `model/model_v3/split.py` (new: plan, unit, merge, encode and decode of partials); `model/model_v3/run.py` (arguments, the `be` block lifted out of `run_point`, `--run-date`; check the budget block in `model-specs/architecture.md`, the budget file count and `run.py`'s line allowance first); `model/model_v3/runner/sweeps.py` (`breakeven_return` takes a schedule and a draw range, nothing else changes); `.github/workflows/model-checks.yml`; `tests/model/model_v3/test_split_run.py`; `project/agents/agent-code.md` and `model-specs/acceptance.md` (the unit list). No model arithmetic, no manifest change.

| stage | work | checkpoint (measured, not stated) |
|---|---|---|
| A | `split.py` encode and decode, header, refusals; the fast tests of item 5 on synthetic partials; `draw_theta` slicing test | the fast tests pass locally after `git clean -fdx`; tripwire PASS |
| B | lift the `be` block and the point steps out of `run_point` and `main` into `unit` and `merge`, with `main` calling them; `--plan`, `--unit`, `--merge`, `--run-date` | all existing suites pass; **the unsplit smoke file is byte-identical to the smoke file before this stage** (same date), proving the refactor changed nothing |
| C | the split proof at smoke size on the machine: items 1 to 5 of the proof | `cmp` identical in every case; refusals refused; noted with times |
| D | the workflow: `plan`, `points`, `o1e`, `merge`, the inputs, the `--final` guard; the `run_split_proof` job | the proof job green on a hosted runner (run id, CPU model); workflow lint by `gh api` dispatch of the smoke case; no job passes `--final` |
| E | the calibration run: one `point` unit and one 25-draw `o1e` batch at final size (`--size final`), timed, to replace the 1.4 and 2.5 factors | the two measured times written into this note; the batch size confirmed or changed; nothing merged before the author reads them |
| report | change report in the brief, progress block, push | |

Stop and report if the stage B smoke file differs from the one before the refactor by a byte (the refactor changed behaviour), if the proof differs in any case (find the cause before anything else), or if the calibration shows an O1e batch over 5 hours.

## Sources

[Limits in GitHub Actions](https://docs.github.com/en/actions/reference/actions-limits); [Supported runners and hardware resources](https://docs.github.com/en/actions/reference/runners/github-hosted-runners). Code: `model/model_v3/run.py`, `runner/runner.py`, `runner/sweeps.py`, `runner/pool.py`, `runner/out_sweeps.py`, `core/returns.py`, `core/support.py`, `out/assemble.py`, `out/writer.py` at 86038f0; `results/run-cost/run-cost.md`; `levers.json`; the Actions run 45803742165 and the runs of 170c for the hosted timings.
