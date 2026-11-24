"""
pages/nav.py: the new site navigation, generated from website/registry/pages.yml (brief 061s;
docs/restructure/site/nav.md sections 3, 5, 6 and 9).

  navbar(rows, infos)          the five-item navbar as data (with page ids)
  navbar_fragment(rows, infos) the same as a Quarto `website:` fragment (search moved to the navbar)
  breadcrumb(page_id, rows)    Hub > FISC, Hub > VAL > DECL
  search_description(info)     question plus the first sentence of the Short answer, at most 155 characters
  is_draft(info), menu_text    the "draft" mark for a spoke whose status is not accepted
  reachability(rows, routes)   click depth from the hub; fails past 2 clicks or when unreachable

Nothing here is wired into the build or into website/site/_quarto.yml: the live navbar stays until
cutover (B16) and preprocess.py reads this module at B15.  Write the fragment with:
    python website/build/pages/nav.py --write _build/navbar.generated.yml
Run the reachability check with:
    python website/build/pages/nav.py
"""

from __future__ import annotations

import argparse
import re
import sys
from collections import deque
from pathlib import Path
from typing import Any

if __package__ in (None, ""):                      # run as a script
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    import routing as R
else:
    from . import routing as R

import yaml

import config as cfg

DESCRIPTION_MAX = 155
MAX_CLICKS = 2
DRAFT_MARK = "draft"
CALC_HEADING = "Calculators (based on the retired model)"
PENDING_HEADING = "Pending review"

# Pages of pages.yml that the new navigation does not need to reach, with the reason.
# HOME shares the hub's URL; CORPUS retires at cutover; E404 is reached by a failed URL
# and links to the hub; legacy papers are removed at cutover (nav.md decision 5).
EXEMPT_IDS = {
    "HOME": "same URL as the hub; replaced at cutover",
    "CORPUS": "retires at cutover; not in the new navigation",
    "E404": "error page; reached by a failed URL, links to the hub",
}
EXEMPT_TYPES = {"legacy": "retired at cutover; no link from the new navigation"}


# ── helpers ───────────────────────────────────────────────────────────────────

def _href(url: str) -> str:
    """Quarto navbar hrefs are relative to the site root and have no leading slash."""
    return url.lstrip("/")


def _by_id(rows: list[dict[str, Any]]) -> dict[str, dict[str, Any]]:
    return {r["id"]: r for r in rows}


