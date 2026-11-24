#!/usr/bin/env python3
"""
wdt_crosslinks.py - section-to-section crosslink index for the WDT paper series.

Scrapes every .md under --source, builds a section index from the headings, extracts
every crosslink (WP §3.5), (GOV.B §G), (VAL), [GOV], bare §3.1 and "Section 3.1",
and validates each one against (a) the headings actually in /source, (b) anchors.yml
and (c) internal.json.

  scan   write crosslinks.json (links, section index, inbound index, issues)
  check  print issues; exit 1 if any error (CI-friendly)
  query  who links to / from a section:  --to WFR§4.2   --from MF§3
  contents  emit contents.yml-shaped data from the headings (diff against registry/contents.yml)
  anchors   emit anchors from the headings (cross-check for build_anchors.py)
  remap  rewrite links after renumbering, from a map file (dry run unless --apply)

Examples
  python pipeline/wdt_crosslinks.py scan             # -> registry/crosslinks.json
  python pipeline/wdt_crosslinks.py check
  python pipeline/wdt_crosslinks.py query --to CLOSE§5
  python pipeline/wdt_crosslinks.py remap --map renumber.yml          # preview
  python pipeline/wdt_crosslinks.py remap --map renumber.yml --apply

Default paths (relative to wdt-site/): source/ (else /source), registry/anchors.yml,
registry/internal.json; output registry/crosslinks.json. Each can be overridden by flag.

Drift tracking: scan/check compare the section index with a baseline (default: the
previous --out file). Titles that changed under an existing number, or numbers that
vanished, are reported against every link pointing at them. To compare against the
last commit:  git show HEAD:registry/crosslinks.json > /tmp/base.json ; ... --baseline /tmp/base.json
"""
from __future__ import annotations

import argparse
import json
import unicodedata
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

# --------------------------------------------------------------------------- paths
# Script lives in wdt-site/pipeline/, so the site root is one level up.
ROOT = Path(__file__).resolve().parent.parent
DEFAULT_OUT = ROOT / "registry" / "crosslinks.json"


def first_existing(*cands):
    return next((Path(c) for c in cands if c and Path(c).exists()), None)


# --------------------------------------------------------------------------- loaders


def load_kv(path):
    """anchors.yml (flat `KEY: value`) or anchors.json -> dict. No PyYAML needed."""
    p = Path(path) if path else None
    if not p or not p.exists():
        return {}
    txt = p.read_text(encoding="utf-8")
    if p.suffix == ".json":
        return json.loads(txt)
    out = {}
    for ln in txt.splitlines():
        ln = ln.strip()
        if ln and not ln.startswith("#") and ": " in ln:
            k, v = ln.split(": ", 1)
            out[k.strip().strip("'\"")] = v.strip().strip("'\"")
    return out


def load_json(path):
    p = Path(path) if path else None
    return json.loads(p.read_text(encoding="utf-8")) if p and p.exists() else {}


# --------------------------------------------------------------------------- headings

HEAD_RE = re.compile(r"^(#{1,6})\s+(.*?)\s*$")
ATTR_RE = re.compile(r"\s*\{[^}]*\}\s*$")
NUM_RE = re.compile(
    r"^(?P<num>\d+(?:\.\d+)*|[A-Z](?:\.\d+)+|[A-Z](?=\.\s)|[J-Z](?=\s+[A-Z]))\.?\s+(?P<title>.*)$"
)
REGIONS = {
    "revision-history": "revision_history",
    "abstract": "abstract",
    "glossary": "glossary",
    "registry": "registry",
}


def slugify(text):
    """Pandoc/Quarto auto-identifier (what anchors.yml records)."""
    t = ATTR_RE.sub("", text)
    t = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", t).lower()
    t = unicodedata.normalize("NFKD", t).encode("ascii", "ignore").decode()
    t = re.sub(r"[^\w\s.\-]", "", t)
    t = re.sub(r"\s+", "-", t.strip())
    return re.sub(r"^[\W\d_]+", "", t)


def parse_heading(raw):
    unnumbered = ".unnumbered" in raw
    text = ATTR_RE.sub("", raw).strip()
    m = NUM_RE.match(text)
    if m and not unnumbered:
        return m["num"], m["title"].strip(), text
    return None, text, text


