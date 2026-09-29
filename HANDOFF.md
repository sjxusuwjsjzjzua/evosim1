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
| brain | 36 senses → 8 hidden (tanh) → 7 outputs (turn, throttle, eat, meat preference, attack, call, give), plus direct input→output weights | the genome is the behaviour |
| senses | energy, health, hurt, plant ahead-left/centre/right, plant here, plant defence here, the attended animal (direction, distance, relative size, kinship by colour tag, its weapon), nearest corpse (direction, distance), crowding, noise, corpse in reach, attended animal in reach, direction to the centre of the animals in sense range, alarm (the strongest hurt among neighbours) and its direction, stomach fill (0 without `gutCap`), mean speed of the animals in view, the loudest call in range and its direction, direction to the centre of look-alikes in view (kinDir), the attended animal's colour tag (animalR/G/B), its own heading in world terms (compassX/Y), the mean heading of the moving animals in view (crowdHeading). Input 25 (was stomach fill) always reads 0 | facts about the world, not advice |
| attention | the 'animal' senses and any strike go to the neighbour with the highest salience = closeness + attSize x relative size + attKin x kinship + attWeapon x its weapon, weights evolvable | the nearest animal was usually a sibling, so a would-be hunter could not single out prey |
| vigilance | an animal that ate last tick senses animals over (1 − `headDown`) = 30% of its range | without it, grouping never paid; with it prey group where predators are (below) |
| plant height | a plant stands `browse` (2) x stature tall; an animal reaches mass^(1/3) and cannot crop the share of the cell's capacity above its reach | without it worlds fell into dwarf grazers on a lawn (16 of 40); with it carnivore specialists evolve in 8 of 12 worlds against 3, though 4 of 12 go giant (below) |
| juveniles | top speed x (mass / adult size)^0.5 while growing | with it off, killing vanished in all 6 sweep worlds (on: 2 of 6 kept killing) |
| sex | `sex` 1, `mateDist` 0.1 by default (2026-09-26). A breeder recombines with the nearest acceptable adult in sense range (colour distance at most 1 − `choosy` for both partners, and genetic distance under `mateDist`), else clones; crossover keeps each neuron's wiring whole | against clonal over 24 paired seeds (`v1-AP-sex`): predator-dominated 20 against 20, carnivore clusters 10 against 12, nothing significant. In 13 of 24 the meat-eaters are a separate species (at most 5% of cross pairs could breed), and in 7 some grazer clusters are isolated from each other. Without `mateDist` sexual worlds fall behind (below) |
| compass | `compass` 0 by default; with 1 an animal senses its own heading in world terms | with it prey populations evolve a shared bearing and travel together (prey clumping 1.22 against 0.84 at 400k ticks), but over 1M ticks predators persist in 10 of 24 worlds against 20 without it (p 0.013) |
| give | `give` 1: when the give urge fires and the attended animal is in reach, `giveRate` x mass^0.75 of reserves passes to it (the receiver gets `giveEff` 0.8); the mouth is busy for the tick | the one way to pass energy on after birth; under test (below) |
| seasons | `seasonAmp` (0 by default) makes plant growth rise and fall over `yearTicks`; `seasonWave` 1 makes the season travel along x | a global season makes giant worlds (18 of 24); a travelling one far fewer (7 of 24), and with the compass most worlds stream with it |
| mouth | three independent urges (eat, prefer meat, strike). Eat takes whatever food is in reach; preference matters only when there is a choice; a strike happens only when the attended animal is in reach | a hard argmax and then a softmax both let selection bury meat-eating, because firing it with nothing in reach cost a meal |
| diet | one axis, concave (`dietCurve` 2): plant yield x (1 − diet²), meat yield x (0.4 + 0.6 (1 − (1 − diet)²)) | flesh is easy to digest, cellulose needs a specialised gut; the concave form made a first step toward either gut cheap and raised the predator rate (16 of 20 worlds against 11 of 20) |
| corpses | carry flesh (`eMeat` 8 per unit mass) plus the reserves the animal died with; rot slowly | a healthy kill must be worth more than a starved carcass |
| combat | damage = `dmg` x weapon x mass^0.75 x (1 − 0.75 armour) x U(0.8, 1.2); hp = 2 x mass | an equal-sized kill takes ~4 ticks; size protects |
| persistence | `Sim.snapshot()` / `Sim.restore()`; once past bootstrap the page autosaves to localStorage every minute and when hidden, and resumes on load | reaching predators takes hours on a phone; genomes are stored at one byte per gene |
| bootstrap | founders get a cheap ancestral body with spread, a random diet and a completely random brain; they keep arriving while the population is under 200 until one has once reached 400 | fully random bodies rarely survived and bootstrap took 40–65k ticks; now 12–33k |

## What is known (2026-09-26, current build)

- Predators dominate in about 3 of 4 worlds and a carnivore cluster forms in
  about a third (72 sexual worlds pooled).
- Sexual reproduction with incompatibility is the default. The meat-eaters
  become a separate species in about half of worlds; plant-eaters sometimes
  split into small grazers and large browsers that feed at different plant
  heights.
- With the compass on (off by default), prey populations evolve a shared
  bearing and stream across the world together, and predators travel with
  the stream. Over 1M ticks this starves predation: predators persist in 10
  of 24 worlds with it against 20 without. There is no local flocking and no
  herding by seeking company.
- Meat-eaters that die by killing are killed by other meat-eaters, mostly
  as juveniles of the killer's own kind.
- Colour, heading and feeding are available to evolution. None yet produced
  warning colours, flocking or aimed feeding.

## What was known (2026-09-25)

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

## The evolved start (2026-09-26): `v1-AU-c1` seed 1006

Current build (sexual, compass, 35 senses), 400k ticks from random brains.
The source world had a carnivore species (diet gene 0.62, 75% of energy from
meat) beside four grazer clusters, with prey streaming (`polar` 0.78).
Candidate dumps founded into new worlds (600 founders, 60k ticks):

| dump | predators held | meat, last half |
|---|---|---|
| s1006 | 7 of 8 | 0.27–0.36 (one at 0.11) |
| s1006, quantised as the page stores it | 4 of 4 | 0.24–0.30 |
| s1001 | 2 of 4 | |
| s1020 | 1 of 4 | |

Founded worlds stream from the start (`polar` 0.66–0.82). The meat-eaters are
big (size 8.4), armoured (0.45) and fast. The grazers are tiny (0.32), never
strike, and turn away from other animals.

## The evolved start before that (2026-09-25)

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
| current defaults (vigilance, voice, growing plants), `v1-AK-medium`, seeds 901–910 | medium | 9 | 9 | 2 |

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

Re-checked under the current defaults (`v1-AI-sex`, seeds 401–412): 9 of 12
predator-dominated against 12 clonal. In 4 of the 5 worlds checked with
`tools/isolation.py` (402, 404, 410, 412; not 406, whose most meat-leaning
cluster is diet 0.29 and breeds with grazers at 13–32%) the meat clusters
(diet 0.46–0.77) breed with 0% of the grazer clusters, and choosiness rose to
0.4–0.85. In s402 two meat clusters (diet 0.54 and 0.65) interbreed with each
other (76–77%) and not with grazers. Corrected by the program audit: isolated meat species show up in about a
third of sexual worlds, and dumps oversample meat eaters, which inflates them.

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

## Switches removed after the program audit (2026-09-26)

These were tested, came out null or worse, and are gone from the build (the
results stay in this file): stomach (`gutCap`, `gutDig`; the `gut` sense is
kept as an always-0 input so evolved genomes keep their layout), `vigilShare`,
`mutReflect`, `growExp`, `strikeCool`/`missCool`/`confHit`/`confR`, `hazard`,
`packHunt`, `fibre`/`digestMass`, `killCool`, `cover`, `kConfusion`. Defaults
bit-identical before and after. `sizeMax` stays for a retest.

## The current defaults, measured (2026-09-26)

24 fresh worlds, seeds 1001–1024, 400k ticks (`results/v1-AL-current24`):
predator-dominated 20, carnivore clusters 12, giant 1, dwarf 0. At 1M ticks
(`v1-AL-1M-current`, seeds 701–710): no giant or dwarf worlds, 4 exits from
the predator state in 7.1k thousand predator ticks (0.06 per 100k); seed 701
barely started.

## Switch results, seeds 401–412, 400k ticks (2026-09-26)

Baseline (current defaults, `runs/voice`): 10 of 12 predator-dominated,
carnivore clusters in 9, one giant world.

| switch | predator-dominated | carnivore clusters | giant / dwarf worlds |
|---|---|---|---|
| baseline | 10 | 9 | 1 / 0 |
| `vigilShare` 1 | 9 | 5 | 2 / 0 |
| **`browseGrown` 1** | **12** | 6 | **0 / 0** (sizes 0.5–1.3) |
| lunge (`strikeCool` 4, `missCool` 12, `confHit` 1) | 0 | 0 | 11 / 0 |
| mild lunge (`strikeCool` 2, `missCool` 6, `confHit` 0.2), local | 6 | 7 | 4 / 0 (prey clump no higher) |
| strike recovery only (`strikeCool` 3), local | 1–3 | 0 | 10 / 0 |
| `killCool` 20 (handling time after a kill), on top of `browseGrown` | 12 | 9 | 0 / 0 (prey clump ~0.90, no gain) |
| `killCool` 60 | 9 | 5 | 0 / 0 (meat 6–29%, prey clump ~0.80) |

