# DEAD END OR SOLVABLE — evosim, 2026-09-12

Third program audit, per `.claude/skills/program-audit/SKILL.md`. Question put by
the owner: rewrite, or keep iterating. `HOST-POSITION-REWRITE.md` was not read.
`AUDIT-PROGRAM-2026-09-11.md` and `AUDIT-PIVOT-2026-09-12.md` were read and
their findings are not relitigated; where this pass reaches the same place by a
different route it is tagged `[cross-validated]`.

Every number below was computed during this pass from `runs/rot-collect/*.json`
(2,316 logs, 1,063 of them alive at day 800 and never under 20 animals in the
matched window days 400-800) and from `evosim-v0_56_0.html`. Scripts were ad hoc
and reproducible from the corpus plus the build.

Confidence 1-10 on every finding; nothing below 4 is written down.
CONFIRMED = verified against data or code in the repo. PLAUSIBLE = reasoned.

---

## Verdict

**ITERATE WITH NAMED CHANGES.** Not a dead end, and a rewrite would reproduce
the same ceiling in cleaner code. But the target is misstated, and the
constants behind three of the metric's four terms — `a_base`/`a_mass`/
`k_toxinHarm`/`toxMaxLoss`, `k_corpseDecay`/`corpseMin`, and `carrionFloor` —
have never been varied in 2,348 logs.

The mission metric is an identity, not a mystery:

```
heterotrophy = (meatValue*carrionValue / energyPerMassA)   ... trophic transfer, a constant ratio
             * epsilon                                      ... animal production / assimilation
             * consumedFraction                             ... share of corpse mass eaten
             * carrionDigest(carnivory)                     ... 0.30 + 0.70*carnivory
```

Across 1,037 runs this reproduces the measured metric with `corr(log
predicted, log observed) = 0.958` and a median observed/predicted ratio of
0.766, the 23% shortfall being mass lost below `corpseMin` and through gut
excretion. At shipped constants the four terms sit at 0.371, 0.130, 0.194 and
0.349, product 0.33%, measured median 0.26%.

Evolution can move two of those four. The other two are numbers in the source.
The ceiling with both evolvable terms maxed is 3.3-4.4%, so the "no run has ever
exceeded 5%" line that framed the last two audits is a statement about
`meatValue/energyPerMassA` and about upkeep, not about whether selection works.

---

# A — Can any setting of the existing constants make a carnivore pay?

**Yes. Named: `k_corpseDecay` down, `corpseMin` up, `k_mixed` down. Magnitudes
and the arithmetic behind them below.** The carnivore corner is marginal, not
dominated, and two constants that have never been varied sit directly on the
margin.

All figures are corpus medians over the matched window, with gene values from
the window-end snapshot: `senseRange` 21.94, `senseAcuity` 0.499, `maxSpeed`
0.569, `biteForce` 1.477, `metabolicRate` 0.912, animal mass 2.812, `aggression`
0.173, upkeep 0.1187 energy/tick, plant energy 0.2083 per graze-tick at a
97.1% graze share.

### A1. Per-act, meat already wins. Per unit time, it does not.

`grazeYield()` (`evosim-v0_56_0.html:1662`) and the SCAVENGE branch
(`:2041-2060`) use different rate constants: `k_intake` 0.01486 against mass^0.667,
`k_attack` 0.120 against mass^0.75, and the graze path is further divided by
`(1 + k_toughBite*tough)` and by `accessOf()`. At the median animal that is
0.0410 mass/tick grazing against 0.3609 mass/tick scavenging, 8.8x.

Measured, not modelled: energy per scavenge-tick is 1.29x energy per graze-tick
at the evolved `carnivory` 0.074 (median of per-run ratios, n=1,037). At
`carnivory` 0.85 it would be 3.3x.

The act is not the problem. Finding the corpse is.

### A2. The search-time budget, which is the number neither prior audit computed

Corpses are detected in the animal scan (`:1794`), with `hide = 0` for a corpse,
so detection probability is `clamp((sr-d)/sr,0,1) * acuity * (1-cover*0.6)`.
Integrating over a uniform corpse field of density `lambda` gives expected
detections per think of `lambda * pi * acuity_eff * sr^2 / 3`.

