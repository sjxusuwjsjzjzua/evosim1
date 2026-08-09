# evosim — working rules

Single-file HTML evolution simulator. Two kingdoms, plants and animals, both
with a genome of continuous traits inherited with mutation. **Nothing about
behaviour is hardcoded** — herbivory, carnivory, herding, speciation, arms
races all have to emerge from the genes and the physics.

**The mission test: if a result had to be written into the code, it doesn't
count.**

Read `HANDOFF.md` before doing anything. Rationale for every decision is in
`LEDGER.md`, indexed by `[Lnn]` tags that appear in the source.

## Files

| file | what it is |
|---|---|
| `evosim-v0_48_0.html` | the build. Single file, no build step, runs on a phone. Bump the filename every version — delete the superseded one once its results are captured in `LEDGER.md`. |
| `LEDGER.md` | rationale + the version log with predictions and outcomes. |
| `HANDOFF.md` | current state, diagnostic frameworks, prioritized work. |
| `analyze.py` | log digest. `python3 analyze.py log1.json [log2.json log3.json]` |
| `check.js` | correctness harness. `node check.js <build.html>` |
| `headless.js` | runs a build outside the browser. `node headless.js --build <html> --seed <n> --days <n> --out <path> [--cfg patch.json] [--progress-days 20] [--max-wall-min <n>]` — see the Automated iteration section below. Writes `<out>.progress.json` while it runs; touch `<out>.stop` to end it early with a still-valid, still-complete log; `--max-wall-min` does the same automatically at a wall-clock budget, so a run that hits it still returns partial results instead of nothing. |
| `experiment.js` | runs N seeds through `headless.js` and feeds them to `analyze.py` in one shot. `node experiment.js --build <html> --days <n> --label <name> [--cfg patch.json] [--n 3]` |
| `.github/workflows/experiment.yml` | same thing on GitHub-hosted runners instead of the session sandbox — one seed per runner (real parallelism), free, doesn't need a session open. Trigger via the Actions tab or `actions_run_trigger`. Results land two ways: as a downloadable artifact, and pushed to a per-seed scratch branch `runs/<label>/seed-<seed>` (fetchable with plain `git` — artifacts sit on blob storage this sandbox's egress policy blocks, so the branch is the reliable path for Claude). |

## Hard rules

1. **Compute is not the constraint; unattributed conclusions are.** CPU time
   (this sandbox, or GitHub Actions) costs no tokens and no attention, so run
   things freely — but every run that tests a biology hypothesis still needs a
   written, falsifiable prediction on record before it starts, same as when a
   run meant carrying a build to a phone. Free compute makes "run it, look,
   tweak, run it again" *easier* to fall into, not a reason to allow it.
   Exception: a pure profiling pass (clocking CPU time to find an
   inefficiency, no ecological claim) needs neither a prediction nor per-run
   approval — it's a stopwatch, not an experiment. The Automated iteration
   section below governs who approves a run firing; it never waives the
   prediction itself.

2. **Run `node check.js <build>` after every edit.** A syntax check is not a
   correctness check and a call check is not an identifier check.

3. **One structural change per version, with a written prediction** — falsifiable,
   named genes, named thresholds, across 3 seeds. Then add a row to `LEDGER.md`.
   A missed prediction means the diagnosis was wrong, not that the constant
   needs to be bigger.

4. **Rationale lives in `LEDGER.md`, not in the source.** The source carries a
   one-line summary and a `[Lnn]` tag. At v0.36 comments were 24% of the file,
   paid on every read and every write, and parts had gone stale and were
   contradicting each other.

5. **Never calibrate a constant against a statistic from a broken or superseded
   run.**

6. **Constant changes ship as a CFG patch, not a new HTML.** ~700 tokens:
   `{"kind":"evosim-cfg","formatVersion":36,"version":"<build>","base":"<build>",
   "note":"<diagnosis>","cfg":{...}}`. Loading a file with `cfg` and no terrain
   arrays assigns the constants and rebuilds from seed. Always put the diagnosis
   in `note` so the patch is self-documenting when it comes back inside a log.
   A new HTML is only for a change of *shape*: a formula, a cost curve, a
   mechanism.