`headDown` 0.9 (local, on `browseGrown`): 10 of 12 predator-dominated, prey
clump 0.70–1.09, no gain over 0.7. The grouping vigilance gave under
full-height plants (1.17) has not carried over to growing plants.

`cover` 2 (animals among taller plants are hard to see; local): 10 of 12
predator-dominated, carnivore clusters 7, prey clump 0.69–1.11 (mean 0.93, as
without). No grouping gain.

**Grazers bite each other, but that is not why grouping does not pay**
(program audit A10; the mechanism was ruled out 2026-09-26, below). The herder diagnostic with each hit attributed to its
attacker (kin-steering herders, seeds 3, 5, 7): 75–90% of the hits grazers
take come from animals living mostly on plants (15–20 per 1000 animal-ticks),
2.5–5 from meat-eaters. Plant-gutted animals strike whoever they touch, their
own kind included, because a kill pays even to a plant gut (`meatFloor` 0.4).
A grazer that joins a group mostly gains neighbours that bite it. The paired
factorial includes `meatFloor` 0.2, which should cut that biting; if prey
clumping rises there, this is the mechanism.
Dropping `meatFloor` to 0.1 in the diagnostic did not cut the biting within
30k ticks (still 20–34 hits per 1000 from plant-eaters): the evolved strike
urges persist; the factorial from random brains is the real test.
From random brains over 400k ticks (`runs/floor1`, seeds 1001–1012, paired
with `v1-AL-current24` by `tools/paired.py`): prey clump unchanged (0.929
against 0.932), carnivore clusters 3 against 6 (p 0.25), and the grazers'
strike urges unchanged (0.39 against 0.37 on contact). So grazers do not bite
for the meat. Either killing a neighbour pays as interference (it frees
forage) or the urge drifts because a strike is cheap (`atkCost` 0.004 x
mass^0.75). A 5x strike cost is being tested (`runs/atk20`).
`eMeat` 5 (24 paired seeds): meat share 0.22 against 0.27 (p 0.064), nothing
else moved.
`eMeat` 12 (24 paired seeds): meat share 0.36 against 0.27 (p 0.002);
predator-dominated 23 against 20 and carnivore clusters 16 against 12, both
not significant; diet gene, prey and predator clumping unchanged. Richer meat
means more killing by the same omnivores, not more specialisation.
`meatFloor` 0.2 (24 paired seeds): nothing significant (predator-dominated
22 against 20, carnivore clusters 15 against 12, prey clump 0.87 against
0.90).
`meatFloor` 0.6 (24 paired seeds): nothing significant (carnivore clusters 9
against 12, diet 0.084 against 0.099, p 0.15). Across 0.1–0.6 the meat floor
barely matters.

`chew` 1 (24 paired seeds): nothing significant (prey clumping 0.886 against
0.900, p 0.31; meat share 0.267 against 0.272).
`chew` 4 (24 paired seeds): nothing significant either (prey clumping 0.834
against 0.900, p 0.54). Chewing time in both directions leaves grouping flat.

Strike cost, `atkCost` 0.02 and 0.05 against 0.004 (v1-AN-atk20/atk50, 24 paired
seeds, dispatched). Expectation, written before the results: grazers' strike
urges fall (two early local worlds at 0.02: 0.01 against 0.23, 0.40 against 0.85)
and prey clumping rises if biting between grazers is what punishes grouping.
Kill share may fall at 0.05, because predators pay the same cost.
Result, `atkCost` 0.02 (24 paired seeds): grazers' strike urges fell (0.28/0.32
on contact with smaller/bigger, against 0.45/0.45) but prey clumping did not
move (0.859 against 0.900, p 0.54), nor did anything else. Locally (`runs/atk20`,
12 seeds) the urges did not even fall; the two early worlds were noise.
`atkCost` 0.05, 12x (24 paired seeds): nothing significant. Grazer urges
0.30/0.30, prey clumping 0.868 against 0.900 (p 0.15), kill share 26% against
27%. Predation does not rest on cheap strikes.
`size` 24 (24 paired seeds): nothing significant (carnivore clusters 7 against
12, p 0.23; prey clumping 0.883 against 0.900).

**Biting ruled out as the barrier** (herder diagnostic, `herd3.js` with `NOBITE`:
every grazer's strike bias −20 at the split, kin-steering herders, seeds 3, 5,
7, 30k ticks). Hits from plant-eaters fell from 14–20 to 2–5 per 1000
animal-ticks, and herders lost in all three worlds (41 against 302, 0 against
823, 0 against 597). With biting left on, the same herders won two of three (172
against 28, 1092 against 21) and lost seed 5. Lineage outcomes over 30k ticks
are mostly drift, and herders were not much more grouped than controls in any
arm (0.35–2.5 neighbours against 0.5–1.9). Cheaper biting is not what grouping
lacks: steering toward look-alikes does not raise density enough to buy
anything.

**Dilution exists, grouping still does not pay** (2026-09-26, scratchpad
`hazard.js`, `herd4.js`):
- Per-tick kill hazard of a grazer by grazer neighbours within 4, with a
  meat-eater within 10 (per 10^4 ticks; evolved start seed 3, and
  `v1-AL-current24` s1004 dump): 0 neighbours 103 / 111, 1: 83 / 105, 2–3:
  55 / 70, 4–7: 35 / 28. Groups of 2+ are much safer; a pair barely is. Almost
  all exposure is at 0–1 neighbours.
- Grazers see few others. About 1000 animals on 256 x 256 leave 1–2 in sense
  range. Grazers eat 82–92% of ticks, so head-down blinds them most of the time.
  A look-alike is in view on 18–22% of ticks (28–37% with `headDown` 0).
- Strong hand-built herders (turn += w x kinDir, throttle up while fewer than 3
  animals in view): at w 4 and 8, 6 of 6 lost and were not more grouped (1.5–2.6
  neighbours within 6, against 1.6–2.7). They moved more and bred less.
- With free 2.5x vision and no head-down for the herder line, vision alone
  won 3 of 3 worlds outright: killed 1.3–1.6 against 2.5–2.6 per 1000
  animal-ticks. Vision plus steering toward kin (w 4) lost 2 of 3, and was
  killed more (1.9–2.1) than vision alone. With 3.6–8.7 animals in view,
  steering toward the centre of look-alikes still left 0–1.2 neighbours
  within 6 and cost births.

So grouping fails on the cost side, not for lack of information: reaching
and keeping a group takes movement that costs forage and breaks off fleeing,
and a pair (the first step) buys almost nothing. Seeing further is worth a
great deal to a grazer, alone.

**Density** (`cellSize` 3 and 2 against 4, same 64 x 64 plant cells, so 1.8x
and 4x the animals per area; v1-AO-cell3/cell2, 24 paired seeds, dispatched).
Expectation: more look-alikes in view, so if the sparse world is what stops
grouping, prey clumping rises above 0.9, most at `cellSize` 2. Predators meet
prey more often too, so kill share may rise and predator worlds may crash more.
Result, `cellSize` 3 (24 paired seeds): prey clumping 1.013 against 0.900 (17
of 24 up, p 0.064), the first arm to move it. Nothing else changed (predator
worlds 22 against 20, meat 0.289 against 0.272). Grazer brains barely changed
on average: turn toward kin −0.06 against −0.16, 5 worlds above +0.5 against 4.
Kin steering does not predict clumping across worlds (rank correlation 0.24,
permutation p 0.25; 0.08 in baseline). So the mean rise may be food patchiness
at the new scale (6 units now spans 2 cells, not 1.5). The top of the tail
does herd, though: the three most clumped dense worlds (1.68, 1.23, 1.22)
turn toward kin at +1.24, +0.85, +0.30. s1021 has the strongest kin
following of all 48 worlds, with prey clumping 1.1–2.0 through the run.
Result, `cellSize` 2 (24 paired seeds; s1009 went extinct at 58k and s1015
at 397k, none in baseline): prey clumping 1.195 against 0.903 without s1009
(18 of 23 up, p 0.011), a dose response. Giant worlds 7 against 1 (p 0.07),
diet gene 0.18 against 0.10 (p 0.09), predator clumping 1.29 against 1.77. But
kin steering falls (mean −0.37, 1 world above +0.5), so the rise is not
grazers seeking look-alikes. A mid-run knockout of the social senses (crowd,
crowdDir, crowdSpeed, heard, heardDir, kinDir) at 200k ticks in four of these
worlds tests whether it is behaviour at all (scratchpad `knock2.js`).
Knockout result (seeds 1001, 1007, 1012, 1019 at `cellSize` 2; mean prey
clumping over the 60k ticks after the cut, against the same world uncut):
1.18 against 1.62, 1.72 against 2.07, 2.18 against 1.74, 1.96 against 2.13. Cut
prey still clump at 1.2–2.2, far above the 0.9 of normal worlds, so most of
the dense-world clumping is not social steering. Likely causes are food
patches at the finer scale, or young staying where they were born, since
a denser world holds the same food per cell in a smaller area. A social part
exists in some worlds. The cut also cost population in three of four worlds
(1389 → 851, 836 → 692, 909 → 559), so prey use those senses, mostly to
flee. `cellSize` stays 4: the clumping is mostly not herding, and giant worlds
rise.

