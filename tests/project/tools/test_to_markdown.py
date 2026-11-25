"""Brief 130c: the reading copies of project/tools/to_markdown.py on small fixtures built in a temporary repo root."""
import importlib.util
import json
import shutil
import sys
from pathlib import Path

import pytest

pytest.importorskip("markitdown")
openpyxl = pytest.importorskip("openpyxl")
ROOT = Path(__file__).resolve().parents[3]
spec = importlib.util.spec_from_file_location("to_markdown", ROOT / "project" / "tools" / "to_markdown.py")
tm = importlib.util.module_from_spec(spec)
sys.modules["to_markdown"] = tm
spec.loader.exec_module(tm)


@pytest.fixture
def repo(tmp_path):
    (tmp_path / "data" / "x").mkdir(parents=True)
    return tmp_path


def sheet(repo, name="a.xlsx", rows=30):
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Table_1"
    ws.append(["year", "value"])
    for i in range(rows):
        ws.append([2000 + i, i * 1.5])
    p = repo / "data" / "x" / name
    wb.save(p)
    return p


def test_the_copy_sits_at_the_mirror_path_with_a_header(repo):
    r = tm.readable_copy(sheet(repo), repo, rows=100)
    dst = repo / "literature" / "readable" / "data" / "x" / "a.xlsx.md"
    text = dst.read_text()
    assert Path(r["dst"]) == dst and r["status"] == "ok" and r["cut"] == []
    head = text.split("\n\n")[0]
    assert "Reading copy** of `data/x/a.xlsx`" in head and "markitdown" in head and "Quote numbers from the source" in head and "converted 20" in head
    assert "| 2029 |" in text and "Truncated" not in text


def test_a_long_sheet_is_capped_with_a_visible_note_and_the_row_count(repo):
    r = tm.readable_copy(sheet(repo, rows=30), repo, rows=10)
    text = Path(r["dst"]).read_text()
    assert r["cut"] == [("Table_1", 30)] and "Row cap: 10 data rows a table; cut: Table_1 (30 rows)" in text.split("\n\n")[0]
    assert "the first 10 of 30 rows" in text and "| 2009 |" in text and "| 2010 |" not in text


def test_the_status_file_and_the_index_list_every_binary(repo):
    sheet(repo, "a.xlsx"), sheet(repo, "b.xlsx", rows=3)
    rc = tm.main(["--readable", "--all", "--index", "--root", str(repo)])
    st = json.loads((repo / "literature/readable/status.json").read_text())
    idx = (repo / "literature/readable/readable-copies-index.md").read_text()
    assert rc == 0 and set(st) == {"data/x/a.xlsx", "data/x/b.xlsx"} and "Files: 2;" in idx and "| `data/x/a.xlsx` | xlsx |" in idx and "ok" in idx
    assert tm.main(["--readable", "--all", "--root", str(repo)]) == 0 and tm.binaries(repo)[0].name == "a.xlsx"          # a second pass converts nothing new


def test_a_file_outside_data_and_literature_and_a_copy_are_refused(repo, tmp_path):
    out = tmp_path / "elsewhere.xlsx"
    shutil.copy(sheet(repo), out)
    with pytest.raises(ValueError, match="not a file under data/ or literature/"):
        tm.readable_copy(out, repo)
    r = tm.readable_copy(sheet(repo), repo)
    with pytest.raises(ValueError, match="not converted again"):
        tm.readable_copy(r["dst"], repo)


@pytest.mark.skipif(not shutil.which("pandoc"), reason="pandoc not installed")
def test_rtf_goes_through_pandoc(repo):
    p = repo / "data" / "x" / "d.rtf"
    p.write_text(r"{\rtf1\ansi Variable HV1 is the household value.\par}")
    r = tm.readable_copy(p, repo)
    assert r["status"] == "ok" and "pandoc" in r["route"] and "household value" in Path(r["dst"]).read_text()


@pytest.mark.skipif(not (shutil.which("soffice") or shutil.which("libreoffice")), reason="LibreOffice not installed")
def test_ods_goes_through_soffice_then_markitdown(repo, tmp_path):
    import subprocess
    x = sheet(repo, "w.xlsx", rows=4)
    subprocess.run([shutil.which("soffice") or "libreoffice", "--headless", "--convert-to", "ods", "--outdir", str(x.parent), str(x)], check=True, capture_output=True)
    x.unlink()
    r = tm.readable_copy(x.with_suffix(".ods"), repo)
    assert r["status"] == "ok" and "soffice" in r["route"] and "| 2003 |" in Path(r["dst"]).read_text()
