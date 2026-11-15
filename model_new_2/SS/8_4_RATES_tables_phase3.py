"""
8_4_RATES_tables_phase3.py -- RATES tables for the Phase 3 outputs (WDT_Refactor_Plan section 5)
================================================================================================
PRESENTATION LAYER. Reads OUTPUTS/RATES/rates_data.json and nothing else. No simulation, no import
of rates_core. Fold into 8_2_RATES_tables.py once the numbering settles (one tables script per paper).

Tables 26-30, one per figure in 8_5_RATES_charts_phase3.py (same number, same slug); confirm numbers against the paper
  T26   effective windows at T, full loop vs contiguous-only, with n_eff       (plan 5.6)
  T27   relief and expenditure every 10 years, full loop vs contiguous-only     (plan 5.1)
  T28  Route B: sale vs lien (spread sweep) vs income (cap sweep): fund and receivable  (plan 5.2, 5.3)
  T29  Route B by launch-wealth band: receipts, receivable, tax saved by deferral      (plan 5.2)
  T30  Route B by launch-wealth band: family wealth at window end                      (plan 5.2)

Inputs named in [rates.figures]: scenario, mode, route_b. Nothing scenario-specific is typed here.
Outputs: OUTPUTS/RATES/tables/rates_table_{n}_{slug}.md

Sample notes the tables carry (read these before quoting)
  * Percentiles stored in the JSON are over windows where the fund FILLS (uncensored). Medians in `medians_all`
    are over all windows. T27 therefore shows p10 / p90 for filling windows only, and the share of windows that
    never fill is reported beside it. Relief is zero before the fill, so an all-window median is dominated by the
    censored share.
  * The receivable (deferred lien outstanding) is NOT in the fund. It is always shown in its own column.
"""

import sys
from pathlib import Path

# wdt_* modules and WDT_Params.toml live in Model/, one level above this RATES folder
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import wdt_core as wc
from wdt_fmt import fmt_pct, fmt_f0, fmt_f, band_labels, out_dir, ensure_dir
from wdt_md import MdDoc, LEFT, RIGHT

CODE = 'RATES'
DASH = '—'


# ─────────────────────────────────────────────────────────────
# JSON accessors
# ─────────────────────────────────────────────────────────────

def _hl(sc, mode, contiguous=False):
    """Headline block of one mode (full loop or contiguous-only). None if the scenario has no such windows."""
    blk = sc.get('headline_contiguous' if contiguous else 'headline') or {}
    if not blk:
        return None
    return blk[mode if mode in blk else next(iter(blk))]


def _med(h, col, all_windows=False):
    if h is None:
        return None
    ov = h['overall']
    src = (ov.get('medians_all') if all_windows else ov.get('medians')) or {}
    return src.get(col)


def _pq(h, col, key):
    """p10 / p90 of a column over uncensored windows."""
    if h is None:
        return None
    return (h['overall'].get(key) or {}).get(col)


def _years(med, prefix):
    """Sorted tenth years present in a medians dict, e.g. rel_y10, rel_y20, ..."""
    ks = [int(k[len(prefix):]) for k in med if k.startswith(prefix) and k[len(prefix):].isdigit()]
    return sorted(ks)


def _band_edges(sc):
    return sc['calibration']['bands']['edges_gbp_m']


def _need(data, name):
    sc = data['scenarios'].get(name)
    if sc is None:
        print(f'  skipped: scenario {name!r} is not in rates_data.json (run it: python rates_core.py --scenario {name})')
    return sc


def _range_cell(med, lo, hi, f):
    """'median [p10 to p90]' or the dash."""
    if med is None:
        return DASH
    if lo is None or hi is None:
        return f(med)
    return f'{f(med)} [{f(lo)} to {f(hi)}]'


# ─────────────────────────────────────────────────────────────
# T26  effective windows
# ─────────────────────────────────────────────────────────────

