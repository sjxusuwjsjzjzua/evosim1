# Host position on rewrite vs iterate, written 2026-09-12 before the auditor runs

Committed first so cross-validation is not an echo. Confidence 1-10.

**My position: not a dead end, and not a tuning problem either. Confidence 6.**

The case that it is salvageable:

- The machinery demonstrably works for genes that have a fitness gradient.
  `biteForce` moves 5.98x to 13.60x the drift yardstick as generations rise,
  `herbivory` 1.24x to 2.79x. Selection is real and duration amplifies it.
- Plant-animal arms races, omnivory on two seeds, and at least one run with a
  herd and 66% corpse consumption have all appeared without being written in.
- Matter conservation is exact. Determinism holds. The measurement stack, after
  the corrections, is sound.

The case that it is a dead end:

- Heterotrophy fraction is 0.302% median, max 3.95%, zero of 1,502 runs above
  5%, and flat across five structural versions.
- The only thing that has ever moved it is raising `meatValue`, a constant.
- `carrionAttraction` sits at 0.65-0.72x drift at every duration. `carnivory`
  0.49-0.84x. Both below the null. Neither responds to any intervention tried.

What I think is actually true, confidence 5: the architecture can support a
second trophic level but the *energetics as configured* cannot. A specialist
carnivore pays 1.63x the herbivore's diet upkeep for comparable intake and must
catch its food. That is a constants problem, not an architecture problem - but
it is a constants problem in a 150-dimensional space where 11 dimensions have
ever been varied and the search has been one-at-a-time.

**So my answer is: neither rewrite nor keep iterating the same way. Run a
screening sweep over the untouched dimensions first, under amended rule 1 which
now permits it, and only conclude dead-end if nothing in that space moves the
metric.** Confidence 5. I have not tested this and it is the obvious
self-serving answer for someone who does not want to throw away 34 days of work,
which is why the auditor should attack it.

**What would change my mind toward rewrite, stated in advance:** a demonstration
that no setting of the existing constants can put a carnivore's net energy rate
above a herbivore's at achievable prey density. That is arithmetic and does not
need a run.
