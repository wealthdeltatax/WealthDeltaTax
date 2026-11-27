"""build_lane_plan.py -- the lane plan and the STATUS agent table, generated from the open briefs' header lines (brief 184c).

  python -I project/tools/build_lane_plan.py            rewrite the generated parts
  python -I project/tools/build_lane_plan.py --check    exit 1 and print a diff if they differ from what the headers say
Exit 2 on a malformed header, naming the file and line.

Header lines of a brief in project/briefs/open/ (before its first `## `):
  - **Status:** underway | review | ready | author | hold   (draft and parked read as hold; the rest of the line is free text)
  - **Agent:** 2 to 6, author, openai (the OpenAI agent), or none
  - **Needs:** 151c, 154c, ~176c   (ids of open briefs or rows; ~ = soft, same files so keep in order; ids of briefs in done/ count as met; none when empty)
  - **Length:** sessions (default 1)
  - **Row:** 183a | agent 4 | ready | needs none | length 1 | Split run, stage A   (optional, repeatable: an extra plan row for a stage that runs apart)
Generated: the B array and the lane notes of project/lane-plan.html (between `// plan:start` and `// plan:end`, `// lanes:start` and `// lanes:end`)
and the agent table of project/STATUS.md (between `<!-- agents:start -->` and `<!-- agents:end -->`). Agent 1, the author lane and the held lane
keep fixed text from project/lane-plan-lanes.json."""
from __future__ import annotations

import argparse
import difflib
import json
import re
import sys
from pathlib import Path

STATUS_WORDS = {'underway': 'under', 'review': 'review', 'ready': 'ready', 'author': 'author', 'hold': 'hold', 'draft': 'hold', 'parked': 'hold'}
RANK = {'under': 0, 'review': 1, 'ready': 2, 'author': 3, 'hold': 4}    # the page's pack() order inside a lane
AGENTS = {'2', '3', '4', '5', '6'}
OTHERS = {'author', 'none', 'openai'}   # openai: the OpenAI agent (notes only, no repo access beyond a branch); lane O
ID = r'\d+[a-z]'
HEAD = re.compile(r'^- \*\*(Status|Agent|Needs|Length|Row):\*\*\s*(.*?)\s*$')
FILES_CUT = 60


class Brief:
    def __init__(self, id, file, line, title, goal, touches, agent, needs, length, status, is_row=False):
        self.id, self.file, self.line, self.title, self.goal, self.touches = id, file, line, title, goal, touches
        self.agent, self.needs, self.length, self.status, self.is_row = agent, needs, length, status, is_row


def parse_needs(text: str):
    """'151c, 154c, ~176c' -> [(id, soft)]; 'none' or '' -> []; None when a token is not an id."""
    text = text.strip()
    if text.lower() in ('', 'none'):
        return []
    out = []
    for tok in re.split(r'\s*,\s*', text):
        m = re.fullmatch(r'(~?)(' + ID + ')', tok.strip())
        if not m:
            return None
        out.append((m.group(2), bool(m.group(1))))
    return out


def status_of(text: str):
    m = re.match(r'(\w+)', text.strip())
    return STATUS_WORDS.get(m.group(1).lower()) if m else None


def section(lines: list[str], name: str) -> str:
    """The first non-empty text line after `## name` (empty if none)."""
    for i, l in enumerate(lines):
        if l.strip() == '## ' + name:
            for m in lines[i + 1:]:
                if m.startswith('## '):
                    return ''
                if m.strip():
                    return m.strip()
    return ''


def first_sentence(text: str) -> str:
    text = re.sub(r'\s+', ' ', text.strip())
    m = re.search(r'(?<=[.!?])\s', text)
    return text[:m.start()] if m else text


