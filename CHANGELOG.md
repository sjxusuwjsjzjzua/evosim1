# Changelog

Moved out of the HTML header in v0.35.0. It was ~1,050 lines, read on every
`view` of the file, and almost none of it was needed to work on the current
build. The file is still self-contained; this is documentation, not code.

Newest first. Everything from v0.6.0 is here verbatim as it was written at the
time, including predictions that turned out wrong — those are the useful part.

---

version 0.36.0  ·  2026-08-06

    THREE STRUCTURAL FIXES, ZERO MAGNITUDE CHANGES. Diagnosed from three v0.35.0
    logs (s4976 321d, s6147 690d, s2661 2149d). `photoCost` was NOT touched
    despite being the standing v0.36 candidate in STATE.md — see the correction
    at the end of this entry.

    GROWTH WAS OUTBIDDING BREEDING AND TAKING EVERYTHING. Growth fired at
    `energy > cap*0.5`, reproduction at `energy > matingThreshold*cap`, and
    matingThreshold sat at its 0.60 founder value in all three seeds because
    nothing had ever moved it. So growth triggered at a STRICTLY LOWER energy
    than breeding, and since growth can absorb ~6 energy/tick against an
    observed surplus of ~0.03 energy/tick, it took the entire surplus every time
    the pool refilled. Reproduction could only ever fire once `room <= 0`, i.e.
    once mass reached size — and mass/size measured 0.62, 0.53, 0.75. It never
    got there. Mean standing energy sat BELOW EVEN THE GROWTH GATE in two of
    three seeds (91.2 vs 95.4; 356 vs 373). Lifetime reproductive output was
    0.33, 1.00, 0.33 — R0 < 1, a sink population.

    Juveniles now grow at the old cap*0.5 gate; adults may only grow on energy
    ABOVE the full clutch cost, `max(matingThreshold*cap, invest+buildE+cap*0.2)`.
    Gating on matingThreshold alone was not enough and was a bug in the first
    draft of this fix: an adult parked between the two bars would grow itself
    back down to the lower one forever. birth/nbUp/invest/buildE are hoisted
    above the growth block so both gates read one number.

    This also hands `size` the demographic cost it never had — a bigger adult
    size is now a longer juvenile period spent at risk of starving before
    breeding even once.

    `size` WAS METABOLICALLY FREE. Intake scaled as mass^0.75. `a_mass`, the
    dominant animal upkeep term, scales as mass^0.75. THEY CANCELLED EXACTLY.
    The only super-Kleiber terms are k_move/k_accel/k_turn/k_armourC, roughly
    10% of upkeep at observed genomes, while the reach benefit saturates. So
    size had no upward-curving net cost at all and ran away in every seed:
    4.57->9.66, 3.59->10.54, 3.21->13.03 from a founder of 5. Because
    `buildE = size * birthMassFraction * 55`, that runaway landed directly on
    the price of an offspring: 138, 129, 271 energy against a surplus of 12-19
    energy/day and a mean lifespan of 6.3, 14.8, 9.0 days.

    Bite mass exponent is now `CFG.biteMassPow = 0.667`, separate from Kleiber.
    A bite is geometric — gape scales with length^2, i.e. mass^(2/3) — and
    maintenance is metabolic. Splitting them is the physically correct fix.
    Do not instead break Kleiber on upkeep.

    k_intake 0.013 -> 0.01486, PIVOTED NOT RAISED: 0.013 * 5^0.75 / 5^0.667
    holds intake exactly constant at the founder size of 5. Dropping the
    exponent alone would have cut intake ~12% at founder mass against a surplus
    that is only 12-25% of upkeep — a magnitude change smuggled in beside a
    structural one, which is exactly what makes the next log unreadable. Small
    animals now gain (+12% at mass 1.25), large ones lose (-9% at mass 16).

    A CLAMPED GENE RANGE IS A SELECTION PRESSURE. `mutateAnimal` clamps to
    [min,max], so a drifting gene walks to the MIDDLE of its declared range, not
    to its founder. `size` was .2-40, midpoint 20.1, founder 5 — a permanent
    upward pull. With harmonic-mean population 2, 3 and 13, that pull beat
    selection outright. The same signature is visible across the whole animal
    table: energyCapacity 2.63->4.26 (mid 5.25), biteForce 0.7->2.24 (mid 2.5),
    maxSpeed 0.401->0.943 (mid 1.525), plus toxinResistance, fibreTolerance,
    thermalTolerance, climbing, meatAttraction, territoriality, restThreshold,
    mutationScale — all toward their midpoints. size range is now .5-16,
    midpoint 8.25. This is not a safety margin, it is a claim about plausible
    morphospace. Ranges do not invalidate saves (count and order unchanged) but
    formatVersion moves anyway because the gates changed.

    maturityAge and lifespan pinned at MINIMUM are the exceptions, and they are
    real selection — the population trying to outrun the problem by breeding
    earlier. In s4976 and s2661 the mean animal died BEFORE sexual maturity
    (6.3d vs 21.1d; 9.0d vs 45.4d).

    THEY WERE NOT SHORT OF FOOD AND NOT SHORT OF FORAGING TIME. 92-95% of all
    animal-ticks were spent in ACT_GRAZE. aAccess 0.46-0.78 (high), eaten/grown
    0.16-0.38 (low), animal intake 1.4-7.5% of gross photosynthesis. Binned by
    season quarter, aRate/aUpkeep was 1.09-1.48 in every quarter of every seed —
    no winter bottleneck. They died mid-bite. The constraint was converting
    surplus into offspring, never acquiring food.

    CORRECTION TO THE v0.36 PLAN IN STATE.md. `photoCost` alone was the standing
    recommendation and it was an incomplete diagnosis. More food raises the
    surplus, but with room > 0 permanently true the extra is converted to body
    mass, and a larger body raises buildE for the next generation. Time to first
    reproduction is roughly ((size-birth)*55 + matingThreshold*cap)/surplus —
    ~565 energy at s6147 genomes, ~30 days against a 14.8-day lifespan. DOUBLING
    THE FOOD SUPPLY STILL LEAVES IT AT ~15 DAYS. photoCost may still be right,
    but the gate ordering would have survived it and been re-diagnosed next
    cycle. It remains the v0.37 candidate, alone, after this run is read.

    analyze.py: the life-support test was a false positive. It flagged any
    cumulative aReseed > 200, which caught s2661 (223 reseeds) despite 1889
    unaided days afterwards. It now computes the net-off day from cfg
    (animalStartDay 200 + animalReseedDays 60 = 260), reports unaided days, and
    flags only reseeds ARRIVING AFTER the window, or a run too short to judge.
    Under the new test s4976 is correctly labelled uninterpretable: 61 unaided
    days. Its entire animal history is inside the net.

    RUN PROTOCOL VIOLATION IN THE INPUT. The three logs were 321/690/2149 days.
    Invariant 12 requires the same duration across seeds. s4976 contributed
    nothing and should not have been weighted equally.

    New invariants 15 (growth must not outbid breeding) and 16 (a clamped gene
    range is a selection pressure).

---

