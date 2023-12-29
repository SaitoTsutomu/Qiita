title: Blenderで球面上の頂点から凸包を作り色を割り当てよう
tags: Python 3DCG Blender 数学 モデリング
url: https://qiita.com/SaitoTsutomu/items/7bd7aba2eaffd4bca440
created_at: 2022-01-10 14:12:41+09:00
updated_at: 2023-12-29 21:32:25+09:00
body:

## やること

- 球面上にランダムに頂点を作成します。
- [Blenderで凸包を作ろう](https://qiita.com/SaitoTsutomu/items/fae863598c5110a5c8d4)を使って、頂点から凸包を作ります。
- [Blenderで隣り合う面に異なる色を割当（四色問題）](https://qiita.com/SaitoTsutomu/items/8def3fb4b99f8520b6ed)を使って、凸包に色を割り当てます。

### 実行例

<img src="https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/13955/8eeb63d7-9acd-9af4-d1b9-83acc4dd9e2e.jpeg" width="300">

## Pythonのコード

30個の頂点を球面上にランダムに作成し、凸包を作って色を割り当てます。
Scriptingワークスペースで新規作成してコピペして実行してください。

```py
import bmesh
import bpy
import numpy as np
from mathutils import Vector


def rand_sphere(radius):
    while True:
        x = np.random.randn(3)
        r = np.linalg.norm(x)
        if r:
            return x / r * radius


def add_vertex_on_sphere(n: int, radius: float = 1, name: str = ""):
    """球面上にランダムに頂点を作成し凸包にする

    :param n: 頂点数
    :param radius: 半径
    :param name: 名前
    """
    pts = [rand_sphere(radius) for _ in range(n)]
    mesh = bpy.data.meshes.new(name=name or "Sphere")
    mesh.from_pydata([Vector(pt) for pt in pts], [], [])
    obj = bpy.data.objects.new(mesh.name, mesh)
    bpy.context.scene.collection.objects.link(obj)
    bpy.context.view_layer.objects.active = obj
    bpy.ops.object.mode_set(mode="EDIT")
    bpy.ops.mesh.convex_hull()
    bpy.ops.object.mode_set(mode="OBJECT")
    return obj


def set_five_color(obj):
    """隣り合う面に異なる色を割当"""
    colors = [
        (1, 0.1, 0.1, 1),
        (0.1, 0.2, 1, 1),
        (0.8, 0.8, 0, 1),
        (0, 0.8, 0.1, 1),
        (0.8, 0.2, 0, 1),
    ]
    bpy.context.view_layer.objects.active = obj
    # 編集モード
    bpy.ops.object.mode_set(mode="EDIT")
    bm = bmesh.from_edit_mesh(obj.data)
    # マテリアルのスロットを5つ用意
    for _ in range(len(colors) - len(obj.material_slots)):
        bpy.ops.object.material_slot_add()
    # 5つのマテリアルを作成
    for i, color in enumerate(colors):
        material = f"M{i}"
        mat = bpy.data.materials.get(material) or bpy.data.materials.new(name=material)
        mat.use_nodes = True
        mat.node_tree.nodes["Principled BSDF"].inputs["Base Color"].default_value = color
        obj.active_material_index = i
        obj.active_material = mat
    # 面ごとに隣り合う面と異なるように、色を若番から割当
    n = len(bm.faces)
    res = [0] * n
    dj = [[] for _ in range(n)]  # 面ごとの禁止領域リスト
    for edge in bm.edges:
        if len(edge.link_faces) == 2:
            i = edge.link_faces[0].index
            j = edge.link_faces[1].index
            dj[max(i, j)].append(min(i, j))
    for i in range(n):
        res[i] = ({1, 2, 3, 4, 5} - {res[j] for j in dj[i]}).pop()
    # 色のマテリアルを面に設定
    for face, i in zip(bm.faces, res):
        if i:
            obj.active_material_index = i - 1
            bpy.ops.mesh.select_all(action="DESELECT")
            face.select = True
            bpy.ops.object.material_slot_assign()
    bm.free()
    # オブジェクトモード
    bpy.ops.object.mode_set(mode="OBJECT")


if __name__ == "__main__":
    obj = add_vertex_on_sphere(30)
    set_five_color(obj)
```

参考：[BlenderでPythonを実行する方法](https://qiita.com/SaitoTsutomu/items/cec67381a8789b40e377)

以上