def parse_brief(path: Path, root: Path):
    """-> (briefs, errors): the brief's own row and its Row: lines; errors are 'file:line message'."""
    rel, lines, errors = path.relative_to(root).as_posix(), path.read_text(encoding='utf-8').splitlines(), []
    bid = re.match(r'(' + ID + r')-', path.name)
    if not bid:
        return [], [f'{rel}:1 file name does not start with a brief id like 184c-']
    bid = bid.group(1)
    h1 = next((l for l in lines if l.startswith('# ')), '')
    title = re.sub(r'^#\s+\d+\w?:\s*', '', h1).strip() or h1[2:].strip()
    seen, rows, line_of = {}, [], {}
    for n, l in enumerate(lines, 1):
        if l.startswith('## '):
            break
        m = HEAD.match(l)
        if not m:
            continue
        key, val = m.group(1), m.group(2)
        if key == 'Row':
            rows.append((n, val))
        elif key in seen:
            errors.append(f'{rel}:{n} second {key} line')
        else:
            seen[key], line_of[key] = val, n
    for key in ('Status', 'Agent', 'Needs'):
        if key not in seen:
            errors.append(f'{rel}:1 missing header line "- **{key}:** ..."')
    goal, touches = first_sentence(section(lines, 'Goal')), re.sub(r'`', '', section(lines, 'Touches'))
    if len(touches) > FILES_CUT:
        touches = touches[:FILES_CUT].rstrip() + '…'
    if errors:
        return [], errors
    st = status_of(seen['Status'])
    if st is None:
        errors.append(f'{rel}:{line_of["Status"]} unknown status word in "{seen["Status"][:40]}" (use underway, review, ready, author, hold)')
    agent = seen['Agent'].strip().lower()
    if agent not in AGENTS | OTHERS:
        errors.append(f'{rel}:{line_of["Agent"]} agent "{seen["Agent"]}" is not 2 to 6, author, openai or none')
    needs = parse_needs(seen['Needs'])
    if needs is None:
        errors.append(f'{rel}:{line_of["Needs"]} Needs "{seen["Needs"]}" is not a list of ids like 151c, ~176c or none')
    length = 1
    if 'Length' in seen:
        if re.fullmatch(r'[1-9]\d*', seen['Length'].strip()):
            length = int(seen['Length'])
        else:
            errors.append(f'{rel}:{line_of["Length"]} Length "{seen["Length"]}" is not a whole number of sessions')
    out = [Brief(bid, rel, line_of['Status'], title, goal, touches, agent, needs or [], length, st)]
    for n, val in rows:
        f = [x.strip() for x in val.split('|')]
        m = len(f) == 6 and re.fullmatch(ID, f[0]) and re.fullmatch(r'agent (\d|author|openai|none)', f[1]) and re.fullmatch(r'needs (.*)', f[3]) and re.fullmatch(r'length ([1-9]\d*)', f[4])
        if not m:
            errors.append(f'{rel}:{n} Row line is not "id | agent N | status | needs LIST | length N | text"')
            continue
        rs, rn = status_of(f[2]), parse_needs(re.fullmatch(r'needs (.*)', f[3]).group(1))
        ra = re.fullmatch(r'agent (.*)', f[1]).group(1)
        if rs is None or rn is None or ra not in AGENTS | OTHERS:
            errors.append(f'{rel}:{n} Row line has an unknown status, agent or needs')
            continue
        out.append(Brief(f[0], rel, n, f[5], goal, touches, ra, rn, int(f[4].split()[1]), rs, is_row=True))
    return out, errors


def load(root: Path):
    """-> (briefs, done_ids, errors). Errors cover headers, unknown Needs ids, duplicate ids and cycles."""
    briefs, errors = [], []
    for p in sorted((root / 'project/briefs/open').glob('*.md')):
        b, e = parse_brief(p, root)
        briefs += b
        errors += e
    done = {m.group(1) for p in (root / 'project/briefs/done').glob('*.md') if (m := re.match(r'(' + ID + r')-', p.name))}
    ids = {}
    for b in briefs:
        if b.id in ids:
            errors.append(f'{b.file}:{b.line} id {b.id} is also used in {ids[b.id].file}')
        ids[b.id] = b
    for b in briefs:
        for nid, _ in b.needs:
            if nid not in ids and nid not in done:
                errors.append(f'{b.file}:{b.line} {b.id} needs {nid}, which is neither an open brief nor in done/')
            if nid == b.id:
                errors.append(f'{b.file}:{b.line} {b.id} needs itself')
    if not errors:
        errors += cycles(briefs)
    return briefs, done, errors


def cycles(briefs):
    ids = {b.id: b for b in briefs}
    state, errors = {}, []

    def visit(x, path):
        state[x] = 1
        for nid, _ in ids[x].needs:
            if nid not in ids:
                continue
            if state.get(nid) == 1:
                errors.append(f'{ids[x].file}:{ids[x].line} needs cycle: ' + ' -> '.join(path[path.index(nid):] + [nid] if nid in path else path + [nid]))
            elif nid not in state:
                visit(nid, path + [nid])
        state[x] = 2
    for b in briefs:
        if b.id not in state:
            visit(b.id, [b.id])
    return errors


def problems(root: Path) -> list[str]:
    return load(root)[2]


def lane_of(b: Brief) -> str:
    return {'author': 'E', 'none': 'G', 'openai': 'O'}.get(b.agent, b.agent)


def depth(b, by_id, seen=None):
    seen = seen if seen is not None else set()
    if b.id in seen:
        return 0
    seen.add(b.id)
    return max([1 + depth(by_id[n], by_id, seen) for n, _ in b.needs if n in by_id] or [0])


