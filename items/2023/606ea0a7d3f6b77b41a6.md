title: Blenderで重複マテリアルの削除
tags: Python 3DCG Blender
url: https://qiita.com/SaitoTsutomu/items/606ea0a7d3f6b77b41a6
created_at: 2023-01-08 13:08:17+09:00
updated_at: 2023-01-08 13:08:17+09:00
body:

## 1オブジェクトで重複マテリアルを削除する方法

1つのオブジェクトに複数のマテリアルスロットがあるときに、同一のマテリアルを1つにまとめる方法です。

- 編集モードで、`P`（分離）の「マテリアルで」を選ぶ。
- オブジェクトモードで、`Ctrl + J`（統合）

※ 使ってないマテリアルや、空きスロットも削除されます。

## 複数オブジェクトで重複マテリアルがあるときに、1マテリアルに1オブジェクトにする方法

1オブジェクトは1マテリアルまでとし、同じマテリアルの複数オブジェクトを統合する方法です。
分離と統合を繰り返せばできますが、オブジェクトがたくさんあると手間です。
以下のPythonを実行すると、まとめてできます。

```py
from collections import defaultdict
import bpy

objs = [obj for obj in bpy.data.objects if obj.type == "MESH"]
bpy.ops.object.select_all(action="DESELECT")
for obj in objs:
    if len(obj.data.materials) >= 2:
        bpy.context.view_layer.objects.active = obj
        bpy.ops.object.mode_set(mode="EDIT")
        bpy.ops.mesh.separate(type="MATERIAL")
        bpy.ops.object.mode_set(mode="OBJECT")
objs = [obj for obj in bpy.data.objects if obj.type == "MESH"]
dc = defaultdict(list)
for obj in objs:
    if len(obj.data.materials) == 1:
        dc[obj.data.materials[0]].append(obj)
for lst in dc.values():
    if len(lst) >= 2:
        bpy.ops.object.select_all(action="DESELECT")
        bpy.context.view_layer.objects.active = lst[0]
        for obj in lst:
            obj.select_set(True)
        bpy.ops.object.join()
```

以上

