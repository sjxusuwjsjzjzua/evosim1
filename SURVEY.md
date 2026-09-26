# Artificial-life survey: which physics produced what, and what it means for evosim

Scope: what comparable systems and models achieved, and **the mechanism** behind
each result, sorted into *physics* (allowed here) and *written-in behaviour or
fitness* (not allowed). Then the body-size runaway, predator confusion, and a
ranked list of engine changes using the function names in `evosim.html`.

On sources: the proxy blocked most publisher, arXiv, PubMed and Wikipedia pages.
Olson et al.'s confusion mechanism was checked in their own code
(`adamilab/eos`, `abeeda/tGame.cpp`). Other claims come from abstracts and
search snippets, or from memory where marked *(memory)*. Treat the *(memory)*
ones as leads to verify, not as quotations.

---

## 0. Where the engine stands (from HANDOFF.md and the code)

- Predators never fill up. A kill is about 5% of the killer's energy capacity
  and is eaten in about one tick, and the next kill comes a median 34 ticks
  later. Predation is limited by how often predators meet prey, not by how
  long they take to eat.
- `kConfusion` divides strike damage by `1 + k·n`, where n counts every animal
  within 3 units of the target. Hand-built herders still lost (0–51 of ~550).
- Body size has two absorbing traps: dwarves on a cropped lawn, and giants
  (size 5–11, 100–350 animals, short plants, little predation). Predation holds
  size at 0.6–0.8 while it lasts. Predation is transient over 1M ticks.
- A voice exists: a `call` output, and `heard`/`heardDir` senses that work with
  the head down. `tools/voice.js` probes dumps for it. HANDOFF has no results
  yet.
- Clonal reproduction by default. Newborns appear at the parent's position, so
  the population is viscous and relatedness between neighbours is high.

---

## 1. Phenomenon by phenomenon: what produced it, and is it physics?

### 1.1 Herding and swarming

