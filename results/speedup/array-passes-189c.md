# Fewer array passes in the level 1 year loop (brief 189c): stop note

**Result: no change applied. No model file is touched.** Each step was tried and stopped at the brief's rule (stop when the next costs more than it saves); the micro-tests are in `model/studies/run-cost/array_pass_micro.py`.

Setting: 2 cores, 8 GB, `NPY_DISABLE_CPU_FEATURES=X86_V4`, household, main `cc3c844`, same spec and seed as 179c. Before-files (bench.py hashes and times) in `/tmp` of the session; the figures are below.

## Before (best of 2, 1,000 paths)
`core_run` 14.9 s; headline-only evaluation 17.5 s; full evaluation 91.4 s (179c measured 15.7 s and 93.7 s: this machine's run-to-run spread is 5 to 10%, so a gain under about 7% cannot be seen here). `eval_hh_20` 9.09 s, `eval_leg_20` 2.15 s, `level1_1sched_1000` 103.4 s; hashes `059139aee5e6`, `d19b6b99445f`, `8337b2022b1b`.

## Step 1: `builtins.sum` (536,000 calls, 12% of own time) -- tried, reverted
Callers (200-path profile, own seconds of 3.2 s in `sum`): `apply_payment` 0.60, `household_step` 0.51, `arm._n` 0.43, `kernel.family_true` 0.39, `assess` 0.32, `_refund_cash` 0.22, `arm.pre` 0.21, `_restart` 0.15, `post` 0.13, `_pay` 0.10, `revenue._value` 0.06, `burden._val` 0.06: twelve callers, none above 19%.

Tried: a helper `asum` (left-to-right add, skips the `0 +` first pass) at 12 hot sites in `household.py`, `kernel.py`, `arm.py`, `revenue.py`, `burden.py` (about 50 lines changed, 0 added to any budgeted file's total except the 1-line import). Identity: `eval_hh_20` and `eval_leg_20` hashes equal (byte-identical). Speed: `eval_hh_20` 9.09 to 9.36 s (+3%, the helper's Python overhead at 20 paths); at 1,000 paths `core_run` 14.9 to 17.0 s, full evaluation 91.4 to 96.2 s (within the spread, no gain seen). Micro-test: 4 arrays of 14,000 elements, `sum` 14.8 and 16.6 us, `asum` 14.7 and 11.2 us in two runs (the machine is noisy): at most about 0.1 to 5 us of 15, and the 12% own time of `sum` is the numpy adds inside it, which stay. Expected gain at most about 2 to 4% of level 1; not measurable here, so not applied. (Sign of zero: `0 + -0.0` is `0.0` where the helper gives `-0.0`; it did not move a hash.)

## Step 2: `where` chains and `asarray` -- measured, not applied
- `_div` as `np.divide(a, b, out=zeros, where=b > 0)` against `np.where(b > 0, a / np.where(b > 0, b, 1), 0)`: byte-identical; 2.9 to 2.3 us at 280 elements (-22%), **64 to 71 us at 14,000 (+11%, slower)**. At 1,000 paths the compares and selects are memory- and branch-bound, so fusing the passes does not pay; it pays only in the 20-path case, where it is 0.6 us per call of about 150,000 calls per evaluation (about 0.1 s of 9 s).
- `asarray` of values already arrays: 0.04 us a call, 1.03 million calls, about 0.04 s per evaluation: not worth a line.

## Step 3: `burden.m2` and `_cash` (5.7 s and 5.1 s own at 1,000 paths) -- measured, not applied
They run once per output over the whole (year x path x line) array, not per year. The masks in `m2` (`w0 > 0` twice, `net > 0`, the `where`s) rewritten with one mask and `(wt * net) * net` for `wt * net ** 2`: 10.9 to 10.2 ms (-6%) on a 100 x 1,000 x 12 array, and **not byte-identical** (the product is associated differently), so it needs the author's tolerance (`Asks`); a 6% gain on a part that is under 12% of level 1 (about 0.7% of `quick`) is not worth one. Not asked for.

## Stop note and next target
- Left, with gain and difference: `asum` (0 to 4%, byte-identical, not measurable here); `_div` by `divide(where=)` (-22% at 20 paths, +11% at 1,000, byte-identical: useful for the small 24% only, about 0.1 s of 9 s per evaluation); `m2` rewrite (-6%, differs in the last bit).
- What this says: at 1,000 paths the cost is the number of full-length passes the model needs (3.58 million wrapped calls per evaluation, 202 per simulated year), and the bytewise-identical rewrites of single operations remove about 1 to 4% at most. To change the time by more than the noise the number of years-times-passes must fall, which is the shared year loop (152c: each `core_run` walks the loop twice) or a structural change (skipping work for lines that cannot pay), neither byte-identical by construction to be assumed. Next target: **152c first**, measured by its first step as the brief says: if the two loop walks are the same work, 152c removes about half of every `core_run`'s step cost, both at 1,000 and at 20 paths; nothing in this brief needs it first.
- `quick` projection from the 179c shares: none applied, so 1,942 s serial and 1,210 s on 2 cores stand.
