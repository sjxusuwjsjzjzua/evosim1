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
| `run.js` | headless runner: `node run.js --seed 1 --ticks 300000 --every 10000 [--cfg patch.json] [--set k=v,k=v] [--out log.json] [--dump genomes.json] [--build file.html]`. `--set` overrides `--cfg`; `--dump` writes the living genomes (for `seedGenomes`). Runs the engine block of `evosim.html` in a vm, so the file on the phone is the file measured. |
| `tools/v1score.py` | one row per log, last half of the run: population, meat share, kill share, predators, diet, regime%, clump, carnivore species. `python3 tools/v1score.py runs/*.json` |
| `tools/paired.py base arm...` | paired comparison of batches on the same seeds, with exact p-values. Change a default only at p < 0.05. |
| `tools/fetch-results.sh [prefix]` | pulls `results/*` branches into `runs/<label>/` (gitignored). |
| `tools/genomes.js` | brain probes of a `--dump`, split at diet 0.3. |
| `tools/batch.sh` | local batch, 4 worlds at a time, on a frozen copy of the build: `tools/batch.sh <label> "<k=v,...>" <ticks> <seeds...>` → `runs/<label>/`. |
| `tools/voice.js`, `tools/herd.js` | brain probes of a dump: what calls mean; whether grazers steer toward look-alikes, everyone, or calls. |
| `tools/colour.js` | does colour mean anything in a `--dump`: how well prey colour predicts armour, and how hunters' strike urge depends on the target's colour. |
| `tools/wave.py` | migration under a travelling season (`seasonWave`): where prey sit in it and how fast they move with it. |
| `tools/isolation.py` | reproductive isolation between the clusters of a `--dump`, by the engine's mating rule. |
| `tools/embed-genomes.py` | embeds a `--dump` as the page's evolved start. Run from the repo root. |
| `README.md` | for people opening the page. |
| `.github/workflows/sim.yml` | the same on GitHub Actions, one seed per job; every log of a dispatch lands on one branch, `results/<label>`. Dispatch with ref = the working branch. |
| `HANDOFF.md` | current state and next steps. |
| `MINING.md` | analysis of 476 run logs (2026-09-26): what predicts predator worlds, how they end. |
| `SURVEY.md` | what other artificial-life systems made emerge and by which physics; ranked engine changes. Some claims are from memory and marked so. |
| `LEDGER.md` | archive of the v0.44–v0.58 program (the previous engine). Read for history only. |
| `evosim-v0_*.html`, `headless.js`, `check.js`, `analyze.py`, `audit.py`, `experiment.js`, `tools/score.py`, `tools/arms.py`, `tools/collect.sh`, `cfg-patches/`, `.github/workflows/experiment.yml`, `AUDIT-*.md`, `HOST-*.md`, `FINDINGS.md`, `PROGRAM-HISTORY.md` and the other upper-case notes | the previous engine, its tooling and audits. History only. |
| `STYLE.md` | how to write replies, commits and docs. `bash tools/style-check.sh` greps for its banned phrases. |

## How the engine works, in one paragraph

Plants are a grid of cells (64x64 in the page, 96x96 headless); an occupied cell has biomass and three genes
(stature, defence, dispersal), grows logistically, keeps an ungrazeable root
reserve, grows up to 2 x stature tall as it grows (never shrinking when grazed; an animal reaches mass^(1/3) and cannot crop what is above its reach), and throws seed into cells grazed below a threshold. Animals are agents
with 17 body genes (size, speed, sense, diet, weapon, armour, detox, three
life-history genes, three colour tags, mate tolerance, three attention weights)
and a neural network (33 senses, 8 hidden,
6 outputs: turn, throttle, eat, meat preference, attack, call). Each mouth output is a
probability. Eating takes whatever food is in reach and the preference only
matters when both plant and corpse are; a strike only happens when an animal is
in reach (the attended one). Diet is one axis with a concave trade-off (`dietCurve` 2, `meatFloor` 0.4): plant yield x (1 - diet^2),
meat yield x (0.4 + 0.6 (1 - (1 - diet)^2)). A corpse carries its flesh plus the reserves the animal died
with. Attention picks which neighbour the animal senses and strikes; its weights
are genes. An animal that ate last tick senses animals over only 30% of its range (`headDown`). A call is heard by every animal in range, heads down or not; it costs energy and means whatever evolution makes it mean. Juveniles are slow. Reproduction is sexual by default (`sex` 1: a breeder recombines with an acceptable
mate in sense range, else clones; `mateDist` 0.1 makes genomes too far apart unable to breed, so clusters become species; `sex` 0 clones). Founders have a cheap ancestral body and a random brain and keep
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
