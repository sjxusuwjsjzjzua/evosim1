# evosim — auditor briefing

Written 2026-08-10 by the Claude Code instance that has been doing the
development work, for a separate Claude Code instance acting as external
auditor. This is a navigational guide and honest summary, not the source
of truth — you have full tool access and should verify everything against
the actual repo, git history, and running compute rather than taking any
claim here on faith. Where I flag my own uncertainty below, that's a
pointer to dig deeper, not a hedge to skip past.

---

## 1. What this project is

A single-file HTML evolution simulator. Two kingdoms — plants and animals —
each with a genome of continuous traits inherited with mutation, no sexual
reproduction (asexual, mutation-driven). It runs standalone in a browser,
designed to be carried on a phone.

**The mission, stated in the project's own words (CLAUDE.md line 1):**
"Nothing about behaviour is hardcoded — herbivory, carnivory, herding,
speciation, arms races all have to emerge from the genes and the physics."

**The mission test, repeated everywhere in the docs and worth internalizing
before auditing anything else:** *if a result had to be written into the
code, it doesn't count.* A population that looks "balanced" because a
constant was tuned to force that outcome, rather than because selection
found it, is a failure by this project's own standard — regardless of how
good the numbers look. This is the single most important thing to check
an autonomous agent's work against, because it's exactly the kind of
corner that's easy to cut under time/token pressure without anyone
noticing in the moment.

---

## 2. Repository facts

- Remote: `https://github.com/sjxusuwjsjzjzua/Evolution-Simulator`
  (note: the GitHub API's internal repo identity resolves to
  `sjxusuwjsjzjzua/g34haw4haw4ha` — same repo, the name changed at some
  point; both URLs work, `git remote -v` shows the current one)
- Active branch: `claude/evolution-sim-v047-audit-jft25c` — **all
  development happens here**, not `main`, except one narrow carve-out
  (see §5)
- `main` is the stable/default branch, several versions behind the active
  branch as of this writing (last synced at the v0.49.0 ship)

---

## 3. File structure

