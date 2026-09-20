"""
wdt_ldw.py — WDT Labour Dividend Welfare Calculator
=====================================================
Models the purchasing power gain for a given salary under a mature WDT.

Two entry points
----------------
  ldw_calc(salary)          → dict of all computed values for one salary
  ldw_tables(out_path=None) → generates all tables used in LDW (§2.2, §4.4)
                              writes markdown if out_path given, else prints

Tax parameters (2025/26)
------------------------
  Income tax
    Personal allowance:        £12,570
    Basic rate (20%):          £12,571 – £50,270
    Higher rate (40%):         £50,271 – £125,140
    Additional rate (45%):     > £125,140

  Employee NICs
    Primary threshold:         £12,570
    Upper earnings limit:      £50,270
    Rate below UEL:            8%
    Rate above UEL:            2%

  Employer NICs
    Secondary threshold:       £5,000
    Rate:                      15%

Purchasing power assumptions (mature WDT, illustrative)
--------------------------------------------------------
  VAT displacement:           20% on 55% of post-tax spend (effective 11%)
  Energy bill reduction:      30% of £1,755 Ofgem Oct-2025 average = £527/yr

All assumption values are module-level constants; override before calling
ldw_calc() if you need to model different scenarios.
"""

from __future__ import annotations
from pathlib import Path
import sys
import os

# ── allow import of project helpers if available ──────────────────────────────
# wdt_fmt and wdt_md are optional; the script degrades gracefully without them.
try:
    from wdt_fmt import fmt_pct0, today_iso, out_dir, ensure_dir
    from wdt_md import MdDoc
    _HELPERS = True
except ImportError:
    _HELPERS = False

# Column alignment tokens — defined here so table functions work standalone
LEFT   = 'left'
RIGHT  = 'right'
CENTER = 'center'

# Canonical output directory for this module
# Resolves to .../OUTPUTS/LDW/ relative to the project root.
# wdt_fmt.out_dir() is used when available; falls back to path relative to
# this file so the script works standalone outside the project layout.
if _HELPERS:
    OUT_DIR = out_dir('LDW')
else:
    OUT_DIR = Path(__file__).parent / 'OUTPUTS' / 'LDW'


# ─────────────────────────────────────────────────────────────────────────────
# TAX PARAMETERS (2025/26)
# ─────────────────────────────────────────────────────────────────────────────

# Income tax
IT_PERSONAL_ALLOWANCE   = 12_570
IT_BASIC_LIMIT          = 50_270
IT_HIGHER_LIMIT         = 125_140
IT_BASIC_RATE           = 0.20
IT_HIGHER_RATE          = 0.40
IT_ADDITIONAL_RATE      = 0.45

# Employee NICs
EE_NIC_PRIMARY          = 12_570    # primary threshold
EE_NIC_UEL              = 50_270    # upper earnings limit
EE_NIC_RATE_MAIN        = 0.08      # below UEL
EE_NIC_RATE_UPPER       = 0.02      # above UEL

# Employer NICs
ER_NIC_SECONDARY        = 5_000     # secondary threshold
ER_NIC_RATE             = 0.15


# ─────────────────────────────────────────────────────────────────────────────
# PURCHASING POWER ASSUMPTIONS (mature WDT, illustrative)
# ─────────────────────────────────────────────────────────────────────────────

# VAT
VAT_RATE                = 0.20      # standard rate
VAT_SPEND_FRACTION      = 0.55      # share of post-tax spend that is VAT-able

# Energy
ENERGY_BASELINE         = 1_755     # Ofgem average annual bill, Oct 2025 (£)
ENERGY_REDUCTION        = 0.30      # illustrative SWF reduction


# ─────────────────────────────────────────────────────────────────────────────
# TAX CALCULATIONS
# ─────────────────────────────────────────────────────────────────────────────

