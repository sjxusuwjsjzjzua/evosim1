#!/usr/bin/env python3
"""The experiment queue and its bookkeeping (see OPS.md). Run from the repo root.

    python3 tools/ops.py status             jobs in flight, pending entries
    python3 tools/ops.py next [N]           the next N pending entries, as dispatch inputs
    python3 tools/ops.py mark LABEL STATE   pending | dispatched | scored | dropped
    python3 tools/ops.py add LABEL SEEDS TICKS SET BASELINE "EXPECT" [BUILD_REF]
    python3 tools/ops.py digest             fetch landed results, score them, log to ops/log.md
    python3 tools/ops.py wait               block until a dispatched entry's results land
    python3 tools/ops.py evergreen [JOBS]   top the queue up with standing runs until JOBS jobs are pending

SEEDS is "a-b" or "a,b,c". SET is the run.js --set string ("" for none; gridN=64 is added).
A dispatched entry lands on branch results/LABEL. The digest scores it with v1score
(means, predator persistence at >= 800k ticks) and, when BASELINE is given, paired.py.
"""
import json, os, subprocess, sys, time, datetime

Q = 'ops/queue.json'; LOG = 'ops/log.md'

def load():
    return json.load(open(Q)) if os.path.exists(Q) else {'entries': []}
def save(q):
    os.makedirs('ops', exist_ok=True); json.dump(q, open(Q, 'w'), indent=1)
def seeds(spec):
    if '-' in spec and ',' not in spec:
        a, b = spec.split('-'); return [str(s) for s in range(int(a), int(b) + 1)]
    return [s.strip() for s in spec.split(',') if s.strip()]
def now(): return datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M')
def sh(cmd): return subprocess.run(cmd, shell=True, capture_output=True, text=True).stdout
def landed(label): return bool(sh('git rev-parse -q --verify origin/results/%s' % label).strip())

def summary(label):
    out = sh('python3 tools/v1score.py runs/%s/s????.json' % label).splitlines()
    rows = [l.split() for l in out[1:] if l.startswith('s')]
    if not rows: return 'no logs'
    col = {n: k for k, n in enumerate(out[0].split())}
    f = lambda r, n: float(r[col[n]])
    n = len(rows); ticks = max(f(r, 'ticks') for r in rows)
    s = 'worlds %d, meat %.1f%%, kill %.1f%%, carnSp>0 in %d, preyCl %.2f' % (
        n, sum(f(r, 'meat%') for r in rows) / n, sum(f(r, 'kill%') for r in rows) / n,
        sum(f(r, 'carnSp') > 0 for r in rows), sum(f(r, 'preyCl') for r in rows) / n)
    if ticks >= 800000:
        s += ', persisting (predK >= 64%% of run after bootstrap) %d, exits %d, re-entries %d' % (
            sum(f(r, 'predK') * 1000 >= 0.64 * (f(r, 'ticks') - 60000) for r in rows),
            sum(f(r, 'exits') for r in rows), sum(f(r, 'reent') for r in rows))
    return s

