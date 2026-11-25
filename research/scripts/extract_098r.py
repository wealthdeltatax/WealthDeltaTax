"""098r: extract published WAS, ONS and ETB tables as tidy text. Run from anywhere: python -I extract_098r.py [REPO_ROOT]
REPO_ROOT defaults to the repository containing this file. Reads (needs openpyxl):
  data/rates/totalwealthtables.xlsx, data/rates/financialwealthtables.xlsx, data/uk-source-workbooks/etbreferencetablesfye202324final.xlsx
  and, from data/uk-wealth-tables/098r/, the ONS workbooks 2813, 3222, periodcohortqx2024basedgb.xlsx and gb1/gb_ppp_machine_readable.xlsx.
Writes CSVs into data/uk-wealth-tables/098r/. Percentages are as published (rounded to whole numbers); nothing is smoothed or inferred
except the columns whose names start with `derived_`, which are weighted total x rounded percentage and carry that rounding."""
import csv, re, sys, warnings
from pathlib import Path
import openpyxl
warnings.filterwarnings('ignore')
HERE = Path(__file__).resolve().parents[2] / 'data' / 'uk-wealth-tables' / '098r'   # the 098r tables (was the folder of this script)
ROOT = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).resolve().parents[2]
RETR = '2026-11-21'
SUP = {'[u]', '[x]', '[c]', '[w]', '..', '-', '[z]', ''}


def num(v):
    """Return (float or None, flag): flag keeps the published marker for a suppressed or empty cell."""
    if v is None:
        return None, 'empty'
    s = str(v).strip()
    if s in SUP or re.fullmatch(r'\[[a-z]\]', s):
        return None, s or 'empty'
    try:
        return float(s.replace(',', '')), ''
    except ValueError:
        return None, s


def clean(s):
    return re.sub(r'\s+', ' ', str(s or '').replace('\n', ' ')).strip()


def write(name, head, rows):
    with open(HERE / name, 'w', newline='', encoding='utf-8') as f:
        w = csv.writer(f)
        w.writerow(head)
        w.writerows(rows)
    print(name, len(rows), 'rows')


def sheet(path, name):
    wb = openpyxl.load_workbook(path, read_only=True)
    return list(wb[name].iter_rows(values_only=True))


ROUND = re.compile(r'^(July 20\d\d to June 20\d\d|April 20\d\d to March 20\d\d)')
BANDS7 = ['Less than £20,000', '£20,000 but < £85,000', '£85,000 but < £200,000', '£200,000 but < £300,000',
          '£300,000 but < £500,000', '£500,000 but < £1 million', '£1 million or more']


# ---------- WAS banded person tables: 2.11 (age), 2.13 (economic activity); 5.17, 5.19 (net financial wealth) ----------
def banded_persons(wbpath, sh, kind, wealth):
    rows = sheet(wbpath, sh)
    hi = next(i for i, r in enumerate(rows) if r[3 if kind == 'activity' else 2] and 'Less than' in str(r[3 if kind == 'activity' else 2]))
    c0 = 3 if kind == 'activity' else 2
    # the band header may sit in the first data columns; locate the first band column by the header row
    hdr = [clean(c) for c in rows[hi]]
    first = next(j for j, h in enumerate(hdr) if h.startswith('Less than'))
    bands = hdr[first:first + 7]
    unw = next((j for j, h in enumerate(hdr) if h.startswith('Unweighted')), None)
    wtd = next((j for j, h in enumerate(hdr) if h.startswith('Weighted')), None)
    out, rnd, parent = [], None, ''
    for i, r in enumerate(rows[hi + 1:], hi + 2):
        if r[0] and ROUND.match(clean(r[0])):
            rnd = ROUND.match(clean(r[0])).group(1)
        elif r[0] and rnd and (str(r[0]).startswith('Source') or re.match(r'^\d:', str(r[0]))):
            break
        if rnd is None:
            continue
        lab_cells = [clean(c) for c in r[:first] if c is not None and not (str(c) in ROUND.pattern)]
        lab_cells = [c for c in lab_cells if not ROUND.match(c)]
        if kind == 'activity':
            if len(r) > 1 and r[1]:
                parent = clean(r[1])
            label = clean(r[2]) if r[2] else ''
            if not label:
                continue
            level = 'sub' if str(r[2]).startswith('    ') else 'main'
            grp = parent if level == 'main' else parent
        else:
            label = lab_cells[-1] if lab_cells else ''
            grp, level = '', 'main'
        if not label:
            continue
        vals = [num(r[first + k]) for k in range(7)]
        un = num(r[unw])[0] if unw is not None else None
        wt = num(r[wtd])[0] if wtd is not None else None
        for k, (v, flag) in enumerate(vals):
            out.append([sh, rnd, kind, grp, label, level, bands[k], v if v is not None else '', flag,
                        int(un) if un is not None else '', int(wt) if wt is not None else '',
                        'Great Britain', wealth, '% of persons in the row group', Path(wbpath).name, RETR])
    return out


