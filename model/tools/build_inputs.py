"""
build_inputs.py: parse the model v3 input register into data/input-register/inputs.json.

Reads docs/model-v3/inputs.md (rows whose first cell starts with ``I-``),
writes data/input-register/inputs.json (generated, never edited by hand).  Brief 030c,
hooks.md sections 2 and 4.3.

Rules
- A register row must have exactly twelve cells; any other count is an error.
- A duplicate id is an error.
- Low, Central and High are numbers where the cell is a plain number.  Any
  other cell becomes an explicit null with a reason: ``not found``,
  ``bracket`` (a cell written in square brackets) or ``text`` (a qualified
  or composite value such as ``1 (listed shares)``); the raw cell is kept so
  the research lane can see what was there.
- The ``(J)`` judgement flag is read from the "How the range was set" cell.

Self-contained on purpose (no sibling imports), so it runs under ``python -I``.
Output is deterministic: register order, sorted keys inside rows, no dates.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
DEFAULT_SRC = ROOT / "docs" / "model-v3" / "inputs.md"
DEFAULT_OUT = ROOT / "data" / "input-register" / "inputs.json"

SCHEMA = "wdt-inputs/1"
N_CELLS = 12
ROW_ID = re.compile(r"^I-[A-Za-z0-9]+$")
SOURCE_ROW = re.compile(r"^\|\s*(S[A-Z]?[0-9]+[a-z]?)\s*\|")
SOURCE_ID = re.compile(r"\bS[A-Z]?[0-9]+[a-z]?\b")
NUMBER = re.compile(r"^[-+−]?(?:\d{1,3}(?:,\d{3})+|\d+)(?:\.\d+)?$")
UNESCAPED_PIPE = re.compile(r"(?<!\\)\|")

# Cell positions in the register row (the header is the same in every table;
# some tables write "Input (feeds)" for "Input").
C_ID, C_INPUT, C_UNIT, C_LOW, C_CENTRAL, C_HIGH, C_HOW, C_SOURCE = range(8)
C_LICENCE, C_COVERAGE, C_IN_REPO, C_CONFIDENCE = range(8, 12)


class RegisterError(Exception):
    pass


def split_row(line: str) -> list[str]:
    parts = UNESCAPED_PIPE.split(line.strip())
    return [p.replace("\\|", "|").strip() for p in parts[1:-1]]


def parse_value(cell: str):
    """Return (value, reason); exactly one of them is None."""
    text = cell.strip()
    if NUMBER.match(text):
        clean = text.replace(",", "").replace("−", "-")
        return (float(clean) if "." in clean else int(clean)), None
    if text.lower() == "not found":
        return None, "not found"
    if text.startswith("[") and text.endswith("]"):
        return None, "bracket"
    return None, "text"


def parse_register(text: str) -> tuple[list[dict], list[str]]:
    lines = text.splitlines()
    known_sources = {m.group(1) for ln in lines if (m := SOURCE_ROW.match(ln))}
    rows: list[dict] = []
    seen: dict[str, int] = {}
    warnings: list[str] = []
    for lineno, line in enumerate(lines, 1):
        if not re.match(r"^\|\s*I-", line):
            continue
        cells = split_row(line)
        if len(cells) != N_CELLS:
            raise RegisterError(
                f"line {lineno}: row {cells[0] if cells else '?'} has "
                f"{len(cells)} cells, expected {N_CELLS}"
            )
        rid = cells[C_ID]
        if not ROW_ID.match(rid):
            raise RegisterError(f"line {lineno}: malformed id {rid!r}")
        if rid in seen:
            raise RegisterError(
                f"line {lineno}: duplicate id {rid} (first at line {seen[rid]})"
            )
        seen[rid] = lineno

        row: dict = {
            "id": rid,
            "input": cells[C_INPUT],
            "unit": cells[C_UNIT],
            "judgement": "(J)" in cells[C_HOW],
            "sources": [],
            "coverage": cells[C_COVERAGE],
            "nulls": {},
        }
        for name, pos in (("low", C_LOW), ("central", C_CENTRAL), ("high", C_HIGH)):
            value, reason = parse_value(cells[pos])
            row[name] = value
            if reason:
                row["nulls"][name] = {"reason": reason, "raw": cells[pos]}
        for sid in SOURCE_ID.findall(cells[C_SOURCE]):
            if sid not in row["sources"]:
                row["sources"].append(sid)
        for sid in row["sources"]:
            if sid not in known_sources:
                warnings.append(f"line {lineno}: {rid} cites {sid}, not in a source table")
        rows.append(row)
    if not rows:
        raise RegisterError("no register rows found")
    return rows, warnings


def render(rows: list[dict]) -> str:
    doc = {"schema": SCHEMA, "count": len(rows), "inputs": rows}
    return json.dumps(doc, ensure_ascii=False, indent=1, sort_keys=True) + "\n"


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--src", type=Path, default=DEFAULT_SRC, help="inputs.md")
    ap.add_argument("--out", type=Path, default=DEFAULT_OUT, help="inputs.json")
    args = ap.parse_args(argv)
    try:
        rows, warnings = parse_register(args.src.read_text(encoding="utf-8"))
    except RegisterError as exc:
        print(f"build_inputs: error: {exc}", file=sys.stderr)
        return 1
    for w in warnings:
        print(f"build_inputs: warning: {w}", file=sys.stderr)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    with open(args.out, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(render(rows))
    nulls = sum(len(r["nulls"]) for r in rows)
    print(f"build_inputs: {len(rows)} inputs, {nulls} null cells -> {args.out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
