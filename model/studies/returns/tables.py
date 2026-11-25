"""Builds tables.md from the JSON outputs of the other scripts. Run order: run_generators, run_level2, run_composition, run_convergence, tables, check."""
import sys, os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import json
H = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..', 'results', 'returns'); L = lambda f: json.load(open(os.path.join(H, f)))
G, V, C, K = L("generators_out.json"), L("level2_out.json"), L("composition_out.json"), L("convergence_out.json")
p = lambda x, d=2: f"{100*x:.{d}f}"
T = {}
rows = ["| Generator | Mean | Geo | SD | Loss yrs | Lag-1 | Longest run (mean) | 100y paths with run >= 4 | with run >= 6 | 30y geo mean P10 / P50 / P90 (independent paths) | Same, 88-window style on 117y paths |", "|---|---|---|---|---|---|---|---|---|---|---|"]
o = G["observed (117 years)"]
rows.append(f"| **Observed, 117 years** | {p(o['mean'])} | {p(o['geo'])} | {p(o['sd'])} | {p(o['loss'],1)} | {o['ac1']:.2f} | 5 (6 across the gap) | n/a (one path) | n/a | {p(o['g30_p10'])} / {p(o['g30_p50'])} / {p(o['g30_p90'])} (88 windows) | same |")
for k, v in G.items():
    if k in ("observed (117 years)", "fit", "pw_block", "acf"): continue
    w = v.get("w117"); ww = " / ".join(p(x) for x in w) if w else "n/a"
    rows.append(f"| {k} | {p(v['mean'])} | {p(v['geo'])} | {p(v['sd'] if not isinstance(v['sd'], list) else v['sd'][0]) if not isinstance(v['sd'], list) else 'mixture'} | {p(v['loss'],1)} | {v['ac1']:.2f} | {v['run_mean']:.1f} | {p(v['run4'],0)}% | {p(v['run6'],0)}% | {p(v['g30_p10'])} / {p(v['g30_p50'])} / {p(v['g30_p90'])} | {ww} |")
T["generators"] = "\n".join(rows)
f = G["fit"]
T["fit"] = (f"Normal: log-likelihood {f['normal']['ll']:.1f}, BIC {f['normal']['bic']:.1f}. Student t: df {f['t']['df']}, BIC {f['t']['bic']:.1f} (skew {f['moments']['skew']:.2f}, kurtosis {f['moments']['kurt']:.2f}). "
            f"AR(1): phi {f['ar1']['phi']:.3f} (SE {f['ar1']['se_phi']:.3f}, t {f['ar1']['phi']/f['ar1']['se_phi']:.1f}), 115 pairs. 2-state HMM: log-likelihood {f['hmm']['ll']:.1f}, BIC {f['hmm']['bic']:.1f}. "
            f"Autocorrelation lags 1 to 5: {', '.join(f'{x:.2f}' for x in G['acf'])} (about 2 standard errors at 0.18). Politis-White block length: {G['pw_block']:.2f}.")
s = V["subs"]
T["subs"] = "\n".join(["| Sample | Years | Arithmetic | Geometric | SD | Loss years |", "|---|---|---|---|---|---|"] + [f"| {k} | {v['n']} | {p(v['mean'])} | {p(v['geo'])} | {p(v['sd'])} | {p(v['loss'],1)}% |" for k, v in s.items()])
l2 = V["lvl2"]
T["se"] = (f"Naive SE {p(V['se_naive'])}; AR(1) corrected {p(V['se_ar1'])} (x{V['inflation_ar1']:.2f}); Newey-West (2 lags) {p(V['se_hac_nw2'])}; block bootstrap {p(V['boot_se_mean'])}; AR(1) parametric bootstrap {p(V['par_boot']['se_mean'])}. "
           f"Effective independent annual observations {V['n_eff']:.0f}. Block-bootstrap interval for the mean, 2.5/10/50/90/97.5%: {', '.join(p(v) for v in V['boot_mean_p'].values())}.")