Corpus medians: 155.5 standing corpses over a 768x768 world = 2.637e-4 per unit
area; mean standing corpse mass 0.622.

| term | ticks |
|---|---|
| search to first detection (`animalThink` 4, 0.0514 detections/think) | 77.8 |
| travel (mean detection distance sr/2 = 11.0 at speed 0.569) | 19.3 |
| handling (0.622 mass at 0.3609 mass/tick) | 1.7 |
| **cycle** | **98.8** |

Energy per cycle and the resulting rate:

| forager | energy/corpse | gross rate | net of upkeep |
|---|---|---|---|
| scavenger at evolved `carnivory` 0.074 | 4.41 | 0.0447/tick | **-0.0740** |
| scavenger at `carnivory` 0.85 | 11.24 | 0.1137/tick | **-0.0050** |
| grazer | - | 0.2021/tick | +0.0834 |

A perfect specialist carnivore at the observed corpse density sits 0.5% below
bare upkeep and 2.4x below a grazer. It needs **2.25x the standing corpse
density** (350 standing corpses) to match a grazer's rate. Search is 79% of its
cycle; handling is 1.7%.

Confidence 8 · CONFIRMED (arithmetic from shipped constants and corpus
medians) · `[auditor-only]`

### A3. Where the 2.25x comes from, and why it is one untouched constant

Standing corpse density is flux times residence. Measured residence is 1,009
ticks against `1/k_corpseDecay` = 1,250, so decay, not consumption, sets it.
`k_corpseDecay` is **0.0008 in all 2,348 logs** — never varied once. At 0.0002
the standing density rises about fourfold and search time falls from 77.8 ticks
to roughly 20, putting the specialist's cycle near 41 ticks and its gross rate
at 0.27/tick, above the grazer's 0.20.

### A4. The other half: a corpse cannot win the act lottery, at any mass

The MVT scores (`:1820` SCAVENGE, `:1683` GRAZE via `plantScore`) at median
genes, both options at distance sr/2:

| option | score |
|---|---|
| GRAZE, median detected plant (mass 9.63, gut-limited) | 0.4442 |
| SCAVENGE, mean standing corpse (0.622), `carrionAttraction` 0.113 | 0.0240 |
| SCAVENGE, same corpse at `carrionAttraction` 0.80 | 0.1705 |

Solving for the corpse mass that ties GRAZE:

- at equal attraction (0.80) and evolved `carnivory`: **1.89 mass**
- at equal attraction and `carnivory` 0.85: 0.64 mass
- at the shipped/evolved `carrionAttraction` 0.113: **no mass works.** The
  SCAVENGE score saturates at `AGUT*cv` and tops out at 0.130 against GRAZE's
  0.444. Scavenging happens at all only when the plant scan returns nothing, or
  through the Luce lottery's tail.

The mean standing corpse is 0.622 while a corpse is created at ~2.81 (mean
animal mass). Exponential decay to a `corpseMin` of 0.04 gives a mean standing
mass of `(m0 - cm)/ln(m0/cm)` = 0.65, which matches the measured 0.622 to 5%.
That expression does not contain `k_corpseDecay`: lowering decay multiplies the
*number* of corpses, not their size. Raising `corpseMin` is what raises the
size — 0.04 -> 1.0 gives a mean standing corpse of 1.75, and 0.04 -> 1.4 gives
2.02, crossing the 1.89 tie point.

`corpseMin` is 0.04 in all 2,348 logs.

Confidence 8 · CONFIRMED · `[auditor-only]`

### A5. And the marginal cost of the gene itself

`dU/d(carnivory)` = `(2*k_gut*carn + k_mixed*herb*[carn*herb > mixedFree])`
scaled by `m75/upkeepRefM75` and `metabolicRate` = 0.00521 energy/tick per unit
carnivory at median genes with the `mixedFree` band active in 41% of runs.
The digestive benefit at the current scavenged mass is 0.00106. Carnivory is
selected against by about 5:1, and the gap closes at roughly a five-fold
increase in scavenged mass — which is what perfect consumption (0.194 -> 1.0)
delivers, with nothing to spare. `k_mixed` 0 removes about 65% of that marginal
cost; `k_gut` supplies the rest.