**Herding under growing plants is the main open question.** Tried and null:
stronger head-down (0.9), handling time after a kill (20, 60), strike
recovery and look-alike confusion (two settings), cover. Prey clump stays at
0.9–1.0 with predators present. The next honest step is a hand-built herder
diagnostic under the current physics (rule 5): if grouping does not pay even
when built in, no amount of evolution will find it.

**Hand-built herder diagnostic under the current physics** (`herd3.js` in the
session scratchpad; seed-42 evolved start, half the grazers given +3 on
turn-toward-crowd after 10k ticks, lineage inherited): herders died out in 3
of 3 worlds within 20–30k ticks. They took 12–70% more hits per head and had
slightly fewer births, and were not even more grouped (1.4–2.1 neighbours
against 1.4–2.3). `crowdDir` points at every animal in view, predators
included, so steering toward it means steering toward predators. Grouping
does not pay in this physics even when built in; evolution cannot be expected
to find it until something changes that.

**Predators group; prey do not** (`clumpPred`, new, local seeds 401–408 on the
current defaults): meat-eaters sit at 1.35–2.81x a random scatter while prey
sit at 0.77–1.14. With `packHunt` (armour turns only the first blow of a tick)
predators form tight packs (4.1, 8.5, 14.7, 3.1x in four worlds) and prey
spread out (0.36–1.00), but predation falls (6 of 8 predator-dominated against
8). Whether the default grouping is cooperative hunting or predators
converging on the same prey and carcasses is not yet known.

**`kinDir`** (new sense, direction to the centre of look-alikes; local seeds
401–412 on the current defaults): 11 of 12 predator-dominated, carnivore
clusters 8, prey clump 0.64–1.10 (mean 0.92, as without). Probes
(`tools/herd.js`): grazers turn toward kin in 3 worlds and away in 4; in two
(408, 409) they turn toward kin (+1.2, +1.3) and away from the crowd (−1.4,
−0.8), following their own kind and avoiding strangers, without that making
them clump more. Grazers turn away from calls in 11 of 12 (replicated).

Handling time does not make groups pay: surplus killing inside a group is not
what keeps prey apart.
| `hazard` 0.0001 | 8 | 7 | 5 / 0 |
| `hazard` 0.0003 | 12 | 8 | 4 / 0 (predation continues in them) |
| `packHunt` 1 | 11 | 7 | 6 / 0 |
| `fibre` 0.6 | 8 | 6 | 7 / 0 (populations 160–700) |
| `sizeMax` 24 | 8 | 3 | 5 / 0 (size 6–7, well under the new cap) |

Fresh seeds 801–812 (`v1-AH-base-rep` against `v1-AH-grown-rep`): predator-
dominated 9 against 9, carnivore clusters 4 against 8, giant worlds 7 against 0.
Over 24 seeds, `browseGrown` gives 21 predator worlds against 19 and 0 giant
worlds against 8, with no dwarf worlds either way. Now the default. The
evolved start holds 4 of 4 under it (meat 34–42% at 10–40k ticks). Populations evolved under the
current engine transplant worse (seeds 802, 805, 808 of `v1-AH-grown-rep`: 0,
3 and 2 of 4 worlds), so seed 42 stays. A second try, 600k ticks on the full
current engine (`runs/evo600`, seeds 1101–1104): seed 1104 shows nearly
everything (alarm and food calls, grazers turning from calls, meat guts
homing on them, grazers following kin and avoiding strangers) but held in 2
of 4 transplants, seed 1103 in 3 of 4; predators died out early in the
failures (1104's dump had 43 meat guts against seed 42's 80). Seed 808 has
clearest voice seen (re-dumped with the killers oversampled by lifetime
intake, 1104 held in 1 of 4 and 1103 in 3 of 4; seed 42 stays):
grazers bolt on a call (+0.79) and turn away (−1.84), meat guts turn toward it
(+0.88).

At 1M ticks (`v1-AH-1M-grown` against `v1-AE-1M-voice`, seeds 701–710)
predation lasts: all 10 worlds still predatory at 1M (meat 12–31%), 9.0k of
~9.4k possible thousand ticks in the predator state against 6.5k, exits 0.04
per 100k predator ticks against 0.11, and no giant or dwarf worlds (mean sizes
0.5–4.9). The body-size traps that ended most long runs are gone.

Predation here needs a predator free to strike every tick: any strike
recovery (`strikeCool`) starved predators before confusion could shape prey.

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
- At `callCost` 0.02 (10x, `runs/call10`) calls turn into a costly, reliable signal:
  baseline loudness fell to 0.00–0.04 in 8 of 12 worlds, 4 of 12 call louder
  at a big armed stranger (+0.19 to +0.52), and grazers turn away from a call
  in 11 of 12 (−0.4 to −1.9). But predator-dominated worlds fell to 8 of 12
  with several small populations. At `callCost` 0.008 (`runs/call4`): alarm
  calls in 4 of 12 (+0.27 to +0.58), grazers turn away from calls in 12 of
  12, but 7 of 12 predator-dominated. Costlier calls make clearer signals and
  consistently cost predation (random founders call at ~0.5 and pay for it
  during bootstrap), so the default stays at 0.002.

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

## Self-audit, 2026-09-27: converging or looping?

Since 2026-09-26: 139 commits, 26 engine commits, 42 result branches.
- **Converging in knowledge.** A long list of nulls now rests on paired
  tests and hand-built diagnostics (herding, flocking, aimed feeding, kin
  sparing, rhythms, freezing, warning colours).
- **Looping in method.** The same move repeated seven times: add a
  sense or action, run 24 paired seeds, get a null, keep it "as information".
  Only the compass came with a diagnostic first (`east.js`); no other
  addition changed behaviour.
- **Genome bloat.** The brain went from 30 senses and 6 outputs (NG 485) to
  39 and 9 (NG 752), mostly weights with no shown function. Every change to
  the layout moved the baseline (AL, AS, AU, AV, AX, AZ).
- **Wrong horizon.** Defaults were changed on 400k-tick evidence (compass
  on) and reversed after 1M-tick runs showed the compass halved predator
  persistence. The core outcome, predators that persist, was never
  measured at 1M before a default changed. Over the day it went 10 of 10
  (old build) → 4 of 12 (then-current) → 9 of 12 (now). There is no net gain on
  it, and it was nearly lost.
- **Real gains.** Sexual species and a browser/grazer niche split, the
  cannibalism finding, the diagnosis of long-run collapse (giant grazers,
  streaming), streaming as an option, and the tooling (paired tests, nulls
  such as `kinNear`).

Rules from here:
1. No new sense or action without a hand-built diagnostic first showing
   that the behaviour it would enable pays.
2. A default changes only after 1M-tick paired runs that include predator
   persistence, not just 400k.
3. Test whether the added null inputs cost anything (lean build against
   current at 1M). Prune them if they cost, or if nothing needs them.
4. Stay on the open core problem, predators that never come back after a
   collapse, until it is understood.

## Running now

**Nutrient loop: predators lost** (`v1-NU-*`, 24 paired seeds, 1M). With it on
(`soil0` 6) predator worlds 7 against 19 (p < 0.001), persisting 8 against
17, animals 796 against 1006 (p < 0.001), prey clump less (0.69 against
0.83). Rich soil (`soil0` 12): 11 against 19 (p 0.077). The fruit gene rose
in all 24 worlds with the loop (0.43). Why: 80% of the nutrient ends in the
soil and 17% in plants (plant mass a third of base). Animals carry it from
where they eat and drop it as dung where they graze, so it piles up in grazed
cells (soil about 6 against 1–2 under full plants; seed 1301 at 150k), where
plants regrow slowly however rich the soil, because growth is logistic from
the biomass left. The rest of the map runs dry. Off by default.
Two fixes tried locally (seed 1301, mean over 100–200k; base: plant mass
16420, animals 1553, meat 25%): loop 4341 / 421 / 16%; dung passed over
~200 ticks (`dungRate` 0.005) 3967 / 610 / 7%; regrowth from the roots
(`resprout` 1) 3352 / 683 / 12%. Soil still holds 75–81%: getting nutrient
back into plants needs a large soil pool at any dung pattern, and at `soil0`
6 that pool starves them. Next: abundant nutrient, limiting only locally
(`v1-NU-s24`, `v1-NU-s48`, paired with `v1-LE-base`).

**Nutrient loop** (`nutrients`, new, 0 until tested). Plant growth draws on
the soil of its cell (x soil/(soil + `nHalf`), never more than it holds);
what an animal eats goes into its body; beyond `nBody` x mass it passes as
dung (`dungRate` of the surplus per tick) where it walks; corpses (as they
rot), rotting fruit, dieback and displaced plants return to the soil, which
seeps slowly (`soilDiff`). Total nutrient is conserved to 1e-14. At 100k
ticks (seeds 3, 4): soil patchy (CV 0.7–1.2), plant mass and animals about
30% lower, meat share lower. Paired test at 1M: `v1-NU-on` and `v1-NU-rich`
(`soil0` 12) against `v1-NU-base`, seeds 1301–1324. Expectation in
`ops/queue.json`.