| work | result | mechanism | physics or written in? |
|---|---|---|---|
| Hamilton 1971, *Geometry for the selfish herd* (J Theor Biol 31:295) *(memory)* | aggregation | the predator appears at a random point and takes the **nearest** prey, so each prey shrinks its "domain of danger" by moving between others | the attack rule is written in |
| Olson, Hintze, Dyer, Knoester, Adami 2013, *Predator confusion is sufficient to evolve swarming behaviour*, J R Soc Interface 10:20130305 | swarming evolves in coevolving prey (and the predator's retina narrows forward) | kill success = X / (number of prey the predator sees within the "safety distance" of the target), plus a **kill delay after every attempt**. Details in §3. | the confusion rule is physics. Roles and fitness (kills; prey survival over 2,000 steps) are imposed; there is no ecology. |
| Olson, Knoester, Adami 2013 GECCO, *Critical interplay between density-dependent predation and evolution of the selfish herd*; 2016 Artif Life 22:299, *Evolution of swarming behavior is shaped by how predators attack* | the selfish herd evolves only under some attack modes | **attack mode** (from outside the group, persistent pursuit of one target, random) and **density-dependent predation** (success falling with local density) decide whether a herd evolves. Density-dependent predation attacked at random took much longer to produce swarming than persistent or outside attacks. | physics of the attack, applied to coevolved brains |
| Olson, Haley, Dyer, Adami 2015, *Exploring the evolution of a trade-off between vigilance and foraging in group-living organisms*, R Soc Open Sci 2:150135 | gregarious foraging evolves from "many eyes" | collective vigilance selects for grouping "as long as there is not a direct cost for grouping (e.g. competition for limited food)", even with the dilution effect controlled for | physics (a trade-off between vigilance and foraging); the engine's `headDown` is the same idea |
| Wood & Ackland 2007, *Evolving the selfish herd*, Proc R Soc B 274:1637 | two evolved phases: a compact torus, and a mobile polarised group that fans out | predation plus foraging on parameterised zone rules (repulsion, alignment, attraction) | the rule structure is written in; only its parameters evolve |
| Ioannou, Guttal, Couzin 2012, Science 337:1212 | real bluegill hunting virtual prey select for alignment and cohesion; coordinated groups were rarely attacked | predators **single out isolated and uncoordinated prey** (the oddity or isolation effect) | the predator's targeting is a real animal's |
| Hein et al. 2015, *The evolution of distributed sensing and collective computation*, eLife 4:e10955 | social attraction evolves and gives collective sensing of resources | **dynamic, patchy resources** that a lone animal senses poorly | physics (the environment) |
| Krakauer 1995, Behav Ecol Sociobiol 36:421; Tosh, Jackson, Ruxton 2006, Am Nat 167:E52 | the confusion effect | confusion is a **targeting failure** in the predator's own perceptual network: position estimates degrade as more similar prey crowd the retina | physics of perception (it can be written as noise in attention) |
| Turner & Pitcher 1986, Am Nat 128:228 *(memory)* | attack abatement = encounter dilution × per-attack dilution | needs predators that take **one victim per attack** (satiation or handling time) and find groups less often per head than loners | physics (satiation, handling time) |
| Polyworld (Yaeger 1994; shinyverse.org/larryy/polyworld.html) | flocking, foraging, fleeing, cannibal "species" | vision; move, eat, mate, fight and light outputs; energy; natural selection only, with no fitness function | physics throughout: the closest relative of evosim, along with Geb |
| The Bibites (Caussan) | herding, pheromone use | v0.3 added a dedicated **herding neuron** | a herding neuron is a written-in behaviour primitive, not allowed here |

**Lesson for evosim.** Every model that evolved grouping against coevolving
predators had a mechanism that makes a predator's success per unit of *its*
time fall with local prey density: confusion with a delay (Olson), or
satiation/handling for dilution (Turner and Pitcher). Or it had many eyes with
no food-competition cost (Olson 2015). evosim now has many eyes (`headDown`),
and it produced prey clumping of 1.17 against 0.90. It has no working
density-dependent predator success.

### 1.2 Alarm calls and signalling

| work | result | mechanism | physics or written in? |
|---|---|---|---|
| Ackley & Littman 1994, *Altruism in the evolution of communication*, ALife IV:40–48 | altruistic warning evolves in a spatial world with food and predators; communication is rewarded only indirectly | **population viscosity**: limited dispersal puts relatives next to each other | physics (spatial structure) |
| Floreano, Mitri, Magnenat, Keller 2007, Curr Biol 17:514 | cooperative signalling evolves only under **high relatedness** or colony-level selection; with low relatedness and individual selection, deceptive signalling evolves | kin/group selection; signal and response must coevolve | relatedness is physics; colony selection is an imposed fitness |
| Mitri, Floreano, Keller 2009, PNAS 106:15786 | information suppression: robots stop signalling when receivers compete with them | competition among receivers | physics |
| Taylor 1992, Evol Ecol 6:352; West, Pen, Griffin 2002, Science 296:72 | in viscous populations, the gain from interacting with kin can be **exactly cancelled by competing with kin** | local density regulation | a warning for evosim: see below |
| Taylor-Davies et al. 2024/25, *Emergent kin selection of altruistic feeding via non-episodic neuroevolution* (EvoApplications; arXiv 2411.10536) | a `feed` action evolves toward own offspring and follows Hamilton's rule rb − c | "environments where it is hard for offspring to survive alone"; **viscosity mattered more than kin recognition** | physics (a transfer actuator, plus juveniles that struggle) |
| Charnov & Krebs 1975, Am Nat 109:107 *(memory)* | alarm calls as manipulation | the caller makes neighbours move, which creates cover or confusion for the caller | needs confusion or selfish-herd physics to exist |
| Hasson 1991; Caro 1995, *Pursuit-deterrence revisited*, TREE 10:500 *(memory)* | calls aimed at the predator ("I've seen you") | the predator gives up because its **success depends on surprise** | physics: attack success depends on whether the prey is aware |
| Lima 1995, Anim Behav 49:11 *(memory)* | many eyes works only if non-detectors learn that a detection happened | an alarm channel closes that gap | evosim's head-down ears do this |

**Implications for the voice evosim now has.**

1. **Relatedness is already high.** Clonal reproduction and births at the
   parent's position make neighbours kin, which is Ackley and Littman's
   condition.
2. **Kin competition may cancel it** (Taylor 1992). Grazers compete for the
   same local cells. The cancellation is weakest where **predators, not food,
   regulate prey**, which is the predator-dominated worlds. Expect alarm calls
   there and not in dwarf or giant worlds.
3. **The `alarm` sense is an involuntary, honest cue** (a neighbour's `hurt`)
   and already carries most of what an alarm call would. A call adds
   information only (a) before anyone is hit, and (b) to animals with their
   head down, which sense others over 30% of their range but hear the full
   range. Look for calls triggered by a big armed stranger in view
   (`animalSize`, `animalWeapon`), not by `alarm`. `tools/voice.js` already
   probes this.
4. **A selfish route needs physics that is not there yet.** A call pays the
   caller when neighbours bolting confuses the predator (Charnov and Krebs;
   needs change 1 below), or when the predator gives up on an aware prey
   (pursuit deterrence; needs change 4). Without either, alarm calls rest on
   kin selection alone.
5. **The cost that matters in nature already emerges:** predators hear calls
   (`heard` is sensed by everyone), so they can evolve to eavesdrop. That is
   good; do not remove it.

### 1.3 Body-size distributions (details in §2)

| work | mechanism |
|---|---|
| Clauset & Erwin 2008, Science 321:399; Clauset, Schwab, Redner 2009 (arXiv 0808.3433) | a lineage's size diffuses with a hard lower bound and a slight upward bias (Cope's rule), against **extinction risk that rises with size**. That trade-off reproduces the right-skewed distribution of 4,002 mammal species. |
| *Ecological determinants of Cope's rule and its inverse*, Commun Biol 2024 (s42003-023-05375-z) | Cope's rule appears when interactions depend only on relative body size and lineage extinction is rare. When extinction is common, top predators are recurrently eliminated, giving recurrent Cope's-rule cycles. When niche matters as well as size, it inverts. |
| Loeuille & Loreau 2005, PNAS 102:5761 | size-structured food webs evolve from one ancestor. The two key parameters are **consumption niche width** and **competition intensity between similar sizes**. |
| Allhoff, Ritterskamp, Rall, Drossel, Guill 2015, Sci Rep 5:10955 | three evolving traits: body mass, preferred prey mass, niche width. Gives realistic webs with **permanent species turnover**. *(memory)*: attack rates follow a kernel in log(prey/preferred mass), with allometric metabolism, competition among consumers of the same prey, and an extinction threshold. |
| Brown, Marquet, Taper 1993, Am Nat 142:573 *(memory)* | an energetic optimum: acquisition rises with mass while conversion into offspring falls, so fitness peaks at an intermediate size |
| Kozłowski & Weiner 1997, Am Nat 149:352 | optimal size comes from allocating to growth or reproduction under **mortality**. Higher size-independent mortality means an earlier maturation and a smaller optimum. |
| Sinclair, Mduma, Brashares 2003, Nature 425:288 | Serengeti: ungulates below ~150 kg are limited by predation, above it by food (a size refuge). This is the engine's giant world. |
| Demment & Van Soest 1985; Jarman–Bell principle; Müller et al. 2013 (Comp Biochem Physiol A) | gut capacity scales with M¹ and intake with M^0.75, so retention time scales with M^0.25. **Large herbivores digest low-quality forage; small ones need high-quality food.** This splits size niches instead of producing one attractor. |
| Lomolino 2005, J Biogeogr 32:1683 *(memory)* (island rule) | on islands small species grow (released from predation and competition) and large ones shrink (limited by resources) |
| Hamilton, Axelrod, Tanese 1990, PNAS 87:3566 *(memory)* | parasites that track common host genotypes favour sex and keep polymorphism: a mortality source that is **frequency-dependent and does not care about size** |

### 1.4 Predator–prey coexistence over long times

| work | mechanism | relevance |
|---|---|---|
| Huffaker 1958 *(memory)*; Goodnight et al. 2008, *Evolution in spatial predator–prey models and the "prudent predator"*, Complexity 13:23 | **spatial structure**: over-exploiting variants drive themselves locally extinct, and patches are recolonised out of phase | evosim's world is one well-mixed arena with mild fertility noise, so there is nothing for a predator to be rescued from |
| Drossel, Higgs, McKane 2001, J Theor Biol 208:91 (Webworld) | **ratio-dependent functional responses** (predators share and compete for prey) and adaptive diet choice give stable, multi-level webs | predator interference is missing here: predators never fill up and do not compete over a kill |
| Kondoh 2003, Science 299:1388 *(memory)* | adaptive foraging (switching between prey) stabilises complex webs | evosim has one prey type per world most of the time |
| Sih 1987; refuge theory *(memory)* | prey refuges stabilise predator–prey cycles | the canopy (`browse`) is a refuge for plants, not for animals |
| Avida: Cooper & Ofria 2003; Chow, Wilke, Ofria, Lenski, Adami 2004, Science 305:84 *(memory)* | **depletable resources** produce frequency-dependent selection and stable diversification; with unlimited resources one type dominates | evosim already has depletable plants |

### 1.5 Speciation

- Dieckmann & Doebeli 1999, Nature 400:354 *(memory)*: sympatric speciation
  needs **disruptive ecological selection** (competition for resources along a
  trait) plus **assortative mating**, on a marker or directly on the
  ecological trait (a "magic trait").
- Avida radiation (Chow et al. 2004): several resources give several niches.
- evosim already has isolation in sexual worlds (0% interbreeding between a
  meat cluster and grazer clusters) and evolved choosiness. What it lacks is
  more **ecological axes** for species to split along. Size niches
  (change 3 below) and canopy height (browsers against grazers) would add them.

### 1.6 Cooperation, kin effects, parental care

- Tags as kin markers are open to **green-beard cheating and mimicry** (Riolo,
  Cohen, Axelrod 2001, Nature 414:441 *(memory)*; Holland's *Echo*, where
  offence, defence and adhesion tags set the interactions). In evosim tags are
  free, so predators could evolve prey-like tags and exploit `attKin`
  (aggressive mimicry). Watch for it; it is a sign of real coevolution.
- Viscous populations favour cooperation unless kin competition cancels it
  (Taylor 1992). Budding dispersal, or regulation by predators rather than
  food, breaks the cancellation.
- Parental care theory (Klug & Bonsall 2010, Evolution; Gross 2005, Q Rev Biol
  *(memory)*): care evolves when **juvenile mortality is high relative to adult
  mortality** and the parent's care raises offspring survival cheaply.
  evosim's `juvSlow` already makes juveniles vulnerable. `childE` and
  `birthSize` are provisioning before birth. Nothing lets a parent act after
  birth. Taylor-Davies et al. got post-birth feeding from a transfer action
  alone.

### 1.7 Open-ended novelty

| work | point |
|---|---|
| Tierra (Ray 1991) *(memory)* | parasites, hyper-parasites and social cooperation arose because organisms could **read and execute each other's code**: the physics left an exploitable interface |
| Avida (Lenski et al. 2003 Nature *(memory)*) | complex features built from rewarded simpler ones; ecology from depletable resources |
| Echo (Holland 1995) *(memory)* | tag-matching interactions give arms races and aggregates (adhesion) |
| Geb (Channon 2001, 2003; channon.net/alastair/geb) | 2D agents with evolved neural nets, actions reproduce/fight/turn/move, no fitness function. First system shown to have **unbounded evolutionary activity** under Bedau's statistics with component normalisation. Closest in spirit to evosim. |
| Bedau, Snyder, Packard 1998 | activity statistics: diversity, new activity, mean cumulative activity, measured against a **neutral shadow** run. Four classes; class 3 is unbounded. |
| Soros & Stanley 2014 (Chromaria) | four necessary conditions: (1) a non-trivial minimal criterion to reproduce; (2) new individuals create new ways to meet it; (3) individuals decide how and where they interact; (4) phenotype complexity not bounded by the representation. **evosim meets 1–3 and fails 4**: 17 body genes, 8 hidden neurons, fixed outputs. |
| Dolson, Vostinar, Wiser, Ofria 2019, *The MODES toolbox*, Artif Life 25:50 | change, novelty, ecology and complexity metrics, with code (github.com/emilydolson/MODES-toolbox-paper) |
| Lenia / Flow-Lenia (Chan 2019; Plantec et al. 2023, ALIFE best paper) | **mass conservation** plus parameters carried locally in the substrate lets several species compete and evolve inside the CA. The general point: conservation laws create ecological interaction for free. |
| ALIEN (Heinemann; github.com/chrxh/alien) | organisms as networks of particle cells with sensor, muscle, weapon and constructor functions; genomes hold blueprints; self-replication. Body plans are open-ended. |
| Karl Sims 1994; Framsticks (Komosinski) *(memory)* | body plans and brains coevolve; Sims used explicit contest fitness, and Framsticks supports both explicit fitness and energy-based ecosystems |
| Primordial Life (Spofford), Evolve 4.0 (Stauffer) *(memory)* | segment or cell types give functions (photosynthesis, attack, defence); organisms built from parts, so morphology becomes the open axis |
| biosim4 (davidrmiller) | pheromone "signals", a genetic-similarity sensor and an optional kill action; selection is a **written-in survival criterion** each generation, so it is not comparable to evosim |
| Sugarscape (Epstein & Axtell 1996) | behaviour rules (movement, combat, trade) are **written in**; useful only for how resource topography shapes migration |

---

## 2. Why body size runs to extremes in evosim, and what stabilises it

### 2.1 An analytic reading of the engine

The quantities, per animal of adult mass m:

- intake while bite-limited: `graze·m^0.75`; upkeep `m^0.75·(upBase + …)` plus
  `upFixed` (F) plus `upMove·m·v²`;
- lifespan `ageK·m^0.25` (`bodyCache`);
- cost of one grown offspring ∝ m (`cBuild` per unit mass plus `childE`
  reserves, capped at `eCap·m0`).

Lifetime offspring, when aging is the main cause of death:

R0(m) ∝ [n·m^0.75 − F − u·v²·m] · m^0.25 / m = **n − F·m^−0.75 − u·v²·m^0.25**

where n is the net bite-limited intake per unit m^0.75.

- **Intake and lifespan cancel.** Intake ∝ m^0.75 times lifespan ∝ m^0.25,
  divided by offspring cost ∝ m, is m⁰. Size is neutral apart from two terms.
- The fixed cost F always favours **larger** bodies.
- Locomotion (∝ m·v²) favours smaller bodies, but only for animals that move.
  Setting the two against each other gives m* ≈ 3F/(u·v²): about 8 at a
  cruising speed of 0.3 and about 1.2 at 0.8. **A giant that sits and grazes
  pays almost nothing to be big.**
- At a density-regulated equilibrium the winner is the type with the **lowest
  break-even resource level** (Tilman's R* rule). From R0 = 1,
  n* = const + F·m^−0.75, which keeps falling as m grows. **Under resource
  competition with bite-limited intake, bigger always wins, up to the gene
  bound or the canopy.** That is the giant trap.
- HANDOFF's optimum, m^0.75 = 4F/n, is right for **rate** of reproduction in a
  growing population, or for any world where mortality does not depend on size
  (lifespan exponent 0). The m^0.25 lifespan removes that interior optimum at
  equilibrium. It also explains why `growExp` 0.75 did not help: maturation
  time ∝ m^0.25 is another factor that cancels.

The dwarf trap is **the other intake regime.** On a cropped lawn (~900 plant
mass over 4,096 cells, about 0.22 a cell against `pRoot` 0.12), a bite is capped
by `B − floor` in `eatPlant`, which does not depend on m. Intake is set by
how fast an animal reaches regrown cells, not by its size, while its costs
rise as m^0.75, so smaller always wins. Lawn and giant are **alternative
stable states that feed themselves**: dwarves crop the plants, which keeps
intake capped and favours dwarves; sparse giants leave standing crop, which
keeps intake bite-limited and favours giants. Plant stature follows, so short
grass locks in the lawn. This explains why each trap is absorbing, and why
height (`browse`) swapped one trap for the other rather than removing traps.

### 2.2 What stabilises size in the literature, mapped onto this engine

1. **Mortality that size cannot escape** (Kozłowski & Weiner 1997; Clauset &
   Erwin 2008, where extinction risk rises with size). With a per-tick hazard
   μ that does not depend on size, lifetime becomes about 1/(μ + 1/L(m)), so
   for large m, R0 ∝ n·m^−0.25 − F·m^−1. That restores HANDOFF's interior
   optimum, m^0.75 ≈ 4F/n. Predation already does this, which is why predator
   worlds hold size at 0.6–0.8, but it is **escapable by size**
   (Sinclair 2003). The mortality that is not escapable should come from
   something emergent: a contact-transmitted parasite, or predators that can
   take big prey together (defence saturation).
2. **Lifespan exponent.** Empirical exponents are about 0.15–0.25. Lowering
   `ageK·m^0.25` to m^β with β < 0.25 gives R0 ∝ m^(β−0.25). β = 0.15 gives
   only a weak pull toward small; β ≈ 0–0.1 is needed for an optimum near 2.
   Cheap to test, but it is a blunt instrument.
3. **Quality against quantity (Jarman–Bell).** Size niches coexist instead of
   one trap winning: small animals take scarce, high-quality regrowth and
   large ones bulk-process abundant low-quality standing biomass. Grazing
   succession and facilitation (Bell 1971; McNaughton's grazing lawns
   *(memory)*) let giants create the lawn that feeds small animals. This
   attacks the root of the bistability, which is that plant energy per unit
   mass is currently the same in a mature cell and in fresh regrowth.
4. **Size-structured predation** (Loeuille & Loreau 2005; Allhoff 2015).
   Interactions depend on size ratios, and similar sizes compete, which gives
   stable size spectra. In evosim a kill takes a time set by the size ratio,
   but big prey escape and there is no synergy between attackers. Group
   hunting (Packer & Ruttan 1988, Am Nat 132:159: cooperative hunting is an
   ESS when solitary hunting is inefficient against large prey) is the
   natural way predators reach giants.
5. **Patchiness and travel cost.** A giant's absolute needs force it to travel
   between patches, at a cost ∝ m·v². A patchier landscape (higher `fertNoise`,
   barren gaps) makes the movement term bite. This is weaker than 1–4 but free
   to test.

---

## 3. Why Olson et al. got swarming from confusion and `kConfusion` did not

What Olson et al. did, from `adamilab/eos` (`abeeda/tGame.cpp`, and the
`eos-data` README):

- One predator and a swarm of prey, each with a Markov-network brain and a
  retina. The predator's view is 180° by default, range 200. Prey see 180°,
  range 100. The predator moves 2.25 units a step, the prey 0.75, so **the
  predator is 3× faster**.
- The predator makes a **kill attempt** on a prey within `killDist` 5 and
  inside its view cone. It counts the live prey that are (a) within
  `safetyDist` (30 in the main runs) of the target, and (b) within the
  predator's vision range and angle. Then `killChance = confusionMultiplier /
  nearbyCount`. A lone target dies for certain.
- **After every attempt, success or failure, `delay = killDelay`** (10 steps,
  with 5 tested). The predator keeps moving but cannot attack again until the
  delay runs out.
- Fitness: predator = kills; prey = number alive summed over 2,000 steps.

Why that selects for swarming while `kConfusion` did not:

1. **In expectation the damage rule is the same; the time cost is not.**
   Dividing damage by (1 + k·n) and landing a hit with probability
   1/(1 + k·n) give the same expected damage. What differs is that Olson's
   predator **pays a fixed block of time for every attempt**. Its kill rate is
   capped at 1/killDelay, and near a swarm it falls to about 1/(killDelay·n).
   In evosim a predator strikes again the next tick at no cost in time, so
   lower damage only makes the kill a few ticks longer. The prey is still
   caught: the predator is fast and has contact.
2. **Kills per encounter against time per kill.** evosim's predators are
   limited by encounters (34 ticks between kills, kills taking ~4 ticks). A
   group that is 2–3× slower to kill still costs the predator little next to
   the search time, and a group is found more easily (herders took 15–60% more
   strikes per head). **A group stays a buffet.** Grouping pays only when a
   group member costs more predator time than finding and killing a loner:
   ≈ 4 hits × (1 + k·n) × cooldown > search time + loner kill time.
3. **The confusion radius is too small.** Olson's safety distance is 6× his
   kill distance. evosim's 3 units is about 2× reach. In the small world
   (256² units, ~1,000 animals) the expected number of other animals within 3
   of a random target is about 0.4, and only ~0.5–1 even at clump 1.2–2.4. So
   k·n is usually below 1. A radius of ~8–10 (about 6 × (radius + reach),
   matching Olson) puts n at 3–10 inside groups.
4. **It counts the wrong animals.** `neighboursOf` counts everyone, including
   other predators and animals of any size or colour. Confusion
   (Krakauer 1995; Tosh et al. 2006) is about **similar-looking** prey. Oddity
   (Landeau & Terborgh 1986 *(memory)*) means an odd-looking prey is singled
   out. Counting only animals similar in tag and size to the target also
   selects for uniform tags within groups, a testable side prediction.
5. **Healing needs time to act.** Prey regain 0.3% of max hp a tick. A
   cooldown lets spread-out, failed damage heal, so failed hits stop adding
   up. With strikes every tick, healing never matters.

**How to express it as physics.** A strike is a **lunge**: a committed act
followed by a recovery time, like a real predator's strike. Whether it
connects depends on how well the attacker can single out the target among
look-alikes around it. Nothing says "group" or "flee", and the prey's response
is left to evolution. Details in change 1 below.

---

## 4. Ranked engine changes

Ranked by (expected effect on a current blocker) × (confidence) ÷ (cost).
All are physics: they change what an act does or costs, what can be sensed, or
what the environment is. None says what an animal should do.

**General notes.**
- A new per-animal state array has to be allocated in `init`, reset in
  `setupBody`, and (if it matters after a reload) saved in
  `snapshot`/`restore`.
- A new body gene or output shifts the genome layout (`W1`, `W2`, `WD`, `NG`).
  Seed genomes then need a remap, as `seedNI`/`seedNO` do now. Prefer config
  constants unless evolvability is the point.
- All rng draws shift trajectories. Compare distributions over seeds, not
  seed against seed.
- Default test: `tools/batch.sh <label> "<k=v>" 400000 401 … 412` (small world),
  against the same 12 seeds on the defaults, scored with `tools/v1score.py`.
  1M-tick runs on seeds 701–710 for anything about persistence.

### 1. Lunge with recovery, and confusion that decides whether the lunge connects (herding)

- **Mechanism.** Olson et al. 2013 (checked in their code), plus
  Krakauer 1995 and Tosh et al. 2006 on confusion as a targeting failure, plus
  Ioannou et al. 2012 on isolated prey being targeted.
- **Implementation** (`updateAnimal`, the `act === 3` block):
  - New `S.cool[i]` (Uint8 or Float32). A strike is possible only when
    `S.cool[i] <= 0`. Decrement it each tick. While cooling, the strike urge
    does nothing and the tick falls through to eating, so no tick is wasted
    (keeps the mouth rule).
  - Confusion: `n` = animals within `confR` (new, ~8–10) of `tj`, excluding
    `i`, **similar to the target**: tag distance (`tagDist(k, tj)`) below
    ~0.25 and mass within 2× (a filtered variant of `neighboursOf`).
    Optionally count only animals within the attacker's sense range, as in
    Olson. Hit probability `p = 1/(1 + kConfusion·n)`: draw `rng()`.
  - On a hit: damage as now, `S.cool[i] = CFG.lungeCool` (e.g. 4).
  - On a miss: no damage, still pay `atkCost`, `S.cool[i] = CFG.missCool`
    (e.g. 8), and give the target a small `hurt` (a startle, so the existing
    `alarm` cue fires).
  - Keep solitary kills about as fast as now by scaling `dmg` by
    `lungeCool`, or leave it and see what predators do.
  - Optional, gene-level: an attention weight `attCrowd` (in the `BODY`
    table), so salience in `sense()` includes −attCrowd × (the neighbour's
    crowding). Predators could then evolve to pick loners, which is what
    selects for grouping in Ioannou et al. This needs a genome remap.
- **Expected outcome.** Kills per unit of predator time drop for prey among
  look-alikes. Loners and odd-coloured animals are taken first. Prey should
  evolve to steer toward the crowd (`crowdDir`), matching tags within groups,
  and bolting on `alarm`/`crowdSpeed`. Risk: fewer predator-dominated worlds.
  Watch regime% and compensate with `eMeat` if needed.
- **Test.**
  1. The existing hand-built herder test (seed-42 evolved start, half the
     herbivores with crowd pull, 20k ticks) in a 3×3 grid: `kConfusion`
     {0, 1, 3} × `missCool` {0, 8, 15}, with `confR` 8. Metric: herders at 20k
     as a share of controls; kill hazard per head; predator ticks per kill.
     **Prediction:** herders ≥ controls at k ≥ 1 with `missCool` ≥ 8; no
     effect at `missCool` 0 (which reproduces the current negative result).
  2. From random, 12 seeds × 400k at the best cell. Metrics: prey clump in
     predator worlds (baseline mean 1.17), share of worlds whose brain probes
     turn toward `crowdDir`, **within-group tag variance** against between
     groups, and meat share and regime%. **Prediction:** mean prey clump
     ≥ 1.5; toward-the-crowd steering in ≥ 4 of 12 worlds (baseline 1);
     meat share −0 to −30%.

### 2. Mortality size cannot escape: a lifespan exponent (quick test) and a background hazard (giant trap)

- **Mechanism.** §2.1: with lifespan ∝ m^0.25, lifetime output does not depend
  on size, so the fixed cost pushes to giants. Kozłowski & Weiner 1997: extra
  mortality that does not depend on size moves the optimum down. Clauset &
  Erwin 2008: extinction risk rising with size bounds the right tail.
- **Implementation.**
  - (a) `bodyCache`: `S.maxAge[i] = CFG.ageK*Math.pow(m, CFG.ageExp)`,
    default 0.25.
  - (b) `updateAnimal`, after metabolism:
    `if (CFG.hazard > 0 && rng() < CFG.hazard) { die(i, 1); return; }`.
    Accidents and disease with no size dependence. This is physics, not a
    cap: it is density-independent and says nothing about behaviour.
    Change 5 is the emergent replacement.
- **Expected outcome.** An interior optimum near m ≈ (4F/n)^(4/3) in worlds
  without predators. Fewer giant worlds. Some risk of pushing back toward the
  dwarf floor where the lawn regime already holds.
- **Test.** 12 seeds × 400k with `browse` 2: `ageExp` {0.25, 0.15, 0.05} and
  `hazard` {0, 1/12000, 1/6000}, as single-factor arms. Metrics: giant worlds
  (mean size ≥ 5; baseline 4 of 12), dwarf worlds (≤ 0.35; baseline 0),
  predator-dominated and carnivore clusters (baseline 8 and 8), and the
  **mid-size share** (worlds with mean size 0.6–3). **Prediction:**
  `ageExp` 0.15 barely helps (R0 ∝ m^−0.1); `hazard` 1/6000 cuts giant worlds
  to ≤ 1 without creating dwarf worlds (browse still blocks the lawn).
  Confirm the mechanism: in giant worlds on the defaults, `dAge` should be the
  main cause of death.

### 3. Plant quality falls as the stand matures; fibre digestion improves with body size (Jarman–Bell; both traps)

- **Mechanism.** Demment & Van Soest 1985 and the Jarman–Bell principle:
  retention time ∝ M^0.25, so large bodies extract more from low-quality
  forage. Grazing succession and lawns: big grazers keep swards short and
  nutritious for small ones. The quality/quantity axis creates coexisting
  size niches (Loeuille & Loreau 2005: niche width and competition set the
  web) instead of one runaway direction. It also breaks the lawn/giant
  bistability of §2.1.
- **Implementation** (`eatPlant`):
  `val = ePlant·(1 − diet^c)·(1 − fib·f_c·(1 − dig(m)))`, where
  - `f_c` = the cell's maturity. Simplest is `S.pB[c]/S.pK[c]`, with stature
    as an alternative: tall woody plants are fibrous. A cleaner version keeps
    a per-cell "young biomass" pool in `updatePlants`: growth feeds it and it
    matures at a set rate.
  - `dig(m) = m^0.25/(m^0.25 + h^0.25)`, a digestion efficiency with
    half-saturation mass `h` ≈ 2.
  - `fib` ≈ 0.6.

  Nothing tells an animal where to feed. Regrowth is simply worth more to a
  small gut.
- **Expected outcome.** In a giant world, cells cropped by giants (low B/K)
  become rich for small animals, so a small grazer can invade (facilitation),
  giving size-structured coexistence. Dwarves on a lawn gain nothing new, but
  the lawn is already blocked by `browse`. Possible split into grazer and
  browser species in sexual worlds (HANDOFF next step 3).
- **Test.** 12 seeds × 400k, `fib` {0, 0.4, 0.7}. Metrics: the number of
  **size clusters** per world (from `--dump`: body sizes 3× apart, each ≥ 5% of
  animals), giant worlds, predator worlds, carnivore clusters. With `sex=1`,
  `mateDist=0.1`, also run `tools/isolation.py` between size clusters.
  **Prediction:** worlds with ≥ 2 herbivore size classes go from ~0 to ≥ 4 of
  12; giant-only worlds ≤ 2.

### 4. Surprise: a strike on an animal that is watching the attacker is weaker (vigilance, pursuit deterrence, alarm calls)

- **Mechanism.** Pursuit-deterrence and perception-advertisement theory
  (Hasson 1991; Caro 1995): if predators depend on surprise, prey gain from
  watching, and a signal aimed at the predator can pay the caller. Many eyes
  (Pulliam 1973; Lima 1995; Olson et al. 2015) needs detection to matter.
  In evosim, detection so far only affects fleeing.
- **Implementation** (`updateAnimal`, strike block): if the target is
  attending to the attacker (`S.tgt[tj] === i && S.tgtId[tj] === S.id[i]`) and
  did not eat last tick (`S.act[tj] !== 1 && S.act[tj] !== 2`), multiply
  damage (or, with change 1, hit probability) by `(1 − CFG.guard)`, e.g.
  guard 0.5. A physical reading: an animal facing its attacker can dodge or
  brace.
- **Expected outcome.** Prey attention evolves toward armed strangers (already
  seen: attWeapon, attSize +0.98). Predators evolve to approach animals whose
  heads are down, and to attend to animals attending elsewhere. The voice
  gains a selfish use: a call that makes neighbours look up protects the
  caller's group. Calls triggered by predators should become more common.
- **Test.** 12 seeds × 400k, `guard` {0, 0.5}, each with `hear` {1, 0}
  (the voice control). Metrics:
  - `tools/voice.js` alarm (loudness with a big armed stranger minus alone)
    and bolt (throttle when a call is heard);
  - mean `call` in the log;
  - a new log field: the correlation, in a world, between a grazer's call
    loudness and a meat-gut animal within its range.

  **Prediction:** alarm call > +0.1 in ≥ 4 of the predator worlds at guard
  0.5 with hear 1, against ≤ 1 with hear 0 or guard 0. Clump rises further.

### 5. A contact-transmitted parasite (mortality that is density-dependent and size-blind; Red Queen on tags; cost of crowding)

- **Mechanism.** Hamilton, Axelrod & Tanese 1990 *(memory)*: parasites
  matching common host genotypes favour rare types and sex. Clauset & Erwin:
  extinction risk. Tierra showed that exploitable interfaces generate new
  ecological roles. This is the emergent version of change 2(b), and the
  realistic cost of herding, so run it after change 1.
- **Implementation.**
  - Per-animal `S.inf[i]` (load 0–1) and `S.strain[i]` (a 3-vector like a
    tag).
  - Transmission when animals are in reach (in the `sense()` neighbour loop,
    or in `updateAnimal` via `neighboursOf(i, reach, -1)`), with probability
    ∝ load × match(strain, recipient tag), where match falls with
    `tagDist`.
  - The load drains `drainK·inf·m^0.75` energy a tick and grows logistically.
  - Recovery at a rate that could depend on a new `immune` gene with upkeep.
  - Strain mutates on transmission.
  - A dead animal's corpse carries its load to scavengers, which creates an
    emergent cost to scavenging.
- **Expected outcome.** Size-blind mortality bounds giants. Negative
  frequency-dependent selection on tags keeps colour diversity. Sexual worlds
  may overtake clonal ones. Dense herds pay a disease cost, so group size
  should become intermediate.
- **Test.** 12 seeds × 400k clonal and sexual, parasite on/off. Metrics: giant
  worlds, tag diversity (entropy), the sexual/clonal gap in predator and meat
  gut worlds (baseline: sex halves meat guts), prey clump. **Prediction:**
  fewer giant worlds, higher tag entropy, and the sex penalty shrinks. Higher
  cost and risk than 1–4.

### 6. Defence saturation: armour guards against one attacker a tick (pack hunting, and a way into giant worlds)

- **Mechanism.** Packer & Ruttan 1988: cooperative hunting pays when a lone
  predator cannot handle large prey. Size-structured food webs (Allhoff 2015)
  keep large prey inside predators' reach. The HANDOFF giant worlds are a size
  refuge (Sinclair 2003); this gives predators a physical route back into
  them.
- **Implementation** (`updateAnimal`): a per-tick counter `S.hitBy[tj]`
  (reset in `step()`). The first strike on `tj` in a tick takes
  `(1 − armourEff·armour)`. Later strikes that tick bypass armour, or face
  `armourEff·armour/(hits)`. Optionally let the prey's counter-strike reach
  only its attended animal, which is already the case. The corpse is already
  shared, since any animal can eat any corpse.
- **Expected outcome.** Predators that converge on one target (same attention
  weights, kin-following) gain. Group hunting of large prey, and bigger
  predators in giant worlds. It gives kin-directed cooperation a real payoff.
- **Test.** 12 seeds × 400k plus the 1M-tick seeds 701–710. Metrics: in
  giant worlds, meat share and kills; the average number of distinct
  attackers per kill (a new counter at kill time); giant worlds at 1M ticks
  (baseline 6–7 of 10). **Prediction:** multi-attacker kills rise; giant
  worlds at 1M drop to ≤ 4 of 10.

### 7. Spatial refuges: concealment in tall vegetation, and a patchier world (long-term coexistence)

- **Mechanism.** Huffaker 1958 and the spatial "prudent predator" work
  (Goodnight et al. 2008): local over-exploitation drives local extinction,
  and asynchronous patches rescue the system. Prey refuges stabilise cycles
  (Sih 1987). evosim's 1M-tick collapse is one global transition into an
  absorbing lawn, with nowhere for predators to persist.
- **Implementation.**
  - (a) Concealment in `sense()`: for neighbour j, cover =
    `clamp((browse·pStat[cj] − cbrt(m_j))/(browse·pStat[cj]), 0, 1) · pB[cj]/pK[cj]`,
    where `cj = cellAt(x_j, y_j)`. j is sensed only if
    `d² < R²·(1 − cover·conceal)²`. This is continuous, so there is no
    threshold (rule 4). Small animals hide in tall stands; giants cannot. It
    also brings in ambush predators and gives trees a second role.
  - (b) Patchiness: raise `fertNoise`, or add a coarse low-fertility mask in
    `init`, so the world is a set of loosely connected fertile patches.
- **Expected outcome.** Predator–prey cycles out of phase between patches, and
  predation surviving to 1M ticks in more worlds. Concealment also gives small
  prey a size-specific refuge, which is a force against gigantism (the island
  rule's predation side, run backwards).
- **Test.** 1M ticks, seeds 701–710, arms (a) and (b) against
  `v1-AD-1M-browse2`. Metrics: predation alive (meat > 15%) at 800k–1M
  (baseline 4 of 10); spatial variance of meat share across quadrants
  (asynchrony); giant and dwarf end states. **Prediction:** ≥ 6 of 10 alive at
  1M, and plant stature stays high in hiding patches.

### 8. A `give` output and inexperienced juvenile mouths (parental care, kin feeding)

- **Mechanism.** Taylor-Davies et al. 2024/25: feeding offspring evolved from
  a transfer actuator in continuously evolving populations, following
  Hamilton's rule, driven mainly by viscosity. Theory of parental care (Klug &
  Bonsall 2010): care evolves when juveniles do badly alone.
- **Implementation.**
  - A seventh output, `give`: a probability, like the mouth urges. When the
    attended animal is in reach (`attendedInReach(i)`), move up to
    `giveRate·m^0.75` energy to it at efficiency ~0.7.
  - Juvenile bite in `eatPlant`/`eatMeat` × `(mass/size)^juvEat`, a physics
    constant, so the young are clumsy eaters.
  - Needs `NO` 7 and the `seedNO` remap.
- **Expected outcome.** Parents feeding animals nearby of their own colour
  (kin), families staying together, and a new route to cohesive groups.
- **Test.** 12 seeds × 400k, `juvEat` {0, 1}. Metrics: energy given per birth,
  the share of gifts going to kin (tag distance < 0.1) against the kin share
  of neighbours, juvenile survival. **Prediction:** at `juvEat` 1, gifts go
  ≥ 3× more to kin than neighbours' kin share would give, in ≥ 6 of 12
  worlds. Lowest priority: it adds an output, and the current blockers are
  size and herding.

### Not physics, but worth adding: open-endedness measurement

Add a tool, not an engine change:

- **Bedau activity.** Components are species clusters (`species()` already
  exists), or brain-weight sign patterns from the `--dump` series. Record
  cumulative activity per component, new activity per window and diversity.
  Run it on a **neutral shadow**: the same run with deaths chosen at random at
  the same rate, which `run.js` could produce by replaying birth and death
  counts.
- **MODES metrics** (Dolson et al. 2019): *change* (persistent phenotype bins
  that differ between checkpoints), *novelty* (bins never seen before),
  *ecology* (entropy of persistent types), and *complexity* (the number of
  brain weights whose knockout changes the probe outputs, since
  `tools/genomes.js` already probes brains).

This turns "open-ended?" into a curve that can be compared between
engine changes. By Chromaria's conditions the fixed genome is evosim's clearest
hard ceiling on novelty. A later mechanism would be duplicating hidden neurons
as a mutation, with NH able to change, and an upkeep per neuron.

---

## 5. Summary of the physics/behaviour line for the systems surveyed

- **Pure physics and natural selection, no fitness function:** Polyworld, Geb,
  Tierra, Avida (tasks reward CPU time, an imposed metabolic physics), Echo,
  ALIEN, Flow-Lenia, the Bibites (except its herding neuron), and evosim.
- **Imposed roles or fitness:** Olson et al. (predator and prey roles, kill and
  survival fitness), Wood & Ackland and Reluga & Viscido (parameterised flocking
  rules, hardcoded predators), Floreano et al. (colony fitness), Karl Sims
  (contest fitness), biosim4 (survival challenges), Sugarscape (hand-written
  rules).
- **The mechanisms worth importing are all physics:** confusion with a time
  cost, surprise, defence saturation, quality/digestion scaling, size-blind
  mortality (parasites), refuges/patchiness, and transfer actuators. Each one
  changes what an act does or costs, or what can be seen, and leaves when to
  do it to the genome.

## Sources (URLs reached or returned by search)

- Olson et al. 2013 code: https://github.com/adamilab/eos (abeeda/tGame.cpp), data: https://github.com/adamilab/eos-data ; paper: https://royalsocietypublishing.org/doi/10.1098/rsif.2013.0305 , https://arxiv.org/abs/1209.3330
- Olson, Knoester, Adami 2016: https://direct.mit.edu/artl/article/22/3/299/2845 , https://arxiv.org/abs/1310.6012 ; GECCO 2013: https://dl.acm.org/doi/10.1145/2463372.2463394
- Olson et al. 2015 vigilance: https://royalsocietypublishing.org/doi/10.1098/rsos.150135 , https://arxiv.org/abs/1408.1906
- Olson et al. 2016 morphology: https://arxiv.org/pdf/1602.08802
- Wood & Ackland 2007: https://doi.org/10.1098/rspb.2007.0306
- Ioannou, Guttal, Couzin 2012: https://www.science.org/doi/10.1126/science.1218919
- Hein et al. 2015: https://elifesciences.org/articles/10955
- Krakauer 1995: https://link.springer.com/article/10.1007/BF00177338 ; Tosh et al. 2006: https://www.journals.uchicago.edu/doi/full/10.1086/499413
- Ackley & Littman 1994 (ALife IV); Floreano et al. 2007: https://www.cell.com/fulltext/S0960-9822(07)01070-6 ; Mitri et al. 2009: https://pnas.org/content/106/37/15786
- Taylor 1992: https://link.springer.com/article/10.1007/BF02270971 ; West, Pen, Griffin 2002: https://pubmed.ncbi.nlm.nih.gov/11935015/
- Taylor-Davies et al.: https://arxiv.org/abs/2411.10536
- Clauset & Erwin 2008: http://science.sciencemag.org/content/321/5887/399.abstract ; Clauset et al. 2009: https://arxiv.org/pdf/0808.3433
- Cope's rule and its inverse (Commun Biol): https://www.nature.com/articles/s42003-023-05375-z
- Loeuille & Loreau 2005: https://www.pnas.org/doi/pdf/10.1073/pnas.0408424102
- Allhoff et al. 2015: https://www.nature.com/articles/srep10955
- Kozłowski & Weiner 1997: https://www.journals.uchicago.edu/doi/abs/10.1086/285994
- Sinclair, Mduma, Brashares 2003: https://www.nature.com/articles/nature01934
- Jarman–Bell / Müller et al. 2013: https://www.sciencedirect.com/science/article/abs/pii/S1095643312004795
- Drossel, Higgs, McKane 2001 (Webworld): https://www.sciencedirect.com/science/article/abs/pii/S0022519300922033
- Goodnight et al. 2008: https://onlinelibrary.wiley.com/doi/abs/10.1002/cplx.20209
- Channon, Geb: http://www.channon.net/alastair/geb/ecal2001/channon_ad_ecal2001.pdf
- Soros & Stanley 2014: https://pdfs.semanticscholar.org/4671/423a1b65f3e35dce603f8746e72ae31193dc.pdf
- Dolson et al. 2019 MODES: https://github.com/emilydolson/MODES-toolbox-paper
- Polyworld: https://shinyverse.org/larryy/polyworld.html
- The Bibites: https://thebibites.itch.io/the-bibites/devlog/267509/the-bibites-030-artificial-life-with-herding-and-viruses
- biosim4: https://github.com/davidrmiller/biosim4
- ALIEN: https://github.com/chrxh/alien
- Flow-Lenia: https://arxiv.org/pdf/2212.07906
