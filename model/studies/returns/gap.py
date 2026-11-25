"""Brief 042r: bridge the return data 2019 to 2025. Run: python3 -I gap.py  (writes gap_results.json)
Inputs typed from pages read 2026-11-18 (see returns-gap.md section 3); JST series from model_v2/jst_r6.json via common.py."""
import sys, os, json; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
from common import load, real, acf
D = load()
# ---- ONS CPI annual average index, 2015=100 (series D7BT, OGL v3.0) ----
CPI = {2019: 107.8, 2020: 108.7, 2021: 111.6, 2022: 121.7, 2023: 130.5, 2024: 133.9, 2025: 138.4}
infl = {y: CPI[y] / CPI[y - 1] - 1 for y in range(2020, 2026)}
# ---- UK HPI, December on December, % (ONS / HM Land Registry, OGL v3.0), as first published in each December release ----
HPI = {2020: 8.5, 2021: 10.8, 2022: 9.8, 2023: -1.4, 2024: 4.6, 2025: 2.4}
RENT_YD = 0.0228           # JST housing_rent_rtn 2020, held, assumption: rent return held at the last JST value
def housing_real(y): return (1 + HPI[y] / 100 + RENT_YD) / (1 + infl[y]) - 1
house = {y: housing_real(y) for y in HPI}
# ---- 2020 wealth return from JST's own 2020 asset returns and composition (036r section 6 medians 1990-2019) ----
W_RISKY, W_EQ = 0.85, 0.35
def wealth_est(y):
    risky = W_EQ * D["eq_tr"][y] + (1 - W_EQ) * D["housing_tr"][y]
    safe = 0.5 * D["bond_tr"][y] + 0.5 * D["bill_rate"][y]
    nom = W_RISKY * risky + (1 - W_RISKY) * safe
    return (1 + nom) / (D["cpi"][y] / D["cpi"][y - 1]) - 1
diag = {y: dict(est=wealth_est(y), jst=(1 + D["capital_tr"][y]) / (D["cpi"][y] / D["cpi"][y - 1]) - 1) for y in range(2010, 2020)}
w2020 = wealth_est(2020)
# check: JST 2020 housing vs the ONS Dec-on-Dec
overlap = dict(jst_housing_nominal_capgain_2020=D["housing_tr"][2020], ons_dec_dec_hpi_2020=HPI[2020] / 100 + RENT_YD)
ys, r = real(D, "capital_tr")
def stats(x):
    n = len(x); mu = x.mean(); sd = x.std(ddof=1); rho = acf(x, 1)
    se = sd / np.sqrt(n) * np.sqrt((1 + rho) / (1 - rho))
    return dict(n=n, mean=100 * mu, sd=100 * sd, rho1=rho, se=100 * se, low=100 * (mu - 1.2816 * se), high=100 * (mu + 1.2816 * se), geo=100 * (np.exp(np.log1p(x).mean()) - 1))
S = {"S0 JST to 2019 (register I-D1a, I-D1b, I-D1b2)": stats(r)}
x1 = np.append(r, w2020)
S["S1 + 2020 (JST composition estimate)"] = stats(x1)
h = np.array([house[y] for y in range(2021, 2026)])
S["S2 + 2021-2025 at the housing-only proxy"] = stats(np.append(x1, h))
for d in (3, 6):
    S[f"S3 S2 with 2021-2025 {d} points lower (illustrative stress, assumption)"] = stats(np.append(x1, h - d / 100))
# sensitivity: shift in the mean from adding k years at mean m_k: k/(n+k) * (m_k - mean)
n0, mu0 = len(r), r.mean()
sens = {f"{m}": 100 * 5 / (n0 + 1 + 5) * (m / 100 - x1.mean()) for m in (-2, 0, 2, 4.74, 6, 8)}
out = dict(infl=infl, house_real=house, w2020=w2020, diag=diag, overlap=overlap, stats=S, sens_mean_shift_5yrs=sens, cpi=CPI, hpi=HPI, rent_yd=RENT_YD)
json.dump(out, open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "docs", "model-v3", "returns", "gap_results.json"), "w"), indent=1)
for y in HPI: print(y, "infl %.2f%% hpi %.1f%% housing real %.2f%%" % (100 * infl[y], HPI[y], 100 * house[y]))
print("wealth 2020 est %.2f%%" % (100 * w2020), "diag", {y: (round(100 * v['est'], 1), round(100 * v['jst'], 1)) for y, v in diag.items()})
print(overlap)
for k, v in S.items(): print(k, {a: round(b, 3) for a, b in v.items()})
print(sens)
