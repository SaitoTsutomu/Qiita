title: Blenderで別の画像を重ね合わせる方法
tags: 3DCG Blender
url: https://qiita.com/SaitoTsutomu/items/5464233bc9dfebd93307
created_at: 2022-03-22 16:12:18+09:00
updated_at: 2022-03-22 16:12:18+09:00
body:

## 概要

すでに存在しているマテリアルの上に、一部だけ別の画像を重ね合わせる方法を紹介します。
たとえば、下記のように地球のマテリアルの上に葉っぱを重ね合わせます。

<img src="https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/13955/a277c5a4-d302-53e7-0c9f-cbbcf315a4f7.png" width="400">

わかりやすい方法としては、メッシュを複製して分離して別オブジェクトにする方法があります。しかし、この方はメッシュが別管理になり修正が面倒になります。

ここでは、メッシュはそのままで、別の画像を重ね合わせる方法を紹介します。

## この方法のポイント

- 元のマテリアルをグループ化して再利用可能にする
- 重ね合わせたい部分について、元のマテリアルのUVマップとは別に、重ね合わせ用のUVマップを作成する
- 重ね合わせたい部分について、RGBミックスで異なるUVマップのカラーをミックスする

## 手順

具体例を通して説明します。

- UV球を追加します。
- Shadingワークスペースを開き、マテリアルを新規追加し、ベースカラーに地球の画像テクスチャを指定します（下図）。

<img src="https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/13955/a6c26617-7797-df93-3b26-3eed3736decb.png" width="400">

- プリンシプルBSDFノードより左側の部分（今回は画像テクスチャノードだけ）を選択し、`Ctrl + G`（グループ作成）でグループ作成します。特に編集しないので、`Tab`で戻ります。作成したグループに名前をつけます。ここでは`base`とします（下図）。

<img src="https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/13955/84aff9fe-e87b-efb7-4cc0-1c5fdc67343b.png" width="300">

※ 今回は、画像テクスチャノードだけですが、もっと複雑なノード構成でも可能です。

- マテリアルを追加し、同じマテリアルを選びます（下図）。

<img src="https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/13955/4244895b-95be-96a9-79f4-afd6dcb5b260.png" width="240">

- コピーを作りたいので、上図の「`2`」のボタン、もしくはその2つ隣の「新規マテリアル」のボタンを押します（下図）。これにより、このマテリアルを修正しても元のマテリアルは変更されなくなります。

<img src="https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/13955/6dfb5cac-7ab1-03a5-bc08-b5e8a4b1fe8b.png" width="200">

- Shadingワークスペースのまま、3Dビューポートで編集モードに入り、重ね合わせしたい部分を選択します。

<img src="https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/13955/bf7f0d1b-97c6-c0f4-6eae-a9d4b68b85a6.png" width="300">

- 編集モードのまま、マテリアルプロパティで`Material.001`を選択していることを確認し「割り当て」ボタンを押します（下図）。

<img src="https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/13955/7ec6cf4d-3261-e3ac-d568-7614549ff5c3.png" width="200">

- オブジェクトモードに戻ります。
- 画像テクスチャノードとRGBミックスノードを追加し、下記のようにノードを組みます。左下の画像テクスチャノードが重ね合わせたい画像です。画像で重ね合わせしたくない部分のアルファは0とします。

<img src="https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/13955/931982a4-e0ac-cb9e-0cbe-7b65e96a0ba5.png" width="600">

- このままでは、思った通りの画像が出ないので、新しくUVマップを作ります。
- UV Editingワークスペースを開き、重ね合わせしたい画像を開きます。
- 右下のオブジェクトデータプロパティのUVマップの「`+`」ボタンを押し、新しいUVマップを作ります。

<img src="https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/13955/332e7042-1d78-b30e-ef38-480cf1232513.png" width="300">

- 重ね合わせしたい部分がうまく表示されるように、UVを編集します（下図）。

<img src="https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/13955/400ca363-0987-eea6-31c8-380de0431eb0.png" width="300">

- Shadingワークスペースに戻り、`Shift + A`（追加）→入力→UVマップでUVマップノードを追加し、対象のUVマップに新しく作成したUVマップを指定します。そして画像テクスチャノードと接続します（下図）。

<img src="https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/13955/bc9de33f-d852-0247-599d-cc8f46c1ad38.png" width="300">

これにより、下記のように一部だけ重ね合わせしたマテリアルになります。

<img src="https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/13955/a277c5a4-d302-53e7-0c9f-cbbcf315a4f7.png" width="400">

## 補足

今回は、RGBミックスノードで、カラーをミックスしました。シェーダーミックスノードを使えば、シェーダーを重ね合わせできます。ただし、シェーダーミックスノードは、Eeveeしか使えないのでご注意ください。

以上

