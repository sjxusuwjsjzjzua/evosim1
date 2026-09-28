#!/usr/bin/env node
// What smell does in a --dump: brain probes of plant-eaters (diet < 0.3) and meat-eaters.
//   node tools/smell.js dump.json [...]
// Turn toward scent: turn with a channel stronger on the right minus stronger on the left
// (positive = toward), on a scene of grazing among others, level 0.5 in every channel:
//   own    the scent of its own colour (its own tag profile, 0.25 + 0.75 x tag, as animals give off)
//   other  the scent of the opposite colour (1 - tag)
//   meat   carrion
//   fruit  ripe fruit (0 in builds without fruit scent)
// Older dumps are remapped (their smell inputs read 0, so every probe gives 0).
const fs = require('fs'), vm = require('vm'), path = require('path');
const src = fs.readFileSync(path.join(__dirname, '..', 'evosim.html'), 'utf8').match(/<script id="engine">([\s\S]*?)<\/script>/)[1];
const ctx = {module: {exports: {}}, console, Math}; vm.createContext(ctx); vm.runInContext(src, ctx); const Sim = ctx.module.exports;
const {NI, NH, NO, NB, W1, W2, WD, INPUT_NAMES, BODY} = Sim, ix = n => INPUT_NAMES.indexOf(n);
const TAG = BODY.findIndex(b => b[0] === 'tagR'), DIET = BODY.findIndex(b => b[0] === 'diet');
function turn(g, IN){
  const H = []; for (let h = 0; h < NH; h++){ let s = 0; for (let k = 0; k < NI; k++) s += g[W1+h*NI+k]*IN[k]; H.push(Math.tanh(s)); }
  let t = 0; for (let h = 0; h < NH; h++) t += g[W2+h]*H[h]; for (let k = 0; k < NI; k++) t += g[WD+k]*IN[k];
  return Math.tanh(t);
}
function scene(){
  const IN = new Array(NI).fill(0); IN[0] = 1; IN[ix('energy')] = 0.5; IN[ix('health')] = 1;
  for (const n of ['plantL', 'plantC', 'plantR', 'plantHere']) IN[ix(n)] = 0.3;
  IN[ix('crowd')] = 0.3; for (const n of ['smellR', 'smellG', 'smellB', 'smellMeat']) IN[ix(n)] = 0.5; return IN;
}
// channel strengths (right-left) set in proportion to a colour profile
function toward(g, prof){
  const r = scene(), l = scene(), D = ['smellRDir', 'smellGDir', 'smellBDir'];
  const mx = Math.max(...prof); for (let q = 0; q < 3; q++){ r[ix(D[q])] = 0.5*prof[q]/mx; l[ix(D[q])] = -0.5*prof[q]/mx; }
  return turn(g, r) - turn(g, l);
}
function meat(g){ const r = scene(), l = scene(); r[ix('smellMeatDir')] = 0.5; l[ix('smellMeatDir')] = -0.5; return turn(g, r) - turn(g, l); }
function fruit(g){ if (ix('smellFruitDir') < 0) return 0; const r = scene(), l = scene(); r[ix('smellFruitDir')] = 0.5; l[ix('smellFruitDir')] = -0.5; return turn(g, r) - turn(g, l); }
for (const f of process.argv.slice(2)){
  const d = JSON.parse(fs.readFileSync(f));
  const G = d.NG === Sim.NG ? d.genomes : d.genomes.map(g => Array.from(Sim.remapGenome(g, d.NI || 22, d.NO || 5)));
  const line = [];
  for (const [name, sel] of [['grazers', g => g[DIET] < 0.3], ['meat-eaters', g => g[DIET] >= 0.3]]){
    const A = G.filter(sel); if (A.length < 5){ line.push(`${name} ${A.length}`); continue; }
    let own = 0, oth = 0, mt = 0, fr = 0;
    for (const g of A){
      const t = [g[TAG], g[TAG+1], g[TAG+2]];
      own += toward(g, t.map(v => 0.25 + 0.75*v)); oth += toward(g, t.map(v => 0.25 + 0.75*(1 - v))); mt += meat(g); fr += fruit(g);
    }
    const n = A.length;
    line.push(`${name} ${n}  own ${(own/n).toFixed(3)}  other ${(oth/n).toFixed(3)}  meat ${(mt/n).toFixed(3)}  fruit ${(fr/n).toFixed(3)}`);
  }
  console.log(f.split('/').slice(-2).join('/').padEnd(34), line.join('   |   '));
}
