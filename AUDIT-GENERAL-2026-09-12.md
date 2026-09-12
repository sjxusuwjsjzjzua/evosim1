# GENERAL PROGRAM AUDIT — evosim, 2026-09-12

Scope: the whole program, not one claim. Premise per the skill: guilty until
proven exceptional. Confidence 1-10 on every finding; 1-3 discarded unwritten.
Every number below was computed by this auditor from `runs/rot-collect`
(2,329 logs) or read off a cited line of `evosim-v0_57_0.html`. Scripts were
written to scratch, not the repo.

Not read, by instruction: `HOST-FINDINGS-2026-09-12-GENERAL.md`,
`HOST-FINDINGS.md`, `HOST-POSITION-REWRITE.md`. Tags below are therefore
`[auditor-only]` where no prior committed audit contains the point, and
`[cross-validated: <file>]` where one does. Host adjudication reassigns them.

---

## Verdict

**PIVOT — but a smaller one than the last three audits proposed, and in the
opposite direction from the one taken.** The mission is reachable. The mission
*metric* is a product of three terms, two of them constants, and the project
has been scoring the product. Recomputed as a ratio of selection to supply, the
program has moved 3.35% to 14.71% across six versions, which is real progress
that the ledger cannot see. Meanwhile the pre-registered sample size has
outrun collection by 15x for three consecutive versions, so none of the last
four hypotheses has data. Stop shipping builds; run the two CFG arms that
decide the question; fix the scorer.

---

# Q1 — Is the mission reachable? Arithmetic.

## The metric is an identity with three terms

From the source: `eCarrion` is credited only at `:2065`, as
`bite * meatValue * carrionValue * carrionDigest(carnivory)`, with
`carrionDigest = carrionFloor + (1-carrionFloor)*carn` (`:1654-1656`) and
`W.carrionMass += bite` on the same line. Corpse mass leaves the world only two
ways: that bite, or decay at `:1518` (`W.corpseRot += d`). So

```
heterotrophy  =  supply  x  consumedFraction  x  carrionDigest

supply           = (carrionMass + corpseRot) * meatValue * carrionValue / (ePlant + eCarrion)
consumedFraction = carrionMass / (carrionMass + corpseRot)
carrionDigest    = 0.30 + 0.70 * carnivory
```

Checked, not assumed. Over 1,822 windowed survivors (days 400-800, animals
alive at 800), `eCarrion / (carrionMass * meatValue * carrionValue *
carrionDigest(median carnivory))` has median **1.002**, p10 0.961, p90 1.052.
The identity closes.

Corpus medians for the three terms: **3.92%**, **0.212**, **0.347**. Product
0.288%. Measured heterotrophy median 0.287%.

## What that makes reachable

`supply` is ecology — corpse mass produced per unit energy assimilated. It is
not a free parameter and it is not evolvable in any direct sense. Median 3.92%,
p10 2.22%, p90 7.44%.

The other two terms are what selection can move. Both at 1.0 gives the median
run **3.92%** and a p90 run 7.44%. So:

- **The 5% bar is above the arithmetic maximum of the median run.** It appears
  in `CLAUDE.md`'s mission section, in `tools/score55.py`'s docstring, and in
  the framing of two prior audits. A perfect world — every corpse eaten, every
  animal an obligate carnivore — scores 3.9% and gets filed as a miss.
  [cross-validated: AUDIT-DEADEND-2026-09-12.md, which put the ceiling at
  3.3-4.4% from a four-term decomposition; this is the same conclusion from a
  three-term identity that closes at 1.002 instead of 0.766.]
- **The reachable multiple is 13.6x**, not the 17x the 5% bar implies, and the
  headroom is entirely in `consumedFraction` (0.212) and `carnivory` (0.072).

## The number that decides the mission, not the metric

The mission is three trophic levels holding each other in check. A carnivore
guild drawing all of its intake from meat cannot exceed the supply term: 3.92%
of animal energy throughput, so roughly 3.92% of animal numbers. Corpus median
N over the window is **197** (p90 547).

