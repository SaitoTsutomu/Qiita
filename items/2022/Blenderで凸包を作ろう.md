title: Blenderで凸包を作ろう
tags: Python 3DCG Blender
url: https://qiita.com/SaitoTsutomu/items/fae863598c5110a5c8d4
created_at: 2022-01-10 11:42:10+09:00
updated_at: 2022-05-06 20:37:59+09:00
body:

## Blenderで凸包を作ろう

頂点座標だけ与えられているとき、その凸包を確認したいとします。
ここでは、Blenderを使って凸包を作成してみましょう。

## やり方

編集モードで頂点を選択し、メッシュメニューの「凸包」で凸包が作成できます。
デフォルトでは、凸包に使われなかった頂点は削除されます。細かい調整は、左下に表示されるオペレーションパネルでできます。

以下は、「凸包」機能に気づく前に作成したものです。参考までに残しておきます。

## SciPyを使う方法

### 準備

SciPyとmore-itertoolsを使います。
[Blenderのコマンドサンプル](https://qiita.com/SaitoTsutomu/items/6b70367455f843a979b1)を参考にして、下記のようにインストールしてください。

```bash
blender_pip install scipy more-itertools
```

### ランダムデータで確認

以下では、ランダムな30個の頂点を作成し、その凸包を作成しています。
Scriptingワークスペースで新規作成して、コピペして実行してください。

```py
from typing import Any, Iterable

import bpy
import numpy as np
from mathutils import Vector
from more_itertools import pairwise
from scipy.spatial import ConvexHull


def add_convex_hull(points: Iterable[Any], name: str = "") -> None:
    """凸包のオブジェクトを作成する

    :param points: 頂点のイテラブル
    :param name: 名前
    """
    ch = ConvexHull(points)
    ar = np.c_[ch.simplices, ch.simplices[:, 0]]
    verts = [Vector(pt) for pt in points]
    edges = list(set(tuple(sorted(j)) for i in ar for j in pairwise(i)))
    faces = ch.simplices
    mesh = bpy.data.meshes.new(name=name or "ConvexHull")
    mesh.from_pydata(verts, edges, faces)
    obj = bpy.data.objects.new(mesh.name, mesh)
    bpy.context.layer_collection.collection.objects.link(obj)


if __name__ == "__main__":
    points = np.random.random((30, 3))
    add_convex_hull(points)
```

参考：[BlenderでPythonを実行する方法](https://qiita.com/SaitoTsutomu/items/cec67381a8789b40e377)

#### 実行例

<img src="https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/13955/720e1dfd-d4b3-189d-1ed3-fc8a09d10a17.jpeg" width="400">

#### 補足

簡単に試したところ、面は全て三角形面でした。もし、多角形面にしたければ、編集モードの削除の「限定的溶解」でできるかもしれません。

以上

