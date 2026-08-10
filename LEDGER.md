# evosim — design ledger

Rationale that used to live in the source. The build carries a one-line
summary and a `[Lnn]` tag; the full argument is here.

**Why this file exists:** at v0.36 the source was 24% comments (42.5 KB,
~11,800 tokens) paid on every read *and* every write of the app. Parts of it
had also gone stale and were contradicting each other — `accessOf` argued for
`k_reach 0.060` while CFG set 0.025 arguing against it, and the animal gene
header said 53 active when `A_ACTIVE` was 54.

**Rule going forward:** code comments say what a term *does*, present tense,
one line. Reasoning, history, and reversed decisions live here.

---

## Version log

One row per version. Prediction written **before** the run. No exceptions —
at Ne ≈ 100 an unpredicted result is indistinguishable from noise.

| ver | change | prediction | seeds | outcome |
|-----|--------|-----------|-------|---------|
| 0.36 | 13 changes (A1,A7-A9,B1,B3-B7,C1-C3) | none recorded | 1 | unattributable |
| 0.37 | plumbing + measurement only, no biology | `sel` signs stop contradicting the pinning data; ecology otherwise unchanged from 0.36 | 3 | **PASS.** Matter drift 0.000000% on all 3. Death counters now sum to total deaths. Logging path verified RNG-neutral (0 `rng()`/`gauss()` calls), so the changes cannot have moved the ecology. `sel` contradictions fell from ~30 to 2, and both survivors are real antagonistic selection. Runs were 885/661/495 d, all non-stationary; seed 5499 fauna went extinct day 385. |
| 0.38 | reach allometry: `reach = k*size^0.333`, k pivoted to 0.0731 | median `pLocked` >= 0.55 in >=2 of 3 | 1 (control arm only) | CFG patch path VERIFIED end to end — log cfg showed 0.025/1.0, export echoed both. Treatment arm still untested. Control at 805d: no extinction, harmonic N 87, pLocked 0.533, aSize still +25.4%/100d. |
| 0.39 | carnivory unblock: body radius on attack/scavenge reach, attack score linear in carnivory, stall + bail-out on pursuit | flesh+carrion >= 1% of animal intake; attacks/day > 1; no runaway predation collapse | 3 | headless 260d animal era: attacks 4447, kills 309, flesh+carrion **1.14%** of intake (was 0.1%) |
| 0.38x | reach allometry: `reach = k*size^0.333`, k pivoted to 0.0731 so reach is unchanged at founder size 5 | median `pLocked` >= 0.55 in >=2 of 3 seeds; no fauna extinction in 3 seeds x 900 d; `corr(aSize,pLocked)` weakens above -0.5 | 3 | |
| 0.47 | **six changes, external audit.** toxin model unified (L47-1); arbiter put in one currency (L47-2); confusion effect + `AN.risk` so grouping pays (L47-3); slot compaction + high-water trim (L47-4); memcpy+geometric mutation (L47-5); render throttle, tile-culled draw, precomputed cover, `P.h` cache (L47-6) | see the six predictions below | default-arm 3-seed set complete (1337, 4001, 4002); 3 `k_confusion:0` seeds | see Scorecard, 3rd pass — L47-1/2 still seed-dependent (2-of-3 leaning, not closed), L47-3's `actAppr` clean miss now 4/4, `socialAttraction` weaker than first pass suggested; L47-4/5/6 can't-tell; **k_confusion:0 isolation-arm finding complicated, not confirmed or refuted — seed 4002's short, subsidy-window default-arm run showed the same failure flavor as the isolation arm despite confusion being ON, confound too large to score either way** |
| 0.48 | performance/mechanical only, no ecological claim. Extinction halt fires now (was gated on `!CFG.animalReseedDays`, always false at default config) (L0.48-1); `CFG` aliased to a local `C` in `updatePlant`/`senseDecide`/`reachOf`/`carrionDigest`/`grazeYield`/`plantScore` — the two functions profiling found responsible for 58% of JS time, 17.5% of it in global-lookup builtins (L0.48-2) | trajectory identical to v0.47 for the same seed at the same tick (proves RNG-neutral by construction — no `rng()` call site touched, no formula changed); ticks/sec measurably higher on a fixed sim-day count; no gene mean or population statistic moves beyond seed noise | 1 exact-match (seed 1337, 300d) | **PASS.** 0 of 97 columns differ, all 60 samples, genes/events byte-identical between v0.47 and v0.48 on seed 1337. 315→322 ticks/s (contended, directional only). See `## v0.48` below. |
| 0.49 | performance/mechanical only, no ecological claim intended. `P.hi`/`AN.hi` are a high-water mark that only grows, so rebuildCanopy/buildPlantIndex/buildAnimalIndex/updatePlants/updateAnimals paid for a run's largest-ever population for the rest of the run even after a crash back down. All five now scan `P.occIdx`/`AN.occIdx`, compact occupied-slot lists maintained incrementally (L0.49-1) | ticks/sec rises at high population, falls or is flat at low/moderate population (bookkeeping overhead not yet repaid); matter conservation exact in both arms; **not** RNG-exact (order-sensitive scans + stagger reassignment) but no consistent directional bias across seeds | 2 seeds x 300d, uncontended (1337, 4001), both `k_confusion:0` | **Mixed, as predicted going in.** Seed 1337 (peaks ~15-17k plants): 320→248 ticks/s, **28% slower** — hi/occupied gap never exceeded ~1.8x in this window. Seed 4001 (peaks ~43-47k plants): 79→120 ticks/s, **52% faster**, matter leak (0.013%) disappeared entirely (0.000000%). Only 8-10 of 97 columns matched exactly on either seed; population outcomes swung hard in *opposite* directions per seed (1337: 361→2390 animal births, life support net firing 234→0 times; 4001: 1506→260 births, net already at 0 both times) — large, but not one-directional, consistent with RNG-path chaos rather than a systematic bias. See `## v0.49` below. |

---

## v0.37 changes

Measurement and process. **No biology was touched** — if the ecology moves,
one of these did something unintended.

| tag | change |
|-----|--------|
| L37-1 | **CFG patch files.** A file with `cfg` and no terrain arrays now assigns the constants and rebuilds from seed. `Export config` writes only constants that differ from the build defaults. A tuning iteration is a 2 KB JSON, not a 177 KB app. |
| L37-2 | **`FORMAT_VERSION` unhooked from `VERSION`.** It tracked the build, so every version bump invalidated every saved world. Frozen at 36 until the save schema actually changes. |
| L37-3 | **Founder pool.** `Export founder pool` samples ~650 standing genomes per kingdom (reservoir sampling). Loading one makes `seedFounders`/`seedAnimalFounders` draw from evolved genetics instead of random morphs around `START`. Fixed seed does *not* give a reproducible starting flora, because any code change shifts RNG draw ordering — so every version comparison to date was confounded with a fresh evolutionary history. Pool genomes are copied without `founderNoise`, or the warm start is thrown away. |
| L37-4 | **`sel` baseline corrected to the mature pool.** It was parents minus the *whole standing population* — adults compared against a pool that is 82% juveniles (animals) or overwhelmingly seedlings (plants), so any gene merely correlated with reaching adulthood read as a selection coefficient. Measured at day 200: 9 of 39 plant genes shift >10%, and `germinationDelay` shifts **+377** — larger than the +242 that was being reported as its selection coefficient. `geneRow` now also emits `nMature` and `matureMean`. |
| L37-5 | **`aSeen` accumulator moved above the MVT early return.** It was sampled only on thinks where an animal did *not* stay on its plant — a biased minority of a headline diagnostic. |
| L37-6 | **Death classification made mutually exclusive.** `pDeadAge`/`aDeadAge` incremented *alongside* one of the other three causes, so the counters would stop summing to total deaths the moment anything aged out — which is exactly the outcome v0.38 is trying to produce. |
| L37-7 | **Log sampled every 5 sim-days** (`CFG.logDays`), not every day. Nothing downstream reads daily resolution. |
| L37-8 | **Comment backlog moved to this file.** |

---

## v0.38 — reach allometry

**[L38-1]** `reachOf` was `k_reach * size`. `size` is a mass (`birth =
size*birthMassFraction`), and reach is a length. Every other mass-dependent
term in the build is already allometric — intake `mass^0.667`, upkeep and
attack damage `mass^0.75`, root uptake `mass^0.75`, plant height `mass^0.5`.
Reach was the only one at 1.0.

That matters because it set the arms race. Plants gain height as `mass^0.5`;
animals were gaining reach as `mass^1.0`. **The animal exponent was double the
plant exponent, so the refuge could only ever lose**, no matter how the
constants were tuned. Three v0.37 seeds agree: `corr(aSize, pLocked)` = -0.86,
-0.30, -0.97, and the seed whose refuge fell furthest is the one whose fauna
went extinct.

At `1/3` the plants win the scaling race, which is also what happens outdoors —
trees outgrow browsers. `k_reach` is pivoted from 0.025 to 0.0731 so reach is
*identical* at the founder size of 5; only the slope changes.

| size | reach 0.37 | reach 0.38 | access at h=0.11 |
|------|-----------|-----------|------------------|
| 5    | 0.125     | 0.125     | 0.595 -> 0.595 |
| 10   | 0.250     | 0.158     | 0.922 -> 0.746 |
| 13.2 | 0.330     | 0.173     | 0.964 -> 0.795 |
| 16   | 0.400     | 0.184     | 0.980 -> 0.824 |

The exponent is `CFG.reachMassPow`, so every future adjustment to it is a
config patch, not a build. `control-v0_37-reach.json` reverts it to the linear
form for the control arm.

**Rejected in favour of this:** making growth `k_grow * mass^0.667`. The audit
proposed it to give size a demographic brake, but the three v0.37 seeds show a
size brake already exists — starvation, which reversed `aSize` from 6.66 to 4.5
in seed 4491. The brake works; it just engages *after* the refuge is gone. A
flat metabolic tax on size would not have changed that ordering.

---

## v0.39 — carnivory unblock

Three edits, all the same class of bug: attacking was harder than grazing for
reasons that were not biological.

**[L39-1] Body radius.** `radiusOf(i) = k_bodyRadius * mass^(1/3)`, a length, so
the same cube-root rule as reach. Attack and scavenge reach are now
`biteRange + radiusOf(self) + radiusOf(target)`. Before this, nothing in the
world had a body: a grazer's reach was `biteRange` **plus the plant's canopy
radius** (~3.8 units) while an attacker got `biteRange` alone (~0.98) against a
target that moves — and `steer` caps closing speed at `dist*turnCap`, so the
last unit is the slowest. Two size-13 animals had to occupy nearly the same
point to interact.

**[L39-2] Attack score linear in carnivory.** It was
`sc = (meat - risk) * aggression * ...` with `meat ∝ carnivory`, so the score
was proportional to **carnivory × aggression** — two near-zero founding genes.
That is the exact failure the C1 note says it fixed, one factor over.
Aggression now discounts the *retaliation* term instead
(`risk *= 1 - 0.9*aggression`), which is what a bold animal actually does, and
the score is linear in carnivory.

**[L39-3] Pursuit escape hatches.** The pursuit block returned before the hunger
and threat checks with nothing but `pursuitPersistence` (up to 500 ticks) to end
it. An animal that picked ATTACK could lose a sim-day for nothing — real
purifying selection on aggression, which duly sat at 0.097. It now breaks on
`stallLimit` or on dropping below `pursuitBailEnergy` days of reserve. `stall`
is also incremented in the ATTACK, SCAVENGE, and APPROACH branches; it was only
ever incremented in GRAZE, so `stallLimit` protected grazers alone.

**Measured, headless, 260-day animal era:** attacks 50 → 4447, kills 6 → 309,
flesh+carrion 0.1% → **1.14%** of animal intake.

**Confounded with v0.38's reach allometry**, which has still only been run as a
control. `control-v0_37-reach.json` still isolates it.

---

## v0.42 — performance

Fixed 330-day run: **82.1 s -> 61.6 s (1.33x)**, and the end state carries 86%
more plants (6,178 -> 11,519), so the per-organism gain is larger than 1.33x.
Profiled first, not guessed: `updatePlant` was 44% of total runtime.

| tag | change | was |
|-----|--------|-----|
| L42-1 | Beer-Lambert walk precomputed per (tile, band) in `rebuildCanopy` into `W.canopyI` / `W.canopyR` | 8 bands x `Math.exp` per plant per update |
| L42-2 | `p75(x) = sqrt(x)*sqrt(sqrt(x))` replaces `Math.pow(mass, 0.75)` at 4 sites | 17% of `updatePlant` alone |
| L42-3 | `refreshTimeCache()` at the top of `tick()` caches `W.seaSin` and `W.lightMulNow` | per-tick trig evaluated once per plant; season sin was 6.4% of `updatePlant` |
| L42-4 | `P.leaf[]` caches `leafArea`, written in `updatePlant`, read by `rebuildCanopy`, grazing and the renderer | 10% of total, recomputed 3x per plant per tick |

**NOT purely a performance change.** L42-1 alters results slightly: the old
per-plant walk applied the `if (bl < leaf) bl = leaf` correction in *every*
band it passed through, so a large plant inflated interception in bands above
itself. The precomputed version applies it only in the plant's own band. That
is more correct, but it is a behaviour change and it is most of why standing
plants nearly doubled.

**Next available perf win, not taken:** `PGENES` is 71 for 39 active genes and
`AGENES` is 85 for 54. The allocation lines in `updatePlant` (a0-a3) profile at
16% and are pure scattered genome reads across a 284-byte stride. Cutting the
padding would roughly halve that memory traffic, but it changes the save schema
and needs a `FORMAT_VERSION` bump.

---

## v0.43 — halt, climbing reach, widened rails

Built on the v0.42 long runs: seed 3012 (367 sim-yr) and seed 6175 (192 sim-yr).

**[L43-1] Terminal halt on fauna extinction.** Seed 6175's animals died at
day ~3900 and the run continued for 3,800 more animal-free days — half the run
producing nothing. If the reseed net is off and the fauna has been gone for
`CFG.haltAfterDays` (200), the run pauses and logs `run-halted-fauna-extinct`.

**[L43-2] `climbing` now extends reach:**
`reach = k_reach*size^0.333 * (1 + k_climbReach*climbing)`, `k_climbReach 4.0`.

The v0.38 reach allometry fixed refuge *collapse* and created refuge *totality*.
At v0.42 day 14695: plant `height` gene raced to 0.741 of its range while
`size` only reached 3.69, giving effHeight 0.653 against reach 0.113 — so
`access = 1/(1+(h/r)^3)` = **0.005** and `pLocked` = **0.996**. The entire fauna
lived on 0.4% of plant biomass, which starved it to extinction in one of the
two long runs and left the other one lucky rather than stable.

`climbing` only ever affected terrain drag, so it was decoration on a
one-dimensional race that plants win outright. It is now a second axis, it uses
a gene already under weak positive selection (0.134 -> 0.346), and it is
bounded by the `k_climbC*climbing^2` cost that already exists.

**[L43-3] Rails widened.** Gene COUNT and ORDER are unchanged, so founder pools
and saves still load and `FORMAT_VERSION` stays at 36.

| gene | was | now |
|------|-----|-----|
| size | .5–16 | .5–**24** |
| acceleration, turnRate | .01–1 | .01–**4** |
| senseRange | 1–60 | 1–**200** |
| toxinResistance | 0–1 | 0–**3** |
| herbivory | 0–1 | 0–**2** |
| hungerUrgency, plantAttraction | 0–1 | 0–**3** |
| climbing | 0–1 | 0–**2** |
| metabolicRate | **.3**–3 | **.1**–3 |
| maturityAge | **2000**–200000 | **300**–200000 |
| birthMassFraction | **.02**–.5 | **.002**–.5 |
| mutationRate | **.002**–.5 | **.0002**–.5 |

At 367 sim-years fourteen genes sat pinned at a declared bound. Design note 8
says whatever caps the population does the selecting — at that point the bounds
*were* the ecology. This is the precondition for measuring anything, not a
tuning choice.

**Measured, headless 330 d:** animals 173 -> **1442** at the same day, plants
5963. `pLocked` is no longer total. Cost: 187 -> 380 ms/sim-day, but that is
8x the animal population, so per-organism it is faster.

---

## v0.44 scorecard, and v0.45 / v0.46

**v0.44 hit 4 of 6.** `senseRange` (cubic vs area), `toxinResistance`
(asymptotic protection), `acceleration` and `turnRate` (3x constants) all came
off their rails. Toxin cost fell 29.9% -> 17.2% of intake. Matter drift back to
0.000000%.

**Failed:** `herbivory` only 99% -> 90% at max; `maturityAge` still 98% at min.

**Own goal:** `size` collapsed 5.07 -> 1.09 with **81% pinned at min**. Three
forces pushed down and nothing pushed back — intake `mass^0.667` vs upkeep
`mass^0.75`, newborn provisioning `offspringInvestment*nbUp` giving a tiny
newborn the same DAYS of reserve as a big one, and v0.44's maturity mass gate
making large size slow to breed. The gate then disabled itself: once size hit
1.09, `mass >= 0.6*size` became trivial, which is why `maturityAge` stayed
railed.

| tag | change |
|-----|--------|
| L45-1 | **`a_base` is no longer mass-scaled.** It sat inside the capability group and got multiplied by `m75/upkeepRefM75`, so it was not a floor at all — it shrank with the animal. Now a genuine fixed per-animal overhead: roughly unchanged at mass 5, ~2.8x heavier at mass 1. This is why there is no mammal smaller than a shrew. |
| L45-2 | **`k_gut` 0.008 -> 0.020.** Right shape, wrong size: a digestion benefit applying to 99.2% of intake outpriced it. Now the largest capability term, which is what a gut is. |
| L46-1 | **Genome padding cut.** `P_PAD` 32 -> 9 (stride 71 -> **48** = exactly 3 cache lines), `A_PAD` 31 -> 10 (85 -> **64** = exactly 4; 85 straddled at 5.3). Frees 11 MB. Nothing reads the pad — `mutateInto`, `geneRow`, `poolOf` and every genome access are bounded by `P_ACTIVE`/`A_ACTIVE`. **Founder pools and world saves still load**: pools store active-length rows, saves store terrain only. `FORMAT_VERSION` stays 36. |

### Deliberately NOT done

- **Plant height superlinear cost.** Proposed off the v0.42 long runs where
  height was 30% of plant upkeep. In the v0.44 run it is **10%** and `pHeight`
  is 0.339, not railed. Acting on it now would break rule 7 — calibrating a
  constant against a statistic from a superseded run.
- **Matter leak.** 0.0157% in v0.42, **0.000000%** in v0.44. Either fixed
  incidentally or the run was too short to show it. Watch it on the next long
  run rather than hunting a leak that may not exist.

### Still open, deliberately not fixed in 0.37

These are v0.38+ and each needs its own version and prediction:

- `size` runaway — 5.67 → 13.2, 22% pinned at the ceiling. Growth is
  multiplicative (`mass*0.02+0.01`), so time-to-maturity is scale-invariant at
  ~73 ticks and the A8 demographic brake does not exist. Candidate: make growth
  `k_grow * mass^0.667`.
- Attack reach. `GRAZE` gets `biteRange + canopy radius` (≈3.8); `ATTACK` and
  `SCAVENGE` get `biteRange` alone (≈0.98) against a moving target. There is no
  body radius anywhere.
- Attack score is `∝ carnivory × aggression` — still quadratic in two
  near-zero genes, the exact failure C1 says it fixed, one factor over.
- `AN.stall[i]++` appears only in the `GRAZE` branch, so `stallLimit` never
  protects an attacker, scavenger, or fleeing animal.
- Plant `photoCost` is 61-70% of plant upkeep for an entire run and is charged
  on leaf whether or not that leaf receives light.

---

## Extracted rationale

### [L01] — line ~249

`const VERSION = '0.37.0', FORMAT_VERSION = 36;`

FORMAT_VERSION tracks the SAVE SCHEMA, not the build. Bumping it with every
version invalidated every saved world, which is why no run has ever started
from a warm state. Bump it only when save()/load() field layout changes.

### [L02] — line ~313

`k_stem: 1.50,          // canopy given up per unit of realized height`

WAS 250, which no plant ever reaches: realised mass runs 6-90 and P90 12-115,
so sqrt(m/250) stayed at 0.05-0.68 and 97% of every flora sat in canopy band
0. Eight bands of layered Beer-Lambert with one band occupied is not layered
light, and height was 0-1% of plant upkeep because nobody could afford to be
tall enough for it to matter.

### [L03] — line ~337

`founderNoise: 0.8,`

in MUTATION SIGMAS. Scaling by gene range instead drew seedEnergy below the
germination cost and made whole morphs sterile. 0 = old single-ancestor
behaviour.

### [L04] — line ~352

`plantStagger: 8,`

is named and recorded. Without it an outlier genome spawned a named lineage
instantly, took a slice of its neighbour for one pass and died: 70 plant names
in 50 years of which 35 lived a single snapshot, and a tree of 240 entries
under 107 distinct pairs. 5 passes at lineageEvery 960 is 10 sim-days.

### [L05] — line ~376

`visMass: 4.0,          // plant mass at which a plant is half as finda`

0 disables height-limited browsing entirely. ANCHORED, NOT GUESSED: 0.025 =
1/AMAX(size), so the largest animal the gene table allows can just browse a
plant at full genetic height. Design 6.4 requires the arms race to be winnable
at both extremes and that fixes the constant. 0.060 came from calibrating
against a mean effHeight measured in a COLLAPSED world — a sparse stand of old
survivors — and gave aAccess 0.66-0.98 and pEscape 0.00 in three seeds.

### [L06] — line ~386

`mvtLeave: 1.0,         // leave a plant yielding less than this x the`

an infinite one. Detection had NO size term, so a 0.5-mass seedling was as
visible as a 184-mass tree — which is why 100% of recruitment was eaten.

### [L07] — line ~407

`corpseMin: 0.04,       // below this a corpse is gone and the slot fre`

WAS 0.0025 — a half-life of 0.58 sim-days, at which 97% of all corpse mass
rotted unfound (1.4 mass/day eaten against ~40 rotting) and carrion delivered
0.14% of animal energy intake.

### [L08] — line ~414

`energyPerMassA: 55.0,  // energy to build one unit of animal mass. mea`

SLOPE, not a clamp — see carrionDigest(). As max(carn, floor) it made every
carnivory below 0.30 worth exactly the same, so the gene that carrion exists
to bootstrap had no gradient to climb and sat at 0.0127 with 92% of the
population at its minimum. Scavenging is the stepping stone to predation and
it cannot be gated behind the gene it is meant to start.

### [L09] — line ~425

`biteMassPow: 0.667,    // A7/CURVATURE. Was 0.75, which is exactly the`

PIVOTED, NOT RAISED. 0.013 x 5^0.75 / 5^0.667 holds intake exactly constant at
the founder size of 5, so v0.36 changes the SHAPE of the size/intake curve and
not its level. Dropping the exponent alone would have cut intake ~12% at
founder mass against a surplus of only 12-25% of upkeep — a magnitude change
smuggled in beside a structural one, which is what makes the next log
unreadable. Small animals now gain (+12% at 1.25), large ones lose (-9% at
16).

### [L10] — line ~435

`k_toughBite: 3.0,`

on a_mass in animal upkeep, so intake and the dominant maintenance term
cancelled and `size` was metabolically free. Only
k_move/k_accel/k_turn/k_armourC scale as mass^1 and they are ~10% of upkeep,
so size ran away in all three v0.35 seeds (4.6->9.7, 3.6->10.5, 3.2->13.0)
while the reach benefit saturates. A bite is geometric — gape scales with
length^2, i.e. mass^(2/3) — while maintenance is metabolic (Kleiber m^0.75).
Splitting them is the physically correct fix and gives size the upward-curving
net cost the curvature rule requires. Do NOT "fix" this by breaking Kleiber on
upkeep.

### [L11] — line ~547

`const AG_DEF = [`

2b. ANIMAL GENE TABLE — LOCKED. 53 active + 32 padding = 85 slots. Indices
0-30 physical, 31-52 behavioural. Behavioural genes are arbiter WEIGHTS, not
capabilities: a bad weight causes bad decisions, which is self-limiting, so
they carry no cost terms. Charging them would double-charge. Cost shapes on
the physical genes follow design 6.1 — every one of them curves up faster than
its benefit.

### [L12] — line ~555

`['size',              .5,      16,   1.2,    5   ],`

A9/DRIFT. Was .2-40. mutateAnimal CLAMPS to [min,max], and a clamped random
walk migrates toward the middle of its declared range, so a 0.2-40 range put a
permanent pull toward 20.1 on a founder of 5. With harmonic-mean population
2-13 in v0.35 that pull beat selection outright: size went 4.6->9.7,
3.6->10.5, 3.2->13.0 in three seeds, and buildE = size*birthMassFraction*55
carried the runaway straight onto the price of an offspring. The range is a
statement about plausible morphospace, not a safety margin; 0.5-16 centres on
8.25 and stops the range itself from doing the selecting. Widen only with a
reason, and never asymmetrically about the founder.

### [L13] — line ~617

`['climbing',           0,       1,   .04,   .10 ],`

53 — takes the first reserved padding slot. Indices 0-52 unchanged, so old
logs still read correctly; the ACTIVE COUNT changes, so fossil records and
saved genomes from before v0.29 are not comparable.

### [L14] — line ~712

`pReseed:0, aReseed:0,                    // life support, so it cannot`

starved: aDeadAge counts only the hard 3x-lifespan cutoff and read zero across
50 years while 37% of deaths sat in the oldest age bin

### [L15] — line ~721

`function rankNormalise(f){`

Steep ground is slow ground unless you can climb it. Below the foothills
terrain is free; above peakElev nothing passes at any climbing skill. Remap a
field so its values are its own RANKS, i.e. exactly uniform on 0..1. Value
noise clusters around its mean and its extremes move with the seed, so a fixed
threshold cut a different fraction of every world — 94% habitable in one run,
43% in the next. After this, every threshold is a share of the map and terrain
proportions are identical across seeds while the terrain itself stays
completely different.

### [L16] — line ~751

`function rebuildFertility(){`

Fertility gates germination and scales growth. Zero above the tree line.
Derived entirely from elev and arid, so a load can rebuild it rather than
inheriting whatever fertility the previous world left in memory. Habitable is
fert > germFertMin, the same threshold germination uses — it was 0.10 against
a germFertMin of 0.08, so habFrac understated the world.

### [L17] — line ~787

`const ez = valueNoise(n, 2, 3, 0.45);`

---- terrain. Elevation is RIDGED noise: 1-|2v-1| peaks along the 0.5 contour
of a smooth field, and contours are lines, so the high ground comes out as
ranges instead of blobs. Aridity is an independent field, so you get dry
lowlands and wet uplands rather than one gradient.

### [L18] — line ~831

`function diffuse(){`

Symmetric pairwise flux, weighted by the POORER of the two tiles. Written this
way rather than as a Laplacian because every flux is added to one tile and
subtracted from the other in the same statement, so a variable rate cannot
break conservation the way a per-tile stencil would. Soil therefore creeps
through barren ground instead of equalising across it, and a desert stays
soil-poor rather than quietly filling from its neighbours with nutrient
nothing there can use.

### [L19] — line ~939

`function drawMorphs(nMorph, ACTIVE, START, SIG, MIN, MAX){`

A world used to start as one genome stamped out N times, so every lineage it
ever had was invented by mutation from a single point. Now it starts from
several distinct morphs. Draws are centred on the ancestral value and scaled
by morphSpread rather than being uniform over the range, so the founders are
varied without being nonsense.

### [L20] — line ~958

`const POOL = { plant:null, animal:null };`

FOUNDER POOL. When loaded, founders are drawn from an EVOLVED genome set
exported from an earlier run instead of from random morphs around START. Fixed
seed does not give a reproducible starting flora, because any code change
shifts RNG draw ordering — so every version comparison was confounded with a
completely fresh evolutionary history. A shared pool removes that. Null =
ancestral behaviour. [L37-3]

### [L21] — line ~1067

`const buildE = CFG.seedlingMass*CFG.energyPerMass*CFG.germCostMult;`

Building tissue costs energy everywhere else in this model; it has to cost
energy here too, or a seed mints biomass and the whole plant economy is a
fiction. A seed that cannot pay never will — its energy only decays — so it
dies rather than squatting on a slot forever. nothing germinates on bare rock
or above the tree line

### [L22] — line ~1128

`(top level)`

B2+B3: disposable soma, as the animals have always had. Without the senescence
divisor, lifespan was linear/linear and senescenceRate was a tax with no
benefit at all — both pinned to their minima, measurably.

### [L23] — line ~1146

`(top level)`

MUTUALLY EXCLUSIVE chain: recent grazing marks "eaten", past lifespan marks
senescence, everything else is shaded out. pDeadAge used to increment
ALONGSIDE one of the other three. [L37-6]

### [L24] — line ~1196

`const dEn = surplus*a1;`

DEFENCE. allocDefence finally has a job: realized defence is what the plant
actually paid for, over what its genes ask for. Costs are quadratic in each
gene per 6.1, and scale with the mass being protected.

### [L25] — line ~1239

`const AN = {`

6b. ANIMALS — struct of arrays, tile index rebuilt every tick. Phase 3 is
herbivory only: GRAZE / APPROACH / REST / WANDER. Attacking, corpses, carrion
and mating wait for phases 4-5; those genes drift.

### [L26] — line ~1273

`function killAnimal(i){`

Death returns body mass AND undigested gut to the tile. Matter closes here.
Death leaves a body. Scavenging is the stepping stone to predation, so there
has to be something to scavenge. Gut contents go straight to the soil; the
flesh stays until it rots or is eaten. Matter is conserved on both paths —
nothing here creates or destroys mass.

### [L27] — line ~1356

`const UPK = new Float64Array(9);`

Upkeep composition, sampled from 1 plant in 64. I had to reconstruct this
arithmetic by hand to find out that height cost 9% of upkeep and bought total
grazing immunity; the log should never make that necessary again.

### [L28] — line ~1361

`const SELP = { acc:null, n:0 }, SELA = { acc:null, n:0 };`

FECUNDITY differential accumulators: the mean genome of everything that
reproduced, offspring-weighted (1 birth in 8 is sampled). Minus the MATURE
mean this is the fecundity component of S. It is NOT the whole selection
differential: viability selection is excluded, and viability is 100% of animal
mortality and 65% of plant mortality. Read it as "who is breeding", never as
"which way is this gene going". [L37-4]

### [L29] — line ~1375

`function reachOf(g){ return CFG.k_reach*Math.max(0.05, AN.genome[g+AG.`

Net worth of one plant to one grazer, per tick of grazing. Used both when
choosing a target and when deciding whether to keep the current one, so the
two can never disagree. Carries all three defences: toughness -> bite RATE,
fibre -> digestion, toxicity -> harm. How much of a plant a given animal can
physically get at. A seedling is wholly available to anything; a tall plant
keeps its crown out of reach. Graded rather than binary so height has a
gradient to climb. LINEAR in size, so the biggest animals can browse the
tallest plants. A sublinear exponent puts a ceiling on reach that plant height
simply walks past, and then every plant is safe forever.

### [L30] — line ~1388

`const r = reach \|\| 1e-6, h = effHeight(j*PGENES, P.mass[j])/r;`

CUBIC, not quadratic. A Lorentzian starting at 1 decays immediately, so the
first cut taxed every plant instead of protecting tall ones. The SHAPE was
never the problem; the SCALE was. At k_reach 0.0175 the population sat at h/r
6.6, out on the dead tail where access is 0.003 and nothing an animal can do
about its own body changes that. Everything it ate was a seedling, where
access is ~1 and flat, so size saw only cost and fell 2.96 -> 1.63, which made
the tail worse. k_reach 0.060 puts the operating point near h/r 1-2, where
this curve has its steepest gradient and the arms race is live in both
directions.

