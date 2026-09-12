# AUDIT OF THE PIVOT — evosim, 2026-09-12

Adversarial audit of the **2026-09-11 pivot itself** (commits `eeff1d0`,
`37cce78`, `c60290b`), per `.claude/skills/program-audit/SKILL.md`. Target is
*not* the pre-pivot program — `AUDIT-PROGRAM-2026-09-11.md` covered that and its
PIVOT verdict is not relitigated here. Target is the rewrite that followed it:
the build, the hard rules, the tooling, the 2×2, and the redefined goal, none of
which has been reviewed by anything other than the agent that wrote them, in one
burst, inside two hours.

Confidence 1–10 on every finding; nothing below 4 is written down.
CONFIRMED = verified against data or code in the repo. PLAUSIBLE = reasoned.
Every number below was computed during this pass from `runs/rot-collect/*.json`
(2,348 logs), `runs/v53-collect/*.json`, and by instrumenting the shipped builds
directly. Scripts were ad hoc and are reproducible from the builds plus the
corpus.

---

## Verdict up front

**Do not let the 2×2 run.** The pivot's *diagnosis* is largely right and its
*prescription* is broken in four independent ways, each sufficient on its own to
waste the 240-run rotation:

1. the control cell does not reproduce the world it claims to reproduce, and its
   defect is in the direction of the hypothesis (P1);
2. the founder-prior number that motivates the whole version is wrong by one to
   two orders of magnitude, and the value that *is* 4096:1 is the new control
   cell (P2);
3. H11 is pre-registered to be indeterminate — the existing corpus already
   estimates its answer at 0.75–0.81%, inside H11's own dead zone between 0.6%
   and 1.5% — and H12 violates rule 10 (P3);
4. neither committed tool can tell the four cells apart (P4).

And underneath: v0.56 is aimed at the third-ranked constraint. Corpse **supply**
caps heterotrophy at ~1.4% even if every corpse is eaten (P5), and the pivot
abandoned the only line that moves supply (P6).

---

# P1 — The 2×2's control cell is not the historical control, and `founderGenesA` breaks it in the direction of the hypothesis
**Confidence 9 · CONFIRMED · attacks (A) and (E)**

`cfg-patches/carrion-lo.json` claims to be *"the OLD world, re-expressed as a CFG
patch ... the control that isolates the founder-symmetry change from everything
else in v0.56."* It is not.

`evosim-v0_56_0.html:1563–1571` applies `founderGenesA` **after** the founder
scatter loop and **overwrites** the drawn value:

```js
for (let j = 0; j < A_ACTIVE; j++)
  G[g+j] = clamp(mo[j] + gauss()*ASIG[j]*CFG.founderNoise, AMIN[j], AMAX[j]);
if (CFG.founderGenesA){                                        // [L0.56-2]
  for (const nm in CFG.founderGenesA){ ... G[g+gi] = clamp(CFG.founderGenesA[nm], ...); }
}
```

RNG-neutral, yes. Variance-neutral, no. I seeded 650 founders directly out of
each build (`vm` harness, same loader `check.js` uses) and measured the realized
founder population:

| cell | mean `carrionAttraction` | **SD** | distinct values among 558 founders |
|---|---|---|---|
| v0.55 default — *the actual historical control* | 0.1876 | **0.1473** | 509 |
| v0.56 default — symmetric / treatment | 0.8086 | **0.1923** | 464 |
| v0.56 + `carrion-lo.json` — *the designated control* | 0.1000 | **0.0000** | **1** |

The control cell founds as a **point mass**: every one of 650 founders carries
`carrionAttraction` = 0.100 exactly. The historical world founds with SD 0.147
spanning 0.000–0.481, because `founderMorphs` 6 (`:404`) × `morphSpread` 3.5
(`:405`) draws each morph at `START ± 0.14` before per-founder scatter.

Three consequences, all material:

- **The contrast confounds mean with variance, favouring the hypothesis.**
  Selection response is proportional to additive genetic variance. The treatment
  cell has SD 0.192 on the trait under test; the control has zero, and must
  regenerate it from mutation alone. Measured in the three v0.56 logs that have
  already landed (`runs/rot-collect/59940,59942,59943.json`, all `carrion-lo`):
  at the first gene snapshot, day 305, `carrionAttraction` SD is **0.0057–0.0114**
  against **0.0532–0.0599** in three v0.55 CONTROL runs
  (`runs/rot-collect/59680,59681,59682.json`) — a 25–100× reduction in variance
  on the one gene the experiment is about.
