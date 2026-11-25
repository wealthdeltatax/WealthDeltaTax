"""
build_skills.py: build project/skills/wdt-<role>.skill from .claude/skills/wdt-<role>/SKILL.md (brief 076c).

    python -I project/tools/build_skills.py [--check] [--root DIR] [--out DIR]

Each archive is a zip holding one entry, wdt-<role>/SKILL.md, with a fixed timestamp
and fixed attributes, so a rerun is byte-identical. --check rebuilds in memory and
compares the unzipped entries (not the zip bytes) with the committed archives; it
names each stale or missing one and exits 1. project/skills/repo-scaffold.skill is not touched.
"""
from __future__ import annotations

import argparse
import io
import sys
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def stubs(root: Path) -> list[Path]:
    return sorted((root / ".claude" / "skills").glob("wdt-*/SKILL.md"))


def entries(stub: Path) -> dict[str, bytes]:
    return {f"{stub.parent.name}/SKILL.md": stub.read_bytes()}


def build(stub: Path) -> bytes:
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w", zipfile.ZIP_DEFLATED) as z:
        for name, data in sorted(entries(stub).items()):
            info = zipfile.ZipInfo(name, date_time=(1980, 1, 1, 0, 0, 0))
            info.compress_type, info.create_system, info.external_attr = zipfile.ZIP_DEFLATED, 3, 0o100644 << 16
            z.writestr(info, data)
    return buf.getvalue()


def unzipped(path: Path) -> dict[str, bytes] | None:
    try:
        with zipfile.ZipFile(path) as z:
            return {i.filename: z.read(i) for i in z.infolist()}
    except (OSError, zipfile.BadZipFile):
        return None


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--check", action="store_true", help="compare unzipped content, write nothing")
    ap.add_argument("--root", type=Path, default=ROOT)
    ap.add_argument("--out", type=Path, help="write archives here (default: <root>/project/skills)")
    args = ap.parse_args(argv)
    out = args.out or args.root / "project" / "skills"
    found = stubs(args.root)
    if not found:
        print("build_skills: no stubs under .claude/skills/wdt-*/", file=sys.stderr)
        return 1
    stale = []
    for stub in found:
        target = out / f"{stub.parent.name}.skill"
        if args.check:
            if unzipped(target) != entries(stub):
                stale.append(target)
                print(f"stale: {target.relative_to(args.root) if target.is_relative_to(args.root) else target}")
        else:
            out.mkdir(parents=True, exist_ok=True)
            target.write_bytes(build(stub))
            print(f"wrote {target}")
    return 1 if stale else 0


if __name__ == "__main__":
    sys.exit(main())
