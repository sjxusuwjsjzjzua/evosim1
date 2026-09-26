#!/usr/bin/env python3
"""Which genes separate grazer clusters that cannot interbreed (at most 5% of cross pairs, mateDist 0.1)?

    python3 tools/gsplit.py runs/<label>/s????-genomes.json

Clusters as in isolation.py; for each isolated pair of plant-eater clusters, the four body genes
that differ most (normalised by range), as cluster means. Run from the repo root.
"""
# which genes separate grazer clusters that cannot interbreed? (per dump, mateDist 0.1)
import json, sys, re, math, random

eng = re.search(r'<script id="engine">([\s\S]*?)</script>', open('evosim.html').read()).group(1)
BODY = [(n, float(a), float(b), c == 'true') for n, a, b, c in re.findall(r"\['(\w+)',\s*(-?[\d.]+),\s*(-?[\d.]+),\s*(true|false)\s*\]", eng.split('var BODY = [')[1].split('];')[0])]
TAG, DIET, CHOOSY, md = 9, 3, 13, 0.1
def tag_dist(a, b): return math.sqrt(sum((a[TAG+q]-b[TAG+q])**2 for q in range(3))/3)
def body_dist(a, b):
    t = n = 0
    for k, (_, lo, hi, lg) in enumerate(BODY):
        if TAG <= k < TAG+3: continue
        t += abs(math.log(a[k]/b[k]))/math.log(hi/lo) if lg else abs(a[k]-b[k])/(hi-lo); n += 1
    return t/n
def can(a, b):
    td = tag_dist(a, b)
    return td <= 1-a[CHOOSY] and td <= 1-b[CHOOSY] and body_dist(a, b) <= md
for f in sys.argv[1:]:
    G = json.load(open(f))['genomes']; L = []
    for g in G:
        v = (g[TAG], g[TAG+1], g[TAG+2], g[DIET])
        for c in L:
            if sum((v[q]-c['c'][q])**2 for q in range(4)) < 0.15**2: c['m'].append(g); break
        else: L.append({'c': v, 'm': [g]})
    L = [c for c in sorted(L, key=lambda c: -len(c['m'])) if len(c['m']) >= 0.05*len(G)][:6]
    gr = [c for c in L if sum(g[DIET] for g in c['m'])/len(c['m']) < 0.3]
    rnd = random.Random(1)
    for i in range(len(gr)):
        for j in range(i+1, len(gr)):
            A, B = gr[i]['m'], gr[j]['m']
            sh = sum(can(rnd.choice(A), rnd.choice(B)) for _ in range(300))/3
            if sh > 5: continue
            tagOK = sum(tag_dist(rnd.choice(A), rnd.choice(B)) <= 0.7 for _ in range(300))/3
            diffs = []
            for k, (n, lo, hi, lg) in enumerate(BODY):
                ma = sum(g[k] for g in A)/len(A); mb = sum(g[k] for g in B)/len(B)
                d = abs(math.log(ma/mb))/math.log(hi/lo) if lg else abs(ma-mb)/(hi-lo)
                diffs.append((d, n, ma, mb))
            diffs.sort(reverse=True)
            print('%s: grazers %d x %d cross %.0f%%  top differences: %s' % (f.split('/')[-1], len(A), len(B), sh, ', '.join('%s %.2f/%.2f' % (n, a, b) for d, n, a, b in diffs[:4])))
