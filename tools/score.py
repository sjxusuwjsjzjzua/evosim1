#!/usr/bin/env python3
"""Matched-window scorer for every build in the corpus.

Replaces the v0.55-only scorer, which gated on `invadeFrac` and so parsed 79 of
2,329 collected logs and none of v0.56 or v0.57 -- two versions after the audit
that flagged it. Arm identity comes from `tools/arms.py`, the one classifier
that tracks the current builds.

Survival is judged at the window end and runs whose log ends before it are
CENSORED out of the denominator. Rule 11: every metric prints its tail, not
only its median.

The mission metric is reported as the identity it is:

    heterotrophy = supply x consumedFraction x carrionDigest

`supply` is the share of a run's animal energy intake that meat COULD carry if
every gram that died were eaten at perfect digestion -- ecology and constants,
no selection in it. `consumedFraction` and `carrionDigest` are the two terms
selection can move. Scoring the product is why five structural versions read as
flat. `check` prints observed over predicted; it should sit near 1.

Usage: python3 tools/score.py [--window A B] [--pickle PATH]
"""
import json, glob, statistics as st, pickle, os, sys, importlib.util

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_spec = importlib.util.spec_from_file_location('arms', os.path.join(ROOT, 'tools', 'arms.py'))
_arms = importlib.util.module_from_spec(_spec)
# arms.py prints its own daily readout on import; borrow the classifier only.
sys.argv, _argv = [sys.argv[0], os.path.join(ROOT, 'runs', '.score-arms.tsv')], sys.argv
_out, sys.stdout = sys.stdout, open(os.devnull, 'w')
try: _spec.loader.exec_module(_arms)
except SystemExit: pass
finally: sys.stdout.close(); sys.stdout = _out; sys.argv = _argv
arm = _arms.arm

W0, D = 400.0, 800.0
PICKLE = None
_a = sys.argv[1:]
while _a:
    if _a[0] == '--window': W0, D = float(_a[1]), float(_a[2]); _a = _a[3:]
    elif _a[0] == '--pickle': PICKLE = _a[1]; _a = _a[2:]
    else: _a = _a[1:]

ACTS = ['actGraze','actScav','actAttack','actFlee','actAppr','actRest','actWander']
# Verified-inert only. `ambushTendency` is READ (build :1769) and inflated this
# null; `territoriality` became `patchLeaving` in v0.57 and left the set.
NEUT = ['mateChoosiness','parentalCare','pathogenResistance']
WATCH = ['meatAttraction','plantAttraction','carrionAttraction','socialAttraction','carnivory',
         'herbivory','aggression','biteForce','maxSpeed','preySizeRatio','fearThreshold','armour',
         'patchLeaving','territoriality']

