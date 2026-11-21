#!/usr/bin/env python3
"""101r block 1: household-account flows from held ONS series (097r).

Run: python -I docs/research/data/101r/derive_ons_flows.py
Reads  docs/research/data/097r/{ons_ukea_household_annual,ons_nbs_household_stocks_annual,
       ons_nbs_financial_annual,qsa_household_annual_2026q2}.csv
Writes docs/research/data/101r/derived_ons_flows.csv  (long: year,item,value,unit,formula,inputs)
       docs/research/data/101r/derived_ons_checks.csv (identity/tolerance checks)
Arithmetic only. No parameter is chosen here. Exits 1 if a hard check fails.
"""
import csv, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "..", "097r")


def load(name, ids_by_file=None):
    d = {}
    with open(os.path.join(SRC, name), newline="") as f:
        for r in csv.DictReader(f):
            try:
                v = float(r["value"])
            except ValueError:
                continue
            k = (r["series_id"], int(r["period"]))
            if k in d and abs(d[k] - v) > 1e-9:
                raise SystemExit(f"conflicting duplicate {name} {k}: {d[k]} vs {v}")
            d[k] = v
    return d


UK = load("ons_ukea_household_annual.csv")
NB = load("ons_nbs_household_stocks_annual.csv")
FI = load("ons_nbs_financial_annual.csv")
QS = load("qsa_household_annual_2026q2.csv")

out, chk = [], []


def put(y, item, val, unit, formula, inputs):
    if val is None:
        return
    out.append((y, item, round(val, 6), unit, formula, inputs))


def g(d, sid, y):
    return d.get((sid, y))


def check(cid, y, comp, pub, tol, hard=True, note=""):
    if comp is None or pub is None:
        return
    diff = comp - pub
    chk.append((cid, y, round(comp, 6), round(pub, 6), round(diff, 6), tol,
                "PASS" if abs(diff) <= tol else ("FAIL" if hard else "INFO"),
                "hard" if hard else "info", note))


def div(a, b):
    return None if a is None or b in (None, 0) else a / b


def add(*xs):
    return None if any(x is None for x in xs) else sum(xs)


