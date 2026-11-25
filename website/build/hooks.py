"""Hook resolver: {{o:}} {{i:}} {{ref:}} {{lit:}} -> numbers or placeholders (hooks.md 4; brief 060c).

    python website/build/hooks.py resolve <spoke.md> [--data F] [--fixture] [--out F]
    python website/build/hooks.py validate <data.json> [--fixture]
    python website/build/hooks.py report <spoke.md ...> [--data F] [--fixture] [--out _build/hooks-report.json]

WDT_MODE=draft|release (default draft). Loads validate_outputs.py and hook_format.py by path; runs under python -I.
"""
import argparse, importlib.util, json, os, re, sys
from pathlib import Path
import yaml

ROOT = Path(__file__).resolve().parent.parent.parent


def _load(name, base=Path(__file__).resolve().parent):
    if name in sys.modules:
        return sys.modules[name]
    spec = importlib.util.spec_from_file_location(name, base / f"{name}.py")
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


vo, hf = _load("validate_outputs", ROOT / "pipeline"), _load("hook_format")   # validate_outputs.py is model-side; stays in pipeline/ until 162c moves it
PATHS = dict(manifest=ROOT / "docs/model-v3/outputs.yml", inputs=ROOT / "registry/inputs.json",
             display=ROOT / "registry/inputs-display.yml", lit=ROOT / "website/registry/lit-figures.yml",
             bib=ROOT / "registry/references.bib")
STATS = {"p10_mean_p90": ("p10", "mean", "p90", "range"), "point_and_range": ("point", "lo", "hi", "range"),
         "point": ("point",)}
DEFSTAT = {"p10_mean_p90": "mean", "point_and_range": "point", "point": "point"}
RANGE = {"p10_mean_p90": ("p10", "p90"), "point_and_range": ("lo", "hi")}
ID = r"[A-Za-z0-9_.-]+"
O_RE = re.compile(rf"o:(?P<id>[A-Za-z0-9]+)(?::(?P<line>[A-Za-z0-9_]+))?(?:\.(?P<stat>[a-z0-9]+))?"
                  rf"(?:@(?P<sched>\w+))?(?:/(?P<hor>\w+))?(?:#(?P<by>{ID}:{ID}(?:,{ID}:{ID})*|overall))?")
I_RE = re.compile(r"i:(?P<id>I-[A-Za-z0-9]+)(?:\.(?P<stat>[a-z]+))?")
REF_RE = re.compile(r"ref:(?P<id>fig-(?P<sp>[A-Za-z0-9]+)-(?P<n>[0-9]+))")
LIT_RE = re.compile(rf"lit:(?P<key>{ID}:{ID})")
HOOK = re.compile(r"\{\{[^{}]*\}\}")
FIG_OPEN = re.compile(r"^:::\s*\{#(fig-([A-Za-z0-9]+)-([0-9]+))\}")


class Err(Exception):
    def __init__(self, code, msg):
        self.code, self.msg = code, msg


