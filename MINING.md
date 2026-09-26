# Mining the evosim 1.x run logs (2026-09-26)

Analysis only; no simulations run, no repo files changed. Scripts and pickles:
`scratchpad/mine/` (`load.py`, `feat.py`, `q1*.py` … `q4*.py`).

## Data

- 476 unique `evosim1-log` files (4 duplicates dropped by final-state signature, 1 log under 5 samples dropped). The `runs/h22`, `runs/h23` files are old-engine (`evosim-log` 0.58) and are excluded.
- `version` is `1.0.0` in every log, so it cannot separate engines. Engine generation is inferred from which cfg keys exist:
  - E0: no `dietCurve` key (L8/L9, 2026-09-25 morning).
  - E1: `dietCurve` exists but not `mateDist`; mostly `upFixed` 0.01 with sex (T, U, V, W-small/medium).
  - E2: `mateDist` and `gutCap` exist; curve-2 era (X, Y, Z, AB, W-sex-md10, V:base, C2).
  - E3: `headDown` exists (V:v0/v7/r0/r1/x0/x1/f5, AC-1M).
  - E4: `browse` exists (V:b1/b15/b2/g75/g75b2, f2b2/f4b2/f6b2, AD-1M).
  Settings are grouped by batch label, and each label was checked to hold one cfg signature.
- The main analysis set is the 290 unseeded worlds from E2–E4 with at least 300k ticks. 168 of them (58%) are predator-dominated.
- Predator-dominated uses the HANDOFF definition: regime (share of samples after max(establishment, 60k) and up to 400k with meatShare > 0.15) above 50%. 1M runs are truncated at 400k for this. E0/E1 are reported separately; their outcome rates are 0–40% and mostly 0.
- Early features are means over 10k-tick windows ending at 20k, 30k, 40k and 60k (`w20`…`w60`), plus windows 10k and 20k after `establishedAt`. Population is scaled to a 64x64 world. Plant mass is per cell. `predFrac` is predators/adults (adults living mostly on meat by lifetime intake). `dietSD` is the spread of the diet histogram. `maxSpMeat` is the meat share of the most carnivorous logged cluster.

## 1. Early predictors of a predator-dominated world

**Early predation is almost universal. What differs is whether it lasts.** Take the first time the 10k-rolling meat share exceeds 0.15:

| | worlds | median first time | never |
|---|---|---|---|
| predator-dominated | 168 | 20.5k | 0 |
| not | 122 | 20.5k | 22 |

Much of the meat before ~25k is bootstrap carry-over. Founders have random diets, and at t = 500 meat share is often ~0.5. The state is sticky but not locked: for the 10k-mean state (meat > 0.15), P(still on after 100k) = 0.75 and P(off → on within 100k) = 0.18.

Univariate AUC for "regime > 50%". Pooled over the 290 worlds, and within batch (only pairs from the same batch, which removes setting effects):

| feature | w20 | w40 | w60 | within-batch w20 / w40 / w60 |
|---|---|---|---|---|
| meat share | 0.61 | 0.69 | 0.72 | 0.57 / 0.68 / 0.69 |
| kill share | 0.62 | 0.69 | 0.73 | 0.58 / 0.68 / 0.71 |
| predFrac | 0.63 | 0.70 | 0.71 | 0.57 / 0.69 / 0.70 |
| diet spread (dietSD) | 0.62 | 0.70 | 0.72 | 0.62 / 0.67 / 0.70 |
| share with diet ≥ 0.5 | 0.62 | 0.66 | 0.68 | 0.63 / 0.63 / 0.66 |
| most carnivorous cluster's meat | 0.60 | 0.69 | 0.72 | 0.54 / 0.70 / 0.71 |
| plant mass | 0.56 | 0.63 | 0.66 | 0.56 / 0.62 / 0.65 |
| species count | 0.56 | 0.65 | 0.65 | 0.57 / 0.65 / 0.67 |
| diet gene | 0.59 | 0.64 | 0.64 | 0.58 / 0.63 / 0.59 |
| detox | 0.57 | 0.54 | 0.51 | 0.60 / 0.57 / 0.54 |
| plant defence | 0.41 | 0.41 | 0.42 | 0.40 / 0.42 / 0.44 |
| starvation share of deaths | 0.45 | 0.38 | 0.37 | 0.45 / 0.42 / 0.44 |
| weapon | 0.52 | 0.53 | 0.54 | 0.53 / 0.50 / 0.49 |
| body size | 0.53 | 0.50 | 0.50 | 0.53 / 0.50 / 0.45 |
| kills per 1000 ticks | 0.58 | 0.64 | 0.67 | 0.51 / 0.56 / 0.60 |
| population | 0.50 | 0.43 | 0.42 | 0.44 / 0.45 / 0.44 |

