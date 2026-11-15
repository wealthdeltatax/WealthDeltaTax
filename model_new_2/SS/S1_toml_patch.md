# TOML patch for S1 (not applied; WDT_Params.toml is reference-only this session)

## [val_gen]
# reset_sens now lists voluntary-reset CYCLES (years) the family may choose; 0 = never. Re-comment the key; it is no longer a schedule.
reset_sens   = [0, 5, 10, 20]
# remove (retired, no reader in valgen_core): reset_interval, death_waiver
# optional, code defaults apply if absent (wdt_core.load_params passes only an explicit key list, so add these to that list):
b_shift      = [0.5, 1.0]
reset_cycles = [5, 10, 20]

## [verification]  already present: lambda_C, lambda_D, death_verifies, lambda_sweep
# lambda_D = 0 means "couple to lambda_C" in valgen (legacy behaviour); a positive value is used as given.

## [names.val]  (S5 will need ids for the new tables/figures; none were registered since S5 was not done)