### [L31] — line ~1400

`function carrionDigest(carn){`

Energy per tick this animal would actually get from this plant, all three
defences and reach included. The arbiter and the MVT test share it, so what an
animal chooses and what it then earns can never disagree. Poison saturates: it
can spoil a meal, not bankrupt the eater. Shared by the target score, the MVT
yield and the bite, which were three separate expressions of the same idea and
could quietly disagree with each other. CARRION DIGESTIBILITY. A SLOPE, NOT A
CLAMP (design 6.1). Same 0.30 at carnivory 0 and the same 1.0 at carnivory 1
as max(carn, floor) gave, but with a gradient the whole way, so the first rung
of the 7.2 ladder exists.

### [L32] — line ~1415

`function satiateBite(i, g, perMass){`

SATIATION. `AN.energy` was never bounded, so `energyCapacity` named a capacity
it did not enforce — animals ran at three times their own cap and went on
eating. `hunger` scales the arbiter SCORE, never the BITE, so a full animal
that still ranks GRAZE highest ate at full rate forever and grazing pressure
had no upper limit of any kind. A bite may now deliver only the energy there
is room to store; the mass stays on the plant otherwise, which keeps both
ledgers honest. `perMass` is the energy one unit of that food is worth to THIS
animal, so a bad digester is limited less, not more.

### [L33] — line ~1440

`function plantScore(j, d, herb, fibreTol, toxRes, pa, hunger){`

MARGINAL VALUE THEOREM, properly: choose a patch by its expected gain, leave
it by its marginal rate. gain = patch/(travel + patch/rate), which tends to
the rate for a big patch and to patch/travel for a small one. This shares
every expression with grazeYield, which the previous version only CLAIMED to
do: it scored a plant by min(1, mass/10) while the yield is bite-rate limited,
so animals walked to big plants they could not eat and abandoned them 2.25
million times — 6.3 per animal per day. UNITS WARNING. Since v0.32 this
returns an MVT gain in ENERGY PER TICK, while SCAVENGE, ATTACK, APPROACH,
WANDER and REST all return dimensionless weights. They happen to balance
within a factor of two at the current constants. Any change to tissueValue,
gutCapMult or k_intake rescales GRAZE against every other action silently. If
the arbiter ever needs retuning, put all seven scores in the same currency
first.

### [L34] — line ~1481

`const cap = Math.max(1e-6, G[g+AG.energyCapacity]*AN.up[i]*CFG.ticksPe`

capacity is DAYS OF UPKEEP, not mass. Denominating it in mass gave a founder a
capacity of 3.75 against 40 starting energy, so it converted its entire
reserve into body mass and starved — the v0.3.1 plant bug, other kingdom.

### [L35] — line ~1486

`let dp = Math.abs((W.tick % CFG.ticksPerDay)/CFG.ticksPerDay - G[g+AG.`

C2: an animal has a preferred time of day. On-phase it senses well; off-phase
it rests better (applied in updateAnimal). Diurnal versus nocturnal becomes a
real niche axis, and it is a pure tradeoff.

### [L36] — line ~1504

`const p = AN.tgt[i];`

A hunt has to survive re-deciding. pursuitPersistence has sat unread in the
genome since phase 3; without it an attacker abandons every target within a
think-tick and can never finish one.

### [L37] — line ~1516

`for (let c = 0; c < TOFFD.length && (found < CFG.senseCap \|\| foundA < `

Plants and animals get SEPARATE detection budgets. Sharing one cap meant a few
plants in the nearest tile exhausted it before any animal was ever looked at,
so in a green world no animal could see another one at all — and scavenging,
the stepping stone to predation, could never start.

### [L38] — line ~1533

`const pm = P.mass[j], vis = pm/(pm + CFG.visMass);`

A plant's visibility scales with its bulk. Without this term a 0.5-mass
seedling was exactly as findable as a 184-mass tree, and since seedlings were
the only thing in reach, every recruit died.

### [L39] — line ~1543

`for (let k = AIDX.start[t]; k < AIDX.start[t+1] && foundA < CFG.senseC`

Animals are always scanned now, not only when social. Four things can be
scored off one detection: herd-mate, prey, corpse, threat. Which one wins is
decided entirely by genes — there is no predator flag anywhere.

### [L40] — line ~1553

`const still = AN.sp[j] < 0.02 ? G[og+AG.ambushTendency] : 0;`

camouflage finally does something: it is a detection roll, not a damage
reduction. Until phase 4 it was a cost with no benefit. C3: sitting still
hides you. An ambusher pays for it in ground covered.

### [L41] — line ~1587

`const meat = carn*CFG.meatValue*(0.5 + G[g+AG.meatAttraction])`

C1: meatAttraction WEIGHTS the value of meat rather than gating the action.
Gating it multiplied two near-zero genes and made attack unreachable; a
0.5-1.5 weight cannot do that.

### [L42] — line ~1608

`const cur = AN.tgt[i];`

Marginal value theorem: stay while this plant beats your own running mean
intake. Comparing against the best plant in VIEW was noise, since detection is
stochastic; comparing against your own recent earnings is both principled and
self-damping, because a poor world lowers the bar. ACCUMULATED BEFORE THE MVT
RETURN. It used to sit after it, so aSeen was sampled only from the minority
of thinks where an animal did NOT stay on its plant — a biased subsample of a
headline band.

### [L43] — line ~1642

`const dist = Math.sqrt(dx*dx + dy*dy);`

Turning radius is speed/turnCap. If it exceeds the distance to the target the
animal orbits forever and starves — which is exactly what they were doing. Cap
approach speed so the circle fits: you must slow down to turn tightly, which
is how turning actually works.

### [L44] — line ~1675

`const acc = accessOf(tgt, reachOf(g));`

realised access, logged: pEscape is a binary against median reach, this is the
browse fraction actually achieved, which is the number that says whether the
standing crop is food or scenery

### [L45] — line ~1762

`const drag = terrainDrag(t, G[g+AG.climbing]);`

--- move. Steep ground drags, peaks are a wall. An animal that walks into a
mountain turns along it rather than sticking, so ranges deflect movement
instead of collecting a rim of trapped animals.

### [L46] — line ~1788

`const capability = CFG.a_base`

Capability costs: the price of OWNING an organ, which in a real body scales
with the body. Left flat, these are a tax that a juvenile cannot pay out of
m^0.75 of an adult intake — and 73-85% of deaths were juveniles. k_bite is in
here rather than /sqrt(mass); see the header.

### [L47] — line ~1835

`const birth = G[g+AG.size]*G[g+AG.birthMassFraction];`

A8: GROWTH IS SUBORDINATE TO BREEDING ONCE MATURE. Growth used to fire at
cap*0.5 while reproduction waited for matingThreshold*cap, and matingThreshold
sat at its 0.60 founder value in all three v0.35 seeds. Growth therefore
triggered at a strictly lower energy than breeding and drained the pool every
time it filled — and since it can absorb ~6 energy/tick against an observed
surplus of ~0.03, it took all of it. mass/size stuck at 0.53-0.75, so room>0
was permanently true and reproduction was unreachable: mean standing energy
was below even the growth gate in 2 of 3 seeds, lifetime output 0.33-1.00.
Juveniles grow at the old gate; adults may only grow on energy ABOVE the full
reproductive requirement. This also gives `size` a second, demographic cost —
a bigger adult size is a longer juvenile period spent at risk of starving
before breeding once — which is the term that was missing from the runaway.
The true bar is the whole clutch cost, not matingThreshold alone: an adult
parked between the two would otherwise grow itself back down to the lower one
forever and never fund a single birth. Hoisted so both gates read it.

### [L48] — line ~1872

`let want = G[g+AG.offspringCount]\|0;`

birth / nbUp / invest / buildE are hoisted above the growth block (A8) so
growGate can read the real clutch cost. Kept here as comments only. RESERVES
ARE UPKEEP-DAYS, NOT ENERGY. Plant storage and the animal energy cap were both
fixed versions ago; this was the one site left in raw energy, and selection
duly drove it to 0.763 against an upkeep of 0.0423 — eighteen ticks of life
for a newborn. 84% of all animal deaths landed in the first quarter of
maturity and aBorn tracked aDeadStarve exactly. The newborn's own upkeep is
the parent's by Kleiber, which is the only estimate available before it
exists. A1: building a body costs energy here exactly as it does when a plant
grows or a seed germinates. Taking the matter from the gut closed the matter
ledger and hid this for thirty versions, but the tissue was being minted free,
and free offspring are why the fauna was nothing but newborns starving faster
than they could be replaced.

### [L49] — line ~1931

`const need = CFG.reseedFloor - P.live;`

The nets are LIFE SUPPORT and were invisible in the log. Three runs held
135-190 animals to the day the net expired and then died, which reads exactly
like a population living off carrion. Count every propped body.

### [L50] — line ~1952

`const MAXLIN = 12, LHN = 120;`

7. LINEAGES — instrumentation, NOT species. Both kingdoms. Online centroid
clustering over a morphology subset. Reproduction is clonal until phase 5, so
there are no reproductive barriers to draw a boundary at; phase 5 swaps the
distance test for the reproductive one and the bookkeeping here stays.
Labelled "lineages", never "species".

### [L51] — line ~2000

`function linName(S, a){`

Names were only de-duplicated against LIVE lineages, so a dead cluster's name
went back in the pool: 240 tree entries under 85 names, 'Melthys' fourteen
times. The tree exists to record ancestry and could not tell two clusters
apart. `used` persists for the life of the run.

### [L52] — line ~2012

`let out = nm, q = 2;`

The base name is a hash of the centroid, so a morph that re-emerges in the
same region of gene space keeps its family name and the serial says which
instance it is.

### [L53] — line ~2044

`// nearest CONFIRMED cluster is the parent: this genome budded off it`

PROVISIONAL. No name, no tree entry, no place in linP until it has held minPop
for lineageConfirm consecutive passes. A cluster seeded from one outlier
genome and published in the same instant is how the tree came to record
"Corvell from Nother" eleven separate times.

### [L54] — line ~2055

`const cur = lin[i];`

Stickiness. Reassigning from scratch every pass let two nearby centroids in a
continuous distribution trade hundreds of members back and forth, which is why
a named lineage swung between hundreds and zero. You keep your lineage unless
something is clearly closer.

### [L55] — line ~2375

`function drawCorpse(i, z, amb, pad, offs){`

Trophic colouring, ready for phase 4: green herbivore through to red
carnivore. A corpse reads as a dull, desaturated disc — it must be visibly NOT
an animal, because watching scavengers gather on one is the phase 4 spectacle.

### [L56] — line ~2859

`function linTrait(v, mean, lo, hi){`

A lineage described in words. Built from the cluster centroid against the
kingdom mean, so it says what makes THIS lineage different, not what every
organism happens to be. Absolute terms where they carry meaning (a diet is a
diet), relative terms where they do not (large compared to what?).

### [L57] — line ~3010

`const LOGCAP = 4096;`

13. RUN LOG - telemetry for offline analysis, so a long run can be done in the
browser and the numbers taken away. Sampled once per sim-day; when the buffer
fills it is decimated in place and the interval doubles, so a run of any
length stays bounded and keeps its whole shape. Pure instrumentation: reads
state, never writes it, never draws PRNG.

### [L58] — line ~3056

`(top level)`

5 days, not 1. Nothing downstream reads daily resolution — the digest works on
~100-day windows, 200-sample tails and a last-third slope — and daily sampling
made the log 5x bigger than the analysis it feeds. [L37-7]

### [L59] — line ~3109

`let lockM = 0, totM = 0;`

pEscape counts PLANTS; pLocked weighs BIOMASS through the same access curve
the grazers actually face. In the v0.33 run pEscape read 0.21 while the adults
holding essentially all the standing crop sat at access 0.045.

### [L60] — line ~3124

`const gpm = i*PGENES;`

adults carry the canopy; the seedling churn is four times the count and none
of the leaf area, and reading them as one number hid that for thirty versions

### [L61] — line ~3175

`(top level)`

These are INTERVAL means from here on, not whole-run running means. They were
the latter, and their smooth monotone decline across an entire log was an
averaging artifact that read exactly like a population trend. NOT COMPARABLE
WITH ANY LOG BEFORE v0.32.

### [L62] — line ~3191

`function selRow(A, act, baseMean){`

Per-gene mean, spread and bound-occupancy. Occupancy at a bound with no spread
is the pinning failure of section 6.1, and it is only visible here. S = mean
genome of everything that reproduced, minus the population mean. Positive
means that gene is being pushed up right now. baseline MUST be the mature-pool
mean, not the standing-population mean.

### [L63] — line ~3209

`const mmean = new Float64Array(act);`

A SECOND MEAN OVER MATURE INDIVIDUALS ONLY. `sel` is parents minus a baseline;
taking the baseline over the whole standing pool compared adults against a
population that is 82% juveniles (animals) or overwhelmingly seedlings
(plants), so any gene merely correlated with reaching adulthood read as a
selection coefficient. germinationDelay reported sel +242 while 62% of
standing plants sat at its minimum — that was the stage confound, not opposing
selection. [L37-4]

### [L64] — line ~3271

`function logLineages(){`

Named lineage tracks and discrete events. The lineage panel names clusters
from a hash of their centroid, so the same name means the same genome
neighbourhood across the run and a rise-and-fall can actually be told.

### [L65] — line ~3386

`const CFG0 = Object.assign({}, CFG);`

CFG PATCH — the whole point of v0.37. A tuning iteration is now a 2KB file,
not a 177KB rebuild of the app. Only genuinely changed constants are written,
so the diff against the build defaults is readable. [L37-1]

### [L66] — line ~3398

`function poolOf(count, hi, stride, active, alive, genome){`

FOUNDER POOL — a sample of the standing genomes, so the next run can start
from evolved genetics instead of re-deriving basic viability from START.
Reservoir sampling: one pass, no allocation proportional to population.
[L37-3]



---

## v0.47 — external audit pass

Six changes in one version, which breaks the one-change rule on purpose and at
a cost: **L47-4/5/6 are performance only and cannot move the ecology, L47-1 is
a bug fix, and only L47-2 and L47-3 change biology.** Both of those are
switchable from a CFG patch, so the arms can still be separated:

- `{"cfg":{"k_confusion":0}}` disables L47-3 entirely (confusion divisor is 1,
  `AN.risk` stays computed but APPROACH scores 0, exactly as v0.46 behaved
  after socialAttraction was purged).
- L47-2 is **not** switchable. If it has to be isolated, run the k_confusion 0
  arm first.

Recommended order: run `k_confusion 0` on 3 seeds to score L47-1 + L47-2 alone,
then turn it on.

### [L47-1] — the toxin model was split-brain

The v0.44 asymptotic fix (`1/(1+tr)` replacing `(1-tr)`) landed in the realized
bite in `updateAnimal` and in **neither** scoring function. `plantScore` and
`grazeYield` both still used `(1-toxRes)`. They agree at `toxRes` 0 and diverge
from there: at 0.5 perception was 33% optimistic, at 1.0 it perceived *zero*
toxin while the animal was still charged half. Three consequences, all live in
every run since v0.44:

1. the MVT leave rule held animals on toxic plants past the point the rule was
   supposed to release them;
2. `toxinResistance` carried a perceptual benefit it never paid for, so the
   selection differential on it is part phantom;
3. the reported "toxin cost 29.9% -> 17.2% of intake" is contaminated — some of
   that fall is animals mis-scoring, not animals resisting.

This also violated the invariant L31 states outright: *the arbiter and the MVT
test share it, so what an animal chooses and what it then earns can never
disagree.* They disagreed for three versions.

**Prediction:** `aToxRes` mean falls relative to v0.46 (the phantom benefit is
gone) and `eToxin` share of intake **rises**, because animals now avoid toxic
plants honestly instead of eating them and paying. If `eToxin` falls instead,
the diagnosis is wrong.

### [L47-2] — one currency for the arbiter

L33 already carried a UNITS WARNING: GRAZE returns an MVT gain in energy per
tick, everything else returned a dimensionless weight, "they happen to balance
within a factor of two." That understated it, because **the imbalance is a
function of body mass**:

| action | scaling in the deciding animal's own mass |
|---|---|
| GRAZE | `mass^0.667` to `mass^1` — via `AGUT = mass*gutCapMult` and `ABITEC` |
| ATTACK | none — `sizeMatch` is a ratio, `min(1, omass/8)` is the target's |
| FLEE | `1/mass` — via `min(4, omass/mass)` |

So when `size` collapsed 5.07 -> 1.09 in v0.44, the *perceived* value of
grazing fell roughly 3x against hunting and 5x against fleeing, with no change
to any actual payoff. **Both omnivory sweeps happened alongside shrinking
size.** The headline result of the project may be part artifact.

Every score is now `gain/(travel + handling)` in expected energy per tick:

- **SCAVENGE** — `patch = min(corpse mass, gut) * carrionValue`, rate
  `AATKC * carrionValue`, travel `d/ASPD`. No armour, no retaliation, corpses
  do not run.
- **ATTACK** — same form, rate is flesh/tick net of armour, crowding and
  retaliation. Retaliation was a per-mass value subtracted from a per-mass
  value; it is charged per bite tick in the sim, so it now subtracts from the
  **rate**. Travel uses closing speed `ASPD - 0.6*prey maxSpeed`, so fast prey
  is far away in *time* — which is the whole point of running, and gives prey
  speed a selective handle it never had.
- **FLEE** — an avoided loss rate: flesh the threat removes per tick, valued at
  `energyPerMassA`, divided by own armour, discounted by time to contact. The
  spurious `1/own mass` term is gone.
- **APPROACH** — see L47-3.
- REST stays a hard override on `stam < restThreshold`. It is a physiological
  constraint, not an arbiter weight, and does not belong in the currency.

Behaviour genes keep their old job: `plantAttraction`, `meatAttraction`,
`carrionAttraction`, `fearThreshold`, `socialAttraction`, `preySizeRatio`,
`kinRecognition` are **weights on a real quantity**, never the quantity.

**Prediction:** non-graze action share rises from 3.8% toward 10%+; `aSeen`
unchanged (detection is untouched); carnivory mean does **not** collapse — if
it does, the v0.39/v0.42 sweeps were substantially the units artifact and that
result needs restating. Watch `corr(aSize, carnivory)`: it should weaken.

### [L47-3] — herding was impossible, not badly tuned

`socialAttraction` and `socialRadius` appeared **only as costs**. No dilution,
no vigilance, no confusion, no group defence — being near a conspecific changed
nothing about detection, predation or feeding. It was worse than neutral:
conspecifics consume the shared `senseCap` of 8 animal detections, so a herd
member was *less* likely to spot a predator or a corpse. And the gate
`if (socialAttraction > 0.02)` made the purge **absorbing** — one drift below
the line and the action was never scored again, so the gene could never be
retested.

Two changes, both physics:

1. **Confusion effect.** Attack rate divides by `1 + k_confusion*(n-1)` where
   `n` is the animal count in the target's tile. Applied in the ATTACK score
   *and* in the realized damage, so perception and payoff agree (L31). Nothing
   is told to herd; hunting into a crowd is simply slower.
2. **`AN.risk`** — a per-animal EWMA of the worst threat rate seen per think,
   in energy/tick. APPROACH now scores as the share of *your own* predation
   loss that joining a group of that size removes:
   `risk * crowd/(1+crowd) * socialAttraction * (1 - kinRecognition*(1-kin))`.
   With no predators `risk` stays 0, APPROACH scores 0, and `socialAttraction`
   drifts instead of being purged — which is the correct null.

`nNear` counts corpses along with the living (AIDX indexes anything with a
stage). Corpses are a small share and the bias is toward under-rewarding
grouping, so it is left alone; fix it if `k_confusion` ever needs calibrating.

**Prediction:** `socialAttraction` stops going to zero — mean above 0.05 and
`atMin` below 50% — **only in runs with real predation**. In a run where
carnivory stays near 0 it should drift, not sweep. `actAppr` above 1% of the
budget. If socialAttraction rises in a run with no attacks, the risk EWMA is
picking up threat that never materialises and the estimator is wrong.

### [L47-4] — slot high-water marks never retreated

`P.hi` and `AN.hi` only ever grew, so the canopy pass, both index builds and
the renderer stayed proportional to the largest seed bank the run ever held
rather than to what is alive. With `maxPlants` 90,000 and `seedSlotFraction`
0.60 that is up to 54,000 dead slots walked several times per tick, forever,
after one transient bloom.

Two halves: trim trailing dead slots at the top of `rebuildCanopy` and
`buildAnimalIndex`; and `compactFree()` every `compactEvery` ticks sorts each
free list descending so `allocSlot` pops the **lowest** index first and the
array actually stays compact. Order-only — no matter moves, no `rng()` is
drawn, and nothing physical depends on which slot an organism occupies.

**Prediction:** no ecological effect whatsoever. If any gene mean or population
statistic moves against v0.46 beyond seed noise, something in the build depends
on slot ordering and that is a bug worth finding.

### [L47-5] — inheritance was 39 (plant) / 54 (animal) rng draws per birth

One `rng()` and one clamped element copy per gene, for every seed and every
birth, when at the `mutationFloor` of 0.004 fewer than one gene in five
actually changes. Now: `copyWithin` (a typed-array memmove) for the whole
active block, then only the mutated indices, drawn from the geometric waiting
time of the same Bernoulli process — `k += 1 + floor(log(1-U)/log(1-rate))`.
Above `mutFastMax` 0.25 it falls back to the per-gene loop, where geometric
skipping stops paying.

The **distribution over which genes mutate is identical**. The draw sequence is
not — which is what the founder pool exists for, and is the reason a fixed seed
has never reproduced a starting flora across code changes anyway (L37-3).

**Prediction:** no distributional effect. Reproduction cost per birth falls;
the visible sign is ticks/sec at high seed counts.

### [L47-6] — six render and hot-loop cuts

| what | why |
|---|---|
| **Render throttle** — above `watchTPS*1.5`, render at most every `fastRenderMs` | `render()` ran every rAF against a 14 ms tick budget. Above watch speed the display is already lying (see `updateStrobe`), so most of the frame was going into a picture nobody reads. Largest single win for unattended long runs. |
| **Tile-culled `drawPlants`** | scanned every slot to `P.hi` once per wrap copy, with two `sqrt` and a `plantShade` per live plant regardless of the viewport. `PIDX` already buckets live plants by tile and each wrap copy maps the world rect onto the screen once, so the visible tile range is a clamp. Plants germinated since the last canopy rebuild miss `PIDX` and do not draw for up to `plantStagger` ticks — cosmetic. |
| **`W.cover[]` precomputed** | `laiOf(t)` was an 8-band sum run per tile, per animal, per think inside `senseDecide`, and depends on nothing individual. Now one array read. `laiOf()` itself is now dead code. |
| **Empty-tile skip in `senseDecide`** | cover, wrapping and two index reads were paid on tiles holding neither a plant nor an animal. |
| **`P.h[]` height cache** | `accessOf` called `effHeight` per scored plant per think. `rebuildCanopy` already computes it per plant; it just was not stored. Same staleness contract as `P.leaf` (L42-4), written additionally at germination and founding so a newly live plant never carries the previous occupant's height. |
| **Wrap by conditional, not `%`** | two modulos per tile scanned on the hottest line in the build; tile offsets are bounded by the sense radius, always below `W.n`. |
| **Tick budget checked every 4, was 16** | one slow batch could overshoot a 14 ms budget well past 100 ms, so the frame hitched instead of throttling. |

**Prediction:** ticks/sec at least doubles at high speed with a large standing
flora, and no ecological statistic moves beyond seed noise. `W.cover` is
zero-filled until the first `rebuildCanopy`, so cover is 0 for the first
`plantStagger` ticks of a run — before any animal exists.

### Not changed, on purpose

- **Detection is re-rolled every think.** P(never detected) over a residence
  time is `(1-p)^n`, so camouflage and `senseAcuity` saturate and are much
  weaker than their formulas suggest. Fixing it means per-animal detection
  memory, which is a real feature, not a patch. Know it before tuning either
  gene.
- **`PIDX` staleness.** A slot released and re-allocated to a seed at a new
  tile stays filed under the old tile until the next rebuild. Self-correcting —
  the `d2 > sr2` test uses live coordinates — but it silently drops that plant
  from detection for up to `plantStagger` ticks.
- **`nNear` includes corpses.** See L47-3.

### Addendum to the third pass — pre-fauna plant state, written 2026-08-09
(corrected same day — see note)

