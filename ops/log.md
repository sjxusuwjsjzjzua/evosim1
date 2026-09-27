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

