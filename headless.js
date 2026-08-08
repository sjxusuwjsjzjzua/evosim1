#!/usr/bin/env node
'use strict';
/*
 * headless.js — run an evosim build outside the browser.
 *
 * Does not modify or fork the build. Reads the shipped HTML as data, pulls
 * out its own <script> verbatim, and runs it in a Node vm context behind a
 * permissive DOM/BOM stub (every element/method the script might touch is a
 * no-op Proxy; nothing renders, nothing needs to). The browser-only trailing
 * block — canvas sizing, the drawer UI, requestAnimationFrame — is spliced
 * out and replaced with a driver that applies a CFG override, calls the
 * build's own buildWorld()/tick() directly, and emits the exact JSON shape
 * exportLog() writes on the phone. analyze.py does not know the difference.
 *
 * The splice point is one exact, literal anchor string taken from the tail
 * of the file. If a future build changes that block, this throws instead of
 * silently running the wrong thing — update ANCHOR to match.
 *
 * A long run is a black box until it finishes, which is dangerous for
 * exactly the reason rule 1 exists — so this writes real state out while it
 * runs, through two plain files (not a debugger port, not a signal into a
 * busy synchronous loop, both of which are unreliable mid-tick-loop):
 *
 *   <out>.progress.json  — rewritten every --progress-days sim-days with
 *                           {tick, days, plants, animals, elapsedSec, ticksPerSec}.
 *                           `cat` it any time; stale data older than a couple
 *                           of these intervals means the process died.
 *   <out>.stop            — touch this file to request a graceful stop.
 *                           Checked every 256 ticks (cheap). The run then
 *                           finishes exactly like it hit its day budget:
 *                           full logGenes(), full JSON, `headless.stopRequested:
 *                           true` in the output. No output is EVER written
 *                           before the loop ends one way or another, so an
 *                           impatient `kill` (not this file) still loses
 *                           everything — use the stop file instead.
 *
 * Usage:
 *   node headless.js --build evosim-v0_47_0.html --seed 1337 --days 1200 \
 *        [--cfg patch.json] --out runs/foo/seed-1337.json \
 *        [--progress-days 20] [--max-ticks N] [--no-autohalt]
 *
 * --cfg accepts either a raw {"k_confusion":0} diff or a full
 * {"kind":"evosim-cfg",...,"cfg":{...}} patch file — either shape works.
 */
const fs = require('fs');
const path = require('path');
const vm = require('vm');

function parseArgs(argv) {
  const out = {};
  for (let i = 0; i < argv.length; i++) {
    const a = argv[i];
    if (a.startsWith('--')) {
      const key = a.slice(2);
      const next = argv[i + 1];
      if (next === undefined || next.startsWith('--')) out[key] = true;
      else { out[key] = next; i++; }
    }
  }
  return out;
}

const ANCHOR = `resizeCanvas();
buildWorld();
buildDrawer();
refreshSpeed();
$('bGraph').classList.add('on');
requestAnimationFrame(frame);`;

// A generic, infinitely-deep stub: readable, writable, callable, chainable.
// Standing in for every DOM element / window / navigator / etc. the script's
// top-level (non-function-body) statements touch on load. Nothing rendered
// is ever read back, so "wrong" values here are harmless by construction —
// the only failure mode this needs to avoid is throwing.
function makeStub() {
  const target = function stub() {};
  const handler = {
    get(t, prop) {
      if (prop === Symbol.toPrimitive) return () => 0;
      if (prop === 'then' || prop === 'nodeType') return undefined;
      if (prop === 'classList') return { add(){}, remove(){}, toggle(){}, contains(){ return false; } };
      if (prop === 'children' || prop === 'childNodes') return [];
      if (!(prop in t)) t[prop] = makeStub();
      return t[prop];
    },
    set(t, prop, val) { t[prop] = val; return true; },
    apply() { return makeStub(); },
  };
  return new Proxy(target, handler);
}

