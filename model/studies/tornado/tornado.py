"""Brief 027r: tier 1 tornado on the revenue identity. Run: python3 -I model/studies/tornado/tornado.py
Reads model-specs/inputs.md (rows by id). Writes tornado_results.csv and tornado_tables.md next to this file.
Identity (drivers.md section 1): M1a = eps * g * omega (refunds netted in g, see tornado.md section 6)."""
import csv, os, re
HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, '..', '..', '..', 'results', 'tornado')   # outputs stay here until 163c
REG = os.path.join(HERE, "..", "..", "..", "model-specs", "inputs.md")
rows = {}
for l in open(REG, encoding="utf-8"):
    if l.startswith("| I-"):
        c = [x.strip() for x in l.strip().strip("|").split("|")]
        rows[c[0]] = c
def num(s):
    m = re.match(r"^-?[\d,]*\.?\d+", s.replace("−", "-"))
    return float(m.group(0).replace(",", "")) if m else None
def lch(i):
    c = rows[i]; return [num(c[3]), num(c[4]), num(c[5])]
def label(i): return rows[i][1]
# ---- assumptions (not register rows) ----
A = dict(
    v2_wdt=7.34,          # synthesis.md section 10, logistic_ln_ref, % of GDP
    m1c=-0.6,             # synthesis.md section 10 point 6, v2 only
    dwell_land_gdp=6.6/3.0,   # I-D10b row text: 6.6tn dwellings plus land over about 3.0tn GDP
    w_d5c=1.0,            # D5c: leavers applied to the whole payer base (upper bound)
    w_d5d=0.10*0.439,     # D5d: business assets about 10% of D10 wealth (I-D5d) x D10 share of payer wealth 40.7/92.7
    bottom5_adults=0.5,   # non-payers proxied by the bottom five income deciles
)
C = {k: lch(k)[1] for k in rows}
def central():
    return dict(g=C["I-D1a"]/100, w0=C["I-D4a"], s=C["I-D4c"]/100, e=C["I-D4e"]/100, r5=C["I-D5a"]/100,
                d10=C["I-D10b"]/100, levy=C["I-D7a"], cor=C["I-D7b"], ct=C["I-T3n"], br=C["I-T3m"],
                cgt=C["I-T3h"], iht=C["I-T3i"], sdlt=C["I-T3k"], sds=C["I-T3l"], m1c=A["m1c"],
                d5b=C["I-D5b"]/100, d5d=C["I-D5d"]/100, eps=None)
def omega(p):
    base = p["w0"]*(p["s"]+p["e"]) + p["d10"]*A["dwell_land_gdp"]*p["s"]
    return base*(1-p["r5"])
P0 = central()
P0["eps"] = A["v2_wdt"]/100/(P0["g"]*omega(P0))   # implied wealth-weighted rate, assumption A1
def m1(p):
    m1a = p["eps"]*p["g"]*omega(p)*100
    m1d = p["cor"]+p["ct"]+p["br"]+p["cgt"]+p["iht"]+p["sdlt"]+p["sds"]
    return m1a + p["levy"] + p["m1c"] - m1d
def m2p(p):  # mean burden proxy, % of payer wealth: eps * g * (1 - avoided share)
    return p["eps"]*p["g"]*(1-p["d5b"]-p["d5d"]*A["w_d5d"])*100
M4_SHARE = dict(cor="I-D6j", ct="I-D6h", br="I-D6i", cgt="I-D6k", iht="I-D6l", sdlt="I-D6m", sds="I-D6n")
Q = [C["I-H1"+k] for k in "abcde"]
def m4a(p, sh=None):
    sh = sh or {k: C[v]/100 for k, v in M4_SHARE.items()}
    save = sum(p[k]*sh[k] for k in M4_SHARE)
    bottom_half_share = (Q[0]+Q[1]+0.5*Q[2])/sum(Q)
    den = bottom_half_share*(31.61+P0["ct"]+P0["br"])
    return 100*save/den
# ---- mapping: row id -> (output, function(value)->params) ----
def setp(**kw):
    def f(v):
        p = dict(P0); p.update({k: (fn(v) if callable(fn) else fn) for k, fn in kw.items()}); return p
    return f
