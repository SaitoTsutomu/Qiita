title: 組合せ最適化でN Queen問題を解く
tags: Python 最適化 パズル 組合せ最適化
url: https://qiita.com/SaitoTsutomu/items/8ae87b08668307b58006
created_at: 2016-05-29 19:13:02+09:00
updated_at: 2016-05-29 20:41:53+09:00
body:

# N Queen問題とは

> N × Nの盤上に、N個のクイーンを配置する。このとき、
どの駒も他の駒に取られるような位置においてはいけない。

この問題も[組合せ最適化](http://qiita.com/Tsutomu-KKE@github/items/bfbf4c185ed7004b5721)で解けます。

## 定式化
<table>
<tr><td>目的関数</td><td>なし</td><td></td></tr>
<tr><td >変数</td><td>$x_j \in \{0,  1\} ~ ~ \forall j \in 各マス$</td><td>そのマスに置くかどうか</td></tr>
<tr><td rowspan="4">制約条件</td><td>$\sum_{j \in 各マス~~~~~}{\{x_j|縦がi列\}} = 1 ~ ~ \forall i \in \{0, \cdots, N-1\}$</td><td>1列に1つ</td></tr>
<tr><td>$\sum_{j \in 各マス~~~~~}{\{x_j|横がi行\}} = 1 ~ ~ \forall i \in \{0, \cdots, N-1\}$</td><td>1行に1つ</td></tr>
<tr><td>$\sum_{j \in 各マス~~~~~}{\{x_j|縦+横がi\}} \le 1 ~ ~ \forall i \in \{0, \cdots, 2 N-2\}$</td><td>斜めは1つ以下</td></tr>
<tr><td>$\sum_{j \in 各マス~~~~~}{\{x_j|縦-横がi-N+1\}} \le 1 ~ ~ \forall i \in \{0, \cdots, 2 N-2\}$</td><td>斜めは1つ以下</td></tr>
</table>


## Pythonで解いてみる
定式化して解いてみましょう。

```py3:python3
%matplotlib inline
import pandas as pd, matplotlib.pyplot as plt
from itertools import product
from ortoolpy import addvar
from pulp import *
def NQueen(N):
    r = range(N)
    m = LpProblem()
    a = pd.DataFrame([(i, j, addvar(cat=LpBinary))
        for i, j in product(r, r)], columns=['縦', '横', 'x'])
    for i in r:
        m += lpSum(a[a.縦 == i].x) == 1
        m += lpSum(a[a.横 == i].x) == 1
    for i in range(2*N-1):
        m += lpSum(a[a.縦 + a.横 == i].x) <= 1
        m += lpSum(a[a.縦 - a.横 == i-N+1].x) <= 1
    %time m.solve()
    return a.x.apply(value).reshape(N, -1)
for N in [8, 16, 32, 64, 128]:
    plt.imshow(NQueen(N), cmap='gray', interpolation='none')
    plt.show()
>>>
CPU times: user 4 ms, sys: 4 ms, total: 8 ms
Wall time: 27.5 ms

CPU times: user 16 ms, sys: 4 ms, total: 20 ms
Wall time: 84.4 ms

CPU times: user 48 ms, sys: 4 ms, total: 52 ms
Wall time: 272 ms

CPU times: user 236 ms, sys: 0 ns, total: 236 ms
Wall time: 1.88 s

CPU times: user 956 ms, sys: 20 ms, total: 976 ms
Wall time: 11.3 s
```
![image](https://qiita-image-store.s3.amazonaws.com/0/13955/374f936c-4bcb-6f4f-e229-2d9ea16523e9.png)

以上

