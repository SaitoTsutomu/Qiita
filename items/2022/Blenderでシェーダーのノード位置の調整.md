title: Blenderでシェーダーのノード位置の調整
tags: Python 3DCG Blender networkx
url: https://qiita.com/SaitoTsutomu/items/ae71dd62aa3fa0067c94
created_at: 2022-04-26 19:37:50+09:00
updated_at: 2022-04-26 19:37:50+09:00
body:

## 概要

Pythonでマテリアルのシェーダーのノード位置を調整してみます。
シェーダーのノード自体をPythonで作成したときに使えるかもしれません（下図は実行例）。

<img src="https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/13955/40987fc2-117d-3588-36ed-5e8d868ad356.png" width="500">

## ロジック

[NetworkX](https://networkx.org/)で有向グラフを作り、マテリアル出力ノードまでの距離ごとにレイヤーを作り、上から配置していきます。

## 実行してみる

対象のマテリアルの名前を`Material`としたとき、下記を実行すると位置を調整します。
NetworkXのインストールが必要です。

```py
import bpy
import networkx as nx
from collections import defaultdict

# 有向グラフの作成
g = nx.DiGraph()
m = bpy.data.materials["Material"]
for link in m.node_tree.links:
    g.add_edge(link.from_node, link.to_node)

# 出力までの距離を算出
mo = m.node_tree.nodes["Material Output"]
dist = nx.shortest_path_length(g, None, mo)

posy = defaultdict(int)  # 現在のY座標
for nd in m.node_tree.nodes:
    d = dist[nd]  # ノードの距離（レイヤー）
    nd.location = -d * 300, posy[d]
    posy[d] -= 300
```

ノードの幅と高さの属性が（有効な値として）使えなかったので固定値にしています。

以上

