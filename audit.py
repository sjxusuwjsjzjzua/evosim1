#!/usr/bin/env python3
"""
audit.py — generates the daily audit report that the adversarial auditor reads.

    python3 audit.py [--out DAILY-AUDIT.md]

The point of this file is to do everything a critic should NOT have to spend
its attention on. A cold subagent has no idea that the Actions ceiling is 20
jobs, or which arms the corpus contains, or which predictions were never
scored. Every one of those is countable, so it gets counted here and handed
over as fact. The auditor's attention is then spent on judgement, which is
the only thing it is actually better at than a script.

Sections, in the order the auditor should read them:

  1. COMPUTE       throughput against the known ceiling; idle time
  2. CORPUS        what arms the accumulated logs actually contain
  3. PREDICTIONS   every prediction found, and whether it was ever scored
  4. COMMITMENTS   things the log says will happen, for follow-up
  5. CLAIMS INDEX  numeric claims with line refs, so drift is checkable

Section 2 exists because of a specific failure: for two days and 82 cold
seeds, every run in the standing batch was a treatment arm and none was a
control, and nobody noticed because nobody counted. That class of error --
a long-lived unexamined assumption -- is what this report is built to
surface, and it is cheap to detect mechanically once you decide to look.

Stdlib only, no build step, consistent with the rest of the project.
"""

import argparse
import collections
import datetime
import glob
import json
import os
import re
import subprocess

PDT = datetime.timezone(datetime.timedelta(hours=-7))
PROJECT_START = datetime.datetime(2026, 8, 8, 13, 4, 38, tzinfo=PDT)

# Measured 2026-08-10, recorded in CLAUDE.md. The auditor cannot know these.
ACTIONS_JOB_CEILING = 20
STANDING_TARGET_PER_HOUR = 18

# v0.51 shipped defaults. An arm is defined by how a log's cfg differs from
# these -- never by whether a set of runs agree with each other, which is the
# mistake that produced the phantom "baseline" arm on 2026-08-10.
BUILD_DEFAULTS = {"k_photoCost": 0.004, "maxPlants": 90000, "maxAnimals": 40000}


def sh(cmd):
    try:
        return subprocess.run(cmd, shell=True, capture_output=True, text=True,
                              timeout=120).stdout.strip()
    except Exception:
        return ""


def now():
    return datetime.datetime.now(PDT)


# --------------------------------------------------------------------------
# 1. COMPUTE
# --------------------------------------------------------------------------

def section_compute():
    L = ["## 1. COMPUTE", ""]
    elapsed = (now() - PROJECT_START).total_seconds() / 3600

    refs = sh("git for-each-ref --format='%(committerdate:unix) %(refname:short)' "
              "refs/remotes/origin/runs/").splitlines()
    stamps = []
    for line in refs:
        line = line.strip().strip("'")
        if not line:
            continue
        parts = line.split(" ", 1)
        if len(parts) == 2 and parts[0].isdigit():
            stamps.append(int(parts[0]))

    local_logs = [p for p in glob.glob("runs/**/*.json", recursive=True)
                  if not p.endswith(("progress.json", "partial.json"))
                  and "standing-collect" not in p]

    L += [f"- Project age: **{elapsed:.0f} h** ({elapsed/24:.1f} days) since "
          f"{PROJECT_START.strftime('%b %d %H:%M PDT')}",
          f"- Actions result branches (completed sims that pushed a log): **{len(stamps)}**",
          f"- Local completed logs on disk: **{len(local_logs)}** "
          f"(floor only — `runs/` is gitignored scratch and gets pruned)",
          ""]

    if stamps:
        stamps.sort()
        rate = len(stamps) / elapsed if elapsed else 0
        util = 100 * rate / STANDING_TARGET_PER_HOUR if STANDING_TARGET_PER_HOUR else 0
        L += [f"- Mean throughput: **{rate:.1f} sims/h** against a standing target of "
              f"{STANDING_TARGET_PER_HOUR}/h → **{util:.0f}% of target**",
              f"- Actions concurrency ceiling is {ACTIONS_JOB_CEILING} running jobs "
              f"(measured, not assumed)", ""]

        gaps = []
        for a, b in zip(stamps, stamps[1:]):
            h = (b - a) / 3600
            if h > 2:
                gaps.append((a, b, h))
        idle = sum(g[2] for g in gaps)
        L += [f"- Idle gaps >2 h: **{len(gaps)}**, totalling **{idle:.1f} h** "
              f"({100*idle/elapsed:.0f}% of project elapsed time)", ""]
        if gaps:
            L += ["| gap start (PDT) | gap end | hours |", "|---|---|---|"]
            for a, b, h in gaps[-8:]:
                L.append("| %s | %s | %.1f |" % (
                    datetime.datetime.fromtimestamp(a, PDT).strftime("%b %d %H:%M"),
                    datetime.datetime.fromtimestamp(b, PDT).strftime("%b %d %H:%M"), h))
            L.append("")

        byday = collections.Counter(
            datetime.datetime.fromtimestamp(s, PDT).strftime("%b %d") for s in stamps)
        L += ["Sims landed per day:", "", "| day | sims |", "|---|---|"]
        L += ["| %s | %d |" % (k, v) for k, v in sorted(byday.items())]
        L.append("")
    else:
        L += ["- **No fetched run branches.** Run "
              "`git fetch --filter=blob:none origin 'refs/heads/runs/*:refs/remotes/origin/runs/*'` "
              "first, or this section is blind.", ""]
    return L