- **[L0.56-2] is applied in exactly the two 0.10 cells and nowhere else.** The
  second structural change is therefore perfectly confounded with one level of
  the first factor. See P7.
- **The three `carrion-lo` logs already collected are void** and should not be
  counted toward n.

**Fix, one line, RNG-neutral and variance-preserving** — re-centre the deviate
that was already drawn instead of discarding it:

```js
G[g+gi] = clamp(CFG.founderGenesA[nm] + (G[g+gi] - mo[gi]), AMIN[gi], AMAX[gi]);
```

`G[g+gi] - mo[gi]` *is* `gauss()*ASIG[gi]*founderNoise`, so no new draw is taken
and rule 7 is satisfied. It still does not restore morph spread (see P10), which
is the larger half of the variance.

---

# P2 — The "4096:1 founder prior" is wrong by 1–2 orders of magnitude, and the configuration that actually is 4096:1 is the new control cell
**Confidence 9 · CONFIRMED · attacks (A)**

`LEDGER.md:8161`, `HANDOFF.md §0.2`, the pivot commit message and
`.github/workflows/experiment.yml` all carry the same sentence: *"`plantAttraction`
founds at 0.80, `carrionAttraction` at 0.10 ... under `k_choiceBeta` 4 that is an
8⁴ = 4096:1 prior against meat before a single tick of biology."* It is the
single most-quoted justification for v0.56.

It is computed from the `START` column of `AG_DEF` and ignores how founders are
actually built. Realized, across six seeds, 650 founders each, measured from the
shipped builds:

| seed | build | mean plant | mean carrion | ratio | **E[plant⁴]/E[carrion⁴]** (the actual Luce weight ratio) |
|---|---|---|---|---|---|
| 1337 | v0.55 default | 0.825 | 0.188 | 4.4 | **63** |
| 909 | v0.55 default | 0.795 | 0.133 | 6.0 | **316** |
| 4001 | v0.55 default | 0.713 | 0.111 | 6.4 | **163** |
| 59940 | v0.55 default | 0.792 | 0.214 | 3.7 | **37** |
| 7 | v0.55 default | 0.822 | 0.089 | 9.3 | **1638** |
| 12345 | v0.55 default | 0.844 | 0.096 | 8.8 | **1617** |
| 1337 | v0.56 default | 0.825 | 0.809 | 1.02 | 0.86 |
| 909 | v0.56 default | 0.795 | 0.830 | 0.96 | 0.91 |
| 1337 | **v0.56 + carrion-lo** | 0.825 | 0.100 | 8.25 | **4759** |
| 12345 | **v0.56 + carrion-lo** | 0.844 | 0.100 | 8.44 | **5273** |

Two things fall out.

**The old world's prior against meat was 37–1,638:1, median ≈ 240 — not 4096:1.**
The founder mean is 0.188, not 0.10, because morphs are drawn N(0.10, 0.14) and
clamped at 0, which truncates the left tail and lifts the mean 88%. And because
the Luce weight is score⁴, the ratio is dominated by the right tail that the
point-value patch deletes.

**The configuration that genuinely is ~4096:1 is `carrion-lo.json`** — 3,155 to
5,273 across seeds. The pivot's motivating number describes an artifact the
pivot itself created, not the world it set out to fix.

This does not make v0.56 pointless — a 240:1 prior is still a prior — but it is
a 17× overstatement of the thing being removed, it appears in four documents,
and it is the sentence a future reader will use to justify the next founder
change. It has to be corrected.

Secondary, same measurement: v0.56's "symmetry" does not produce weight parity
either — `E[p⁴]/E[c⁴]` is 0.74–1.39 across seeds, i.e. the symmetric build
sometimes favours *meat*. With only 6 morphs, the realized founder mean of any
gene is a 6-sample draw and varies enormously run to run. That is a fact about
the design, and P3 turns it into an instrument.

---

# P3 — H11 is pre-registered to be indeterminate; the corpus already estimates its answer, and the answer lands in H11's own dead zone. H12 violates rule 10.
**Confidence 9 · CONFIRMED · attacks (C)**