Free follow-up on the open question the third pass left hanging (did 1337/
4001 look like 4002 in their own first 40 days with fauna) — answerable
directly from raw JSON already in the repo, no new run needed. Only 1337 has
one (4001's is still blob-storage-blocked); the comparison is 1337 vs 4002.

**Correction:** the first version of this addendum read
`evosim-log-s1337-t1199603.json` as the 1337 default-arm run. It is not —
its own `cfg.k_confusion` is 0, making it the 1337 **`k_confusion:0`**
isolation-arm log (2499d, matches the previously-recorded near-extinction
numbers: harmonic N 55, min population 0, mean death age 0.0d). The correct
default-arm file is `evosim-log-s1337-t577507.json` (`k_confusion` 0.06,
1203d, matches the standing scorecard's R0 1.06 / harmonic N 215 / death age
12.1d). Numbers below are corrected against the right file. The qualitative
finding survives the correction; the magnitudes below replace the wrong
first-pass ones.

**The two seeds' plant communities were on different trajectories before a
single animal existed, let alone after:**

|  | day 260 plants | day 260 `pOcc` | day 260 `lai` | `caps` seen, days 215-265 |
|---|---|---|---|---|
| 1337 default | 15,619 | 0.30 | 1.22 | 0 (never) |
| 4002 default | 53,180 | 0.79 | 1.42 | 1 (bit 0 — plant slots), 6 of 11 samples |

4002's flora was already **~3.4x** 1337's standing count and **repeatedly
sitting at its `maxPlants` slot cap** in the run-up to day 265 (`caps=1` on
6 of the 11 five-day samples from day 215 on) while 1337 never hit it once.
This is a pure plant-side, pre-fauna difference; it cannot be an effect of
animal behaviour, confusion mechanics, or anything L47-3 touches, because no
animal exists yet in either trace at that point.

**Once fauna do arrive (day 265 in both, exactly — the reseed schedule
isn't seed-randomized), the two seeds diverge just as sharply:**

|  | day 265 animals | day 265 `pLocked` | day 300-305 animals | day 300-305 `pLocked` |
|---|---|---|---|---|
| 1337 default | 209 | 0.808 | 134-142 | 0.820-0.835 (stable) |
| 4002 default | 45 | 0.392 | 9,326 | 0.245 (falling) |

1337's founding population settles down to ~130 and its refuge holds steady
near 0.82-0.84. 4002's founding population — smaller at the start (45 vs
209) but sitting on top of ~3.4x the food and a refuge already less than
half as deep — explodes 200x in 35 days and its refuge keeps collapsing.

**This changes the read on the k_confusion:0 finding again, and this time in
a specific, testable direction.** The obvious candidate explanation is not
"the confusion mechanism doesn't actually protect populations" (the third
pass's tentative complication) — it's that **seed 4002's plant community
happened to grow far larger than 1337's before fauna ever arrived, likely
running into the `maxPlants` slot cap on its own, and that oversized,
capped food base is what let a tiny founding population explode past
whatever the confusion mechanism could dampen.** If true, this would also
explain why the `k_confusion:0` arm failed on *every* seed tried (a smaller
food base makes any given confusion setting matter less, not more, when the
real lever is how much standing biomass existed before predation started) —
but that inference needs checking, not assuming.

**Not acted on — this is a new hypothesis nobody proposed before this
addendum, so it's Tier B by CLAUDE.md's rule regardless of how compelling
the numbers look.** Candidate falsifiable prediction for the next Tier B
proposal: **pre-fauna plant standing count / cap status (not `k_confusion`)
predicts boom-bust outcome.** Testable by comparing pre-fauna plant
trajectories across more seeds (cheap — needs raw JSON, not a new run, for
any seed already logged) and, if the pattern holds, by testing whether
lowering `maxPlants` or otherwise capping pre-fauna plant growth changes the
outcome independent of `k_confusion`. Proposed to the owner in this
session; awaiting a decision before any new run or CFG patch tests it.

### Scorecard — third pass, written 2026-08-09

Closes out the default-arm 3-seed set: seed 4002 default (`kc-arm-default-
retry2`, GitHub Actions, v0.48.0) landed as a real raw JSON — no reconstruction
needed this time, the digest glob fix held. Promoted as
`evosim-log-s4002-default-t302d.json` / `evosim-digest-s4002-default-t302d.txt`.

**This seed is the weakest of the three and should not be read as equal-weight
to 1337/4001.** It hit `--max-wall-min 165` at day **302** — a third to a
quarter the length of 1337 (1200d) and 4001 (930d) — because it ran on
v0.48.0, before the v0.49 occupied-slot fix, at a standing population large
enough (~55-64k plants, up to 9,326 animals) to pay the full P.hi/AN.hi tax
the whole time. Two additional caveats specific to this run, neither seen in
1337 or 4001's digests:

- **`caps seen [0, 1]`** — a slot bound was hit at some point (bit 0: plant
  slots), vs. `[0]` clean in both other default-arm seeds. Some part of this
  trajectory is bound-limited, not purely selection.
- **Fauna arrived very late (day 265) and the run ended 37 days later, day
  302 — entirely inside the `aReseed` subsidy window** (net off day 320, "0
  unaided days" per the digest). Every animal that existed in this run's
  entire history did so with active artificial restocking still running.
  Demography numbers below are read with that in mind, not as a clean
  self-sustaining test.

**STATIONARITY GATE fails hard** — plants/bio/animals/soil all still moving,
animals **+2626.67%/100 samples** in the last third (population went
135->4004->9326 in the last ~40 days). Per HANDOFF.md §4's read order this
run is scored the same way 1337 and 4001 already were: a transient snapshot,
not a settled result. All three default-arm seeds have now failed this gate
— none of the three protocol runs has actually reached stationarity yet.

- **L47-1 (toxin) — still can't-tell, now 2-of-3 toward "rises."** `eToxin`
  **30.0%** of intake, matching 4001's 30.5% rise, not 1337's 11.1% fall.
  Two seeds now show the predicted rise, one shows the opposite. Still not a
  repeating pattern strong enough to score outright, but the balance shifted.
- **L47-2 (carnivory) — still seed-dependent, now 2-of-3 toward "stays low."**
  Histogram `[9244, 79, 2, 1, 0,...]` — near-zero, matching 1337, not 4001's
  moderate-carnivory read. `corr(aSize, carnivory)` was not computed for this
  seed (needs the raw JSON's per-tick series; not run here to keep this pass
  short). Two of three seeds sampled now sit near zero — leaning toward "the
  v0.39/v0.42 omnivory sweeps don't reproduce at this build," but one still-
  moderate seed (4001) keeps this open rather than closed.
- **L47-3 — `actAppr` now a clean miss on four of four seeds.** 0.02% of the
  action budget (rounds to the same 0.0% as the other three). No seed sampled
  so far has cleared the >1% falsifier. `socialAttraction` stayed PINNED 84%
  at min here (sel +0.00215, barely moving) — closer to 4001's flat read than
  1337's clear unpinning. Two of four samples now show little to no movement;
  the "unpins with real predation" half of the prediction is weaker than the
  first pass suggested, not stronger.
- **L47-4/5/6 — still can't-tell**, and this run is the wrong one to lean on
  for it regardless: it's the one seed that already shows a bound being hit
  (`caps seen [0,1]`), so a same-seed v0.46 control would be needed before
  drawing any performance-only conclusion from it specifically.
- **The `k_confusion:0` isolation-arm finding gets genuinely complicated,
  not confirmed and not refuted.** The second pass called two default-arm
  seeds "stable, still growing" against three failing `k_confusion:0` seeds.
  This third default-arm seed does **not** fit that pattern — it shows the
  same *flavor* of failure the isolation arm showed: refuge collapsing
  (`pLocked` worst 30-day fall **-0.197**, `corr(aSize, pLocked)` **-0.572**),
  R0 **0.11**, mean death age **0.5d** against maturityAge 6.4d (ratio
  **0.09**, worse than any number in this table so far), 98.5% of deaths by
  starvation. Read literally next to the isolation arm's numbers (1337 kc0:
  extinct; 4002 kc0: extinct; 4001 kc0: R0 0.72, refuge fall -0.502; and now
  4001 **default**: R0 1.00) this seed's default-arm R0 of 0.11 is *worse*
  than 4001's own `k_confusion:0` arm. But the confound above is real and
  large — this is a 37-day-old, reseed-subsidized fauna population, not a
  930-1200 day established one, and none of the other seeds have a
  directly comparable early window on record to check whether *they* also
  looked this rough right after fauna first arrived. **This cannot be scored
  as "confirms" or "refutes" the isolation-arm finding — it can only be
  scored as "the comparison needs an apples-to-apples early window from the
  other seeds, or a longer run of this one, before it means anything."**
  Flagging this explicitly rather than either dropping the caveat (which
  would overclaim the isolation-arm result) or dropping the new data point
  (which would hide a real complication) — this is exactly the kind of
  thing rule 5 exists for: don't calibrate anything against this run's
  demography numbers alone.

**Net: the default-arm 3-seed set is now complete by seed count (1337, 4001,
4002), but not complete by data quality** — 4002's short, bound-hitting,
subsidy-window run is not a peer of the other two, and its most striking
number (the R0/refuge collapse) is exactly the one most compromised by that.
The clean reads from this pass are the gene-frequency snapshots (`actAppr`
now 4/4 clean miss, `eToxin`/`carnivory` both now 2-of-3 leaning one way
without closing) — the population-dynamics reads need a longer version of
this seed, not a new seed, before they can be trusted.

**In plain language:** this world's plants bloomed on schedule — half a
million germinations, a canopy that closed in by day 165 — but animals
didn't show up until day 265, a full third of the way through even this
short run, and the moment they did, they overshot. From 135 animals to over
9,000 in about forty days, eating into a plant refuge that had been sitting
untouched and stable near half its biomass locked away from grazing. By the
time the run's compute budget ran out, that refuge was collapsing and almost
every animal that had ever been born in this world had already starved to
death before it was old enough to breed. It looks, on its face, exactly like
the population crashes seen when the herding-confusion mechanism was turned
off — except this run had that mechanism turned *on*. Whether that means the
confusion mechanism isn't actually what's saving the other seeds, or whether
every population in this simulation goes through a rough overshoot right
after fauna first establishes and the confusion mechanism only matters for
what happens *after* that rough patch, is exactly the open question this
pass can't answer with the data in hand. It needs either a longer run of
this same seed past its wall-clock cutoff, or a look at what 1337 and 4001
were doing in their own first forty days with fauna — not a new seed.

---

### Scorecard — second pass, written 2026-08-09

Supersedes the first pass below (kept for the record of how the data arrived,
not because its verdicts still stand as written). Two more seeds landed:
4001 default and 4001 `k_confusion:0`, both retry-batch runs, both stopped by
`--max-wall-min 165` rather than the day target or extinction (`headless.
wallClockExceeded: true` in both) — real data, just not the longest possible
read on either seed. Both raw JSONs are still stuck behind the same
blob-storage block as before; both digests here are reconstructed from the
Actions job log the same way the original seed-4002 `k_confusion:0` digest
was, and promoted as `evosim-digest-s4001-default-t930d.txt` /
`evosim-digest-s4001-kc0-t785d.txt`. That original seed-4002 reconstruction
has since been superseded by the real thing — a local regeneration (same
seed, same cfg, deterministic) finished and autohalted at the same day 560
the reconstruction reported, confirming the reconstruction was accurate;
`evosim-digest-s4002-kc0-t560d.txt` is deleted in favour of the raw
`evosim-log-s4002-kc0-t560d.json` it was standing in for. Seed 4002 default
is still missing — its Actions job also hit the digest-step glob bug below
and its own retry is running now (`kc-arm-default-retry2`, single seed,
v0.48.0 build — RNG-identical to v0.47.0 per the verified diff, so it slots
into this comparison
without asterisks). This section will get a third pass once that lands
rather than holding the whole write-up for it.

**Tooling note, not a biology finding:** both retry-batch digest jobs
crashed with `KeyError: 'cols'` immediately after printing their first
seed's digest. Root cause: `logs/seed-*.json` also matches each run's own
`seed-*.json.progress.json` (bash only checks the string *ends* in `.json`,
which the progress stub does too), so `analyze.py` choked on the second
argument. Fixed in the workflow (an extglob exclusion). Neither seed's
actual simulation output was affected — this only broke the auto-generated
digest artifact, recovered here from the job's console log instead.

- **L47-1 (toxin unified) — now conflicting, not a clean miss.** Seed 1337
  default: `eToxin` 11.1% of intake (fell, misses the "rises" prediction).
  Seed 4001 default: `eToxin` **30.5%** of intake — a clear rise past the
  17.2% baseline, the opposite result on the same arm. Two seeds, one hit one
  miss, is not a repeating pattern either direction — this needs the third
  default seed (4002, in flight) before it can be scored at all. Recorded as
  **can't-tell**, not miss.
- **L47-2 (one currency) — still open, and now visibly seed-dependent.**
  Seed 1337 default's carnivory histogram was dominated by the near-zero bin
  (`[2, 369, ...]`). Seed 4001 default's is **not** — `[0, 0, 0, 2, 84, 80, 5,
  2, ...]`, 164 of 173 standing animals sitting in the two moderate-carnivory
  bins, `carnivory` gene at `sel -0.0137` (roughly flat, not still climbing
  or falling hard). That is a real population sitting at moderate carnivory,
  not near zero — on the same build, same arbiter fix, different seed. The
  two seeds disagree on where carnivory lands as directly as they disagree on
  toxin cost. `corr(aSize, carnivory)` was only computed for seed 1337 (needs
  the raw JSON, which exists for that seed and doesn't for 4001/4001kc0/4002)
  so it can't be checked against the new data yet. **Verdict unchanged from
  the first pass — still open — but "carnivory stayed low" is no longer an
  accurate summary of what's been seen; say "seed-dependent" instead.**
- **L47-3 (confusion + `AN.risk`) — still mixed, `actAppr` now a clean miss
  on three of three seeds.** `actAppr` share: 0.0% (seed 1337 default), 0.2%
  (seed 4001 default), 0.0% (seed 4001 `k_confusion:0`) — all under the >1%
  falsifier, no exceptions. The `socialAttraction`-unpinning half is weaker
  than the first pass suggested: seed 4001 default shows no reported `moved`
  value for `socialAttraction` at all (below `analyze.py`'s move-reporting
  threshold), unlike seed 1337's clear 0.235 rise. One seed unpinned it
  clearly, one didn't move it much — not yet a repeating result either way.
  The `AN.risk`-EWMA hypothesis and the ATTACK-floor asymmetry from the first
  pass are unchanged: still untested, still flagged, still not acted on.
- **L47-4/5/6 (performance only) — still can't-tell**, same reasoning as the
  first pass. Seed 4001 default and seed 4001 `k_confusion:0` both show
  `caps seen [0]` (clean), consistent with "no effect" but not proof of it
  without a same-seed v0.46 control.
- **The `k_confusion:0` isolation arm — the one clear result in this batch,
  and it isn't one of the six predictions.** Three of three `k_confusion:0`
  seeds now show severe population failure: 1337 extinct ~day 680, 4002
  extinct ~day 560, and 4001 — not confirmed extinct, but in freefall when
  the wall-clock budget cut it off at day 785 (`animals -299.7%/100d` in the
  last third, `pLocked`'s worst 30-day fall -0.502, R0 0.72, mean death age
  4.7d **below** maturityAge 5.1d). Against that, two of two default-arm
  seeds sampled so far are stable at their own cutoffs: seed 1337 (1200d,
  animals +32.7%/100d, still growing) and seed 4001 (930d, animals
  +46.0%/100d, still growing). `control-v0_47-k_confusion0.json` changes
  exactly one constant (`k_confusion: 0`, nothing else), so this is a clean,
  well-isolated comparison, not a confound: **disabling the confusion
  mechanism is associated with population collapse across every seed tried
  so far, and leaving it on is associated with stability across every seed
  tried so far.** This is n=3 vs n=2 on a comparison nobody set out to run
  for its own sake — it fell out of trying to isolate L47-1/L47-2 from
  L47-3 — but by invariant 12 ("believe nothing that does not repeat") a
  5-for-5 split this clean is worth taking seriously rather than waiting on
  a seventh seed to say so. Not one of the six original predictions, so it
  doesn't get a hit/miss/can't-tell tag — it gets flagged as a candidate
  finding for the next Tier B proposal instead. See below.

**Net: still not a clean six-result scorecard, but no longer mostly holes
either.** State now: two default-arm seeds (stable, disagreeing on toxin/
carnivory specifics), three `k_confusion:0` seeds (uniformly failing), one
seed still in flight (4002 default). L47-1 and L47-3's `socialAttraction`
half went from "scored" to "can't-tell" on more data, which is the point of
running more seeds before trusting n=1 — a miss on more data means the first
pass's diagnosis was drawn too early, not that this pass's is wrong.

### Scorecard — first pass, incomplete, written 2026-08-09 (superseded above)

The full 3-seed protocol this section calls for was never cleanly completed.
What exists: seed 1337 at default config (1200d, not stationary), seed 1337
at `k_confusion:0` (2495d, fauna extinct unaided at day ~680), and seed 4002
at `k_confusion:0` (560d, fauna extinct — reconstructed from a GitHub Actions
job log, not the raw JSON, after the artifact landed on blob storage this
sandbox's egress policy blocks). Two more seeds (4001/4002 default, 4001
`k_confusion:0`) were lost outright to a 180-minute Actions timeout that
produced zero output — `headless.js` only wrote results at the end of a run,
so a hard-killed job returned nothing for ~3 hours of compute. Fixed in v0.48
tooling (a wall-clock safety budget that always returns partial output), too
late for this batch.

- **L47-1 (toxin unified) — MISS** on this seed alone (later contradicted —
  see the second pass above).
- **L47-2 (one currency) — open, leaning concerning, not resolved** on this
  seed alone (later complicated by seed-dependence — see the second pass).
- **L47-3 (confusion + `AN.risk`) — mixed** on this seed alone.
- **L47-4/5/6 (performance only) — can't-tell.**

---

## v0.48 — extinction-halt fix + global-lookup caching

Two changes, both performance/mechanical, neither an ecological claim —
following straight from auditing the actual project this session, not from
scoring the v0.47 predictions above (that scorecard is unrelated to why
these shipped).

### [L0.48-1] — the extinction halt never fired

```js
if (LOG.aGone && !ST.apop && !CFG.animalReseedDays && !LOG.halted
    && W.tick - LOG.aGoneTick > CFG.haltAfterDays*TPD()){
```

`!CFG.animalReseedDays` required that *constant* to be falsy. It defaults to
60 and nothing in the shipped build ever changes it, so this condition could
never be true at default config, regardless of how long a world sat
animal-free. This is exactly the bug the comment above it describes fixing
("seed 6175 ran 3,800 animal-free days... half the run producing nothing")
— it just never actually worked. `headless.js`'s own autohalt (`!ST.apop`
with no reseed-days gate at all) never had this bug; this brings the shipped
build in line with it. One clause dropped, nothing else touched.

### [L0.48-2] — the two hottest functions were re-resolving a global 20+ times a call

A `--prof` pass over a fixed 300-sim-day run (seed 4001, default config —
chosen to cross both the plant bloom and the day-260 fauna arrival) found
`updatePlant` and `senseDecide` responsible for **58% of all JS execution
time** between them, with V8's `LoadGlobalIC`/`LoadIC` builtins alone
accounting for **17.5%**. `CFG` is a top-level `const`, referenced by name
~20-25 times per `updatePlant` call and ~24 times directly in `senseDecide`
(more via the scoring helpers it calls up to `senseCap` times per candidate)
— and it never changes mid-run; only `buildWorld()` assigns it, before
`tick()` ever runs. Re-resolving the global binding on every one of those
reads was pure overhead the existing code already avoided for other
frequently-read state (`W.n`, `W.tileArea`, `P.genome` were already aliased
to locals at the top of `updatePlant`; `CFG` was the omission). Fix: alias
`CFG` to a local `C` once per call in `updatePlant`, `senseDecide`, and the
small scoring helpers those call — `reachOf`, `carrionDigest`, `grazeYield`,
`plantScore` — and read `C.foo` instead of `CFG.foo` everywhere in those six
functions. No formula changed, no `rng()`/`gauss()` call site touched.
`updateAnimal` (2.7% of JS time) and `rebuildCanopy` (5.2%) were left alone —
real but well below the two dominant functions, and widening scope raises
diff size/risk for a return that isn't where the profile pointed.

**Prediction:** trajectory identical to v0.47 for the same seed at the same
tick (RNG-neutral by construction); ticks/sec measurably higher on a fixed
sim-day count; no gene mean or population statistic moves beyond seed noise.

**Verification: PASS, exactly.** Seed 1337, 300 days, v0.47 vs v0.48: 0 of 97
`cols` differ across all 60 samples, gene snapshots byte-identical, event log
byte-identical, final matter/plants/animals identical. 315→322 ticks/s
(contended with another job running alongside it — directional, not a clean
benchmark, but consistent with the hypothesis).

### A structural naming problem, found while writing this section, worth knowing about

Every `[Lnn]` tag before v0.37 is a flat, ever-incrementing sequence (now
past L66). Since v0.37, a version that bundles several changes tags them
`L<version>-<index>` instead — `L37-1`, `L47-1`..`L47-6`, and this version's
`L0.48-1`/`L0.48-2`. **These two schemes share one integer space, and the
flat sequence has already grown past both 47 and 48** — there is a real,
pre-existing bare `[L47]` (line ~1835 in the source, about growth/breeding
order) and a real bare `[L48]` (line ~1872, about clutch-cost hoisting),
both unrelated to the v0.47 audit or this version, both from years before
either. `L47-1..6` already silently collided with the older bare `[L47]`;
adding bare `L48-1`/`L48-2` would have collided with the older bare `[L48]`
too, which is why this version's tags are `L0.48-1`/`L0.48-2` instead — the
version string itself, not just its integer, so a dot makes it un-collidable
with the flat sequence forever. Not fixing the existing `L47-1..6` /
`[L47]` collision retroactively — those already shipped, `grep` for the
exact bracketed string still resolves each one unambiguously, and rewriting
six already-referenced tags for a cosmetic problem is not worth the risk.
Going forward: **any new version-bundle tag should use the `L<major>.<minor>`
form** (`L0.49-1`, not `L49-1`) so this stops happening.

---

## v0.49 — occupied-slot lists replace the P.hi/AN.hi scan bound

### [L0.49-1] — a run pays for its largest-ever population forever, not its current one

Found investigating a real complaint: a world holding a *steady* 14-20k live
plants was running at a fraction of a same-population world that had never
exceeded that count. Root cause was already half-documented in [L47-4]'s own
comment ("P.hi/AN.hi never come back down") but the consequence hadn't been
traced through: five per-tick loops — `rebuildCanopy`, `buildPlantIndex`,
`buildAnimalIndex`, `updatePlants`, `updateAnimals` — scanned `0..P.hi` /
`0..AN.hi`, and `P.hi`/`AN.hi` are a high-water mark that only ever grows
within a run (the existing top-trim only removes a fully-empty *suffix*; one
long-lived survivor near a historical peak index blocks it indefinitely).
`buildAnimalIndex` was the worst case — it runs unstaggered, every tick, two
full passes.

Confirmed empirically before writing any code: a diagnostic (`plantsHi`/
`animalsHi` added to `headless.js`'s own progress output, not the shipped
build) on an uncontended run showed live plants swing 23,163 → 14,577 →
13,844 → 19,842 over 30 sim-days while `plantsHi` sat frozen at 26,584 the
entire time, with the instantaneous tick rate dropping in lockstep with the
gap, not with the live count.

**The fix:** `P.occIdx`/`AN.occIdx` — compact arrays of currently-occupied
slots (seed or live for plants; alive or corpse for animals, matching
exactly what `buildAnimalIndex`/`updateAnimals` need), maintained
incrementally: push on `allocSlot`/`allocAnimal`, O(1) swap-remove on
`releaseSlot`/`freeAnimal`. Every place that used to push directly onto the
free list (five sites, mostly founder-placement failures and one
scavenge-consumed-corpse case) now routes through those two functions so the
bookkeeping can't drift out of sync. **No organism's slot index ever
changes** — `AN.tgt` and every other index-based cross-reference stays valid
throughout an organism's life — only the *order* the five loops visit
organisms in does, since swap-remove doesn't preserve insertion order.

**Why this isn't RNG-exact, laid out before running anything:** two of the
five loops (`buildPlantIndex`, `buildAnimalIndex`) feed `PIDX`/`AIDX`, which
`senseDecide` scans with early-stopping once `senseCap` candidates are
found — a different insertion order changes which candidates get evaluated
and in what sequence, which changes the `rng()` draw sequence from that
point on. Separately, `updatePlants`' stagger loop now strides over
*position* in `P.occIdx` rather than raw slot index, so a plant dying as a
direct result of its own update this tick can swap an unvisited slot into an
already-visited position — skipped for one stagger cycle, never lost,
self-corrects next cycle. `updateAnimals` isn't strided (it's a full pass
every tick; think-scheduling still keys off each animal's own slot index,
unchanged) but the same swap-remove-during-iteration hazard applies when one
animal's action kills a *different* animal mid-pass (confirmed a real,
existing case: `ACT_SCAVENGE` finishing off a corpse frees a slot elsewhere
in the list). Worst case in both loops is one skipped or double-processed
tick for one organism — bounded, rare, self-correcting, but enough to shift
the global RNG sequence permanently from that point on.

**Prediction:** ticks/sec rises measurably at high population (the pathology
this targets) and doesn't regress badly at low population; matter
conservation holds exactly in both arms; trajectories will **not** be
RNG-exact, but no gene mean or population statistic should show a
*consistent, one-directional* shift across independent seeds — chaotic
divergence in either direction is expected and acceptable, a systematic bias
in one direction would not be.

**Verification.** Two seeds, 300 days each, `k_confusion:0` (a reliable
bloom, and CFG-unrelated to this change), each run solo (no CPU contention)
on the unmodified v0.48.0 build and this change, same seed both times:

| | seed 1337 (peaks ~15-17k plants) | seed 4001 (peaks ~43-47k plants) |
|---|---|---|
| wall-clock, 300d | 450.2s → 580.4s (**28% slower**) | 1825.4s → 1201.0s (**34% faster**) |
| ticks/sec | 320 → 248 | 79 → **120** (52% higher) |
| matter conservation | 6819→6819 both (exact) | 7533→7534 (0.013% leak) → 7533→7533 (exact) |
| columns identical / 97 | 10 | 8 |
| animal births | 361 → 2390 | 1506 → 260 |
| life-support net fired | 234 → **0** | 0 → 0 |

Matter conservation — the one hard invariant that has to hold regardless of
RNG path — holds exactly in every run, and the tiny leak in seed 4001's
unmodified run disappeared rather than worsened. Performance is exactly the
mixed picture predicted: a real, substantial win at the population scale the
fix targets (44-47k, where the `P.hi`-vs-live gap is large), and a real
regression at a scale where that gap stays modest (the per-birth/death
bookkeeping — one swap-remove per event — is a fixed tax that doesn't pay
for itself until the gap does). Neither seed went through a full bloom-bust
cycle in 300 days (that happens later for both, per existing `k_confusion:0`
data), so the *worst*-case pre-fix scenario (a busted population still
paying for its peak) wasn't directly re-created here — the diagnostic run
above stands in for that instead, on the unmodified build alone.

The population outcomes moved by a lot in absolute terms and in **opposite
directions** on the two seeds (seed 1337's fauna did dramatically better
after the fix — zero life-support interventions against 234 before; seed
4001's did worse — 260 births against 1506 before). Read alone, either
result would be alarming. Read together, they're the signature of chaotic
RNG-path sensitivity, not a systematic bug: a directional bias would show
the *same* arm doing better on both seeds, not opposite arms winning on
different seeds. This is the same category of change [L47-4]'s slot
compaction and [L47-5]'s inheritance rewrite already made and shipped —
order changes, draw sequence changes, individual-seed outcomes are not
comparable to their pre-change counterparts, but aggregate/statistical
behavior across seeds is the thing that has to stay put, and by that
standard this passes.

**Shipped as v0.49.0, not folded into v0.48.0**, per rule 3 — a separate
structural change gets its own version and its own row, even though v0.48
was mechanical too.

### Known limitation, not fixed this pass

The regression at modest population (seed 1337, -28%) is real and
unaddressed. The fixed per-event cost of maintaining `P.occIdx`/`AN.occIdx`
doesn't scale with the `hi`-vs-occupied gap, so at low inflation it's pure
overhead. Worth revisiting only if it turns out to matter in practice — most
runs of interest are exactly the large/inflated-population regime this
targets, and the fix can't be *worse* than the pre-v0.49 behavior once a
world has actually busted (a scan of a smaller occupied list is never slower
than a scan of a larger `hi`-bounded one), so the downside is bounded to
runs that stay small and never bloom, which are already the cheapest runs
regardless.

---

## v0.49 CFG finding — k_photoCost is the actual lever on plant carrying capacity

Not a new HTML version — a CFG patch, per rule 6. Fell out of the pre-fauna
plant-cap addendum above: plants were hitting `maxPlants` (90,000) via a
slot ceiling, not any biological mechanism, fifty days before fauna even
existed. Every default-config seed tried this session (1337, 4001, 4002,
both arms) either boom-busted into extinction or came within a hair of it.

**Screening batch (owner-approved fast-iteration mode, 1 seed each unless
noted):** all runs share a `maxPlants:25000, maxAnimals:11000` arena — a
deliberate 3.6x shrink for iteration speed (was hitting 165-min wall-clock
timeouts at 90k/40k; the smaller arena finishes 1200 days in 20-30 minutes).
That arena shrink is itself untested in isolation from `k_photoCost` — see
"Open confound" below.

- **`fast-batch-arena`** (arena shrink only, control, no `k_photoCost`
  change) — seed 1337 extinct (R0 0.48), seed 4002 not extinct but R0 0.72,
  `caps seen [0,1,4]` (multiple bound types hit). Same failure mode as every
  90k/40k default run, just smaller.
- **`fast-batch-photocost`** (`k_photoCost` 0.004→0.012, 3x) — **seed 1337
  R0 1.21, seed 4002 R0 1.31, seed 4001 R0 1.03. All three seeds finished
  the full 1200-day target. Zero extinctions.** First viable (R0>1)
  populations in any log this session. Seed 1337: plants oscillating
  7,000-11,000 (in the range the owner independently flagged as
  "balanced"), `pLocked` refuge holding 0.83-0.88 instead of collapsing,
  `caps` clean.
- **Dose-response, seed 1337 only:** `screen-photocost-lo` (2x, 0.008) R0
  1.80 but death/maturityAge ratio only 0.29 and hit a cap once;
  `screen-photocost-hi` (5x, 0.020) R0 1.16, ratio 0.39, clean. Direction
  holds at 2x and 5x; 3x isn't a knife-edge.
- **Combo arms** (3x `k_photoCost` + one previously-extinct-alone lever,
  seed 1337): `+a_base 0.008` R0 1.08; `+k_gut/k_digest halved` R0 **1.37**,
  ratio **0.73** (best demographic health of any arm this session);
  `+carrionFloor 0.10` R0 0.96 (borderline). All three survived the full
  1200 days where they'd gone extinct on the inflated 90k-cap food base
  alone — consistent with the diagnosis that those levers were fighting an
  artificially large prey base, not a real one.

**Net (revised below — a 4th seed broke the pattern, see next paragraph): 8
of 8 runs with `k_photoCost` raised (any dose, any combo, any of 3 seeds)
survived the full run. 0 of 2 runs with the arena shrink alone did.** This
established `k_photoCost` as a real, dose-consistent, multi-seed finding —
not just a screen — but "8 of 8" understated how it should be read going
forward; see the correction immediately below before treating this as a
guarantee.

**Correction, same day — seed 6060 (4th seed, base 3x dose, same 25k/11k
arena as the original 3) went extinct.** R0 0.25, mean death age 3.5d
against maturityAge 27.4d (ratio 0.13, worse than any prior photocost-arm
run), harmonic N 8, autohalted day 685. `caps seen [0]` — clean, no cap
ever bound, and population stayed small throughout (max 248) rather than
showing the boom-then-refuge-collapse shape the pre-photocost extinctions
had. This looks like a different failure mode: a founding population that
never caught a lucky early run rather than one that overshot and crashed a
food base. **Revised count: 3 of 4 seeds at the base 0.012 dose survived
with R0>1; the 4th went extinct by a different mechanism than the old
default-config failures.** `k_photoCost` raised the *odds* of a viable
population dramatically (was 0 of several default-config seeds all
session; now most seeds at this dose) — it did not make every seed viable
unconditionally. Treat "photocost fixes it" as a strong, real, majority
effect from here on, not a universal one, until more seeds narrow whether
6060 is an outlier or the actual base rate is closer to 75%.

**Second correction — seed 6363 (5th seed, same base dose/arena) also went
extinct, but looks like a different, closer call than 6060.** R0 0.76 (vs
6060's 0.25 — much nearer viable), death age 8.5d against maturityAge 4.2d
(ratio **2.03**, genuinely healthy — most animals that died had already
outlived maturity), harmonic N 60 (vs 6060's 8), ran to day 1015 before
autohalting (vs 6060's 685). `caps seen [0]` clean again. **Revised count:
3 of 5 seeds at the base dose survived the full 1200 days (60%), not 3 of
4.** The two extinctions don't look like the same failure mode as each
other, let alone the old pre-photocost boom-bust crashes: 6060 was unhealthy
throughout (ratio 0.13, tiny harmonic N), 6363 looked like a fundamentally
viable population that still tipped over late — closer to normal stochastic
extinction risk at a small population size than a diagnosable flaw.
`k_photoCost` is still the strongest lever found this session by a wide
margin (0/many at default config vs 3/5 here, plus the dose-response and
combo arms all surviving at n=1 each) — but "balanced" at this dose still
means "usually viable, not always," which itself may be realistic (small
populations really do face stochastic extinction risk) rather than a defect
to keep chasing. Worth deciding explicitly, not by default: is 60% survival
at N~100-200 animals an acceptable "balanced," or does the target population
scale need to be larger (fewer stochastic wipeouts) even at the cost of
returning to a bigger, slower arena?

**Confound resolved — the arena shrink was never load-bearing.**
`photocost-isolate-arena` seed 1337: `k_photoCost` 0.012 alone, ORIGINAL
`maxPlants` 90,000 / `maxAnimals` 40,000, no arena shrink at all. Result is
**numerically identical** to the small-arena version of the same seed: R0
1.21, harmonic N 43, plants oscillating 7,000-11,000, `pLocked` refuge
0.83-0.88, `caps seen [0]` clean, death/maturityAge ratio 0.60. Plants
settle to the same equilibrium regardless of whether the ceiling is 25k or
90k, exactly as predicted — respiration cost sets the carrying capacity,
the slot count was never the actual constraint once this dose is applied.
**This means the 25k/11k arena used throughout this investigation was
purely a speed optimization with zero independent ecological effect** —
`k_photoCost` alone, at full original scale, is the clean, isolated fix.
Worth keeping the smaller arena for iteration speed regardless (confirmed
faster, no downside), but it's no longer an open confound in the finding.
**Second seed confirms:** local seed 6262, same isolation cfg (full 90k/
40k arena), also survived the full 1200 days — R0 **1.42**, ratio **0.82**
(best demographic health of any full-arena or small-arena run to date),
harmonic N 68. 2 of 2 seeds tried at full arena scale are viable.
itself.

**Remaining next steps:**
1. **The gutcost combo — 3rd seed lands weaker, tempering the early read.**
   Seed 1337: R0 1.37, ratio 0.73, caps clean. Seed 4001: R0 1.07, ratio
   2.61 (best yet), caps clean. **Seed 6161 (local, 3rd): R0 0.91**
   (borderline — under 1 for the first time on this combo), **ratio 0.23**
   (poor — worse than either of the first two), and **`caps seen [0,1]`**
   (the plant slot cap bound at some point, unlike the first two). No
   extinction on any of the 3, which is still real signal, but the
   demographic-health numbers swing as widely on this combo as they did on
   the base dose alone (0.23 to 2.61 on ratio, 0.91 to 1.37 on R0). Revise
   down from "looking like the strongest configuration" to "no extinctions
   in 3/3, but not obviously more consistent than the base dose" — more
   seeds (batch of 3 + 2 more already queued on Actions) will settle
   whether this was a weak seed or the combo's real variance.
2. **Survival at the base dose updated to 4/6 (67%) with a 6th seed.**
   Seed 6464: full 1200 days, R0 **1.20**, ratio 0.49, harmonic N 20,
   `caps seen [0,1]` (bound hit once, first time in this specific batch).
   Tally now: 1337✓ 4001✓ 4002✓ 6464✓ / 6060✗ 6363✗ — 4 of 6, not
   universal but trending better than the earlier 3/5 read, and now
   comfortably ahead of the demoted gutcost combo's 2/5. Worth deciding
   "balanced" (small populations do face real stochastic extinction risk)
   or whether the target scale needs to be larger.
3. `STATIONARITY GATE` still fails on every arm above (still drifting at
   1200 days) — read all R0/ratio numbers as directional, not final, same
   discipline as every other scorecard this project keeps.

**Status: `k_photoCost` 0.004→0.012 is ready to promote to a shipped CFG
patch.** Confound resolved, dose-response checked (2x/3x/5x all positive),
multi-seed (5 seeds at base dose, majority viable), combo arms tested. Not
yet added to the version-log table — doing that alongside the gutcost
3-seed confirmation landing, so both go in together rather than as two
separate small edits.

---

## v0.50 — ATTACK arbiter floor removed [L0.50-1]

**One structural change.** ATTACK's score carried `*(0.5 + meatAttraction)`
— a hard floor at 0.5x regardless of how low `meatAttraction` drifts, while
GRAZE (`plantScore`, via `plantAttraction`) and SCAVENGE
(`*G[g+AG.carrionAttraction]*hunger`) both multiply their attraction genes
unfloored, reaching true zero. Flagged in HANDOFF.md as an untouched
structural asymmetry since the v0.47 audit: **predation could never fully
switch off the way herbivory and scavenging can**, meaning any population
that never evolves real carnivory is still silently scored *as if* it were
half-interested in attacking, every single think, every tick. Changed
`*(0.5 + G[g+AG.meatAttraction])` to `*G[g+AG.meatAttraction]` — now
matches the unfloored pattern used everywhere else in the arbiter.

**Prediction, written before any run:** in populations where `meatAttraction`
sits near its current default (~0.10, far from either bound), this should
move almost nothing — the multiplier only differs from before by removing
a *constant* 0.5, so ATTACK's score roughly halves in absolute terms but
the *relative* ranking against GRAZE/SCAVENGE/FLEE shifts only where
`meatAttraction` is genuinely near zero. Falsifiable readout: compare
`actAttack` share and the carnivory histogram's near-zero bin population
against a same-seed, same-cfg v0.49 run. **Hit** = `actAttack` share drops
further toward true zero in runs that already showed near-zero carnivory
(1337-style), while runs with real predation pressure (4001-style, or any
of this session's photocost-positive runs) are not obviously worse. **Miss**
= `actAttack` share collapses everywhere, including runs that previously
sustained real predation — that would mean the floor was load-bearing for
keeping predation viable at all, not just an asymmetry, and the change
should be reverted rather than defended.

Only `node check.js` run so far (PASS, VERSION 0.50.0, arbiter branches
WANDER/GRAZE/ATTACK entered in the harness's 71-call sample). No ecological
run yet — firing a 3-seed comparison against v0.49 next, on top of the
confirmed `k_photoCost` base dose (0.012) so the comparison isn't muddied
by the food-base problem v0.50 inherits from every prior version.

`evosim-v0_49_0.html` kept alongside `evosim-v0_50_0.html` until this
verifies — not deleted per rule 9's convention (delete only once results
are captured here).

**Gutcost combo — 5-seed tally, verdict revised down.** No extinctions in
5/5, but R0>1 in only 2/5:

| seed | arena | R0 | ratio |
|---|---|---|---|
| 1337 | small | 1.37 | 0.73 |
| 4001 | small | 1.07 | 2.61 |
| 6161 | small | 0.91 | 0.23 |
| 1337 | full | 0.86 | 0.36 |
| 9099 | small | **0.58** | **0.18** |

**Revised verdict: the gutcost combo is not better than the base
`k_photoCost` dose alone.** Base dose was 3/5 seeds with R0>1 (60%); this
combo is 2/5 (40%) — weaker on the metric that matters most, despite zero
extinctions. The "no extinction" framing was true but incomplete: R0<1
means the population is shrinking even where it isn't dead yet, so 3 of
these 5 runs would eventually fail given more days. Arena size (small vs
full) doesn't explain the spread — both extremes (1.37 and 0.58) are on
the small arena. **This combo should not be promoted ahead of the base
dose alone** — it adds a second changed constant for no demonstrated
benefit and measurably worse R0 odds. The base `k_photoCost` 0.012 dose
by itself remains the strongest, most-tested, most defensible finding
of this investigation.

**8-seed final tally** (3 more Actions seeds landed, `gutcost-confirm-batch2`
— note this batch's own trailing `digest` Actions job got stuck queued
behind the concurrency ceiling even though all 3 simulations finished;
fetched the per-seed results directly via git branch instead of waiting
on it, worth remembering as the general pattern going forward — a run's
top-level "completed" status lags behind its actual simulation results
whenever the digest step queues):

| seed | R0 | ratio | caps |
|---|---|---|---|
| 1337 (small) | 1.37 | 0.73 | clean |
| 4001 (small) | 1.07 | 2.61 | clean |
| 9001 (small) | 0.90 | 0.33 | clean |
| 9003 (small) | 0.73 | 0.93 | bound hit |
| 9002 (small) | 0.67 | 0.51 | clean |
| 6161 (small) | 0.91 | 0.23 | bound hit |
| 1337 (full) | 0.86 | 0.36 | clean |
| 9099 (small) | 0.58 | 0.18 | clean |

**2 of 8 (25%) clearly R0>1 — verdict confirmed, not just an early read.**
Gutcost combo settles further below the base dose's independent 4/6 (67%).
Closing this branch of investigation: no further seeds planned for this
combo, the base `k_photoCost` dose alone is the finding worth carrying
forward.

---

### v0.50 — first ecological data point, seed 1337, base photocost dose

Local run, 800 days, no extinction. Compared against the same seed's v0.49
baseline (`fast-batch-photocost` seed 1337: R0 1.21, ratio 0.60, actAttack
0.8%, harmonic N 43):

| | v0.49 | v0.50 |
|---|---|---|
| R0 | 1.21 | **0.57** |
| ratio | 0.60 | 0.40 |
| actAttack | 0.8% | **0.1%** |
| harmonic N | 43 | 31 |

**Partially consistent with the prediction, but n=1 and not scoreable yet.**
The prediction was specifically about `actAttack`/carnivory on already-
near-zero-carnivory seeds like this one — and it did drop further (0.8%
→ 0.1%), the predicted direction. But R0 also dropped substantially, which
the prediction didn't address either way, and a single-seed comparison
after a genuine formula change (not a measurement-only edit) is exactly
the situation where chaotic RNG-path sensitivity can produce a large swing
that has nothing to do with the ecological claim — the same caveat v0.49's
occupied-slot-list change carried, documented at length in that section.
**Not treating this as a miss yet** — it's one seed. The Actions 3-seed
v0.50 test (`v050-attack-floor-test`, seeds 1337/4001/4002) and the two
v0.50 combo re-tests are still queued/running; scoring the L0.50-1
prediction properly waits for those.

### Dose-response tally update — 5x dose looks strongest so far

More Actions seeds landed (fetched directly via git branch — several of
these runs' trailing `digest` jobs are stuck queued behind the concurrency
ceiling even though all their simulation jobs finished; this is now a
established pattern, not a one-off, see the gutcost-combo note above).

**5x dose (`k_photoCost` 0.020) — 4 seeds, 3/4 (75%) R0>1:**
1337 (local) 1.16✓, 4001 1.08✓, 7002 **1.51✓** (best single result of any
arm this session, ratio 1.86 — genuinely healthy), 4002 0.22✗ (weak,
`caps` hit). Best survival rate of any dose tried so far, ahead of the
base dose's 4/6 (67%).

**2x dose (`k_photoCost` 0.008) — 2 seeds, 1/2 so far:** 1337 (local)
1.80✓ (highest single R0 all session), 7001 0.88✗. Two more Actions seeds
(4001, 4002) still in flight.

**a_base combo — 2 seeds, 1/2 so far:** 1337 (local) 1.08✓, 4001 0.70✗.

**Emerging picture: no configuration is anywhere near universally viable,
but 5x `k_photoCost` alone is pulling ahead of every other arm tried
(75% at n=4, best single-seed result, best single-seed ratio).** Worth
watching as more seeds land — if this holds, 5x may be the better
constant to promote over the original 3x base dose, not just a confirmed
alternative dose.

**carrionFloor-alone combo, 2nd seed:** 4001 R0 0.66, ratio 0.25 (weak).
Combined with 1337 (0.96, borderline): 0/2 clearly viable. Also trailing
the base dose.

### Deep-dive: is there an early-warning signal for which seeds crash?

Compared per-tick trajectories (not just summary stats) between a survivor
(4001, R0 1.31) and an extinct run (6060) at the identical base-dose cfg.
Striking difference in the first 50 days after fauna arrival (day 265):
survivor's `pLocked` (refuge) oscillates in a stable band (0.38-0.50);
6060's `pLocked` shows a sustained downward trend (0.31→0.15) that
precedes the population crash by ~15-20 days. Hypothesis: an early,
sustained refuge-erosion trend (not just level) is a leading indicator
of eventual collapse.

**Checked across 7 seeds with raw JSON on hand — mixed, not confirmed:**

| seed | cfg | day-265 aSize | 50-day `pLocked` trend | outcome |
|---|---|---|---|---|
| 4001 | base | 2.55 | -0.020 (flat) | survived, R0 1.31 |
| 6464 | base | 4.34 | +0.048 | survived, R0 1.20 |
| 6262 | full-arena | 6.73 | +0.100 | survived, R0 1.42 (best) |
| 6060 | base | 3.12 | **-0.138** | **extinct d685** |
| 6161 | gutcost | 4.67 | **-0.177** | weak, R0 0.91 |
| 6363 | base | 4.98 | +0.261 | **extinct d1015** (contradicts) |
| 9099 | gutcost | 6.65 | +0.079 | weak, R0 0.58 (contradicts) |

5 of 7 fit (down-trend → bad, up-trend → good); 2 contradict outright.
**`aSize0` shows no relationship at all** — the run with the largest
founding animals (6262, aSize 6.73) had the best outcome, the smallest
(4001, aSize 2.55) also did fine, ruling out my first-pass "big founders
doom the run" read from the 2-seed comparison. The comparison set also
mixes cfgs (base/gutcost/full-arena), which confounds any clean read.

**Not confirmed — flagged as a real lead, not a mechanism.** The right
next test: hold cfg constant (base dose only) across ~8-10 seeds, record
`pLocked` trend in the first 50 days post-arrival, and check whether it
actually predicts the eventual R0 with a clean same-cfg sample. If it
holds, the next question is what drives the trend itself — likely
candidates: how many founders arrive at once (reseed count), or how much
standing plant biomass existed at exactly day 265 (independent of the
pre-fauna trajectory already documented). Worth doing before inventing
any new CFG lever aimed at "fixing" the crash rate — if this is real,
it may be irreducible stochasticity (small-N founder luck) rather than
anything a constant can fix, which would mean the ~60-75% viability
already found is close to the ceiling for this population scale.

---

## Correction to v0.50 — external audit caught a confounded change, 2026-08-10

An external Claude Code audit (full review: `EVOSIM-EXTERNAL-REVIEW.md` on
`main`) found a real bug in [L0.50-1]: `*(0.5 + meatAttraction)` →
`*meatAttraction` removes the floor **and** silently changes the gain.
At the founder value (`meatAttraction` 0.10), the old formula scored
0.5+0.10=0.60; the new one scored just 0.10 — a 6x reduction riding along
with the floor removal, violating one-structural-change-per-version in
spirit even though it was one line. The audit's own words: "the n=1 run
may not be noise — it may be a real effect of the confounded half of the
change." That's a serious, specific, correct catch — the mixed n=1 result
recorded earlier (actAttack dropped as predicted, R0 also dropped
unexpectedly) is now suspect: the R0 drop may simply be a 6x-weaker
ATTACK score crowding out predation entirely, not a genuine RNG-path
noise artifact as I'd guessed at the time.

**Fixed by pivoting, the same discipline HANDOFF.md §2b already documents
for exactly this situation** (re-pivot so the value is unchanged at the
founder, only the slope moves): added `k_meatAttr: 6.0` and changed the
score to `*k_meatAttr*meatAttraction`. `6.0 * 0.10 = 0.60`, matching the
old floored formula exactly at the founder gene. `node check.js`: PASS.

**All v0.50 ecological data collected before this fix is invalidated** —
it tested the confounded (gain-reduced) version, not the isolated
floor-removal this change was supposed to be. This includes:
- The local seed-1337 n=1 result ("mixed, not scoreable")
- Whichever seeds of `v050-attack-floor-test`, `v050-gutcost-retest`,
  `v050-confusion-off-retest` had already run against the pre-fix file

**Not re-fired yet** — per the audit's suggested order of operations,
the noise-floor run and decision-rule work below take priority over
re-testing v0.50, since without a noise floor a fresh v0.50 test would
have the same "moved in the predicted direction" interpretation problem
the whole session has been making. Re-test v0.50 after the noise floor
lands.

**Kept as an open, unsolved flag per the audit's point #12 (absorbing
states):** with the floor removed, if `meatAttraction` drifts to ~0 via
mutation-drift in a population not currently attacking, ATTACK's score
goes to ~0, meaning ATTACK is never chosen, meaning there's no fitness
event to ever select the gene back up — a one-way ratchet where the
behavior becomes structurally unreachable, not just currently unselected.
The audit connects this directly to the standing, unsolved
`socialAttraction`/herding mystery (HANDOFF.md, "Herding, partially
mechanised"). An epsilon floor would just be a hardcode by the project's
own rule 8 spirit (rule 8 is literally about gene *bounds*, but the
underlying principle — don't paper over a structural problem with a
constant — applies). The audit's suggested real fix (reachability via
exploration noise in action selection, not the gene's magnitude) is a
bigger design question, not attempted here. Flagged for the mission-queue
work once population balance is settled (HANDOFF §0.5 priority 6).

---

## Noise floor + decision rule — written before the run, per external audit points 1/2/10

The external audit (`EVOSIM-EXTERNAL-REVIEW.md`) made a sharp, correct
point: **every comparison in this investigation so far has been made
without ever measuring seed-to-seed variance at a fixed config.**
"3/4 (5x) vs 4/6 (3x)" was reported as "5x is the leading candidate" —
the audit ran the actual math (Fisher's exact test on that 2x2 table)
and got p≈1.0, with 95% exact intervals of roughly 19-99% and 22-96% —
overlapping across nearly their whole range. **That claim was
unsupported. Retracting it.** 5x is not shown to be better than 3x by
anything in this LEDGER as it stands.

Compounding this: dichotomizing R0 to "> 1 or not" throws away most of
the signal in a continuous variable, and with ~24 CFG arms tried at
n≈2-8 each, the single best result of the session (R0 1.51) is very
plausibly just the max of a large noisy set — the audit's term is
"winner's curse," and it's the right term. **Expect it to regress on
retest.**

**Noise-floor run, decided before firing:** rather than a separate
"true default config" run (which would mostly show near-universal
collapse and measure variance in a regime nobody cares about), the
useful noise floor is at the config actually being compared — the 3x
base `k_photoCost` dose, since it's both the original fix and the arm
with the most data already. Extending 3x to n=30 serves as the noise
floor **and** the comparison group for the eventual 3x-vs-5x call in
one run. (Deviating from the audit's literal "default config" wording
here, deliberately — noted so the reasoning is checkable, not just the
conclusion.)

**Decision rule, written now, before results exist:** run 3x to n≥30
(24 more seeds beyond the 6 already logged: 1337, 4001, 4002, 6060,
6363, 6464) and 5x to n≥30 (26 more beyond the 4 already logged: 1337,
4001, 4002, 7002). Compare the **R0 distributions** (median, IQR, or a
rank test — not the dichotomized fraction). Promote 5x over 3x only if
the gap exceeds one noise-floor SD (estimated from 3x's own n=30
spread); otherwise promote 3x on parsimony (it's the smaller, already-
better-understood change, and "no measured difference" should default
to the simpler existing choice, not the one that happened to look
better on a small sample). Apply the same rule to any future
`k_photoCost`-adjacent claim in this investigation.

**Also retracting, same reasoning:** the "5x... including the best
single result of the whole session" framing from the earlier
dose-response tally entry. That single result (seed 7002, R0 1.51) is
flagged for specific retest — if it reproduces, it's a real find; if it
regresses toward the 3x/5x pooled median, that's the winner's-curse
prediction confirming itself, which is itself worth recording.

Firing the noise-floor batch now (24 seeds, 3x dose) alongside 26 more
5x seeds, both to n=30, both at the new 800-day target.

---

## The deepest finding in the external audit: k_photoCost selection may itself violate the mission test

Audit point 5, and worth sitting with rather than fixing reflexively. The
diagnosis (plants hitting an array-size artifact, not a biological limit)
was sound and independently verified (the arena-isolation test). But the
**selection of the dose** — sweeping `k_photoCost` across 2x/3x/5x and
describing whichever one produced more animal survival as "the leading
candidate" — is a physics constant chosen by its downstream ecological
outcome. The project's own standard, quoted at the top of every governing
doc in this repo: *if a result had to be written into the code, it
doesn't count.* Picking a respiration cost because it happens to let
animals survive is a softer version of the same move as hardcoding a
survival rule directly — the code isn't dictating behavior, but the
*researcher* is dictating which physics gets kept based on whether it
produces the behavior wanted. That's outcome-tuning wearing a physics
costume, and it's a real, substantive violation risk, not a statistical
nuance like points 1-4.

**This is not resolved by more seeds or better statistics on the
existing arms.** No amount of rigor applied to "which dose gives higher
R0" fixes the fact that R0 was the selection criterion in the first
place.

**Proposed fix, not yet executed (queued as top priority, ahead of
finishing the 3x-vs-5x horse race the noise-floor run above was
built for):** choose `k_photoCost` from a criterion independent of
animal outcomes, decided and written down *before* looking at any R0
number, then report whatever ecology results — including "the animals
go extinct at the principled value," if that's what happens. Candidate
criteria, none yet chosen:
- a target respiration-to-gross-photosynthesis ratio (biologically
  interpretable, checkable against real plant physiology as a sanity
  bound)
- pre-fauna standing plant crop as a stated fraction of arena capacity
  (directly targets the original artifact — cap should not bind, but
  the target fraction is chosen for its own sake, not for what it does
  to R0)
- a stated plant-layer turnover time

**What this means for the noise-floor/decision-rule work above:** still
worth having — establishing the natural seed-to-seed spread at a fixed
config is useful groundwork regardless of which criterion eventually
picks the dose, and the 3x-vs-5x statistical comparison is honest as far
as it goes. But the *conclusion* of that comparison should not be read
as "the final answer" even once it lands — it answers "which of these
two arbitrarily-chosen doses is statistically distinguishable," not "is
either of these doses the principled one." HANDOFF §0.5's priority list
is being reordered to put the independent-criterion work ahead of
promoting either 3x or 5x.

---

## Backlog processing, 2026-08-10: riskEwma and confusion-off-retest (2 of 3 seeds each)

Working through `INFLIGHT.json`'s reconstructed backlog. First two results
pulled: `riskewma-test` and `confusion-off-retest`, both at v0.49, both
fired before the audit landed, seeds 1337 and 4001 (4002 not yet landed
for either).

**riskewma-test** (`cfg-patches/photocost-riskewma.json`) — tests
HANDOFF's long-standing herding hypothesis: that a faster-adapting risk
EWMA (lower smoothing) would let the herding/`socialAttraction` gene
actually express as behavior, measured by `actAppr` (the "approach a
same-species neighbor" action share) clearing >1%.

| seed | R0 | mean death age | maturityAge | actAppr |
|---|---|---|---|---|
| 1337 | 0.61 | 14.7d | 62.5d | 0.0% |
| 4001 | 0.23 | 1.1d | 14.4d | 0.2% |

Both seeds: R0 < 1, not viable, dying well before maturity. `actAppr`
stayed at 0.0%/0.2% — under the >1% falsifier the original prediction set.
**Read this as a miss on n=2**, not a confirmation and not yet a full
retraction (n=2 is too small to close the herding question outright, and
both populations were also failing on food/survival grounds independent
of herding, which muddies attributing the flat `actAppr` specifically to
the EWMA change rather than to general population collapse). Recorded
honestly rather than left silently unprocessed. Third seed (4002) still
outstanding; if it also shows actAppr flat, that's reasonably strong
grounds to close this specific mechanism as insufficient on its own and
return to the absorbing-state hypothesis (see the v0.50 UNRESOLVED flag)
as the more likely explanation for herding never appearing.

**confusion-off-retest** (`cfg-patches/photocost-confusion-off.json`) —
clean re-run of the original v0.47 `k_confusion:0` finding, now under the
`k_photoCost` fix that removes the `maxPlants` confound the original test
never controlled for.

| seed | R0 | mean death age | maturityAge | actAppr |
|---|---|---|---|---|
| 1337 | 0.64 | 4.6d | 8.6d | 0.0% |
| 4001 | 0.70 | 13.1d | 35.3d | 0.0% |

Both R0 < 1 with `k_confusion` disabled. This is a genuinely useful data
point: the original v0.47 conclusion (disabling confusion/herding defense
causes population failure) survives on these two seeds even with the
`maxPlants` artifact controlled for — i.e. this specific finding does not
look like it was just an artifact of the food-base confound. **Still not
a confirmed comparison** — no confusion-ON base-dose R0 numbers at the
same photocost dose have been pulled alongside these yet, so "R0 < 1 with
confusion off" isn't yet contrasted against "R0 ? with confusion on" at
the same dose. Filed as MODERATE-strength directional support for the
original finding, not as a re-confirmed result, per the no-dichotomizing/
small-n discipline written up in the noise-floor section above. Third
seed (4002) outstanding.

`INFLIGHT.json` updated: both entries moved to `partially_collected` (2
of 3 seeds landed) with these R0 numbers noted.

---

## Backlog processing, 2026-08-10 (continued): remaining CFG-variant branches

Pulled every other `runs/*` branch still sitting unprocessed in
`INFLIGHT.json`. Consolidating rather than one entry per label — the
pattern across all of them is the story, not any individual number.

| label | seed(s) landed | R0 |
|---|---|---|
| retal-test | 1337 | 0.58 |
| armeff-test | 1337, 4001 | 0.44, **1.00** |
| animal-headroom | 1337, 4001 | 0.73, 0.71 |
| mixedfree-dose | 1337, 4001 | 0.71, 0.45 |
| hi-gutcost-stack | 1337, 4001, 4002 (complete) | 0.95, 0.95, 0.46 |
| lo-gutcost-stack | 1337, 4001 | 0.76, 0.69 |
| triple-stack | 1337, 4001 | 0.59, 0.77 |
| gutcost-carrionfloor-stack | 1337, 4001 | 0.71, 0.95 |
| photocost-lo-confirm | 4001, 4002, 7001 (complete) | 0.67, 0.59, 0.88 |
| photocost-abase-confirm | 4001, 4002 (complete) | 0.70, 0.65 |
| photocost-carrionfloor-confirm | 4001, 4002 (complete) | 0.66, 0.69 |

19 seed-results, **1 at parity (armeff-test seed 4001, R0 1.00, exactly on
the boundary), 0 above 1, 18 below 1.** None of the specific hypotheses
tested here (retaliation cost, armour efficacy, bigger animal headroom,
mixed-diet free parameter, gutcost stacked on top of the dose, carrionFloor
variants) shows a clear rescue effect — nothing clusters meaningfully above
where the base dose alone sits.

This matters for more than each individual label: it's more evidence for
the point already flagged in the noise-floor section — the whole
neighborhood of CFG space being explored here sits close to R0≈1, with
result-to-result variance (seed, not treatment) large enough to swing
individual runs from ~0.4 to ~1.0 without a clear treatment signal. That's
exactly the regime where small-n "leading candidate" claims are least
trustworthy, and exactly why the noise-floor/n≥30 protocol above is the
right next step rather than reading any of these numbers as a verdict on
their respective hypotheses. None of these labels is being promoted,
retested at higher n, or deprioritized further based on this batch alone
— they're recorded as data, not conclusions.

`photocost-lo-confirm`, `photocost-abase-confirm`, and
`photocost-carrionfloor-confirm` are now at their originally-planned seed
counts (marked `collected` in `INFLIGHT.json`). The rest remain
`partially_collected` pending their outstanding seed(s) — `retal-test`
seeds 4001/4002, `armeff-test` seed 4002, `animal-headroom`/`mixedfree-dose`/
`lo-gutcost-stack`/`triple-stack`/`gutcost-carrionfloor-stack` seed 4002
each. `hi-confirm-batch2` (5151/7777/8888) and `hi-confirm-batch3`
(6060/6363) have no branches pushed yet as of this check — still running
or queued, not yet actionable.

---

## Stationarity plan (external audit point 4), not yet executed

Point 4's argument: a run that hasn't reached stationarity biases R0
comparisons, it doesn't just add noise — an arm that's still trending
down at day 800 will read as "worse" than one that happened to plateau
earlier, independent of any real difference. `analyze.py`'s stationarity
gate already flags this per-run; what's missing is a systematic check
that the doses being compared (2x/3x/5x `k_photoCost`) aren't being
ranked while one or more of them is still non-stationary at the 800-day
cutoff.

**Plan, queued, not yet run:** once the noise-floor batches
(`noisefloor-3x`/`noisefloor-5x`) are collected, pick 3-4 seeds per dose
and compare R0 computed over day-400, day-800 (current cutoff), and
day-1200 windows (a longer run, not a re-slice of the same 800-day log —
population trajectory can't be reconstructed retroactively past where the
log stops). If the ranking between doses is stable across those three
windows, that's evidence the 800-day comparison isn't a stationarity
artifact. If it flips, the comparison needs the longer cutoff. This is a
Tier A extension (already-approved noise-floor protocol, just reading it
with an extra lens) once the base batches land — no new hypothesis, just
an extra window on data already being collected.

## Compute status, 2026-08-10 ~05:30

14 Actions workflow runs in progress at time of writing, including the
two 15-seed noise-floor matrices — likely at or near the account's
observed concurrency ceiling. Per the same-day policy reconciliation
above (CLAUDE.md, external audit point 9), holding off firing anything
new until this batch clears rather than adding to an already-saturated
queue. Two Tier A retests are queued next once headroom opens: the
v0.50 ecological retest (`v050-attack-floor-test`, invalidated, needs
re-fire against the k_meatAttr-pivoted file) and the seed-7002 winner's-
curse retest (external audit point 3, flagged earlier this session,
never fired).

---

## Heartbeat, 2026-08-10 ~06:00: 5x-dose confirm results, both very weak

Two more seeds landed from the pre-audit 5x confirm batches (`hi-confirm-batch2`
seed 8888, `hi-confirm-batch3` seed 6060 — the latter being the specific
targeted retest of the seed that broke the 3x pattern, at 5x instead).

| label | seed | R0 | death age | maturityAge | matter drift |
|---|---|---|---|---|---|
| hi-confirm-batch2 | 8888 | 0.03 | 2.1d | 36.9d | 0.000000% |
| hi-confirm-batch3 | 6060 | 0.03 | 2.0d | 41.9d | 0.000000% |

Both essentially collapse (R0 0.03, dying at ~5% of maturity age) — the
weakest results seen yet in this whole investigation, and notably
**seed 6060 does not get rescued by 5x** — at 3x it was extinct with R0
0.25 (see the "6060 correction" entry above); at 5x it's worse, not
better. That's a direct data point against the already-retracted "5x
rescues the hard seeds" framing — worth having on record precisely
because it points the opposite direction from what that framing would
have predicted. Matter-conservation clean on both, `caps seen [0]` on
both (not slot-cap-bound). No local jobs finished this cycle (three
1200-day runs from the prior session still in progress: seed 5151,
7575-lo, 8686-gutcost). `noisefloor-3x`/`noisefloor-5x` (30 seeds
total) have not landed any results yet — still queued behind the
Actions concurrency ceiling.

---

## v0.50 re-test, corrected build, seed 1337 (first of 3)

First ecological data point for the k_meatAttr-pivoted fix (all prior
v0.50 data was invalidated by the confounded-gain bug, see the
correction entry above). Compared against the same v0.49 baseline used
before (`fast-batch-photocost` seed 1337: R0 1.21, ratio 0.60, actAttack
0.8%, harmonic N 43):

| | v0.49 | v0.50 (corrected) |
|---|---|---|
| R0 | 1.21 | 0.78 |
| ratio | 0.60 | 0.29 |
| actAttack | 0.8% | 0.6% |
| harmonic N | 43 | 27 |
| matter drift | — | 0.000000% |

**Reading this carefully, not overclaiming on n=1.** `actAttack` barely
moved (0.8%→0.6%) — nowhere near the 0.8%→0.1% collapse the *confounded*
version showed, which is itself informative: most of that earlier crash
in `actAttack` really was the gain-reduction bug, not the floor removal.
That's evidence the fix worked as intended on the mechanism the audit
flagged. But R0, ratio, and harmonic N all fell substantially anyway —
on a change that's supposed to be close to a no-op at this gene value.
Per the same caveat carried since v0.49's occupied-slot-list change: a
genuine formula edit (not measurement-only) can shift the RNG draw
sequence and produce a real single-seed swing unrelated to the
ecological claim. Not scoreable as hit or miss yet. Seed 4001 now
running locally; seed 4002 still to come, to reach the original 3-seed
plan for `v050-attack-floor-test`.

## Base-dose tally, 8th seed: 5151, R0 0.75

Extends the 3x `k_photoCost` base-dose tally (previously 4/6 R0>1: 1337,
4001, 4002, 6464 survived; 6060, 6363 extinct). Seed 5151: R0 0.75,
ratio 0.91, `actAttack` 1.7%, matter clean, but **`caps seen [0, 1]`** —
this run did touch the plant slot-array bound at least once, unlike most
of the recent tally. Revised count: **4 of 7 (57%)** at the original
6-seed-plus-1 tally; this is separate bookkeeping from the dedicated
`noisefloor-3x` n≥30 batch (still queued behind the Actions ceiling,
0/15 landed) — this seed is being folded in as an extra data point, not
a substitute for that batch. A fresh local seed (30001) now running to
keep this line moving while the two v0.50-retest seeds also run.

---

## Heartbeat, 2026-08-10 ~06:45: large Actions batch landed

Substantial batch of Actions results landed since the last check. Processing
all of it in one entry.

### noisefloor-3x — 7 of 15 seeds landed, hit rate lower than the ad-hoc tally

| seed | R0 |
|---|---|
| 10001 | 0.64 |
| 10004 | **1.12** |
| 10005 | 0.18 |
| 10006 | 0.25 |
| 10008 | 0.66 |
| 10009 | 0.70 |
| 10010 | 0.18 |

**1 of 7 (14%) R0>1.** This is the dedicated, non-cherry-picked noise-floor
sample for the 3x dose — and it's running noticeably lower than the
informal tally built from the original seeds (1337/4001/4002/6464/6060/
6363/5151, 4/7 = 57%). Two live explanations, not yet distinguishable at
n=7: (a) genuine high variance and this is still noise at small n, or (b)
the original seed set was inadvertently non-representative (picked in
the course of exploration rather than drawn cold). Not concluding either
way yet — this is exactly why the noise-floor protocol exists, and it's
doing its job by surfacing this gap early rather than after a doomed
promotion decision. 8 more seeds still to land for this batch.

### 5x dose — full tally now 9 seeds, revised down to 33%

Combining the original screen (1337 1.16✓, 4001 1.08✓, 7002 1.51✓, 4002
0.22✗ — 3/4) with the two confirm batches that just landed complete:

| seed | R0 | batch |
|---|---|---|
| 5151 | 0.49 | hi-confirm-batch2 |
| 7777 | 0.33 | hi-confirm-batch2 |
| 8888 | 0.03 | hi-confirm-batch2 |
| 6060 | 0.03 | hi-confirm-batch3 (targeted retest — 3x gave 0.25, 5x is *worse*) |
| 6363 | 0.07 | hi-confirm-batch3 (targeted retest — 3x gave 0.76, 5x is *worse*) |

**9 seeds total, 3/9 (33%) R0>1** — a sharp revision down from the
originally-reported "75% at n=4." This is the clearest evidence yet that
the earlier "5x may be the better constant" read (already once retracted
via the audit's Fisher's-exact-test point) was winner's-curse-driven: the
first 4 seeds happened to include the session's single best result
(7002, 1.51) and no catastrophic failures; the next 5 landed 0/5. Neither
targeted retest seed was rescued by the higher dose — both did *worse*
at 5x than they did at 3x. **5x is not "ahead" of anything at this point
— if anything the fuller sample makes 3x's ad-hoc 57% look relatively
better, though both now look shakier than either looked at n=4-6.**
`noisefloor-5x` (dedicated batch, 15 more seeds) is still 0/15 landed —
that will be the real answer, not this ad-hoc reconstruction.

### confusion-off-retest — complete, 3/3, all R0<1

| seed | R0 |
|---|---|
| 1337 | 0.64 |
| 4001 | 0.70 |
| 4002 | 0.79 |

Completes the clean re-test of the original v0.47 `k_confusion:0` finding
under the fixed food base. **All three seeds R0<1.** Directionally
consistent with the original finding (disabling confusion/herding
defense hurts population health) surviving the `maxPlants` fix — though
this still isn't a true A/B: no confusion-ON run at the identical dose
and seeds has been pulled alongside these for direct comparison. Given
the base-dose tally itself hovers around 50-60% R0>1 depending which
seed set is used (see the noise-floor gap above), three R0<1 seeds
in a row on the confusion-off arm is suggestive but not yet distinguishable
from the general weakness this whole neighborhood of CFG space is
showing. Filed as MODERATE, not upgraded to HIGH.

### animal-headroom — complete, 3/3, all R0<1

1337 0.73, 4001 0.71, 4002 0.81. No rescue effect from bigger
animal-population headroom.

### Other completions/updates

- **retal-test**: 2/3 now (1337 0.58, 4001 0.85). Seed 4002 still out.
- **triple-stack**: complete, 3/3 (1337 0.59, 4001 0.77, 4002 0.70).
- **lo-gutcost-stack**: complete, 3/3 (1337 0.76, 4001 0.69, 4002 0.49).

None of these show a rescue effect either — consistent with everything
else in this backlog.

### Bookkeeping correction: two different carrionFloor+gutcost combos got
### merged under one label

Checking the actual `cfg` block inside the fetched JSON (not just the
branch name) turned up a mistake in this session's own tracking: seeds
1337/4001 (R0 0.71/0.95, previously filed under "carrionfloor-lo-gutcost")
were pushed to branch `runs/gutcost-carrionfloor-stack/*` running
**`carrionFloor 0.10`** (`cfg-patches/gutcost-carrionfloor-combo.json`).
Seed 4002 (R0 0.67) landed separately on branch
`runs/carrionfloor-lo-gutcost/*` running **`carrionFloor 0.05`**
(`cfg-patches/carrionfloor-lower-gutcost.json`, the dose-response follow-on
testing a lower floor than the 0.10 combo). These are two different CFG
arms, not three seeds of one arm. Corrected in `INFLIGHT.json`:
- `gutcost-carrionfloor-combo` (carrionFloor 0.10): seeds 1337 (0.71), 4001
  (0.95) — 2 seeds, no third fired yet under this exact cfg.
- `carrionfloor-lo-gutcost` (carrionFloor 0.05): seed 4002 (0.67) only —
  1 seed, needs 1337/4001 to complete the originally-planned 3.
Neither shows a rescue effect either way (all three raw numbers are in
the same weak 0.67-0.95 neighborhood as everything else this cycle).

---

## Gutcost combo, 9th seed: 8686, R0 1.15 — but flags the stationarity question directly

Local run, 1200 days (longer than the standard 800-day cutoff). R0 1.15,
ratio 0.87, matter clean, `caps seen [0, 1]`. **Revises the gutcost-combo
tally to 3/9 (33%)** — still well below the base dose's own tallies, not
changing the "doesn't outperform the dose alone" conclusion, but a hit,
not a miss, this time.

**More useful than the R0 number itself: this run is a concrete example of
the stationarity concern from the plan written above.** At 1200 days —
50% longer than the standard cutoff — `analyze.py`'s own gate says
`plants +14.5%/100d NOT STATIONARY`, `bio -26.5%/100d DRIFTING`, `animals
+23.0%/100d NOT STATIONARY`. If a run this long still hasn't settled, the
800-day cutoff used everywhere else in this investigation is almost
certainly reading transient dynamics, not equilibrium — R0 1.15 here
could easily still be rising or about to fall. This doesn't invalidate
anything already recorded (every comparison so far has used the same
800-day cutoff consistently, so relative comparisons between arms are
less affected than any individual arm's absolute number), but it's a
concrete, load-bearing data point for the stationarity plan, not just a
theoretical worry anymore. Worth prioritizing a couple of matched
800-vs-1200-vs-1600-day runs at the same seed/cfg once the noise-floor
batches are further along, to see whether R0 keeps drifting the same
direction or genuinely settles.

---

## Full-corpus re-tally, 2026-08-10 — three of my own conclusions do not survive it

Prompted by a "check everything" pass. Instead of trusting the prose
tallies scattered through this file, I re-derived every arm from scratch:
walked all 91 logs on disk (repo + local runs + fetched Actions results),
grouped them by **actual cfg diff read out of each log's own `cfg` block**
rather than by the label or patch filename it was fired under, and
recomputed R0 with a reimplementation verified line-for-line against
`analyze.py`'s output on three files (1.15/0.78/0.75, exact matches).
84 logs yielded a computable R0.

### The measured noise floor, at last

| arm | n | mean R0 | SD | median | range |
|---|---|---|---|---|---|
| base dose (3x, `k_photoCost` 0.012) | 14 | 0.73 | 0.39 | 0.72 | 0.18-1.31 |
| 5x (0.020) | 9 | 0.55 | 0.53 | 0.33 | 0.03-1.51 |
| gutcost combo | 8 | 0.92 | 0.25 | 0.91 | 0.58-1.37 |
| 2x (0.008) | 4 | 0.98 | 0.48 | 0.78 | 0.59-1.80 |

**Within-cfg seed-to-seed SD is 0.25-0.53 in R0.** That is the number
this whole investigation needed on day one and never had. With SD 0.39,
the sample size needed to detect a given difference in mean R0 at 80%
power:

| difference to detect | n per arm |
|---|---|
| 0.1 | 239 |
| 0.2 | 60 |
| 0.3 | 27 |
| 0.4 | 15 |
| 0.5 | 10 |

**The largest gap between any two arms above is 0.37 (5x vs 2x means);
the gap that actually drove decisions — base 0.73 vs gutcost 0.92 — is
0.19, needing n≈60 per arm. Real n was 14 and 8.** Essentially every CFG
comparison made this session has been ~4-7x underpowered. The external
audit said this in the abstract; this is the arithmetic.

### Correction 1 — the "noise-floor gap" I flagged one cycle ago was me misreading noise, again

Last cycle I reported that `noisefloor-3x` (1/7 R0>1) was running "well
below" the ad-hoc base-dose tally (4/7) and raised "whether the original
seed set was inadvertently non-representative" as a live hypothesis.

Tested properly: **Fisher exact two-sided p = 0.266; permutation test on
the median difference p = 0.186.** Neither is close to significant. The
two subsets are entirely consistent with binomial variation around the
pooled rate. There is no gap to explain. Pooled, the base dose is
**5/14 (36%) R0>1, median 0.72**.

Worth naming plainly: I wrote the decision rule warning against exactly
this kind of small-n overread, and then made the same error one cycle
later on the very batch that rule was written for. The rule was not
enough on its own; running the test before writing the sentence is what
would have caught it.

### Correction 2 — the gutcost combo was deprioritized on a dichotomized statistic, and that call does not survive

The deprioritization ("Closing this branch of investigation... the base
`k_photoCost` dose alone is the finding worth carrying forward") rested
on "2/5 (40%) vs the base dose's 3/5 (60%)", later "2/8 vs 4/6". That is
a dichotomized R0>1 comparison — the specific move the external audit
told me to stop making.

On the full corpus, distributionally:

- hit rate: gutcost **3/8** vs base **5/14** — Fisher exact **p = 1.000**.
  Not a difference; not even a hint of one.
- median: gutcost **0.91** vs base **0.72**, difference **+0.18** in
  gutcost's favour, permutation p = 0.406 — also not significant.
- spread: gutcost **SD 0.25, min 0.58**; base **SD 0.39, min 0.18**.

So: the gutcost combo is **not** demonstrably better than the base dose —
but it was never demonstrably worse either, and it has the highest median
and the tightest distribution of any arm with n≥8 in the corpus. **The
verdict "does not outperform the dose alone, closing this branch" is
retracted.** The correct statement is that base dose and gutcost combo are
statistically indistinguishable on every measure available, and if
anything the ordering implied by the point estimates runs the *other*
way from the one I acted on.

### Correction 3 — the headline the whole corpus supports

Every arm in the table above has **mean and median R0 below 1.0.** The
best median of any arm with n≥8 is gutcost's 0.91. Pooling all 84 runs,
no configuration tested this session is demographically viable; the
populations are all shrinking, some faster than others, and the
differences between them are inside the noise.

That is a substantially different — and much more honest — summary than
"the base dose is the finding worth carrying forward, 5x may be better."
The dose-response investigation did not find a viable configuration. It
found that `k_photoCost` moves the plant equilibrium off the `maxPlants`
artifact (that part is real, confirmed by a control, and stands), and
then spent ~24 arms at n≤9 failing to distinguish anything downstream of
that because every candidate difference was smaller than the noise.

### What this implies for what to do next

Not "more seeds on the dose comparison." At n=60 per arm to resolve 0.2 in
R0, finishing the 3x-vs-5x horse race honestly costs ~120 runs to answer a
question whose answer is already "both are well under 1, so neither is the
configuration you want." **The bottleneck is not which dose — it is that
nothing tested reaches replacement.** Chasing 0.7 vs 0.9 is optimizing
inside a regime that is failing for a reason none of these constants
addresses.

One arm in the corpus does stand out and has never been extended: base
photocost at the **original full 90k/40k arena**, n=2, **2/2 above 1
(R0 1.21, 1.42)** — the only arm where every seed cleared replacement.
n=2 is nothing on its own (and the sample-size table above says so
loudly), but it is the only untested-at-scale direction pointing anywhere
other than sideways, and it is a *scale* change rather than another
cost-constant tweak. Flagged as the highest-value next test; not fired
here, and it needs its own written prediction first.

### Same pass — the v0.50 pivot's own comment was overclaiming

Reading [L0.50-1] against the arbiter code rather than against my memory
of it: the source comment said the unfloored ATTACK score "matches"
GRAZE/SCAVENGE's unfloored attraction genes. It doesn't, and can't.

- SCAVENGE: `*G[carrionAttraction]` — bare gene, span [0,1]
- APPROACH: `*G[socialAttraction]` — bare gene, span [0,1]
- FLEE: `*G[fearThreshold]` — bare gene, span [0,1]
- ATTACK (v0.50): `*k_meatAttr*G[meatAttraction]` — span **[0,6]**

The old form was **affine** (`0.5 + g`, span 1.0 offset by 0.5); the new
form is **linear** (`k*g`). An affine function cannot be matched by a
linear one at more than a single point, so *any* unflooring has to give
something up: match the siblings' gain (bare gene, k=1) and you cut the
founder-value score 6x — the confound the external audit caught — or
preserve the founder value (k=6, what's shipped) and the slope
necessarily steepens 6x relative to the siblings.

Shipping the pivot is still the right call: it's the project's own
documented discipline (HANDOFF §2b), and it isolates the change being
tested at the operating point where the population actually sits. But
"matches GRAZE/SCAVENGE" was wrong and is now corrected in the source to
"matches in REACHABILITY, not in gain." Comment-only edit, no executable
line touched (verified by diff), `node check.js` PASS, no version bump —
nothing about behaviour changed, only a claim that was overstated.

Worth flagging for whoever picks up the absorbing-state question: the 6x
slope means selection on `meatAttraction` now has 6x the behavioural
leverage above the founder value that it had before, which is a real
(if deliberate) second-order consequence of this version, and is *not*
what the v0.50 prediction was written against.

---

## Correction 4, same day — I made the same error again in the act of reporting the first three

In the write-up of the full-corpus re-tally above I flagged the
"full 90k/40k arena at base photocost" as a standout: *"n=2, 2/2 above
replacement (R0 1.21, 1.42) — the only arm where every seed cleared
replacement... the highest-value next test."*

That was wrong, and checking it took two minutes:

| seed | maxPlants | R0 | max plants reached |
|---|---|---|---|
| 1337 | 90000 | **1.2096** | 18462 |
| 1337 | 25000 | **1.2096** | — |
| 6262 | 90000 | 1.4183 | 16734 |

Seed 1337 is **bit-identical at both arena sizes** (1.2096 to four
decimal places), and neither full-arena run ever came within 6,000 plants
of the 25k cap. The cap never binds, so the arena size is inert — which
is precisely what the arena-isolation test established in the first
place, and which `FINDINGS.md` already records as HIGH confidence.

So the "full-arena arm" is not an arm. It is **one duplicate of a
base-dose run I had already counted, plus one ordinary base-dose seed
(6262) that happened to be run with a larger, never-binding array
allocation.** Reporting it as "2/2, the only arm where every seed
cleared" double-counted 1337 across two groups and then read the
resulting overlap as a difference between them.

**Corrected base-dose tally**, folding in 6262 (arena inert, so it is a
base-dose seed) and the newly-landed 30001 (R0 0.72):
**16 seeds, 6/16 (38%) R0>1, median 0.72.**

Worth stating without softening: this is the fourth error of the same
family in one session, and I made it *in the same message* where I
reported catching the first three, while explicitly warning that n=2
proves nothing. Writing the caveat next to the claim did not stop me
making the claim. The thing that actually caught it was running one
query against the logs. **Cheap mechanical checks beat carefully-worded
hedges** — the hedge makes a wrong claim look responsible, the query
makes it go away.

---

## New diagnostic: is `aRate/aUpkeep` an emergent equilibrium or a parameter?

**The observation that prompted this.** Pulling the animal-energetics
lines across three arms with very different outcomes:

| run | R0 | aRate/aUpkeep | death age / maturityAge | starved share of deaths |
|---|---|---|---|---|
| 30001 (base dose) | 0.72 | **1.19** | 0.46 | 85% |
| 6262 (base dose) | 1.42 | **1.20** | 0.82 | 59% |
| 8686 (gutcost) | 1.15 | **1.18** | 0.87 | 67% |

`aRate/aUpkeep` — realised intake rate over upkeep — is pinned at
**1.18-1.20 across arms whose R0 differs by 2x.** Nothing was tuned to
make that happen; no constant in any of these three cfgs sets it. That
is the signature of a **density-dependent equilibrium**: selection
converts any intake surplus into more animals until competition drags
the realised rate back down to just above break-even. If real, it is
the single most on-mission result in this corpus — regulation *emerging*
from the physics rather than being written into it — and it has been
sitting in the digest output unremarked all session.

It also reframes the whole dose-response investigation: if the animals
self-regulate to ~1.19 regardless, then plant-side constants can only
move *how many* animals sit at that ratio, not whether they clear
replacement. That would explain why ~24 arms all landed in the same
0.5-1.0 R0 band.

**Falsifiable prediction, written before the run.** Arm:
`k_intake` 0.01486 → 0.02229 (+50%), base photocost dose and arena,
`cfg-patches/intake-regulation-probe.json`. Seeds 1337, 4001, 4002 —
chosen because all three have matched base-dose values on record
(1.21, 1.03, 1.31; mean **1.18**).

Powered honestly: with within-cfg SD 0.39 (measured above), a 3-seed
mean has SE ≈ 0.23, so only a shift larger than ~0.45 is detectable.
This test is deliberately powered to detect a *large* effect or nothing;
it will be reported as "large effect / no large effect" and never as a
point estimate.

- **HIT (regulation is emergent):** `aRate/aUpkeep` returns to
  **1.10-1.30**, mean R0 stays within ±0.45 of 1.18 (i.e. 0.73-1.63),
  and standing animal N rises **>25%**. Reading: the extra intake is
  absorbed by more animals, not by better per-animal demography.
- **MISS (ratio is parameter-set, not regulated):** `aRate/aUpkeep`
  settles **above 1.35** and stays there, **or** mean R0 exceeds 1.63.
  Either would mean the population is not self-regulating and the ratio
  is being set exogenously — which would make it a legitimate target
  for a physics correction, and would also mean the emergent-regulation
  reading above is wrong.

**Mission-test guard, stated up front:** this is a sensitivity probe,
not a search for a `k_intake` that produces R0>1. No value of `k_intake`
gets promoted on the basis of raising R0 — that is exactly the
outcome-tuning-in-a-physics-costume error already logged against the
`k_photoCost` dose selection. The question here is *whether the system
regulates*, and a HIT means leaving `k_intake` alone.

Firing seed 1337 now (one local core free); 4001/4002 to follow as cores
free up.

### Scoring the emergent-regulation diagnostic: hypothesis NOT SUPPORTED, withdrawn

The `aRate/aUpkeep` invariance is real as a *measurement* — across 86 runs
spanning `k_photoCost` 0.004-0.020 and R0 from 0.02 to 1.80, the ratio
holds at **1.166 ± 0.089** (CV 0.076 vs R0's 0.528, i.e. 7x more tightly
held). The k_intake +50% arm came back at 1.179, right on the corpus mean.
On the face of it that looks exactly like density-dependent regulation.

**It isn't, and two free checks against existing logs show why.**

**Check 1 — the trajectory test.** Regulation predicts the ratio starts
high at low density right after fauna arrive (day 260, plants abundant,
few animals) and *decays* as density builds. Survivorship filtering
predicts no such systematic decay.

| seed | d260-300 | d300-400 | d400-600 | d600+ | N d260-300 | N d600+ |
|---|---|---|---|---|---|---|
| 6262 | 1.29 | 1.02 | 1.20 | 1.23 | 177 | 139 |
| 30001 | 1.30 | 1.17 | 1.19 | 1.20 | 144 | 45 |
| 8686 | 1.28 | 1.19 | 1.19 | 1.17 | 200 | 256 |
| 6464 | **1.07** | 1.14 | 1.25 | **1.26** | 124 | 209 |

No consistent decay. **6464 moves the opposite way** — ratio *rises*
1.07→1.26 while density nearly doubles (124→209), which is the exact
reverse of a competition-driven equilibrium. And 8686 holds 1.17 while
density rises 200→256, where 6262 holds ~1.2 while density *falls*
177→139. The ratio does not track density in any consistent direction.

**Check 2 — the mechanism is more parsimoniously explained.** Both
`AN.rate` and `AN.up` are averaged over **living animals only**
(`aRt += AN.rate[i]` at line 3263, summed across the standing
population). An animal whose realised rate sits below upkeep depletes
reserves and starves out. So the surviving population is *filtered* to
rate ≳ upkeep by construction — a mean just above 1.0 is what that
filter produces on its own, no regulation required. On top of that
`AN.rate` is an EWMA with `rateEwma = 0.002`, an extremely slow
smoothing constant that mechanically compresses the statistic's
variance. Survivorship floor + heavy smoothing account for both the
level and the tightness without invoking any emergent feedback.

**So the hypothesis is withdrawn.** It never reached `FINDINGS.md` — the
check happened first, which is the process working the way it was
supposed to. What stands is the narrower, duller claim: *aRate/aUpkeep is
a survivorship-filtered, heavily-smoothed statistic that sits just above
1 in almost any run, and therefore carries much less information about
population health than its tightness suggests.* That is worth knowing
precisely because its stability is misleading.

**The probe run itself is compromised as evidence.** Seed 1337 at
`k_intake` +50% did not reach a steady state — it went **extinct**:

| window | mean N |
|---|---|
| d260-350 | 90 |
| d450-550 | 56 |
| d550-650 | **1** |
| d750-810 | **0** |

The digest's "aRate/aUpkeep 1.18" is computed over the last 200 samples,
i.e. over a population of zero-to-one animals. It is noise, not a
measurement, and the fact that it landed neatly on the corpus mean is
coincidence. R0 0.56 likewise describes a collapse, not an equilibrium.

**Prediction scored: neither HIT nor MISS as written — the prediction was
badly specified.** I defined HIT as (ratio 1.10-1.30) AND (R0 within
±0.45 of 1.18) AND (standing N up >25%), MISS as (ratio >1.35 sustained)
OR (mean R0 >1.63). Seed 1337 gave ratio 1.18 (HIT band), R0 0.56 (below
the HIT band), N down 100% (not up). **Extinction was not a branch I
wrote**, so the outcome falls through the specification entirely. A
prediction whose HIT/MISS conditions don't tile the outcome space isn't
falsifiable in the way it claims to be — noting that as a defect in how I
wrote it, not patching it after the fact.

**The process lesson, which is the real one here.** Both checks that
killed this hypothesis ran against logs already on disk, cost no compute,
and took about two minutes. I fired the probe *before* running either.
The order should have been: cheap check against existing data first, new
run only for what existing data genuinely cannot answer. That is the
same lesson as Correction 4 above, and it is now the second time today
the fix was a query I already had the data to run.

**Continuing the arm anyway, with a different question.** Seeds 4001
(running) and 4002 still complete the 3-seed protocol on record, but what
they now test is not regulation — it is whether **a 50% intake increase
reliably drives extinction**, which is counterintuitive enough to be
worth the two runs (plausible mechanism: faster harvesting depletes the
plant layer faster, converting a marginal equilibrium into boom-bust).
That is a *new* reading of an already-fired arm, and it gets its own
honest n=1-so-far label until 4001/4002 land, not a promotion to finding.

---

## Cap-binding audit, 2026-08-10 — 29% of base-dose runs still ride the artifact, and the best-looking dose is the most contaminated

Zero-compute check against the 86 logs already on disk, prompted by
noticing `caps seen [0, 1]` in runs I had been counting as clean. `caps`
is a bitmask written every sample (`v0_49` line 3251): **bit 0 = plant
slot array full**, bit 1 = animal array full, bit 2 = seed pool near its
own fraction bound. Nobody had audited it across the corpus.

**The animal cap never binds anywhere: 0/86 runs.** `maxAnimals` is not
and has never been a constraint. The plant cap is another matter.

Normalized to `maxPlants` 25000 (the arena everything recent uses, so
doses are compared against the same bound):

| dose | n | runs that hit the plant cap | mean fraction of run capped | median peak plants |
|---|---|---|---|---|
| 0.004 (default) | 5 | 1/5 | 0.083 | 15488 |
| 0.008 (2x) | 7 | **5/7** | **0.243** | **24630** |
| 0.012 (3x, base) | 52 | **15/52 (29%)** | 0.061 | 18216 |
| 0.020 (5x) | 12 | 2/12 | **0.008** | 12067 |

**Finding 1 — the base dose does not actually clear the artifact.** 29%
of 3x runs still hit the plant slot cap at some point. The whole
investigation has treated 3x as "off the artifact"; for roughly three
runs in ten it isn't, and that was never checked.

**Finding 2 — the dose that looked demographically best is the one most
pinned against the artifact it was supposed to remove.** 2x has the best
mean R0 of any arm (0.98, from the re-tally above) and is *also* the
worst offender here by a wide margin: 5 of 7 runs hit the cap, a quarter
of run-time spent capped, median peak plants 24630 against a bound of
25000 — essentially pinned. Its demographic advantage is not
independent of the artifact; the most likely reading is that 2x looks
good *because* it is still riding an inflated food base.

**Finding 3 — capped runs bias R0 upward, so the corpus slightly
overstates viability.** Within 3x-dose runs: capped mean R0 **0.84**
vs uncapped **0.70** (difference +0.14, permutation p = 0.103; R0>1 rate
4/15 vs 6/37). Not significant at n=52, and I am not claiming it as
established — but the direction is what mechanism predicts (cap binding
means abundant plants means more food), so it should be treated as a
live upward bias rather than dismissed on p>0.05.

### This hands the mission-test problem an outcome-independent criterion

The unresolved objection logged earlier (audit point 5) is that choosing
`k_photoCost` by which dose yields more animal survival is outcome-tuning
in a physics costume. One of the three candidate replacements proposed
there was *"pre-fauna standing plant crop as a stated fraction of arena
capacity — targets the original artifact, chosen for its own sake, not
for what it does to R0."*

**Cap-binding frequency is exactly that criterion, and it is already
measured in every log.** It is computed entirely from plant dynamics,
makes no reference to animals, and answers precisely the question the
intervention was introduced to answer: does the plant population stay
off the array bound? By that criterion the ranking is unambiguous:
**5x (frac 0.008, peak 12067) ≫ 3x (0.061) > default (0.083) ≫ 2x
(0.243)**.

**And it points the opposite way from the outcome criterion.** 5x is
cleanest on the principled measure and has the *worst* demography of any
arm (mean R0 0.55). 2x is dirtiest and has the *best* (0.98). Had I kept
selecting on R0, I would have promoted the most contaminated
configuration in the corpus — which is the concrete form the audit's
abstract warning takes here, and a much better argument for the audit's
point than the audit itself made.

**Not promoting 5x on this basis either, yet.** Two reasons. (a) The
criterion needs a *threshold stated in advance* — "cap binds in <5% of
runs" or "peak plants below 60% of the array bound" — chosen for
plant-physiology reasons rather than picked after seeing which dose wins,
or it is just outcome-tuning against a different outcome. (b) A dose
that keeps plants off the cap while driving animals extinct has not
solved the ecology; it has traded one broken regime for another. The
honest position is that **the plant-side artifact and the animal-side
viability failure are two separate problems**, the corpus has been
conflating them, and no single `k_photoCost` value is currently known to
fix both.

### Consequence for the corpus

Every R0 comparison in this file pools capped and uncapped runs. The
cleanest available reading of the base dose is the **uncapped subset**,
and it is worse than the pooled number: mean R0 0.70, 6/37 above
replacement. The pooled figures reported earlier are not withdrawn — the
capped/uncapped difference is not significant — but they carry a known
upward bias whose size is about +0.14 in mean R0.

---

## Heartbeat ~08:15 — a correctness finding that outranks the ecology

### The "matter leak" is a rounding artifact, and it invalidates how this project has been *phrasing* its conservation checks

`analyze.py` flagged `matter 7533 -> 7534 drift 0.013275% <<LEAK` on the
v0.50 seed-4001 retest. Chased it, because a conservation violation
outranks every ecological question in this file.

**It is not a v0.50 regression.** Auditing drift across all 95 logs by
version: v0.47 0/10 clean, v0.48 0/3 clean, **v0.49 9/79 nonzero — every
single one seed 4001**, across nine different cfg arms; v0.50 1/3, also
seed 4001. Always exactly `7533 -> 7534`, +1 unit. The *timing* differs
by build (day 505 on v0.49, day 355 on v0.50), which is expected — the
formula change shifts the RNG path.

**Root cause, found in the export path (`v0_49` line 3504):**

```js
a[j] = Math.abs(v) >= 1000 ? Math.round(v) : +v.toFixed(4);
```

**Every logged value ≥1000 is rounded to an integer on export.** Matter
runs ~7500, so it is *always* rounded. The "+1" is a true drift of
somewhere under ~1 unit crossing a rounding boundary — bounded at
0.013%, not a meaningful leak.

**The consequential part is the other direction.** `LEDGER.md` states
"matter conservation exact" and quotes `drift 0.000000%` throughout, and
I have repeated that phrasing in nearly every heartbeat this session.
**It does not mean what it says.** A logged 0.000000% only establishes
that drift stayed inside one rounding bucket — |drift| < ~0.5 units out
of ~7000, i.e. **< 0.007%**. That is a real and reassuring bound, but it
is a *bound*, not exactness, and no headless run in this project has ever
demonstrated exact conservation.

Note the live build is unaffected: line 3724 computes drift from
unrounded `W.matter`, so the in-browser check is exact. **It is
specifically the exported log — and therefore `analyze.py`, and therefore
every conclusion drawn headlessly this session — that is coarsened.**

**Fix identified, deliberately NOT applied.** Exporting matter at full
precision is a measurement-only change (pure output formatting, cannot
touch the RNG draw sequence, satisfies rule 7 trivially). But it is an
HTML edit, and **v0.50 already carries one unverified structural change
whose 3-seed retest is running right now.** Editing the file mid-retest
would invalidate the comparison in flight, and stacking a second change
into v0.50 breaks one-change-per-version. **Queued for v0.51**, after
v0.50's ATTACK-floor change is scored. Recording the exact line and
reproducer here so it needs no rediscovery.

### v0.50 corrected-build retest, seed 4001 (2 of 3)

| | v0.49 | v0.50 (corrected) |
|---|---|---|
| R0 | 1.03 | 0.73 |
| actAttack | — | 0.4% |
| death age / maturityAge | — | 0.30 |
| caps | — | clean `[0]` |

With seed 1337 (0.78 vs 1.21), both retested seeds come in below their
v0.49 baseline. **Still not scoring the L0.50-1 prediction** — n=2, and
the measured within-cfg SD of 0.39 means a 2-seed mean carries SE 0.28,
so a drop of this size is roughly one standard error and cannot be
distinguished from RNG-path reshuffling. Seed 4002 now running to
complete the protocol.

### Structural lead: animals die at 0.44 of maturity, and the gene does not respond

Corpus-wide, using the gene snapshot the way `analyze.py` does (final
mean `maturityAge` in days vs mean death age):

- `maturityAge` final mean **32.2 d**; mean death age **10.5 d**;
  **ratio 0.44** (median 0.34)
- **only 6 of 85 runs** have animals reaching maturity on average
- yet the gene **drifts rather than falling**: rose in 40/85 runs, fell
  in 35/85, mean essentially unmoved (30.9 → 32.2 d), and only 1/85 runs
  sits near its MIN bound

That is the strange part. If 93% of the population dies before the age
its own gene sets for breeding, selection to lower that gene should be
overwhelming. It isn't happening.

**Candidate explanation, and it is measurable:** effective population
size. Harmonic mean animal N across 79 runs is **median 43**, with
**57% of runs below 50** and **90% below 200**. At Ne≈43, selection
coefficients below roughly 1/(2Ne) ≈ 0.012 are invisible to selection —
drift dominates. `analyze.py` already prints `<<DRIFT REGIME` for this
and it has been scrolling past unremarked all session.

This suggests a very different diagnosis from anything the dose-response
work was testing: **the animal population may be too small for selection
to optimise life history at all**, which would make every constant-tuning
arm a search for a value that lets a drift-dominated population survive
by luck rather than by adaptation. It would also explain the maturityAge
result, the ~24 arms landing in the same R0 band, and why nothing has
reached replacement.

**Not yet a finding — explicitly a hypothesis with an obvious confound:**
Ne is low *because* R0 < 1, so low Ne and poor demography are mutually
entailed and this could be effect rather than cause. Distinguishing them
needs a design where Ne is raised without changing per-capita
demography, which is not something any existing arm does. Proposing that
test is the next real step; it is not fired here, and it needs its own
written prediction.

### Method note, third time today

My first pass at the maturity analysis used the `aMature` log column as
if it were an age in days. It is not — `analyze.py` derives maturityAge
from the *gene snapshot*, and `aMature` is a different quantity
entirely. My wrong version produced "ratio 1.33, 43/85 reaching
maturity", almost the exact inverse of the correct "ratio 0.44, 6/85".
Caught by cross-checking against `analyze.py`'s own implementation before
writing anything down. Logging it because the near-miss is the point:
the number looked plausible and contradicted the digests, and the only
reason it did not become a finding is that the contradiction was checked
instead of explained away.

---

## Heartbeat ~08:45 — the Ne/drift hypothesis is rejected, and the real gap is instrumentation

Zero-compute cycle (all four cores were mid-run; a container restart then
killed them, see the note at the end). Tested last cycle's Ne hypothesis
against existing logs rather than firing anything new.

### Rejected: drift does not explain the maturityAge puzzle

The hypothesis was that harmonic Ne ≈ 43 puts the animal population in a
drift-dominated regime where selection on `maturityAge` cannot operate.
That makes a specific, testable prediction: **the variance of gene change
should scale as 1/Ne** — low-Ne runs should show large random excursions,
high-Ne runs small ones. Split 74 runs into Ne terciles:

| tercile | Ne range (median) | mean relative change | mean \|change\| | fell |
|---|---|---|---|---|
| LOW | 3-33 (21) | +0.092 | 0.478 | 10/24 |
| MID | 36-82 (43) | −0.044 | 0.472 | 11/24 |
| HIGH | 87-447 (140) | +0.333 | 0.538 | 13/26 |

- corr(Ne, |relative change|) = **−0.045**
- corr(log Ne, |relative change|) = **+0.002**
- corr(Ne, signed change) = **+0.065**

**Flat across a 100x range of Ne.** Magnitude of gene movement is
independent of population size, and direction stays a coin flip
(~45% falling) in every tercile. The drift signature is absent.
**Hypothesis rejected** — correctly labelled a hypothesis rather than a
finding when it was raised, and now retired without ever having been
propagated into `FINDINGS.md`.

### Also rejected: the mass gate is not the binding constraint

The competing explanation was that `adult` requires *both*
`age > maturityAge` **and** `mass >= maturityMassFrac*size`, so if the
mass gate were what actually blocked breeding, `maturityAge` would be
neutral and free to drift. Measured across 85 runs:

| quantity | value |
|---|---|
| `size` gene final mean | 5.18 |
| mass gate (0.6 × size) | 3.11 |
| median animal mass (P50) | 3.08 — **ratio 1.11** |
| P90 animal mass | 5.84 — ratio 2.23 |
| runs where the median animal clears the mass gate | **45/85** |
| runs where P90 clears it | 79/85 |

About half the population clears the mass gate, against **6/85** runs
where mean death age clears the age gate. **The age gate is far more
binding**, so `maturityAge` is genuinely the constraint on reproduction —
it is not a neutral passenger. That explanation is out too.

### What is actually going on: the selection readout cannot see the selection

Standing variance is healthy — `maturityAge` CV 0.316, not monomorphic,
plenty to select on. And the mutational step is 0.78× the standing SD,
which sounded anomalous until compared against the rest of the genome:
**all 54 animal genes sit between 0.67 and 1.29** on that ratio.
`maturityAge` (0.78) is unremarkable. That uniformity is what you expect
when standing variance is mutation-generated and equilibrates to roughly
one mutational step — it is a property of the mutation kernel, not a
defect in this gene.

The sharp comparison is against the model's own neutral markers.
`tag0/tag1/tag2` are identity tags used only for kin recognition — as
close to neutral as this model has. Fecundity selection differentials,
normalized by standing SD (units: SD per generation, n=85):

| gene | mean | SE | \|mean\|/SE |
|---|---|---|---|
| `maturityAge` | −0.566 | 0.412 | 1.38 |
| `tag0` (neutral) | −0.069 | 0.105 | 0.66 |
| `tag1` (neutral) | +0.363 | 0.315 | 1.15 |
| `tag2` (neutral) | +0.165 | 0.145 | 1.14 |
| `size` | −0.404 | 0.199 | **2.03** |

`maturityAge`'s differential is in the right direction (negative =
breeders mature earlier) but **not distinguishable from zero**, and not
distinguishable from the neutral tags. Note honestly that this test is
weak: SE 0.412 cannot rule out a real differential up to ~1 SD. It does
not prove selection is absent.

**And here is the part that matters.** `analyze.py` prints its own
warning under this readout: *"sel is FECUNDITY only. Viability selection
is excluded, and viability is most of all mortality."* Viability — dying
before reaching breeding age — is **exactly** the channel through which
selection on `maturityAge` must operate. The one statistic the project
has for measuring selection is structurally blind to the only selection
that could be acting here.

So the honest conclusion is not "selection is absent." It is: **the
project has no viability-selection readout, and viability is where all
the action is.** Whether `maturityAge` is failing to respond, or
responding invisibly, cannot be resolved with current instrumentation.

### Consequence for what to do next

The next step is a **measurement, not an experiment**: log the gene
means of animals that die before breeding versus those that reproduce, so
a viability selection differential can be computed directly. That is a
change to the logging path in the HTML — measurement-only, so rule 7's
RNG-neutrality check applies and should be easy to satisfy, but it still
needs a version bump and cannot land while v0.50's retest is in flight.
**Queued behind v0.51's matter-precision fix**, which is in the same
part of the code and should ship together as one measurement-focused
version.

This is now the fifth time today the binding constraint turned out to be
a measurement problem rather than an ecological one: the missing noise
floor, the export rounding on matter conservation, the unaudited `caps`
flag, the `aMature` column misread, and now the absent viability readout.
The ecology has not been the bottleneck; knowing what the numbers mean
has been.

### Container restart, ~08:40

The session container restarted and killed all four running jobs:
`intake-probe` 4001 (at day 780 of 800), `intake-probe` 4002 (day 280),
`v050-retest` 4002 (day 280), base-dose 30002 (day 720). `headless.js`
writes output only at completion, so all four produced nothing and were
restarted from scratch. No data integrity issue — runs are deterministic
per (build, seed, cfg), so the restarts reproduce exactly what was lost —
but roughly four core-hours of CPU went with it. Worth noting as an
argument for `--progress-days` checkpointing that can actually be resumed,
which does not currently exist.

---

## The pre-registered 3x-vs-5x comparison RESOLVES: no difference, 3x stands on parsimony

Both noise-floor batches completed on Actions (fetched by git branch;
`mcp__github__*` was not needed). **30 cold-drawn seeds, 15 per arm** —
seeds chosen as a block before any results were seen, which is what makes
this the first non-cherry-picked comparison in the whole investigation.

Scoring against the decision rule written *before* the data landed
("compare R0 distributions not dichotomized fractions; promote 5x only if
the gap exceeds one noise-floor SD; otherwise 3x wins on parsimony"):

| | 3x (`k_photoCost` 0.012) | 5x (0.020) |
|---|---|---|
| n | 15 | 15 |
| R0 mean | **0.674** | **0.735** |
| R0 SD | 0.278 | 0.314 |
| R0 median | 0.699 | 0.764 |
| R0 range | 0.18-1.12 | 0.14-1.35 |
| R0 ≥ 1 | 2/15 | 3/15 |
| extinct | 5/15 | 5/15 |
| hit plant cap | **8/15** | **2/15** |

- mean difference (3x − 5x) = **−0.061**, SE 0.108, |d|/SE = 0.56
- **permutation p = 0.590**
- R0≥1 rate: **Fisher p = 1.000**
- one-noise-floor-SD threshold = 0.314; observed gap 0.061 → **does not
  come close to exceeding it**

**Verdict: 5x is NOT promoted. 3x stands, on parsimony, exactly as the
pre-registered rule specifies.** Since 3x is already the base dose, the
operational consequence is *no change* — which is the correct outcome of
a horse race whose entrants turned out to be indistinguishable.

This also closes out the retraction chain properly. The original "5x is
the leading candidate (3/4 vs 4/6)" claim was retracted mid-session after
the external audit's Fisher test returned p≈1.0 at that tiny n. At 15
cold seeds per arm the answer is the same, with the difference now
measured rather than guessed: **p = 0.59, gap one-fifth of a noise-floor
SD.** The audit was right, and the retraction was not premature caution.

### Two things this sample settles that matter more than the horse race

**1. Neither dose is viable, now measured properly.** 3x mean R0 0.674,
5x 0.735; 2/15 and 3/15 seeds clear replacement; **5/15 go extinct in
both arms.** The "no configuration tested reaches replacement" conclusion
from the full-corpus re-tally holds on cold, pre-registered seeds — it
was not an artifact of pooling heterogeneous arms.

**2. The cap-binding result reproduces, and is worse than estimated.**
On these cold seeds the base dose hits the plant slot cap in **8/15 (53%)**
of runs, against 5x's 2/15 (13%). My mixed-corpus estimate last cycle was
29%; the clean number is roughly double that. The dose the project has
been treating as "off the `maxPlants` artifact" spends time pinned against
it in **more than half** of unselected runs.

So the two criteria now separate cleanly and point opposite ways: the
outcome criterion (R0) cannot distinguish 3x from 5x at all (p=0.59),
while the outcome-*independent* mechanistic criterion (does the plant
population stay off the array bound) separates them decisively, 53% vs
13%, in 5x's favour. The pre-registered rule governs and says 3x — but
it is worth being explicit that **the rule being followed here is the
R0 rule, which is the very outcome-tuning approach audit point 5
criticised.** The mechanistic criterion is the more principled one and it
prefers 5x. Not overriding a pre-registered rule after seeing the data —
that would be the worst of both worlds — but flagging that the *next*
selection decision should be made on the mechanistic criterion with a
threshold fixed in advance, not on R0.

### Stationarity: audit point 4, answered, and it is bad

With 30 clean same-cutoff runs in hand, the stationarity gate finally has
a proper sample. Slope over the last third, in `analyze.py`'s own units
(% per 100 samples):

| arm | runs failing the gate | median \|plant slope\| | median \|animal slope\| |
|---|---|---|---|
| 3x | **15/15** | 143.6% | 91.6% |
| 5x | **15/15** | 97.0% | 265.9% |

**Every single run fails**, and not marginally — `analyze.py` flags
anything above ~10% as DRIFTING, and these medians are 10-25x that.
**No R0 in this project has ever been an equilibrium measurement.** They
are all snapshots of populations still in motion at the 800-day cutoff.

Direction is not consistent, which is the one piece of good news for the
comparison: animal counts are falling in 6/13 surviving 3x runs and 8/14
5x runs, rising in the rest. So the non-stationarity is **not a uniform
downward bias that would make both arms look better than they are** — it
is genuine unsettled dynamics in both directions. That protects the
*comparison* (both arms share the cutoff and the churn) while
invalidating any *absolute* claim: "3x mean R0 is 0.674" describes a
transient, and there is no evidence for what the equilibrium value would
be, or that one exists at 800 days.

**This is the strongest argument yet that 800 days is too short a
protocol**, and it is now measured rather than suspected. Extending the
protocol has a real cost (a 1200-day run took ~4 hours locally), so the
right next move is a small matched 800/1600/2400-day ladder on 3 seeds to
find where — or whether — the trajectories settle, rather than
unilaterally raising the cutoff for everything. That needs its own
prediction and is not fired here.

---

## intake-probe seed 4001: the extinction reframing is not supported either

Seed 4001 at `k_intake` +50%: **R0 0.78, population persisted** (N ~58-86
through the final window, never hit zero). Matter clean, caps clean,
`aRate/aUpkeep` **1.13** — flagged `<<LOW`, i.e. *below* the corpus mean
of 1.166 despite a 50% larger intake constant, which is one more small
strike against the already-withdrawn regulation reading.

Two cycles ago, after seed 1337 went extinct, I reframed this arm as
testing "does +50% intake reliably drive extinction (boom-bust via faster
plant depletion)?" **That reframing does not survive seed 4001.** One
extinction in two seeds is exactly the base rate — the cold noise-floor
sample puts extinction at **5/15 (33%)** for the base dose, so 1/2 is
unremarkable. There is no extinction effect to report.

What the arm does show, on the **paired** comparison (same seed, same RNG
stream start, which is far stronger than comparing against the cold-seed
mean):

| seed | base dose R0 | +50% `k_intake` R0 | Δ |
|---|---|---|---|
| 1337 | 1.21 | 0.56 | −0.65 |
| 4001 | 1.03 | 0.78 | −0.25 |
| 4002 | 1.31 | *running* | — |

Both paired differences are negative, mean −0.45 against a noise-floor SD
of ~0.28-0.31. Suggestive that more efficient eating makes things
*worse*, not better — but n=2, and I am not calling it until 4002 lands.
Noting explicitly that seeds 1337/4001/4002 are, per the cold-seed
result, an unusually *favourable* trio at base dose (1.21/1.03/1.31, mean
1.18, against the cold-seed mean of 0.674) — which is exactly why the
paired design matters here and why the unpaired comparison against 0.674
would be misleading in the opposite direction.

---

## Stationarity ladder — prediction, written before the run

The 30-seed cold sample established that **15/15 runs in both arms fail
the stationarity gate**, at 10-25x the DRIFTING threshold. Every R0 in
this project describes a population still in motion. What is not known is
whether 800 days is merely *early* on a trajectory that settles, or
whether these systems never settle at all — and those two imply opposite
fixes.

**Design efficiency note:** this does not need three runs per seed. Run
length is a loop bound, not an input to the RNG stream, so the first 800
days of a 2400-day run are the same trajectory as an 800-day run. One
long run per seed yields the whole ladder, and **the run verifies that
assumption itself**: R0 computed over the day-600-800 window of the long
run must reproduce the known 800-day value for the same seed and cfg
(seed 1337, base dose, R0 **1.21**). If it does not, the assumption is
wrong and the ladder is discarded — checking rather than trusting, given
how many assumptions have failed today.

**Falsifiable prediction.** Seed 1337, base dose, 2400 days. Compare R0
over matched trailing windows ending at day 800, 1600, and 2400, and the
stationarity slope in each.

- **HIT — "800 days is too short, the system settles later":**
  |R0(2400) − R0(800)| **> 0.31** (one noise-floor SD) *and* the
  stationarity slope at 2400 is materially smaller than at 800.
  Consequence: the protocol cutoff must rise, and every absolute number
  in `LEDGER.md` is an early-transient artifact.
- **MISS — "these systems do not settle at all":** R0 windows agree
  within 0.31 *and* slopes stay comparably large at 2400. Consequence:
  the non-stationarity is sustained oscillation rather than an
  unfinished transient, no cutoff is privileged, 800 days is as
  defensible as any, and the stationarity gate should be reinterpreted
  as a property of the model rather than a defect in the protocol.
- **Discard:** the day-600-800 window fails to reproduce R0 1.21,
  invalidating the single-long-run design.

Both outcomes are actionable and they imply opposite responses, which is
the point. Firing seed 1337 now on the core freed by intake-probe 4001;
additional seeds to follow as cores free, since n=1 cannot settle this
and the prediction is written for the pattern across seeds.

---

## The mission scorecard, computed for the first time — and it is much better news than this session's narrative

Free analysis across **120 runs with usable mortality ledgers**. This
session has been almost entirely demography and methodology; nobody had
ever directly measured the two things the project actually exists to
produce, stated at the top of `CLAUDE.md`: *herbivory controls plants,
carnivory controls herbivores*. Both are measurable straight out of the
mortality counters, and neither has been looked at.

### Pillar 1 — does herbivory control plants? Substantially, yes.

| metric | value |
|---|---|
| share of plant deaths caused by being eaten | mean **37.2%**, median 39.5%, range 9.3-76.2% |
| runs where grazing is >25% of plant mortality | **91/120** |
| runs where grazing is >50% | 24/120 |
| **eaten/grown — share of plant production consumed** | mean **53.0%**, median 58.1% |

**Over half of primary production is being eaten.** For terrestrial
systems that is at the high end of the real-world range but squarely
plausible. Grazing is a first-order force on the plant layer in almost
every run, not a rounding error.

This corrects an impression I have been carrying, and repeating, from
individual digests. I quoted `eaten/grown 0.289 <<LOW` and "plant deaths:
eaten 31432 starved 123872" (21%) from the v0.50 seed-1337 run several
cycles back, and let that stand as representative. It was one of the
weakest runs in the corpus. The median run is roughly double it. Note
also that these are whole-run cumulative counters including the ~260-day
pre-fauna period, during which plants starve and none are eaten — so
**37.2% understates the animal-era grazing share.**

### Pillar 2 — does carnivory control herbivores? Partially.

| metric | value |
|---|---|
| share of animal deaths caused by predation | mean **23.6%**, median 19.9%, range 1.5-67.6% |
| runs where predation is >25% of animal mortality | 48/120 |
| runs where predation is >50% | **5/120** |

Real, but secondary — starvation dominates. In most real herbivore
populations predation is the leading cause of death, so ~24% is on the
low side. This is the weaker of the two pillars, and it is the honest
answer to "has carnivory ever controlled herbivores here": not usually.

### The finding that reframes the session: trophic coupling tracks viability

| | plant deaths from grazing | animal deaths from predation | eaten/grown |
|---|---|---|---|
| **viable runs (R0≥1), n=22** | **44.3%** | **36.2%** | 54.0% |
| **non-viable (R0<1), n=97** | 35.8% | 20.5% | 52.9% |

- corr(R0, predation share) = **+0.481** (t=5.93, df=117, p < 1e-6)
- corr(R0, plant-grazing share) = **+0.391** (p < 1e-4)
- corr(R0, eaten/grown) = +0.274 (p ≈ 0.003)

**The runs where animals sustain themselves are exactly the runs where
the food web is working hardest.** Predation share is nearly double in
viable runs, and it is the strongest correlate of viability found
anywhere this session — stronger than any constant tested across ~24 CFG
arms.

**The causal reading is genuinely ambiguous and I am not claiming
direction.** More animals mechanically create more predator-prey
encounters, so higher R0 could be *producing* the higher predation share
rather than resulting from it. That reverse path is at least as
plausible as the forward one, and nothing here separates them. What the
correlation does establish is that **the viable regime is the
strongly-coupled regime** — the two states go together, whichever drives
which.

### Why this matters more than the dose-response work it displaces

The whole investigation has been asking "which value of `k_photoCost`
lets animals survive" — a question that, after 30 pre-registered cold
seeds, answered *neither, and the two candidates are indistinguishable*.
This suggests a different question with a real signal behind it:
**what makes trophic coupling strong?** Coupling and viability travel
together at r≈0.48, which is an effect size nothing in the dose-response
matrix came close to.

It also puts the earlier `k_confusion:0` result in a new light. That arm
disables the anti-predator confusion effect — a *coupling* parameter, not
a food-supply one — and all three cold-ish seeds came in below
replacement. Consistent with the coupling story, though it was a
3-seed comparison with no matched control, so it stays MODERATE.

**Not proposing a constant to change on this basis.** The obvious move —
find a parameter that raises predation share and promote it — would be
outcome-tuning in exactly the form already logged against the
`k_photoCost` selection, and worse, would be tuning against a metric
whose causal direction is unknown. The right next step is to *separate
the causal directions*, and the honest position until then is that this
is the most promising correlation in the corpus and the least understood.

### Base-dose seed 30002 — a clean counterexample to the coupling correlation, one cycle after finding it

R0 **0.80**, matter clean, hit the plant cap (peak 24589/25000, so it
joins the 53% of base-dose runs that ride the artifact). Local base-dose
tally now 30001 (0.72), 30002 (0.80) — both below replacement, both
sitting near the cold-seed mean of 0.674.

The interesting part is the trophic numbers:

| | seed 30002 | corpus mean | viable-run mean |
|---|---|---|---|
| predation share of animal deaths | **42.0%** | 23.6% | 36.2% |
| grazing share of plant deaths | **46.0%** | 37.2% | 44.3% |
| R0 | **0.80** | — | ≥1 by definition |

**This run has stronger trophic coupling than the average *viable* run on
both pillars, and it still fails to reach replacement.** Predation share
42% is nearly double the corpus mean and above the 36.2% that
characterises viable runs; grazing share likewise.

Recorded deliberately and immediately, one cycle after reporting
corr(R0, predation share) = +0.481 as the strongest signal in the corpus.
An r of 0.48 leaves ~77% of the variance unexplained, so counterexamples
are *expected* rather than surprising — but the useful discipline is to
say so with a concrete case rather than let a strong correlation harden
into "coupling ⇒ viability" through repetition. It does not. Seed 30002
is what the unexplained 77% looks like, and it is one more reason not to
go looking for a constant that raises predation share.

Also worth noting against the reverse-causality reading: if high R0 were
simply *producing* high predation share via more encounters, a run with
R0 0.80 should not be showing 42%. That does not resolve the direction
question, but it does mean the reverse path is not a complete
explanation either.

---

## The k_confusion paired experiment — the only real controlled manipulation in the corpus, and it confirms the v0.47 finding

When `confusion-off-retest` completed I flagged what was missing: *"still
no confusion-ON comparison at the identical dose/seeds pulled alongside
it — filed MODERATE not HIGH."* That control exists in the corpus and I
had not assembled it. Doing so now, with a **strict pairing rule**: same
seed, same build, and identical cfg on *every* key except `k_confusion`.

| seed | arm | R0 | predation share | grazing share | attacks | kills | actAppr | mean N |
|---|---|---|---|---|---|---|---|---|
| 1337 | ON (0.06) | **1.21** | 41.7% | 49.9% | 39885 | 1633 | 0.005 | 59 |
| 1337 | OFF (0) | **0.64** | 21.8% | 44.2% | 31019 | 1577 | 0.000 | 80 |
| 4001 | ON | **1.03** | 23.1% | 50.6% | 27164 | 1953 | 0.010 | 153 |
| 4001 | OFF | **0.70** | 19.1% | 32.9% | 11402 | 814 | 0.000 | 128 |
| 4002 | ON | **1.31** | 31.6% | 53.7% | 183428 | 7051 | 0.460 | 320 |
| 4002 | OFF | **0.79** | 34.7% | 36.7% | 87652 | 2887 | 0.000 | 386 |

**ΔR0 (OFF − ON) = −0.52, −0.57, −0.33; mean −0.47.** Negative in every
seed, and the magnitude is 1.5x the measured noise-floor SD (~0.31) in
two of three. This is a *paired* design — same seed means the same RNG
stream start — which is far more powerful than the unpaired comparisons
that have dominated this session.

**The v0.47 `k_confusion` finding is confirmed, with its control, and is
upgraded from MODERATE to HIGH.** It survives the `maxPlants` fix, and it
is now the only ecological claim in the project backed by a matched
paired manipulation rather than a cross-arm comparison.

### What it does and does not say about the coupling correlation

It was assembled to test causality on last cycle's corr(R0, predation
share) = +0.481. It does not settle that, for a reason worth being
precise about: **`k_confusion:0` is not a single-channel manipulation.**
Per the v0.47 notes, setting it to zero both removes the crowding
protection *and* zeroes the APPROACH score, since `crowd` gates that
branch. `actAppr` goes to exactly **0.000** in all three OFF runs,
confirming herding is fully disabled, not merely reduced.

The knock-on is visible and counterintuitive: **attacks fall in all three
OFF runs** (39885→31019, 27164→11402, 183428→87652) even though each
attack is mechanically *more* effective without the `1/(1+crowd)`
divisor. Removing herding stops animals aggregating, aggregation drives
encounter rate, and the encounter-rate loss outweighs the per-attack
gain. Grazing share falls in all three as well (49.9→44.2, 50.6→32.9,
53.7→36.7).

So the arm moves coupling *and* viability together, consistent with the
correlation — but it moves two coupling channels at once and cannot
isolate predation. And predation share itself is **not** monotone with
R0 here: seed 1337 has predation share *rising* (+3.1%) while R0 falls
0.52. Combined with seed 30002 last cycle (42% predation, R0 0.80),
that is now two independent cases where high predation share coincides
with failure. **"More predation ⇒ more viable" is not supported**; what
survives is the weaker and better-evidenced claim that the herding /
confusion *mechanism* is load-bearing, worth ~0.47 R0.

### Method note — I caught a contaminated pairing mid-analysis

My first pass at this filtered on seven named cfg keys and paired
whatever matched. It produced seed 1337 "ON" with R0 0.44, which I
recognised as wrong because base-dose 1337 is 1.21 — the filter had
silently matched the `armeff-test` run (`k_armEff` 2→1), a key I had not
thought to exclude, and the dict kept whichever file was globbed first.
The fix was to stop enumerating keys and instead require an exact match
on the *entire* cfg dict minus seed and `k_confusion`. Recording it
because the wrong version was internally consistent and would have
supported a tidy story about confusion-off *raising* R0 on one seed; the
only thing that caught it was a remembered value not matching.

---

## intake probe COMPLETE (3/3 paired): more efficient eating makes things worse, via emergent overexploitation

All three seeds landed. Paired against the same seed's base-dose run
(same RNG stream start), which is the strong design:

| seed | base R0 | +50% `k_intake` R0 | ΔR0 | base N | probe N | ΔN |
|---|---|---|---|---|---|---|
| 1337 | 1.21 | 0.56 | **−0.65** | 59 | 48 | −19% |
| 4001 | 1.03 | 0.78 | **−0.25** | 153 | 93 | −39% |
| 4002 | 1.31 | 0.80 | **−0.51** | 320 | 319 | −0% |

**Mean ΔR0 = −0.47, negative in 3/3.** Standing population did not rise
in any seed — it fell in two and was flat in the third. Making animals
**50% better at extracting food makes the population less viable and no
more numerous.**

### The mechanism, checked rather than assumed

| seed | arm | standing plants | LAI | eaten/grown |
|---|---|---|---|---|
| 1337 | base | 7074 | 0.576 | 44.1% |
| 1337 | +50% | **1547** | 0.476 | 63.0% |
| 4001 | base | 10084 | 0.532 | 72.3% |
| 4001 | +50% | **7367** | 0.539 | 47.7% |
| 4002 | base | 18650 | 0.583 | 76.0% |
| 4002 | +50% | **11671** | 0.452 | 74.2% |

**Standing plant biomass collapses in 3/3 seeds** (−78%, −27%, −37%; mean
−5074 plants). Meanwhile the *share* of production consumed barely moves
(−2.5% mean) — the herbivores keep taking a similar fraction of a much
smaller pie. That is **overexploitation**: raising per-capita harvesting
efficiency degrades the resource base faster than it feeds the consumers,
and the consumers are worse off for it.

**Nothing in the code implements this.** There is no overharvesting rule,
no resource-depletion penalty, no density-dependent efficiency term. It
falls out of plants growing at a finite rate and animals eating them
faster. By the project's own mission test — *if a result had to be
written into the code, it doesn't count* — **this one counts.** It is
the clearest emergent trophic dynamic found so far, and it is a textbook
consumer-resource result arrived at from the physics.

It also sharpens Pillar 1 from the mission scorecard. Herbivory does not
merely "control" plants here; it controls them **strongly enough that a
50% efficiency increase crashes the plant layer**. The coupling is not
weak — if anything the base configuration already sits close to
overexploiting.

### The prediction, scored honestly

The original HIT branch required all three of: `aRate/aUpkeep` in
1.10-1.30 ✓ (1.18/1.13/1.20), R0 within ±0.45 of 1.18 ✗ (0.56 falls
outside), standing N up >25% ✗ (fell in two, flat in one). The MISS
branch required ratio >1.35 sustained ✗ or mean R0 >1.63 ✗. **Neither
branch fires** — as already recorded when seed 1337 landed, the
prediction was badly specified and did not tile the outcome space. The
descriptive result above stands on its own and is not being retro-fitted
to either branch.

Note also the two intermediate stories I told about this arm and then
had to drop: "emergent density-dependent regulation" (withdrawn — no
density relationship, and the ratio is survivorship-filtered) and
"reliably drives extinction" (withdrawn — 1/2 then 1/3 extinctions,
matching the 33% base rate). The finding that survived is the third
reading, and the only one built on the paired comparison across all
three seeds rather than on the first seed to land.

---

## Reciprocal arm — prediction, written before the run

If base `k_intake` sits on the **overexploiting side** of an optimum,
making animals *less* efficient should move the system toward the peak
and **raise** R0. If base sits near the peak already, reducing intake
should **lower** R0, same as raising it did.

Arm: `k_intake` 0.01486 → **0.00991** (−33%),
`cfg-patches/intake-down-probe.json`, seeds 1337/4001/4002 (all have
matched base-dose values: 1.21, 1.03, 1.31).

- **HIT — "base is overexploiting":** paired ΔR0 **> 0 in ≥2 of 3
  seeds**, and standing plants rise in ≥2 of 3. Reading: the base
  configuration harvests past the sustainable point, and the plant layer
  is being held below the density that would best support consumers.
- **MISS — "base is near the peak":** paired ΔR0 **< 0 in ≥2 of 3**, i.e.
  R0 falls on *both* sides of base. Reading: an inverted-U with base near
  its top, and `k_intake` is not the lever — which would make the
  overexploitation finding above a statement about the *direction of the
  gradient above base*, not about base itself being misconfigured.
- **Ambiguous:** ΔR0 within ±0.31 (one noise-floor SD) on all three,
  i.e. no detectable effect either way — the gradient is flat below base
  even though it is steep above.

**Mission-test guard, restated:** this is a gradient probe. **No
`k_intake` value will be promoted on the basis of producing a higher
R0**, whatever this returns — that is precisely the outcome-tuning trap
already logged against the `k_photoCost` dose selection, and the fact
that this arm has a more interesting mechanism behind it does not make
the trap any less of one. What a HIT would license is a *diagnosis*
(base overexploits), not a new constant.

Seed 1337 firing now on the core freed by intake-probe 4002.

### Reciprocal arm, seed 1337 only (1 of 3) — NOT scoring yet, but two details already complicate the story

| arm | `k_intake` | R0 | standing plants | mean N | eaten/grown |
|---|---|---|---|---|---|
| −33% | 0.00991 | **0.62** | 3897 | **82** | 46.9% |
| base | 0.01486 | **1.21** | **7074** | 59 | 44.1% |
| +50% | 0.02229 | **0.56** | 1547 | 48 | 63.0% |

ΔR0 = **−0.59**, which points at the MISS branch (R0 falls on both sides
of base → inverted-U with base near the peak). **Explicitly not scoring
it**: the prediction requires ≥2 of 3 seeds, this is one, and n=1 reads
are the specific error I have made repeatedly today. Seeds 4001 and 4002
decide it; 4001 is firing now.

Two things in this single run are worth flagging early because they do
not fit the tidy overexploitation gradient:

**1. Standing plants fall on *both* sides of base** (3897 and 1547 vs
base 7074). Less efficient herbivory producing *fewer* plants is not what
the overexploitation story predicts — that story says easing harvest
pressure should let the plant layer recover. Whatever is happening is not
a simple monotone consumer-resource gradient in `k_intake`.

**2. Animal numbers move opposite to R0.** The −33% arm carries **more**
animals than base (82 vs 59) while having roughly half the R0. More
individuals, each further from replacement. Standing population and
per-capita viability are decoupled here — which is a concrete instance of
the point `analyze.py` has been making all along ("no extinction is not
the same as viable"), and a warning against reading population size as
health in either direction.

A candidate reconciliation, untested: at lower intake efficiency animals
take longer to reach breeding mass, so more of them accumulate in a
juvenile, non-reproducing standing crop that still eats. That would give
simultaneously more animals, more total consumption, fewer plants, and
lower R0 — consistent with all four observations. It also predicts the
juvenile fraction should be higher in this arm, which is directly
checkable once the other two seeds land. Recording the hypothesis now,
before seeing them, so it is a prediction rather than a story fitted
afterwards.

### Juvenile-accumulation hypothesis: REJECTED, and it corrects an earlier conclusion

Tested the hypothesis recorded last cycle (before seeing any of this
data) on seed 1337, where all three `k_intake` arms have now landed.

| arm | `k_intake` | R0 | juvFrac | mean N | median mass | **evolved maturityAge** | death age | plants |
|---|---|---|---|---|---|---|---|---|
| −33% | 0.00991 | 0.62 | 0.542 | 82 | 3.19 | **64.4 d** | 19.4 | 3897 |
| base | 0.01486 | **1.21** | 0.778 | 59 | 4.55 | **40.4 d** | 28.8 | 7074 |
| +50% | 0.02229 | 0.56 | 0.394 | 48 | 5.51 | **34.7 d** | 19.1 | 1547 |

**Prediction: juvenile fraction should be HIGHER in the −33% arm.
Observed: 0.542 vs base 0.778 — LOWER. Not supported, hypothesis
rejected.** Base actually carries the *most* juveniles of the three. The
"more animals, fewer plants, lower R0" pattern is not explained by
juveniles piling up.

**What the table does show is cleaner, and it corrects something I
concluded two cycles ago.** Two quantities move monotonically with
`k_intake`:

- **median animal mass: 3.19 → 4.55 → 5.51** (rises with intake)
- **evolved `maturityAge`: 64.4 → 40.4 → 34.7 days** (falls with intake)

`maturityAge` spans a **1.85x range**, cleanly ordered by the food
environment, at fixed seed with everything else identical. That is a
gene responding to selection, and it directly contradicts the reading I
recorded earlier: *"maturityAge drifts rather than falling — rose in
40/85 runs, fell in 35/85 — the gene does not respond."*

**Why the earlier analysis missed it:** it measured *direction of change
from the founder value, pooled across ~24 heterogeneous cfg arms*. Pooling
across arms with different selective environments averages away exactly
the signal visible here, and "direction from founder" is the wrong
statistic when different environments have different optima — a gene
sitting correctly at 64 days in a poor environment and correctly at 35
days in a rich one both count as "moved" in whichever direction the
founder happened to sit. **The gene responds to its environment; the
pooled test could not have detected that.** The maturityAge puzzle that
consumed two cycles is substantially dissolved: the correct statement is
not "selection cannot move this gene," it is "selection moves it to
match the food environment, and the environment is poor."

The mechanism is sensible: more food → faster growth → reaching breeding
mass sooner pays → earlier maturity is selected. Less food → growth is
slow → the mass gate binds regardless → the age threshold drifts up.

### Why base wins: the lifespan-to-maturity match

Base is the only arm where lifespan and maturity are close:
**28.8 / 40.4 = 0.71**, against 0.30 (−33%) and 0.55 (+50%). R0 peaks
where that ratio peaks, which is a coherent explanation for the
inverted-U in `k_intake` without needing overexploitation to be monotone.

Across the whole corpus the relationship holds but is modest:
corr(R0, deathAge/maturityAge) = **+0.260** (t=2.95, df=120, p≈0.004) —
real, weaker than predation share's +0.481. The group split is sharper
than the correlation suggests:

| | mean deathAge/maturityAge |
|---|---|
| viable (R0≥1, n=22) | **0.99** |
| non-viable (n=100) | **0.67** |

Viable populations are precisely those where animals live, on average,
just about exactly to their own evolved breeding age. That the
correlation is only +0.26 while the group means are 0.99 vs 0.67 suggests
a **threshold** relationship rather than a linear one — clearing ratio≈1
is what matters, and exceeding it further buys little. Worth noting as a
candidate structural criterion, not yet a finding: n=22 viable runs, and
the ratio is partly definitional (both terms involve age).

**Caveat on all of the above: the three-arm comparison is one seed.**
Seeds 4001 and 4002 are queued and will confirm or break the monotonicity
in `maturityAge` and median mass. Recording the correction now because it
overturns a stated conclusion, and flagging the n clearly rather than
waiting.

---

## v0.50 SCORED: MISS on 3/3 paired seeds. Reverted as v0.51 [L0.51-1]

The corrected-build retest is complete. Paired against the same seed's
v0.49 run (identical cfg, same RNG stream start):

| seed | R0 v0.49 | R0 v0.50 | ΔR0 | actAttack% | kills v0.49 → v0.50 | carnivory |
|---|---|---|---|---|---|---|
| 1337 | 1.21 | 0.78 | **−0.43** | 0.82 → 0.57 | 1633 → **505** | 0.195 → 0.088 |
| 4001 | 1.03 | 0.73 | **−0.29** | 0.28 → 0.41 | 1953 → **727** | 0.065 → 0.137 |
| 4002 | 1.31 | 0.85 | **−0.46** | 0.87 → 0.69 | 7051 → **2587** | 0.066 → 0.060 |

**Mean ΔR0 = −0.39, negative 3/3.** Against the measured noise-floor SD
of ~0.30, a 3-seed paired mean has SE 0.17, so this is **2.3 SE** — and
the direction is unanimous. **Kills fall 60-70% in every seed.**

**Scored against the prediction written before the run:**

- **HIT required:** `actAttack` drops toward zero in already-low-carnivory
  runs *while runs with real predation pressure are* ***not obviously
  worse***. All three seeds are obviously worse — R0 down 0.29-0.46,
  kills down ~65%. **Hit condition fails.**
- **MISS as written:** "`actAttack` share collapses everywhere." It did
  not — the action *share* barely moved (mean −0.10 percentage points,
  and it *rose* on seed 4001).

So the outcome is a **MISS on the criterion that mattered** (not obviously
worse), reached by a mechanism the Miss branch did not describe. Worth
being precise about, because the distinction is informative: **the action
share stayed flat while absolute kills collapsed.** Animals chose ATTACK
about as often, but far fewer attacks converted to kills. The likely
reason is distributional — with the floor gone, ATTACK's score is
proportional to `meatAttraction`, so low-`meatAttraction` animals stop
attacking entirely while a shrinking high-`meatAttraction` minority keeps
going. A stable mean share can hide that. Seed 1337's carnivory halving
(0.195 → 0.088) is consistent with predation decaying out of the
population, which is exactly the **absorbing-state** failure flagged when
this change was first corrected.

**Reverted, per the prediction's own pre-registered consequence** ("the
change should be reverted rather than defended") and rule 3 ("a missed
prediction means the diagnosis was wrong, not that the constant needs to
be bigger").

### v0.51 — the revert [L0.51-1]

`evosim-v0_51_0.html`. `k_meatAttr` removed entirely; the ATTACK score
line restored to `*sizeMatch*(0.5 + G[g+AG.meatAttraction])`.

**Verified exact, not assumed:** diffing v0.49 against v0.51 with comment
lines stripped, **the only executable difference in the entire file is
the VERSION string.** `node check.js`: PASS (reports VERSION 0.51.0,
arbiter branches entered). A confirmation run (seed 1337, base dose) is
in flight and must reproduce v0.49's R0 **1.21** exactly; if it does not,
the revert is not clean and this entry is wrong.

**What was actually learned — the floor is load-bearing.** v0.50's
premise was that ATTACK's `0.5 +` floor was an unprincipled asymmetry
against GRAZE/SCAVENGE's unfloored attraction genes. The asymmetry is
real, but it is doing real work: predation needs a baseline interest to
stay *reachable*, because an animal that never attacks never discovers
that attacking pays, and `meatAttraction` then has no fitness signal to
push it back up. Removing the floor does not liberate predation, it lets
predation decay. That is a genuine structural finding and it is worth
more than the change was.

**The absorbing-state problem is therefore real and still unsolved** —
v0.50 was an accidental experiment demonstrating it. The audit's proposed
fix (reachability via exploration noise in *action selection*, so the
gene itself can stay unfloored) is now the live candidate, and it is a
genuinely different mechanism rather than a constant tweak. **Not
attempted here**: it needs its own version and its own written prediction,
and stacking it onto a revert would repeat exactly the mistake being
reverted.

**File hygiene, pending verification:** once the seed-1337 confirmation
reproduces 1.21, `evosim-v0_50_0.html` can be deleted (its results are
captured above, satisfying CLAUDE.md's rule) and `evosim-v0_49_0.html`
becomes redundant with v0.51. Holding both until that run lands rather
than deleting on the strength of a diff.

---

# MAJOR CORRECTION, 2026-08-10 ~14:00 — every paired comparison made today was confounded by run length

The v0.51 verification run was designed to confirm the revert reproduced
v0.49 exactly. It returned **R0 0.73 against v0.49's 1.21** — and finding
out why invalidated most of today's conclusions.

### The confound

A rigorous diff (block comments and trailing comments stripped, 2900 code
lines each) confirms **v0.49 and v0.51 differ in exactly one token: the
VERSION string.** The cfg dicts are identical. Same seed. So the
difference could not be the build.

It was **run length**. The v0.49 "baselines" I have been pairing against
all day are **1200-day** runs; every treatment run I compared them to is
**800 days**. `analyze.py` computes R0 over the *last 200 samples*, so
a 1200-day run is measured over days 200-1200 and an 800-day run over
days 0-800. Given the stationarity result established earlier today —
**15/15 runs fail the gate, at 10-25x the DRIFTING threshold** — those
windows sample completely different parts of a moving trajectory.

**The artifact is larger than every effect I reported today.** Identical
code, identical cfg, same seed 1337: **R0 1.21 at the 1200-day window,
0.73 at the 800-day window. A −0.48 difference from run length alone.**

### What survives, recomputed on matched 800-day windows

| claim | as reported | corrected | verdict |
|---|---|---|---|
| **v0.50 floor removal, ΔR0** | −0.39 (3/3 neg) | **+0.00** (+0.05, +0.02, −0.07) | **RETRACTED — no effect** |
| v0.50, kills **per day** | "−65%" | 1.00→0.63, 0.95→0.91, 4.91→3.23 | **survives** — falls 3/3 |
| **intake +50%, ΔR0** | −0.47 (3/3 neg) | **−0.07** (−0.16, +0.07, −0.12) | **RETRACTED — inside noise** |
| intake +50%, standing plants | −5074 | **−2683, −762, −9046** | **survives** — falls 3/3 |
| intake −33%, ΔR0 | −0.59 | **−0.11** | **RETRACTED** |
| **k_confusion OFF, ΔR0** | −0.47 (3/3 neg) | **−0.08** (−0.08, −0.02, −0.13) | **DOWNGRADED** — 3/3 direction holds, magnitude ~6x smaller and well inside the noise floor |

Three headline claims from today are retracted outright. Two mechanism
claims survive because they rest on **rate or window-mean** quantities
rather than endpoint totals: kills *per day* and standing plant *mean*
both still move consistently.

### Consequences, stated plainly

**1. The v0.50 MISS scoring is retracted.** On matched windows the R0
effect is zero. The HIT condition ("runs with real predation are not
obviously worse") is *met*, not failed. The correct verdict is
**can't-tell on R0, with a modest consistent reduction in realized
predation (kills/day down 3/3)** — not a miss.

**2. The v0.51 revert was therefore made on bad data.** The revert
itself is mechanically sound — at a *matched* 800-day window v0.49
truncated and v0.51 native agree to **six decimal places (0.728954 vs
0.728954)**, so it restores v0.49 exactly, as claimed. But the *reason*
given for making it does not survive.

**Decision: v0.51 stands, on a different and weaker basis, stated
honestly as a judgment call on null data.** With R0 neutral, the
tiebreaker is structural: the floor's removal reduces realized predation
(kills/day down 3/3) with no demographic benefit, and carnivory is
already the weaker of the two mission pillars (23.6% of animal deaths).
Keeping the floor is also the lowest-risk option because v0.51 is
byte-equivalent in behaviour to v0.49, the best-characterised build in
the project. **Had I had correct data at the time, this would have been
scored can't-tell and the change would more likely have been left in
place pending a better test.** Recording that counterfactual rather than
pretending the revert was always justified.

**3. "Emergent overexploitation" is narrowed, not withdrawn.** More
efficient herbivores really do deplete the standing plant layer (3/3 on
matched windows). What is *not* supported is that this costs the
consumers measurable R0 — that number was the artifact. The mechanism
stands; the demographic consequence does not. It remains an emergent
result that passes the mission test, but a smaller claim than I made.

**4. The k_confusion finding drops from HIGH to LOW-MODERATE.** Still
3/3 in the same direction, which is worth something, but at mean −0.08
against a noise floor SD of ~0.30 it is not distinguishable from chance
at n=3. It is also not cleanly matched even now: seed 4002's OFF run
terminated at 640 days, so that pair is 640-vs-800 rather than 800-vs-800.

### Root cause and the guard that should have existed

The error is mine and it is a process failure, not bad luck. I built
strict cfg-matching into the pairing logic — after being burned by the
`armeff-test` contamination earlier today — and then **never checked the
one property that matters most for a non-stationary system: how long each
run went.** I had *already established* that 15/15 runs fail the
stationarity gate. Knowing that R0 is a moving target and still comparing
across different cutoffs is the specific inconsistency here.

Adding a hard rule to `CLAUDE.md` so this cannot recur silently:
**never compare R0 (or any trailing-window statistic) across runs of
different length — match the cutoff explicitly, and state the cutoff
in any comparison.** Endpoint totals (kills, births, matter) are worse
still: they scale with duration directly and must be normalised to rates
before any cross-run comparison.

---

## Corpus recomputed at a matched 800-day cutoff — and the fix has its own limit

**First, a correction to my own remediation plan.** Last cycle I said the
next step was regenerating baselines at matched length. That was
unnecessary: **truncating an existing longer run to 800 days is exactly
equivalent to having run 800 days**, verified to six decimals (v0.49
truncated → 0.728954, v0.51 native 800d → 0.728954). So the entire
length confound is fixable analytically, at **zero compute cost**, across
all existing data. No re-runs were needed and none were fired for this.

**Base dose (3x), every run evaluated at a matched 800-day cutoff,
deduplicated by seed, n=20:**

| | matched 800d | previously (mixed lengths) |
|---|---|---|
| mean R0 | **0.791** | 0.73 |
| SD | **0.134** | 0.278-0.39 |
| median | 0.762 | 0.72 |
| R0 ≥ 1 | **2/20** | 6/16 |

**3x vs 5x at matched cutoff:** difference −0.026, SE 0.080,
**|d|/SE = 0.32 — indistinguishable.** The pre-registered conclusion
survives the correction intact, which is the one piece of good news here:
that comparison used cold 800-day seeds on both arms, so it was never
exposed to the confound.

### The limit of the fix, stated rather than buried

Matching cutoffs **cannot** be done for runs that ended before 800 days —
**36 of 131 runs (27%)** halted early, and those are precisely the
early-extinction cases, i.e. the low-R0 tail. So every matched-window
statistic above is **conditional on surviving to ~800 days** and is
survivor-biased upward.

That explains the otherwise-suspicious tightening of the SD from ~0.30 to
**0.134**: matching the window did not reveal a quieter system, it
**excluded the runs that failed**. The two numbers answer different
questions and neither supersedes the other:

- **SD 0.134, mean 0.791, 2/20 ≥ 1** — spread among populations that
  lasted the full protocol. The right noise floor for comparing arms
  *conditional on both surviving*.
- **SD ~0.30, 2/15 and 3/15 ≥ 1, 5/15 extinct per arm** (the cold
  pre-registered batches) — the right numbers for "what does this
  configuration do", because extinction is an outcome, not missing data.

**Practical rule going forward, added to the same discipline as 7b:**
report matched-window R0 *and* the extinction rate as two separate
numbers. Folding extinctions into a matched-window mean is impossible
(they have no window) and silently dropping them inflates every arm.
A single headline R0 for an arm is not a well-defined quantity in this
project.

### What this does not change

The corrected picture is still that **no configuration reaches
replacement**: base dose 2/20 among *survivors* at matched cutoff, and
27% of all runs do not even survive. If anything the matched view is
bleaker than the mixed-length one it replaces — the earlier 6/16 was
partly counting long runs measured over a favourable late window.

---

# STATIONARITY LADDER, seed 1337: HIT — 800 days is far too short, and the base dose IS viable

The single most consequential result of the day, and it points the
opposite way from almost everything concluded before it.

**Discard check first: PASS.** The prediction required the day-600-800
window of the 2400-day run to reproduce the native 800-day run. It
returns **0.728954** against the native run's **0.728954** — exact to six
decimals. The single-long-run design is valid, and this independently
re-confirms that truncation is exactly equivalent to a shorter run.

*(Note: the prediction as written named the target as "R0 1.21". That
figure was itself the 1200-day-window value — one of the numbers the
run-length correction invalidated earlier today. The check was scored
against the corrected 800-day value, 0.728954. Flagging that the
prediction text contained a stale number rather than quietly using the
right one.)*

### The ladder

| window ends | R0 | plant slope | animal slope | mean N | mean plants |
|---|---|---|---|---|---|
| day 800 | **0.729** | 27.0 | 99.0 | 48 | 4230 |
| day 1200 | **1.210** | 43.7 | 103.4 | 59 | 7053 |
| day 1600 | **1.564** | 24.4 | 15.7 | 72 | 10085 |
| day 2000 | **1.522** | −22.7 | 34.2 | 100 | 11352 |
| day 2400 | **1.354** | 17.7 | −27.3 | 100 | 12098 |

**Scored: HIT on both criteria.**
- |R0(2400) − R0(800)| = **0.625**, against a 0.31 threshold — nearly
  double.
- Slopes are materially smaller at 2400 than at 800: plants 27.0 → 17.7,
  animals **99.0 → −27.3** (magnitude 99 → 27). The system is settling,
  not oscillating indefinitely.

### What this means, and it is large

**The base dose crosses replacement between day 800 and day 1200 and
stays above it through day 2400** (1.21, 1.56, 1.52, 1.35). Standing
population climbs 48 → 100 and plateaus; standing plants climb 4230 →
12098 and decelerate. This is a population *establishing*, not failing.

**The session's central conclusion — "no configuration tested reaches
replacement" — is very likely an artifact of the 800-day protocol.** That
claim was recorded at HIGH confidence in `FINDINGS.md` on the strength of
30 cold pre-registered seeds. Those seeds were all 800-day runs, i.e. all
measured during the transient, before the populations had established.

It also explains **corr(run length, R0) = +0.758** cleanly. That was not a
measurement pathology — it is the real signal. Longer runs show higher R0
*because the populations are still climbing at 800 days*. The
"1200-day baseline vs 800-day treatment" mismatch found earlier today was
a genuine confound (two different points on a trajectory), but the
1200-day numbers were the *less* misleading half.

### What is NOT established

- **n = 1 seed.** Seeds 4001 (day 1120 of 2400) and 4002 (just started)
  are running. One seed cannot carry a claim this large, and today has
  repeatedly punished exactly that. **This is not being written into
  `FINDINGS.md` until 4001 and 4002 land.**
- **Not fully settled even at 2400 days.** Slopes of 17.7 and −27.3 are
  still above `analyze.py`'s ~10 DRIFTING threshold, and R0 has drifted
  down from its 1600-day peak (1.564 → 1.354), which could be the start
  of an oscillation rather than a plateau. Where the protocol cutoff
  *should* sit is not yet answerable; day 1600-2000 is the first place
  the slopes drop sharply, but that is a read on one trajectory.
- **This says nothing about the other arms.** Whether 5x, gutcost, or any
  other configuration also establishes given time is untested. The
  pre-registered 3x-vs-5x comparison remains valid *as a comparison at
  800 days* and its conclusion (indistinguishable) is unaffected — but
  both arms may simply have been measured too early.

### Consequence for the protocol

Per the prediction's own stated consequence: **the cutoff must rise, and
every absolute R0 in this file is an early-transient artifact.** The
800-day default in `experiment.yml` (lowered from 1000 earlier in this
session, on the reasoning that 1000 days was "a long time") now looks
like the most costly parameter choice in the project. Not changing it
yet — that decision should wait for 4001/4002, and a cutoff should be
chosen from where the slopes actually flatten across several seeds, not
from one.

### intake-down completes at matched windows: null, and the arm is retired

| seed | base R0 @800d | −33% R0 @800d | ΔR0 | Δ standing plants |
|---|---|---|---|---|
| 1337 | 0.73 | 0.62 | −0.11 | −333 |
| 4001 | 0.71 | 0.77 | **+0.05** | +257 |

Mean ΔR0 **−0.03**, direction split 1/2, against an SE of 0.09 at n=2.
**Null.** Combined with the corrected intake **+50%** result (−0.07, also
null), **`k_intake` has no detectable effect on R0 in either direction at
800 days.** The prediction's HIT branch (base overexploits → ΔR0 > 0 in
≥2/3) and MISS branch (inverted-U → ΔR0 < 0 in ≥2/3) both fail; the
"Ambiguous" branch — all within ±one noise SD — is what actually fired.
Seed 4002 is **not** being run: two null seeds plus a null reciprocal arm
is enough, and the stationarity result below makes any further 800-day
arm comparison low-value.

What survives from the whole `k_intake` investigation is exactly one
thing: **raising intake efficiency depletes the standing plant layer**
(−2683, −762, −9046 on matched windows, 3/3). Lowering it does
approximately nothing to plants (−333, +257). The demographic
consequence I originally claimed does not exist.

---

## The stationarity result has a hard boundary: extinction is terminal

Checking which cold seeds could even in principle be rescued by a longer
protocol turned up the constraint that bounds yesterday's finding.

Among the 15 cold 3x noise-floor seeds, the worst performers **did not
merely score low — they went extinct and the run halted**:

| seed | 800d R0 | ran until | final animals |
|---|---|---|---|
| 10005 | 0.18 | 650 d | **0** |
| 10010 | 0.18 | 590 d | **0** |
| 10006 | 0.25 | 620 d | **0** |
| 10013 | 0.61 | 800 d | **0** |

**A longer cutoff cannot rescue these.** The population is gone; there is
no trajectory left to establish. So the ladder finding does **not** mean
"everything is fine, just run longer." The honest reformulation:

> The base dose produces roughly **one-third outright extinctions**, and
> among the populations that survive, R0 at 800 days **understates** their
> established value — possibly by enough to cross replacement.

That is a genuinely different claim from either "nothing reaches
replacement" (the session's previous headline, now doubtful) or "the
protocol was just too short" (too strong). Extinction rate and
conditional-on-survival R0 are two separate outcomes and neither
substitutes for the other — the same two-numbers discipline recorded for
matched windows.

### Sharpened test now running

Seed 1337 established, but it is one of the "favourable trio"
(1337/4001/4002) I have already flagged as unrepresentative. The strongest
available test is **cold, unselected seeds that survived 800 days but
scored well below replacement** — if even those establish, the claim
holds on seeds that were never chosen for it.

Fired at 2400 days on `evosim-v0_51_0.html`:
- **seed 10001** — 800d R0 **0.64**, 106 animals alive at cutoff
- **seed 10008** — 800d R0 **0.66**, 233 animals alive at cutoff

**Prediction, written before either finishes.** These are cold seeds
drawn as a block, so they carry no selection advantage.
- **HIT:** both cross **R0 ≥ 1.0** by day 2400, and the animal-count slope
  at 2400 is smaller in magnitude than at 800. Reading: establishment is
  general to surviving populations, not a property of the favourable trio,
  and the 800-day protocol is confirmed as the cause of the session's
  central wrong conclusion.
- **MISS:** either seed stays below 1.0 at 2400 with a non-shrinking
  slope. Reading: seed 1337's establishment was particular to that seed,
  and 800-day R0 is not systematically understating anything.
- **Split (one each):** the effect is real but not general; the
  interesting question becomes what distinguishes establishing seeds from
  persistently-subreplacement ones, which is a different investigation.

Deliberately chosen as the seeds *most likely to falsify* the claim among
survivors, rather than the ones most likely to confirm it.

---

# The ladder finding GENERALIZES: n=18, 17/18, across seeds and across arms

Before waiting on the four 2400-day runs, I checked what was already on
disk. **Every run in the corpus of ≥1000 days is itself a partial
ladder** — compute R0 at a matched 800-day window and again at its full
length. That is 18 runs, free, and it settles the question the 2400-day
runs were fired to answer.

| seed | full | R0@800 | R0@full | change | k_photoCost | k_gut | final N |
|---|---|---|---|---|---|---|---|
| 1337 | 2400 | 0.73 | 1.35 | **+0.63** | 0.012 | 0.02 | 82 |
| 6464 | 1200 | 0.81 | 1.20 | +0.39 | 0.012 | 0.02 | 147 |
| 6161 | 1200 | 0.57 | 0.91 | +0.34 | 0.012 | 0.01 | 179 |
| 6262 | 1200 | 0.89 | 1.42 | +0.52 | 0.012 | 0.02 | 141 |
| 8686 | 1200 | 0.86 | 1.15 | +0.29 | 0.012 | 0.01 | 305 |
| 7575 | 1200 | 0.63 | 0.92 | +0.29 | **0.008** | 0.02 | 259 |
| 4001 | 1200 | 0.72 | 1.07 | +0.35 | 0.012 | 0.01 | 51 |
| 4002 | 1200 | 0.92 | 1.31 | +0.39 | 0.012 | 0.02 | 63 |
| 4001 | 1200 | 0.71 | 1.03 | +0.32 | 0.012 | 0.02 | 129 |
| 1337 | 1200 | 0.74 | 1.16 | +0.42 | **0.02** | 0.02 | 47 |
| 1337 | 1200 | 1.03 | 1.80 | +0.77 | **0.008** | 0.02 | 2 |
| 1337 | 1200 | 0.68 | 1.06 | +0.38 | **0.004** | 0.02 | 371 |
| 6363 | 1015 | 0.88 | **0.76** | **−0.12** | 0.012 | 0.02 | **0** |

*(plus 5 more seed-1337 variants, all positive, omitted for length)*

- **R0 rose in 17 of 18 runs.** Mean change **+0.394**, median +0.383.
- **13 of 18 crossed from below replacement to at-or-above it.**
- The single exception, seed 6363, **went extinct** (final N 0) — exactly
  the boundary case identified last cycle.
- The effect spans **k_photoCost 0.004, 0.008, 0.012 and 0.020**, and both
  `k_gut` values. It is not a property of one dose, one arm, or the
  "favourable trio" of seeds.

**This is no longer n=1.** The 2400-day runs still in flight (4001, 4002,
10001, 10008) are now confirmatory rather than decisive.

### The corrected headline for the whole session

Two separate outcomes, neither substituting for the other:

1. **Roughly one-third of runs go extinct early.** Terminal, unaffected
   by any cutoff choice. This is the real failure mode.
2. **Among populations that survive, 800-day R0 understates the
   established value by ~0.39 on average, and most cross replacement
   given time.**

So **"no configuration tested reaches replacement" — recorded at HIGH
confidence in `FINDINGS.md` on the strength of 30 cold pre-registered
seeds — is wrong, and wrong because of the protocol, not the sample.**
Those 30 seeds were correctly drawn, correctly analysed, and measured at
a cutoff that sits in the middle of the establishment transient. Being
rigorous about seed selection did not protect against being wrong about
when to look.

That is the more uncomfortable lesson of the day. The noise floor, the
pre-registration, the cold seeds, the Fisher tests — all of that
machinery was sound and none of it caught this, because every arm shared
the same defective cutoff. **A confound common to every arm is invisible
to any amount of between-arm rigour.** The only things that exposed it
were a verification run that was supposed to be a formality, and then
looking at data already sitting on disk.

### Protocol consequence

`experiment.yml`'s 800-day default is now demonstrably too short.
Changing it is a `main` push (workflow files only take effect from the
default branch) and is within the standing authorization, but I am
**not** changing it this cycle: the right cutoff should come from where
the slopes actually flatten, and the four 2400-day runs that answer that
land shortly. Raising it blind would repeat in the other direction the
mistake being corrected.

---

## The mechanical explanation for the whole artifact — and it is not "run longer"

Characterising seed 1337's completed 2400-day run with a **rolling
400-day window** (local dynamics) rather than `analyze.py`'s cumulative
trailing window:

| window | R0 | mean N | mean plants |
|---|---|---|---|
| d200-600 | **0.77** | 50 | 4358 |
| d400-800 | **1.49** | 37 | 5687 |
| d600-1000 | 1.49 | 49 | 7789 |
| d800-1200 | 1.55 | 74 | 9975 |
| d1000-1400 | **1.60** | 85 | 11020 |
| d1200-1600 | 1.59 | 85 | 11964 |
| d1400-1800 | 1.51 | 110 | 12415 |
| d1600-2000 | 1.32 | 118 | 10945 |
| d1800-2200 | 1.27 | 94 | 10618 |
| d2000-2400 | **1.18** | 85 | 12879 |

**The population establishes by ~day 600 and is at R0 ≈ 1.5 from then
on.** It was never slowly climbing toward viability — it got there early
and stayed.

### So why did the 800-day runs read 0.73?

`analyze.py` computes R0 over the **last `min(n-1, 200)` samples**, and
samples are 5 days apart — so the window is *up to 1000 days long*:

| run length | samples | R0 window covers |
|---|---|---|
| **800 d** | 160 | **days 5-800** ← the entire run, including establishment |
| **1200 d** | 240 | **days 200-1200** ← still includes part of it |
| 1600 d | 320 | days 600-1600 |
| 2400 d | 480 | days 1400-2400 |

**An 800-day run cannot exclude the establishment transient, because its
whole history is shorter than the averaging window.** Its "R0 0.73" is
not the population's R0 at day 800 — it is the average over the
population's entire life including the ~600 days before it established.
That is the complete mechanical account of the confound, and it explains
every symptom: why R0 rose with run length (17/18), why
corr(length, R0) = +0.758, and why the 1200-day baselines read higher
than the 800-day treatments.

### This changes the fix

"Raise the cutoff to 1600+" is only half right, and the cheaper half is
better: **compute R0 over a window that starts after establishment**,
rather than over whatever happens to fit. A 1200-day run already contains
a clean post-establishment stretch (days 600-1200); the default analysis
just doesn't use it.

**This is a measurement fix, not a protocol fix** — and measurement fixes
have been the binding constraint all day. It also costs nothing in
compute, whereas doubling the cutoff doubles every run.

**Deliberately not implementing it this cycle.** Changing how `analyze.py`
computes R0 would silently reinterpret every number in this file, and
three of the four ladder runs that would validate the choice land within
the hour. Queued as the top item, with the shape already clear: an
explicit post-establishment window (`animalStartDay` + a settling margin)
rather than a trailing-N-samples rule.

### The other half: R0 declines after ~1600 days

Worth flagging as unresolved rather than smoothing over. R0 peaks at 1.60
(d1000-1400) and falls monotonically to 1.18 (d2000-2400), while standing
N peaks at 118 and falls to 85. That is either a slow overshoot-and-settle
or the start of a long-period oscillation; 2400 days on one seed cannot
distinguish them. It does mean **there may be no single "settled" R0 to
measure**, which would make the choice of window a genuine judgement call
rather than a technicality. The three ladder runs in flight will show
whether the post-1600 decline is general or particular to this seed.

---

## Ladder seed 4001 (2/4): the post-1600 decline is an OSCILLATION, not a collapse

| window | 4001 R0 | 4001 N | 1337 R0 | 1337 N |
|---|---|---|---|---|
| d200-600 | 0.90 | 160 | 0.77 | 50 |
| d400-800 | **1.11** | 135 | **1.49** | 37 |
| d600-1000 | 1.07 | 135 | 1.49 | 49 |
| d800-1200 | 1.16 | 153 | 1.55 | 74 |
| d1000-1400 | 1.17 | 128 | **1.60** | 85 |
| d1200-1600 | 1.12 | **68** | 1.59 | 85 |
| d1400-1800 | **1.01** | **48** | 1.51 | 110 |
| d1600-2000 | **1.32** | 53 | 1.32 | **118** |
| d1800-2200 | 1.21 | 120 | 1.27 | 94 |
| d2000-2400 | 1.06 | **177** | 1.18 | 85 |

**Both seeds establish early and stay above replacement.** Seed 4001 is
≥1.01 in every window from d400 onward; cumulative R0 at 2400d is **1.11**
(1337: 1.354). n=2 of 4, both viable.

**The open question from last cycle is answered.** Seed 1337's monotone
decline after d1600 (1.60 → 1.18) looked like it might be overshoot into
collapse. Seed 4001 falls to **1.01** at d1400-1800 and then **recovers to
1.32** — so the decline is not terminal. This is a **long-period
oscillation**, not a slide.

**And the standing populations oscillate hard:** 4001 swings N 160 → 48 →
177 (3.7x); 1337 swings 37 → 118 → 85. Plant biomass swings with it.
These are consumer-resource cycles.

Worth connecting to the project's own stated success criterion, which is
in the source header and which I had not been measuring against: *"The
success test is a **stable plant-grazer oscillation**, not a monotone
line."* By that criterion these runs are doing the right thing, and the
flat-line equilibrium I have implicitly been looking for all day was
never the target. The `analyze.py` stationarity gate flags oscillation as
`<<DRIFTING`, which is correct as a warning that R0 is not a fixed
quantity — but it is not evidence of a defect.

**Consequence for the pending measurement fix:** if the system genuinely
cycles with a period of order 800-1200 days, then **there is no single
settled R0 to measure**, and a post-establishment window has to be wide
enough to average over at least one full cycle rather than land on a peak
or trough. That is a stronger constraint than "start after day 600" and
it changes the shape of the fix. Holding implementation until seeds 10001
and 10008 land — those are cold, unselected, and will show whether the
cycle is general.

**Matter flag on this run is the known rounding artifact**, not a new
problem: `7533 -> 7534`, seed 4001, exactly the case root-caused earlier
today as the `Math.round` on export for values ≥1000. Noting it because
`analyze.py` prints `<<LEAK` and a future reader should not re-chase it.

---

# The measurement fix, implemented and validated — and it overturns the headline on the pre-registered sample

## First, a correction to last cycle's framing

I called the post-1600 behaviour "a long-period oscillation". Checking it
properly: the 40-day autocorrelation peak I might have read as a cycle is
the **seasonal forcing** (`daysPerYear: 40`, `seasonAmp: 0.35`). After
smoothing that out, seed 1337 shows a weak peak at 115 d (r=0.41) and
seed 4001 at 85/170/350 d (r=0.31/0.24/0.15), but the mean-crossing
half-periods are wildly heterogeneous — **5 to 495 days (1337), 5 to 590
days (4001)**.

**There is no clean period. These are aperiodic fluctuations**, not a
limit cycle. "Long-period oscillation" was too specific a claim and is
withdrawn. The practical consequence is the opposite of what I wrote last
cycle: since there is no cycle length to average over, the averaging
window should simply be **as long as available after establishment**, and
R0 carries irreducible variance from these fluctuations no matter what.

## The fix `[L61b]`

Added to `analyze.py` — **additively**. The original trailing-200-sample
R0 line is unchanged and still printed first, so every number already in
this file still refers to it. The new line starts the window at
`animalStartDay + 340` (≈ day 600, where establishment completes as
measured on the two 2400-day runs) and runs to the end.

Validation across the three regimes it has to handle:

| run | old (trailing) | new (post-establishment) | rolling-window truth |
|---|---|---|---|
| 1337 @2400d | 1.35 | **1.46** | plateau ≈1.5 ✓ |
| 4001 @2400d | 1.11 | **1.15** | ≈1.1 ✓ |
| **30001 @800d** | **0.72 "NOT VIABLE"** | **1.04** | — |
| 10010 (extinct d585) | 0.18 | **n/a, run too short** | — graceful ✓ |

The 800-day case is the decisive one: **the same run that reported
"R0 0.72 — NOT VIABLE" reports 1.04 once the founding transient is
excluded.** That is the artifact, isolated and fixed, on the exact class
of run the whole session was built on.

## Rescoring the 30 cold pre-registered seeds

This is the sample the retracted headline rested on — drawn as a block
before any results were seen, so it carries no selection advantage.

| arm | old R0 mean | old ≥1 | **new R0 mean** | **new ≥1** | extinct |
|---|---|---|---|---|---|
| 3x | 0.67 | **2/15** | **1.25** | **9/12** | 5/15 |
| 5x | 0.74 | **3/15** | **1.20** | **7/12** | 5/15 |

**Among cold seeds whose populations survived long enough to measure,
three-quarters are above replacement.** The session's headline — "no
configuration tested reaches replacement", recorded at HIGH confidence —
is now definitively wrong, and wrong on its own best evidence.

The honest two-number summary, unchanged in shape from the last two
cycles but now quantified on the pre-registered sample:

> **~1/3 of runs go extinct early (5/15 in both arms) — the real failure
> mode, unaffected by any measurement choice. Among the rest, the base
> configuration sits comfortably above replacement (mean R0 ≈ 1.25).**

Note the 3 seeds per arm that survived but ran <600 days are *not*
counted in the new column — they are neither extinct-by-day-585 nor
measurable post-establishment. Reporting `n=12` rather than quietly
folding them in.

**3x vs 5x on the new metric: 1.25 vs 1.20, 9/12 vs 7/12.** Still
indistinguishable at this n, consistent with the pre-registered
conclusion, which survives its third re-examination.

## What is deliberately NOT done

`analyze.py`'s output is now two R0 lines, and **no existing conclusion
in `LEDGER.md` has been retroactively edited to use the new one.** Doing
that would rewrite history rather than correct it. The rescoring above is
additive and explicit about which metric produced which number.

---

## Infrastructure: why runs kept dying, and using Actions properly [L62]

Prompted by the owner asking two direct questions — how to avoid the
container restarts, and whether Actions compute is being maximised. Both
had the same answer, and the honest response to the second is "no".

### The restarts are not something I can prevent

Measured rather than guessed: **756 MB of 16 GB memory in use, ~80 MB RSS
per sim job, 30 GB free disk, 4 jobs on 4 cores.** Nothing is close to a
limit. The restarts are **platform-side session-worker restarts** — not
resource exhaustion, not anything tuneable from inside. So the goal is
not prevention, it is making work survive them. Two independent fixes:

**1. Long runs belong on Actions, not local cores.** GitHub runners are
entirely independent of this container; a restart here cannot touch them.
Two restarts today killed four multi-hour runs, one at **day 2040 of
2400**. That work should never have been local.

**2. Checkpointing, for the local runs that remain.** `headless.js` wrote
its log exactly once, at the very end, so a killed run produced
**nothing** — hours of CPU for zero data. Now it serialises the full log
to `<out>.partial.json` every `--checkpoint-days` (default **200**),
written atomically via tmp+rename so a partial can never be observed
half-written. `analyze.py` reads it identically — it is the same shape,
just shorter. Verified end to end: a killed 100-day run left a valid
90-day log that digests cleanly, matter conservation intact. The partial
is deleted once the real output lands.

Implementation note worth recording because the first attempt was wrong:
I initially forward-declared `__buildLog` and assigned it after the tick
loop, so the checkpoint hook inside the loop always saw `null` and
silently never fired — the smoke test caught it only because I checked
for the file rather than assuming. Fixed by defining the builder *before*
the loop; it is a closure over live `LOG`/`W` state, so it reads whatever
exists at call time. Gene snapshots need no special handling: the build
already calls `logGenes()` on its own schedule (`LOG.k % LOG.geneEvery`),
so a partial carries the snapshots taken up to that point.

### Actions was idle, and that was a real waste

Straightforwardly: the Actions queue has been **empty for many cycles**
while 4 local cores ground through multi-hour runs. I noted "Actions
queue empty" in cycle after cycle and did nothing about it. That is the
opposite of the standing compute policy and it cost real throughput.

Refilled with the experiment that actually matters now — **30 jobs, the
definitive test of the establishment finding on the cold pre-registered
seeds**, at the corrected 1600-day protocol:

| label | seeds | cfg |
|---|---|---|
| `establish-3x-a` | 10001-10008 | base dose |
| `establish-3x-b` | 10009-10015 | base dose |
| `establish-5x-a` | 20001-20008 | 5x |
| `establish-5x-b` | 20009-20015 | 5x |

**Prediction, written before they land.** These are the same 30 cold
seeds whose 800-day runs produced the retracted "nothing reaches
replacement" headline, now run to 1600 days so a clean 1000-day
post-establishment window exists.
- **HIT:** post-establishment R0 ≥ 1 in **≥70%** of the seeds that
  survive to 1600 days, in both arms, and the two arms remain
  statistically indistinguishable. Reading: the establishment
  interpretation is confirmed on the pre-registered sample at full
  protocol length, and the retraction of the headline stands.
- **MISS:** fewer than half of survivors clear 1.0. Reading: the
  truncated-window rescoring (9/12 and 7/12) was itself an artifact of
  measuring a short post-establishment window on 800-day runs, and the
  establishment story needs rethinking.
- Extinction count is reported **separately** either way, per the
  two-numbers rule — it is an outcome, not missing data.

### Workflow changes (pushed to `main`, within the standing carve-out)

- `timeout-minutes` **180 → 350** and `--max-wall-min` **165 → 330**.
  GitHub hosted runners cap a job at 6 h; this sits near that ceiling with
  margin for checkout/upload, and makes 1600-2400 day runs feasible on
  Actions at all.
- default `days` **800 → 1600**, since an 800-day run cannot exclude the
  founding transient.

### Correction to the [L62] entry above: my "verified end to end" was not

The entry above says the checkpoint work was *"verified end to end"*. It
was not, and the gap is the same shape as the errors this file has been
cataloguing all day.

I tested that the **new** path worked — a partial appeared, `analyze.py`
digested it, matter conservation was intact — and wrote it up. I did not
test that the **existing** path still worked. It did not: `__buildLog`
was declared `const` inside the driver's bare block, so the final
`JSON.stringify(__buildLog())` outside that block threw
`ReferenceError: __buildLog is not defined`. **Every run would have
produced a checkpoint and then died without writing its real output.**
That is strictly worse than the problem being fixed, and it was live in
the committed tree for one commit.

Caught by checking whether the final log file actually existed rather
than trusting the smoke test's exit code — the run exited 0 because the
error was caught and reported by the host wrapper, not because it
succeeded.

**Fixed:** `let __buildLog;` declared outside the block so the final call
can see it, assigned inside the block before the tick loop so the
checkpoint hook can too.

**Now actually verified, all four properties:**

| check | result |
|---|---|
| final log written on a normal run | **yes** |
| partial written mid-run | **yes**, digests cleanly |
| partial removed once the real output lands | **yes** |
| **RNG-safety (hard rule 7)** — log identical with checkpointing on vs off, seed 777 | **`cols`, `genes`, `tick`, `cfg` all IDENTICAL** |

The rule-7 check is the one that matters most and I had not run it in the
first pass either. A measurement-only change must not move the draw
sequence; this one provably does not.

**The generalisable lesson, third time today:** verifying that a new
feature works is not verifying that the change is correct. The regression
is always in the path you did not think to re-test — the `armeff`
contamination, the run-length confound, and now this were all found by
checking something adjacent to what I had just built, not by checking the
thing itself.

### The first 30-job batch failed instantly — `ref` vs workflow-file location

All four dispatches returned `204 queued` and then **every job failed in
seconds**. Cause, found by listing what each branch actually contains
rather than reading logs:

| | `main` | `claude/evolution-sim-v047-audit-jft25c` |
|---|---|---|
| HTML builds | `evosim-v0_49_0.html` only | v0.49, v0.50, **v0.51** |
| `cfg-patches/` | **does not exist** | ~26 patches |

I dispatched with `ref: main` — because I had just pushed the workflow
change there — against `build: evosim-v0_51_0.html` and
`cfg: cfg-patches/arena-speed-photocost.json`. **Neither file exists on
`main`.** The runner checked out `main`, found no build and no cfg, and
died.

**The rule, which I had been following by accident and then broke by
reasoning about it:** the workflow *file* must be on the default branch
for `workflow_dispatch` inputs to register at all, but the *run* must
target the branch that holds the builds and patches. Every earlier
successful batch today used the feature-branch ref; I switched to `main`
only because that is where I had just pushed, and that switch is exactly
what broke it.

Fixed: synced `experiment.yml` onto the feature branch (so the raised
350-min budget applies there too) and re-dispatched all four batches with
`ref: claude/evolution-sim-v047-audit-jft25c`. Confirmed **in_progress**
on the correct head SHA.

Cost: about ten minutes and four wasted dispatches. Cheap, but it is the
third instance today of the same failure mode — *the thing I changed was
fine; what broke was an adjacent assumption I did not re-check.*

---

# Why Actions sat idle for 11 hours overnight — root-caused and fixed

The owner asked why compute was not saturated overnight and whether the
heartbeat was broken. Measured rather than assumed:

**Actions run timeline, 2026-08-10 (UTC):** batches at 00:27, 02:54-03:08,
04:39, 04:51, **05:38 — then nothing until 16:44. An 11.1-hour gap.**

### The heartbeat was NOT broken

`trig_01NMXj4nE2nbtncjqLk4L5pp`, cron `35 * * * *`, `enabled: true`,
`last_fired_at 16:35:14Z`. **It fired every hour, all night, exactly as
configured.** The schedule was never the problem.

### It was structurally incapable of doing the thing it was asked to do

Two hard limits, both verified this cycle:

1. **The Routine's `allowed_tools` contains no `mcp__github__*`.** Listed
   directly from the trigger config. A heartbeat turn cannot call the
   GitHub MCP tools at all.
2. **The ambient `$GITHUB_TOKEN` has Actions read but not
   `actions:write`.** Tested directly: `GET .../actions/runs` succeeds
   (it correctly listed the 30 in-flight jobs), while
   `POST .../workflows/experiment.yml/dispatches` returns
   **403 "Resource not accessible by integration"**.

So a heartbeat can *check* Actions and *collect* results, but **cannot
dispatch a run by any available path**. Every hourly firing overnight did
local work, correctly reported "Actions queue empty", and had no mechanism
to do anything about it. The queue drained at 05:38 and stayed drained
until an interactive turn arrived.

**My fault, and specifically:** I wrote that Routine prompt. I observed
the MCP limitation when creating it, wrote *"work with local compute only…
say so in your report rather than silently skipping the Actions half"* —
i.e. I encoded the limitation as something to *narrate* rather than
something to *solve*, and step 3 of the prompt only ever said "keep all
available **local cores** busy". Actions was not in the instruction.

### Fix 1 — a self-firing standing batch (the structural one)

GitHub's own scheduler needs no credentials from this side, so it is the
only mechanism that works with no interactive turn happening. Added to
`experiment.yml`:

- `schedule: '25 */6 * * *'` — every 6 h, **6 jobs, 24 jobs/day.**
  Deliberately modest, per the "bursty-but-bounded, not always-max"
  amendment (external audit point 9); this is a standing commitment, not
  a burst, and sustained maximum saturation is the pattern that carries
  account-safety risk.
- **Seeds derived from `github.run_number`** (`40000 + run_number*10`),
  so every firing draws *fresh cold seeds* rather than re-burning old
  ones. Each is a valid extra replicate of the establishment protocol
  already on record — the arm that most needs n.
- All inputs defaulted, since a scheduled firing passes none.
- **Checkout pinned to the working branch for scheduled runs.**
  `schedule:` only ever fires from the default branch, and `main`
  deliberately holds only the shipped v0.49 with no `cfg-patches/` — an
  unpinned scheduled run would fail instantly, which is precisely how the
  16:44 batch died. Caught before shipping this time.

### Fix 2 — the heartbeat prompt now checks what it can

Rewritten to state the measured tool reality up front (read yes, dispatch
no, don't retry the 403), to require **both** counts in every report
(local jobs *and* Actions in-flight, via the curl that does work), and to
**escalate loudly** if in-flight is 0 and the last scheduled run is >7 h
old — the exact signature of last night's failure. It also now points at
the checkpoint files and at rule 7b.

### The general lesson

This is the same failure shape as the run-length confound, three cycles
apart: **I correctly identified a limitation, wrote it down accurately,
and then treated the written-down version as the end of the work.** A
constraint that gets documented instead of engineered around is still a
constraint. "Say so in your report" is not a fix.

---

## Establishment batch, first 8 results — and a completion-order trap worth naming before reading them

First returns from the 30-job 1600-day cold-seed batch. **All 8 that have
landed went extinct (final N = 0).**

| seed | arm | ran | R0 trailing | R0 post-est | caps |
|---|---|---|---|---|---|
| 10005 | 3x | 650 d | 0.18 | n/a | clean |
| 10006 | 3x | 620 d | 0.25 | n/a | clean |
| 10010 | 3x | 590 d | 0.18 | n/a | cap |
| 20008 | 5x | 885 d | 0.23 | 0.56 | clean |
| 20009 | 5x | **1290 d** | **1.21** | **1.21** | clean |
| 20011 | 5x | 580 d | 0.14 | n/a | clean |
| 20012 | 5x | 840 d | 0.32 | 0.13 | clean |
| 20013 | 5x | 775 d | 0.53 | n/a | clean |

**Do NOT read an extinction rate off this table.** A run that goes
extinct **autohalts and finishes early**; a run that survives grinds
through the full 1600 days. So results arrive in roughly *inverse order
of health*, and the first 8 of 30 are close to a pure sample of the
failures. Computing 8/8 = "100% extinction" from this would be exactly
the selection artifact that has bitten this project twice today. The
extinction rate is only meaningful once all 30 are in.

### The one genuinely new result: seed 20009

It ran **1290 days**, held **post-establishment R0 1.21** — comfortably
above replacement, on the corrected metric — **and went extinct anyway.**

That is a real complication to the establishment story, and it is not a
measurement artifact: it is the corrected metric, on a cold pre-registered
seed, at full protocol length. **Clearing replacement over a long window
does not confer persistence.** It fits what the aperiodic-fluctuation
analysis already showed — smoothed N swinging 8→407 on one seed, 31→174
on another, with no characteristic period. A population averaging R0 1.21
can still hit zero on a downswing, because extinction is absorbing and a
favourable mean does not protect against a bad excursion.

This sharpens the two-number framing rather than overturning it. The
right pair is not "R0 among survivors" + "extinction rate" as independent
facts — **the second is partly a function of the variance that the first
averages away.** A configuration is only genuinely viable if it clears
replacement *and* its fluctuations stay off zero, and nothing measured so
far separates those.

Recording now, before the survivors land, so the framing is on record
ahead of the data rather than fitted to it.

## Establishment batch, 20 of 30 — R0 > 1 does not predict persistence

Twelve more results landed. Now 20 of 30, and the pattern flagged last
cycle on a single seed is confirmed on several.

| | 3x | 5x |
|---|---|---|
| landed | 8 | 12 |
| extinct | 6 | 8 |
| alive at end | 2 | 4 |
| reached full 1600 d | 2 | 5 |
| survivors' post-est R0 | 1.12, 2.14 (mean 1.63) | 1.04, 1.25, 1.49, 1.59 (mean 1.34) |

Completion-order bias still applies — 10 runs are outstanding and they are
the slow ones, i.e. disproportionately survivors — so **these extinction
counts are still upper bounds, not the rate.**

### The result that matters

Among the 14 runs with a computable post-establishment R0:

- **9 cleared replacement (R0 ≥ 1). Of those, 6 survived and 3 went
  extinct.**
- Extinct runs' R0 values include **1.21, 1.46, and 1.84**.
- The **highest R0 in the entire extinct group (1.84, seed 20005) exceeds
  four of the six survivors' values.** Seed 20005 also ran the *full*
  1600 days — it did not die young, it held R0 1.84 and then went to zero
  inside the last stretch.
- Aggregate signal does exist: alive mean **1.44** vs extinct mean 0.89.

So R0 carries real information in aggregate and **fails badly on the
individual run: one in three populations that cleared replacement still
went extinct.**

### Why this matters more than the dose comparison

The whole session has treated R0 as *the* viability metric — the
retracted headline, the pre-registered 3x-vs-5x rule, the noise floor, all
of it is R0. This says that is the wrong success criterion on its own.
With fluctuations this large (smoothed N swinging 8→407 within a run, no
characteristic period), **mean growth rate does not determine
persistence** — extinction is absorbing, and a population with strongly
positive mean growth still dies if a downswing reaches zero.

A configuration is "balanced" in this project's sense only if it clears
replacement **and** its excursions stay off zero. R0 measures the first
and is blind to the second. The natural replacement is a **persistence
probability** — fraction of cold seeds still alive at a fixed horizon —
with R0 kept as a secondary descriptor. That is directly estimable from
this very batch once all 30 land, at no extra compute.

**Not switching metrics mid-batch.** The 30-seed run has a pre-registered
prediction stated in R0 terms; changing the criterion now, having seen 20
results, is precisely the forking-path move the external audit warned
about. Score the prediction as written, then propose persistence
probability as the successor metric with its own pre-registration.

### Standing batch: still zero scheduled runs

`cron '0 * * * *'` did not fire at 18:00 (verified 18:36, workflow state
`active`, schedule present on `main` since 17:11). Moved to `:37` — but
that change landed at ~18:37-18:38, too late for the 18:37 tick, so it has
not actually been tested yet. **First real test is 19:37.** If that also
produces nothing, `schedule:` is not dependable on this account and the
fallback is deep queues dispatched from interactive turns, since
heartbeats provably cannot dispatch.

## Ladder seed 10001 — the cold falsifier seed HITS

Seed 10001 was chosen deliberately as one of the two seeds **most likely
to falsify** the establishment claim: cold, drawn as part of the
pre-registered block, and reading **R0 0.64 at 800 days** — well below
replacement. Result at 2400 days:

| window ends | R0 | mean N |
|---|---|---|
| day 800 | **0.64** | 64 |
| day 1200 | 0.94 | 70 |
| day 1600 | **1.12** | 90 |
| day 2000 | 1.13 | 92 |
| day 2400 | **1.11** | 86 |

Rolling 400-day windows: 0.77 → **1.09, 1.08, 1.13, 1.13, 1.09, 1.09**.
Survived the full 2400 days (final N 32). Matter clean (6000 → 6000).
The day-800 window reproduces the cold run's 0.64 exactly, confirming
determinism and that this is the same trajectory measured further along.

**This is a HIT on the sharpened prediction**, on the arm designed to
break it. The seed is not marginal — it holds R0 ≈ 1.10 continuously from
day ~500 to day 2400. Its 800-day reading of 0.64 was the averaging
window swallowing the establishment transient, exactly as [L61b]
diagnosed. Seed 10008 still needed to complete the pair.

**A qualifier worth noting, because it cuts against my own volatility
story:** 10001 is remarkably *stable* — rolling R0 stays inside
1.08-1.13 across five consecutive windows, and N stays 60-115. That is
nothing like seed 1337 (1.49 → 1.60 → 1.18) or 4001 (N swinging 48 →
177). So the large aperiodic fluctuations documented earlier are **a
property of some seeds, not of the model uniformly.** Any persistence
metric has to account for that heterogeneity rather than assuming a
common variance — which also means the 3-of-9 extinction-despite-R0>1
result is probably concentrated in the volatile seeds, a hypothesis that
is directly checkable once all 30 land.

Fired seed 10015 (cold, 800d R0 0.72, survived) at 2400 d on the freed
core to extend the ladder — first local run to carry the new
`--checkpoint-days 200` protection.

---

# ESTABLISHMENT BATCH SCORED: HIT. 29/30 cold seeds, both criteria met

The 1600-day re-run of the 30 cold pre-registered seeds is essentially
complete (29 landed, 1 outstanding). Scored against the prediction
written before any of it returned.

**HIT required:** post-establishment R0 ≥ 1 in **≥70%** of seeds surviving
to 1600 days, in **both** arms, and the two arms statistically
indistinguishable.

| arm | n | extinct | alive | **persistence** | survivors with post-est R0 ≥ 1 |
|---|---|---|---|---|---|
| 3x | 14 | 7 | 7 | **50%** | 6/7 = **86%** PASS |
| 5x | 15 | 8 | 7 | **47%** | 7/7 = **100%** PASS |

Persistence 7/14 vs 7/15, **Fisher exact p = 1.000** — indistinguishable.

**VERDICT: HIT on both criteria.**

Survivors' post-establishment R0: 3x mean **1.47**
(0.97, 1.09, 1.12, 1.32, 1.58, 2.06, 2.14); 5x mean **1.37**
(1.04, 1.12, 1.25, 1.49, 1.53, 1.56, 1.59).

### What this settles

**The retracted headline is now definitively dead, on the same
pre-registered sample that produced it.** Those 30 cold seeds read
"2/15 and 3/15 above replacement, nothing is viable" at 800 days. Run to
1600 days and measured post-establishment, **half of them persist and
essentially all persisting ones sit comfortably above replacement.** The
difference is entirely the measurement window — same seeds, same configs,
same code.

**And the 3x-vs-5x conclusion survives its fourth independent
examination**: indistinguishable at 800 d by R0 (p=0.59), indistinguishable
at matched windows (|d|/SE 0.32), and now indistinguishable at 1600 d by
persistence (p=1.000). That comparison has been stable under every
correction applied to it, which is worth something given how much else
moved.

### The two-number summary, now measured rather than asserted

> **Persistence ≈ 50% at 1600 days.** Among the half that persist, R0 sits
> at **1.4**, comfortably above replacement. Among the half that do not,
> the population reaches zero and no measurement choice recovers it.

That is a real, defensible characterisation of where the simulation
currently stands — and it is the first time this project has had one that
survived its own scrutiny.

### R0-vs-persistence, on the fuller sample

17 runs cleared replacement post-establishment. **13 survived, 4 went
extinct** — seeds 20005 (R0 1.84), 10002 (1.46), 20009 (1.21), 10011
(1.06). So **24% of populations that cleared replacement still died**,
down from the 33% seen at n=9 but the same phenomenon. R0 remains a
genuinely imperfect predictor of persistence, which is why persistence
itself is the better headline metric — now pre-registerable for the next
comparison rather than adopted mid-batch.

**Standing batch is confirmed working:** first scheduled run fired
**1:09 PM PDT** (a delayed 12:37 tick — GitHub's scheduler runs loose,
which is normal and not a fault), 12 sim jobs, seeds 41080-41091 derived
from `run_number` exactly as designed. The mechanism that failed silently
overnight is now demonstrably live.

---

## Sharper explanation of "extinct despite R0 > 1": R0 is inflated at low N

The standing batch's first result forced a better answer than the one I
gave two cycles ago. **Seed 41081: post-establishment R0 2.93 — the
highest ever recorded here — and extinct.** Its trajectory:

| window | mean N | min | max |
|---|---|---|---|
| d260-500 | 47 | 0 | 334 |
| d500-750 | 40 | 3 | 691 |
| d750-1000 | **8** | 3 | 13 |
| d1000-1150 | **2** | 0 | 13 |
| d1150+ | 0 | 0 | 0 |

It spent its last 400 days at **N = 2-13**. And R0 is
`births / (mean N × days) × lifespan` — **it divides by mean standing
population.** A handful of animals still reproducing produces a large
ratio. R0 2.93 there does not mean "thriving"; it means demographic noise
in a population of about eight.

**This is the third measurement pathology found today, and the same shape
as the other two:** the arithmetic mean is inflated by rare high-N
excursions (that run peaked at 691) while the quantity that actually
kills a population — how *low* it goes — is averaged away.

### Testing it properly

Across all 25 runs with a computable post-establishment window
(14 survived, 11 extinct), as a predictor of survival:

| predictor | AUC | median (survivors) | median (extinct) |
|---|---|---|---|
| post-establishment R0 | **0.74** | 1.4 | 1.0 |
| harmonic mean N | **0.82** | 54.7 | 18.4 |
| **minimum N reached** | **0.83** | **15.5** | **1.0** |

And the five extinct-despite-R0≥1 cases are exactly the ones that came
near zero:

| | n | mean R0 | harmonic N | min N |
|---|---|---|---|---|
| extinct despite R0≥1 | 5 | 1.70 | **22** | **1** |
| survived with R0≥1 | 13 | 1.45 | **65** | **16** |

**Every one of the five extinct cases touched N = 1 or 2.** None of the
thirteen survivors did — their median minimum is 16. A single threshold,
**harmonic N ≥ 25, predicts survival with 80% accuracy** (13 survivors and
7 extinctions correct, 5 errors) — better than R0 at any cutoff.

### Correcting my own framing

Two cycles ago I wrote that "R0 > 1 does not predict persistence" and
explained it as absorbing-state plus variance. Directionally right, but
vague and slightly wrong in emphasis. The precise statement is:

> **R0 divides by arithmetic mean N, which rare high-N excursions inflate.
> Persistence depends on the low tail. Harmonic mean N and minimum N
> capture that tail directly and outpredict R0 (AUC 0.82-0.83 vs 0.74).**

So the high-R0 extinctions were never paradoxical — they were a metric
reading high *because* the population was small.

**And `analyze.py` has been printing harmonic N all along**, with a
`<<DRIFT REGIME` flag on it. That is now the fourth time today the better
number was already in the digest and going unread — after the `caps`
bitmask, the stationarity gate, and the two R0 lines. The recurring
failure in this project is not missing instrumentation; it is not reading
the instrumentation it already has.

**Not switching the headline metric unilaterally.** Persistence remains
the pre-registerable outcome; harmonic N is a *predictor* of it, and the
right next step is to pre-register "harmonic N ≥ 25 at day 1000 predicts
survival to 1600" on the seeds still outstanding, rather than fitting a
threshold to 25 runs and declaring it. The 80% figure above is in-sample
and will be optimistic.

---

## PRE-REGISTRATION: harmonic N as a persistence predictor, tested out-of-sample

Written **before** fetching the new standing-batch results, so the test is
genuinely out-of-sample. Committed on its own, ahead of the data, so the
git history proves the order.

**Background.** On 25 in-sample runs, harmonic mean N (AUC 0.82) and
minimum N (0.83) both outpredicted post-establishment R0 (0.74) for
survival, and a threshold of **harmonic N ≥ 25** classified 80% correctly.
That 80% is in-sample and fitted to those 25 runs, so it is optimistic by
construction and cannot be quoted as a real accuracy.

**Test set.** The standing batch's fresh cold seeds (41080-41091 and
successors), derived from `github.run_number`, never examined before —
**excluding seeds 41081 and 41086**, which I already inspected last cycle
and which are therefore contaminated.

**Prediction.**
- **HIT:** on the unseen standing seeds, `harmonic N ≥ 25` (measured over
  the post-establishment window) classifies survival-to-run-end with
  **≥70% accuracy**, and its AUC exceeds post-establishment R0's on the
  same seeds. Reading: the low-tail statistic is genuinely the better
  persistence predictor and should replace R0 as the headline health
  metric, with R0 demoted to a descriptor.
- **MISS:** accuracy below 70%, **or** R0's AUC matches or beats harmonic
  N's. Reading: the in-sample advantage was overfitting to 25 runs, R0
  keeps its place, and the extinct-despite-high-R0 cases need a different
  explanation than the low-N inflation account.
- **Can't-tell:** fewer than 8 unseen seeds have a computable
  post-establishment window (needs >600 days), in which case report n and
  wait rather than scoring.

**Guard.** The threshold 25 is frozen at its in-sample value and will not
be re-tuned to the new data — re-fitting and then reporting the fit is the
forking-path failure the external audit named. If 25 turns out to be
badly placed, that is a MISS, not an invitation to pick 30.

### Out-of-sample test: CAN'T-TELL at n=5, not scored

Twelve standing-batch results landed. Applying the pre-registration
written one commit earlier:

| seed | days | R0 post-est | harmonic N | final N | outcome | set |
|---|---|---|---|---|---|---|
| 41081 | 1245 | 2.93 | 7 | 0 | EXTINCT | contaminated |
| 41085 | 1600 | 1.37 | 25 | 43 | alive | unseen |
| 41086 | 1205 | 0.65 | 33 | 0 | EXTINCT | contaminated |
| 41087 | 1020 | 0.65 | 4 | 0 | EXTINCT | unseen |
| 41088 | 1600 | 1.89 | 44 | 73 | alive | unseen |
| 41102 | 910 | 0.41 | 11 | 0 | EXTINCT | unseen |
| 41110 | 865 | 0.32 | 3 | 0 | EXTINCT | unseen |
| 41090, 41100, 41101, 41103, 41108 | 535-705 | n/a | n/a | 0 | EXTINCT | unseen — died before day 600, no window |

**Only 5 unseen seeds have a computable post-establishment window. The
pre-registration requires ≥8. Scored CAN'T-TELL; not evaluated.**

The threshold would have gone 5/5 on those five (41085 harm 25 alive,
41088 harm 44 alive, 41087 harm 4 extinct, 41102 harm 11 extinct, 41110
harm 3 extinct) — **recorded but explicitly not counted.** Scoring a
pre-registered test at n=5 after specifying n≥8, because the early
numbers look good, is precisely the move the guard clause exists to
prevent. Waiting for the batch to fill.

**Completion-order bias again, and worth restating because it will keep
biting:** 10 of 12 landed results are extinctions, and five of those died
before day 600 without ever producing a measurable window. Runs that
survive take the full 1600 days and land last. Any extinction rate read
off a partially-collected batch is an overestimate — the same trap as the
establishment batch, where the first 8 results were 8/8 extinct and the
final figure was ~50%.
