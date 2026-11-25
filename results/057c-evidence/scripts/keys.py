import sys, json; sys.path.insert(0,'.')
from dataclasses import replace
import yaml
from model_v3 import run
from model_v3.out import assemble as asm
from model_v3.core import pack as pk, returns as rt
from model_v3.runner import runner as R, sweeps as S
man=yaml.safe_load(run.MANIFEST.read_text()); lv=json.loads(run.LEVERS.read_text())
tier1=next(o for o in man['outputs'] if o['id']=='OT1')['by']['input']
once=[e['id'] for e in asm.entries(man).values() if e.get('once_not_per_schedule')]
ctx=R.context(pk.load_pack(next(d for d in sorted(run.PACKS.iterdir()) if (d/'manifest.json').is_file())),pk.load_register(run.INPUTS),lv,tier1,list(asm.entries(man)),once)
inp=json.loads(run.HH_INPUTS.read_text())
cp=replace(ctx,arm=dict(arm='household',inputs=inp,saving='median',regime='mid'))
named={'S_central': None}
st=rt.streams(run.SEED)
fm,_=S.feasibility(R.make_ev(cp,st['tornado_crn'].standard_normal((R.T,20))),S.grid(lv)); nm=S.choose(fm,man['feasibility'])
smp,_=R.level1(cp,{'S_central':nm['S_central']},st['level1_paths'],n=50)
for o in ('O1','O2','O3','O4a'):
    ks=[k for k in smp[o] if k[1]=='short'][:6]; print(o,len(smp[o]),ks[:6], [getattr(smp[o][k],'shape',None) for k in ks[:2]])
print(list(smp['O3']), [k for k in smp['O4a'] if 'overall' in str(k)], [k for k in smp['O4a']][-3:])