def _income_tax(salary: float) -> float:
    """2025/26 income tax liability for a given gross salary."""
    tax = 0.0
    if salary <= IT_PERSONAL_ALLOWANCE:
        return 0.0
    taxable = salary - IT_PERSONAL_ALLOWANCE
    # Basic rate band
    basic_band = IT_BASIC_LIMIT - IT_PERSONAL_ALLOWANCE
    if taxable <= basic_band:
        return taxable * IT_BASIC_RATE
    tax += basic_band * IT_BASIC_RATE
    taxable -= basic_band
    # Higher rate band
    higher_band = IT_HIGHER_LIMIT - IT_BASIC_LIMIT
    if taxable <= higher_band:
        return tax + taxable * IT_HIGHER_RATE
    tax += higher_band * IT_HIGHER_RATE
    taxable -= higher_band
    # Additional rate
    tax += taxable * IT_ADDITIONAL_RATE
    return tax


def _employee_nics(salary: float) -> float:
    """2025/26 employee NICs liability for a given gross salary."""
    if salary <= EE_NIC_PRIMARY:
        return 0.0
    nics = 0.0
    # Main rate band (primary threshold to UEL)
    main_band_top = min(salary, EE_NIC_UEL)
    nics += (main_band_top - EE_NIC_PRIMARY) * EE_NIC_RATE_MAIN
    # Upper rate (above UEL)
    if salary > EE_NIC_UEL:
        nics += (salary - EE_NIC_UEL) * EE_NIC_RATE_UPPER
    return nics


def _employer_nics(salary: float) -> float:
    """2025/26 employer NICs liability for a given gross salary."""
    if salary <= ER_NIC_SECONDARY:
        return 0.0
    return (salary - ER_NIC_SECONDARY) * ER_NIC_RATE


# ─────────────────────────────────────────────────────────────────────────────
# PURCHASING POWER CALCULATIONS
# ─────────────────────────────────────────────────────────────────────────────

def _vat_gain(post_tax_income: float) -> float:
    """
    Annual VAT saving from full VAT displacement.

    VAT is embedded in VAT-able prices at rate r, so the current cost of
    VAT-able spending is inflated by (1 + r). Displacement removes that
    mark-up. The saving as a fraction of the current VAT-inclusive price is:
        r / (1 + r)
    applied to the VAT-able share of post-tax spend.
    """
    vat_able_spend = post_tax_income * VAT_SPEND_FRACTION
    # Current price includes VAT; saving is the embedded VAT fraction
    return vat_able_spend * (VAT_RATE / (1 + VAT_RATE))


def _energy_gain() -> float:
    """Annual energy bill saving from SWF-owned generation (illustrative)."""
    return ENERGY_BASELINE * ENERGY_REDUCTION


# ─────────────────────────────────────────────────────────────────────────────
# MAIN CALCULATION
# ─────────────────────────────────────────────────────────────────────────────

