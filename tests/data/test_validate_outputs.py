"""validate_outputs.py: rules V1 to V12 on the fixture and on mutations of it (brief 030c)."""

from __future__ import annotations

import copy
import json
import math
import subprocess
import sys

import pytest

from conftest import FIXTURE, INPUTS_JSON, MANIFEST, PIPELINE

SCRIPT = str(PIPELINE / "validate_outputs.py")


@pytest.fixture()
def run(vo, manifest):
    def _run(doc, mode="default", inputs_path=INPUTS_JSON):
        return vo.validate(doc, manifest, MANIFEST, inputs_path, mode)
    return _run


def hits(findings, rule, level=None):
    return [f for f in findings if f.rule == rule and (level is None or f.level == level)]


def errors(findings):
    return [f for f in findings if f.level == "error"]


def cell(doc, oid, **match):
    """First cell of output oid whose fields equal match."""
    for c in doc["outputs"][oid]["cells"]:
        if all(c.get(k) == v for k, v in match.items()):
            return c
    raise LookupError(oid, match)


# ── the fixture ──────────────────────────────────────────────────────────────

def test_fixture_covers_every_manifest_entry(fixture_doc, manifest):
    ids = {e["id"] for e in manifest["outputs"]} | {e["id"] for e in manifest["checks"]}
    assert set(fixture_doc["outputs"]) == ids
    assert fixture_doc["run"]["fixture"] is True


def test_fixture_is_current(make_fixture):
    """Fails when outputs.yml or inputs.json changed: run python tests/data/make_fixture.py."""
    assert FIXTURE.read_text(encoding="utf-8") == make_fixture.render(make_fixture.build())


def test_fixture_passes_in_fixture_mode_without_findings(run, fixture_doc):
    assert run(fixture_doc, "fixture") == []


def test_fixture_fails_in_final_mode(run, fixture_doc):
    f = run(fixture_doc, "final")
    assert {x.where for x in errors(f)} == {"run.status", "run.fixture"}


def test_fixture_in_default_mode_only_warns(run, fixture_doc):
    f = run(fixture_doc)
    assert errors(f) == [] and [x.where for x in f] == ["run.fixture"]


def test_cli_exit_codes_and_every_rule_is_reported():
    base = [sys.executable, "-I", SCRIPT, str(FIXTURE)]
    ok = subprocess.run(base + ["--fixture"], capture_output=True, text=True)
    assert ok.returncode == 0 and "result: PASS" in ok.stdout
    for n in range(1, 13):
        assert f"  V{n} " in ok.stdout or f"  V{n:<2}" in ok.stdout
    bad = subprocess.run(base + ["--final"], capture_output=True, text=True)
    assert bad.returncode == 1 and "result: FAIL" in bad.stdout
    assert subprocess.run(base + ["--final", "--fixture"], capture_output=True).returncode == 2
    gone = subprocess.run([sys.executable, "-I", SCRIPT, str(FIXTURE) + ".missing"], capture_output=True)
    assert gone.returncode == 2


def test_manifest_notes_name_the_known_findings(vo, manifest):
    notes = {n.rule: n.message for n in vo.manifest_notes(manifest)}
    for oid in ("DH1a", "CK1", "OH1b2"):
        assert oid in notes["M1"]
    # brief 045g (V3-0) gave the six list-valued `by` entries and CK1 a vocabulary map, so the M2 note must be gone
    assert "M2" not in notes


# ── V1, V2 ───────────────────────────────────────────────────────────────────

def test_v1_schema(run, doc):
    doc["schema"] = "wdt-outputs/2"
    assert hits(run(doc, "fixture"), "V1", "error")


def test_v2_unknown_output_and_summary_mismatch(run, doc):
    doc["outputs"]["ZZ9"] = {"summary": "p10_mean_p90", "cells": []}
    doc["outputs"]["O2"]["summary"] = "point_and_range"
    f = hits(run(doc, "fixture"), "V2", "error")
    assert {x.where for x in f} == {"ZZ9", "O2"}


# ── V3, V4 ───────────────────────────────────────────────────────────────────

@pytest.mark.parametrize("mutate", [
    lambda d: cell(d, "O2").__setitem__("schedule", "S_extreme"),
    lambda d: cell(d, "O2").__setitem__("horizon", "single"),
    lambda d: cell(d, "O2")["by"].__setitem__("wealth_band", "D1"),
    lambda d: cell(d, "O2")["by"].__setitem__("extra", "x"),
    lambda d: cell(d, "O2").pop("by"),
    lambda d: cell(d, "O3").__setitem__("line", "M3"),              # O3 declares no lines
    lambda d: cell(d, "OB1").__setitem__("line", "B9"),
    lambda d: cell(d, "OH1b").__setitem__("schedule", "S_central"),  # reported once, not per schedule
    lambda d: d["outputs"]["O2"]["cells"].__setitem__(0, "not a cell"),
])
def test_v3_dimension_errors(run, doc, mutate):
    mutate(doc)
    assert hits(run(doc, "fixture"), "V3", "error")


