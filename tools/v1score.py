#!/usr/bin/env python3
"""Score evosim 1.x logs (run.js --out). One row per run, late-window means.

    python3 tools/v1score.py log1.json [log2.json ...] [--from 0.5]

--from sets where the scoring window starts, as a share of each run's length
(default: the last half). Columns:
  animals   mean population
  meat%     share of animal energy intake that came from flesh (carrion + kills)
  kill%     share that came from the eater's own kills
  pred%     adults whose LIFETIME intake is more than half meat, as % of adults
  kills/kt  kills per 1000 ticks
  diet      mean diet gene (0 plant gut, 1 meat gut)
  hi-diet%  animals with diet >= 0.5 at the last sample
  size, speed, weapon, armour, plantDef: mean genes
"""
import json, sys, statistics as st

args = [a for a in sys.argv[1:] if not a.startswith('--')]
frac = 0.5
if '--from' in sys.argv: frac = 1 - float(sys.argv[sys.argv.index('--from') + 1])
hdr = ('%-26s %7s %6s %7s %6s %6s %7s %6s %8s %5s %5s %6s %6s %6s'
       % ('run', 'ticks', 'anim', 'meat%', 'kill%', 'pred%', 'kills/kt', 'diet', 'hi-diet%', 'size', 'spd', 'weapon', 'armour', 'pDef'))
print(hdr)
for f in args:
    d = json.load(open(f)); L = d['log']
    if not L: continue
    w = L[int(len(L) * (1 - frac)):] if frac < 1 else L
    w = [r for r in w if r['animals'] > 0] or w
    m = lambda k: st.mean(r[k] for r in w)
    mg = lambda k: st.mean(r['genes'][k] for r in w)
    eP, eC, eK = sum(r['eP'] for r in w), sum(r['eC'] for r in w), sum(r['eK'] for r in w)
    eA = eP + eC + eK or 1
    ad = sum(r['adults'] for r in w) or 1
    span = (w[-1]['t'] - w[0]['t']) or 1
    last = L[-1]; dh = last['dietHist']; n = sum(dh) or 1
    print('%-26s %7d %6.0f %7.2f %6.2f %6.1f %7.2f %6.3f %8.1f %5.2f %5.2f %6.2f %6.2f %6.2f' % (
        f.split('/')[-1][:26], d['ticks'], m('animals'), 100 * (eC + eK) / eA, 100 * eK / eA,
        100 * sum(r['predators'] for r in w) / ad, 1000 * sum(r['kills'] for r in w) / span,
        mg('diet'), 100 * sum(dh[5:]) / n, mg('size'), mg('speed'), mg('weapon'), mg('armour'), m('plantDef')))
