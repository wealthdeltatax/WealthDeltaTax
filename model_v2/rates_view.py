"""
rates_view.py -- JSON accessors shared by the RATES presentation scripts (8_2_RATES_tables.py, 8_3_RATES_charts.py)
===================================================================================================================
Read-only helpers over rates_data.json: no simulation, no import of rates_core, no formatting beyond scenario labels.
They were duplicated in both scripts (patch W2-08); one copy now. Underscore aliases in the scripts keep call sites unchanged.
"""
from wdt_fmt import fmt_pct


def med(x, arg=None, all_windows=False):
    """
    Median lookup, two call forms:
      med(sc, mode)               scenario block -> (medians, mode_used). Uses `mode` if the scenario ran it,
                                  else the one mode it did run (e.g. the house-index scenario).
      med(h, col, all_windows)    headline block (or None) -> the median of column `col`, over uncensored
                                  windows, or over all windows with all_windows=True.
    """
    if x is None:
        return None
    if 'headline' in x:                                  # scenario form
        hl = x['headline']
        m = arg if arg in hl else next(iter(hl))
        return hl[m]['overall']['medians'], m
    ov = x['overall']                                    # headline-block form
    src = (ov.get('medians_all') if all_windows else ov.get('medians')) or {}
    return src.get(arg)


def hl(sc, mode, contiguous=False):
    """Headline block of one mode (full loop or contiguous-only). None if the scenario has no such windows."""
    blk = sc.get('headline_contiguous' if contiguous else 'headline') or {}
    if not blk:
        return None
    return blk[mode if mode in blk else next(iter(blk))]


def pq(h, col, key):
    """p10 / p90 of a column over uncensored windows."""
    if h is None:
        return None
    return (h['overall'].get(key) or {}).get(col)


def years(med_, prefix):
    """Sorted tenth years present in a medians dict, e.g. rel_y10, rel_y20, ..."""
    return sorted(int(k[len(prefix):]) for k in med_ if k.startswith(prefix) and k[len(prefix):].isdigit())


def need(data, name):
    """Scenario block, or None with a note saying how to run it."""
    sc = data['scenarios'].get(name)
    if sc is None:
        print(f'  skipped: scenario {name!r} is not in rates_data.json (run it: python rates_core.py --scenario {name})')
    return sc


def route_b_names(data, p):
    """Scenarios of [rates.figures].route_b that are in the JSON, in order."""
    out = []
    for n in p['rates']['figures'].get('route_b', []):
        if n in data['scenarios']:
            out.append(n)
        else:
            print(f'  note: route_b scenario {n!r} not in rates_data.json')
    return out


def default_of_mode(data, names, mode):
    """First scenario in `names` running Route B in `mode` with no spread / cap override (the mode's default case)."""
    for n in names:
        rb = data['scenarios'][n].get('route_b') or {}
        if rb.get('mode') == mode and rb.get('deferral_spread') is None and rb.get('income_cap') is None:
            return n
    return None


def rb_label(sc, long=False):
    """Route B scenario label. long=True (tables) names where an unset spread / cap comes from; short (charts) says 'default'."""
    rb = sc.get('route_b') or {}
    m = rb.get('mode', 'sale')
    if m == 'lien':
        sp = rb.get('deferral_spread')
        return 'Lien' + (f', spread {fmt_pct(sp, 0)}' if sp is not None else (', spread from [route_b]' if long else ', default spread'))
    if m == 'income':
        cap = rb.get('income_cap')
        return 'Income' + (f', cap {fmt_pct(cap, 0)}' if cap is not None else (', cap from [income]' if long else ', default cap'))
    return 'Sale (cash-equivalent units)' if long else 'Sale'
