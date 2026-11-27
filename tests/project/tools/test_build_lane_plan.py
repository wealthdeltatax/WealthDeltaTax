"""build_lane_plan.py: header parsing, errors, idempotence, --check and retiring a brief, on temp trees (brief 184c)."""
import importlib.util
import json
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[3]
spec = importlib.util.spec_from_file_location("build_lane_plan", ROOT / "project" / "tools" / "build_lane_plan.py")
blp = importlib.util.module_from_spec(spec)
spec.loader.exec_module(blp)

PAGE = "head\n  // lanes:start\n  var LANES = [];\n  // lanes:end\n  // plan:start\n  var B = [];\n  // plan:end\ntail\n"
STATUS = "# Status\n<!-- agents:start -->\n<!-- agents:end -->\nrest\n"
LANES = {"lanes": [{"id": "1", "name": "Agent 1"}, {"id": "2", "name": "Agent 2"}, {"id": "3", "name": "Agent 3"}, {"id": "E", "name": "You"}, {"id": "G", "name": "Held"}],
         "notes": {"1": "guru", "E": "author", "G": "held"}, "agent1": {"now": "reviewing", "next": "more"}}


def brief(bid="150c", title="Do a thing", status="ready", agent="2", needs="none", length=None, rows=(), extra=""):
    head = [f"# {bid[:-1]}: {title}", "", f"- **Status:** {status}", f"- **Agent:** {agent}", f"- **Needs:** {needs}"]
    if length:
        head.append(f"- **Length:** {length}")
    head += [f"- **Row:** {r}" for r in rows]
    return "\n".join(head) + f"\n\n## Goal\nDo it well. Then more text here.\n\n## Touches\n`a/b.py` and `c.md`\n{extra}\n"


def tree(tmp_path, briefs, done=()):
    for rel, text in {"project/lane-plan.html": PAGE, "project/STATUS.md": STATUS, "project/lane-plan-lanes.json": json.dumps(LANES)}.items():
        (tmp_path / rel).parent.mkdir(parents=True, exist_ok=True)
        (tmp_path / rel).write_text(text, encoding="utf-8")
    (tmp_path / "project/briefs/open").mkdir(parents=True, exist_ok=True)
    (tmp_path / "project/briefs/done").mkdir(parents=True, exist_ok=True)
    for name, text in briefs.items():
        (tmp_path / "project/briefs/open" / name).write_text(text, encoding="utf-8")
    for name in done:
        (tmp_path / "project/briefs/done" / name).write_text("done\n", encoding="utf-8")
    return tmp_path


def run(root, *args):
    return blp.main(["--root", str(root), *args])


def test_every_status_word_maps_and_draft_and_parked_read_as_hold(tmp_path):
    words = {"underway": "under", "review": "review", "ready": "ready", "author": "author", "hold": "hold", "draft": "hold", "parked": "hold"}
    files = {f"{150 + i}c-x.md": brief(f"{150 + i}c", status=f"{w}; some free text") for i, w in enumerate(words)}
    briefs, _, errors = blp.load(tree(tmp_path, files))
    assert errors == [] and {b.status for b in briefs} == set(words.values())
    assert [b.status for b in briefs] == list(words.values())


def test_unknown_status_word_is_an_error_not_a_guess(tmp_path):
    root = tree(tmp_path, {"150c-x.md": brief(status="done in part")})
    assert any("unknown status word" in e and "150c-x.md:3" in e for e in blp.problems(root))
    assert run(root) == 2


def test_needs_soft_marker_none_and_done_ids(tmp_path):
    root = tree(tmp_path, {"150c-a.md": brief("150c"), "151c-b.md": brief("151c", needs="150c, ~152c, 140c"), "152c-c.md": brief("152c")}, done=["140c-old.md"])
    briefs, done, errors = blp.load(root)
    assert errors == [] and done == {"140c"}
    assert [b for b in briefs if b.id == "151c"][0].needs == [("150c", False), ("152c", True), ("140c", False)]
    assert 'soft: true' in blp.b_array(briefs) and '140c' not in blp.b_array(briefs).split('"151c"')[1]   # a done id is met, so not drawn


def test_unknown_need_cycle_and_agent_are_errors(tmp_path):
    assert any("neither an open brief nor in done" in e for e in blp.problems(tree(tmp_path / "a", {"150c-a.md": brief(needs="999c")})))
    cyc = {"150c-a.md": brief("150c", needs="151c"), "151c-b.md": brief("151c", needs="150c")}
    assert any("cycle" in e for e in blp.problems(tree(tmp_path / "b", cyc)))
    assert any("agent" in e for e in blp.problems(tree(tmp_path / "c", {"150c-a.md": brief(agent="7")})))
    assert any("Needs" in e for e in blp.problems(tree(tmp_path / "d", {"150c-a.md": brief(needs="the other brief")})))


def test_missing_and_malformed_header_lines_name_file_and_line(tmp_path):
    root = tree(tmp_path, {"150c-a.md": "# 150: x\n\n- **Status:** ready\n\n## Goal\nx.\n", "151c-b.md": brief("151c", length="two")})
    errs = blp.problems(root)
    assert any(e.startswith("project/briefs/open/150c-a.md:1 missing header line") for e in errs)
    assert any("151c-b.md" in e and "Length" in e for e in errs)


