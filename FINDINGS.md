# evosim — current findings

Current believed-true claims only, one line each, with `n`, effect size,
date last tested, and confidence. **A walked-back claim is edited or
deleted here, not just corrected later in `LEDGER.md`.** This file answers
"what do we actually know right now" in one read; `LEDGER.md` is the
archival chronology — consult it for the reasoning and the walk-backs, but
this file is what a new session should trust for current state.

Added 2026-08-10 per an external audit finding: a 100KB+ chronological
narrative with corrections woven in is the wrong shape for a project that
has already documented two reversals (gutcost combo, the aSize0
hypothesis) in a single session — it's exactly the format where a future
reader re-adopts an early optimistic claim and misses the later walk-back.

Confidence levels: **HIGH** (mechanistic, verified by a real control, not
just a small-n comparison) / **MODERATE** (direction confirmed, magnitude
or generality still open) / **LOW** (n too small to trust, included
because it's the current best guess, not because it's solid) /
**RETRACTED** (kept visible with the retraction reason, not deleted
silently — deleting a retraction would recreate the exact problem this
file exists to prevent).

---

## Structural / mechanical (build correctness, not ecology)

- **`P.hi`/`AN.hi` occupied-slot-list fix (v0.49) is RNG-neutral in effect,
  not RNG-exact in draw sequence.** Verified via matter conservation
  (exact, both arms) and absence of *consistent* directional bias across
  2 seeds — individual seed outcomes moved substantially and in opposite
  directions, expected chaos from an order-sensitive change, not
  evidence of a bug. **Confidence: HIGH** (mechanistic argument + control
  check, not an ecological claim). Full detail: LEDGER.md "v0.49 —
  occupied-slot lists...".
- **A run's Actions "completed" status can lag its actual results if a
  trailing job queues behind the concurrency ceiling.** Directly
  observed multiple times this session; fixed 2026-08-10 by removing the
  digest job from `experiment.yml` entirely. **Confidence: HIGH**
  (directly observed, root-caused, fixed).
- **GitHub Actions concurrency ceiling on this account is roughly 40-50
  simultaneous jobs.** Found empirically (jobs stuck at `runner_id: 0`
  above this range). External audit's read: this is very likely just the
  documented per-plan cap (20 free / 40 pro / 60 team), not a genuine
  discovery. **Confidence: MODERATE** (consistent with a known
  explanation, not independently confirmed against account billing
  details).

## Ecological — the trophic-balance investigation

- **`maxPlants` (a slot-array size, not a biological limit) was binding
  regardless of predation in every default-config run this session.**
  Confirmed via comparing pre-fauna plant trajectories across seeds (one
  seed sat at its cap fifty days before any animal existed) and an
  arena-isolation test (`k_photoCost` alone at the original 90k/40k
  arena reproduced the shrunk-arena results exactly). **Confidence:
  HIGH** — this is a real control, not a small-n statistical comparison.
- **Raising `k_photoCost` (plant respiration cost) moves the plant
  equilibrium off that artifact — but the base dose does not fully clear
  it.** Direction confirmed across multiple doses. **Cap-binding audit
  (2026-08-10, 86 logs, `caps` bitmask): the plant slot cap still binds
  in 15/52 (29%) of 3x base-dose runs** — and on the 30 cold-drawn
  noise-floor seeds the clean figure is **worse: 8/15 (53%) for 3x vs
  2/15 (13%) for 5x.** The dose treated all session as "off the
  `maxPlants` artifact" is pinned against it in over half of unselected
  runs. Ranking by fraction of run spent capped: 5x 0.008 ≫ 3x 0.061 >
  default 0.083 ≫ 2x 0.243 (2x median peak plants 24630 against a 25000
  bound — essentially pinned).
  The animal cap never binds in any run (0/86); `maxAnimals` has never
  been a constraint. **Which exact multiplier, if any, is
  "correct" is NOT settled** — see the retractions below.
- **Cap-binding frequency is an outcome-independent selection criterion
  for `k_photoCost`, and it ranks the doses OPPOSITE to R0.** It is
  computed purely from plant dynamics with no reference to animals,
  which is what audit point 5 asked for. 5x is cleanest by it and has
  the *worst* demography (mean R0 0.55); 2x is dirtiest and has the
  *best* (0.98) — i.e. 2x's demographic advantage is probably an
  artifact of the inflated food base rather than independent of it.
  **Selecting on R0 would have promoted the most contaminated config in
  the corpus.** Not acted on yet: the criterion needs a threshold fixed
  in advance on plant-physiology grounds, and clearing the cap while
  animals go extinct trades one broken regime for another.
  **Confidence: HIGH** on the cap measurements (direct, mechanical),
  **UNRESOLVED** on what dose to pick.
