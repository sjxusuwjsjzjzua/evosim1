#!/usr/bin/env node
// =====================================================================
// check.js — run this after EVERY edit.  node check.js evosim-vX_Y_Z.html
//
// Invariant 14: a syntax check is not a correctness check and a call check is
// not an identifier check.  This does all three:
//
//   1. PARSE     — the script block compiles.
//   2. BOOT      — every top-level statement and every function reached during
//                  init resolves against a permissive DOM stub.  Catches the
//                  ReferenceError/TypeError class that a syntax check cannot.
//   3. EXCEPTION — the changed hot paths (tick, senseDecide, updateAnimal,
//                  drawPlants, rebuildCanopy, compactFree, mutate*) are each
//                  entered at least once and must not throw.
//
// THIS IS NOT A RUN.  It prints no population, no gene mean, no rate.  See
// rule 6b: a short headless run answers a different question than the one
// being asked, and nothing measured here may be compared to a log or used to
// calibrate a constant.  Its only output is pass/fail.
// =====================================================================
'use strict';
const fs = require('fs'), vm = require('vm'), path = require('path');

const file = process.argv[2];
if (!file) { console.error('usage: node check.js <build.html>'); process.exit(2); }
const html = fs.readFileSync(file, 'utf8');

// ---- 1. extract -----------------------------------------------------
const m = html.match(/<script>\n([\s\S]*?)\n<\/script>/);
if (!m) { console.error('FAIL: no <script> block found'); process.exit(1); }
let src = m[1];

// top-level `const` does not land on the context global, so hand them over
src += `
globalThis.__M = { tick, seedFounders, seedAnimalFounders, rebuildCanopy,
  buildAnimalIndex, buildPlantIndex, senseDecide, updateAnimal, updatePlants,
  updateAnimals, drawPlants, drawAnimals, render, mutateInto, mutateAnimal,
  compactFree, collectStats, logSample, AN, P, W, CFG, AGENES, PGENES,
  A_ACTIVE, P_ACTIVE, VERSION };
`;

// ---- DOM stub -------------------------------------------------------
const stub = (name) => new Proxy(function () {}, {
  get(t, k) {
    if (k === Symbol.toPrimitive) return () => 0;
    if (k === Symbol.iterator) return [][Symbol.iterator];
    if (k === 'then' || k === 'inspect' || k === 'constructor') return undefined;
    if (k === 'length') return 0;
    if (k === 'width' || k === 'height' || k === 'clientWidth' || k === 'clientHeight'
        || k === 'innerWidth' || k === 'innerHeight' || k === 'devicePixelRatio') return 400;
    if (k === 'value') return '0';
    if (k === 'textContent' || k === 'innerHTML' || k === 'id' || k === 'className') return '';
    if (k === 'children' || k === 'childNodes') return [];
    return stub(name + '.' + String(k));
  },
  set() { return true; },
  has() { return true; },
  apply() { return stub(name + '()'); },
  construct() { return stub('new ' + name); },
});

const sandbox = {
  console, Math, JSON, Date, Number, String, Array, Object, Error, isNaN, isFinite,
  Float32Array, Float64Array, Int32Array, Uint8Array, Uint32Array, Int16Array,
  Map, Set, Proxy, Symbol, parseInt, parseFloat, setTimeout, clearTimeout,
  document: stub('document'), navigator: stub('navigator'),
  localStorage: stub('localStorage'), history: stub('history'), location: stub('location'),
  performance: { now: () => 0 },
  requestAnimationFrame: () => 0,        // <- the sim never advances on its own
  cancelAnimationFrame: () => {},
  addEventListener: () => {}, removeEventListener: () => {},
  alert: () => {}, prompt: () => null, confirm: () => false,
  Image: function () { return stub('Image'); },
  Blob: function () { return stub('Blob'); },
  File: function () { return stub('File'); },
  FileReader: function () { return stub('FileReader'); },
  URL: { createObjectURL: () => '', revokeObjectURL: () => {} },
  devicePixelRatio: 2, innerWidth: 400, innerHeight: 800,
  matchMedia: () => stub('mql'),
};
sandbox.window = sandbox;
sandbox.globalThis = sandbox;
sandbox.self = sandbox;

const fail = (stage, e) => {
  console.error(`\n  FAIL at ${stage}\n  ${e.constructor.name}: ${e.message}`);
  const st = (e.stack || '').split('\n').slice(1, 6).join('\n');
  if (st) console.error(st);
  process.exit(1);
};

console.log(`check.js  ${path.basename(file)}`);

// ---- 1. parse -------------------------------------------------------
let script;
try { script = new vm.Script(src, { filename: 'evosim.js' }); }
catch (e) { fail('PARSE', e); }
console.log('  1. parse      ok');

// ---- 2. boot --------------------------------------------------------
vm.createContext(sandbox);
try { script.runInContext(sandbox); }
catch (e) { fail('BOOT (top level / init)', e); }
const M = sandbox.__M;
if (!M) fail('BOOT', new Error('export shim did not run'));
console.log(`  2. boot       ok   (build reports VERSION ${M.VERSION})`);

// ---- 3. exception pass ----------------------------------------------
let stage = '';
try {
  stage = 'tick x40 (plants only)';        for (let i = 0; i < 40; i++) M.tick();
  stage = 'rebuildCanopy';                 M.rebuildCanopy();
  stage = 'buildPlantIndex';               M.buildPlantIndex();
  stage = 'seedAnimalFounders';            M.seedAnimalFounders(80);
  stage = 'buildAnimalIndex';              M.buildAnimalIndex();
  stage = 'tick x200 (both kingdoms)';     for (let i = 0; i < 200; i++) M.tick();
  stage = 'compactFree';                   M.compactFree();
  stage = 'collectStats';                  M.collectStats();
  stage = 'logSample';                     M.logSample();
  stage = 'drawPlants';                    M.drawPlants([0, 0]);
  stage = 'drawAnimals';                   M.drawAnimals([0, 0]);
  stage = 'render';                        M.render();

  // every live animal through decide + act, so every arbiter branch that the
  // state permits is entered.  Counting branches, not scoring them.
  stage = 'senseDecide + updateAnimal sweep';
  const seen = new Set();
  let n = 0;
  for (let i = 0; i < M.AN.hi; i++) {
    if (!M.AN.stage[i]) continue;
    M.senseDecide(i);
    seen.add(M.AN.act[i]);
    M.updateAnimal(i);
    n++;
  }
  stage = 'mutate';
  if (M.AN.hi > 1) M.mutateAnimal(1 * M.AGENES, 0 * M.AGENES);
  if (M.P.hi > 1)  M.mutateInto(1 * M.PGENES, 0 * M.PGENES);

  const names = ['REST', 'WANDER', 'GRAZE', 'APPROACH', 'ATTACK', 'SCAVENGE', 'FLEE'];
  const hit = [...seen].sort().map(a => names[a] || ('?' + a)).join(' ');
  console.log(`  3. exception  ok   (${n} decide+act calls, arbiter branches entered: ${hit || 'none'})`);
} catch (e) { fail(stage, e); }

console.log('\n  PASS — no exception. This says NOTHING about whether the change is');
console.log('  correct, only that it resolves and runs. Reason it through against');
console.log('  the last log; do not read numbers out of this harness.\n');
