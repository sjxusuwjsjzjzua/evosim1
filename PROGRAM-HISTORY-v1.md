# Program history, engine 1.x designed runs (generated 2026-09-29)

From `ops/queue.json` and `ops/log.md`: every designed entry (standing blocks `v1-EG-base-*` left out; 176 of them, pooled persistence 1,374 of 1,944 = 70.7%, carnivore species in about 30% of worlds, meat about 18%). Earlier runs before the queue existed are summarised in `HANDOFF.md` and `MINING.md`.

## v1-BE-sizemax8  `sizeMax=8`  (scored, 1000000 ticks, seeds 1101-1112, baseline v1-BC-s1c0)

Expected: giant-grazer escapes (grazers outgrowing hunters) become rarer: fewer exits, persistence at least the baseline 9 of 12

- worlds 12, meat 15.2%, kill 10.9%, carnSp>0 in 3, preyCl 0.79, persisting (predK >= 64% of run after bootstrap) 6, exits 11, re-entries 2
- baseline v1-BC-s1c0: worlds 12, meat 19.3%, kill 15.3%, carnSp>0 in 2, preyCl 0.77, persisting (predK >= 64% of run after bootstrap) 9, exits 6, re-entries 1
    pred   baseline 10  arm  5   (+0 / -5)  McNemar p 0.062
    carn   baseline  2  arm  2   (+1 / -1)  McNemar p 1.000
    giant  baseline  0  arm  0   (+0 / -0)  McNemar p 1.000
    dwarf  baseline  0  arm  0   (+0 / -0)  McNemar p 1.000
    meat   baseline 0.193  arm 0.152   mean diff -0.041  sign test 6+/6-  p 1.000
    align  baseline 0.022  arm 0.007   mean diff -0.014  sign test 5+/7-  p 0.774
    predSp baseline 0.478  arm 0.416   mean diff -0.062  sign test 4+/8-  p 0.388

## v1-BE-mutsd12  `mutSd=0.12`  (scored, 1000000 ticks, seeds 1101-1112, baseline v1-BC-s1c0)

Expected: bigger mutation steps help a grazer line cross to hunting again: re-entries after an exit above 0 in some worlds (baseline: 0)

- worlds 12, meat 18.4%, kill 14.0%, carnSp>0 in 3, preyCl 0.87, persisting (predK >= 64% of run after bootstrap) 9, exits 12, re-entries 6
- baseline v1-BC-s1c0: worlds 12, meat 19.3%, kill 15.3%, carnSp>0 in 2, preyCl 0.77, persisting (predK >= 64% of run after bootstrap) 9, exits 6, re-entries 1
    pred   baseline 10  arm  8   (+1 / -3)  McNemar p 0.625
    carn   baseline  2  arm  3   (+1 / -0)  McNemar p 1.000
    giant  baseline  0  arm  0   (+0 / -0)  McNemar p 1.000
    dwarf  baseline  0  arm  0   (+0 / -0)  McNemar p 1.000
    meat   baseline 0.193  arm 0.184   mean diff -0.009  sign test 4+/8-  p 0.388
    align  baseline 0.022  arm 0.000   mean diff -0.022  sign test 5+/7-  p 0.774
    predSp baseline 0.478  arm 0.452   mean diff -0.026  sign test 5+/7-  p 0.774

## v1-BE-3M  `defaults`  (scored, 3000000 ticks, seeds 1201-1212, baseline -)

Expected: over 3M ticks: does any world re-evolve predators after a collapse (re-entries > 0)? Expected rare or none

- worlds 12, meat 16.1%, kill 11.7%, carnSp>0 in 1, preyCl 0.89, persisting (predK >= 64% of run after bootstrap) 6, exits 14, re-entries 7

## v1-BF-fruit1  `fruit=1`  (scored, 1000000 ticks, seeds 1101-1124, baseline v1-BF-fruit0)

Expected: fruit gene settles low but above 0; animal-carried seeds a steady share; meat share and predator persistence at least baseline

- worlds 24, meat 18.3%, kill 14.0%, carnSp>0 in 8, preyCl 0.87, persisting (predK >= 64% of run after bootstrap) 15, exits 11, re-entries 4
- baseline v1-BF-fruit0: worlds 24, meat 18.0%, kill 13.5%, carnSp>0 in 4, preyCl 0.80, persisting (predK >= 64% of run after bootstrap) 17, exits 20, re-entries 8
    pred   baseline 16  arm 14   (+4 / -6)  McNemar p 0.754
    carn   baseline  4  arm  8   (+8 / -4)  McNemar p 0.388
    giant  baseline  0  arm  1   (+1 / -0)  McNemar p 1.000
    dwarf  baseline  1  arm  1   (+1 / -1)  McNemar p 1.000
    meat   baseline 0.180  arm 0.183   mean diff +0.004  sign test 10+/14-  p 0.541
    align  baseline 0.009  arm 0.018   mean diff +0.009  sign test 11+/13-  p 0.839
    predSp baseline 0.464  arm 0.477   mean diff +0.013  sign test 12+/12-  p 1.000

## v1-BF-fruit0  `fruit=0`  (scored, 1000000 ticks, seeds 1101-1124, baseline -)

Expected: baseline for fruit on this build

- worlds 24, meat 18.0%, kill 13.5%, carnSp>0 in 4, preyCl 0.80, persisting (predK >= 64% of run after bootstrap) 17, exits 20, re-entries 8

## v1-BG-grid96  `gridN=96`  (scored, 1000000 ticks, seeds 1101-1112, baseline v1-BF-fruit0)

Expected: a bigger world holds more predators and more refuges: persistence above the 64-grid baseline, fewer exits

- worlds 12, meat 17.6%, kill 14.0%, carnSp>0 in 2, preyCl 0.78, persisting (predK >= 64% of run after bootstrap) 9, exits 7, re-entries 2
- baseline v1-BF-fruit0: worlds 24, meat 18.0%, kill 13.5%, carnSp>0 in 4, preyCl 0.80, persisting (predK >= 64% of run after bootstrap) 17, exits 20, re-entries 8
    pred   baseline  7  arm  7   (+3 / -3)  McNemar p 1.000
    carn   baseline  2  arm  2   (+2 / -2)  McNemar p 1.000
    giant  baseline  0  arm  0   (+0 / -0)  McNemar p 1.000
    dwarf  baseline  0  arm  0   (+0 / -0)  McNemar p 1.000
    meat   baseline 0.158  arm 0.176   mean diff +0.018  sign test 7+/5-  p 0.774
    align  baseline -0.001  arm 0.048   mean diff +0.049  sign test 9+/3-  p 0.146
    predSp baseline 0.446  arm 0.554   mean diff +0.107  sign test 7+/5-  p 0.774

## v1-BH-mutsd12b  `mutSd=0.12`  (scored, 1000000 ticks, seeds 1113-1124, baseline v1-EG-base-1113)

Expected: replicates v1-BE-mutsd12: more re-entries and more exits than baseline, persistence unchanged

- worlds 12, meat 17.6%, kill 13.2%, carnSp>0 in 1, preyCl 0.77, persisting (predK >= 64% of run after bootstrap) 7, exits 8, re-entries 1
- baseline v1-EG-base-1113: worlds 12, meat 15.3%, kill 11.1%, carnSp>0 in 2, preyCl 0.82, persisting (predK >= 64% of run after bootstrap) 6, exits 11, re-entries 4
    pred   baseline  6  arm  7   (+4 / -3)  McNemar p 1.000
    carn   baseline  2  arm  1   (+1 / -2)  McNemar p 1.000
    giant  baseline  0  arm  0   (+0 / -0)  McNemar p 1.000
    dwarf  baseline  0  arm  0   (+0 / -0)  McNemar p 1.000
    meat   baseline 0.153  arm 0.176   mean diff +0.024  sign test 7+/5-  p 0.774
    align  baseline 0.005  arm 0.014   mean diff +0.009  sign test 8+/4-  p 0.388
    predSp baseline 0.416  arm 0.483   mean diff +0.067  sign test 8+/4-  p 0.388

## v1-BH-mutsd16  `mutSd=0.16`  (scored, 1000000 ticks, seeds 1101-1112, baseline v1-BC-s1c0)

Expected: dose: still more turnover (re-entries and exits) than 0.12; persistence may fall

- worlds 12, meat 13.4%, kill 8.5%, carnSp>0 in 1, preyCl 0.81, persisting (predK >= 64% of run after bootstrap) 5, exits 9, re-entries 2
- baseline v1-BC-s1c0: worlds 12, meat 19.3%, kill 15.3%, carnSp>0 in 2, preyCl 0.77, persisting (predK >= 64% of run after bootstrap) 9, exits 6, re-entries 1
    pred   baseline 10  arm  4   (+2 / -8)  McNemar p 0.109
    carn   baseline  2  arm  1   (+1 / -2)  McNemar p 1.000
    giant  baseline  0  arm  0   (+0 / -0)  McNemar p 1.000
    dwarf  baseline  0  arm  0   (+0 / -0)  McNemar p 1.000
    meat   baseline 0.193  arm 0.134   mean diff -0.059  sign test 4+/8-  p 0.388
    align  baseline 0.022  arm -0.007   mean diff -0.028  sign test 3+/9-  p 0.146
    predSp baseline 0.478  arm 0.392   mean diff -0.086  sign test 5+/7-  p 0.774

## v1-BI-3Mb  `defaults`  (scored, 3000000 ticks, seeds 1213-1224, baseline -)

Expected: default build over 3M ticks: exits and re-entries both several per 12 worlds (v1-BE-3M: 14 and 7); species turnover

- worlds 12, meat 10.3%, kill 5.5%, carnSp>0 in 1, preyCl 0.80, persisting (predK >= 64% of run after bootstrap) 2, exits 14, re-entries 5

## v1-BJ-fjc  `fruit=1,jc=0.8`  (scored, 400000 ticks, seeds 1101-1112, baseline v1-BJ-fjcnd)

Expected: fruit gene holds or rises (up in most worlds); carried seed a large share; plant diversity up