T["lvl2"] = "\n".join(["| Parameter | Low (10th) | Central | High (90th) | 95% interval |", "|---|---|---|---|---|",
    f"| Arithmetic mean, % a year | {p(l2['mean'][0])} | {p(l2['mean'][1])} | {p(l2['mean'][2])} | {p(l2['mean95'][0])} to {p(l2['mean95'][1])} |",
    f"| Standard deviation, % a year | {p(l2['sd'][0])} | {p(l2['sd'][1])} | {p(l2['sd'][2])} | |",
    f"| Lag-1 autocorrelation | {l2['rho'][0]:.2f} | {l2['rho'][1]:.2f} | {l2['rho'][2]:.2f} | |"])
st = V["sup_t"]; c5 = V["contrast_1950"]; c8 = V["contrast_1980"]
T["break"] = (f"Largest mean-shift statistic over candidate break years (15% trimmed): {st['stat']:.2f} at {st['year']}; null 95th percentile {st['null_p95']:.2f}; p = {st['p_value']:.2f} (AR(1) parametric bootstrap, 2,000 series). "
              f"Fixed-date contrasts (the date picked after seeing the data): 1950 on versus before {p(c5['diff'])} points, t = {c5['t']:.2f}; 1980 on versus before {p(c8['diff'])} points, t = {c8['t']:.2f}.")
iw = C["implied_weights"]
T["weights"] = "\n".join(["| Period | Risky weight (equity plus housing), median | Equity within risky, median |", "|---|---|---|"] + [f"| {k} | {v['risky_w_median']:.2f} (n={v['risky_n']}) | {v['equity_in_risky_median']:.2f} (n={v['eq_n']}) |" for k, v in iw.items()])
se_ = C["series"]
T["series"] = "\n".join(["| Real return series (JST UK) | Mean 1896-2019 | Geo | SD | Mean 1950-2019 | SD |", "|---|---|---|---|---|---|"] + [f"| {k} | {p(v['1896-2019']['mean'])} | {p(v['1896-2019']['geo'])} | {p(v['1896-2019']['sd'])} | {p(v['1950-2019']['mean'])} | {p(v['1950-2019']['sd'])} |" for k, v in se_.items()])
rs = C["round8_shares"]
T["mix"] = "\n".join(["| Band (Round 8, Table 2.2) | Property | Financial | Pension | Physical | Mix mean (financial 30/60/90% equity) | Mix SD (same) |", "|---|---|---|---|---|---|---|"] + [
    f"| {g} | {p(rs[g]['property'],0)}% | {p(rs[g]['financial'],0)}% | {p(rs[g]['pension'],0)}% | {p(rs[g]['physical'],0)}% | {p(C['mixes'][g+', financial 30% equity']['mean'])} / {p(C['mixes'][g+', financial 60% equity']['mean'])} / {p(C['mixes'][g+', financial 90% equity']['mean'])} | {p(C['mixes'][g+', financial 30% equity']['sd'])} / {p(C['mixes'][g+', financial 60% equity']['sd'])} / {p(C['mixes'][g+', financial 90% equity']['sd'])} |" for g in rs] + [
    f"| JST wealth return, same years | | | | | {p(C['mixes']['JST wealth return, same years']['mean'])} | {p(C['mixes']['JST wealth return, same years']['sd'])} |"])
T["conv"] = "\n".join(["| Paths N | Mean 100y gain | range over 5 seeds | 30y mean P10 | range | 30y mean | range | 30y mean P90 | range | Within 0.1? |", "|---|---|---|---|---|---|---|---|---|---|"] + [
    f"| {t['N']:,} | {t['mean100_mid']:.3f} | {t['mean100_range']:.3f} | {t['p10_30_mid']:.3f} | {t['p10_30_range']:.3f} | {t['mean_30_mid']:.3f} | {t['mean_30_range']:.3f} | {t['p90_30_mid']:.3f} | {t['p90_30_range']:.3f} | {'yes' if t['settled'] else 'no'} |" for t in K["table"]])
with open(os.path.join(H, "tables.md"), "w") as fh:
    for k, v in T.items(): fh.write(f"### {k}\n\n{v}\n\n")
print(open(os.path.join(H, "tables.md")).read())
