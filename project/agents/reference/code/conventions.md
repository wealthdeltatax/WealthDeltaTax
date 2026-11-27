# WDT model conventions

Target conventions for the legacy model (model_v1, removed from the tree: tag `legacy-models-2026-11`; kept as history). Decided by the user: layer order, cores never
import each other, `wdt_analytics` is dissolved, JSON names are consistent, LDW is paper
21, VAL/SWEEPS numbering is updated. Items marked **(proposal)** or **(open)** are my
reading or an unsettled gap; confirm before enforcing. Where to move things:
`refactor-map.md`.

Contents: 1 Layers · 2 Import rules · 3 TOML rules · 4 JSON contract · 5 Paths and
naming · 6 Tables · 7 Charts · 8 Cores · 9 Adding a paper · 10 Tests, patches and fixtures

---

> **Legacy layers.** The file names in this table (`WDT_Params.toml`, `wdt_core.py`, the `*_core` files, `OUTPUTS/{CODE}/`) belong to the legacy models, removed from the tree (tag `legacy-models-2026-11`). Model v3 follows `model-specs/architecture.md` (layers core, runner, out in `model/model_v3/`); the rules below on cores, JSON contract and presentation scripts still describe the old pattern.

## 1. Layers

| # | Layer | Files | Owns | Must not |
|:-:|:---|:---|:---|:---|
| 1 | Parameters | `WDT_Params.toml` | Every hardcoded model value | contain logic |
| 2 | Base | `wdt_core.py` | `load_params`, `tau`, `simulate*`, `run_sim*`, `run_pair`, NPV, decomposition, `_ssm_marginals`, `synthetic_returns`; the shared fund-model engine (SSM/TCM/start-year sweep) once moved; JSON `save_json`/`load_json`; path helpers; any helper ≥2 cores need | import matplotlib, import any other project module, write anything except via `save_json` |
| 3 | Cores | `val_core`, `rates_core`, `sweeps_core`, `wfr_core`, `ldw_core` | Paper-specific computation; emit JSON on run | import matplotlib, format markdown, hardcode inputs, **import another core** |
| 4 | Data | `OUTPUTS/{CODE}/*.json` | The contract | contain formatted strings or numpy objects |
| 5 | Presentation | `{n}_{m}_{CODE}_tables.py`, `_charts.py` | Read JSON → markdown / PNG | run simulations, re-derive numbers, import any `*_core`, import another presentation script |
| – | Presentation utilities | `wdt_fmt`, `wdt_style`, `wdt_md` | Formatting, paths, style, markdown assembly | import a core (wdt_fmt / wdt_style / wdt_md should be leaves) |
| – | Tests and patches | `model_v1/test/` | `patch_NNN_*.py`, `test_patch_NNN_*.py`, `wdt_patchlib.py`, `extract_jst_sample.py`, `fixtures/`, `PATCHES.md` | be imported by the pipeline; hardcode paths; touch the real tree except via `--apply`; hold logic that belongs in a core (section 10) |

`wdt_analytics` is **being dissolved**: its functions go to `wdt_core`, `sweeps_core`,
`wdt_style` and the TOML (table in `refactor-map.md` §3). Don't add to it and don't
write new code that imports it.

## 2. Import rules

- Direction is downward only: 5 → 3 → 2 → 1.
- **Cores never import each other.** If two cores need it, it goes in `wdt_core`. This
  currently forces the SSM/TCM engine out of `rates_core` (needed by `sweeps_core`).
- **Presentation never imports a `*_core`** (it reads JSON through `wdt_core.load_json`)
  **or another presentation script** (`16_3` imports `8_2` today; shared table code
  belongs in `wdt_md` / `wdt_fmt`).
- `wdt_fmt`, `wdt_style`, `wdt_md` import nothing from the project (stdlib / matplotlib
  only; matplotlib lazily).
- Presentation may import `wdt_core` for `load_json`, `load_params`, `tau`, path helpers
  and other pure maths.