**Median sustainable carnivore guild: 7.7 individuals. p90: 21.4.**

This reproduces `HANDOFF.md` §0.2's independently derived 8-21 from different
inputs. A guild of eight cannot hold a herbivore population in check and cannot
survive demographic noise for the 20 generations a run lasts.

**So: reachable metric, unreachable mission, at the current arena and the
current energy budget.** Raising the guild to ~100 needs N ~2,500, i.e. arena
area x12 — which at the measured 0.51 h per 800-day job is ~6 h, against the
350-minute Actions job budget. Alternatively raise `supply`, which is set by
how much assimilated energy becomes animal tissue rather than upkeep: **81.0%
of assimilated energy goes to upkeep** (median of per-run medians, n=2,199) and
**24.6% of plant energy is lost to toxin** on top of that.

`a_base`, `a_mass`, `k_toxinHarm`, `toxMaxLoss`, `worldSize`, `carrionFloor`,
`k_corpseDecay` and `corpseMin` have **never been varied in 2,329 logs**. Every
term that sets the guild size is in that set.

---

# Q2 — Rate of progress, in units that matter

Proposed metric: **capture = consumedFraction x carrionDigest**, the share of
available corpse energy that animals actually assimilate. It is the part of the
mission metric selection can move, with the supply term divided out, so it is
immune to run-length, population size and turnover rate.

| build | n | capture | consumedFraction | carrionDigest | supply |
|---|---|---|---|---|---|
| v0.51 | 78 | 3.35% | 0.092 | 0.347 | 2.23% |
| v0.52 | 1239 | 7.71% | 0.215 | 0.348 | 4.00% |
| v0.53 | 258 | 8.21% | 0.224 | 0.348 | 3.58% |
| v0.54 | 184 | 7.11% | 0.221 | 0.347 | 4.37% |
| v0.55 | 49 | 9.51% | 0.258 | 0.349 | 4.95% |
| v0.56 | 14 | **14.71%** | **0.435** | 0.343 | 5.20% |

Three readings, all material:

1. **The program is not walking in circles.** Capture has risen 4.4x. The raw
   mission metric hid it because `supply` moves 2-3x between arms for reasons
   that have nothing to do with selection.
2. **v0.56's founder change is the largest single move the project has made** —
   `consumedFraction` 0.258 to 0.435 — and it is recorded in `LEDGER.md` as
   "tracking toward MISS" on a 1.5% heterotrophy line it was never going to
   reach. On n=14. Nobody has looked at it since.
3. **`carrionDigest` is flat to the third decimal in every build.** Mean
   `carnivory` has not moved in 2,329 logs. That one column is the whole
   summary of six versions of work on the diet genome.

A project converging would show both columns rising. One is; one has never
moved. That is the state.

---

# Q3 — What should be abandoned

1. **The heterotrophy fraction as the primary endpoint.** Replace with
   `capture`, reported alongside `supply`, both per run with the tail rule 11
   already requires. Scoring a product of ecology and selection as if it
   measured selection is why five versions read as flat.
2. **The 5% bar, in every file that carries it.** It is above the median run's
   arithmetic maximum. `CLAUDE.md`'s mission section and
   `tools/score55.py`:43-45 both still state it.
3. **Shipping an HTML version per hypothesis.** Six builds in 35 days against
   14 of 154 config keys ever varied. Every named constant that sets the guild
   size is untouched while the shape of the code keeps changing. The next two
   moves are CFG arms, not builds.
4. **The `meatAttraction` / ATTACK line stays abandoned** — already decided,
   and confirmed here: `eFlesh` is nonzero in 126 of 2,329 logs, all of them
   v0.51. ATTACK has fed nobody since v0.52.

Not abandoned, against the last audit's ranking: the founder-pool chaining
build. See F4.

---

# CONFIRMED findings

## F1 — The mission metric is a product of three terms and the project scores the product. Two of the three are not evidence about selection.
**Confidence 9 · CONFIRMED · `[auditor-only]`**

