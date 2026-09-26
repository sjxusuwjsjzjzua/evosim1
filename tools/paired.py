#!/usr/bin/env python3
"""Paired comparison of two batches run on the same seeds.

    python3 tools/paired.py runs/<baseline> runs/<arm> [runs/<arm2> ...]

For each arm, worlds are matched to the baseline by seed. Per world, over the
last half of the run:
  pred      predator-dominated: meat over 15% of intake in >50% of samples after 60k
  carn      a cluster living mostly on meat (meat > 0.5, 10+ animals) at the end
  giant     mean body size >= 5 at the end;  dwarf: <= 0.35
  meat      meat share of intake
  preyCl    prey clumping (1 = random)
  predCl    meat-eater clumping
  diet      mean diet gene
Yes/no measures: counts and an exact McNemar p (discordant pairs, two-sided).
Continuous measures: mean difference (arm - baseline) and an exact sign-test p.
Change a default only at p < 0.05 (the 1.x program audit).
"""
import json, sys, glob, os, math

def binom_p(k, n):   # two-sided exact binomial test at 0.5
    if n == 0: return 1.0
    k = min(k, n - k)
    return min(1.0, 2 * sum(math.comb(n, i) for i in range(k + 1)) / 2 ** n)

def world(f):
    d = json.load(open(f))
    if d.get('kind') != 'evosim1-log': return None
    L = d['log']; half = L[len(L) // 2:]; last = L[-5:]
    post = [r for r in L if r['t'] > 60000]
    eA = sum(r['eP'] + r['eC'] + r['eK'] for r in half) or 1
    size = sum(r['genes']['size'] for r in last) / len(last)
    m = lambda k: None if any(k not in r for r in half) else sum(r[k] or 0 for r in half) / len(half)
    return {
        'pred': sum(1 for r in post if r['meatShare'] > 0.15) / max(1, len(post)) > 0.5,
        'carn': any(sp['meat'] > 0.5 and sp['n'] >= 10 for sp in L[-1]['species']),
        'giant': size >= 5, 'dwarf': size <= 0.35,
        'meat': sum(r['eC'] + r['eK'] for r in half) / eA,
        'preyCl': m('clumpPrey'), 'predCl': m('clumpPred'),
        'diet': sum(r['genes']['diet'] for r in half) / len(half),
    }

def load(d):
    out = {}
    for f in glob.glob(os.path.join(d, 's*.json')):
        b = os.path.basename(f)
        if b.endswith('-genomes.json'): continue
        w = world(f)
        if w: out[b[1:-5]] = w
    return out

base = load(sys.argv[1])
print('baseline', sys.argv[1], len(base), 'worlds')
for arm_dir in sys.argv[2:]:
    arm = load(arm_dir); seeds = sorted(set(base) & set(arm)); n = len(seeds)
    print('\n== %s (%d paired worlds)' % (arm_dir, n))
    for k in ('pred', 'carn', 'giant', 'dwarf'):
        b = sum(base[s][k] for s in seeds); a = sum(arm[s][k] for s in seeds)
        up = sum(1 for s in seeds if arm[s][k] and not base[s][k]); down = sum(1 for s in seeds if base[s][k] and not arm[s][k])
        print('  %-6s baseline %2d  arm %2d   (+%d / -%d)  McNemar p %.3f' % (k, b, a, up, down, binom_p(up, up + down)))
    for k in ('meat', 'preyCl', 'predCl', 'diet'):
        if any(base[s][k] is None or arm[s][k] is None for s in seeds):
            print('  %-6s not logged in one of the batches' % k); continue
        diffs = [arm[s][k] - base[s][k] for s in seeds]
        pos = sum(1 for x in diffs if x > 0); neg = sum(1 for x in diffs if x < 0)
        print('  %-6s baseline %.3f  arm %.3f   mean diff %+.3f  sign test %d+/%d-  p %.3f' % (
            k, sum(base[s][k] for s in seeds) / n, sum(arm[s][k] for s in seeds) / n, sum(diffs) / n, pos, neg, binom_p(pos, pos + neg)))
