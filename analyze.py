#!/usr/bin/env python3
"""
evosim log digest.  python3 analyze.py log1.json [log2.json ...]

One fixed page per log, plus a cross-seed table when given several. Exists so
that reading a run costs one tool call instead of ten ad-hoc ones, and so that
the same checks get run every time instead of whichever ones came to mind.

Every threshold here is a STANDING BAND from the ledger. When a band moves,
move it here too, or the verdicts drift away from the project.
"""
import json, sys, statistics as st

# ---------------------------------------------------------------- bands
BANDS = {                       # col: (lo, hi, note)
    'eaten/grown': (0.4, 0.8, 'grazing pressure'),
    'aAccess':     (0.10, 0.40, 'realised browse'),
    'pEscape':     (0.15, 0.55, 'refuge, by plant count'),
    'pLocked':     (0.30, 0.75, 'refuge, by BIOMASS - trust this one'),
    'pPerTile':    (2.0, 99.0, 'two plants must share a tile or no shading'),
    'aSeen':       (0.20, 99.0, 'animal-animal encounters per look'),
    'recruit':     (0.005, 0.30, 'germinations reaching maturity'),
    'aRate/aUpkeep': (1.15, 3.0, 'is eating profitable'),
}
CUM = set('eaten grown limN limE limM pSeeded pGerm pMature pSeedFail pDeadEat '
          'pDeadStarve pDeadAge pDeadSen aBorn aDeadStarve aDeadAge aDeadSen '
          'aDeadKilled attacks scavenged ePhoto ePlant eFlesh eCarrion eToxin '
          'corpseRot abandons pReseed aReseed'.split())

def g(c, k, default=0.0):
    return c[k] if k in c else None

def rates(c, k, n):
    v = c.get(k)
    if v is None: return None
    return [v[i] - v[i-1] for i in range(1, n)]

def slope100(y):
    w = len(y)
    if w < 20: return 0.0
    x = list(range(w)); mx = st.mean(x); my = st.mean(y)
    den = sum((a-mx)**2 for a in x)
    return (sum((a-mx)*(b-my) for a, b in zip(x, y))/den)*100 if den else 0.0

def verdict(name, val):
    if name not in BANDS or val is None: return ''
    lo, hi, _ = BANDS[name]
    if val < lo: return '  <<LOW'
    if val > hi: return '  <<HIGH'
    return '  ok'

