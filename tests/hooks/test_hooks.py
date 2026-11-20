"""CK1 is hookable (brief 065g): one cell for each of its three metrics, formatted with the per-metric unit and decimals."""
import pytest

# fixture values at S_central, short, amplitude A5: P1 2.8, P3 4.3, P7b 5.8; units years, pct_gdp, ratio; decimals 1, 2, 2
@pytest.mark.parametrize("line, shown", [("P1", "2.8 years"), ("P3", "4.30% of GDP"), ("P7b", "5.80")])
def test_ck1_line_resolves_with_its_unit(run, fixture_doc, line, shown):
    cell = next(c for c in fixture_doc["outputs"]["CK1"]["cells"]
                if c["line"] == line and c["by"] == {"amplitude": "A5"} and c["schedule"] == "S_central")
    r = run("{{o:CK1:%s.point#amplitude:A5}}" % line, spoke="FALS")
    assert not r["errors"] and r["counts"]["resolved"] == 1
    assert r["text"].split("---\n")[-1].strip() == shown, cell
