#!/usr/bin/env python3
"""Feeding (the give output): per log, early (to 20k ticks) against the last half.

    python3 tools/give.py runs/<label>/s????.json

gift%  energy received as gifts, as a share of all energy taken in (plants, meat, gifts)
kin%   share of gift energy that went to look-alikes (colour distance under 0.3)
juv%   share that went to juveniles (still growing)
"""
import json, sys
def part(rows):
    g = sum(r.get('eG', 0) for r in rows); a = sum(r['eP'] + r['eC'] + r['eK'] for r in rows) + g
    k = sum(r.get('eGkin', 0) for r in rows); j = sum(r.get('eGjuv', 0) for r in rows)
    return 100 * g / max(1e-9, a), 100 * k / max(1e-9, g), 100 * j / max(1e-9, g)
late_g = []
print('%-12s %24s   %24s' % ('run', 'early: gift% kin% juv%', 'late: gift% kin% juv%'))
for f in sys.argv[1:]:
    L = json.load(open(f))['log']
    if 'eG' not in L[-1]: print(f.split('/')[-1], 'no gift fields'); continue
    e = part([r for r in L if r['t'] <= 20000]); l = part(L[len(L) // 2:]); late_g.append(l[0])
    print('%-12s %8.2f %6.0f %6.0f   %8.2f %6.0f %6.0f' % ((f.split('/')[-1],) + e + l))
if late_g:
    s = sorted(late_g); print('late gift%%: median %.2f, max %.2f, worlds above 1%%: %d of %d' % (s[len(s) // 2], s[-1], sum(x > 1 for x in s), len(s)))
