"""website/registry/glossary.yml and the registry mode of website/build/build_glossary.py (brief 064s)."""
import json
import re
import subprocess
import sys

import pytest
import yaml

import build_glossary as bg
from conftest import FIXTURES, ROOT

SCRIPT = ROOT / "pipeline" / "build_glossary.py"
TEST_ROOT = FIXTURES.parent


def pages(name="pages.yml"):
    return yaml.safe_load((FIXTURES / name).read_text(encoding="utf-8"))


def check(name):
    rows = bg.load_registry(FIXTURES / f"{name}.yml")
    return bg.validate_registry(rows, pages(), root=TEST_ROOT)


def cli(*args):
    return subprocess.run([sys.executable, str(SCRIPT), *map(str, args)], capture_output=True, text=True)


# ── the real registry ─────────────────────────────────────────────────────────

def test_real_registry_validates_in_registry_mode(tmp_path):
    done = cli("--registry", ROOT / "website/registry/glossary.yml", "--pages", ROOT / "website/registry/pages.yml",
               "--out", tmp_path / "g.md", "--lookup", tmp_path / "g.json")
    assert done.returncode == 0, done.stderr


def test_real_registry_rows_are_seeded_with_existing_source_and_owner():
    rows = bg.load_registry(ROOT / "website/registry/glossary.yml")
    ids = {r["id"] for r in yaml.safe_load((ROOT / "website/registry/pages.yml").read_text(encoding="utf-8"))}
    assert len(rows) >= 8
    for r in rows:
        assert r["status"] == "seeded"
        assert (ROOT / r["source"].split(",")[0]).is_file(), r["term"]
        assert r["owner"] in ids


def test_real_seed_definitions_are_verbatim_from_their_source():
    """Copy only: the definition text occurs in the cited file (the S_ rows use two copied sentences)."""
    rows = bg.load_registry(ROOT / "website/registry/glossary.yml")
    for r in rows:
        text = " ".join((ROOT / r["source"].split(",")[0]).read_text(encoding="utf-8").split())
        text = re.sub(r"\s*\(author[^)]*\)", "", text)       # the source's dated author notes are not part of a definition
        for sentence in re.split(r"(?<=\.)\s+", r["definition"]):
            body = re.sub(r"\s*\(author[^)]*\)", "", sentence.rstrip("."))
            assert body.lower()[:60] in text.lower(), (r["term"], body[:60])


# ── fixtures: the good file and every failure ─────────────────────────────────

def test_ok_fixture_is_valid():
    assert check("ok") == []


@pytest.mark.parametrize("name, needle", [
    ("missing_field", "missing field 'aliases'"),
    ("unknown_field", "unknown field 'colour'"),
    ("bad_status", "status 'draft'"),
    ("duplicate_term", "duplicate term"),
    ("alias_equals_term", "collides with the term"),
    ("alias_collision", "collides with an alias"),
    ("alias_own_term", "equals its own term"),
    ("owner_unknown", "not in pages.yml"),
    ("owner_calculator", "cannot own a definition"),
    ("owner_pending", "cannot own a definition"),
    ("owner_legacy", "cannot own a definition"),
    ("owner_site", "cannot own a definition"),
    ("source_missing_file", "does not exist"),
    ("source_absent", "has no source"),
    ("typed_figure", "typed figure"),
    ("typed_figure_pp", "typed figure"),
])
def test_each_failure_is_reported_with_the_term(name, needle):
    errors = check(name)
    hit = [e for e in errors if needle in e]
    assert hit, errors
    assert any(t in hit[0] for t in ("Harbour lamp", "Lamp keeper", "harbour lamp", "Zero tide")), hit[0]


def test_hook_is_accepted():
    assert check("ok") == []      # the Lamp keeper row carries {{o:..}} and {{i:..}} hooks


def test_cli_exit_code_1_on_error(tmp_path):
    done = cli("--registry", FIXTURES / "typed_figure.yml", "--pages", FIXTURES / "pages.yml", "--out", tmp_path / "g.md")
    assert done.returncode == 1
    assert "typed figure" in done.stderr
    assert not (tmp_path / "g.md").exists()


# ── lookup file ───────────────────────────────────────────────────────────────

def build_ok(tmp_path):
    out, look = tmp_path / "g.md", tmp_path / "g.json"
    done = cli("--registry", FIXTURES / "ok.yml", "--pages", FIXTURES / "pages.yml", "--out", out, "--lookup", look)
    assert done.returncode == 0, done.stderr
    return out.read_text(encoding="utf-8"), json.loads(look.read_text(encoding="utf-8"))