def ldw_calc(salary: float) -> dict:
    """
    Compute the full LDW purchasing power picture for a given gross salary.

    Parameters
    ----------
    salary : float   gross annual salary in £

    Returns
    -------
    dict with keys:

    -- Inputs --
    salary                  gross salary (echo of input)

    -- Current system --
    income_tax              current income tax liability
    employee_nics           current employee NICs liability
    employer_nics           current employer NICs cost
    take_home_current       current net take-home (salary - IT - EE NICs)
    total_employment_cost   current total cost to employer (salary + ER NICs)

    -- Post-WDT (payslip layer) --
    take_home_wdt           take-home under mature WDT (= gross salary)
    payslip_gain_annual     annual take-home gain (IT + EE NICs removed)
    payslip_gain_monthly    monthly take-home gain
    employer_saving_annual  annual employer cost saving (ER NICs removed)

    -- Post-WDT (purchasing power layer) --
    vat_gain_annual         annual VAT displacement saving (illustrative)
    vat_gain_monthly        monthly VAT displacement saving
    energy_gain_annual      annual energy bill saving (illustrative)
    energy_gain_monthly     monthly energy bill saving
    total_gain_annual       sum of all four channels
    total_gain_monthly      monthly equivalent of total_gain_annual
    purchasing_power_equiv  current take-home + total_gain_annual
                            (what the WDT take-home buys in today's £)

    -- Summary ratios --
    pp_increase_pct         purchasing power increase as a fraction
                            (purchasing_power_equiv / take_home_current) - 1
    payslip_increase_pct    payslip-only increase as a fraction
                            (take_home_wdt / take_home_current) - 1
    """
    it        = _income_tax(salary)
    ee_nics   = _employee_nics(salary)
    er_nics   = _employer_nics(salary)

    take_home_current     = salary - it - ee_nics
    take_home_wdt         = salary              # all labour taxes removed
    total_employment_cost = salary + er_nics

    payslip_gain_annual  = it + ee_nics         # what reappears on payslip
    payslip_gain_monthly = payslip_gain_annual / 12

    employer_saving_annual = er_nics

    vat_gain_ann  = _vat_gain(take_home_wdt)    # VAT on post-WDT income
    vat_gain_mon  = vat_gain_ann / 12
    energy_ann    = _energy_gain()
    energy_mon    = energy_ann / 12

    total_gain_annual  = payslip_gain_annual + vat_gain_ann + energy_ann
    total_gain_monthly = total_gain_annual / 12

    # Purchasing power equivalent: what the WDT take-home buys in today's £
    # = current take-home + all gains (payslip, VAT, energy)
    pp_equiv = take_home_current + total_gain_annual

    pp_increase_pct      = (pp_equiv / take_home_current) - 1
    payslip_increase_pct = (take_home_wdt / take_home_current) - 1

    return {
        # inputs
        'salary':                  salary,
        # current
        'income_tax':              it,
        'employee_nics':           ee_nics,
        'employer_nics':           er_nics,
        'take_home_current':       take_home_current,
        'total_employment_cost':   total_employment_cost,
        # post-WDT payslip
        'take_home_wdt':           take_home_wdt,
        'payslip_gain_annual':     payslip_gain_annual,
        'payslip_gain_monthly':    payslip_gain_monthly,
        'employer_saving_annual':  employer_saving_annual,
        # post-WDT purchasing power
        'vat_gain_annual':         vat_gain_ann,
        'vat_gain_monthly':        vat_gain_mon,
        'energy_gain_annual':      energy_ann,
        'energy_gain_monthly':     energy_mon,
        'total_gain_annual':       total_gain_annual,
        'total_gain_monthly':      total_gain_monthly,
        'purchasing_power_equiv':  pp_equiv,
        # summary ratios
        'pp_increase_pct':         pp_increase_pct,
        'payslip_increase_pct':    payslip_increase_pct,
    }


# ─────────────────────────────────────────────────────────────────────────────
# TABLE GENERATION  (LDW §2.2 and §4.4)
# ─────────────────────────────────────────────────────────────────────────────

# Salary points used in the paper
_PAPER_SALARIES = [25_000, 39_039, 50_000]
_PAPER_LABELS   = ['£25,000', '£39,039 (median)', '£50,000']


def _gbp(v: float) -> str:
    """Format as £N,NNN (no pence)."""
    return f'£{v:,.0f}'


def _gbp_approx(v: float) -> str:
    """Format as ~£N,NNN (for illustrative purchasing power figures)."""
    return f'~£{v:,.0f}'


def _pct(v: float) -> str:
    """Format as N% (integer)."""
    return f'{round(v * 100)}%'


def _mon(v: float) -> str:
    """Format as £NNN/month."""
    return f'£{v:,.0f}'


def table_222(results: list[dict]) -> str:
    """
    LDW §2.2 Table — payslip comparison across three salary points.

    Columns: Salary | Current take-home | Post-WDT take-home |
             Purchasing power equivalent | Monthly payslip gain
    """
    headers = [
        'Salary',
        'Current take-home',
        'Post-WDT take-home',
        'Purchasing power equivalent',
        'Monthly gain (payslip)',
    ]
    col_fmt = [LEFT, RIGHT, RIGHT, RIGHT, RIGHT]
    rows = []
    for label, r in zip(_PAPER_LABELS, results):
        rows.append([
            label,
            _gbp(r['take_home_current']),
            _gbp(r['take_home_wdt']),
            _gbp_approx(r['purchasing_power_equiv']),
            _mon(r['payslip_gain_monthly']),
        ])

    lines = ['| ' + ' | '.join(headers) + ' |']
    sep_map = {LEFT: ':---', RIGHT: '---:', CENTER: ':---:'}
    lines.append('|' + '|'.join(sep_map[a] for a in col_fmt) + '|')
    for row in rows:
        lines.append('| ' + ' | '.join(row) + ' |')
    return '\n'.join(lines)


