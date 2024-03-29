title: Blenderでサッカーボールを作ろう
tags: 3DCG 初心者 Blender モデリング Blenderで作ろう
url: https://qiita.com/SaitoTsutomu/items/e7e5114a5916843dd068
created_at: 2021-12-10 20:45:58+09:00
updated_at: 2023-01-15 17:46:42+09:00
body:

## サッカーボールを作ろう

「Blenderに興味があるけど、しきいが高そう」という方向けに、なるべくわかりやすくサッカーボールの作り方を紹介します。

Blenderが初めての方は、「[Blender Debut! ステップ１:Blenderをはじめよう](https://vook.vc/n/3779)」や「[初心者向け！Blender超入門講座 - 夏森轄（なつもり かつ）YouTube](https://youtu.be/OoM0ikOi1v4)」が参考になります。

## 対象読者

- Blenderで何か作ってみたいけど、難しいと思っている人

## 完成物

<img src="https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/13955/81e83f16-55b6-b378-5230-984c8a0bb03b.jpeg" width="300">

[完成物をSketchfabで見る](https://skfb.ly/orXuR)

## 手順

操作方法は、日本語設定時の表記になっています。日本語設定の方法は、[こちら](https://vook.vc/n/3779#toc-2)を参考にしてください。
macOSでのキーを書いています。Windowsの場合は、`Option`を`Alt`に読み替えてください。
間違えたときは、`Ctrl + Z`で戻ります。それでもよくわからなくなったら、`Ctrl + N`の「新規ファイル」の「全般」で最初からやり直してみてください。

- Blenderを起動します。インストール後の最初の起動で言語が選択できるので、日本語を選んでください（以降の説明は日本語表記になっています）。
  - Blenderは、**マウスカーソルの位置によってできることが変わります**。以降の作業は、基本的に中央の広い画面で行うので、カーソルがこの画面内にあるようにしましょう（この画面は「**3Dビューポート**」と呼ばれます）。
- Blenderには**オブジェクトの対話モード**があり、対話モードによって処理が変わります。起動時の対話モードは**オブジェクトモード**になっています。もし、オブジェクトモードになっていなかったら、下図のように画面左上で対話モードをオブジェクトモードに変えてください。

<img src="https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/13955/0ceac484-9857-3755-98f6-ee03ba58d32c.jpeg" width="300">

- 3Dビューポートの表示はシェーディングで変わります。起動時はソリッドモードになっています。色を確認できるように**マテリアルプレビューモード**に変えてください。`Z`を押すと下図のような表示になります。この表示をパイメニューといいます。パイメニューは、マウスカーソルを少し動かすと選択肢を切り替えられます。マウスカーソルを少し下のように動かし、図のように真ん中の丸の下を青くしてマウスをクリックしてください。

<img src="https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/13955/76f6bae2-c23a-dc4d-f243-e8d5067a5c2d.jpeg" width="500">

- マテリアルプレビューモードになると、右上が下図のようになります。もし、下図のようになっていなかったら、下図の青いところをクリックしてもマテリアルプレビューモードに変更できます。

<img src="https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/13955/21755d1b-da6f-e581-8b9d-f6ef96655a78.jpeg" width="300">

- 最初にCube（立方体）がありますが、使わないので削除します。
  - Cubeを選択します。Cubeにオレンジ色の枠がつきます（オレンジ色の枠は選択してアクティブになっていることを意味します）。
  - キーボードから`X`を押してください（以降の説明では「押してください」を書かずに単に`X`のように記述します）。
  - メニューが表示されるので「削除」を選んで削除します。

- サッカーボールの元になるオブジェクトを作成しましょう。
  - `Shift + A`で追加メニューが開きます。下図のように「メッシュ」の「ICO球」を選んでください。

<img src="https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/13955/eb23783e-450d-e401-64ba-99c1267a4f23.jpeg" width="500">

- 画面左下の「ICO球を追加」をクリックしてください。この画面で、ICO球のパラメーターを変更できます。下図のように「細分化」を`1`にしてください。数字はクリックすると入力できます。
  - この画面は作成時にだけ表示されます。どこかをクリックすると、この画面は消えてしまいます。その場合、すぐにF9を押すと再表示できます。
  - 「細分化」を1にしたら、下図の「∨ ICO球を追加」の「∨」をクリックして画面を小さくしましょう。
  - このICO球がサッカーボールになります。

<img src="https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/13955/9fafe6cc-b571-8b9c-566a-3c78cdffa018.jpeg" width="400">

- ICO球を選択してください。

<img src="https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/13955/c5b008f4-b0f3-5d64-929a-3946a86b34bb.jpeg" width="300">

- 画面右下のプロパティ画面でいろいろな設定ができます。ここでは、下図のように赤い丸っぽいアイコンをクリックして**マテリアルプロパティ**にしてください。マテリアルは、オブジェクトの質感を表現するものです。

<img src="https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/13955/e16f47e8-a26e-1072-2523-84a39a6dc13d.jpeg" width="400">

- マテリアルプロパティの「新規」を押してください。新規のマテリアルが作成されます。もう1つマテリアルが欲しいので、ちょっと右上にある「＋」を押してマテリアルを追加してください。もう一度「新規」を押してください。下図のようになります。

<img src="https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/13955/bc48f8b1-1b62-4489-34d1-41d8057c6874.jpeg" width="280">

- 下のマテリアル（上図だと`Material.002`）を選択している状態で、少し下にある「ベースカラー」の右にある横長の白い四角をクリックしてください。色の設定画面が出ます。この色の設定画面の右にある縦の四角内を下にドラッグして、下図のように色を黒にしてください。

<img src="https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/13955/5699bf6c-46f5-11b9-6c96-deeb15fa858e.jpeg" width="240">

- プロパティ画面で、下図のように青いスパナのアイコンをクリックして**モディファイアープロパティ**にしてください。ここから6個のモディファイアーを追加していきます。モディファイアーとは、オブジェクトに何らかの処理を追加する機能です。

<img src="https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/13955/0d615a15-4cf4-983f-4ac3-d0414a81323f.jpeg" width="400">

- 最初は「モディファイアーを追加」から「ベベル」を選んでください。
  - 「頂点」を選んでください。
  - 「量」は`0.36`にしてください。
  - 「シェーディング」を開いて「マテリアルインデックス」を`1`にしてください。下図のようになっていればOKです。早速サッカーボールらしくなりました。追加したモディファイアーの左上の「∨」をクリックすると畳むことができます。

<img src="https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/13955/3a2aa8c0-e734-443e-2b5e-8a95ea7f65d4.jpeg" width="640">

- 次に「モディファイアーを追加」から「辺分離」を選んでください。
- 次に「モディファイアーを追加」から「サブディビジョンサーフェス」を選んでください。
  - 「シンプル」を選んでください。
  - 「ビューポートのレベル数」を`2`にしてください。下図のようになっていればOKです。

<img src="https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/13955/2cb0eee3-bce8-2c40-6ccc-585f15fca9f7.jpeg" width="400">

- 次に「モディファイアーを追加」から「キャスト」を選んでください。
  - 「係数」を`1`にしてください。下図のようになっていればOKです。

<img src="https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/13955/49acb732-6ea2-d91b-56e6-5b6bfff168c4.jpeg" width="400">

- 次に「モディファイアーを追加」から「ソリッド化」を選んでください。
- 最後に「モディファイアーを追加」からもう一度「ベベル」を選んでください。下図のようになっていればOKです。

<img src="https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/13955/809c37e5-fa27-fd13-4e5f-4cb5ff6594d8.jpeg" width="400">

- ICO球を選んで、右クリックし「スムーズシェード」を選んでください。

<img src="https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/13955/b53b1b34-02f8-4665-1416-ae0d86e74ae8.jpeg" width="500">

- 完成です！

少ない手順で完成できるように心がけましたが、オブジェクトやマテリアルに名前をつけた方がわかりやすくなることを追記します。

## モディファイアーの補足

ここでは、ICO球に対し、6つのモディファイアーがどのような処理をしているか簡単に紹介します。

- 最初のICO球は細分化を1にしたので、**正二十面体**になっています。この20個の面は、サッカーボールでは20個の白い六角形になります。
- 最初のベベルは頂点ベベルというもので、頂点を削って平らにする処理です。シェーディングのマテリアルインデックスで2番目のマテリアルを選んだので、削った五角形の部分が黒になります。
- 2つ目の辺分離は、六角形と五角形の面をバラバラにする処理です。バラバラにした効果は最後に説明します。
- 3つ目のサブディビジョンサーフェスは、面を分割する処理です。ICO球の細かさを増やしています。
- 4つ目のキャストは、ICO球を丸くする処理です。これにより膨らんだサッカーボールになります。ただし、面が分割されてないと丸くなりません。直前のサブディビジョンサーフェスは、丸くするために必要でした。
- 5つ目のソリッド化は、面に厚みを持たせる処理です。
- 6つ目のベベルは辺ベベルというもので、角を丸くする処理です。厚みがないと角が存在しませんが、直前のソリッド化で厚みができているので、六角形や五角形の角を丸くできます。これにより六角形や五角形の境界がへこんだ感じになります。そもそも、六角形や五角形の周りが丸くなるのは、分離されているからです。辺分離をしていたことで、六角形や五角形の境界がへこんだことになります。

Blenderは、覚えることがたくさんあって使いこなすのが大変ですが、いろいろなことができて楽しいので、ぜひ体験してみてください。

参考：いろいろな「[Blenderで作ろう](https://qiita.com/tags/blenderで作ろう)」

以上

