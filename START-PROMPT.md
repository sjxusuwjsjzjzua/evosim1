# Starter prompt for a fresh Claude Code session

Only needed if you're bootstrapping a brand-new session with no memory of
this project. If you're continuing an existing chat, you don't need this —
just keep going.

---

You're picking up an existing project: a single-file HTML evolution simulator
where nothing about behaviour is hardcoded — herbivory, carnivory, herding and
speciation all have to emerge from genes and physics.

Read `CLAUDE.md` first (working rules), then `HANDOFF.md` in full (current
state, diagnostic frameworks, prioritized work), then skim `LEDGER.md` — read
its version-log table and the most recent version sections properly, and
treat the rest as a reference to go back to rather than something to read end
to end.

Three things to internalise before you touch anything:

1. **Compute is free, conclusions still need a paper trail.** You can run the
   sim yourself — `headless.js`/`experiment.js` locally, or the `evosim
   experiment` GitHub Actions workflow for real parallelism — without asking
   permission to spend CPU. What still requires a written, falsifiable
   prediction on record *before* the run, and the owner's approval before it
   fires unless it's executing an already-approved plan: see `CLAUDE.md`'s
   "Automated iteration" section for the exact Tier A / Tier B split.
2. **One structural change per version, with a falsifiable written prediction
   across 3 seeds**, then a row in `LEDGER.md`.
3. **Constants ship as a ~700-token CFG JSON patch, not a new HTML.** Only a
   change of shape — a formula, a cost curve, a mechanism — earns a new file,
   and any such change is always gated on the owner's go-ahead before it ships
   or before the run that tests it fires.

Read the current build filename out of `CLAUDE.md`'s Files table rather than
assuming a version number here — it moves every version and this file isn't
updated on that cadence.

When you've read everything, tell me:

- your one-paragraph summary of what this project is trying to prove and
  where it currently stands against that;
- what `HANDOFF.md` §3's Tier 1 currently lists as the most pressing open
  question, and what you'd check first to make progress on it;
- whether that next step is Tier A (you can just run it) or Tier B (you need
  my go-ahead first) — and if Tier B, the exact prediction you're proposing.

Then stop and wait before running anything or changing any code, unless the
next step is Tier A and HANDOFF.md already shows it as approved and queued.

## Useful commands

```bash
node check.js <current-build.html>                     # after EVERY edit
python3 analyze.py log1.json log2.json log3.json
node headless.js --build <html> --seed <n> --days <n> --out <path> \
    [--cfg patch.json] [--progress-days 20] [--max-wall-min <n>]
node experiment.js --build <html> --days <n> --label <name> [--cfg patch.json] [--n 3]
```

## Git and GitHub

Commit, push, open PRs, and merge them yourself — the owner doesn't want to
do backend/git work, only to approve substantive changes. Don't ask
permission for the git mechanics themselves.
