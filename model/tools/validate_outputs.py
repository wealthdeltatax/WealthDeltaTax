"""
validate_outputs.py: validate an output data file against the output manifest.

    python model/tools/validate_outputs.py FILE [--final | --fixture]
                                        [--manifest outputs.yml]
                                        [--inputs data/input-register/inputs.json]

Implements rules V1 to V12 of docs/restructure/site/hooks.md section 3.4
(brief 030c).  The data file is JSON, schema ``wdt-outputs/1``; the manifest
is model-specs/outputs.yml.  Every run prints one line per rule so a rule
that silently stopped running is visible.

Modes
- default      V7, V9 and V11 are errors when ``run.status`` is ``final`` and
               warnings when it is ``provisional``.
- ``--final``  the release gate: V7, V9 and V11 are errors whatever the file
               says, the file must say ``status: final`` and must not be a
               fixture, and nulls are not allowed.
- ``--fixture`` for a file made by tests/model/data/make_fixture.py: it must carry
               ``run.fixture: true``; stale hashes and manifest version are
               warnings (the fixture is regenerated on demand).

Exit status: 0 no errors, 1 errors, 2 the file could not be read.

Manifest notes (printed every run, never errors): the validator also reports
where outputs.yml and hooks.md disagree, so the guru can fix the source.
Self-contained on purpose (no sibling imports), so it runs under ``python -I``.
"""

from __future__ import annotations

import argparse
import datetime
import hashlib
import json
import math
import re
import sys
from dataclasses import dataclass, field
from itertools import product
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent.parent
DEFAULT_MANIFEST = ROOT / "model-specs" / "outputs.yml"
DEFAULT_INPUTS = ROOT / "data" / "input-register" / "inputs.json"

SCHEMA = "wdt-outputs/1"
ALL_WINDOWS = ["transition", "short", "long"]

# Numeric fields of a cell, by manifest summary form.  ``point`` alone is used
# by DH1b and OH1b2; hooks.md section 3.3 lists only the first two forms.
STAT_FIELDS = {
    "p10_mean_p90": ("p10", "mean", "p90"),
    "point_and_range": ("point", "lo", "hi"),
    "point": ("point",),
}
CELL_FIELDS = {"schedule", "horizon", "by", "line", "series"}
# Stated markers a numeric field may carry instead of a number, per output id (089c): OF1 where no schedule passes the 75% threshold, CK1 and OF1 where a point was not run.
MARKERS = {"OF1": {"none_passes_75", "not_run_this_point"}, "CK1": {"not_run_this_point"}}
ENTRY_FIELDS = {"summary", "cells", "withheld", "withheld_by", "pending"}
NO_PAYER, NO_PAYER_IDS = "no_payer_at_launch", ("O2", "O2b", "O2c", "O2d", "OH1b", "OH1c", "OW3")   # a wealth band with no payer at launch under the schedule, and what derives from it (author, 2026-11-23)
NOT_RUN = "not_run_this_point"                                                              # O1e ran at one scenario point only (author, 2026-11-23); accepted for O1e, in the centre slot
PACK_LABELS = {"GBR": "UK"}                                                                   # stated mapping: pack code to manifest label (author, 2026-11-23)
NOT_DEFINED, NOT_RUN_RUN, NO_SIGN = "not_defined_under_safe_fund", "not_run_this_run", "no_sign_change_0_15"                  # O1e only
NO_CENTRAL = "no_central"                                                                    # the centre slot of a range across scenario points
CENTRE_SLOT = {"p10_mean_p90": "mean", "point_and_range": "point", "point": "point"}
MAY_WITHHOLD = ("OW1",)                                                                       # household arm: the labelled marker `withheld: legacy_only` is accepted, not required (author, 2026-11-23; 121c, 135c)
PENDING_IDS = ("OF1", "CK1")                                                                  # labelled pending until the author rules on the feasibility rule (140c, 089c)
TOP_FIELDS = {"schema", "run", "outputs", "level2"}
RUN_REQUIRED = (
    "manifest_version", "manifest_sha256", "country_pack", "run_date",
    "status", "model_version", "inputs_sha256", "paths", "base_year",
)
RUN_FIELDS = set(RUN_REQUIRED) | {"fixture", "arm", "seed", "level2_draws", "level2_paths", "unfilled_paths"}
ARMS = ("legacy", "household")   # run.arm: the name, or an object whose `arm` is the name (model_v3 runner/arm.py label); absent means legacy
LEVEL2_FIELDS = {"tornado", "p10", "p90"}
HOOKS_ID_RE = re.compile(r"^O[A-Z]?[0-9]+[a-z]?$")   # hooks.md section 4.1