def t26_effective_windows(data, p):
    fg = p['rates']['figures']
    name, mode = fg['scenario'], fg['mode']
    sc = _need(data, name)
    if sc is None or 'effective_windows' not in sc:
        return None
    ew = sc['effective_windows']
    mode = mode if mode in ew['by_mode'] else next(iter(ew['by_mode']))
    blk = ew['by_mode'][mode]
    T = ew['T']

    def row(label, c):
        tot = c['total']
        return [label, f"{tot:,}", f"{c['contiguous']:,}", f"{c['wraps']:,}", f"{c['repeat']:,}",
                fmt_pct(c['repeat'] / tot, 1) if tot else DASH]

    rows = [row(iso, c) for iso, c in sorted(blk['by_country'].items())]
    rows.append(row('**All countries**', blk['overall']))

    doc = MdDoc()
    doc.table(['Country', 'Windows (full loop)', 'Contiguous only', 'Cross the seam', 'Repeat years', 'Share with repeats'],
              rows, col_fmt=[LEFT, RIGHT, RIGHT, RIGHT, RIGHT, RIGHT])
    doc.caption(f"Table 26: Effective windows at T = {T} years, scenario '{sc['label']}'. A window is T consecutive usable years "
                f"of one country; the series wraps from the last usable year to the first. Contiguous windows cross no seam and "
                f"have no calendar gap. Windows that repeat years (T longer than the usable series) are kept and flagged.")
    # independent windows: bootstrap n_eff (only scenarios in [rates.representativeness].bootstrap_scenarios carry it)
    case = p['rates']['replacement']['levy_case']
    for contiguous, lab in ((False, 'full loop'), (True, 'contiguous only')):
        h = _hl(sc, mode, contiguous)
        boot = (((h or {}).get('levy_variants') or {}).get(case) or {}).get('bootstrap')
        if not boot:
            continue
        cells = []
        for metric in ('relief_gdp', 'cov_ref', 'net_gdp_mean', 'drift'):
            m = boot.get(metric)
            if not m:
                continue
            ne = (m.get('period') or {}).get('n_eff')
            cells.append(f"{metric}: {m['n']:,} windows, n_eff {fmt_f0(ne)}")
        if cells:
            doc.add(f"Independent windows ({lab}, blocks of {boot['block_years']} start years across all countries): " + '; '.join(cells) + '.')
            doc.blank()
    return doc


# ─────────────────────────────────────────────────────────────
# T27  relief and expenditure every 10 years
# ─────────────────────────────────────────────────────────────

def t27_decade_relief(data, p):
    fg = p['rates']['figures']
    name, mode = fg['scenario'], fg['mode']
    sc = _need(data, name)
    if sc is None:
        return None
    full, cont = _hl(sc, mode, False), _hl(sc, mode, True)
    yrs = _years(full['overall']['medians'], 'rel_y')
    if not yrs:
        print('  skipped T27: no rel_y* columns in the JSON (re-run rates_core.py)')
        return None

    def ratio(h, k):
        r, e = _med(h, f'rel_y{k}'), _med(h, f'exp_y{k}')
        return (r / e) if (r is not None and e) else None

    def rel(h, k):
        return _range_cell(_med(h, f'rel_y{k}'), _pq(h, f'rel_y{k}', 'p10'), _pq(h, f'rel_y{k}', 'p90'), lambda v: fmt_pct(v, 2))

    rows = []
    for k in yrs:
        rows.append([f'**{k}**', rel(full, k), rel(cont, k), fmt_pct(_med(full, f'exp_y{k}'), 1),
                     fmt_pct(ratio(full, k), 0), fmt_pct(ratio(cont, k), 0) if cont else DASH])

    def cov_cell(h):
        return fmt_f0(_med(h, 'rel_cov_year')) if h else DASH
    rows.append(['**First year relief covers expenditure (median)**', cov_cell(full), cov_cell(cont), '', '', ''])
    rows.append(['**Windows that fill (of all)**',
                 f"{full['overall']['uncensored']:,} of {full['overall']['windows']:,}",
                 (f"{cont['overall']['uncensored']:,} of {cont['overall']['windows']:,}" if cont else DASH), '', '', ''])

    doc = MdDoc()
    doc.table(['Year', 'Relief / GDP, full loop', 'Relief / GDP, contiguous', 'Expenditure / GDP', 'Relief / expenditure, full loop',
               'Relief / expenditure, contiguous'], rows, col_fmt=[LEFT, RIGHT, RIGHT, RIGHT, RIGHT, RIGHT])
    doc.caption(f"Table 27: Relief and expenditure at every tenth year, scenario '{sc['label']}'. Median [p10 to p90] over windows in which "
                f"the fund fills; relief is zero before the fill. The ratio is the ratio of the two medians. The first-year row is the median "
                f"over windows in which relief reaches expenditure at all: windows where it never does are not in that median.")
    return doc


