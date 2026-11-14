title: Blenderでサイコロを作ろう
tags: 3DCG 初心者 Blender モデリング Blenderで作ろう
url: https://qiita.com/SaitoTsutomu/items/8888a0cad6b2fe5f480b
created_at: 2021-12-19 08:44:10+09:00
updated_at: 2021-12-22 19:42:33+09:00
body:

## はじめに

「Blenderに興味があるけど、しきいが高そう」という方向けに、なるべくわかりやすくサイコロの作り方を紹介します。
Blenderの基本的な操作方法は、「[Blenderでサッカーボールを作ろう](https://qiita.com/SaitoTsutomu/items/e7e5114a5916843dd068)」に書いてあるので、先にそちらをやってみてください。

## 対象読者

- Blenderで何か作ってみたいけど、難しいと思っている人

## 完成物

<img src="https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/13955/eda464a8-583d-207b-3441-e45961f9768d.png" width="400">
[完成物をSketchfabで見る](https://skfb.ly/orXvF)

## 手順

操作方法は、日本語設定時の表記になっています。日本語設定の方法は、[こちら](https://vook.vc/n/3779#toc-2)を参考にしてください。
macOSでのキーを書いています。Windowsの場合は、`Option`を`Alt`に読み替えてください。
間違えたときは、`Ctrl + Z`で戻ります。それでもよくわからなくなったら、`Ctrl + N`の「新規ファイル」の「全般」で最初からやり直してみてください。

- 色を確認できるように**マテリアルプレビューモード**に変えてください。変え方は「はじめに」の紹介記事に書いてあります。

- 最初にある立方体は使わないので削除します。立方体を選択して`X`、`[Enter]`で削除できます。
- 操作が簡単になるようにアドオンを有効にします。アドオンとは、Blenderを機能拡張をするしくみです。
  - 編集メニューの「プリファレンス」を選び、表示される画面の左側から「アドオン」を選んでください。
  - 下図のように、虫眼鏡のボックスに`extr`と入力して表示される`Add Mesh: Extra Objects`をチェックしてください。チェックしたら画面を閉じてください。

<img src="https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/13955/75509285-41ac-e4b5-5ddd-5655a86a5b35.png" width="700">

- サイコロの元になるオブジェクトを作成しましょう。
  - `Shift + A`で追加メニューが開きます。下図のように「メッシュ」の「Round Cube」を選んでください（以降ではRoundcubeと呼びます）。

<img src="https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/13955/57ea5640-bfff-61f3-2e4c-f2258db02751.png" width="400">

- 画面左下の「Add Round Cube」をクリックして開いてください。下図のように、「分割」の「Arc」を`2`に、「Linear」を`2.0`に、「タイプ」を`全て`にしてください。

<img src="https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/13955/a5f7c1eb-c7a0-e299-9833-71da8de7b727.png" width="360">

- Roundcubeを選択します。
- 右クリックし「スムーズシェード」を選んでください。
- 選択したまま、右下のプロパティ画面で下図のように青いスパナのアイコンをクリックして**モディファイアープロパティ**にしてください。モディファイアーについては「はじめに」の紹介記事も参考にしてください。

<img src="https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/13955/c11e3c02-42af-215c-0d09-effb17a14d0b.jpeg" width="350">

- 「モディファイアーを追加」から「サブディビジョンサーフェス」を選び、「ビューポートのレベル数」と「レンダー」を両方`3`にしてください。下図のようになります。

<img src="https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/13955/e63a0680-ff56-c06b-3de2-ed0d0c26a124.png" width="280">

- 選択したまま、プロパティ画面の赤い丸っぽいアイコンをクリックして**マテリアルプロパティ**にしてください。

<img src="https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/13955/d8c7afc7-b31d-f41d-8d2b-da00e5b9ffcc.png" width="350">

- マテリアルプロパティの「新規」を押してください。新規のマテリアルが作成されます。もう1つマテリアルが欲しいので、ちょっと右上にある「＋」を押してマテリアルを追加してください。もう一度「新規」を押してください。
- 下のマテリアル（`Material.002`）を選択している状態で、少し下にある「ベースカラー」の右の横長の白い四角をクリックして黒にしてください。下図のようになります。黒の指定方法は「はじめに」の紹介記事も参考にしてください。

<img src="https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/13955/a4fb2ecc-0045-3139-efe3-bcc75cbdc3c5.png" width="350">

これからサイコロになっていきます。

- Roundcubeを選択したまま、`[Tab]`を押して**編集モード**にしてください。左上が下図のようになります。`[Tab]`を押すことでオブジェクトモードと編集モードを切り替えできます。

<img src="https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/13955/f80d0e31-8233-592f-a1cb-fb5c04000a78.png" width="240">

- 下図のように「編集モード」の表示の右にある３つのアイコンの右側を選択してください。これは、**面選択モード**です。また、３つのアイコンはそれぞれ「点選択モード」「辺選択モード」「面選択モード」です。

<img src="https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/13955/8523327b-dcd8-2932-d79d-6bb32232707b.png" width="340">

- 下図のように、サイコロの目に当たる部分を選択してください。`Shift`キーを押しながらクリックすると追加選択ができます。画面の回転は、中ボタンを押したままドラッグでできます。なお、選択状態も`Ctrl + Z`で戻せます。「元に戻す」の逆の操作（やり直し）は、`Ctrl + Shift + Z`です。

<table><tr><td>
斜め上から見たところ
<img src="https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/13955/e1b97730-5ae8-4d38-c3f2-62d27040de03.png" width="340">


</td><td>
斜め下から見たところ
<img src="https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/13955/fbd79be4-3487-efd7-55e9-d23ab394fa5d.png" width="340">


</td></tr></table>

- 選択を維持したまま、`I`、`[Enter]`（面を差し込む）。左下の詳細設定画面で、「幅」を`0.01`に、「個別」をチェックしてください。下図のようになります。

<img src="https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/13955/9d920a82-3fbb-08f0-9909-e455ba5f3b8b.png" width="400">

- 選択を維持したまま、`Option + E`（Windowsでは`Alt + E`）を押して「押し出し」メニューを出し、「個々の面で押し出し」を選んで、`-.15`、`[Enter]`を押してください。下図のようになります。もし、サイコロの目がくぼんでなかったら、`-0.15`を`0.15`に変えてみてください。

<img src="https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/13955/2d6c0a4f-8784-5c52-9f7b-3abe7d2c9101.png" width="600">


- 選択を維持したまま、「選択」メニューの「選択の拡大縮小」の「拡大」を選んでください。
- 選択を維持したまま、マテリアルプロパティ画面で、２番目の黒のマテリアル（`Material.002`）を選択して、下図左下の「割り当て」を押してださい。

<img src="https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/13955/f0a67f8e-3ead-01a0-1458-f5712046b6b8.png" width="350">

- 完成です！`[Tab]`を押して、オブジェクトモードに戻り確認してみましょう。

本記事では、少ない手順で完成できるように心がけましたが、オブジェクトやマテリアルに名前をつけた方がわかりやすくなります。また、操作を迷わないように数値入力しましたが、マウス操作で調整することもできます。慣れてきたらマウス操作で調整してみましょう。
Blenderは、覚えることがたくさんあって使いこなすのが大変ですが、いろいろなことができて楽しいので、ぜひ体験してみてください。

参考：いろいろな「[Blenderで作ろう](https://qiita.com/tags/blenderで作ろう)」

以上




