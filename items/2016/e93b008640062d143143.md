title: Pythonで物流の可視化
tags: Python Graphviz pandas Jupyter
url: https://qiita.com/SaitoTsutomu/items/e93b008640062d143143
created_at: 2016-07-28 13:52:34+09:00
updated_at: 2016-07-29 13:14:32+09:00
body:

# これなに
流量データの傾向をさくっと見るためのサンプル。

# 元データ
[国交省の物流センサス](http://www.mlit.go.jp/sogoseisaku/transport/butsuryu06100.html)から[都道府県間流動量（品類別）　－重量－](http://www.mlit.go.jp/sogoseisaku/transport/sosei_transport_fr_000074.html)を利用する。
各シートは、平成22年の県別の物流量の重量データ。シートは、合計, 農水, 林業, 鉱産, 金属機械, 化学, 軽工, 雑工, 排出, 特殊の10枚ある。

# 実行環境
graphviz をさくっと使えるように Dockerイメージ([tsutomu7/graphviz](https://hub.docker.com/r/tsutomu7/graphviz/))を用意したので、下記を実行すればよい。

```bash:bash
firefox http://localhost:8888 &
docker run -it --rm -p 8888:8888 tsutomu7/graphviz
```

自前で構築する場合は、[Anaconda](https://www.continuum.io/downloads)インストール後に、"conda install graphviz"と"pip install graphviz"などをする。condaでgraphgvizの本体を、pipでラッパーをインストールする。

# Pythonでやってみる
### データの読込
read_excel で全シートを一度に変数 a に読み込む。a は、0-9をキー、DataFrameが値となる。a[0]は全産業の"合計"のDataFrameとなる。

```py3:python3
import numpy as np, pandas as pd
cat = '合計 農水 林業 鉱産 金属機械 化学 軽工 雑工 排出 特殊'.split()
rng = list(range(len(cat)))
a = pd.read_excel('http://www.mlit.go.jp/sogoseisaku/transport/butsuryucensus/T9-010301.xls',
    rng, skip_footer=1, skiprows=8, header=None, index_col=0, parse_cols=np.arange(1,49))
a[0].ix[:3, :7]
```

<table>
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>1</th>
      <th>2</th>
      <th>3</th>
      <th>4</th>
      <th>5</th>
      <th>6</th>
      <th>7</th>
    </tr>
    <tr>
      <th>1</th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>北　 海 　道</th>
      <td>944271.4669</td>
      <td>6728.8486</td>
      <td>1075.6893</td>
      <td>7623.1429</td>
      <td>2350.6049</td>
      <td>164.8547</td>
      <td>4221.1922</td>
    </tr>
    <tr>
      <th>青　　　　森</th>
      <td>22969.4545</td>
      <td>257605.0057</td>
      <td>12702.7039</td>
      <td>2857.1319</td>
      <td>8079.5519</td>
      <td>750.9524</td>
      <td>1799.4754</td>
    </tr>
    <tr>
      <th>岩　　　　手</th>
      <td>211.2175</td>
      <td>5090.7300</td>
      <td>194668.7805</td>
      <td>10623.9818</td>
      <td>1518.8552</td>
      <td>676.9535</td>
      <td>1244.9179</td>
    </tr>
  </tbody>
</table>

行がFromとなる県、列がToとなる県を表し、47 × 47 の行列となっている。

### 正規化する
各産業ごとに物流量の多い順にソートする。

```py3:python3
prefs = a[0].index.map(lambda x: x.replace('\u3000', ''))
b = [pd.DataFrame([(prefs[i], prefs[j], a[h].iloc[i, j]) for i in range(47) for j in range(47)
    if i != j], columns=['From', 'To', 'Val']).sort_values('Val', ascending=False) for h in rng]
b[0][:3]
```

<table>
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>From</th>
      <th>To</th>
      <th>Val</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>1080</th>
      <td>三重</td>
      <td>愛知</td>
      <td>170322.9506</td>
    </tr>
    <tr>
      <th>1268</th>
      <td>兵庫</td>
      <td>大阪</td>
      <td>165543.7879</td>
    </tr>
    <tr>
      <th>1499</th>
      <td>岡山</td>
      <td>兵庫</td>
      <td>142949.9022</td>
    </tr>
  </tbody>
</table>

### 各産業のトップ5の流量で図を描く
図は、"fig_産業.png"で出力する。流量の数字は、1000トン/年。

```py3:python3
from graphviz import Digraph
from IPython.display import display
for h, c in zip(rng, cat):
    g = Digraph(format='png')
    g.attr('graph', label=c, labelloc='t')
    g.node_attr['fontsize'] = '10'
    for _, r in b[h][:5].iterrows():
        g.edge(r.From, r.To, label='%d'%(r.Val//1000))
    g.render('fig_%s'%c)
    display(g)
```

![fig_合計.png](https://qiita-image-store.s3.amazonaws.com/0/13955/4efdcef3-ee41-89f3-e5dc-d7411a3efe7e.png)
![fig_農水.png](https://qiita-image-store.s3.amazonaws.com/0/13955/42eee3d0-ab8a-1f67-0064-d186f52bdd13.png)
![fig_林業.png](https://qiita-image-store.s3.amazonaws.com/0/13955/91d45b7b-9673-0e5c-3a47-09150d8a87d4.png)
![fig_鉱産.png](https://qiita-image-store.s3.amazonaws.com/0/13955/b2352ef6-6a1e-63c3-f0ec-7ad9dc1cd9a7.png)
![fig_金属機械.png](https://qiita-image-store.s3.amazonaws.com/0/13955/014154f1-981a-e5ca-4447-01bb96d3e0dd.png)
![fig_化学.png](https://qiita-image-store.s3.amazonaws.com/0/13955/358efc6f-0e2c-9b8f-949c-46c88a50d8c3.png)
![fig_軽工.png](https://qiita-image-store.s3.amazonaws.com/0/13955/a144169f-0c3f-f57a-f146-b1fadac0a63e.png)
![fig_雑工.png](https://qiita-image-store.s3.amazonaws.com/0/13955/76e06af8-84c8-3c76-ff37-0167cc384c39.png)
![fig_排出.png](https://qiita-image-store.s3.amazonaws.com/0/13955/465cd54b-d34b-1ea5-3aee-5fff7c01b6ed.png)
![fig_特殊.png](https://qiita-image-store.s3.amazonaws.com/0/13955/01a6cf6c-643a-67ef-0cb7-abb1e793a219.png)


以上


