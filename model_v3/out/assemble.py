"""Output layer, assembly: Samples and Level2 to the `outputs` and `level2` objects of the output file.

Reads only the manifest (a mapping loaded from outputs.yml) and the interface contract. Data-driven: no per-output code.
Format: docs/restructure/site/hooks.md section 3 with the 030c rulings; ids and units are the manifest's, values are never rescaled.

Conventions fixed here, because interface.py says only "arrays of one entry per path":
  p10_mean_p90     the array holds the draws; P10 and P90 are numpy.percentile (linear), the mean is arithmetic.
  point_and_range  the array holds exactly three entries, [point, lo, hi]; the runner knows what the range means.
  point            the array holds exactly one entry.
  series           a Samples key whose `by` also holds the pair ("t", n) is the year-n point of an annual series; it is
                   attached to every cell of the same schedule, horizon and line whose `by`, without `year`, equals its own.
  line_horizons    a line listed in the manifest entry's `line_horizons` gets cells only for those horizons.
A missing cell, a missing output or a non-finite value is an error in a final run; in a provisional run the cell or output is
left out, or the value is null, and the validator reports it (V5, V7).
"""
from __future__ import annotations

from itertools import product

import numpy as np

SIGNIFICANT = 12   # floats are rounded to 12 significant digits so the bytes do not depend on the last bit of a platform


class AssembleError(ValueError):
    """The samples do not fit the manifest, or a final run holds a gap or a non-finite value."""


def entries(manifest: dict) -> dict:
    """Manifest outputs and checks by id, in manifest order."""
    return {e["id"]: e for key in ("outputs", "checks") for e in manifest.get(key) or []}


def _vocab(entry: dict) -> dict:
    by = entry.get("by") or {}
    if not isinstance(by, dict):
        raise AssembleError(f"{entry['id']}: by must be a map of dimension to values")
    return {str(k): [str(v) for v in vals] for k, vals in by.items()}


def _expected(manifest: dict, entry: dict) -> list:
    """Every cell key of an output: (schedule or None, horizon, by tuple, line or None), in manifest order."""
    schedules = [None] if entry.get("once_not_per_schedule") else list(manifest["schedules"])
    horizons = [str(h) for h in entry.get("horizons") or manifest["horizons"]]
    lines = [str(x) for x in entry.get("lines") or []] or [None]
    line_hor = entry.get("line_horizons") or {}
    vocab = _vocab(entry)
    names = sorted(vocab)
    combos = list(product(*(vocab[n] for n in names))) if names else [()]
    keys = []
    for s, ln in product(schedules, lines):
        hs = [str(h) for h in line_hor[ln]] if ln in line_hor else horizons
        keys += [(s, h, tuple(zip(names, c)), ln) for h in hs for c in combos]
    return keys


def _norm(key: tuple) -> tuple:
    s, h, by, ln = key
    return (None if s is None else str(s), str(h), tuple(sorted((str(k), str(v)) for k, v in by)), None if ln is None else str(ln))


def _round(x: float) -> float:
    return float(f"{x:.{SIGNIFICANT}g}")


def _finite(values, where: str, final: bool):
    """The values rounded, or None (provisional) when any is not finite; a final run raises."""
    arr = np.asarray(values, dtype=float).ravel()
    if np.isfinite(arr).all():
        return arr
    if final:
        raise AssembleError(f"{where}: non-finite value in a final run")
    return None


def _stats(summary: str, values, where: str, final: bool) -> dict:
    fields = {"p10_mean_p90": ("p10", "mean", "p90"), "point_and_range": ("point", "lo", "hi"), "point": ("point",)}[summary]
    arr = _finite(values, where, final)
    if arr is None:
        return {f: None for f in fields}
    if summary == "p10_mean_p90":
        if arr.size == 0:
            raise AssembleError(f"{where}: no draws")
        p10, p90 = np.percentile(arr, [10, 90])
        return dict(zip(fields, (_round(p10), _round(arr.mean()), _round(p90))))
    if arr.size != len(fields):
        raise AssembleError(f"{where}: {summary} needs {len(fields)} entries ({', '.join(fields)}), found {arr.size}")
    return dict(zip(fields, (_round(v) for v in arr)))


def _series(entry: dict, samples: dict, cell_key: tuple, final: bool):
    """Annual points for a cell of an output the manifest declares `series: true`; None when there are none."""
    s, h, by, ln = cell_key
    rest = tuple(p for p in by if p[0] != "year")
    pts = {}
    for key, values in samples.items():
        ks, kh, kby, kln = key
        t = [v for k, v in kby if k == "t"]
        if t and (ks, kh, kln) == (s, h, ln) and tuple(p for p in kby if p[0] != "t") == rest:
            pts[int(t[0])] = _stats(entry["summary"], values, f"{entry['id']} series t={t[0]}", final)
    return [{"t": t, **pts[t]} for t in sorted(pts)] or None


