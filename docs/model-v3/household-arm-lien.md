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

**Not carried.**
- `min_mid`: the floor alarm of 127c still fires on D4 in year 61 (0.0012) and D5 in year 78 (0.0012), the same amounts as before. The lien took the tax that the classes could not pay (`unpaid` is now 0); it does not remove this alarm, which is the saving that cannot enter a line whose units are all zero.
- `median_high`: no lien arises, and every figure is as in 127c. The tax on pension gains takes the non-pension wealth of nine lines (D10a in year 70 up to D1 in year 97). The kernel itself caps what it collects at the line's route units and records the rest in its `unpaid_B`; no class payment fails, so the hook never sees an unpaid amount to carry. To carry it a lien would have to be netted from the family value in the kernel, which the brief does not touch. Stop rule: reported, not built. The floor alarms listed in `lien_alarms.csv` stand.

## Unchanged

The three passing grid points `median_mid`, `max_mid` and `median_low`, and the legacy context, at 1,000 paths: `grid_results.csv` and the checks rows byte-identical (md5) to a run of the same script on `origin/main` before this brief. The 14-line account and ledger CSVs regenerated with an empty `git diff`. `test_legacy_digest` and all four suites pass (`model_v3` 333 after the receivable test).

## For the author

1. The kernel-cap case: a brief for the kernel (a lien netted from the family value, or a cap that records the excess as a lien) is needed before `median_high` can run to a clean account.
2. Whether the settlement draw should be limited to what the heir would receive (see the draw rule).
3. Whether the deferral rate should be a register row (it is 0.0 now).
