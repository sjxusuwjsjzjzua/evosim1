# Strategic audit — 2026-08-11

Brief: answer four strategic questions, do not re-file the five findings in
`AUDIT-FINDINGS.md`. Everything below was recomputed from logs on disk with
`python3`, reading `cfg.ticksPerDay` (480) and each run's own `cfg` block.
Arms were established by diffing each log's cfg against build defaults
(`k_photoCost` 0.004, `maxPlants` 90000, `maxAnimals` 40000), never by runs
agreeing with each other.

Corpus used: the 82 v0.51 cold seeds in `runs/standing-collect/`, of which 45
have ≥4 animal gene snapshots at n≥20 and 31 are alive at their final
snapshot; plus `runs/v052/smoke-7001.json.partial.json` (day ~300, the only
real v0.52 ecology on disk); plus the build itself.

---

## The short answer

**Neither carnivory nor stability is the critical path. Both are symptoms of a
third thing that nobody is working on: the animal population's effective
population size is ~2.** Median `Ne` estimated from neutral-gene variance
across 37 surviving runs is **1.66**, against a median census N of 70 and
peaks of 300-580. At that `Ne`, drift dominates any selection coefficient
below roughly `1/(2Ne)` ≈ 0.25 per generation. The project has spent eleven
versions asking why behaviour genes do not respond to selection, in a
population where **almost no selection coefficient is large enough to be
visible above drift.**

The load-bearing measurement: across 45 runs, evolved `meatAttraction`
(median 0.117, >0.30 in 4/45) is **statistically indistinguishable from
`territoriality`** (median 0.161, >0.30 in 4/45) — a gene with **zero
references anywhere in the simulation** (`grep -c 'AG.territoriality'` = 0)
and an identical gene-table row: same bounds `[0,1]`, same sigma `0.04`, same
founder start `0.10` (`evosim-v0_52_0.html:703` vs `:708`). Paired sign test
across the same 45 runs: lower in 27, higher in 18, **p = 0.23**.

That is the mission test applied to the mission test. `meatAttraction` is not
being purged and it is not being selected. It is invisible.

---

## 0. The measurement, in full

### 0a. Neutral variance collapses in animals and not in plants — CONFIRMED

Mean inert-gene SD (`tag0-2`, `immunity0-3`, `mateChoosiness`,
`pathogenResistance` — all verified 0-reference in the build) at the final
snapshot, as a ratio to the **first** snapshot with live animals:

| kingdom | median final/first inert SD | n |
|---|---|---|
| **animal** | **0.157** | 58 |
| plant | 0.801 | 82 |

38 of 58 animal runs lose ≥75% of neutral variation. Plants — census 10⁴ —
keep 80% of theirs. The collapse is specific to the kingdom where every
unresolved mission pillar lives.

### 0b. `Ne` from mutation–drift balance — CONFIRMED in order of magnitude

For a neutral continuous trait, equilibrium variance `Ve ≈ 2·Ne·Vm` with
`Vm = mutationRate · (sigma·mutationScale)²`. Using each run's own evolved
`mutationRate` and `mutationScale`, and the three `tag` genes (sigma 0.05,
`:686`):

| | value |
|---|---|
| median `Ne` estimate, 37 surviving runs | **1.66** |
| median census N at the same snapshot | 70 |
| median `Ne/N` | **0.030** |
| best case in the corpus (seed 41091, N=283) | Ne 20.7 |
| worst (seed 41181, N=67) | Ne 0.33 |

Treat the absolute number as order-of-magnitude — the estimator assumes
equilibrium and a Brownian step. The *qualitative* claim needs no estimator
and is CONFIRMED directly: inert-gene SD sits at 0.02-0.03 against a founder
0.15, flat for a thousand days, in populations of 100-300.

### 0c. Populations are frozen, and it is visible per-run — CONFIRMED

`runs/standing-collect/seed-41111.json`, inert `tag1` SD by day:

```
day 305  n=173  tag1 sd 0.1482      day  905  n=151  tag1 sd 0.0134
day 605  n= 78  tag1 sd 0.1095      day 1205  n=244  tag1 sd 0.0036
day 705  n= 52  tag1 sd 0.0000  <-- bottleneck   day 1600  n=103  tag1 sd 0.0031
```

Across that same day-605→705 window `meatAttraction` goes 0.117 → **0.000**
and stays there for 900 days, while `carnivory` goes 0.069 → 0.219 and
`territoriality` (inert) goes 0.165 → **0.252**. Every gene moves at once,
including the ones nothing reads, and then all of them stop. That is a
selective sweep of one lineage, not selection on any gene.

`AUDIT-FINDINGS.md` F1 cites seed 41111 as decisive evidence that carnivory is
not emergent ("119,948 attacks on a gene indistinguishable from zero"). The
conclusion holds. The mechanism is not "selection purged it" — it is "one
genome fixed and it happened to carry `meatAttraction ≈ 0`."

### 0d. The corpus's best carnivory result is a founder lottery — CONFIRMED

`runs/standing-collect/seed-41121.json` has the second-highest evolved
`meatAttraction` in the corpus (0.411) and would score a HIT on v0.52's
threshold. Its trajectory, against its matched inert control:

```
day  305  n=308  meatAttraction 0.187   territoriality 0.131   inertSD 0.146
day  405  n= 74  meatAttraction 0.329   territoriality 0.335   inertSD 0.029
day 1600  n=298  meatAttraction 0.411   territoriality 0.322   inertSD 0.029
```

Both genes jump +0.20 in the same 100-day window, at the same bottleneck, and
then freeze for 1200 days. `analyze.py` prints `meatAttraction moved
0.187->0.411` for this run and prints `territoriality moved 0.131->0.322`
eleven lines later, and nothing connects them.

### 0e. F1's control comparison does not survive contact with the gene table — CONFIRMED

F1's decisive argument was: `plantAttraction` evolved to 0.80 while
`meatAttraction` sits at 0.09, in the same genome under the same selection.
But `plantAttraction`'s founder start **is 0.80** (`:702`). Median evolved
value 0.823 — it moved **+0.023 in 1600 days.** Selection did not raise it;
it was initialised there.

Median |Δ from founder start| across 22 `[0,1]` animal genes over 1600 days:
`herbivory` +0.148 (the largest), `territoriality` **+0.082 (inert)**,
`camouflage` +0.065, `immunity3` **−0.072 (inert)**, `carnivory` +0.052,
`meatAttraction` −0.001. **The largest single-gene move in a typical run
belongs to an inert gene** (`tag1` in 7/45 runs, `climbing` 7/45, `immunity0-3`
in 14/45 combined).

F1's *conclusion* — carnivory is not demonstrated emergent — is correct and
should stand. Its *argument* should be replaced, because the replacement is
stronger, free, and already in every log.

---

## Q1. Is carnivory the right thing to be working on?

**No — but "stability" is not the right answer either. CONFIRMED that both are
downstream of the same oscillation; PLAUSIBLE on the direction of causation.**