# ─────────────────────────────────────────────────────────────
# Route B scenario selection
# ─────────────────────────────────────────────────────────────

def _route_b_names(data, p):
    """Scenarios of [rates.figures].route_b that are in the JSON, in order."""
    out = []
    for n in p['rates']['figures'].get('route_b', []):
        if n in data['scenarios']:
            out.append(n)
        else:
            print(f'  note: route_b scenario {n!r} not in rates_data.json')
    return out


def _default_of_mode(data, names, mode):
    """First scenario in `names` running Route B in `mode` with no spread / cap override (the mode's default case)."""
    for n in names:
        rb = data['scenarios'][n].get('route_b') or {}
        if rb.get('mode') == mode and rb.get('deferral_spread') is None and rb.get('income_cap') is None:
            return n
    return None


def _rb_label(sc):
    rb = sc.get('route_b') or {}
    m = rb.get('mode', 'sale')
    if m == 'lien':
        sp = rb.get('deferral_spread')
        return 'Lien' + (f", spread {fmt_pct(sp, 0)}" if sp is not None else ', spread from [route_b]')
    if m == 'income':
        cap = rb.get('income_cap')
        return 'Income' + (f", cap {fmt_pct(cap, 0)}" if cap is not None else ', cap from [income]')
    return 'Sale (cash-equivalent units)'


# ─────────────────────────────────────────────────────────────
# T28  fund and receivable by Route B scenario
# ─────────────────────────────────────────────────────────────

def t28_route_b_fund(data, p):
    names = _route_b_names(data, p)
    if not names:
        return None
    mode = p['rates']['figures']['mode']
    rows = []
    for n in names:
        sc = data['scenarios'][n]
        h = _hl(sc, mode)
        ov = h['overall']
        rows.append([_rb_label(sc), fmt_pct(ov['censored_share'], 0), fmt_f0(_med(h, 'fill_year')),
                     fmt_pct(_med(h, 'relief_gdp'), 2), fmt_pct(_med(h, 'cov_ref'), 0),
                     fmt_pct(_med(h, 'fund_gdp_end', True), 1), fmt_pct(_med(h, 'lien_out_gdp_end', True), 1),
                     fmt_pct(_med(h, 'fund_plus_recv_gdp_end', True), 1)])
    doc = MdDoc()
    doc.table(['Route B treatment', 'Never fills', 'Fill year', 'Relief / GDP', 'Spending covered', 'Fund / GDP at end',
               'Receivable / GDP at end', 'Fund plus receivable'], rows, col_fmt=[LEFT] + [RIGHT] * 7)
    doc.caption("Table 28: Route B treatment and the fund. 'Never fills' is the share of all windows; fill year, relief and spending covered are "
                "medians over windows that fill; the three end-of-window columns are medians over all windows. The fund counts settled cash "
                "only: the deferred lien is the receivable, reported in its own column and never added to the fund. The last column is shown "
                "only to size the receivable.")
    return doc


# ─────────────────────────────────────────────────────────────
# T29 / T30  by launch-wealth band
# ─────────────────────────────────────────────────────────────