PHEAD = ['table', 'round', 'group_kind', 'parent_group', 'group', 'level', 'wealth_band', 'percent', 'flag',
         'unweighted_n', 'weighted_n', 'geography', 'wealth_measure', 'unit', 'source_file', 'retrieval_date']


def was():
    tw = ROOT / 'data/rates/totalwealthtables.xlsx'
    fw = ROOT / 'data/rates/financialwealthtables.xlsx'
    age = banded_persons(tw, 'Table 2.11', 'age', 'household total wealth')
    act = banded_persons(tw, 'Table 2.13', 'activity', 'household total wealth')
    write('was_persons_age_by_wealth_band.csv', PHEAD, age)
    write('was_persons_activity_by_wealth_band.csv', PHEAD, act)
    # households by band: Table 2.5 percentage and frequency blocks
    rows = sheet(tw, 'Table 2.5')
    rounds = [clean(c) for c in rows[2][2:] if c]
    rounds = [re.sub(r'^\(\d\)\s*', '', x) for x in rounds]
    out, meas = [], None
    for r in rows[3:]:
        if r[0] and (str(r[0]).startswith('Source') or re.match(r'^\d:', str(r[0]))):
            break
        if r[0]:
            meas = clean(r[0])
        label = clean(r[1])
        if not label or meas is None:
            continue
        for k, rd in enumerate(rounds):
            v, flag = num(r[2 + k])
            out.append(['Table 2.5', rd, meas, label, v if v is not None else '', flag,
                        '£' if 'Wealth' in meas and 'Frequency' not in meas else ('households' if 'Frequency' in meas else '%'),
                        'Great Britain', 'Table 2.5 (banded household total wealth)', RETR])
    write('was_households_by_wealth_band.csv',
          ['table', 'round', 'measure', 'wealth_band', 'value', 'flag', 'unit', 'geography', 'source_file', 'retrieval_date'], out)
    return act, out


# ---------- derived stage weights on WDT bands ----------
# WAS £ bands 1-7 -> WDT bands. Partition chosen to follow the pack's decile shares; the achieved household share is reported.
MAP = [('D1-3', [0, 1], (0, 30)), ('D4-5', [2, 3], (30, 50)), ('D6-7', [4], (50, 70)), ('D8-9', [5], (70, 90)), ('D10', [6], (90, 100))]
STAGE = {'In employment': 'working', 'Unemployed': 'unemployed', 'Student': 'inactive_not_retired',
         'Looking after family/home': 'inactive_not_retired', 'Sick/disabled (2)': 'inactive_not_retired',
         'Other inactive': 'inactive_not_retired', 'Retired': 'retired'}


