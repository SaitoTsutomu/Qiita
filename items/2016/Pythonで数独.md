title: Pythonで数独
tags: Python 数学 パズル 組合せ最適化 数独
url: https://qiita.com/SaitoTsutomu/items/67c253a68360e477937c
created_at: 2016-10-21 16:02:33+09:00
updated_at: 2017-12-03 14:36:01+09:00
body:

# Pythonで数独
数独は、[組合せ最適化](http://qiita.com/SaitoTsutomu/items/bfbf4c185ed7004b5721)で簡単に解ける。
まずは、実行の様子。(事前に、「pip install -U ortoolpy」が必要)

```py3:python
from ortoolpy import sudoku
data = """\
4 . . |. . . |1 . . 
. 5 . |. 3 . |. . 8 
2 . . |7 . 8 |. 9 . 
------+------+------
. 4 5 |6 . . |8 . 1 
. . 3 |. 5 . |. . . 
. 2 . |1 . 3 |. . . 
------+------+------
8 . . |. . 5 |. . . 
. . 4 |. . . |. . . 
. 1 . |. 6 4 |3 . 9 
"""
sudoku(data)[0]
>>>
[[4, 7, 8, 5, 9, 6, 1, 2, 3],
 [6, 5, 9, 2, 3, 1, 7, 4, 8],
 [2, 3, 1, 7, 4, 8, 6, 9, 5],
 [9, 4, 5, 6, 7, 2, 8, 3, 1],
 [1, 8, 3, 4, 5, 9, 2, 6, 7],
 [7, 2, 6, 1, 8, 3, 9, 5, 4],
 [8, 9, 7, 3, 2, 5, 4, 1, 6],
 [3, 6, 4, 9, 1, 7, 5, 8, 2],
 [5, 1, 2, 8, 6, 4, 3, 7, 9]]
```

メソッド sudoku は、81個の「数字またはドット(.)」を入力とし、「解とユニークかどうか」を返す。上記の問題が、ユニークかどうか見てみよう。

```py3:python
sudoku(data, checkOnlyOne=True)[1]
>>>
True
```

Trueなので、ユニーク(解が1つしかない)ということがわかる。
sudokuの中身を見てみよう。

```py3:ipython
sudoku??
```

```py3:出力
def sudoku(s, checkOnlyOne=False):
    """
    sudoku(
    '4 . . |. . . |1 . . '
    '. 5 . |. 3 . |. . 8 '
    '2 . . |7 . 8 |. 9 . '
    '------+------+------'
    '. 4 5 |6 . . |8 . 1 '
    '. . 3 |. 5 . |. . . '
    '. 2 . |1 . 3 |. . . '
    '------+------+------'
    '8 . . |. . 5 |. . . '
    '. . 4 |. . . |. . . '
    '. 1 . |. 6 4 |3 . 9 ')[0]
    """
    import re, pandas as pd
    from itertools import product
    from pulp import LpProblem, lpSum, value
    data = re.sub(r'[^\d.]','',s)
    assert(len(data) == 81)
    r = range(9)
    a = pd.DataFrame([(i,j,(i//3)*3+j//3,k+1,c==str(k+1))
        for (i,j),c in zip(product(r,r),data) for k in r],
        columns=['行','列','_3x3','数','固'])
    a['Var'] = addbinvars(len(a))
    m = LpProblem()
    for cl in [('行','列'),('行','数'),('列','数'),('_3x3','数')]:
        for _,v in a.groupby(cl):
            m += lpSum(v.Var) == 1
    for _,r in a[a.固==True].iterrows():
        m += r.Var == 1
    m.solve()
    if m.status != 1:
        return None, None
    a['Val'] = a.Var.apply(value)
    res = a[a.Val>0.5].数.values.reshape(9,9).tolist()
    if checkOnlyOne:
        fr = a[(a.Val>0.5)&(a.固!=True)].Var
        m += lpSum(fr) <= len(fr)-1
        return res, m.solve()!=1
    return res, None
```

10行ほど定式化して solve を呼ぶだけで解ける。計算時間は、一瞬である。
ユニークかどうかも、最初の解を禁止して解きなおし、もう1つの解がなければユニークである。

## 参考

- [数独を通して組合せ最適化を学ぼう](https://qiita.com/SaitoTsutomu/items/bd09190d8a02432b3f16)
- [組合せ最適化を使おう](https://qiita.com/SaitoTsutomu/items/bfbf4c185ed7004b5721)
- [数理最適化によるパズルの解法](https://qiita.com/SaitoTsutomu/items/0c0db8d22979fc9de8f4)
- [最適化におけるPython](https://qiita.com/SaitoTsutomu/items/070ca9cb37c6b2b492f0)
- [パズルでみる組合せ最適化のテクニック](https://qiita.com/SaitoTsutomu/items/f05f4ff05d4ce6099ff3)

以上

