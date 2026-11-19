"""Layout tests for brief 062s: page types, draft/release, mobile, print, tap targets, redirect, 404."""
import re

import pytest

from layout_helpers import ALL_PAGES, ANCHORS, FILL_JS, SPOKE_LIKE


def html(built_site, name):
    return (built_site / name).read_text(encoding="utf-8")


# (a) structure per page type ------------------------------------------------

@pytest.mark.parametrize("name", ["spoke.html", "parent.html", "standalone.html", "standalone-scope.html"])
def test_spoke_like_jump_bar_and_sections(open_page, name):
    page = open_page(name)
    links = page.eval_on_selector_all(".wdt-jumpbar a", "els => els.map(e => '#' + e.getAttribute('href').split('#').pop())")
    assert links == ANCHORS
    for a in ANCHORS:
        assert page.locator(a).count() == 1, a


def test_hub_contents_and_no_jump_bar(open_page):
    page = open_page("index.html")
    assert page.locator(".wdt-jumpbar").count() == 0
    assert page.locator(".wdt-hubnav a").count() == 8
    for i in range(8):
        assert page.locator(f"#h{i}").count() == 1


def test_parent_reached_banner_and_breadcrumb_slot(open_page):
    page = open_page("parent.html")
    assert "More detail for" in page.locator(".wdt-banner--parent").inner_text()
    assert page.locator("[data-slot='breadcrumb'][data-steps='3']").count() == 1


def test_spoke_breadcrumb_slot_two_steps(open_page):
    page = open_page("spoke.html")
    assert page.locator("[data-slot='breadcrumb'][data-steps='2']").count() == 1


def test_standalone_banners(open_page):
    plain = open_page("standalone.html").locator(".wdt-banner").inner_text()
    assert "Standalone paper. The argument in the hub does not depend on it." in plain
    scope = open_page("standalone-scope.html").locator(".wdt-banner").inner_text()
    assert "Standalone paper." in scope and "Outside the argument; sets the project's boundaries." in scope


def test_spoke_has_data_section_and_read_next_slot(open_page):
    page = open_page("spoke.html")
    assert page.locator("#data [data-slot='data-tables']").count() == 1
    assert page.locator(".wdt-readnext [data-slot='read-next']").count() == 1


# (b) draft vs release -----------------------------------------------------------

def test_draft_has_banner_and_noindex(built_site):
    d = html(built_site, "spoke-draft.html")
    assert "Draft: numbers are not final" in d
    assert re.search(r'<meta name="robots" content="noindex"', d)


def test_release_has_neither(built_site):
    r = html(built_site, "spoke.html")
    assert "Draft: numbers are not final" not in r
    assert "noindex" not in r


# (c) mobile -------------------------------------------------------------------------

@pytest.mark.parametrize("name", ALL_PAGES)
def test_no_horizontal_scroll_375(open_page, name):
    page = open_page(name, 375, 700)
    assert page.evaluate("document.documentElement.scrollWidth") <= 375


@pytest.mark.parametrize("name", ALL_PAGES)
def test_no_horizontal_scroll_375_filled(open_page, name):
    page = open_page(name, 375, 700)
    page.evaluate(FILL_JS)
    assert page.evaluate("document.documentElement.scrollWidth") <= 375


def test_short_answer_in_first_viewport_360(open_page):
    page = open_page("spoke.html", 360, 640)
    assert page.locator(".navbar-toggler").is_visible(), "navbar should be collapsed at 360px"
    bottom = page.evaluate("document.querySelector('#short-answer').getBoundingClientRect().bottom")
    assert 0 < bottom <= 640, bottom


# (d) print ------------------------------------------------------------------------------

HIDDEN_IN_PRINT = [".navbar", ".wdt-jumpbar", ".wdt-readnext", ".wdt-footer-menu", ".nav-footer"]


def displayed(page, sel):
    return page.evaluate(
        "s => Array.from(document.querySelectorAll(s)).some(e => getComputedStyle(e).display !== 'none')", sel)


@pytest.mark.parametrize("name", ["spoke.html", "index.html"])
def test_print_hides_chrome(open_page, name):
    page = open_page(name, media="print")
    for sel in HIDDEN_IN_PRINT:
        assert not displayed(page, sel), sel


def test_print_details_content_visible(open_page):
    page = open_page("spoke.html", media="print")
    page.evaluate(FILL_JS)
    page.evaluate("window.dispatchEvent(new Event('beforeprint'))")
    n = page.evaluate("document.querySelectorAll('details').length")
    assert n > 0
    assert page.evaluate("Array.from(document.querySelectorAll('details')).every(d => d.open)")
    assert page.locator(".wdt-reftable table").is_visible()


def test_print_details_content_visible_without_script(open_page):
    """CSS alone must show closed details content (the ::details-content rule)."""
    page = open_page("spoke.html", media="print")
    page.evaluate(FILL_JS)
    assert page.locator(".wdt-reftable table").is_visible()


def test_closed_on_screen(open_page):
    page = open_page("spoke.html")
    page.evaluate(FILL_JS)
    assert not page.locator(".wdt-reftable table").is_visible()


def test_print_header_footer_shown_in_print_hidden_on_screen(open_page):
    screen = open_page("spoke.html")
    assert not displayed(screen, ".wdt-print-header")
    assert not displayed(screen, ".wdt-print-footer")
    pr = open_page("spoke.html", media="print")
    assert displayed(pr, ".wdt-print-header")
    assert displayed(pr, ".wdt-print-footer")


# (e) tap targets ---------------------------------------------------------------------------

def test_tap_targets_375(open_page):
    page = open_page("spoke.html", 375, 700)
    page.evaluate(FILL_JS)
    sizes = page.evaluate("""() => Array.from(document.querySelectorAll('.wdt-jumpbar a, .wdt-routing-slot a, .wdt-breadcrumb a'))
        .map(a => [a.className || a.textContent.slice(0, 20), a.getBoundingClientRect().height])""")
    assert sizes
    small = [s for s in sizes if s[1] < 44]
    assert not small, small


def test_routing_slot_links_tap_375(open_page):
    page = open_page("index.html", 375, 700)
    page.evaluate(FILL_JS)
    hs = page.evaluate("Array.from(document.querySelectorAll('.wdt-routing-slot a')).map(a => a.getBoundingClientRect().height)")
    assert len(hs) == 6 and min(hs) >= 44


# (f) hub redirect ----------------------------------------------------------------------------

def test_wp_redirect(built_site, base_url, open_page):
    assert (built_site / "wp.html").exists()
    assert "index.html" in html(built_site, "wp.html")
    page = open_page("wp.html")
    page.wait_for_url(re.compile(r"/(index\.html)?$"), timeout=5000)


# (g) 404 -------------------------------------------------------------------------------------

def test_404_links_hub_and_has_routing_slot(built_site):
    h = html(built_site, "404.html")
    assert re.search(r'<a href="/"[^>]*>Go to the hub</a>', h)
    assert 'data-slot="routing-block"' in h