(I tested and rejected a sharper version of this: that the population is pinned
at the `mixedFree` cliff, `carnivory = mixedFree/herbivory` = 0.086. It is not.
`carn*herb` spans 0.015 to 0.31 across control runs, 59% below the free band,
and the `k_mixed` 0 arm sits at the same 56%. Recorded because it looked right
and was not.)

### A6. Answer to A

A carnivore's net energy rate can exceed a herbivore's at densities this world
can reach, and the settings are `k_corpseDecay` 0.0008 -> ~0.0002, `corpseMin`
0.04 -> ~1.0, both CFG-reachable today, combined with v0.56's founder
`carrionAttraction` 0.80 which is already shipped. `k_mixed` -> 0 removes the
physiological gene's cost penalty on top.

What that does **not** buy is a mission metric above 5%. The identity caps it at
3.3-4.4% with `meatValue` 24, because `epsilon` is 0.13 and the trophic transfer
ratio is 0.371. The 5% bar is above the model's arithmetic maximum.

---

# B — Is this a search problem?

**No, and the corpus says the search that was run resolved almost nothing.**

Across 1,063 surviving runs, 22 distinct configurations and the 17 CFG keys that
were ever varied, configuration identity explains **8.7%** of the variance in
`log(heterotrophy)`. **91.3% of the spread in the mission metric is seed-to-seed
variation inside the configurations that were chosen.**

Confidence 9 · CONFIRMED · `[auditor-only]`

The identity says why. The terms that were varied move the metric barely:

| arm (seasonAmp / daysPerYear / k_photoCost) | n | heterotrophy % | mean N |
|---|---|---|---|
| 0.35 / 40 / 0.004 | 346 | 0.293 | 283 |
| 0 / 40 / 0.004 | 312 | 0.250 | 289 |
| 0.35 / 120 / 0.004 | 192 | 0.242 | 329 |
| 0.35 / 40 / 0.012 | 162 | 0.243 | 173 |
| 0.35 / 40 / 0.02 | 10 | 0.265 | 106 |

Seasonality took 48% of all compute and plant productivity 20%. Together they
span 0.242% to 0.307%, a factor of 1.27, while moving mean population from 106
to 329. They move total assimilation, and total assimilation cancels out of a
ratio.

The terms that were not varied have this much room in the corpus's own spread:

| term | p10 | median | p90 | max | headroom to its bound |
|---|---|---|---|---|---|
| `consumedFraction` | 0.049 | 0.194 | 0.441 | 0.760 | 5.1x (to 1.0) |
| `epsilon` | 0.064 | 0.132 | 0.246 | 0.441 | 3.4x (observed) |
| `carrionDigest` | 0.316 | 0.349 | 0.421 | 0.540 | 2.6x (to 0.895) |
| transfer ratio | 0.371 | 0.371 | 0.371 | 0.618 | constants only |

So: not 139 dimensions of irrelevance, and not a search problem either. The
causal path is about 19 constants — `meatValue`, `carrionValue`,
`energyPerMassA`, `carrionFloor`, `k_corpseDecay`, `corpseMin`, `k_gut`,
`k_mixed`, `mixedFree`, `k_digest`, `k_toxinHarm`, `toxMaxLoss`, `a_base`,
`a_mass`, `upkeepRefM75`, `k_attack`, `k_health`, `k_retal`, `k_confusion` — of
which four decide the answer and three of those four have never been varied. The
remaining ~130 set population size and total energy flux and drop out of the
ratio. Do not screen 150 constants; the identity already says which handful to
run.

`epsilon` deserves a line of its own. Upkeep is **59.3%** of animal assimilation
and toxin loss **26.0%**, leaving 13.0% for production. Fixed overhead alone
(`a_base` + `a_mass*mass^0.75`) is 43% of upkeep. `a_base`, `a_mass`,
`k_toxinHarm` and `toxMaxLoss` are single-valued across the whole corpus.
`corr(log heterotrophy, log epsilon) = 0.527`.

Confidence 8 · CONFIRMED · `[auditor-only]`

---

# C — What would a rewrite change?

**Nothing that binds.** Any model that conserves matter and charges a realistic
metabolic overhead lands on the same identity. The ceiling is
`transfer * epsilon`, and both factors are choices a rewrite would have to make
again, with no corpus to calibrate them against.