RULES = {
    "V1": "schema equals wdt-outputs/1",
    "V2": "outputs keys are manifest ids; summary matches the manifest",
    "V3": "cell dimensions and vocabulary values match the manifest",
    "V4": "no two cells of an output share a key",
    "V5": "numeric fields are present and finite (null only when provisional)",
    "V6": "ordering: p10<=p90, lo<=hi (error); mean, point inside range (warning); tornado order",
    "V7": "coverage: every manifest id present, cells equal the full product (error when final)",
    "V8": "run metadata: manifest version and hash, country pack, status, date",
    "V9": "inputs_sha256 equals the hash of data/input-register/inputs.json (error when final)",
    "V10": "series: integer t from 1, strictly increasing, reported years present",
    "V11": "every year in a by.year vocabulary has a cell (error when final)",
    "V12": "unknown top-level, entry, cell, run and level 2 fields (warning)",
}
STRICT_RULES = {"V7", "V9", "V11"}   # errors in final mode


@dataclass
class Finding:
    rule: str
    level: str          # "error" or "warning"
    where: str
    message: str

    def line(self) -> str:
        return f"{self.rule:<4} {self.level:<7} {self.where}: {self.message}"


@dataclass
class Entry:
    id: str
    summary: str
    schedules: list[str] | None      # None: reported once, not per schedule
    horizons: list[str]
    by: dict[str, list[str] | None]  # None: vocabulary not declared (list form)
    lines: list[str]
    series: bool
    kind: str
    line_horizons: dict[str, list[str]] = field(default_factory=dict)   # line -> its own horizons; absent line: `horizons`
    arms: list[str] | None = None    # the arms that produce the output; None: all (122c)
    arms_by: dict[str, dict[str, list[str]]] = field(default_factory=dict)   # dimension -> value -> the arms that produce that part


def sha256_file(path: Path) -> str | None:
    try:
        return hashlib.sha256(path.read_bytes()).hexdigest()
    except OSError:
        return None


# ── manifest ─────────────────────────────────────────────────────────────────

def load_entries(manifest: dict) -> dict[str, Entry]:
    schedules = list(manifest.get("schedules") or [])
    horizons = list(manifest.get("horizons") or ALL_WINDOWS)
    entries: dict[str, Entry] = {}
    for key in ("outputs", "checks"):
        for e in manifest.get(key) or []:
            by = e.get("by")
            if isinstance(by, dict):
                by_map = {str(k): [str(v) for v in vals] for k, vals in by.items()}
            elif isinstance(by, list):
                by_map = {str(k): None for k in by}
            else:
                by_map = {}
            entries[e["id"]] = Entry(
                id=e["id"],
                summary=e.get("summary", ""),
                schedules=None if e.get("once_not_per_schedule") else schedules,
                horizons=[str(h) for h in (e.get("horizons") or horizons)],
                by=by_map,
                lines=[str(x) for x in (e.get("lines") or [])],
                series=e.get("series") is True,
                kind=e.get("kind", ""),
                line_horizons={str(k): [str(h) for h in v] for k, v in (e.get("line_horizons") or {}).items()},
                arms=[str(a) for a in e["arms"]] if e.get("arms") else None,
                arms_by={str(d): {str(v): [str(a) for a in x] for v, x in m.items()} for d, m in (e.get("arms_by") or {}).items()},
            )
    return entries


