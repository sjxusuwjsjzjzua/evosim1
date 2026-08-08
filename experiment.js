#!/usr/bin/env node
'use strict';
/*
 * experiment.js — run headless.js across several seeds and digest the result.
 *
 * One command for the thing the project's protocol always wants: N seeds,
 * same build, same CFG, run to the same day count, dropped in one directory,
 * then fed to analyze.py's cross-seed table in one shot. Doesn't decide
 * anything or loop on its own — it's the mechanical half of an iteration,
 * not the judgment half.
 *
 * Usage:
 *   node experiment.js --build evosim-v0_47_0.html --days 1200 --label my-run \
 *        [--cfg patch.json] [--seeds 1337,2222,3333] [--base-seed 1000] [--n 3] \
 *        [--no-autohalt]
 *
 * Writes runs/<label>/seed-<seed>.json for each seed, runs/<label>/digest.txt
 * with the analyze.py output, and prints the digest to stdout.
 */
const fs = require('fs');
const path = require('path');
const { spawnSync } = require('child_process');

function parseArgs(argv) {
  const out = {};
  for (let i = 0; i < argv.length; i++) {
    const a = argv[i];
    if (a.startsWith('--')) {
      const key = a.slice(2);
      const next = argv[i + 1];
      if (next === undefined || next.startsWith('--')) out[key] = true;
      else { out[key] = next; i++; }
    }
  }
  return out;
}

function main() {
  const args = parseArgs(process.argv.slice(2));
  const build = args.build || 'evosim-v0_47_0.html';
  const days = args.days;
  if (!days) { console.error('need --days'); process.exit(1); }
  const label = args.label || `run-${Date.now()}`;
  const seeds = args.seeds
    ? String(args.seeds).split(',').map(Number)
    : Array.from({ length: Number(args.n || 3) },
        (_, i) => Number(args['base-seed'] || 1000) + i * 137);

  const outDir = path.join('runs', label);
  fs.mkdirSync(outDir, { recursive: true });

  const logPaths = [];
  for (const seed of seeds) {
    const outPath = path.join(outDir, `seed-${seed}.json`);
    const hArgs = ['headless.js', '--build', build, '--seed', String(seed),
                    '--days', String(days), '--out', outPath];
    if (args.cfg) hArgs.push('--cfg', args.cfg);
    if (args['no-autohalt']) hArgs.push('--no-autohalt');
    console.error(`--- seed ${seed} ---`);
    const r = spawnSync('node', hArgs, { stdio: 'inherit' });
    if (r.status !== 0) {
      console.error(`seed ${seed} failed (exit ${r.status})`);
      process.exit(r.status || 1);
    }
    logPaths.push(outPath);
  }

  const manifest = {
    label, build, days, cfg: args.cfg || null, seeds,
    startedAt: new Date().toISOString(), logs: logPaths,
  };
  fs.writeFileSync(path.join(outDir, 'manifest.json'), JSON.stringify(manifest, null, 2));

  console.error(`\n--- analyze.py ${logPaths.join(' ')} ---`);
  const a = spawnSync('python3', ['analyze.py', ...logPaths], { encoding: 'utf8' });
  const digest = (a.stdout || '') + (a.stderr || '');
  fs.writeFileSync(path.join(outDir, 'digest.txt'), digest);
  process.stdout.write(digest);
  if (a.status !== 0) {
    console.error(`\nanalyze.py exited ${a.status} — digest may be incomplete, see above`);
    process.exit(a.status);
  }
}

main();
