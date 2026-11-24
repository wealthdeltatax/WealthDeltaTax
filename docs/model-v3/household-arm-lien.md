# The household arm: the pension-secured lien (brief 132c)

Status: block 3 of 132c, 2026-11-22. The lien carries the class-payment case (`min_mid`). The kernel-cap case (`median_high`) is not carried and waits for the author's ruling (the stop rule). No headline number is in this note. Units: millions of pounds per adult, real, unless stated; the ledger receivable is in billions.

## The rule as built

- A line's WDT that its non-pension classes cannot pay is not taken from the pension in life. It becomes a deferred balance `PL` against the pension, shown as debt in the account and not a receipt of the year.
- **Deferral rate.** `PL` accrues at the kernel's `r_def` (the Route B lien's rate), read from the book. The kernel default is 0.0 and no register row sets one, so the lien is real-zero-interest in every run here; the run label says so. Nothing was invented.
- **Settlement** at a death and at the horizon: from the positive non-pension classes pro rata, never beyond their net total; then a one-off draw on the pension (the only time it is drawn); what is still unpaid stays in the lien and in `unpaid_B` (an alarm, expected zero).
- **Draw rule used.** The draw is capped at the pension balance, not at what the heir would receive: the lien is a claim on the pension, and the brief left the heir's share open. Under this rule a draw can take the whole pension and leave the heir none of it. The author rules on the limit.
- **Ledger.** The lien is a receivable of the public ledger (`ledger['rec']`: balance, new, accrued, settled, written off; billions; six phases). The year's cash receipts exclude new lien and include settlement, so `sum(rc) + new - settled = assessed`; `dL = receipts + return - payout` by class holds with the receivable apart; both to 1e-9 (test, `min_mid` at threshold ratio 0.25, a lien from year 61 settled at deaths and in year 100). `M1a` and the fund read cash receipts; with no lien the adjustment is exactly zero.
- A lien on a line with no units left (the 127c floor) is written off and recorded as `wo`. It is zero in every run here.

## Results (20 paths; the arm has no spread: paths move only the fund)

Files: `household-arm-run/lien_checks.csv`, `lien_lines.csv`, `lien_alarms.csv`, from `lien_rerun.py`.

| Point | I1 | Account residual (max) | `unpaid` (max) | `unpaid_B` (max) | Ledger tie (max) | Shortfall lines counted | Lines with a lien |
|---|---|---|---|---|---|---|---|
| `min_mid` | holds | 1.6e-11 | 0 (127c: 1.1e-02) | 1.3e-01 (as 127c) | 6.3e-13 | 280 (127c: 300) | 2 (D4, D5) |
| `median_high` | holds | 1.9e-11 | 0 | 1.4e-01 (as 127c) | 2.3e-12 | 3,000 (as 127c) | none |

**Where the lien arises, `min_mid`.**
- **D4:** first in year 61, an unpaid tax of 0.0108. The line is in non-pension debt (-0.084 at the largest balance), so nothing settles from the classes. The balance is carried 29 years to the death settlement and reaches 0.386 in year 89 against a pension of 0.522 (74% of it). The settlement is 0.419 in all, all from the pension; nothing is left unpaid.
- **D5:** an unpaid tax of 0.0250 in year 95, in the year of a death; it is created and settled in the same year from the pension (0.0250), so no balance is carried at a year end.
- The figures are for the instance (phase and path) with the largest balance; D4 carries a lien in 40 of the 120 phase-path instances and D5 in 20.

