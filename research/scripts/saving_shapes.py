"""145r block 2: three saving shapes (flat, mild, steep) over the model's 14 lines, scaled so aggregate saving equals flat's at every flat value.
Reads the pack and register read-only (model_v3.core.pack, base.build_base at ratio 0.44, the test ratio) for each line's adults and income; the flat values from
docs/model-v3/household-arm-account/account_table.csv (min, median, max of the ONS non-pension saving ratio). Nothing is run in the model; no concentration is computed.
Writes saving_shapes.csv (one row per line and shape) and saving_evidence.csv (figures with page and flag). Prints one line; exits 1 on a failed check.
Run from the repo root: python -I research/scripts/saving_shapes.py
Scaling: s_i = s + delta_i, delta_i = A * (h_i - hbar), hbar the income-weighted mean of h, so sum(w_i * s_i) = s for every s (w_i = line income share). Additive, because the flat value can be negative."""
import csv, sys, collections
from pathlib import Path
import numpy as np
sys.path.insert(0, '.')
from model_v3.core import pack as pk, base as bs
D = Path('research/tables/145r-saving-shapes-and-withdrawal-range')
pack, reg = pk.load_pack(Path('model_v3/pack/GBR')), pk.load_register(Path('registry/inputs.json'))
b = bs.build_base(pack, reg, 0.44)
inc = np.where(np.isnan(b.income), reg['I-D9a'].low / reg['I-D4h'].central / 1e6, b.income)   # as runner/arm.py line_state does
ad = np.asarray(b.adults_k, float); w = inc * ad / (inc * ad).sum()
cum = np.cumsum(ad) / ad.sum() * 100; rank = cum - ad / ad.sum() * 50               # adult percentile at the middle of each line
flat = collections.OrderedDict((r['saving_value'], float(r['saving'])) for r in csv.DictReader(open('docs/model-v3/household-arm-account/account_table.csv')))
fails = []
if len(b.labels) != 14 or abs(w.sum() - 1) > 1e-12 or abs(cum[-1] - 100) > 1e-9: fails.append('lines or weights not as expected')
if list(flat) != ['min', 'median', 'max']: fails.append('flat values not min, median, max')
step = (rank > 20).astype(float)                                                       # D1, D2 below the 20th percentile (Norway row I-W3a: near zero below, flat above)
ramp = np.clip((rank - 25.0) / (100.0 - 25.0), 0.0, 1.0)                               # from the middle of D3 to the top of the distribution
SHAPES = {'flat': (0.0, np.zeros(len(rank))), 'mild': (0.07, step), 'steep': (0.07, step + ramp)}   # A in ratio units (7 pp); h is the index
rows = []
for name, (A, h) in SHAPES.items():
    hbar = float((w * h).sum()); delta = A * (h - hbar)
    if abs(float((w * delta).sum())) > 1e-12: fails.append(f'{name}: deltas not income-weighted zero')
    for i, lab in enumerate(b.labels):
        r = dict(line=lab, shape=name, adult_percentile_mid=round(float(rank[i]), 3), adults_k=round(float(ad[i]), 3), income_share=round(float(w[i]), 6), delta_pp=round(100 * float(delta[i]), 4))
        for k, s in flat.items():
            r[f'ratio_{k}_pct'] = round(100 * (s + float(delta[i])), 4)
        rows.append(r)
    for k, s in flat.items():
        agg = sum(w[i] * (s + float(delta[i])) for i in range(len(w)))
        if abs(agg - s) > 1e-12: fails.append(f'{name} {k}: aggregate {agg} != flat {s}')
import re, subprocess
def rfpage(p):
    t = subprocess.run(['pdftotext', '-f', str(p), '-l', str(p), '-layout', 'literature/Before-the-fall.pdf', '-'], capture_output=True, text=True).stdout
    return re.sub(r'\s+', '', t)
for p, strs in {7: ['just\u00a3\u200b80', '\u00a34,200'], 29: ['\u00a380compared', '\u00a34,100'], 32: ['morethan\u00a3300', '\u00a34,200'], 38: ['55percent', '64percent', '23percent', '45percent'], 21: ['53percent', '47percent', '40percent'], 30: ['25percentinQ22020']}.items():
    t = rfpage(p)
    for x in strs:
        x2 = re.sub(r'\s+', '', x).replace('\u200b', '').replace('\u00a0', '')
        if x2 not in t.replace('\u00a0', '').replace('\u200b', ''): fails.append(f'RF p{p}: {x!r} not found')
cols = list(rows[0])
with open(D / 'saving_shapes.csv', 'w', newline='') as f:
    wr = csv.DictWriter(f, cols); wr.writeheader(); wr.writerows(rows)
RF = 'Resolution Foundation, Before the Fall (2025), WAS, GB'
ev = [
 ('S-P01', f'{RF}: typical family, lowest income quintile, rise in liquid savings 2019-20 to 2021-22', '80', 'GBP', '7 and 29', 'text', 'by income quintile, liquid savings only, pandemic window; not a saving rate, not by wealth'),
 ('S-P02', f'{RF}: typical family, highest income quintile, same', '4200', 'GBP', '7 and 32', 'text', 'p.29 gives 4,100 for higher-income families'),
 ('S-P03', f'{RF}: second income quintile, same, against the two years before', 'more than 300 against 100', 'GBP', '32', 'text', 'text says a threefold increase; the chart label 310 is not used'),
 ('S-P04', f'{RF}: share of families that increased liquid savings, bottom and top income quintile', '55; 64', '%', '38', 'text', 'flatter than pandemic-era surveys (23; 45)'),
 ('S-P05', f'{RF}: active share of the growth in average family wealth, since 2010-12; latest period (includes the pandemic)', '47; 40', '%', '21', 'text', 'aggregate, includes debt repayment; excludes DB and pensions in payment (note 19)'),
 ('S-P06', f'{RF}: adjusted household saving ratio, peak Q2 2020', '25', '%', '30', 'text', 'aggregate; excludes pension equity adjustments'),
 ('S-R01', 'Register I-W3a (Fagereng and others, Norway 2005-2015): net active saving by wealth, flat from about the 20th percentile, near zero around the 15th', '6 to 8', '% of disposable income', 'source pp. 2, 24-25 (as the register states)', 'read from register row; source not held here', 'foreign; the only banded shape held; the saving ratio of the model is a share of income'),
 ('S-R02', 'Register I-W3b (same source): gross saving rate of the top 1%', '35', '%', 'source pp. 2, 25', 'read from register row; source not held here', 'context only by author ruling: includes capital gains, not a saving parameter; not used'),
 ('S-R03', 'Register I-W3c: UK share of the change in family financial wealth that is net saving (Bangham and Leslie 2020)', '7 to 24', '%', 'source p. 18', 'read from register row; source not held here', 'aggregate, not by wealth band'),
]
with open(D / 'saving_evidence.csv', 'w', newline='') as f:
    wr = csv.writer(f); wr.writerow(['row_id', 'item', 'value', 'unit', 'page', 'flag', 'note_or_challenge']); wr.writerows(ev)
if fails: print('FAILED:', *fails, sep='\n'); sys.exit(1)
dl = {n: [r['delta_pp'] for r in rows if r['shape'] == n] for n in SHAPES}
print('ok: 14 lines x 3 shapes; aggregate saving equals flat at min, median, max for every shape; mild delta_pp', dl['mild'][0], dl['mild'][-1], '; steep', dl['steep'][0], dl['steep'][-1])
