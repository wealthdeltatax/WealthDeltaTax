"""146r block 2: the pack's own top-1% and top-decile shares, the Advani-Summers-Tarrant (AST 2025) range, and the stock scalings for ast_low (14.4%) and ast_high (16.5%).
Read only: the pack and register through model_v3.core.pack / base.build_base (ratio 0.44) and runner.arm.line_state (class balances, I-D1l cap). Nothing is run in the model.
AST figures are asserted on their PDF pages (docs/research/data/129r/1-s2.0-S0014292125001266-main.pdf; journal page = PDF page). Writes tail_current.csv, tail_ast_evidence.csv, tail_scenarios.csv.
Prints one line; exits 1 on any failed check. Run from the repo root: python -I docs/research/data/146r/top_tail_mapping.py"""
import csv, re, subprocess, sys
from pathlib import Path
import numpy as np
sys.path.insert(0, '.')
from model_v3.core import pack as pk, base as bs
from model_v3.runner import arm
D = Path('docs/research/data/146r'); PDF = 'docs/research/data/129r/1-s2.0-S0014292125001266-main.pdf'
P, R = pk.load_pack(Path('model_v3/pack/GBR')), pk.load_register(Path('registry/inputs.json'))
b = bs.build_base(P, R, 0.44)
fails = []
def page(p): return re.sub(r'\s+', '', subprocess.run(['pdftotext', '-f', str(p), '-l', str(p), '-layout', PDF, '-'], capture_output=True, text=True).stdout)
def need(p, *ss):
    t = page(p)
    for s in ss:
        if re.sub(r'\s+', '', s) not in t: fails.append(f'AST p{p}: {s!r} not found')
need(1, 'between 14.4% and 16.5% – in 2016–18'); need(2, 'aggregate net wealth was £14.2 trillion', '£9.9 trillion', 'individuals aged 20 or older', 'We exclude consumer durables')
need(5, 'The Pareto adjusted series is actually our preferred series'); need(12, 'rising from 14.4% to 16.5%', '12% and 18%'); need(13, "Income capitalisation, survey aggregates")
need(8, 'unfunded DB pensions decreases the top 1% share')
L = list(b.labels); W = np.asarray(b.wealth_bn, float); T = float(W.sum()); A = np.asarray(b.adults_k, float)
if L != ['D1', 'D2', 'D3', 'D4', 'D5', 'D6', 'D7', 'D8', 'D9', 'D10a', 'D10b', 'RL3', 'RL2', 'RL1']: fails.append('lines changed')
top1, top10 = float(W[10:].sum()), float(W[9:].sum())
survey_total = T / (1 + R['I-D4e'].central / 100)                                   # before the missing-wealth addition
cur = [('pack total after the missing-wealth addition', T, 'GBP bn'), ('top 1% (D10b, RL3, RL2, RL1) wealth', top1, 'GBP bn'), ('top 1% share of the pack total', 100 * top1 / T, '%'),
       ('top 10% (D10a and the top 1%) share of the pack total', 100 * top10 / T, '%'), ('survey total before the addition (I-D4e 5%)', survey_total, 'GBP bn'),
       ('register I-D4d (top 1% of the survey total, WAS as published)', R['I-D4d'].central, '%'), ('top 10% of the survey total (the survey deciles, no addition)', 100 * (top10 - R['I-D4e'].central / 100 * survey_total) / survey_total, '%'),
       ('Rich List total inside the top 1% (I-D4f)', R['I-D4f'].central, 'GBP bn'), ('adults share of the top 1% and of the top 10%', f'{100 * A[10:].sum() / A.sum():.2f}; {100 * A[9:].sum() / A.sum():.2f}', '% of adults')]
with open(D / 'tail_current.csv', 'w', newline='') as f:
    w = csv.writer(f); w.writerow(['item', 'value', 'unit']); w.writerows([[a, round(v, 3) if isinstance(v, float) else v, u] for a, v, u in cur])
