# I1 at the class floor (brief 127c)

For the author's review. Diagnosis first (block 1), then the fix and the reruns. **No headline number appears here.**

## Diagnosis (block 1, before any code change)

Reproduced with a logging subclass of the hook (20 paths; point, line and year as 124c reported). I1 is "the kernel's family value equals the class total N of the non-pension classes (property, net financial, physical)". Both failures are in `HouseholdHook.post`, in the check after the year's payment.

| Point | Line | Year | Class balances (millions of pounds per adult) | Kernel family value | Rule responsible | Bookkeeping or economics |
|---|---|---|---|---|---|---|
| `min_mid` (saving min, regime mid) | D5 | 78 | property 0.1175, net financial -0.1329, physical 0.0142, pension 0.4387; N = -0.0012; no tax this year | 0 (all route units 0) | **The household's own dissaving.** From year 73 the line's N falls 0.0015 a year (minimum saving is negative); its WDT is 0.0004 a year; in year 77 the tax equals the whole of N (2.2e-5, capped at holdings), and in year 78 the household step takes N below zero (net financial is net of the debt, 0 real). The kernel cannot hold negative units, so the family value is floored at 0 while the class book goes negative | **Economics** (a line whose non-pension wealth is exhausted by minimum-saving dissaving and tax) **plus a bookkeeping gap at the floor** (the book has no way to say "negative") |
| `median_high` (saving median, regime high) | D10a | 97 (the failure at ratio 0.25, year 70, is the same rule on the rerun's base) | property 1.8e-18, net financial 0.00228, physical 5e-20, pension 6.453; N = 0.0023 | 0 (all route units 0) | **A payment capped at non-pension wealth, then re-entry.** The line's pension (6.25 at year 96) gains about 0.19 a year; the WDT assessed on that gain exceeds the non-pension wealth (0.28 at year 95), so in year 96 the tax takes all of N (tax 0.0321 = N) and the pension, never sold, is not touched. Year 97: N0 is 0, there are no route units, and the household's saving (0.0023) cannot enter a book whose units are zero (units grow multiplicatively: 0 x anything = 0) | **Economics in year 96** (the tax on pension gains exhausts the line) and **bookkeeping in year 97** (saving cannot re-enter an empty book) |

So neither case is a pure bookkeeping disagreement, and neither is only economics: in both the line's non-pension wealth is genuinely exhausted first (by dissaving at `min_mid`, by tax on pension gains at `median_high`), and the raise is the book's failure to represent a line at the floor. The rule is not changed: the fix below only makes the book and the kernel agree at the floor and records the exhaustion as an alarm.

## The fix (block 2)

Both changes are in `HouseholdHook` (`arm.py`, 253 lines; its budget row goes from 245 to 255, named here and in `architecture.md`). `household.py` and the kernel are unchanged (no kernel change was needed, so no stop-and-report).

1. **A line with no units stays at the floor** (`pre`). When a line's non-pension total is 0 at the start of a year, its route units are all 0 and cannot carry any flow (units grow multiplicatively), so the line is held at 0: its non-pension classes are set to 0 and the year's flow that could not enter (negative: lost saving) or that the floor had to supply (positive: a debt the book could not carry) is recorded as the `floor` entry of `account()` and added to `book.unpaid_B`, so `shortfall_lines` counts it. The account's residual includes it. A line with negative non-pension wealth and non-zero units is **not** floored: it was always legal and its numbers do not move.
2. **A tax the classes cannot pay is followed by the book** (`_pay`). The kernel has already taken the whole tax from the line's units; the classes can pay only from positive non-pension balances. Before, the book kept the unpaid part and I1 raised (the `min_mid` line D4 in year 61 shows it; the diagnosis found the later D5 first). Now the unpaid part is taken from net financial wealth (it becomes debt) and recorded as `unpaid` in the hook and in `unpaid_B`.

No household behaviour, asset return, pension rule or settlement rule changed. The failures remain visible as alarms for the author to rule on; nothing was tuned.

**Unchanged (byte-identical):** the 14-line account and ledger CSVs at the three saving values (regenerated, `git diff` empty); the three passing grid points `median_mid`, `max_mid`, `median_low` (their `grid_results.csv` and `checks.csv` at 1,000 paths, compared before and after the fix on the same code base); `test_legacy_digest` and all ten suites pass (327 tests in `model_v3`). One intermediate version of the floor (also flooring a line whose wealth only turned negative) moved the account CSV; it was narrowed to the zero-unit case, which leaves them identical.

**Tests** (`test_household_tax.py`): a tax on a line in debt is followed by the book and recorded (`unpaid`, `unpaid_B`, `shortfall_lines`); a line with no units stays at 0, I1 holds, the floor is recorded and the account closes; a line that never reaches the floor records none.

## Results (block 3, 20 paths; the arm has no spread)

Files: `household-arm-run/i1_floor_checks.csv`, `i1_floor_alarms.csv` (labelled by point; the 124c files are not rewritten).

| Point | I1 | Raise | Account residual (max) | `unpaid` (max) | `unpaid_B` (max) | Ledger tie (max) | Shortfall lines counted |
|---|---|---|---|---|---|---|---|
| `min_mid` | holds | none | 1.6e-11 | 1.1e-02 | 1.3e-01 | 6.3e-13 | 300 |
| `median_high` | holds | none | 1.9e-11 | 0 | 1.4e-01 | 2.3e-12 | 3,000 |

Where the alarm first fires (millions of pounds per adult; full list in the CSV):
- `min_mid`: D4 in year 61 (the classes could not pay a tax of 0.0108 on a line in debt, and the floor holds the line at 0), and D5 in year 78 (the floor supplies 0.0012 the book could not carry). This is the 124c failure, now reported.
- `median_high`: the floor fires on D1 to D10b, from D10a in year 70 and D9 in year 71 up to D1 in year 97, each time a line whose non-pension wealth the tax on pension gains has taken cannot receive the year's saving (about 0.0013 to 0.0018 a year). The three RL lines do not reach it.

**Per case, plainly.** `min_mid` is economics at its root (minimum-saving dissaving and tax exhaust the line) with a bookkeeping gap at the floor, now closed. `median_high` is economics (tax on pension gains takes the whole non-pension wealth of nine lines in the second half of the century) plus the re-entry gap, now closed. In both, the alarm is a finding about the scenario, not a number to tune: the author rules on it.

Not done here: pension withdrawal, a running pension cap, any change to the settlement rule (out of scope). No headline number is stated.

## 137c block 1: every floor line-year at the five grid points (20 paths)

Method: a logging subclass of `HouseholdHook` (as `lien_rerun.py`) records each (phase, path, line, year) where `pre` sets the floor entry `fl` to a non-zero value, at the five points of `run_grid.py` at 20 paths. Per line and year the rows are collapsed over the phases and paths in `household-arm-run/floor_line_years_137.csv` (227 rows; the paths do not differ, so each row is the same value in every path-phase it counts). Saving here is the year's non-pension flow on the zero-unit line (the closing non-pension total, `N1 = -fl`), millions of pounds per adult; units are the kernel's family value of the line before the year. **No headline number.**

| Point | Floor line-years | Lines | Units | Saving sign | Case |
|---|---|---|---|---|---|
| `min_mid` | 1,740 | D4 (from year 61), D5 (from year 78) | 0 (to 1e-13) | negative, -0.0012 to -0.0044 | **Not restartable**: negative saving on zero units |
| `median_high` | 26,640 | D1 (97), D3 (96), D4 (91), D5 (90), D6 (86), D7 (85), D8 (77), D9 (71), D10a (70), D10b (83) | 0 (to 3e-13) | positive, +0.0013 to +0.0024 | **Restartable**: positive saving on zero units |
| `median_mid`, `max_mid`, `median_low` | 0 | none | | | held points, no floor |

Totals: 28,380 floor line-years, 26,640 restartable (all at `median_high`), 1,740 another case (all at `min_mid`). Counts equal the 133c rerun (1,740 and 26,640).

Balances at the floor (millions of pounds per adult, the whole range over the line-years of each case):
- `median_high` (restartable): non-pension classes at 0 to rounding (property and physical below 2e-13, net financial at most 1.3e-4 on D1 only); pension 1.31 (D1) to 10.5 (D10b); the pension lien up to 0.13 (D10b).
- `min_mid` D4: property 0.0696, net financial -0.0881, physical 0.0185 (they sum to 0); pension 0.26 to 0.65; saving -0.0012 to -0.0044. D5: property 0.116, net financial -0.130, physical 0.014 (sum 0); pension 0.43 to 0.69; same saving range. The classes hold debt against assets with no net wealth, and minimum-saving dissaving takes the line below zero. A zero-unit line cannot hold negative units, so a restart from saving does not apply.

So the table gives the stop rule's second case: the 1,740 `min_mid` line-years are not restartable by the preferred design (units = saving / price needs positive saving). Block 2 restarts the 26,640 and leaves the 1,740 as a listed alarm with the balances above; the author rules on them (see the change report).
