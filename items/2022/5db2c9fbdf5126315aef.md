title: Blenderのちょっとした自作アドオンの紹介
tags: Python 3DCG addon Blender
url: https://qiita.com/SaitoTsutomu/items/5db2c9fbdf5126315aef
created_at: 2022-05-08 17:41:09+09:00
updated_at: 2022-05-08 17:41:09+09:00
body:

## 概要

Blenderのちょっとした自作アドオンを紹介します。

- OpenURL：テキストに書いてあるURLからブラウザを開きます。
- ShapeKeyBit：シェイプキーのちょっとしたツールです。

## OpenURL

### アドオンのインストール

- [Blender Add-on: OpenURL](https://github.com/SaitoTsutomu/OpenURL)の画面にしたがってインストールしてください。
    - アドオンのチェックでは「テスト中」を選んでください。

### 使い方

- URLの記述されたテキストを選択します。
- オブジェクトメニューの`Open URL`を選びます。

### Pythonのコード

https://github.com/SaitoTsutomu/OpenURL/blob/main/__init__.py

## ShapeKeyBit

### アドオンのインストール

- [Blender Add-on: ShapeKeyBit](https://github.com/SaitoTsutomu/ShapeKeyBit)の画面にしたがってインストールしてください。
    - アドオンのチェックでは「テスト中」を選んでください。

### 使い方

シェイプキーを持つオブジェクトを選択します。
サイドバーの編集タブのShapeKeyBitで、下記を実行できます。

- Select Diff：選択したシェイプキーとBasisシェイプキーとの差分を選択して表示します。
- Set Vert：選択したシェイプキーの選択している点を対象のシェイプキーに反映します。対象のシェイプキーのインデックスは、パネルの`Target ShapeKey Index`に指定します。
- Save CSV：選択したシェイプキーの選択している点をCSVに出力します。
- Load CSV：シェイプキーのCSVを読み込み反映します。

たとえば、Basisで行うべき修正を別のシェイプキーで行った場合、影響範囲を確認したり、シェイプキー間で反映したりできます。

### Pythonのコード

https://github.com/SaitoTsutomu/ShapeKeyBit/blob/main/__init__.py

以上

