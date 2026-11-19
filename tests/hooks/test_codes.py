"""One test per error code of hooks.md 4.7 (H01 to H13, H20 to H23, H30 to H32, H40 to H42, R1r, A2) plus F1."""
import pytest
from conftest import codes

FIG = '::: {#fig-PAY-%d}\noutput: [O2]\nkind: bar\ncaption: "Burden. Data: Table F-PAY-%d."\n:::\n'


def test_h01_text_matches_no_hook_form(run):
    for body in ["{{o:O2.mean", "{{x:foo}}", "{{o:O2.mean#}}", "{{lit:nocolon}}", "{{ref:fig-nope}}"]:
        assert "H01" in codes(run(body)), body


def test_h02_unknown_output_id(run):
    assert codes(run("{{o:ZZ9}}")) == ["H02"]


def test_h03_stat_illegal_for_the_summary_form(run):
    for body in ["{{o:O2.point}}", "{{o:O2.series}}", "{{o:DH1b.range}}", "{{o:O7.mean}}"]:
        assert "H03" in codes(run(body, spoke="HUB")), body


def test_h04_unknown_schedule_and_schedule_on_a_once_output(run):
    assert codes(run("{{o:O2@S_bad}}")) == ["H04"]
    assert codes(run("{{o:OH1b@S_central}}", spoke="HUB")) == ["H04"]


def test_h05_unknown_horizon(run):
    assert codes(run("{{o:O2/yearly}}")) == ["H05"]


def test_h06_horizon_for_a_single_output_or_outside_the_set(run):
    assert codes(run("{{o:OP1/short}}", spoke="FISC")) == ["H06"]
    assert codes(run("{{o:OW3:M15b/short}}", spoke="WELF")) == ["H06"]      # M15b is transition only


def test_h07_by_key_value_or_line_not_in_the_manifest(run):
    for body in ["{{o:O2#wealth_band:XX}}", "{{o:O2#nokey:x}}", "{{o:O1:ZZ.mean}}", "{{o:O2:M1}}"]:
        assert "H07" in codes(run(body, spoke="FISC")), body


def test_h08_line_or_by_value_missing_and_no_overall(run):
    assert codes(run("{{o:O1.mean}}", spoke="FISC")) == ["H08"]            # no line selector
    assert codes(run("{{o:OP6.mean}}", spoke="FUND")) == ["H08"]           # year has no overall
    assert codes(run("{{o:OP6.mean#overall}}", spoke="FUND")) == ["H08"]


def test_h09_schedule_or_horizon_omitted_without_default(run):
    assert codes(run("{{o:O2.mean}}", defaults=False)) == ["H09"]


def test_h10_forward_r1_output_does_not_list_the_spoke(run):
    assert codes(run("{{o:O1a}}")) == ["H10"]
    assert codes(run("{{o:O1a}}", mode="release")) == ["H10"]


def cell(doc, oid, **kw):
    return next(c for c in doc["outputs"][oid]["cells"] if all(c.get(k) == v for k, v in kw.items()))


def test_h11_no_cell_or_no_data(run, make, doc):
    doc["outputs"]["O2"]["cells"].remove(cell(doc, "O2", schedule="S_central", horizon="short", by={"wealth_band": "overall"}))
    r = run("{{o:O2}}", ctx=make("draft", doc))
    assert "[[O2.mean@S_central/short]]" in r["text"] and codes(r, "unresolved") == ["H11"] and not r["errors"]
    assert codes(run("{{o:O2}}", "release", ctx=make("release", doc))) == ["H11"]
    assert codes(run("{{o:O2}}", ctx=make("draft", None)), "unresolved") == ["H11"]


def test_h12_null_field(run, make, doc):
    cell(doc, "O2", schedule="S_central", horizon="short", by={"wealth_band": "overall"})["mean"] = None
    r = run("{{o:O2}}", ctx=make("draft", doc))
    assert codes(r, "unresolved") == ["H12"] and "[[O2.mean@S_central/short]]" in r["text"]
    assert codes(run("{{o:O2}}", "release", ctx=make("release", doc))) == ["H12"]


def test_h13_data_inconsistent_with_manifest(hooks, make, doc, run):
    doc["run"]["status"] = "bogus"                                          # a V8 error
    c = make("draft", doc)
    assert c.data is None and c.data_findings[0][1] == "H13"
    assert "H13" in [x["code"] for x in hooks.build_report([run("{{o:O2}}", ctx=c)], c)["errors"]]
    assert make("draft", fixture=False).data is None                        # fixture file without --fixture
    doc2 = {**doc, "run": {k: v for k, v in doc["run"].items() if k != "fixture"}}
    doc2["run"]["status"] = "provisional"
    assert make("release", doc2, fixture=False).data_findings[0][1] == "H13"   # release needs final


