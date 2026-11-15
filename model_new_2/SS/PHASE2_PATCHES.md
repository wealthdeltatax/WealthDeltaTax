# Phase 2 patches: Route B lien and income, death verification, archetypes, relief by tenth year

Status (11 Oct 2026): written and tested on local copies of the code. NOT yet run against your model files.
The valgen and RATES engine edits were tested on verbatim subsets typed from the project copies, not on the files
themselves, so the first real run is also the first test of the anchors. Every script stops before writing a file if
an anchor is missing or found twice, and keeps a backup.

Note: the status line of BASIS_CHANGE.md ("NOT run yet") is out of date: apply_basis_change.py was run and the validators ran OK on 10 Oct.

## Run order

Put these in one folder (they import each other): apply_basis_change.py, apply_phase2_params.py,
apply_phase2_valgen.py, apply_phase2_rates.py, bridge_d9.py. Then, from the model folder's parent:

    python apply_phase2_params.py MODEL_DIR --check     then without --check
    python apply_phase2_valgen.py MODEL_DIR --check     then without --check
    python apply_phase2_rates.py  MODEL_DIR --check     then without --check
    python bridge_d9.py MODEL_DIR
    (then valgen_core.py from its folder, then rates_core.py --quick from its folder)

(apply_basis_change.py must already have been run: it has.)  Backups: *.pre_p2.bak (and wdt_core.py.pre_p2b.bak).

## 1. apply_phase2_params.py

- Appends to WDT_Params.toml: [route_b], [income], [income.by_archetype], [verification], five [archetypes.*].
  Every value is a PLACEHOLDER (plan section 8, risk 7). payment_mode = "sale", lambda = 0, death_verifies = false,
  so nothing changes until you set them. If any of these headers already exists, nothing is appended.
- Adds _parse_phase2() to wdt_core.py (validates mode, shares in [0,1], cap in [0,1], archetype shares summing to 1)
  and returns p['route_b'], p['income'], p['verification'], p['archetypes'] from load_params() and load_rates_params().
- Not wired: [verification] lambda_C and lambda_D (valgen still takes one lambda, from [val_gen]; the single value feeds C,
  and D when the rule set has dauc = on). They are parsed and reserved.

## 2. apply_phase2_valgen.py (valgen_core.run_family3)

New arguments, all defaulting to the old behaviour: route_b ('sale' | 'lien' | 'income'), r_def, income_ratio, income_cap,
death_verify. _p5_opts passes them from the parameter file, so every search and surface picks them up.

Route B semantics (decisions made here; change them if you disagree):
- lien: the Route B share of each year's tax (allocated by delta shares as before) is not collected. It is added to a deferred
  balance LB, which accrues at r_def = sovereign real rate + deferral spread from the next year. LB is settled by sale of Route B
  units at the true price at each death (BEFORE the heir is taxed) and at the horizon. A refund on B cancels LB first.
- declared wealth is NET of the lien: W = sum of holdings - LB, and the post-settlement basis is net too. Without this the
  taxpayer would be taxed on wealth already owed to the state, and sale and lien would differ in base as well as timing.
- heir tax: its Route B share is deferred too (it is assessed after the lien is settled).
- income: the Route B share is paid from external income, allowance = income_cap x income_ratio x V0 x index per year (income
  grows with the W_min / k index), shortfall met by pro-rata sale of units. Income paid is cash to the state (ledger accounts
  'income' -> 'state_cash'); state_true_T includes it. A refund returns income paid (this generation) first. Income and the
  allowance reset at a death (the heir has its own income).
- death_verify: at each death, all unverified Route C moves to the verified tranche and the correction is assessed ('tax_death_C').
  Needs Route C. Route D is already auctioned at death unless death_waiver applies.
- PV: pv_true counts the state's receipts when received. Under the lien the receipt is late (death / horizon), under income it is
  cash. PV is therefore not comparable across modes without the state's holding gains; the archetype report says so.

