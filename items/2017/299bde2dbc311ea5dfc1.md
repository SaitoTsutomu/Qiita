title: ビンパッキング問題に対するアプローチ考
tags: Python 数学 最適化 組合せ最適化
url: https://qiita.com/SaitoTsutomu/items/299bde2dbc311ea5dfc1
created_at: 2017-04-17 17:03:10+09:00
updated_at: 2017-05-16 12:00:43+09:00
body:

# これなに
- ビンパッキング問題に対する、定式化ベースの6つのアプローチの比較。
- 1サンプルなので、一般的とは言い難いが、参考として。
- ソルバーAはCOIN-ORのCBC、ソルバーBは商用ソルバー。

# 対象となるビンパッキング問題

> 20個のいろいろなサイズのアイテムを3つの箱になるべく均等入れたい

# 結果
## 計算時間
アプローチごとの計算時間(ミリ秒)

 |ソルバーA |ソルバーB
--:|--:|--:
アプローチ0|38000|536
アプローチ1|13400|125
アプローチ2|41200|416
アプローチ3|48600|750
アプローチ4|(79)|1150
アプローチ5|694000|484

ただし、アプローチ4のソルバーAは、MIPGAPの設定のためか、最適解ではない。
それ以外は、全て最適解。(アプローチ5は関数近似だが、たまたま厳密解)

## アプローチの概要

- アプローチ0: 平均からの増分の和の最小化
- アプローチ1: 上限で抑える。(上限は、別途ループで探す)
- アプローチ2: 上限で抑える。非対称性の制約条件を追加する。(上限は、別途ループで探す)
- アプローチ3: 最大値の最小化
- アプローチ4: 最小値の最大化
- アプローチ5: 平均からの差分の2乗を線形区分近似

## 考察
- 目的関数を設定せずに、上限で抑える制約条件で平準化するのが、最も高速。ただし、上限を探すためのループが必要なので、トータルでは遅くなる。
- 対称性を崩す制約条件を入れても、場合によっては遅くなる。
- 平均からの増分の和の最小化がよさそう。「最大値の最小化」や「最小値の最大化」より対称性が少ないと思われる。
- 「最大値の最小化」と「最小値の最大化」では、計算時間に差が出る。
- 凸2次関数を区分線形で近似すると、上記アプローチより均等な解が出る可能性があるが、遅くなる。

# Pythonプログラム
## 問題作成

```py3:python3
import numpy as np
from pulp import *
n1, n2 = 3, 20 # 箱数, アイテム数
np.random.seed(1)
a = np.random.randint(1,1000000,n2) # サイズ
a
>>>
array([128038, 491756, 470925, 791625, 491264, 836490, 371404,  73350,
       117584,  21441, 229521, 413826, 966605, 925256, 436974, 293373,
       167303, 513301,  21759, 176486])
```

最も均等にすると、2646029, 2646115, 2646137 に分かれる。

## アプローチ0

```py3:python3
m = LpProblem()
x = [[LpVariable('x%.1d%.2d'%(i,j), cat=LpBinary)
      for j in range(n2)] for i in range(n1)]
y = [LpVariable('y%.1d'%i) for i in range(n1)]
z = LpVariable('z', lowBound=0)
m += z
for j in range(n2):
    m += lpSum(x[i][j] for i in range(n1)) == 1
for i in range(n1):
    m += y[i] == lpDot(a, x[i])
    m += y[i] - sum(a)/n1 <= z
%time m.solve()
print(LpStatus[m.status])
```

## アプローチ1

```py3:python3
m = LpProblem()
x = [[LpVariable('x%.1d%.2d'%(i,j), cat=LpBinary)
      for j in range(n2)] for i in range(n1)]
y = [LpVariable('y%.1d'%i) for i in range(n1)]
for j in range(n2):
    m += lpSum(x[i][j] for i in range(n1)) == 1
for i in range(n1):
    m += y[i] == lpDot(a, x[i])
    m += y[i] <= 2646137
%time m.solve()
print(LpStatus[m.status])
```

## アプローチ2

```py3:python3
m = LpProblem()
x = [[LpVariable('x%.1d%.2d'%(i,j), cat=LpBinary)
      for j in range(n2)] for i in range(n1)]
y = [LpVariable('y%.1d'%i) for i in range(n1)]
for j in range(n2):
    m += lpSum(x[i][j] for i in range(n1)) == 1
for i in range(n1):
    m += y[i] == lpDot(a, x[i])
    m += y[i] <= 2646137
    if i:
        m += y[i-1] <= y[i]
%time m.solve()
print(LpStatus[m.status])
```

## アプローチ3

```py3:python3
m = LpProblem()
x = [[LpVariable('x%.1d%.2d'%(i,j), cat=LpBinary)
      for j in range(n2)] for i in range(n1)]
y = [LpVariable('y%.1d'%i) for i in range(n1)]
z = LpVariable('z') # max
m += z
for j in range(n2):
    m += lpSum(x[i][j] for i in range(n1)) == 1
for i in range(n1):
    m += y[i] == lpDot(a, x[i])
    m += y[i] <= z
%time m.solve()
print(LpStatus[m.status], value(m.objective))
```

## アプローチ4

```py3:python3
m = LpProblem(sense=LpMaximize)
x = [[LpVariable('x%.1d%.2d'%(i,j), cat=LpBinary)
      for j in range(n2)] for i in range(n1)]
y = [LpVariable('y%.1d'%i) for i in range(n1)]
z = LpVariable('z') # min
m += z
for j in range(n2):
    m += lpSum(x[i][j] for i in range(n1)) == 1
for i in range(n1):
    m += y[i] == lpDot(a, x[i])
    m += y[i] >= z
%time m.solve()
print(LpStatus[m.status], value(m.objective))
```

## アプローチ5

```py3:python3
mean = sum(a)/n1
m = LpProblem()
x = [[LpVariable('x%.1d%.2d'%(i,j), cat=LpBinary)
      for j in range(n2)] for i in range(n1)]
y = [LpVariable('y%.1d'%i) for i in range(n1)] # sum
z = [LpVariable('z%.1d'%i) for i in range(n1)] # diff
w = [LpVariable('w%.1d'%i) for i in range(n1)] # cost
m += lpSum(w)
for j in range(n2):
    m += lpSum(x[i][j] for i in range(n1)) == 1
for i in range(n1):
    m += y[i] == lpDot(a, x[i])
    m += z[i] >=  (y[i]-mean)
    m += z[i] >= -(y[i]-mean)
    m += w[i] >= 0.2 * z[i]
    m += w[i] >= 0.5 * z[i] - 7.5
    m += w[i] >=       z[i] - 25
%time m.solve()
print(LpStatus[m.status], value(m.objective))
```

# 参考
- [組合せ最適化を使おう - Qiita](http://qiita.com/SaitoTsutomu/items/bfbf4c185ed7004b5721)
- [最適化におけるPython - Qiita](http://qiita.com/SaitoTsutomu/items/070ca9cb37c6b2b492f0)
- [ビンパッキング問題の解き方 - Qiita](http://qiita.com/SaitoTsutomu/items/3a970e071768bbe96005)
- [ミニサムとかミニマックスって何ですか？ - Qiita](http://qiita.com/SaitoTsutomu/items/0f90e79ad9b29209fbc4)

以上



