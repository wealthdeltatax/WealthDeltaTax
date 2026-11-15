"""
test_wdt_fmt.py — Tests for wdt_fmt.py
=======================================
Each test group verifies:
  1. Normal inputs produce the expected string
  2. None inputs return "—" (where applicable)
  3. The new function is a drop-in for its predecessor by comparing
     outputs on a shared set of values

Run with:
    python test_wdt_fmt.py
"""

import sys
import traceback
from pathlib import Path

# ---------------------------------------------------------------------------
# Test runner (no external dependencies)
# ---------------------------------------------------------------------------

_PASS = 0
_FAIL = 0


def check(label: str, got, expected):
    global _PASS, _FAIL
    if got == expected:
        _PASS += 1
    else:
        _FAIL += 1
        print(f"  FAIL  {label}")
        print(f"        got:      {got!r}")
        print(f"        expected: {expected!r}")


def section(title: str):
    print(f"\n{'─' * 60}")
    print(f"  {title}")
    print(f"{'─' * 60}")


# ---------------------------------------------------------------------------
# Import the module under test
# ---------------------------------------------------------------------------

sys.path.insert(0, str(Path(__file__).parent))
import wdt_fmt as F


# ---------------------------------------------------------------------------
# 1. fmt_pct
# ---------------------------------------------------------------------------

section("fmt_pct — percentage formatting")

check("default 2dp",          F.fmt_pct(0.1234),       "12.34%")
check("dp=1",                  F.fmt_pct(0.1234, dp=1), "12.3%")
check("dp=0",                  F.fmt_pct(0.1234, dp=0), "12%")
check("zero",                  F.fmt_pct(0.0),          "0.00%")
check("negative",              F.fmt_pct(-0.045),       "-4.50%")
check("exactly 1.0",          F.fmt_pct(1.0),           "100.00%")
check("None → em-dash",        F.fmt_pct(None),          "—")
check("dp=3",                  F.fmt_pct(0.10453, dp=3), "10.453%")

# Confirm drop-in for val_helpers.pct_str (default dp=2)
# pct_str(v, decimals=2) == fmt_pct(v, dp=2)
for v in [0.0, 0.05, 0.1045, 0.15, 0.70, -0.0455, 0.254]:
    check(f"pct_str compat v={v}",
          F.fmt_pct(v, dp=2),
          f'{v * 100:.2f}%')

# Confirm drop-in for val_helpers.fp (fraction → pct, default dp=2)
# fp(v, dp=2) == fmt_pct(v, dp=2)
for v in [0.15, 0.09, 0.70]:
    check(f"fp compat v={v}",
          F.fmt_pct(v, dp=2),
          f'{v * 100:.2f}%')


section("fmt_pct1 / fmt_pct0 shorthands")

check("fmt_pct1 normal",  F.fmt_pct1(0.1045), "10.4%")   # 10.45 → 10.4 (banker's rounding)
check("fmt_pct1 None",    F.fmt_pct1(None),   "—")
check("fmt_pct0 normal",  F.fmt_pct0(0.1045), "10%")
check("fmt_pct0 None",    F.fmt_pct0(None),   "—")

# Confirm drop-in for rates_s_helpers.fmt_pct (default dp=1)
for v in [0.05, 0.10, 0.15, 0.20, 0.70]:
    check(f"rates_s_helpers.fmt_pct compat v={v}",
          F.fmt_pct1(v),
          f'{v * 100:.1f}%')


# ---------------------------------------------------------------------------
# 2. fmt_gbp_m
# ---------------------------------------------------------------------------

section("fmt_gbp_m — £m currency formatting")

check("3dp default",    F.fmt_gbp_m(12.345),       "£12.345m")
check("2dp",            F.fmt_gbp_m(12.345, dp=2), "£12.35m")
check("0dp",            F.fmt_gbp_m(12.345, dp=0), "£12m")
check("negative",       F.fmt_gbp_m(-5.123),       "£-5.123m")
check("zero",           F.fmt_gbp_m(0.0),           "£0.000m")
check("None → em-dash", F.fmt_gbp_m(None),          "—")

# Confirm drop-in for val_helpers.fm (default dp=3)
# fm(v, dp=3) == fmt_gbp_m(v, dp=3)
for v in [20.0, 8.547, 0.401789, -1.23]:
    check(f"fm compat v={v}",
          F.fmt_gbp_m(v, dp=3),
          f'£{v:.3f}m')


