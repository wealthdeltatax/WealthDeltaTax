# Plan: WFR.A §F — Extended Concentration Horizon (N=73)

## What the section needs to contain

The WFR main paper §7.4 now states:

> "The N=73 concentration sensitivity — running the full historical return sequence from
> 1947 to 2019 — is included in (WFR.A §F) as an additional appendix result. It
> establishes the horizon at which the progressive WDT concentration advantage first
> becomes visible and traces its magnitude through the full empirical dataset."

§F therefore needs:

1. **F.1 — Setup and scope statement**: clarify what changes relative to Section D
   (same tiers, same systems, same parameters — only the horizon extends from N=30
   to N=73 using the full 1947–2019 return sequence)

2. **F.2 — Extended concentration path table**: Great/Poor ratio at key years from
   initial through N=73, for all systems, showing when the flat-vs-progressive WDT
   gap opens up

3. **F.3 — Horizon crossover table**: for each pair (flat WDT vs progressive WDT),
   the first year at which their concentration paths diverge beyond a meaningful
   threshold (e.g. >1× difference in ratio) — this is the "when does the progressive
   advantage become visible" result §7.4 promises

4. **F.4 — All-tier concentration at N=73**: full four-tier concentration matrix at
   the terminal horizon across all systems, analogous to D.3 but at N=73

---

## Current §F

Currently §F is the Parameter Reference table. That needs to be renumbered.
Options:
- Move Parameter Reference to §G (shift everything)
- Keep Parameter Reference as §F.0 or a standalone unnumbered section before §F.1
- Most consistent with appendix style: rename current §F to §G (Parameter Reference),
  insert new §F as the N=73 section

**Decision: rename current §F → §G; new §F = N=73 concentration sensitivity.**

---

## What the Python model needs to produce

### New script: `19_3_wfr_concentration_extended.py`
(following existing naming convention for WFR output scripts)

Output directory: `OUTPUTS/WFR/` (matching the other WFR scripts)

---

## Inputs the script requires

### From existing model infrastructure
- `wdt_core.load_params()` — for rate function τ(W) and canonical parameters
- `p['returns']` — the 73-observation UK historical equity return series (1947–2019),
  already loaded by `load_params()` from the JST dataset in TOML
- `wdt_core.tau(W, p)` — logistic rate function for progressive WDT
- `wdt_style`, `wdt_md`, `wdt_fmt` — standard infrastructure

### Parameters defined locally in the script (not in TOML)
These are WFR-specific, not part of the core rate/SWF model:

| Parameter | Value | Source |
|:---|:---|:---|
| Tier wealth levels W₀ | Poor £2.9m, Ok £7.1m, Good £19.9m, Great £139.6m | D section |
| Tier return differentials | Poor −4.55pp, Ok −2.05pp, Good +0.95pp, Great +3.45pp | Fagereng (2020) |
| Base equity mean r̄ | 10.45% | JST dataset |
| Revenue-equivalent flat rates | From D section (already computed) | D section |
| γ | 2.0 | Canonical |
| N_extended | 73 | Full dataset length |
| Start year | 1947 | First JST observation |
| Convergence threshold for crossover detection | 1.0× ratio difference | New |

---

## Core simulation logic

### Per-tier wealth path (one function, called for each system × tier)

```
W_t+1 = W_t × (1 + r_tier_t) - tax_t + refund_t
```

Where:
- `r_tier_t` = historical return in year t + tier_differential
  (tier differential shifts the base JST return each year — same shift applied
  uniformly, not a separate draw)
- `tax_t` and `refund_t` depend on the system:

| System | tax_t | refund_t |
|:---|:---|:---|
| Flat WDT | τ_flat × max(ΔW, 0) | τ_flat × max(−ΔW, 0) |
| Progressive WDT | τ(W_t, p) × max(ΔW, 0) | τ(W_t, p) × max(−ΔW, 0) |
| Stock Wealth Tax | τ_swt × W_t | 0 |
| Income Tax | τ_it × max(r_tier_t × W_t, 0) | 0 |
| Consumption Tax | τ_ct × W_t | 0 (equivalent to SWT in this model) |
| No-tax | 0 | 0 |

Note: ΔW = W_t × r_tier_t (the raw wealth delta before tax; the WDT base)

Revenue-equivalent rates (τ_flat, τ_swt, τ_it, τ_ct) are carried forward from
the D section computation — they are solved at N=30 and held fixed for the N=73
extension. This is correct: we are asking what happens to concentration if the
same tax system is applied for longer, not re-solving for revenue equivalence at N=73.

### Great/Poor ratio at each year t

```
ratio_t = W_Great_t / W_Poor_t
```

Computed for all systems simultaneously.

### Crossover detection

For each year t from N=30 onward, compute:
```
gap_t = ratio_progressive_t - ratio_flat_t
```

The crossover year is the first t at which gap_t > threshold (1.0× suggested;
may need adjustment once simulation runs — use the first year where the two
lines are visually distinct rather than floating-point noise).

---

## Outputs required

### Table F.2 — Extended concentration path (all systems, key years)

Years: Initial (1947), 1957, 1967, 1977, 1987, 1997, 2007, 2019 (N=73)
Plus: 2000 (matching D.3 start) and 2029 (matching D.3 endpoint) if within range

Columns: System | 1947 | 1957 | 1967 | 1977 | 1987 | 1997 | 2007 | 2019

Rows: all six systems (Flat WDT, Progressive WDT, Stock Wealth Tax, Income Tax,
Consumption Tax) — no No-Tax row (ratio is trivially constant in D section terms)

