# Host self-findings, 2026-09-11 — written BEFORE the auditor runs

Committed first so cross-validation means something. Confidence 1–10 per the
program-audit skill; anything I would score 1–3 is not written down.

---

**HF-1 — Five versions spent on one target, five wrong diagnoses. CONFIRMED. Confidence 9.**
Carnivory has now consumed v0.50 (unfloor ATTACK), v0.52 (injury payoff), v0.53
(selection consistency), v0.54 (choice rule), v0.55 (invasion probe). In every
one of them `meatAttraction` moved less than the neutral-gene drift yardstick.
Rule 3 says a missed prediction means the diagnosis was wrong. Five consecutive
wrong diagnoses about the same target is not five pieces of bad luck — it is the
signature of attacking something unreachable. The rule told me to re-diagnose
each time; it never told me to question whether the target exists.

**HF-2 — The arithmetic that reframes the whole question was available from day one and I computed it in week five. CONFIRMED. Confidence 9.**
LEDGER 2026-09-11: a specialist carnivore (0.85, 0.15) pays 0.01612 diet upkeep
against an evolved herbivore's 0.00987 — 1.63× — while extracting 18.26 per unit
prey mass against 17.5 per unit *undefended* foliage. Both numbers come from
shipped constants (`k_gut`, `k_mixed`, `mixedFree`, `meatValue`, `carrionValue`,
`tissueValue`). Nothing about that calculation needed a single run, and it
reframes five versions of mechanism work. This is the largest process failure in
the project: I ran experiments where I should have read the cost function.

**HF-3 — There is no mission-level metric, so "are we making progress" is unanswerable. CONFIRMED. Confidence 8.**
Everything measured is local: survival %, cv, GRAZE share, carnivory, predation
share, ACF. Nothing aggregates to "is this world closer to plants, herbivores
and carnivores holding each other in check than it was a month ago?" The loop
was invisible from inside the project precisely because no number tracks the
mission. The owner noticed it before any instrument did.

**HF-4 — The pre-registration machinery is discarding real signal. CONFIRMED. Confidence 8.**
`meat-rich` produced survival 92.2% against a matched control's 66.7%, Fisher
p=0.0022 (LEDGER §WEEKLY PASS 2026-09-08) — the largest effect this project has
ever measured — and was scored **MISS**, because the frozen criterion was about
`carnivory` and `carnivory` did not move. Freezing criteria stops me fooling
myself, which is why it exists; but with no slot for a large unpredicted effect
it also throws away the best result on the board. The criteria need a "notable
unpredicted effect" clause that records without licensing a post-hoc story.

**HF-5 — The process caps learning at about one bit per week, and compute is free. CONFIRMED. Confidence 8.**
One structural change per version, weekly scoring, n≥25 gate. This week the
answer was zero bits. Four arms run in parallel but all four are downstream of a
single diagnosis, so they buy precision, not breadth. Actions minutes are
unlimited and the concurrency cap is 20 — the bottleneck is that I serialise
hypotheses, not that I lack compute.

**HF-6 — Self-inflicted measurement errors consume a large share of each cycle. CONFIRMED. Confidence 7.**
In roughly five weeks: an arm mislabelled as baseline when no baseline existed;
`ticksPerDay` hardcoded to 60 against a real 480; absence-vs-difference in
`arm_of` twice; act columns differenced as if cumulative when they are snapshots;
a rule-7 identity check that verified nothing because both runs stopped before
animals existed; queueing arithmetic wrong twice, once producing a 110-run
backlog that starved a week of work; a collector path bug that collected nothing for a cycle. Each cost a cycle. The instrumentation is not
converging on reliable any faster than the simulator is converging on the
mission.

**HF-7 — Mechanisms are accumulating faster than evidence justifies them. CONFIRMED. Confidence 7.**
`k_choiceBeta` ships today with a falsified motivating diagnosis and no
measurable benefit (H4 MISS, survival p=0.69). `invadeFrac`/`invadeGenes` exist
only to run one probe. `k_meatAttrFloor` remains at 0.5 by default. The build is
gaining configuration surface per version while the mission metrics are flat.

**HF-8 — The mission test is being applied to new work but not to the default build. PLAUSIBLE. Confidence 6.**
`k_meatAttrFloor: 0.5` supplies 83% of ATTACK's attraction term against an
evolved `meatAttraction` of ~0.10, and removing it drops predation from 61% to
25%. By the project's own stated test — *if a result had to be written into the
code, it doesn't count* — predation in the shipped default does not count, and
has not for five versions. I have been running arms *around* that constant
rather than treating the shipped build as failing its own test.