# ---------------------------------------------------------------------------
# 3. fmt_gbp_b
# ---------------------------------------------------------------------------

section("fmt_gbp_b — £b currency formatting")

check("1dp default",    F.fmt_gbp_b(1157.4),       "£1157.4b")
check("0dp",            F.fmt_gbp_b(1157.4, dp=0), "£1157b")
check("None → em-dash", F.fmt_gbp_b(None),          "—")
check("small value",    F.fmt_gbp_b(28.0),          "£28.0b")


# ---------------------------------------------------------------------------
# 4. fmt_gbp_yr
# ---------------------------------------------------------------------------

section("fmt_gbp_yr — £/yr with near-zero suppression")

check("above threshold",    F.fmt_gbp_yr(12345.0),          "£12,345")
check("exact threshold",    F.fmt_gbp_yr(0.5),              "£0")   # not suppressed (abs(0.5) < 0.5 is False), banker's rounds 0.5→0
check("below threshold",    F.fmt_gbp_yr(0.49),             "£—")
check("zero",               F.fmt_gbp_yr(0.0),              "£—")
check("negative below",     F.fmt_gbp_yr(-0.4),             "£—")
check("negative above",     F.fmt_gbp_yr(-1000.0),          "£-1,000")
check("custom threshold",   F.fmt_gbp_yr(100.0, threshold=200.0), "£—")

# Confirm drop-in for 8_3._fmt_gbp
def _old_fmt_gbp(v, threshold=0.5):
    return '£—' if abs(v) < threshold else f'£{v:,.0f}'

for v in [0.0, 0.3, 0.5, 1.0, 100.0, 12345.67, -500.0]:
    check(f"_fmt_gbp compat v={v}",
          F.fmt_gbp_yr(v),
          _old_fmt_gbp(v))


# ---------------------------------------------------------------------------
# 5. fmt_rev_m
# ---------------------------------------------------------------------------

section("fmt_rev_m — £m/yr revenue with near-zero suppression")

check("above threshold",  F.fmt_rev_m(1234.0),              "£1,234m")
check("below threshold",  F.fmt_rev_m(0.0004),              "£—")
check("zero",             F.fmt_rev_m(0.0),                 "£—")
check("custom threshold", F.fmt_rev_m(1.0, threshold=2.0),  "£—")

# Confirm drop-in for 8_3._fmt_m
def _old_fmt_m(v, threshold=0.0005):
    return '£—' if abs(v) < threshold else f'£{v:,.0f}m'

for v in [0.0, 0.0004, 0.001, 1.5, 100.0]:
    check(f"_fmt_m compat v={v}",
          F.fmt_rev_m(v),
          _old_fmt_m(v))


# ---------------------------------------------------------------------------
# 6. fmt_f and shorthands
# ---------------------------------------------------------------------------

section("fmt_f — generic float formatting")

check("default .1f",     F.fmt_f(12.345),          "12.3")
check(".2f",             F.fmt_f(12.345, '.2f'),   "12.35")
check(".0f",             F.fmt_f(12.6, '.0f'),     "13")
check(".0f integer",     F.fmt_f(34.0, '.0f'),     "34")
check("None → em-dash",  F.fmt_f(None),             "—")
check("negative",        F.fmt_f(-3.7),             "-3.7")

check("fmt_f0 normal",   F.fmt_f0(29.0),            "29")
check("fmt_f0 None",     F.fmt_f0(None),            "—")
check("fmt_f2 normal",   F.fmt_f2(3.14159),         "3.14")
check("fmt_f2 None",     F.fmt_f2(None),            "—")
check("fmt_f4 normal",   F.fmt_f4(0.9876),          "0.9876")
check("fmt_f4 None",     F.fmt_f4(None),            "—")

# Confirm drop-in for rates_s_helpers.fmt_f
def _old_fmt_f(v, fmt='.1f'):
    if v is None:
        return '—'
    return f'{v:{fmt}}'

for v, spec in [(3.14, '.1f'), (29.0, '.0f'), (None, '.1f'), (0.9876, '.4f')]:
    check(f"fmt_f compat v={v} spec={spec}",
          F.fmt_f(v, spec),
          _old_fmt_f(v, spec))


# ---------------------------------------------------------------------------
# 7. eff_rate
# ---------------------------------------------------------------------------

section("eff_rate — effective lifetime tax rate")