M1MAP = {
 "I-D1a": setp(g=lambda v: v/100),
 "I-D4a": setp(w0=lambda v: v),
 "I-D4c": setp(s=lambda v: v/100),
 "I-D4e": setp(e=lambda v: v/100),
 "I-D5a": setp(r5=lambda v: v/100),
 "I-D5b": setp(r5=lambda v: P0["r5"]+(v/100-P0["d5b"])),
 "I-D5c": setp(r5=lambda v: P0["r5"]+(v/100-C["I-D5c"]/100)*A["w_d5c"]),
 "I-D5d": setp(r5=lambda v: P0["r5"]+(v/100-P0["d5d"])*A["w_d5d"]),
 "I-D10a": setp(d10=lambda v: P0["d10"]*v/C["I-D10a"]),
 "I-D10b": setp(d10=lambda v: v/100),
 "I-D7a": setp(levy=lambda v: v),
 "I-D7c": setp(levy=lambda v: v*P0["cor"]),
 "I-D7d": setp(cor=lambda v: P0["cor"]*v/C["I-D7d"]),
 "I-T3f": setp(cor=lambda v: v),
 "I-T3n": setp(ct=lambda v: v), "I-T3m": setp(br=lambda v: v), "I-T3h": setp(cgt=lambda v: v),
 "I-T3i": setp(iht=lambda v: v), "I-T3k": setp(sdlt=lambda v: v), "I-T3l": setp(sds=lambda v: v),
}
NOT_M1 = {
 "I-D1b": "Spread of annual returns. In the identity refunds are netted in g, so sigma acts only through the refund cap and the fill years (not reachable). Direction: a higher sigma raises the arithmetic mean over the geometric g (+0.34 points of return at the central 8.2%, my arithmetic) and the loss-year share.",
 "I-D1c": "Loss-year share. Acts through refunds, the cap on them and the reserve fill (P1, P4). Not reachable on the identity. Direction: more loss years, larger refunds, longer fill.",
 "I-D1d": "Longest loss run. Acts on the reserve fill and on P3 only. Not reachable. Direction: a longer run lengthens the transition.",
 "I-D1e": "Gap between the end of the return history and the last full year. A data-vintage input; no term in the identity.",
 "I-D4b": "Share of adults at or above W_min. Sets the number of payers and M2b; omega depends on the wealth share I-D4c, not on the head count.",
 "I-D4d": "Top 1% share: a check on the tail (I-D4e), no separate term.",
 "I-D4f": "Rich List total (one value): cross-check on I-D4e, no range.",
 "I-D4g": "National balance sheet ratio (one value): cross-check on I-D4a, no range.",
 "I-D7b": "Single value; its range is in I-T3f (below).",
 "I-D10c": "Share of a stamp duty cut that reaches house prices. Needs the transaction turnover, which the register does not hold. Not reachable. Direction: a higher share raises omega.",
 "I-D8a": "Reserve multiple. Acts on fill years and the transition only; steady-state M1 is unchanged.",
 "I-D8b": "Long reserve fill time (P1): transition only.", "I-D8c": "Short reserve fill time (P1): transition only.",
 "I-D11a": "Discount rate: M3 only.", "I-D11b": "M3 only; unused at G = 30.", "I-D11c": "M3 only; unused at G = 30.",
 "I-D11d": "M3 only; no value.",
}
for k in "abcdefgh": NOT_M1["I-D9"+k] = "Income and liquid assets by wealth band: enter M2b, M2c and M4b, not M1."
for k in "abcdefghijklmnopq":
    NOT_M1["I-D6"+k] = "Incidence by income decile: allocates the retired taxes among households (M4a), not the receipts (M1d)."
out = []
def rec(i, tier, out_name, lo, ce, hi, note=""):
    out.append(dict(id=i, tier=tier, output=out_name, low_in=lch(i)[0] if i in rows else "", cen_in=lch(i)[1] if i in rows else "",
                    high_in=lch(i)[2] if i in rows else "", low_res=lo, central=ce, high_res=hi,
                    swing=(abs(hi-lo) if lo is not None else None), note=note))
TIER = lambda i: 2 if i.startswith(("I-D7","I-D8","I-D11")) else (1 if i[:4] in ("I-D4","I-D5","I-D6","I-D9","I-D1","I-D10") and not i.startswith("I-D11") and not i.startswith("I-D10x") else 0)
def tier(i):
    if i.startswith(("I-D7","I-D8","I-D11")): return "2"
    if i.startswith("I-T3"): return "M1d line"
    return "1"
M1c = m1(P0)
for i, f in M1MAP.items():
    lo_, ce_, hi_ = lch(i)
    rec(i, tier(i), "M1", m1(f(lo_)), M1c, m1(f(hi_)))
for i, why in NOT_M1.items():
    rec(i, tier(i), "M1", None, M1c, None, why)
