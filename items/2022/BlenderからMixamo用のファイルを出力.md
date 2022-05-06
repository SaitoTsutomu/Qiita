title: BlenderからMixamo用のファイルを出力
tags: Python 3DCG Blender Mixamo FBX
url: https://qiita.com/SaitoTsutomu/items/205d614d9840da6485ab
created_at: 2022-05-06 13:51:46+09:00
updated_at: 2022-05-06 20:29:14+09:00
body:

## 概要

Blenderから[Mixamo](https://www.mixamo.com/)用のファイルを出力する方法を紹介します。

FBXにはテクスチャが含まれないため、Blenderから出力したFBXをMixamoにアップロードしてもうまく行かないようです。
しかし、FBXとテクスチャをZIP化してアップロードするとMixamoでもテクスチャを認識するようになります。

ただし、複雑なシェーダーノードはMixamoで認識されないので、一度テクスチャにベイクする必要があります。

参考：[Blenderで自動ベイク](https://qiita.com/SaitoTsutomu/items/f95fcc7b58f22b872bcf)

## 手順

- 関連するテクスチャをファイルとして保存する。
- 同じディレクトリにFBXをエクスポートする。
    - エクスポート時にパスモードをストリップパスにして、パスを無視する。
- これらのファイルをZIP化する。
- MixamoにZIPをアップロードする。

## Pythonで実行

一連の手順をPythonで実行できるようにしました。
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

参考：[BlenderでPythonを実行する方法](https://qiita.com/SaitoTsutomu/items/cec67381a8789b40e377)

以上

