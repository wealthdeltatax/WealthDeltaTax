"""registry/routing.yml and pipeline/pages/routing.py (brief 061s): the checks of nav.md 4.2."""
import pytest

import config as cfg
from conftest import FIXTURES, ROOT
from pages import routing as R


def codes(findings, level=None):
    return sorted({f.code for f in findings if level is None or f.level == level})


# ── the good file passes every check ──────────────────────────────────────────

def test_good_file_has_no_findings(rows, routes, infos):
    assert R.check_routing(routes, rows, infos) == []


# ── R01: every start id exists in the registry ────────────────────────────────

def test_r01_unknown_start_id_is_an_error(rows, infos, broken):
    routes = broken(lambda r: r[0]["start"].append("NOPE"))
    f = R.check_routing(routes, rows, infos)
    assert codes(f, "error") == ["R01"] and "NOPE" in f[0].message


def test_r01_a_non_spoke_row_is_not_a_start_id(rows, infos, broken):
    routes = broken(lambda r: r[0]["start"].append("H"))        # the hub row exists but is not a spoke
    assert "R01" in codes(R.check_routing(routes, rows, infos), "error")


def test_r01_data_token_and_appendix_ids_are_accepted(rows, infos, broken):
    routes = broken(lambda r: r[1]["start"].append("DECL"))
    assert "R01" not in codes(R.check_routing(routes, rows, infos))


# ── R02: reader and a non-empty start ─────────────────────────────────────────

def test_r02_missing_reader_is_an_error(rows, infos, broken):
    routes = broken(lambda r: r[2].pop("reader"))
    assert codes(R.check_routing(routes, rows, infos), "error") == ["R02"]


def test_r02_empty_start_is_an_error(rows, infos, broken):
    def cut(r):
        r[2]["start"] = []
    f = R.check_routing(broken(cut), rows, infos)
    assert "R02" in codes(f, "error")


# ── R03: every menu spoke is in a route ───────────────────────────────────────

def test_r03_uncovered_menu_spoke_is_an_error(rows, infos, broken):
    def drop_fair(r):
        r[1]["start"].remove("FAIR")
    f = R.check_routing(broken(drop_fair), rows, infos)
    assert codes(f, "error") == ["R03"] and f[0].where == "FAIR"


def test_r03_an_appendix_need_not_be_in_a_route(rows, routes, infos):
    assert not any(f.where == "DECL" for f in R.check_routing(routes, rows, infos))


# ── R04: dependencies earlier in the same route (warning) ─────────────────────

def test_r04_spoke_before_its_dependency_is_a_warning(rows, infos, broken):
    def reorder(r):
        r[0]["start"] = ["FISC", "MECH", "VAL", "data"]
    f = R.check_routing(broken(reorder), rows, infos)
    assert codes(f, "warning") == ["R04"] and codes(f, "error") == []
    assert {x.message.split()[0] for x in f} == {"FISC"}


def test_r04_passes_when_dependencies_come_first(rows, routes, infos):
    assert "R04" not in codes(R.check_routing(routes, rows, infos))


# ── R05: prompt at most 20 words, no digit ────────────────────────────────────

def test_r05_prompt_over_20_words_is_an_error(rows, infos, broken):
    routes = broken(lambda r: r[0].update(prompt=" ".join(["word"] * 21)))
    assert codes(R.check_routing(routes, rows, infos), "error") == ["R05"]


def test_r05_prompt_of_exactly_20_words_passes(rows, infos, broken):
    routes = broken(lambda r: r[0].update(prompt=" ".join(["word"] * 20)))
    assert R.check_routing(routes, rows, infos) == []


def test_r05_prompt_with_a_digit_is_an_error(rows, infos, broken):
    routes = broken(lambda r: r[0].update(prompt="I want 3 results."))
    assert codes(R.check_routing(routes, rows, infos), "error") == ["R05"]


# ── R06: field rules ──────────────────────────────────────────────────────────

def test_r06_duplicate_route_id(rows, infos, broken):
    routes = broken(lambda r: r[1].update(id="alpha"))
    assert "R06" in codes(R.check_routing(routes, rows, infos), "error")


def test_r06_start_of_six_and_duplicate_entries(rows, infos, broken):
    routes = broken(lambda r: r[0].update(start=["MECH", "VAL", "FISC", "FAIR", "data", "DECL"]))
    assert any("limit is 5" in f.message for f in R.check_routing(routes, rows, infos))
    routes = broken(lambda r: r[0].update(start=["MECH", "MECH"]))
    assert any("duplicate" in f.message for f in R.check_routing(routes, rows, infos))


# ── renderer data ─────────────────────────────────────────────────────────────

