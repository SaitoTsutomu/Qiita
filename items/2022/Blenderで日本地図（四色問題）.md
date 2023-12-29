title: Blenderで日本地図（四色問題）
tags: Python 3DCG Blender 地図 四色問題
url: https://qiita.com/SaitoTsutomu/items/2425a51139b79c6d87fa
created_at: 2022-03-20 19:16:48+09:00
updated_at: 2023-12-29 21:25:03+09:00
body:

## これなに

Blenderで日本地図の県ごとにオブジェクトを作り、4色に塗ってみます。


## 完成物

<img src="https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/13955/6550812e-86c2-98a0-1103-29a4bfcfab0d.jpeg" width="600">

- [完成物をSketchfabで見る](https://skfb.ly/otDJR)

## 四色問題を解く

県ごとの色は、数理最適化を用いて四色問題を解いて求めます。
数理最適化については、「[組合せ最適化を使おう](https://qiita.com/SaitoTsutomu/items/bfbf4c185ed7004b5721)」を参考にしてください。

最初、BlenderのPythonで実行したのですが、異常終了してしまったため、色の割り当て（変数`assign`の値）は下記のコードで別途求めました。

```py
from mip import Model
from japanmap import adjacent, get_data

qpqo = get_data()
m = Model()  # 数理モデル
v = m.add_var_tensor((47, 4), "v", var_type="I")
m += v.sum(axis=1) == 1
for ipr in range(47):
    for ad in adjacent(ipr + 1, qpqo):
        if ad > ipr:
            m += v[ipr] + v[ad - 1] <= 1
m.optimize()
assign = (v.astype(float) * range(4)).sum(axis=1).astype(int).tolist()
```

数理最適化は、[Python-MIP](https://www.python-mip.com/)ライブラリーを用いています。
どうも、BlenderとPython-MIPは相性が悪いようです。ちなみに、Blender2.83では動きましたが、Blender2.93以降は動きませんでした。

Python-MIPの使い方については下記を参考にしてください。

- [Python-MIPによるモデル作成方法 - PyQドキュメント](https://docs.pyq.jp/python/math_opt/python_mip.html)

ちなみに、「[Blenderで隣り合う面に異なる色を割当（四色問題）](https://qiita.com/SaitoTsutomu/items/8def3fb4b99f8520b6ed)」の貪欲法で色を求めると長野県のあたりで5色目を使ってたので、定式化して解くことにしました。

## やってみる

県の境界の座標や、県間の隣接関係は、japanmapというライブラリーを用います。
japanmapについては、「[県別データの可視化](https://qiita.com/SaitoTsutomu/items/6d17889ba47357e44131)」を参考にしてください。

Blender上で下記を実行すると、日本地図ができます。

```py
import numpy as np
import bpy
from mathutils import Vector
from japanmap import get_data, pref_points, pref_names

colors = [
    (1, 0.1, 0.1, 1),
    (0.1, 0.2, 1, 1),
    (0.8, 0.8, 0, 1),
    (0, 0.8, 0.1, 1),
]
center = np.array([139.75, 35.68])
assign = [
    0, 2, 0, 2, 1, 0, 3, 0, 2, 1, 3, 2, 0, 2, 2, 1, 0, 3, 1, 0, 2, 3, 1, 0,
    1, 2, 0, 1, 3, 2, 0, 1, 2, 3, 0, 1, 0, 3, 0, 0, 2, 1, 1, 3, 2, 0, 3
]

for i, color in enumerate(colors):
    mat = bpy.data.materials.new(name=f"M{i}")
    mat.use_nodes = True
    mat.node_tree.nodes["Principled BSDF"].inputs["Base Color"].default_value = color
pnts = pref_points(get_data())
for ipr in range(47):
    verts = [Vector(pt + [0]) for pt in (pnts[ipr] - center).tolist()]
    mesh = bpy.data.meshes.new(name=pref_names[ipr + 1])
    mesh.from_pydata(verts, [], np.arange(len(verts))[None, :])
    obj = bpy.data.objects.new(mesh.name, mesh)
    obj.active_material = bpy.data.materials.get(f"M{assign[ipr]}")
    bpy.context.scene.collection.objects.link(obj)
    bpy.context.view_layer.objects.active = obj
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.extrude_region_move(TRANSFORM_OT_translate={"value":(0, 0, 0.2)})
    bpy.ops.transform.resize(value=(0.96, 0.96, 0.96))
    bpy.ops.object.mode_set(mode='OBJECT')
```

参考：[BlenderでPythonを実行する方法](https://qiita.com/SaitoTsutomu/items/cec67381a8789b40e377)

以上



