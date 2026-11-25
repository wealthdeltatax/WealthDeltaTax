"""
make_fixture.py: write tests/model/data/fixtures/outputs.fixture.json.

A fixture output data file covering every entry of docs/model-v3/outputs.yml
(outputs and checks) with fake numbers, until the v3 model exists.  Brief 030c.
The numbers are a hash of the cell key, carry no meaning, and are the same on
every run; ``run.fixture`` is true so no release build can take it for data.

    python tests/model/data/make_fixture.py            # rewrite the fixture
    python tests/model/data/make_fixture.py --check    # exit 1 if the file is stale

Run it again whenever outputs.yml or data/input-register/inputs.json changes; the test
``test_fixture_is_current`` fails until you do.
"""

from __future__ import annotations

import argparse
import hashlib
import zlib
import json
import sys
from itertools import product
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[3]
MANIFEST = ROOT / "docs" / "model-v3" / "outputs.yml"
INPUTS = ROOT / "data" / "input-register" / "inputs.json"
OUT = Path(__file__).resolve().parent / "fixtures" / "outputs.fixture.json"

ALL_WINDOWS = ["transition", "short", "long"]
FAKE_VOCAB = ["v1", "v2"]          # stands in for a by key the manifest gives as a bare list
SERIES_LEN = 100


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def stats(summary: str, base: float) -> dict:
    if summary == "p10_mean_p90":
        return {"p10": round(base * 0.5, 4), "mean": round(base, 4), "p90": round(base * 1.5, 4)}
    if summary == "point_and_range":
        return {"point": round(base, 4), "lo": round(base * 0.5, 4), "hi": round(base * 1.5, 4)}
    if summary == "point":
        return {"point": round(base, 4)}
    raise ValueError(f"unknown summary form {summary!r}")


def fake_run_field(name: str, manifest: dict) -> str:
    """Value for a run field the manifest adds: pack_country follows country_pack, hashes are fake."""
    if name == "pack_country":
        return manifest["country_pack"]
    return hashlib.sha256(f"fixture-{name}".encode()).hexdigest()


def build(manifest_path: Path = MANIFEST, inputs_path: Path = INPUTS) -> dict:
    manifest = yaml.safe_load(manifest_path.read_text(encoding="utf-8"))
    schedules = list(manifest["schedules"])
    horizons_all = list(manifest.get("horizons") or ALL_WINDOWS)
    outputs: dict = {}
    for e in list(manifest["outputs"]) + list(manifest.get("checks") or []):
        by = e.get("by")
        if isinstance(by, dict):
            names = sorted(by)
            vocab = [[str(v) for v in by[k]] for k in names]
        elif isinstance(by, list):
            names = sorted(str(k) for k in by)
            vocab = [FAKE_VOCAB for _ in names]
        else:
            names, vocab = [], []
        scheds = [None] if e.get("once_not_per_schedule") else schedules
        horizons = [str(h) for h in (e.get("horizons") or horizons_all)]
        lines = [str(x) for x in (e.get("lines") or [])] or [None]
        line_h = {str(k): [str(h) for h in v] for k, v in (e.get("line_horizons") or {}).items()}
        cells = []
        for s, h, ln, combo in product(scheds, horizons, lines, list(product(*vocab)) if names else [()]):
            if ln is not None and h not in line_h.get(ln, horizons):
                continue   # a line is reported only at its own horizons (manifest line_horizons)
            key = f"{e['id']}|{s}|{h}|{ln}|{combo}"   # keyed by cell, so adding an output never moves another's numbers
            base = 1.0 + (zlib.crc32(key.encode()) % 17) * 0.3
            cell: dict = {}
            if s is not None:
                cell["schedule"] = s
            cell["horizon"] = h
            if ln is not None:
                cell["line"] = ln
            cell["by"] = dict(zip(names, combo))
            cell.update(stats(e["summary"], base))
            if e.get("series") is True:
                cell["series"] = [
                    {"t": t, **stats(e["summary"], base * (1 + t / 200))}
                    for t in range(1, SERIES_LEN + 1)
                ]
            cells.append(cell)
        outputs[e["id"]] = {"summary": e["summary"], "cells": cells}
    return {
        "schema": "wdt-outputs/1",
        "run": {
            "manifest_version": manifest["version"],
            "manifest_sha256": sha256(manifest_path),
            "country_pack": manifest["country_pack"],
            "run_date": "2026-01-01",
            "status": "provisional",
            "model_version": "fixture",
            "inputs_sha256": sha256(inputs_path),
            "paths": 0,
            "base_year": 2025,
            "fixture": True,
            **{k: fake_run_field(k, manifest) for k in manifest.get("run_fields_added") or []},
        },
        "outputs": outputs,
    }


def render(doc: dict) -> str:
    """One line per cell, so the file is reviewable and its diffs are small."""
    dump = lambda obj: json.dumps(obj, ensure_ascii=False, separators=(", ", ": "))
    out = ["{", f' "schema": {dump(doc["schema"])},', f' "run": {dump(doc["run"])},', ' "outputs": {']
    items = list(doc["outputs"].items())
    for i, (oid, entry) in enumerate(items):
        out.append(f'  {dump(oid)}: {{"summary": {dump(entry["summary"])}, "cells": [')
        cells = entry["cells"]
        for j, cell in enumerate(cells):
            out.append("   " + dump(cell) + ("," if j < len(cells) - 1 else ""))
        out.append("  ]}" + ("," if i < len(items) - 1 else ""))
    out += [" }", "}", ""]
    return "\n".join(out)


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--check", action="store_true", help="do not write; exit 1 if the file is stale")
    args = ap.parse_args(argv)
    text = render(build())
    if args.check:
        current = OUT.read_text(encoding="utf-8") if OUT.exists() else None
        if current != text:
            print(f"{OUT} is stale: run python tests/model/data/make_fixture.py", file=sys.stderr)
            return 1
        return 0
    OUT.parent.mkdir(parents=True, exist_ok=True)
    with open(OUT, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(text)
    print(f"wrote {OUT} ({text.count(chr(10))} lines)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
