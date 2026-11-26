"""build_skills.py: archives from the stubs, byte-identical, checked by content (brief 076c). Suite: tests/project/tools."""
import hashlib
import subprocess
import sys
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
SCRIPT = str(ROOT / "project" / "tools" / "build_skills.py")
ROLES = ("wdt-code", "wdt-guru")


def tree(tmp_path):
    for r in ROLES:
        p = tmp_path / ".claude" / "skills" / r / "SKILL.md"
        p.parent.mkdir(parents=True)
        p.write_text(f"---\nname: {r}\n---\nRead `AGENTS.md`.\n", encoding="utf-8")
    return tmp_path


def run(*args, root):
    return subprocess.run([sys.executable, "-I", SCRIPT, "--root", str(root), *args], capture_output=True, text=True)


def digests(d):
    return {p.name: hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(d.glob("*.skill"))}


def test_two_builds_are_byte_identical(tmp_path):
    t = tree(tmp_path)
    assert run("--out", str(t / "a"), root=t).returncode == 0
    assert run("--out", str(t / "b"), root=t).returncode == 0
    assert digests(t / "a") == digests(t / "b") and len(digests(t / "a")) == 2


def test_unzipped_content_equals_each_stub(tmp_path):
    t = tree(tmp_path)
    run(root=t)
    for r in ROLES:
        with zipfile.ZipFile(t / "project" / "skills" / f"{r}.skill") as z:
            assert z.namelist() == [f"{r}/SKILL.md"]
            assert z.infolist()[0].date_time == (1980, 1, 1, 0, 0, 0)   # fixed timestamp
            assert z.read(f"{r}/SKILL.md") == (t / ".claude" / "skills" / r / "SKILL.md").read_bytes()


def test_check_passes_then_fails_after_a_one_character_change(tmp_path):
    t = tree(tmp_path)
    run(root=t)
    ok = run("--check", root=t)
    assert ok.returncode == 0 and ok.stdout == ""
    stub = t / ".claude" / "skills" / "wdt-guru" / "SKILL.md"
    stub.write_text(stub.read_text(encoding="utf-8").replace("Read", "Reed"), encoding="utf-8")
    bad = run("--check", root=t)
    assert bad.returncode == 1 and "stale: project/skills/wdt-guru.skill" in bad.stdout and "wdt-code" not in bad.stdout


def test_check_names_a_missing_archive_and_writes_nothing(tmp_path):
    t = tree(tmp_path)
    r = run("--check", root=t)
    assert r.returncode == 1 and "project/skills/wdt-code.skill" in r.stdout and not (t / "project" / "skills").exists()


def test_scaffold_archive_is_not_touched(tmp_path):
    t = tree(tmp_path)
    (t / "project" / "skills").mkdir(parents=True)
    (t / "project" / "skills" / "repo-scaffold.skill").write_bytes(b"keep")
    run(root=t)
    assert (t / "project" / "skills" / "repo-scaffold.skill").read_bytes() == b"keep"


def test_committed_archives_match_the_stubs():
    assert run("--check", root=ROOT).returncode == 0
