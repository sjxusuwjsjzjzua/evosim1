# Gene Ledger — current as of v0.35.0

One row per active gene. Four questions, all answerable by reading code:

1. **Read?** does the model (not the UI) use it
2. **Charged?** does anything take energy for it
3. **Shape?** cost must curve up faster than benefit (DESIGN §6.1)
4. **Reachable?** are the two sides on commensurate scales

**Any new gene gets a row here, or it does not ship.**

This file is **rewritten each version, not appended to.** It had become a
six-section append log by v0.34, with sections contradicting earlier ones.
History lives in CHANGELOG.md; this is the current picture only.

Verdicts: **OK** · **FLAG** (broken now) · **DORMANT** (waiting on a later phase)

Occupancy figures are from s1337 / v0.33.0, 50.5 sim-years, the best run so far.

---

## Conservation ledger — checked first, because it outranks everything

| transfer | matter | energy | verdict |
|---|---|---|---|
| photosynthesis → plant | none (light) | `gain` added | OK |
| soil → plant mass | `dM × nutrientPerMass` | `dM × energyPerMass` charged | OK |
| seed → seedling | `seedlingMass × nutrientPerMass` | charged since v0.25 | OK |
| parent → offspring | `birth × nutrientPerMass` from gut | `birth × energyPerMassA` charged since v0.27 | OK |
| plant → grazer | mass to gut | `tissueValue × digest`, capped by satiation since v0.33 | OK |
| animal → predator | mass to gut | `meatValue × carnivory` | OK |
| corpse → scavenger | mass to gut | `meatValue × carrionValue × carrionDigest(carn)` | OK |
| death → detritus → soil | conserved | upkeep leaves as heat | OK |
| trophic efficiency, plant path | — | `tissueValue/energyPerMass` = 42% | OK |
| trophic efficiency, meat path | — | `meatValue/energyPerMassA` = 44% | OK |

Measured: matter flat at 6819 over 968,804 ticks, drift 0.000000%.

---

## Plant genes — 39 active + 32 padding = 71 slots. LOCKED.

| # | gene | benefit | cost | shape | v0.33 state | verdict |
|---|---|---|---|---|---|---|
| 0 | maxMass | caps `room` and maturity | indirect | cap, not a trait | 193, interior | **FLAG P4** |
| 1 | height | light band + grazing escape | `k_height·h²·mass`, and `k_stem` cuts leaf | linear / quadratic | 0.326→0.503 | OK |
| 2 | canopySpread | leaf area → light | `k_leaf·leaf` + `k_photoCost·pe²·leaf`, leaf ∝ sp² | saturating / quadratic | 4.71, CV 0.04 | OK |
| 3 | photoEfficiency | linear on gain | `k_photoCost·pe²·leaf` | linear / quadratic | 0.525 | OK, see **P1** |
| 4 | rootDepth | `k_uptake·rd·m^0.75` uptake cap | `k_root·rd²·mass` | linear / quadratic | 0.443 | OK |
| 5 | toughness | cuts bite rate | `k_toughCost·t²·mass` | saturating / quadratic | 0.076, 34% at min | see **P3** |
| 6 | toxicity | saturating loss to eater | `k_toxCost·tx²·mass` | saturating / quadratic | 0.089, **55% at min**, sel − | see **P3** |
| 7 | fibre | cuts digestion | `k_fibreCost·fb²·mass` | saturating / quadratic | 0.278, 18% at min | see **P3** |
| 8 | regrowthRate | cheaper rebuild after a bite | `k_regrowCost·r²·mass` | linear / quadratic | 0.204 | OK |
| 9 | seedCount | seeds per bout | bounded by `repro/costPer` | saturating / none | 3.95→9.68, sel + | OK |
| 10 | seedEnergy | seedling startup capital | linear from repro pool | threshold / linear | 71.8→93.4, sel **+2.44** | OK |
| 11 | dispersalRange | escapes parent shade | `k_disperse·disp²` per seed | unclear / quadratic | 18.0, sel −1.70 | **FLAG P5** |
| 12 | germinationDelay | bet-hedging | seed decay (absolute, tiny) | none / ~none | 1725, 45% at min, sel −156 | **FLAG P6** |
| 13 | shadeTolerance | `+tol·(1−relLight)·k_shadeGain` | `−k_shadeCost·tol` on photoEff | two-sided | 0.192 | OK |
| 14–17 | allocGrowth/Defence/Repro/Storage | split of surplus | renormalised to 1 | pure tradeoff | Defence **51% at min** | **FLAG P3** |
| 18–21 | ageShift ×4 | allocation drift with age | tradeoff | — | interior | OK |
| 22–25 | seasonShift ×4 | allocation drift with season | tradeoff | — | interior | OK |
| 26 | maturityMass | earlier reproduction | two-sided | tradeoff | 25.4, sel +3.11 | OK |
| 27 | lifespan | delays senescence | `k_longevity·life·m^0.75/(sen+0.2)` | linear / coupled | 194k, sel −560 | OK |
| 28 | senescenceRate | buys a cheaper body | accelerates decline | disposable soma | 0.680→1.013 | OK |
| 29 | pollenRange | — | — | phase 5 | 28% at min (drift) | DORMANT |
| 30 | mateChoosiness | — | — | phase 5 | — | DORMANT |
| 31 | selfingTolerance | — | — | phase 5 | — | DORMANT |
| 32 | pathogenResistance | — | — | phase 5.5 | — | DORMANT |
| 33–36 | immunity0–3 | — | — | phase 5.5 | — | DORMANT |
| 37 | mutationRate | self-adaptive, floored | — | by design | 0.109 | OK |
| 38 | mutationScale | self-adaptive | — | by design | 1.02 | OK |

