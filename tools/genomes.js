#!/usr/bin/env node
// Describe an evolved population from a run.js --dump file: gene means and
// brain probes, split by gut (diet >= 0.3 vs < 0.3).
//   node tools/genomes.js dump.json
const fs = require('fs'), vm = require('vm'), path = require('path');
const html = fs.readFileSync(path.join(__dirname, '..', 'evosim.html'), 'utf8');
const ctx = { module: { exports: {} }, console, Math }; vm.createContext(ctx);
vm.runInContext(html.match(/<script id="engine">([\s\S]*?)<\/script>/)[1], ctx);
const Sim = ctx.module.exports, NI = Sim.NI, NH = Sim.NH, NO = Sim.NO;
const d = JSON.parse(fs.readFileSync(process.argv[2]));
const IN = n => Sim.INPUT_NAMES.indexOf(n), sig = x => 1/(1+Math.exp(-x));
function run(G, inp){
  const H = []; for (let h = 0; h < NH; h++){ let s = 0; for (let k = 0; k < NI; k++) s += G[Sim.W1+h*NI+k]*inp[k]; H.push(Math.tanh(s)); }
  const o = []; for (let q = 0; q < NO; q++){ let t = 0; for (let h = 0; h < NH; h++) t += G[Sim.W2+q*NH+h]*H[h];
    for (let k = 0; k < NI; k++) t += G[Sim.WD+q*NI+k]*inp[k]; o.push(t); } return o;
}
function base(hunger){ const a = new Array(NI).fill(0); a[IN('bias')] = 1; a[IN('energy')] = 1 - hunger; a[IN('health')] = 1;
  ['plantHere','plantC','plantL','plantR'].forEach(n => a[IN(n)] = 0.2); return a; }
function probe(G){
  const r = {};
  let a = base(0.5); a[IN('animal')] = 1; a[IN('animalNear')] = 1; a[IN('animalInReach')] = 1; a[IN('animalKin')] = 0.3;
  a[IN('animalSize')] = -0.33; r.strikeSmaller = sig(run(G, a)[4]);
  a[IN('animalSize')] = 0.33; r.strikeBigger = sig(run(G, a)[4]);
  a = base(0.5); a[IN('corpse')] = 1; a[IN('corpseNear')] = 1; a[IN('corpseInReach')] = 1; r.meatPref = sig(run(G, a)[3]);
  // steering toward (+) or away (-) from an animal 0.3*pi to the right, smaller then bigger
  for (const [lab, sz] of [['towardSmaller', -0.33], ['towardBigger', 0.33]]){
    a = base(0.5); a[IN('animal')] = 1; a[IN('animalNear')] = 0.5; a[IN('animalKin')] = 0.3; a[IN('animalSize')] = sz;
    a[IN('animalDir')] = 0.3; const R = Math.tanh(run(G, a)[0]); a[IN('animalDir')] = -0.3; const L = Math.tanh(run(G, a)[0]);
    r[lab] = (R - L)/2;
  }
  a = base(0.5); r.throttleAlone = sig(run(G, a)[1]);
  a[IN('animal')] = 1; a[IN('animalNear')] = 0.5; a[IN('animalSize')] = -0.33; r.throttleSeesSmaller = sig(run(G, a)[1]);
  a[IN('animalSize')] = 0.33; a[IN('animalWeapon')] = 0.5; r.throttleSeesBigArmed = sig(run(G, a)[1]);
  return r;
}
const groups = { carnivores: [], herbivores: [] };
for (const g of d.genomes) (g[3] >= 0.3 ? groups.carnivores : groups.herbivores).push(g);
const B = Sim.BODY.map(b => b[0]);
for (const [name, gs] of Object.entries(groups)){
  if (!gs.length) continue;
  console.log(`\n== ${name} (${gs.length} sampled)`);
  const mean = k => gs.reduce((s, g) => s + g[k], 0)/gs.length;
  console.log(B.map((n, k) => `${n} ${mean(k).toFixed(2)}`).join('  '));
  const P = gs.map(g => probe(g)), pm = k => P.reduce((s, p) => s + p[k], 0)/P.length;
  console.log(Object.keys(P[0]).map(k => `${k} ${pm(k).toFixed(2)}`).join('  '));
}
