title: Blenderでアニメーションのオブジェクトをステップごとに可視化する
tags: Python 3DCG animation Blender
url: https://qiita.com/SaitoTsutomu/items/ec03097bc67e8978f8fe
created_at: 2022-04-17 16:50:22+09:00
updated_at: 2022-05-06 20:30:49+09:00
body:

## 概要

アニメーションのオブジェクトがどのように動くかをひと目で確認する方法を紹介します。
ここでは、パス追従コンストレイントのオブジェクトを対象にします。

<img src="https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/13955/667f71bd-131e-9667-ed36-dcff918ee169.jpeg" width="400">

## 具体例

具体例で説明します。
オブジェクトとして、モンキー（`Suzanne`とします）を作成してください。
また、パスに沿ってアニメーションさせるために、ベジエカーブを作成し、適当に編集してください。
モンキーを選択し、Shiftを押しながらベジエカーブを選択し、`Ctrl + P`(ペアレント）のパス追従コンストレイントを選んでください。
スザンヌを選択し、オブジェクトコンストレイントプロパティで下記のように設定してください。

- 前方の軸：`-Y`
- カーブに従う：チェック

<img src="https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/13955/4f9a3757-af0c-9e83-ef8d-9104b09e7882.jpeg" width="300">

上図の`パスアニメーション`ボタンを押してください。

レンダリングの最終フレームを250から100に変えてください。

この状態でスペースを押すとアニメーション実行がトグルで切り替わるので、確認しましょう。

## Pythonで可視化

Scriptingワークスペースで、テキストを新規作成し、下記をコピペしテキストメニューのスクリプト実行をしてください。
スクリプトでは、フレームの`20, 40, 60, 80`で、Suzanneを複製し、コンストレイントを適用しています。

```py
import bpy

bpy.ops.object.select_all(action='DESELECT')
obj = bpy.data.objects["Suzanne"]
for t in range(0, 100, 20):
    bpy.context.scene.frame_current = t
    bpy.context.view_layer.objects.active = obj
    obj.select_set(True)
    bpy.ops.object.duplicate_move()
    bpy.ops.constraint.apply(constraint="AutoPath")
    bpy.context.object.select_set(False)
bpy.context.scene.frame_current = 100
```

参考：[BlenderでPythonを実行する方法](https://qiita.com/SaitoTsutomu/items/cec67381a8789b40e377)

以上