def test_v3_line_required_when_declared(run, doc):
    cell(doc, "OB1").pop("line")
    assert hits(run(doc, "fixture"), "V3", "error")


def test_v3_level2_input_must_be_a_register_id(run, doc):
    doc["level2"] = {"O2": {"p10": 1.0, "p90": 2.0, "tornado": [
        {"input": "I-D4a", "low_effect": -1.0, "high_effect": 1.5},
        {"input": "I-NOPE", "low_effect": -0.5, "high_effect": 0.5},
    ]}}
    f = hits(run(doc, "fixture"), "V3", "error")
    assert len(f) == 1 and "I-NOPE" in f[0].message


def test_v4_duplicate_cell(run, doc):
    cells = doc["outputs"]["O2"]["cells"]
    cells.append(dict(cells[0]))
    assert hits(run(doc, "fixture"), "V4", "error")


# ── V5, V6 ───────────────────────────────────────────────────────────────────

def test_v5_null_is_allowed_only_when_provisional(run, doc):
    cell(doc, "O2")["mean"] = None
    assert not hits(run(doc, "fixture"), "V5")
    assert hits(run(doc, "final"), "V5", "error")
    doc["run"]["status"] = "final"
    assert hits(run(doc), "V5", "error")


@pytest.mark.parametrize("bad", ["0.2", True, math.nan, math.inf])
def test_v5_not_a_finite_number(run, doc, bad):
    cell(doc, "O2")["p10"] = bad
    assert hits(run(doc, "fixture"), "V5", "error")


def test_v5_missing_field(run, doc):
    cell(doc, "O7").pop("lo")
    assert hits(run(doc, "fixture"), "V5", "error")


def test_v6_ordering(run, doc):
    c = cell(doc, "O2")
    c["p10"], c["p90"] = 5.0, 1.0
    assert hits(run(doc, "fixture"), "V6", "error")
    c["p10"], c["mean"], c["p90"] = 1.0, 9.0, 2.0
    f = run(doc, "fixture")
    assert hits(f, "V6", "warning") and not hits(f, "V6", "error")
    c = cell(doc, "O7")
    c["lo"], c["hi"] = 3.0, 1.0
    assert hits(run(doc, "fixture"), "V6", "error")
    c["lo"], c["point"], c["hi"] = 1.0, 9.0, 2.0
    assert hits(run(doc, "fixture"), "V6", "warning")


def test_v6_tornado_order_and_range(run, doc):
    doc["level2"] = {"O2": {"p10": 2.0, "p90": 1.0, "tornado": [
        {"input": "I-D4a", "low_effect": -0.1, "high_effect": 0.2},
        {"input": "I-D4b", "low_effect": -1.0, "high_effect": 0.5},
    ]}}
    f = hits(run(doc, "fixture"), "V6", "error")
    assert len(f) == 2


# ── V7, V9, V11: errors in final mode, warnings in a provisional file ────────

def drop_cell(doc):
    doc["outputs"]["O2"]["cells"].pop(0)


def drop_output(doc):
    del doc["outputs"]["O2"]


def stale_inputs_hash(doc):
    doc["run"]["inputs_sha256"] = "0" * 64


def drop_year(doc):
    doc["outputs"]["OP6"]["cells"] = [c for c in doc["outputs"]["OP6"]["cells"] if c["by"]["year"] != "25"]


@pytest.mark.parametrize("rule,mutate", [
    ("V7", drop_cell), ("V7", drop_output), ("V9", stale_inputs_hash), ("V11", drop_year),
])
def test_strict_rules_by_mode(run, doc, rule, mutate):
    mutate(doc)
    assert hits(run(doc, "default"), rule, "warning") and not hits(run(doc, "default"), rule, "error")
    assert hits(run(doc, "final"), rule, "error")
    doc["run"]["status"] = "final"
    assert hits(run(doc, "default"), rule, "error")


def test_v7_names_the_missing_cell(run, doc):
    drop_cell(doc)
    msg = hits(run(doc), "V7")[0].message
    assert "1 cell(s) missing" in msg and "S_" in msg


def test_v7_a_once_output_needs_no_schedule_product(run, doc):
    assert all("schedule" not in c for c in doc["outputs"]["OH1c"]["cells"])
    assert not hits(run(doc, "fixture"), "V7")


