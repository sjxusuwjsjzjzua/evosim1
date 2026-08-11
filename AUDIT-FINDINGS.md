# Adversarial audit — 2026-08-11

**5 findings filed. 5 CONFIRMED, 0 PLAUSIBLE.** Three would change a conclusion
(F1, F2, F3); two are hygiene with a sharp edge (F4, F5).

Three hunt categories were checked and **nothing was filed** in them — see
"Categories deliberately left empty" at the bottom. That list is part of the
result, not an omission.

All arithmetic below was recomputed from the logs on disk with `python3`, using
`cfg.ticksPerDay` read out of each file. Where a LEDGER number reproduced
exactly, I say so and file nothing.

---

## F1. The freshest carnivory headline is mostly a constant in the source, not selection

**Severity: HIGHEST — this is the mission-test category, and it changes a
conclusion.**
**CONFIRMED.**

### The claim under audit

`LEDGER.md:5750-5775`, written this session as a "free measurement off the same
54 seeds":

> Predation share grows with world age — 26% at day 800, 35% by day 1600 …
> better than one in four survivors (6/21) now has predation as the *majority*
> cause of animal death — against 5-in-120 previously. **That is a real upgrade
> to the weakest mission pillar** and it was sitting in already-paid-for data.

I reproduced every number in that entry exactly (median day-800 share 0.2640,
median endpoint 0.3540, mean 0.3151, range 0.047-0.578, 11/21 >30%, 6/21 >50%,
median starvation 0.641, 3x 24.7% n=12 vs 5x 49.0% n=9, and all 21 survivors did
run to exactly 1600 days). **The arithmetic is right.** The problem is what it is
being read as.

### The mechanism

`evosim-v0_51_0.html:1735-1741` — the ATTACK arbiter score:

```
*sizeMatch*(0.5 + G[g+AG.meatAttraction])
```

GRAZE uses `G[g+AG.plantAttraction]` bare (`:1668`), SCAVENGE uses
`G[g+AG.carrionAttraction]` bare (`:1706`), APPROACH and FLEE likewise. ATTACK
alone carries an additive `0.5` that no gene can remove. `meatAttraction` is
bounded `[0,1]` (`:668`).

### What the genes actually did in those 21 runs

Population-mean `meatAttraction` at the final gene snapshot, against the constant
it is added to:

| | median across the 21 survivors |
|---|---|
| evolved `meatAttraction` | **0.093** |
| effective ATTACK attraction `0.5 + meatAttraction` | 0.593 |
| **share of that supplied by the hardcoded floor** | **84%** |
| evolved `plantAttraction` (GRAZE's, unfloored) | 0.800 |

The six seeds the entry counts as "predation is the majority cause of animal
death" have `meatAttraction` = **0.0333, 0.0347, 0.124, 0.0935, 0.0005, 0.2109**.
In five of the six the constant supplies 80-99.9% of the attraction weight.

Two runs are decisive on their own:

- **seed 41181** (`runs/standing-collect/seed-41181.json`): mean `meatAttraction`
  **0.0000** — the gene is fully purged — and the world still ran 37,536 attacks
  and 4,499 kills, 16.1% of animal deaths.
- **seed 41111**: mean `meatAttraction` **0.0005**, 119,948 attacks, and predation
  is **51.5% of all animal deaths** — one of the six "majority predation" worlds,
  in a population whose meat-attraction gene is indistinguishable from zero.

And the project's showcase 2400-day survivor,
`runs/stationarity/seed-10008-2400d.json`: predation **61.7%** of animal deaths,
`meatAttraction` **0.102**, `plantAttraction` 0.582. So `0.5 + 0.102 = 0.602`
slightly *exceeds* the fully-evolved grazing attraction — and 83% of it is a
number typed into the file.

### Why this is not merely a caveat

The project already has direct causal evidence that the constant is load-bearing
for exactly this metric, and it is in the source comment above the line
(`:1737-1740`) and in `LEDGER.md:3752-3800`: v0.50 removed the floor (gain-pivoted
at the founder value) and **kills/day fell in 3/3 paired seeds** — the one v0.50
result that survived the run-length correction (`LEDGER.md:3860-3866`, "kills per day …
survives"). The source comment says it outright: *"the floor is LOAD-BEARING …
Predation needs a baseline interest to stay reachable."*

So the file records (a) that the constant is load-bearing for predation and
(b) that predation-as-mortality-regulator is "a real upgrade to the weakest
mission pillar", and **no entry connects them.** Under the project's own test —
*if a result had to be written into the code, it doesn't count* — the second
claim cannot stand at its current strength while the first is true.

Note the honest limit, which I am not hiding: `carnivory` (a different gene) does
gate ATTACK, since `rateA` is proportional to `carn*meatValue` and the
`rateA > 1e-12` guard kills the branch at `carnivory = 0`; evolved `carnivory` in
these runs is 0.08-0.35, genuinely nonzero. Predation here is therefore not
*purely* the constant. But the quantity that decides ATTACK *versus* GRAZE — the
attraction multiplier — is 84% constant at the median and ~100% in two of the
runs being counted as the pillar's best evidence.

### What follows

The predation-share numbers should stay on record — they are correctly computed
and the day-800-vs-day-1600 growth is a real within-run result. What should be
retracted is the reading: **"a real upgrade to the weakest mission pillar" is not
supported, because the pillar's metric is substantially supplied by
`0.5 +`.** The defensible statement is narrower: *predation accounts for a growing
share of animal deaths, but in most surviving worlds the meat-attraction gene has
been selected toward zero and the behaviour is sustained by a hardcoded floor;
whether carnivory is emergent here is untested.*

The measurement that would settle it already has a design on file and is not a
new hypothesis: `LEDGER.md:3817-3822` and `FINDINGS.md:262-269` both name the
same successor mechanism (reachability via exploration noise in *action
selection*, leaving the gene unfloored). Until something like that exists, the
mission-relevant number to track is not predation share but predation share
*conditional on evolved `meatAttraction`* — free to compute from logs already on
disk, and this audit's table is the first pass at it.

---

## F2. The 25,000-slot plant array is binding across the live v0.51 corpus, and it will dominate the 1x control arm before that arm produces a single scoreable seed

**Severity: HIGH — would change a conclusion, and it is actionable before the
data lands rather than after.**
**CONFIRMED.**

### The long-lived assumption

`HANDOFF.md:37-39`, stated without qualification:

> Confirmed via an isolation test at the *original* 90k/40k arena (no shrink) —
> identical results to the shrunk-arena version, so the arena shrink used
> throughout was purely a speed optimization, not load-bearing.

The underlying test (`LEDGER.md:1690-1704`) was **one seed (1337), 1200 days,
`k_photoCost` 0.012, `caps seen [0]` clean**, plus a second full-arena seed. Its
own wording is properly conditional — *"the slot count was never the actual
constraint **once this dose is applied**"* — and HANDOFF dropped the condition.

### What the current corpus actually shows

`caps` is a bitfield; `evosim-v0_51_0.html:3255-3257` defines bit 1 as
`P.freeN === 0`, i.e. the plant slot array is full. Live plants and seeds share
that array (`:956-996`, `P.freeN = M` with `P.live`/`P.seeds` as sub-counters), so
`plants + seeds` is what must reach `maxPlants`.

Across all 82 standing-batch v0.51 logs in `runs/standing-collect/`:

| arm | runs where the plant slot cap binds | median peak `(plants+seeds)/maxPlants` |
|---|---|---|
| 3x (`k_photoCost` 0.012), n=39 | **21 (54%)** | **1.000** |
| 5x (0.020), n=43 | 4 (9%) | 0.445 |

Worst cases spend a quarter to nearly half the run pinned: seed 41216 42.2%,
41091 29.7%, 41129 26.6%, 41131 25.6%, 41082 24.2%. The local 2400-day ladder is
the same picture — seed 4002 17.2% of samples capped, 10008 10.8%, and even
**seed 1337 itself touches the bound at 2400 days** (peak `plants+seeds` exactly
25000), the seed whose clean `caps seen [0]` at 1200 days is the entire basis for
"the arena is inert".

So: the claim "the arena shrink is purely a speed optimization" is **false for the
3x arm at the run lengths now standard**, and it has been carried forward
unqualified in the file CLAUDE.md tells every session to read first.

### Why this lands on the head of the queue specifically

The frozen pre-registration at `LEDGER.md:5714-5735` adds arm 0 as
`cfg-patches/arena-photocost-1x.json` — `maxPlants 25000, maxAnimals 11000,
k_photoCost 0.004` — described as *"same arena caps, only `k_photoCost` back to
the default 0.004 — a clean one-variable dose series"*, and its HIT branch reads:

> …respiration cost is a monotonic extinction lever across the whole range and
> the shipped default is already the survivable end of it.

The four 1x seeds already running locally say that reading will not be available:

| file | day reached | `plantsHi` | `maxPlants` |
|---|---|---|---|
| `runs/standing-1x/seed-50001.json.progress.json` | 360 | **25000** | 25000 |
| `runs/standing-1x/seed-50002.json.progress.json` | 280 | 24998 | 25000 |
| `runs/standing-1x/seed-50003.json.progress.json` | 160 | **25000** | 25000 |
| `runs/standing-1x/seed-50004.json.progress.json` | 200 | **25000** | 25000 |

Four of four are at, or two slots from, the array bound inside the first 360 days
— before the day-800 cutoff the prediction is scored at. `seed-50004`'s 200-day
checkpoint already logs 2.5% of samples with `caps & 1`.

That is not a dose control. It is `maxPlants` deciding the plant standing crop
while `k_photoCost` is nominally the variable — **the exact artifact whose
discovery started this whole investigation** (`FINDINGS.md:129-136`, "`maxPlants`
(a slot-array size, not a biological limit) was binding regardless of predation in
every default-config run"). Lowering `k_photoCost` back to 0.004 while holding the
shrunk arena reintroduces it by construction, and the frozen prediction was
written without checking.

### An honest limit on this finding

Within the 3x arm, cap-binding does **not** separate outcomes: alive-at-day-800 is
9/13 among capped runs and 7/11 among uncapped (Fisher p = 1.000). So I am *not*
claiming the frozen 3x figure of 16/24 is itself an artifact. The claim is
narrower and I think unavoidable: the arms differ six-fold in how often the cap
binds, the 1x arm will bind essentially always, and n=24 is far below the n≈60
this project measured as necessary to resolve a 0.2 difference
(`FINDINGS.md:225-232`) — so a within-arm null at n=24 does not license ignoring a
six-fold mechanical difference between arms.

### What follows

The dose series can be made clean at near-zero cost and without touching a hard
rule (`maxPlants` is a cfg constant, not a gene bound — rule 8 does not apply, and
this is rule 6's CFG-patch path, not a shape change). `cfg-patches/photocost-only-
fullarena.json` (0.012 at 90k/40k) already exists, and rotation arm 3 is already
the shipped 90k/40k default at 0.004. Running the dose series at 90k/40k gives
1x/3x/5x with the cap off in every arm, at the cost of slower runs — the *only*
thing the shrink ever bought (`LEDGER.md:1616`, `1702-1703`).

If the 25k arm is kept for speed, then the prediction needs its reading amended
before scoring: state in advance that an arm whose runs spend a material fraction
of samples with `caps & 1` is reported as **cap-limited, not dose-limited**, and
that the monotonic-lever conclusion is unavailable for it either way. Amending a
frozen prediction after seeing partial data is itself a hazard — which is why this
should be settled now, while only 4 partial 1x seeds exist and none has reached
day 800.

---

## F3. A prediction was parked as "can't-tell" for a reason that is answered by one line of the build and one column of the log

**Severity: MODERATE — an unscored prediction that should be scored a MISS, and it
is the same fact as F2.**
**CONFIRMED.**

`LEDGER.md:5665-5668`:

> Not scored here: that same run's `caps seen [0, 1]` flag. Standing plants peak
> at 24,691 against a 25,000 cap and never come within 0.5% of it, so the
> plant-count cap is not what tripped it. **Until I know which counter `caps[]`
> increments**, the arena patch's own written prediction ("cap stops binding") is
> **can't-tell**, not a hit.

Three things are wrong here and all were checkable in under a minute:

1. **The build states it.** `evosim-v0_51_0.html:3255` — `// caps is a bitfield:
   1 plant slots full, 2 animal slots full, 4 seed bank full`, and `:3256` —
   `(P.freeN === 0 ? 1 : 0)`. There was nothing to wait to know.
2. **The log proves it.** In `runs/stationarity/seed-10008-2400d.json`, all **52
   of 480** samples flagged `caps & 1` have `plants + seeds` equal to **exactly
   25000 = maxPlants**, e.g. day 1700 (24133 + 867), day 1955 (23407 + 1593), day
   2390 (24138 + 862). The array is full. The cap binds.
3. **The reasoning that dismissed it fails because seeds share the slot array.**
   "Standing plants peak at 24,691, so the cap is not what tripped it" treats
   `plants` as the only occupant. It is not (`:956-996`). Incidentally 24,691 is
   1.24% below 25,000, not the ">0.5%" clearance the entry claims.

So the arena patch's prediction — that raising `k_photoCost` makes the slot cap
stop binding — is a **MISS on this run** (10.8% of samples pinned), not a
can't-tell, and per hard rule 3 that means the diagnosis was wrong rather than
that the constant needs to be bigger. It is a MISS on 54% of the 3x arm corpus-
wide (F2). `analyze.py:67-69` had already printed
`caps seen [0, 1]   <<A BOUND IS DOING THE SELECTING, nothing below means what it
looks like` on this exact run; the LEDGER itself has flagged four prior instances
of "the better number was already in the digest and going unread"
(`LEDGER.md:4985-4989`). This is the fifth.

---

## F4. The frozen pre-registration's definition line does not produce its own frozen numbers

**Severity: MODERATE — a scoring hazard on the head-of-queue prediction. Hygiene
in form, consequential in effect.**
**CONFIRMED.**

`LEDGER.md:5721-5733`:

> Frozen comparison values, fixed now and not to be re-derived later: **3x = 16/24
> (67%), 5x = 11/30 (37%), cutoff day 800, extinct = final animals 0, complete
> blocks only.**
> - **HIT** if the 1x arm … is **alive at day 800** at a rate **>= 67%** …

I rebuilt both from the logs over the four named complete blocks (41080-91,
41100-11, 41120-31, 41180-97; block membership and arm confirmed by diffing each
log's own cfg against build defaults, never by agreement between runs):

| definition | 3x | 5x |
|---|---|---|
| animals > 0 **at day 800** | **16/24 = 67%** | **11/30 = 37%** |
| `final animals 0` → alive at run end | 12/24 = 50% | 9/30 = 30% |

Both frozen headline values reproduce exactly under the first definition. The
second definition — the one written into the frozen line — yields **50% and 30%**,
and matches instead the *adjacent* "extinct 50% / 70%" column. So the frozen block
bundles two mutually inconsistent definitions of the same word, and the number a
future scorer computes for the 1x arm depends on which sentence they read. A 1x
arm landing at, say, 55% is a CAN'T-TELL under one reading and a clear HIT over 3x
under the other.

Worth one further note while the prediction is still open: "alive at day 800"
counts four seeds — 41081, 41086, 41087, 41127 — that were alive at day 800 and
then died (at days 1245, 1205, 1020, 1245). This project has established twice
over that a short horizon overstates persistence (`LEDGER.md:5284-5288`,
"1600-day persistence is itself a truncation artifact"). Day 800 was chosen for
rule-7b matching, which is right; but the metric being frozen is *"not yet dead at
day 800"*, and the entry should say so rather than call it persistence.

**What follows:** pick one definition in a single sentence, restate both frozen
values under it, and note that this is a disambiguation of an already-written
prediction rather than a re-derivation — before the first 1x seed reaches day 800.

---

## F5. `FINDINGS.md` and `HANDOFF.md` carry four superseded numbers with no retraction

**Severity: HYGIENE — but `FINDINGS.md`'s stated purpose is to be the one file a
new session trusts, and every item below is exactly the failure it was created to
prevent.**
**CONFIRMED.**

`FINDINGS.md:1-22` states the rule: *"A walked-back claim is edited or deleted
here, not just corrected later in `LEDGER.md`."* Last commit touching
`FINDINGS.md` is `10942ef`; `HANDOFF.md` is `8644f96`. Both predate the work that
overturned these.

| where | what it says | what supersedes it |
|---|---|---|
| `FINDINGS.md:41-47` and `HANDOFF.md:77-79` | Actions ceiling "roughly 40-50 simultaneous jobs", HANDOFF adding "**not the 20 originally assumed**" | `CLAUDE.md:147-152`: **"CORRECTED … the real ceiling is 20 simultaneous *running* jobs, not the 40-50 previously recorded here."** HANDOFF has it exactly inverted. |
| `HANDOFF.md:43-47` dose table, `5x … 3/4 (75%), leading candidate`; `HANDOFF.md:83-84` "if 5x continues to lead, promote it (not 3x)" | 5x is the leading `k_photoCost` dose | `FINDINGS.md:174-184` itself: **RESOLVED, no difference**, permutation p=0.590, Fisher p=1.000, 3x stands. The two files contradict each other. |
| `FINDINGS.md:195-202` "~1/3 extinctions … Roughly a third of runs go extinct early" | extinction rate ≈ 33% | Establishment batch 7/14 and 8/15 extinct at 1600 d (`LEDGER.md:4864-4867`); complete blocks measured in this audit: 3x 12/24 = 50%, 5x 21/30 = 70%. |
| `FINDINGS.md:61-67` "Predation causes 23.6% of animal deaths … exceeds 50% in only **5/120** runs" | the carnivory pillar number | `LEDGER.md:5757-5775`: 35.4% median, 6/21 above 50% on mature worlds; the LEDGER explicitly says the old figure "was not wrong; it was early" — and did not update `FINDINGS.md`. (Read alongside **F1** before promoting the new number.) |

Two smaller ones in the same class: `HANDOFF.md:121` is headed **"Current state —
v0.49.0"** while the shipped build is v0.51 and v0.50 was scored and reverted
(`LEDGER.md:3752`); and `CLAUDE.md`'s Files table still names
`evosim-v0_50_0.html` as "the build", never mentions `evosim-v0_51_0.html`, and
states an explicit deletion criterion for `evosim-v0_49_0.html` ("a 3-seed
ecological retest … written into `LEDGER.md`, win or lose") which **has been
satisfied** — yet all three HTML files are still present.

**What follows:** this is cheap to fix and I would not normally file it, except
that `FINDINGS.md` exists specifically because a chronological ledger lets a
future reader re-adopt a superseded claim. It is currently doing that job for four
claims. The Actions-ceiling row is the sharpest, because HANDOFF states the
corrected value as the thing that was wrong.

---

## Categories deliberately left empty

**Predictions never scored.** `DAILY-AUDIT.md:61-79` lists 6 apparently-unscored
predictions. I traced all six. Five are naming mismatches, not gaps: L3141 and
L3576 and L4371 and L4412 are themselves *scoring* headings that the keyword
matcher classified as predictions, and L3597 (the `k_intake` reciprocal arm) was
scored at `LEDGER.md:4080-4093` under the heading "intake-down completes at
matched windows: null, and the arm is retired", with the Ambiguous branch
explicitly fired. The sixth, L5714, is the 1x control — genuinely open because no
1x seed has reached day 800 yet (see F4, which is about its wording, not its
absence). **Nothing filed. If it is worth avoiding tomorrow's re-derivation,
`audit.py` could match on `[Lnn]` tags or explicit `SCORED:` markers rather than
keyword overlap.**

**Rule 7b violations / statistics compared across incompatible run lengths.** I
recomputed the two freshest quantitative entries from source logs. The predation
entry (`LEDGER.md:5750-5790`) reproduced to every digit — 26.4%, 35.4%, mean 31.5,
range 4.7-57.8, 11/21, 6/21, starvation 64%, 3x 24.7% n=12, 5x 49.0% n=9 — and its
matching claim holds: all 21 survivors did run to exactly 1600 days, and both
cutoffs are computed on the same runs, so the day-800-to-day-1600 comparison is
within-run and legitimate. The frozen 3x/5x block reproduced exactly at a fixed
calendar day-800 cutoff. The local ladder table (`LEDGER.md:5552-5558`,
`5517-5524`) reproduced: 4001 31→216, 1337 76→82, 10001 59→32, 10015 488→89, 4002
12→0, 10008 677→681. The seed-10008 stationarity figures (+21.2% plants, +25.8%
bio) and the 1745→24,326 plant climb reproduce as `analyze.py` window means — I
checked raw samples first, got 1938/24447, and confirmed the difference is window
smoothing rather than an error before filing anything. **Nothing filed.**

**Busy-but-unproductive work.** The one real instance — 82 cold seeds accumulated
with no control arm — was caught by the project itself
(`LEDGER.md:5672-5686`) and fixed the same cycle with a 4-way rotation that adds
both a 1x arm and a shipped-defaults arm. Re-filing it would be scoring the
project for an error it had already found. Per `AUDIT-PROTOCOL.md:133-138` I also
did not evaluate throughput or utilisation. **Nothing filed.**

---

## Ranking

| # | changes a conclusion? | one line |
|---|---|---|
| **F1** | **yes** — retracts a claim made this session | the carnivory pillar number is 84% a hardcoded `0.5 +` at the median, and ~100% in two of the six worlds counted as its best evidence |
| **F2** | **yes** — invalidates the stated reading of the head-of-queue prediction *before* it lands | the 25k plant array binds in 54% of 3x runs and in 4/4 of the 1x control seeds already running; "the arena shrink is purely a speed optimization" is false at current run lengths |
| **F3** | **yes** — converts a can't-tell to a MISS | `caps` bit 1 is defined in the build and provable from the log: `plants + seeds == maxPlants` at every flagged sample |
| **F4** | scoring hazard, not yet an error | the frozen pre-registration's definition line yields 50%/30%, not the 67%/37% it freezes |
| **F5** | hygiene | four superseded numbers still live in the two files a new session is told to trust, including an Actions ceiling stated as the inverse of the measured one |