- No module-level side effects on import (the old `load_params()`-at-import in
  `val_s_helpers` was removed for this reason). Anything needing `p` takes it as an
  argument or is initialised in `main()`.
- Mutable module globals populated in `main()` (`wdt_analytics` CANON_*, `BASELINE` in
  `16_4`) work but are fragile. Prefer passing `p` explicitly in new code.

## 3. TOML rules

- If it changes a number, a grid, a scenario, or a number quoted in text, it's in the TOML.
- Every key has a comment with units and meaning. Fractions as decimals, money in £m
  (except budget in £b).
- One source per value. The `[sweep]` canonical block (`tau_0_canon`, `k_canon`,
  `N_canon`, `V0_canon`, `g_canon`, …) currently duplicates `[rate]`, `[val]` and
  `[tcm]` values; new code should read the primary and prefer deriving canon values
  over adding more copies.
- Derived values (`N_fill`, anything from the SSM) are never TOML inputs.
  `snapshot_N` is a fallback only.
- Integers without decimal, floats with (TOML is strict); cast in `load_params`.
- New sweep grids go under `[sweep]` (or the paper's own section), are parsed in
  `load_params`, and are read through `p`.
- Things that currently live in code but belong here: see drift register §A.

## 4. JSON contract

- Written by the core's `main()` via `wdt_core.save_json`; one primary JSON per paper code
  (two for SWEEPS: one per `SWEEPS_V` / `SWEEPS_R` directory), named `{code}_data.json`
  **(proposal for the exact form; consistency is decided)**: `val_data.json`,
  `rates_data.json`, `wfr_data.json`, `ldw_data.json`, `sweeps_v_data.json`,
  `sweeps_r_data.json`. Today: `val_data`, `rates_output`, `wfr_results`, `sweep_cache`.
- Uniform top-level `meta`: `code`, `generated`, `model_version`, `scenario_start_year`,
  `N_val`, `N_fill`, parameter snapshot; then the data. `rates_output.json` is flat today.
- Plain JSON types only. Convert numpy and nan/inf → `None`. Float-keyed dicts are
  stringified; decode in one documented place (`_decode_tcm` and `_rekey_float` are two
  ad hoc versions).
- Each figure/table dataset carries the `N` it was computed at. `val_core` stamps and
  validates this; other cores should.
- Money, rates and units: the JSON stores raw model units (fractions, £m/£b) and never
  percentages or formatted strings. Formatting is the presentation layer's job. Note the
  existing exception: `val_core` chart matrices are in percentage points; label this
  in the key name or notes.
- Loading and saving are shared: `wdt_core.save_json` / `load_json` (+ one `rekey_float`)
  replace four sanitisers and the per-core loaders (`load_val_data`, `load_rates_output`),
  so presentation never imports a core to read data.

## 5. Paths and naming

- Root is the flat `model_v1/` directory. Path helpers `out_dir(code)`, `json_path(code)`,
  `tables_dir(code)`, `charts_dir(code)` belong in `wdt_core` **(proposal)** because cores
  need them and `wdt_fmt` must stay a leaf; `wdt_fmt.out_dir` is the current home.
- Shortcodes as directory names: `VAL`, `RATES`, `SWEEPS_V`, `SWEEPS_R`, `WFR`, `LDW`.
- Script names: `{paper#}_{seq}_{CODE}_{tables|charts}.py`; `_2` = tables, `_3` = charts
  (RATES and WFR already follow this; cores are unnumbered). Paper numbers: VAL 5,
  RATES 8, SWEEPS 16, WFR 19, LDW 21. VAL and SWEEPS are to be renumbered; the proposed
  renames are in `refactor-map.md` §6. Worked-examples script placement is **(open)**.
- Figure files: `{code}_fig_{number}_{slug}.png`, lowercase prefix, number matching the
  paper's figure number and the title text. Currently mixed (`val_fig_`, `rates_fig_`,
  `SWEEPS_v_fig_`, `sweeps_r_fig_`, `wfr_fig_`); SWEEPS_V should become `sweeps_v_fig_`.
