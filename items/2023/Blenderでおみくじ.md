title: Blenderでおみくじ
tags: Python 3DCG Blender
url: https://qiita.com/SaitoTsutomu/items/883bc3cda561355093f6
created_at: 2023-02-18 17:26:48+09:00
updated_at: 2023-02-18 17:26:48+09:00
body:

## はじめに

Blenderでおみくじを引いてみましょう。

## おみくじを作る

Pythonでおみくじを作ります。下記のコードをコピーして実行してみましょう。

Pythonの実行方法は、次を参考にしてみてください。

https://qiita.com/SaitoTsutomu/items/cec67381a8789b40e377

```python
import random
from math import pi

import bpy


def get_font():
    search_list = [
        ("Meiryo Regular", "/Windows/Fonts/Meiryo.ttc"),
        ("Hiragino Sans GB W3", "/System/Library/Fonts/Hiragino Sans GB.ttc"),
    ]
    for f, l in search_list:
        if not (font := bpy.data.fonts.get(f)):
            try:
                font = bpy.data.fonts.load(l)
            except RuntimeError:
                pass
        if font:
            return font


def main():
    # みくじ文字用マテリアル
    mat1 = bpy.data.materials.new(name="text")
    mat1.use_nodes = True
    ndpb = mat1.node_tree.nodes["Principled BSDF"]
    ndpb.inputs[0].default_value = mat1.diffuse_color = 0, 0, 0, 1
    # みくじ棒用マテリアル
    mat2 = bpy.data.materials.new(name="stick")
    mat2.use_nodes = True
    ndpb = mat2.node_tree.nodes["Principled BSDF"]
    ndpb.inputs[0].default_value = mat2.diffuse_color = 0.8, 0.5, 0.2, 1
    text_list = "大吉 中吉 小吉 吉 末吉".split()
    for i, s in enumerate(random.sample(text_list, len(text_list))):
        # みくじ文字
        bpy.ops.object.text_add(location=(-0.85, 0, 1.2), rotation=(pi / 2, 0, 0))
        txt = bpy.context.object
        txt.data.body = s
        txt.data.font = get_font()
        txt.active_material = mat1
        # 100mのみくじ棒を作成
        bpy.ops.mesh.primitive_cylinder_add(
            vertices=6, radius=10, depth=100, location=(i * 0.5 - 1, 0, 0.5)
        )
        # みくじ棒
        stk = bpy.context.object
        stk.active_material = mat2
        txt.parent = stk  # みくじ棒をみくじ文字の親に
        bpy.ops.transform.resize(value=(0.01, 0.01, 0.01))  # みくじ棒を1/100倍に
    # 白板
    bpy.ops.mesh.primitive_plane_add(location=(0, 0.01, 1.5), rotation=(pi / 2, 0, 0))
    bpy.ops.transform.resize(value=(1, 1, 0.5))
    bpy.context.object.select_set(state=False)
    bpy.context.view_layer.objects.active = None


main()
```

実行すると、下記のようになります。

![image.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/13955/42ba0965-4308-b6da-c6d1-e6bb458e1543.png)

## おみくじを引いてみよう

5本の「**みくじ棒**」から1本を選び、削除してください。文字が表示されます。

![image.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/13955/f39d62c4-b580-98b1-b140-d5ec88e49d11.png)

## 文字が表示されるしくみ

1つの**みくじ棒**は、100mの長さで作られます。そのみくじ棒に対応した文字を子供にして、1/100倍にリサイズします。
このとき、子供の文字も1/100倍になります。そして親のみくじ棒が削除されると、子供は元の大きさに戻るので表示されるようになります。

## さいごに

神社の雰囲気を出したり、アニメーションにしてもいいかもしれません。

以上

