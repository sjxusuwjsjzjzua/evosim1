# evosim — external sanity check

**Reviewer scope:** I read `AUDITOR-BRIEFING.md` only. No repo, no git history, no
LEDGER.md, no raw logs. Everything below is conditional on the briefing being an
accurate self-report — verify before acting. Where the briefing is the only
evidence, I say so.

**Verdict:** The engineering discipline here is unusually good — better than most
human research codebases. The *statistics* are not, and that gap is where the
project is currently losing. Several months of careful process is being spent
generating conclusions that the sample sizes cannot support. Nothing below is
about working harder; most of it is about spending the same free compute
differently.

---

## Critical — fix before running another hypothesis

### 1. There is no noise floor. Everything downstream is uninterpretable.

Nowhere in the briefing is there a baseline measurement of seed-to-seed variance
for a **fixed build and fixed config**. Without that denominator, statements like
"3/4 vs 4/6" and "the predicted metric moved the predicted direction" are not
evidence of anything — there is no way to know whether the movement exceeds what
identical runs produce by chance.

This matters more here than in a typical experiment because v0.49 is documented as
*not RNG-exact* against v0.48. The project already knows its outcomes diverge
chaotically under order-sensitive changes. That is a statement that the noise
floor is large. It has never been measured.

**Do this first, before anything else:** current build, default config, 30+ seeds,
nothing varied. Report the full distribution — not the mean — of R0, death-age /
maturity ratio, time-to-extinction, and the pLocked trajectory. That is one fill
of the Actions budget and it converts every future claim from "moved in the
predicted direction" into "moved by X noise-floor SDs."

### 2. Dichotomising R0 destroys most of the data

"Fraction of seeds with R0 > 1" collapses a continuous variable to one bit. At
n = 4–8 that is close to statistically powerless.

Concretely, the current leading claim: **3/4 (5x) vs 4/6 (3x) is not evidence of a
difference.** Fisher's exact test on that table gives p ≈ 1.0. Exact
(Clopper–Pearson) 95% intervals are roughly **19–99%** and **22–96%** — they
overlap across nearly their entire range. Describing 5x as "the leading candidate"
over 3x is confidence running well ahead of evidence, and it is exactly the failure
mode §9.4 of the briefing warns about, occurring in §8 of the same briefing.

**Fix:** compare distributions of R0 (or log R0) across seeds — median and spread,
or a rank test. Keep "> 1" as a reporting convenience for humans; never use it as
the comparison statistic. This alone buys several-fold effective power at zero
compute cost.

### 3. The seeds-per-arm policy is backwards, and it is manufacturing false leads

CLAUDE.md's standing policy prefers "new hypotheses in preference to duplicate-seed
padding." That is the correct policy for a project with a low false-positive rate.
This project has documented **two** reversals caused by low n in a single session
(gutcost 2/8; the aSize0 hypothesis collapsing between n=2 and n=7). That is a high
reversal rate, and it means breadth is producing bad leads faster than they can be
retired.

There are ~24 CFG patch arms. At n ≈ 4 with a noisy binary outcome, several arms
would look like wins from chance alone. That is a garden-of-forking-paths problem,
and the single best result of the session (R0 1.51) is the maximum of a large noisy
set — it is *expected* to regress on retest. This is the winner's curse, not a
find.

**Fix, three parts:**
- Invert the policy: fewer arms, more seeds. Set a floor (n ≥ 20, ideally 30)
  before any arm may be described as "leading" or "promising" in LEDGER.
- No arm gets promoted without a **confirmation run on seeds not used in its
  discovery**. Held-out seeds, decided in advance.
- Retest the R0 1.51 result specifically. If it doesn't reproduce, that is
  itself a finding worth writing down.

### 4. Non-stationarity is bias, and more seeds will not fix it

The briefing concedes most 800–1200 day runs fail the stationarity gate. Comparing
arms on a transient risks measuring *which arm is further along its transient*
rather than which has the better equilibrium. Because this is bias rather than
variance, it does not shrink with n — running 100 non-stationary seeds gives a
very precise estimate of the wrong quantity.