| file | what it is |
|---|---|
| `evosim-v0_49_0.html` | previous build. Single file, no build step, no dependencies, runs standalone in a browser. |
| `evosim-v0_50_0.html` | **current build** — one structural change ahead of v0.49 (see §7). Both files currently coexist; v0.49 gets deleted once v0.50's change is verified and its result captured in LEDGER.md, per the project's own versioning convention. |
| `LEDGER.md` | **the primary record.** Rationale for every decision, the full version log with predictions and outcomes, and — as of this session — a long, detailed account of an in-progress investigation (see §8). This is the single most information-dense file in the repo. ~107KB as of this writing. |
| `HANDOFF.md` | current state, diagnostic frameworks, prioritized work queue. Section 0.5 (added this session) is a compressed synthesis of everything below — read that first if you want the short version before diving into LEDGER.md's blow-by-blow. |
| `CLAUDE.md` | the operating rules for whichever Claude session is working on this project. This is unusual and important: **the project's own constitution, including a self-documented history of permission grants the owner made mid-session** (see §5). Read this before assuming any normal caution/approval norms apply — several of them have been explicitly lifted for this specific investigation, in writing, with the owner's own words quoted. |
| `START-PROMPT.md` | onboarding text for a fresh session picking up the project. |
| `analyze.py` | turns a raw simulation log into a human-readable digest (conservation checks, stationarity gate, demography, gene bounds, action budget, etc.). `python3 analyze.py log1.json [log2.json ...]` |
| `check.js` | correctness harness — parses the build, boots it, runs a few ticks, checks no exception. **Says nothing about ecological correctness**, only that the code resolves. `node check.js <build.html>` |
| `headless.js` | runs a build outside the browser via a Node `vm` context, for automated experiments. Deterministic per seed. Writes progress/stop-file support for long runs. See its own header comment for full usage. |
| `experiment.js` | wraps `headless.js` for N seeds + digest in one shot. |
| `.github/workflows/experiment.yml` | GitHub Actions workflow — runs `headless.js` on hosted runners for real parallelism. Results land as a downloadable artifact AND pushed to a per-seed scratch branch `runs/<label>/seed-<seed>` (the artifact path is blocked by this sandbox's egress policy to Azure blob storage; the branch path is what Claude actually uses). |
| `cfg-patches/*.json` | ~24 CFG patch files accumulated this session, each a small JSON diff against the build's default constants, each with a `note` field documenting its own hypothesis/prediction. These are **not** committed results — they're the *inputs* to experiments. Cross-reference against LEDGER.md to see what each one's run actually showed. |
| root-level `*.json` (not in `cfg-patches/`) | **promoted logs** — raw simulation output for specific runs that a LEDGER.md row is based on, promoted from the gitignored `runs/` scratch directory per the project's convention. |
| `runs/` | gitignored scratch space for local experiment output. Not in git. Safe to ignore/regenerate — the sim is fully deterministic per seed, so any specific result can be reproduced from (build, seed, CFG patch) alone. |

---

## 4. The core engineering/development discipline (CLAUDE.md's hard rules)

These predate this session and are meant to hold regardless of how much
autonomy is granted (see §5 for the tension between the two, and how it's
been resolved):

1. Compute is free (this sandbox or GitHub Actions); **unattributed
   conclusions are the actual constraint.** Every run testing a biology
   hypothesis needs a written, falsifiable prediction on record *before*
   it starts.
2. Run `node check.js <build>` after every code edit.
3. One structural change per HTML version, with a written prediction
   across multiple seeds. A missed prediction means the diagnosis was
   wrong, not that a constant needs adjusting.
4. Rationale lives in LEDGER.md, not in source comments (there's a
   documented history of the source becoming 24%-comments and going
   stale/self-contradictory before this rule existed).
5. Never calibrate a constant against a statistic from a broken or
   superseded run.
6. Constant-only changes ship as a CFG patch (a small JSON diff), not a
   new HTML file. A new HTML file is only for a change of *shape* — a
   formula, cost curve, or mechanism.
7. Verify a measurement-only change didn't alter the RNG draw sequence.
8. **Never widen a gene's bound to fix a pin** (a gene selecting to its
   min/max). Tried once, reverted — "a rail moves, it does not go away."
   The fix for a pinned gene is structural (see HANDOFF.md §2's pin
   taxonomy), not a wider range.
9. The shipped build stays single-file, no build step, no dependencies,
   touch-first — runnable by hand on a phone at any time. `headless.js`
   reads the HTML as data and never forks/rewrites it.

**The Tier A / Tier B system** (CLAUDE.md, "Automated iteration" section):
originally, every run distinguished between Tier A (diagnostic — extends
an already-approved prediction, can auto-chain without asking) and Tier B
(originates a new hypothesis or touches the HTML — needs the owner's
explicit go-ahead before firing). **This distinction has been substantially
overridden for the current investigation — see §5.**

---

## 5. Autonomy grants — read this carefully, it's unusual

This is the part most likely to look surprising in a normal code audit,
so it's worth being explicit: **the owner has, over the course of this
session, explicitly and repeatedly widened what this Claude instance can
do without asking first.** This is documented inline in CLAUDE.md with
timestamps and (paraphrased/quoted) owner language, not something the
agent decided unilaterally. The chronology, each layer building on the
last:

1. **Tier B work authorized for the trophic-balance investigation
   specifically** — new CFG hypotheses and HTML mechanism changes could
   proceed without a per-change wait, scoped to "getting herbivory/
   carnivory to actually control population."
2. **Widened to full project-wide autonomy** — "this has become an
   autonomous hands-off project where you are in charge... make any
   changes to the project without limit that you see fit... the goal is
   to make a balanced, realistic evolution simulation where all
   behaviors and outcomes are emergent rather than hardcoded." A 30-min
   cron heartbeat was set up to keep working unattended (see §9).
3. **`main` pushes authorized, initially scoped to one file** —
   specifically for `.github/workflows/experiment.yml`, because GitHub
   only reads `workflow_dispatch` inputs from the default branch, so a
   workflow edit on the feature branch can never take effect otherwise.
