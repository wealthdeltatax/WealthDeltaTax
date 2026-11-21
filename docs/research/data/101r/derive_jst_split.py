#!/usr/bin/env python3
"""101r block 2a: JST cash-yield / holding-gain split statistics, reproduced from 100r output.

Run: python -I docs/research/data/101r/derive_jst_split.py
Reads  docs/research/data/100r/returns_decomposition.csv (117 UK years 1896-2019, 1940-46 absent)
       docs/research/data/101r/derived_ons_flows.csv (for the ONS housing-services cross-check)
Writes docs/research/data/101r/jst_split_stats.csv
Arithmetic means of annual real/nominal components. Geometric (I-D1a2) does not split additively.
Tolerance vs 100r headline table: 0.0006 pp (the note reports 3 decimals).
"""
import csv, os, statistics as st, sys

HERE = os.path.dirname(os.path.abspath(__file__))
rows = [{k: float(v) for k, v in r.items()}
        for r in csv.DictReader(open(os.path.join(HERE, "..", "100r", "returns_decomposition.csv")))]
for r in rows:
    r["year"] = int(round(r["year"]))
assert len(rows) == 117, len(rows)

HEAD = {  # 100r headline, percent
    "portfolio_y_nominal": 4.197, "portfolio_g_nominal": 4.274, "capital_tr_nominal": 8.471,
    "portfolio_y_real": 4.034, "portfolio_g_real": 0.708, "capital_tr_real": 4.742,
}
out, bad = [], 0


def stat(period, lo, hi, col):
    v = [100 * r[col] for r in rows if lo <= r["year"] <= hi]
    return len(v), st.mean(v), (st.stdev(v) if len(v) > 1 else float("nan")), min(v), max(v)


PERIODS = [("all_1896_2019", 1896, 2019), ("1896_1939", 1896, 1939), ("1947_1979", 1947, 1979),
           ("1980_2019", 1980, 2019), ("1998_2019_ons_overlap", 1998, 2019)]
COLS = ["portfolio_y_real", "portfolio_g_real", "capital_tr_real", "portfolio_y_nominal", "portfolio_g_nominal",
        "capital_tr_nominal", "equity_y_real", "equity_g_real", "housing_y_real", "housing_g_real",
        "bond_y_real", "bond_g_real", "bill_y_real", "bill_g_real", "weight_equity", "weight_housing",
        "weight_bond", "weight_bill", "cpi_inflation", "housing_y_nominal", "equity_y_nominal"]
for p, lo, hi in PERIODS:
    for c in COLS:
        n, m, sd, mn, mx = stat(p, lo, hi, c)
        out.append((p, c, n, round(m, 4), round(sd, 4), round(mn, 4), round(mx, 4), "pct (weights: pct of portfolio)"))
    # yield share of total return (ratio of means; arithmetic, not a per-year average of ratios)
    ny = st.mean([r["portfolio_y_real"] for r in rows if lo <= r["year"] <= hi])
    nt = st.mean([r["capital_tr_real"] for r in rows if lo <= r["year"] <= hi])
    out.append((p, "yield_share_of_total_real_ratio_of_means", len([1 for r in rows if lo <= r["year"] <= hi]),
                round(ny / nt, 4), "", "", "", "ratio"))

# reproduction check vs 100r headline
for c, h in HEAD.items():
    m = st.mean([100 * r[c] for r in rows])
    d = m - h
    ok = abs(d) <= 0.0006
    bad += not ok
    out.append(("check_vs_100r_headline", c, 117, round(m, 4), h, round(d, 5), "PASS" if ok else "FAIL", "pp"))
# additivity: yield + gain = total, per year, real and nominal (arithmetic identity of the decomposition)
for sfx, tr in (("real", "capital_tr_real"), ("nominal", "capital_tr_nominal")):
    mx = max(abs(r[f"portfolio_y_{sfx}"] + r[f"portfolio_g_{sfx}"] - r[tr]) for r in rows)
    out.append(("check_additivity", f"max|y+g-tr| {sfx}", 117, f"{mx:.3e}", "", "", "PASS" if mx < 1e-7 else "FAIL", "decimal"))
    bad += not (mx < 1e-7)

# cross-check: JST housing rental return (nominal) vs ONS B2g / opening dwellings+land (S14), 1998-2019
ons = {}
for r in csv.DictReader(open(os.path.join(HERE, "derived_ons_flows.csv"))):
    if r["item"] == "B2g_over_open_dwellings_land":
        ons[int(r["year"])] = float(r["value"])
ys = [y for y in range(1998, 2020) if y in ons]
jst = {r["year"]: r["housing_y_nominal"] for r in rows}
mj = 100 * st.mean([jst[y] for y in ys])
mo = 100 * st.mean([ons[y] for y in ys])
out.append(("cross_check_housing_1998_2019", "jst_housing_y_nominal_mean", len(ys), round(mj, 4), "", "", "", "pct"))
out.append(("cross_check_housing_1998_2019", "ons_B2g_over_open_dwellings_land_mean", len(ys), round(mo, 4), "", "", "", "pct"))
out.append(("cross_check_housing_1998_2019", "difference_ons_minus_jst_pp", len(ys), round(mo - mj, 4), "", "", "",
            "pp; definitions differ: JST net rent/price (country-level housing stock), ONS gross operating surplus "
            "(incl. non-dwelling GOS, before CFC) / S14 dwellings+land. Reported, not spliced."))

with open(os.path.join(HERE, "jst_split_stats.csv"), "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["period_or_check", "item", "n", "mean_or_value", "sd_or_ref", "min_or_diff", "max_or_result", "unit_note"])
    w.writerows(out)
for o in out:
    if o[0].startswith(("check", "cross")) or (o[0] == "all_1896_2019" and o[1].startswith(("portfolio_", "capital_", "housing_y_real", "yield_share"))):
        print(o)
print("hard_fail", bad)
sys.exit(1 if bad else 0)