version 0.35.0  ·  2026-08-05

    v0.34.0 HAS NOT BEEN RUN. Its two carrion changes are untouched here so the
    experiment stays clean. v0.35.0 adds only instrumentation, all of it
    orthogonal to carrion, plus one clustering fix — because a second reading of
    the s1337 v0.33 log found that the headline result of that run is inflated.

    THE LINEAGE COUNT IS MOSTLY PHANTOM. 70 distinct plant lineage names over
    50 years, and THIRTY-FIVE OF THEM APPEAR IN EXACTLY ONE 10-DAY SNAPSHOT,
    some carrying 200-1,700 members. The tree holds 240 entries under 107
    distinct (name, parent) pairs: "Corvell from Nother" is logged eleven
    separate times, "Olther from Milume" ten, "Gartha from Nother" ten. Only
    about eight are real — Milume for all 202 snapshots, then Umbmyr 111,
    Solsil 102, Nother 85, Yarvell 83, and Hyral / Ophmor / Hysil forming in the
    last fifteen years. The animal side is one lineage, Hyrin, for 45 years,
    with five one-snapshot phantoms budding off it.

    The mechanism is in recluster(). A new cluster is seeded from a SINGLE
    outlier genome and is named, given a parent and pushed to the tree in the
    same instant. It then either has to reach minPop (max(8, 1% of the
    population) = ~140 plants) within one interval or it is killed, or the
    merge pass folds it back into the neighbour it budded from. So an outlier
    spawns a cluster, the cluster grabs a slice of its neighbour's members for
    one pass, and it dies — repeatedly, off the same parent. That is not
    speciation, it is the clustering algorithm breathing.

    v0.35 makes a cluster PROVISIONAL at birth. It gets no name, no tree entry
    and no place in linP until it has held at least minPop for
    `lineageConfirm` consecutive reclusters. Ancestry is the point of the tree
    and it should only record clusters that actually existed.

    TWO NEW MEASUREMENTS, both of which the v0.33 log needed and did not have:

    · pLocked — the fraction of plant BIOMASS out of reach of a median animal,
      mass-weighted through accessOf rather than counted. pEscape reads 0.21
      and looks healthy; the mass-weighted figure is far worse, because the
      1,700 adults holding 180,000 of the 181,000 standing biomass sit at
      effHeight ~0.50 against a realised reach of 0.181 — access 0.045, so
      ROUGHLY 95% OF THE STANDING CROP IS A VAULT. The fauna is living on the
      annual seedling cohort, which is why animal numbers swing 138-300 inside
      a single year while adult biomass moves only 1.18x. That seasonal
      bottleneck is what sets the effective population at ~126 and therefore
      what makes the animal kingdom drift-dominated. pEscape could not show it;
      pLocked can.

    · aDeadSen — animals had no senescent-death bucket. aDeadAge counts only the
      hard cutoff past 3x lifespan and read ZERO across the whole run, while the
      death-age histogram put 37% of deaths in the OLDEST bin. Every one of
      those was filed as starvation. Plants got this split in v0.32; animals
      did not.

    95 -> 97 columns.

    WHAT THE v0.33 RUN GOT RIGHT, so it does not get tuned away:
    · 50.5 years, both kingdoms alive, matter flat at 6819, no cap ever bound,
      and effectively no life support — pReseed 91, aReseed 9.
    · Canopy stratified: the height histogram closes with ALL TWELVE bins
      occupied, 45% of plants above band 0, height 6.2% of plant upkeep.
    · The arms race ran in both directions: plant height 0.326 -> 0.503,
      animal size 5.59 -> 7.25.
    · Juvenile mortality solved: 37% of deaths in the oldest age bin,
      aJuvFrac 0.48, aRate 0.081 against aUpkeep 0.054.
    · The adult canopy is seasonally STABLE (biomass 1.44x, adults 1.52x)
      while the seedling cohort swings 3x. That is forest structure.
    · About eight real plant lineages, persisting for hundreds of days each.

    WHAT IS STILL WRONG, unchanged here on purpose:
    · THE RUN IS NOT STATIONARY. Over the last 1,000 days: plants -6.4% per
      100 days, LAI -4.8%, biomass -3.7%, while animals run +13.1%. Meanwhile
      pHeight +2.8% and pEscape +2.9% against aSize -1.1%: the plants are
      pulling away in the arms race and the flora is thinning into fewer,
      taller, larger individuals. Fifty more years might settle or might crash.
    · photoCost is 59.5% of plant upkeep and the entire animal kingdom lives on
      1.245% of gross photosynthesis. STILL THE ONE CHANGE FOR THE NEXT VERSION,
      alone.
    · metabolicRate is 43% at its minimum and fell 0.97 -> 0.374. B4 was
      declared fixed in v0.27 and it is still pinning.
    · allocDefence is 51% at min, so realised plant defence is ~0.065 of
      whatever the defence genes say. Toughness, toxicity and fibre cannot be
      evaluated until the allocation that gates them is off its bound.
    · carnivory 92% at min, actAttack 0.0000 for the last 200 days, carrion
      0.175% of animal energy intake. That is what v0.34 is for.

    FORMAT_VERSION 34 -> 35. Gene count and order unchanged in both kingdoms.

  version 0.34.0  ·  2026-08-05

    s1337 UNDER v0.33.0 — 50.5 SIM-YEARS, BOTH KINGDOMS ALIVE AT THE END.
    The best run this project has produced. What actually worked, measured:

    · THE ARMS RACE RAN, IN BOTH DIRECTIONS, FOR THE FIRST TIME. Plant `height`
      0.326 -> 0.503 (+54%) while animal `size` 5.6 -> 8.2 (+46%). Realised
      reach 0.204 against a mean effHeight that swings 0.06-0.21 seasonally, so
      the browse line sits inside the height distribution instead of above or
      below it. k_reach anchored at 1/AMAX(size) landed.
    · THE CANOPY IS STRATIFIED. Height histogram closes at
      [7732,4242,666,250,252,736,325,99,60,49,20,13] — every one of the twelve
      bins occupied, against [19244,503,76,10,0,0,0,0,0,0,0,0] in v0.32. 45% of
      plants are above band 0. `height` is now 6% of plant upkeep, not 0-1%.
      k_heightMass 40 turned layered light back on.
    · JUVENILE MORTALITY IS SOLVED. Death-age histogram closes at
      [7,6,8,8,13,2,3,26]: 10% in bin 0 and 37% in the OLDEST bin, against 84%
      in bin 0 two versions ago. aDeathAge rose 10 -> 47 days, aJuvFrac fell
      0.84 -> 0.46. The fauna is adult-dominated and dying of age.
    · THE FAUNA IS SELF-SUSTAINING. aReseed 9, from two firings in the first
      fortnight. No life support after day 320.
    · Matter flat at 6819. No cap ever bound. Plant gain/upkeep 2.03.
      pDeadStarve 813,145 against pDeadEat 389,258 — shading kills twice what
      grazing does, which is what a light-limited flora should look like.

    WHAT IS STILL WRONG, and the two are the same problem:

    A. THE CARRION LADDER HAS NO FIRST RUNG. Of the corpse mass produced,
       roughly 97% rots unfound: 1.4 mass/day eaten against ~40 rotting.
       eCarrion is 12 energy/day out of 8,615 total animal intake — 0.14%.
       actAttack is 0.000 for the last thousand days, the carnivory histogram
       is a single spike in bin 0, and `carnivory` sits at 0.0127 with 91.9%
       at min.

       The cause is a clamp, and this project has a rule about clamps.
       `max(carnivory, carrionFloor)` with carrionFloor 0.30 means carrion is
       FULLY available at carnivory 0 and every value below 0.30 is worth
       exactly the same. Section 7.2 says "above the floor, carnivory still
       pays, so the ladder runs carrion -> carnivory -> predation" — but a
       population sitting at 0.013 is on dead flat ground and can never reach
       the floor to find out. Section 6.1 names this failure: prefer a
       saturating form over a clamp, because a clamp leaves a linear ramp
       below and flat ground above. **Now `carrionFloor + (1-carrionFloor)*carn`,
       which gives the same 0.30 bootstrap at carnivory 0 and the same 1.0 at
       carnivory 1, but has a gradient everywhere in between.**

    B. THE ANIMAL POPULATION IS DRIFT-DOMINATED AND THAT IS THE PHASE 5 BLOCKER.
       Harmonic-mean population over the last thousand days is 123. The
       signature is all over the gene table: coefficient of variation is
       0.02-0.20 on almost every animal gene (herbivory 0.03, hungerUrgency
       0.02, matingThreshold 0.03, acceleration 0.04) where the plants, at
       Ne ~12,000, run 0.2-1.1. Genes that NOTHING READS are pinned at bounds —
       parentalCare 86.5% at min, climbing 70.8% at min — which is impossible
       under selection and diagnostic of drift. `offspringCount` sits at 61.6%
       at min with a POSITIVE selection differential. linA has been 1 for
       forty-five years.

       At 182 animals in 589,824 square units, animal-animal encounters are
       too rare for predation, herding or kin recognition to have any signal,
       and a second lineage cannot differentiate faster than drift erases it.
       The new `aSeen` column measures this directly.

    v0.34.0 CHANGES

    1. Carrion floor: clamp -> slope (above). Structural, section 6.1.
    2. k_corpseDecay 0.0025 -> 0.0008. Corpse half-life 0.58 -> 1.8 sim-days.
       At the realised density a corpse that lasts half a day is not a
       resource. This is the magnitude that pairs with change 1; they aim at
       the same mechanism rather than competing.
    3. LINEAGE NAMES ARE NOW UNIQUE FOR THE LIFE OF THE RUN. The tree carried
       240 entries under 85 names — 'Melthys' fourteen times — because a name
       was only de-duplicated against LIVE lineages and was recycled once a
       cluster died. Ancestry is the point of the tree and it could not
       distinguish two clusters that happened to hash alike.
    4. New column `aSeen`: mean animals detected per sensing animal per look.
       94 -> 95 columns.

    NOT CHANGED, DELIBERATELY, and named so the next run can settle them:

    · photoCost is 59% of plant upkeep. Plants convert 554,760 energy/day into
      1,518 mass/day, burning 84% of gross photosynthesis, and the whole animal
      kingdom lives on 1.6% of it. THIS IS THE LEVER ON ANIMAL POPULATION and
      therefore on everything in B above — but halving it changes the flora,
      the fauna and the arms race in one move, and this run is too good to
      spend on a compound experiment. It should be the ONLY change in v0.35.
    · This run is NOT stationary. Over the last 25 years the seasonal peak
      plant count fell 25,700 -> 13,600, LAI fell 0.68 -> 0.39, and animals
      rose 12 -> 245. The grazers are slowly winning. Fifty more years might
      settle or might crash.
    · `climbing` does not earn its keep: 70.8% at min, and aElev 0.399 against
      pElev 0.393, so animals are not using the high ground at all. That
      answers handoff open question 4, negatively.
    · plantScore has returned an MVT gain in ENERGY PER TICK since v0.32 while
      every other action score is a dimensionless weight. They currently
      balance within a factor of two by luck. Any change to tissueValue,
      gutCapMult or k_intake silently rescales GRAZE against FLEE, ATTACK,
      SCAVENGE and APPROACH. Left alone because this run works; flagged
      because it is fragile.

    FORMAT_VERSION 33 -> 34. Gene count and order unchanged in both kingdoms.

  version 0.33.0  ·  2026-08-05

    THREE v0.32.0 RUNS: s3478, s5419, s7418. Same story in all three.

    THE FLORA FINALLY WORKS. Pre-grazer it reaches LAI 0.60-1.02, 13,000-28,000
    plants, 13-24 plants per occupied tile, and seedlings now die of STARVATION
    rather than of being eaten (pDeadStarve 200-660/day against pDeadEat 0).
    Recruitment survival is 3-9%. limE is 67-80%, so the world is genuinely
    light-limited. That is shading, working, for the first time.

    THEN THE GRAZERS LAND AND EAT EVERYTHING. eaten/grown 1.6, then 7, then 15.
    Flora gone in 30-60 days in every seed. Four separate causes, all mine:

    1. NO SATIATION ANYWHERE. `AN.energy` is never clamped; `energyCapacity`
       named a capacity it did not enforce. Measured in v0.31: aEnergy 132-164
       against a cap of ~54, so animals ran at 3x their own capacity. `hunger`
       scales the arbiter SCORE but never the BITE, so a full animal that still
       ranks GRAZE highest eats at full rate forever. Grazing had no upper
       brake of any kind. **Fixed: a bite can only deliver the energy the
       animal has room for.** Same on attack and scavenge. This also finally
       gives `energyCapacity` a real benefit instead of the perverse one at B6.

    2. k_heightMass 250 IS CALIBRATED TO A MASS NO PLANT REACHES. Realised
       plant mass runs 6-90 with P90 12-115, so sqrt(mass/250) sits at 0.05-0.68
       and the height gene is multiplied by a number that never approaches 1.
       The pre-grazer height histogram is [19244, 503, 76, 10, 0,0,0,0,0,0,0,0]
       — **97% of every flora in band 0.** The eight-band layered Beer-Lambert
       stratification degenerates to one well-mixed layer, `height` is 0-1% of
       plant upkeep, and height buys nothing but a within-band weight.

       THIS IS A REGRESSION OF A BUG THIS PROJECT ALREADY FIXED. Read the
       v0.8.1 note further down: "At k_heightMass 20 a plant needed mass 20
       just to realize half its genetic height, so realized height stayed near
       0.06, EVERY plant sat in band 0, light was shared proportionally again,
       and nothing died. The mechanism was correct and unreachable." It was cut
       to 3, then raised to 100 and to 250 as tiles and maxMass changed — and
       the same failure came back, because the check that justified 100 assumed
       an h-gene of 0.5 and masses of 20-100. The realised h-gene is 0.13-0.24.

       Now 40, checked the same way at the ANCESTRAL h-gene 0.15 and the
       evolved maturityMass:
         mass  5  -> effH 0.053, band 0      (juvenile, overtopped)
         mass 20  -> effH 0.106, band 0/1    (adult, just clears)
         mass 40+ -> effH 0.150, band 1
       and a taller mutant climbs immediately: h-gene 0.4 at mass 40 is band 3,
       h-gene 0.6 is band 4. Realised mass P90 is 12-115, so the population
       straddles the cap rather than sitting under it or flat above it.

    3. k_reach 0.060 WAS CALIBRATED ON A STATISTIC FROM A COLLAPSED WORLD. I
       took mean effHeight 0.19 from the v0.31 log — but that world was a
       sparse stand of old survivors, all its recruits having been eaten. A
       healthy flora's mean effHeight is 0.02-0.05. Result: aAccess 0.66-0.98,
       pEscape 0.00, no refuge at all. Now **0.025, which is 1/AMAX(size)** —
       the largest possible animal can just browse the tallest possible plant.
       That is what design 6.4 asks of the arms race, and it takes this
       constant out of the guessing pool.

    4. THE LOG LIED TO BOTH OF US, TWICE.
       · `ST.apop` COUNTED CORPSES AS LIVING ANIMALS. s3478 day 391 reads 208
         animals; 128 of them were corpses. The HUD said the same.
       · THE RESEED NET WAS INVISIBLE. animalReseedDays 200 from day 260 tops
         the fauna back up to 135 until day 460, and all three runs held ~135-190
         animals and then died within days of the net expiring. That reads
         exactly like a population surviving on carrion. It was life support.
         Reseeds are now logged as columns and events, and the animal net is
         cut 200 -> 60 days so it stops propping up the fauna through the very
         window under test.

    ALSO FIXED: save() never persisted `elev` or `arid`, and load never
    recomputed `fert` or `habFrac`, so loading a save pasted the saved light
    and soil onto whatever terrain happened to be in memory.

    WHAT THE ANIMAL FIXES FROM v0.32 DID, for the record, because they worked:
    offspringInvestment now sits interior at 0.9-1.1 upkeep-days with sd ~0.5
    instead of pinned at a floor; death-age bin 0 fell from 84% to 68%; and
    animal gene variance is real again (size sd 3.2 against a mean of 3.7)
    where v0.31 was a single clone. Plant `lifespan` is live too — pDeadSen
    fires 4,677 times where pDeadAge fired zero times in 59 years.

    STILL OPEN: photoCost is 51-59% of plant upkeep. maxMass evolves to ~205
    but realised mass never exceeds ~115, so it is inert in practice.
    dispersalRange is under negative selection while pOcc says the flora only
    ever fills 20-58% of habitable ground, which is a real tension.

    FORMAT_VERSION 32 -> 33. Gene count and order unchanged in both kingdoms.

  version 0.32.0  ·  2026-08-05

    WHAT THE v0.31.0 LOG SAID (s1337, 59 sim-years, 2,372 samples)

    The three things v0.31.0 set out to fix all landed. eaten/grown came in
    at 0.485 post-arrival, inside the 0.4-0.8 band. pSeedFail fell from 65/day
    to under 2. The flora did get a head start: it peaked at 10,896 plants and
    LAI 0.836 on day 260, the exact day the grazers arrived.

    And the world is still dying. Over the last 1,500 days plants fall 82 per
    100 days, biomass 580, LAI 0.008. Nothing is at equilibrium.

    THE READING THAT MATTERED: eaten/grown IS THE WRONG REGULATOR. It measures
    mass. Lifetime plant fates over the run: 559,116 germinated, 467,492 eaten
    to death, 91,077 starved, none of old age. pGerm/day and pDeadEat/day are
    equal in every window past day 300 — NET RECRUITMENT IS ZERO — while
    eaten/grown reads a healthy 0.48, because a seedling is 0.5 mass and an
    adult is 184. The grazers take almost no biomass and annihilate the entire
    recruitment flux. A metric denominated in mass cannot see that.

    WHY: mean effHeight 0.19 against mean reach 0.0288 (k_reach 0.0175 x an
    evolved size of 1.645) gives access 0.0034. pEscape went 0.205 -> 0.612.
    Adults hold essentially all the biomass and are unreachable, so grazers
    live entirely off seedlings. Zeroed recruitment means adult density stays
    near 0.5 per tile, two adults never share a tile, and the within-tile
    height competition that is supposed to drive plant height NEVER HAPPENS.
    That is why LAI has not exceeded 0.5 since the world was enlarged: shading
    is not switched off, it has no participants. It worked fine at 10,896
    plants on day 260.

    And with height a cheap perfect escape, all three plant defence genes pin
    to their minima under negative selection: toughness at 0.39 on a 184-mass
    plant costs 0.034/tick, toughness 1.0 on the same plant costs 0.74 for a
    4x bite reduction instead of a 300x one. Realised pDefence: 0.023.

    v0.32.0 — ONE MAGNITUDE MOVE, FOUR STRUCTURAL FIXES

    1. k_reach 0.0175 -> 0.060. THE magnitude move; everything else here is
       structural. At 0.060 a mean-height plant (effHeight 0.19) sits at
       h/r 1.94 against the current size 1.645 — access 0.12, with a real
       gradient in both directions instead of dead flat ground. A mid-canopy
       plant at mass 20 comes to access 0.31. That is a browse line: small
       plants edible, big plants safe, and getting bigger is worth paying for
       in BOTH kingdoms. WATCH: aAccess (new) should land 0.15-0.40, pEscape
       0.2-0.5, eaten/grown 0.4-0.8. Sustained eaten/grown over 1.0, or
       pEscape under 0.1, means this went too far.

    2. offspringInvestment IS NOW DENOMINATED IN UPKEEP-DAYS. It was the last
       reserve in the model still in raw energy, and selection drove it to
       0.763 against a newborn upkeep of 0.0423/tick — EIGHTEEN TICKS of life
       before a newborn must feed. Consequences, all measured: 84% of animal
       deaths in the first quarter of maturity (v0.28 had this at 16%),
       aJuvFrac 0.93, nine mature animals in a population of 170, and aBorn
       equal to aDeadStarve in every single window — a pure treadmill with
       77,000 units of plant biomass standing there uneaten. A newborn's
       upkeep is estimated from its parent's by Kleiber. Gene range is now
       0.05-10 DAYS, ancestral 1.0.

    3. PLANT DETECTION SCALES WITH PLANT MASS. A 0.5-mass seedling was exactly
       as findable as a 184-mass adult. That is not a balance choice, it is a
       missing term, and it is the direct cause of recruitment being wiped:
       grazers found seedlings at the same rate as trees and seedlings were
       the only thing they could eat. vis = m/(m+visMass).

    4. plantScore IS NOW THE MVT GAIN FUNCTION and shares every expression
       with grazeYield. The comment claimed they shared; they did not. The
       arbiter valued a plant by min(1, mass/10) while the actual yield is
       bite-rate limited, so animals walked to big plants, earned nothing and
       abandoned them: 2,249,000 abandons, 6.3 per animal per day. Score is
       now patch/(travel + patch/rate) — choose by expected gain, leave by
       marginal rate, which is what MVT actually says.

    5. aUpkeep, aFeedFrac AND aDeathAge WERE WHOLE-RUN RUNNING MEANS, not
       per-day values. Their smooth monotone decline across the whole log was
       an averaging artifact, and I read it as a population trend. They are
       now reset every sample. NOT COMPARABLE WITH ANY EARLIER LOG.

    6. New columns, 86 -> 92: pAdults, pOcc, pPerTile, pMature, aAccess,
       pDeadSen. pMature against pGerm is recruitment survival — the number
       this whole audit needed and did not have. pOcc and pPerTile say
       whether two plants ever share a tile, i.e. whether shading is even
       possible. pDeadSen splits senescent deaths out of pDeadStarve;
       pDeadAge only fires past 3x lifespan and never fired once in 59 years,
       so plant lifespan looked like a pure tax when it was miscounted.

    7. FORMAT_VERSION 31 -> 32. Gene COUNT and ORDER unchanged in both
       kingdoms; offspringInvestment's range, sigma and ancestral value change
       meaning, so pre-v0.32 fossil values of gene 51 are not comparable.

    STILL OPEN, and named so the next log can settle them: photoCost is now
    68.5% of all plant upkeep (was 56-65%) because photoEfficiency evolved
    0.50 -> 0.64 against a quadratic cost — the plant cost model is one term.
    limN has risen 40% -> 59% and is at the stated 60% flip threshold.
    The animal population is one lineage with sd under 3% of the mean on most
    genes; selection differentials on 170 near-clones are mostly noise.
    seedEnergy sits at 121 against a germination cost of 30.

  version 0.31.0  ·  2026-08-05
    WHAT WORKED IN v0.30, from five runs:
    · Rank-normalised terrain is exact. habFrac came out 0.871, 0.874,
      0.875, 0.876, 0.873 across five seeds. The lottery is gone.
    · Founder morphs work. Worlds now open with 4-7 plant lineages instead
      of one, immediately.

    WHAT BROKE, and it was mine:
    · k_intake 0.022 OVERSHOT. I predicted eaten/grown near 0.5 and said past
      1.0 would mean too far. Measured: 1.3, 1.6, 1.8, 2.2, 3.3, and 17 in the
      last gasp of one world. Every run went the same way — grazers land,
      pressure climbs past 1 within a year or two, flora gone by year 5-7.
      Worse, per-capita consumption kept RISING while animal numbers fell:
      the surplus let them grow large, and a bite scales with mass^0.75, so
      grazer biomass climbed while the count dropped. Now 0.013, between the
      two measured points — 0.010 left intake and upkeep equal and nothing
      could grow, 0.022 stripped the world. Target band is 0.4-0.8.
    · animalStartDay 110 -> 260. The real error underneath the intake one.
      The world is 4.35x the area but the grazers still arrived on roughly
      the old schedule, catching a flora of 189-2,249 plants at LAI 0.02-0.42
      that was still climbing steeply. There was never a standing crop to
      graze, only a growth curve, and they ate the curve.
    · MORPH DRAWS WERE SCALED BY GENE RANGE, which is nonsense for a gene
      like seedEnergy (2-400) or maxMass (2-800): morphs drew seed
      provisioning below the germination cost and simply could not
      reproduce. pSeedFail ran at 833-1,621 a year in the opening. Draws are
      now scaled by each gene's own MUTATION SIGMA, which is already
      calibrated per gene, so morphs are a few sigmas apart rather than
      scattered across a range that has no business being uniform.

    · NUTRIENT DIFFUSION IS NOW TERRAIN-AWARE, the piece I deferred in v0.29.
      It was a uniform Laplacian, so soil quietly equalised across a desert
      that could not use it. It is now written as symmetric PAIRWISE FLUX
      weighted by the poorer of the two tiles, which keeps it exactly
      conserving — every flux is added to one tile and subtracted from the
      other in the same statement — while soil moves slowly through barren
      ground. Deserts now stay soil-poor as well as unproductive.

    · FORMAT_VERSION 30 -> 31.
    · TERRAIN IS RANK-NORMALISED. The two runs came out 94% habitable and 43%
      habitable from the same settings, and the 43% world died at year 6 — the
      flora never established before the grazers landed. Value noise averages
      toward its middle and its extremes wander by seed, so raw thresholds
      were a lottery. Both fields are now remapped BY RANK, so elevation and
      aridity are exactly uniform on 0..1 in every world. foothill, treeLine
      and peakElev stop being heights and become FRACTIONS OF THE MAP: 0.68
      means 68% of tiles are lowland, peakElev 0.94 means exactly 6% is
      impassable, every seed, every time. The terrain still differs
      completely between seeds; only the proportions are fixed.
    · k_intake 0.010 -> 0.022, which is why the herbivores never expanded.
      Measured in the healthy run: mean intake 0.076-0.111 per tick against a
      mean upkeep of 0.090-0.094. A grazer feeding 70% of its ticks, with
      38,744 plants available, was earning almost exactly what it cost to
      exist. Net surplus near zero means no growth and no offspring: only
      10-25% of the population ever reached maturity, median body mass sat at
      40% of adult size, and the standing crop went uneaten — eaten/grown was
      0.18, so 82% of primary production was simply left there.
      k_intake is a RATE, not an efficiency, so raising it does not touch the
      trophic transfer. Intake/upkeep goes from about 1.1 to about 2.4.
      Expect eaten/grown to land near 0.5 and the animal population to rise
      several-fold. If eaten/grown goes past 1.0 this went too far.
    · animalStartDay 60 -> 110. In a world 4.35x the area the flora needs
      longer to establish, and the failed run had 85 plants when the grazers
      arrived.
    · FOUNDERS ARE NO LONGER ONE GENOME. Each kingdom is now seeded from
      `founderMorphs` distinct draws, each a genuine random genome rather than
      the ancestral one with noise on it, and copies of each are stamped out
      with the usual per-copy jitter. So a world starts with real variety and
      several lineages instead of one clone lineage that has to invent all its
      diversity by mutation. Morph draws are biased toward the ancestral
      values rather than uniform over the whole range, so founders are varied
      but not absurd.
    · Name bank: 16x12 = 192 possible names -> 44x34 = 1,496.
    · FORMAT_VERSION 29 -> 30.
    TERRAIN. The world gets elevation and aridity, and both make life harder.

    · worldSize 368 -> 768 (48 x 48 tiles, tileSize still 16). 4.35x the
      area. I did not go to 1024 as suggested: that is 7.7x area and, at the
      plant densities the last run reached, would have wanted a slot pool
      around 150,000 and roughly 50MB of genome on a phone. 768 is one
      slider move from 1024 if it turns out to run fine — keep
      worldSize/tiles at 16 when you move it.
    · ELEVATION is ridged noise, 1-|2v-1|, so the high ground forms RANGES
      along contours rather than round blobs. Below `foothill` the ground is
      ordinary. Above it, movement gets progressively harder. At `peakElev`
      it is an absolute wall that nothing crosses, so ranges genuinely