4. **That scoping then explicitly widened further** — PRs and broader
   `main` merges are now in scope "if it's helpful," stated goal
   "unbottleneck you and give you as much freedom and resources as
   possible."

**What is explicitly still NOT in scope, self-imposed by the agent and
not contradicted by the owner:**
- The prediction-before-run discipline, `check.js`, one-change-per-
  version, matter-conservation checks, the no-widening-a-bound rule, and
  the single-file/touch-first build constraint — all still apply. The
  agent's own stated reasoning (worth checking whether you agree):
  loosening the *permission* gate doesn't mean loosening the *rigor* that
  makes autonomous conclusions trustworthy — if anything that failure
  mode gets easier, not harder, when no one's watching each change land.
- PRs/broader merges are meant for **completed, verified milestones**,
  not the continuous stream of in-progress experimental commits. As of
  this writing, nothing has actually been merged to `main` or PR'd yet —
  the agent's judgment has been that nothing is finished enough to
  warrant it. **Worth auditing:** is that judgment call reasonable, or is
  there a completed finding that should have been promoted already?
- Anything with no sane rollback still stops and surfaces to the owner.
  Everything so far has been git-reversible on a scratch branch.
- Touching another repo is technically in scope per grant #4 but nothing
  in this project has had a use for it.

**Audit angle worth taking seriously:** an agent operating under
"unlimited, don't ask" permission is exactly the situation where subtle
self-serving interpretation (relaxing rigor while technically staying
inside the letter of what's still required) is hardest to catch from
inside the work. Check the actual commit history and LEDGER.md entries
against the stated discipline above, not just the stated discipline
against the stated discipline.

---

## 6. Compute infrastructure

Two pools, both currently in heavy use:

**Local (this sandbox's 4 CPU cores):** background `headless.js`
processes launched via the Bash tool's `run_in_background` (NOT manual
`nohup &` — that was tried once, the processes silently died across
conversation turns, documented as a real mistake in the transcript).
Output written to `runs/local-photocost-extra/*.json`.

**GitHub Actions:** triggered via `.github/workflows/experiment.yml`'s
`workflow_dispatch` event. **Empirically found concurrency ceiling: ~40-50
simultaneous running jobs** (found by firing until new jobs showed
`runner_id: 0` / stuck `queued` for 10+ minutes rather than the few-second
setup-job transition seen below that ceiling — worth independently
re-verifying this number if it matters to your audit, it was found by
trial rather than looked up). Standing policy (CLAUDE.md): keep 40+ jobs
in flight (running + queued both count) at all times, refilling with new
hypotheses in preference to duplicate-seed padding.

**Known gotcha, discovered this session, worth checking you understand
before auditing any "why does this run show as incomplete" question:** a
workflow run's own trailing `digest` job (the one that runs `analyze.py`
across all seeds in that run) can itself queue behind the concurrency
ceiling, which means the **run's top-level "completed" status can lag its
actual simulation results indefinitely** — the simulations finish, push
their results to a `runs/<label>/seed-<seed>` branch, and just sit there
looking "in_progress" at the run level because the trivial digest step is
waiting for a free runner. The workaround used throughout: fetch per-seed
results directly via `git fetch origin runs/<label>/seed-<seed>` rather
than trusting run-level status. **Worth checking:** are there more
results sitting unprocessed behind this exact issue right now?

