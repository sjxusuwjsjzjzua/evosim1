# evosim — handoff

Read this first, then `CLAUDE.md` for the hard rules. Rationale for everything
is in `LEDGER.md`, indexed by the `[Lnn]` tags in the source.

---

## 0. What this project is

A single-file HTML evolution simulator. Two kingdoms, plants and animals, both
with a genome of continuous traits inherited with mutation. **Nothing about
behaviour is hardcoded** — herbivory, carnivory, herding, speciation, arms races
all have to emerge from the genes and the physics. The owner runs it on a phone.

**The mission test:** if a result had to be written into the code, it doesn't
count.

---

## 0.5. Trophic-balance investigation, 2026-08-10 — read this before §1

Owner asked for a hands-off, fully autonomous push toward "herbivory
controls plants, carnivory controls herbivores, balanced populations."
Full session synthesis (LEDGER.md has every individual run — this is the
compressed version):

**Root cause found and fixed:** plants were hitting the `maxPlants` slot
cap (90,000) purely as an artifact of array size, not biology — confirmed
by comparing pre-fauna plant trajectories across seeds (one seed sat at
its cap fifty days before any animal existed; another never came close).
Every default-config run this session either boom-busted into extinction
or came within a hair of it, entirely explained by predation fighting an
artificially inflated food base.

**The fix: raise `k_photoCost`** (plant respiration cost), which sets the
carrying-capacity equilibrium directly and makes the slot cap irrelevant.
Confirmed via an isolation test at the *original* 90k/40k arena (no
shrink) — identical results to the shrunk-arena version, so the arena
shrink used throughout was purely a speed optimization, not load-bearing.

**Dose-response tally (seeds with R0 > 1 = viable population):**

| dose | k_photoCost | seeds tried | R0 > 1 |
|---|---|---|---|
| 2x | 0.008 | 2 | 1/2 |
| 3x (original base) | 0.012 | 6 | 4/6 (67%) |
| **5x** | **0.020** | **4** | **3/4 (75%), leading candidate** |

**Combo arms tried on top of the base dose — all underperformed the dose
alone, none promoted:**
- gutcost (`k_gut`/`k_digest` cut): **2/8 (25%)** — closed out, worse than
  base dose despite zero extinctions (R0 stayed under 1 in 6 of 8).
- a_base (cheaper animal upkeep): 1/2 so far.
- carrionFloor alone: 0/2 so far.
Lesson: "no extinction" is not the same as "viable" — R0 < 1 means a
population that's shrinking even where it hasn't died yet. Score on R0,
not survival-to-cutoff.

**Real structural change shipped: v0.50.0.** ATTACK's arbiter score
carried a `0.5 +` floor on `meatAttraction` that GRAZE/SCAVENGE's
attraction genes don't have — predation could never fully switch off.
Unfloored to match. `node check.js` PASS. First single-seed ecological
result is mixed (actAttack dropped as predicted on an already-near-zero-
carnivory seed, but R0 also dropped, which wasn't part of the specific
prediction and may be RNG-path noise from a genuine formula change, same
caveat v0.49 carried). **Not scored yet — needs the 3-seed Actions test,
still in flight.**

**Still open, not yet acted on this session:** `riskEwma` (HANDOFF's
long-standing herding hypothesis), `k_confusion` re-test now that the
food base is fixed, `k_retal`, `k_armEff`, `k_mixed` (omnivory cost),
`maxAnimals` headroom — all fired, predictions on record, results not
yet landed as of this writing.

**Tooling finding worth knowing:** a workflow run's top-level "completed"
status can lag its actual simulation results indefinitely if the
trailing `digest` Actions job queues behind the concurrency ceiling
(discovered empirically — ~40-50 concurrent jobs is the real ceiling on
this account, not the 20 originally assumed). Fetch per-seed results
directly via `git fetch origin runs/<label>/seed-<seed>` rather than
trusting run-level status when checking for completions.

