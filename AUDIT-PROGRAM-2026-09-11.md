# PROGRAM AUDIT — evosim, 2026-09-11

Adversarial audit of the **program**, per `.claude/skills/program-audit/SKILL.md`.
Premise: guilty until proven exceptional. `HOST-FINDINGS.md` was **not** read.

Every number below was computed by the auditor from the repo during this pass,
not taken from `LEDGER.md`. Scripts were ad-hoc; all are reproducible from
`runs/rot-collect/*.json` + `runs/v53-collect/*.json` (2,341 logs parsed) and
`evosim-v0_55_0.html`. Where a statistic differs from one in `LEDGER.md` or
`PROGRAM-HISTORY.md`, the discrepancy is stated explicitly.

Confidence 1–10 on every finding. Nothing below 4 is written down.
CONFIRMED = verified against data in the repo. PLAUSIBLE = reasoned.
Tags: `[auditor-only]` = I believe the project has not seen this;
`[cross-validated]` = the project has stated something equivalent.

---

## Summary of the verdict

**PIVOT.** The program is not failing at execution — the bookkeeping, the
determinism, the rule discipline and the honesty of the scoring are genuinely
better than most research code ever gets. It is failing at **target selection,
at three separate levels at once**:

1. It has been optimising a **proxy** (`meatAttraction`, `carnivory`, predation
   share of deaths) instead of the thing the mission is about (what fraction of
   animal energy comes from animals). That fraction has been measured by me for
   the first time: **0.26% median, hard-capped at 2.21% across 1,075 healthy
   surviving runs**, and **flat across every structural version**.
2. Three of the five structural versions targeted the `ATTACK` act, which by
   construction **delivers zero energy to the attacker** — all meat energy in
   this model flows through `ACT_SCAVENGE`, gated by `carrionAttraction`, a gene
   that has never been varied, never been a metric, and is not even a CFG
   constant.
3. The decision statistics have standard errors **larger than the pre-registered
   thresholds they are compared against**, so a substantial part of the
   seven-MISS streak is a power artifact rather than a biological result.

And underneath all three: the carnivore niche in this model is **11–20
individuals out of 353**. Not zero. Not dominated. Just far too small to be
evolutionarily visible in the **14–30 generations** a run provides. No amount of
re-pricing the genome fixes an 11-individual niche.

---

# MANDATORY QUESTION 1 — Is the mission reachable in this model at all?

**Answer: the carnivore corner is NOT strictly dominated — it is energetically
superior per unit of handling time — but it is unreachable at the shipped world
scale and run length, because the niche it would occupy is ~3–6% of the animal
population (≈11–20 individuals) and a run is 14–30 generations long.**

All numbers below computed from `runs/rot-collect/*.json`, v0.55 CONTROL arm
(invadeFrac 0, k_mixed 0.018, meatValue 24), matched window days 400–800, n=12,
medians across seeds.

### 1a. The per-unit-mass payoff favours the carnivore — the LEDGER's arithmetic is wrong in the program's disfavour

`LEDGER.md:8095` and `PROGRAM-HISTORY.md:57–66` compare a specialist carnivore's
`24*0.85*0.895 = 18.26` per unit prey mass against a herbivore's
`tissueValue*herb = 17.5` "*before* any plant defence reduces it", and conclude
the two corners are "comparable on intake per unit mass". That comparison uses
a hypothetical for one side and a realized value for neither.

Realized, from the logs (`ePlant / eaten`, `eCarrion / carrionMass`, `eToxin / eaten`):

| quantity | value |
|---|---|
| realized energy per unit **plant** mass ingested | **15.03** |
| toxin loss per unit plant mass ingested | **3.41** |
| realized **net** plant energy per unit mass | **11.62** |
| realized energy per unit **carrion** mass, at the evolved carnivory 0.157 | 8.13 |
| energy per unit carrion mass at carnivory 0.85 | **18.26** |

**A specialist carnivore extracts 1.57× the net energy per unit mass that a
realized herbivore does**, not "comparable". And the handling-rate constants
(`evosim-v0_55_0.html:490` `k_attack: 0.120` vs `:555` `k_intake: 0.01486`)
differ by **8.1×** in the carnivore's favour at equal `biteForce`, before the
grazing path is further divided by `(1 + k_toughBite*tough)` and `accessOf()`.
Per tick spent with food in front of you, meat is worth roughly **an order of
magnitude more than foliage**, against a diet upkeep penalty of 1.63×.

**The carnivore's problem is not metabolism. It is encounter and supply.** This
matters directly: H9 (`k_mixed` → 0) is aimed at the metabolic term, which was
never the binding one.

### 1b. The supply ceiling — computed three ways, all agreeing

Corpse **mass flux** = (`carrionMass` eaten + `corpseRot`) per tick, from the
logs. A carnivore matching a herbivore's realized intake (0.1735 energy per
animal-tick) needs `0.1735 / 18.26 = 0.0095` mass of corpse per tick.

| window | corpse flux (mass/tick) | mean N | carnivores at bare upkeep | at herbivore-equivalent intake | % of N |
|---|---|---|---|---|---|
| 260–320 | 0.0743 | 263 | 12.4 | 8.3 | 3.1–4.7% |
| 320–400 | 0.1242 | 638 | 21.5 | 15.2 | 2.4–3.4% |
| 400–800 | 0.1079 | 353 | 20.1 | 11.3 | 3.2–5.7% |

Cross-check via ecological efficiency: animal assimilation = 353 × 0.1742 × 480
= 29,522 energy/day; animal production = 48.8 mass/day × `energyPerMassA` 55 =
2,684 energy/day → **9.1% ecological efficiency**. That is textbook-realistic.
The ~3–6% carnivore share is therefore **physics, not a bug** — it is what a
second trophic level *should* be.

