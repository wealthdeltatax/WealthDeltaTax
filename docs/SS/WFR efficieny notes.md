Good. Now I'll do a systematic read of each file, tracking helper usage. I'll go file by file efficiently since I already have all the content in context.

Here's my sweep across all six files (`welfare_core.py` already confirmed as the computation spine — I'll focus on the five module scripts and `welfare_tables.py`):

---

## Audit Report: Helper Function Usage in WFR Pipeline

### Summary verdict up front

The files are **mostly compliant** but have **several concrete gaps** — some minor, some worth fixing before the paper ships. No file is in bad shape, but `welfare_tables.py` has the most issues.

---

### `welfare_core.py` — computation spine

**Role:** ✅ Correct. Holds all the shared primitives (`crra_utility`, `expected_utility`, `variance_of_consumption`, `solve_revenue_equivalent_rate`, `run_welfare_comparison`, `dm_test`). The modules call this correctly.

**Helper usage:** `welfare_core` intentionally imports *nothing* from `wdt_fmt/md/style` — correct, it is a pure computation layer. No issues here.

---

### `19_2_module1_baseline.py`

| Area | Status | Detail |
|:---|:---|:---|
| `wdt_style` | ✅ | `apply_style()`, `save_fig()`, all figure size constants (`FIG_PAIR`, `FIG_WIDE_L`, `FIG_QUAD`), `DPI_SCREEN` — all used |
| `wdt_fmt` | ✅ | `fmt_pct`, `fmt_pct0` imported and used |
| `wdt_md` | ⚠️ **unused** | Module 1 produces no markdown tables and does not import `wdt_md` at all. This is probably intentional (tables come from `welfare_tables.py`), but worth noting if Module 1 ever gains standalone table output |
| `welfare_core` | ✅ | All heavy computation delegated correctly: `run_welfare_comparison`, `dm_test`, `variance_of_consumption`, `expected_tax`, `get_tax_fn`, `make_empirical_distribution_scenario`, `make_idealised_distribution_scenario`, `make_scenario_sequence` |
| `_save()` local wrapper | ⚠️ | Defines a local `_save(fig, name)` that calls `save_fig(fig, OUTPUT_DIR / name, dpi=DPI_SCREEN)`. This passes `DPI_SCREEN` (150) rather than `DPI_PRINT` (300). All four modules do this — consistent but diverges from the canonical `save_fig` default (300 dpi). |

**Actionable:** The `dpi=DPI_SCREEN` in all `_save()` wrappers is a deliberate low-res choice for the WFR module charts — but it's inconsistent with `save_fig`'s documented default (`DPI_PRINT=300`). Either (a) accept 150 dpi for WFR preview outputs and document it, or (b) remove the `dpi` override and let `save_fig` default apply.

---

### `19_3_module2_progression.py`

| Area | Status | Detail |
|:---|:---|:---|
| `wdt_style` | ✅ | `apply_style()`, `save_fig()`, `FIG_SINGLE`, `FIG_PAIR`, `FIG_WIDE`, `DPI_SCREEN` — all used |
| `wdt_fmt` | ✅ | `fmt_pct`, `fmt_pct0`, `fmt_pct4`, `fmt_gbp_m` — all used |
| `wdt_md` | ⚠️ **unused** | Not imported. Same situation as Module 1. |
| `welfare_core` | ✅ | `run_welfare_comparison`, `expected_utility`, `expected_tax`, `consumption_equiv_welfare`, `variance_of_consumption`, `solve_revenue_equivalent_rate`, `get_tax_fn` all delegated correctly |
| Local computation | ⚠️ | `ProgressiveRateFunction`, `tax_progressive_wdt`, `expected_utility_progressive`, `expected_tax_progressive`, `variance_progressive` are all defined locally in Module 2. This is correct architecture (progressive-specific logic lives here), but `variance_progressive` duplicates the pattern of `variance_of_consumption` in `welfare_core` — candidate for eventual consolidation |

**Actionable:** `variance_progressive` could be added to `welfare_core` as an overloaded variant that accepts a callable (not a `(W0, R, tau)` signature). Low priority.

---

### `19_4_module3_lockin.py`

| Area | Status | Detail |
|:---|:---|:---|
| `wdt_style` | ✅ | `apply_style()`, `save_fig()`, `FIG_SINGLE`, `FIG_WIDE`, `DPI_SCREEN` |
| `wdt_fmt` | ✅ | `fmt_pct`, `fmt_pct0`, `fmt_pct1`, `fmt_pct4`, `fmt_gbp_m` |
| `wdt_md` | ⚠️ **unused** | Not imported |
| `welfare_core` | ✅ | `run_welfare_comparison`, `consumption_equiv_welfare`, `crra_utility`, `get_tax_fn`, `solve_revenue_equivalent_rate` all correctly delegated |
| Local computation | ✅ appropriate | `AssetSwitchDecision`, `compute_lock_in_welfare_cost`, `sensitivity_*`, `full_comparison_with_lockin` — all lock-in specific, correctly belong here |

