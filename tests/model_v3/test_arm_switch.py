"""Brief 121c (W7), block 1: the arm is chosen in core_run, written into the run record, and the household arm runs through core_run with I1, the account identity and the ledger ties of 120c."""
import json
from dataclasses import replace

import numpy as np
import pytest

from model_v3.core import kernel as K
from model_v3.out import assemble
from model_v3.runner import arm as ab, runner as R
from model_v3.out import writer
from model_v3.runner import sweeps as S
from test_out import INFO, INPUTS, LEVERS, MANIFEST, fixture, synthetic
from test_runner import ROOT, ctx, fake, lv, out, tier1  # noqa: F401  (the fixtures)

SPEC = dict(tau_0=0.04, tau_m=0.7, k_ln=1, ratio=0.5)
INP = json.loads((ROOT / 'docs' / 'model-v3' / 'cell-baseline' / 'inputs_used.json').read_text())
PATHS = (np.full((100, 2), 0.01), np.full((100, 2), 0.0157))


def test_the_default_arm_is_legacy_and_the_run_record_says_so(ctx):
    assert ctx.arm == 'legacy'
    raw = R.core_run(ctx, ctx.centre, SPEC, *PATHS)
    assert raw.arm == dict(arm='legacy') and raw.c == ctx.centre['I-D14c'] / 100
    a = ab.build('legacy', ctx, ctx.centre, raw.base)
    assert isinstance(a.make(), ab.LegacyHook) and a.safe(100, 2) is None and a.c == raw.c
    with pytest.raises(ValueError, match="'legacy' or 'household'"):
        ab.build('hybrid', ctx, ctx.centre, raw.base)


def test_the_household_arm_runs_through_core_run_and_keeps_the_identities(ctx, monkeypatch):
    seen, books, orig = [], [], K.Book

    class Spy(ab.HouseholdHook):
        def post(self, book, fl):
            super().post(book, fl)
            a = self.account()
            seen.append((np.abs(a['residual']).max(), np.abs(a['unpaid']).max()))                  # the account identity and the model alarm, every year of every phase

    monkeypatch.setattr(ab, 'HouseholdHook', Spy)
    monkeypatch.setattr(K, 'Book', lambda *a, **k: books.append(orig(*a, **k)) or books[-1])
    c2 = replace(ctx, arm=dict(arm='household', inputs=INP, saving='median'))
    raw = R.core_run(c2, c2.centre, SPEC, *PATHS)                                                 # I1 is checked inside the hook every year: a failure raises
    lab = raw.arm
    assert lab['arm'] == 'household' and lab['central'] is False and lab['scenario']['saving'] == 'median' and 'stand-in' in lab['safe_return'] and 'ledger' in raw.run
    assert len(seen) > 1000 and max(r for r, _ in seen) < 1e-9 and max(u for _, u in seen) == 0.0 and books and all((b.unpaid_B == 0).all() and K.shortfall_lines(b) == 0 for b in books)
    wdt = sum(raw.run[k] for k in ('tax', 'refund', 'death_tax', 'heir', 'death_B', 'death_D'))
    assert np.abs(sum(raw.run['ledger']['rc'].values()) - wdt).max() < 1e-9 and wdt.max() > 0
    f = raw.r['fund']
    for k in f['L']:
        dL = np.diff(np.vstack([np.zeros((1, 2)), f['L'][k]]), axis=0)
        assert np.abs(dL - (f['rc'][k] + f['ret'][k] - f['pay'][k])).max() < 1e-9
    legacy = R.core_run(ctx, ctx.centre, SPEC, *PATHS)
    assert not np.allclose(legacy.run['tax'], raw.run['tax']) and legacy.arm != raw.arm            # a household-arm result is never a legacy result


