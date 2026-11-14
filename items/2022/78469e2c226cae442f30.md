title: Blenderで移動できる窓を作る
tags: Python 3DCG addon Blender
url: https://qiita.com/SaitoTsutomu/items/78469e2c226cae442f30
created_at: 2022-02-23 14:18:41+09:00
updated_at: 2022-05-08 17:58:42+09:00
body:

## Blenderで移動できる窓を作る

Blenderの標準アドオンの[Archimesh](https://docs.blender.org/manual/en/latest/addons/add_mesh/archimesh.html)で窓を作成すると、壁に沿って移動できます。

手動で行う場合は、壁のオブジェクトにブーリアンモディファイアーを使って実現できます。
穴用のオブジェクトをブーリアンの差分に指定することで、壁に穴を開けられます。

ここでは、Pythonを使った「移動できる窓の作成方法」を紹介します。

## パネルの表示

パネルを表示するために、scriptingワークスペースで新規を押し、下記をコピペしてスクリプト実行をしてください。なお、このコードをファイルに保存すれば、アドオンとしてインストール可能です。

```py
"""
Window frame setting
- Make a hole in the wall.
- Make a hole in the frame.
- Make the hole the parent of the frame.
- Make the glass the parent of the frame.
- Hide the hole.
- Set materials.
"""
import bpy

bl_info = {
    "name": "Window frame setting",  # プラグイン名
    "author": "tsutomu",  # 制作者名
    "version": (1, 0),  # バージョン
    "blender": (3, 0, 0),  # 動作可能なBlenderバージョン
    "support": "TESTING",  # サポートレベル
    "category": "3D View",  # カテゴリ名
    "description": "Window frame setting",  # 説明文
    "location": "",  # 機能の位置付け
    "warning": "",  # 注意点やバグ情報
    "doc_url": "",  # ドキュメントURL
}


class CWS_OT_make_sample(bpy.types.Operator):
    bl_idname = "object.make_sample_operator"
    bl_label = "Make sample"

    def execute(self, context):
        dc = {
            "frame": {"scale": (0.6, 0.1, 0.6)},
            "glass": {"scale": (0.5, 0.02, 0.5)},
            "wall": {"scale": (1, 0.05, 1)},
            "hole": {"scale": (0.5, 0.2, 0.5)},
        }
        for name, prop in dc.items():
            bpy.ops.mesh.primitive_cube_add(**prop)
            bpy.context.selected_objects[0].name = name
        return {"FINISHED"}


class CWS_OT_set_frame(bpy.types.Operator):
    """What to do when the 'Set to frame' button is pressed"""

    bl_idname = "object.set_frame_operator"
    bl_label = "Set to frame"
    frame: bpy.props.StringProperty(name="frame")  # type: ignore
    glass: bpy.props.StringProperty(name="glass")  # type: ignore
    wall: bpy.props.StringProperty(name="wall")  # type: ignore
    hole: bpy.props.StringProperty(name="hole")  # type: ignore
    doset: bpy.props.BoolProperty(name="doset")  # type: ignore

    def execute(self, context):
        try:
            frame = bpy.data.objects[self.frame]
            glass = bpy.data.objects[self.glass]
            wall = bpy.data.objects[self.wall]
            hole = bpy.data.objects[self.hole]
        except KeyError as e:
            self.report({"ERROR"}, f"Not found {e.args[0].split()[2]}")
            return {"CANCELLED"}
        chk = lambda m: m.name == "Boolean" and m.object == hole
        for obj in [wall, frame]:
            if not next(filter(chk, obj.modifiers), None):
                bpy.context.view_layer.objects.active = obj
                bpy.ops.object.modifier_add(type="BOOLEAN")
                obj.modifiers[-1].object = hole
        if not glass.parent and not hole.parent:
            bpy.ops.object.select_all(action="DESELECT")
            glass.select_set(state=True)
            hole.select_set(state=True)
            bpy.context.view_layer.objects.active = frame
            bpy.ops.object.parent_set()
        hole.hide_set(state=True)
        hole.hide_render = True
        matprop = {
            wall: {"Base Color": (0.5, 0.5, 0.5, 1)},
            frame: {},
            glass: {"Roughness": 0, "Transmission": 1},
        }
        for obj, prop in matprop.items():
            if not obj.active_material:
                obj.active_material = bpy.data.materials.new(name=obj.name)
                obj.active_material.use_nodes = True
            node = obj.active_material.node_tree.nodes.get("Principled BSDF")
            if self.doset and node:
                for key, value in prop.items():
                    node.inputs[key].default_value = value
        return {"FINISHED"}


class CWS_PT_set_frame(bpy.types.Panel):
    bl_label = "Window frame"
    bl_idname = "CWS_PT_set_frame"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Edit"

    def draw(self, context):
        self.layout.operator(CWS_OT_make_sample.bl_idname, text=CWS_OT_make_sample.bl_label)
        for name in ["frame", "glass", "wall", "hole"]:
            self.layout.prop(context.scene, name, text=name.capitalize() + " ")
        self.layout.prop(context.scene, "doset", text="Set material properties")
        prop = self.layout.operator(CWS_OT_set_frame.bl_idname, text=CWS_OT_set_frame.bl_label)
        prop.frame = context.scene.frame
        prop.glass = context.scene.glass
        prop.wall = context.scene.wall
        prop.hole = context.scene.hole
        prop.doset = context.scene.doset


regist_classes = (
    CWS_OT_make_sample,
    CWS_OT_set_frame,
    CWS_PT_set_frame,
)


def register():
    for regist_class in regist_classes:
        bpy.utils.register_class(regist_class)
    bpy.types.Scene.frame = bpy.props.StringProperty(default="frame")
    bpy.types.Scene.glass = bpy.props.StringProperty(default="glass")
    bpy.types.Scene.wall = bpy.props.StringProperty(default="wall")
    bpy.types.Scene.hole = bpy.props.StringProperty(default="hole")
    bpy.types.Scene.doset = bpy.props.BoolProperty(default=True)


def unregister():
    for regist_class in regist_classes:
        bpy.utils.unregister_class(regist_class)
    del bpy.types.Scene.frame
    del bpy.types.Scene.glass
    del bpy.types.Scene.wall
    del bpy.types.Scene.hole
    del bpy.types.Scene.doset


if __name__ == "__main__":
    register()
```

参考：[BlenderでPythonを実行する方法](https://qiita.com/SaitoTsutomu/items/cec67381a8789b40e377)

## 試してみる

layoutワークスペースに戻り、`N`でサイドバーを出し、編集タブを表示してください。下記のように、パネルが表示されています。

<img src="https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/13955/bd4b718a-f31a-f87c-3ef5-5b8919bf9eeb.jpeg" width="300">

実行するには、下記の4つのオブジェクトが必要ですが、`Make sample`ボタンを押すと自動で作成できます。自分でオブジェクトを用意している場合は、`Make sample`を押す必要はありません。

- 窓枠（`frame`）
- ガラス（`glass`）
- 壁（`wall`）
- 穴（`hole`）

4つのオブジェクトを用意したら、それらのオブジェクトの名前をパネルに入力してください。`Make sample`で用意した場合は、すでに入力済みです。

`Set to frame`ボタンを押すと、移動できる窓の設定が完了です。
このボタンでは、下記の処理をします。

- 壁に穴を開けます。
- 窓枠に穴を開けます。
- 窓枠を、穴とガラスの親にします。これにより、窓枠を移動すると穴とガラスも一緒に移動します。
- 穴を非表示にします。
- マテリアルを設定します。（`Set material properties`チェック時）

適当に背景を設定すると、下記のようになります。


<img src="https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/13955/9f2d0f08-1c8b-b32b-0ab5-ecb951959057.jpeg" width="300">

窓枠を動かすと、穴も動きます。

<img src="https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/13955/0d873df0-b2e4-4589-f392-dc76e039bd29.jpeg" width="300">

以上