"      partition the map and the two sides can diverge.
    · ARIDITY is a second, independent field. Dry ground is poor ground.
    · FERTILITY combines them: (1 - arid*aridBite) * altitude falloff, zero
      above the tree line. It gates germination and scales growth, and the
"      opening soil is laid down proportional to it, so deserts start poor as
      well as staying poor.
    · Note the plant altitude penalty is deliberately GENTLER than the
      movement penalty. That leaves a band between the foothills and the tree
      line which has food in it but is hard to walk through — which is the
      only thing that can make a climbing gene worth carrying. Barren
      mountains would just pin `climbing` to zero.

    · GENOME CHANGE, FLAGGED LOUDLY. `climbing` is now animal gene 53, taking
      the first reserved padding slot. Active count 53 -> 54, padding 32 -> 31,
      stride UNCHANGED at 85. Indices 0-52 are untouched, so gene positions in
      every existing log still mean what they meant. But the active count has
      changed: old fossil records and any saved genomes are no longer
      comparable, and FORMAT_VERSION goes to 29 so old saves are rejected.

    · Founders are placed on habitable ground only — dropping the opening
      population on a mountainside would just be a slow start disguised as a
      balance problem.
    Three defects, all long-standing. Terrain and world size come next.

    1. WHY THE HERBIVORES NEVER EXPAND. The new age-at-death histogram is
      unambiguous: 73-85% of every animal death happens before a QUARTER of
      maturity, the standing population is 67-100% juveniles, and mean age at
      death is 4-6 sim-days against a maturity age near forty. They are not
      failing to find food — aFeedFrac is 62-78%, they are eating most ticks.
      They are eating and still losing.