The stability reading in the brief is correct as far as it goes: 15/15 cold
seeds fail the stationarity gate (`FINDINGS.md:218-226`), 50-70% go extinct
(`FINDINGS.md:207-217`), seed 1337 at 4000 days is still non-stationary with
R0 1.56 → 1.02 on matched in-run windows (`LEDGER.md`, "SCORED: the 4000-day
long-horizon probe … is a MISS"). A carnivore layer on a non-stationary
two-level system will not produce "stable on most seeds".

But look at what the instability *is*, in the runs that survive:

| among 31 surviving runs, last 400 days | value |
|---|---|
| animal population max/min | **median 18.3×** (p75 47×, max 511×) |
| median annual peak N | 251 |
| median annual trough N | **15** |
| runs with a trough ≤ 10 animals | 12/31 |

The world has a 40-day year (`:314`) with a ±35% light swing (`:334`), and
mean animal death age is 24.2 days (`analyze.py` DEMOGRAPHY, seed 41121).
**The forcing period is shorter than the generation time.** The population
cannot average over the cycle, so every year is a bottleneck, and the
bottleneck is what sets `Ne` — `analyze.py:167` already says so in a comment
("Ne is set by the trough, not the mean") without anyone acting on it.

So one mechanism produces all three failures:

```
40-day seasonal forcing, shorter than a generation
        ↓
consumer-resource oscillation, 18× median amplitude, troughs of 1-15
        ↓                                    ↓
50-70% extinction              Ne ≈ 2  →  no gene responds to selection
(the stability failure)            (the emergence failure)
```

It also explains a problem the project has recorded but not diagnosed:
within-cfg seed-to-seed R0 noise of SD 0.25-0.53, making every CFG comparison
4-7× underpowered (`FINDINGS.md:240-247`). At `Ne ≈ 2`, a run's outcome is
mostly determined by which of six founder morphs won the first bottleneck.
**The "seed noise" that has been treated as a statistical nuisance is the
founder lottery, and it is the same finding.**

### What this means for the plan

- **Carnivory is not the wrong problem, but it is currently not a testable
  problem.** No mechanism change to ATTACK can be scored while the gene it is
  scored on behaves like an unread gene. v0.52 is the right kind of change;
  it is being run in a population that cannot answer it.
- **"Stability" as currently framed (raise R0, reduce extinctions) is also not
  the critical path.** It is one of the two outputs. Optimising it directly is
  what produced the `k_photoCost` dose series, which `FINDINGS.md:263-268`
  already flags as "outcome-tuning in a physics costume."
- **The critical path is the amplitude of the oscillation relative to
  generation time.** It is upstream of both, it is a physics question rather
  than an outcome-tuning question, and it has a cheap decisive test.

### The test I would run, with its prediction

Tier B, one CFG patch, no build change. Three arms, same 12 seeds, 1600 days,
shipped full arena:

| arm | cfg | rationale |
|---|---|---|
| control | shipped v0.52 | `daysPerYear` 40, `seasonAmp` 0.35 |
| long-year | `daysPerYear: 120` | forcing period 3× generation time |
| no-season | `seasonAmp: 0.0` | forcing removed entirely |

**Prediction, falsifiable, frozen before the run:**

- **HIT** if, in the two treatment arms, (a) median animal trough N over the
  last 400 days rises above **40** (control median 15), **and** (b) mean
  inert-gene SD at day 1600 is **≥ 0.40×** its first-animal-snapshot value
  (control median 0.157), **and** (c) `meatAttraction` separates from
  `territoriality` in the paired sign test at n≥12 in *either* direction.
  That establishes that the bottleneck, not the ATTACK formula, is what has
  been suppressing gene response — and (c) is the part that makes every
  subsequent emergence test scoreable.
- **MISS** if inert-gene SD ratio stays below 0.25 in both treatment arms.
  Then `Ne` is set by reproductive skew or by spatial structure rather than by
  seasonal bottlenecks, the diagnosis is wrong (rule 3), and the next question
  is which of those it is — **not** a bigger `daysPerYear`.
- **CAN'T-TELL** at n<12 complete blocks per arm, or if the no-season arm's
  extinction rate exceeds 90% (removing winter may change productivity enough
  to be a different world).

Note honestly what this arm is and is not. Changing `daysPerYear` is a change
to the world's physics, in the same class as `k_photoCost` — it does not write
a behaviour into the code, so it does not fail the mission test. But it is a
**diagnostic**, not a proposed ship. If it confirms the diagnosis, the shipped
fix should be whatever lets a population buffer a seasonal cycle *by
evolving* — which is a genuinely open design question and should not be
pre-decided here.

---

## Q2. Decision tree for v0.52, written before the data lands

First, three scoring hazards in the frozen prediction, all fixable now without
amending it, because they add controls rather than move thresholds.

**H1. The frozen HIT threshold has no null attached.** "mean `meatAttraction`
exceeds 0.30" — under v0.51, with the floor ON, `meatAttraction` already
exceeds 0.30 in 4/45 runs (8.9%), and so does the inert `territoriality` in
exactly 4/45. The conjunct with "predation ≥ 20% of animal deaths" does most
of the protective work; the binomial risk of a false HIT from drift alone at
"≥ 6 of 12 seeds" is small — **P = 0.00028 at p = 4/45**. So the threshold is not
*fatally* weak. But it is uninterpretable on its own, and the fix is free:

> **Score `meatAttraction` against `territoriality` in the same run.** Same
> bounds, same sigma, same founder value, zero references in the build. It is
> already logged in every run. Report the paired difference and the sign test
> alongside the absolute threshold. If `meatAttraction` clears 0.30 in half
> the seeds and `territoriality` does too, that is drift and must be reported
> as drift regardless of what the absolute number says.

**H2. Gene means cannot be read from a checkpoint** — already recorded in
`LEDGER.md` (`__buildLog()` does not call `logGenes()`). Restated here only
because the paired-control fix above must also be run on completed logs.

**H3. The floor-off arm changes the selection regime, not just the level.**
With `k_meatAttrFloor = 0.5`, `meatAttraction` contributes ±20% of ATTACK's
attraction term — the floor does not merely supply 84% of the weight (F1), it
**shields the gene from selection**, which is why it reads as neutral. With
the floor at 0, the gene becomes the entire term. So the floor-off arm should
show *more* selection on `meatAttraction` in **either** direction. A result
where floor-off `meatAttraction` moves *down* faster than floor-on is
informative, not a null, and the frozen prediction has nowhere to put it.
Record that branch now.

### The tree

Let **m** = median population-mean `meatAttraction` across surviving
floor-off seeds; **t** = the same run's `territoriality`; **p** = predation
share of animal deaths; **inertSD** = final/first inert-gene SD ratio.

| observed | reading | next move |
|---|---|---|
| **m > 0.30, p ≥ 20% in ≥half, and m − t > 0.15 in ≥⅔ of seeds** | HIT, and it is selection, not drift | Score it. Carnivory passes the mission test for the first time. Then ship `k_meatAttrFloor: 0` as the default via CFG patch and re-baseline. |
| **m > 0.30 but m ≈ t** | drift, not selection | **Not a HIT.** Report as "unresolved — `Ne` too low to distinguish". Go to the Q1 experiment. |
| **m < 0.15, and inertSD < 0.25 (the corpus norm)** | the test never ran | **Not a MISS of the injury diagnosis.** This is the modal outcome and the one to plan for: the population was frozen, so no gene could have moved. Rule 3 does not apply, because the prediction was not actually tested. Go to the Q1 experiment. |
| **m < 0.15 with inertSD > 0.40** | genuine MISS | The population *could* have moved the gene and did not. Injury was not the barrier. Then, and only then, is "this physics cannot support a third trophic level at this productivity" on the table — and even then only after checking the delivery ratio in Q3.1 below. |
| **mean N in floor-off < half floor-on, or `aDeadKilled` > `aDeadStarve` with plant biomass climbing** | OVERSHOOT | Already in the frozen text. Report separately, never as a HIT. |

### When "this physics cannot support a third trophic level" becomes a finding

Concretely, and this is worth stating because it would be a legitimate result
rather than a failure. It requires **all four**:

1. `inertSD > 0.40` — the population is genetically capable of responding.
2. Realized meat delivery ≥ 50% of the ATTACK score's assumed payoff
   (Q3.1) — the perceived and actual returns agree, so [L31] holds.
3. Meat share of animal intake stays **< 2%** across ≥12 seeds at a matched
   1600-day cutoff, with `k_meatAttrFloor = 0`.
4. The energetic budget confirms it: animal intake is **3.08%** of gross
   photosynthesis (seed 41121 ENERGY block). A third level at that base needs
   a carnivore standing crop ~10% of the herbivore one, which is 10-30
   individuals against annual troughs of 15 — i.e. the carnivore niche is
   **thinner than the annual bottleneck**, and a specialist carnivore lineage
   would be expected to go extinct every winter.

Point 4 is the real argument and it is available *now*, before v0.52 lands.
It is also the strongest reason to believe the Q1 experiment matters more than
the Q2 one: **at this productivity and this oscillation amplitude, a
specialist carnivore population is demographically impossible regardless of
how good the ATTACK formula is.** That would be a genuine finding about the
physics — and the way to establish it is to raise the trough, not the floor.

---

## Q3. What v0.52 is likely to get wrong

Ranked by consequence. The brief's three worries are addressed; two of them
are smaller than feared and one is much larger.

### 3.1. All predation payoff now flows through a channel that is ~8% efficient — CONFIRMED, highest consequence

This is the one. v0.52 routes every unit of meat energy through the carrion
path (attack execution `:1943-1958`, SCAVENGE `:1962-1983`; `eFlesh`/
`fleshMass` are 0 by design). Measured in the only
real v0.52 log on disk, `runs/v052/smoke-7001.json.partial.json` at day ~300:

| quantity | value |
|---|---|
| `killMass` (corpse mass created by predation) | **315.07** |
| `carrionMass` (corpse mass actually eaten, all sources) | **90.58** |
| `corpseRot` (corpse mass decayed to detritus) | **988.15** |
| eaten fraction of all corpse mass | **8.4%** |
| `eCarrion` as a share of animal intake | **0.097%** |

Corpses decay at `k_corpseDecay` 0.0008/tick (`:526`), a ~1.7-day 1/e life,
and the only way to eat one is the SCAVENGE branch (`:1962`) whose score is
multiplied by **`carrionAttraction`, bare and unfloored** (`:1749`) — median
evolved value **0.096**, as low as `meatAttraction` and behaving the same way.

So the ATTACK score at `:1774-1783` values a target at the **whole corpse**
(`mvK` = `meatValue·carrionValue·carrionDigest(carn)` = 6.83/mass at founder
carnivory, up from 1.20 in v0.51 — a 5.7× rise in *perceived* return), while
the realized capture is under 10%. **v0.52 raised the perceived payoff ~5.7×
and plausibly lowered the realized payoff, and that is precisely the [L31]
violation the change was written to fix**, moved from the ATTACK branch to the
ATTACK→SCAVENGE handoff.

It is also a two-locus problem. Hunting only pays if `meatAttraction` **and**
`carrionAttraction` are both nonzero. Reproduction is asexual with no
crossover (`:2119` comment, "crossover at phase 5"), and `Ne ≈ 2`. Two loci
that pay only jointly, no recombination, `Ne` of 2 — that adaptation is
effectively unreachable.

The killer not auto-eating is defensible as design (the LEDGER argues it makes
kill-stealing emergent, which is true). The problem is not the choice; it is
that **nothing measures whether the killer ever gets the meal**, and the score
assumes it always does.

*Cheapest correction, and it is a measurement, not a mechanism:* log
`killMass` and `carrionMass` per window and report `carrionMass/killMass` in
`analyze.py`'s TROPHIC section. Both columns already exist (`:3316-3322`). If
that ratio is under ~0.3 in the v0.52 arms, the emergence test is measuring a
delivery failure, not a selection result, and should be scored CAN'T-TELL.

### 3.2. `carrionFloor` is now a hardcoded subsidy on the payoff side — CONFIRMED, mission-test relevant

`carrionDigest(carn) = carrionFloor + (1 − carrionFloor)·carn` (`:1583-1586`),
`carrionFloor = 0.30` (`:530`). Because v0.52 routes all meat through it:

- At `carnivory = 0`, meat is still worth `24 × 0.85 × 0.30 = 6.12` per unit
  mass. In v0.51 it was worth **0** and the `rateA > 1e-12` guard killed the
  ATTACK branch entirely. **The carnivory gate that the v0.52 diagnosis
  identified ("retaliation cancels meat gain below carnivory ≈ 0.031") has not
  been removed — it has been replaced by a constant.**
- The marginal value of `carnivory` is now nearly flat: 0 → 1 buys only 3.3×
  (6.12 → 20.4), and the founder-range move 0.05 → 0.30 buys **1.52×**
  (`carrionDigest` 0.335 → 0.51), against a
  quadratic gut cost `k_gut·(carn² + herb²)`. **v0.52 may make `carnivory`
  itself *less* selectable than v0.51 did**, which is the opposite of the
  intent.

`HANDOFF.md:415-418` (Tier 3, item 10) says exactly this and says to leave it
alone "until something else forces it." v0.52 forced it, without the entry
being revisited. Consequence for scoring: **the `k_meatAttrFloor: 0` arm is
described as "carnivory with no subsidy of any kind" (`LEDGER.md`, v0.52
pre-registration). It is not.** 30% of meat digestion is free at
`carnivory = 0`. That sentence should be corrected before the arm is scored,
or a HIT will be reported under a claim the code does not support.

### 3.3. `threatR` values a threat that no longer exists — CONFIRMED, the brief's worry, and it is real

`:1805-1807`:

```
threatR = k_attack·biteForce_j·p75(omass)·carnivory_j·aggression_j·energyPerMassA
          /(1 + k_armEff·armour_i)
```

Under v0.51 an attack removed prey **mass**, so pricing the threat as
"flesh taken per tick × cost to build mass (55)" was approximately right.
Under v0.52 an attack removes **no mass at all** (`:1953-1955`, "MASS IS
CONSERVED HERE BY DOING NOTHING TO IT"). The victim's real expected loss rate
is `dmgRate/(k_health·mass_i) × (value of its whole life)`.

Two specific errors follow, both of which shrink perceived threat:

1. **`carnivory_j` multiplies the threat, but the damage formula at
   `:1943-1945` contains no `carnivory` term at all.** Under v0.52 *any*
   animal that picks ATTACK does full damage. Median evolved `carnivory` is
   0.102, so prey underestimate threat by ~10×.
2. **`aggression_j` also multiplies it**, and aggression gates nothing in the
   attack execution either — it appears only in the retaliation charge.
   Median 0.219.

Combined, prey perceive roughly **`0.102 × 0.219 ≈ 2.2%`** of the actual
threat rate. Consequences: FLEE is scored ~45× too low against ATTACK, and —
more importantly — **`AN.risk`, the EWMA that gates APPROACH, is fed from
`riskMax` derived from the same `threatR`** (`:1809-1812`, `:1830`). APPROACH
is the *only* mechanism in the build by which grouping pays (`:1815-1822`).

That makes this a candidate answer to the eleven-version herding mystery
(`HANDOFF.md:199-209`, `actAppr` stuck at ~0% of the action budget against a
>1% falsifier): the herding hypothesis has been tested three times against a
risk signal scaled down by a factor of ~45. `HANDOFF.md:371-375` proposes
testing the `AN.risk` EWMA smoothing as the culprit; the magnitude looks like
the larger problem.

I would **not** fix this inside v0.52 — that would be a second structural
change in one version (rule 3). File it as the next candidate after v0.52
scores, and note that it makes v0.52's ecology *harder* to read: under injury
killing, prey that do not flee die, so a mispriced FLEE now costs lives rather
than nibbles.

### 3.4. Things the brief worried about that are smaller than feared

**Sustained hunts are working — CONFIRMED, not a problem.** `dmgDealt` 378.11
against `killMass` 315.07 at `k_health = 1.00` means **83% of damage dealt
converted into kills**; healing at `k_heal` 0.0012 (`:499`, `:2070`) is not
eating hunts. The rise in attacks/kill from 13.0 to 20.2 recorded in the
LEDGER is the expected cost and no more.

**`eFlesh`/`fleshMass` = 0 changes `analyze.py`'s energy section — CONFIRMED,
cosmetic.** The ENERGY block prints "flesh %" and "carrion %" separately;
under v0.52 the first is structurally 0 and the second carries everything. No
statistic is wrong, but a reader comparing a v0.52 digest to a v0.51 one will
read "flesh 0.000%" as predation collapsing. Add a one-line note to the
section, or sum them.

**`AN.dmg` bookkeeping is clean — CONFIRMED.** Reset on founder seeding
(`:1544`, inside `seedAnimalFounders` at `:1520`) and on birth (`:2131`);
corpses cannot be attacked (`ACT_ATTACK` requires `stage === ALIVE`, `:1920`);
both slot-allocation paths reset it. No
leak.

### 3.5. One real defect I did not expect

**`ttk` ignores damage already on the target** (`:1781`). A prey animal at 95%
of its lethal threshold is valued identically to an untouched one, so a hunter
that has invested 19 of 20 contact ticks sees no rising return and the escape
hatches at `:1679-1690` can abandon a nearly-dead target. The fix is one line
— `ttk = (k_health·omass − AN.dmg[j])/dmgRate` — and it is a [L31] correction
of the same class as the ones already made, not a new mechanism. **Do not ship
it inside v0.52**; it would confound the arm currently running. Queue it.

---

## Q4. What is being neglected

Ranked. The first item is, in my judgement, worth more than everything else in
this document combined.

**1. `Ne`. Nobody is working on it, and it gates every remaining mission
pillar.** Detail in §0 and Q1. The instrument that should have caught it
exists and is miscalibrated in two independent ways — see item 2. Every
open item in `HANDOFF.md` §1 "Not achieved" (herding, speciation, effective
population, behavioural monoculture) and the entire carnivory line is
downstream of this one number.

**2. `analyze.py`'s `Ne` meter reports "rising" on the most genetically frozen
run in the corpus — CONFIRMED, and it is the reason item 1 went unseen.**
`sec_ne` (`analyze.py:325-362`) has two defects:

- **Baseline is `snaps[1]`, not `snaps[0]`** (`:348`). On seed 41121 the
  bottleneck lands between snapshot 0 (day 305) and snapshot 1 (day 405), so
  the meter baselines on the collapse. Mean ratio from `snaps[1]`: **1.99,
  printed as "rising"**. From `snaps[0]`: **0.258**.
- **`parentalCare` is averaged in raw.** Its range is `[0, 20000]`; its SD goes
  58.4 → 552.9, ratio **9.47**, which single-handedly drags the mean of ten
  ratios from ~1.15 to 1.99. It is also flagged `PINNED 82% at min` by
  `analyze.py`'s own GENE BOUNDS section in the same digest.

Corpus-wide the two baselines disagree systematically: median ratio **0.53**
from `snaps[1]` versus **0.24** from `snaps[0]`; "FALLING" fires in 33/45 runs
versus 44/45. Fix: baseline on the first snapshot with n≥20, use the **median**
of per-gene ratios, and drop `parentalCare` (or normalise by range). This is
`AUDIT-PROTOCOL.md:139-143`'s own rule — "if an audit produces a finding a
script could have produced, write the script."

**3. Add `territoriality` as the standing neutral control, everywhere.** It is
inert (0 references), `[0,1]`, sigma 0.04, founder start 0.10 — **identical in
every respect to `meatAttraction` and `carrionAttraction` except that nothing
reads it** (`:703`, `:704`, `:708`). It is a matched null for the two genes the
mission hangs on, it is already logged in every run ever produced, and it costs
nothing. `analyze.py` should print `meatAttraction − territoriality` and
`carrionAttraction − territoriality` in the GENE FLAGS section, and no
attraction-gene claim should be made without it again. Note for the docs:
`HANDOFF.md:314-318` lists the inert genes and omits `territoriality`, and
includes `ambushTendency`, which **is** read (`:1724`).

**4. The perturbation statistic.** Confirmed absent — `grep -n 'shock' analyze.py`
returns nothing, while `shockDay`/`shockFraction` are shipped and working
(`:503-508`, `:2208-2217`). This is the right instrument and the reasoning
behind it in the v0.52 LEDGER entry is the best paragraph in the file: every
"stable" metric this project uses is satisfiable by something other than
stability. Two notes before it is used: (a) at `Ne ≈ 2` a cull is also a
genetic bottleneck, so a shock arm measures demographic *and* genetic recovery
together and cannot separate them — run it **after** the Q1 experiment, not
before; (b) the natural annual trough is already a 18× cull, so a shock of
50% is inside the system's normal seasonal range and may show nothing.

**5. Plant-side hardcodes — checked, and I found none. CONFIRMED clean.**
`plantScore` (`:1610-1625`, the return at `:1624`) applies `pa`
(`plantAttraction`) bare with no
additive floor, exactly like GRAZE/SCAVENGE, and germination/allocation are
gene-driven. The ATTACK floor was not part of a pattern. Nothing filed.

**6. Prune or wire the inert genes — but keep four per kingdom.** Nine animal
genes are 0-reference (`territoriality`, `mateChoosiness`, `parentalCare`,
`pathogenResistance`, `immunity0-3`, plus plant `pollenRange`,
`selfingTolerance`). `HANDOFF.md:424-426` already says keep at least four as
the `Ne` meter. Given items 1-3, I would **raise** that: they are now the
project's most valuable instrument, not debt. Do not prune them.

---

## Deliberately not flagged

- **Throughput, Actions saturation, queue sizing.** `AUDIT-PROTOCOL.md:133-138`
  puts it out of scope, and the recent LEDGER entries show the arrival-rate
  arithmetic already corrected.
- **The full-arena dose-series pre-registration** that replaced the voided one.
  It is well-formed, has one metric in one sentence, and carries an explicit
  cap-limited guard. Nothing to add.
- **v0.52's verification** (check.js, matter conservation 0.000000%,
  determinism 40 samples × 100 columns). I re-read the diff and found no
  correctness defect; §3.5 is a design mismatch, not a bug.
- **The `k_health = 1.00` pivot.** Holding time-to-kill identical to v0.51 so
  only payoff structure changes is exactly right and is the cleanest
  application of `HANDOFF.md` §2b in the file.
- **Re-litigating F1-F5.** All five were accepted with correct reasoning;
  §0e sharpens F1's argument rather than disputing its conclusion.
- **Any recommendation to widen a gene bound** (rule 8), compare across
  unmatched cutoffs (rule 7b), or add a build step (rule 9).

---

## Ranked recommendation

| # | action | tier | cost |
|---|---|---|---|
| 1 | Fix `analyze.py:325-362` — baseline `snaps[0]`, median not mean, drop `parentalCare`. Re-digest the 82-seed corpus. | tooling | minutes |
| 2 | Print `meatAttraction − territoriality` and `carrionAttraction − territoriality` in GENE FLAGS; add the paired sign test to the v0.52 scoring sheet **before** the arms land. | tooling | minutes |
| 3 | Print `carrionMass/killMass` per window. If it is <0.3 in the v0.52 arms, score them CAN'T-TELL, not MISS. | tooling | minutes |
| 4 | Correct the v0.52 pre-registration sentence "no subsidy of any kind" — `carrionFloor` 0.30 is a subsidy on the payoff side (§3.2). Do not move a threshold. | LEDGER | minutes |
| 5 | Let the v0.52 arms finish. Score them with 1-3 in place, against the tree in Q2. | — | already running |
| 6 | Fire the `daysPerYear`/`seasonAmp` experiment in Q1 with its frozen prediction. This is the one that decides whether anything else is measurable. | Tier B | 36 jobs |
| 7 | Queue, in order, for after v0.52 scores: `threatR` recurrency (§3.3), `ttk` damage-awareness (§3.5). One per version. | Tier B | — |

**If I had to name one thing you are getting wrong:** the project is testing
mechanisms in a population that cannot respond to them, and has been reading
"the gene did not move" as evidence about the mechanism when it is evidence
about `Ne`. Every diagnosis since v0.39 — the carnivory unblock, the
`socialAttraction` connection fix, the currency unification, and now injury
killing — may well have been correct and unmeasurable for the same reason.
