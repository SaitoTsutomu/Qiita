title: Blender 4.2で虹を作る
tags: Python 3DCG Blender
url: https://qiita.com/SaitoTsutomu/items/4ff1e6c1bb9a34a8128b
created_at: 2022-04-24 14:57:14+09:00
updated_at: 2024-10-06 14:34:26+09:00
body:

## 概要

Blenderで虹を作る方法を紹介します。
ポイントは、カラーランプのカラーモードをHSLにすると2色で十分というところです。

<img src="https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/13955/37a047e1-0a3b-6112-7e63-44ed7e4ca2f1.jpeg" width="400">

## 作成方法

細かい手順を説明するよりPythonで実行した方が簡単で間違いもないので、Pythonで作成します。
下記をコピペして実行してください。

```py
"""
Make Rainbow
"""
import bpy

bpy.ops.mesh.primitive_circle_add(
    fill_type='NGON', rotation=(1.5708, -1.5708, 0))
obj = bpy.context.object
mat = bpy.data.materials.new(name="rainbow")
obj.active_material = mat
mat.use_nodes = True
mat.blend_method = "BLEND"
ndtc = mat.node_tree.nodes.new("ShaderNodeTexCoord")
ndtc.location = -800, 250
ndmp = mat.node_tree.nodes.new("ShaderNodeMapping")
ndmp.location = -630, 250
ndmp.inputs[1].default_value = -0.5, -0.5, 0
ndtw = mat.node_tree.nodes.new("ShaderNodeTexWave")
ndtw.location = -450, 250
ndtw.wave_type = "RINGS"
ndtw.rings_direction = "Z"
ndtw.inputs[1].default_value = 0.31
ndgr = mat.node_tree.nodes.new("ShaderNodeTexGradient")
ndgr.location = -450, -80
ndvr = mat.node_tree.nodes.new("ShaderNodeValToRGB")
ndvr.location = -260, 250
ndvr.color_ramp.elements[0].position = 0.949
ndvr.color_ramp.elements[0].color = 0, 0, 0, 0
p1 = ndvr.color_ramp.elements.new(position=0.95)
p1.color = 0.333, 0, 1, 1
ndvr.color_ramp.elements[2].color = 1, 0, 0, 1
ndvr.color_ramp.color_mode = "HSL"
ndvr.color_ramp.hue_interpolation = "FAR"
ndmv = mat.node_tree.nodes.new("ShaderNodeMath")
ndmv.location = -250, -110
ndmv.operation = "MULTIPLY"
ndpb = mat.node_tree.nodes["Principled BSDF"]
ndpb.inputs[0].default_value = 0, 0, 0, 1
ndpb.inputs[2].default_value = 1
ndpb.inputs[27].default_value = 1
mat.node_tree.links.new(ndtc.outputs[0], ndmp.inputs[0])
mat.node_tree.links.new(ndmp.outputs[0], ndtw.inputs[0])
mat.node_tree.links.new(ndmp.outputs[0], ndgr.inputs[0])
mat.node_tree.links.new(ndtw.outputs[1], ndvr.inputs[0])
mat.node_tree.links.new(ndgr.outputs[1], ndmv.inputs[1])
mat.node_tree.links.new(ndvr.outputs[0], ndpb.inputs[26])
mat.node_tree.links.new(ndvr.outputs[1], ndmv.inputs[0])
mat.node_tree.links.new(ndmv.outputs[0], ndpb.inputs[4])
```

参考：[BlenderでPythonを実行する方法](https://qiita.com/SaitoTsutomu/items/cec67381a8789b40e377)

円のオブジェクトの上半分だけ表示しています。

作成した虹のマテリアルは、下記のようになります。

<img src="https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/13955/c9344652-6cb6-f05c-f175-8e529dd583ec.jpeg" width="800">

以上