- worlds 12, meat 24.7%, kill 20.0%, carnSp>0 in 6, preyCl 0.91
- fruit: gene 0.197 -> 0.130 (up in 0 of 12), div 0.157, fruit 28.8%, carried 10.0%
- baseline v1-BJ-fjcnd: worlds 12, meat 27.3%, kill 22.3%, carnSp>0 in 5, preyCl 1.01
    pred   baseline 10  arm 10   (+2 / -2)  McNemar p 1.000
    carn   baseline  5  arm  6   (+3 / -2)  McNemar p 1.000
    giant  baseline  0  arm  0   (+0 / -0)  McNemar p 1.000
    dwarf  baseline  0  arm  0   (+0 / -0)  McNemar p 1.000
    meat   baseline 0.273  arm 0.247   mean diff -0.026  sign test 8+/4-  p 0.388
    align  baseline -0.004  arm 0.007   mean diff +0.011  sign test 8+/4-  p 0.388
    predSp baseline 0.506  arm 0.569   mean diff +0.062  sign test 9+/3-  p 0.146

## v1-BJ-fjcnd  `fruit=1,jc=0.8,gutTicks=0`  (scored, 400000 ticks, seeds 1101-1112, baseline -)

Expected: no carrying: fruit gene falls

- worlds 12, meat 27.3%, kill 22.3%, carnSp>0 in 5, preyCl 1.01
- fruit: gene 0.182 -> 0.085 (up in 0 of 12), div 0.147, fruit 20.1%, carried 0.0%

## v1-BJ-f  `fruit=1`  (scored, 400000 ticks, seeds 1101-1112, baseline v1-BJ-fjcnd)

Expected: fruit without jc: gene falls as before

- worlds 12, meat 26.2%, kill 21.4%, carnSp>0 in 6, preyCl 0.91
- fruit: gene 0.200 -> 0.130 (up in 0 of 12), div 0.157, fruit 28.7%, carried 10.7%
- baseline v1-BJ-fjcnd: worlds 12, meat 27.3%, kill 22.3%, carnSp>0 in 5, preyCl 1.01
    pred   baseline 10  arm 10   (+1 / -1)  McNemar p 1.000
    carn   baseline  5  arm  6   (+3 / -2)  McNemar p 1.000
    giant  baseline  0  arm  0   (+0 / -0)  McNemar p 1.000
    dwarf  baseline  0  arm  0   (+0 / -0)  McNemar p 1.000
    meat   baseline 0.273  arm 0.262   mean diff -0.010  sign test 5+/7-  p 0.774
    align  baseline -0.004  arm -0.004   mean diff -0.000  sign test 4+/8-  p 0.388
    predSp baseline 0.506  arm 0.583   mean diff +0.077  sign test 9+/3-  p 0.146

## v1-BJ-jc  `jc=0.8`  (scored, 400000 ticks, seeds 1101-1112, baseline v1-BJ-base)

Expected: jc alone: plant diversity up; animal effects small

- worlds 12, meat 17.7%, kill 12.8%, carnSp>0 in 4, preyCl 0.86
- baseline v1-BJ-base: worlds 12, meat 22.6%, kill 17.6%, carnSp>0 in 3, preyCl 0.96
    pred   baseline  9  arm  5   (+2 / -6)  McNemar p 0.289
    carn   baseline  3  arm  4   (+4 / -3)  McNemar p 1.000
    giant  baseline  1  arm  0   (+0 / -1)  McNemar p 1.000
    dwarf  baseline  0  arm  0   (+0 / -0)  McNemar p 1.000
    meat   baseline 0.226  arm 0.177   mean diff -0.049  sign test 5+/7-  p 0.774
    align  baseline -0.009  arm 0.007   mean diff +0.016  sign test 8+/4-  p 0.388
    predSp baseline 0.439  arm 0.416   mean diff -0.023  sign test 5+/7-  p 0.774

## v1-BJ-base  `defaults`  (scored, 400000 ticks, seeds 1101-1112, baseline -)

Expected: baseline for the fruit and jc arms on this build

- worlds 12, meat 22.6%, kill 17.6%, carnSp>0 in 3, preyCl 0.96

## v1-BK-fjc02  `fruit=1,jc=0.8,fruitPerSeed=0.2`  (scored, 400000 ticks, seeds 1101-1124, baseline v1-BK-fjcnd02)

Expected: with 2.5x the seeds per fruit, carrying pays: fruit gene higher than without carrying in most pairs and holding or rising

- worlds 24, meat 26.7%, kill 22.1%, carnSp>0 in 12, preyCl 0.94
- fruit: gene 0.200 -> 0.148 (up in 3 of 24), div 0.157, fruit 28.2%, carried 17.0%
- baseline v1-BK-fjcnd02: worlds 24, meat 26.6%, kill 21.6%, carnSp>0 in 10, preyCl 1.01
    pred   baseline 20  arm 23   (+4 / -1)  McNemar p 0.375
    carn   baseline 10  arm 12   (+8 / -6)  McNemar p 0.791
    giant  baseline  0  arm  0   (+0 / -0)  McNemar p 1.000
    dwarf  baseline  0  arm  0   (+0 / -0)  McNemar p 1.000
    meat   baseline 0.266  arm 0.267   mean diff +0.001  sign test 12+/12-  p 1.000
    align  baseline -0.008  arm -0.003   mean diff +0.005  sign test 15+/9-  p 0.307
    predSp baseline 0.518  arm 0.501   mean diff -0.016  sign test 10+/14-  p 0.541

## v1-BK-fjcnd02  `fruit=1,jc=0.8,fruitPerSeed=0.2,gutTicks=0`  (scored, 400000 ticks, seeds 1101-1124, baseline -)

Expected: no carrying: fruit gene falls

- worlds 24, meat 26.6%, kill 21.6%, carnSp>0 in 10, preyCl 1.01
- fruit: gene 0.184 -> 0.087 (up in 0 of 24), div 0.146, fruit 21.1%, carried 0.0%

## v1-BL-fc  `fruit=1,fruitPerSeed=0.2`  (scored, 1000000 ticks, seeds 1101-1124, baseline v1-BL-fnc)

Expected: carrying without jc: fruit gene above no-carrying at 1M, settling or rising

- worlds 24, meat 20.8%, kill 16.2%, carnSp>0 in 3, preyCl 0.86, persisting (predK >= 64% of run after bootstrap) 19, exits 13, re-entries 3
- fruit: gene 0.194 -> 0.250 (up in 11 of 24), div 0.181, fruit 28.9%, carried 29.8%
- baseline v1-BL-fnc: worlds 24, meat 18.8%, kill 14.4%, carnSp>0 in 5, preyCl 0.83, persisting (predK >= 64% of run after bootstrap) 15, exits 10, re-entries 5
    pred   baseline 13  arm 20   (+11 / -4)  McNemar p 0.118
    carn   baseline  5  arm  3   (+2 / -4)  McNemar p 0.688
    giant  baseline  0  arm  0   (+0 / -0)  McNemar p 1.000
    dwarf  baseline  0  arm  1   (+1 / -0)  McNemar p 1.000
    meat   baseline 0.188  arm 0.208   mean diff +0.020  sign test 14+/10-  p 0.541
    align  baseline 0.013  arm 0.013   mean diff +0.000  sign test 12+/12-  p 1.000
    predSp baseline 0.484  arm 0.530   mean diff +0.046  sign test 12+/12-  p 1.000

## v1-BL-fnc  `fruit=1,fruitPerSeed=0.2,gutTicks=0`  (scored, 1000000 ticks, seeds 1101-1124, baseline -)

Expected: no carrying, no jc: fruit gene falls

- worlds 24, meat 18.8%, kill 14.4%, carnSp>0 in 5, preyCl 0.83, persisting (predK >= 64% of run after bootstrap) 15, exits 10, re-entries 5
- fruit: gene 0.184 -> 0.075 (up in 0 of 24), div 0.160, fruit 17.1%, carried 0.0%

## v1-BL-fjc  `fruit=1,jc=0.8,fruitPerSeed=0.2`  (scored, 1000000 ticks, seeds 1101-1124, baseline v1-BL-fjnc)

Expected: carrying with jc: as without jc (jc did not matter at 400k)

- worlds 24, meat 20.4%, kill 16.3%, carnSp>0 in 5, preyCl 0.85, persisting (predK >= 64% of run after bootstrap) 19, exits 12, re-entries 8
- fruit: gene 0.200 -> 0.348 (up in 17 of 24), div 0.203, fruit 31.8%, carried 37.5%
- baseline v1-BL-fjnc: worlds 24, meat 21.2%, kill 17.0%, carnSp>0 in 6, preyCl 0.84, persisting (predK >= 64% of run after bootstrap) 19, exits 9, re-entries 3
    pred   baseline 17  arm 16   (+3 / -4)  McNemar p 1.000
    carn   baseline  6  arm  5   (+4 / -5)  McNemar p 1.000
    giant  baseline  0  arm  0   (+0 / -0)  McNemar p 1.000
    dwarf  baseline  0  arm  0   (+0 / -0)  McNemar p 1.000
    meat   baseline 0.212  arm 0.204   mean diff -0.008  sign test 11+/13-  p 0.839
    align  baseline 0.010  arm 0.008   mean diff -0.002  sign test 8+/16-  p 0.152
    predSp baseline 0.517  arm 0.495   mean diff -0.022  sign test 13+/11-  p 0.839

## v1-BL-fjnc  `fruit=1,jc=0.8,fruitPerSeed=0.2,gutTicks=0`  (scored, 1000000 ticks, seeds 1101-1124, baseline -)

Expected: no carrying, jc: fruit gene falls

- worlds 24, meat 21.2%, kill 17.0%, carnSp>0 in 6, preyCl 0.84, persisting (predK >= 64% of run after bootstrap) 19, exits 9, re-entries 3
- fruit: gene 0.184 -> 0.070 (up in 0 of 24), div 0.156, fruit 15.2%, carried 0.0%

## v1-BM-fruit3M  `fruit=1,fruitPerSeed=0.2`  (scored, 3000000 ticks, seeds 1201-1212, baseline -)

Expected: over 3M ticks with carrying the fruit gene levels off above 0 or climbs; carried seed a steady share

- worlds 12, meat 13.3%, kill 9.4%, carnSp>0 in 2, preyCl 0.83, persisting (predK >= 64% of run after bootstrap) 7, exits 18, re-entries 12
- fruit: gene 0.196 -> 0.680 (up in 11 of 12), div 0.198, fruit 34.7%, carried 69.5%

## v1-BN-default  `defaults`  (scored, 1000000 ticks, seeds 1125-1148, baseline -)