Three architectural properties of this build are real and are candidates for a
rewrite's justification. All three are edits, not rewrites.

**C1. The killer is not fed by its kill, so there is no carnivore, only a
scavenger.** `ACT_ATTACK` (`:1999-2039`) deposits damage and calls
`killAnimal`; the corpse is left on the tile. Cost accounting for the attacker
at median genes: retaliation `biteForce * aggression * k_retal` = 0.102
energy/tick, plus 0.202/tick of forgone grazing, against a kill that takes
`k_health*mass/dmgRate` = 7.8 ticks at zero armour and 9.1 at the evolved
`armour` 0.082. Credit the attacking class with **100% of
all carrion energy in the world** and it collects 0.087 per attack-tick
(`eCarrion / attack-ticks`, corpus median). ATTACK is negative by 0.217
energy/tick under the most generous possible accounting, and it occurs anyway
because `k_meatAttrFloor` 0.5 supplies 83% of its attraction term.

A trophic level in which the predator does not eat its prey is a scavenging
guild. `carrionFloor` 0.30 then lets any herbivore scavenge at 34% efficiency
with no adaptation, so the successful outcome of the current design is
omnivores, not carnivores. Giving the killer a time-limited claim on its kill is
roughly 30 lines: stamp the corpse with the killer's index and a decay, and
multiply the SCAVENGE score by a possession term.
[`[cross-validated]` with AUDIT-PROGRAM F2 on the mechanism; the energy
accounting and the 0.217/tick figure are new.]

Confidence 8 · CONFIRMED · partly `[cross-validated]`

**C2. Reproduction is clonal.** `:2198` — *"reproduce (asexual + mutation in
phase 3; crossover at phase 5)"*. Phase 5 does not exist. `mateChoosiness`
(`:738`) is in the genome and is in the verified-inert list. A carnivore
phenotype needs `carrionAttraction`, `carnivory` and arguably `biteForce` and
`maxSpeed` to move together, and `k_mixed` makes the intermediates cost more
than either corner. With no recombination the only path is sequential mutation
through a fitness valley. Adding crossover is a bounded edit to one function.

Confidence 7 · CONFIRMED (code) / PLAUSIBLE (that it is binding) ·
`[auditor-only]`

**C3. Selection has never built a carnivore in this corpus.** `carnMax`, the
highest `carnivory` in the living population, has median **0.176** across 1,063
runs (p10 0.092, p90 0.287, max 0.571). The founder draw is `START` 0.05 with
`morphSpread` 3.5 sigmas at `ASIG` 0.03 plus `founderNoise` 0.8, i.e. a founder
ceiling near 0.23. In the median run the most carnivorous animal alive at day
800 is inside the founder envelope. Nineteen generations of selection have not
produced one individual outside the range the world was seeded with.

Confidence 7 · CONFIRMED · `[auditor-only]`

**Answer to C.** A rewrite reproduces the dead end with cleaner code. The three
mechanisms above are 30 lines, 60 lines and a CFG slider inside this build.

---

# D — Is the mission well-posed?

**Well-posed, under-scaled, and over-specified in its success bar.**

The sim is producing correct ecology and the project has been scoring it as
failure. Measured: animal assimilation 0.2027 energy per animal-tick, production
13.0% of it, i.e. an ecological efficiency inside the 10% textbook band and
inside the 10-40% range for ectothermic net production efficiency. The prior
audit's carnivore carrying capacity of 8-21 individuals out of 353 is 2-6%,
which is where terrestrial predator:prey biomass ratios actually sit (large-
carnivore biomass runs ~1-3% of large-herbivore biomass in savanna systems).

So the model's answer to "how big is the carnivore niche" is right, and the
answer is **single digits to low double digits** — the prior audit's own
measurement is 8-21 at herbivore-equivalent intake, and the 1-3% field ratio
applied to N=272 gives 3-8. That is the problem. A distinct asexual genotype at
N of order 10 is lost to drift on a timescale of order N generations, and a run
supplies 17-19. The niche is correct and too small to hold a lineage.