function buildSandbox({ onProgress, shouldStop }) {
  const sandbox = {
    console,
    document: makeStub(),
    window: makeStub(),
    navigator: makeStub(),
    screen: makeStub(),
    localStorage: makeStub(),
    performance: { now: () => Date.now() },
    requestAnimationFrame: () => 0,
    cancelAnimationFrame: () => {},
    alert: () => {},
    confirm: () => false,
    prompt: () => null,
    URL: { createObjectURL: () => '', revokeObjectURL: () => {} },
    Blob: function Blob() {},
    FileReader: function FileReader() { this.readAsText = () => {}; },
    // Real Node callbacks the injected driver uses to talk to the outside
    // world without ever needing to interrupt the tick loop mid-flight.
    __reportProgress: onProgress,
    __shouldStop: shouldStop,
  };
  return sandbox;
}

function extractScript(html) {
  const m = html.match(/<script>([\s\S]*?)<\/script>/);
  if (!m) throw new Error('no <script> block found in build HTML');
  return m[1];
}

function spliceDriver(script, { seed, days, maxTicks, cfgOverrides, autohalt, progressDays }) {
  if (!script.includes(ANCHOR)) {
    throw new Error(
      'headless.js ANCHOR text not found in the build. The trailing init ' +
      'block in the HTML changed shape — update ANCHOR in headless.js to match ' +
      'the new tail before trusting this tool again.'
    );
  }
  const overrides = Object.assign({ seed }, cfgOverrides || {});
  const driver = `
// ==== headless driver (injected by headless.js, not part of the build) ====
Object.assign(CFG, ${JSON.stringify(overrides)});
buildWorld();
let __haltedEarly = false, __stopRequested = false;
{
  const __tpd = TPD();
  const __t0 = performance.now();
  const __maxTicks = ${maxTicks != null ? Number(maxTicks) : `Math.round(${JSON.stringify(days)} * __tpd)`};
  const __autohalt = ${autohalt ? 'true' : 'false'};
  const __progressEvery = Math.max(1, Math.round(${JSON.stringify(progressDays)} * __tpd));
  for (let __i = 0; __i < __maxTicks; __i++) {
    tick();
    if ((__i & 255) === 0 && __shouldStop()) { __haltedEarly = true; __stopRequested = true; break; }
    if (W.tick % __progressEvery === 0) {
      const __el = (performance.now() - __t0) / 1000;
      __reportProgress({
        tick: W.tick, days: +(W.tick / __tpd).toFixed(2), targetDays: ${JSON.stringify(days ?? null)},
        plants: ST.pop, animals: ST.apop, elapsedSec: +__el.toFixed(1),
        ticksPerSec: __el > 0 ? +(W.tick / __el).toFixed(0) : null, done: false,
      });
    }
    if (__autohalt && LOG.aGone && !ST.apop &&
        (W.tick - LOG.aGoneTick) > CFG.haltAfterDays * __tpd) { __haltedEarly = true; break; }
  }
}
logGenes();
const __cols = {};
for (let __c = 0; __c < LOGCOLS.length; __c++) {
  const __src = LOG.col[__c], __a = new Array(LOG.n);
  for (let __j = 0; __j < LOG.n; __j++) {
    const __v = __src[__j];
    __a[__j] = Math.abs(__v) >= 1000 ? Math.round(__v) : +__v.toFixed(4);
  }
  __cols[LOGCOLS[__c]] = __a;
}
const __data = {
  kind: 'evosim-log', version: VERSION, formatVersion: FORMAT_VERSION,
  seed: W.seed, tick: W.tick, sampleEvery: LOG.every,
  ticksPerDay: TPD(), daysPerYear: CFG.daysPerYear,
  slots: { plants: CFG.maxPlants, animals: CFG.maxAnimals,
           seeds: Math.round(CFG.maxPlants * CFG.seedSlotFraction) },
  cfg: Object.assign({}, CFG),
  geneNames: { plant: geneNames(PG), animal: geneNames(AG) },
  cols: __cols, genes: LOG.gene, lineages: LOG.lin, events: LOG.events,
  clusterGenes: { plant: PLIN ? PLIN.spec.genes : [], animal: ALIN ? ALIN.spec.genes : [] },
  trees: { plant: PLIN ? PLIN.tree : [], animal: ALIN ? ALIN.tree : [] },
  upkeep: LOG.upk,
  carnivoryHistogram: { bins: CARNBINS, series: LOG.carn },
  heightHistogram: { bins: HGTBINS, series: LOG.hgt },
  deathAgeHistogram: { bins: DAGEBINS, note: 'age at death in quarters of maturityAge', series: LOG.dage },
  headless: { tool: 'headless.js', haltedEarly: __haltedEarly, stopRequested: __stopRequested }
};
__reportProgress({ tick: W.tick, days: +(W.tick / TPD()).toFixed(2), plants: ST.pop, animals: ST.apop, done: true });
JSON.stringify(__data);
`;
  return script.replace(ANCHOR, driver);
}

