"""Shared fixtures for tests/model/data (brief 030c). Loads the pipeline scripts by path."""

from __future__ import annotations

import copy
import importlib.util
import json
import sys
from pathlib import Path

import pytest
import yaml

ROOT = Path(__file__).resolve().parents[3]
PIPELINE = ROOT / "model" / "tools"
FIXTURE = Path(__file__).resolve().parent / "fixtures" / "outputs.fixture.json"
MANIFEST = ROOT / "model-specs" / "outputs.yml"
INPUTS_JSON = ROOT / "data" / "input-register" / "inputs.json"
METRICS_JSON = ROOT / "data" / "input-register" / "metrics.json"
INPUTS_MD = ROOT / "model-specs" / "inputs.md"
METRICS_MD = ROOT / "model-specs" / "metrics.md"


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


@pytest.fixture(scope="session")
def build_inputs():
    return load_module("build_inputs", PIPELINE / "build_inputs.py")


@pytest.fixture(scope="session")
def build_metrics():
    return load_module("build_metrics", PIPELINE / "build_metrics.py")


@pytest.fixture(scope="session")
def vo():
    return load_module("validate_outputs", PIPELINE / "validate_outputs.py")


@pytest.fixture(scope="session")
def make_fixture():
    return load_module("make_fixture", Path(__file__).resolve().parent / "make_fixture.py")


@pytest.fixture(scope="session")
def manifest():
    return yaml.safe_load(MANIFEST.read_text(encoding="utf-8"))


@pytest.fixture(scope="session")
def fixture_doc():
    return json.loads(FIXTURE.read_text(encoding="utf-8"))


@pytest.fixture()
def doc(fixture_doc):
    """A private copy of the fixture to mutate."""
    return copy.deepcopy(fixture_doc)
