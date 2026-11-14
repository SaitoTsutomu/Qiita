title: Blenderのジオメトリーノードメモ
tags: 3DCG Blender
url: https://qiita.com/SaitoTsutomu/items/39eb1f022218c647c323
created_at: 2023-01-21 13:54:20+09:00
updated_at: 2023-01-22 08:49:10+09:00
body:

# はじめに

Blender3.4のジオメトリーノードのメモです。

## 参考

https://docs.blender.org/manual/ja/latest/modeling/geometry_nodes/

https://qiita.com/SaitoTsutomu/items/f509adeaabd0b8302608

https://www.ultra-noob.com/category/000/

## メモ

ジオメトリーノードは、数が多いです。ノードを追加しようにも、どこにあるか覚えてられません。そうすると、`Shift + A`で追加するより、ドラッグして出てくる欄に手打ちする方が良さそうです。

ノード名を手打ちする場合、英語で入力する方が手間がかかりません。普段は日本語UIにしているので、日本語と英語をワンタッチで切り替えられるようにしています（下記を参考にアドオンを作成しています）。

https://www.cgradproject.com/archives/5503/

- リンク上の値は、マウスカーソルをソケットにホバーさせると確認できます。
- Group Outputにつないだ値は、Modifier PropertiesのOutput Attributesに名前をつけることで、Spreadsheetで確認できます。ベクトルは平均となるようです。
- 属性の指定は、接続されたノードの属性が渡されます。同じ属性の指定ノードからつながっていても別の値になります。そのノード時点での属性の取得は、Capture Attributeを使います。
- ソケットは形と色で種類がわかります。
- ポイントは位置情報です。頂点はメッシュを構成する要素です。メッシュの面が持つのは頂点です。カーブが持つのはポイントです。
- Selectionに数値を渡すと、０より大きいものが選択されます（０以外ではないので注意）。

## 概要を学ぶ

操作や概念がわかりやすい動画です。Part9まであります。

https://www.youtube.com/watch?v=BfrFakU5XTY

Node Wranglerに慣れましょう。

---

# サンプル

以降では、GroupInputを使わないので、基本的にメッシュは何でも良いです（CubeでOK）。

## サンプル - 卵

UV球をプロポーショナル編集すればできますが、ジオメトリーノードで作ると結構たいへんです。
<img src="https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/13955/49d604f1-b3c0-2e25-f98f-cf00e0242b9a.png" width="160">

![image.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/13955/415cb4dd-5767-ca8f-dfcf-b67cc186a450.png)

簡単な説明

1. UV Sphere: UV球を元にしています。`XYZ`が`±１`の範囲にあります。
2. Position: 位置属性を取り出し、(３)と(７)の入力にします。(３)の方で卵型に変形を計算します。
3. Separate XYZ: `Z`だけ取得します。
4. Map Range: 入力が`±1`なので、`0-1`の範囲になるようにします（よく使うノードです）。
5. Float Curve: カラーランプのように`0-1`の範囲を`0-1`に変換します。ここでは、`Z`を「卵型への係数」に変換します。
6. Combine XYZ: (５)からXとYにつなぎます。`Z`は`１`です。
7. Vector Math: ベクトルの掛け算をします。ここで、球を卵型にします。
8. Set Position: 位置を設定します。これによりジオメトリーが卵型になります。
9. Set Shade Smooth: スムーズをかけます。

## サンプル - バウンディングボックス

メッシュのバウンディングボックスを「バウンディングボックスのノード」を使わずに作成します。
ここでは確認のためGroupInputを使います。下図はスザンヌの例です。

<img src="https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/13955/9b11642b-5384-f3f8-7780-aab5cde9666f.png" width="240">

![image.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/13955/c0543fb2-ae38-70ca-2295-08fb68885357.png)

簡単な説明

1. Group Input: (３)と(８)につながってます。(3)からバウンディングボックスを計算します。
2. Position: 位置属性を指定します。
3. Attribute Statistic: 属性の統計を取り出します。ベクトルを指定し、位置のMinとRangeを取得します。
4. Vector Math: ベクトルの計算をします。Rangeに`0.5`をかけて、Minを足します。これが中心位置になります。
5. Cube: RnageをサイズとしてCubeを作成します。
6. Transform: (4)の値だけ移動します。
7. Mesh To Curve: カーブに変換することでワイヤーフレームになります。
8. Join Geometry: (1)と(7)を結合します。

---

# 各ノード

## [Attribute Statistic(属性統計)ノード](https://docs.blender.org/manual/ja/latest/modeling/geometry_nodes/attribute/attribute_statistic.html)

[サンプルのバウンディングボックス](https://qiita.com/SaitoTsutomu/items/39eb1f022218c647c323#バウンディングボックス)のように属性の統計情報を取得します。

## [Capture Attribute(属性キャプチャ)ノード](https://docs.blender.org/manual/ja/latest/modeling/geometry_nodes/attribute/capture_attribute.html)

入力時点のValueで指定された属性を取得します。

## [Domain Size(ドメインサイズ)ノード](https://docs.blender.org/manual/ja/latest/modeling/geometry_nodes/attribute/domain_size.html)

ドメイン（ポイントや辺など。下記参照）のサイズを取得します。

https://docs.blender.org/manual/ja/latest/modeling/geometry_nodes/attributes_reference.html#attribute-domains

## [Remove Named Attribute(名前付き属性削除)ノード](https://docs.blender.org/manual/ja/latest/modeling/geometry_nodes/attribute/remove_named_attribute.html)

指定した名前の属性を削除します。

## [Store Named Attribute(名前付き属性格納)ノード](https://docs.blender.org/manual/ja/latest/modeling/geometry_nodes/attribute/store_named_attribute.html)

値を、指定した名前の属性として保存します。

## [Color Ramp(カラーランプ)ノード](https://docs.blender.org/manual/ja/latest/modeling/geometry_nodes/color/color_ramp.html)

値をカラーにマッピングします。

## [Combine Color(カラー合成)ノード](https://docs.blender.org/manual/ja/latest/modeling/geometry_nodes/color/combine_color.html)

RGBなどからカラーを作成します。

## （カラーの）[Mix(ミックス)ノード](https://docs.blender.org/manual/ja/latest/modeling/geometry_nodes/color/mix_rgb.html)

色をさまざまな方法でブレンドします。
Blender3.4では、Node Wranglerで作成すると、古い（下記の左）ので注意しましょう。

![image.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/13955/0e326fe1-d5d7-e739-ce5f-301c8e44de14.png)

## [RGB Curves(RGBカーブ)ノード](https://docs.blender.org/manual/ja/latest/modeling/geometry_nodes/color/rgb_curves.html)

CRGBごとに曲線で変換を指定できます。Cは統合で、コントラストを補正します。

## [Separate Color(カラー分離)ノード](https://docs.blender.org/manual/ja/latest/modeling/geometry_nodes/color/separate_color.html)

カラーからRGBなどを作成します。







---

適宜更新します。