- DPI 300 via `save_fig` everywhere (WFR currently passes `DPI_SCREEN`).

## 6. Tables

- Build with `MdDoc` and `md_table` / `pct_table`; number formatting from `wdt_fmt`.
  `5_3`, `5_5` still use raw `lines.append`.
- Captions under tables, "Table X.n: …" form, with parameters drawn from `p`.
- No literal parameter values in prose or captions.
- Tables are pure formatting of JSON.

## 7. Charts

- `apply_style()` / `apply_style_nogrid()` at the top of every figure function.
- Sizes from `wdt_style` FIG_* constants; if a paper needs a bespoke size used more than
  once, add a named constant to `wdt_style`, not a local tuple.
- Colours from `wdt_style`. Paper-specific palettes (WFR systems, tiers) go there too.
- Titles built from data (`p`, meta), not typed numbers.
- Each figure function returns the saved path and takes the data dict, not globals.
- Figure counts quoted in docstrings must match reality.

## 8. Cores

- `main()` does: `p = load_params()` → compute → validate → write JSON → print the
  path and size. Re-running with unchanged inputs gives identical JSON (no timestamp
  in the body; date in `meta` only).
- Explicit N everywhere; stamp outputs.
- Internal validation where feasible: identity checks and cross-table equalities (see
  `val_core._validate`). New cores should add their own cheap invariants.
- Console reporting functions inside cores (`report_*` in `rates_core`) are tolerated
  but keep them out of the compute path.
- Heavy loops should cache or reuse (`_ssm_marginals` is called many times; `load_params`
  runs a full marginal pass on every call).

## 9. Adding a paper (checklist)

1. Choose the shortcode and get the paper number from the user (LDW = 21).
2. `[code]` section in TOML with commented keys; parse in `load_params`.
3. `{code}_core.py`: imports `wdt_core` only (no other core); `main()` writes
   `OUTPUTS/{CODE}/{code}_data.json` via `save_json`.
4. `{n}_{m}_{CODE}_tables.py` → `OUTPUTS/{CODE}/tables/`.
5. `{n}_{m}_{CODE}_charts.py` → `OUTPUTS/{CODE}/charts/`.
6. Add all to `run_all.bat` in order (core first).
7. Run, then check: no literals that belong in TOML, no simulation in presentation,
   captions/titles derived from `p`.

## 10. Tests, patches and fixtures

Full workflow: `patch-and-test.md`. The rules that bear on convention:

- Everything new in the test layer lives in `model_v1/test/` and is run from there. Paths are found
  at run time (`wdt_patchlib.model_root()`, `find_file(name)`), never typed in, so the same
  patch works whether a core sits in `model_v1/`, `model_v1/RATES/` or `model_v1/VAL/`.
- Existing tests that sit beside the modules (`kernel_test.py`, `test_valgen_pairs.py`,
  `rates_test.py`, `test_wdt_*.py`) are not moved as a side effect of another change. Several
  locate the modules with `Path(__file__).parent`, so a move needs that line changed.
- Tests are not presentation: they may import any layer, cores included. They still follow the
  hardcode test: a tolerance is code, but a parameter that changes a result is read from the TOML
  (or set explicitly in a sandbox copy of it), not retyped.
- Tests never read the real JST or `OUTPUTS/`. They use `fixtures/jst_sample.json` (generated by
  `extract_jst_sample.py`) and run on a sandbox copy of the code, so a test cannot change the
  real tree and does not depend on a prior pipeline run.
- A patch is immutable once applied; a fix is the next numbered patch. The log is `PATCHES.md`.
- Pass criteria use the project's tolerances: 1e-9 for bridge and parity checks (as
  `kernel_test.py`), identical JSON for a pure move.
