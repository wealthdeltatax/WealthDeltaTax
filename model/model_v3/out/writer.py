"""Output layer, writer: the only module that writes outputs.json.

Deterministic bytes (sorted keys, one indent, UTF-8, floats already rounded by assemble.py), the `run` block with its hashes,
then a call to model/tools/validate_outputs.py, whose non-zero exit raises. Output location, dates and sizes arrive as arguments:
no path, date or environment variable is chosen here (R5, R8). Imports no core and no runner (R4).
"""
from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[3]
VALIDATOR = REPO / "model" / "tools" / "validate_outputs.py"
SCHEMA = "wdt-outputs/1"
REQUIRED = ("status", "run_date", "model_version", "paths", "base_year")   # supplied by the run script, never invented
OPTIONAL = ("pack_country", "pack_sha256", "seed", "level2_draws", "level2_paths", "unfilled_paths", "fixture", "arm")   # arm: the run label of runner/arm.py (121c)


class WriterError(ValueError):
    """The run information is incomplete, or the validator rejected the file."""


def sha256_file(path) -> str:
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def run_block(manifest: dict, manifest_path, inputs_path, levers_path, info: dict) -> dict:
    """The `run` object (hooks.md section 9 and architecture.md 1). `info` holds what only the run knows."""
    missing = [k for k in REQUIRED if k not in info]
    if missing:
        raise WriterError(f"run information missing: {', '.join(missing)}")
    unknown = sorted(set(info) - set(REQUIRED) - set(OPTIONAL))
    if unknown:
        raise WriterError(f"run information not understood: {', '.join(unknown)}")
    run = {k: info[k] for k in (*REQUIRED, *OPTIONAL) if k in info}
    run.setdefault("fixture", False)
    run.update(manifest_version=manifest["version"], manifest_sha256=sha256_file(manifest_path),
               country_pack=manifest["country_pack"], inputs_sha256=sha256_file(inputs_path),
               levers_sha256=sha256_file(levers_path))
    return run


def document(outputs: dict, level2: dict, run: dict) -> dict:
    doc = {"schema": SCHEMA, "run": run, "outputs": outputs}
    if level2:
        doc["level2"] = level2
    return doc


def dumps(doc: dict) -> bytes:
    """The file's bytes. A non-finite number is refused here as a last guard; assemble.py turns it into null or an error first."""
    try:
        return (json.dumps(doc, sort_keys=True, indent=1, ensure_ascii=False, allow_nan=False) + "\n").encode("utf-8")
    except ValueError as exc:
        raise WriterError(f"non-finite number in the document: {exc}") from exc


def write_outputs(out_dir, doc: dict, manifest_path, inputs_path, validator=VALIDATOR) -> Path:
    """Write out_dir/outputs.json, then validate it (default mode, or --final when the run says final). Raises if it fails."""
    path = Path(out_dir) / "outputs.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(dumps(doc))
    cmd = [sys.executable, "-I", str(validator), str(path), "--manifest", str(manifest_path), "--inputs", str(inputs_path)]
    if doc["run"]["status"] == "final":
        cmd.append("--final")
    done = subprocess.run(cmd, capture_output=True, text=True, check=False)
    if done.returncode != 0:
        raise WriterError(f"validate_outputs rejected {path}:\n{done.stdout}{done.stderr}")
    return path
