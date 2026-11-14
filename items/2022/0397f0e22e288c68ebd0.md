title: Blenderの「辺ループのブリッジ」
tags: Python 3DCG Blender
url: https://qiita.com/SaitoTsutomu/items/0397f0e22e288c68ebd0
created_at: 2022-09-19 09:35:43+09:00
updated_at: 2022-09-19 09:35:43+09:00
body:

## 概要

Blenderの「辺ループのブリッジ」を紹介します。
2つの面を選んで辺ループのブリッジをすると、面をブリッジすることができます。
下図は、2つの球の面をランダムに選んでブリッジを作成したものです。30回繰り返しています。

<img src="https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/13955/470034ff-a6fc-2033-2214-75e7debe164e.png" width=500">

## Pythonで実行

下記では、`bpy.ops.mesh.bridge_edge_loops(number_cuts=20)`で辺ループのブリッジをしています。`number_cuts`はブリッジの分割数です。最後にスムーズとサブディビジョンサーフェスをかけて紐っぽくしています。面の向きによっては内側を通るので穴が空いたようになります。

```py
import numpy as np
import bmesh
import bpy
import random

def center(face):
    return tuple(np.round(face.calc_center_median(), 4))

bpy.ops.object.mode_set(mode="OBJECT")
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False)
bpy.ops.outliner.orphans_purge(do_recursive=True)

bpy.ops.mesh.primitive_uv_sphere_add()
bpy.ops.mesh.primitive_uv_sphere_add(location=(4, 0, 0))
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.join()
bpy.ops.object.transform_apply(location=True)
obj = bpy.context.object

st1, st2 = set(), set()

for _ in range(30):
    bpy.ops.object.mode_set(mode="OBJECT")
    bpy.ops.object.mode_set(mode="EDIT")
    bpy.ops.mesh.select_mode(type='FACE')
    bpy.ops.mesh.select_all(action="DESELECT")
    bm = bmesh.from_edit_mesh(obj.data)
    bm.faces.ensure_lookup_table()

    if not st1:
        for face in bm.faces:
            p = center(face)
            if abs(p[2]) < 0.8:
                if p[0] < 2:
                    st1.add(p)
                else:
                    st2.add(p)

    for st in [st1, st2]:
        while True:
            f = random.choice(bm.faces)
            p = center(f)
            if p in st:
                st.remove(p)
                f.select_set(True)
                break
    bpy.ops.mesh.bridge_edge_loops(number_cuts=20)
    bm.free()

bpy.ops.object.mode_set(mode="OBJECT")
bpy.ops.object.shade_smooth(use_auto_smooth=True)
bpy.ops.object.modifier_add(type='SUBSURF')
bpy.context.object.modifiers["Subdivision"].levels = 2
```

以上

