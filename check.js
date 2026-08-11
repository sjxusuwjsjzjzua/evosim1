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
  A_ACTIVE, P_ACTIVE, VERSION, LOGCOLS, LOG, logGenes, SELP, SELA, DAGE, UPK };
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

// ---- 2b. structural invariants --------------------------------------
// These are the two things that silently break a build while every other
// stage still reports ok.
//
// (a) LOGCOLS vs the value array. The build only console.warn()s a length
//     mismatch (it does not throw), and a warning scrolls past unnoticed --
//     so a miscounted new column shifts EVERY column after it and the run
//     still "passes". Adding a column means editing two lists that must stay
//     index-aligned, which is exactly the kind of edit that goes wrong.
// (b) The headless ANCHOR. headless.js splices its driver in by matching a
//     literal block at the tail of the build. A change there passes every
//     check below and then makes every single headless run throw, which is
//     how the build is actually exercised.
{
  const before = M.LOG.n;
  M.logSample();
  if (M.LOG.n !== before + 1) {
    console.error('FAIL: logSample did not append a row');
    process.exit(1);
  }
  const nCols = M.LOGCOLS.length;
  let filled = 0;
  for (let i = 0; i < M.LOG.col.length; i++) if (M.LOG.col[i]) filled++;
  if (filled !== nCols) {
    console.error(`FAIL: LOG.col has ${filled} arrays for ${nCols} LOGCOLS names`);
    process.exit(1);
  }
  console.log(`  4. logcols   ok   (${nCols} columns, value array aligned)`);
}
{
  // Kept byte-identical to headless.js's own ANCHOR constant. If you change
  // one, change both -- that coupling is the point of this check.
  const ANCHOR = [
    'resizeCanvas();', 'buildWorld();', 'buildDrawer();', 'refreshSpeed();',
    "$('bGraph').classList.add('on');", 'requestAnimationFrame(frame);',
  ].join('\n');
  if (!html.includes(ANCHOR)) {
    console.error('FAIL: headless ANCHOR missing -- headless.js cannot splice its');
    console.error('      driver, so EVERY headless run of this build will throw.');
    console.error('      Expected this block, verbatim, at the tail:');
    console.error(ANCHOR.split('\n').map(l => '        ' + l).join('\n'));
    process.exit(1);
  }
  console.log('  5. anchor    ok   (headless.js can splice its driver)');
}

// ---- 2c. checkpoint save/restore invariant --------------------------
// headless.js takes a FRESH gene reading at every checkpoint so a run killed
// by a container restart still yields usable gene data [L64]. logGenes() is
// not side-effect free -- geneRow() ends by zeroing the selection
// accumulators, because `sel` is a WINDOW not a cumulative total -- so
// headless.js snapshots that state, reads, and restores it.
//
// That restore was WRONG on first write. The end-to-end rule-7 check caught it
// (plant selN 864 where the control had 191776), but only after three attempts
// were killed mid-flight by container restarts, and the animal half needs a
// 320-day run that has never once survived to completion. So the property is
// asserted directly here instead: populate the accumulators, do exactly what
// headless.js does, and require the state to come back identical. Seconds
// instead of half an hour, and it cannot be killed by a restart.
{
  M.seedAnimalFounders(80);
  M.buildAnimalIndex();
  for (let i = 0; i < 200; i++) M.tick();
  // Populate the accumulators SYNTHETICALLY rather than waiting for the sim to
  // do it. This stage tests headless.js's save/restore logic, not the build's
  // seeding dynamics -- and relying on the latter made the first version pass
  // vacuously with both accumulators at n=0. Distinctive values so a partial
  // or shifted restore cannot look correct by accident.
  if (M.SELP.acc) { for (let i = 0; i < M.SELP.acc.length; i++) M.SELP.acc[i] = i + 0.5; M.SELP.n = 137; }
  if (M.SELA.acc) { for (let i = 0; i < M.SELA.acc.length; i++) M.SELA.acc[i] = -(i + 0.25); M.SELA.n = 91; }
  for (let i = 0; i < M.DAGE.length; i++) M.DAGE[i] = i + 3;
  for (let i = 0; i < M.UPK.length; i++) M.UPK[i] = i * 1.5 + 0.125;
  const snapArr = (a) => (a ? Array.from(a) : null);
  const before = {
    selP: snapArr(M.SELP.acc), selPn: M.SELP.n,
    selA: snapArr(M.SELA.acc), selAn: M.SELA.n,
    dage: snapArr(M.DAGE), upk: snapArr(M.UPK),
  };
  // A round-trip of two empty arrays passes trivially. Refuse to report ok in
  // that case -- a vacuous pass is worse than no test, because it reads as
  // evidence. First version of this stage did exactly that and said "ok".
  // A round-trip of empty arrays passes trivially. Refuse to report ok in that
  // case -- a vacuous pass is worse than no test because it reads as evidence.
  // The first version of this stage did exactly that and printed "ok".
  if (!(before.selP && before.selPn > 0) || !(before.selA && before.selAn > 0)) {
    console.error('FAIL: accumulators not populated (SELP n=' + before.selPn +
                  ', SELA n=' + before.selAn + '); the round-trip would be vacuous.');
    process.exit(1);
  }

  // exactly headless.js's save -> logGenes() -> restore
  const sg = {
    gene: M.LOG.gene.slice(), carn: M.LOG.carn.slice(), hgt: M.LOG.hgt.slice(),
    dage: M.LOG.dage.slice(), upk: M.LOG.upk.slice(), every: M.LOG.geneEvery,
    dageA: snapArr(M.DAGE), upkA: snapArr(M.UPK),
    selP: snapArr(M.SELP.acc), selPn: M.SELP.n,
    selA: snapArr(M.SELA.acc), selAn: M.SELA.n,
  };
  M.logGenes();
  M.LOG.gene = sg.gene; M.LOG.carn = sg.carn; M.LOG.hgt = sg.hgt;
  M.LOG.dage = sg.dage; M.LOG.upk = sg.upk; M.LOG.geneEvery = sg.every;
  M.DAGE.set(sg.dageA); M.UPK.set(sg.upkA);
  if (sg.selP) { M.SELP.acc.set(sg.selP); M.SELP.n = sg.selPn; }
  if (sg.selA) { M.SELA.acc.set(sg.selA); M.SELA.n = sg.selAn; }

  const same = (a, b) => (a === null && b === null) ||
    (a && b && a.length === b.length && a.every((v, i) => v === b[i]));
  const bad = [];
  if (!same(before.selP, snapArr(M.SELP.acc)) || before.selPn !== M.SELP.n) bad.push('SELP');
  if (!same(before.selA, snapArr(M.SELA.acc)) || before.selAn !== M.SELA.n) bad.push('SELA');
  if (!same(before.dage, snapArr(M.DAGE))) bad.push('DAGE');
  if (!same(before.upk, snapArr(M.UPK))) bad.push('UPK');
  if (bad.length) {
    console.error('FAIL: checkpoint restore does not round-trip: ' + bad.join(', '));
    console.error('      headless.js would silently corrupt these in the FINAL log.');
    process.exit(1);
  }
  console.log('  6. checkpoint ok   (round-trips; SELP n=' + before.selPn +
              ', SELA n=' + before.selAn + ')');
}

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
