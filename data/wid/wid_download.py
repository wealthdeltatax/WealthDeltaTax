#!/usr/bin/env python3
"""
wid_download.py - automated WID.world downloader for the WDT data audit.

Python port of the request logic in the official R package `wid`
(world-inequality-database/wid-r-tool: R/get-requests.R, R/download-wid.R).
Dependencies: `requests` and `pandas` only.

!! NOT TESTED AGAINST THE LIVE API !!  It was written in a sandbox that cannot
reach wid.world. Parsing is unit-tested against synthetic responses built from
the R source. Run `discover` first; if anything fails, read the saved raw
response in OUT/raw/ and the script tells you which step broke.

Usage
-----
  python wid_download.py discover              # 1. what exists? -> catalogue CSV
  python wid_download.py fetch                 # 2. download selected presets
  python wid_download.py fetch --presets wealth_levels composition
  python wid_download.py fetch --countries GB US --no-extrapolations
  python wid_download.py list-presets

Outputs (default ./wid_out/)
  catalogue.csv           every (country, variable, percentile, age, pop) WID offers
  raw/*.json              untouched API responses (provenance)
  wid_long.csv            tidy: series, country, year, value, unit, source, vintage,
                          is_extrapolated, + parsed code parts
  wid_wide_<preset>.csv   year x country convenience pivots (aggregate presets)
  manifest.json           timestamp, arguments, row counts, sha256 of each output

API key: the official package ships a public client key (inside R/sysdata.rda).
This script embeds that same key as the default. Override with env WID_API_KEY
(the raw value that is base64-encoded, or set WID_API_KEY_B64 for the already
encoded header value).
"""
from __future__ import annotations

import argparse
import base64
import datetime as dt
import hashlib
import json
import os
import re
import sys
import time
from pathlib import Path

import pandas as pd
import requests

BASE_URL = "https://rfap9nitz6.execute-api.eu-west-1.amazonaws.com/prod/"
# Header value exactly as the R package sends it: base64encode(api_key bytes).
DEFAULT_KEY_B64 = "rYFByOB0ioaPATwHtllMI71zLOZSK0Ic5veQonJP"

# WID uses ISO-2. 14 JST/WID-usable countries (per audit) + BE/PT as availability probes.
COUNTRIES = ["AU", "CH", "DE", "DK", "ES", "FI", "FR", "GB", "IT", "JP", "NL", "NO", "SE", "US"]
PROBE_COUNTRIES = ["BE", "PT"]

# ---------------------------------------------------------------------------
# What to download. Each preset = regex on the 5-letter concept, allowed series
# letters, and allowed (percentile, age, pop) combos. Variable codes in the API
# are  <series letter><concept>_<percentile>_<age>_<pop>  e.g. apweal_p0p100_992_i.
# Discovery decides what actually exists; presets only filter the catalogue, so a
# wrong guess about a code simply yields nothing (reported), never a bad request.
# ---------------------------------------------------------------------------
AGG = {"percentiles": ["p0p100"]}
PRESETS = {
    # D1: wealth-to-income/GDP levels and the denominators
    "wealth_levels": dict(
        series="amwy", concepts=["pweal", "nweal", "hweal", "agdpro", "anninc", "ndpro", "gdpro", "nninc", "ninc"],
        concepts_regex=r"^(pweal|nweal|hweal|gdpro|nninc|anninc|agdpro|ndpro)$",
        percentiles=["p0p100"], ages=["999", "992"], pops=["i", "j", "t"]),
    "ratios": dict(  # WID's own wealth/income and wealth/GDP ratios, for cross-checking W_NNI
        series="wy", concepts_regex=r"^(pweal|nweal|hweal)$",
        percentiles=["p0p100"], ages=["999", "992"], pops=["i", "j", "t"]),
    # D1/D2/D4: split of national / private wealth by asset and liability type
    "composition": dict(
        series="amwy",
        concepts_regex=r"^(pweal|pwnfa|pwfin|pwdeb|nweal|nwnfa|nwhou|nwdwe|nwlan|nwbus|nwagr|nwodk|"
                       r"nwnxa|nwgxa|nwgxd|nwboo|cwres|nwdka|nwfin|nwdeb|nwpen|nwequ|nwbon|nwdep|nwcas|nwins)$",
        percentiles=["p0p100"], ages=["999", "992"], pops=["i", "j", "t"]),
    # D8: wealth distribution (top shares, group averages, thresholds, Gini)
    "wealth_distribution": dict(
        series="astgb", concepts_regex=r"^(hweal|pweal)$",
        percentiles=["p0p50", "p50p90", "p90p100", "p99p100", "p99.9p100", "p90p99", "p0p90", "p0p100"],
        ages=["992"], pops=["j", "i", "t"]),
    # D2/saving rates, inequality context: income distribution
    "income_distribution": dict(
        series="astgb", concepts_regex=r"^(ptinc|diinc|pllin|pkkin|fiinc)$",
        percentiles=["p0p50", "p50p90", "p90p100", "p99p100", "p99.9p100", "p90p99", "p0p100"],
        ages=["992"], pops=["j", "i", "t"]),
    "income_levels": dict(
        series="am", concepts_regex=r"^(ptinc|diinc|pllin|pkkin|fiinc|gdpro|anninc|nninc)$",
        percentiles=["p0p100"], ages=["992", "999"], pops=["j", "i", "t"]),
    # D9: population / adults per head
    "population": dict(
        series="n", concepts_regex=r"^(popul)$",
        percentiles=["p0p100"], ages=["999", "992", "996", "014", "156", "991", "997"], pops=["i", "j"]),
    # unit conversion / price deflators (needed to put everything on one basis)
    "deflators": dict(
        series="ix", concepts_regex=r"^(yixx|lcusp|lceup|lcusx|lceux|lcyup|lcyux)$",
        percentiles=["p0p100"], ages=["999"], pops=["i"]),
}
DEFAULT_PRESETS = ["wealth_levels", "ratios", "composition", "wealth_distribution",
                   "income_distribution", "income_levels", "population", "deflators"]

