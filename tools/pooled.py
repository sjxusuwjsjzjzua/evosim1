#!/usr/bin/env python3
"""Score arms against a frozen pooled baseline instead of same-seed pairs.

Same-seed pairing does nothing at 1M ticks: over 587 arm/baseline pairs the
correlation of meat share is 0.02 and of predator-state share 0.004
(AUDIT-AUDITOR-2026-09-29.md, finding 2). So an arm is compared with every
standing-block world of the current build, frozen in ops/baseline.json.

  python3 tools/pooled.py freeze [SINCE]   pool the standing blocks dispatched at or after SINCE
                                          (default: when smellDecay 0.1 became the default)
  python3 tools/pooled.py runs/ARM [runs/ARM2 ...]   score the arm(s), pooled, against the baseline

Endpoints (predator state as in tools/v1score.py: 20k rolling meat share, in
above 15%, out below 8%, after 60k ticks):
  exits    exits from the predator state per 100k ticks spent in it; exact Poisson p
  reform   carnivore clusters re-formed after the hunter line was gone, per 100k
           ticks outside the predator state; exact Poisson p
  predFrac share of the run (after 60k) in the predator state; rank test p
  persist  predator state for 64%+ of the run (the digest's measure); exact binomial p
  carn     share of samples with a carnivore cluster (10+ animals, meat > 0.5); rank test p
  meat     meat share of intake, last half; rank test p
The per-world scorer follows the auditor's scratch script score_all.py.
"""
import json, glob, os, sys, math

BASE = 'ops/baseline.json'
SINCE = '2026-09-28 14:31'   # smellDecay 0.1 default (commit 6f2f5356)


