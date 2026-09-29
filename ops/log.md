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

### v1-EG-base-1137 (2026-09-27 11:23)

`defaults`, seeds 1137-1148, 1000000 ticks. Expected: standing replication of the default build at 1M ticks: predators persist in about 3 of 4

- worlds 12, meat 13.9%, kill 9.6%, carnSp>0 in 0, preyCl 0.79, persisting (predK >= 64% of run after bootstrap) 7, exits 10, re-entries 2

### v1-BG-grid96 (2026-09-27 11:27)

`gridN=96`, seeds 1101-1112, 1000000 ticks. Expected: a bigger world holds more predators and more refuges: persistence above the 64-grid baseline, fewer exits

- worlds 12, meat 17.6%, kill 14.0%, carnSp>0 in 2, preyCl 0.78, persisting (predK >= 64% of run after bootstrap) 9, exits 7, re-entries 2
- baseline v1-BF-fruit0: worlds 24, meat 18.0%, kill 13.5%, carnSp>0 in 4, preyCl 0.80, persisting (predK >= 64% of run after bootstrap) 17, exits 20, re-entries 8
    pred   baseline  7  arm  7   (+3 / -3)  McNemar p 1.000
    carn   baseline  2  arm  2   (+2 / -2)  McNemar p 1.000
    giant  baseline  0  arm  0   (+0 / -0)  McNemar p 1.000
    dwarf  baseline  0  arm  0   (+0 / -0)  McNemar p 1.000
    meat   baseline 0.158  arm 0.176   mean diff +0.018  sign test 7+/5-  p 0.774
    preyCl baseline 0.771  arm 0.784   mean diff +0.012  sign test 7+/5-  p 0.774
    predCl baseline 3.061  arm 3.957   mean diff +0.896  sign test 7+/5-  p 0.774
    diet   baseline 0.085  arm 0.080   mean diff -0.006  sign test 3+/9-  p 0.146
    polar  baseline 0.035  arm 0.024   mean diff -0.011  sign test 1+/11-  p 0.006
    align  baseline -0.001  arm 0.048   mean diff +0.049  sign test 9+/3-  p 0.146
    preySp baseline 0.279  arm 0.285   mean diff +0.006  sign test 4+/8-  p 0.388
    predSp baseline 0.446  arm 0.554   mean diff +0.107  sign test 7+/5-  p 0.774

### v1-BI-3Mb (2026-09-27 12:23)

`defaults`, seeds 1213-1224, 3000000 ticks. Expected: default build over 3M ticks: exits and re-entries both several per 12 worlds (v1-BE-3M: 14 and 7); species turnover

- worlds 12, meat 10.3%, kill 5.5%, carnSp>0 in 1, preyCl 0.80, persisting (predK >= 64% of run after bootstrap) 2, exits 14, re-entries 5

### v1-EG-base-1149 (2026-09-27 12:23)

`defaults`, seeds 1149-1160, 1000000 ticks. Expected: standing replication of the default build at 1M ticks: predators persist in about 3 of 4

- worlds 12, meat 19.3%, kill 14.9%, carnSp>0 in 4, preyCl 0.81, persisting (predK >= 64% of run after bootstrap) 8, exits 11, re-entries 7

### v1-BJ-fjc (2026-09-27 12:23)

`fruit=1,jc=0.8`, seeds 1101-1112, 400000 ticks. Expected: fruit gene holds or rises (up in most worlds); carried seed a large share; plant diversity up

- worlds 12, meat 24.7%, kill 20.0%, carnSp>0 in 6, preyCl 0.91
- fruit: gene 0.197 -> 0.130 (up in 0 of 12), div 0.157, fruit 28.8%, carried 10.0%
- baseline v1-BJ-fjcnd: worlds 12, meat 27.3%, kill 22.3%, carnSp>0 in 5, preyCl 1.01
    pred   baseline 10  arm 10   (+2 / -2)  McNemar p 1.000
    carn   baseline  5  arm  6   (+3 / -2)  McNemar p 1.000
    giant  baseline  0  arm  0   (+0 / -0)  McNemar p 1.000
    dwarf  baseline  0  arm  0   (+0 / -0)  McNemar p 1.000
    meat   baseline 0.273  arm 0.247   mean diff -0.026  sign test 8+/4-  p 0.388
    preyCl baseline 1.013  arm 0.913   mean diff -0.099  sign test 4+/8-  p 0.388
    predCl baseline 1.886  arm 1.502   mean diff -0.384  sign test 5+/7-  p 0.774
    diet   baseline 0.095  arm 0.097   mean diff +0.001  sign test 8+/4-  p 0.388
    polar  baseline 0.028  arm 0.030   mean diff +0.002  sign test 6+/6-  p 1.000
    align  baseline -0.004  arm 0.007   mean diff +0.011  sign test 8+/4-  p 0.388
    preySp baseline 0.241  arm 0.326   mean diff +0.085  sign test 9+/3-  p 0.146
    predSp baseline 0.506  arm 0.569   mean diff +0.062  sign test 9+/3-  p 0.146

### v1-BJ-fjcnd (2026-09-27 12:23)

`fruit=1,jc=0.8,gutTicks=0`, seeds 1101-1112, 400000 ticks. Expected: no carrying: fruit gene falls

- worlds 12, meat 27.3%, kill 22.3%, carnSp>0 in 5, preyCl 1.01
- fruit: gene 0.182 -> 0.085 (up in 0 of 12), div 0.147, fruit 20.1%, carried 0.0%

### v1-BJ-f (2026-09-27 12:55)

`fruit=1`, seeds 1101-1112, 400000 ticks. Expected: fruit without jc: gene falls as before

- worlds 12, meat 26.2%, kill 21.4%, carnSp>0 in 6, preyCl 0.91
- fruit: gene 0.200 -> 0.130 (up in 0 of 12), div 0.157, fruit 28.7%, carried 10.7%
- baseline v1-BJ-fjcnd: worlds 12, meat 27.3%, kill 22.3%, carnSp>0 in 5, preyCl 1.01
    pred   baseline 10  arm 10   (+1 / -1)  McNemar p 1.000
    carn   baseline  5  arm  6   (+3 / -2)  McNemar p 1.000
    giant  baseline  0  arm  0   (+0 / -0)  McNemar p 1.000
    dwarf  baseline  0  arm  0   (+0 / -0)  McNemar p 1.000
    meat   baseline 0.273  arm 0.262   mean diff -0.010  sign test 5+/7-  p 0.774
    preyCl baseline 1.013  arm 0.912   mean diff -0.101  sign test 5+/7-  p 0.774
    predCl baseline 1.886  arm 1.404   mean diff -0.482  sign test 7+/5-  p 0.774
    diet   baseline 0.095  arm 0.095   mean diff -0.000  sign test 8+/4-  p 0.388
    polar  baseline 0.028  arm 0.028   mean diff -0.001  sign test 5+/7-  p 0.774
    align  baseline -0.004  arm -0.004   mean diff -0.000  sign test 4+/8-  p 0.388
    preySp baseline 0.241  arm 0.309   mean diff +0.068  sign test 10+/2-  p 0.039
    predSp baseline 0.506  arm 0.583   mean diff +0.077  sign test 9+/3-  p 0.146

### v1-BJ-jc (2026-09-27 12:55)

`jc=0.8`, seeds 1101-1112, 400000 ticks. Expected: jc alone: plant diversity up; animal effects small

- worlds 12, meat 17.7%, kill 12.8%, carnSp>0 in 4, preyCl 0.86
- baseline v1-BJ-base: worlds 12, meat 22.6%, kill 17.6%, carnSp>0 in 3, preyCl 0.96
    pred   baseline  9  arm  5   (+2 / -6)  McNemar p 0.289
    carn   baseline  3  arm  4   (+4 / -3)  McNemar p 1.000
    giant  baseline  1  arm  0   (+0 / -1)  McNemar p 1.000
    dwarf  baseline  0  arm  0   (+0 / -0)  McNemar p 1.000
    meat   baseline 0.226  arm 0.177   mean diff -0.049  sign test 5+/7-  p 0.774
    preyCl baseline 0.962  arm 0.857   mean diff -0.106  sign test 3+/9-  p 0.146
    predCl baseline 2.142  arm 1.342   mean diff -0.800  sign test 5+/7-  p 0.774
    diet   baseline 0.090  arm 0.097   mean diff +0.007  sign test 6+/6-  p 1.000
    polar  baseline 0.034  arm 0.042   mean diff +0.008  sign test 7+/5-  p 0.774
    align  baseline -0.009  arm 0.007   mean diff +0.016  sign test 8+/4-  p 0.388
    preySp baseline 0.226  arm 0.287   mean diff +0.061  sign test 10+/2-  p 0.039
    predSp baseline 0.439  arm 0.416   mean diff -0.023  sign test 5+/7-  p 0.774

### v1-BJ-base (2026-09-27 12:55)

`defaults`, seeds 1101-1112, 400000 ticks. Expected: baseline for the fruit and jc arms on this build

- worlds 12, meat 22.6%, kill 17.6%, carnSp>0 in 3, preyCl 0.96

### v1-BK-fjc02 (2026-09-27 13:10)

`fruit=1,jc=0.8,fruitPerSeed=0.2`, seeds 1101-1124, 400000 ticks. Expected: with 2.5x the seeds per fruit, carrying pays: fruit gene higher than without carrying in most pairs and holding or rising

- worlds 24, meat 26.7%, kill 22.1%, carnSp>0 in 12, preyCl 0.94
- fruit: gene 0.200 -> 0.148 (up in 3 of 24), div 0.157, fruit 28.2%, carried 17.0%
- baseline v1-BK-fjcnd02: worlds 24, meat 26.6%, kill 21.6%, carnSp>0 in 10, preyCl 1.01
    pred   baseline 20  arm 23   (+4 / -1)  McNemar p 0.375
    carn   baseline 10  arm 12   (+8 / -6)  McNemar p 0.791
    giant  baseline  0  arm  0   (+0 / -0)  McNemar p 1.000
    dwarf  baseline  0  arm  0   (+0 / -0)  McNemar p 1.000
    meat   baseline 0.266  arm 0.267   mean diff +0.001  sign test 12+/12-  p 1.000
    preyCl baseline 1.009  arm 0.940   mean diff -0.069  sign test 7+/17-  p 0.064
    predCl baseline 1.902  arm 1.733   mean diff -0.169  sign test 15+/9-  p 0.307
    diet   baseline 0.097  arm 0.107   mean diff +0.010  sign test 14+/10-  p 0.541
    polar  baseline 0.029  arm 0.028   mean diff -0.001  sign test 13+/11-  p 0.839
    align  baseline -0.008  arm -0.003   mean diff +0.005  sign test 15+/9-  p 0.307
    preySp baseline 0.264  arm 0.287   mean diff +0.023  sign test 12+/12-  p 1.000
    predSp baseline 0.518  arm 0.501   mean diff -0.016  sign test 10+/14-  p 0.541

### v1-BK-fjcnd02 (2026-09-27 13:11)

`fruit=1,jc=0.8,fruitPerSeed=0.2,gutTicks=0`, seeds 1101-1124, 400000 ticks. Expected: no carrying: fruit gene falls

- worlds 24, meat 26.6%, kill 21.6%, carnSp>0 in 10, preyCl 1.01
- fruit: gene 0.184 -> 0.087 (up in 0 of 24), div 0.146, fruit 21.1%, carried 0.0%

### v1-BL-fc (2026-09-27 15:22)

`fruit=1,fruitPerSeed=0.2`, seeds 1101-1124, 1000000 ticks. Expected: carrying without jc: fruit gene above no-carrying at 1M, settling or rising

- worlds 24, meat 20.8%, kill 16.2%, carnSp>0 in 3, preyCl 0.86, persisting (predK >= 64% of run after bootstrap) 19, exits 13, re-entries 3
- fruit: gene 0.194 -> 0.250 (up in 11 of 24), div 0.181, fruit 28.9%, carried 29.8%
- baseline v1-BL-fnc: worlds 24, meat 18.8%, kill 14.4%, carnSp>0 in 5, preyCl 0.83, persisting (predK >= 64% of run after bootstrap) 15, exits 10, re-entries 5
    pred   baseline 13  arm 20   (+11 / -4)  McNemar p 0.118
    carn   baseline  5  arm  3   (+2 / -4)  McNemar p 0.688
    giant  baseline  0  arm  0   (+0 / -0)  McNemar p 1.000
    dwarf  baseline  0  arm  1   (+1 / -0)  McNemar p 1.000
    meat   baseline 0.188  arm 0.208   mean diff +0.020  sign test 14+/10-  p 0.541
    preyCl baseline 0.831  arm 0.862   mean diff +0.031  sign test 12+/12-  p 1.000
    predCl baseline 3.578  arm 2.497   mean diff -1.081  sign test 10+/14-  p 0.541
    diet   baseline 0.092  arm 0.102   mean diff +0.010  sign test 11+/13-  p 0.839
    polar  baseline 0.033  arm 0.032   mean diff -0.001  sign test 12+/12-  p 1.000
    align  baseline 0.013  arm 0.013   mean diff +0.000  sign test 12+/12-  p 1.000
    preySp baseline 0.324  arm 0.344   mean diff +0.020  sign test 15+/9-  p 0.307
    predSp baseline 0.484  arm 0.530   mean diff +0.046  sign test 12+/12-  p 1.000

### v1-BL-fnc (2026-09-27 15:23)

`fruit=1,fruitPerSeed=0.2,gutTicks=0`, seeds 1101-1124, 1000000 ticks. Expected: no carrying, no jc: fruit gene falls

- worlds 24, meat 18.8%, kill 14.4%, carnSp>0 in 5, preyCl 0.83, persisting (predK >= 64% of run after bootstrap) 15, exits 10, re-entries 5
- fruit: gene 0.184 -> 0.075 (up in 0 of 24), div 0.160, fruit 17.1%, carried 0.0%

### v1-BL-fjc (2026-09-27 16:47)

`fruit=1,jc=0.8,fruitPerSeed=0.2`, seeds 1101-1124, 1000000 ticks. Expected: carrying with jc: as without jc (jc did not matter at 400k)

- worlds 24, meat 20.4%, kill 16.3%, carnSp>0 in 5, preyCl 0.85, persisting (predK >= 64% of run after bootstrap) 19, exits 12, re-entries 8
- fruit: gene 0.200 -> 0.348 (up in 17 of 24), div 0.203, fruit 31.8%, carried 37.5%
- baseline v1-BL-fjnc: worlds 24, meat 21.2%, kill 17.0%, carnSp>0 in 6, preyCl 0.84, persisting (predK >= 64% of run after bootstrap) 19, exits 9, re-entries 3
    pred   baseline 17  arm 16   (+3 / -4)  McNemar p 1.000
    carn   baseline  6  arm  5   (+4 / -5)  McNemar p 1.000
    giant  baseline  0  arm  0   (+0 / -0)  McNemar p 1.000
    dwarf  baseline  0  arm  0   (+0 / -0)  McNemar p 1.000
    meat   baseline 0.212  arm 0.204   mean diff -0.008  sign test 11+/13-  p 0.839
    preyCl baseline 0.840  arm 0.854   mean diff +0.014  sign test 14+/10-  p 0.541
    predCl baseline 2.719  arm 3.482   mean diff +0.764  sign test 13+/11-  p 0.839
    diet   baseline 0.094  arm 0.104   mean diff +0.009  sign test 14+/10-  p 0.541
    polar  baseline 0.032  arm 0.031   mean diff -0.002  sign test 11+/13-  p 0.839
    align  baseline 0.010  arm 0.008   mean diff -0.002  sign test 8+/16-  p 0.152
    preySp baseline 0.303  arm 0.336   mean diff +0.033  sign test 16+/8-  p 0.152
    predSp baseline 0.517  arm 0.495   mean diff -0.022  sign test 13+/11-  p 0.839

### v1-BL-fjnc (2026-09-27 16:47)

`fruit=1,jc=0.8,fruitPerSeed=0.2,gutTicks=0`, seeds 1101-1124, 1000000 ticks. Expected: no carrying, jc: fruit gene falls

- worlds 24, meat 21.2%, kill 17.0%, carnSp>0 in 6, preyCl 0.84, persisting (predK >= 64% of run after bootstrap) 19, exits 9, re-entries 3
- fruit: gene 0.184 -> 0.070 (up in 0 of 24), div 0.156, fruit 15.2%, carried 0.0%

### v1-EG-base-1161 (2026-09-27 16:47)

`defaults`, seeds 1161-1172, 1000000 ticks. Expected: standing replication of the default build at 1M ticks: predators persist in about 3 of 4

- worlds 12, meat 21.5%, kill 17.6%, carnSp>0 in 4, preyCl 0.83, persisting (predK >= 64% of run after bootstrap) 11, exits 2, re-entries 0

### v1-BM-fruit3M (2026-09-27 18:24)

`fruit=1,fruitPerSeed=0.2`, seeds 1201-1212, 3000000 ticks. Expected: over 3M ticks with carrying the fruit gene levels off above 0 or climbs; carried seed a steady share

- worlds 12, meat 13.3%, kill 9.4%, carnSp>0 in 2, preyCl 0.83, persisting (predK >= 64% of run after bootstrap) 7, exits 18, re-entries 12
- fruit: gene 0.196 -> 0.680 (up in 11 of 12), div 0.198, fruit 34.7%, carried 69.5%

### v1-EG-base-1173 (2026-09-27 18:24)

`defaults`, seeds 1173-1184, 1000000 ticks. Expected: standing replication of the default build at 1M ticks: predators persist in about 3 of 4

- worlds 12, meat 17.6%, kill 13.4%, carnSp>0 in 4, preyCl 0.89, persisting (predK >= 64% of run after bootstrap) 9, exits 7, re-entries 6

### v1-BN-default (2026-09-27 18:24)

`defaults`, seeds 1125-1148, 1000000 ticks. Expected: the fruit build's default at 1M: persistence about 2/3 or better; fruit gene rising

- worlds 24, meat 17.8%, kill 13.7%, carnSp>0 in 5, preyCl 0.85, persisting (predK >= 64% of run after bootstrap) 17, exits 19, re-entries 14

### v1-BN-jc (2026-09-27 19:38)