**Fix:** for the two or three arms that actually matter, run long enough to pass
the gate, or demonstrate that the ranking is stable across time windows
(e.g. compare arms at day 400, 800, 1200 — if the ordering flips, the readings are
transient artefacts). Note the 6-hour hosted-runner job cap: if a run cannot reach
stationarity inside it, that is a design constraint to surface explicitly
(checkpoint/resume, or a faster build), not to work around silently.

### 5. The mission test has a soft spot in *how* `k_photoCost` is being chosen

The diagnosis is excellent — finding that `maxPlants` (an array-size artefact) was
binding regardless of predation is genuinely high-value work, and the arena-shrink
isolation test was the right control. Moving the equilibrium off an artefact onto a
physical parameter is the right *class* of fix.

The problem is the selection criterion. Sweeping `k_photoCost` across doses and
picking the value that produces the animal population you want is outcome-tuning in
a physics costume. The project's own standard — *if a result had to be written into
the code, it doesn't count* — applies to constants chosen by their downstream
ecological outcome just as much as to hardcoded behaviour. Every emergent result
downstream is then conditioned on a constant that was selected to produce it.

**Fix:** choose `k_photoCost` from a criterion **independent of animal outcomes**,
write that criterion into LEDGER *before* looking at animal R0, and then report
whatever ecology results — including "the animals go extinct at the principled
value." Candidate independent criteria: a target respiration-to-gross-photosynthesis
ratio; pre-fauna plant standing crop as a stated fraction of arena area; a stated
turnover time for the plant layer. Any of these is defensible. "The one where the
animals survived" is not.

### 6. The `maxPlants` discovery invalidates an unknown amount of LEDGER, and only one retest was scheduled

If plants sat at a slot cap regardless of predation, then *every* conclusion drawn
under that regime is confounded — not just `k_confusion`. That plausibly reaches
back to the v0.40 `k_photoCost` result, the v0.39 omnivory milestone, and parts of
the pin taxonomy in HANDOFF §2. Retesting confounded conclusions ad hoc, as they
happen to come up, leaves the rest of them sitting in LEDGER reading as settled.

**Fix:** a systematic invalidation pass **before** new experiments. Every LEDGER
conclusion gets tagged `CLEAN` / `CONFOUNDED` / `UNKNOWN` with respect to the
food-base artefact. This is a few hours of reading that protects every future
session from building on sand.

---

## Structural — process and infrastructure

### 7. LEDGER's format is the wrong shape for a project with documented reversals

A 107KB chronological narrative with corrections woven in is precisely the format
where a future reader — or future you, skimming under context pressure — re-adopts
an early optimistic claim and misses the later walk-back. This project has
documented that exact pattern happening twice already. The format is loaded against
you.

**Fix:** split the record.
- `LEDGER.md` stays the append-only chronology. Archival. Consulted, not read.
- `FINDINGS.md` is new: current believed-true claims only, one line each, with
  `n`, effect size, date last tested, confidence. A walked-back claim is **edited
  or deleted here**, not merely corrected 40KB later.

Sessions read FINDINGS and boot in a fraction of the tokens. HANDOFF §0.5 is
already reaching for this — make it a real file with an enforced format.

### 8. The orchestration state is the least durable part of the system and it isn't in the repo

Heartbeats are session-internal, die with the session, and the hourly backstop
can't reach GitHub. So the component that knows what is currently in flight is the
component guaranteed to disappear. §6's own open worry — "are there results sitting
unprocessed right now?" — is unanswerable *by construction*.

**Fix:** commit an `INFLIGHT.json` manifest. One entry per fired experiment: label,
branch, seeds, cfg hash, the prediction text, fired-at, collected-at, status. Any
session, or Michael, reconciles fired-vs-collected with one diff instead of from
memory. This also makes the prediction-before-run rule externally auditable via
commit timestamps, which is what §9.2 wants to check anyway.