def test_lookup_shape_order_slugs_aliases(tmp_path):
    _, data = build_ok(tmp_path)
    assert data["schema"] == "wdt-glossary/1"
    terms = data["terms"]
    assert [t["term"] for t in terms] == ["Harbour lamp", "Lamp keeper", "Zero tide"]
    assert all(set(t) == {"term", "owner", "aliases", "slug"} for t in terms)
    by = {t["term"]: t for t in terms}
    assert by["Harbour lamp"]["slug"] == "harbour-lamp"
    assert by["Harbour lamp"]["aliases"] == ["lighthouse lamp", "lamp"]
    assert by["Zero tide"]["owner"] == "H" and by["Zero tide"]["aliases"] == ["slack water"]


def test_lookup_of_real_registry_has_every_alias(tmp_path):
    out, look = tmp_path / "g.md", tmp_path / "g.json"
    assert cli("--registry", ROOT / "website/registry/glossary.yml", "--pages", ROOT / "website/registry/pages.yml",
               "--out", out, "--lookup", look).returncode == 0
    data = json.loads(look.read_text(encoding="utf-8"))
    rows = {r["term"]: r for r in bg.load_registry(ROOT / "website/registry/glossary.yml")}
    names = [t["term"].lower() for t in data["terms"]]
    assert names == sorted(names)
    for t in data["terms"]:
        assert t["aliases"] == rows[t["term"]]["aliases"]
        assert t["slug"] == bg.slugify(t["term"])


# ── page markup ───────────────────────────────────────────────────────────────

def test_page_markup(tmp_path):
    page, _ = build_ok(tmp_path)
    assert page.startswith('---\ntitle: "Glossary"\n')
    assert page.count('<div class="wdt-glossary-jumpbar">') == 1
    for letter in "HLZ":
        assert f'<a href="#glossary-{letter.lower()}">{letter}</a>' in page
        assert f'<h3 id="glossary-{letter.lower()}" class="wdt-glossary-letter">{letter}</h3>' in page
    assert page.count("wdt-glossary-entry}") == 3                      # one block per term
    assert "::: {#harbour-lamp .wdt-glossary-entry}" in page
    assert "Defined on [Rates and revenue](/fisc.html)" in page       # owner link, from pages.yml
    assert "Defined on [Who pays](/pay.html)" in page
    assert "Defined on [The Wealth Delta Tax](/index.html)" in page
    assert "{{o:O1e}}" in page                                          # hooks pass through unresolved
    assert "Used in" not in page and "not built yet" in page


def test_used_in_only_with_contents(tmp_path):
    papers = tmp_path / "papers"
    papers.mkdir()
    (papers / "p.md").write_text('---\ntitle: "Fixture Paper"\n---\n\n# 1. Lamps\n\nThe harbour lamp is lit.\n', encoding="utf-8")
    contents = tmp_path / "contents.yml"
    contents.write_text('P1:\n  title: Fixture Paper\n  sections:\n    "1": Lamps\n', encoding="utf-8")
    out = tmp_path / "g.md"
    done = cli("--registry", FIXTURES / "ok.yml", "--pages", FIXTURES / "pages.yml", "--out", out,
               "--papers", papers, "--contents", contents)
    assert done.returncode == 0, done.stderr
    page = out.read_text(encoding="utf-8")
    assert "Used in (P1 §1)" in page and "not built yet" not in page


# ── legacy mode unchanged ─────────────────────────────────────────────────────

def test_legacy_mode_output_identical_to_unchanged_script(tmp_path):
    """Run the committed script and the version at HEAD~ of the brief's base on the same inputs."""
    base = subprocess.run(["git", "show", "origin/main:website/build/build_glossary.py"], cwd=ROOT,
                          capture_output=True, text=True)
    if base.returncode != 0:
        pytest.skip("origin/main not available")
    old = tmp_path / "old_build_glossary.py"
    old.write_text(base.stdout, encoding="utf-8")
    papers = tmp_path / "papers"
    papers.mkdir()
    (papers / "p.md").write_text(
        '---\ntitle: "Fixture Paper"\n---\n\n# 1. Lamps\n\nText.\n\n# Glossary\n\n**Harbour lamp:** A lamp lit at dusk.\n',
        encoding="utf-8")
    contents = tmp_path / "contents.yml"
    contents.write_text('P1:\n  title: Fixture Paper\n  sections:\n    "1": Lamps\n', encoding="utf-8")
    a, b = tmp_path / "a.md", tmp_path / "b.md"
    r1 = subprocess.run([sys.executable, str(old), "--papers", str(papers), "--contents", str(contents), "--out", str(a)],
                        capture_output=True, text=True)
    r2 = cli("--papers", papers, "--contents", contents, "--out", b)
    assert r1.returncode == 0 and r2.returncode == 0
    assert a.read_bytes() == b.read_bytes()