`worldSize` is **768 in all 2,348 logs**. It is a CFG constant with a UI slider
spanning 128-1024 (`:3110`). Doubling it to 1536 quadruples the arena, which at
the observed density gives roughly 1,100 animals and a carnivore niche near 44 —
above the drift floor — for about 4x the CPU per simulated day. A 800-day run
goes from ~0.5 h to ~2 h on the Actions runners, which is affordable at the
current job rate.

Selection pressure on the gene that gates the whole path is the other half.
`carrionAttraction` enters the SCAVENGE score linearly and the Luce arbiter
raises it to `k_choiceBeta` 4, so the elasticity of scavenging on the gene is 4.
At a 0.26% energy share and a mutational step of `0.04 * mutationScale 0.897`
against a mean of 0.113, the selection differential is about 0.0034 of the
energy budget, against a drift floor `1/(2N)` of 0.0018. Two-fold. The gene
drifts because its benefit is two-fold above noise, and its benefit is small
because the act is rarely chosen, and the act is rarely chosen because the gene
is small. The corpus shows the loop resolving both ways: in the top 15 runs by
heterotrophy, `carrionAttraction` sits at 0.19-0.44 against a median of 0.113,
`consumedFraction` at 0.40-0.68 against 0.194, and heterotrophy at 1.7-2.2%
against 0.26% — all inside the *same* configuration.

Confidence 7 · CONFIRMED (numbers) / PLAUSIBLE (the drift-floor inference) ·
partly `[cross-validated]` with the pivot's founder-prior diagnosis

**Answer to D.** Achievable at this scale in the sense that carnivory can be
made to pay and can rise by selection to the model's ceiling of ~3%. Not
achievable in the sense of "two trophic levels regulating each other with a
distinct predator lineage" until the arena carries enough animals for the
predator niche to exceed a few dozen. That is `worldSize`, one number, never
varied. And the 5% bar used in the last two audits is above the model's
arithmetic maximum, so it cannot be met at `meatValue` 24 by any amount of
evolution.

---

# E — Sunk cost

**No, it does not change the answer, and the recommendation does not depend on
preserving the build.**

Every number in this audit came from two places: the 2,316 logs and the
constants in the shipped HTML. The build is ~209 KB of one file and could be
rewritten in a week. The corpus cannot — it is 2.6 million simulated days that
calibrate `epsilon`, corpse flux, corpse residence, detection rate, the act
shares, the founder envelope and the gene medians that every piece of the
arithmetic above depends on. A rewrite that discards the build keeps the corpus
only if the new model's constants mean the same things, which a rewrite by
definition does not guarantee.

What is sunk and should be written off is not code. It is the 68% of
compute spent on seasonality and plant productivity, and the seven-MISS streak
scored on arm medians. Neither is recoverable and neither is an argument for
either option.

If the owner threw away everything except `headless.js`, `experiment.js`, the
Actions workflow and `runs/`, the right next move would still be the five
changes below, because they are properties of the identity and not of this
implementation.

---

# MANDATORY QUESTIONS

**Q1 — Is the mission reachable?** Partly. `heterotrophy = transfer * epsilon *
consumed * digest`. Selection reaches `consumed` and `digest`; the product of
their headroom is 13x, taking 0.26% to roughly 3.3%. `transfer` and the
constants behind `epsilon` are source. So "carnivory emerges by selection and
occupies its physical niche" is reachable; "heterotrophy above 5%" is not, at
`meatValue` 24.

**Q2 — Rate of progress.** The metric: fraction of the mission metric's own
corpus variance that the experimental design accounts for. **R^2 = 0.087 across
1,063 runs and 22 configurations.** A converging program drives that up by
choosing configurations that separate; this one has been resolving a twelfth of
the variation it generates, and the other eleven-twelfths contains runs at 2.2%
sitting next to runs at 0.05% under identical CFG.

**Q3 — What should be abandoned?** The 5% heterotrophy bar, and with it any
pre-registration written against an absolute level of the metric. It is above
the model's maximum and it made a correct result look like failure twice. Score
the two evolvable terms instead: `consumedFraction` and the `carnivory` tail.
Both have known corpus distributions, so rule 10's SE test can actually be
applied to them. Second, and cross-validated with the prior audit: the
seasonality line, which cancels out of a ratio.

