import re
from pathlib import Path

import pytest

import config as cfg
from conftest import ROOT
from pages import retired as R

# 30 retired numbered papers: the legacy rows that are not the three standalones or site pages
STANDALONE = {"ADD", "INST", "SCOPE"}


def retired_ledger_stems(pages, ledger):
    return [h for row, h in R.legacy_papers(pages, ledger)]


def test_header_states_mapping_and_frozen():
    head = R.RETIRED_YML.read_text(encoding="utf-8").split("papers:")[0]
    assert "frozen: true" in head
    for word in ("glossary", "UK data pack", "parameter register", "method note for O7", "H1, H2"):
        assert word in head


def test_every_legacy_paper_once_and_no_other(pages, retired, ledger):
    expected = [row["id"] for row, _ in R.legacy_papers(pages, ledger)]
    got = [p["id"] for p in retired]
    assert len(got) == 30
    assert sorted(got) == sorted(expected) and len(set(got)) == len(got)
    ids = {r["id"]: r for r in pages}
    for pid in got:
        assert ids[pid]["type"] == "legacy"


def test_ids_and_successors_resolve(pages, retired):
    ids = {r["id"] for r in pages}
    for p in retired:
        assert 1 <= len(p["successor"]) <= 3 or not p["successor"]
        for s in p["successor"]:
            assert s in ids
        for sec in p["sections"]:
            assert sec["page"] is None or sec["page"] in ids


def test_null_page_rows_carry_a_reason_or_target(retired):
    for p in retired:
        for s in p["sections"]:
            if s["page"] is None and s["target"] == "-":
                assert s["reason"]
            if s["page"] is not None:
                assert s["reason"] is None


def test_every_ledger_row_of_the_30_papers_once(pages, retired, ledger):
    for row, heading in R.legacy_papers(pages, ledger):
        paper = next(p for p in retired if p["id"] == row["id"])
        want = [(r["sec"], r["title"], r["words"], r["disp"], r["target"]) for r in ledger[heading]]
        got = [(s["sec"], s["title"], s["words"], s["disp"], s["target"]) for s in paper["sections"]]
        assert got == want


def test_successor_is_top_kept_and_merged_words():
    rows = [
        {"words": 100, "disp": "K", "page": "A"}, {"words": 50, "disp": "M", "page": "B"},
        {"words": 40, "disp": "D", "page": "C"}, {"words": 30, "disp": "K", "page": "C"},
        {"words": 20, "disp": "K", "page": "D"}, {"words": 10, "disp": "K", "page": None},
    ]
    assert R.successors(rows) == ["A", "B", "C"]


def test_successor_tie_is_an_error():
    rows = [{"words": 5, "disp": "K", "page": "A"}, {"words": 5, "disp": "K", "page": "B"}]
    with pytest.raises(R.TieError):
        R.successors(rows)


def test_resolve_target_mapping():
    by_id = {"FISC": {"type": "spoke"}, "H": {"id": "H", "type": "hub"}, "GLOSS": {"type": "appendix"}}
    assert R.resolve_target("FISC", by_id) == ("FISC", True)
    assert R.resolve_target("H1", by_id) == ("H", True)
    assert R.resolve_target("glossary", by_id) == ("GLOSS", True)
    assert R.resolve_target("UK data pack", by_id) == (None, True)
    assert R.resolve_target("-", by_id) == (None, True)
    assert R.resolve_target("nonsense", by_id) == (None, False)


def test_frozen_file_is_not_overwritten(tmp_path):
    out = tmp_path / "retired.yml"
    out.write_text("frozen: true\npapers: []\n", encoding="utf-8")
    with pytest.raises(R.FrozenError):
        R.run_convert(out=out)
    assert out.read_text(encoding="utf-8") == "frozen: true\npapers: []\n"


def test_the_committed_file_is_frozen():
    assert R.is_frozen(R.RETIRED_YML)


def test_page_has_one_table_per_paper_and_no_legacy_link(page_text, pages, retired):
    assert page_text.count("| Old shortcode |") == len(retired) == 30
    # Five new pages (VAL, CORP, GOV, BEHAV, POL) reuse the URL of the old paper they replace, so a
    # link is judged by the page row it points to: every link target must belong to a live (non-legacy) row.
    live_urls = {r["url"] for r in pages if r["type"] != "legacy"}
    targets = [t for _x, t in re.findall(r"\[([^\]]*)\]\(([^)]*)\)", page_text)]
    assert targets
    for t in targets:
        assert t in live_urls
    assert "/revision_history.html" in targets


def test_null_rows_show_reason_without_link(page_text):
    assert "(no page yet)" in page_text


def _shingles(text, n=12):
    w = re.findall(r"\w+", text.lower())
    return {" ".join(w[i:i + n]) for i in range(len(w) - n + 1)}


def test_no_twelve_word_overlap_with_legacy_source(page_text, pages, retired):
    """
    No legacy prose is copied.  Titles are copied on purpose (brief: section numbers and titles), and
    a title of 12 words or more matches the paper's own heading; those lines are the only exemption.
    """
    titles = {p["title"] for p in retired} | {s["title"] for p in retired for s in p["sections"]}
    src = set()
    for r in pages:
        if r["type"] == "legacy" and r["source"] and r["source"].startswith("papers/legacy/"):
            src |= _shingles((ROOT / r["source"]).read_text(encoding="utf-8"))
    for line in page_text.splitlines():
        if _shingles(line) & src:
            assert any(t in line for t in titles if len(re.findall(r"\w+", t)) >= 12), line
