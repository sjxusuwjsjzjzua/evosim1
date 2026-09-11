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
| `evosim-v0_56_0.html` | the build. Single file, no build step, runs on a phone. **v0.56 ships two structural changes together** — founder symmetry [L0.56-1] and a CFG-reachable genome [L0.56-2] — under amended rule 3, because the rotation is a 2x2 factorial that separates them. `evosim-v0_55_0.html` is kept as the revert target and as the reference for the founder-value comparison. **Deletion criterion:** delete `evosim-v0_55_0.html` once H11/H12 are scored at n>=60 per cell on the days 400-800 window and written into `LEDGER.md`, win or lose. v0.52/v0.53/v0.54 are deletable now — their results are captured and they are recoverable from git history. |
| `LEDGER.md` | rationale + the version log with predictions and outcomes. |
| `HANDOFF.md` | current state, diagnostic frameworks, prioritized work. |
| `tools/collect.sh`, `tools/arms.py`, `tools/score55.py` | collection, arm classification by cfg diff, and the weekly matched-window scorer. Committed rather than kept in scratch because `runs/` and the scratchpad do NOT survive a container restart — every log is recoverable from its `runs/<label>/seed-<N>` branch, and `tools/collect.sh` re-fetches the lot in minutes. |
| `.claude/skills/program-audit/` | harsh audit of the PROGRAM, not of claims. Run it when the project may be looping. `AUDIT-PROTOCOL.md` audits whether numbers are right and has only ever produced local corrections; this one asks whether the work is going anywhere, and returned PIVOT on 2026-09-11. |
| `analyze.py` | log digest. `python3 analyze.py log1.json [log2.json log3.json]` |
| `check.js` | correctness harness. `node check.js <build.html>` |
| `headless.js` | runs a build outside the browser. `node headless.js --build <html> --seed <n> --days <n> --out <path> [--cfg patch.json] [--progress-days 20] [--max-wall-min <n>]` — see the Automated iteration section below. Writes `<out>.progress.json` while it runs; touch `<out>.stop` to end it early with a still-valid, still-complete log; `--max-wall-min` does the same automatically at a wall-clock budget, so a run that hits it still returns partial results instead of nothing. |
| `experiment.js` | runs N seeds through `headless.js` and feeds them to `analyze.py` in one shot. `node experiment.js --build <html> --days <n> --label <name> [--cfg patch.json] [--n 3]` |
| `.github/workflows/experiment.yml` | same thing on GitHub-hosted runners instead of the session sandbox — one seed per runner (real parallelism), free, doesn't need a session open. Trigger via the Actions tab or `actions_run_trigger`. Results land two ways: as a downloadable artifact, and pushed to a per-seed scratch branch `runs/<label>/seed-<seed>` (fetchable with plain `git` — artifacts sit on blob storage this sandbox's egress policy blocks, so the branch is the reliable path for Claude). |

## The mission metric

**Heterotrophy fraction** = `eCarrion / (ePlant + eCarrion)` over a matched
window — the share of animal energy intake that came from animals. One number
for "do the trophic levels feed each other."

Measured 2026-09-11 across **1,502 survivors**: median **0.302%**, max 3.95%,
**0 runs above 5%**. Across five structural versions: pre-v0.53 0.285% → v0.53
0.323% → v0.54 CONTROL 0.267% → v0.55 CONTROL 0.211%. Flat. The only arm that
ever moved it is `meatValue` 40 (0.86–0.99%) — a constant, not selection.

**Report it every pass.** The project ran 34 days without a mission-level number
and could not tell it was looping; the owner noticed before any instrument did.

## Hard rules

1. **Compute is not the constraint; unattributed conclusions are.** Free CPU
   makes "run it, look, tweak, run it again" easier to fall into, not allowed.
   Every biology hypothesis needs a written falsifiable prediction on record
   before its runs start.
   **AMENDED 2026-09-11: the prediction unit is the QUESTION, not the run.** A
   screening batch that sweeps twenty untouched constants is **one** prediction
   ("none of these moves the mission metric by more than X"), not twenty. The
   old per-run reading is why 139 of 150 CFG constants had never been varied and
   2,341 runs covered 12 distinct configurations. Breadth was forbidden by a
   rule meant to forbid fishing.

2. **Run `node check.js <build>` after every edit.**

