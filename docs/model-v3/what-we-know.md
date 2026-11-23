# What we do and do not know about the model

Written 2026-11-23 by the guru for the author. Plain English; the detail is in the notes linked at the end. This is a snapshot: the status board (`STATUS.md`) is the live view.

## What the model is
A range model of the Wealth Delta Tax. It follows 14 representative groups of adults ("payer lines", the ten wealth deciles, the top tenth split in two, and three Rich List tiers) for 100 years. It reports government revenue, taxpayer burden and non-payer savings as **ranges across labelled scenarios**, never one central forecast. Two arms exist: the **household arm** (income, saving and class returns, the arm the first official run will use) and the older **legacy arm** (consumption as 3.5% of wealth, kept only as a comparator).

## What we know (checked, reproducible)
- **The household arm runs and ties out.** Its account identity, the public ledger and the "family value equals class total" check (I1) hold to about 1e-11 at four of the five scenario points; the fifth (`median_high`) only awaits a tolerance fix (138c).
- **The pension is handled consistently.** It is inside the assessed base, never sold in life, and unpaid tax on it is carried as a lien that accrues and is settled at death. Anything the pension cannot cover is written off and shown in the ledger.
- **The two arms gave different answers for understood reasons** (136c). Gross receipts are similar. The M2 gap was mostly the legacy arm's market volatility plus one bookkeeping defect, now ruled for repair. The P6 (fund size) gap is entirely the fund's return: market mean in the legacy arm, a safe stand-in in the household arm.
- **Several earlier errors are fixed:** tail lines holding too much pension (118c, 119c), exhausted lines (127c, 133c, 137c), OW1 under per-path returns (135c).
- **Market risk is modelled** (per-path returns, 200 paths); GDP growth risk is not.

## What we know only roughly (evidence is a proxy, labelled as such)
- **Pension value.** ONS basis is central; the IFS basis is about 1.96 times larger. The IFS basis overshoots wealth over GDP and does not fix the top-tail gap (131r).
- **Pension drawdown.** No held source gives a pension withdrawal rate. The nearest proxy is net financial wealth drawdown for the over-70s (IFS/ELSA, 0 to 4% a year) (145r).
- **Saving by wealth band.** No held source gives it. Only a step from Norwegian data suggests the poorest save less (145r).
- **The top 1%.** Published shares (14.4% to 16.5%) are below the pack's own 21.9%, from different methods and years (146r).
- **The lien deferral rate.** 2% real central (0% to 3% range), a judgement (134r).
- **Validation.** Of 33 held research moments, 5 are held, 4 partly, 24 not tested (125c).

## What we do not know
- **Whether any tax schedule is feasible.** Under the household arm no schedule passes the feasibility test, even on a constant return path (140c). The suspected cause is the six-phase death timing, which makes receipts lumpy every fifth year; this is untested (149c). Until it is settled the three named schedules behind the headline numbers are not backed by a feasibility result.
- **How wide the final ranges are.** The fund's size changes more than tenfold with one choice (safe or market return). No one has yet seen the full combined ranges, so we cannot say whether they will support a clear message.
- **Wealth concentration over time.** One saving ratio for everyone makes the model too equal (top tenth 20% to 34% against 50% observed). Saving gradients are queued as scenarios, not fitted.
- **Growth risk, pension drawdown, the heir's share of the pension, behaviour of the top tail.** Not in the model yet; queued as default-off scenarios (147c, 148c) or unset.
- **Run time.** A full five-point household run is hours to days at today's speed (150c).

## How to read the numbers
Every output is a range over named scenarios with no central case. A low and a high are not a confidence interval. Cells marked pending (OF1, CK1), withheld or not applicable are marked in the file on purpose.

## Where the detail is
`docs/model-v3/household-vs-legacy.md`, `household-arm-validation.md`, `household-arm-paths.md`, `household-arm-lien.md`, `f1-household.md`, `docs/research/131r-*`, `134r-*`, `145r-*`, `146r-*`, `docs/decisions.md`.