def read_papers(source):
    papers = {}
    for f in sorted(Path(source).rglob("*.md")):
        lines = f.read_text(encoding="utf-8").split("\n")
        code, fm_end = None, 0
        if lines and lines[0].strip() == "---":
            for j in range(1, len(lines)):
                if lines[j].strip() == "---":
                    fm_end = j + 1
                    break
            for ln in lines[1 : max(fm_end - 1, 1)]:
                m = re.match(r"shortcode:\s*[\"']?([^\"'#\s]+)", ln)
                if m:
                    code = m.group(1)
        if not code:
            print(f"warning: {f.name} has no shortcode in front matter - skipped", file=sys.stderr)
            continue
        if code in papers:
            print(f"warning: duplicate shortcode {code} ({f.name}) - skipped", file=sys.stderr)
            continue
        heads, fence = [], False
        for n, ln in enumerate(lines, 1):
            if n <= fm_end:
                continue
            if ln.lstrip().startswith(("```", "~~~")):
                fence = not fence
                continue
            hm = None if fence else HEAD_RE.match(ln)
            if hm:
                num, title, full = parse_heading(hm.group(2))
                heads.append(dict(line=n, level=len(hm.group(1)), num=num, title=title,
                                  slug=slugify(full), has_math="$" in full))
        papers[code] = dict(path=f, lines=lines, fm_end=fm_end, headings=heads)
    return papers


# --------------------------------------------------------------------------- link extraction


class Patterns:
    def __init__(self, codes):
        alt = "|".join(sorted((re.escape(c) for c in codes), key=len, reverse=True))
        code = r"(?<![A-Za-z0-9.])(?:" + alt + r")(?![A-Za-z0-9])"
        sec = r"(?:\d+|[A-Z])(?:\.\d+)*(?![A-Za-z0-9])"
        self.token = re.compile(r"(?:(?P<code>" + code + r")\s*)?§\s*(?P<sec>" + sec + ")")
        self.papers_only = re.compile(
            r"\s*(?:" + code + r")(?:\s*(?:,|;|and|&)\s*(?:" + code + r"))*\s*")
        self.code_find = re.compile(code)
        self.prose = re.compile(r"\b[Ss]ections?\s+(?P<sec>\d{1,2}(?:\.\d+)*)(?!\d)")
        self.groups = (("paren", re.compile(r"\(([^()]*)\)")),
                       ("bracket", re.compile(r"\[([^\[\]]*)\](?![(:\[])")))


def extract(line, P, prose=True):
    out, consumed = [], []
    for form, rx in P.groups:
        for m in rx.finditer(line):
            inner, off = m.group(1), m.start(1)
            if inner.startswith("@"):
                continue
            toks = list(P.token.finditer(inner))
            found = bool(toks)
            cur = None
            for t in toks:
                own = t.group("code")
                cur = own or cur
                out.append(dict(form=form, tcode=own or cur, tsec=t.group("sec"),
                                span=(off + t.start(), off + t.end()), has_code=bool(own),
                                raw=t.group(0)))
            if not toks and P.papers_only.fullmatch(inner):
                found = True
                for c in P.code_find.finditer(inner):
                    out.append(dict(form=form + "_paper", tcode=c.group(0), tsec=None,
                                    span=(off + c.start(), off + c.end()), has_code=True,
                                    raw=c.group(0)))
            if found:
                consumed.append((m.start(), m.end()))

    def free(s, e):
        return not any(s < ce and e > cs for cs, ce in consumed)

    for t in P.token.finditer(line):
        if free(*t.span()):
            out.append(dict(form="inline" if t.group("code") else "bare", tcode=t.group("code"),
                            tsec=t.group("sec"), span=t.span(), has_code=bool(t.group("code")),
                            raw=t.group(0)))
    if prose:
        for t in P.prose.finditer(line):
            if free(*t.span()):
                out.append(dict(form="prose", tcode=None, tsec=t.group("sec"), span=t.span("sec"),
                                has_code=False, raw=t.group(0)))
    out.sort(key=lambda d: d["span"][0])
    for a, b in zip(out, out[1:]):  # "(X §9.4.1) through (X §9.4.9)"
        gap = line[a["span"][1] : b["span"][0]].strip("()[] \t").lower()
        if gap in ("to", "through", "-", "\u2013", "\u2014"):
            a["range"], b["range"] = "start", "end"
    return out