check("normal",       F.eff_rate({'Net_settled': 5.0,  'TW_settled': 100.0}), 0.05)
check("negative net", F.eff_rate({'Net_settled': -2.0, 'TW_settled': 50.0}), -0.04)
check("TW zero",      F.eff_rate({'Net_settled': 5.0,  'TW_settled': 0.0}),  0.0)
check("TW tiny",      F.eff_rate({'Net_settled': 5.0,  'TW_settled': 1e-13}), 0.0)
check("exact match",  F.eff_rate({'Net_settled': 3.0,  'TW_settled': 20.0}), 0.15)


# ---------------------------------------------------------------------------
# 8. dist_row
# ---------------------------------------------------------------------------

section("dist_row — distribution summary string")

d = {'min': 0.05, 'median': 0.10, 'mean': 0.11, 'max': 0.20}
check("fmt_pct1",
      F.dist_row(d, F.fmt_pct1),
      "5.0% / 10.0% / 11.0% / 20.0%")

check("fmt_pct",
      F.dist_row(d, F.fmt_pct),
      "5.00% / 10.00% / 11.00% / 20.00%")

d_none = {'min': None, 'median': 29.0, 'mean': 31.0, 'max': 45.0}
check("None in dict",
      F.dist_row(d_none, F.fmt_f0),
      "— / 29 / 31 / 45")

# Confirm drop-in for rates_s_helpers.dist_row
def _old_dist_row(d, fmt_fn):
    return (f"{fmt_fn(d['min'])} / {fmt_fn(d['median'])} / "
            f"{fmt_fn(d['mean'])} / {fmt_fn(d['max'])}")

for d_test, fn in [
    ({'min': 0.05, 'median': 0.10, 'mean': 0.11, 'max': 0.20}, F.fmt_pct1),
    ({'min': 29.0, 'median': 34.0, 'mean': 35.5, 'max': 50.0}, F.fmt_f0),
]:
    check(f"dist_row compat fn={fn.__name__}",
          F.dist_row(d_test, fn),
          _old_dist_row(d_test, fn))


# ---------------------------------------------------------------------------
# 9. baseline_marker
# ---------------------------------------------------------------------------

section("baseline_marker — sweep table baseline indicator")

check("exact match",        F.baseline_marker(0.15, 0.15),           " ◄")
check("within tol",         F.baseline_marker(0.15, 0.15 + 1e-10),   " ◄")
check("outside tol",        F.baseline_marker(0.15, 0.20),           "")
check("zero baseline",      F.baseline_marker(0.0, 0.0),             " ◄")
check("custom tol match",   F.baseline_marker(1.0, 1.001, tol=0.01), " ◄")
check("custom tol miss",    F.baseline_marker(1.0, 1.02,  tol=0.01), "")

# Confirm identical to rates_s_helpers.baseline_marker
def _old_baseline_marker(v, baseline_v, tol=1e-9):
    return ' ◄' if abs(v - baseline_v) < tol else ''

for v, bv in [(0.001, 0.001), (0.15, 0.20), (0.001, 0.001 + 5e-10)]:
    check(f"baseline_marker compat v={v} bv={bv}",
          F.baseline_marker(v, bv),
          _old_baseline_marker(v, bv))


# ---------------------------------------------------------------------------
# 10. today_iso
# ---------------------------------------------------------------------------

section("today_iso — date string")

import datetime
result = F.today_iso()
check("returns string",  isinstance(result, str), True)
check("correct format",  result, datetime.date.today().isoformat())
check("length",          len(result), 10)


# ---------------------------------------------------------------------------
# 11. out_dir / ensure_dir
# ---------------------------------------------------------------------------

section("out_dir / ensure_dir — path helpers")

import tempfile, os

val_path = F.out_dir('VAL')
check("VAL subdir type",   isinstance(val_path, Path), True)
check("VAL ends with VAL", val_path.name,               'VAL')
check("parent is OUTPUTS", val_path.parent.name,         'OUTPUTS')

# Test ensure_dir creates the directory
with tempfile.TemporaryDirectory() as tmp:
    test_path = Path(tmp) / 'TEST' / 'SUBDIR'
    returned  = F.ensure_dir(test_path)
    check("ensure_dir creates dir",  test_path.exists(),  True)
    check("ensure_dir returns path", returned,            test_path)


# ---------------------------------------------------------------------------
# Summary
# ---------------------------------------------------------------------------

print(f"\n{'═' * 60}")
print(f"  Results: {_PASS} passed, {_FAIL} failed")
print(f"{'═' * 60}")

if _FAIL > 0:
    sys.exit(1)