def derived(act, hh):
    rounds = []
    for r in act:
        if r[1] not in rounds:
            rounds.append(r[1])
    out, cov = [], []
    hhpct = {(r[1], r[3]): r[4] for r in hh if r[2] == 'Percentage of households' or r[2].startswith('Percentage')}
    for rd in rounds:
        pct = [hhpct.get((rd, b)) for b in BANDS7]
        if any(p in (None, '') for p in pct):
            continue
        cum = [sum(pct[:k + 1]) for k in range(7)]
        for wb_, idx, (lo, hi) in MAP:
            lo_a = 0 if idx[0] == 0 else cum[idx[0] - 1]
            hi_a = cum[idx[-1]]
            cov.append([rd, wb_, lo, hi, lo_a, hi_a, round(hi_a - lo_a, 1), ' + '.join(BANDS7[i] for i in idx)])
        tot = {}
        for r in act:
            if r[1] != rd or r[5] != 'main' or r[4] not in STAGE or r[7] == '' or r[10] == '':
                continue
            k = BANDS7.index(r[6])
            tot[(STAGE[r[4]], r[4], k)] = r[7] / 100 * r[10]
        for wb_, idx, _ in MAP:
            band_total = sum(v for (s, g, k), v in tot.items() if k in idx)
            for stage in ('working', 'unemployed', 'inactive_not_retired', 'retired'):
                n = sum(v for (s, g, k), v in tot.items() if s == stage and k in idx)
                out.append([rd, wb_, stage, round(n), round(n / band_total * 100, 1) if band_total else '',
                            round(band_total), 'adults 16+, persons; derived: weighted total x rounded % (each cell +-0.5pp of its row total)',
                            'Table 2.13', RETR])
    write('was_stage_by_wdt_band_derived.csv',
          ['round', 'wdt_band', 'stage', 'derived_persons', 'derived_share_of_band_pct', 'derived_band_total_persons', 'note', 'source_table', 'retrieval_date'], out)
    write('was_band_edge_mapping.csv',
          ['round', 'wdt_band', 'target_cum_lo_pct', 'target_cum_hi_pct', 'was_cum_lo_pct', 'was_cum_hi_pct', 'was_household_share_pct', 'was_bands_used'], cov)


# ---------- ONS workbooks ----------
def ons_2813():
    rows = sheet(HERE / 'meanmedianaggregateandpercentageofwealthbywealthcomponentandageofhouseholdreferenceperson.xlsx', 'Table_1')
    grp, names = '', []
    for j in range(1, len(rows[2])):
        if rows[2][j]:
            grp = clean(re.sub(r'\[\d+\]', '', str(rows[2][j])))
        names.append((grp, clean(rows[3][j])))
    out = []
    for r in rows[4:]:
        if not r[0] or str(r[0]).startswith('Source'):
            break
        for j, (g, s) in enumerate(names, 1):
            v, flag = num(r[j])
            unit = '£' if '(£)' in s else ('£ million' if '£ million' in s else '%')
            out.append([clean(r[0]), g, re.sub(r'\s*\(.*\)', '', s), v if v is not None else '', flag, unit,
                        'Great Britain', 'April 2020 to March 2022', 'ONS Ad hoc 2813', RETR])
    write('ons_was_wealth_by_age_of_hrp.csv',
          ['hrp_age', 'wealth_component', 'statistic', 'value', 'flag', 'unit', 'geography', 'period', 'source', 'retrieval_date'], out)


def ons_3222():
    p = HERE / 'personalfinancialandpropertydebtbyageandregion.xlsx'
    out = []
    for sh, kind in (('Table 1', 'personal financial debt'), ('Table 2', 'personal property debt')):
        rows = sheet(p, sh)
        hdr = [clean(c) for c in rows[5]]
        for r in rows[6:]:
            if not (r[0] and r[1]):
                continue
            for j, h in enumerate(hdr):
                if j < 2 or 'CI' in h or h == '':
                    continue
                v, flag = num(r[j])
                lo = num(r[j - 1])[0] if 'CI' in hdr[j - 1] else None
                up = num(r[j + 1])[0] if j + 1 < len(hdr) and 'CI' in hdr[j + 1] else None
                unit = '£' if '(£)' in h else 'persons or households'
                out.append([sh, kind, clean(r[0]), clean(r[1]), re.sub(r'\s*\(£\)', '', h), v if v is not None else '', flag,
                            lo if lo is not None else '', up if up is not None else '', unit,
                            'Great Britain', 'April 2020 to March 2022', 'ONS Ad hoc 3222', RETR])
    write('ons_was_debt_by_age_region.csv',
          ['table', 'debt_type', 'age_band', 'region', 'measure', 'value', 'flag', 'lower_ci', 'upper_ci', 'unit', 'geography', 'period', 'source', 'retrieval_date'], out)


