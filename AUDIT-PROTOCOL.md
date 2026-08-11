# Daily adversarial audit — protocol

A once-a-day pass in which a fresh Opus 5 subagent, at maximum thinking, audits
this project's work and files findings. Claude then answers every finding in
writing. Both halves are committed.

This file is the auditor's charter. It is also the thing that stops the audit
from becoming theatre, which is the failure mode it is most exposed to.

---

## Why the auditor reads the repo, not a report

The obvious design — Claude writes a self-audit, a critic critiques it — does
not work here, and it is worth being precise about why, because the reasoning
generalises.

Look at what actually went wrong on 2026-08-10: an arm mislabelled as
"baseline" when no baseline existed; `ticksPerDay` hardcoded to 60 when the
real value was 480; completion-order bias mis-read three separate times; 82
cold seeds accumulated with no control arm. **Not one of those was a reasoning
error a reader could have caught.** Each was factual, and each was caught by
checking data — diffing a cfg against build defaults, reading the tick rate out
of the file that was already open.

A critic handed the sentence "Baseline (1x), local — 4/5 survived" has no way
to know that sentence is false. It will critique the framing of a table whose
contents are wrong, and it will sound insightful doing it. Worse, the report is
written by the same mind that made the error, so the blind spot is laundered
into the input.

So the auditor gets the repo, the logs, and `DAILY-AUDIT.md`'s counted facts —
and its central job is **verifying claims against the data they came from.**

---

## What to hunt

Aim at the class of error that survives self-review. Errors Claude catches
within a cycle or two of ordinary work do not need an auditor; the ones that
sit for days do.

1. **Long-lived unexamined assumptions.** The signature failure. "No control
   arm" survived two days and 82 seeds because nobody asked the dumb question.
   Ask the dumb questions. What has been true so long that it stopped being
   visible?
2. **Predictions never scored.** §3 of the report lists candidates. A prediction
   that quietly never resolves is the cheapest way for a wrong diagnosis to
   survive contact with evidence.
3. **Numbers that drifted without a retraction.** §5 indexes every numeric
   claim with a line ref. The same quantity quoted differently in two entries,
   with nothing between them acknowledging the change, is a finding.
4. **Claims whose evidence does not support them.** Follow a headline number
   back to the log it came from and check it. Especially: statistics compared
   across different run lengths (hard rule 7b), endpoint totals not normalised
   to rates, and ratios where the denominator is doing the work.
5. **Mission-test violations.** *If a result had to be written into the code, it
   doesn't count.* A population target hit by capping or rate-limiting rather
   than by selection finding it is a failure no matter how good the numbers
   look. This is the one finding category that outranks everything else.
6. **Work that is busy rather than productive.** Runs fired without a
   falsifiable prediction; seeds added to an already-settled question; screening
   data accumulating with no shipped change attached to it.

---

## Rules the auditor must follow

**Every finding cites evidence.** A file and line, a number in `LEDGER.md`, a
log path, a commit. A finding that cannot point at something is not a finding
and must not be filed.

**Finding nothing is a valid, expected outcome.** For each category above,
"nothing here" is an acceptable and useful answer. An auditor told to be harsh
will manufacture ten findings whether or not ten exist — that is a known
failure of the role, and inventing filler actively costs the project, because
every filed finding consumes a written response.

**Rank by consequence, most severe first.** Say plainly which findings would
change a conclusion and which are hygiene.

**Separate confidence from severity.** Mark each finding CONFIRMED (verified
against data) or PLAUSIBLE (reasoned, unverified). Do not present the second as
the first.

**Do not propose a change you cannot justify from evidence in the repo.** "Try
raising X" with no argument is noise. The project has free compute and a strict
prediction rule; the bottleneck has never been ideas for constants to tweak.

**Stay inside the hard rules.** They are in `CLAUDE.md` and several were learned
expensively. A finding that recommends violating one — widening a gene bound to
fix a pin, comparing trailing-window statistics across run lengths, adding a
build step — needs to argue against the recorded rationale explicitly, not
ignore it.

---

## Claude's obligations

**Answer every finding in writing.** Accept or reject, each with a reason,
appended to `LEDGER.md` under the date. A finding that is rejected is fine — a
finding that is silently ignored defeats the whole mechanism.

**The auditor proposes; it does not decide.** This matters more here than in
most projects. The mission test says a result written into the code doesn't
count; the direct analogue is that *a change made to satisfy a critic is not
an improvement*. Rejecting a finding with a stated reason is a first-class
outcome and should be common.

**Anything acted on still obeys the normal discipline.** A code change needs a
version bump, `node check.js`, one structural change, a written falsifiable
prediction. The audit is not a bypass.

---

## Running it

```
python3 audit.py                # regenerates DAILY-AUDIT.md
```

Then spawn the auditor against the repo with `AUDIT-PROTOCOL.md` and
`DAILY-AUDIT.md` as its brief. It should read `LEDGER.md` (recent entries),
`CLAUDE.md`, `HANDOFF.md`, `FINDINGS.md`, the current build, and whatever logs
it needs to verify a claim.

Findings land in `AUDIT-FINDINGS.md`; Claude's responses go into `LEDGER.md`.
Both are committed to `claude/evolution-sim-v047-audit-jft25c`.

---

## What is deliberately NOT the auditor's job

**Throughput and utilisation.** A cold subagent does not know the Actions
ceiling is 20 jobs, or that the repo is public so minutes are free. It will
suggest parallelising things already at cap. Those numbers are measurable, so
§1 of `DAILY-AUDIT.md` measures them and the auditor should read them as given
rather than reasoning about them.

**Anything a script can check.** Unscored predictions, corpus composition, run
lengths, idle gaps — all mechanical, all in the report. If an audit produces a
finding that a script could have produced, the correct response is to write
the script, not to rediscover the finding tomorrow.
