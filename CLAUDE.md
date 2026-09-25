# evosim — working rules

Single-file HTML evolution simulator. Two kingdoms, plants and animals, both
with a genome of continuous traits inherited with mutation. Nothing about
behaviour is hardcoded: herbivory, carnivory, herding, speciation and arms races
have to come out of the genes and the physics.

**The mission test: if a result had to be written into the code, it doesn't
count.** Changing the physics (what meat is worth, how fast plants grow, what a
gut costs) is allowed. Writing in a behaviour or a target population is not.

Read `HANDOFF.md` first: it is short and holds the current state. `LEDGER.md` is
the archive: rationale and history, indexed by the `[Lnn]` tags in the source.
Look things up in it; don't read it end to end.

## Files

| file | what it is |
|---|---|
| `evosim-v0_58_0.html` | the build. Single file, no build step, runs on a phone. |
| `HANDOFF.md` | current state, what is known, what to do next. |
| `LEDGER.md` | archive of rationale and every version's predictions and outcomes. |
| `STYLE.md` | how to write replies, commits and docs. `bash tools/style-check.sh` greps for its banned phrases. |
| `check.js` | smoke harness: `node check.js <build.html>`. Proves it parses and runs, nothing more. |
| `headless.js` | one run outside the browser: `node headless.js --build <html> --seed <n> --days <n> --out <path> [--cfg patch.json] [--max-wall-min <n>]`. Touch `<out>.stop` to end early with a valid log. |
| `experiment.js` | N seeds through `headless.js`, then `analyze.py`. |
| `analyze.py` | digest of one to three logs. |
| `tools/score.py` | scores every log under `runs/*/` on a matched window (default days 400-800). `--pickle` dumps per-run rows. |
| `tools/collect.sh`, `tools/arms.py` | pull result branches into `runs/`; classify a run's arm from its cfg. |
| `cfg-patches/` | CFG patches. A constant change ships as one of these, not as a new HTML. |
| `.github/workflows/experiment.yml` | runs seeds on GitHub Actions, one per job. Each log is pushed to branch `runs/<label>/seed-<N>` as `seed-<N>.json` at the branch root. `schedule:` and `workflow_dispatch` inputs are only read from `main`. |

`runs/` is gitignored and does not survive a container restart. The result
branches do.

## Rules

1. `node check.js <build>` after every edit to the build.
2. Write down what you expect before a batch runs, in `LEDGER.md`, with the
   number that would prove you wrong. One line is enough. Score it when the data
   lands, the same day. Unscored data is the most expensive thing this project
   produces.
3. **Score behaviour, not just genes.** A gene value is not a diet. Check what
   animals actually do (`actGraze`, `actAttack`, `actScav`) and where their energy
   comes from (`ePlant`, `eCarrion`, `eFlesh`). H22 showed a population can carry
   carnivory 0.84 and still graze 99.5% of the time.
4. Constants change by CFG patch. A new HTML is for a change of shape (a
   formula, a mechanism) and bumps the version. Keep the previous build in the
   repo only until the new one is scored, then delete it.
5. Measurement-only changes must not alter the RNG draw sequence. Check on a
   run where the changed code actually executes (animals arrive at day 260).
6. Compare runs on a matched window, never on endpoints of runs of different
   length. Report the tail as well as the median: the interesting worlds are a
   minority.
7. Don't widen a gene bound to fix a pin. See `HANDOFF.md` on pin shapes.
8. The build stays single-file, no build step, no dependencies, touch-first.

## Autonomy

The owner has handed the project over. Make CFG or mechanism changes, run them,
commit, push, and merge finished work to `main` without asking. Stop and ask only
for something with no rollback (deleting result branches, rewriting `main`'s
history). Keep reports short: what happened in the world, the numbers, what's
next.