# --------------------------------------------------------------------------
# 2. CORPUS — the blind-spot detector
# --------------------------------------------------------------------------

def arm_of(cfg):
    """Name a run's arm by diffing its cfg against the BUILD DEFAULTS.

    Never by comparing runs to each other. Uniformity across a set of runs
    says they share a condition; it says nothing about which one.
    """
    diff = {k: cfg.get(k) for k, v in BUILD_DEFAULTS.items() if cfg.get(k) != v}
    if not diff:
        return "SHIPPED DEFAULTS (control)"
    return ", ".join("%s=%s" % (k, diff[k]) for k in sorted(diff))


def section_corpus():
    L = ["## 2. CORPUS COMPOSITION", "",
         "What the accumulated logs actually contain, by arm. Arm is determined by "
         "diffing each log's cfg against the v0.51 build defaults "
         "(`k_photoCost=0.004, maxPlants=90000, maxAnimals=40000`).", ""]

    arms = collections.Counter()
    lengths = collections.Counter()
    bad = 0
    paths = [p for p in glob.glob("runs/**/*.json", recursive=True)
             if not p.endswith(("progress.json", "partial.json"))]
    for p in paths:
        try:
            d = json.load(open(p))
        except Exception:
            bad += 1
            continue
        cfg = d.get("cfg", {})
        arms[arm_of(cfg)] += 1
        c = d.get("cols", {})
        if c.get("tick") and cfg.get("ticksPerDay"):
            lengths[int(c["tick"][-1] / cfg["ticksPerDay"] // 400 * 400)] += 1

    total = sum(arms.values())
    L += [f"Logs scanned: **{total}**" + (f" ({bad} unparseable)" if bad else ""), ""]
    if total:
        L += ["| arm | n | share |", "|---|---|---|"]
        for k, v in arms.most_common():
            L.append("| %s | %d | %.0f%% |" % (k, v, 100 * v / total))
        L.append("")

        ctrl = sum(v for k, v in arms.items() if k.startswith("SHIPPED"))
        if ctrl == 0:
            L += ["> **FLAG: the corpus contains ZERO runs at shipped defaults.** "
                  "Every treatment comparison in it is treatment-vs-treatment with no "
                  "control. This is the exact condition that went unnoticed for two "
                  "days and 82 seeds on 2026-08-10.", ""]
        else:
            L += [f"- Control runs at shipped defaults: **{ctrl}** "
                  f"({100*ctrl/total:.0f}% of corpus)", ""]

        if len(arms) == 1:
            L += ["> **FLAG: single-arm corpus.** Nothing here can support a "
                  "comparative claim.", ""]

    if lengths:
        L += ["Run lengths (binned, 400 sim-days) — **rule 7b: never compare a "
              "trailing-window statistic across these bins**:", "",
              "| length bin (days) | n |", "|---|---|"]
        L += ["| %d–%d | %d |" % (k, k + 399, v) for k, v in sorted(lengths.items())]
        L.append("")
        if len(lengths) > 1:
            L += ["> Mixed run lengths present. Any statistic quoted across them "
                  "must be at a matched calendar cutoff, or normalised to a per-day "
                  "rate if it is an endpoint total.", ""]
    return L


# --------------------------------------------------------------------------
# 3. PREDICTIONS
# --------------------------------------------------------------------------

PRED_RE = re.compile(r"^#+\s*(.*(?:PREDICTION|PRE-REGISTRAT|PRE-REGISTERED|prediction).*)$",
                     re.I | re.M)
SCORE_RE = re.compile(r"^#+\s*(.*(?:SCORED|\bHIT\b|\bMISS\b|CAN'T-TELL|RETRACT).*)$",
                      re.I | re.M)

STOP = set("the a an and or of to in on for by is are was were be been with that this "
           "it its as at from not no than then so if but before after over under "
           "prediction predictions scored score written run runs seed seeds day days "
           "test tested testing new".split())


def keywords(s):
    return {w for w in re.findall(r"[a-zA-Z_]{4,}", s.lower()) if w not in STOP}


def section_predictions(text):
    L = ["## 3. PREDICTION REGISTER", "",
         "Every heading that declares a prediction, and whether a later heading "
         "appears to score it. Matching is keyword overlap and is **advisory, not "
         "authoritative** — an UNSCORED row may simply be a naming mismatch. Treat "
         "each as a question to answer, not a verdict.", ""]

    preds = [(text[:m.start()].count("\n") + 1, m.group(1).strip())
             for m in PRED_RE.finditer(text)]
    scores = [(text[:m.start()].count("\n") + 1, m.group(1).strip())
              for m in SCORE_RE.finditer(text)]

    if not preds:
        L += ["_No prediction headings found._", ""]
        return L

    rows, unscored = [], 0
    for line, title in preds:
        kw = keywords(title)
        best, best_ov = None, 0
        for sline, stitle in scores:
            if sline <= line:
                continue
            ov = len(kw & keywords(stitle))
            if ov > best_ov:
                best, best_ov = (sline, stitle), ov
        if best and best_ov >= 2:
            rows.append((line, title, "scored", "L%d: %s" % (best[0], best[1][:60])))
        else:
            rows.append((line, title, "**UNSCORED?**", "—"))
            unscored += 1

    L += [f"Predictions found: **{len(preds)}**  ·  apparently unscored: "
          f"**{unscored}**", "",
          "| LEDGER line | prediction | status | matched scoring |",
          "|---|---|---|---|"]
    for line, title, status, match in rows:
        L.append("| %d | %s | %s | %s |" % (line, title[:70], status, match))
    L.append("")
    if unscored:
        L += ["> A prediction that is never scored is the cheapest way for a wrong "
              "diagnosis to survive. Each row above marked UNSCORED needs either a "
              "scoring entry or an explicit note saying why it cannot be scored.", ""]
    return L


# --------------------------------------------------------------------------
# 4. COMMITMENTS
# --------------------------------------------------------------------------

COMMIT_RE = re.compile(
    r"^(.*(?:I will |I am not going to |committed to |commitment |"
    r"stops and surfaces|must not|do not quote|will stop|next step|"
    r"before then|until .{0,40}finish).*)$", re.I | re.M)


def section_commitments(text):
    L = ["## 4. OPEN COMMITMENTS", "",
         "Statements in LEDGER.md that promise a future action or forbid one. The "
         "auditor should check whether each was honoured — a commitment quietly "
         "dropped is indistinguishable, from the outside, from one that was kept.", ""]
    hits = [(text[:m.start()].count("\n") + 1, m.group(1).strip())
            for m in COMMIT_RE.finditer(text)]
    hits = [(l, t) for l, t in hits if 40 < len(t) < 400]
    if not hits:
        L += ["_None found._", ""]
        return L
    L += ["| line | statement |", "|---|---|"]
    for l, t in hits[-25:]:
        L.append("| %d | %s |" % (l, t.replace("|", "\\|")[:220]))
    L += ["", f"_Showing the {min(25, len(hits))} most recent of {len(hits)}._", ""]
    return L


# --------------------------------------------------------------------------
# 5. CLAIMS INDEX
# --------------------------------------------------------------------------

CLAIM_RE = re.compile(r"^.*?(\d+(?:\.\d+)?\s*%|\bR0\s+\d+\.\d+|\b\d+/\d+\b).*$", re.M)


def section_claims(text):
    L = ["## 5. NUMERIC CLAIMS INDEX", "",
         "Every line carrying a percentage, an R0 value, or an n/N ratio, newest "
         "last. **Use this to check for drift**: the same quantity quoted with "
         "different values in different entries, with no retraction between them. "
         "That pattern has occurred repeatedly (the 1600→2400 persistence rate went "
         "50% → 60% → 50% → 4/6 → 82% before the block was complete).", ""]
    lines = text.split("\n")
    hits = [(i + 1, ln.strip()) for i, ln in enumerate(lines)
            if CLAIM_RE.match(ln) and 20 < len(ln.strip()) < 300]
    L += [f"Lines carrying numeric claims: **{len(hits)}**. Most recent 40:", "",
          "| line | claim |", "|---|---|"]
    for i, ln in hits[-40:]:
        L.append("| %d | %s |" % (i, ln.replace("|", "\\|")[:200]))
    L.append("")
    return L


# --------------------------------------------------------------------------

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default="DAILY-AUDIT.md")
    ap.add_argument("--ledger", default="LEDGER.md")
    a = ap.parse_args()

    text = open(a.ledger).read() if os.path.exists(a.ledger) else ""

    L = [f"# Daily audit — {now().strftime('%Y-%m-%d %H:%M PDT')}", "",
         "Generated by `audit.py`. Everything here is **counted, not judged** — it "
         "is the factual substrate the auditor works from, so that its attention "
         "goes to judgement rather than to arithmetic it would have to redo.", "",
         "Constants the auditor cannot infer and should not re-derive: the Actions "
         f"concurrency ceiling is **{ACTIONS_JOB_CEILING} running jobs** (measured); "
         "the repo is **public** so Actions minutes are unlimited and free; the "
         "build is **single-file, no build step, runs on a phone**; and "
         "**nothing about behaviour may be hardcoded** — the mission test is *if a "
         "result had to be written into the code, it doesn't count*.", ""]

    L += section_compute()
    L += section_corpus()
    L += section_predictions(text)
    L += section_commitments(text)
    L += section_claims(text)

    open(a.out, "w").write("\n".join(L) + "\n")
    print("wrote %s (%d lines)" % (a.out, len(L)))


if __name__ == "__main__":
    main()