if abs(100 * top1 / T - 21.9048) > 1e-3: fails.append('pack top 1% share differs from 21.9048')
st = arm.line_state(b, P.tables['decile_composition'], R, 0.01, cap=R['I-D1l'].central)
cap = R['I-D1l'].central; pen = st['pos']['pension']; per_adult = W / A                                   # GBP bn / thousand adults = GBP m per adult
SC = {'ast_low': 14.4, 'ast_high': 16.5}; list_bn = R['I-D4f'].central
rows = []
def share(Wv): return 100 * Wv[10:].sum() / Wv.sum(), 100 * Wv[9:].sum() / Wv.sum()
for sname, tgt in SC.items():
    for scaled in ('all_top1_lines', 'D10b_only_list_fixed'):
        for off in ('to_D10a', 'pro_rata_D1_to_D10a', 'none_total_falls'):
            Wn = W.copy(); t = tgt / 100
            if off == 'none_total_falls':                                          # target is a share of the new total: top1' = t * (rest + top1')
                rest = W[:10].sum(); new_top1 = t * rest / (1 - t)
            else:
                new_top1 = t * T
            if scaled == 'all_top1_lines':
                Wn[10:] = W[10:] * new_top1 / top1
            else:
                Wn[10] = new_top1 - list_bn
            moved = top1 - Wn[10:].sum()
            if off == 'to_D10a': Wn[9] += moved
            elif off == 'pro_rata_D1_to_D10a': Wn[:10] += moved * W[:10] / W[:10].sum()
            ok_total = abs(Wn.sum() - T) < 1e-6 if off != 'none_total_falls' else True
            nonpen_after = Wn[10:] / A[10:] - np.minimum(pen[10:], cap)            # non-pension per adult in the reduced lines (pension left at its balance)
            s1, s10 = share(Wn)
            if scaled == 'D10b_only_list_fixed' and Wn[10] <= 0: fails.append('D10b not positive')
            if not ok_total: fails.append('total not held')
            if (nonpen_after < 0).any(): fails.append(f'{sname} {scaled} {off}: non-pension of a top line negative')
            rows.append([sname, tgt, scaled, off, round(float(moved), 1), round(s1, 2), round(s10, 2), round(float(Wn.sum()), 1), round(float(Wn.sum() / T), 4),
                         round(float(Wn[9] / A[9]), 3), round(float(Wn[10] / A[10]), 3), round(float(nonpen_after.min()), 3), round(float(pen[9]), 4), round(float(pen[10]), 4)])
HDR = ['setting', 'top1_target_pct', 'lines_scaled', 'offset', 'wealth_moved_gbp_bn', 'top1_share_pct', 'top10_share_pct', 'total_gbp_bn', 'total_vs_pack', 'D10a_per_adult_gbp_m', 'D10b_per_adult_gbp_m', 'min_nonpension_top_line_gbp_m', 'D10a_pension_gbp_m', 'D10b_pension_gbp_m']
with open(D / 'tail_scenarios.csv', 'w', newline='') as f:
    w = csv.writer(f); w.writerow(HDR); w.writerows(rows)
EV = [('T-P01', 'top 1% wealth share, 2016-18, income capitalisation, survey aggregates', 14.4, '%', '1, 12, Fig. 3 (p. 13)', 'text and figure', 'individuals aged 20+; capitalised income, not the WAS distribution; no Pareto adjustment'),
      ('T-P02', 'same, National Accounts aggregates (after reranking)', 16.5, '%', '1, 12, Fig. 3', 'text and figure', 'NA aggregate total £9.9tn against survey £14.2tn (p. 2)'),
      ('T-P03', 'over 2006 to 2016-18 the top 1% share is higher with NA than survey aggregates by', '2.1 to 3.3 points (12 to 18%)', 'points', '12', 'text', 'the 2016-18 gap is 2.1'),
      ('T-P04', 'aggregate net wealth, 2016-18, survey and National Accounts', '14.2; 9.9', 'GBP trillion', '2', 'text', 'different wealth definitions (pension, housing)'),
      ('T-P05', 'wealth definition and population', 'market value of assets net of debts incl. pension entitlements; excludes consumer durables, vehicles, unfunded DB (main results); individuals aged 20 or older', '', '2', 'text', 'the pack lines are adults of households, wealth per adult equal inside a household'),
      ('T-P06', 'preferred series (Pareto-adjusted survey distribution), top 1% share', 'not held', '', '5 (stated); Appendix F.3', 'unset', 'data request: the appendix is not in the held 18-page PDF'),
      ('T-P07', 'including unfunded DB pensions lowers the top 1% share', 'size not held', '', '8; Appendix F.2', 'unset', 'direction only')]
with open(D / 'tail_ast_evidence.csv', 'w', newline='') as f:
    w = csv.writer(f); w.writerow(['row_id', 'item', 'value', 'unit', 'page', 'flag', 'note_or_challenge']); w.writerows(EV)
if fails: print('FAILED:', *fails, sep='\n'); sys.exit(1)
print(f'ok: pack top 1% {100 * top1 / T:.2f}% and top 10% {100 * top10 / T:.2f}% of GBP {T:.1f}bn; {len(rows)} scenario rows; AST figures found on their pages')
