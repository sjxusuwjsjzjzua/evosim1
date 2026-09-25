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
| animal body | 13 genes: size, speed, sense, diet, weapon, armour, detox, reproT, childE, 3 colour tags, birthSize | every capability has an upkeep cost that curves up faster than its benefit |
| brain | 22 senses → 8 hidden (tanh) → 5 outputs, plus direct input→output weights | the genome is the behaviour |
| senses | energy, health, hurt, plant ahead-left/centre/right, plant here, plant defence here, nearest animal (direction, distance, relative size, kinship by colour tag, its weapon), nearest corpse (direction, distance), crowding, noise, corpse in reach, animal in reach | facts about the world, not advice |
| mouth | three independent urges (eat, prefer meat, strike). Eat takes whatever food is in reach; preference matters only when there is a choice; a strike happens only with an animal in reach | a hard argmax and then a softmax both let selection bury meat-eating, because firing it with nothing in reach cost a meal |
| diet | one axis: plant yield x (1 − diet), meat yield x (0.4 + 0.6 diet) | flesh is easy to digest, cellulose needs a specialised gut |
| corpses | carry flesh (`eMeat` 8 per unit mass) plus the reserves the animal died with; rot slowly | a healthy kill must be worth more than a starved carcass |
| combat | damage = `dmg` x weapon x mass^0.75 x (1 − 0.75 armour); hp = 2 x mass | an equal-sized kill takes ~4 ticks; size protects |
| bootstrap | random genomes arrive while the population is under 200, until tick 60,000 | nothing else seeds behaviour |

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

## Next

1. Find out whether a specialist predator lineage evolves at `eMeat` 8 given
   enough generations (`results/v1-L8`, 12 seeds x 500k ticks).
2. If not, test the gradual path: can an omnivore hunter (diet ~0.3) invade? If
   omnivore hunters fail where specialists succeed, the diet trade-off shape is
   the barrier.
3. Measure more of what should emerge: grouping (crowding when predators are
   present), speciation (clusters in tag and gene space), and a better predator
   metric (lifetime intake per individual is logged; plot its distribution).
4. Sexual reproduction with mate choice, so speciation can be real rather than
   clonal divergence.
