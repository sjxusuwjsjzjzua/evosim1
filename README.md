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
- **scavenging and predation**. In about 3 of 4 worlds killing becomes the main
  cause of death and meat is over 15% of all animal energy for most of the run,
  typically 20–30%. Much of the killing is done by plant-gutted animals biting
  whoever they touch, their own kind included;
- **carnivore species**. In about a third of worlds a lineage's gut shifts toward
  flesh (diet gene 0.45–1.0, 75–100% of its energy from meat) and lives
  alongside herbivore species. The predators are big, armed cruisers that strike
  whatever they touch; the herbivores are small grazers that sit still and speed
  up when a big armed animal comes into view;
- **arms races**: armour against weapons, speed against speed, herbivore detox
  against plant defence;
- **vigilance and alarm**: an animal eating has its eyes on the food, so prey
  learn to bolt when their neighbours bolt;
- **calls**: every animal has a voice. Grazers learn to turn away from a call
  (in 11 of 12 test worlds), meat-eaters often learn to home in on one, and in
  some worlds grazers call when a big armed stranger comes close;
- **company**: meat-eaters move in loose groups; in some worlds grazers follow
  their own kind and avoid strangers. Prey rarely form tight herds: in this
  physics a group costs them more than it saves;
- **speciation**: in 13 of 24 test worlds the meat-eaters became a species
  that cannot breed with any grazer, and in 7 grazer lineages stopped
  interbreeding with each other. In one, a
  new grazer species with little detox arose once the plants had lost their
  defences, and it was replacing the old one;
- **streaming herds**: every animal can tell which way it is facing, as with a
  sun compass. Within a few hundred generations a world's grazers share a
  bearing and travel together across the (wrapping) world, keeping off ground
  already grazed. Nothing tells them which way to go; different worlds pick
  different directions. The meat-eaters travel with the herd rather than
  against it. With the travelling season on, most worlds go the way the
  season goes;
- **trophic cascades**: where predators thin the grazers, the plants recover.
- **trees and browsers**: plants grow tall enough to keep their leaves out of
  a small grazer's reach, and bodies grow to reach them.

Not every world gets there: in about one world in four predators never take
hold. Once predators are there they tend to stay: in ten test worlds run for a
million ticks, most still had them at the end, and none collapsed into worlds
of dwarf or giant grazers.

Predators usually need one to three hundred generations to appear. On a phone
that can take a while; **world → evolved start** founds a world from an evolved
predator-and-prey population so you can watch one straight away.

Once past bootstrap, your world is saved in the browser every minute and when you leave the page, and
picks up where it was next time you open it. **world → new world** starts over.

## Controls

- **pause / speed slider**: the slider's right end runs as fast as the device
  can.
- **colour** (the button labelled diet): cycles diet (green plant gut → red meat
  gut), kin (heritable colour) and action (grazing, eating meat, attacking).
- **tap an animal** to follow it and see its genes, diet and kills.
- **tap a number** in the top bar for what it means. A **legend** for the
  current colour mode sits above the graph; tap the graph to fold it.
- **what happened**: firsts and turning points (the first kill, a meat-eating
  species appearing, prey grouping, a crash, calls getting loud) pop up as
  they happen and are listed in the world drawer. They are read off the same
  log the graph uses; nothing in the simulation knows about them.
- a followed animal that dies is explained (killed by #N, old age, starved)
  and the view moves on to its killer or a relative; its relatives get white
  rings.
- **drag** pans, **pinch** or the mouse wheel zooms.
- a faint **tail** behind an animal shows which way it is moving and how fast;
  when a world's grazers share a bearing the tails line up.
- a **blue ring** round an animal means it is calling. Every animal has a voice
  that costs energy and ears that work while it eats; what a call means, if
  anything, is up to evolution.
- **world**: species measured live, physics sliders, world size and
  reproduction (clonal or sexual; each starts a new world), new world, same
  seed, evolved start, save the log.
- **predators** in the top bar counts adults that got most of their lifetime
  energy from meat.
- **groups** in the top bar is how many neighbours a plant-eater has compared
  with a random scatter: 1.0× is random, above it they are in groups.

## For developers

```bash
node run.js --seed 1 --ticks 300000 --every 10000 --out s1.json   # headless
python3 tools/v1score.py s1.json                                   # score a run
```

`HANDOFF.md` has the design and the evidence behind each piece of physics,
`CLAUDE.md` the working rules. `LEDGER.md` and the `evosim-v0_*` files are the
previous engine, kept for history.