def test_h20_unknown_input_id(run):
    assert codes(run("{{i:I-ZZ9}}")) == ["H20"]


def test_h21_stat_illegal_for_an_input(run):
    assert codes(run("{{i:I-D4b.mean}}")) == ["H21"]


def test_h22_no_display_spec(run, make):
    c = make()
    c.display.pop("I-D4b")
    assert codes(run("{{i:I-D4b}}", ctx=c)) == ["H22"]


def test_h23_selected_value_is_not_a_number(run, make):
    c = make()
    text_row = next(k for k, v in c.display.items() if v["unit"] == "text")
    assert codes(run("{{i:%s}}" % text_row, ctx=c)) == ["H23"]
    assert codes(run("{{i:I-D1c}}", ctx=c)) == ["H23"]                      # no numeric cell yet
    assert "54.9%" in run("{{i:I-D4b}} {{i:I-D4b.range}}", ctx=c)["text"]


def test_h30_ref_to_a_figure_not_in_this_file(run):
    assert codes(run("{{ref:fig-PAY-9}}")) == ["H30"]
    assert codes(run("{{ref:fig-FISC-1}}")) == ["H30"]                      # another spoke's figure


def test_h31_figure_numbers_not_one_to_k(run):
    body = FIG % (1, 1) + FIG % (3, 3) + "{{ref:fig-PAY-1}} {{o:O2}}. {{ref:fig-PAY-3}} {{o:O2}}."
    assert "H31" in codes(run(body))
    ok = FIG % (1, 1) + FIG % (2, 2) + "{{ref:fig-PAY-1}} {{o:O2}}. {{ref:fig-PAY-2}} {{o:O2}}."
    assert "H31" not in codes(run(ok))


def test_h32_figure_uncited_or_citing_sentence_without_an_o_hook(hooks, run):
    assert codes(run(FIG % (1, 1))) == ["H32"]
    assert codes(run(FIG % (1, 1) + "See {{ref:fig-PAY-1}}.")) == ["H32"]
    assert codes(run(FIG % (1, 1) + "The burden is {{o:O2}}, as {{ref:fig-PAY-1}} draws.")) == []
    assert hooks.check_f4(FIG % (1, 1))[0][0] == "H32"


def test_h40_lit_key_not_in_registry(run):
    assert codes(run("{{lit:Foo2000:bar}}")) == ["H40"]


def test_h41_lit_not_verified(run, make):
    c = make()
    c.lit["ONS2025ETB:retired-net-recipients"]["verified"] = False
    k = "ONS2025ETB:retired-net-recipients"
    assert f"[[lit:{k}]]" in run("{{lit:%s}}" % k, ctx=c)["text"]
    rel = make("release")
    rel.lit = c.lit
    assert codes(run("{{lit:%s}}" % k, mode="release", ctx=rel)) == ["H41"]


def test_h42_lit_bib_key_missing_and_verified_lit_cites_its_source(run):
    assert codes(run("{{lit:AdvaniBanghamLeslie2021:top1-share-survey}}")) == ["H42"]
    r = run("{{lit:ONS2025ETB:council-tax-top-decile-gbp}}")
    assert not r["errors"] and r["citations"] == {"ONS2025ETB"} and "£" in r["text"]


def test_r1r_reverse_r1_warning_in_draft_error_in_release(hooks, run):
    assert "R1r" in codes(run("No hooks here."), "warnings", True) and not run("No hooks here.")["errors"]
    assert "R1r" in codes(run("No hooks here.", mode="release"), "errors", True)
    miss = hooks.check_r1_reverse({"PAY": "{{o:O2}}"})
    assert ("PAY", "O3") in miss and ("PAY", "O2") not in miss


def test_a2_long_in_short_answer_needs_a_short_beside_it(run):
    assert codes(run("**Short answer.** The burden is {{o:O2/long}}.")) == ["A2"]
    assert "A2" not in codes(run("**Short answer.** It is {{o:O2/long}}, from {{o:O2/short}}."))
    assert "A2" not in codes(run("Evidence: {{o:O2/long}}."))


def test_f1_hook_in_a_figure_caption(run):
    body = '::: {#fig-PAY-1}\noutput: [O2]\ncaption: "Burden {{o:O2}}. Data: Table F-PAY-1."\n:::'
    assert "F1" in codes(run(body))
