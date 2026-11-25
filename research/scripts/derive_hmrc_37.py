#!/usr/bin/env python3
"""101r block 2b: HMRC Personal Incomes Table 3.7 (2023-24) property, interest, dividend income by total-income range,
compared with ONS household-account aggregates. By TOTAL INCOME of UK taxpayers (SPI), not by wealth band.

Run: python -I research/scripts/derive_hmrc_37.py
Reads  data/uk-wealth-tables/097r/hmrc_csv/Collated_Tables_3_1_to_3_11_2324__Table_3_7.csv
       research/tables/101r-parameter-map-flows-and-returns/derived_ons_flows.csv
Writes research/tables/101r-parameter-map-flows-and-returns/hmrc_37_income_composition.csv and hmrc_37_coverage_vs_ons.csv
Coverage ratios are descriptive; tax-year 2023-24 is set against calendar 2023 and 2024 and not merged with either.
"""
import csv, os, sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..'))   # the repository root (this script is in research/scripts/)
HERE = os.path.join(ROOT, 'research', 'tables', '101r-parameter-map-flows-and-returns')   # the 101r tables (was the folder of this script)
rows = list(csv.reader(open(os.path.join(ROOT, "data", "uk-wealth-tables", "097r", "hmrc_csv", "Collated_Tables_3_1_to_3_11_2324__Table_3_7.csv"))))
hdr = rows[4]
body = [r for r in rows[5:] if r and r[0] and r[0] not in ("End of worksheet",)]
allr = [r for r in body if r[0] == "All ranges"][0]
rng = [r for r in body if r[0] != "All ranges"]
f = lambda s: float(s.replace(",", ""))
C = {"prop": 2, "int": 5, "div": 8, "oth": 11, "tot": 14}
bad = 0
out = []
# column sums vs All-ranges row (published to 3 sf, so allow 1.5 percent)
for k, i in C.items():
    s = sum(f(r[i]) for r in rng)
    a = f(allr[i])
    ok = abs(s - a) <= 0.015 * a
    bad += not ok
    out.append(("check_sum_vs_all", k, round(s, 1), a, "PASS" if ok else "FAIL"))
tot = f(allr[C["tot"]])
for r in rng:
    lo = int(r[0])
    out.append(("range", lo, *(round(f(r[C[k]]), 1) for k in C),
                round(f(r[C["div"]]) / f(r[C["tot"]]), 4), round(f(r[C["int"]]) / f(r[C["tot"]]), 4),
                round(f(r[C["prop"]]) / f(r[C["tot"]]), 4)))
# cumulative share of each income type received by taxpayers with total income >= thresholds
for thr in (50000, 100000, 150000, 500000):
    for k in ("prop", "int", "div", "tot"):
        s = sum(f(r[C[k]]) for r in rng if int(r[0]) >= thr)
        out.append(("share_at_or_above", thr, k, round(s / f(allr[C[k]]), 4)))
with open(os.path.join(HERE, "hmrc_37_income_composition.csv"), "w", newline="") as fh:
    w = csv.writer(fh)
    w.writerow(["kind", "key", "v1", "v2", "v3", "v4", "v5", "v6", "v7", "v8"])
    for o in out:
        w.writerow(o)

# coverage vs ONS (GBPm)
ons = {}
for r in csv.DictReader(open(os.path.join(HERE, "derived_ons_flows.csv"))):
    ons[(r["item"], int(r["year"]))] = float(r["value"])
cov = []
pairs = [("HMRC property net income", "prop", "no like-for-like ONS series (landlord rent sits in B.2g gross operating surplus with imputed owner-occupier rent)", None),
         ("HMRC bank and building society interest", "int", "D41_interest_GBPm", 1),
         ("HMRC dividends", "div", "D42_distributed_GBPm", 1)]
for lab, k, item, _ in pairs:
    h = f(allr[C[k]])
    for y in (2023, 2024):
        o = ons.get((item, y))
        cov.append((lab, "2023-24", y, h, o, round(h / o, 4) if o else "", "SPI taxpayers only, taxable income; ONS includes sheltered (ISA, pension) and non-taxpayer income" if o else "no like-for-like ONS series; see note"))
with open(os.path.join(HERE, "hmrc_37_coverage_vs_ons.csv"), "w", newline="") as fh:
    w = csv.writer(fh)
    w.writerow(["hmrc_item", "hmrc_year", "ons_year", "hmrc_gbpm", "ons_gbpm", "ratio", "note"])
    w.writerows(cov)
for o in out:
    if o[0] in ("check_sum_vs_all", "share_at_or_above") : print(o)
for c in cov: print(c[:6])
print("hard_fail", bad)
sys.exit(1 if bad else 0)
