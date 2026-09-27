# Results log (written by tools/ops.py digest; newest last)

### v1-BE-sizemax8 (2026-09-27 08:29)

`sizeMax=8`, seeds 1101-1112, 1000000 ticks. Expected: giant-grazer escapes (grazers outgrowing hunters) become rarer: fewer exits, persistence at least the baseline 9 of 12

- worlds 12, meat 15.2%, kill 10.9%, carnSp>0 in 3, preyCl 0.79, persisting (predK >= 64% of run after bootstrap) 6, exits 11, re-entries 2
- baseline v1-BC-s1c0: worlds 12, meat 19.3%, kill 15.3%, carnSp>0 in 2, preyCl 0.77, persisting (predK >= 64% of run after bootstrap) 9, exits 6, re-entries 1
    pred   baseline 10  arm  5   (+0 / -5)  McNemar p 0.062
    carn   baseline  2  arm  2   (+1 / -1)  McNemar p 1.000
    giant  baseline  0  arm  0   (+0 / -0)  McNemar p 1.000
    dwarf  baseline  0  arm  0   (+0 / -0)  McNemar p 1.000
    meat   baseline 0.193  arm 0.152   mean diff -0.041  sign test 6+/6-  p 1.000
    preyCl baseline 0.772  arm 0.791   mean diff +0.019  sign test 7+/5-  p 0.774
    predCl baseline 1.875  arm 3.501   mean diff +1.626  sign test 9+/3-  p 0.146
    diet   baseline 0.091  arm 0.086   mean diff -0.005  sign test 5+/7-  p 0.774
    polar  baseline 0.037  arm 0.040   mean diff +0.004  sign test 6+/6-  p 1.000
    align  baseline 0.022  arm 0.007   mean diff -0.014  sign test 5+/7-  p 0.774
    preySp baseline 0.284  arm 0.292   mean diff +0.008  sign test 7+/5-  p 0.774
    predSp baseline 0.478  arm 0.416   mean diff -0.062  sign test 4+/8-  p 0.388

### v1-BE-mutsd12 (2026-09-27 09:36)

`mutSd=0.12`, seeds 1101-1112, 1000000 ticks. Expected: bigger mutation steps help a grazer line cross to hunting again: re-entries after an exit above 0 in some worlds (baseline: 0)

- worlds 12, meat 18.4%, kill 14.0%, carnSp>0 in 3, preyCl 0.87, persisting (predK >= 64% of run after bootstrap) 9, exits 12, re-entries 6
- baseline v1-BC-s1c0: worlds 12, meat 19.3%, kill 15.3%, carnSp>0 in 2, preyCl 0.77, persisting (predK >= 64% of run after bootstrap) 9, exits 6, re-entries 1
    pred   baseline 10  arm  8   (+1 / -3)  McNemar p 0.625
    carn   baseline  2  arm  3   (+1 / -0)  McNemar p 1.000
    giant  baseline  0  arm  0   (+0 / -0)  McNemar p 1.000
    dwarf  baseline  0  arm  0   (+0 / -0)  McNemar p 1.000
    meat   baseline 0.193  arm 0.184   mean diff -0.009  sign test 4+/8-  p 0.388
    preyCl baseline 0.772  arm 0.872   mean diff +0.100  sign test 9+/3-  p 0.146
    predCl baseline 1.875  arm 2.713   mean diff +0.838  sign test 10+/2-  p 0.039
    diet   baseline 0.091  arm 0.085   mean diff -0.006  sign test 4+/8-  p 0.388
    polar  baseline 0.037  arm 0.035   mean diff -0.001  sign test 5+/7-  p 0.774
    align  baseline 0.022  arm 0.000   mean diff -0.022  sign test 5+/7-  p 0.774
    preySp baseline 0.284  arm 0.263   mean diff -0.021  sign test 5+/7-  p 0.774
    predSp baseline 0.478  arm 0.452   mean diff -0.026  sign test 5+/7-  p 0.774

### v1-BE-3M (2026-09-27 09:36)

`defaults`, seeds 1201-1212, 3000000 ticks. Expected: over 3M ticks: does any world re-evolve predators after a collapse (re-entries > 0)? Expected rare or none

- worlds 12, meat 16.1%, kill 11.7%, carnSp>0 in 1, preyCl 0.89, persisting (predK >= 64% of run after bootstrap) 6, exits 14, re-entries 7

### v1-EG-base-1113 (2026-09-27 09:36)

`defaults`, seeds 1113-1124, 1000000 ticks. Expected: standing replication of the default build at 1M ticks: predators persist in about 3 of 4

- worlds 12, meat 15.3%, kill 11.1%, carnSp>0 in 2, preyCl 0.82, persisting (predK >= 64% of run after bootstrap) 6, exits 11, re-entries 4

### v1-EG-base-1125 (2026-09-27 09:36)

`defaults`, seeds 1125-1136, 1000000 ticks. Expected: standing replication of the default build at 1M ticks: predators persist in about 3 of 4

- worlds 12, meat 15.3%, kill 11.1%, carnSp>0 in 1, preyCl 0.81, persisting (predK >= 64% of run after bootstrap) 8, exits 8, re-entries 2
### v1-BF-fruit1 (2026-09-27 10:48)

`fruit=1`, seeds 1101-1124, 1000000 ticks. Expected: fruit gene settles low but above 0; animal-carried seeds a steady share; meat share and predator persistence at least baseline

