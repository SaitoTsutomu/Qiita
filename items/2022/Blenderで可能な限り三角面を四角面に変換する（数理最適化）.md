title: Blenderで可能な限り三角面を四角面に変換する（数理最適化）
tags: Python 3DCG Blender 最適化 数理最適化
url: https://qiita.com/SaitoTsutomu/items/b608c80d70a54718ec78
created_at: 2022-03-21 17:05:44+09:00
updated_at: 2022-03-21 18:37:08+09:00
body:

## メッシュの四角面化

Blenderには、三角面を四角面にする機能があります。これは、面の角度を考慮して四角面を選んでいます。
これはこれで便利なのですが、**可能な限り三角面を四角面に変えたい**ことがあります。
ここでは、それを**数理最適化**で実現するアドオンを紹介します。

## 具体例

下記のメッシュで試してみます。

<img src="https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/13955/26141131-8915-b923-87f3-78e115397f85.png" width="300">

通常の「三角面を四角面に」を実行すると下記のようになります。

<img src="https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/13955/21a01f16-46d2-1765-239a-17c19d654514.png" width="300">

隅の方に三角面ができています。

一方で、今回紹介するアドオンを実行すると下記のようになります。

<img src="https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/13955/928d6e87-6d11-b922-2452-980fb8eeb984.png" width="300">

すべての三角面が四角面になっています。

## インストール方法

### PuLPのインストール

本アドオンは、Pythonの[PuLP](https://github.com/coin-or/pulp)モジュールを利用しています。
そのため、下記のように、コマンドラインでBlenderにPuLPをインストールする必要があります。コマンドラインからBlenderを操作する方法については、「[Blenderのコマンドサンプル](https://qiita.com/SaitoTsutomu/items/6b70367455f843a979b1)」も参考にしてください。

- macOSの場合
```
/Applications/Blender.app/Contents/Resources/3.1/python/bin/python3.10 -m pip install pulp
```

- Windowsの場合
```
"C:\Program Files\Blender Foundation\Blender 3.1\3.1\python\bin\python" -m pip install pulp
```

※ 実は、[Python-MIP](https://www.python-mip.com/)ライブラリーを使いたかったのですが、Blender3.1では動かないためPuLPを用いています。

### アドオンのインストール

- GitHubの[Tris-Quads-Ex](https://github.com/SaitoTsutomu/Tris-Quads-Ex)から、下記のアドオンのZIPファイルをダウンロードしてください。ZIPファイルは解凍しないでください。

  - [アドオンのZIPファイル](https://github.com/SaitoTsutomu/Tris-Quads-Ex/archive/refs/heads/main.zip)

- Blenderのプリファレンスのアドオンで「インストール…」ボタンを押し、ダウンロードしたZIPファイルを選択します。

- 下図のようになるので、`Mesh: Tris to Quads Ex`にチェックを入れてください。

<img src="https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/13955/250a50eb-529d-242d-2227-ff0fb6eced28.png" width="600">

## 使い方

- 対象のオブジェクトを選んで、編集モードに入ります。
- 対象の範囲を選択して、面メニューの「Tris to Quads Ex」を選びます。

※ 選択している辺の中でしか溶解しません。すべてを対象にする場合は、`A`で全選択してください。

## 最適化について

「可能な限り三角面を四角面にする」ためには、溶解する辺の数をなるべくたくさん選ぶ必要があります。
一方で、選びすぎるとNゴン（頂点が5以上の多角形）になってしまうので、できる多角形の頂点を4までに抑える必要があります。
このような問題は混合整数最適化問題になります。
混合整数最適化問題とは何かについては、「[組合せ最適化を使おう](https://qiita.com/SaitoTsutomu/items/bfbf4c185ed7004b5721)」を参考にしてください。
ここでは、混合整数最適化問題を定式化し、PuLPでモデル化しCBCソルバーで解きます。

### 定式化

変数は以下の条件を満たす辺ごとに0-1変数を作成します。1が溶解する、0が溶解しないに対応します。

- 選択されている
- 両側の面がともに選択された三角面である

ここでは、下記の定式化を解いて、溶解する辺を求めています。

| 目的関数 | 溶解する辺の数 → 最大化 |
|:-:|:-:|
| 制約条件 | 三角面ごとに、溶解する辺は1本以下 |

三角面に対し2本以上を溶解するとNゴンになるため、上記の制約条件になります。

## アドオンのコード（Python）

実際に辺を溶解するのは、`execute()`メソッドになります。

```py
import bmesh
import bpy
from pulp import LpMaximize, LpProblem, LpVariable, lpSum, value

bl_info = {
    "name": "Tris to Quads Ex",  # プラグイン名
    "author": "tsutomu",  # 制作者名
    "version": (1, 0),  # バージョン
    "blender": (3, 1, 0),  # 動作可能なBlenderバージョン
    "support": "COMMUNITY",  # サポートレベル
    "category": "Mesh",  # カテゴリ名
    "description": "Tris to quads by mathematical optimization.",  # 説明文
    "location": "Mesh: Tris to Quads Ex",  # 機能の位置付け
    "warning": "",  # 注意点やバグ情報
    "doc_url": "https://github.com/SaitoTsutomu/Tris-Quads-Ex",  # ドキュメントURL
}


class CEF_OT_tris_convert_to_quads_ex(bpy.types.Operator):
    """Tris to Quads"""

    bl_idname = "object.tris_convert_to_quads_ex"
    bl_label = "Tris to Quads Ex"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        # BMesh（bm）が使い回されないようにモードを切り替える
        bpy.ops.object.mode_set(mode="OBJECT")
        bpy.ops.object.mode_set(mode="EDIT")
        obj = bpy.context.edit_object
        bm = bmesh.from_edit_mesh(obj.data)
        bm.edges.ensure_lookup_table()

        m = LpProblem(sense=LpMaximize)
        edges = {}
        for edge in bm.edges:
            if (
                not edge.select
                or len(edge.link_faces) != 2
                or not edge.link_faces[0].select
                or not edge.link_faces[1].select
                or len(edge.link_faces[0].edges) != 3
                or len(edge.link_faces[1].edges) != 3
            ):
                continue
            edges[edge] = LpVariable(f"v{len(edges):03}", cat="Binary")
        m.setObjective(lpSum(edges.values()))
        for face in bm.faces:
            if len(face.edges) != 3:
                continue
            vv = [v for edge in face.edges if (v := edges.get(edge)) is not None]
            if len(vv) > 1:
                m += lpSum(vv) <= 1
        m.solve()
        if m.status != 1:
            self.report({"INFO"}, "Not solved.")
        else:
            bpy.ops.mesh.select_all(action="DESELECT")
            n = 0
            for edge, v in edges.items():
                if value(v) > 0.5:
                    edge.select_set(True)
                    n += 1
            self.report({"INFO"}, f"{n} edges are dissolved.")
            bpy.ops.mesh.dissolve_edges(use_verts=False)
        bm.free()
        del bm
        return {"FINISHED"}


ui_classes = (CEF_OT_tris_convert_to_quads_ex,)


def menu_func(self, context):
    self.layout.operator(CEF_OT_tris_convert_to_quads_ex.bl_idname)


def register():
    for ui_class in ui_classes:
        bpy.utils.register_class(ui_class)
    # Adds the new operator to an existing menu(Face in Edit mode).
    bpy.types.VIEW3D_MT_edit_mesh_faces.append(menu_func)


def unregister():
    for ui_class in ui_classes:
        bpy.utils.unregister_class(ui_class)


if __name__ == "__main__":
    register()
```

以上

