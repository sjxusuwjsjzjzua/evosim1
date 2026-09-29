# Operations: how the work keeps running

**Current mode: 2** (set by the owner; change only on their word). Paused: no.

The owner wants work to continue in the background without input, at a token
budget they set: mode 1 (low), 2 (value) or 3 (burn). This file is what every session and every
scheduled wake-up reads first.

## Resources

- **GitHub Actions** (`sim.yml`): the repo is public, so minutes are unlimited.
  About 20 jobs run at once across the account; the rest queue. Three quarters
  of that is ours (see the cap below). A runner has 4 cores, so one job
  runs up to 4 worlds side by side (`per_job`, default 4): about 80 worlds at
  once. One world: 400k ticks
  takes 10–25 minutes, 1M takes 25–60, 3M about 2–3 hours (timeout 330 minutes).
  Idle runners are the waste to avoid. On 2026-09-27 they sat idle for 5 hours.
- **Local**: 4 cores (`tools/batch.sh`, replays, diagnostics). Local jobs and
  background watchers die when the container restarts; Actions jobs do not.
- **Tokens**: the owner's budget, set by the mode.

## The queue

`ops/queue.json` holds every planned run, fully specified: label, seeds, ticks,
`--set` string, optional `build_ref`, the baseline it pairs with, and the
expectation, written before it runs (CLAUDE.md rule 2). `tools/ops.py` does the
bookkeeping:

```
python3 tools/ops.py status            # jobs in flight and pending
python3 tools/ops.py next 5            # dispatch inputs for the next 5 entries
python3 tools/ops.py mark LABEL dispatched
python3 tools/ops.py digest            # fetch, score and log whatever has landed (ops/log.md)
python3 tools/ops.py wait              # blocks until something lands (run in the background: it wakes the session)
python3 tools/ops.py evergreen 60      # top up with standing replication runs
```

Dispatch is one `actions_run_trigger` call per entry (ref = the working
branch, workflow `sim.yml`), with the inputs `next` prints.

**Capacity cap, all modes (owner, 2026-09-29):** use at most three quarters of
GitHub Actions. The account runs about 20 jobs at once and the owner's other
simulator (botciv) needs the rest. Keep **at most 60 worlds (15 jobs of 4)
dispatched and not landed**, queued jobs included: a queued job still takes a
slot as soon as one frees. `python3 tools/ops.py room` prints how many worlds
may be dispatched now; dispatch only that many, in whole 12-world blocks, and
never cancel a run whose world jobs are done (it only waits for its collect
step). Keep about 24 worlds pending in `ops/queue.json`. If designed work runs short, `evergreen` adds standing runs:
the default build at 1M ticks on fresh 12-seed blocks. They build up the
sample on the core outcome (predator persistence) and are never wasted.

## Wake-ups

1. A server-side Routine fires into this session on a schedule set by the mode
   (below). It survives container restarts.
2. `tools/ops.py wait`, run in the background, exits when results land and so
   re-invokes the session.
3. Local batches, likewise, when run in the background.

## Modes

| | 1: low | 2: value | 3: burn |
|---|---|---|---|
| heartbeat | every 2 hours | hourly | hourly, and the session keeps working between wakes |
| per wake-up | `digest`; `status`; dispatch to saturation; `evergreen` if short; restart `wait`. Nothing else. | as 1, then read each landed result against its expectation, record it in `HANDOFF.md` in a few lines, design the next arms for the open question, merge when a result settles something | as 5, with several open questions in parallel |
| new experiments | only from the queue and evergreen | designed each wake from the latest result; cheap local diagnostics when they settle a question faster than Actions | broad sweeps (24–48 seeds, several parameters), long runs, replays and diagnostics on all 4 local cores at all times |
| engine changes | none | when a diagnostic has shown the change should matter (audit rule 1); defaults change only on 1M-tick paired evidence (audit rule 2) | same rules, pursued faster; also speed work (more worlds per Actions minute), page improvements |
| writing | the log line `digest` writes; one commit per wake at most | concise HANDOFF entries, PR and merge per settled result | fuller write-ups, reviews of own work, subagents for parallel analysis where they save wall-clock time |
| rough cost per wake | a few thousand tokens | tens of thousands | as much as the work needs |

Mode 3 (burn) buys depth and parallelism, not a faster version of the
add-a-switch loop. Every experiment still states its expectation, and every
result is recorded (see the self-audit in `HANDOFF.md`).

## Changing mode

When the owner names a mode, edit the "Current mode" line above, commit, and
set the Routine's schedule (`update_trigger`, id `trig_01AFPVT5d29ZrjBYy7DxiEAo`,
"evosim ops heartbeat") (mode 1: `0 */2 * * *`; modes 2 and 3:
`0 * * * *`). "Pause" disables the Routine and stops dispatching; running jobs
finish and are digested on resume.

## The goal, and the questions that serve it, in order

The goal: an evolution simulator of plants and animals in which every behaviour
emerges. The owner's direction (2026-09-27): keep the app's shape (plants and
animals as separate kingdoms, one body template); add realism that can unlock
behaviour; no modular bodies or single genome for now. Questions are ranked by
how much they move that goal.

1. **Realism that unlocks behaviour.** Smell: done, on (grazing fronts,
   alignment p < 0.001); follow-up on scent lifetime (`v1-SD02-*`) and 3M
   (`v1-SM-3M`) running. Nutrient loop: costs predators at `soil0` 6 and
   carnivore species even with abundant nutrient (3 against 12 at `soil0` 24
   with smell): off. Lifetime learning: stays active but costs animals and
   speed with no gain in predation: off.
2. **Speed.** More worlds per Actions minute (4 per job, done), then the
   engine (sense is 26% of time, the brain 25%).
3. **Plants as partners.** Fruit-seeking evolves with fruit senses but does
   not pay the plants more; why (where seed lands?).
4. **Open-ended evolution.** Predators rarely re-evolve after a collapse.
5. **Predator persistence of the default build**, from growing samples:
   `v1-EG-base-*`.
