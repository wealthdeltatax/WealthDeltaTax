# VALGEN tables and figures plan (for the next agent)

Status: plan only, nothing built. Written against `valgen_core.py` (P5 final, 63 checks pass), `valgen_data.json`, the old VAL presentation scripts (`5_3_VAL_tables.py`, `5_4_VAL_charts.py`, `5_5_VAL_generate_worked_examples.py`) and the wdt-model conventions.

**Rule for this plan: every figure has exactly one paired table. The table holds the numbers the figure draws, so a reader can check the picture.** Both read the same JSON key.

---

## 0. What the paper has to show

The figures serve one claim and its supporting evidence.

> **Claim.** Under the WDT no strategy has unbounded benefit, and the state does not need the true value of unvaluable assets. Under a conventional self-declared wealth tax, understatement is always a clear, unbounded benefit.

So the story order is:

1. **Headline contrast** (G12): conventional gain grows without bound as α falls; WDT best response stays small and bounded.
2. **Why it is bounded** (G1–G6): mechanics. Units are conserved, the Route C cap bites, Route D accrues and settles at reset, the corrective auction makes misstatement risky.
3. **How hard we tried to break it** (G7–G11, G13): 428-strategy search, rule-set ablation, λ, growth, shocks.
4. **Where it is not clean** (G10 plus the verdict table): the G3 near-miss on the stake. Show it, don't hide it.

---

## 1. Old items: disposition

The old VAL figures and tables describe the single-agent model (`val_core`, constant α, Route C only). They stay in the `val_core` pipeline untouched. **Do not regenerate or rewrite them in this task.** The paper rewrite (P6) decides what is retired.

Old figures that lack a dedicated table. These break the new pairing rule, so a small paired table must be added to `5_3` (or to a new `5_x` tables script) before the old chart set is considered compliant. Mapping below is from reading the scripts; verify before relying on it.

| Old figure | Closest existing table | Verdict |
|:--|:--|:--|
| Fig 5 rate function τ(W) | none | **Add** small table (τ at W = W_min, 5, 10, 20, 50, 100, 500, 1000 £m), values from `wdt_core.tau` via `p`. Reuse in the new paper as-is. |
| Fig 5.2a heatmap Net / TW | C.1, C.1b | OK |
| Fig 5.2b TW decomposition | C.11.1–C.11.5 | OK |
| Fig 7.1a overstatement coherence | C.1, C.1b, C.7 | OK (partly) |
| Fig 7.1b equilibrium cost curve | none exact | **Add** (α_fine × g_scenarios sample) |
| Fig 7.1c (g, N) surfaces | none | **Add** (cells at canonical N and a few g) |
| Fig 7.1d Net / TW / PV | C.1, C.1b, C.12 | OK |
| Fig 7.2a TW gap by N | C.8 | OK |
| Fig 7.2b / 7.2c reversal boundaries | none | **Add** (inflection and plateau stats, first-reversal g per α) |
| Fig 7.4 tolerance zone | C.12b.1, C.12b.2 | OK |
| Fig 7.5 ρ sweep | C.12b | OK |
| Fig 7.6 breakeven ρ | C.12b.3 | OK |
| Fig 7.7 uncertainty | C.13.1, C.13.2 | OK |

Likely to be superseded by the new work (do not decide, flag for P6): Figs 7.4–7.6 and the "state need not care about overstatement" framing (plan §10). The new evidence is the corrective-auction and conventional-baseline results.

Old table/figure numbering (C.x, 5.x, 7.x) is kept as is. The new set gets its own prefix so nothing collides.

---

## 2. New set: figure and table pairs

Provisional numbering `G1…G13`. Table IDs match (`Table G1` ↔ `Figure G1`). **Renumbering to the paper's real figure numbers is the user's call, at P6.** Filenames use the slug, so renumbering is cheap.

JSON source keys are in `valgen_data.json`. "Core gap" means the view is not in the JSON yet and the core must emit it (presentation never simulates, and heavy re-aggregation belongs in the core, not the chart script).

