title: 献立を組合せ最適化で考える
tags: Python 数学 最適化 組合せ最適化
url: https://qiita.com/SaitoTsutomu/items/f8be15f56cbacdbb7bd9
created_at: 2016-01-04 15:39:40+09:00
updated_at: 2016-01-04 16:10:06+09:00
body:

# <i class='fa fa-graduation-cap' /> 問題
医者から1週間の食事のカロリー制限をしなさいと言われました。
また、必要な栄養素A、栄養素Bの最低取得量も指示されました。
なるべく、好きなものを食べるにはどうしたらいいでしょうか？

# <i class='fa fa-graduation-cap' /> 定式化
[組合せ最適化問題](http://qiita.com/Tsutomu-KKE@github/items/bfbf4c185ed7004b5721)の中の割当問題になります。
料理の候補は与えられているものとし、その中からどれを選ぶかを0-1変数$x$で表すことにしましょう。

<table>
<tr><td>変数</td><td>$x_i \in \{0, 1\}$</td><td>$i$番目の料理を選ぶかどうか</td></tr>
<tr><td>目的関数</td><td>$\sum_i{好み_i x_i}$</td><td>$\rightarrow$ 最大</td></tr>
<tr><td>制約条件</td><td>$\sum_i{x_i} = 7 $</td><td>7日分を選ぶ</td></tr>
<tr><td></td><td>$\sum_i{カロリー_i x_i} \le 90 $</td><td>カロリー制限</td></tr>
<tr><td></td><td>$\sum_i{栄養素A_i x_i} \ge 95 $</td><td>最低取得量</td></tr>
<tr><td></td><td>$\sum_i{栄養素B_i x_i} \ge 95 $</td><td>最低取得量</td></tr>
</table>

# <i class='fa fa-graduation-cap' /> pythonで解いてみる
最適化ライブラリは、[pulp](http://qiita.com/Tsutomu-KKE@github/items/bfbf4c185ed7004b5721#%E3%82%BD%E3%83%95%E3%83%88%E3%81%AE%E3%82%A4%E3%83%B3%E3%82%B9%E3%83%88%E3%83%BC%E3%83%AB)を使います。
まず、ダミーデータを作成してみましょう。

```py3:python
import numpy as np, pandas as pd
from pulp import *
menu = ['牛丼', '親子丼', 'カツ丼', '鉄火丼', 'ねぎとろ丼', 'ちらし寿司',
        '麻婆茄子', 'ドリア', 'オムライス', 'チャーハン', 'カレーライス']
n = len(menu)
np.random.seed(1)
a = pd.DataFrame({
        '料理名': menu,
        'カロリー': np.random.randint(10,20,n),
        '栄養素A': np.random.randint(10,20,n),
        '栄養素B': np.random.randint(10,20,n),
        '好み': np.random.randint(10,20,n),
    })
print(a)
```

 |料理名|好み|カロリー|栄養素A|栄養素B
:--|:--|--:|--:|--:|--:
0|牛丼|18|15|14|10
1|親子丼|13|18|15|16
2|カツ丼|19|19|12|19
3|鉄火丼|18|15|14|19
4|ねぎとろ丼|17|10|12|17
5|ちらし寿司|13|10|14|16
6|麻婆茄子|16|11|17|19
7|ドリア|15|17|17|11
8|オムライス|11|16|19|10
9|チャーハン|19|19|11|11
10|カレーライス|13|12|17|18

解いてみましょう。

```py3:python
m = LpProblem(sense=LpMaximize) # 最大化問題
a['x'] = [LpVariable('x%d'%i, cat=LpBinary) for i in range(n)] # 選択する/しない
m += lpDot(a.好み, a.x) # 好みを最大化
m += lpSum(a.x) == 7 # 1週間分の献立
m += lpDot(a.カロリー, a.x) <= 90
m += lpDot(a.栄養素A, a.x) >= 95
m += lpDot(a.栄養素B, a.x) >= 95
m.solve()
if m.status == 1: # Optimal
    a['val'] = a.x.apply(lambda v: value(v)) # 結果
    print(a[a.val == 1].料理名)
>>>
0         牛丼
3        鉄火丼
4      ねぎとろ丼
5      ちらし寿司
6       麻婆茄子
7        ドリア
10    カレーライス
```

# <i class='fa fa-graduation-cap' /> Docker
Dockerでちょっと試してみたい場合、下記を実行してブラウザでホストを開くと、Jupyterが起動します。ライブラリも[いろいろインストール](https://hub.docker.com/r/tsutomu7/jupyter/)しています。

    docker run -d -p 80:8888 tsutomu7/jupyter

以上