### The instrument the project already owns

Because `founderMorphs` is 6, realized founder `carrionAttraction` varies across
seeds from **0.007 to 0.497** with no CFG patch at all. That is a 70× natural
dose range on precisely the variable H11 manipulates, already run 1,388 times at
`meatValue` 24 / floor 0.5. Measured (matched window days 400–800, survivors):

| founder `carrionAttraction` bin | n | median ca | corpse consumed % | **median heterotrophy %** | corpse flux | carnMax |
|---|---|---|---|---|---|---|
| 0.00–0.06 | 220 | 0.039 | 13.3 | **0.196** | 0.0918 | 0.161 |
| 0.06–0.10 | 353 | 0.081 | 22.4 | **0.234** | 0.1067 | 0.210 |
| 0.10–0.16 | 509 | 0.124 | 23.8 | **0.292** | 0.0798 | 0.171 |
| 0.16–0.30 | 283 | 0.195 | 33.9 | **0.523** | 0.1066 | 0.163 |
| 0.30–1.00 | 23 | 0.327 | 47.9 | **0.810** | 0.0685 | 0.170 |

Log-log fit, n=1,387: **elasticity 0.526 ± 0.052**, r = 0.294 (t = 11.45).
Extrapolated to `carrionAttraction` 0.80: **0.75%**. Empirical top bin
(ca ≥ 0.30, n=23): median **0.810%**, max 1.82%, 2/23 above 1.5%, **0 above 5%**.

Both estimates land **between H11's MISS line (0.6%) and its HIT line (1.5%)**.

### What that does to the pre-registration

Bootstrapped 3,000 times, resampling the empirical elevated-attraction and
control distributions, scaled so the symmetric cell has median 0.75% and with
the floor-off multiplier fixed at the **measured** 0.66 (see P6):

| n per cell | H11 HIT | H11 MISS | **H11 indeterminate** | H12 HIT | H12 MISS | H12 indeterminate | interaction z |
|---|---|---|---|---|---|---|---|
| 46 (60 runs × 77% survival) | 0.0% | 10.8% | **89.2%** | 41.2% | 15.9% | 42.9% | 0.96 |
| 60 | 0.0% | 8.3% | **91.7%** | 40.6% | 11.3% | 48.1% | 1.07 |
| 120 | 0.0% | 2.6% | **97.4%** | 36.5% | 5.4% | 58.1% | 1.46 |

- **H11 returns no verdict ~92% of the time at its planned n**, and *more* often
  as n grows, because larger n concentrates the estimate inside the 0.6–1.5 gap.
- **The interaction — which `LEDGER.md` calls "the point" — has z ≈ 1.07.** No
  criterion, no threshold and no power calculation was ever written for it. It
  is unpowered at 240 runs and still unpowered at 480.
- **H12 breaches rule 10 directly.** Its HIT band is ±30% relative on a
  ratio of two medians; I measured the SD of that ratio under the null (both
  cells drawn from the same distribution) at **0.286 at n=60** and **0.365 at
  n=40**. The threshold is *at* the SD of its own statistic. Under a true ratio
  of exactly 1.0, H12 fails its own HIT test 26% of the time at n=60, 35% at
  n=40. Rule 10 was introduced in the same commit and in the same LEDGER entry
  that says *"this time the threshold is checked against its SE."*

### Rule 10 was applied to the wrong statistic

`LEDGER.md` sets the gate as *"n ≥ 60 per cell (set by rule 10: at n=25 the
Fisher power against a 15-point survival difference is 14%)"* — a power
calculation on **survival**, while the line above it declares *"Primary endpoint
is the mission metric, not survival."* The SE of the primary endpoint was never
computed. It is:

| n | SE(median heterotrophy), control scale | SE, elevated scale |
|---|---|---|
| 25 | 0.094 pp | — |
| 40 | 0.0717 pp | 0.111 pp |
| 60 | 0.0583 pp | 0.092 pp |

Also unspecified: whether "n ≥ 60 per cell" is 60 *runs* or 60 *survivors*. At
the corpus survival rate (77.0%, n=1,577) those differ by 14 survivors and by
~20% on the SE.

---

# P4 — Neither committed tool can score the 2×2, and rule 11 is declared but not implemented
**Confidence 9 · CONFIRMED · attacks (C), (E)**

