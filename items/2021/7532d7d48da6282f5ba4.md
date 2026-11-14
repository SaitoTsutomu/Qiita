title: Blenderチャレンジ：らせんトーラス
tags: 3DCG Blender クイズ Blenderチャレンジ
url: https://qiita.com/SaitoTsutomu/items/7532d7d48da6282f5ba4
created_at: 2021-12-12 17:49:24+09:00
updated_at: 2021-12-22 20:06:35+09:00
body:

3DCGソフトウェアのBlenderを使って、お題のモデルを作成してみましょう。
やり方は一通りではないと思います。あなたは、どんな方法を考えますか？

## 問題

下図のようなモデルを作成してください（色はだいたいでOK）。

![スクリーンショット 2021-12-12 17.13.28.jpg](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/13955/9fbd1041-98b7-7591-5304-12fa77e0d24a.jpeg)

[完成物をSketchfabで見る](https://skfb.ly/orXwK)

※ できれば、テクスチャを使わない方法で

…
…
…

OK？

---

## 解答例

作成する手順です。

- `Shift + A`の追加で「カーブ」→「円」で円を追加します。名前を`BezierCircle`とします。
- アドオンの「Add Mesh: Extra Objects」を有効にします。
- `Shift + A`の追加で「メッシュ」→「Single Vert」→「Add Single Vert」で点を追加します（編集モードに入ることに注意）。
- `GX.25`、`[Enter]`（`0.25 = 0.5 / 2`、寸法`Z`の半分）
- `EZ.5236`、`[Enter]`（`0.5236 ≒ π / 6`）
- `A`、「細分化」、さらに「細分化」
- `[Tab]`でオブジェクトモードにします。
- マテリアルを追加し、赤にします。
- 「スクリュー」モディファイアーを追加し、「スクリュー」を`1.0472`に、「反復」を`6`にします（`1.0472 ≒ π / 3`）。
- 「カーブ」モディファイアーを追加し、「カーブオブジェクト」を`BezierCircle`に、「変形軸」を`Z`にします。

![スクリーンショット 2021-12-12 19.13.39.jpg](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/13955/399216bb-0c8d-c438-de29-5ab9efd9fa68.jpeg)

- `Shift + D`、`RZ180`、`[Enter]`
- マテリアルをシングルユーザー化し、青にします。

以上

