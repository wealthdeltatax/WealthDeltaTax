"""146r block 1: evidence for a per-path real GDP-per-head growth process, from the pack's own JST series (read only).
Reads model_v3/pack/GBR via model_v3.core.pack, returns.real_series (the 128c market series: real total return on wealth, usable years) and revenue.gdp_growth.
Writes gdp_process.csv (statistics, proposed parameters, unset rows) and gdp_illustration.csv (arithmetic spread of the GDP index under the proposed AR(1); not a model run).
Prints one line; exits 1 on a failed check. Run from the repo root: python -I docs/research/data/146r/gdp_process.py"""
import csv, math, sys
from pathlib import Path
import numpy as np
sys.path.insert(0, '.')
from model_v3.core import pack as pk, returns as rt, revenue as rv
D = Path('docs/research/data/146r')
P = pk.load_pack(Path('model_v3/pack/GBR'))
yrs, r = rt.real_series(P)
g = 100 * rv.gdp_growth(P, yrs)
fails = []
def lag1(x):
    d = x - x.mean(); return float((d[:-1] * d[1:]).sum() / (d * d).sum())
def seg_lag1(x, y):                         # lag-1 inside each contiguous run only (no pair across the 1939/1947 gap)
    cuts = np.r_[0, np.where(np.diff(y) > 1)[0] + 1, len(y)]
    d = x - x.mean(); num = sum((d[a:b - 1] * d[a + 1:b]).sum() for a, b in zip(cuts[:-1], cuts[1:])); return float(num / (d * d).sum())
def fisher(rho, n):
    z, se = math.atanh(rho), 1 / math.sqrt(n - 3); return math.tanh(z - 1.96 * se), math.tanh(z + 1.96 * se)
if abs(g.mean() / 100 - 0.01570385404020596) > 1e-12: fails.append('mean GDP growth is not the model constant 0.0157039')
if len(yrs) != 117: fails.append(f'expected 117 usable years, got {len(yrs)}')
rows = []
def add(*a): rows.append(list(a))
SRC = 'pack returns.csv gdp_pc (JST R6 rgdpmad, real GDP per head) and capital_tr, cpi; years usable in returns.real_series'
W = {'all': (0, 9999), '1950-2019': (1950, 2019), '1871-1938': (1871, 1938)}
st = {}
for k, (a, b) in W.items():
    m = (yrs >= a) & (yrs <= b); gg, rr = g[m], r[m]
    c = float(np.corrcoef(gg, rr)[0, 1]); lo, hi = fisher(c, int(m.sum()))
    st[k] = dict(n=int(m.sum()), mean=float(gg.mean()), sd=float(gg.std(ddof=1)), phi=lag1(gg), corr=c, lo=lo, hi=hi)
    add(f'G-D-{k}', 'derived', f'real GDP per head growth, years {yrs[m][0]} to {yrs[m][-1]} ({int(m.sum())} usable years)', f'mean {gg.mean():.3f}; SD {gg.std(ddof=1):.3f}; lag-1 {lag1(gg):.3f}; corr with the market real return {c:.3f} (95% CI {lo:.2f} to {hi:.2f})', '% per year', SRC, 'computed from the pack table', 'derived', 'one realisation of one country; the 1940-46 gap is absent; war years inside the full sample')
