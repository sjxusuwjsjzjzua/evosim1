#!/usr/bin/env python3
"""Daily rhythm (dayTicks > 0): per log, early (to 20k ticks) against the last half.

    python3 tools/daynight.py runs/<label>/s????.json

prey n/d   prey mean speed at night / by day (1 = no rhythm; below 1 = resting at night)
pred n/d   the same for animals living mostly on meat
night%     share of kills made at night (light under 0.5, half of each day)
"""
import json, sys, math
def part(rows):
    r = lambda a, b: sum(x[a] for x in rows) / max(1e-9, sum(x[b] for x in rows))
    k = sum(x['kills'] for x in rows); kn = sum(x['killsNight'] for x in rows)
    return r('preySpNight', 'preySpDay'), (r('predSpNight', 'predSpDay') if any(x['predSpDay'] for x in rows) else float('nan')), 100 * kn / max(1, k)
out = []
print('%-12s %22s   %22s' % ('run', 'early: prey pred night%', 'late: prey pred night%'))
for f in sys.argv[1:]:
    L = json.load(open(f))['log']
    if 'killsNight' not in L[-1]: print(f.split('/')[-1], 'no day/night fields'); continue
    e = part([r for r in L if r['t'] <= 20000]); l = part(L[len(L) // 2:]); out.append(l)
    print('%-12s %7.2f %6.2f %6.0f   %7.2f %6.2f %6.0f' % ((f.split('/')[-1],) + e + l))
if out:
    pr = sorted(x[0] for x in out); print('late prey n/d: median %.2f, range %.2f-%.2f; below 0.8 in %d of %d' % (pr[len(pr) // 2], pr[0], pr[-1], sum(x < 0.8 for x in pr), len(pr)))
    pd = sorted(x[1] for x in out if not math.isnan(x[1]))
    if pd: print('late pred n/d: median %.2f, range %.2f-%.2f' % (pd[len(pd) // 2], pd[0], pd[-1]))
