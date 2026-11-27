"""
split.py -- partial files of a split run, and the checks the merge makes before it reads one (model v3, brief 183c stage A)
==========================================================================================================================
Layer L5 (`out/`; numpy and the standard library only). Design: results/split-run/design.md, sections 2 to 4. A split run is `plan`, then `point` units (level 1 and
tornado of one grid point), then `o1e` units (the point roots, then batches of draws of one schedule), then the merge. Each unit writes one partial file; this module
holds what they and the merge share: the byte encoding, the header, the draw slice and its hash, the list of units a run must have, and `check`, which refuses a set of
partials before anything is merged. It runs no model and writes no file.

Bytes: UTF-8 JSON, sorted keys, no timestamp, CPU or wall time (those go in a sidecar the merge never reads), so a rerun of a shard gives the same bytes. A float that
must cross exactly is written `enc`: the string 'f:' and its hex form (`float.hex`, exact, also for nan and inf); `dec` reverses it. Plain JSON numbers are exact too
(repr), and `dumps` refuses a non-finite number rather than write one.

The merge never repairs: a differing header field, a missing or extra unit, a duplicate unit whose bytes differ, all raise `SplitError` with the field or the unit.
"""

import hashlib
import json

import numpy as np

SCHEMA = 'wdt-split-partial/1'
KINDS = ('plan', 'point', 'o1e-point', 'o1e')
COMMON = ('size', 'seed', 'arm', 'n1', 'n2p', 'n2', 'tol', 'points', 'schedules', 'batch', 'git_sha', 'inputs', 'numerics')   # equal in every partial of a run
HEADER = ('schema', 'kind', 'unit', 'workers', 'plan_sha256', 'draws_sha256') + COMMON   # `unit` is the identity and `workers` is not a result: neither is compared


class SplitError(ValueError):
    pass


def enc(x):
    """Floats (also numpy) as 'f:' + hex, through lists, tuples and dicts."""
    if isinstance(x, (float, np.floating)):
        return 'f:' + float(x).hex()
    if isinstance(x, dict):
        return {k: enc(v) for k, v in x.items()}
    return [enc(v) for v in x] if isinstance(x, (list, tuple, np.ndarray)) else x


def dec(x):
    if isinstance(x, str):
        return float.fromhex(x[2:]) if x.startswith('f:') else x
    if isinstance(x, dict):
        return {k: dec(v) for k, v in x.items()}
    return [dec(v) for v in x] if isinstance(x, list) else x


def dumps(partial: dict) -> bytes:
    try:
        return (json.dumps(partial, sort_keys=True, indent=1, allow_nan=False) + '\n').encode('utf-8')
    except ValueError as e:
        raise SplitError(f'a partial holds a non-finite number written as JSON (use enc): {e}') from None


def loads(raw: bytes) -> dict:
    return json.loads(raw.decode('utf-8'))


def sha256(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def draws_sha(draws: dict) -> str:
    """SHA-256 of the full draw table, ids in the table's order, values as little-endian float64."""
    h = hashlib.sha256()
    for k, v in draws.items():
        h.update(k.encode('utf-8') + b'\0' + np.ascontiguousarray(v, dtype='<f8').tobytes())
    return h.hexdigest()


def slice_draws(draws: dict, a: int, b: int) -> dict:
    """Draws a..b of every id. Never compute them with n = b - a: the Latin hypercube of draw_theta depends on the whole n (design 2)."""
    return {k: np.asarray(v)[a:b] for k, v in draws.items()}


def unit(kind, point=None, schedule=None, a=None, b=None) -> dict:
    return {'kind': kind, **{k: v for k, v in (('point', point), ('schedule', schedule), ('a', a), ('b', b)) if v is not None}}


def header(kind, unit_, common: dict, workers=1, plan_sha256=None, draws_sha256=None) -> dict:
    """The header of a partial: `common` holds exactly the COMMON fields. A unit that draws (o1e) carries the hash of the draws; every unit but `plan` that of the plan."""
    if kind not in KINDS or set(common) != set(COMMON):
        raise SplitError(f'header: kind {kind!r} or fields {sorted(set(common) ^ set(COMMON))} wrong')
    if (kind == 'plan') != (plan_sha256 is None) or (kind.startswith('o1e')) != (draws_sha256 is not None):
        raise SplitError(f'header: plan_sha256 and draws_sha256 are required for exactly the kinds that use them (kind {kind})')
    return dict(schema=SCHEMA, kind=kind, unit=unit_, workers=workers, plan_sha256=plan_sha256, draws_sha256=draws_sha256, **common)


def uid(h: dict) -> str:
    u = h['unit']
    return ':'.join(str(u[k]) for k in ('kind', 'point', 'schedule', 'a', 'b') if k in u)


def expected(h: dict) -> list:
    """The units a run needs, from any header of it: the plan, one `point` per grid point, the `o1e-point` unit, and (n2 > 0) batches of `batch` draws of each schedule."""
    us = [unit('plan')] + [unit('point', point=p) for p in h['points']] + [unit('o1e-point')]
    return [uid({'unit': u}) for u in us] + [uid({'unit': unit('o1e', schedule=s, a=a, b=min(a + h['batch'], h['n2']))})
                                             for s in h['schedules'] for a in range(0, h['n2'], h['batch'])]


def check(files) -> dict:
    """`files`: [(name, bytes)]. Returns {uid: decoded partial} in the order of `expected`, or raises SplitError naming the field, the unit or the file."""
    by, raw = {}, {}
    for name, b in files:
        p = loads(b)
        h = p.get('header') or {}
        if h.get('schema') != SCHEMA:
            raise SplitError(f"{name}: schema {h.get('schema')!r}, expected {SCHEMA!r}")
        if set(h) != set(HEADER) or h['kind'] not in KINDS:
            raise SplitError(f"{name}: header fields {sorted(set(h) ^ set(HEADER))} wrong or kind {h['kind']!r} unknown")
        k = uid(h)
        if k in by and raw[k][1] != b:
            raise SplitError(f'unit {k}: {raw[k][0]} and {name} differ (a rerun must reproduce the first partial byte for byte)')
        by[k], raw[k] = p, (name, b)
    if not by:
        raise SplitError('no partial files')
    ref = by.get('plan') or next(iter(by.values()))
    for k, p in by.items():
        for f in COMMON:
            if p['header'][f] != ref['header'][f]:
                raise SplitError(f"header field {f}: {p['header'][f]!r} in unit {k}, {ref['header'][f]!r} in unit {uid(ref['header'])}")
    want = expected(ref['header'])
    missing, extra = [k for k in want if k not in by], [k for k in by if k not in want]
    if missing or extra:
        raise SplitError(f"units missing: {missing or 'none'}; unexpected: {extra or 'none'}")
    plan_hash = {sha256(raw[k][1]) for k in by if k == 'plan'}
    for k, p in by.items():
        if p['header']['kind'] != 'plan' and plan_hash and {p['header']['plan_sha256']} != plan_hash:
            raise SplitError(f'unit {k} was built from another plan (plan_sha256 differs)')
    ds = {p['header']['draws_sha256'] for p in by.values() if p['header']['kind'].startswith('o1e')}
    if len(ds) > 1:
        raise SplitError(f'draws_sha256 differs between o1e units: {sorted(ds)}')
    return {k: by[k] for k in want}
