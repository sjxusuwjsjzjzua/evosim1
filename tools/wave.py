#!/usr/bin/env python3
"""Migration under a travelling season (seasonWave 1): per log, over the last half.

    python3 tools/wave.py runs/<label>/s????.json

track  mean waveTrack: where prey sit in the season (1 = all at the peak of growth).
vx     mean waveVx: prey velocity along the wave in units of the wave's own speed
       (1 = the whole population keeps pace with it; 0 = no net drift).
vx>0   share of log rows with waveVx above 0.
The last line tests whether vx is above 0 across worlds (sign test, exact).
"""
import json, sys, math
rows = []
for f in sys.argv[1:]:
    L = json.load(open(f))['log']; L = [r for r in L[len(L) // 2:] if 'waveVx' in r]
    if not L: print(f.split('/')[-1], 'no wave fields'); continue
    tr = sum(r['waveTrack'] for r in L) / len(L); vx = sum(r['waveVx'] for r in L) / len(L)
    pos = sum(r['waveVx'] > 0 for r in L) / len(L)
    rows.append(vx); print('%-12s track %6.3f  vx %6.3f  vx>0 %3.0f%%' % (f.split('/')[-1], tr, vx, 100 * pos))
if rows:
    k, n = sum(v > 0 for v in rows), len(rows)
    p = min(1, 2 * sum(math.comb(n, i) for i in range(max(k, n - k), n + 1)) / 2 ** n)
    print('worlds %d, vx > 0 in %d, sign test p %.3f, mean vx %.3f' % (n, k, p, sum(rows) / n))
