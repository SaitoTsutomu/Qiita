title: Blenderで4次元データの可視化
tags: Python 3DCG Blender
url: https://qiita.com/SaitoTsutomu/items/b65306fb9f0f29840ca1
created_at: 2022-03-17 19:46:35+09:00
updated_at: 2022-05-06 20:33:43+09:00
body:

## やること

4次元データのグラフをBlenderで作成してみましょう。
4軸目は、球のサイズにします。

## やってみる

データはダミーで作ります。

```py
import bpy
import numpy as np


def draw(data, scale=0.02):
    mn = data.min()
    mx = data.max()
    data[:, :3] = (data[:, :3] - mn) / (mx - mn) * 2
    for x, y, z, s in data:
        bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=3, radius=s * scale, location=(x, y, z))
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.shade_smooth()
    bpy.ops.mesh.primitive_cylinder_add(vertices=4, radius=0.02, location=(1, 0, 0), rotation=(0, 1.5708, 0))
    bpy.ops.mesh.primitive_cylinder_add(vertices=4, radius=0.02, location=(0, 1, 0), rotation=(1.5708, 0, 0))
    bpy.ops.mesh.primitive_cylinder_add(vertices=4, radius=0.02, location=(0, 0, 1))
    bpy.ops.object.select_all(action='DESELECT')

# 今回は乱数で生成するが、np.loadtxtでCSVから読んでもよい
data = np.random.default_rng(0).uniform(0, 100, (20, 4))
data[:, 3] = data[:, 3] // 10 + 1

draw(data)
```

実行結果

<img src="https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/13955/bce35b9a-91b4-9bf1-ed9e-176bec50896e.jpeg" width="300">

参考：[BlenderでPythonを実行する方法](https://qiita.com/SaitoTsutomu/items/cec67381a8789b40e377)

以上

