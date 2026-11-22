# The household arm: what a run produces and withholds (brief 121c)

Status: the manifest amendment below was signed off and applied by brief 122c (2026-11-22): `outputs.yml` carries `arms: [legacy]` on the six withheld ids and `arms_by: {headline: {M3: [legacy]}}` on OT1, and the validator accepts a withheld entry under the household arm only. Written for the author's sign-off by 121c. No revenue, fund or burden number is in this note; it lists outputs, labels and gaps only. Brief 121c, 2026-11-22.

## Labels

- A run chooses its arm in `Ctx.arm`: `'legacy'` (the default, digest unchanged) or `'household'`, or a dict naming the scenario (`arm`, `inputs`, `saving`, `regime`). `runner.arm.build` returns the hook, the safe series and the label.
- The run record (`Raw.arm`) is `{arm: 'legacy'}` under the legacy arm. Under the household arm it is `{arm: 'household', scenario: {saving, saving_ratio, regime, class_returns, pension_accrual, tail_pension_cap, income_scale}, safe_return, central: false}`. No run is called central.
- `out/writer.run_block` accepts the label as the optional run field `arm`. The validator does not know that field and warns (V12, a warning); see the proposal below.
- A withheld id is written by `assemble(..., withheld=arm.withheld(label))` as `{summary, cells: [], withheld: 'legacy_only'}`. It never holds a value, and `assemble` raises if samples exist for it.

## Grid point of the smoke run

Schedule tau_0 0.04, tau_m 0.7, k_ln 1, ratio 0.5 (the digest's `centre`, as in the account table). Saving: the median of the ONS non-pension ratio (1.0063% of income; the min and max are the other two grid values). Regime: mid. Class returns (fixed, see below): property 1.6455% (F-20, a named constant in `arm.py`), net financial 0.9389% (the mid regime's total less its yield, I-D1h and I-D1i), physical 0 (I-D1j), pension as net financial. Pension accrual I-D1k at the observed 2024 value (4.83% of income). Tail pension ceiling I-D1l at 0.386. Incomes scaled by 1.3733 to B.6g 2024. Smoke paths: 2 paths of 100 years at a constant 1.57% market return (the household arm does not read them for class returns). All other register rows at their central values.

## Rules the arm implements

- **Fixed class returns.** The household arm uses the scenario's class returns, constant over years and paths. The run's market path `g` is not read by the household arm; only GDP growth moves with the path. This is the account script's rule, reused.
- **Stand-in safe return.** The public ledger's safe asset earns the net financial class return (0.9389% at this grid point) until a register row exists. The label says so.
- **`fl` horizon settlement (fixed by 123c).** The burden run's line flows (`fl`) used to miss the horizon settlement of year T (about £639bn at the centre). `burden.line_flows` now settles Route D and B in year T under the household arm, as `run_lines` does, and counts it with the death flows; `fl` and `run_lines` agree in every year (test). M2 in life leaves death flows out, so the settlement is not in it by construction; M2b, M2c and M2d count it.

## One row per manifest id

Smoke run: 29 ids produced, 6 withheld, 5 not produced by a single evaluation (same under the legacy arm). The cells of O2, O2b, O2c and O2d at the short horizon are `nan` on the smoke paths, where the reserve does not fill; that is the existing gate, not a household-arm effect.