3. **One structural change per version — AMENDED 2026-09-11.** Multiple
   structural changes may ship in one version **when they are independently
   motivated and the arms are a factorial that separates them.** Attribution is
   what the rule protects, and a 2×2 with matched arms buys attribution that
   serialisation buys with a week of latency. One change per version plus weekly
   scoring capped learning at roughly one bit per week against unlimited compute;
   that cap, not the compute, was the bottleneck.
   A missed prediction still means the diagnosis was wrong, not that the
   constant needs to be bigger.

4. **Rationale lives in `LEDGER.md`, not in the source.**

5. **Never calibrate a constant against a statistic from a broken or superseded
   run.**

6. **Constant changes ship as a CFG patch, not a new HTML.** A new HTML is only
   for a change of *shape*.
   **Note 2026-09-11:** this rule silently excluded the genome. Founder gene
   values were not CFG-reachable, so the starting genome — which turned out to
   contain the monoculture — could not be tested by patch. `founderGenesA` /
   `founderGenesP` [L0.56-2] fix that.

7. **Verify a measurement-only change did not alter the RNG draw sequence** —
   and verify it on a run where the changed code path actually executes. A
   300-day identity check that stops at day 200 with `animalStartDay` 260 tests
   nothing and prints a pass.

7b. **Never compare a trailing-window statistic across runs of different
   length.** Match the window explicitly; normalise endpoint totals to rates.

8. **DO NOT widen a gene bound to fix a pin.**

9. **The shipped build stays single-file, no build step, no dependencies,
   touch-first.**

10. **NEW — a frozen threshold must be larger than the standard error of the
    statistic that gates it, at the planned n.** Compute the SE before freezing.
    H4's MISS line was 0.15 SD against a bootstrap SE of 0.222 SD at n=61; H10
    had 14% exact Fisher power against its own criterion at n=25. A meaningful
    share of the seven-MISS streak was power, not biology, and an underpowered
    pre-registration is worse than none — it launders noise as a finding.

11. **NEW — report the tail, not only the median.** "GRAZE has never fallen
    below 93%" was false: 126 of 1,075 qualifying runs are below it, minimum
    78.3%, and `runs/rot-collect/59400.json` contains a herd (APPROACH 3.95%),
    an arms race (`maxSpeed` 3.2× control) and 66% corpse consumption — inside
    an arm scored MISS on its median. Emergence is a minority state. An
    arm-median pipeline is built to miss exactly the thing this project exists
    to find.

12. **NEW — a large effect that missed its pre-registered variable is recorded
    as a NOTABLE UNPREDICTED EFFECT, not discarded.** `meat-rich` produced the
    largest effect the project has measured (survival 92.2% vs 66.7%,
    p=0.0022) and was filed as MISS because `carnivory` did not move. Freezing
    criteria stops self-deception and stays; it must not also throw away signal.
    A notable effect gets logged and earns a replication arm — it does **not**
    earn a post-hoc story.

## Neutral-gene drift yardstick — corrected 2026-09-11

Selection response is measured against genes the simulator never reads. The list
was **contaminated**: `ambushTendency` IS read (`evosim-v0_56_0.html:1769`, it
sets `hide` in the detection roll), which inflated the null and biased every
selection test toward MISS.

Verified-inert set: `territoriality`, `mateChoosiness`, `parentalCare`,
`pathogenResistance`. Re-verify by grep before each use; a gene that gains a
reader silently invalidates every past comparison.

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