def world(f):
    d = json.load(open(f))
    L = d.get('log') or []
    if not L: return None
    ticks = d.get('ticks', L[-1]['t'])
    cT = [0.0]; cM = [0.0]
    for r in L:
        cT.append(cT[-1] + r['eP'] + r['eC'] + r['eK']); cM.append(cM[-1] + r['eC'] + r['eK'])
    ts = [r['t'] for r in L]
    carn = lambda r: any(sp['meat'] > 0.5 and sp['n'] >= 10 for sp in r.get('species', []))
    inP = False; predT = 0; outT = 0; exits = 0; prev = None; j = 0
    gone = False      # the hunter line is gone: out of the predator state, no carnivore cluster, <= 2 meat-fed adults
    reform = 0; carnS = []
    for k, r in enumerate(L):
        while ts[j] <= r['t'] - 20000: j += 1
        j0 = max(j, k - 60)
        ms = (cM[k + 1] - cM[j0]) / ((cT[k + 1] - cT[j0]) or 1)
        if r['t'] > 60000:
            c = carn(r); carnS.append(c)
            if not inP and ms > 0.15: inP = True
            elif inP and ms < 0.08: inP = False; exits += 1
            if not inP and not c and r['predators'] <= 2: gone = True
            if gone and c: reform += 1; gone = False
            if prev is not None:
                if inP: predT += r['t'] - prev
                else: outT += r['t'] - prev
        prev = r['t']
    half = L[len(L) // 2:]
    eA = sum(r['eP'] + r['eC'] + r['eK'] for r in half) or 1
    return {'ticks': ticks, 'predT': predT, 'outT': outT, 'exits': exits, 'reform': reform,
            'predFrac': predT / max(1, ticks - 60000), 'persist': predT >= 0.64 * (ticks - 60000),
            'carn': sum(carnS) / max(1, len(carnS)), 'meat': sum(r['eC'] + r['eK'] for r in half) / eA}


def worlds(dirs):
    out = []
    for dd in dirs:
        for f in sorted(glob.glob(os.path.join(dd, 's????.json'))):
            w = world(f)
            if w: out.append(w)
    return out


def pois_p(k, mu):   # two-sided exact Poisson p (sum of outcomes no more likely than k)
    if mu <= 0: return 1.0
    pk = lambda x: math.exp(-mu + x * math.log(mu) - math.lgamma(x + 1))
    p0 = pk(k); hi = int(mu + 20 * math.sqrt(mu) + 20)
    return min(1.0, sum(pk(x) for x in range(hi + 1) if pk(x) <= p0 * (1 + 1e-9)))


def binom_p(k, n, p):
    pk = lambda x: math.exp(math.lgamma(n + 1) - math.lgamma(x + 1) - math.lgamma(n - x + 1) + x * math.log(p) + (n - x) * math.log(1 - p))
    p0 = pk(k)
    return min(1.0, sum(pk(x) for x in range(n + 1) if pk(x) <= p0 * (1 + 1e-9)))


def rank_p(a, b):    # Mann-Whitney U, normal approximation with ties, two-sided
    allv = sorted([(v, 0) for v in a] + [(v, 1) for v in b]); n = len(allv)
    ranks = [0.0] * n; i = 0; tie = 0.0
    while i < n:
        j = i
        while j + 1 < n and allv[j + 1][0] == allv[i][0]: j += 1
        for q in range(i, j + 1): ranks[q] = (i + j) / 2 + 1
        t = j - i + 1; tie += t ** 3 - t; i = j + 1
    na, nb = len(a), len(b)
    ra = sum(r for r, (v, g) in zip(ranks, allv) if g == 0)
    u = ra - na * (na + 1) / 2; mu = na * nb / 2
    sd = math.sqrt(na * nb / 12 * ((n + 1) - tie / (n * (n - 1))))
    return math.erfc(abs(u - mu) / sd / math.sqrt(2)) if sd else 1.0


def freeze(since):
    q = json.load(open('ops/queue.json'))['entries']
    labs = [e['label'] for e in q if e['label'].startswith('v1-EG-base-') and e['status'] == 'scored'
            and e.get('dispatched_at', '') >= since and os.path.isdir('runs/' + e['label'])]
    W = worlds(['runs/' + l for l in labs])
    json.dump({'since': since, 'labels': labs, 'worlds': W}, open(BASE, 'w'))
    print('froze %d blocks, %d worlds since %s' % (len(labs), len(W), since))


def compare(dirs):
    B = json.load(open(BASE)); bw = B['worlds']; A = worlds(dirs)
    if not A: print('no logs in', dirs); return
    rate = lambda W, k, t: sum(w[k] for w in W) / max(1e-9, sum(w[t] for w in W) / 1e5)
    print('baseline: %d worlds (%d blocks since %s); arm: %d worlds from %s' % (len(bw), len(B['labels']), B['since'], len(A), ' '.join(dirs)))
    for k, t, name in (('exits', 'predT', 'exits per 100k predator ticks'), ('reform', 'outT', 'carnivore re-formations per 100k collapsed ticks')):
        rb = rate(bw, k, t); n = sum(w[k] for w in A); mu = rb * sum(w[t] for w in A) / 1e5
        print('  %-48s baseline %.3f  arm %.3f  (%d against %.1f expected)  Poisson p %.3f' % (name, rb, rate(A, k, t), n, mu, pois_p(n, mu)))
    pb = sum(w['persist'] for w in bw) / len(bw); k = sum(w['persist'] for w in A)
    print('  %-48s baseline %.3f  arm %.3f  (%d of %d)  binomial p %.3f' % ('persisting (64%+ of the run)', pb, k / len(A), k, len(A), binom_p(k, len(A), pb)))
    for key, name in (('predFrac', 'share of the run in the predator state'), ('carn', 'share of samples with a carnivore cluster'), ('meat', 'meat share, last half')):
        mb = sum(w[key] for w in bw) / len(bw); ma = sum(w[key] for w in A) / len(A)
        print('  %-48s baseline %.3f  arm %.3f  rank test p %.3f' % (name, mb, ma, rank_p([w[key] for w in A], [w[key] for w in bw])))
    # the smallest cut in the exit rate this arm could show at p < 0.05
    mu = rate(bw, 'exits', 'predT') * sum(w['predT'] for w in A) / 1e5
    lo = next((x for x in range(int(mu) + 1) if pois_p(x, mu) >= 0.05), 0)
    print('  power: this arm reaches p < 0.05 on exits at %d or fewer (%.0f%% of the %.1f expected)' % (lo - 1, 100 * (lo - 1) / mu if mu else 0, mu))


if __name__ == '__main__':
    a = sys.argv[1:]
    if not a: print(__doc__)
    elif a[0] == 'freeze': freeze(a[1] if len(a) > 1 else SINCE)
    else: compare(a)
