# Program audit, auditor's report (2026-09-29)

Written without reading `AUDIT-HOST-2026-09-29.md`. The host tags each finding
[cross-validated], [auditor-only] or [host-only] afterwards.

Data: the 1,956 standing-block worlds on disk (`runs/v1-EG-base-*`, 163 blocks
of 12, 1M ticks), every designed arm in `ops/queue.json` with its baseline
(587 same-seed pairs), and the six 3M blocks (71 worlds). I re-derived the
predator state with the definitions in `tools/v1score.py:62-77` (20k rolling
meat share, in above 15%, out below 8%, after 60k) and `tools/ops.py:47`
(persisting = predK >= 64% of the run after 60k). My count matches the digest
(1,386 of 1,956 persisting, 70.9%). The scripts are in the session scratchpad
(`score_all.py`, `reent.py`); nothing in the repo was changed except this file.

## Summary

Persistence at 1M, as measured, cannot register the size of change that any
single lever is likely to make, so the seven-lever loop could not have ended
any other way. Pairing by seed does nothing. The standing blocks now use all the
capacity to re-measure a number already known to about one point. The
archive already answers the re-origination question the replays were
designed for: carnivore lines re-form at a steady, measurable rate. Pivot:
stop the lever loop and the standing blocks, retarget to exit and re-formation
rates, and spend the capacity on few, large arms.

## Surfaced findings

### 1. The persistence test cannot detect a plausible positive lever. Score 9, CONFIRMED

- The pooled baseline on the current build (smellDecay 0.1 era, seeds from
  2177) is 69.7% (744 of 1,068). The most any lever can add is 30 points.
- With the program's p < 0.05 rule, an arm of 24 worlds must reach 22 of 24
  (92%) to differ from 69.7% (exact binomial against the pooled rate). At 48
  it needs 40 (83%), at 96 it needs 76 (79%), at 192 it needs 147 (77%).
  McNemar on 24 same-seed pairs is weaker still (finding 2).
- "Moved persistence less than the spread between standing blocks" does not
  measure the levers. That spread is sampling noise at n = 12: block counts
  have variance 2.86 against 2.48 for a binomial at 70.9%, and the
  histogram of 163 blocks (4 to 12 persisting) matches the binomial counts
  within a few blocks at every value.
