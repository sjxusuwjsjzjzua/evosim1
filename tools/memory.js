#!/usr/bin/env node
// What does memory do in an evolved population? Probes of a run.js --dump, split at diet 0.3.
//   node tools/memory.js dump.json [...]
// linger: throttle on a quiet step that follows a scare (hurt, a big armed animal close),
//   minus throttle on a quiet step that follows a quiet one. Non-zero only through memory.
// clock: with every step quiet, how much the memory units still change from step to step
//   after 20 steps (mean |change|); above ~0.05 the brain runs a rhythm of its own.
const fs = require('fs'), vm = require('vm'), path = require('path');
const html = fs.readFileSync(path.join(__dirname, '..', 'evosim.html'), 'utf8');
const ctx = { module: { exports: {} }, console, Math }; vm.createContext(ctx);
vm.runInContext(html.match(/<script id="engine">([\s\S]*?)<\/script>/)[1], ctx);
const Sim = ctx.module.exports, NI = Sim.NI, NH = Sim.NH, NO = Sim.NO;
const IN = n => Sim.INPUT_NAMES.indexOf(n), OUT = n => Sim.OUTPUT_NAMES.indexOf(n), sig = x => 1/(1+Math.exp(-x));
const M1 = IN('mem1'), M2 = IN('mem2'), O1 = OUT('mem1'), O2 = OUT('mem2');
function run(G, inp){
  const H = []; for (let h = 0; h < NH; h++){ let s = 0; for (let k = 0; k < NI; k++) s += G[Sim.W1+h*NI+k]*inp[k]; H.push(Math.tanh(s)); }
  const o = []; for (let q = 0; q < NO; q++){ let t = 0; for (let h = 0; h < NH; h++) t += G[Sim.W2+q*NH+h]*H[h];
    for (let k = 0; k < NI; k++) t += G[Sim.WD+q*NI+k]*inp[k]; o.push(t); } return o;
}
function quiet(m){ const a = new Array(NI).fill(0); a[IN('bias')] = 1; a[IN('energy')] = 0.5; a[IN('health')] = 1; a[IN('light')] = 1;
  ['plantHere','plantC','plantL','plantR'].forEach(n => a[IN(n)] = 0.2); a[M1] = m[0]; a[M2] = m[1]; return a; }
function scare(m){ const a = quiet(m); a[IN('hurt')] = 1; a[IN('health')] = 0.6; a[IN('animal')] = 1; a[IN('animalNear')] = 0.8; a[IN('animalSize')] = 0.66; a[IN('animalWeapon')] = 0.6; return a; }
const mem = o => [Math.tanh(o[O1]), Math.tanh(o[O2])];
function probe(G){
  let m = [0, 0]; for (let t = 0; t < 10; t++) m = mem(run(G, quiet(m)));   // settle
  const base = sig(run(G, quiet(mem(run(G, quiet(m)))))[1]);
  const after = sig(run(G, quiet(mem(run(G, scare(m)))))[1]);
  let mm = m, ch = 0; for (let t = 0; t < 20; t++){ const n = mem(run(G, quiet(mm))); if (t >= 10) ch += (Math.abs(n[0]-mm[0]) + Math.abs(n[1]-mm[1]))/2/10; mm = n; }
  return [after - base, ch];
}
for (const f of process.argv.slice(2)){
  const d = JSON.parse(fs.readFileSync(f));
  if (d.NG !== Sim.NG) d.genomes = d.genomes.map(g => Array.from(Sim.remapGenome(g, d.NI || 22, d.NO || 5)));
  const out = [];
  for (const [name, gs] of [['grazers', d.genomes.filter(g => g[3] < 0.3)], ['meat-eaters', d.genomes.filter(g => g[3] >= 0.3)]]){
    if (gs.length < 5){ continue; }
    const P = gs.map(probe), L = P.map(p => p[0]), C = P.map(p => p[1]);
    out.push(`${name} ${gs.length}: linger ${(L.reduce((a, b) => a + b, 0)/L.length).toFixed(3)} (|linger| ${(L.reduce((a, b) => a + Math.abs(b), 0)/L.length).toFixed(3)}) clock ${(C.reduce((a, b) => a + b, 0)/C.length).toFixed(3)}`);
  }
  console.log(`${f.split('/').slice(-2).join('/')}  ${out.join('  |  ')}`);
}