**Lifetime learning** (`learn`, new, 0 until tested; NI 51, NO 10; the owner
asked for the full version). Every brain weight moves by `learnRate` x m x
(its input's activity) x (its output's activity) at the previous think; m is
the brain's own tenth output (tanh), a neuromodulator, so when, which way and
how much to learn is genetic. A new sense, felt (the change in reserves since
the last think), gives it something to learn from. For the four mouth urges
an output's activity is the act minus its odds. Animals start from their
genome's weights; nothing learned is inherited or saved; founders start with
m silent. `tools/heredity.js` checks it: over 47,514 births in a learning world
(parents had moved 71% of their weights) every clone's brain genes equal the
parent's genome exactly, no sexual birth took a gene from learned weights, and
after scrambling every living brain the next births' genomes did not move. Cost: 1.7-2x run time per world (the update is bound by memory
writes; learnStep 35% of time against 13% for the forward pass). Log:
`learnM` (mean |m|, logged in every world: with learning off the output
drives nothing, so its drift is the null), `learnDev`, `learnMoved`.
Knockout (scratchpad `learnko.js`, seeds 1001, 1004, 1006, 1013: at 200k
ticks half of all lines lose m, inherited; lines at +80k, without against
with learning): 613 against 14, 780 against 14, 38 against 309, 408 against
925. Mixed: learning lost two worlds outright and won two. (The script's
meat share at 200k read 0 in all four; that was an artefact, a sample taken
right after the engine's own had reset the counters. At 60k the same worlds
had meat 18–27%.) Probe (scratchpad `learnprobe.js`, 60k ticks): learned
weights move the attack urge on contact both ways (0.33 → 0.23, 0.60 → 0.66,
0.04 → 0.48, 0.90 → 0.87): learning does not steadily train hunting out. All
four worlds had meat at 18–27% by 60k. Paired test: `v1-LE-on` against `v1-LE-base`, seeds 1361–1384.

**Smell** (`smell`, NI 50; on by default since the test above). Animals give off scent in
three channels (0.25 + 0.75 x colour tag, x mass^0.75), corpses a fourth; it
spreads and fades on the spatial-hash grid (about 20 ticks). Two nostrils,
ahead-left and ahead-right, read each channel's level and which side is
stronger. It works with the head down and at night, which sight does not.
Paired test: `v1-SM-on` against `v1-SM-base`, seeds 1325–1348.

**Fruit** (`fruit`, new, 0 by default until tested). Plants have a fourth gene,
fruit (initial values 0–0.5). A plant turns `fruitRate` x fruit x biomass into
fruit per tick, up to `fruitMax` of its capacity. Fruit rots (`fruitRot`
0.005 per tick), is worth `fruitValue` 3 times a leaf to the same gut, ignores
plant defence and height, and is eaten before leaves. An animal that eats fruit
swallows the plant's seeds (its four genes) and drops them `gutTicks` 200
later wherever it is; they take root if the ground is open. Nothing says
who eats fruit or where seeds go. Log: `plantFruit` (mean gene), `fruitMass`,
`eF` (energy from fruit), `seedsWind`, `seedsAnimal`. First look (seed 1,
80k ticks): the fruit gene drifts from 0.25 to 0.13, fruit is about half the
plant energy animals take, and 4–20% of new plants come from animal-carried
seeds. Paired test at 1M ticks, 24 seeds: `v1-BF-fruit1` against `-fruit0`.
Expectation: the gene settles low but above 0 where animal dispersal pays.
Within the fruit arm (`v1-BF-fruit1`, 24 seeds, 1M ticks; the paired baseline
is still running): the fruit gene fell in 24 of 24 worlds, from about 0.18
early to a mean of 0.10 in the last half (0.03–0.17). Fruit gave animals 5–42%
of their plant energy. Animals carried 3–49% of new plants (mean 24%). So fruit
is eaten and seeds travel, but fruiting costs plants more than it returns.
Likely reasons: one seed load per 200 ticks however much fruit an animal eats,
and open ground is plentiful near the parent, so distance buys little. Local
test (`runs/fruitdisp` against `runs/fruitnodisp`, `gutTicks` 0 turns carrying
off): if the gene falls as fast without carrying, carrying currently buys
nothing.
Paired result (`v1-BF-fruit1` against `-fruit0`, 24 seeds, 1M ticks): predation
unchanged (meat 18.3% against 18.0%, predator-dominated 14 against 16,
persisting 15 against 17). Prey clump more with fruit (0.87 against 0.80, 18
of 24, p 0.023), likely gathering at fruiting plants. Carnivore clusters 8
against 4 (p 0.39). Fruit stays off by default while the gene declines.
Carrying test (local, seeds 1101–1102, 300k ticks): the fruit gene follows the
same path with carrying (0.19 → 0.11–0.14) as without (0.18–0.21 →
0.09–0.15). Carrying buys a plant nothing: grazing opens ground everywhere,
so wind seed finds room nearby and distance gains nothing. New physics `jc`
(Janzen–Connell, off by default): a seed takes root with chance 1 − `jc` x
(share of its 8 neighbours that are plants of its own kind, plant genes
within 0.15). Specialised enemies near parents are the usual reason
dispersal pays in nature. Log: `plantDiv` (mean sd of the four plant genes).
Local test: `runs/fruitjc` (`jc` 0.8) and `runs/fruitjcnodisp` (`jc` 0.8,
no carrying). Expectation: with carrying the fruit gene holds or rises;
without carrying it falls; plant diversity rises under `jc`.

Fruit and jc on Actions (12 seeds, 400k ticks). With carrying (`v1-BJ-fjc`) the
fruit gene went 0.197 → 0.130; without carrying (`-fjcnd`) 0.182 → 0.085. It was
higher with carrying in 9 of 12 pairs (+0.045, p 0.15) but fell in every world.
Carried seed made up 10% of new plants and fruit 29% of animals' plant energy.
Carrying now helps a little, not enough to pay for the fruit. Fruit without `jc`
(`v1-BJ-f`, carrying on) also ends at 0.130, so `jc` is not what helps. The
comparison with the no-carrying arm mixes `jc` and carrying, so carrying's
share is not isolated. `jc` alone (`v1-BJ-jc` against `-base`): plant
diversity 0.185 against 0.171 (7 of 12 higher, p 0.77), plant mass 14.5k
against 20.8k (p 0.15), predator-dominated 5 against 9 (p 0.29). It does not
do what it was for. Next:
`fruitPerSeed` 0.2 (2.5 times the seeds per fruit), `v1-BK-fjc02` against
`-fjcnd02`, 24 seeds.

**Over 3M ticks the mutualism deepens** (`v1-BM-fruit3M`, 12 seeds, fruit with
carrying). The fruit gene climbed from 0.196 to 0.680 (up in 11 of 12 worlds).
Carried seed grew 69.5% of new plants, so most plant reproduction runs
through animal guts. Fruit was 35% of the animals' plant energy, and plant
diversity 0.198. Predators: 18 exits, 12 re-entries, persisting in 7 of 12.
The no-fruit 3M worlds on the same seeds (`v1-BE-3M`, older build) had 14 and 7,
and 6 of 12: more comebacks with fruit, suggestive only. The fruit build's
predator persistence at 1M ticks, pooled (`v1-BN-default`, `v1-EG-base-1161`,
`-1173`): 37 of 48 (77%), against 47 of 72 (65%) before fruit.

**Fruit is on by default** (2026-09-27, `fruit` 1, `fruitPerSeed` 0.2, `jc` 0). At
1M ticks (`v1-BL-fc` against `-fnc`, 24 paired seeds, no `jc`), the fruit gene
went 0.194 → 0.250 with carrying and ended higher than it started in 11 of 24
worlds. Without carrying it went 0.184 → 0.075, higher in none. Carried seed
made up 30% of new plants, and fruit 29% of animals' plant energy. Against
no fruit at all (`v1-BF-fruit0`, same seeds, bit-identical build with fruit
off), predators persisted in 19 of 24 against 17, predator-dominated 20 against
16, and meat 20.8% against 18.0%; nothing significant, nothing worse. `jc`
is not needed. Fruit shows on the page as a pink blush on plant cells, with
a legend entry and an on/off in the world drawer.

With `jc` 0.8 at 1M ticks (`v1-BL-fjc` against `-fjnc`, 24 seeds) the fruit gene
went 0.200 → 0.348 (up in 17 of 24), carried seed 37.5%, plant diversity 0.203
against 0.156 without carrying. Against carrying without `jc` (`v1-BL-fc`), paired:
fruit gene +0.099 (16 of 24, p 0.15), diversity +0.022 (15 of 24, p 0.31),
predator-dominated 16 against 20 (p 0.34). Not significant, so `jc` stays off.
Replication on 24 more seeds (`v1-BN-jc` against `-default`, 1125–1148): the fruit
gene was lower with `jc` (−0.09, 8 of 24). Pooled over 48 pairs: fruit gene
+0.006 (24 of 48), diversity +0.016 (p 0.47), meat +0.013. Null, so `jc` was
pruned (bit-identical at 0). The plant diversity log stays. The first evergreen block on
the fruit build (`v1-EG-base-1161`) kept predators in 11 of 12 worlds.

**Seed carrying selects for fruit** (`v1-BK-fjc02` against `-fjcnd02`, `fruit` 1,
`jc` 0.8, `fruitPerSeed` 0.2, 24 paired seeds, 400k ticks). The fruit gene was
higher with carrying in 20 of 24 pairs (+0.061, sign test p 0.0015): 0.200 →
0.148 with carrying, 0.184 → 0.087 without. It rose again late in some worlds
(s1101: 0.24 → 0.13 → 0.20) and ended above its start in 3 of 24. Carried
seed made up 17% of new plants, fruit 28% of animals' plant energy. Animals
carrying seed now select for plants that feed them: a mutualism that no
rule states. A 2x2 at 1M ticks (carrying x `jc`, `v1-BL-*`, 24 seeds each)
tests where the gene settles and whether `jc` matters.