def menu_spokes(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """The menu spokes in `order`."""
    return sorted((r for r in rows if r["type"] == "spoke" and r["order"] is not None),
                  key=lambda r: r["order"])


def data_pages(rows: list[dict[str, Any]]) -> list[dict[str, str]]:
    """DL0 to DL6: registry rows of type `site`/`data` whose id starts DL when B9 adds them, else ids.md."""
    reg = [r for r in rows if re.fullmatch(r"DL[0-6]", r["id"] or "")]
    if reg:
        return [{"id": r["id"], "title": r["title"], "url": r["url"]} for r in sorted(reg, key=lambda r: r["id"])]
    return list(R.DATA_PAGES)


def is_draft(info: dict[str, Any]) -> bool:
    """True when the spoke's front-matter status is not `accepted` (nav.md section 3)."""
    return info.get("status") != "accepted"


def menu_text(row: dict[str, Any], info: dict[str, Any] | None) -> str:
    """Menu text for a spoke: 'FISC Rates and revenue', plus ' (draft)' until it is accepted."""
    text = f"{row['id']} {row['label'] or row['id']}"
    if info is not None and is_draft(info):
        text += f" ({DRAFT_MARK})"
    return text


# ── navbar ────────────────────────────────────────────────────────────────────

def _item(row: dict[str, Any], text: str | None = None) -> dict[str, str]:
    return {"text": text or row["title"], "href": _href(row["url"]), "id": row["id"]}


def navbar(rows: list[dict[str, Any]], infos: dict[str, dict[str, Any]] | None = None,
           mark_drafts: bool = True) -> list[dict[str, Any]]:
    """
    The five navbar items of nav.md section 3, each a dict with `text` and either `href` or `menu`.
    Menu entries carry an `id` (dropped by navbar_fragment).  A heading entry has `text` only.
      Questions  the 15 menu spokes in order, registry label
      Data       DL0 to DL6
      Papers     ADD, INST, SCOPE
      Resources  References, Glossary, Retired papers; Calculators group; Pending review group
      About      the author page
    """
    infos = infos if infos is not None else R.spoke_infos(rows)[0]
    by = _by_id(rows)

    questions = [{"text": menu_text(r, infos.get(r["id"]) if mark_drafts else None),
                  "href": _href(r["url"]), "id": r["id"]} for r in menu_spokes(rows)]
    data = [{"text": f"{d['id']} {d['title']}", "href": _href(d["url"]), "id": d["id"]} for d in data_pages(rows)]
    papers = [_item(by[i]) for i in ("ADD", "INST", "SCOPE") if i in by]

    resources: list[dict[str, str]] = [_item(by[i]) for i in ("REFS", "GLOSS", "RET") if i in by]
    calcs = [by[i] for i in ("CALCIDX",) if i in by] + [r for r in rows if r["type"] == "calculator"]
    if calcs:
        resources.append({"text": CALC_HEADING})
        resources.extend(_item(r) for r in calcs)
    pending = [r for r in rows if r["type"] == "pending"]
    if pending:
        resources.append({"text": PENDING_HEADING})
        resources.extend(_item(r) for r in pending)

    items: list[dict[str, Any]] = [
        {"text": "Questions", "menu": questions},
        {"text": "Data", "menu": data},
        {"text": "Papers", "menu": papers},
        {"text": "Resources", "menu": resources},
    ]
    if "ABOUT" in by:
        items.append({"text": "About", "href": _href(by["ABOUT"]["url"]), "id": "ABOUT"})
    return items


def navbar_ids(items: list[dict[str, Any]]) -> set[str]:
    """Every page id the navbar links to."""
    ids: set[str] = set()
    for it in items:
        if it.get("id"):
            ids.add(it["id"])
        for sub in it.get("menu", []):
            if sub.get("id"):
                ids.add(sub["id"])
    return ids


def navbar_fragment(rows: list[dict[str, Any]], infos: dict[str, dict[str, Any]] | None = None) -> dict[str, Any]:
    """
    A Quarto `website:` fragment: the navbar plus the search block moved to the navbar.
    Merge it under `website:` at cutover (B16); it replaces `navbar:` and `search:`.
    """
    def strip(entry: dict[str, Any]) -> dict[str, Any]:
        out = {k: v for k, v in entry.items() if k != "id"}
        if "menu" in out:
            out["menu"] = [strip(m) for m in out["menu"]]
        return out

    return {"website": {
        "search": {"location": "navbar", "type": "textbox"},
        "navbar": {"left": [strip(i) for i in navbar(rows, infos)]},
    }}


def write_navbar_fragment(path: Path, rows: list[dict[str, Any]] | None = None) -> Path:
    rows = rows if rows is not None else cfg.load_pages()
    frag = navbar_fragment(rows)
    header = ("# Generated by website/build/pages/nav.py from website/registry/pages.yml (brief 061s). Do not edit.\n"
              "# Not used by the build until cutover (B16); then it replaces website.navbar and website.search.\n")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(header + yaml.safe_dump(frag, sort_keys=False, allow_unicode=True, width=1000),
                    encoding="utf-8")
    return path


# ── breadcrumb ────────────────────────────────────────────────────────────────

def breadcrumb(page_id: str, rows: list[dict[str, Any]],
               infos: dict[str, dict[str, Any]] | None = None) -> list[dict[str, Any]]:
    """
    Breadcrumb data: Hub > FISC for a menu spoke, Hub > VAL > DECL for a parent-reached spoke.
    Each crumb: id, text (the id; "Hub" for the hub), title (the question or label), url, current.
    """
    infos = infos if infos is not None else R.spoke_infos(rows)[0]
    by = _by_id(rows)
    hub = next((r for r in rows if r["type"] == "hub"), None)
    hub_url = hub["url"] if hub else "/index.html"
    crumbs = [{"id": hub["id"] if hub else "H", "text": "Hub", "title": hub["title"] if hub else "Hub",
               "url": hub_url, "current": False}]
    if hub and page_id == hub["id"]:
        crumbs[0]["current"] = True
        return crumbs
    chain: list[str] = []
    cur = by[page_id]
    while cur is not None:
        chain.append(cur["id"])
        cur = by.get(cur["parent"]) if cur["parent"] else None
    for pid in reversed(chain):
        row = by[pid]
        info = infos.get(pid, {})
        crumbs.append({"id": pid, "text": pid, "title": info.get("question") or row["label"] or row["title"] or pid,
                       "url": row["url"], "current": False})
    crumbs[-1]["current"] = True
    return crumbs


# ── search description ────────────────────────────────────────────────────────

_SENTENCE_END = re.compile(r"(?<=[.!?])\s+")


def first_sentence(text: str) -> str:
    text = " ".join(text.split())
    return _SENTENCE_END.split(text, maxsplit=1)[0] if text else ""


def search_description(info: dict[str, Any], limit: int = DESCRIPTION_MAX) -> str:
    """
    The meta description a search result shows: the spoke's question plus the first sentence
    of its Short answer, at most `limit` characters (cut at a word boundary, ending in an ellipsis).
    A hook in the sentence reads as written; resolve hooks before this runs in the build (B15).
    """
    parts = [" ".join(str(info.get("question") or "").split()), first_sentence(info.get("short_answer") or "")]
    text = " ".join(p for p in parts if p)
    if len(text) <= limit:
        return text
    cut = text[:limit - 1].rsplit(" ", 1)[0].rstrip(" ,;:-")
    return cut + "…"


# ── reachability (nav.md section 9) ───────────────────────────────────────────

def _targets_to_check(rows: list[dict[str, Any]], data_ids: set[str],
                      exempt_ids: dict[str, str], exempt_types: dict[str, str]) -> list[str]:
    out = []
    for r in rows:
        if r["id"] in exempt_ids or r["type"] in exempt_types:
            continue
        out.append(r["id"])
    out.extend(sorted(data_ids - {r["id"] for r in rows}))
    return out


def reachability(rows: list[dict[str, Any]], routes: list[dict[str, Any]],
                 infos: dict[str, dict[str, Any]] | None = None,
                 max_clicks: int = MAX_CLICKS,
                 exempt_ids: dict[str, str] | None = None,
                 exempt_types: dict[str, str] | None = None) -> dict[str, Any]:
    """
    Click depth from the hub over the three kinds of link a reader has: the navbar (on every
    page, so every navbar target is one click from anywhere), the routing cards and Read next
    lines, and the parent link (a parent-reached spoke is reached from its parent).
    Returns {"depth": {id: clicks}, "too_far": [ids], "unreachable": [ids], "exempt": {id: reason}, "ok": bool}.
    """
    exempt_ids = EXEMPT_IDS if exempt_ids is None else exempt_ids
    exempt_types = EXEMPT_TYPES if exempt_types is None else exempt_types
    infos = infos if infos is not None else R.spoke_infos(rows)[0]
    by = _by_id(rows)
    hub = next((r["id"] for r in rows if r["type"] == "hub"), None)
    if hub is None:
        raise ValueError("pages.yml has no hub row")

    nav_ids = navbar_ids(navbar(rows, infos))
    data_ids = {d["id"] for d in data_pages(rows)}

    # adjacency: page -> pages one click away
    edges: dict[str, set[str]] = {r["id"]: set(nav_ids) for r in rows}      # the navbar is on every page
    for d in data_ids:
        edges.setdefault(d, set(nav_ids))
    edges[hub] |= {"DL0"} if "DL0" in data_ids else set()
    for card in R.hub_cards(routes, rows, infos):                          # hub routing cards
        for link in card["links"]:
            edges[hub].add("DL0" if link["is_data"] else link["id"])
    for r in rows:                                                          # parent link and Read next
        if r["parent"] and r["parent"] in edges:
            edges[r["parent"]].add(r["id"])
        if r["type"] in cfg.SPOKE_KINDS:
            for line in R.read_next(r["id"], routes, rows, infos):
                if line["next"] is not None:
                    edges[r["id"]].add("DL0" if line["next"]["is_data"] else line["next"]["id"])

    depth = {hub: 0}
    queue = deque([hub])
    while queue:
        cur = queue.popleft()
        for nxt in sorted(edges.get(cur, ())):
            if nxt not in depth:
                depth[nxt] = depth[cur] + 1
                queue.append(nxt)

    must = _targets_to_check(rows, data_ids, exempt_ids, exempt_types)
    too_far = sorted(i for i in must if i in depth and depth[i] > max_clicks)
    unreachable = sorted(i for i in must if i not in depth)
    exempt = {r["id"]: exempt_ids.get(r["id"]) or exempt_types[r["type"]]
              for r in rows if r["id"] in exempt_ids or r["type"] in exempt_types}
    return {"depth": depth, "too_far": too_far, "unreachable": unreachable, "exempt": exempt,
            "checked": len(must), "ok": not too_far and not unreachable}


# ── script ────────────────────────────────────────────────────────────────────

def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="Generate the new navbar fragment or check reachability.")
    ap.add_argument("--write", metavar="PATH", help="write the navbar fragment (YAML) to PATH")
    args = ap.parse_args(argv)

    rows = cfg.load_pages()
    errs = cfg.validate_pages(rows)
    if errs:
        for e in errs:
            print(f"ERROR pages.yml: {e}")
        return 1
    if args.write:
        out = write_navbar_fragment(Path(args.write), rows)
        print(f"wrote {out}")
    routes = R.load_routing()
    infos, _ = R.spoke_infos(rows)
    res = reachability(rows, routes, infos)
    worst = max((res["depth"][i] for i in res["depth"] if i not in res["exempt"]), default=0)
    print(f"reachability: {res['checked']} pages checked, longest path {worst} clicks, "
          f"{len(res['too_far'])} too far, {len(res['unreachable'])} unreachable, {len(res['exempt'])} exempt")
    for i in res["too_far"]:
        print(f"ERROR too far: {i} is {res['depth'][i]} clicks from the hub (limit {MAX_CLICKS})")
    for i in res["unreachable"]:
        print(f"ERROR unreachable: {i}")
    return 0 if res["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
