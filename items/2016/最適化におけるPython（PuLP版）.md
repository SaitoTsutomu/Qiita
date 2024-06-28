title: 最適化におけるPython（PuLP版）
tags: Python 最適化 組合せ最適化
url: https://qiita.com/SaitoTsutomu/items/070ca9cb37c6b2b492f0
created_at: 2016-08-18 17:17:48+09:00
updated_at: 2024-01-31 10:08:38+09:00
body:

# はじめに
**Python-MIP**版の記事を作成しました。モデラーとしてPuLPよりPython-MIPの方がメリットが多いので、ぜひ、下記の記事も参考にしてください。

- [最適化におけるPython（Python-MIP版）](https://qiita.com/SaitoTsutomu/items/c7b43c2e02710749d117)

# 概要
私は、業務で、組合せ最適化技術を用いたソフトウェア開発(例えば、物流における輸送コストの最小化など)を行っています。以前は、C++やC#を用いて、最適化のモデルを作成していましたが、最近ではPythonを用いることが多いです。
ここでは、最適化におけるPythonについて紹介します。

# Pythonのメリット
Pythonを利用している理由としては、以下のような点があげられます。

- わかりやすい。数式によるモデルとPythonによるモデルが近いため、より本質的な記述に専念でき、保守しやすいモデルを作成できる。
![sample.png](https://qiita-image-store.s3.amazonaws.com/0/13955/e5b72a98-4c4c-bff0-00c4-e260d752bb3f.png)


- 短い記述量で済む。C++などに比べるとプログラムのサイズは、数分の1になる。
- 学習コストが小さい。シンプルな文法で、予約語も少ない。
- Pythonで完結できる。汎用言語であるため、種々の目的の処理もほぼPythonで記述できる。
例えば、webからデータを取得して、集計して、分析して、最適化して、可視化するなど、すべてPythonでできる。
- ライブラリが多い。パッケージコミュニティサイト https://pypi.python.org/pypi だけでも約9万ものパッケージが公開されている。
他にも、https://github.com/ や https://anaconda.org/ にも多くのパッケージが公開されている。
- 様々な環境で実行できる。Windows、Mac、Linuxの各種OSや、処理系もCythonやPypyやIronPythonなどがある。
- 多くの最適化ソフトウェアがPythonに対応している。有料、無料含めて、多くの最適化ソフトウェアが存在しているが、Pythonから利用できるものが多い。

Pythonは、C++などのコンパイラ言語に比べると、実行速度が遅いと言われます。しかし、最適化においては、主にモデルの作成(モデリング)にPythonを用い、最適化アルゴリズムの実行はC++などで記述された専用ソフトウェア(ソルバー)を用います。このため、最適化でPythonを利用しても、実行時間はあまり問題となりません。

最適化のモデリングでは、主にPuLPとpandasパッケージを用いています。

- PuLPは、数理モデリングのパッケージであり、pandasはデータ分析のパッケージである。
- pandasは、モデルに含まれるデータの中で、表で表現できるデータを扱うのに適しており、複雑な処理をわかりやすく記述できる。
また、pandasは内部でnumpyを利用している。
- numpyは、CやFortranで書かれた高度に最適化された線形代数ライブラリを使用しており行列計算を効率よく計算することができる。

# PuLPについて

数理最適化問題を解くためには、以下のステップを行います。

- モデラーで数理モデルを作成します
- ソルバーをよび出して、解を得ます

ソルバーは、数理モデルを入力とし、数理モデルを解いて、変数の値（解）を出力とするソフトウェアです。

![image.png](https://qiita-image-store.s3.amazonaws.com/0/13955/df605726-dbd1-cf5b-632b-6c6b483ea0ef.png)

PuLPはCOINプロジェクトで作成されたソフトウェアで、モデラーになります。
PuLPでは、ソルバーとしてCBC,Gurobi,GLPKなどいろいろなものが使えます。
デフォルトでは、CBCが使われます。PuLPをインストールすると、CBCも同時にインストールされます。

  - CBC: COINプロジェクトの無料ソルバー(COIN-OR Branch and Cut の略)  https://projects.coin-or.org/Cbc
  - Gurobi: 高性能な商用ソルバー http://www.gurobi.com/
  - GLPK: GNU製の無料ソルバー www.gnu.org/software/glpk/

PuLPで扱うことができる問題は、混合整数最適化問題です。
混合整数最適化問題は、数理最適化問題の1種で、下記の特徴があります。

- 連続(実数)変数と整数変数を使って表現される
- 目的関数と制約条件が1次式である

さらに詳細について調べたい場合は、参考サイトを参考にしてください。



# PuLPの使い方
下記の問題を考えてみましょう。

```text:問題
材料AとBから合成できる化学製品XとYをたくさん作成したい。
Xを1kg作るのに、Aが1kg、Bが3kg必要である。
Yを1kg作るのに、Aが2kg、Bが1kg必要である。
また、XもYも1kg当りの価格は100円である。
材料Aは16kg、Bは18kgしかないときに、XとYの価格の合計が最大になるようにするには、
XとYをどれだけ作成すればよいか求めよ。
```

![region.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/13955/ba6f4de8-d74b-c97d-c4bb-8e5e5232d431.png)

問題を数理モデルであらわすと下記のようになります。数理モデルを式で表現することを定式化するといいます。

![formula.png](https://qiita-image-store.s3.amazonaws.com/0/13955/f32472bc-b2c7-5879-5ba8-428db713b2c9.png)

これをPuLPでモデル化して解いてみます。

```py3:python3
from pulp import *
m = LpProblem(sense=LpMaximize) # 数理モデル
x = LpVariable('x', lowBound=0) # 変数
y = LpVariable('y', lowBound=0) # 変数
m += 100 * x + 100 * y # 目的関数
m += x + 2 * y <= 16 # 材料Aの上限の制約条件
m += 3 * x + y <= 18 # 材料Bの上限の制約条件
m.solve() # ソルバーの実行
print(value(x), value(y)) # 4, 6
```

以下、順番に簡単に説明します。

## パッケージのインポート
    from pulp import *

## 数理モデルの作成
    最小化問題のとき: m = LpPrblem()
    最大化問題のとき: m = LpProblem(sense=LpMaximize)

## 変数の作成
    連続変数: x = LpVariable(変数名, lowBound=0)
    0-1変数: x = LpVariable(変数名, cat=LpBinary)
    連続変数のリスト: x = [LpVariable(i番目の変数名, lowBound=0) for i in range(n)]
    変数名は、必ず異なるようにしないといけません

## 目的関数の設定
    m += 式

## 制約条件の追加
    m += 式 == 式
    m += 式 <= 式
    m += 式 >= 式

## 式の例
    2 * x + 3 * y - 5
    和: lpSum(変数のリスト)
    内積: lpDot(係数のリスト, 変数のリスト)

## ソルバーの実行
    m.solve()

## 変数や式や目的関数の値
    value(変数)、value(式)、value(m.objective)


# PuLPとpandasの組合せについて
PuLPとpandasを組合せて、pandasの表(DataFrame)で変数(LpVariable)を管理すると、定式化をわかりやすくできます。

輸送最適化問題を例にしてみてみましょう。

## 輸送最適化問題

> 倉庫群から工場群へ部品を搬送したい。輸送費が最小となる計画を求めたい。

- 倉庫群から工場群への輸送量を決めたい → 変数
- 輸送コストを最小化したい → 目的関数
- 各倉庫からの搬出は、供給可能量以下 → 制約
- 各工場への搬入は、需要量以上 → 制約

<table>
<tr><td rowspan="2" colspan="2">輸送費</td><td colspan="4">組み立て工場</td></tr>
<tr><td>F1</td><td>F2</td><td>F3</td><td>F4</td><td>供給</td></tr>
<tr><td rowspan="3">倉庫</td><td>W1</td><td>10</td><td>10</td><td>11</td><td>17</td><td>35</td></tr>
<tr><td>W2</td><td>16</td><td>19</td><td>12</td><td>14</td><td>41</td></tr>
<tr><td>W3</td><td>15</td><td>12</td><td>14</td><td>12</td><td>42</td></tr>
<tr><td></td><td>需要</td><td>28</td><td>29</td><td>31</td><td>25</td></tr>
</table>

## パラメータの設定
必要なパラメータを設定します。(数字は前表と同じ)

```py3:python3
import numpy as np, pandas as pd
from itertools import product
from pulp import *
np.random.seed(1)
nw, nf = 3, 4
pr = list(product(range(nw),range(nf)))
供給 = np.random.randint(30, 50, nw)
需要 = np.random.randint(20, 40, nf)
輸送費 = np.random.randint(10, 20, (nw,nf))
```

## pandasを使わない数理モデル
変数は、添え字でアクセスします。

```py3:python3
m1 = LpProblem()
v1 = {(i,j):LpVariable('v%d_%d'%(i,j), lowBound=0) for i,j in pr}
m1 += lpSum(輸送費[i][j] * v1[i,j] for i,j in pr)
for i in range(nw):
    m1 += lpSum(v1[i,j] for j in range(nf)) <= 供給[i]
for j in range(nf):
    m1 += lpSum(v1[i,j] for i in range(nw)) >= 需要[j]
m1.solve()
{k:value(x) for k,x in v1.items() if value(x) > 0}
>>>
{(0, 0): 28.0,
 (0, 1): 7.0,
 (1, 2): 31.0,
 (1, 3): 5.0,
 (2, 1): 22.0,
 (2, 3): 20.0}
```

## pandasを使った数理モデル
変数は、表の属性でアクセスできます。まず、表を作成しましょう。

```py3:python3
a = pd.DataFrame([(i,j) for i, j in pr], columns=['倉庫', '工場'])
a['輸送費'] = 輸送費.flatten()
a[:3]
```

<table>
<tr><th></th><th>倉庫</th><th>工場</th><th>輸送費</th></tr>
<tr><th>0</th><td>0</td><td>0</td><td>10</td></tr>
<tr><th>1</th><td>0</td><td>1</td><td>10</td></tr>
<tr><th>2</th><td>0</td><td>2</td><td>11</td></tr>
</table>

同様に数理モデルを作ってみましょう。

```py3:python3
m2 = LpProblem()
a['Var'] = [LpVariable('v%d'%i, lowBound=0) for i in a.index]
m2 += lpDot(a.輸送費, a.Var)
for k, v in a.groupby('倉庫'):
    m2 += lpSum(v.Var) <= 供給[k]
for k, v in a.groupby('工場'):
    m2 += lpSum(v.Var) >= 需要[k]
m2.solve()
a['Val'] = a.Var.apply(value)
a[a.Val > 0]
```

<table>
    <tr>
      <th></th>
      <th>倉庫</th>
      <th>工場</th>
      <th>輸送費</th>
      <th>Var</th>
      <th>Val</th>
    </tr>
    <tr>
      <th>0</th>
      <td>0</td>
      <td>0</td>
      <td>10</td>
      <td>v0</td>
      <td>28.0</td>
    </tr>
    <tr>
      <th>1</th>
      <td>0</td>
      <td>1</td>
      <td>10</td>
      <td>v1</td>
      <td>7.0</td>
    </tr>
    <tr>
      <th>6</th>
      <td>1</td>
      <td>2</td>
      <td>12</td>
      <td>v6</td>
      <td>31.0</td>
    </tr>
    <tr>
      <th>7</th>
      <td>1</td>
      <td>3</td>
      <td>14</td>
      <td>v7</td>
      <td>5.0</td>
    </tr>
    <tr>
      <th>9</th>
      <td>2</td>
      <td>1</td>
      <td>12</td>
      <td>v9</td>
      <td>22.0</td>
    </tr>
    <tr>
      <th>11</th>
      <td>2</td>
      <td>3</td>
      <td>12</td>
      <td>v11</td>
      <td>20.0</td>
    </tr>
</table>

添え字を使った表現は、添え字が何を表しているか覚えていないといけませんでした。しかし、PuLPとpandasを組合せることによって、下記のように、数理モデルが理解しやすくなります。

- 単なる"i"とかではなく、"倉庫"などの列名が使える。
- pandasの条件式を使って、数式を組み立てられる。(参考 [組合せ最適化でN Queen問題を解く](http://qiita.com/Tsutomu-KKE@github/items/8ae87b08668307b58006))
- pandasの便利な関数(groupbyなど)が使える。


# 参考サイト

- Qiita 記事
    - [組合せ最適化を使おう](http://qiita.com/Tsutomu-KKE@github/items/bfbf4c185ed7004b5721)
    - [数理モデルにおける変数の和](http://qiita.com/Tsutomu-KKE@github/items/6701841122acc3130a29)
    - [組合せ最適化ソルバーの威力](http://qiita.com/Tsutomu-KKE@github/items/82831e01adc3f84c36f5)
    - [双対問題を調べる](http://qiita.com/Tsutomu-KKE@github/items/d1812ff9b5ccf0ecc716)
    - [Python+PuLPによるタダで仕事に使える数理最適化](http://qiita.com/samuelladoco/items/703bf78ea66e8369c455)
    - [数理最適化モデラー(PuLP)チートシート(Python)](https://qiita.com/SaitoTsutomu/items/c0bbf6cf8873ccd7edf3)
    - PuLPとpandasの組合せの例
        - [県別データの可視化(4色問題)](http://qiita.com/Tsutomu-KKE@github/items/6d17889ba47357e44131#4%E8%89%B2%E5%95%8F%E9%A1%8C)
        - [組合せ最適化でデートコースを決めよう](http://qiita.com/Tsutomu-KKE@github/items/364786bbcf57c5b922ad)
        - [組合せ最適化でN Queen問題を解く](http://qiita.com/Tsutomu-KKE@github/items/8ae87b08668307b58006)
        - [ハラハラするトーナメントの日程を求めよう](http://qiita.com/Tsutomu-KKE@github/items/402af3ea31c627f21750)
        - [組合せ最適化で学会プログラムを作成する](http://qiita.com/Tsutomu-KKE@github/items/305c171e0c562cad96b8)
        - [レストランの売上を組合せ最適化で最大化する](http://qiita.com/Tsutomu-KKE@github/items/41341ed5a58890c931d2)
        - [最適化で道路設置](http://qiita.com/Tsutomu-KKE@github/items/4d5715f6281be39f51c6)
        - [数独を組合せ最適で解く](http://qiita.com/Tsutomu-KKE@github/items/4f919f453aae95b3834b)
        - [献立を組合せ最適化で考える](http://qiita.com/Tsutomu-KKE@github/items/f8be15f56cbacdbb7bd9)
- Qiita 以外の記事
    - [組合せ最適化(松井先生)](http://tomomi.my.coocan.jp/text/or92b.pdf)(PDF 2ページ)
    - [⼤規模な組合せ最適化問題に対する発⾒的解法(梅谷先生)](http://coop-math.ism.ac.jp/files/4/umetani.pdf)(PDF 51ページ)
- 書籍
    - [「今日から使える!組合せ最適化」](https://www.amazon.co.jp/dp/4061565443/)
    - [「Python言語によるビジネスアナリティクス」](http://logopt.com/python_analytics/)
    - [「モデリングの諸相 (シリーズ:最適化モデリング)」](https://www.amazon.co.jp/dp/4764905191/)
- ソルバー関連
    - [PuLPドキュメント](https://coin-or.github.io/pulp/)
    - [整数計画法メモ(宮代先生)](http://web.tuat.ac.jp/~miya/ipmemo.html)
    - [整数計画法による定式化入門](http://web.tuat.ac.jp/~miya/fujie_ORSJ.pdf)
    - [整数計画ソルバー入門](http://web.tuat.ac.jp/~miya/miyashiro_ORSJ.pdf)
    - [ZIMPL言語とSCIPによる数理最適化](http://ir.acc.senshu-u.ac.jp/?action=pages_view_main&active_action=repository_view_main_item_detail&item_id=9818&item_no=1&page_id=13&block_id=52)
    - [Gurobi Optimizer](https://www.octobersky.jp/products/gurobi/gurobi.html)

---

数理最適化に関するコンサルティングや開発をしています。詳しくは、下記を参照してください。

https://www.beproud.jp/business/mathematical_optimization/

以上

