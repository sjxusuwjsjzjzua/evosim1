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
| brain | 30 senses → 8 hidden (tanh) → 6 outputs (turn, throttle, eat, meat preference, attack, call), plus direct input→output weights | the genome is the behaviour |
| senses | energy, health, hurt, plant ahead-left/centre/right, plant here, plant defence here, the attended animal (direction, distance, relative size, kinship by colour tag, its weapon), nearest corpse (direction, distance), crowding, noise, corpse in reach, attended animal in reach, direction to the centre of the animals in sense range, alarm (the strongest hurt among neighbours) and its direction, stomach fill (0 without `gutCap`), mean speed of the animals in view, the loudest call in range and its direction, direction to the centre of look-alikes in view (kinDir) | facts about the world, not advice |
| attention | the 'animal' senses and any strike go to the neighbour with the highest salience = closeness + attSize x relative size + attKin x kinship + attWeapon x its weapon, weights evolvable | the nearest animal was usually a sibling, so a would-be hunter could not single out prey |
| vigilance | an animal that ate last tick senses animals over (1 − `headDown`) = 30% of its range | without it, grouping never paid; with it prey group where predators are (below) |
| plant height | a plant stands `browse` (2) x stature tall; an animal reaches mass^(1/3) and cannot crop the share of the cell's capacity above its reach | without it worlds fell into dwarf grazers on a lawn (16 of 40); with it carnivore specialists evolve in 8 of 12 worlds against 3, though 4 of 12 go giant (below) |
| juveniles | top speed x (mass / adult size)^0.5 while growing | with it off, killing vanished in all 6 sweep worlds (on: 2 of 6 kept killing) |
| sex | `sex` 1, `mateDist` 0.1 by default (2026-09-26). A breeder recombines with the nearest acceptable adult in sense range (colour distance at most 1 − `choosy` for both partners, and genetic distance under `mateDist`), else clones; crossover keeps each neuron's wiring whole | against clonal over 24 paired seeds (`v1-AP-sex`): predator-dominated 20 against 20, carnivore clusters 10 against 12, nothing significant. In 13 of 24 the meat-eaters are a separate species (at most 5% of cross pairs could breed), and in 7 some grazer clusters are isolated from each other. Without `mateDist` sexual worlds fall behind (below) |
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

## Running now

Predators against streaming prey (`runs/predstream`, local, seeds 1001, 1004,
1006, 1020, current defaults). New log fields: `polarPred` (the meat-eaters'
shared heading) and `predVsPrey` (the cosine between the predators' and prey's
mean headings; −1 = head-on). Expectation: head-on travel (negative) meets
more prey per tick, so predators with their own bearing should evolve it.

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
on (4 of 4 worlds, meat 26–34% at 60k ticks against 34–40% clonal). Local batches: `tools/batch.sh <label> "<k=v,...>" <ticks> <seeds...>`
runs 4 at a time on a frozen copy of the build (editing `evosim.html` mid-batch
is safe) into `runs/<label>/`; a 400k-tick small world takes ~10 minutes on one
core, so local batches beat Actions for anything under ~20 worlds.

## Next

1. **Giant worlds: solved** by `browseGrown` (above). Over 1M ticks every
   test world stayed predatory.
2. **Herding: out of reach in this physics** (factorial and diagnostics
   above). Energy, strike cost, chew time, meat floor and size cap all left
   prey clumping at ~0.9. Hand-built herders lose even with free vision. Prey
   do bolt when neighbours bolt, and some turn toward kin, but no world forms
   lasting groups. What might change it: prey that are much denser than
   their sense range (a smaller world per animal), or predators that cannot
   kill again while the group is still near.
3. **Speciation.** Sexual worlds on the current physics (`runs/sexH`, seeds
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
4. **Phone time.** Predators arrive in 20–130k ticks; the page runs ~200–600
   ticks/s. The evolved start covers the wait.
