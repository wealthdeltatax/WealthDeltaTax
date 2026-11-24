"""Tests for pipeline/page_cards.py. Run: pytest tests/website/cards"""
import filecmp
import pathlib
import re
import sys

import pytest

ROOT = pathlib.Path(__file__).resolve().parent.parent.parent.parent
sys.path.insert(0, str(ROOT / 'website' / 'build'))
import page_cards as pc  # noqa: E402


@pytest.fixture(scope='module')
def out(tmp_path_factory):
    d = tmp_path_factory.mktemp('cards')
    pc.main(['--out', str(d)])
    return d


def test_26_cards(out):
    names = sorted(p.stem for p in out.glob('*.md'))
    assert len(names) == 26
    assert names == sorted(pc.UNITS)
    assert len(pc.SPOKES) == 22 and len(pc.STANDALONE) == 3


def test_banner_and_blank_question(out):
    for p in out.glob('*.md'):
        t = p.read_text(encoding='utf-8')
        assert 'Do not edit by hand' in t, p.name
        if p.stem in pc.SPOKES:
            assert 'question: ""' in t, p.name
            assert 'status: draft' in t and 'budget: {cap: 6000}' in t, p.name


def ledger_summary():
    """Kept words per page from the table of ledger.md section 2."""
    kept = {}
    sec = False
    for line in pc.LEDGER.read_text(encoding='utf-8').splitlines():
        if line.startswith('## 2.'):
            sec = True
        elif line.startswith('## 3.'):
            break
        elif sec and line.startswith('| ') and not line.startswith('| Page') and not line.startswith('|---'):
            c = [x.strip() for x in line.strip().strip('|').split('|')]
            kept[c[0].split()[0]] = pc.num(c[2])
    return kept


def card_kept(out, unit):
    t = (out / f'{unit}.md').read_text(encoding='utf-8')
    return pc.num(re.search(r'- Kept \(K rows\): ([\d,]+)', t).group(1))


def test_kept_words_match_ledger_section_2(out):
    summary = ledger_summary()
    checked = 0
    for u in pc.SPOKES:
        if u in summary:
            assert card_kept(out, u) == summary[u], u
            checked += 1
    assert checked == 19
    assert card_kept(out, pc.HUB) == summary['H1'] + summary['H2']
    # POL and FALS keep the pre-split rows until the author takes the split; the split pages are empty
    for u in ('ADOPT', 'PILOT', 'HYPO'):
        assert card_kept(out, u) == 0


def test_standalone_words(out):
    want = {'ADD': 6789, 'INST': 14264, 'SCOPE': 2537}
    for u, w in want.items():
        t = (out / f'{u}.md').read_text(encoding='utf-8')
        assert pc.num(re.search(r'- Standalone \(SA rows\): ([\d,]+)', t).group(1)) == w, u


def test_every_element_entry_on_exactly_its_pages(out):
    outputs = pc.read_outputs()
    for o in outputs:
        pages = {pc.pages_of_element(e) for e in o['element']}
        on = set()
        for p in out.glob('*.md'):
            t = p.read_text(encoding='utf-8')
            sect = t.split('## Outputs whose')[1].split('## Register')[0]
            if re.search(rf'^\| {re.escape(o["id"])} \|', sect, re.M):
                on.add(p.stem)
        assert on == pages, (o['id'], on, pages)


def test_spoke_front_matter_outputs_equal_manifest(out):
    outputs = pc.read_outputs()
    for u in pc.SPOKES:
        want = [o['id'] for o in outputs if u in o['element']]
        t = (out / f'{u}.md').read_text(encoding='utf-8')
        got = re.search(r'^outputs: \[(.*?)\]', t, re.M).group(1)
        assert [x.strip() for x in got.split(',') if x.strip()] == want, u


def test_rerun_changes_nothing(tmp_path):
    a, b = tmp_path / 'a', tmp_path / 'b'
    pc.main(['--out', str(a)])
    pc.main(['--out', str(b)])
    cmp = filecmp.dircmp(a, b)
    assert not cmp.diff_files and not cmp.left_only and not cmp.right_only
    for f in a.glob('*.md'):
        assert f.read_bytes() == (b / f.name).read_bytes()


def test_committed_cards_are_current(out):
    committed = pc.DEFAULT_OUT
    if not committed.exists():
        pytest.skip('cards not generated yet')
    for f in out.glob('*.md'):
        assert (committed / f.name).read_bytes() == f.read_bytes(), f.name