| id | metric | status under the household arm | reason / later brief |
|---|---|---|---|
| O1, O1a, O1b, O1c, O1d, O1f | M1, M1a to M1c, M1e, M1g | produced, household label | M1 includes the horizon settlement |
| O1e | M1f | not run here | break-even return, from `sweeps.breakeven_return` (a sweep, not one evaluation); not exercised under the household arm in 121c |
| O2 | M2 | produced | in life: the horizon settlement counts with the death flows and is left out of M2 by construction; `fl` now equals the receipts in every year |
| O2b, O2c, O2d | M2b, M2c, M2d | produced | count the horizon settlement (fixed by 123c) in windows that include year T |
| O3 | M3 | produced (126c) | `burden.m3` reads the run's own flows (the net change in wealth, saving included, as under legacy); no `free_path` |
| O4a | M4a | produced | M4a reads the retirement years and the pack's deciles, not `fl`; the 121c note was wrong to list it with the gap |
| O4b, OL1 | M4b, M4c | produced | read `P5` and the income deciles, not `fl` |
| O5, O6 | M5, M6 | produced | register rows only |
| O7 | M7 | produced | no c |
| O8 | M8 | produced | no c |
| OP1, OP3, OP4, OP5, OP6, OR1 | P1, P3, P4, P5, P6, P7 | produced | from the ledger and the safe series (the stand-in) |
| OS1 | S1 | produced | reruns the core under the household arm |
| OH1b | M3 (today) | produced (126c) | `m3_today` on the household hook's untaxed path (`HouseholdHook.free`, T = 0 through the same year), the static base at ratio 0.5 |
| OH1b2 | M11 | produced | register row I-T1d |
| OH1c | M12 | produced (126c) | `m12` on the same untaxed path |
| DH1a, DH1b | none | not run here | pack facts (`static`, once); the smoke context holds no `once` list; unchanged by the arm |
| DH1c | none | produced | pack and retired taxes |
| OW1 | M13 | produced (126c) | the WDT line on the account (terminal wealth = units plus pension) against the stock tax (opening net worth, pension included), the tax on gains (CG) and the consumption tax (C), each paid from the non-pension classes (`HouseholdHook.system`), all at the WDT's lifetime tax per adult; no legacy c |
| OW2 | M14 | produced | no c |
| OW3 | M15a, M15b | produced (126c) | the kernel rerun on the account (`out_support._record` with the household hook: growth and consumption from the account, the WDT paid from the non-pension classes); refunds due and the cap's `lost_refund` are the kernel's. The account ignores g, so the paths of one schedule are identical. |
| OB1 | B1 | produced | |
| OD1 | M7 | produced | no c |
| OM1 | M1, X, M9 | produced (126c) | M1 and the payers as for O1; X = leavers x (income x rate_income + spend x I-T3q), the leavers' spend the account's consumption C = (1 - saving) x income (`HouseholdHook.consumption`, payer-weighted mean) instead of c times wealth |
| OF1 | F1 | not run here | feasibility map (a sweep); not exercised under the household arm |
| OT1 | T1 | produced with its M3 head (126c) | the M3 head returned; the manifest has no `arms_by` |

The set withheld is `arm.WITHHELD`: empty since 126c (O3, OH1b, OH1c, OW1, OW3, OM1 and OT1's M3 head returned; the manifest restricts no id, version `stage-A16-comparators-2026-11-22`); the module-to-id table of `architecture.md` 2.10 and the manifest are unchanged and still agree (`test_w7`).

## Manifest amendment (applied by 122c; as proposed by 121c, plus the OT1 head)

```diff
-  - {id: O3,   metric: M3,  title: "Taxpayer burden, gain-weighted lifetime rate", summary: p10_mean_p90, ...
+  - {id: O3,   metric: M3,  arms: [legacy], title: "Taxpayer burden, gain-weighted lifetime rate", summary: p10_mean_p90, ...
```

The same `arms: [legacy]` on OH1b, OH1c, OW1, OW3 and OM1. In `pipeline/validate_outputs.py`: add `withheld` to `ENTRY_FIELDS`; V7 then reads an entry with `arms: [legacy]` and `withheld: legacy_only` as covered when the run's `arm` is `household` (cells must be empty), and as an error otherwise; add `arm` to the run block's known fields. The validator also takes `withheld_by` on OT1 (the M3 head). A final household-arm file with the six ids withheld and OT1's M3 head labelled passes `--final`; the same file labelled legacy fails V7.