Cross-check via the corpus: across **1,075 runs alive at day 800 and never below
20 animals in the window**, the heterotrophy fraction
`eCarrion / (ePlant + eCarrion)` has **median 0.26%, p90 0.98%, and a maximum of
2.21%**. No run in the entire 2,309-log corpus with a surviving healthy
population has ever exceeded 2.3%.

### 1c. Why that ceiling makes the mission unreachable — the generation count

This is the number the project has never computed. From `aGen` in the logs:

| arm | generations elapsed, days 400–800 | mean generation at day 800 |
|---|---|---|
| v0.55 CONTROL | 11.6 | **13.9** |
| v0.55 mixed-flat | 12.8 | 17.2 |
| v0.55 invade-carn | 8.8 | 12.5 |
| v0.55 meat-rich | 26.7 | 33.4 |

A 1600-day run is ~30 generations. Mutational input per gene per generation is
`mutationRate × (ASIG × mutationScale)` — evolved `mutationRate` 0.056,
`mutationScale` 1.12, `ASIG[carnivory]` 0.03 (`evosim-v0_55_0.html:696`) → a
per-generation step SD of 0.034 applied 5.6% of the time. Over 14 generations a
lineage accumulates a random-walk SD of **≈0.030 on `carnivory`**. The
displacement from the founder 0.05 to the invader's 0.85 is **0.80 — 27
mutational SDs**. Even under *complete truncation selection on that one gene*,
the mean can move at most about one phenotypic SD per generation (population SD
0.028), i.e. **≈29 generations of maximum-possible selection**, on a trait whose
entire benefit channel is 0.26% of the energy budget.

And the destination population is ~12 individuals. A genetically distinct
asexual morph at N ≈ 12 has an expected drift-loss time of order N generations —
i.e. **the same order as the whole run**.

**Conclusion.** Reachable in principle; unreachable in practice at
`worldSize` 768 / `animalFounders` 650 / N ≈ 353 / 14–30 generations. The three
levers that would change this — **world scale**, **generations per run**, and
**meat encounter rate** — have been touched by **none** of the five structural
versions. Every version so far has adjusted the fitness landscape, which is the
one thing that was never binding.

---

# MANDATORY QUESTION 2 — Rate of progress, in units that matter

**The metric: heterotrophy fraction**, `(eCarrion + eFlesh) / (ePlant + eCarrion
+ eFlesh)` over the matched window — the share of animal-assimilated energy that
came from animal tissue. This *is* the second trophic level, in one number. It
cannot be satisfied by a constant the way predation-share-of-deaths can, it does
not depend on a gene threshold, and a converging project makes it go up.

Computed across the entire corpus (matched window days 400–800, medians):

| arm | n | heterotrophy % | evolved `carnivory` |
|---|---|---|---|
| **pre-v0.53 (the whole earlier project)** | 1577 | **0.350** | 0.080 |
| v0.53 CONTROL | 83 | 0.473 | 0.079 |
| v0.53 halfseason | 89 | 0.318 | 0.092 |
| v0.53 seasonless | 91 | 0.321 | 0.070 |
| v0.53 seasonless-flooroff | 81 | 0.305 | 0.088 |
| v0.54 CONTROL | 63 | 0.375 | 0.065 |
| v0.54 beta-hi | 60 | 0.384 | 0.072 |
| v0.54 flooroff | 52 | 0.245 | 0.070 |
| **v0.54 meat-rich (`meatValue` 24→40)** | 56 | **0.908** | 0.106 |
| v0.55 CONTROL | 12 | 0.443 | 0.157 |
| v0.55 invade-carn | 15 | 0.430 | 0.068 |
| v0.55 mixed-flat (`k_mixed`=0) | 14 | 0.542 | 0.105 |
| **v0.55 meat-rich** | 16 | **0.963** | 0.054 |

**This is a circling project, and the table says so in one line.** Across five
structural versions, 34 days, 2,341 runs and ~2.6 million simulated days, the
mission metric went from **0.350% to 0.443%** — inside the seed-to-seed spread.
The *only* intervention that ever moved it is **doubling a constant**
(`meatValue` 24→40, +2.4×, replicated in two independent builds) — which is the
mission test failing in its purest form: **the size of the second trophic level
in this simulator is a linear readout of a number in the source.**

Cost of that non-movement, by cfg-diff topic (sim-days, 2,341 logs):

| topic | runs | sim-days | % of all compute |
|---|---|---|---|
| **seasonality** (`seasonAmp` / `daysPerYear` / `k_seasonPhen`) | 1180 | 1,244,770 | **48.1%** |
| plant productivity (`k_photoCost`) | 397 | 524,450 | 20.3% |
| other / array caps / pure control | 442 | 489,035 | 18.9% |
| **trophic / carnivory** (`k_meatAttrFloor`, `meatValue`, `k_mixed`, `invadeFrac`) | 262 | 264,240 | **10.2%** |
| choice rule (`k_choiceBeta`) | 60 | 66,250 | 2.6% |

**Half the compute went to seasonality**, a line whose terminal result (H1
FORCED, `LEDGER.md:7400`) was that the oscillation was the calendar — a correct
and valuable deflation, but a deflation. **One tenth went to the stated
mission.**

---

# FINDINGS, ranked by what it costs to be wrong about them

## F1 — The mission has never had a metric, and the proxies in use can read "healthy" while the trophic level does not exist
**Confidence 9 · CONFIRMED · `[auditor-only]`**

`PROGRAM-HISTORY.md:26–37` and every weekly pass report **"predation share of
deaths" 54–65%** as the trophic headline. In the same runs, meat is **0.44% of
animal energy intake** and **67.5% of all corpse mass rots uneaten**
(`carrionMass` eaten 0.0330 vs `corpseRot` 0.0686 mass/tick, v0.55 CONTROL,
n=12). There are **169 standing corpses against 353 live animals**, mean corpse
residence 841 ticks ≈ exactly the `k_corpseDecay` half-life — corpses are dying
of old age, not being found.