`jc=0.8`, seeds 1125-1148, 1000000 ticks. Expected: jc raises the fruit gene and plant diversity (replicating +0.10 and +0.02); predators unchanged

- worlds 24, meat 20.6%, kill 16.4%, carnSp>0 in 3, preyCl 0.85, persisting (predK >= 64% of run after bootstrap) 19, exits 11, re-entries 6
- baseline v1-BN-default: worlds 24, meat 17.8%, kill 13.7%, carnSp>0 in 5, preyCl 0.85, persisting (predK >= 64% of run after bootstrap) 17, exits 19, re-entries 14
    pred   baseline 13  arm 18   (+8 / -3)  McNemar p 0.227
    carn   baseline  5  arm  3   (+3 / -5)  McNemar p 0.727
    giant  baseline  0  arm  0   (+0 / -0)  McNemar p 1.000
    dwarf  baseline  2  arm  0   (+0 / -2)  McNemar p 0.500
    meat   baseline 0.178  arm 0.206   mean diff +0.027  sign test 15+/9-  p 0.307
    preyCl baseline 0.854  arm 0.853   mean diff -0.001  sign test 12+/12-  p 1.000
    predCl baseline 3.168  arm 2.803   mean diff -0.365  sign test 9+/15-  p 0.307
    diet   baseline 0.090  arm 0.095   mean diff +0.006  sign test 15+/9-  p 0.307
    polar  baseline 0.032  arm 0.030   mean diff -0.002  sign test 10+/14-  p 0.541
    align  baseline 0.009  arm 0.017   mean diff +0.008  sign test 13+/11-  p 0.839
    preySp baseline 0.321  arm 0.318   mean diff -0.002  sign test 15+/9-  p 0.307
    predSp baseline 0.467  arm 0.510   mean diff +0.044  sign test 15+/9-  p 0.307

### v1-EG-base-1185 (2026-09-27 19:38)

`defaults`, seeds 1185-1196, 1000000 ticks. Expected: standing replication of the default build at 1M ticks: predators persist in about 3 of 4

- worlds 12, meat 20.4%, kill 16.4%, carnSp>0 in 4, preyCl 0.90, persisting (predK >= 64% of run after bootstrap) 11, exits 4, re-entries 2

### v1-BO-see1 (2026-09-27 21:09)

`seeFruit=1`, seeds 1101-1124, 1000000 ticks. Expected: grazers turn toward fruit; fruit share of energy up; fruit gene higher; predators unchanged

- worlds 24, meat 21.4%, kill 17.1%, carnSp>0 in 9, preyCl 0.89, persisting (predK >= 64% of run after bootstrap) 20, exits 13, re-entries 5
- fruit: gene 0.195 -> 0.308 (up in 12 of 24), div 0.176, fruit 26.5%, carried 34.5%
- baseline v1-BO-see0: worlds 24, meat 16.3%, kill 12.3%, carnSp>0 in 4, preyCl 0.86, persisting (predK >= 64% of run after bootstrap) 19, exits 12, re-entries 9
    pred   baseline 14  arm 19   (+9 / -4)  McNemar p 0.267
    carn   baseline  4  arm  9   (+7 / -2)  McNemar p 0.180
    giant  baseline  0  arm  0   (+0 / -0)  McNemar p 1.000
    dwarf  baseline  0  arm  3   (+3 / -0)  McNemar p 0.250
    meat   baseline 0.163  arm 0.214   mean diff +0.051  sign test 17+/7-  p 0.064
    preyCl baseline 0.860  arm 0.889   mean diff +0.030  sign test 15+/9-  p 0.307
    predCl baseline 3.482  arm 2.849   mean diff -0.634  sign test 11+/13-  p 0.839
    diet   baseline 0.087  arm 0.098   mean diff +0.012  sign test 14+/10-  p 0.541
    polar  baseline 0.031  arm 0.031   mean diff +0.000  sign test 13+/11-  p 0.839
    align  baseline 0.008  arm 0.010   mean diff +0.003  sign test 16+/8-  p 0.152
    preySp baseline 0.307  arm 0.329   mean diff +0.022  sign test 14+/10-  p 0.541
    predSp baseline 0.437  arm 0.511   mean diff +0.074  sign test 14+/10-  p 0.541

### v1-BO-see0 (2026-09-27 21:09)

`seeFruit=0`, seeds 1101-1124, 1000000 ticks. Expected: baseline on the fruit-sense build

- worlds 24, meat 16.3%, kill 12.3%, carnSp>0 in 4, preyCl 0.86, persisting (predK >= 64% of run after bootstrap) 19, exits 12, re-entries 9
- fruit: gene 0.199 -> 0.436 (up in 21 of 24), div 0.210, fruit 27.3%, carried 46.9%

### v1-EG-base-1197 (2026-09-27 22:10)

`defaults`, seeds 1197-1208, 1000000 ticks. Expected: standing replication of the default build at 1M ticks: predators persist in about 3 of 4

- worlds 12, meat 22.1%, kill 17.9%, carnSp>0 in 4, preyCl 0.87, persisting (predK >= 64% of run after bootstrap) 9, exits 7, re-entries 2
- fruit: gene 0.198 -> 0.350 (up in 6 of 12), div 0.183, fruit 29.8%, carried 39.3%

### v1-BP-3Mdefault (2026-09-27 22:16)

`defaults`, seeds 1213-1224, 3000000 ticks. Expected: current default (fruit, fruit senses) over 3M ticks: fruit gene climbs as in v1-BM-fruit3M; predator comebacks; grazers turn toward fruit late

- worlds 12, meat 14.3%, kill 10.5%, carnSp>0 in 1, preyCl 0.85, persisting (predK >= 64% of run after bootstrap) 8, exits 15, re-entries 12
- fruit: gene 0.199 -> 0.712 (up in 12 of 12), div 0.200, fruit 35.2%, carried 72.4%

### v1-EG-base-1209 (2026-09-27 22:26)

`defaults`, seeds 1209-1220, 1000000 ticks. Expected: standing replication of the default build at 1M ticks: predators persist in about 3 of 4

- worlds 12, meat 18.2%, kill 13.9%, carnSp>0 in 4, preyCl 0.87, persisting (predK >= 64% of run after bootstrap) 9, exits 7, re-entries 3
- fruit: gene 0.200 -> 0.339 (up in 9 of 12), div 0.189, fruit 25.6%, carried 37.3%

### v1-NU-base (2026-09-27 23:36)

`defaults`, seeds 1301-1324, 1000000 ticks. Expected: nutrient loop at 1M, 24 paired seeds. Expect: with it on, plant mass and animals 20-40% lower, soilCV above 0.5 throughout (dung and carcass patches), meat share a few points lower; predator persistence within 4 worlds of base either way (no strong prior). Rich soil (soil0 12) sits between.

- worlds 24, meat 19.2%, kill 14.8%, carnSp>0 in 5, preyCl 0.83, persisting (predK >= 64% of run after bootstrap) 17, exits 12, re-entries 4
- fruit: gene 0.193 -> 0.356 (up in 17 of 24), div 0.187, fruit 28.9%, carried 40.7%

### v1-NU-on (2026-09-27 23:37)

`nutrients=1`, seeds 1301-1324, 1000000 ticks. Expected: nutrient loop at 1M, 24 paired seeds. Expect: with it on, plant mass and animals 20-40% lower, soilCV above 0.5 throughout (dung and carcass patches), meat share a few points lower; predator persistence within 4 worlds of base either way (no strong prior). Rich soil (soil0 12) sits between.

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
    preyCl baseline 0.832  arm 0.690   mean diff -0.142  sign test 2+/22-  p 0.000
    predCl baseline 2.297  arm 2.812   mean diff +0.515  sign test 17+/7-  p 0.064
    diet   baseline 0.099  arm 0.066   mean diff -0.033  sign test 2+/22-  p 0.000
    polar  baseline 0.030  arm 0.032   mean diff +0.002  sign test 18+/6-  p 0.023
    align  baseline 0.010  arm -0.007   mean diff -0.017  sign test 5+/19-  p 0.007
    preySp baseline 0.341  arm 0.361   mean diff +0.020  sign test 18+/6-  p 0.023
    predSp baseline 0.500  arm 0.442   mean diff -0.058  sign test 9+/15-  p 0.307

### v1-NU-rich (2026-09-27 23:37)

`nutrients=1,soil0=12`, seeds 1301-1324, 1000000 ticks. Expected: nutrient loop at 1M, 24 paired seeds. Expect: with it on, plant mass and animals 20-40% lower, soilCV above 0.5 throughout (dung and carcass patches), meat share a few points lower; predator persistence within 4 worlds of base either way (no strong prior). Rich soil (soil0 12) sits between.

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
    preyCl baseline 0.832  arm 0.760   mean diff -0.072  sign test 8+/16-  p 0.152
    predCl baseline 2.297  arm 4.059   mean diff +1.762  sign test 15+/9-  p 0.307
    diet   baseline 0.099  arm 0.091   mean diff -0.007  sign test 13+/11-  p 0.839
    polar  baseline 0.030  arm 0.031   mean diff +0.001  sign test 13+/11-  p 0.839
    align  baseline 0.010  arm 0.008   mean diff -0.002  sign test 12+/12-  p 1.000
    preySp baseline 0.341  arm 0.350   mean diff +0.010  sign test 12+/12-  p 1.000
    predSp baseline 0.500  arm 0.489   mean diff -0.011  sign test 13+/11-  p 0.839

### v1-EG-base-1349 (2026-09-27 23:42)

`defaults`, seeds 1349-1360, 1000000 ticks. Expected: standing replication of the default build at 1M ticks: predators persist in about 3 of 4

- worlds 12, meat 21.3%, kill 17.0%, carnSp>0 in 4, preyCl 0.83, persisting (predK >= 64% of run after bootstrap) 7, exits 5, re-entries 2
- fruit: gene 0.197 -> 0.264 (up in 6 of 12), div 0.179, fruit 30.9%, carried 30.9%

### v1-LE-base (2026-09-28 00:33)

`defaults`, seeds 1361-1384, 1000000 ticks. Expected: baseline for v1-LE-on (the NI 51 / NO 10 build, learning off)

- worlds 24, meat 18.0%, kill 13.6%, carnSp>0 in 7, preyCl 0.89, persisting (predK >= 64% of run after bootstrap) 17, exits 16, re-entries 8
- fruit: gene 0.192 -> 0.327 (up in 15 of 24), div 0.193, fruit 24.0%, carried 38.1%

### v1-SM-base (2026-09-28 00:33)

`defaults`, seeds 1325-1348, 1000000 ticks. Expected: baseline for v1-SM-on (the NI 50 build)

- worlds 24, meat 19.4%, kill 15.4%, carnSp>0 in 5, preyCl 0.86, persisting (predK >= 64% of run after bootstrap) 18, exits 11, re-entries 4
- fruit: gene 0.194 -> 0.310 (up in 13 of 24), div 0.184, fruit 26.5%, carried 34.4%

### v1-SM-on (2026-09-28 00:39)

`smell=1`, seeds 1325-1348, 1000000 ticks. Expected: smell at 1M, 24 paired seeds. Expect: kill share and meat share up a few points (carrion and prey scent lead hunters to food), prey clumping up if prey use scent to keep together or to avoid hunters, predator persistence at least as often as base. A null here means smell is not worth its 8 inputs.

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
    preyCl baseline 0.863  arm 0.926   mean diff +0.063  sign test 17+/7-  p 0.064
    predCl baseline 3.519  arm 2.581   mean diff -0.937  sign test 13+/11-  p 0.839
    diet   baseline 0.093  arm 0.090   mean diff -0.003  sign test 12+/12-  p 1.000
    polar  baseline 0.031  arm 0.031   mean diff -0.000  sign test 13+/11-  p 0.839
    align  baseline 0.007  arm 0.069   mean diff +0.063  sign test 21+/3-  p 0.000
    preySp baseline 0.319  arm 0.357   mean diff +0.038  sign test 17+/7-  p 0.064
    predSp baseline 0.481  arm 0.620   mean diff +0.139  sign test 17+/7-  p 0.064

### v1-EG-base-1385 (2026-09-28 01:21)

`defaults`, seeds 1385-1396, 1000000 ticks. Expected: standing replication of the default build at 1M ticks: predators persist in about 3 of 4

- worlds 12, meat 20.2%, kill 15.9%, carnSp>0 in 4, preyCl 0.87, persisting (predK >= 64% of run after bootstrap) 11, exits 4, re-entries 1
- fruit: gene 0.192 -> 0.321 (up in 8 of 12), div 0.185, fruit 27.2%, carried 35.6%

### v1-EG-base-1397 (2026-09-28 01:21)

`defaults`, seeds 1397-1408, 1000000 ticks. Expected: standing replication of the default build at 1M ticks: predators persist in about 3 of 4

- worlds 12, meat 19.8%, kill 15.7%, carnSp>0 in 3, preyCl 0.89, persisting (predK >= 64% of run after bootstrap) 9, exits 4, re-entries 2
- fruit: gene 0.198 -> 0.287 (up in 6 of 12), div 0.178, fruit 23.1%, carried 33.6%

### v1-LE-on (2026-09-28 01:22)

`learn=1`, seeds 1361-1384, 1000000 ticks. Expected: lifetime learning at 1M, 24 paired seeds. Expect: learnM above the base arm's drift of the same (unused) output if selection favours learning; weights of adults moved from their genome (learnMoved over 0.1); behaviour: kill share and meat share up a few points (hunters improve with practice), bootstrap somewhat slower; predator persistence within 4 worlds of base. A learnM at or below drift means evolution switches learning off.

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
    preyCl baseline 0.887  arm 1.077   mean diff +0.190  sign test 21+/3-  p 0.000
    predCl baseline 2.217  arm 4.358   mean diff +2.142  sign test 18+/6-  p 0.023
    diet   baseline 0.087  arm 0.077   mean diff -0.010  sign test 8+/16-  p 0.152
    polar  baseline 0.032  arm 0.036   mean diff +0.003  sign test 21+/3-  p 0.000
    align  baseline 0.004  arm 0.017   mean diff +0.013  sign test 11+/13-  p 0.839
    preySp baseline 0.313  arm 0.262   mean diff -0.051  sign test 5+/19-  p 0.007
    predSp baseline 0.481  arm 0.292   mean diff -0.190  sign test 1+/23-  p 0.000
    learnM baseline 0.875  arm 0.879   mean diff +0.004  sign test 9+/15-  p 0.307

### v1-EG-base-1409 (2026-09-28 01:43)

`defaults`, seeds 1409-1420, 1000000 ticks. Expected: standing replication of the default build at 1M ticks: predators persist in about 3 of 4

- worlds 12, meat 22.0%, kill 18.0%, carnSp>0 in 3, preyCl 0.91, persisting (predK >= 64% of run after bootstrap) 10, exits 5, re-entries 4
- fruit: gene 0.201 -> 0.218 (up in 5 of 12), div 0.161, fruit 26.6%, carried 23.4%

### v1-EG-base-1421 (2026-09-28 01:43)

`defaults`, seeds 1421-1432, 1000000 ticks. Expected: standing replication of the default build at 1M ticks: predators persist in about 3 of 4

- worlds 12, meat 20.7%, kill 16.2%, carnSp>0 in 1, preyCl 0.90, persisting (predK >= 64% of run after bootstrap) 10, exits 4, re-entries 2
- fruit: gene 0.197 -> 0.257 (up in 5 of 12), div 0.190, fruit 25.3%, carried 30.5%

### v1-EG-base-1433 (2026-09-28 02:19)

`defaults`, seeds 1433-1444, 1000000 ticks. Expected: standing replication of the default build at 1M ticks: predators persist in about 3 of 4

- worlds 12, meat 21.3%, kill 17.3%, carnSp>0 in 3, preyCl 0.93, persisting (predK >= 64% of run after bootstrap) 8, exits 7, re-entries 5
- fruit: gene 0.197 -> 0.299 (up in 6 of 12), div 0.177, fruit 22.1%, carried 32.0%

### v1-EG-base-1445 (2026-09-28 02:19)

`defaults`, seeds 1445-1456, 1000000 ticks. Expected: standing replication of the default build at 1M ticks: predators persist in about 3 of 4

- worlds 12, meat 20.2%, kill 16.2%, carnSp>0 in 4, preyCl 0.82, persisting (predK >= 64% of run after bootstrap) 11, exits 6, re-entries 4
- fruit: gene 0.199 -> 0.357 (up in 10 of 12), div 0.183, fruit 28.6%, carried 37.4%

### v1-NU-s24 (2026-09-28 02:19)

`nutrients=1,soil0=24`, seeds 1361-1384, 1000000 ticks. Expected: nutrient loop with abundant nutrient, 24 seeds paired with v1-LE-base (same build and defaults). At soil0 6 predator worlds fell 19 -> 7 because 78% of the nutrient idles in the soil and plant mass drops to a third. Expect: soil0 24 predator worlds within 3 of base and plant mass within 25%; soil0 48 same as base; soilCV above 0.5 in both (dung and carcass patches still form).

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
    preyCl baseline 0.887  arm 0.783   mean diff -0.104  sign test 7+/17-  p 0.064
    predCl baseline 2.217  arm 3.027   mean diff +0.811  sign test 15+/9-  p 0.307
    diet   baseline 0.087  arm 0.086   mean diff -0.001  sign test 12+/12-  p 1.000
    polar  baseline 0.032  arm 0.032   mean diff -0.000  sign test 13+/11-  p 0.839
    align  baseline 0.004  arm 0.016   mean diff +0.012  sign test 17+/7-  p 0.064
    preySp baseline 0.313  arm 0.341   mean diff +0.028  sign test 12+/12-  p 1.000
    predSp baseline 0.481  arm 0.492   mean diff +0.010  sign test 11+/13-  p 0.839
    learnM baseline 0.875  arm 0.877   mean diff +0.002  sign test 11+/13-  p 0.839

### v1-EG-base-1457 (2026-09-28 02:45)

`defaults`, seeds 1457-1468, 1000000 ticks. Expected: standing replication of the default build at 1M ticks: predators persist in about 3 of 4

- worlds 12, meat 19.7%, kill 14.9%, carnSp>0 in 6, preyCl 0.89, persisting (predK >= 64% of run after bootstrap) 8, exits 9, re-entries 4
- fruit: gene 0.195 -> 0.305 (up in 7 of 12), div 0.207, fruit 21.9%, carried 40.5%

