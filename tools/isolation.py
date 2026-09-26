#!/usr/bin/env python3
"""Reproductive isolation between clusters in a genome dump (run.js --dump).

    python3 tools/isolation.py dump.json [--mateDist 0.1]

Clusters animals by colour tags and diet the way the engine's species() does,
then, for each pair of clusters of 5% or more of the dump, the share of
cross-cluster pairs that could breed under the engine's rule: colour distance
at most 1 - choosy for both partners, and body distance under mateDist (when
mateDist < 1). 0% means the two clusters cannot interbreed at all. Also the
same share within each cluster, for scale. Body gene ranges come from
evosim.html, so run it from the repo root.
"""
import json, sys, re, math, random
args = sys.argv[1:]
md = 1.0
if '--mateDist' in args:
    k = args.index('--mateDist'); md = float(args[k + 1]); del args[k:k + 2]
eng = re.search(r'<script id="engine">([\s\S]*?)</script>', open('evosim.html').read()).group(1)
BODY = [(float(a), float(b), c == 'true') for _, a, b, c in
        re.findall(r"\['(\w+)',\s*(-?[\d.]+),\s*(-?[\d.]+),\s*(true|false)\s*\]", eng.split('var BODY = [')[1].split('];')[0])]
NB, TAG, DIET, CHOOSY = len(BODY), 9, 3, 13

def tag_dist(a, b): return math.sqrt(sum((a[TAG + q] - b[TAG + q]) ** 2 for q in range(3)) / 3)
def body_dist(a, b):
    t = n = 0
    for k, (lo, hi, lg) in enumerate(BODY):
        if TAG <= k < TAG + 3: continue
        t += abs(math.log(a[k] / b[k])) / math.log(hi / lo) if lg else abs(a[k] - b[k]) / (hi - lo); n += 1
    return t / n
def can_breed(a, b):
    td = tag_dist(a, b)
    if td > 1 - a[CHOOSY] or td > 1 - b[CHOOSY]: return False
    return md >= 1 or body_dist(a, b) <= md

for f in args:
    G = json.load(open(f))['genomes']
    L = []
    for g in G:
        v = (g[TAG], g[TAG + 1], g[TAG + 2], g[DIET])
        for c in L:
            if sum((v[q] - c['c'][q]) ** 2 for q in range(4)) < 0.15 ** 2: c['m'].append(g); break
        else: L.append({'c': v, 'm': [g]})
    L = sorted([c for c in L if len(c['m']) >= 0.05 * len(G)], key=lambda c: -len(c['m']))[:6]
    rnd = random.Random(1)
    def share(A, B):
        pairs = [(rnd.choice(A), rnd.choice(B)) for _ in range(400)]
        return 100 * sum(can_breed(a, b) for a, b in pairs) / len(pairs)
    print('==', f.split('/')[-1], '(%d genomes, mateDist %g)' % (len(G), md))
    for i, c in enumerate(L):
        d = sum(g[DIET] for g in c['m']) / len(c['m'])
        print('  cluster %d: n=%d diet %.2f choosy %.2f  breed within %3.0f%%' % (i, len(c['m']), d, sum(g[CHOOSY] for g in c['m']) / len(c['m']), share(c['m'], c['m'])),
              ' '.join('x%d %3.0f%%' % (j, share(c['m'], L[j]['m'])) for j in range(len(L)) if j != i))
