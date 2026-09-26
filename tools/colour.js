#!/usr/bin/env node
// Does colour mean anything? Probes of a run.js --dump, split at diet 0.3.
//   node tools/colour.js dump.json [...]
// prey armour R2 / weapon R2: how much of the prey's armour (weapon) their colour tags
//   predict (least squares on the three tags). Lineages differ in both, so this is
//   not zero without signalling (in v1-AQ-tags0, where the colour senses read 0, R2 ran 0.00-0.74).
// hunters' colour effect: for each hunter and each of up to 60 prey, the strike urge on
//   contact with that prey, minus the same with the colour senses (animalR/G/B) read 0.
//   |effect| is the mean size; r(armour) is the correlation, over prey, of the mean effect
//   with the prey's armour: negative = hunters hold back from the colours armoured prey wear.
const fs = require('fs'), vm = require('vm'), path = require('path');
const html = fs.readFileSync(path.join(__dirname, '..', 'evosim.html'), 'utf8');
const ctx = { module: { exports: {} }, console, Math }; vm.createContext(ctx);
vm.runInContext(html.match(/<script id="engine">([\s\S]*?)<\/script>/)[1], ctx);
const Sim = ctx.module.exports, NI = Sim.NI, NH = Sim.NH, NO = Sim.NO;
const IN = n => Sim.INPUT_NAMES.indexOf(n), sig = x => 1/(1+Math.exp(-x));
const B = n => Sim.BODY.findIndex(b => b[0] === n);
const TAG = B('tagR'), ARM = B('armour'), WPN = B('weapon'), SIZE = B('size'), DIET = B('diet');
function run(G, inp){
  const H = []; for (let h = 0; h < NH; h++){ let s = 0; for (let k = 0; k < NI; k++) s += G[Sim.W1+h*NI+k]*inp[k]; H.push(Math.tanh(s)); }
  let t = 0; for (let h = 0; h < NH; h++) t += G[Sim.W2+4*NH+h]*H[h];
  for (let k = 0; k < NI; k++) t += G[Sim.WD+4*NI+k]*inp[k];
  return t;   // the attack output
}
function r2(X, y){   // least squares with intercept, R^2
  const n = y.length, p = X[0].length + 1, A = [], b = new Array(p).fill(0);
  for (let i = 0; i < p; i++) A.push(new Array(p).fill(0));
  for (let r = 0; r < n; r++){ const x = [1, ...X[r]];
    for (let i = 0; i < p; i++){ b[i] += x[i]*y[r]; for (let j = 0; j < p; j++) A[i][j] += x[i]*x[j]; } }
  for (let i = 0; i < p; i++) A[i][i] += 1e-9;
  for (let i = 0; i < p; i++){ let m = i; for (let k = i+1; k < p; k++) if (Math.abs(A[k][i]) > Math.abs(A[m][i])) m = k;
    [A[i], A[m]] = [A[m], A[i]]; [b[i], b[m]] = [b[m], b[i]];
    for (let k = i+1; k < p; k++){ const f = A[k][i]/A[i][i]; for (let j = i; j < p; j++) A[k][j] -= f*A[i][j]; b[k] -= f*b[i]; } }
  const w = new Array(p).fill(0);
  for (let i = p-1; i >= 0; i--){ let s = b[i]; for (let j = i+1; j < p; j++) s -= A[i][j]*w[j]; w[i] = s/A[i][i]; }
  const my = y.reduce((a, v) => a + v, 0)/n; let ss = 0, se = 0;
  for (let r = 0; r < n; r++){ const x = [1, ...X[r]]; const f = x.reduce((a, v, i) => a + v*w[i], 0); se += (y[r]-f)**2; ss += (y[r]-my)**2; }
  return ss > 0 ? 1 - se/ss : 0;
}
function corr(a, b){ const n = a.length, ma = a.reduce((s, v) => s + v, 0)/n, mb = b.reduce((s, v) => s + v, 0)/n;
  let c = 0, va = 0, vb = 0; for (let i = 0; i < n; i++){ c += (a[i]-ma)*(b[i]-mb); va += (a[i]-ma)**2; vb += (b[i]-mb)**2; }
  return va > 0 && vb > 0 ? c/Math.sqrt(va*vb) : 0; }
for (const f of process.argv.slice(2)){
  const d = JSON.parse(fs.readFileSync(f));
  if (d.NG !== Sim.NG) d.genomes = d.genomes.map(g => Array.from(Sim.remapGenome(g, d.NI || 22, d.NO || 5)));
  const prey = d.genomes.filter(g => g[DIET] < 0.3), hunt = d.genomes.filter(g => g[DIET] >= 0.3);
  const name = f.split('/').slice(-2).join('/');
  if (prey.length < 10){ console.log(`${name}  too few prey`); continue; }
  const X = prey.map(g => [g[TAG], g[TAG+1], g[TAG+2]]);
  let line = `${name}  prey ${prey.length} armour R2 ${r2(X, prey.map(g => g[ARM])).toFixed(2)} weapon R2 ${r2(X, prey.map(g => g[WPN])).toFixed(2)}`;
  if (hunt.length >= 5){
    const P = prey.slice(0, 60), eff = new Array(P.length).fill(0); let abs = 0;
    for (const H of hunt) P.forEach((q, k) => {
      const a = new Array(NI).fill(0);
      a[IN('bias')] = 1; a[IN('energy')] = 0.5; a[IN('health')] = 1; a[IN('animal')] = 1; a[IN('animalNear')] = 1; a[IN('animalInReach')] = 1;
      a[IN('animalSize')] = Math.max(-3, Math.min(3, Math.log2(q[SIZE]/H[SIZE])))/3;
      let td = 0; for (let t = 0; t < 3; t++) td += (H[TAG+t] - q[TAG+t])**2;
      a[IN('animalKin')] = 1 - Math.sqrt(td/3); a[IN('animalWeapon')] = q[WPN]/1.5;
      const off = sig(run(H, a));
      a[IN('animalR')] = q[TAG]; a[IN('animalG')] = q[TAG+1]; a[IN('animalB')] = q[TAG+2];
      const e = sig(run(H, a)) - off; eff[k] += e/hunt.length; abs += Math.abs(e)/(hunt.length*P.length);
    });
    line += `  hunters ${hunt.length} colour effect |${abs.toFixed(3)}| r(armour) ${corr(eff, P.map(q => q[ARM])).toFixed(2)}`;
  }
  console.log(line);
}