class Ctx:
    """Everything a hook needs. Data checks call the validator; a failure is H13 and no data is used."""
    def __init__(self, data=None, fixture=False, mode=None, paths=None):
        p = {**PATHS, **(paths or {})}
        self.mode = mode or os.environ.get("WDT_MODE", "draft")
        if self.mode not in ("draft", "release"):
            raise SystemExit(f"WDT_MODE must be draft or release, not {self.mode!r}")
        self.manifest = yaml.safe_load(p["manifest"].read_text(encoding="utf-8"))
        self.entries = vo.load_entries(self.manifest)
        self.raw = {e["id"]: e for k in ("outputs", "checks") for e in self.manifest.get(k) or []}
        rows = json.loads(p["inputs"].read_text(encoding="utf-8"))["inputs"]
        self.inputs = {r["id"]: r for r in rows}
        self.display = (yaml.safe_load(p["display"].read_text(encoding="utf-8")) or {}).get("inputs", {})
        self.lit = (yaml.safe_load(p["lit"].read_text(encoding="utf-8")) or {}).get("figures", {})
        self.bib = set(re.findall(r"@\w+\s*\{\s*([^,\s]+)\s*,", p["bib"].read_text(encoding="utf-8")))
        self.data, self.data_findings, self.data_status, self.cells = None, [], "none", {}
        if data is not None:
            self._load_data(data, fixture, p)

    def _load_data(self, data, fixture, p):
        run = data.get("run") if isinstance(data, dict) else None
        run = run if isinstance(run, dict) else {}
        self.data_status = "fixture" if run.get("fixture") else str(run.get("status"))
        if run.get("fixture") is True and not fixture:
            self.data_findings.append(("error", "H13", "fixture data is not accepted without --fixture"))
            return
        vmode = "fixture" if fixture else "final" if self.mode == "release" else "default"
        found = vo.validate(data, self.manifest, p["manifest"], p["inputs"], vmode)
        self.data_findings += [(f.level, "H13" if f.level == "error" else f.rule, f"{f.rule} {f.where}: {f.message}")
                               for f in found]
        if not any(f.level == "error" for f in found):
            self.data = data
            for oid, e in data["outputs"].items():
                self.cells[oid] = {(c.get("schedule"), c.get("horizon"), c.get("line"),
                                    tuple(sorted((k, vo.vstr(v)) for k, v in c["by"].items()))): c for c in e["cells"]}


def count_words(text):
    """One hook, or one unresolved placeholder, counts as one word."""
    return len(re.sub(r"\{\{[^{}]*\}\}|\[\[[^\[\]]*\]\]", "x", text).split())


def scan(text):
    """Split a spoke file into hooks (outside code, front matter and figure blocks), figure blocks and front matter."""
    lines, front, hooks, figs, i = text.split("\n"), {}, [], [], 0
    if lines and lines[0].strip() == "---":
        end = next((k for k in range(1, len(lines)) if lines[k].strip() == "---"), 0)
        front = yaml.safe_load("\n".join(lines[1:end])) or {}
        i = end + 1
    fence, fig = None, False
    for n in range(i, len(lines)):
        ln = lines[n]
        if fence:
            fence = None if ln.lstrip().startswith(fence) else fence
            continue
        if ln.lstrip().startswith(("```", "~~~")):
            fence = ln.lstrip()[:3]
            continue
        m = FIG_OPEN.match(ln)
        if m:
            figs.append((m.group(1), m.group(2), int(m.group(3)), n + 1)); fig = True; continue
        if fig and ln.strip() == ":::":
            fig = False; continue
        masked = re.sub(r"`[^`\n]*`", lambda k: " " * len(k.group()), ln)
        if fig and not masked.lstrip().startswith("caption:"):
            continue
        for k in HOOK.finditer(masked):
            hooks.append(dict(line=n + 1, s=k.start(), e=k.end(), raw=k.group(), zone="caption" if fig else "prose"))
        j = HOOK.sub(lambda k: " " * len(k.group()), masked).find("{{")
        if j >= 0:
            hooks.append(dict(line=n + 1, s=j, e=len(ln), raw=ln[j:], zone="open"))
    return front, hooks, figs, lines


def _by(ent, d):
    given = {}
    if d["by"] and d["by"] != "overall":
        for pair in d["by"].split(","):
            k, v = pair.split(":", 1)
            if k not in ent.by:
                raise Err("H07", f"by key {k!r} not in {sorted(ent.by)}")
            if ent.by[k] is not None and v not in ent.by[k]:
                raise Err("H07", f"by.{k} value {v!r} not in {ent.by[k]}")
            given[k] = v
    out = {}
    for k, vocab in ent.by.items():
        if k in given:
            out[k] = given[k]
        elif vocab is not None and "overall" in vocab:
            out[k] = "overall"
        else:
            raise Err("H08", f"by.{k} not given and the output has no 'overall'")
    return out