def test_v9_unreadable_inputs_file(run, doc, tmp_path):
    f = run(doc, "final", tmp_path / "missing.json")
    assert hits(f, "V9", "error") and "cannot read" in hits(f, "V9")[0].message


# ── V8 ───────────────────────────────────────────────────────────────────────

@pytest.mark.parametrize("field,value", [
    ("manifest_version", "other"), ("manifest_sha256", "0" * 64),
])
def test_v8_stale_manifest_is_error_but_a_stale_fixture_only_warns(run, doc, field, value):
    doc["run"][field] = value
    assert hits(run(doc, "default"), "V8", "error")
    assert hits(run(doc, "fixture"), "V8", "warning") and not hits(run(doc, "fixture"), "V8", "error")


@pytest.mark.parametrize("field,value", [
    ("country_pack", "FR"), ("status", "draft"), ("run_date", "17/11/2026"), ("paths", -1), ("base_year", "2025"),
])
def test_v8_run_field_errors(run, doc, field, value):
    doc["run"][field] = value
    assert hits(run(doc, "fixture"), "V8", "error")


def test_v8_missing_run_field_and_missing_run(run, doc):
    del doc["run"]["model_version"]
    assert hits(run(doc, "fixture"), "V8", "error")
    del doc["run"]
    assert hits(run(doc, "fixture"), "V8", "error")


def test_v8_fixture_flag(run, doc):
    doc["run"]["fixture"] = False
    assert hits(run(doc, "fixture"), "V8", "error")


# ── V10 ──────────────────────────────────────────────────────────────────────

def test_v10_series_rules(run, doc):
    c = cell(doc, "OP6", horizon="single", schedule="S_central", by={"year": "10"})
    series = c["series"]
    assert not hits(run(doc, "fixture"), "V10")
    c["series"] = series[1:]                      # starts at t = 2
    assert hits(run(doc, "fixture"), "V10", "error")
    c["series"] = [series[0], series[2], series[1]] + series[3:]   # t not increasing
    assert hits(run(doc, "fixture"), "V10", "error")
    c["series"] = series[:5]                      # year 10 not reached
    assert any("year" in x.message for x in hits(run(doc, "fixture"), "V10", "error"))
    c["series"] = []
    assert hits(run(doc, "fixture"), "V10", "error")


def test_v10_missing_series_is_strict(run, doc):
    cell(doc, "OP6").pop("series")
    assert hits(run(doc, "default"), "V10", "warning")
    assert hits(run(doc, "final"), "V10", "error")


def test_v10_series_points_are_checked_as_numbers(run, doc):
    cell(doc, "OP6")["series"][3]["mean"] = "x"
    assert hits(run(doc, "fixture"), "V5", "error")


# ── V12 ──────────────────────────────────────────────────────────────────────

def test_v12_unknown_fields_warn_only(run, doc):
    doc["extra"] = 1
    doc["run"]["note"] = "x"
    doc["outputs"]["O2"]["note"] = "x"
    cell(doc, "O2")["diagnostic"] = 1
    cell(doc, "O3")["series"] = [{"t": 1, "p10": 1.0, "mean": 2.0, "p90": 3.0}]
    f = run(doc, "fixture")
    assert len(hits(f, "V12", "warning")) == 5 and not errors(f)


# ── line_horizons and the added run fields (brief 058c) ──────────────────────

def m15b(doc):
    return [c for c in doc["outputs"]["OW3"]["cells"] if c.get("line") == "M15b"]


def finalise(doc):
    """The fixture as a complete final model file (fixture flag removed, status final)."""
    doc["run"]["status"] = "final"
    doc["run"].pop("fixture", None)
    return doc


def test_m15b_is_reported_at_transition_only_in_the_fixture(doc):
    assert {c["horizon"] for c in m15b(doc)} == {"transition"}
    assert {c["horizon"] for c in doc["outputs"]["OW3"]["cells"] if c.get("line") == "M15a"} == \
        {"transition", "short", "long"}


def test_v7_complete_final_file_passes(run, doc):
    f = run(finalise(doc), "default")
    assert hits(f, "V7") == []


def test_v7_cell_outside_line_horizons_fails_in_every_mode(run, doc):
    extra = dict(m15b(doc)[0], horizon="short")
    doc["outputs"]["OW3"]["cells"].append(extra)
    for mode in ("fixture", "default", "final"):
        assert hits(run(doc, mode), "V7", "error"), mode


