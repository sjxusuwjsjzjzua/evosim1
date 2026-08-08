# State — v0.36.0

Replaces PROJECT-HANDOFF.md. Everything needed to continue without re-deriving
anything. Process lives in WORKFLOW.md; the spec in DESIGN.md; per-gene
accounting in GENE-LEDGER.md; history in CHANGELOG.md.

---

## 1. Where the build is

**v0.36.0, `formatVersion` 36. Shipped, not run.**
v0.34.0's two carrion changes are STILL untested and are carried forward
untouched again — they cannot be evaluated in a drift-dominated fauna, so they
wait on v0.36 fixing Ne first.

The last runs of record are **three v0.35.0 logs: s4976 (321d), s6147 (690d),
s2661 (2149d)**. Note these violate invariant 12 — different durations — and
s4976 had only 61 unaided days after the reseed net closed on day 260, so it is
uninterpretable and should not have been weighted equally. `analyze.py` now
detects this case.

### What v0.36.0 changed — three structural fixes, no magnitude changes

| change | why |
|---|---|
| adults grow only above `max(matingThreshold·cap, invest+buildE+cap*0.2)`; juveniles keep the old `cap*0.5` gate | **A8.** Growth fired at a strictly lower energy than breeding and, absorbing ~6 energy/tick against a ~0.03 surplus, took the whole surplus. Reproduction needed `room ≤ 0`; mass/size was 0.53–0.75 and never got there. Lifetime output 0.33/1.00/0.33 — R0 < 1 |
| `CFG.biteMassPow` 0.667, split from Kleiber; `k_intake` pivoted 0.013→0.01486 | **A7.** Intake `m^0.75` and `a_mass` upkeep `m^0.75` cancelled exactly, so `size` was metabolically free and ran away in all three seeds. Pivot holds intake constant at founder size so only the shape moved |
| `size` range .2–40 → .5–16 | **A9.** `mutateAnimal` clamps, so a drifting gene walks to its range midpoint — 20.1, from a founder of 5. At harmonic Ne 2–13 that pull beat selection |
| `analyze.py` life-support test rewritten | flagged any cumulative `aReseed` > 200, a false positive on s2661 (223 reseeds, then 1889 unaided days). Now computes the net-off day from cfg and flags only reseeds arriving after it |

**Correction to the previous v0.36 plan.** `photoCost` alone was the standing
recommendation and was an incomplete diagnosis: with `room > 0` permanently
true, extra food converts to body mass, and a bigger body raises `buildE` next
generation. Doubling food still leaves time-to-first-reproduction at ~15 days
against a 14.8-day lifespan. **`photoCost` is now the v0.37 candidate, alone,
after this run is read.**

**World:** 768 × 768 units, 48 × 48 tiles (keep `worldSize/tiles` at 16),
terrain with impassable peaks and deserts. `maxPlants` 90,000,
`maxAnimals` 40,000. No cap has bound in any recent run.

**Genomes:** plant 39 active + 32 padding = 71. Animal 54 active + 31 padding
= 85. Frozen.

### What v0.34.0 changed, and is waiting on a run

| change | why |
|---|---|
| `carrionDigest` = `floor + (1−floor)·carn` instead of `max(carn, floor)` | a clamp made every carnivory below 0.30 worth the same, so the gene carrion exists to bootstrap had no gradient to climb |
| `k_corpseDecay` 0.0025 → 0.0008 | corpse half-life 0.58 → 1.8 sim-days; ~94% of corpse mass was rotting unfound |
| unique lineage names for the life of the run | a name was recycled once a cluster died |
| new `aSeen` column | animal–animal encounters per look — whether any social or predatory gene can have signal at all |

### What v0.35.0 changed

| change | why |
|---|---|
| clusters are **provisional** until they hold `minPop` for `lineageConfirm` (5) passes | 70 plant lineage names in 50 years, 35 of them alive for a single 10-day snapshot; the tree held 240 entries under 107 distinct (name, parent) pairs |
| new `pLocked` column | refuge measured by **biomass** through `accessOf`, not by plant count. `pEscape` read 0.21 while ~95% of standing biomass was unreachable |
| new `aDeadSen` | animals had no senescent bucket; `aDeadAge` read zero for 50 years while 37% of deaths were in the oldest age bin |
| header history moved to CHANGELOG.md | ~1,050 lines re-read on every `view`; the file is 25% smaller and still self-contained |

97 log columns.

---

## 2. What the v0.33 run established

**Verified, and should not be tuned away:**