`v1-BI-3Mb` (12 more seeds at 3M ticks, defaults): 14 exits, 5 re-entries;
predators persisted in 2 of 12. Over 3M ticks predators come and go.

`mutSd` 0.16 (`v1-BH-mutsd16`, 12 paired seeds, 1M ticks): predators persisted
in 5 of 12 against 9, predator-dominated 4 against 10 (p 0.11), meat 13.4%
against 19.3%. Mutation load costs the specialists most.
Fruit-fed prey may support more predators (meat share up), and plant cover
may change. A fruit sense for animals comes only if this shows fruit matters.

See `OPS.md` (operating modes) and `ops/queue.json` (what runs next).

**Predators do come back, given time; bigger mutation steps raise the
turnover** (2026-09-27):
- `v1-BE-3M`, 12 seeds (1201–1212) at 3M ticks, defaults: 14 exits from the
  predator state and 7 re-entries after an exit. Predators persisted in 6 of
  12 for at least 64% of the run. A second origin is rare over 1M ticks and
  real over 3M. The valley (`valley.js`) is crossed, slowly.
- `v1-BE-mutsd12` (`mutSd` 0.12 against 0.08, 12 paired seeds, 1M ticks): 6
  re-entries against 1 and 12 exits against 6. **Not replicated**
  (`v1-BH-mutsd12b`, seeds 1113–1124: 1 re-entry against 4, 8 exits against
  11, persistence 7 against 6). Treat as noise. Persistence is unchanged (9 of
  12 in both), with predator clumping higher (2.71 against 1.88, p 0.039).
  Bigger mutation steps cross the valley more often, and they also lose
  predators more often.
- The default's persistence, pooled over 36 worlds at 1M ticks (`v1-BC-s1c0`,
  `v1-EG-base-1113`, `-1125`): 23 of 36 (64%). The first 12 (9 of 12) were a
  lucky draw.

**A bigger world does not keep predators longer** (`v1-BG-grid96`, 96 x 96
against 64 x 64, 12 paired seeds, 1M ticks): predator-dominated 7 against 7,
persisting 9 of 12, meat 17.6% against 15.8%; nothing significant. Pooled
persistence of the default build at 1M ticks: 47 of 72 (65%).

**A lower size cap hurts predators** (`v1-BE-sizemax8`, `sizeMax` 8 against 12,
12 paired seeds, 1M ticks). Expected: fewer giant-grazer escapes. Wrong: predators
persisted in 6 of 12 against 9, with 11 exits against 6 and predator-dominated
worlds 5 against 10 (p 0.062). The cap binds hunters, who must outsize their
prey, more than it stops grazers outgrowing them. `sizeMax` stays 12. Both arms
show a rare re-entry into the predator state after an exit (2 and 1), so a
second origin is possible, only rare.

**The added inputs cost nothing** (`v1-BD-lean`, build e784265 with 30 senses and
6 outputs, sexual, against `v1-BC-s1c0`, the current build with the compass
off; 12 paired seeds, 1M ticks): predators persisted in 9 of 12 in both, meat
21.9% against 19.3%, nothing significant. The null inputs stay.

**After a collapse the ecology still supports predators; evolution cannot find
them again** (scratchpad `regrow.js`). Worlds that lost their predators are
replayed to 1M ticks and run 150k more three ways. Seeds 1102, 1105, 1109,
1111, 4 of 4 alike:
- as is: meat 4.8–10.3%;
- 60 evolved meat-eaters injected: meat 22.4–33.9%, 1–2 carnivore clusters;
- 60 random-brain founders injected: meat 5.9–10.9%, no cluster.

Which step is missing (scratchpad `valley.js`, same four collapsed worlds on
the pre-fruit build, 60 injected animals each, 150k ticks). Resident grazers
given only the hunters' mean diet reached 5–13% meat. Diet plus weapon, armour
and size reached 5–19%. A hunter's brain in a grazer's body reached 5–11%.
A hunter's whole body (all 17 genes) with a grazer's brain reached 5–18%.
Whole hunters reached 20–34%, with carnivore clusters. Neither the body nor
the brain founds a predator line alone; they have to change together, a
valley that single mutations do not cross. At a world's start, the random
founders are diverse enough to cross it at once.

So the barrier is re-origination. At the start of a world, predation arises
from a diverse random population. After a collapse the grazers are one kind,
and the steps from grazer to hunter (diet, weapon, size, strike urge
together) are not taken.

Local batches: `tools/batch.sh <label> "<k=v,...>" <ticks> <seeds...>`
runs 4 at a time on a frozen copy of the build (editing `evosim.html` mid-batch
is safe) into `runs/<label>/`; a 400k-tick small world takes ~10 minutes on one
core, so local batches beat Actions for anything under ~20 worlds.

## Recent results (2026-09-26/27, newest first)

**Owner's direction (2026-09-27).** Keep the shape of the app: plants and
animals stay separate kingdoms, bodies stay one template with gene dials.
Add realism where it can unlock behaviour: smell, a nutrient loop, speed.
Lifetime learning only if cheap (the brain is about 25% of run time).

**Nutrient loop with abundant nutrient is harmless** (`v1-NU-s24`, `soil0`
24, against `v1-LE-base`, seeds 1361–1384, smell off). Predator worlds 15
against 16, meat 17.2% against 18.0%, animals 914 against 1007 (p 0.064),
plant mass 10098 against 11642 (-13%). Soil patchiness (CV) 0.56: dung and
carcass patches form. Soil holds 88% of the nutrient: it limits growth only
where it runs low. At `soil0` 48 (`v1-NU-s48`): predator worlds 12 against
16 (p 0.42), animals 1026 against 1007, meat 16.6% against 18.0%: no
difference at 24 seeds either. Confirming on the smell default (`v1-NU24-1457`, `-1469`,
paired with the standing blocks of the same seeds) before turning it on.

**Fruit scent** (`smellFruit`, new, 0 until tested; NI 53). Ripe fruit gives
off scent into a fifth channel (`fruitEmit` 3 per unit of fruit per tick);
two nostril senses read its level and side. At 20k ticks (seed 3) fruit scent
per bucket runs 0.3 (p10) to 3 (p90), max 10: fruiting patches smell ten
times stronger than bare ground. Question: does sensing fruit from afar let
seed-carrying pay the plants, which fruit sight (seeFruit) did not? Paired
test `v1-SF-*` against standing blocks of the same seeds on this build.
**Result, 24 pairs (`v1-SF-2513`, `-2525`): fruit scent collapses the
mutualism.** Fruit gene at 1M 0.10 against 0.29, lower in 22 of 24 (p
0.00004); fruit's share of plant-eaters' energy 12% against 30% (21 of 24);
carried seed 14% against 37% (20 of 24). Grazers do steer toward fruit scent
(toward in 14 of 24, away in 1). `smellFruit` stays off. First half
(`v1-SF-2513`): the opposite of the expectation. Fruit gene 0.19 →
0.10 (up in 2 of 12) against 0.33 on the same seeds, fruit's share of
plant-eaters' energy 14% against 29%, carried seed 13% against 42%, animals
864 against 1040. A guess, untested: the scent advertises the whole plant, so
plant-eaters drawn to it crop its leaves too, and fruiting stops paying.

**Compass on the smell default** (`v1-CP-2321`, `-2333`, `compass` 1, paired
with the standing blocks of the same seeds, 24 pairs, `smellDecay` 0.1). Prey
stream in every world: polarisation 0.42 and 0.34 against 0.03, alignment 0.30
and 0.23 against 0.07. Predators persist in 13 against 18 (pair one 5 against
10, p 0.031 for predator worlds; pair two 8 against 8). Before smell it was 10
against 20 of 24. The compass still costs predators, perhaps less; the
compass stays off by default.

**Shorter-lived scent is the default** (`v1-SD10-1841`, `-1853`, `-1985`,
`-2021`, `smellDecay` 0.1 against 0.05, paired with standing blocks of the
same seeds, 48 pairs): alignment 0.080 against 0.047, higher in 32 of 48
(p 0.029); predator worlds 33 against 27, carnivore clusters 14 against 11,
meat 17.7% against 15.5% (n.s.). With 0.02 alignment fell. Scent that fades
in about 10 ticks marks where others are now, and grazers steer off it.
`smellDecay` is now 0.1. The fifth pair (`v1-SD10-2129`) agreed: alignment
0.073 against 0.043 (8 of 12), predators 8 against 8; over 60 pairs 40 higher.
Watch: the first five standing blocks on the 0.1 default (seeds 2177–2236)
kept predators in 39 of 60 (65%) against 76% on 0.05, about two standard
errors low, though the same-seed pairs showed no cost (33 against 27). After
nine blocks (to seed 2284): 75 of 108 (69%); fourteen (to seed 2344): 119
of 168 (71%); 24 blocks (to seed 2464): 199 of 288 (69%) against 228 of 300
(76%) on 0.05, about 1.9 standard errors. The same-seed pairs point the other
way (0.1 44 of 60, 0.05 36 of 60). More pairs, 0.05 against the 0.1 default,
running (`v1-SD05-*`). First (`v1-SD05-2573`): predators persisted 10 on 0.1
against 4 on 0.05 (predator worlds p 0.031), alignment 0.084 against 0.059.
The block gap looks like seed noise. All three reverse pairs: persisting 23
on 0.1 against 21 on 0.05, alignment higher on 0.1 in all three. With the five
forward pairs: 67 of 96 against 57. Settled: 0.1 stays.