- worlds 24, meat 18.3%, kill 14.0%, carnSp>0 in 8, preyCl 0.87, persisting (predK >= 64% of run after bootstrap) 15, exits 11, re-entries 4
- baseline v1-BF-fruit0: worlds 24, meat 18.0%, kill 13.5%, carnSp>0 in 4, preyCl 0.80, persisting (predK >= 64% of run after bootstrap) 17, exits 20, re-entries 8
    pred   baseline 16  arm 14   (+4 / -6)  McNemar p 0.754
    carn   baseline  4  arm  8   (+8 / -4)  McNemar p 0.388
    giant  baseline  0  arm  1   (+1 / -0)  McNemar p 1.000
    dwarf  baseline  1  arm  1   (+1 / -1)  McNemar p 1.000
    meat   baseline 0.180  arm 0.183   mean diff +0.004  sign test 10+/14-  p 0.541
    preyCl baseline 0.805  arm 0.867   mean diff +0.062  sign test 18+/6-  p 0.023
    predCl baseline 2.713  arm 3.241   mean diff +0.528  sign test 13+/11-  p 0.839
    diet   baseline 0.086  arm 0.088   mean diff +0.002  sign test 11+/13-  p 0.839
    polar  baseline 0.035  arm 0.033   mean diff -0.003  sign test 5+/19-  p 0.007
    align  baseline 0.009  arm 0.018   mean diff +0.009  sign test 11+/13-  p 0.839
    preySp baseline 0.284  arm 0.302   mean diff +0.019  sign test 12+/12-  p 1.000
    predSp baseline 0.464  arm 0.477   mean diff +0.013  sign test 12+/12-  p 1.000

### v1-BF-fruit0 (2026-09-27 10:48)

`fruit=0`, seeds 1101-1124, 1000000 ticks. Expected: baseline for fruit on this build

- worlds 24, meat 18.0%, kill 13.5%, carnSp>0 in 4, preyCl 0.80, persisting (predK >= 64% of run after bootstrap) 17, exits 20, re-entries 8

### v1-BH-mutsd12b (2026-09-27 10:48)

`mutSd=0.12`, seeds 1113-1124, 1000000 ticks. Expected: replicates v1-BE-mutsd12: more re-entries and more exits than baseline, persistence unchanged

- worlds 12, meat 17.6%, kill 13.2%, carnSp>0 in 1, preyCl 0.77, persisting (predK >= 64% of run after bootstrap) 7, exits 8, re-entries 1
- baseline v1-EG-base-1113: worlds 12, meat 15.3%, kill 11.1%, carnSp>0 in 2, preyCl 0.82, persisting (predK >= 64% of run after bootstrap) 6, exits 11, re-entries 4
    pred   baseline  6  arm  7   (+4 / -3)  McNemar p 1.000
    carn   baseline  2  arm  1   (+1 / -2)  McNemar p 1.000
    giant  baseline  0  arm  0   (+0 / -0)  McNemar p 1.000
    dwarf  baseline  0  arm  0   (+0 / -0)  McNemar p 1.000
    meat   baseline 0.153  arm 0.176   mean diff +0.024  sign test 7+/5-  p 0.774
    preyCl baseline 0.820  arm 0.766   mean diff -0.054  sign test 4+/8-  p 0.388
    predCl baseline 3.227  arm 3.123   mean diff -0.104  sign test 5+/7-  p 0.774
    diet   baseline 0.082  arm 0.083   mean diff +0.001  sign test 7+/5-  p 0.774
    polar  baseline 0.035  arm 0.035   mean diff -0.000  sign test 6+/6-  p 1.000
    align  baseline 0.005  arm 0.014   mean diff +0.009  sign test 8+/4-  p 0.388
    preySp baseline 0.257  arm 0.281   mean diff +0.024  sign test 8+/4-  p 0.388
    predSp baseline 0.416  arm 0.483   mean diff +0.067  sign test 8+/4-  p 0.388

### v1-BH-mutsd16 (2026-09-27 11:04)

`mutSd=0.16`, seeds 1101-1112, 1000000 ticks. Expected: dose: still more turnover (re-entries and exits) than 0.12; persistence may fall

- worlds 12, meat 13.4%, kill 8.5%, carnSp>0 in 1, preyCl 0.81, persisting (predK >= 64% of run after bootstrap) 5, exits 9, re-entries 2
- baseline v1-BC-s1c0: worlds 12, meat 19.3%, kill 15.3%, carnSp>0 in 2, preyCl 0.77, persisting (predK >= 64% of run after bootstrap) 9, exits 6, re-entries 1
    pred   baseline 10  arm  4   (+2 / -8)  McNemar p 0.109
    carn   baseline  2  arm  1   (+1 / -2)  McNemar p 1.000
    giant  baseline  0  arm  0   (+0 / -0)  McNemar p 1.000
    dwarf  baseline  0  arm  0   (+0 / -0)  McNemar p 1.000
    meat   baseline 0.193  arm 0.134   mean diff -0.059  sign test 4+/8-  p 0.388
    preyCl baseline 0.772  arm 0.813   mean diff +0.040  sign test 6+/6-  p 1.000
    predCl baseline 1.875  arm 4.613   mean diff +2.738  sign test 9+/3-  p 0.146
    diet   baseline 0.091  arm 0.089   mean diff -0.002  sign test 5+/7-  p 0.774
    polar  baseline 0.037  arm 0.034   mean diff -0.003  sign test 3+/9-  p 0.146
    align  baseline 0.022  arm -0.007   mean diff -0.028  sign test 3+/9-  p 0.146
    preySp baseline 0.284  arm 0.278   mean diff -0.006  sign test 7+/5-  p 0.774
    predSp baseline 0.478  arm 0.392   mean diff -0.086  sign test 5+/7-  p 0.774

