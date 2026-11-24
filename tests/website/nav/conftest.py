"""Put pipeline/ on sys.path (its modules import each other by bare name)."""
import copy
import sys
from pathlib import Path

import pytest
import yaml

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "pipeline"))
FIXTURES = Path(__file__).resolve().parent / "fixtures"

import config as cfg  # noqa: E402
from pages import nav, routing  # noqa: E402


@pytest.fixture
def rows():
    return cfg.load_pages(FIXTURES / "pages_nav.yml")


@pytest.fixture
def spokes_dir():
    return FIXTURES / "spokes"


@pytest.fixture
def infos(rows, spokes_dir):
    return routing.spoke_infos(rows, spokes_dir)[0]


@pytest.fixture
def routes():
    return routing.load_routing(FIXTURES / "routing_ok.yml")


@pytest.fixture
def broken(tmp_path):
    """Write a routing file with one change applied to the good one, and load it back."""
    def make(mutate):
        data = yaml.safe_load((FIXTURES / "routing_ok.yml").read_text(encoding="utf-8"))
        mutate(data["routes"])
        p = tmp_path / "routing_broken.yml"
        p.write_text(yaml.safe_dump(data), encoding="utf-8")
        return routing.load_routing(p)
    return make
