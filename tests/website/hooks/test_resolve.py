"""Resolver behaviour beyond single codes: scanning, ids, modes, counting, the real registries."""
from conftest import FX, codes


def test_hooks_in_code_spans_and_fences_are_ignored(run):
    body = "A `{{o:ZZ9}}` span.\n```\n{{o:ZZ9}} {{broken\n```\n~~~\n{{x:y}}\n~~~"
    r = run(body)
    assert not r["errors"] and r["counts"] == {"resolved": 0, "placeholder": 0, "error": 0}
    assert "{{o:ZZ9}}" in r["text"]


def test_ids_the_old_regex_missed_are_recognised(run):
    r = run("{{o:DH1a#series:wid_top1}} {{o:OH1b2}}", spoke="HUB")
    assert not r["errors"] and r["counts"]["resolved"] == 2
    r = run("{{o:CK1:P1.point#amplitude:A1}}", spoke="FALS")
    # brief 065g: CK1 declares lines P1, P3, P7b, so it resolves like OW3
    assert not r["errors"] and r["counts"]["resolved"] == 1


def test_default_and_explicit_overall_give_the_template_placeholder(run, make):
    r = run("{{o:O2.mean#wealth_band:overall}} {{o:O2}}", ctx=make("draft", None))
    assert r["text"].count("[[O2.mean@S_central/short]]") == 2 and not r["errors"]


def test_ref_becomes_a_link_and_figure_numbers_follow_the_block(run):
    body = '::: {#fig-PAY-1}\noutput: [O2]\ncaption: "Burden. Data: Table F-PAY-1."\n:::\n{{o:O2}} as {{ref:fig-PAY-1}}.'
    assert "[Figure 1](#fig-PAY-1)" in run(body)["text"]


def test_draft_and_release_for_the_same_input(run, make, doc):
    doc["outputs"]["O2"]["cells"] = [c for c in doc["outputs"]["O2"]["cells"] if c["by"]["wealth_band"] != "D10"]
    body = "{{o:O2}} {{o:O2#wealth_band:D10}}"
    d = run(body, ctx=make("draft", doc))
    assert d["counts"] == {"resolved": 1, "placeholder": 1, "error": 0} and not d["errors"]
    assert "4.00%" in d["text"] and "[[O2.mean@S_central/short#wealth_band:D10]]" in d["text"]
    r = run(body, "release", ctx=make("release", doc))
    assert codes(r) == ["H11"] and r["counts"]["error"] == 1


def test_word_count_treats_a_hook_and_its_placeholder_alike(hooks, run, make):
    text = "The burden is {{o:O2.range#wealth_band:D10}} of wealth."
    resolved = run(text, ctx=make("draft", None))["text"].split("---\n", 2)[2]
    assert hooks.count_words(text) == hooks.count_words(resolved) == 6


def test_wdt_mode_selects_the_mode(hooks, monkeypatch):
    monkeypatch.setenv("WDT_MODE", "release")
    assert hooks.Ctx(None, False, None, {"bib": FX / "references.bib"}).mode == "release"
    monkeypatch.delenv("WDT_MODE")
    assert hooks.Ctx(None, False, None, {"bib": FX / "references.bib"}).mode == "draft"


def test_the_real_registries_load(hooks):
    c = hooks.Ctx()
    assert len(c.inputs) == len(c.display) >= 274 and len(c.lit) >= 67
    assert c.data is None and len(c.entries) >= 37
    # H42 fires on the lit keys whose bib key is not in the real bibliography (proposed keys, brief 043r): expected
    missing = {k for k in c.lit if k.split(":")[0] not in c.bib}
    assert missing, "expected the proposed keys to be missing from references.bib until the references rework"