"      Cause: nine upkeep terms did not scale with body mass at all, and one
      scaled INVERSELY. a_base, sensing, camouflage, digestion, generalism,
      fibre tolerance, toxin resistance and thermal tolerance were flat, and
      k_bite*biteForce^2/sqrt(mass) actually charged a small animal MORE.
      A newborn earns m^0.75 of an adult intake — about 35% — while paying
      roughly 62% of an adult upkeep. It is a flat tax, and a flat tax falls
      hardest on the smallest body. Section 6.1 says costs charged per unit
      mass^0.75 stay scale-neutral and that anything else smuggles in a size
      bias you have not reasoned about; that is exactly what happened.
      All of these now scale with m75/upkeepRefM75. Juvenile upkeep falls
      about 38%, adult upkeep rises about 8%.
      NOTE this deviates from doc 5.2, which specifies k_bite/sqrt(mass).
      That form was meant to reward large bodies, but size has measured
      negative selection in every run, so it was buying nothing and killing
      juveniles. Flagged deliberately.

    2. THE ANIMALS THAT WALK IN CIRCLES UNTIL THEY DIE. Geometric, and it
      has been there since phase 3. Turning radius is speed/turnCap. At
      turnRate 0.4, turnScale 0.25, mass 5 the cap is 0.08 rad/tick, and at
      maxSpeed 0.4 the radius is 5 units — while the grazing reach is about
      2.8. The animal physically cannot turn tightly enough to close, so it
      orbits its target forever. The inspector says "grazing" because it IS
      grazing: act is ACT_GRAZE the whole time.
      Worse, the marginal-value test could never rescue it. AN.rate decays
      while it is not eating, so the bar it must beat falls toward zero and
      the doomed target keeps clearing it. A death spiral with no exit.
      Two fixes. Approach speed is now capped at dist*turnCap so the turning
