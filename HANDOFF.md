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
optional `set`, and a label; all logs land on branch `results/<label>`.
Roughly 10 ms per tick at 3,000 animals on one core, so 500,000 ticks is about
1.5 hours.

Browser check (Chromium and Playwright are preinstalled):
`require(execSync('npm root -g') + '/playwright').chromium`, load
`file:///…/evosim.html`, wait, screenshot, and collect `pageerror` events.

## Design, and why each piece is the way it is

| piece | how | why |
|---|---|---|
| plants | 96x96 cells; biomass grows logistically; genes: stature (capacity vs growth), defence (shrinks a grazer's bite, costs growth), dispersal | cheap enough that thousands of animals fit; still evolves |
| roots | grazing cannot take a cell below `pRoot`; seeds take over cells grazed below `pTakeover` | efficient grazers otherwise ate the flora to extinction |
| animal body | 17 genes: size, speed, sense, diet, weapon, armour, detox, reproT, childE, 3 colour tags, birthSize, choosy, 3 attention weights | every capability has an upkeep cost that curves up faster than its benefit |
| fixed cost | `upFixed` 0.003 per animal per tick regardless of size | 0.010 gave an interior body size but 0 predator worlds in 20 at 600k ticks; at 0.003 small fast breeders evolve predation, and predation holds size off the floor |
| brain | 22 senses → 8 hidden (tanh) → 5 outputs, plus direct input→output weights | the genome is the behaviour |
| senses | energy, health, hurt, plant ahead-left/centre/right, plant here, plant defence here, the attended animal (direction, distance, relative size, kinship by colour tag, its weapon), nearest corpse (direction, distance), crowding, noise, corpse in reach, attended animal in reach | facts about the world, not advice |
| attention | the 'animal' senses and any strike go to the neighbour with the highest salience = closeness + attSize x relative size + attKin x kinship + attWeapon x its weapon, weights evolvable | the nearest animal was usually a sibling, so a would-be hunter could not single out prey |
| juveniles | top speed x (mass / adult size)^0.5 while growing | with it off, killing vanished in all 6 sweep worlds (on: 2 of 6 kept killing) |
| sex | `sex` 0 by default (clonal). With 1, a breeder recombines with the nearest acceptable adult in sense range (colour distance within both partners' `choosy`), else clones; crossover keeps each neuron's wiring whole | every predator world so far evolved without it; a 2x2 is separating its effect from the fixed cost |
| mouth | three independent urges (eat, prefer meat, strike). Eat takes whatever food is in reach; preference matters only when there is a choice; a strike happens only with an animal in reach | a hard argmax and then a softmax both let selection bury meat-eating, because firing it with nothing in reach cost a meal |
| diet | one axis: plant yield x (1 − diet), meat yield x (0.4 + 0.6 diet) | flesh is easy to digest, cellulose needs a specialised gut |
| corpses | carry flesh (`eMeat` 8 per unit mass) plus the reserves the animal died with; rot slowly | a healthy kill must be worth more than a starved carcass |
| combat | damage = `dmg` x weapon x mass^0.75 x (1 − 0.75 armour); hp = 2 x mass | an equal-sized kill takes ~4 ticks; size protects |
| persistence | `Sim.snapshot()` / `Sim.restore()`; the page autosaves to localStorage every minute and when hidden, and resumes on load | reaching predators takes hours on a phone; genomes are stored at one byte per gene |
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
- **The diet gene lags behaviour.** Even in predator worlds mean diet is
  0.04–0.10: predators are omnivore-gutted killers. A gut shift only pays once a
  lineage gets over ~40% of its energy from meat (linear trade-off, floor 0.4).

- **Evolved brains avoid contact.** Measured by probing brains with synthetic
  senses: they strike 44% of the time when touching another animal, prefer meat
  82% of the time when a corpse is in reach, and turn away from other animals.
  That is why most worlds settle into peaceful, evasive omnivores: contact means
  being bitten.
- **Omnivore hunters can invade.** Hand-built hunters with diet 0.3 persisted in
  a mature world and their diet gene climbed to 0.47, so a gradual path from
  omnivore to carnivore exists in this physics.
- **What did not help:** meatFloor 0 (removes scavenging entirely, meat → 0%), a
  concave diet trade-off, weapon-linked teeth (kills fell to zero), a 0.015 fixed
  cost (bootstrap failures, giant animals).

## A carnivore species evolved (2026-09-25, seed 21, `upFixed` 0.003, `sex` 0)

Reproducible at commit eafc1c4: `node run.js --seed 21 --ticks 240000 --set upFixed=0.003,sex=0`
(later speed changes alter rounding, so the exact trajectory differs at HEAD; the population itself is embedded in the page).

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

This population is embedded in the page ("evolved start" in the world drawer,
600 founders); the carnivores held on in 3 of 4 test worlds, one of them with
predator-prey oscillation (3,520 → 1,076 → 2,911 animals).

The previous default (0.010 with sex) produced 0 such worlds in 20 at 600k ticks
(`results/v1-U-base`), so the defaults were switched.

## The defaults, tested: fixed cost x sex, 10 seeds a cell, 400k ticks (`results/v1-V-*`, `results/v1-U-base`)

| | asexual | sexual |
|---|---|---|
| `upFixed` 0.003 | **6 of 10** worlds predator-dominated (regime 17–81%); **2 of 10** with meat guts (up to 10% of animals at diet ≥ 0.5, peak meat share 50–57%) | 1 of 10 predator-dominated; no gut shift |
| `upFixed` 0.010 | 0 of 10 | 0 of 20 (600k ticks) |

regime = share of post-bootstrap samples with meat above 15% of intake. The
small fixed cost is necessary; clonal reproduction multiplies it. A likely reason
sex hurts: recombination with the herbivore majority breaks up carnivore gene
combinations unless mating is already assortative.

## Herding does not pay in this physics (tested 2026-09-25)

Hand-built test in worlds founded from the evolved predator population: after
10k ticks, half the herbivores got a weight turning them toward the centre of
the animals they can see (the `crowdDir` sense).

- Crowd pull alone: herders went from half the herbivores to extinct within 15k
  ticks in both worlds.
- With `alarm` / `alarmDir` senses (a neighbour under attack, and where) and a
  flee response given to **both** halves: herders still lost, 549 → 44–160 in
  20k ticks, while solitary animals held.

Grouping costs more in shared, depleted plant cells than it returns in early
warning, and a cruising predator that strikes whatever it touches finds a
cluster of easy contacts. The senses stay (they are information, and a lone
animal can use them too); no benefit to grouping has been written in. If herding
is wanted, the physics to try next is predator confusion or satiation (a
predator can only use one kill at a time), not a rule.

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

- `results/v1-U-base`, `results/v1-U-meat10`: 20 seeds each, 600k ticks. The
  question is how often a predator-dominated world appears.
- Locally: the current engine at `upFixed` 0.003 and `sex` 0, the setting of the
  two predator worlds found so far.

## Next

1. Score the U batch by its tail: count worlds that reach >20% meat and hold it.
2. Pick defaults that maximise that rate, then make it faster per tick (fewer
   ticks per generation) so it shows up on a phone within an hour.
3. Grouping: the `clump` index sits near 1 (random) so far. Herding should pay
   under predation through the attended-target mechanics; check it in the
   predator worlds.
4. Speciation: `species` clusters exist (several per world). Check whether they
   are reproductively isolated (choosy) and ecologically distinct.
