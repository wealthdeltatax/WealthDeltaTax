"""Number formatting and placeholders for data hooks (hooks.md 4.6; brief 060c). Pure functions, no I/O."""
from decimal import Decimal, ROUND_HALF_UP

# unit tag -> (prefix, suffix, group thousands, forced decimals or None). The ten manifest tags (outputs.yml
# unit_tags) and the eight input-only tags of the 032r ruling; `text` is deliberately absent (never numeric).
UNITS = {
    "pct": ("", "%", False, None),
    "pct_per_year": ("", "% per year", False, None),
    "pct_gdp": ("", "% of GDP", False, None),
    "gbp_bn": ("£", "bn", True, None),
    "years": ("", " years", False, None),
    "pp": ("", " percentage points", False, None),
    "ratio": ("", "", False, None),
    "bp": ("", " basis points", True, None),
    "count": ("", "", True, None),
    "gbp_month": ("£", " a month", True, None),
    "pp_per_year": ("", " pp per year", False, None),
    "usd_bn": ("US$", " bn", True, None),
    "gbp": ("£", "", True, None),
    "gbp_m": ("£", " m", True, None),
    "gbp_k": ("£", " k", True, None),
    "coefficient": ("", "", False, None),
    "correlation": ("", "", False, 2),
    "text": None,
}
NON_NUMERIC = {"text"}


class UnitError(ValueError):
    """The unit tag is not one of the formatted tags (one error for every unknown tag)."""


def _spec(unit):
    if unit not in UNITS or UNITS[unit] is None:
        raise UnitError(f"unit tag {unit!r} cannot be formatted as a number")
    return UNITS[unit]


def _number(value, decimals, group, forced):
    """Decimal half-up on the decimal representation of the stored number (0.125 at 2 -> 0.13)."""
    d = forced if forced is not None else int(decimals)
    q = Decimal(str(value)).quantize(Decimal(1).scaleb(-d), rounding=ROUND_HALF_UP)
    if q == 0:
        q = abs(q)                                   # no "-0.0"
    s = f"{q:,.{d}f}" if group else f"{q:.{d}f}"
    return s                                         # a negative keeps the hyphen-minus


def format_value(value, unit, decimals):
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise TypeError(f"not a number: {value!r}")
    pre, suf, group, forced = _spec(unit)
    return f"{pre}{_number(value, decimals, group, forced)}{suf}"


def format_range(lo, hi, unit, decimals):
    """Return (text, warning). Ends that round to the same string render once with warning W2."""
    pre, suf, group, forced = _spec(unit)
    for v in (lo, hi):
        if isinstance(v, bool) or not isinstance(v, (int, float)):
            raise TypeError(f"not a number: {v!r}")
    a, b = _number(lo, decimals, group, forced), _number(hi, decimals, group, forced)
    if a == b:
        return f"{pre}{a}{suf}", "W2: range ends round to the same value, shown once"
    return f"{pre}{a} to {b}{suf}", None


def placeholder(oid, stat, schedule=None, horizon=None, by=(), line=None):
    """[[ID.STAT@SCHEDULE/HORIZON]] with defaults applied; #KEY:VALUE only for keys not `overall`."""
    s = f"[[{oid}" + (f":{line}" if line else "") + f".{stat}"
    if schedule:
        s += f"@{schedule}"
    if horizon:
        s += f"/{horizon}"
    pairs = [f"{k}:{v}" for k, v in sorted(dict(by).items()) if str(v) != "overall"]
    if pairs:
        s += "#" + ",".join(pairs)
    return s + "]]"
