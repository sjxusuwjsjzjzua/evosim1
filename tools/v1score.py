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
  regime%   post-bootstrap samples with meat over 15% of intake
  maxMeat   highest meat share in any post-bootstrap sample
  clump     mean clumping index (1 = random, above 1 = animals in groups)
  preyClump the same among animals living mostly on plants
  carnSp    species at the last sample living mostly on meat (meat > 50%)
"""
import json, sys, statistics as st

args = [a for a in sys.argv[1:] if not a.startswith('--')]
frac = 0.5
if '--from' in sys.argv: frac = 1 - float(sys.argv[sys.argv.index('--from') + 1])
hdr = ('%-26s %7s %6s %7s %6s %6s %7s %6s %8s %5s %5s %6s %6s %6s %7s %7s %5s %6s %6s'
       % ('run', 'ticks', 'anim', 'meat%', 'kill%', 'pred%', 'kills/kt', 'diet', 'hi-diet%', 'size', 'spd', 'weapon', 'armour', 'pDef',
          'regime%', 'maxMeat', 'clump', 'preyCl', 'carnSp'))
print(hdr)
for f in args:
    d = json.load(open(f))
    if d.get('kind') != 'evosim1-log': continue
    L = d['log']
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
    # regime: share of post-bootstrap samples where meat is over 15% of intake
    est = next((r['t'] for r in L if r.get('establishedAt')), 0) or (L[0]['establishedAt'] if L and 'establishedAt' in L[0] else 0)
    post = [r for r in L if r['t'] > max(est, 60000) and r['animals'] > 0]
    regime = 100 * sum(1 for r in post if r['meatShare'] > 0.15) / len(post) if post else float('nan')
    maxMeat = 100 * max((r['meatShare'] for r in post), default=0)
    clump = st.mean(r.get('clump', float('nan')) for r in w)
    preyCl = st.mean(r.get('clumpPrey', float('nan')) for r in w)
    carnSp = sum(1 for sp in last.get('species', []) if sp.get('meat', 0) > 0.5)
    print('%-26s %7d %6.0f %7.2f %6.2f %6.1f %7.2f %6.3f %8.1f %5.2f %5.2f %6.2f %6.2f %6.2f %7.1f %7.1f %5.2f %6.2f %6d' % (
        f.split('/')[-1][:26], d['ticks'], m('animals'), 100 * (eC + eK) / eA, 100 * eK / eA,
        100 * sum(r['predators'] for r in w) / ad, 1000 * sum(r['kills'] for r in w) / span,
        mg('diet'), 100 * sum(dh[5:]) / n, mg('size'), mg('speed'), mg('weapon'), mg('armour'), m('plantDef'), regime, maxMeat, clump, preyCl, carnSp))