VAR_RE = re.compile(r"^(?P<series>[a-z])(?P<concept>[a-z]{5})$")


# ------------------------------------------------------------------ HTTP layer
class WID:
    def __init__(self, out: Path, pause: float = 0.3, retries: int = 4):
        self.out = out
        (out / "raw").mkdir(parents=True, exist_ok=True)
        self.sess = requests.Session()
        key_b64 = os.environ.get("WID_API_KEY_B64")
        if not key_b64:
            raw = os.environ.get("WID_API_KEY")
            key_b64 = base64.b64encode(raw.encode()).decode() if raw else DEFAULT_KEY_B64
        self.sess.headers["x-api-key"] = key_b64
        self.pause, self.retries = pause, retries
        self.n_raw = 0

    def _get(self, url: str, tag: str):
        last = None
        for i in range(self.retries):
            try:
                r = self.sess.get(url, timeout=120)
                if r.status_code == 200:
                    txt = r.text
                    self.n_raw += 1
                    (self.out / "raw" / f"{self.n_raw:04d}_{tag}.json").write_text(txt, encoding="utf-8")
                    time.sleep(self.pause)
                    return json.loads(txt)
                last = f"HTTP {r.status_code}: {r.text[:200]}"
                if r.status_code in (400, 401, 403, 404):
                    break  # not retryable
            except (requests.RequestException, ValueError) as e:
                last = repr(e)
            time.sleep(2 ** i)
        raise RuntimeError(f"request failed ({tag}): {last}\nURL: {url}")

    def available(self, countries, sixlet="all"):
        """countries-available-variables -> DataFrame(variable, country, percentile, age, pop)"""
        url = f"{BASE_URL}countries-available-variables?countries={','.join(countries)}&variables={sixlet}"
        js = self._get(url, f"avail_{sixlet}_{'-'.join(countries)[:30]}")
        if isinstance(js, list) and len(js) == 1:  # R: if length 1, take [[1]]
            js = js[0]
        rows = []
        if isinstance(js, dict):
            for variable, by_country in js.items():
                if not isinstance(by_country, dict):
                    continue
                for country, combos in by_country.items():
                    for c in combos:
                        rows.append((variable, country, c[0], str(c[1]), c[2]))
        return pd.DataFrame(rows, columns=["variable", "country", "percentile", "age", "pop"])

    def data(self, countries, codes):
        """countries-variables -> list of dict rows (indicator, country, year, value, extrap_years set)"""
        url = (f"{BASE_URL}countries-variables?countries={','.join(countries)}"
               f"&variables={','.join(codes)}&years=all")
        js = self._get(url, f"data_{codes[0]}_{len(codes)}")
        if isinstance(js, dict) and js.get("status"):
            if js["status"] == "payload_too_large":  # alternative route, as in the R package
                dl = js.get("download_url")
                if not dl:
                    raise RuntimeError("large payload without download_url")
                r = self.sess.get(dl, timeout=300)  # presigned URL: R sends no key here
                r.raise_for_status()
                (self.out / "raw" / f"{self.n_raw + 1:04d}_large.json").write_text(r.text, encoding="utf-8")
                self.n_raw += 1
                js = r.json()
            else:
                raise RuntimeError(js.get("message") or "server response invalid")
        return parse_data(js)