def ons_population():
    rows = sheet(HERE / 'gb1/gb_ppp_machine_readable.xlsx', 'Population')
    yrs = [str(c) for c in rows[0]]
    out = []
    for r in rows[1:]:
        for j in range(2, len(r)):
            y = int(yrs[j])
            if 2024 <= y <= 2074 and r[j] is not None:
                out.append([r[0], str(r[1]), y, int(r[j]), 'persons', 'Great Britain', '2024-based principal projection',
                            'ONS 2024-based national population projections (28 April 2026)', RETR])
    write('ons_population_gb_principal_2024based.csv',
          ['sex', 'age', 'year', 'population', 'unit', 'geography', 'projection', 'source', 'retrieval_date'], out)


def ons_qx():
    wb = openpyxl.load_workbook(HERE / 'periodcohortqx2024basedgb.xlsx', read_only=True)
    out = []
    for sh in ('males period qx', 'females period qx', 'males cohort qx', 'females cohort qx'):
        rows = list(wb[sh].iter_rows(values_only=True))
        sex, basis = sh.split()[0], sh.split()[1]
        hdr = [clean(c) for c in rows[3]]
        cols = {j: int(re.sub(r'\D', '', h)) for j, h in enumerate(hdr) if j > 0 and re.search(r'\d{4}', h)}
        lim = (2024, 2074) if basis == 'period' else (1981, 2024)
        for r in rows[4:]:
            if r[0] is None or not str(r[0]).strip().isdigit():
                continue
            age = int(str(r[0]).strip())
            if not 16 <= age <= 100:
                continue
            for j, y in cols.items():
                if lim[0] <= y <= lim[1] and r[j] is not None:
                    out.append([sex, basis, age, y, float(r[j]), 'per 100,000', 'Great Britain', 'principal projection, 2024-based',
                                'ONS Ad hoc 3459', RETR])
    write('ons_qx_gb_2024based.csv',
          ['sex', 'basis', 'exact_age', 'year_or_birth_year', 'qx', 'unit', 'geography', 'projection', 'source', 'retrieval_date'], out)


# ---------- ETB: retired and non-retired individuals by equivalised disposable income decile ----------
def etb():
    p = ROOT / 'data/uk-source-workbooks/etbreferencetablesfye202324final.xlsx'
    out = []
    for sh, grp in (('Table 4b', 'retired individuals'), ('Table 3b', 'non-retired individuals')):
        rows = sheet(p, sh)
        hi = next(i for i, r in enumerate(rows) if r[2] == 'Bottom')
        deciles = [clean(c) for c in rows[hi][2:13]]
        section = ''
        for r in rows[hi + 1:]:
            if r[0] is None and r[1] is None:
                continue
            if r[0]:
                section = clean(r[0])
            item = clean(r[1])
            if not item or str(r[0] or '').startswith(('See', 'Source', 'Notes')):
                continue
            for k, d in enumerate(deciles):
                v, flag = num(r[2 + k])
                out.append([sh, grp, section, item, d, v if v is not None else '', flag,
                            '£ per year' if 'Number' not in item else 'count (sample)', 'UK', '2023/24', 'ONS ETB reference tables FYE 2023/24', RETR])
    write('etb_income_by_decile_retired_nonretired.csv',
          ['table', 'population', 'section', 'item', 'income_decile', 'value', 'flag', 'unit', 'geography', 'period', 'source', 'retrieval_date'], out)


if __name__ == '__main__':
    act, hh = was()
    derived(act, hh)
    ons_2813(); ons_3222(); ons_population(); ons_qx(); etb()
