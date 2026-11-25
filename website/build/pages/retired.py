"""
pages/retired.py: the retired papers page and its data (brief 063s; site.md B10).

  python website/build/pages/retired.py --convert            one-off: ledger-sections.md -> website/registry/retired.yml
  python website/build/pages/retired.py --out FILE           write the generated page (site/pages/retired.md)

--convert reads website/notes/ledger-sections.md by paper heading and table row and writes
website/registry/retired.yml, then the file is frozen: a later --convert refuses to overwrite a file whose
`frozen` key is true.  After the first run the file is edited by hand.

--out reads website/registry/retired.yml and website/registry/pages.yml and writes the page: an explanatory
paragraph, then one table per paper (old shortcode, title, old address, successor links) with
that paper's section rows in a collapsible block.  Only section numbers and titles from the
ledger appear; no text of any legacy paper is copied.  Not wired into the build (B15).

Mapping of a ledger target to a page id (also written in the header of retired.yml):
  a spoke or appendix shortcode (FAIR, FISC, DECL, ...)   its own id
  H1, H2 (hub sections)                                    H
  glossary                                                 GLOSS
  UK data pack, input register, parameter register,
  method note for O7                                       the data-layer page DL0 if pages.yml has a
                                                           row for it; otherwise page null, target kept as text
  -                                                        page null; `reason` is the ledger Note
Rows of the three standalone papers (ADD, INST, SCOPE) are not converted: those papers stay.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from collections import defaultdict
from pathlib import Path
from typing import Any

if __package__ in (None, ""):                      # run as a script
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import yaml

import config as cfg

LEDGER_MD = cfg.ROOT_DIR / "docs" / "restructure" / "ledger-sections.md"
RETIRED_YML = cfg.ROOT_DIR / "website" / "registry" / "retired.yml"
SOURCE_DIR = cfg.ROOT_DIR / "papers" / "legacy"

DATA_TARGETS = {"UK data pack", "input register", "parameter register", "method note for O7"}
DATA_PAGE_IDS = ("DL0", "data")                    # the data-layer page, once pages.yml has a row for it
HUB_TARGET = re.compile(r"H[0-7]")
SUCCESSOR_DISPS = {"K", "M"}                       # kept and merged words decide the successor
MAX_SUCCESSORS = 3
LEDGER_STOP = "## Site pages"                      # four reader-facing pages follow the 980 rows
RETIRED_TITLE = "Where the old papers went"


class FrozenError(RuntimeError):
    """The target retired.yml is frozen; --convert will not overwrite it."""


class TieError(RuntimeError):
    """Two pages tie for a place among a paper's three successors (brief open question 3)."""


# ── ledger ────────────────────────────────────────────────────────────────────

_HEADING_RE = re.compile(r"^## (\S+) \((\d+) words\)\s*$")
_PIPE_RE = re.compile(r"(?<!\\)\|")


def parse_ledger(text: str) -> dict[str, list[dict[str, Any]]]:
    """Paper heading (the source file stem) -> its table rows, in ledger order."""
    papers: dict[str, list[dict[str, Any]]] = {}
    cur: str | None = None
    for line in text.split(LEDGER_STOP)[0].splitlines():
        m = _HEADING_RE.match(line)
        if m:
            cur = m.group(1)
            papers[cur] = []
            continue
        if cur is None or not line.startswith("| ") or line.startswith("| Sec") or line.startswith("|---"):
            continue
        cells = [c.strip().replace("\\|", "|") for c in _PIPE_RE.split(line.strip().strip("|"))]
        if len(cells) != 8:
            raise ValueError(f"{cur}: expected 8 columns, got {len(cells)}: {line[:90]}")
        sec, title, words, disp, target, _model, _demands, note = cells
        papers[cur].append({"sec": sec, "title": title, "words": int(words),
                            "disp": disp, "target": target, "note": note})
    return papers


def resolve_target(target: str, rows_by_id: dict[str, dict[str, Any]]) -> tuple[str | None, bool]:
    """
    Page id for a ledger target and whether the target is covered by the mapping.
    (None, True): resolved to nothing on purpose (`-`, or a data-layer target with no row yet).
    (None, False): not covered by the mapping at all (a question for the guru).
    """
    if target == "-":
        return None, True
    row = rows_by_id.get(target)
    if row is not None and row["type"] in cfg.SPOKE_KINDS:
        return target, True
    if HUB_TARGET.fullmatch(target):
        hub = next((r["id"] for r in rows_by_id.values() if r["type"] == "hub"), None)
        return hub, True
    if target == "glossary":
        return ("GLOSS" if "GLOSS" in rows_by_id else None), True
    if target in DATA_TARGETS:
        return next((i for i in DATA_PAGE_IDS if i in rows_by_id), None), True
    return None, False


# ── conversion ────────────────────────────────────────────────────────────────

