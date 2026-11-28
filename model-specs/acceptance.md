# Model v3: acceptance plan (stage D1, brief 040g)

Status: approved by the author, 2026-11-18, with Q1 to Q6 as proposed (applied to `architecture.md` sections 0, 6.1 and 7). Written by the guru from `architecture.md` (approved 2026-11-18), `synthesis.md` section 4 (R1 to R11), `order.md` G1 and G2. Nothing is built or run here. The build briefs (D2) are written only after the author approves this file. Section 7 lists what the author must decide; the plan assumes the proposed answers.

Test ids (P1, K6, I1 and so on) are those of `architecture.md` section 6.2 and 6.3. A criterion is a command, a bound or a pinned number; "passes" means `pytest` exits 0 for the named tests.

## 1. The acceptance command

The gate checker (`model/tools/check_gate.py`, G1 of `order.md`) reads the one line below and runs it. It is the only line in this file of that form.

Acceptance command: `bash tests/model/model_v3/accept.sh`

`accept.sh` is written in stage V3-12 and runs with `set -euo pipefail`, so it exits 0 only if every step exits 0. Steps, in order:

| # | Step | Passes when |
|---|---|---|
| 1 | `python -I -m pytest tests/model/model_v3 -q -m "not converge"` | all stage tests of section 3, the rules tests (R4, R8, R9, R11) and the smoke test pass |
| 2 | `python -I -m pytest tests/model/model_v3/test_converge.py -q -m converge` | the convergence test of section 5 passes |
| 3 | `python -I -c "import sys; sys.path.insert(0, 'model'); from model_v3 import run; run.main(['--out', TMP])"` (provisional, starting sample sizes or larger) | exits 0 and the file validates |
| 4 | `python model/tools/validate_outputs.py "$TMP/outputs.json"` | zero errors in provisional mode |
| 5 | assertions on `$TMP/outputs.json` | every manifest id has an entry (R1); no cell is `null`; `run.fixture` is false; `run.seed` is 20261118; `run.paths` at least 10,000; `run.level2_draws` at least 200; `run.unfilled_paths` at most 5% of paths (Q3); `run.status` is `provisional` |
| 6 | run the same step 3 again into `$TMP2` and compare | the two files are byte-identical (R5) |
| 7 | grep checks of R6 (section 4) | each convention is in its module docstring and in `project/decisions.md` |

It never passes `--final`. The final run is the author's act (G2); acceptance proves the model could be run final, not that it was.

**Numerics path.** Every digest and pin in this plan (the legacy digest of section 3, the `test_groups` pin, the tripwire baseline) is held on one numpy code path: `NPY_DISABLE_CPU_FEATURES=X86_V4`, which switches off numpy's AVX512 `exp`, `log` and `pow`; the AVX512 and AVX2 results differ in the last bits and, through values that are zero in theory, in some counts (`results/169c-numerics/difference-report.md`). `run.py` (via `model_v3/numerics.py`), the model conftest, the tripwire and the Actions workflow set the variable; on the author's machine it must be set in the shell for anything else that computes a number the pins cover. The acceptance command itself needs nothing extra.

## 2. Policies

**Seed.** One master seed, 20261118, recorded in `run.seed`; streams are the five of `architecture.md` 3.1, in that order, new streams appended only. The convergence test uses four further seeds, fixed in the test: 20261119, 20261120, 20261121, 20261122. No module calls a global random function (test R5 of rules).

**Sample size.** Starting values `N1 = 10,000`, `N2 = 200`, `N2P = 1,000`. The convergence test may raise them, never lower them. The value in force is the default in `run.py` and is recorded in `run`; `--final` is refused below it. Raising a size is a change to `run.py` and a line in `decisions.md` (R6).