def resolve_o(c, fm, d):
    """Returns (text, warning) or raises Err; an Err with a 'placeholder' code carries the placeholder in msg."""
    oid = d["id"]
    ent = c.entries.get(oid)
    if ent is None:
        raise Err("H02", f"unknown output id {oid!r}")
    dfl, raw, once, single = fm.get("defaults") or {}, c.raw[oid], ent.schedules is None, ent.horizons == ["single"]
    stat = d["stat"] or DEFSTAT.get(ent.summary, "mean")
    sched = None if once else d["sched"] or dfl.get("schedule")
    hor = "single" if single else d["hor"] or dfl.get("horizon")
    if not once and not sched or not hor:
        raise Err("H09", "schedule or horizon omitted and the front matter has no default")
    if stat not in STATS.get(ent.summary, ()):
        raise Err("H03", f"stat {stat!r} not legal for summary {ent.summary!r}: {STATS.get(ent.summary)}")
    if once and d["sched"]:
        raise Err("H04", "output is reported once, not per schedule: remove @SCHEDULE")
    if sched is not None and sched not in c.manifest["schedules"]:
        raise Err("H04", f"unknown schedule {sched!r}")
    if single and d["hor"]:
        raise Err("H06", "output has no horizon dimension: remove /HORIZON")
    if hor not in c.manifest["horizons"] + ["single"]:
        raise Err("H05", f"unknown horizon {hor!r}")
    line = d["line"]
    if ent.lines and not line:
        raise Err("H08", f"output has lines {ent.lines}: write {{{{o:{oid}:LINE...}}}}")
    if line and line not in ent.lines:
        raise Err("H07", f"line {line!r} not in {ent.lines}")
    if hor not in ent.line_horizons.get(line, ent.horizons):
        raise Err("H06", f"horizon {hor!r} outside the output's own set {ent.line_horizons.get(line, ent.horizons)}")
    by = _by(ent, d)
    el = raw.get("element") or []
    if fm.get("spoke") not in el and not (fm.get("spoke") == "HUB" and any(re.fullmatch(r"H\d", x) for x in el)):
        raise Err("H10", f"{oid} is not an output of spoke {fm.get('spoke')!r} (element: {el})")
    ph = hf.placeholder(oid, stat, sched, None if single else hor, by, line)
    cell = c.cells.get(oid, {}).get((sched, hor, line, tuple(sorted(by.items()))))
    if cell is None:
        raise Err("H11", ph)
    fields = RANGE[ent.summary] if stat == "range" else (stat,)
    vals = [cell.get(f) for f in fields]
    if any(isinstance(v, bool) or not isinstance(v, (int, float)) for v in vals):
        raise Err("H12", ph)
    unit, dec = raw.get("unit"), raw.get("decimals")
    if isinstance(unit, dict) or isinstance(dec, dict):
        if not line:
            raise Err("H13", f"manifest gives unit or decimals per line but {oid} declares no lines")
        unit, dec = (unit[line] if isinstance(unit, dict) else unit), (dec[line] if isinstance(dec, dict) else dec)
    return fmt(vals, unit, dec)


def fmt(vals, unit, dec):
    try:
        return hf.format_range(*vals, unit, dec) if len(vals) == 2 else (hf.format_value(vals[0], unit, dec), None)
    except hf.UnitError as e:
        raise Err("H13", str(e))


def resolve_i(c, d):
    rid, stat = d["id"], d["stat"] or "central"
    row = c.inputs.get(rid)
    if row is None:
        raise Err("H20", f"unknown input id {rid!r}")
    if stat not in ("central", "low", "high", "range"):
        raise Err("H21", f"stat {stat!r} not in central, low, high, range")
    spec = row.get("display") or c.display.get(rid)
    if not spec or "unit" not in spec or "decimals" not in spec:
        raise Err("H22", f"no display spec for {rid}")
    vals = [row.get(k) for k in (("low", "high") if stat == "range" else (stat,))]
    if spec["unit"] in hf.NON_NUMERIC or any(isinstance(v, bool) or not isinstance(v, (int, float)) for v in vals):
        raise Err("H23", f"{rid} {stat} is not a number (unit {spec['unit']!r}, value {vals})")
    return fmt(vals, spec["unit"], spec["decimals"])


