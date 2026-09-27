#!/usr/bin/env python3
"""Fruit and plants: per log, early (to 50k ticks) against the last half.

    python3 tools/fruit.py runs/<label>/s????.json

gene   mean fruit gene of the plants (0 = no fruit)
div    plant genetic diversity (mean sd of the four plant genes; logged as plantDiv)
fruit% share of the animals' plant energy that came from fruit
carried share of new plants that grew from animal-carried seed
"""
import json, sys
out = []
for f in sys.argv[1:]:
    L = json.load(open(f))['log']; h = L[len(L) // 2:]; e = [r for r in L if r['t'] <= 50000]
    m = lambda R, k: sum(r.get(k, 0) for r in R) / max(1, len(R))
    eF = sum(r.get('eF', 0) for r in h); eP = sum(r['eP'] for r in h)
    sa = sum(r.get('seedsAnimal', 0) for r in h); sw = sum(r.get('seedsWind', 0) for r in h)
    row = (m(e, 'plantFruit'), m(h, 'plantFruit'), m(h, 'plantDiv'), 100 * eF / max(1, eP), 100 * sa / max(1, sa + sw))
    out.append(row); print('%-11s gene %.3f -> %.3f  div %.3f  fruit %4.1f%%  carried %4.1f%%' % ((f.split('/')[-1],) + row))
if out:
    n = len(out); print('mean: gene %.3f -> %.3f (up in %d of %d), div %.3f, fruit %.1f%%, carried %.1f%%' % (
        sum(r[0] for r in out) / n, sum(r[1] for r in out) / n, sum(r[1] > r[0] for r in out), n,
        sum(r[2] for r in out) / n, sum(r[3] for r in out) / n, sum(r[4] for r in out) / n))
