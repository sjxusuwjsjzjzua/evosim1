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

