// What calls mean, from brain probes of a dump (run.js --dump), split at diet 0.3.
//   node tools/voice.js dump.json [...]
// Synthetic senses: a grazer on plants, nothing else in view. Then:
//   alarm   loudness with a big armed stranger close by, minus alone
//   food    loudness on a corpse in reach, minus alone
//   bolt    throttle when a loud call is heard, minus when nothing is heard
//   away    turn with the call on the right minus on the left (negative: turns away)
// Uses the engine from evosim.html, so the dump must match its senses and outputs.
const fs = require('fs'), vm = require('vm'), path = require('path');
const src = fs.readFileSync(path.join(__dirname, '..', 'evosim.html'), 'utf8').match(/<script id="engine">([\s\S]*?)<\/script>/)[1];
const ctx = {module: {exports: {}}, console}; vm.createContext(ctx); vm.runInContext(src, ctx); const Sim = ctx.module.exports;
const {NI, NH, NO, W1, W2, WD, INPUT_NAMES, OUTPUT_NAMES} = Sim, ix = n => INPUT_NAMES.indexOf(n), CALL = OUTPUT_NAMES.indexOf('call');
function brain(g, IN){
  const H = []; for (let h = 0; h < NH; h++){ let s = 0; for (let k = 0; k < NI; k++) s += g[W1+h*NI+k]*IN[k]; H.push(Math.tanh(s)); }
  const out = []; for (let q = 0; q < NO; q++){ let t = 0; for (let h = 0; h < NH; h++) t += g[W2+q*NH+h]*H[h]; for (let k = 0; k < NI; k++) t += g[WD+q*NI+k]*IN[k]; out.push(t); }
  return out;
}
const sig = x => 1/(1 + Math.exp(-x));
function base(){
  const IN = new Array(NI).fill(0); IN[0] = 1; IN[ix('energy')] = 0.5; IN[ix('health')] = 1;
  for (const n of ['plantL', 'plantC', 'plantR', 'plantHere']) IN[ix(n)] = 0.3;
  IN[ix('tasteHere')] = 0.2; return IN;
}
function stranger(IN){ IN[ix('animal')] = 1; IN[ix('animalNear')] = 0.8; IN[ix('animalSize')] = 0.6; IN[ix('animalWeapon')] = 0.5; IN[ix('animalKin')] = 0.2; IN[ix('crowd')] = 0.1; return IN; }
for (const f of process.argv.slice(2)){
  const d = JSON.parse(fs.readFileSync(f));
  if (d.NG !== Sim.NG){ console.log(path.basename(f), 'genome length', d.NG, 'does not match the engine', Sim.NG); continue; }
  for (const [name, grp] of [['grazers', d.genomes.filter(g => g[3] < 0.3)], ['meat guts', d.genomes.filter(g => g[3] >= 0.3)]]){
    if (!grp.length) continue;
    let quiet = 0, alarm = 0, food = 0, bolt = 0, away = 0;
    for (const g of grp){
      const q = sig(brain(g, base())[CALL]); quiet += q;
      alarm += sig(brain(g, stranger(base()))[CALL]) - q;
      const c = base(); c[ix('corpse')] = 1; c[ix('corpseNear')] = 0.9; c[ix('corpseInReach')] = 1; food += sig(brain(g, c)[CALL]) - q;
      const hr = base(); hr[ix('heard')] = 0.8; hr[ix('heardDir')] = 0.5;
      bolt += sig(brain(g, hr)[1]) - sig(brain(g, base())[1]);
      const hl = base(); hl[ix('heard')] = 0.8; hl[ix('heardDir')] = -0.5;
      away += Math.tanh(brain(g, hr)[0]) - Math.tanh(brain(g, hl)[0]);
    }
    const n = grp.length;
    console.log(path.basename(f).padEnd(24), name.padEnd(9), 'n', String(n).padStart(3), ' quiet', (quiet/n).toFixed(3),
      ' alarm', (alarm/n).toFixed(3), ' food', (food/n).toFixed(3), ' bolt', (bolt/n).toFixed(3), ' away', (away/n).toFixed(3));
  }
}