def main():
    a = sys.argv[1:] or ['status']; q = load(); E = q['entries']
    if a[0] == 'status':
        sh('git fetch -q origin')
        fl = [e for e in E if e['status'] == 'dispatched']
        pend = [e for e in E if e['status'] == 'pending']
        print('in flight: %d entries, %d jobs (%s)' % (len(fl), sum(len(seeds(e['seeds'])) for e in fl),
              ', '.join(e['label'] + ('*' if landed(e['label']) else '') for e in fl) or '-'))
        print('pending: %d entries, %d jobs' % (len(pend), sum(len(seeds(e['seeds'])) for e in pend)))
        print('(* = landed, run digest)')
    elif a[0] == 'next':
        n = int(a[1]) if len(a) > 1 else 1
        for e in [e for e in E if e['status'] == 'pending'][:n]:
            inp = {'seeds': ','.join(seeds(e['seeds'])), 'ticks': str(e['ticks']),
                   'set': 'gridN=64' + (',' + e['set'] if e['set'] else ''), 'label': e['label']}
            if e.get('build_ref'): inp['build_ref'] = e['build_ref']
            print(json.dumps(inp))
    elif a[0] == 'mark':
        for e in E:
            if e['label'] == a[1]: e['status'] = a[2]; e[a[2] + '_at'] = now()
        save(q)
    elif a[0] == 'add':
        label, sd, ticks, st, base, expect = a[1:7]
        if any(e['label'] == label for e in E): sys.exit('label exists: ' + label)
        E.append({'label': label, 'seeds': sd, 'ticks': int(ticks), 'set': st, 'baseline': base,
                  'expect': expect, 'build_ref': a[7] if len(a) > 7 else '', 'status': 'pending', 'added_at': now()})
        save(q); print('added', label, len(seeds(sd)), 'jobs')
    elif a[0] == 'digest':
        sh('git fetch -q origin'); lines = []
        for e in E:
            if e['status'] != 'dispatched' or not landed(e['label']): continue
            b = e.get('baseline')
            if b and not landed(b) and not os.path.isdir('runs/' + b): continue   # score when its baseline has landed too
            sh('bash tools/fetch-results.sh %s' % e['label'])
            txt = '### %s (%s)\n\n`%s`, seeds %s, %d ticks. Expected: %s\n\n- %s\n' % (
                e['label'], now(), e['set'] or 'defaults', e['seeds'], e['ticks'], e['expect'], summary(e['label']))
            fr = sh('python3 tools/fruit.py runs/%s/s????.json' % e['label']).strip().splitlines()
            if fr and fr[-1].startswith('mean:') and 'fruit=0' not in e['set']: txt += '- fruit: %s\n' % fr[-1][6:]
            b = e.get('baseline')
            if b:
                if not os.path.isdir('runs/' + b): sh('bash tools/fetch-results.sh %s' % b)
                p = sh('python3 tools/paired.py runs/%s runs/%s' % (b, e['label'])).splitlines()[3:]
                txt += '- baseline %s: %s\n' % (b, summary(b))
                txt += ''.join('    ' + l.strip() + '\n' for l in p if l.strip() and 'not logged' not in l)
            lines.append(txt); e['status'] = 'scored'; e['scored_at'] = now()
        if lines:
            new = not os.path.exists(LOG)
            with open(LOG, 'a') as f:
                if new: f.write('# Results log (written by tools/ops.py digest; newest last)\n\n')
                f.write('\n'.join(lines) + '\n')
            save(q); print('\n'.join(lines))
        else: print('nothing new landed')
    elif a[0] == 'wait':
        while True:
            sh('git fetch -q origin')
            ready = lambda e: landed(e['label']) and (not e.get('baseline') or landed(e['baseline']) or os.path.isdir('runs/' + e['baseline']))
            done = [e['label'] for e in E if e['status'] == 'dispatched' and ready(e)]
            if done: print('landed:', ' '.join(done)); return
            if not any(e['status'] == 'dispatched' for e in E): print('nothing in flight'); return
            time.sleep(300)
    elif a[0] == 'evergreen':
        want = int(a[1]) if len(a) > 1 else 36
        pend = lambda: sum(len(seeds(e['seeds'])) for e in E if e['status'] == 'pending')
        used = [int(s) for e in E for s in seeds(e['seeds']) if s.isdigit()]   # fresh seeds, never reused
        nxt = max(used + [1112]) + 1
        while pend() < want:
            lab = 'v1-EG-base-%d' % nxt
            E.append({'label': lab, 'seeds': '%d-%d' % (nxt, nxt + 11), 'ticks': 1000000, 'set': '', 'baseline': '',
                      'expect': 'standing replication of the default build at 1M ticks: predators persist in about 3 of 4',
                      'build_ref': '', 'status': 'pending', 'added_at': now()})
            nxt += 12
        save(q); print('pending jobs:', pend())
    else: sys.exit(__doc__)

if __name__ == '__main__': main()