**Next step once the pending batches land:** if 5x continues to lead,
promote it (not 3x) as the shipped `k_photoCost` CFG patch and add the
version-log table row. `evosim-v0_49_0.html`/`v0_50_0.html` both still
present pending that decision and v0.50's own verification.

**Priority-ordered plan for the autonomous loop, so each heartbeat has
concrete direction instead of re-deriving strategy:**

1. **Land the pending batches** (5x dose confirmations, riskEwma/retal/
   armEff/confusion-off/animal-headroom/mixedfree, v0.50 3-seed test and
   its two combo re-tests). Digest each honestly, fold into LEDGER.
2. **Score v0.50's L0.50-1 prediction** once its 3-seed Actions test
   lands — this has been sitting unscored on n=1 too long.
3. **Run the clean same-cfg pLocked-trend test** (previous section) —
   8-10 base-dose-only seeds, record day-265 `pLocked` and its 50-day
   trend, check correlation with final R0. This answers whether the
   ~60-75% viability ceiling is fixable or is founder-luck stochasticity.
   Do this **before** inventing more untested CFG levers — it tells you
   whether that's even a productive use of the next batch.
4. **Decide and promote:** once (1)-(3) settle, pick the winning
   `k_photoCost` dose, add its LEDGER version-log row, delete whichever
   of v0.49/v0.50 doesn't end up superseded (per rule 6/9's convention —
   only once results are captured here).
5. **Only then** open new CFG-lever territory beyond what's already
   fired (there's a lot already in flight — let it resolve before adding
   more untested branches; CLAUDE.md's saturation policy prefers new
   seeds on real open questions over padding).
6. **Longer-horizon, once the above settles:** the still-untouched
   HANDOFF §1 threads (omnivory/carnivory magnitude via v0.50, herding
   via riskEwma, effective population, behavioral monoculture) are the
   actual mission-relevant questions this whole investigation has been
   in service of — don't lose sight of them once the population-balance
   question is settled. A "balanced" population that still shows 90%+
   GRAZE and near-zero carnivory hasn't achieved the mission, just fixed
   a prerequisite for testing it properly.

---

## 1. Current state — v0.49.0

**Achieved and replicated:**

- **Herbivory** emerged, obviously.
- **Omnivory emerged twice on independent seeds** (v0.39 seed 5723, v0.42
  seed 3012, the latter holding for 367 sim-years with all 207 animals in one
  carnivory histogram bin). This is the project's headline result — **still
  on the hook, still not confirmed for the current build, but now visibly
  seed-dependent rather than uniformly weak.** Seed 1337 default's carnivory
  histogram sits at near-zero; seed 4001 default's sits at moderate carnivory
  (164/173 animals in two adjacent mid-range bins). Two seeds disagreeing this
  directly means neither confirms nor overturns the old result — it means the
  3-seed protocol isn't optional here, it's the only way to know which seed
  is the outlier. See §3 Tier 1, item 1.
- **The `k_confusion:0` isolation-arm finding, revisited: complicated by the
  third default-arm seed, not confirmed.** The default-arm 3-seed set is now
  complete (1337, 4001, 4002) alongside 3 `k_confusion:0` seeds, closing the
  last gap in the v0.47 protocol — but seed 4002's default-arm run does not
  fit the "stable" pattern the first two default seeds showed. It hit its
  wall-clock budget at day 302 (fauna arrived day 265, so only a 37-day-old,
  still-reseed-subsidized population) showing the same *flavor* of failure
  as the isolation arm: refuge collapsing (`pLocked` 30-day fall -0.197),
  R0 0.11, 98.5% of deaths by starvation — despite `k_confusion` being ON.
  The confound (a third the length of the other two seeds, entirely inside
  the reseed subsidy window, one plant slot bound hit) is large enough that
  this **cannot be scored as confirming or refuting** the isolation-arm
  result on its own. See LEDGER.md's v0.47 Scorecard, 3rd pass, for the
  full numbers and reasoning.