rows = []
for f in sorted(glob.glob(os.path.join(ROOT, 'runs', '*', '*.json'))):
    if f.endswith('.progress.json'): continue
    try: d = json.load(open(f))
    except Exception: continue
    if d.get('kind') != 'evosim-log': continue
    cfg = d.get('cfg', {}); c = d['cols']; tpd = d.get('ticksPerDay', 480)
    day = [t/tpd for t in c['tick']]; an = c['animals']; endday = day[-1]
    if an[-1] <= 0 and endday < D: status = 'dead'
    elif endday >= D:
        i = max(j for j, x in enumerate(day) if x <= D)
        status = 'alive' if an[i] > 0 else 'dead'
    else: status = 'censored'
    r = dict(f=f, arm=arm(cfg), ver=d.get('version'), status=status, endday=endday)
    if status == 'alive':
        idx = [j for j, x in enumerate(day) if W0 <= x <= D]; a0, b0 = idx[0], idx[-1]
        A = [an[j] for j in idx]; m = st.mean(A) or 1
        r['meanN'] = m; r['cv'] = 100*st.pstdev(A)/m
        mu = {k: st.mean([c[k][j] for j in idx]) for k in ACTS}; tot = sum(mu.values())
        for k in ACTS: r[k] = 100*mu[k]/tot if tot > 0 else float('nan')
        dl = lambda k: c[k][b0] - c[k][a0]
        ec, ep, ef = dl('eCarrion'), dl('ePlant'), dl('eFlesh')
        # eFlesh is the OTHER meat channel. It is zero from v0.52 on, where
        # ATTACK stopped moving mass, and nonzero in every v0.51 log. Dropping
        # it reads those runs at a quarter of their real meat intake and would
        # score any future direct-transfer build as a regression.
        r['hetero'] = 100*ec/(ec+ep) if ec+ep > 0 else float('nan')
        r['heteroAll'] = 100*(ec+ef)/(ec+ef+ep) if ec+ef+ep > 0 else float('nan')
        aMass = st.mean([c['aMass'][j] for j in idx])
        deaths = dl('aDeadKilled') + dl('aDeadStarve') + dl('aDeadAge') + dl('aDeadSen') if 'aDeadSen' in c \
                 else dl('aDeadKilled') + dl('aDeadStarve') + dl('aDeadAge')
        deathMass = deaths*aMass
        mv = cfg.get('meatValue', 24.0)*cfg.get('carrionValue', 0.85)
        r['supply'] = 100*deathMass*mv/(deathMass*mv + ep) if deathMass*mv + ep > 0 else float('nan')
        r['consumed'] = dl('carrionMass')/deathMass if deathMass > 0 else float('nan')
        aCarn = st.mean([c['aCarn'][j] for j in idx])
        fl = cfg.get('carrionFloor', 0.30)
        r['digest'] = fl + (1-fl)*aCarn
        pred = r['supply']*r['consumed']*r['digest']
        r['check'] = r['hetero']/pred if pred > 0 else float('nan')
        dk = dl('aDeadKilled')
        r['predShare'] = 100*dk/deaths if deaths > 0 else float('nan')
        ch = d.get('carnivoryHistogram') or {}
        best = None
        for row in ch.get('series') or []:
            if W0 <= row['t']/tpd <= D: best = row
        if best:
            b = best['bins']; tt = sum(b)
            r['carnHi'] = 100*sum(b[6:])/tt if tt > 0 else float('nan')
        gn = d['geneNames']['animal']
        ok = lambda s: (s.get('animal') or {}).get('n', 0) > 0 and (s.get('animal') or {}).get('mean')
        snaps = [s for s in d['genes'] if W0 <= s['t']/tpd <= D and ok(s)]
        first = [s for s in d['genes'] if ok(s)]
        if snaps and first:
            f0 = first[0]['animal']['mean']; fN = snaps[-1]['animal']['mean']
            for g in WATCH + NEUT:
                if g not in gn: continue
                i = gn.index(g); r['g_'+g] = fN[i]; r['d_'+g] = fN[i]-f0[i]
    rows.append(r); del d

if PICKLE: pickle.dump(rows, open(PICKLE, 'wb'))
alive = [r for r in rows if r['status'] == 'alive']
print('logs parsed %d | alive %d | censored %d | dead %d | window days %g-%g'
      % (len(rows), len(alive), sum(1 for r in rows if r['status'] == 'censored'),
         sum(1 for r in rows if r['status'] == 'dead'), W0, D))

def tail(v, p):
    v = sorted(x for x in v if x == x)
    return v[min(len(v)-1, int(p*(len(v)-1)))] if v else float('nan')

by = {}
for r in rows: by.setdefault(r['arm'] or '-', []).append(r)
hdr = '%-26s %4s %5s %8s %8s %8s %8s %8s %7s %6s'
print(hdr % ('arm', 'n', 'surv%', 'het med', 'het p90', 'het max', 'supply', 'consum', 'digest', 'check'))
for k in sorted(by, key=lambda k: -len(by[k])):
    v = by[k]; av = [r for r in v if r['status'] == 'alive']
    den = [r for r in v if r['status'] != 'censored']
    if not av: continue
    h = [r['hetero'] for r in av]
    print(hdr % (k[:26], len(av),
                 '%.1f' % (100*len(av)/len(den)) if den else '-',
                 '%.3f' % tail(h, .5), '%.3f' % tail(h, .9), '%.3f' % max(h),
                 '%.2f' % tail([r['supply'] for r in av], .5),
                 '%.3f' % tail([r['consumed'] for r in av], .5),
                 '%.3f' % tail([r['digest'] for r in av], .5),
                 '%.3f' % tail([r['check'] for r in av], .5)))
if alive:
    h = [r['hetero'] for r in alive]
    print('\nTHE MISSION METRIC, whole corpus: median %.3f%% p90 %.3f%% max %.3f%% (n=%d)'
          % (tail(h, .5), tail(h, .9), max(h), len(alive)))
    print('with eFlesh:                     median %.3f%% p90 %.3f%% max %.3f%%'
          % (tail([r['heteroAll'] for r in alive], .5), tail([r['heteroAll'] for r in alive], .9),
             max(r['heteroAll'] for r in alive)))
    ch = [r['check'] for r in alive]
    print('identity check (observed/predicted): median %.3f p10 %.3f p90 %.3f'
          % (tail(ch, .5), tail(ch, .1), tail(ch, .9)))