Identity, verification and the per-version table are in Q1 and Q2. The cost of
being wrong here is the whole scoring pipeline, which is why it is first.

The specific damage: `LEDGER.md`'s "five structural versions moved it from
0.285% to 0.211%" compares products whose supply terms are 4.00% and 4.95%.
Recomputed as capture, the same two builds read 7.71% and 9.51%. The direction
of the headline finding reverses when the ecology term is divided out.

Action: `capture` and `supply` as two columns in the weekly pass; the
pre-registered lines restated against capture.

## F2 — The carnivore guild the mission needs is eight animals, and every constant that sets that number is untouched
**Confidence 8 · CONFIRMED (arithmetic + corpus) · `[cross-validated: AUDIT-DEADEND-2026-09-12.md named `worldSize` and the epsilon screen; the guild-size arithmetic from the supply term is new]`**

3.92% supply x median N 197 = 7.7 carnivores. Of the four routes to a larger
guild — arena size, upkeep, toxin loss, meat value — `worldSize` 768,
`a_base` 0.012, `a_mass` 0.020, `k_toxinHarm` 110, `toxMaxLoss` 1.15 have zero
variation across 2,329 logs; `meatValue` has been varied once, to 40, which
raised the supply ceiling from 6.73% to 15.47% (n=66) and produced the largest
survival effect in the project's history.

The deadend audit ranked `worldSize` first, at n=5, with a stated falsifier
("if `carnMax` does not move, the arena work stops there"). It has not been
run. v0.57 shipped instead.

## F3 — The pre-registered n has outrun collection by 15x for three consecutive versions, so four hypotheses have no data
**Confidence 9 · CONFIRMED · `[auditor-only]`**

Rotation dates from `git log` on `.github/workflows/experiment.yml`: v0.53
08-22, v0.54 08-29, v0.55 09-08, the v0.56 2x2 09-11, H14 09-11, H15/v0.57
09-12. Logs in the corpus by build: 343, 244, 63, 16, 0.

| version | cells | planned n/cell | achieved n/cell |
|---|---|---|---|
| v0.54 | 4 | — | ~61 |
| v0.55 | 3 | >=25 | ~21 |
| v0.56 (H11/H12/H13) | 4 | >=60 | 1-5 |
| v0.57 (H15) | 2 | >=40 | 0 |

Run length is not the cause: median days per run is 1245, 1105, 960, 1040,
1175, 942 across v0.51-v0.56 — flat. The rotation interval collapsed from 7-10
days to one day while the pre-registered n rose 2.4x.

Rule 10 says compute the SE before freezing a threshold. It is being satisfied
on paper and voided in practice: the threshold is correctly sized and then the
arm is replaced at 2-8% of its own planned n. H11, H12, H13 and H14 were all
superseded before their data existed. H15 is on the same trajectory.

This is the strongest single answer to "is the process the bottleneck". It is
not the one-change-per-version rule; that was amended. It is that the version
cadence now runs an order of magnitude faster than the evidence cadence.

## F4 — The analysis that cancelled the pool-chaining build was measured entirely inside the regime it was meant to test out of
**Confidence 8 · CONFIRMED · `[auditor-only]`**

`LEDGER.md`, 2026-09-12, "Duration does NOT rescue carnivory": across four
generation quartiles spanning 35x of evolutionary time, `carrionAttraction`
sits at 0.65-0.72x the drift yardstick, flat. The build was cancelled on that.

Every run in that 1,507-log sample has founder `carrionAttraction` 0.10. The
corpus contains 16 v0.56 logs and 0 v0.57 logs; there is no other regime in it.
Two paragraphs later the same entry states that at founder 0.10 "almost nothing
scavenges, so `carnivory` has nearly no fitness consequence".

A gene under no selection is flat at any duration. The measurement cannot
separate "duration does not help" from "nothing was under selection during the
measurement", and the entry's own mechanism argument says the second was true.
The ratio landing *below* 1.0 is the tell: an unselected gene should sit at 1.0.

