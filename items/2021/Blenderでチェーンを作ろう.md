title: Blenderでチェーンを作ろう
tags: 3DCG 初心者 Blender モデリング Blenderで作ろう
url: https://qiita.com/SaitoTsutomu/items/0efc83ea526b44c05eb1
created_at: 2021-12-19 10:53:12+09:00
updated_at: 2021-12-22 19:50:28+09:00
body:

## はじめに

「Blenderに興味があるけど、しきいが高そう」という方向けに、なるべくわかりやすくチェーンの作り方を紹介します。
Blenderの基本的な操作方法は、「[Blenderでサッカーボールを作ろう](https://qiita.com/SaitoTsutomu/items/e7e5114a5916843dd068)」に書いてあるので、先にそちらをやってみてください。

## 対象読者

- Blenderで何か作ってみたいけど、難しいと思っている人

## 完成物

<img src="https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/13955/501f1d58-2064-a780-d865-226c8d2d70ee.png" width="600">
[完成物をSketchfabで見る](https://skfb.ly/orXvZ)

## 手順

操作方法は、日本語設定時の表記になっています。日本語設定の方法は、[こちら](https://vook.vc/n/3779#toc-2)を参考にしてください。
macOSでのキーを書いています。Windowsの場合は、`Option`を`Alt`に読み替えてください。
間違えたときは、`Ctrl + Z`で戻ります。それでもよくわからなくなったら、`Ctrl + N`の「新規ファイル」の「全般」で最初からやり直してみてください。

- 最初にある立方体は使わないので削除します。立方体を選択して`X`、`[Enter]`で削除できます。
- 操作が簡単になるようにアドオンを有効にします。アドオンとは、Blenderを機能拡張をするしくみです。
  - 編集メニューの「プリファレンス」を選び、表示される画面の左側から「アドオン」を選んでください。
  - 下図のように、虫眼鏡のボックスに`mirr`と入力して表示される`Mesh: Auto Mirror`をチェックしてください。チェックしたら画面を閉じてください。

<img src="https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/13955/021a3cf6-41c6-c927-5df3-3603683cb6e7.png" width="600">


- チェーンの元になるオブジェクトを作成しましょう。
  - `Shift + A`で追加メニューが開きます。下図のように「メッシュ」の「トーラス」を選んでください。

<img src="https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/13955/a4902b1d-2352-2ea0-c5f9-5844c0ce3518.png" width="500">

- トーラス（以降ではTorusと呼びます）を選択したまま、`N`を押すと画面右上に**サイドバー**が表示されます。サイドバーの右の「編集」タブを押して、「Auto Mirror」を開きます。「Auto Mirror」ボタンを押してください（下図）。

<img src="https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/13955/ba9a24fc-71c3-8256-523b-b6a6e300b20f.jpeg" width="300">

- Torusを選択したまま、`[Tab]`を押して**編集モード**にしてください。左上が下図のようになります。`[Tab]`を押すことでオブジェクトモードと編集モードを切り替えできます。

<img src="https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/13955/f80d0e31-8233-592f-a1cb-fb5c04000a78.png" width="240">

- `AGX.5`、`[Enter]`を押してください。下図のようになります。

<img src="https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/13955/c01f7cbd-06f2-fae3-460c-453b2e913ed8.jpeg" width="300">

- `[Tab]`を押して**オブジェクトモード**に戻ります。左上が下図のようになります。

<img src="https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/13955/ed27597c-ac68-0571-17e2-cbac736d0a39.png" width="240">

- チェーンを表示させる場所を作成します。
- `Shuft + A`の追加メニューで「カーブ」の「パス」を選んでください。NurbsPathが追加されます。

<img src="https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/13955/b7bc147c-f0cd-c0f2-44e8-be925333edf7.jpeg" width="400">

- NurbsPathを選択したまま、`S3`、`[Enter]`で３倍に拡大しておきましょう。
- NurbsPathを選択したまま、`[Tab]`を押して**編集モード**にしてください。
- 下記のように、５つの点を適当に移動してください。移動は、点を選択して`G`キーを押した後にマウスの移動でできます。左クリックで確定、右クリックでキャンセルです。

<img src="https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/13955/b8e186c9-79ec-b3ac-154d-52e7b6736628.jpeg" width="500">

- `[Tab]`を押して**オブジェクトモード**に戻ります。
- `Shuft + A`の「エンプティ」の「十字」を選んでください。Emptyが追加されます。
- Emptyを選んだまま、`RX90`、`[Enter]`でX軸を起点に90度回転します。このEmptyを使うことで、後述するようにTorusを並べたときに、90度ずつ回転するようになります。
- Torusを選んで、右クリックし「スムーズシェード」を選んでください。
- Torusを選んだまま、右下のプロパティ画面で下図のように青いスパナのアイコンをクリックして**モディファイアープロパティ**にしてください。モディファイアーについては「はじめに」の紹介記事も参考にしてください。

<img src="https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/13955/63c31560-4a5b-d944-13fa-ee60b9d85ce9.png" width="300">

- 既に「ミラー」モディファイアーが追加されています。蝶のアイコンの左の「`∨`」をクリックしてたたんでください。
- 「モディファイアーを追加」から「配列」を選んでください。
  - 「適合する種類」を「カーブに合わせる」にします。
  - 「カーブ」のプルダウンからNurbsPathを選びます。
  - 「オフセット（倍率）」の「係数X」を`0.6`にします。
  - 「オフセット（OBJ）」をチェックし、開いて「オブジェクト」のプルダウンからEmptyを選びます。
  - 下図のようになります。

<img src="https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/13955/5715cca2-6ba1-055f-6c01-2a29f2dc6717.png" width="300">

- 「`∨`」をクリックしてたたんでおきましょう。
- 「モディファイアーを追加」から「カーブ」を選んでください。
  - 「カーブオブジェクト」のプルダウンからNurbsPathを選びます。
  - 下図のようになります。

<img src="https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/13955/9a3389f5-a9de-ef23-11e0-1310c2838249.png" width="300">

仕上げに質感を設定しましょう。

- 色を確認できるように**マテリアルプレビューモード**に変えてください。変え方は「はじめに」の紹介記事に書いてあります。
- Torusを選んだまま、プロパティ画面の赤い丸っぽいアイコンをクリックして**マテリアルプロパティ**にしてください。
  - 「新規」を押してください。
  - 「サーフェス」の「メタリック」を`1`にしてください。
  - 「サーフェス」の「粗さ」を`0.1`にしてください。
  - 下図のようになります。

<img src="https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/13955/1be37eee-871b-44f3-3fb1-1f13ff2a5fd4.png" width="300">

- 完成です！

本記事では、少ない手順で完成できるように心がけましたが、オブジェクトやマテリアルに名前をつけた方がわかりやすくなります。また、操作を迷わないように数値入力しましたが、マウス操作で調整することもできます。慣れてきたらマウス操作で調整してみましょう。
Blenderは、覚えることがたくさんあって使いこなすのが大変ですが、いろいろなことができて楽しいので、ぜひ体験してみてください。

参考：いろいろな「[Blenderで作ろう](https://qiita.com/tags/blenderで作ろう)」

以上

