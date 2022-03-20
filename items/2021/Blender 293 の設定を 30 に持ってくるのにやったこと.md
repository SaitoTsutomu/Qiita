title: Blender 2.93 の設定を 3.0 に持ってくるのにやったこと
tags: Python Blender
url: https://qiita.com/SaitoTsutomu/items/b4326269a2e0d5f48b19
created_at: 2021-12-04 08:46:45+09:00
updated_at: 2021-12-07 17:42:53+09:00
body:

# Blender3.0リリース

Blenderの3.0が12/3にリリースされました。
ちょっと使ってみたので、その紹介をします。

環境はmacOSです。管理者権限のユーザーで実行しています。

## インストール

まずは、2.93を残しておくために下記を実行しています。

```bash
mv /Applications/Blender.app/ /Applications/Blender.2.93.app/
```

https://www.blender.org/ の「Download Blender」を押してインストーラーをダウンロードしてインストールします。

3.0も下記のようにフォルダを変更します。

```bash
mv /Applications/Blender.app/ /Applications/Blender.3.00.app/
```

アプリケーションのフォルダを開いて、Blender.3.00を起動しましょう。

![スクリーンショット 2021-12-04 7.43.50.jpg](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/13955/3dabc661-959c-cb25-dd41-ff55291d10e3.jpeg)

新しい[スプラッシュスクリーン](https://cloud.blender.org/p/gallery/617933e9b7b35ce1e1c01066)ですね。
「Load 2.93 Settings」を押します。

- 2.93の設定を引き継いでくれました。
- 新規作成時のデフォルトも引き継いでくれました。
- アドオンも2.93のものがインストールされてました。

下記のようにエイリアスを設定します。

```bash
alias blender=/Applications/Blender.3.00.app/Contents/MacOS/Blender
alias blender_pip="/Applications/Blender.3.00.app/Contents/Resources/3.0/python/bin/python3.9 -m pip"
```

blenderのPythonのライブラリーは自前で作業が必要のようです。上記で作成した`blender_pip`で必要なライブラリーをインストールします。

行った移行作業はここまでです。簡単でした。

## ちょっと使ってみる。

UIは若干違うところもありますが、2.93と同じように使えました。
macOSだと日本語入力できませんでしたが、一部は日本語入力できるようになってますね。

適当なモデルでCyclesのレンダリング時間をはかってみました。

![スクリーンショット 2021-12-04 8.09.54.jpg](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/13955/26c487e3-5765-4c59-19ad-d3c70dfcec69.jpeg)

上が2.93で下が3.0です。1.4倍くらい速くなってます。
とはいえ、思ったとおりにレンダリングできないモデルもあったので、しばらく2.93を使い続けようと思います。

また、3.0以降のロードマップについては、「[Blender3のロードマップを皆で読もう！ - Youtube](https://youtu.be/to4qkYs83m0)」が参考になりました。

## 追記

[Asset Demo Bundles](https://www.blender.org/download/demo-files/)から、アセットブラウザーのサンプル（Cube Diorama）とポーズライブラリーのサンプル（Ellie Pose Library）をダウンロードできます。

「Cube Diorama」は、そのまま開いて実行できました。
「Ellie Pose Library」は、そのままだと実行できませんでしたが、下記のようにしたらできました。

- 先にBlenderを起動する。
- 編集メニューのプリファレンスのアドオンで「pose」で検索して出てくる「Animation: Pose Library」をチェックする。

![image.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/13955/88345b5d-4671-b1f0-25db-5ae551e47efa.png)

- Blenderの「開く」で`ellie_animation.blend`を選んで開く。ただし、右上の歯車アイコンの設定で「UIをロード」のチェックを外しておく。

![image.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/13955/4b273b57-46d8-b696-449e-825043fa44db.png)

- ビューポートの画面を分割して、片方の画面のエディタータイプからアセットブラウザーを選ぶ。

![image.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/13955/44fb2dab-63ff-1cdf-67c0-9b175ee67bba.png)

- 好きなポーズを選んでポーズライブラリーの適用を押す。

それでは、よきBlenderライフを。