### v1-NU-s48 (2026-09-28 02:45)

`nutrients=1,soil0=48`, seeds 1361-1384, 1000000 ticks. Expected: nutrient loop with abundant nutrient, 24 seeds paired with v1-LE-base (same build and defaults). At soil0 6 predator worlds fell 19 -> 7 because 78% of the nutrient idles in the soil and plant mass drops to a third. Expect: soil0 24 predator worlds within 3 of base and plant mass within 25%; soil0 48 same as base; soilCV above 0.5 in both (dung and carcass patches still form).

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
    preyCl baseline 0.887  arm 0.860   mean diff -0.027  sign test 11+/13-  p 0.839
    predCl baseline 2.217  arm 3.380   mean diff +1.163  sign test 15+/9-  p 0.307
    diet   baseline 0.087  arm 0.085   mean diff -0.002  sign test 11+/13-  p 0.839
    polar  baseline 0.032  arm 0.030   mean diff -0.002  sign test 12+/12-  p 1.000
    align  baseline 0.004  arm 0.014   mean diff +0.010  sign test 13+/11-  p 0.839
    preySp baseline 0.313  arm 0.308   mean diff -0.005  sign test 12+/12-  p 1.000
    predSp baseline 0.481  arm 0.443   mean diff -0.038  sign test 10+/14-  p 0.541
    learnM baseline 0.875  arm 0.877   mean diff +0.002  sign test 11+/13-  p 0.839

### v1-EG-base-1469 (2026-09-28 03:42)

`defaults`, seeds 1469-1480, 1000000 ticks. Expected: standing replication of the default build at 1M ticks: predators persist in about 3 of 4

- worlds 12, meat 17.4%, kill 13.1%, carnSp>0 in 6, preyCl 0.89, persisting (predK >= 64% of run after bootstrap) 11, exits 5, re-entries 1
- fruit: gene 0.193 -> 0.275 (up in 6 of 12), div 0.189, fruit 22.6%, carried 34.9%

### v1-EG-base-1481 (2026-09-28 03:42)

`defaults`, seeds 1481-1492, 1000000 ticks. Expected: standing replication of the default build at 1M ticks: predators persist in about 3 of 4

- worlds 12, meat 18.6%, kill 14.4%, carnSp>0 in 5, preyCl 0.87, persisting (predK >= 64% of run after bootstrap) 9, exits 6, re-entries 2
- fruit: gene 0.193 -> 0.327 (up in 9 of 12), div 0.202, fruit 23.8%, carried 37.6%

### v1-EG-base-1493 (2026-09-28 03:42)

`defaults`, seeds 1493-1504, 1000000 ticks. Expected: standing replication of the default build at 1M ticks: predators persist in about 3 of 4

- worlds 12, meat 15.3%, kill 11.0%, carnSp>0 in 3, preyCl 0.84, persisting (predK >= 64% of run after bootstrap) 8, exits 7, re-entries 3
- fruit: gene 0.203 -> 0.307 (up in 8 of 12), div 0.201, fruit 21.9%, carried 39.6%

### v1-EG-base-1505 (2026-09-28 04:03)

`defaults`, seeds 1505-1516, 1000000 ticks. Expected: standing replication of the default build at 1M ticks: predators persist in about 3 of 4

- worlds 12, meat 16.6%, kill 12.2%, carnSp>0 in 1, preyCl 0.93, persisting (predK >= 64% of run after bootstrap) 7, exits 5, re-entries 2
- fruit: gene 0.193 -> 0.377 (up in 9 of 12), div 0.213, fruit 27.5%, carried 45.8%

### v1-EG-base-1517 (2026-09-28 04:03)

`defaults`, seeds 1517-1528, 1000000 ticks. Expected: standing replication of the default build at 1M ticks: predators persist in about 3 of 4

- worlds 12, meat 21.8%, kill 17.1%, carnSp>0 in 4, preyCl 0.98, persisting (predK >= 64% of run after bootstrap) 12, exits 3, re-entries 1
- fruit: gene 0.201 -> 0.203 (up in 3 of 12), div 0.170, fruit 27.3%, carried 24.2%

### v1-EG-base-1529 (2026-09-28 04:03)

`defaults`, seeds 1529-1540, 1000000 ticks. Expected: standing replication of the default build at 1M ticks: predators persist in about 3 of 4

- worlds 12, meat 19.1%, kill 14.5%, carnSp>0 in 4, preyCl 0.95, persisting (predK >= 64% of run after bootstrap) 11, exits 5, re-entries 4
- fruit: gene 0.198 -> 0.245 (up in 4 of 12), div 0.190, fruit 22.7%, carried 34.5%

### v1-EG-base-1541 (2026-09-28 04:03)

`defaults`, seeds 1541-1552, 1000000 ticks. Expected: standing replication of the default build at 1M ticks: predators persist in about 3 of 4

- worlds 12, meat 18.4%, kill 13.3%, carnSp>0 in 5, preyCl 0.90, persisting (predK >= 64% of run after bootstrap) 8, exits 6, re-entries 3
- fruit: gene 0.193 -> 0.295 (up in 7 of 12), div 0.204, fruit 26.6%, carried 37.3%

### v1-NU24-1457 (2026-09-28 04:03)

`nutrients=1,soil0=24`, seeds 1457-1468, 1000000 ticks. Expected: nutrient loop at soil0 24 on the smell default, paired with the standing block of the same seeds (same build). Expect as v1-NU-s24 against v1-LE-base: predator worlds within 3 of the block, plant mass within 25%, soilCV above 0.5. If so, the loop goes on by default at soil0 24.

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
    preyCl baseline 0.893  arm 0.765   mean diff -0.129  sign test 2+/10-  p 0.039
    predCl baseline 3.467  arm 2.162   mean diff -1.305  sign test 4+/8-  p 0.388
    diet   baseline 0.101  arm 0.083   mean diff -0.018  sign test 4+/8-  p 0.388
    polar  baseline 0.031  arm 0.032   mean diff +0.001  sign test 9+/3-  p 0.146
    align  baseline 0.042  arm 0.058   mean diff +0.016  sign test 9+/3-  p 0.146
    preySp baseline 0.315  arm 0.355   mean diff +0.039  sign test 9+/3-  p 0.146
    predSp baseline 0.467  arm 0.512   mean diff +0.044  sign test 8+/4-  p 0.388
    learnM baseline 0.880  arm 0.901   mean diff +0.021  sign test 7+/5-  p 0.774

### v1-EG-base-1553 (2026-09-28 04:45)

`defaults`, seeds 1553-1564, 1000000 ticks. Expected: standing replication of the default build at 1M ticks: predators persist in about 3 of 4

- worlds 12, meat 17.2%, kill 12.2%, carnSp>0 in 4, preyCl 0.92, persisting (predK >= 64% of run after bootstrap) 8, exits 7, re-entries 2
- fruit: gene 0.186 -> 0.267 (up in 8 of 12), div 0.183, fruit 25.7%, carried 37.7%

### v1-NU24-1469 (2026-09-28 04:45)

`nutrients=1,soil0=24`, seeds 1469-1480, 1000000 ticks. Expected: nutrient loop at soil0 24 on the smell default, paired with the standing block of the same seeds (same build). Expect as v1-NU-s24 against v1-LE-base: predator worlds within 3 of the block, plant mass within 25%, soilCV above 0.5. If so, the loop goes on by default at soil0 24.

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
    preyCl baseline 0.889  arm 0.758   mean diff -0.130  sign test 3+/9-  p 0.146
    predCl baseline 2.733  arm 2.860   mean diff +0.127  sign test 7+/5-  p 0.774
    diet   baseline 0.094  arm 0.084   mean diff -0.010  sign test 4+/8-  p 0.388
    polar  baseline 0.033  arm 0.032   mean diff -0.001  sign test 5+/7-  p 0.774
    align  baseline 0.072  arm 0.027   mean diff -0.045  sign test 4+/8-  p 0.388
    preySp baseline 0.335  arm 0.357   mean diff +0.022  sign test 9+/3-  p 0.146
    predSp baseline 0.551  arm 0.514   mean diff -0.037  sign test 5+/7-  p 0.774
    learnM baseline 0.895  arm 0.873   mean diff -0.021  sign test 4+/8-  p 0.388

### v1-EG-base-1565 (2026-09-28 05:37)

`defaults`, seeds 1565-1576, 1000000 ticks. Expected: standing replication of the default build at 1M ticks: predators persist in about 3 of 4

- worlds 12, meat 24.5%, kill 20.0%, carnSp>0 in 7, preyCl 0.92, persisting (predK >= 64% of run after bootstrap) 11, exits 4, re-entries 3
- fruit: gene 0.197 -> 0.268 (up in 5 of 12), div 0.178, fruit 30.8%, carried 29.7%

### v1-EG-base-1577 (2026-09-28 05:37)

`defaults`, seeds 1577-1588, 1000000 ticks. Expected: standing replication of the default build at 1M ticks: predators persist in about 3 of 4

- worlds 12, meat 22.3%, kill 17.7%, carnSp>0 in 7, preyCl 0.99, persisting (predK >= 64% of run after bootstrap) 9, exits 4, re-entries 1
- fruit: gene 0.193 -> 0.220 (up in 4 of 12), div 0.180, fruit 28.5%, carried 26.2%

### v1-EG-base-1589 (2026-09-28 05:37)

`defaults`, seeds 1589-1600, 1000000 ticks. Expected: standing replication of the default build at 1M ticks: predators persist in about 3 of 4

- worlds 12, meat 17.3%, kill 12.8%, carnSp>0 in 3, preyCl 0.85, persisting (predK >= 64% of run after bootstrap) 9, exits 8, re-entries 1
- fruit: gene 0.191 -> 0.246 (up in 7 of 12), div 0.196, fruit 20.2%, carried 32.6%

### v1-EG-base-1601 (2026-09-28 05:38)

`defaults`, seeds 1601-1612, 1000000 ticks. Expected: standing replication of the default build at 1M ticks: predators persist in about 3 of 4

- worlds 12, meat 13.8%, kill 9.2%, carnSp>0 in 5, preyCl 0.87, persisting (predK >= 64% of run after bootstrap) 7, exits 7, re-entries 3
- fruit: gene 0.191 -> 0.314 (up in 8 of 12), div 0.221, fruit 21.9%, carried 39.2%

### v1-EG-base-1637 (2026-09-28 05:38)

`defaults`, seeds 1637-1648, 1000000 ticks. Expected: standing replication of the default build at 1M ticks: predators persist in about 3 of 4

- worlds 12, meat 22.5%, kill 17.4%, carnSp>0 in 6, preyCl 0.89, persisting (predK >= 64% of run after bootstrap) 10, exits 6, re-entries 2
- fruit: gene 0.195 -> 0.272 (up in 6 of 12), div 0.176, fruit 31.1%, carried 31.9%

### v1-EG-base-1625 (2026-09-28 06:04)

`defaults`, seeds 1625-1636, 1000000 ticks. Expected: standing replication of the default build at 1M ticks: predators persist in about 3 of 4

- worlds 12, meat 21.6%, kill 17.0%, carnSp>0 in 4, preyCl 0.97, persisting (predK >= 64% of run after bootstrap) 11, exits 5, re-entries 1
- fruit: gene 0.193 -> 0.278 (up in 7 of 12), div 0.168, fruit 25.6%, carried 33.3%

### v1-EG-base-1649 (2026-09-28 07:05)

`defaults`, seeds 1649-1660, 1000000 ticks. Expected: standing replication of the default build at 1M ticks: predators persist in about 3 of 4

- worlds 12, meat 17.9%, kill 12.7%, carnSp>0 in 6, preyCl 0.91, persisting (predK >= 64% of run after bootstrap) 10, exits 7, re-entries 2
- fruit: gene 0.195 -> 0.261 (up in 8 of 12), div 0.200, fruit 22.7%, carried 35.0%

### v1-EG-base-1661 (2026-09-28 07:05)

`defaults`, seeds 1661-1672, 1000000 ticks. Expected: standing replication of the default build at 1M ticks: predators persist in about 3 of 4

- worlds 12, meat 21.6%, kill 16.6%, carnSp>0 in 8, preyCl 0.89, persisting (predK >= 64% of run after bootstrap) 11, exits 4, re-entries 3
- fruit: gene 0.189 -> 0.248 (up in 5 of 12), div 0.188, fruit 22.3%, carried 30.8%

### v1-EG-base-1673 (2026-09-28 07:05)

`defaults`, seeds 1673-1684, 1000000 ticks. Expected: standing replication of the default build at 1M ticks: predators persist in about 3 of 4

- worlds 12, meat 11.6%, kill 7.0%, carnSp>0 in 3, preyCl 0.84, persisting (predK >= 64% of run after bootstrap) 5, exits 8, re-entries 2
- fruit: gene 0.196 -> 0.360 (up in 11 of 12), div 0.229, fruit 23.0%, carried 44.5%

### v1-SD02-1649 (2026-09-28 07:05)