7. **Verify a measurement-only change did not alter the RNG draw sequence.**

8. **DO NOT widen a gene bound to fix a pin.** Tried in v0.43, reverted in
   v0.44. A rail moves; it does not go away.

9. **The shipped build stays single-file, no build step, no dependencies,
   touch-first** — the owner can still run it by hand on a phone any time, and
   nothing about `headless.js` changes that file. Headless execution reads the
   HTML as data (extracts the `<script>`, runs it in a Node `vm` context) and
   never forks or rewrites it. If a change ever makes the build unable to run
   standalone in a browser again, that change is wrong regardless of what the
   headless tool reports.

## Before touching a constant

Read `HANDOFF.md` §2 — the pin taxonomy (`p<2` / `p=2` / `p>2`) and pivot
discipline. They are the two things that made the difference in the last chat
and they answer most "why is this gene railed" questions without a run.

## Automated iteration: Tier A / Tier B

(Not "rule 7" — this is the workflow the hard rules above operate inside, not
another rule in the numbered list. Referenced elsewhere as "the Tier A/B
section" or "CLAUDE.md's Automated iteration section", never "§7", to avoid
colliding with hard rule 7 above.)

Two tiers. The difference is whether a run can fire without the owner
watching, not whether it needs a prediction — every run needs one either way.

**Tier A — diagnostic, auto-chains, no per-run wait.** A run belongs here only
if it executes a prediction *already on record*, originating nothing new:
extra seeds filling out an approved 3-seed protocol, an isolation arm the last
analysis already called for (the k_confusion:0 arm is the template), a
replication of a result that looked too clean on n=1. These can run back to
back — start the next one the moment the last digest is read — without asking
first each time.

**Tier B — gated, needs the owner's word before it runs.** Anything that
originates a new hypothesis: a new CFG constant nobody has proposed before, and
*always* any change to the shipped HTML itself (a new formula, cost
curve, mechanism — rule 6's definition of a *shape* change). These stop and
wait for approval before the run that tests them starts, same as always.

One iteration, done by Claude, looks like:

1. Propose the change with a written, falsifiable prediction across 3 seeds
   (rule 1/3). If it's Tier B, get the owner's go-ahead before step 2.
2. Run it — whichever is fastest and least contended:
   - `node experiment.js --build <html> --days <n> --cfg <patch.json>
     --label <name>` locally (competes with this session's own CPU), or
   - the `evosim experiment` GitHub Actions workflow (Files table above) for
     real per-seed parallelism that costs no sandbox CPU or tokens while it
     runs — preferred for anything long or multi-seed.
   Either way: writes `runs/<name>/seed-*.json` (local) or per-seed artifacts
   (Actions), plus a digest. A run that's taking too long can be stopped
   gracefully via `<out>.stop` — it still finishes through the normal
   logGenes()+JSON path, just short; check `<out>.progress.json` instead of
   guessing.
3. Read the digest, not the raw logs. Score the prediction (hit / miss /
   can't-tell) using `HANDOFF.md` §4's order, stopping early if the
   stationarity gate fails.
4. Add the row to `LEDGER.md`. Promote the specific logs that row is based on
   into the repo root (same convention as the phone-run logs) — `runs/` itself
   is gitignored, it's scratch space, individual runs are cheap to regenerate
   from a seed since the sim is fully deterministic per seed.
5. Report back: the scorecard, plus **one paragraph in plain language on what
   happened in that world this iteration** — not a table, an actual account of
   what the population did and why it matters. Tier A: fold this into a batch
   update and keep going to the next queued diagnostic run without waiting.
   Tier B, or whenever the diagnostic queue is empty and the next step would
   originate something new: propose the next change with its own prediction,
   then **stop and wait**. A code change never ships past this point without
   the owner's word, regardless of tier.

What auto-chains is executing an already-approved plan faster — never
deciding what the plan is.
