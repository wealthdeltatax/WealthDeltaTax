"""check_agent_docs.py: one test per rule, on temp trees (brief 075c). Suite: tests/project/tools (no tests/scaffold exists)."""
import importlib.util
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
SCRIPT = ROOT / "project" / "tools" / "check_agent_docs.py"
spec = importlib.util.spec_from_file_location("check_agent_docs", SCRIPT)
cad = importlib.util.module_from_spec(spec)
spec.loader.exec_module(cad)

SKILL = "---\nname: wdt-code\n---\nRead `AGENTS.md`, then `project/agents/agent-code.md`.\n"


def tree(tmp_path, files=None):
    base = {
        "AGENTS.md": "rules\n",
        "project/START_HERE.md": "start\n",
        "project/agents/agent-code.md": "code guide\n",
        "project/agents/reference/x.md": "ref\n",
        ".claude/skills/wdt-code/SKILL.md": SKILL,
    }
    base.update(files or {})
    for rel, text in base.items():
        p = tmp_path / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(text, encoding="utf-8")
    return tmp_path


def test_clean_tree_passes(tmp_path):
    assert cad.check(tree(tmp_path)) == []


def test_rule1_broken_link_fails_and_good_links_pass(tmp_path):
    t = tree(tmp_path, {"project/agents/agent-guru.md": "[a](reference/x.md) [b](https://e.org/x) [c](#top) [d](reference/x.md#h)\n[e](reference/gone.md)\n"})
    assert cad.check(t) == ["project/agents/agent-guru.md:2 broken link reference/gone.md"]


def test_rule1_anchor_link_to_missing_file_fails(tmp_path):
    t = tree(tmp_path, {"AGENTS.md": "[a](docs/nope.md#sec)\n"})
    assert len(cad.check(t)) == 1


def test_rule2_missing_backticked_path_fails(tmp_path):
    t = tree(tmp_path, {"project/agents/agent-guru.md": "see `docs/missing.md` and `scripts/run.py`\n"})
    out = cad.check(t)
    assert [o.split(" ")[0] for o in out] == ["project/agents/agent-guru.md:1"] * 2 and "docs/missing.md" in out[0]


def test_rule2_root_relative_and_file_relative_both_resolve(tmp_path):
    t = tree(tmp_path, {"project/agents/agent-guru.md": "`reference/x.md` `project/agents/reference/x.md` `project/agents/reference/`\n"})
    assert cad.check(t) == []


def test_rule2_allow_list_and_non_paths_are_skipped(tmp_path):
    line = "`_build/` `_site/a.html` `website/registry/anchors.yml` `project/briefs/open/NNNx-slug.md` `a/<role>/b.md` `src/*.py` `origin/main` `brief/NNN-slug` `https://e.org/a.md` `project/tools/x`\n"
    assert cad.check(tree(tmp_path, {"project/agents/agent-guru.md": line})) == []


def test_rule3_skill_pointing_at_a_missing_guide_fails(tmp_path):
    t = tree(tmp_path, {".claude/skills/wdt-web/SKILL.md": "Read `AGENTS.md`, then `project/agents/agent-web.md`.\n"})
    out = cad.check(t)
    assert any("guide project/agents/agent-web.md does not exist" in o for o in out)


def test_rule3_skill_without_agents_or_guide_fails(tmp_path):
    t = tree(tmp_path, {".claude/skills/wdt-code/SKILL.md": "Do things. See `project/agents/change-report.md`.\n"})
    out = cad.check(t)
    assert any("does not name AGENTS.md" in o for o in out) and any("names no project/agents guide" in o for o in out)


def test_cli_exit_status_and_real_repo_is_clean(tmp_path):
    t = tree(tmp_path, {"AGENTS.md": "[a](gone.md)\n"})
    run = lambda root: subprocess.run([sys.executable, "-I", str(SCRIPT), "--root", str(root)], capture_output=True, text=True)
    bad = run(t)
    assert bad.returncode == 1 and "AGENTS.md:1 broken link gone.md" in bad.stdout
    assert run(ROOT).returncode == 0


def test_a_binary_research_file_without_a_reading_copy_is_a_warning_not_an_error(tmp_path, capsys):
    tree(tmp_path, {"data/x/a.pdf": "pdf", "data/x/b.csv": "text", "data/x/c.rtf": "rtf", "literature/readable/data/x/c.rtf.md": "copy", "literature/l.pdf": "pdf"})
    assert cad.main(["--root", str(tmp_path)]) == 0
    err = capsys.readouterr().err
    assert "warning: no reading copy for data/x/a.pdf" in err and "warning: no reading copy for literature/l.pdf" in err and "b.csv" not in err and "c.rtf" not in err
    (tmp_path / "literature/readable/data/x/a.pdf.md").write_text("copy"); (tmp_path / "literature/readable/l.pdf.md").write_text("copy")
    assert cad.main(["--root", str(tmp_path)]) == 0 and capsys.readouterr().err == ""
