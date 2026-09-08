"""
wdt_welfare_paths.py
====================
Single source of truth for all paths in the WFR model.
Every module imports from here. Changing the directory layout
means editing exactly one file.
"""
import os
from pathlib import Path

# ── Root: directory containing this file ────────────────────────────────────
_ROOT = Path(__file__).resolve().parent

# ── Inputs ───────────────────────────────────────────────────────────────────
TOML_PATH   = _ROOT / "WDT_Params.toml"

# ── Outputs ──────────────────────────────────────────────────────────────────
OUTPUT_ROOT = _ROOT / "OUTPUTS" / "WFR"

def module_output_dir(module_name: str) -> Path:
    """
    Returns (and creates) the output subdirectory for a given module.
    e.g. module_output_dir("module2") → .../WFR/module2/
    """
    d = OUTPUT_ROOT / module_name
    d.mkdir(parents=True, exist_ok=True)
    return d

# Validate on import
if not TOML_PATH.exists():
    raise FileNotFoundError(
        f"WDT_Params.toml not found at {TOML_PATH}. "
        "Expected layout: model/WDT_Params.toml relative to project root."
    )
