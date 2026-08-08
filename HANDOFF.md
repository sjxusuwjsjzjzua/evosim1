# evosim — handoff to a new chat

Paste this, `LEDGER.md`, `analyze.py` and the current build into the new chat or
project knowledge. Read this file first.

---

## 0. What this project is

A single-file HTML evolution simulator. Two kingdoms, plants and animals, both
with a genome of continuous traits inherited with mutation. **Nothing about
behaviour is hardcoded** — herbivory, carnivory, herding, speciation, arms races
all have to emerge from the genes and the physics. The owner runs it on a phone.

**The mission test:** if a result had to be written into the code, it doesn't
count.

---

## 1. Current state — v0.46.0

**Achieved and replicated:**

- **Herbivory** emerged, obviously.
- **Omnivory emerged twice on independent seeds.** v0.39 seed 5723: carnivory
  swept to 0.269 while herbivory stayed 0.988, with a coherent ecomorph
  (senseRange 16.8→47.2, preySizeRatio 0.86→2.46, size 2.1→1.74, maturityAge
  down 4.6x, socialAttraction purged). v0.42 seed 3012 held it for 367 sim-years
  with **all 207 animals in one carnivory histogram bin** and corpse recovery at
  70.2%. This is the project's headline result.
- **Plant/animal arms races** in height-vs-reach and toxicity-vs-resistance.
- **Matter conservation** to 0.000000% on most runs.
- **Demography fixed:** mean death age 12.4 d against maturityAge 4.2 d, ratio
  2.95. It was 0.65 at v0.36.
- **Possible plant speciation, uninvestigated:** v0.42 seed 3012's height
  histogram is bimodal — `[12,7,0,0,0,0,0,16,20,10,7,2]`, 19 plants low, 55
  high, nothing between. Understory vs canopy. Nobody has checked whether the
  clusters are reproductively separated.

**Not achieved:**

- **Herding.** `socialAttraction` is actively purged in every run.
- **Speciation is not properly testable.** Reproduction is still asexual;
  crossover was "phase 5" and never built. Lineages are k-means instrumentation,
  not reproductive isolation.
- **Effective population.** Harmonic N runs 90–340 against a target of 500.
  Everything is still partly drift.
- **Behavioural monoculture.** 96% of the action budget is GRAZE. Every
  behaviour gene outside grazing is unselected.

---

## 2. The two frameworks that made the difference

These are the most valuable things discovered in the last chat. Apply them
before touching a constant.

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
  cost fell 29.9% → 17.2% of intake.
- `acceleration`, `turnRate` — shape already right, constants 3x too small.
  Magnitude fix. Unpinned.
- `herbivory` — `k_digest` only charged the excess over `carn+herb=1`, so
  herbivory below 1.0 was **free**. Added `k_gut·(carn²+herb²)`. Still 90% at
  max at 0.008; raised to 0.020 in v0.45, untested.

**DO NOT widen a bound to fix a pin.** It was tried in v0.43 and reverted in
v0.44. A rail moves; it does not go away.

### 2b. Pivot discipline

When changing an exponent, re-pivot the constant so the value is **unchanged at
the founder / typical value** and only the slope moves. Otherwise you've changed
two things and can't attribute the result.

- `k_reach` 0.025 → 0.0731 when reach went `size^1.0` → `size^0.333` (identical
  at the founder size of 5).
- `k_sense` 4e-5 → 2e-6 when sense cost went `r²` → `r³` (identical at range 20).

### 2c. Other diagnostics worth keeping in mind

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
  they were well fed and still died. The real cause was `pOcc` 0.03 with
  `pPerTile` 43: the flora had collapsed into clumps on 3% of tiles, and ~0.7
  offspring per lifetime meant R0 < 1 from the founders on. **Always compute
  births per animal-lifetime before blaming food.**

---

## 3. Outstanding changes, prioritized

### Tier 1 — do these next

