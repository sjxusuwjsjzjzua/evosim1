# Evidence pack for the program audit — 2026-09-11

Compact history. Every structural version, its one change, its prediction, its
outcome. Generated for the auditor so it reads facts, not my summary of them.

## Scale of the effort
- Project start 2026-08-08; **34 days**.
- 211 commits on `claude/evolution-sim-v047-audit-jft25c`.
- **2,565 result branches**, 2,309 logs collected locally.
- `LEDGER.md` 8,115 lines; `HANDOFF.md` 690; `CLAUDE.md` 245.
- Builds shipped in this period: v0.50, v0.51, v0.52, v0.53, v0.54, v0.55.

## Structural versions and outcomes

| ver | one structural change | prediction | outcome |
|---|---|---|---|
| v0.50 | remove the `0.5 +` floor on ATTACK's attraction | predation falls, carnivory becomes selectable | kills fell 3/3 as predicted, R0 also fell; floor restored as a CFG-switchable parameter in v0.52 |
| v0.51 | (maintenance) | — | — |
| v0.52 | injury-based predation: ATTACK deposits damage, death at `k_health*mass` | payoff fixed → carnivory emerges | predation share of deaths rose 24%→56%; **emergence MISS**, `meatAttraction` unmoved |
| v0.53 | `k_seasonPhen` multiplies `W.seaSin`, making seasonality switchable | H1 endogenous cycles / H2 trough-limited extinction / H3 consistency | **H1 FORCED** (real result), **H2 MISS**, **H3 MISS** |
| v0.54 | Luce choice arbiter, `P(act) ∝ score^k_choiceBeta`, replacing hard argmax | H4 genes selectable / H5 monoculture breaks / H6 meat value / H7 mission test | **H4 MISS, H5 MISS, H6 MISS, H7 MISS** |
| v0.55 | invasion probe: `invadeFrac`/`invadeGenes` seed a named genotype | H8 does the carnivore peak exist / H9 concave frontier / H10 replication | **unscored** — arms at n=10–13 against a pre-registered n≥25 |

**Scored predictions to date: 1 informative result (H1), 7 MISS, 3 pending.**

## Mission metrics, every build where they were measured the same way
Matched window days 400–800, survival at day 800, censoring applied.

| build / arm | survival | GRAZE % of acts | predation share | evolved `carnivory` | evolved `meatAttraction` |
|---|---|---|---|---|---|
| v0.53 CONTROL | 71.4% | 97.03 | 61.0% | 0.072 | 0.1259 |
| v0.53 seasonless-flooroff | 68.8% | 96.05 | 25.0% | 0.058 | 0.0869 |
| v0.54 CONTROL | 66.7% | 96.33 | 54.4% | 0.061 | 0.078 |
| v0.54 meat-rich | **92.2%** | 95.90 | 64.1% | 0.070 | 0.115 |
| v0.54 beta-flooroff | 59.6% | 96.72 | 24.5% | 0.058 | 0.083 |
| v0.55 CONTROL | 83.3% | 97.53 | 62.4% | 0.157 | — |
| v0.55 invade-carn | 71.4% | 96.57 | 59.4% | 0.056 | — |

**`carnivory` has never exceeded 0.16 in any arm of any build. GRAZE has never
fallen below 93%. `meatAttraction` has never left its 0.10 founder value by more
than the neutral-gene drift yardstick.**

## Selection response, v0.54 CONTROL (n=32), in units of each gene's own SD
Neutral-gene drift yardstick **0.059 SD** (five genes the sim never reads).

| gene | Δ |
|---|---|
| biteForce | +1.14 SD |
| herbivory | +0.75 SD |
| maxSpeed | +0.32 SD |
| carnivory | +0.16 SD |
| **plantAttraction** | **+0.07 SD** |
| **meatAttraction** | **−0.16 SD** |
| **carrionAttraction** | **+0.00 SD** |
| **socialAttraction** | **−0.01 SD** |

## The cost function, from shipped constants
`k_gut` 0.020, `k_digest` 0.004, `k_mixed` 0.018, `mixedFree` 0.060,
`meatValue` 24, `carrionValue` 0.85, `tissueValue` 25, `k_meatAttrFloor` 0.5.

Diet upkeep = `k_gut*(carn²+herb²) + k_digest*max(0,carn+herb−1)² + k_mixed*max(0,carn*herb−mixedFree)`

| genotype | diet upkeep | intake per unit food mass |
|---|---|---|
| specialist carnivore (0.85, 0.15) | 0.01612 | 18.26 (perfect prey) |
| evolved herbivore (0.06, 0.70) | 0.00987 | ≤17.5 (undefended foliage) |

Carnivore pays **1.63×** the upkeep for comparable intake, and must catch its food.

## Known self-inflicted measurement errors, 34 days
arm mislabelled "baseline" when no baseline existed · `ticksPerDay` hardcoded 60
vs real 480 · absence-vs-difference in arm assignment, twice · act columns
differenced as cumulative when they are per-sample snapshots · a rule-7 identity
check that verified nothing because both runs stopped before animals existed ·
queueing arithmetic wrong twice, once producing a 110-run backlog that starved a
week · collector path bug that collected nothing for a cycle.

## Standing rules that shape the rate of work
`CLAUDE.md` hard rules 1–9: every run needs a written falsifiable prediction;
one structural change per version; constants ship as CFG patches not builds;
never compare trailing-window statistics across run lengths; never widen a gene
bound to fix a pin; build stays single-file / no build step / touch-first.
Weekly analysis cadence; daily low-token collection between passes.