`smellDecay=0.02`, seeds 1649-1660, 1000000 ticks. Expected: scent that lasts longer (smellDecay 0.02, about 50 ticks, against 0.05), paired with the standing block of the same seeds. Expect: grazers steer off older trails, so alignment rises (above the block's in 8 of 12) and prey spread further; predators within 2 of the block. If alignment falls, fresh scent carries the information and old trails are noise.

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
    preyCl baseline 0.912  arm 0.899   mean diff -0.012  sign test 5+/7-  p 0.774
    predCl baseline 2.135  arm 2.753   mean diff +0.618  sign test 9+/3-  p 0.146
    diet   baseline 0.102  arm 0.093   mean diff -0.008  sign test 6+/6-  p 1.000
    polar  baseline 0.032  arm 0.033   mean diff +0.000  sign test 6+/6-  p 1.000
    align  baseline 0.053  arm 0.031   mean diff -0.021  sign test 5+/7-  p 0.774
    preySp baseline 0.331  arm 0.317   mean diff -0.014  sign test 6+/6-  p 1.000
    predSp baseline 0.499  arm 0.524   mean diff +0.025  sign test 6+/6-  p 1.000
    learnM baseline 0.876  arm 0.902   mean diff +0.026  sign test 7+/5-  p 0.774

### v1-EG-base-1685 (2026-09-28 07:11)

`defaults`, seeds 1685-1696, 1000000 ticks. Expected: standing replication of the default build at 1M ticks: predators persist in about 3 of 4

- worlds 12, meat 17.1%, kill 12.5%, carnSp>0 in 4, preyCl 0.88, persisting (predK >= 64% of run after bootstrap) 8, exits 6, re-entries 2
- fruit: gene 0.193 -> 0.272 (up in 9 of 12), div 0.203, fruit 25.9%, carried 35.9%

### v1-SD02-1661 (2026-09-28 07:21)

`smellDecay=0.02`, seeds 1661-1672, 1000000 ticks. Expected: scent that lasts longer (smellDecay 0.02, about 50 ticks, against 0.05), paired with the standing block of the same seeds. Expect: grazers steer off older trails, so alignment rises (above the block's in 8 of 12) and prey spread further; predators within 2 of the block. If alignment falls, fresh scent carries the information and old trails are noise.

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
    preyCl baseline 0.896  arm 0.908   mean diff +0.011  sign test 6+/6-  p 1.000
    predCl baseline 2.053  arm 2.453   mean diff +0.400  sign test 10+/2-  p 0.039
    diet   baseline 0.102  arm 0.093   mean diff -0.009  sign test 5+/7-  p 0.774
    polar  baseline 0.033  arm 0.031   mean diff -0.002  sign test 3+/9-  p 0.146
    align  baseline 0.070  arm 0.047   mean diff -0.022  sign test 5+/7-  p 0.774
    preySp baseline 0.354  arm 0.346   mean diff -0.008  sign test 7+/5-  p 0.774
    predSp baseline 0.606  arm 0.624   mean diff +0.019  sign test 7+/5-  p 0.774
    learnM baseline 0.896  arm 0.910   mean diff +0.014  sign test 6+/6-  p 1.000

### v1-EG-base-1697 (2026-09-28 08:30)

`defaults`, seeds 1697-1708, 1000000 ticks. Expected: standing replication of the default build at 1M ticks: predators persist in about 3 of 4

- worlds 12, meat 17.2%, kill 12.5%, carnSp>0 in 7, preyCl 0.92, persisting (predK >= 64% of run after bootstrap) 9, exits 5, re-entries 1
- fruit: gene 0.198 -> 0.291 (up in 7 of 12), div 0.205, fruit 25.0%, carried 35.8%

### v1-EG-base-1709 (2026-09-28 08:30)

`defaults`, seeds 1709-1720, 1000000 ticks. Expected: standing replication of the default build at 1M ticks: predators persist in about 3 of 4

- worlds 12, meat 17.7%, kill 12.9%, carnSp>0 in 3, preyCl 0.91, persisting (predK >= 64% of run after bootstrap) 9, exits 7, re-entries 2
- fruit: gene 0.202 -> 0.272 (up in 8 of 12), div 0.205, fruit 23.6%, carried 36.5%

### v1-EG-base-1721 (2026-09-28 08:30)

`defaults`, seeds 1721-1732, 1000000 ticks. Expected: standing replication of the default build at 1M ticks: predators persist in about 3 of 4

- worlds 12, meat 16.4%, kill 12.0%, carnSp>0 in 4, preyCl 0.83, persisting (predK >= 64% of run after bootstrap) 9, exits 5, re-entries 2
- fruit: gene 0.200 -> 0.349 (up in 8 of 12), div 0.193, fruit 26.9%, carried 41.8%

### v1-EG-base-1733 (2026-09-28 08:30)

`defaults`, seeds 1733-1744, 1000000 ticks. Expected: standing replication of the default build at 1M ticks: predators persist in about 3 of 4

- worlds 12, meat 18.1%, kill 13.0%, carnSp>0 in 4, preyCl 0.90, persisting (predK >= 64% of run after bootstrap) 8, exits 7, re-entries 5
- fruit: gene 0.195 -> 0.360 (up in 7 of 12), div 0.214, fruit 28.6%, carried 41.0%

### v1-EG-base-1745 (2026-09-28 08:31)

`defaults`, seeds 1745-1756, 1000000 ticks. Expected: standing replication of the default build at 1M ticks: predators persist in about 3 of 4

- worlds 12, meat 18.4%, kill 14.0%, carnSp>0 in 3, preyCl 0.87, persisting (predK >= 64% of run after bootstrap) 10, exits 7, re-entries 3
- fruit: gene 0.196 -> 0.342 (up in 6 of 12), div 0.202, fruit 26.3%, carried 41.1%

### v1-EG-base-1757 (2026-09-28 08:31)

`defaults`, seeds 1757-1768, 1000000 ticks. Expected: standing replication of the default build at 1M ticks: predators persist in about 3 of 4

- worlds 12, meat 18.4%, kill 13.8%, carnSp>0 in 5, preyCl 0.96, persisting (predK >= 64% of run after bootstrap) 10, exits 6, re-entries 2
- fruit: gene 0.196 -> 0.274 (up in 7 of 12), div 0.202, fruit 24.5%, carried 35.5%

### v1-SM-3M (2026-09-28 09:10)

`defaults`, seeds 1613-1624, 3000000 ticks. Expected: the smell default over 3M ticks. Expect: alignment keeps rising past 1M (above 0.08 in the last third), predators come and go as in v1-BP-3Mdefault (persisting in about 8 of 12), fruit gene near 0.7.

- worlds 12, meat 14.5%, kill 10.1%, carnSp>0 in 4, preyCl 0.86, persisting (predK >= 64% of run after bootstrap) 7, exits 22, re-entries 18
- fruit: gene 0.195 -> 0.558 (up in 12 of 12), div 0.220, fruit 28.5%, carried 59.4%

### v1-EG-base-1769 (2026-09-28 09:10)

`defaults`, seeds 1769-1780, 1000000 ticks. Expected: standing replication of the default build at 1M ticks: predators persist in about 3 of 4

- worlds 12, meat 17.2%, kill 12.7%, carnSp>0 in 4, preyCl 0.90, persisting (predK >= 64% of run after bootstrap) 8, exits 12, re-entries 7
- fruit: gene 0.191 -> 0.285 (up in 7 of 12), div 0.210, fruit 22.4%, carried 36.1%

### v1-EG-base-1781 (2026-09-28 09:10)

`defaults`, seeds 1781-1792, 1000000 ticks. Expected: standing replication of the default build at 1M ticks: predators persist in about 3 of 4

- worlds 12, meat 20.0%, kill 15.0%, carnSp>0 in 6, preyCl 0.93, persisting (predK >= 64% of run after bootstrap) 7, exits 6, re-entries 2
- fruit: gene 0.197 -> 0.229 (up in 5 of 12), div 0.186, fruit 29.4%, carried 27.4%

### v1-EG-base-1793 (2026-09-28 09:10)

`defaults`, seeds 1793-1804, 1000000 ticks. Expected: standing replication of the default build at 1M ticks: predators persist in about 3 of 4

- worlds 12, meat 16.4%, kill 11.7%, carnSp>0 in 3, preyCl 0.89, persisting (predK >= 64% of run after bootstrap) 8, exits 9, re-entries 4
- fruit: gene 0.194 -> 0.286 (up in 8 of 12), div 0.213, fruit 24.2%, carried 38.9%

### v1-EG-base-1805 (2026-09-28 09:52)

`defaults`, seeds 1805-1816, 1000000 ticks. Expected: standing replication of the default build at 1M ticks: predators persist in about 3 of 4

- worlds 12, meat 14.5%, kill 9.8%, carnSp>0 in 1, preyCl 0.85, persisting (predK >= 64% of run after bootstrap) 5, exits 12, re-entries 5
- fruit: gene 0.187 -> 0.289 (up in 9 of 12), div 0.202, fruit 21.1%, carried 40.2%

### v1-EG-base-1817 (2026-09-28 09:52)

`defaults`, seeds 1817-1828, 1000000 ticks. Expected: standing replication of the default build at 1M ticks: predators persist in about 3 of 4

- worlds 12, meat 18.2%, kill 13.6%, carnSp>0 in 6, preyCl 0.93, persisting (predK >= 64% of run after bootstrap) 7, exits 7, re-entries 2
- fruit: gene 0.197 -> 0.316 (up in 7 of 12), div 0.197, fruit 29.7%, carried 38.0%

### v1-EG-base-1829 (2026-09-28 09:53)

`defaults`, seeds 1829-1840, 1000000 ticks. Expected: standing replication of the default build at 1M ticks: predators persist in about 3 of 4

- worlds 12, meat 18.7%, kill 13.9%, carnSp>0 in 3, preyCl 0.93, persisting (predK >= 64% of run after bootstrap) 9, exits 6, re-entries 1
- fruit: gene 0.196 -> 0.278 (up in 7 of 12), div 0.201, fruit 29.5%, carried 33.8%

### v1-EG-base-1841 (2026-09-28 10:29)

`defaults`, seeds 1841-1852, 1000000 ticks. Expected: standing replication of the default build at 1M ticks: predators persist in about 3 of 4

- worlds 12, meat 12.9%, kill 8.3%, carnSp>0 in 1, preyCl 0.89, persisting (predK >= 64% of run after bootstrap) 6, exits 9, re-entries 3
- fruit: gene 0.200 -> 0.312 (up in 8 of 12), div 0.225, fruit 22.6%, carried 40.7%

### v1-EG-base-1865 (2026-09-28 10:29)

`defaults`, seeds 1865-1876, 1000000 ticks. Expected: standing replication of the default build at 1M ticks: predators persist in about 3 of 4

- worlds 12, meat 18.5%, kill 14.0%, carnSp>0 in 2, preyCl 0.93, persisting (predK >= 64% of run after bootstrap) 10, exits 5, re-entries 1
- fruit: gene 0.190 -> 0.335 (up in 8 of 12), div 0.208, fruit 26.2%, carried 41.5%

### v1-SD10-1841 (2026-09-28 10:29)

`smellDecay=0.1`, seeds 1841-1852, 1000000 ticks. Expected: shorter-lived scent (smellDecay 0.1, about 10 ticks, against 0.05), paired with the standing block of the same seeds. Longer scent (0.02) lowered alignment in both halves (0.039 against 0.062 pooled, n.s.), so fresh scent seems to carry the signal. Expect: alignment above the block's in 8 of 12 or more; predators within 2 of the block. If it also falls, 0.05 is near the best lifetime.

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
    preyCl baseline 0.888  arm 0.863   mean diff -0.026  sign test 6+/6-  p 1.000
    predCl baseline 3.617  arm 2.806   mean diff -0.810  sign test 5+/7-  p 0.774
    diet   baseline 0.080  arm 0.101   mean diff +0.021  sign test 11+/1-  p 0.006
    polar  baseline 0.031  arm 0.031   mean diff +0.001  sign test 6+/6-  p 1.000
    align  baseline 0.054  arm 0.074   mean diff +0.019  sign test 8+/4-  p 0.388
    preySp baseline 0.315  arm 0.344   mean diff +0.029  sign test 8+/4-  p 0.388
    predSp baseline 0.469  arm 0.535   mean diff +0.067  sign test 9+/3-  p 0.146
    learnM baseline 0.881  arm 0.879   mean diff -0.002  sign test 3+/9-  p 0.146

### v1-EG-base-1853 (2026-09-28 10:30)

`defaults`, seeds 1853-1864, 1000000 ticks. Expected: standing replication of the default build at 1M ticks: predators persist in about 3 of 4

- worlds 12, meat 16.7%, kill 12.2%, carnSp>0 in 5, preyCl 0.91, persisting (predK >= 64% of run after bootstrap) 7, exits 7, re-entries 3
- fruit: gene 0.199 -> 0.336 (up in 9 of 12), div 0.216, fruit 22.7%, carried 40.9%

### v1-EG-base-1877 (2026-09-28 11:21)

`defaults`, seeds 1877-1888, 1000000 ticks. Expected: standing replication of the default build at 1M ticks: predators persist in about 3 of 4

- worlds 12, meat 17.7%, kill 13.0%, carnSp>0 in 4, preyCl 0.90, persisting (predK >= 64% of run after bootstrap) 9, exits 6, re-entries 4
- fruit: gene 0.190 -> 0.325 (up in 7 of 12), div 0.198, fruit 29.0%, carried 38.3%

### v1-EG-base-1889 (2026-09-28 11:21)

`defaults`, seeds 1889-1900, 1000000 ticks. Expected: standing replication of the default build at 1M ticks: predators persist in about 3 of 4

- worlds 12, meat 15.4%, kill 10.8%, carnSp>0 in 3, preyCl 0.89, persisting (predK >= 64% of run after bootstrap) 8, exits 11, re-entries 6
- fruit: gene 0.199 -> 0.342 (up in 8 of 12), div 0.215, fruit 24.3%, carried 43.9%

### v1-SD10-1853 (2026-09-28 11:21)

`smellDecay=0.1`, seeds 1853-1864, 1000000 ticks. Expected: shorter-lived scent (smellDecay 0.1, about 10 ticks, against 0.05), paired with the standing block of the same seeds. Longer scent (0.02) lowered alignment in both halves (0.039 against 0.062 pooled, n.s.), so fresh scent seems to carry the signal. Expect: alignment above the block's in 8 of 12 or more; predators within 2 of the block. If it also falls, 0.05 is near the best lifetime.

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
    preyCl baseline 0.914  arm 0.884   mean diff -0.030  sign test 6+/6-  p 1.000
    predCl baseline 2.986  arm 2.714   mean diff -0.272  sign test 5+/7-  p 0.774
    diet   baseline 0.085  arm 0.098   mean diff +0.013  sign test 7+/5-  p 0.774
    polar  baseline 0.031  arm 0.032   mean diff +0.001  sign test 8+/4-  p 0.388
    align  baseline 0.058  arm 0.084   mean diff +0.026  sign test 8+/4-  p 0.388
    preySp baseline 0.316  arm 0.336   mean diff +0.020  sign test 7+/5-  p 0.774
    predSp baseline 0.528  arm 0.575   mean diff +0.047  sign test 8+/4-  p 0.388
    learnM baseline 0.889  arm 0.879   mean diff -0.011  sign test 4+/8-  p 0.388

### v1-EG-base-1913 (2026-09-28 12:23)

`defaults`, seeds 1913-1924, 1000000 ticks. Expected: standing replication of the default build at 1M ticks: predators persist in about 3 of 4

- worlds 12, meat 15.9%, kill 11.7%, carnSp>0 in 2, preyCl 0.81, persisting (predK >= 64% of run after bootstrap) 8, exits 6, re-entries 2
- fruit: gene 0.199 -> 0.344 (up in 9 of 12), div 0.216, fruit 24.5%, carried 41.4%

### v1-EG-base-1925 (2026-09-28 12:23)

`defaults`, seeds 1925-1936, 1000000 ticks. Expected: standing replication of the default build at 1M ticks: predators persist in about 3 of 4

- worlds 12, meat 19.3%, kill 14.9%, carnSp>0 in 3, preyCl 0.95, persisting (predK >= 64% of run after bootstrap) 9, exits 5, re-entries 1
- fruit: gene 0.196 -> 0.269 (up in 5 of 12), div 0.179, fruit 23.6%, carried 33.2%

### v1-EG-base-1937 (2026-09-28 12:23)

`defaults`, seeds 1937-1948, 1000000 ticks. Expected: standing replication of the default build at 1M ticks: predators persist in about 3 of 4

- worlds 12, meat 14.4%, kill 10.3%, carnSp>0 in 1, preyCl 0.85, persisting (predK >= 64% of run after bootstrap) 7, exits 10, re-entries 6
- fruit: gene 0.194 -> 0.354 (up in 11 of 12), div 0.204, fruit 20.9%, carried 46.0%

### v1-EG-base-1949 (2026-09-28 13:05)

`defaults`, seeds 1949-1960, 1000000 ticks. Expected: standing replication of the default build at 1M ticks: predators persist in about 3 of 4

- worlds 12, meat 20.1%, kill 15.1%, carnSp>0 in 5, preyCl 0.91, persisting (predK >= 64% of run after bootstrap) 10, exits 4, re-entries 2
- fruit: gene 0.195 -> 0.233 (up in 4 of 12), div 0.172, fruit 24.5%, carried 33.4%

### v1-EG-base-1961 (2026-09-28 13:05)

`defaults`, seeds 1961-1972, 1000000 ticks. Expected: standing replication of the default build at 1M ticks: predators persist in about 3 of 4

- worlds 12, meat 17.6%, kill 12.9%, carnSp>0 in 8, preyCl 0.85, persisting (predK >= 64% of run after bootstrap) 11, exits 5, re-entries 1
- fruit: gene 0.196 -> 0.247 (up in 7 of 12), div 0.188, fruit 21.9%, carried 31.5%

### v1-EG-base-1973 (2026-09-28 13:05)

`defaults`, seeds 1973-1984, 1000000 ticks. Expected: standing replication of the default build at 1M ticks: predators persist in about 3 of 4

- worlds 12, meat 21.6%, kill 16.6%, carnSp>0 in 3, preyCl 0.91, persisting (predK >= 64% of run after bootstrap) 11, exits 8, re-entries 5
- fruit: gene 0.193 -> 0.220 (up in 4 of 12), div 0.172, fruit 27.0%, carried 29.8%

### v1-EG-base-1997 (2026-09-28 13:41)

`defaults`, seeds 1997-2008, 1000000 ticks. Expected: standing replication of the default build at 1M ticks: predators persist in about 3 of 4

- worlds 12, meat 17.2%, kill 12.7%, carnSp>0 in 2, preyCl 0.89, persisting (predK >= 64% of run after bootstrap) 8, exits 5, re-entries 2
- fruit: gene 0.186 -> 0.299 (up in 7 of 12), div 0.200, fruit 26.2%, carried 37.0%

### v1-EG-base-1985 (2026-09-28 14:13)

`defaults`, seeds 1985-1996, 1000000 ticks. Expected: standing replication of the default build at 1M ticks: predators persist in about 3 of 4

- worlds 12, meat 15.8%, kill 11.1%, carnSp>0 in 3, preyCl 0.86, persisting (predK >= 64% of run after bootstrap) 9, exits 7, re-entries 2
- fruit: gene 0.197 -> 0.349 (up in 7 of 12), div 0.198, fruit 27.8%, carried 43.0%

### v1-EG-base-2009 (2026-09-28 14:13)

`defaults`, seeds 2009-2020, 1000000 ticks. Expected: standing replication of the default build at 1M ticks: predators persist in about 3 of 4

- worlds 12, meat 18.9%, kill 14.4%, carnSp>0 in 3, preyCl 0.91, persisting (predK >= 64% of run after bootstrap) 10, exits 7, re-entries 4
- fruit: gene 0.200 -> 0.241 (up in 6 of 12), div 0.188, fruit 25.9%, carried 31.3%

### v1-EG-base-2021 (2026-09-28 14:13)

`defaults`, seeds 2021-2032, 1000000 ticks. Expected: standing replication of the default build at 1M ticks: predators persist in about 3 of 4

- worlds 12, meat 16.4%, kill 11.8%, carnSp>0 in 2, preyCl 0.85, persisting (predK >= 64% of run after bootstrap) 5, exits 13, re-entries 8
- fruit: gene 0.191 -> 0.407 (up in 11 of 12), div 0.218, fruit 27.2%, carried 47.7%

### v1-EG-base-2033 (2026-09-28 14:13)

`defaults`, seeds 2033-2044, 1000000 ticks. Expected: standing replication of the default build at 1M ticks: predators persist in about 3 of 4

- worlds 12, meat 12.5%, kill 7.7%, carnSp>0 in 1, preyCl 0.85, persisting (predK >= 64% of run after bootstrap) 5, exits 10, re-entries 0
- fruit: gene 0.196 -> 0.385 (up in 11 of 12), div 0.238, fruit 24.3%, carried 46.5%

### v1-SD10-1985 (2026-09-28 14:13)

`smellDecay=0.1`, seeds 1985-1996, 1000000 ticks. Expected: third pair for shorter-lived scent (smellDecay 0.1): first half gave alignment 0.074 against 0.054 (8 of 12), predator worlds 10 against 6. Expect alignment above the block in 8 of 12; pooled over 36 pairs, alignment p < 0.05 would make 0.1 the default.

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
    preyCl baseline 0.858  arm 0.889   mean diff +0.030  sign test 6+/6-  p 1.000
    predCl baseline 3.163  arm 2.741   mean diff -0.422  sign test 4+/8-  p 0.388
    diet   baseline 0.094  arm 0.103   mean diff +0.009  sign test 8+/4-  p 0.388
    polar  baseline 0.031  arm 0.033   mean diff +0.002  sign test 8+/4-  p 0.388
    align  baseline 0.054  arm 0.105   mean diff +0.051  sign test 8+/4-  p 0.388
    preySp baseline 0.346  arm 0.356   mean diff +0.010  sign test 6+/6-  p 1.000
    predSp baseline 0.567  arm 0.522   mean diff -0.045  sign test 5+/7-  p 0.774
    learnM baseline 0.921  arm 0.887   mean diff -0.033  sign test 5+/7-  p 0.774

### v1-SM-3M-b (2026-09-28 14:30)

`defaults`, seeds 1901-1912, 3000000 ticks. Expected: a second 3M block on the smell default, to firm up predator comebacks: v1-SM-3M had 18 re-entries in 12 worlds against 12 without smell (v1-BP-3Mdefault). Expect re-entries 12 or more again, alignment about 0.04 throughout.

- worlds 12, meat 12.8%, kill 8.3%, carnSp>0 in 6, preyCl 0.85, persisting (predK >= 64% of run after bootstrap) 7, exits 16, re-entries 13
- fruit: gene 0.187 -> 0.530 (up in 11 of 12), div 0.228, fruit 26.8%, carried 56.7%

### v1-EG-base-2045 (2026-09-28 14:30)

`defaults`, seeds 2045-2056, 1000000 ticks. Expected: standing replication of the default build at 1M ticks: predators persist in about 3 of 4

- worlds 12, meat 19.3%, kill 14.5%, carnSp>0 in 6, preyCl 0.91, persisting (predK >= 64% of run after bootstrap) 9, exits 6, re-entries 2
- fruit: gene 0.192 -> 0.263 (up in 7 of 12), div 0.199, fruit 23.2%, carried 33.5%

### v1-SD10-2021 (2026-09-28 14:30)

`smellDecay=0.1`, seeds 2021-2032, 1000000 ticks. Expected: fourth pair for shorter-lived scent (smellDecay 0.1). Pairs so far: alignment higher in 16 of 24, predators persisting 21 against 13. Expect alignment above the block in 8 of 12; pooled 48 pairs decide the default at p < 0.05.

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
    preyCl baseline 0.853  arm 0.894   mean diff +0.041  sign test 7+/5-  p 0.774
    predCl baseline 2.604  arm 3.263   mean diff +0.658  sign test 7+/5-  p 0.774
    diet   baseline 0.088  arm 0.084   mean diff -0.004  sign test 7+/5-  p 0.774
    polar  baseline 0.030  arm 0.031   mean diff +0.001  sign test 5+/7-  p 0.774
    align  baseline 0.022  arm 0.058   mean diff +0.036  sign test 8+/4-  p 0.388
    preySp baseline 0.316  arm 0.316   mean diff +0.000  sign test 6+/6-  p 1.000
    predSp baseline 0.444  arm 0.507   mean diff +0.064  sign test 7+/5-  p 0.774
    learnM baseline 0.856  arm 0.863   mean diff +0.007  sign test 7+/5-  p 0.774

### v1-EG-base-2057 (2026-09-28 15:23)

`defaults`, seeds 2057-2068, 1000000 ticks. Expected: standing replication of the default build at 1M ticks: predators persist in about 3 of 4

- worlds 12, meat 18.9%, kill 14.7%, carnSp>0 in 5, preyCl 0.90, persisting (predK >= 64% of run after bootstrap) 8, exits 7, re-entries 5
- fruit: gene 0.194 -> 0.304 (up in 7 of 12), div 0.212, fruit 26.1%, carried 36.3%

### v1-EG-base-2069 (2026-09-28 15:23)

`defaults`, seeds 2069-2080, 1000000 ticks. Expected: standing replication of the default build at 1M ticks: predators persist in about 3 of 4

- worlds 12, meat 17.7%, kill 13.0%, carnSp>0 in 2, preyCl 0.87, persisting (predK >= 64% of run after bootstrap) 7, exits 9, re-entries 3
- fruit: gene 0.190 -> 0.382 (up in 8 of 12), div 0.218, fruit 26.2%, carried 43.5%

### v1-EG-base-2081 (2026-09-28 15:23)

`defaults`, seeds 2081-2092, 1000000 ticks. Expected: standing replication of the default build at 1M ticks: predators persist in about 3 of 4

- worlds 12, meat 17.1%, kill 12.4%, carnSp>0 in 4, preyCl 0.89, persisting (predK >= 64% of run after bootstrap) 8, exits 8, re-entries 3
- fruit: gene 0.187 -> 0.328 (up in 9 of 12), div 0.213, fruit 24.8%, carried 38.3%

### v1-EG-base-2093 (2026-09-28 15:23)

`defaults`, seeds 2093-2104, 1000000 ticks. Expected: standing replication of the default build at 1M ticks: predators persist in about 3 of 4

- worlds 12, meat 16.4%, kill 12.0%, carnSp>0 in 3, preyCl 0.86, persisting (predK >= 64% of run after bootstrap) 9, exits 7, re-entries 4
- fruit: gene 0.191 -> 0.344 (up in 9 of 12), div 0.208, fruit 23.9%, carried 39.7%

### v1-EG-base-2105 (2026-09-28 15:55)

`defaults`, seeds 2105-2116, 1000000 ticks. Expected: standing replication of the default build at 1M ticks: predators persist in about 3 of 4

- worlds 12, meat 18.9%, kill 14.4%, carnSp>0 in 4, preyCl 0.86, persisting (predK >= 64% of run after bootstrap) 10, exits 4, re-entries 3
- fruit: gene 0.201 -> 0.264 (up in 8 of 12), div 0.192, fruit 22.5%, carried 35.3%

### v1-EG-base-2129 (2026-09-28 15:55)

`defaults`, seeds 2129-2140, 1000000 ticks. Expected: standing replication of the default build at 1M ticks: predators persist in about 3 of 4

- worlds 12, meat 18.1%, kill 13.7%, carnSp>0 in 4, preyCl 0.86, persisting (predK >= 64% of run after bootstrap) 9, exits 7, re-entries 3
- fruit: gene 0.195 -> 0.323 (up in 7 of 12), div 0.197, fruit 22.0%, carried 39.7%

### v1-SD10-2129 (2026-09-28 16:15)

`smellDecay=0.1`, seeds 2129-2140, 1000000 ticks. Expected: fifth pair for shorter-lived scent (smellDecay 0.1). 36 pairs: alignment 0.088 against 0.055, higher in 24 (p 0.065); predator worlds 27 against 22. Expect alignment above the block in 8 of 12; pooled 60 pairs decide the default at p < 0.05.

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
    preyCl baseline 0.864  arm 0.891   mean diff +0.028  sign test 6+/6-  p 1.000
    predCl baseline 3.039  arm 2.468   mean diff -0.570  sign test 5+/7-  p 0.774
    diet   baseline 0.091  arm 0.101   mean diff +0.010  sign test 7+/5-  p 0.774
    polar  baseline 0.031  arm 0.031   mean diff -0.000  sign test 5+/7-  p 0.774
    align  baseline 0.043  arm 0.073   mean diff +0.029  sign test 8+/4-  p 0.388
    preySp baseline 0.338  arm 0.354   mean diff +0.017  sign test 6+/6-  p 1.000
    predSp baseline 0.502  arm 0.557   mean diff +0.055  sign test 7+/5-  p 0.774
    learnM baseline 0.888  arm 0.851   mean diff -0.037  sign test 5+/7-  p 0.774

### v1-EG-base-2141 (2026-09-28 16:36)

`defaults`, seeds 2141-2152, 1000000 ticks. Expected: standing replication of the default build at 1M ticks: predators persist in about 3 of 4

- worlds 12, meat 19.1%, kill 14.6%, carnSp>0 in 4, preyCl 0.87, persisting (predK >= 64% of run after bootstrap) 9, exits 6, re-entries 1
- fruit: gene 0.196 -> 0.277 (up in 7 of 12), div 0.195, fruit 25.2%, carried 33.4%

### v1-EG-base-2153 (2026-09-28 16:36)

`defaults`, seeds 2153-2164, 1000000 ticks. Expected: standing replication of the default build at 1M ticks: predators persist in about 3 of 4

- worlds 12, meat 17.1%, kill 12.9%, carnSp>0 in 3, preyCl 0.89, persisting (predK >= 64% of run after bootstrap) 7, exits 9, re-entries 6
- fruit: gene 0.189 -> 0.386 (up in 8 of 12), div 0.207, fruit 22.9%, carried 46.5%

### v1-EG-base-2117 (2026-09-28 17:11)

`defaults`, seeds 2117-2128, 1000000 ticks. Expected: standing replication of the default build at 1M ticks: predators persist in about 3 of 4

- worlds 12, meat 19.5%, kill 14.9%, carnSp>0 in 6, preyCl 0.91, persisting (predK >= 64% of run after bootstrap) 9, exits 3, re-entries 0
- fruit: gene 0.195 -> 0.195 (up in 4 of 12), div 0.182, fruit 23.3%, carried 27.1%

### v1-EG-base-2165 (2026-09-28 17:11)

`defaults`, seeds 2165-2176, 1000000 ticks. Expected: standing replication of the default build at 1M ticks: predators persist in about 3 of 4

- worlds 12, meat 17.1%, kill 12.5%, carnSp>0 in 5, preyCl 0.94, persisting (predK >= 64% of run after bootstrap) 8, exits 10, re-entries 4
- fruit: gene 0.198 -> 0.249 (up in 6 of 12), div 0.188, fruit 22.0%, carried 34.7%

### v1-EG-base-2177 (2026-09-28 17:11)

`defaults`, seeds 2177-2188, 1000000 ticks. Expected: standing replication of the default build at 1M ticks: predators persist in about 3 of 4

- worlds 12, meat 17.4%, kill 13.0%, carnSp>0 in 5, preyCl 0.84, persisting (predK >= 64% of run after bootstrap) 8, exits 7, re-entries 3
- fruit: gene 0.202 -> 0.278 (up in 7 of 12), div 0.209, fruit 21.8%, carried 34.9%

### v1-EG-base-2189 (2026-09-28 17:11)

`defaults`, seeds 2189-2200, 1000000 ticks. Expected: standing replication of the default build at 1M ticks: predators persist in about 3 of 4

- worlds 12, meat 16.4%, kill 11.7%, carnSp>0 in 1, preyCl 0.86, persisting (predK >= 64% of run after bootstrap) 10, exits 9, re-entries 3
- fruit: gene 0.190 -> 0.342 (up in 10 of 12), div 0.232, fruit 23.0%, carried 43.3%

### v1-EG-base-2201 (2026-09-28 17:38)

`defaults`, seeds 2201-2212, 1000000 ticks. Expected: standing replication of the default build at 1M ticks: predators persist in about 3 of 4

- worlds 12, meat 14.3%, kill 9.8%, carnSp>0 in 4, preyCl 0.82, persisting (predK >= 64% of run after bootstrap) 9, exits 7, re-entries 3
- fruit: gene 0.194 -> 0.340 (up in 10 of 12), div 0.227, fruit 22.1%, carried 43.2%

### v1-EG-base-2213 (2026-09-28 17:38)

`defaults`, seeds 2213-2224, 1000000 ticks. Expected: standing replication of the default build at 1M ticks: predators persist in about 3 of 4

- worlds 12, meat 15.5%, kill 10.4%, carnSp>0 in 3, preyCl 0.84, persisting (predK >= 64% of run after bootstrap) 5, exits 13, re-entries 5
- fruit: gene 0.198 -> 0.280 (up in 9 of 12), div 0.219, fruit 23.8%, carried 39.2%

### v1-EG-base-2225 (2026-09-28 17:38)

`defaults`, seeds 2225-2236, 1000000 ticks. Expected: standing replication of the default build at 1M ticks: predators persist in about 3 of 4

- worlds 12, meat 17.5%, kill 12.4%, carnSp>0 in 4, preyCl 0.86, persisting (predK >= 64% of run after bootstrap) 7, exits 8, re-entries 2
- fruit: gene 0.199 -> 0.314 (up in 8 of 12), div 0.218, fruit 28.2%, carried 39.9%

### v1-EG-base-2237 (2026-09-28 18:24)

`defaults`, seeds 2237-2248, 1000000 ticks. Expected: standing replication of the default build at 1M ticks: predators persist in about 3 of 4

- worlds 12, meat 18.3%, kill 13.9%, carnSp>0 in 5, preyCl 0.90, persisting (predK >= 64% of run after bootstrap) 10, exits 6, re-entries 1
- fruit: gene 0.195 -> 0.214 (up in 6 of 12), div 0.185, fruit 22.4%, carried 30.3%

### v1-EG-base-2249 (2026-09-28 18:24)

`defaults`, seeds 2249-2260, 1000000 ticks. Expected: standing replication of the default build at 1M ticks: predators persist in about 3 of 4

- worlds 12, meat 17.0%, kill 12.5%, carnSp>0 in 4, preyCl 0.89, persisting (predK >= 64% of run after bootstrap) 9, exits 7, re-entries 4
- fruit: gene 0.202 -> 0.392 (up in 7 of 12), div 0.188, fruit 29.4%, carried 44.8%

### v1-EG-base-2261 (2026-09-28 18:24)

`defaults`, seeds 2261-2272, 1000000 ticks. Expected: standing replication of the default build at 1M ticks: predators persist in about 3 of 4

- worlds 12, meat 21.2%, kill 16.0%, carnSp>0 in 5, preyCl 0.94, persisting (predK >= 64% of run after bootstrap) 11, exits 6, re-entries 3
- fruit: gene 0.200 -> 0.241 (up in 6 of 12), div 0.183, fruit 24.2%, carried 31.8%

### v1-EG-base-2273 (2026-09-28 18:24)

`defaults`, seeds 2273-2284, 1000000 ticks. Expected: standing replication of the default build at 1M ticks: predators persist in about 3 of 4

- worlds 12, meat 17.9%, kill 13.2%, carnSp>0 in 3, preyCl 0.89, persisting (predK >= 64% of run after bootstrap) 6, exits 7, re-entries 2
- fruit: gene 0.199 -> 0.332 (up in 8 of 12), div 0.209, fruit 28.4%, carried 39.5%

### v1-EG-base-2285 (2026-09-28 19:05)

`defaults`, seeds 2285-2296, 1000000 ticks. Expected: standing replication of the default build at 1M ticks: predators persist in about 3 of 4

- worlds 12, meat 20.5%, kill 15.4%, carnSp>0 in 6, preyCl 0.97, persisting (predK >= 64% of run after bootstrap) 10, exits 4, re-entries 1
- fruit: gene 0.197 -> 0.252 (up in 5 of 12), div 0.183, fruit 28.7%, carried 31.5%

### v1-EG-base-2297 (2026-09-28 19:05)

`defaults`, seeds 2297-2308, 1000000 ticks. Expected: standing replication of the default build at 1M ticks: predators persist in about 3 of 4

- worlds 12, meat 17.6%, kill 12.5%, carnSp>0 in 2, preyCl 0.93, persisting (predK >= 64% of run after bootstrap) 8, exits 7, re-entries 2
- fruit: gene 0.201 -> 0.260 (up in 6 of 12), div 0.195, fruit 25.1%, carried 36.3%

### v1-EG-base-2309 (2026-09-28 19:58)

`defaults`, seeds 2309-2320, 1000000 ticks. Expected: standing replication of the default build at 1M ticks: predators persist in about 3 of 4

- worlds 12, meat 18.4%, kill 13.8%, carnSp>0 in 2, preyCl 0.90, persisting (predK >= 64% of run after bootstrap) 8, exits 9, re-entries 5
- fruit: gene 0.189 -> 0.317 (up in 8 of 12), div 0.210, fruit 23.9%, carried 39.0%

### v1-EG-base-2321 (2026-09-28 19:58)

`defaults`, seeds 2321-2332, 1000000 ticks. Expected: standing replication of the default build at 1M ticks: predators persist in about 3 of 4

- worlds 12, meat 18.0%, kill 13.1%, carnSp>0 in 4, preyCl 0.87, persisting (predK >= 64% of run after bootstrap) 10, exits 8, re-entries 1
- fruit: gene 0.197 -> 0.280 (up in 7 of 12), div 0.206, fruit 23.4%, carried 35.1%

### v1-EG-base-2333 (2026-09-28 19:58)

`defaults`, seeds 2333-2344, 1000000 ticks. Expected: standing replication of the default build at 1M ticks: predators persist in about 3 of 4

- worlds 12, meat 19.8%, kill 14.6%, carnSp>0 in 4, preyCl 0.86, persisting (predK >= 64% of run after bootstrap) 8, exits 9, re-entries 5
- fruit: gene 0.193 -> 0.288 (up in 7 of 12), div 0.212, fruit 26.5%, carried 36.5%

### v1-CP-2321 (2026-09-28 19:58)

`compass=1`, seeds 2321-2332, 1000000 ticks. Expected: compass on the smell default (smellDecay 0.1), paired with the standing block of the same seeds. Before smell the compass cost predators (persisting 10 of 24 against 20) because prey streamed. Expect: prey still stream (polar above 0.3 in most worlds) and predators still persist less (fewer than the block in 2 blocks pooled); if smell's fronts let hunters keep up, persistence within 3 of the blocks.

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
    preyCl baseline 0.874  arm 0.910   mean diff +0.036  sign test 8+/4-  p 0.388
    predCl baseline 2.790  arm 3.516   mean diff +0.726  sign test 8+/4-  p 0.388
    diet   baseline 0.097  arm 0.082   mean diff -0.015  sign test 3+/9-  p 0.146
    polar  baseline 0.031  arm 0.415   mean diff +0.384  sign test 12+/0-  p 0.000
    align  baseline 0.072  arm 0.303   mean diff +0.231  sign test 10+/2-  p 0.039
    preySp baseline 0.324  arm 0.335   mean diff +0.011  sign test 7+/5-  p 0.774
    predSp baseline 0.520  arm 0.405   mean diff -0.115  sign test 4+/8-  p 0.388
    learnM baseline 0.905  arm 0.902   mean diff -0.003  sign test 8+/4-  p 0.388

### v1-CP-2333 (2026-09-28 19:58)

`compass=1`, seeds 2333-2344, 1000000 ticks. Expected: compass on the smell default (smellDecay 0.1), paired with the standing block of the same seeds. Before smell the compass cost predators (persisting 10 of 24 against 20) because prey streamed. Expect: prey still stream (polar above 0.3 in most worlds) and predators still persist less (fewer than the block in 2 blocks pooled); if smell's fronts let hunters keep up, persistence within 3 of the blocks.

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
    preyCl baseline 0.859  arm 0.987   mean diff +0.129  sign test 10+/2-  p 0.039
    predCl baseline 3.004  arm 2.242   mean diff -0.762  sign test 5+/7-  p 0.774
    diet   baseline 0.103  arm 0.095   mean diff -0.008  sign test 6+/6-  p 1.000
    polar  baseline 0.032  arm 0.335   mean diff +0.303  sign test 12+/0-  p 0.000
    align  baseline 0.070  arm 0.229   mean diff +0.159  sign test 12+/0-  p 0.000
    preySp baseline 0.353  arm 0.380   mean diff +0.027  sign test 6+/6-  p 1.000
    predSp baseline 0.545  arm 0.601   mean diff +0.056  sign test 8+/4-  p 0.388
    learnM baseline 0.870  arm 0.899   mean diff +0.029  sign test 8+/4-  p 0.388

### v1-EG-base-2345 (2026-09-28 20:14)

`defaults`, seeds 2345-2356, 1000000 ticks. Expected: standing replication of the default build at 1M ticks: predators persist in about 3 of 4

- worlds 12, meat 20.5%, kill 15.8%, carnSp>0 in 3, preyCl 0.96, persisting (predK >= 64% of run after bootstrap) 11, exits 6, re-entries 2
- fruit: gene 0.196 -> 0.256 (up in 6 of 12), div 0.195, fruit 24.4%, carried 31.1%

### v1-EG-base-2357 (2026-09-28 20:17)

`defaults`, seeds 2357-2368, 1000000 ticks. Expected: standing replication of the default build at 1M ticks: predators persist in about 3 of 4

- worlds 12, meat 19.7%, kill 14.6%, carnSp>0 in 4, preyCl 0.92, persisting (predK >= 64% of run after bootstrap) 8, exits 8, re-entries 1
- fruit: gene 0.197 -> 0.319 (up in 7 of 12), div 0.182, fruit 31.7%, carried 39.5%

### v1-EG-base-2369 (2026-09-28 21:26)

`defaults`, seeds 2369-2380, 1000000 ticks. Expected: standing replication of the default build at 1M ticks: predators persist in about 3 of 4

- worlds 12, meat 17.2%, kill 12.1%, carnSp>0 in 4, preyCl 0.90, persisting (predK >= 64% of run after bootstrap) 8, exits 9, re-entries 3
- fruit: gene 0.185 -> 0.321 (up in 8 of 12), div 0.210, fruit 25.3%, carried 40.1%

### v1-EG-base-2381 (2026-09-28 21:26)

`defaults`, seeds 2381-2392, 1000000 ticks. Expected: standing replication of the default build at 1M ticks: predators persist in about 3 of 4

- worlds 12, meat 14.8%, kill 10.2%, carnSp>0 in 3, preyCl 0.86, persisting (predK >= 64% of run after bootstrap) 9, exits 8, re-entries 3
- fruit: gene 0.181 -> 0.239 (up in 8 of 12), div 0.207, fruit 18.4%, carried 34.3%

### v1-EG-base-2393 (2026-09-28 21:26)

`defaults`, seeds 2393-2404, 1000000 ticks. Expected: standing replication of the default build at 1M ticks: predators persist in about 3 of 4

- worlds 12, meat 20.8%, kill 16.1%, carnSp>0 in 7, preyCl 0.92, persisting (predK >= 64% of run after bootstrap) 9, exits 3, re-entries 0
- fruit: gene 0.192 -> 0.250 (up in 5 of 12), div 0.183, fruit 25.3%, carried 33.8%

### v1-EG-base-2405 (2026-09-28 21:26)

`defaults`, seeds 2405-2416, 1000000 ticks. Expected: standing replication of the default build at 1M ticks: predators persist in about 3 of 4

- worlds 12, meat 19.7%, kill 15.2%, carnSp>0 in 4, preyCl 0.86, persisting (predK >= 64% of run after bootstrap) 10, exits 4, re-entries 1
- fruit: gene 0.195 -> 0.212 (up in 6 of 12), div 0.183, fruit 26.1%, carried 28.0%

### v1-EG-base-2417 (2026-09-28 21:26)

`defaults`, seeds 2417-2428, 1000000 ticks. Expected: standing replication of the default build at 1M ticks: predators persist in about 3 of 4

- worlds 12, meat 13.2%, kill 8.1%, carnSp>0 in 3, preyCl 0.86, persisting (predK >= 64% of run after bootstrap) 4, exits 9, re-entries 4
- fruit: gene 0.189 -> 0.418 (up in 9 of 12), div 0.227, fruit 26.1%, carried 50.4%

### v1-EG-base-2429 (2026-09-28 22:13)

`defaults`, seeds 2429-2440, 1000000 ticks. Expected: standing replication of the default build at 1M ticks: predators persist in about 3 of 4

- worlds 12, meat 16.6%, kill 12.0%, carnSp>0 in 3, preyCl 0.90, persisting (predK >= 64% of run after bootstrap) 6, exits 10, re-entries 4
- fruit: gene 0.199 -> 0.337 (up in 8 of 12), div 0.206, fruit 25.2%, carried 42.4%

### v1-EG-base-2441 (2026-09-28 22:13)

`defaults`, seeds 2441-2452, 1000000 ticks. Expected: standing replication of the default build at 1M ticks: predators persist in about 3 of 4

- worlds 12, meat 21.1%, kill 16.3%, carnSp>0 in 5, preyCl 0.97, persisting (predK >= 64% of run after bootstrap) 10, exits 4, re-entries 2
- fruit: gene 0.193 -> 0.333 (up in 7 of 12), div 0.197, fruit 25.4%, carried 39.1%

### v1-EG-base-2453 (2026-09-28 22:13)

`defaults`, seeds 2453-2464, 1000000 ticks. Expected: standing replication of the default build at 1M ticks: predators persist in about 3 of 4

- worlds 12, meat 13.0%, kill 8.4%, carnSp>0 in 2, preyCl 0.85, persisting (predK >= 64% of run after bootstrap) 5, exits 12, re-entries 5
- fruit: gene 0.192 -> 0.380 (up in 10 of 12), div 0.234, fruit 21.7%, carried 47.9%

### v1-EG-base-2465 (2026-09-28 22:44)

`defaults`, seeds 2465-2476, 1000000 ticks. Expected: standing replication of the default build at 1M ticks: predators persist in about 3 of 4

- worlds 12, meat 19.6%, kill 14.9%, carnSp>0 in 5, preyCl 0.93, persisting (predK >= 64% of run after bootstrap) 9, exits 6, re-entries 5
- fruit: gene 0.193 -> 0.264 (up in 7 of 12), div 0.195, fruit 25.3%, carried 33.4%

### v1-EG-base-2477 (2026-09-28 22:44)

`defaults`, seeds 2477-2488, 1000000 ticks. Expected: standing replication of the default build at 1M ticks: predators persist in about 3 of 4

- worlds 12, meat 17.8%, kill 12.7%, carnSp>0 in 4, preyCl 0.88, persisting (predK >= 64% of run after bootstrap) 10, exits 5, re-entries 2
- fruit: gene 0.205 -> 0.296 (up in 8 of 12), div 0.193, fruit 29.2%, carried 37.6%

### v1-EG-base-2489 (2026-09-28 22:44)

`defaults`, seeds 2489-2500, 1000000 ticks. Expected: standing replication of the default build at 1M ticks: predators persist in about 3 of 4

- worlds 12, meat 16.1%, kill 11.6%, carnSp>0 in 1, preyCl 0.88, persisting (predK >= 64% of run after bootstrap) 8, exits 5, re-entries 0
- fruit: gene 0.199 -> 0.290 (up in 9 of 12), div 0.211, fruit 22.7%, carried 38.9%

### v1-EG-base-2501 (2026-09-28 22:44)

`defaults`, seeds 2501-2512, 1000000 ticks. Expected: standing replication of the default build at 1M ticks: predators persist in about 3 of 4

- worlds 12, meat 17.6%, kill 13.0%, carnSp>0 in 5, preyCl 0.89, persisting (predK >= 64% of run after bootstrap) 6, exits 7, re-entries 5
- fruit: gene 0.191 -> 0.298 (up in 7 of 12), div 0.212, fruit 24.1%, carried 37.1%

### v1-EG-base-2513 (2026-09-28 23:30)

`defaults`, seeds 2513-2524, 1000000 ticks. Expected: standing replication of the default build at 1M ticks: predators persist in about 3 of 4

- worlds 12, meat 16.1%, kill 10.7%, carnSp>0 in 4, preyCl 0.92, persisting (predK >= 64% of run after bootstrap) 7, exits 9, re-entries 4
- fruit: gene 0.193 -> 0.328 (up in 7 of 12), div 0.209, fruit 29.1%, carried 42.1%

### v1-EG-base-2525 (2026-09-28 23:30)

`defaults`, seeds 2525-2536, 1000000 ticks. Expected: standing replication of the default build at 1M ticks: predators persist in about 3 of 4

- worlds 12, meat 20.8%, kill 15.3%, carnSp>0 in 2, preyCl 0.97, persisting (predK >= 64% of run after bootstrap) 10, exits 5, re-entries 1
- fruit: gene 0.195 -> 0.261 (up in 5 of 12), div 0.186, fruit 30.7%, carried 32.2%

### v1-SF-2513 (2026-09-28 23:30)

`smellFruit=1`, seeds 2513-2524, 1000000 ticks. Expected: fruit scent (smellFruit 1) on the smellDecay 0.1 default, paired with the standing block of the same seeds (NI 53 build). seeFruit alone let grazers steer to fruit but did not pay the plants (fruit gene 0.31 against 0.44). Expect: grazers turn toward fruit scent (tools/smell.js), fruit share of plant-eaters' energy up (above the block's in 8 of 12), fruit gene and carried-seed share higher; predators within 2 of the block.

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
    preyCl baseline 0.922  arm 0.876   mean diff -0.047  sign test 6+/6-  p 1.000
    predCl baseline 2.332  arm 2.213   mean diff -0.119  sign test 5+/7-  p 0.774
    diet   baseline 0.102  arm 0.096   mean diff -0.006  sign test 5+/7-  p 0.774
    polar  baseline 0.031  arm 0.035   mean diff +0.004  sign test 11+/1-  p 0.006
    align  baseline 0.056  arm 0.104   mean diff +0.048  sign test 9+/3-  p 0.146
    preySp baseline 0.358  arm 0.330   mean diff -0.027  sign test 6+/6-  p 1.000
    predSp baseline 0.529  arm 0.591   mean diff +0.061  sign test 7+/5-  p 0.774
    learnM baseline 0.879  arm 0.892   mean diff +0.013  sign test 8+/4-  p 0.388

### v1-EG-base-2537 (2026-09-29 00:07)

`defaults`, seeds 2537-2548, 1000000 ticks. Expected: standing replication of the default build at 1M ticks: predators persist in about 3 of 4

- worlds 12, meat 19.4%, kill 14.3%, carnSp>0 in 5, preyCl 0.91, persisting (predK >= 64% of run after bootstrap) 9, exits 6, re-entries 1
- fruit: gene 0.195 -> 0.250 (up in 7 of 12), div 0.204, fruit 25.8%, carried 33.0%

### v1-EG-base-2549 (2026-09-29 00:07)

`defaults`, seeds 2549-2560, 1000000 ticks. Expected: standing replication of the default build at 1M ticks: predators persist in about 3 of 4

- worlds 12, meat 18.1%, kill 13.5%, carnSp>0 in 3, preyCl 0.84, persisting (predK >= 64% of run after bootstrap) 9, exits 6, re-entries 2
- fruit: gene 0.195 -> 0.308 (up in 7 of 12), div 0.189, fruit 28.7%, carried 37.7%

### v1-SF-2525 (2026-09-29 00:07)

`smellFruit=1`, seeds 2525-2536, 1000000 ticks. Expected: fruit scent (smellFruit 1) on the smellDecay 0.1 default, paired with the standing block of the same seeds (NI 53 build). seeFruit alone let grazers steer to fruit but did not pay the plants (fruit gene 0.31 against 0.44). Expect: grazers turn toward fruit scent (tools/smell.js), fruit share of plant-eaters' energy up (above the block's in 8 of 12), fruit gene and carried-seed share higher; predators within 2 of the block.

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
    preyCl baseline 0.975  arm 0.854   mean diff -0.121  sign test 5+/7-  p 0.774
    predCl baseline 2.573  arm 2.211   mean diff -0.362  sign test 6+/6-  p 1.000
    diet   baseline 0.104  arm 0.091   mean diff -0.014  sign test 3+/9-  p 0.146
    polar  baseline 0.032  arm 0.035   mean diff +0.002  sign test 9+/3-  p 0.146
    align  baseline 0.122  arm 0.097   mean diff -0.025  sign test 4+/8-  p 0.388
    preySp baseline 0.406  arm 0.312   mean diff -0.094  sign test 2+/10-  p 0.039
    predSp baseline 0.613  arm 0.606   mean diff -0.007  sign test 5+/7-  p 0.774
    learnM baseline 0.879  arm 0.870   mean diff -0.009  sign test 5+/7-  p 0.774