YEARS = range(1998, 2026)
for y in YEARS:
    B6, D8, P31, B8, B5 = (g(UK, s, y) for s in ("HABN", "HAZA", "ABPB", "HADA", "HABL"))
    # ---- 1. saving identity and ratio -------------------------------------
    put(y, "B6g_gdhi", B6, "GBPm", "HABN", "HABN")
    put(y, "D8_pension_adj", D8, "GBPm", "HAZA", "HAZA")
    put(y, "P31_consumption", P31, "GBPm", "ABPB", "ABPB")
    put(y, "B8g_saving", B8, "GBPm", "HADA", "HADA")
    if None not in (B6, D8, P31, B8):
        check("ID1 B6g+D8-P31=B8g", y, B6 + D8 - P31, B8, 2.0, note="GBPm, rounding")
        ratio = 100 * B8 / (B6 + D8)
        put(y, "saving_ratio_pct", ratio, "pct", "100*B8g/(B6g+D8)", "HADA,HABN,HAZA")
        check("ID2 saving ratio vs DG5H", y, ratio, g(UK, "DG5H", y), 0.06, note="published to 1dp")
        # pension share of the ratio (D8 over resources) vs non-pension remainder
        put(y, "ratio_pension_part_pct", 100 * D8 / (B6 + D8), "pct", "100*D8/(B6g+D8)", "HAZA,HABN")
        put(y, "ratio_nonpension_part_pct", ratio - 100 * D8 / (B6 + D8), "pct",
            "ratio - pension part (identity P31=B6g+D8-B8g)", "HADA,HABN,HAZA")
        put(y, "consumption_share_of_B6g", P31 / B6, "ratio", "P31/B6g", "ABPB,HABN")
        put(y, "saving_share_of_B6g", B8 / B6, "ratio", "B8g/B6g", "HADA,HABN")
        put(y, "D8_share_of_B6g", D8 / B6, "ratio", "D8/B6g", "HAZA,HABN")
        put(y, "nonpension_saving_GBPm", B8 - D8, "GBPm", "B8g-D8", "HADA,HAZA")
    # QSA split vs published
    js8, js9, dgd8 = (g(QS, s, y) for s in ("JS8S", "JS97", "DGD8"))
    if None not in (js8, js9, dgd8):
        check("QSA1 JS8S+JS97=DGD8", y, js8 + js9, dgd8, 0.101, note="pp; three terms each rounded to 1dp, so up to 0.1")
        put(y, "qsa_pension_contribution_pp", js9, "pct", "JS97", "JS97")
        put(y, "qsa_nonpension_contribution_pp", js8, "pct", "JS8S", "JS8S")
    # UKEA ratio (this vintage) vs QSA ratio (latest vintage): vintage difference, informational
    check("QSA2 DGD8 vs UKEA DG5H (vintage)", y, dgd8, g(UK, "DG5H", y), 0.0, hard=False,
          note="different release vintages; report, do not splice")
    check("QSA3 RPHA vs HABN (vintage)", y, g(QS, "RPHA", y), B6, 0.0, hard=False, note="GBPm vintage")
    csj8 = g(QS, "CSJ8", y)
    if csj8 is not None:
        put(y, "cash_basis_saving_ratio_pct", csj8, "pct", "CSJ8", "CSJ8")
    # ---- 2. income side: shares of gross primary income B.5g ----------------
    if B5:
        for item, sid in (("D1_compensation", "HAEB"), ("B2gB3g_operating_mixed", "CRTY"),
                          ("D4_property_received", "HAXU"), ("D4_property_paid", "HACX")):
            v = g(UK, sid, y)
            put(y, item + "_GBPm", v, "GBPm", sid, sid)
            put(y, item + "_share_B5g", div(v, B5), "ratio", f"{sid}/B5g", f"{sid},HABL")
        put(y, "B5g_primary_GBPm", B5, "GBPm", "HABL", "HABL")
        net4 = add(g(UK, "HAXU", y), -(g(UK, "HACX", y) or 0))
        put(y, "D4_net_GBPm", net4, "GBPm", "HAXU-HACX", "HAXU,HACX")
        put(y, "D4_net_share_B5g", div(net4, B5), "ratio", "(HAXU-HACX)/B5g", "HAXU,HACX,HABL")
        check("ID3 D1+B2B3+D4rec-D4paid=B5g", y,
              (g(UK, "HAEB", y) or 0) + (g(UK, "CRTY", y) or 0) + (g(UK, "HAXU", y) or 0) - (g(UK, "HACX", y) or 0),
              B5, 3.0, note="GBPm")
    # ---- 3. property income composition (received) --------------------------
    comp = {"D41_interest": "HAXV", "D42_distributed": "HAXW", "D441_insurance_attrib": "KZK8",
            "D442_pension_attrib": "KZK9", "D443_cis": "L5V2", "D45_rent_on_land": "M8MD"}
    for item, sid in comp.items():
        put(y, item + "_GBPm", g(UK, sid, y), "GBPm", sid, sid)
    d4 = g(UK, "HAXU", y)
    if d4:
        parts = [g(UK, s, y) for s in ("HAXV", "HAXW", "NRVN", "M8MD")]
        if None not in parts:
            check("ID4 D41+D42+D44+D45=D4", y, sum(parts), d4, 3.0, note="GBPm")
        d44 = g(UK, "NRVN", y)
        subs = [g(UK, s, y) for s in ("KZK8", "KZK9", "L5V2")]
        if d44 and None not in subs:
            check("ID5 D441+D442+D443=D44", y, sum(subs), d44, 3.0, note="GBPm")
        k9, d614 = g(UK, "KZK9", y), g(UK, "L8Q9", y)
        check("ID6 D442=D614 (paid back)", y, k9, d614, 1.0, note="GBPm")
        direct = d4 - (g(UK, "KZK8", y) or 0) - (g(UK, "KZK9", y) or 0)
        put(y, "D4_excl_D441_D442_GBPm", direct, "GBPm", "D4 - D441 - D442", "HAXU,KZK8,KZK9")
        if B6:
            put(y, "D4_excl_D441_D442_share_B6g", direct / B6, "ratio", "(D4-D441-D442)/B6g", "HAXU,KZK8,KZK9,HABN")
            put(y, "D442_share_B6g", div(k9, B6), "ratio", "D442/B6g", "KZK9,HABN")
    # ---- 4. social contributions and benefits (pension-relevant) -----------
    for item, sid in (("D611_employer_actual", "L8NL"), ("D612_employer_imputed", "MA4A"),
                      ("D613_household_actual", "L8PT"), ("D614_supplements", "L8Q9"),
                      ("D61SC_service_charges", "M92I"), ("D61_net_contributions", "HADI"),
                      ("D621_social_security_cash", "L8QH"), ("D622_other_social_insurance", "L8QV"),
                      ("D623_social_assistance", "HAYU"), ("D62_benefits", "HAYP"),
                      ("D51_income_tax", "HAYD"), ("D5_taxes_income_wealth", "HAYC")):
        put(y, item + "_GBPm", g(UK, sid, y), "GBPm", sid, sid)
    p = [g(UK, s, y) for s in ("L8NL", "MA4A", "L8PT", "L8Q9", "M92I")]
    if None not in p and g(UK, "HADI", y):
        check("ID7 D611+D612+D613+D614+D61SC=D61", y, sum(p), g(UK, "HADI", y), 3.0, note="GBPm")
    d622 = g(UK, "L8QV", y)
    if D8 is not None and d622:
        put(y, "D8_over_D622", D8 / d622, "ratio", "D8/D622 (descriptive only)", "HAZA,L8QV")
    if B6:
        put(y, "D622_share_B6g", div(d622, B6), "ratio", "D622/B6g", "L8QV,HABN")
        put(y, "D5_share_B5g", div(g(UK, "HAYC", y), B5), "ratio", "D5/B5g", "HAYC,HABL")
    # ---- 5. imputed-rent / housing services against held stocks -------------
    b2 = g(UK, "HABM", y)
    dw0, ld0 = g(NB, "E46V", y - 1), g(NB, "E44N", y - 1)
    if None not in (b2, dw0, ld0):
        put(y, "B2g_over_open_dwellings_land", b2 / (dw0 + ld0), "ratio",
            "HABM/(E46V+E44N)[t-1]; GBPm over end-prior-year stock", "HABM,E46V,E44N")
    # ---- 6. net worth, stocks and the net-worth constraint -------------------
    nw1, nw0 = g(NB, "E45V", y), g(NB, "E45V", y - 1)
    if None not in (nw1, nw0):
        put(y, "NW_S14_end", nw1, "GBPm", "E45V", "E45V")
        put(y, "dNW_S14", nw1 - nw0, "GBPm", "E45V[t]-E45V[t-1]", "E45V")
        if B8:
            put(y, "B8g_over_open_NW", B8 / nw0, "ratio", "B8g/E45V[t-1] (gross of CFC)", "HADA,E45V")
            put(y, "nonpension_B8g_over_open_NW", (B8 - D8) / nw0, "ratio", "(B8g-D8)/E45V[t-1]", "HADA,HAZA,E45V")
            put(y, "D8_over_open_NW", D8 / nw0, "ratio", "D8/E45V[t-1]", "HAZA,E45V")
        b101 = g(UK, "HABD", y)
        b102, b103 = g(UK, "CWU2", y), g(UK, "CWUR", y)
        if None not in (b101, b102, b103):
            resid = (nw1 - nw0) - b101 - b102 - b103
            put(y, "B101g_saving_plus_capital_transfers", b101, "GBPm", "HABD", "HABD")
            put(y, "B102_other_volume_fin", b102, "GBPm", "CWU2 (S14+S15)", "CWU2")
            put(y, "B103_holding_gain_fin", b103, "GBPm", "CWUR (S14+S15, financial only)", "CWUR")
            put(y, "O_residual_dNW_less_B101g_B102_B103", resid, "GBPm",
                "dNW - B101g - B102 - B103 ; contains -CFC, non-financial revaluation, S15 mismatch, discrepancy",
                "E45V,HABD,CWU2,CWUR")
            put(y, "O_residual_over_open_NW", resid / nw0, "ratio", "residual/E45V[t-1]", "as above")
        # arithmetic checks on held pieces
        nf1 = add(g(NB, "E462", y), g(NB, "E3VW", y), g(FI, "NYOH", y))
        check("ID8 E45V=AN.1+AN.2+BF.90 (S14)", y, nf1, nw1, 3.0, note="GBPm")
    b9n = g(UK, "A99R", y)
    if None not in (b101 if 'b101' in dir() else None, g(UK, "NRLK", y), g(UK, "HAZJ", y), b9n):
        check("ID9 B101g-P5g-NP=B9N", y, g(UK, "HABD", y) - g(UK, "NRLK", y) - g(UK, "HAZJ", y), b9n, 3.0, note="GBPm")
    chk_b101 = add(B8, g(UK, "HAZC", y), -(g(UK, "HADR", y) or 0)) if B8 is not None else None
    check("ID10 B8g+D9r-D9p=B101g", y, chk_b101, g(UK, "HABD", y), 3.0, note="GBPm")
    # revaluation components of B.103 (financial) by instrument
    rev = [g(UK, s, y) for s in ("M9XL", "N48T", "N4AV", "N4CX", "N4EV", "N4GT", "N4IV")]
    if None not in rev and g(UK, "CWUR", y) is not None:
        check("ID11 sum B103 instruments=CWUR", y, sum(rev), g(UK, "CWUR", y), 3.0, note="GBPm")
        put(y, "B103_AF5_equity", g(UK, "N4CX", y), "GBPm", "N4CX", "N4CX")
        put(y, "B103_AF6_pension_insurance", g(UK, "N4EV", y), "GBPm", "N4EV", "N4EV")
    # financial leg: net financial assets
    f1, f0 = g(FI, "NYOH", y), g(FI, "NYOH", y - 1)
    if None not in (f1, f0):
        put(y, "dNFA_S14", f1 - f0, "GBPm", "NYOH[t]-NYOH[t-1]", "NYOH")
        if b9n is not None and g(UK, "CWU2", y) is not None:
            r2 = (f1 - f0) - b9n - g(UK, "CWU2", y) - g(UK, "CWUR", y)
            put(y, "O_fin_residual_dNFA_less_B9N_B102_B103", r2, "GBPm",
                "dNFA - B9N - B102 - B103 (S14 vs S14+S15 mismatch, statistical discrepancy)", "NYOH,A99R,CWU2,CWUR")
    # ---- 7. real erosion of opening liabilities (derived, not in B.103) -----
    defl, defl0 = g(UK, "CRXA", y), g(UK, "CRXA", y - 1)
    L0 = g(FI, "NIWJ", y - 1)
    A0 = g(FI, "NITF", y - 1)
    if None not in (defl, defl0, L0):
        pi = defl / defl0 - 1
        put(y, "pi_hfce_deflator", pi, "ratio", "CRXA[t]/CRXA[t-1]-1", "CRXA")
        put(y, "real_erosion_opening_liabilities_GBPm", L0 * pi / (1 + pi), "GBPm",
            "NIWJ[t-1]*pi/(1+pi); loans are valued at par so this is NOT in B.103", "NIWJ,CRXA")
        if nw0:
            put(y, "real_erosion_over_open_NW", L0 * pi / (1 + pi) / nw0, "ratio", "above/E45V[t-1]", "NIWJ,CRXA,E45V")
    # ---- 8. property income per opening financial assets (descriptive bounds)
    if A0 and d4:
        put(y, "D4_received_over_open_total_fin_assets", d4 / A0, "ratio",
            "HAXU/NITF[t-1]; denominator includes pension and insurance entitlements. Not a yield.", "HAXU,NITF")
        put(y, "D4_excl_D441_D442_over_open_total_fin_assets", (d4 - (g(UK, 'KZK8', y) or 0) - (g(UK, 'KZK9', y) or 0)) / A0,
            "ratio", "(D4-D441-D442)/NITF[t-1]; not a yield", "HAXU,KZK8,KZK9,NITF")

with open(os.path.join(HERE, "derived_ons_flows.csv"), "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["year", "item", "value", "unit", "formula", "inputs"])
    w.writerows(out)
with open(os.path.join(HERE, "derived_ons_checks.csv"), "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["check", "year", "computed", "published", "diff", "tolerance", "result", "kind", "note"])
    w.writerows(chk)

fails = [c for c in chk if c[6] == "FAIL"]
by = {}
for c in chk:
    by.setdefault(c[0], [0, 0, 0.0])
    by[c[0]][0] += 1
    by[c[0]][1] += c[6] == "FAIL"
    by[c[0]][2] = max(by[c[0]][2], abs(c[4]))
for k, (n, nf, mx) in by.items():
    print(f"{k:42s} n={n:3d} fail={nf:3d} max|diff|={mx:.4f}")
print(f"rows={len(out)} checks={len(chk)} hard_fail={len(fails)}")
for c in fails[:15]:
    print("FAIL", c)
sys.exit(1 if fails else 0)
