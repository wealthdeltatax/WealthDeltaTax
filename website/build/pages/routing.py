"""
pages/routing.py: reader routing data, its checks, and the data the hub cards and the
spoke Read next lines are drawn from (brief 061s; docs/restructure/site/nav.md section 4).

Reads website/registry/routing.yml and website/registry/pages.yml, and, where a spoke file exists, the
front matter of source/spokes/<ID>.md (question, status, depends, Short answer).
Writes nothing and emits no markup: output is plain data (dicts and Finding records);
markup belongs to the page-type brief (B8).

Not wired into preprocess.py (B15).  Run the checks with:
    python website/build/pages/routing.py
"""

from __future__ import annotations

import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any

if __package__ in (None, ""):                      # run as a script
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import yaml

import config as cfg

ROUTING_YML = cfg.ROOT_DIR / "registry" / "routing.yml"
SPOKES_DIR = cfg.ROOT_DIR / "source" / "spokes"

DATA_TOKEN = "data"
MAX_PROMPT_WORDS = 20
MAX_START = 5

# Data-layer pages of docs/restructure/site/ids.md section 2 (DL0 to DL6).  Used until
# B9 adds registry rows for them; nav.py reads the same list.
DATA_PAGES: list[dict[str, str]] = [
    {"id": "DL0", "title": "The data layer", "url": "/data.html"},
    {"id": "DL1", "title": "Outputs", "url": "/data/outputs.html"},
    {"id": "DL2", "title": "Input register", "url": "/data/inputs.html"},
    {"id": "DL3", "title": "Metrics", "url": "/data/metrics.html"},
    {"id": "DL4", "title": "Method", "url": "/data/method.html"},
    {"id": "DL5", "title": "Downloads and run record", "url": "/data/downloads.html"},
    {"id": "DL6", "title": "UK data pack", "url": "/data/uk-pack.html"},
]
DATA_LABEL = "The numbers"                          # card text for the `data` token (nav.md 4.3)


@dataclass(frozen=True)
class Finding:
    code: str       # R01 ... R07
    level: str      # "error" | "warning" | "info"
    message: str
    where: str = ""  # route id or page id

    def __str__(self) -> str:
        return f"{self.level.upper():7} {self.code} {self.where + ': ' if self.where else ''}{self.message}"


# ── loading ───────────────────────────────────────────────────────────────────

def load_routing(path: Path | None = None) -> list[dict[str, Any]]:
    """Read routing.yml; every route gets id, reader, prompt, start, order."""
    with (path or ROUTING_YML).open(encoding="utf-8") as fh:
        raw = yaml.safe_load(fh) or {}
    routes = []
    for r in raw.get("routes") or []:
        route = {"id": None, "reader": None, "prompt": None, "start": [], "order": None}
        route.update(r)
        route["start"] = list(route["start"] or [])
        routes.append(route)
    return routes


_FM_RE = re.compile(r"\A---\s*\n(.*?)^---\s*$\n?(.*)\Z", re.S | re.M)
_SHORT_RE = re.compile(r"^##\s+Short answer\s*$", re.I)


def read_spoke_file(path: Path) -> dict[str, Any] | None:
    """Front matter dict and body of one spoke file, or None when the file is absent or has none."""
    if not path.exists():
        return None
    m = _FM_RE.match(path.read_text(encoding="utf-8"))
    if not m:
        return None
    return {"meta": yaml.safe_load(m.group(1)) or {}, "body": m.group(2)}


def short_answer(body: str) -> str:
    """The first paragraph under a `## Short answer` heading ('' if there is none)."""
    lines = body.splitlines()
    for i, line in enumerate(lines):
        if _SHORT_RE.match(line.strip()):
            para: list[str] = []
            for nxt in lines[i + 1:]:
                if nxt.lstrip().startswith("#"):
                    break
                if nxt.strip():
                    para.append(nxt.strip())
                elif para:
                    break
            return " ".join(para)
    return ""


