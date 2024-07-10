title: Blenderで鉄板を作成
tags: Python 3DCG addon Blender
url: https://qiita.com/SaitoTsutomu/items/7c96f67cfb88cc39d9f3
created_at: 2024-01-13 13:32:25+09:00
updated_at: 2024-07-08 20:54:30+09:00
body:

## はじめに

Blender 4.0で、**ジオメトリーノード**を使って**鉄板**（チェッカープレート）を作成してみました。
また、すべての操作をPythonで記述することで、簡単に再現できるようにしています。

作成した鉄板とジオメトリーノードは下記になります。

<img src="https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/13955/03bd9589-92db-ae65-9934-abcbe3e76e54.png" width="360">

![](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/13955/f69cf24d-120e-4283-db90-cce1c1badc66.png)

下記の動画を参考に作成しました[^1]。

[^1]: いつも面白い動画ありがとうございます。

https://www.youtube.com/watch?v=ZUijTYYXD-Y

動画では、模様の数が固定でしたが、本記事ではパラメータ化しています。

## ジオメトリーノードの簡単な説明

- 模様は、UV球（Sphere）を元にしています。鉄板は立方体（Cube）を元にしています。
- 模様を横に複製するのと縦に複製するのは同じ処理なので、グループ化しています。グループの名前はDupInsです。複製方法は、カーブノードを使っています。
- トランスフォームを使って、模様の回転と移動をしています。

## Pythonで実行

下記のコードをコピペして実行すると、鉄板を作成できます。

