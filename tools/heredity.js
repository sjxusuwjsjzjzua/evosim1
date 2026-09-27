#!/usr/bin/env node
// node tools/heredity.js — are learned changes inherited? (They must not be.) In a learning world, every birth is checked: the newborn's
// genome against the parents' genomes and against the parents' learned weights, and the
// newborn's starting brain against its own genome. Then a harsher test: scramble every
// animal's learned weights and check that the next generation's genomes do not move.
const fs = require('fs'), vm = require('vm'), path = require('path');
function load(patches){   // the engine block of evosim.html, with source patches [[from, to], ...]
  let src = fs.readFileSync(path.join(__dirname, '..', 'evosim.html'), 'utf8').match(/<script id="engine">([\s\S]*?)<\/script>/)[1];
  for (const [a, b] of patches){ if (!src.includes(a)) throw new Error('patch anchor missing: ' + a); src = src.replace(a, b); }
  const ctx = {module: {exports: {}}, console, Math}; vm.createContext(ctx); vm.runInContext(src, ctx); return ctx.module.exports;
}
const Sim = load([
  ["var CFG, S;", "var CFG, S; var BR = [];"],
  ["        if (mate >= 0) recombine(k, i, mate); else copyGenome(k, i);",
   "        if (mate >= 0) recombine(k, i, mate); else copyGenome(k, i); var PRE = S.genome.slice(k*NG, (k+1)*NG);"],
  ["        setupBody(k, S.x[i], S.y[i], mk, S.gen[i]+1);",
   "        setupBody(k, S.x[i], S.y[i], mk, S.gen[i]+1); if (BR.length < 3000) BR.push({k: k, p: i, mate: mate, pre: PRE});"],
  ["return { init: init,", "return { BR: BR, init: init,"]]);
Sim.init({seed: 11, gridN: 64, learn: 1});
const S = Sim.S, NG = Sim.NG, NB = Sim.NB, NW = NG - NB;
let sex = 0, sexG = 0, sexL = 0, sexX = 0, n = 0, clones = 0, sameAsGenome = 0, sameAsLearned = 0, lwDiffers = 0, startOK = 0, parentMoved = 0;
for (let t = 0; t < 60000; t++){ Sim.BR.length = 0; Sim.step(); check(); }
function check(){
  for (const b of Sim.BR){
    n++;
    const c = b.k*NG, p = b.p*NG, pl = b.p*NW, cl = b.k*NW;
    // the newborn starts from its own genome
    let ok = true; for (let w = 0; w < NW; w++) if (S.lw[cl+w] !== S.genome[c+NB+w]){ ok = false; break; }
    if (ok) startOK++;
    if (b.mate >= 0){ sex++; const m = b.mate*NG, ml = b.mate*NW;
      for (let w = 0; w < NW; w++){ const v = b.pre[NB+w];
        if (v === S.genome[p+NB+w] || v === S.genome[m+NB+w]) sexG++;
        else if (v === S.lw[pl+w] || v === S.lw[ml+w]) sexL++; else sexX++; }
      continue; }
    clones++;
    // before mutation, a clone's brain genes equal the parent's genome exactly, not its learned weights
    let g = 0, l = 0, moved = 0;
    for (let w = 0; w < NW; w++){
      const pre = b.pre[NB+w];
      if (pre === S.genome[p+NB+w]) g++;
      if (pre === S.lw[pl+w]) l++;
      if (S.lw[pl+w] !== S.genome[p+NB+w]) moved++;
    }
    sameAsGenome += g/NW; sameAsLearned += l/NW; parentMoved += moved/NW;
  }
}
console.log(`births ${n}: newborn brain starts exactly at its own genome in ${startOK}`);
console.log(`clone births ${clones}: before mutation the child's brain genes equal the parent's GENOME in ${(100*sameAsGenome/clones).toFixed(2)}% of weights, the parent's LEARNED weights in ${(100*sameAsLearned/clones).toFixed(2)}% (parents had moved ${(100*parentMoved/clones).toFixed(1)}% of their weights by learning)`);
console.log(`sexual births ${sex}: brain genes taken from a parent's genome ${sexG}, from a parent's learned weights only ${sexL}, from neither ${sexX}`);
// scramble the learned weights of every animal alive now; follow their births by id
const G0 = new Map();
for (let i = 0; i < S.hi; i++) if (S.alive[i]){
  G0.set(S.id[i], S.genome.slice(i*NG, (i+1)*NG));
  for (let w = 0; w < NW; w++) S.lw[i*NW+w] = 4*(Math.random()*2 - 1);
}
let kids = 0, leak = 0, diff = 0;
for (let t = 0; t < 20000; t++){ Sim.BR.length = 0; Sim.step();
  for (const b of Sim.BR){ if (b.mate >= 0) continue; const g0 = G0.get(S.id[b.p]); if (!g0) continue; kids++;
    for (let w = 0; w < NW; w++){ if (b.pre[NB+w] !== g0[NB+w]) diff++; if (b.pre[NB+w] === S.lw[b.p*NW+w] && S.lw[b.p*NW+w] !== g0[NB+w]) leak++; } } }
console.log(`after scrambling every living animal's learned weights: ${kids} clone births by those animals; brain genes differing from the parent's genome before mutation: ${diff}; copied from its scrambled learned weights: ${leak}`);