**Q4 — Simplicity counterfactual.** The identity in this document is four
measurements — `eCarrion`, `ePlant`, `aUpkeep`, `corpseRot` — all four of which
are already logged columns in `evosim-v0_49_0.html`, together with
`carrionMass`. Computing it once at v0.50 would have shown that
`meatAttraction`, `k_choiceBeta`, seasonality and the ATTACK payoff model do not
appear in it. Five structural versions, 2,341 runs and 34 days were spent on
mechanisms the metric does not contain. The shorter path was one afternoon with
`analyze.py` and the columns already in the logs.

**Q5 — Is the process the bottleneck?** Not now. Rules 10, 11 and 12 and the CFG
-reachable genome fix the specific failures they name. The bottleneck is that no
one wrote down what the metric is made of, so target selection had nothing to
aim at. One structural change per version is not the cap; aiming at terms that
are not in the equation is.

**Q6 — What is being ignored for not fitting a box?** The top tail. 5 of 1,037
surviving runs exceed 2% heterotrophy, and in those runs `carrionAttraction`,
`consumedFraction` and `epsilon` are all 2-3x the median together, under the
control configuration. Those five runs are the existence proof that the
machinery works and that the founder value is the thing holding it down. They
have never been analysed as a group because the scoring unit is the arm median.
This is rule 11 stated as a specific target rather than a principle.

---

# NAMED CHANGES

Ordered by what they cost and what they decide.

1. **`worldSize` 768 -> 1536, n=5, before anything else.** Never varied in 2,348
   logs, and it decides whether the carnivore niche can exceed a few dozen
   individuals, which is upstream of every other question here. Prediction
   (rule 1, on record before the runs): mean N rises to 1,000-1,300; the
   heterotrophy median moves by less than 0.1 pp, because the identity is scale
   -free; `carnMax` p90 rises above 0.35. If `carnMax` does not move, scale is
   not the barrier and the arena work stops there.

2. **Corpse persistence as a CFG arm: `k_corpseDecay` 0.0002, `corpseMin` 1.0**,
   against the v0.56 default (which already carries founder `carrionAttraction`
   0.80). Rule 6-legal, no new HTML. Prediction, on record: mean standing corpse
   mass rises above 1.5 from 0.62; `consumedFraction` rises above 0.40 from
   0.19; SCAVENGE act share rises above 0.8% from 0.19%; heterotrophy rises
   above 0.8%. If corpse mass rises and the act share does not, the MVT-score
   arithmetic in A4 is wrong and the barrier is somewhere I have not found.
   (Two paired seeds were launched during this audit; result appended below if
   they finished.)

3. **Kill possession.** The one HTML change that produces a carnivore instead of
   an omnivore, and the one that reopens the ATTACK line the pivot abandoned.
   ~30 lines: stamp the corpse with the killer's index and a possession timer,
   multiply the SCAVENGE score by a possession term. Rule 3 says one structural
   change per version; this is the one to spend it on. It is also the change
   most at risk of failing the mission test, so the possession term must be a
   *gene* weight on an existing score, not a hardcoded energy transfer at the
   moment of death.

4. **Score the two evolvable terms, not the metric's absolute level.** Replace
   the 5% bar with pre-registrations on `consumedFraction` and the `carnivory`
   tail, and add both to `score55.py` along with the per-run distribution rule
   11 already requires and no committed tool prints.

5. **Screen `epsilon`'s constants once, as one prediction.** `a_base`, `a_mass`,
   `k_toxinHarm`, `toxMaxLoss`. Upkeep and toxin together take 85.3% of animal
   assimilation, and `epsilon` multiplies the mission metric directly. One
   family-wise prediction covering all four, per rule 1 as amended, with the
   multiplicity clause the pivot audit's P7 says was dropped.

---

# What would change this verdict to REWRITE

- The corpse-persistence arm raises `consumedFraction` above 0.50 and
  heterotrophy stays below 0.5%. That falsifies the identity and means there is
  an energy sink I did not find, at which point the model is not understood and
  a rewrite is cheaper than reverse-engineering it.
- `worldSize` 1536 leaves `carnMax` and the carnivore count flat. Scale is then
  not the barrier, the niche cannot hold a lineage at any size this hardware
  reaches, and the single-arena design is the thing to replace.
