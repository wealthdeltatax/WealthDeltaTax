# WDT Data Audit Specification

Status: draft for review, 14 October 2026. Theory decisions settled; no research done yet.
Purpose: define, before any sourcing, what data the model extensions need, how each item will be graded and used, and what would stop us proceeding.

**Source caveat.** Every source named below is a candidate recalled from memory. None has been opened or verified. Mark each `unverified` in the register until opened.

---

## 1. Decisions this audit supports

| Area | Settled decision |
|:---|:---|
| c level | Per-country constant, observed from history. Seams interpolated and flagged. |
| c shape | Varies with wealth, per country. Rescaled so the wealth-weighted mean equals the country constant. Net drawdown (consumption minus saving); may be negative. |
| Saving | Taxable as delta. Include it and decompose it (returns versus saving inflow), by band and for entrants. |
| Entry | Calibrate on aggregate wealth/GDP and micro saving. Validate on ownership. Ownership tracked in full, no mortgage adjustment, unless better data supersedes it. |
| W_min index | Baseline GDP/head. House-price index as a named sensitivity. |
| CORP | tau_corp = attributable rate. Natives net it against WDT (income-neutral). Attributed foreign pay it flat as a final charge. tau_h = final rate on unattributed. tau_prov = internal accounting only. Two calibrations presented side by side: (A) to current CIT revenue, (B) to comparable company burden. |
| Incidence | CIT incidence unknown. Treat as a swept parameter, applied symmetrically to CIT retired and levy introduced. Employer NI saving treated as a firm-side saving, independent of employee NI, not allocated to individuals. |
| Net-change display | By wealth group, before and after, in three metrics: £ per adult, % of income, % of wealth (plus % of return at the top). |
| Scope | Pre-behavioural throughout. Population growth not modelled separately. Dynamic threshold path deferred. |
| T | Several horizons. |

---

## 2. Principles

1. **No tuning to outcomes.** Data fixes inputs or provides validation. A dataset may not be used for both on the same sample.
2. **Provenance on every number.** Each series carries the fields in section 5.
3. **Supersession rule.** If better data than the stated candidate is found, it replaces the candidate. Log the swap and the reason.
4. **Definition fidelity.** The model's wealth is household net worth per adult including pension wealth (WAS-style). Mismatched definitions (national wealth, financial wealth only, gross of debt) are allowed but graded and flagged.
5. **Real terms.** All series real, deflated by the country's CPI, per adult unless stated. State the base year.
6. **Timing.** Model sim year t uses data year `start + t - 1`. Wealth is measured against GDP/head at the end of `start - 1`. Align all new series to that convention.

### Quality grades

| Grade | Meaning |
|:---|:---|
| A | Official or primary source, definition matches the model. |
| B | Secondary or derived, definition differs in a documented way. |
| C | Imputed, pooled across countries, or fallback. Must be flagged in every output that uses it. |

### Interpolation and gaps

- Interpolate linearly in log level between benchmark years.
- Maximum interpolated gap is a parameter (suggested default 10 years).
- Interpolated values carry flag `interp`. Beyond the maximum gap the value is `missing`, not filled.
- War and hyperinflation breaks are `break`, never bridged.

---

## 3. Datasets

Each entry gives the variable, the model hook, candidate sources, required coverage, fallback and acceptance gate.

### D0. Internal JST audit (no research needed)

Run first, on the existing file.

- **Variables:** `capital_tr`, `eq_capgain`, `gdp`, `pop`, `cpi`, `hpnom`, `revenue`, `expenditure`.
- **Output per country and variable:** first and last usable year, number of gaps, longest contiguous span, flagged years.
- **Why:** explains the 69 contiguous windows out of 1,728, shows which countries have house-price and equity data, and gives window counts for each candidate T.
- **Gate:** none. It informs every later choice.

### D1. Household wealth/GDP history (drives c level)