- Three of the seven levers (`meatFloor` 0.6, `mutSd` 0.12 replay, `sex` 0)
  were never 1M persistence tests. They were 4-world, 400k-tick replays
  (HANDOFF.md "Re-origination levers, replay test" and "Gene flow as the
  barrier?"). Finding 3 gives their power.
- The measure stacks three thresholds (15% entry, 8% exit, 64% of run). This
  is the failure CLAUDE.md rule 4 warns about, applied to the measure itself.

### 2. Same-seed pairing does nothing. Score 9, CONFIRMED

Over all 587 designed-arm/baseline pairs in `ops/queue.json` (38 arm/baseline
comparisons):

- Persistence: both 291, arm only 110, baseline only 129, neither 57.
  Independence predicts 287 for "both". phi = 0.03.
- Correlation between arm and baseline on the same seed: predator-state share
  of the run r = 0.02, meat share of the last half r = 0.005.

A seed fixes the fertility map and nothing that matters by 1M. Every designed
test that ran a fresh same-seed block as its baseline paid double for no
variance reduction. McNemar on discordant pairs then throws away the
concordant half of the data. The right comparator for any arm on the current
build is the pooled baseline, which is already known to about ±1.4 points.

### 3. Re-origination is a slow rate, not a wall, and the archive measures it. Score 9, CONFIRMED

HANDOFF.md "Next" item 1 says: "After an exit no world has re-evolved
predators within the run." The re-origination replays were built on that
premise ("a specialist line does not" come back).

From the standing blocks: 471 re-entries into the predator state after an
exit. For 211 of them, the gap before contained no carnivore cluster (10+
animals, meat > 0.5, the definition in `tools/paired.py:34`) and the adults
living mostly on meat fell to 2 or fewer. The hunter line was gone. In 98 of
those 211, a carnivore cluster formed again in the new predator episode (85
after a gap of 100k ticks or more). The 3M blocks show 23 of 33.

As a rate: 98 re-formations in 260M ticks of collapsed world at 1M, and 23 in
58M at 3M. That is 0.038 and 0.039 per 100k collapsed ticks, the same in both.
The mean wait is about 2.6M ticks, which is why 1M runs rarely show it and 3M
runs do.

Power of the replays: at that rate, 4 worlds for 400k ticks expect 0.6
re-formations with no lever at all. A lever that doubled the rate expects 1.2.
0 of 4 "as is" was the expected result, and the design could not tell a
doubling from nothing. Meanwhile 694 standing worlds end collapsed, and their
end-of-run genome dumps are ready-made starting states.

### 4. Standing blocks take most of the compute and add almost nothing. Score 8, CONFIRMED

- In the queue era, standing blocks are 2,028 of 3,067 million-tick worlds
  (66%). Designed arms are 1,039.
- Right now every entry in flight or pending is a standing block (4
  dispatched, 2 pending, `ops/queue.json`). No designed run is queued.
- The pooled rate has a standard error of about 1.0 point (1.4 on the
  current build alone). By 240-world slice in dispatch order: 75.0, 75.8,
  69.6, 67.5, 70.4, 65.4, 71.3, 70.0%. Carnivore species at the end: 69,
  92, 70, 74, 77, 70, 78, 70 per 240. Another block moves neither.
- OPS.md says standing runs "are never wasted". Given finding 2 they are not
  needed as same-seed baselines either. Under the 60-world cap a 96-world
  arm at 1M takes two waves, about two to three hours.

### 5. Persistence at 1M comes from two steady rates; measure those instead. Score 8, CONFIRMED (the rates); PLAUSIBLE (the recommendation)

- Exits from the predator state, per 100k ticks spent in it, by the episode's
  age: 0.047 (first 100k), 0.087, 0.099, 0.089, 0.075 (600k to 1M). After the
  first 100k the hazard is flat. Exits land evenly across 100k to 1M in
  absolute time (109, 149, 153, 148, 135, 128, 112, 113, 109 per 100k slot).
  Nothing about a world's age or history predicts the next exit. That fits
  MINING.md's result that early genes predict nothing (AUC 0.45 to 0.55).
- Re-entry to the predator state runs at 0.12 per 100k ticks out of it (471
  in 382M). With exits at 0.085 per 100k in it, the long-run share of time
  in the predator state is 0.12 / (0.12 + 0.085), about 0.59. The six 3M
  blocks give 0.36 to 0.74, mean about 0.61.
- Under a constant hazard with several causes, removing one cause moves 1M
  persistence little. HANDOFF's own sweep analysis finds a 40%+ size rise
  before 42% of predator losses. If a lever removed every sweep exit, the
  hazard would fall by about 40% and persistence would rise from about 70%
  to about 80% (a rough estimate from the flat hazard). By finding 1, 24
  pairs cannot see that.
- Exit counts are the more sensitive endpoint. A 24-world arm at the
  current rate expects about 15 exits. A 50% cut (7 exits) is Poisson
  p 0.037 against the pooled rate, where persistence would need 22 of 24.

Recommendation: report, for every arm against the pooled baseline, the exit
hazard per 100k predator ticks, the re-formation rate per 100k collapsed
ticks, and the predator-state share of the run, with exact Poisson or
binomial p. Keep 1M persistence as a descriptive line only.

### 6. The strike levers were read as null because of a lucky baseline. Score 7, CONFIRMED (numbers); PLAUSIBLE (reading)

- The same-seed blocks `v1-EG-base-3137` and `-3161` persisted in 19 of 24
  (79%) and had 9 exits where their predator time predicts 15.8 at the pooled
  rate (Poisson p 0.10).
- `dmgExp` 1 and `dmg` 0.64 persisted in 20 and 21 of 24. Pooled, 41 of 48
  (85%) against 69.7%: exact binomial p 0.018. This pools two levers after
  the fact, and 11 arms were compared with the pool, so treat it as a lead.
  Exits 25 against 31.9 expected (p 0.25). Predator-state share 0.83 against
  0.78.
- HANDOFF.md explains the null as "saved from one crash, they are lost
  another way or later", citing exits 11 and 14 against 9. The 9 is the lucky
  block. Against the pooled rate the strike arms had fewer exits, not more.
- This is the one lever whose 1M data fit its diagnosed mechanism (branches:
  hunter line kept through the sweep window in 9 of 12 against 3 of 12). A
  96-world `dmg` 0.64 arm against the pooled baseline, with exit hazard as
  the endpoint, settles it in two to three hours of the capacity now used
  for standing blocks.

### 7. On the core metric the program has been flat since the queue started. Score 7, CONFIRMED (metric); approximate (behaviour count)

Two measures. Persistence of the default build at 1M: flat at about 70%
since 2026-09-27 (finding 4's slices). Every default change since then
(fruit, smell, `smellDecay` 0.1) left it unchanged. The large gains came
earlier, from quick physics sweeps at 400k: `dietCurve` 2 (16 of 20
predator-dominated against 11 of 20), `browseGrown` (giant worlds 0 against
8), compass off (20 of 24 persisting against 10).

New emergent behaviours per day, my count from HANDOFF.md headings and
commit subjects: about 8 on 09-25 (grazing, defence response, scavenging,
predation, arms races, a carnivore species, a trophic cascade, grouping
under vigilance), about 7 on 09-26 (alarm calls and eavesdropping,
reproductive isolation, a browser/grazer split, assortative mating,
streaming, predators following herds, cannibalism), about 3 on 09-27 (seed
carrying selects for fruit, fruit-seeking, memory in use), 1 on 09-28
(grazing fronts from smell), 0 on 09-29. The rate of discovery is falling
while the rate of runs is not.

## Mandatory questions

### 1. Is the mission reachable?

Yes, and the data say it is mostly reached. From `evosim.html:99-266`:

- Food value per tick of feeding, per mass^0.75. Grazing: `graze` 0.12 x
  `ePlant` 1 x (1 - diet^2) = 0.12 at diet 0. Flesh: `chew` 0.20 x `eMeat` 8
  x yield = 0.64 at diet 0 (yield 0.4) and 1.6 at diet 1. A corpse also
  carries the reserves it died with (up to `eCap` 40 per unit mass), so a
  healthy carcass is worth up to 3.84 per tick even to a plant gut. For a
  plant gut meat is 5 to 30 times richer per feeding tick than leaves, and
  more for a meat gut. Carnivory is not dominated.
- The diet trade-off favours omnivores. The yields at diet d are 1 - d^2 and
  0.4 + 0.6(1 - (1 - d)^2). Their sum peaks at d = 0.375 (1.625, against 1.4
  at 0 and 1.0 at 1). An animal whose raw intake is a share s meat does best
  at d = 1.2s / (2 - 0.8s). At the world's 18% meat that is 0.12. The
  standing blocks' mean diet gene is 0.092. A gut above 0.5 pays only when
  meat is over 62.5% of intake, and above 0.9 only when it is over 94%. A
  specialist carnivore is a narrow corner of this physics, reached only by
  animals that take most of the kills. It is not blocked.
- Time to kill (`dmg` 0.5, `dmgExp` 0.75, `hpPerMass` 2, `armourEff` 0.75):
  4 m^0.25 / (weapon x k^0.75 x (1 - 0.75 armour)) for prey mass m and a
  hunter k times heavier. A 2.7 hunter with weapon 0.7 kills a 0.3 grazer in
  under a tick and a 1.8 grazer in about 5. Grazer growth is a real refuge,
  but not a wall.
- Outcomes: 70.9% of 1,956 standing worlds keep meat-eating for most of 1M
  ticks. In those worlds a carnivore cluster is present in a mean 54% of
  samples. It is present in over half the samples in 794 of 1,386 worlds
  and over a fifth in 1,259. So persistence does track carnivores, not only
  opportunistic biting. Transplants into collapsed worlds take over (HANDOFF
  s2184, s2278).

The goal of plants, herbivores and carnivores holding each other in check is
met in most worlds most of the time. The open part is the last 30%, and that
is a stochastic loss process (finding 5), not a missing mechanism.

### 2. Rate of progress

Metric: the default build's 1M persistence, and new emergent behaviours per
day (finding 7). Persistence has been flat at about 70% for three days and
2,000+ worlds. Behaviour discoveries fell from about 8 to 0 per day. Since
2026-09-27 the program is walking in circles on its core metric. It is still
producing knowledge (the sweep mechanism, transplants, nulls), but no change
in the thing it measures.

### 3. What should be abandoned

- The persistence-lever loop at 12 to 24 worlds per arm (finding 1).
- Standing blocks (finding 4). Freeze the pooled baseline. Run a check block
  only after a default changes.
- Same-seed baselines and McNemar/sign tests as the main test (finding 2).
- Four-world replays as tests of re-origination levers (finding 3). Use the
  archive's 98 re-formations and 694 collapsed end states instead.

### 4. Simplicity counterfactual

The seven levers could have been one analysis of the archive plus one arm.
The archive held 1,165 exits, 471 re-entries and 98 re-formations when the
replays began. A case-control of what precedes an exit (grazer size, plant
mass, diet spread) against matched windows without one would have ranked
exit causes and shown the flat hazard. Then one 96-world arm on the top cause
would have tested it. That is about a day of analysis and three hours of
Actions, against the day spent on the seven levers.

Mechanisms in the build without a measurement that justifies them: off by
default after a null or negative test, `patchy`, `nutrients` (with
`resprout`), `learn`, `smellFruit`, `dmgExp`, `dayTicks`, `seasonWave`: 7.
On by default with a world-level null, `give`, `crowdHeading`, `kinDir` and
the colour senses: 4. Inputs constant by default: 7 of 53 (`gut`,
`compassX`, `compassY`, `felt`, `smellFruit`, `smellFruitDir`, and `light`,
which is a constant 1 like the bias). The `learn` output drives nothing.
Together that is 187 of 1,051 genome values. `v1-BD-lean` showed the extra
inputs cost nothing at 1M, so pruning buys speed only (appendix A3).

### 5. Is the process the bottleneck?

Not the cadence. The queue scored 59 designed entries in about two and a
half days, not one bit a week. The bottleneck is statistical design:

- a binary endpoint with three thresholds and a 70% baseline (finding 1);
- pairing that does nothing (finding 2);
- capacity filled with replication (finding 4);
- a p < 0.05 gate that no feasible positive persistence result can pass at
  24 worlds.

Replace these while keeping pre-registration, expectations written first,
and p < 0.05 for defaults, which are what stopped the earlier fabrications:

1. One frozen pooled baseline per build.
2. Rate endpoints (exit hazard, re-formation rate, predator-state share)
   with exact tests.
3. Arms of 96 or more worlds, or none. Fewer, larger tests.
4. A power line in every pre-registration: the smallest effect the arm can
   detect. An arm that cannot detect its expected effect is not dispatched.

### 6. What is being ignored because it did not fit the box

- Re-formations in the archive (finding 3). The 3M results ("predators come
  back ... at about the same rate per world", HANDOFF) were filed as "not a
  clear change", while "Next" still says predators never return.
- The strike levers' positive signal (finding 6), filed null against a lucky
  block.
- Persistence used as a veto on behaviour (appendix A1): the compass and
  learning are off because they did not help predators.
- `smellFruit` collapsed the fruit mutualism in 22 of 24 pairs (p 0.00004),
  the largest plant-side effect in the program. It was switched off without
  a located cause (appendix A2).

## What to do next, in order

1. Stop dispatching standing blocks. Freeze the current-build baseline
   (1,068 worlds). Add exit hazard, re-formation rate and predator-state
   share to `tools/ops.py digest`, each against the pooled baseline.
2. Case-control on the archive: what precedes the 1,165 exits and the 98
   re-formations, against matched windows. Rank exit causes by share.
3. One 96-world arm of `dmg` 0.64 against the pooled baseline. Pre-registered
   endpoint: exit hazard, with a stated detectable effect.
4. If re-origination (OPS question 4) stays a goal: arms of about 100
   collapsed worlds for 400k each, founded from the 694 collapsed end-state
   dumps. At 0.038 per 100k that expects about 15 re-formations per arm, so
   a doubling is detectable.
5. Put the freed capacity back on OPS questions 1 to 3 (realism that unlocks
   behaviour, speed, plants as partners), which rank above persistence in
   OPS.md and got less of the last day than the persistence levers did.

## Appendix (scores 4 to 6)

**A1. Persistence works as a veto on emergent behaviour. Score 6, PLAUSIBLE.**
The compass gives the clearest collective behaviour in the program
(streaming in 24 of 24 worlds; on the smell build alignment 0.30 and 0.23
against 0.07, 22 of 24). It is off because it cost persistence: 10 against
20 of 24 before smell (p 0.013), 13 against 18 on the smell build (13 of 24
against the pooled 69.7%: p 0.12). Learning is off for "no gain in
predation", although it moved predator speed in 23 of 24 pairs and prey
clumping at p < 0.001. Whether a world with more behaviour and fewer
predators is better is the owner's call. The program made that call through
its metric without stating it.

**A2. The fruit-scent collapse is unexplained and fits OPS question 3. Score 6, PLAUSIBLE.**
`v1-SF-*`: fruit gene 0.10 against 0.29, lower in 22 of 24; carried seed
14% against 37%; animals 864 and 904 against 1040 and 1015. Two diagnostics
ruled out two causes. The loop "has no located start" (HANDOFF). It is the
largest plant-animal effect measured, and "plants as partners" ranks third
in OPS.md.

**A3. Dead genome values. Score 5, CONFIRMED.** 187 of 1,051 values sit on
constant inputs or the idle `learn` output (`evosim.html:827-852, 951-952`).
The brain is about 25% of run time. Pruning would save a few percent, too
little to justify a layout break on its own.

**A4. Sign tests on continuous measures. Score 5, CONFIRMED.**
`tools/paired.py:66-70` tests continuous measures by the sign of the
difference only. With pairing worthless (finding 2), a two-sample
permutation or rank test against the pooled baseline uses the magnitudes and
the 1,068 baseline worlds.

## Verdict

Pivot. Do not stop the project: the mission is met in most worlds, and the
physics produces carnivores, re-forms them at a measurable rate, and still
yields new behaviour when physics changes. Stop the persistence-lever loop
and the standing blocks today. They cannot produce a positive result at their
size, and the second one no longer informs anything. Retarget the predator
question to exit and re-formation rates measured against a frozen pooled
baseline. Mine the archive before running anything new. Run few arms, of 96
or more worlds. What would change this verdict: a 96-world arm (`dmg` 0.64 or
the top exit cause from the case-control) that cuts the exit hazard by a
third or more would justify one more round on persistence. If two
well-powered arms on the top two exit causes both show no hazard change,
treat the remaining 30% as irreducible loss in finite worlds and move the
predator program to re-formation rate or drop it for OPS questions 1 to 3.