Early weapon, size, speed, sense and attention genes carry no signal (AUC 0.45–0.55). The candidates in the brief (weapon, diet, size, kills rate) are weak or empty. The informative quantities describe how meat-eating is distributed: a few specialists (predFrac, diet spread, a clearly carnivorous cluster) rather than everyone biting a little.

Classifiers, validated leave-one-batch-out (fit on all other batches, score the held-out batch). Majority class = 57.9%. Predicting each batch's own majority in-sample gives 66.2%, which is roughly what knowing the setting is worth.

| window | logistic, 13 features: acc / AUC | 4 features (meat, dietSD, predFrac, plant mass) | best single threshold |
|---|---|---|---|
| 20k | 61.7% / 0.63 | 58.3% / 0.61 | predFrac > 0.005: 63.8% |
| 30k | 64.1% / 0.67 | 62.4% / 0.65 | dietSD > 0.070: 64.5% |
| 40k | 68.6% / 0.74 | 65.9% / 0.69 | predFrac > 0.037: 67.2% |
| 60k | 69.0% / 0.74 | 68.6% / 0.72 | meat > 0.19: 70.0% |

The ceiling from ≤ 60k data is about 70% accuracy against a 58% base. At 20k the models are barely above base.

Among worlds already predatory at 40k (meat > 0.15, n = 218, 63% go on to dominate), within-batch AUC:

| feature | AUC | median, dominating / not |
|---|---|---|
| most carnivorous cluster's meat | 0.73 | 0.51 / 0.38 |
| predFrac | 0.69 | 0.20 / 0.12 |
| meat share | 0.69 | 0.31 / 0.24 |
| dietSD | 0.68 | 0.12 / 0.09 |
| plant mass | 0.64 | 5.8 / 5.2 |
| population | 0.43 | 787 / 843 |
| plant defence | 0.42 | 0.33 / 0.36 |

Size, weapon, speed and sense stay at 0.44–0.53.

## 2. End states and exits from the predator state

End state from the 380–400k mean (or the last 20k for 300k runs). Classes, in this order: predator (meat > 0.15; `g` marks a predator world with mean size ≥ 5), dwarf (size ≤ 0.35), giant (size ≥ 5), other.

| setting | n | predator [giant] | dwarf | giant | other | at 1M |
|---|---|---|---|---|---|---|
| E1 upFixed 0.01 (T, U, V-f010) | 72 | 1 | 0 | 1 | 70 (mid-size, peaceful) | |
| E1 V-f003-asex / -sex | 10 / 10 | 4 / 0 | 4 / 9 | 0 | 2 / 1 | |
| E1 W-small / W-medium | 10 / 10 | 4 / 1 | 6 / 6 | 0 | 0 / 3 | |
| E2 X-curve2, Y-small, Y-medium | 30 | 17 | 10 | 0 | 3 | |
| E2 X-senses | 10 | 2 | 7 | 0 | 1 | |
| E2 AB-base / gut2 / gut1slow | 30 | 5 / 4 [d1] / 2 | 5 / 4 / 7 | 0 | 0 / 2 / 1 | |
| E2 sex+md (W, Y) | 20 | 5 | 11 | 0 | 4 | |
| E2 Z-1M | 10 | 6 | 3 | 0 | 1 | 5 P, 5 dwarf |
| E2 V:base, C2 | 12 | 9 | 3 | 0 | 0 | |
| E3 v0 / v7 | 12 / 12 | 7 / 8 | 4 / 3 | 0 | 1 / 1 | |
| E3 r0 / r1 / x0 / x1 / f5 | 40 | 15 [1] | 21 | 1 | 3 | |
| E3 AC-1M | 10 | 5 | 4 | 1 | 0 | 1 P, 7 dwarf, 2 other |
| E4 b1 | 8 | 3 | 3 | 0 | 2 | |
| E4 b15 | 12 | 5 | 0 | 0 | 7 (size 1.0–3.0) | |
| E4 b2 | 12 | 8 [2] | 1 | 2 | 1 | |
| E4 g75 / g75b2 | 8 / 8 | 3 / 3 [1] | 4 / 0 | 0 / 5 | 1 / 0 | |
| E4 f2b2 / f4b2 / f6b2 | 12 each | 8 [3] / 7 [1] / 4 [1] | 0 | 4 / 5 / 7 | 0 / 0 / 1 | |
| E4 AD-1M browse2 / browse4 | 10 / 10 | 7 [2] / 7 [1] | 0 | 3 / 3 | 0 | 4 P [1], 6 giant each |

