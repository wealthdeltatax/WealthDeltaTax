#!/usr/bin/env python3
"""
wid_summarise.py - turns the big wid_out/wid_long.csv into ~7 small files in wid_out/summary/
that are enough for me (or a future agent) to understand what the data is, how good it is,
and how it plugs into the WDT audit. Send me the whole summary/ folder (a few hundred KB).

  python wid_summarise.py            # reads wid_out/wid_long.csv
  python wid_summarise.py --out wid_out
"""
import argparse
import json
from pathlib import Path

import pandas as pd

ap = argparse.ArgumentParser()
ap.add_argument("--out", default="wid_out")
a = ap.parse_args()
out = Path(a.out)
sm = out / "summary"
sm.mkdir(exist_ok=True)

df = pd.read_csv(out / "wid_long.csv", dtype={"age": str, "aux": str})
df["has_value"] = df.value.notna()
v = df[df.has_value]

# 1. inventory: one row per series definition (not per country/year)
inv = (v.groupby(["preset", "concept", "series_type", "percentile", "age", "pop"])
         .agg(n_countries=("country", "nunique"), n_rows=("year", "size"),
              first_year=("year", "min"), last_year=("year", "max"),
              share_extrapolated=("is_extrapolated", "mean"))
         .reset_index())
inv.to_csv(sm / "1_inventory.csv", index=False)

# 2. what is `aux`? value counts by extrapolation flag and by pre/post-1980
df["period"] = pd.cut(df.year, [0, 1949, 1979, 1999, 3000], labels=["<1950", "1950-79", "1980-99", "2000+"])
aux = (df.groupby(["aux", "is_extrapolated", "period"], observed=True, dropna=False)
         .size().rename("n").reset_index())
aux.to_csv(sm / "2_aux_profile.csv", index=False)

# 3. coverage + longest contiguous run per country for the D1 key series
def runs(years):
    ys = sorted(set(years))
    best, cur = 0, 0
    prev = None
    for y in ys:
        cur = cur + 1 if prev is not None and y == prev + 1 else 1
        best, prev = max(best, cur), y
    return best

key = v[v.concept.isin(["pweal", "nweal", "hweal", "gdpro", "nninc", "ninc", "ptinc", "diinc"])
        & (v.series_type.isin(["a", "m", "w", "y"])) & (v.percentile == "p0p100")]
cov = (key.groupby(["concept", "series_type", "age", "pop", "country"])
          .agg(first=("year", "min"), last=("year", "max"), n=("year", "size"),
               n_observed=("is_extrapolated", lambda s: int((~s).sum())),
               longest_run=("year", runs)).reset_index())
cov.to_csv(sm / "3_coverage_key_series.csv", index=False)

# 4. D1 gate on the actual ratio, all (age,pop) combos that have both numerator and denominator
rows = []
piv = (v[(v.series_type == "a") & (v.percentile == "p0p100")]
       .pivot_table(index=["country", "year", "age", "pop"], columns="concept", values="value"))
for num in ("pweal", "nweal", "hweal"):
    for den in ("nninc", "gdpro", "ninc"):
        if num in piv and den in piv:
            r = (piv[num] / piv[den]).dropna().rename("ratio").reset_index()
            for (c, age, pop), g in r.groupby(["country", "age", "pop"]):
                g = g.sort_values("year")
                rows.append(dict(numerator=num, denominator=den, country=c, age=age, pop=pop,
                                 first=g.year.min(), last=g.year.max(), n=len(g),
                                 longest_run=runs(g.year),
                                 pass_50=len(g) >= 50,
                                 ratio_1979=g.loc[g.year == 1979, "ratio"].mean(),
                                 ratio_1980=g.loc[g.year == 1980, "ratio"].mean(),
                                 ratio_2000=g.loc[g.year == 2000, "ratio"].mean(),
                                 ratio_last=g.ratio.iloc[-1]))
gate = pd.DataFrame(rows)
if len(gate):
    gate["seam_1979_80_pct"] = (gate.ratio_1980 / gate.ratio_1979 - 1) * 100
gate.to_csv(sm / "4_d1_gate_and_seam.csv", index=False)

# 5. composition completeness: concept x country, years available (aggregates, age 999/992)
comp = v[(v.preset == "composition") & (v.percentile == "p0p100")]
cc = (comp.groupby(["concept", "series_type", "age", "pop", "country"]).year.agg(["min", "max", "size"])
          .reset_index())
cc.to_csv(sm / "5_composition_coverage.csv", index=False)

# 6. units sanity: median / min / max of the level for one recent year, per series
y = v[v.year == v.year.max() - 1]
units = (y.groupby(["concept", "series_type", "age", "pop", "percentile"]).value
           .agg(["count", "median", "min", "max"]).reset_index())
units.to_csv(sm / "6_latest_year_ranges.csv", index=False)

# 7. a few raw rows for the format, plus country list and run facts
df.sort_values(["country", "series_key", "year"]).head(60).to_csv(sm / "7_sample_rows.csv", index=False)
facts = dict(rows=len(df), rows_with_value=int(df.has_value.sum()),
             countries=sorted(df.country.unique()), years=[int(df.year.min()), int(df.year.max())],
             presets=sorted(df.preset.unique()), vintage=sorted(df.vintage.unique()),
             n_series_keys=int(df.series_key.nunique()),
             aux_examples=sorted(df.aux.dropna().unique())[:15])
manifest = out / "manifest.json"
if manifest.exists():
    facts["manifest_args"] = json.loads(manifest.read_text()).get("args")
(sm / "0_facts.json").write_text(json.dumps(facts, indent=2, default=str))
print("written to", sm)
for p in sorted(sm.iterdir()):
    print(f"  {p.name:32s} {p.stat().st_size/1024:8.1f} KB")
