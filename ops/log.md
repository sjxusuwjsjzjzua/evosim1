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