- Kill possession ships and predation still returns less than grazing per tick.
  That would mean the cost structure, not the payoff routing, forbids
  carnivory, and the cost structure is the whole animal model.

# What would change it to plain ITERATE

Nothing in the corpus. The five changes above are all either untouched
constants or a bounded edit; calling the current trajectory "iterate" without
naming them repeats the last five versions.

---

# Appendix — confidence 4-6

- **The Luce arbiter carries the current baseline.** At
  `carrionAttraction` 0.113 no corpse outscores the median plant (A4), so
  scavenging happens through the lottery tail or when the plant scan returns
  empty. `HANDOFF.md` records a plan to revert to argmax if v0.55 gives
  `k_choiceBeta` no reason to exist. The pre-v0.54 argmax corpus sits at 0.350%
  against v0.54's 0.375%, so the revert is probably close to neutral, but the
  cross-version comparison is the one rule 7b warns about and the revert should
  be run as a matched arm rather than assumed. Confidence 5 · PLAUSIBLE.
- **`plantScore` is gut-limited and SCAVENGE is not.** `patch = min(P.mass,
  AGUT)` saturates at `AGUT` = 5.62 for any plant above that mass, which is why
  GRAZE's score is flat from mass 9.63 upward (0.4442 at both 9.63 and 20.0).
  A corpse never reaches the cap because it never exceeds 2.81. The asymmetry is
  not a bug but it is why corpse size, and therefore `corpseMin`, matters more
  than corpse count. Confidence 6 · CONFIRMED (arithmetic), material only in
  support of A4.
- **The `mixedFree` cliff is not binding.** Tested and rejected; recorded in A5
  so it is not re-derived by the next reader.

# What I did not find

- No evidence that the energetics strictly dominate the carnivore. A2's
  specialist is 0.5% below upkeep, not orders of magnitude below.
- No error in the pivot audit's supply-ceiling arithmetic. My `epsilon`-based
  derivation reaches 3.3-4.4% independently against its 3.51%.
- No sign that `analyze.py`, `headless.js`, `check.js` or the determinism
  guarantees are wrong. The corpus parses cleanly and the mass accounting
  closes: production computed from `epsilon` is 4.79e-4 mass per animal-tick
  against a measured corpse flux of 3.80e-4, a 79% recovery consistent with the
  0.766 realisation factor in the identity.

---

# ADDENDUM — the grazing lock-in, found by running change 2

**F0 — A four-line early return in `senseDecide` discards the act choice on 98%
of grazing decisions. It is not a gene, no gene can override it, and `mvtLeave`
has never been varied in 2,348 logs.**

Confidence 9 · CONFIRMED · `[auditor-only]`

This is the largest finding in the audit and it was not in the draft above. It
turned up because change 2 was fired during the audit and its result did not
match A4's arithmetic.

`evosim-v0_56_0.html:1915-1918`, after the entire scan has run and `bestAct` has
been chosen:

```js
const cur = AN.tgt[i];
if (AN.act[i] === ACT_GRAZE && cur >= 0 && P.stage[cur] === 2 && cur !== bestT){
  if (grazeYield(i, cur, herb, fibreTol, toxRes, AREACH) >= AN.rate[i]*C.mvtLeave) return;
  W.abandons++;
}
```

An animal that is already grazing a plant yielding at or above its own running
mean returns before `AN.act[i] = bestAct` and keeps grazing. Measured from
`abandons` against animal-thinks across 157 runs at days 400-800: **1.78% of
grazing decisions re-choose. 98.22% discard the scan.** With GRAZE at 96.8% of
the act budget, an animal is free to act on its scan on about 4.9% of thinks.

Multiply that by the corpse encounter rate from A2 (0.027-0.051 per think) and
SCAVENGE survives to the arbiter on 0.13-0.25% of thinks, against a measured
SCAVENGE share of 0.19%. The act share is accounted for by encounter rate times
lock-in, with no reference to the MVT scores or to any attraction gene. That is
why four structural attempts at the attraction genes moved nothing: at 98%
lock-in the arbiter they were aimed at is bypassed.

The guard has three further properties, all from the same four lines:

