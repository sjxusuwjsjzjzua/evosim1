#!/usr/bin/env node
// Headless runner for evosim.html. Runs the <script id="engine"> block in a
// vm context, so the file you open on a phone is the file that is measured.
//
//   node run.js [--seed 1] [--ticks 200000] [--cfg patch.json | --set k=v,k=v]
//               [--out log.json] [--every 10000] [--build evosim.html]
//
// Prints one summary line every --every ticks and writes the full log.
const fs = require('fs'), vm = require('vm'), path = require('path');
const args = {};
for (let i = 2; i < process.argv.length; i++){
  const a = process.argv[i];
  if (a.startsWith('--')) args[a.slice(2)] = process.argv[i+1] && !process.argv[i+1].startsWith('--') ? process.argv[++i] : true;
}
const build = args.build || path.join(__dirname, 'evosim.html');
const html = fs.readFileSync(build, 'utf8');
const m = html.match(/<script id="engine">([\s\S]*?)<\/script>/);
if (!m) { console.error('no engine block in ' + build); process.exit(1); }
const ctx = { module: { exports: {} }, console, Math };
vm.createContext(ctx);
vm.runInContext(m[1], ctx, { filename: 'engine' });
const Sim = ctx.module.exports;

let patch = {};
if (args.cfg) { const j = JSON.parse(fs.readFileSync(args.cfg, 'utf8')); patch = j.cfg || j; }
if (args.set) for (const kv of String(args.set).split(',')) {
  const [k, v] = kv.split('='); patch[k] = isNaN(+v) ? v : +v;
}
patch.seed = +(args.seed || patch.seed || 1);
const ticks = +(args.ticks || 200000), every = +(args.every || 10000);
Sim.init(patch);
const t0 = Date.now();
const fmt = r => {
  const g = r.genes;
  return `t=${r.t} A=${r.animals} C=${r.corpses} plant=${r.plantMass.toFixed(0)}/${r.plantCells} ` +
    `def=${r.plantDef.toFixed(2)} stat=${r.plantStat.toFixed(2)} | size=${g.size.toFixed(2)} spd=${g.speed.toFixed(2)} ` +
    `sense=${g.sense.toFixed(1)} diet=${g.diet.toFixed(2)} wpn=${g.weapon.toFixed(2)} arm=${g.armour.toFixed(2)} ` +
    `| meat=${(100*r.meatShare).toFixed(1)}% kill=${(100*r.killShare).toFixed(1)}% pred=${r.predators}/${r.adults} ` +
    `kills=${r.kills} gen=${r.meanGen} deaths s/a/k=${r.dStarve}/${r.dAge}/${r.dKill} dh=[${r.dietHist.join(',')}]`;
};
let last = null;
for (let t = 1; t <= ticks; t++) {
  Sim.step();
  const S = Sim.S;
  if (S.tick % every === 0) {
    last = S.log[S.log.length - 1];
    console.log(fmt(last) + `  (${((Date.now() - t0) / 1000).toFixed(0)}s)`);
  }
  if (S.n === 0 && S.tick > Sim.CFG.reseedUntil) { console.log(`extinct at t=${S.tick}`); break; }
}
if (args.out) {
  fs.writeFileSync(args.out, JSON.stringify({ kind: 'evosim1-log', version: Sim.VERSION, cfg: Sim.CFG,
    ticks: Sim.S.tick, wallSec: (Date.now() - t0) / 1000, log: Sim.S.log }));
}
