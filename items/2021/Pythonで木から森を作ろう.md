title: Pythonで木から森を作ろう
tags: Python 3DCG Blender
url: https://qiita.com/SaitoTsutomu/items/6a6c45f3bf52d15d5bd0
created_at: 2021-11-06 07:23:11+09:00
updated_at: 2021-12-02 07:01:06+09:00
body:

この記事は、Blender Advent Calendar 2021の2日目の記事です。「[ささらBch ローポリの森](https://youtu.be/du2dyCzM65M)」を参考にして作成しました。

- macOSのBlender2.93で動作確認してますが、Windowsでも動くはずです。
- 記事中の文言は、言語設定を`日本語`にしたものです。英語にしている方は適宜読み替えてください。

## 完成物のサンプル

下記のようなモデルをPythonを使って作成します。

![forest.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/13955/5320e12b-6f45-e542-555f-e5532dc2d341.png)

## 対象読者

- Blenderでモデルを作ったことがある方
- Pythonを使ったことがある方

## ローポリの木を作ろう

最初に、森の元になる1本の木を作りましょう。
Blenderを起動してください。初期状態の立方体は使わないので削除してください。

※ macOSでBlenderのPythonを使う場合、コンソールからBlenderを起動すると、コンソールでエラーメッセージを確認できて便利です。

- `Shift + A`、`メッシュ`、`円錐`で円錐を作成します。左下の設定は下記のようにしてください。

![スクリーンショット 2021-11-06 5.39.27.jpg](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/13955/8c80d3b2-65ae-6870-39bf-0d4a7352a048.jpeg)


- `3Dビューのシェーディング`を`マテリアルプレビュー`にしてください。
- マテリアルを新規作成し、名前をダブルクリックして`green`にしてください。
- `Shift + D`、`Z.5 [Enter]`、`Shift + R`で上に2つ複製します。下記のようになります。

![スクリーンショット 2021-11-06 6.56.23.jpg](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/13955/a446f685-0a79-fda3-1d36-aadf7ee76198.jpeg)


- `Shift + A`、`メッシュ`、`円柱`で円柱を作成します。左下の設定は下記のようにしてください。

![スクリーンショット 2021-11-06 5.48.04.jpg](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/13955/25aee6d1-a026-ab6b-a645-1c514f23abf5.jpeg)


- マテリアルを新規作成し、名前を`brown`にしてください。ベースカラーを適当に茶色（例：16進数で`806030`）にしてください。
- 作成した4つのオブジェクトを選択し、`Ctrl + J`で1つのオブジェクトにします。
- 右上のアウトライナーで、名前をダブルクリックして`tree`に変えてください。
- `Ctrl + A`、`全トランスフォーム`でトランスフォームをリセットしてください。

- プロパティ画面の`オブジェクトプロパティ`の一番下の`カスタムプロパティ`を開いて追加を押してください。
  - `編集`を押してください。
    - プロパティ名を`color`に、プロパティ値を`[0.05, 0.2, 0.05, 1.0]`にしてください。デフォルト値も同じ値にしてください。
    - プロパティ値を変えることで、下部にサブタイプが表示されます。サブタイプを`Linear Color`に変えてください。
    - 下図のようになっていれば`OK`を押します。

![スクリーンショット 2021-11-06 6.11.07.jpg](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/13955/2ac5d059-976a-7546-40dc-592566942046.jpeg)


- マテリアルで`green`を選んでください。
- ワークスペースをShadingにします。
- `Shift + A`、`入力`、`属性`で属性を作成します。
- タイプを`オブジェクト`に、名前を`["color"]`にします。下記のように`カラー`を`ベースカラー`につなぎます。

![スクリーンショット 2021-11-06 6.04.10.jpg](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/13955/84ea6c09-d71d-e8dc-c935-d4a9726aa499.jpeg)


- ワークスペースをLayoutにします。
- 木が完成です。

## 地面を作ろう

- `Shift + A`、`メッシュ`、`グリッド`でグリッドを作成します。左下の設定は下記のようにしてください。

![スクリーンショット 2021-11-06 6.15.58.jpg](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/13955/4f2f21c8-7d00-1298-61ca-c6f486a71f45.jpeg)


- マテリアルを新規作成し、名前を`ground`にしてください。ベースカラーを適当にこげ茶色（例：16進数で`302010`）にしてください。
- 編集モードに入ります。
- `メッシュメニュー`、`トランスフォーム`、`ランダム化`で、少しデコボコにします。
- オブジェクトモードに戻ります。
- 地面が完成です。

## 森をつくろう

- 管理しやすいように森を入れるためのコレクションを作りましょう。
  - アウトライナーで右クリックから`新規コレクション`を選び、名前を下記のように`forest`に変えてください。

![スクリーンショット 2021-11-06 6.31.23.jpg](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/13955/9c223879-1b1c-9bb1-a334-96f6a0fe9dd7.jpeg)


- ワークスペースをScriptingにします。
- `新規`を押し、下記を記述します。

```py
import bpy
import random

n = 2000
R = 40

tr = bpy.data.objects["tree"]
c = bpy.data.collections["forest"]
for _ in range(n):
    obj = bpy.data.objects.new("new_tree", tr.data)
    x = (random.random() * 2 - 1) * R
    y = (random.random() * 2 - 1) * R
    s = random.random() * 0.3 + 0.7
    obj.location = x, y, random.random() * 0.4
    obj.scale = s, s, s
    obj.rotation_euler.z = random.random() * 360
    obj["color"] = (
        random.random() * 0.05,
        random.random() * 0.1 + 0.15,
        random.random() * 0.05,
        1,
    )
    c.objects.link(obj)
```

- `テキストメニュー`の`スクリプト実行`を押して完成です。

### コードの解説

- treeを2000個、リンク複製しています。
- リンク複製なので、メッシュは同一のメッシュオブジェクトです。リンク複製にすることで高速に作成でき、ファイルサイズも小さくできます。
- 複製したオブジェクトの位置、サイズ、角度、色を変えています。
- 通常のマテリアルだと、色を変えたい場合、別のマテリアルにすることになります。ここでは、マテリアルのノードでカスタムプロパティで色を指定することにより、同一のマテリアルで色を変えられるようにしています。
  - カスタムプロパティは、オブジェクトの属性なのでリンク複製でも変更可能です。
  - 複製したカスタムプロパティのサブタイプは、`Linear Color`になっていません。`Linear Color`にするのがややこしそうなので、このままにしています。

※ パーティクルを使ってオブジェクトを配置することも可能ですが、今回はPythonを使ってみました。

## レンダリングしよう

モデルの範囲が広いので、ライトは`サン`が良いでしょう。ライトとカメラを調整してレンダリングしてみましょう。

完成例：[Forest using Python - sketchfab](https://skfb.ly/oqFWT)

以上

