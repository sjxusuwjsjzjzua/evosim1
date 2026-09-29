# Program audit, host findings (2026-09-29)

Written before the auditor runs, per `.claude/skills/program-audit/SKILL.md`.
Question put to the audit: seven levers in a row on predator persistence at 1M
ticks (`meatFloor`, `mutSd`, `sex` 0, `gridN` 96, `patchy`, `dmgExp`, `dmg`)
each moved it by less than the spread between standing blocks. Is persistence
the right target, and what next?

## H1. The persistence tests cannot see the effects they are looking for (9, CONFIRMED)

162 standing blocks of the default build (`ops/log.md`, `v1-EG-base-*`): 1,374
of 1,944 worlds persisting (70.7%); per block 4 to 12 of 12, distributed as
4:1, 5:9, 6:11, 7:18, 8:41, 9:36, 10:27, 11:17, 12:2. That is what a binomial
with n = 12, p = 0.71 gives (sd 1.6): the block spread is sampling noise, not
build drift. A 24-pair McNemar test at about 10 discordant pairs reaches p <
0.05 only at about 8 to 1 or better, so only effects of roughly 25 points or
more are visible. Every lever today was tested at that size. The nulls are
"not large", not "none".

## H2. Most of the Actions capacity went to replication that no longer teaches anything (8, CONFIRMED)

Queue (`ops/queue.json`): 176 standing blocks (about 2,100 worlds) against 60
designed entries (about 720). Standing-block means by day: persistence 71%,
71%, 69%; worlds with a carnivore species 26%, 32%, 31%; meat 18.5, 18.0,
17.7%. The number is known to within a point or two. The standing blocks
exist to give paired baselines, but a baseline is only needed on seeds a
designed arm uses. `evergreen` should stop being the default filler.

## H3. The work drifted to the goals ranked lowest (8, CONFIRMED)

`OPS.md` ranks the questions: 1 realism that unlocks behaviour, 2 speed,
3 plants as partners, 4 re-origination, 5 persistence of the default build.
Today's designed runs were all on 4 and 5. Speed (2), which multiplies
everything else, has had no work since per-job packing: the engine profile
(sense 26%, brain 25%) is written down and untouched. The self-audit rule 4
of 2026-09-27 ("stay on the open core problem, predators that never come
back") is what pulled the work here; it has now been followed through seven
levers and should be retired or rewritten.

## H4. Persistence at about 70% may not be a defect (6, PLAUSIBLE)

The mission is plants, herbivores and carnivores holding each other in check,
with behaviour emerging. About 7 in 10 worlds keep predators for 1M ticks and
about 3 in 10 form a carnivore species. Local extinction of a predator guild
is ordinary ecology. Pushing 70% toward 90% by physics tuning may buy little
toward the mission compared with what the surviving worlds show (or fail to
show) in behaviour.

## H5. Re-origination may be an unrealistic target (5, PLAUSIBLE; appendix)

Specialist hunter lines were built over about 600k ticks and are lost in one
sweep. Transplants show hunting still pays afterwards, so the path is what is
missing. Real predator guilds do not re-evolve on short timescales either;
expecting it within 400k ticks may be asking for something nature does not do.

## H6. The option surface keeps growing (5, CONFIRMED; appendix)

Options off by default now include `nutrients`, `learn`, `smellFruit`,
`compass`, `seasonAmp`, `seasonWave`, `patchy`, `dmgExp`, `dayTicks`, and
more. Each is a nulled or harmful mechanism kept "as information". They cost
reading time and code paths, not simulation speed.

## What the host would do next (before seeing the auditor)

1. Stop `evergreen` as the default filler; run standing blocks only as
   baselines for designed arms.
2. Spend the freed capacity on speed (engine profile) and on the plants
   question, per `OPS.md`'s ranking.
3. If persistence is kept as a target, test only levers that a diagnostic
   says should move it by 25 points or more, or pool 48+ pairs.
