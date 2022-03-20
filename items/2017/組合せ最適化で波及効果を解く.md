title: 組合せ最適化で波及効果を解く
tags: Python 数学 最適化 パズル 組合せ最適化
url: https://qiita.com/SaitoTsutomu/items/2eab3212beb3bf17ceb7
created_at: 2017-12-22 21:22:11+09:00
updated_at: 2017-12-23 18:12:06+09:00
body:

Advent Calendar 22日目の記事 [組合せ最適化で不等式を解く](https://qiita.com/SaitoTsutomu/items/ed0fe93f9f765262b890)
Advent Calendar 24日目の記事 [組合せ最適化でへやわけを解く](https://qiita.com/SaitoTsutomu/items/82c670fd5aba8bad081d)


## これなに

**波及効果**を、Pythonで[組合せ最適化](https://qiita.com/SaitoTsutomu/items/bfbf4c185ed7004b5721)モデルを作って解きます。
解く楽しみは、モデル化を工夫することになります。

自分でも試してみたい人は、下記を参考にしてください。

- [数独を通して組合せ最適化を学ぼう](https://qiita.com/SaitoTsutomu/items/bd09190d8a02432b3f16)

## 問題
* 各部屋のマスには1からその部屋のマス数までの数を1つずつ入れます
* 同じ数字を同じ横行、または同じ縦列に入れる場合、数字と数字の間にその数字と同じ数以上のマス目がなくてはなりません

下記は、左が問題で、右が答えです。

![](https://raw.githubusercontent.com/SaitoTsutomu/opt4puzzle/master/pic/ripple.png)

### 入力パラメータ

`data`にヒントが入っているとします。

```py3:python
import numpy as np
from pulp import LpProblem, lpSum, lpDot, value
from ortoolpy import addvars, addbinvars
data = """\
...3..
......
..2..4
3..4..
......
..2...""".split()
rms = [[eval(t) for t in s.split('/')] for s in """\
0,0
0,1/0,2/1,2
0,3/1,3/1,4/2,3
0,4
0,5/1,5/2,4/2,5/3,5
1,0/1,1
2,0/3,0/3,1/4,1
2,1/2,2/3,2/4,2
3,3/4,3/5,1/5,2/5,3
3,4
4,0/5,0
4,4/4,5/5,5
5,4""".splitlines()]
nw, nh = len(data[0]), len(data)
na = max(len(rm) for rm in rms)
```

## Pythonで解く

数理モデルを作成し、解きましょう。

### 変数
* v：各位置がどの数字か (1)
* r：各位置の数字 (2)

### 制約
* 数字があれば、その数字 (3)
* 数字は１つのみ (4)
* rをvで表現 (5)
* nマス以内に2つ以上の数字nはないこと (6)
* 各部屋内で同じ数字はないこと (7)

```py3:python
m = LpProblem()
v = addbinvars(nh, nw, na) # (1)
r = addvars(nh, nw) # (2)
def dirs(i, j, k):
    yield from (v[i+l][j][k] for l in range(1, k+2) if i+l < nh)
    yield from (v[i][j+l][k] for l in range(1, k+2) if j+l < nw)
for i in range(nh):
    for j in range(nw):
        if data[i][j].isdigit():
            m += r[i][j] == int(data[i][j]) # (3)
        m += lpSum(v[i][j]) == 1 # (4)
        m += lpDot(range(na), v[i][j]) + 1 == r[i][j] # (5)
        for k in range(na):
            m += lpSum(dirs(i,j,k)) <= 2*(1-v[i][j][k]) # (6)
for rm in rms:
    for k in range(len(rm)):
        m += lpSum(v[i][j][k] for i,j in rm) == 1 # (7)
m.solve()
```

### 結果の表示

```py3:python
print(np.vectorize(value)(r).astype(int))
>>>
[[1 2 1 3 1 2]
 [2 1 3 2 4 1]
 [4 3 2 1 5 4]
 [3 2 1 4 1 3]
 [2 1 4 1 3 1]
 [1 5 2 3 1 2]]
```

解けていることが確認できます。

以上

