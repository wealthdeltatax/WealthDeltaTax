# Layout partials and styles (brief 062s)

One place for the class, anchor and slot names that B6 (checker), B7 (navigation) and B15 (integration) rely on. Do not rename without updating all three.

Styles: `website/site/style/spoke.css` (screen) and `website/site/style/print.css` (print). Neither is in the global `format.html.css` yet; a page that uses them lists them in its own `css:`. Partials are static HTML. An empty slot is an empty element: the builder fills it, CSS hides it while empty.

## Placement

| Partial | Where | Page types |
|---|---|---|
| `spoke-head.html` | `include-before-body` | spoke, standalone (breadcrumb 2 steps + status chip) |
| `parent-head.html` | `include-before-body` | parent-reached spoke (breadcrumb 3 steps) |
| `hub-head.html` | `include-before-body` | hub (chip only) |
| `datalayer-head.html` | `include-before-body` | data-layer page (breadcrumb, chip, run record) |
| `banner-draft.html` | before-body, after head | any page in draft mode |
| `banner-parent.html` | before-body | parent-reached spoke |
| `banner-standalone.html`, `banner-standalone-scope.html` | before-body | standalone; the scope variant adds one sentence to the standard text |
| `draft-head.html` | `include-in-header` | draft mode only (`noindex`) |
| `print-chrome.html` | `include-after-body` | every page (print header/footer, details opener) |
| `spoke-nav.html` | raw block in body, after Short answer | spoke types (prerequisites slot, jump bar, more-detail slot) |
| `spoke-data.html` | raw block, end of body | spoke (`#data`) |
| `spoke-read-next.html` | raw block, last | spoke |
| `hub-contents.html` | raw block | hub (8-entry contents, links `#h0`..`#h7`) |
| `hub-numbers.html` | raw block | hub (`#numbers`) |
| `routing-slot.html` | raw block | hub, 404 |

Include inside body with a ```` ```{=html} ```` block containing `{{< include includes/X.html >}}`.

## Authored blocks (fenced divs, not partials)

`.wdt-short-answer #short-answer`, `.wdt-evidence #evidence`, `.wdt-objection #strongest-objection`, `.wdt-table-wrap` (wide tables), `.wdt-utility` (404 and other non-spoke pages).

## Spoke order

Head, banners, title, Short answer, `spoke-nav`, Evidence, Strongest objection, `spoke-data`, `spoke-read-next`.

## Slots (`data-slot`)

breadcrumb (`data-steps`), status-chip, prerequisites, more-detail, run-record, placeholder-count, parent-link, parent-id, parent-question, data-summary, data-tables, read-next, numbers-list, routing-block, print-title, print-draft, print-url. Footer: `data-run-date`, `data-manifest-version`. Routing cards are `a.wdt-routing-card`.

## Notes

- Fixtures set `toc: false`; hub pages must too, since the hub has its own contents list.
- Print: chrome hidden, `details` forced open, fixed header/footer on every sheet.
- Tests: `tests/website/layout/` (needs Quarto on PATH or `QUARTO_BIN`).