def spoke_infos(rows: list[dict[str, Any]], spokes_dir: Path | None = None
                ) -> tuple[dict[str, dict[str, Any]], list[Finding]]:
    """
    One info dict per spoke or appendix row: id, label, question, status, depends,
    short_answer, has_file.  Title and status come from the file's front matter
    (site.md R4).  A spoke with no file falls back to its registry label and is
    reported as information, not an error (brief 061s design 6).
    """
    spokes_dir = spokes_dir or SPOKES_DIR
    infos: dict[str, dict[str, Any]] = {}
    findings: list[Finding] = []
    for r in rows:
        if r["type"] not in cfg.SPOKE_KINDS:
            continue
        f = read_spoke_file(spokes_dir / f"{r['id']}.md")
        meta = f["meta"] if f else {}
        label = r["label"] or r["id"]
        infos[r["id"]] = {
            "id": r["id"],
            "type": r["type"],
            "label": label,
            "question": meta.get("question") or label,
            "status": meta.get("status") or "draft",
            "depends": list(meta.get("depends") or []),
            "short_answer": short_answer(f["body"]) if f else "",
            "has_file": f is not None,
        }
        if f is None:
            findings.append(Finding("I01", "info", f"no spoke file {r['id']}.md; the registry label is used", r["id"]))
    return infos, findings


# ── checks (nav.md 4.2) ───────────────────────────────────────────────────────

