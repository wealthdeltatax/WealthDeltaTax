# WDT data audit: D7 to D9 review (15 Oct 2026)

Companion to `audit_progress_2026-10-15b.md`. Reviewed: `provenance_register_d7/d8/d9.md`, `coverage_matrix_d7/d8/d9.csv`, `wdt_audit_to_json.py`, `wdt_audit.json`, and the updated `WDT_audit_summary_open_items.md`. Nothing in those files was edited.

## 1. Checks that passed

- **D7 window counts reproduce exactly** from `windows.csv` and `usable.csv`: total windows LEVY 1728 to HOUSE 1575 (153 lost: ESP 66, PRT 40, ITA 36, JPN 6, GBR 5); against BASE 1801 the loss is 226 (PRT 57 there, because BASE keeps 72 PRT years). Contiguous losses 78 / 62 / 53 / 34 / 0 at T = 30 / 40 / 50 / 60 / 100, all as stated. Countries with contiguous windows 16 to 15, 16 to 15, 14 to 13, 12 to 10, 2 to 2.
- **`wdt_audit.json`** carries every CSV: row counts match (D1 21, D2 7, D3 9, D4 11, D5 9, D6 6, D7 5, D8 5, D9 3, overlap runs 79, ONS 28) with no warnings, and the compacted usable-year runs agree with `d1_overlap_runs.csv` (spot-checked PRT LEVY runs 1948-87 and 2005-19). Cosmetic: `meta.files` lists the usable-years file as `b1c35576-usable_years.csv` (an upload prefix) and `source_dir` is `/home/claude`.
- **D9 age-at-inheritance and D8 contents** are as described in the registers; no values to verify.

## 2. D7 findings

1. **T = 100 is the model's horizon, and the contiguous-window loss there is 0 only because just SWE and USA have 100-year contiguous runs.** The meaningful house-mode loss at T = 100 is the total: 1728 to 1575 (-8.9%). Windows that repeat years are 477 of 1728 (27.6%) under LEVY and 441 of 1575 (28.0%) under HOUSE, so house mode does not change the share of repeating windows materially. Report this next to the T = 30-60 table.
2. **PRT wording.** The register says contiguous windows lose ESP, ITA and PRT "altogether at long T". PRT (runs of 40 and 15 years under LEVY) only has contiguous windows at T of 40 or less, so for T of 50 or more it is already out of the LEVY set; the HOUSE loss at T of 50 or more is ESP and ITA (ITA keeps one window at T = 50, none at T = 60).
3. **D7 open item 3 (pre-1970 price-to-income level): not needed on the model's use of house prices.** Per the Code Reference, `house` index mode uses only the JST house-price index growth (`hpg_real`), and W_min is anchored once at launch (`wmin_house_ratio` x `house_median_gbp_m`). No house-price level or ratio enters a window. The D3 ownership validation compares `scope_share_t` with tenure shares and does not use price-to-income. D7d can stay "not needed". This is my reading of the code description; say so if a level is wanted elsewhere.
4. **D7 open item 1 (JST source for ITA, ESP, PRT).** macrohistory.net lists Italy, Spain and Portugal among the 18 R6 countries (Ireland added in R6), and says the house-price sources are in a separate file, "Documentation - House Price Data" (NPLH_documentation.pdf), which I could not open. The D0 start years (ITA 1971, ESP 1972, PRT 2005) remain consistent with a post-1970 BIS/OECD source but that is unconfirmed.

## 3. D9 findings

1. **`pop_per_adult = 1.27` behaves as an 18+ convention.** ONS mid-2017 UK population 66,040,229 / 1.27 = 52.0m, against the ONS 18+ projection for 2018 of 52,403,344 (mid-2016 base, variant not stated), within about 1%. A 16+ basis (about 53.5m in mid-2017, derived) would give about 1.23. Record it as 18+. (Different years, so approximate.) This is also why `adults_m = 54.0` in the TOML is inconsistent.
2. **Generation gap G.** ONS births, England and Wales, all births: mean age of mother 30.9 (2023), 30.0 (2013); mean age of father 33.8 (2023), 32.8 (2013). G = 30 sits at the mothers' mean and slightly below the fathers'.
3. **Correction to the D9 register's reasoning.** It says an inheritance age near 61 against a mean age at childbirth "would imply a generation gap near the length of a parent's remaining life". That conflates the two. With a death every G years and the heir inheriting at the parent's death, G = (parent's age at death) - (heir's age at inheritance) = the parent's age when the heir was born. So G should be read against mean parental age at birth (about 30 to 34 now), and the TOML's own cross-check (life expectancy about 85 less inheritance age about 57 gives about 28) is the same quantity. A Resolution Foundation mode of 61 would imply a parent age at death of about 91 at G = 30, which is a projection for today's 20-35 year olds, not a stylised-fact check on G.
4. **Not closed:** the long-run range of mean age at birth, and of adults per head, before 2010. Needs the ONS long series (instruction in the reply).

## 4. D8

No gate; extraction deferred. If wanted, the UK and US top-1% and top-0.1% net personal wealth shares can be taken from the same WID download as the D1 wealth series (code names to be confirmed in the WID codes dictionary). Treat WID's imputed country-years as non-independent, as the register says.

## 5. Stale text in the summary and JSON

- `WDT_audit_summary_open_items.md` sections 1, 4, 5 and 8 still say: D1 passes rest on unverified sources (NLD, CHE, DNK now read at paper level); "None is saved to the WDT RESEARCH project yet" (they are now); D4 `mc_gdp` awaits your data. The D1 rows of `coverage_matrix_d1.csv` and the JSON still show NLD (Moatsos) "author list not confirmed", CHE "unverified (abstract only)", PRT/DNK as before. See `audit_progress_2026-10-15b.md` for the updated statuses. I have not edited the summary, matrices or JSON.
