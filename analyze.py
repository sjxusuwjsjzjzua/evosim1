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
    'pLocked':     (0.50, 0.95, 'refuge, by BIOMASS - trust this one'),
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
        first = next((i for i, v in enumerate(c.get('animals', [])) if v > 0), None)
        parts = []
        for k in ('plants', 'pAdults', 'bio', 'animals'):
            if k not in c: continue
            win = c[k][s:] if k != 'animals' else c[k][max(first or 0, n+s):]
            if not win: continue
            parts.append('%s %.2fx' % (k, max(win)/max(1e-9, min(win))))
        P('  ' + '   '.join(parts))

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
    # ANIMAL ERA ONLY. Averaging in the pre-arrival zeros made harmonic N
    # meaningless on short runs (read 3 on seed 4491, true value 205).
    first = next((i for i, v in enumerate(c['animals']) if v > 0), 0)
    a = c['animals'][max(first, n-1000):]
    zeros = sum(1 for x in a if x == 0)
    live = [x for x in a if x > 0]
    harm = len(live)/sum(1/x for x in live) if live else 0
    P('  animal pop, animal era (%d samples from day %.0f): mean %.0f  HARMONIC %.0f  min %d  max %d%s'
      % (len(a), c['tick'][first]/tpd, st.mean(a), harm, min(a), max(a),
         '   <<DRIFT REGIME' if harm < 500 else ''))
    if zeros:
        P('  >> %d of %d animal-era samples have ZERO animals. THE FAUNA WENT EXTINCT.'
          % (zeros, len(a)))
        P('  >> Nothing below this line about animal genes means anything.')

    # ---- energy
    P('\n-- ENERGY --')
    if 'ePhoto' in c:
        ph = c['ePhoto'][-1]
        ai = sum(c[k][-1] for k in ('ePlant', 'eFlesh', 'eCarrion') if k in c)
        P('  animal intake %.3f%% of gross photosynthesis' % (100*ai/ph if ph else 0))
        if ai:
            P('  of animal intake: plant %.2f%%  carrion %.3f%%  flesh %.3f%%  toxin cost %.1f%%' %
              (100*c['ePlant'][-1]/ai, 100*c['eCarrion'][-1]/ai, 100*c['eFlesh'][-1]/ai,
               100*c.get('eToxin', [0])[-1]/ai))
        else:
            P('  of animal intake: n/a (no intake yet)')
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
    stationary = sec_stationary(c, n, tpd, P)
    sec_demography(c, n, tpd, d, P)
    sec_ne(d, P)
    sec_refuge(c, n, tpd, P)
    sec_actions(c, n, P)
    sec_trophic(c, P)
    sec_ceilings(d, P)
    sec_sel_health(d, P)
    out['selectable'] = sec_selectable(d, P)
    out['stationary'] = stationary

    out['days'] = days
    out['tail'] = {k: st.mean(c[k][tail]) for k in
                   ('plants', 'animals', 'lai', 'aAccess', 'pLocked', 'pPerTile') if k in c}
    out['harm'] = harm
    out['eg'] = egv
    out['drift'] = {k: 100*slope100(c[k][-w:])/(st.mean(c[k][-w:]) or 1)
                    for k in ('plants', 'bio', 'animals') if k in c}
    out['seed'] = d['seed']; out['ver'] = d['version']
    return out


# ------------------------------------------------------- v0.37 additions
# Everything below had to be derived by hand during the v0.36 audit. Each one
# is a question that comes up every cycle, so it belongs in the tool.