def context(line, s, e, cap=400):
    a = line.rfind(". ", 0, s)
    a = 0 if a < 0 else a + 2
    b = line.find(". ", e)
    b = len(line) if b < 0 else b + 1
    if b - a > cap:
        a, b = max(0, s - cap // 2), min(len(line), e + cap // 2)
    return re.sub(r"\s+", " ", line[a:b]).strip(" |")


# --------------------------------------------------------------------------- scan


def disp(key):
    return key.replace("§", " §")


def norm(t):
    return re.sub(r"\s+", " ", t).strip().casefold()


def scan(source, anchors, internal, baseline, prose=True):
    papers = read_papers(source)
    reg = {p["id"]: p for p in internal.get("internal_papers", [])}
    codes = set(papers) | set(reg) | {k.split("§")[0] for k in anchors}
    P = Patterns(codes)
    issues = []

    def issue(sev, typ, link, detail):
        s = link["src"]
        issues.append(dict(severity=sev, type=typ, link_id=link["id"],
                           src=f"{s['paper']} §{s['section']}" if s["section"] else s["paper"],
                           target=disp(link["target"]["key"]), where=f"{s['file']}:{s['line']}",
                           detail=detail))

    # section index (first heading wins; duplicates are an error)
    index = {}
    for code, p in papers.items():
        d = index.setdefault(code, {})
        for h in p["headings"]:
            if h["num"] is None:
                continue
            if h["num"] in d:
                issues.append(dict(severity="error", type="duplicate_section_number", link_id=None,
                                   src=f"{code} §{h['num']}", target="", where=f"{p['path'].name}:{h['line']}",
                                   detail=f"also used by '{d[h['num']]['title']}' (line {d[h['num']]['line']})"))
            else:
                d[h["num"]] = h

    # extract links
    links, seen = [], Counter()
    for code, p in papers.items():
        cur, fence = dict(sec=None, title=None, region="front"), False
        hl = {h["line"]: h for h in p["headings"]}
        for n, ln in enumerate(p["lines"], 1):
            if n <= p["fm_end"]:
                continue
            if ln.lstrip().startswith(("```", "~~~")):
                fence = not fence
                continue
            if fence:
                continue
            if n in hl:
                h = hl[n]
                if h["num"]:
                    cur = dict(sec=h["num"], title=h["title"], region="body")
                else:
                    cur = dict(sec=h["slug"], title=h["title"],
                               region=REGIONS.get(h["slug"], "unnumbered"))
                continue
            for r in extract(ln, P, prose):
                tcode = r["tcode"] or code
                tsec = r["tsec"]
                tkey = f"{tcode}§{tsec}" if tsec else tcode
                base = f"{code}§{cur['sec']}->{tkey}"
                seen[base] += 1
                links.append(dict(
                    id=f"{base}#{seen[base]}",
                    src=dict(paper=code, section=cur["sec"], title=cur["title"], region=cur["region"],
                             file=p["path"].name, line=n, col=r["span"][0] + 1),
                    target=dict(paper=tcode, section=tsec, key=tkey),
                    form=r["form"], scope="intra" if tcode == code else "inter",
                    range=r.get("range"), raw=r["raw"], context=context(ln, *r["span"]),
                    _span=r["span"], _has_code=r["has_code"], _path=str(p["path"])))

    # validate
    changes, old_titles = [], {}
    for code, op in (baseline.get("papers") or {}).items():
        if code in index:
            old_titles[code] = {s["num"]: s["title"] for s in op.get("sections", [])}
    retitled = {}
    for code, old in old_titles.items():
        for num, ot in old.items():
            if num not in index[code]:
                changes.append(dict(key=f"{code}§{num}", change="removed", old=ot, new=None))
            elif norm(ot) != norm(index[code][num]["title"]):
                nt = index[code][num]["title"]
                retitled[f"{code}§{num}"] = (ot, nt)
                changes.append(dict(key=f"{code}§{num}", change="retitled", old=ot, new=nt))
        for num in index[code]:
            if num not in old:
                changes.append(dict(key=f"{code}§{num}", change="added", old=None,
                                    new=index[code][num]["title"]))

    for l in links:
        t = l["target"]
        loaded = t["paper"] in index
        hist = l["src"]["region"] == "revision_history"
        head = index[t["paper"]].get(t["section"]) if loaded and t["section"] else None
        exists = (head is not None) if (loaded and t["section"]) else (True if loaded else None)
        anchor = anchors.get(t["key"]) if t["section"] else None
        status = None
        if t["section"]:
            if exists is None:
                status = "unchecked"
            elif exists:
                if anchor is None:
                    status = "missing"
                elif head["has_math"]:
                    status = "unverifiable"
                else:
                    f, _, slug = anchor.partition("#")
                    ok_file = f == t["paper"].lower().replace(".", "-") + ".html"
                    ok_slug = re.fullmatch(re.escape(head["slug"]) + r"(-\d+)?", slug) is not None
                    status = "ok" if ok_file and ok_slug else "stale"
        t.update(exists=exists, title=head["title"] if head else None, anchor=anchor, anchor_status=status)
        if hist:
            continue
        if exists is None:
            issue("info", "paper_not_in_source", l, f"{t['paper']} not found under --source; target unverified")
        elif t["section"] and not exists:
            idx = index[t["paper"]]
            par = t["section"].rsplit(".", 1)[0] if "." in t["section"] else None
            sib = [k for k in idx if (k.rsplit(".", 1)[0] == par if par and "." in k else (not par and "." not in k))]
            hint = "; ".join(f"§{k} {idx[k]['title'][:40]}" for k in sib[:6])
            issue("error", "section_not_found", l, f"{t['paper']} has no §{t['section']}. Nearby: {hint}")
        else:
            if status == "missing":
                issue("warn", "not_in_anchors", l, f"{t['key']} exists ('{t['title']}') but has no anchors entry")
            elif status == "stale":
                issue("warn", "anchor_stale", l, f"anchors says {anchor}; heading '{t['title']}' now slugs to #{head['slug']}")
            if t["key"] in retitled:
                o, nw = retitled[t["key"]]
                issue("warn", "target_retitled", l, f"§{t['section']} was '{o}', now '{nw}' - confirm link still fits")
        if l["form"] == "prose":
            issue("warn", "prose_reference", l, f"'{l['raw']}' - house style is (§X.Y), not 'Section X'")

    # registry (internal.json) vs text
    reg_diff = {}
    for code in papers:
        actual = {l["target"]["paper"] for l in links
                  if l["src"]["paper"] == code and l["scope"] == "inter" and l["src"]["region"] != "revision_history"}
        if code in reg:
            listed = set(reg[code].get("outbound_internal", []))
            reg_diff[code] = dict(in_text_not_in_registry=sorted(actual - listed),
                                  in_registry_not_in_text=sorted(listed - actual))
            for tgt in reg_diff[code]["in_text_not_in_registry"]:
                issues.append(dict(severity="info", type="registry_outbound_missing", link_id=None, src=code,
                                   target=tgt, where="internal.json", detail=f"{code} links to {tgt} but outbound_internal omits it"))

    inbound = defaultdict(list)
    for l in links:
        inbound[l["target"]["key"]].append(l["id"])
    graph = defaultdict(Counter)
    for l in links:
        if l["scope"] == "inter" and l["src"]["region"] != "revision_history":
            graph[l["src"]["paper"]][l["target"]["paper"]] += 1

    orphan = sorted(k for k in anchors if "§" in k and k.split("§")[0] in index and k.split("§", 1)[1] not in index[k.split("§")[0]])
    data = dict(
        meta=dict(source=str(source), papers=len(papers), links=len(links),
                  issues=dict(Counter(i["severity"] for i in issues))),
        papers={c: dict(file=p["path"].name, version=reg.get(c, {}).get("version"),
                        sections=[dict(num=h["num"], title=h["title"], level=h["level"], line=h["line"],
                                       slug=h["slug"], anchor=anchors.get(f"{c}§{h['num']}"))
                                  for h in p["headings"] if h["num"]])
                for c, p in papers.items()},
        links=[{k: v for k, v in l.items() if not k.startswith("_")} for l in links],
        inbound={k: sorted(v) for k, v in sorted(inbound.items())},
        paper_graph={a: dict(sorted(b.items())) for a, b in sorted(graph.items())},
        section_changes=changes,
        registry_diff=reg_diff,
        anchors_orphaned=orphan,
        issues=issues,
    )
    return dict(data=data, links=links, papers=papers)


# --------------------------------------------------------------------------- commands

SEV = {"info": 0, "warn": 1, "error": 2}


def cmd_scan(ctx, a):
    out = Path(a.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(ctx["data"], indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    m = ctx["data"]["meta"]
    print(f"{m['links']} links from {m['papers']} papers -> {out}   issues: {m['issues'] or 'none'}")


def cmd_check(ctx, a):
    floor = SEV[a.min_severity]
    items = [i for i in ctx["data"]["issues"] if SEV[i["severity"]] >= floor
             and (not a.paper or i["src"].split(" ")[0] == a.paper)]
    by = defaultdict(list)
    for i in items:
        by[(i["severity"], i["type"])].append(i)
    for (sev, typ), lst in sorted(by.items(), key=lambda kv: (-SEV[kv[0][0]], kv[0][1])):
        print(f"\n[{sev.upper()}] {typ}  ({len(lst)})")
        for i in lst:
            print(f"  {i['where']:<22} {i['src']:<14} -> {i['target']:<14} {i['detail']}")
    for c in ctx["data"]["section_changes"]:
        if c["change"] != "added":
            print(f"\n[CHANGE] {disp(c['key'])} {c['change']}: {c['old']!r} -> {c['new']!r}")
    if ctx["data"]["anchors_orphaned"]:
        print(f"\n[INFO] anchors.yml entries with no matching heading: {len(ctx['data']['anchors_orphaned'])}")
        print("  " + ", ".join(ctx["data"]["anchors_orphaned"][:40]))
    errs = sum(1 for i in items if i["severity"] == "error")
    print(f"\n{len(items)} issue(s), {errs} error(s)")
    return 1 if errs else 0


def _match(key, q):
    if "§" not in q:
        return key.split("§")[0] == q
    return key == q or key.startswith(q + ".")


def cmd_query(ctx, a):
    n = 0
    for l in ctx["data"]["links"]:
        s = l["src"]
        skey = f"{s['paper']}§{s['section']}"
        if (a.to and not _match(l["target"]["key"], a.to)) or (a.frm and not _match(skey, a.frm)):
            continue
        if s["region"] == "revision_history" and not a.history:
            continue
        n += 1
        t = l["target"]
        print(f"{disp(skey):<14} {s['file']}:{s['line']:<5} -> {disp(t['key']):<14} "
              f"{(t['title'] or '?')[:42]:<42} [{l['form']}]\n    {l['context'][:300]}")
    print(f"\n{n} link(s)")


def cmd_remap(ctx, a):
    mapping = load_kv(a.map)
    if not mapping:
        sys.exit("empty or missing map file")
    used, edits = set(), defaultdict(list)
    for l in ctx["links"]:
        if l["form"] in ("prose", "paren_paper", "bracket_paper"):
            continue
        if l["src"]["region"] == "revision_history" and not a.include_history:
            continue
        t = l["target"]
        hit = None
        for old, new in mapping.items():
            if t["key"] == old:
                hit = (old, new, "")
                break
            if not a.no_cascade and t["key"].startswith(old + ".") and (not hit or len(old) > len(hit[0])):
                hit = (old, new, t["key"][len(old):])
        if not hit:
            continue
        used.add(hit[0])
        new = hit[1]
        ncode, nsec = new.split("§", 1) if "§" in new else (t["paper"], new)
        nsec += hit[2]
        sep = re.search(r"(\s*)§", l["raw"]).group(1)
        text = f"{ncode}{sep}§{nsec}" if (l["_has_code"] or ncode != t["paper"]) else f"§{nsec}"
        edits[l["_path"]].append((l["src"]["line"], l["_span"], l["raw"], text))
    for path, lst in edits.items():
        lines = Path(path).read_text(encoding="utf-8").split("\n")
        for line, (s, e), old, new in sorted(lst, key=lambda x: (x[0], -x[1][0])):
            print(f"{Path(path).name}:{line}: {old}  ->  {new}")
            lines[line - 1] = lines[line - 1][:s] + new + lines[line - 1][e:]
        if a.apply:
            Path(path).write_text("\n".join(lines), encoding="utf-8")
    for k in mapping.keys() - used:
        print(f"note: no links matched {k}")
    total = sum(len(v) for v in edits.values())
    print(f"\n{total} link(s) {'rewritten' if a.apply else 'would change (dry run; add --apply)'}")
    print("Note: this rewrites links only. Renumber the headings and refresh anchors.yml separately.")


def cmd_anchors(ctx, a):
    """Write anchors derived from current headings (pandoc ids, -N for duplicates)."""
    out = Path(a.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    rows, math = [], 0
    for code, p in ctx["papers"].items():
        used = Counter()
        for h in p["headings"]:
            n = used[h["slug"]]
            used[h["slug"]] += 1
            if h["num"]:
                math += h["has_math"]
                rows.append(f"{code}§{h['num']}: {code.lower().replace('.', '-')}.html#{h['slug']}" + (f"-{n}" if n else ""))
    out.write_text("\n".join(sorted(rows)) + "\n", encoding="utf-8")
    print(f"{len(rows)} anchors -> {out}  ({math} from headings with math: verify those by hand)")


def cmd_contents(ctx, a):
    """Emit contents.yml-shaped data from the markdown headings, for diffing against registry/contents.yml."""
    out = Path(a.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    lines = []
    for code, p in ctx["papers"].items():
        lines += [f"{code}:", f"  page: {code.lower().replace('.', '-')}.html", "  sections:"]
        lines += [f"    {json.dumps(h['num'])}: {json.dumps(h['title'], ensure_ascii=False)}"
                  for h in p["headings"] if h["num"]]
    out.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"{len(lines)} lines -> {out}")


def main():
    for st in (sys.stdout, sys.stderr):  # Windows consoles default to cp1252; titles contain τ etc.
        st.reconfigure(encoding="utf-8", errors="replace")
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)

    def common(p):
        p.add_argument("--source", help="markdown folder (default: wdt-site/source, else /source)")
        p.add_argument("--anchors", help="default: registry/anchors.yml, then registry/anchors.yml")
        p.add_argument("--internal", help="default: registry/internal.json, then registry/internal.json")
        p.add_argument("--baseline", help="previous crosslinks.json for drift detection")
        p.add_argument("--no-prose", action="store_true", help="ignore 'Section 3.1' prose references")

    s = sub.add_parser("scan"); common(s); s.add_argument("--out", default=str(DEFAULT_OUT))
    c = sub.add_parser("check"); common(c)
    c.add_argument("--min-severity", default="warn", choices=list(SEV)); c.add_argument("--paper")
    g = sub.add_parser("anchors"); common(g); g.add_argument("--out", default=str(ROOT / "registry" / "anchors.generated.yml"))
    k = sub.add_parser("contents"); common(k); k.add_argument("--out", default=str(ROOT / "registry" / "contents.generated.yml"))
    q = sub.add_parser("query"); common(q)
    q.add_argument("--to"); q.add_argument("--from", dest="frm"); q.add_argument("--history", action="store_true")
    r = sub.add_parser("remap"); common(r)
    r.add_argument("--map", required=True); r.add_argument("--apply", action="store_true")
    r.add_argument("--no-cascade", action="store_true", help="exact keys only (default: WP§3 also maps WP§3.x)")
    r.add_argument("--include-history", action="store_true")
    a = ap.parse_args()

    source = first_existing(a.source, ROOT / "source", "/source")
    if not source:
        sys.exit("source folder not found; pass --source")
    apath = first_existing(a.anchors, ROOT / "registry" / "anchors.yml", ROOT / "registry" / "anchors.yml", ROOT / "anchors.yml")
    ipath = first_existing(a.internal, ROOT / "registry" / "internal.json", ROOT / "registry" / "internal.json", ROOT / "internal.json")
    anchors = load_kv(apath)
    print(f"source={source}  anchors={apath}  internal={ipath}", file=sys.stderr)
    if not anchors:
        print("warning: anchors.yml not found; anchor checks disabled", file=sys.stderr)
    base_path = a.baseline or (a.out if a.cmd == "scan" else None)
    ctx = scan(source, anchors, load_json(ipath), load_json(base_path), prose=not a.no_prose)
    code = {"scan": cmd_scan, "check": cmd_check, "query": cmd_query, "remap": cmd_remap, "anchors": cmd_anchors, "contents": cmd_contents}[a.cmd](ctx, a)
    sys.exit(code or 0)


if __name__ == "__main__":
    main()
