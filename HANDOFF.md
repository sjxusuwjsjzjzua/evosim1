# evosim — handoff

Current state only. `LEDGER.md` holds the history of the previous engine
(v0.44–v0.58) and the reasons it was retired.

## What this is

`evosim.html` is a single-file evolution simulator (engine 1.x, written
2026-09-25). Plants are an evolving cellular layer; animals are agents whose
behaviour is a neural network in their genome. Nothing in the code says what an
animal eats, whom it attacks or where it goes. Open the file on a phone to
watch; run `run.js` to measure.

## How to run it

```bash
node run.js --seed 1 --ticks 300000 --every 10000 --out runs/s1.json   # one world, headless
node run.js --seed 1 --ticks 300000 --set eMeat=10,seasonAmp=0.3        # with physics overrides
python3 tools/v1score.py runs/*.json                                    # one row per world
```

On Actions: dispatch `sim.yml` (ref = the working branch) with seeds, ticks,
optional `set` or `cfg`, and a label; each job also saves `sN-genomes.json`
(`--dump`) and `sN.txt`. All land on branch `results/<label>`;
`bash tools/fetch-results.sh <prefix>` copies them to `runs/`.
About 1 ms per tick at 1,000 animals on one core headless (run.js),
so 400,000 ticks is 10–20 minutes.

Browser check (Chromium and Playwright are preinstalled):
`require(execSync('npm root -g') + '/playwright').chromium`, load
`file:///…/evosim.html`, wait, screenshot, and collect `pageerror` events.

## Design, and why each piece is the way it is

