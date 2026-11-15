"""
5_9_VAL_numbers.py — numbers register (plan D8)
===============================================
Every number the prose may quote, named, with its source in valgen_data.json. Prose cites the id, never the
value; the register is regenerated with every run, so a changed result changes the number everywhere.
Presentation layer: reads valgen_data.json and the TOML only; no simulation, no core import.

Output: OUTPUTS/VAL/tables/val_numbers.md and OUTPUTS/VAL/val_numbers.json
Ids: <TEST OR OUTPUT>_<QUANTITY>_<BASE|CAND>; BASE = first rule in dmg_rules, CAND = last.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))   # model root
from wdt_core import load_params
from wdt_fmt import out_dir, ensure_dir, fmt_pct
from wdt_md import MdDoc, md_table

_DATA = out_dir('VAL') / 'valgen_data.json'
_OUT = out_dir('VAL')


def build(data: dict, p: dict) -> list:
    vg = p['val_gen']
    p5 = data['p5']
    rules = list(p5['dmg']['by_rule'])
    tag = {rules[0]: 'BASE', rules[-1]: 'CAND'}
    lam_b = vg['lambda_base']
    out = []

    def add(i, v, kind, src, note):
        out.append({'id': i, 'value': v, 'kind': kind, 'source': src, 'note': note})

    for r, t in tag.items():
        d = p5['dmg']['by_rule'][r]
        add(f'DMG_NDOM_{t}', d['n_dominant'], 'count', 'p5.dmg', f'strategies gaining in every scenario, {r}')
        add(f'DMG_NMAT_{t}', d['n_dominant_material'], 'count', 'p5.dmg', f'of those, gaining by more than the BRG tolerance, {r}')
        add(f'DMG_MAXIMIN_{t}', d['maximin']['min_gain'], 'pct3', 'p5.dmg', f'highest worst-scenario gain, {r}')
        add(f'DMG_NSCEN_{t}', d['n_scenarios'], 'count', 'p5.dmg', 'scenarios per rule set')
        vb = p5['verdict_by_rule'][r]
        add(f'BRG_WORST_{t}', vb['worst_best_response_gain'], 'pct1', 'p5.verdict_by_rule',
            f"worst best-response gain over lambda, {r} (at lambda {vb['worst_lambda']})")
        cells = [c for c in p5['hec']['cells'].values() if c['rule'] == r and c['sigma'] > 0.0]
        top = max(cells, key=lambda c: c['gain_mean'])
        add(f'HEC_MEANMAX_{t}', top['gain_mean'], 'pct2', 'p5.hec',
            f"largest mean gain from honest error, {r} (sigma {top['sigma']}, lambda {top['lambda']})")
        low = min(cells, key=lambda c: c['state_mean'])
        add(f'HEC_STATEMIN_{t}', low['state_mean'], 'pct2', 'p5.hec',
            f"largest mean fall in the state stake from honest error, {r}")
        uo = p5['uos']
        shares = uo['c_share_vals']
        def best(cs, d):
            return uo['cells'][f'{r}|{lam_b}|{cs}']['best'][d]['gain']
        cross = next((cs for cs in shares if best(cs, 'over') > best(cs, 'under')), None)
        above = next((cs for cs in shares if max(best(cs, 'over'), best(cs, 'under')) > p5['thresholds']['brg_tol']), None)
        add(f'UOS_CROSS_{t}', cross, 'pct0', 'p5.uos', f'smallest Route C share where overstating beats understating at lambda_base, {r}')
        add(f'UOS_BRGC_{t}', above, 'pct0', 'p5.uos', f'smallest Route C share where the best gain exceeds the BRG tolerance at lambda_base, {r}')
        add(f'UOS_OVERMAX_{t}', max(best(cs, 'over') for cs in shares), 'pct1', 'p5.uos', f'largest overstating gain over the share sweep at lambda_base, {r}')
        add(f'UOS_UNDERMAX_{t}', max(best(cs, 'under') for cs in shares), 'pct1', 'p5.uos', f'largest understating gain over the share sweep at lambda_base, {r}')
    lf = data['life']
    over = [(c['gain'], k) for k, c in lf['grid'].items() if float(k.split('|')[0]) > 1.0]
    under = [(c['gain'], k) for k, c in lf['grid'].items() if float(k.split('|')[0]) < 1.0]
    add('LIFE_OVERMAX', max(over)[0], 'pct1', 'life.grid', f"largest single-life gain from overstating (alpha|g {max(over)[1]})")
    add('LIFE_UNDERMAX', max(under)[0], 'pct1', 'life.grid', f"largest single-life gain from understating (alpha|g {max(under)[1]})")
    return out


_FMT = {'count': lambda v: f'{v:d}', 'pct0': lambda v: 'none' if v is None else fmt_pct(v, 0),
        'pct1': lambda v: fmt_pct(v, 1), 'pct2': lambda v: fmt_pct(v, 2), 'pct3': lambda v: fmt_pct(v, 3)}


def main() -> None:
    p = load_params()
    data = json.load(open(_DATA, encoding='utf-8'))
    nums = build(data, p)
    ensure_dir(_OUT)
    with open(_OUT / 'val_numbers.json', 'w', encoding='utf-8') as fh:
        json.dump(nums, fh, indent=1)
    rows = [[f"**{n['id']}**", _FMT[n['kind']](n['value']), n['source'], n['note']] for n in nums]
    doc = MdDoc()
    doc.add_block(md_table(['Id', 'Value', 'Source', 'Meaning'], rows, col_fmt=['left', 'center', 'left', 'left']))
    doc.write(_OUT / 'tables' / 'val_numbers.md')
    print(f'Written {len(nums)} numbers')


if __name__ == '__main__':
    main()