def lane_order(briefs, lane):
    by_id = {b.id: b for b in briefs}
    return sorted((b for b in briefs if lane_of(b) == lane), key=lambda b: (RANK[b.status] * 100 + depth(b, by_id), b.id))


def short(title: str) -> str:
    t = re.split(r'[;:(]', title)[0].strip().replace('`', '')
    return t if len(t) <= 42 else t[:42].rstrip() + '…'


def lane_note(briefs, lane):
    order = lane_order(briefs, lane)
    if not order:
        return ''
    return f'{order[0].id} ({short(order[0].title)})' + ''.join(f', then {b.id}' if i == 1 else f', {b.id}' for i, b in enumerate(order[1:], 1))


def js(s):
    return json.dumps(s, ensure_ascii=False)


def b_array(briefs):
    ids = {b.id for b in briefs}
    rows = []
    for b in sorted(briefs, key=lambda b: b.id):
        needs = ', '.join('{ id: %s%s }' % (js(n), ', soft: true' if soft else '') for n, soft in b.needs if n in ids)
        rows.append('    { id: %s, lane: %s, at: 0, len: %d, st: %s, t: %s, needs: [%s], why: %s, files: %s }' %
                    (js(b.id), js(lane_of(b)), b.length, js(b.status), js(b.title.replace('`', '')), needs, js(b.goal), js(b.touches)))
    return '  var B = [\n' + ',\n'.join(rows) + '\n  ];'


def lanes_array(briefs, fixed):
    out = []
    for lane in fixed['lanes']:
        note = fixed['notes'].get(lane['id']) if lane['id'] in fixed['notes'] else lane_note(briefs, lane['id'])
        out.append('    { id: %s, name: %s, note: %s }' % (js(lane['id']), js(lane['name']), js(note)))
    return '  var LANES = [\n' + ',\n'.join(out) + '\n  ];'


def agent_table(briefs, fixed):
    rows = ['| Agent | Now | Next |', '|---|---|---|', '| Agent 1 (guru prime) | %s | %s |' % (fixed['agent1']['now'], fixed['agent1']['next'])]
    for a in sorted(AGENTS):
        order = lane_order(briefs, a)
        now = f'{order[0].id} ({short(order[0].title)})' if order else 'free'
        nxt = ', then '.join([', '.join(b.id for b in order[1:2])] + [', '.join(b.id for b in order[2:])]) if len(order) > 2 else (order[1].id if len(order) == 2 else '')
        rows.append(f'| Agent {a} | {now} | {nxt} |')
    order = lane_order(briefs, 'O')
    rows.append('| OpenAI agent (notes only) | %s | %s |' % (f'{order[0].id} ({short(order[0].title)})' if order else 'free', ', '.join(b.id for b in order[1:])))
    return '\n'.join(rows)


def between(text, start, end, new, rel):
    i, j = text.find(start), text.find(end)
    if i < 0 or j < i:
        raise SystemExit(f'{rel}: markers {start!r} and {end!r} not found')
    return text[:i + len(start)] + '\n' + new + '\n' + text[j:]


def render(root: Path, briefs):
    fixed = json.loads((root / 'project/lane-plan-lanes.json').read_text(encoding='utf-8'))
    page = (root / 'project/lane-plan.html').read_text(encoding='utf-8')
    page = between(page, '// lanes:start', '  // lanes:end', lanes_array(briefs, fixed), 'project/lane-plan.html')
    page = between(page, '// plan:start', '  // plan:end', b_array(briefs), 'project/lane-plan.html')
    status = (root / 'project/STATUS.md').read_text(encoding='utf-8')
    status = between(status, '<!-- agents:start -->', '<!-- agents:end -->', agent_table(briefs, fixed), 'project/STATUS.md')
    return {'project/lane-plan.html': page, 'project/STATUS.md': status}


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split('\n\n')[0])
    ap.add_argument('--root', type=Path, default=Path(__file__).resolve().parents[2])
    ap.add_argument('--check', action='store_true')
    a = ap.parse_args(argv)
    briefs, _, errors = load(a.root)
    if errors:
        print('\n'.join(errors), file=sys.stderr)
        return 2
    want, bad = render(a.root, briefs), 0
    for rel, text in want.items():
        cur = (a.root / rel).read_text(encoding='utf-8')
        if cur == text:
            continue
        if a.check:
            bad = 1
            sys.stdout.writelines(difflib.unified_diff(cur.splitlines(True), text.splitlines(True), rel, rel + ' (from the headers)'))
        else:
            (a.root / rel).write_text(text, encoding='utf-8', newline='\n')
    if bad:
        print('\nlane plan or agent table is stale: run python -I project/tools/build_lane_plan.py', file=sys.stderr)
    return bad


if __name__ == '__main__':
    sys.exit(main())
