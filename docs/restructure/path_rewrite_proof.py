#!/usr/bin/env python3
"""Proof that a restructure stage changed paths and nothing else (044c, tier 2).

    python docs/restructure/path_rewrite_proof.py --base <pre-move commit> [--head HEAD] [--map file-layout-map.csv]

For every file of the map (old path, new path) it reads the old bytes at --base and
the new bytes at --head and reports one of:
  moved       the bytes are identical (a pure rename)
  path-only   the new bytes equal the old bytes after every old path named in them
              is replaced by its new path (files exactly; folders when all their
              files move by one common rule)
  changed     anything else: listed with the number of differing lines, for the
              stage report to explain (depth shifts, renamed readers, deliberate edits)
  pending     the file is still at its old path (stage not yet run)
  removed     a byte-identical duplicate (R4) that is gone
Files at --head that the map does not know are listed as `added`.
Exit code 0 only if nothing is `changed` or `added` that the stage did not declare
with --allow (a text file of paths, one per line, new paths of declared edits).
"""
import argparse, csv, difflib, subprocess, sys
from pathlib import Path

ROOT = Path(subprocess.run(['git', 'rev-parse', '--show-toplevel'], capture_output=True, text=True).stdout.strip() or '.')


def git(*a, raw=False):
    r = subprocess.run(['git', '-c', 'core.quotepath=off', '-C', str(ROOT), *a], capture_output=True)
    if r.returncode:
        return None
    return r.stdout if raw else r.stdout.decode('utf-8', 'replace')


def read_map(path):
    with open(path, newline='', encoding='utf-8') as fh:
        return list(csv.DictReader(fh))


def rewriter(rows):
    """The one rewrite rule of the programme: pipeline/path_refs.py (project/tools/ after 164c), shared with --apply."""
    for d in ('pipeline', 'project/tools'):
        if (ROOT / d / 'path_refs.py').is_file():
            sys.path.insert(0, str(ROOT / d))
            break
    import path_refs
    return path_refs.Rewriter({r['old']: r for r in rows}).text


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--base', required=True)
    ap.add_argument('--head', default='HEAD')
    ap.add_argument('--map', default=str(ROOT / 'docs/restructure/file-layout-map.csv'))
    ap.add_argument('--allow', help='file listing new paths whose edits the stage declares')
    ap.add_argument('--show', type=int, default=0, help='print the first N differing lines of each changed file')
    a = ap.parse_args()
    rows = read_map(a.map)
    rw = rewriter(rows)
    allow = set(Path(a.allow).read_text().split()) if a.allow else set()
    head_files = set((git('ls-tree', '-r', '--name-only', a.head) or '').splitlines())
    known, tally, bad = set(), {}, []
    for r in rows:
        o, n = r['old'], r['new']
        old = git('show', f'{a.base}:{o}', raw=True)
        if r['duplicate_of']:
            st = 'removed' if o not in head_files else 'pending'
            tally.setdefault(st, []).append(o)
            continue
        known.add(n)
        if old is None:
            tally.setdefault('changed', []).append(f'{o} (not in base)'); bad.append(o); continue
        new = git('show', f'{a.head}:{n}', raw=True)
        if new is None:
            st = 'pending' if o in head_files else 'changed'
            tally.setdefault(st, []).append(o + ('' if st == 'pending' else ' (neither old nor new path exists)'))
            if st == 'changed': bad.append(o)
            continue
        known.add(o) if o in head_files else None
        if new == old:
            tally.setdefault('moved', []).append(n); continue
        try:
            ot, nt = old.decode('utf-8'), new.decode('utf-8')
        except UnicodeDecodeError:
            tally.setdefault('changed', []).append(f'{n} (binary differs)'); bad.append(n); continue
        if rw(ot) == nt:
            tally.setdefault('path-only', []).append(n); continue
        d = [l for l in difflib.unified_diff(rw(ot).splitlines(), nt.splitlines(), lineterm='', n=0) if l[:1] in '+-' and l[:3] not in ('+++', '---')]
        tally.setdefault('changed', []).append(f'{n} ({len(d)} lines differ after the path rewrite)')
        if n not in allow:
            bad.append(n)
        for l in d[:a.show]:
            print(f'   {n}: {l[:160]}')
    added = sorted(head_files - known - {r['old'] for r in rows} - allow)
    for k in ('moved', 'path-only', 'removed', 'pending', 'changed'):
        v = tally.get(k, [])
        print(f'{k:10} {len(v)}')
        if k == 'changed' or (k == 'path-only' and a.show) or (k == 'pending' and v and len(v) < 20):
            for x in v[:200]:
                print('   ', x)
    print(f'{"added":10} {len(added)}')
    for x in added[:200]:
        print('   ', x)
    undeclared = [x for x in added if not x.startswith(('docs/restructure/', 'pipeline/path_refs'))]
    bad += undeclared
    print('PASS' if not bad else f'FAIL: {len(bad)} files changed or added beyond a path rewrite')
    return 1 if bad else 0


if __name__ == '__main__':
    sys.exit(main())