Expected: the fruit build's default at 1M: persistence about 2/3 or better; fruit gene rising

- worlds 24, meat 17.8%, kill 13.7%, carnSp>0 in 5, preyCl 0.85, persisting (predK >= 64% of run after bootstrap) 17, exits 19, re-entries 14

## v1-BN-jc  `jc=0.8`  (scored, 1000000 ticks, seeds 1125-1148, baseline v1-BN-default)

Expected: jc raises the fruit gene and plant diversity (replicating +0.10 and +0.02); predators unchanged

- worlds 24, meat 20.6%, kill 16.4%, carnSp>0 in 3, preyCl 0.85, persisting (predK >= 64% of run after bootstrap) 19, exits 11, re-entries 6
- baseline v1-BN-default: worlds 24, meat 17.8%, kill 13.7%, carnSp>0 in 5, preyCl 0.85, persisting (predK >= 64% of run after bootstrap) 17, exits 19, re-entries 14
    pred   baseline 13  arm 18   (+8 / -3)  McNemar p 0.227
    carn   baseline  5  arm  3   (+3 / -5)  McNemar p 0.727
    giant  baseline  0  arm  0   (+0 / -0)  McNemar p 1.000
    dwarf  baseline  2  arm  0   (+0 / -2)  McNemar p 0.500
    meat   baseline 0.178  arm 0.206   mean diff +0.027  sign test 15+/9-  p 0.307
    align  baseline 0.009  arm 0.017   mean diff +0.008  sign test 13+/11-  p 0.839
    predSp baseline 0.467  arm 0.510   mean diff +0.044  sign test 15+/9-  p 0.307

## v1-BO-see1  `seeFruit=1`  (scored, 1000000 ticks, seeds 1101-1124, baseline v1-BO-see0)

Expected: grazers turn toward fruit; fruit share of energy up; fruit gene higher; predators unchanged

- worlds 24, meat 21.4%, kill 17.1%, carnSp>0 in 9, preyCl 0.89, persisting (predK >= 64% of run after bootstrap) 20, exits 13, re-entries 5
- fruit: gene 0.195 -> 0.308 (up in 12 of 24), div 0.176, fruit 26.5%, carried 34.5%
- baseline v1-BO-see0: worlds 24, meat 16.3%, kill 12.3%, carnSp>0 in 4, preyCl 0.86, persisting (predK >= 64% of run after bootstrap) 19, exits 12, re-entries 9
    pred   baseline 14  arm 19   (+9 / -4)  McNemar p 0.267
    carn   baseline  4  arm  9   (+7 / -2)  McNemar p 0.180
    giant  baseline  0  arm  0   (+0 / -0)  McNemar p 1.000
    dwarf  baseline  0  arm  3   (+3 / -0)  McNemar p 0.250
    meat   baseline 0.163  arm 0.214   mean diff +0.051  sign test 17+/7-  p 0.064
    align  baseline 0.008  arm 0.010   mean diff +0.003  sign test 16+/8-  p 0.152
    predSp baseline 0.437  arm 0.511   mean diff +0.074  sign test 14+/10-  p 0.541

## v1-BO-see0  `seeFruit=0`  (scored, 1000000 ticks, seeds 1101-1124, baseline -)

Expected: baseline on the fruit-sense build

- worlds 24, meat 16.3%, kill 12.3%, carnSp>0 in 4, preyCl 0.86, persisting (predK >= 64% of run after bootstrap) 19, exits 12, re-entries 9
- fruit: gene 0.199 -> 0.436 (up in 21 of 24), div 0.210, fruit 27.3%, carried 46.9%

## v1-BP-3Mdefault  `defaults`  (scored, 3000000 ticks, seeds 1213-1224, baseline -)

Expected: current default (fruit, fruit senses) over 3M ticks: fruit gene climbs as in v1-BM-fruit3M; predator comebacks; grazers turn toward fruit late

- worlds 12, meat 14.3%, kill 10.5%, carnSp>0 in 1, preyCl 0.85, persisting (predK >= 64% of run after bootstrap) 8, exits 15, re-entries 12
- fruit: gene 0.199 -> 0.712 (up in 12 of 12), div 0.200, fruit 35.2%, carried 72.4%

## v1-NU-base  `defaults`  (scored, 1000000 ticks, seeds 1301-1324, baseline -)

Expected: nutrient loop at 1M, 24 paired seeds. Expect: with it on, plant mass and animals 20-40% lower, soilCV above 0.5 throughout (dung and carcass patches), meat share a few points lower; predator persistence within 4 worlds of base either way (no strong prior). Rich soil (soil0 12) sits between.

- worlds 24, meat 19.2%, kill 14.8%, carnSp>0 in 5, preyCl 0.83, persisting (predK >= 64% of run after bootstrap) 17, exits 12, re-entries 4
- fruit: gene 0.193 -> 0.356 (up in 17 of 24), div 0.187, fruit 28.9%, carried 40.7%

## v1-NU-on  `nutrients=1`  (scored, 1000000 ticks, seeds 1301-1324, baseline v1-NU-base)

Expected: nutrient loop at 1M, 24 paired seeds. Expect: with it on, plant mass and animals 20-40% lower, soilCV above 0.5 throughout (dung and carcass patches), meat share a few points lower; predator persistence within 4 worlds of base either way (no strong prior). Rich soil (soil0 12) sits between.

- worlds 24, meat 10.9%, kill 7.0%, carnSp>0 in 1, preyCl 0.69, persisting (predK >= 64% of run after bootstrap) 8, exits 23, re-entries 5
- fruit: gene 0.150 -> 0.425 (up in 24 of 24), div 0.264, fruit 33.3%, carried 58.6%
- baseline v1-NU-base: worlds 24, meat 19.2%, kill 14.8%, carnSp>0 in 5, preyCl 0.83, persisting (predK >= 64% of run after bootstrap) 17, exits 12, re-entries 4
    pred   baseline 19  arm  7   (+0 / -12)  McNemar p 0.000
    carn   baseline  5  arm  1   (+1 / -5)  McNemar p 0.219
    giant  baseline  0  arm  0   (+0 / -0)  McNemar p 1.000
    dwarf  baseline  1  arm  1   (+1 / -1)  McNemar p 1.000
    meat   baseline 0.192  arm 0.109   mean diff -0.083  sign test 8+/16-  p 0.152
    kill   baseline 0.148  arm 0.070   mean diff -0.078  sign test 8+/16-  p 0.152
    animals baseline 1006  arm 796   mean diff -210.944  sign test 1+/23-  p 0.000
    align  baseline 0.010  arm -0.007   mean diff -0.017  sign test 5+/19-  p 0.007
    predSp baseline 0.500  arm 0.442   mean diff -0.058  sign test 9+/15-  p 0.307

## v1-NU-rich  `nutrients=1,soil0=12`  (scored, 1000000 ticks, seeds 1301-1324, baseline v1-NU-base)

Expected: nutrient loop at 1M, 24 paired seeds. Expect: with it on, plant mass and animals 20-40% lower, soilCV above 0.5 throughout (dung and carcass patches), meat share a few points lower; predator persistence within 4 worlds of base either way (no strong prior). Rich soil (soil0 12) sits between.

- worlds 24, meat 16.4%, kill 11.9%, carnSp>0 in 4, preyCl 0.76, persisting (predK >= 64% of run after bootstrap) 14, exits 15, re-entries 4
- fruit: gene 0.184 -> 0.331 (up in 16 of 24), div 0.215, fruit 31.3%, carried 44.4%
- baseline v1-NU-base: worlds 24, meat 19.2%, kill 14.8%, carnSp>0 in 5, preyCl 0.83, persisting (predK >= 64% of run after bootstrap) 17, exits 12, re-entries 4
    pred   baseline 19  arm 11   (+4 / -12)  McNemar p 0.077
    carn   baseline  5  arm  4   (+4 / -5)  McNemar p 1.000
    giant  baseline  0  arm  0   (+0 / -0)  McNemar p 1.000
    dwarf  baseline  1  arm  0   (+0 / -1)  McNemar p 1.000
    meat   baseline 0.192  arm 0.164   mean diff -0.028  sign test 12+/12-  p 1.000
    kill   baseline 0.148  arm 0.119   mean diff -0.029  sign test 12+/12-  p 1.000
    animals baseline 1006  arm 915   mean diff -91.141  sign test 6+/18-  p 0.023
    align  baseline 0.010  arm 0.008   mean diff -0.002  sign test 12+/12-  p 1.000
    predSp baseline 0.500  arm 0.489   mean diff -0.011  sign test 13+/11-  p 0.839

## v1-SM-base  `defaults`  (scored, 1000000 ticks, seeds 1325-1348, baseline -)

Expected: baseline for v1-SM-on (the NI 50 build)

- worlds 24, meat 19.4%, kill 15.4%, carnSp>0 in 5, preyCl 0.86, persisting (predK >= 64% of run after bootstrap) 18, exits 11, re-entries 4
- fruit: gene 0.194 -> 0.310 (up in 13 of 24), div 0.184, fruit 26.5%, carried 34.4%

## v1-SM-on  `smell=1`  (scored, 1000000 ticks, seeds 1325-1348, baseline v1-SM-base)

Expected: smell at 1M, 24 paired seeds. Expect: kill share and meat share up a few points (carrion and prey scent lead hunters to food), prey clumping up if prey use scent to keep together or to avoid hunters, predator persistence at least as often as base. A null here means smell is not worth its 8 inputs.

- worlds 24, meat 19.1%, kill 14.6%, carnSp>0 in 2, preyCl 0.93, persisting (predK >= 64% of run after bootstrap) 19, exits 13, re-entries 2
- fruit: gene 0.193 -> 0.242 (up in 10 of 24), div 0.180, fruit 25.1%, carried 32.0%
- baseline v1-SM-base: worlds 24, meat 19.4%, kill 15.4%, carnSp>0 in 5, preyCl 0.86, persisting (predK >= 64% of run after bootstrap) 18, exits 11, re-entries 4
    pred   baseline 16  arm 19   (+7 / -4)  McNemar p 0.549
    carn   baseline  5  arm  2   (+1 / -4)  McNemar p 0.375
    giant  baseline  0  arm  0   (+0 / -0)  McNemar p 1.000
    dwarf  baseline  1  arm  1   (+1 / -1)  McNemar p 1.000
    meat   baseline 0.194  arm 0.191   mean diff -0.003  sign test 13+/11-  p 0.839
    kill   baseline 0.154  arm 0.146   mean diff -0.008  sign test 12+/12-  p 1.000
    animals baseline 1023  arm 1089   mean diff +65.722  sign test 15+/9-  p 0.307
    align  baseline 0.007  arm 0.069   mean diff +0.063  sign test 21+/3-  p 0.000
    predSp baseline 0.481  arm 0.620   mean diff +0.139  sign test 17+/7-  p 0.064