**1. `maturityAge` still pinned 98% at min, and the v0.44 fix disabled itself.**
The mass gate (`mass >= 0.60*size`) made large size slow to breed, so `size`
collapsed to 1.09 and the gate became trivially satisfiable. v0.45's fixed
`a_base` should put a floor under size and restore the gate's bite — **check
this first in the next log.** If `size` is healthy and `maturityAge` is *still*
railed, the gate is the wrong mechanism entirely and needs replacing, not
repairing. The honest alternative is that breeding small should produce
offspring with poor survival, and currently it doesn't: newborn provisioning is
`offspringInvestment * nbUp`, so a tiny newborn gets the same *days* of reserve
as a big one. Being born small is free.

**2. Verify the v0.45 / v0.46 predictions.** `size` off the minimum and
interior; `herbivory` below 0.9; genome padding cut didn't break anything
(strides are now 48 and 64; founder pools and saves still load, `FORMAT_VERSION`
stays 36).

**3. Raise effective population above 500.** Everything below is partly
unmeasurable until this happens. It has moved 87 → 338 via the `k_photoCost`
cut, which was the single biggest win of the last chat, so productivity is the
lever that works.

### Tier 2 — real science, currently blocked

**4. Sexual reproduction / per-gene crossover.** Long-planned, never built.
Without it there is no biological species concept and the speciation half of the
mission is untestable. This is the largest genuinely outstanding feature.

**5. Investigate the bimodal plant height in v0.42 seed 3012.** Check whether
the two clusters are separated in the lineage tree. If they are, that's
speciation and it hasn't been claimed.

**6. Break the behavioural monoculture.** 96% GRAZE means every non-grazing
behaviour gene is unselected. Probably downstream of density and the one-
dimensional environment rather than a bug in the arbiter.

### Tier 3 — held on purpose, with reasons

**7. Plant height superlinear cost.** Proposed when height was 30% of plant
upkeep in v0.42. It is **10%** in v0.44 with `pHeight` 0.339, not railed. Acting
now would break rule 7 — calibrating against a superseded run.

**8. `carrionFloor` 0.30.** Analysis said it subsidises scavenging and destroys
the marginal return on low carnivory. But the v0.39 omnivory sweep happened
*with* the floor at 0.3, so the diagnosis is at least incomplete. Do not touch
until something else forces it.

**9. Matter leak.** 0.0157% in v0.42, 0.000000% in v0.44 and v0.46. Either fixed
incidentally or the runs were too short. Watch on the next long run rather than
hunting a leak that may not exist.

**10. Prune the inert genes** (8 plant, 7 animal). Cheap tokens and cheap
memory, but they are the Ne meter — keep at least four per kingdom if you cut.

---

## 4. The iteration cycle

### What the owner does
Runs the current HTML on a phone, exports the run log (JSON), and brings it back.
Long runs are the constraint — anything under ~900 sim-days can't see a
carnivory sweep, which historically starts around day 800.

### What Claude does, in order

**Step 1 — copy the log locally first.**
Uploads have vanished mid-conversation more than once.
```
cp /mnt/user-data/uploads/evosim-log-*.json /home/claude/logs/
```

**Step 2 — confirm what actually ran.**
The log carries a `cfg` block. Check it before anything else, because config
patches sometimes don't get loaded and the run isn't what you think:
```python
d['version'], d['seed'], d['tick']/d['ticksPerDay'], d['cfg']
```

**Step 3 — run the digest.**
```
python3 analyze.py log1.json [log2.json log3.json]
```
Multiple files print the cross-seed table, which is the part that matters most.

**Step 4 — read it in this order, and stop early if a gate fails:**

1. **CONSERVATION** — matter drift and `caps seen`. A cap that binds means a
   bound is doing the selecting and nothing below is what it looks like.
2. **STATIONARITY GATE** — if it fails, gene means are a transient. Say so and
   do not compare them to another version.
3. **DEMOGRAPHY** — extinction flag; mean death age vs maturityAge; and
   **births per animal-lifetime**, which analyze.py does not yet compute:
   `aBorn / (mean N × animal-era days) × mean death age`. Below 1 means the
   population was never viable regardless of how well fed it looked.