Worlds that are neither predator, dwarf nor giant are uncommon after E1: 29 of 290. They are mostly b15 mid-sized grazers or near-threshold worlds with meat 0.10–0.15.

### When worlds leave the predator state

An exit is defined on the 10k-rolling meat share: on (above 0.15) for at least 40k, then below 0.08, staying under 0.15 for the next 40k (or until the run ends, with at least 20k left). This finds 185 exits in all eras. Of these, 142 fall after 60k in E2–E4.

- **The exit rate is the same in every engine era: about 0.2 per 100k ticks spent in the predator state.** E2 had 44 exits over 23.2M predator-state ticks (0.19), E3 38 over 16.3M (0.23), E4 60 over 28.5M (0.21). At that rate a predator phase lasts about 500k ticks on average; half end within ~330k.
- **Plant height changed where worlds fall, not how often.** In E2/E3, 63 of 82 exits went to dwarf worlds. In E4, 42 of 60 went to giant worlds and 8 to dwarf worlds.
- Timing: median exit tick 250k for both kinds (10–90%: 140k–600k). Median time in the predator state before exit: 214k (dwarf exits), 226k (giant exits).
- Returns: 12 of 71 dwarf exits and 11 of 45 giant exits came back to meat > 0.15 before the run ended. Most runs end at 400k, so this undercounts.

**Exits into a dwarf world** (n = 68). Median ratio to the value 100–110k before the exit:

| k ticks before exit | 60 | 50 | 40 | 30 | 20 | 10 | 0 |
|---|---|---|---|---|---|---|---|
| plant mass | 0.90 | 0.83 | 0.72 | 0.61 | 0.49 | 0.36 | 0.27 |
| plant stature | 0.94 | 0.91 | 0.87 | 0.79 | 0.74 | 0.63 | 0.51 |
| diet gene | 0.88 | 0.85 | 0.86 | 0.78 | 0.71 | 0.63 | 0.56 |
| predFrac | 0.92 | 0.87 | 0.77 | 0.71 | 0.60 | 0.40 | 0.15 |
| starvation share of deaths | 1.08 | 1.17 | 1.54 | 2.23 | 3.68 | 3.91 | 8.07 |
| body size | 0.97 | 0.94 | 0.90 | 0.85 | 0.71 | 0.59 | 0.49 |
| weapon | 0.96 | 0.92 | 0.82 | 0.75 | 0.67 | 0.62 | 0.50 |
| kills per head | 1.16 | 1.09 | 1.11 | 0.98 | 0.86 | 0.60 | 0.22 |
| meat share | 1.04 | 1.00 | 0.97 | 0.90 | 0.82 | 0.67 | 0.36 |
| population | 0.94 | 0.95 | 0.96 | 0.97 | 1.04 | 1.11 | 1.11 |

- Plant mass, plant stature, the diet gene and predFrac start falling 50–60k before the exit. Kills per head and meat share are still at or above baseline 40k before.
- Population is flat, so the plant decline is not caused by more grazers. Starvation rises from −50k. Body size falls from −40k.
- By trophic cluster: the main grazer cluster shrinks from size 0.54 (−100k) to 0.34 (−30k) to 0.31, the size floor. Meat-eaters grow from 3.2 to 4.6. The predator/prey size ratio goes from 3 to 10, and then the meat-eaters disappear.

**Exits from giant worlds** (n = 45):