## Animal genes — 54 active + 31 padding = 85 slots. LOCKED.

| # | gene | benefit | cost | shape | v0.33 state | verdict |
|---|---|---|---|---|---|---|
| 0 | size | reach (linear, saturating), bite ∝ m^0.667 | `a_mass·m^0.75` + juvenile period | **upward-curving (v0.36)** | 9.66 / 10.54 / 13.03, was runaway | **FIXED v0.36 — A7/A9** |
| 1 | maxSpeed | travel, pursuit | `k_move·mass·v²` | linear / quadratic | 0.473→0.275 | OK |
| 2 | acceleration | `accCap` | `k_accel·mass·a²` | linear / quadratic | 0.578, CV 0.04 | OK |
| 3 | turnRate | `turnCap` | `k_turn·mass·t²` | linear / quadratic | 0.329 | OK |
| 4 | armour | cuts damage taken | `k_armourC·armour·mass` | saturating / linear | 0.048 — no predators | OK |
| 5 | biteForce | bite & attack damage | `k_bite·bf²/√mass` | linear / quadratic | 0.825 | OK |
| 6 | biteRange | bite without closing | `k_biteRangeC·range²·m^0.75` | linear / quadratic | 0.744 | OK |
| 7 | senseRange | detections | `k_sense·sr²·acuity²` | saturating / quadratic | 20.5 | OK |
| 8 | senseAcuity | detection roll | `k_sense·sr²·acuity²` | bounded / quadratic | 0.506 | OK |
| 9 | camouflage | `(1−hide)` vs other animals | `k_camo·camo²` | bounded / quadratic | 0.312 | OK |
| 10 | carnivory | meat & carrion digestion | `k_digest`, `k_mixed` | frontier + concave | **0.0127, 92% at min** | **FLAG A1** |
| 11 | herbivory | plant digestion | `k_digest`, `k_mixed` | frontier + concave | 0.707, CV 0.03 | OK |
| 12 | fibreTolerance | offsets plant fibre | `k_fibreC·ft²` | linear / quadratic | 0.289 | OK |
| 13 | toxinResistance | offsets plant toxin | `k_toxinC·tr²` | saturating / quadratic | 0.114 | OK |
| 14 | energyCapacity | reserve, and **satiation ceiling** since v0.33 | `k_storeC·cap·m^0.75` | saturating / linear | 3.28 | OK |
| 15 | metabolicRate | throughput at `metRate^0.7` | linear on whole upkeep | sublinear / linear | 0.971→0.374, **43% at min** | **FLAG A2** |
| 16 | maturityAge | earlier breeding | two-sided | tradeoff | 9601, 34% at min | OK |
| 17 | lifespan | delays senescence | `k_longevityA·life·m^0.75/(sen+0.2)` | linear / coupled | 133k | OK |
| 18 | senescenceRate | reduces longevity cost | accelerates decline | disposable soma | 0.726 | OK |
| 19 | birthMassFraction | bigger offspring | gut matter + `birth × energyPerMassA` | linear / linear | 0.163 | OK |
| 20–22 | tag0–2 | kin recognition marker | free by design | — | drifting | OK |
| 23 | pathogenResistance | — | `k_immune` | phase 5.5 | — | DORMANT |
| 24–27 | immunity0–3 | — | — | phase 5.5 | — | DORMANT |
| 28 | thermalTolerance | cuts winter upkeep | `k_thermal·tt²` | linear / quadratic | 0.286 | OK |
| 29–30 | mutationRate/Scale | self-adaptive | — | by design | 0.134 / 0.595 | OK |
| 31 | aggression | gates ATTACK | none by design | self-limiting | 0.090 | OK |
| 32 | fearThreshold | gates FLEE | none by design | self-limiting | 0.319 | OK |
| 33 | hungerUrgency | scales `hunger` | none by design | self-limiting | 0.822, CV 0.02 | OK |
| 34 | preySizeRatio | centre of `sizeMatch` | none by design | self-limiting | 0.619 | OK |
| 35 | preySizeTolerance | width of `sizeMatch` | none by design | self-limiting | 0.362 | OK |
| 36 | plantAttraction | weights GRAZE | none by design | self-limiting | 0.786 | OK |
| 37 | meatAttraction | weights meat value `(0.5+m)` | none by design | self-limiting | 0.095 | OK |
| 38 | carrionAttraction | weights SCAVENGE | none by design | self-limiting | 0.099→**0.306** | OK, see A1 |
| 39 | socialAttraction | weights APPROACH | none by design | self-limiting | 0.343 | OK |
| 40 | socialRadius | herd spacing | none by design | self-limiting | 13.2 | OK |
| 41 | kinRecognition | discounts kin as prey | none by design | self-limiting | 0.247 | OK |
| 42 | territoriality | **NOTHING READS IT** | — | phase 4 never built | 21% at min | **FLAG A5** |
| 43 | explorationBias | wander jitter | none by design | self-limiting | 0.602 | OK |
| 44 | activityPhase | on-phase sensing, off-phase rest | none by design | self-limiting | 0.486 | OK |
| 45 | restThreshold | triggers REST | none by design | self-limiting | 0.353 | OK |
| 46 | ambushTendency | hides a stationary animal | none by design | self-limiting | 0.315 | OK |
| 47 | pursuitPersistence | holds a hunt together | none by design | self-limiting | 96.9 | OK |
| 48 | mateChoosiness | — | — | phase 5 | — | DORMANT |
| 49 | matingThreshold | energy gate on breeding | none by design | self-limiting | 0.823, CV 0.03 | OK |
| 50 | offspringCount | litter size | `invest` + `buildE` + gut each | saturating / linear | 1.90, **62% at min, sel +** | **FLAG A3** |
| 51 | offspringInvestment | newborn reserve, **in upkeep-days** since v0.32 | paid from parent | two-sided | 0.634 d, interior | OK |
| 52 | parentalCare | — | — | phase 5 | **86% at min (drift proof)** | DORMANT |
| 53 | climbing | offsets `terrainDrag` above `foothill` | `k_climbC·climbing²` in the capability group | linear-to-a-cap / quadratic | **71% at min** | **FLAG A4** |

