title: Pythonによる生産最適化モデルの解説
tags: Python 数学 pandas 最適化 組合せ最適化
url: https://qiita.com/SaitoTsutomu/items/0217097c9fb51a36353c
created_at: 2017-06-29 19:15:59+09:00
updated_at: 2017-09-11 23:40:09+09:00
body:

# はじめに
ここでは、**Pythonで最適化を始めたばかりの人が、理解を深める一助になる**ことを目的としています。

組合せ最適化に関しては、[「組合せ最適化を使おう 」](http://qiita.com/SaitoTsutomu/items/bfbf4c185ed7004b5721)をご覧ください。
モデル、変数、目的関数、制約条件という要素があることを踏まえて進めます。

# 対象者
- Python で最適化を学びたい人
- Excelソルバーなどで、線形最適化を実行したことがある人
- 無料でソルバーを使いたい人
- 典型的な最適化問題の雛形を見たい人

# 対象問題

> 生産最適化問題
原料に限りがある状態で製品を生産して、利益を最大化したい

詳細は、[Google検索](https://www.google.co.jp/search?q=生産計画問題+例題)を見てください。

今回は、元となる入力データは、下記のような表で用意されているものとします。

```:data.csv
,原料1,原料2,原料3,利益
製品1,1,4,3,5
製品2,2,4,1,4
在庫,40,80,50
```

# Pythonコード

```py3:python3
import pandas as pd
from pulp import *
from ortoolpy import addvars
入力表 = pd.read_csv('data.csv', encoding='cp932', index_col=0) # 諸元の読込
変数表,在庫 = 入力表.iloc[:-1,:].copy(),入力表.iloc[-1,:-1] # 2つに分ける
モデル = LpProblem(sense=LpMaximize) # 線形最適化モデル
変数表['変数'] = addvars(len(変数表)) # 生産量を表す変数を表に追加
モデル += lpDot(変数表.利益,変数表.変数) # 総利益を表す目的関数
for 原料 in 変数表.columns[:-2]: # 各製品ごとの処理
    モデル += lpDot(変数表[原料],変数表.変数) <= 在庫[原料] # 原料の使用量が在庫以下
モデル.solve() # ソルバで解を求める
変数表['結果'] = 変数表.変数.apply(value) # 変数の値(結果)を表に追加
print('目的関数',value(モデル.objective)) # 目的関数の表示
print(変数表) # 変数表の表示
```

```:結果
目的関数 95.0
      原料1  原料2  原料3   利益     変数    結果
製品1     1      4     3    5.0   v0001    15.0
製品2     2      4     1    4.0   v0002     5.0
```

# 解説

### パッケージ指定

```py3:python3
import pandas as pd
from pulp import *
from ortoolpy import addvars
```

利用するパッケージを import します。モデルの変数は、変数表の列として表します。

- pandas: 変数表を通してモデルを扱うために使用します。
  - Anaconda利用の場合 pandas はそのまま使えます。そうでない場合「pip install pandas」でインストールできます。
- pulp: 数理最適化モデルを作ることができます。
- ortoolpy: 変数生成関数(addvars)を使用します。
  - このパッケージを使わなくても、pulp.LpVariable でもできます。
- この2つは「pip install pulp ortoolpy」でインストールできます。

### 入力表の読込

```py3:python3
入力表 = pd.read_csv('data.csv', encoding='cp932', index_col=0) # 諸元の読込
```

```py3:ファイルを用意できない場合
from io import StringIO
入力表 = pd.read_table(StringIO("""
	原料1	原料2	原料3	利益
製品1	1	4	3	5
製品2	2	4	1	4
在庫	40	80	50	
"""),index_col=0)
```

必要な諸元をファイルから読込み、入力表とします。pandas.read_csvを使うと、簡単に読込むことができます。

![image.png](https://qiita-image-store.s3.amazonaws.com/0/13955/6d7d3f07-a92e-97c4-74dd-994087b32c33.png)

### 入力表の分割

```py3:python3
変数表,在庫 = 入力表.iloc[:-1,:].copy(),入力表.iloc[-1,:-1] # 2つに分ける
```

上図の青い部分を「変数表」に、緑の部分を「在庫」に代入します。入力表.iloc でスライスを使って、表から自由に取出すことができます。

スライスの詳細は、[Google検索](https://www.google.co.jp/search?q=python+numpy+スライス)を見てください。

### モデルの作成

```py3:python3
モデル = LpProblem(sense=LpMaximize) # 最適化モデル
```

pulp.LpProblem を使って最適化モデル[^1]を作成します。sense=LpMaximize を指定することによって、目的関数を最大化したいことを示します。何も指定しないと最小化になります。

[^1]: 実務家にとって、解決したい状態(問題)と、それを抽象化して解きやすくしたモデルは、きちんと分けて捉えたいものです。研究者は、定式化されたものを発端とするので、問題＝モデルと捉えることが多いようです。LpProblem はモデルに対応します。

### 変数の列の追加

```py3:python3
変数表['変数'] = addvars(len(変数表)) # 生産量を表す変数を表に追加
```

pandas では、「変数表['変数'] = …」で「変数」という名前の新しい列を追加できます。
addvarsでは変数の配列を作成できます。変数表の1行が「1変数とその属性」に対応します。

### 目的関数の追加

```py3:python3
モデル += lpDot(変数表.利益,変数表.変数) # 総利益を表す目的関数
```

pulp では、「モデル += …」で目的関数を設定できます[^2]。
lpDot(c,x) は内積を意味し、$c^T x$になります。

[^2]: 紛らわしいのですが、追加ではありません。2回やっても、2回目だけが有効です。

### 制約条件の追加

```py3:python3
for 原料 in 変数表.columns[:-2]: # 各製品ごとの処理
    モデル += lpDot(変数表[原料],変数表.変数) <= 在庫[原料] # 原料の使用量が在庫以下
```

pulp では、「モデル += … <= 値」で制約条件を追加できます。他には、「>=」や「==」を使えますが、「!=」は使えません。

### ソルバ実行

```py3:python3
モデル.solve() # ソルバで解を求める
```

作成されたモデルは、ソルバと呼ばれる別のプログラムで解くことができます。
pulpでは、いろいろなソルバを指定できます。何も指定しないと無料のCBCというソルバを使って求解します。CBCは、pulpインストール時に一緒にインストールされています。

### 結果の追加

```py3:python3
変数表['結果'] = 変数表.変数.apply(value) # 変数の値(結果)を表に追加
```

ソルバで解くと、value(XXX) で XXX の値を取出すことができます。「変数表.変数.apply(value)」とすることにより変数の列全体にvalueを適用できます。
「変数表['結果'] = …」により新しく結果の列が作られます。

### 結果の表示

```py3:python3
print('目的関数',value(モデル.objective)) # 目的関数の表示
print(変数表) # 変数表の表示
```

```:結果再掲
目的関数 95.0
      原料1  原料2  原料3   利益     変数    結果
製品1     1      4     3    5.0   v0001    15.0
製品2     2      4     1    4.0   v0002     5.0
```

製品1 を 15、製品2 を 5 作ると、総利益が最大の 95 になることがわかります。

# その他
- 環境構築は、[Anaconda](https://www.continuum.io/downloads)が便利です。
- [Jupyter Notebook](http://jupyter.org/) を使うと試行錯誤が捗ります。
- 式の合計は、sumではなく、lpSumを使いましょう。lpSumは$\mathcal{O}(n)$ですが、sumは$\mathcal{O}(n^2)$です。

# 勉強するには
- 書籍を読んだりwebで調べる。
- 勉強会や入門セミナーに参加する。
- 詳しい人に聞く。
- 仕事で使うことにして自分を追い込む。

Let's enjoy Mathematical Optimization!

