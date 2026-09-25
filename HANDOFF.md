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
| diet | one axis, concave (`dietCurve` 2): plant yield x (1 − diet²), meat yield x (0.4 + 0.6 (1 − (1 − diet)²)) | flesh is easy to digest, cellulose needs a specialised gut; the concave form made a first step toward either gut cheap and raised the predator rate (16 of 20 worlds against 11 of 20) |
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

## Levers on the predator rate (10 seeds each, 400k ticks, 2026-09-25)

| batch | world | worlds with steady killing | predator-dominated (regime > ~30%) | with meat guts |
|---|---|---|---|---|
| defaults (`v1-W-medium`) | medium | 7 | 3 | 1 |
| defaults (`v1-W-small`) | small | 8 | 6 | 2 |
| defaults + new senses (`v1-X-small-senses`) | small | 7 | 5 | 1 |
| `sex=1, mateDist=0.1` (`v1-W-sex-md10`) | medium | 7 | 4 | **3** |
| `dietCurve=2` (`v1-X-small-curve2`) | small | **10** | **10** | **4** |

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
animal can use them too); no benefit to grouping has been written in.

Predator confusion (`kConfusion`: strike damage / (1 + k x others within 3 of the
target), off by default) was tested too: at k 0.5 and 1.5 herders still fell to
0–51 of ~550 in 20k ticks. Sharing depleted plant cells costs more than any of
these benefits return. Herding would likely need a different plant ecology
(abundant forage in patches, so groups do not starve each other), not a rule.

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

- `results/v1-Y-medium-curve2`: 10 seeds, medium world, `dietCurve` 2. Does the
  concave trade-off help as much in the bigger world?
- `results/v1-Z-small-1M`: 10 seeds, small world, 1M ticks. Do predator worlds
  and carnivore species hold for ~1000 generations, or collapse?
- `results/v1-AA-base`, `-rich` (`pR` 0.024), `-patchy` (`fertNoise` 1): 10 seeds
  each, 400k ticks. Does grouping (`clump` above 1) evolve on its own once
  forage is richer or patchier?

## Next

1. Herding: if neither richer nor patchier forage lifts `clump`, the benefit of
   a group is too small against the cost of sharing forage. Handling time and
   satiety are already physics (a corpse is chewed at `chew` x mass^0.75 a
   tick, intake stops at the energy cap, a strike costs `atkCost`), so a group
   already dilutes a sated predator. What is missing is a reason for prey to
   be near each other that outweighs sharing forage.
2. Speciation under sex: clonal worlds have lineages, not species. With
   `sex=1, mateDist=0.1` clusters are reproductively isolated; check whether
   they split by niche (diet) in the predator worlds.
3. Time to predators: 100–300 generations. Anything that shortens it without
   writing in a diet helps the phone.
