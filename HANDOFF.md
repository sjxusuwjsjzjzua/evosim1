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

## 1. Current state — v0.47.0

**Achieved and replicated:**

- **Herbivory** emerged, obviously.
- **Omnivory emerged twice on independent seeds.** v0.39 seed 5723: carnivory
  swept to 0.269 while herbivory stayed 0.988, with a coherent ecomorph
  (senseRange 16.8→47.2, preySizeRatio 0.86→2.46, size 2.1→1.74, maturityAge
  down 4.6x, socialAttraction purged). v0.42 seed 3012 held it for 367 sim-years
  with **all 207 animals in one carnivory histogram bin** and corpse recovery at
  70.2%. This is the project's headline result — **and v0.47 [L47-2] puts a
  question mark on it. See §3 Tier 1.**
- **Plant/animal arms races** in height-vs-reach and toxicity-vs-resistance.
- **Matter conservation** to 0.000000% on most runs.
- **Demography fixed:** mean death age 12.4 d against maturityAge 4.2 d, ratio
  2.95. It was 0.65 at v0.36.
- **Possible plant speciation, uninvestigated:** v0.42 seed 3012's height
  histogram is bimodal — `[12,7,0,0,0,0,0,16,20,10,7,2]`, 19 plants low, 55
  high, nothing between. Understory vs canopy. Nobody has checked whether the
  clusters are reproductively separated.

**Not achieved:**

- **Herding.** Was impossible by construction until v0.47 — `socialAttraction`
  appeared only as a cost, with no dilution, vigilance or confusion anywhere in
  the model, behind an absorbing `> 0.02` gate. [L47-3] gives it a mechanism.
  Untested.
- **Speciation is not properly testable.** Reproduction is still asexual;
  crossover was "phase 5" and never built. Lineages are k-means instrumentation,
  not reproductive isolation.
- **Effective population.** Harmonic N runs 90–340 against a target of 500.
  Everything is still partly drift.
- **Behavioural monoculture.** 96% of the action budget was GRAZE at v0.46.
  [L47-2] is the first serious attempt at the cause.

**v0.47 is unrun.** It is six changes from an external audit: one bug fix, two
biology changes, three performance. Full rationale and all six predictions are
in `LEDGER.md` under "v0.47 — external audit pass".

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

**1. Score the six v0.47 predictions.** They are written out in `LEDGER.md`
("v0.47 — external audit pass"), one per change, with the falsifier for each.
Recommended run order:

- 3 seeds with a `{"cfg":{"k_confusion":0}}` patch — scores L47-1 (toxin) and
  L47-2 (arbiter currency) with the herding mechanism off.
- then 3 seeds with `k_confusion` at its default 0.060 — scores L47-3.

L47-4/5/6 are performance only and **must not move any ecological statistic**.
If they do, something in the build depends on slot ordering or draw ordering and
that is a bug worth finding.

**2. The omnivory result is on the hook.** [L47-2] found that GRAZE scored as
own `mass^0.667`–`mass^1` while ATTACK was scale-free in own mass, so the
collapse of `size` from 5.07 to 1.09 cut the *perceived* value of grazing ~3x
against hunting with no change to any actual payoff — and both omnivory sweeps
happened alongside shrinking size. If carnivory does not survive v0.47 on 3
seeds, the headline result needs restating, not defending. Check
`corr(aSize, carnivory)` explicitly.

**3. `maturityAge` still pinned 98% at min, and the v0.44 fix disabled itself.**
The mass gate (`mass >= 0.60*size`) made large size slow to breed, so `size`
collapsed to 1.09 and the gate became trivially satisfiable. v0.45's fixed
`a_base` should put a floor under size and restore the gate's bite — **check
this in the next log.** If `size` is healthy and `maturityAge` is *still*
railed, the gate is the wrong mechanism entirely and needs replacing, not
repairing. The honest alternative is that breeding small should produce
offspring with poor survival, and currently it doesn't: newborn provisioning is
`offspringInvestment * nbUp`, so a tiny newborn gets the same *days* of reserve
as a big one. Being born small is free.

