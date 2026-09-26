# Program audit, engine 1.x: host's own findings (written before the auditor runs)

2026-09-26. Per `.claude/skills/program-audit/SKILL.md` step 1. Confidence 1–10.

1. **The herding line is looping (9).** Since the vigilance result, eight
   physics levers were tried for prey grouping and all were null (headDown 0.9,
   killCool 20/60, lunge at two settings, strike recovery, cover, kinDir,
   packHunt made predators group instead). The hand-built diagnostic
   (HANDOFF, "Hand-built herder diagnostic") says grouping does not pay even
   when built in. More switch sweeps on herding should stop until a mechanism
   is found that makes the diagnostic pass first.
2. **Config surface bloat (8).** Thirteen switches ship off by default with null
   or negative results: gutCap/gutDig, vigilShare, mutReflect, growExp,
   strikeCool, missCool, confHit/confR, hazard, packHunt, fibre/digestMass,
   sizeMax, killCool, cover. Each costs code in the hot loop and a reader's
   attention; none is justified by a measurement. They should be removed from
   the build (the result stays in HANDOFF).
3. **Default changes rest on small samples (7).** vigilance (12 v 12), plant
   height browse 2 (12 v 12), browseGrown (24 v 24 at 400k, 10 at 1M). The
   browseGrown effect (0 v 8 giant worlds) is large enough; the vigilance
   grouping effect (mean clump 1.17 v 0.90) is not replicated under the
   current plants and may be gone.
4. **The headline metric is saturated (6).** "Predator-dominated" is 20 of 24;
   it no longer separates settings. Exit rate at 1M ticks and carnivore
   clusters are the discriminating measures now, and the 1M runs are 10 seeds.
5. **Evolved-start refresh was repeated without a hypothesis (5).** Five
   candidates, all worse than seed 42, and the likely cause (transplant seed 3
   fails for most) was never tested.

Mission: predators, carnivore species and plants hold each other in check for
1M ticks in every test world under the current defaults. That part is reached.
Herding is not.