def _menu_spokes(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return sorted((r for r in rows if r["type"] == "spoke" and r["order"] is not None),
                  key=lambda r: r["order"])


def check_routing(routes: list[dict[str, Any]], rows: list[dict[str, Any]],
                  infos: dict[str, dict[str, Any]] | None = None) -> list[Finding]:
    """
    The five checks of nav.md 4.2 plus the field rules of 4.1.  Codes:
      R01 error    a start id is not a spoke in the registry (and not `data`)
      R02 error    a route has no reader or no start
      R03 error    a menu spoke is in no route
      R04 warning  a route includes a spoke before the spokes it depends on
      R05 error    a prompt is over 20 words or contains a digit
      R06 error    field rules: duplicate route id, start over 5 or with duplicates, bad order
    """
    infos = infos if infos is not None else spoke_infos(rows)[0]
    valid = {r["id"] for r in rows if r["type"] in cfg.SPOKE_KINDS}
    findings: list[Finding] = []
    seen_ids: set[str] = set()
    covered: set[str] = set()

    for idx, route in enumerate(routes):
        rid = route["id"] or f"#{idx + 1}"
        if not route["id"]:
            findings.append(Finding("R06", "error", "route has no id", rid))
        elif route["id"] in seen_ids:
            findings.append(Finding("R06", "error", "duplicate route id", rid))
        elif route["id"] != str(route["id"]).lower():
            findings.append(Finding("R06", "error", "route id must be lowercase", rid))
        seen_ids.add(route["id"])

        if not route["reader"]:
            findings.append(Finding("R02", "error", "route has no reader", rid))
        start = route["start"]
        if not start:
            findings.append(Finding("R02", "error", "route has an empty start list", rid))
        if len(start) > MAX_START:
            findings.append(Finding("R06", "error", f"start has {len(start)} entries; the limit is {MAX_START}", rid))
        if len(set(start)) != len(start):
            findings.append(Finding("R06", "error", "start has duplicate ids", rid))
        if route["order"] is not None and not isinstance(route["order"], int):
            findings.append(Finding("R06", "error", f"order must be an integer, got {route['order']!r}", rid))

        for sid in start:
            if sid == DATA_TOKEN:
                continue
            if sid not in valid:
                findings.append(Finding("R01", "error", f"start id {sid!r} is not a spoke in pages.yml", rid))
            else:
                covered.add(sid)

        # R04: dependencies earlier in the same route
        for i, sid in enumerate(start):
            for dep in (infos.get(sid) or {}).get("depends", []):
                if dep not in start[:i]:
                    findings.append(Finding("R04", "warning",
                                            f"{sid} comes without its dependency {dep} earlier in the route", rid))

        prompt = route["prompt"]
        if prompt:
            words = len(str(prompt).split())
            if words > MAX_PROMPT_WORDS:
                findings.append(Finding("R05", "error", f"prompt has {words} words; the limit is {MAX_PROMPT_WORDS}", rid))
            if re.search(r"\d", str(prompt)):
                findings.append(Finding("R05", "error", "prompt contains a digit", rid))

    for r in _menu_spokes(rows):
        if r["id"] not in covered:
            findings.append(Finding("R03", "error", f"menu spoke {r['id']} is in no route", r["id"]))
    return findings


def errors(findings: list[Finding]) -> list[Finding]:
    return [f for f in findings if f.level == "error"]


# ── data for the two renderers (nav.md 4.3) ───────────────────────────────────

def _hub_url(rows: list[dict[str, Any]]) -> str:
    return next((r["url"] for r in rows if r["type"] == "hub"), "/index.html")


def _link(page_id: str, rows: list[dict[str, Any]], infos: dict[str, dict[str, Any]]) -> dict[str, Any]:
    """One link: text is the spoke's question (label if no file), id is the chip."""
    if page_id == DATA_TOKEN:
        return {"id": DATA_TOKEN, "text": DATA_LABEL, "chip": None, "url": DATA_PAGES[0]["url"], "is_data": True}
    row = next(r for r in rows if r["id"] == page_id)
    info = infos.get(page_id, {})
    return {"id": page_id, "text": info.get("question") or row["label"] or page_id,
            "chip": page_id, "url": row["url"], "is_data": False}


def _ordered(routes: list[dict[str, Any]]) -> list[dict[str, Any]]:
    keyed = [((r["order"] if isinstance(r["order"], int) else i + 1), i, r) for i, r in enumerate(routes)]
    return [r for _, _, r in sorted(keyed, key=lambda t: (t[0], t[1]))]


def hub_cards(routes: list[dict[str, Any]], rows: list[dict[str, Any]],
              infos: dict[str, dict[str, Any]] | None = None) -> list[dict[str, Any]]:
    """
    The hub's routing cards: reader, prompt, and the ordered links.  The first link is
    the primary button; `data` renders as "The numbers" linking to DL0.
    """
    infos = infos if infos is not None else spoke_infos(rows)[0]
    cards = []
    for route in _ordered(routes):
        links = [_link(sid, rows, infos) for sid in route["start"]]
        for n, link in enumerate(links):
            link["primary"] = n == 0
        cards.append({"id": route["id"], "reader": route["reader"], "prompt": route["prompt"], "links": links})
    return cards


def read_next(page_id: str, routes: list[dict[str, Any]], rows: list[dict[str, Any]],
              infos: dict[str, dict[str, Any]] | None = None) -> list[dict[str, Any]]:
    """
    Read next lines for one spoke: one per route that contains it.  `next` is the entry
    after this spoke in the route's start list, or None after the last entry, when the
    line reads "Back to the hub".  `text` follows nav.md 4.3 wording.
    """
    infos = infos if infos is not None else spoke_infos(rows)[0]
    lines = []
    for route in _ordered(routes):
        start = route["start"]
        if page_id not in start:
            continue
        pos = start.index(page_id)
        nxt = _link(start[pos + 1], rows, infos) if pos + 1 < len(start) else None
        if nxt is None:
            text = f"If you are a {route['reader']}: Back to the hub"
        else:
            text = f"If you are a {route['reader']}: next, {nxt['text']}"
        lines.append({"route": route["id"], "reader": route["reader"], "next": nxt,
                      "back_to_hub": nxt is None, "hub_url": _hub_url(rows), "text": text})
    return lines


# ── script: the routing check ─────────────────────────────────────────────────

def main(argv: list[str] | None = None) -> int:
    rows = cfg.load_pages()
    page_errors = cfg.validate_pages(rows)
    routes = load_routing()
    infos, info_findings = spoke_infos(rows)
    findings = check_routing(routes, rows, infos)
    for e in page_errors:
        print(f"ERROR   pages.yml: {e}")
    for f in findings:
        print(f)
    n_info = len(info_findings)
    print(f"{len(routes)} routes; {len(errors(findings))} errors, "
          f"{sum(f.level == 'warning' for f in findings)} warnings, {n_info} spokes without a file (information)")
    return 1 if page_errors or errors(findings) else 0


if __name__ == "__main__":
    raise SystemExit(main())