function loadCfgOverrides(cfgPath) {
  if (!cfgPath) return {};
  const raw = JSON.parse(fs.readFileSync(cfgPath, 'utf8'));
  return raw && typeof raw.cfg === 'object' ? raw.cfg : raw;
}

function main() {
  const args = parseArgs(process.argv.slice(2));
  if (!args.build || args.seed === undefined || (args.days === undefined && args['max-ticks'] === undefined)) {
    console.error('usage: node headless.js --build <html> --seed <n> --days <n> --out <path> ' +
                   '[--cfg patch.json] [--progress-days 20] [--max-ticks n] [--no-autohalt]');
    process.exit(1);
  }
  const buildPath = args.build;
  const seed = Number(args.seed);
  const days = args.days !== undefined ? Number(args.days) : undefined;
  const maxTicks = args['max-ticks'] !== undefined ? Number(args['max-ticks']) : undefined;
  const cfgOverrides = loadCfgOverrides(args.cfg);
  const autohalt = !args['no-autohalt'];
  const progressDays = args['progress-days'] !== undefined ? Number(args['progress-days']) : 20;

  // outPath has to be known BEFORE the run starts now — progress/stop files
  // live next to it. Final tick count is no longer part of the default name.
  let outPath = args.out || `evosim-log-s${seed}.json`;
  if (outPath.endsWith('/')) outPath = path.join(outPath, `evosim-log-s${seed}.json`);
  fs.mkdirSync(path.dirname(outPath) || '.', { recursive: true });
  const progressPath = outPath + '.progress.json';
  const stopPath = outPath + '.stop';
  if (fs.existsSync(stopPath)) fs.unlinkSync(stopPath); // stale from a reused path

  const html = fs.readFileSync(buildPath, 'utf8');
  const script = extractScript(html);
  const finalScript = spliceDriver(script, { seed, days, maxTicks, cfgOverrides, autohalt, progressDays });

  const onProgress = (info) => {
    try { fs.writeFileSync(progressPath, JSON.stringify(info)); } catch (e) { /* best-effort */ }
  };
  const shouldStop = () => { try { return fs.existsSync(stopPath); } catch (e) { return false; } };
  const sandbox = buildSandbox({ onProgress, shouldStop });
  const context = vm.createContext(sandbox);
  const t0 = Date.now();
  let jsonText;
  try {
    jsonText = vm.runInContext(finalScript, context, { filename: path.basename(buildPath) });
  } catch (e) {
    console.error('headless run threw:', e.stack || e);
    process.exit(1);
  }
  const elapsed = (Date.now() - t0) / 1000;

  const data = JSON.parse(jsonText);
  fs.writeFileSync(outPath, jsonText);
  if (fs.existsSync(stopPath)) fs.unlinkSync(stopPath);

  const days_ = data.tick / data.ticksPerDay;
  console.error(`seed ${data.seed}: ${data.tick} ticks = ${days_.toFixed(1)} days in ${elapsed.toFixed(1)}s ` +
                `(${(data.tick / elapsed).toFixed(0)} ticks/s)${data.headless.stopRequested ? ' [STOPPED EARLY by request]' : ''}` +
                `${data.headless.haltedEarly && !data.headless.stopRequested ? ' [AUTOHALTED: fauna extinct, no recovery]' : ''}` +
                ` -> ${outPath}`);
}

main();