- **Free follow-up (addendum to the 3rd pass) found a more specific
  candidate explanation, still untested.** (Corrected same session — the
  first version misread the 1337 `k_confusion:0` log as its default-arm
  log; see LEDGER.md's addendum note.) 1337's correct default-arm raw JSON
  shows a different pre-fauna plant trajectory than 4002: at day 260,
  **15,619** plants / `pOcc` 0.30 for 1337 vs **53,180** plants / `pOcc`
  0.79 for 4002, with 4002 repeatedly sitting at its `maxPlants` slot cap
  in the run-up to day 265 while 1337 never hit it once. That is a pure
  plant-side difference no animal-behaviour mechanism (confusion or
  otherwise) can explain. Leading candidate: **the boom-bust isn't about
  `k_confusion` at all — it's that seed 4002 grew an oversized, capped food
  base before fauna arrived, and that's what let a tiny founding population
  explode past whatever protection existed.** This would also explain the
  isolation arm's 3-for-3 failure rate (a smaller pre-fauna food base makes
  `k_confusion`'s setting matter less either way).
  **Not acted on — new hypothesis, Tier B, proposed to the owner and
  awaiting a decision before any run or CFG patch tests it.** A resumed
  seed-4002 long read on v0.49 (`kc-arm-default-v49-longread`, Tier A,
  already queued) is running to at least get this seed to a comparable
  length to 1337/4001, independent of whether the plant-cap hypothesis is
  pursued.
- **Plant/animal arms races** in height-vs-reach and toxicity-vs-resistance.
- **Matter conservation** to 0.000000% on most runs.
- **Demography, mixed since v0.47.** The 1200-day default seed-1337 run has
  mean death age 12.1 d against maturityAge 36.0 d (ratio 0.34, "dies before
  breeding") and R0 1.06 — better than extinct, worse than the v0.42 ratio of
  2.95 this line used to cite. The run is **not stationary** (animals still
  +32.7%/100d at the end), so treat this as a mid-transient snapshot, not a
  result.
- **Possible plant speciation, uninvestigated:** v0.42 seed 3012's height
  histogram is bimodal — `[12,7,0,0,0,0,0,16,20,10,7,2]`, 19 plants low, 55
  high, nothing between. Understory vs canopy. Nobody has checked whether the
  clusters are reproductively separated.

**Not achieved:**

- **Herding, partially mechanised, not confirmed working.** `socialAttraction`
  was impossible to select for by construction before v0.47 — appeared only
  as a cost, absorbing `>0.02` gate, no dilution/vigilance/confusion anywhere
  in the model. [L47-3] gave it a confusion mechanism and an `AN.risk` EWMA.
  Result so far: `socialAttraction` mean rose to 0.235 with 0% pinned at min
  in a run with real predation — the purge stopped — but `actAppr` (the act
  that would express grouping-for-safety behaviourally) stayed ~0.0% of the
  action budget, missing its own >1% falsifier. Leading hypothesis, untested:
  `AN.risk`'s EWMA smooths out the threat signal that would make APPROACH
  worth it, so GRAZE (always available) structurally outcompetes it even
  though the underlying gene isn't purged anymore.
- **Speciation is not properly testable.** Reproduction is still asexual;
  crossover was "phase 5" and never built. Lineages are k-means instrumentation,
  not reproductive isolation.
- **Effective population.** Harmonic N was 215 in the healthiest available
  v0.47-era log, still under the 500 target, and the run wasn't stationary so
  even that number is a transient reading.
- **Behavioural monoculture, improved but not solved.** GRAZE fell from 96%
  (v0.46) to 92.2% of the action budget in the same run — non-graze share
  roughly doubled (3.8% → 7.8%) but is still far from the ≥20% target.

**v0.48 and v0.49 are both mechanical/tooling versions, not biology
versions.** v0.48 fixed a bug that silently disabled the extinction halt at
default config ([L0.48-1]) and a performance win in the two hottest
functions ([L0.48-2]), verified RNG-neutral against v0.47 on an exact-match
diff. v0.49 replaced the five hottest per-tick loops' `0..P.hi`/`0..AN.hi`
scan with a compact occupied-slot list ([L0.49-1]) — a run no longer pays
forever for its largest-ever population once it's crashed back down.
**Unlike v0.48, v0.49 is *not* RNG-exact** — verified instead on matter
conservation (exact in both arms) and the absence of a *consistent*
directional bias across two independent seeds, since two of the five
converted loops feed order-sensitive detection scans. Individual-seed
population outcomes moved a lot and in opposite directions per seed — read
the full verification in `LEDGER.md` before treating either seed's specific
numbers as informative on their own. Neither version changed a formula, a
constant, or a gene. **The v0.47 biology questions above are still open**
and carry forward unchanged — finishing that interrupted 3-seed protocol
(Tier A: it executes an already-approved plan, originates nothing new) is
the natural next run, and can run on v0.49 exactly as it would have on v0.48
now that the wall-clock-bound seeds won't be held back by the high-water-mark
slowdown. Full writeups: `LEDGER.md`, "v0.47 — external audit pass" and its
"Scorecard" subsections, "v0.48 — extinction-halt fix + global-lookup
caching", and "v0.49 — occupied-slot lists replace the P.hi/AN.hi scan
bound".

One more open question, found reading the code rather than a run, not yet
acted on: ATTACK's arbiter weight is `0.5 + meatAttraction` (floor 0.5,
`meatAttraction` ∈ [0,1]) while GRAZE and SCAVENGE use their attraction genes
unfloored — predation structurally can't fully switch off the way herbivory
and scavenging can. Owner hasn't said whether this is intentional; flagged,
not touched.

---

## 2. The three frameworks that made the difference

Apply these before touching a constant.

### 2a. Why a gene pins at a bound

A gene rails when marginal benefit over marginal cost never crosses 1 inside its
range. With cost `k·g²` and benefit `b·g^p`:

| | outcome | fix |
|---|---|---|
| **p < 2** | interior optimum at `g* = (pb/2k)^(1/(2-p))`; rails only if `k` too small | **magnitude** — change the constant |
| **p = 2** | *no* interior optimum at any `k`; rails to max if b>k, min if b<k, and changing `k` only flips which rail | **structural** — change the cost shape |
| **p > 2** | always rails to max | **structural** |

`photoEfficiency` is the control that proves it: quadratic cost, linear benefit,
never pinned in any run (0.487, `atMax 0.00`).

**Worked examples from v0.44, which hit 4 of 6 predictions:**

- `senseRange` — detections scale with the **area** scanned, so p=2. Squared
  cost was hopeless. Made cost cubic. Unpinned.
- `toxinResistance` — protection was `(1 - tr)`, hitting exactly zero at tr=1,
  so total immunity was purchasable at a fixed price while plants escalated
  toxicity without limit. Changed to `1/(1+tr)`, asymptotic. Unpinned, and toxin
  cost fell 29.9% → 17.2% of intake. **Caveat: [L47-1] found this fix never
  landed in the two scoring functions, so that number is contaminated.**
- `acceleration`, `turnRate` — shape already right, constants 3x too small.
  Magnitude fix. Unpinned.
- `herbivory` — `k_digest` only charged the excess over `carn+herb=1`, so
  herbivory below 1.0 was **free**. Added `k_gut·(carn²+herb²)`. Still 90% at
  max at 0.008; raised to 0.020 in v0.45, untested.

**DO NOT widen a bound to fix a pin.** Tried in v0.43, reverted in v0.44. A rail
moves; it does not go away.

### 2b. Pivot discipline

When changing an exponent, re-pivot the constant so the value is **unchanged at
the founder / typical value** and only the slope moves. Otherwise you've changed
two things and can't attribute the result.

- `k_reach` 0.025 → 0.0731 when reach went `size^1.0` → `size^0.333` (identical
  at the founder size of 5).
- `k_sense` 4e-5 → 2e-6 when sense cost went `r²` → `r³` (identical at range 20).

### 2c. Is the gene even connected? (new, v0.47)

Before diagnosing a gene as badly *tuned*, check it has a **benefit term
anywhere in the model at all**. `socialAttraction` was diagnosed as an arbiter
weighting problem for eleven versions when grouping conferred no advantage of
any kind — it could only ever be purged, and no constant would have changed
that. Two follow-ups worth making habit:

- **Does the score that reads it share a currency with its rivals?** Until
  v0.47 GRAZE returned energy per tick and everything else returned a
  dimensionless weight, so the modeller, not selection, set what animals did.
- **Is there a threshold gate around it?** `if (gene > 0.02)` around the only
  code that can select for a drifting gene is an absorbing state.

### 2d. Other diagnostics worth keeping in mind

- **Inert genes are a free Ne meter.** Nothing reads `immunity0-3`, `tag0-2`,
  `mateChoosiness`, `pollenRange`, `selfingTolerance`, `pathogenResistance`,
  `parentalCare`. Their spread is pure mutation–drift balance. Flat or falling
  means Ne is far below census N. `analyze.py` reports this.
- **`pLocked` is the control variable of the whole consumer–resource system**,
  and **both extremes kill**. At 0.02 (v0.37 seed 5499) the grazers ate
  everything and starved. At 0.996–0.998 (v0.42) the fauna lived on 0.4% of
  plant biomass and starved anyway. Target roughly **0.5–0.85**. Its *rate* of
  change is the early warning; its level is a lagging signal.
- **Check whether an extinction is starvation or fecundity.** v0.46 seed 3071's
  last animals had `aEnergy` 186 and `aFeedFrac` 0.81 with plants recovering —
  well fed and still dying. The real cause was `pOcc` 0.03 with `pPerTile` 43:
  the flora had collapsed into clumps on 3% of tiles, and ~0.7 offspring per
  lifetime meant R0 < 1 from the founders on. **analyze.py now computes
  births/animal-lifetime** — it is printed in the DEMOGRAPHY block.

---

## 3. Outstanding changes, prioritized

### Tier 1 — do these next

**1. The v0.47 protocol's seed count is complete; its data quality is not.**
`LEDGER.md`'s "Scorecard, 3rd pass" (under "v0.47 — external audit pass") now
has the full 3-seed default arm (1337, 4001, 4002) and 3 `k_confusion:0`
seeds. But seed 4002 default only reached day 302 (wall-clock cutoff) with
fauna 37 days old and still inside the reseed-subsidy window — not a peer of
1337 (1200d) or 4001 (930d). Its gene-frequency snapshot (`eToxin`,
carnivory histogram, `actAppr`) is usable at the same weight as the other
two; its population-dynamics numbers (R0, refuge collapse) are not, and are
exactly what would be needed to settle item 2 below. **Next step, Tier A
(extends an already-approved seed's run, originates nothing new) but
requires the owner's go-ahead per this session's explicit instruction not to
act on the k_confusion:0 finding further without it:** either resume seed
4002 past its wall-clock cutoff on `evosim-v0_49_0.html` (now cheap — v0.49's
occupied-slot fix removes the exact tax that cut this run short), or pull
1337/4001's own first-40-days-with-fauna window from their existing raw JSON
to check whether they looked this rough too before stabilizing.

L47-4/5/6 are performance-only claims and **must not move any ecological
statistic**. If they do, something in the build depends on slot ordering or
draw ordering and that is a bug worth finding.

**2. The omnivory result is still on the hook.** [L47-2] found that GRAZE
scored as own `mass^0.667`–`mass^1` while ATTACK was scale-free in own mass,
so the collapse of `size` from 5.07 to 1.09 cut the *perceived* value of
grazing ~3x against hunting with no change to any actual payoff — and both
historic omnivory sweeps happened alongside shrinking size. What exists now
(three `k_confusion:0` seeds, all failing; three default seeds, two stable-
at-cutoff and one too short/subsidized to read) still neither confirms nor
overturns this — `corr(aSize, carnivory)` stayed strongly negative (-0.79) in
the 1337 default run, consistent with the concern but not conclusive across
seeds that disagree on where carnivory even lands (near-zero in 1337/4002,
moderate in 4001). Item 1's follow-up (a longer seed-4002 read, or the
early-window check) is what would settle it.

**3. The `AN.risk`-EWMA hypothesis for `actAppr` staying near 0% is
untested.** See §1. Worth checking directly in the next `k_confusion`-default
log rather than guessing further — plot `AN.risk` against attack events in
the same window and see whether it ever clears whatever threshold would make
APPROACH competitive with GRAZE.

**4. `maturityAge`'s status needs a direct check, not more inherited
assumptions.** Older versions of this doc said it was "pinned 98% at min."
The most recent log (seed 1337 default, 1200d) shows mean `maturityAge` 36.0
d against mean death age 12.1 d — animals dying well before that, which is a
different problem (see the demography line in §1) and doesn't by itself say
whether the gene is railed, since `analyze.py`'s GENE BOUNDS section for that
run doesn't list `maturityAge` among the pinned genes at all. Don't assume
either the old "pinned at min" finding or its opposite — check the next
log's GENE BOUNDS section directly before reasoning further about the mass
gate (`mass >= 0.60*size`) or newborn provisioning.

**5. Raise effective population above 500.** Harmonic N was 215 in the most
recent usable log (not stationary, so read as a floor not a ceiling). It
moved 87 → 338 once before, via the `k_photoCost` cut — productivity is the
lever that has worked historically. v0.48's performance fix should make
longer runs cheap enough that this is measurable over more generations.

### Tier 2 — real science, currently blocked

**6. Sexual reproduction / per-gene crossover.** Long-planned, never built.
Without it there is no biological species concept and the speciation half of the
mission is untestable. This is the largest genuinely outstanding feature.

**7. Investigate the bimodal plant height in v0.42 seed 3012.** Check whether
the two clusters are separated in the lineage tree. If they are, that's
speciation and it hasn't been claimed.

**8. Detection is re-rolled every think.** P(never detected) over a residence
time is `(1-p)^n`, so `camouflage` and `senseAcuity` saturate and are much
weaker than their formulas suggest. Fixing it means per-animal detection memory
— a real feature, not a patch. **Know this before tuning either gene.**

### Tier 3 — held on purpose, with reasons

**9. Plant height superlinear cost.** Proposed when height was 30% of plant
upkeep in v0.42. It is **10%** in v0.44 with `pHeight` 0.339, not railed. Acting
now would break rule 5 — calibrating against a superseded run.

**10. `carrionFloor` 0.30.** Analysis said it subsidises scavenging and destroys
the marginal return on low carnivory. But the v0.39 omnivory sweep happened
*with* the floor at 0.3, so the diagnosis is at least incomplete. Do not touch
until something else forces it.

**11. Matter leak.** 0.0157% in v0.42, 0.000000% since v0.44 including v0.48's
verification run. Either fixed incidentally or the runs were too short. Watch
on the next long run rather than hunting a leak that may not exist.

**12. Prune the inert genes** (8 plant, 7 animal). Cheap tokens and cheap
memory, but they are the Ne meter — keep at least four per kingdom if you cut.

**13. Cosmetic debt.** `laiOf()` is dead code after [L47-6]. `PIDX` can file a
recycled slot under a stale tile for up to `plantStagger` ticks — self-correcting,
but it silently drops that plant from detection meanwhile.

---

## 4. The iteration cycle

**As of the headless tooling (`headless.js`/`experiment.js`/the GitHub Actions
workflow, see `CLAUDE.md`'s "Automated iteration" section), Claude runs the
experiments.** That section splits runs into two tiers: **Tier A (diagnostic —
extra seeds, an isolation arm already called for, a replication)** auto-chains
without waiting on the owner between runs; **Tier B (a new CFG hypothesis, or
anything touching `evosim-v0_49_0.html`)** always stops for approval before it
runs. The owner's
job either way is to approve what originates a run, not to carry a build to
their phone or to click go on every mechanical follow-through. The owner can
still run a build by hand any time (spot checks, or to watch it) — that log
works exactly the same way through the steps below. Long runs are still the
constraint that matters: anything under ~900 sim-days can't see a carnivory
sweep, which historically starts around day 800, and true stationarity has
needed hundreds of sim-years (v0.42 ran 367). Prefer the longest run that's
practical over a short one — a run taking too long is a reason to stop it
early with `<out>.stop` (see `headless.js`'s header) or move it to GitHub
Actions, not a reason to quietly shorten the day target without saying so.

### What Claude does, in order

**Step 0 — get the change and prediction on record, and approved if it's Tier
B.** Nothing in this cycle starts without a written, falsifiable prediction.
Tier A only ever executes a prediction that's already on record from a prior
approval; it never originates one. This is the step automation does not
remove (`CLAUDE.md` rule 1).

**Step 1 — run it.**
```
node experiment.js --build evosim-v0_49_0.html --days <n> --label <name> \
    [--cfg patch.json] [--n 3]
```
or, for real per-seed parallelism at no sandbox cost, trigger the `evosim
experiment` GitHub Actions workflow with the same arguments (needs the
workflow file on `main`; ask the owner if it isn't there yet). Writes
`runs/<name>/seed-*.json`, `manifest.json`, and `digest.txt` locally, or a
per-seed artifact plus a digest artifact on Actions. Watch `<out>.progress.json`
during a long run instead of guessing how far along it is, and use `<out>.stop`
to end one early with a still-valid, still-complete log rather than `kill`ing
it and getting nothing back. Confirm what actually ran before reading
further, same as ever — the manifest and each log's own `cfg` block say so;
config patches sometimes don't apply the way you expect.

**Step 2 — read the digest in this order, and stop early if a gate fails:**

1. **CONSERVATION** — matter drift and `caps seen`. A cap that binds means a
   bound is doing the selecting and nothing below is what it looks like.
2. **STATIONARITY GATE** — if it fails, gene means are a transient. Say so and
   do not compare them to another version.
3. **DEMOGRAPHY** — extinction flag; mean death age vs maturityAge; and
   **births/animal-lifetime (R0)**. Below 1 means the population was never
   viable regardless of how well fed it looked.
4. **REFUGE** — `pLocked` p10/median, worst 30-day fall, `corr(aSize, pLocked)`.
5. **EFFECTIVE POPULATION** — inert-gene diversity trend.
6. **GENE FLAGS** — every `PINNED` line, classified by §2a into
   magnitude / structural / correctly-pinned.
7. **ENERGY, ACTION BUDGET, TROPHIC LEDGER, HISTOGRAMS, LINEAGES.**

**Step 3 — write the scorecard against the prediction that was approved for
this run.** State plainly which predictions hit and which missed. A missed
prediction means the diagnosis was wrong, not that the constant needs to be
bigger.

**Step 4 — add the row to `LEDGER.md`**, and promote the specific logs that
row is based on into the repo root, same convention as the phone-run logs —
`runs/` is gitignored scratch space; a run is cheap to reproduce from its seed
since the sim is fully deterministic per seed (`headless.js` proves this by
construction: same script, same seed, same `tick()` loop the browser runs).

**Step 5 — report, and stop unless the next step is already-approved Tier A.**
The scorecard, plus **one plain-language paragraph on what happened in that
world this iteration** — what the population actually did and why it matters,
not a restatement of the table. If the next queued run is Tier A (already
approved, nothing new originated), fold this into a running batch update and
start it without waiting. The moment the next step would be Tier B — a new
hypothesis, or any change to `evosim-v0_49_0.html` — propose it with its own
prediction and **stop and wait**. No code change ever ships without the
owner's word, regardless of tier.

### The one thing that will still bite you

`headless.js`/`experiment.js` make running the sim *easy* — that was true and
dangerous even before they existed, and it does not stop being dangerous now
that it's sanctioned. The discipline that keeps it honest is Step 0: a
prediction on record before the run, one change at a time, no quietly trying a
few variants to see which looks better. `check.js` still prints no statistic,
on purpose — it checks the code resolves, nothing about the ecology.

---

## 5. Standing scorecard

Check every version. This is the answer to "are we still on mission".

The v0.47/v0.48 column is **one seed (1337, default config, 1200d), not
stationary** — the interrupted protocol (§3 Tier 1 item 1) never produced the
3-seed set this table wants. Read it as a transient snapshot, not a verdict,
and finish that protocol before trusting it further. v0.48 changed no
formula or constant, so this column is unchanged from v0.47.

| | target | v0.36 | v0.42 (367 yr) | v0.47/v0.48 (n=1, not stationary) |
|---|---|---|---|---|
| harmonic animal N | ≥ 500 | 100 | 91 | 215 |
| mean death age / maturityAge | ≥ 1.0 | 0.65 | **2.95** | 0.34 (12.1d / 36.0d) |
| births / animal-lifetime (R0) | > 1.0 | — | — | **1.06** |
| deaths by age or predation | ≥ 20% | 0.07% | 1.83% | 36.5% (killed) + 0.0% (age) |
| carnivory mean | ≥ 0.20 | 0.072 | **0.288** | low — histogram-dominated near zero (369/371 animals in the bottom bin); not printed as a scalar |
| flesh + carrion, share of intake | ≥ 5% | 0.1% | 0.85% | 0.26% |
| `aSeen` | ≥ 1.0 | 0.36 | **7.03** | 0.36 |
| non-graze action share | ≥ 20% | 3% | 3.8% | 7.8% |
| `socialAttraction` mean | not railed at 0 | 0 | 0 | **0.235, 0% pinned at min** |
| `pLocked` | 0.5–0.85 | — | 0.996 | 0.969 (median) |
| inert-gene sd | rising | falling | flat | plant flat (ceiling), animal falling |
| genes pinned at a bound | 0 | — | 14 | 4 explicitly flagged PINNED (fibre, toughness, toxicity, pathogenResistance) + several more 20-27% at a bound |
| stationary at end of run | yes | no | no | **no** — plants/bio/animals/soil all still drifting |

---

## 6. Current tunables worth knowing

```
k_photoCost 0.004    k_darkResp 0.25       (plant respiration on lit leaf)
k_reach 0.0731       reachMassPow 0.333    (reach = k·size^p, a LENGTH)
k_climbReach 4.0                           (reach × (1 + k·climbing))
k_bodyRadius 0.60                          (attack/scavenge reach)
k_sense 2.0e-6       cubic in range
k_gut 0.020          k_digest 0.004        mixedFree 0.06   k_mixed 0.018
k_accel 0.012        k_turn 0.009
a_base 0.012         FIXED, not mass-scaled
maturityMassFrac 0.60
carrionFloor 0.30
haltAfterDays 200    logDays 5             poolSize 650

  new in v0.47
k_confusion 0.060    attack rate / (1 + k·(neighbours−1)). 0 disables herding.
riskEwma 0.010       smoothing on AN.risk, the per-animal threat estimate
mutFastMax 0.25      above this mutationRate, mutate gene-by-gene
compactEvery 2400    ticks between free-list compactions. 0 disables.
fastRenderMs 100     min ms between frames once above watch speed
```

Genome strides: plant **48** (39 active + 9 pad), animal **64** (54 active + 10
pad). `FORMAT_VERSION` 36, unhooked from `VERSION` — bump only when the save
schema changes. v0.47 adds no genes and does not touch the save schema.

**Founder pool:** "Export founder pool" writes ~650 evolved genomes per kingdom.
Loading one makes founders draw from evolved genetics instead of random morphs.
This is the replication fix — fixed seed does *not* reproduce a starting flora,
because any code change shifts RNG draw ordering. **If a run reaches an omnivory
sweep, export the pool before stopping it.** That turns future short runs from
"too short to see it" into "long enough to test whether it holds".