Action: the duration question is open, not closed. Re-ask it inside the v0.56
symmetric configuration, where `carrionAttraction` is not purged — across 11
symmetric cells it goes 0.80 to 0.785 median, rising in 6 and falling in 5, so
the founder value is not being eroded.

## F5 — Selection on carnivory is present, weak, and scales with meat share; the cheapest lever on it has never been varied
**Confidence 7 · CONFIRMED (arithmetic and corpus) · `[auditor-only]`**

Marginal arithmetic at corpus medians (`aRate` 0.1408, `aUpkeep` 0.1122,
`aMass` 2.501, `metabolicRate` 0.895, `carnivory` 0.0716, `heterotrophy`
0.287%):

- marginal cost, from `:2124` and the `capability*(m75/upkeepRefM75)` scaling at
  `:2142`: `2*k_gut*c*(m75/3.0)*met` = **1.70e-3** energy/tick per unit
  carnivory. The `k_mixed` and `k_digest` terms are both inactive at the
  realized genotype (`c*h` = 0.050 against `mixedFree` 0.060; `c+h-1` < 0), so
  the concave-frontier diagnosis that drove v0.55's H9 does not bind at the
  genotype the population actually occupies.
- marginal benefit: `(0.70/carrionDigest) * heterotrophy * aRate` = **8.2e-4**.

Cost exceeds benefit by 2.1x; break-even at heterotrophy **0.60%** against a
corpus median of 0.287% and a p90 of 1.12%.

The corpus agrees on direction and says the coefficient is smaller than that.
Signed `Δcarnivory` over the drift yardstick, by heterotrophy band (n=1,822):

| heterotrophy | n | Δcarnivory / drift |
|---|---|---|
| 0-0.2% | 706 | +0.01 |
| 0.2-0.4% | 392 | +0.15 |
| 0.4-0.6% | 236 | +0.17 |
| 0.6-1.0% | 254 | +0.32 |
| 1.0-2.0% | 206 | +0.43 |
| >2.0% | 28 | +0.61 |

Monotone, never crossing 1.0. Selection points the right way and is roughly an
order of magnitude too weak to displace the gene in ~20 generations at Ne ~200.

**`carrionFloor` 0.30 is the largest single multiplier on that gradient and has
never been varied.** It hands 30% of carrion digestion away at carnivory 0, so
the marginal benefit carries a factor `0.70/carrionDigest` = 2.0 instead of
`1/c` = 14 at the realized genotype. Setting it to 0 raises the benefit ~7x and
moves break-even from 0.60% to ~0.09%, below the corpus median. One CFG key, no
HTML. `HANDOFF.md` §3 item 10 holds it on a rationale from v0.39.

## F6 — The mission metric omits one of the two meat channels and will score the next proposed build as a regression
**Confidence 7 · CONFIRMED · `[auditor-only]`**

`heterotrophy = eCarrion/(ePlant + eCarrion)` ignores `eFlesh`. `eFlesh` is
nonzero in 126 of 2,329 logs, all v0.51; for those runs the metric reads
**0.059%** against **0.242%** with flesh included — it drops three quarters of
the meat.

Harmless today, since ATTACK has transferred no energy since v0.52. It stops
being harmless the moment kill possession or any direct flesh transfer ships,
which is the deadend audit's named change 3. As written, `score55.py` would
score that build as a regression.

Action: one-line fix to the metric before the next build touches ATTACK.

## F7 — No committed tool can score the shipped build, two versions after the audit that flagged it
**Confidence 8 · CONFIRMED · `[cross-validated: AUDIT-PIVOT-2026-09-12.md P4]`**

`tools/score55.py:19`: `if 'invadeFrac' not in c: return None`. Every v0.56 and
v0.57 log is dropped. It is the only committed code that computes the mission
metric.

`tools/arms.py` classifies v0.56 and v0.57 arms correctly (`:16-34`) but its
output line (`:97`) prints n, survival, cv and `meatAttraction` — no
heterotrophy, no tail, and `meatAttraction` is the gene the pivot abandoned.