def resolve_lit(c, d, cites):
    key, e = d["key"], c.lit.get(d["key"])
    if e is None:
        raise Err("H40", f"lit key {key!r} not in lit-figures.yml")
    if key.split(":")[0] not in c.bib:
        raise Err("H42", f"bib key {key.split(':')[0]!r} not in references.bib")
    if not e.get("verified"):
        raise Err("H41", f"[[lit:{key}]]")
    cites.add(key.split(":")[0])
    return fmt([e["value"]], e["unit"], e["decimals"])


def sentences(text):
    return re.split(r"(?<=[.!?])\s+|\n{2,}", text)


def check_f4(text):
    """H32: every figure block is cited by a ref hook, and a citing sentence holds an o hook. Returns [(code, msg)]."""
    _, hooks, figs, lines = scan(text)
    prose = "\n".join(l for l in lines if not FIG_OPEN.match(l))
    out = []
    for fid, _, _, ln in figs:
        cites = [s for s in sentences(prose) if "{{ref:" + fid + "}}" in s]
        if not cites:
            out.append(("H32", f"figure {fid} (line {ln}) is never cited"))
        elif not any("{{o:" in s for s in cites):
            out.append(("H32", f"no sentence citing {fid} has an o hook"))
    return out


def check_r1_reverse(spokes, manifest=None):
    """R1r: spokes maps shortcode -> text; returns [(spoke, output id)] for outputs listing a spoke that no hook cites."""
    m = manifest or yaml.safe_load(PATHS["manifest"].read_text(encoding="utf-8"))
    out = []
    for sp, text in spokes.items():
        cited = set(re.findall(r"\{\{o:([A-Za-z0-9]+)", text))
        cited |= {x.strip() for g in re.findall(r"output:\s*\[([^\]]*)\]", text) for x in g.split(",")}   # figure blocks (F5)
        out += [(sp, e["id"]) for k in ("outputs", "checks") for e in m.get(k) or []
                if sp in (e.get("element") or []) and e["id"] not in cited]
    return out


def check_a2(text):
    """A2: a /long hook in the Short answer needs a /short hook of the same output in that paragraph."""
    fm, _, _, _ = scan(text)
    dfl, out = (fm.get("defaults") or {}), []
    for para in re.split(r"\n\s*\n", re.sub(r"\A---\n.*?\n---\n", "", text, flags=re.S)):
        if not para.lstrip().startswith("**Short answer"):
            continue
        hs = [O_RE.fullmatch(h[2:-2]) for h in HOOK.findall(para)]
        hs = [(m["id"], m["hor"] or dfl.get("horizon")) for m in hs if m]
        out += [("A2", f"/long hook of {i} in the Short answer has no /short hook of {i} beside it")
                for i, h in hs if h == "long" and (i, "short") not in hs]
    return out