| piece | how | why |
|---|---|---|
| plants | 96x96 cells headless, 64x64 in the page (`gridN`); biomass grows logistically; genes: stature (capacity vs growth), defence (shrinks a grazer's bite, costs growth), dispersal | cheap enough that thousands of animals fit; still evolves |
| roots | grazing cannot take a cell below `pRoot`; seeds take over cells grazed below `pTakeover` | efficient grazers otherwise ate the flora to extinction |
| animal body | 17 genes: size, speed, sense, diet, weapon, armour, detox, reproT, childE, 3 colour tags, birthSize, choosy, 3 attention weights | sense, weapon, detox and speed have quadratic upkeep; armour costs linearly and slows; tags, attention and life-history genes are free |
| fixed cost | `upFixed` 0.003 per animal per tick regardless of size | 0.010 gave an interior body size but 0 predator worlds in 20 at 600k ticks; at 0.003 small fast breeders evolve predation, and predation holds size off the floor |
| brain | 29 senses → 8 hidden (tanh) → 6 outputs (turn, throttle, eat, meat preference, attack, call), plus direct input→output weights | the genome is the behaviour |
| senses | energy, health, hurt, plant ahead-left/centre/right, plant here, plant defence here, the attended animal (direction, distance, relative size, kinship by colour tag, its weapon), nearest corpse (direction, distance), crowding, noise, corpse in reach, attended animal in reach, direction to the centre of the animals in sense range, alarm (the strongest hurt among neighbours) and its direction, stomach fill (0 without `gutCap`), mean speed of the animals in view, the loudest call in range and its direction | facts about the world, not advice |
| attention | the 'animal' senses and any strike go to the neighbour with the highest salience = closeness + attSize x relative size + attKin x kinship + attWeapon x its weapon, weights evolvable | the nearest animal was usually a sibling, so a would-be hunter could not single out prey |
| vigilance | an animal that ate last tick senses animals over (1 − `headDown`) = 30% of its range | without it, grouping never paid; with it prey group where predators are (below) |
| plant height | a plant stands `browse` (2) x stature tall; an animal reaches mass^(1/3) and cannot crop the share of the cell's capacity above its reach | without it worlds fell into dwarf grazers on a lawn (16 of 40); with it carnivore specialists evolve in 8 of 12 worlds against 3, though 4 of 12 go giant (below) |
| juveniles | top speed x (mass / adult size)^0.5 while growing | with it off, killing vanished in all 6 sweep worlds (on: 2 of 6 kept killing) |
| sex | `sex` 0 by default (clonal). With 1, a breeder recombines with the nearest acceptable adult in sense range (colour distance at most 1 − `choosy` for both partners, and genetic distance under `mateDist`, default off), else clones; crossover keeps each neuron's wiring whole | every predator world so far evolved without it; with incompatibility (`mateDist` 0.1) sexual worlds match clonal ones, without it they fall behind (below) |
| mouth | three independent urges (eat, prefer meat, strike). Eat takes whatever food is in reach; preference matters only when there is a choice; a strike happens only when the attended animal is in reach | a hard argmax and then a softmax both let selection bury meat-eating, because firing it with nothing in reach cost a meal |
| diet | one axis, concave (`dietCurve` 2): plant yield x (1 − diet²), meat yield x (0.4 + 0.6 (1 − (1 − diet)²)) | flesh is easy to digest, cellulose needs a specialised gut; the concave form made a first step toward either gut cheap and raised the predator rate (16 of 20 worlds against 11 of 20) |
| corpses | carry flesh (`eMeat` 8 per unit mass) plus the reserves the animal died with; rot slowly | a healthy kill must be worth more than a starved carcass |
| combat | damage = `dmg` x weapon x mass^0.75 x (1 − 0.75 armour) x U(0.8, 1.2); hp = 2 x mass | an equal-sized kill takes ~4 ticks; size protects |
| persistence | `Sim.snapshot()` / `Sim.restore()`; once past bootstrap the page autosaves to localStorage every minute and when hidden, and resumes on load | reaching predators takes hours on a phone; genomes are stored at one byte per gene |
| bootstrap | founders get a cheap ancestral body with spread, a random diet and a completely random brain; they keep arriving while the population is under 200 until one has once reached 400 | fully random bodies rarely survived and bootstrap took 40–65k ticks; now 12–33k |

## What is known (2026-09-25)

- **Grazing evolves from random brains** in every seed, in about 10–20k ticks.
- **Plant defence responds to grazing** (drifts from 0.24 to 0.02–0.45 depending on
  the world).
- **Scavenging and opportunistic predation evolve** once the mouth has no wasted
  ticks. In some worlds killing becomes the main cause of death. It is done by
  plant-gutted animals (diet ~0.01) biting whoever is in reach, and it tends to
  fade over ~30 generations as weapons are lost.
- **Armour rises under predation pressure** (to 0.91 in one world): an arms race.
- **Specialist predators are viable** when flesh is valuable enough: hand-built
  hunters injected into a mature world grew 54 → 127 at `eMeat` 10, and big fast
  hunters cycled with their prey (Lotka–Volterra oscillation, not seasonal).
- **Predator-structured worlds evolve on their own, given time.** In the first
  long batch (500k ticks, 200–450 generations, engine at commit b808ed6/6b3b891)
  2 of 14 worlds became predator-dominated: 30% of all animal energy from meat,
  9–16% of adults living mostly on meat by lifetime intake, killing nearly the
  only cause of death, and plants recovering from ~2k to 10–30k because
  predators hold grazers down (a trophic cascade nobody wrote). In seed 72 it
  switched on around generation 85 after a long peaceful phase, then held for
  250k ticks while top speed doubled (0.64 → 1.38) and sense range doubled:
  a pursuit arms race. Four more worlds held steady killing at 5–8% meat.
  Logs: branches `results/v1-L8`, `results/v1-L9-sex`.
- **The diet gene lags behaviour.** Under the old linear trade-off (`dietCurve`
  1), mean diet in predator worlds was 0.04–0.10: predators were omnivore-gutted
  killers, and a gut shift paid only above ~40% meat. Under `dietCurve` 2 it is
  0.04–0.22.

- **Evolved brains avoid contact.** Measured by probing brains with synthetic
  senses: they strike 44% of the time when touching another animal, prefer meat
  82% of the time when a corpse is in reach, and turn away from other animals.
  That is why most worlds settle into peaceful, evasive omnivores: contact means
  being bitten.
- **Omnivore hunters can invade.** Hand-built hunters with diet 0.3 persisted in
  a mature world and their diet gene climbed to 0.47, so a gradual path from
  omnivore to carnivore exists in this physics.
- **What did not help:** meatFloor 0 (removes scavenging entirely, meat → 0%), a
  concave diet trade-off under the old defaults (`upFixed` 0.010, sex on; it is
  the strongest lever under the current ones, below), weapon-linked teeth (kills fell to zero), a 0.015 fixed
  cost (bootstrap failures, giant animals).

## A carnivore species evolved (2026-09-25, seed 21, `upFixed` 0.003, `sex` 0)

Reproducible at commit eafc1c4: `node run.js --seed 21 --ticks 240000 --set upFixed=0.003,sex=0`
(later speed changes alter rounding, so the exact trajectory differs at HEAD).

| tick | carnivore cluster | diet gene | lifetime meat | world |
|---|---|---|---|---|
| 100,000 | 108 animals | 0.58 | 82% | meat 17% of intake, 621 kills / 500 ticks |
| 120,000 | 196 | 0.56 | 81% | meat 28%, 1,606 kills; 23% of adults are lifetime carnivores |
| 160,000 | 66 + 39 | 0.81, 0.59 | 95%, 86% | plants recovered 11.6k → 29.7k |
| 200,000 | 101 | 0.95 | 99% | meat 23% |
| 240,000 | 85 | 1.00 | 100% | meat 35% |

Herbivore species in the same world sit at diet 0.00–0.01 and 2–4% meat. Speed
and sense range rose on both sides through the run. Nothing about diet, prey or
hunting is written anywhere: the brains started random and the gut followed the
behaviour once a lineage got most of its energy from flesh.

What evolved, from the genome dump at tick 200,000 (`tools/genomes.js`, brain
probes with synthetic senses):

| | carnivores | herbivores |
|---|---|---|
| body size | 2.70 | 0.36 |
| top speed | 1.28 | 0.89 |
| weapon / armour | 0.70 / 0.61 | 0.11 / 0.04 |
| diet gene | 0.95 | 0.01 |
| detox (vs plant defence) | 0.11 | 1.00 |
| sense range | 3.4 | 7.3 |
| strikes when touching an animal | 95–98% | 12–13% |
| throttle alone / near a big armed animal | 0.81 / 0.91 | 0.23 / 0.46 |
| steering near others | neutral | away |
| attention | — | bigger animals (+0.98), strangers (kin −1.59) |

Carnivores are big armed cruisers that strike whatever they meet; herbivores are
small vigilant grazers that watch large strangers and run from them, with
maximal detox against defended plants.

The previous default (0.010 with sex) produced 0 such worlds in 20 at 600k ticks
(`results/v1-U-base`), so the defaults were switched.

This population was the page's "evolved start" until 2026-09-25. Under the
current defaults (`dietCurve` 2, small world) it established predation in only 2
of 4 test worlds, so it was replaced (next section).

## The evolved start (2026-09-25)

Four small worlds on the current defaults, 300k ticks each, with genome dumps
(`run.js --dump`). Three became predator-dominated (regime 72–98%). Each dump
was then founded into 4 new small worlds (600 founders, seeds 3, 5, 7, 9, 40k
ticks); a world counts if meat is over 15% of intake with more than 5 adults
living mostly on meat:

| population | worlds | meat at 40k |
|---|---|---|
| seed 41 | 4 of 4 | 22–25% |
| **seed 42** | **4 of 4** | **30–34%** |
| seed 44 | 2 of 4 | 4–26% |
| seed 21 (the previous one) | 2 of 4 | 3–26% |

Seed 42 is now embedded. Its 80 predators (diet 0.45, size 3.7, weapon 0.58)
cruise (throttle 0.79 alone) and strike 95% of what they touch; its 263
herbivores (size 0.39, speed 1.41, detox 0.99) sit still grazing (throttle 0.06)
and speed up to 0.50 when a big armed animal is in view.

Found a world from a dump headless with `node run.js --cfg seed.json`, where
seed.json is `{"seedGenomes": <dump>.genomes, "seedNI": <dump>.NI, "founders": 600}`.

## Predator worlds are transient over 1M ticks (`results/v1-Z-small-1M`, 10 seeds)

Meat share of intake per 100k ticks (small world, defaults at commit 3ecd997):

| seed | 100k … 1M |
|---|---|
| 701 | 9 4 4 5 5 5 5 5 4 4 |
| 702 | 38 40 32 27 29 29 28 22 19 5 |
| 703 | 24 34 30 28 27 26 21 20 4 5 |
| 704 | 41 34 24 33 31 26 6 4 4 4 |
| 705 | 19 13 5 4 7 18 32 28 27 20 |
| 706 | 32 29 33 27 27 26 27 25 23 18 |
| 707 | 12 18 5 4 13 9 4 5 21 25 |
| 708 | 39 32 16 5 4 4 4 5 5 5 |
| 709 | 19 16 25 20 20 21 21 17 15 19 |
| 710 | 20 19 18 17 19 20 18 20 15 20 |

- Predation holds for 1M ticks in 3 worlds, ends in 4 (at 300k–1M), and
  returns after a peaceful spell in 2 (705, 707).
- The collapse follows one path. While predators hold grazers down, plants
  stand at 8–23k. Where predation fails (in 704 right after an arms-race peak:
  weapon 0.61, armour 0.47, speed 1.27), grazers crop plants to about 900
  across 4,096 cells, and the body shrinks to the size gene's floor (0.30).
  The plants answer by dropping stature to ~0.01: short, fast grass. A lawn of
  dwarves, which predators did not re-invade in 600k ticks in seed 708.
- It is all emergent, and the physics does not forbid a return: 40 seed-42
  predators injected into a dwarf world (founded from seed 708's 1M-tick
  population, 40k ticks to crop the lawn) took it over in 3 of 3 seeds, meat
  5% → 33–36% and plants ~900 → 9–10k within 40k ticks (`reinvade.js` in the
  session scratchpad; a diagnostic, rule 5). What is missing is a path: a
  predator must evolve out of dwarves, and a big body, a weapon and a striking
  brain have to arrive together.

## The defaults, tested: fixed cost x sex, 10 seeds a cell, 400k ticks (`results/v1-V-*`, `results/v1-U-base`)

| | asexual | sexual |
|---|---|---|
| `upFixed` 0.003 | **6 of 10** worlds predator-dominated (regime 17–81%); **2 of 10** with meat guts (up to 10% of animals at diet ≥ 0.5, peak meat share 50–57%) | 1 of 10 predator-dominated; no gut shift |
| `upFixed` 0.010 | 0 of 10 | 0 of 20 (600k ticks) |

regime = share of samples after bootstrap (and after tick 60k) with meat above 15% of intake. The
small fixed cost is necessary; clonal reproduction multiplies it. A likely reason
sex hurts: recombination with the herbivore majority breaks up carnivore gene
combinations unless mating is already assortative.

## Levers on the predator rate (10 seeds each, 400k ticks, 2026-09-25)

| batch | world | worlds with steady killing | predator-dominated (regime > ~30%) | with meat guts |
|---|---|---|---|---|
| defaults (`v1-W-medium`) | medium | 7 | 3 | 1 |
| defaults (`v1-W-small`) | small | 8 | 6 | 2 |
| defaults + new senses (`v1-X-small-senses`) | small | 7 | 5 | 1 |
| `sex=1, mateDist=0.1` (`v1-W-sex-md10`) | medium | 7 | 4 | **3** |
| `dietCurve=2` (`v1-X-small-curve2`) | small | **10** | **10** | **4** |
| `dietCurve=2` (`v1-Y-medium-curve2`) | medium | **10** | **10** | **4** |
| current engine (audit fixes, shared mouth time), local seeds 301–308 | small | **8 of 8** | **8 of 8** | **3 of 8** |

- Genetic incompatibility rescues sex: without it sexual worlds had 1 predator
  world and no meat guts; with it they match or beat clonal ones.
- The concave diet trade-off (`dietCurve` 2: a first step toward either gut is
  cheap) is the strongest lever found. Every world became predator-dominated,
  meat typically 16–29% of intake, mean diet 0.04–0.22, and 4 of 10 grew
  specialists. On fresh seeds (`v1-Y-small-curve2`) it gave 6 of 10 and 2 of 10:
  over both batches 16 of 20 predator-dominated and 6 of 20 with meat guts,
  against 11 and 3 of 20 for the linear trade. **Now the default.** Adding
  `sex=1, mateDist=0.1` on top (`v1-Y-small-curve2-sexmd`) gave 7 and 1 of 10,
  so reproduction stays clonal by default.

## Prey group where predators are, once eating costs vigilance (2026-09-25)

`headDown` (now 0.7, default): an animal that ate last tick senses animals over
30% of its range. A new sense, `crowdSpeed`, reports how fast the animals in
view are moving. Local batch, small world, 400k ticks, seeds 401–412, the same
engine with and without it:

| | `headDown` 0 | `headDown` 0.7 |
|---|---|---|
| predator-dominated (regime > 50%) | 9 of 12 | 8 of 12 |
| prey clump in those worlds | 0.76–1.05, mean 0.90 | 0.93–1.55, mean 1.17 |
| predator worlds with prey clump ≥ 1.02 | 2 of 9 | 7 of 8 |
| strongest "bolt when the others run" (throttle, crowdSpeed 0.8 vs 0.1) | 0.36 | 0.85 (s404) |
| strongest "turn toward the crowd" | 0.39 (a world without predation) | 1.80 (s406, prey clump 1.30) |

- Grouping appears only where there are predators; in the peaceful worlds of
  the same batch prey clump is 0.69–0.86.
- Within a world it builds with predation: s404 went 0.97 → 2.40 over 400k
  ticks at 25–34% meat.
- Mostly it is not steering. In s404 (clump 2.4) prey turn away from the crowd
  and bolt when neighbours bolt: social information, and loners, who get no
  warning, die first. In s406 prey steer hard toward the crowd: herding.
- Brain probes: `probe-crowd.js` in the session scratchpad.
- Founded into 4 new worlds under it, the seed-42 evolved start held predation
  in all 4 (meat 33–50% at 40k ticks), and its prey grouped within 20–30k ticks
  (prey clump 1.34–2.08 at 30–40k). Populations evolved under vigilance (seeds
  404 and 406) also held 4 of 4 and grouped from the start, but at 22–32% meat
  and without a meat-gut cluster, so seed 42 stays the evolved start.

## Worlds without predators are dwarf worlds (2026-09-26)

Across the 40 worlds run on the current engine (seeds 401–412 twice, 501–508,
601–608), 16 ended with mean body size at the size gene's floor (0.30–0.32),
and those are the worlds without predation. In each, killing started (100–600
kills per 1000 ticks early on) and stopped within a few thousand ticks of the
body size reaching the floor, at 80–160k ticks. Among equal dwarves a kill takes
~12 strikes and is worth a small corpse; where predation holds, it holds body
size at 0.6–0.8. The race to small bodies is what the low fixed cost (`upFixed`
0.003) allows. Big predators injected into a dwarf world still take it over
(`reinvade.js`), so the trap is the missing path, not the physics.

Over 1M ticks (`results/v1-AC-1M-vigil`, current engine, seeds 701–710) the
dwarf lawn is where most worlds end: 7 of 10 had mean size 0.30 and meat ~4% by
1M ticks, against 5 of 10 on the older engine (`v1-Z-small-1M`), and none came
back. Predation lasted 100k–700k ticks before the fall. The trap is absorbing.
`browse` (plants taller than an animal's reach keep a canopy it cannot crop;
off by default) is being tested against it. Local, 400k ticks, seeds 401–412
(browse 1: 401–408), against the same seeds without it:

| | none | `browse` 1 | `browse` 2 |
|---|---|---|---|
| predator-dominated | 8 of 12 | 4 of 8 | 8 of 12 |
| worlds with a carnivore cluster | 3 of 12 | 3 of 8 | **8 of 12** |
| dwarf worlds (size ≤ 0.35) | 3 | 2 | 0 |
| giant worlds (size ≥ 5, 100–350 animals) | 0 | 0 | 4 |
| plant stature at the end | 0.03–0.38 | | 0.3–0.98 |

Height turns carnivore specialisation from rare to common, and trees grow
tall. But at `browse` 2 the dwarf trap becomes a giant one: giants sit at mass
8–10, what it takes to reach the tallest plants (height 2 = reach of mass 8).
`browse` 1.5 (tallest plants reachable at mass 3.4), same 12 seeds: 6 of 12
predator-dominated, carnivore clusters in 2, and 5 peaceful worlds of mid-sized
grazers (size 1.9–3.3) too big for their predators. Not monotone in height.
At 1M ticks (`results/v1-AD-1M-browse2`, `-browse4`, seeds 701–710, against
`v1-AC-1M-vigil`), predation (meat > 15%) was alive at 800k–1M in 4 of 10
worlds at browse 2 and 4–6 of 10 at browse 4, against 2–3 of 10 without. But 6–7
of 10 ended as giants (mean size 5–8 at 2, ~11 at 4, 160–380 animals). With or
without height, body size runs to a bound.

A likely reason: growth is `growRate` x mass, so every body size matures in
the same ~170 ticks, while lifespan grows as mass^0.25. Giants get long lives
and quick maturity for free. `growExp` 0.75 (growth like metabolism, time to
maturity rising as mass^0.25) made it worse: seeds 401–408 without browse,
dwarf worlds 3–4 against 1 and predator worlds 4 against 5; with browse 2,
giant worlds 5 against 2. Maturation time is not what drives the runaway;
more likely only giants reach a tall canopy, and their bulk keeps predators
off. `growExp` stays 1.

`browse` 2 is now the default: over the first 400k ticks it turns carnivore
specialists from rare to common and removes dwarf worlds, at the price of
giant ones; at 1M ticks predation lasts in more worlds (4 against 2–3 of 10).
The seed-42 evolved start holds 4 of 4 under it (meat 34–43% at 10–40k).

`upFixed` 0.005 (seeds 401–408, against the same seeds at 0.003): 5 of 8
predator-dominated either way; dwarf worlds 3 against 1, and two giant worlds
(mean size 7–10, ~200 animals). Body size has two traps, dwarf and giant, and
predation lives between them. The fixed cost stays at 0.003.

## Species in sexual worlds are reproductively isolated (2026-09-26)

Current engine, seeds 601–608, 400k ticks, `sex=1, mateDist=0.1` against clonal.
Isolation measured on the end-of-run dumps with `tools/isolation.py`: the share
of cross-cluster pairs the engine's mating rule allows.

- Predator-dominated: 3 of 8 either way. Worlds ending with a cluster living
  mostly on meat: 1 of 8 sexual, 3 of 8 clonal. Pooled with the earlier sexual
  batches (`v1-W-sex-md10`, `v1-Y-small-curve2-sexmd`), meat guts evolve about
  half as often with sex.
- The clusters in sexual worlds are species in the biological sense. In s602
  the meat-leaning cluster (diet 0.56) can breed with 0% of the three grazer
  clusters. In s601 the omnivore cluster (diet 0.31) is isolated (0%) from four
  of the five others. In s603 and s604 choosiness rose to 0.66–0.87:
  assortative mating evolved. Clonal worlds only have lineages.
- Clonal stays the default for the predator rate. The page offers sexual
  worlds as a choice.

## Reflecting mutation bounds: no clear effect (`mutReflect`, 2026-09-25)

A mutation past a gene's bound reflects back instead of sticking to the bound.
Seeds 501–508, 400k ticks: 4 of 8 predator-dominated against 3 of 8 clamped,
2 worlds with a carnivore cluster either way. Off by default.

## Herding without vigilance (tested 2026-09-25)

Hand-built test in worlds founded from the seed-21 population (the evolved start at the time): after
10k ticks, half the herbivores got a weight turning them toward the centre of
the animals they can see (the `crowdDir` sense).

- Crowd pull alone: herders went from half the herbivores to extinct within 15k
  ticks in both worlds.
- With `alarm` / `alarmDir` senses (a neighbour under attack, and where) and a
  flee response given to **both** halves: herders still lost, 549 → 44–160 in
  20k ticks, while solitary animals held.

**Correction (2026-09-25, measured).** Forage is not what herders lose to. Rerun
from the seed-42 evolved start, herders' plant intake per head was within 5% of
the controls and their births per head equal or higher. What differed was
predation: herders took 15–60% more strikes per head and had an 8–27% higher
kill hazard. The reason is that predators never fill up. A kill is worth a
median 5% of the killer's energy capacity, is eaten in about one tick, and the
next kill follows a median 34 ticks later (20% within 10). A group is a buffet
and gives no dilution. The herder brain also steered toward all animals, since
`crowdDir` includes predators. A plant "lawn" that regrew faster raised
herbivore intake and herders still lost. The senses stay (they are information, and a lone
animal can use them too); no benefit to grouping has been written in.

Predator confusion (`kConfusion`: strike damage / (1 + k x others within 3 of the
target), off by default) was tested too: at k 0.5 and 1.5 herders still fell to
0–51 of ~550 in 20k ticks. Confusion lowers damage per strike, not kills per
encounter, so it cannot help while a predator never fills up.

## Sweep, 2026-09-25, previous default at 300k ticks (6 seeds each, `results/v1-T-*`)

Share of energy from meat, per world, last two thirds of the run:

| variant | worlds | meat % | worlds with steady killing (>100 kills / 1000 ticks) |
|---|---|---|---|
| base | 6 | 2.0–5.0 | 2 |
| eMeat 10 | 6 | 3.0–10.4 | 3 |
| dmg 1 | 6 | 2.4–6.1 | 3 |
| seasons 0.4 | 6 | 2.3–5.1 | 2 |
| juvenile slowness off | 6 | 2.1–3.0 | 0 |
| fast life (ageK 3000, growRate 0.016) | 6 | 3.3–6.8 | 0 (one never finished bootstrapping) |

None reached the predator-dominated state within 300k ticks (~80–160
generations). In the older engine that took 85–200 generations.

## Switch results, seeds 401–412, 400k ticks (2026-09-26)

Baseline (current defaults, `runs/voice`): 10 of 12 predator-dominated,
carnivore clusters in 9, one giant world.

| switch | predator-dominated | carnivore clusters | giant / dwarf worlds |
|---|---|---|---|
| baseline | 10 | 9 | 1 / 0 |
| `vigilShare` 1 | 9 | 5 | 2 / 0 |
| **`browseGrown` 1** | **12** | 6 | **0 / 0** (sizes 0.5–1.3) |
| lunge (`strikeCool` 4, `missCool` 12, `confHit` 1) | 0 | 0 | 11 / 0 |
| `hazard` 0.0001 | 8 | 7 | 5 / 0 |
| `hazard` 0.0003 | 12 | 8 | 4 / 0 (predation continues in them) |
| `packHunt` 1 | 11 | 7 | 6 / 0 |
| `fibre` 0.6 | 8 | 6 | 7 / 0 (populations 160–700) |
| `sizeMax` 24 | 8 | 3 | 5 / 0 (size 6–7, well under the new cap) |

`browseGrown` (plant height grows with the plant and does not shrink when
grazed; seedlings are short and grazeable) removed both body-size traps at
400k. The lunge was far too harsh: in a bootstrap population everyone looks
alike, strikes almost never connect, and predation never starts; milder
settings are next (`runs/lungeM`, `runs/coolOnly`). `browseGrown` is being
checked at 1M ticks (`v1-AH-1M-grown`) and on fresh seeds
(`v1-AH-grown-rep` against `v1-AH-base-rep`, seeds 801–812).

## A voice: prey flee calls, predators home on them (2026-09-26)

Every animal has a `call` output (loudness, costs `callCost` 0.002 x loudness x
mass^0.75) and hears the loudest call in sense range, heads down or not.
Seeds 401–412, 400k ticks, against `hear` 0 (calls cost but go unheard).
Probes with `tools/voice.js`:

| | heard | deaf (control) |
|---|---|---|
| predator-dominated worlds | 10 of 12 (populations 850–1,500) | 8 of 12 (three at 100–400 animals) |
| grazers bolt on a call (throttle up) | 11 of 12 worlds, +0.07 to +0.59 | 7 of 12 (untrained weights) |
| grazers turn away from a call | 9 of 12, −0.3 to −1.7 | 5 of 12 |
| meat-eaters turn toward a call | 7 of 10, +0.6 to +1.35 | 4 of 9 |
| alarm calls (louder at a big armed stranger) | 2 of 12 (+0.51, +0.66) | |

- In deaf worlds the hearing weights drift unused, so the probes there read
  about ±1 at random; the heard-world pattern is in the expected direction but
  modest at 12 worlds a side.
- Predators eavesdropping on prey calls is a real phenomenon; nothing wrote it in.
- The call is too cheap to be silenced at the default: mean loudness drifts
  from 0 to 0.9 even in deaf worlds.
- At `callCost` 0.02 (10x, `runs/call10`) calling becomes an honest signal:
  baseline loudness fell to 0.00–0.04 in 8 of 12 worlds, 4 of 12 call louder
  at a big armed stranger (+0.19 to +0.52), and grazers turn away from a call
  in 11 of 12 (−0.4 to −1.9). But predator-dominated worlds fell to 8 of 12
  with several small populations. `callCost` 0.008 is next.

## What 476 run logs say (2026-09-26, `MINING.md`)

- Nearly every world has a predator phase early (meat first passes 15% at a
  median 20k ticks). What differs is how long it lasts: exits run at ~0.2 per
  100k predator-state ticks in all three engine generations (curve 2,
  vigilance, plant height), so a predator phase lasts ~500k ticks on average.
  Score levers by exit rate in long runs, not by onset (`v1score` columns
  predK and exits). Measured that way on the 1M-tick batches (seeds 701–710),
  plant height does lower it: 0.23 exits per 100k predator ticks without,
  0.16 at browse 2, 0.10 at browse 4 (5.1k, 5.8k, 6.9k thousand ticks spent
  predatory).
- Early genes predict nothing (AUC 0.45–0.55). Concentrated meat-eating does,
  weakly: the share of adults living on meat at 40k gives ~67–70% against a
  58% base rate.
- Plant height changed where worlds fall, not how often: before it, 63 of 82
  exits went to dwarf worlds; with it, 42 of 60 went to giant worlds.
- Dwarf exits: plant mass and stature fall 50–60k ticks before the collapse;
  grazers shrink to the size floor while meat-eaters grow (size ratio 3 → 10)
  and then vanish.
- Giant exits: meat-eaters are already at size 10–12 against a gene cap of 12
  (23 of 32 exits); grazers grow 5 → 8 and the predator/prey size ratio falls
  1.6 → 1.4. `sizeMax` (new) tests whether the cap ends these worlds.
- Plant height keeps early carnivore clusters alive more than it makes new ones.
- Plant defence tracks grazer detox, not predation: a plant–grazer cycle of
  its own. Predation speeds up breeding (reproT 0.37 in predator worlds, 0.58
  in giant ones).

## Literature-driven switches (2026-09-26, off by default)

`SURVEY.md` compares this engine with other artificial-life systems. Two of its
ranked changes are now switches, being tested on Actions (seeds 401–412):

- `strikeCool` / `missCool` / `confHit` / `confR`: a strike costs recovery
  time, more after a miss, and connects with chance 1 / (1 + confHit x
  look-alikes near the target). Olson et al. evolved swarming this way; our
  `kConfusion` only divided damage, which costs a predator nothing
  (`results/v1-AG-lunge`).
- `hazard`: a per-tick death chance that no body size escapes, the usual
  stabiliser of body size (`results/v1-AG-hazard1`, `-hazard3`).
- Also from a review: `vigilShare` (head-down in proportion to eating time)
  and `browseGrown` (plant height grows with the plant, seedlings are short):
  `results/v1-AF-vigilShare`, `-browseGrown`.

## Running now

Nothing. Local batches: `tools/batch.sh <label> "<k=v,...>" <ticks> <seeds...>`
runs 4 at a time on a frozen copy of the build (editing `evosim.html` mid-batch
is safe) into `runs/<label>/`; a 400k-tick small world takes ~10 minutes on one
core, so local batches beat Actions for anything under ~20 worlds.

## Next

1. **Giant worlds.** With plant height, 4 of 12 worlds (and 6–7 of 10 by 1M
   ticks) end as giants: size 6–11, 100–350 animals, little predation. Not a
   canopy race: plants in the giant worlds are short (stature 0.21–0.30,
   height ~0.6), while the predator worlds have tall plants (0.95). Scarce food
   per animal pushes the best body size up (optimum ~ (4 upFixed / net intake
   per mass^0.75)^(4/3)), and giants also appeared at `upFixed` 0.005 without
   browse. Fixed cost with browse 2, seeds 401–412 (giant = mean size ≥ 5):

   | `upFixed` | giant worlds | predator-dominated | carnivore clusters |
   |---|---|---|---|
   | 0.002 | 7 | 6 | 4 |
   | **0.003** | **4** | 8 | **8** |
   | 0.004 | 6 | 9 | 7 |
   | 0.006 | 8 | 5 | 2 |

   0.003 is the minimum for giants either way, so the fixed cost is not the
   lever. Big bodies carry more reserve per unit of upkeep (40 x mass against
   mass^0.75), so they outlast scarcity; nothing yet pays for being small
   except a head start on the dwarf race that plant height now blocks. Growth time (`growExp`
   0.75) made it worse.
2. **Herding.** Vigilance made grouping pay (prey clump 1.17 against 0.90 in
   predator worlds), but active steering toward others evolved in 1 of 12
   worlds; mostly prey bolt when neighbours bolt. Longer runs, or the sexual
   worlds (a mate must be in range), may show more.
3. **Speciation** is real in sexual worlds (0% interbreeding between a meat
   cluster and grazer clusters). With plant height, check whether browsers and
   grazers split into species too.
4. **Phone time.** Predators arrive in 20–130k ticks; the page runs ~200–600
   ticks/s. The evolved start covers the wait.