## v1-LE-base  `defaults`  (scored, 1000000 ticks, seeds 1361-1384, baseline -)

Expected: baseline for v1-LE-on (the NI 51 / NO 10 build, learning off)

- worlds 24, meat 18.0%, kill 13.6%, carnSp>0 in 7, preyCl 0.89, persisting (predK >= 64% of run after bootstrap) 17, exits 16, re-entries 8
- fruit: gene 0.192 -> 0.327 (up in 15 of 24), div 0.193, fruit 24.0%, carried 38.1%

## v1-LE-on  `learn=1`  (scored, 1000000 ticks, seeds 1361-1384, baseline v1-LE-base)

Expected: lifetime learning at 1M, 24 paired seeds. Expect: learnM above the base arm's drift of the same (unused) output if selection favours learning; weights of adults moved from their genome (learnMoved over 0.1); behaviour: kill share and meat share up a few points (hunters improve with practice), bootstrap somewhat slower; predator persistence within 4 worlds of base. A learnM at or below drift means evolution switches learning off.

- worlds 24, meat 18.1%, kill 14.9%, carnSp>0 in 3, preyCl 1.08, persisting (predK >= 64% of run after bootstrap) 19, exits 8, re-entries 7
- fruit: gene 0.186 -> 0.371 (up in 18 of 24), div 0.202, fruit 15.2%, carried 38.3%
- baseline v1-LE-base: worlds 24, meat 18.0%, kill 13.6%, carnSp>0 in 7, preyCl 0.89, persisting (predK >= 64% of run after bootstrap) 17, exits 16, re-entries 8
    pred   baseline 16  arm 18   (+7 / -5)  McNemar p 0.774
    carn   baseline  7  arm  3   (+2 / -6)  McNemar p 0.289
    giant  baseline  2  arm  0   (+0 / -2)  McNemar p 0.500
    dwarf  baseline  2  arm  1   (+1 / -2)  McNemar p 1.000
    meat   baseline 0.180  arm 0.181   mean diff +0.000  sign test 13+/11-  p 0.839
    kill   baseline 0.136  arm 0.149   mean diff +0.013  sign test 13+/11-  p 0.839
    animals baseline 1007  arm 818   mean diff -188.934  sign test 5+/19-  p 0.007
    align  baseline 0.004  arm 0.017   mean diff +0.013  sign test 11+/13-  p 0.839
    predSp baseline 0.481  arm 0.292   mean diff -0.190  sign test 1+/23-  p 0.000

## v1-NU-s24  `nutrients=1,soil0=24`  (scored, 1000000 ticks, seeds 1361-1384, baseline v1-LE-base)

Expected: nutrient loop with abundant nutrient, 24 seeds paired with v1-LE-base (same build and defaults). At soil0 6 predator worlds fell 19 -> 7 because 78% of the nutrient idles in the soil and plant mass drops to a third. Expect: soil0 24 predator worlds within 3 of base and plant mass within 25%; soil0 48 same as base; soilCV above 0.5 in both (dung and carcass patches still form).

- worlds 24, meat 17.2%, kill 13.2%, carnSp>0 in 4, preyCl 0.78, persisting (predK >= 64% of run after bootstrap) 16, exits 18, re-entries 6
- fruit: gene 0.192 -> 0.304 (up in 17 of 24), div 0.200, fruit 27.4%, carried 37.7%
- baseline v1-LE-base: worlds 24, meat 18.0%, kill 13.6%, carnSp>0 in 7, preyCl 0.89, persisting (predK >= 64% of run after bootstrap) 17, exits 16, re-entries 8
    pred   baseline 16  arm 15   (+7 / -8)  McNemar p 1.000
    carn   baseline  7  arm  4   (+2 / -5)  McNemar p 0.453
    giant  baseline  2  arm  0   (+0 / -2)  McNemar p 0.500
    dwarf  baseline  2  arm  1   (+1 / -2)  McNemar p 1.000
    meat   baseline 0.180  arm 0.172   mean diff -0.008  sign test 13+/11-  p 0.839
    kill   baseline 0.136  arm 0.132   mean diff -0.005  sign test 12+/12-  p 1.000
    animals baseline 1007  arm 914   mean diff -93.463  sign test 7+/17-  p 0.064
    align  baseline 0.004  arm 0.016   mean diff +0.012  sign test 17+/7-  p 0.064
    predSp baseline 0.481  arm 0.492   mean diff +0.010  sign test 11+/13-  p 0.839

## v1-NU-s48  `nutrients=1,soil0=48`  (scored, 1000000 ticks, seeds 1361-1384, baseline v1-LE-base)

Expected: nutrient loop with abundant nutrient, 24 seeds paired with v1-LE-base (same build and defaults). At soil0 6 predator worlds fell 19 -> 7 because 78% of the nutrient idles in the soil and plant mass drops to a third. Expect: soil0 24 predator worlds within 3 of base and plant mass within 25%; soil0 48 same as base; soilCV above 0.5 in both (dung and carcass patches still form).

- worlds 24, meat 16.6%, kill 12.3%, carnSp>0 in 6, preyCl 0.86, persisting (predK >= 64% of run after bootstrap) 14, exits 16, re-entries 8
- fruit: gene 0.197 -> 0.325 (up in 16 of 24), div 0.210, fruit 24.6%, carried 40.8%
- baseline v1-LE-base: worlds 24, meat 18.0%, kill 13.6%, carnSp>0 in 7, preyCl 0.89, persisting (predK >= 64% of run after bootstrap) 17, exits 16, re-entries 8
    pred   baseline 16  arm 12   (+5 / -9)  McNemar p 0.424
    carn   baseline  7  arm  6   (+5 / -6)  McNemar p 1.000
    giant  baseline  2  arm  0   (+0 / -2)  McNemar p 0.500
    dwarf  baseline  2  arm  0   (+0 / -2)  McNemar p 0.500
    meat   baseline 0.180  arm 0.166   mean diff -0.015  sign test 11+/13-  p 0.839
    kill   baseline 0.136  arm 0.123   mean diff -0.013  sign test 10+/14-  p 0.541
    animals baseline 1007  arm 1026   mean diff +18.404  sign test 12+/12-  p 1.000
    align  baseline 0.004  arm 0.014   mean diff +0.010  sign test 13+/11-  p 0.839
    predSp baseline 0.481  arm 0.443   mean diff -0.038  sign test 10+/14-  p 0.541

## v1-NU24-1457  `nutrients=1,soil0=24`  (scored, 1000000 ticks, seeds 1457-1468, baseline v1-EG-base-1457)

Expected: nutrient loop at soil0 24 on the smell default, paired with the standing block of the same seeds (same build). Expect as v1-NU-s24 against v1-LE-base: predator worlds within 3 of the block, plant mass within 25%, soilCV above 0.5. If so, the loop goes on by default at soil0 24.

- worlds 12, meat 17.3%, kill 12.7%, carnSp>0 in 2, preyCl 0.76, persisting (predK >= 64% of run after bootstrap) 6, exits 9, re-entries 4
- fruit: gene 0.193 -> 0.308 (up in 7 of 12), div 0.208, fruit 24.7%, carried 40.3%
- baseline v1-EG-base-1457: worlds 12, meat 19.7%, kill 14.9%, carnSp>0 in 6, preyCl 0.89, persisting (predK >= 64% of run after bootstrap) 8, exits 9, re-entries 4
    pred   baseline  8  arm  8   (+2 / -2)  McNemar p 1.000
    carn   baseline  6  arm  2   (+0 / -4)  McNemar p 0.125
    giant  baseline  0  arm  0   (+0 / -0)  McNemar p 1.000
    dwarf  baseline  0  arm  0   (+0 / -0)  McNemar p 1.000
    meat   baseline 0.197  arm 0.173   mean diff -0.023  sign test 3+/9-  p 0.146
    kill   baseline 0.149  arm 0.127   mean diff -0.022  sign test 4+/8-  p 0.388
    animals baseline 1006  arm 924   mean diff -81.569  sign test 3+/9-  p 0.146
    align  baseline 0.042  arm 0.058   mean diff +0.016  sign test 9+/3-  p 0.146
    predSp baseline 0.467  arm 0.512   mean diff +0.044  sign test 8+/4-  p 0.388

## v1-NU24-1469  `nutrients=1,soil0=24`  (scored, 1000000 ticks, seeds 1469-1480, baseline v1-EG-base-1469)

Expected: nutrient loop at soil0 24 on the smell default, paired with the standing block of the same seeds (same build). Expect as v1-NU-s24 against v1-LE-base: predator worlds within 3 of the block, plant mass within 25%, soilCV above 0.5. If so, the loop goes on by default at soil0 24.

- worlds 12, meat 14.3%, kill 9.4%, carnSp>0 in 1, preyCl 0.76, persisting (predK >= 64% of run after bootstrap) 5, exits 11, re-entries 5
- fruit: gene 0.190 -> 0.370 (up in 9 of 12), div 0.230, fruit 27.5%, carried 49.0%
- baseline v1-EG-base-1469: worlds 12, meat 17.4%, kill 13.1%, carnSp>0 in 6, preyCl 0.89, persisting (predK >= 64% of run after bootstrap) 11, exits 5, re-entries 1
    pred   baseline 12  arm  7   (+0 / -5)  McNemar p 0.062
    carn   baseline  6  arm  1   (+0 / -5)  McNemar p 0.062
    giant  baseline  0  arm  0   (+0 / -0)  McNemar p 1.000
    dwarf  baseline  0  arm  1   (+1 / -0)  McNemar p 1.000
    meat   baseline 0.174  arm 0.143   mean diff -0.030  sign test 4+/8-  p 0.388
    kill   baseline 0.131  arm 0.094   mean diff -0.037  sign test 2+/10-  p 0.039
    animals baseline 985  arm 926   mean diff -59.327  sign test 3+/9-  p 0.146
    align  baseline 0.072  arm 0.027   mean diff -0.045  sign test 4+/8-  p 0.388
    predSp baseline 0.551  arm 0.514   mean diff -0.037  sign test 5+/7-  p 0.774

