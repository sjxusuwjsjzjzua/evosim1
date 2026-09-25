# evosim — working rules

An evolution simulator in one HTML file. Plants and animals both carry genomes
that are inherited with mutation. **Nothing about behaviour is hardcoded**:
grazing, scavenging, predation, fleeing, herding and speciation have to come out
of the genes and the physics.

**The mission test: if a result had to be written into the code, it doesn't
count.** Changing physics (what food is worth, what a body costs, what a bite
does, what an animal can sense) is allowed. Writing in a behaviour, a diet, a
target or a population cap is not.

Read `HANDOFF.md` first: current state, what is known, what is next.

## Files

| file | what it is |
|---|---|
| `evosim.html` | **the build** (engine 1.x). Single file, no build step, runs on a phone. The `<script id="engine">` block is the whole simulation and never touches the DOM; the second script is the UI. |
| `run.js` | headless runner: `node run.js --seed 1 --ticks 300000 --every 10000 [--set k=v,k=v] [--cfg patch.json] [--out log.json]`. Runs the engine block of `evosim.html` in a vm, so the file on the phone is the file measured. |
| `tools/v1score.py` | one row per log: population, meat share, kill share, predators, diet genes. `python3 tools/v1score.py runs/*.json` |
| `.github/workflows/sim.yml` | the same on GitHub Actions, one seed per job; every log of a dispatch lands on one branch, `results/<label>`. Dispatch with ref = the working branch. |
| `HANDOFF.md` | current state and next steps. |
| `LEDGER.md` | archive of the v0.44–v0.58 program (the previous engine). Read for history only. |
| `evosim-v0_58_0.html`, `headless.js`, `check.js`, `analyze.py`, `tools/score.py`, `tools/arms.py`, `tools/collect.sh`, `cfg-patches/`, `experiment.yml` | the previous engine and its tooling, kept as a reference. |
| `STYLE.md` | how to write replies, commits and docs. `bash tools/style-check.sh` greps for its banned phrases. |

## How the engine works, in one paragraph

Plants are a grid of cells (64x64 in the page, 96x96 headless); an occupied cell has biomass and three genes
(stature, defence, dispersal), grows logistically, keeps an ungrazeable root
reserve, and throws seed into cells grazed below a threshold. Animals are agents
with 17 body genes (size, speed, sense, diet, weapon, armour, detox, three
life-history genes, three colour tags, mate tolerance, three attention weights)
and a neural network (25 senses, 8 hidden,
5 outputs: turn, throttle, eat, meat preference, attack). Each mouth output is a
probability. Eating takes whatever food is in reach and the preference only
matters when both plant and corpse are; a strike only happens when an animal is
in reach. Diet is one axis with a concave trade-off: plant yield x (1 - diet^2),
meat yield x (0.4 + 0.6 (1 - (1 - diet)^2)). A corpse carries its flesh plus the reserves the animal died
with. Attention picks which neighbour the animal senses and strikes; its weights
are genes. Juveniles are slow. Reproduction is clonal by default (`sex` 1 recombines with an acceptable
mate in sense range; `mateDist` adds genetic incompatibility). Founders have a cheap ancestral body and a random brain and keep
arriving until a population establishes. See `HANDOFF.md` for why each piece is
there.

## Rules

1. Run a smoke test after every engine edit: `node run.js --ticks 3000 --every 1000`
   must run clean, and the page must load without console errors (Chromium +
   Playwright are installed; see `HANDOFF.md`).
2. Say what you expect before a batch, and score it when it lands. Score
   **behaviour and intake** (meat share, kills, predators by lifetime intake), not
   gene means alone.
3. Report the tail, not just the median. The interesting worlds are a minority.
4. When selection does nothing, check for a threshold first. Twice now a hard
   choice rule (an argmax) hid every small step from selection.
5. Hand-built brains are allowed as **diagnostics** (does the physics reward this
   behaviour at all?) and never ship.
6. The build stays one file, no build step, no dependencies, touch-first.
7. Don't `pkill -f` a pattern that appears in your own command line; it kills
   the shell. Kill by PID.

## Autonomy

The owner has handed the project over and asked for continuous iteration without
check-ins. Change physics or mechanism, run it, commit, push, and merge finished
work to `main`. Stop and ask only for something with no rollback (deleting
result branches, rewriting `main`'s history).