def assemble_output(manifest: dict, entry: dict, samples: dict, final: bool, held: dict | None = None) -> dict:
    """One output entry, `{"summary", "cells"}`; cells follow the manifest product."""
    oid, summary = entry["id"], entry["summary"]
    every = {_norm(k): v for k, v in samples.items()}
    got = {k: v for k, v in every.items() if not any(p[0] == "t" for p in k[2])}
    gone = lambda k: any(dict(k[2]).get(d) == v for d, vs in (held or {}).items() for v in vs)   # a by-value the arm withholds (121c, 122c)
    wanted = [k for k in (_norm(k) for k in _expected(manifest, entry)) if not gone(k)]
    if any(gone(k) for k in got):
        raise AssembleError(f"{oid}: samples for a withheld by-value")
    extra = sorted(set(got) - set(wanted), key=str)
    if extra:
        raise AssembleError(f"{oid}: {len(extra)} sample key(s) outside the manifest, e.g. {extra[0]}")
    cells = []
    for key in wanted:
        if key not in got:
            if final:
                raise AssembleError(f"{oid}: no samples for cell {key}")
            continue
        s, h, by, ln = key
        cell = {} if s is None else {"schedule": s}
        cell["horizon"] = h
        if ln is not None:
            cell["line"] = ln
        cell["by"] = dict(by)
        cell.update(_stats(summary, got[key], f"{oid} {key}", final))
        if entry.get("series") is True:
            series = _series(entry, every, key, final)
            if series is None and final:
                raise AssembleError(f"{oid}: series declared but no annual points for cell {key}")
            if series is not None:
                cell["series"] = series
        cells.append(cell)
    return {"summary": summary, "cells": cells, **({"withheld_by": {d: {v: "legacy_only" for v in vs} for d, vs in held.items()}} if held else {})}


def assemble_level2(level2: dict, ids: dict, final: bool) -> dict:
    """The `level2` object: tornado rows as supplied (the validator checks their order) and the level 2 P10 and P90."""
    doc = {}
    for oid, item in level2.items():
        if oid not in ids:
            raise AssembleError(f"{oid}: level 2 result for an id not in the manifest")
        rows = []
        for r in item.tornado:
            lo, hi = r.low_effect, r.high_effect
            ok = _finite([lo, hi], f"{oid} tornado {r.input}", final) is not None
            rows.append({"input": r.input, "low_effect": _round(lo) if ok else None, "high_effect": _round(hi) if ok else None})
        ok = _finite([item.p10, item.p90], f"{oid} level 2", final) is not None
        doc[oid] = {"tornado": rows, "p10": _round(item.p10) if ok else None, "p90": _round(item.p90) if ok else None}
    return doc


def assemble(manifest: dict, samples: dict, level2: dict | None = None, status: str = "provisional", withheld: dict | None = None) -> tuple:
    """(outputs, level2) objects for the file. An output id not in the manifest raises; so does any gap when status is final.
    `withheld` {id: 'legacy_only'}: that id is written as `{"summary", "cells": [], "withheld": label}`, never a value; samples for it raise (121c)."""
    if status not in ("provisional", "final"):
        raise AssembleError(f"status must be provisional or final, found {status!r}")
    final, ids = status == "final", entries(manifest)
    unknown = sorted(set(samples) - set(ids))
    if unknown:
        raise AssembleError(f"output id(s) not in the manifest: {', '.join(unknown)}")
    outputs = {}
    for oid, entry in ids.items():
        if isinstance(withheld, dict) and isinstance(withheld.get(oid), dict):
            outputs[oid] = assemble_output(manifest, entry, samples.get(oid, {}), final, {d: list(v) for d, v in withheld[oid].items()})
        elif oid in (withheld or {}):
            if samples.get(oid):
                raise AssembleError(f"{oid}: withheld ({withheld[oid]}) but samples were given")
            outputs[oid] = {"summary": entry["summary"], "cells": [], "withheld": withheld[oid]}
        elif oid in samples:
            outputs[oid] = assemble_output(manifest, entry, samples[oid], final)
        elif final:
            raise AssembleError(f"{oid}: no samples for a manifest id in a final run")
    return outputs, assemble_level2(level2 or {}, ids, final)