- 50.5 years, both kingdoms alive at the end. Matter flat at 6819, drift
  0.000000%. No cap ever bound. Effectively no life support — `pReseed` 91,
  `aReseed` 9.
- **The canopy is stratified.** Height histogram closes with all twelve bins
  occupied, 45% of plants above band 0, `height` 6.2% of plant upkeep. Two
  versions earlier it was 97% in band 0.
- **The arms race ran in both directions.** Plant `height` 0.326 → 0.503,
  animal `size` 5.59 → 7.25.
- **Juvenile mortality is solved.** Death-age histogram 37% in the *oldest* bin
  against 84% in bin 0 two versions earlier. `aJuvFrac` 0.48, `aRate` 0.081
  against `aUpkeep` 0.054.
- **The adult canopy is seasonally stable** (biomass 1.44×, adults 1.52×) while
  the seedling cohort swings 3×. That is forest structure.
- **About eight real plant lineages**, persisting for hundreds of days each.
  (Roughly sixty more were clustering artifacts — see v0.35.)

DESIGN §0 lists four things never achieved together. Three are now met: stable
for 30+ years, a self-sustaining grazer population, a stratified canopy. The
fourth, predation running, is not.

**Still wrong:**

1. **Not stationary.** Over the last 1,000 days: plants −6.4% per 100 days,
   LAI −4.8%, biomass −3.7%, animals **+13.1%**. Simultaneously `pHeight` +2.8%
   and `pEscape` +2.9% against `aSize` −1.1%. The plants are pulling away in the
   arms race and the flora is thinning into fewer, taller individuals.
2. **The fauna is drift-dominated.** Harmonic-mean population 126. The proof is
   not the low variance, it is that `parentalCare` (nothing reads it) sits 86%
   at its minimum and `climbing` 71%. An inert gene cannot be pushed to a bound
   by selection.
3. **Carnivory is dead.** 92% at min, `actAttack` 0.0000, carrion 0.175% of
   animal intake.
4. `photoCost` is 59.5% of plant upkeep; the whole fauna lives on 1.245% of
   gross photosynthesis.

Items 2 and 3 are the same problem. See GENE-LEDGER flag A1.

---

## 3. The plan, in order

1. **3 seeds of v0.35.0.** Read `pLocked`, `aSeen` and the lineage section
   first. Question: did the carrion slope give `carnivory` a gradient, and is
   the decline in item 1 above real across seeds or a single-seed trajectory?
2. **v0.36 = `photoCost` alone.** It is the lever on animal Ne and therefore on
   everything in items 2 and 3. Changing it moves the flora, the fauna and the
   arms race at once, so it must be the only change in that version.
3. **Then Phase 4's success test is fair** — the carnivory histogram going
   bimodal unaided. It has been met once, in s6499 under v0.21, and not since.
4. **Then Phase 5.** Note that the plant kingdom is arguably ready now
   (Ne ~14,000, eight real lineages, `pollenRange` / `selfingTolerance` /
   `mateChoosiness` already reserved and dormant) while the animals at Ne 126
   would likely be extinguished by the added cost of finding a mate. Staging sex
   into the flora first is a legitimate option if Ne does not move.

**Do not build ahead of this.** Phase 4 is built and failing.

---

## 3b. The success test for v0.36 — read this before the next run

Run **three seeds at the SAME duration**, at least 600 days so there are 340+
unaided days after the net closes on day 260. `analyze.py` will now say so.

**The gate question: does `parentalCare` come off its bound?** Nothing reads it,
so it can only be pinned by drift. If it is still pinned, Ne is still too low,
every other gene reading in that log is uninterpretable, and the answer is
`photoCost` (v0.37) before anything else.

If Ne has recovered, then in order:

| check | v0.35 baseline | what would count as fixed |
|---|---|---|
| harmonic-mean animals | 2 / 3 / 13 | 3 digits |
| mass/size | 0.62 / 0.53 / 0.75 | approaching 1.0 — adults actually reaching adult size |
| `size` mean | 9.66 / 10.54 / 13.03 from founder 5 | stable, not climbing to the new midpoint of 8.25 |
| lifetime output (births/animal-day × aDeathAge) | 0.33 / 1.00 / 0.33 | > 1 without reseeds |
| aDeathAge vs maturityAge | died before maturity in 2 of 3 | dying after it |
| `aReseed` after day 260 | n/a | zero |

**Watch for the new failure mode this could create.** Adults now refuse to grow
until they can afford a clutch. If `matingThreshold` or `offspringCount` drift
high, adults could stall permanently at sub-adult mass — growth blocked by a
reproduction bar they cannot reach, which is the old bug wearing a hat. The tell
is mass/size FALLING while `size` holds steady. If that appears, the fix is on
`matingThreshold`, not on the gate ordering.

