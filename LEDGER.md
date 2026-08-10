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
