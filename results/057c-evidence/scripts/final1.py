import sys, json, time; sys.path.insert(0,'.')
from dataclasses import replace
import yaml
from model_v3 import run
from model_v3.core import pack as pk, returns as rt
from model_v3.out import assemble as asm
from model_v3.runner import runner as R, sweeps as S
man=yaml.safe_load(run.MANIFEST.read_text()); lv=json.loads(run.LEVERS.read_text())
tier1=next(o for o in man['outputs'] if o['id']=='OT1')['by']['input']
once=[e['id'] for e in asm.entries(man).values() if e.get('once_not_per_schedule')]
ctx=R.context(pk.load_pack(next(d for d in sorted(run.PACKS.iterdir()) if (d/'manifest.json').is_file())),pk.load_register(run.INPUTS),lv,tier1,list(asm.entries(man)),once)
inp=json.loads(run.HH_INPUTS.read_text())
c0=replace(ctx,arm=dict(arm='household',inputs=inp,saving='median',regime='mid'))
st=rt.streams(run.SEED)
named=S.choose(S.feasibility(R.make_ev(c0,st['tornado_crn'].standard_normal((R.T,20))),S.grid(lv))[0],man['feasibility'])
t=time.time()
d,i=run.run_point(ctx,inp,'median_mid',named,man,R.N1,R.N2P,None,run.SEED,1e-2,False)
open(sys.argv[1],'w').write(f'{time.time()-t:.0f} s one final-size grid point without O1e (level 1 {R.N1} paths x3, tornado {R.N2P} paths)\n')