def digest(path):
    d = json.load(open(path))
    c = d['cols']; n = len(c['tick']); tpd = d['ticksPerDay']; dpy = d['daysPerYear']
    days = c['tick'][-1]/tpd
    out = {}
    P = print
    P('=' * 78)
    P('%s   v%s  seed %s  %.0f days = %.1f years  %d cols' %
      (path.split('/')[-1], d['version'], d['seed'], days, days/dpy, len(c)))

    # ---- conservation, first, because it outranks everything
    P('\n-- CONSERVATION --')
    m0, m1 = c['matter'][0], c['matter'][-1]
    P('  matter %g -> %g   drift %.6f%%%s' %
      (m0, m1, 100*(m1-m0)/m0 if m0 else 0, '' if m0 == m1 else '   <<LEAK'))
    caps = set(c['caps'])
    P('  caps seen %s%s' % (sorted(caps), '' if caps == {0} else
      '   <<A BOUND IS DOING THE SELECTING, nothing below means what it looks like'))
    # ledger closure
    pin = c['pGerm'][-1]
    pout = sum(c[k][-1] for k in ('pDeadEat', 'pDeadStarve', 'pDeadAge') if k in c)
    if 'pDeadSen' in c: pout += c['pDeadSen'][-1]
    P('  plant  germ %d  deaths %d  standing %d  residual %d (founders + reseeds)' %
      (pin, pout, c['plants'][-1], pin - pout - c['plants'][-1]))
    ain = c['aBorn'][-1] + c.get('aReseed', [0])[-1]
    aout = sum(c[k][-1] for k in ('aDeadStarve', 'aDeadAge', 'aDeadKilled') if k in c)
    if 'aDeadSen' in c: aout += c['aDeadSen'][-1]
    P('  animal born %d  deaths %d  standing %d' % (ain, aout, c['animals'][-1]))
    # The net closes at animalStartDay + animalReseedDays. A big CUMULATIVE
    # aReseed says nothing on its own — v0.35/s2661 tripped the old >200 test
    # with 223 reseeds and then ran 1829 unaided days. What matters is whether
    # reseeds are still ARRIVING after the window, and how much of the run was
    # actually unaided. Report both; only flag on a live drip.
    cfg = d.get('cfg', {})
    netOff = cfg.get('animalStartDay', 0) + cfg.get('animalReseedDays', 0)
    endDay = c['tick'][-1] / d['ticksPerDay']
    rs = c.get('aReseed', [0])
    postDrip = 0
    for i, t in enumerate(c['tick']):
        if t / d['ticksPerDay'] > netOff:
            postDrip = rs[-1] - rs[i]
            break
    unaided = max(0.0, endDay - netOff)
    note = ''
    if postDrip > 0:
        note = '   <<RESEEDING AFTER NET OFF (%d) — FAUNA IS ON LIFE SUPPORT' % postDrip
    elif unaided < 200:
        note = '   <<ONLY %.0f UNAIDED DAYS — RUN TOO SHORT TO JUDGE' % unaided
    P('  life support: pReseed %s  aReseed %s (net off day %.0f, %.0f unaided days)%s' %
      (c.get('pReseed', ['-'])[-1], rs[-1], netOff, unaided, note))

    # ---- trajectory
    P('\n-- TRAJECTORY (window means) --')
    R = {k: rates(c, k, n) for k in ('eaten', 'grown', 'pGerm', 'pMature',
                                     'pDeadEat', 'pDeadStarve', 'aBorn', 'aDeadStarve')}
    cols = [('plants', 7, '%7.0f'), ('pAdults', 7, '%7.0f'), ('animals', 6, '%6.0f'),
            ('pPerTile', 6, '%6.1f'), ('pOcc', 5, '%5.2f'), ('lai', 6, '%6.3f'),
            ('pLocked', 7, '%7.3f'), ('aAccess', 7, '%7.3f'), ('aSeen', 6, '%6.2f'),
            ('pHeight', 7, '%7.3f'), ('aSize', 6, '%6.2f')]
    have = [x for x in cols if x[0] in c]
    P('  %5s %8s %6s ' % ('day', 'eat/gr', 'recr') +
      ' '.join(('%%%ds' % w) % k for k, w, _ in have))
    W = max(1, (n-1)//14)
    for s in range(0, n-1, W):
        e = sum(R['eaten'][s:s+W]); gr = sum(R['grown'][s:s+W])
        gm = sum(R['pGerm'][s:s+W]); mt = sum(R['pMature'][s:s+W]) if R['pMature'] else 0
        P('  %5.0f %8.3f %6.3f ' % (c['tick'][s]/tpd, e/gr if gr else 0, mt/gm if gm else 0) +
          ' '.join(f % st.mean(c[k][s:s+W]) for k, w, f in have))

    # ---- stationarity: the question a single number never answers
    P('\n-- STATIONARITY (last third, percent change per 100 days) --')
    w = max(30, n//3)
    row = []
    for k in ('plants', 'pAdults', 'bio', 'lai', 'pOcc', 'pPerTile', 'animals',
              'pHeight', 'aSize', 'pEscape', 'pLocked', 'soil'):
        if k not in c: continue
        y = c[k][-w:]; m = st.mean(y)
        row.append('%s %+.1f%%' % (k, 100*slope100(y)/m if m else 0))
    P('  ' + '   '.join(row))
    big = [k for k in ('plants', 'bio', 'lai', 'animals') if k in c and
           abs(100*slope100(c[k][-w:])/(st.mean(c[k][-w:]) or 1)) > 2]
    P('  ' + ('NOT STATIONARY on ' + ', '.join(big) if big else 'stationary within 2%/100d'))

    # ---- seasonal amplitude: separates a cohort pulse from a real boom-bust
    yr = int(dpy)
    if n > 3*yr:
        P('\n-- SEASONAL (last %d days, max/min) --' % (10*yr))
        s = -10*yr
        P('  ' + '   '.join('%s %.2fx' % (k, max(c[k][s:])/max(1e-9, min(c[k][s:])))
                            for k in ('plants', 'pAdults', 'bio', 'animals') if k in c))

    # ---- demography
    P('\n-- DEMOGRAPHY (cumulative) --')
    rec = c['pMature'][-1]/pin if 'pMature' in c and pin else None
    P('  plant  germ %d -> mature %d (%s)%s' %
      (pin, c.get('pMature', [0])[-1], '%.4f' % rec if rec else 'n/a',
       verdict('recruit', rec)))
    P('  plant  deaths: eaten %d  starved %d  senescent %s  age %d' %
      (c['pDeadEat'][-1], c['pDeadStarve'][-1],
       c.get('pDeadSen', ['-'])[-1], c['pDeadAge'][-1]))
    P('  animal born %d  starved %d  senescent %s  killed %d  attacks %d  scav %d' %
      (c['aBorn'][-1], c['aDeadStarve'][-1], c.get('aDeadSen', ['-'])[-1],
       c['aDeadKilled'][-1], c['attacks'][-1], c['scavenged'][-1]))
    tail = slice(-min(200, n), None)
    rate_up = (st.mean(c['aRate'][tail]) / st.mean(c['aUpkeep'][tail])
               if st.mean(c['aUpkeep'][tail]) else 0)
    P('  animal aRate/aUpkeep %.2f%s   aFeedFrac %.2f  aJuvFrac %.2f  aDeathAge %.1f' %
      (rate_up, verdict('aRate/aUpkeep', rate_up), st.mean(c['aFeedFrac'][tail]),
       st.mean(c['aJuvFrac'][tail]), st.mean(c['aDeathAge'][tail])))
    # Ne is set by the trough, not the mean
    a = c['animals'][-min(1000, n):]
    harm = len(a)/sum(1/max(1, x) for x in a)
    P('  animal pop last1000d: mean %.0f  HARMONIC %.0f  min %d  max %d%s' %
      (st.mean(a), harm, min(a), max(a),
       '   <<DRIFT REGIME' if harm < 500 else ''))

    # ---- energy
    P('\n-- ENERGY --')
    if 'ePhoto' in c:
        ph = c['ePhoto'][-1]
        ai = sum(c[k][-1] for k in ('ePlant', 'eFlesh', 'eCarrion') if k in c)
        P('  animal intake %.3f%% of gross photosynthesis' % (100*ai/ph if ph else 0))
        P('  of animal intake: plant %.2f%%  carrion %.3f%%  flesh %.3f%%  toxin cost %.1f%%' %
          (100*c['ePlant'][-1]/ai, 100*c['eCarrion'][-1]/ai, 100*c['eFlesh'][-1]/ai,
           100*c.get('eToxin', [0])[-1]/ai))
    if d.get('upkeep'):
        u = d['upkeep'][-1]['terms']; t = sum(v for k, v in u.items() if k != 'gain')
        P('  plant upkeep: ' + ' '.join('%s %.0f%%' % (k, 100*v/t)
                                        for k, v in u.items() if k != 'gain'))
        P('  plant gain/upkeep %.2f' % (u['gain']/t))
    rr = rates(c, 'limN', n); re_ = rates(c, 'limE', n); rm = rates(c, 'limM', n)
    if rr:
        s = -min(500, n-1); a1, b1, c1 = sum(rr[s:]), sum(re_[s:]), sum(rm[s:]); t = a1+b1+c1 or 1
        P('  growth limited by: N %.0f%%  E %.0f%%  M %.0f%%%s' %
          (100*a1/t, 100*b1/t, 100*c1/t, '   <<NUTRIENT-LIMITED' if a1/t > 0.6 else ''))

    # ---- bands
    P('\n-- STANDING BANDS (last 200 samples) --')
    for k in ('aAccess', 'pEscape', 'pLocked', 'pPerTile', 'aSeen'):
        if k in c:
            v = st.mean(c[k][tail]); P('  %-9s %7.3f%s   (%s)' % (k, v, verdict(k, v), BANDS[k][2]))
    e = c['eaten'][-1]-c['eaten'][max(0, n-201)]; gr = c['grown'][-1]-c['grown'][max(0, n-201)]
    egv = e/gr if gr else 0
    P('  %-9s %7.3f%s   (%s)' % ('eaten/grown', egv, verdict('eaten/grown', egv), BANDS['eaten/grown'][2]))

    # ---- genes: only the ones that are saying something
    P('\n-- GENE FLAGS --')
    G = d['genes']
    for kind in ('plant', 'animal'):
        names = d['geneNames'][kind]
        sn = [x[kind] for x in G if x[kind]['n'] > 20]
        if not sn: continue
        first, last = sn[0], sn[-1]
        tl = [x for x in sn[-10:] if x['selN'] > 0]
        P('  [%s]  n=%d' % (kind, last['n']))
        inert_pinned = []
        for i, nm in enumerate(names):
            m, sd = last['mean'][i], last['sd'][i]
            cv = sd/abs(m) if m else 0
            pin_ = max(last['atMin'][i], last['atMax'][i])
            sel = st.mean([t['sel'][i] for t in tl]) if tl else 0
            rel = abs(sel)/(abs(m) or 1)
            tags = []
            if pin_ > 0.5: tags.append('PINNED %.0f%% at %s' % (100*pin_, 'min' if last['atMin'][i] > last['atMax'][i] else 'max'))
            if cv < 0.05: tags.append('CV %.3f' % cv)
            if rel > 0.02: tags.append('sel %+.3g' % sel)
            if abs(m-first['mean'][i]) > 0.60*abs(first['mean'][i] or 1): tags.append('moved %.3g->%.3g' % (first['mean'][i], m))
            if tags: P('    %-20s %s' % (nm, '; '.join(tags)))
            if pin_ > 0.5: inert_pinned.append(nm)
        # drift proof: a gene nothing reads cannot be driven to a bound by selection
        INERT = {'plant': ['pollenRange', 'mateChoosiness', 'selfingTolerance',
                           'pathogenResistance', 'immunity0', 'immunity1', 'immunity2', 'immunity3'],
                 'animal': ['parentalCare', 'mateChoosiness', 'pathogenResistance',
                            'immunity0', 'immunity1', 'immunity2', 'immunity3']}[kind]
        hits = [x for x in inert_pinned if x in INERT]
        if hits:
            P('    >> DRIFT PROOF: inert gene(s) at a bound: %s' % ', '.join(hits))

    # ---- histograms
    P('\n-- HISTOGRAMS (last) --')
    for h in ('heightHistogram', 'carnivoryHistogram', 'deathAgeHistogram'):
        if h in d and d[h]['series']:
            b = d[h]['series'][-1]['bins']; tot = sum(b) or 1
            note = ''
            if h == 'heightHistogram' and b[0]/tot > 0.9: note = '   <<CANOPY IS ONE BAND'
            if h == 'carnivoryHistogram' and b[0]/tot > 0.9: note = '   <<no carnivores'
            if h == 'deathAgeHistogram' and b[0]/tot > 0.5: note = '   <<juveniles dying'
            P('  %-20s %s%s' % (h.replace('Histogram', ''), b, note))

    # ---- lineages: real vs phantom
    if d.get('lineages'):
        P('\n-- LINEAGES --')
        for key, lbl in (('p', 'plant'), ('a', 'animal')):
            seen = {}
            for s in d['lineages']:
                for row in s[key]: seen.setdefault(row[0], []).append(row[1])
            if not seen: continue
            real = {k: v for k, v in seen.items() if len(v) >= 5}
            P('  %-7s %d names, %d persisting >=5 snapshots%s' %
              (lbl, len(seen), len(real),
               '   <<MOSTLY PHANTOM' if len(seen) > 2*max(1, len(real)) else ''))
            for k, v in sorted(real.items(), key=lambda kv: -len(kv[1]))[:6]:
                P('    %-14s %3d snaps  peak %d' % (k, len(v), max(v)))
        tr = d.get('trees', {}).get('plant', [])
        if tr:
            pairs = len({(e['n'], e['p']) for e in tr})
            P('  plant tree: %d entries, %d distinct (name,parent)%s' %
              (len(tr), pairs, '   <<CLUSTER FLICKER' if len(tr) > 1.5*pairs else ''))
    out['days'] = days
    out['tail'] = {k: st.mean(c[k][tail]) for k in
                   ('plants', 'animals', 'lai', 'aAccess', 'pLocked', 'pPerTile') if k in c}
    out['harm'] = harm
    out['eg'] = egv
    out['drift'] = {k: 100*slope100(c[k][-w:])/(st.mean(c[k][-w:]) or 1)
                    for k in ('plants', 'bio', 'animals') if k in c}
    out['seed'] = d['seed']; out['ver'] = d['version']
    return out


def cross(rows):
    print('\n' + '=' * 78)
    print('CROSS-SEED  (the project rule: believe nothing that does not repeat)')
    ks = ['days', 'plants', 'animals', 'lai', 'pLocked', 'aAccess', 'pPerTile', 'eaten/grown',
          'harmonicN', 'plants %/100d', 'bio %/100d', 'animals %/100d']
    print('  %-14s ' % 'seed' + ' '.join('%12s' % k for k in ks))
    for r in rows:
        vals = [r['days']] + [r['tail'].get(k, float('nan')) for k in
                              ('plants', 'animals', 'lai', 'pLocked', 'aAccess', 'pPerTile')]
        vals += [r['eg'], r['harm']] + [r['drift'].get(k, float('nan')) for k in ('plants', 'bio', 'animals')]
        print('  %-14s ' % ('%s v%s' % (r['seed'], r['ver'])) +
              ' '.join('%12.3f' % v for v in vals))


if __name__ == '__main__':
    rows = [digest(p) for p in sys.argv[1:]]
    if len(rows) > 1: cross(rows)
