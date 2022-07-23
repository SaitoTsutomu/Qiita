title: Blenderで2つのオブジェクトの頂点の差分を調べる
tags: Python 3DCG Blender
url: https://qiita.com/SaitoTsutomu/items/8b40d349511e63f64081
created_at: 2022-05-08 20:17:53+09:00
updated_at: 2022-05-08 22:38:51+09:00
body:

## 概要

Blenderでメッシュが微妙に異なる2つのオブジェクトがあったときに、差分を選択状態にして可視化する方法を紹介します。
なお、シェイプキーがある場合は、先頭のシェイプキーを対象にします。
また、オブジェクトは、頂点数が異なっていても大丈夫です。

## 手順

頂点座標をイミュータブルにして積集合を作り、積集合に入ってない頂点を選択します。

```py
import bpy


def main():
    """2つのオブジェクトの差分を選択"""
    if len(bpy.context.selected_objects) != 2:
        print("2つのオブジェクトを選択してください")
        return
    obj1, obj2 = bpy.context.selected_objects
    bpy.ops.object.mode_set(mode="EDIT")  # for deselect
    bpy.ops.mesh.select_all(action="DESELECT")
    bpy.ops.object.mode_set(mode="OBJECT")  # for select
    vtx1 = [vert.co.to_tuple(4) for vert in obj1.data.vertices]
    vtx2 = [vert.co.to_tuple(4) for vert in obj2.data.vertices]
    st = set(vtx1) & set(vtx2)
    for vtx, vert in zip(vtx1, obj1.data.vertices):
        vert.select = vtx not in st
    for vtx, vert in zip(vtx2, obj2.data.vertices):
        vert.select = vtx not in st
    bpy.ops.object.mode_set(mode="EDIT")


if __name__ == "__main__":
    main()
```

参考：[BlenderでPythonを実行する方法](https://qiita.com/SaitoTsutomu/items/cec67381a8789b40e377)

`bpy.ops.mesh.select_all(action="DESELECT")`せずに、下記だけでもできそうですが、うまくいきませんでした。

```py
        vert.select = vtx not in st
```

すべて非選択にしてからオブジェクトモードに戻らないと反映されないようです。

以上

