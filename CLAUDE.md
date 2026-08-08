# evosim — working rules

Single-file HTML evolution simulator. Two kingdoms, plants and animals, both
with a genome of continuous traits inherited with mutation. **Nothing about
behaviour is hardcoded** — herbivory, carnivory, herding, speciation, arms
races all have to emerge from the genes and the physics.

**The mission test: if a result had to be written into the code, it doesn't
count.**

Read `HANDOFF.md` before doing anything. Rationale for every decision is in
`LEDGER.md`, indexed by `[Lnn]` tags that appear in the source.

## Files

| file | what it is |
|---|---|
| `evosim-v0_47_0.html` | the build. Single file, no build step, runs on a phone. |
| `LEDGER.md` | rationale + the version log with predictions and outcomes. |
| `HANDOFF.md` | current state, diagnostic frameworks, prioritized work. |
| `analyze.py` | log digest. `python3 analyze.py log1.json [log2.json log3.json]` |
| `check.js` | correctness harness. `node check.js <build.html>` |

## Hard rules

1. **NEVER run the sim to test a change.** Not headless, not in a harness, not
   "just to see." It is far too compute-expensive, and a short run answers a
   different question: populations shift with every change, so end-state counts
   are not comparable between versions. `check.js` proves the code *resolves*;
   it prints no statistic on purpose. Reason the change through against the
   **last log**, then ship the file. Profiling a *performance* change is the
   one exception, and even then measure a fixed sim-day count, not a tail.
   (This is invariant 6b in the file header.)

2. **Run `node check.js <build>` after every edit.** A syntax check is not a
   correctness check and a call check is not an identifier check.

3. **One structural change per version, with a written prediction** — falsifiable,
   named genes, named thresholds, across 3 seeds. Then add a row to `LEDGER.md`.
   A missed prediction means the diagnosis was wrong, not that the constant
   needs to be bigger.

4. **Rationale lives in `LEDGER.md`, not in the source.** The source carries a
   one-line summary and a `[Lnn]` tag. At v0.36 comments were 24% of the file,
   paid on every read and every write, and parts had gone stale and were
   contradicting each other.

5. **Never calibrate a constant against a statistic from a broken or superseded
   run.**

6. **Constant changes ship as a CFG patch, not a new HTML.** ~700 tokens:
   `{"kind":"evosim-cfg","formatVersion":36,"version":"<build>","base":"<build>",
   "note":"<diagnosis>","cfg":{...}}`. Loading a file with `cfg` and no terrain
   arrays assigns the constants and rebuilds from seed. Always put the diagnosis
   in `note` so the patch is self-documenting when it comes back inside a log.
   A new HTML is only for a change of *shape*: a formula, a cost curve, a
   mechanism.

7. **Verify a measurement-only change did not alter the RNG draw sequence.**

8. **DO NOT widen a gene bound to fix a pin.** Tried in v0.43, reverted in
   v0.44. A rail moves; it does not go away.

9. **The owner runs the build on a phone** and brings back a JSON log. Keep it
   single-file, no build step, no dependencies, touch-first.

## Before touching a constant

Read `HANDOFF.md` §2 — the pin taxonomy (`p<2` / `p=2` / `p>2`) and pivot
discipline. They are the two things that made the difference in the last chat
and they answer most "why is this gene railed" questions without a run.
