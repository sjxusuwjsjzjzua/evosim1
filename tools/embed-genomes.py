#!/usr/bin/env python3
"""Embed an evolved population into evosim.html for the 'evolved start' button.

    python3 tools/embed-genomes.py genomes.json "note about where it came from"

genomes.json is written by `node run.js ... --dump genomes.json`. Each gene is
quantised to one byte over its range (body genes over their bounds, brain
weights over [-wMax, wMax]) and the lot is base64'd between the EVOLVED markers
in the UI script. The engine is not touched. Run it from the repo root. Dumps
without an NI field predate it and have 22 senses.
"""
import json, sys, re, base64
src = json.load(open(sys.argv[1])); note = sys.argv[2] if len(sys.argv) > 2 else ''
html = open('evosim.html').read()
eng = re.search(r'<script id="engine">([\s\S]*?)</script>', html).group(1)
body = re.findall(r"\['(\w+)',\s*(-?[\d.]+),\s*(-?[\d.]+),\s*(true|false)\s*\]", eng.split('var BODY = [')[1].split('];')[0])
wmax = float(re.search(r'wMax:\s*([\d.]+)', eng).group(1))
NB = len(body); NG = src['NG']
lo = [float(b[1]) for b in body] + [-wmax]*(NG-NB); hi = [float(b[2]) for b in body] + [wmax]*(NG-NB)
out = bytearray()
for g in src['genomes']:
    for k in range(NG):
        v = min(max(g[k], lo[k]), hi[k])
        out.append(round(255*(v-lo[k])/(hi[k]-lo[k])))
b64 = base64.b64encode(bytes(out)).decode()
block = ("/*EVOLVED-START*/var EVOLVED = {NG: %d, ni: %d, no: %d, n: %d, tick: %d, note: %s, data: '%s'};/*EVOLVED-END*/"
         % (NG, src.get('NI', 22), src.get('NO', 5), len(src['genomes']), src.get('tick', 0), json.dumps(note), b64))
if '/*EVOLVED-START*/' in html:
    html = re.sub(r'/\*EVOLVED-START\*/[\s\S]*?/\*EVOLVED-END\*/', lambda m: block, html)
else:
    sys.exit('no EVOLVED markers in evosim.html')
open('evosim.html', 'w').write(html)
print('embedded %d genomes, %d bytes base64' % (len(src['genomes']), len(b64)))
