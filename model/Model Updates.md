Perfect. That's clean and complete. Let me restate the failure conditions precisely and then write the full plan.

---

## Failure conditions

**LRR hits zero** — the buffer is exhausted. The LRR cannot go negative. Record `lrr_failure_year`. This is the primary failure signal: the political buffer is gone and any further SRR deficit has no backstop.

**SRR hits zero** — by definition the LRR is already at zero when this happens (because the LRR covered SRR deficits until it was exhausted, so LRR hits zero first). Record `srr_failure_year`. This is the terminal failure: the refund guarantee is mechanically broken.

The ordering is always LRR failure → SRR failure, never the reverse. If the LRR hits zero and the SRR subsequently runs a deficit, the SRR just runs a deficit unmet — record the SRR failure year when SRR balance hits zero.

The gap between `lrr_failure_year` and `srr_failure_year` (if both occur) tells you how long the system limps after the buffer is exhausted before the refund guarantee itself breaks. That gap is a meaningful policy signal.

---

## The complete plan

### 1 — Capitalisation window (no change)

Everything up to and including LRR fill is unchanged. The SSM runs year by year, SRR fills, surplus flows to LRR, LRR hits its floor target. Record `srr_fill_year`, `lrr_fill_year`, `lrr_balance_at_fill`, `srr_balance_at_lrr_fill`.

---

### 2 — Post-fill mechanic (new, replacing the current post-fill block)

Each year t after `lrr_fill_year`, in strict priority order:

**Step 1 — SRR from income:**
```
srr_target_t  = srr_ratio × (cum_net / N)
srr_gap_t     = max(0, srr_target_t - srr_bal)
srr_contrib_t = min(max(net_t, 0), srr_gap_t)
srr_bal      += srr_contrib_t
remainder_t   = net_t - srr_contrib_t
```

**Step 2 — LRR floor maintenance from remainder:**
```
lrr_target_t  = lrr_years × budget_t
lrr_gap_t     = max(0, lrr_target_t - lrr_bal)
lrr_contrib_t = min(max(remainder_t, 0), lrr_gap_t)
lrr_bal      += lrr_contrib_t
remainder_t  -= lrr_contrib_t
```

**Step 3 — LRR covers remaining SRR deficit (if any):**
```
srr_still_short = max(0, srr_target_t - srr_bal)
lrr_to_srr_t   = min(lrr_bal, srr_still_short)
lrr_bal        -= lrr_to_srr_t
srr_bal        += lrr_to_srr_t

if lrr_bal == 0 and lrr_failure_year is None:
    lrr_failure_year = t

if srr_bal <= 0 and srr_failure_year is None:
    srr_failure_year = t
```

**Step 4 — Surplus above SRR target tops up LRR toward floor:**
```
if srr_bal >= srr_target_t and remainder_t > 0:
    lrr_headroom  = max(0, lrr_target_t - lrr_bal)
    lrr_topup_t   = min(remainder_t, lrr_headroom)
    lrr_bal      += lrr_topup_t
    remainder_t  -= lrr_topup_t
```

**Step 5 — Labour tax relief:**
```
available_t = max(0, remainder_t)
cov_frac_t  = available_t / budget_t
```

If either failure condition has already been reached in a prior year, coverage is zero from that point forward. The model continues running to record trajectories but flags all subsequent years as post-failure.

---

### 3 — Coverage windows

After the post-fill loop completes, for each window length W in {5, 10, 20, 50}:

- Take the `cov_frac_t` values for post-fill years 1 through W (wrapping the return series cyclically if needed — already handled by the rotated series)
- Compute average SSM coverage fraction over W years
- Record number of zero-coverage years in that window
- Record minimum LRR balance in that window
- Record years where LRR balance was below its own floor in that window

This produces 4 SSM window outputs per start year.

---

### 4 — TCM rework

The TCM is restructured from a single-horizon integral into a year-by-year marginal accumulator, matching the SSM structure.

**For each post-fill year t**, for each tier × bracket cell, the TCM computes marginal net revenue: simulate to year t with tier differential applied to the rotated return series, simulate to year t-1, take the difference. Aggregate across all tier × bracket cells with population weights to get `tcm_net_t` in £b. Apply the same priority ordering (Steps 1–5) using `tcm_net_t` in place of `ssm_net_t` — but using separate SRR and LRR balance trackers so the SSM and TCM run independently.

Compute `tcm_cov_frac_t = tcm_available_t / budget_t` and average over the same {5, 10, 20, 50} windows.

This produces 4 TCM window outputs per start year. TCM is expected to be higher than SSM in most years because heterogeneous tier returns are less correlated than the SSM's uniform shock — making SSM the lower bound and TCM the upper bound of the justifiable range.

---

### 5 — Metrics retired

- `lrr_breach_year` — replaced by `lrr_failure_year`
- `years_fill_to_breach` — replaced by gap between failure years if both occur
- `max_lrr_breach` — replaced by minimum LRR balance in each window
- `srr_breach_covered` — retired, no longer meaningful under new mechanic
- `ssm_post_fill_coverage` (old) — replaced by 4-window SSM averages
- `tcm_post_fill_coverage` (old) — replaced by 4-window TCM averages

---

### 6 — Metrics added

Per start year:
- `lrr_failure_year` (None if LRR never hits zero within 71-year window)
- `srr_failure_year` (None if SRR never hits zero)
- `lrr_srr_failure_gap` (years between the two failures, if both occur)
- For each window W in {5, 10, 20, 50}:
  - `ssm_cov_W` — average SSM coverage fraction
  - `tcm_cov_W` — average TCM coverage fraction
  - `zero_cov_years_W` — count of zero-coverage years in window
  - `min_lrr_bal_W` — minimum LRR balance in window
  - `lrr_below_floor_years_W` — years LRR was below its rising floor

---

### 7 — Sweep table and reporting

The sweep table gains the new coverage columns (likely show 10yr window as the headline, with others available). The extremal dimensions are redefined:

- **Speed:** unchanged — fastest and slowest LRR fill year
- **Margin:** unchanged — thinnest and largest LRR surplus at fill
- **Durability:** redefined — highest and lowest 50yr average coverage fraction (replaces breach lag, which was an artefact)
- **Resilience:** new dimension — latest and earliest LRR failure year (or "no failure" as best case)

The statistical pass gains distribution tables for each coverage window across all 73 start years and across the cycle buckets.

---

### 8 — Files affected

- `rates_model.py` — SSM post-fill block rewrite, TCM full rewrite, new metrics, new statistics
- `rates_output.py` — sweep table columns, statistical pass tables, extremal reporting
- `revenue.html` (tool) — summary boxes and SWF milestones section updated to show coverage range rather than LRR breach metrics
- Module docstring and ARCHITECTURE comment updated throughout

---

### 9 — What does not change

- The capitalisation window (SSM up to LRR fill)
- The marginal cohort approach and bracket × tier structure
- The rotated return series and 73-year sweep
- The `budget_t` growing denominator (conservative, no displacement feedback)
- The SRR target formula throughout
- The TCM's internal simulation engine (`simulate`, `simulate_sell_year`) — only the outer loop and aggregation change
- `wdt_core.py` — untouched

---

That is the complete plan. When you're ready to implement, the natural order is: SSM post-fill block first, verify the failure conditions and coverage fractions are behaving sensibly on a single start year, then extend to the sweep, then rework the TCM, then update reporting.