```py
import bpy

def new(nodes, bl_idname, inputs=None, **kwargs):
    """ノード作成関数"""
    nd = nodes.new(bl_idname)
    for name, value in kwargs.items():
        setattr(nd, name, value)
    for name, value in (inputs or {}).items():
        nd.inputs[name].default_value = value

# オブジェクト作成
bpy.ops.mesh.primitive_plane_add()
modifier = bpy.context.active_object.modifiers.new("GeometryNodes", "NODES")
node_groups = bpy.data.node_groups

# DupIns作成
node_tree = node_groups.new("DupIns", "GeometryNodeTree")
nodes = node_tree.nodes
node_tree.interface.new_socket("Instances", in_out="OUTPUT", socket_type="NodeSocketGeometry")
node_tree.interface.new_socket("Instance", in_out="INPUT", socket_type="NodeSocketGeometry")
node_tree.interface.new_socket("End", in_out="INPUT", socket_type="NodeSocketVector")
node_tree.interface.new_socket("Count", in_out="INPUT", socket_type="NodeSocketInt")
new(nodes, "NodeGroupInput", name="Group Input", location=[-420, 0])
kwargs = dict(name="Resample Curve", location=[-56, -1], hide=True, mode="COUNT")
new(nodes, "GeometryNodeResampleCurve", {1: True}, **kwargs)
kwargs = dict(name="Curve Line", location=[-243, -3], hide=True, mode="POINTS")
new(nodes, "GeometryNodeCurvePrimitiveLine", {0: [0.0, 0.0, 0.0]}, **kwargs)
inputs = {1: True, 3: False, 4: 0, 5: [0.0, 0.0, 0.0], 6: [1.0, 1.0, 1.0]}
kwargs = dict(name="Instance on Points", location=[107, -61], hide=True)
new(nodes, "GeometryNodeInstanceOnPoints", inputs, **kwargs)
new(nodes, "NodeGroupOutput", name="Group Output", location=[283, 0])
node_tree.links.new(nodes["Curve Line"].outputs[0], nodes["Resample Curve"].inputs[0])
node_tree.links.new(nodes["Resample Curve"].outputs[0], nodes["Instance on Points"].inputs[0])
node_tree.links.new(nodes["Group Input"].outputs[0], nodes["Instance on Points"].inputs[2])
node_tree.links.new(nodes["Instance on Points"].outputs[0], nodes["Group Output"].inputs[0])
node_tree.links.new(nodes["Group Input"].outputs[1], nodes["Curve Line"].inputs[1])
node_tree.links.new(nodes["Group Input"].outputs[2], nodes["Resample Curve"].inputs[2])

# IronPlate作成
node_tree = node_groups.new("IronPlate", "GeometryNodeTree")
nodes = node_tree.nodes
node_tree.interface.new_socket("Geometry", in_out="OUTPUT", socket_type="NodeSocketGeometry")
node_tree.interface.new_socket("Geometry", in_out="INPUT", socket_type="NodeSocketGeometry")
node_tree.interface.new_socket("CountX", in_out="INPUT", socket_type="NodeSocketInt")
node_tree.interface.new_socket("CountY", in_out="INPUT", socket_type="NodeSocketInt")
node_tree.interface.new_socket("Material", in_out="INPUT", socket_type="NodeSocketMaterial")
new(nodes, "NodeFrame", name="Frame", label="slim sphere")
new(nodes, "NodeFrame", name="Frame2")
new(nodes, "NodeFrame", name="Frame3")
new(nodes, "NodeFrame", name="Frame1", label="plate")
new(nodes, "GeometryNodeJoinGeometry", name="Join Geometry", location=[764, -3])
new(nodes, "GeometryNodeSetMaterial", {1: True}, name="Set Material", location=[1292, 2])
new(nodes, "NodeGroupOutput", name="Group Output", location=[1468, 10])
new(nodes, "NodeGroupInput", name="Group Input", location=[-340, 0])
kwargs = dict(name="UV Sphere", location=[-193, -115], hide=True, parent=nodes["Frame"])
new(nodes, "GeometryNodeMeshUVSphere", {0: 12, 1: 6, 2: 1.0}, **kwargs)
inputs = {1: [0.0, 0.0, 0.0], 2: [0.0, 0.0, 0.0], 3: [0.2, 1.0, 0.2]}
kwargs = dict(name="Transform Geometry2", location=[-25, -120], hide=True, parent=nodes["Frame"])
new(nodes, "GeometryNodeTransform", inputs, **kwargs)
kwargs = dict(name="Set Shade Smooth", location=[146, -112], domain="FACE", parent=nodes["Frame"])
new(nodes, "GeometryNodeSetShadeSmooth", {1: True, 2: True}, hide=True, **kwargs)
kwargs = dict(name="Math3", location=[-105, -31], operation="MULTIPLY_ADD", parent=nodes["Frame2"])
new(nodes, "ShaderNodeMath", {1: 2.0, 2: -2.0}, hide=True, **kwargs)
kwargs = dict(name="Combine XYZ", location=[54, -31], hide=True, parent=nodes["Frame2"])
new(nodes, "ShaderNodeCombineXYZ", {1: 0.0, 2: 0.0}, **kwargs)
new(nodes, "GeometryNodeGroup", name="Group", location=[216, -16], parent=nodes["Frame2"])
nodes["Group"].node_tree = node_groups["DupIns"]
kwargs = dict(name="Math4", location=[597, -126], operation="MULTIPLY_ADD", parent=nodes["Frame3"])
new(nodes, "ShaderNodeMath", {1: 2.0, 2: -2.0}, hide=True, **kwargs)
kwargs = dict(name="Combine XYZ1", location=[765, -128], hide=True, parent=nodes["Frame3"])
new(nodes, "ShaderNodeCombineXYZ", {0: 0.0, 2: 0.0}, **kwargs)
new(nodes, "GeometryNodeGroup", name="Group1", location=[932, -48], parent=nodes["Frame3"])
nodes["Group1"].node_tree = node_groups["DupIns"]
kwargs = dict(name="Transform Geometry1", location=[733, -237], parent=nodes["Frame1"])
new(nodes, "GeometryNodeTransform", {2: [0.0, 0.0, 0.0]}, **kwargs)
kwargs = dict(name="Math1", location=[419, -319], operation="ADD", parent=nodes["Frame1"])
new(nodes, "ShaderNodeMath", {1: -0.5}, hide=True, **kwargs)
kwargs = dict(name="Math2", location=[415, -408], operation="MULTIPLY_ADD", parent=nodes["Frame1"])
new(nodes, "ShaderNodeMath", {1: 2.0, 2: 0.5}, hide=True, **kwargs)
kwargs = dict(name="Math6", location=[416, -452], operation="MULTIPLY_ADD", parent=nodes["Frame1"])
new(nodes, "ShaderNodeMath", {1: 2.0, 2: 0.5}, hide=True, **kwargs)
kwargs = dict(name="Math5", location=[417, -361], operation="ADD", parent=nodes["Frame1"])
new(nodes, "ShaderNodeMath", {1: -0.5}, hide=True, **kwargs)
kwargs = dict(name="Combine XYZ2", location=[569, -316], parent=nodes["Frame1"])
new(nodes, "ShaderNodeCombineXYZ", {2: -0.15}, hide=True, **kwargs)
kwargs = dict(name="Combine XYZ3", location=[579, -409], parent=nodes["Frame1"])
new(nodes, "ShaderNodeCombineXYZ", {2: 0.3}, hide=True, **kwargs)
kwargs = dict(name="Cube", location=[537, -256], parent=nodes["Frame1"])
new(nodes, "GeometryNodeMeshCube", {0: [1.0, 1.0, 1.0], 1: 2, 2: 2, 3: 2}, hide=True, **kwargs)
inputs = {1: [1.0, 1.0, 0.0], 2: [0.0, 0.0, 0.0], 3: [1.0, 1.0, 1.0]}
kwargs = dict(name="Transform Geometry", location=[598, -66], hide=True)
new(nodes, "GeometryNodeTransform", inputs, **kwargs)
new(nodes, "GeometryNodeJoinGeometry", name="Join Geometry1", location=[1129, -46], hide=True)
inputs = {1: True, 2: [0.0, 0.0, 0.7854], 3: [0.0, 0.0, 0.0], 4: True}
kwargs = dict(name="Rotate Instances", location=[444, -17], hide=True)
new(nodes, "GeometryNodeRotateInstances", inputs, **kwargs)
inputs = {1: True, 2: [0.0, 0.0, -0.7854], 3: [0.0, 0.0, 0.0], 4: True}
kwargs = dict(name="Rotate Instances1", location=[443, -67], hide=True)
new(nodes, "GeometryNodeRotateInstances", inputs, **kwargs)
nodes["Frame"].location = [-116, -150]
nodes["Frame2"].location = [13, -19]
nodes["Frame3"].location = [2, -88]
nodes["Frame1"].location = [190, -112]
node_tree.links.new(nodes["Transform Geometry"].outputs[0], nodes["Join Geometry"].inputs[0])
node_tree.links.new(nodes["Rotate Instances"].outputs[0], nodes["Join Geometry"].inputs[0])
node_tree.links.new(nodes["Rotate Instances1"].outputs[0], nodes["Transform Geometry"].inputs[0])
node_tree.links.new(nodes["Join Geometry"].outputs[0], nodes["Group1"].inputs[0])
node_tree.links.new(nodes["Transform Geometry1"].outputs[0], nodes["Join Geometry1"].inputs[0])
node_tree.links.new(nodes["Group1"].outputs[0], nodes["Join Geometry1"].inputs[0])
node_tree.links.new(nodes["Set Material"].outputs[0], nodes["Group Output"].inputs[0])
node_tree.links.new(nodes["Cube"].outputs[0], nodes["Transform Geometry1"].inputs[0])
node_tree.links.new(nodes["Join Geometry1"].outputs[0], nodes["Set Material"].inputs[0])
node_tree.links.new(nodes["Set Shade Smooth"].outputs[0], nodes["Group"].inputs[0])
node_tree.links.new(nodes["UV Sphere"].outputs[0], nodes["Transform Geometry2"].inputs[0])
node_tree.links.new(nodes["Transform Geometry2"].outputs[0], nodes["Set Shade Smooth"].inputs[0])
node_tree.links.new(nodes["Group Input"].outputs[1], nodes["Group"].inputs[2])
node_tree.links.new(nodes["Combine XYZ"].outputs[0], nodes["Group"].inputs[1])
node_tree.links.new(nodes["Combine XYZ1"].outputs[0], nodes["Group1"].inputs[1])
node_tree.links.new(nodes["Group Input"].outputs[3], nodes["Set Material"].inputs[2])
node_tree.links.new(nodes["Group Input"].outputs[1], nodes["Math1"].inputs[0])
node_tree.links.new(nodes["Math1"].outputs[0], nodes["Combine XYZ2"].inputs[0])
node_tree.links.new(nodes["Combine XYZ2"].outputs[0], nodes["Transform Geometry1"].inputs[1])
node_tree.links.new(nodes["Math2"].outputs[0], nodes["Combine XYZ3"].inputs[0])
node_tree.links.new(nodes["Combine XYZ3"].outputs[0], nodes["Transform Geometry1"].inputs[3])
node_tree.links.new(nodes["Group Input"].outputs[1], nodes["Math3"].inputs[0])
node_tree.links.new(nodes["Math3"].outputs[0], nodes["Combine XYZ"].inputs[0])
node_tree.links.new(nodes["Group Input"].outputs[1], nodes["Math2"].inputs[0])
node_tree.links.new(nodes["Math4"].outputs[0], nodes["Combine XYZ1"].inputs[1])
node_tree.links.new(nodes["Group Input"].outputs[2], nodes["Math4"].inputs[0])
node_tree.links.new(nodes["Group Input"].outputs[2], nodes["Group1"].inputs[2])
node_tree.links.new(nodes["Group Input"].outputs[2], nodes["Math5"].inputs[0])
node_tree.links.new(nodes["Math5"].outputs[0], nodes["Combine XYZ2"].inputs[1])
node_tree.links.new(nodes["Group Input"].outputs[2], nodes["Math6"].inputs[0])
node_tree.links.new(nodes["Math6"].outputs[0], nodes["Combine XYZ3"].inputs[1])
node_tree.links.new(nodes["Group"].outputs[0], nodes["Rotate Instances"].inputs[0])
node_tree.links.new(nodes["Group"].outputs[0], nodes["Rotate Instances1"].inputs[0])

mat = bpy.data.materials.new("Material")
mat.metallic = 1
node_tree.interface.items_tree["CountX"].default_value = 10
node_tree.interface.items_tree["CountY"].default_value = 10
node_tree.interface.items_tree["Material"].default_value = mat
modifier.node_group = node_tree
modifier.node_group.is_modifier = True
```

BlenderでPythonを実行するには、下記を参考にしてください。

https://qiita.com/SaitoTsutomu/items/cec67381a8789b40e377

### Pythonコードの作成について

本記事では、ジオメトリーノードからPythonコードへの変換用するために、下記のアドオンを使用しています。

https://github.com/SaitoTsutomu/GeometryScript

以上