### 9. The Actions concurrency ceiling isn't mysterious, and the standing policy is self-harming

The briefing describes ~40–50 as an empirically discovered ceiling, found by firing
until jobs stuck. It is almost certainly just the documented per-plan cap:
<cite index="2-1">concurrent standard-runner jobs are capped at 20 on Free, 40 on Pro and 60 on Team</cite>, and <cite index="5-1">that cap applies per billing account, not per repository</cite>. An observed
ceiling near 40 means a Pro plan, not a discovery. Three consequences:

- **The digest starvation is self-inflicted.** A policy of "keep 40+ jobs in flight
  at all times" pins the account at its cap permanently, so the trailing digest job
  necessarily queues behind the simulations it is meant to summarise. Stop running
  digest on Actions at all — `analyze.py` is trivial compute and belongs on the
  local 4 cores. Failing that, reserve headroom (cap sims at ~35).
- **Account risk.** Sustained 24/7 saturation of a personal account's runner quota
  is a pattern that <cite index="4-1">community reports associate with queueing or automated abuse review that disables Actions until support clears it</cite>. This project's continuous
  heartbeat is exactly that pattern. Worth a deliberate decision rather than a
  drift into it.
- **Cost.** <cite index="2-1">Actions is unlimited on public repositories; private repos on the Free plan get 2,000 Linux minutes per month, with overage at $0.006 per Linux 2-core minute since the January 2026 rate cut</cite>. Confirm public vs
  private and report the current month's usage. At this job volume the difference
  is not small.
- Also worth knowing: <cite index="8-1">GitHub Support can raise job concurrency limits on request via a support ticket</cite> — cheaper than probing for the ceiling by trial.

### 10. No stopping rule, so the investigation cannot end