def legacy_papers(pages: list[dict[str, Any]], ledger: dict[str, list[dict[str, Any]]]
                  ) -> list[tuple[dict[str, Any], str]]:
    """(pages.yml row, ledger heading) for the 30 retired papers, in ledger order."""
    by_source = {Path(r["source"]).stem: r for r in pages if r["type"] == "legacy" and r["source"]}
    out = []
    for heading in ledger:
        row = by_source.get(heading)
        if row is not None:
            out.append((row, heading))
    return out


def front_matter_shortcode(source: str) -> str:
    text = (cfg.ROOT_DIR / source).read_text(encoding="utf-8")
    m = re.match(r"---\s*\n(.*?)^---", text, re.S | re.M)
    return str((yaml.safe_load(m.group(1)) or {}).get("shortcode") or "") if m else ""


def successors(rows: list[dict[str, Any]], paper: str = "") -> list[str]:
    """
    The pages that receive the most kept and merged words of the paper, descending, at most
    three.  Raises TieError when two pages tie for a place inside the three (or for the third place).
    """
    words: dict[str, int] = defaultdict(int)
    for r in rows:
        if r["disp"] in SUCCESSOR_DISPS and r["page"]:
            words[r["page"]] += r["words"]
    ranked = sorted(words.items(), key=lambda kv: (-kv[1], kv[0]))
    top = ranked[:MAX_SUCCESSORS + 1]
    for (a, wa), (b, wb) in zip(top, top[1:]):
        if wa == wb:
            raise TieError(f"{paper}: {a} and {b} tie at {wa} kept and merged words")
    return [p for p, _ in ranked[:MAX_SUCCESSORS]]


def convert(pages: list[dict[str, Any]], ledger: dict[str, list[dict[str, Any]]]
            ) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    """Build the paper list and a report (counts, unresolved targets, null rows)."""
    rows_by_id = {r["id"]: r for r in pages}
    papers, unresolved = [], defaultdict(int)
    null_dropped = null_data = 0
    for row, heading in legacy_papers(pages, ledger):
        sections = []
        for r in ledger[heading]:
            page, covered = resolve_target(r["target"], rows_by_id)
            if not covered:
                unresolved[r["target"]] += 1
            if r["target"] == "-":
                null_dropped += 1
            elif page is None:
                null_data += 1
            sections.append({"sec": r["sec"], "title": r["title"], "words": r["words"], "disp": r["disp"],
                             "target": r["target"], "page": page,
                             "reason": r["note"] if r["target"] == "-" else None})
        papers.append({"id": row["id"], "shortcode": front_matter_shortcode(row["source"]),
                       "title": row["title"], "url": row["url"],
                       "successor": successors(sections, row["id"]), "sections": sections})
    report = {"papers": len(papers), "sections": sum(len(p["sections"]) for p in papers),
              "unresolved": dict(unresolved), "page_null_dropped": null_dropped,
              "page_null_unmapped": null_data}
    return papers, report


_HEADER = """\
# Where each section of the 30 retired numbered papers went (brief 063s; site.md B10).
#
# Converted once from website/notes/ledger-sections.md by `python website/build/pages/retired.py --convert`;
# frozen: a later --convert refuses to overwrite this file. Edit by hand from here on.
# Feeds the retired papers page (`python website/build/pages/retired.py --out site/pages/retired.md`).
#
# Per paper: id (the pages.yml row), shortcode and title (as the paper had them), url (the old address),
# successor (up to three page ids, descending by kept and merged words; frozen), sections.
# Per section: sec, title, words, disp (K keep, M merge, D drop, AR archive, DL data layer), target
# (the ledger's text), page (a pages.yml id or null), reason (the ledger note when the target is `-`).
#
# Mapping of a ledger target to a page id:
#   a spoke or appendix shortcode (FAIR, FISC, DECL, ...)   its own id
#   H1, H2 (hub sections)                                    H
#   glossary                                                 GLOSS
#   UK data pack, input register, parameter register,
#   method note for O7                                       the data-layer page when pages.yml has a row
#                                                            for it (none yet): page null, target kept as text
#   -                                                        page null; reason is the ledger note
# Rows of the standalone papers ADD, INST and SCOPE are not here: those papers stay.
frozen: true
"""


def _q(v: Any) -> str:
    """A YAML scalar: JSON strings are valid YAML; null and ints are bare."""
    return "null" if v is None else json.dumps(v, ensure_ascii=False)


def dump_retired(papers: list[dict[str, Any]]) -> str:
    out = [_HEADER, "papers:"]
    for p in papers:
        out.append(f"  - id: {_q(p['id'])}")
        for k in ("shortcode", "title", "url"):
            out.append(f"    {k}: {_q(p[k])}")
        out.append(f"    successor: [{', '.join(_q(s) for s in p['successor'])}]")
        out.append("    sections:")
        for s in p["sections"]:
            out.append("      - {" + ", ".join(f"{k}: {_q(s[k])}" for k in
                                                ("sec", "title", "words", "disp", "target", "page", "reason")) + "}")
        out.append("")
    return "\n".join(out)


