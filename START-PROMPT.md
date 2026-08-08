# Starter prompt for Claude Code

Drop the whole folder somewhere, `cd` into it, run `claude`, and paste this:

---

You're picking up an existing project: a single-file HTML evolution simulator
where nothing about behaviour is hardcoded — herbivory, carnivory, herding and
speciation all have to emerge from genes and physics. I run it on my phone and
bring back JSON logs; you analyse them and ship the next version.

Start by reading `CLAUDE.md`, then `HANDOFF.md` in full, then skim `LEDGER.md`
— read the version-log table at the top and the "v0.47 — external audit pass"
section at the bottom properly, and treat the `[Lnn]` sections as a reference
you go back to rather than something to read end to end.

Three things to internalise before you touch anything:

1. **Never run the sim to test a change.** Not headless, not "just to see." You
   have node and it will be tempting. `check.js` is the only harness and it
   prints no statistics on purpose. Reason changes through against the last log.
2. **One structural change per version, with a falsifiable written prediction
   across 3 seeds**, then a row in `LEDGER.md`.
3. **Constants ship as a ~700-token CFG JSON patch, not a new HTML.** Only a
   change of shape — a formula, a cost curve, a mechanism — earns a new file.

Current state: **v0.47.0 is unrun.** It's six changes from an external audit —
one bug fix, two biology changes, three performance — with all six predictions
already written into `LEDGER.md`. I haven't run it yet.

When you've read everything, tell me:

- your one-paragraph summary of what this project is trying to prove and where
  it currently stands against that;
- whether you agree with the v0.47 §3 Tier 1 item that the omnivory result may
  be partly an artifact of the arbiter's units, and what in the next log would
  settle it either way;
- the exact run plan you want from me — how many seeds, what CFG patches, how
  many sim-days each, and what you'll check first when the logs come back.

Then stop and wait. Don't change any code yet.

---

## After that first exchange

The natural next moves, in order:

1. **`git init` and commit the package as-is** before anything changes. There is
   no version control on this project yet and it has been iterating for ~11
   versions on a single file. Tag it `v0.47.0`.
2. **Run the two arms** — 3 seeds with `{"cfg":{"k_confusion":0}}`, then 3 seeds
   at the default — and bring the logs back.
3. **Score the six predictions honestly.** A miss means the diagnosis was wrong,
   not that the constant needs to be bigger.

## Useful commands

```bash
node check.js evosim-v0_47_0.html          # after EVERY edit
python3 analyze.py log1.json log2.json log3.json
```