Rule 11 (report the tail) is declared in `CLAUDE.md` and implemented in neither
tool. `HANDOFF.md` §0.2 lists this as unresolved and it has survived two
version bumps. `CLAUDE.md`'s first section says the mission metric is
"reported every pass"; no committed code currently can.

## F8 — Compute allocation has not followed the mission
**Confidence 7 · CONFIRMED · `[cross-validated: LEDGER.md records 48.1% on seasonality; the config-coverage numbers are new]`**

Across 2,329 logs: **28 distinct configurations** (seed excluded), 65% of the
corpus on **four** of them, median 38 runs per configuration, and **53.4% of
all runs on a seasonality-varied configuration** for a question closed as H1
FORCED. 14 of 154 config keys have ever taken more than one value.

Seven configurations have n<10 — including every cell of the two most recent
pre-registrations.

---

# PLAUSIBLE

## P1 — The concave-frontier diagnosis was never binding at the realized genotype
**Confidence 6 · CONFIRMED (arithmetic) / PLAUSIBLE (that this explains H9) · `[auditor-only]`**

`k_mixed` charges `max(0, carn*herb - mixedFree)`. At corpus median carnivory
0.0716 and herbivory 0.7008, `carn*herb` = 0.0502 against `mixedFree` 0.060 —
the term is zero. `k_digest` needs `carn+herb > 1`; the realized sum is 0.772.
Both omnivory penalties are inactive in the median run and have been inactive
in every build measured here.

v0.55's H9 arm set `k_mixed` to 0 to test whether the concavity was the barrier.
It was testing the removal of a term that was already contributing nothing at
the genotype the population occupies. The arm is not wrong, it is void, in the
same way H8 was void.

## P2 — The apparent gain in `consumedFraction` may be an encounter-rate effect rather than a preference effect
**Confidence 5 · PLAUSIBLE · `[auditor-only]`**

v0.56 raised founder `carrionAttraction` and `consumedFraction` went 0.258 to
0.435. Standing corpses are 126 against 214 animals (medians, n=1,822), so an
animal is rarely far from one. The founder change could be acting through the
act lottery rather than through any improvement in finding corpses. Separating
them needs the `k_corpseDecay` arm the deadend audit named, which would move
encounter rate without touching preference. Not run.

---

# What would change the verdict

- **To "continue as is":** `tools/score55.py` scoring v0.57, capture reported
  per version with a tail, and the H15 rotation reaching n>=40 per cell before
  the next build ships. The pipeline problem in F3 and F7 is the whole gap
  between this verdict and that one.
- **To "stop":** the `worldSize` 1536 arm at n=5 leaves `carnMax` and the
  carnivore count flat *and* the `carrionFloor` 0 arm leaves `Δcarnivory/drift`
  below 1.0. Together those close both routes to a guild larger than eight, and
  no mechanism work reaches the mission after that.

---

# Appendix

## Mandatory question 4 — simplicity counterfactual

The same knowledge was available from the corpus without four of the six
builds. The three-term identity in Q1 needs `carrionMass`, `corpseRot`,
`eCarrion`, `ePlant` and `aCarn` — all five columns have been logged since
before v0.51. Computing it on the 1,537 v0.52 logs, in 2026-08, would have
given: supply 4.00%, consumed 0.215, digest 0.348, and the reading that the
digestion gene never moves while the consumption term does. v0.53 (seasonality,
53% of all compute), v0.54 (Luce arbiter) and v0.55 (invasion probe) all
targeted terms outside that identity.

Mechanisms now in the build that no current measurement justifies:
`k_choiceBeta` (the Luce arbiter — `HANDOFF.md` §0.3 already records it as
unvalidated debt and its revert condition has been met), `invadeFrac` /
`invadeGenes` (H8 withdrawn as void, the keys remain), `k_seasonPhen` (H1
returned FORCED; the mechanism is retained as a switch and 53.4% of the corpus
sits on its arms). Three of the five structural additions since v0.50 are
carrying no measurement.

The shorter path: compute the identity on the standing corpus, then vary the
constants inside it. That is two CFG arms and no builds.