def manifest_notes(manifest: dict) -> list[Finding]:
    """Where outputs.yml and hooks.md disagree (site.md R12 and related)."""
    notes: list[Finding] = []
    entries = list(manifest.get("outputs") or []) + list(manifest.get("checks") or [])
    bad_ids = [e["id"] for e in entries if not HOOKS_ID_RE.match(e["id"])]
    if bad_ids:
        notes.append(Finding("M1", "warning", "manifest",
            f"ids the hooks.md section 4.1 regex O[A-Z]?[0-9]+[a-z]? does not match: {', '.join(bad_ids)}"))
    list_by = [e["id"] for e in entries if isinstance(e.get("by"), list)]
    if list_by:
        notes.append(Finding("M2", "warning", "manifest",
            f"by is a list, not a map of key to values (hooks.md Q3), so no vocabulary to check: {', '.join(list_by)}"))
    point = [e["id"] for e in entries if e.get("summary") == "point"]
    if point:
        notes.append(Finding("M3", "warning", "manifest",
            f"summary 'point' is not one of the forms in hooks.md section 3.3: {', '.join(point)}"))
    lines = [e["id"] for e in entries if e.get("lines")]
    if lines:
        notes.append(Finding("M4", "warning", "manifest",
            "outputs with lines: hooks.md section 3.2 has no line key for a cell; "
            f"this validator requires a cell field 'line' for: {', '.join(lines)}"))
    return notes


# ── value helpers ────────────────────────────────────────────────────────────

def is_number(v) -> bool:
    return isinstance(v, (int, float)) and not isinstance(v, bool) and math.isfinite(v)


def vstr(v) -> str:
    return str(v)


# ── validation ───────────────────────────────────────────────────────────────

