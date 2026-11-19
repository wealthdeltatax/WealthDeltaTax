"""The command line: resolve, validate, report; exit status; byte-identical report."""
import json, os, subprocess, sys
from conftest import DATA, FX, PIPELINE

SCRIPT = str(PIPELINE / "hooks.py")


def cli(*args, mode="draft"):
    env = {**os.environ, "WDT_MODE": mode}
    return subprocess.run([sys.executable, "-I", SCRIPT, *map(str, args)], capture_output=True, text=True, env=env)


def partial(tmp_path, doc):
    doc["outputs"]["O2"]["cells"] = [c for c in doc["outputs"]["O2"]["cells"] if c["by"]["wealth_band"] != "D10"]
    p = tmp_path / "partial.json"
    p.write_text(json.dumps(doc), encoding="utf-8")
    return p


def test_resolve_draft_gives_placeholders_for_missing_cells_and_numbers_for_the_rest(tmp_path, doc):
    r = cli("resolve", FX / "pay.md", "--data", partial(tmp_path, doc), "--fixture")
    assert r.returncode == 0, r.stderr
    assert "[[O2.range@S_central/short#wealth_band:D10]]" in r.stdout and "3.10% over a lifetime" in r.stdout


def test_resolve_release_fails_on_every_placeholder(tmp_path, doc):
    r = cli("resolve", FX / "pay.md", "--data", partial(tmp_path, doc), "--fixture", mode="release")
    assert r.returncode == 1 and r.stderr.count("H11 ") == 1


def test_both_fixture_spokes_resolve_cleanly_in_both_modes():
    for spoke in ("pay", "fisc"):
        for mode in ("draft", "release"):
            r = cli("resolve", FX / f"{spoke}.md", "--data", DATA, "--fixture", mode=mode)
            assert r.returncode == 0 and not r.stderr and "[[" not in r.stdout, (spoke, mode, r.stderr)


def test_validate_calls_the_validator(tmp_path):
    assert cli("validate", DATA, "--fixture").returncode == 0
    assert cli("validate", DATA).returncode == 1          # a fixture is not accepted without the flag


def test_report_is_byte_identical_and_has_the_schema(tmp_path, doc):
    a, b = tmp_path / "a.json", tmp_path / "b.json"
    data = partial(tmp_path, doc)
    for out in (a, b):
        assert cli("report", FX / "pay.md", FX / "fisc.md", "--data", data, "--fixture", "--out", out).returncode == 0
    assert a.read_bytes() == b.read_bytes()
    rep = json.loads(a.read_text(encoding="utf-8"))
    assert rep["schema"] == "wdt-hooks-report/1" and rep["mode"] == "draft" and rep["data_status"] == "fixture"
    assert set(rep) == {"schema", "mode", "data_status", "counts", "unresolved", "errors", "warnings"}
    assert [u["code"] for u in rep["unresolved"]] == ["H11"] and rep["counts"]["placeholder"] == 1
    assert set(rep["unresolved"][0]) == {"file", "line", "hook", "code", "message"}


def test_no_data_means_every_o_hook_is_a_placeholder_in_draft():
    r = cli("resolve", FX / "fisc.md")
    assert r.returncode == 0 and "[[O1:M1.mean@S_central/short]]" in r.stdout