def table_444(r: dict) -> str:
    """
    LDW §4.4 Table — full purchasing power gain for a single salary.

    Columns: Channel | Annual gain | Monthly gain | Basis
    """
    headers = ['Channel', 'Annual gain', 'Monthly gain', 'Basis']
    col_fmt = [LEFT, RIGHT, RIGHT, LEFT]

    rows = [
        ['Employee NICs removal',
         _gbp(r['employee_nics']),
         _gbp(r['payslip_gain_monthly'] - r['income_tax'] / 12),
         'Arithmetic — verified'],
        ['Income tax removal',
         _gbp(r['income_tax']),
         _gbp(r['income_tax'] / 12),
         'Full displacement scenario'],
        ['VAT displacement',
         _gbp(r['vat_gain_annual']),
         _gbp(r['vat_gain_monthly']),
         f'Illustrative — {round(VAT_SPEND_FRACTION * 100)}% VAT-able'],
        ['Energy bill reduction (SWF)',
         _gbp(r['energy_gain_annual']),
         _gbp(r['energy_gain_monthly']),
         f'Illustrative — {round(ENERGY_REDUCTION * 100)}% reduction'],
        ['**Total**',
         f'**{_gbp(r["total_gain_annual"])}**',
         f'**{_gbp(r["total_gain_monthly"])}**',
         ''],
        ['**Equivalent purchasing power**',
         f'**{_gbp(r["purchasing_power_equiv"])}**',
         '',
         ''],
    ]

    sep_map = {LEFT: ':---', RIGHT: '---:', CENTER: ':---:'}
    lines = ['| ' + ' | '.join(headers) + ' |']
    lines.append('|' + '|'.join(sep_map[a] for a in col_fmt) + '|')
    for row in rows:
        lines.append('| ' + ' | '.join(row) + ' |')
    return '\n'.join(lines)


