"""Brief 125c block 1: write moments_map.csv, one row per row of research/tables/099r-held-research-moments/moments.csv. Run from the repository root: python -I model/studies/household-arm-validation/make_map.py
Status codes: computable (validate.py computes an analogue), definition differs (held, but the model has no analogue of that definition), not held (no data held; `needs` says what would resolve it)."""
import csv
from pathlib import Path

HERE = Path(__file__).resolve().parent
SRC = HERE.parents[2] / 'research' / 'tables' / '099r-held-research-moments' / 'moments.csv'
COLS = ('id', 'source', 'held_as_data', 'validation_moment', 'status', 'analogue', 'computed_where', 'definitions_that_differ', 'needs')

# id -> (status, analogue, computed where, definitions that differ, needs)
MAP = {
    'BF-11': ('computable', 'Aggregate net wealth over GDP and the class shares at year 0 (the pack: WAS Table 2.1 basis)', 'validate.py wealth_gdp', 'RF values pensions at market annuity rates, the pack at ONS SCAPE; price bases may differ; year 0 is the pack, so it is a consistency check, not a test of the run', ''),
    'BF-12': ('definition differs', 'Mean wealth per household by pack band (not per adult family by wealth decile)', 'not computed', 'per-adult family deciles against household bands; RF pension valuation', 'microdata or a per-adult conversion of the pack bands'),
    'BF-13': ('computable', 'Wealth share of the top band (D10, the top 10% of households) at year 0 and year 100 untaxed', 'validate.py top_share', 'the observed top 10% hold about half (families, RF basis); D10 is households, pack basis. The 18% to 23% top-1% share is not computable: no split inside D10', 'a split of D10'),
    'EER-01': ('definition differs', 'Top-1% share of wealth', 'not computable', 'the model has no split inside D10; the paper excludes unfunded DB; survey against national-accounts aggregates', 'a split of D10 (Pareto tail), or a top-1% row in the pack'),
    'TZ-01': ('definition differs', 'Wealth above fixed pound thresholds from 50m', 'not computable', 'above the top band; Rich List net worth, resident entries; totals differ by population (not reconciled)', 'a tail row in the pack'),
    'BF-14': ('computable', 'Retired cells share of wealth at year 0 (the stage split of wealth is by person share)', 'validate.py retired_share', 'observed is people aged 60 and over (an age proxy; retired not identified); the model stage split is by person share, so its number is the person share, not a wealth measure', 'wealth by stage and age'),
    'BF-15': ('computable', 'Realised household saving ratio, total, year 1 (S over income, pension accrual included)', 'validate.py saving_ratio', 'the RF 25% is a seasonally adjusted quarterly adjusted ratio (not held); the held annual DGD8 is 16.5% in 2020 and 5.7% in 2019; the model non-pension ratio is an input drawn from the same ONS series', 'the quarterly series'),
    'GB-01': ('computable', 'Realised household saving ratio, total, year 1', 'validate.py saving_ratio', 'held annual DGD8 5.0% (2022) and 9.6% (2025) against the report 4.0% and 10.8% (vintage, quarter); the non-pension ratio is an input from the same series', ''),
}
NEEDS = {
    'AB-04': 'WAS financial wealth for 2006-08 and 2016-18 on one price basis (only 2020-22 is held); the observed 1.4tn to 2.3tn is the paper figure, not held data',
    'BF-01': 'RF active and passive decomposition tables', 'BF-02': 'the same decomposition', 'BF-03': 'median passive return by wealth quintile',
    'BF-04': 'linked WAS microdata (UKDS)', 'BF-05': 'linked WAS microdata (UKDS)', 'BF-06': 'linked WAS microdata (UKDS)', 'BF-07': 'linked WAS microdata (UKDS)',
    'BF-08': 'WAS composition by age and income', 'BF-09': 'WAS liquid-asset tables by income quintile', 'BF-10': 'the same', 'AB-01': 'Bangham and Leslie 2020 decomposition',
    'AB-02': 'linked WAS microdata (UKDS)', 'AB-03': 'WAS microdata or the paper tables', 'AB-05': 'WAS financial wealth by asset type and decile',
    'AT-01': 'none (an illustration, not data)', 'AT-02': 'none (a US study)', 'AT-03': 'none (other countries, taxable wealth response)', 'SM-01': 'HMRC SPI tables', 'SM-02': 'HMRC SPI tables',
    'TZ-02': 'the Rich List series with entries and exits', 'ZM-01': 'none (global billionaires)', 'TD-01': 'ELSA (not held)', 'TD-02': 'HMRC probate estate tables', 'GB-02': 'a forecast, not an observation',
}


def main():
    rows = list(csv.DictReader(open(SRC, encoding='utf-8')))
    out = []
    for r in rows:
        held = r['held_as_data'].split(':')[0].split('.')[0].split(' ')[0].strip().lower()
        held = {'yes': 'yes', 'partly': 'partly'}.get(held, 'no')
        val = 'no' if r['validation_moment_096r'].strip().lower() == 'none' else 'yes'
        if r['id'] in MAP:
            st, an, where, diff, need = MAP[r['id']]
        else:
            st, an, where, diff, need = 'not held', '', '', r['what_it_mixes'][:160], NEEDS[r['id']]
        out.append(dict(id=r['id'], source=r['source'].split(' (')[0], held_as_data=held, validation_moment=val, status=st, analogue=an, computed_where=where, definitions_that_differ=diff, needs=need))
    with open(HERE / 'moments_map.csv', 'w', newline='', encoding='utf-8') as fh:
        w = csv.DictWriter(fh, COLS); w.writeheader(); w.writerows(out)
    n = lambda k, v: sum(1 for o in out if o[k] == v)
    print(f"{len(out)} rows; held yes {n('held_as_data','yes')}, partly {n('held_as_data','partly')}, no {n('held_as_data','no')}; validation moments {n('validation_moment','yes')}; "
          f"computable {n('status','computable')}, definition differs {n('status','definition differs')}, not held {n('status','not held')}")
    print('validation moments that are held or partly held:', [o['id'] for o in out if o['validation_moment'] == 'yes' and o['held_as_data'] != 'no'])


main()
