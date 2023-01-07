title: Blenderチャレンジ：りんごのうさぎ
tags: 3DCG Blender クイズ Blenderチャレンジ
url: https://qiita.com/SaitoTsutomu/items/cfee1dccece3605ce822
created_at: 2023-01-01 22:44:20+09:00
updated_at: 2023-01-01 22:52:58+09:00
body:

3DCGソフトウェアのBlenderを使って、お題のモデルを作成してみましょう。
やり方は一通りではないと思います。あなたは、どんな方法を考えますか？

## 問題

以下のようなオブジェクトを作ってください。

![image.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/13955/917f5f2f-a43b-bf1f-25d3-c9608bf9e662.png)

[完成物をSketchfabで見る](https://skfb.ly/oCosP)

…
…
…

OK？

---

## 解答例

作成する手順です。macOSのキーを書いています。Windowsの場合は、`Option`を`Alt`に読み替えてください。

- `Shift + A`（追加メニュー）の「メッシュ」の「平面」を選びます。
- 編集モードに入り、`X`（削除）の頂点で全部消します。
- `1`でフロントビューにし、下図のように`Ctrl + 右クリック`で点を追加していきます。最後は2点を選んで`F`でつなげます。だいたいでOKです。

![image.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/13955/2f72af6b-9e9f-4548-ee78-3a6def419bb6.png)

- オブジェクトモードに戻り、スクリューモディファイアーを追加し、角度を45に、ビューのステップ数を4にし、適用します。
- `RZ-22.5`、`Space`、`RY-90`、`Space`で向きを整えます。
- 右クリックで自動スムーズを適用します。
- 編集モードに入り、`AF`で面を貼ります。ノーマルが反転しているかもしれないので、`Shift + N`で外向きにしましょう。
- 皮部分にナイフで切り込みを入れ、適当に選択し、`Option + E`（押し出し）の法線に沿って面を押し出しします。
- マテリアルを設定します。

以上