Format: ratio as "NNN×" to one decimal place (e.g. "286.3×")

### Table F.3 — Flat vs Progressive WDT: crossover horizon

One-row summary table:

| Metric | Value |
|:---|:---|
| Great/Poor ratio: Flat WDT at N=30 | 286.3× |
| Great/Poor ratio: Progressive WDT at N=30 | 288.1× |
| Gap at N=30 | 1.8× (Progressive higher — i.e. slightly worse) |
| First year progressive WDT below flat WDT | [computed] |
| Gap at crossover year | [computed] |
| Great/Poor ratio: Flat WDT at N=73 | [computed] |
| Great/Poor ratio: Progressive WDT at N=73 | [computed] |
| Gap at N=73 | [computed] |

Note on sign: At N=30 the progressive WDT shows *higher* concentration than flat
(288.1× vs 286.3×) — counterintuitive but explained by the logistic operating near
its entry rate so the progressive schedule collects only marginally more from the
Great tier. The crossover question is whether this inverts at longer horizons.

### Table F.4 — All-tier concentration matrix at N=73

Analogous to D.3 but at terminal horizon. Rows = systems; columns = tier pairs.
Primary column: Great/Poor. Secondary columns: Great/Ok, Ok/Poor (to show
where the progressive advantage manifests by tier, if it does).

| System | Great/Poor | Great/Ok | Ok/Poor |
|:---|---:|---:|---:|
| Flat WDT | [N=73] | [N=73] | [N=73] |
| Progressive WDT | [N=73] | [N=73] | [N=73] |
| Stock Wealth Tax | [N=73] | [N=73] | [N=73] |
| Income Tax | [N=73] | [N=73] | [N=73] |
| Consumption Tax | [N=73] | [N=73] | [N=73] |

### Figure F.1 — Concentration path: Flat vs Progressive WDT, N=73

Single panel. X-axis: year (1947–2019). Y-axis: Great/Poor ratio.
Two series: Flat WDT (solid blue), Progressive WDT (dashed blue).
Vertical reference line at 1977 (N=30 equivalent from the 1947 start).
Annotation: gap at N=30, gap at N=73, crossover year if it occurs.
Purpose: the visual that §7.4 promises — showing when/whether the progressive
advantage on concentration becomes visible.

### Figure F.2 — Full concentration path: all systems, N=73

Analogous to existing Figure 4.3.2 in WFR main paper but extended to N=73.
Five series (all systems). Two-panel: left = ratio trajectories; right = per-tier
wealth growth normalised to W₀=1.
Vertical reference line at N=30 (year 1977 from 1947 start) to anchor the
comparison against D.3.

---

## Key analytical question the output must answer

§7.4 says:

> "The expectation, following from the logistic geometry, is that the progressive
> advantage on concentration begins to emerge as cumulative wealth growth pushes
> the tested tiers higher up the logistic curve and the effective rate differential
> between Great and Poor widens."

The script must either confirm or disconfirm this. Two possible outcomes:

**Outcome A — crossover occurs within N=73**: Progressive WDT concentration
drops below flat WDT concentration at some year t*. The table and figure show t*,
the magnitude of the gap at N=73, and the trajectory. The §7.4 expectation is
confirmed. The finding is: the flat-progressive axis is relevant but only at
horizons beyond the canonical 30-year window.

**Outcome B — no crossover within N=73**: Progressive WDT concentration remains
higher than or equal to flat WDT throughout. This means the logistic geometry
does not produce a visible progressive advantage even at the full empirical
horizon. The §7.4 expectation is disconfirmed. The finding would be: at canonical
parameters, progressive WDT does not outperform flat WDT on concentration at
any empirically observed horizon. This is a legitimate and interesting result —
it means the WFR §7.4 language ("the progressive advantage would emerge at longer
horizons") requires qualification or revision.

The script must be written to detect both outcomes cleanly and the appendix prose
must state which one occurred.

---

## What does NOT need to change

- Sections A–E of WFR.A: unchanged
- The D.3 table (N=30): reference anchor, not replaced
- The revenue-equivalent rates: carried forward from Section D, not re-solved
- The tier parameters: identical to Section D
- The return series: same JST data, now used for all 73 years rather than
  the 30-year window starting in 2000

---

## Appendix structural change required

Current WFR.A structure:
```
# A. Baseline Single-Agent Comparison
# B. Progressive Rates and the Three D-M Complications
# C. CGT Lock-In Distortion
# D. Heterogeneous Agents — Incidence and Concentration
# E. Welfare Sweep Analysis
# F. Parameter Reference       ← currently here
```

New structure:
```
# A. Baseline Single-Agent Comparison
# B. Progressive Rates and the Three D-M Complications
# C. CGT Lock-In Distortion
# D. Heterogeneous Agents — Incidence and Concentration
# E. Welfare Sweep Analysis
# F. Extended Concentration Horizon (N=73)   ← new section
# G. Parameter Reference                      ← renamed from F
```

The WFR.A revision history should log this structural change.
The WFR main paper cross-reference (WFR.A §F) in §7.4 already points to the
new §F — the §G rename of Parameter Reference needs no cross-reference update
since nothing else in the main paper cites (WFR.A §F) for parameters (they are
cited inline by value).

---

## Estimated scope

- ~150 lines of new Python
- One new output script (`19_3_wfr_concentration_extended.py`)
- Two new figures (F.1 and F.2)
- Three new tables (F.2, F.3, F.4)
- Prose for F.1 (setup), plus interpretation paragraphs after each table
- WFR.A revision history update
- Current §F → §G rename in the appendix file
