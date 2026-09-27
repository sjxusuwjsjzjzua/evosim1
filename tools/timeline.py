#!/usr/bin/env python3
"""A world's history at a glance: one line per log, one cell per window.

    python3 tools/timeline.py [--every 100000] runs/<label>/s????.json

Each cell, averaged over the window: meat share of intake (%), carnivore
clusters at the window's last sample (meat over half, 10 or more animals),
prey streaming (polar x 10, rounded), mean grazer and meat-eater body size.
"""
import json, sys
av = sys.argv[1:]; every = 100000
if av and av[0] == '--every': every = int(av[1]); av = av[2:]
for f in av:
    L = json.load(open(f))['log']; cells = []
    for w0 in range(0, L[-1]['t'], every):
        W = [r for r in L if w0 < r['t'] <= w0 + every]
        if not W: continue
        eA = sum(r['eP'] + r['eC'] + r['eK'] for r in W) or 1
        meat = 100 * sum(r['eC'] + r['eK'] for r in W) / eA
        carn = sum(1 for sp in W[-1]['species'] if sp.get('meat', 0) > 0.5 and sp['n'] >= 10)
        pol = sum(r.get('polar', 0) for r in W) / len(W)
        sp = W[-1]['species']
        gz = [s for s in sp if s.get('meat', 0) <= 0.5]; mz = [s for s in sp if s.get('meat', 0) > 0.5]
        size = lambda S: sum(s['size'] * s['n'] for s in S) / max(1, sum(s['n'] for s in S)) if S else 0
        cells.append('%2.0f%%/%d/%d/%.1f/%s' % (meat, carn, round(10 * pol), size(gz), ('%.1f' % size(mz)) if mz else '-'))
    print('%-11s %s' % (f.split('/')[-1], '  '.join(cells)))
print('cells: meat%%/carnivore clusters/polar x10/grazer size/meat-eater size, every %dk ticks' % (every // 1000))