4. **REFUGE** — `pLocked` p10/median, worst 30-day fall, `corr(aSize, pLocked)`.
5. **EFFECTIVE POPULATION** — inert-gene diversity trend.
6. **GENE FLAGS** — every `PINNED` line, classified by section 2a into
   magnitude / structural / correctly-pinned.
7. **ENERGY, ACTION BUDGET, TROPHIC LEDGER, HISTOGRAMS, LINEAGES.**

**Step 5 — write the scorecard against the previous version's prediction.**
State plainly which predictions hit and which missed. A missed prediction means
the diagnosis was wrong, not that the constant needs to be bigger.

**Step 6 — decide config vs code.**

- **Config patch** (a small JSON, ~700 tokens): any constant change. Emit as
  `{"kind":"evosim-cfg","formatVersion":36,"version":"<build>","base":"<build>",
  "note":"<diagnosis>","cfg":{...}}`. Loading a file with `cfg` and no terrain
  arrays assigns the constants and rebuilds from seed. Always put the diagnosis
  in `note` so the patch is self-documenting when it comes back in a log.
- **Code change** (a new HTML): only when the cost *shape*, a formula, or a
  mechanism has to change.

**Step 7 — ship, with a written prediction.**
One structural change per version. Falsifiable, named genes, named thresholds,
across 3 seeds. Then add a row to `LEDGER.md`.

### Hard rules

- **Never run the sim in a headless harness to test a change.** Far too
  compute-expensive, and short runs answer a different question — populations
  shift with every change, so end-state counts aren't comparable between
  versions. Syntax-check the script block, reason against the last log, ship the
  file. Profiling a *performance* change is the one exception, and even then
  measure a fixed sim-day count, not a tail. (This is rule 6b in the file
  header.)
- **Small turns.** Responses have failed to generate from doing too much at
  once. One change per turn, ship a runnable file each time.
- **Rationale lives in `LEDGER.md`, not in the source.** The source carries a
  one-line summary and a `[Lnn]` tag. At v0.36 comments were 24% of the file,
  paid on every read and every write, and parts had gone stale and were
  contradicting each other.
- **Never calibrate a constant against a statistic from a broken or superseded
  run.**
- Verify a change didn't alter the RNG draw sequence when it was only supposed
  to change measurement.

---

## 5. Standing scorecard

Check every version. This is the answer to "are we still on mission".

| | target | v0.36 | v0.42 (367 yr) |
|---|---|---|---|
| harmonic animal N | ≥ 500 | 100 | 91 |
| mean death age / maturityAge | ≥ 1.0 | 0.65 | **2.95** |
| deaths by age or predation | ≥ 20% | 0.07% | 1.83% |
| carnivory mean | ≥ 0.20 | 0.072 | **0.288** |
| flesh + carrion, share of intake | ≥ 5% | 0.1% | 0.85% |
| `aSeen` | ≥ 1.0 | 0.36 | **7.03** |
| non-graze action share | ≥ 20% | 3% | 3.8% |
| `pLocked` | 0.5–0.85 | — | 0.996 |
| inert-gene sd | rising | falling | flat |
| genes pinned at a bound | 0 | — | 14 |
| stationary at end of run | yes | no | no |

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
```

Genome strides: plant **48** (39 active + 9 pad), animal **64** (54 active + 10
pad). `FORMAT_VERSION` 36, unhooked from `VERSION` — bump only when the save
schema changes.

**Founder pool:** "Export founder pool" writes ~650 evolved genomes per kingdom.
Loading one makes founders draw from evolved genetics instead of random morphs.
This is the replication fix — fixed seed does *not* reproduce a starting flora,
because any code change shifts RNG draw ordering. **If a run reaches an omnivory
sweep, export the pool before stopping it.** That turns future short runs from
"too short to see it" into "long enough to test whether it holds".
