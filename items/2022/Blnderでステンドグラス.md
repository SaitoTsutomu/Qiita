title: Blnderでステンドグラス
tags: Python 3DCG Blender
url: https://qiita.com/SaitoTsutomu/items/7acee5298cd25c80a757
created_at: 2022-12-23 21:13:38+09:00
updated_at: 2022-12-31 13:11:05+09:00
body:

## 概要

YouTubeの[ささらBch](https://www.youtube.com/@sasara_Bch)さんの「[【ステンドグラス】Blender M01-100](https://www.youtube.com/watch?v=Phx2CpsyjBE)」のアレンジです。

下記のようなステンドグラス化したスザンヌを作成します。

<img src="https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/13955/921994ff-39d7-882d-1bbe-17b79fcd36d5.png" width="300">

ポイントは、カラーランプのカラーモードをHSVにすると2色設定するだけでいろいろな色になるところです。

参考：[Blenderで虹を作る](https://qiita.com/SaitoTsutomu/items/4ff1e6c1bb9a34a8128b)

## 作成方法

細かい手順を説明するよりPythonで実行した方が簡単で間違いもないので、Pythonで作成します。
下記をコピペして実行してください。

```py
import bpy

bpy.ops.mesh.primitive_monkey_add()
bpy.ops.object.modifier_add(type='WIREFRAME')
obj = bpy.context.object
mat = bpy.data.materials.new(name="frame")
obj.active_material = mat
mat.use_nodes = True
ndpb = mat.node_tree.nodes["Principled BSDF"]
ndpb.inputs[0].default_value = (0, 0, 0, 1)

bpy.ops.mesh.primitive_monkey_add()
obj = bpy.context.object
mat = bpy.data.materials.new(name="frame")
obj.active_material = mat
mat.use_nodes = True
ndpb = mat.node_tree.nodes["Principled BSDF"]
ndoi = mat.node_tree.nodes.new("ShaderNodeObjectInfo")
ndoi.location = -500, -110
ndcr = mat.node_tree.nodes.new("ShaderNodeValToRGB")
ndcr.location = -300, -110
ndcr.color_ramp.color_mode = 'HSV'
ndcr.color_ramp.hue_interpolation = 'CW'
ndcr.color_ramp.elements[0].color = (1, 0, 0, 1)
ndcr.color_ramp.elements[1].color = (1, 0, 0.01, 1)

mat.node_tree.links.new(ndoi.outputs[5], ndcr.inputs[0])
mat.node_tree.links.new(ndcr.outputs[0], ndpb.inputs[19])

bpy.ops.object.editmode_toggle()
bpy.ops.mesh.edge_split(type='EDGE')
bpy.ops.mesh.separate(type='LOOSE')
bpy.ops.object.editmode_toggle()
```

参考：[BlenderでPythonを実行する方法](https://qiita.com/SaitoTsutomu/items/cec67381a8789b40e377)

作成したマテリアルは、下記のようになります。

<img src="https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/13955/045e1184-1d78-ef98-2aa2-069586141a33.png" width="600">

## 補足

下記のようにマテリアルでワイヤーフレームを表示させることもできます。

![image.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/13955/6f631921-14c8-0aa1-5ccf-7bf51654bee7.png)

以上

