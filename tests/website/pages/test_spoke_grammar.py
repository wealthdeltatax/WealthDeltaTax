"""Section ids and the shortcode cross-reference grammar (brief 029s)."""
import pytest

import transforms as T
from conftest import ROOT

URLS = {"H": "/index.html", "FISC": "/fisc.html", "VAL": "/val.html", "ADD": "/add.html"}


def test_h2_ids_by_position():
    src = "# Title\n\n## Short answer\ntext\n\n### Sub\n\n## Evidence\n"
    out = T.add_section_ids(src, "FISC")
    assert "## Short answer {#fisc-1}" in out
    assert "## Evidence {#fisc-2}" in out
    assert "### Sub\n" in out                      # H3 untouched


def test_hub_sections_are_h0_to_h7():
    src = "".join(f"## Section {i}\n" for i in range(8))
    out = T.add_section_ids(src, "H", hub=True)
    for i in range(8):
        assert f"## Section {i} {{#h{i}}}" in out
    with pytest.raises(ValueError):
        T.add_section_ids(src + "## Ninth\n", "H", hub=True)


def test_existing_id_kept_and_counted():
    src = "## One {#custom}\n## Two\n"
    out = T.add_section_ids(src, "FISC")
    assert "## One {#custom}" in out and "## Two {#fisc-2}" in out


def test_attrs_without_id_get_one():
    assert T.add_section_ids("## One {.unnumbered}\n", "FISC") == "## One {#fisc-1 .unnumbered}\n"


def test_fenced_code_is_skipped():
    src = "```\n## not a heading\n```\n## Real\n"
    out = T.add_section_ids(src, "FISC")
    assert "## not a heading\n" in out and "## Real {#fisc-1}" in out


def test_refs_resolve():
    text = "See (FISC §2), (VAL), (H3), (DL2), (DL1-O1), (ADD §3)."
    out, bad = T.convert_spoke_refs(text, URLS)
    assert bad == []
    assert "[(FISC §2)](/fisc.html#fisc-2)" in out
    assert "[(VAL)](/val.html)" in out
    assert "[(H3)](/index.html#h3)" in out
    assert "[(DL2)](/data/inputs.html)" in out
    assert "[(DL1-O1)](/data/o1.html)" in out
    assert "[(ADD §3)](/add.html#add-3)" in out


def test_unknown_code_with_section_is_reported_bare_acronym_is_not():
    out, bad = T.convert_spoke_refs("A (FICS §2) typo, and (GDP) prose.", URLS)
    assert bad == ["(FICS §2)"]
    assert out == "A (FICS §2) typo, and (GDP) prose."


def test_old_s_form_and_dotted_codes_do_not_match():
    text = "(S5 §2) (LR.A §1) (VAL.A) (WP §3.5)"
    out, bad = T.convert_spoke_refs(text, URLS)
    assert out == text and bad == []


def test_code_is_skipped():
    out, _ = T.convert_spoke_refs("`(FISC §2)`\n```\n(FISC §2)\n```\n", URLS)
    assert "](" not in out


def test_only_spoke_files_are_eligible():
    src = ROOT / "papers" / "legacy"
    assert T.is_spoke_source(src / "hub.md", src)
    assert T.is_spoke_source(src / "spokes" / "FISC.md", src)
    assert not T.is_spoke_source(src / "5_Valuing_Wealth.md", src)
    assert not T.is_spoke_source(src / "spokes" / "x" / "y.md", src)
    assert not T.is_spoke_source(ROOT / "website" / "site" / "pages" / "faq.md", src)


def test_legacy_crossref_conversion_unchanged():
    """The legacy path must not pick up the new grammar."""
    out = T.convert_crossrefs("See (VAL §2) and (FISC §2).", {"VAL": "val.html"}, {})
    assert "[(VAL §2)](val.html)" in out
    assert "(FISC §2)" in out and "[(FISC" not in out