## v1-SM-3M  `defaults`  (scored, 3000000 ticks, seeds 1613-1624, baseline -)

Expected: the smell default over 3M ticks. Expect: alignment keeps rising past 1M (above 0.08 in the last third), predators come and go as in v1-BP-3Mdefault (persisting in about 8 of 12), fruit gene near 0.7.

- worlds 12, meat 14.5%, kill 10.1%, carnSp>0 in 4, preyCl 0.86, persisting (predK >= 64% of run after bootstrap) 7, exits 22, re-entries 18
- fruit: gene 0.195 -> 0.558 (up in 12 of 12), div 0.220, fruit 28.5%, carried 59.4%

## v1-SD02-1649  `smellDecay=0.02`  (scored, 1000000 ticks, seeds 1649-1660, baseline v1-EG-base-1649)

Expected: scent that lasts longer (smellDecay 0.02, about 50 ticks, against 0.05), paired with the standing block of the same seeds. Expect: grazers steer off older trails, so alignment rises (above the block's in 8 of 12) and prey spread further; predators within 2 of the block. If alignment falls, fresh scent carries the information and old trails are noise.

- worlds 12, meat 20.4%, kill 16.1%, carnSp>0 in 3, preyCl 0.90, persisting (predK >= 64% of run after bootstrap) 11, exits 5, re-entries 1
- fruit: gene 0.196 -> 0.210 (up in 6 of 12), div 0.181, fruit 18.1%, carried 25.0%
- baseline v1-EG-base-1649: worlds 12, meat 17.9%, kill 12.7%, carnSp>0 in 6, preyCl 0.91, persisting (predK >= 64% of run after bootstrap) 10, exits 7, re-entries 2
    pred   baseline  8  arm 10   (+3 / -1)  McNemar p 0.625
    carn   baseline  6  arm  3   (+0 / -3)  McNemar p 0.250
    giant  baseline  0  arm  0   (+0 / -0)  McNemar p 1.000
    dwarf  baseline  0  arm  0   (+0 / -0)  McNemar p 1.000
    meat   baseline 0.179  arm 0.204   mean diff +0.025  sign test 6+/6-  p 1.000
    kill   baseline 0.127  arm 0.161   mean diff +0.034  sign test 5+/7-  p 0.774
    animals baseline 1000  arm 969   mean diff -30.579  sign test 6+/6-  p 1.000
    align  baseline 0.053  arm 0.031   mean diff -0.021  sign test 5+/7-  p 0.774
    predSp baseline 0.499  arm 0.524   mean diff +0.025  sign test 6+/6-  p 1.000

## v1-SD02-1661  `smellDecay=0.02`  (scored, 1000000 ticks, seeds 1661-1672, baseline v1-EG-base-1661)

Expected: scent that lasts longer (smellDecay 0.02, about 50 ticks, against 0.05), paired with the standing block of the same seeds. Expect: grazers steer off older trails, so alignment rises (above the block's in 8 of 12) and prey spread further; predators within 2 of the block. If alignment falls, fresh scent carries the information and old trails are noise.

- worlds 12, meat 20.8%, kill 16.2%, carnSp>0 in 5, preyCl 0.91, persisting (predK >= 64% of run after bootstrap) 12, exits 3, re-entries 1
- fruit: gene 0.193 -> 0.196 (up in 4 of 12), div 0.172, fruit 24.8%, carried 25.1%
- baseline v1-EG-base-1661: worlds 12, meat 21.6%, kill 16.6%, carnSp>0 in 8, preyCl 0.89, persisting (predK >= 64% of run after bootstrap) 11, exits 4, re-entries 3
    pred   baseline  9  arm 10   (+2 / -1)  McNemar p 1.000
    carn   baseline  8  arm  5   (+1 / -4)  McNemar p 0.375
    giant  baseline  0  arm  0   (+0 / -0)  McNemar p 1.000
    dwarf  baseline  0  arm  0   (+0 / -0)  McNemar p 1.000
    meat   baseline 0.216  arm 0.208   mean diff -0.009  sign test 6+/6-  p 1.000
    kill   baseline 0.166  arm 0.162   mean diff -0.004  sign test 6+/6-  p 1.000
    animals baseline 988  arm 1073   mean diff +85.034  sign test 7+/5-  p 0.774
    align  baseline 0.070  arm 0.047   mean diff -0.022  sign test 5+/7-  p 0.774
    predSp baseline 0.606  arm 0.624   mean diff +0.019  sign test 7+/5-  p 0.774

## v1-SD10-1841  `smellDecay=0.1`  (scored, 1000000 ticks, seeds 1841-1852, baseline v1-EG-base-1841)

Expected: shorter-lived scent (smellDecay 0.1, about 10 ticks, against 0.05), paired with the standing block of the same seeds. Longer scent (0.02) lowered alignment in both halves (0.039 against 0.062 pooled, n.s.), so fresh scent seems to carry the signal. Expect: alignment above the block's in 8 of 12 or more; predators within 2 of the block. If it also falls, 0.05 is near the best lifetime.

- worlds 12, meat 19.1%, kill 14.1%, carnSp>0 in 3, preyCl 0.86, persisting (predK >= 64% of run after bootstrap) 10, exits 7, re-entries 4
- fruit: gene 0.197 -> 0.305 (up in 8 of 12), div 0.199, fruit 26.2%, carried 39.9%
- baseline v1-EG-base-1841: worlds 12, meat 12.9%, kill 8.3%, carnSp>0 in 1, preyCl 0.89, persisting (predK >= 64% of run after bootstrap) 6, exits 9, re-entries 3
    pred   baseline  6  arm 10   (+5 / -1)  McNemar p 0.219
    carn   baseline  1  arm  3   (+2 / -0)  McNemar p 0.500
    giant  baseline  0  arm  0   (+0 / -0)  McNemar p 1.000
    dwarf  baseline  0  arm  0   (+0 / -0)  McNemar p 1.000
    meat   baseline 0.129  arm 0.191   mean diff +0.062  sign test 9+/3-  p 0.146
    kill   baseline 0.083  arm 0.141   mean diff +0.059  sign test 9+/3-  p 0.146
    animals baseline 1084  arm 1032   mean diff -51.952  sign test 6+/6-  p 1.000
    align  baseline 0.054  arm 0.074   mean diff +0.019  sign test 8+/4-  p 0.388
    predSp baseline 0.469  arm 0.535   mean diff +0.067  sign test 9+/3-  p 0.146

## v1-SD10-1853  `smellDecay=0.1`  (scored, 1000000 ticks, seeds 1853-1864, baseline v1-EG-base-1853)

Expected: shorter-lived scent (smellDecay 0.1, about 10 ticks, against 0.05), paired with the standing block of the same seeds. Longer scent (0.02) lowered alignment in both halves (0.039 against 0.062 pooled, n.s.), so fresh scent seems to carry the signal. Expect: alignment above the block's in 8 of 12 or more; predators within 2 of the block. If it also falls, 0.05 is near the best lifetime.

- worlds 12, meat 20.4%, kill 15.5%, carnSp>0 in 5, preyCl 0.88, persisting (predK >= 64% of run after bootstrap) 11, exits 5, re-entries 3
- fruit: gene 0.204 -> 0.202 (up in 5 of 12), div 0.182, fruit 22.8%, carried 27.7%
- baseline v1-EG-base-1853: worlds 12, meat 16.7%, kill 12.2%, carnSp>0 in 5, preyCl 0.91, persisting (predK >= 64% of run after bootstrap) 7, exits 7, re-entries 3
    pred   baseline  8  arm 10   (+4 / -2)  McNemar p 0.688
    carn   baseline  5  arm  5   (+3 / -3)  McNemar p 1.000
    giant  baseline  1  arm  0   (+0 / -1)  McNemar p 1.000
    dwarf  baseline  0  arm  0   (+0 / -0)  McNemar p 1.000
    meat   baseline 0.167  arm 0.204   mean diff +0.037  sign test 7+/5-  p 0.774
    kill   baseline 0.122  arm 0.155   mean diff +0.033  sign test 6+/6-  p 1.000
    animals baseline 1119  arm 1044   mean diff -74.998  sign test 4+/8-  p 0.388
    align  baseline 0.058  arm 0.084   mean diff +0.026  sign test 8+/4-  p 0.388
    predSp baseline 0.528  arm 0.575   mean diff +0.047  sign test 8+/4-  p 0.388

## v1-SM-3M-b  `defaults`  (scored, 3000000 ticks, seeds 1901-1912, baseline -)

Expected: a second 3M block on the smell default, to firm up predator comebacks: v1-SM-3M had 18 re-entries in 12 worlds against 12 without smell (v1-BP-3Mdefault). Expect re-entries 12 or more again, alignment about 0.04 throughout.

- worlds 12, meat 12.8%, kill 8.3%, carnSp>0 in 6, preyCl 0.85, persisting (predK >= 64% of run after bootstrap) 7, exits 16, re-entries 13
- fruit: gene 0.187 -> 0.530 (up in 11 of 12), div 0.228, fruit 26.8%, carried 56.7%

## v1-SD10-1985  `smellDecay=0.1`  (scored, 1000000 ticks, seeds 1985-1996, baseline v1-EG-base-1985)

Expected: third pair for shorter-lived scent (smellDecay 0.1): first half gave alignment 0.074 against 0.054 (8 of 12), predator worlds 10 against 6. Expect alignment above the block in 8 of 12; pooled over 36 pairs, alignment p < 0.05 would make 0.1 the default.

- worlds 12, meat 17.0%, kill 11.7%, carnSp>0 in 3, preyCl 0.89, persisting (predK >= 64% of run after bootstrap) 7, exits 7, re-entries 1
- fruit: gene 0.195 -> 0.297 (up in 5 of 12), div 0.198, fruit 29.6%, carried 39.2%
- baseline v1-EG-base-1985: worlds 12, meat 15.8%, kill 11.1%, carnSp>0 in 3, preyCl 0.86, persisting (predK >= 64% of run after bootstrap) 9, exits 7, re-entries 2
    pred   baseline  8  arm  7   (+1 / -2)  McNemar p 1.000
    carn   baseline  3  arm  3   (+1 / -1)  McNemar p 1.000
    giant  baseline  0  arm  0   (+0 / -0)  McNemar p 1.000
    dwarf  baseline  0  arm  0   (+0 / -0)  McNemar p 1.000
    meat   baseline 0.158  arm 0.170   mean diff +0.012  sign test 6+/6-  p 1.000
    kill   baseline 0.111  arm 0.117   mean diff +0.006  sign test 6+/6-  p 1.000
    animals baseline 1072  arm 984   mean diff -88.040  sign test 6+/6-  p 1.000
    align  baseline 0.054  arm 0.105   mean diff +0.051  sign test 8+/4-  p 0.388
    predSp baseline 0.567  arm 0.522   mean diff -0.045  sign test 5+/7-  p 0.774

## v1-SD10-2021  `smellDecay=0.1`  (scored, 1000000 ticks, seeds 2021-2032, baseline v1-EG-base-2021)

Expected: fourth pair for shorter-lived scent (smellDecay 0.1). Pairs so far: alignment higher in 16 of 24, predators persisting 21 against 13. Expect alignment above the block in 8 of 12; pooled 48 pairs decide the default at p < 0.05.

- worlds 12, meat 14.2%, kill 9.7%, carnSp>0 in 3, preyCl 0.89, persisting (predK >= 64% of run after bootstrap) 9, exits 8, re-entries 3
- fruit: gene 0.196 -> 0.366 (up in 10 of 12), div 0.223, fruit 23.2%, carried 44.4%
- baseline v1-EG-base-2021: worlds 12, meat 16.4%, kill 11.8%, carnSp>0 in 2, preyCl 0.85, persisting (predK >= 64% of run after bootstrap) 5, exits 13, re-entries 8
    pred   baseline  5  arm  6   (+3 / -2)  McNemar p 1.000
    carn   baseline  2  arm  3   (+3 / -2)  McNemar p 1.000
    giant  baseline  0  arm  0   (+0 / -0)  McNemar p 1.000
    dwarf  baseline  1  arm  0   (+0 / -1)  McNemar p 1.000
    meat   baseline 0.165  arm 0.142   mean diff -0.023  sign test 5+/7-  p 0.774
    kill   baseline 0.118  arm 0.097   mean diff -0.021  sign test 6+/6-  p 1.000
    animals baseline 1077  arm 1095   mean diff +18.078  sign test 7+/5-  p 0.774
    align  baseline 0.022  arm 0.058   mean diff +0.036  sign test 8+/4-  p 0.388
    predSp baseline 0.444  arm 0.507   mean diff +0.064  sign test 7+/5-  p 0.774

## v1-SD10-2129  `smellDecay=0.1`  (scored, 1000000 ticks, seeds 2129-2140, baseline v1-EG-base-2129)

Expected: fifth pair for shorter-lived scent (smellDecay 0.1). 36 pairs: alignment 0.088 against 0.055, higher in 24 (p 0.065); predator worlds 27 against 22. Expect alignment above the block in 8 of 12; pooled 60 pairs decide the default at p < 0.05.

- worlds 12, meat 16.7%, kill 11.2%, carnSp>0 in 4, preyCl 0.89, persisting (predK >= 64% of run after bootstrap) 7, exits 10, re-entries 3
- fruit: gene 0.199 -> 0.340 (up in 7 of 12), div 0.191, fruit 26.0%, carried 42.4%
- baseline v1-EG-base-2129: worlds 12, meat 18.1%, kill 13.7%, carnSp>0 in 4, preyCl 0.86, persisting (predK >= 64% of run after bootstrap) 9, exits 7, re-entries 3
    pred   baseline  8  arm  8   (+4 / -4)  McNemar p 1.000
    carn   baseline  4  arm  4   (+3 / -3)  McNemar p 1.000
    giant  baseline  0  arm  0   (+0 / -0)  McNemar p 1.000
    dwarf  baseline  0  arm  2   (+2 / -0)  McNemar p 0.500
    meat   baseline 0.181  arm 0.167   mean diff -0.014  sign test 5+/7-  p 0.774
    kill   baseline 0.137  arm 0.112   mean diff -0.025  sign test 5+/7-  p 0.774
    animals baseline 961  arm 989   mean diff +28.113  sign test 8+/4-  p 0.388
    align  baseline 0.043  arm 0.073   mean diff +0.029  sign test 8+/4-  p 0.388
    predSp baseline 0.502  arm 0.557   mean diff +0.055  sign test 7+/5-  p 0.774

## v1-CP-2321  `compass=1`  (scored, 1000000 ticks, seeds 2321-2332, baseline v1-EG-base-2321)

Expected: compass on the smell default (smellDecay 0.1), paired with the standing block of the same seeds. Before smell the compass cost predators (persisting 10 of 24 against 20) because prey streamed. Expect: prey still stream (polar above 0.3 in most worlds) and predators still persist less (fewer than the block in 2 blocks pooled); if smell's fronts let hunters keep up, persistence within 3 of the blocks.

- worlds 12, meat 13.5%, kill 8.4%, carnSp>0 in 2, preyCl 0.91, persisting (predK >= 64% of run after bootstrap) 5, exits 10, re-entries 2
- fruit: gene 0.197 -> 0.371 (up in 10 of 12), div 0.227, fruit 24.7%, carried 51.5%
- baseline v1-EG-base-2321: worlds 12, meat 18.0%, kill 13.1%, carnSp>0 in 4, preyCl 0.87, persisting (predK >= 64% of run after bootstrap) 10, exits 8, re-entries 1
    pred   baseline 10  arm  4   (+0 / -6)  McNemar p 0.031
    carn   baseline  4  arm  2   (+1 / -3)  McNemar p 0.625
    giant  baseline  0  arm  0   (+0 / -0)  McNemar p 1.000
    dwarf  baseline  0  arm  0   (+0 / -0)  McNemar p 1.000
    meat   baseline 0.180  arm 0.135   mean diff -0.045  sign test 3+/9-  p 0.146
    kill   baseline 0.131  arm 0.084   mean diff -0.047  sign test 4+/8-  p 0.388
    animals baseline 1010  arm 976   mean diff -33.191  sign test 6+/6-  p 1.000
    align  baseline 0.072  arm 0.303   mean diff +0.231  sign test 10+/2-  p 0.039
    predSp baseline 0.520  arm 0.405   mean diff -0.115  sign test 4+/8-  p 0.388

## v1-CP-2333  `compass=1`  (scored, 1000000 ticks, seeds 2333-2344, baseline v1-EG-base-2333)

Expected: compass on the smell default (smellDecay 0.1), paired with the standing block of the same seeds. Before smell the compass cost predators (persisting 10 of 24 against 20) because prey streamed. Expect: prey still stream (polar above 0.3 in most worlds) and predators still persist less (fewer than the block in 2 blocks pooled); if smell's fronts let hunters keep up, persistence within 3 of the blocks.

- worlds 12, meat 19.0%, kill 13.1%, carnSp>0 in 3, preyCl 0.99, persisting (predK >= 64% of run after bootstrap) 8, exits 7, re-entries 2
- fruit: gene 0.195 -> 0.227 (up in 6 of 12), div 0.186, fruit 24.7%, carried 38.9%
- baseline v1-EG-base-2333: worlds 12, meat 19.8%, kill 14.6%, carnSp>0 in 4, preyCl 0.86, persisting (predK >= 64% of run after bootstrap) 8, exits 9, re-entries 5
    pred   baseline  7  arm  8   (+4 / -3)  McNemar p 1.000
    carn   baseline  4  arm  3   (+3 / -4)  McNemar p 1.000
    giant  baseline  0  arm  0   (+0 / -0)  McNemar p 1.000
    dwarf  baseline  0  arm  0   (+0 / -0)  McNemar p 1.000
    meat   baseline 0.198  arm 0.190   mean diff -0.008  sign test 7+/5-  p 0.774
    kill   baseline 0.146  arm 0.131   mean diff -0.015  sign test 6+/6-  p 1.000
    animals baseline 971  arm 1021   mean diff +50.138  sign test 6+/6-  p 1.000
    align  baseline 0.070  arm 0.229   mean diff +0.159  sign test 12+/0-  p 0.000
    predSp baseline 0.545  arm 0.601   mean diff +0.056  sign test 8+/4-  p 0.388

## v1-SF-2513  `smellFruit=1`  (scored, 1000000 ticks, seeds 2513-2524, baseline v1-EG-base-2513)

Expected: fruit scent (smellFruit 1) on the smellDecay 0.1 default, paired with the standing block of the same seeds (NI 53 build). seeFruit alone let grazers steer to fruit but did not pay the plants (fruit gene 0.31 against 0.44). Expect: grazers turn toward fruit scent (tools/smell.js), fruit share of plant-eaters' energy up (above the block's in 8 of 12), fruit gene and carried-seed share higher; predators within 2 of the block.

- worlds 12, meat 20.6%, kill 15.8%, carnSp>0 in 4, preyCl 0.88, persisting (predK >= 64% of run after bootstrap) 9, exits 8, re-entries 3
- fruit: gene 0.186 -> 0.104 (up in 2 of 12), div 0.170, fruit 14.0%, carried 13.3%
- baseline v1-EG-base-2513: worlds 12, meat 16.1%, kill 10.7%, carnSp>0 in 4, preyCl 0.92, persisting (predK >= 64% of run after bootstrap) 7, exits 9, re-entries 4
    pred   baseline  7  arm  8   (+4 / -3)  McNemar p 1.000
    carn   baseline  4  arm  4   (+3 / -3)  McNemar p 1.000
    giant  baseline  0  arm  0   (+0 / -0)  McNemar p 1.000
    dwarf  baseline  0  arm  0   (+0 / -0)  McNemar p 1.000
    meat   baseline 0.161  arm 0.206   mean diff +0.045  sign test 9+/3-  p 0.146
    kill   baseline 0.107  arm 0.158   mean diff +0.051  sign test 9+/3-  p 0.146
    animals baseline 1040  arm 864   mean diff -175.958  sign test 4+/8-  p 0.388
    align  baseline 0.056  arm 0.104   mean diff +0.048  sign test 9+/3-  p 0.146
    predSp baseline 0.529  arm 0.591   mean diff +0.061  sign test 7+/5-  p 0.774

## v1-SF-2525  `smellFruit=1`  (scored, 1000000 ticks, seeds 2525-2536, baseline v1-EG-base-2525)

Expected: fruit scent (smellFruit 1) on the smellDecay 0.1 default, paired with the standing block of the same seeds (NI 53 build). seeFruit alone let grazers steer to fruit but did not pay the plants (fruit gene 0.31 against 0.44). Expect: grazers turn toward fruit scent (tools/smell.js), fruit share of plant-eaters' energy up (above the block's in 8 of 12), fruit gene and carried-seed share higher; predators within 2 of the block.