- **Capped runs bias R0 upward by roughly +0.14.** Within 3x runs:
  capped mean 0.84 vs uncapped 0.70 (permutation p = 0.103 — not
  significant, but the direction is what mechanism predicts). Pooled R0
  figures throughout `LEDGER.md` carry this bias. Cleanest base-dose
  reading is the uncapped subset: **mean R0 0.70, 6/37 above
  replacement.** **Confidence: MODERATE.**
  **Confidence: MODERATE** on direction, **UNRESOLVED** on magnitude.
  Note the magnitude question is now known to be *unanswerable at the
  sample sizes used* (see the noise-floor entry below), and largely moot:
  no dose reaches replacement, so ranking them is optimizing inside a
  failing regime.
- **RESOLVED (was RETRACTED): "5x `k_photoCost` is the leading candidate
  over 3x" — there is no difference.** The pre-registered comparison
  completed 2026-08-10 on **30 cold-drawn seeds, 15/arm**, selected as a
  block before any results were seen. 3x mean R0 **0.674** (SD 0.278),
  5x **0.735** (SD 0.314); difference −0.061, SE 0.108, **permutation
  p = 0.590**, **Fisher p = 1.000** on the R0≥1 rate. The gap is one-fifth
  of one noise-floor SD (threshold 0.314). Per the rule fixed in advance,
  **5x is not promoted and 3x stands on parsimony** — and since 3x is
  already the base dose, nothing changes operationally. The external
  audit's p≈1.0 call at n=4/6 was correct. **Confidence: HIGH** — this is
  the only pre-registered, non-cherry-picked comparison in the project.
- **Neither dose is viable, on cold seeds.** 2/15 (3x) and 3/15 (5x)
  clear replacement; **5/15 go extinct in both arms.** Confirms the
  "nothing tested reaches replacement" conclusion was not a pooling
  artifact. **Confidence: HIGH.**
- **NO run in this project has ever been an equilibrium measurement.**
  Stationarity gate on all 30 cold seeds: **15/15 fail in both arms**,
  median slopes 10-25x `analyze.py`'s DRIFTING threshold. Direction is
  mixed (animals falling in ~half, rising in ~half), so this is genuine
  unsettled dynamics rather than a uniform bias — which protects
  *comparisons* at a shared cutoff but invalidates any *absolute* R0
  claim, including the two means above. 800 days is too short a protocol;
  how much too short is unmeasured. **Confidence: HIGH** (direct
  measurement on 30 runs).