**Tier B — normally gated, needs the owner's word before it runs.** Anything
that originates a new hypothesis: a new CFG constant nobody has proposed
before, and *always* any change to the shipped HTML itself (a new formula,
cost curve, mechanism — rule 6's definition of a *shape* change). These
normally stop and wait for approval before the run that tests them starts.

**Full autonomy grant, 2026-08-10:** the owner has taken this project fully
hands-off — a 30-minute cron heartbeat checks finished compute, analyzes it,
and Claude makes whatever changes (CFG or HTML mechanism) it judges will
move toward a balanced, realistic simulation with every behavior emergent,
without waiting for approval first. This supersedes the narrower
trophic-balance-only exception above: the *wait-for-approval* gate is lifted
project-wide, not just for one investigation. It does not lift anything
else — every run still needs a written falsifiable prediction on record
first (rule 1, never optional), an HTML mechanism change still bumps the
version and stays one structural change at a time (rule 3), `node check.js`
still runs after every edit (rule 2), matter-conservation/RNG-safety still
gets checked (rule 5/7), gene bounds still don't get widened to fix a pin
(rule 8), the shipped build still stays single-file/no-build-step/touch-
first (rule 9), and the mission test still applies harder than ever now
that nobody is watching each change land: **if a result had to be written
into the code, it doesn't count.** A fix that hits its population target by
hardcoding a cap or a rate rather than letting selection find it is not a
win, regardless of how clean the numbers look — that failure mode is easier
to fall into unsupervised, not harder. Compute discipline: keep all
available cores (local + Actions) running productive work continuously;
report tersely, no restating background each cycle.

**Standing saturation target, 2026-08-10:** keep Actions at **40+ jobs in
flight** (running + queued-behind-the-runner-ceiling both count — a queued
job still keeps the pipeline saturated, since it starts the instant a
runner frees up) at all times, not just in bursts.

**CORRECTED 2026-08-10: the real ceiling is 20 simultaneous *running*
jobs, not the 40-50 previously recorded here.** Measured directly —
20 running / 9 queued across four dispatched runs, exactly the documented
per-plan cap, which is what the external audit predicted. The old figure
came from counting *jobs in flight* (running + queued) and calling it the
ceiling. Above 20, new jobs queue rather than run, which is fine and
expected, not a problem to solve.

**Also measured, and it changes the sizing arithmetic:** a successful
800-day sim job takes median **0.51 h** (mean 0.80, p90 1.90); a 1600-day
job ~1.1 h. The repo is **public**, so Actions minutes are unlimited and
free — there is no quota to conserve, only the concurrency cap. To hold
~13 of 20 slots busy continuously the arrival rate needs to be ~12
jobs/hour, which is what `experiment.yml`'s standing `schedule:` now
fires. Sizing a standing batch without dividing service time by interval
is how it ended up at 5% utilisation on the first attempt. When the in-flight count drops below 40
(check cheaply — `list_workflow_jobs` with `filter: latest` on a couple of
recent runs, or count non-completed runs, never a full unfiltered dump),
refill it: extend an under-sampled arm with more seeds, or — preferred —
design a genuinely new, falsifiable hypothesis (rule 1 still applies to
every one of these, no exceptions for volume) and fire it. This is meant
to sustain wide-and-shallow exploration continuously, not to pad the
count with duplicate seeds on already-confirmed findings. Pair every
finding that survives triage with an actual shipped change (a promoted
CFG patch, or a version-bumped HTML edit like v0.50's ATTACK-floor fix) —
the goal is a steadily improving app, not an ever-growing pile of
unintegrated screening data.

**Reconciliation, 2026-08-10, external audit point 9:** the audit flagged
that sustained 24/7 saturation of a *personal* account's Actions quota
carries real account-safety risk (automated-abuse review), separately
from whether the compute itself is being used well. That risk is real and
the "40+ jobs, always" target above is read literally in tension with it.
Standing amendment: **40+ is a ceiling to reach when there's a genuine
queue of falsifiable, already-approved work to run, not a floor to
backfill for its own sake.** Concretely: don't invent volume just to hit
the number; when the account already has a large batch in flight (e.g.
the 2026-08-10 noise-floor batches, ~13 concurrent runs including two
15-seed matrices), that's a legitimate reason to hold off firing more
until it clears, not a gap to fill immediately. The digest-job removal
(same day, `experiment.yml`) already fixes the specific mechanical
problem (misleading "completed" status); this note fixes the policy
tension the audit also raised. Bursty-but-bounded, not always-max.

**Amendment, same day:** the owner additionally authorized direct pushes to
`main` specifically for `.github/workflows/experiment.yml` changes, since
GitHub only reads `workflow_dispatch` inputs from the default branch, so a
workflow edit on a feature branch can never actually take effect otherwise.

**Second amendment, same day — widened further.** The owner explicitly
lifted the workflow-file-only scoping above ("no touching main beyond that
one file, no PRs, no other repos" — "you can do this if it's helpful"),
stated goal: unbottleneck Claude, maximize freedom and resources for this
project. PRs and broader `main` merges are now in scope when judged
helpful; touching another repo is technically in scope too, though nothing
in this project currently has a use for it. **Claude's own operating rule,
stated back to the owner and not contradicted:** use this for genuinely
*completed, verified* milestones — a settled `k_photoCost` dose, a scored
v0.50 — not for the continuous stream of in-progress experimental commits,
which stay on `claude/evolution-sim-v047-audit-jft25c` until they resolve
into something real. Merging half-tested state into `main` would promote
unverified work as settled, a different mistake than the one the original
scoping guarded against. Still the one thing that stops and surfaces
regardless of any grant: anything with no sane rollback.

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