### v1-EG-base-2561 (2026-09-29 00:39)

`defaults`, seeds 2561-2572, 1000000 ticks. Expected: standing replication of the default build at 1M ticks: predators persist in about 3 of 4

- worlds 12, meat 16.4%, kill 12.1%, carnSp>0 in 3, preyCl 0.89, persisting (predK >= 64% of run after bootstrap) 8, exits 6, re-entries 2
- fruit: gene 0.201 -> 0.340 (up in 7 of 12), div 0.212, fruit 24.6%, carried 44.2%

### v1-EG-base-2573 (2026-09-29 00:39)

`defaults`, seeds 2573-2584, 1000000 ticks. Expected: standing replication of the default build at 1M ticks: predators persist in about 3 of 4

- worlds 12, meat 20.2%, kill 15.7%, carnSp>0 in 2, preyCl 0.88, persisting (predK >= 64% of run after bootstrap) 10, exits 6, re-entries 3
- fruit: gene 0.193 -> 0.265 (up in 7 of 12), div 0.194, fruit 28.1%, carried 34.8%

### v1-EG-base-2585 (2026-09-29 00:40)

`defaults`, seeds 2585-2596, 1000000 ticks. Expected: standing replication of the default build at 1M ticks: predators persist in about 3 of 4

- worlds 12, meat 18.3%, kill 13.6%, carnSp>0 in 4, preyCl 0.90, persisting (predK >= 64% of run after bootstrap) 5, exits 11, re-entries 7
- fruit: gene 0.200 -> 0.255 (up in 7 of 12), div 0.196, fruit 24.7%, carried 33.8%