def ldw_tables(out_path: str | Path | None = None) -> str:
    """
    Generate all tables used in the LDW paper and return as a markdown string.

    Parameters
    ----------
    out_path : str | Path | None
        Destination path for the markdown file.
        If None, defaults to .../OUTPUTS/LDW/ldw_tables.md (using wdt_fmt
        out_dir if available, else relative to this file's directory).
        Pass False to suppress writing entirely (return string only).

    Returns
    -------
    str   complete markdown output
    """
    results = [ldw_calc(s) for s in _PAPER_SALARIES]
    median  = results[1]   # £39,039

    lines = []
    A = lines.append

    A('# LDW Generated Tables')
    A('')
    if _HELPERS:
        A(f'*Generated: {today_iso()}*')
    A('')
    A('---')
    A('')

    # ── §2.2 ──────────────────────────────────────────────────────────────────
    A('## §2.2 — Payslip comparison')
    A('')
    A(table_222(results))
    A('')
    caption_222 = (
        '*2025/26 income tax and NICs rate schedules throughout. '
        'Post-WDT take-home assumes zero income tax and zero employee NICs. '
        f'Purchasing power equivalent adds VAT displacement '
        f'({round(VAT_SPEND_FRACTION * 100)}% VAT-able spend) '
        f'and energy bill reduction '
        f'({round(ENERGY_REDUCTION * 100)}% SWF infrastructure reduction '
        f'from £{ENERGY_BASELINE:,} baseline); see §4.4 for full methodology. '
        'Transport and communications infrastructure effects not included '
        'in purchasing power figure — directional only. '
        'Employer NICs displacement shown separately in §3.1.*'
    )
    A(caption_222)
    A('')
    A('---')
    A('')

    # ── §4.4 ──────────────────────────────────────────────────────────────────
    A(f'## §4.4 — Full purchasing power gain — median earner '
      f'({_gbp(median["salary"])})')
    A('')
    A(table_444(median))
    A('')
    A('---')
    A('')

    # ── Summary figures (for prose reference) ─────────────────────────────────
    A('## Summary figures (prose reference)')
    A('')
    for label, r in zip(_PAPER_LABELS, results):
        A(f'**{label}**')
        A(f'- Current take-home: {_gbp(r["take_home_current"])}')
        A(f'- Post-WDT take-home: {_gbp(r["take_home_wdt"])}')
        A(f'- Purchasing power equivalent: {_gbp(r["purchasing_power_equiv"])}')
        A(f'- Purchasing power increase: {_pct(r["pp_increase_pct"])}')
        A(f'- Payslip increase only: {_pct(r["payslip_increase_pct"])}')
        A(f'- Monthly payslip gain: {_gbp(r["payslip_gain_monthly"])}')
        A(f'- Monthly total gain: {_gbp(r["total_gain_monthly"])}')
        A(f'- Employer saving: {_gbp(r["employer_saving_annual"])}/yr')
        A(f'- Total employment cost: {_gbp(r["total_employment_cost"])} '
          f'→ {_gbp(r["salary"])} under WDT')
        A('')

    text = '\n'.join(lines)

    if out_path is not False:
        if out_path is None:
            # Default: OUTPUTS/LDW/ldw_tables.md alongside the project root
            if _HELPERS:
                dest = ensure_dir(out_dir('LDW')) / 'ldw_tables.md'
            else:
                dest = Path(__file__).parent / 'OUTPUTS' / 'LDW' / 'ldw_tables.md'
                dest.parent.mkdir(parents=True, exist_ok=True)
        else:
            dest = Path(out_path)
            dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_text(text, encoding='utf-8')
        print(f'Written: {dest}')

    return text


# ─────────────────────────────────────────────────────────────────────────────
# CLI
# ─────────────────────────────────────────────────────────────────────────────

def _print_calc(salary: float) -> None:
    r = ldw_calc(salary)
    print(f'\nWDT Labour Dividend — salary: {_gbp(r["salary"])}')
    print(f'  Current take-home:          {_gbp(r["take_home_current"])}')
    print(f'    Income tax:               {_gbp(r["income_tax"])}')
    print(f'    Employee NICs:            {_gbp(r["employee_nics"])}')
    print(f'  Post-WDT take-home:         {_gbp(r["take_home_wdt"])}')
    print(f'  Payslip gain:               {_gbp(r["payslip_gain_annual"])}/yr  '
          f'({_gbp(r["payslip_gain_monthly"])}/mo)')
    print(f'  VAT saving:                 {_gbp(r["vat_gain_annual"])}/yr')
    print(f'  Energy saving:              {_gbp(r["energy_gain_annual"])}/yr')
    print(f'  Purchasing power equiv:     {_gbp(r["purchasing_power_equiv"])}')
    print(f'  Purchasing power increase:  {_pct(r["pp_increase_pct"])}')
    print(f'  Employer saving:            {_gbp(r["employer_saving_annual"])}/yr')
    print()


if __name__ == '__main__':
    args = sys.argv[1:]

    if not args:
        # Default: show paper salary points, write tables to OUTPUTS/LDW/
        for s in _PAPER_SALARIES:
            _print_calc(s)
        ldw_tables()   # writes to default path, prints confirmation

    elif args[0] == '--tables':
        # --tables              → write to OUTPUTS/LDW/ldw_tables.md (default)
        # --tables path/out.md  → write to explicit path
        out = args[1] if len(args) > 1 else None
        ldw_tables(out_path=out)

    elif args[0] == '--print':
        # --print   → stdout only, no file written
        print(ldw_tables(out_path=False))

    else:
        # Treat argument as a salary; no file output
        try:
            salary = float(args[0].replace(',', '').replace('£', ''))
            _print_calc(salary)
        except ValueError:
            print('Usage: python wdt_ldw.py [salary | --tables [path] | --print]')
            sys.exit(1)