"      circle always fits inside the approach — you must slow down to turn
      tightly, which is real. And a stall counter drops any target an animal
      has failed to reach for stallLimit ticks, and bans it from being
      immediately re-chosen.

    3. LINEAGES FLICKERING BETWEEN HUNDREDS AND ZERO. Every clustering pass
      reassigned every organism from scratch to its nearest centroid. Where
      two centroids sit close together in a continuous distribution, tiny
      centroid drift flips hundreds of members across the boundary each pass.
      Assignment is now sticky: you keep your lineage unless another centroid
      is closer by a factor of linStick. Same idea as the grazing hysteresis.

    FORMAT_VERSION 27 -> 28.
    THE LEDGER PASS. Every gene audited for: is it read, is it charged, do
    the two curve correctly, are they on commensurate scales. 92 genes, one
    version, structural only — no magnitude guesses except where a measured
    number forced one, and those are called out.

    A1 ANIMAL BIRTH MINTED FREE BODY MASS. The germination bug, other
      kingdom, still open. birth = size*birthMassFraction was taken from the
      parent GUT (so matter closed, which is why 30 versions of drift checks
      never saw it) but the ENERGY to build that tissue was never charged.
      69-151 energy of free flesh per offspring against an offspringInvestment
      of about 4. It explains every symptom of the last four runs: offspring
      nearly free -> offspringCount 2.8 -> 5.6 unopposed -> newborns carrying
      4 energy against 0.05-0.11/tick upkeep, under a fifth of a day of life
      -> births and starvations matching almost exactly while the world was
      full of uneaten food. Now charged, and the birth is refused if the
      parent cannot pay. Exact mirror of the v0.25 seed fix.

    CURVATURE FIXES (design 6.1 — cost must curve up faster than benefit)
    B1 rootDepth was linear/linear. Cost now quadratic. AND its benefit was
      invisible: measured, the uptake cap was oversupplied about a
      hundredfold, which is why growth was 98-100% energy-limited and
      rootDepth measured negative (S -0.17 to -0.36) as pure overhead.
      k_uptake 0.0006 -> 0.00003 brings it to roughly 5x oversupply, so a
      shallow-rooted plant is throttled and a deep-rooted one is not. Watch
      limN: 1-2% before, should now be tens of percent. If it goes past ~60%
      the world has flipped to nutrient-limited and this wants backing off.
    B2+B3 plant lifespan was linear/linear and plant senescenceRate was a
      PURE TAX with no benefit anywhere — animals got the disposable-soma
      coupling, plants never did. One change fixes both: the longevity term
      is now divided by (senescenceRate + 0.2), so ageing fast is a way of
      buying a cheaper body, exactly as in the animal model.
    B7 dispersalRange: linear cost per seed, measured strongly negative
      (S -0.42 to -0.82). Cost now quadratic; k_disperse rescaled so the
      ancestral 12 costs about what it used to and the top of the range
      costs far more.

    SHAPE FIXES
    D4 leafArea used min(want, support). A hard clamp leaves a linear ramp
      underneath it (6.1) and a flat landscape above. Now a smooth
      saturation, support*(1-exp(-want/support)).
    D5 fibre reduced digestion linearly to a hard floor at zero. Now
      saturating: 1/(1+k_fibreBite*fibre*def*(1-tol)), which never clamps.
    D6 regrowDays 3 -> 6. The cost of regrowthRate is paid every tick, the
      benefit landed in a window covering 0.9% of plants.
    D7 maturityMass is floored at 2x seedlingMass. In v0.24 it evolved to
      1.53 against a seedling mass of 2.5, so every sprout was born mature.

    ANIMAL SIDE
    B4 metabolicRate appeared in exactly ONE place: as a multiplier on the
      whole upkeep expression. Nothing benefited from raising it. A pure tax
      pins to its minimum and it did — measured 1.00 -> 0.30. It now buys
      THROUGHPUT: bite size, attack damage, scavenging rate, growth rate and
      stamina recovery all scale with metabolicRate^0.7 while upkeep scales
      with metabolicRate^1. Sublinear benefit against linear cost, so it has
      an interior optimum instead of a rail.
    B5 biteRange had no cost anywhere. Now k_biteRangeC*range^2*mass^0.75 —
      a long reach is a structural investment.
    B6 energyCapacity had no direct cost either; its only counterbalance was
      the perverse one that a bigger reserve raises the absolute energy
      needed to breed. Now k_storeC*capacity*mass^0.75, against a benefit
      that saturates once the buffer covers a famine.
    C1 meatAttraction was read by NOTHING — I removed it from the attack
      score in v0.21 to kill a double-gate and never gave it another home.
      It now weights the VALUE of meat, (0.5 + meatAttraction), rather than
      gating the action, so it cannot re-create the near-zero double-gate.
    C2 activityPhase was read by nothing either, though section 2.2 says the
      day/night cycle exists to give it something to select on. An animal now
      senses better on-phase and recovers stamina better off-phase, so
      diurnal and nocturnal are a real niche axis. Pure tradeoff, no cost.
    C3 ambushTendency now makes a nearly stationary animal harder to detect.
      Sit still and you are hidden; you also cover no ground. Two-sided, no
      cost term needed. territoriality stays deferred — it needs a home point
      that does not exist in the state arrays, and half-building it would be
      worse than leaving it honest.

    FORMAT_VERSION 26 -> 27.
    · THE SEED PUMP FIX HELD. Across four runs pSeedE sat at 55-62 against a
      germination cost of 30, pSeedFail stayed low, matter closed at
      0.000000%, and no run rebuilt a flora from dozens to twenty thousand in
      a season again. That bug is gone.
    · POISON NOW SATURATES. k_toxinHarm 110 gave toxicity an UNBOUNDED LINEAR
      benefit, which is precisely the shape the curvature rule says will run
      to a bound — and it did: toxicity 0.05 -> 0.60 and still climbing. In
      the s1337 run the toxin drain reached 1,575,000 energy/year against a
      few hundred animals, roughly TWICE their whole metabolic budget, and
      the fauna went extinct at year 38 in a world with 20,000 plants in it.
      A poison should be able to make a meal worthless. It should not be able
      to make it arbitrarily expensive. Loss is now
      meal*toxMaxLoss*toxRaw/(toxRaw+meal): saturating, capped a little above
      the value of the meal, so a fully toxic plant is firmly avoided rather
      than lethal to eat. Benefit saturates, cost stays quadratic.
      The same form is used in all three places toxin is evaluated — the
      target score, the MVT yield and the bite — which were three separate
      expressions before and could disagree.
    · WHAT I COULD NOT SETTLE, and what the new columns are for. In all four
      runs animal births and animal starvations tracked each other almost
      exactly (2,831 born against 2,872 starved in one window) while grazing
      pressure sat at 0.03-0.35, meaning the grazers were leaving 65-97% of