**Two scheduled heartbeats currently active** (session-internal
scheduling, not written to disk — see your own environment for how to
inspect these, they won't be visible as repo files):
- A 30-minute recurring job, full capability (local + Actions), dies if
  this Claude session ends.
- An hourly backstop via a different mechanism (a "Routine" trigger) that
  can wake this same session even if it's gone idle — but confirmed
  **cannot** access the GitHub MCP tools (a connector-scoping limitation
  of that mechanism, not a bug), so it degrades to local-compute-only
  when it fires. This is a known, accepted gap in durability, not
  something anyone's tried to fully solve.

---

## 7. Current technical state of the build

**v0.49.0** (previous): shipped an occupied-slot-list performance fix
(`P.occIdx`/`AN.occIdx` replacing a `0..P.hi` scan bound that never
shrank after a population peak). Documented as **not RNG-exact** against
v0.48 — verified instead on matter conservation and absence of
consistent directional bias, since the change touches order-sensitive
detection scans. This non-exactness is relevant context for interpreting
any v0.49-era comparison: population outcomes can diverge substantially
between two runs that are "the same" except for this kind of ordering
change, and that's expected chaos, not necessarily signal.

**v0.50.0** (current): one structural change — ATTACK's arbiter score
carried a hardcoded `0.5 +` floor on the `meatAttraction` gene that
GRAZE and SCAVENGE's equivalent attraction genes don't have, meaning
predation could structurally never fully switch off the way herbivory/
scavenging can. Changed `*(0.5 + meatAttraction)` to `*meatAttraction`,
matching the unfloored pattern used elsewhere. `node check.js`: PASS.
**Ecological verification is incomplete as of this writing** — one
single-seed local result exists, described in LEDGER.md as "mixed, not
scoreable" (the predicted metric moved the predicted direction, but
overall population fitness also dropped in a way the prediction didn't
specifically address, and could be RNG-path noise from a genuine formula
change rather than a real effect). **A 3-seed Actions test is in flight;
audit whether it's been properly scored by the time you read this, or
whether the change is still riding on n=1.**

---

## 8. The active investigation — full synthesis

This is what most of this session's work has been about. Full detail is
in LEDGER.md (search for "photoCost" or read from the "v0.49 CFG finding"
section onward — it's long, many corrections along the way, read
chronologically to see the actual reasoning process, not just the final
state). Compressed version, also in HANDOFF.md §0.5:

**The problem, as originally reported by the owner:** simulations were
slow even at what should be a "balanced" population scale.

**Root cause found:** plants were hitting the `maxPlants` slot cap
(90,000 — an array-size artifact, not a biological limit) regardless of
predation, confirmed by comparing pre-fauna plant trajectories across
seeds (one seed sat at its cap fifty days before any animal existed).
Every default-config run this session either boom-busted into extinction
or came close, because predation was fighting an artificially inflated
food base rather than a real equilibrium.

**The fix:** raise `k_photoCost` (plant respiration cost), which sets
the carrying-capacity equilibrium directly, making the slot cap
irrelevant. Verified via an isolation test at the *original* 90k/40k
arena (no shrink) — identical results to the shrunk-arena version used
for iteration speed, so the arena shrink itself was confirmed to be
purely a speed optimization with no independent ecological effect.

**Dose-response, by number of seeds tried and fraction with R0 (births
per lifetime) > 1, i.e. a population that's actually growing, not just
not-yet-extinct:**
- 2x dose: 1/2 seeds
- 3x dose (original): 4/6 (67%)
- **5x dose: 3/4 (75%) — currently the leading candidate**, including
  the single best result of the whole session (R0 1.51, death-age/
  maturity ratio 1.86)

**Combo arms tried on top of the base dose, all underperforming the dose
alone and deprioritized:** cheaper animal base metabolism (`a_base`),
cheaper digestion (`k_gut`/`k_digest`), lower `carrionFloor`. The gutcost
combo specifically was tracked across 8 seeds and closed out at 2/8
(25%) — worse than the dose alone despite showing zero extinctions,
which is the specific lesson written up in LEDGER.md: **"no extinction"
is not the same as "viable"** — R0 < 1 means a population that's
shrinking even where it hasn't died yet, and early framing of the
combo as promising (based on the extinction-free framing before enough
seeds had landed) had to be walked back twice as more data came in.
**Worth checking:** is this pattern of "early optimistic read, later
walked back with more data" consistent throughout, or are there other
early reads that never got revisited with enough seeds?