| ID | Figure | Table (same data) | JSON source | Status |
|:--|:--|:--|:--|:--|
| **G1** | **Units are conserved.** Round-trip units and oscillation of the benchmark plan: units paid/returned by year, honest vs misdeclared. | Per-year units and £ at declared vs true price. | `p2b_round_trip_units`, `p2b_oscillation`, `p2_benchmark_plan_s1` | ready |
| **G2** | **Worked example ledger.** One honest and one understater path, year by year: declared value, true value, liability, units paid, refund. | The ledger itself. | `bridge`, `examples` | ready; check which examples are stable after cleanup |
| **G3** | **α_C × α_D surface.** Two heatmaps: terminal-wealth gain and PV revenue change, with the conflict cells outlined. | Grid of both metrics, plus conflict cell list. | `p3_surface.cells` (key `alpha_C|alpha_D`), `p3_surface.conflict_cells` | ready |
| **G4** | **Route D reset sensitivity.** Gain vs reset interval. | Gain by interval. | `p3_reset_sensitivity` | ready |
| **G5** | **Dilution and Route C share.** Gain vs share of wealth in C, and the dilution effect. | Both sensitivities. | `p3_dilution`, `p4_C_share_sensitivity`, `p4_C_heavy_stress_gain` | ready |
| **G6** | **Corrective auction: verified share by year,** one line per λ. | Share by year (selected years) per λ. | `p4_lambda_sweep.by_lambda[λ].verified_share_by_year` | ready |
| **G7** | **Best response vs λ, by rule set (ablation chain).** Lines: base `units`, then each added rule, ending at `units_and_value/reset/on`. Shows what each rule buys. Horizontal reference = G1 threshold. | Best-response gain by rule × λ, with the strategy name. | `p5.search["{rule}|{lam}"].best` | ready |
| **G8** | **Verdict map.** Rule × λ grid coloured by pass/fail on G1, G2, G3. | G1/G2/G3 verdict table with the numbers behind each flag. | `p5.verdict_by_rule`, `p5.thresholds` | ready |
| **G9** | **Best response by strategy family** (constant, first_gen_only, late_deviation, correct_before_death, pre_reset_deviation, reset_gaming, k). Bar chart at λ_base, with 0% and 10% as markers. | Best gain per family per λ. | `p5.search[...].best_by_family` | ready |
| **G10** | **G3 scatter.** Each of the 428 strategies: terminal gain (x) vs PV revenue change (y), ±2% band, near-miss points labelled. | Worst conflicts: top N strategies by shortfall. | `p5.search[...].all`, `.worst_conflicts` | ready |
| **G11** | **Growth × λ surface** for the final rule. Heatmap with values printed. | The 5 × 5 grid. | `p5.growth_surface` | ready |
| **G12** | **Headline contrast.** Gain vs α (declaration ratio): conventional tax (rises without bound), WDT best response, no-tax ceiling as dashed line. | α, conventional gain, WDT best response (λ_base, plus λ=0 as worst case), ceiling. | `p5.conventional_baseline`, `p5.no_tax_ceiling`, `p5.search[...].all` | **core gap**: WDT best response by α needs a per-α aggregate emitted by the core (max over the other strategy dimensions). Do not reconstruct it in the chart script. |
| **G13** | **G2 shock cost.** Honest-taxpayer cost from the rule after a −20% / −50% shock at year 20, by rule and λ. | Cost by shock × rule. Final rule should read 0.000%. | `p5.g2_honest_shock_cost` | ready |

Recommended order in the paper: G12 first (it is the claim), then G7/G8/G9/G11 (the evidence), G10 and G13 (limits), then G1–G6 as mechanism appendix. A reader needs the contrast before the mechanics.

### Content specifics for the less obvious ones

- **G12.** x-axis α from 1 down to 0 (understatement increasing to the right), y-axis gain over honest (% of honest terminal wealth). The conventional curve uses `conv_extra_alphas` plus the grid. Note on the figure: conventional rate is calibrated to equal honest terminal wealth (1.207% a year); no audits modelled in the baseline. The no-tax ceiling (+236.6%) should be a labelled dashed line, not a data series, so the WDT curve is still readable (consider a broken axis or a second panel at the WDT scale). **The ceiling is a leak check, not a result; label it so.**
- **G7.** One panel, λ on x (0, 1, 2, 5, 10%), y best-response gain (%). One line per rule set. The ablation order is the order the rules were adopted: base → `units_and_value` → `reset` → `dauc on`. Read rule keys from `p5.rules`, do not hardcode.
- **G8.** Cells show the number inside (best response, stake change), colour shows pass/fail. G3 near-miss (−2.1% to −2.3% against the ±2% tolerance) must be visible as a fail, not rounded to a pass.
- **G10.** Axis units: use whatever the JSON stores (check: fractions vs pp; the old `val_core` chart matrices were pp, so label the unit in the key and the axis).

---

## 3. Files, layers, naming

Layer rules apply as per the wdt-model conventions: TOML → `wdt_core` → `valgen_core` → JSON → presentation. **Presentation never simulates and never imports `valgen_core`.**

