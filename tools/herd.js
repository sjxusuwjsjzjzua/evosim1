// Do grazers steer toward others? Brain probes of a dump (run.js --dump), split at diet 0.3.
//   node tools/herd.js dump.json [...]
// Synthetic senses: a grazer on plants with company in view. Turn with the direction on the
// right minus on the left, so positive = turns toward it:
//   kin     toward the centre of look-alikes (kinDir)
//   crowd   toward the centre of everyone in view (crowdDir)
//   call    toward the loudest call (heardDir)
// Older dumps are remapped to the current senses (their new inputs read 0).
const fs = require('fs'), vm = require('vm'), path = require('path');
const src = fs.readFileSync(path.join(__dirname, '..', 'evosim.html'), 'utf8').match(/<script id="engine">([\s\S]*?)<\/script>/)[1];
const ctx = {module: {exports: {}}, console}; vm.createContext(ctx); vm.runInContext(src, ctx); const Sim = ctx.module.exports;
const {NI, NH, NO, W1, W2, WD, INPUT_NAMES} = Sim, ix = n => INPUT_NAMES.indexOf(n);
function brain(g, IN){
  const H = []; for (let h = 0; h < NH; h++){ let s = 0; for (let k = 0; k < NI; k++) s += g[W1+h*NI+k]*IN[k]; H.push(Math.tanh(s)); }
  let t = 0; for (let h = 0; h < NH; h++) t += g[W2+h]*H[h]; for (let k = 0; k < NI; k++) t += g[WD+k]*IN[k];
  return Math.tanh(t);   // turn
}
function base(){
  const IN = new Array(NI).fill(0); IN[0] = 1; IN[ix('energy')] = 0.5; IN[ix('health')] = 1;
  for (const n of ['plantL', 'plantC', 'plantR', 'plantHere']) IN[ix(n)] = 0.3;
  IN[ix('tasteHere')] = 0.2; IN[ix('crowd')] = 0.3; IN[ix('crowdSpeed')] = 0.2; return IN;
}
function toward(g, name, extra){
  const r = base(), l = base(); r[ix(name)] = 0.5; l[ix(name)] = -0.5;
  if (extra) for (const [k, v] of extra){ r[ix(k)] = v; l[ix(k)] = v; }
  return brain(g, r) - brain(g, l);
}
for (const f of process.argv.slice(2)){
  const d = JSON.parse(fs.readFileSync(f));
  const gs = d.NG === Sim.NG ? d.genomes : d.genomes.map(g => Array.from(Sim.remapGenome(g, d.NI || 22, d.NO || 5)));
  const grp = gs.filter(g => g[3] < 0.3); if (!grp.length) continue;
  let kin = 0, crowd = 0, call = 0;
  for (const g of grp){ kin += toward(g, 'kinDir'); crowd += toward(g, 'crowdDir'); call += toward(g, 'heardDir', [['heard', 0.8]]); }
  const n = grp.length;
  console.log(path.basename(f).padEnd(24), 'grazers', String(n).padStart(3), ' kin', (kin/n).toFixed(3), ' crowd', (crowd/n).toFixed(3), ' call', (call/n).toFixed(3));
}