# ------------------------------------------------------------------ parsing
def _json_maybe(s):
    if s is None or s == "" or (isinstance(s, float) and pd.isna(s)):
        return None
    if isinstance(s, str):
        try:
            return json.loads(s)
        except ValueError:
            return None
    return s


def parse_data(js):
    """Port of the R loop. Marks extrapolated/interpolated years from meta, rather than dropping them."""
    if isinstance(js, list) and len(js) == 1:  # R: unnamed length-1 -> [[1]]
        js = js[0]
    out = []
    if not isinstance(js, dict):
        raise RuntimeError("server response invalid (not an object)")
    for variable, entries in js.items():
        for entry in entries:  # each entry: {country: {values: [[y, v]...], meta: {...}}}
            for country, body in entry.items():
                meta = body.get("meta") or {}
                brackets = _json_maybe(meta.get("extrapolation"))
                points = _json_maybe(meta.get("data_points"))
                points = {str(p[0]) if isinstance(p, list) else str(p) for p in (points or [])}
                extrap = set()
                for b in brackets or []:
                    lo, hi = int(b[0]), int(b[1])
                    extrap.update(str(y) for y in range(lo + 1, hi + 1))
                extrap -= points
                for rec in body.get("values", []):
                    # R uses only [0]=year, [1]=value; the API now sends a 3rd element (meaning
                    # undocumented) - kept raw as `aux` so nothing is lost.
                    if isinstance(rec, dict):  # newer API format: dict per point
                        lk = {str(k).lower(): k for k in rec}
                        yk = next((lk[k] for k in ("y", "year", "yr") if k in lk), None)
                        vk = next((lk[k] for k in ("v", "value", "val") if k in lk), None)
                        if yk is None or vk is None:
                            raise RuntimeError(
                                f"unrecognised data-point format, keys={list(rec)} sample={rec!r}. "
                                "Send me this line.")
                        y, v = rec[yk], rec[vk]
                        aux = {k: x for k, x in rec.items() if k not in (yk, vk)} or None
                        aux = json.dumps(aux) if aux else None
                    else:
                        y, v = rec[0], rec[1]
                        aux = rec[2] if len(rec) > 2 else None
                    out.append(dict(indicator=variable, country=country, year=int(y), value=v,
                                    aux=aux, is_extrapolated=str(y) in extrap))
    return out


# ------------------------------------------------------------------ selection
def select(cat: pd.DataFrame, preset: dict) -> pd.DataFrame:
    m = cat.variable.str.extract(VAR_RE)
    ok = cat.variable.str.match(VAR_RE)
    c = cat[ok].copy()
    c["series"], c["concept"] = m.loc[ok, "series"], m.loc[ok, "concept"]
    keep = (c.concept.str.match(preset["concepts_regex"])
            & c.series.isin(list(preset["series"]))
            & c.percentile.isin(preset["percentiles"])
            & c.age.isin(preset["ages"])
            & c["pop"].isin(preset["pops"]))
    return c[keep]


def chunked(xs, n):
    for i in range(0, len(xs), n):
        yield xs[i:i + n]


# ------------------------------------------------------------------ commands
def cmd_discover(a, w: WID):
    countries = a.countries + (PROBE_COUNTRIES if a.probe else [])
    frames = [w.available([c]) for c in countries]  # one country per call keeps responses small
    cat = pd.concat(frames, ignore_index=True)
    cat.to_csv(w.out / "catalogue.csv", index=False)
    print(f"catalogue.csv: {len(cat)} rows, {cat.variable.nunique()} variables, {cat.country.nunique()} countries")
    # preview what each preset would pick up
    for name, p in PRESETS.items():
        s = select(cat, p)
        per = s.groupby("country").variable.nunique().to_dict()
        print(f"  {name:20s} {len(s):5d} series-keys | countries: {len(per)} | concepts: "
              f"{', '.join(sorted(s.concept.unique())[:12])}")
    # the stems nobody asked for but which exist: lets you spot useful ones
    stems = (cat.variable.str[1:].value_counts().head(400))
    stems.to_csv(w.out / "catalogue_concepts.csv", header=["n_rows"])
    print("catalogue_concepts.csv: all 5-letter concepts present (grep it for ideas)")