def _band_table(data, p, cols, caption, title_no):
    names = _route_b_names(data, p)
    pick = {m: _default_of_mode(data, names, m) for m in ('sale', 'lien', 'income')}
    have = {m: n for m, n in pick.items() if n}
    if 'sale' not in have or len(have) < 2:
        print(f'  skipped Table {title_no}: needs a sale scenario and at least one of lien / income in [rates.figures].route_b')
        return None
    sc0 = data['scenarios'][have['sale']]
    labels = band_labels(_band_edges(sc0))
    mode = p['rates']['figures']['mode']
    meds = {m: _hl(data['scenarios'][n], mode) for m, n in have.items()}
    heads, getters = cols(have)
    rows = []
    for i, lab in enumerate(labels):
        rows.append([lab] + [g(meds, i) for g in getters])
    doc = MdDoc()
    doc.table(['Launch wealth'] + heads, rows, col_fmt=[LEFT] + [RIGHT] * len(heads))
    doc.caption(caption)
    return doc


def t29_route_b_receipts(data, p):
    def cols(have):
        heads, gets = [], []

        def recv(m):
            return lambda meds, i: fmt_pct(_med(meds[m], f'recv_gdp_mean_band{i}', True), 3)
        heads.append('Receipts, sale')
        gets.append(recv('sale'))
        if 'lien' in have:
            heads += ['Receipts, lien', 'Receivable at end, lien', 'Saved by deferral']
            gets += [recv('lien'),
                     lambda meds, i: fmt_pct(_med(meds['lien'], f'lien_out_gdp_end_band{i}', True), 3),
                     lambda meds, i: fmt_pct(
                         (_med(meds['sale'], f'recv_gdp_mean_band{i}', True) or 0.0)
                         - (_med(meds['lien'], f'recv_gdp_mean_band{i}', True) or 0.0), 3)]
        if 'income' in have:
            heads.append('Receipts, income')
            gets.append(recv('income'))
        return heads, gets
    cap = ("Table 29: Route B by launch-wealth band, share of GDP, median over all windows. Receipts are the mean annual value reaching the "
           "state (units, income cash and lien settled at deaths). The receivable is the deferred lien still outstanding at the window end and is "
           "not in the fund. 'Saved by deferral' is sale receipts minus lien receipts: what lien holders do not pay while the balance is deferred. "
           "It is a timing effect, not forgiveness: read it with the receivable and with the spread sweep in Table 28.")
    return _band_table(data, p, cols, cap, '29')


def t30_route_b_wealth(data, p):
    def cols(have):
        heads, gets = [], []
        for m, lab in (('sale', 'sale'), ('lien', 'lien'), ('income', 'income')):
            if m in have:
                heads.append(f'Family wealth, {lab}')
                gets.append((lambda mm: lambda meds, i: fmt_pct(_med(meds[mm], f'wealth_gdp_end_band{i}', True), 2))(m))
        return heads, gets
    cap = ("Table 30: Family wealth at the window end by launch-wealth band, share of GDP, median over all windows. Reported on its own: it is "
           "not combined with cumulative income paid into one objective. Income mode pays the tax from external income rather than from holdings, "
           "so its family wealth is higher by construction; that gap is not a welfare gain until the income paid is set against it.")
    return _band_table(data, p, cols, cap, '30')


# ─────────────────────────────────────────────────────────────
# main
# ─────────────────────────────────────────────────────────────

# (number, slug, function): numbers and slugs must match FIGURES in 8_5_RATES_charts_phase3.py
TABLES = [(26, 'effective_windows', t26_effective_windows),
          (27, 'decade_relief', t27_decade_relief),
          (28, 'route_b_fund', t28_route_b_fund),
          (29, 'route_b_receipts', t29_route_b_receipts),
          (30, 'route_b_wealth', t30_route_b_wealth)]


def main(json_path=None, toml=None, out=None):
    p = wc.load_rates_params(toml)
    jp = Path(json_path) if json_path else out_dir(CODE) / 'rates_data.json'
    data = wc.load_json(jp)
    tdir = ensure_dir(Path(out) if out else out_dir(CODE) / 'tables')
    for n, slug, fn in TABLES:
        doc = fn(data, p)
        if doc is None:
            continue
        doc.write(tdir / f'rates_table_{n}_{slug}.md', verbose=False)
        print(f'  Table {n}: {slug}')


if __name__ == '__main__':
    main()