# M2 proxy
M2c = m2p(P0)
M2MAP = {"I-D1a": setp(g=lambda v: v/100), "I-D5b": setp(d5b=lambda v: v/100), "I-D5d": setp(d5d=lambda v: v/100)}
for i, f in M2MAP.items():
    lo_, ce_, hi_ = lch(i); rec(i, tier(i), "M2 (mean burden proxy)", m2p(f(lo_)), M2c, m2p(f(hi_)))
# M4a
M4c = m4a(P0)
for k, rid in M4_SHARE.items():
    lo_, ce_, hi_ = lch(rid)
    def f(v, k=k): return {**{kk: C[vv]/100 for kk, vv in M4_SHARE.items()}, k: v/100}
    rec(rid, "1", "M4a", m4a(P0, f(lo_)), M4c, m4a(P0, f(hi_)))
lo_, ce_, hi_ = lch("I-D6p")
sh = lambda v: {**{kk: C[vv]/100 for kk, vv in M4_SHARE.items()}, "br": v/100}
rec("I-D6p", "1", "M4a", m4a(P0, sh(lo_)), M4c, m4a(P0, sh(hi_)), "ONS allocation of business rates, replaces I-D6i")
for k, rid in dict(cor="I-T3f", ct="I-T3n", br="I-T3m", cgt="I-T3h", iht="I-T3i", sdlt="I-T3k", sds="I-T3l").items():
    lo_, ce_, hi_ = lch(rid)
    rec(rid, "M1d line", "M4a", m4a({**P0, k: lo_}), M4c, m4a({**P0, k: hi_}))
with open(os.path.join(DATA, "tornado_results.csv"), "w", newline="") as fh:
    w = csv.DictWriter(fh, fieldnames=list(out[0])); w.writeheader(); w.writerows(out)
# ---- back-out ----
w_c = omega(P0)
backout = dict(
  omega0=C["I-D4a"]*C["I-D4c"]/100, omega_tail=C["I-D4a"]*(C["I-D4c"]+C["I-D4e"])/100,
  omega_cap=P0["d10"]*A["dwell_land_gdp"]*P0["s"], omega_eff=w_c, gain_base=P0["g"]*w_c*100, eps=P0["eps"],
  guess20=0.20*P0["g"]*w_c*100)
v2like_w = 6.81*0.93; v2like_g = 0.0474
backout["eps_v2like"] = A["v2_wdt"]/100/(v2like_g*v2like_w)
backout["gain_base_v2like"] = v2like_g*v2like_w*100
for k, v in backout.items(): print(k, round(v, 4))
print("M1 central", round(M1c, 3), "M2 proxy", round(M2c, 3), "M4a", round(M4c, 2))
for r in sorted([r for r in out if r["swing"] is not None and r["output"] == "M1"], key=lambda r: -r["swing"])[:12]:
    print(r["id"], round(r["low_res"], 2), round(r["central"], 2), round(r["high_res"], 2), round(r["swing"], 2))
import json; json.dump(dict(backout=backout, P0={k: v for k, v in P0.items()}, A=A, M1c=M1c, M2c=M2c, M4c=M4c), open(os.path.join(DATA, "tornado_central.json"), "w"), indent=1)

# ---- markdown tables ----
def fmt(x, d=2): return "" if x is None else f"{x:,.{d}f}"
def table(output, ids=None, extra=None):
    rs = [r for r in out if r["output"] == output]
    rs.sort(key=lambda r: (-(r["swing"] or 0), r["id"]))
    lines = ["| Rank | Input | Row id | Tier | Input low / central / high | Result at low | Central | Result at high | Swing | Note |", "|---|---|---|---|---|---|---|---|---|---|"]
    k = 0
    for r in rs:
        if r["swing"] is None:
            rank = "-"; res = ("n/r", fmt(r["central"]), "n/r", "0")
        else:
            k += 1; rank = str(k); res = (fmt(r["low_res"]), fmt(r["central"]), fmt(r["high_res"]), fmt(r["swing"]))
        lab = label(r["id"]).split(" (")[0][:70]
        lines.append(f"| {rank} | {lab} | {r['id']} | {r['tier']} | {r['low_in']} / {r['cen_in']} / {r['high_in']} | {res[0]} | {res[1]} | {res[2]} | {res[3]} | {r['note'] if r['swing'] is None else ''} |")
    return "\n".join(lines)
with open(os.path.join(DATA, "tornado_tables.md"), "w") as fh:
    for o in ("M1", "M2 (mean burden proxy)", "M4a"):
        fh.write(f"## {o}\n\n" + table(o) + "\n\n")
