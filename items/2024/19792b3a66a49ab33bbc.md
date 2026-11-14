title: Blender 4.2で星空を作ろう
tags: Python 3DCG Blender
url: https://qiita.com/SaitoTsutomu/items/19792b3a66a49ab33bbc
created_at: 2024-07-17 06:20:49+09:00
updated_at: 2024-10-12 13:33:03+09:00
body:

Blender 4.2 LTSがリリースされました！

https://www.blender.org/

さっそく、次のような星空を作ってみましょう。

<img src="https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/13955/af995d56-931d-f3eb-7dbf-02bb6e0f1d2d.png" width="480">

## まずは、アドオンをインストールしよう

次のリンク先からアドオンをダウンロードしてください。ダウンロードしたZIPファイルは**解凍せずに**使います。

https://github.com/SaitoTsutomu/StarrySky/archive/refs/heads/master.zip

次の手順でアドオンをインストールします。

* 編集メニューのプリファレンスを選ぶ
* 左のタブの中からアドオンを選ぶ
* 右上の `v` のボタンの「ディスクからインストール…」を選ぶ（下図）
* ダウンロードしたファイルを選択し、「ディスクからインストール」を押す

![](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/13955/3b4de8d6-8f54-cb32-3be4-a2894b013fd1.png)

## 星空を作る

最初に、立方体があれば削除してください。
次に、オブジェクトメニュー（下図）の一番下にある「Starry Sky」を選んでください。

![](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/13955/f55807e4-73d0-058d-2e1a-92cc7a090667.png)

:::note info
**ノート**
メニューが選びにくいときは、メニュー表示後に上矢印を押してEnterを押してください。
:::

星空が作成されました！

## 説明

しくみについては、次の記事を参照してください。

https://qiita.com/SaitoTsutomu/items/1161fce06ade74be4d5d

アドオンの詳細については、GitHubを参照してください。

https://github.com/SaitoTsutomu/StarrySky

データは、次のサイトからダウンロードして加工したものをアドオンに組み込んでいます。

http://astro.starfree.jp/commons/hip/

先程の記事との違いです。

* Blender 4.2で動くように修正した
* 簡単に、使えるようにアドオンにした
* データをアドオンに埋め込んだ
* コンポジターを作成しブルームを設定した
* pandasがなくても使えるようにした

BlenderのPythonで、pandasっぽいことをしてみたいときに、参考になるかもしれません。

## Blender 4.2対応の記事について

下記の記事は、Blender 4.2で動作確認しています。

https://qiita.com/SaitoTsutomu/items/19792b3a66a49ab33bbc

https://qiita.com/SaitoTsutomu/items/9c7aae103bf13d72dd5c

https://qiita.com/SaitoTsutomu/items/33b376c82a96434672d3

https://qiita.com/SaitoTsutomu/items/711989ba3e5ebcb78730

https://qiita.com/SaitoTsutomu/items/4ff1e6c1bb9a34a8128b

https://qiita.com/SaitoTsutomu/items/ea976764e13e408420e8

https://qiita.com/SaitoTsutomu/items/20ce443d0b0675716705

https://qiita.com/SaitoTsutomu/items/7c96f67cfb88cc39d9f3

https://qiita.com/SaitoTsutomu/items/72734602fcf3f993f8e3

https://qiita.com/SaitoTsutomu/items/b608c80d70a54718ec78

https://qiita.com/SaitoTsutomu/items/2425a51139b79c6d87fa

https://qiita.com/SaitoTsutomu/items/8c39e65fa2fc443d87b7

https://qiita.com/SaitoTsutomu/items/dda5b92ba636728bbb39

以上

