"""build_inputs.py: the register becomes registry/inputs.json (brief 030c)."""

from __future__ import annotations

import json
import subprocess
import sys

import pytest

from conftest import INPUTS_JSON, INPUTS_MD, PIPELINE, ROOT

HEADER = "| ID | Input | Unit | Low | Central | High | How | Source | Licence | Coverage | In repo | Confidence |\n|---|---|---|---|---|---|---|---|---|---|---|---|\n"


def row(rid="I-X1", low="1", central="2", high="3", how="**(J)** why", source="S1, S2"):
    return f"| {rid} | an input | % | {low} | {central} | {high} | {how} | {source} | OGL | GB | none | low |\n"


def parse(build_inputs, text):
    return build_inputs.parse_register(text)


def test_real_register_has_274_entries(build_inputs):
    rows, _ = parse(build_inputs, INPUTS_MD.read_text(encoding="utf-8"))
    assert len(rows) == 298
    assert len({r["id"] for r in rows}) == 298


def test_committed_json_matches_the_register(build_inputs):
    rows, _ = parse(build_inputs, INPUTS_MD.read_text(encoding="utf-8"))
    on_disk = json.loads(INPUTS_JSON.read_text(encoding="utf-8"))
    assert on_disk["count"] == 298 == len(on_disk["inputs"])
    assert INPUTS_JSON.read_text(encoding="utf-8") == build_inputs.render(rows)


def test_row_with_other_than_twelve_cells_fails(build_inputs):
    short = HEADER + "| I-X1 | an input | % | 1 | 2 | 3 | how | S1 | OGL | GB | none |\n"
    with pytest.raises(build_inputs.RegisterError, match="11 cells"):
        parse(build_inputs, short)
    long = HEADER + row().rstrip("\n") + " extra |\n"
    with pytest.raises(build_inputs.RegisterError, match="13 cells"):
        parse(build_inputs, long)


def test_duplicate_id_fails(build_inputs):
    with pytest.raises(build_inputs.RegisterError, match="duplicate id I-X1"):
        parse(build_inputs, HEADER + row() + row())


def test_empty_register_fails(build_inputs):
    with pytest.raises(build_inputs.RegisterError, match="no register rows"):
        parse(build_inputs, "# nothing here\n")


def test_numbers_and_explicit_nulls(build_inputs):
    text = HEADER + row(low="not found", central="12,570", high="[0.5]") + row(
        "I-X2", low="1 (listed shares)", central="-3.5", high="7"
    )
    rows, _ = parse(build_inputs, text)
    a, b = rows
    assert a["low"] is None and a["nulls"]["low"] == {"reason": "not found", "raw": "not found"}
    assert a["central"] == 12570 and "central" not in a["nulls"]
    assert a["high"] is None and a["nulls"]["high"]["reason"] == "bracket"
    assert b["low"] is None and b["nulls"]["low"] == {"reason": "text", "raw": "1 (listed shares)"}
    assert b["central"] == -3.5 and b["high"] == 7


def test_judgement_flag_and_sources(build_inputs):
    text = HEADER + row(how="**(J)** bounds", source="X (S1, https://e.org), SH2") + row(
        "I-X2", how="plain", source="none"
    )
    rows, warns = parse(build_inputs, text)
    assert rows[0]["judgement"] is True and rows[1]["judgement"] is False
    assert rows[0]["sources"] == ["S1", "SH2"]
    assert rows[1]["sources"] == []
    assert any("S1" in w for w in warns)   # no source table in the snippet


def test_real_register_nulls_are_counted(build_inputs):
    rows, _ = parse(build_inputs, INPUTS_MD.read_text(encoding="utf-8"))
    reasons = [v["reason"] for r in rows for v in r["nulls"].values()]
    assert reasons.count("not found") == 11
    assert set(reasons) <= {"not found", "bracket", "text"}


def test_two_runs_are_byte_identical_under_isolated_python(tmp_path):
    outs = []
    for i in range(2):
        out = tmp_path / f"inputs{i}.json"
        subprocess.run(
            [sys.executable, "-I", str(PIPELINE / "build_inputs.py"), "--out", str(out)],
            check=True, capture_output=True, cwd=tmp_path,
        )
        outs.append(out.read_bytes())
    assert outs[0] == outs[1]
    assert outs[0] == INPUTS_JSON.read_bytes()


def test_failure_exit_status(tmp_path):
    bad = tmp_path / "inputs.md"
    bad.write_text(HEADER + row() + row(), encoding="utf-8")
    r = subprocess.run(
        [sys.executable, "-I", str(PIPELINE / "build_inputs.py"), "--src", str(bad), "--out", str(tmp_path / "o.json")],
        capture_output=True, text=True, cwd=tmp_path,
    )
    assert r.returncode == 1 and "duplicate id" in r.stderr
    assert not (tmp_path / "o.json").exists()