- Grazers grow from 5.2 (−100k) to 6.4 (−60k) to 8.0 (−10k).
- Meat-eaters are already at 10.1–11.8, against a size gene maximum of 12 (`evosim.html` line 207). The size ratio falls from 1.61 to 1.41.
- 23 of the 32 giant exits that had a meat-eater cluster 20–60k before had it at size ≥ 10.
- Mean armour rises 16% by −50k and 30% by −30k. Population falls 18% by −60k and 40% by −10k. Kills per head drop to 0.78 at −50k.
- Among E4 predator worlds still alive at 400k, the largest meat-eater cluster is at 11.3–12.0 in 24 of 54. The persisting worlds with a ratio near 1 (f2b2 s403, s410; b2 s403; browse4 s710) have meat of only 0.17–0.29.

**Early warning.** Predicting "exit within the next 60k" from any predator-state 10k window (5,818 windows, 423 positive), validated leave-one-batch-out:

- Logistic regression on 12 level and 30k-trend features: AUC 0.71.
- Current meat share alone: 0.67.
- 30k trends alone (plant mass, diet, predFrac, size, armour): 0.65.

The lead signal is real in the average but noisy for any single world.

## 3. Carnivore specialisation (a cluster with meat > 0.5 and at least 10 animals)

- **Most carnivore clusters are present from the bootstrap.** 255 of 290 worlds show one at some point by 400k. In 148 of them it is already there by 30k, when establishment is at ~8k and founders have random diets.
  - A cluster that appears after 40k, following at least 20k without one, and persists (10 of the next 20 samples) occurs in 83 worlds.
  - Of the 130 worlds with a carnivore cluster at 400k, 41 have had one continuously since ≤ 30k. In V:b2 that is 6 of 8, so most of the browse-2 "8 of 12 carnivore clusters" are clusters kept from the bootstrap.
  - Early clusters survive continuously to 400k in 20 of 79 E2/E3 worlds and 21 of 69 E4 worlds (b2: 6 of 11).
- **New clusters start as omnivores that kill.** Diet gene at appearance: median 0.36 (IQR 0.27–0.47); 31% are below 0.3. A cluster with diet ≥ 0.5 follows in 182 of 255 worlds, a median of 20k after the first carnivore cluster. Across 10k time steps, a rise in predFrac is followed by a rise in the diet gene (lag-1 r = +0.09; lag −1 r = +0.01).
- **Where new clusters arise** (by batch, out of n):
  - Most: AB-gut2 6/10, AC-1M 6/10, Y-medium 5/10, v7 5/12, AB-gut1slow 4/10, b1 4/8, g75 4/8, f4b2 4/12.
  - Least: f6b2 0/12, x0 0/8, browse4 1/10, b15 1/12, f5 1/8, r0 1/8, b2 2/12.
  - Height worlds get their carnivores early; new ones rarely arise later.
  - A meat gut (a cluster at diet ≥ 0.5) at any time: v0 11/12, Y-medium 10/10, f4b2 9/12, b2 9/12. Only gut1slow (0/10) and b1 (2/8) stand out low.
- **Conditions 10–30k before a new cluster**, compared with predator-state windows (meat > 0.15) in which no cluster was present within ±40k (58 vs 248 windows):

  | feature | before a new cluster | control | AUC |
  |---|---|---|---|
  | predFrac | 0.089 | 0.046 | 0.78 |
  | dietSD | 0.094 | 0.067 | 0.77 |
  | prey clump | 0.99 | 0.84 | 0.74 |
  | kill share | 0.18 | 0.14 | 0.73 |
  | population | 802 | 490 | 0.63 |
  | mean size | 1.39 | 2.46 | 0.30 |
  | armour | 0.10 | 0.17 | 0.29 |
  | weapon | 0.20 | 0.28 | 0.35 |
  | sense | 6.3 | 7.3 | 0.37 |

  New carnivores arise where killing is concentrated in a subset and prey are small, numerous and unarmoured. Against all non-cluster windows, not only predatory ones, pre-origin windows mainly show a running kill regime: predFrac AUC 0.92, meat 0.88, starvation share 0.23.

## 4. Other correlations

All are over the 290 E2–E4 worlds, using 60k–400k means. "Within" is the Spearman correlation computed inside each batch and then averaged; "lagged" is the correlation of 10k-tick changes at the stated lag, with each world z-scored and all worlds pooled.

