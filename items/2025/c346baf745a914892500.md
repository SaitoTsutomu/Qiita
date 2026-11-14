title: Blenderでテクスチャの境目を目立たなくする
tags: 3DCG tips Blender
url: https://qiita.com/SaitoTsutomu/items/c346baf745a914892500
created_at: 2025-08-13 18:20:56+09:00
updated_at: 2025-08-13 18:20:56+09:00
body:

## はじめに

YouTubeで見かけた「テクスチャの境目を目立たなくする方法」を、自分用の備忘録としてまとめます。

## やり方

この記事では、UV球を使って効果を確認します。あらかじめ Node Wrangler アドオンを有効にしておいてください。

1. **UV球を追加**
    * `Shift + A` → メッシュ → UV球
2. **マテリアルの作成**
    * シェーディングワークスペースで「新規」をクリック
    * プリンシプルBSDFの操作
        * 粗さを`1`に変更（見やすくするため）
        * プリンシプルBSDFを選択したまま`Ctrl + T`で「画像テクスチャ」「マッピング」「テクスチャ座標」ノードを追加
    * 画像テクスチャの修正
        * 適当な画像を設定
        * 「平面」から「ボックス」に変更
        * 「ブレンド」に小さな値を設定（例：`0.03`）
    * 「テクスチャ座標」の「生成」出力を、「マッピング」の「ベクトル」入力に接続

設定後は、以下のような見た目になります。

![shading.jpg](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/13955/e7464502-516e-4af4-b92b-117bc1feae72.jpeg)

## ブレンドの値による比較

**ブレンド = 0.00**

![before.jpg](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/13955/9fbaccb7-07d0-42e5-97f0-149c40ff2c42.jpeg)

**ブレンド = 0.03**

![after.jpg](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/13955/019bf043-393b-4932-a434-d2295b0d378d.jpeg)

ブレンド値を少し上げると、水平方向のテクスチャ境界が目立たなくなりました。

## おわりに

テクスチャの境目を目立たなくする方法はいくつかありますが、この方法は設定が簡単で汎用性も高いです。ぜひ試してみてください。

以上