### v1-SD05-2573 (2026-09-29 00:40)

`smellDecay=0.05`, seeds 2573-2584, 1000000 ticks. Expected: the old scent lifetime (smellDecay 0.05) against the 0.1 default, paired with the standing block of the same seeds. Unpaired blocks put 0.1 at 69% persistence (199 of 288) against 76% for 0.05 (228 of 300), while five same-seed pairs gave 0.1 44 of 60 against 36. Expect: persistence within 2 of the block per 12 (no cost of 0.1), alignment lower on 0.05 in 8 of 12.

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
    preyCl baseline 0.882  arm 0.898   mean diff +0.015  sign test 8+/4-  p 0.388
    predCl baseline 2.116  arm 3.120   mean diff +1.004  sign test 9+/3-  p 0.146
    diet   baseline 0.101  arm 0.082   mean diff -0.019  sign test 4+/8-  p 0.388
    polar  baseline 0.031  arm 0.032   mean diff +0.000  sign test 7+/5-  p 0.774
    align  baseline 0.084  arm 0.059   mean diff -0.025  sign test 4+/8-  p 0.388
    preySp baseline 0.367  arm 0.328   mean diff -0.039  sign test 4+/8-  p 0.388
    predSp baseline 0.603  arm 0.477   mean diff -0.126  sign test 3+/9-  p 0.146
    learnM baseline 0.885  arm 0.881   mean diff -0.004  sign test 5+/7-  p 0.774

### v1-EG-base-2597 (2026-09-29 01:06)

`defaults`, seeds 2597-2608, 1000000 ticks. Expected: standing replication of the default build at 1M ticks: predators persist in about 3 of 4

- worlds 12, meat 18.4%, kill 13.7%, carnSp>0 in 0, preyCl 0.88, persisting (predK >= 64% of run after bootstrap) 8, exits 9, re-entries 5
- fruit: gene 0.196 -> 0.328 (up in 9 of 12), div 0.201, fruit 26.6%, carried 39.0%

### v1-SD05-2585 (2026-09-29 01:06)

`smellDecay=0.05`, seeds 2585-2596, 1000000 ticks. Expected: the old scent lifetime (smellDecay 0.05) against the 0.1 default, paired with the standing block of the same seeds. Unpaired blocks put 0.1 at 69% persistence (199 of 288) against 76% for 0.05 (228 of 300), while five same-seed pairs gave 0.1 44 of 60 against 36. Expect: persistence within 2 of the block per 12 (no cost of 0.1), alignment lower on 0.05 in 8 of 12.

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
    preyCl baseline 0.905  arm 0.916   mean diff +0.012  sign test 6+/6-  p 1.000
    predCl baseline 2.570  arm 3.217   mean diff +0.647  sign test 5+/7-  p 0.774
    diet   baseline 0.084  arm 0.084   mean diff +0.000  sign test 6+/6-  p 1.000
    polar  baseline 0.030  arm 0.031   mean diff +0.001  sign test 8+/4-  p 0.388
    align  baseline 0.055  arm 0.033   mean diff -0.022  sign test 4+/8-  p 0.388
    preySp baseline 0.322  arm 0.312   mean diff -0.010  sign test 6+/6-  p 1.000
    predSp baseline 0.542  arm 0.453   mean diff -0.089  sign test 3+/9-  p 0.146
    learnM baseline 0.886  arm 0.854   mean diff -0.032  sign test 2+/10-  p 0.039

### v1-SD05-2597 (2026-09-29 01:06)

`smellDecay=0.05`, seeds 2597-2608, 1000000 ticks. Expected: third reverse pair: 0.05 against the 0.1 default on the same seeds, to settle whether 0.1 costs predator persistence (unpaired blocks 69% against 76%; earlier pairs favour 0.1). Expect persistence within 2 of the block.

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
    preyCl baseline 0.880  arm 0.940   mean diff +0.060  sign test 8+/4-  p 0.388
    predCl baseline 2.315  arm 2.527   mean diff +0.212  sign test 8+/4-  p 0.388
    diet   baseline 0.093  arm 0.097   mean diff +0.005  sign test 8+/4-  p 0.388
    polar  baseline 0.031  arm 0.032   mean diff +0.001  sign test 7+/5-  p 0.774
    align  baseline 0.069  arm 0.061   mean diff -0.008  sign test 8+/4-  p 0.388
    preySp baseline 0.355  arm 0.370   mean diff +0.016  sign test 5+/7-  p 0.774
    predSp baseline 0.508  arm 0.604   mean diff +0.096  sign test 9+/3-  p 0.146
    learnM baseline 0.857  arm 0.851   mean diff -0.006  sign test 6+/6-  p 1.000

### v1-EG-base-2609 (2026-09-29 01:57)

`defaults`, seeds 2609-2620, 1000000 ticks. Expected: standing replication of the default build at 1M ticks: predators persist in about 3 of 4

- worlds 12, meat 18.5%, kill 14.2%, carnSp>0 in 2, preyCl 0.89, persisting (predK >= 64% of run after bootstrap) 9, exits 7, re-entries 3
- fruit: gene 0.196 -> 0.269 (up in 6 of 12), div 0.196, fruit 28.2%, carried 34.6%

