title: 最適化におけるPython（Python-MIP版）
tags: Python 最適化 組合せ最適化 python-mip
url: https://qiita.com/SaitoTsutomu/items/c7b43c2e02710749d117
created_at: 2022-06-12 14:30:27+09:00
updated_at: 2024-01-31 10:08:33+09:00
body:

# はじめに
この記事は、「[最適化におけるPython（PuLP版）](https://qiita.com/SaitoTsutomu/items/070ca9cb37c6b2b492f0)」で使っているモデラーのPuLPを[Python-MIP](https://www.python-mip.com/)に置き換えたものです。
どちらのモデラーもデフォルトのソルバーはCBCで使い勝手もほぼ同じですが、Python-MIPは下記の利点があります。

- ソルバーとのインターフェースに[CFFI](https://cffi.readthedocs.io/)を用いていて高速です。
- [PyPy](https://www.pypy.org/)が使えます。Python部分の実行速度も向上できる可能性があります。
- ベクトル（NumPyの多次元配列）で制約条件を書けます。PuLPでは`for`を使わないといけない制約条件を`for`を使わずにシンプルに書けます。[サンプル](https://docs.python-mip.com/en/latest/examples.html)
- PuLPよりわかりやすくモデルを作成できます。
  - 目的関数の設定でobjectiveを明記してわかりやすい。
  - 最大化か最小化を目的関数で指定できてわかりやすい。
  - 目的関数の設定が`=`なのでわかりやすい（PuLPでは、追加でないのに`+=`）。
  - モデルのクラス名がModelでわかりやすい（PuLPでは、LpProblem）。
  - 多次元配列で変数を作成でき、制約条件もブロードキャストで書ける。
  - 変数名を省略できる。また、同じ変数名でもエラーにならず、ちゃんと解ける（PuLPで同じ変数名を使うと意味不明のエラーメッセージが出る）。
  - `式 != 式`を制約条件にするとエラーになる（PuLPはならない）。


# 概要
私は、業務で、組合せ最適化技術を用いたソフトウェア開発(例えば、物流における輸送コストの最小化など)を行っています。以前は、C++やC#を用いて、最適化のモデルを作成していましたが、最近ではPythonを用いることが多いです。
ここでは、最適化におけるPythonについて紹介します。

# Pythonのメリット
Pythonを利用している理由としては、以下のような点があげられます。

- わかりやすい。数式によるモデルとPythonによるモデルが近いため、より本質的な記述に専念でき、保守しやすいモデルを作成できる。

<img src="https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/13955/9782482a-798f-3461-fbb8-84b9c957620c.png" width="700">

- 短い記述量で済む。C++などに比べるとプログラムのサイズは、数分の1になる。
- 学習コストが小さい。シンプルな文法で、予約語も少ない。
- Pythonで完結できる。汎用言語であるため、種々の目的の処理もほぼPythonで記述できる。
例えば、webからデータを取得して、集計して、分析して、最適化して、可視化するなど、すべてPythonでできる。
- ライブラリが多い。パッケージコミュニティサイト（https://pypi.org/ ）で約40万ものパッケージが公開されている。
- 様々な環境で実行できる。Windows、Mac、Linuxの各種OSや、処理系もCythonやPyPyなどがある。
- 多くの最適化ソフトウェアがPythonに対応している。有料、無料含めて、多くの最適化ソフトウェアが存在しているが、Pythonから利用できるものが多い。

Pythonは、C++などのコンパイラ言語に比べると、実行速度が遅いと言われます。しかし、最適化においては、主にモデルの作成(モデリング)にPythonを用い、最適化アルゴリズムの実行はC++などで記述された専用ソフトウェア(ソルバー)を用います。このため、最適化でPythonを利用しても、実行時間はあまり問題となりません。

最適化のモデリングでは、主にPython-MIPとpandasパッケージを用いています。

- Python-MIPは、数理モデリングのパッケージであり、pandasはデータ分析のパッケージである。
- pandasは、モデルに含まれるデータの中で、表で表現できるデータを扱うのに適しており、複雑な処理をわかりやすく記述できる。
また、Python-MIPとpandasは内部でNumPyを利用している。
- NumPyは、CやFortranで書かれた高度に最適化された線形代数ライブラリを使用しており行列計算を効率よく計算することができる。

# Python-MIPについて

数理最適化問題を解くためには、以下のステップを行います。

- モデラーで数理モデルを作成します
- ソルバーをよび出して、解を得ます

ソルバーは、数理モデルを入力とし、数理モデルを解いて、変数の値（解）を出力とするソフトウェアです。

<img src="https://qiita-image-store.s3.amazonaws.com/0/13955/df605726-dbd1-cf5b-632b-6c6b483ea0ef.png" width="400">

Python-MIPは、モデラーになります。
Python-MIPでは、ソルバーとしてCBC,Gurobiなどいろいろなものが使えます。
デフォルトでは、CBCが使われます。Python-MIPをインストールすると、CBCも同時にインストールされます。

  - CBC: COINプロジェクトの無料ソルバー(COIN-OR Branch and Cut の略)  https://projects.coin-or.org/Cbc
  - Gurobi: 高性能な商用ソルバー http://www.gurobi.com/

Python-MIPで扱うことができる問題は、混合整数最適化問題です。
混合整数最適化問題は、数理最適化問題の1種で、下記の特徴があります。

- 連続(実数)変数と整数変数を使って表現される
- 目的関数と制約条件が1次式である

さらに詳細について調べたい場合は、参考サイトを参考にしてください。

# Python-MIPの使い方

下記の問題を考えてみましょう。

```text:問題
材料AとBから合成できる化学製品XとYをたくさん作成したい。
Xを1kg作るのに、Aが1kg、Bが3kg必要である。
Yを1kg作るのに、Aが2kg、Bが1kg必要である。
また、XもYも1kg当りの価格は100円である。
材料Aは16kg、Bは18kgしかないときに、XとYの価格の合計が最大になるようにするには、
XとYをどれだけ作成すればよいか求めよ。
```

<img src="https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/13955/ba6f4de8-d74b-c97d-c4bb-8e5e5232d431.png" width="200">

問題を数理モデルであらわすと下記のようになります。数理モデルを式で表現することを定式化するといいます。

<img src="https://qiita-image-store.s3.amazonaws.com/0/13955/f32472bc-b2c7-5879-5ba8-428db713b2c9.png" width="300">

これをPython-MIPでモデル化して解いてみます。

```py:python
from mip import Model, maximize, minimize, xsum

m = Model()  # 数理モデル
# 変数
x = m.add_var("x")
y = m.add_var("y")
# 目的関数
m.objective = maximize(100 * x + 100 * y)
# 制約条件
m += x + 2 * y <= 16  # 材料Aの上限
m += 3 * x + y <= 18  # 材料Bの上限
m.optimize()  # ソルバーの実行
print(x.x, y.x)
>>>
4.0 6.0
```

以下、順番に簡単に説明します。

## パッケージのインポート
```py
from mip import Model, maximize, minimize, xsum
```

## 数理モデルの作成
```py
m = Model()
```

## 変数の作成
```py
x = m.add_var(変数名)
```

主な変数の作り方です。
- 非負の連続変数：`m.add_var(変数名)`
- 自由変数：`m.add_var(変数名, lb=-np.inf)`
- 0-1変数：`m.add_var(変数名, var_type="B")`
- 非負の整数変数：`m.add_var(変数名, var_type="I")`
- `n`個の非負の連続変数のベクトル：`m.add_var_tensor((n,), 変数名)`
- 非負の連続変数の多次元配列：`m.add_var_tensor(形状, 変数名)`
- `n`個の0-1変数のベクトル：`m.add_var_tensor((n,), 変数名, var_type="B")`
- 0-1変数の多次元配列：`m.add_var_tensor(形状, 変数名, var_type="B")`

※ 形状は、多次元配列の`shape`を意味します。1次元（ベクトル）の形状は、`(n,)`のように書きます。

## 目的関数の設定
```py
# 最小化
m.objective = minimize(式)

# 最大化
m.objective = maximize(式)
```

## 制約条件の追加
```py
m += 式 == 式
m += 式 <= 式
m += 式 >= 式
```

## 式の例

式は、数式のように書けます。また、`add_var_tensor()`の戻り値は、NumPyの多次元配列の派生クラス（LinExprTensor）なので、NumPyと同様に記述できます。
和や内積は、`sum()`も使えますが、`xsum()`の方が効率的です（参考「[数理モデルにおける変数の和](https://qiita.com/SaitoTsutomu/items/6701841122acc3130a29)」）。

```py
2 * x + 3 * y - 5

# 和
xsum(変数のベクトル)

# 内積
xsum(係数のベクトル * 変数のベクトル)
```

## ソルバーの実行
```py
m.optimize()
```
ソルバーを実行すると、ソルバーのログが出力されますが、下記をするとログ出力を抑制できます。
```py
m.verbose = 0
```

## 変数や式や目的関数の値
ソルバーを実行して、 `m.status.value == 0` であれば、下記のようにして変数などの値を取得できます。

```py
x.x  # 変数xの値
y.x  # 変数yの値
(2 * x + 3 * y - 5).x  # 式の値
m.objective.x  # 目的関数の値
v.astype(float)  # 変数の多次元配列vの値
```

# Python-MIPとpandasの組合せについて
Python-MIPとpandasを組合せて、pandasの表(DataFrame)で変数(Var)を管理すると、シンプルでわかりやすくモデルを作成できます。

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
<tr><td rowspan="3">倉庫</td><td>W1</td><td>10</td><td>11</td><td>18</td><td>16</td><td>47</td></tr>
<tr><td>W2</td><td>19</td><td>15</td><td>16</td><td>19</td><td>42</td></tr>
<tr><td>W3</td><td>17</td><td>16</td><td>15</td><td>15</td><td>40</td></tr>
<tr><td></td><td>需要</td><td>25</td><td>26</td><td>20</td><td>21</td></tr>
</table>

## パラメータの設定
必要なパラメータを設定します。(数字は前表と同じ)

```py
import numpy as np
import pandas as pd
from mip import Model, minimize, xsum

nw = 3  # 倉庫数
nf = 4  # 工場数
rnd = np.random.default_rng(0)
供給 = rnd.integers(30, 50, nw)
需要 = rnd.integers(20, 40, nf)
輸送費 = rnd.integers(10, 20, (nw, nf))
```

## pandasを使わない数理モデル
変数に添字でアクセスします。

```py
m1 = Model()
v1 = m1.add_var_tensor((nw, nf), "v1")
expr = xsum(xsum(v) for v in 輸送費 * v1)
m1.objective = minimize(expr)
for i in range(nw):
    m1 += xsum(v1[i]) <= 供給[i]
for j in range(nf):
    m1 += xsum(v1[:, j]) >= 需要[j]
m1.verbose = 0
m1.optimize()
v1.astype(float)
>>>
LinExprTensor([[25., 22.,  0.,  0.],
               [ 0.,  4.,  1.,  0.],
               [ 0.,  0., 19., 21.]])
```

## pandasを使った数理モデル
変数を表に持つことで、変数を表の属性でアクセスできます。まずは、表を作成しましょう。

```py
dfw = pd.DataFrame({"倉庫": ["W1", "W2", "W3"], "供給": 供給})
dff = pd.DataFrame({"工場": ["F1", "F2", "F3", "F4"], "需要": 需要})
df = pd.merge(dfw, dff, "cross").assign(輸送費=輸送費.flatten())
df
```

| |倉庫|供給|工場|需要|輸送費|
|--:|:--|--:|:--|--:|--:|
|0|W1|47|F1|25|10|
|1|W1|47|F2|26|11|
|2|W1|47|F3|20|18|
|3|W1|47|F4|21|16|
|4|W2|42|F1|25|19|
| ... | ...  | ...  |   ... |  ... |  ... |

同様に数理モデルを作って解いてみましょう。

```py
m2 = Model()
df["Var"] = m2.add_var_tensor((len(df),), "v2")
m2.objective = minimize(xsum(df.輸送費 * df.Var))
for _, gr in df.groupby('倉庫'):
    m2 += xsum(gr.Var) <= gr.供給.iloc[0]
for _, gr in df.groupby('工場'):
    m2 += xsum(gr.Var) >= gr.需要.iloc[0]
m2.verbose = 0
m2.optimize()
df["Val"] = df.Var.astype(float)
df[df.Val > 0]
```

|    | 倉庫   | 工場   |   輸送費 |   供給 |   需要 |   Var |   Val |
|---:|:-------|:-------|---------:|-------:|-------:|------:|------:|
|  0 | W0     | F0     |       10 |     47 |     25 |  v2_0 |    25 |
|  1 | W0     | F1     |       11 |     47 |     26 |  v2_1 |    22 |
|  5 | W1     | F1     |       15 |     42 |     26 |  v2_5 |     4 |
|  6 | W1     | F2     |       16 |     42 |     20 |  v2_6 |     1 |
| 10 | W2     | F2     |       15 |     40 |     20 | v2_10 |    19 |
| 11 | W2     | F3     |       15 |     40 |     21 | v2_11 |    21 |

添え字を使った表現は、添え字が何を表しているか覚えていないといけませんでした。しかし、Python-MIPとpandasを組合せることによって、下記のように、数理モデルが理解しやすくなります。

- 実務ではスパース（疎）なデータが多い。表にすることでスパースなデータでも扱いやすくなる。
- 変数が持つ属性が行を見ればわかる。
- 単なる`i`とかではなく、`倉庫`などの列名が使える。
- pandasの条件式を使って、数式を組み立てられる。(参考 [組合せ最適化でN Queen問題を解く](https://qiita.com/SaitoTsutomu/items/8ae87b08668307b58006))
- pandasの便利な関数(`groupby`や`merge`や`join`など)が使える。

# 参考サイト

- Qiita 記事
    - [組合せ最適化を使おう](https://qiita.com/SaitoTsutomu/items/bfbf4c185ed7004b5721)
    - [数理モデルにおける変数の和](https://qiita.com/SaitoTsutomu/items/6701841122acc3130a29)
    - [組合せ最適化ソルバーの威力](https://qiita.com/SaitoTsutomu/items/82831e01adc3f84c36f5)
    - [Python-MIPのLinExprTensor.astype()をDataFrameの列に追加したときの考察](https://qiita.com/SaitoTsutomu/items/4f409507b04ddda4fb7c)
    - [双対問題を調べる](http://qiita.com/SaitoTsutomu/items/d1812ff9b5ccf0ecc716)
    - [今度こそ？使い物になるフリーの数理最適化（混合整数最適化）ソルバー（付きインターフェース） Python-MIP](https://qiita.com/keisukesato-ac/items/f2fb63140b80226ba687)
- Qiita 以外の記事
    - [Python-MIPによるモデル作成方法](https://docs.pyq.jp/python/math_opt/python_mip.html)
    - [組合せ最適化(松井先生)](http://tomomi.my.coocan.jp/text/or92b.pdf)(PDF 2ページ)
    - [⼤規模な組合せ最適化問題に対する発⾒的解法(梅谷先生)](http://coop-math.ism.ac.jp/files/4/umetani.pdf)(PDF 51ページ)
- 書籍
    - [「今日から使える!組合せ最適化」](https://www.kspub.co.jp/book/detail/1565449.html)
    - [「Python言語によるビジネスアナリティクス」](http://logopt.com/python_analytics/)
    - [「モデリングの諸相 (シリーズ:最適化モデリング)」](https://www.kindaikagaku.co.jp/book_list/detail/9784764905191/)
    - [データ分析ライブラリーを用いた最適化モデルの作り方](https://www.kindaikagaku.co.jp/book_list/detail/9784764905801/)
- ソルバー関連
    - [Python-MIP ドキュメント](https://docs.python-mip.com/en/latest/index.html)
    - [整数計画法メモ(宮代先生)](http://web.tuat.ac.jp/~miya/ipmemo.html)
    - [整数計画法による定式化入門](http://web.tuat.ac.jp/~miya/fujie_ORSJ.pdf)
    - [整数計画ソルバー入門](http://web.tuat.ac.jp/~miya/miyashiro_ORSJ.pdf)
    - [Gurobi Optimizer](https://www.octobersky.jp/products/gurobi)

---

数理最適化に関するコンサルティングや開発をしています。詳しくは、下記を参照してください。

https://www.beproud.jp/business/mathematical_optimization/

以上