- worlds 12, meat 20.5%, kill 15.8%, carnSp>0 in 6, preyCl 0.85, persisting (predK >= 64% of run after bootstrap) 9, exits 5, re-entries 1
- fruit: gene 0.195 -> 0.101 (up in 2 of 12), div 0.168, fruit 10.0%, carried 14.7%
- baseline v1-EG-base-2525: worlds 12, meat 20.8%, kill 15.3%, carnSp>0 in 2, preyCl 0.97, persisting (predK >= 64% of run after bootstrap) 10, exits 5, re-entries 1
    pred   baseline  9  arm  8   (+1 / -2)  McNemar p 1.000
    carn   baseline  2  arm  6   (+5 / -1)  McNemar p 0.219
    giant  baseline  0  arm  0   (+0 / -0)  McNemar p 1.000
    dwarf  baseline  0  arm  0   (+0 / -0)  McNemar p 1.000
    meat   baseline 0.208  arm 0.205   mean diff -0.003  sign test 5+/7-  p 0.774
    kill   baseline 0.153  arm 0.158   mean diff +0.004  sign test 5+/7-  p 0.774
    animals baseline 1015  arm 904   mean diff -111.622  sign test 3+/9-  p 0.146
    align  baseline 0.122  arm 0.097   mean diff -0.025  sign test 4+/8-  p 0.388
    predSp baseline 0.613  arm 0.606   mean diff -0.007  sign test 5+/7-  p 0.774