**Do not read the carrion changes in this run.** They have waited two versions
and can wait one more; carnivory cannot be judged until Ne is up.

---

## 4. Rules learned the hard way

These are also in the HTML header as the invariants list. Breaking any of them
has cost at least one run.

1. **A closed matter ledger does not prove a closed energy ledger.** Charge
   `energyPerMass` at every site that creates mass.
2. **Cost must curve up faster than benefit**, or the gene pins to a bound and
   its tradeoff is fictional.
3. **A saturating form beats a clamp.** A clamp leaves a linear ramp below it
   and dead flat ground above.
4. **Every upkeep term scales with mass^0.75** or it is a flat tax on juveniles.
5. **Reserves are denominated in upkeep-days**, not energy or mass.
6. **Check achievable ranges, not just shapes.** A correct mechanism at the
   wrong scale does nothing. This has cost `reach` vs `height`, seed dormancy,
   `rootDepth`, and `k_heightMass` twice.
7. **Never calibrate a constant against a statistic measured in a broken run.**
8. **Whatever caps the population is what does the selecting.**
9. **Competition must be asymmetric** or no organism size is preferred.
10. **Never multiply two gate genes.**
11. **The system is chaotic.** Believe nothing that does not repeat across seeds.
12. **A syntax check is not a correctness check** and a call check is not an
    identifier check.
13. **Founding near the attractor is legitimate but must be stated.**
14. **A metric denominated in mass cannot see a failure of recruitment.**
    `eaten/grown` read a healthy 0.48 while every germinating seedling was being
    eaten. Read `pMature/pGerm` alongside it.
15. **A logging artifact will be read as biology.** Corpses were counted as
    living animals; the reseed net was invisible and made three consecutive
    extinctions look like survival; the lineage tree recorded clusters that
    lived ten days. Check what a column actually counts before believing it.

---

## 4b. Added v0.36

- **Growth must not outbid breeding.** Any allocation gate that fires at a lower
  energy than reproduction takes the entire surplus, because growth absorbs two
  orders of magnitude more per tick than the surplus supplies.
- **A clamped gene range is a selection pressure.** `mutateAnimal` clamps, so a
  drifting gene walks to the MIDDLE of its declared range, not to its founder.
  Check the midpoint of every range. **Only `size` has been audited for this —
  the rest of the animal table has not.**
- **Check that a structural fix is magnitude-neutral at the operating point.**
  Dropping the bite exponent alone would have cut intake 12% at founder mass; it
  had to be pivoted through `k_intake` so only the shape changed.

---

## 5. Reading a log

Run `python3 analyze.py log1.json log2.json log3.json` first, always. It prints
one fixed page per log plus a cross-seed table, with the standing bands built in.

**The columns that diagnose, roughly in order:**

- `caps` — bitfield: 1 plant slots full, 2 animal slots full, 4 seed bank full.
  **Check first.** If a cap binds, the array is doing the selecting and nothing
  else in the log means what it appears to.
- `matter` — must be flat to six decimal places.
- `aReseed` / `pReseed` — life support. A fauna held at the floor by the opening
  net is not a surviving population.
- `pMature` / `pGerm` — recruitment survival. Read *before* `eaten/grown`.
- `pLocked` — the fraction of standing **biomass** out of reach. `pEscape`
  counts plants and is dominated by the seedling cohort.
- `pOcc`, `pPerTile` — whether two plants ever share a tile, which is the
  precondition for shading.
- `aSeen` — animal–animal encounters per look. Under ~0.2, no social or
  predatory gene can be under selection at all.
- `aRate` vs `aUpkeep` — whether eating pays. Equality is a treadmill.
- `deathAgeHistogram` — bin 0 dominant means newborns dying before they feed,
  which is a birth-economics problem, not a foraging one.
- `heightHistogram` — everything in bin 0 means the eight canopy bands are one
  band and layered light is off.
- `sel` in the gene snapshots — selection differential: the mean genome of
  everything that reproduced, minus the population mean. Says which way a gene
  is being pushed *now*.
- **The drift check:** if an inert gene (`parentalCare`, `pollenRange`, the
  immunity block) sits at a bound, the population is too small for selection to
  beat drift and every other gene reading is suspect.

**Habits worth keeping:** always compare `aBorn` against `aDeadStarve` (equality
means a treadmill); always read a per-capita figure alongside a population
figure; and always check whether a column is cumulative or an interval mean
before differencing it.