"      plant production uneaten. Abundant food, starving animals, implied mean
      lifespans near seven sim-days against a maturity age of seventeen to
      forty. Three hypotheses fit that and the log cannot separate them:
      newborns dying before they ever feed, animals unable to FIND food, or
      animals unable to PROCESS it fast enough. So this version adds mean
      animal upkeep, the fraction of animal-ticks that landed a bite, mean
      age at death, the juvenile fraction, and an age-at-death histogram in
      units of maturity. One of those three will be obvious next run.
      I have deliberately NOT guessed at k_intake or the birth economics as
      well — changing the toxin and the food supply in the same version would
      make the next log unreadable.
    · FORMAT_VERSION 25 -> 26 (CFG gained toxMaxLoss).
    · THE FREE-BIOMASS PUMP IS CLOSED. Germination created seedlingMass of
      living tissue out of nothing but soil. Normal growth pays
      energyPerMass for every unit of mass; germination paid ZERO. At
      seedlingMass 2.5 that was 150 energy of tissue minted per seed, for a
      seed a parent could provision with as little as 2.
      The population found it. Over 26 years seedEnergy fell 58.6 -> 17.6 and
      maturityMass fell 18.1 -> 1.53 — below the seedling mass itself, so
      every sprout was born mature and immediately spent everything on more
      cheap seeds. The run ended making 1,204,116 seeds a year from a
