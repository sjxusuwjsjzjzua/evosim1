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
Roughly 10 ms per tick at 3,000 animals on one core, so 500,000 ticks is about
1.5 hours.

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
| brain | 25 senses → 8 hidden (tanh) → 5 outputs, plus direct input→output weights | the genome is the behaviour |
| senses | energy, health, hurt, plant ahead-left/centre/right, plant here, plant defence here, the attended animal (direction, distance, relative size, kinship by colour tag, its weapon), nearest corpse (direction, distance), crowding, noise, corpse in reach, attended animal in reach, direction to the centre of the animals in sense range, alarm (the strongest hurt among neighbours) and its direction | facts about the world, not advice |
| attention | the 'animal' senses and any strike go to the neighbour with the highest salience = closeness + attSize x relative size + attKin x kinship + attWeapon x its weapon, weights evolvable | the nearest animal was usually a sibling, so a would-be hunter could not single out prey |
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

## Herding does not pay in this physics (tested 2026-09-25)

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

## Running now

- `results/v1-Z-small-1M`: 10 seeds, small world, 1M ticks. Do predator worlds
  and carnivore species hold for ~1000 generations, or collapse?
- `results/v1-AA-base`, `-rich` (`pR` 0.024), `-patchy` (`fertNoise` 1): 10 seeds
  each, 400k ticks, engine before the audit fixes. Does `clump` rise with
  richer or patchier forage? (Expected no, given the correction above.)
- `results/v1-AB-base`, `-gut2` (`gutCap` 2), `-gut1slow` (`gutCap` 1, `gutDig`
  0.08): 10 seeds each, 400k ticks, current engine. Expected: fewer kills per
  predator with a stomach; if dilution now pays, `preyClump` above 1 in the
  predator worlds.
- Locally: the seed-42 evolved start with and without a stomach, 2 seeds,
  100k ticks.

## Next

1. Herding: predators do not fill up, so a group gives no dilution (above).
   Next physics: a gut. Eating fills a stomach of limited capacity that
   digests into reserves over time, and a sense reports how full it is. Then a
   predator can use about one kill per encounter, and striking while full buys
   nothing but the strike's cost.
2. Speciation under sex: checked on `v1-Y-small-curve2` vs `-sexmd` (10 seeds
   each). A cluster living mostly on meat was present in the last 10 samples of
   4–5 of 10 clonal worlds and 1 of 10 sexual ones. Sex with incompatibility
   does not split niches more readily. Most predator-dominated worlds of either
   kind do their killing inside plant-gutted clusters.
3. Time to predators: 100–300 generations. Anything that shortens it without
   writing in a diet helps the phone.