## v1-SD05-2573  `smellDecay=0.05`  (scored, 1000000 ticks, seeds 2573-2584, baseline v1-EG-base-2573)

Expected: the old scent lifetime (smellDecay 0.05) against the 0.1 default, paired with the standing block of the same seeds. Unpaired blocks put 0.1 at 69% persistence (199 of 288) against 76% for 0.05 (228 of 300), while five same-seed pairs gave 0.1 44 of 60 against 36. Expect: persistence within 2 of the block per 12 (no cost of 0.1), alignment lower on 0.05 in 8 of 12.

- worlds 12, meat 13.5%, kill 8.6%, carnSp>0 in 1, preyCl 0.90, persisting (predK >= 64% of run after bootstrap) 4, exits 8, re-entries 4
- fruit: gene 0.193 -> 0.383 (up in 9 of 12), div 0.217, fruit 21.7%, carried 48.1%
- baseline v1-EG-base-2573: worlds 12, meat 20.2%, kill 15.7%, carnSp>0 in 2, preyCl 0.88, persisting (predK >= 64% of run after bootstrap) 10, exits 6, re-entries 3
    pred   baseline 10  arm  4   (+0 / -6)  McNemar p 0.031
    carn   baseline  2  arm  1   (+1 / -2)  McNemar p 1.000
    giant  baseline  0  arm  0   (+0 / -0)  McNemar p 1.000
    dwarf  baseline  0  arm  0   (+0 / -0)  McNemar p 1.000
    meat   baseline 0.202  arm 0.135   mean diff -0.068  sign test 4+/8-  p 0.388
    kill   baseline 0.157  arm 0.086   mean diff -0.071  sign test 3+/9-  p 0.146
    animals baseline 1011  arm 997   mean diff -14.074  sign test 5+/7-  p 0.774
    align  baseline 0.084  arm 0.059   mean diff -0.025  sign test 4+/8-  p 0.388
    predSp baseline 0.603  arm 0.477   mean diff -0.126  sign test 3+/9-  p 0.146

## v1-SD05-2585  `smellDecay=0.05`  (scored, 1000000 ticks, seeds 2585-2596, baseline v1-EG-base-2585)

Expected: the old scent lifetime (smellDecay 0.05) against the 0.1 default, paired with the standing block of the same seeds. Unpaired blocks put 0.1 at 69% persistence (199 of 288) against 76% for 0.05 (228 of 300), while five same-seed pairs gave 0.1 44 of 60 against 36. Expect: persistence within 2 of the block per 12 (no cost of 0.1), alignment lower on 0.05 in 8 of 12.

- worlds 12, meat 16.8%, kill 12.5%, carnSp>0 in 3, preyCl 0.92, persisting (predK >= 64% of run after bootstrap) 7, exits 9, re-entries 4
- fruit: gene 0.200 -> 0.346 (up in 9 of 12), div 0.220, fruit 23.8%, carried 43.1%
- baseline v1-EG-base-2585: worlds 12, meat 18.3%, kill 13.6%, carnSp>0 in 4, preyCl 0.90, persisting (predK >= 64% of run after bootstrap) 5, exits 11, re-entries 7
    pred   baseline  5  arm  6   (+3 / -2)  McNemar p 1.000
    carn   baseline  3  arm  3   (+2 / -2)  McNemar p 1.000
    giant  baseline  0  arm  0   (+0 / -0)  McNemar p 1.000
    dwarf  baseline  0  arm  0   (+0 / -0)  McNemar p 1.000
    meat   baseline 0.183  arm 0.168   mean diff -0.015  sign test 6+/6-  p 1.000
    kill   baseline 0.136  arm 0.125   mean diff -0.011  sign test 6+/6-  p 1.000
    animals baseline 1062  arm 1045   mean diff -16.276  sign test 5+/7-  p 0.774
    align  baseline 0.055  arm 0.033   mean diff -0.022  sign test 4+/8-  p 0.388
    predSp baseline 0.542  arm 0.453   mean diff -0.089  sign test 3+/9-  p 0.146

## v1-SD05-2597  `smellDecay=0.05`  (scored, 1000000 ticks, seeds 2597-2608, baseline v1-EG-base-2597)

Expected: third reverse pair: 0.05 against the 0.1 default on the same seeds, to settle whether 0.1 costs predator persistence (unpaired blocks 69% against 76%; earlier pairs favour 0.1). Expect persistence within 2 of the block.

- worlds 12, meat 21.1%, kill 16.2%, carnSp>0 in 5, preyCl 0.94, persisting (predK >= 64% of run after bootstrap) 10, exits 4, re-entries 1
- fruit: gene 0.192 -> 0.276 (up in 7 of 12), div 0.200, fruit 29.6%, carried 33.1%
- baseline v1-EG-base-2597: worlds 12, meat 18.4%, kill 13.7%, carnSp>0 in 0, preyCl 0.88, persisting (predK >= 64% of run after bootstrap) 8, exits 9, re-entries 5
    pred   baseline  7  arm 10   (+3 / -0)  McNemar p 0.250
    carn   baseline  0  arm  5   (+5 / -0)  McNemar p 0.062
    giant  baseline  0  arm  0   (+0 / -0)  McNemar p 1.000
    dwarf  baseline  0  arm  0   (+0 / -0)  McNemar p 1.000
    meat   baseline 0.184  arm 0.211   mean diff +0.028  sign test 8+/4-  p 0.388
    kill   baseline 0.137  arm 0.162   mean diff +0.025  sign test 7+/5-  p 0.774
    animals baseline 1007  arm 981   mean diff -25.907  sign test 5+/7-  p 0.774
    align  baseline 0.069  arm 0.061   mean diff -0.008  sign test 8+/4-  p 0.388
    predSp baseline 0.508  arm 0.604   mean diff +0.096  sign test 9+/3-  p 0.146

## v1-PA60-3065  `patchy=0.6`  (scored, 1000000 ticks, seeds 3065-3076, baseline v1-EG-base-3065)

Expected: pasture in patches (patchy 0.6, patchN 8: 60% of the world barren, about three patches joined by corridors), paired with the standing block of the same seeds. Predator lines are lost in one grazer size sweep across the whole map, and a transplant shows hunting still pays afterwards, so the path back is what is missing. Patches should let a sweep miss one patch or reach it later. Expect: predators persisting (predK >= 64%) in more worlds than the block (baseline 17 of 24 over both blocks), fewer exits, fewer animals (40% of the pasture). If persistence does not rise, a sweep crosses corridors as fast as open ground.

- worlds 12, meat 10.1%, kill 6.4%, carnSp>0 in 0, preyCl 1.74, persisting (predK >= 64% of run after bootstrap) 6, exits 10, re-entries 1
- fruit: gene 0.206 -> 0.122 (up in 1 of 12), div 0.199, fruit 13.5%, carried 21.0%
- baseline v1-EG-base-3065: worlds 12, meat 19.3%, kill 14.4%, carnSp>0 in 5, preyCl 0.93, persisting (predK >= 64% of run after bootstrap) 8, exits 6, re-entries 2
    pred   baseline  9  arm  6   (+1 / -4)  McNemar p 0.375
    carn   baseline  5  arm  0   (+0 / -5)  McNemar p 0.062
    giant  baseline  0  arm  0   (+0 / -0)  McNemar p 1.000
    dwarf  baseline  0  arm  0   (+0 / -0)  McNemar p 1.000
    meat   baseline 0.193  arm 0.101   mean diff -0.092  sign test 1+/11-  p 0.006
    kill   baseline 0.144  arm 0.064   mean diff -0.079  sign test 1+/11-  p 0.006
    animals baseline 1036  arm 354   mean diff -681.978  sign test 0+/12-  p 0.000
    align  baseline 0.101  arm 0.005   mean diff -0.096  sign test 1+/11-  p 0.006
    predSp baseline 0.546  arm 0.316   mean diff -0.230  sign test 2+/10-  p 0.039

## v1-PA60-3089  `patchy=0.6`  (scored, 1000000 ticks, seeds 3089-3100, baseline v1-EG-base-3089)

Expected: pasture in patches (patchy 0.6, patchN 8: 60% of the world barren, about three patches joined by corridors), paired with the standing block of the same seeds. Predator lines are lost in one grazer size sweep across the whole map, and a transplant shows hunting still pays afterwards, so the path back is what is missing. Patches should let a sweep miss one patch or reach it later. Expect: predators persisting (predK >= 64%) in more worlds than the block (baseline 17 of 24 over both blocks), fewer exits, fewer animals (40% of the pasture). If persistence does not rise, a sweep crosses corridors as fast as open ground.