class Validator:
    def __init__(self, data, manifest: dict, manifest_path: Path, inputs_path: Path,
                 mode: str = "default"):
        self.data = data
        self.manifest = manifest
        self.manifest_path = manifest_path
        self.inputs_path = inputs_path
        self.mode = mode
        self.entries = load_entries(manifest)
        self.findings: list[Finding] = []
        run = data.get("run") if isinstance(data, dict) else None
        self.run = run if isinstance(run, dict) else {}
        self.status = self.run.get("status")
        self.input_ids = self._load_input_ids()

    # severity ------------------------------------------------------------
    def strict(self) -> bool:
        """True where V7, V9 and V11 are errors."""
        return self.mode == "final" or (self.status == "final" and self.mode != "fixture")

    def provisional(self) -> bool:
        return self.status == "provisional" and self.mode != "final"

    def add(self, rule: str, level: str, where: str, message: str) -> None:
        self.findings.append(Finding(rule, level, where, message))

    def add_strict(self, rule: str, where: str, message: str) -> None:
        self.add(rule, "error" if self.strict() else "warning", where, message)

    def _load_input_ids(self) -> set[str] | None:
        try:
            doc = json.loads(self.inputs_path.read_text(encoding="utf-8"))
            return {r["id"] for r in doc["inputs"]}
        except (OSError, ValueError, KeyError, TypeError):
            return None

    # driver --------------------------------------------------------------
    def run_all(self) -> list[Finding]:
        d = self.data
        if not isinstance(d, dict):
            self.add("V1", "error", "file", "top level is not a JSON object")
            return self.findings
        self.v1_schema()
        self.v8_run()
        self.v9_inputs_hash()
        self.top_level_fields()
        outputs = d.get("outputs")
        if not isinstance(outputs, dict):
            self.add("V2", "error", "outputs", "missing or not an object")
            outputs = {}
        for oid, entry in outputs.items():
            self.check_output(oid, entry)
        for oid, ent in self.entries.items():
            if oid not in outputs:
                self.add_strict("V7", oid, "manifest id has no entry in the data file")
        self.check_level2(d.get("level2"))
        return self.findings

    # V1 ------------------------------------------------------------------
    def v1_schema(self) -> None:
        if self.data.get("schema") != SCHEMA:
            self.add("V1", "error", "schema", f"expected {SCHEMA!r}, found {self.data.get('schema')!r}")

    def top_level_fields(self) -> None:
        for k in sorted(set(self.data) - TOP_FIELDS):
            self.add("V12", "warning", "file", f"unknown top-level field {k!r}")

    # V8 ------------------------------------------------------------------
    def added_run_fields(self) -> list[str]:
        return [str(k) for k in (self.manifest.get("run_fields_added") or [])]

    def v8_run(self) -> None:
        run = self.data.get("run")
        if not isinstance(run, dict):
            self.add("V8", "error", "run", "missing or not an object")
            return
        for k in RUN_REQUIRED:
            if k not in run:
                self.add("V8", "error", "run", f"missing field {k!r}")
        added = self.added_run_fields()
        for k in added:
            if k not in run:
                self.add("V8", "error" if self.strict() else "warning", "run",
                         f"missing field {k!r} (manifest run_fields_added)")
        if "pack_country" in added and "pack_country" in run and "country_pack" in run \
                and PACK_LABELS.get(run["pack_country"], run["pack_country"]) != run["country_pack"]:
            self.add("V8", "error", "run.pack_country",
                     f"{run['pack_country']!r} must equal run.country_pack {run['country_pack']!r}")
        for k in sorted(set(run) - RUN_FIELDS - set(added)):
            self.add("V12", "warning", "run", f"unknown field {k!r}")
        if "arm" in run and self.run_arm() not in ARMS:
            self.add("V8", "error", "run.arm", f"must be one of {ARMS} (or an object naming one in `arm`), found {run['arm']!r}")
        for t in (run["arm"].get("targets", []) if isinstance(run.get("arm"), dict) else []):   # a grid point that missed its closure target is labelled, with the figure reached beside the target (author, 2026-11-24)
            sf = t.get("shortfalls") if isinstance(t, dict) else None
            if not isinstance(t, dict) or t.get("status") not in ("met", "target_not_met") or (t["status"] == "target_not_met") != bool(sf) or not all(
                    isinstance(v, dict) and all(isinstance(v.get(f), (int, float)) for f in ("reached", "target")) for v in (sf or {}).values()):
                self.add("V8", "error", "run.arm.targets", f"an entry needs status met, or target_not_met with the reached and target figures: {t!r}")
        status = run.get("status")
        if "status" in run and status not in ("provisional", "final"):
            self.add("V8", "error", "run.status", f"must be 'provisional' or 'final', found {status!r}")
        rd = run.get("run_date")
        if "run_date" in run:
            try:
                datetime.date.fromisoformat(str(rd))
            except ValueError:
                self.add("V8", "error", "run.run_date", f"not an ISO date: {rd!r}")
        if "paths" in run and (not isinstance(run["paths"], int) or isinstance(run["paths"], bool) or run["paths"] < 0):
            self.add("V8", "error", "run.paths", "must be a non-negative integer")
        if "base_year" in run and (not isinstance(run["base_year"], int) or isinstance(run["base_year"], bool)):
            self.add("V8", "error", "run.base_year", "must be an integer year")
        if "country_pack" in run and run["country_pack"] != self.manifest.get("country_pack"):
            self.add("V8", "error", "run.country_pack",
                     f"{run['country_pack']!r} but the manifest says {self.manifest.get('country_pack')!r}")
        stale = "warning" if self.mode == "fixture" else "error"
        hint = " (stale fixture: run tests/model/data/make_fixture.py)" if self.mode == "fixture" else ""
        if "manifest_version" in run and run["manifest_version"] != self.manifest.get("version"):
            self.add("V8", stale, "run.manifest_version",
                     f"{run['manifest_version']!r} but the manifest version is {self.manifest.get('version')!r}{hint}")
        if "manifest_sha256" in run:
            actual = sha256_file(self.manifest_path)
            if run["manifest_sha256"] != actual:
                self.add("V8", stale, "run.manifest_sha256",
                         f"does not match the hash of {self.manifest_path.name}{hint}")
        fixture = run.get("fixture") is True
        if self.mode == "fixture" and not fixture:
            self.add("V8", "error", "run.fixture", "--fixture needs run.fixture: true")
        if self.mode == "final":
            if status != "final":
                self.add("V8", "error", "run.status", f"final mode needs status 'final', found {status!r}")
            if fixture:
                self.add("V8", "error", "run.fixture", "a fixture is never final data")
        elif self.mode == "default" and fixture:
            self.add("V8", "warning", "run.fixture", "fixture data, not a model run")

    # V9 ------------------------------------------------------------------
    def v9_inputs_hash(self) -> None:
        want = self.run.get("inputs_sha256")
        if "inputs_sha256" not in self.run:
            return   # already a V8 missing-field error
        actual = sha256_file(self.inputs_path)
        if actual is None:
            msg = f"cannot read {self.inputs_path.name} to check the hash"
        elif want != actual:
            msg = f"does not match the hash of {self.inputs_path.name}"
        else:
            return
        if self.mode == "fixture":
            self.add("V9", "warning", "run.inputs_sha256", msg + " (stale fixture: run tests/model/data/make_fixture.py)")
        else:
            self.add_strict("V9", "run.inputs_sha256", msg)

    def run_arm(self):
        """The run's arm name: run.arm as a string or the `arm` of its label object; absent means legacy."""
        run = self.data.get("run")
        a = run.get("arm", "legacy") if isinstance(run, dict) else "legacy"
        return a.get("arm") if isinstance(a, dict) else a

    # per output ----------------------------------------------------------
    def check_output(self, oid: str, entry) -> None:
        ent = self.entries.get(oid)
        if ent is None:
            self.add("V2", "error", oid, "not an id in the manifest")
            return
        if not isinstance(entry, dict):
            self.add("V2", "error", oid, "entry is not an object")
            return
        for k in sorted(set(entry) - ENTRY_FIELDS):
            self.add("V12", "warning", oid, f"unknown entry field {k!r}")
        if entry.get("summary") != ent.summary:
            self.add("V2", "error", oid, f"summary {entry.get('summary')!r} but the manifest says {ent.summary!r}")
        cells = entry.get("cells")
        if not isinstance(cells, list):
            self.add("V3", "error", oid, "cells missing or not an array")
            return
        if "pending" in entry:   # a labelled pending marker, never a value: only OF1 and CK1, no cells
            if oid not in PENDING_IDS:
                self.add("V7", "error", oid, f"pending is accepted only for {', '.join(PENDING_IDS)}")
            elif not (isinstance(entry["pending"], str) and entry["pending"]) or cells:
                self.add("V7", "error", oid, "a pending entry needs a label and no cells")
            return
        held = ent.arms is not None and "household" not in ent.arms and self.run_arm() == "household"   # an output this arm cannot produce (122c)
        if "withheld" in entry or held:
            if not (held or (oid in MAY_WITHHOLD and self.run_arm() == "household")):
                self.add("V7", "error", oid, f"withheld under arm {self.run_arm()!r}, but the manifest lets this arm produce it")
            elif entry.get("withheld") != "legacy_only":
                self.add("V7", "error", oid, "the household arm cannot produce this id: the entry must carry withheld: legacy_only")
            elif cells:
                self.add("V7", "error", oid, "a withheld entry holds cells; a legacy_only id is never a value")
            return
        part = {(d, v) for d, m in ent.arms_by.items() for v, arms in m.items() if "household" not in arms} if self.run_arm() == "household" else set()
        claim = {(d, v) for d, m in (entry.get("withheld_by") or {}).items() if isinstance(m, dict) for v in m if m[v] == "legacy_only"}
        if claim != part:
            self.add("V7", "error", oid, f"withheld_by {sorted(claim)} but the arm {self.run_arm()!r} withholds {sorted(part)} (manifest arms_by)")
        seen: dict[tuple, int] = {}
        for i, cell in enumerate(cells):
            where = f"{oid} cells[{i}]"
            key = self.check_cell(ent, cell, where)
            if key is None:
                continue
            if key in seen:
                self.add("V4", "error", where, f"same key as cells[{seen[key]}]")
            else:
                seen[key] = i
        for key in seen:
            if any((d, v) in part for d, v in key[2]):
                self.add("V7", "error", oid, f"cells[{seen[key]}] holds a withheld by-value")
        self.check_coverage(ent, set(seen), part)

    def cell_key(self, ent: Entry, cell: dict) -> tuple:
        by = cell.get("by") if isinstance(cell.get("by"), dict) else {}
        return (
            vstr(cell.get("schedule")) if ent.schedules is not None else None,
            vstr(cell.get("horizon")),
            tuple(sorted((k, vstr(v)) for k, v in by.items())),
            vstr(cell.get("line")) if ent.lines else None,
        )

    def check_cell(self, ent: Entry, cell, where: str):
        if not isinstance(cell, dict):
            self.add("V3", "error", where, "cell is not an object")
            return None
        stats = STAT_FIELDS.get(ent.summary, ())
        for k in sorted(set(cell) - CELL_FIELDS - set(stats)):
            self.add("V12", "warning", where, f"unknown cell field {k!r}")
        ok = True
        # schedule
        if ent.schedules is None:
            if "schedule" in cell:
                self.add("V3", "error", where, "output is reported once, not per schedule: remove 'schedule'")
                ok = False
        elif cell.get("schedule") not in ent.schedules:
            self.add("V3", "error", where, f"schedule {cell.get('schedule')!r} not in {ent.schedules}")
            ok = False
        # horizon
        if cell.get("horizon") not in ent.horizons:
            self.add("V3", "error", where, f"horizon {cell.get('horizon')!r} not in {ent.horizons}")
            ok = False
        # by
        by = cell.get("by")
        if not isinstance(by, dict):
            self.add("V3", "error", where, "'by' missing or not an object (use {} for none)")
            ok = False
        else:
            if set(by) != set(ent.by):
                self.add("V3", "error", where,
                         f"by keys {sorted(by)} but the manifest declares {sorted(ent.by)}")
                ok = False
            for k, v in by.items():
                vocab = ent.by.get(k)
                if vocab is not None and vstr(v) not in vocab:
                    self.add("V3", "error", where, f"by.{k} value {v!r} not in {vocab}")
                    ok = False
        # line
        if ent.lines:
            if cell.get("line") not in ent.lines:
                self.add("V3", "error", where, f"line {cell.get('line')!r} not in {ent.lines}")
                ok = False
            else:
                own = ent.line_horizons.get(cell.get("line"))
                if own is not None and cell.get("horizon") in ent.horizons and cell.get("horizon") not in own:
                    self.add("V7", "error", where,
                             f"unexpected cell: line {cell.get('line')!r} is reported only at {own}, "
                             f"not {cell.get('horizon')!r}")
                    ok = False
        elif "line" in cell:
            self.add("V3", "error", where, "output declares no lines: remove 'line'")
            ok = False
        self.check_stats(ent.summary, cell, where, ent.id)
        self.check_series(ent, cell, where)
        return self.cell_key(ent, cell) if ok else None

    # V5, V6 --------------------------------------------------------------
    def check_stats(self, summary: str, obj: dict, where: str, oid: str | None = None) -> None:
        fields = STAT_FIELDS.get(summary)
        if fields is None:
            return   # unknown summary already a V2 error
        vals = {}
        by = obj.get("by") if isinstance(obj.get("by"), dict) else {}
        for f in fields:
            if f not in obj:
                self.add("V5", "error", where, f"missing numeric field {f!r}")
                continue
            v = obj[f]
            if v is None:
                if not self.provisional():
                    self.add("V5", "error", where, f"{f} is null (allowed only in a provisional file)")
            elif v == NO_PAYER and oid in NO_PAYER_IDS and by.get("wealth_band") not in (None, "overall"):
                continue   # stated marker (author, 2026-11-23): the band has no payer at launch; accepted for these ids and a named band only
            elif v == NOT_RUN and oid == "O1e" and f == CENTRE_SLOT[summary]:
                continue
            elif oid == "O1e" and (v in (NOT_DEFINED, NO_SIGN) or (v == NOT_RUN_RUN and f != CENTRE_SLOT[summary])):
                continue   # stated markers (author, 2026-11-23): the safe fund ignores the generator mean; the range over input draws was not run (--o1e-draws 0)
            elif v == NO_CENTRAL and f == CENTRE_SLOT[summary] and self.run_arm() == "household":
                continue   # stated marker (author, 2026-11-23): a range across labelled scenario points has no central value
            elif isinstance(v, str) and v in MARKERS.get(oid, ()):
                continue   # a stated marker (MARKERS), not a number: nothing to compare
            elif not is_number(v):
                self.add("V5", "error", where, f"{f} is not a finite number: {v!r}")
            else:
                vals[f] = v
        if summary == "p10_mean_p90" and "p10" in vals and "p90" in vals:
            if vals["p10"] > vals["p90"]:
                self.add("V6", "error", where, f"p10 {vals['p10']} is above p90 {vals['p90']}")
            elif "mean" in vals and not vals["p10"] <= vals["mean"] <= vals["p90"]:
                self.add("V6", "warning", where, f"mean {vals['mean']} outside [{vals['p10']}, {vals['p90']}]")
        if summary == "point_and_range" and "lo" in vals and "hi" in vals:
            if vals["lo"] > vals["hi"]:
                self.add("V6", "error", where, f"lo {vals['lo']} is above hi {vals['hi']}")
            elif "point" in vals and not vals["lo"] <= vals["point"] <= vals["hi"]:
                self.add("V6", "warning", where, f"point {vals['point']} outside [{vals['lo']}, {vals['hi']}]")

    # V10 -----------------------------------------------------------------
    def check_series(self, ent: Entry, cell: dict, where: str) -> None:
        if "series" not in cell:
            if ent.series:
                self.add_strict("V10", where, "manifest declares series: true but the cell has none")
            return
        if not ent.series:
            self.add("V12", "warning", where, "series on an output the manifest does not declare series: true")
        series = cell["series"]
        if not isinstance(series, list) or not series:
            self.add("V10", "error", where, "series must be a non-empty array")
            return
        ts: list[int] = []
        prev = 0
        for j, pt in enumerate(series):
            pw = f"{where} series[{j}]"
            if not isinstance(pt, dict):
                self.add("V10", "error", pw, "point is not an object")
                continue
            t = pt.get("t")
            if not isinstance(t, int) or isinstance(t, bool):
                self.add("V10", "error", pw, f"t must be an integer, found {t!r}")
                continue
            expected_first = j == 0 and t != 1
            if expected_first:
                self.add("V10", "error", pw, f"series must start at t = 1, found {t}")
            elif j > 0 and t <= prev:
                self.add("V10", "error", pw, f"t {t} does not increase (previous {prev})")
            prev = t
            ts.append(t)
            for k in sorted(set(pt) - {"t"} - set(STAT_FIELDS.get(ent.summary, ()))):
                self.add("V12", "warning", pw, f"unknown series field {k!r}")
            self.check_stats(ent.summary, pt, pw)
        by = cell.get("by") if isinstance(cell.get("by"), dict) else {}
        if "year" in by:
            try:
                year = int(by["year"])
            except (TypeError, ValueError):
                year = None
            if year is None or year not in ts:
                self.add("V10", "error", where, f"reported year {by['year']!r} is not among the series t values")

    # V7, V11 -------------------------------------------------------------
    def expected_keys(self, ent: Entry) -> set[tuple]:
        scheds = ent.schedules if ent.schedules is not None else [None]
        lines = ent.lines or [None]
        declared = {k: v for k, v in ent.by.items() if v is not None}
        names = sorted(declared)
        combos = product(*(declared[n] for n in names)) if names else [()]
        keys = set()
        for s, h, combo, ln in product(scheds, ent.horizons, list(combos), lines):
            if ln is not None and h not in ent.line_horizons.get(ln, ent.horizons):
                continue
            keys.add((s, h, tuple(zip(names, combo)), ln))
        return keys

    def check_coverage(self, ent: Entry, actual: set[tuple], part: frozenset | set = frozenset()) -> None:
        names = sorted(k for k, v in ent.by.items() if v is not None)
        # Project the actual keys onto the declared dimensions; a dimension with
        # no declared vocabulary (list form of by) is not part of coverage.
        projected = {(s, h, tuple((k, v) for k, v in by if k in names), ln) for s, h, by, ln in actual}
        missing = sorted({k for k in self.expected_keys(ent) if not any(p in k[2] for p in part)} - projected, key=str)
        if missing:
            sample = "; ".join(self.describe_key(k) for k in missing[:3])
            more = f" (+{len(missing) - 3} more)" if len(missing) > 3 else ""
            self.add_strict("V7", ent.id, f"{len(missing)} cell(s) missing, e.g. {sample}{more}")
        year_vocab = ent.by.get("year")
        if year_vocab:
            have = {dict(by).get("year") for _, _, by, _ in actual}
            for t in year_vocab:
                if t not in have:
                    self.add_strict("V11", ent.id, f"by.year {t} has no cell")

    @staticmethod
    def describe_key(key: tuple) -> str:
        s, h, by, ln = key
        parts = [x for x in (s, h, ln) if x]
        parts += [f"{k}={v}" for k, v in by]
        return "/".join(parts)

    # level 2 -------------------------------------------------------------
    def check_level2(self, level2) -> None:
        if level2 is None:
            return
        if not isinstance(level2, dict):
            self.add("V3", "error", "level2", "not an object")
            return
        for oid, item in level2.items():
            where = f"level2.{oid}"
            if oid not in self.entries:
                self.add("V2", "error", where, "not an id in the manifest")
                continue
            if not isinstance(item, dict):
                self.add("V3", "error", where, "not an object")
                continue
            for k in sorted(set(item) - LEVEL2_FIELDS):
                self.add("V12", "warning", where, f"unknown field {k!r}")
            for f in ("p10", "p90"):
                v = item.get(f)
                if v is None and f in item and self.provisional():
                    continue
                if not is_number(v):
                    self.add("V5", "error", where, f"{f} is not a finite number: {v!r}")
            if is_number(item.get("p10")) and is_number(item.get("p90")) and item["p10"] > item["p90"]:
                self.add("V6", "error", where, f"p10 {item['p10']} is above p90 {item['p90']}")
            tornado = item.get("tornado")
            if tornado is None:
                continue
            if not isinstance(tornado, list):
                self.add("V3", "error", where, "tornado is not an array")
                continue
            prev = math.inf
            for j, row in enumerate(tornado):
                tw = f"{where}.tornado[{j}]"
                if not isinstance(row, dict):
                    self.add("V3", "error", tw, "not an object")
                    continue
                for k in sorted(set(row) - {"input", "low_effect", "high_effect"}):
                    self.add("V12", "warning", tw, f"unknown field {k!r}")
                if self.input_ids is not None and row.get("input") not in self.input_ids:
                    self.add("V3", "error", tw, f"input {row.get('input')!r} is not a register id")
                lo, hi = row.get("low_effect"), row.get("high_effect")
                if not (is_number(lo) and is_number(hi)):
                    self.add("V5", "error", tw, "low_effect and high_effect must be finite numbers")
                    continue
                size = max(abs(lo), abs(hi))
                if size > prev:
                    self.add("V6", "error", tw, "tornado not in descending order of absolute effect")
                prev = size


