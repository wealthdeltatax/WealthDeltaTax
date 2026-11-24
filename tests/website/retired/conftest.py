"""Put website/build/ on sys.path (its modules import each other by bare name)."""
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "website" / "build"))

import config as cfg  # noqa: E402
from pages import retired as R  # noqa: E402


@pytest.fixture(scope="session")
def pages():
    return cfg.load_pages()


@pytest.fixture(scope="session")
def retired():
    return R.load_retired()


@pytest.fixture(scope="session")
def ledger():
    return R.parse_ledger(R.LEDGER_MD.read_text(encoding="utf-8"))


@pytest.fixture(scope="session")
def page_text(pages, retired):
    return R.generate_page(retired, pages)
