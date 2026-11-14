title: Blenderで特定のタグのアセットを全て取り込む（Python）
tags: Python 3DCG addon Blender
url: https://qiita.com/SaitoTsutomu/items/3b6a5ad3258c7cb88cad
created_at: 2022-01-22 16:01:36+09:00
updated_at: 2022-05-08 17:58:05+09:00
body:

## やりたいこと

アニメーションが入っている複数のBlenderのファイルがあります。
これを1つのファイルに統合したいとします。

Blender3.0からアセットブラウザーが使えるので、アニメーションのオブジェクトをアセット化したとしましょう。
しかし、ファイルやオブジェクトが多くなると手間がかかります。ここでは、Pythonを使って、ボタン1つで統合する方法を紹介します。

## アドオンの追加

下記のコードをファイルに保存し、Blenderのプリファレンスのアドオンからインストールしてください。
インストール後、「テスト中」を選び、「3D View: Load assets」をチェックしてください。

```py
"""
アセットライブラリとタグを指定し、リンクモードで読み込む。
UIはサイドバーのEdit(編集)のAsset（アセット）にある。
- Library（ライブラリ）：対象アセットライブラリを指定する。
- Tag（タグ）：タグを指定する。空の場合、全て読み込む。
- Load（読み込み）：アセットを読み込む。
"""
import glob
import pickle
from pathlib import Path

import bpy

bl_info = {
    "name": "Load assets",  # プラグイン名
    "author": "Tsutomu Saito",  # 制作者名
    "version": (1, 0),  # バージョン
    "blender": (3, 0, 0),  # 動作可能なBlenderバージョン
    "support": "TESTING",  # サポートレベル
    "category": "3D View",  # カテゴリ名
    "description": "Load assets",  # 説明文
    "location": "",  # 機能の位置付け
    "warning": "",  # 注意点やバグ情報
    "doc_url": "",  # ドキュメントURL
}


class Config:
    PATH = Path("/tmp/load_asset.pickle")

    @staticmethod
    def load() -> dict:
        try:
            with open(Config.PATH, "rb") as fp:
                dc = pickle.load(fp)
        except FileNotFoundError:
            return {}
        assert isinstance(dc, dict)
        return dc

    @staticmethod
    def save(*, clear=False, **kwargs) -> None:
        if not clear:
            kwargs |= Config.load()
        Config.PATH.parent.mkdir(exist_ok=True)
        with open(Config.PATH, "wb") as fp:
            pickle.dump(kwargs, fp)


class CLA_OT_load(bpy.types.Operator):
    """Loadボタン押下"""

    bl_idname = "object.load_operator"
    bl_label = "Load Operator"
    bl_options = {"REGISTER", "UNDO"}
    Library: bpy.props.StringProperty()  # type: ignore
    Tag: bpy.props.StringProperty()  # type: ignore

    def _check_asset(self, obj):
        if not obj.asset_data:
            return False
        if not self.Tag:
            return True
        ss = set(tag.name for tag in obj.asset_data.tags)
        return bool(set(self.Tag.split(",")) & ss)

    def execute(self, context):
        for lib in bpy.context.preferences.filepaths.asset_libraries:
            if lib.name == self.Library:
                break
        else:
            return {"CANCELLED"}
        bpy.context.window.cursor_set("WAIT")
        col_name = self.Tag or "Load Asset"
        if ano := bpy.data.collections.get(col_name):
            bpy.data.collections.remove(ano)
        col = bpy.data.collections.new(col_name)
        bpy.context.scene.collection.children.link(col)
        lc = bpy.context.view_layer.layer_collection.children[col_name]
        bpy.context.view_layer.active_layer_collection = lc
        for fnam in glob.glob(f"{lib.path}/**/*.blend", recursive=True):
            with bpy.data.libraries.load(str(fnam)) as (data_from, data_to):
                data_to.objects.extend(data_from.objects)
            files = []
            for name, obj in zip(data_from.objects, data_to.objects):
                if self._check_asset(obj):
                    files.append({"name": name})
            if files:
                bpy.ops.wm.link(directory=f"{fnam}/Object", files=files)
        bpy.ops.outliner.orphans_purge(do_recursive=True)
        Config.save(Library=self.Library, Tag=self.Tag)
        return {"FINISHED"}


class CLA_PT_load(bpy.types.Panel):
    """パネル"""

    bl_label = "Asset"
    bl_idname = "CLA_PT_load"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Edit"

    def draw(self, context):
        layout = self.layout
        layout.prop(context.scene, "Library")
        layout.prop(context.scene, "Tag")
        prop = layout.operator(CLA_OT_load.bl_idname, text="Load")
        prop.Library = context.scene.Library
        prop.Tag = context.scene.Tag


regist_classes = (
    CLA_OT_load,
    CLA_PT_load,
)


def register():
    config = Config().load()
    for regist_class in regist_classes:
        bpy.utils.register_class(regist_class)
    Library = config.get("Library", "User Library")
    Tag = config.get("Tag", "")
    bpy.types.Scene.Library = bpy.props.StringProperty(default=Library)
    bpy.types.Scene.Tag = bpy.props.StringProperty(default=Tag)


def unregister():
    for regist_class in regist_classes:
        bpy.utils.unregister_class(regist_class)
    del bpy.types.Scene.Library
    del bpy.types.Scene.Tag


if __name__ == "__main__":
    register()
```

参考：[BlenderでPythonを実行する方法](https://qiita.com/SaitoTsutomu/items/cec67381a8789b40e377)

## 使い方

必要に応じて、プリファレンスのファイルパスのアセットライブラリにパスを追加してください。

3Dビューポートで、サイドバーの編集を開いてください。

<img src="https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/13955/4500b579-b631-4069-068b-ba1bedd5eb3c.jpeg" width="280">

ライブラリには、アセットライブラリのパスの名前を指定します。
「読み込み」ボタンを押すと、指定されたパス以下のすべてのオブジェクトのリンクを読み込みます。
タグを指定すると、そのタグのオブジェクトだけになります。タグには、カンマ区切りで複数のタグを書けます。

追加されるオブジェクトは、タグ名のコレクションに入ります。このコレクションは読み込み前にクリアされます。

※ 実行すると、項目の内容をファイル（`/tmp/load_asset.pickle`）に書き込みます。次回起動時に同じ項目が表示されます。

## 補足

このアドオンは、アセットライブラリのAPIは使ってません。アセットライブラリのパスに存在するBlendファイルを解析しています。オブジェクトがアセットかどうかやタグが対象かどうかを調べた後、`bpy.ops.wm.link`を使っているので、二度手間になってます。

## なぜ、アセットを自動化の対象にしたのか

そもそも、アセットブラウザーで手動で統合してたのを、自動化したいというニーズがあったのでアドオン化しました。アドオンにした時点で、アセットを対象にする必要性はなくなりました。しかし、アセットを対象にすることで、統合前のオブジェクトをアセットブラウザーで確認できたり、手動でも実行できたりというメリットがあります。

以上

