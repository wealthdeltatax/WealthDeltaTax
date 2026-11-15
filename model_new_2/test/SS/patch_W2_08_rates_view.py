"""W2-08  One copy of the JSON accessors shared by 8_2_RATES_tables.py and 8_3_RATES_charts.py.

 new       Model/rates_view.py   med, hl, pq, years, need, route_b_names, default_of_mode, rb_label(sc, long=False)
           (source shipped as test/rates_view_new.py; patch copies it to Model/)
 8_2, 8_3  the duplicated _med _hl _pq _years _need _route_b_names _default_of_mode _rb_label are deleted and imported
           with underscore aliases, so no call site changes.
 Differences kept: tables label unset spread / cap "spread from [route_b]" / "cap from [income]" and "Sale (cash-equivalent units)"
 (rb_label long=True); charts keep "default spread" / "default cap" / "Sale".  8_3's _route_b_names now also prints the
 "route_b scenario not in rates_data.json" note that 8_2 already printed.

Numbers: neutral (tables and charts identical).  Check: rates_test.py (registries) and re-run 8_2 / 8_3, diff the output .md files.
"""
import os, re
from patchlib import Patch
P = Patch('W2-08', __doc__)
S = re.S | re.M
P.create('rates_view.py', open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'rates_view_new.py'), encoding='utf-8').read())

def drop(f, name):
    P.regex(f, r"^def %s\(.*?\n(?=^\S)" % name, "", count=1, flags=S)

IMPORT = ("from rates_view import (med as _med, hl as _hl, pq as _pq, years as _years, need as _need,\n"
          "                         route_b_names as _route_b_names, default_of_mode as _default_of_mode, rb_label as _rb_label_)\n")
T, C = '8_2_RATES_tables.py', '8_3_RATES_charts.py'
for f in (T, C):
    for n in ('_med', '_hl', '_pq', '_years', '_need', '_route_b_names', '_default_of_mode', '_rb_label'):
        drop(f, n)
P.replace(T, "from wdt_md import LEFT, RIGHT, MdDoc\n",
          "from wdt_md import LEFT, RIGHT, MdDoc\n" + IMPORT.replace(', rb_label as _rb_label_)', ')') +
          "from rates_view import rb_label as _rb_label_long\n_rb_label = lambda sc: _rb_label_long(sc, long=True)   # tables: say where an unset spread / cap comes from\n")
P.replace(C, "import wdt_core as wc\n", "import wdt_core as wc\n" + IMPORT.replace('rb_label as _rb_label_)', 'rb_label as _rb_label)'))
P.run()
