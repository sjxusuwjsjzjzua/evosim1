# Program audit, engine 1.x (auditor), 2026-09-26

Scope: the 1.x program, 2026-09-24 to 2026-09-26 (146 commits: 46 `handoff`, 36 `engine`, 12 `ui`). Evidence: `evosim.html` CFG block (lines 99–240), `HANDOFF.md`, `MINING.md`, `README.md`, and every 1.x log under `runs/` (re-scored for this audit; scripts in the session scratchpad). `AUDIT-HOST-v1.md` was not read, so every finding below is `[auditor-only]` until the host adjudicates against its own list.

Metric definitions used throughout, computed by me from the logs:
- **predDom**: regime > 50% (MINING's definition).
- **carn**: a logger cluster at the last sample (≤ 400k) with meat > 0.5 and n ≥ 10.
- **preyClump**: mean `clumpPrey` over the last half, in predDom worlds only.
- **killDeaths**: kills as a share of all deaths.
- P-values are two-sided Fisher exact tests.

## Verdict on convergence

The program converged on predation and then stopped moving. Predation went from 0 of 56 worlds (T/U, 2026-09-25 morning) to a carnivore cluster in 26 of 48 worlds (AF-browseGrown, AH-grown-rep, AL-current24). The last ~15 batches changed no mission metric. Prey grouping has not moved in any batch.

---

## Surfaced findings (confidence ≥ 7)

### 1. Herding is being looped on, and the carnivore-cluster rate has plateaued. Confidence 9, CONFIRMED

Per-batch metrics at the default of the day:

| era | batches | carn | preyClump (predDom worlds) |
|---|---|---|---|
| T, U (old defaults) | 8 | 0 / 56 | – |
| V-f003, W, X, Y (upFixed 0.003, curve 2) | 7 | 15 / 70 | – (not logged yet) |
| AB-base | 1 | 2 / 10 | 0.90 |
| voice (static browse 2) | 1 | 8 / 12 | 0.94 |
| AF-browseGrown, AH-grown-rep, AL-current24 | 3 | 26 / 48 | 0.92, 0.93, 0.93 |

Herding-directed batches on disk and their preyClump:

| batch | preyClump |
|---|---|
| vigilShare | 0.86 |
| lungeM | 0.87 |
| coolOnly | 0.82 |
| AJ-kill20 | 0.89 |
| AJ-kill60 | 0.83 |
| hd9 | 0.90 |
| cover2 | 0.97 |
| pk0 | 0.94 |
| pk1 | 0.76 |
| kin | 0.95 |
| call10 | 0.73 |
| call4 | 0.70 |

Earlier herding work: crowdDir, alarm and kConfusion. Two hand-built herder diagnostics also failed. That makes at least 13 attempts, all in the 0.70–0.97 band.

- The only batches above 1.1 were in the static-plant-height era: AD-1M-browse2 at 1.16 and f6b2 at 1.27 (n = 5). The vigilance result (1.17, HANDOFF.md:243) is also from that era.
- Making `browseGrown` the default (deadd8b) erased those values. HANDOFF.md:424 records this.
- HANDOFF "Next" #2 (HANDOFF.md:590) still cites 1.17 as current.
- Since browseGrown became the default, about 15 batches ran (lungeM, coolOnly, call4/10, kill20/60, hd9, cover2, pk0/1, kin, AI-sex, AK-medium, AL-current24, AL-1M, evo600). The only default they changed was one added sense, `kinDir`, at 11 vs 10 of 12 (p = 1.0).

### 2. Defaults are chosen on differences that 12-seed batches cannot resolve. Confidence 8, CONFIRMED

Decisions and the p-values of their own evidence:

| decision | evidence | p |
|---|---|---|
| dietCurve 2 is "the strongest lever found" (HANDOFF.md:224) | 16/20 vs 11/20 | 0.18 |
| meat guts under curve 2 | 6/20 vs 3/20 | 0.45 |
| browse 2 for carnivore clusters | 8/12 vs 3/12 | 0.10 |
| voice shipped | predDom 10 vs 8 | 0.64 |
| voice shipped | grazers turn from calls 9 vs 5 | 0.21 |
| voice shipped | bolt 11 vs 7 | 0.16 |
| kinDir shipped | 11 vs 10 | 1.0 |
| callCost 0.008 rejected | 10 vs 7 | 0.37 |
| sex rejected | 12 vs 9 | 0.22 |
| packHunt rejected | 8 vs 6 of 8 | 0.47 |

Three results in the program clear p < 0.05:
- `upFixed` 0.003 against 0.010: 6/10 against 0/30 worlds.
- `browseGrown` against giant worlds: 0/24 against 8/24, p = 0.004.
- Sex costing carnivore clusters: 1/12 in AI-sex, below.

A replication shows the noise band directly:
- `v1-AH-1M-grown` (sha ab062ce) and `v1-AL-1M-current` (sha 9e0f2d7) use the same seeds 701–710 and the same cfg. The build differs only by the `kinDir` input and two off switches.
- Worlds with last-100k meat above 15%: 10/10 against 6/10 (p = 0.087).
- Predator-state time: 9,018k against 7,108k ticks.
- README.md ("all ten still had predators at the end") quotes the favourable draw. HANDOFF.md:400–404 reports the current-build batch only as an exit rate.

### 3. The constants that set the trophic energetics were never varied. Twelve mechanisms were added instead. Confidence 8, CONFIRMED

Across every 1.x log on disk:
- Never varied: `eCap`, `meatFloor`, `chew`, `cBuild`, `graze`, `ePlant`, `pR`, `kDef`, `atkCost`, `armourEff`, `hpPerMass`, `corpseDecay`.
- `eMeat` and `dmg` were varied only under the retired defaults (T/U/S batches, `upFixed` 0.010).

The host's own diagnosis of the herding failure is energetic: "predators never fill up … a kill is eaten in about one tick" (HANDOFF.md:369). That is a direct consequence of these constants (Q1 below).

The responses were `killCool`, `gutCap`/`gutDig`, `strikeCool`/`missCool`/`confHit`, `kConfusion` and `packHunt`. Each is a new mechanism, and none changed the constant behind the problem. The reserve term in `die()` (`evosim.html:582`, `cE = mass*eMeat + E`) makes a healthy carcass 3–4 times richer than its flesh. It has not been tested once.

### 4. Large mission-relevant effects were rejected because they moved the predator count by a non-significant amount. Confidence 8, CONFIRMED

This answers Q6. The program optimises one scalar, the predDom count out of 12, and the mission's other items lose to it:

- **Signalling.** At `callCost` 0.02 and 0.008, calls became reliable alarms:
  - baseline loudness fell to 0.00–0.04 in 8 of 12 worlds;
  - alarm calls appeared in 4 of 12 worlds;
  - grazers turned from calls in 11–12 of 12.

  This was rejected because predDom fell 10 → 8 and 10 → 7 (p = 0.37). HANDOFF.md:526–534.
- **Speciation.** The mission lists speciation, and `sex=1, mateDist=0.1` is the only setting that produces reproductively isolated species (HANDOFF.md:331). It stays off by default over 12 → 9 predDom (p = 0.22). The shipped default is clonal, so it cannot produce biological species at all. The honest reason to keep sex off is a significant drop in carnivore clusters (AI-sex 1/12 against 8/12 on the same seeds in `voice`, p = 0.009), and HANDOFF does not cite it.
- **Pack hunting.** `packHunt` produced predator packs at 3.1–14.7x a random scatter. It was rejected for 8 → 6 of 8 (p = 0.47).

### 5. The speciation claim in HANDOFF is overstated, and one of its five cited worlds contradicts it. Confidence 8, CONFIRMED

The claim, HANDOFF.md:339–345: "In all 5 worlds checked (402, 404, 406, 410, 412) the meat-leaning clusters (diet 0.46–0.77) breed with 0% of the grazer clusters … Diet-split species are the rule."

What `python3 tools/isolation.py runs/v1-AI-sex/s406-genomes.json --mateDist 0.1` shows for s406:
- No animal in the dump has diet ≥ 0.45.
- The most meat-leaning clusters (diet 0.29 and 0.30) breed with the grazer clusters at 13–32%, not 0%.

Across all 12 AI-sex worlds:
- Only 5 contain any animal with diet ≥ 0.5, and those are 1–9% of the population (end `dietHist`).
- The logger finds a meat > 0.5 cluster in 1 of 12.
- The dumps oversample meat-eaters (commits c8a786f, 6ec8a66), so clusters built from dumps look larger than the populations are.

The supportable statement is "an isolated meat-gut species in 4 of 12 sexual worlds".

### 6. The headline metric counts worlds with no carnivores, and the omnivore outcome follows from the constants. Confidence 8, CONFIRMED

AL-current24 (the current defaults, 24 seeds):
- predDom in 20, a carnivore cluster in 12. So at least 8 predator-dominated worlds have no carnivore population.
- Mean diet gene is 0.057–0.154 in all 24.
- Adults living mostly on meat: 0.9–15.3%.
- Kills are 51–99% of all deaths (median about 94%).
- Mean lifetime is 320–2,900 ticks, against a potential lifespan of about 6,000 x mass^0.25.

Brain probes (`node tools/genomes.js`, diet < 0.3 class, strike probability on contact with a smaller animal):

| world | strike probability |
|---|---|
| s1012 | 1.00 |
| s1013 | 0.99 |
| s1017 | 0.94 |
| s1004 | 0.85 |
| s1016 | 0.76 |
| s704 (1M) | 0.53 |

That is 6 of 13 dumps probed. In those worlds the "herbivores" are killers too. "Predator-dominated" as scored (meat > 15% of intake) is met by omnivores killing each other. It does not need a trophic level to exist.

### 7. Carnivore body size runs to whatever upper bound the size gene has. Confidence 7, CONFIRMED

- AL-current24: 4 of the 12 worlds with a carnivore cluster have it at mean size 11.1–12.0, against `sizeMax` 12.
- voice: 3 of 8 at 10.8–11.9.
- AG-size24: one carnivore cluster at exactly 24.0.
- HANDOFF.md:491 says "no giant or dwarf worlds (mean sizes 0.5–4.9)". Population means are dominated by the small grazers, so they hide that the giant trap now sits in the carnivore guild.
- `sizeMax` 24 was only tested with `browseGrown` 0 (the AG-size24 cfg). An arbitrary gene bound sets predator body size in a third of carnivore worlds under the shipped defaults.

### 8. The build carries mechanisms that no measurement justifies, including a dead input. Confidence 7, CONFIRMED

This answers Q4.

Off-by-default mechanisms, all with null or negative results, still in the engine: 12 mechanisms on 17 CFG keys.
- `kConfusion`
- `strikeCool`/`missCool`
- `confHit`/`confR`
- `cover`
- `killCool`
- `packHunt`
- `fibre`/`digestMass`
- `hazard`
- `mutReflect`
- `gutCap`/`gutDig`
- `teethBase`
- `growExp`
- `vigilShare`

`seasonAmp`/`yearTicks` are also untested since T-season.

Senses:
- `gut` (input 25) is constant 0 at the default `gutCap` 0 (`evosim.html:724`). It is a dead input carrying 14 weights.
- Eight of the 30 inputs (`crowdDir`, `alarm`, `alarmDir`, `gut`, `crowdSpeed`, `heard`, `heardDir`, `kinDir`) were added for herding or voice. None has a significant effect on a mission metric. Together they are 112 of the 485 genome loci (23%).
- Every added input changes the genome layout, so matched seeds on either side of the change do not form a paired comparison. The AH/AL divergence in finding 2 shows the result.

### 9. The process is limited by resolution and choice of target, not by cadence. Confidence 7, PLAUSIBLE

This answers Q5. The 1.x program has no weekly cap. It ran about 60 batches and more than 600 worlds in roughly 48 hours. The constraints are elsewhere:
1. Decisions are made at a resolution of 12 worlds, while the baseline on seeds 401–412 itself moved between 10 and 12 of 12 across commits (voice 10, AF-browseGrown 12, kin 11).
2. The scored target is a binary that is nearly saturated.
3. Each null leaves a switch behind.

The rate of experiments is not the problem.

### 10. The herding program is probably aimed at the wrong cause. Confidence 7, PLAUSIBLE

The herder diagnostics (HANDOFF.md:437–445) measured "12–70% more hits per head". They never split those hits by attacker diet. Finding 6 shows that in about half of worlds the diet < 0.3 class strikes on contact with probability 0.5–1.0. In those worlds a group of grazers is a group of mutual attackers, whatever predator satiation does.

The step before any further herding mechanism is to split strikes and kills by the attacker's diet class. That needs logger code only.

---

## The six mandatory questions

**Q1. Is the mission reachable?** Yes. Energetics do not block it, and the shipped constants tilt it toward omnivores rather than toward a carnivore trophic level. Arithmetic from CFG:

- **Carcass energy density.** Energy per unit mass is `eMeat + E/m` = 8 + 40 x (energy share). At the median `reproT` of 0.37–0.6 that is about 23–32. Plants give `ePlant` 1 per unit mass.
- **Intake rate per mass^0.75 per tick.**
  - Plants: `graze` 0.12 x 1.
  - Meat: `chew` 0.20 x ~28 x meat yield.
  - A plant gut at diet 0.1 has meat yield 0.4 + 0.6(1 − 0.81) = 0.51, so it takes in 2.9 energy per tick from meat against 0.12 from plants: **24 times** its grazing rate.
- **Transfer efficiency.** Prey pays `cBuild` 10 per unit mass plus reserves. A diet-1 eater recovers (8 + 20)/(10 + 20) = **93%**. A diet-0.1 gut recovers 48%. So killing pays for every gut, and a predator fills in about one meal (HANDOFF.md:371).
- **Optimal gut.** Let P be the plant energy on offer and M the meat energy. Yield is P(1 − d²) + M(0.4 + 0.6(1 − (1 − d)²)), which is maximised at d\* = 0.6M/(P + 0.6M).
  - A meat gut (d\* ≥ 0.5) is optimal only when meat is at least **62.5%** of a lineage's intake.
  - At the world meat shares observed (25–35%), d\* = 0.18–0.24. The observed mean diet is 0.06–0.15.
  - The constants predict an omnivore-killer majority with a minority carnivore clade, and that is what evolves: a carnivore cluster in about half of worlds, 1–15% of adults.
- **Persistence.** At 1M ticks, plants, killers and grazers do hold each other in check: 6–10 of 10 worlds are still predatory, with 0.04–0.06 exits per 100k predator ticks.

The mission is reached for "predation that persists". It is only partly reached for "carnivores as a separate trophic level". Herding and speciation in the default build are not reached.

**Q2. Rate of progress.** Two metrics tell a converging program from a looping one:
- **P(carnivore cluster at 400k)** went 0/56 → 15/70 → 8/12 → 26/48. It rose over about 30 hours and has been flat at about 50% since browseGrown.
- **preyClump in predator worlds** stayed at 0.70–0.98 in every batch under the current plant model. It shows no trend over 13 or more attempts.

Speciation in the default build has been 0 throughout, because the default is clonal. The program converged on predation and is looping on herding.

**Q3. What to abandon.**
1. The herding line as currently run: one new switch, 12 seeds, then prey clump checked. Its 13 or more attempts are all nulls.
2. The evolved-start replacement search: six candidate populations, each tested in 4 worlds, and none replaced seed 42.
3. predDom as the headline and decision metric. It is saturated (20/24) and satisfied without carnivores.
4. The 12 off switches and the dead `gut` input. Delete them from the build. The logs and HANDOFF keep the record.

**Q4. Simplicity counterfactual.** Three changes carry all the significant gains: `upFixed` 0.003, plant height, and `browseGrown`. A shorter path existed.
- On 2026-09-25, a single factorial screen of the energetic constants (`upFixed`, `eCap`/reserve transfer, `eMeat`, `meatFloor`, `chew`) would have found the `upFixed` effect and mapped the omnivory optimum from Q1.
- Six or more mechanism batches would then not have been spent treating the consequences of one energy ratio.

Currently unjustified in the build: 12 off mechanisms (17 keys), 1 dead input, and 7 other herding/voice inputs with no significant effect. `kinDir` shipped at p = 1.0.

**Q5. Is the process the bottleneck?** Yes, but not through cadence (finding 9). Replace "one switch, 12 seeds, count predDom" with three rules:
- **Paired seeds on a frozen build.** No new input on the day of a comparison.
- **A continuous per-world target vector**, scored with a paired test: predator-state ticks, carnivore-cluster ticks, preyClump, and kills split by attacker diet.
- **A significance bar before a default changes**: at least 24 paired seeds or p < 0.05. A switch that fails is deleted, not kept off.

This keeps the pre-registration and logging discipline that stopped the v0.x fabrications.

**Q6. What was ignored because it did not fit the box.**
- Honest alarm signals (finding 4).
- Reproductive isolation (finding 4).
- Predator packs (finding 4).
- Sex's significant cost to carnivore clusters, which went uncited.
- Predators pinned at the size cap (finding 7).
- Near-total death by killing and short lives (finding 6).
- The plant defence–detox cycle, which MINING.md §4 shows runs independently of predation.

---

## Appendix (confidence 4–6)

- **(6) HANDOFF "Next" is stale.** HANDOFF.md:590 directs herding work using prey clump 1.17 from the static-height era. Current defaults give 0.92–0.93. CONFIRMED.
- **(5) Onset timing contradicts MINING.** README.md says predators "usually need one to three hundred generations to appear". MINING.md §1 finds meat first passing 15% at a median of 20.5k ticks, and much of that is bootstrap carry-over. CONFIRMED on the documents.
- **(5) The evolved start comes from retired physics.** Seed 42 evolved before vigilance, voice, plant height and `kinDir`, and is remapped on load. Populations evolved under the current engine transplant worse (0–3 of 4 worlds). This is unexplained, and it may mean current-engine predation is an ecological state rather than a heritable predator genotype. PLAUSIBLE.
- **(5) The predDom threshold drifted.** It was regime > ~30% in HANDOFF's lever table (HANDOFF.md:211) and > 50% later. v1-X-small-curve2 is 10/10 at the first threshold and 8/10 at the second. CONFIRMED.
- **(4) An unused emergent result.** MINING.md §4 describes a plant defence–detox coevolution cycle (lag r ≈ ±0.2) that has never been turned into a target or shown in the page.

## Verdict

**Pivot.** The engine works for predation; do not rebuild it. Stop the herding-by-switch line. Delete the null switches and the dead input, and freeze the build for a paired design. Spend the next cycle on the energetic constants that set Q1's numbers: the reserve transfer into corpses (`eCap` against `cBuild` and `eMeat`), `meatFloor` and `chew`. Score them with a vector target: carnivore-cluster persistence at 1M ticks, preyClump, kills split by attacker diet, and speciation. Decide explicitly whether speciation belongs in the default build, since clonal cannot speciate. Two results would change this verdict. If a factorial over those constants moves preyClump above 1.1 or carnivore clusters well above 50% at p < 0.05, continue on that axis. If it leaves both flat, herding is out of reach in this physics class: say so in README and stop working on it.
