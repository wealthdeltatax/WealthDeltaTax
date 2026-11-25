"""hook_format: all 18 unit tags, rounding, ranges, placeholders (hooks.md 4.6)."""
import pytest
from conftest import load


@pytest.fixture(scope="module")
def hf():
    return load("hook_format")


CASES = [
    ("pct", 0.22, 2, "0.22%"), ("pct_per_year", 0.22, 2, "0.22% per year"), ("pct_gdp", 0.22, 2, "0.22% of GDP"),
    ("gbp_bn", 0.22, 2, "£0.22bn"), ("years", 0.22, 2, "0.22 years"), ("pp", 0.22, 2, "0.22 percentage points"),
    ("ratio", 0.22, 2, "0.22"), ("bp", 22, 0, "22 basis points"), ("count", 220000, 0, "220,000"),
    ("gbp_month", 22, 0, "£22 a month"), ("pp_per_year", 0.2, 1, "0.2 pp per year"), ("usd_bn", 12, 0, "US$12 bn"),
    ("gbp", 150000, 0, "£150,000"), ("gbp_m", 2, 0, "£2 m"), ("gbp_k", 150, 0, "£150 k"),
    ("coefficient", 0.5, 1, "0.5"), ("correlation", 0.5, 0, "0.50"),
]


@pytest.mark.parametrize("unit,value,dec,want", CASES)
def test_every_unit_tag(hf, unit, value, dec, want):
    assert hf.format_value(value, unit, dec) == want


def test_eighteen_tags_and_text_is_never_numeric(hf):
    assert len(hf.UNITS) == 18 and len(CASES) == 17
    with pytest.raises(hf.UnitError):
        hf.format_value(1, "text", 0)
    with pytest.raises(hf.UnitError):
        hf.format_value(1, "no_such_tag", 0)


def test_half_up_on_the_decimal_representation(hf):
    assert hf.format_value(0.125, "ratio", 2) == "0.13"
    assert hf.format_value(2.675, "ratio", 2) == "2.68"        # float repr would round down
    assert hf.format_value(-0.125, "ratio", 2) == "-0.13"


def test_negative_uses_hyphen_minus_and_no_negative_zero(hf):
    assert hf.format_value(-0.6, "pct", 1) == "-0.6%"
    assert hf.format_value(-0.001, "pct", 1) == "0.0%"


def test_range_unit_once_and_bands_rounded_separately(hf):
    assert hf.format_range(0.11, 0.33, "pct_per_year", 2) == ("0.11 to 0.33% per year", None)
    assert hf.format_range(0.11, 0.33, "gbp_bn", 2) == ("£0.11 to 0.33bn", None)
    assert hf.format_range(0.124, 0.125, "ratio", 2) == ("0.12 to 0.13", None)


def test_w2_equal_ends_render_once(hf):
    text, warn = hf.format_range(0.301, 0.304, "pct", 1)
    assert text == "0.3%" and warn.startswith("W2")


def test_placeholder_expansion(hf):
    assert hf.placeholder("O2", "mean", "S_central", "short") == "[[O2.mean@S_central/short]]"
    assert hf.placeholder("O2", "mean", "S_central", "short", {"wealth_band": "overall"}) == "[[O2.mean@S_central/short]]"
    assert hf.placeholder("O2", "p90", "S_low", "long", {"wealth_band": "D10"}) == "[[O2.p90@S_low/long#wealth_band:D10]]"
    assert hf.placeholder("O1", "mean", "S_central", "short", {}, "M1") == "[[O1:M1.mean@S_central/short]]"
    assert hf.placeholder("OP1", "mean", "S_central") == "[[OP1.mean@S_central]]"


def test_non_numbers_are_refused(hf):
    for bad in (None, "1", True):
        with pytest.raises(TypeError):
            hf.format_value(bad, "pct", 1)