def is_frozen(path: Path) -> bool:
    if not path.exists():
        return False
    return bool((yaml.safe_load(path.read_text(encoding="utf-8")) or {}).get("frozen"))


def run_convert(out: Path = RETIRED_YML, ledger_md: Path = LEDGER_MD,
                pages: list[dict[str, Any]] | None = None) -> dict[str, Any]:
    if is_frozen(out):
        raise FrozenError(f"{out} is frozen (frozen: true); edit it by hand")
    pages = pages if pages is not None else cfg.load_pages()
    ledger = parse_ledger(ledger_md.read_text(encoding="utf-8"))
    papers, report = convert(pages, ledger)
    report["ledger_rows_total"] = sum(len(v) for v in ledger.values())
    out.write_text(dump_retired(papers), encoding="utf-8", newline="\n")
    return report


def load_retired(path: Path = RETIRED_YML) -> list[dict[str, Any]]:
    return (yaml.safe_load(path.read_text(encoding="utf-8")) or {}).get("papers") or []


# ── the page ──────────────────────────────────────────────────────────────────

_ESC_RE = re.compile(r"([\\`*_\[\]<>$|])")


def _esc(text: str) -> str:
    return _ESC_RE.sub(r"\\\1", text)


def _page_link(page_id: str, by_id: dict[str, dict[str, Any]]) -> str:
    row = by_id[page_id]
    if row["type"] == "hub":
        text = "The hub"
    elif row["label"]:
        text = f"{page_id} {row['label']}"
    else:
        text = page_id
    return f"[{_esc(text)}]({row['url']})"


def _section_line(s: dict[str, Any], by_id: dict[str, dict[str, Any]]) -> str:
    head = f"{_esc(s['sec'])} {_esc(s['title'])}"
    if s["page"]:
        return f"- {head}: {_page_link(s['page'], by_id)}"
    if s["reason"]:
        return f"- {head}: {_esc(s['reason'])}"
    return f"- {head}: {_esc(s['target'])} (no page yet)"


def generate_page(papers: list[dict[str, Any]], pages: list[dict[str, Any]]) -> str:
    by_id = {r["id"]: r for r in pages}
    hist = by_id.get("REVHIST")
    hist_text = (f"the [revision history]({hist['url']})" if hist else "the revision history")
    lines = [
        "---",
        f'title: "{RETIRED_TITLE}"',
        'description: "Each section of the 30 retired numbered papers, with the page of the new series that took it."',
        "---",
        "",
        ("The numbered paper series that came before this site is retired. "
         "This page does not link to the old papers. "
         "Find the paper below by its old shortcode, title or address; open the section list to see which page "
         "of the new series now carries each section, or why a section was dropped or archived. "
         f"The history of the old series before publication is in {hist_text}."),
        "",
    ]
    for p in papers:
        lines += [f"## {_esc(p['shortcode'])}: {_esc(p['title'])} {{#{p['id']}}}", ""]
        succ = ", ".join(_page_link(s, by_id) for s in p["successor"]) or "None"
        lines += ["| Old shortcode | Title | Old address | Successor |",
                  "|---|---|---|---|",
                  f"| {_esc(p['shortcode'])} | {_esc(p['title'])} | `{p['url']}` | {succ} |", "",
                  "<details>", f"<summary>Sections of {_esc(p['shortcode'])} ({len(p['sections'])})</summary>", ""]
        lines += [_section_line(s, by_id) for s in p["sections"]]
        lines += ["", "</details>", ""]
    return "\n".join(lines)


def write_page(out: Path, retired: Path = RETIRED_YML) -> Path:
    pages = cfg.load_pages()
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(generate_page(load_retired(retired), pages), encoding="utf-8", newline="\n")
    return out


# ── script ────────────────────────────────────────────────────────────────────

def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="Convert the ledger once, or write the retired papers page.")
    ap.add_argument("--convert", action="store_true", help="write website/registry/retired.yml from the ledger (refuses if frozen)")
    ap.add_argument("--out", metavar="FILE", help="write the generated page to FILE")
    args = ap.parse_args(argv)
    if not (args.convert or args.out):
        ap.error("give --convert or --out FILE")
    if args.convert:
        try:
            rep = run_convert()
        except (FrozenError, TieError) as e:
            print(f"ERROR: {e}")
            return 1
        print(f"wrote {RETIRED_YML}: {rep['papers']} papers, {rep['sections']} sections of "
              f"{rep['ledger_rows_total']} ledger rows; page null: {rep['page_null_dropped']} dropped or archived, "
              f"{rep['page_null_unmapped']} data-layer targets with no page; unresolved targets: {rep['unresolved'] or 'none'}")
    if args.out:
        out = write_page(Path(args.out))
        n = sum(1 for line in out.read_text(encoding="utf-8").splitlines() if line.startswith("| Old shortcode"))
        print(f"wrote {out}: {n} papers")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