- **Variable:** household net worth (or private wealth) / GDP or national income, by country and year, with the volume (saving) versus price (revaluation) decomposition where available.
- **Hook:** per-country c in the TOML via `c_mode = "observed"`.
- **Two routes, to be reconciled:**
  - *Identity route:* c = 1 - (1 + g_{W/Y}) (1 + g_pc) / (1 + r), using real r from the same basket the engine grows. The constant c per country is the root that reproduces the observed endpoint W/Y over the usable span. Also report era sub-spans.
  - *Flow route:* net household saving over wealth plus revaluation mismatch, from national accounts or the Piketty–Zucman decomposition.
- **Candidates (unverified):** Piketty–Zucman national wealth series, WID, OECD national accounts, national statistical offices.
- **Fallback:** pooled cross-country c, grade C and flagged.
- **Gate (suggested):** at least 8 of 16 countries with at least 50 usable years; the rest on the fallback.

### D2. Consumption and saving by wealth (drives c shape)

- **Variable:** relative net drawdown rate by wealth percentile, anchors in ln W, with uncertainty.
- **Hook:** shape curve in `_c_cell`, rescaled to the country c by the constrained-absorb device already used for `payout_top`.
- **Candidates (unverified):** Saez–Zucman (2016), Fagereng–Holm–Moll–Natvik (2019), Mian–Straub–Sufi, Dynan–Skinner–Zeldes (2004), Scandinavian register studies, UK WAS.
- **Hierarchy:** country-specific where observed, otherwise a pooled shape, grade C, flagged.
- **Note:** shape is material. The top-6%-consume-1% scenario moves coverage from 26% to 35%.
- **Gate (suggested):** shape evidence for at least the UK, US and one Nordic country; others pooled.

### D3. Ownership and scope share (validation, not calibration)

- **Variables:** owner-occupancy rate; outright (mortgage-free) ownership rate where available; share of adults above the median house value in net wealth.
- **Hook:** model diagnostic `scope_share_t` (adults with W/idx >= W_min each year) compared with the observed path.
- **Mapping:** scope_share is approximately ownership times the share of owners above W_min. Track full ownership first, per your decision, and do not assume the second factor is constant.
- **Candidates (unverified):** national censuses, Eurostat, UK ONS and housing surveys.
- **Validation rule:** set the tolerance before running. If validation fails, say so; do not recalibrate on ownership.
- **Gate (suggested):** UK and US full series; others sparse benchmarks with interpolation.

### D4. Equity ownership and market capitalisation (drives CORP shares)

- **Variables:** share of listed equity held by households, pension funds, insurers, other financial institutions, public sector, charities, rest of world; market capitalisation / GDP; by country and year.
- **Hook:** per-year tranche shares in `levy_path` in place of the scalars `f_inc`, `f_attr`, `mc_gdp`.
- **Candidates (unverified):** ONS Ownership of UK quoted shares (UK, long history), OECD and national flow-of-funds, World Bank financial structure data, long-run equity-market histories.
- **Attribution shares** (what share of intermediary holdings is attributable) are not observed. Treat as a swept parameter with UK-based anchors.
- **Foreign share is exogenous** to the tax (pre-behavioural; state it).
- **Gate (suggested):** UK history from first available year; other countries by era with grade C fallback.

### D5. Corporate tax base and burden (drives calibrations A and B)

- **Variables:** CIT revenue / GDP, statutory rate, corporate profits / GDP, by country and year; UK current 3.2% of GDP.
- **Calibration A:** median net state revenue from the levy equals CIT revenue.
- **Calibration B:** gross company-paid levy equals comparable company burden. Requires a definition decision: gross levy / GDP, or effective rate on profits. Obtain both measures so the choice can be made on evidence.
- **Candidates (unverified):** OECD Revenue Statistics, HMRC corporation tax statistics, national accounts for profits.
- **Note:** JST has only total revenue, not CIT.
- **Gate (suggested):** UK full; others only if profits series exist.

### D6. Baseline burden allocation (drives the net-change display)

- **Variables:**
  - CGT and IHT by wealth or estate band (HMRC statistics).
  - Income tax and employee NI paid, by wealth band (requires a joint income-by-wealth cut of WAS to replace the placeholder `income_by_wealth` profile).
  - CIT incidence range from the literature, to bound the owner share swept.
  - Employer NI aggregates (firm-side line).
