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
  predK     thousands of ticks in the predator state (20k-tick rolling meat share
            enters it above 15%, leaves below 8%), after tick 60k
  exits     times the world left the predator state
"""
import json, sys, statistics as st

frac, args, av = 0.5, [], sys.argv[1:]
while av:
    a = av.pop(0)
    if a == '--from': frac = 1 - float(av.pop(0))
    elif not a.startswith('--'): args.append(a)
hdr = ('%-26s %7s %6s %7s %6s %6s %7s %6s %8s %5s %5s %6s %6s %6s %7s %7s %5s %6s %6s %6s %5s'
       % ('run', 'ticks', 'anim', 'meat%', 'kill%', 'pred%', 'kills/kt', 'diet', 'hi-diet%', 'size', 'spd', 'weapon', 'armour', 'pDef',
          'regime%', 'maxMeat', 'clump', 'preyCl', 'carnSp', 'predK', 'exits'))
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
    # predator state with hysteresis on a 20k-tick rolling meat share
    inP, predT, exits, prev_t = False, 0, 0, None
    for k, r in enumerate(L):
        win = [q for q in L[max(0, k - 60):k + 1] if q['t'] > r['t'] - 20000]
        eAk = sum(q['eP'] + q['eC'] + q['eK'] for q in win) or 1
        ms = sum(q['eC'] + q['eK'] for q in win) / eAk
        if r['t'] > 60000:
            if not inP and ms > 0.15: inP = True
            elif inP and ms < 0.08: inP = False; exits += 1
            if inP and prev_t is not None: predT += r['t'] - prev_t
        prev_t = r['t']
    print('%-26s %7d %6.0f %7.2f %6.2f %6.1f %7.2f %6.3f %8.1f %5.2f %5.2f %6.2f %6.2f %6.2f %7.1f %7.1f %5.2f %6.2f %6d %6.0f %5d' % (
        f.split('/')[-1][:26], d['ticks'], m('animals'), 100 * (eC + eK) / eA, 100 * eK / eA,
        100 * sum(r['predators'] for r in w) / ad, 1000 * sum(r['kills'] for r in w) / span,
        mg('diet'), 100 * sum(dh[5:]) / n, mg('size'), mg('speed'), mg('weapon'), mg('armour'), m('plantDef'), regime, maxMeat, clump, preyCl, carnSp, predT / 1000, exits))