- worlds 12, meat 16.9%, kill 12.0%, carnSp>0 in 3, preyCl 1.96, persisting (predK >= 64% of run after bootstrap) 7, exits 7, re-entries 1
- fruit: gene 0.215 -> 0.143 (up in 1 of 12), div 0.182, fruit 25.3%, carried 18.1%
- baseline v1-EG-base-3089: worlds 12, meat 20.3%, kill 15.1%, carnSp>0 in 4, preyCl 0.95, persisting (predK >= 64% of run after bootstrap) 9, exits 5, re-entries 0
    pred   baseline  9  arm  7   (+1 / -3)  McNemar p 0.625
    carn   baseline  4  arm  3   (+2 / -3)  McNemar p 1.000
    giant  baseline  0  arm  0   (+0 / -0)  McNemar p 1.000
    dwarf  baseline  0  arm  0   (+0 / -0)  McNemar p 1.000
    meat   baseline 0.203  arm 0.169   mean diff -0.034  sign test 4+/8-  p 0.388
    kill   baseline 0.151  arm 0.120   mean diff -0.031  sign test 4+/8-  p 0.388
    animals baseline 1069  arm 468   mean diff -600.764  sign test 0+/12-  p 0.000
    align  baseline 0.120  arm 0.040   mean diff -0.080  sign test 3+/9-  p 0.146
    predSp baseline 0.630  arm 0.417   mean diff -0.213  sign test 3+/9-  p 0.146

## v1-G96-3065  `gridN=96`  (dropped, 1000000 ticks, seeds 3065-3076, baseline v1-EG-base-3065)

Expected: a larger world at the same density (gridN 96, 2.25x the area of the standing blocks' 64), on the seeds of v1-EG-base-3065. Seeds do not pair across grid sizes, so compare counts, not pairs. patchy 0.6 lost predators by cutting food (animals 354 against 1036, meat 10% against 19%); this adds room without cutting density. If a sweep takes a fixed time to cross ground, a bigger world should keep a hunter line somewhere. Expect: predators persisting in 10+ of 12 (block: 9), carnivore species in more worlds (block: 5), animals about 2.2x. MINING had 96x96 worlds predator-dominated 13 of 20, confounded by batch.

(no digest)

## v1-DX1-3137  `dmgExp=1`  (scored, 1000000 ticks, seeds 3137-3148, baseline v1-EG-base-3137)

Expected: strike damage x attacker mass^1 (dmgExp 1, default 0.75), paired with the standing block of the same seeds. Hit points are 2 x mass, so at 0.75 a fight at a given size ratio lasts longer the bigger the pair, and grazer size sweeps end predator lines. Pre-crash branches (regen/branch3.js): hunters kept above 20 in 3 of 3 against 2 of 3 as is, but the dmg 0.64 control did as well. Expect: predators persisting in more worlds than the block (pooled baseline for the two blocks 19 of 24), fewer exits; kill share up; if dmg 0.64 (v1-DM064) does as well, it is strength, not scaling.

- worlds 12, meat 20.1%, kill 14.9%, carnSp>0 in 4, preyCl 0.94, persisting (predK >= 64% of run after bootstrap) 9, exits 5, re-entries 3
- fruit: gene 0.198 -> 0.299 (up in 5 of 12), div 0.198, fruit 32.5%, carried 36.7%
- baseline v1-EG-base-3137: worlds 12, meat 17.8%, kill 12.9%, carnSp>0 in 5, preyCl 0.92, persisting (predK >= 64% of run after bootstrap) 10, exits 5, re-entries 2
    pred   baseline  9  arm  7   (+2 / -4)  McNemar p 0.688
    carn   baseline  5  arm  4   (+2 / -3)  McNemar p 1.000
    giant  baseline  0  arm  0   (+0 / -0)  McNemar p 1.000
    dwarf  baseline  0  arm  0   (+0 / -0)  McNemar p 1.000
    meat   baseline 0.178  arm 0.201   mean diff +0.024  sign test 6+/6-  p 1.000
    kill   baseline 0.129  arm 0.149   mean diff +0.020  sign test 6+/6-  p 1.000
    animals baseline 1005  arm 1165   mean diff +159.556  sign test 8+/4-  p 0.388
    align  baseline 0.066  arm 0.082   mean diff +0.017  sign test 6+/6-  p 1.000
    predSp baseline 0.510  arm 0.586   mean diff +0.076  sign test 7+/5-  p 0.774

## v1-DM064-3137  `dmg=0.64`  (scored, 1000000 ticks, seeds 3137-3148, baseline v1-EG-base-3137)

Expected: plain strike damage x1.28 (dmg 0.64, default 0.5): the control for dmgExp 1, the same boost at the pre-crash hunters' size 2.7, paired with the standing block of the same seeds. Expect: persistence up with it too if strength is what saves hunters through a size sweep; less than v1-DX1 in giant worlds if scaling matters.

- worlds 12, meat 16.5%, kill 11.6%, carnSp>0 in 3, preyCl 0.86, persisting (predK >= 64% of run after bootstrap) 10, exits 8, re-entries 3
- fruit: gene 0.194 -> 0.245 (up in 6 of 12), div 0.186, fruit 24.1%, carried 32.9%
- baseline v1-EG-base-3137: worlds 12, meat 17.8%, kill 12.9%, carnSp>0 in 5, preyCl 0.92, persisting (predK >= 64% of run after bootstrap) 10, exits 5, re-entries 2
    pred   baseline  9  arm  9   (+3 / -3)  McNemar p 1.000
    carn   baseline  5  arm  3   (+2 / -4)  McNemar p 0.688
    giant  baseline  0  arm  0   (+0 / -0)  McNemar p 1.000
    dwarf  baseline  0  arm  0   (+0 / -0)  McNemar p 1.000
    meat   baseline 0.178  arm 0.165   mean diff -0.013  sign test 4+/8-  p 0.388
    kill   baseline 0.129  arm 0.116   mean diff -0.013  sign test 5+/7-  p 0.774
    animals baseline 1005  arm 979   mean diff -26.731  sign test 5+/7-  p 0.774
    align  baseline 0.066  arm 0.081   mean diff +0.016  sign test 5+/7-  p 0.774
    predSp baseline 0.510  arm 0.533   mean diff +0.023  sign test 7+/5-  p 0.774

## v1-DX1-3161  `dmgExp=1`  (scored, 1000000 ticks, seeds 3161-3172, baseline v1-EG-base-3161)

Expected: strike damage x attacker mass^1 (dmgExp 1, default 0.75), paired with the standing block of the same seeds. Hit points are 2 x mass, so at 0.75 a fight at a given size ratio lasts longer the bigger the pair, and grazer size sweeps end predator lines. Pre-crash branches (regen/branch3.js): hunters kept above 20 in 3 of 3 against 2 of 3 as is, but the dmg 0.64 control did as well. Expect: predators persisting in more worlds than the block (pooled baseline for the two blocks 19 of 24), fewer exits; kill share up; if dmg 0.64 (v1-DM064) does as well, it is strength, not scaling.

- worlds 12, meat 20.8%, kill 15.7%, carnSp>0 in 3, preyCl 0.92, persisting (predK >= 64% of run after bootstrap) 11, exits 6, re-entries 0
- fruit: gene 0.197 -> 0.304 (up in 7 of 12), div 0.176, fruit 27.1%, carried 38.2%
- baseline v1-EG-base-3161: worlds 12, meat 17.4%, kill 12.7%, carnSp>0 in 3, preyCl 0.93, persisting (predK >= 64% of run after bootstrap) 9, exits 4, re-entries 1
    pred   baseline  8  arm 10   (+3 / -1)  McNemar p 0.625
    carn   baseline  3  arm  3   (+2 / -2)  McNemar p 1.000
    giant  baseline  0  arm  0   (+0 / -0)  McNemar p 1.000
    dwarf  baseline  1  arm  2   (+2 / -1)  McNemar p 1.000
    meat   baseline 0.174  arm 0.208   mean diff +0.033  sign test 7+/5-  p 0.774
    kill   baseline 0.127  arm 0.157   mean diff +0.030  sign test 6+/6-  p 1.000
    animals baseline 1072  arm 1151   mean diff +79.239  sign test 8+/4-  p 0.388
    align  baseline 0.080  arm 0.069   mean diff -0.010  sign test 5+/7-  p 0.774
    predSp baseline 0.523  arm 0.557   mean diff +0.033  sign test 7+/5-  p 0.774

## v1-DM064-3161  `dmg=0.64`  (scored, 1000000 ticks, seeds 3161-3172, baseline v1-EG-base-3161)

Expected: plain strike damage x1.28 (dmg 0.64, default 0.5): the control for dmgExp 1, the same boost at the pre-crash hunters' size 2.7, paired with the standing block of the same seeds. Expect: persistence up with it too if strength is what saves hunters through a size sweep; less than v1-DX1 in giant worlds if scaling matters.

- worlds 12, meat 22.2%, kill 17.1%, carnSp>0 in 6, preyCl 0.92, persisting (predK >= 64% of run after bootstrap) 11, exits 6, re-entries 3
- fruit: gene 0.202 -> 0.235 (up in 3 of 12), div 0.178, fruit 28.3%, carried 31.7%
- baseline v1-EG-base-3161: worlds 12, meat 17.4%, kill 12.7%, carnSp>0 in 3, preyCl 0.93, persisting (predK >= 64% of run after bootstrap) 9, exits 4, re-entries 1
    pred   baseline  8  arm 10   (+3 / -1)  McNemar p 0.625
    carn   baseline  3  arm  6   (+5 / -2)  McNemar p 0.453
    giant  baseline  0  arm  0   (+0 / -0)  McNemar p 1.000
    dwarf  baseline  1  arm  0   (+0 / -1)  McNemar p 1.000
    meat   baseline 0.174  arm 0.222   mean diff +0.047  sign test 10+/2-  p 0.039
    kill   baseline 0.127  arm 0.171   mean diff +0.044  sign test 10+/2-  p 0.039
    animals baseline 1072  arm 1019   mean diff -52.797  sign test 6+/6-  p 1.000
    align  baseline 0.080  arm 0.091   mean diff +0.011  sign test 7+/5-  p 0.774
    predSp baseline 0.523  arm 0.571   mean diff +0.048  sign test 8+/4-  p 0.388