"Not yet decided: whether 3x or 5x becomes the promoted value" cannot be decided
from the data that exists (see #2). With free compute and no pre-committed decision
rule, an investigation like this runs forever and drifts into optimising R0 for its
own sake — which is precisely the risk flagged in §9.6, and which §8's contents
suggest already materialised: essentially the whole session is dose-response on one
constant against one scalar.

**Fix:** write the decision rule *before* the run, in LEDGER. For example: "run 3x
and 5x at n ≥ 30; promote the higher median R0 only if the gap exceeds 1 noise-floor
SD; otherwise promote 3x on parsimony." Same for keep-or-revert on v0.50. And
re-anchor the queue to the actual mission questions — omnivory magnitude, herding,
effective population size, behavioural monoculture. Population balance was the
prerequisite, not the goal.

---

## Technical — the v0.50 change specifically

### 11. `*(0.5 + g)` → `*g` is two changes, not one

Removing the floor also **lowers the gain**. If `meatAttraction` is bounded on
roughly [0, 1], mean ATTACK score drops by about a third as a side effect. That is
a magnitude change riding along with the structural change, and it violates
one-structural-change-per-version in spirit if not in letter.

It also *predicts the result you got*: "predicted metric moved the predicted
direction, but overall population fitness dropped" is exactly the signature of an
unintended gain reduction. The n=1 run may not be noise — it may be a real effect of
the confounded half of the change.

**Fix:** renormalise so mean ATTACK score is preserved and only the floor is
removed (e.g. `*(k·g)` with k chosen to match the old mean), then difference the two
variants to separate floor-removal from gain-reduction. Also confirm GRAZE and
SCAVENGE's attraction genes are on the same scale — "matching the unfloored
pattern" only makes them comparable if the genes are comparable.

### 12. Unfloored multiplicative gates can create absorbing states

With `*g`, once `g → 0` the behaviour becomes unreachable; if no attacks occur there
is no fitness signal on `meatAttraction`, and the gene drifts freely. That is a
one-way ratchet — a behaviour that can be permanently lost rather than selected
against.

This is worth taking seriously because it may already be the mechanism behind a
phenomenon this project has independently reported: herding never appearing
behaviourally despite the gene not being purged, and `socialAttraction` collapsing
to 0.006. If GRAZE/SCAVENGE share this structure, "no hardcoded behaviour" may be
quietly buying "behaviour that can be irreversibly lost," which is a different and
arguably worse failure of emergence.

An epsilon floor would be a hardcode and is off the table by the project's own
rules. A legitimate alternative is making the behaviour reachable through
exploration noise in action selection rather than through the gene's magnitude —
that keeps the *gene* unfloored while keeping the behaviour recoverable. Worth a
LEDGER entry either way; this connects directly to the `riskEwma` thread.

---

## Minor

- **Internal inconsistency in the briefing.** §2 says `main` was last synced at the
  v0.49.0 ship. §5 says nothing has been merged or PR'd to `main` yet. §5 grant #3
  authorises workflow pushes to `main`, and §6 says `workflow_dispatch` is in heavy
  use — which *requires* the workflow file on the default branch. These cannot all
  be strictly true. Small, but in a document whose entire purpose is accurate
  self-report, that kind of drift is the thing worth correcting.
- **Two builds coexisting** with v0.50 unverified is fine, but set the deletion
  criterion for v0.49 explicitly rather than leaving it as "once verified."

---

## Do not break these while fixing the above

Several practices here are better than standard research norms and should survive
any process change:

- **Prediction written before the run.** Rare and genuinely load-bearing.
- **Rationale in LEDGER, not in source comments** — and the fact that this rule was
  born from a documented failure (24%-comments, stale and self-contradictory).
- **"Never widen a gene's bound to fix a pin."** Sophisticated. That rule prevents a
  specific and seductive form of self-deception.
- **Determinism per seed**, so any result reproduces from (build, seed, cfg) alone.
  This is what makes the gitignored `runs/` directory safe rather than reckless.
- **The arena-shrink isolation test.** Correct control, easy to skip, not skipped.
- **Documented walk-backs.** An agent that reverses its own claims in writing, twice,
  is behaving well. The problem is the n that made the reversals necessary, not the
  reversing.
- **"No extinction is not the same as viable."** A real conceptual insight, correctly
  identified and correctly generalised.
- **Keeping the rigor rules while relaxing the permission gates.** That is the right
  discrimination, and the stated reasoning — that the self-deception failure mode
  gets *easier* when nobody is watching each change land — is correct.

---

## One note on the audit setup itself

The briefing is written by the audited party and supplies its own "suggested audit
angles." That is honest and useful, and the self-flagged weak spots are real. But it
also frames the audit: an auditor who works §9 top to bottom is auditing the map the
agent drew.

Note what §9 does *not* ask. It does not ask whether R0 is the right metric, whether
dichotomising it is valid, whether ~24 arms at n ≈ 4 constitutes a multiple-comparisons
problem, whether a noise floor exists, or whether the selection criterion for
`k_photoCost` satisfies the project's own mission test. Every one of those is a
larger problem than anything on the §9 list.

Recommendation for the auditing instance: generate your own question list from the
repo and the raw logs *before* opening §9, then read §9 and note the delta. The
delta is the finding.

---

## Suggested order of operations

1. Noise-floor run — 30 seeds, current build, default config. Nothing else until
   this lands.
2. Invalidation pass over LEDGER for the `maxPlants` confound. Tag everything.
3. Split `FINDINGS.md` out of `LEDGER.md`; commit `INFLIGHT.json`.
4. Move `analyze.py` digest off Actions to local; drop the standing in-flight target
   below the concurrency cap. Confirm public/private and current minutes.
5. Re-run 3x vs 5x at n ≥ 30, compared on the R0 *distribution*, with the decision
   rule written down first.
6. Re-do v0.50 as a properly isolated change (gain-preserved), and open a LEDGER
   entry on the absorbing-state question.
7. Only then return to the mission queue — omnivory magnitude, herding, Ne,
   behavioural monoculture.
