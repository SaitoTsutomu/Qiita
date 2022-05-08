title: BlenderからMixamo用のファイルを出力
tags: Python 3DCG Blender Mixamo FBX
url: https://qiita.com/SaitoTsutomu/items/205d614d9840da6485ab
created_at: 2022-05-06 13:51:46+09:00
updated_at: 2022-05-08 10:53:33+09:00
body:

## 概要

Blenderから[Mixamo](https://www.mixamo.com/)用のファイルを出力する方法を紹介します。

デフォルトではFBXにはテクスチャが含まれないため、Blenderから出力したFBXをMixamoにアップロードしてもテクスチャが反映されないようです。
ここでは、テクスチャを反映する方法として、「テクスチャを埋め込む方法」と「FBXとテクスチャをZIP化する方法」の2種類を紹介します。

なお、複雑なシェーダーノードはMixamoで認識されないので、一度テクスチャにベイクする必要があります。

参考：[Blenderで自動ベイク](https://qiita.com/SaitoTsutomu/items/f95fcc7b58f22b872bcf)

## 方法1：テクスチャを埋め込む方法

### 手順

- FBXをエクスポートするときに、パスモードをコピーにして、`テクスチャを埋め込む`をオンにする（下図の赤い枠）
- MixamoにFBXファイルをアップロードする。

<img src="https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/13955/a8572724-8b14-311e-0371-70462f84b16c.png" width="200">

### Pythonで実行

ファイル作成の手順をPythonで記述すると以下のようになります。
対象のオブジェクトを選択して、下記を実行すると、Blenderファイルと同じ場所に、FBXファイルを作成します。

```py
from pathlib import Path

import bpy


def main():
    if not bpy.data.filepath:
        print("Save blend file.")
        return
    if not bpy.context.selected_objects:
        print("Select target.")
        return
    fnam = str(Path(bpy.data.filepath).with_suffix('.fbx'))
    bpy.ops.export_scene.fbx(
        filepath=fnam, use_selection=True, path_mode="COPY", embed_textures=True)
    print(f"Create {fnam}")


if __name__ == "__main__":
    main()
```

参考：[BlenderでPythonを実行する方法](https://qiita.com/SaitoTsutomu/items/cec67381a8789b40e377)

## 方法２：FBXとテクスチャをZIP化する方法

FBXファイルとは別にテクスチャをファイルに保存し、ZIPでまとめる方法です。テクスチャを一覧しやすくなります。

### 手順

- 関連するテクスチャをファイルとして保存する。
- 同じディレクトリにFBXをエクスポートする。
    - エクスポート時にパスモードをストリップパスにして、パスを無視する。
- これらのファイルをZIP化する。
- MixamoにZIPファイルをアップロードする。

### Pythonで実行

ファイル作成の手順をPythonで記述すると以下のようになります。
対象のオブジェクトを選択して、下記を実行すると、Blenderファイルと同じ場所に、ZIPファイルを作成します。
実行すると、テクスチャのパスが変わりパックが解除されるので注意してください。

```py
import shutil
import tempfile
from pathlib import Path

import bpy


def main():
    if not bpy.data.filepath:
        print("Save blend file.")
        return
    if not bpy.context.selected_objects:
        print("Select target.")
        return
    with tempfile.TemporaryDirectory() as td:
        for obj in bpy.context.selected_objects:
            for slot in obj.material_slots:
                mat = slot.material
                if mat and mat.use_nodes:
                    for node in mat.node_tree.nodes:
                        if node.type == "TEX_IMAGE" and node.image:
                            node.image.filepath = f"{td}/{node.image.name}.png"
                            node.image.save()
        fnam = Path(bpy.data.filepath)
        bnam = f"{td}/{fnam.stem}.fbx"
        bpy.ops.export_scene.fbx(filepath=bnam, use_selection=True, path_mode="STRIP")
        shutil.make_archive(fnam.with_suffix(""), format="zip", root_dir=td)
        print(f"Create {fnam.with_suffix('.zip')}")


if __name__ == "__main__":
    main()
```

以上