**Smell over 3M, second block** (`v1-SM-3M-b`, seeds 1901–1912): predators
persist in 7 of 12, 16 exits and 13 re-entries. Pooled with `v1-SM-3M`: 31
re-entries in 24 worlds against 12 in 12 without smell (`v1-BP-3Mdefault`),
persistence 14 of 24 against 8 of 12. Predators come back after a collapse at
about the same rate per world (1.3 against 1.0); not a clear change.

**Smell over 3M ticks** (`v1-SM-3M`, seeds 1613–1624). The grazing fronts
hold but do not grow: alignment 0.047, 0.042, 0.039 in the three millions
(best world 0.134 at the end), against 0.008, 0.000, 0.002 without smell
(`v1-BP-3Mdefault`). Expected a rise past 0.08; it plateaus. Predators persist
through 7 of 12 runs (8 of 12 without smell); 22 exits and 18 re-entries
against 15 and 12, so predators come back more often (n.s. at 12 worlds).
Fruit gene 0.20 → 0.56, 59% of new plants from carried seed.

**Longer-lasting scent does not help** (`v1-SD02-1649`, `-1661`, `smellDecay`
0.02 against 0.05, paired with the standing blocks of the same seeds, 24
pairs). Alignment lower in both halves (0.031 against 0.053, 0.047 against
0.070; 10 higher, 14 lower, n.s.), carnivore clusters 8 against 14, predator
worlds 20 against 17, meat the same. Old trails add noise; the fresh signal
is what grazers steer by. Shorter scent (`smellDecay` 0.1) next (`v1-SD10-*`).

**Predator persistence, pooled standing blocks** (digest measure, predK at
least 64% of the run after bootstrap, 1M ticks): before smell 144 of 192
worlds (75%), on the smell default 111 of 144 (77%).

**Nutrient loop stays off** (`v1-NU24-1457`, `-1469`, `soil0` 24, smell on,
against the standing blocks of the same seeds, 24 pairs). Carnivore species 3
against 12 (p 0.004), kill share 11.0% against 14.0% (p 0.023), animals 925
against 995 (p 0.023), prey clumping 0.76 against 0.89 (p 0.007), predators
persisting 11 against 19, alignment 0.043 against 0.057 (n.s.). With smell
off (`v1-NU-s24`) the direction was the same but smaller (carnivore species 4
against 7). Even with abundant nutrient, a closed loop costs meat-eaters:
plant growth is a little lower everywhere, and the soil's patchiness does not
pay it back. The loop stays an option in the drawer.

**Evolved start refreshed** (2026-09-28): the page's evolved start is now
`v1-SM-on` seed 1335 at 1M (325 genomes), the smell world with the strongest
grazing fronts (alignment 0.18), predators throughout, meat-eaters that turn
toward carrion scent. Loaded in the page it shows alignment 0.12 within 2k
ticks. The old one (seed 1104) had no smell weights.

**Engine speed, tried** (2026-09-28): in `sense`, reusing the tag distance and
size ratio per neighbour and caching each heading's cos and sin gave
bit-identical worlds and no measurable gain (66 s against 64 s for 40k
ticks); V8 already folds them. Reverted. The big gain was 4 worlds per
Actions job.

**Lifetime learning: active, costly, no gain in predation** (`v1-LE-on`
against `v1-LE-base`, seeds 1361–1384, 1M, smell off in both). Learning stays
in use: adults' weights sit 0.27 from their genome on average and 41% have
moved by more than 0.1, the same at 100k and in the second half, in every
world (0.37–0.44). `learnM` does not separate the arms (0.879 against 0.875):
the unused output drifts to large values too, so it is no null. Effects: prey
clump more (1.08 against 0.89, 21 of 24, p < 0.001), meat-eaters clump more
(4.36 against 2.22, p 0.023), everyone moves slower (prey 0.26 against 0.31,
p 0.007; meat-eaters 0.29 against 0.48, 23 of 24), fewer animals (818
against 1007, p 0.007), less fruit in the diet (15% against 24%). Predator
worlds 18 against 16, meat 18.1% against 18.0%, carnivore clusters 3 against
7 (n.s.). Slower animals stay nearer their kin, so the clumping may come from
the slowing, not from seeking company; untested. It costs 1.7–2x run time.
Stays off by default.

**Smell makes grazing fronts; on by default** (`v1-SM-on` against
`v1-SM-base`, seeds 1325–1348, 1M). Moving prey neighbours head the same way:
alignment 0.069 against 0.007, higher in 21 of 24 (p < 0.001), rising over
the run (0.014 at 50–250k, 0.06–0.08 after 250k; best worlds 0.13–0.18).
Prey clump more (0.93 against 0.86, p 0.064), prey and predators move faster
(p 0.064). Predator worlds 19 against 16, meat 19.1% against 19.4%, carnivore
clusters 2 against 5 (n.s.). Mechanism (`tools/smell.js`): grazers turn away
from animal scent in 24 of 24 worlds (mean -1.54 of a possible -2; -0.11
where the senses read 0), their own kind's and others' alike, so they steer
off ground others have been on; neighbours fleeing the same trail travel
together. Meat-eaters' response to carrion scent is mixed (toward in about
half). The first local alignment in this engine: sight-based flocking was
null. `smell` is now 1.

**The default over 3M ticks** (`v1-BP-3Mdefault`, seeds 1213–1224, fruit and
fruit senses on). The fruit gene climbs 0.20 → 0.71, up in all 12 worlds, and
72% of new plants grow from animal-carried seed: over 3M the mutualism takes
over whether or not animals see fruit. Grazers steer toward fruit in 6 of 12
(mean +0.46). Predators persist through 8 of 12 runs; 15 exits and 12
re-entries across the 12, so over 3M predators come and go rather than
vanish. Meat share 14.3%, carnivore clusters at the end in 1.

**Fruit senses work as behaviour, not for the plants** (`v1-BO-see1` against
`v1-BO-see0`, 24 seeds, 1M). Grazers evolve to turn toward fruit in 17 of 24
worlds (`tools/herd.js` fruit probe, mean +0.40 against -0.09 where the senses
read 0). But fruit's share of plant-eaters' energy is unchanged (26.5% against
27.3%), and the fruit gene rises less (0.31 against 0.44 at 1M; higher without
the senses in 17 of 24, p 0.064), with less seed carried (34.5% against
46.9%, n.s.). Meat share 21.4% against 16.3% (p 0.064), carnivore clusters in
9 worlds against 4. Predators persisted in 20 against 19. Seeing fruit stays
on: it is a sense animals have, and fruit-seeking now evolves. Plants being
sought out does not pay them more; a guess, untested: seekers feed in full
fruiting cells and drop seed where cells are full.

**Memory** (2026-09-27): two more brain outputs whose values (tanh) come back
as inputs at the next think, 0 at birth (NI 39, NO 9). Until then the brain
was purely feedforward.
Knockout (scratchpad `memko.js`, current defaults, seeds 1001, 1004, 1006,
1013; at 200k ticks half of all animals lose the weights from their memory
inputs, inherited, lines followed through the mother): the cut lines were
nearly or entirely gone within 60k ticks in 3 of 4 worlds (7 against 673, 0
against 888, 0 against 1207). They won in one (517 against 29). By 200k ticks
most worlds' brains lean on their memory.
Paired test (`v1-BB-mem1` against `v1-BB-mem0`, inputs read 0, 24 seeds):
nothing significant at the world level. Prey clumping 1.195 against 1.121
(p 0.064); predator worlds 19 against 16. `tools/memory.js` shows selection
acting on it. The memory units' own drift from step to step with nothing
happening ("clock") is 0.161 in grazers against 0.283 where the weights are
unselected: evolved brains hold a steadier state rather than a rhythm. A scare
lingers into the next step about equally in both (0.140 against 0.147). The
switch is removed (always on).

**Long worlds lose their predators** (`v1-BA-long`, 12 seeds 1101–1112, 1.6M
ticks, defaults of the time: sexual, compass, colour and heading senses,
give; no memory). Every world had a predator phase early: meat 12–36% of
intake in the first 200k ticks, carnivore clusters in 7 of 12. Then 9 of 12
left the predator state (predK 95–731 thousand ticks) and settled at 5–12%
meat with no carnivore cluster. Three held to the end (s1102, s1106, s1110;
18–27% meat), with carnivore clusters coming and going. Grazers shrank to
size 0.3–1.6. Streaming held in most worlds (`polar` 0.4–0.9). The expectation
(predators hold, as 10 of 10 did to 1M under the older clonal, compass-free
build) was wrong. A 2x2 at 1M ticks on the current build tests which of
today's defaults is responsible: `v1-BC-s1c1` (sex, compass), `-s0c1`,
`-s1c0`, `-s0c0`, 12 seeds each (1101–1112).
Control, the build before those defaults (merged PR #27: clonal, no compass,
30 senses) on seeds 1101–1104, 1M ticks (`runs/oldbuild-long`, local): predators
held in all four (624–940 thousand ticks in the predator state, 0–2 exits,
meat 17–25% over the last half). The current defaults on the same seeds kept
them in one of four (s1102).
Current build, clonal (`sex` 0) with the compass, same seeds, 1M ticks
(`runs/s0c1-local`): predators held in one of four (s1101: 940 thousand ticks,
19% meat). s1102 never entered the predator state, and s1103 and s1104 left it
(5–7% meat late). So clonal reproduction alone does not bring persistence back.