def validate(data, manifest: dict, manifest_path: Path = DEFAULT_MANIFEST,
             inputs_path: Path = DEFAULT_INPUTS, mode: str = "default") -> list[Finding]:
    return Validator(data, manifest, manifest_path, inputs_path, mode).run_all()


def report(findings: list[Finding], notes: list[Finding]) -> tuple[list[str], int, int]:
    errors = sum(1 for f in findings if f.level == "error")
    warns = len(findings) - errors
    out: list[str] = []
    if notes:
        out.append("manifest notes (outputs.yml against hooks.md):")
        out += [f"  {n.line()}" for n in notes]
    if findings:
        out.append("findings:")
        out += [f"  {f.line()}" for f in findings]
    out.append("rules:")
    for rule, text in RULES.items():
        e = sum(1 for f in findings if f.rule == rule and f.level == "error")
        w = sum(1 for f in findings if f.rule == rule and f.level == "warning")
        state = "ok" if not (e or w) else f"{e} error(s), {w} warning(s)"
        out.append(f"  {rule:<4} {state:<22} {text}")
    return out, errors, warns


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("file", type=Path, help="output data file (JSON)")
    group = ap.add_mutually_exclusive_group()
    group.add_argument("--final", action="store_true", help="release gate: V7, V9, V11 are errors")
    group.add_argument("--fixture", action="store_true", help="accept a fixture file (run.fixture: true)")
    ap.add_argument("--manifest", type=Path, default=DEFAULT_MANIFEST)
    ap.add_argument("--inputs", type=Path, default=DEFAULT_INPUTS)
    args = ap.parse_args(argv)
    mode = "final" if args.final else "fixture" if args.fixture else "default"
    try:
        data = json.loads(args.file.read_text(encoding="utf-8"))
        manifest = yaml.safe_load(args.manifest.read_text(encoding="utf-8"))
    except (OSError, ValueError, yaml.YAMLError) as exc:
        print(f"validate_outputs: cannot read input: {exc}", file=sys.stderr)
        return 2
    findings = validate(data, manifest, args.manifest, args.inputs, mode)
    lines, errors, warns = report(findings, manifest_notes(manifest))
    run = data.get("run") if isinstance(data, dict) else None
    status = run.get("status") if isinstance(run, dict) else None
    print(f"validate_outputs: {args.file} (mode {mode}, run.status {status})")
    print("\n".join(lines))
    print(f"result: {'FAIL' if errors else 'PASS'} ({errors} error(s), {warns} warning(s))")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
