---
name: program-audit
description: Harsh adversarial audit of the RESEARCH PROGRAM, not of individual claims. Use when the project may be looping - shipping versions and scoring predictions without moving the mission. Attacks strategy, target selection, and whether the whole line of work should be abandoned. Distinct from AUDIT-PROTOCOL.md, which audits whether numbers are right.
---

# Program audit — is this project going anywhere?

Adapted 2026-09-11 from three open-source Claude Code adversarial-review skills,
after the owner observed the project was "in a loop of tiny adjustments and not
getting anywhere." Sources and what was taken from each:

- **lemon03390/Claude-code-adversarial-review-skill** — the *"guilty until proven
  exceptional"* premise, and **mandatory 1–10 confidence scoring with discard
  thresholds** (9–10 surface automatically, 7–8 surface with evidence, 4–6 go to
  an appendix, **1–3 are discarded entirely, not written down**). That last rule
  is the anti-filler mechanism this project needed and did not have.
- **robertoecf/adversarial-review** — *"break confidence rather than validate;
  expensive attack surfaces first; material-only findings; mandatory simplicity
  counterfactuals; terse ship/no-ship summary"*, and the **cross-validation
  tagging** scheme (`[cross-validated]` / `[auditor-only]` / `[host-only]`) with
  the host writing its own list **before** seeing the auditor's, so agreement
  means something instead of being an echo.
- **ecfm/adversarial-review** — the red-team / blue-team / **adjudication** shape.
  Its evidence standards were *not* copied: it has none, and an auditor with no
  evidence bar manufactures findings, which is the failure mode this project is
  most exposed to.

## What makes this different from AUDIT-PROTOCOL.md

`AUDIT-PROTOCOL.md` audits **claims**: is this number right, does the evidence
support it, was the arm labelled correctly. It has caught real errors and should
keep running.

It has never once asked **whether the program is working.** Every finding it has
ever produced was a local correction. Meanwhile the thing the owner actually
noticed — many consecutive missed predictions with the mission no closer — is
invisible to a claim-level audit, because each individual claim was *correctly*
reported as a miss.

This audit attacks the layer above: target selection, rate of progress, and
whether to stop.

## Premise

**Guilty until proven exceptional.** The null hypothesis is that this project is
a well-documented random walk that produces excellent bookkeeping and no
progress. The burden is on the *work* to show otherwise, not on the auditor to
prove waste.

## Mandatory questions — every one gets an explicit answer

1. **Is the mission reachable?** The mission test is "if a result had to be
   written into the code, it doesn't count", and the goal is plants, herbivores
   and carnivores holding each other in check. Is that achievable in this model
   *at all*? If the energetics make a carnivore strictly dominated, no amount of
   mechanism work reaches it, and the correct move is to say so rather than ship
   another version. **Answer with arithmetic from the shipped constants.**
2. **What is the rate of progress, in units that matter?** Not versions shipped,
   not predictions scored, not seeds run. Pick a metric that would distinguish a
   project converging on its goal from one walking in circles, state it, compute
   it across the whole history, and say which one this is.
3. **What should be abandoned?** Name at least one thing — a hypothesis line, a
   mechanism, a measurement, a rule — that is consuming effort and should stop.
   "Nothing" is an allowed answer only with an argument.
4. **Simplicity counterfactual.** Could the same knowledge have been obtained
   with fewer versions, fewer mechanisms, fewer config surfaces? Name the
   specific shorter path. Count the mechanisms now in the build that no
   measurement currently justifies.
5. **Is the process itself the bottleneck?** One structural change per version,
   pre-registered thresholds, and a weekly scoring cadence cap the learning rate
   at roughly one bit per week. Is that cap the reason for the loop, and if so
   what should replace it — without discarding the discipline that stopped the
   earlier fabrications?
6. **What is being ignored because it did not fit a pre-registered box?** Look
   specifically for large, significant effects that were filed as MISS because
   they moved the wrong variable.

## Rules the auditor must follow

**Confidence score, 1–10, mandatory on every finding.** 9–10 surface first. 7–8
surface with evidence attached. 4–6 go in an appendix. **1–3 are discarded — do
not write them down.** A finding you would not defend is worse than no finding,
because every one filed costs a written response.

**Evidence mandate: concrete over abstract.** Every finding cites a file and
line, a `LEDGER.md` line number, a log path, a commit, or a number you computed
yourself. A finding that cannot point at something is not filed.

**Material only.** If acting on the finding would not change what gets built or
measured next, it is not material. Do not file it.

**Expensive attack surfaces first.** Rank by what it would cost to be wrong
about, not by how easy it is to say.

**Separate CONFIRMED from PLAUSIBLE.** CONFIRMED means you verified it against
data in the repo. PLAUSIBLE means you reasoned it. Never present the second as
the first.

**Finding nothing in a category is valid and expected.** An auditor told to be
harsh will invent ten findings whether or not ten exist.

**Stay inside the hard rules or argue against them explicitly.** `CLAUDE.md`'s
rules were learned from a specific failure; several encode a specific past failure.
Recommending one be dropped is allowed — recommending it while ignoring the
recorded rationale is not.

**Terse ship / no-ship verdict.** End with one paragraph: continue as-is, pivot,
or stop — and what would have to be true for you to change that verdict.

## Procedure

1. **Host writes its own findings list first**, before the auditor runs, and
   commits it. This is what makes cross-validation mean anything.
2. Generate the evidence pack (`PROGRAM-HISTORY.md`): every version, its one
   structural change, its prediction, its outcome, and the mission metrics
   measured under it.
3. Spawn the auditor with this file, `PROGRAM-HISTORY.md`, `CLAUDE.md`,
   `HANDOFF.md` and the repo. Maximum thinking.
4. Tag every finding `[cross-validated]`, `[auditor-only]`, or `[host-only]`.
   **`[auditor-only]` findings are the ones that justify the exercise** — they
   are what the host could not see about itself.
5. Answer every surfaced finding in writing in `LEDGER.md`: accept or reject,
   each with a reason. Rejecting with a stated reason is a an acceptable outcome.
6. Anything acted on still obeys the normal discipline. The audit is not a
   bypass.