### v1-EG-base-2621 (2026-09-29 01:57)

`defaults`, seeds 2621-2632, 1000000 ticks. Expected: standing replication of the default build at 1M ticks: predators persist in about 3 of 4

- worlds 12, meat 14.9%, kill 10.3%, carnSp>0 in 4, preyCl 0.83, persisting (predK >= 64% of run after bootstrap) 7, exits 8, re-entries 5
- fruit: gene 0.192 -> 0.406 (up in 11 of 12), div 0.221, fruit 24.9%, carried 48.7%

### v1-EG-base-2633 (2026-09-29 01:57)

`defaults`, seeds 2633-2644, 1000000 ticks. Expected: standing replication of the default build at 1M ticks: predators persist in about 3 of 4

- worlds 12, meat 16.6%, kill 11.9%, carnSp>0 in 3, preyCl 0.92, persisting (predK >= 64% of run after bootstrap) 9, exits 7, re-entries 1
- fruit: gene 0.197 -> 0.265 (up in 7 of 12), div 0.195, fruit 25.5%, carried 34.7%

### v1-EG-base-2645 (2026-09-29 02:34)

`defaults`, seeds 2645-2656, 1000000 ticks. Expected: standing replication of the default build at 1M ticks: predators persist in about 3 of 4

- worlds 12, meat 19.2%, kill 13.6%, carnSp>0 in 2, preyCl 0.97, persisting (predK >= 64% of run after bootstrap) 5, exits 8, re-entries 4
- fruit: gene 0.198 -> 0.298 (up in 7 of 12), div 0.216, fruit 27.5%, carried 39.4%

### v1-EG-base-2657 (2026-09-29 02:34)

`defaults`, seeds 2657-2668, 1000000 ticks. Expected: standing replication of the default build at 1M ticks: predators persist in about 3 of 4

- worlds 12, meat 18.8%, kill 13.8%, carnSp>0 in 6, preyCl 0.92, persisting (predK >= 64% of run after bootstrap) 9, exits 6, re-entries 2
- fruit: gene 0.198 -> 0.288 (up in 6 of 12), div 0.177, fruit 24.4%, carried 37.8%

### v1-EG-base-2669 (2026-09-29 02:34)

`defaults`, seeds 2669-2680, 1000000 ticks. Expected: standing replication of the default build at 1M ticks: predators persist in about 3 of 4

- worlds 12, meat 21.4%, kill 16.8%, carnSp>0 in 7, preyCl 0.94, persisting (predK >= 64% of run after bootstrap) 11, exits 4, re-entries 0
- fruit: gene 0.194 -> 0.217 (up in 3 of 12), div 0.182, fruit 23.0%, carried 28.9%

### v1-EG-base-2681 (2026-09-29 02:34)

`defaults`, seeds 2681-2692, 1000000 ticks. Expected: standing replication of the default build at 1M ticks: predators persist in about 3 of 4

- worlds 12, meat 16.2%, kill 11.4%, carnSp>0 in 3, preyCl 0.83, persisting (predK >= 64% of run after bootstrap) 6, exits 10, re-entries 5
- fruit: gene 0.188 -> 0.288 (up in 7 of 12), div 0.204, fruit 25.5%, carried 39.2%

### v1-EG-base-2693 (2026-09-29 02:34)

`defaults`, seeds 2693-2704, 1000000 ticks. Expected: standing replication of the default build at 1M ticks: predators persist in about 3 of 4

- worlds 12, meat 15.8%, kill 11.4%, carnSp>0 in 5, preyCl 0.89, persisting (predK >= 64% of run after bootstrap) 7, exits 9, re-entries 3
- fruit: gene 0.185 -> 0.338 (up in 8 of 12), div 0.219, fruit 25.7%, carried 40.8%

### v1-EG-base-2705 (2026-09-29 03:56)

`defaults`, seeds 2705-2716, 1000000 ticks. Expected: standing replication of the default build at 1M ticks: predators persist in about 3 of 4

- worlds 12, meat 18.1%, kill 13.6%, carnSp>0 in 3, preyCl 0.91, persisting (predK >= 64% of run after bootstrap) 6, exits 10, re-entries 3
- fruit: gene 0.196 -> 0.306 (up in 8 of 12), div 0.217, fruit 23.6%, carried 39.1%

### v1-EG-base-2717 (2026-09-29 03:56)

`defaults`, seeds 2717-2728, 1000000 ticks. Expected: standing replication of the default build at 1M ticks: predators persist in about 3 of 4

- worlds 12, meat 18.4%, kill 13.2%, carnSp>0 in 6, preyCl 0.89, persisting (predK >= 64% of run after bootstrap) 8, exits 8, re-entries 3
- fruit: gene 0.185 -> 0.270 (up in 8 of 12), div 0.192, fruit 25.0%, carried 35.4%

### v1-EG-base-2729 (2026-09-29 03:56)

`defaults`, seeds 2729-2740, 1000000 ticks. Expected: standing replication of the default build at 1M ticks: predators persist in about 3 of 4

- worlds 12, meat 17.3%, kill 12.8%, carnSp>0 in 2, preyCl 0.88, persisting (predK >= 64% of run after bootstrap) 11, exits 7, re-entries 4
- fruit: gene 0.188 -> 0.348 (up in 7 of 12), div 0.214, fruit 26.0%, carried 42.2%

### v1-EG-base-2741 (2026-09-29 03:56)

`defaults`, seeds 2741-2752, 1000000 ticks. Expected: standing replication of the default build at 1M ticks: predators persist in about 3 of 4

- worlds 12, meat 15.9%, kill 11.0%, carnSp>0 in 3, preyCl 0.85, persisting (predK >= 64% of run after bootstrap) 8, exits 12, re-entries 5
- fruit: gene 0.198 -> 0.313 (up in 8 of 12), div 0.208, fruit 22.3%, carried 40.5%

### v1-EG-base-2753 (2026-09-29 03:57)

`defaults`, seeds 2753-2764, 1000000 ticks. Expected: standing replication of the default build at 1M ticks: predators persist in about 3 of 4

- worlds 12, meat 17.2%, kill 12.0%, carnSp>0 in 5, preyCl 0.89, persisting (predK >= 64% of run after bootstrap) 9, exits 11, re-entries 4
- fruit: gene 0.188 -> 0.282 (up in 6 of 12), div 0.192, fruit 21.3%, carried 38.3%

### v1-EG-base-2765 (2026-09-29 03:57)

`defaults`, seeds 2765-2776, 1000000 ticks. Expected: standing replication of the default build at 1M ticks: predators persist in about 3 of 4

- worlds 12, meat 17.7%, kill 13.1%, carnSp>0 in 4, preyCl 0.88, persisting (predK >= 64% of run after bootstrap) 8, exits 8, re-entries 4
- fruit: gene 0.192 -> 0.368 (up in 11 of 12), div 0.222, fruit 23.9%, carried 44.3%

### v1-EG-base-2777 (2026-09-29 03:57)

`defaults`, seeds 2777-2788, 1000000 ticks. Expected: standing replication of the default build at 1M ticks: predators persist in about 3 of 4

- worlds 12, meat 14.8%, kill 9.9%, carnSp>0 in 2, preyCl 0.85, persisting (predK >= 64% of run after bootstrap) 8, exits 11, re-entries 7
- fruit: gene 0.193 -> 0.341 (up in 8 of 12), div 0.215, fruit 23.3%, carried 44.3%

### v1-EG-base-2789 (2026-09-29 04:43)

`defaults`, seeds 2789-2800, 1000000 ticks. Expected: standing replication of the default build at 1M ticks: predators persist in about 3 of 4

- worlds 12, meat 18.2%, kill 13.2%, carnSp>0 in 3, preyCl 0.83, persisting (predK >= 64% of run after bootstrap) 8, exits 8, re-entries 5
- fruit: gene 0.192 -> 0.286 (up in 7 of 12), div 0.206, fruit 25.1%, carried 35.7%

### v1-EG-base-2801 (2026-09-29 05:09)

`defaults`, seeds 2801-2812, 1000000 ticks. Expected: standing replication of the default build at 1M ticks: predators persist in about 3 of 4

- worlds 12, meat 17.1%, kill 12.4%, carnSp>0 in 2, preyCl 0.88, persisting (predK >= 64% of run after bootstrap) 10, exits 8, re-entries 2
- fruit: gene 0.198 -> 0.228 (up in 7 of 12), div 0.194, fruit 22.4%, carried 32.0%

### v1-EG-base-2825 (2026-09-29 05:09)

`defaults`, seeds 2825-2836, 1000000 ticks. Expected: standing replication of the default build at 1M ticks: predators persist in about 3 of 4

- worlds 12, meat 18.0%, kill 13.2%, carnSp>0 in 6, preyCl 0.93, persisting (predK >= 64% of run after bootstrap) 8, exits 7, re-entries 4
- fruit: gene 0.187 -> 0.355 (up in 10 of 12), div 0.221, fruit 21.1%, carried 43.6%

### v1-EG-base-2813 (2026-09-29 05:36)

`defaults`, seeds 2813-2824, 1000000 ticks. Expected: standing replication of the default build at 1M ticks: predators persist in about 3 of 4

- worlds 12, meat 17.2%, kill 12.1%, carnSp>0 in 6, preyCl 0.93, persisting (predK >= 64% of run after bootstrap) 9, exits 7, re-entries 3
- fruit: gene 0.189 -> 0.364 (up in 8 of 12), div 0.207, fruit 28.7%, carried 42.1%

### v1-EG-base-2837 (2026-09-29 05:36)

`defaults`, seeds 2837-2848, 1000000 ticks. Expected: standing replication of the default build at 1M ticks: predators persist in about 3 of 4

- worlds 12, meat 18.4%, kill 13.5%, carnSp>0 in 4, preyCl 0.89, persisting (predK >= 64% of run after bootstrap) 8, exits 9, re-entries 3
- fruit: gene 0.199 -> 0.362 (up in 8 of 12), div 0.215, fruit 28.1%, carried 42.4%

### v1-EG-base-2849 (2026-09-29 05:36)

`defaults`, seeds 2849-2860, 1000000 ticks. Expected: standing replication of the default build at 1M ticks: predators persist in about 3 of 4

- worlds 12, meat 18.0%, kill 13.2%, carnSp>0 in 5, preyCl 0.88, persisting (predK >= 64% of run after bootstrap) 8, exits 8, re-entries 2
- fruit: gene 0.198 -> 0.329 (up in 7 of 12), div 0.205, fruit 29.1%, carried 40.6%

### v1-EG-base-2861 (2026-09-29 05:36)

`defaults`, seeds 2861-2872, 1000000 ticks. Expected: standing replication of the default build at 1M ticks: predators persist in about 3 of 4

- worlds 12, meat 19.8%, kill 15.3%, carnSp>0 in 4, preyCl 0.90, persisting (predK >= 64% of run after bootstrap) 8, exits 10, re-entries 4
- fruit: gene 0.191 -> 0.342 (up in 7 of 12), div 0.207, fruit 28.9%, carried 41.2%

### v1-EG-base-2873 (2026-09-29 05:52)

`defaults`, seeds 2873-2884, 1000000 ticks. Expected: standing replication of the default build at 1M ticks: predators persist in about 3 of 4

- worlds 12, meat 16.2%, kill 11.5%, carnSp>0 in 5, preyCl 0.88, persisting (predK >= 64% of run after bootstrap) 7, exits 7, re-entries 2
- fruit: gene 0.200 -> 0.270 (up in 6 of 12), div 0.200, fruit 24.0%, carried 36.7%

### v1-EG-base-2885 (2026-09-29 06:02)

`defaults`, seeds 2885-2896, 1000000 ticks. Expected: standing replication of the default build at 1M ticks: predators persist in about 3 of 4

- worlds 12, meat 17.7%, kill 12.8%, carnSp>0 in 6, preyCl 0.86, persisting (predK >= 64% of run after bootstrap) 8, exits 7, re-entries 4
- fruit: gene 0.193 -> 0.200 (up in 5 of 12), div 0.187, fruit 25.5%, carried 29.6%

### v1-EG-base-2897 (2026-09-29 06:35)

`defaults`, seeds 2897-2908, 1000000 ticks. Expected: standing replication of the default build at 1M ticks: predators persist in about 3 of 4

- worlds 12, meat 16.6%, kill 12.1%, carnSp>0 in 2, preyCl 0.88, persisting (predK >= 64% of run after bootstrap) 8, exits 7, re-entries 3
- fruit: gene 0.194 -> 0.331 (up in 8 of 12), div 0.225, fruit 25.8%, carried 41.6%

### v1-EG-base-2921 (2026-09-29 06:35)

`defaults`, seeds 2921-2932, 1000000 ticks. Expected: standing replication of the default build at 1M ticks: predators persist in about 3 of 4

- worlds 12, meat 15.3%, kill 10.2%, carnSp>0 in 3, preyCl 0.83, persisting (predK >= 64% of run after bootstrap) 5, exits 11, re-entries 4
- fruit: gene 0.194 -> 0.373 (up in 10 of 12), div 0.219, fruit 28.3%, carried 44.5%

### v1-EG-base-2933 (2026-09-29 06:35)

`defaults`, seeds 2933-2944, 1000000 ticks. Expected: standing replication of the default build at 1M ticks: predators persist in about 3 of 4

- worlds 12, meat 19.9%, kill 15.4%, carnSp>0 in 6, preyCl 0.84, persisting (predK >= 64% of run after bootstrap) 12, exits 1, re-entries 0
- fruit: gene 0.193 -> 0.216 (up in 5 of 12), div 0.182, fruit 24.8%, carried 29.3%

### v1-EG-base-2945 (2026-09-29 06:40)

`defaults`, seeds 2945-2956, 1000000 ticks. Expected: standing replication of the default build at 1M ticks: predators persist in about 3 of 4

- worlds 12, meat 20.7%, kill 15.5%, carnSp>0 in 6, preyCl 0.94, persisting (predK >= 64% of run after bootstrap) 11, exits 5, re-entries 1
- fruit: gene 0.197 -> 0.334 (up in 8 of 12), div 0.216, fruit 28.4%, carried 40.3%

### v1-EG-base-2909 (2026-09-29 06:46)

`defaults`, seeds 2909-2920, 1000000 ticks. Expected: standing replication of the default build at 1M ticks: predators persist in about 3 of 4

- worlds 12, meat 15.4%, kill 11.0%, carnSp>0 in 2, preyCl 0.89, persisting (predK >= 64% of run after bootstrap) 7, exits 7, re-entries 2
- fruit: gene 0.197 -> 0.328 (up in 9 of 12), div 0.225, fruit 23.6%, carried 41.8%

### v1-EG-base-2969 (2026-09-29 07:22)

`defaults`, seeds 2969-2980, 1000000 ticks. Expected: standing replication of the default build at 1M ticks: predators persist in about 3 of 4

- worlds 12, meat 15.7%, kill 10.0%, carnSp>0 in 4, preyCl 0.90, persisting (predK >= 64% of run after bootstrap) 6, exits 9, re-entries 1
- fruit: gene 0.193 -> 0.310 (up in 9 of 12), div 0.211, fruit 25.2%, carried 44.7%

### v1-EG-base-2981 (2026-09-29 07:22)

`defaults`, seeds 2981-2992, 1000000 ticks. Expected: standing replication of the default build at 1M ticks: predators persist in about 3 of 4

- worlds 12, meat 18.8%, kill 13.8%, carnSp>0 in 5, preyCl 0.87, persisting (predK >= 64% of run after bootstrap) 10, exits 9, re-entries 7
- fruit: gene 0.191 -> 0.320 (up in 7 of 12), div 0.190, fruit 24.8%, carried 39.0%

### v1-EG-base-2993 (2026-09-29 07:22)

`defaults`, seeds 2993-3004, 1000000 ticks. Expected: standing replication of the default build at 1M ticks: predators persist in about 3 of 4

- worlds 12, meat 14.9%, kill 10.6%, carnSp>0 in 1, preyCl 0.87, persisting (predK >= 64% of run after bootstrap) 6, exits 11, re-entries 3
- fruit: gene 0.202 -> 0.327 (up in 8 of 12), div 0.222, fruit 24.2%, carried 41.3%

### v1-EG-base-2957 (2026-09-29 07:28)

`defaults`, seeds 2957-2968, 1000000 ticks. Expected: standing replication of the default build at 1M ticks: predators persist in about 3 of 4

- worlds 12, meat 20.2%, kill 15.3%, carnSp>0 in 2, preyCl 0.97, persisting (predK >= 64% of run after bootstrap) 10, exits 6, re-entries 1
- fruit: gene 0.198 -> 0.209 (up in 5 of 12), div 0.173, fruit 26.4%, carried 28.2%

### v1-EG-base-3005 (2026-09-29 07:38)

`defaults`, seeds 3005-3016, 1000000 ticks. Expected: standing replication of the default build at 1M ticks: predators persist in about 3 of 4

- worlds 12, meat 15.4%, kill 10.3%, carnSp>0 in 3, preyCl 0.87, persisting (predK >= 64% of run after bootstrap) 10, exits 9, re-entries 1
- fruit: gene 0.192 -> 0.407 (up in 9 of 12), div 0.229, fruit 25.0%, carried 49.4%

### v1-EG-base-3017 (2026-09-29 07:44)

`defaults`, seeds 3017-3028, 1000000 ticks. Expected: standing replication of the default build at 1M ticks: predators persist in about 3 of 4

- worlds 12, meat 18.9%, kill 13.9%, carnSp>0 in 5, preyCl 0.91, persisting (predK >= 64% of run after bootstrap) 8, exits 8, re-entries 5
- fruit: gene 0.191 -> 0.344 (up in 10 of 12), div 0.214, fruit 24.3%, carried 41.8%

### v1-EG-base-3065 (2026-09-29 09:00)

`defaults`, seeds 3065-3076, 1000000 ticks. Expected: standing replication of the default build at 1M ticks: predators persist in about 3 of 4

- worlds 12, meat 19.3%, kill 14.4%, carnSp>0 in 5, preyCl 0.93, persisting (predK >= 64% of run after bootstrap) 8, exits 6, re-entries 2
- fruit: gene 0.195 -> 0.240 (up in 6 of 12), div 0.185, fruit 23.4%, carried 32.7%