def test_v7_missing_transition_cell_fails_when_final_only(run, doc):
    cells = doc["outputs"]["OW3"]["cells"]
    cells.remove(m15b(doc)[0])
    assert not hits(run(doc, "fixture"), "V7", "error")
    assert not hits(run(doc, "default"), "V7", "error")   # provisional status: warning
    assert hits(run(finalise(doc), "default"), "V7", "error")


@pytest.mark.parametrize("name", ["pack_sha256", "pack_country", "levers_sha256"])
def test_v8_added_run_fields(run, doc, name):
    del doc["run"][name]
    assert hits(run(doc, "default"), "V8", "warning")      # provisional
    assert not hits(run(doc, "default"), "V8", "error")
    assert hits(run(finalise(doc), "default"), "V8", "error")
    assert not hits(run(doc, "default"), "V12")


def test_v8_pack_country_must_equal_country_pack(run, doc):
    doc["run"]["pack_country"] = "XXX"
    assert hits(run(doc, "default"), "V8", "error")


def test_added_run_fields_are_known_fields_and_absent_list_changes_nothing(vo, manifest, doc):
    assert hits(vo.validate(doc, manifest, MANIFEST, INPUTS_JSON, "fixture"), "V12") == []
    m = dict(manifest)
    m.pop("run_fields_added")
    for k in ("pack_sha256", "pack_country", "levers_sha256"):
        del doc["run"][k]
    assert vo.validate(doc, m, MANIFEST, INPUTS_JSON, "fixture") == []


# ── arms and withheld entries (brief 122c) ───────────────────────────────────

LEGACY_ONLY = ("OW1", "OW3", "OM1")                                   # 126c: O3, OH1b, OH1c and the tornado's M3 head returned to the household arm


def household(doc, arm="household"):
    """The fixture as a final household-arm file: the three legacy-only ids withheld (summary, no cells, the label), run.arm set."""
    finalise(doc)["run"]["arm"] = arm
    for oid in LEGACY_ONLY:
        doc["outputs"][oid] = {"summary": doc["outputs"][oid]["summary"], "cells": [], "withheld": "legacy_only"}
    return doc


def test_the_manifest_restricts_exactly_the_three_ids_to_the_legacy_arm(vo, manifest):
    assert {i for i, e in vo.load_entries(manifest).items() if e.arms} == set(LEGACY_ONLY)
    assert all(e.arms == ["legacy"] for i, e in vo.load_entries(manifest).items() if e.arms)


@pytest.mark.parametrize("arm", ["household", {"arm": "household", "central": False}])
def test_a_household_file_with_the_three_ids_withheld_passes_final(run, doc, arm):
    f = run(household(doc, arm), "final")
    assert errors(f) == [] and hits(f, "V12") == []


@pytest.mark.parametrize("arm", ["legacy", {"arm": "legacy"}, None])
def test_the_same_file_under_a_legacy_or_missing_arm_fails_v7(run, doc, arm):
    d = household(doc)
    d["run"].pop("arm") if arm is None else d["run"].update(arm=arm)
    f = run(d, "final")
    assert {x.where for x in hits(f, "V7", "error")} == {*LEGACY_ONLY}


def test_a_value_under_a_withheld_id_fails_v7_under_the_household_arm(run, doc):
    d = household(doc)
    d["outputs"]["OW3"] = {"summary": d["outputs"]["OW3"]["summary"], "cells": [dict(horizon="single", p10=1.0, mean=2.0, p90=3.0)], "withheld": "legacy_only"}
    assert [x.where for x in hits(run(d, "final"), "V7", "error")] == ["OW3"]
    d["outputs"]["OW1"].pop("withheld")                                    # a household file may not hold an id the arm cannot produce without the label
    assert [x.where for x in hits(run(d, "final"), "V7", "error")] == ["OW1", "OW3"]


def test_the_tornado_m3_head_is_a_household_value_since_126c(run, doc):
    d = household(doc)
    assert any(c["by"]["headline"] == "M3" for c in d["outputs"]["OT1"]["cells"]) and errors(run(d, "final")) == []


def test_withheld_is_refused_on_an_id_the_arm_produces_and_a_wrong_label_is_refused(run, doc):
    d = household(doc)
    d["outputs"]["O2"] = {"summary": d["outputs"]["O2"]["summary"], "cells": [], "withheld": "legacy_only"}
    d["outputs"]["OW1"]["withheld"] = "other"
    assert [x.where for x in hits(run(d, "final"), "V7", "error")] == ["O2", "OW1"]


def test_v8_run_arm_must_name_an_arm(run, doc):
    doc["run"]["arm"] = "hybrid"
    assert [x.where for x in hits(run(doc, "fixture"), "V8", "error")] == ["run.arm"]
