title: Blenderでミラーボールを作ろう
tags: 3DCG 初心者 Blender モデリング Blenderで作ろう
url: https://qiita.com/SaitoTsutomu/items/2fd6d9d7afa6b5cdda94
created_at: 2022-03-20 13:14:55+09:00
updated_at: 2022-03-20 13:14:55+09:00
body:

## はじめに

「Blenderに興味があるけど、しきいが高そう」という方向けに、なるべくわかりやすくミラーボールの作り方を紹介します。
Blenderの基本的な操作方法は、「[Blenderでサッカーボールを作ろう](https://qiita.com/SaitoTsutomu/items/e7e5114a5916843dd068)」に書いてあるので、先にそちらをやってみてください。

## 対象読者

- Blenderで何か作ってみたいけど、難しいと思っている人

## 完成物

<img src="https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/13955/86317714-ef5d-00b2-805e-f0f92db8e398.jpeg" width="360">

[完成物をSketchfabで見る](https://skfb.ly/otDDo)

## 手順

操作方法は、日本語設定時の表記になっています。日本語設定の方法は、[こちら](https://vook.vc/n/3779#toc-2)を参考にしてください。
macOSでのキーを書いています。Windowsの場合は、`Option`を`Alt`に読み替えてください。
間違えたときは、`Ctrl + Z`で戻ります。それでもよくわからなくなったら、`Ctrl + N`の「新規ファイル」の「全般」で最初からやり直してみてください。

- 3Dビューポートの表示はシェーディングで変わります。起動時はソリッドモードになっています。色を確認できるように**マテリアルプレビューモード**に変えてください。`Z`を押すと下図のような表示になります。この表示をパイメニューといいます。パイメニューは、マウスカーソルを少し動かすと選択肢を切り替えられます。マウスカーソルを少し下のように動かし、図のように真ん中の丸の下を青くしてマウスをクリックしてください。

<img src="https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/13955/76f6bae2-c23a-dc4d-f243-e8d5067a5c2d.jpeg" width="500">

- マテリアルプレビューモードになると、右上が下図のようになります。もし、下図のようになっていなかったら、下図の青いところをクリックしてもマテリアルプレビューモードに変更できます。

<img src="https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/13955/21755d1b-da6f-e581-8b9d-f6ef96655a78.jpeg" width="300">

- 最初にある立方体は使わないので削除します。立方体を選択して`X`、`[Enter]`で削除できます。
- 操作が簡単になるようにアドオンを有効にします。アドオンとは、Blenderを機能拡張をするしくみです。
  - 編集メニューの「プリファレンス」を選び、表示される画面の左側から「アドオン」を選んでください。
  - 下図のように、虫眼鏡のボックスに`tis`と入力して表示される`Mesh: Tissue`をチェックしてください。チェックしたら画面を閉じてください。

<img src="https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/13955/b08e57f9-c651-561e-fa09-795c5a615a08.jpeg" width="600">

- ミラーボールの元になるオブジェクトを作成しましょう。
  - `Shift + A`で追加メニューが開きます。下図のように「メッシュ」の「ICO球」を選んでください。

<img src="https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/13955/0dbf1679-d727-9506-01da-6b349e626c1d.png" width="320">

- 画面左下の「ICO球を追加」をクリックして開いてください。下図のように、「細分化」を`4`にしてください。

<img src="https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/13955/011640d2-6a50-e4c1-282f-5983efca5dca.jpeg" width="360">

- ICO球（以降ではIcosphereと呼びます）を選択したまま、`N`を押すと画面右上に**サイドバー**が表示されます。サイドバーの右の「Tissue」タブを押します。「Convert to Dual Mesh」ボタンを押してください（下図）。

<img src="https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/13955/dc5a6a31-6a7d-d9a5-6ccf-0b51be488d25.png" width="300">

- Icosphereを選んだまま、右下のプロパティ画面で下図のように青いスパナのアイコンをクリックして**モディファイアープロパティ**にしてください。モディファイアーについては「はじめに」の紹介記事も参考にしてください。

<img src="https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/13955/46ad97b7-3991-c158-a624-8c18d24ba080.png" width="300">


- 「モディファイアーを追加」から「辺分離」を選んでください。
  - 「辺の角度」を`1`にします（下図）。

<img src="https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/13955/3fb93fa1-c063-c558-e398-8013f497872e.png" width="240">

- 「`∨`」をクリックしてたたんでおきましょう。
- 「モディファイアーを追加」から「サブディビジョンサーフェス」を選んでください。
  - 「ビューポートのレベル数」を`2`にします（下図）。

<img src="https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/13955/6f65d6d3-bef9-4723-8d4b-06dad2dca47c.jpeg" width="240">

仕上げに質感を設定しましょう。

- Icosphereを選んだまま、プロパティ画面の赤い丸っぽいアイコンをクリックして**マテリアルプロパティ**にしてください。
  - 「新規」を押してください。
  - 「サーフェス」の「メタリック」を`1`にしてください。
  - 「サーフェス」の「粗さ」を`0.1`にしてください（下図）。

<img src="https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/13955/fc63ab5f-bedd-557c-aa9a-5a1d25078417.jpeg" width="280">

- 完成です！

本記事では、少ない手順で完成できるように心がけましたが、オブジェクトやマテリアルに名前をつけた方がわかりやすくなります。また、操作を迷わないように数値入力しましたが、マウス操作で調整することもできます。慣れてきたらマウス操作で調整してみましょう。
Blenderは、覚えることがたくさんあって使いこなすのが大変ですが、いろいろなことができて楽しいので、ぜひ体験してみてください。

参考：いろいろな「[Blenderで作ろう](https://qiita.com/tags/blenderで作ろう)」

以上

