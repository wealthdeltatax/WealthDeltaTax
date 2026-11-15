#!/usr/bin/env python3
"""
wid_checks.py - second, targeted diagnostic pass over wid_out/wid_long.csv.
Answers three questions the first summary could not:
  A. Where does the data-quality flag (dq, 0-5) change for each key series?  -> dq_runs.csv
  B. Does the private-wealth balance sheet add up (pwfin + pwnfa - pwdeb = pweal) and from
     which year?  A break marks where pweal stops being balance-sheet data.   -> identity_private.csv
  C. Same for national wealth (nweal vs nwnfa + nwnxa).                        -> identity_national.csv
Writes to wid_out/summary2/. Send me that folder (small).

  python wid_checks.py            # reads wid_out/wid_long.csv
"""
import argparse
import json
from pathlib import Path

import pandas as pd

ap = argparse.ArgumentParser()
ap.add_argument("--out", default="wid_out")
a = ap.parse_args()
out = Path(a.out)
sm = out / "summary2"
sm.mkdir(exist_ok=True)

df = pd.read_csv(out / "wid_long.csv", dtype={"age": str, "aux": str},
                 usecols=["series_key", "country", "year", "value", "aux", "series_type", "concept",
                          "percentile", "age", "pop"])
df = df[(df.series_type == "a") & (df.percentile == "p0p100") & (df.age == "999") & (df["pop"] == "i")]
df["dq"] = df.aux.map(lambda s: json.loads(s).get("dq") if isinstance(s, str) else None)

# --- A. dq run-length encoding per series x country
KEY = ["pweal", "hweal", "nweal", "nninc", "gdpro", "pwfin", "pwnfa", "pwdeb", "nwhou", "nwnfa", "nwnxa", "nwdwe"]
rows = []
for (c, k), g in df[df.concept.isin(KEY)].sort_values("year").groupby(["country", "concept"]):
    start, prev = None, "init"
    last_y = None
    for y, q in zip(g.year, g.dq):
        if q != prev:
            if start is not None:
                rows.append(dict(country=c, concept=k, dq=prev, from_year=start, to_year=last_y))
            start, prev = y, q
        last_y = y
    rows.append(dict(country=c, concept=k, dq=prev, from_year=start, to_year=last_y))
dqr = pd.DataFrame(rows)
dqr["n_years"] = dqr.to_year - dqr.from_year + 1
dqr.to_csv(sm / "dq_runs.csv", index=False)

# --- B/C. identities
piv = df.pivot_table(index=["country", "year"], columns="concept", values="value")


def identity(lhs, parts, signs, path, tag):
    need = [lhs] + parts
    if any(c not in piv for c in need):
        print(f"{tag}: missing {set(need) - set(piv.columns)}")
        return
    t = piv[need].dropna().copy()
    t["rhs"] = sum(s * t[p] for p, s in zip(parts, signs))
    t["rel_diff"] = t.rhs / t[lhs] - 1
    t = t.reset_index()
    t.to_csv(path.with_name(path.stem + "_full.csv"), index=False)
    s = (t.groupby("country")
           .agg(first=("year", "min"), last=("year", "max"), n=("year", "size"),
                median_abs=("rel_diff", lambda x: x.abs().median()),
                max_abs=("rel_diff", lambda x: x.abs().max()),
                n_gt_1pct=("rel_diff", lambda x: int((x.abs() > 0.01).sum())),
                first_year_gt_1pct=("year", lambda y: int(y[t.loc[y.index, "rel_diff"].abs() > 0.01].min())
                                    if (t.loc[y.index, "rel_diff"].abs() > 0.01).any() else None))
           .reset_index())
    s.to_csv(path, index=False)
    print(f"{tag}:\n", s.to_string(index=False), "\n")


identity("pweal", ["pwfin", "pwnfa", "pwdeb"], [1, 1, -1], sm / "identity_private.csv", "pweal = pwfin + pwnfa - pwdeb")
identity("nweal", ["nwnfa", "nwnxa"], [1, 1], sm / "identity_national.csv", "nweal = nwnfa + nwnxa")

# --- D. growth seam in W/NNI and in its components at 1979/80 (is it the splice?)
seam = []
for c, g in piv.reset_index().groupby("country"):
    g = g.set_index("year")
    for k in ("pweal", "nninc", "pwfin", "pwnfa", "pwdeb"):
        if k in g and {1978, 1979, 1980, 1981} <= set(g[k].dropna().index):
            s = g[k]
            seam.append(dict(country=c, concept=k, g_1978_79=s[1979] / s[1978] - 1,
                             g_1979_80=s[1980] / s[1979] - 1, g_1980_81=s[1981] / s[1980] - 1))
pd.DataFrame(seam).to_csv(sm / "seam_growth.csv", index=False)
print("written to", sm)
