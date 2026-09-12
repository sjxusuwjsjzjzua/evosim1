# Host self-findings — general program audit, 2026-09-12

Written BEFORE the auditor for this pass runs, and committed first, so the
cross-validation tags mean something. Confidence 1-10 per
`.claude/skills/program-audit/SKILL.md`; nothing I would score 1-3 is written
down. CONFIRMED = computed this pass against the corpus or the build.
PLAUSIBLE = reasoned.

Corpus: all 2,585 `runs/*` branches re-fetched this pass, 2,329 standing logs
plus 32 arm logs collected via `tools/collect.sh`. Window filters are stated per
finding. Scripts were ad hoc and reproduce from the corpus plus the build.

---

## GF-1 — Killing and eating are decoupled, and the design note that decoupled them misreads the mission test
**Confidence 9 · CONFIRMED · this is the finding I would act on first**

Measured over days 400-800, 1,360 runs with at least 20 animals throughout:

- predation is **56.4% of all animal deaths** (median; p10 27.5%, p90 78.7%)
- **13.3% of the mass of dead animals is ever eaten** (median; p90 31.7%)
- 150 corpses stand at any moment against ~280 live animals

So the interaction the mission asks for — animals killing animals at a rate that
governs herbivore numbers — **already happens, at scale, in the shipped build.**
What does not happen is the energy return. `evosim-v0_57_0.html:2020-2040`
deposits damage and moves no mass, and its comment says feeding the killer
"would be a hardcode". That is a misreading. The mission test forbids writing a
*behaviour* into the code; it does not forbid *physics*. Photosynthesis,
digestion and toxin loss are all energy transfers written into the source and
none of them is a hardcode. A predator that eats what it kills is the same kind
of statement.

The consequence is structural: the payoff for an attack is a corpse on a shared
tile, reachable only by winning a second, independent arbiter decision gated by
`carrionAttraction` (founder 0.10, below the drift yardstick in every version).
Attacking is privately costly — retaliation at `k_retal`, double stamina drain,
halved speed, 10.5 attacks per kill — and its benefit is a public good. A
strategy whose cost is private and whose benefit is common cannot be selected
for. **Five versions of work on attack propensity were aimed downstream of this.**

## GF-2 — The mission metric does not detect the mission
**Confidence 9 · CONFIRMED**

75 of 2,329 standing runs (3.2%) end with a majority of the animal population
above carnivory 0.33. Nine end at **100%**. Examples, all at shipped defaults
with `invadeFrac` 0:

| log | version | animals | mean carnivory | heterotrophy |
|---|---|---|---|---|
| `58681.json` | 0.54.0 | 339 | 0.979 | 1.66% |
| `53642.json` | 0.52.0 | 2,287 | 0.506 | 0.52% |
| `59640.json` | 0.55.0 | 763 | 0.471 | 1.06% |
| `49281.json` | 0.52.0 | 771 | 0.518 | 1.39% |

A population whose mean carnivory is 0.979 scores 1.66% on the mission metric —
inside the range control runs reach on noise. The metric is a population-mean
energy ratio, so a carnivore guild at any realistic share of the population
cannot move it; and a high carnivory gene without the attraction genes to match
does not produce a carnivorous diet, which is why these worlds still graze
79-93% of the time. **The project has been steering on a number that a
fully carnivorous genome barely moves, and reporting it every pass as required.**
Rule 11 named exactly this failure for arm medians; the same argument applies to
the metric itself and was not extended to it.

## GF-3 — "Carnivory has never moved" is false as stated, and the corpus has said so since v0.51
**Confidence 8 · CONFIRMED**

`HANDOFF.md` §0.3 states carnivory sits at "≈0.06 in every arm ever measured"
and §0.2 that it is "below drift at 0.49-0.84x". At day 800 that is right
(median 0.073, n=1,360). It is not right about the corpus: `carnMax` reaches
0.825, mean carnivory reaches 0.558 at day 800 and 0.801 at day 1600, and the
75 runs in GF-2 cross versions 0.51 through 0.55 — including arms scored MISS on
their medians. Three versions were motivated by a claim of universality that the
tail contradicts.

## GF-4 — Corpse supply is not the constraint, and `AUDIT-DEADEND` P5 should be re-checked before anything is built on it
**Confidence 7 · CONFIRMED against the corpus, contradicts a live audit finding**

P5 says corpse **supply** caps heterotrophy at ~1.4%. Measured: 87% of the mass
of dead animals is never eaten and 150 corpses sit uneaten at any instant. The
binding term is `consumedFraction` (0.133 measured here, 0.194 in P5), which is
a demand quantity, not a supply one. Both readings can produce the same ceiling
arithmetic, but they point at opposite interventions — P5's named constants
(`k_corpseDecay` down, `corpseMin` up) add supply to a world that is already
throwing supply away.

## GF-5 — The scoring window ends before half the simulated time and before the strongest signal
**Confidence 7 · CONFIRMED, effect real but smaller than it first looks**

Standing jobs run to 1,600 days; every score uses days 400-800. Paired within
run over the 213 runs that reach day 1600: heterotrophy 0.284% -> 0.352%
(+24%), mean carnivory 0.078 -> 0.110 (+41%), and the tail widens far more —
p99 heterotrophy 1.79% and max 2.99% late against p90 0.95% early. Only 52% of
runs rise, so this is a fatter tail rather than a trend, which is the
regime rule 11 says to report. Half of the compute already spent is unscored,
and scoring it costs nothing.

## GF-6 — Auditing now consumes more of the project than the biology does
**Confidence 8 · CONFIRMED**

Ten top-level markdown files are audit or findings documents; `LEDGER.md` is
447 KB. Three program audits ran in two days and returned three different
verdicts — PIVOT (09-11), "do not let the 2x2 run" (09-12), ITERATE WITH NAMED
CHANGES (09-12) — and the named changes of the third have not been run. The
marginal audit is now re-deriving the previous audit rather than the world. This
pass is the fourth; it should be the last for a while, and its output should be
one shipped change, not a fifth document.

## GF-7 — 130 of 156 CFG constants have still never been varied
**Confidence 6 · CONFIRMED**

26 distinct keys appear across the 51 committed patches (the "11 ever varied"
figure in `HANDOFF.md` is stale and too harsh). `k_corpseDecay`, `corpseMin`,
`carrionValue`, `k_health`, `k_attack`, `nutrientPerMass`, `tissueValue`,
`satiate*` and the whole plant-defence block have never been touched. Amended
rule 1 explicitly permits a single screening prediction over a block of them and
no screening batch has been fired since the amendment.

---

## What I got right, so it is on record before the auditor argues otherwise

v0.57 is well aimed. The MVT guard at `:1916` discards the entire scan —
SCAVENGE, ATTACK and FLEE included — for any animal already grazing an adequate
plant, which is the mechanical reason `carrionAttraction` never expressed and so
never selected. Making it a gene is the correct move by the mission test, and
the `k_mvtScale` 0 identity check against v0.56 is the best verification work in
the project's history. GF-1 and GF-2 do not argue against v0.57; they argue that
it is not sufficient on its own and that H15 will be scored by an instrument
that cannot see its result.
