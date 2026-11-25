"""run_suites.py: each suite in its own process, failures reported, the rest still run (brief 077c). Suite: tests/hooks."""
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SCRIPT = str(ROOT / "pipeline" / "run_suites.py")


def suite(root, name, body, conftest=True):
    d = root / "tests" / name
    d.mkdir(parents=True)
    if conftest:
        (d / "conftest.py").write_text("", encoding="utf-8")
    (d / "test_x.py").write_text(body, encoding="utf-8")


def tree(tmp_path):
    suite(tmp_path, "data", "def test_a():\n    pass\n\ndef test_b():\n    pass\n")
    suite(tmp_path, "gate", "def test_boom():\n    assert 1 == 2\n\ndef test_other():\n    assert False\n")
    suite(tmp_path, "zeta", "def test_c():\n    pass\n")                 # discovered: has a conftest
    suite(tmp_path, "cards", "def test_d():\n    pass\n", conftest=False)  # named, no conftest
    suite(tmp_path, "loose", "def test_e():\n    pass\n", conftest=False)  # not named, no conftest: ignored
    return tmp_path


def run(root, *args):
    return subprocess.run([sys.executable, SCRIPT, "--root", str(root), *args], capture_output=True, text=True)


def test_list_discovers_named_suites_and_conftest_dirs(tmp_path):
    r = run(tree(tmp_path), "--list")
    assert r.returncode == 0 and r.stdout.split() == ["data", "gate", "cards", "zeta"]


def test_failing_suite_is_reported_and_the_others_still_run(tmp_path):
    r = run(tree(tmp_path))
    assert r.returncode == 1
    assert "2 passed" in next(l for l in r.stdout.splitlines() if l.startswith("data"))
    assert "1 passed" in next(l for l in r.stdout.splitlines() if l.startswith("zeta"))   # ran after gate failed
    assert "FAILED suite gate: tests/model/gate/test_x.py::test_boom, tests/model/gate/test_x.py::test_other" in r.stdout
    assert "3 of 4 suites passed; failed: gate" in r.stdout


def test_each_row_records_the_exact_command_and_exit_status(tmp_path):
    r = run(tree(tmp_path), "data", "gate")
    rows = {l.split()[0]: l for l in r.stdout.splitlines() if l.split()[:1] in (["data"], ["gate"])}
    assert "  0  " in rows["data"] and "(python -m pytest tests/model/data -q)" in rows["data"]
    assert "  1  " in rows["gate"] and "zeta" not in r.stdout


def test_all_passing_exits_zero_and_unknown_suite_exits_two(tmp_path):
    t = tree(tmp_path)
    assert run(t, "data", "zeta").returncode == 0
    bad = run(t, "nope")
    assert bad.returncode == 2 and "unknown suite(s) nope" in bad.stderr


def test_real_repo_lists_the_five_named_suites():
    r = run(ROOT, "--list")
    assert r.returncode == 0 and r.stdout.split()[:5] == ["data", "gate", "cards", "model_v3", "hooks"]