New validator _p6_validate (10 checks, run in main after P5): defaults reproduce the sale engine to 1e-12; lien matches an
independent hand recursion (3 deferral rates); income hand case (state cash = sum of tax, family keeps all units); income shortfall
is sold and conserved; zero income = sale; family wealth falls with the deferral rate; ledger balance, caps and conservation over 80
runs (modes x shares x strategies x death_verify); death verification inert for the honest family and erodes the understatement gain
(C-heavy mix); invalid switches raise.
New archetype report (_p6_archetypes, JSON key 'p6'): per archetype and mode, honest terminal wealth, state PV, income paid,
unpaid B, best-response gain under the candidate rule at lambda 0 and the base lambda, and the breakeven deferral spread
(state receipts PV equals sale). It prints "not bracketed" when no spread in [-4%, +30%] equalises PV.

On the local copy, with invented parameters, the first-pass archetype numbers were: lien leaves the family richer than sale and the
state's receipts PV higher; read this as an artefact of PV counting only receipts, not as a finding. Check on your parameters.

## 3. apply_phase2_rates.py (rates_core.run_lines and run_window)

- run_lines(..., rb=None): rb is a dict of per-line arrays (Route B share, income ratio) and the mode. rb=None is the earlier engine
  exactly (tested bit-for-bit). With rb, the same mechanics as valgen on a vectorised line: lien balance, net declared wealth, income
  allowance, settlement at deaths, the heir tax's Route B share deferred or paid from income.
- Per cell, Route B share and income ratio come from [route_b].share_by_wealth and [income].ratio_by_wealth by launch wealth (£m),
  linear in ln W, flat beyond the ends. The share is CONSTANT per cell along the window; the engine's changes as payments move units.
- Scenario key route_b_mode ('sale' | 'lien' | 'income'); else [route_b].payment_mode. The script registers the key in wdt_core
  (_RATES_OPTIONAL); if its anchor is not found it says so and only the global setting works.
- New window columns: lien_gdp_mean, lien_out_gdp_end (balance outstanding at the window end; RATES does not collect it inside the
  window), rel_y10 ... rel_yT and exp_y10 ... (relief and expenditure as a share of GDP in each tenth year), rel_cov_year (first year
  relief covers expenditure; NaN if never). headline.<mode>.overall.p10 / p90 over uncensored windows.
- net receipts now include lien settled at deaths and income cash.
- Run_lines tests: rb=None identical to the post-basis engine; Route B share 0 reproduces it to 3e-16 in every mode and cap; lien and
  income hand cases; deaths settle the balance; unit conservation.

## 4. bridge_d9.py

One RATES line against run_family3, honest, same path. One-route families (A, C, B under sale / lien / income): asserted to 1e-9 on a
rising path (and for Route C on a volatile path). On local copies they agree to 1e-15. Volatile paths for A/B and the income/lien modes
are reported only (refund caps differ: valgen pools real value and caps by the state's stake; RATES caps by units paid).
Archetypes (Route D moved into A: an honest D accrues rather than paying in kind) are reported: RATES's constant Route B share against
the engine, whose share moves with the deltas. On local copies, differences were about 1-2% of terminal wealth in lien and income modes.

## 5. Not done

- Removal of reset_interval / death_waiver, and the strategy library rewrite (plan phase 3). They still work as before.
- Rebuild of the VAL / RATES tables, charts, numbers and examples for the new JSON keys (p6, lien and decade columns).
- D11: retirement of the legacy settle loop and run_pair / run_sim_hist (they are idle under the post basis; the bridge still uses them).
- Kernel vectorisation in the cores (BASIS_CHANGE (m)); the kernel is unchanged.
- D8 / D10 claims; per-window breakeven spread in RATES; lambda_C / lambda_D separately.
- PLAN_S1 fixtures remain gated; re-derive them with check_params_and_plan_s1.py.
- The Route D corrective auction in the kernel.