`tools/score55.py` is the weekly scorer, the only place the mission metric is
computed, and the file the pivot edited. Its `arm()` keys on `invadeFrac`,
`k_mixed`, `meatValue`. v0.56 runs have `invadeFrac` 0, `k_mixed` 0.018,
`meatValue` 24 in **all four cells**. Verified against the three landed logs and
against synthetic cfgs for the other two cells:

```
59940 -> score55.py arm: CONTROL   | true cell: carrionAttraction 0.1  floor 0.5
59942 -> score55.py arm: CONTROL   | true cell: carrionAttraction 0.1  floor 0.5
59943 -> score55.py arm: CONTROL   | true cell: carrionAttraction 0.1  floor 0.5
v0.56 default   -> CONTROL
v0.56 flooroff  -> CONTROL
```

All four cells, plus v0.55 CONTROL, pool into one bucket. The next weekly pass
would print a single confidently wrong number.

`tools/arms.py` *does* classify the cells (uncommitted change, in the working
tree), but it prints `n / surv% / cv / meatAttr` and **no heterotrophy at all** —
against `CLAUDE.md`'s "Report it every pass."

Rule 11's tail statistics — *"the fraction of runs above 5% heterotrophy, and the
maximum"*, promised in H11's own text — appear in neither tool. Grep for `p90`,
`carnMax` or any tail statistic in `tools/arms.py` returns nothing.

Related, and it will bite the *next* experiment: `arms.py` labels a cell by
`fg.get('carrionAttraction', 0.80)`. Any future `founderGenes` arm that patches
a different gene — which the amended rule 1 explicitly invites — is silently
labelled the 0.80 control cell.

---

# P5 — v0.56 is aimed at the third-ranked constraint; corpse supply caps the metric below H11's own HIT line
**Confidence 8 · CONFIRMED · attacks (D)**

First, the prior audit's three numbers re-derived independently (v0.54+v0.55
CONTROL, n=47, matched window 400–800, medians):

| quantity | prior audit | this audit |
|---|---|---|
| generations at day 800 | 13.9 | **19.2** (window 400–800: 15.8) |
| carnivore niche at herbivore-equivalent intake | 8–21 individuals | **10.5**, 4.09% of N |
| corpse mass flux / tick | 0.1079 | **0.0995** |
| corpse mass consumed | 32.5% | **22.4%** |

All three confirmed in order of magnitude. (Corpse-consumed is *worse* than
reported — see P10.)

Now the decomposition nobody has run. On 500 randomly sampled survivors, in logs:

```
corr(log hetero, log consumed-fraction) = +0.940
corr(log hetero, log corpse-flux)       = +0.412
corr(log hetero, log(flux*cons/N))      = +0.927   (R^2 = 0.860)
corr(log consumed-fraction, log founder carrionAttraction) = +0.355  (R^2 = 0.13)
corr(log corpse-flux,       log founder carrionAttraction) = -0.006
```

Heterotrophy is `supply × consumption / population`, to R² 0.86. The founder
prior explains **13%** of the consumption term and **nothing** of the supply
term. It is a real lever on one of three factors.

**And the supply term caps the answer.** For each of 102 control-arm survivors I
computed the heterotrophy that would obtain if **100% of the corpse mass produced
were eaten**, holding plant intake and corpse production fixed:

| scenario | median ceiling | runs above H11's 1.5% HIT line |
|---|---|---|
| every corpse eaten, at the **evolved** carnivory (0.077) | **1.43%** | 48 / 102 |
| every corpse eaten, at carnivory **0.85** | 3.51% | 100 / 102 |

The perfect-scavenging ceiling at the carnivory that actually evolves is
**below H11's HIT line**, and the perfect-scavenging *and* perfect-digestion
ceiling is still below the 5% bar the prior audit set as "the mission is
reachable." Consumption climbs 13.3% → 47.9% across the corpus's founder range
while flux stays flat (0.069–0.107) — so the feedback that might rescue this
(more scavenging → more kills → more corpses) does not operate in the observed
range.

**Which constraint binds, in order:** (1) corpse supply — sets a ~1.4% ceiling at
the evolved genome; (2) duration/`carnivory` — lifting the ceiling to 3.5%
requires the 27-mutational-SD displacement the prior audit computed, against
19 generations; (3) the founder prior — worth ~2.5–3× on a number that needs
17×. v0.56 addresses (3). It cannot reach the mission however well it works, and
the single-seed smoke result at 0.447% is exactly what that predicts.