No issues beyond the `dpi=DPI_SCREEN` pattern.

---

### `19_5_module4_heterogeneous.py`

| Area | Status | Detail |
|:---|:---|:---|
| `wdt_style` | ✅ | `apply_style()`, `save_fig()`, `FIG_PAIR`, `FIG_PAIR_T`, `FIG_WIDE_L`, `FIG_QUAD`, `DPI_SCREEN` |
| `wdt_fmt` | ✅ | `fmt_pct`, `fmt_pct0`, `fmt_pct1`, `fmt_pct4`, `fmt_gbp_m` |
| `wdt_md` | ⚠️ **unused** | Not imported |
| `welfare_core` | ✅ | `run_welfare_comparison`, `expected_utility`, `expected_tax`, `variance_of_consumption`, `consumption_equiv_welfare`, `solve_revenue_equivalent_rate`, `get_tax_fn`, `make_scenario_sequence`, `make_empirical_distribution_scenario` — all delegated |
| Import pattern | ⚠️ | Uses `importlib.import_module('19_3_module2_progression')` to import `ProgressiveRateFunction` etc. This works but is fragile — file rename breaks it silently. The progressive types should either be in `welfare_core` or a dedicated `welfare_progressive.py` |
| `_solve_aggregate_rate` | ✅ | Correctly does a brentq solve; uses `expected_tax` from `welfare_core` inside — good |
| `run_tier_comparison` rebuilds `SystemResult` manually | ⚠️ | Constructs `SystemResult(...)` directly with `state_taxes`, `state_wealth`, `state_cons` arrays. This is fine but note it bypasses `run_welfare_comparison` (which also constructs these arrays). The logic is duplicated rather than extracted — a minor maintenance risk |

**Actionable (medium priority):** The `importlib.import_module('19_3_...')` pattern is the most brittle thing in the pipeline. Move `ProgressiveRateFunction`, `tax_progressive_wdt`, `expected_utility_progressive`, `expected_tax_progressive` into a `welfare_progressive.py` module and import cleanly from there. Both Module 4 and Module 5 would benefit.

---

### `19_6_module5_sweeps.py`

| Area | Status | Detail |
|:---|:---|:---|
| `wdt_style` | ✅ | `apply_style()`, `save_fig()`, `FIG_PAIR`, `FIG_WIDE`, `FIG_WIDE_L`, `FIG_QUAD`, `DPI_SCREEN` |
| `wdt_fmt` | ✅ | `fmt_pct`, `fmt_pct0`, `fmt_pct4`, `fmt_gbp_m`, `today_iso` |
| `wdt_md` | ✅ | `MdDoc`, `md_table`, `LEFT`, `RIGHT`, `CENTER` — all used in `write_tables()` |
| `welfare_core` | ✅ | `run_welfare_comparison`, `expected_utility`, `expected_tax`, `consumption_equiv_welfare`, `solve_revenue_equivalent_rate`, `get_tax_fn`, `tax_symmetric_flat`, `make_*_distribution_scenario`, `make_scenario_sequence` — correctly delegated |
| `importlib` pattern | ⚠️ | Same `import_module('19_3_module2_progression')` fragility as Module 4 |
| `ScaledProgressiveRateFunction` | ⚠️ | Defined locally in Module 5. It subclasses `ProgressiveRateFunction` from Module 2, which was itself imported via `importlib`. This is a three-layer chain of fragile imports. |
| `solve_progressive_scale` | ✅ appropriate | Module-5 specific; fine to live here |
| `_make_dist_for_start` | ⚠️ | Reimplements the scenario-sequence rotation logic that already exists in `welfare_core.make_scenario_sequence`. The two differ: `_make_dist_for_start` uses modular wrap-around via list comprehension; `make_scenario_sequence` also does wrap-around. They should be the same call. |

**Actionable (medium priority):** `_make_dist_for_start(p, start_year, N)` in Module 5 should call `welfare_core.make_empirical_distribution_scenario` after temporarily mutating `p["returns"]["offset"]`, or `welfare_core` should expose a `make_distribution_for_start(p, start_year, N)` helper so Module 5 doesn't reimplement the rotation logic.

---

