title: Blender 4.2で卵を作成
tags: Python 3DCG addon Blender
url: https://qiita.com/SaitoTsutomu/items/72734602fcf3f993f8e3
created_at: 2023-12-31 14:47:39+09:00
updated_at: 2024-10-06 13:09:30+09:00
body:

## はじめに

Blender 4.2で、**ジオメトリーノード**を使って**卵**を作成してみました。
また、すべての操作をPythonで記述することで、簡単に再現できるようにしています。

作成した卵とジオメトリーノードは下記になります。

<img src="https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/13955/49d604f1-b3c0-2e25-f98f-cf00e0242b9a.png" width="160">

![](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/13955/7f587c93-7801-6e77-1bb5-9b26c5fdba88.png)

## ジオメトリーノードの説明

1. `グループ入力`: UV球を元にしています。`XYZ`が`±１`の範囲にあります
2. `位置`: 位置属性を取り出し、「XYZ分離」と「乗算」の入力にします。「XYZ分離」の方で卵型に変形を計算します
3. `XYZ分離`: `Z`だけ取得します
4. `範囲マッピング`: 入力が`±1`なので、`0-1`の範囲になるようにします
5. `Floatカーブ`: カラーランプのように`0-1`の範囲を`0-1`に変換します。ここでは、`Z`を「卵型への係数」に変換します
6. `XYZ合成`: 「Floatカーブ」からXとYにつなぎます。`Z`は`１`です
7. `乗算`: ベクトルの掛け算をします。ここで、球を卵型にします
8. `位置設定`: 位置を設定します。これによりジオメトリーが卵型になります
9. `スムーズシェード設定`: スムーズをかけます

このジオメトリーノードは、下記のBlender 3.4の記事を参考にBlender 4.2用にアレンジしたものです。

https://qiita.com/SaitoTsutomu/items/39eb1f022218c647c323

## Pythonで実行

下記のコードをコピペして実行すると、卵を作成できます。

```py
import bpy

ATTRIBUTES = {"name": str, "location": list, "mapping": list, "operation": str}


def new(nodes, bl_idname, inputs=None, **kwargs):
    nd = nodes.new(bl_idname)
    for name, value in kwargs.items():
        typ = ATTRIBUTES.get(name)
        if value and typ and isinstance(value, typ):
            if name == "mapping":
                crv = nd.mapping.curves[0]
                for _ in value[2:]:
                    crv.points.new(0, 0)
                for pnt, s in zip(crv.points, value):
                    pnt.handle_type, *pnt.location = s
            else:
                setattr(nd, name, value)
    for name, value in (inputs or {}).items():
        nd.inputs[name].default_value = value


bpy.ops.mesh.primitive_uv_sphere_add()
obj = bpy.context.object
node_group = bpy.data.node_groups.new("Geometry Nodes", "GeometryNodeTree")
mod = obj.modifiers.new("GeometryNodes", "NODES")
mod.node_group = node_group
node_group.is_modifier = True
nodes = node_group.nodes
node_group.interface.new_socket("Geometry", in_out="OUTPUT", socket_type="NodeSocketGeometry")
node_group.interface.new_socket("Geometry", in_out="INPUT", socket_type="NodeSocketGeometry")
new(nodes, "NodeGroupOutput", name="Group Output", location=[910, 6])
new(nodes, "GeometryNodeSetPosition", name="Set Position", location=[756, 4])
new(nodes, "GeometryNodeSetShadeSmooth", name="Set Shade Smooth", location=[756, -200])
new(nodes, "ShaderNodeVectorMath", name="Vector Math", location=[600, -200], operation="MULTIPLY")
new(nodes, "ShaderNodeCombineXYZ", {"Z": 1.0}, name="Combine XYZ", location=[600, 4])
new(nodes, "ShaderNodeSeparateXYZ", name="Separate XYZ", location=[24, -200])
new(nodes, "GeometryNodeInputPosition", name="Position", location=[24, -110])
new(nodes, "NodeGroupInput", name="Group Input", location=[24, 2])
new(nodes, "ShaderNodeMapRange", {"From Min": -1}, name="Map Range", location=[184, 3])
mapping = [("AUTO", 0, 0.8), ("AUTO", 1, 0.7)]
new(nodes, "ShaderNodeFloatCurve", name="Float Curve", location=[342, 2], mapping=mapping)
node_group.links.new(nodes["Set Shade Smooth"].outputs[0], nodes["Group Output"].inputs[0])
node_group.links.new(nodes["Group Input"].outputs[0], nodes["Set Position"].inputs[0])
node_group.links.new(nodes["Position"].outputs["Position"], nodes["Separate XYZ"].inputs[0])
node_group.links.new(nodes["Vector Math"].outputs[0], nodes["Set Position"].inputs["Position"])
node_group.links.new(nodes["Set Position"].outputs[0], nodes["Set Shade Smooth"].inputs[0])
node_group.links.new(nodes["Separate XYZ"].outputs["Z"], nodes["Map Range"].inputs[0])
node_group.links.new(nodes["Combine XYZ"].outputs[0], nodes["Vector Math"].inputs[0])
node_group.links.new(nodes["Position"].outputs["Position"], nodes["Vector Math"].inputs[1])
node_group.links.new(nodes["Map Range"].outputs["Result"], nodes["Float Curve"].inputs["Factor"])
node_group.links.new(nodes["Float Curve"].outputs[0], nodes["Combine XYZ"].inputs["X"])
node_group.links.new(nodes["Float Curve"].outputs[0], nodes["Combine XYZ"].inputs["Y"])
```

BlenderでPythonを実行するには、下記を参考にしてください。

https://qiita.com/SaitoTsutomu/items/cec67381a8789b40e377

### Pythonコードの作成について

下記の記事では、アドオンを使って、YAMLからジオメトリーノードを作成しました。

https://qiita.com/SaitoTsutomu/items/7213552baf9b65de3df6

本記事では、アドオンを使わずに手軽に実行できるように、Pythonでジオメトリーノードを作成するようにしました。
さらに、ジオメトリーノードからPythonコードへの変換用するために、下記のアドオンを使用しています。

https://github.com/SaitoTsutomu/GeometryScript

なお、アドオンで作成したコードは完璧ではないため、本記事では手動で調整しています。

以上

