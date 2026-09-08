#!/usr/bin/env python3
"""Daily arm readout. Classifies every collected log by diffing its cfg against
build defaults, and caches per-file results so a cycle does not re-parse the
whole corpus.

Arm identity is decided by the cfg diff, NEVER by agreement between runs, and a
MISSING key means the feature predates that build rather than marking a
different arm -- conflating those split the corpus into bogus arms twice.

Usage: python3 tools/arms.py [cache_path]
"""
import json, glob, statistics as st, os, sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CACHE = sys.argv[1] if len(sys.argv) > 1 else os.path.join(ROOT, 'runs', 'arms.tsv')

def arm(c):
    # v0.54+ first: k_choiceBeta exists only from v0.54 on.
    if 'k_choiceBeta' in c:
        b = c['k_choiceBeta']; mv = c.get('meatValue', 24.0); fl = c.get('k_meatAttrFloor', 0.5)
        if b == 12.0: return 'beta-hi'
        if mv != 24.0: return 'meat-rich'
        if fl == 0:    return 'beta-flooroff'
        if b == 4.0 and mv == 24.0 and fl == 0.5: return 'CONTROL'
        return 'v54-other'
    sp = c.get('k_seasonPhen')
    if sp is None: return None                      # pre-v0.53
    fl = c.get('k_meatAttrFloor', 0.5)
    if sp == 1.0 and fl == 0.5: return 'v53-CONTROL'
    if sp == 0 and fl == 0.5:   return 'v53-seasonless'
    if sp == 0.5:               return 'v53-halfseason'
    if sp == 0 and fl == 0:     return 'v53-seasonless-flooroff'
    return 'v53-other'

done = set()
if os.path.exists(CACHE):
    for r in open(CACHE): done.add(r.split('\t')[0])
os.makedirs(os.path.dirname(CACHE), exist_ok=True)
out = open(CACHE, 'a')
for f in sorted(glob.glob(os.path.join(ROOT,'runs','rot-collect','*.json'))
              + glob.glob(os.path.join(ROOT,'runs','v53-collect','*.json'))):
    if f in done: continue
    try: d = json.load(open(f))
    except Exception: continue
    a = arm(d.get('cfg', {}))
    if not a:
        out.write('%s\t-\t\t\t\t\n' % f); continue
    an = d['cols']['animals']; tk = d['cols']['tick']; tpd = d.get('ticksPerDay', 480)
    days = tk[-1]/tpd
    surv = 1 if an[-1] > 0 else 0
    half = an[len(an)//2:]
    mu = st.mean(half) if half else 0
    cv = (st.pstdev(half)/mu*100) if mu > 0 else float('nan')
    gn = d['geneNames']; gn = gn['animal'] if isinstance(gn, dict) else gn
    gi = gn.index('meatAttraction') if 'meatAttraction' in gn else None
    ma = ''
    if gi is not None:
        for snap in reversed(d['genes']):
            am = snap.get('animal') or {}
            if am.get('n', 0) > 0 and am.get('mean'):
                ma = '%.4f' % am['mean'][gi]; break
    out.write('%s\t%s\t%.0f\t%d\t%.1f\t%s\n' % (f, a, days, surv, cv, ma))
    del d
out.close()

acc = {}
for r in open(CACHE):
    p = r.rstrip('\n').split('\t')
    if len(p) < 6 or p[1] in ('-', ''): continue
    acc.setdefault(p[1], []).append(p)
print('%-24s %4s %6s %8s %10s' % ('arm', 'n', 'surv', 'cv%', 'meatAttr'))
for k in ['CONTROL','beta-hi','meat-rich','beta-flooroff','v54-other',
          'v53-CONTROL','v53-seasonless','v53-halfseason','v53-seasonless-flooroff','v53-other']:
    v = acc.get(k)
    if not v:
        if not k.endswith('other'): print('%-24s %4d' % (k, 0))
        continue
    n = len(v); s = sum(int(x[3]) for x in v)/n*100
    cvs = [float(x[4]) for x in v if x[4] != 'nan']
    mas = [float(x[5]) for x in v if x[5]]
    print('%-24s %4d %5.0f%% %7.1f %10s' % (k, n, s,
          st.median(cvs) if cvs else float('nan'),
          '%.4f' % st.median(mas) if mas else '-'))