def sec_stationary(c, n, tpd, P):
    """Gate. Gene means read off a non-stationary run are a transient, and
    that is a large part of why consecutive versions disagreed."""
    P('')
    P('-- STATIONARITY GATE ' + '-'*56)
    w = max(20, n//3)
    bad = []
    for k in ('plants', 'bio', 'animals', 'soil'):
        if k not in c: continue
        m = st.mean(c[k][-w:]) or 1
        sl = 100*slope100(c[k][-w:])/m
        flag = '  <<DRIFTING' if abs(sl) > 2.0 else ''
        if flag: bad.append(k)
        P('  %-10s %+8.2f %%/100 samples over last third%s' % (k, sl, flag))
    if bad:
        P('  >> NOT STATIONARY (%s). Gene means below are a SNAPSHOT OF A' % ', '.join(bad))
        P('  >> TRANSIENT. Do not compare them against another version.')
    else:
        P('  >> stationary. Gene means are comparable across versions.')
    return not bad


def sec_ne(d, P):
    """Effective population size from the inert genes. Nothing reads them, so
    their spread is pure mutation-drift balance and it is a free Ne meter.
    Census N is not Ne; at v0.36 plant census was 16,197 and this read 'tens'."""
    P('')
    P('-- EFFECTIVE POPULATION (inert-gene diversity) ' + '-'*31)
    INERT = {'plant':  ['mateChoosiness', 'pollenRange', 'selfingTolerance',
                        'pathogenResistance', 'immunity0', 'immunity1', 'immunity2', 'immunity3'],
             'animal': ['parentalCare', 'mateChoosiness', 'pathogenResistance',
                        'immunity0', 'immunity1', 'immunity2', 'immunity3', 'tag0', 'tag1', 'tag2']}
    G = d.get('genes', [])
    if not G: return
    for kind in ('plant', 'animal'):
        names = d['geneNames'][kind]
        idx = [names.index(x) for x in INERT[kind] if x in names]
        if not idx: continue
        snaps = [x for x in G if x[kind]['n'] >= 20]
        if len(snaps) < 4: continue
        # ratio to each gene's OWN early sd: the inert genes span very different
        # ranges (pollenRange 0-30, immunity 0-1) and averaging raw sd just
        # reports the widest one.
        rr = []
        for i in idx:
            a = snaps[1][kind]['sd'][i]; b = snaps[-1][kind]['sd'][i]
            if a > 1e-9: rr.append(b/a)
        if not rr: continue
        r = st.mean(rr)
        trend = 'FALLING' if r < 0.85 else ('rising' if r > 1.15 else 'flat')
        flag = '   <<DIVERSITY BEING LOST' if trend == 'FALLING' else (
               '   <<AT A CEILING, NOT ACCUMULATING' if trend == 'flat' else '')
        P('  %-7s inert sd now %.2fx its early value  (%s, %d genes)%s'
          % (kind, r, trend, len(rr), flag))
        worst = sorted(((snaps[-1][kind]['sd'][i]/snaps[1][kind]['sd'][i], names[i])
                        for i in idx if snaps[1][kind]['sd'][i] > 1e-9))[:3]
        P('           lowest: ' + ',  '.join('%s %.2fx' % (nm, v) for v, nm in worst))
    P('  mutation injects variance every generation; if this is flat or falling,')
    P('  drift is removing it faster and Ne is far below census N.')


def sec_demography(c, n, tpd, d, P):
    """Does the average individual live long enough to breed. If not, every
    lifespan / senescence / care gene is unselected and reads as drift."""
    P('')
    P('-- DEMOGRAPHY ' + '-'*63)
    G = d.get('genes', [])
    matA = None
    if G:
        an = d['geneNames']['animal']
        if 'maturityAge' in an:
            snaps = [x for x in G if x['animal']['n'] >= 20]
            if snaps: matA = snaps[-1]['animal']['mean'][an.index('maturityAge')]/tpd
    da = st.mean(c['aDeathAge'][-min(n, 200):]) if 'aDeathAge' in c else None
    if da is not None and matA:
        r = da/matA
        P('  mean death age %.1f d   maturityAge %.1f d   ratio %.2f%s'
          % (da, matA, r, '   <<DIES BEFORE BREEDING' if r < 1.0 else '   ok'))
    tot = sum(c[k][-1] for k in ('aDeadStarve','aDeadAge','aDeadSen','aDeadKilled') if k in c)
    if tot:
        for k in ('aDeadStarve', 'aDeadSen', 'aDeadAge', 'aDeadKilled'):
            if k in c: P('  %-12s %8d  %5.1f%%' % (k, c[k][-1], 100*c[k][-1]/tot))
        nonstarve = 100*(tot - c.get('aDeadStarve',[0])[-1])/tot
        P('  non-starvation mortality %.2f%%%s' % (nonstarve,
          '   <<NO AGE OR PREDATION SIGNAL: lifespan genes are pure drift' if nonstarve < 5 else ''))
    if 'aJuvFrac' in c:
        P('  juvenile fraction %.2f' % st.mean(c['aJuvFrac'][-min(n,200):]))
    # ---- R0. The handoff calls this a gate and analyze.py never computed it.
    # aBorn is CUMULATIVE; animals is a standing stock; aDeathAge is an interval
    # mean in days. births per animal-lifetime = (births/day/animal) x lifespan.
    # Below 1 the population was never viable no matter how well fed it looked.
    if 'aBorn' in c and 'animals' in c and 'aDeathAge' in c:
        w = min(n - 1, 200)
        i0 = n - 1 - w
        if w > 0:
            dB = c['aBorn'][-1] - c['aBorn'][i0]
            dD = (c['tick'][-1] - c['tick'][i0]) / tpd
            pops = [x for x in c['animals'][i0:] if x > 0]
            ages = [x for x in c['aDeathAge'][i0:] if x > 0]
            if dD > 0 and pops and ages:
                meanN = st.mean(pops)
                life = st.mean(ages)
                r0 = dB / (meanN * dD) * life
                P('  births/animal-lifetime (R0) %.2f   [%d births, mean N %.0f, %.0f d, life %.1f d]%s'
                  % (r0, dB, meanN, dD, life,
                     '   <<R0 < 1: NOT VIABLE, food is not the diagnosis' if r0 < 1.0 else ''))
        # POST-ESTABLISHMENT R0. The line above averages over the LAST 200
        # samples (up to 1000 d), so a short run cannot exclude the founding
        # transient: an 800-day run's window is days 5-800, i.e. its whole
        # history, most of which is the population still establishing. That
        # made R0 rise with run length in 17/18 corpus runs (mean +0.39) and
        # produced a full day of wrong paired conclusions. This second figure
        # starts the window at animalStartDay + a settling margin instead, so
        # it measures the established population regardless of run length.
        # Printed ALONGSIDE the original, never replacing it — every number
        # already in LEDGER.md refers to the line above.  [L61b]
        start = d.get('cfg', {}).get('animalStartDay', 260)
        settle = 340                     # measured: establishment done by ~day 600
        t0 = (start + settle)
        est = [i for i, t in enumerate(c['tick']) if t / tpd >= t0]
        if len(est) >= 40:
            j0 = est[0]
            dB2 = c['aBorn'][-1] - c['aBorn'][j0]
            dD2 = (c['tick'][-1] - c['tick'][j0]) / tpd
            pops2 = [x for x in c['animals'][j0:] if x > 0]
            ages2 = [x for x in c['aDeathAge'][j0:] if x > 0]
            if dD2 > 0 and pops2 and ages2:
                r0b = dB2 / (st.mean(pops2) * dD2) * st.mean(ages2)
                P('  R0 post-establishment  %.2f   [from day %d, %.0f d, mean N %.0f]%s'
                  % (r0b, t0, dD2, st.mean(pops2),
                     '   <<still below replacement' if r0b < 1.0 else ''))
        else:
            P('  R0 post-establishment  n/a   [run too short: needs >%d d]' % t0)


def sec_refuge(c, n, tpd, P):
    """pLocked is the control variable of the whole consumer-resource system:
    across four seeds corr(aSize, pLocked) is -0.86, -0.30, -0.97. Its LEVEL is
    a lagging signal - seed 5499 read 'ok' at 0.393 four samples before the
    fauna went extinct - so watch the rate of decline as well."""
    P('')
    P('-- REFUGE ' + '-'*67)
    if 'pLocked' not in c: return
    # LIVE samples only: after an extinction both aSize and pLocked log as 0,
    # which manufactures a spurious POSITIVE correlation out of the corpse.
    A = c.get('animals', [])
    idx = [i for i in range(len(A)) if A[i] > 0]
    if len(idx) < 8: return
    first = idx[0]
    L = [c['pLocked'][i] for i in idx]
    S = [c['aSize'][i] for i in idx] if 'aSize' in c else []
    P('  pLocked  p10 %.3f  median %.3f  p90 %.3f' %
      (sorted(L)[len(L)//10], st.median(L), sorted(L)[9*len(L)//10]))
    # worst 30-day slide
    win = max(2, int(30*tpd/(c['tick'][1]-c['tick'][0])))
    worst, at = 0.0, 0
    for i in range(len(L)-win):
        drop = L[i] - L[i+win]
        if drop > worst: worst, at = drop, i
    P('  worst %d-day fall  -%.3f  starting day %.0f%s'
      % (30, worst, c['tick'][idx[at]]/tpd,
         '   <<REFUGE COLLAPSING' if worst > 0.15 else ''))
    if S and len(S) == len(L):
        ms, ml = st.mean(S), st.mean(L)
        da = sum((x-ms)**2 for x in S)**.5; db = sum((y-ml)**2 for y in L)**.5
        r = sum((x-ms)*(y-ml) for x, y in zip(S, L))/(da*db) if da*db else 0
        P('  corr(aSize, pLocked) %+.3f%s' % (r,
          '   size is eating the refuge' if r < -0.5 else ''))


def sec_trophic(c, P):
    """Where carrion actually goes. 'tune carrionFloor' is the wrong answer if
    92% of corpse mass rots before anything reaches it."""
    P('')
    P('-- TROPHIC LEDGER ' + '-'*59)
    eaten = c.get('carrionMass', [0])[-1]; rot = c.get('corpseRot', [0])[-1]
    tot = eaten + rot
    if tot:
        P('  corpse mass produced %.0f   eaten %.0f (%.1f%%)   rotted %.0f'
          % (tot, eaten, 100*eaten/tot, rot))
        if 100*eaten/tot < 25:
            P('  >> carrion is not being FOUND. Check sense range against mean animal')
            P('  >> spacing and corpse half-life before touching any carrion constant.')
    intake = sum(c.get(k, [0])[-1] for k in ('ePlant', 'eCarrion', 'eFlesh'))
    if intake:
        for k in ('ePlant', 'eCarrion', 'eFlesh'):
            if k in c: P('  %-9s %12.4g  %6.3f%% of intake' % (k, c[k][-1], 100*c[k][-1]/intake))
    at = c.get('attacks', [0])[-1]; sc = c.get('scavenged', [0])[-1]
    P('  attacks %d   kills %d   scavenge events %d'
      % (at, c.get('aDeadKilled', [0])[-1], sc))
    if sc: P('  energy per scavenge event %.3g' % (c.get('eCarrion',[0])[-1]/sc))


def sec_actions(c, n, P):
    """Behavioural repertoire. If one act is >90% of the budget there is only
    one strategy in the world, whatever the gene table says."""
    P('')
    P('-- ACTION BUDGET ' + '-'*60)
    ks = ['actGraze','actWander','actAppr','actRest','actAttack','actScav','actFlee']
    tail = min(n, 200)
    vals = {k: st.mean(c[k][-tail:]) for k in ks if k in c}
    tot = sum(vals.values()) or 1
    for k, v in sorted(vals.items(), key=lambda kv: -kv[1]):
        P('  %-10s %8.2f  %5.1f%%' % (k, v, 100*v/tot))
    top = max(vals.values())/tot if vals else 0
    if top > 0.90:
        P('  >> %.0f%% of the budget is ONE action. No behavioural variety exists;' % (100*top))
        P('  >> every behaviour gene outside that act is unselected.')


def sec_ceilings(d, P):
    """A gene pinned at a declared bound means the BOUND is doing the selecting,
    not the ecology. 50% is the flag; 15% already deserves a look."""
    P('')
    P('-- GENE BOUNDS ' + '-'*62)
    G = d.get('genes', [])
    if not G: return
    for kind in ('plant', 'animal'):
        names = d['geneNames'][kind]
        snaps = [x for x in G if x[kind]['n'] >= 20]
        if not snaps: continue
        a = snaps[-1][kind]
        hits = []
        for i, nm in enumerate(names):
            for lbl, arr in (('max', a['atMax']), ('min', a['atMin'])):
                if i < len(arr) and arr[i] > 0.15: hits.append((arr[i], kind, nm, lbl))
        for frac, kd, nm, lbl in sorted(hits, reverse=True)[:10]:
            P('  %-7s %-20s %4.0f%% at %s%s' % (kd, nm, 100*frac, lbl,
              '   <<BOUND IS SELECTING' if frac > 0.5 else ''))


def sec_sel_health(d, P):
    """v0.37 made `sel` a fecundity differential against the MATURE mean.
    It is still not total selection. Flag the mismatch rather than trusting it."""
    P('')
    P('-- SELECTION READOUT HEALTH ' + '-'*49)
    G = d.get('genes', [])
    if not G: return
    snaps = [x for x in G if x['plant']['n'] >= 20]
    if not snaps: return
    if 'matureMean' not in snaps[-1]['plant']:
        P('  >> log predates v0.37. `sel` used the WHOLE standing population as its')
        P('  >> baseline, so it contains a life-stage confound as well as fecundity.')
        P('  >> Treat every sel value in this file as unreliable.')
        return
    for kind in ('plant', 'animal'):
        s = [x for x in G if x[kind]['n'] >= 20]
        if not s: continue
        a = s[-1][kind]
        P('  %-7s n %6d   mature %6d (%.0f%%)'
          % (kind, a['n'], a.get('nMature', 0), 100*a.get('nMature', 0)/max(1, a['n'])))
        bad = []
        for i, nm in enumerate(d['geneNames'][kind]):
            if i >= len(a['sel']): break
            if a['atMin'][i] > 0.5 and a['sel'][i] > 0: bad.append((nm, 'pinned at MIN, sel +'))
            if a['atMax'][i] > 0.5 and a['sel'][i] < 0: bad.append((nm, 'pinned at MAX, sel -'))
        for nm, why in bad[:6]:
            P('    %-20s %s   <<FECUNDITY AND VIABILITY DISAGREE' % (nm, why))
    P('  sel is FECUNDITY only. Viability selection is excluded, and viability is')
    P('  most of all mortality. Read it as "who is breeding", never as direction.')


def cross(rows):
    print('\n' + '=' * 78)
    print('CROSS-SEED  (the project rule: believe nothing that does not repeat)')
    ks = ['days', 'plants', 'animals', 'lai', 'pLocked', 'aAccess', 'pPerTile', 'eaten/grown',
          'harmonicN', 'plants %/100d', 'bio %/100d', 'animals %/100d']
    print('  %-14s ' % 'seed' + ' '.join('%12s' % k for k in ks))
    for r in rows:
        if not r.get('stationary', True):
            print('  %-14s NOT STATIONARY - do not compare gene means from this seed'
                  % ('%s v%s' % (r['seed'], r['ver'])))
    for r in rows:
        vals = [r['days']] + [r['tail'].get(k, float('nan')) for k in
                              ('plants', 'animals', 'lai', 'pLocked', 'aAccess', 'pPerTile')]
        vals += [r['eg'], r['harm']] + [r['drift'].get(k, float('nan')) for k in ('plants', 'bio', 'animals')]
        print('  %-14s ' % ('%s v%s' % (r['seed'], r['ver'])) +
              ' '.join('%12.3f' % v for v in vals))


# Genes the simulation loop NEVER reads. Verified by grepping for AG.<name>
# in the build: zero hits each. They mutate and drift exactly like every other
# gene and are acted on by nothing, which makes them a built-in negative
# control for "is selection detectable at all?".
INERT_CONTROL = ['territoriality', 'ambushTendency', 'mateChoosiness',
                 'parentalCare', 'pathogenResistance']


def sec_selectable(d, P):
    """THE SELECTION-RESPONSE GATE.

    Added 2026-08-11 after a strategic audit found that evolved
    meatAttraction was statistically indistinguishable from `territoriality`
    -- a gene with identical bounds, identical sigma, identical founder start
    and ZERO references anywhere in the simulation. Every mechanism claim in
    this project rests on reading an evolved gene value, and nobody had ever
    checked whether the population could move a gene at all.

    Two numbers, both cheap:
      1. neutral variance retention -- inert-gene SD now vs at the first
         populated snapshot. Collapse means drift is swamping selection.
      2. whether ANY functional gene has moved further than the furthest
         inert gene. If not, "the gene did not move" is a statement about the
         population, not about the mechanism under test.

    This gate outranks the ecological sections below it. A run that fails it
    cannot score a mechanism prediction, in either direction.
    """
    P('')
    P('-- SELECTION RESPONSE (can this population move a gene at all?) ' + '-' * 14)
    snaps = [x for x in d.get('genes', []) if x.get('animal', {}).get('n', 0) > 20]
    names = d.get('geneNames', {}).get('animal', [])
    if len(snaps) < 2 or not names:
        P('  n/a  [needs >=2 gene snapshots with a populated animal census]')
        return None
    f, l = snaps[0]['animal'], snaps[-1]['animal']

    ratios = []
    for g in INERT_CONTROL:
        if g not in names:
            continue
        i = names.index(g)
        if i < len(f['sd']) and f['sd'][i] > 1e-9:
            ratios.append(l['sd'][i] / f['sd'][i])
    if not ratios:
        P('  n/a  [no inert control genes found in this build]')
        return None
    keep = st.median(ratios)

    # How far each gene moved, IN UNITS OF ITS OWN STANDING VARIATION
    # (|dmean| / sd_at_first_census). Raw movement is unusable as a yardstick
    # because gene ranges differ by five orders of magnitude -- parentalCare
    # spans [0, 20000] and armour spans [0, 1], so an absolute comparison is
    # just a ranking of gene ranges. The same mistake is live in sec_ne above,
    # which averages parentalCare raw; flagged by the 2026-08-11 strategic
    # audit and not fixed here to keep this one change reviewable.
    def moved(i):
        sd0 = f['sd'][i] if i < len(f['sd']) else 0.0
        if sd0 <= 1e-12 or i >= len(f['mean']):
            return None
        return abs(l['mean'][i] - f['mean'][i]) / sd0

    inert_move = [m for m in (moved(names.index(g)) for g in INERT_CONTROL
                              if g in names) if m is not None]
    ceiling = max(inert_move) if inert_move else 0.0

    P('  neutral variance retained   %.1f%%   [inert-gene SD now / at first census]%s'
      % (100 * keep, '   <<DRIFT DOMINATES' if keep < 0.40 else ''))
    P('  drift yardstick             %.2f sd  [largest move by a gene nothing reads]' % ceiling)

    beat = []
    for g in names:
        if g in INERT_CONTROL:
            continue
        mv = moved(names.index(g))
        if mv is not None and mv > ceiling:
            beat.append((mv, g))
    beat.sort(reverse=True)
    if beat:
        P('  functional genes that beat drift: %d' % len(beat))
        for mv, g in beat[:6]:
            P('      %-22s moved %.2f sd' % (g, mv))
    else:
        P('  functional genes that beat drift: NONE')

    ok = keep >= 0.40 and len(beat) > 0
    if not ok:
        P('  >> SELECTION NOT DEMONSTRABLE. No mechanism prediction is scoreable on')
        P('  >> this run in EITHER direction -- a gene that did not move here is')
        P('  >> evidence about the population, not about the mechanism.')
    return ok


if __name__ == '__main__':
    rows = [digest(p) for p in sys.argv[1:]]
    if len(rows) > 1: cross(rows)