**Result of the 2x2** (12 seeds each, 1M ticks; "persisting" = at least 600
thousand ticks in the predator state):

| arm | persisting | exits | meat | 
|---|---|---|---|
| sexual, compass (`v1-BC-s1c1`) | 4 of 12 | 11 | 14.9% |
| clonal, compass (`-s0c1`) | 6 of 12 | 7 | 17.2% |
| sexual, no compass (`-s1c0`) | 9 of 12 | 6 | 19.3% |
| clonal, no compass (`-s0c0`) | 11 of 12 | 3 | 22.5% |

Paired by seed, pooled over reproduction: without the compass predators
persist in 20 of 24 against 10 (+12/−2, McNemar p 0.013). Predator-state time
is higher in 16 of 20 changed pairs (p 0.012). Reproduction's effect is not
significant (+5/−3 and +2/−0). Streaming prey starve predation over the long
run, even though at 400k ticks the compass arms showed no loss. **The compass
is now off by default** and is a toggle in the page's world drawer. Sexual
reproduction stays the default. The evolved start is now `v1-BC-s1c0` seed
1104 (sexual, no compass, 1M ticks): founded into 8 worlds (4 quantised as the
page stores it), the predators held in 8 (meat 20–34%, 1–2 carnivore clusters).

Motion catches the eye (`stillHide`, tested 2026-09-27, pruned): an animal
moving slower than 0.05 was seen over (1 − `stillHide`) of anyone's range, so
the same rule could hide a freezing prey or an ambushing hunter. `v1-AZ-still5`
against `v1-AZ-still0`, 24 paired seeds: nothing significant. Prey mean speed
0.281 against 0.271, predators 0.382 against 0.372; predator worlds 16 against
13, carnivore clusters 5 against 9 (p 0.34). Grazers' resting throttle was
lower (0.20 against 0.33, lower in 16 of 24, p 0.15). On seeing a big armed
animal they still speed up (0.61) and freeze in none. Streaming prey have to
move to eat, so stillness costs them more than it hides. The switch is
removed; its absence is bit-identical to 0.
`v1-AZ-still0` is the baseline for the current build (37 senses, 7 outputs).

Day and night (`dayTicks`, new, 0 = off): light follows a sine over `dayTicks`
ticks. At full dark animals and corpses are seen over `nightSight` (0.3) of the
sense range, while ears and the plant senses are unaffected. New sense `light`
(NI 37). Logged per row when on: `killsNight`, and mean speed of prey and of
meat-eaters by day and by night (`preySpDay`, `preySpNight`, `predSpDay`,
`predSpNight`). `v1-AY-day` (`dayTicks` 400, several days per lifetime)
against `v1-AY-noday` (0), 24 paired seeds on the same build. Expectation:
kills fall at night at first (hunters hunt by sight). Some worlds evolve a
rhythm: prey slower at night than by day (resting, hidden by the dark), or
predators active at night if calls and short sight suffice. Score: prey and
predator night/day speed ratios and the night share of kills, against the
first 20k ticks.
Result (24 paired seeds): nothing changed at the world level (predator worlds
13 against 13, meat 0.183 against 0.185, prey clumping 1.145 against 1.146).
No rhythm evolved. Prey speed at night over by day was 0.95 in the first 20k
ticks and 0.97 in the last half, lower later in 12 of 24. Three worlds sit
below 0.8, as they did from the start. Fewer kills happen at night (37% in the
last half, under half in 19 of 24; 43% at the start), which is the short
night sight at work, not evolved timing. `dayTicks` stays available, off by
default.

**Feeding** (2026-09-26): a seventh brain output, `give`. When its urge fires
and the attended animal is in reach, the animal passes it energy from its
reserves (`giveRate` 0.1 x mass^0.75 per tick, at most half its reserves; the
receiver gets `giveEff` 0.8). The mouth is busy for that tick. Logged:
`gives`, `eG`, `eGkin` (to look-alikes), `eGjuv` (to juveniles) and `kinNear`
(the share of close neighbours that are look-alikes, the null for `eGkin`).
`tools/give.py` scores it.

Result (`v1-AX-give1` against `v1-AX-give0`, 24 paired seeds): nothing
changed (predator worlds 15 against 15, carnivore clusters 9 against 9, all
else p > 0.3). Giving is selected down, from 1.3–6.0% of intake in the first
20k ticks to a median 0.55% in the last half (5 of 24 above 1%, max 1.8%).
What remains is not aimed. Its kin share tracks `kinNear` (e.g. 97 against 94,
82 against 83, 88 against 97), and its juvenile share (44–69%) looks like the
juveniles nearby. No parental feeding. The action stays available, and the
switch is gone.

**Sparing kin does not pay a meat-eater** (scratchpad `spare.js`; at 200k
ticks the meat-eaters of seeds 1001, 1006, 1013 and 1020 are split in half,
and one half never strikes a look-alike meat-eater, inherited). The sparing
half was gone within 60k ticks in 4 of 4 worlds (0 against 6, 42, 38, 71). The
same rule sparing all look-alikes, prey included, also lost 4 of 4. Young of
their own kind are food worth taking, which is why cannibalism persists.

**Meat-eaters eat their own young** (2026-09-26). Log counters `killsMeat`
(kills whose victim lived mostly on meat) and `killsMeatByMeat` (the killer did
too). `runs/trophic`, seeds 1001, 1006, 1013, 1020, current defaults, last
half: meat-eaters are 2–4% of kill victims. Expectation was that plant-eaters
biting on contact would do most of it. Wrong: meat-eaters made 88–98% of
those kills. A replay (scratchpad `mm.js`, same kill counts as the batch)
of the kills after 200k in seeds 1001 and 1013:

| seed | kills | killer/victim mass, median (quartiles) | victim a juvenile | victim a look-alike |
|---|---|---|---|---|
| 1001 | 3565 | 1.8 (1.2–6.0) | 73% | 71% (colour distance < 0.3) |
| 1013 | 18786 | 2.5 (1.8–24) | 80% | 69% |

The killer is the larger one in about 90% of cases. So it is cannibalism of
juveniles of the killer's own kind, not a third trophic level. No kin
avoidance evolved, even though the attention genes could weight kinship.

Heading sense (2026-09-26): `crowdHeading`, the mean heading of the moving
animals in view relative to the animal's own (NI 36). Without it an animal
could not see which way others face, so the alignment rule of flocking could
not evolve. Tested as a switch, 24 paired seeds each:
- With the compass (`v1-AV-h1` against `-h0`): a tighter shared bearing,
  `polar` 0.777 against 0.692 (p 0.064), `align` 0.594 against 0.485 (p 0.023).
  No local alignment beyond it: `align − polar²` −0.029 in both. Predator
  worlds 14 against 18 (p 0.34), prey clumping 1.14 against 1.05 (p 0.15).
- Without the compass (`-h1c0` against `-h0c0`): nothing. `polar` 0.031
  against 0.033, `align` −0.005 against 0.019 (p 0.15), prey clumping 0.88
  against 0.85.

Flocking does not evolve. Matching neighbours' headings does not pay here,
just as steering toward company does not. The sense stays as information and
the switch is gone.
`v1-AV-h1` is the baseline for the current build (it ran with the sense on).

Predators against streaming prey (`runs/predstream`, local, seeds 1001, 1004,
1006, 1020, current defaults). New log fields: `polarPred` (the meat-eaters'
shared heading) and `predVsPrey` (the cosine between the predators' and prey's
mean headings; −1 = head-on). Expectation: head-on travel (negative) meets
more prey per tick, so predators with their own bearing should evolve it.
Result, the reverse. Last half of each run, samples with more than 5 predators:

| seed | prey `polar` | `polarPred` | `predVsPrey` |
|---|---|---|---|
| 1001 | 0.73 | 0.49 | +0.94 (never negative) |
| 1004 | 0.75 | 0.37 | +0.40 (negative in 24% of samples) |
| 1006 | 0.78 | 0.70 | +0.99 (never negative) |
| 1020 | 0.81 | 0.56 | +0.88 (never negative) |

Predators move with the herd, as wolves follow a caribou migration. A strike
needs the target within reach, so a hunter keeping pace stays in contact,
while a head-on pass lasts a tick. Whether they hold the bearing by compass
or by chasing is not yet separated.

Compass (`compass`, on by default since 2026-09-26): senses compassX/Y (cos and sin of the
animal's heading in world terms, NI 35). `v1-AT-wavec1` against `v1-AT-wavec0`
(`seasonAmp` 0.8, `seasonWave` 1, sexual default), 24 paired seeds.
Expectation: without a compass `waveVx` stays near 0.03 as before. With one,
some worlds evolve a heading bias along the wave and `waveVx` rises well
above 0.1 in the last half. A population moving with the season would also
travel together, which is another route to grouping.
Result, compass in a travelling season (`v1-AT-wavec1` against `-wavec0`, 24
paired seeds, sexual): prey clumping 1.381 against 0.862, up in 23 of 24
worlds (p < 0.001). Prey populations stream along x at 0.2–7.7 times the
wave's speed: with the wave in 18 worlds, against it in 6 (sign test p
0.023). Worlds streaming with it sit deeper in the growth band (`waveTrack`
up to 0.43), those against it the least (0.09–0.14). Carnivore clusters 7
against 12 (p 0.27), meat share 0.169 against 0.206: not significant.