**4. Raise effective population above 500.** Everything below is partly
unmeasurable until this happens. It moved 87 → 338 via the `k_photoCost` cut,
which was the single biggest win of the last chat, so productivity is the lever
that works. The v0.47 performance work should also make longer runs cheap enough
that this is measurable over more generations.

### Tier 2 — real science, currently blocked

**5. Sexual reproduction / per-gene crossover.** Long-planned, never built.
Without it there is no biological species concept and the speciation half of the
mission is untestable. This is the largest genuinely outstanding feature.

**6. Investigate the bimodal plant height in v0.42 seed 3012.** Check whether
the two clusters are separated in the lineage tree. If they are, that's
speciation and it hasn't been claimed.

**7. Detection is re-rolled every think.** P(never detected) over a residence
time is `(1-p)^n`, so `camouflage` and `senseAcuity` saturate and are much
weaker than their formulas suggest. Fixing it means per-animal detection memory
— a real feature, not a patch. **Know this before tuning either gene.**

### Tier 3 — held on purpose, with reasons

**8. Plant height superlinear cost.** Proposed when height was 30% of plant
upkeep in v0.42. It is **10%** in v0.44 with `pHeight` 0.339, not railed. Acting
now would break rule 5 — calibrating against a superseded run.

**9. `carrionFloor` 0.30.** Analysis said it subsidises scavenging and destroys
the marginal return on low carnivory. But the v0.39 omnivory sweep happened
*with* the floor at 0.3, so the diagnosis is at least incomplete. Do not touch
until something else forces it.

**10. Matter leak.** 0.0157% in v0.42, 0.000000% in v0.44 and v0.46. Either
fixed incidentally or the runs were too short. Watch on the next long run rather
than hunting a leak that may not exist.

**11. Prune the inert genes** (8 plant, 7 animal). Cheap tokens and cheap
memory, but they are the Ne meter — keep at least four per kingdom if you cut.

**12. Cosmetic debt.** `laiOf()` is dead code after [L47-6]. `PIDX` can file a
recycled slot under a stale tile for up to `plantStagger` ticks — self-correcting,
but it silently drops that plant from detection meanwhile.

---

## 4. The iteration cycle

**As of the headless tooling (`headless.js`/`experiment.js`/the GitHub Actions
workflow, see `CLAUDE.md` §7), Claude runs the experiments.** §7 splits runs
into two tiers: **Tier A (diagnostic — extra seeds, an isolation arm already
called for, a replication)** auto-chains without waiting on the owner between
runs; **Tier B (a new CFG hypothesis, or anything touching
`evosim-v0_47_0.html`)** always stops for approval before it runs. The owner's
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
node experiment.js --build evosim-v0_47_0.html --days <n> --label <name> \
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
hypothesis, or any change to `evosim-v0_47_0.html` — propose it with its own
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

| | target | v0.36 | v0.42 (367 yr) | v0.47 |
|---|---|---|---|---|
| harmonic animal N | ≥ 500 | 100 | 91 | — |
| mean death age / maturityAge | ≥ 1.0 | 0.65 | **2.95** | — |
| births / animal-lifetime (R0) | > 1.0 | — | — | — |
| deaths by age or predation | ≥ 20% | 0.07% | 1.83% | — |
| carnivory mean | ≥ 0.20 | 0.072 | **0.288** | — |
| flesh + carrion, share of intake | ≥ 5% | 0.1% | 0.85% | — |
| `aSeen` | ≥ 1.0 | 0.36 | **7.03** | — |
| non-graze action share | ≥ 20% | 3% | 3.8% | — |
| `socialAttraction` mean | not railed at 0 | 0 | 0 | — |
| `pLocked` | 0.5–0.85 | — | 0.996 | — |
| inert-gene sd | rising | falling | flat | — |
| genes pinned at a bound | 0 | — | 14 | — |
| stationary at end of run | yes | no | no | — |

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
