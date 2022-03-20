title: 第15回オフラインリアルタイム どう書くの問題をpythonで解いてみた
tags: Python どう書く
url: https://qiita.com/SaitoTsutomu/items/fefd861facc08781a41d
created_at: 2014-06-08 01:51:36+09:00
updated_at: 2014-06-08 01:52:48+09:00
body:

どう書くの問題
https://codeiq.jp/magazine/2013/11/1559/

```python
d = {'1011':'L', '1110':'R', '0111':'J', '111010':'T', '101111':'U', '111101':'N', '011110':'S', '110011':'Z'}
def f(s1, s2, s3):
    t1, t2 = [bin(int(s, 16))[2:].rjust(32, '0') for s in (s1, s2)]
    r = []
    while t1:
        for i in [3, 2]:
            c = d.get(t1[:i] + t2[:i], None)
            if c:
                r.append(c)
                t1, t2 = t1[i - 1:], t2[i - 1:]
                break
        t1, t2 = t1[1:], t2[1:]
    return s3 == ''.join(r)
all([f(*s.split('/')) for s in """
2ed8aeed/34b0ea5b/LTRSUNTSJ
00000200/00000300/L
00018000/00010000/R
00002000/00006000/J
00000700/00000200/T
01400000/01c00000/U
00003800/00002800/N
000c0000/00180000/S
00003000/00001800/Z
132eae6c/1a64eac6/LRJTUNSZ
637572d0/36572698/ZSNUTJRL
baddb607/d66b6c05/LTJZTSSSN
db74cd75/6dac6b57/ZZZTJZRJNU
3606c2e8/1b0d8358/ZZSSLTJ
ad98c306/e6cc6183/UZZZZZZ
4a4aaee3/db6eeaa6/JJLLUUNNS
ecd9bbb6/598cd124/TSSZZTTRR
e0000002/40000003/TL
a0000007/e0000005/UN
c0000003/80000006/RS
40000006/c0000003/JZ
01da94db/00b3b6b2/TSUJLRSR
76eeaaea/24aaeeae/TRNNUUNU
1dacaeee/1566e444/NRJZUTTT
26c9ac60/6c6d66c0/JSZLRJZS
6c977620/36da5360/ZZLLTNZJ
069aeae6/0db34eac/SJSLTUNS
06d53724/049da56c/RRULRNJJ
069b58b0/04d66da0/RLRSLZJR
1b6eced4/11b46a9c/RZZTZNRU
522e8b80/db6ad900/JLLJNLJT
6546cdd0/376c6898/ZULSZRTL
4e6d5b70/6ad9d620/LNSSURST
37367772/65635256/SNSZNTNJ
25535d58/377669cc/LUUSLTUZ
0ae6a55d/0eacedcb/UNSUJUTJ
76762edc/23536a88/TZNZJNRT
""".strip().split('\n')])
```