**Not carried (updated by 133c).**
- The kernel-cap case is now carried. `Book.cap_cb` (default None, today's behaviour: the excess goes to the kernel's `unpaid_B`) hands the excess to the household hook, which adds it to the lien `PL` and to `PK`, the part the kernel never moved. The kernel's pension is the hook's pension net of `PK`, the units are untouched, so I1 holds; settlement takes the total from the classes and then the pension (the hook's gross pension balance is the draw base). The ledger reads the part of `new` that the kernel never moved (`xnew`) for its cash line.
- `median_high` (20 paths), before 133c and after: lien on 0 lines before and 11 after (D1 to D10b; D2 carries it for one year); `unpaid_B` that comes from the kernel's cap, 0 path-phases after (the counts before were 3,000 shortfall lines at 132c); `shortfall_lines` 3,000 before and 2,560 after, all of it the floor alarm below. `min_mid`: the kernel-cap excess on D4, D5 and D6 is carried too (80 shortfall lines, all floor alarm). I1, the account identity (1.9e-11) and the ledger ties (2.3e-12) hold at both points; `unpaid` is 0. Every lien is settled from the pension (the classes of these lines are empty by construction); none is left unpaid.
- **Still failing, reported separately (127c, not removed here):** the floor alarm. A line whose units are all zero cannot take the year's saving, so the floor records it. After 133c it is the only source of `unpaid_B` and of the shortfall lines: `min_mid` D4 (year 61) and D5 (year 78); `median_high` D10a from year 70 to D1 in year 97, the same amounts as in 127c. The 133c rerun logged it as 1,740 line-years at `min_mid` and 26,640 at `median_high` (20 paths over the phases). The cause is that the kernel cannot create units from a zero balance, which this brief does not change. **Update (137c):** a dead line with a positive saving now restarts from it (`HouseholdHook._restart`): the floor alarm is 0 at `median_high` (20 paths) and at the three market-path points (200 paths); `min_mid`'s 1,740 line-years (negative saving on zero units, D4 and D5) remain. See `household-arm-i1-floor.md`.
- Per-path returns (`run_grid.py --market-paths --paths 200`, `cap_lien/checks_paths_200.csv`), `unpaid_B` path-phases before (the brief's counts) and after: `median_mid` 2,776 to 375, `max_mid` 446 to 26, `median_low` 6 to 0. I1, the account identity (2.6e-11) and the ledger ties (2.9e-11 at most) hold at all three; `unpaid` is 0. I did not split the remaining path-phases into floor and kernel cap at these three points (done only for `min_mid` and `median_high` above).
- Files: `household-arm-run/cap_lien/` (`lien_checks.csv`, `lien_alarms.csv`, `lien_lines.csv`, from `lien_rerun.py --paths 20`). No headline number is read.

## Unchanged

The three passing grid points `median_mid`, `max_mid` and `median_low`, and the legacy context, at 1,000 paths: `grid_results.csv` and the checks rows byte-identical (md5) to a run of the same script on `origin/main` before this brief. The 14-line account and ledger CSVs regenerated with an empty `git diff`. `test_legacy_digest` and all four suites pass (`model_v3` 333 after the receivable test).

## Lien rate before and after (139c)

The arm now reads the register row I-D1m (the real deferral rate: 0% low, 2% central, 3% high) and the household default is the central, 2%. "6 phases, 0%" is `origin/main` before 139c; "10 phases, 0%" is this branch with `lien_rate='low'`; "10 phases, 2%" is this branch at its default. 20 paths, central returns path (`paths` off), schedule S, `scenario_before_after.py`; the CSVs are `scenario_rows_{before,lien0,central}.csv`. Money in millions of pounds per adult, real; M1a in % of GDP (mean over the paths). No headline number is read.

| point | run | shortfall line-phases | `unpaid` max | `unpaid_B` max | largest lien balance | settled from the pension | ledger tie max |
|---|---|---|---|---|---|---|---|
| `min_mid` | 6 phases, 0% | 80 | 0 | 0.13 | 0.381 | 8.84 | 6.25e-13 |
| `min_mid` | 10 phases, 0% | 160 | 0 | 0.13 | 0.475 | 18.8 | 4.83e-13 |
| `min_mid` | 10 phases, 2% (register central) | 160 | 0 | 0.13 | 0.624 | 22.3 | 4.83e-13 |
| `median_mid` | 6 phases, 0% | 0 | 0 | 0 | 0 | 0 | 1.59e-12 |
| `median_mid` | 10 phases, 0% | 0 | 0 | 0 | 0 | 0 | 1.19e-12 |
| `median_mid` | 10 phases, 2% (register central) | 0 | 0 | 0 | 0 | 0 | 1.19e-12 |
| `max_mid` | 6 phases, 0% | 0 | 0 | 0 | 0 | 0 | 1.32e-11 |
| `max_mid` | 10 phases, 0% | 0 | 0 | 0 | 0 | 0 | 5.46e-12 |
| `max_mid` | 10 phases, 2% (register central) | 0 | 0 | 0 | 0 | 0 | 5.46e-12 |
| `median_low` | 6 phases, 0% | 0 | 0 | 0 | 0 | 0 | 1.68e-12 |
| `median_low` | 10 phases, 0% | 0 | 0 | 0 | 0 | 0 | 1.02e-12 |
| `median_low` | 10 phases, 2% (register central) | 0 | 0 | 0 | 0 | 0 | 1.02e-12 |
| `median_high` | 6 phases, 0% | 0 | 0 | 0 | 0.243 | 70.6 | 2.27e-12 |
| `median_high` | 10 phases, 0% | 0 | 0 | 0 | 0.252 | 134 | 1.36e-12 |
| `median_high` | 10 phases, 2% (register central) | 0 | 0 | 0 | 0.259 | 156 | 1.36e-12 |

Reading: the lien rate moves only the lien balance and the amount settled from the pension (`min_mid` 18.8 to 22.3, `median_high` 134 to 156); it moves no shortfall count, no `unpaid`, no ledger tie and, on the accrual basis M1a is read on, no M1a. The 80 to 160 shortfall line-phases at `min_mid` are the 10-phase count over the same 20 paths (200 path-phases against 120), not new lines; they are the 137c floor alarm, still open. Every tie holds to 1e-11 and I1 holds in all 15 runs.

## Pension withdrawal and the heir floor (brief 148c)

Two scenario switches on the lien's flows, both off by default (off is byte-identical; `test_legacy_digest` unchanged). **Scenarios, never forecasts; no central value; no headline number.** Code: `model_v3/runner/flow_switches.py`. Run: `household-arm-run/lien_rerun.py --paths 20 --pension-withdrawal low|mid|high | --heir-floor 0|25|50`, and `flow_ties.py` for the ledger tie on every core run. Files: `household-arm-run/flow_switches/` (`lien_checks_*.csv`, `lien_lines_*.csv`, `lien_alarms_*.csv`, `ties_*.csv`). The points are the two 127c points with a lien, `min_mid` and `median_high`, at 20 paths (the arm has no spread at fixed returns).

**Rules as built.**
- **`pension_withdrawal`** (`low`, `mid`, `high`; 145r): a line draws, each year, its band's retired share (the pack's persons) times the half's rate (bottom half `D1-3`, `D4-5`: 0, 0.7, 2.9% of the opening pension; top half `D6-7` to `D10`: 0.8, 2.4, 4.1%) into net financial wealth. Total wealth is unchanged; the pension stays in the assessed base while held. Evidence class `proxy`; the not-retired stage is `unset` and does not draw; the retired share is a person-based proxy because the pension is not split by stage in the pack. `low` is a floor (zero in the bottom half).
- **`heir_floor`** (0, 25, 50 % of the pension; author ruling 2026-11-23): the settlement draw at a death and at the horizon cannot take that share of the pension. The hook cannot tell the two apart. What the floor leaves unpaid is written off, reported in the ledger as `wo` (the column of the limited-recourse write-off, 138c). 0 is today's uncapped draw.

**Checks (20 paths).** I1 holds (it raises in the hook otherwise), `unpaid` is 0 and no run failed, at all twelve rows. The tie column is the worst over every `core_run` of the evaluation (`flow_ties.py`), not only the main run.

| Setting | Point | Account residual | `unpaid_B` max | Shortfall lines | Lines with a lien | Ledger tie (all runs) | Ledger write-off (billions, all runs, years and paths) |
|---|---|---|---|---|---|---|---|
| floor 0 | `min_mid` | 1.6e-11 | 0.13 | 160 | 3 | 8.4e-12 | 1,185 |
| floor 0 | `median_high` | 1.9e-11 | 0 | 0 | 11 | 4.3e-10 | 0 |
| floor 25 | `min_mid` | 1.6e-11 | 0.13 | 160 | 3 | 8.4e-12 | 4,059 |
| floor 25 | `median_high` | 1.9e-11 | 0 | 0 | 11 | 4.3e-10 | 0 |
| floor 50 | `min_mid` | 1.6e-11 | 0.13 | 160 | 3 | 8.4e-12 | 6,933 |
| floor 50 | `median_high` | 1.9e-11 | 0 | 0 | 11 | 4.3e-10 | 0 |
| withdrawal low | `min_mid` | 2.0e-11 | 0.13 | 120 | 2 | 8.8e-12 | 1,185 |
| withdrawal low | `median_high` | 1.6e-11 | 0 | 0 | 10 | 5.5e-12 | 0 |
| withdrawal mid | `min_mid` | 1.6e-11 | 0.034 | 120 | 2 | 2.6e-12 | 0 |
| withdrawal mid | `median_high` | 1.9e-11 | 0 | 0 | 0 | 4.6e-12 | 0 |
| withdrawal high | `min_mid` | 1.8e-11 | 0.034 | 120 | 1 | 1.7e-12 | 0 |
| withdrawal high | `median_high` | 1.7e-11 | 0 | 0 | 0 | 7.1e-12 | 0 |

The `median_high` ledger tie of 4.3e-10 at floor 0, 25 and 50 is 3e-13 of the largest balance in the run (1,377 billions); floor 0 is the run without a switch (today's settlement), so the figure is the unswitched run's. The lien balance and the shortfall lines at `min_mid` rest on the 127c floor alarm (zero-unit lines), which the switches do not touch.

**The heir floor, `min_mid`, line D4** (the instance with the largest balance; millions of pounds per adult). The lien balance reaches 0.624 against a pension of 0.558 even at floor 0, so a write-off exists before any floor (0.106 on that instance; 2.27 summed over the 40 instances that write off). The settlement draw from the pension falls from 0.578 (floor 0) to 0.433 (25%) and 0.289 (50%); the write-off on that instance rises to 0.249 and 0.391 (summed over instances: 7.79 and 13.3). D5 and D6 settle 0.0012 and 0.0007 from pensions of 0.68 and 0.87, so the floor never binds there.

**The heir floor, `median_high`: no effect.** Every line settles under 3% of its pension (0.7 to 2.5%) at the horizon (0.010 of 1.46 at D1 to 0.26 of 10.5 at D10b), so a floor of 50% leaves the settlement and the ledger as at floor 0 (write-off 0 at all three floors). The floor binds only where the lien approaches the pension, here the low-saving line.

**Withdrawal.**
- At `median_high` it shrinks the lien (liens on 11 lines at the baseline, 10 at `low`, none at `mid` and `high`) and in the main run (schedule S) the ledger's largest balance falls from 272 billions to 0 at all three settings; at `low` liens remain in the other runs (largest balance 470 billions across all runs, against 1,377 at the baseline).
- At `min_mid` the bottom-half rates apply to D4 (`low` is zero there, so D4 is as at the baseline; `mid` and `high` cut its largest balance from 0.624 to 0.0005 and 0.0010 and the write-off to 0). The lien lines fall from 3 to 2 (`low`, `mid`) and 1 (`high`); `unpaid_B` falls from 0.13 to 0.034 at `mid` and `high`. The shortfall lines fall from 160 to 120 at all three settings: the rest are the floor alarm.
- The draw is a transfer inside total wealth, so what it changes is the capacity to pay in life, not the wealth.

**Found and fixed on the way (block 3 smoke run).** The withdrawal hook's `_year` read `self.q` on the untaxed path (`free`, used by M3 and M12), before any run had set it; the statics raised `AttributeError`. The block 1 tests did not reach that path. Fixed in `flow_switches.py` (one line) with a regression test, `test_the_untaxed_path_runs_with_the_withdrawal_on_before_any_run` (fails without the fix, passes with it).

## For the author

1. The floor alarm (zero-unit lines that cannot take the year's saving) is now the only shortfall; it needs its own ruling.
2. Whether the settlement draw should be limited to what the heir would receive (see the draw rule).
3. Settled in 139c: the deferral rate is the register row I-D1m (central 2%).
