"""Brief 088c: O1e and OT1 as Samples cells from the sweeps (27 grid points as schedules), DH1a and DH1b equal the pack, nothing changes per path."""
from dataclasses import replace

import numpy as np

from model_v3.core import pack as pk
from model_v3.out import assemble as A
from model_v3.runner import out_sweeps as W, runner as R, sweeps as S
from test_runner import ROOT, ROW, ctx, fake, lv, out, tier1  # noqa: F401  (the fixtures)


def specs(lv):
    return {'_'.join(S.labels(sp)): sp for sp in S.grid(lv)}


def test_o1e_is_one_single_cell_per_schedule_with_its_range_from_the_draws(lv):
    sp = specs(lv)
    c = W.o1e(S.breakeven_return(fake(lambda o: o['I-D1a'] - 3.55), sp, 'I-D1a', draws={'z': np.arange(1.0, 6.0)}))['O1e']
    assert len(sp) == 27 and set(c) == {(s, 'single', (), None) for s in sp} and all(abs(v[0] - 3.55) < 0.02 and v.shape == (3,) for v in c.values())
    c = W.o1e(S.breakeven_return(fake(lambda o: o['I-D1a'] - 3.55 + o.get('z', 0)), {'S': sp[next(iter(sp))]}, 'I-D1a', draws={'z': np.array([-1.0, 0.0, 1.0, 2.0, 3.0])}))['O1e']
    assert np.allclose(c['S', 'single', (), None], [3.55, 0.95, 4.15], atol=0.03)      # roots 4.55 down to 0.55: p10 and p90


def test_ot1_has_a_low_and_a_high_for_each_input_and_headline_and_the_unread_are_zero(lv, tier1):
    sp, rows = specs(lv), {i: ROW(0, 5, 10) for i in tier1}
    t = W.ot1(S.tornado(fake(lambda o: 2.0 * o.get('I-D4a', 5)), sp, rows, {'I-D4a'}))['OT1']
    assert len(t) == 27 * 40 * 4 and t[next(iter(sp)), 'single', (('headline', 'M1'), ('input', 'I-D4a')), None].tolist() == [0.0, -10.0, 10.0]
    assert sum(not v.any() for v in t.values()) == 27 * 4 * 40 - 27 and all(v.shape == (3,) for v in t.values())
    assert {k[2] for k in t} == {(('headline', h), ('input', i)) for h in ('M1', 'M2', 'M4a', 'M3') for i in tier1}


def test_dh1a_and_dh1b_equal_the_pack_and_the_group_adds_no_per_path_cell(ctx, out):
    pack = pk.load_pack(ROOT / 'model_v3' / 'pack' / 'GBR')
    man = {o['id']: o for o in out['outputs']}
    c1 = replace(ctx, once=frozenset(i for i, o in man.items() if o.get('once_not_per_schedule')))
    s = W.static(R.env_of(c1, c1.centre))
    a, b = pk.dh1a(pack), pk.dh1b(pack)['lines']
    assert W.static(R.env_of(replace(ctx, once=frozenset()), ctx.centre)) == {} and set(s) == {'DH1a', 'DH1b'}                    # no once id in the context, no static cell
    assert {k[1][0][1] for k in s['DH1a']} == set(man['DH1a']['by']['series']) == set(a) and {k[1][0][1] for k in s['DH1b']} == set(man['DH1b']['by']['line']) == set(b)
    assert all(s['DH1a']['single', (('series', n),), None][0] == a[n]['point'] for n in a) and all(s['DH1b']['single', (('line', n),), None][0] == v for n, v in b.items())
    assert W.IDS == ('DH1a', 'DH1b', 'O1e', 'OT1') and W.cells({}) == W.per_path(None, None, None) == {}