- **RETRACTED (flagged, not disproven): "R0 1.51 (seed 7002, 5x dose) is
  the best result of the session."** With ~24 CFG arms tried at low n
  each, the single best result across all of them is expected to be
  inflated by selection (winner's curse) and likely to regress on
  retest. Specific retest not yet run.
- **RETRACTED: "The gutcost combo does not outperform the dose alone."**
  This was decided on a dichotomized R0>1 comparison (2/8 vs 4/6) — the
  exact move the external audit flagged. On the full corpus
  (2026-08-10 re-tally): gutcost 3/8 vs base 5/14, **Fisher exact
  p = 1.000**; medians 0.91 vs 0.72 (permutation p = 0.406). The two are
  statistically indistinguishable, and gutcost has the *highest* median
  and *tightest* spread (SD 0.25, min 0.58) of any arm with n≥8. Not
  better — but the deprioritization was unsupported.
- **Within-cfg seed-to-seed noise in R0 is SD 0.25-0.53.** Measured
  across four arms on 84 logs (base dose n=14 SD 0.39; 5x n=9 SD 0.53;
  gutcost n=8 SD 0.25; 2x n=4 SD 0.48). Implication, from a standard
  power calculation at SD 0.39: detecting a 0.2 difference in mean R0
  needs **n≈60 per arm**; 0.1 needs n≈239. Real arm sizes this session
  were 4-14. **Essentially every CFG comparison made this session was
  4-7x underpowered.** **Confidence: HIGH** — this is a direct
  measurement across distinct seeds at fixed cfg, not an inference.
- **No configuration tested this session is demographically viable.**
  All four arms with n≥4 have mean *and* median R0 below 1.0 (best
  median: gutcost 0.91). **Confidence: HIGH** — it holds across all 84
  runs and doesn't depend on distinguishing arms from each other.
- **The base-dose R0 rate is 5/14 (36%), median 0.72.** Supersedes every
  earlier partial tally of this arm (4/6, 4/7, etc.). The apparent gap
  between the ad-hoc seed set (4/7) and the cold `noisefloor-3x` set
  (1/7) is **not significant** (Fisher p=0.266, permutation p=0.186) —
  an earlier note treating it as a possible sampling problem was itself
  an overread of noise.
- **"No extinction" is not the same as "viable."** R0 < 1 means a
  population shrinking even where it hasn't died yet within the run's
  day budget. This is a conceptual point, not a statistical claim about
  any specific arm. **Confidence: HIGH** (it's a definitional/logical
  point, not an empirical one).
- **UNRESOLVED, real methodological concern (not yet a finding to act
  on):** choosing `k_photoCost`'s value by which dose produces more
  animal survival is outcome-tuning in a physics costume — a candidate
  violation of the project's own mission test. See LEDGER.md's dedicated
  entry. No dose should be described as "correct" or "promoted" until
  this is resolved with an outcome-independent selection criterion.
- **v0.50 (ATTACK arbiter floor removed) — mechanism verified, ecological
  effect UNKNOWN.** The floor removal itself is confirmed correct by code
  reading (parallel to GRAZE/SCAVENGE's unfloored attraction genes) and
  `node check.js` passes. **All ecological data collected before
  2026-08-10's gain-preserving fix is invalidated** (the original change
  also silently cut mean ATTACK score ~6x at the founder gene — a
  confound the fix removes). Not yet retested with the fix.
- **UNRESOLVED, flagged design question:** unflooring `meatAttraction`
  may create an absorbing state — if the gene drifts to ~0 via drift in
  a population not currently attacking, ATTACK's score goes to ~0, so
  there's no fitness event to ever select it back up. Possibly the same
  structural problem behind the long-standing, separately-documented
  herding/`socialAttraction` mystery. Not fixed; needs real design work
  (the audit's suggestion: make the *behavior* reachable via exploration
  noise in action selection, not via the gene's magnitude, so the gene
  itself stays unfloored).

## Historical (pre-this-session) — status with respect to the `maxPlants` confound

Every LEDGER conclusion drawn before this session's `maxPlants` diagnosis
was potentially running in a regime where the plant population was
artifact-capped regardless of predation. External audit point 6 asked for
a systematic pass instead of a blanket "unknown." First pass below —
**reasoned from re-reading each section, not from re-running historical
seeds with the array cap isolated**, so treat CLEAN/CONFOUNDED as a
considered judgment call, not a re-verified control. A real resolution of
any UNKNOWN row would need that seed re-run, which hasn't happened.

| milestone | tag | why |
|---|---|---|
| v0.39 carnivory unblock (body radius, attack-score-linear, pursuit escape hatches) | **CONFOUNDED (plausible, not confirmed)** | The measured shift (attacks 50→4447, flesh share 0.1%→1.14%) is a claim about ATTACK becoming *reachable*, which the three mechanism fixes plausibly explain on their own — but how *attractive* ATTACK was relative to GRAZE also depends on plant abundance, which this run didn't control for. Direction of the finding (attack became reachable) likely survives; the specific magnitude doesn't have a clean claim to standing. |
| v0.42 performance (canopy interception fix, "86% more plants") | **CONFOUNDED on the plant-count figure, CLEAN on the runtime figure** | The 82.1s→61.6s speedup is a wall-clock measurement, unaffected by any ecological confound. But "11,519 plants, 86% more than before" cannot be read as evidence of a healthier plant population — 11,519 could simply be closer to (or at) `maxPlants`. The interception-formula fix itself (a real bug: over-counting light in bands above a plant's own canopy) is independently correct by code reading, separate from either number. |
| v0.44 scorecard (senseRange/toxinResistance/acceleration/turnRate off rails; herbivory pin; size collapse) | **UNKNOWN, genuinely** | The gene-bound diagnoses for senseRange/toxinResistance/acceleration/turnRate are geometric/kinematic arguments, not food-availability arguments, and likely stand regardless. But `herbivory` pinning near max and `size` collapsing toward the floor are exactly the shape a starvation-driven (food-scarce) population would produce, which an artifact-capped plant population could cause independent of any real selective pressure. Genuinely can't tell without a re-run at a k_photoCost that keeps plants off the cap. |
| v0.47 six-prediction scorecard, currency unification (L47-2) | **PARTIALLY PROTECTED** | The currency fix normalizes GRAZE/ATTACK/FLEE scores by mass specifically *because* the section itself already flagged that shrinking `size` (v0.44) was contaminating cross-action comparisons — that self-correction reduces (doesn't eliminate) sensitivity to food abundance. The toxin split-brain fix (L47-1) is a pure logic/bookkeeping bug, independent of plant supply — CLEAN. The `k_confusion:0` finding (L47-3) is the one item from this section actually re-tested this session under the fixed food base (`confusion-off-retest`, see above) — R0 stayed <1 on both seeds pulled so far, directionally consistent with the original finding surviving, though not yet a full re-confirmation (n=2, no confusion-ON comparison at the same dose pulled alongside it yet). |
| HANDOFF.md §2 pin taxonomy (p<2/p=2/p>2 framework itself) | **CLEAN — it's a framework, not a data claim** | The taxonomy is a way of *classifying* a pinned gene's evidentiary status, not itself a claim about any specific run's ecology. It doesn't depend on plant abundance. Individual pins classified using it (e.g. the v0.44 examples above) inherit that row's tag, not this one. |

Net: nothing here needed retracting outright on this pass — no historical
claim was found to directly contradict a controlled result the way the
original `k_confusion` finding's food-base confound did. But v0.44's
herbivory/size rows are a real open question, not a formality, and are
the best candidate for a targeted historical re-run if anyone wants to
close it rather than leave it flagged.
