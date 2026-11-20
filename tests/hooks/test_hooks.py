"""CK1 is hookable (brief 065g): one cell for each of its three metrics, formatted with the per-metric unit and decimals."""
import pytest

# fixture values at S_central, short, amplitude A5: P1 5.8, P3 2.2, P7b 3.7; units years, pct_gdp, ratio; decimals 1, 2, 2
@pytest.mark.parametrize("line, shown", [("P1", "5.8 years"), ("P3", "2.20% of GDP"), ("P7b", "3.70")])
def test_ck1_line_resolves_with_its_unit(run, fixture_doc, line, shown):
    cell = next(c for c in fixture_doc["outputs"]["CK1"]["cells"]
                if c["line"] == line and c["by"] == {"amplitude": "A5"} and c["schedule"] == "S_central")
    r = run("{{o:CK1:%s.point#amplitude:A5}}" % line, spoke="FALS")
    assert not r["errors"] and r["counts"]["resolved"] == 1
    assert r["text"].split("---\n")[-1].strip() == shown, cell