"      standing crop that dipped to 23 plants, which is 62 slot allocations
      per tick and is why the tick rate died.
      It also fed the animals: a 2.5-mass seedling is worth ~37 energy to a
      grazer and cost its parent ~3, a twelvefold subsidy paid by nobody.
      That is how thousands of animals lived on dozens of plants.
      Germination now debits seedlingMass*energyPerMass*germCostMult from the
      seed. A seed that cannot pay is dead — seed energy only ever decays, so
      it could never pay later. seedEnergy therefore acquires a hard
      viability floor and should stop being selected downward.
    · seedlingMass 2.5 -> 0.5. It was a quarter of the mean adult mass, which
      is not a seedling. At 0.5 the germination debit is 30 energy against an
      ancestral seedEnergy of 58, so the founder is comfortably viable and
      the constraint bites on the cheap-seed strategies rather than on life.
    · WHAT WORKED LAST VERSION, for the record. Toxin harm at 110 finally
      armed the plants: toxicity 0.05 -> 0.60, fibre 0.20 -> 0.48, and
      toxinResistance moved for the first time in this project, 0.20 -> 0.78.
      The carrion floor worked too — eCarrion went from ~0 to 231k/yr, and a
      carnivore burst followed at year 25-26 with 35,114 kills/yr and a
      genuinely bimodal carnivory histogram. Both changes stay.
    · FORMAT_VERSION 24 -> 25 (CFG gained germCostMult).
    · The selection differentials paid for themselves immediately. Measured
      over the s1337 21-year run, in the crisis window:
        toxicity  -0.49 to -0.78 sd     seedCount +0.71 to +0.92 sd
        fibre     -0.29 to -0.43 sd     height    +0.53 to +0.88 sd
        toughness -0.11 to -0.32 sd     regrowth  +0.12 to +0.49 sd
      ALL THREE DEFENCE GENES ARE UNDER NEGATIVE SELECTION. Defence was never
      failing to evolve for want of time or variance — it was actively
      reducing fitness, every generation, in every run.
    · k_toxinHarm 20 -> 110. At toxicity 0.05 a toxin removed 0.72 energy from
      a meal worth ~15 — under 5%. The plant paid a real quadratic cost to
      inconvenience a grazer by a twentieth, so of course it was selected out.
      At 110 a modest 0.15 costs the grazer 15% of the meal and 0.8 makes the
      meal net NEGATIVE, which is what a poison is supposed to do. It also
      gives toxinResistance — flat at 0.20 for the whole project — something
      to respond to. Cost stays quadratic, benefit linear: cost still curves
      up faster.
    · CARRION IS EDIBLE NOW. Up to 1,418 corpses on the map and eCarrion was
      ~0, because carrion energy gates on carnivory and carnivory sits at
      0.02-0.05 — a corpse was worth 3% of its mass to a herbivore. The
      stepping stone was priced out of existence. Carrion digestion now has a
      floor, carrionFloor: rotting flesh is partly digestible by anything,
      which is true of real herbivores and hardcodes no trophic role. Above
      the floor, carnivory still pays, so the ladder runs carrion -> carnivory
      -> predation exactly as design section 10 intends.
    · The MVT comparator ignored poison. AN.rate was updated with gross plant
      energy while grazeYield subtracted toxin, so an animal scored a toxic
      plant honestly and then remembered it as though it had been clean.
    · FORMAT_VERSION 23 -> 24 (CFG gained carrionFloor).
    · k_mixed HAD A FREE BAND ADDED. Charging k_mixed*carn*herb from the very
      first increment taxed carnivory while it was still unused, so all three
      runs PURGED it: 0.058 -> 0.018, fleshMass exactly 0, zero kills. The
      concave frontier is still right for splitting a population that already
      eats both, but it must not tax the exploratory mutation that predation
      has to pass through. Now k_mixed*max(0, carn*herb - mixedFree).
    · meatValue 16 -> 24 and energyPerMassA 40 -> 55. 16 made meat strictly
      worse than plants per unit mass, which killed the payoff. 24 against 55
      is a 44% trophic transfer, matching plant->herbivore at 42%, so a
      trophic level still loses energy and the pyramid cannot invert.
    · k_seedDecay 0.0002 -> 0.00004. THE SEED BANK WAS AN UNREACHABLE
      MECHANISM. germinationDelay ranges to 20,000 ticks, but at the old decay
      a seed dormant that long kept 1.8% of its energy — so dormancy could
      never pay and the bank stayed at 26-948 seeds against thousands of
      plants. It now keeps 45%, which makes a real bank an option. This
      matters because all three runs died the same way: adults escape grazing
      by height, every seedling is eaten, and the stand is reproductively
      sterile until the adults age out. A seed bank is the only buffer that
      survives that, and it was priced out of existence.
    · LOGGING OVERHAUL. Births, energy by source, growth limitation, upkeep
      composition, per-lineage genomes, more histograms, and a per-gene
      SELECTION DIFFERENTIAL — the mean gene of everything that successfully
      reproduced minus the population mean. That last one says which way a
      gene is being pushed RIGHT NOW, instead of waiting many generations for
      the mean to visibly move.
    · PREDATION EMERGED. s6499 ran the carnivory histogram from 95% in the
      bottom bin at year 6 to a distribution centred on 0.5-0.8 by year 17,
      with 606,044 attacks and 95,149 kills. The thesis works.
    · BUT A TROPHIC LEVEL WAS NOT LOSING ENERGY. meatValue 38 against
      energyPerMassA 40 meant eating a unit of flesh returned 95% of what it
      cost to build — an almost lossless trophic transfer, where reality runs
      at 10-20%. Animal biomass ended at 5,020 against a plant biomass of 854
      and the population pinned to its 6,000 slot cap. meatValue 38 -> 16,
      which puts meat->predator at 40%, matching the 42% of plant->herbivore.
      Meat still beats plants for a specialist, so predation stays viable.
    · THE DIET FRONTIER WAS FLAT, SO THE HISTOGRAM SWEPT INSTEAD OF SPLIT.
      Charging only max(0,carn+herb-1)^2 makes every point on the carn+herb=1
      line cost the same, so selection along it is neutral and the whole
      kingdom slides together to whatever the current food mix rewards — which
      is what happened: unimodal at 0.66, not bimodal. Bimodality needs the
      middle to be strictly WORSE than either end, so there is now a
      k_mixed*carn*herb term: zero for a pure specialist, maximal at 50/50.
      Jack of all trades, master of none, which is the disruptive selection
      the phase 4 success test actually requires.
    · maxAnimals 6000 -> 20000. The cap bound at year 16.9 and whatever caps
      the population is what does the selecting.
    · Flesh and carrion are now logged as MASS, not just bite counts. The
      trophic question above had to be answered by estimating bite size, which
      is exactly the sort of thing the log should not make me guess at.
    · Interface: live tick rate, richer inspector, per-lineage descriptions,
      ancestry, and colour-by modes.
    · PREDATION WAS UNREACHABLE. Two runs, 67 sim-years between them: ZERO
      attacks and zero kills. Three compounding reasons, all now fixed.
      1. ATTACK was double-gated. Scoring it as aggression x meatAttraction
         multiplied two genes that both start near 0.1-0.2, putting attack
         ~17x below scavenging and ~76x below grazing at founding. Design
         section 7 specifies aggression alone; it now matches.
      2. k_attack 0.030 -> 0.12. A bite took ~1.5% of a typical animal, so
         killing anything needed ~60 uninterrupted ticks. Even a forced
         carnivore morph landed 228 attacks and zero kills.
      3. No pursuit. The arbiter re-decided every think-tick, so an attacker
         never stayed on one target long enough to finish. pursuitPersistence
         has been in the genome since phase 3 and was never read; it now
         holds a hunt together.
    · SCAVENGING, BY CONTRAST, WORKED EXACTLY AS DESIGNED. 114,534 carrion
      bites in the s1337 run, and carnivory rose 0.039 -> 0.118 on carrion
      alone. The stepping stone is real; it just had nowhere to step to.
    · UI rebuilt — see the interface section.
    · PHASE 4: OMNIVORY. carnivory stops being inert. Animals can attack each
      other, corpses persist as entities, and scavenging is available as the
      cheap stepping stone toward predation. Nothing is hardcoded: there is
      no predator flag. An animal that bites another gains energy in
      proportion to its carnivory gene, pays stamina, and takes retaliation.
      Early on that trade is bad, so aggression is selected against — until
      one lineage in one crowded corner finds it is not.
    · CORPSES ARE A STAGE, NOT A NEW POOL. AN.stage 0 empty / 1 alive /
      2 corpse. A corpse keeps its mass, does not move, pays no upkeep, and
      bleeds into the tile detritus at k_corpseDecay until it is gone or
      eaten. Reusing the animal pool avoids a third entity type entirely.
    · THE GENERALISM PENALTY IS NOW CHARGED: k_digest*max(0,carn+herb-1)^2.
      This is what stops both digestion genes reaching 1 and is the reason
      the carnivory histogram should go bimodal rather than mushy.
    · FORMAT_VERSION 20 -> 21.
    HOUSEKEEPING from the 40-year run:
    · maxPlants 30000 -> 45000. plants+seeds touched 30000 exactly in years
      16-24; brief, but the array was doing the selecting during the window
      the height strategy took over.
    · k_regrowCost 0.0025 -> 0.0010. regrowthRate DECLINED 0.20 -> 0.15 under
      the first tuning: the cost is paid every tick, the benefit only lands in
      the window after a bite, so as priced it was mildly deleterious.
    · A lineage must now hold >=1% of its kingdom across 3 consecutive log
      samples before it is announced. The last run emitted 80+ events for
      what were mostly single-outlier clusters living two passes.
    · regrowthRate IS FINALLY WIRED. It has sat in the plant gene table since
      phase 2 marked "inert until phase 3", and phase 3 was built three
      versions ago without anyone reading it. Compensatory regrowth is THE
      stabilising feedback in real grazing systems: a cropped plant still has
      its roots and meristems, so rebuilding leaf is cheaper than growing it
      the first time. Without it every mouthful was a permanent loss that had
      to be rebuilt at the full energyPerMass of 60, so the standing crop
      could never track grazing pressure and every run ended in a boom-bust.
      A plant bitten within regrowDays rebuilds at
      energyPerMass*(1 - k_regrow*regrowthRate), against a permanent upkeep
      of k_regrowCost*regrowthRate^2*mass for holding the capacity ready.
      Benefit linear and bounded by what was lost, cost quadratic.
    · FORMAT_VERSION 19 -> 20 (CFG gained k_regrow/k_regrowCost/regrowDays).
    · Diagnosis this came from: with height no longer pinning, two runs both
      ended with the GRAZERS extinct and the plants fine. Starvation killed
      every animal, yet energyCapacity never rose (2.97->3.22) because when
      everyone dies in the bust, surviving the bust cannot be selected for.
      What did evolve was a race to the bottom: matingThreshold 0.60->0.41
      and maturityAge 20294->2697, breeding ever earlier on ever less.
    · REACH AND HEIGHT NOW SHARE A SCALE. reach was k_reach*size^0.4, which
      tops out at 0.127 even at the maximum size of 40, while effHeight goes
      to 1.0. The arms race was unwinnable: over 200 years the animals did
      everything right — size 5.6->11.9, biteForce 1.13->3.18, senseRange
      20->30 — and still could not follow. 100% of plants ended out of reach.
      reach is now LINEAR in size, k_reach 0.0175: size 5 -> 0.088,
      size 40 -> 0.70. A max-height plant is still 26% accessible to the
      largest animal, so the refuge is partial rather than absolute.
      (Scaling k_reach to the OBSERVED height distribution instead of the
      ACHIEVABLE one was the error — design section 10, unreachable mechanism.)
    · k_height 0.0003 -> 0.0012. Measured: taking the height gene from 0.15
      to 1.0 at mass 150 cost only 9% more upkeep and bought total immunity
      to grazing, so height pinned at max (98% of the population, sd 0.013).
      At 0.0012 the same move costs ~36%.
    · seedSlotFraction 0.25 -> 0.6. The seed bank sat at its 7500 cap for 30%
      of the run (years 25-102) — the array selecting again, this time in the
      seed compartment.
    · W.grown now counts mass created at germination. It previously counted
      only incremental growth of standing plants, so in a recruitment-driven
      world eaten/grown read 2.4-3.3 while biomass was in fact steady. The
      grazing-pressure metric was wrong in exactly the regime that matters.
    · A lineage must persist two consecutive samples before it is announced,
      killing the appear/vanish churn that produced 95 events for 1 lineage.
    · HEIGHT-LIMITED BROWSING. Until now every plant was edible by every
      animal at all times, so plant biomass was a common pool with no
      protected fraction and could be driven to zero. A grazer now reaches
      only so high: access = 1/(1 + (effHeight/reach)^2), reach =
      k_reach * size^0.4. Graded, not a cliff, so height has a gradient to
      climb. This is the same asymmetry that already makes plant-plant
      light competition work, applied to the plant-animal interaction.
      k_reach 0.029 puts a median animal (size 5) at reach 0.055 against a
      measured effHeight distribution of p50 0.022 / p90 0.041 / p99 0.076,
      so access is 0.94 at the median, 0.71 at p90 and 0.28 at p99.
      Curvature: plant height cost is quadratic, escape saturates. Animal
      reach costs Kleiber on a x5.7 mass for a x2 reach, benefit saturates.
    · FORAGING IS NOW MARGINAL-VALUE-THEOREM. v0.16.1 compared the current
      plant to the best alternative in view, but detection is stochastic so
      that comparator was noise: grazers abandoned ~15 targets each per day
      and spread their grazing so thinly that no plant could grow. A grazer
      now keeps its plant while that plant yields more than its own running
      average intake (EWMA) times CFG.mvtLeave. In a poor world the average
      falls too, so animals stop thrashing and settle - which is the brake
      the system has been missing.
    · FORMAT_VERSION 18 -> 19 (grazeStick out, k_reach/mvtLeave/rateEwma in).
    · GRAZE HYSTERESIS IS NOW A BONUS, NOT A LOCK. Previously a grazer that
      started on a plant never re-evaluated the target and stayed until the
      plant died. Defence could therefore only change the DURATION of a
      death, never the outcome, so toughness/fibre bought a delay while
      biteForce bought a meal. Over 8 generations biteForce rose 37% and
      toxicity fell. A grazer now holds its plant only while that plant
      still beats the best alternative in view, times CFG.grazeStick.
    · TOUGHNESS IS NOW VISIBLE TO THE ARBITER. The graze score already
      carried fibre and toxicity but not toughness, which sets the bite
      RATE. Without it a tough plant looked exactly as good as a soft one.
    · Fixes a latent bug: a grazer whose target died kept pointing at the
      dead slot for as long as any plant stayed in view.
    · FORMAT_VERSION 17 -> 18 (CFG gained grazeStick). Old saves rejected.
    · Log gains: behaviour mix, abandonment count, deaths by cause, named
      lineage tracks, and a discrete event list.
    · 0.16.1: plant deaths are attributed properly. A grazed plant almost
      never reaches the kill-by-mass threshold — it is cropped, fails
      energetically and dies by the ordinary energy test, so the first cut
      of this counter recorded 0 eaten and 5279 starved in a world that was
      visibly being eaten. P.bit stamps the last bite, and a plant that dies
      within two sim-days of being bitten is counted as grazed, not starved.
    · TUNING WORLD: area halved (23x23 tiles of 368 units) to iterate faster.
      tileSize stays 16 and nutrientStart stays per-tile, so matter DENSITY
      and the per-tile light budget are unchanged - the ecology per unit area
      is identical, there is simply less of it. Total matter halves with area,
      which is correct. Keep worldSize / tiles == 16 when retuning either.
    · Founder counts and floors halved with the area, so founding DENSITY
      is unchanged.
    · maxPlants 20000 -> 30000. In the full world the plant slot cap bound
      from year 3.4 to 9.4, exactly while grazers were building, and forced
      the population to shrink individuals instead of adding them. At half
      area the ceiling is ~10k, so 30000 slots cannot bind and the array
      stops doing the selecting.  ·  save formatVersion 15
    · RUN LOG: telemetry sampled once per sim-day, exported as JSON from
      the menu drawer. Pure instrumentation — reads state, never writes it.
    · W.eaten / W.grown counters, so grazing pressure (eaten/grown) is
      measurable. >1 means the standing crop is being mined.

  0.11.1 — fixes a broken 0.11.0 patch. buildPlantIndex, PIDX and laiOf were
  called but never defined, and P.defence was declared but never allocated, so
  the first tick threw. A syntax check cannot catch a missing definition; the
  build now also runs a static undefined-call check.
  PHASE 3 — ANIMALS, HERBIVORY ONLY.

  0.11.0
    · ANIMAL GENOME LOCKED: 53 active + 32 padding = 85 slots. Order fixed.
    · Spatial index by tile for plants (rebuilt with the canopy) and animals
      (rebuilt every tick). Sense scans tiles in order of distance and stops
      after senseCap detections — that cap is what saturates senseRange's
      benefit and stops it pinning (design 6.1).
    · Utility arbiter: GRAZE / APPROACH / REST / WANDER, with hysteresis.
      ATTACK, FLEE, SCAVENGE and MATE wait for phase 4/5; their genes drift.
    · Movement by acceleration and turn-rate caps, both scaled down by mass.
    · PLANT DEFENCE GENES ARE NOW LIVE. toughness resists the bite, fibre
      resists digestion, toxicity harms the eater. Their cost is paid out of
      allocDefence, which finally has a job: realized defence = what the plant
      actually spent, over what its genes ask for.
    · Matter still closes. A bite moves mass from plant to the animal's gut;
      growth draws on it; the surplus is excreted to tile detritus; death
      returns body mass and gut alike.
    · Cost model checked headless first: ancestral grazer runs ~1.7x gain over
      upkeep, equilibrium ~430 animals against a design target of 600.

  0.10.0 — COARSER TILES, TO BUY BACK THE TICK BUDGET

  0.10.0 — COARSER TILES, TO BUY BACK THE TICK BUDGET
    A plant draws light only from its own tile, so leaf area beyond tileArea is
    wasted. That put a hard floor under plant count: LAI x worldArea / tileArea.
    At tiles 64 (area 64) the floor was ~10,000 and the observed equilibrium was
    27,716 at 383 t/s — no room for animals, which cost far more per tick.

    tiles 64 -> 32 (area 256). Verified before shipping: recruitment blocks above
    ~1 adult/tile, adults die above ~2.7, equilibrium 2,000-3,000 plants needing
    4,573 of 6,144 available matter. That is the design's 4,000-plant target and
    roughly a tenth of the tick cost.

    Matter is stored PER TILE, so quartering the tile count quartered the world's
    matter. nutrientStart 1.5 -> 6.0 and nutrientCap 3 -> 12 keep the total the
    same. canopySpread max 6 -> 10 and maxMass 80 -> 200 so a plant can actually
    fill the larger tile; k_heightMass 100 -> 250 so the size hierarchy spans the
    new mass range.

  0.9.1

  0.9.1
    · Strobe suppression came in far too late. It began at 0.4 sim-days/sec and
      only reached full at 1.6, so at 383 t/s (0.8 d/s) two thirds of the day
      swing was still being drawn — a pulse roughly once a second. Now it starts
      at 0.08 d/s and is fully flat by 0.30, i.e. once a day passes in under
      about three seconds of watching. Render only; the simulation is untouched.
    · The height trace on the graph was scaled 0..1 and therefore invisible at
      the values height actually takes. It now autoscales to its own range, so
      the phase 2 success test can be read at a glance.

  0.9.0 — SLOT COUNT IS NOW ALMOST FREE
    Every loop over plants walked all maxPlants indices and skipped dead ones, so
    raising the slot pool cost tick time even when the population was far below
    it. The pool is now bounded by a high-water mark (P.hi), and because the free
    list reuses low indices first, that mark tracks peak concurrent population.
    Raising maxPlants now costs memory and essentially no time.

    This matters because "population sat at the cap" is only a failure if the cap
    is what stopped it. A 512x512 world, tiles of area 64, plants that have
    evolved leaf ~63 (one full tile), and LAI ~2.5 genuinely holds around 10,000
    plants. The question was never whether the number is small — only whether the
    population stops on its own. Default pool raised to 40,000 so that can
    actually be observed. Memory is the limit now: ~330 bytes per slot, so 40,000
    is ~13 MB and 100,000 is ~33 MB.

  0.8.2 — REALIZED HEIGHT SATURATED TOO FAST
    v0.8.1 got the arms race running (h-gene finally moved, 0.15 -> 0.30) but the
    population still capped. Cause: m/(m+3) reaches 0.5 at mass 3 and 0.9 at mass
    27, so a mass-5 seedling and a mass-60 adult had realized heights of 0.19 and
    0.285 — the size hierarchy collapsed into one or two bands and proportional
    sharing came back. The tell in the run was mean leaf ~23 against a predicted
    47: the population was mostly small plants that should not have survived.

    Now effHeight = h * min(1, sqrt(mass/k_heightMass)), k_heightMass 3 -> 100.
    Checked before shipping, at h-gene 0.5:
      mass  2.5 -> band 0    mass 22 -> band 1
      mass   60 -> band 3    mass 100 -> band 4     (old form: bands 1 to 3 only)
    Recruitment blocks above ~1 adult/tile (~4,100 adults); adults themselves
    start dying above ~2.7/tile. Equilibrium sits well under the slot pool.

  0.8.1 — k_heightMass 20 -> 3
    0.8.0 built the asymmetry but put it out of reach. At k_heightMass 20 a plant
    needed mass 20 just to realize half its genetic height, so realized height
    stayed near 0.06, EVERY plant sat in band 0, light was shared proportionally
    again, and nothing died. Observed run: h-gene never moved off 0.15, LAI 1.42,
    population back at the cap. The mechanism was correct and unreachable.

    At k_heightMass 3, checked numerically before shipping:
      · adult (mass 20) lands in band 1, seedling (mass 2.5) in band 0
      · seedling runs 0.64x at 1.5 adults/tile and dies
      · a taller mutant invades at every step from h 0.15 upward, and an
        overtopped resident's surplus goes NEGATIVE — the arms race has a
        gradient, and losing it is fatal
      · recruitment is blocked above ~1.2 adults/tile, so the population is
        bounded by light near 5,000 adults, about a third of the slot pool
    Ancestral height stays 0.15 — the payoff should emerge, not be handed over.
  PHASE 2 — PLANTS ONLY.

  0.8.0 — BREAKING SCALE INVARIANCE
    The 30,000-slot test settled it: population doubled and mean mass halved
    (20.3 -> 10.9). With leaf = k_leafPerMass * mass, gain is proportional to
    mass and upkeep is proportional to mass, so two plants of mass 10 and one of
    mass 20 have identical total fitness. Nothing in the model preferred any
    plant size, so the population always ran to whatever hard bound it met — the
    array. Competition was symmetric: proportional light sharing has no losers.

    · HEIGHT MUST BE EARNED WITH MASS.  effHeight = heightGene * m/(m+k_heightMass).
      A seedling has no trunk and cannot be tall. Large plants reach the upper
      bands and take light first; small ones get the residual. By the arithmetic
      an understory plant now runs gain 0.008 against upkeep 0.035 and dies.
      That is the asymmetry that bounds population by light instead of by slots.
    · HEIGHT COSTS CANOPY.  leafSupport = k_leafPerMass*m / (1 + k_stem*effHeight).
      Mass in the stem is mass not in leaves, so tall-narrow vs short-broad is a
      real axis and height is worth paying for only when crowded.
    · photoEfficiency cost is now QUADRATIC (k_photoCost * eff^2 * leaf). It was
      pinned at 0.95 because benefit and cost were both linear in eff, so it
      could only sit at a rail. GENERAL RULE, worth adding to design section 10:
      any gene with linear benefit and linear cost will pin to a bound.
    · GENERATION TIME. energyPerMass 1 -> 60, so first reproduction lands near
      one sim-year instead of ~2 days. lifespan, germinationDelay, seedEnergy and
      seed decay all rescaled to match. Costs ~17x more compute per generation.
    · Canopy bands 6 -> 8, now indexed by realized height. Slots 12k -> 16k.
    · k_longevity is now charged per unit mass^0.75, so it stays scale-neutral
      and does not smuggle in a second size bias.

  0.7.0 — WHY THE SLOT CAP KEPT WINNING
    At the cap, spawnSeed fails constantly, so surplus energy has NO fitness
    value: it cannot become offspring. The only selection left is "do not die",
    which rewards low upkeep, which rewards being small. Every matter increase in
    0.5.0 and 0.6.0 was therefore ignored — v0.6.0 ended with 91% of all matter
    sitting unused in the soil and mean mass falling to 3.5.

    Two states are self-consistent at LAI 2: ~8,000 large plants, or ~52,000 tiny
    ones. The large-plant state has roughly 80x the per-plant energy surplus and
    wins on selection easily. But from founders at spread 0.8 the population
    reaches the 12,000-slot cap within a few generations — long before
    canopySpread can evolve — and the cap then freezes the small state in place.
    It is a transient trap, not an equilibrium.

    Fix: found the world inside the correct basin. Ancestral canopySpread
    0.8 -> 4.5, maxMass 20 -> 80, maturityMass 8 -> 18, seedEnergy 4 -> 10,
    seedlingMass 0.5 -> 2.5. Expected equilibrium ~8,000 plants at mass ~25 and
    LAI ~2, limited by LIGHT with soil to spare.

    Stated honestly: this seeds the ancestor near the attractor. It does not
    demonstrate that the system finds large plants from arbitrary starting
    values. Gene COUNT and ORDER are unchanged — only ancestral values.

  0.6.0: light-limited ecology, 6 canopy bands with within-band weighting so
         height is a continuous gradient, speed slider, strobe suppression.

  Plant genome UNCHANGED: 39 active + 32 padding = 71 slots, same order.
