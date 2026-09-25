# evosim — handoff

Current state only. History is in `LEDGER.md` and in git.

## Where the project stands, 2026-09-25

Started 2026-08-08. Seven weeks, builds v0.44 to v0.58, about 3,200 result
branches on GitHub. The simulator works: deterministic per seed, matter
conserved, runs on a phone, plants and animals coexist for 800+ days in most
seeds, animals kill each other often (predation is about half of animal
deaths), and grazing does limit plants (animals eat 70-100% of plant growth in
the control).

**The mission has not been reached.** No build has produced carnivores on its
own. Across 1,700 surviving runs, the share of animal energy that comes from
meat has a median of about 0.3-0.9% depending on build, and GRAZE is 93-99% of
all actions in every arm ever run.

Most of the last four weeks went into process rather than the simulator: four
program audits in two days, a 475 KB ledger, fourteen numbered rules, and
pre-registered hypotheses whose runs were starved of seeds or never scored. The
H22 runs below sat finished and unscored for three days. The rules were cut back
on 2026-09-25 (see `CLAUDE.md`).

## What H22 showed (scored 2026-09-25, n=12 seeds per cell)

H22 started populations at the carnivore end of the diet frontier to ask whether
a carnivore peak exists that the herbivore population can't reach.

| cell | founder carn / herb | survived to day 800 | carnivory at 800 | GRAZE % | ATTACK % | meat share of intake |
|---|---|---|---|---|---|---|
| control | 0.05 / 0.60 | 8/10 | 0.12 | 93.5 | 1.29 | 0.86% |
| carn40 | 0.40 / 0.45 | 10/12 | 0.49 | 95.2 | 0.66 | 1.20% |
| carn70 | 0.70 / 0.25 | 9/12 | 0.70 | 97.9 | 0.48 | 0.90% |
| carn85 | 0.85 / 0.12 | 3/12 | 0.84 | 99.5 | 0.08 | 0.63% |

By its own pre-registered criterion this is a HIT for "unreachable peak": the
carnivore cells keep their carnivory. **That reading is wrong.** The animals keep
the gene and still graze. The carn85 population attacks *less* than the control
and gets 99.4% of its energy from plants. The `carnivory` gene only sets how well
an animal digests meat it happens to eat. It does not change what the animal
chooses to do, and since almost nothing is eaten as meat, the gene is close to
neutral and drifts wherever the founders put it. That explains why carnivory
never rises from 0.05 and never falls from 0.85.

So the question the last six versions were built around ("is the carnivore peak
absent or unreachable?") was not the right question. There is no peak to find,
because carnivory as coded barely affects fitness. What needs explaining is why
an animal with a good meat gut still chooses plants.

## Why a carnivore-gutted animal still grazes

Instrumented probe running (2026-09-25), results to follow here.

## The physics, in numbers

- A plant gives `tissueValue` 25 energy per unit mass, times `herbivory`, and
  it sits still.
- Meat gives `meatValue` 24 x `carrionValue` 0.85 x digestion (0.3 + 0.7 x
  `carnivory`), about 18 per unit mass for a strong carnivore, after the prey has
  been found, caught, damaged to death (`k_health` x its mass) and fought
  (retaliation).
- Building a unit of animal costs `energyPerMassA` 55.

Per unit mass, meat is worth about the same as leaves and costs far more to get.
In real ecosystems the gap runs the other way: animals digest meat at roughly
80-90% and plants at roughly 20-60%. `meat-rich` (`meatValue` 40) is the only
intervention that moved the meat share (0.86-0.99%) and it raised survival from
67% to 92%, but it was tested on herbivore founders, which never attacked
enough for it to matter.

## What to do next

1. **Score from behaviour.** Add a per-animal lifetime energy-by-source record
   (plant / carrion / flesh) to the log, so a predator subpopulation is visible
   even when the population average is 1%. A population mean of 1% can be 1% of
   animals eating 100% meat or every animal eating 1%, and those are different
   worlds.
2. **Fix the choice, not the gene.** The probe above says where. Whatever
   decides that an animal looks at prey should be scored in energy per tick
   against the plant option on the same terms. The attraction floor
   `k_meatAttrFloor` and the hunger term are the places to look.
3. **Test the energetics on carnivore founders.** `meatValue` 40 x the carn70
   founders is the obvious 2x2: if meat is worth more and the animals already have
   the gut, do they hunt? That separates "meat isn't worth it" from "the arbiter
   never offers it".
4. **Decide what success is.** "Heterotrophy fraction of all animal intake" caps
   out near its supply term (about 4-6%) even if every corpse is eaten. A better
   target is whether a lineage that gets most of its energy from meat persists
   for a few hundred days alongside grazers.

## Open housekeeping (needs the owner's go-ahead)

- About 20 stale files in the repo root are candidates for deletion: the
  `AUDIT-*`, `HOST-*`, `DAILY-AUDIT`, `AUDITOR-BRIEFING`, `PROGRAM-HISTORY`,
  `START-PROMPT`, `FINDINGS.md` and `INFLIGHT.json` docs, `audit.py`, the
  v0.49 and v0.57 builds (v0.57 is `k_possession` 0 on v0.58), and the old
  v0.4x phone logs and digests. Git keeps all of them.
- About 3,200 `runs/*` branches on GitHub. Pruning everything older than v0.56
  would make `git fetch` usable again. This deletes data, so it waits for the
  owner.
- `experiment.yml` on `main` still fires four seeds an hour through the H16/H17
  2x2. Keep it running until those cells reach n=40, or retarget it at item 3
  above.

## Diagnostic tools worth keeping

**Why a gene pins at a bound.** With cost `k*g^2` and benefit `b*g^p`: p<2 gives
an interior optimum and a pin means the constant is wrong; p=2 has no interior
optimum at any k, so the cost *shape* has to change; p>2 always rails high.
Don't widen the bound; the rail just moves.

**Pivot when changing an exponent.** Re-pivot the constant so the value is
unchanged at the founder value and only the slope moves, or two things changed
at once.

**Check the gene is connected before tuning it.** Does anything read it? Does
the score that reads it share a currency with its rivals? Is there an
`if (gene > x)` gate around it, which makes low values permanent? And, after
H22: does it change behaviour, or only the payoff of behaviour that never
happens?

**Inert genes are a drift yardstick.** `mateChoosiness`, `parentalCare`,
`pathogenResistance` have no readers. Express responses in founding SD before
comparing; `parentalCare` has a range 20,000 times the others and swamped the
raw average until 2026-09-22. Grep for readers before each use.

**Starvation or fecundity?** Before blaming food for an extinction, check
births per lifetime and whether the plants have collapsed into a few tiles.
