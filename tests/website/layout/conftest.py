"""Fixtures for the layout tests (brief 062s).

Builds a temporary Quarto project from the real site config, the new includes
and styles, the fixture pages and the real 404 page, serves the output over
HTTP and drives Chromium with Playwright. Nothing in website/site/ is written.

Quarto is not on the sandbox PATH by default. Put it on PATH or set QUARTO_BIN
to the executable. Without Quarto the module is skipped, not failed.
"""
import functools
import http.server
import os
import shutil
import subprocess
import threading
from pathlib import Path

import pytest
import yaml

ROOT = Path(__file__).resolve().parents[3]
SITE = ROOT / "website" / "site"
FIXTURES = Path(__file__).resolve().parent / "fixtures"


def _quarto():
    exe = os.environ.get("QUARTO_BIN") or shutil.which("quarto")
    if not exe:
        pytest.skip("Quarto not found: put it on PATH or set QUARTO_BIN", allow_module_level=True)
    return exe


@pytest.fixture(scope="session")
def built_site(tmp_path_factory):
    """Render the fixtures with a temporary copy of the site config; return the _site path."""
    quarto = _quarto()
    proj = tmp_path_factory.mktemp("layout_site")
    shutil.copytree(SITE / "style", proj / "style")
    shutil.copytree(SITE / "includes", proj / "includes")
    for qmd in FIXTURES.glob("*.qmd"):
        shutil.copy2(qmd, proj / qmd.name)
    shutil.copy2(SITE / "pages" / "404.qmd", proj / "404.qmd")

    cfg = yaml.safe_load((SITE / "_quarto.yml").read_text(encoding="utf-8"))
    cfg["project"]["render"] = ["*.qmd"]
    cfg["project"].pop("resources", None)
    cfg.pop("bibliography", None)
    (proj / "_quarto.yml").write_text(yaml.safe_dump(cfg, sort_keys=False), encoding="utf-8")

    done = subprocess.run([quarto, "render"], cwd=proj, capture_output=True, text=True, timeout=600)
    assert done.returncode == 0, done.stdout[-2000:] + done.stderr[-2000:]
    return proj / "_site"


@pytest.fixture(scope="session")
def base_url(built_site):
    class Quiet(http.server.SimpleHTTPRequestHandler):
        def log_message(self, *a, **k):
            pass

    handler = functools.partial(Quiet, directory=str(built_site))
    server = http.server.ThreadingHTTPServer(("127.0.0.1", 0), handler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    yield "http://127.0.0.1:%d" % server.server_address[1]
    server.shutdown()


@pytest.fixture(scope="session")
def browser():
    from playwright.sync_api import sync_playwright
    with sync_playwright() as p:
        b = p.chromium.launch()
        yield b
        b.close()


@pytest.fixture
def open_page(browser, base_url):
    """Open a built page at a viewport size; pages are closed after the test."""
    opened = []

    def _open(name, width=1280, height=900, media=None):
        ctx = browser.new_context(viewport={"width": width, "height": height})
        page = ctx.new_page()
        if media:
            page.emulate_media(media=media)
        page.goto(base_url + "/" + name, wait_until="load")
        opened.append(ctx)
        return page

    yield _open
    for c in opened:
        c.close()
