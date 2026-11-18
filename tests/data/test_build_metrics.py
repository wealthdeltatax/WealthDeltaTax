"""build_metrics.py: the metric register becomes registry/metrics.json and is checked against outputs.yml."""

from __future__ import annotations

import json
import subprocess
import sys

import pytest

from conftest import MANIFEST, METRICS_JSON, METRICS_MD, PIPELINE

TABLE = (
    "## Headline metrics\n"
    "| ID | Name | Definition | Denominator | Unit | Horizon |\n|---|---|---|---|---|---|\n"
    "| M1 | Net effect | def | GDP | % of GDP and real £bn | transition, short and long |\n"
    "| M2 | Burden | def | wealth | % per year | one life, G years |\n"
    "| M3 | Child | def | wealth | % | as M1 |\n"
)


def manifest(**over):
    entry = {"id": "O1", "metric": "M1", "summary": "p10_mean_p90", "unit": "pct_gdp", "decimals": 2}
    entry.update(over)
    return {
        "version": "t", "country_pack": "UK", "horizons": ["transition", "short", "long"],
        "unit_tags": {"pct_gdp": "", "pct": "", "pct_per_year": "", "gbp_bn": ""},
        "outputs": [entry], "checks": [],
    }


def check(bm, mf, text=TABLE):
    metrics, _ = bm.parse_register(text)
    return bm.cross_check(metrics, mf)


def codes(findings, level=None):
    return [c for lv, c, _ in findings if level in (None, lv)]


def test_real_register_parses_and_resolves_ids(build_metrics):
    import yaml
    metrics, _ = build_metrics.parse_register(METRICS_MD.read_text(encoding="utf-8"))
    ids = [m["id"] for m in metrics]
    assert len(ids) == len(set(ids)) == 45
    mf = yaml.safe_load(MANIFEST.read_text(encoding="utf-8"))
    found = build_metrics.cross_check(metrics, mf)
    # ids, unit maps and declared tags agree with the manifest; unit text may not (reported by the script)
    assert not [c for c in codes(found, "error") if c in {"X01", "X04", "X07"}]
    assert not [c for c in codes(found) if c == "X01"]


def test_committed_json_matches_the_register(build_metrics):
    metrics, _ = build_metrics.parse_register(METRICS_MD.read_text(encoding="utf-8"))
    assert METRICS_JSON.read_text(encoding="utf-8") == build_metrics.render(metrics)


def test_m7_unescaped_pipe_is_rejoined_by_position(build_metrics):
    metrics, findings = build_metrics.parse_register(METRICS_MD.read_text(encoding="utf-8"))
    m7 = next(m for m in metrics if m["id"] == "M7")
    assert m7["unit_text"] == "percentage points" and m7["unit_tags"] == ["pp"]
    assert "X10" in codes(findings)


def test_row_shorter_than_header_fails(build_metrics):
    with pytest.raises(build_metrics.RegisterError, match="header has 6"):
        build_metrics.parse_register(TABLE + "| M9 | Short | def | x |\n")


def test_duplicate_id_fails(build_metrics):
    with pytest.raises(build_metrics.RegisterError, match="duplicate metric id M1"):
        build_metrics.parse_register(TABLE + "| M1 | Again | d | x | % | short |\n")


def test_unit_tags_and_horizons(build_metrics):
    metrics, _ = build_metrics.parse_register(TABLE)
    m1, m2, m3 = metrics
    assert m1["unit_tags"] == ["pct_gdp", "gbp_bn"]
    assert m1["horizons"] == ["transition", "short", "long"]
    assert m2["unit_tags"] == ["pct_per_year"] and m2["horizons"] == ["single"]
    assert m3["horizons"] == ["transition", "short", "long"] and m3["horizon_same_as"] == "M1"


def test_agreeing_manifest_has_no_errors(build_metrics):
    assert codes(check(build_metrics, manifest()), "error") == []


def test_unknown_metric_is_an_error(build_metrics):
    assert "X01" in codes(check(build_metrics, manifest(metric="M99")), "error")


def test_unit_disagreement_is_an_error(build_metrics):
    f = check(build_metrics, manifest(metric="M2", unit="pct"))
    assert codes(f, "error") == ["X05"]


def test_unit_that_is_one_of_several_forms_agrees(build_metrics):
    assert codes(check(build_metrics, manifest(unit="gbp_bn")), "error") == []


def test_undeclared_unit_tag_is_an_error(build_metrics):
    assert "X04" in codes(check(build_metrics, manifest(unit="furlongs")), "error")


def test_unit_map_must_match_lines(build_metrics):
    f = check(build_metrics, manifest(lines=["M1", "M2"], unit={"M1": "pct_gdp"}))
    assert "X07" in codes(f, "error")


def test_unit_not_stated_in_register_is_only_a_warning(build_metrics):
    text = TABLE.replace("% per year", "")
    f = check(build_metrics, manifest(metric="M2", unit="pct"), text)
    assert codes(f, "error") == [] and "X06" in codes(f, "warning")


def test_family_head_and_line_without_id(build_metrics):
    text = TABLE + "| M1a | Part | d | x | % of GDP | short |\n"
    f = check(build_metrics, manifest(metric="M1", lines=["M1a", "M1z"], unit="pct_gdp"), text)
    assert codes(f, "error") == [] and "X03" in codes(f, "warning")
    f = check(build_metrics, manifest(metric="M1", unit="pct_gdp"), text)
    assert "X03" not in codes(f)


def test_horizon_outside_the_register_is_a_warning(build_metrics):
    f = check(build_metrics, manifest(metric="M2", unit="pct_per_year"))   # M2 is one life
    assert "X08" in codes(f, "warning")
    f = check(build_metrics, manifest(metric="M2", unit="pct_per_year", horizons=["single"]))
    assert "X08" not in codes(f)


def test_two_runs_are_byte_identical_under_isolated_python(tmp_path):
    outs = []
    for i in range(2):
        out = tmp_path / f"metrics{i}.json"
        subprocess.run(
            [sys.executable, "-I", str(PIPELINE / "build_metrics.py"), "--out", str(out)],
            capture_output=True, cwd=tmp_path,   # exit 1 is allowed: the file is written either way
        )
        outs.append(out.read_bytes())
    assert outs[0] == outs[1] == METRICS_JSON.read_bytes()