- **Hook:** `band_net_position`, extended with before-and-after taxes by band.
- **Sweep:** CIT owner share at 100%, 50%, 25% (suggested), applied identically to the levy.
- **Gate:** if the joint cut is unavailable, the net-change display must say the income profile is a placeholder.

### D7. House prices

- **Variables:** JST `hpnom` coverage and house-price / income by country and year.
- **Hook:** the `house` index mode (sensitivity) and the ownership validation.
- **Gate:** D0 reports coverage. Windows without house prices drop under that mode; record how many.

### D8. Historical wealth concentration (context only)

- **Variables:** top 1% and top 0.1% wealth shares over time.
- **Hook:** none directly. The distribution is a 2016–18 snapshot; this dataset shows how far history departs from it.
- **Candidates (unverified):** WID, Alvaredo et al.
- **Priority:** low.

### D9. Demographic conventions (documentation only)

- **Variables:** adults per head (`pop_per_adult`, currently fixed at 1.27), generation gap, age at inheritance.
- **Hook:** none. Record the convention and its historical range.

### D10. Placeholder register

Source or replace every placeholder the tables depend on:

| TOML item | Status now |
|:---|:---|
| `house_median_gbp_m` | Placeholder (£0.225m) |
| `f_inc`, `f_attr` | Placeholder and ONS-derived respectively |
| `mc_gdp` | Sourced, year-matched, verify |
| `employer_share` | Judgment (0.25) |
| `income_by_wealth` | Placeholder |
| taxpayer-count curves, leg shares | Placeholder |
| `adults_m`, `motivated_gbp` | Placeholder, judgment |
| cohort premium levels (high) | Placeholder, no source above top 1% |
| `lambda_base`, `brg_tol`, `hsc_tol`, `hec_phi` | Framing or placeholder |

---

## 4. Procedure and gates

1. **D0** (now): internal JST audit; produce the coverage matrix and window counts for candidate T values.
2. **D1, D4, D3:** coverage census first (what exists, for which countries and years), then definitions, then extraction.
3. **D2:** micro evidence for c shape, per country where possible.
4. **D5, D6, D10:** calibration targets and baseline burdens.
5. **Decision review:** for each gate, record pass, fallback or fail, and what the fallback changes in the claims.

**Rule:** a failed gate does not block the project. It forces a flagged fallback and a weaker claim for the affected countries.

---

## 5. Deliverables

| File | Contents |
|:---|:---|
| `coverage_matrix.csv` | country x dataset x first/last year x grade x gaps |
| `c_country.csv` | country, c, span, route (identity or flow), grade, interpolation share |
| `c_shape.csv` | country, ln W anchors, relative c, uncertainty, grade |
| `provenance_register.md` | one row per series: source, citation, vintage date, definition, transformation, status (`verified` or `unverified`), flags |
| `decision_log.md` | supersessions, fallbacks and gate outcomes |
| `placeholder_register.md` | section D10 with status after the audit |

Provenance fields: `series`, `country`, `source`, `citation`, `vintage`, `definition`, `units`, `real_base`, `transformation`, `grade`, `flags`, `verified`.

---

## 6. What the data must support

- **c:** split-sample test. Calibrate on early years, test drift on later years. Same-sample matching is an identity, not a test.
- **Tax-off control:** untaxed model drift versus observed wealth/GDP drift per country and era. This tests the hypothesis that untaxed wealth/GDP grows consistently.
- **Entry:** model `scope_share_t` versus observed ownership, with tolerance set beforehand.
- **CORP:** annual levy / CIT ratio distribution, volatility and shortfall years under calibrations A and B.
- **Net-change display:** a before-and-after table by wealth group that can show non-neutrality at the top as well as neutrality.

---

## 7. Out of scope and deferred

- Behavioural response (migration, avoidance, restructuring).
- Dynamic income-tax threshold path.
- General-equilibrium incidence (assigned to MACRO).
- Entry module beyond endogenous saving, unless validation fails.
- Equity-settlement loan terms (pending CORP mechanics).

---

## 8. Open items

1. Define "comparable company burden" for calibration B (gross levy / GDP versus effective rate on profits).
2. Decide the CIT owner-share sweep values after D6.
3. Set the ownership validation tolerance.
4. Choose maximum interpolation gap and its sensitivity.