So the project's headline predation statistic is measuring **animals killing
each other and walking away from the bodies.** It can read 62% in a world with
no functioning second trophic level, and it has.

**Material consequence.** Every pre-registered criterion that scores on
predation share (H7's 30% line, H9's "predation share ≥ 45%") is scoring a
quantity that is not the mission. Replace it with heterotrophy fraction and the
corpse-consumed fraction, both computable from columns already logged
(`ePlant`, `eCarrion`, `carrionMass`, `corpseRot`) with no build change.

## F2 — Three of five structural versions targeted an act that delivers zero energy to the actor
**Confidence 9 · CONFIRMED · `[auditor-only]`**

Read the code path:

- `evosim-v0_55_0.html:1985–2009` — `ACT_ATTACK` deposits `AN.dmg[tgt] += dmg`,
  charges the attacker retaliation, and on death calls `killAnimal(tgt)`. **It
  transfers no energy and no mass to the attacker.** The comment at :2002 says so
  explicitly ("MASS IS CONSERVED HERE BY DOING NOTHING TO IT").
- `evosim-v0_55_0.html:2011–2031` — `ACT_SCAVENGE` is the **only** path by which
  an animal gains energy from flesh (`AN.energy[i] += gainE`, `:2025`).
- The corpse is left on the tile as a **public good**. `carrionDigest()`
  (`:1619`) has `carrionFloor: 0.30` (`:550`), so an animal with `carnivory` 0
  still extracts 30% of the meat value. The killer has no priority.

Therefore: **`meatAttraction` and `k_meatAttrFloor` gate an act that cannot feed
anyone.** The gene that gates 100% of meat energy is `carrionAttraction`
(`:1794`).

Now look at where the program went. v0.50 removed the `0.5+` floor on ATTACK.
v0.52 rebuilt ATTACK's payoff model. v0.54's H7 was "the mission test: does
carnivory survive `k_meatAttrFloor` 0". `k_meatAttrFloor` has 155 runs against
it. **`carrionAttraction` has zero runs, zero pre-registrations, is named in no
hypothesis, and is not a CFG constant** — it lives in the gene table at
`evosim-v0_55_0.html:724`, so rule 6 (constants ship as CFG patches) cannot even
reach it.

Worse, ATTACK's *perceived* value (`:1820–1845`) prices the target at
`omass * meatValue * carrionValue * carrionDigest(carn)` — the **whole corpse at
the attacker's own digestion** — which is precisely the assumption the code does
not honour. `[L31]`/`[L47-2]` exist to keep perception and payoff in agreement;
here they are out of agreement by roughly the reciprocal of the 32.5%
corpse-consumed fraction.

**Material consequence.** The next carnivory experiment should be on
`carrionAttraction` and on kill possession, not on `meatAttraction`. Concretely:
(a) raise the founder `carrionAttraction` from 0.10 toward `plantAttraction`'s
0.80 and see whether selection puts it back (if it does, the monoculture is a
real attractor and the mission question is answered; if it does not, the
monoculture was a founder artifact); (b) give the killer temporary possession of
its kill, which is the one change that would make `carnivory` and
`meatAttraction` actually correlate with energy.

## F3 — The herbivore monoculture is written into the founder genome, and the founder genome has never been varied
**Confidence 9 · CONFIRMED · `[auditor-only]`**

`evosim-v0_55_0.html:722–724`:

```
['plantAttraction',    0, 1, .04, .80 ],
['meatAttraction',     0, 1, .04, .10 ],
['carrionAttraction',  0, 1, .04, .10 ],
```

`plantAttraction` starts **8× higher** than either meat gene. These scores enter
the Luce arbiter linearly and are then raised to `k_choiceBeta` = 4
(`:1729`, `:1794–1796`, `:1845–1846`), so an 8:1 founder ratio is a **4096:1 weight ratio**
before any biology happens. The founder spread is `ASIG` 0.04 × (morphSpread,
`founderNoise` 0.8) — i.e. all 650 founders sit within ~0.1 of 0.10. It is a
point founder.

Back out the intrinsic merit from the data. `aSeen` = 0.61 animal detections per
think (`:1883`), of which corpses are 169/(353+169) = 32% → ≈0.20 corpse
detections per decision. `SCAVENGE` is 0.265% of acts. So
`P(scavenge | corpse detected) ≈ 1.3%`. Under `P ∝ score⁴` against ~8 detected
plants, that implies `s_corpse / s_plant ≈ 0.57`. Dividing out the attraction
ratio (`carrionAttraction` 0.17 / `plantAttraction` 0.76 = 0.22) leaves the
**intrinsic MVT rate of a detected corpse at ≈2.6× that of a detected plant.**
The corpse is the better meal by a factor of 2.6 and loses anyway, entirely
because of a founder value.

This is also **self-sealing**, and it is exactly the trap H4 diagnosed and then
walked away from. H4 concluded "the acts they weight barely matter to fitness"
(`LEDGER.md:7818`). True — but the act share is itself set by the founder value,
so the gene cannot rise because the act is rare, and the act is rare because the
gene is low. The project treated an initial condition as a result.

**Material consequence.** In 2,341 runs the project has explored exactly **one
founder genome**. Every evolutionary conclusion it holds is conditional on that
point. A founder-value sensitivity pass — randomise the four attraction genes
uniformly on [0,1] at founding, or just set `carrionAttraction` START to 0.80 —
is one edit, satisfies the mission test in both directions, and is the single
highest-information experiment available.

## F4 — The v0.55 invasion probe is dosed 8–20× the niche it is testing for, and the program has pre-committed to redirect on its result
**Confidence 8 · CONFIRMED (arithmetic) / PLAUSIBLE (inference) · `[auditor-only]`**

`cfg-patches/invade-carn.json` sets `invadeFrac` 0.25 against `animalFounders`
650 (`evosim-v0_55_0.html:429`) → **≈162 seeded carnivores**. From §1b the
carnivore niche in that window (days 260–320) is **8–12 individuals.**