**Smoke test.** `python -I -c "import sys; sys.path.insert(0, 'model'); from model_v3 import run; run.main(['--smoke', '--out', DIR])"` with `N1 = 50`, `N2 = 3`, `N2P = 20` exits 0, writes `outputs.json` with `run.status` `provisional` and `run.paths` 50, and `validate_outputs.py` passes it. A second test renames one module file (in a copy of the tree) and a third breaks one import; each must make the smoke test exit non-zero (R5, "fail loudly").

**Run script.** `python -m model_v3.run [--paths N] [--seed S] [--out DIR] [--smoke] [--final]` as `architecture.md` 6.5. Tested by the smoke test and by acceptance step 3.

**Partial runs (`--parts`, 178c).** `--parts` takes a comma list from `level1,map,tornado,o1e` (default all four; `map` is required, because every part reads its named schedules). A subset is the same method on fewer parts, for the fast loop while variables change: the file carries `run.parts`, and the ids of a part not run are `{"cells": [], "not_run": "not_run_this_run"}` (`map` owns OF1 and CK1, `tornado` OT1, `o1e` O1e, `level1` every other id). The validator checks the requested parts only. A partial file is a development file: `--final`, `accept.sh` (step 5) and `check_gate.py` (G2) refuse it, and acceptance always runs the full default. A default run writes no `run.parts` and is byte-identical to the file before 178c.

**Stage stop.** Each build stage ends when its tests pass, its change report is written and its branch is merged by the auto-merge rule; the next stage does not start before (R7). Each stage reports its files' line counts against the budgets of `architecture.md` 6.1 (the test `test_budget.py` does the count); a file over its budget fails the stage, and a stage more than 15% over its budget in total reports it before the next stage starts.

## 3. Each build stage: stop and criterion

