"""Shared constants and a slot filler for the layout tests (brief 062s)."""

# Page type -> fixture page (the file name in the built site).
SPOKE_LIKE = ["spoke.html", "parent.html", "standalone.html", "standalone-scope.html"]
ALL_PAGES = [
    "index.html", "spoke.html", "spoke-draft.html", "parent.html", "standalone.html",
    "standalone-scope.html", "data-layer.html", "utility.html", "404.html",
]
ANCHORS = ["#short-answer", "#evidence", "#strongest-objection", "#data"]

# Stands in for what the builder (B15) puts into the empty slots: long, awkward
# content, so the layout is tested at its worst and not on empty frames.
FILL_JS = r"""
() => {
  const put = (sel, html) => document.querySelectorAll(sel).forEach(el => { el.innerHTML = html; });
  const steps = (n) => {
    const names = ["Hub", "A parent spoke with a rather long working title", "The appendix of the parent spoke"];
    return names.slice(0, n).map((t, i) => `<li><a href="#s${i}">${t}</a></li>`).join("");
  };
  document.querySelectorAll("[data-slot='breadcrumb']").forEach(ol => {
    ol.innerHTML = steps(parseInt(ol.dataset.steps || "2", 10) + 0);
  });
  put("[data-slot='status-chip']", "Draft");
  put("[data-slot='prerequisites']", 'Assumes: <a href="#a">MECH</a>, <a href="#b">VALU</a>');
  put("[data-slot='more-detail']", 'More detail: <a href="#c">DECL Declaration incentives</a>');
  put("[data-slot='run-record']", "Run 2026-01-01 · manifest version 1");
  put("[data-slot='placeholder-count']", "3 placeholders");
  put("[data-slot='parent-id']", "PARENT");
  put("[data-slot='parent-question']", ", what is the parent question of this fixture?");
  const row = (c) => "<tr>" + Array.from({length: 14}, (_, i) => `<${c}>col ${i + 1} header text</${c}>`).join("") + "</tr>";
  put("[data-slot='data-summary']", '<p>Outputs cited: OX1, OX2. Run: fixture. Replicate: none. https://example.org/a/very/long/unbroken/link/that/has/no/natural/break/points/at/all/0123456789</p>');
  put("[data-slot='data-tables']",
    '<details class="wdt-reftable"><summary>Table F-FX-1 (14 columns)</summary>' +
    '<div class="wdt-table-wrap"><table><thead>' + row("th") + "</thead><tbody>" + row("td") + row("td") + "</tbody></table></div></details>");
  put("[data-slot='read-next']", '<a href="#n1">Next spoke with a long title that wraps on a phone</a>');
  put("[data-slot='numbers-list']", '<details><summary>Outputs cited</summary><p>OX1</p></details>');
  const card = (t) => `<a class="wdt-routing-card" href="#r">${t}</a>`;
  put("[data-slot='routing-block']", ["I want the short version", "I want to check the numbers", "I think it is unfair",
        "I run a business", "I work in tax administration", "I want the full argument"].map(card).join(""));
}
"""