def test_hub_cards_follow_the_file_and_link_by_question(rows, routes, infos):
    cards = R.hub_cards(routes, rows, infos)
    assert [c["id"] for c in cards] == ["alpha", "beta", "gamma"]
    a = cards[0]
    assert a["reader"] == "Economist" and a["prompt"].startswith("I want to check")
    first = a["links"][0]
    assert first == {"id": "MECH", "text": "How does the tax work?", "chip": "MECH",
                     "url": "/mech.html", "is_data": False, "primary": True}
    assert not a["links"][1]["primary"]


def test_hub_cards_render_data_as_the_numbers(rows, routes, infos):
    link = R.hub_cards(routes, rows, infos)[0]["links"][-1]
    assert (link["text"], link["url"], link["chip"], link["is_data"]) == ("The numbers", "/data.html", None, True)
    assert R.hub_cards(routes, rows, infos)[2]["links"][0]["primary"] is True     # data first


def test_link_falls_back_to_the_label_without_a_spoke_file(rows, routes, infos):
    fair = R.hub_cards(routes, rows, infos)[1]["links"][0]
    assert fair["text"] == "Fairness"                      # no FAIR.md in the fixture


def test_card_order_field_overrides_file_order(rows, infos, broken):
    routes = broken(lambda r: r[2].update(order=0))
    assert R.hub_cards(routes, rows, infos)[0]["id"] == "gamma"


def test_read_next_lists_only_routes_containing_the_spoke(rows, routes, infos):
    ids = [l["route"] for l in R.read_next("VAL", routes, rows, infos)]
    assert ids == ["alpha", "beta", "gamma"]
    assert [l["route"] for l in R.read_next("FAIR", routes, rows, infos)] == ["beta"]


def test_read_next_gives_the_following_entry(rows, routes, infos):
    line = R.read_next("MECH", routes, rows, infos)[0]
    assert line["route"] == "alpha" and line["next"]["id"] == "VAL" and not line["back_to_hub"]
    assert line["text"] == "If you are a Economist: next, How is wealth valued?"


def test_read_next_last_entry_goes_back_to_the_hub(rows, routes, infos):
    lines = R.read_next("FISC", routes, rows, infos)
    beta = next(l for l in lines if l["route"] == "beta")
    assert beta["next"] is None and beta["back_to_hub"] and beta["hub_url"] == "/index.html"
    assert beta["text"].endswith("Back to the hub")


def test_read_next_before_data_names_the_numbers(rows, routes, infos):
    alpha = next(l for l in R.read_next("FISC", routes, rows, infos) if l["route"] == "alpha")
    assert alpha["next"]["text"] == "The numbers"


def test_read_next_for_a_page_in_no_route_is_empty(rows, routes, infos):
    assert R.read_next("DECL", routes, rows, infos) == []


# ── spoke information ─────────────────────────────────────────────────────────

def test_spoke_infos_read_front_matter_and_report_missing_files(rows, spokes_dir):
    infos, findings = R.spoke_infos(rows, spokes_dir)
    assert infos["FISC"]["question"] == "What rate, what threshold, how much?"
    assert infos["FISC"]["status"] == "accepted" and infos["FISC"]["depends"] == ["MECH", "VAL"]
    assert infos["FISC"]["short_answer"].startswith("The tax raises a modest share")
    assert infos["FAIR"]["has_file"] is False and infos["FAIR"]["question"] == "Fairness"
    missing = {f.where for f in findings}
    assert missing == {"FAIR", "DECL"} and {f.level for f in findings} == {"info"}


# ── the real files ────────────────────────────────────────────────────────────

def test_real_routing_file_passes_every_check():
    rows = cfg.load_pages()
    assert cfg.validate_pages(rows) == []
    routes = R.load_routing()
    findings = R.check_routing(routes, rows)
    assert R.errors(findings) == [], [str(f) for f in findings]


def test_real_routing_file_has_six_routes_and_covers_the_menu():
    rows = cfg.load_pages()
    routes = R.load_routing()
    assert [r["id"] for r in routes] == ["economist", "lawyer", "policy", "business", "sceptic", "researcher"]
    assert [r["reader"] for r in routes] == [
        "Economist", "Tax lawyer or administrator", "Policymaker or adviser",
        "Business owner or accountant", "Philosopher or sceptic", "Researcher wanting the numbers"]
    page_ids = {r["id"] for r in rows if r["type"] in cfg.SPOKE_KINDS}
    for route in routes:
        assert 1 <= len(route["start"]) <= 5
        assert all(s == "data" or s in page_ids for s in route["start"])
    menu = {r["id"] for r in rows if r["type"] == "spoke" and r["order"] is not None}
    assert len(menu) == 15 and menu <= {s for r in routes for s in r["start"]}
    for route in routes:
        assert len(route["prompt"].split()) <= 20 and not any(c.isdigit() for c in route["prompt"])


def test_script_check_exits_zero_on_the_real_files():
    assert R.main([]) == 0