### `welfare_tables.py`

This file has the most issues — it is both the most complex and the least clean.

| Area | Status | Detail |
|:---|:---|:---|
| `wdt_md` | ✅ | `MdDoc`, `md_table`, `LEFT`, `RIGHT`, `CENTER` — all used correctly |
| `wdt_fmt` | ✅ | `fmt_pct`, `fmt_pct0`, `fmt_pct1`, `fmt_pct4`, `fmt_gbp_m`, `fmt_f2`, `fmt_f4`, `today_iso` — imported; most used |
| `wdt_style` | ❌ **not imported** | `welfare_tables.py` produces no charts, so no `wdt_style` import needed — that's correct. But `fmt_f2` and `fmt_f4` are imported and **not used** anywhere in the file. |
| `importlib` chain | ⚠️ | Uses `importlib` to import Modules 2, 3, 4, and 5 — all four with the fragile `19_*` naming. Module 5 is imported **twice** (once at the top before the per-module imports, then again with `_m5`). The first `_m5` binding is overwritten by the second. |
| `welfare_core` | ✅ | `run_welfare_comparison`, `dm_test`, `variance_of_consumption`, etc. — all delegated correctly in `main()` |
| `make_empirical_distribution` (full series) | ⚠️ | `main()` calls `make_empirical_distribution(p)` (full 73-year series, equal weight) for Modules 1–3, but the module scripts themselves call `make_empirical_distribution_scenario(p, N)` (N-year scenario window). This means the tables are computed on a **different distribution** than the module charts. |
| `table_wfr2` | ⚠️ | Contains dead code: `notax_vars = {}` is computed but never used; there's a "simpler version" comment that completely replaces the headers and rows defined above it, leaving the first `headers`/`rows` construction dead. |
| `table_wfr12` path unpacking | ✅ | Correctly handles the `(paths, years)` tuple from `run_concentration_analysis` |
| Column `fmt_f2`, `fmt_f4` | ❌ | Imported but not called anywhere in the file |

**Actionable (high priority — data integrity):** The `make_empirical_distribution(p)` vs `make_empirical_distribution_scenario(p, N)` mismatch in `welfare_tables.py` `main()` is the most serious issue. Tables WFR.1–4 are computed on the full 73-year series; Module 1 charts use the 30-year scenario window starting 2000. The numbers will differ, making appendix tables inconsistent with the paper's charts.

**Fix:** Replace in `welfare_tables.py main()`:
```python
# WRONG — uses full 73-year series
dist_A = make_empirical_distribution(p)
dist_B = make_idealised_distribution(p)

# CORRECT — matches what the module scripts use
N      = p["tcm"]["canonical_N"]
dist_A = make_empirical_distribution_scenario(p, N)
dist_B = make_idealised_distribution_scenario(p, N)
```

---

### Consolidated action list

| Priority | File | Issue | Fix |
|:---|:---|:---|:---|
| 🔴 High | `welfare_tables.py` | `make_empirical_distribution` vs `make_empirical_distribution_scenario` — tables inconsistent with module charts | Switch to `_scenario` variants with `N = p["tcm"]["canonical_N"]` |
| 🔴 High | `welfare_tables.py` | Module 5 imported twice; first binding silently overwritten | Remove the first `_m5` import block (lines before the per-module imports) |
| 🟡 Medium | `welfare_tables.py` | `fmt_f2`, `fmt_f4` imported but unused | Remove from import line |
| 🟡 Medium | `welfare_tables.py` | Dead code in `table_wfr2` (first `notax_vars`, first `headers`/`rows`) | Delete the dead block, keep only the "simpler version" |
| 🟡 Medium | All 19_* modules | `importlib.import_module('19_3_...')` fragile import chain | Extract `ProgressiveRateFunction` + progressive tax helpers into `welfare_progressive.py`; import cleanly |
| 🟡 Medium | `19_6_module5_sweeps.py` | `_make_dist_for_start` reimplements rotation logic from `welfare_core` | Expose `make_distribution_for_start(p, start_year, N)` in `welfare_core` and call it from Module 5 |
| 🟢 Low | All 19_* modules | `_save()` wrapper uses `dpi=DPI_SCREEN` (150) not `DPI_PRINT` (300) | Document the choice or remove the override |
| 🟢 Low | `welfare_core.py` | `variance_progressive` duplicated across Module 2 and implicitly in Module 5 | Optional: consolidate into `welfare_core` as a callable-based variant |
| 🟢 Low | Modules 1–4 | `wdt_md` not imported (no standalone table output per module) | No action needed if `welfare_tables.py` is the sole table producer |