---

## Open flags — the fix queue

### The one that gates the phase

**A1 — carnivory is dead.** 0.0127 with 92% at min, `actAttack` 0.0000 for the
last thousand days, carnivory histogram a single spike, carrion 0.175% of animal
energy intake, ~94% of corpse mass rotting unfound. **v0.34 aims at this and has
not been run**: `carrionDigest` is now a slope (`floor + (1−floor)·carn`) instead
of `max(carn, floor)`, which had made every carnivory below 0.30 worth exactly
the same; and `k_corpseDecay` 0.0025 → 0.0008 so a corpse lasts 1.8 sim-days
instead of 0.58. `carrionAttraction` tripling to 0.306 is independent evidence
that the animals want carrion and cannot reach it.

**The blocker underneath A1 is not a gene, it is Ne.** Harmonic-mean animal
population 2, 3 and 13 across the three v0.35 seeds — an order of magnitude
worse than the 126 recorded below, which came from a shorter, net-supported run.
Harmonic-mean animal
population 126. Proof: `parentalCare`, which nothing reads, sits 86% at its
minimum, and `climbing` 71% — an inert gene cannot be driven to a bound by
selection. `offspringCount` is 62% at min with a *positive* selection
differential, the same signature. `linA` has been 1 for 45 years. At 126
effective animals in 589,824 square units, predation, herding and kin
recognition have no signal to select on.


### New in v0.36 — the three that were never gene problems