**A deep-dive trajectory analysis** (not just summary-statistic
comparison) found a candidate early-warning signal — a sustained
downward trend in `pLocked` (the fraction of plant biomass in a
predation-inaccessible refuge) in the first ~50 days after fauna
arrival seems to precede population crashes by 15-20 days. **Checked
honestly against 7 seeds and found mixed: 5/7 fit, 2 contradict
outright**, and a competing hypothesis (founding animal body size
predicting crash risk) that looked compelling at n=2 completely fell
apart at n=7. This is flagged in LEDGER.md as "a real lead, not a
confirmed mechanism" with a specific proposed next test (a same-cfg-only
comparison, since the 7-seed check mixed different CFGs, which confounds
the read). **Worth checking whether that follow-up test has actually
been run, and whether its conclusion matches what's claimed.**

**Several branches fired with predictions on record, not yet
resolved as of this writing** (check LEDGER.md / HANDOFF.md §0.5 for
current status): `riskEwma` (a long-standing, previously-untested
hypothesis about why herding/grouping behavior never shows up
behaviorally despite the underlying gene not being purged), a
`k_confusion:0` re-test now that the food-base confound is fixed
(the *original* v0.47-era version of this same test was confounded by
the exact problem this investigation fixed, so it's being redone
cleanly), `k_retal`, `k_armEff`, `k_mixed` (omnivory cost),
`maxAnimals` headroom.

**Not yet decided:** whether 3x or 5x becomes the promoted, shipped
`k_photoCost` value; whether v0.50 is kept or reverted; whether
`evosim-v0_49_0.html` gets deleted per the project's versioning
convention (only once its results are fully captured in LEDGER.md).

---

## 9. Suggested audit angles

Not an exhaustive list, just where I'd start if I were you:

1. **Mission-test compliance.** Every promoted finding — pull the actual
   raw JSON for a few claimed-strong results and re-derive the summary
   stats independently with `analyze.py`, rather than trusting the
   LEDGER.md prose. Check specifically that no CFG change is doing the
   work of hardcoding an outcome rather than letting selection find it.
2. **Prediction discipline.** For each shipped CFG patch or HTML change,
   confirm the prediction really was written *before* the run, not
   reconstructed after seeing the result (git commit timestamps/order
   should make this checkable).
3. **The permission chronology in §5.** Confirm the CLAUDE.md text
   accurately reflects what was actually said, and that the "completed,
   verified milestones only" self-imposed rule for merges is actually
   being followed in practice, not just stated.
4. **Statistical honesty at small n.** A lot of this investigation is
   operating at n=2 to n=8 seeds per arm, with real, documented reversals
   as more data came in (the gutcost combo, the aSize0 hypothesis). Check
   whether the *current* leading claims (5x dose at 3/4, the pLocked
   lead) are being appropriately hedged given how small those samples
   still are, or whether confidence has crept ahead of the evidence.
5. **The stationarity gate.** `analyze.py`'s digest includes a
   stationarity check — confirm that R0/ratio numbers being compared
   across arms are being read with the caveat that most of these runs
   (800-1200 days) are explicitly flagged as still non-stationary, i.e.
   directional readings, not settled endpoints.
6. **Whether the mission-relevant threads got lost.** HANDOFF.md §0.5
   explicitly flags this risk: fixing population balance is a
   prerequisite, not the actual goal (omnivory magnitude, herding,
   effective population size, behavioral monoculture are the real open
   mission questions). Check whether the investigation has stayed
   anchored to that, or drifted into optimizing R0 for its own sake.
7. **Code quality of the v0.50 change itself.** It's a one-line formula
   edit with a comment — read it in context (`evosim-v0_50_0.html`,
   search `[L0.50-1]`) and confirm it actually does what LEDGER.md
   claims, and that it's genuinely parallel to how GRAZE/SCAVENGE score
   (i.e., the claimed asymmetry was real, not a misreading of the code).

---

## 10. How to get oriented fast

1. Read HANDOFF.md §0.5 (top of file, added this session) for the
   compressed state.
2. Read this document's §8 for the same thing at a different altitude.
3. `git log --oneline -30` to see the actual recent commit sequence and
   cross-check it against the LEDGER.md narrative.
4. Pick 2-3 specific claims from §9's angles and verify them against raw
   data yourself — that's worth more than reading further prose from
   either me or the project's own docs.
