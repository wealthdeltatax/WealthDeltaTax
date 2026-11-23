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

## For the author

1. The floor alarm (zero-unit lines that cannot take the year's saving) is now the only shortfall; it needs its own ruling.
2. Whether the settlement draw should be limited to what the heir would receive (see the draw rule).
3. Settled in 139c: the deferral rate is the register row I-D1m (central 2%).
