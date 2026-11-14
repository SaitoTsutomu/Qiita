title: 組合せ最適化 - 典型問題 - 重みマッチング問題
tags: Python 最適化 組合せ最適化
url: https://qiita.com/SaitoTsutomu/items/bbebc69ebc2549b0d5d2
created_at: 2015-07-11 01:32:17+09:00
updated_at: 2023-12-24 08:01:50+09:00
body:

[典型問題と実行方法](0f6c1a4415d196e64314)

# 重みマッチング問題

重みマッチング問題は、「最大重みマッチング問題、最大重み最大マッチング問題、最大重み完全マッチング問題、最小重み最大マッチング問題、最小重み完全マッチング問題」などの総称である。

重みマッチング問題|問題種類|マッチングした辺数
:--|:--|:--
最大重みマッチング問題|最大化|任意
最大重み最大マッチング問題|最大化|最大マッチング問題と等しくなければいけない
最大重み完全マッチング問題|最大化|点数の半分でなければいけない
最小重み最大マッチング問題|最小化|最大マッチング問題と等しくなければいけない
最小重み完全マッチング問題|最小化|点数の半分でなければいけない

- 重みは全て0以上とする。
- 最小重みマッチング問題は、**空**が自明な最適解なので、通常、検討対象としない。
- 「最大重みマッチング問題と最大重み最大マッチング問題と最小重み最大マッチング問題」において重みが全て1のとき、単に「[最大マッチング問題](http://qiita.com/SaitoTsutomu/items/37262bef6f2cab331e01)」とよぶ。
- 「最大重み完全マッチング問題と最小重み完全マッチング問題」において重みが全て1のとき、単に「完全マッチング問題」とよぶ。
- 最小重み最大マッチング問題と最小重み完全マッチング問題は、当該重みを「重みの最大ー当該重み」に変えれば、最大重み最大マッチング問題と最大重み完全マッチング問題に帰着できる。
- 最大重み完全マッチング問題は、最大重み最大マッチング問題の解が完全マッチングになっている場合のみ解となる。
- これらのことから、最大重みマッチング問題と最大重み最大マッチング問題の解法があればよいことになる。
- 最大重みマッチング問題は、下記の max_weight_matching (エドモンズ法)で解ける。
- 最大重み最大マッチング問題を解く場合、下記の max_weight_matching で maxcardinality=True を指定すればよい。
- グラフが2部グラフの場合、一般のグラフより高性能の(ハンガリー法などの)アルゴリズムが存在する（参考「[二部グラフの最小重み完全マッチング](https://qiita.com/manman4/items/fdd56b76051e9a0331d1)」）。

##最大重みマッチング問題

無向グラフ$G=(V,E)$に対し、各辺$e \in E$の重み$w(e)$が与えられているとき、$\sum_{e \in M}{w(e)}$が最大のマッチング$M$を求めよ。

##実行方法(最大重みマッチング問題)

```text:usage
Signature: nx.max_weight_matching(G, maxcardinality=False)
Docstring:
Compute a maximum-weighted matching of G.

A matching is a subset of edges in which no node occurs more than once.
The cardinality of a matching is the number of matched edges.
The weight of a matching is the sum of the weights of its edges.
```

```python:python
# CSVデータ
import pandas as pd, networkx as nx, matplotlib.pyplot as plt
from ortoolpy import graph_from_table, networkx_draw
tbn = pd.read_csv('data/node0.csv')
tbe = pd.read_csv('data/edge0.csv')
g = graph_from_table(tbn, tbe)[0]
d = nx.max_weight_matching(g)
pos = networkx_draw(g)
nx.draw_networkx_edges(g, pos, width=3, edgelist=[(i, j) for i, j in d])
plt.show()
print(d)
```

```text:結果
{5: 1, 1: 5, 0: 2, 2: 0, 4: 3, 3: 4}
```

![mwm2.png](https://qiita-image-store.s3.amazonaws.com/0/13955/68ac3c74-9fbd-7ce1-8b3c-5d200c25b6b4.png)

```python:python
# pandas.DataFrame
from ortoolpy.optimization import MaxWeightMatching
MaxWeightMatching('data/edge0.csv')
```

<table>
  <thead>
    <tr>
      <th></th>
      <th>node1</th>
      <th>node2</th>
      <th>capacity</th>
      <th>weight</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>0</td>
      <td>2</td>
      <td>2</td>
      <td>4</td>
    </tr>
    <tr>
      <th>1</th>
      <td>1</td>
      <td>5</td>
      <td>2</td>
      <td>5</td>
    </tr>
    <tr>
      <th>2</th>
      <td>3</td>
      <td>4</td>
      <td>2</td>
      <td>4</td>
    </tr>
  </tbody>
</table>

```python:python
# 乱数データ
import networkx as nx, matplotlib.pyplot as plt
from ortoolpy import networkx_draw
g = nx.random_graphs.fast_gnp_random_graph(10, 0.3, 1)
for i, j in g.edges():
    g.adj[i][j]['weight'] = 1
d = nx.max_weight_matching(g)
pos = networkx_draw(g, nx.spring_layout(g))
nx.draw_networkx_edges(g, pos, width=3, edgelist=[(i, j) for i, j in d])
plt.show()
```

![mwm.png](https://qiita-image-store.s3.amazonaws.com/0/13955/3669538d-0084-6407-112d-28d3807aaea4.png)

##データ
- [data/node0.csv](https://www.dropbox.com/s/7v4x2ypbgkj52vr/node0.csv)
- [data/edge0.csv](https://www.dropbox.com/s/2vryg0i2kb76mic/edge0.csv)

