#!/usr/bin/env python3
"""Weekly scoring pass for the v0.55 arms. Matched window days 400-800,
survival judged at day 800, runs still alive when their log ends before 800
CENSORED out of the denominator. Act shares are means of the snapshot columns."""
import json, glob, statistics as st, pickle, os, sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = sys.argv[1] if len(sys.argv) > 1 else '/tmp/score55.pkl'
D, W0 = 800.0, 400.0
ACTS = ['actGraze','actScav','actAttack','actFlee','actAppr','actRest','actWander']
NEUT = ['territoriality','ambushTendency','mateChoosiness','parentalCare','pathogenResistance']
WATCH = ['meatAttraction','plantAttraction','carrionAttraction','socialAttraction','carnivory',
         'herbivory','aggression','biteForce','maxSpeed','preySizeRatio','fearThreshold','armour']
def arm(c):
    if 'invadeFrac' not in c: return None
    if c.get('invadeFrac',0) > 0: return 'invade-carn'
    if c.get('k_mixed',0.018) == 0: return 'mixed-flat'
    if c.get('meatValue',24.0) != 24.0: return 'meat-rich-55'
    return 'CONTROL'
rows=[]
for f in sorted(glob.glob(os.path.join(ROOT,'runs','rot-collect','*.json'))):
    try: d=json.load(open(f))
    except Exception: continue
    a=arm(d.get('cfg',{}))
    if not a: continue
    tpd=d.get('ticksPerDay',480); c=d['cols']
    day=[t/tpd for t in c['tick']]; an=c['animals']; endday=day[-1]
    if an[-1]<=0 and endday<D: status='dead'
    elif endday>=D:
        i=max(j for j,x in enumerate(day) if x<=D)
        status='alive' if an[i]>0 else 'dead'
    else: status='censored'
    r=dict(f=f,arm=a,status=status,endday=endday)
    if status=='alive':
        idx=[j for j,x in enumerate(day) if W0<=x<=D]; a0,b0=idx[0],idx[-1]
        A=[an[j] for j in idx]; m=st.mean(A) or 1
        r['meanN']=m; r['cv']=100*st.pstdev(A)/m
        mu={k:st.mean([c[k][j] for j in idx]) for k in ACTS}; tot=sum(mu.values())
        for k in ACTS: r[k]=100*mu[k]/tot if tot>0 else float('nan')
        dk=c['aDeadKilled'][b0]-c['aDeadKilled'][a0]
        t2=dk+sum(c[k][b0]-c[k][a0] for k in ('aDeadAge','aDeadSen','aDeadStarve'))
        r['predShare']=100*dk/t2 if t2>0 else float('nan')
        # H8: fraction of animals above carnivory 0.5, from the histogram row
        # nearest the window end. 12 bins over [0,1], so bins 6..11 are >= 0.5.
        ch=d.get('carnivoryHistogram') or {}
        best=None
        for row in ch.get('series') or []:
            t=row['t']/tpd
            if W0<=t<=D: best=row
        if best:
            b=best['bins']; tt=sum(b)
            r['carnHi']=100*sum(b[6:])/tt if tt>0 else float('nan')
            r['carnHistT']=best['t']/tpd
        gn=d['geneNames']['animal']
        snaps=[s for s in d['genes'] if W0<=s['t']/tpd<=D and (s.get('animal') or {}).get('n',0)>0 and (s.get('animal') or {}).get('mean')]
        first=[s for s in d['genes'] if (s.get('animal') or {}).get('n',0)>0 and (s.get('animal') or {}).get('mean')]
        if snaps and first:
            f0=first[0]['animal']['mean']; fN=snaps[-1]['animal']['mean']
            for g in WATCH+NEUT:
                i=gn.index(g); r['g_'+g]=fN[i]; r['d_'+g]=fN[i]-f0[i]
    rows.append(r); del d
pickle.dump(rows,open(OUT,'wb'))
print('v0.55 runs parsed:',len(rows))