The probe therefore does not ask "can a carnivore lineage persist?" It asks "can
162 carnivores coexist on a resource that supports 12?" — to which the answer is
no, regardless of whether a carnivore peak exists. That is a classic
propagule-overload resource crash, and it is consistent with every observation
the project has: invaders gone by day 305 (`LEDGER.md:8070`), and
`invade-carn` mean N **168 vs CONTROL 316** (`LEDGER.md:8075`) — seeding
carnivores halves the whole population, which is what an overload looks like.

The stakes are the highest in the repo. `LEDGER.md:7940–7944` pre-commits: *"If
lineages handed a working carnivore genotype are purged anyway, then no
valley-crossing mechanism is worth building and the far peak has to be
constructed before it can be reached."* A confounded NO-PEAK reading redirects
the whole program.

Two secondary defects in the same probe, both CONFIRMED:

- **It can only fire at founding.** `seedAnimalFounders()` is called at
  `day === CFG.animalStartDay` (`:2247`) and inside the reseed net which closes
  at `animalStartDay + animalReseedDays` = day 320 (`:2268`, `:432`). A carnivore
  niche is a property of a *mature* ecosystem; the probe can never inject into
  one. The `shockDay` hook at `:2256` is the in-house precedent for a mid-run
  intervention, and is itself inert and unused in all 2,341 logs.
- **`invadeFrac` 0.25 and the alternative are not the same experiment.** An arm
  at `invadeFrac` ≈ 0.02 (≈13 invaders, at capacity) costs one CFG number and no
  build change, and is the version of H8 that can actually answer H8.

## F5 — Decision thresholds are smaller than the standard error of the statistics they gate; the MISS streak is substantially a power artifact
**Confidence 8 · CONFIRMED · `[auditor-only]`**

**H4.** Its frozen rule is "MISS if either gene stays below 0.15 SD". I
recomputed the per-run selection response (first animal gene snapshot → last
snapshot in window, normalised by the population SD) for the v0.54 CONTROL arm,
n=61 — nearly double the n=32 H4 was actually scored on — and bootstrapped the
median (2,000 resamples):

| gene | median Δ (SD) | IQR | **bootstrap SE of the median** |
|---|---|---|---|
| `plantAttraction` | +0.127 | 1.94 | **0.222** |
| `carnivory` | +0.230 | 1.69 | 0.184 |
| `carrionAttraction` | +0.228 | 2.11 | 0.189 |
| `meatAttraction` | −0.367 | 1.60 | 0.118 |
| `territoriality` *(declared neutral)* | −0.023 | 1.81 | 0.131 |
| `mateChoosiness` *(declared neutral)* | −0.334 | 2.46 | 0.246 |

**The SE on the `plantAttraction` statistic (0.222 SD) is 1.5× H4's entire
decision threshold (0.15 SD).** H4's MISS is a coin flip. Note also that the
declared-neutral `mateChoosiness` moved −0.334 SD — *further than
`plantAttraction`* — which is why the "payoff genes move 10–25× further than
attraction genes" claim needs re-derivation before it is quoted again.

**H10.** Its rule is "CONFIRMED if survival exceeds the matched CONTROL by ≥ 15
points at n ≥ 25 with Fisher p < 0.05". I computed the exact Fisher power by
enumeration:

| design | true effect | power |
|---|---|---|
| n=25/arm | 0.667 → 0.817 (H10's own 15-point line) | **0.14** |
| n=25/arm | 0.667 → 0.922 (the v0.54 effect being replicated) | 0.50 |
| n=40/arm | 0.667 → 0.922 | 0.77 |
| n=60/arm | 0.667 → 0.922 | 0.92 |

**H10 has a 14% chance of confirming its own stated effect size, and a 50%
chance of confirming the effect it was written to replicate.** It is set up to
produce another MISS. `n ≥ 60` is the honest gate; the project already knows how
to do this arithmetic — it did it for R0 at `LEDGER.md:2466–2494` — and did not
apply it here.

**Material consequence.** Recompute the n-gate for H8/H9/H10 before scoring
them, and hold H10 at n ≥ 60 rather than 25. Roughly half a dozen of the seven
misses deserve re-reading as "underpowered", which changes what is believed
about the mechanisms, not just about the runs.

## F6 — The "neutral-gene drift yardstick" includes a gene the simulator reads
**Confidence 8 · CONFIRMED · `[auditor-only]`**

`PROGRAM-HISTORY.md:44` and `tools/score55.py:NEUT` define the yardstick from
five genes "the sim never reads": `territoriality`, `ambushTendency`,
`mateChoosiness`, `parentalCare`, `pathogenResistance`.

`ambushTendency` **is** read — `evosim-v0_55_0.html:1769`:

```js
const still = AN.sp[j] < 0.02 ? G[og+AG.ambushTendency] : 0;
```

It feeds `hide` in the detection roll on the next line, so it is under direct
viability selection (be harder to see when stationary). Measured: in the v0.55
arms its Δ is **+0.67 / +0.76 / +0.25 SD** — the largest-magnitude member of the
"neutral" set in two of four arms. Including it **inflates the yardstick**, and
an inflated yardstick biases every H4-style test **toward MISS**.

Separately, the yardstick is not a constant. Recomputed per arm as the median
|Δ| of the five declared-neutral genes: **v0.54 CONTROL 0.07 SD, v0.55 CONTROL
0.50 SD, v0.55 invade-carn 0.65 SD, v0.55 mixed-flat 0.41 SD, v0.55 meat-rich
0.25 SD** — a 9-fold range, scaling with arm n and with population size. The
single value **0.059 SD** quoted as a project-wide constant in
`PROGRAM-HISTORY.md:44` is a v0.54-CONTROL-specific number and is **not portable
to the v0.55 arms it is about to be used on.**

**Material consequence.** Drop `ambushTendency` from `NEUT` in
`tools/score55.py`; compute the yardstick within each arm, not once; re-score
H4 against the corrected yardstick before citing it again.

## F7 — Two headline claims in `PROGRAM-HISTORY.md` are false against the project's own corpus
**Confidence 8 · CONFIRMED · `[auditor-only]`**

`PROGRAM-HISTORY.md:39–42`: *"`carnivory` has never exceeded 0.16 in any arm of
any build. **GRAZE has never fallen below 93%.** `meatAttraction` has never left
its 0.10 founder value by more than the neutral-gene drift yardstick."*

**Claim 2 is false.** Over the 1,075 runs alive at day 800 that never dropped
below 20 animals in the window, GRAZE share of acts (days 400–800):

| | value |
|---|---|
| median | 97.07% |
| p10 | 92.54% |
| p05 | 90.13% |
| **minimum** | **78.32%** |
| runs below 95% | 269 (25.0%) |
| runs below 93% | **126 (11.7%)** |
| runs below 90% | 52 (4.8%) |

**The monoculture breaks in roughly one healthy run in eight, and nobody has
ever opened one.** `runs/rot-collect/50381.json` (seed 50381, v0.53-era defaults,
`daysPerYear` 120): GRAZE **79.5%**, SCAVENGE 2.45%, ATTACK 2.97%, APPROACH
1.92%, mean N 686, heterotrophy 1.91%, evolved `socialAttraction` 0.451 with a
population SD of **0.143** — 3.4× the neutral spread, i.e. a real polymorphism in
sociality. `runs/rot-collect/59400.json` (v0.54 meat-rich): GRAZE **86.0%**,
SCAVENGE 2.50%, ATTACK 3.29%, **APPROACH 3.95%**, `maxSpeed` 1.85 against the
control's 0.58, `biteForce` 2.93, `aggression` 0.31, `armour` up, `size` 6.6,
**66% of corpse mass consumed** against the control's 32.5%. That is a faster,
bigger-biting, more aggressive, more armoured, herding animal eating twice as
much meat — an arms race, one of the mission's named targets — inside an arm
that was scored MISS on its median.

**Claim 3 is false in v0.55.** Computed the same way in the same units as H4, the
v0.55 CONTROL arm shows `meatAttraction` **+1.65 SD** and `carnivory` **+1.66
SD**, against an in-arm neutral median of 0.50 SD. At n=12 this is suggestive
rather than decisive, but "has never left its founder value by more than drift"
is not what the data now says, and it is the sentence the whole redirect rests on.

**Material consequence, and this is the real one.** The analysis unit is wrong.
Every statistic in this project is an arm median over seeds, and **the phenomenon
of interest is a minority state that occurs in ~12% of runs.** H5's frozen rule
("MISS if GRAZE ≥ 96%") applied to an arm median is a test of the median seed,
and the median seed is by construction the one where nothing happened. Score the
*tail*: "fraction of surviving runs with GRAZE < 90%" would have been a live,
moving, mission-relevant number from day one.

## F8 — The H8 instrument fails silently in 8.5% of runs
**Confidence 7 · CONFIRMED · `[auditor-only]`**

H8's decision statistic is the share of animals above `carnivory` 0.5 in the
day-800 carnivory histogram (`tools/score55.py`, `carnHi`). `CARNHIST` is filled
inside `collectStats()` (`evosim-v0_55_0.html:3412, :3435`) and snapshotted by
`logGenes()` (`:3588`).

Of 1,965 runs with a mean in-window population ≥ 50, **167 (8.5%) return an
all-zero histogram at the last in-window sample**, and the histogram total is a
median 0.878× the population. With arms at n=10 survivors, roughly one "0.00%
above carnivory 0.5" reading per arm is an empty instrument rather than an
absence of carnivores. The current preliminary H8 reading is *"0.00% in 10 of
10 survivors"* (`LEDGER.md:8050`) — that number needs a non-empty-histogram
filter before it is scored, or H8 inherits an 8.5% silent-failure rate on the
statistic that redirects the program.

Related and cheap to fix: gene/histogram snapshots are decimated when
`LOG.gene` exceeds `geneCap` (`:3582–3586`) but `LOG.carn`, `LOG.hgt` and
`LOG.dage` are **not** decimated in the same block, so the series drift out of
alignment in length (they remain safe to read by `t`, which `score55.py` does).
Sparse sampling is the bigger issue: a 715-day run carries **9 gene snapshots**,
so every gene statistic in every hypothesis rests on a single coarse sample near
day 700.

## F9 — 139 of 150 constants have never been varied; the process forbids the design that would find which ones matter
**Confidence 8 · CONFIRMED · `[auditor-only]`**

Parsing the `CFG` block of `evosim-v0_55_0.html` gives **150 numeric constants**.
Diffing every logged `cfg` against them across 2,341 logs:

**Constants ever varied from default, entire project: 11.**
`seasonAmp` (780 runs), `daysPerYear` (495), `k_photoCost` (397),
`k_seasonPhen` (287), `k_meatAttrFloor` (155), `maxPlants`/`maxAnimals` (114),
`meatValue` (76), `k_choiceBeta` (60), `invadeFrac` (16), `k_mixed` (15).

**Distinct configurations ever run: 12.** Never touched, among many others:
`carrionFloor`, `carrionValue`, `k_gut`, `k_digest`, `mixedFree`, `k_attack`,
`k_retal`, `k_health`, `k_armEff`, `k_confusion`, `senseCap`, `k_corpseDecay`,
`corpseMin`, `worldSize`, `animalFounders`, `maturityMassFrac`, `energyPerMassA`,
`shockDay`. Several of those are direct levers on §1's three binding
constraints.

The cause is structural, and it is the answer to mandatory question 5. Hard
rule 1 requires a written falsifiable prediction per **run**, and the Tier A/B
section governs per-**run** firing. A screening design — a fractional factorial
or Latin hypercube over the ~15 constants that plausibly gate heterotrophy — has
a perfectly good falsifiable pre-registration at the *design* level (*"no
single-constant perturbation within these ranges raises median heterotrophy
above 2%"*), but no natural per-arm one. So the rule that stopped the
fabrications also quietly banned the one design that explores 139 unexplored
dimensions, and the project has spent 34 days doing depth-first search down a
corridor 11 wide.

**This does not mean drop rule 1.** It means amend it: *a pre-registered
screening batch is one prediction, not N.*

## F10 — The `headless.js` tooling cannot use the founder pool, so the deepest evolutionary history ever explored is 30 generations
**Confidence 7 · CONFIRMED · `[auditor-only]`**

`[L37-3]` (`LEDGER.md:44`) and `HANDOFF.md:685` document "Export founder pool":
`POOL.animal` makes `seedAnimalFounders()` draw from **evolved** genomes instead
of random morphs around `START` (`evosim-v0_55_0.html:1542–1549`). It is the
mechanism that would let runs be **chained**.

`grep -i pool headless.js` returns **nothing**. The pool has never been used in
any of the 2,341 automated runs.

So the project's compute profile is: 2,341 *independent* 14-to-30-generation
histories from one naive genome. Ten chained 800-day runs would give **~140
generations** — five times deeper than anything ever run — at 1/200th of the
compute already spent, and it directly attacks the binding constraint identified
in §1c. Wiring `--pool` into `headless.js` is a tooling change, not a build
change, and does not touch the single-file browser build (rule 9 safe).

## F11 — 2,309 logs have never had a cross-run analysis run on them; the "unexplained 70% survival ceiling" has a strong answer sitting in them
**Confidence 7 · CONFIRMED · `[auditor-only]`**

Every analysis in this project is *arm mean vs arm mean*. No regression, no
correlation, no tail analysis has ever been run across seeds. I ran one screen:
mean of each logged column over **days 200–400** (strictly before the outcome),
against survival to day 800, restricted to `meatValue` 24 arms of v0.54/v0.55,
n=191, 132 survivors. Point-biserial correlations:

| early predictor (days 200–400) | r_pb | mean if alive | mean if dead |
|---|---|---|---|
| `aAge` (mean animal age, days) | **+0.45** | 11.27 | 8.09 |
| `aFeedFrac` | +0.38 | 0.500 | 0.452 |
| **cv of N in the window** | **−0.37** | 114.2 | 153.7 |
| `aAccess` | +0.32 | 0.574 | 0.524 |
| `aDeathAge` | +0.32 | 8.74 | 6.36 |
| `aMature` | −0.28 | 58.1 | 93.7 |
| **`animals` (population size!)** | **−0.26** | 305 | 452 |

**Higher early population predicts extinction.** Short-lived, fast-turnover,
high-amplitude populations die; long-lived, steady, well-fed ones survive. That
is an overshoot-and-crash signature and it is the most plausible account of the
~70% survival ceiling that `HANDOFF.md §0.4` records as "unexplained" after H2
was scored MISS. H2 tested **trough depth in the second half**; the signal is
**overshoot amplitude in the first half**. The data to score that was already on
disk when H2 was written.

Corroborating and counterintuitive: generation turnover over days 200–400
predicts survival **negatively and non-monotonically** (top tercile 46% survival
vs middle tercile 86%, n=191, `meatValue` 24 only) — which falsifies the obvious
"meat-rich survived because it bred faster" story, since meat-rich has both the
highest turnover *and* the best survival. That arm is escaping a strong
population-wide relationship, which is a much more interesting fact about it than
the survival number itself, and it is unreported.

## F12 — Cross-version comparison of mission metrics is invalid, and `PROGRAM-HISTORY.md`'s central table does exactly that
**Confidence 6 · CONFIRMED · `[cross-validated with rule 7b in spirit]`**

v0.54 CONTROL and v0.55 CONTROL run **bit-identical code at defaults** — the
project verified this itself under rule 7 (`LEDGER.md:7905–7931`). Their mean
evolved `carnivory` over the identical matched window:

| arm | n | mean `carnivory` | SD |
|---|---|---|---|
| v0.54 CONTROL | 61 | 0.0905 | 0.072 |
| v0.55 CONTROL | 12 | 0.1547 | 0.066 |

**Welch t = 3.02** (p ≈ 0.005) between two arms with **no treatment and no code
difference**. Whatever the cause — sequential rotation blocks, completion-order
bias at n=12, the log-decimation sampling — the block-to-block offset on the
project's headline mission metric is **0.064**, which straddles H9's MISS line
(0.12) and is larger than most treatment effects ever reported.

`PROGRAM-HISTORY.md:26–37` presents a table with rows "v0.53 CONTROL / v0.54
CONTROL / v0.55 CONTROL" and columns `carnivory` (0.072 / 0.061 / 0.157) and
invites exactly the comparison that number forbids. Rule 7b already bans
comparing trailing-window statistics across run lengths; the same argument
applies to comparing them across rotation blocks, and it is not yet written down.

## F13 — Reverting `k_choiceBeta` to argmax is not the neutral cleanup it is recorded as
**Confidence 6 · PLAUSIBLE · `[auditor-only]`**

`HANDOFF.md §0.3` records the standing decision: if v0.55 gives the Luce rule no
reason to exist, the arbiter reverts to argmax in v0.56, filed as removing an
unvalidated mechanism.

From the numbers in F3: a detected corpse scores ≈0.57× a detected plant after
the founder attraction ratio is applied. Under **Luce**, that corpse still wins
`0.57⁴ / (0.57⁴ + 8) ≈ 1.3%` of the time — which is where essentially all of the
0.265% SCAVENGE share and therefore **all of the meat energy** in this model
comes from. Under **argmax**, a candidate that scores below the best plant wins
**never**.

So the revert is predicted to **reduce heterotrophy fraction toward zero**, not
leave it unchanged. That is a clean, falsifiable, free prediction to attach to
the revert decision — and if it holds, it is itself a mission-test result:
*the only reason any meat is eaten in this simulator is a stochastic tie-break*.

---

# MANDATORY QUESTION 3 — What should be abandoned?

Four things, in order of how much effort they are consuming.

1. **The `meatAttraction` / `k_meatAttrFloor` / ATTACK line — abandon entirely.**
   Per F2 the act it governs delivers no energy. 155 runs and three of five
   structural versions have been spent on it. H7 ("the mission test") tests
   whether a subsidy on a non-feeding act is load-bearing; whatever the answer,
   it is not about carnivory. Redirect that effort to `carrionAttraction` and to
   kill possession.

2. **Seasonality — abandon; it is already finished and still consuming 48% of
   compute.** H1 FORCED settled it (`LEDGER.md:7400`): the cycles are the
   calendar, there is no Lotka–Volterra loop, and the seasonless arm has the best
   survival of any arm ever run. 1,180 runs and 1.24M sim-days are still
   allocated to `seasonAmp`/`daysPerYear`/`k_seasonPhen` variation. Nothing
   further is pending on it. Reallocate the rotation.

3. **Arm-median-only analysis — abandon as the sole unit.** Per F7 the mission's
   target behaviours occur in ~12% of healthy runs and the reporting pipeline
   erases them. Every frozen criterion that compares an arm median to a fixed
   number should be paired with a tail statistic.

4. **Shipping a new HTML mechanism per hypothesis — abandon for now.** Five
   structural versions, one informative result (H1), seven MISSes. Each costs a
   version bump, a rule-7 identity check, a build in the tree, and a week of
   rotation. Per F9 the alternative — a screening pass over the 139 untouched
   constants — has not been tried once.

**Not abandoned, explicitly:** the pre-registration discipline, the matched
window, the censoring rule, rule 7b, rule 8, rule 9, the determinism, and the
practice of writing down rejected reasons. These are why this audit could be
done at all; almost no project can be audited this hard because almost none
records enough to be caught.

---

# MANDATORY QUESTION 4 — Simplicity counterfactual

**The shorter path, concretely:** on day one, `ePlant` / `eCarrion` /
`carrionMass` / `corpseRot` / `aGen` were already being logged. Four lines of
Python over the existing corpus produce (a) heterotrophy = 0.35%, (b) corpse
consumed = 32.5%, (c) carnivore carrying capacity = 3–6% of N, (d) generations
per run = 14. Those four numbers together say: *the second trophic level is
2% of energy at most, the niche is a dozen animals, and a run is fourteen
generations — so scale and duration are binding, not the fitness landscape.*
**Every one of v0.52, v0.53, v0.54 and v0.55 is downstream of not having
computed them.** No new instrumentation, no new build, no new mechanism was
needed — the project had the data and was looking at a different column.

**Mechanisms now in the build that no measurement justifies — count: 4.**

| mechanism | status |
|---|---|
| `k_choiceBeta` Luce arbiter (v0.54) | motivating diagnosis falsified (H4); no measurable benefit (H5 MISS, H7 unchanged, p=0.69); costs one `rng()` per candidate. **Already on the project's own books as debt** — `[cross-validated]`. But see F13: removing it is not free. |
| `k_seasonPhen` (v0.53) | its own result (H1 FORCED) says the mechanism it switches is a pure forcing term with no ecological role, and switching it **off** improves survival. Kept as a switch for an arm nobody needs any more. |
| `shockDay` / `shockFraction` (`:517–522`, `:2248–2266`) | never set to non-zero in **any** of 2,341 logs. Built for a restoring-force test that was never run. |
| `invadeFrac` / `invadeGenes` (v0.55) | as dosed and as gated to founding-only, cannot answer its own question (F4). Salvageable with a CFG change plus a mid-run hook. |

Config surfaces: **150 constants, 11 ever varied.** The build's surface area is
not the problem; the *unused* surface area is 93% of it.

---

# MANDATORY QUESTION 5 — Is the process itself the bottleneck?

**Yes, in one specific and fixable way, and no in general.**

The rules are not why the mission hasn't moved — F1/F2/F3 are, and those are
target-selection errors that would have happened under any process. But two
rule interactions are actively slowing the fix:

1. **Per-run pre-registration forbids screening (F9).** Rule 1's unit is the
   run. A design that perturbs 15 constants one at a time has one honest
   falsifiable prediction total, not 15, and the current reading of rule 1 has no
   slot for it. Result: 139 of 150 constants unexplored after 34 days of free
   compute. **Amendment to propose:** *a pre-registered screening batch is one
   prediction covering the batch, with the decision rule stated as a family-wise
   criterion before firing.* This keeps the property that matters (the claim is
   frozen before the data) and drops the property that doesn't (one claim per
   process).

2. **The n-gate is being enforced without a power calculation behind it
   (F5).** The 2026-09-11 weekly pass held H8/H9/H10 at n ≥ 25 and scored
   nothing — correctly, under the rule as written. But n=25 gives H10 **14%
   power** against its own threshold. Holding a gate that cannot resolve the
   question costs a week per cycle and then produces a MISS anyway. The gate
   should be set by an MDE calculation at pre-registration time, which this
   project already knows how to do (`LEDGER.md:2466–2494`) and did not do here.

3. **One structural change per version is not the cap.** The cap is one
   structural change *per diagnosis*, and the diagnoses have been coming from
   argument rather than from measurement. v0.55's instinct — *"stop guessing the
   mechanism and measure the landscape"* (`LEDGER.md:7866`) — is exactly right and
   should have arrived three versions earlier. Rule 3 is not what slowed that
   down; not having a mission metric (F1) is.

---

# MANDATORY QUESTION 6 — What is being ignored because it did not fit a pre-registered box?

Five things, all large, all sitting in data already collected.

1. **The non-monoculture tail (F7).** 126 of 1,075 healthy surviving runs have
   GRAZE below 93%, down to 78.3%. `runs/rot-collect/59400.json` has GRAZE 86%,
   APPROACH 3.95% (herding), `maxSpeed` 3.2× control, `biteForce` 1.9× control,
   armour up, and 66% of corpse mass consumed — an arms race and a herd, two named
   mission targets, in one file, inside an arm scored MISS on its median. Not one
   of these runs has ever been opened.

2. **The overshoot–extinction relationship (F11).** Early mean animal age
   r_pb=+0.45, early cv of N r=−0.37, early population size r=−0.26 against
   day-800 survival. This is the strongest unexplained thing in the project
   (`HANDOFF.md §0.4`: "the ~70% survival ceiling is unexplained") and the answer
   was on disk before H2 was written. It did not get filed because nobody ran a
   regression — the pipeline only computes arm means.

3. **The 67.5% of corpse mass that rots (F1).** A standing larder of 169 bodies,
   13% of live animal biomass, decaying untouched, in a world where the project
   has concluded three times that meat is not attractive enough. "Fraction of
   corpse mass consumed" is computable from two logged columns and has never been
   printed.

4. **`carnMax`** — the maximum `carnivory` anywhere in the population — has been
   logged in every run since before v0.49 (`evosim-v0_55_0.html:3431`) and appears
   in no analysis. It reads **0.231** in v0.55 CONTROL. That is the single most
   direct statement of "the far corner is empty" available, and it is free.

5. **The meat-rich effect itself (`[cross-validated]`).** The project *did*
   notice the 92.2%-vs-66.7% survival result and correctly refused to promote it
   on one block. What it has not noticed is that meat-rich is the **only**
   intervention that has ever moved the mission metric (0.375% → 0.908%,
   replicated at 0.963% in v0.55), and that it does so at almost exactly the ratio
   of the constant that was changed — i.e. it is the cleanest *failure* of the
   mission test in the project's history, and simultaneously its only lever.

---

# Appendix — findings at confidence 4–6

- **A1 [5, CONFIRMED]** `LOG.carn` / `LOG.hgt` / `LOG.dage` are not decimated in
  the `LOG.gene` halving block (`evosim-v0_55_0.html:3582–3590`), so they grow
  unbounded relative to the gene series. Reads keyed on `t` (as `score55.py`
  does) stay correct; memory does not.
- **A2 [5, CONFIRMED]** A 715-day run carries **9 gene snapshots**. Every gene
  statistic in every hypothesis is one coarse sample, and `geneEvery` doubles
  adaptively, so snapshot spacing is not constant across runs of different
  length — a sibling of rule 7b that is not written down.
- **A3 [5, CONFIRMED]** `runs/rot-collect/50381.json` shows evolved
  `socialAttraction` 0.451 with population SD **0.143**, against a typical
  gene SD of 0.03–0.05. A 3–4× inflated standing variance is the signature of a
  maintained polymorphism. The project believes herding never emerges.
- **A4 [4, PLAUSIBLE]** `satiateBite()` (`:1676–1681`) caps intake at
  `energyCapacity × upkeep × ticksPerDay`. A specialist carnivore's upkeep is
  1.25–1.6× a herbivore's, so its satiation cap is *higher* — one of the few
  places the cost curve helps the carnivore, and it is not in any analysis.
- **A5 [4, PLAUSIBLE]** Plant and animal detections have separate `senseCap`
  budgets (`:1744`, `:1761`, `senseCap: 8` at `:437`) but feed **one** Luce reservoir. So a
  corpse competes against up to 8 plants in a single weighted draw and loses 8:1
  on candidate count alone, independent of score. Making the act choice
  hierarchical (choose a *class* of act, then a target within it) would remove a
  structural bias that nothing in the biology asked for.

---

# VERDICT

**PIVOT.** Do not ship v0.56 as another mechanism. Do not score H8 as it
currently stands.

The ordered change list this audit implies:

1. **Adopt heterotrophy fraction as the mission metric** and add
   corpse-consumed-fraction and `carnMax` to every digest. No build change; the
   columns exist. (F1)
2. **Re-dose H8** to `invadeFrac` ≈ 0.02 and add a mid-run injection hook
   (`shockDay` is the precedent), so the probe tests a lineage rather than an
   overload. Filter the histogram statistic for non-empty before scoring. (F4, F8)
3. **Fix the scoring instruments before the next weekly pass:** drop
   `ambushTendency` from `NEUT`, compute the drift yardstick per arm, and set
   every n-gate from an MDE calculation — H10 needs n ≥ 60, not 25. (F5, F6)
4. **Retarget carnivory work onto `carrionAttraction` and kill possession.**
   The single highest-information experiment available is a founder-value arm:
   set `carrionAttraction` START to 0.80 and see whether selection puts it back.
   (F2, F3)
5. **Attack the two binding constraints nothing has touched:** generations
   (wire `--pool` into `headless.js` and chain runs) and scale (`worldSize`,
   `animalFounders`, primary productivity). (F10, §1c)
6. **Reallocate the 48% of compute currently on seasonality** to a screening
   pass over the 139 never-varied constants, pre-registered as one batch-level
   prediction. (F9)
7. **Mine the corpus you already have.** 2,309 logs, zero cross-run regressions,
   and a ~12% tail of runs where the mission partially happened. (F7, F11)

**What would change this verdict to "continue as-is":** a single number. If
heterotrophy fraction — measured the way §Q2 measures it, on a matched window,
at n ≥ 40 — exceeds **5%** in any arm that did not get there by raising
`meatValue`, then a second trophic level is emergent in this model, the corner
is reachable at the shipped scale, and the mechanism-per-version programme is
justified after all. The corpus currently caps it at **2.21% across 1,075
runs**, and the only intervention that ever moved it is a constant. Until that
number moves on its own, every additional version is a well-documented step
sideways.
