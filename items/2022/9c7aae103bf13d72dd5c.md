title: Blender 4.2で花火を打ち上げるアドオン
tags: Python 3DCG addon Blender
url: https://qiita.com/SaitoTsutomu/items/9c7aae103bf13d72dd5c
created_at: 2022-04-11 07:10:13+09:00
updated_at: 2024-10-05 09:13:31+09:00
body:

Blenderで、花火を打ち上げるアドオンをPythonで作成したので紹介します。

<img src="https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/13955/a5d919a0-ae1e-e31f-af96-580e25f88813.gif" width="300">

## やり方

### アドオンのインストール

- [Blender Add-on: Fireworks](https://github.com/SaitoTsutomu/Fireworks)の画面にしたがってインストールしてください

### Tomlファイルの作成

花火の設定は、Tomlファイルで行います。アドオンには、下記のサンプルTomlファイルが含まれています。

* [サンプルTomlファイル](https://github.com/SaitoTsutomu/Fireworks/blob/master/fireworks.toml)

**サンプルの説明**

`shot1`は、作成する花火のオブジェクトの名前です。任意の名前が使えます。花火はいくつでも作成できます。
`launch`は打ち上げ時のフレーム（アニメーションの時刻のようなもの）です。`explode`は爆発時のフレームです。

花火はパーティクルで実現しています。
上記では、下記の３つのパーティクルシステムを設定しています。いくつでも設定できます。パーティクルシステムの名前も任意です。

- `up`：爆発までの火花
- `ex1`：内側の爆発
- `ex2`：外側の爆発

### 作成

- サイドバーの編集タブの「Fireworks」を開いてください
- `file`に作成したファイルを指定します
  - デフォルトの `./fireworks.toml` はサンプルの指定です
- `Make（作成）`ボタンを押します

## 補足

花火の色はカラーランプで、時間により色が変わるようにしています。Cyclesではパーティクル情報ノードが使えたようなのですが、Eeveeだとパーティクルの情報が取得できなかったので、ドライバーで設定しています。爆発時にカラーランプの係数が0で、爆発終了＋寿命で係数が1になります。

### Pythonのコード

https://github.com/SaitoTsutomu/Fireworks/blob/main/__init__.py

以上

