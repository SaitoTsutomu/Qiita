title: Blenderで隣り合う面に異なる色を割当（四色問題）
tags: Python 3DCG Blender
url: https://qiita.com/SaitoTsutomu/items/8def3fb4b99f8520b6ed
created_at: 2022-01-06 07:50:44+09:00
updated_at: 2022-05-06 20:38:21+09:00
body:

## 隣り合う面に異なる色を割当

実用性は不明ですが、Blenderで面を色で区別する方法を紹介します。

平面で行う場合、四色問題と言われますが、この記事では順番に割り当てるだけなので、厳密に四色問題を解いてはいません。また、平面ではないので五色まで使うことにします。

## 完成図

スザンヌを例にして実行した画面です。オブジェクトはメッシュであれば何でも良いです。見た感じ四色までしか使ってませんね。

<img src="https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/13955/d14d4bfa-7771-58cd-4dd5-2d449f825ba1.jpeg" width="300">


## 手順

- 適当にオブジェクト（例：スザンヌ）を作成します。
- 編集モードに入ります。
- マテリアルのスロットを5つ用意します。
- 5つのマテリアルスロットに`Principled BSDF`を作成し、`Base Color`を変えます。
- 面ごとに隣り合う面と異なるように、色を若番から割り当てます。
- その色のマテリアルを面に設定します。
- オブジェクトモードに戻ります。

## Pythonプログラム

プログラムは下記です。オブジェクトを選択して、Scriptingワークスペースに貼り付けて実行してください。

```py
import bmesh
import bpy

colors = [
    (1, 0.1, 0.1, 1),
    (0.1, 0.2, 1, 1),
    (0.8, 0.8, 0, 1),
    (0, 0.8, 0.1, 1),
    (0.8, 0.2, 0, 1),
]

# スザンヌ作成
bpy.ops.mesh.primitive_monkey_add()
# 編集モード
bpy.ops.object.mode_set(mode="EDIT")
obj = bpy.context.edit_object
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
```

参考：[BlenderでPythonを実行する方法](https://qiita.com/SaitoTsutomu/items/cec67381a8789b40e377)

以上