def test_the_household_arm_produces_every_id_and_withholds_none_since_126c(ctx, out):
    c2 = replace(ctx, arm=dict(arm='household', inputs=INP, saving='median'))
    ev = {'S': R.evaluate(c2, c2.centre, SPEC, *PATHS)}
    s = R.samples(ev, c2.ids, c2.once, R.statics(c2, c2.centre))
    held = ab.withheld(R.core_run(c2, c2.centre, SPEC, *PATHS).arm)
    assert ab.WITHHELD == {} and not ab.WITHHELD_BY and held == {} and np.isfinite(ev['S']['M3']).any()         # every id is produced (M3, M12, M13, M15 and M9 came back in 126c)
    assert all(s[i] for i in s) and ab.withheld(dict(arm='legacy')) == {} and set(s) >= {'O1', 'O2', 'O4a', 'O7', 'OW2', 'OS1', 'OW1', 'OW3', 'OM1'}
    o, _ = assemble.assemble(out, {}, None, 'provisional', dict.fromkeys(('OW3', 'OM1'), 'legacy_only'))                  # the assembler keeps the mechanism for an id an arm cannot produce
    assert all(o[i] == dict(summary=o[i]['summary'], cells=[], withheld='legacy_only') for i in ('OW3', 'OM1')) and set(o) == {'OW3', 'OM1'}
    with pytest.raises(assemble.AssembleError, match='withheld'):
        assemble.assemble(out, {'O3': {('S', 'single', (), None): np.ones(3)}}, None, 'provisional', {'O3': 'legacy_only'})


def test_the_tornado_keeps_the_m3_head_and_a_household_file_with_the_returned_ids_passes_final(out, tmp_path):
    ev = lambda *a, **k: {x: v for x, v in fake()(*a, **k).items() if x != 'M3'}                      # a household-arm evaluation holds no M3
    rows = {'a': type('Row', (), dict(low=0.0, high=1.0))(), 'b': type('Row', (), dict(low=0.0, high=1.0))()}
    t = S.tornado(ev, {'S': dict(SPEC)}, rows, {'a'})
    assert t and {r['headline'] for r in t} == {'M1', 'M2', 'M4a'} and 'M3' in {r['headline'] for r in S.tornado(fake(), {'S': dict(SPEC)}, rows, {'a'})}
    held = ab.withheld(dict(arm='household'))
    drop = [i for i in held if isinstance(held[i], str)]
    smp = synthetic(skip=drop)
    o, _ = assemble.assemble(out, smp, None, 'final', held)
    run = writer.run_block(out, MANIFEST, INPUTS, LEVERS, {**INFO, 'status': 'final', 'pack_sha256': 'x' * 64, 'pack_country': 'UK', 'arm': dict(arm='household', central=False)})
    path = writer.write_outputs(tmp_path, writer.document(o, {}, run), MANIFEST, INPUTS)               # the validator runs inside with --final and raises on any error
    assert path.exists() and 'withheld_by' not in o['OT1'] and o['O3']['cells'] and o['OW3']['cells'] and o['OM1']['cells'] and o['OW1']['cells']    # nothing is withheld: the manifest restricts no id (V7 on a restricted id is tested in tests/data)


@pytest.mark.parametrize('saving', ['min', 'median'])
def test_the_burden_flows_equal_the_revenue_receipts_in_every_year_including_the_horizon(ctx, saving):
    c2 = replace(ctx, arm=dict(arm='household', inputs=INP, saving=saving))
    raw = R.core_run(c2, c2.centre, SPEC, *PATHS)                                                  # six phases, two paths, 100 years
    fl, run = raw.fl, raw.run
    net = np.einsum('tnp,n->tp', fl['net'], fl['wt']) * fl['adults_k']
    wdt = sum(run[k] for k in ('tax', 'refund', 'death_tax', 'heir', 'death_B', 'death_D'))
    assert fl['net'].shape[:2] == (100, 6 * len(raw.base.labels)) and wdt[-1].min() > 0
    assert np.abs(net - wdt).max() < 1e-6 * np.abs(wdt).max()