def resolve_text(text, c, file="-"):
    fm, hooks, figs, lines = scan(text)
    res = dict(text="", counts=dict(resolved=0, placeholder=0, error=0), unresolved=[], errors=[], warnings=[],
               citations=set())
    rep = {}

    def add(kind, h, code, msg):
        res[kind].append(dict(file=file, line=h["line"], hook=h["raw"], code=code, message=msg))

    for h in hooks:
        body = h["raw"][2:-2]
        if h["zone"] != "prose":
            res["counts"]["error"] += 1
            add("errors", h, "H01" if h["zone"] == "open" else "F1",
                "unclosed or malformed {{" if h["zone"] == "open" else "a hook in a figure caption (rule F1)")
            continue
        try:
            if body.startswith("ref:"):
                m = REF_RE.fullmatch(body)
                if not m:
                    raise Err("H01", "text does not match any hook form")
                if m["id"] not in [f[0] for f in figs]:
                    raise Err("H30", f"{m['id']} is not a figure block of this file")
                val, warn = f"[Figure {m['n']}](#{m['id']})", None
            else:
                kind = body.split(":", 1)[0]
                m = {"o": O_RE, "i": I_RE, "lit": LIT_RE}.get(kind)
                m = m and m.fullmatch(body)
                if not m:
                    raise Err("H01", "text does not match any hook form")
                d = m.groupdict()
                val, warn = (resolve_o(c, fm, d) if kind == "o" else resolve_i(c, d) if kind == "i"
                             else resolve_lit(c, d, res["citations"]))
            rep[(h["line"], h["s"])] = (h["e"], val)
            res["counts"]["resolved"] += 1
            if warn:
                add("warnings", h, "W2", warn)
        except Err as e:
            if e.code in ("H11", "H12", "H41") and c.mode == "draft":
                rep[(h["line"], h["s"])] = (h["e"], e.msg)
                res["counts"]["placeholder"] += 1
                add("unresolved", h, e.code, "no value yet: placeholder")
            else:
                res["counts"]["error"] += 1
                add("errors", h, e.code, e.msg)
    nums = [f[2] for f in figs if f[1] == fm.get("spoke")]
    if nums != list(range(1, len(nums) + 1)):
        res["errors"].append(dict(file=file, line=figs[0][3], hook="", code="H31", message=f"figure numbers {nums} are not 1 to {len(nums)}"))
    top = dict(file=file, line=1, hook="")
    res["errors"] += [dict(top, code=c_, message=m_) for c_, m_ in check_f4(text) + check_a2(text)]
    sp = fm.get("spoke")
    r1 = [dict(top, code="R1r", message=f"{o} lists {s} in element but no hook cites it") for s, o in check_r1_reverse({sp: text}, c.manifest)] if sp else []
    res["errors" if c.mode == "release" else "warnings"] += r1
    for (ln, s), (e, val) in sorted(rep.items(), reverse=True):
        lines[ln - 1] = lines[ln - 1][:s] + val + lines[ln - 1][e:]
    res["text"] = "\n".join(lines)
    return res


def build_report(results, c):
    keys = ("errors", "warnings", "unresolved")
    rep = dict(schema="wdt-hooks-report/1", mode=c.mode, data_status=c.data_status,
               counts={k: sum(r["counts"][k] for r in results) for k in ("resolved", "placeholder", "error")})
    for k in keys:
        rep[k] = sorted((x for r in results for x in r[k]), key=lambda x: (x["file"], x["line"], x["hook"], x["code"]))
    for lvl, code, msg in c.data_findings:
        rep["errors" if lvl == "error" else "warnings"].append(dict(file="data", line=0, hook="", code=code, message=msg))
    return rep


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("cmd", choices=["resolve", "validate", "report"])
    ap.add_argument("files", nargs="+")
    ap.add_argument("--data"), ap.add_argument("--out"), ap.add_argument("--fixture", action="store_true")
    a = ap.parse_args(argv)
    data_path = a.files[0] if a.cmd == "validate" else a.data
    c = Ctx(json.loads(Path(data_path).read_text(encoding="utf-8")) if data_path else None, a.fixture)
    results = [] if a.cmd == "validate" else [resolve_text(Path(f).read_text(encoding="utf-8"), c, f) for f in a.files]
    rep = build_report(results, c)
    for x in rep["errors"] + rep["warnings"]:
        print(f"{x['code']:<4} {x['file']}:{x['line']} {x['hook']} {x['message']}", file=sys.stderr)
    if a.cmd == "resolve" and not a.out:
        print(results[0]["text"])
    elif a.cmd == "resolve":
        Path(a.out).write_text(results[0]["text"], encoding="utf-8", newline="\n")
    elif a.cmd == "report":
        out = Path(a.out or ROOT / "_build/hooks-report.json")
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(json.dumps(rep, indent=1, sort_keys=True, ensure_ascii=False) + "\n", encoding="utf-8", newline="\n")
    return 1 if rep["errors"] else 0


if __name__ == "__main__":
    sys.exit(main())