def cmd_fetch(a, w: WID):
    cat_path = w.out / "catalogue.csv"
    if cat_path.exists() and not a.refresh_catalogue:
        cat = pd.read_csv(cat_path, dtype={"age": str})
        cat = cat[cat.country.isin(a.countries + (PROBE_COUNTRIES if a.probe else []))]
    else:
        cat = pd.concat([w.available([c]) for c in a.countries + (PROBE_COUNTRIES if a.probe else [])],
                        ignore_index=True)
        cat.to_csv(cat_path, index=False)

    frames, report = [], []
    for name in a.presets:
        sel = select(cat, PRESETS[name])
        if sel.empty:
            report.append((name, 0, 0))
            print(f"[{name}] nothing matched in catalogue")
            continue
        sel = sel.assign(code=sel.variable + "_" + sel.percentile + "_" + sel.age + "_" + sel["pop"])
        rows = []
        # chunk by code (as the R package does) across the countries that have it
        for codes in chunked(sorted(sel.code.unique()), a.chunk):
            ctry = sorted(sel[sel.code.isin(codes)].country.unique())
            rows += w.data(ctry, codes)
        df = pd.DataFrame(rows)
        if df.empty:
            report.append((name, len(sel), 0))
            continue
        df["preset"] = name
        frames.append(df)
        report.append((name, len(sel), len(df)))
        print(f"[{name}] {sel.code.nunique()} codes -> {len(df)} rows")

    if not frames:
        sys.exit("no data downloaded")
    long = pd.concat(frames, ignore_index=True)
    long = long.drop_duplicates(["country", "indicator", "year"])
    parts = long.indicator.str.split("_", expand=True)
    long["series"] = parts[0]
    long["percentile"], long["age"], long["pop"] = parts[1], parts[2], parts[3]
    long["concept"] = long.series.str[1:]
    long["series_type"] = long.series.str[0]
    vintage = dt.date.today().isoformat()
    long["unit"] = long.series_type.map({"a": "LCU const (ref yr) per capita", "m": "LCU const (ref yr) total",
                                           "w": "ratio to national income", "y": "ratio to GDP",
                                           "s": "share (0-1)", "t": "LCU const threshold", "g": "gini (0-1)",
                                           "n": "persons", "i": "index", "x": "exchange rate"}).fillna("see WID dictionary")
    long["source"] = "WID.world"
    long["vintage"] = vintage
    if a.no_extrapolations:
        long = long[~long.is_extrapolated]
    long["series_key"] = long.indicator
    cols = ["series_key", "country", "year", "value", "unit", "source", "vintage", "is_extrapolated", "aux",
            "series", "series_type", "concept", "percentile", "age", "pop", "preset"]
    long = long[cols].sort_values(["country", "series_key", "year"])
    long.to_csv(w.out / "wid_long.csv", index=False)

    # convenience wide pivots for aggregate presets: one column per country
    for name in ("wealth_levels", "ratios", "composition", "population"):
        sub = long[(long.preset == name)]
        if sub.empty:
            continue
        sub.pivot_table(index=["series_key", "year"], columns="country", values="value").reset_index() \
           .to_csv(w.out / f"wid_wide_{name}.csv", index=False)

    # coverage per series x country, so the audit gate is one groupby away
    cov = (long.dropna(subset=["value"]).groupby(["series_key", "country"]).year
           .agg(first="min", last="max", n="count").reset_index())
    cov.to_csv(w.out / "wid_coverage.csv", index=False)

    manifest = dict(created=dt.datetime.now(dt.timezone.utc).isoformat(), vintage=vintage,
                    args=vars(a), api=BASE_URL, preset_report=report,
                    n_rows=len(long),
                    files={p.name: hashlib.sha256(p.read_bytes()).hexdigest()
                           for p in sorted(w.out.glob("*.csv"))})
    (w.out / "manifest.json").write_text(json.dumps(manifest, indent=2, default=str))
    print(f"\nwid_long.csv: {len(long)} rows | manifest.json written | {w.out}")


def cmd_list(a, w):
    for k, v in PRESETS.items():
        print(f"{k:22s} series={v['series']:6s} ages={v['ages']} pops={v['pops']}\n"
              f"{'':22s} concepts~ {v['concepts_regex']}")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("command", choices=["discover", "fetch", "list-presets"])
    ap.add_argument("--out", default="wid_out")
    ap.add_argument("--countries", nargs="+", default=COUNTRIES)
    ap.add_argument("--probe", action="store_true", help="also query BE and PT (availability test)")
    ap.add_argument("--presets", nargs="+", default=DEFAULT_PRESETS, choices=list(PRESETS))
    ap.add_argument("--chunk", type=int, default=10, help="variables per data request")
    ap.add_argument("--no-extrapolations", action="store_true",
                    help="drop interpolated/extrapolated years (default: keep, flagged in is_extrapolated)")
    ap.add_argument("--refresh-catalogue", action="store_true")
    a = ap.parse_args()
    out = Path(a.out)
    out.mkdir(parents=True, exist_ok=True)
    w = WID(out)
    {"discover": cmd_discover, "fetch": cmd_fetch, "list-presets": cmd_list}[a.command](a, w)


if __name__ == "__main__":
    main()