---

# P6 — The abandoned ATTACK line is the corpse-supply lever, i.e. the one that binds
**Confidence 8 · CONFIRMED · attacks (E)**

The pivot's founding insight is correct: `ACT_ATTACK` transfers no energy. The
inference drawn from it — *"the `meatAttraction`/ATTACK line is **abandoned**"* —
does not follow. ATTACK is not the demand side of the trophic link; it is the
**supply** side, and supply is the ceiling (P5). Predation is 56–64% of deaths.

Matched arms from the same rotations:

| arm | heterotrophy | corpse flux | consumed % | predation share | killMass/tick |
|---|---|---|---|---|---|
| v0.54 CONTROL (n=35) | 0.267% | 0.0995 | 23.6 | 56.1% | 0.0464 |
| v0.54 beta-flooroff (n=31) | **0.176%** | **0.0673** | 18.1 | **24.5%** | 0.0137 |
| v0.53 CONTROL (n=55) | 0.360% | 0.1242 | 25.4 | 60.8% | 0.0852 |
| v0.53 seasonless-flooroff (n=46) | **0.261%** | **0.0880** | 21.9 | **24.4%** | 0.0179 |

Turning off `k_meatAttrFloor` — an ATTACK constant on an act that "feeds nobody" —
cuts corpse flux ~30% and heterotrophy 27–34%. The two other arms that ever
moved the mission metric moved it the same way: `meat-rich` (flux 0.1631,
heterotrophy 0.863%) and `mixed-flat` (flux 0.1780, heterotrophy 0.542%) both
have the highest corpse fluxes in the corpus.

This also pre-computes H12. The historical floor-off/floor-on heterotrophy ratio
is **0.66** (v0.54) and **0.72** (v0.53) — straddling H12's 0.70 HIT boundary,
with a between-block spread larger than the gap. H12 is a coin flip on data the
project already holds.

---

# P7 — Rule 3's amendment states a condition the version it permits does not meet; rule 1's amendment drops the clause that made it safe
**Confidence 8 · CONFIRMED · attacks (B)**

Per-amendment, as requested.