a_all = st['all']
add('G-D-seg', 'derived', 'lag-1 of GDP growth inside the contiguous runs only (no pair across 1939/1947)', f'{seg_lag1(g, yrs):.3f}', 'ratio', SRC, 'computed', 'derived', 'the 128c market process takes its lag-1 over the concatenated series; the difference shows how much the gap pair matters')
add('G-D-lead', 'derived', 'correlation of GDP growth with the market real return one year earlier and one year later', f'{float(np.corrcoef(g[1:], r[:-1])[0, 1]):.3f}; {float(np.corrcoef(g[:-1], r[1:])[0, 1]):.3f}', 'ratio', SRC, 'computed (pairs with consecutive years only approximately: the gap pair is included)', 'derived', 'a descriptive check on the timing; not used in the proposal')
# relation between observed same-year correlation and innovation correlation of two AR(1)s
f1, f2 = lag1(r), a_all['phi']
k_adj = math.sqrt((1 - f1 ** 2) * (1 - f2 ** 2)) / (1 - f1 * f2)
add('G-D-adj', 'derived', 'factor: observed same-year correlation = innovation correlation x factor (two AR(1)s)', f'{k_adj:.4f}', 'ratio', 'arithmetic', 'formula', 'derived', 'so the innovation correlation equals the observed one to three decimals; the proposal uses the observed value as the innovation correlation')
# proposed process
add('G-S01', 'proposed', 'mean real GDP per head growth', '1.5704', '% per year', 'the pack constant (revenue.gdp_growth mean over the usable years); not a deviation', 'computed', 'derived', 'zero deviation reproduces the fixed arm (as for 128c); the process is a deviation around this mean')
add('G-S02', 'proposed', 'standard deviation of annual growth, marginal: option "full sample"', f'{a_all["sd"]:.2f}', '% per year', SRC, 'computed', 'derived', 'same 117 years as the market process, so the two share one sample; includes the war and depression years')
add('G-S03', 'proposed', 'standard deviation of annual growth, option "postwar"', f'{st["1950-2019"]["sd"]:.2f}', '% per year', SRC, 'computed', 'derived', 'a lower-volatility regime; 70 years; the author rules between the two')
add('G-S04', 'proposed', 'lag-1 autocorrelation (AR(1) coefficient)', f'{a_all["phi"]:.2f}', 'ratio', SRC, 'computed', 'derived', f'standard error about {1 / math.sqrt(a_all["n"]):.2f}; the postwar value is {st["1950-2019"]["phi"]:.2f}')
add('G-S05', 'proposed', 'correlation with the market return, option A: independent', '0', 'ratio', 'by construction', '', 'scenario', 'isolates growth risk from market risk; contradicts the sample (the independent value lies outside the 95% interval)')
add('G-S06', 'proposed', 'correlation with the market return, option B: historic', f'{a_all["corr"]:.2f}', 'ratio', SRC, 'computed', 'derived', f'95% interval {a_all["lo"]:.2f} to {a_all["hi"]:.2f} (Fisher); postwar {st["1950-2019"]["corr"]:.2f}; the author rules; no choice made here')
for i, t in enumerate(['a register row for the process (no I-D row holds GDP growth, its spread, persistence or correlation)', 'GDP growth after 2019 (the pack series ends 2019; 2020-21 and 2022-25 absent)', 'GDP growth by tail line or by band (income growth is one number for every line)', 'any link between GDP growth and property or physical returns (both fixed in 128c)', 'distribution shape (normal innovations assumed as for the market process; not tested for GDP growth here)']):
    add(f'G-U0{i + 1}', 'unset', t, '', '', '', '', 'unset', '')
with open(D / 'gdp_process.csv', 'w', newline='') as f:
    w = csv.writer(f); w.writerow(['row_id', 'kind', 'item', 'value', 'unit', 'source', 'flag', 'evidence_class', 'note_or_challenge']); w.writerows([x if len(x) == 9 else x[:5] + [x[5], x[6], x[7], x[8] if len(x) > 8 else ''] for x in rows])
# arithmetic illustration: sd of log GDP index deviation after T years of a stationary AR(1) of growth deviations, and the 10th-90th percentile ratio to the fixed path
ill = []
for name, sd in (('full sample', a_all['sd']), ('postwar', st['1950-2019']['sd'])):
    phi = a_all['phi']
    for T in (10, 25, 50, 100):
        var = T * (sd / 100) ** 2 * ((1 + phi) / (1 - phi) - 2 * phi * (1 - phi ** T) / (T * (1 - phi) ** 2))
        s = math.sqrt(var); ill.append([name, T, round(100 * s, 2), round(math.exp(-1.2816 * s), 3), round(math.exp(1.2816 * s), 3)])
with open(D / 'gdp_illustration.csv', 'w', newline='') as f:
    w = csv.writer(f); w.writerow(['sd_option', 'years', 'sd_log_gdp_index_pct', 'p10_ratio_to_fixed_path', 'p90_ratio_to_fixed_path']); w.writerows(ill)
if fails: print('FAILED:', *fails, sep='\n'); sys.exit(1)
print(f'ok: {len(rows)} rows; mean {a_all["mean"]:.4f}% equals the model constant; sd {a_all["sd"]:.2f}/{st["1950-2019"]["sd"]:.2f}; phi {a_all["phi"]:.2f}; corr {a_all["corr"]:.2f}')
