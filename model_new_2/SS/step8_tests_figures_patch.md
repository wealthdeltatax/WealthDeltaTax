# Step 8: tests, tables, figures

Files: `8_2_RATES_tables.py` (tables 1-12), `8_3_RATES_charts.py` (figures 1-12),
`rates_test_hybrid_snippet.py` (new `test_hybrid`). Numbers and slugs match between tables and figures.

## 1. WDT_Params.toml: extend [rates.figures]

Keep the existing keys (scenario, mode, group, decomposition, rate_grid, ...) and add:

```toml
schedules = ["gain_ladder", "stock_ladder", "logistic_ln_gain", "logistic_ln_stock", "logistic_gain", "logistic_stock"]
cohorts   = ["baseline", "cohort_central", "cohort_high"]
scope     = ["baseline", "wmin_house", "wmin_house_hp"]
```

All three lists must be in `[rates.run].scenarios` (they are, after step 2).
Tables/figures 9-12 read these lists; `wmin_house_hp` runs only the 'house' index, and the
`_med` helper falls back to the mode a scenario did run (the caption states which was used).

## 2. wdt_core.py: figures validation (in `_parse_rates`)

Wherever `figures` is parsed, make the three new lists optional (default `[]`) and check each name is a defined scenario:

```python
fg = dict(raw['figures'])
for key in ('decomposition', 'rate_grid', 'schedules', 'cohorts', 'scope'):
    fg[key] = list(fg.get(key, []))
    for n in fg[key]:
        if n not in scenarios:
            raise ValueError(f"[rates.figures].{key}: unknown scenario '{n}'")
```

## 3. rates_test.py: four edits

a. Paste `test_hybrid` from `rates_test_hybrid_snippet.py` between `test_engine_invariants` and `test_valgen_equivalence`.

b. In `main()`, after `test_engine_invariants()`: `test_hybrid(p, J)`

c. In `test_params`, the raw dict: delete `'solve': {'scenario': 'x'},` (the solver is gone; it is ignored if left).
   Extend the optional-defaults check to the new keys:
   `('tiers', 'wmin_pct', 'payout_top', 'exp_paths', 'levy', 'countries', 'cohorts', 'wmin_house_ratio', 'anchor_from')`

d. `test_registries` needs no change; it compares both registries, so 9-12 are covered.

`test_hybrid` was run against the synthetic harness (26 checks, all pass, including the
pipeline block and the three new scenarios). It has not run on the real JST file.

## 4. Remove

`rates_core1.py` from the project (archive).
