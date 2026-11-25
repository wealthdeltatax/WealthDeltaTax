"""
run_suites.py: run each test suite in its own pytest process (brief 077c).

    python model/tools/run_suites.py [SUITE ...] [--list] [--root DIR]

The conftests of the suites clash in one pytest session, so each tests/<dir> runs as
`python -m pytest tests/<dir> -q` in its own subprocess. Suites: data, gate, cards,
model_v3, hooks (when present) plus every other tests/<dir> that has a conftest.py.
All selected suites run even after a failure; a table shows the command, exit status
and last output line, and a failed suite lists its first failing tests. Exit 1 if any
suite failed, 2 for an unknown suite name. Expectations are never changed or combined.
"""
from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
NAMED = ("data", "gate", "cards", "model_v3", "hooks")
SHOW_FAILED = 5


def discover(root: Path) -> list[str]:
    tests = root / "tests"
    if not tests.is_dir():
        return []
    named = [n for n in NAMED if (tests / n).is_dir()]
    extra = sorted(d.name for d in tests.iterdir() if d.is_dir() and d.name not in NAMED and (d / "conftest.py").is_file())
    return named + extra


def run_suite(root: Path, name: str) -> dict:
    cmd = [sys.executable, "-m", "pytest", f"tests/{name}", "-q"]
    proc = subprocess.run(cmd, cwd=root, capture_output=True, text=True)
    lines = [ln for ln in proc.stdout.splitlines() if ln.strip()]
    failed = [ln.split(" ")[1] for ln in lines if ln.startswith(("FAILED ", "ERROR ")) and len(ln.split(" ")) > 1]
    return {
        "name": name, "cmd": " ".join(["python", "-m", "pytest", f"tests/{name}", "-q"]),
        "code": proc.returncode, "last": lines[-1] if lines else "(no output)", "failed": failed,
    }


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("suites", nargs="*", help="suite names (default: all)")
    ap.add_argument("--list", action="store_true", help="print the suites and exit")
    ap.add_argument("--root", type=Path, default=ROOT)
    args = ap.parse_args(argv)
    available = discover(args.root)
    if args.list:
        print("\n".join(available))
        return 0
    unknown = [s for s in args.suites if s not in available]
    if unknown:
        print(f"run_suites: unknown suite(s) {', '.join(unknown)}; available: {', '.join(available)}", file=sys.stderr)
        return 2
    results = [run_suite(args.root, n) for n in (args.suites or available)]
    width = max((len(r["name"]) for r in results), default=5)
    print(f"{'suite':<{width}}  exit  result  (command)")
    for r in results:
        print(f"{r['name']:<{width}}  {r['code']:>4}  {r['last']}  ({r['cmd']})")
    for r in results:
        if r["code"]:
            shown = r["failed"][:SHOW_FAILED]
            more = f" (+{len(r['failed']) - SHOW_FAILED} more)" if len(r["failed"]) > SHOW_FAILED else ""
            print(f"FAILED suite {r['name']}: {', '.join(shown) or 'no test names in the output'}{more}")
    bad = [r["name"] for r in results if r["code"]]
    print(f"{len(results) - len(bad)} of {len(results)} suites passed" + (f"; failed: {', '.join(bad)}" if bad else ""))
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
