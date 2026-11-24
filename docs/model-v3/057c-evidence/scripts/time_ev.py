import sys, time, json
sys.path.insert(0, '.')
from dataclasses import replace
import yaml
from model_v3 import run as X
from model_v3.core import pack as pk, returns as rt
from model_v3.out import assemble as asm
from model_v3.runner import runner as R, sweeps as S
man = yaml.safe_load(X.MANIFEST.read_text()); lv = json.loads(X.LEVERS.read_text())
tier1 = next(o for o in man['outputs'] if o['id']=='OT1')['by']['input']
once=[e['id'] for e in asm.entries(man).values() if e.get('once_not_per_schedule')]
ctx = R.context(pk.load_pack(X.PACK), pk.load_register(X.INPUTS), lv, tier1, list(asm.entries(man)), once)
inp = json.loads(X.HH_INPUTS.read_text())
spec = dict(tau_0=0.04, tau_m=0.7, k_ln=1, ratio=0.5)
for name, c in (('legacy', ctx), ('household', replace(ctx, arm=dict(arm='household', inputs=inp, saving='median', regime='mid')))):
    st = rt.streams(1)
    ev = R.make_ev(c, st['tornado_crn'].standard_normal((R.T, 20)))
    t=time.perf_counter(); ev(spec); print(name, 'one ev, 20 paths:', round(time.perf_counter()-t,2), 's', flush=True)
