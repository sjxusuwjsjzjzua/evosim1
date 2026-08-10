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
  equilibrium off that artifact.** Direction confirmed across multiple
  doses (2x/3x/5x all show populations surviving to full run length more
  often than unmodified default). **Which exact multiplier, if any, is
  "correct" is NOT settled** — see the two retractions below.
  **Confidence: MODERATE** on direction, **UNRESOLVED** on magnitude.
- **RETRACTED: "5x `k_photoCost` is the leading candidate over 3x."**
  Was based on 3/4 vs 4/6 seeds with R0>1. External audit ran Fisher's
  exact test: p≈1.0, 95% CIs of ~19-99% and ~22-96%, overlapping almost
  entirely. Not evidence of a difference. A noise-floor + n≥30
  confirmation run for both doses is in flight as of 2026-08-10; decision
  rule is written in LEDGER.md before that data lands.
- **RETRACTED (flagged, not disproven): "R0 1.51 (seed 7002, 5x dose) is
  the best result of the session."** With ~24 CFG arms tried at low n
  each, the single best result across all of them is expected to be
  inflated by selection (winner's curse) and likely to regress on
  retest. Specific retest not yet run.
- **The gutcost combo (`k_gut`/`k_digest` cut, on top of the base
  `k_photoCost` dose) does not outperform the dose alone.** 8 seeds,
  2/8 with R0>1 (25%), vs the base dose's 4/6 (67%) at the time this
  was written — though note the base-dose fraction is itself subject to
  the same small-n caveat above. **Confidence: LOW-MODERATE** — n=8 is
  still small, but the direction (worse, not better) was consistent
  enough across enough seeds to deprioritize the combo, and this
  specific claim doesn't require distinguishing a small real effect
  from noise, just "not obviously better."
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

## Historical (pre-this-session) — status with respect to the `maxPlants` confound: UNKNOWN

Every LEDGER conclusion drawn before this session's `maxPlants` diagnosis
was potentially running in a regime where the plant population was
artifact-capped regardless of predation — not just the `k_confusion`
finding that happened to get checked. This has **not** been
systematically audited yet (external audit's point 6). Treat every
pre-2026-08-10 ecological claim in LEDGER.md as unverified against this
specific confound until tagged otherwise. This includes, at minimum: the
v0.39/v0.42 omnivory milestones, the v0.47 six-prediction scorecard, and
parts of HANDOFF.md §2's pin taxonomy.
