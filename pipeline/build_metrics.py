"""
build_metrics.py: parse the model v3 metric register into registry/metrics.json
and cross-check it against the output manifest.

Reads docs/model-v3/metrics.md and docs/model-v3/outputs.yml, writes
registry/metrics.json (generated, never edited by hand).  Brief 030c,
hooks.md sections 2 and 4.6.

Each metric row gives: id, name, section, the register's unit text and the
unit tags it maps to, and the horizon text and the windows it names.  The
register writes units as free text ("% per year; share of payers"); a fixed
table (UNIT_RULES) maps each piece to a manifest unit tag.  A metric can map
to several tags because one metric can be reported in several forms.

Cross-check against outputs.yml (exit status 1 when any error is found; the
JSON is written either way):
- every ``metric:`` id is a register id or the head of a family (B1 for
  B1a to B1d); every ``lines:`` id is a register id (a line with no id is a
  warning);
- every manifest ``unit:`` tag is declared in ``unit_tags``, a unit map has
  a key for each line and no other, and the tag is one the register's unit
  text maps to for that metric.  A metric whose register text states no unit
  cannot be checked: warning.
- horizons are compared where the register states them (the manifest windows
  must be among the register's): warning only.

Self-contained on purpose (no sibling imports), so it runs under ``python -I``.
Output is deterministic: register order, sorted keys, no dates.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
DEFAULT_SRC = ROOT / "docs" / "model-v3" / "metrics.md"
DEFAULT_MANIFEST = ROOT / "docs" / "model-v3" / "outputs.yml"
DEFAULT_OUT = ROOT / "registry" / "metrics.json"

SCHEMA = "wdt-metrics/1"
ID_RE = re.compile(r"^[A-Z]+[0-9]+[a-z]?$")
UNESCAPED_PIPE = re.compile(r"(?<!\\)\|")
ALL_WINDOWS = ["transition", "short", "long"]

# Register unit text (one piece, lower case) to manifest unit tag.  Ordered:
# the first rule that matches wins.  A piece no rule matches is kept in
# ``unit_unmapped`` and never guessed.
UNIT_RULES: list[tuple[re.Pattern, str]] = [
    (re.compile(r"% of gdp"), "pct_gdp"),
    (re.compile(r"£bn"), "gbp_bn"),
    (re.compile(r"% per year"), "pct_per_year"),
    (re.compile(r"^%( of (payers|paths|adults|refunds due))?$"), "pct"),
    (re.compile(r"^share of (payers|paths)$"), "pct"),
    (re.compile(r"^points of gdp"), "pp"),
    (re.compile(r"percentage points"), "pp"),
    (re.compile(r"basis points"), "bp"),
    (re.compile(r"^pounds per month$"), "gbp_month"),
    (re.compile(r"^ratio$"), "ratio"),
    (re.compile(r"^alpha$"), "ratio"),   # alpha is a plain number: "number alone"
    (re.compile(r"^count$"), "count"),
]


class RegisterError(Exception):
    pass


def split_cells(line: str) -> list[str]:
    parts = UNESCAPED_PIPE.split(line.strip())
    return [p.replace("\\|", "|").strip() for p in parts[1:-1]]


def clean(text: str) -> str:
    return text.replace("**", "").strip()


def map_units(text: str | None) -> tuple[list[str], list[str]]:
    """Return (tags in order, unmapped pieces)."""
    tags: list[str] = []
    unmapped: list[str] = []
    if not text:
        return tags, unmapped
    for piece in (p.strip().lower() for p in re.split(r";| and ", text)):
        if not piece:
            continue
        for rx, tag in UNIT_RULES:
            if rx.search(piece):
                if tag not in tags:
                    tags.append(tag)
                break
        else:
            unmapped.append(piece)
    return tags, unmapped


def parse_horizon(text: str | None) -> tuple[list[str] | None, str | None]:
    """Return (windows, same_as).  windows is None when the text states none."""
    if not text:
        return None, None
    low = text.lower()
    m = re.match(r"^as ([A-Z]+[0-9]+[a-z]?)$", text.strip())
    if m:
        return None, m.group(1)
    m = re.match(r"^the ([A-Z]+[0-9]+[a-z]?) horizon$", text.strip())
    if m:
        return None, m.group(1)
    if "one life" in low or "one year" in low or "holding period" in low:
        return ["single"], None
    found = [w for w in ALL_WINDOWS if re.search(rf"\b{w}\b", low)]
    return (found or None), None


def parse_register(text: str) -> tuple[list[dict], list[tuple[str, str, str]]]:
    findings: list[tuple[str, str, str]] = []
    metrics: list[dict] = []
    seen: dict[str, int] = {}
    section = ""
    header: list[str] | None = None
    for lineno, line in enumerate(text.splitlines(), 1):
        if line.startswith("#"):
            section = line.lstrip("#").strip()
            header = None
            continue
        if not line.startswith("|"):
            continue
        cells = split_cells(line)
        if not cells or set(cells[0]) <= set("-: "):
            continue
        if cells[0] == "ID":
            header = cells
            continue
        if header is None or "Name" not in header or not ID_RE.match(cells[0]):
            continue   # a table that is not a metric table (data facts) or no header
        n = len(header)
        if len(cells) < n:
            raise RegisterError(
                f"line {lineno}: row {cells[0]} has {len(cells)} cells, header has {n}"
            )
        if len(cells) > n:
            # An unescaped pipe inside a cell (M7 writes |C.1|).  The columns after
            # Definition are fixed, so rejoin the surplus into Definition.
            tail = n - 3
            head = cells[:2]
            rest = cells[2:]
            definition = "|".join(rest[: len(rest) - tail]) if tail else "|".join(rest)
            cells = head + [definition] + (rest[len(rest) - tail:] if tail else [])
            findings.append((
                "warning", "X10",
                f"line {lineno}: {cells[0]} has an unescaped '|' in its Definition; "
                f"rejoined by position (write \\| or reword in metrics.md)",
            ))
        row = dict(zip(header, cells))
        mid = cells[0]
        if mid in seen:
            raise RegisterError(f"line {lineno}: duplicate metric id {mid} (first at line {seen[mid]})")
        seen[mid] = lineno
        name = clean(row["Name"])
        unit_text = clean(row["Unit"]) if row.get("Unit") else None
        horizon_text = clean(row["Horizon"]) if row.get("Horizon") else None
        tags, unmapped = map_units(unit_text)
        windows, same_as = parse_horizon(horizon_text)
        metrics.append({
            "id": mid,
            "name": name,
            "section": section,
            "status": "dropped" if name.lower().startswith("(dropped") else "active",
            "unit_text": unit_text,
            "unit_tags": tags,
            "unit_unmapped": unmapped,
            "horizon_text": horizon_text,
            "horizons": windows,
            "horizon_same_as": same_as,
        })
        if unmapped:
            findings.append((
                "warning", "X12",
                f"{mid}: unit text piece(s) with no tag: {', '.join(repr(u) for u in unmapped)}",
            ))
    if not metrics:
        raise RegisterError("no metric rows found")
    resolve_horizons(metrics)
    return metrics, findings


def resolve_horizons(metrics: list[dict]) -> None:
    by_id = {m["id"]: m for m in metrics}
    for m in metrics:
        seen = {m["id"]}
        cur = m
        while cur["horizons"] is None and cur["horizon_same_as"]:
            ref = cur["horizon_same_as"]
            if ref in seen or ref not in by_id:
                break
            seen.add(ref)
            cur = by_id[ref]
        if m["horizons"] is None and cur is not m:
            m["horizons"] = cur["horizons"]


def manifest_horizons(entry: dict) -> list[str]:
    h = entry.get("horizons")
    return list(h) if h else list(ALL_WINDOWS)


def cross_check(metrics: list[dict], manifest: dict) -> list[tuple[str, str, str]]:
    f: list[tuple[str, str, str]] = []
    by_id = {m["id"]: m for m in metrics}
    declared_tags = set((manifest.get("unit_tags") or {}).keys())
    entries = list(manifest.get("outputs") or []) + list(manifest.get("checks") or [])
    cited: set[str] = set()

    def exists(mid: str) -> bool:
        return mid in by_id

    def family(mid: str) -> bool:
        return any(re.fullmatch(re.escape(mid) + r"[a-z]", k) for k in by_id)

    for e in entries:
        oid = e["id"]
        raw = e.get("metric")
        if raw is None:
            continue   # data facts carry no metric
        mids = raw if isinstance(raw, list) else [raw]
        for mid in mids:
            cited.add(mid)
            if not exists(mid) and not family(mid):
                f.append(("error", "X01", f"{oid}: metric {mid} is not in the metric register"))
        lines = list(e.get("lines") or [])
        if not lines:
            lines = [m for m in mids if exists(m)]
        for ln in lines:
            cited.add(ln)
            if not exists(ln) and ln not in mids:
                f.append(("warning", "X03", f"{oid}: line {ln} has no metric id in the register"))

        unit = e.get("unit")
        if isinstance(unit, dict):
            extra = sorted(set(unit) - set(lines))
            missing = sorted(set(lines) - set(unit))
            if extra or missing:
                f.append(("error", "X07",
                          f"{oid}: unit map keys differ from lines (missing {missing}, extra {extra})"))
        for ln in lines:
            tag = unit.get(ln) if isinstance(unit, dict) else unit
            if tag is None:
                continue
            if tag not in declared_tags:
                f.append(("error", "X04", f"{oid} {ln}: unit {tag!r} is not in the manifest unit_tags"))
                continue
            rec = by_id.get(ln) or (by_id.get(mids[0]) if len(mids) == 1 else None)
            if rec is None:
                continue
            if not rec["unit_tags"]:
                f.append(("warning", "X06",
                          f"{oid} {ln}: manifest unit {tag}; the register states no unit for {rec['id']}"))
            elif tag not in rec["unit_tags"]:
                f.append(("error", "X05",
                          f"{oid} {ln}: manifest unit {tag} but the register's unit for {rec['id']} "
                          f"is {rec['unit_text']!r} ({', '.join(rec['unit_tags'])})"))
            want = manifest_horizons(e)
            reg = rec["horizons"]
            if reg is not None and not set(want) <= set(reg):   # an output may report fewer windows
                f.append(("warning", "X08",
                          f"{oid} {ln}: manifest horizons {want} but the register states "
                          f"{rec['horizon_text']!r} for {rec['id']} ({reg})"))

    for m in metrics:
        if m["status"] == "active" and not m["section"].startswith("Check") and m["id"] not in cited:
            f.append(("warning", "X09", f"{m['id']}: in the register, cited by no output"))
    return f


def render(metrics: list[dict]) -> str:
    doc = {"schema": SCHEMA, "count": len(metrics), "metrics": metrics}
    return json.dumps(doc, ensure_ascii=False, indent=1, sort_keys=True) + "\n"


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--src", type=Path, default=DEFAULT_SRC, help="metrics.md")
    ap.add_argument("--manifest", type=Path, default=DEFAULT_MANIFEST, help="outputs.yml")
    ap.add_argument("--out", type=Path, default=DEFAULT_OUT, help="metrics.json")
    args = ap.parse_args(argv)
    try:
        metrics, findings = parse_register(args.src.read_text(encoding="utf-8"))
        manifest = yaml.safe_load(args.manifest.read_text(encoding="utf-8"))
    except (RegisterError, yaml.YAMLError, OSError) as exc:
        print(f"build_metrics: error: {exc}", file=sys.stderr)
        return 1
    findings += cross_check(metrics, manifest)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    with open(args.out, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(render(metrics))
    for level, code, msg in findings:
        print(f"build_metrics: {level} {code}: {msg}", file=sys.stderr)
    errors = sum(1 for lv, _, _ in findings if lv == "error")
    warns = len(findings) - errors
    print(f"build_metrics: {len(metrics)} metrics, {errors} errors, {warns} warnings -> {args.out}")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