Local preview, compass with no season (`runs/c1`, 4 seeds): prey populations
stream one way. `polar` 0.54–0.86 (about 0.02 without a compass), `align`
0.30–0.73, prey clumping 1.07–1.96. In each world `align` is close to `polar`
squared, which a shared bearing alone produces, so neighbours are not
matching each other. The bearing is inherited and moving straight avoids
re-grazing, so a lineage's direction takes over the population. Parallel
travel keeps relatives near each other. Paired test: `v1-AU-c1` against
`v1-AU-c0`, 24 seeds.

**Result, compass with no season** (`v1-AU-c1` against `v1-AU-c0`, 24 paired
seeds, sexual):
- `polar` 0.728 against 0.035 and `align` 0.551 against 0.017, 24 of 24 worlds.
- Prey clumping 1.223 against 0.841, 23 of 24 (p < 0.001).
- Predator-dominated 16 against 16, carnivore clusters 8 against 8, meat
  share 0.219 against 0.234.

Streaming appears within 40–200k ticks. It is a shared bearing, not flocking.
`align − polar²` averages −0.015 and is positive in 4 of 24 worlds, so
neighbours line up no more than a common direction implies. The bearing is
adaptive, not a mark of common descent (scratchpad `compassko.js`). At 150k
ticks half the grazers lose their compass weights, and the lines are followed
through the mother. In the three worlds already streaming, the cut lines were
gone within 60k ticks (0 against 1679, 0 against 678, 0 against 917). In the
one that was not yet streaming (`polar` 0.11) the cut line won (449 against
175). Moving on in one direction likely keeps an animal off ground its
neighbours and its own line have grazed. The build noise between two
identical-in-effect builds (`v1-AS-base24` against `v1-AU-c0`) was 20 against
16 predator worlds (p 0.29). The compass is now on by default. `v1-AU-c1` is the baseline for the
current build (sexual, compass, 35 senses). The page has a "seasons move:
still / travelling" control next to the seasons slider.

**Migration pays, and needs a compass** (scratchpad `east.js`; evolved start
in a wave world, `seasonAmp` 0.8, clonal; after 20k ticks half the grazers get
+2 x the heading error to east added to their turn, inherited). With the wave,
east-steerers beat the rest in 4 of 4 worlds within 40k ticks (599 against
210, 1227 against 0, 761 against 31, 1350 against 5), with more births per
head. Control, the same world with a season that does not travel: 2 wins, 2
losses (190 against 390, 0 against 361, 531 against 0, 73 against 16). Evolution
cannot find this without a compass. An animal senses nothing about absolute
direction, and the plants it can see (at most 10 units ahead) show no season
gradient through the grazing noise. Local previews of the wave (4 seeds each,
`yearTicks` 6000 and 24000) agree: prey track the band by breeding in it
(`waveTrack` 0.13–0.38) and drift with it at only 0.03 of its speed.

**Travelling season, result** (`v1-AR-wave8` against `v1-AR-glob8`, both
`seasonAmp` 0.8, clonal, 24 paired seeds):
- Giant worlds: 7 against 18 (McNemar p 0.003). A global season makes giants
  in three worlds of four; a travelling one mostly does not.
- Prey clumping: 0.954 against 0.840 (p 0.023).
- Predator-dominated: 10 against 12 (both far below the ~20 of 24 without
  seasons).
- Prey drift along the wave in 21 of 24 worlds (sign test p < 0.001), but at
  only 0.03 of its speed (`waveVx` −0.008 to 0.065). They follow it by
  breeding in it (`waveTrack` 0.07–0.37), not by travelling.

Travelling season (`seasonWave`, new, off by default): with `seasonAmp` > 0 the
season's phase shifts with x, so a band of fast plant growth crosses the world
once a year (256 units per 6000 ticks, 0.043 per tick). Logged: `waveTrack`
(where prey sit in the season, 1 = at the peak) and `waveVx` (prey velocity
along the wave, in units of its speed). `v1-AR-wave8` (`seasonAmp` 0.8,
`seasonWave` 1) against `v1-AR-glob8` (`seasonAmp` 0.8, a global season), 24
paired seeds. Expectation: prey sit ahead of the trough in both. `waveTrack`
above 0 in the wave arm comes from demography alone (more births where
plants grow) and is not migration. Migration is `waveVx` well above 0 across
the last half of the run. That would take steering that tracks plant
gradients over generations, so maybe a minority of worlds. Predator rates may
fall under seasons (bottlenecks).

Colour senses (2026-09-26): the attended animal's colour tag is three senses
(animalR/G/B, NI 33). Before, an animal sensed only how much another looked
like itself. Tested as a switch, `v1-AQ-tags1` against `v1-AQ-tags0` (same
build, inputs read 0), 24 paired seeds, clonal: nothing significant.
Predator-dominated 15 against 18, meat share 0.197 against 0.240 (p 0.15).
`tools/colour.js` finds no warning colours. How well prey colour predicts
armour scatters the same in both arms (R2 0.00–0.60 on, 0.00–0.74 off), and
hunters' colour sensitivity does not line up with armour in either. The
senses are used: in s1022 hunters' strike urge depends strongly on the
target's colour (mean effect 0.76), not in line with armour, which suggests
telling species apart. The senses stay, the switch is gone.

Sexual is now the default (result in the table at the top). The colour and
season arms below were dispatched before the switch and run clonal; they
are paired within themselves. The evolved start keeps its predators with sex
on (4 of 4 worlds, meat 26–34% at 60k ticks against 34–40% clonal).

**Speciation: browsers and grazers.** In the 24 sexual worlds of `v1-AP-sex`,
`tools/gsplit.py` finds plant-eater clusters that cannot interbreed (at
most 5% of cross pairs) in 7. In 4 of them (s1002, s1020, s1022, s1023) the
split is by body size: small grazers (size 0.3–0.9) against large browsers
(2.4–4.8). The large ones breed only at higher reserves (reproT 0.6–0.7
against 0.3–0.4) and give each young more (childE 0.45–0.5 against
0.25). Replays on the build they ran on (scratchpad `browse.js`,
300–400k): in s1020 the large species (mass about 2.7) feeds on plants
0.61–0.69 tall, 30–36% of its feeding on plants taller than a small grazer
reaches (12–13% of plant cells). The small one (mass about 0.3) feeds on
plants 0.11–0.21 tall, 1–6% of it above its reach. That is niche
partitioning by plant height. In s1023 plant height swings widely (27–57%
of cells tall) and both species use tall cells; the large one leans
taller in 4 of 6 samples. In the other three
(s1001, s1012, s1016) the split is mainly in attention genes and colour.
Earlier: sexual worlds on the current physics (`runs/sexH`, seeds
2001–2008, `sex` 1, `mateDist` 0.1, 400k ticks; `tools/isolation.py`, which
now prints size and speed): a meat-eating species that cannot breed with any
grazer cluster (0% of cross pairs) in 7 of 8 worlds. The eighth has no
meat-eaters. This was about a third before plant height. Plant-eaters split
by body size in none. In s2007 the grazers split into two species (0–1% cross
pairs, by body distance alone; colour tags would allow all of them). One is
armed (weapon 0.17–0.25) and high-detox (0.87–0.98), with short sight (3.1–3.6)
and attention turned away from kin and weapons. The other is unarmed
(0.02–0.08), lower-detox (0.63–0.66) and sharper-eyed (5.2–5.6), and attends
to kin. A replay (scratchpad `niche.js`) shows a replacement, not two
niches. The low-detox species was 5% of grazers at 240k and 1% at 280k,
then grew to 68% by 400k as mean plant defence fell from 0.26 to 0.09.
What the two ate barely differs: defence 0.12 against 0.10, height 0.78
against 0.58 of reach. A cheaper species that could not interbreed with
the old one took over once detox stopped paying. Partial isolation between grazer
clusters (19–25%) in s2006.
Earlier: speciation is real in sexual worlds (0% interbreeding between a meat
cluster and grazer clusters). With plant height, check whether browsers and
grazers split into species too.

## Next

1. **Predators after a collapse never come back.** With the defaults, 9 of 12
   worlds keep predators for most of a million ticks. The exits seen are a
   giant-grazer escape (s1109: grazers 0.4 → 5.2 in 50k ticks) and
   streaming (compass on). After an exit no world has re-evolved predators
   within the run, although from random brains they appear within
   20–130k ticks. Worth finding out what blocks the second origin.
2. **Streaming with predators.** With the compass on, prey stream and
   predation starves over the long run. Is there physics under which
   predators keep up with a stream (e.g. what a moving prey is worth, or
   how far a hunter can see ahead)?
3. **Settled, null in this physics** (each paired over 24 seeds): herding
   by seeking company, flocking by alignment, aimed feeding (the give
   output), sparing kin, daily rhythms, freezing and ambush, warning
   colours. Each needs a benefit from neighbours or from timing that this
   physics does not give.
4. **Phone time.** Predators arrive in 20–130k ticks; the page runs ~200–600
   ticks/s. The evolved start covers the wait.