| Stage | Stop: these pass | Measurable criterion |
|---|---|---|
| V3-0 manifest and levers (guru) | script `tests/model/data` and a YAML check | `outputs.yml` carries A1 to A7; its `version` changed; every `by` is a map (script: no list-valued `by`); `levers.json` parses and holds the grid of `architecture.md` 3.3; `data/input-register/metrics.json` regenerated by `build_metrics.py` with exit 0; the fixture file of 030c validates |
| V3-1 scaffold and rules | the rules tests, run on the empty scaffold | each rule test fails on a seeded violation (import across a layer, a lazy import, a side effect on import, a country name, a file over budget) and passes on the clean tree; `test_budget.py` totals equal the 4,770 and 3,020 of `architecture.md` 6.1 |
| V3-2 pack loader | P1 to P7, P10 | ZZZ fixture pack loads with no code change (R11); a changed byte fails on sha256 naming file, row and column; the fixture pack hash is pinned |
| V3-3 UK pack | P8, P9 and the 038c scan | X1 holds within 1e-9; X2 holds within 0.01; the register row count equals the row count of `inputs.md` (the architecture's 269 is replaced by that count, Q6), `low <= central <= high`, `(J)` flags equal `inputs.md`; `pack_sha256` is pinned; scan hits zero |
| V3-4 schedule and kernel | S1 to S5, K1 to K10 | K8 identity to 1e-12 on the 70-point grid and on one case with `settle_delta` not zero; K6 and K9 to 1e-12; K3 exact to the pound |
| V3-5 returns | R1 to R7 | sample statistics pinned: n 117, arithmetic 4.742, geometric 4.420, SD 8.219, lag-1 0.303 (each to 0.001); 100,000-path mean, SD and lag-1 within 0.05, 0.05 and 0.02 of the inputs; level 2 band 3.41 and 6.07 within 0.02 |
| V3-6 base | B1 to B5 | band shares partition and equal the pack totals; `W_min` equals the lever ratio times the pack's median house price per adult |
| V3-7 revenue (statistic: mean over the 117 windows, not the median; as restated in `architecture.md` "Restatement": I1 = take equals v2's in every window at v2's fill year; I2 at v2's fill year; the fill-year difference is reported) | M1 to M7, I1, I2, I3 | I1: post-fill 10-year WDT take 7.34 within 0.02 points of GDP (patched refund); I2: between 6.34 and 7.36 with the model's refund, the difference written in the change report; I3: accounting identity within 5% of M1a; M1 equals its parts to 1e-12; a negative-M1 path passes unclipped. An I2 miss stops the build and goes to the author |
| V3-8 burden | D1 to D6 | hand cases exact to 1e-12; DH1c equals the pack decile table |
| V3-9 support | U1 to U6 | hand cases exact; S1 off equals S1 absent |
| V3-10 runner | N1 to N7 | same seed gives byte-identical `Samples`; tornado rows in descending absolute effect; named schedules follow the choice rule on a toy map; N7 measures one 10,000-path schedule and writes the time to `run`; if the full run would exceed 60 minutes or K6 failed, `pool.py` is added and tested |
| V3-11 output layer | W1 to W7 | each of V1 to V12 has a failing input that the validator rejects; W7: the module-to-id table covers `outputs.yml` exactly (39 outputs and one check); P10 and P90 equal `numpy.percentile` on a known array |
| V3-12 run script, smoke, acceptance | smoke tests, `accept.sh` itself | `bash tests/model/model_v3/accept.sh` exits 0 on the whole tree; it exits non-zero when any one of five seeded breakages is applied (a failing unit test, a changed seed, a missing manifest id, a `null` cell, a non-identical rerun) |

Tests P8 and P9 (listed under `pack` in `architecture.md` 6.2) are assigned to V3-3, since they need the UK pack.

## 4. Requirements R1 to R11

| Req | Criterion | Where tested |
|---|---|---|
| R1 manifest | Every id in `outputs.json` is in `outputs.yml` (an unknown id raises, W6); every manifest id has an entry (step 5); every output has a non-empty `element:` (script in V3-0) | W6, W7, acceptance step 5 |
| R2 metric register | Every manifest `metric` id exists in `data/input-register/metrics.json` (V3-0 script); C.1 uses TW(1) as denominator (U1) | V3-0, U1 |
| R3 parameter file | Every register id the model reads exists with low, central, high and a unit (P9); every tier 1 input of `drivers.md` is drawn at level 2 (a set-equality test in V3-10 between the drawn ids and the tier 1 list); register rows that no module reads are counted and printed by acceptance, and fail it only if they are tier 1 or tier 2 rows | P9, V3-10, step 1 |
| R4 layering | The `ast` import-graph test of `architecture.md` 5.1 passes; the output layer imports no `core` and no `runner`; a function-level import fails | rules tests (V3-1), rerun in step 1 |
| R5 reproducibility | Seed recorded; same inputs give a byte-identical file (step 6, W5, N1); renaming a module or breaking an import makes the smoke test fail | smoke tests, step 6 |
| R6 convention log | The three conventions (arithmetic basis, refund is tau times loss, envelope resets at death) are each named in the docstring of `returns.py` or `kernel.py` and have a dated entry in `project/decisions.md` (grep, acceptance step 7) | step 7 |
| R7 tests travel | A test file exists for each core module, runner and output module; each stage's change report records its tests passing before the next stage began; nothing under `model_v2/` or `model_v1/` is imported (grep) | step 1, stage reports |
| R8 no side effects, no orphans | The subprocess import test (`python -B -I`) finds no change in environment, working directory or tree; no top-level function without a caller or test | rules tests |
| R9 size | `test_budget.py`: every file within its budget, `out/` smaller than core plus runner, totals 4,770 and 3,020 | rules tests |
| R10 progressive schedules | S2 and S3; a test in V3-10 runs the monotone check over every cell of the `levers.json` grid and fails on any non-progressive cell | S2, S3, V3-10 |
| R11 country pack | Scan over `model_v3/**/*.py` returns zero hits outside the allowed `country` handling; the ZZZ pack loads with no code change | V3-1, V3-2 |

## 5. Convergence test

`tests/model/model_v3/test_converge.py`, marked `converge`, runs through the runner and the summary code, not through the file writer. Level 1 only except C3. S_central, short horizon (O1 and O3 in their own units; O2 and O4a overall).

| # | Test | Passes when |
|---|---|---|
| C1 | five seeds (the master and four more) at `N1` = 10,000 | the spread (max minus min) of the mean, P10 and P90 of O1, O2, O3 and O4a is at most the limit for that output and statistic in `tests/model/model_v3/c1_limits.json`, in the output's unit; the limits are measured seed noise (`model/tools/c1_noise.py`, `results/converge/c1-noise.md`, brief 187c): q times the standard deviation across seeds at `N1`, q the 99th percentile of the range of five draws; the test lists every output and statistic that fails |
| C2 | the master seed at `N1` = 20,000 against 10,000 | the mean of each of the four moves by at most 0.05 |
| C3 | level 2 at `N2` = 400 against 200 (the master seed) | P10 and P90 of the level 1 mean of O1 move by at most 0.10 |
| C4 | tornado at two seeds | the top three inputs for M1 are the same, in the same order |

A failure raises the size in `run.py` (never lowers it), reruns, and records the new value in `decisions.md`. A failure that doubling does not fix stops the build and goes to the author. The thresholds are proposals (Q2); 036r supports 0.1 points on toy statistics only.

## 6. How this closes G1

G1 of `order.md` holds when `architecture.md` and this file exist, `project/briefs/done/011g-model-v3-design.md` exists, and the command of section 1 exits 0. The brief 011g retires when D2 is approved. A change to `outputs.yml`, `data/input-register/inputs.json` or the pack after an accepted run does not undo G1 (G2 is the check that does).

## 7. Questions for the author

Each has a proposed answer; this file assumes it.

**Q1. Two files not in the architecture.** `accept.sh` and `test_converge.py` are new files in stage V3-12. *Proposed:* add both to V3-12's files and raise its test budget by 90 lines (30 for the shell script, 60 for the convergence test), so the test total is 3,020; the guru edits `architecture.md` section 6.1 and 7 once. Otherwise V3-12 would break its own file list.

**Q2. Convergence thresholds.** Spread limits for C1 measured from seed noise (187c; before it, a guessed 0.15 on every output and statistic, loosened from 0.10 by the author, 2026-11-27), 0.05 on doubling and 0.10 on level 2 (section 5). *Proposed:* as written. Tighter costs run time; looser lets the ranges the papers quote move in the first decimal.

**Q3. Unfilled paths.** Step 5 fails if more than 5% of paths do not fill by year 90 (`architecture.md` 3.4). *Proposed:* 5%. A larger share means the short window is not a property of the central design and the author should see it before a run.

**Q4. Time.** The full run has a 60-minute rule for `pool.py`; acceptance runs the full run twice (steps 3 and 6) and the convergence test, so it may take several times that. *Proposed:* no time cap on `accept.sh` itself; N7 records the measured time and the reference machine is whichever machine runs it, named in the run record.

**Q5. Acceptance includes a full provisional run.** *Proposed:* yes (step 3), so that "model accepted" means the model has produced a complete file, not that its unit tests pass.

**Q6. Register row count.** `architecture.md` P9 pins 269 rows; `011g` says 274 and `order.md` G3 says 269 and 70 `(J)` rows. *Proposed:* P9 compares the register's row count to the count read from `inputs.md` at test time, and does not pin a number. Say if you want a pinned value.

## 8. Checks run

| Check | Result |
|---|---|
| Every build stage V3-0 to V3-12 has a stop and a criterion | section 3, 13 rows |
| R1 to R11 each have a criterion | section 4 |
| Smoke test, seed and sample policy, convergence test and run script specified | sections 2 and 5 |
| One acceptance command, named once | section 1 |
| Not run | any test or run: nothing is built |