**Rule 3 — rationalisation as applied.** The general principle ("a 2×2 with
matched arms buys attribution that serialisation buys with a week of latency") is
defensible and I would not drop it. But the specific claim — *"the rotation is a
2×2 factorial that separates them"* — is false. The 2×2 is
`{carrionAttraction founder} × {k_meatAttrFloor}`. The second factor is a
pre-existing CFG constant, **not** [L0.56-2]. [L0.56-2] appears in no cell as a
factor; it is the delivery mechanism for one level of factor 1, applied in
exactly the two 0.10 cells. Per P1 it has a large side effect on the outcome. So
the amendment was written in the same commit as the version it permits, its
stated condition is not met by that version, and the confounding it claims to
prevent is present in it. Either add a fifth arm that runs `founderGenesA:
{carrionAttraction: 0.80}` against the v0.56 default (same realized genome under
the fix in P1; a genuine no-op check on [L0.56-2]), or ship the two changes
serially.

**Rule 1 — justified in direction, under-specified in the one way that matters.**
The evidence is real and I re-verified the sharpest part of it: `carrionFloor`
(0.30), `carrionValue` (0.85) and `k_corpseDecay` (0.0008) are **identical in all
2,348 logs** — never varied once, despite `cfg-patches/screen-carrionfloor.json`
existing since v0.49. A rule that produced that is a rule worth amending. But the
prior audit's recommendation was *"one prediction covering the batch, **with the
decision rule stated as a family-wise criterion before firing**"*, and the shipped
text (`CLAUDE.md`, rule 1) keeps the example and drops the multiplicity clause. A
20-constant screen against a fixed per-constant threshold, on a right-skewed
statistic with SE 0.058 pp at n=60, will return false positives by construction.
Rule 1 existed to stop fishing; the amendment reopens it one level up. One
sentence restores it.

**Rules 10, 11, 12 — well-evidenced, not self-serving, and each constrains rather
than licenses.** No objection to any of the three as written. They are, however,
already being broken by the version that introduced them: rule 10 by H12 and by
H11's n-gate (P3), rule 11 by the tooling (P4).

---

# P8 — The mission metric can reach its ceiling with no carnivore evolving, because `carrionFloor` 0.30 is itself a hardcode — and it has never been varied
**Confidence 7 · CONFIRMED · attacks (F)**

`carrionDigest()` (`evosim-v0_56_0.html:1639`) is
`carrionFloor + (1 - carrionFloor)*carnivory`, with `carrionFloor: 0.30`
(`:554`). An animal with `carnivory` 0 extracts 30% of meat value with no
adaptation whatsoever. Heterotrophy is therefore satisfiable by **behaviour
alone**, and the project's own mission test — *if a result had to be written into
the code, it doesn't count* — applies to the 0.30.

The smoke run is the demonstration, and the LEDGER did not report this half of
it. From `v55c.json` / `v56.json` (seed 909, matched harness, the logs the
commit is based on):

| | v0.55 | v0.56 |
|---|---|---|
| heterotrophy | 0.402% | 0.548% |
| corpse consumed | 14.7% | **30.1%** |
| final `carrionAttraction` | 0.149 | **0.706** |
| final **`carnivory`** | 0.0395 | **0.0083** |
| `carnMax` | 0.177 | **0.128** |

Founder symmetry raised the *behavioural* gene 4.7× and **lowered the
physiological one 4.8×**, with the population-maximum carnivory falling too.
n=1, but the corpus agrees: `carnMax` is flat at 0.16–0.21 across an 8× range in
founder `carrionAttraction` (P3 table). Attraction and digestion are decoupled
by the floor, and relaxing the need to specialise is what a 30% free extraction
does.

So H11's success state is "herbivores that also eat corpses", not a trophic
level. It is not a reason to drop the metric — heterotrophy does track
population health and carnivory positively (decile 1 → 10: mean N 169 → 222,
evolved carnivory 0.0585 → 0.1180, GRAZE 98.6% → 91.5%), so it is not a
starvation artifact. It is a reason to (a) report `carnMax` and the carnivory
histogram tail alongside it, which rule 11 already demands and neither tool
prints, and (b) run the `carrionFloor` arm that has been sitting in
`cfg-patches/` for seven versions before running a fourth attraction experiment.

---

# P9 — Three prior-audit findings were never answered, and one of them undermines the new design
**Confidence 8 · CONFIRMED · attacks (E)**

`SKILL.md` step 5: *"Answer every surfaced finding in writing in `LEDGER.md`:
accept or reject, each with a reason."* The pivot entry answers F1–F7, Q1, Q4,
Q5. It does not mention **F8, F11, F12, F13** or the A1–A5 appendix at all. F8 is
moot (H8 withdrawn). The other three are not.

**F12 is the dangerous one.** It showed that v0.54 CONTROL and v0.55 CONTROL —
**bit-identical code, no treatment** — differ on evolved `carnivory` at Welch
t = 3.02, p ≈ 0.005, a block-to-block offset larger than most treatment effects
in the project. `.github/workflows/experiment.yml` then assigns the v0.56 cell by
`case $(( github.run_number % 4 ))` and derives all four seeds of a tick from the
same `run_number` (`base=$(( 40000 + run_number * 20 ))`). Verified against the
landed logs: seed 59940 → run_number 997 → 997 % 4 = 1 → `carrion-lo`, and 59942
and 59943 are the same tick and the same cell. So **cell is perfectly confounded
with dispatch block**, which is the exact variable F12 showed moves the headline
metric under no treatment.

**The fix is free and large.** The sim is deterministic per seed, and
`founderGenesA` is applied *after* the RNG draws, so all four cells share a
bit-identical founding world at a given seed. Running the **same** seed list
through all four cells — common random numbers — converts the 2×2 into a
within-seed factorial and removes the seed variance that currently dominates
everything (SD of log heterotrophy ≈ 0.91 across the corpus). It costs one
change to the workflow's seed derivation and is the single largest power gain
available anywhere in this design. n ≥ 60 was calculated for an *unpaired*
Fisher test; paired, far fewer seeds resolve far more.

**F11** (early overshoot predicts extinction: mean animal age r_pb +0.45, cv of N
−0.37, population size −0.26, against the "unexplained 70% survival ceiling")
was the strongest cross-run signal in the prior audit and is now unowned.
**F13** (the `k_choiceBeta` → argmax revert is predicted to drive heterotrophy
toward zero, because the 1.3% stochastic tie-break is where all the meat energy
comes from) mattered because `HANDOFF.md §0.3` still carries a standing decision
to do that revert in v0.56. The v0.55 block was never scored, the revert was
neither done nor cancelled, and the debt is now invisible.

---

# Appendix — confidence 4–6

- **A1 [6, CONFIRMED]** `founderGenesA` silently ignores an unknown gene name
  (`if (gi === undefined) continue`, `:1566`). A typo'd patch runs as the control
  and produces a valid-looking log. One `console.warn` or a `check.js` assertion.
- **A2 [6, CONFIRMED]** `founderGenesP` ships and is used by no patch; the plant
  half of [L0.56-2] is untested.
- **A3 [6, CONFIRMED]** `check.js` calls `seedAnimalFounders(80)` at defaults
  only (`:236`), so the `founderGenes` path never executes. "check.js passes all
  six stages" says nothing about [L0.56-2] — the same vacuous-check pattern rule 7
  was written for.
- **A4 [6, CONFIRMED]** [L0.56-2] can only express a **point mass**, so the
  design the prior audit actually recommended — *"randomise the four attraction
  genes uniformly on [0,1] at founding"*, which turns the founder value into a
  measured covariate instead of a constant and would settle H11 in one arm — is
  still unreachable after the version whose stated purpose was making the genome
  reachable. Accepting a `[min,max]` pair or a `*_sd` key would fix it.
- **A5 [6, CONFIRMED]** *"67.5% of corpse mass rots uneaten"*, quoted in
  `LEDGER.md`, `HANDOFF.md §0.2` and `CLAUDE.md`, measures **76.4%** in v0.54
  CONTROL (n=35) and **80.9%** in v0.55 CONTROL (n=12) on the matched window.
  The claim understates the project's own best evidence for its own thesis.
- **A6 [5, CONFIRMED]** H11's statistic is *"median heterotrophy in the symmetric
  cells"* — plural, pooled across the floor factor — while H12 asserts that same
  factor moves that same statistic by ~34%. Pooling drags H11's number down ~17%,
  which matters when the whole question is whether it clears 0.6%.
- **A7 [5, CONFIRMED]** `CLAUDE.md`'s deletion criterion for
  `evosim-v0_55_0.html` is *"once H11/H12 are scored at n ≥ 60 per cell"*. Per P3
  that condition has an ~8% chance of ever being met, so the revert target is
  effectively pinned by a criterion that cannot fire. Tie it to a date or to a
  decision, not to a scoring event that will not happen.

---

# What I did not find

- No error in the ACT_ATTACK / ACT_SCAVENGE energy-path reading. It is correct
  and it was the right thing to notice.
- No evidence the mission metric is gamed downward by starvation: it rises with
  population size and with evolved carnivory across deciles (P8).
- `eFlesh` is 0 by design (`evosim-v0_56_0.html:828`), so dropping it from the
  metric relative to the prior audit's version changes nothing.
- The v0.55 → v0.56 diff is clean: 20 insertions, 2 deletions, nothing else
  moved. The build change is exactly what it claims to be.
- Rules 10, 11 and 12 are honest constraints and I found no self-serving content
  in them.

---

# VERDICT

**HOLD THE ROTATION, THEN RE-RUN IT PAIRED.** Not a second pivot — the pivot's
reading of the code was right and the mission metric is a genuine improvement.
But the instrument it built to test that reading is broken in four independent
places, and three of the four break in the direction of the hypothesis. Fix the
`founderGenesA` variance defect (P1, one line), correct the 4096:1 figure in the
four places it appears (P2), re-write H11/H12 with thresholds derived from the
corpus estimate of 0.75–0.81% rather than from aspiration and with a stated
criterion for the interaction (P3), teach `score55.py` the four cells and print
the tail rule 11 already requires (P4), and switch the workflow to common random
numbers across cells (P9). Then the 240 runs are worth firing. Before all that,
stop and answer the question P5 and P6 raise: the ceiling is corpse **supply**,
the ATTACK line is what moves supply, and it was just abandoned.

**What would change this verdict.** One number, and the rotation will produce it
within days: if the first ~15 `carrionAttraction` 0.80 / floor-ON seeds come back
with a median heterotrophy above **~1.2%**, then the 0.526 elasticity and the
1.43% perfect-scavenging ceiling are both wrong, the founder prior really was the
binding constraint, and P3/P5/P6 collapse together. Equally, if corpse flux is
measured to *rise* with founder `carrionAttraction` in those seeds — it does not
in the existing 1,388 (r = −0.006) — the supply ceiling is not fixed and P5 is
wrong. Everything else here is arithmetic on code and logs already in the repo
and does not depend on any run.

---

# Addendum — three commits landed while this audit ran

`2aebac4` (arms.py cells), `6fa47b3` (duration does not rescue carnivory;
pool-chaining cancelled), `38082ab` (STYLE.md). Checked against the findings
above; nothing is retracted.

**Confirmed and already fixed by `6fa47b3`.** Generations are ~19.5, not 13.9 —
I measured 19.2 independently on v0.54+v0.55 CONTROL (n=47) before seeing that
commit. Agreement.

**P4 still stands after `2aebac4`.** That commit is the `arms.py` change that was
already sitting uncommitted in the working tree when this audit began. It does
not touch `tools/score55.py`, whose `arm()` still returns `CONTROL` for all four
v0.56 cells, and `arms.py` still prints no heterotrophy and no tail statistic.
Both halves of P4 are live.

**New finding: the corpse-uneaten figure has now been stated twice and neither
value reproduces.** `6fa47b3` corrects 67.5% to **53.0%**. I measured it three
ways on a 300-run random sample of survivors, from the only conservation-
consistent pair of columns (`carrionMass` eaten vs `corpseRot`):

| formula | median uneaten |
|---|---|
| window 400–800, `corpseRot/(carrionMass+corpseRot)` | **79.4%** |
| full-run cumulative, same ratio | **76.4%** |
| mass-weighted aggregate over 600 runs, window | **71.7%** |
| `1 − carrionMass/killMass` (wrong denominator — excludes natural deaths) | 59.8% |

Nothing gives 53.0%. This is not cosmetic: the uneaten fraction is exactly the
headroom term in P5's ceiling calculation, so whichever number is right changes
the ceiling. **Confidence 7 · CONFIRMED.** Publish the formula next to the
figure.

**`6fa47b3`'s "scale does not bind" answers a different question than the one
the prior audit asked.** Heterotrophy is `flux × consumed / N` (P5, R²=0.86), so
flatness across N is close to arithmetic — flux scales with N and the ratio
cancels. The prior audit's scale claim was about *absolute* niche size (≈10
carnivores, a drift problem), which a ratio cannot test. The statistic that can
is the carnivory tail. I ran it, and it supports the conclusion by the right
measure:

