title: Blenderで正多面体
tags: Blender 正多面体
url: https://qiita.com/SaitoTsutomu/items/4b977a8f75b30b369067
created_at: 2022-01-10 07:36:58+09:00
updated_at: 2022-01-12 22:56:53+09:00
body:

## Blenderで正多面体

Blenderで**辺の長さ1の正多面体**を作成する方法を紹介します。

以降では、編集モードで「ビューポートオーバーレイ」の「計測」の「辺の長さ」をオンにし、選択辺の長さが1であることが確認できるようにしています。

### 正四面体

<img src="https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/13955/0b3cf513-747f-17b5-6768-ed62e8fbaed0.jpeg" width="300">

追加メニューのメッシュの円錐（Cone）

- 頂点：`3`
- 半径1：`sqrt(1/3)`
- 深度：`sqrt(2/3)`

### 正六面体

<img src="https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/13955/8d4007ba-26af-2344-06ef-1f003c04e084.jpeg" width="300">

追加メニューのメッシュの立方体（Cube）

- サイズ：`1`

### 正八面体

<img src="https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/13955/c8557a84-566b-2b0d-57e9-ab59468b6e0f.jpeg" width="300">

正六面体の双対多面体を作成することで、正八面体を作成します。

- 追加メニューのメッシュの立方体（Cube）で、正六面体を作成します。
  - サイズ：`sqrt(2)`
- 編集モードに入ります。
- 辺メニューの「辺をベベル」を選び、`[Enter]`を押します。
  - 幅のタイプ：`%`
  - 幅のパーセント：`50`
- メッシュメニューのマージの「距離で」
- オブジェクトモードに戻ります。

### 正十二面体

<img src="https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/13955/f8124ac4-40ad-8e40-dd45-4b2b479e4461.jpeg" width="300">

正二十面体の双対多面体を作成することで、正十二面体を作成します。

- 追加メニューのメッシュのICO球（Icosphere）で、正二十面体を作成します。
  - 細分化：`1`
  - 半径：`1.763`
- 編集モードに入ります。
- 辺メニューの「辺をベベル」を選び、`[Enter]`を押します。
  - 幅のタイプ：`%`
  - 幅のパーセント：`100/3`
- メッシュメニューのマージの「距離で」
- オブジェクトモードに戻ります。

### 正二十面体

<img src="https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/13955/5306ea05-2005-cc55-0ac3-b50be9c24537.jpeg" width="300">

追加メニューのメッシュのICO球（Icosphere）

- 細分化：`1`
- 半径：`0.952`

## 補足

- 実数値は、[正多面体のデータ（厳密値）](https://qiita.com/ikiuo/items/0292a58993c4e6d14f2d)を参考にすると、より正確になるかもしれません。
- 頂点の座標を知りたければ、別画面でエディタータイプをスプレッドシートにすると確認できます。

以上


