# evosim

An evolution simulator in one HTML file. Open `evosim.html` in a browser,
phone included. There is no build step and nothing to install.

Plants grow, spread and evolve defences on a grid. Animals are born with a small
neural network in their genome. The founders' brains are random. Nothing in the
code tells an animal what to eat, whom to attack, when to run or where to go:
those come from selection, given physics (what food is worth, what a body costs,
what a bite does).

What evolves, without being written in:

- **grazing**, in every world, within a few dozen generations;
- **scavenging and predation**. In about 6 of 10 worlds killing becomes the main
  cause of death, and meat 15–40% of all animal energy;
- **carnivore species**. In about 2 of 10 worlds a lineage's gut specialises for
  flesh (diet gene 0.95–1.0, 94–100% of its energy from meat) and lives
  alongside herbivore species. In the best-studied case the carnivores are big,
  fast, armed cruisers that strike whatever they touch, and the herbivores are
  small, vigilant grazers that watch large strangers and run from them;
- **arms races**: armour against weapons, speed against speed, herbivore detox
  against plant defence;
- **trophic cascades**: where predators thin the grazers, the plants recover.

Predators usually need one to three hundred generations to appear. On a phone
that can take a while; **world → evolved start** founds a world from an evolved
predator-and-prey population so you can watch one straight away.

## Controls

- **pause / speed slider**: the slider's right end runs as fast as the device
  can.
- **colour** (the button labelled diet): cycles diet (green plant gut → red meat
  gut), kin (heritable colour) and action (grazing, eating meat, attacking).
- **tap an animal** to follow it and see its genes, diet and kills.
- **world**: species measured live, physics sliders, world size, new world,
  evolved start, save the log.

## For developers

```bash
node run.js --seed 1 --ticks 300000 --every 10000 --out s1.json   # headless
python3 tools/v1score.py s1.json                                   # score a run
```

`HANDOFF.md` has the design and the evidence behind each piece of physics,
`CLAUDE.md` the working rules. `LEDGER.md` and the `evosim-v0_*` files are the
previous engine, kept for history.