- **It is asymmetric.** Only GRAZE is protected. There is no matching rule for
  SCAVENGE or ATTACK, so the herbivore state is sticky and no other state is.
- **It discards FLEE.** `bestAct` is thrown away whatever it is, so a grazing
  animal on an adequate plant will not flee a predator it just detected.
  Predation risk cannot redirect a feeding animal, which weakens the one
  feedback that would make `fearThreshold`, `camouflage` and herding pay.
- **It compares two index spaces.** `cur` is a plant slot and `bestT` may be an
  animal slot; `cur !== bestT` is a plant index tested against an animal index.
  Harmless in effect (it can only skip the guard by coincidence) but it means
  the guard was written for a build where GRAZE was the only act with a target.

`mvtLeave` is 1.0 in all 2,348 logs and its own comment calls it a tuning knob
(`:482`; it also has a UI slider at `:3093` spanning 0-2.5). It is CFG-reachable today.

This is also the clearest mission-test failure in the build. The herbivore
monoculture that five structural versions have tried to break is held in place
by a hardcoded behavioural rule that no genome can reach.

## The change-2 smoke test that found it

Fired during this audit under the prediction written in the Named Changes
section. Two seeds launched; one (777101) produced a usable window before the
40-minute wall budget truncated it at day 365, giving ~105 animal-days and 2.4
generations. **This is a smoke test, not a scored arm** — n=1, no evolutionary
time, window days 290-365, far short of the matched 400-800.

| | v0.56 default | + `k_corpseDecay` 0.0002, `corpseMin` 1.0 |
|---|---|---|
| mean standing corpse mass | 0.994 | **2.728** |
| standing corpses | 109.5 | 105.4 |
| corpse mass consumed | 22.2% | 30.5% |
| SCAVENGE act share | 0.044% | 0.134% |
| heterotrophy | 0.278% | 0.302% |
| evolved `carrionAttraction` | 0.866 | 0.857 |
| `carnivory` | 0.030 | 0.029 |

Scored against the prediction: corpse mass above 1.5 **HIT**; consumed fraction
above 0.40 **MISS** (0.305); SCAVENGE share above 0.8% **MISS** (0.134%);
heterotrophy above 0.8% **MISS** (0.302%). Every term moved in the predicted
direction — corpse mass 2.7x, act share 3.0x — and every one fell short of its
line.

Two corrections to the draft above follow from it:

- **`corpseMin` 1.0 cancels the density gain from `k_corpseDecay` 0.0002.**
  Standing corpses went 109.5 -> 105.4 instead of the ~4x A3 predicted, because
  raising the removal floor ends a corpse earlier. The two constants trade
  against each other and should be varied one at a time: `k_corpseDecay` for
  encounter rate, `corpseMin` for corpse size.
- **A4's score arithmetic is not falsified but it is not the binding term
  either.** At `carrionAttraction` 0.857 against `plantAttraction` 0.730 and a
  corpse of 2.73, the SCAVENGE score should beat GRAZE outright. It did, and the
  act share still sat at 0.134%, which is what sent me to `:1915`.

## Revised order of the named changes

1. **`mvtLeave`, alone, as a CFG arm.** 1.0 -> 0.3 and -> 0 against the v0.56
   default. Prediction, on record: at `mvtLeave` 0 the abandon rate rises above
   30% of grazing decisions, the SCAVENGE act share rises above 1.0% from 0.19%,
   FLEE rises above 0.5% from 0.14%, and heterotrophy rises above 0.8%. If the act shares
   move and heterotrophy does not, the encounter rate is binding and change 2
   is next. If nothing moves, F0 is wrong and the lock-in is not the filter.
   One CFG key, no HTML, and it tests the only term that is large enough to
   account for the 97% GRAZE share on its own.
2. `k_corpseDecay` 0.0002 **without** `corpseMin`, then `corpseMin` separately.
3. `worldSize` 1536.
4. Kill possession (the HTML change).
5. The `epsilon` screen.

`mvtLeave` also belongs in the pin taxonomy discussion in `HANDOFF.md` §2: a
gene cannot be selected on a decision the animal is not allowed to make, and
`plantAttraction`, `carrionAttraction`, `meatAttraction` and `socialAttraction`
all sit behind this guard. Their drift is the expected result of it.