| N quartile | n | median N | heterotrophy % | `carnMax` | % of animals above carnivory 0.5 |
|---|---|---|---|---|---|
| 1 | 382 | 89 | 0.245 | 0.141 | **0.0000** |
| 2 | 382 | 182 | 0.305 | 0.173 | **0.0000** |
| 3 | 382 | 285 | 0.274 | 0.163 | **0.0000** |
| 4 | 382 | 453 | 0.358 | 0.186 | **0.0000** |

A 5× range of N moves the population-maximum carnivory from 0.141 to 0.186 and
never puts a single animal past 0.5. Caveat that belongs in the LEDGER row: this
is *observational* N variation, generated by seed and arm, not a scale
manipulation — `worldSize`, `animalFounders` and every productivity constant are
still identical in all 2,348 logs. The conclusion is well supported for N; it is
not yet a test of the shipped world's size.

**`6fa47b3`'s coadaptation-trap reading strengthens P5 and P8, and weakens the
case for running the 2×2 as written.** If `carrionAttraction` and `carnivory` are
each unselectable while the other is near zero, and `carnivory` is below drift at
every duration, then the founder-symmetry arm moves one member of the pair and
leaves the other in the same trap — which is precisely what the smoke run shows
(`carrionAttraction` 0.149 → 0.706, `carnivory` 0.0395 → **0.0083**, P8). The arm
that tests the trap is `founderGenesA: {carrionAttraction: 0.80, carnivory: 0.60}`
— both members lifted together, which is the one thing [L0.56-2] is genuinely
good for and which is not in the rotation. Run that before, or instead of, a
second week of the current 2×2.