### v1-EG-base-3089 (2026-09-29 09:00)

`defaults`, seeds 3089-3100, 1000000 ticks. Expected: standing replication of the default build at 1M ticks: predators persist in about 3 of 4

- worlds 12, meat 20.3%, kill 15.1%, carnSp>0 in 4, preyCl 0.95, persisting (predK >= 64% of run after bootstrap) 9, exits 5, re-entries 0
- fruit: gene 0.201 -> 0.253 (up in 4 of 12), div 0.192, fruit 33.7%, carried 30.7%

### v1-EG-base-3101 (2026-09-29 09:07)

`defaults`, seeds 3101-3112, 1000000 ticks. Expected: standing replication of the default build at 1M ticks: predators persist in about 3 of 4

- worlds 12, meat 17.8%, kill 12.9%, carnSp>0 in 2, preyCl 0.92, persisting (predK >= 64% of run after bootstrap) 11, exits 7, re-entries 2
- fruit: gene 0.201 -> 0.319 (up in 8 of 12), div 0.199, fruit 27.0%, carried 39.3%

### v1-EG-base-3077 (2026-09-29 09:12)

`defaults`, seeds 3077-3088, 1000000 ticks. Expected: standing replication of the default build at 1M ticks: predators persist in about 3 of 4

- worlds 12, meat 15.0%, kill 10.7%, carnSp>0 in 2, preyCl 0.88, persisting (predK >= 64% of run after bootstrap) 7, exits 7, re-entries 3
- fruit: gene 0.197 -> 0.323 (up in 9 of 12), div 0.218, fruit 24.4%, carried 41.5%

### v1-EG-base-3113 (2026-09-29 09:18)

`defaults`, seeds 3113-3124, 1000000 ticks. Expected: standing replication of the default build at 1M ticks: predators persist in about 3 of 4

- worlds 12, meat 17.2%, kill 12.4%, carnSp>0 in 3, preyCl 0.88, persisting (predK >= 64% of run after bootstrap) 10, exits 9, re-entries 6
- fruit: gene 0.191 -> 0.222 (up in 6 of 12), div 0.197, fruit 20.8%, carried 34.5%

### v1-EG-base-3125 (2026-09-29 10:28)

`defaults`, seeds 3125-3136, 1000000 ticks. Expected: standing replication of the default build at 1M ticks: predators persist in about 3 of 4

- worlds 12, meat 17.6%, kill 13.0%, carnSp>0 in 3, preyCl 0.85, persisting (predK >= 64% of run after bootstrap) 8, exits 9, re-entries 3
- fruit: gene 0.194 -> 0.323 (up in 9 of 12), div 0.208, fruit 22.0%, carried 42.1%

### v1-EG-base-3137 (2026-09-29 10:33)

`defaults`, seeds 3137-3148, 1000000 ticks. Expected: standing replication of the default build at 1M ticks: predators persist in about 3 of 4

- worlds 12, meat 17.8%, kill 12.9%, carnSp>0 in 5, preyCl 0.92, persisting (predK >= 64% of run after bootstrap) 10, exits 5, re-entries 2
- fruit: gene 0.201 -> 0.334 (up in 8 of 12), div 0.211, fruit 23.4%, carried 42.5%

### v1-EG-base-3161 (2026-09-29 10:38)

`defaults`, seeds 3161-3172, 1000000 ticks. Expected: standing replication of the default build at 1M ticks: predators persist in about 3 of 4

- worlds 12, meat 17.4%, kill 12.7%, carnSp>0 in 3, preyCl 0.93, persisting (predK >= 64% of run after bootstrap) 9, exits 4, re-entries 1
- fruit: gene 0.197 -> 0.337 (up in 9 of 12), div 0.208, fruit 24.8%, carried 42.4%

### v1-EG-base-3149 (2026-09-29 11:09)

`defaults`, seeds 3149-3160, 1000000 ticks. Expected: standing replication of the default build at 1M ticks: predators persist in about 3 of 4

- worlds 12, meat 19.2%, kill 14.1%, carnSp>0 in 3, preyCl 0.88, persisting (predK >= 64% of run after bootstrap) 8, exits 9, re-entries 3
- fruit: gene 0.191 -> 0.303 (up in 7 of 12), div 0.209, fruit 31.7%, carried 37.1%

### v1-PA60-3065 (2026-09-29 11:09)

`patchy=0.6`, seeds 3065-3076, 1000000 ticks. Expected: pasture in patches (patchy 0.6, patchN 8: 60% of the world barren, about three patches joined by corridors), paired with the standing block of the same seeds. Predator lines are lost in one grazer size sweep across the whole map, and a transplant shows hunting still pays afterwards, so the path back is what is missing. Patches should let a sweep miss one patch or reach it later. Expect: predators persisting (predK >= 64%) in more worlds than the block (baseline 17 of 24 over both blocks), fewer exits, fewer animals (40% of the pasture). If persistence does not rise, a sweep crosses corridors as fast as open ground.

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
    preyCl baseline 0.929  arm 1.738   mean diff +0.810  sign test 12+/0-  p 0.000
    predCl baseline 2.397  arm 2.982   mean diff +0.585  sign test 6+/6-  p 1.000
    diet   baseline 0.091  arm 0.080   mean diff -0.012  sign test 4+/8-  p 0.388
    polar  baseline 0.032  arm 0.051   mean diff +0.019  sign test 12+/0-  p 0.000
    align  baseline 0.101  arm 0.005   mean diff -0.096  sign test 1+/11-  p 0.006
    preySp baseline 0.353  arm 0.302   mean diff -0.051  sign test 7+/5-  p 0.774
    predSp baseline 0.546  arm 0.316   mean diff -0.230  sign test 2+/10-  p 0.039
    learnM baseline 0.879  arm 0.868   mean diff -0.012  sign test 5+/7-  p 0.774

### v1-EG-base-3173 (2026-09-29 11:16)

`defaults`, seeds 3173-3184, 1000000 ticks. Expected: standing replication of the default build at 1M ticks: predators persist in about 3 of 4

- worlds 12, meat 16.3%, kill 11.7%, carnSp>0 in 2, preyCl 0.86, persisting (predK >= 64% of run after bootstrap) 6, exits 10, re-entries 5
- fruit: gene 0.194 -> 0.314 (up in 8 of 12), div 0.211, fruit 23.3%, carried 40.3%

### v1-PA60-3089 (2026-09-29 11:16)

`patchy=0.6`, seeds 3089-3100, 1000000 ticks. Expected: pasture in patches (patchy 0.6, patchN 8: 60% of the world barren, about three patches joined by corridors), paired with the standing block of the same seeds. Predator lines are lost in one grazer size sweep across the whole map, and a transplant shows hunting still pays afterwards, so the path back is what is missing. Patches should let a sweep miss one patch or reach it later. Expect: predators persisting (predK >= 64%) in more worlds than the block (baseline 17 of 24 over both blocks), fewer exits, fewer animals (40% of the pasture). If persistence does not rise, a sweep crosses corridors as fast as open ground.

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
    preyCl baseline 0.949  arm 1.955   mean diff +1.006  sign test 12+/0-  p 0.000
    predCl baseline 2.703  arm 3.932   mean diff +1.228  sign test 9+/3-  p 0.146
    diet   baseline 0.105  arm 0.100   mean diff -0.005  sign test 6+/6-  p 1.000
    polar  baseline 0.032  arm 0.047   mean diff +0.016  sign test 12+/0-  p 0.000
    align  baseline 0.120  arm 0.040   mean diff -0.080  sign test 3+/9-  p 0.146
    preySp baseline 0.385  arm 0.323   mean diff -0.061  sign test 4+/8-  p 0.388
    predSp baseline 0.630  arm 0.417   mean diff -0.213  sign test 3+/9-  p 0.146
    learnM baseline 0.887  arm 0.869   mean diff -0.018  sign test 5+/7-  p 0.774

### v1-EG-base-3185 (2026-09-29 12:02)

`defaults`, seeds 3185-3196, 1000000 ticks. Expected: standing replication of the default build at 1M ticks: predators persist in about 3 of 4

- worlds 12, meat 17.2%, kill 12.0%, carnSp>0 in 5, preyCl 0.87, persisting (predK >= 64% of run after bootstrap) 7, exits 8, re-entries 4
- fruit: gene 0.198 -> 0.342 (up in 8 of 12), div 0.213, fruit 27.7%, carried 41.4%

### v1-EG-base-3233 (2026-09-29 12:33)

`defaults`, seeds 3233-3244, 1000000 ticks. Expected: standing replication of the default build at 1M ticks: predators persist in about 3 of 4

- worlds 12, meat 18.1%, kill 13.4%, carnSp>0 in 5, preyCl 0.85, persisting (predK >= 64% of run after bootstrap) 10, exits 6, re-entries 3
- fruit: gene 0.185 -> 0.333 (up in 9 of 12), div 0.190, fruit 23.9%, carried 39.5%

### v1-EG-base-3209 (2026-09-29 12:43)

`defaults`, seeds 3209-3220, 1000000 ticks. Expected: standing replication of the default build at 1M ticks: predators persist in about 3 of 4

- worlds 12, meat 20.9%, kill 15.6%, carnSp>0 in 4, preyCl 0.96, persisting (predK >= 64% of run after bootstrap) 9, exits 6, re-entries 3
- fruit: gene 0.205 -> 0.314 (up in 6 of 12), div 0.198, fruit 30.3%, carried 36.4%

### v1-EG-base-3197 (2026-09-29 12:59)

`defaults`, seeds 3197-3208, 1000000 ticks. Expected: standing replication of the default build at 1M ticks: predators persist in about 3 of 4

- worlds 12, meat 14.9%, kill 10.3%, carnSp>0 in 2, preyCl 0.85, persisting (predK >= 64% of run after bootstrap) 6, exits 10, re-entries 3
- fruit: gene 0.195 -> 0.355 (up in 9 of 12), div 0.220, fruit 26.2%, carried 42.2%

### v1-EG-base-3221 (2026-09-29 13:19)

`defaults`, seeds 3221-3232, 1000000 ticks. Expected: standing replication of the default build at 1M ticks: predators persist in about 3 of 4

- worlds 12, meat 20.0%, kill 15.3%, carnSp>0 in 4, preyCl 0.90, persisting (predK >= 64% of run after bootstrap) 10, exits 6, re-entries 0
- fruit: gene 0.196 -> 0.237 (up in 5 of 12), div 0.188, fruit 29.8%, carried 30.7%

### v1-EG-base-3245 (2026-09-29 13:30)

`defaults`, seeds 3245-3256, 1000000 ticks. Expected: standing replication of the default build at 1M ticks: predators persist in about 3 of 4

- worlds 12, meat 19.0%, kill 14.5%, carnSp>0 in 4, preyCl 0.91, persisting (predK >= 64% of run after bootstrap) 9, exits 6, re-entries 1
- fruit: gene 0.196 -> 0.220 (up in 4 of 12), div 0.190, fruit 21.8%, carried 32.0%

### v1-EG-base-3257 (2026-09-29 13:51)

`defaults`, seeds 3257-3268, 1000000 ticks. Expected: standing replication of the default build at 1M ticks: predators persist in about 3 of 4

- worlds 12, meat 17.0%, kill 12.1%, carnSp>0 in 3, preyCl 0.84, persisting (predK >= 64% of run after bootstrap) 9, exits 8, re-entries 4
- fruit: gene 0.192 -> 0.358 (up in 9 of 12), div 0.222, fruit 23.7%, carried 44.8%

### v1-DM064-3137 (2026-09-29 14:21)

`dmg=0.64`, seeds 3137-3148, 1000000 ticks. Expected: plain strike damage x1.28 (dmg 0.64, default 0.5): the control for dmgExp 1, the same boost at the pre-crash hunters' size 2.7, paired with the standing block of the same seeds. Expect: persistence up with it too if strength is what saves hunters through a size sweep; less than v1-DX1 in giant worlds if scaling matters.

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
    preyCl baseline 0.915  arm 0.862   mean diff -0.053  sign test 4+/8-  p 0.388
    predCl baseline 2.187  arm 2.829   mean diff +0.642  sign test 7+/5-  p 0.774
    diet   baseline 0.091  arm 0.102   mean diff +0.011  sign test 7+/5-  p 0.774
    polar  baseline 0.032  arm 0.033   mean diff +0.002  sign test 8+/4-  p 0.388
    align  baseline 0.066  arm 0.081   mean diff +0.016  sign test 5+/7-  p 0.774
    preySp baseline 0.341  arm 0.327   mean diff -0.014  sign test 5+/7-  p 0.774
    predSp baseline 0.510  arm 0.533   mean diff +0.023  sign test 7+/5-  p 0.774
    learnM baseline 0.863  arm 0.867   mean diff +0.005  sign test 7+/5-  p 0.774

### v1-DX1-3137 (2026-09-29 15:14)

`dmgExp=1`, seeds 3137-3148, 1000000 ticks. Expected: strike damage x attacker mass^1 (dmgExp 1, default 0.75), paired with the standing block of the same seeds. Hit points are 2 x mass, so at 0.75 a fight at a given size ratio lasts longer the bigger the pair, and grazer size sweeps end predator lines. Pre-crash branches (regen/branch3.js): hunters kept above 20 in 3 of 3 against 2 of 3 as is, but the dmg 0.64 control did as well. Expect: predators persisting in more worlds than the block (pooled baseline for the two blocks 19 of 24), fewer exits; kill share up; if dmg 0.64 (v1-DM064) does as well, it is strength, not scaling.

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
    preyCl baseline 0.915  arm 0.937   mean diff +0.022  sign test 6+/6-  p 1.000
    predCl baseline 2.187  arm 2.742   mean diff +0.555  sign test 7+/5-  p 0.774
    diet   baseline 0.091  arm 0.096   mean diff +0.005  sign test 7+/5-  p 0.774
    polar  baseline 0.032  arm 0.029   mean diff -0.002  sign test 4+/8-  p 0.388
    align  baseline 0.066  arm 0.082   mean diff +0.017  sign test 6+/6-  p 1.000
    preySp baseline 0.341  arm 0.391   mean diff +0.050  sign test 6+/6-  p 1.000
    predSp baseline 0.510  arm 0.586   mean diff +0.076  sign test 7+/5-  p 0.774
    learnM baseline 0.863  arm 0.888   mean diff +0.026  sign test 6+/6-  p 1.000

### v1-DX1-3161 (2026-09-29 15:14)

`dmgExp=1`, seeds 3161-3172, 1000000 ticks. Expected: strike damage x attacker mass^1 (dmgExp 1, default 0.75), paired with the standing block of the same seeds. Hit points are 2 x mass, so at 0.75 a fight at a given size ratio lasts longer the bigger the pair, and grazer size sweeps end predator lines. Pre-crash branches (regen/branch3.js): hunters kept above 20 in 3 of 3 against 2 of 3 as is, but the dmg 0.64 control did as well. Expect: predators persisting in more worlds than the block (pooled baseline for the two blocks 19 of 24), fewer exits; kill share up; if dmg 0.64 (v1-DM064) does as well, it is strength, not scaling.

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
    preyCl baseline 0.928  arm 0.917   mean diff -0.011  sign test 5+/7-  p 0.774
    predCl baseline 2.573  arm 2.297   mean diff -0.276  sign test 5+/7-  p 0.774
    diet   baseline 0.084  arm 0.093   mean diff +0.009  sign test 9+/3-  p 0.146
    polar  baseline 0.031  arm 0.029   mean diff -0.002  sign test 2+/10-  p 0.039
    align  baseline 0.080  arm 0.069   mean diff -0.010  sign test 5+/7-  p 0.774
    preySp baseline 0.363  arm 0.351   mean diff -0.012  sign test 8+/4-  p 0.388
    predSp baseline 0.523  arm 0.557   mean diff +0.033  sign test 7+/5-  p 0.774
    learnM baseline 0.877  arm 0.901   mean diff +0.024  sign test 9+/3-  p 0.146

### v1-DM064-3161 (2026-09-29 15:14)

`dmg=0.64`, seeds 3161-3172, 1000000 ticks. Expected: plain strike damage x1.28 (dmg 0.64, default 0.5): the control for dmgExp 1, the same boost at the pre-crash hunters' size 2.7, paired with the standing block of the same seeds. Expect: persistence up with it too if strength is what saves hunters through a size sweep; less than v1-DX1 in giant worlds if scaling matters.

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
    preyCl baseline 0.928  arm 0.916   mean diff -0.012  sign test 8+/4-  p 0.388
    predCl baseline 2.573  arm 2.052   mean diff -0.521  sign test 3+/9-  p 0.146
    diet   baseline 0.084  arm 0.108   mean diff +0.024  sign test 9+/3-  p 0.146
    polar  baseline 0.031  arm 0.032   mean diff +0.001  sign test 5+/7-  p 0.774
    align  baseline 0.080  arm 0.091   mean diff +0.011  sign test 7+/5-  p 0.774
    preySp baseline 0.363  arm 0.365   mean diff +0.002  sign test 6+/6-  p 1.000
    predSp baseline 0.523  arm 0.571   mean diff +0.048  sign test 8+/4-  p 0.388
    learnM baseline 0.877  arm 0.895   mean diff +0.018  sign test 8+/4-  p 0.388

### v1-EG-base-3269 (2026-09-29 15:20)

`defaults`, seeds 3269-3280, 1000000 ticks. Expected: standing replication of the default build at 1M ticks: predators persist in about 3 of 4

- worlds 12, meat 20.1%, kill 15.5%, carnSp>0 in 4, preyCl 0.90, persisting (predK >= 64% of run after bootstrap) 12, exits 6, re-entries 4
- fruit: gene 0.193 -> 0.259 (up in 8 of 12), div 0.188, fruit 23.4%, carried 33.1%

### v1-EG-base-3281 (2026-09-29 15:51)

`defaults`, seeds 3281-3292, 1000000 ticks. Expected: standing replication of the default build at 1M ticks: predators persist in about 3 of 4

- worlds 12, meat 21.2%, kill 16.0%, carnSp>0 in 6, preyCl 0.93, persisting (predK >= 64% of run after bootstrap) 9, exits 5, re-entries 1
- fruit: gene 0.190 -> 0.293 (up in 7 of 12), div 0.188, fruit 27.2%, carried 34.4%