## Mandatory question 5 — is the process the bottleneck?

Yes, but not the part that has been amended. One-change-per-version and the
prediction requirement are not what capped learning; both have been relaxed and
the rate did not improve. The binding constraint is F3: the version cadence
(one per day since 09-11) now runs an order of magnitude ahead of the
collection rate (~20-25 logs/day, four cells per rotation), so pre-registrations
are replaced before they can be scored. The fix is a gate, not a rule change —
**no new arm fires while a pre-registered arm is below half its planned n** —
and it costs nothing, because the runners are the same either way.

The second process defect is F7: the discipline is declared in `CLAUDE.md` and
absent from the committed tools. Rule 11's tail, the mission metric on the
current build, and the SE computation of rule 10 are all hand-work each pass.
A rule with no implementation decays into a document.

## Mandatory question 6 — what is being ignored for missing a pre-registered box?

1. **v0.56's `consumedFraction` result.** 0.258 to 0.435, the largest single
   move on the term that measures selection, filed in `LEDGER.md` as "tracking
   toward MISS" against a heterotrophy line it could not reach. Rule 12 exists
   for this and was not applied.
2. **`meatValue` 40.** Survival 92.2% vs 66.7%, p=0.0022, filed MISS because
   `carnivory` did not move. Rule 12 was written about this case and the
   replication arm (H10) was never completed — 66 logs exist, the
   pre-registration wanted 25 per cell and the arm was retired at the v0.55
   rotation.
3. **The 44 runs with mean carnivory above 0.30**, maximum 0.558, against a
   `PROGRAM-HISTORY.md` headline that "`carnivory` has never exceeded 0.16 in
   any arm of any build". The arm medians are 0.16; the runs are not.
   `runs/rot-collect/46902.json` carries 3,759 animals with mean carnivory
   0.558 and 42% of them above 0.5, sustained from day 705 to the end of the
   run. Rule 11 names this failure mode and no tool yet reports the tail.

## Confidence 4-6 findings

- **The `capability` upkeep group is scaled by `m75/upkeepRefM75` (`:2142`),
  and realized mass is 2.50 against a reference of 3.0^(4/3).** Every diet-cost
  constant is therefore charged at 0.66x its nominal value. Ratios between
  genotypes are unaffected, so no past attribution changes, but any future
  calibration of `k_gut` or `k_mixed` against the founder mass will be 1.5x off.
  Confidence 6 · CONFIRMED (arithmetic).
- **`W.scavenged` is a bite counter (`:2065`, `W.scavenged++`) while `W.eaten`
  is a mass (`:1987`, `+= bite`).** `analyze.py:499` uses `carrionMass`
  correctly, so no committed number is wrong; the naming is a trap for the next
  analysis written against the column list. Confidence 5 · CONFIRMED.
- **Kills per attack is 0.097** over the matched window (n=1,822), and
  predation is 55.6% of deaths at median. Top-down control of the herbivore
  level already exists; it is driven by an act that returns no energy to the
  actor and whose attraction term is 83% constant (`k_meatAttrFloor` 0.5). The
  mission's "carnivores control herbivores" is being met by a hardcoded
  mortality source, which is the mission test failing in a place nobody is
  looking. Confidence 6 · CONFIRMED (numbers) / PLAUSIBLE (that it matters more
  than the metric).

## Method

Corpus: `runs/rot-collect`, 2,329 JSON logs. Window days 400-800 throughout,
with runs whose animals are extinct at day 800 excluded (1,822 qualify for the
identity; 2,199 for state variables that do not need the window differenced).
Cumulative columns (`ePlant`, `eCarrion`, `carrionMass`, `corpseRot`, `eaten`)
were differenced across the window after checking each is monotone;
`clearHistory()` at `:2516` is the only reset and does not fire mid-run. Gene
deltas use the first snapshot with a live animal population as the baseline and
the last snapshot inside the window as the endpoint, normalised by the median
absolute delta of `mateChoosiness`, `parentalCare`, `pathogenResistance`.