**A7 — `size` had no upward-curving net cost.** Intake was `mass^0.75` and the
dominant upkeep term `a_mass` is `mass^0.75`. They cancelled exactly. Only
k_move/k_accel/k_turn/k_armourC scale as `mass^1` and they are ~10% of upkeep;
the reach benefit saturates. So `size` was metabolically free and ran away in
all three v0.35 seeds (4.57→9.66, 3.59→10.54, 3.21→13.03 from founder 5), and
because `buildE = size·birthMassFraction·55` the runaway landed on the price of
an offspring. **Fixed v0.36:** `CFG.biteMassPow = 0.667` splits geometric gape
from metabolic maintenance; `k_intake` pivoted 0.013→0.01486 so the level is
unchanged at founder size and only the shape moves. **Unverified.**

**A8 — growth outbid breeding.** Growth fired at `cap*0.5`, reproduction at
`matingThreshold*cap` = 0.60·cap, so growth triggered at a strictly lower energy
and, absorbing ~6 energy/tick against a ~0.03 surplus, took all of it.
Reproduction needed `room ≤ 0`; mass/size measured 0.53–0.75 and never got
there. **Fixed v0.36:** adults grow only above `max(matingThreshold·cap,
invest+buildE+cap*0.2)`. **Unverified.**

**A9 — the range was doing the selecting.** `mutateAnimal` clamps, so a drifting
gene walks to its range MIDPOINT. `size` .2–40 pulled toward 20.1 from a founder
of 5. Every animal gene that moved in v0.35 moved toward its midpoint. **Fixed
v0.36 for `size` only:** .5–16, midpoint 8.25. **The rest of the table has not
been audited for this and should be** — see invariant 16.

### Curvature and scale

**A2 — `metabolicRate` still pins.** 0.971 → 0.374, 43% at min. Declared fixed in
v0.27 by making it buy throughput at `metabolicRate^0.7` against linear upkeep.
Sublinear benefit against linear cost is still a losing shape whenever the
population is not intake-limited, and this one is not (`aRate`/`aUpkeep` 1.5).

**A3 — `offspringCount` is 62% at min with positive selection.** Read as drift
until Ne is above a few hundred; re-examine after that.

**P1 — `photoCost` is 59.5% of all plant upkeep.** Open since v0.26. The plant
cost model is effectively one term plus noise, and the whole animal kingdom lives
on 1.245% of gross photosynthesis. **This is the lever on animal Ne and therefore
on A1. It must be the only change in the version that touches it.**

**P2 — the standing crop is a vault.** 1,700 adults hold ~180,000 of 181,000
standing biomass at mean mass 106, so `effHeight` ≈ 0.50 against a realised reach
of 0.181 — access 0.045. The fauna lives on the annual seedling cohort, which is
why animal numbers swing 138 → 300 → 141 inside one year while adult biomass
moves 1.44×. That seasonal bottleneck is what sets Ne. `pEscape` reads a healthy
0.21 because it counts plants; the new `pLocked` column weighs biomass through
`accessOf` and is the number to trust.

**P3 — `allocDefence` is 51% at min**, mean 0.065, so realised plant defence is
about 6% of whatever `toughness`, `toxicity` and `fibre` specify. Those three
genes cannot be evaluated until the allocation that gates them comes off its
bound. The mechanism itself works — toxin costs the fauna 7.1% of everything it
eats — so this is about the four-way simplex, not the defence formulas.

**P4 — `maxMass` is inert in practice.** Evolves to ~193 while realised mass P90
is 12–115. A cap the population never approaches.

**P5 — `dispersalRange` is under negative selection** (sel −1.70) while `pOcc`
says the flora only ever fills 50–60% of habitable ground. The gene that would
fill the world is being selected against. A real tension, not obviously a bug.

**P6 — `germinationDelay` is now selected against** (45% at min, sel −156). In
v0.31 it was under strong positive selection. A filling world punishes waiting.
The v0.32 reading that grazing had made it live was a one-seed conclusion.

### Dead genes that should be live

**A4 — `climbing` does not earn its keep.** 71% at min, and `aElev` 0.399 against
`pElev` 0.393 — animals are not using the high ground at all. Either the mountain
band needs food worth the drag, or the gene should be retired to padding.

**A5 — `territoriality`** — nothing reads it. Needs a home point in the state
arrays (two Float32Arrays). Deferred since Phase 4. It is also the most obvious
candidate for giving the mobile kingdom the spatial structure the sessile one
gets for free, which is what plant lineages have and animal lineages do not.

### Legitimately dormant, no action

`pollenRange`, `selfingTolerance`, both `mateChoosiness`, both
`pathogenResistance`, all eight `immunity` genes, `parentalCare`.

---

## What this ledger cannot do

It fixes structure, not magnitudes. Every `k_` remains a guess. The ledger only
guarantees that every gene is read, charged, and shaped so that it *can* find an
interior optimum instead of sitting on a rail.