| Item | Path | Note |
|:--|:--|:--|
| Core | `valgen_core.py` | existing; writes `OUTPUTS/VALGEN/valgen_data.json` via `save_json`. Add the G12 aggregate here. |
| Tables | `5_6_VALGEN_tables.py` | **proposed name**, continues VAL's numbering. Output to `OUTPUTS/VALGEN/tables/`. Use `MdDoc` / `md_table` (not bare `lines.append`, as `5_3` still does). |
| Charts | `5_7_VALGEN_charts.py` | **proposed name**. Output to `OUTPUTS/VALGEN/charts/`. Files `valgen_fig_{n}_{slug}.png`, 300 dpi via `save_fig`. |
| Params | `WDT_Params.toml` `[val_gen]` | add any new grid (e.g. `headline_alphas` if the G12 α grid is not the existing one). Nothing numeric in the scripts. |

Numbering of the two scripts follows the current VAL pattern; the target `{n}_2_`/`{n}_3_` renumbering is in the refactor map. **Confirm with the user** whether VALGEN is its own paper number or sits inside paper 5.

Conventions to hold:

- `apply_style()` first in every figure function. Sizes and colours from `wdt_style`; add a palette entry there for rule sets and strategy families (don't use inline hex as the old charts did).
- Each figure function takes the data dict and returns the saved path.
- Titles and captions are built from `p` and `meta`. **No literal parameter values.** In particular λ_base, thresholds (G1/G2/G3 tolerance), g, ρ, τ values all come from the JSON/TOML.
- Captions below tables in the "Table G7: …" form, with the parameters the numbers depend on.
- Each dataset carries its stamp (N, T, G). Add `_check_stamp` equivalents against `meta`.
- Percent vs fraction: the JSON stores raw fractions. Format in the presentation layer only.
- Shared helpers (heatmap with printed cells, verdict colouring) go in `wdt_md` / `wdt_style` / `wdt_fmt`, **not** shared between the two presentation scripts.

---

## 4. Pairing check (build this first)

Because the rule is "every figure has a table", enforce it mechanically rather than by review.

- Each script declares a module-level `PAIRS` dict, e.g. `{"G7": {"json": "p5.search", "caption": "Table G7"}}`.
- A small test `test_valgen_pairs.py` imports both presentation scripts and asserts: the set of figure IDs equals the set of table IDs; both reference the same JSON key; every figure PNG has a matching table file; the figure titles carry the same ID as the table.
- A number check: for each pair, pick 3 values from the table and assert the chart's plotted arrays contain them (figure function exposes its plotted series for this, or returns them with the path).

---

## 5. Build order

1. **Core gaps first.** Add the G12 per-α aggregate to `valgen_core.py` (and any per-strategy `pv_change` field G10 needs, if `all` doesn't already carry it). Re-run, confirm the 63 checks still pass and the existing results are unchanged (best response by λ, G1/G2/G3 flags, growth surface). **State explicitly if any number moves.**
2. **Pairing test and `PAIRS` skeleton**, with all 13 pairs stubbed (fails until filled).
3. **Evidence set first:** G12, G7, G8, G9, G11, G10, G13. These carry the claim.
4. **Mechanism set:** G3, G6, G4, G5, G1, G2.
5. **Old-figure gap tables:** Fig 5, 7.1b, 7.1c, 7.2b/c (small additions to the old tables script).
6. **Check pass:** run pairing test; open every PNG; compare 3 table numbers per pair to the JSON; confirm captions have no literals.
7. Then P6 (paper rewrite) uses the final numbers.

---

## 6. Decisions the next agent should not make alone

- Final figure numbers and whether VALGEN is a separate paper or an addendum to paper 5.
- Which old figures (esp. 7.4–7.6) are retired in the rewrite.
- Whether G12 should include a conventional baseline *with audits* (currently none; the comparison is therefore generous to the conventional tax's detection and unfair to it in that sense: stated on the figure).
- Whether the G1/G2/G3 thresholds (1% / 1% / ±2%) stay as placeholders in the figures. They are drawn from `p5.thresholds`; if they change, the verdict map changes with them.
- λ_base = 5% is a placeholder and λ is a framing device (exogenous); G7/G8/G11 show the full λ range so no single λ carries the claim. Keep it that way.

## 7. Caveats the figures must carry

- Strategy search is a **lower bound** on the true best response (428 strategies, not an optimiser).
- One parameter point (τ0 .15, τm .70, k .001, W_min £2m, V0 £20m, g 10.45%, ρ 5%) apart from the growth × λ surface.
- Residual gain at low λ (up to +4.4% at λ=0) is late understatement before death; probably linked to the heir inheriting the declared basis (D4/D6). Not yet analysed; no figure for it. **Candidate extra figure/table pair if the user wants it** (heir/generation view): needs a core view first.
- G3 stake near-miss −2.1% to −2.3% against ±2%.
- Failed assets are not modelled (D-list).
