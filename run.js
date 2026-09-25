#!/usr/bin/env node
// Headless runner for evosim.html. Runs the <script id="engine"> block in a
// vm context, so the file you open on a phone is the file that is measured.
//
//   node run.js [--seed 1] [--ticks 200000] [--cfg patch.json] [--set k=v,k=v]
//               [--out log.json] [--every 10000] [--dump genomes.json] [--build evosim.html]
//
// --set is applied on top of --cfg; --cfg also accepts a log (its cfg is used).
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
const ctx = { module: { exports: {} }, console };   // the context's own Math: a host Math is neither fast to look up nor inlined
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
    `kills=${r.kills} gen=${r.meanGen} deaths s/a/k=${r.dStarve}/${r.dAge}/${r.dKill} clump=${r.clump} dh=[${r.dietHist.join(',')}]` +
    ` sp=${(r.species||[]).map(c => c.n + ':' + c.diet.toFixed(2) + '/' + (100*c.meat).toFixed(0) + '%').join(' ')}`;
};
let last = null;
for (let t = 1; t <= ticks; t++) {
  Sim.step();
  const S = Sim.S;
  if (S.tick % every === 0) {
    last = S.log[S.log.length - 1]; if (!last) continue;
    console.log(fmt(last) + `  (${((Date.now() - t0) / 1000).toFixed(0)}s)`);
    // a partial log survives a killed job
    if (args.out && S.tick % (every*5) === 0) save();
  }
  if (S.n === 0 && (S.established || S.tick > Sim.CFG.reseedUntil)) { console.log(`extinct at t=${S.tick}`); break; }
}
if (args.out) save();
if (args.dump) dump(args.dump);
// --dump <path>: the living population's genomes (body + brain), for seeding
function dump(p) {
  const S = Sim.S, NG = Sim.NG, out = [];
  // every animal with a meat gut (diet > 0.3, up to 100), so a rare carnivore
  // species survives the sampling, then every step-th of the rest to fill ~300
  // slots (the floor on step means the total can run over 300)
  const G = S.genome, take = i => out.push(Array.from(G.subarray(i*NG, (i+1)*NG)).map(v => +v.toFixed(3)));
  const meat = [], rest = [];
  for (let i = 0; i < S.hi; i++) if (S.alive[i]) (G[i*NG + 3] > 0.3 ? meat : rest).push(i);
  meat.slice(0, 100).forEach(take);
  const step = Math.max(1, Math.floor(rest.length / (300 - Math.min(100, meat.length))));
  for (let k = 0; k < rest.length; k += step) take(rest[k]);
  fs.writeFileSync(p, JSON.stringify({ kind: 'evosim1-genomes', version: Sim.VERSION, tick: S.tick, NG, NI: Sim.NI, genomes: out }));
}
function save() {
  fs.writeFileSync(args.out, JSON.stringify({ kind: 'evosim1-log', version: Sim.VERSION, cfg: Sim.CFG,
    ticks: Sim.S.tick, wallSec: (Date.now() - t0) / 1000, log: Sim.S.log }));
}