- **Plant defence does not track predation.** Within-batch rho is −0.04 with meat share and −0.08 with kills. It does track grazer detox (+0.42). Its time structure fits a plant–grazer cycle:
  - Defence rising is followed by detox rising 10–30k later (r = +0.18 to +0.21).
  - Detox rising is followed by defence falling 10–30k later (r = −0.14 to −0.17).
  - This runs regardless of predators. The trophic cascade shows up in plant mass (meat vs plant mass rho +0.57; same-bin r = +0.39, and meat leads plant mass by 10k at +0.16) but not in plant defence.
- **Predation speeds up life history.** Kills per head vs births per head: rho +0.96. Kills vs the reproduction-threshold gene reproT: −0.46. A rise in kills is followed by falling reproT 20–30k later (r ≈ −0.10). Medians at 400k:

  | | reproT | childE | birthSize |
  |---|---|---|---|
  | predator worlds | 0.37 | 0.25 | 0.53 |
  | dwarf worlds | 0.41 | 0.37 | 0.38 |
  | giant worlds | 0.58 | 0.52 | 0.40 |

  So under predation, animals breed at a lower energy threshold and give less energy per child, but at a larger birth size.
- **Order of trait changes after kills** (lagged r, 10k): sense +0.15, speed +0.10, armour +0.05. A size increase is followed by fewer kills (−0.15). Weapon leads armour (+0.12 forward vs +0.02 backward), so prey armour follows predator weapons with a ~10k lag. Armour is highest in giant worlds (0.44 at 400k vs 0.09 predator, 0.01 dwarf).
- **Prey clumping moves with kills in the same 10k bin** (r = +0.26) with no lead or lag; world-level rho +0.46. Sense range correlates negatively with clumping within batches (−0.41): worlds that evolve long sight clump less. Dwarf worlds lose sense range (3.4 vs 6.5 in predator worlds).
- **Attention genes (attSize, attKin, attWeapon) do not correlate with predation** at world level (|rho| ≤ 0.04). Neither does choosiness (0.03).
- **Seed number carries no outcome across settings.** Seeds 401–412 appear in 7–11 settings each; per-seed mean regime is 0.47–0.84, and a permutation test gives p = 0.15. Early states differ by setting from the first 20k.
- **Medium worlds** (96x96) were predator-dominated in 13 of 20 against 155 of 270 small worlds (Y-medium 10/10, W-sex-md10 3/10). The sample is too small to separate world size from batch.

## Caveats

- Regime and early meat share are the same quantity at different times. Early meat carries part of the outcome by autocorrelation, and the bootstrap inflates meat before ~25k.
- Clusters are the logger's per-sample colour clusters, not lineages. "Continuous since ≤ 30k" means some carnivore cluster was present without a 20k gap, not that it was the same lineage.
- The exit lead-lag profiles are medians of ratios over worlds with very different baselines. Single worlds are noisy (early-warning AUC 0.71).
- E1 batches have almost no outcome variance, so they are excluded from the classifiers.

## Suggested experiments

1. **Raise the size gene maximum from 12 to 24** with `browse` 2, seeds 401–412 and 701–710. Prediction: fewer exits from giant worlds, and meat-eaters keeping a size ratio above ~2. If giant exits stay the same, the upper bound is not what ends them. This changes a gene range, not a behaviour.
2. **Separate founder carnivores from evolved ones.** Log a founder-lineage id per animal and per cluster (logger only), or bound founder diet to ≤ 0.2 in a test batch. Then re-score the browse table on clusters that arose after 40k. Current data suggests height mostly keeps bootstrap carnivores alive rather than creating new ones.
3. **Test whether plant stature decline drives dwarf exits.** Plant mass and stature fall 50–60k before the collapse, while kills are still high. Freeze plant stature evolution (stature mutation 0) in E3 settings and see whether the rate of exits into dwarf worlds drops. If it does, the dwarf race starts in the plants.
4. **Target the exit rate, not the onset.** Onset happens by ~20k in nearly every world, and the exit rate has been ~0.2 per 100k across three engine changes. Score levers by exits per 100k predator-state ticks (tooling: add this to `v1score.py`), run on 1M-tick worlds.
5. **Log per-cluster weapon, armour, speed and reproT** so arms races and life-history shifts can be split by trophic level. Today they are only visible in means.
6. **Probe the plant defence and detox cycle directly.** Run a batch with no animals able to kill (e.g. `dmg` 0) and check whether the defence/detox lag structure is unchanged. If it is, that confirms the cycle is between plants and grazers only.