def test_row_lines_make_extra_rows_and_bad_rows_fail(tmp_path):
    good = brief("183c", status="hold", agent="3", needs="183a", length="2", rows=["183a | agent 2 | ready | needs none | length 1 | Stage A, new files only"])
    briefs, _, errors = blp.load(tree(tmp_path / "a", {"183c-x.md": good}))
    assert errors == [] and {b.id: (b.agent, b.status, b.title) for b in briefs}["183a"] == ("2", "ready", "Stage A, new files only")
    bad = brief("183c", rows=["183a | agent 2 | ready"])
    assert any("Row line" in e for e in blp.problems(tree(tmp_path / "b", {"183c-x.md": bad})))


def test_generated_row_uses_title_goal_sentence_and_files_cut_to_60(tmp_path):
    long = "`" + "x" * 80 + "`"
    root = tree(tmp_path, {"150c-a.md": brief(title="Do a `thing`").replace("`a/b.py` and `c.md`", long)})
    b = blp.load(root)[0][0]
    assert b.title == "Do a `thing`" and b.goal == "Do it well." and len(b.touches) == 61 and b.touches.endswith("…")
    assert 't: "Do a thing"' in blp.b_array([b])


def test_first_brief_of_each_agent_leads_its_lane_and_a_held_one_waits(tmp_path):
    files = {"150c-a.md": brief("150c", status="hold", needs="151c"), "151c-b.md": brief("151c", status="ready"), "152c-c.md": brief("152c", agent="author"), "153c-d.md": brief("153c", agent="none")}
    briefs = blp.load(tree(tmp_path, files))[0]
    assert [b.id for b in blp.lane_order(briefs, "2")] == ["151c", "150c"]
    assert blp.lane_note(briefs, "2").startswith("151c (Do a thing), then 150c")
    assert [b.id for b in blp.lane_order(briefs, "E")] == ["152c"] and [b.id for b in blp.lane_order(briefs, "G")] == ["153c"]


def test_idempotent_and_check_exit_codes(tmp_path):
    root = tree(tmp_path, {"150c-a.md": brief("150c"), "151c-b.md": brief("151c", agent="3", needs="150c")})
    assert run(root, "--check") == 1                      # the markers are empty: stale
    assert run(root) == 0 and run(root, "--check") == 0
    first = {p: (root / p).read_bytes() for p in ("project/lane-plan.html", "project/STATUS.md")}
    assert run(root) == 0
    assert first == {p: (root / p).read_bytes() for p in first}   # run twice, identical bytes
    page, status = first["project/lane-plan.html"].decode(), first["project/STATUS.md"].decode()
    assert '"150c"' in page and '"151c"' in page and "| Agent 3 | 151c (Do a thing) |" in status and "| Agent 1 (guru prime) | reviewing | more |" in status
    assert page.startswith("head\n") and page.endswith("tail\n")          # nothing outside the markers moved


def test_header_edit_without_rebuild_is_red_and_changes_only_generated_parts(tmp_path):
    root = tree(tmp_path, {"150c-a.md": brief("150c")})
    run(root)
    f = root / "project/briefs/open/150c-a.md"
    f.write_text(f.read_text().replace("**Agent:** 2", "**Agent:** 3"), encoding="utf-8")
    assert run(root, "--check") == 1
    before = (root / "project/lane-plan.html").read_text()
    run(root)
    after = (root / "project/lane-plan.html").read_text()
    assert before != after and before.replace('lane: "2"', 'lane: "3"').split("// lanes:start")[0] == after.split("// lanes:start")[0]
    assert run(root, "--check") == 0


def test_a_retired_brief_leaves_the_plan_and_a_new_one_joins(tmp_path):
    root = tree(tmp_path, {"150c-a.md": brief("150c"), "151c-b.md": brief("151c")})
    run(root)
    assert '"151c"' in (root / "project/lane-plan.html").read_text()
    (root / "project/briefs/open/151c-b.md").rename(root / "project/briefs/done/151c-b.md")
    (root / "project/briefs/open/152c-c.md").write_text(brief("152c"), encoding="utf-8")
    run(root)
    page = (root / "project/lane-plan.html").read_text()
    assert '"151c"' not in page and '"152c"' in page and '"150c"' in page


def test_malformed_header_exits_2_and_leaves_files_alone(tmp_path, capsys):
    root = tree(tmp_path, {"150c-a.md": brief(status="finished")})
    assert run(root) == 2 and "150c-a.md:3" in capsys.readouterr().err
    assert (root / "project/lane-plan.html").read_text() == PAGE


def test_check_agent_docs_reports_the_same_header_problems(tmp_path):
    spec2 = importlib.util.spec_from_file_location("check_agent_docs", ROOT / "project" / "tools" / "check_agent_docs.py")
    cad = importlib.util.module_from_spec(spec2)
    spec2.loader.exec_module(cad)
    root = tree(tmp_path, {"150c-a.md": brief(needs="999c")})
    assert any("999c" in f for f in cad.check(root))


def test_the_real_tree_is_clean():
    assert blp.problems(ROOT) == []


def test_openai_agent_briefs_go_to_lane_o_and_the_table_row(tmp_path):
    root = tree(tmp_path, {"150c-x.md": brief("150c", agent="openai"), "151c-y.md": brief("151c", agent="openai", status="hold; waits", needs="150c")})
    briefs, _, errors = blp.load(root)
    fixed = json.loads((root / "project/lane-plan-lanes.json").read_text(encoding="utf-8"))
    assert errors == [] and {blp.lane_of(b) for b in briefs} == {"O"}
    table = blp.agent_table(briefs, fixed)
    assert "| OpenAI agent (notes only) | 150c (Do a thing) | 151c |" in table
    assert blp.agent_table([], fixed).endswith("| OpenAI agent (notes only) | free |  |")
