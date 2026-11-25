"""Shared fixtures for tests/hooks (brief 060c). Loads the pipeline scripts by path; runs on the fixture data file."""
import copy, importlib.util, json, sys
from pathlib import Path
import pytest

ROOT = Path(__file__).resolve().parents[3]
PIPELINE = ROOT / "website" / "build"
MODEL_TOOLS = ROOT / "model" / "tools"   # validate_outputs.py is model-side
FX = Path(__file__).resolve().parent / "fixtures"
DATA = ROOT / "tests" / "model" / "data" / "fixtures" / "outputs.fixture.json"


def load(name, base=PIPELINE):
    spec = importlib.util.spec_from_file_location(name, base / f"{name}.py")
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


@pytest.fixture(scope="session")
def hooks():
    load("validate_outputs", MODEL_TOOLS); load("hook_format")
    return load("hooks")


@pytest.fixture(scope="session")
def fixture_doc():
    return json.loads(DATA.read_text(encoding="utf-8"))


@pytest.fixture()
def doc(fixture_doc):
    return copy.deepcopy(fixture_doc)


@pytest.fixture()
def make(hooks, fixture_doc):
    """make(mode, data=<fixture>, fixture=True) -> Ctx on the fixture bibliography."""
    def _make(mode="draft", data="fixture", fixture=True):
        d = fixture_doc if data == "fixture" else data
        return hooks.Ctx(d, fixture, mode, {"bib": FX / "references.bib"})
    return _make


@pytest.fixture()
def run(hooks, make):
    """run(body, mode, spoke, defaults, ctx) -> result of a spoke built from the body (a few lines)."""
    def _run(body, mode="draft", spoke="PAY", defaults=True, ctx=None):
        dfl = "defaults: {schedule: S_central, horizon: short}\n" if defaults else ""
        text = f"---\nspoke: {spoke}\n{dfl}---\n{body}\n"
        return hooks.resolve_text(text, ctx or make(mode), "t.md")
    return _run


def codes(res, kind="errors", r1r=False):
    """Codes of one result list; the reverse-R1 findings of a three-line spoke are left out unless asked for."""
    return [x["code"] for x in res[kind] if r1r or x["code"] != "R1r"]
